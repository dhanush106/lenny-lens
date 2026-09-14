import re

from backend.agent.intents import expand_retrieval_query
from backend.agent.skills.ship30_playbook import SHIP30_SYSTEM_PROMPT
from backend.services.citations import (
    citation_footer,
    conversation_history,
    filter_used_sources,
    format_context,
    numbered_sources,
)
from backend.services.llm import get_llm_provider
from backend.services.retrieval import RetrievalService
from backend.db.session import AsyncSessionLocal
from backend.core.config import settings


def essay_title(markdown: str, fallback: str = "Ship 30 essay") -> str:
    for line in markdown.splitlines():
        stripped = line.strip()
        if stripped.startswith("#"):
            return re.sub(r"^#+\s*", "", stripped).strip() or fallback
    return fallback[:80]


class EssaySkill:
    """Dedicated Ship 30 for 30 skill: retrieve evidence, then write to the playbook."""

    def __init__(self):
        self.llm = get_llm_provider()
        self.retrieval_service = RetrievalService()

    async def execute(self, query: str, history: list[dict] | None = None) -> dict:
        retrieval_query = expand_retrieval_query(query, history)
        async with AsyncSessionLocal() as session:
            chunks = await self.retrieval_service.search(session, retrieval_query, top_k=settings.RETRIEVAL_TOP_K)
            chunks = [item for item in chunks if item.score >= settings.RETRIEVAL_MIN_SCORE]

            if not chunks:
                return {
                    "answer": "I don't have enough information in the podcast transcripts to write a grounded Ship 30 essay on that topic.",
                    "sources": [],
                }

            sources = numbered_sources(chunks)
            prompt = (
                f"Conversation context:\n{conversation_history(history) or '(none)'}\n\n"
                f"Transcript evidence:\n{format_context(chunks)}\n\n"
                f"Essay request:\n{query}"
            )
            essay = await self.llm.generate_response(
                prompt, system_prompt=SHIP30_SYSTEM_PROMPT, max_tokens=4500
            )
            used = filter_used_sources(essay, sources)
            footer = citation_footer(used)
            if footer and "## Sources" not in essay:
                essay = f"{essay.rstrip()}\n\n## Sources\n\n{footer}\n"
            title = essay_title(essay)
            return {
                "answer": f"Wrote a Ship 30 for 30 essay: {title}",
                "sources": used,
                "artifact": {
                    "type": "markdown",
                    "title": title,
                    "content": essay,
                    "summary": f"Ship 30 essay grounded in {len(used)} transcript sources.",
                },
            }
