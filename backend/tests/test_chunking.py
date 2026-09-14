from backend.services.chunking import ChunkingService


def test_chunking_prefers_natural_boundaries():
    text = "First complete thought. Second complete thought. Third complete thought."
    chunks = ChunkingService(chunk_size=35, overlap=5).split_text(text)
    assert all(chunk for chunk in chunks)
    assert all(not chunk.startswith("hought") for chunk in chunks[1:])