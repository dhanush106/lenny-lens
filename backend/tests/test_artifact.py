from backend.agent.skills.artifact import ArtifactSkill, choose_template
from backend.agent.skills.essay import essay_title
from backend.services.security import sanitize_html


def test_choose_template_from_user_language():
    assert "HTML" in choose_template("Create an HTML strategy canvas")
    assert "comparison" in choose_template("Build a comparison table of the two approaches")
    assert "Markdown" in choose_template("Write a one-pager brief")


def test_artifact_payload_is_sanitized_and_structured():
    raw = """
    {
      "artifact_type": "html",
      "title": "Discovery canvas",
      "summary": "A one-page canvas.",
      "content": "<h1>Canvas</h1><script>alert(1)</script><p>Validate first [1]</p>"
    }
    """
    sources = [{"n": 1, "title": "Discovery vs execution", "guest": "Teresa Torres"}]
    artifact = ArtifactSkill._validate_and_sanitize_artifact(raw, sources)
    assert artifact["type"] == "artifact"
    assert artifact["format"] == "html"
    assert artifact["title"] == "Discovery canvas"
    assert "<script" not in artifact["content"]
    assert "Validate first" in artifact["content"]
    assert artifact["content"].startswith("<!doctype html>")


def test_malformed_artifact_json_fails_closed():
    assert ArtifactSkill._validate_and_sanitize_artifact("not json", []) is None
    assert ArtifactSkill._validate_and_sanitize_artifact('{"artifact_type":"pdf"}', []) is None


def test_requested_markdown_can_be_returned_without_json_wrapper():
    artifact = ArtifactSkill._validate_and_sanitize_artifact(
        "# 5 Principles\n\nValidate first [1].",
        [{"n": 1}],
        requested_format="markdown",
    )
    assert artifact["type"] == "artifact"
    assert artifact["format"] == "markdown"
    assert artifact["content"].startswith("# 5 Principles")


def test_html_is_sanitized_for_sandboxed_preview():
    artifact = ArtifactSkill._validate_and_sanitize_artifact(
        '{"artifact_type":"html","content":"<script>alert(1)</script><h1>Safe</h1>"}',
        [],
        requested_format="html",
    )
    assert "<script" not in artifact["content"]
    assert "<!doctype html>" in artifact["content"]


def test_essay_title_from_heading():
    assert essay_title("# Stop shipping unvalidated bets\n\nHook here") == "Stop shipping unvalidated bets"


def test_html_footer_uses_allowed_tags():
    cleaned = sanitize_html('<div class="sources"><h3>Sources</h3><ol><li>[1] Title</li></ol></div>')
    assert "Sources" in cleaned
    assert "<script" not in cleaned


def test_artifact_response_schema_is_stable():
    artifact = ArtifactSkill._validate_and_sanitize_artifact(
        '{"artifact_type":"markdown","title":"Growth","content":"# Growth"}',
        [],
        requested_format="markdown",
    )
    assert set(("type", "format", "title", "content", "summary")).issubset(artifact)
    assert artifact["type"] == "artifact"


def test_grounded_fallback_artifact_is_available_when_model_claims_fail():
    markdown = ArtifactSkill._build_evidence_artifact(
        "Create a Markdown artifact",
        "markdown",
        "Growth Evidence",
        [{"evidence": "Find recurring patterns instead of re-engineering them.", "source": 1, "confidence": 0.9}],
        [{"n": 1, "title": "Growth tactics", "guest": "Elena Verna"}],
    )
    assert "# Growth Evidence" in markdown
    assert "Find recurring patterns" in markdown
    assert "[1]" in markdown


def test_grounded_html_fallback_is_self_contained():
    html = ArtifactSkill._build_evidence_artifact(
        "Create an HTML artifact",
        "html",
        "Growth Evidence",
        [{"evidence": "Find recurring patterns instead of re-engineering them.", "source": 1, "confidence": 0.9}],
        [{"n": 1, "title": "Growth tactics", "guest": "Elena Verna"}],
    )
    assert html.startswith("<!doctype html>")
    assert "<style>" in html
    assert "Find recurring patterns" in html


def test_grounded_fallback_content_is_not_overwritten():
    fallback = ArtifactSkill._build_evidence_artifact(
        "Create an HTML artifact",
        "html",
        "Strategy Canvas",
        [{"evidence": "Strategy connects direction to execution.", "source": 1, "confidence": 0.9}],
        [{"n": 1, "title": "Strategy", "guest": "Guest"}],
    )
    grounded_content = ""
    if fallback:
        grounded_content = fallback
    assert grounded_content.startswith("<!doctype html>")
    assert "Strategy connects direction to execution." in grounded_content
