# Product Requirements Document (PRD)

## 1.1 Primary users and personas

### Primary user
Product and growth team members

### Secondary user
Internal client/evaluator

### User personas
- Product and growth professionals who need fast insight from large transcript archives
- Internal stakeholders evaluating whether the system is useful, grounded, and reliable

### Core user need
Users need to discover product and growth insight from Lenny's podcast and newsletter transcripts without reading every episode manually.

---

## 1.2 Problem statement

Product and growth teams need to extract actionable product and growth insights from Lenny's podcast transcripts without manually searching through large volumes of transcript content. The problem is not just finding information, but finding the right evidence quickly and being able to trust that the answer is grounded in the transcript corpus.

---

## 1.3 User jobs

The core jobs this product must support are:

- Ask a product question
- Ask a follow-up question
- Find supporting source material
- Generate an essay
- Generate a document
- Generate an HTML artifact
- Review generated artifact
- Start a new conversation

These jobs reflect a workflow that moves from discovery to synthesis to artifact creation.

---

## 1.4 Success metrics

The product should be measured using the following outcomes:

- Grounded-answer success rate
- Retrieval relevance quality
- Response latency
- Artifact generation success rate
- Application startup success rate
- Session continuity quality
- User trust in source-backed answers

### Success thresholds
- The assistant should answer questions using retrieved transcript evidence rather than generic model knowledge.
- Retrieval should surface the most relevant transcript chunks for the given question.
- High-value answers should be returned within a practical response time for a local MVP.
- Generated artifacts should be usable and reviewable without exposing unsafe HTML content.

---

## 1.5 Assumptions

- Users are internal product and growth professionals.
- The transcript repository is the authoritative knowledge source.
- Users prefer concise, useful answers with clear evidence.
- Generated HTML is untrusted and must be sanitized before display.
- Local Ollama models may be lower quality than cloud models but provide a workable local option.
- Product teams will value grounded reasoning more than open-ended conversation.

---

## 1.6 Scope

### In scope
- Chat
- RAG-based evidence retrieval
- Sessions and conversation persistence
- PostgreSQL storage
- Ollama local model support
- Cloud LLM support
- Ship 30 for 30 content skill
- Artifact generation
- Artifact viewer
- Testing
- Dockerized local startup
- Observability

### Out of scope
- Advanced authentication
- Multi-tenant enterprise RBAC
- Fine-tuning
- Mobile app
- Real-time collaborative editing
- Complex analytics dashboard

---

## 1.7 Risks and mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Hallucination | Untrusted responses | Strict grounding using transcript retrieval and source citations |
| Bad retrieval | Irrelevant or weak answers | Retrieval evaluation, chunking discipline, metadata filtering |
| Ollama unavailable | App feature failure for local mode | Graceful fallback to cloud model or clear error state |
| HTML XSS | Unsafe user experience | Sanitization, sandboxing, and safe rendering practices |
| LLM timeout | Failed responses | Timeout handling and user-friendly error messages |
| Database failure | Lost history and broken sessions | Error handling and persistence validation |
| High latency | Poor UX | Logging, model limits, retrieval tuning, and health diagnostics |
| High cost | Unpredictable spend | Prefer local model options and narrow cloud usage |

Key trade-off: prioritize reliability, grounded outputs, and security over broad but shallow functionality.

---

## 1.8 Acceptance criteria

### Acceptance criterion 1: Grounded answer retrieval
Given a product question, when relevant transcript chunks exist, then the assistant answers using those chunks and provides source information.

### Acceptance criterion 2: Session isolation
Given multiple concurrent conversations, when users interact in separate sessions, then the assistant maintains correct conversation context for each session without leaking messages across sessions.

### Acceptance criterion 3: Artifact generation
Given a user asks for an essay or document, when the content can be grounded in transcript evidence, then the system generates a structured artifact with useful formatting and source grounding.

### Acceptance criterion 4: Safe rendering
Given generated HTML content, when it is displayed to the user, then unsafe elements are sanitized or sandboxed before rendering.

### Acceptance criterion 5: Operational reliability
Given missing configuration, unavailable models, or database issues, when the system encounters an error, then it fails gracefully with a clear message and health signals.

### Acceptance criterion 6: Fresh setup
Given a clean environment, when the README instructions are followed, then the application can be started with the documented local workflow.

---

## 1.9 Initial API contract

The backend should expose the following routes as part of the early MVP contract:

- GET /health
- POST /sessions
- GET /sessions
- GET /sessions/{session_id}
- POST /chat
- POST /artifacts

### Endpoint intent
- /health: confirm the service is running and responsive
- /sessions: create and list conversation sessions
- /sessions/{session_id}: retrieve conversation history and state
- /chat: send a question and receive a grounded answer with sources
- /artifacts: create an essay or document artifact from transcript-grounded content

### Response expectations
- Structured JSON responses with clear success and error payloads
- Source metadata attached to answers where transcript evidence is used
- Session-scoped conversation state to preserve independent chat history
- Standardized error handling for missing configuration, DB issues, and model outages

---

## 1.10 Product requirements summary

The final product should function as a grounded assistant for product and growth research built on top of Lenny's transcript knowledge base. It should help users ask informed questions, retrieve relevant evidence, synthesize insight, and create artifacts without sacrificing trust, safety, or operational stability.

This PRD defines the phase-0 planning baseline and gives the implementation team a clear product contract for the rest of the build.

---