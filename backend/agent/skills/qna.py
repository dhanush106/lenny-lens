from backend.services.rag import RAGService

class QnASkill:
    def __init__(self):
        self.rag_service = RAGService()
        
    async def execute(self, query: str, history: list[dict] | None = None) -> dict:
        return await self.rag_service.answer_question(query, history)
