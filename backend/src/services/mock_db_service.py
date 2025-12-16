import logging
import sqlite3
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from contextlib import contextmanager
from passlib.context import CryptContext

logger = logging.getLogger(__name__)

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class MockDBService:
    """Mock database service for testing authentication functionality without PostgreSQL"""

    def __init__(self, db_path: str = "test_auth.db"):
        self.db_path = db_path
        self.init_db()

    def init_db(self):
        """Initialize the mock database with required tables"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Create users table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    email TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Create user_profiles table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_profiles (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    software_background TEXT,
                    hardware_background TEXT,
                    primary_interest TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
                )
            """)

            conn.commit()
            logger.info(f"Database tables initialized successfully in {self.db_path}")
        except Exception as e:
            logger.error(f"Error initializing database: {e}")
        finally:
            if conn:
                conn.close()

    @contextmanager
    def get_connection(self):
        """Context manager to get database connection"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # This allows accessing columns by name
        try:
            yield conn
        finally:
            conn.close()

    def create_user(self, email: str, password_hash: str) -> Optional[Dict[str, Any]]:
        """Create a new user in the mock database"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("""
                    INSERT INTO users (email, password_hash)
                    VALUES (?, ?)
                """, (email, password_hash))

                user_id = cursor.lastrowid
                conn.commit()

                return {
                    'id': user_id,
                    'email': email
                }
            except sqlite3.IntegrityError:
                # Email already exists
                return None
            except Exception as e:
                logger.error(f"Error creating user: {e}")
                return None

    def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Get a user by email from the mock database"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, email, password_hash FROM users WHERE email = ?
            """, (email,))

            row = cursor.fetchone()
            if row:
                return {
                    'id': row['id'],
                    'email': row['email'],
                    'password_hash': row['password_hash']
                }
            return None

    def create_user_profile(self, user_id: int, profile_data: Dict[str, str]) -> bool:
        """Create a user profile in the mock database"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("""
                    INSERT INTO user_profiles (
                        user_id, software_background, hardware_background, primary_interest
                    ) VALUES (?, ?, ?, ?)
                """, (
                    user_id,
                    profile_data.get('software_background'),
                    profile_data.get('hardware_background'),
                    profile_data.get('primary_interest')
                ))

                conn.commit()
                return True
            except Exception as e:
                logger.error(f"Error creating user profile: {e}")
                return False

    def get_user_profile(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Get user profile from the mock database"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT
                    u.email,
                    up.software_background,
                    up.hardware_background,
                    up.primary_interest
                FROM users u
                JOIN user_profiles up ON u.id = up.user_id
                WHERE u.id = ?
            """, (user_id,))

            row = cursor.fetchone()
            if row:
                return {
                    'email': row['email'],
                    'software_background': row['software_background'],
                    'hardware_background': row['hardware_background'],
                    'primary_interest': row['primary_interest']
                }
            return None

# Global instance
mock_db_service = MockDBService()