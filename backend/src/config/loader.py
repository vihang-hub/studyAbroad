"""
Configuration Loader

Singleton pattern for loading and caching environment configuration.
Equivalent to TypeScript loader.ts.
"""

from typing import Any
from config.environment import EnvironmentConfig


class ConfigLoader:
    """
    Configuration Loader Class

    Provides singleton access to validated environment configuration.
    Configuration is loaded once and cached for performance.
    """

    _instance: EnvironmentConfig | None = None

    @classmethod
    def load(cls) -> EnvironmentConfig:
        """
        Load and validate environment configuration

        This method validates all environment variables against the Pydantic schema.
        On validation failure, it logs detailed error messages and raises.
        Subsequent calls return the cached instance for performance.

        Returns:
            Validated configuration object

        Raises:
            ValueError: If configuration validation fails
        """
        if cls._instance is not None:
            return cls._instance

        try:
            cls._instance = EnvironmentConfig()
            return cls._instance
        except Exception as e:
            print("❌ Configuration validation failed:")
            print(str(e))
            raise ValueError(
                "Invalid environment configuration. Please check your environment variables."
            ) from e

    @classmethod
    def get(cls, key: str) -> Any:
        """
        Get specific configuration value

        Args:
            key: Configuration key

        Returns:
            Configuration value

        Raises:
            ValueError: If configuration not loaded
        """
        if cls._instance is None:
            raise ValueError("Configuration not loaded. Call ConfigLoader.load() first.")
        return getattr(cls._instance, key)

    @classmethod
    def is_loaded(cls) -> bool:
        """
        Check if configuration is loaded

        Returns:
            True if configuration is loaded
        """
        return cls._instance is not None

    @classmethod
    def reload(cls) -> None:
        """
        Reload configuration

        Clears cached instance and forces re-validation.
        Useful for testing or dynamic configuration updates.
        """
        cls._instance = None

    @classmethod
    def reset(cls) -> None:
        """
        Reset configuration (alias for reload)

        Primarily used in test environments to clear state between tests.
        """
        cls.reload()


# Global singleton instance
config_loader = ConfigLoader()
