from typing import List, Protocol

import httpx

from backend.core.config import settings
from backend.core.exceptions import ServiceUnavailableError

class EmbeddingProvider(Protocol):
    model_name: str
    dimensions: int
    async def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        ...

    async def generate_embedding(self, text: str) -> List[float]:
        ...

class MockEmbeddingProvider:
    """
    A mock provider for local development without API keys.
    Returns a dummy vector of 1536 dimensions (OpenAI's size) or 384 (all-MiniLM-L6-v2 size).
    """
    def __init__(self, dimensions: int = 384):
        self.dimensions = dimensions
        self.model_name = "mock-embedding"

    async def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        # In a real implementation, this would call an API or a local model.
        return [[0.1] * self.dimensions for _ in texts]

    async def generate_embedding(self, text: str) -> List[float]:
        return [0.1] * self.dimensions

class OllamaEmbeddingProvider:
    def __init__(self, base_url: str, model: str, dimensions: int):
        self.base_url = base_url.rstrip("/")
        self.model_name = model
        self.dimensions = dimensions

    async def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    f"{self.base_url}/api/embed", json={"model": self.model_name, "input": texts}
                )
                response.raise_for_status()
                embeddings = response.json().get("embeddings", [])
        except httpx.HTTPError as exc:
            raise ServiceUnavailableError(
                "embedding_unavailable",
                "The configured embedding model is unavailable. Start Ollama and pull the embedding model.",
            ) from exc

        if len(embeddings) != len(texts) or any(len(vector) != self.dimensions for vector in embeddings):
            raise ServiceUnavailableError(
                "embedding_configuration_error",
                f"Embedding model '{self.model_name}' did not return {self.dimensions}-dimension vectors.",
            )
        return embeddings

    async def generate_embedding(self, text: str) -> List[float]:
        return (await self.generate_embeddings([text]))[0]


def get_embedding_provider() -> EmbeddingProvider:
    if settings.EMBEDDING_PROVIDER.lower() == "mock":
        return MockEmbeddingProvider(settings.EMBEDDING_DIMENSIONS)
    return OllamaEmbeddingProvider(
        settings.OLLAMA_BASE_URL,
        settings.OLLAMA_EMBEDDING_MODEL,
        settings.EMBEDDING_DIMENSIONS,
    )
