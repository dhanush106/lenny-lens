import React from 'react';
import { ExternalLink, Quote } from 'lucide-react';

export default function SourceCards({ sources, highlightedN, onSelect }) {
  if (!sources?.length) return null;

  return (
    <div className="source-index mt-4 space-y-2">
      <div className="eyebrow text-[11px] font-semibold uppercase tracking-wider text-slate-500">Sources</div>
      {sources.map((source) => {
        const n = source.n ?? source.id;
        const active = highlightedN === n;
        return (
          <div
            key={`${source.chunk_id || source.id}-${n}`}
            id={`source-card-${n}`}
            className={`source-card w-full text-left rounded-xl border p-3 transition-colors ${
              active
                ? 'border-cyan-500/70 bg-cyan-500/10'
                : 'border-slate-800 bg-slate-950/60 hover:border-slate-700'
            }`}
          >
            <div className="flex items-start justify-between gap-2">
              <div>
                <button type="button" onClick={() => onSelect?.(n)} className="text-left text-xs font-semibold text-cyan-300 hover:underline">[{n}] {source.title || source.video_id || 'Untitled episode'}</button>
                <div className="text-[11px] text-slate-500 mt-0.5">
                  {source.guest ? source.guest : 'Guest not listed'}
                  {source.timestamp ? ` · ${source.timestamp}` : ''}
                </div>
              </div>
              {source.source_url && (
                <a
                  href={source.source_url}
                  target="_blank"
                  rel="noreferrer"
                  onClick={(event) => event.stopPropagation()}
                  className="shrink-0 text-slate-400 hover:text-cyan-300"
                  aria-label="Open source"
                >
                  <ExternalLink size={14} />
                </a>
              )}
            </div>
            {source.excerpt && (
              <p className="mt-2 text-xs text-slate-400 leading-relaxed flex gap-2">
                <Quote size={12} className="mt-0.5 shrink-0 text-slate-600" />
                <span>{source.excerpt}</span>
              </p>
            )}
          </div>
        );
      })}
    </div>
  );
}
