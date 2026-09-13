# Design decisions

## Product experience

LennyLens is designed for product and growth teams who need evidence before
recommendations. The primary flow is intentionally short: create a session,
ask a question, inspect the source references, and optionally turn the
grounded material into an essay or artifact.

## Information architecture

- **Sidebar:** session history and a clear new-chat action.
- **Chat pane:** the active conversation, loading state, and model response.
- **Artifact pane:** a side-by-side preview so generated work does not replace
  the research conversation.

## Key states

- Empty session: explains the three supported tasks.
- Loading: disables duplicate sends and communicates that a response is in
  progress.
- Empty retrieval: the assistant says that transcript evidence is insufficient
  instead of inventing an answer.
- Artifact: JSON is summarized in chat and rendered in the dedicated pane.

## Accessibility and responsive behavior

The UI uses semantic buttons and form controls, visible focus styles, readable
contrast, and text labels/placeholders. On narrower screens, the artifact pane
should be treated as a secondary view; a future iteration should make it a
full-width drawer rather than retaining the current fixed minimum width.

## Artifact trust boundary

Generated HTML is sanitized server-side and rendered in an iframe with an empty
`sandbox` attribute. The preview cannot execute scripts, navigate the parent,
or access same-origin data. Markdown is rendered as text through ReactMarkdown.
