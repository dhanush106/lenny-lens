import React, { useMemo } from 'react';
import ReactMarkdown from 'react-markdown';
import { X, Code, FileText, ExternalLink } from 'lucide-react';

export default function ArtifactViewer({ activeArtifact, onClose }) {
  if (!activeArtifact) return null;

  let artifact = null;
  try {
    artifact = JSON.parse(activeArtifact);
  } catch (e) {
    // If it's not valid JSON, it's not an artifact. This component shouldn't render it.
    return null;
  }

  const { artifact_type, title, content } = artifact;

  const renderContent = () => {
    if (artifact_type === 'markdown') {
      return (
        <div className="prose prose-slate prose-invert max-w-none prose-sm p-6 overflow-y-auto h-full">
          <ReactMarkdown>{content}</ReactMarkdown>
        </div>
      );
    } else if (artifact_type === 'html') {
      // Sandboxed iframe for safe rendering
      const srcDoc = `
        <!DOCTYPE html>
        <html>
        <head>
          <meta charset="utf-8">
          <meta name="viewport" content="width=device-width, initial-scale=1">
        </head>
        <body style="margin: 0; padding: 1rem; font-family: system-ui, sans-serif;">
          ${content}
        </body>
        </html>
      `;
      return (
        <iframe
          srcDoc={srcDoc}
          sandbox=""
          className="w-full h-full border-0 bg-white"
          title="Artifact Preview"
        />
      );
    }
    return <div className="p-6 text-slate-400">Unsupported artifact type.</div>;
  };

  return (
    <div className="w-1/2 min-w-[400px] border-l border-slate-800 bg-slate-950 flex flex-col shadow-2xl animate-slide-in-right z-20">
      <div className="h-16 border-b border-slate-800 bg-slate-900/80 backdrop-blur-md flex items-center justify-between px-6 shrink-0">
        <div className="flex items-center gap-3 overflow-hidden">
          {artifact_type === 'html' ? (
            <Code className="text-cyan-400 shrink-0" size={18} />
          ) : (
            <FileText className="text-indigo-400 shrink-0" size={18} />
          )}
          <h2 className="text-sm font-semibold text-slate-200 truncate">{title || 'Generated Artifact'}</h2>
        </div>
        <div className="flex items-center gap-2">
          <button className="p-2 text-slate-400 hover:text-cyan-400 transition-colors rounded-lg hover:bg-slate-800">
             <ExternalLink size={16} />
          </button>
          <button 
            onClick={onClose}
            className="p-2 text-slate-400 hover:text-rose-400 transition-colors rounded-lg hover:bg-slate-800"
          >
            <X size={18} />
          </button>
        </div>
      </div>
      <div className="flex-1 overflow-hidden relative bg-slate-950">
        {renderContent()}
      </div>
    </div>
  );
}
