import re
from typing import Any

from backend.services.retrieval import RetrievedChunk

CITE_RE = re.compile(r"\[(\d+)\]")
# [m:ss], [mm:ss], [h:mm:ss]
BRACKET_TS_RE = re.compile(r"\[(?:(\d{1,2}):)?(\d{1,2}):(\d{2})\]")
# line-start 12:34 or 1:12:34 used in many ChatPRD transcripts
LINE_TS_RE = re.compile(r"(?m)^\s*(?:(\d{1,2}):)?(\d{1,2}):(\d{2})\b")
YOUTUBE_ID_RE = re.compile(r"^[A-Za-z0-9_-]{11}$")


def _seconds_from_match(match: re.Match[str]) -> int | None:
    hours = int(match.group(1) or 0)
    minutes = int(match.group(2))
    seconds = int(match.group(3))
    if minutes > 59 or seconds > 59:
        return None
    return hours * 3600 + minutes * 60 + seconds


def parse_timestamp_seconds(text: str | None) -> int | None:
    """Return the first real transcript timestamp in seconds, or None."""
    if not text:
        return None
    match = BRACKET_TS_RE.search(text) or LINE_TS_RE.search(text)
    if not match:
        return None
    return _seconds_from_match(match)


def format_timestamp(seconds: int | None) -> str | None:
    if seconds is None:
        return None
    hours, rem = divmod(int(seconds), 3600)
    minutes, secs = divmod(rem, 60)
    if hours:
        return f"{hours}:{minutes:02d}:{secs:02d}"
    return f"{minutes}:{secs:02d}"


def excerpt_text(text: str | None, limit: int = 420) -> str:
    preview = " ".join((text or "").split())
    if len(preview) <= limit:
        return preview
    return preview[: limit - 1].rsplit(" ", 1)[0] + "…"


def watch_url(video_id: str | None, source_url: str | None, start_seconds: int | None) -> str | None:
    is_youtube_url = bool(source_url and re.match(r"https?://(www\.)?(youtube\.com|youtu\.be)/", source_url))
    base = source_url if is_youtube_url else None
    if not base and video_id and YOUTUBE_ID_RE.match(video_id):
        base = f"https://www.youtube.com/watch?v={video_id}"
    if not base:
        return None
    if start_seconds is None:
        return base
    if re.search(r"[?&]t=", base):
        return base
    separator = "&" if "?" in base else "?"
    return f"{base}{separator}t={int(start_seconds)}s"


def source_payload(item: RetrievedChunk, n: int) -> dict[str, Any]:
    chunk = item.chunk
    transcript = chunk.transcript
    text = chunk.text or ""
    parsed_seconds = parse_timestamp_seconds(text)
    stored_seconds = chunk.start_time if chunk.start_time and chunk.start_time > 0 else None
    start_seconds = parsed_seconds if parsed_seconds is not None else stored_seconds
    title = transcript.title if transcript else None
    video_id = transcript.video_id if transcript else None
    guest = getattr(transcript, "guest", None) if transcript else None
    source_url = getattr(transcript, "source_url", None) if transcript else None
    url = watch_url(video_id, source_url, start_seconds)
    excerpt = excerpt_text(text)
    return {
        "n": n,
        "id": chunk.id,
        "chunk_id": chunk.id,
        "transcript_id": chunk.transcript_id,
        "title": title,
        "guest": guest,
        "video_id": video_id,
        "source_url": url or source_url,
        "start_seconds": start_seconds,
        "timestamp": format_timestamp(start_seconds),
        "score": round(item.score, 4),
        "excerpt": excerpt,
        "text_preview": excerpt if len(excerpt) <= 100 else excerpt[:97] + "...",
    }


def numbered_sources(chunks: list[RetrievedChunk]) -> list[dict[str, Any]]:
    return [source_payload(item, n) for n, item in enumerate(chunks, 1)]


def format_context(chunks: list[RetrievedChunk]) -> str:
    blocks = []
    for n, item in enumerate(chunks, 1):
        chunk = item.chunk
        transcript = chunk.transcript
        title = (transcript.title if transcript else None) or (transcript.video_id if transcript else "Untitled")
        guest = getattr(transcript, "guest", None) or "unknown guest"
        parsed_seconds = parse_timestamp_seconds(chunk.text)
        stored_seconds = chunk.start_time if chunk.start_time and chunk.start_time > 0 else None
        stamp = format_timestamp(parsed_seconds if parsed_seconds is not None else stored_seconds)
        time_bit = f" | {stamp}" if stamp else ""
        blocks.append(
            f"--- Source [{n}] {title} — {guest}{time_bit} ---\n{chunk.text}"
        )
    return "\n\n".join(blocks)


def citation_footer(sources: list[dict[str, Any]]) -> str:
    lines = []
    for source in sources:
        n = source.get("n")
        title = source.get("title") or source.get("video_id") or "Untitled episode"
        guest = source.get("guest")
        stamp = source.get("timestamp")
        parts = [f"[{n}] {title}"]
        if guest:
            parts.append(guest)
        if stamp:
            parts.append(stamp)
        lines.append(" — ".join(parts))
    return "\n".join(lines)


def filter_used_sources(answer: str, sources: list[dict[str, Any]]) -> list[dict[str, Any]]:
    used = {int(n) for n in CITE_RE.findall(answer or "")}
    if not used:
        return sources
    filtered = [source for source in sources if source.get("n") in used]
    return filtered or sources


def conversation_history(history: list[dict] | None, *, drop_current_user: bool = True) -> str:
    turns = list(history or [])
    if drop_current_user and turns and turns[-1].get("role") == "user":
        turns = turns[:-1]
    recent = turns[-6:]
    return "\n".join(f"{item['role']}: {item['content']}" for item in recent)
