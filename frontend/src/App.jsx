import React, { useEffect, useState } from 'react';
import Sidebar from './components/Sidebar';
import Chat from './components/Chat';
import ArtifactViewer from './components/ArtifactViewer';
import { getSessions, createSession, getMessages, sendMessage, getRuntime } from './api';

function classifyIntent(text) {
  const normalized = text.toLowerCase();
  if (normalized.includes('essay') || normalized.includes('ship 30')) return 'essay';
  if (/(html|css|canvas|artifact|markdown)/.test(normalized) && /(generat|creat|build|make|render)/.test(normalized)) {
    return 'artifact';
  }
  return 'qna';
}

function loadingCopy(intent) {
  if (intent === 'essay') return 'Writing Ship 30 essay…';
  if (intent === 'artifact') return 'Rendering artifact…';
  return 'Retrieving transcripts…';
}

function latestArtifact(msgs) {
  for (let i = msgs.length - 1; i >= 0; i -= 1) {
    if (msgs[i].artifact) return msgs[i].artifact;
  }
  return null;
}

function App() {
  const [sessions, setSessions] = useState([]);
  const [activeSessionId, setActiveSessionId] = useState(null);
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [loadingIntent, setLoadingIntent] = useState('qna');
  const [activeArtifact, setActiveArtifact] = useState(null);
  const [highlightedSource, setHighlightedSource] = useState(null);
  const [runtime, setRuntime] = useState(null);

  useEffect(() => {
    fetchSessions();
    getRuntime()
      .then((res) => setRuntime(res.data))
      .catch(() => setRuntime(null));
  }, []);

  const fetchSessions = async () => {
    try {
      const res = await getSessions();
      setSessions(res.data);
      if (res.data.length > 0 && !activeSessionId) {
        handleSelectSession(res.data[0].id);
      }
    } catch (err) {
      console.error('Failed to fetch sessions', err);
    }
  };

  const handleSelectSession = async (id) => {
    setActiveSessionId(id);
    setHighlightedSource(null);
    try {
      const res = await getMessages(id);
      setMessages(res.data);
      setActiveArtifact(latestArtifact(res.data));
    } catch (err) {
      console.error('Failed to fetch messages', err);
    }
  };

  const handleNewSession = async () => {
    try {
      const res = await createSession(`New Chat ${sessions.length + 1}`);
      setSessions([res.data, ...sessions]);
      setActiveSessionId(res.data.id);
      setMessages([]);
      setActiveArtifact(null);
      setHighlightedSource(null);
    } catch (err) {
      console.error('Failed to create session', err);
    }
  };

  const handleHighlightSource = (n) => {
    setHighlightedSource(n);
    const card = document.getElementById(`source-card-${n}`);
    card?.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  };

  const handleSendMessage = async (text) => {
    let sessionId = activeSessionId;
    if (!sessionId) {
      try {
        const created = await createSession('New Chat');
        sessionId = created.data.id;
        setSessions((prev) => [created.data, ...prev]);
        setActiveSessionId(sessionId);
      } catch (err) {
        console.error('Failed to create session', err);
        return;
      }
    }

    const userMsg = { role: 'user', content: text };
    setMessages((prev) => [...prev, userMsg]);
    setLoadingIntent(classifyIntent(text));
    setLoading(true);

    try {
      const res = await sendMessage(sessionId, text);
      const assistantMsg = {
        ...res.data.message,
        sources: res.data.sources || res.data.message.sources || [],
        artifact: res.data.artifact || res.data.message.artifact || null,
        error: res.data.error || null,
      };
      setMessages((prev) => [...prev, assistantMsg]);
      if (assistantMsg.artifact) {
        setActiveArtifact(assistantMsg.artifact);
      }
    } catch (err) {
      console.error('Failed to send message', err);
      const detail = err.response?.data?.detail;
      const message = typeof detail === 'object' ? detail.message : detail;
      setMessages((prev) => [
        ...prev,
        { role: 'assistant', content: message || 'An error occurred while generating a response.' },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="workspace-shell flex h-screen w-full bg-slate-950 font-sans antialiased text-slate-200 overflow-hidden">
      <Sidebar
        sessions={sessions}
        activeSessionId={activeSessionId}
        onSelectSession={handleSelectSession}
        onNewSession={handleNewSession}
        runtime={runtime}
        onRuntimeChange={setRuntime}
      />
      <Chat
        messages={messages}
        onSendMessage={handleSendMessage}
        loading={loading}
        loadingLabel={loadingCopy(loadingIntent)}
        onOpenArtifact={setActiveArtifact}
        highlightedSource={highlightedSource}
        onHighlightSource={handleHighlightSource}
      />
      <ArtifactViewer
        artifact={activeArtifact}
        onClose={() => setActiveArtifact(null)}
      />
    </div>
  );
}

export default App;
