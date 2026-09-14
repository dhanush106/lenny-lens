import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api/v1';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const getSessions = () => api.get('/sessions/');
export const createSession = (title) => api.post('/sessions/', { user_id: 1, title });
export const getMessages = (sessionId) => api.get(`/sessions/${sessionId}/messages`);
export const sendMessage = (sessionId, message) => api.post(`/sessions/${sessionId}/chat`, { message });
export const getRuntime = () => api.get('/runtime');
export const updateRuntime = (config) => api.put('/runtime', config);
export const getAvailableModels = (config) => api.post('/runtime/models', config);

export default api;
