"""Safe, read-only knowledge-base diagnostics.

Run with: python -m backend.scripts.diagnostics --query "product discovery versus execution"
"""

import argparse
import asyncio

from sqlalchemy import func, select

from backend.db.session import AsyncSessionLocal
from backend.models import Chunk, Transcript
from backend.services.embeddings import get_embedding_provider
from backend.services.retrieval import RetrievalService
from backend.core.config import settings


async def main() -> None:
    parser = argparse.ArgumentParser(description="Inspect LennyLens knowledge-base readiness")
    parser.add_argument("--query", help="Optional query to test vector retrieval")
    args = parser.parse_args()

    provider = get_embedding_provider()
    async with AsyncSessionLocal() as session:
        transcript_count = await session.scalar(select(func.count()).select_from(Transcript))
        chunk_count = await session.scalar(select(func.count()).select_from(Chunk))
        embedded_count = await session.scalar(
            select(func.count()).select_from(Chunk).where(Chunk.embedding.is_not(None))
        )

        print("Knowledge Base Diagnostics")
        print("--------------------------")
        print(f"Database: connected")
        print(f"Transcripts: {transcript_count}")
        print(f"Chunks: {chunk_count}")
        print(f"Chunks with embeddings: {embedded_count}")
        print(f"Retrieval mode: {settings.RETRIEVAL_MODE}")
        print(f"Embedding model: {provider.model_name}")
        print(f"Embedding dimension: {provider.dimensions}")

        if not args.query:
            return

        print(f"\nQuery: {args.query}")
        results = await RetrievalService().search(session, args.query)
        print(f"Vector search: working ({len(results)} results)")
        for index, result in enumerate(results, 1):
            chunk = result.chunk
            title = chunk.transcript.title or chunk.transcript.video_id
            preview = " ".join(chunk.text.split())[:160]
            print(f"{index}. Episode: {title}")
            print(f"   score: {result.score:.4f}; chunk: {chunk.id}; source: {chunk.transcript_id}")
            print(f"   preview: {preview}")


if __name__ == "__main__":
    asyncio.run(main())
