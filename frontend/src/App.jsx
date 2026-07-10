import React from 'react';
import { Provider } from 'react-redux';
import { store } from './redux/store';
import LogInteractionScreen from './components/LogInteractionScreen';
import '@fontsource/inter';

function App() {
  return (
    <Provider store={store}>
      <LogInteractionScreen />
    </Provider>
  );
}

export default App;