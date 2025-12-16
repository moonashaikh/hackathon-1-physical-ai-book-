from fastapi import APIRouter, HTTPException, Depends
from typing import List, Dict
import logging

from src.models.chatbot import ChatQuery, ChatResponse, QueryRequest, QueryResponse
from src.services.chatbot_service import chatbot_service

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/chat/query", response_model=ChatResponse)
async def chat_query(chat_query: ChatQuery):
    """
    Main chat endpoint that processes user queries and returns AI-generated responses
    based on textbook content using RAG.

    This RAG system utilizes OpenAI Agents/ChatKit SDKs, Qdrant Cloud Free Tier vector database
    and Neon Serverless Postgres to retrieve and answer questions about the textbook content.
    Supports dual modes: Full Book search and Selected Text mode (answers based only on user-selected text).
    """
    try:
        # Use the chatbot service to process the query based on the selected mode
        result = chatbot_service.process_query(
            query=chat_query.query,
            context_text=chat_query.context_text,
            mode=chat_query.mode
        )

        return ChatResponse(
            response=result["answer"],
            source_references=result["source_references"] if result["source_references"] else None,
            context_used=chat_query.context_text
        )

    except Exception as e:
        logger.error(f"Error processing chat query: {e}")
        raise HTTPException(status_code=500, detail="Internal server error processing your query")

@router.post("/query", response_model=QueryResponse)
async def query_endpoint(query_request: QueryRequest):
    """
    Query endpoint for retrieving relevant textbook content based on a query
    """
    try:
        # Use the chatbot service to retrieve relevant content
        relevant_chunks = chatbot_service.retrieve_relevant_content(
            query=query_request.query,
            context_text=query_request.context_text,
            top_k=query_request.top_k
        )

        # Generate response based on the retrieved content
        if relevant_chunks:
            # Combine the content to create a comprehensive answer
            combined_content = " ".join([item["content"] for item in relevant_chunks[:2]])  # Use top 2
            answer = f"Based on the textbook: {combined_content[:1000]}"  # Limit to 1000 chars
        else:
            answer = f"Could not find information about '{query_request.query}' in the textbook content."

        return QueryResponse(
            answer=answer,
            relevant_chunks=[
                {
                    "id": item["id"],
                    "content": item["content"][:200] + "..." if len(item["content"]) > 200 else item["content"],
                    "score": item["score"]
                }
                for item in relevant_chunks
            ],
            confidence_score=relevant_chunks[0]["score"] if relevant_chunks else 0.0
        )

    except Exception as e:
        logger.error(f"Error processing query: {e}")
        raise HTTPException(status_code=500, detail="Internal server error processing your query")

@router.post("/chat", response_model=ChatResponse)
async def general_chat(chat_query: ChatQuery):
    """
    General chat endpoint (could be used for broader conversations beyond textbook content)
    """
    try:
        # Use the chatbot service to process the query based on the selected mode
        result = chatbot_service.process_query(
            query=chat_query.query,
            context_text=chat_query.context_text,
            mode=chat_query.mode
        )

        return ChatResponse(
            response=result["answer"],
            context_used=chat_query.context_text
        )

    except Exception as e:
        logger.error(f"Error processing general chat: {e}")
        raise HTTPException(status_code=500, detail="Internal server error processing your chat")