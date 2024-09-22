import React from 'react';
import { Link } from 'react-router-dom';
import './Home.css';  // Ensure this path is correct

const THREAD_ID = process.env.REACT_APP_THREAD_ID;  // Access the thread ID

const Home = () => {
  return (
    <div className="home-container">
      <h1>Welcome to Streaming PoC</h1>
      <p>Click the button below to go to the chat page.</p>
      <Link to={`/chat/${THREAD_ID}`}>  {/* Pass the THREAD_ID here */}
        <button className="home-button">Go to Chat</button>
      </Link>
    </div>
  );
};

export default Home;
