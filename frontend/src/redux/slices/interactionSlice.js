import { createSlice } from '@reduxjs/toolkit';

const initialState = {
  loading: false,
  chatMessages: [
    { role: 'assistant', content: '👋 Hello! How can I help you log your HCP interaction?' }
  ]
};

const interactionSlice = createSlice({
  name: 'interactions',
  initialState,
  reducers: {
    setLoading: (state, action) => {
      state.loading = action.payload;
    },
    addChatMessage: (state, action) => {
      state.chatMessages.push(action.payload);
    }
  }
});

export const { setLoading, addChatMessage } = interactionSlice.actions;
export default interactionSlice.reducer;