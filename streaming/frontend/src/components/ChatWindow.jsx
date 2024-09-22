import React, { useState, useEffect } from 'react';
import './ChatWindow.css';

const StreamingMessageBox = () => {
  const [streamedMessages, setStreamedMessages] = useState([]);

  useEffect(() => {
    const threadId = 'ththread_cJEs0nsgvYDyFfxE1ZxKu4EF';  // Use your actual thread ID
    
  // Open WebSocket connection
    const socket = new WebSocket(`ws://127.0.0.1:8001/ws/openstream/${threadId}/`);

    socket.onopen = function() {
      console.log('WebSocket connection opened');
      // Send a test message once the connection opens
      socket.send(JSON.stringify({ message: 'Hello, WebSocket!' }));
    };

    // When receiving a message through the WebSocket
    socket.onmessage = function (event) {
      const data = JSON.parse(event.data);
      const newMessage = data.message;

      setStreamedMessages((prevMessages) => [...prevMessages, newMessage]);
    };

    socket.onerror = function (error) {
      console.error("WebSocket error:", error);
    };

    socket.onclose = function () {
      console.log("WebSocket connection closed");
    };

    // // Cleanup WebSocket on component unmount to prevent memory leaks
    // return () => {
    //   if (socket.readyState === WebSocket.OPEN || socket.readyState === WebSocket.CONNECTING) {
    //     socket.close();
    //   }
    // };
  }, []);

  return (
    <div className="streaming-container">
      <h2>OpenAI Assistant Responses</h2>
      <div className="message-box">
        {streamedMessages.map((msg, index) => (
          <p key={index}>{msg}</p>
        ))}
      </div>
    </div>
  );
};

const ChatWindow = () => {
  const [message, setMessage] = useState('');

  // Helper function to send a message to the backend
  const sendMessageToBackend = async (message) => {
    try {
      const response = await fetch('http://127.0.0.1:8000/openstream/add-message/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          thread_id: 'thread_2nU1RPxlJ42nMYLuesE3I5xK', // Static thread ID for now
          content: message,
        }),
      });

      return await response.json();
    } catch (error) {
      console.error('Error sending message to backend:', error);
    }
  };

  // Helper function to execute run_assistant
  const runAssistant = async () => {
    try {
      const response = await fetch('http://127.0.0.1:8000/openstream/run-assistant/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          thread_id: 'thread_2nU1RPxlJ42nMYLuesE3I5xK',  // Static thread ID
        }),
      });

      return await response.json();
    } catch (error) {
      console.error('Error running assistant:', error);
    }
  };

  // Handler for submitting a message and running the assistant
  const handleSubmit = async (e) => {
    e.preventDefault();

    if (message.trim()) {
      try {
        // Step 1: Send the message to the backend
        const messageResponse = await sendMessageToBackend(message);
        console.log('Message response:', messageResponse);

        if (messageResponse && messageResponse.success) {
          // Step 2: Execute run_assistant after the message is sent
          const runResponse = await runAssistant();
          console.log('Run assistant response:', runResponse);
        }
      } catch (error) {
        console.error('Error:', error);
      }

      setMessage(''); // Clear the input box after submission
    }
  };

  return (
    <div className="container">
      <h1 className="title">Streaming PoC</h1>
      <h3 className="subtitle">Thread ID: thread_2nU1RPxlJ42nMYLuesE3I5xK</h3>
      <h3 className="subtitle">Assistant ID: asst_Ibsbv3KtyxTuXB7lj88yVZOi</h3>

      {/* Form for submitting a message */}
      <form onSubmit={handleSubmit} className="form">
        <input
          type="text"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          placeholder="Type your message..."
          className="input"
        />
        <button type="submit" className="button">Submit</button>
      </form>

      {/* Streaming message box */}
      <StreamingMessageBox />
    </div>
  );
};

export default ChatWindow;
