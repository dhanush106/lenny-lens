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
   cp .env.example .env
   # Add your ANTHROPIC_API_KEY if desired.
   ```

2. **Run via Docker Compose**
   ```bash
   docker-compose up --build
   ```

3. **Access the App**
   Open your browser and navigate to `http://localhost`.

## 📚 Documentation
- [Architecture](docs/architecture.md)
- [Design Decisions](docs/design.md)
- [Manual Test Plan](docs/manual-test-plan.md)

## 🔧 Troubleshooting
- **Database Connection Fails**: Ensure port 5433 isn't blocked and the `pgvector` container is healthy.
- **Ollama Timeout**: If using a local model, ensure `host.docker.internal` is accessible from the container.

---
*Built with FastAPI, React, TailwindCSS, and PostgreSQL/pgvector.*
