"""
User Repository

Repository for User model with CRUD operations.
"""

from typing import Any
from sqlalchemy import select
from database.types import Repository, DatabaseAdapter
from database.models.user import User


class UserRepository(Repository[User]):
    """
    User Repository

    Provides CRUD operations for User model.
    Note: Users don't have soft delete, but we maintain consistency with interface.
    """

    def __init__(self, adapter: DatabaseAdapter):
        super().__init__(adapter)

    async def find_by_id(self, id: str, include_deleted: bool = False) -> User | None:
        """
        Find user by ID

        Args:
            id: User UUID
            include_deleted: Ignored for users (no soft delete)

        Returns:
            User instance or None
        """
        async with await self.adapter.get_session() as session:
            result = await session.execute(select(User).where(User.user_id == id))
            return result.scalar_one_or_none()

    async def find_by_clerk_id(self, clerk_user_id: str) -> User | None:
        """
        Find user by Clerk user ID

        Args:
            clerk_user_id: Clerk's unique identifier

        Returns:
            User instance or None
        """
        async with await self.adapter.get_session() as session:
            result = await session.execute(select(User).where(User.clerk_user_id == clerk_user_id))
            return result.scalar_one_or_none()

    async def find_by_email(self, email: str) -> User | None:
        """
        Find user by email

        Args:
            email: User's email address

        Returns:
            User instance or None
        """
        async with await self.adapter.get_session() as session:
            result = await session.execute(select(User).where(User.email == email))
            return result.scalar_one_or_none()

    async def find_all(
        self, skip: int = 0, limit: int = 100, include_deleted: bool = False
    ) -> list[User]:
        """
        Find all users with pagination

        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            include_deleted: Ignored for users

        Returns:
            List of User instances
        """
        async with await self.adapter.get_session() as session:
            result = await session.execute(select(User).offset(skip).limit(limit))
            return list(result.scalars().all())

    async def create(self, data: dict[str, Any]) -> User:
        """
        Create new user

        Args:
            data: User data dictionary

        Returns:
            Created User instance
        """
        async with await self.adapter.get_session() as session:
            user = User(**data)
            session.add(user)
            await session.commit()
            await session.refresh(user)
            return user

    async def update(self, id: str, data: dict[str, Any]) -> User | None:
        """
        Update user

        Args:
            id: User UUID
            data: Updated data dictionary

        Returns:
            Updated User instance or None
        """
        async with await self.adapter.get_session() as session:
            user = await self.find_by_id(id)
            if not user:
                return None

            for key, value in data.items():
                if hasattr(user, key):
                    setattr(user, key, value)

            session.add(user)
            await session.commit()
            await session.refresh(user)
            return user

    async def soft_delete(self, id: str) -> User | None:
        """
        Soft delete not applicable for users

        Args:
            id: User UUID

        Returns:
            None (not implemented)
        """
        # Users don't support soft delete in this implementation
        return None

    async def hard_delete(self, id: str) -> bool:
        """
        Hard delete user (permanent)

        Args:
            id: User UUID

        Returns:
            True if deleted, False otherwise
        """
        async with await self.adapter.get_session() as session:
            user = await self.find_by_id(id)
            if not user:
                return False

            await session.delete(user)
            await session.commit()
            return True

    async def restore(self, id: str) -> User | None:
        """
        Restore not applicable for users

        Args:
            id: User UUID

        Returns:
            None (not implemented)
        """
        # Users don't support soft delete
        return None
