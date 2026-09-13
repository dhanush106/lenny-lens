from typing import Protocol, Optional
import httpx
# pyrefly: ignore [missing-import]
from anthropic import AsyncAnthropic
from backend.core.config import settings
from backend.core.exceptions import ServiceUnavailableError

class LLMProvider(Protocol):
    async def generate_response(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        ...

class OllamaProvider:
    def __init__(self, base_url: str = "http://127.0.0.1:11434", model: str = "llama3"):
        self.base_url = base_url
        self.model = model

    async def generate_response(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        try:
            async with httpx.AsyncClient() as client:
                payload = {
                    "model": self.model,
                    "prompt": prompt,
                    "system": system_prompt or "",
                    "stream": False
                }
                response = await client.post(f"{self.base_url}/api/generate", json=payload, timeout=60.0)
                response.raise_for_status()
                data = response.json()
                return data.get("response", "")
        except httpx.HTTPError as exc:
            raise ServiceUnavailableError(
                "ollama_unavailable",
                "The configured Ollama model is unavailable. Start Ollama and pull the configured model.",
            ) from exc

class AnthropicProvider:
    def __init__(self, api_key: str, model: str = "claude-3-haiku-20240307"):
        self.client = AsyncAnthropic(api_key=api_key)
        self.model = model

    async def generate_response(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        messages = [{"role": "user", "content": prompt}]
        
        response = await self.client.messages.create(
            model=self.model,
            max_tokens=4096,
            system=system_prompt or "",
            messages=messages
        )
        return response.content[0].text

def get_llm_provider() -> LLMProvider:
    provider = settings.LLM_PROVIDER.lower()
    if provider == "anthropic":
        api_key = settings.ANTHROPIC_API_KEY
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY is missing")
        return AnthropicProvider(api_key=api_key)
    else:
        # Default to Ollama
        return OllamaProvider(base_url=settings.OLLAMA_BASE_URL, model=settings.OLLAMA_MODEL)
