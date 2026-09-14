# Agent transcripts

The assignment asks for coding-agent logs, including failed attempts, with secrets removed.

This folder records how the product was directed and corrected. Full Cursor JSONL dumps are not copied here because they can contain environment paths and tool payloads; the notes below are the sanitized handoff.

## 2026-09-13 — Recruiter-grade citations, artifacts, and answers

### What we tried
- First implementation stored artifacts as JSON strings in `messages.content` and detected them with `startsWith('{')`. Essays stayed in the chat bubble. Citations were appended as a relevance-score dump.
- Chunk `start_time` was a character offset (`i * 750`). Using that as a YouTube timestamp would have been dishonest.

### What failed
- Local models truncated long essays because `num_predict` was 2200.
- `test_qna_pipeline` asserted an outdated source dict and would fail after the citation contract change.
- `test_session_isolation` was an empty stub.
- An unused ExternalLink control in the artifact viewer did nothing.
- Claude Agent SDK / Pi were considered and rejected: they are coding-agent runtimes, not a retrieval assistant.

### What we corrected
- First-class `messages.artifact` JSON plus human `content`.
- Ship 30 output opens as a markdown artifact.
- Citations: numbered `[n]`, guest, excerpt, timestamp only when parsed from the transcript, unused sources dropped.
- Retrieval diversity (max two chunks per episode).
- Viewer: Preview/Source, copy, download, pop-out, sandboxed iframe + CSP.
- Sidebar runtime badge, starter chips, skill-aware loading.
- Isolation, citation, and artifact tests.

### How to extend
Add a skill next to `QnASkill` / `EssaySkill` / `ArtifactSkill` and a clause in `classify_intent`. Do not introduce a general filesystem agent.
