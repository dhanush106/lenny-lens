from unittest.mock import AsyncMock, patch

import pytest

from backend.agent.router import AgentRouter
from backend.agent.skills.essay import EssaySkill
from backend.models.chunk import Chunk
from backend.models.transcript import Transcript
from backend.services.retrieval import RetrievedChunk
from backend.agent.skills.artifact import ArtifactSkill


class _FakeSession:
    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        return False


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


@pytest.mark.asyncio
async def test_essay_skill_returns_markdown_artifact():
    skill = EssaySkill()
    transcript = Transcript(id=7, video_id="abc", title="Retention interview", guest="Casey Winters")
    chunk = Chunk(id=1, transcript_id=7, start_time=0, end_time=0, text="Retention is a product problem.")
    chunk.transcript = transcript
    skill.retrieval_service.search = AsyncMock(return_value=[RetrievedChunk(chunk=chunk, score=0.8)])
    skill.llm.generate_response = AsyncMock(
        return_value="# Retention is a product job\n\nHook. Teams treat churn as a growth leak [1]."
    )

    with patch("backend.agent.skills.essay.AsyncSessionLocal", return_value=_FakeSession()):
        result = await skill.execute("Write a Ship 30 essay about retention.")
    assert result["artifact"]["type"] == "markdown"
    assert "Retention is a product job" in result["artifact"]["title"]
    assert result["sources"][0]["n"] == 1
    assert "Wrote a Ship 30" in result["answer"]


@pytest.mark.asyncio
async def test_artifact_skill_retrieves_before_generating_markdown():
    skill = ArtifactSkill()
    transcript = Transcript(id=8, video_id="growth", title="Growth interview", guest="Lenny guest")
    chunk = Chunk(id=2, transcript_id=8, start_time=0, end_time=0, text="Growth starts with retention.")
    chunk.transcript = transcript
    events = []

    async def retrieve(*args, **kwargs):
        events.append("retrieve")
        return [RetrievedChunk(chunk=chunk, score=0.9)]

    async def generate(*args, **kwargs):
        events.append("generate")
        return '{"artifact_type":"markdown","title":"5 Principles","content":"# 5 Principles\\n\\nRetention matters [1]."}'

    skill.retrieval_service.search = retrieve
    skill.llm.generate_response = generate
    with patch("backend.agent.skills.artifact.AsyncSessionLocal", return_value=_FakeSession()):
        result = await skill.execute("Create a short Markdown artifact titled 5 Principles")
    assert events == ["retrieve", "generate"]
    assert result["artifact"]["format"] == "markdown"
    assert result["artifact"]["content"].startswith("# 5 Principles")
    assert result["sources"][0]["n"] == 1


@pytest.mark.asyncio
async def test_exact_growth_prompt_keeps_only_validated_claims():
    skill = ArtifactSkill()
    transcript = Transcript(id=9, video_id="growth", title="Elena Verna on growth", guest="Elena Verna")
    chunk = Chunk(
        id=3,
        transcript_id=9,
        start_time=0,
        end_time=0,
        text="Look for recurring patterns in activation and monetization rather than trying to re-engineer them.",
    )
    chunk.transcript = transcript
    skill.retrieval_service.search = AsyncMock(return_value=[RetrievedChunk(chunk=chunk, score=0.9)])
    skill.llm.generate_response = AsyncMock(return_value=(
        '{"artifact_type":"markdown","title":"5 Principles for Better Product Growth",'
        '"content":"# 5 Principles for Better Product Growth\\n\\n'
        '## Own Your Growth Channels\\n\\nSEO, SEM and social media are the best sustainable growth channels. [1]\\n\\n'
        '## Find Recurring Patterns\\n\\nLook for recurring patterns in activation and monetization instead of trying to re-engineer every problem from scratch. [1]"}'
    ))
    query = """Based only on the relevant ideas in Lenny's Podcast transcripts, create a short one-page Markdown artifact titled:

'5 Principles for Better Product Growth'

Include 5 concise principles, source attribution, and a final Key Takeaway section."""
    with patch("backend.agent.skills.artifact.AsyncSessionLocal", return_value=_FakeSession()):
        result = await skill.execute(query)
    assert "SEO, SEM" not in result["artifact"]["content"]
    assert len(result["grounding"]["rejected_claims"]) == 1
    assert "Find Recurring Patterns" in result["artifact"]["content"]


@pytest.mark.asyncio
async def test_artifact_empty_retrieval_is_distinct_from_validation_failure():
    skill = ArtifactSkill()
    skill.retrieval_service.search = AsyncMock(return_value=[])
    with patch("backend.agent.skills.artifact.AsyncSessionLocal", return_value=_FakeSession()):
        result = await skill.execute("Create a Markdown artifact about the Roman Empire")
    assert result["error"]["code"] == "insufficient_evidence"
    assert result.get("artifact") is None
