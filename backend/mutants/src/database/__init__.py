"""
Database Module

Repository pattern with PostgreSQL and Supabase adapters.
Equivalent to TypeScript @study-abroad/shared-database package.

This module provides:
- Database models (User, Report, Payment)
- Repository pattern with soft delete support
- Database adapters (PostgreSQL, Supabase)
- Transaction support

Usage:
    from database import get_database_adapter, UserRepository

    adapter = get_database_adapter()
    user_repo = UserRepository(adapter)

    user = await user_repo.find_by_id(user_id)
"""

from database.types import DatabaseAdapter, Repository
from database.adapters import PostgreSQLAdapter, SupabaseAdapter, get_database_adapter
from database.repositories import UserRepository, ReportRepository, PaymentRepository

__all__ = [
    "DatabaseAdapter",
    "Repository",
    "PostgreSQLAdapter",
    "SupabaseAdapter",
    "get_database_adapter",
    "UserRepository",
    "ReportRepository",
    "PaymentRepository",
]
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
