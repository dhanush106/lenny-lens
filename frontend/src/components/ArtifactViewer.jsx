import React, { useMemo, useState } from 'react';
import ReactMarkdown from 'react-markdown';
import { X, Code, FileText, Copy, Download, ExternalLink, Eye } from 'lucide-react';
import { artifactFormat, htmlDocument } from './artifactViewerUtils';

export default function ArtifactViewer({ artifact, onClose }) {
  const [tab, setTab] = useState('preview');
  const [copied, setCopied] = useState(false);

  const parsed = useMemo(() => {
    if (!artifact) return null;
    if (typeof artifact === 'object') return artifact;
    try {
      return JSON.parse(artifact);
    } catch {
      return null;
    }
  }, [artifact]);

  if (!parsed) return null;

  const artifactType = artifactFormat(parsed);
  const { title, content } = parsed;
  const isHtml = artifactType === 'html';

  const copyContent = async () => {
    try {
      await navigator.clipboard.writeText(content || '');
      setCopied(true);
      setTimeout(() => setCopied(false), 1500);
    } catch {
      setCopied(false);
    }
  };

  const downloadContent = () => {
    const blob = new Blob([isHtml ? htmlDocument(content) : content || ''], {
      type: isHtml ? 'text/html' : 'text/markdown',
    });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `${(title || 'artifact').replace(/[^\w-]+/g, '-').toLowerCase()}.${isHtml ? 'html' : 'md'}`;
    link.click();
    URL.revokeObjectURL(url);
  };

  const popOut = () => {
    const blob = new Blob([isHtml ? htmlDocument(content) : content || ''], {
      type: isHtml ? 'text/html' : 'text/plain',
    });
    const url = URL.createObjectURL(blob);
    window.open(url, '_blank', 'noopener,noreferrer');
  };

  const renderPreview = () => {
    if (isHtml) {
      return (
        <iframe
          srcDoc={htmlDocument(content)}
          sandbox=""
          className="w-full h-full border-0 bg-white"
          title={title || 'Artifact Preview'}
        />
      );
    }
    return (
      <div className="prose prose-slate prose-invert max-w-none prose-sm p-6 overflow-y-auto h-full">
        <ReactMarkdown>{content}</ReactMarkdown>
      </div>
    );
  };

  return (
    <div className="fixed inset-0 z-30 bg-slate-950/80 md:static md:bg-transparent md:w-1/2 md:min-w-[400px] md:max-w-[640px] border-l border-slate-800 bg-slate-950 flex flex-col shadow-2xl">
      <div className="h-16 border-b border-slate-800 bg-slate-900/80 backdrop-blur-md flex items-center justify-between px-4 shrink-0 gap-2">
        <div className="flex items-center gap-3 overflow-hidden min-w-0">
          {isHtml ? (
            <Code className="text-cyan-400 shrink-0" size={18} />
          ) : (
            <FileText className="text-indigo-400 shrink-0" size={18} />
          )}
          <div className="min-w-0">
            <h2 className="text-sm font-semibold text-slate-200 truncate">{title || 'Generated Artifact'}</h2>
            <p className="text-[11px] text-slate-500 truncate">{isHtml ? 'Sandboxed HTML' : 'Markdown document'}</p>
          </div>
        </div>
        <div className="flex items-center gap-1">
          <button type="button" onClick={copyContent} className="p-2 text-slate-400 hover:text-cyan-400 rounded-lg hover:bg-slate-800" aria-label="Copy artifact">
            <Copy size={16} />
          </button>
          <button type="button" onClick={downloadContent} className="p-2 text-slate-400 hover:text-cyan-400 rounded-lg hover:bg-slate-800" aria-label="Download artifact">
            <Download size={16} />
          </button>
          <button type="button" onClick={popOut} className="p-2 text-slate-400 hover:text-cyan-400 rounded-lg hover:bg-slate-800" aria-label="Open artifact in new tab">
            <ExternalLink size={16} />
          </button>
          <button type="button" onClick={onClose} className="p-2 text-slate-400 hover:text-rose-400 rounded-lg hover:bg-slate-800" aria-label="Close artifact">
            <X size={18} />
          </button>
        </div>
      </div>
      <div className="px-4 py-2 border-b border-slate-800 flex items-center gap-2 text-xs">
        <button
          type="button"
          onClick={() => setTab('preview')}
          className={`px-3 py-1.5 rounded-lg flex items-center gap-1 ${tab === 'preview' ? 'bg-slate-800 text-cyan-300' : 'text-slate-400'}`}
        >
          <Eye size={14} /> Preview
        </button>
        <button
          type="button"
          onClick={() => setTab('source')}
          className={`px-3 py-1.5 rounded-lg flex items-center gap-1 ${tab === 'source' ? 'bg-slate-800 text-cyan-300' : 'text-slate-400'}`}
        >
          <Code size={14} /> Source
        </button>
        {copied && <span className="ml-auto text-cyan-400">Copied</span>}
      </div>
      <div className="flex-1 overflow-hidden relative bg-slate-950">
        {tab === 'preview' ? renderPreview() : (
          <pre className="h-full overflow-auto p-4 text-xs text-slate-300 whitespace-pre-wrap">{content}</pre>
        )}
      </div>
    </div>
  );
}
