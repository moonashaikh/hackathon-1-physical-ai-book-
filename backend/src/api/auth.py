from fastapi import APIRouter, HTTPException, Depends, status, Request
from pydantic import BaseModel
from typing import Optional
from datetime import timedelta
from src.services.auth_service import auth_service
import os

router = APIRouter(prefix="/auth", tags=["auth"])

# Pydantic models
class UserLogin(BaseModel):
    email: str
    password: str

class UserSignup(BaseModel):
    email: str
    password: str
    software_background: str
    hardware_background: str
    primary_interest: str

class Token(BaseModel):
    access_token: str
    token_type: str

class UserProfile(BaseModel):
    email: str
    software_background: Optional[str] = None
    hardware_background: Optional[str] = None
    primary_interest: Optional[str] = None


@router.post("/signup", response_model=Token)
async def signup(user_data: UserSignup):
    """Create a new user account"""
    # Validate background data
    valid_software_backgrounds = ["beginner", "intermediate", "advanced"]
    valid_hardware_backgrounds = ["none", "basic electronics", "robotics", "embedded systems"]
    valid_primary_interests = ["AI", "Robotics", "Web", "Hardware", "Mixed"]

    if user_data.software_background not in valid_software_backgrounds:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid software background"
        )

    if user_data.hardware_background not in valid_hardware_backgrounds:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid hardware background"
        )

    if user_data.primary_interest not in valid_primary_interests:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid primary interest"
        )

    # Check if user already exists
    from src.services.pg_service import pg_service
    conn = pg_service.get_connection()
    if conn:
        import psycopg2.extras
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        try:
            cursor.execute(
                "SELECT id FROM users WHERE email = %s",
                (user_data.email,)
            )
            existing_user = cursor.fetchone()
            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="User with this email already exists"
                )
        finally:
            cursor.close()
    else:
        # Fallback to mock database
        from src.services.mock_db_service import mock_db_service
        existing_user = mock_db_service.get_user_by_email(user_data.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this email already exists"
            )

    # Create user with profile
    profile_data = {
        'software_background': user_data.software_background,
        'hardware_background': user_data.hardware_background,
        'primary_interest': user_data.primary_interest
    }

    user = auth_service.create_user(
        email=user_data.email,
        password=user_data.password,
        profile_data=profile_data
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create user"
        )

    # Create access token
    access_token_expires = timedelta(minutes=30)
    access_token = auth_service.create_access_token(
        data={"sub": str(user['id'])},
        expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/signin", response_model=Token)
async def signin(user_credentials: UserLogin):
    """Authenticate user and return access token"""
    user = auth_service.authenticate_user(
        email=user_credentials.email,
        password=user_credentials.password
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create access token
    access_token_expires = timedelta(minutes=30)
    access_token = auth_service.create_access_token(
        data={"sub": str(user['id'])},
        expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}


async def get_current_user(request: Request):
    """Dependency to get current user from token in Authorization header"""
    authorization = request.headers.get("Authorization")
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = authorization[7:]  # Remove "Bearer " prefix
    payload = auth_service.verify_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return int(user_id)


@router.get("/profile", response_model=UserProfile)
async def get_profile(current_user_id: int = Depends(get_current_user)):
    """Get current user's profile"""
    user_profile = auth_service.get_user_profile(current_user_id)
    if not user_profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User profile not found"
        )

    return UserProfile(
        email=user_profile['email'],
        software_background=user_profile['software_background'],
        hardware_background=user_profile['hardware_background'],
        primary_interest=user_profile['primary_interest']
    )