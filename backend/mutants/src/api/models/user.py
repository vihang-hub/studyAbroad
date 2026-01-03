"""
User Pydantic models
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr
from inspect import signature as _mutmut_signature
from typing import Annotated
from typing import Callable
from typing import ClassVar


MutantDict = Annotated[dict[str, Callable], "Mutant"]


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg = None):
    """Forward call to original or mutated function, depending on the environment"""
    import os
    mutant_under_test = os.environ['MUTANT_UNDER_TEST']
    if mutant_under_test == 'fail':
        from mutmut.__main__ import MutmutProgrammaticFailException
        raise MutmutProgrammaticFailException('Failed programmatically')      
    elif mutant_under_test == 'stats':
        from mutmut.__main__ import record_trampoline_hit
        record_trampoline_hit(orig.__module__ + '.' + orig.__name__)
        result = orig(*call_args, **call_kwargs)
        return result
    prefix = orig.__module__ + '.' + orig.__name__ + '__mutmut_'
    if not mutant_under_test.startswith(prefix):
        result = orig(*call_args, **call_kwargs)
        return result
    mutant_name = mutant_under_test.rpartition('.')[-1]
    if self_arg is not None:
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs)
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs)
    return result


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
