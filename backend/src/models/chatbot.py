from pydantic import BaseModel
from typing import Optional, List, Dict
from datetime import datetime

class ChatQuery(BaseModel):
    query: str
    context_text: Optional[str] = None  # Optional context from selected text
    session_id: Optional[str] = None  # For tracking conversation history

class ChatResponse(BaseModel):
    response: str
    source_references: Optional[List[Dict]] = None  # References to textbook content used
    context_used: Optional[str] = None  # The context that was used to generate the response
    timestamp: datetime = datetime.now()

class EmbeddingRequest(BaseModel):
    text: str
    text_type: Optional[str] = "general"  # e.g., "chapter", "query", "context"

class EmbeddingResponse(BaseModel):
    embedding: List[float]
    text: str
    text_type: str

class QueryRequest(BaseModel):
    query: str
    context_text: Optional[str] = None
    top_k: Optional[int] = 5  # Number of similar chunks to retrieve

class QueryResponse(BaseModel):
    answer: str
    relevant_chunks: List[Dict]  # The chunks used to generate the answer
    confidence_score: Optional[float] = None