from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from backend.db.session import get_db
from backend.schemas.session import SessionResponse, SessionCreate, MessageResponse, MessageCreate
from backend.services import session as session_service

router = APIRouter()

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
