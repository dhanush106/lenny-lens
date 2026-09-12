# Phase 0: Evaluation Matrix

## 1. Requirement -> Evidence mapping

| Requirement area | What must be shown | Likely evidence location |
| --- | --- | --- |
| Problem framing | User need and role clarity | docs/requirements.md |
| Product direction | Primary/secondary users, scope, success metrics | docs/requirements.md |
| Architecture | Components, boundaries, database, model flow | docs/architecture.md |
| Data source | Transcript ingestion and metadata handling | ingestion/ and docs/ |
| Retrieval | Embeddings, chunking, similarity search | backend/app/services/ |
| Grounded chat | Evidence-backed answers with citations | backend/app/agents/ |
| Agent skills | Q&A, content, artifact routing | backend/app/agents/ |
| Artifact output | Markdown/HTML generation | backend/app/services/ |
| Security | Sanitization, sandbox, XSS tests | backend/app/security/ |
| UX | Chat UI and artifact viewer | frontend/ |
| Persistence | Session/message/transcript storage | backend/app/db/ |
| Deployment | Docker and environment config | docker-compose.yml, .env.example |
| Testing | API/retrieval/routing/persistence checks | backend/tests/ |
| Handoff | README, architecture docs, troubleshooting | README.md, docs/ |

## 2. Mandatory validation rubric

### Product & problem fit
- Does the app solve an actual information retrieval problem for product/growth teams?
- Are the user jobs clearly supported?
- Is the product grounded in transcript evidence rather than generic chat?

### Technical rigor
- Is the system layered cleanly?
- Are database, retrieval, LLM, and agent components separated?
- Is the LLM provider configurable without code changes?

### Quality of outputs
- Are answers grounded in transcript sources?
- Does the Ship 30 skill produce structured, narrative, skimmable writing?
- Does artifact generation create presentable outputs?

### Security posture
- Are generated HTML artifacts treated as untrusted?
- Is sanitization or sandboxing applied before rendering?
- Are malicious payloads blocked in tests?

### Operability
- Can a fresh environment run the app using documented steps?
- Are missing keys, DB issues, and model outages handled gracefully?
- Is the app observable through logs and health checks?

## 3. Evidence to collect during build
- README setup steps and prerequisites
- Architecture document with component boundaries
- Screenshot or demo of chat + source citations
- Screenshot or demo of artifact viewer
- Test output for API and retrieval flows
- Docker startup command results
- Security testing evidence for HTML sanitization

## 4. Success threshold
The project should be considered ready when each required area has both implementation evidence and a corresponding validation path.
