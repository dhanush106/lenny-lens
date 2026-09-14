import React from 'react';
import { ExternalLink, Quote } from 'lucide-react';

export default function SourceCards({ sources, highlightedN, onSelect }) {
  if (!sources?.length) return null;

  return (
    <div className="source-index mt-6 space-y-2 border-t border-stoneLaurel/15 pt-4">
      <div className="eyebrow font-mono text-[10px] uppercase tracking-widest text-stoneLaurel">
        Referenced Sources
      </div>
      <div className="grid grid-cols-1 gap-2">
        {sources.map((source) => {
          const n = source.n ?? source.id;
          const active = highlightedN === n;
          return (
            <div
              key={`${source.chunk_id || source.id}-${n}`}
              id={`source-card-${n}`}
              className={`source-card w-full text-left rounded-lg border p-3 transition-all ${
                active
                  ? 'border-forestUmber bg-fennel/50 text-forestUmber shadow-xs'
                  : 'border-stoneLaurel/20 bg-chalk-subtle/30 hover:border-stoneLaurel/40 hover:bg-chalk-subtle/60'
              }`}
            >
              <div className="flex items-start justify-between gap-2">
                <div>
                  <button
                    type="button"
                    onClick={() => onSelect?.(n)}
                    className="text-left text-xs font-semibold text-forestUmber hover:underline flex items-center gap-1.5"
                  >
                    <span className="font-mono text-[10px] bg-fennel/60 border border-stoneLaurel/20 px-1 py-0.2 rounded text-forestUmber">
                      [{n}]
                    </span>
                    <span>{source.title || source.video_id || 'Untitled episode'}</span>
                  </button>
                  <div className="text-[11px] text-stoneLaurel mt-1 font-sans">
                    {source.guest ? source.guest : 'Guest not listed'}
                    {source.timestamp ? <span className="font-mono text-[10px] ml-1">· {source.timestamp}</span> : ''}
                  </div>
                </div>
                {source.source_url && (
                  <a
                    href={source.source_url}
                    target="_blank"
                    rel="noreferrer"
                    onClick={(event) => event.stopPropagation()}
                    className="shrink-0 text-stoneLaurel hover:text-forestUmber p-1"
                    aria-label="Open source episode"
                  >
                    <ExternalLink size={13} />
                  </a>
                )}
              </div>
              {source.excerpt && (
                <p className="mt-2 text-xs text-stoneLaurel leading-relaxed flex gap-2 font-serif italic border-l-2 border-stoneLaurel/30 pl-2">
                  <span>"{source.excerpt}"</span>
                </p>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
