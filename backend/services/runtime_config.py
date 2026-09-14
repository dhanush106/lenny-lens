from dataclasses import dataclass

from backend.core.config import settings
from backend.core.exceptions import ServiceUnavailableError


SUPPORTED_PROVIDERS = {"ollama", "openai", "anthropic", "openrouter"}


@dataclass
class ActiveLLMConfig:
    provider: str
    model: str
    api_key: str = ""


def _env_config() -> ActiveLLMConfig:
    provider = settings.LLM_PROVIDER.lower()
    if provider == "openai":
        return ActiveLLMConfig(provider, settings.OPENAI_MODEL, settings.OPENAI_API_KEY)
    if provider == "anthropic":
        return ActiveLLMConfig(provider, settings.ANTHROPIC_MODEL, settings.ANTHROPIC_API_KEY)
    return ActiveLLMConfig("ollama", settings.OLLAMA_MODEL)


_active = _env_config()


def active_llm_config() -> ActiveLLMConfig:
    return _active


def set_active_llm_config(provider: str, model: str, api_key: str = "") -> ActiveLLMConfig:
    provider = provider.lower().strip()
    model = model.strip()
    if provider not in SUPPORTED_PROVIDERS:
        raise ServiceUnavailableError("unsupported_llm_provider", "Choose Ollama, OpenAI, Claude, or OpenRouter.")
    if not model:
        raise ServiceUnavailableError("missing_llm_model", "Choose a model before applying the LLM configuration.")
    if provider != "ollama" and not api_key.strip():
        raise ServiceUnavailableError("missing_llm_api_key", "A cloud provider requires an API key.")
    global _active
    _active = ActiveLLMConfig(provider, model, api_key.strip())
    return _active
