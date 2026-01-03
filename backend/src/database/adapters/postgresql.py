"""
PostgreSQL Database Adapter

Local PostgreSQL implementation for development mode.
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


class PostgreSQLAdapter(DatabaseAdapter):
    """
    PostgreSQL Database Adapter

    Connects to local PostgreSQL database for development.
    Uses asyncpg driver for async operations.
    """

    def __init__(self, database_url: str, pool_size: int = 20, pool_timeout: int = 30):
        """
        Initialize PostgreSQL adapter

        Args:
            database_url: PostgreSQL connection string
            pool_size: Maximum connection pool size
            pool_timeout: Connection timeout in seconds
        """
        self.database_url = database_url
        self.engine: AsyncEngine = create_async_engine(
            database_url,
            pool_size=pool_size,
            max_overflow=10,
            pool_timeout=pool_timeout,
            echo=False,  # Set to True for SQL logging
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
