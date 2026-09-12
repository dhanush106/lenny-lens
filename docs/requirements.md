# Phase 0: Requirements Checklist

## 1. Assignment overview
The assignment requires building a grounded Lenny Growth Assistant that helps product and growth teams explore Lenny's podcast/transcript knowledge base, answer questions with evidence, generate useful content, and produce safe artifacts.

## 2. Required problem framing
- User/problem: Product and growth teams need a fast way to turn a large transcript corpus into reliable product insight without manually reading every relevant episode.
- Success metric: The application should answer questions with grounded evidence, produce useful outputs, maintain session continuity, and run reliably in a local environment.
- Assumptions: The transcript corpus is the source of truth; users want concise, useful answers; local LLMs may be slower or lower quality than cloud providers; the product should work with generated artifacts as untrusted content.
- Scope: A working local MVP with chat, retrieval, transcript grounding, agent routing, artifact generation, security controls, and documentation.
- Risks: Hallucination, weak retrieval, model availability, XSS risk from generated HTML, database failures, and latency.
- Trade-offs: Favor reliability and grounding over broad feature breadth; prefer a smaller set of well-tested skills over a large feature set.

## 3. Mandatory requirements
- Product and growth team use case
- Grounded Q&A using transcript data
- Session-based conversation flow
- PostgreSQL persistence
- FastAPI backend
- Retrieval and embedding pipeline
- LLM abstraction with local/cloud model switching
- Agent layer with routing between skills
- Ship 30 for 30 writing skill
- Artifact generation in Markdown or HTML
- Safe handling of generated HTML as untrusted content
- Frontend experience for chat and artifact viewing
- Automated tests for API, retrieval, routing, and persistence
- Docker-based local startup path
- Observability and failure handling
- Documentation and handoff readiness

## 4. Nice-to-have / optional items
- Streaming responses
- Advanced analytics dashboards
- Authentication and RBAC
- Multi-user tenant separation
- Complex editor UX
- Additional agent skills beyond core requirements
- Custom visual design beyond the MVP

## 5. Evaluation-focused checklist
- Requirements are clearly defined and documented
- Architecture is explicit before implementation
- Data ingestion and indexing are described
- Retrieval is grounded in transcript evidence
- The app handles local/fallback model configuration
- Agent decisions are explainable and constrained
- Artifacts are rendered safely
- Tests cover critical failures and expected flows
- Docker + README make fresh setup reproducible

## 6. Deliverable checklist
- Project/product documentation
- Architecture documentation
- Backend implementation
- Database schema and persistence
- Retrieval and embeddings
- LLM provider configuration
- Agent routing and content generation
- Artifact security strategy
- Frontend UI
- Testing suite
- Deployment and setup instructions
- Agent transcripts / build log

## 7. Final assessment criteria
This project should be judged on:
1. Product clarity and user value
2. Technical architecture discipline
3. Grounding quality and retrieval relevance
4. Agent skill design
5. Security maturity and artifact handling
6. Ease of running in a fresh environment
7. Documentation quality and team handoff readiness
