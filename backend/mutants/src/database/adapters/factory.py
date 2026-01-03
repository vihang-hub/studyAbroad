"""
Database Adapter Factory

Creates appropriate database adapter based on feature flags.
"""

from database.types import DatabaseAdapter
from database.adapters.postgresql import PostgreSQLAdapter
from database.adapters.supabase import SupabaseAdapter
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


def x_get_database_adapter__mutmut_orig() -> DatabaseAdapter:
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


def x_get_database_adapter__mutmut_1() -> DatabaseAdapter:
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

    config = None

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


def x_get_database_adapter__mutmut_2() -> DatabaseAdapter:
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

    if feature_flags.is_enabled(None):
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


def x_get_database_adapter__mutmut_3() -> DatabaseAdapter:
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
        if config.SUPABASE_SERVICE_ROLE_KEY:
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


def x_get_database_adapter__mutmut_4() -> DatabaseAdapter:
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
            raise ValueError(None)

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


def x_get_database_adapter__mutmut_5() -> DatabaseAdapter:
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
            raise ValueError("XXSUPABASE_SERVICE_ROLE_KEY is required when ENABLE_SUPABASE=trueXX")

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


def x_get_database_adapter__mutmut_6() -> DatabaseAdapter:
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
            raise ValueError("supabase_service_role_key is required when enable_supabase=true")

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


def x_get_database_adapter__mutmut_7() -> DatabaseAdapter:
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
            raise ValueError("SUPABASE_SERVICE_ROLE_KEY IS REQUIRED WHEN ENABLE_SUPABASE=TRUE")

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


def x_get_database_adapter__mutmut_8() -> DatabaseAdapter:
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
            database_url=None,
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


def x_get_database_adapter__mutmut_9() -> DatabaseAdapter:
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
            service_role_key=None,
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


def x_get_database_adapter__mutmut_10() -> DatabaseAdapter:
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
            pool_size=None,
            pool_timeout=config.DATABASE_IDLE_TIMEOUT_MS // 1000,
        )
    else:
        # Dev mode: Use local PostgreSQL
        return PostgreSQLAdapter(
            database_url=config.DATABASE_URL,
            pool_size=config.DATABASE_POOL_MAX,
            pool_timeout=config.DATABASE_IDLE_TIMEOUT_MS // 1000,
        )


def x_get_database_adapter__mutmut_11() -> DatabaseAdapter:
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
            pool_timeout=None,
        )
    else:
        # Dev mode: Use local PostgreSQL
        return PostgreSQLAdapter(
            database_url=config.DATABASE_URL,
            pool_size=config.DATABASE_POOL_MAX,
            pool_timeout=config.DATABASE_IDLE_TIMEOUT_MS // 1000,
        )


def x_get_database_adapter__mutmut_12() -> DatabaseAdapter:
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


def x_get_database_adapter__mutmut_13() -> DatabaseAdapter:
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


def x_get_database_adapter__mutmut_14() -> DatabaseAdapter:
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
            pool_timeout=config.DATABASE_IDLE_TIMEOUT_MS // 1000,
        )
    else:
        # Dev mode: Use local PostgreSQL
        return PostgreSQLAdapter(
            database_url=config.DATABASE_URL,
            pool_size=config.DATABASE_POOL_MAX,
            pool_timeout=config.DATABASE_IDLE_TIMEOUT_MS // 1000,
        )


def x_get_database_adapter__mutmut_15() -> DatabaseAdapter:
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
            )
    else:
        # Dev mode: Use local PostgreSQL
        return PostgreSQLAdapter(
            database_url=config.DATABASE_URL,
            pool_size=config.DATABASE_POOL_MAX,
            pool_timeout=config.DATABASE_IDLE_TIMEOUT_MS // 1000,
        )


def x_get_database_adapter__mutmut_16() -> DatabaseAdapter:
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
            pool_timeout=config.DATABASE_IDLE_TIMEOUT_MS / 1000,
        )
    else:
        # Dev mode: Use local PostgreSQL
        return PostgreSQLAdapter(
            database_url=config.DATABASE_URL,
            pool_size=config.DATABASE_POOL_MAX,
            pool_timeout=config.DATABASE_IDLE_TIMEOUT_MS // 1000,
        )


def x_get_database_adapter__mutmut_17() -> DatabaseAdapter:
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
            pool_timeout=config.DATABASE_IDLE_TIMEOUT_MS // 1001,
        )
    else:
        # Dev mode: Use local PostgreSQL
        return PostgreSQLAdapter(
            database_url=config.DATABASE_URL,
            pool_size=config.DATABASE_POOL_MAX,
            pool_timeout=config.DATABASE_IDLE_TIMEOUT_MS // 1000,
        )


def x_get_database_adapter__mutmut_18() -> DatabaseAdapter:
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
            database_url=None,
            pool_size=config.DATABASE_POOL_MAX,
            pool_timeout=config.DATABASE_IDLE_TIMEOUT_MS // 1000,
        )


def x_get_database_adapter__mutmut_19() -> DatabaseAdapter:
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
            pool_size=None,
            pool_timeout=config.DATABASE_IDLE_TIMEOUT_MS // 1000,
        )


def x_get_database_adapter__mutmut_20() -> DatabaseAdapter:
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
            pool_timeout=None,
        )


def x_get_database_adapter__mutmut_21() -> DatabaseAdapter:
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
            pool_size=config.DATABASE_POOL_MAX,
            pool_timeout=config.DATABASE_IDLE_TIMEOUT_MS // 1000,
        )


def x_get_database_adapter__mutmut_22() -> DatabaseAdapter:
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
            pool_timeout=config.DATABASE_IDLE_TIMEOUT_MS // 1000,
        )


def x_get_database_adapter__mutmut_23() -> DatabaseAdapter:
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
            )


def x_get_database_adapter__mutmut_24() -> DatabaseAdapter:
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
            pool_timeout=config.DATABASE_IDLE_TIMEOUT_MS / 1000,
        )


def x_get_database_adapter__mutmut_25() -> DatabaseAdapter:
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
            pool_timeout=config.DATABASE_IDLE_TIMEOUT_MS // 1001,
        )

x_get_database_adapter__mutmut_mutants : ClassVar[MutantDict] = {
'x_get_database_adapter__mutmut_1': x_get_database_adapter__mutmut_1, 
    'x_get_database_adapter__mutmut_2': x_get_database_adapter__mutmut_2, 
    'x_get_database_adapter__mutmut_3': x_get_database_adapter__mutmut_3, 
    'x_get_database_adapter__mutmut_4': x_get_database_adapter__mutmut_4, 
    'x_get_database_adapter__mutmut_5': x_get_database_adapter__mutmut_5, 
    'x_get_database_adapter__mutmut_6': x_get_database_adapter__mutmut_6, 
    'x_get_database_adapter__mutmut_7': x_get_database_adapter__mutmut_7, 
    'x_get_database_adapter__mutmut_8': x_get_database_adapter__mutmut_8, 
    'x_get_database_adapter__mutmut_9': x_get_database_adapter__mutmut_9, 
    'x_get_database_adapter__mutmut_10': x_get_database_adapter__mutmut_10, 
    'x_get_database_adapter__mutmut_11': x_get_database_adapter__mutmut_11, 
    'x_get_database_adapter__mutmut_12': x_get_database_adapter__mutmut_12, 
    'x_get_database_adapter__mutmut_13': x_get_database_adapter__mutmut_13, 
    'x_get_database_adapter__mutmut_14': x_get_database_adapter__mutmut_14, 
    'x_get_database_adapter__mutmut_15': x_get_database_adapter__mutmut_15, 
    'x_get_database_adapter__mutmut_16': x_get_database_adapter__mutmut_16, 
    'x_get_database_adapter__mutmut_17': x_get_database_adapter__mutmut_17, 
    'x_get_database_adapter__mutmut_18': x_get_database_adapter__mutmut_18, 
    'x_get_database_adapter__mutmut_19': x_get_database_adapter__mutmut_19, 
    'x_get_database_adapter__mutmut_20': x_get_database_adapter__mutmut_20, 
    'x_get_database_adapter__mutmut_21': x_get_database_adapter__mutmut_21, 
    'x_get_database_adapter__mutmut_22': x_get_database_adapter__mutmut_22, 
    'x_get_database_adapter__mutmut_23': x_get_database_adapter__mutmut_23, 
    'x_get_database_adapter__mutmut_24': x_get_database_adapter__mutmut_24, 
    'x_get_database_adapter__mutmut_25': x_get_database_adapter__mutmut_25
}

def get_database_adapter(*args, **kwargs):
    result = _mutmut_trampoline(x_get_database_adapter__mutmut_orig, x_get_database_adapter__mutmut_mutants, args, kwargs)
    return result 

get_database_adapter.__signature__ = _mutmut_signature(x_get_database_adapter__mutmut_orig)
x_get_database_adapter__mutmut_orig.__name__ = 'x_get_database_adapter'
