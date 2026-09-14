import os
import hashlib
import asyncio
import argparse
from pathlib import Path
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from backend.db.session import async_session_maker
from backend.models import Transcript, Chunk
from backend.services.embeddings import get_embedding_provider
from backend.services.chunking import ChunkingService
from backend.services.citations import parse_timestamp_seconds
from backend.core.config import settings


def read_transcript(filepath: str, source_root: str) -> tuple[str, str, str, str, str | None, str | None]:
    """Read ChatPRD-style YAML frontmatter without requiring a YAML runtime."""
    raw_text = Path(filepath).read_text(encoding="utf-8")
    metadata: dict[str, str] = {}
    content = raw_text
    if raw_text.startswith("---"):
        parts = raw_text.split("---", 2)
        if len(parts) == 3:
            for line in parts[1].splitlines():
                if ":" in line:
                    key, value = line.split(":", 1)
                    metadata[key.strip().lower()] = value.strip().strip('"').strip("'")
            content = parts[2].strip()

    relative_path = Path(filepath).relative_to(source_root)
    fallback_id = "-".join(relative_path.with_suffix("").parts)
    source_url = metadata.get("url") or metadata.get("source_url") or metadata.get("youtube_url")
    guest = metadata.get("guest") or metadata.get("guests")
    return (
        metadata.get("video_id", fallback_id),
        metadata.get("title", relative_path.parent.name.replace("-", " ").title()),
        content,
        hashlib.sha256(raw_text.encode("utf-8")).hexdigest(),
        source_url,
        guest,
    )


async def ingest_file(session: AsyncSession, filepath: str):
    filename = os.path.basename(filepath)
    source_root = os.environ.get("TRANSCRIPT_SOURCE_DIR", os.path.dirname(filepath))
    video_id, title, text, file_hash, source_url, guest = read_transcript(filepath, source_root)

    result = await session.execute(select(Transcript).filter_by(video_id=video_id))
    transcript = result.scalar_one_or_none()

    if transcript:
        if transcript.source_hash == file_hash:
            print(f"Skipping {filename}: Already ingested and unchanged.")
            return
        print(f"Updating {filename}: Content changed.")
        await session.execute(Chunk.__table__.delete().where(Chunk.transcript_id == transcript.id))
        transcript.source_hash = file_hash
        transcript.title = title
        transcript.source_url = source_url
        transcript.guest = guest
    else:
        print(f"Ingesting {filename}: New file.")
        transcript = Transcript(
            video_id=video_id,
            title=title,
            source_hash=file_hash,
            source_url=source_url,
            guest=guest,
        )
        session.add(transcript)
        await session.flush()

    # ~700-1000 characters with overlap keeps a claim and its nearby context together
    # without stuffing an entire episode into one vector/lexical document.
    chunker = ChunkingService(chunk_size=900, overlap=150)
    text_chunks = chunker.split_text(text)
    embeddings = None
    if settings.RETRIEVAL_MODE.lower() == "semantic":
        embedding_provider = get_embedding_provider()
        embeddings = await embedding_provider.generate_embeddings(text_chunks)

    for i, c_text in enumerate(text_chunks):
        start_seconds = parse_timestamp_seconds(c_text)
        chunk = Chunk(
            transcript_id=transcript.id,
            start_time=float(start_seconds) if start_seconds is not None else None,
            end_time=float(start_seconds + 30) if start_seconds is not None else None,
            text=c_text,
            embedding=embeddings[i] if embeddings else None,
        )
        session.add(chunk)

    await session.commit()
    print(f"Finished {filename}: {len(text_chunks)} chunks created.")


async def main():
    parser = argparse.ArgumentParser(description="Ingest transcripts")
    parser.add_argument('--dir', type=str, default='data/transcripts', help='Directory containing markdown transcripts')
    args = parser.parse_args()

    if not os.path.exists(args.dir):
        raise SystemExit(
            f"Transcript directory '{args.dir}' does not exist. Add authoritative .md files "
            "before running ingestion; an empty directory does not create a knowledge base."
        )

    async with async_session_maker() as session:
        transcript_files = list(Path(args.dir).rglob("*.md"))
        if not transcript_files:
            raise SystemExit(
                f"No .md transcript files found in '{args.dir}'. Nothing was ingested."
            )
        os.environ["TRANSCRIPT_SOURCE_DIR"] = str(Path(args.dir).resolve())
        for filepath in transcript_files:
            await ingest_file(session, str(filepath))


if __name__ == "__main__":
    asyncio.run(main())
