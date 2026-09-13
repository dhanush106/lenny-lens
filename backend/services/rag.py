from backend.services.retrieval import RetrievalService
from backend.services.llm import get_llm_provider
from backend.db.session import AsyncSessionLocal

class RAGService:
    def __init__(self):
        self.retrieval_service = RetrievalService()
        self.llm_provider = get_llm_provider()

    async def answer_question(self, query: str) -> dict:
        async with AsyncSessionLocal() as session:
            # 1. Retrieve chunks
            chunks = await self.retrieval_service.search(session, query, top_k=5)
            
            if not chunks:
                return {
                    "answer": "I don't have enough information in the podcast transcripts to answer that question.",
                    "sources": []
                }
            
            # 2. Build context
            context_text = ""
            sources = []
            for idx, chunk in enumerate(chunks, 1):
                context_text += f"\n--- Source [{idx}] ---\n{chunk.text}\n"
                sources.append({
                    "id": chunk.id,
                    "transcript_id": chunk.transcript_id,
                    "text_preview": chunk.text[:100] + "..."
                })

            # 3. Build Prompt
            system_prompt = (
                "You are 'The Lenny Growth Assistant', an AI that answers product management and growth questions "
                "strictly using the provided transcripts from Lenny's Podcast. "
                "If the context does not contain enough information to answer the question, state that clearly and do not make up an answer. "
                "Cite your sources using [1], [2], etc."
            )
            
            prompt = f"Context from transcripts:\n{context_text}\n\nUser Question:\n{query}"
            
            # 4. Generate answer
            answer = await self.llm_provider.generate_response(prompt, system_prompt=system_prompt)
            
            return {
                "answer": answer,
                "sources": sources
            }
