"""
User Repository

Repository for User model with CRUD operations.
"""

from typing import Any
from sqlalchemy import select
from database.types import Repository, DatabaseAdapter
from database.models.user import User
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


class UserRepository(Repository[User]):
    """
    User Repository

    Provides CRUD operations for User model.
    Note: Users don't have soft delete, but we maintain consistency with interface.
    """

    def xǁUserRepositoryǁ__init____mutmut_orig(self, adapter: DatabaseAdapter):
        super().__init__(adapter)

    def xǁUserRepositoryǁ__init____mutmut_1(self, adapter: DatabaseAdapter):
        super().__init__(None)
    
    xǁUserRepositoryǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁUserRepositoryǁ__init____mutmut_1': xǁUserRepositoryǁ__init____mutmut_1
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁUserRepositoryǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁUserRepositoryǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁUserRepositoryǁ__init____mutmut_orig)
    xǁUserRepositoryǁ__init____mutmut_orig.__name__ = 'xǁUserRepositoryǁ__init__'

    async def xǁUserRepositoryǁfind_by_id__mutmut_orig(self, id: str, include_deleted: bool = False) -> User | None:
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

    async def xǁUserRepositoryǁfind_by_id__mutmut_1(self, id: str, include_deleted: bool = True) -> User | None:
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

    async def xǁUserRepositoryǁfind_by_id__mutmut_2(self, id: str, include_deleted: bool = False) -> User | None:
        """
        Find user by ID

        Args:
            id: User UUID
            include_deleted: Ignored for users (no soft delete)

        Returns:
            User instance or None
        """
        async with await self.adapter.get_session() as session:
            result = None
            return result.scalar_one_or_none()

    async def xǁUserRepositoryǁfind_by_id__mutmut_3(self, id: str, include_deleted: bool = False) -> User | None:
        """
        Find user by ID

        Args:
            id: User UUID
            include_deleted: Ignored for users (no soft delete)

        Returns:
            User instance or None
        """
        async with await self.adapter.get_session() as session:
            result = await session.execute(None)
            return result.scalar_one_or_none()

    async def xǁUserRepositoryǁfind_by_id__mutmut_4(self, id: str, include_deleted: bool = False) -> User | None:
        """
        Find user by ID

        Args:
            id: User UUID
            include_deleted: Ignored for users (no soft delete)

        Returns:
            User instance or None
        """
        async with await self.adapter.get_session() as session:
            result = await session.execute(select(User).where(None))
            return result.scalar_one_or_none()

    async def xǁUserRepositoryǁfind_by_id__mutmut_5(self, id: str, include_deleted: bool = False) -> User | None:
        """
        Find user by ID

        Args:
            id: User UUID
            include_deleted: Ignored for users (no soft delete)

        Returns:
            User instance or None
        """
        async with await self.adapter.get_session() as session:
            result = await session.execute(select(None).where(User.user_id == id))
            return result.scalar_one_or_none()

    async def xǁUserRepositoryǁfind_by_id__mutmut_6(self, id: str, include_deleted: bool = False) -> User | None:
        """
        Find user by ID

        Args:
            id: User UUID
            include_deleted: Ignored for users (no soft delete)

        Returns:
            User instance or None
        """
        async with await self.adapter.get_session() as session:
            result = await session.execute(select(User).where(User.user_id != id))
            return result.scalar_one_or_none()
    
    xǁUserRepositoryǁfind_by_id__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁUserRepositoryǁfind_by_id__mutmut_1': xǁUserRepositoryǁfind_by_id__mutmut_1, 
        'xǁUserRepositoryǁfind_by_id__mutmut_2': xǁUserRepositoryǁfind_by_id__mutmut_2, 
        'xǁUserRepositoryǁfind_by_id__mutmut_3': xǁUserRepositoryǁfind_by_id__mutmut_3, 
        'xǁUserRepositoryǁfind_by_id__mutmut_4': xǁUserRepositoryǁfind_by_id__mutmut_4, 
        'xǁUserRepositoryǁfind_by_id__mutmut_5': xǁUserRepositoryǁfind_by_id__mutmut_5, 
        'xǁUserRepositoryǁfind_by_id__mutmut_6': xǁUserRepositoryǁfind_by_id__mutmut_6
    }
    
    def find_by_id(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁUserRepositoryǁfind_by_id__mutmut_orig"), object.__getattribute__(self, "xǁUserRepositoryǁfind_by_id__mutmut_mutants"), args, kwargs, self)
        return result 
    
    find_by_id.__signature__ = _mutmut_signature(xǁUserRepositoryǁfind_by_id__mutmut_orig)
    xǁUserRepositoryǁfind_by_id__mutmut_orig.__name__ = 'xǁUserRepositoryǁfind_by_id'

    async def xǁUserRepositoryǁfind_by_clerk_id__mutmut_orig(self, clerk_user_id: str) -> User | None:
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

    async def xǁUserRepositoryǁfind_by_clerk_id__mutmut_1(self, clerk_user_id: str) -> User | None:
        """
        Find user by Clerk user ID

        Args:
            clerk_user_id: Clerk's unique identifier

        Returns:
            User instance or None
        """
        async with await self.adapter.get_session() as session:
            result = None
            return result.scalar_one_or_none()

    async def xǁUserRepositoryǁfind_by_clerk_id__mutmut_2(self, clerk_user_id: str) -> User | None:
        """
        Find user by Clerk user ID

        Args:
            clerk_user_id: Clerk's unique identifier

        Returns:
            User instance or None
        """
        async with await self.adapter.get_session() as session:
            result = await session.execute(None)
            return result.scalar_one_or_none()

    async def xǁUserRepositoryǁfind_by_clerk_id__mutmut_3(self, clerk_user_id: str) -> User | None:
        """
        Find user by Clerk user ID

        Args:
            clerk_user_id: Clerk's unique identifier

        Returns:
            User instance or None
        """
        async with await self.adapter.get_session() as session:
            result = await session.execute(select(User).where(None))
            return result.scalar_one_or_none()

    async def xǁUserRepositoryǁfind_by_clerk_id__mutmut_4(self, clerk_user_id: str) -> User | None:
        """
        Find user by Clerk user ID

        Args:
            clerk_user_id: Clerk's unique identifier

        Returns:
            User instance or None
        """
        async with await self.adapter.get_session() as session:
            result = await session.execute(select(None).where(User.clerk_user_id == clerk_user_id))
            return result.scalar_one_or_none()

    async def xǁUserRepositoryǁfind_by_clerk_id__mutmut_5(self, clerk_user_id: str) -> User | None:
        """
        Find user by Clerk user ID

        Args:
            clerk_user_id: Clerk's unique identifier

        Returns:
            User instance or None
        """
        async with await self.adapter.get_session() as session:
            result = await session.execute(select(User).where(User.clerk_user_id != clerk_user_id))
            return result.scalar_one_or_none()
    
    xǁUserRepositoryǁfind_by_clerk_id__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁUserRepositoryǁfind_by_clerk_id__mutmut_1': xǁUserRepositoryǁfind_by_clerk_id__mutmut_1, 
        'xǁUserRepositoryǁfind_by_clerk_id__mutmut_2': xǁUserRepositoryǁfind_by_clerk_id__mutmut_2, 
        'xǁUserRepositoryǁfind_by_clerk_id__mutmut_3': xǁUserRepositoryǁfind_by_clerk_id__mutmut_3, 
        'xǁUserRepositoryǁfind_by_clerk_id__mutmut_4': xǁUserRepositoryǁfind_by_clerk_id__mutmut_4, 
        'xǁUserRepositoryǁfind_by_clerk_id__mutmut_5': xǁUserRepositoryǁfind_by_clerk_id__mutmut_5
    }
    
    def find_by_clerk_id(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁUserRepositoryǁfind_by_clerk_id__mutmut_orig"), object.__getattribute__(self, "xǁUserRepositoryǁfind_by_clerk_id__mutmut_mutants"), args, kwargs, self)
        return result 
    
    find_by_clerk_id.__signature__ = _mutmut_signature(xǁUserRepositoryǁfind_by_clerk_id__mutmut_orig)
    xǁUserRepositoryǁfind_by_clerk_id__mutmut_orig.__name__ = 'xǁUserRepositoryǁfind_by_clerk_id'

    async def xǁUserRepositoryǁfind_by_email__mutmut_orig(self, email: str) -> User | None:
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

    async def xǁUserRepositoryǁfind_by_email__mutmut_1(self, email: str) -> User | None:
        """
        Find user by email

        Args:
            email: User's email address

        Returns:
            User instance or None
        """
        async with await self.adapter.get_session() as session:
            result = None
            return result.scalar_one_or_none()

    async def xǁUserRepositoryǁfind_by_email__mutmut_2(self, email: str) -> User | None:
        """
        Find user by email

        Args:
            email: User's email address

        Returns:
            User instance or None
        """
        async with await self.adapter.get_session() as session:
            result = await session.execute(None)
            return result.scalar_one_or_none()

    async def xǁUserRepositoryǁfind_by_email__mutmut_3(self, email: str) -> User | None:
        """
        Find user by email

        Args:
            email: User's email address

        Returns:
            User instance or None
        """
        async with await self.adapter.get_session() as session:
            result = await session.execute(select(User).where(None))
            return result.scalar_one_or_none()

    async def xǁUserRepositoryǁfind_by_email__mutmut_4(self, email: str) -> User | None:
        """
        Find user by email

        Args:
            email: User's email address

        Returns:
            User instance or None
        """
        async with await self.adapter.get_session() as session:
            result = await session.execute(select(None).where(User.email == email))
            return result.scalar_one_or_none()

    async def xǁUserRepositoryǁfind_by_email__mutmut_5(self, email: str) -> User | None:
        """
        Find user by email

        Args:
            email: User's email address

        Returns:
            User instance or None
        """
        async with await self.adapter.get_session() as session:
            result = await session.execute(select(User).where(User.email != email))
            return result.scalar_one_or_none()
    
    xǁUserRepositoryǁfind_by_email__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁUserRepositoryǁfind_by_email__mutmut_1': xǁUserRepositoryǁfind_by_email__mutmut_1, 
        'xǁUserRepositoryǁfind_by_email__mutmut_2': xǁUserRepositoryǁfind_by_email__mutmut_2, 
        'xǁUserRepositoryǁfind_by_email__mutmut_3': xǁUserRepositoryǁfind_by_email__mutmut_3, 
        'xǁUserRepositoryǁfind_by_email__mutmut_4': xǁUserRepositoryǁfind_by_email__mutmut_4, 
        'xǁUserRepositoryǁfind_by_email__mutmut_5': xǁUserRepositoryǁfind_by_email__mutmut_5
    }
    
    def find_by_email(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁUserRepositoryǁfind_by_email__mutmut_orig"), object.__getattribute__(self, "xǁUserRepositoryǁfind_by_email__mutmut_mutants"), args, kwargs, self)
        return result 
    
    find_by_email.__signature__ = _mutmut_signature(xǁUserRepositoryǁfind_by_email__mutmut_orig)
    xǁUserRepositoryǁfind_by_email__mutmut_orig.__name__ = 'xǁUserRepositoryǁfind_by_email'

    async def xǁUserRepositoryǁfind_all__mutmut_orig(
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

    async def xǁUserRepositoryǁfind_all__mutmut_1(
        self, skip: int = 1, limit: int = 100, include_deleted: bool = False
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

    async def xǁUserRepositoryǁfind_all__mutmut_2(
        self, skip: int = 0, limit: int = 101, include_deleted: bool = False
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

    async def xǁUserRepositoryǁfind_all__mutmut_3(
        self, skip: int = 0, limit: int = 100, include_deleted: bool = True
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

    async def xǁUserRepositoryǁfind_all__mutmut_4(
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
            result = None
            return list(result.scalars().all())

    async def xǁUserRepositoryǁfind_all__mutmut_5(
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
            result = await session.execute(None)
            return list(result.scalars().all())

    async def xǁUserRepositoryǁfind_all__mutmut_6(
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
            result = await session.execute(select(User).offset(skip).limit(None))
            return list(result.scalars().all())

    async def xǁUserRepositoryǁfind_all__mutmut_7(
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
            result = await session.execute(select(User).offset(None).limit(limit))
            return list(result.scalars().all())

    async def xǁUserRepositoryǁfind_all__mutmut_8(
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
            result = await session.execute(select(None).offset(skip).limit(limit))
            return list(result.scalars().all())

    async def xǁUserRepositoryǁfind_all__mutmut_9(
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
            return list(None)
    
    xǁUserRepositoryǁfind_all__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁUserRepositoryǁfind_all__mutmut_1': xǁUserRepositoryǁfind_all__mutmut_1, 
        'xǁUserRepositoryǁfind_all__mutmut_2': xǁUserRepositoryǁfind_all__mutmut_2, 
        'xǁUserRepositoryǁfind_all__mutmut_3': xǁUserRepositoryǁfind_all__mutmut_3, 
        'xǁUserRepositoryǁfind_all__mutmut_4': xǁUserRepositoryǁfind_all__mutmut_4, 
        'xǁUserRepositoryǁfind_all__mutmut_5': xǁUserRepositoryǁfind_all__mutmut_5, 
        'xǁUserRepositoryǁfind_all__mutmut_6': xǁUserRepositoryǁfind_all__mutmut_6, 
        'xǁUserRepositoryǁfind_all__mutmut_7': xǁUserRepositoryǁfind_all__mutmut_7, 
        'xǁUserRepositoryǁfind_all__mutmut_8': xǁUserRepositoryǁfind_all__mutmut_8, 
        'xǁUserRepositoryǁfind_all__mutmut_9': xǁUserRepositoryǁfind_all__mutmut_9
    }
    
    def find_all(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁUserRepositoryǁfind_all__mutmut_orig"), object.__getattribute__(self, "xǁUserRepositoryǁfind_all__mutmut_mutants"), args, kwargs, self)
        return result 
    
    find_all.__signature__ = _mutmut_signature(xǁUserRepositoryǁfind_all__mutmut_orig)
    xǁUserRepositoryǁfind_all__mutmut_orig.__name__ = 'xǁUserRepositoryǁfind_all'

    async def xǁUserRepositoryǁcreate__mutmut_orig(self, data: dict[str, Any]) -> User:
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

    async def xǁUserRepositoryǁcreate__mutmut_1(self, data: dict[str, Any]) -> User:
        """
        Create new user

        Args:
            data: User data dictionary

        Returns:
            Created User instance
        """
        async with await self.adapter.get_session() as session:
            user = None
            session.add(user)
            await session.commit()
            await session.refresh(user)
            return user

    async def xǁUserRepositoryǁcreate__mutmut_2(self, data: dict[str, Any]) -> User:
        """
        Create new user

        Args:
            data: User data dictionary

        Returns:
            Created User instance
        """
        async with await self.adapter.get_session() as session:
            user = User(**data)
            session.add(None)
            await session.commit()
            await session.refresh(user)
            return user

    async def xǁUserRepositoryǁcreate__mutmut_3(self, data: dict[str, Any]) -> User:
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
            await session.refresh(None)
            return user
    
    xǁUserRepositoryǁcreate__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁUserRepositoryǁcreate__mutmut_1': xǁUserRepositoryǁcreate__mutmut_1, 
        'xǁUserRepositoryǁcreate__mutmut_2': xǁUserRepositoryǁcreate__mutmut_2, 
        'xǁUserRepositoryǁcreate__mutmut_3': xǁUserRepositoryǁcreate__mutmut_3
    }
    
    def create(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁUserRepositoryǁcreate__mutmut_orig"), object.__getattribute__(self, "xǁUserRepositoryǁcreate__mutmut_mutants"), args, kwargs, self)
        return result 
    
    create.__signature__ = _mutmut_signature(xǁUserRepositoryǁcreate__mutmut_orig)
    xǁUserRepositoryǁcreate__mutmut_orig.__name__ = 'xǁUserRepositoryǁcreate'

    async def xǁUserRepositoryǁupdate__mutmut_orig(self, id: str, data: dict[str, Any]) -> User | None:
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

    async def xǁUserRepositoryǁupdate__mutmut_1(self, id: str, data: dict[str, Any]) -> User | None:
        """
        Update user

        Args:
            id: User UUID
            data: Updated data dictionary

        Returns:
            Updated User instance or None
        """
        async with await self.adapter.get_session() as session:
            user = None
            if not user:
                return None

            for key, value in data.items():
                if hasattr(user, key):
                    setattr(user, key, value)

            session.add(user)
            await session.commit()
            await session.refresh(user)
            return user

    async def xǁUserRepositoryǁupdate__mutmut_2(self, id: str, data: dict[str, Any]) -> User | None:
        """
        Update user

        Args:
            id: User UUID
            data: Updated data dictionary

        Returns:
            Updated User instance or None
        """
        async with await self.adapter.get_session() as session:
            user = await self.find_by_id(None)
            if not user:
                return None

            for key, value in data.items():
                if hasattr(user, key):
                    setattr(user, key, value)

            session.add(user)
            await session.commit()
            await session.refresh(user)
            return user

    async def xǁUserRepositoryǁupdate__mutmut_3(self, id: str, data: dict[str, Any]) -> User | None:
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
            if user:
                return None

            for key, value in data.items():
                if hasattr(user, key):
                    setattr(user, key, value)

            session.add(user)
            await session.commit()
            await session.refresh(user)
            return user

    async def xǁUserRepositoryǁupdate__mutmut_4(self, id: str, data: dict[str, Any]) -> User | None:
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
                if hasattr(None, key):
                    setattr(user, key, value)

            session.add(user)
            await session.commit()
            await session.refresh(user)
            return user

    async def xǁUserRepositoryǁupdate__mutmut_5(self, id: str, data: dict[str, Any]) -> User | None:
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
                if hasattr(user, None):
                    setattr(user, key, value)

            session.add(user)
            await session.commit()
            await session.refresh(user)
            return user

    async def xǁUserRepositoryǁupdate__mutmut_6(self, id: str, data: dict[str, Any]) -> User | None:
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
                if hasattr(key):
                    setattr(user, key, value)

            session.add(user)
            await session.commit()
            await session.refresh(user)
            return user

    async def xǁUserRepositoryǁupdate__mutmut_7(self, id: str, data: dict[str, Any]) -> User | None:
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
                if hasattr(user, ):
                    setattr(user, key, value)

            session.add(user)
            await session.commit()
            await session.refresh(user)
            return user

    async def xǁUserRepositoryǁupdate__mutmut_8(self, id: str, data: dict[str, Any]) -> User | None:
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
                    setattr(None, key, value)

            session.add(user)
            await session.commit()
            await session.refresh(user)
            return user

    async def xǁUserRepositoryǁupdate__mutmut_9(self, id: str, data: dict[str, Any]) -> User | None:
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
                    setattr(user, None, value)

            session.add(user)
            await session.commit()
            await session.refresh(user)
            return user

    async def xǁUserRepositoryǁupdate__mutmut_10(self, id: str, data: dict[str, Any]) -> User | None:
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
                    setattr(user, key, None)

            session.add(user)
            await session.commit()
            await session.refresh(user)
            return user

    async def xǁUserRepositoryǁupdate__mutmut_11(self, id: str, data: dict[str, Any]) -> User | None:
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
                    setattr(key, value)

            session.add(user)
            await session.commit()
            await session.refresh(user)
            return user

    async def xǁUserRepositoryǁupdate__mutmut_12(self, id: str, data: dict[str, Any]) -> User | None:
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
                    setattr(user, value)

            session.add(user)
            await session.commit()
            await session.refresh(user)
            return user

    async def xǁUserRepositoryǁupdate__mutmut_13(self, id: str, data: dict[str, Any]) -> User | None:
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
                    setattr(user, key, )

            session.add(user)
            await session.commit()
            await session.refresh(user)
            return user

    async def xǁUserRepositoryǁupdate__mutmut_14(self, id: str, data: dict[str, Any]) -> User | None:
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

            session.add(None)
            await session.commit()
            await session.refresh(user)
            return user

    async def xǁUserRepositoryǁupdate__mutmut_15(self, id: str, data: dict[str, Any]) -> User | None:
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
            await session.refresh(None)
            return user
    
    xǁUserRepositoryǁupdate__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁUserRepositoryǁupdate__mutmut_1': xǁUserRepositoryǁupdate__mutmut_1, 
        'xǁUserRepositoryǁupdate__mutmut_2': xǁUserRepositoryǁupdate__mutmut_2, 
        'xǁUserRepositoryǁupdate__mutmut_3': xǁUserRepositoryǁupdate__mutmut_3, 
        'xǁUserRepositoryǁupdate__mutmut_4': xǁUserRepositoryǁupdate__mutmut_4, 
        'xǁUserRepositoryǁupdate__mutmut_5': xǁUserRepositoryǁupdate__mutmut_5, 
        'xǁUserRepositoryǁupdate__mutmut_6': xǁUserRepositoryǁupdate__mutmut_6, 
        'xǁUserRepositoryǁupdate__mutmut_7': xǁUserRepositoryǁupdate__mutmut_7, 
        'xǁUserRepositoryǁupdate__mutmut_8': xǁUserRepositoryǁupdate__mutmut_8, 
        'xǁUserRepositoryǁupdate__mutmut_9': xǁUserRepositoryǁupdate__mutmut_9, 
        'xǁUserRepositoryǁupdate__mutmut_10': xǁUserRepositoryǁupdate__mutmut_10, 
        'xǁUserRepositoryǁupdate__mutmut_11': xǁUserRepositoryǁupdate__mutmut_11, 
        'xǁUserRepositoryǁupdate__mutmut_12': xǁUserRepositoryǁupdate__mutmut_12, 
        'xǁUserRepositoryǁupdate__mutmut_13': xǁUserRepositoryǁupdate__mutmut_13, 
        'xǁUserRepositoryǁupdate__mutmut_14': xǁUserRepositoryǁupdate__mutmut_14, 
        'xǁUserRepositoryǁupdate__mutmut_15': xǁUserRepositoryǁupdate__mutmut_15
    }
    
    def update(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁUserRepositoryǁupdate__mutmut_orig"), object.__getattribute__(self, "xǁUserRepositoryǁupdate__mutmut_mutants"), args, kwargs, self)
        return result 
    
    update.__signature__ = _mutmut_signature(xǁUserRepositoryǁupdate__mutmut_orig)
    xǁUserRepositoryǁupdate__mutmut_orig.__name__ = 'xǁUserRepositoryǁupdate'

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

    async def xǁUserRepositoryǁhard_delete__mutmut_orig(self, id: str) -> bool:
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

    async def xǁUserRepositoryǁhard_delete__mutmut_1(self, id: str) -> bool:
        """
        Hard delete user (permanent)

        Args:
            id: User UUID

        Returns:
            True if deleted, False otherwise
        """
        async with await self.adapter.get_session() as session:
            user = None
            if not user:
                return False

            await session.delete(user)
            await session.commit()
            return True

    async def xǁUserRepositoryǁhard_delete__mutmut_2(self, id: str) -> bool:
        """
        Hard delete user (permanent)

        Args:
            id: User UUID

        Returns:
            True if deleted, False otherwise
        """
        async with await self.adapter.get_session() as session:
            user = await self.find_by_id(None)
            if not user:
                return False

            await session.delete(user)
            await session.commit()
            return True

    async def xǁUserRepositoryǁhard_delete__mutmut_3(self, id: str) -> bool:
        """
        Hard delete user (permanent)

        Args:
            id: User UUID

        Returns:
            True if deleted, False otherwise
        """
        async with await self.adapter.get_session() as session:
            user = await self.find_by_id(id)
            if user:
                return False

            await session.delete(user)
            await session.commit()
            return True

    async def xǁUserRepositoryǁhard_delete__mutmut_4(self, id: str) -> bool:
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
                return True

            await session.delete(user)
            await session.commit()
            return True

    async def xǁUserRepositoryǁhard_delete__mutmut_5(self, id: str) -> bool:
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

            await session.delete(None)
            await session.commit()
            return True

    async def xǁUserRepositoryǁhard_delete__mutmut_6(self, id: str) -> bool:
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
            return False
    
    xǁUserRepositoryǁhard_delete__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁUserRepositoryǁhard_delete__mutmut_1': xǁUserRepositoryǁhard_delete__mutmut_1, 
        'xǁUserRepositoryǁhard_delete__mutmut_2': xǁUserRepositoryǁhard_delete__mutmut_2, 
        'xǁUserRepositoryǁhard_delete__mutmut_3': xǁUserRepositoryǁhard_delete__mutmut_3, 
        'xǁUserRepositoryǁhard_delete__mutmut_4': xǁUserRepositoryǁhard_delete__mutmut_4, 
        'xǁUserRepositoryǁhard_delete__mutmut_5': xǁUserRepositoryǁhard_delete__mutmut_5, 
        'xǁUserRepositoryǁhard_delete__mutmut_6': xǁUserRepositoryǁhard_delete__mutmut_6
    }
    
    def hard_delete(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁUserRepositoryǁhard_delete__mutmut_orig"), object.__getattribute__(self, "xǁUserRepositoryǁhard_delete__mutmut_mutants"), args, kwargs, self)
        return result 
    
    hard_delete.__signature__ = _mutmut_signature(xǁUserRepositoryǁhard_delete__mutmut_orig)
    xǁUserRepositoryǁhard_delete__mutmut_orig.__name__ = 'xǁUserRepositoryǁhard_delete'

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
