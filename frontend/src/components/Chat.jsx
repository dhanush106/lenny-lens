import React, { useState, useRef, useEffect } from 'react';
import { Send, Bot, User, Loader2, Sparkles, FileText } from 'lucide-react';
import ReactMarkdown from 'react-markdown';
import SourceCards from './SourceCards';

const STARTERS = [
  {
    label: 'Ask a product question',
    text: 'What do Lenny’s guests say about product discovery versus execution?',
  },
  {
    label: 'Ship 30 essay',
    text: 'Write a Ship 30 essay about why discovery should come before roadmap commitments.',
  },
  {
    label: 'Compare those ideas',
    text: 'Compare those two approaches and explain when each is useful.',
  },
  {
    label: 'HTML strategy canvas',
    text: 'Create an HTML product strategy canvas summarizing the discovery versus execution advice.',
  },
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
            className="mx-0.5 text-cyan-300 font-semibold align-super text-[11px] hover:underline"
            aria-label={`Open source ${n}`}
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
  const messagesEndRef = useRef(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, loading]);

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
    <div className="flex-1 flex flex-col h-full bg-slate-950 relative min-w-0">
      <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-slate-900 via-slate-950 to-slate-950 opacity-80 pointer-events-none" />

      <div className="flex-1 overflow-y-auto p-6 space-y-6 z-10 scroll-smooth">
        {messages.length === 0 ? (
          <div className="h-full flex flex-col items-center justify-center text-slate-500 space-y-6">
            <div className="w-16 h-16 rounded-2xl bg-slate-900 border border-slate-800 flex items-center justify-center shadow-xl shadow-cyan-500/10">
              <Sparkles className="w-8 h-8 text-cyan-400" />
            </div>
            <div className="text-center space-y-2">
              <h2 className="text-xl font-medium text-slate-300">Lenny Growth Assistant</h2>
              <p className="text-sm text-slate-500 max-w-md">
                Ask product and growth questions, request a Ship 30 essay, or generate a sandboxed HTML artifact. Answers stay grounded in Lenny’s transcripts.
              </p>
            </div>
            <div className="flex flex-wrap justify-center gap-2 max-w-xl">
              {STARTERS.map((starter) => (
                <button
                  key={starter.label}
                  type="button"
                  onClick={() => onSendMessage(starter.text)}
                  disabled={loading}
                  className="text-left text-xs px-3 py-2 rounded-xl border border-slate-800 bg-slate-900/80 text-slate-300 hover:border-cyan-500/40 hover:text-cyan-200"
                >
                  {starter.label}
                </button>
              ))}
            </div>
          </div>
        ) : (
          messages.map((msg, idx) => (
            <div
              key={msg.id || idx}
              className={`flex gap-4 max-w-3xl mx-auto w-full ${
                msg.role === 'user' ? 'justify-end' : 'justify-start'
              }`}
            >
              {msg.role === 'assistant' && (
                <div className="w-8 h-8 rounded-full bg-gradient-to-tr from-indigo-500 to-cyan-500 flex items-center justify-center flex-shrink-0 shadow-lg mt-1">
                  <Bot size={16} className="text-white" />
                </div>
              )}

              <div
                className={`px-5 py-4 rounded-2xl max-w-[80%] shadow-md ${
                  msg.role === 'user'
                    ? 'bg-gradient-to-br from-indigo-600 to-indigo-700 text-white rounded-br-none border border-indigo-500/50'
                    : 'bg-slate-900/80 text-slate-300 rounded-bl-none border border-slate-800'
                }`}
              >
                <div className="prose prose-invert prose-sm max-w-none">
                  <ReactMarkdown components={msg.role === 'assistant' ? markdownComponents : undefined}>
                    {msg.content}
                  </ReactMarkdown>
                </div>
                {msg.artifact && (
                  <button
                    type="button"
                    onClick={() => onOpenArtifact(msg.artifact)}
                    className="mt-3 w-full flex items-center gap-2 text-left text-xs rounded-xl border border-cyan-500/30 bg-cyan-500/10 px-3 py-2 text-cyan-200 hover:bg-cyan-500/20"
                  >
                    <FileText size={14} />
                    <span>Open artifact: {msg.artifact.title || 'Generated document'}</span>
                  </button>
                )}
                {msg.role === 'assistant' && (
                  <SourceCards
                    sources={msg.sources}
                    highlightedN={highlightedSource}
                    onSelect={onHighlightSource}
                  />
                )}
              </div>

              {msg.role === 'user' && (
                <div className="w-8 h-8 rounded-full bg-slate-800 border border-slate-700 flex items-center justify-center flex-shrink-0 mt-1">
                  <User size={16} className="text-slate-400" />
                </div>
              )}
            </div>
          ))
        )}

        {loading && (
          <div className="flex gap-4 max-w-3xl mx-auto w-full justify-start">
            <div className="w-8 h-8 rounded-full bg-gradient-to-tr from-indigo-500 to-cyan-500 flex items-center justify-center flex-shrink-0 shadow-lg mt-1">
              <Loader2 size={16} className="text-white animate-spin" />
            </div>
            <div className="px-5 py-4 rounded-2xl bg-slate-900/80 text-slate-400 rounded-bl-none border border-slate-800">
              {loadingLabel || 'Generating response...'}
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <div className="p-6 bg-transparent z-10">
        <form onSubmit={handleSubmit} className="max-w-3xl mx-auto relative">
          <label htmlFor="chat-input" className="sr-only">Message the assistant</label>
          <input
            id="chat-input"
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask a product question, request an essay, or generate an artifact..."
            className="w-full bg-slate-900/90 border border-slate-700 focus:border-cyan-500 rounded-2xl py-4 pl-5 pr-14 text-slate-200 outline-none transition-all shadow-lg placeholder:text-slate-500"
            disabled={loading}
          />
          <button
            type="submit"
            disabled={!input.trim() || loading}
            className="absolute right-2 top-2 p-2 bg-gradient-to-r from-indigo-500 to-cyan-500 text-white rounded-xl disabled:opacity-50 disabled:cursor-not-allowed"
            aria-label="Send message"
          >
            <Send size={18} />
          </button>
        </form>
      </div>
    </div>
  );
}
