import React, { useEffect, useRef, useState } from 'react';
import { Check, ChevronDown, Cloud, Cpu, KeyRound, LoaderCircle, MessageSquare, Plus, RefreshCw, Server, Sparkles, SlidersHorizontal } from 'lucide-react';
import { getAvailableModels, updateRuntime } from '../api';

const PROVIDERS = [
  { id: 'openai', label: 'OpenAI', description: 'GPT models' },
  { id: 'anthropic', label: 'Anthropic', description: 'Claude models' },
  { id: 'openrouter', label: 'OpenRouter', description: 'Many providers' },
];
const DEFAULT_LOCAL_MODEL = 'qwen3.5:2b';

function ProviderChoice({ provider, selected, onClick }) {
  return (
    <button
      type="button"
      onClick={onClick}
      aria-pressed={selected}
      className={`flex flex-col p-2 rounded-md border text-left transition-all focus:outline-none ${
        selected
          ? 'border-forestUmber bg-fennel/40 text-forestUmber'
          : 'border-stoneLaurel/20 bg-chalk-subtle/50 text-stoneLaurel hover:border-stoneLaurel/40 hover:text-forestUmber'
      }`}
    >
      <div className="flex items-center justify-between w-full">
        <span className="text-[11px] font-medium tracking-tight">{provider.label}</span>
        {selected && <Check size={11} className="text-forestUmber shrink-0" />}
      </div>
      <span className="text-[9px] text-stoneLaurel/80 mt-0.5">{provider.description}</span>
    </button>
  );
}

export default function Sidebar({ sessions, activeSessionId, onSelectSession, onNewSession, runtime, onRuntimeChange }) {
  const [mode, setMode] = useState('local');
  const [provider, setProvider] = useState('ollama');
  const [apiKey, setApiKey] = useState('');
  const [models, setModels] = useState([]);
  const [model, setModel] = useState(DEFAULT_LOCAL_MODEL);
  const [loadingModels, setLoadingModels] = useState(false);
  const [status, setStatus] = useState(null);
  const [settingsOpen, setSettingsOpen] = useState(false);
  const fetchedInitialOllama = useRef(false);

  useEffect(() => {
    if (runtime) {
      setProvider(runtime.provider);
      setMode(runtime.provider === 'ollama' ? 'local' : 'cloud');
      setModel(runtime.model);
    }
  }, [runtime]);

  const loadModels = async (chosenProvider = provider, key = apiKey) => {
    setLoadingModels(true);
    setStatus(null);
    try {
      const res = await getAvailableModels({ provider: chosenProvider, api_key: key });
      const nextModels = res.data.models || [];
      setModels(nextModels);
      setModel((current) => (nextModels.length && !nextModels.includes(current) ? nextModels[0] : current));
      setStatus({
        tone: nextModels.length ? 'success' : 'warning',
        text: nextModels.length
          ? `${nextModels.length} model${nextModels.length === 1 ? '' : 's'} available`
          : chosenProvider === 'ollama'
          ? 'Ollama is connected, but no models found.'
          : 'No models returned. Check API key.',
      });
    } catch (err) {
      setModels([]);
      setStatus({
        tone: 'error',
        text: err.response?.data?.detail || 'Could not load models.',
      });
    } finally {
      setLoadingModels(false);
    }
  };

  useEffect(() => {
    if (runtime?.provider === 'ollama' && !fetchedInitialOllama.current) {
      fetchedInitialOllama.current = true;
      loadModels('ollama');
    }
  }, [runtime]);

  const chooseMode = (nextMode) => {
    const nextProvider = nextMode === 'local' ? 'ollama' : 'openai';
    setMode(nextMode);
    setProvider(nextProvider);
    setModels([]);
    setModel(nextProvider === 'ollama' ? runtime?.model || DEFAULT_LOCAL_MODEL : '');
    setStatus(null);
    if (nextMode === 'local') loadModels('ollama');
  };

  const chooseProvider = (nextProvider) => {
    setProvider(nextProvider);
    setModels([]);
    setModel('');
    setStatus(null);
  };

  const apply = async () => {
    setStatus(null);
    try {
      const res = await updateRuntime({ provider, model, api_key: apiKey });
      onRuntimeChange(res.data);
      setApiKey('');
      setStatus({ tone: 'success', text: `Active: ${model}` });
    } catch (err) {
      setStatus({ tone: 'error', text: err.response?.data?.detail || 'Could not activate model.' });
    }
  };

  const local = mode === 'local';
  const selectedProvider = PROVIDERS.find((item) => item.id === provider);
  const canApply = Boolean(model) && (local || Boolean(apiKey));

  const statusClass =
    status?.tone === 'error'
      ? 'border-red-800/20 bg-red-900/10 text-red-900'
      : status?.tone === 'warning'
      ? 'border-amber-800/20 bg-amber-900/10 text-amber-900'
      : 'border-stoneLaurel/20 bg-fennel/30 text-forestUmber';

  return (
    <aside className="flex h-full w-72 shrink-0 flex-col border-r border-stoneLaurel/20 bg-chalk text-forestUmber">
      {/* Header */}
      <div className="p-5 pb-3">
        <div className="flex items-center justify-between mb-5">
          <div>
            <h1 className="text-lg font-serif font-bold tracking-tight text-forestUmber">LennyLens</h1>
            <p className="text-[10px] text-stoneLaurel tracking-widest font-mono uppercase">Grounded Product Thinking</p>
          </div>
          <button
            type="button"
            onClick={() => setSettingsOpen(!settingsOpen)}
            className={`p-1.5 rounded-md border transition-all ${
              settingsOpen
                ? 'border-forestUmber bg-fennel/50 text-forestUmber'
                : 'border-stoneLaurel/20 text-stoneLaurel hover:text-forestUmber hover:border-stoneLaurel/40'
            }`}
            title="Model Settings"
            aria-label="Toggle model settings"
          >
            <SlidersHorizontal size={14} />
          </button>
        </div>

        {/* Model Config Drawer / Panel */}
        {settingsOpen && (
          <section aria-labelledby="model-settings-title" className="mb-4 rounded-xl border border-stoneLaurel/20 bg-chalk-subtle/50 p-3.5 space-y-3">
            <div className="flex items-center justify-between">
              <h2 id="model-settings-title" className="text-xs font-semibold text-forestUmber">Model Provider</h2>
              <span className="text-[9px] font-mono uppercase px-1.5 py-0.5 rounded bg-fennel/40 text-forestUmber border border-stoneLaurel/20">
                {local ? 'Local' : 'Cloud'}
              </span>
            </div>

            <div className="grid grid-cols-2 p-0.5 rounded-lg bg-chalk border border-stoneLaurel/20 text-xs font-medium">
              <button
                type="button"
                onClick={() => chooseMode('local')}
                className={`py-1 rounded-md transition-all ${
                  local ? 'bg-fennel/60 text-forestUmber font-semibold shadow-xs' : 'text-stoneLaurel hover:text-forestUmber'
                }`}
              >
                On-device
              </button>
              <button
                type="button"
                onClick={() => chooseMode('cloud')}
                className={`py-1 rounded-md transition-all ${
                  !local ? 'bg-fennel/60 text-forestUmber font-semibold shadow-xs' : 'text-stoneLaurel hover:text-forestUmber'
                }`}
              >
                Cloud
              </button>
            </div>

            {local ? (
              <div className="space-y-2 pt-1">
                <div className="flex items-center justify-between text-[11px]">
                  <label htmlFor="ollama-model" className="font-medium text-forestUmber">Ollama Model</label>
                  <button
                    type="button"
                    onClick={() => loadModels('ollama')}
                    className="flex items-center gap-1 text-stoneLaurel hover:text-forestUmber font-mono text-[10px]"
                  >
                    <RefreshCw size={10} className={loadingModels ? 'animate-spin' : ''} /> Refresh
                  </button>
                </div>
                <input
                  id="ollama-model"
                  list="ollama-models"
                  value={model}
                  onChange={(e) => setModel(e.target.value)}
                  placeholder={DEFAULT_LOCAL_MODEL}
                  className="w-full rounded-md border border-stoneLaurel/30 bg-chalk py-1.5 px-2.5 text-xs text-forestUmber outline-none placeholder:text-stoneLaurel/50 focus:border-forestUmber"
                />
                <datalist id="ollama-models">
                  {models.map((item) => (
                    <option key={item} value={item} />
                  ))}
                </datalist>
              </div>
            ) : (
              <div className="space-y-2.5 pt-1">
                <div className="grid grid-cols-3 gap-1">
                  {PROVIDERS.map((item) => (
                    <ProviderChoice
                      key={item.id}
                      provider={item}
                      selected={provider === item.id}
                      onClick={() => chooseProvider(item.id)}
                    />
                  ))}
                </div>
                <div>
                  <label htmlFor="provider-key" className="block text-[11px] font-medium text-forestUmber mb-1">
                    API Key
                  </label>
                  <input
                    id="provider-key"
                    type="password"
                    autoComplete="off"
                    value={apiKey}
                    onChange={(e) => setApiKey(e.target.value)}
                    placeholder="Paste key for session"
                    className="w-full rounded-md border border-stoneLaurel/30 bg-chalk px-2.5 py-1.5 text-xs text-forestUmber outline-none placeholder:text-stoneLaurel/50 focus:border-forestUmber"
                  />
                </div>
                <div>
                  <div className="flex items-center justify-between mb-1">
                    <label htmlFor="cloud-model" className="text-[11px] font-medium text-forestUmber">Select Model</label>
                    <button
                      type="button"
                      onClick={() => loadModels()}
                      disabled={!apiKey || loadingModels}
                      className="text-[10px] text-stoneLaurel hover:text-forestUmber disabled:opacity-40 font-mono"
                    >
                      {loadingModels ? 'Loading...' : 'Find models'}
                    </button>
                  </div>
                  <select
                    id="cloud-model"
                    value={model}
                    onChange={(e) => setModel(e.target.value)}
                    disabled={!models.length}
                    className="w-full rounded-md border border-stoneLaurel/30 bg-chalk px-2 py-1.5 text-xs text-forestUmber outline-none focus:border-forestUmber disabled:opacity-50"
                  >
                    <option value="">{models.length ? 'Select a model' : 'Add key & fetch models'}</option>
                    {models.map((item) => (
                      <option key={item} value={item}>{item}</option>
                    ))}
                  </select>
                </div>
              </div>
            )}

            {status && (
              <p role="status" className={`rounded-md border p-2 text-[10px] font-mono leading-relaxed ${statusClass}`}>
                {status.text}
              </p>
            )}

            <button
              type="button"
              onClick={apply}
              disabled={!canApply}
              className="w-full py-1.5 text-xs font-semibold rounded-md border border-forestUmber bg-forestUmber text-chalk transition-all hover:bg-forestUmber-light disabled:opacity-30 disabled:cursor-not-allowed"
            >
              Use {model || 'Model'}
            </button>
          </section>
        )}

        {/* Runtime info summary */}
        {runtime && !settingsOpen && (
          <div className="mb-4 flex items-center justify-between text-[11px] px-2.5 py-1.5 rounded-md bg-chalk-subtle/60 border border-stoneLaurel/15 text-stoneLaurel">
            <span className="font-mono text-[9px] uppercase tracking-wider text-stoneLaurel/80">Active Model</span>
            <span className="font-medium text-forestUmber truncate max-w-[130px] font-mono text-[10px]">{runtime.model}</span>
          </div>
        )}

        {/* New Session Button */}
        <button
          type="button"
          onClick={onNewSession}
          className="flex w-full items-center justify-center gap-2 rounded-lg border border-forestUmber/30 bg-chalk-subtle/30 px-3 py-2 text-xs font-medium text-forestUmber transition-all hover:border-forestUmber hover:bg-fennel/30"
        >
          <Plus size={14} /> New Conversation
        </button>
      </div>

      {/* Sessions list */}
      <div className="flex-1 overflow-y-auto px-3 py-2 space-y-0.5">
        <div className="px-2 py-1.5 text-[9px] font-mono uppercase tracking-widest text-stoneLaurel/70">
          History
        </div>
        {sessions.map((session) => {
          const active = activeSessionId === session.id;
          return (
            <button
              key={session.id}
              type="button"
              onClick={() => onSelectSession(session.id)}
              className={`group flex w-full items-center gap-2.5 rounded-lg px-2.5 py-2 text-left text-xs transition-all ${
                active
                  ? 'bg-fennel/50 font-semibold text-forestUmber'
                  : 'text-stoneLaurel hover:bg-chalk-subtle/60 hover:text-forestUmber'
              }`}
            >
              <MessageSquare size={13} className={active ? 'text-forestUmber shrink-0' : 'text-stoneLaurel/60 shrink-0'} />
              <span className="truncate flex-1">{session.title || 'Untitled session'}</span>
            </button>
          );
        })}
      </div>
    </aside>
  );
}

