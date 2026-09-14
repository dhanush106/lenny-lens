# Lenny Growth Assistant

Full-stack assistant that answers product and growth questions from Lenny's Podcast transcripts, writes Ship 30 essays, and renders sandboxed HTML/Markdown artifacts beside the chat.

## Features
- **Grounded Q&A** with inline `[n]` citations, guest/episode source cards, and optional YouTube timestamps when the transcript actually contains them
- **Ship 30 for 30** essays that open in the artifact viewer (~1,250 words, hook, headings, takeaway)
- **Artifact viewer** with Preview / Source, copy, download, and pop-out; HTML is Bleach-sanitized and iframed with `sandbox=""`
- **Visible LLM checklist** in the sidebar showing the selected Ollama, OpenAI, or Claude model and configuration state
- **Idempotent ingestion** of the ChatPRD transcript archive

## Prerequisites
- Docker and Docker Compose
- Ollama on the host for the local demo, with a chat model and `all-minilm` if you use semantic retrieval

## Getting Started

1. **Clone and configure**
   ```bash
   copy .env.example .env
   # macOS/Linux: cp .env.example .env
   # Demo default: LLM_PROVIDER=ollama. For cloud, set LLM_PROVIDER=openai or anthropic and the matching API key.
   ```

2. **Run**
   ```bash
   docker compose up --build
   ```

3. **Open**
   - App: `http://localhost`
   - Health: `http://localhost:8000/api/v1/health`
   - Runtime (provider/model): `http://localhost:8000/api/v1/runtime`

4. **Tests**
   ```bash
   docker compose exec -e PYTHONPATH=/app backend pytest -q
   cd frontend && npm run build && npm run lint
   ```

Alembic runs at API startup. The local demo user is created automatically; it is not authentication.

### Load transcript evidence

```bash
git clone https://github.com/ChatPRD/lennys-podcast-transcripts data/lennys-podcast-transcripts
ollama pull qwen3.5:2b
ollama pull all-minilm
docker compose exec backend python -m backend.scripts.ingest --dir /app/data/transcripts
docker compose exec backend python -m backend.scripts.diagnostics --query "product discovery versus execution"
```

Match `.env` `OLLAMA_MODEL` to a model you actually pulled. Changing embedding model or dimension requires re-ingest.

### LLM provider configuration

Use the sidebar’s **Local / Cloud** toggle to change the running demo without editing code or restarting. The selection and cloud key are held only in backend memory until the backend restarts. `.env` remains the default configuration used at startup.

| Provider | Required configuration | Suggested use |
| --- | --- | --- |
| Ollama (local) | `LLM_PROVIDER=ollama`, `OLLAMA_MODEL=qwen3.5:2b` | Required demo path; run `ollama pull qwen3.5:2b` first. |
| OpenAI (cloud) | `LLM_PROVIDER=openai`, `OPENAI_API_KEY`, `OPENAI_MODEL` | Cloud Responses API. |
| Claude (cloud) | `LLM_PROVIDER=anthropic`, `ANTHROPIC_API_KEY`, `ANTHROPIC_MODEL` | Anthropic Messages API. |
| OpenRouter (cloud) | Select OpenRouter in the sidebar and provide an API key | Loads the live OpenRouter model catalog. |

The local toggle lists models installed in the running Ollama server. Cloud mode has provider and API-key inputs; OpenAI and OpenRouter can load their model catalogs. Failures never silently change providers: missing keys, unreachable Ollama, and cloud API failures return a clear error.

If Ollama reports embeddings unsupported, restart it with embeddings enabled before switching `RETRIEVAL_MODE=semantic`.

## Documentation
- [PRD](docs/PRD.md)
- [Architecture](docs/architecture.md)
- [Design](docs/design.md)
- [Manual test plan](docs/manual-test-plan.md)
- [Agent transcripts](agent-transcripts/README.md)

## Troubleshooting
- **Database**: `docker compose ps`; Postgres must be healthy. Host port is `5433`.
- **Ollama**: the API container uses `host.docker.internal:11434`. Timeouts return a 503 instead of crashing.
- **No answer**: ingest transcripts first; empty retrieval declines instead of guessing.
- **HTML looks empty**: the viewer only allows a static tag/CSS allowlist. Scripts are stripped on purpose.

Built with FastAPI, React, Tailwind CSS, and PostgreSQL/pgvector.
