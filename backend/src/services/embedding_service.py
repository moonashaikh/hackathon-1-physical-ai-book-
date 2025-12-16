"""
Embedding service for the RAG chatbot system.
Utilizes OpenAI embedding APIs with fallback to sentence transformers.
"""
import numpy as np
from typing import List, Union
import logging
import os
from dotenv import load_dotenv
import openai

load_dotenv()

logger = logging.getLogger(__name__)

class EmbeddingService:
    def __init__(self):
        # Initialize OpenAI API key
        openai.api_key = os.getenv("OPENAI_API_KEY")

        if not openai.api_key:
            logger.warning("OPENAI_API_KEY environment variable is not set")
            self.use_openai = False
        else:
            self.use_openai = True
            logger.info("OpenAI API key loaded successfully")

        # Fallback to sentence transformers if OpenAI is not available
        self.model = None
        if not self.use_openai:
            try:
                from sentence_transformers import SentenceTransformer
                model_name = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
                self.model = SentenceTransformer(model_name)
                logger.info(f"Loaded fallback embedding model: {model_name}")
            except ImportError:
                logger.warning("Sentence Transformers library not available, using mock embeddings")
                logger.info("Install sentence-transformers for fallback functionality: pip install sentence-transformers")
            except Exception as e:
                logger.warning(f"Could not load fallback embedding model: {e}")

    def generate_embedding(self, text: str) -> List[float]:
        """Generate embedding for a single text"""
        if self.use_openai:
            # Use OpenAI embeddings
            try:
                response = openai.embeddings.create(
                    input=text,
                    model="text-embedding-ada-002"  # OpenAI's recommended embedding model
                )
                embedding = response.data[0].embedding
                return embedding
            except Exception as e:
                logger.error(f"Error generating OpenAI embedding: {e}")
                logger.info("Falling back to sentence transformers or mock embeddings")

        # Fallback to sentence transformers
        if self.model is not None:
            try:
                embedding = self.model.encode([text])
                # Convert to list of floats for JSON serialization
                return embedding[0].tolist()
            except Exception as e:
                logger.error(f"Error generating embedding with sentence transformers: {e}")

        # Final fallback to mock embedding
        logger.warning("Embedding model is not available, returning mock embedding")
        # OpenAI embeddings are 1536-dimensional, so return that size for consistency
        return [0.0] * 1536

    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for multiple texts"""
        if self.use_openai:
            # Use OpenAI embeddings
            try:
                response = openai.embeddings.create(
                    input=texts,
                    model="text-embedding-ada-002"  # OpenAI's recommended embedding model
                )
                embeddings = [item.embedding for item in response.data]
                return embeddings
            except Exception as e:
                logger.error(f"Error generating OpenAI embeddings: {e}")
                logger.info("Falling back to sentence transformers or mock embeddings")

        # Fallback to sentence transformers
        if self.model is not None:
            try:
                embeddings = self.model.encode(texts)
                # Convert to list of lists of floats
                return [embedding.tolist() for embedding in embeddings]
            except Exception as e:
                logger.error(f"Error generating embeddings with sentence transformers: {e}")

        # Final fallback to mock embeddings
        logger.warning("Embedding model is not available, returning mock embeddings")
        # OpenAI embeddings are 1536-dimensional, so return that size for consistency
        return [[0.0] * 1536 for _ in texts]

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