# Quickstart Guide: Textbook Generation Feature

This guide provides a quick overview of how to set up, run, and interact with the Textbook Generation project, including both the Docusaurus frontend and FastAPI backend.

## 1. Prerequisites

Ensure you have the following installed:

*   **Node.js** (LTS version recommended) and **npm** or **Yarn** (for Docusaurus frontend)
*   **Python 3.11+** (for FastAPI backend)
*   **Git**
*   **Docker** (optional, for local Qdrant/Postgres setup)

## 2. Setup

### Frontend (Docusaurus)

1.  **Navigate to the frontend directory**:
    ```bash
    cd frontend
    ```

2.  **Install dependencies**:
    ```bash
    npm install # or yarn install
    ```

3.  **Start the Docusaurus development server**:
    ```bash
    npm start # or yarn start
    ```
    The Docusaurus site should now be accessible at `http://localhost:3000`.

### Backend (FastAPI)

1.  **Navigate to the backend directory**:
    ```bash
    cd backend
    ```

2.  **Create a virtual environment and activate it**:
    ```bash
    python -m venv venv
    ./venv/Scripts/activate # On Windows
    source venv/bin/activate # On macOS/Linux
    ```

3.  **Install Python dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up environment variables**:
    Create a `.env` file in the `backend/` directory with your Qdrant and Neon Postgres connection details. Example:
    ```dotenv
    QDRANT_HOST=localhost
    QDRANT_PORT=6333
    NEON_POSTGRES_URL="postgresql://user:password@host:port/database"
    ```

5.  **Run database migrations (initial setup)**:
    (Once implemented, this will create your tables in Neon Postgres and potentially Qdrant collections)
    ```bash
    # Example command (actual command will be defined during implementation)
    python -m app.db.schema migrate
    ```

6.  **Start the FastAPI server**:
    ```bash
    uvicorn main:app --reload
    ```
    The FastAPI application will be running at `http://localhost:8000`. You can access the API documentation at `http://localhost:8000/docs`.

## 3. Interacting with the RAG Chatbot (Backend API)

You can interact with the backend API using tools like `curl`, Postman, or directly from the `/docs` page (Swagger UI).

### Example: Embedding Chapter Content

```bash
curl -X POST "http://localhost:8000/embed" \
  -H "Content-Type: application/json" \
  -d '{ "chapter_id": "<UUID_OF_CHAPTER>", "content": "# Chapter 1\nThis is the content..." }'
```

### Example: Querying the RAG Chatbot

```bash
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{ "query_text": "What is Physical AI?" }'
```

### Example: General Chat

```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{ "message": "Tell me about humanoid robotics." }'
```

## 4. Deployment

Deployment to GitHub Pages will be handled via GitHub Actions. Refer to the project's GitHub Actions workflows for details.
