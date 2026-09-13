from pydantic import BaseModel
from typing import Optional, List

class TranscriptMetadata(BaseModel):
    video_id: str
    title: Optional[str] = None
    speaker: Optional[str] = None

class TranscriptCreate(TranscriptMetadata):
    content: str

class TranscriptResponse(TranscriptMetadata):
    id: int

    class Config:
        from_attributes = True
