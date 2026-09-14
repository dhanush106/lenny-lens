import logging
import time
import uuid
import asyncio

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from pydantic import BaseModel, Field

from backend.db.session import get_db
from backend.schemas.session import SessionResponse, SessionCreate, MessageResponse, MessageCreate
from backend.services import session as session_service
from backend.agent.router import AgentRouter
from backend.agent.intents import classify_intent
from backend.core.logging import log_event
from backend.core.exceptions import ServiceUnavailableError

logger = logging.getLogger(__name__)


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=8000)


class ChatResponse(BaseModel):
    message: MessageResponse
    sources: list = []
    intent: str | None = None
    artifact: dict | None = None
    error: dict | None = None
    grounding: dict | None = None


router = APIRouter()


def get_current_user_id() -> int:
    return 1


@router.post("/", response_model=SessionResponse, status_code=status.HTTP_201_CREATED)
async def create_new_session(
    session_in: SessionCreate,
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    if session_in.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to create session for another user")
    return await session_service.create_session(db=db, session_in=session_in)


@router.get("/", response_model=List[SessionResponse])
async def list_sessions(
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    return await session_service.get_user_sessions(db=db, user_id=user_id)


@router.get("/{session_id}/messages", response_model=List[MessageResponse])
async def get_messages(
    session_id: int,
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    db_session = await session_service.get_session(db=db, session_id=session_id, user_id=user_id)
    if not db_session:
        raise HTTPException(status_code=404, detail="Session not found")
    return await session_service.get_session_messages(db=db, session_id=session_id)


@router.post("/{session_id}/messages", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
async def post_message(
    session_id: int,
    message_in: MessageCreate,
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    db_session = await session_service.get_session(db=db, session_id=session_id, user_id=user_id)
    if not db_session:
        raise HTTPException(status_code=404, detail="Session not found")
    return await session_service.add_message(db=db, session_id=session_id, message_in=message_in)


@router.post("/{session_id}/chat", response_model=ChatResponse)
async def chat_with_agent(
    session_id: int,
    request: ChatRequest,
    http_request: Request,
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    started_at = time.perf_counter()
    request_id = http_request.headers.get("x-request-id") or str(uuid.uuid4())
    db_session = await session_service.get_session(db=db, session_id=session_id, user_id=user_id)
    if not db_session:
        raise HTTPException(status_code=404, detail="Session not found")

    user_msg_in = MessageCreate(role="user", content=request.message)
    await session_service.add_message(db=db, session_id=session_id, message_in=user_msg_in)

    history = [
        {"role": message.role, "content": message.content}
        for message in await session_service.get_session_messages(db=db, session_id=session_id)
    ]

    log_event(logger, "request_started", request_id=request_id, session_id=session_id, message_chars=len(request.message))
    agent = AgentRouter()
    intent = classify_intent(request.message)
    try:
        response_data = await asyncio.wait_for(
            agent.route_request(request.message, history),
            timeout=240,
        )
    except asyncio.TimeoutError as exc:
        logger.exception("agent_request_timeout", extra={"request_id": request_id, "session_id": session_id})
        response_data = {
            "answer": "The grounded response took too long to complete. Please try a shorter request or check the configured LLM.",
            "sources": [],
            "error": {
                "code": "agent_request_timeout",
                "message": "The grounded response exceeded the 240 second local request limit.",
            },
        }
    except ServiceUnavailableError as exc:
        logger.warning("agent_dependency_unavailable", extra={"request_id": request_id, "code": exc.code})
        response_data = {
            "answer": exc.message,
            "sources": [],
            "error": {"code": exc.code, "message": exc.message},
        }
    except Exception as exc:
        logger.exception("agent_request_failed", extra={"request_id": request_id, "session_id": session_id})
        response_data = {
            "answer": "I couldn't complete that request because the grounded response pipeline failed. Please try again.",
            "sources": [],
            "error": {
                "code": "agent_request_failed",
                "message": f"The grounded response pipeline failed before it could produce a response ({type(exc).__name__}).",
            },
        }

    assistant_msg_in = MessageCreate(role="assistant", content=response_data.get("answer", ""))
    assistant_msg = await session_service.add_message(
        db=db,
        session_id=session_id,
        message_in=assistant_msg_in,
        sources=response_data.get("sources") or None,
        artifact=response_data.get("artifact"),
    )

    log_event(
        logger,
        "chat_completed",
        request_id=request_id,
        session_id=session_id,
        intent=intent,
        source_count=len(response_data.get("sources", [])),
        duration_ms=round((time.perf_counter() - started_at) * 1000, 2),
    )
    return ChatResponse(
        message=MessageResponse.model_validate(assistant_msg),
        sources=response_data.get("sources", []),
        intent=intent,
        artifact=response_data.get("artifact"),
        error=response_data.get("error"),
        grounding=response_data.get("grounding"),
    )
