import logging
import re
from html import unescape
from typing import Any

from backend.core.logging import log_event
from backend.services.retrieval import RetrievedChunk
from backend.core.config import settings

logger = logging.getLogger(__name__)

_TOKEN_RE = re.compile(r"[a-z][a-z0-9'-]{2,}")
_STOPWORDS = {
    "about", "after", "also", "because", "being", "from", "have", "into", "more",
    "only", "over", "that", "their", "there", "these", "they", "this", "those",
    "through", "with", "without", "your", "than", "then", "very", "what", "when",
    "where", "which", "while", "will", "would", "should", "could", "instead",
}
_CITATION_RE = re.compile(r"\[(\d+)\]")
_SYNONYMS = {
    "find": "look", "looking": "look", "patterns": "pattern", "patternized": "pattern",
    "reinvent": "re-engineer", "reinventing": "re-engineer", "reinvention": "re-engineer",
    "problems": "problem", "solutions": "solution", "teams": "team",
}


def _tokens(text: str) -> set[str]:
    return {
        _SYNONYMS.get(token, token.rstrip("s"))
        for token in _TOKEN_RE.findall(text.lower())
        if token not in _STOPWORDS
    }


def normalize_evidence(evidence: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Adapt retrieval/source payload variants to the grounding contract."""
    normalized = []
    for index, item in enumerate(evidence, 1):
        text = item.get("evidence") or item.get("content") or item.get("text") or item.get("excerpt")
        if not isinstance(text, str) or not text.strip():
            continue
        source = item.get("source", item.get("source_id", item.get("n", index)))
        try:
            source = int(source)
        except (TypeError, ValueError):
            source = index
        normalized.append({
            **item,
            "evidence": text.strip(),
            "source": source,
            "confidence": float(item.get("confidence", item.get("score", 0.0)) or 0.0),
        })
    return normalized


def extract_evidence(chunks: list[RetrievedChunk]) -> list[dict[str, Any]]:
    """Create small, source-linked evidence units from retrieved transcript chunks."""
    evidence: list[dict[str, Any]] = []
    for source_number, item in enumerate(chunks, 1):
        sentences = re.split(r"(?<=[.!?])\s+|\n+", item.chunk.text or "")
        for sentence in sentences:
            statement = " ".join(sentence.split()).strip()
            if len(_tokens(statement)) < 3:
                continue
            evidence.append({
                "claim": statement,
                "evidence": statement,
                "source": source_number,
                "source_title": getattr(item.chunk.transcript, "title", None) if item.chunk.transcript else None,
                "source_guest": getattr(item.chunk.transcript, "guest", None) if item.chunk.transcript else None,
                "confidence": round(min(0.99, max(0.5, item.score)), 2),
            })
    log_event(logger, "artifact_evidence_extracted", evidence_count=len(evidence), evidence=evidence)
    return evidence


def validate_claim(
    claim: str,
    evidence: list[dict[str, Any]],
    *,
    require_citation: bool = True,
) -> dict[str, Any]:
    """Reject claims that introduce unsupported topics or outrun the evidence."""
    evidence = normalize_evidence(evidence)
    claim_text = re.sub(r"\[\d+\]", "", claim or "").strip()
    claim_tokens = _tokens(claim_text)
    cited = {int(number) for number in _CITATION_RE.findall(claim or "")}
    candidates = [item for item in evidence if not cited or item["source"] in cited]
    best = None
    best_score = 0.0
    for item in candidates:
        evidence_tokens = _tokens(item["evidence"])
        if not evidence_tokens:
            continue
        overlap = claim_tokens & evidence_tokens
        score = len(overlap) / max(1, len(claim_tokens))
        coverage = len(overlap) / max(1, len(evidence_tokens))
        combined = (score * 0.7) + (coverage * 0.3)
        if combined > best_score:
            best_score = combined
            best = item

    # Synthesis can combine several retrieved excerpts. Score their combined
    # vocabulary while keeping the supporting source IDs for attribution.
    synthesis_items = [item for item in evidence if not cited or item["source"] in cited]
    if len(synthesis_items) > 1:
        cited_items = synthesis_items
        combined_text = " ".join(item["evidence"] for item in cited_items)
        combined_tokens = _tokens(combined_text)
        overlap = claim_tokens & combined_tokens
        synthesis_score = len(overlap) / max(1, len(claim_tokens))
        if synthesis_score > best_score:
            best_score = synthesis_score
            best = cited_items[0] if cited_items else best

    accepted = bool(
        best
        and best_score >= settings.GROUNDING_MIN_CONFIDENCE
        and (not require_citation or (cited and best["source"] in cited))
    )
    result = {
        "claim": claim,
        "accepted": accepted,
        "source": best["source"] if best else None,
        "supporting_sources": [item["source"] for item in synthesis_items if item["source"] in cited] if cited else ([best["source"]] if best else []),
        "confidence": round(best_score, 3),
        "reason": "supported by evidence" if accepted else "claim lacks citation or introduces unsupported or overly specific facts",
        "evidence": best.get("evidence") if best else None,
    }
    log_event(logger, "artifact_claim_validated", **result)
    return result


def validate_artifact_content(content: str, evidence: list[dict[str, Any]]) -> tuple[str, list[dict[str, Any]], list[dict[str, Any]]]:
    """Keep headings and formatting, but remove unsupported prose blocks."""
    evidence = normalize_evidence(evidence)
    is_html = bool(re.search(r"<html|<body|<section|<article|<div", content, re.I))
    validation_content = content
    if is_html:
        validation_content = re.sub(r"<style\b[^>]*>.*?</style>|<script\b[^>]*>.*?</script>", "", content, flags=re.I | re.S)
        validation_content = re.sub(r"<[^>]+>", "\n", validation_content)
        validation_content = unescape(validation_content)
    accepted: list[dict[str, Any]] = []
    rejected: list[dict[str, Any]] = []
    kept_blocks: list[str] = []
    for block in re.split(r"\n\s*\n", validation_content.strip()):
        stripped = block.strip()
        if not stripped or stripped.startswith("#") or stripped.startswith("## Sources"):
            kept_blocks.append(block)
            continue
        original_lines = [line for line in stripped.splitlines() if line.strip()]
        if is_html:
            original_lines = [line for line in original_lines if len(_tokens(line)) >= 4]
            if not original_lines:
                continue
        claims = [line.strip().lstrip("- ") for line in original_lines]
        if not claims:
            kept_blocks.append(block)
            continue
        results = [validate_claim(claim, evidence) for claim in claims]
        inferred_lines = list(original_lines)
        for index, (claim, result) in enumerate(zip(claims, results)):
            if not result["accepted"] and not _CITATION_RE.search(claim):
                inferred = validate_claim(claim, evidence, require_citation=False)
                if inferred["accepted"]:
                    inferred_lines[index] = f"{original_lines[index]} [{inferred['source']}]"
                    results[index] = {**inferred, "claim": inferred_lines[index], "inferred_citation": True}
        if all(result["accepted"] for result in results):
            kept_blocks.append("\n".join(inferred_lines))
            accepted.extend(results)
        else:
            rejected.extend(result for result in results if not result["accepted"])
            accepted.extend(result for result in results if result["accepted"])
    if is_html and rejected:
        # Do not return partially validated HTML. The caller will build a
        # safe, evidence-only HTML artifact from accepted transcript evidence.
        validated_content = ""
    else:
        validated_content = content if is_html else "\n\n".join(kept_blocks)
    log_event(logger, "artifact_claims_finalized", accepted_claims=accepted, rejected_claims=rejected)
    return validated_content, accepted, rejected
