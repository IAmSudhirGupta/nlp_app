import React, { useState } from 'react';
import axios from 'axios';
import ChatWindow from './ChatWindow';
import InputArea from './InputArea';
import './App.css';

const App = () => {
  const [messages, setMessages] = useState([]);

  const handleSendMessage = async (text) => {
    const newMessage = { id: messages.length, text, sender: 'user' };
    setMessages([...messages, newMessage]);

    try {
      const response = await axios.post('http://localhost:5000/nlpa/qa', { message: text }); // Call Flask backend
      const botResponse = response.data;

      const parsedEntities = botResponse.parsed_question.entities.map(entity => (
        <div key={entity[0]} className="bot-section">
          <div className="bot-section-content">
            <span>- {entity[0]} ({entity[1]})</span>
          </div>
        </div>
      ));

      const posTags = botResponse.parsed_question.pos_tags.map(tag => (
        <span key={tag[0]}>{tag[0]} ({tag[1]}), </span>
      ));


      const tokens = botResponse.parsed_question.tokens.join(', ');

      const rankedResults = botResponse.ranked_results.map(result => (
        <div key={result[0][0]} className="bot-section">
          <div className="bot-section-content">
            <span>- {result[0][0]}: {result[0][1]} (Score: {result[1]})</span>
          </div>
        </div>
      ));

      const botMessage = {
        id: messages.length + 1,
        text: (
          <div>
            <div className="bot-section">
              <div className="bot-section-title">Parsed Entities:</div>
              {parsedEntities}
            </div>
            <div className="bot-section">
              <div className="bot-section-title">POS Tags:</div>
              <span>{posTags}</span><br /><br />
            </div>
            <div className="bot-section">
              <div className="bot-section-title">Tokens:</div>
              <span>{tokens}</span><br /><br />
            </div>
            <div className="bot-section">
              <div className="bot-section-title">Ranked Results:</div>
              {rankedResults}
            </div>
          </div>
        ),
        sender: 'bot'
      };

      setMessages((prevMessages) => [...prevMessages, botMessage]);
    } catch (error) {
      console.error('Error fetching the bot response:', error);
      const errorMessage = { id: messages.length + 1, text: "Sorry, something went wrong.", sender: 'bot' };
      setMessages((prevMessages) => [...prevMessages, errorMessage]);
    }
  };

  return (
    <div className="app">
      <ChatWindow messages={messages} />
      <InputArea onSendMessage={handleSendMessage} />
    </div>
  );
};

export default App;
