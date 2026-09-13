*

 *

# LennyLens — Complete Implementation Roadmap

> **Project:** LennyLens — AI-Powered Product & Growth Intelligence Assistant  
> **Repository:** `lenny-lens`  
> **Purpose:** Master implementation roadmap from system architecture through final submission.

 *

# Table of Contents

1. Phase 2 — System Architecture
2. Phase 3 — Repository Foundation
3. Phase 4 — FastAPI Backend Foundation
4. Phase 5 — PostgreSQL Database
5. Phase 6 — Session Management
6. Phase 7 — Transcript Ingestion
7. Phase 8 — Chunking
8. Phase 9 — Embeddings
9. Phase 10 — Vector Retrieval
10. Phase 11 — LLM Provider Abstraction
11. Phase 12 — RAG Question Answering
12. Phase 13 — Agent Architecture
13. Phase 14 — Conversational Assistant
14. Phase 15 — Ship 30 for 30 Skill
15. Phase 16 — Artifact Generation
16. Phase 17 — Artifact Security
17. Phase 18 — Frontend
18. Phase 19 — Artifact Viewer
19. Phase 20 — UI/UX Polish
20. Phase 21 — Full Integration
21. Phase 22 — Testing
22. Phase 23 — Observability
23. Phase 24 — Resilience
24. Phase 25 — Docker & Deployment
25. Phase 26 — Data Refresh & Ingestion Automation
26. Phase 27 — Documentation
27. Phase 28 — Agent Development Transcripts
28. Phase 29 — Security Review
29. Phase 30 — Code Quality Review
30. Phase 31 — Evaluation Matrix
31. Phase 32 — Fresh Machine Verification
32. Phase 33 — Demo Preparation
33. Phase 34 — Final Repository Cleanup
34. Phase 35 — Final Submission

 *

# Phase 2 — System Architecture

## Objective

Design the complete technical architecture of LennyLens before implementing major functionality.

The architecture must clearly explain:

*   Frontend
*   Backend
*   Agent layer
*   RAG pipeline
*   Database
*   Vector search
*   LLM providers
*   Transcript ingestion
*   Artifact generation
*   Artifact security
*   Session management
*   API boundaries
*   Deployment topology
*   Failure handling

 *

| Step | Task | Detailed Description | What to Learn | Deliverable | Validation | Git Commit |
| --- | --- | --- | --- | --- | --- | --- |
| 2.1 | Define system requirements | Convert the PRD into technical requirements. Identify every system capability required by LennyLens and map each requirement to a technical component. | Functional vs non-functional requirements, system constraints | `docs/technical-requirements.md` | Every PRD requirement has a technical implementation target | `docs: define technical system requirements` |
| 2.2 | Design high-level architecture | Design the complete flow from user → frontend → FastAPI → agent → skills → RAG → database/LLM → response. | Layered architecture, service boundaries | Architecture diagram | Every major component has a clear responsibility | `docs: add high level system architecture` |
| 2.3 | Define frontend boundary | Decide exactly what belongs to React and what belongs to FastAPI. Frontend should handle presentation/state while backend owns business logic and AI orchestration. | Client/server architecture | Frontend architecture section | No business-critical AI logic is unnecessarily duplicated in frontend | `docs: define frontend architecture boundary` |
| 2.4 | Define backend layers | Establish API, service, agent, retrieval, repository and database boundaries. Avoid putting all logic inside route handlers. | Clean architecture, separation of concerns | Backend architecture | Every backend responsibility belongs to one logical layer | `docs: define backend component boundaries` |
| 2.5 | Define API contracts | Design endpoints, HTTP methods, request schemas, response schemas, status codes and errors before implementation. | REST APIs, HTTP semantics, Pydantic schemas | API specification | Frontend can theoretically be implemented against the contracts | `docs: define initial API contracts` |
| 2.6 | Design database schema | Define users, sessions, messages, transcripts and transcript chunks. Identify primary keys, foreign keys, indexes and relationships. | Relational modeling, normalization, indexes | ER diagram + schema | Relationships and ownership are unambiguous | `docs: define database schema` |
| 2.7 | Design vector storage | Decide how transcript embeddings will be stored and searched using PostgreSQL/vector capabilities. | Embeddings, vector similarity, pgvector concepts | Vector architecture | Retrieval requirements can be implemented without another database | `docs: define vector storage architecture` |
| 2.8 | Design ingestion pipeline | Define transcript → cleaning → metadata extraction → chunking → embedding → indexing. | ETL/ELT, data pipelines, indexing | Ingestion architecture | Pipeline is repeatable and traceable | `docs: define transcript ingestion architecture` |
| 2.9 | Design retrieval pipeline | Define query embedding → similarity search → top-K chunks → optional filtering → context construction. | Semantic search, top-K retrieval, reranking concepts | Retrieval design | Retrieval output contains content + source metadata | `docs: define RAG retrieval pipeline` |
| 2.10 | Design agent routing | Define how the agent determines whether a request is Q&A, essay generation or artifact generation. | Agents, routing, tools, skills | Agent routing diagram | Every supported user intent maps to a skill | `docs: define agent routing architecture` |
| 2.11 | Design skill boundaries | Define separate responsibilities for Q&A, Ship 30 for 30 and artifact generation. | Tool/skill architecture | Skill specifications | Skills are independently testable | `docs: define agent skill boundaries` |
| 2.12 | Design LLM abstraction | Define a common provider interface allowing local Ollama and cloud model providers to be switched through configuration. | Strategy pattern, dependency inversion, LLM abstraction | Provider architecture | Application code does not depend directly on one provider | `docs: define LLM provider abstraction` |
| 2.13 | Design model configuration | Decide environment variables and runtime configuration for selecting the LLM provider/model. | Configuration management | `.env` specification | Switching providers does not require source changes | `docs: define runtime model configuration` |
| 2.14 | Design conversation state | Define what gets stored in sessions and messages and how previous conversation context is loaded. | Stateful applications, conversation memory | Session architecture | Two sessions cannot accidentally share context | `docs: define conversation state architecture` |
| 2.15 | Design artifact pipeline | Define generation → validation → sanitization → storage/transport → sandboxed rendering. | Secure content rendering | Artifact architecture | Generated HTML is treated as untrusted | `docs: define artifact generation architecture` |
| 2.16 | Design security boundary | Identify trust boundaries between user input, LLM output, database and generated HTML. | Threat modeling, XSS, CSP, sandboxing | Security architecture | Every untrusted input/output has a mitigation | `docs: define application security boundaries` |
| 2.17 | Design observability | Define structured logs and diagnostic fields such as request ID, session ID, model, retrieval latency and error type. | Structured logging, observability | Logging specification | Failures can be diagnosed from logs | `docs: define observability architecture` |
| 2.18 | Design failure handling | Document expected behavior when database, Ollama, cloud LLM, retrieval or artifact generation fails. | Fault tolerance, graceful degradation | Failure matrix | Every critical dependency has an explicit failure path | `docs: define system failure handling` |
| 2.19 | Design deployment topology | Define local development and evaluator startup architecture using Docker/Compose where appropriate. | Containers, service orchestration | Deployment diagram | Fresh environment can reproduce the stack | `docs: define deployment topology` |
| 2.20 | Finalize architecture document | Consolidate all architecture decisions into a single professional document. | Technical documentation | `docs/architecture.md` | Architecture is internally consistent | `docs: finalize architecture documentation` |

 *

## Phase 2 Completion Criteria

Phase 2 is complete only when:

- [ ] High-level architecture is documented.
- [ ] Backend boundaries are documented.
- [ ] Frontend boundaries are documented.
- [ ] API contracts are defined.
- [ ] Database schema is defined.
- [ ] RAG pipeline is defined.
- [ ] Ingestion pipeline is defined.
- [ ] Agent routing is defined.
- [ ] Skill boundaries are defined.
- [ ] LLM provider abstraction is defined.
- [ ] Ollama/cloud switching strategy is defined.
- [ ] Artifact security architecture is defined.
- [ ] Failure handling is defined.
- [ ] Observability strategy is defined.
- [ ] Deployment architecture is defined.
- [ ] `docs/architecture.md` is complete.

 *

# Phase 3 — Repository Foundation

## Objective

Create a professional repository structure that supports clean development, testing, deployment and documentation.

 *

| Step | Task | Detailed Description | What to Learn | Deliverable | Validation | Git Commit |
| --- | --- | --- | --- | --- | --- | --- |
| 3.1 | Create repository | Create the `lenny-lens` Git repository and establish the main branch. | Git/GitHub basics | Git repository | Repository is accessible and initialized correctly | `chore: initialize repository` |
| 3.2 | Add `.gitignore` | Prevent secrets, virtual environments, caches, build artifacts and dependencies from being committed. | Git ignore rules | `.gitignore` | Sensitive/generated files are ignored | `chore: add gitignore` |
| 3.3 | Add `.env.example` | Document every required environment variable without exposing real credentials. | Environment configuration | `.env.example` | Fresh developer knows what configuration is needed | `chore: add environment configuration template` |
| 3.4 | Create backend structure | Create API, services, agents, database, models, schemas and core configuration directories. | Python package organization | Backend structure | Imports work correctly | `chore: create backend structure` |
| 3.5 | Create frontend structure | Establish React/TypeScript application structure for components, pages, API client and state. | React architecture | Frontend structure | Frontend builds successfully | `chore: create frontend structure` |
| 3.6 | Create docs structure | Create documentation folders for architecture, design, testing and agent transcripts. | Technical documentation organization | `docs/` | Documentation has predictable locations | `chore: create documentation structure` |
| 3.7 | Add initial README | Explain project purpose, current status and high-level setup. | README design | `README.md` | Someone can understand the project in under 2 minutes | `docs: add initial project README` |
| 3.8 | Configure formatting | Establish consistent Python and frontend formatting/linting. | Code quality tooling | Formatter/linter configuration | Formatting checks pass | `chore: configure code quality tooling` |

 *

# Phase 4 — FastAPI Backend Foundation

## Objective

Build a clean backend foundation before implementing AI functionality.

 *

| Step | Task | Detailed Description | What to Learn | Deliverable | Validation | Git Commit |
| --- | --- | --- | --- | --- | --- | --- |
| 4.1 | Create Python environment | Create and activate a dedicated virtual environment. | Python environments | `.venv` | Python dependencies are isolated | `chore: configure Python development environment` |
| 4.2 | Install dependencies | Install FastAPI, Uvicorn, Pydantic, SQLAlchemy, async database driver, Alembic and testing dependencies. | Python dependency management | Dependency file | Environment installs successfully | `chore: add backend dependencies` |
| 4.3 | Create FastAPI app | Create the application entry point and initialize FastAPI. | FastAPI fundamentals | `main.py` | Server starts successfully | `feat(api): initialize FastAPI application` |
| 4.4 | Add configuration | Build typed application settings using environment variables. | Pydantic Settings | Configuration module | Missing configuration produces useful errors | `feat(config): add typed application settings` |
| 4.5 | Add health endpoint | Implement `/health` to verify the API process is alive. | HTTP health checks | `GET /health` | Returns successful health response | `feat(api): add health endpoint` |
| 4.6 | Add exception handling | Establish centralized handling for validation, application and unexpected errors. | FastAPI exception handling | Error middleware/handlers | Errors have predictable responses | `feat(api): add structured error handling` |
| 4.7 | Add request validation | Define Pydantic request/response models. | Schema validation | API schemas | Invalid requests are rejected cleanly | `feat(api): add request and response validation` |
| 4.8 | Add API tests | Test health, validation and error responses. | pytest, HTTPX | Backend API tests | Tests pass consistently | `test(api): add foundational API tests` |

 *

# Phase 5 — PostgreSQL Database

## Objective

Build reliable relational persistence for users, sessions, messages and transcript data.

 *

| Step | Task | Detailed Description | What to Learn | Deliverable | Validation | Git Commit |
| --- | --- | --- | --- | --- | --- | --- |
| 5.1 | Start PostgreSQL | Run PostgreSQL locally, preferably through Docker. | PostgreSQL basics | Running database | Application can connect | `chore(db): add local PostgreSQL service` |
| 5.2 | Configure SQLAlchemy | Create database engine, session management and base model configuration. | SQLAlchemy | DB layer | Connection succeeds | `feat(db): configure SQLAlchemy database layer` |
| 5.3 | Create user model | Define user identity required by the application. | Relational modeling | User model | Migration can be generated | `feat(db): add user model` |
| 5.4 | Create session model | Store independent conversations. | Foreign keys, relationships | Session model | Sessions are independently identifiable | `feat(db): add chat session model` |
| 5.5 | Create message model | Store user and assistant messages associated with sessions. | One-to-many relationships | Message model | Messages correctly belong to sessions | `feat(db): add conversation message model` |
| 5.6 | Create transcript model | Store transcript-level metadata. | Data modeling | Transcript model | Transcript records can be persisted | `feat(db): add transcript model` |
| 5.7 | Create chunk model | Store transcript chunks and associated metadata. | Search-oriented schema design | Chunk model | Chunks retain traceability | `feat(db): add transcript chunk model` |
| 5.8 | Configure migrations | Configure Alembic. | Database migrations | Alembic configuration | Migration commands work | `chore(db): configure Alembic migrations` |
| 5.9 | Create initial migration | Generate and execute initial schema migration. | Schema versioning | Initial migration | Fresh database can be created | `chore(db): create initial database migration` |
| 5.10 | Test persistence | Verify records survive application restarts. | Persistence testing | DB tests | Persistence tests pass | `test(db): verify database persistence` |

 *

# Phase 6 — Session Management

## Objective

Implement independent conversational sessions so each chat maintains its own history and context.

 *

| Step | Task | Detailed Description | What to Learn | Deliverable | Validation | Git Commit |
| --- | --- | --- | --- | --- | --- | --- |
| 6.1 | Create session service | Centralize session creation and retrieval logic. | Service layer design | Session service | Business logic isn’t inside routes | `feat(session): add session service` |
| 6.2 | Create session endpoint | Add endpoint to create a new conversation. | REST API design | `POST /sessions` | New session is persisted | `feat(session): add chat session creation` |
| 6.3 | List sessions | Allow frontend to retrieve previous sessions. | Pagination/basic querying | `GET /sessions` | Sessions are returned correctly | `feat(session): add session listing` |
| 6.4 | Retrieve history | Return messages belonging to one session. | Relational queries | `GET /sessions/{id}` | Correct history is returned | `feat(session): add session history retrieval` |
| 6.5 | Persist messages | Store every user and assistant message. | Persistence patterns | Message service | Messages survive restart | `feat(session): persist conversation messages` |
| 6.6 | Test isolation | Verify session A cannot retrieve session B’s context. | Authorization boundaries, isolation | Session tests | Isolation tests pass | `test(session): verify session context isolation` |

 *

# Phase 7 — Transcript Ingestion

## Objective

Create a repeatable pipeline that converts the transcript repository into searchable knowledge.

 *

| Step | Task | Detailed Description | What to Learn | Deliverable | Validation | Git Commit |
| --- | --- | --- | --- | --- | --- | --- |
| 7.1 | Identify source format | Understand the transcript source structure, metadata and file formats. | Data inspection | Source documentation | Source structure is documented | `docs(data): document transcript source` |
| 7.2 | Build source loader | Read transcript files into a normalized internal representation. | File processing, parsers | Transcript loader | Multiple transcripts load successfully | `feat(ingestion): add transcript loader` |
| 7.3 | Clean text | Normalize whitespace, encoding, formatting and obvious noise. | Text preprocessing | Cleaning pipeline | Clean output is readable | `feat(ingestion): add transcript cleaning pipeline` |
| 7.4 | Extract metadata | Preserve episode title, source, speaker, timestamp and other useful metadata. | Metadata modeling | Metadata extractor | Metadata remains attached to content | `feat(ingestion): extract transcript metadata` |
| 7.5 | Validate records | Reject malformed or incomplete records rather than silently indexing bad data. | Data validation | Validation layer | Invalid records are reported | `feat(ingestion): add transcript validation` |
| 7.6 | Add ingestion logging | Record files processed, records created and failures. | Pipeline observability | Ingestion logs | Failures are diagnosable | `feat(ingestion): add ingestion progress logging` |

 *

# Phase 8 — Chunking

## Objective

Break long transcripts into retrieval-friendly units while preserving enough context for useful answers.

 *

| Step | Task | Detailed Description | What to Learn | Deliverable | Validation | Git Commit |
| --- | --- | --- | --- | --- | --- | --- |
| 8.1 | Study chunking | Understand why long documents must be divided into smaller retrieval units. | RAG fundamentals | Chunking notes | Design decision is documented | `docs(rag): document transcript chunking strategy` |
| 8.2 | Select chunk size | Choose an initial chunk-size strategy based on semantic completeness and retrieval quality. | Tokenization, context windows | Chunk configuration | Configuration is explicit | `docs(rag): document chunk size decision` |
| 8.3 | Select overlap | Add appropriate overlap where useful so important information isn’t split across boundaries. | Chunk overlap | Chunk configuration | Overlap behavior is tested | `feat(rag): configure chunk overlap strategy` |
| 8.4 | Implement chunker | Convert cleaned transcript text into chunks. | Text splitting | Chunker | Transcripts produce expected chunks | `feat(rag): implement transcript chunking` |
| 8.5 | Preserve metadata | Attach source information to every chunk. | Data lineage | Chunk metadata | Every chunk can be traced to source | `feat(rag): preserve source metadata during chunking` |
| 8.6 | Test chunking | Test short text, long text, empty text and boundary cases. | Unit testing | Chunking tests | Edge cases pass | `test(rag): add transcript chunking tests` |

 *

# Phase 9 — Embeddings

## Objective

Convert transcript chunks and user queries into vector representations that capture semantic meaning.

 *

| Step | Task | Detailed Description | What to Learn | Deliverable | Validation | Git Commit |
| --- | --- | --- | --- | --- | --- | --- |
| 9.1 | Learn embeddings | Understand how text is transformed into numerical vectors and why semantic similarity works. | Embeddings, vector spaces | Learning notes | Can explain embeddings clearly | `docs(rag): document embedding fundamentals` |
| 9.2 | Select embedding model | Choose an embedding model appropriate for local development and the assignment. | Embedding model trade-offs | Model decision | Choice is documented | `docs(rag): document embedding model decision` |
| 9.3 | Build embedding interface | Abstract embedding generation behind a clean interface. | Dependency inversion | Embedding provider | Application isn’t tightly coupled | `feat(rag): define embedding provider interface` |
| 9.4 | Generate embeddings | Generate vectors for transcript chunks. | Batch processing | Embedding pipeline | Embeddings are generated successfully | `feat(rag): add transcript embedding generation` |
| 9.5 | Validate vectors | Verify dimensionality and successful storage preparation. | Vector validation | Validation tests | Invalid vectors are rejected | `test(rag): validate embedding generation` |

 *

# Phase 10 — Vector Retrieval

## Objective

Build semantic search over the transcript knowledge base.

 *

| Step | Task | Detailed Description | What to Learn | Deliverable | Validation | Git Commit |
| --- | --- | --- | --- | --- | --- | --- |
| 10.1 | Enable vector support | Configure PostgreSQL vector functionality. | pgvector concepts | DB vector support | Database supports vector fields | `feat(db): enable vector storage` |
| 10.2 | Store embeddings | Persist transcript chunk vectors. | Vector storage | Vectorized chunks | Embeddings survive restart | `feat(rag): persist transcript embeddings` |
| 10.3 | Embed user query | Convert user questions into the same embedding space. | Query embeddings | Query embedding service | Query vectors are generated | `feat(rag): add query embedding generation` |
| 10.4 | Implement similarity search | Retrieve chunks based on semantic similarity. | Cosine/distance similarity | Retrieval service | Relevant chunks appear for known questions | `feat(rag): implement semantic similarity retrieval` |
| 10.5 | Add top-K retrieval | Control how many candidate chunks are returned. | Top-K search | Configurable retrieval | K is configurable | `feat(rag): add configurable top-k retrieval` |
| 10.6 | Add metadata filters | Support filtering by available transcript metadata where useful. | Hybrid retrieval concepts | Filter support | Filters behave correctly | `feat(rag): add transcript metadata filtering` |
| 10.7 | Return source metadata | Retrieval results must include source information for grounding/citations. | Data lineage | Retrieval result schema | Every result has traceable source | `feat(rag): expose transcript source metadata` |
| 10.8 | Add retrieval scores | Preserve relevance/similarity information for debugging and evaluation. | Retrieval evaluation | Relevance scores | Scores are available | `feat(rag): expose retrieval relevance scores` |
| 10.9 | Test retrieval | Build questions with known relevant transcripts and verify results. | Information retrieval evaluation | Retrieval tests | Retrieval tests pass | `test(rag): add retrieval relevance tests` |

 *

# Phase 11 — LLM Provider Abstraction

## Objective

Allow LennyLens to run using local Ollama and a cloud LLM provider without changing business logic.

 *

| Step | Task | Detailed Description | What to Learn | Deliverable | Validation | Git Commit |
| --- | --- | --- | --- | --- | --- | --- |
| 11.1 | Study provider abstraction | Understand why application logic should depend on an interface instead of one LLM SDK. | Strategy pattern, dependency inversion | Design notes | Can explain the abstraction | `docs(llm): document provider abstraction strategy` |
| 11.2 | Define provider interface | Create a common contract for generation, streaming and model metadata where needed. | Interfaces/protocols | `LLMProvider` | Providers implement same contract | `feat(llm): define LLM provider interface` |
| 11.3 | Implement Ollama provider | Connect to local Ollama. | Ollama API, HTTP clients | Ollama provider | Local model generates response | `feat(llm): add Ollama provider` |
| 11.4 | Test Ollama | Test successful generation and connection failure. | Integration testing | Ollama tests | Provider tests pass | `test(llm): add Ollama provider tests` |
| 11.5 | Implement cloud provider | Add one cloud provider using the same interface. | Cloud LLM API | Cloud provider | Cloud generation works | `feat(llm): add cloud LLM provider` |
| 11.6 | Implement provider factory | Select implementation from configuration. | Factory pattern | Provider factory | Correct provider is selected | `feat(llm): add configurable provider factory` |
| 11.7 | Add model configuration | Configure provider/model through environment variables. | Configuration | LLM settings | Switching provider requires no code modification | `feat(llm): add runtime model configuration` |
| 11.8 | Handle unavailable providers | Return useful errors if the selected provider cannot be reached. | Resilience | Error handling | Application doesn’t crash unexpectedly | `fix(llm): handle unavailable model providers` |

 *

# Phase 12 — RAG Question Answering

## Objective

Combine retrieval and LLM generation into a grounded product/growth question-answering system.

 *

| Step | Task | Detailed Description | What to Learn | Deliverable | Validation | Git Commit |
| --- | --- | --- | --- | --- | --- | --- |
| 12.1 | Create RAG service | Combine query embedding, retrieval, context construction and LLM generation. | End-to-end RAG | RAG service | Question produces grounded answer | `feat(rag): create grounded question answering service` |
| 12.2 | Build context formatter | Convert retrieved chunks into structured context for the LLM. | Prompt context construction | Context builder | Context contains source metadata | `feat(rag): add retrieved context builder` |
| 12.3 | Create grounding prompt | Instruct model to answer using supplied transcript evidence and acknowledge insufficient evidence. | Prompt engineering | Grounding prompt | Unsupported questions aren’t invented | `feat(rag): add transcript grounding instructions` |
| 12.4 | Generate grounded answer | Send prompt + retrieved evidence to the selected LLM. | LLM orchestration | Answer service | Answers use retrieved evidence | `feat(rag): implement grounded answer generation` |
| 12.5 | Add source citations | Return source information alongside the answer. | Citation design | Source response schema | User can understand where answer came from | `feat(rag): attach transcript sources to answers` |
| 12.6 | Handle empty retrieval | Avoid generating unsupported answers when no useful evidence is retrieved. | RAG failure modes | Empty retrieval handling | Model responds appropriately | `feat(rag): handle unsupported questions gracefully` |
| 12.7 | Test hallucination boundary | Ask questions unsupported by the transcript corpus. | Grounding evaluation | Tests | System acknowledges insufficient evidence | `test(rag): verify unsupported questions are not hallucinated` |

 *

# Phase 13 — Agent Architecture

## Objective

Introduce the required agent layer and make it responsible for routing user requests to specialized skills.

 *

| Step | Task | Detailed Description | What to Learn | Deliverable | Validation | Git Commit |
| --- | --- | --- | --- | --- | --- | --- |
| 13.1 | Learn agent architecture | Understand agents, tools, skills, routing, context and execution loops. | Agentic AI fundamentals | Learning notes | Can explain why an agent is useful here | `docs(agent): document agent architecture fundamentals` |
| 13.2 | Select agent framework | Use the framework permitted by the assignment. | Agent SDK concepts | Framework decision | Decision documented | `docs(agent): document agent framework decision` |
| 13.3 | Integrate framework | Add framework without coupling the rest of the application to framework-specific internals. | SDK integration | Agent module | Application starts successfully | `feat(agent): integrate agent framework` |
| 13.4 | Create router | Route user requests to appropriate skills. | Intent classification/routing | Agent router | Known intents route correctly | `feat(agent): add request routing` |
| 13.5 | Create Q&A skill | Connect Q&A intent to grounded RAG service. | Agent skill design | Q&A skill | Q&A uses RAG | `feat(agent): add grounded Q&A skill` |
| 13.6 | Create error handling | Handle invalid routing, unavailable tools and execution failures. | Agent resilience | Error strategy | Failures become useful responses | `feat(agent): add agent failure handling` |
| 13.7 | Test routing | Verify questions, essay requests and artifact requests route correctly. | Agent testing | Routing tests | All expected routes pass | `test(agent): verify skill routing behavior` |

 *

# Phase 14 — Conversational Assistant

## Objective

Expose the agent/RAG system through a complete conversational backend.

 *

| Step | Task | Detailed Description | What to Learn | Deliverable | Validation | Git Commit |
| --- | --- | --- | --- | --- | --- | --- |
| 14.1 | Create chat endpoint | Add the primary conversational endpoint. | REST API | `POST /chat` | Request produces response | `feat(chat): add chat API endpoint` |
| 14.2 | Load session context | Retrieve relevant previous messages for the active session. | Conversation context | Context loader | Follow-up questions understand previous conversation | `feat(chat): add session context loading` |
| 14.3 | Execute agent | Send current request and session context into agent routing. | Agent orchestration | Chat orchestration | Correct skill executes | `feat(chat): connect chat endpoint to agent` |
| 14.4 | Persist user message | Store incoming user message before/around processing. | Transaction design | Message persistence | User message appears in history | `feat(chat): persist user messages` |
| 14.5 | Persist assistant response | Store generated response and useful metadata. | Persistence | Assistant message persistence | Response appears after reload | `feat(chat): persist assistant responses` |
| 14.6 | Add streaming | Stream generated output where supported. | Streaming HTTP/SSE | Streaming endpoint | UI can receive incremental output | `feat(chat): add streaming assistant responses` |
| 14.7 | Test conversation flow | Verify complete request → agent → RAG → response → persistence flow. | E2E testing | Chat E2E tests | End-to-end tests pass | `test(chat): add end to end conversation tests` |

 *

# Phase 15 — Ship 30 for 30 Skill

## Objective

Build a dedicated content-generation skill based on the required writing principles and grounded in transcript evidence.

 *

| Step | Task | Detailed Description | What to Learn | Deliverable | Validation | Git Commit |
| --- | --- | --- | --- | --- | --- | --- |
| 15.1 | Study writing principles | Extract the required principles for hooks, narrative progression, formatting and useful takeaways. | Content structure | Writing notes | Principles are documented | `docs(agent): document Ship 30 for 30 writing principles` |
| 15.2 | Define essay structure | Establish a consistent schema for title, hook, introduction, sections, takeaway and sources. | Structured generation | Essay schema | Schema validates generated content | `feat(essay): define essay output structure` |
| 15.3 | Build skill prompt | Create a dedicated skill prompt with explicit structure and quality requirements. | Prompt engineering | Skill prompt | Prompt produces consistent structure | `feat(agent): add Ship 30 for 30 content skill` |
| 15.4 | Add target length | Aim for approximately 1,250 words while allowing natural variation. | LLM output control | Length validation | Output is within acceptable range | `feat(essay): enforce target essay length` |
| 15.5 | Ground essay | Ensure claims and insights originate from retrieved transcript evidence. | Grounded generation | Source-aware essay | Sources are attached | `feat(essay): ground generated essays in transcript sources` |
| 15.6 | Test essay quality | Check hook, structure, narrative, takeaway, length and source grounding. | LLM evaluation | Essay tests | Acceptance criteria pass | `test(essay): add Ship 30 for 30 generation tests` |

 *

# Phase 16 — Artifact Generation

## Objective

Allow LennyLens to generate useful Markdown and complete HTML/CSS artifacts from user requests.

 *

| Step | Task | Detailed Description | What to Learn | Deliverable | Validation | Git Commit |
| --- | --- | --- | --- | --- | --- | --- |
| 16.1 | Define artifact types | Define supported artifact formats and their intended use. | Content schemas | Artifact specification | Types are explicit | `feat(artifact): define supported artifact types` |
| 16.2 | Define artifact schema | Represent artifact type, title, content, metadata and sources consistently. | Typed schemas | Artifact model | Schema validation works | `feat(artifact): add artifact data model` |
| 16.3 | Create artifact skill | Add a dedicated agent skill for artifact generation. | Agent tools/skills | Artifact skill | Artifact intent routes correctly | `feat(agent): add artifact generation skill` |
| 16.4 | Generate Markdown | Produce structured Markdown artifacts. | Markdown formatting | Markdown generator | Valid Markdown is produced | `feat(artifact): add Markdown artifact generation` |
| 16.5 | Generate HTML/CSS | Produce complete standalone HTML/CSS when requested. | HTML/CSS generation | HTML generator | Browser can render artifact | `feat(artifact): add HTML and CSS artifact generation` |
| 16.6 | Add artifact endpoint | Expose artifact generation through backend API. | API design | Artifact API | Frontend can call endpoint | `feat(api): add artifact generation endpoint` |
| 16.7 | Add source metadata | Preserve evidence/source information where applicable. | Traceability | Artifact metadata | User can identify supporting sources | `feat(artifact): attach source metadata to artifacts` |

 *

# Phase 17 — Artifact Security

## Objective

Treat all generated HTML as **untrusted content** and prevent generated artifacts from executing arbitrary scripts or escaping their intended rendering boundary.

 *

| Step | Task | Detailed Description | What to Learn | Deliverable | Validation | Git Commit |
| --- | --- | --- | --- | --- | --- | --- |
| 17.1 | Study XSS | Understand stored, reflected and DOM-based XSS and why generated HTML is dangerous. | Web security, XSS | Security notes | Can explain attack vectors | `docs(security): document XSS threat model` |
| 17.2 | Define HTML policy | Specify allowed tags, attributes, URL schemes and blocked content. | HTML sanitization | Security policy | Policy is explicit | `docs(security): define artifact HTML policy` |
| 17.3 | Sanitize HTML | Remove dangerous scripts, event handlers and unsafe URLs. | Sanitization libraries | Sanitizer | Malicious payloads are neutralized | `feat(security): sanitize generated HTML artifacts` |
| 17.4 | Sandbox rendering | Render HTML inside an appropriately restricted iframe/sandbox boundary. | Browser sandboxing | Secure artifact renderer | Artifact cannot freely access parent application | `feat(security): sandbox artifact rendering` |
| 17.5 | Configure CSP | Add appropriate Content Security Policy controls where applicable. | CSP | Security headers/policy | Dangerous execution paths are restricted | `feat(security): add artifact content security policy` |
| 17.6 | Add XSS tests | Test scripts, event handlers, dangerous URLs and malformed HTML. | Security testing | Security test suite | Malicious content cannot execute through intended viewer | `test(security): add artifact XSS protection tests` |

 *

# Phase 18 — Frontend

## Objective

Build a polished React/TypeScript interface around sessions, chat, sources and artifacts.

 *

| Step | Task | Detailed Description | What to Learn | Deliverable | Validation | Git Commit |
| --- | --- | --- | --- | --- | --- | --- |
| 18.1 | Initialize React | Create frontend application using React + TypeScript. | React fundamentals | Frontend app | Development server starts | `feat(frontend): initialize React application` |
| 18.2 | Configure API client | Centralize communication with FastAPI. | HTTP clients, API abstraction | API client | Requests reach backend | `feat(frontend): add backend API client` |
| 18.3 | Create layout | Establish sidebar + chat + artifact panel structure. | UI architecture | Main layout | Layout works at desktop width | `feat(ui): add main application layout` |
| 18.4 | Build session sidebar | Display previous conversations and allow selection. | React state | Session sidebar | Sessions load from API | `feat(ui): add conversation session sidebar` |
| 18.5 | Add new chat | Allow users to start a fresh session. | UI interactions | New chat flow | New session opens correctly | `feat(ui): add new conversation flow` |
| 18.6 | Build messages | Render user and assistant messages distinctly. | Component architecture | Message components | Messages render correctly | `feat(ui): add chat message components` |
| 18.7 | Build input | Create message composer with submit/loading behavior. | Forms, controlled components | Chat input | Messages can be submitted | `feat(ui): add chat input component` |
| 18.8 | Connect chat API | Send messages and receive assistant responses. | Async frontend state | Working chat | Full conversation works | `feat(ui): connect frontend to chat API` |
| 18.9 | Add loading states | Display useful progress while assistant is working. | UX states | Loading UI | User receives immediate feedback | `feat(ui): add assistant loading state` |
| 18.10 | Add streaming | Display streaming responses incrementally. | SSE/streaming | Streaming UI | Partial response appears progressively | `feat(ui): render streaming assistant responses` |
| 18.11 | Render Markdown | Render assistant Markdown cleanly. | Markdown rendering | Markdown renderer | Formatting is readable | `feat(ui): add Markdown message rendering` |
| 18.12 | Render sources | Show supporting transcript/source information. | Source UX | Citation component | Sources are understandable | `feat(ui): add transcript source citations` |

 *

# Phase 19 — Artifact Viewer

## Objective

Render generated artifacts beside the chat instead of exposing raw generated code.

 *

| Step | Task | Detailed Description | What to Learn | Deliverable | Validation | Git Commit |
| --- | --- | --- | --- | --- | --- | --- |
| 19.1 | Create artifact panel | Build a dedicated panel beside the conversation. | Responsive UI layouts | Artifact panel | Panel can open/close | `feat(ui): add artifact viewer panel` |
| 19.2 | Render Markdown | Display Markdown artifacts as formatted documents. | Markdown rendering | Markdown artifact view | Artifact is readable | `feat(ui): render Markdown artifacts` |
| 19.3 | Render HTML | Render sanitized/sandboxed HTML artifact output. | Secure rendering | HTML artifact viewer | Artifact renders safely | `feat(ui): render HTML artifacts` |
| 19.4 | Connect generation | Connect viewer to backend artifact endpoint. | Async workflows | End-to-end artifact flow | Generated artifact appears automatically | `feat(ui): connect artifact generation workflow` |
| 19.5 | Add states | Support generating, success, empty and error states. | State machines/UX states | Artifact states | All states are understandable | `feat(ui): add artifact viewer interaction states` |
| 19.6 | Add refresh/regenerate | Allow users to regenerate an artifact when appropriate. | UI action design | Regeneration flow | Regeneration works without breaking session | `feat(ui): add artifact regeneration flow` |

 *

# Phase 20 — UI/UX Polish

## Objective

Move from a functional interface to a professional, evaluator-ready product experience.

 *

| Step | Task | Detailed Description | What to Learn | Deliverable | Validation | Git Commit |
| --- | --- | --- | --- | --- | --- | --- |
| 20.1 | Responsive layout | Ensure layout works on desktop, tablet and narrower screens. | Responsive CSS | Responsive UI | No major layout breakage | `feat(ui): make application responsive` |
| 20.2 | Empty states | Explain what users can do when no conversation/artifact exists. | UX writing | Empty state components | New users understand next action | `feat(ui): add chat empty state` |
| 20.3 | Error states | Turn technical failures into useful user-facing messages. | Error UX | Error components | Users understand recovery action | `feat(ui): add user friendly error states` |
| 20.4 | Loading states | Provide clear feedback during retrieval and generation. | Perceived performance | Loading components | UI never appears frozen | `feat(ui): improve loading experience` |
| 20.5 | Accessibility | Keyboard navigation, labels, focus states, semantic HTML and readable contrast. | WCAG/accessibility | Accessibility improvements | Keyboard-only flow works | `feat(ui): improve accessibility` |
| 20.6 | Visual consistency | Standardize spacing, typography, controls and component states. | Design systems | UI design system | Interface feels cohesive | `refactor(ui): standardize visual design system` |
| 20.7 | UX review | Walk through primary user journeys and eliminate confusing interactions. | UX evaluation | UX review notes | Critical journey has no obvious friction | `docs(ui): document UX review findings` |

 *

# Phase 21 — Full Integration

## Objective

Connect every major subsystem into one complete product workflow.

 *

| Step | Task | Detailed Description | Validation | Git Commit |
| --- | --- | --- | --- | --- |
| 21.1 | Connect grounded Q&A | Frontend → API → Agent → RAG → LLM → response → persistence → UI. | Ask real transcript-based questions | `feat(integration): connect grounded Q&A end to end` |
| 21.2 | Connect essay generation | User request → agent → Ship30 skill → RAG → essay → sources → UI. | Generate a complete essay | `feat(integration): connect Ship 30 for 30 workflow` |
| 21.3 | Connect artifact generation | User request → artifact skill → generation → security → viewer. | Generate and render artifact | `feat(integration): connect artifact generation end to end` |
| 21.4 | Verify session persistence | Reload application and verify conversations remain available. | History survives restart | `feat(integration): persist complete conversation lifecycle` |
| 21.5 | Verify model switching | Run same application with Ollama and cloud provider. | No application-code changes required | `test(integration): verify runtime model switching` |

 *

# Phase 22 — Testing

## Objective

Build meaningful automated coverage for the application’s critical behavior.

 *

| Step | Task | Detailed Description | What to Learn | Deliverable | Git Commit |
| --- | --- | --- | --- | --- | --- |
| 22.1 | Unit tests | Test chunking, schemas, prompts, configuration and utility functions. | Unit testing | Unit suite | `test: add core unit test coverage` |
| 22.2 | API tests | Test health, sessions, chat and artifact endpoints. | API integration testing | API test suite | `test(api): add API integration tests` |
| 22.3 | Retrieval tests | Test semantic retrieval using known questions and expected relevant sources. | Retrieval evaluation | Retrieval suite | `test(rag): expand retrieval evaluation tests` |
| 22.4 | Routing tests | Verify each request type reaches correct skill. | Agent testing | Routing suite | `test(agent): verify skill routing behavior` |
| 22.5 | Persistence tests | Verify sessions and messages persist correctly. | DB integration testing | Persistence suite | `test(db): verify session and message persistence` |
| 22.6 | Security tests | Verify generated HTML cannot execute dangerous payloads. | Security testing | XSS suite | `test(security): expand artifact security tests` |
| 22.7 | Failure tests | Simulate unavailable Ollama, DB failure, timeouts and empty retrieval. | Fault injection | Failure suite | `test: add critical failure scenario coverage` |
| 22.8 | Manual UI test plan | Document exact manual scenarios for the evaluator. | QA test planning | `docs/manual-test-plan.md` | `docs: add manual UI test plan` |
| 22.9 | Run complete test suite | Ensure all automated tests pass from a clean environment. | CI/testing discipline | Passing test suite | `test: verify complete automated test suite` |

 *

# Phase 23 — Observability

## Objective

Make production-like failures diagnosable rather than mysterious.

 *

| Step | Task | Detailed Description | Git Commit |
| --- | --- | --- | --- |
| 23.1 | Structured logging | Use consistent machine-readable log records. | `feat(observability): add structured application logging` |
| 23.2 | Request IDs | Assign a correlation ID to requests for tracing. | `feat(observability): add request correlation IDs` |
| 23.3 | Retrieval metrics | Record retrieval duration, top-K and result count. | `feat(observability): instrument retrieval diagnostics` |
| 23.4 | LLM metrics | Record provider, model, duration and failure type without logging secrets. | `feat(observability): instrument model diagnostics` |
| 23.5 | Database diagnostics | Record meaningful DB failures and latency where appropriate. | `feat(observability): add database diagnostics` |
| 23.6 | Artifact diagnostics | Log artifact generation/rendering failures. | `feat(observability): add artifact diagnostics` |
| 23.7 | Health checks | Expand health information to identify dependency failures. | `feat(observability): expand service health checks` |

 *

# Phase 24 — Resilience

## Objective

Ensure failures become controlled application states instead of crashes or confusing behavior.

 *

| Scenario | Expected Behavior | Git Commit |
| --- | --- | --- |
| Missing API key | Explain configuration issue clearly. | `fix(config): handle missing LLM credentials gracefully` |
| Ollama unavailable | Return useful error or configured fallback. | `fix(llm): handle Ollama connection failures gracefully` |
| Cloud provider unavailable | Return controlled error. | `fix(llm): handle cloud provider failures gracefully` |
| Model timeout | Stop waiting after configured timeout and report failure. | `fix(llm): add model timeout handling` |
| Database unavailable | API returns controlled service error. | `fix(db): handle database connection failures` |
| Empty retrieval | Avoid unsupported answer generation. | `fix(rag): improve empty retrieval behavior` |
| Malformed artifact | Reject or safely display failure. | `fix(artifact): handle malformed artifact output` |
| Invalid user request | Return validation error. | `fix(api): improve invalid request handling` |
| Agent routing failure | Fall back to a safe response. | `fix(agent): improve routing failure handling` |

 *

# Phase 25 — Docker & Deployment

## Objective

Make LennyLens reproducible and easy to start from a fresh environment.

 *

| Step | Task | Detailed Description | Validation | Git Commit |
| --- | --- | --- | --- | --- |
| 25.1 | Backend Dockerfile | Containerize FastAPI backend. | Image builds and server starts | `chore(docker): containerize backend` |
| 25.2 | Frontend Dockerfile | Containerize frontend production build. | Frontend image serves correctly | `chore(docker): containerize frontend` |
| 25.3 | PostgreSQL service | Add PostgreSQL to Compose. | DB starts automatically | `chore(docker): add PostgreSQL compose service` |
| 25.4 | Ollama workflow | Document/configure practical local Ollama execution. | Local model can be used | `chore(docker): configure local Ollama workflow` |
| 25.5 | Compose stack | Connect frontend, backend and database. | `docker compose up` works | `chore(docker): add complete local development stack` |
| 25.6 | Health checks | Add service health checks and dependency startup conditions. | Unhealthy services are detectable | `chore(docker): add container health checks` |
| 25.7 | Clean startup test | Test from a fresh clone/environment. | Complete stack starts without manual hidden steps | `test(docker): verify clean environment startup` |

 *

# Phase 26 — Data Refresh & Ingestion Automation

## Objective

Make the knowledge base maintainable rather than a one-time manually created dataset.

 *

| Step | Task | Detailed Description | Git Commit |
| --- | --- | --- | --- |
| 26.1 | Create ingestion command | Provide a documented command to process transcripts. | `feat(ingestion): add transcript ingestion command` |
| 26.2 | Make ingestion idempotent | Re-running ingestion should not blindly duplicate existing data. | `feat(ingestion): make transcript ingestion idempotent` |
| 26.3 | Track source identity | Use stable identifiers to determine whether content is new/changed. | `feat(ingestion): add transcript source identity tracking` |
| 26.4 | Add refresh mechanism | Provide a repeatable workflow for updating the knowledge base. | `feat(ingestion): add transcript refresh workflow` |
| 26.5 | Log ingestion results | Report processed, skipped, updated and failed records. | `feat(ingestion): improve ingestion result reporting` |
| 26.6 | Document refresh process | Explain how an evaluator/developer can rebuild or update the index. | `docs: document transcript refresh workflow` |

 *

# Phase 27 — Documentation

## Objective

Create documentation good enough for another developer to understand, run and modify LennyLens without personal assistance.

 *

| Document | Required Content | Git Commit |
| --- | --- | --- |
| `README.md` | Project purpose, architecture overview, prerequisites, installation, configuration, startup and usage. | `docs(readme): document project setup and usage` |
| `docs/architecture.md` | Components, database, APIs, ingestion, retrieval, agent routing, models, security and deployment. | `docs: finalize architecture documentation` |
| `docs/design.md` | UI/UX decisions, layout, states, accessibility and responsive behavior. | `docs: add UI UX design document` |
| `docs/manual-test-plan.md` | Step-by-step UI acceptance scenarios. | `docs: add manual UI test plan` |
| `.env.example` | All required environment variables without secrets. | `chore: finalize environment configuration template` |
| Troubleshooting | Common startup, DB, Ollama and configuration failures. | `docs(readme): add troubleshooting guide` |
| API documentation | Endpoint purpose, request/response examples and errors. | `docs(readme): document API usage` |
| Model configuration | How to switch between local and cloud models. | `docs(readme): document LLM configuration` |

 *

# Phase 28 — Agent Development Transcripts

## Objective

Preserve useful evidence of the agent-assisted development process.

The transcripts should demonstrate:

*   Real development reasoning
*   Problems encountered
*   Failed attempts
*   Corrections
*   Technical decisions
*   Final results

Do not manufacture failures that did not happen.

 *

| Step | Task | Description | Git Commit |
| --- | --- | --- | --- |
| 28.1 | Create transcript directory | Add `agent-transcripts/`. | `docs(agent): add coding agent transcript directory` |
| 28.2 | Capture architecture work | Preserve meaningful architecture-related agent interactions. | `docs(agent): add architecture development transcript` |
| 28.3 | Capture backend work | Preserve important backend implementation interactions. | `docs(agent): add backend development transcript` |
| 28.4 | Capture RAG work | Preserve retrieval/chunking/embedding development process. | `docs(agent): add RAG development transcript` |
| 28.5 | Capture agent work | Preserve routing and skill development. | `docs(agent): add agent development transcript` |
| 28.6 | Capture frontend work | Preserve important UI implementation decisions. | `docs(agent): add frontend development transcript` |
| 28.7 | Capture security work | Preserve security testing and corrections. | `docs(agent): add security development transcript` |
| 28.8 | Finalize transcripts | Ensure useful failures and corrections are included without exposing secrets. | `docs(agent): finalize development transcripts` |

 *

# Phase 29 — Security Review

## Objective

Perform a complete pre-submission security audit.

 *

| Check | What to Verify | Result |
| --- | --- | --- |
| Secrets | No API keys, tokens or passwords committed. | \[ \] |
| `.env` | Real `.env` is ignored by Git. | \[ \] |
| API validation | User inputs are validated. | \[ \] |
| SQL safety | Database operations don’t construct unsafe SQL. | \[ \] |
| HTML security | Generated HTML is treated as untrusted. | \[ \] |
| XSS | Dangerous scripts/event handlers are blocked. | \[ \] |
| Sandbox | HTML rendering is isolated. | \[ \] |
| CSP | Appropriate browser restrictions are applied where applicable. | \[ \] |
| Logs | Secrets aren’t written to logs. | \[ \] |
| Dependencies | Unnecessary dependencies removed. | \[ \] |
| Error messages | Errors don’t expose sensitive implementation details. | \[ \] |

### Commit

```
security: complete pre-submission security review
```