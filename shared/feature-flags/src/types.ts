/**
 * Feature flag type definitions
 *
 * @module types
 */

/**
 * Available feature flags in the system
 */
export enum Feature {
  SUPABASE = 'ENABLE_SUPABASE',
  PAYMENTS = 'ENABLE_PAYMENTS',
  RATE_LIMITING = 'ENABLE_RATE_LIMITING',
  OBSERVABILITY = 'ENABLE_OBSERVABILITY',
}

/**
 * Environment mode type
 */
export type EnvironmentMode = 'dev' | 'test' | 'production';

/**
 * Feature flag state map
 */
export type FeatureFlagState = Record<Feature, boolean>;

/**
 * Feature flag evaluation result
 */
export interface FeatureFlagEvaluation {
  feature: Feature;
  enabled: boolean;
  environment: EnvironmentMode;
  timestamp: Date;
}
