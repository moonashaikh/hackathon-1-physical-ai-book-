from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from src.services.auth_service import auth_service

security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Dependency to get current user from JWT token
    Compatible with both the original auth and Better Auth implementations
    """
    token = credentials.credentials
    payload = auth_service.verify_token(token)

    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    user_id = payload.get("user_id")
    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid token: no user ID")

    # Get user profile information
    user_profile = auth_service.get_user_profile(user_id)
    if user_profile is None:
        raise HTTPException(status_code=401, detail="User not found")

    return {
        "id": user_id,
        "email": user_profile["email"],
        "software_background": user_profile.get("software_background"),
        "hardware_background": user_profile.get("hardware_background"),
        "primary_interest": user_profile.get("primary_interest")
    }