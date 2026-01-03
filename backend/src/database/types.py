"""
Database Types

Type definitions and abstract base classes for database operations.
"""

from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar
from sqlalchemy.ext.asyncio import AsyncSession

T = TypeVar("T")


class DatabaseAdapter(ABC):
    """
    Abstract Database Adapter

    Defines interface for database connections.
    Implementations: PostgreSQL, Supabase
    """

    @abstractmethod
    async def get_session(self) -> AsyncSession:
        """Get database session"""
        pass

    @abstractmethod
    async def close(self) -> None:
        """Close database connection"""
        pass

    @abstractmethod
    async def execute_raw(self, query: str, params: dict[str, Any] | None = None) -> Any:
        """Execute raw SQL query"""
        pass


class Repository(ABC, Generic[T]):
    """
    Abstract Repository Pattern

    Provides common CRUD operations with soft delete support.
    Subclass this for specific entity repositories.
    """

    def __init__(self, adapter: DatabaseAdapter):
        self.adapter = adapter

    @abstractmethod
    async def find_by_id(self, id: str, include_deleted: bool = False) -> T | None:
        """Find entity by ID"""
        pass

    @abstractmethod
    async def find_all(
        self, skip: int = 0, limit: int = 100, include_deleted: bool = False
    ) -> list[T]:
        """Find all entities with pagination"""
        pass

    @abstractmethod
    async def create(self, data: dict[str, Any]) -> T:
        """Create new entity"""
        pass

    @abstractmethod
    async def update(self, id: str, data: dict[str, Any]) -> T | None:
        """Update entity"""
        pass

    @abstractmethod
    async def soft_delete(self, id: str) -> T | None:
        """Soft delete entity (set deleted_at)"""
        pass

    @abstractmethod
    async def hard_delete(self, id: str) -> bool:
        """Hard delete entity (permanent)"""
        pass

    @abstractmethod
    async def restore(self, id: str) -> T | None:
        """Restore soft-deleted entity"""
        pass
