import React, { useState } from 'react';
import './InputArea.css';

const InputArea = ({ onSendMessage }) => {
  const [inputValue, setInputValue] = useState('');

  const handleInputChange = (e) => {
    setInputValue(e.target.value);
  };

  const handleSendClick = () => {
    if (inputValue.trim()) {
      onSendMessage(inputValue);
      setInputValue('');
    }
  };

  return (
    <div className="input-area">
      <input
        type="text"
        value={inputValue}
        onChange={handleInputChange}
        placeholder="Ask a question..."
      />
      <button onClick={handleSendClick}>Send</button>
    </div>
  );
};

export default InputArea;
