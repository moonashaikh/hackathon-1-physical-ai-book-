from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import Optional
from src.services.auth_service import auth_service
import json

router = APIRouter(prefix="/auth", tags=["auth"])

# Models for Better Auth compatibility
class SignUpRequest(BaseModel):
    email: str
    password: str
    software_background: Optional[str] = None
    hardware_background: Optional[str] = None
    primary_interest: Optional[str] = None

class SignInRequest(BaseModel):
    email: str
    password: str

class BetterAuthResponse(BaseModel):
    session: Optional[dict] = None
    user: Optional[dict] = None
    error: Optional[dict] = None

security = HTTPBearer()

@router.post("/sign-up")
async def better_auth_signup(request: SignUpRequest):
    """Better Auth compatible signup endpoint"""
    try:
        # Validate background data like in the original auth
        valid_software_backgrounds = ["beginner", "intermediate", "advanced"]
        valid_hardware_backgrounds = ["none", "basic electronics", "robotics", "embedded systems"]
        valid_primary_interests = ["AI", "Robotics", "Web", "Hardware", "Mixed"]

        if request.software_background not in valid_software_backgrounds:
            raise HTTPException(
                status_code=400,
                detail="Invalid software background"
            )

        if request.hardware_background not in valid_hardware_backgrounds:
            raise HTTPException(
                status_code=400,
                detail="Invalid hardware background"
            )

        if request.primary_interest not in valid_primary_interests:
            raise HTTPException(
                status_code=400,
                detail="Invalid primary interest"
            )

        # Check if user already exists (similar to original auth)
        from src.services.pg_service import pg_service
        conn = pg_service.get_connection()
        if conn:
            import psycopg2.extras
            cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            try:
                cursor.execute(
                    "SELECT id FROM users WHERE email = %s",
                    (request.email,)
                )
                existing_user = cursor.fetchone()
                if existing_user:
                    raise HTTPException(
                        status_code=400,
                        detail="User with this email already exists"
                    )
            finally:
                cursor.close()
        else:
            # Fallback to mock database
            from src.services.mock_db_service import mock_db_service
            existing_user = mock_db_service.get_user_by_email(request.email)
            if existing_user:
                raise HTTPException(
                    status_code=400,
                    detail="User with this email already exists"
                )

        # Prepare profile data for the existing auth service
        profile_data = {
            'software_background': request.software_background,
            'hardware_background': request.hardware_background,
            'primary_interest': request.primary_interest
        }

        # Use existing auth service
        user = auth_service.create_user(
            request.email,
            request.password,
            profile_data
        )

        if user:
            # Create session token
            token = auth_service.create_access_token(data={"sub": user['email'], "user_id": user['id']})
            return {
                "session": {"token": token, "expiresAt": "30min"},  # Simplified
                "user": {"id": user['id'], "email": user['email']},
                "status": "success"
            }
        else:
            raise HTTPException(status_code=400, detail="Signup failed")
    except HTTPException:
        # Re-raise HTTP exceptions as they are
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/sign-in")
async def better_auth_signin(request: SignInRequest):
    """Better Auth compatible signin endpoint"""
    try:
        user = auth_service.authenticate_user(request.email, request.password)
        if user:
            token = auth_service.create_access_token(data={"sub": user['email'], "user_id": user['id']})
            return {
                "session": {"token": token, "expiresAt": "30min"},
                "user": {"id": user['id'], "email": user['email']},
                "status": "success"
            }
        else:
            raise HTTPException(status_code=401, detail="Invalid credentials")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/get-session")
async def better_auth_get_session(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Better Auth compatible get session endpoint"""
    token = credentials.credentials
    payload = auth_service.verify_token(token)

    if payload:
        user_id = payload.get("user_id")
        user_profile = auth_service.get_user_profile(user_id)
        if user_profile:
            return {
                "user": {
                    "id": user_id,
                    "email": user_profile['email'],
                    "software_background": user_profile.get('software_background'),
                    "hardware_background": user_profile.get('hardware_background'),
                    "primary_interest": user_profile.get('primary_interest')
                },
                "session": {"token": token, "expiresAt": "30min"}
            }

    return {"user": None, "session": None}

@router.post("/sign-out")
async def better_auth_signout():
    """Better Auth compatible signout endpoint"""
    return {"status": "success"}