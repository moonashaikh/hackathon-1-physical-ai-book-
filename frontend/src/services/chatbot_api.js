/**
 * API client for interacting with the backend chatbot service
 *
 * This chatbot utilizes OpenAI Agents/ChatKit SDKs, FastAPI backend with Neon Serverless Postgres database
 * and Qdrant Cloud Free Tier to answer user questions about the book's content.
 * Supports dual modes: Full Book search and Selected Text mode (answers based only on user-selected text).
 */

// Docusaurus-compatible API URL - using a simple constant
// In Docusaurus, environment variables are handled differently
// You can override this in docusaurus.config.js if needed
const API_BASE_URL = 'http://localhost:8005/api';

class ChatbotAPIClient {
  constructor() {
    this.baseURL = API_BASE_URL;
  }

  /**
   * Get the auth token from localStorage
   */
  getAuthToken() {
    return localStorage.getItem('access_token');
  }

  /**
   * Send a query to the chatbot API
   */
  async queryChat(query, contextText = null, sessionId = null, mode = 'full_book') {
    try {
      const token = this.getAuthToken();
      const headers = {
        'Content-Type': 'application/json',
      };

      if (token) {
        headers['Authorization'] = `Bearer ${token}`;
      }

      const response = await fetch(`${this.baseURL}/chat/query`, {
        method: 'POST',
        headers: headers,
        body: JSON.stringify({
          query: query,
          context_text: contextText,
          session_id: sessionId,
          mode: mode
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
  async queryText(query, contextText = null, topK = 5, mode = 'full_book') {
    try {
      const token = this.getAuthToken();
      const headers = {
        'Content-Type': 'application/json',
      };

      if (token) {
        headers['Authorization'] = `Bearer ${token}`;
      }

      const response = await fetch(`${this.baseURL}/query`, {
        method: 'POST',
        headers: headers,
        body: JSON.stringify({
          query: query,
          context_text: contextText,
          top_k: topK,
          mode: mode
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
  async generalChat(query, contextText = null, sessionId = null, mode = 'full_book') {
    try {
      const token = this.getAuthToken();
      const headers = {
        'Content-Type': 'application/json',
      };

      if (token) {
        headers['Authorization'] = `Bearer ${token}`;
      }

      const response = await fetch(`${this.baseURL}/chat`, {
        method: 'POST',
        headers: headers,
        body: JSON.stringify({
          query: query,
          context_text: contextText,
          session_id: sessionId,
          mode: mode
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

  /**
   * Get vector database information
   */
  async getVectorDbInfo() {
    try {
      const token = this.getAuthToken();
      const headers = {
        'Content-Type': 'application/json',
      };

      if (token) {
        headers['Authorization'] = `Bearer ${token}`;
      }

      const response = await fetch(`${this.baseURL}/vector-db-info`, {
        method: 'GET',
        headers: headers,
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error getting vector database info:', error);
      throw error;
    }
  }

  /**
   * Get vector database points with pagination
   */
  async getVectorDbPoints(skip = 0, limit = 10) {
    try {
      const token = this.getAuthToken();
      const headers = {
        'Content-Type': 'application/json',
      };

      if (token) {
        headers['Authorization'] = `Bearer ${token}`;
      }

      const response = await fetch(`${this.baseURL}/vector-db-points?skip=${skip}&limit=${limit}`, {
        method: 'GET',
        headers: headers,
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error getting vector database points:', error);
      throw error;
    }
  }
}

// Export a singleton instance
const chatbotAPIClient = new ChatbotAPIClient();
export default chatbotAPIClient;