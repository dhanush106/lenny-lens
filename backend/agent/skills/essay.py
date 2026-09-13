from backend.services.llm import get_llm_provider
from backend.services.retrieval import RetrievalService
from backend.db.session import AsyncSessionLocal

class EssaySkill:
    def __init__(self):
        self.llm = get_llm_provider()
        self.retrieval_service = RetrievalService()

    async def execute(self, query: str) -> dict:
        async with AsyncSessionLocal() as session:
            # 1. Retrieve transcripts context
            chunks = await self.retrieval_service.search(session, query, top_k=5)
            
            if not chunks:
                return {
                    "answer": "I don't have enough information in the podcast transcripts to write an essay on that topic.",
                    "sources": []
                }
            
            context_text = ""
            sources = []
            for idx, chunk in enumerate(chunks, 1):
                context_text += f"\n--- Source [{idx}] ---\n{chunk.text}\n"
                sources.append({
                    "id": chunk.id,
                    "transcript_id": chunk.transcript_id,
                    "text_preview": chunk.text[:100] + "..."
                })

            # 2. Build Ship 30 for 30 Essay Prompt
            system_prompt = (
                "You are an expert essay writer using the 'Ship 30 for 30' principles. "
                "Write an essay based on the provided user topic and strictly grounded in the provided context. "
                "Your essay should be approximately 1,250 words and must include:\n"
                "- A strong hook and clear narrative progression.\n"
                "- Skimmable formatting with headings, bullets, and selective bold emphasis.\n"
                "- A specific, useful takeaway.\n"
                "Do NOT hallucinate information outside of the provided context. "
                "Cite sources when making claims using [1], [2], etc."
            )
            
            prompt = f"Context:\n{context_text}\n\nEssay Topic:\n{query}"
            
            answer = await self.llm.generate_response(prompt, system_prompt=system_prompt)
            
            return {
                "answer": answer,
                "sources": sources
            }
