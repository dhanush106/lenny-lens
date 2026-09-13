# Lenny Growth Assistant 🚀

Lenny Growth Assistant is a full-stack, AI-powered conversational application designed to help users extract actionable product growth insights from the *Lenny's Podcast* transcripts.

## 🌟 Features
- **Grounded Q&A**: Uses RAG (Retrieval-Augmented Generation) against a PostgreSQL vector database (`pgvector`) to provide grounded, hallucination-free answers.
- **Ship 30 for 30 Engine**: Generates highly-structured essays based on podcast context.
- **Dynamic Artifact Rendering**: Securely generates and renders HTML/Markdown artifacts right next to your chat!
- **Idempotent Ingestion**: Easily keep your knowledge base up-to-date with intelligent hashing.

## 🛠 Prerequisites
- Docker & Docker Compose
- (Optional) Local Ollama instance running `llama3` if not using Anthropic.

## 🚀 Getting Started

1. **Clone & Configure**
   ```bash
   copy .env.example .env
   # On macOS/Linux: cp .env.example .env
   # Use Ollama locally, or set LLM_PROVIDER=anthropic and add ANTHROPIC_API_KEY.
   ```

2. **Run via Docker Compose**
   ```bash
   docker compose up --build
   ```

3. **Access the App**
   Open `http://localhost`. Confirm the API is ready at
   `http://localhost:8000/api/v1/health`.

4. **Run automated checks**
   ```bash
   docker compose exec -e PYTHONPATH=/app backend pytest -q
   cd frontend && npm run build && npm run lint
   ```

The backend runs Alembic migrations at startup. The local demo account is
created automatically; it is not an authentication feature.

### Load transcript evidence

The repository intentionally does not include Lenny's transcript corpus. Place
authoritative `.md` transcript files in `data/transcripts/`, start Ollama, and
pull both configured models before ingesting:

```bash
ollama pull llama3
ollama pull all-minilm
# The embedding endpoint must be enabled by the local Ollama server. If the
# server reports that embeddings are unsupported, restart it with --embeddings.
docker compose exec backend python -m backend.scripts.ingest --dir /app/data/transcripts
docker compose exec backend python -m backend.scripts.diagnostics --query "product discovery versus execution"
```

Ingestion and querying use the same configured embedding model and dimension.
Changing either requires re-ingesting the corpus.

## 📚 Documentation
- [Architecture](docs/architecture.md)
- [Design decisions](docs/design.md)
- [Manual test plan](docs/manual-test-plan.md)

## 🔧 Troubleshooting
- **Database Connection Fails**: Run `docker compose ps`; the `db` service must be healthy. Ensure port 5433 isn't blocked.
- **Ollama Timeout**: If using a local model, ensure `host.docker.internal` is accessible from the container.
- **No answer available**: Ingest transcript files before asking questions; the assistant deliberately declines unsupported questions when retrieval is empty.

---
*Built with FastAPI, React, TailwindCSS, and PostgreSQL/pgvector.*
