"""
Authentication service (Clerk JWT verification)
"""

import jwt
from typing import Optional
from fastapi import HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()


def verify_clerk_token(credentials: HTTPAuthorizationCredentials = Security(security)) -> str:
    """
    Verify Clerk JWT token from Authorization header
    Returns the Clerk user ID if valid
    Raises HTTPException if invalid
    """
    token = credentials.credentials

    try:
        # Clerk uses RS256 algorithm with JWKS
        # For production, we should fetch the JWKS from Clerk and verify properly
        # For now, we'll do basic validation

        # Decode without verification for development
        # TODO: Implement proper JWKS verification for production
        payload = jwt.decode(
            token,
            options={"verify_signature": False},  # Development only!
        )

        clerk_user_id = payload.get("sub")
        if not clerk_user_id:
            raise HTTPException(status_code=401, detail="Invalid token: missing subject")

        return clerk_user_id

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")


async def get_current_user_id(
    credentials: HTTPAuthorizationCredentials = Security(security),
) -> str:
    """
    FastAPI dependency to get current user ID from JWT
    Usage: user_id: str = Depends(get_current_user_id)
    """
    return verify_clerk_token(credentials)


def validate_cron_secret(cron_secret: Optional[str]) -> bool:
    """
    Validate cron secret for scheduled jobs
    """
    # TODO: Add CRON_SECRET to EnvironmentConfig if needed
    # For now, accept any non-empty secret in dev mode
    return bool(cron_secret)
