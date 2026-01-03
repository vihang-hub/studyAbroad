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


class PostgreSQLAdapter(DatabaseAdapter):
    """
    PostgreSQL Database Adapter

    Connects to local PostgreSQL database for development.
    Uses asyncpg driver for async operations.
    """

    def xǁPostgreSQLAdapterǁ__init____mutmut_orig(self, database_url: str, pool_size: int = 20, pool_timeout: int = 30):
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

    def xǁPostgreSQLAdapterǁ__init____mutmut_1(self, database_url: str, pool_size: int = 21, pool_timeout: int = 30):
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

    def xǁPostgreSQLAdapterǁ__init____mutmut_2(self, database_url: str, pool_size: int = 20, pool_timeout: int = 31):
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

    def xǁPostgreSQLAdapterǁ__init____mutmut_3(self, database_url: str, pool_size: int = 20, pool_timeout: int = 30):
        """
        Initialize PostgreSQL adapter

        Args:
            database_url: PostgreSQL connection string
            pool_size: Maximum connection pool size
            pool_timeout: Connection timeout in seconds
        """
        self.database_url = None
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

    def xǁPostgreSQLAdapterǁ__init____mutmut_4(self, database_url: str, pool_size: int = 20, pool_timeout: int = 30):
        """
        Initialize PostgreSQL adapter

        Args:
            database_url: PostgreSQL connection string
            pool_size: Maximum connection pool size
            pool_timeout: Connection timeout in seconds
        """
        self.database_url = database_url
        self.engine: AsyncEngine = None
        self.session_maker = async_sessionmaker(
            self.engine, class_=AsyncSession, expire_on_commit=False
        )

    def xǁPostgreSQLAdapterǁ__init____mutmut_5(self, database_url: str, pool_size: int = 20, pool_timeout: int = 30):
        """
        Initialize PostgreSQL adapter

        Args:
            database_url: PostgreSQL connection string
            pool_size: Maximum connection pool size
            pool_timeout: Connection timeout in seconds
        """
        self.database_url = database_url
        self.engine: AsyncEngine = create_async_engine(
            None,
            pool_size=pool_size,
            max_overflow=10,
            pool_timeout=pool_timeout,
            echo=False,  # Set to True for SQL logging
        )
        self.session_maker = async_sessionmaker(
            self.engine, class_=AsyncSession, expire_on_commit=False
        )

    def xǁPostgreSQLAdapterǁ__init____mutmut_6(self, database_url: str, pool_size: int = 20, pool_timeout: int = 30):
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
            pool_size=None,
            max_overflow=10,
            pool_timeout=pool_timeout,
            echo=False,  # Set to True for SQL logging
        )
        self.session_maker = async_sessionmaker(
            self.engine, class_=AsyncSession, expire_on_commit=False
        )

    def xǁPostgreSQLAdapterǁ__init____mutmut_7(self, database_url: str, pool_size: int = 20, pool_timeout: int = 30):
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
            max_overflow=None,
            pool_timeout=pool_timeout,
            echo=False,  # Set to True for SQL logging
        )
        self.session_maker = async_sessionmaker(
            self.engine, class_=AsyncSession, expire_on_commit=False
        )

    def xǁPostgreSQLAdapterǁ__init____mutmut_8(self, database_url: str, pool_size: int = 20, pool_timeout: int = 30):
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
            pool_timeout=None,
            echo=False,  # Set to True for SQL logging
        )
        self.session_maker = async_sessionmaker(
            self.engine, class_=AsyncSession, expire_on_commit=False
        )

    def xǁPostgreSQLAdapterǁ__init____mutmut_9(self, database_url: str, pool_size: int = 20, pool_timeout: int = 30):
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
            echo=None,  # Set to True for SQL logging
        )
        self.session_maker = async_sessionmaker(
            self.engine, class_=AsyncSession, expire_on_commit=False
        )

    def xǁPostgreSQLAdapterǁ__init____mutmut_10(self, database_url: str, pool_size: int = 20, pool_timeout: int = 30):
        """
        Initialize PostgreSQL adapter

        Args:
            database_url: PostgreSQL connection string
            pool_size: Maximum connection pool size
            pool_timeout: Connection timeout in seconds
        """
        self.database_url = database_url
        self.engine: AsyncEngine = create_async_engine(
            pool_size=pool_size,
            max_overflow=10,
            pool_timeout=pool_timeout,
            echo=False,  # Set to True for SQL logging
        )
        self.session_maker = async_sessionmaker(
            self.engine, class_=AsyncSession, expire_on_commit=False
        )

    def xǁPostgreSQLAdapterǁ__init____mutmut_11(self, database_url: str, pool_size: int = 20, pool_timeout: int = 30):
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
            max_overflow=10,
            pool_timeout=pool_timeout,
            echo=False,  # Set to True for SQL logging
        )
        self.session_maker = async_sessionmaker(
            self.engine, class_=AsyncSession, expire_on_commit=False
        )

    def xǁPostgreSQLAdapterǁ__init____mutmut_12(self, database_url: str, pool_size: int = 20, pool_timeout: int = 30):
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
            pool_timeout=pool_timeout,
            echo=False,  # Set to True for SQL logging
        )
        self.session_maker = async_sessionmaker(
            self.engine, class_=AsyncSession, expire_on_commit=False
        )

    def xǁPostgreSQLAdapterǁ__init____mutmut_13(self, database_url: str, pool_size: int = 20, pool_timeout: int = 30):
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
            echo=False,  # Set to True for SQL logging
        )
        self.session_maker = async_sessionmaker(
            self.engine, class_=AsyncSession, expire_on_commit=False
        )

    def xǁPostgreSQLAdapterǁ__init____mutmut_14(self, database_url: str, pool_size: int = 20, pool_timeout: int = 30):
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
            )
        self.session_maker = async_sessionmaker(
            self.engine, class_=AsyncSession, expire_on_commit=False
        )

    def xǁPostgreSQLAdapterǁ__init____mutmut_15(self, database_url: str, pool_size: int = 20, pool_timeout: int = 30):
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
            max_overflow=11,
            pool_timeout=pool_timeout,
            echo=False,  # Set to True for SQL logging
        )
        self.session_maker = async_sessionmaker(
            self.engine, class_=AsyncSession, expire_on_commit=False
        )

    def xǁPostgreSQLAdapterǁ__init____mutmut_16(self, database_url: str, pool_size: int = 20, pool_timeout: int = 30):
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
            echo=True,  # Set to True for SQL logging
        )
        self.session_maker = async_sessionmaker(
            self.engine, class_=AsyncSession, expire_on_commit=False
        )

    def xǁPostgreSQLAdapterǁ__init____mutmut_17(self, database_url: str, pool_size: int = 20, pool_timeout: int = 30):
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
        self.session_maker = None

    def xǁPostgreSQLAdapterǁ__init____mutmut_18(self, database_url: str, pool_size: int = 20, pool_timeout: int = 30):
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
            None, class_=AsyncSession, expire_on_commit=False
        )

    def xǁPostgreSQLAdapterǁ__init____mutmut_19(self, database_url: str, pool_size: int = 20, pool_timeout: int = 30):
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
            self.engine, class_=None, expire_on_commit=False
        )

    def xǁPostgreSQLAdapterǁ__init____mutmut_20(self, database_url: str, pool_size: int = 20, pool_timeout: int = 30):
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
            self.engine, class_=AsyncSession, expire_on_commit=None
        )

    def xǁPostgreSQLAdapterǁ__init____mutmut_21(self, database_url: str, pool_size: int = 20, pool_timeout: int = 30):
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
            class_=AsyncSession, expire_on_commit=False
        )

    def xǁPostgreSQLAdapterǁ__init____mutmut_22(self, database_url: str, pool_size: int = 20, pool_timeout: int = 30):
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
            self.engine, expire_on_commit=False
        )

    def xǁPostgreSQLAdapterǁ__init____mutmut_23(self, database_url: str, pool_size: int = 20, pool_timeout: int = 30):
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
            self.engine, class_=AsyncSession, )

    def xǁPostgreSQLAdapterǁ__init____mutmut_24(self, database_url: str, pool_size: int = 20, pool_timeout: int = 30):
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
            self.engine, class_=AsyncSession, expire_on_commit=True
        )
    
    xǁPostgreSQLAdapterǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁPostgreSQLAdapterǁ__init____mutmut_1': xǁPostgreSQLAdapterǁ__init____mutmut_1, 
        'xǁPostgreSQLAdapterǁ__init____mutmut_2': xǁPostgreSQLAdapterǁ__init____mutmut_2, 
        'xǁPostgreSQLAdapterǁ__init____mutmut_3': xǁPostgreSQLAdapterǁ__init____mutmut_3, 
        'xǁPostgreSQLAdapterǁ__init____mutmut_4': xǁPostgreSQLAdapterǁ__init____mutmut_4, 
        'xǁPostgreSQLAdapterǁ__init____mutmut_5': xǁPostgreSQLAdapterǁ__init____mutmut_5, 
        'xǁPostgreSQLAdapterǁ__init____mutmut_6': xǁPostgreSQLAdapterǁ__init____mutmut_6, 
        'xǁPostgreSQLAdapterǁ__init____mutmut_7': xǁPostgreSQLAdapterǁ__init____mutmut_7, 
        'xǁPostgreSQLAdapterǁ__init____mutmut_8': xǁPostgreSQLAdapterǁ__init____mutmut_8, 
        'xǁPostgreSQLAdapterǁ__init____mutmut_9': xǁPostgreSQLAdapterǁ__init____mutmut_9, 
        'xǁPostgreSQLAdapterǁ__init____mutmut_10': xǁPostgreSQLAdapterǁ__init____mutmut_10, 
        'xǁPostgreSQLAdapterǁ__init____mutmut_11': xǁPostgreSQLAdapterǁ__init____mutmut_11, 
        'xǁPostgreSQLAdapterǁ__init____mutmut_12': xǁPostgreSQLAdapterǁ__init____mutmut_12, 
        'xǁPostgreSQLAdapterǁ__init____mutmut_13': xǁPostgreSQLAdapterǁ__init____mutmut_13, 
        'xǁPostgreSQLAdapterǁ__init____mutmut_14': xǁPostgreSQLAdapterǁ__init____mutmut_14, 
        'xǁPostgreSQLAdapterǁ__init____mutmut_15': xǁPostgreSQLAdapterǁ__init____mutmut_15, 
        'xǁPostgreSQLAdapterǁ__init____mutmut_16': xǁPostgreSQLAdapterǁ__init____mutmut_16, 
        'xǁPostgreSQLAdapterǁ__init____mutmut_17': xǁPostgreSQLAdapterǁ__init____mutmut_17, 
        'xǁPostgreSQLAdapterǁ__init____mutmut_18': xǁPostgreSQLAdapterǁ__init____mutmut_18, 
        'xǁPostgreSQLAdapterǁ__init____mutmut_19': xǁPostgreSQLAdapterǁ__init____mutmut_19, 
        'xǁPostgreSQLAdapterǁ__init____mutmut_20': xǁPostgreSQLAdapterǁ__init____mutmut_20, 
        'xǁPostgreSQLAdapterǁ__init____mutmut_21': xǁPostgreSQLAdapterǁ__init____mutmut_21, 
        'xǁPostgreSQLAdapterǁ__init____mutmut_22': xǁPostgreSQLAdapterǁ__init____mutmut_22, 
        'xǁPostgreSQLAdapterǁ__init____mutmut_23': xǁPostgreSQLAdapterǁ__init____mutmut_23, 
        'xǁPostgreSQLAdapterǁ__init____mutmut_24': xǁPostgreSQLAdapterǁ__init____mutmut_24
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁPostgreSQLAdapterǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁPostgreSQLAdapterǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁPostgreSQLAdapterǁ__init____mutmut_orig)
    xǁPostgreSQLAdapterǁ__init____mutmut_orig.__name__ = 'xǁPostgreSQLAdapterǁ__init__'

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

    async def xǁPostgreSQLAdapterǁexecute_raw__mutmut_orig(self, query: str, params: dict[str, Any] | None = None) -> Any:
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

    async def xǁPostgreSQLAdapterǁexecute_raw__mutmut_1(self, query: str, params: dict[str, Any] | None = None) -> Any:
        """
        Execute raw SQL query

        Args:
            query: SQL query string
            params: Query parameters

        Returns:
            Query result
        """
        async with self.session_maker() as session:
            result = None
            await session.commit()
            return result

    async def xǁPostgreSQLAdapterǁexecute_raw__mutmut_2(self, query: str, params: dict[str, Any] | None = None) -> Any:
        """
        Execute raw SQL query

        Args:
            query: SQL query string
            params: Query parameters

        Returns:
            Query result
        """
        async with self.session_maker() as session:
            result = await session.execute(None, params or {})
            await session.commit()
            return result

    async def xǁPostgreSQLAdapterǁexecute_raw__mutmut_3(self, query: str, params: dict[str, Any] | None = None) -> Any:
        """
        Execute raw SQL query

        Args:
            query: SQL query string
            params: Query parameters

        Returns:
            Query result
        """
        async with self.session_maker() as session:
            result = await session.execute(text(query), None)
            await session.commit()
            return result

    async def xǁPostgreSQLAdapterǁexecute_raw__mutmut_4(self, query: str, params: dict[str, Any] | None = None) -> Any:
        """
        Execute raw SQL query

        Args:
            query: SQL query string
            params: Query parameters

        Returns:
            Query result
        """
        async with self.session_maker() as session:
            result = await session.execute(params or {})
            await session.commit()
            return result

    async def xǁPostgreSQLAdapterǁexecute_raw__mutmut_5(self, query: str, params: dict[str, Any] | None = None) -> Any:
        """
        Execute raw SQL query

        Args:
            query: SQL query string
            params: Query parameters

        Returns:
            Query result
        """
        async with self.session_maker() as session:
            result = await session.execute(text(query), )
            await session.commit()
            return result

    async def xǁPostgreSQLAdapterǁexecute_raw__mutmut_6(self, query: str, params: dict[str, Any] | None = None) -> Any:
        """
        Execute raw SQL query

        Args:
            query: SQL query string
            params: Query parameters

        Returns:
            Query result
        """
        async with self.session_maker() as session:
            result = await session.execute(text(None), params or {})
            await session.commit()
            return result

    async def xǁPostgreSQLAdapterǁexecute_raw__mutmut_7(self, query: str, params: dict[str, Any] | None = None) -> Any:
        """
        Execute raw SQL query

        Args:
            query: SQL query string
            params: Query parameters

        Returns:
            Query result
        """
        async with self.session_maker() as session:
            result = await session.execute(text(query), params and {})
            await session.commit()
            return result
    
    xǁPostgreSQLAdapterǁexecute_raw__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁPostgreSQLAdapterǁexecute_raw__mutmut_1': xǁPostgreSQLAdapterǁexecute_raw__mutmut_1, 
        'xǁPostgreSQLAdapterǁexecute_raw__mutmut_2': xǁPostgreSQLAdapterǁexecute_raw__mutmut_2, 
        'xǁPostgreSQLAdapterǁexecute_raw__mutmut_3': xǁPostgreSQLAdapterǁexecute_raw__mutmut_3, 
        'xǁPostgreSQLAdapterǁexecute_raw__mutmut_4': xǁPostgreSQLAdapterǁexecute_raw__mutmut_4, 
        'xǁPostgreSQLAdapterǁexecute_raw__mutmut_5': xǁPostgreSQLAdapterǁexecute_raw__mutmut_5, 
        'xǁPostgreSQLAdapterǁexecute_raw__mutmut_6': xǁPostgreSQLAdapterǁexecute_raw__mutmut_6, 
        'xǁPostgreSQLAdapterǁexecute_raw__mutmut_7': xǁPostgreSQLAdapterǁexecute_raw__mutmut_7
    }
    
    def execute_raw(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁPostgreSQLAdapterǁexecute_raw__mutmut_orig"), object.__getattribute__(self, "xǁPostgreSQLAdapterǁexecute_raw__mutmut_mutants"), args, kwargs, self)
        return result 
    
    execute_raw.__signature__ = _mutmut_signature(xǁPostgreSQLAdapterǁexecute_raw__mutmut_orig)
    xǁPostgreSQLAdapterǁexecute_raw__mutmut_orig.__name__ = 'xǁPostgreSQLAdapterǁexecute_raw'
