# Phase 0: MVP Definition

## 1. MVP goal
Build a minimal but reliable product that demonstrates the full workflow:
- ingest transcript knowledge
- retrieve relevant evidence
- answer grounded questions
- generate a Ship 30 style essay
- create a safe artifact output
- expose the experience through a usable interface

## 2. In-scope features for the MVP
- FastAPI backend with health endpoint
- PostgreSQL-backed session and message persistence
- Transcript ingestion and chunking pipeline
- Embedding generation and vector retrieval
- Local LLM support via Ollama and optional cloud model fallback
- Agent router with a small number of clear skills
- Chat interface with session context
- Artifact generation workflow
- Artifact viewer with untrusted HTML protection
- Logging, error handling, and configuration management
- Docker-based local startup
- Test coverage for critical user flows

## 3. Out-of-scope features for the MVP
- Multi-user auth and billing
- Enterprise RBAC
- Social network or collaborative editing features
- Mobile-native experience
- Fine-tuned custom model training
- Broad analytics dashboard
- Large-scale production deployment architecture

## 4. MVP success definition
The MVP is successful when a user can:
1. Start a conversation in a session
2. Ask a question grounded in transcript content
3. Receive an answer with source references
4. Request a Ship 30 style content artifact
5. View the generated artifact safely in the app
6. Run the whole project from setup instructions without hidden steps

## 5. Quality bar
The MVP should prioritize reliability over feature breadth. Small, well-tested flows are preferred over a large but brittle system.
