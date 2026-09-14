# Manual test plan

Run `docker compose up --build`, then work through the following checks.

1. Open `http://localhost`. Confirm the sidebar shows the active provider and model, and the empty chat offers three starter chips.
2. Start two chats, add a message to each via New Chat, and switch between them. Histories must stay separate.
3. After ingesting transcripts, ask a product question. Confirm inline `[n]` chips, source cards with excerpts, and a guest/episode label. Click a source. Ask an unsupported question and confirm it declines.
4. Ask a short follow-up such as “compare those two approaches.” The answer should still cite transcripts.
5. Request a Ship 30 essay. Confirm it opens in the artifact pane as Markdown, with headings and a Sources section—not a raw JSON blob in chat.
6. Request an HTML strategy canvas, including a prompt that mentions `<script>alert(1)</script>`. Confirm Preview renders, Source shows markup, and no script runs. Copy/download/pop-out work.
7. Refresh the page. The latest artifact on the session should still be reopenable.
8. Stop Ollama and send a request. Confirm a clear model failure, not a crash.
9. Hit `http://localhost:8000/api/v1/ready` and `/api/v1/runtime`. Provider and retrieval mode should match the sidebar.
10. Run `docker compose down`, then `docker compose up --build`; health still returns `status: ok`.
