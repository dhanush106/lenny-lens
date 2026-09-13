import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api/v1';

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

export default api;
