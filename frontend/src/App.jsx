import React, { useEffect, useState } from 'react';
import Sidebar from './components/Sidebar';
import Chat from './components/Chat';
import ArtifactViewer from './components/ArtifactViewer';
import { getSessions, createSession, getMessages, sendMessage } from './api';

function App() {
  const [sessions, setSessions] = useState([]);
  const [activeSessionId, setActiveSessionId] = useState(null);
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [activeArtifact, setActiveArtifact] = useState(null);

  useEffect(() => {
    fetchSessions();
  }, []);

  const fetchSessions = async () => {
    try {
      const res = await getSessions();
      setSessions(res.data);
      if (res.data.length > 0 && !activeSessionId) {
        handleSelectSession(res.data[0].id);
      }
    } catch (err) {
      console.error("Failed to fetch sessions", err);
    }
  };

  const handleSelectSession = async (id) => {
    setActiveSessionId(id);
    setActiveArtifact(null); // Close artifact on session switch
    try {
      const res = await getMessages(id);
      setMessages(res.data);
      checkForArtifacts(res.data);
    } catch (err) {
      console.error("Failed to fetch messages", err);
    }
  };

  const handleNewSession = async () => {
    try {
      const res = await createSession("New Chat " + (sessions.length + 1));
      setSessions([res.data, ...sessions]);
      setActiveSessionId(res.data.id);
      setMessages([]);
      setActiveArtifact(null);
    } catch (err) {
      console.error("Failed to create session", err);
    }
  };

  const handleSendMessage = async (text) => {
    if (!activeSessionId) return;

    // Optimistically add user message
    const userMsg = { role: 'user', content: text };
    setMessages(prev => [...prev, userMsg]);
    setLoading(true);

    try {
      const res = await sendMessage(activeSessionId, text);
      const assistantMsg = res.data.message;
      setMessages(prev => [...prev, assistantMsg]);
      
      // Check if the response contains an artifact
      try {
        if (assistantMsg.content.trim().startsWith('{') && assistantMsg.content.includes('"artifact_type"')) {
          setActiveArtifact(assistantMsg.content);
        }
      } catch (e) {}

    } catch (err) {
      console.error("Failed to send message", err);
      // fallback error message
      setMessages(prev => [...prev, { role: 'assistant', content: "An error occurred while generating a response." }]);
    } finally {
      setLoading(false);
    }
  };

  const checkForArtifacts = (msgs) => {
    // Look backwards for the most recent artifact
    for (let i = msgs.length - 1; i >= 0; i--) {
      const content = msgs[i].content;
      try {
        if (content.trim().startsWith('{') && content.includes('"artifact_type"')) {
          JSON.parse(content);
          setActiveArtifact(content);
          return;
        }
      } catch (e) {}
    }
  };

  return (
    <div className="flex h-screen w-full bg-slate-950 font-sans antialiased text-slate-200 overflow-hidden">
      <Sidebar 
        sessions={sessions} 
        activeSessionId={activeSessionId} 
        onSelectSession={handleSelectSession}
        onNewSession={handleNewSession}
      />
      <Chat 
        messages={messages} 
        onSendMessage={handleSendMessage} 
        loading={loading}
      />
      <ArtifactViewer 
        activeArtifact={activeArtifact} 
        onClose={() => setActiveArtifact(null)} 
      />
    </div>
  );
}

export default App;
