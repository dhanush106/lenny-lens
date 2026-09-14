from backend.services.grounding import normalize_evidence, validate_artifact_content, validate_claim


def test_grounding_rejects_more_specific_growth_channel_claim():
    evidence = [{
        "source": 1,
        "evidence": "Look for recurring patterns in activation and monetization rather than trying to re-engineer them.",
        "confidence": 0.9,
    }]
    result = validate_claim(
        "SEO, SEM and social media are the best sustainable growth channels. [1]",
        evidence,
    )
    assert result["accepted"] is False


def test_grounding_accepts_faithful_paraphrase():
    evidence = [{
        "source": 1,
        "evidence": "Look for recurring patterns in activation and monetization rather than trying to re-engineer them.",
        "confidence": 0.9,
    }]
    result = validate_claim(
        "Look for recurring patterns in activation and monetization instead of trying to re-engineer every problem from scratch. [1]",
        evidence,
    )
    assert result["accepted"] is True


def test_grounding_requires_claim_level_citation():
    evidence = [{"source": 1, "evidence": "Retention patterns matter.", "confidence": 0.8}]
    result = validate_claim("Retention patterns matter.", evidence)
    assert result["accepted"] is False


def test_grounding_accepts_retrieval_result_schema_adapter():
    result = validate_claim(
        "Activation patterns should guide product decisions. [7]",
        [{"content": "Activation patterns guide product decisions.", "source_id": 7, "score": 0.82}],
    )
    assert result["accepted"] is True
    assert result["source"] == 7


def test_grounding_accepts_bounded_multi_source_synthesis():
    result = validate_claim(
        "Activation and retention patterns should guide product growth decisions. [1][2]",
        [
            {"evidence": "Study activation patterns.", "source": 1, "confidence": 0.8},
            {"evidence": "Retention patterns guide growth decisions.", "source": 2, "confidence": 0.8},
        ],
    )
    assert result["accepted"] is True


def test_normalize_evidence_drops_empty_items_and_preserves_scores():
    normalized = normalize_evidence([
        {"text": "Useful evidence", "n": 3, "score": 0.82},
        {"content": None, "source_id": 4},
    ])
    assert normalized == [{
        "text": "Useful evidence",
        "n": 3,
        "score": 0.82,
        "evidence": "Useful evidence",
        "source": 3,
        "confidence": 0.82,
    }]


def test_artifact_adds_source_to_supported_uncited_model_claim():
    content, accepted, rejected = validate_artifact_content(
        "## Principle\n\nLook for recurring patterns before reinventing the solution.",
        [{"evidence": "Find recurring patterns instead of trying to re-engineer it.", "source": 1, "confidence": 0.9}],
    )
    assert accepted
    assert not rejected
    assert "[1]" in content


def test_html_strategy_canvas_accepts_supported_multi_source_synthesis():
    html = """<!doctype html><html><head><style>body { color: red; }</style></head><body>
    <h1>Product Strategy Canvas</h1>
    <section><h2>Strategy</h2><p>Strategy connects product direction with the roadmap and goals.</p></section>
    <section><h2>Execution</h2><p>Strategy must translate into execution through the roadmap.</p></section>
    </body></html>"""
    evidence = [
        {"evidence": "Product strategy connects with the roadmap and goals.", "source": 1, "confidence": 0.9},
        {"evidence": "Strong strategy without execution does not produce results.", "source": 2, "confidence": 0.9},
    ]
    content, accepted, rejected = validate_artifact_content(html, evidence)
    assert content.startswith("<!doctype html>")
    assert accepted
    assert not rejected


def test_strategy_canvas_rejects_unsupported_okrs_claim():
    result = validate_claim(
        "Companies should always use OKRs to manage strategy. [1]",
        [{"evidence": "Product strategy connects with the roadmap and goals.", "source": 1, "confidence": 0.9}],
    )
    assert result["accepted"] is False