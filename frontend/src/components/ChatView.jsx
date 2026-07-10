import React, { useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { addChatMessage, setLoading } from '../redux/slices/interactionSlice';
import { sendChatMessage } from '../services/api';

function ChatView() {
  const dispatch = useDispatch();
  const chatMessages = useSelector((state) => state.interactions.chatMessages);
  const loading = useSelector((state) => state.interactions.loading);
  const [input, setInput] = useState('');

  const handleSend = async () => {
    if (!input.trim() || loading) return;

    const userMessage = input;
    dispatch(addChatMessage({ role: 'user', content: userMessage }));
    setInput('');
    dispatch(setLoading(true));

    try {
      const response = await sendChatMessage(userMessage);
      dispatch(addChatMessage({ 
        role: 'assistant', 
        content: response.data.response || '✅ Done!' 
      }));
    } catch (error) {
      dispatch(addChatMessage({ 
        role: 'assistant', 
        content: '❌ Error: Make sure Django is running on port 8000' 
      }));
    }
    dispatch(setLoading(false));
  };

  return (
    <div style={{ maxWidth: 700, margin: '0 auto' }}>
      <h2>💬 AI Chat Assistant</h2>
      <div style={{
        border: '1px solid #ddd',
        borderRadius: 8,
        padding: 20,
        height: 400,
        overflowY: 'auto',
        background: '#f9f9f9'
      }}>
        {chatMessages.map((msg, i) => (
          <div key={i} style={{
            textAlign: msg.role === 'user' ? 'right' : 'left',
            margin: '10px 0'
          }}>
            <div style={{
              display: 'inline-block',
              background: msg.role === 'user' ? '#007bff' : '#e9ecef',
              color: msg.role === 'user' ? 'white' : 'black',
              padding: '10px 15px',
              borderRadius: 15,
              maxWidth: '80%'
            }}>
              {msg.content}
            </div>
          </div>
        ))}
        {loading && <div>⏳ Thinking...</div>}
      </div>
      <div style={{ marginTop: 15, display: 'flex', gap: 10 }}>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && handleSend()}
          placeholder="Type: Met Dr. Sharma today..."
          style={{ flex: 1, padding: 12, borderRadius: 5, border: '1px solid #ddd' }}
          disabled={loading}
        />
        <button onClick={handleSend} disabled={loading} style={{
          padding: '12px 25px',
          background: '#007bff',
          color: 'white',
          border: 'none',
          borderRadius: 5,
          cursor: 'pointer'
        }}>
          Send
        </button>
      </div>
    </div>
  );
}

export default ChatView;