# Technical Requirements

## 1. Product objective
LennyLens is a grounded knowledge assistant for product and growth teams. It provides semantic search over Lenny's podcast and newsletter transcript corpus, conversation-based Q&A, content generation, and safe artifact rendering.

## 2. Functional requirements

### 2.1 Session management
- Users must be able to create a new conversation session.
- Sessions must be independent from one another.
- Messages and agent responses must be stored per session.
- Users must be able to load previous session history.

### 2.2 Conversational Q&A
- Users must be able to ask product or growth questions.
- The system must retrieve transcript evidence before answering.
- Answers must include relevant source references.
- If evidence is insufficient, the system must say so clearly.

### 2.3 Retrieval and grounding
- Transcript content must be chunked into retrievable units.
- Chunks must retain source metadata.
- Query text must be embedded and compared to stored embeddings.
- Top-k relevant chunks must be used to ground responses.
- Retrieval results must include source metadata and relevance scores.

### 2.4 Transcript ingestion
- Transcript data must be loaded and normalized.
- Transcript metadata must be extracted.
- Data must be chunked into retrievable segments.
- Embeddings must be generated and stored.
- Ingestion must be idempotent and refreshable.

### 2.5 Agent routing
- The system must route requests to the correct capability.
- Supported intents include Q&A, essay generation, and artifact generation.
- Routing must be deterministic enough to be tested.

### 2.6 Ship 30 for 30 skill
- The app must support essay generation grounded in transcript evidence.
- Essay output should roughly target 1,250 words.
- It should include a hook, scannable sections, a takeaway, and source grounding.

### 2.7 Artifact generation
- The app must generate Markdown or HTML artifacts.
- Artifact generation must be tied to a session and source-backed context.
- Users must be able to review generated artifacts in the UI.

### 2.8 Artifact security
- Generated HTML must be treated as untrusted content.
- HTML must be sanitized before rendering.
- Unsafe tags, event handlers, javascript: URLs, and script execution vectors must be blocked.
- The artifact viewer should isolate generated content from the main app context.

### 2.9 LLM provider abstraction
- The app must support at least one local model provider and one cloud provider.
- Model provider selection must be configurable through environment variables.
- The application should not depend directly on one provider implementation.

### 2.10 Observability and troubleshooting
- The app must emit structured logs for API calls, retrieval, model calls, and artifacts.
- Logs must include request IDs, session IDs, and operation duration.
- Health monitoring should cover API, database, and model availability.

### 2.11 Deployment
- The app must have a reproducible local startup path.
- Docker Compose should be able to run the core stack.
- Environment configuration must be documented and isolated in .env.example.

## 3. Non-functional requirements

### 3.1 Reliability
- Missing configuration, database failures, model outages, and empty retrievals must fail gracefully.
- The application must not silently hallucinate when evidence is absent.

### 3.2 Security
- No secrets may be committed to source control.
- Generated HTML must never run unrestricted in the main app DOM.
- DB queries and user input validation must be parameterized and validated.

### 3.3 Maintainability
- The architecture must separate frontend, API, business logic, retrieval, database, security, and deployment concerns.
- Each major capability must have a clear owner and test boundary.

### 3.4 Extensibility
- New skills and providers should be added without rewriting the core system.
- The architecture must favor clear boundaries over over-engineering.

### 3.5 Performance
- Retrieval should return a small number of relevant chunks for grounded generation.
- Long-running model requests should be bounded by timeouts.
- The app should favor correctness and traceability over excessive complexity.

## 4. Technical constraints
- Backend must be FastAPI.
- PostgreSQL must be the durable data store.
- Vector storage must be supported within the database layer or with a compatible PostgreSQL extension.
- Local execution must work with Ollama or an equivalent local model path.
- Cloud LLM support is optional but necessary for provider flexibility.
- The project must be operable by an evaluator in a fresh environment with documentation.

## 5. Mapping to system components

| Requirement | Core technical component |
| --- | --- |
| Sessions and persistence | PostgreSQL + session services |
| Q&A and retrieval | RAG pipeline + vector search |
| Essay generation | Agent skill + prompt + synthesis |
| Artifact generation | Artifact service + sanitizer + viewer |
| Model switching | LLM provider abstraction |
| Local execution | Ollama + configuration |
| UI interaction | React frontend |
| API logic | FastAPI routes + services |
| Security | Sanitizer, sandbox, trust boundaries |
| Deployment | Docker Compose + env config |
| Failure handling | error handling, logging, health checks |

## 6. Acceptance criteria for technical implementation
- Every PRD requirement maps to a technical component or service.
- Session state is isolated and persisted.
- Q&A uses retrieval before generation.
- The app can use local and cloud model providers.
- Generated HTML is sanitized and isolated.
- Artifact generation and chat flows are testable.
- Docker and environment configuration support a fresh setup path.
- The system is understandable enough for evaluator handoff.
