from backend.models.chunk import Chunk
from backend.models.transcript import Transcript
from backend.services.retrieval import RetrievedChunk, rerank_candidates, understand_query


def _candidate(title: str, text: str, score: float = 0.5, transcript_id: int = 1) -> RetrievedChunk:
    transcript = Transcript(id=transcript_id, video_id=f"video-{transcript_id}", title=title, guest="Guest")
    chunk = Chunk(id=transcript_id, transcript_id=transcript_id, text=text)
    chunk.transcript = transcript
    return RetrievedChunk(chunk=chunk, score=score)


def test_query_understanding_expands_product_growth_intent():
    intent = understand_query("Give me principles for product growth")
    assert intent.task == "artifact_generation"
    assert {"product", "growth"}.issubset(intent.domain)
    assert {"activation", "retention", "monetization"}.issubset(set(intent.concepts))


def test_activation_relevance_outranks_generic_growth_mention():
    candidates = [
        _candidate("General product discussion", "Growth is important for every company.", 0.9),
        _candidate("Activation and onboarding", "Improve activation by studying onboarding and user behavior.", 0.7, 2),
    ]
    ranked = rerank_candidates(candidates, understand_query("How can I improve activation?"))
    assert ranked[0].chunk.transcript.title == "Activation and onboarding"


def test_growth_tactics_query_prefers_growth_source():
    candidates = [
        _candidate("Writing style tips", "Present one idea at a time.", 0.9),
        _candidate("Growth tactics that never work", "Avoid growth tactics that ignore retention and user behavior.", 0.7, 2),
    ]
    ranked = rerank_candidates(candidates, understand_query("What growth tactics should a startup avoid?"))
    assert ranked[0].chunk.transcript.title == "Growth tactics that never work"


def test_retention_query_prefers_retention_source():
    candidates = [
        _candidate("Career emotions", "Personal principles can accelerate your career.", 0.9),
        _candidate("Retention and churn", "Retention depends on engagement, habits, and reducing churn.", 0.7, 2),
    ]
    ranked = rerank_candidates(candidates, understand_query("How should I think about retention?"))
    assert ranked[0].chunk.transcript.title == "Retention and churn"


def test_engineering_management_query_prefers_management_source():
    candidates = [
        _candidate("Product growth", "Activation and monetization patterns matter.", 0.8),
        _candidate("Engineering management", "Engineering managers should hold effective one-on-ones and lead teams.", 0.7, 2),
    ]
    ranked = rerank_candidates(candidates, understand_query("What does Lenny say about engineering management?"))
    assert ranked[0].chunk.transcript.title == "Engineering management"