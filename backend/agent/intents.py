import re

ESSAY_HINTS = ("ship 30", "write an essay", "write a essay", "essay about", "write an article")
ARTIFACT_VERBS = ("generat", "creat", "build", "make", "render", "show me")
ARTIFACT_NOUNS = ("artifact", "canvas", "html page", "html document", "markdown document")
FOLLOWUP_HINTS = (
    "those",
    "these",
    "the two",
    "you mentioned",
    "that approach",
    "those approaches",
    "compare them",
    "compare the",
    "the first",
    "the second",
)


def classify_intent(user_message: str) -> str:
    """Deterministic routing. Prefer explicit skills over a coding-agent loop."""
    normalized = user_message.lower().strip()
    if any(term in normalized for term in ESSAY_HINTS) or (
        "essay" in normalized and any(verb in normalized for verb in ("write", "draft", "ship"))
    ):
        return "essay"

    if is_artifact_request(normalized) or (
        re.search(r"\b(html|css|markdown)\b", normalized)
        and any(verb in normalized for verb in ARTIFACT_VERBS)
    ):
        return "artifact"

    if len(normalized.split()) < 2 or not any(char.isalpha() for char in normalized):
        return "chat"

    return "qna"


def is_artifact_request(user_message: str) -> bool:
    """Recognize explicit artifact requests, including unsupported formats."""
    normalized = user_message.lower().strip()
    return any(noun in normalized for noun in ARTIFACT_NOUNS) or (
        re.search(r"\b(html|css|markdown)\b", normalized)
        and any(verb in normalized for verb in ARTIFACT_VERBS)
    )


def requested_artifact_format(user_message: str) -> str | None:
    normalized = user_message.lower()
    if re.search(r"\b(html|htm)\b", normalized):
        return "html"
    if re.search(r"\b(markdown|md)\b", normalized):
        return "markdown"
    return None


def expand_retrieval_query(query: str, history: list[dict] | None) -> str:
    """Use prior user turns so follow-ups like 'compare the two approaches' still retrieve."""
    if not history:
        return query

    lowered = query.lower()
    is_followup = any(hint in lowered for hint in FOLLOWUP_HINTS) or len(query.split()) <= 8
    if not is_followup:
        return query

    prior_user = [item["content"] for item in history if item.get("role") == "user"]
    previous_question = prior_user[-2] if len(prior_user) >= 2 else (prior_user[0] if prior_user else "")
    last_assistant = ""
    for item in reversed(history):
        if item.get("role") == "assistant":
            last_assistant = (item.get("content") or "")[:400]
            break
    parts = [part for part in (previous_question, last_assistant, query) if part]
    return "\n".join(parts)
