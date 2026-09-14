import React, { useState, useRef, useEffect } from 'react';
import { FileText, ArrowUp } from 'lucide-react';
import ReactMarkdown from 'react-markdown';
import SourceCards from './SourceCards';

const STARTERS = [
  {
    label: 'Product Discovery vs Execution',
    text: 'What do Lenny’s guests say about product discovery versus execution?',
  },
  {
    label: 'Ship 30 Essay',
    text: 'Write a Ship 30 essay about why discovery should come before roadmap commitments.',
  },
  {
    label: 'Compare Approaches',
    text: 'Compare those two approaches and explain when each is useful.',
  },
  {
    label: 'HTML Strategy Canvas',
    text: 'Create an HTML product strategy canvas summarizing the discovery versus execution advice.',
  },
];

const LOADING_STAGES = [
  'SEARCHING TRANSCRIPTS…',
  'READING SOURCES…',
  'SYNTHESIZING KNOWLEDGE…',
  'COMPOSING ANSWER…',
];

function injectCites(children, onCite) {
  const cite = onCite || (() => {});
  const walk = (node) => {
    if (typeof node === 'string') {
      const parts = node.split(/(\[\d+\])/g);
      if (parts.length === 1) return node;
      return parts.map((part, index) => {
        const match = part.match(/^\[(\d+)\]$/);
        if (!match) return part;
        const n = Number(match[1]);
        return (
          <button
            key={`${n}-${index}`}
            type="button"
            onClick={() => cite(n)}
            className="inline-flex items-center justify-center font-mono text-[11px] font-medium text-forestUmber bg-fennel/40 hover:bg-fennel border border-stoneLaurel/30 px-1 py-0.5 rounded mx-0.5 align-baseline transition-all"
            aria-label={`Open source citation ${n}`}
          >
            [{n}]
          </button>
        );
      });
    }
    if (Array.isArray(node)) return node.map((child, index) => <React.Fragment key={index}>{walk(child)}</React.Fragment>);
    return node;
  };
  return walk(children);
}

export default function Chat({
  messages,
  onSendMessage,
  loading,
  loadingLabel,
  onOpenArtifact,
  highlightedSource,
  onHighlightSource,
}) {
  const [input, setInput] = useState('');
  const [loadingStageIdx, setLoadingStageIdx] = useState(0);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, loading]);

  useEffect(() => {
    if (!loading) {
      setLoadingStageIdx(0);
      return;
    }
    const interval = setInterval(() => {
      setLoadingStageIdx((prev) => (prev + 1) % LOADING_STAGES.length);
    }, 1400);
    return () => clearInterval(interval);
  }, [loading]);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!input.trim() || loading) return;
    onSendMessage(input.trim());
    setInput('');
  };

  const markdownComponents = {
    p: ({ children }) => <p>{injectCites(children, onHighlightSource)}</p>,
    li: ({ children }) => <li>{injectCites(children, onHighlightSource)}</li>,
    strong: ({ children }) => <strong>{injectCites(children, onHighlightSource)}</strong>,
  };

  return (
    <div className="flex-1 flex flex-col h-full bg-chalk relative min-w-0 text-forestUmber">
      {/* Messages area */}
      <div className="flex-1 overflow-y-auto px-6 py-8 space-y-10 scroll-smooth">
        {messages.length === 0 ? (
          <div className="h-full flex flex-col items-center justify-center text-center max-w-xl mx-auto py-12">
            <div className="mb-2 font-mono text-[10px] uppercase tracking-widest text-stoneLaurel">
              LennyLens Knowledge Engine
            </div>
            <h2 className="text-3xl font-serif font-bold text-forestUmber tracking-tight mb-3">
              Grounded product thinking.
            </h2>
            <p className="text-sm text-stoneLaurel leading-relaxed mb-8 max-w-md">
              Ask product and growth questions, generate Ship 30 essays, or construct interactive HTML strategy canvases grounded in Lenny’s podcast transcripts.
            </p>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-2.5 w-full max-w-lg">
              {STARTERS.map((starter) => (
                <button
                  key={starter.label}
                  type="button"
                  onClick={() => onSendMessage(starter.text)}
                  disabled={loading}
                  className="text-left p-3.5 rounded-xl border border-stoneLaurel/20 bg-chalk-subtle/50 text-forestUmber transition-all hover:border-forestUmber/40 hover:bg-fennel/30 group"
                >
                  <span className="block text-xs font-semibold group-hover:text-forestUmber">{starter.label}</span>
                  <span className="block text-[11px] text-stoneLaurel line-clamp-2 mt-0.5">{starter.text}</span>
                </button>
              ))}
            </div>
          </div>
        ) : (
          messages.map((msg, idx) => (
            <div key={msg.id || idx} className="max-w-2xl mx-auto w-full space-y-3">
              {/* Role Indicator */}
              <div className="flex items-center gap-2 font-mono text-[10px] uppercase tracking-widest text-stoneLaurel">
                <span>{msg.role === 'user' ? 'Question' : 'Analysis'}</span>
                <span className="w-1 h-1 rounded-full bg-stoneLaurel/40" />
              </div>

              {/* Message Content */}
              {msg.role === 'user' ? (
                <div className="text-lg font-serif font-medium text-forestUmber leading-snug py-1">
                  {msg.content}
                </div>
              ) : (
                <div className="space-y-4">
                  <div className="prose-minimal">
                    <ReactMarkdown components={markdownComponents}>
                      {msg.content}
                    </ReactMarkdown>
                  </div>

                  {msg.artifact && (
                    <button
                      type="button"
                      onClick={() => onOpenArtifact(msg.artifact)}
                      className="w-full flex items-center justify-between p-3 rounded-lg border border-stoneLaurel/30 bg-fennel/30 text-forestUmber hover:bg-fennel/60 transition-all font-mono text-xs"
                    >
                      <div className="flex items-center gap-2 truncate">
                        <FileText size={14} className="text-forestUmber shrink-0" />
                        <span className="font-medium truncate">{msg.artifact.title || 'Generated Artifact'}</span>
                      </div>
                      <span className="text-[10px] uppercase tracking-wider underline shrink-0 ml-2">View Document →</span>
                    </button>
                  )}

                  <SourceCards
                    sources={msg.sources}
                    highlightedN={highlightedSource}
                    onSelect={onHighlightSource}
                  />
                </div>
              )}
            </div>
          ))
        )}

        {loading && (
          <div className="max-w-2xl mx-auto w-full pt-2">
            <div className="flex items-center gap-2 font-mono text-[11px] text-stoneLaurel animate-pulse">
              <span className="w-1.5 h-1.5 rounded-full bg-forestUmber" />
              <span>{loadingLabel ? loadingLabel.toUpperCase() : LOADING_STAGES[loadingStageIdx]}</span>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input container */}
      <div className="p-4 md:p-6 bg-chalk border-t border-stoneLaurel/15">
        <form onSubmit={handleSubmit} className="max-w-2xl mx-auto relative">
          <label htmlFor="chat-input" className="sr-only">Message the assistant</label>
          <div className="flex items-center rounded-xl border border-stoneLaurel/30 bg-chalk-subtle/50 px-4 py-2.5 focus-within:border-forestUmber focus-within:bg-chalk transition-all">
            <input
              id="chat-input"
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask a product question, request a Ship 30 essay, or generate an artifact..."
              className="w-full bg-transparent text-sm text-forestUmber outline-none placeholder:text-stoneLaurel/60 font-sans"
              disabled={loading}
            />
            <button
              type="submit"
              disabled={!input.trim() || loading}
              className="ml-2 p-1.5 rounded-lg border border-forestUmber bg-forestUmber text-chalk disabled:opacity-20 disabled:border-stoneLaurel/30 disabled:bg-transparent disabled:text-stoneLaurel transition-all shrink-0"
              aria-label="Send message"
            >
              <ArrowUp size={15} />
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
