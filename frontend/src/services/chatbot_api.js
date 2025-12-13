/**
 * API client for interacting with the backend chatbot service
 */

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

class ChatbotAPIClient {
  constructor() {
    this.baseURL = API_BASE_URL;
  }

  /**
   * Send a query to the chatbot API
   */
  async queryChat(query, contextText = null, sessionId = null) {
    try {
      const response = await fetch(`${this.baseURL}/chat/query`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          query: query,
          context_text: contextText,
          session_id: sessionId
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error querying chatbot API:', error);
      throw error;
    }
  }

  /**
   * Send a general query to the backend
   */
  async queryText(query, contextText = null, topK = 5) {
    try {
      const response = await fetch(`${this.baseURL}/query`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          query: query,
          context_text: contextText,
          top_k: topK
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error querying text API:', error);
      throw error;
    }
  }

  /**
   * Send a general chat message
   */
  async generalChat(query, contextText = null, sessionId = null) {
    try {
      const response = await fetch(`${this.baseURL}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          query: query,
          context_text: contextText,
          session_id: sessionId
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error sending chat message:', error);
      throw error;
    }
  }
}

// Export a singleton instance
const chatbotAPIClient = new ChatbotAPIClient();
export default chatbotAPIClient;