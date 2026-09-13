from backend.services.retrieval import RetrievalService
from backend.services.llm import get_llm_provider
from backend.db.session import AsyncSessionLocal
from backend.core.config import settings

class RAGService:
    def __init__(self):
        self.retrieval_service = RetrievalService()
        self.llm_provider = get_llm_provider()

    async def answer_question(self, query: str, history: list[dict] | None = None) -> dict:
        async with AsyncSessionLocal() as session:
            # 1. Retrieve chunks
            chunks = await self.retrieval_service.search(session, query, top_k=settings.RETRIEVAL_TOP_K)
            chunks = [item for item in chunks if item.score >= settings.RETRIEVAL_MIN_SCORE]
            
            if not chunks:
                return {
                    "answer": "I don't have enough information in the podcast transcripts to answer that question.",
                    "sources": []
                }
            
            # 2. Build context
            context_text = ""
            sources = []
            for idx, item in enumerate(chunks, 1):
                chunk = item.chunk
                context_text += f"\n--- Source [{idx}] {chunk.transcript.title or chunk.transcript.video_id} ---\n{chunk.text}\n"
                sources.append({
                    "id": chunk.id,
                    "transcript_id": chunk.transcript_id,
                    "title": chunk.transcript.title,
                    "video_id": chunk.transcript.video_id,
                    "score": round(item.score, 4),
                    "text_preview": chunk.text[:100] + "..."
                })

            # 3. Build Prompt
            system_prompt = (
                "You are 'The Lenny Growth Assistant', an AI that answers product management and growth questions "
                "strictly using the provided transcripts from Lenny's Podcast. "
                "If the context does not contain enough information to answer the question, state that clearly and do not make up an answer. "
                "Cite your sources using [1], [2], etc."
            )
            
            history_text = "\n".join(f"{item['role']}: {item['content']}" for item in (history or [])[-6:])
            prompt = f"Conversation context:\n{history_text}\n\nTranscript evidence:{context_text}\n\nUser Question:\n{query}"
            
            # 4. Generate answer
            answer = await self.llm_provider.generate_response(prompt, system_prompt=system_prompt)
            
            return {
                "answer": answer,
                "sources": sources
            }
