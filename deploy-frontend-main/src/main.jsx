import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import './index.css';
import App from './App.jsx';
import { loadConfig } from './config.js'; // Import the config loader

const startApp = async () => {
  await loadConfig(); // Load config before rendering
  createRoot(document.getElementById('root')).render(
    <StrictMode>
      <App />
    </StrictMode>
  );
};

startApp();

