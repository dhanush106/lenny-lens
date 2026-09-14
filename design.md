# LennyLens — Design System & UX Specification

**Document Status:** Current Implementation Baseline  
**Version:** 1.0.0  

---

## 1. Design Philosophy

LennyLens is designed to feel like a high-end product research tool built for serious product thinkers. It deliberately rejects generic SaaS tropes—such as dark slate backgrounds, vibrant neon gradients, glassmorphism, heavy shadows, and rounded chat bubbles—in favor of a **radically minimal, calm, editorial workspace**.

### Core Aesthetic Principles
- **Print & Editorial Feel:** Uses warm neutral backgrounds reminiscent of high-grade paper (`Chalk`), crisp serif typography for headlines and prompts (`Newsreader`), and clean sans-serif for body reading (`Inter`).
- **Content as Hero:** Removes heavy card borders and speech bubbles. Information hierarchy is established through typography, whitespace, and font weights rather than heavy visual containers.
- **Quiet Micro-Interactions:** Subtle background highlights (`Fennel`), muted borders (`Stone Laurel`), and monospaced badges (`JetBrains Mono`).

---

## 2. Color Palette & Tokens

The application enforces a strict 4-color palette configured in `tailwind.config.js`:

| Token Name | Hex Code | Purpose & Usage |
| :--- | :--- | :--- |
| **Chalk** | `#E5E3D0` | Primary app background, main chat column, workspace shell. |
| **Chalk Subtle** | `#DCD9C4` | Input containers, drawer card backgrounds, subtle panel fills. |
| **Forest Umber** | `#493606` | Primary headings, active text, key buttons, dark structural accents. |
| **Stone Laurel** | `#646557` | Subtitles, metadata, timestamps, quiet borders, inactive icons. |
| **Fennel** | `#C9C49F` | Active session highlights, selection states, code pill backgrounds. |

---

## 3. Typography System

| Usage / Component | Font Family | Weight / Style | Tailwind Classes |
| :--- | :--- | :--- | :--- |
| **Brand Logo & Primary Headings** | `Newsreader` (Serif) | Bold (700) / SemiBold (600) | `font-serif font-bold text-forestUmber` |
| **User Prompts** | `Newsreader` (Serif) | Medium (500) | `text-lg font-serif text-forestUmber` |
| **Assistant Prose** | `Inter` (Sans-Serif) | Regular (400) | `prose-minimal text-forestUmber` |
| **Citation Badges & Code** | `JetBrains Mono` | Medium (500) | `font-mono text-[11px] bg-fennel/40` |
| **Labels & Eyebrows** | `JetBrains Mono` | SemiBold / Uppercase | `font-mono text-[10px] uppercase tracking-widest text-stoneLaurel` |

---

## 4. Component Architecture

```
[ App.jsx ]  (Workspace shell container with bg-chalk)
   │
   ├── [ Sidebar.jsx ]
   │      ├── Brand Header & Settings Toggle button
   │      ├── Collapsible Model Configuration Drawer (On-device vs Cloud)
   │      ├── Active Model Summary Badge
   │      ├── "New Conversation" Button
   │      └── Session History List (with Fennel active states)
   │
   ├── [ Chat.jsx ]
   │      ├── Empty State (Hero title & Starter Topic Buttons)
   │      ├── Message List (User questions in Serif, Assistant in Prose)
   │      ├── [ SourceCards.jsx ] (Footnote reference cards with quotes)
   │      ├── Loading Indicator (Dynamic text-based stage ticker)
   │      └── Input Form (Quiet borderless input container + ArrowUp button)
   │
   └── [ ArtifactViewer.jsx ] (Collapsible document workspace side-panel)
          ├── Panel Header (Title, Format type, Copy, Download, External, Close)
          ├── Tab Switcher (Preview vs Source code)
          └── Content Render Area (ReactMarkdown preview or Sandboxed HTML iframe)
```

---

## 5. Key UX Flows & Micro-Interactions

### 5.1 Interactive Citation Routing
1. In assistant messages, citation references like `[1]` and `[2]` are parsed and converted into monospaced text badges.
2. Clicking a citation badge `[1]` triggers `onHighlightSource(1)`.
3. The corresponding source card (`#source-card-1`) in `SourceCards.jsx` receives an active state highlight (`border-forestUmber bg-fennel/50`) and smooth-scrolls into view.

### 5.2 Dynamic Text Loading Ticker
Instead of a generic spinning loader, the system displays a text-based progress ticker indicating the backend execution stage:
`SEARCHING TRANSCRIPTS…` → `READING SOURCES…` → `SYNTHESIZING KNOWLEDGE…` → `COMPOSING ANSWER…`

### 5.3 Collapsible Model Configuration Drawer
- Located at the top of `Sidebar.jsx`.
- Standard mode displays a compact badge showing the active model (e.g. `ACTIVE MODEL: qwen3.5:2b`).
- Toggling the settings icon opens a minimal control card allowing users to switch between **On-device** (Ollama) and **Cloud** (OpenAI, Anthropic, OpenRouter) and test API keys.

---

## 6. HTML Security & Sandboxing Architecture

To prevent Cross-Site Scripting (XSS) or malicious code execution via LLM-generated HTML artifacts, LennyLens enforces a multi-layered security wrapper:

1. **Backend Sanitization (`security.py`):**
   - Uses `bleach` to parse and clean HTML string output.
   - Allows safe structural elements (`<!doctype html>`, `<html>`, `<head>`, `<body>`, `<h1>`-`<h6>`, `<p>`, `<style>`, `<table>`, `<ul>`, `<li>`, `<article>`, `<section>`, `<div>`, `<span>`).
   - Completely removes `<script>`, `<iframe>`, `<form>`, `<input>`, `<object>`, `<embed>`, inline event handlers (`onload`, `onclick`), and external network image links (`http://`, `https://`).
2. **CSP Meta Injection (`security.py`):**
   - Automatically injects `<meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src 'unsafe-inline';">` into every generated HTML document head.
3. **Frontend Sandboxing (`ArtifactViewer.jsx`):**
   - HTML preview is rendered inside an `<iframe>` with an empty sandbox attribute:
     `<iframe srcDoc={htmlDocument(content)} sandbox="" className="w-full h-full border-0 bg-white" />`.
   - `sandbox=""` restricts all script execution, popups, form submissions, and same-origin access.
