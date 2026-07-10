import axios from 'axios';

// ✅ Hardcode URL
const API_BASE = 'http://127.0.0.1:8000/api';

export const api = axios.create({
  baseURL: API_BASE,
  headers: { 'Content-Type': 'application/json' },
  timeout: 10000
});

export const sendChatMessage = (message) => {
  console.log('Sending to:', API_BASE + '/interactions/chat/');
  return api.post('/interactions/chat/', { message });
};