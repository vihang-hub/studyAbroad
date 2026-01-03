"""
Database Types

Type definitions and abstract base classes for database operations.
"""

from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar
from sqlalchemy.ext.asyncio import AsyncSession

T = TypeVar("T")
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

    def xǁRepositoryǁ__init____mutmut_orig(self, adapter: DatabaseAdapter):
        self.adapter = adapter

    def xǁRepositoryǁ__init____mutmut_1(self, adapter: DatabaseAdapter):
        self.adapter = None
    
    xǁRepositoryǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁRepositoryǁ__init____mutmut_1': xǁRepositoryǁ__init____mutmut_1
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁRepositoryǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁRepositoryǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁRepositoryǁ__init____mutmut_orig)
    xǁRepositoryǁ__init____mutmut_orig.__name__ = 'xǁRepositoryǁ__init__'

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
