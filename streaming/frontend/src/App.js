import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import ChatWindow from './components/ChatWindow';
import Home from './components/Home';  // Import the Home component

const THREAD_ID = process.env.REACT_APP_THREAD_ID;  // Access the thread ID

function App() {
  return (
    <Router>
      <Routes>
        {/* Home route */}
        <Route path="/" element={<Home />} />

        {/* Chat route with thread ID as a parameter */}
        <Route path="/chat/:threadId" element={<ChatWindow />} />
      </Routes>
    </Router>
  );
}

export default App;
