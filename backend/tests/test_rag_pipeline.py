from unittest.mock import patch
import uuid

import pytest
from sqlalchemy import delete

from backend.models import Chunk, Transcript
from backend.db.session import AsyncSessionLocal
from backend.services.embeddings import MockEmbeddingProvider
from backend.services.rag import RAGService
from backend.services.retrieval import RetrievedChunk, RetrievalService


@pytest.mark.asyncio
async def test_retrieval_returns_relevant_chunks_for_product_question():
    video_id = f"retrieval-test-{uuid.uuid4()}"
    service = RetrievalService()
    service.embedding_provider = MockEmbeddingProvider()

    async with AsyncSessionLocal() as session:
        transcript = Transcript(video_id=video_id, title="Product discovery interview")
        session.add(transcript)
        await session.flush()
        session.add(
            Chunk(
                transcript_id=transcript.id,
                start_time=0,
                end_time=42,
                text="Strong product teams use discovery interviews before committing to execution.",
                embedding=[0.1] * 384,
            )
        )
        await session.commit()

        try:
            results = await service.search(session, "product discovery versus execution")
            assert results
            assert results[0].chunk.text
            assert results[0].chunk.transcript_id == transcript.id
            assert results[0].chunk.transcript.title == "Product discovery interview"
            assert -1.0 <= results[0].score <= 1.0
        finally:
            await session.execute(delete(Chunk).where(Chunk.transcript_id == transcript.id))
            await session.execute(delete(Transcript).where(Transcript.id == transcript.id))
            await session.commit()


class FakeLLM:
    async def generate_response(self, prompt: str, system_prompt: str | None = None, max_tokens: int = 800) -> str:
        assert "Product discovery evidence" in prompt
        return "Teams validate problems before execution. [1]"


class FakeRetrieval:
    async def search(self, db, query: str, top_k: int):
        transcript = Transcript(id=99, video_id="source-99", title="Product discovery evidence")
        chunk = Chunk(id=123, transcript_id=99, start_time=0, end_time=0, text="Validate the problem before building.")
        chunk.transcript = transcript
        return [RetrievedChunk(chunk=chunk, score=0.82)]


class _FakeSession:
    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        return False


@pytest.mark.asyncio
async def test_qna_pipeline_returns_grounded_answer_and_sources():
    service = RAGService()
    service.retrieval_service = FakeRetrieval()
    service.llm_provider = FakeLLM()

    with patch("backend.services.rag.AsyncSessionLocal", return_value=_FakeSession()):
        response = await service.answer_question("How should teams approach discovery?")

    assert response["answer"] == "Teams validate problems before execution. [1]"
    assert len(response["sources"]) == 1
    source = response["sources"][0]
    assert source["n"] == 1
    assert source["title"] == "Product discovery evidence"
    assert source["video_id"] == "source-99"
    assert source["chunk_id"] == 123
    assert source["excerpt"].startswith("Validate the problem")
    assert source["start_seconds"] is None
