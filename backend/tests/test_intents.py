from backend.agent.intents import classify_intent, expand_retrieval_query, requested_artifact_format


def test_classify_intent_prefers_explicit_skills():
    assert classify_intent("What are good discovery practices?") == "qna"
    assert classify_intent("Write a Ship 30 essay about prioritization.") == "essay"
    assert classify_intent("Create an HTML product strategy canvas.") == "artifact"
    assert classify_intent("Turn this into an artifact") == "artifact"
    assert classify_intent("Render this as an artifact") == "artifact"
    assert classify_intent("ok") == "chat"


def test_requested_artifact_format_is_explicit():
    assert requested_artifact_format("Generate a Markdown artifact") == "markdown"
    assert requested_artifact_format("Create an HTML artifact") == "html"


def test_expand_retrieval_query_uses_prior_question_and_assistant_takeaway():
    history = [
        {"role": "user", "content": "How should teams do discovery versus execution?"},
        {"role": "assistant", "content": "Guests argue validation comes first."},
        {"role": "user", "content": "compare those two approaches"},
    ]
    expanded = expand_retrieval_query("compare those two approaches", history)
    assert "discovery versus execution" in expanded
    assert "validation comes first" in expanded
    assert expanded.endswith("compare those two approaches")
