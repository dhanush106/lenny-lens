import json
from backend.services.llm import get_llm_provider
from backend.agent.skills.qna import QnASkill
from backend.agent.skills.essay import EssaySkill

class AgentRouter:
    def __init__(self):
        self.llm = get_llm_provider()
        self.qna_skill = QnASkill()
        self.essay_skill = EssaySkill()

    async def route_request(self, user_message: str) -> dict:
        # Simple intent classification
        system_prompt = (
            "You are a router. Classify the user's intent into one of the following categories:\n"
            "1. 'QnA': The user is asking a product or growth question that should be answered from Lenny's podcast transcripts.\n"
            "2. 'Essay': The user is asking to write a Ship 30 for 30 style essay or article.\n"
            "3. 'Artifact': The user is asking for a Markdown document or HTML/CSS code snippet to be generated.\n"
            "4. 'Chat': General conversational chit-chat.\n"
            "Respond ONLY with a valid JSON object in the following format: {\"intent\": \"QnA\"}"
        )
        
        try:
            # We use the LLM to classify the intent
            response_text = await self.llm.generate_response(user_message, system_prompt=system_prompt)
            # Try to parse the intent
            # Clean up potential markdown formatting from LLM response
            clean_text = response_text.replace("```json", "").replace("```", "").strip()
            intent_data = json.loads(clean_text)
            intent = intent_data.get("intent", "Chat")
        except Exception as e:
            # Fallback to QnA if parsing fails
            intent = "QnA"

        if intent == "QnA":
            return await self.qna_skill.execute(user_message)
        elif intent == "Essay":
            return await self.essay_skill.execute(user_message)
        elif intent == "Artifact":
            return {"answer": "Artifact generation skill is not yet implemented.", "sources": []}
        else:
            # Basic conversational fallback
            return {"answer": "I'm the Lenny Growth Assistant. How can I help you today?", "sources": []}
