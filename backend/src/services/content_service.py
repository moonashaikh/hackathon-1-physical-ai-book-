from typing import List, Dict, Optional
import logging
import hashlib
from src.services.qdrant_service import qdrant_service
from src.services.pg_service import pg_service
from src.services.embedding_service import embedding_service

logger = logging.getLogger(__name__)

class ContentService:
    def __init__(self):
        self.qdrant = qdrant_service
        self.pg = pg_service
        self.embedding = embedding_service

    def generate_content_id(self, content: str, chapter_id: str = None) -> str:
        """Generate a unique ID for content"""
        content_hash = hashlib.md5(content.encode()).hexdigest()
        if chapter_id:
            return f"{chapter_id}_{content_hash[:8]}"
        return content_hash

    def store_textbook_content(self, chapter_id: str, title: str, content: str, content_id: str = None) -> bool:
        """
        Store textbook content in both Qdrant (for vector search) and PostgreSQL (for metadata)
        """
        try:
            # Generate content ID if not provided
            if content_id is None:
                content_id = self.generate_content_id(content, chapter_id)

            # Generate embedding for the content
            content_embedding = self.embedding.generate_embedding(content)

            # Store in Qdrant for vector search
            qdrant_success = self.qdrant.store_content(
                content_id=content_id,
                content=content,
                embedding=content_embedding,
                metadata={
                    "chapter_id": chapter_id,
                    "title": title,
                    "type": "textbook_content"
                }
            )

            # Store in PostgreSQL for metadata
            self.pg.store_chapter(
                chapter_id=chapter_id,
                title=title,
                content=content,
                content_embedding=str(content_embedding)  # Store as string for now
            )

            if qdrant_success:
                logger.info(f"Successfully stored textbook content: {chapter_id}")
                return True
            else:
                logger.error(f"Failed to store content in Qdrant: {chapter_id}")
                return False

        except Exception as e:
            logger.error(f"Error storing textbook content: {e}")
            return False

    def store_textbook_chapters(self, chapters: List[Dict]) -> Dict[str, bool]:
        """
        Store multiple textbook chapters at once
        Each chapter dict should have: id, title, content
        """
        results = {}

        for chapter in chapters:
            chapter_id = chapter.get("id")
            title = chapter.get("title")
            content = chapter.get("content")

            if not all([chapter_id, title, content]):
                logger.warning(f"Skipping chapter with missing data: {chapter_id}")
                results[chapter_id] = False
                continue

            success = self.store_textbook_content(
                chapter_id=chapter_id,
                title=title,
                content=content
            )
            results[chapter_id] = success

        return results

# Global instance
content_service = ContentService()