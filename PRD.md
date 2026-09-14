# LennyLens — Product Requirements Document (PRD)

**Document Status:** Current Implementation Baseline  
**Version:** 1.0.0  
**Author:** Product & Engineering Team  

---

## 1. Product Vision & Goals

### 1.1 Vision Statement
LennyLens is an intelligent, grounded product research workspace. It enables product managers, growth leaders, and founders to synthesize insights from *Lenny’s Podcast* transcripts, generate atomic Ship 30 for 30 essays, and build interactive HTML strategy artifacts with verifiable evidence.

### 1.2 Core Product Goals
- **Eliminate AI Hallucinations:** Provide zero-hallucination answers where every assertion is traceable to specific podcast transcript excerpts.
- **Transform Audio Knowledge into Artifacts:** Convert raw interview transcripts into actionable product deliverables (strategy canvases, comparison tables, timeline briefings).
- **Provide Model Autonomy:** Give teams the choice between running privacy-focused local models (Ollama/Qwen) or high-capacity cloud models (OpenAI, Anthropic, OpenRouter).
- **Delight with Editorial Polish:** Offer a calm, radically minimal reading workspace tailored for high-focus strategic thinking.

---

## 2. Target Persona

### Primary Persona: Product Lead & Growth Builder
- **Role:** Senior Product Manager, VP of Product, Head of Growth, or Founder.
- **Jobs to be Done (JTBD):**
  1. *Discovery vs Execution:* Needs proven frameworks from top product leaders (e.g., Shreyas Doshi, Casey Winters, Elena Verna) when pitching strategy to executives.
  2. *Synthesize Best Practices:* Needs fast comparisons between conflicting advice (e.g., PLG vs sales-led growth).
  3. *Shareable Deliverables:* Needs structured strategy one-pagers and HTML canvases to present in team workshops.
- **Pain Points:** Generic ChatGPT outputs lack verified sources, hallucinate quotes, and produce basic, unformatted text bubbles.

---

## 3. Functional Requirements & User Stories

### 3.1 Grounded Product Question Answering (Q&A)
- **User Story:** *As a PM, I want to ask natural-language questions about product strategy so that I receive concise answers backed by transcript quotes.*
- **Functional Requirements:**
  - System must classify incoming queries and invoke the `QnASkill`.
  - Answers must embed inline citation tags (e.g., `[1]`, `[2]`).
  - Output must include interactive source cards detailing the guest name, episode title, timestamp (when available), and transcript excerpt.
  - Clicking a citation tag `[1]` must smooth-scroll and highlight the corresponding source card.

### 3.2 Ship 30 for 30 Essay Generator
- **User Story:** *As a product writer, I want to request a Ship 30 essay on a product topic so that I get a structured 300-word atomic essay ready for publishing.*
- **Functional Requirements:**
  - Queries containing essay keywords (e.g., `"Ship 30"`, `"write an essay"`) must trigger the `EssaySkill`.
  - System must format the output according to the Ship 30 playbook structure (Hook, Main Body, Actionable Takeaways).
  - An artifact payload (`type: "markdown"`) must be generated and made available in the Artifact Viewer.

### 3.3 Interactive HTML & Markdown Product Artifacts
- **User Story:** *As a growth lead, I want to generate strategy canvases and comparison tables so that I can present formatted documents to stakeholders.*
- **Functional Requirements:**
  - Queries requesting canvases, tables, timelines, or documents trigger `ArtifactSkill`.
  - Supported artifact formats: `html` and `markdown`.
  - Artifact templates supported: Strategy Canvas (HTML), Comparison Table (HTML), Vertical Timeline (HTML), and One-Pager Brief (Markdown).
  - All HTML artifacts must be static HTML documents containing CSS inside `<style>` tags with zero external script or network dependencies.
  - An explicit error (`unsupported_format`) must be returned if the user requests PDF, DOCX, CSV, or JSON.

### 3.4 Runtime Model Switching
- **User Story:** *As a developer/evaluator, I want to switch between local Ollama and cloud LLMs on the fly without restarting services.*
- **Functional Requirements:**
  - System must support Ollama (`qwen3.5:2b` default), OpenAI (`gpt-4o`, `gpt-4o-mini`), Anthropic (`claude-3-5-sonnet`), and OpenRouter.
  - Model selection must update in memory via `PUT /api/v1/runtime` without container restarts or disk persistence.
  - The model discovery endpoint (`POST /api/v1/runtime/models`) must query local Ollama tags or cloud provider model catalogs.

### 3.5 Session & Conversation Management
- **User Story:** *As a researcher, I want my chat history saved so that I can review prior conversations and ask follow-up questions.*
- **Functional Requirements:**
  - Multi-session persistence stored in PostgreSQL (`sessions` and `messages` tables).
  - Conversations expand follow-up questions (e.g., `"compare the two"`) using previous user/assistant context.

---

## 4. Non-Functional Requirements

### 4.1 Groundedness & Claim Validation
- All generated claims must be validated using token-overlap matching against extracted transcript evidence (`GROUNDING_MIN_CONFIDENCE = 0.45`).
- Unsubstantiated claims in model outputs must be stripped or flagged. If model prose fails validation completely, a deterministic fallback evidence artifact is generated directly from retrieved transcript statements.

### 4.2 Security & HTML Sandboxing
- All HTML artifacts must pass through `sanitize_html()` (`bleach` sanitizer) to strip JavaScript (`<script>`), inline event handlers (`onclick`), `<iframe>`, `<form>`, and external image loading.
- HTML artifacts must inject a strict Content Security Policy (`CSP`) meta tag:
  `<meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src 'unsafe-inline';">`.
- In the frontend, HTML artifacts are rendered inside an `<iframe sandbox="" />` container to prevent DOM or script execution.

### 4.3 Performance & Reliability
- **Timeout Protection:** Grounded agent requests are bounded by a 240-second timeout limit.
- **Empty Knowledge Base Handling:** If no transcript chunks exist in the database, retrieval gracefully returns an empty result set rather than throwing a model exception.

---

## 5. Feature Status Matrix

| Feature Module | Current Status | Description |
| :--- | :--- | :--- |
| **Grounded Q&A Engine** | **Implemented** | Natural language queries with inline citations `[1]` and source cards. |
| **Ship 30 Essay Skill** | **Implemented** | Atomic essay generation following the Ship 30 playbook structure. |
| **HTML/Markdown Artifacts** | **Implemented** | Strategy canvases, comparison tables, timelines, and Markdown briefs. |
| **Claim Validation Pipeline** | **Implemented** | Deterministic token-overlap validation & fallback evidence builder. |
| **HTML Security Sanitizer** | **Implemented** | Script stripping, CSP meta injection, and sandboxed `<iframe>` preview. |
| **Hybrid RAG Retrieval** | **Implemented** | `tsvector` lexical + `pgvector` cosine search + concept reranking. |
| **Dynamic Runtime Model Config** | **Implemented** | Switch between local Ollama and Cloud OpenAI/Anthropic in memory. |
| **Session Persistence** | **Implemented** | Full PostgreSQL persistence for sessions and chat history. |
| **Editorial Light UI** | **Implemented** | Custom Chalk design system (`#E5E3D0` background, serif typography). |
| **Multi-User Authentication** | **Planned / Not currently implemented** | Currently defaults to single demo user (`user_id = 1`). |
| **PDF/DOCX Exporting** | **Planned / Not currently implemented** | Format request returns an explicit `unsupported_format` message. |
| **Automated Scraping Pipeline**| **Planned / Not currently implemented** | Transcripts are seeded via `seed_db.py` from static JSON files. |
| **Persistent Key Storage** | **Planned / Not currently implemented** | API keys are held strictly in memory for security. |
