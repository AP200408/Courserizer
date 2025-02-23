import React, { useState } from 'react';
import './Chatbot.css';
import Navbar from '../Navbar/Navbar';
import Footer from '../Footer/Footer';

const Chatbot = () => {
  const [input, setInput] = useState('');
  const [chatHistory, setChatHistory] = useState([]);
  const [streaming, setStreaming] = useState(false);

  const sendQuestion = async () => {
    if (!input.trim()) return;
    
    setChatHistory((prev) => [...prev, { role: 'user', text: input }]);
    setInput('');
    setStreaming(true);

    const response = await fetch('http://localhost:5000/Korsy', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ question: input })
    });

    if (!response.ok) {
      setChatHistory((prev) => [...prev, { role: 'bot', text: 'Error: Unable to get response.' }]);
      setStreaming(false);
      return;
    }

    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    let botAnswer = '';

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      const chunk = decoder.decode(value);
      botAnswer += chunk;
      setChatHistory((prev) => {
        const last = prev[prev.length - 1];
        if (last && last.role === 'bot' && !last.final) {
          const updated = { ...last, text: botAnswer };
          return [...prev.slice(0, -1), updated];
        } else {
          return [...prev, { role: 'bot', text: botAnswer }];
        }
      });
    }
    setStreaming(false);
  };

  return (<>
    <Navbar />
    <div className="chatbot-wrapper">
      <div className="chatbot-container">
        <h2 className="chatbot-title">KorsyAI</h2>
        <div className="chat-history">
          {chatHistory.map((msg, index) => (
            <div key={index} className={`chat-message ${msg.role}`}>
              <div className="chat-bubble">{msg.text}</div>
            </div>
          ))}
        </div>
        <div className="chat-input-area">
          <textarea
            rows="3"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Type your question here..."
            className="chat-input"
          />
          <button
            onClick={sendQuestion}
            disabled={streaming}
            className="chat-send-button"
          >
            {streaming ? 'Waiting for response...' : 'Send'}
          </button>
        </div>
      </div>
    </div>
    <Footer/>
    </>
  );
};

export default Chatbot;
