from backend.agent.skills.qna import QnASkill
from backend.agent.skills.essay import EssaySkill
from backend.agent.skills.artifact import ArtifactSkill

class AgentRouter:
    def __init__(self):
        self.qna_skill = QnASkill()
        self.essay_skill = EssaySkill()
        self.artifact_skill = ArtifactSkill()

    async def route_request(self, user_message: str, history: list[dict] | None = None) -> dict:
        normalized = user_message.lower()
        if any(term in normalized for term in ("ship 30", "essay", "article")):
            intent = "Essay"
        elif any(term in normalized for term in ("html", "css", "artifact", "canvas", "markdown document")):
            intent = "Artifact"
        elif len(normalized.split()) < 2 or not any(char.isalpha() for char in normalized):
            intent = "Chat"
        else:
            intent = "QnA"

        if intent == "QnA":
            return await self.qna_skill.execute(user_message, history)
        elif intent == "Essay":
            return await self.essay_skill.execute(user_message)
        elif intent == "Artifact":
            return await self.artifact_skill.execute(user_message)
        else:
            # Basic conversational fallback
            return {"answer": "I'm the Lenny Growth Assistant. How can I help you today?", "sources": []}
