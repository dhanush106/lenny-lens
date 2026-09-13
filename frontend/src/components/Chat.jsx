import React, { useState, useRef, useEffect } from 'react';
import { Send, Bot, User, Loader2, Sparkles } from 'lucide-react';
import ReactMarkdown from 'react-markdown';

export default function Chat({ messages, onSendMessage, loading }) {
  const [input, setInput] = useState('');
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, loading]);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!input.trim() || loading) return;
    onSendMessage(input.trim());
    setInput('');
  };

  return (
    <div className="flex-1 flex flex-col h-full bg-slate-950 relative">
      {/* Decorative gradient background */}
      <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-slate-900 via-slate-950 to-slate-950 opacity-80 pointer-events-none"></div>
      
      <div className="flex-1 overflow-y-auto p-6 space-y-6 z-10 scroll-smooth">
        {messages.length === 0 ? (
          <div className="h-full flex flex-col items-center justify-center text-slate-500 space-y-4 animate-fade-in">
            <div className="w-16 h-16 rounded-2xl bg-slate-900 border border-slate-800 flex items-center justify-center shadow-xl shadow-cyan-500/10">
              <Sparkles className="w-8 h-8 text-cyan-400" />
            </div>
            <h2 className="text-xl font-medium text-slate-300">Start a conversation</h2>
            <p className="text-sm text-slate-500 max-w-sm text-center">
              Ask product and growth questions, request a Ship 30 essay, or generate an artifact.
            </p>
          </div>
        ) : (
          messages.map((msg, idx) => {
            // For artifacts, we might want to hide the raw json from the chat if it's rendered in the side panel
            // But let's assume we show a placeholder if it's an artifact JSON string.
            let content = msg.content;
            let isArtifact = false;
            try {
              if (content.trim().startsWith('{') && content.includes('"artifact_type"')) {
                const parsed = JSON.parse(content);
                isArtifact = true;
                content = `✨ Generated artifact: **${parsed.title}**\n\n*(See the artifact panel)*`;
              }
            } catch (e) {}

            return (
              <div
                key={idx}
                className={`flex gap-4 max-w-3xl mx-auto w-full ${
                  msg.role === 'user' ? 'justify-end' : 'justify-start'
                } animate-slide-up`}
              >
                {msg.role === 'assistant' && (
                  <div className="w-8 h-8 rounded-full bg-gradient-to-tr from-indigo-500 to-cyan-500 flex items-center justify-center flex-shrink-0 shadow-lg mt-1">
                    <Bot size={16} className="text-white" />
                  </div>
                )}
                
                <div
                  className={`px-5 py-4 rounded-2xl max-w-[80%] shadow-md backdrop-blur-sm ${
                    msg.role === 'user'
                      ? 'bg-gradient-to-br from-indigo-600 to-indigo-700 text-white rounded-br-none border border-indigo-500/50'
                      : 'bg-slate-900/80 text-slate-300 rounded-bl-none border border-slate-800'
                  }`}
                >
                  <div className="prose prose-invert prose-sm max-w-none">
                    <ReactMarkdown>{content}</ReactMarkdown>
                  </div>
                </div>
                
                {msg.role === 'user' && (
                  <div className="w-8 h-8 rounded-full bg-slate-800 border border-slate-700 flex items-center justify-center flex-shrink-0 mt-1">
                    <User size={16} className="text-slate-400" />
                  </div>
                )}
              </div>
            );
          })
        )}
        
        {loading && (
          <div className="flex gap-4 max-w-3xl mx-auto w-full justify-start animate-pulse">
             <div className="w-8 h-8 rounded-full bg-gradient-to-tr from-indigo-500 to-cyan-500 flex items-center justify-center flex-shrink-0 shadow-lg mt-1">
                <Loader2 size={16} className="text-white animate-spin" />
             </div>
             <div className="px-5 py-4 rounded-2xl bg-slate-900/80 text-slate-400 rounded-bl-none border border-slate-800 flex items-center gap-2">
                Generating response...
             </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <div className="p-6 bg-transparent z-10">
        <form onSubmit={handleSubmit} className="max-w-3xl mx-auto relative group">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Message LennyLens..."
            className="w-full bg-slate-900/90 border border-slate-700 focus:border-cyan-500 rounded-2xl py-4 pl-5 pr-14 text-slate-200 outline-none transition-all shadow-lg backdrop-blur-md placeholder:text-slate-500 focus:shadow-cyan-500/20"
            disabled={loading}
          />
          <button
            type="submit"
            disabled={!input.trim() || loading}
            className="absolute right-2 top-2 p-2 bg-gradient-to-r from-indigo-500 to-cyan-500 hover:from-indigo-400 hover:to-cyan-400 text-white rounded-xl disabled:opacity-50 disabled:cursor-not-allowed transition-all transform hover:scale-105 active:scale-95 shadow-md"
          >
            <Send size={18} />
          </button>
        </form>
      </div>
    </div>
  );
}
