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
