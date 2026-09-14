from pydantic import BaseModel, ConfigDict, Field
from typing import Any, List, Optional
from datetime import datetime

class MessageBase(BaseModel):
    role: str
    content: str

class MessageCreate(MessageBase):
    pass

class MessageResponse(MessageBase):
    id: int
    session_id: int
    created_at: datetime
    sources: Optional[List[dict[str, Any]]] = None
    artifact: Optional[dict[str, Any]] = None
    error: Optional[dict[str, Any]] = None
    grounding: Optional[dict[str, Any]] = None

    model_config = ConfigDict(from_attributes=True)

class SessionBase(BaseModel):
    title: Optional[str] = None

class SessionCreate(SessionBase):
    user_id: int

class SessionResponse(SessionBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

class SessionWithMessages(SessionResponse):
    messages: List[MessageResponse] = []
