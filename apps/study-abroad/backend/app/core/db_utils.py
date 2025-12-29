"""
Database utility functions for RLS and user context
"""
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
import logging

logger = logging.getLogger(__name__)


async def set_rls_context(db: AsyncSession, user_id: UUID) -> None:
    """
    Set Row Level Security context for the current session.
    This enables RLS policies to filter data based on the authenticated user.

    Usage:
        await set_rls_context(db, user.id)
    """
    try:
        await db.execute(
            "SELECT set_user_context(:user_id)",
            {"user_id": str(user_id)}
        )
        logger.debug(f"RLS context set for user: {user_id}")
    except Exception as e:
        logger.error(f"Failed to set RLS context: {e}")
        raise


async def clear_rls_context(db: AsyncSession) -> None:
    """
    Clear Row Level Security context.
    Call this after operations that need elevated privileges.
    """
    try:
        await db.execute("SELECT set_config('app.user_id', '', false)")
        logger.debug("RLS context cleared")
    except Exception as e:
        logger.error(f"Failed to clear RLS context: {e}")
        raise


async def check_db_connection(db: AsyncSession) -> bool:
    """
    Check if database connection is healthy.
    Returns True if connected, False otherwise.
    """
    try:
        await db.execute("SELECT 1")
        return True
    except Exception as e:
        logger.error(f"Database connection check failed: {e}")
        return False
