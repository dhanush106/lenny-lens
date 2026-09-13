import json
import logging
import time

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from backend.db.session import get_db
from backend.schemas.session import SessionResponse, SessionCreate, MessageResponse, MessageCreate
from backend.services import session as session_service
from backend.agent.router import AgentRouter
from pydantic import BaseModel

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    message: MessageResponse
    sources: list = []

router = APIRouter()
logger = logging.getLogger(__name__)

# Dependency for mocking auth
def get_current_user_id() -> int:
    return 1

@router.post("/", response_model=SessionResponse, status_code=status.HTTP_201_CREATED)
async def create_new_session(
    session_in: SessionCreate,
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    # Enforce current user
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
    # Validate session belongs to user
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
    # Validate session belongs to user
    db_session = await session_service.get_session(db=db, session_id=session_id, user_id=user_id)
    if not db_session:
        raise HTTPException(status_code=404, detail="Session not found")
    return await session_service.add_message(db=db, session_id=session_id, message_in=message_in)

@router.post("/{session_id}/chat", response_model=ChatResponse)
async def chat_with_agent(
    session_id: int,
    request: ChatRequest,
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    started_at = time.perf_counter()
    # Validate session belongs to user
    db_session = await session_service.get_session(db=db, session_id=session_id, user_id=user_id)
    if not db_session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # 1. Persist user message
    user_msg_in = MessageCreate(session_id=session_id, role="user", content=request.message)
    await session_service.add_message(db=db, session_id=session_id, message_in=user_msg_in)
    
    history = [
        {"role": message.role, "content": message.content}
        for message in await session_service.get_session_messages(db=db, session_id=session_id)
    ]

    # 2. Invoke Agent Router
    agent = AgentRouter()
    response_data = await agent.route_request(request.message, history)
    
    # 3. Persist assistant message
    assistant_msg_in = MessageCreate(
        session_id=session_id, 
        role="assistant", 
        content=response_data.get("answer", "")
    )
    assistant_msg = await session_service.add_message(db=db, session_id=session_id, message_in=assistant_msg_in)
    
    logger.info(json.dumps({
        "event": "chat_completed",
        "session_id": session_id,
        "source_count": len(response_data.get("sources", [])),
        "duration_ms": round((time.perf_counter() - started_at) * 1000, 2),
    }))
    return ChatResponse(
        message=MessageResponse.model_validate(assistant_msg),
        sources=response_data.get("sources", [])
    )
