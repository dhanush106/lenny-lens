from typing import List
from backend.schemas.chunk import ChunkCreate

class ChunkingService:
    def __init__(self, chunk_size: int = 1000, overlap: int = 100):
        self.chunk_size = chunk_size
        self.overlap = overlap

    def split_text(self, text: str) -> List[str]:
        if not text:
            return []
            
        chunks = []
        start = 0
        text_length = len(text)
        
        while start < text_length:
            end = start + self.chunk_size
            chunks.append(text[start:end])
            if end >= text_length:
                break
            start += (self.chunk_size - self.overlap)
            
        return chunks

    def chunk_transcript(self, transcript_id: int, text: str) -> List[ChunkCreate]:
        text_chunks = self.split_text(text)
        return [
            ChunkCreate(transcript_id=transcript_id, text=chunk_text)
            for chunk_text in text_chunks
        ]
