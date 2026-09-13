import json

from backend.services.llm import get_llm_provider
from backend.services.retrieval import RetrievalService
from backend.db.session import AsyncSessionLocal
from backend.services.security import sanitize_html
from backend.core.config import settings

class ArtifactSkill:
    def __init__(self):
        self.llm = get_llm_provider()
        self.retrieval_service = RetrievalService()

    async def execute(self, query: str) -> dict:
        async with AsyncSessionLocal() as session:
            # 1. Retrieve transcripts context
            chunks = await self.retrieval_service.search(session, query, top_k=min(3, settings.RETRIEVAL_TOP_K))
            chunks = [item for item in chunks if item.score >= settings.RETRIEVAL_MIN_SCORE]
            
            context_text = ""
            sources = []
            if chunks:
                for idx, item in enumerate(chunks, 1):
                    chunk = item.chunk
                    context_text += f"\n--- Source [{idx}] ---\n{chunk.text}\n"
                    sources.append({
                        "id": chunk.id,
                        "transcript_id": chunk.transcript_id,
                        "title": chunk.transcript.title,
                        "score": round(item.score, 4),
                        "text_preview": chunk.text[:100] + "..."
                    })
            else:
                return {
                    "answer": "I don't have enough transcript evidence to create a grounded artifact on that topic.",
                    "sources": [],
                }

            # 2. Build Artifact Prompt
            system_prompt = (
                "You are an expert developer and writer. "
                "Generate a self-contained artifact based on the user's request and the provided context. "
                "The artifact must be EITHER a standalone HTML document (with embedded CSS) OR a Markdown document. "
                "Output your response STRICTLY as a JSON object with the following keys:\n"
                "- 'artifact_type': 'html' or 'markdown'\n"
                "- 'title': A short descriptive title\n"
                "- 'content': The complete artifact code/text\n"
                "Do NOT include any markdown code block formatting (like ```json) in your response, just the raw JSON object."
            )
            
            prompt = f"Context:\n{context_text}\n\nArtifact Request:\n{query}"
            
            # 3. Generate response
            answer = await self.llm.generate_response(prompt, system_prompt=system_prompt)
            
            return {
                "answer": self._validate_and_sanitize_artifact(answer),
                "sources": sources
            }

    @staticmethod
    def _validate_and_sanitize_artifact(answer: str) -> str:
        """Keep the persisted artifact contract strict and treat HTML as untrusted."""
        try:
            artifact = json.loads(answer)
        except json.JSONDecodeError:
            return "I couldn't create a valid artifact. Please try again."

        if not isinstance(artifact, dict) or artifact.get("artifact_type") not in {"html", "markdown"}:
            return "I couldn't create a supported artifact. Please request HTML or Markdown."

        content = artifact.get("content")
        if not isinstance(content, str):
            return "I couldn't create a valid artifact. Please try again."

        artifact["title"] = str(artifact.get("title") or "Generated Artifact")
        if artifact["artifact_type"] == "html":
            artifact["content"] = sanitize_html(content)
        return json.dumps(artifact)
