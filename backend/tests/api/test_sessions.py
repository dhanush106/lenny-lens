import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_session_isolation(async_client: AsyncClient):
    first = await async_client.post("/api/v1/sessions/", json={"user_id": 1, "title": "Session A"})
    second = await async_client.post("/api/v1/sessions/", json={"user_id": 1, "title": "Session B"})
    assert first.status_code == 201
    assert second.status_code == 201
    session_a = first.json()["id"]
    session_b = second.json()["id"]
    assert session_a != session_b

    posted_a = await async_client.post(
        f"/api/v1/sessions/{session_a}/messages",
        json={"role": "user", "content": "alpha only"},
    )
    posted_b = await async_client.post(
        f"/api/v1/sessions/{session_b}/messages",
        json={"role": "user", "content": "beta only"},
    )
    assert posted_a.status_code == 201
    assert posted_b.status_code == 201

    messages_a = (await async_client.get(f"/api/v1/sessions/{session_a}/messages")).json()
    messages_b = (await async_client.get(f"/api/v1/sessions/{session_b}/messages")).json()
    contents_a = [item["content"] for item in messages_a]
    contents_b = [item["content"] for item in messages_b]
    assert "alpha only" in contents_a
    assert "beta only" not in contents_a
    assert "beta only" in contents_b
    assert "alpha only" not in contents_b


@pytest.mark.asyncio
async def test_messages_include_optional_artifact_field(async_client: AsyncClient):
    created = await async_client.post("/api/v1/sessions/", json={"user_id": 1, "title": "Artifact field"})
    session_id = created.json()["id"]
    await async_client.post(
        f"/api/v1/sessions/{session_id}/messages",
        json={"role": "assistant", "content": "Created a canvas."},
    )
    messages = (await async_client.get(f"/api/v1/sessions/{session_id}/messages")).json()
    assert messages[0]["artifact"] is None
    assert "sources" in messages[0]
