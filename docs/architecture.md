# LennyLens Architecture

## 1. Overview
The Lenny Growth Assistant utilizes a decoupled modern architecture:
- **Frontend**: React + Tailwind CSS + Vite
- **Backend**: FastAPI
- **Database**: PostgreSQL with `pgvector`
- **Models**: Configurable (Local Ollama `llama3` or Cloud Anthropic `claude-3-haiku-20240307`)

## 2. Core Components
- **API Router (`api/`)**: Exposes REST endpoints for session and message management.
- **Services (`services/`)**: Contains logic for LLM communication, RAG execution, and security sanitization.
- **Agent (`agent/`)**: An Intent Router that analyzes user queries and passes execution context to specialized Skills (QnA, Essay, Artifact).
- **Scripts (`scripts/`)**: Idempotent transcript ingestion workflow that parses, hashes, and updates vectors in the database without duplication.
