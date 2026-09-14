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
            if end < text_length:
                boundary_start = start + int(self.chunk_size * 0.6)
                sentence_boundary = max(
                    text.rfind(". ", boundary_start, end),
                    text.rfind("? ", boundary_start, end),
                    text.rfind("! ", boundary_start, end),
                    text.rfind("\n", boundary_start, end),
                    text.rfind(" ", boundary_start, end),
                )
                if sentence_boundary > start:
                    end = sentence_boundary + 1
            chunks.append(text[start:end].strip())
            if end >= text_length:
                break
            next_start = max(start + 1, end - self.overlap)
            word_boundary = text.find(" ", next_start, min(text_length, next_start + 40))
            start = word_boundary + 1 if word_boundary >= 0 else next_start
            
        return chunks

    def chunk_transcript(self, transcript_id: int, text: str) -> List[ChunkCreate]:
        text_chunks = self.split_text(text)
        return [
            ChunkCreate(transcript_id=transcript_id, text=chunk_text)
            for chunk_text in text_chunks
        ]
