import psycopg2
from psycopg2.extras import RealDictCursor
import logging
import os
from dotenv import load_dotenv
from typing import Dict, List, Optional

load_dotenv()

logger = logging.getLogger(__name__)

class PostgresService:
    def __init__(self):
        self.connection_string = os.getenv("NEON_POSTGRES_URL")
        if not self.connection_string:
            raise ValueError("NEON_POSTGRES_URL environment variable is not set")

        self._connection = None
        self._ensure_tables_exist()

    def get_connection(self):
        """Get database connection, creating one if needed"""
        if self._connection is None or self._connection.closed:
            try:
                self._connection = psycopg2.connect(
                    self.connection_string,
                    cursor_factory=RealDictCursor
                )
            except Exception as e:
                logger.error(f"Error connecting to PostgreSQL: {e}")
                raise
        return self._connection

    def _ensure_tables_exist(self):
        """Ensure the required tables exist in the database"""
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            # Create textbook_content table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS textbook_content (
                    id SERIAL PRIMARY KEY,
                    chapter_id VARCHAR(100) UNIQUE NOT NULL,
                    title VARCHAR(255) NOT NULL,
                    content TEXT NOT NULL,
                    content_embedding TEXT,  -- Store as JSON string
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)

            # Create chat_history table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS chat_history (
                    id SERIAL PRIMARY KEY,
                    session_id VARCHAR(100),
                    query TEXT NOT NULL,
                    response TEXT NOT NULL,
                    context_used TEXT,  -- What context was used for the response
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)

            conn.commit()
            logger.info("Database tables are ready")

        except Exception as e:
            logger.error(f"Error creating tables: {e}")
            conn.rollback()
            raise
        finally:
            cursor.close()

    def store_chapter(self, chapter_id: str, title: str, content: str, content_embedding: Optional[str] = None):
        """Store a chapter in the database"""
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                INSERT INTO textbook_content (chapter_id, title, content, content_embedding)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (chapter_id)
                DO UPDATE SET
                    title = EXCLUDED.title,
                    content = EXCLUDED.content,
                    content_embedding = EXCLUDED.content_embedding,
                    updated_at = CURRENT_TIMESTAMP
            """, (chapter_id, title, content, content_embedding))

            conn.commit()
            logger.info(f"Stored chapter {chapter_id}")

        except Exception as e:
            logger.error(f"Error storing chapter: {e}")
            conn.rollback()
            raise
        finally:
            cursor.close()

    def get_chapter_by_id(self, chapter_id: str) -> Optional[Dict]:
        """Retrieve a chapter by its ID"""
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
                "SELECT * FROM textbook_content WHERE chapter_id = %s",
                (chapter_id,)
            )
            result = cursor.fetchone()

            if result:
                return dict(result)
            return None

        except Exception as e:
            logger.error(f"Error retrieving chapter: {e}")
            return None
        finally:
            cursor.close()

    def get_all_chapters(self) -> List[Dict]:
        """Retrieve all chapters"""
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("SELECT * FROM textbook_content ORDER BY id")
            results = cursor.fetchall()

            return [dict(row) for row in results]

        except Exception as e:
            logger.error(f"Error retrieving chapters: {e}")
            return []
        finally:
            cursor.close()

    def store_chat_history(self, session_id: str, query: str, response: str, context_used: Optional[str] = None):
        """Store a chat interaction in history"""
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                INSERT INTO chat_history (session_id, query, response, context_used)
                VALUES (%s, %s, %s, %s)
            """, (session_id, query, response, context_used))

            conn.commit()

        except Exception as e:
            logger.error(f"Error storing chat history: {e}")
            conn.rollback()
            raise
        finally:
            cursor.close()

# Global instance
pg_service = PostgresService()