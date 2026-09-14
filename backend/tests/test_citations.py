from backend.models.chunk import Chunk
from backend.models.transcript import Transcript
from backend.services.citations import (
    filter_used_sources,
    format_context,
    numbered_sources,
    parse_timestamp_seconds,
    source_payload,
    watch_url,
)
from backend.services.retrieval import RetrievedChunk, diversify_chunks


def _chunk(text: str, transcript_id: int = 1, chunk_id: int = 10, **meta) -> RetrievedChunk:
    transcript = Transcript(
        id=transcript_id,
        video_id=meta.get("video_id", "dQw4w9wgXcQ"),
        title=meta.get("title", "Discovery vs execution"),
        guest=meta.get("guest", "Teresa Torres"),
        source_url=meta.get("source_url", "https://www.youtube.com/watch?v=dQw4w9wgXcQ"),
    )
    chunk = Chunk(
        id=chunk_id,
        transcript_id=transcript_id,
        start_time=0,
        end_time=0,
        text=text,
    )
    chunk.transcript = transcript
    return RetrievedChunk(chunk=chunk, score=0.91)


def test_parse_timestamp_seconds_reads_bracket_and_line_times():
    assert parse_timestamp_seconds("Intro [12:34] later") == 12 * 60 + 34
    assert parse_timestamp_seconds("1:02:03 we started discovery") == 3723
    assert parse_timestamp_seconds("no clock here") is None


def test_watch_url_adds_timestamp_only_when_known():
    url = watch_url("dQw4w9wgXcQ", "https://www.youtube.com/watch?v=dQw4w9wgXcQ", 94)
    assert url.endswith("t=94s")
    assert watch_url("not-a-youtube-id", None, 10) is None


def test_source_payload_is_numbered_and_omits_invented_times():
    item = _chunk("Teams validate problems before building.")
    payload = source_payload(item, 1)
    assert payload["n"] == 1
    assert payload["guest"] == "Teresa Torres"
    assert payload["start_seconds"] is None
    assert payload["excerpt"]
    timed = source_payload(_chunk("[08:15] Opportunity solution trees."), 2)
    assert timed["start_seconds"] == 8 * 60 + 15
    assert "t=495s" in timed["source_url"]


def test_filter_used_sources_drops_uncited_chunks():
    sources = numbered_sources(
        [
            _chunk("one", transcript_id=1, chunk_id=1),
            _chunk("two", transcript_id=2, chunk_id=2, title="Other"),
        ]
    )
    used = filter_used_sources("Only the first claim matters [1].", sources)
    assert [item["n"] for item in used] == [1]


def test_filter_used_sources_keeps_all_when_model_forgets_to_cite():
    sources = numbered_sources([_chunk("one"), _chunk("two", transcript_id=2, chunk_id=2)])
    assert len(filter_used_sources("No markers here.", sources)) == 2


def test_format_context_uses_source_labels_models_must_cite():
    context = format_context([_chunk("Validate the problem first.")])
    assert "Source [1] Discovery vs execution — Teresa Torres" in context


def test_diversify_chunks_caps_per_episode_then_fills():
    items = [
        _chunk("a", transcript_id=1, chunk_id=1),
        _chunk("b", transcript_id=1, chunk_id=2),
        _chunk("c", transcript_id=1, chunk_id=3),
        _chunk("d", transcript_id=2, chunk_id=4, title="Other"),
    ]
    selected = diversify_chunks(items, top_k=3, max_per_transcript=2)
    counts = {}
    for item in selected:
        counts[item.chunk.transcript_id] = counts.get(item.chunk.transcript_id, 0) + 1
    assert counts[1] == 2
    assert counts[2] == 1
