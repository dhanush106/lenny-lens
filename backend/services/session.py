from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import desc
from typing import List

from backend.models.session import Session
from backend.models.message import Message
from backend.schemas.session import SessionCreate, MessageCreate

async def create_session(db: AsyncSession, session_in: SessionCreate) -> Session:
    db_session = Session(
        user_id=session_in.user_id,
        title=session_in.title
    )
    db.add(db_session)
    await db.commit()
    await db.refresh(db_session)
    return db_session

async def get_user_sessions(db: AsyncSession, user_id: int) -> List[Session]:
    result = await db.execute(
        select(Session).where(Session.user_id == user_id).order_by(desc(Session.created_at))
    )
    return result.scalars().all()

async def get_session(db: AsyncSession, session_id: int, user_id: int) -> Session:
    result = await db.execute(
        select(Session).where(Session.id == session_id, Session.user_id == user_id)
    )
    return result.scalars().first()

async def add_message(db: AsyncSession, session_id: int, message_in: MessageCreate) -> Message:
    db_message = Message(
        session_id=session_id,
        role=message_in.role,
        content=message_in.content
    )
    db.add(db_message)
    await db.commit()
    await db.refresh(db_message)
    return db_message

async def get_session_messages(db: AsyncSession, session_id: int) -> List[Message]:
    result = await db.execute(
        select(Message).where(Message.session_id == session_id).order_by(Message.created_at)
    )
    return result.scalars().all()
