from unittest.mock import AsyncMock

import pytest

from backend.agent.router import AgentRouter


@pytest.mark.asyncio
async def test_router_selects_dedicated_skills_without_calling_an_llm():
    router = AgentRouter()
    router.qna_skill.execute = AsyncMock(return_value={"answer": "qna", "sources": []})
    router.essay_skill.execute = AsyncMock(return_value={"answer": "essay", "sources": []})
    router.artifact_skill.execute = AsyncMock(return_value={"answer": "artifact", "sources": []})

    assert (await router.route_request("What are good discovery practices?"))["answer"] == "qna"
    assert (await router.route_request("Write a Ship 30 essay about prioritization."))["answer"] == "essay"
    assert (await router.route_request("Create an HTML product strategy canvas."))["answer"] == "artifact"
    assert (await router.route_request("dagfjlds"))["sources"] == []

    router.qna_skill.execute.assert_awaited_once()
    router.essay_skill.execute.assert_awaited_once()
    router.artifact_skill.execute.assert_awaited_once()
