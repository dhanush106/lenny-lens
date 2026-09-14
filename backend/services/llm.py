from typing import Protocol, Optional
import logging
import time

import httpx

from backend.core.config import settings
from backend.core.exceptions import ServiceUnavailableError
from backend.core.logging import log_event
from backend.services.runtime_config import active_llm_config

logger = logging.getLogger(__name__)


class LLMProvider(Protocol):
    name: str
    model: str

    async def generate_response(
        self, prompt: str, system_prompt: Optional[str] = None, max_tokens: int = 800
    ) -> str:
        ...


class OllamaProvider:
    name = "ollama"

    def __init__(self, base_url: str = "http://127.0.0.1:11434", model: str = "qwen3.5:2b"):
        self.base_url = base_url
        self.model = model

    async def generate_response(
        self, prompt: str, system_prompt: Optional[str] = None, max_tokens: int = 800
    ) -> str:
        started_at = time.perf_counter()
        log_event(logger, "llm_started", provider=self.name, model=self.model)
        try:
            async with httpx.AsyncClient() as client:
                payload = {
                    "model": self.model,
                    "prompt": prompt,
                    "system": system_prompt or "",
                    "stream": False,
                    "think": False,
                    "keep_alive": "10m",
                    "options": {"temperature": 0.2, "num_predict": max_tokens},
                }
                response = await client.post(
                    f"{self.base_url}/api/generate",
                    json=payload,
                    timeout=settings.OLLAMA_TIMEOUT_SECONDS,
                )
                if response.status_code == 404:
                    raise ServiceUnavailableError(
                        "ollama_model_unavailable",
                        f"Ollama does not have model '{self.model}'. Run `ollama pull {self.model}`.",
                    )
                response.raise_for_status()
                data = response.json()
                text = data.get("response", "")
                log_event(
                    logger,
                    "llm_completed",
                    provider=self.name,
                    model=self.model,
                    duration_ms=round((time.perf_counter() - started_at) * 1000, 2),
                )
                return text
        except ServiceUnavailableError:
            raise
        except httpx.TimeoutException as exc:
            log_event(logger, "llm_failed", provider=self.name, model=self.model, error="timeout")
            raise ServiceUnavailableError(
                "ollama_timeout",
                f"Ollama timed out after {settings.OLLAMA_TIMEOUT_SECONDS:.0f}s. Pull a smaller model or raise OLLAMA_TIMEOUT_SECONDS.",
            ) from exc
        except httpx.HTTPError as exc:
            log_event(logger, "llm_failed", provider=self.name, model=self.model, error="unavailable")
            raise ServiceUnavailableError(
                "ollama_unavailable",
                "The configured Ollama server is unavailable. Start Ollama on the host (the API container reaches it at host.docker.internal:11434).",
            ) from exc


class AnthropicProvider:
    name = "anthropic"

    def __init__(self, api_key: str, model: str = "claude-3-haiku-20240307"):
        # Keep the optional cloud SDK out of Ollama startup and test imports.
        from anthropic import AsyncAnthropic

        self.client = AsyncAnthropic(api_key=api_key, timeout=60.0)
        self.model = model

    async def generate_response(
        self, prompt: str, system_prompt: Optional[str] = None, max_tokens: int = 800
    ) -> str:
        from anthropic import APIError

        started_at = time.perf_counter()
        log_event(logger, "llm_started", provider=self.name, model=self.model)
        try:
            response = await self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                system=system_prompt or "",
                messages=[{"role": "user", "content": prompt}],
            )
            text = response.content[0].text
            log_event(
                logger,
                "llm_completed",
                provider=self.name,
                model=self.model,
                duration_ms=round((time.perf_counter() - started_at) * 1000, 2),
            )
            return text
        except APIError as exc:
            log_event(logger, "llm_failed", provider=self.name, model=self.model, error=type(exc).__name__)
            raise ServiceUnavailableError(
                "anthropic_unavailable",
                "Anthropic request failed. Check ANTHROPIC_API_KEY, ANTHROPIC_MODEL, and network access.",
            ) from exc


class OpenAIProvider:
    name = "openai"

    def __init__(self, api_key: str, model: str = "gpt-4.1-mini"):
        # Keep the optional cloud SDK out of Ollama startup and test imports.
        from openai import AsyncOpenAI

        self.client = AsyncOpenAI(api_key=api_key, timeout=60.0)
        self.model = model

    async def generate_response(
        self, prompt: str, system_prompt: Optional[str] = None, max_tokens: int = 800
    ) -> str:
        from openai import APIError

        started_at = time.perf_counter()
        log_event(logger, "llm_started", provider=self.name, model=self.model)
        try:
            response = await self.client.responses.create(
                model=self.model,
                instructions=system_prompt or None,
                input=prompt,
                max_output_tokens=max_tokens,
            )
            text = response.output_text
            log_event(
                logger,
                "llm_completed",
                provider=self.name,
                model=self.model,
                duration_ms=round((time.perf_counter() - started_at) * 1000, 2),
            )
            return text
        except APIError as exc:
            log_event(logger, "llm_failed", provider=self.name, model=self.model, error=type(exc).__name__)
            raise ServiceUnavailableError(
                "openai_unavailable",
                "OpenAI request failed. Check OPENAI_API_KEY, OPENAI_MODEL, and network access.",
            ) from exc


class OpenRouterProvider(OpenAIProvider):
    name = "openrouter"

    def __init__(self, api_key: str, model: str):
        from openai import AsyncOpenAI

        self.client = AsyncOpenAI(
            api_key=api_key, base_url="https://openrouter.ai/api/v1", timeout=60.0
        )
        self.model = model


def configured_model_name() -> str:
    return active_llm_config().model


def get_llm_provider() -> LLMProvider:
    config = active_llm_config()
    provider = config.provider
    if provider == "openai":
        api_key = config.api_key
        if not api_key:
            raise ServiceUnavailableError(
                "missing_openai_api_key",
                "LLM_PROVIDER=openai requires OPENAI_API_KEY in the environment.",
            )
        return OpenAIProvider(api_key=api_key, model=config.model)
    if provider == "anthropic":
        api_key = config.api_key
        if not api_key:
            raise ServiceUnavailableError(
                "missing_anthropic_api_key",
                "LLM_PROVIDER=anthropic requires ANTHROPIC_API_KEY in the environment.",
            )
        return AnthropicProvider(api_key=api_key, model=config.model)
    if provider == "openrouter":
        if not config.api_key:
            raise ServiceUnavailableError("missing_openrouter_api_key", "OpenRouter requires an API key.")
        return OpenRouterProvider(api_key=config.api_key, model=config.model)
    if provider == "ollama":
        return OllamaProvider(base_url=settings.OLLAMA_BASE_URL, model=config.model)
    raise ServiceUnavailableError(
        "unsupported_llm_provider",
        "LLM_PROVIDER must be one of: ollama, openai, anthropic, openrouter.",
    )
