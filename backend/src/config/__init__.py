"""
Configuration Module

Environment-based configuration management with Pydantic validation.
Equivalent to TypeScript @study-abroad/shared-config package.

This module provides:
- EnvironmentConfig: Pydantic model for all configuration
- ConfigLoader: Singleton configuration loader
- Environment presets for dev/test/production

Usage:
    from config import config_loader

    config = config_loader.load()
    print(config.ENVIRONMENT_MODE)
"""

from config.environment import EnvironmentConfig, EnvironmentMode, LogLevel
from config.loader import ConfigLoader, config_loader
from config.presets import DEV_PRESET, TEST_PRESET, PRODUCTION_PRESET

# Backward compatibility: Create a settings object for old code
settings = config_loader.load()

__all__ = [
    "EnvironmentConfig",
    "EnvironmentMode",
    "LogLevel",
    "ConfigLoader",
    "config_loader",
    "DEV_PRESET",
    "TEST_PRESET",
    "PRODUCTION_PRESET",
    "settings",  # Backward compatibility
]
