"""
Feature Flag Evaluator

Evaluates feature flags based on environment configuration.
Equivalent to TypeScript evaluator.ts.
"""

from feature_flags.types import Feature


class FeatureFlagEvaluator:
    """
    Feature Flag Evaluator

    Evaluates feature flags from environment configuration.
    Provides is_enabled(), require_enabled(), and get_all_flags() methods.
    """

    def __init__(self):
        """Initialize evaluator with configuration"""
        # Import here to avoid circular dependency
        from config import config_loader

        self._config = config_loader.load()

    def is_enabled(self, feature: Feature) -> bool:
        """
        Check if a feature is enabled

        Args:
            feature: Feature to check

        Returns:
            True if enabled, false otherwise
        """
        flag_value = getattr(self._config, feature.value, False)

        # Log feature flag evaluation
        self._log_evaluation(feature, flag_value)

        return flag_value is True

    def require_enabled(self, feature: Feature) -> None:
        """
        Require a feature to be enabled, raise if not

        Args:
            feature: Feature to require

        Raises:
            ValueError: If feature is not enabled
        """
        if not self.is_enabled(feature):
            raise ValueError(
                f"Feature {feature.value} is required but not enabled. "
                f"Set {feature.value}=true in environment variables."
            )

    def get_all_flags(self) -> dict[str, bool]:
        """
        Get all feature flags and their states

        Returns:
            Dictionary with all feature flags and their values
        """
        return {
            Feature.SUPABASE.value: self.is_enabled(Feature.SUPABASE),
            Feature.PAYMENTS.value: self.is_enabled(Feature.PAYMENTS),
            Feature.RATE_LIMITING.value: self.is_enabled(Feature.RATE_LIMITING),
            Feature.OBSERVABILITY.value: self.is_enabled(Feature.OBSERVABILITY),
        }

    def _log_evaluation(self, feature: Feature, enabled: bool) -> None:
        """
        Log feature flag evaluation

        Args:
            feature: Feature being evaluated
            enabled: Whether feature is enabled
        """
        # Import logger to avoid circular dependency
        try:
            import structlog

            logger = structlog.get_logger()
            logger.debug(
                "feature_flag_evaluated",
                feature=feature.value,
                enabled=enabled,
                environment=self._config.ENVIRONMENT_MODE,
            )
        except Exception:
            # Silently fail if logging not configured yet
            pass


# Global singleton instance
feature_flags = FeatureFlagEvaluator()
