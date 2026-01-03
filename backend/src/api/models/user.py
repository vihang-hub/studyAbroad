"""
User Pydantic models
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr


class User(BaseModel):
    """User model (synced with Clerk)"""

    id: str
    clerk_user_id: str
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    profile_image_url: Optional[str] = None
    auth_provider: str
    email_verified: bool = False
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    """Request to create a new user"""

    clerk_user_id: str
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    profile_image_url: Optional[str] = None
    auth_provider: str
    email_verified: bool = False


class UserProfile(BaseModel):
    """Public user profile"""

    user_id: str
    display_name: str
    email: EmailStr
    avatar_url: Optional[str] = None
    is_subscribed: bool = False
