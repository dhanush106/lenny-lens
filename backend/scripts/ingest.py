import os
import hashlib
import asyncio
import argparse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

# Adjust path to import backend modules
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from backend.db.session import async_session_maker
from backend.models import Transcript, Chunk

def get_file_hash(filepath: str) -> str:
    hasher = hashlib.sha256()
    with open(filepath, 'rb') as f:
        buf = f.read()
        hasher.update(buf)
    return hasher.hexdigest()

def basic_chunker(text: str, chunk_size: int = 1000) -> list[str]:
    # Very basic chunking by character length
    chunks = []
    for i in range(0, len(text), chunk_size):
        chunks.append(text[i:i+chunk_size])
    return chunks

async def ingest_file(session: AsyncSession, filepath: str):
    filename = os.path.basename(filepath)
    video_id = os.path.splitext(filename)[0]
    file_hash = get_file_hash(filepath)
    
    # Check if exists
    result = await session.execute(select(Transcript).filter_by(video_id=video_id))
    transcript = result.scalar_one_or_none()
    
    if transcript:
        if transcript.source_hash == file_hash:
            print(f"Skipping {filename}: Already ingested and unchanged.")
            return
        else:
            print(f"Updating {filename}: Content changed.")
            # Delete old chunks
            await session.execute(Chunk.__table__.delete().where(Chunk.transcript_id == transcript.id))
            transcript.source_hash = file_hash
    else:
        print(f"Ingesting {filename}: New file.")
        with open(filepath, 'r', encoding='utf-8') as f:
            title = f.readline().strip() # Use first line as title
            if not title:
                title = filename
        
        transcript = Transcript(video_id=video_id, title=title, source_hash=file_hash)
        session.add(transcript)
        await session.flush() # get ID
        
    # Read text
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()
        
    text_chunks = basic_chunker(text)
    
    for i, c_text in enumerate(text_chunks):
        # Generate dummy embedding (or real if ollama is running, but let's just insert a dummy for speed in this demo)
        dummy_embedding = [0.0] * 384
        chunk = Chunk(transcript_id=transcript.id, text=c_text, embedding=dummy_embedding)
        session.add(chunk)
        
    await session.commit()
    print(f"Finished {filename}: {len(text_chunks)} chunks created.")

async def main():
    parser = argparse.ArgumentParser(description="Ingest transcripts")
    parser.add_argument('--dir', type=str, default='data/transcripts', help='Directory containing markdown transcripts')
    args = parser.parse_args()
    
    if not os.path.exists(args.dir):
        print(f"Directory {args.dir} does not exist.")
        # Create it so it doesn't fail
        os.makedirs(args.dir, exist_ok=True)
        return
        
    async with async_session_maker() as session:
        for filename in os.listdir(args.dir):
            if filename.endswith('.md'):
                filepath = os.path.join(args.dir, filename)
                await ingest_file(session, filepath)

if __name__ == "__main__":
    asyncio.run(main())
