from pydantic import BaseModel
from typing import Optional, List, Dict
from datetime import datetime
from enum import Enum

class ChatMode(str, Enum):
    FULL_BOOK = "full_book"
    SELECTED_TEXT = "selected_text"

class ChatQuery(BaseModel):
    query: str
    context_text: Optional[str] = None  # Optional context from selected text
    session_id: Optional[str] = None  # For tracking conversation history
    mode: ChatMode = ChatMode.FULL_BOOK  # Default to full book mode

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