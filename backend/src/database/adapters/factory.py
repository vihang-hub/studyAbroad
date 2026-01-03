"""
Database Adapter Factory

Creates appropriate database adapter based on feature flags.
"""

from database.types import DatabaseAdapter
from database.adapters.postgresql import PostgreSQLAdapter
from database.adapters.supabase import SupabaseAdapter


def get_database_adapter() -> DatabaseAdapter:
    """
    Get appropriate database adapter based on feature flags

    Returns PostgreSQLAdapter for dev mode (ENABLE_SUPABASE=false)
    Returns SupabaseAdapter for test/production (ENABLE_SUPABASE=true)

    Returns:
        DatabaseAdapter instance

    Raises:
        ValueError: If configuration is invalid
    """
    from config import config_loader
    from feature_flags import feature_flags, Feature

    config = config_loader.load()

    if feature_flags.is_enabled(Feature.SUPABASE):
        # Test/Production mode: Use Supabase
        if not config.SUPABASE_SERVICE_ROLE_KEY:
            raise ValueError("SUPABASE_SERVICE_ROLE_KEY is required when ENABLE_SUPABASE=true")

        return SupabaseAdapter(
            database_url=config.DATABASE_URL,
            service_role_key=config.SUPABASE_SERVICE_ROLE_KEY,
            pool_size=config.DATABASE_POOL_MAX,
            pool_timeout=config.DATABASE_IDLE_TIMEOUT_MS // 1000,
        )
    else:
        # Dev mode: Use local PostgreSQL
        return PostgreSQLAdapter(
            database_url=config.DATABASE_URL,
            pool_size=config.DATABASE_POOL_MAX,
            pool_timeout=config.DATABASE_IDLE_TIMEOUT_MS // 1000,
        )
