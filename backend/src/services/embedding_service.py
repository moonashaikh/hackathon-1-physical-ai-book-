from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List, Union
import logging
import os
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

class EmbeddingService:
    def __init__(self):
        model_name = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
        self.model = SentenceTransformer(model_name)
        logger.info(f"Loaded embedding model: {model_name}")

    def generate_embedding(self, text: str) -> List[float]:
        """Generate embedding for a single text"""
        try:
            embedding = self.model.encode([text])
            # Convert to list of floats for JSON serialization
            return embedding[0].tolist()
        except Exception as e:
            logger.error(f"Error generating embedding: {e}")
            raise

    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for multiple texts"""
        try:
            embeddings = self.model.encode(texts)
            # Convert to list of lists of floats
            return [embedding.tolist() for embedding in embeddings]
        except Exception as e:
            logger.error(f"Error generating embeddings: {e}")
            raise

    def cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """Calculate cosine similarity between two vectors"""
        try:
            # Convert to numpy arrays
            v1 = np.array(vec1)
            v2 = np.array(vec2)

            # Calculate cosine similarity
            dot_product = np.dot(v1, v2)
            norm_v1 = np.linalg.norm(v1)
            norm_v2 = np.linalg.norm(v2)

            if norm_v1 == 0 or norm_v2 == 0:
                return 0.0

            return float(dot_product / (norm_v1 * norm_v2))
        except Exception as e:
            logger.error(f"Error calculating cosine similarity: {e}")
            return 0.0

# Global instance
embedding_service = EmbeddingService()