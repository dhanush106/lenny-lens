from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import text
from typing import List

from backend.models.chunk import Chunk
from backend.services.embeddings import get_embedding_provider

class RetrievalService:
    def __init__(self):
        self.embedding_provider = get_embedding_provider()

    async def search(self, db: AsyncSession, query: str, top_k: int = 5) -> List[Chunk]:
        # 1. Generate embedding for query
        query_embedding = await self.embedding_provider.generate_embedding(query)
        
        # 2. Perform cosine similarity search using pgvector
        # <-> is L2 distance, <=> is cosine distance, <#> is inner product
        # pgvector uses <=> for cosine distance
        
        result = await db.execute(
            select(Chunk)
            .order_by(Chunk.embedding.cosine_distance(query_embedding))
            .limit(top_k)
        )
        
        return result.scalars().all()
