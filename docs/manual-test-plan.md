# Manual test plan

Run `docker compose up --build`, then work through the following checks.

1. Open `http://localhost` and confirm that the sidebar and empty chat state
   render without browser-console errors.
2. Start two chats, add a message to each, and switch between them. Confirm
   their message histories remain separate.
3. After ingesting at least one transcript, ask a product question. Confirm the
   answer identifies source material; ask an unsupported question and confirm
   it declines rather than guessing.
4. Request a Ship 30 for 30 essay. Confirm it has a hook, headings, a useful
   takeaway, and citations.
5. Request an HTML artifact containing `<script>alert(1)</script>`. Confirm
   the preview appears but no script runs.
6. Stop Ollama and send a request. Confirm the app gives a clear model failure
   response rather than crashing.
7. Run `docker compose down`, then `docker compose up --build`; confirm the
   health endpoint returns `{"status":"ok", ...}`.
