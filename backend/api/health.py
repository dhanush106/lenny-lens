import httpx
from fastapi import APIRouter, HTTPException
from sqlalchemy import text

from backend.core.config import settings
from backend.db.session import AsyncSessionLocal
from backend.schemas.health import (
    HealthResponse,
    LLMConfigurationRequest,
    ModelListRequest,
    ReadinessResponse,
    RuntimeResponse,
)
from backend.services.llm import configured_model_name
from backend.services.runtime_config import active_llm_config, set_active_llm_config

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Process liveness. Does not touch the database."""
    return HealthResponse(status="ok", environment=settings.ENVIRONMENT)


@router.get("/ready", response_model=ReadinessResponse)
async def readiness_check():
    """Readiness: PostgreSQL must accept a query."""
    try:
        async with AsyncSessionLocal() as session:
            await session.execute(text("SELECT 1"))
        return ReadinessResponse(
            status="ok",
            database="ok",
            llm_provider=settings.LLM_PROVIDER,
            llm_model=configured_model_name(),
            retrieval_mode=settings.RETRIEVAL_MODE,
        )
    except Exception:
        return ReadinessResponse(
            status="degraded",
            database="unavailable",
            llm_provider=settings.LLM_PROVIDER,
            llm_model=configured_model_name(),
            retrieval_mode=settings.RETRIEVAL_MODE,
            detail="PostgreSQL is not reachable. Check docker compose ps and DATABASE_URL.",
        )


@router.get("/runtime", response_model=RuntimeResponse)
async def runtime_config():
    """Evaluator-visible model selection. Never includes secrets."""
    active = active_llm_config()
    active_provider = active.provider
    providers = [
        {"id": "ollama", "label": "Ollama (local)", "model": active.model if active_provider == "ollama" else settings.OLLAMA_MODEL,
         "selected": active_provider == "ollama", "configured": bool(settings.OLLAMA_BASE_URL)},
        {"id": "openai", "label": "ChatGPT / OpenAI", "model": active.model if active_provider == "openai" else settings.OPENAI_MODEL,
         "selected": active_provider == "openai", "configured": bool(active.api_key if active_provider == "openai" else settings.OPENAI_API_KEY)},
        {"id": "anthropic", "label": "Claude", "model": active.model if active_provider == "anthropic" else settings.ANTHROPIC_MODEL,
         "selected": active_provider == "anthropic", "configured": bool(active.api_key if active_provider == "anthropic" else settings.ANTHROPIC_API_KEY)},
        {"id": "openrouter", "label": "OpenRouter", "model": active.model if active_provider == "openrouter" else "Choose from catalog",
         "selected": active_provider == "openrouter", "configured": bool(active.api_key if active_provider == "openrouter" else "")},
    ]
    return RuntimeResponse(
        provider=active.provider,
        model=configured_model_name(),
        retrieval_mode=settings.RETRIEVAL_MODE,
        embedding_model=settings.OLLAMA_EMBEDDING_MODEL,
        environment=settings.ENVIRONMENT,
        providers=providers,
    )


@router.put("/runtime", response_model=RuntimeResponse)
async def update_runtime_config(payload: LLMConfigurationRequest):
    """Apply a demo LLM selection in memory. API keys are never returned or persisted."""
    try:
        set_active_llm_config(payload.provider, payload.model, payload.api_key)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return await runtime_config()


@router.post("/runtime/models")
async def list_models(payload: ModelListRequest):
    """Discover locally installed Ollama models or cloud catalog models."""
    provider = payload.provider.lower().strip()
    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            if provider == "ollama":
                configured_url = settings.OLLAMA_BASE_URL.rstrip("/")
                # Docker needs host.docker.internal while a locally-run backend needs localhost.
                candidates = list(dict.fromkeys([
                    configured_url,
                    "http://127.0.0.1:11434",
                    "http://localhost:11434",
                    "http://host.docker.internal:11434",
                ]))
                failures = []
                for base_url in candidates:
                    try:
                        response = await client.get(f"{base_url}/api/tags")
                        response.raise_for_status()
                        models = sorted(item["name"] for item in response.json().get("models", []) if item.get("name"))
                        return {"models": models, "source": base_url}
                    except httpx.HTTPError as exc:
                        failures.append(f"{base_url}: {type(exc).__name__}")
                raise HTTPException(
                    status_code=502,
                    detail="Ollama is not reachable. Start Ollama, then run `ollama pull qwen3.5:2b`. "
                    f"Tried: {', '.join(failures)}",
                )
            if provider == "openrouter":
                headers = {"Authorization": f"Bearer {payload.api_key}"} if payload.api_key else {}
                response = await client.get("https://openrouter.ai/api/v1/models", headers=headers)
                response.raise_for_status()
                return {"models": sorted(item["id"] for item in response.json().get("data", []))}
            if provider == "openai":
                if not payload.api_key:
                    raise HTTPException(status_code=400, detail="Enter an OpenAI API key to load models.")
                response = await client.get("https://api.openai.com/v1/models", headers={"Authorization": f"Bearer {payload.api_key}"})
                response.raise_for_status()
                return {"models": sorted(item["id"] for item in response.json().get("data", []) if item["id"].startswith("gpt-") )}
            if provider == "anthropic":
                return {"models": [settings.ANTHROPIC_MODEL]}
        raise HTTPException(status_code=400, detail="Unknown LLM provider.")
    except HTTPException:
        raise
    except httpx.HTTPError as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Could not load {provider} models ({type(exc).__name__}). Check the API key and network connection.",
        ) from exc
