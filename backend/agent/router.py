from backend.agent.skills.qna import QnASkill
from backend.agent.skills.essay import EssaySkill
from backend.agent.skills.artifact import ArtifactSkill
from backend.agent.intents import classify_intent


class AgentRouter:
    """Explicit skill router.

    Claude Agent SDK / Pi are coding-agent runtimes (filesystem, shell). This
    product is a grounded research assistant, so routing is deterministic and
    each skill is a testable tool with structured inputs/outputs. LLM calls
    happen inside skills after retrieval, not as an unconstrained agent loop.
    """

    def __init__(self):
        self.qna_skill = QnASkill()
        self.essay_skill = EssaySkill()
        self.artifact_skill = ArtifactSkill()

    async def route_request(self, user_message: str, history: list[dict] | None = None) -> dict:
        intent = classify_intent(user_message)
        if intent == "qna":
            return await self.qna_skill.execute(user_message, history)
        if intent == "essay":
            return await self.essay_skill.execute(user_message, history)
        if intent == "artifact":
            return await self.artifact_skill.execute(user_message, history)
        return {
            "answer": "I'm the Lenny Growth Assistant. Ask a product/growth question, request a Ship 30 essay, or generate a markdown/HTML artifact.",
            "sources": [],
        }
