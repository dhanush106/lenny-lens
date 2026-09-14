import json
import logging
import re
from html import escape

from backend.agent.intents import expand_retrieval_query, requested_artifact_format
from backend.services.llm import get_llm_provider
from backend.services.retrieval import RetrievalService
from backend.services.citations import (
    citation_footer,
    conversation_history,
    filter_used_sources,
    numbered_sources,
)
from backend.db.session import AsyncSessionLocal
from backend.services.security import sanitize_html
from backend.services.grounding import extract_evidence, validate_artifact_content
from backend.core.config import settings
from backend.core.logging import log_event

logger = logging.getLogger(__name__)

ARTIFACT_SYSTEM_PROMPT = """
You generate a self-contained product artifact from numbered transcript evidence.

Output STRICTLY a JSON object with keys:
- artifact_type: "html" or "markdown"
- title: short descriptive title
- summary: one sentence describing the artifact
- content: the complete artifact body

Choose a template from the request:
- strategy canvas / HTML / CSS / canvas → HTML one-pager with CSS in a <style> tag
- comparison / vs / table → HTML comparison table
- timeline → HTML vertical timeline
- brief / one-pager / document / markdown → Markdown briefing

Rules:
- Do not invent facts. Use only the transcript evidence. Cite claims as [1], [2].
- HTML must be a complete static document: include <!doctype html>, <html>, <head>, a <meta charset>, a <style> tag, and <body>.
- HTML must contain no scripts, event handlers, external network requests, iframes, forms, or network images.
- CSS must live in a <style> tag. Prefer a clean product-doc look (system fonts, generous spacing).
- Close the artifact with a Sources section listing the numbered citations you used.
- Do not wrap the JSON in markdown fences.
""".strip()


def choose_template(query: str) -> str:
    lowered = query.lower()
    if any(term in lowered for term in ("compar", " vs", "versus", "table")):
        return "comparison table (HTML)"
    if "timeline" in lowered:
        return "timeline (HTML)"
    if any(term in lowered for term in ("canvas", "html", "css")):
        return "strategy canvas (HTML)"
    return "one-pager brief (Markdown)"


class ArtifactSkill:
    def __init__(self):
        self.llm = get_llm_provider()
        self.retrieval_service = RetrievalService()

    async def execute(self, query: str, history: list[dict] | None = None) -> dict:
        artifact_format = requested_artifact_format(query)
        log_event(logger, "artifact_pipeline_started", query=query)
        if re.search(r"\b(pdf|docx|doc|csv|json)\b", query.lower()) and not artifact_format:
            return self._error(
                "unsupported_format",
                "I can generate grounded Markdown or HTML artifacts, but not that format.",
            )

        retrieval_query = expand_retrieval_query(query, history)
        async with AsyncSessionLocal() as session:
            chunks = await self.retrieval_service.search(
                session, retrieval_query, top_k=min(5, settings.RETRIEVAL_TOP_K)
            )
            chunks = [item for item in chunks if item.score >= settings.RETRIEVAL_MIN_SCORE]
            log_event(logger, "artifact_retrieval_result", query=query, chunks=[
                {"document_id": item.chunk.transcript_id, "chunk_id": item.chunk.id,
                 "title": getattr(item.chunk.transcript, "title", None), "score": item.score,
                 "text": item.chunk.text} for item in chunks
            ])

            if not chunks:
                return self._error(
                    "insufficient_evidence",
                    "I couldn't find enough relevant Lenny transcript evidence to create this artifact.",
                )

            sources = numbered_sources(chunks)
            template = choose_template(query)
            log_event(logger, "artifact_chunks_retrieved", chunks=sources)
            try:
                evidence = extract_evidence(chunks)
                log_event(logger, "artifact_validation_input", evidence=evidence)
            except Exception as exc:
                logger.exception("artifact_evidence_extraction_failed")
                return self._error(
                    "evidence_extraction_failed",
                    "I could not safely extract grounded evidence from the retrieved transcripts.",
                    sources=sources,
                )
            prompt = (
                f"Conversation context:\n{conversation_history(history) or '(none)'}\n\n"
                f"Validated structured evidence (use only these statements; do not add facts):\n"
                f"{json.dumps(evidence, ensure_ascii=True)}\n\n"
                f"Preferred template: {template}\n"
                f"Artifact request:\n{query}"
            )
            raw = await self.llm.generate_response(
                prompt, system_prompt=ARTIFACT_SYSTEM_PROMPT, max_tokens=4096
            )
            artifact = self._validate_and_sanitize_artifact(raw, sources, requested_format=artifact_format)
            log_event(logger, "artifact_generated_claims", raw=raw)
            if not artifact:
                return self._error(
                    "generation_failed",
                    "The artifact generator returned an invalid or incomplete document. No artifact was created.",
                    sources=sources,
                )

            try:
                grounded_content, accepted_claims, rejected_claims = validate_artifact_content(
                    artifact["content"], evidence
                )
                log_event(logger, "artifact_validation_output", accepted_claims=accepted_claims, rejected_claims=rejected_claims)
            except Exception:
                logger.exception("artifact_claim_validation_failed")
                return self._error(
                    "claim_validation_failed",
                    "I could not validate the generated claims against the transcript evidence.",
                    sources=sources,
                )
            if rejected_claims:
                artifact["content"] = grounded_content
            if not accepted_claims or not artifact["content"].strip():
                fallback = self._build_evidence_artifact(
                    query, artifact["format"], artifact.get("title"), evidence, sources
                )
                if fallback:
                    artifact["content"] = fallback
                    grounded_content = fallback
                    accepted_claims = [
                        {"claim": item["evidence"], "source": item["source"], "confidence": item["confidence"], "accepted": True, "reason": "direct transcript evidence"}
                        for item in evidence[:5]
                    ]
                    rejected_claims = rejected_claims or []
                else:
                    return self._error(
                        "insufficient_validated_evidence",
                        "The retrieved transcript evidence was not sufficient to support the generated claims.",
                        sources=sources,
                    )
            artifact["content"] = grounded_content
            log_event(logger, "artifact_final", content=grounded_content, accepted_claims=accepted_claims)
            used = filter_used_sources(artifact["content"], sources)
            artifact["content"] = self._append_sources(artifact["format"], artifact["content"], used)
            summary = artifact.get("summary") or f"Created {artifact['title']}"
            return {
                "answer": summary,
                "sources": used,
                "artifact": artifact,
                "grounding": {
                    "retrieved_sources": sources,
                    "validated_evidence": evidence,
                    "rejected_claims": rejected_claims,
                    "final_claims": accepted_claims,
                },
            }

    @staticmethod
    def _error(code: str, message: str, sources: list[dict] | None = None) -> dict:
        return {"answer": message, "sources": sources or [], "error": {"code": code, "message": message}}

    @staticmethod
    def _build_evidence_artifact(
        query: str,
        artifact_format: str,
        title: str | None,
        evidence: list[dict],
        sources: list[dict],
    ) -> str:
        """Create a useful artifact from transcript evidence when model prose fails validation."""
        usable = [item for item in evidence if item.get("evidence") and item.get("source")]
        if not usable:
            return ""
        artifact_title = title or "Grounded Transcript Brief"
        selected = usable[:5]
        if artifact_format == "html":
            items = "".join(
                f'<article><h2>Evidence {item["source"]}</h2><p>{escape(item["evidence"])} <sup>[{item["source"]}]</sup></p></article>'
                for item in selected
            )
            return (
                "<!doctype html><html><head><meta charset=\"utf-8\"><meta name=\"viewport\" content=\"width=device-width,initial-scale=1\"><style>"
                "body{font-family:system-ui,sans-serif;max-width:760px;margin:0 auto;padding:32px;color:#172033;background:#f7f8fb}"
                "h1{font-size:30px;margin-bottom:24px}article{background:white;border:1px solid #dfe4ec;border-radius:12px;padding:18px;margin:14px 0;box-shadow:0 4px 14px #17203312}h2{font-size:14px;color:#52617a;text-transform:uppercase;letter-spacing:.06em}p{line-height:1.6}sup{color:#2563eb}"
                f"</style></head><body><h1>{escape(artifact_title)}</h1>{items}<h2>Key Takeaway</h2><p>The available transcript evidence supports the points above; it does not support additional principles beyond these excerpts.</p></body></html>"
            )
        lines = [f"# {artifact_title}", "", "The available transcript evidence supports the following points:"]
        for index, item in enumerate(selected, 1):
            lines.extend(["", f"## Principle {index}", "", f"{item['evidence']} [{item['source']}]"])
        lines.extend(["", "## Key Takeaway", "", "The available transcript evidence supports the points above; it does not support additional principles beyond these excerpts."])
        return "\n".join(lines)

    @staticmethod
    def _extract_json(answer: str) -> dict | None:
        text = answer.strip()
        if text.startswith("```"):
            text = re.sub(r"^```(?:json)?\s*", "", text)
            text = re.sub(r"\s*```$", "", text)
        try:
            parsed = json.loads(text)
            return parsed if isinstance(parsed, dict) else None
        except json.JSONDecodeError:
            match = re.search(r"\{.*\}", text, re.S)
            if not match:
                return None
            try:
                parsed = json.loads(match.group(0))
                return parsed if isinstance(parsed, dict) else None
            except json.JSONDecodeError:
                return None

    @classmethod
    def _validate_and_sanitize_artifact(
        cls, answer: str, sources: list[dict], requested_format: str | None = None
    ) -> dict | None:
        payload = cls._extract_json(answer)
        if not payload:
            inferred_format = requested_format
            if inferred_format and answer.strip():
                payload = {"artifact_type": inferred_format, "content": answer.strip()}
            else:
                log_event(logger, "artifact_failed", reason="invalid_payload")
                return None

        artifact_type = payload.get("artifact_type") or payload.get("format") or payload.get("type")
        if artifact_type == "artifact":
            artifact_type = payload.get("format")
        if artifact_type not in {"html", "markdown"} or (
            requested_format and artifact_type != requested_format
        ):
            log_event(logger, "artifact_failed", reason="unsupported_or_mismatched_format")
            return None

        content = payload.get("content")
        if not isinstance(content, str) or not content.strip():
            log_event(logger, "artifact_failed", reason="missing_content")
            return None

        title = str(payload.get("title") or "Generated Artifact")
        summary = str(payload.get("summary") or f"Created {title} from {len(sources)} transcript sources.")
        if artifact_type == "html":
            content = sanitize_html(content)
            content = cls._complete_html_document(content)
            log_event(logger, "artifact_sanitized", title=title)
        else:
            log_event(logger, "artifact_generated", artifact_type="markdown", title=title)
        return {
            "type": "artifact",
            "format": artifact_type,
            "title": title,
            "content": content,
            "summary": summary,
        }

    @staticmethod
    def _complete_html_document(content: str) -> str:
        lowered = content.lstrip().lower()
        if lowered.startswith("<!doctype html>") or lowered.startswith("<html"):
            return content
        return (
            '<!doctype html><html><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width, initial-scale=1">'
            '<meta http-equiv="Content-Security-Policy" content="default-src &#x27;none&#x27;; style-src &#x27;unsafe-inline&#x27;;">'
            "</head><body>"
            f"{content}"
            "</body></html>"
        )

    @staticmethod
    def _append_sources(artifact_format: str, content: str, sources: list[dict]) -> str:
        footer = citation_footer(sources)
        if not footer:
            return content
        if "Sources" in content and "[1]" in content[-800:]:
            return content
        if artifact_format == "html":
            items = "".join(f"<li>{escape(line)}</li>" for line in footer.splitlines())
            marker = f'<div class="sources"><h3>Sources</h3><ol>{items}</ol></div>'
            return content.replace("</body>", f"{marker}</body>")
        return f"{content.rstrip()}\n\n## Sources\n\n{footer}\n"
