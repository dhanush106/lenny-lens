import React, { useEffect, useRef, useState } from 'react';
import { Check, ChevronDown, Cloud, Cpu, KeyRound, LoaderCircle, MessageSquare, MessageSquarePlus, RefreshCw, Server, Sparkles } from 'lucide-react';
import { getAvailableModels, updateRuntime } from '../api';

const PROVIDERS = [
  { id: 'openai', label: 'OpenAI', description: 'GPT models', icon: Sparkles },
  { id: 'anthropic', label: 'Anthropic', description: 'Claude models', icon: Sparkles },
  { id: 'openrouter', label: 'OpenRouter', description: 'Many providers', icon: Cloud },
];
const DEFAULT_LOCAL_MODEL = 'qwen3.5:2b';

function ProviderChoice({ provider, selected, onClick }) {
  const Icon = provider.icon;
  return <button type="button" onClick={onClick} aria-pressed={selected} className={`group flex min-w-0 items-center gap-2 rounded-lg border px-2.5 py-2 text-left transition focus:outline-none focus:ring-2 focus:ring-cyan-400/70 ${selected ? 'border-cyan-400/70 bg-cyan-400/10 text-cyan-100' : 'border-slate-700/80 bg-slate-900/70 text-slate-300 hover:border-slate-600 hover:bg-slate-800'}`}>
    <span className={`flex h-7 w-7 shrink-0 items-center justify-center rounded-md ${selected ? 'bg-cyan-400 text-slate-950' : 'bg-slate-800 text-slate-400'}`}><Icon size={14} /></span>
    <span className="min-w-0 flex-1"><span className="block truncate text-[11px] font-semibold">{provider.label}</span><span className="block truncate text-[10px] text-slate-500">{provider.description}</span></span>
    {selected && <Check size={14} className="shrink-0 text-cyan-300" aria-hidden="true" />}
  </button>;
}

export default function Sidebar({ sessions, activeSessionId, onSelectSession, onNewSession, runtime, onRuntimeChange }) {
  const [mode, setMode] = useState('local');
  const [provider, setProvider] = useState('ollama');
  const [apiKey, setApiKey] = useState('');
  const [models, setModels] = useState([]);
  const [model, setModel] = useState(DEFAULT_LOCAL_MODEL);
  const [loadingModels, setLoadingModels] = useState(false);
  const [status, setStatus] = useState(null);
  const fetchedInitialOllama = useRef(false);

  useEffect(() => { if (runtime) { setProvider(runtime.provider); setMode(runtime.provider === 'ollama' ? 'local' : 'cloud'); setModel(runtime.model); } }, [runtime]);

  const loadModels = async (chosenProvider = provider, key = apiKey) => {
    setLoadingModels(true); setStatus(null);
    try {
      const res = await getAvailableModels({ provider: chosenProvider, api_key: key });
      const nextModels = res.data.models || [];
      setModels(nextModels);
      setModel((current) => (nextModels.length && !nextModels.includes(current) ? nextModels[0] : current));
      setStatus({ tone: nextModels.length ? 'success' : 'warning', text: nextModels.length ? `${nextModels.length} model${nextModels.length === 1 ? '' : 's'} ready to choose${res.data.source ? ` · ${res.data.source}` : ''}` : chosenProvider === 'ollama' ? 'Ollama is connected, but no models are installed.' : 'No models were returned. Check the key and try again.' });
    } catch (err) { setModels([]); setStatus({ tone: 'error', text: err.response?.data?.detail || 'Could not load models. Check the connection and try again.' }); }
    finally { setLoadingModels(false); }
  };

  useEffect(() => { if (runtime?.provider === 'ollama' && !fetchedInitialOllama.current) { fetchedInitialOllama.current = true; loadModels('ollama'); } }, [runtime]);

  const chooseMode = (nextMode) => {
    const nextProvider = nextMode === 'local' ? 'ollama' : 'openai';
    setMode(nextMode); setProvider(nextProvider); setModels([]); setModel(nextProvider === 'ollama' ? runtime?.model || DEFAULT_LOCAL_MODEL : ''); setStatus(null);
    if (nextMode === 'local') loadModels('ollama');
  };
  const chooseProvider = (nextProvider) => { setProvider(nextProvider); setModels([]); setModel(''); setStatus(null); };
  const apply = async () => {
    setStatus(null);
    try { const res = await updateRuntime({ provider, model, api_key: apiKey }); onRuntimeChange(res.data); setApiKey(''); setStatus({ tone: 'success', text: `${model} is now active for this session.` }); }
    catch (err) { setStatus({ tone: 'error', text: err.response?.data?.detail || 'Could not activate this model.' }); }
  };

  const local = mode === 'local';
  const selectedProvider = PROVIDERS.find((item) => item.id === provider);
  const canApply = Boolean(model) && (local || Boolean(apiKey));
  const statusClass = status?.tone === 'error' ? 'border-rose-500/20 bg-rose-500/10 text-rose-200' : status?.tone === 'warning' ? 'border-amber-400/20 bg-amber-400/10 text-amber-100' : 'border-cyan-400/20 bg-cyan-400/10 text-cyan-100';

  return <aside className="flex h-full w-80 shrink-0 flex-col border-r border-slate-800 bg-slate-900 text-slate-300 shadow-xl">
    <div className="p-5 pb-3">
      <div className="mb-5 flex items-center gap-2"><div className="flex h-9 w-9 items-center justify-center rounded-xl bg-gradient-to-br from-indigo-500 to-cyan-400 shadow-lg shadow-cyan-500/10"><Sparkles size={17} className="text-white" /></div><div><h1 className="text-lg font-bold tracking-tight text-white">LennyLens</h1><p className="text-[10px] text-slate-500">Grounded product thinking</p></div></div>
      <section aria-labelledby="model-settings-title" className="rounded-2xl border border-slate-700/70 bg-slate-950/60 p-3.5 shadow-inner shadow-black/10">
        <div className="mb-3 flex items-start justify-between gap-2"><div><h2 id="model-settings-title" className="text-sm font-semibold text-slate-100">Choose a model</h2><p className="mt-0.5 text-[10px] leading-4 text-slate-500">Switch anytime. Your chats stay intact.</p></div><span className={`mt-0.5 rounded-full px-2 py-0.5 text-[9px] font-semibold uppercase tracking-wide ${local ? 'bg-emerald-400/10 text-emerald-300' : 'bg-violet-400/10 text-violet-300'}`}>{local ? 'Local' : 'Cloud'}</span></div>
        <div className="grid grid-cols-2 rounded-xl bg-slate-900 p-1" role="group" aria-label="Model location">
          <button type="button" onClick={() => chooseMode('local')} aria-pressed={local} className={`flex items-center justify-center gap-1.5 rounded-lg px-2 py-2 text-xs font-medium transition focus:outline-none focus:ring-2 focus:ring-cyan-400/70 ${local ? 'bg-slate-700 text-white shadow-sm' : 'text-slate-500 hover:text-slate-300'}`}><Server size={13} />On this device</button>
          <button type="button" onClick={() => chooseMode('cloud')} aria-pressed={!local} className={`flex items-center justify-center gap-1.5 rounded-lg px-2 py-2 text-xs font-medium transition focus:outline-none focus:ring-2 focus:ring-cyan-400/70 ${!local ? 'bg-slate-700 text-white shadow-sm' : 'text-slate-500 hover:text-slate-300'}`}><Cloud size={13} />Cloud</button>
        </div>
        {local ? <div className="mt-4 space-y-2">
          <div className="flex items-center justify-between"><label htmlFor="ollama-model" className="text-[11px] font-medium text-slate-300">Installed Ollama model</label><button type="button" onClick={() => loadModels('ollama')} className="flex items-center gap-1 text-[10px] font-medium text-cyan-300 hover:text-cyan-200 focus:outline-none focus:underline"><RefreshCw size={12} className={loadingModels ? 'animate-spin' : ''} />Refresh</button></div>
          <div className="relative"><Cpu size={14} className="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 text-slate-500" /><input id="ollama-model" list="ollama-models" value={model} onChange={(e) => setModel(e.target.value)} placeholder={DEFAULT_LOCAL_MODEL} className="w-full rounded-xl border border-slate-700 bg-slate-900 py-2.5 pl-9 pr-3 text-xs text-slate-100 outline-none transition placeholder:text-slate-600 focus:border-cyan-400 focus:ring-2 focus:ring-cyan-400/15" /><datalist id="ollama-models">{models.map((item) => <option key={item} value={item} />)}</datalist></div>
          <p className="text-[10px] leading-4 text-slate-500">Pick an installed model or enter its exact Ollama name.</p>
        </div> : <div className="mt-4 space-y-3">
          <div><p className="mb-1.5 text-[11px] font-medium text-slate-300">1. Select a provider</p><div className="grid grid-cols-3 gap-1.5">{PROVIDERS.map((item) => <ProviderChoice key={item.id} provider={item} selected={provider === item.id} onClick={() => chooseProvider(item.id)} />)}</div></div>
          <div><label htmlFor="provider-key" className="mb-1.5 flex items-center gap-1.5 text-[11px] font-medium text-slate-300"><KeyRound size={12} className="text-slate-500" />2. Add your {selectedProvider?.label} API key</label><input id="provider-key" type="password" autoComplete="off" value={apiKey} onChange={(e) => setApiKey(e.target.value)} placeholder="Paste key for this session" className="w-full rounded-xl border border-slate-700 bg-slate-900 px-3 py-2.5 text-xs text-slate-100 outline-none transition placeholder:text-slate-600 focus:border-cyan-400 focus:ring-2 focus:ring-cyan-400/15" /></div>
          <div><div className="mb-1.5 flex items-center justify-between"><label htmlFor="cloud-model" className="text-[11px] font-medium text-slate-300">3. Choose a model</label><button type="button" onClick={() => loadModels()} disabled={!apiKey || loadingModels} className="flex items-center gap-1 text-[10px] font-medium text-cyan-300 disabled:cursor-not-allowed disabled:text-slate-600 hover:text-cyan-200 focus:outline-none focus:underline">{loadingModels ? <LoaderCircle size={12} className="animate-spin" /> : <RefreshCw size={12} />}Find models</button></div><div className="relative"><select id="cloud-model" value={model} onChange={(e) => setModel(e.target.value)} disabled={!models.length} className="w-full appearance-none rounded-xl border border-slate-700 bg-slate-900 px-3 py-2.5 pr-9 text-xs text-slate-100 outline-none transition disabled:cursor-not-allowed disabled:text-slate-600 focus:border-cyan-400 focus:ring-2 focus:ring-cyan-400/15"><option value="">{models.length ? 'Select a model' : 'Add a key, then find models'}</option>{models.map((item) => <option key={item} value={item}>{item}</option>)}</select><ChevronDown size={14} className="pointer-events-none absolute right-3 top-1/2 -translate-y-1/2 text-slate-500" /></div></div>
          <p className="text-[10px] leading-4 text-slate-500">Your key is held only in server memory for this demo session.</p>
        </div>}
        {status && <p role="status" className={`mt-3 rounded-lg border px-2.5 py-2 text-[10px] leading-4 ${statusClass}`}>{status.text}</p>}
        <button type="button" onClick={apply} disabled={!canApply} className="mt-3 flex w-full items-center justify-center gap-2 rounded-xl bg-gradient-to-r from-indigo-500 to-cyan-500 px-3 py-2.5 text-xs font-semibold text-white shadow-lg shadow-indigo-500/20 transition hover:from-indigo-400 hover:to-cyan-400 focus:outline-none focus:ring-2 focus:ring-cyan-300 focus:ring-offset-2 focus:ring-offset-slate-950 disabled:cursor-not-allowed disabled:opacity-40"><Check size={14} />Use {model || 'this model'}</button>
        {runtime && <div className="mt-3 flex items-center gap-2 border-t border-slate-800 pt-3 text-[10px]"><span className="flex h-5 w-5 shrink-0 items-center justify-center rounded-full bg-emerald-400/10 text-emerald-300"><Check size={12} /></span><span className="min-w-0 text-slate-500">Active now <span className="font-medium text-slate-300">{runtime.model}</span></span></div>}
      </section>
      <button type="button" onClick={onNewSession} className="mt-4 flex w-full items-center justify-center gap-2 rounded-xl bg-gradient-to-r from-indigo-500 to-cyan-500 px-4 py-3 text-sm font-medium text-white shadow-lg shadow-indigo-500/30 transition hover:from-indigo-400 hover:to-cyan-400"><MessageSquarePlus size={17} />New chat</button>
    </div>
    <div className="flex-1 overflow-y-auto px-4 py-3"><div className="mb-2 px-2 text-[10px] font-semibold uppercase tracking-wider text-slate-500">Recent chats</div><div className="space-y-1">{sessions.map((session) => <button key={session.id} type="button" onClick={() => onSelectSession(session.id)} className={`flex w-full items-center gap-3 rounded-xl px-3 py-2.5 text-left text-xs transition ${activeSessionId === session.id ? 'border border-slate-700 bg-slate-800 text-cyan-300 shadow-inner' : 'text-slate-400 hover:bg-slate-800/70 hover:text-slate-200'}`}><MessageSquare size={15} className={activeSessionId === session.id ? 'shrink-0 text-cyan-400' : 'shrink-0 text-slate-500'} /><span className="truncate">{session.title || 'Untitled chat'}</span></button>)}</div></div>
  </aside>;
}
