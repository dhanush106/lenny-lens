# Project Planning Checklist

## Phase 0 — Understand the assignment
- [ ] Read the assignment and extract all explicit requirements.
- [ ] Identify mandatory vs optional scope.
- [ ] Define primary user, secondary user, and evaluator context.
- [ ] Document the problem, assumptions, risks, trade-offs, and success metrics.
- [ ] Confirm what will be in scope vs out of scope.

## Phase 1 — Product discovery / PRD
- [ ] Define user personas and primary tasks.
- [ ] Write the product problem statement.
- [ ] Capture the user jobs and workflow.
- [ ] Define measurable success metrics.
- [ ] Record assumptions and constraints.
- [ ] Define scope and non-goals.
- [ ] Document risks and mitigations.
- [ ] Write acceptance criteria.
- [ ] Define the initial API endpoints.
- [ ] Finalize the PRD for implementation.

## Phase 2 — Architecture
- [ ] Define high-level architecture diagram.
- [ ] Identify backend layers, services, and repositories.
- [ ] Define API contracts and payload shapes.
- [ ] Design database schema for sessions, messages, transcripts, and chunks.
- [ ] Define retrieval and RAG flow.
- [ ] Define agent routing and skills.
- [ ] Define model abstraction for local and cloud LLMs.
- [ ] Define artifact security model (sanitization + sandboxing).
- [ ] Document deployment topology and local running setup.

## Phase 3 — Repository setup
- [ ] Initialize Git repository.
- [ ] Create .gitignore and environment template.
- [ ] Create the initial project folder structure.
- [ ] Add backend, frontend, docs, ingestion, scripts, and docker folders.
- [ ] Prepare baseline README and contributor notes.

## Phase 4 — Backend foundation
- [ ] Create Python environment.
- [ ] Install backend dependencies.
- [ ] Initialize FastAPI app.
- [ ] Add /health endpoint.
- [ ] Add request validation and structured error handling.
- [ ] Configure environment settings and app config.

## Phase 5 — Database and persistence
- [ ] Run PostgreSQL locally or via Docker.
- [ ] Configure SQLAlchemy/ORM.
- [ ] Create user, session, message, transcript, and chunk models.
- [ ] Add Alembic migrations.
- [ ] Verify DB connectivity and migration success.
- [ ] Test session isolation and message persistence.

## Phase 6 — Transcript ingestion
- [ ] Identify data source and metadata contract.
- [ ] Build transcript ingest pipeline.
- [ ] Clean and normalize transcript content.
- [ ] Extract metadata such as title, episode, speaker, timestamp, and source URL.
- [ ] Store ingested transcripts in the database.

## Phase 7 — Chunking and embeddings
- [ ] Design chunking approach and chunk size/overlap strategy.
- [ ] Preserve source metadata in each chunk.
- [ ] Select embedding model and document rationale.
- [ ] Generate embeddings for transcript chunks.
- [ ] Store embeddings in PostgreSQL vector storage.
- [ ] Test retrieval relevance quality.

## Phase 8 — Retrieval and RAG
- [ ] Build semantic similarity search.
- [ ] Add metadata filters for episode and source context.
- [ ] Expose retrieval scores and source metadata.
- [ ] Build grounded answer service using transcript context.
- [ ] Add citation support in the response.
- [ ] Handle empty retrieval and unsupported Q&A gracefully.

## Phase 9 — LLM provider abstraction
- [ ] Define LLM provider interface.
- [ ] Implement Ollama provider.
- [ ] Implement cloud provider (Anthropic or OpenAI).
- [ ] Add provider factory and runtime configuration.
- [ ] Add graceful fallback behavior.
- [ ] Validate the active model provider setup.

## Phase 10 — Agent architecture
- [ ] Design agent routing logic.
- [ ] Define main skills: Q&A, essay, artifact generation.
- [ ] Integrate the chosen agent framework.
- [ ] Add prompt grounding instructions.
- [ ] Implement routing between Q&A vs content vs artifact jobs.
- [ ] Add error handling and fallback behavior.

## Phase 11 — Conversational assistant
- [ ] Create /chat endpoint.
- [ ] Load session history and conversation context.
- [ ] Save messages and assistant responses.
- [ ] Support follow-up question flows.
- [ ] Add streaming responses if feasible.
- [ ] Validate end-to-end assistant responses.

## Phase 12 — Ship 30 for 30 skill
- [ ] Study the underlying writing principles.
- [ ] Define essay schema and structure.
- [ ] Generate a 1,250-word style long-form essay grounded in transcript evidence.
- [ ] Enforce narrative hook, skimmable sections, takeaway, and source grounding.
- [ ] Test generated essays for structure and quality.

## Phase 13 — Artifact generation
- [ ] Define artifact types (Markdown and HTML).
- [ ] Create artifact data model and generation pipeline.
- [ ] Generate Markdown artifacts.
- [ ] Generate HTML/CSS artifacts.
- [ ] Expose artifact generation endpoint.
- [ ] Validate output quality and formatting.

## Phase 14 — Artifact security
- [ ] Document XSS risks and threat model.
- [ ] Define allowed HTML policy and blocked tags/protocols.
- [ ] Implement HTML sanitization.
- [ ] Add sandboxing or isolated rendering strategy.
- [ ] Add CSP or equivalent security controls if needed.
- [ ] Create malicious payload tests.

## Phase 15 — Frontend UI
- [ ] Initialize React + Vite frontend.
- [ ] Create responsive app layout.
- [ ] Build session sidebar and new conversation flow.
- [ ] Build chat messages and input controls.
- [ ] Connect frontend to backend chat API.
- [ ] Add loading, error, and empty states.
- [ ] Render Markdown and sources clearly.

## Phase 16 — Artifact viewer
- [ ] Create artifact panel in the frontend.
- [ ] Render Markdown artifacts.
- [ ] Render sanitized HTML artifacts in a secure container.
- [ ] Connect artifact generation workflow to the viewer.
- [ ] Add artifact states for generating, success, empty, and error.

## Phase 17 — Full integration
- [ ] Connect frontend to FastAPI chat flow.
- [ ] Connect Q&A flow end-to-end.
- [ ] Connect essay generation workflow.
- [ ] Connect artifact generation workflow.
- [ ] Persist the full conversation lifecycle.

## Phase 18 — Testing
- [ ] Add unit tests for chunking, prompt building, routing, and validation.
- [ ] Add API tests for sessions, chat, health, and artifacts.
- [ ] Add retrieval tests.
- [ ] Add routing tests.
- [ ] Add persistence tests.
- [ ] Add failure case tests for model outage, DB failure, empty retrieval, and invalid artifact.
- [ ] Create a manual UI smoke test plan.

## Phase 19 — Observability
- [ ] Add structured logging.
- [ ] Add request correlation IDs.
- [ ] Instrument retrieval latency and LLM latency.
- [ ] Expand health checks for API, DB, and model services.
- [ ] Review logs for failure diagnosis.

## Phase 20 — Resilience
- [ ] Handle missing API keys gracefully.
- [ ] Handle Ollama unavailable gracefully.
- [ ] Add model timeout handling.
- [ ] Add DB and retrieval failure handling.
- [ ] Handle empty retrieval and artifact generation failure states.

## Phase 21 — Docker and deployment
- [ ] Containerize backend.
- [ ] Containerize frontend.
- [ ] Add PostgreSQL service.
- [ ] Configure local Ollama setup.
- [ ] Add docker-compose stack.
- [ ] Add container health checks.
- [ ] Test clean startup from scratch.

## Phase 22 — Data ingestion automation
- [ ] Add a transcript ingestion command.
- [ ] Ensure ingestion is idempotent.
- [ ] Add refresh and re-index logic.
- [ ] Add ingestion logging and summary output.

## Phase 23 — Documentation and handoff
- [ ] Update README with prerequisites and install steps.
- [ ] Document Ollama setup and cloud model configuration.
- [ ] Document API usage and troubleshooting.
- [ ] Finalize architecture and design docs.
- [ ] Add agent transcripts / build logs.
- [ ] Prepare evaluation checklist and demo script.

## Phase 24 — Final review and submission
- [ ] Confirm secrets are not committed.
- [ ] Verify no unrestricted HTML execution.
- [ ] Validate parameterized DB queries and validation coverage.
- [ ] Review logs for sensitive data leakage.
- [ ] Conduct final refactor and code cleanup.
- [ ] Check repository status and final git history.
- [ ] Prepare final GitHub submission and demo evidence.

## API endpoints to define early
- [ ] GET /health
- [ ] POST /sessions
- [ ] GET /sessions
- [ ] GET /sessions/{session_id}
- [ ] POST /chat
- [ ] POST /artifacts
- [ ] GET /artifacts/{artifact_id} (optional if persistence is added)

## Core architectural flow
- [ ] Frontend -> API -> Agent -> Skills -> Retrieval -> Database -> LLM
- [ ] Ensure responses are grounded in transcript evidence
- [ ] Ensure artifact generation is safe and reviewable
- [ ] Ensure sessions remain isolated and persistent

## Definition of done
- [ ] PRD is complete.
- [ ] Architecture is mapped.
- [ ] Data flow is clear.
- [ ] API routes are defined.
- [ ] Retrieval and grounding are implemented.
- [ ] Agent and skills are working.
- [ ] Frontend and artifact viewer are connected.
- [ ] Tests and security checks are passing.
- [ ] Docker startup works.
- [ ] Documentation supports a clean handoff.
