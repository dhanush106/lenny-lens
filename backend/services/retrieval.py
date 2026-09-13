from sqlalchemy.ext.asyncio import AsyncSession
from dataclasses import dataclass
import json
import logging
import time
from typing import List

from sqlalchemy import select
from sqlalchemy.orm import joinedload

from backend.models.chunk import Chunk
from backend.services.embeddings import get_embedding_provider


@dataclass
class RetrievedChunk:
    chunk: Chunk
    score: float

class RetrievalService:
    def __init__(self):
        self.embedding_provider = get_embedding_provider()

    async def search(self, db: AsyncSession, query: str, top_k: int = 5) -> List[RetrievedChunk]:
        started_at = time.perf_counter()
        # Do not call the embedding provider when there is no corpus. An empty
        # knowledge base is an evidence problem, not an Ollama outage.
        if await db.scalar(select(Chunk.id).where(Chunk.embedding.is_not(None)).limit(1)) is None:
            return []

        # 1. Generate embedding for query
        query_embedding = await self.embedding_provider.generate_embedding(query)
        
        # 2. Perform cosine similarity search using pgvector
        # <-> is L2 distance, <=> is cosine distance, <#> is inner product
        # pgvector uses <=> for cosine distance
        
        distance = Chunk.embedding.cosine_distance(query_embedding)
        result = await db.execute(
            select(Chunk, (1 - distance).label("score"))
            .options(joinedload(Chunk.transcript))
            .where(Chunk.embedding.is_not(None))
            .order_by(distance)
            .limit(top_k)
        )
        retrieved = [RetrievedChunk(chunk=row[0], score=float(row[1])) for row in result.all()]
        logging.getLogger(__name__).info(json.dumps({
            "event": "retrieval",
            "query": query[:200],
            "results": len(retrieved),
            "top_score": retrieved[0].score if retrieved else None,
            "duration_ms": round((time.perf_counter() - started_at) * 1000, 2),
        }))
        return retrieved
