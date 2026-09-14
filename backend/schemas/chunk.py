from pydantic import BaseModel
from typing import Optional

class ChunkCreate(BaseModel):
    transcript_id: int
    text: str
    start_time: Optional[float] = None
    end_time: Optional[float] = None

class ChunkResponse(ChunkCreate):
    id: int

    class Config:
        from_attributes = True
