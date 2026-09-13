import React from 'react';
import { MessageSquarePlus, MessageSquare } from 'lucide-react';

export default function Sidebar({ sessions, activeSessionId, onSelectSession, onNewSession }) {
  return (
    <div className="w-64 bg-slate-900 text-slate-300 flex flex-col h-full border-r border-slate-800 shadow-xl">
      <div className="p-6">
        <h1 className="text-2xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-indigo-400 to-cyan-400 mb-6">
          LennyLens
        </h1>
        <button
          onClick={onNewSession}
          className="w-full flex items-center justify-center gap-2 bg-gradient-to-r from-indigo-500 to-cyan-500 hover:from-indigo-400 hover:to-cyan-400 text-white py-3 px-4 rounded-xl font-medium transition-all transform hover:scale-[1.02] active:scale-95 shadow-lg shadow-indigo-500/30"
        >
          <MessageSquarePlus size={18} />
          New Chat
        </button>
      </div>
      
      <div className="flex-1 overflow-y-auto px-4 py-2 space-y-2">
        <div className="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-3 px-2">Recent Chats</div>
        {sessions.map((session) => (
          <button
            key={session.id}
            onClick={() => onSelectSession(session.id)}
            className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-200 text-left truncate ${
              activeSessionId === session.id
                ? 'bg-slate-800 text-cyan-400 shadow-inner border border-slate-700'
                : 'hover:bg-slate-800/50 hover:text-slate-200 text-slate-400'
            }`}
          >
            <MessageSquare size={16} className={activeSessionId === session.id ? 'text-cyan-400' : 'text-slate-500'} />
            <span className="truncate">{session.title || 'Untitled Chat'}</span>
          </button>
        ))}
      </div>
    </div>
  );
}
