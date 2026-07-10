import React from 'react';
import ChatView from './ChatView';

function LogInteractionScreen() {
  return (
    <div style={{ fontFamily: 'Inter, sans-serif', minHeight: '100vh', background: '#f0f2f5' }}>
      <div style={{ 
        background: '#1a1a2e', 
        padding: '15px 30px',
        color: 'white'
      }}>
        <h1 style={{ margin: 0, fontSize: 22 }}>🏥 AI CRM - HCP Module</h1>
      </div>
      <div style={{ padding: 30 }}>
        <ChatView />
      </div>
    </div>
  );
}

export default LogInteractionScreen;