# LennyLens Architecture

LennyLens is a modular monolith: React chat UI, FastAPI, PostgreSQL/pgvector, a deterministic skill router, and a configurable LLM provider (Ollama or Anthropic).

## Request path

```text
POST /api/v1/sessions/{id}/chat
  → persist user message
  → classify intent (qna | essay | artifact)
  → retrieve diversified transcript chunks
  → number evidence [1]…[n]
  → skill-specific generation
  → keep only cited sources
  → persist assistant message (content, sources, optional artifact)
```

Chat never stores raw artifact JSON in `content`. Essays and HTML canvases live on `messages.artifact`.

## Agent SDK trade-off

The assignment lists the Anthropic Claude Agent SDK and Pi Coding Agent. Those are coding-agent runtimes (filesystem, shell). This product is a grounded research assistant, so routing is deterministic and each skill is a testable tool. LLM calls happen after retrieval. That is stricter isolation than an unconstrained agent loop.

## Citations

`backend/services/citations.py` is the contract: `n`, title, guest, excerpt, optional timestamp parsed from `[mm:ss]` in the chunk, and a source URL. YouTube `t=` is added only when a timestamp was parsed. Retrieval fetches extra candidates then caps two chunks per episode.

## Artifacts and security

HTML is Bleach-sanitized, then rendered in an iframe with `sandbox=""` and a CSP that allows only inline CSS. Markdown is rendered as text. Permit: static HTML/CSS and markdown. Block: script, event handlers, forms, iframes, network images, javascript URLs.

## Runtime visibility

`GET /api/v1/runtime` and `GET /api/v1/ready` expose provider, model, and retrieval mode without secrets. The sidebar shows the same values.

## Deployment

`docker compose up --build` starts Postgres, runs Alembic, and serves the API and UI. Ollama stays on the host; the API container reaches it at `host.docker.internal:11434`.
