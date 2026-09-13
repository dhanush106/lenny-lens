from pydantic import BaseModel
from typing import Optional

class ChunkCreate(BaseModel):
    transcript_id: int
    text: str
    start_time: Optional[float] = 0.0
    end_time: Optional[float] = 0.0

class ChunkResponse(ChunkCreate):
    id: int

    class Config:
        from_attributes = True
