from typing import List, Protocol

class EmbeddingProvider(Protocol):
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

    async def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        # In a real implementation, this would call an API or a local model.
        return [[0.1] * self.dimensions for _ in texts]

    async def generate_embedding(self, text: str) -> List[float]:
        return [0.1] * self.dimensions

def get_embedding_provider() -> EmbeddingProvider:
    return MockEmbeddingProvider()
