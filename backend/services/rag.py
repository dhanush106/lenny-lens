from backend.agent.intents import expand_retrieval_query
from backend.services.citations import (
    conversation_history,
    filter_used_sources,
    format_context,
    numbered_sources,
)
from backend.services.retrieval import RetrievalService
from backend.services.llm import get_llm_provider
from backend.db.session import AsyncSessionLocal
from backend.core.config import settings

GROUNDING_SYSTEM_PROMPT = """
You are The Lenny Growth Assistant for product and growth teams.

Answer strictly from the numbered transcript excerpts. Do not invent guests, episodes, companies, metrics, or quotes.

Write in this skimmable shape:
1. **Direct answer** — 2–4 sentences that resolve the question.
2. **What guests said** — evidence with inline citations like [1] and [2] after each claim.
3. **How to apply** — a concrete next step a PM or growth lead can try this week. Label this as synthesis.
4. **Gaps** — say what the excerpts do not cover. If they cannot support the question, say so and stop.

Rules:
- Cite every substantive claim with [n] matching the provided sources.
- Do not infer a comparison from a source that only discusses one side.
- Never pad with generic startup advice that is not in the excerpts.
""".strip()


class RAGService:
    def __init__(self):
        self.retrieval_service = RetrievalService()
        self.llm_provider = get_llm_provider()

    async def answer_question(self, query: str, history: list[dict] | None = None) -> dict:
        retrieval_query = expand_retrieval_query(query, history)
        async with AsyncSessionLocal() as session:
            chunks = await self.retrieval_service.search(session, retrieval_query, top_k=settings.RETRIEVAL_TOP_K)
            chunks = [item for item in chunks if item.score >= settings.RETRIEVAL_MIN_SCORE]

            if not chunks:
                return {
                    "answer": (
                        "I don't have enough evidence in Lenny's podcast transcripts to answer that. "
                        "Try a product, growth, or GTM topic covered in the ingested corpus."
                    ),
                    "sources": [],
                }

            sources = numbered_sources(chunks)
            history_text = conversation_history(history)
            prompt = (
                f"Conversation context:\n{history_text or '(none)'}\n\n"
                f"Transcript evidence:\n{format_context(chunks)}\n\n"
                f"User Question:\n{query}"
            )
            answer = await self.llm_provider.generate_response(
                prompt,
                system_prompt=GROUNDING_SYSTEM_PROMPT,
                max_tokens=900,
            )
            return {"answer": answer, "sources": filter_used_sources(answer, sources)}
