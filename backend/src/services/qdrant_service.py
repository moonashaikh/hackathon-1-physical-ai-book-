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
        try:
            qdrant_url = os.getenv("QDRANT_URL", "http://localhost:6333")
            qdrant_api_key = os.getenv("QDRANT_API_KEY")

            # For local Qdrant, API key is often not required
            if qdrant_api_key:
                self.client = QdrantClient(
                    url=qdrant_url,
                    api_key=qdrant_api_key
                )
            else:
                # Connect without API key (for local instance)
                self.client = QdrantClient(url=qdrant_url)

            self.collection_name = "textbook_content"
            self._ensure_collection_exists()
            logger.info("Successfully connected to Qdrant")
        except Exception as e:
            logger.warning(f"Could not connect to Qdrant: {e}")
            logger.info("Qdrant service will be unavailable until connection is established")
            self.client = None

    def _ensure_collection_exists(self):
        """Ensure the collection exists with proper configuration"""
        if self.client is None:
            logger.warning("Qdrant client is not available, skipping collection check")
            return

        try:
            # Check if collection exists
            collection_info = self.client.get_collection(self.collection_name)
            logger.info(f"Collection '{self.collection_name}' already exists")

            # Check if the vector size is correct (1536 for OpenAI embeddings)
            vector_size = collection_info.config.params.vectors.size
            if vector_size != 1536:
                logger.warning(f"Collection vector size is {vector_size}, expected 1536 for OpenAI embeddings. "
                              f"Consider recreating the collection for optimal performance.")
        except:
            # Create collection if it doesn't exist - using 1536 dimensions for OpenAI embeddings
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=models.VectorParams(size=1536, distance=models.Distance.COSINE),  # Using OpenAI embeddings which produce 1536-dim vectors
            )
            logger.info(f"Created collection '{self.collection_name}' with 1536-dimensional vectors")

    def store_content(self, content_id: str, content: str, embedding: List[float], metadata: Dict = None):
        """Store content with its embedding in Qdrant"""
        if self.client is None:
            logger.warning("Qdrant client is not available, skipping store content operation")
            return False

        if metadata is None:
            metadata = {}

        try:
            points = [
                models.PointStruct(
                    id=content_id,
                    vector=embedding,
                    payload={
                        "content": content,
                        "metadata": metadata
                    }
                )
            ]

            # Store the point in Qdrant
            self.client.upsert(
                collection_name=self.collection_name,
                points=points
            )

            logger.info(f"Stored content with ID {content_id} in Qdrant")
            return True
        except Exception as e:
            logger.error(f"Error storing content in Qdrant: {e}")
            return False

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