# Design decisions

## Product experience

LennyLens is designed for product and growth teams who need evidence before
recommendations. The primary flow is short: create a session, ask a question,
inspect source cards, then turn the same evidence into a Ship 30 essay or a
sandboxed HTML artifact.

## Information architecture

- **Sidebar:** session history, new chat, and the active provider/model badge
  from `/api/v1/runtime`.
- **Chat pane:** conversation, starter chips, skill-aware loading copy, inline
  `[n]` citation chips, and source cards with quote + guest + episode link.
- **Artifact pane:** Preview and Source tabs, copy, download, and pop-out. On
  small screens it is a full-viewport overlay; on desktop it sits beside chat.

## Key states

- Empty session: three starter chips (Q&A, Ship 30, HTML canvas).
- Loading: send is disabled; copy names the skill
  (“Retrieving transcripts…”, “Writing Ship 30 essay…”, “Rendering artifact…”).
- Empty retrieval: honest refusal, no invented guests.
- Artifact: chat shows a human summary plus an Open card; the pane renders the
  structured payload. Refresh restores the latest artifact on the session.

## Accessibility and responsive behavior

Inputs have labels, icon buttons have `aria-label`, focus styles are visible,
and contrast stays on the slate/cyan palette. The artifact viewer is an overlay
below the `md` breakpoint so it does not crush the chat column.

## Artifact trust boundary

Generated HTML is untrusted. The server allowlists tags and CSS, then the
viewer renders inside an iframe with an empty `sandbox` attribute and a CSP
that allows only inline styles. Markdown is rendered as text through
ReactMarkdown. Scripts, forms, iframes, and network requests are blocked.
