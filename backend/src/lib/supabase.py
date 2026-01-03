"""
Supabase client for backend (Python)
Service role access for server-side operations
"""

from typing import Optional
from supabase import create_client, Client
from src.config import settings

# Global Supabase client with service role key (full access)
_supabase_client: Optional[Client] = None


def get_supabase() -> Client:
    """
    Get Supabase client instance with service role key
    This client has full access and bypasses RLS policies
    """
    global _supabase_client

    if _supabase_client is None:
        _supabase_client = create_client(settings.SUPABASE_URL, settings.SUPABASE_SERVICE_ROLE_KEY)

    return _supabase_client


def get_supabase_anon() -> Client:
    """
    Get Supabase client with anon key (respects RLS policies)
    Use this when you want to enforce Row Level Security
    """
    return create_client(settings.SUPABASE_URL, settings.SUPABASE_ANON_KEY)
