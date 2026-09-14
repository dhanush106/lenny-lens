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
      <div className="prose-minimal p-6 overflow-y-auto h-full bg-chalk">
        <ReactMarkdown>{content}</ReactMarkdown>
      </div>
    );
  };

  return (
    <div className="fixed inset-0 z-30 bg-chalk/90 md:static md:bg-transparent md:w-1/2 md:min-w-[400px] md:max-w-[640px] border-l border-stoneLaurel/20 bg-chalk flex flex-col shadow-xl">
      <div className="h-14 border-b border-stoneLaurel/20 bg-chalk-subtle/50 flex items-center justify-between px-4 shrink-0 gap-2">
        <div className="flex items-center gap-2.5 overflow-hidden min-w-0">
          {isHtml ? (
            <Code className="text-forestUmber shrink-0" size={16} />
          ) : (
            <FileText className="text-forestUmber shrink-0" size={16} />
          )}
          <div className="min-w-0">
            <h2 className="text-xs font-serif font-bold text-forestUmber truncate">{title || 'Generated Artifact'}</h2>
            <p className="text-[10px] font-mono text-stoneLaurel truncate uppercase tracking-wide">
              {isHtml ? 'Sandboxed HTML Canvas' : 'Markdown Document'}
            </p>
          </div>
        </div>
        <div className="flex items-center gap-1">
          <button type="button" onClick={copyContent} className="p-1.5 text-stoneLaurel hover:text-forestUmber rounded hover:bg-fennel/40 transition-all" aria-label="Copy artifact">
            <Copy size={15} />
          </button>
          <button type="button" onClick={downloadContent} className="p-1.5 text-stoneLaurel hover:text-forestUmber rounded hover:bg-fennel/40 transition-all" aria-label="Download artifact">
            <Download size={15} />
          </button>
          <button type="button" onClick={popOut} className="p-1.5 text-stoneLaurel hover:text-forestUmber rounded hover:bg-fennel/40 transition-all" aria-label="Open artifact in new tab">
            <ExternalLink size={15} />
          </button>
          <button type="button" onClick={onClose} className="p-1.5 text-stoneLaurel hover:text-forestUmber rounded hover:bg-fennel/40 transition-all" aria-label="Close artifact">
            <X size={16} />
          </button>
        </div>
      </div>

      <div className="px-4 py-1.5 border-b border-stoneLaurel/15 flex items-center gap-2 text-xs bg-chalk">
        <button
          type="button"
          onClick={() => setTab('preview')}
          className={`px-2.5 py-1 rounded font-mono text-[11px] flex items-center gap-1 transition-all ${
            tab === 'preview' ? 'bg-fennel/60 font-semibold text-forestUmber border border-stoneLaurel/20' : 'text-stoneLaurel hover:text-forestUmber'
          }`}
        >
          <Eye size={13} /> Preview
        </button>
        <button
          type="button"
          onClick={() => setTab('source')}
          className={`px-2.5 py-1 rounded font-mono text-[11px] flex items-center gap-1 transition-all ${
            tab === 'source' ? 'bg-fennel/60 font-semibold text-forestUmber border border-stoneLaurel/20' : 'text-stoneLaurel hover:text-forestUmber'
          }`}
        >
          <Code size={13} /> Source
        </button>
        {copied && <span className="ml-auto font-mono text-[10px] text-forestUmber">Copied</span>}
      </div>

      <div className="flex-1 overflow-hidden relative bg-chalk">
        {tab === 'preview' ? renderPreview() : (
          <pre className="h-full overflow-auto p-5 text-xs text-forestUmber font-mono bg-chalk-subtle/30 whitespace-pre-wrap">{content}</pre>
        )}
      </div>
    </div>
  );
}
