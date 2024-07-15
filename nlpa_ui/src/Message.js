import React from 'react';
import './Message.css';

const Message = ({ message }) => {
  const messageClass = message.sender === 'user' ? 'message user' : 'message bot';

  return (
    <div className={`message-container ${message.sender}`}>
      <div className={messageClass}>
        <div className="message-text"><div>{message.text}</div></div>
      </div>
    </div>
  );
};

export default Message;
