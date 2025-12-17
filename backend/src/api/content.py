from fastapi import APIRouter, HTTPException, Depends
from typing import List, Dict
import logging

from src.models.chatbot import ChatQuery, ChatResponse, QueryRequest, QueryResponse
from src.services.content_service import content_service
from src.services.qdrant_service import qdrant_service
from src.middleware.auth_middleware import get_current_user
from pydantic import BaseModel

router = APIRouter()
logger = logging.getLogger(__name__)

# Define the request models for uploading textbook content
class Chapter(BaseModel):
    id: str
    title: str
    content: str

class ContentUploadRequest(BaseModel):
    chapters: List[Chapter]

@router.post("/content/upload", response_model=Dict[str, bool])
async def upload_textbook_content(content_request: ContentUploadRequest, current_user: dict = Depends(get_current_user)):
    """
    Upload textbook content to be indexed for RAG
    """
    try:
        # Upload all chapters to the content service
        results = content_service.store_textbook_chapters(content_request.chapters)

        return results

    except Exception as e:
        logger.error(f"Error uploading textbook content: {e}")
        raise HTTPException(status_code=500, detail="Internal server error uploading textbook content")

@router.post("/content/upload-single")
async def upload_single_chapter(chapter: Chapter, current_user: dict = Depends(get_current_user)):
    """
    Upload a single chapter to be indexed for RAG
    """
    try:
        success = content_service.store_textbook_content(
            chapter_id=chapter.id,
            title=chapter.title,
            content=chapter.content
        )

        return {"success": success, "chapter_id": chapter.id}

    except Exception as e:
        logger.error(f"Error uploading single chapter: {e}")
        raise HTTPException(status_code=500, detail="Internal server error uploading chapter")

@router.get("/vector-db-info")
async def get_vector_db_info(current_user: dict = Depends(get_current_user)):
    """
    Get information about the vector database contents
    """
    try:
        # Get collection info from Qdrant
        collection_name = "textbook_content"

        # Check if Qdrant client is available
        if not qdrant_service.client:
            info = {
                "collection_name": collection_name,
                "vectors_count": 0,
                "indexed_vectors_count": 0,
                "config": None,
                "error": "Could not connect to Qdrant",
                "samples": []
            }
            return info

        try:
            collection_info = qdrant_service.client.get_collection(collection_name)

            info = {
                "collection_name": collection_name,
                "vectors_count": collection_info.points_count,
                "indexed_vectors_count": collection_info.indexed_vectors_count,
                "config": {
                    "vector_size": collection_info.config.params.vectors.size,
                    "distance": collection_info.config.params.vectors.distance
                }
            }
        except Exception as e:
            logger.error(f"Error getting collection info: {e}")
            info = {
                "collection_name": collection_name,
                "vectors_count": 0,
                "indexed_vectors_count": 0,
                "config": None,
                "error": f"Error accessing collection: {str(e)}",
                "samples": []
            }
            return info

        # Get some sample points from the collection
        try:
            # Get first 5 points as samples
            scroll_result = qdrant_service.client.scroll(
                collection_name=collection_name,
                limit=5
            )
            samples = []
            for point in scroll_result[0]:  # scroll_result[0] contains the points
                samples.append({
                    "id": point.id,
                    "content_preview": point.payload.get("content", "")[:100] + "..." if len(point.payload.get("content", "")) > 100 else point.payload.get("content", ""),
                    "title": point.payload.get("metadata", {}).get("title", ""),
                    "chapter_id": point.payload.get("metadata", {}).get("chapter_id", "")
                })
            info["samples"] = samples
        except Exception as e:
            logger.error(f"Error getting sample points: {e}")
            info["samples"] = []

        return info

    except Exception as e:
        logger.error(f"Error getting vector database info: {e}")
        raise HTTPException(status_code=500, detail="Internal server error getting vector database info")

@router.get("/vector-db-points")
async def get_vector_db_points(skip: int = 0, limit: int = 10, current_user: dict = Depends(get_current_user)):
    """
    Get points from the vector database with pagination
    """
    try:
        collection_name = "textbook_content"

        # Check if Qdrant client is available
        if not qdrant_service.client:
            return {
                "points": [],
                "total": 0,
                "skip": skip,
                "limit": limit,
                "error": "Could not connect to Qdrant"
            }

        try:
            # Get points from Qdrant with pagination
            scroll_result = qdrant_service.client.scroll(
                collection_name=collection_name,
                limit=limit,
                offset=skip
            )

            points = []
            for point in scroll_result[0]:  # scroll_result[0] contains the points
                points.append({
                    "id": point.id,
                    "content_preview": point.payload.get("content", "")[:200] + "..." if len(point.payload.get("content", "")) > 200 else point.payload.get("content", ""),
                    "title": point.payload.get("metadata", {}).get("title", ""),
                    "chapter_id": point.payload.get("metadata", {}).get("chapter_id", ""),
                    "score": getattr(point, 'score', None)  # score may not be present in scroll results
                })

            # Get total count
            collection_info = qdrant_service.client.get_collection(collection_name)
            total = collection_info.points_count

            return {
                "points": points,
                "total": total,
                "skip": skip,
                "limit": limit
            }
        except Exception as e:
            logger.error(f"Error getting vector database points: {e}")
            return {
                "points": [],
                "total": 0,
                "skip": skip,
                "limit": limit,
                "error": f"Error accessing vector database: {str(e)}"
            }

    except Exception as e:
        logger.error(f"Error getting vector database points: {e}")
        raise HTTPException(status_code=500, detail="Internal server error getting vector database points")