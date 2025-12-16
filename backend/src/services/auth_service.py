import logging
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from passlib.context import CryptContext
from jose import JWTError, jwt
import os
from dotenv import load_dotenv
from src.services.pg_service import pg_service

# Import mock database service for fallback
from src.services.mock_db_service import mock_db_service

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT configuration
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class AuthService:
    def __init__(self):
        self.pwd_context = pwd_context
        self.secret_key = SECRET_KEY
        self.algorithm = ALGORITHM

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a plain password against a hashed password"""
        return pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str) -> str:
        """Hash a plain password"""
        return pwd_context.hash(password)

    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """Create a JWT access token"""
        to_encode = data.copy()

        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt

    def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Verify a JWT token and return the payload if valid"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except JWTError as e:
            logger.error(f"Token verification failed: {e}")
            return None

    def authenticate_user(self, email: str, password: str) -> Optional[Dict]:
        """Authenticate a user by email and password"""
        # Try PostgreSQL first
        conn = pg_service.get_connection()
        if conn is not None:
            cursor = conn.cursor()

            try:
                cursor.execute(
                    "SELECT id, email, password_hash FROM users WHERE email = %s",
                    (email,)
                )
                user = cursor.fetchone()

                if user and self.verify_password(password, user['password_hash']):
                    return {
                        'id': user['id'],
                        'email': user['email']
                    }
                return None

            except Exception as e:
                logger.error(f"Error authenticating user with PostgreSQL: {e}")
                return None
            finally:
                cursor.close()
        else:
            # Fallback to mock database
            user = mock_db_service.get_user_by_email(email)
            if user and self.verify_password(password, user['password_hash']):
                return {
                    'id': user['id'],
                    'email': user['email']
                }
            return None

    def create_user(self, email: str, password: str, profile_data: Dict) -> Optional[Dict]:
        """Create a new user with profile data"""
        # Try PostgreSQL first
        conn = pg_service.get_connection()
        if conn is not None:
            cursor = conn.cursor()

            try:
                # Hash the password
                hashed_password = self.get_password_hash(password)

                # Start transaction
                conn.autocommit = False

                # Insert user
                cursor.execute("""
                    INSERT INTO users (email, password_hash)
                    VALUES (%s, %s)
                    RETURNING id, email
                """, (email, hashed_password))

                user = cursor.fetchone()

                # Insert user profile
                cursor.execute("""
                    INSERT INTO user_profiles (
                        user_id,
                        software_background,
                        hardware_background,
                        primary_interest
                    )
                    VALUES (%s, %s, %s, %s)
                """, (
                    user['id'],
                    profile_data.get('software_background'),
                    profile_data.get('hardware_background'),
                    profile_data.get('primary_interest')
                ))

                conn.commit()
                conn.autocommit = True

                logger.info(f"User created successfully: {user['email']}")
                return {
                    'id': user['id'],
                    'email': user['email']
                }

            except Exception as e:
                logger.error(f"Error creating user: {e}")
                conn.rollback()
                conn.autocommit = True
                return None
            finally:
                cursor.close()
        else:
            # Fallback to mock database
            hashed_password = self.get_password_hash(password)

            user = mock_db_service.create_user(email, hashed_password)
            if user:
                profile_success = mock_db_service.create_user_profile(user['id'], profile_data)
                if profile_success:
                    logger.info(f"User created successfully in mock DB: {user['email']}")
                    return user
            return None

    def get_user_profile(self, user_id: int) -> Optional[Dict]:
        """Get user profile information"""
        # Try PostgreSQL first
        conn = pg_service.get_connection()
        if conn is not None:
            cursor = conn.cursor()

            try:
                cursor.execute("""
                    SELECT
                        u.email,
                        up.software_background,
                        up.hardware_background,
                        up.primary_interest
                    FROM users u
                    JOIN user_profiles up ON u.id = up.user_id
                    WHERE u.id = %s
                """, (user_id,))

                result = cursor.fetchone()

                if result:
                    return {
                        'email': result['email'],
                        'software_background': result['software_background'],
                        'hardware_background': result['hardware_background'],
                        'primary_interest': result['primary_interest']
                    }
                return None

            except Exception as e:
                logger.error(f"Error retrieving user profile: {e}")
                return None
            finally:
                cursor.close()
        else:
            # Fallback to mock database
            return mock_db_service.get_user_profile(user_id)

    def update_user_profile(self, user_id: int, profile_data: Dict) -> bool:
        """Update user profile information"""
        # Try PostgreSQL first
        conn = pg_service.get_connection()
        if conn is not None:
            cursor = conn.cursor()

            try:
                cursor.execute("""
                    UPDATE user_profiles
                    SET
                        software_background = %s,
                        hardware_background = %s,
                        primary_interest = %s,
                        updated_at = CURRENT_TIMESTAMP
                    WHERE user_id = %s
                """, (
                    profile_data.get('software_background'),
                    profile_data.get('hardware_background'),
                    profile_data.get('primary_interest'),
                    user_id
                ))

                conn.commit()
                return cursor.rowcount > 0

            except Exception as e:
                logger.error(f"Error updating user profile: {e}")
                conn.rollback()
                return False
            finally:
                cursor.close()
        else:
            # For mock database, we don't implement update functionality
            # This is a limitation of the mock implementation
            logger.warning("Update user profile not implemented for mock database")
            return False


# Global instance
auth_service = AuthService()