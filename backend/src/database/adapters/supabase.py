"""
Supabase Database Adapter

Supabase PostgreSQL implementation for test and production modes.
"""

from typing import Any
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker,
    AsyncEngine,
)
from sqlalchemy import text
from database.types import DatabaseAdapter


class SupabaseAdapter(DatabaseAdapter):
    """
    Supabase Database Adapter

    Connects to Supabase PostgreSQL database for test/production.
    Uses service role key to bypass Row Level Security (RLS).
    """

    def __init__(
        self,
        database_url: str,
        service_role_key: str,
        pool_size: int = 20,
        pool_timeout: int = 30,
    ):
        """
        Initialize Supabase adapter

        Args:
            database_url: Supabase connection string
            service_role_key: Supabase service role key (bypasses RLS)
            pool_size: Maximum connection pool size
            pool_timeout: Connection timeout in seconds
        """
        self.database_url = database_url
        self.service_role_key = service_role_key

        # Create async engine with Supabase connection
        self.engine: AsyncEngine = create_async_engine(
            database_url,
            pool_size=pool_size,
            max_overflow=10,
            pool_timeout=pool_timeout,
            echo=False,
        )

        self.session_maker = async_sessionmaker(
            self.engine, class_=AsyncSession, expire_on_commit=False
        )

    async def get_session(self) -> AsyncSession:
        """
        Get database session

        Returns:
            AsyncSession instance
        """
        return self.session_maker()

    async def close(self) -> None:
        """Close database connection pool"""
        await self.engine.dispose()

    async def execute_raw(self, query: str, params: dict[str, Any] | None = None) -> Any:
        """
        Execute raw SQL query

        Args:
            query: SQL query string
            params: Query parameters

        Returns:
            Query result
        """
        async with self.session_maker() as session:
            result = await session.execute(text(query), params or {})
            await session.commit()
            return result
