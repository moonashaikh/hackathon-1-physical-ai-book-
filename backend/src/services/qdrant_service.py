from qdrant_client import QdrantClient
from qdrant_client.http import models
from typing import List, Dict, Optional
import logging
import os
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

class QdrantService:
    def __init__(self):
        self.url = os.getenv("QDRANT_URL", "http://localhost:6333")
        self.api_key = os.getenv("QDRANT_API_KEY")
        self.collection_name = "textbook_content"

        try:
            self.client = QdrantClient(
                url=self.url,
                api_key=self.api_key
            )
            self._ensure_collection_exists()
            logger.info("Successfully connected to Qdrant")
        except Exception as e:
            logger.warning(f"Could not connect to Qdrant at {self.url}: {e}")
            logger.info("Qdrant service will be unavailable until connection is established")
            self.client = None

    def _ensure_collection_exists(self):
        """Ensure the collection exists with proper configuration"""
        if self.client is None:
            logger.warning("Qdrant client is not available, skipping collection check")
            return

        try:
            # Check if collection exists
            self.client.get_collection(self.collection_name)
            logger.info(f"Collection '{self.collection_name}' already exists")
        except:
            # Create collection if it doesn't exist
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=models.VectorParams(size=384, distance=models.Distance.COSINE),  # Using all-MiniLM-L6-v2 which produces 384-dim vectors
            )
            logger.info(f"Created collection '{self.collection_name}'")

    def store_content(self, content_id: str, content: str, metadata: Dict = None):
        """Store content with its embedding in Qdrant"""
        if metadata is None:
            metadata = {}

        # We'll embed the content in the embedding_service, so for now just store the content
        # This method will be called after embedding is generated
        points = [
            models.PointStruct(
                id=content_id,
                vector=[],  # Will be filled in by embedding service
                payload={
                    "content": content,
                    "metadata": metadata
                }
            )
        ]

        # For now, we'll just return the structure - actual embedding happens elsewhere
        return points

    def search_similar(self, query_vector: List[float], limit: int = 5) -> List[Dict]:
        """Search for similar content based on the query vector"""
        if self.client is None:
            logger.warning("Qdrant client is not available, returning empty results")
            return []

        try:
            results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_vector,
                limit=limit
            )

            return [
                {
                    "id": result.id,
                    "content": result.payload.get("content", ""),
                    "metadata": result.payload.get("metadata", {}),
                    "score": result.score
                }
                for result in results
            ]
        except Exception as e:
            logger.error(f"Error searching in Qdrant: {e}")
            return []

    def get_content_by_id(self, content_id: str) -> Optional[Dict]:
        """Retrieve specific content by ID"""
        if self.client is None:
            logger.warning("Qdrant client is not available, returning None")
            return None

        try:
            records = self.client.retrieve(
                collection_name=self.collection_name,
                ids=[content_id]
            )

            if records:
                record = records[0]
                return {
                    "id": record.id,
                    "content": record.payload.get("content", ""),
                    "metadata": record.payload.get("metadata", {})
                }
            return None
        except Exception as e:
            logger.error(f"Error retrieving content from Qdrant: {e}")
            return None

# Global instance
qdrant_service = QdrantService()