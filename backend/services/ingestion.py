import os
import re
from typing import List
from backend.schemas.transcript import TranscriptCreate

class IngestionService:
    @staticmethod
    def clean_text(text: str) -> str:
        # Normalize whitespace
        text = re.sub(r'\s+', ' ', text)
        return text.strip()

    @staticmethod
    def load_markdown_transcripts(directory_path: str) -> List[TranscriptCreate]:
        transcripts = []
        if not os.path.exists(directory_path):
            return transcripts
            
        for filename in os.listdir(directory_path):
            if filename.endswith(".md"):
                file_path = os.path.join(directory_path, filename)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                # Basic extraction: video_id from filename, clean content
                video_id = filename.replace('.md', '')
                clean_content = IngestionService.clean_text(content)
                
                transcript = TranscriptCreate(
                    video_id=video_id,
                    title=video_id.replace('-', ' ').title(),
                    content=clean_content
                )
                transcripts.append(transcript)
                
        return transcripts
