/**
 * Feature flag evaluator
 *
 * Provides type-safe feature flag evaluation based on environment configuration.
 *
 * @module evaluator
 */

import { ConfigLoader, type EnvironmentConfig } from '@study-abroad/shared-config';
import { Feature, type EnvironmentMode, type FeatureFlagState } from './types';

/**
 * Feature flag evaluator service
 *
 * Singleton service that evaluates feature flags based on environment configuration.
 * Integrates with @study-abroad/shared-config for configuration management.
 */
export class FeatureFlags {
  private static instance: FeatureFlags | null = null;

  private config: EnvironmentConfig;

  /**
   * Private constructor for singleton pattern
   */
  private constructor() {
    this.config = ConfigLoader.load();
  }

  /**
   * Get singleton instance
   */
  private static getInstance(): FeatureFlags {
    if (!FeatureFlags.instance) {
      FeatureFlags.instance = new FeatureFlags();
    }
    return FeatureFlags.instance;
  }

  /**
   * Reset singleton instance (for testing)
   * @internal
   */
  public static reset(): void {
    FeatureFlags.instance = null;
  }

  /**
   * Check if a feature is enabled
   *
   * @param feature - Feature flag to check
   * @returns True if feature is enabled, false otherwise
   *
   * @example
   * ```typescript
   * if (FeatureFlags.isEnabled(Feature.PAYMENTS)) {
   *   await processPayment();
   * }
   * ```
   */
  public static isEnabled(feature: Feature): boolean {
    const instance = FeatureFlags.getInstance();
    const enabled = instance.getFeatureValue(feature);
    return enabled;
  }

  /**
   * Get current environment mode
   *
   * @returns Environment mode ('dev' | 'test' | 'production')
   *
   * @example
   * ```typescript
   * const mode = FeatureFlags.getEnvironmentMode();
   * if (mode === 'dev') {
   *   console.log('Running in development mode');
   * }
   * ```
   */
  public static getEnvironmentMode(): EnvironmentMode {
    const instance = FeatureFlags.getInstance();
    return instance.config.ENVIRONMENT_MODE;
  }

  /**
   * Get all feature flag states
   *
   * @returns Object mapping all feature flags to their current states
   *
   * @example
   * ```typescript
   * const flags = FeatureFlags.getAllFlags();
   * console.log(flags); // { ENABLE_SUPABASE: true, ENABLE_PAYMENTS: false, ... }
   * ```
   */
  public static getAllFlags(): FeatureFlagState {
    const instance = FeatureFlags.getInstance();
    return {
      [Feature.SUPABASE]: instance.getFeatureValue(Feature.SUPABASE),
      [Feature.PAYMENTS]: instance.getFeatureValue(Feature.PAYMENTS),
      [Feature.RATE_LIMITING]: instance.getFeatureValue(Feature.RATE_LIMITING),
      [Feature.OBSERVABILITY]: instance.getFeatureValue(Feature.OBSERVABILITY),
    };
  }

  /**
   * Require a feature to be enabled, throw if not
   *
   * @param feature - Feature that must be enabled
   * @throws Error if feature is not enabled
   *
   * @example
   * ```typescript
   * // In an API route that requires payments
   * FeatureFlags.requireEnabled(Feature.PAYMENTS);
   * // Throws if payments are disabled
   * ```
   */
  public static requireEnabled(feature: Feature): void {
    if (!FeatureFlags.isEnabled(feature)) {
      const mode = FeatureFlags.getEnvironmentMode();
      throw new Error(
        `Feature ${feature} is required but not enabled in ${mode} environment. ` +
        `Set ${feature}=true in environment variables.`,
      );
    }
  }

  /**
   * Get feature value from configuration
   */
  private getFeatureValue(feature: Feature): boolean {
    switch (feature) {
      case Feature.SUPABASE:
        return this.config.ENABLE_SUPABASE;
      case Feature.PAYMENTS:
        return this.config.ENABLE_PAYMENTS;
      case Feature.RATE_LIMITING:
        return this.config.ENABLE_RATE_LIMITING;
      case Feature.OBSERVABILITY:
        return this.config.ENABLE_OBSERVABILITY;
      default:
        // TypeScript should prevent this, but handle exhaustiveness
        return false;
    }
  }
}
