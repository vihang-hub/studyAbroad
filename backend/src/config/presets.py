"""
Environment Configuration Presets

Predefined configuration values for dev/test/production environments.
Equivalent to TypeScript presets.ts.
"""

# Development preset
DEV_PRESET: dict[str, any] = {
    "ENVIRONMENT_MODE": "dev",
    "ENABLE_SUPABASE": False,
    "ENABLE_PAYMENTS": False,
    "LOG_LEVEL": "DEBUG",
    "LOG_PRETTY_PRINT": True,
    "DATABASE_URL": "postgresql://studyabroad:studyabroad_dev@localhost:5432/studyabroad_dev",
}

# Test preset
TEST_PRESET: dict[str, any] = {
    "ENVIRONMENT_MODE": "test",
    "ENABLE_SUPABASE": True,
    "ENABLE_PAYMENTS": False,
    "LOG_LEVEL": "DEBUG",
    "LOG_PRETTY_PRINT": False,
}

# Production preset
PRODUCTION_PRESET: dict[str, any] = {
    "ENVIRONMENT_MODE": "production",
    "ENABLE_SUPABASE": True,
    "ENABLE_PAYMENTS": True,
    "LOG_LEVEL": "ERROR",
    "LOG_PRETTY_PRINT": False,
    "LOG_CONSOLE_ENABLED": False,
}
