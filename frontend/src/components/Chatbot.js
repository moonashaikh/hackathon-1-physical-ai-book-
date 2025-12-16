import React, { useState, useEffect } from 'react';
import chatbotAPIClient from '../services/chatbot_api';
import styles from './Chatbot.module.css';

const Chatbot = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [selectedText, setSelectedText] = useState('');
  const [mode, setMode] = useState('full_book'); // 'full_book' or 'selected_text'

  // Function to handle text selection
  useEffect(() => {
    const handleTextSelection = () => {
      const selectedText = window.getSelection().toString().trim();
      if (selectedText) {
        setSelectedText(selectedText);
        // Auto-switch to selected text mode when text is selected
        setMode('selected_text');
      }
    };

    document.addEventListener('mouseup', handleTextSelection);
    return () => {
      document.removeEventListener('mouseup', handleTextSelection);
    };
  }, []);

  const handleSendMessage = async (e) => {
    e.preventDefault();
    if (!inputValue.trim()) return;

    // Add user message to chat
    const userMessage = { sender: 'user', text: inputValue, timestamp: new Date() };
    setMessages(prev => [...prev, userMessage]);

    try {
      // Call the backend API using the client service with mode
      const data = await chatbotAPIClient.queryChat(inputValue, selectedText, null, mode);
      const botMessage = { sender: 'bot', text: data.response, timestamp: new Date() };
      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      const errorMessage = { sender: 'bot', text: 'Sorry, I encountered an error. Please try again.', timestamp: new Date() };
      setMessages(prev => [...prev, errorMessage]);
    }

    setInputValue('');
    // Don't clear selectedText if in selected_text mode, as it might be needed for multiple queries
    if (mode === 'full_book') {
      setSelectedText('');
    }
  };

  const handleModeChange = (newMode) => {
    setMode(newMode);
    if (newMode === 'full_book') {
      setSelectedText(''); // Clear selected text when switching to full book mode
    }
  };

  return (
    <div className={styles.chatbotContainer}>
      {isOpen ? (
        <div className={styles.chatWindow}>
          <div className={styles.chatHeader}>
            <div className={styles.headerContent}>
              <h3>AI Textbook Chatbot</h3>
              <div className={styles.modeSelector}>
                <button
                  className={`${styles.modeButton} ${mode === 'full_book' ? styles.activeMode : ''}`}
                  onClick={() => handleModeChange('full_book')}
                >
                  Full Book
                </button>
                <button
                  className={`${styles.modeButton} ${mode === 'selected_text' ? styles.activeMode : ''}`}
                  onClick={() => handleModeChange('selected_text')}
                  disabled={!selectedText}
                >
                  Selected Text
                </button>
              </div>
            </div>
            <button onClick={() => setIsOpen(false)} className={styles.closeButton}>
              ×
            </button>
          </div>
          <div className={styles.chatMessages}>
            {messages.map((msg, index) => (
              <div key={index} className={`${styles.message} ${styles[msg.sender]}`}>
                {msg.text}
              </div>
            ))}
            {selectedText && mode === 'selected_text' && (
              <div className={styles.contextPreview}>
                <strong>Selected Text:</strong> {selectedText.substring(0, 100)}...
              </div>
            )}
            {mode === 'selected_text' && !selectedText && (
              <div className={styles.instruction}>
                Please select text in the textbook to use the Selected Text mode.
              </div>
            )}
          </div>
          <form onSubmit={handleSendMessage} className={styles.chatInputForm}>
            <input
              type="text"
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              placeholder={mode === 'selected_text' ? "Ask about the selected text..." : "Ask about the textbook content..."}
              className={styles.chatInput}
            />
            <button type="submit" className={styles.sendButton}>
              Send
            </button>
          </form>
        </div>
      ) : (
        <button onClick={() => setIsOpen(true)} className={styles.openButton}>
          🤖
        </button>
      )}
    </div>
  );
};

export default Chatbot;