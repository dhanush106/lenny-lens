from sqlalchemy.ext.asyncio import AsyncSession
from dataclasses import dataclass
import logging
import re
import time
from typing import Any, List

from sqlalchemy import func, select
from sqlalchemy.orm import joinedload

from backend.models.chunk import Chunk
from backend.models.transcript import Transcript
from backend.services.embeddings import get_embedding_provider
from backend.core.config import settings
from backend.core.logging import log_event


@dataclass
class RetrievedChunk:
    chunk: Chunk
    score: float


@dataclass
class QueryIntent:
    domain: list[str]
    concepts: list[str]
    task: str
    constraints: list[str]
    expanded_terms: list[str]


_STOP_WORDS = {
    "about", "according", "and", "are", "based", "create", "does", "for", "from",
    "give", "how", "include", "into", "is", "just", "key", "lenny", "only", "our",
    "podcast", "principles", "product", "relevant", "short", "tell", "the", "this",
    "transcripts", "what", "with", "your",
}
_CONCEPT_GROUPS = {
    "growth": {"growth", "activation", "retention", "monetization", "acquisition", "experimentation", "growth loops", "metrics", "user behavior", "product-led growth"},
    "product": {"product strategy", "discovery", "prioritization", "experimentation", "user behavior", "metrics"},
    "retention": {"retention", "churn", "engagement", "habit", "activation", "monetization"},
    "activation": {"activation", "onboarding", "user behavior", "conversion", "retention", "monetization"},
    "engineering": {"engineering management", "engineering", "management", "one-on-ones", "team", "leadership"},
    "startup": {"startup", "founder", "fundraising", "market", "growth", "customers"},
}


def _terms(text: str) -> list[str]:
    return [term for term in re.findall(r"[a-z][a-z-]{2,}", text.lower()) if term not in _STOP_WORDS]


def understand_query(query: str) -> QueryIntent:
    normalized = query.lower()
    terms = _terms(normalized)
    concepts: set[str] = set()
    domain: set[str] = set()
    for key, related in _CONCEPT_GROUPS.items():
        if key in normalized or any(term in terms for term in key.split()):
            domain.add("engineering" if key == "engineering" else key)
            concepts.update(related)
    if not concepts:
        concepts.update(terms)
    if "growth" in normalized or any(item in normalized for item in ("activation", "retention", "monetization")):
        domain.update({"product", "growth"})
    task = "artifact_generation" if any(item in normalized for item in ("artifact", "markdown", "html", "principles")) else "question_answering"
    constraints = []
    if "transcript" in normalized or "lenny" in normalized:
        constraints.append("Lenny transcripts only")
    if "grounded" in normalized or "based only" in normalized:
        constraints.append("grounded")
    count_match = re.search(r"\b(\d+)\s+(?:principles|ideas|tactics|steps)\b", normalized)
    if count_match:
        constraints.append(f"{count_match.group(1)} {count_match.group(0).split(maxsplit=1)[1]}")
    expanded = list(dict.fromkeys(terms + sorted(concepts)))
    return QueryIntent(sorted(domain), sorted(concepts), task, constraints, expanded)


def rerank_candidates(candidates: list[RetrievedChunk], intent: QueryIntent) -> list[RetrievedChunk]:
    """Rerank lexical/vector candidates using query concepts and episode metadata."""
    query_terms = set(intent.expanded_terms)
    scored: list[RetrievedChunk] = []
    for item in candidates:
        transcript = item.chunk.transcript
        title = (getattr(transcript, "title", "") or "").lower()
        text = (item.chunk.text or "").lower()
        title_hits = sum(1 for term in query_terms if term in title)
        text_hits = sum(1 for term in query_terms if term in text)
        concept_hits = sum(1 for concept in intent.concepts if concept in text or concept in title)
        # Preserve the database score while rewarding substantive concept coverage.
        score = (item.score * 0.45) + min(0.25, title_hits * 0.05) + min(0.25, text_hits * 0.02) + min(0.35, concept_hits * 0.07)
        scored.append(RetrievedChunk(chunk=item.chunk, score=score))
    return sorted(scored, key=lambda item: item.score, reverse=True)

class RetrievalService:
    def __init__(self):
        self.embedding_provider = get_embedding_provider()

    async def search(self, db: AsyncSession, query: str, top_k: int = 5) -> List[RetrievedChunk]:
        started_at = time.perf_counter()
        intent = understand_query(query)
        candidate_limit = max(top_k * 5, 20)
        candidate_rows: dict[int, RetrievedChunk] = {}
        # Do not call any provider when there is no corpus. An empty knowledge
        # base is an evidence problem, not a model outage.
        if await db.scalar(select(Chunk.id).limit(1)) is None:
            return []

        if settings.RETRIEVAL_MODE.lower() in {"lexical", "hybrid"}:
            # Build an OR query from meaningful words. Full websearch syntax
            # treats a natural-language comparison such as "discovery versus
            # execution" as an AND query, which over-filters useful evidence.
            stop_words = {
                *_STOP_WORDS, "compare", "successful", "teams", "versus",
            }
            terms = [
                term for term in re.findall(r"[a-zA-Z]{3,}", query.lower())
                if term not in stop_words
            ]
            terms = list(dict.fromkeys(terms + intent.expanded_terms))
            if not terms:
                return []

            query_terms = func.plainto_tsquery("english", terms[0])
            for term in terms[1:]:
                query_terms = query_terms.op("||")(func.plainto_tsquery("english", term))

            document = func.to_tsvector(
                "english", func.coalesce(Transcript.title, "") + " " + Chunk.text
            )
            score = func.ts_rank_cd(document, query_terms)
            result = await db.execute(
                select(Chunk, score.label("score"))
                .options(joinedload(Chunk.transcript))
                .join(Chunk.transcript)
                .where(document.op("@@")(query_terms))
                .order_by(score.desc())
                .limit(candidate_limit)
            )
            for row in result.all():
                candidate_rows[row[0].id] = RetrievedChunk(chunk=row[0], score=float(row[1]))
        if settings.RETRIEVAL_MODE.lower() in {"semantic", "hybrid"}:
            # Semantic mode requires an embedding endpoint and matching vectors
            # generated during ingestion.
            query_embedding = await self.embedding_provider.generate_embedding(query)
            distance = Chunk.embedding.cosine_distance(query_embedding)
            result = await db.execute(
                select(Chunk, (1 - distance).label("score"))
                .options(joinedload(Chunk.transcript))
                .where(Chunk.embedding.is_not(None))
                .order_by(distance)
                .limit(candidate_limit)
            )
            for row in result.all():
                existing = candidate_rows.get(row[0].id)
                semantic_score = float(row[1])
                if existing:
                    existing.score = (existing.score + semantic_score) / 2
                else:
                    candidate_rows[row[0].id] = RetrievedChunk(chunk=row[0], score=semantic_score)
        retrieved = list(candidate_rows.values())
        reranked = rerank_candidates(retrieved, intent)
        log_event(
            logging.getLogger(__name__),
            "retrieval_diagnostics",
            query=query,
            interpreted_intent=intent.__dict__,
            candidate_count=len(retrieved),
            top_candidates=[_candidate_diagnostic(item) for item in reranked[:10]],
        )
        retrieved = diversify_chunks(
            reranked,
            top_k=top_k,
            max_per_transcript=settings.RETRIEVAL_MAX_PER_TRANSCRIPT,
        )
        selected_ids = {item.chunk.id for item in retrieved}
        log_event(
            logging.getLogger(__name__),
            "retrieval_selection",
            selected_candidates=[_candidate_diagnostic(item) for item in retrieved],
            rejected_candidates=[
                _candidate_diagnostic(item) for item in reranked if item.chunk.id not in selected_ids
            ][:20],
        )
        log_event(
            logging.getLogger(__name__),
            "retrieval_completed",
            query_chars=len(query),
            results=len(retrieved),
            top_score=retrieved[0].score if retrieved else None,
            duration_ms=round((time.perf_counter() - started_at) * 1000, 2),
            mode=settings.RETRIEVAL_MODE,
        )
        return retrieved


def _candidate_diagnostic(item: RetrievedChunk) -> dict[str, Any]:
    transcript = item.chunk.transcript
    return {
        "chunk_id": item.chunk.id,
        "transcript_id": item.chunk.transcript_id,
        "title": getattr(transcript, "title", None),
        "guest": getattr(transcript, "guest", None),
        "score": round(item.score, 4),
        "excerpt": " ".join((item.chunk.text or "").split())[:240],
    }


def diversify_chunks(
    retrieved: list[RetrievedChunk],
    top_k: int,
    max_per_transcript: int = 2,
) -> list[RetrievedChunk]:
    """Prefer evidence from multiple episodes; fill remaining slots from overflow."""
    if max_per_transcript <= 0:
        return retrieved[:top_k]

    selected: list[RetrievedChunk] = []
    overflow: list[RetrievedChunk] = []
    per_transcript: dict[int, int] = {}
    for item in retrieved:
        transcript_id = item.chunk.transcript_id
        count = per_transcript.get(transcript_id, 0)
        if count < max_per_transcript:
            selected.append(item)
            per_transcript[transcript_id] = count + 1
        else:
            overflow.append(item)
        if len(selected) >= top_k:
            return selected[:top_k]
    for item in overflow:
        if len(selected) >= top_k:
            break
        selected.append(item)
    return selected[:top_k]
