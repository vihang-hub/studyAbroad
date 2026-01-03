/**
 * React hooks for feature flag evaluation
 *
 * @module hooks
 */

import { useMemo } from 'react';
import { FeatureFlags } from './evaluator';
import { Feature, type EnvironmentMode } from './types';

/**
 * React hook for feature flag evaluation
 *
 * @param feature - Feature flag to check
 * @returns True if feature is enabled, false otherwise
 *
 * @example
 * ```typescript
 * function PaymentButton() {
 *   const paymentsEnabled = useFeatureFlag(Feature.PAYMENTS);
 *
 *   if (!paymentsEnabled) {
 *     return <div>Payments disabled in this environment</div>;
 *   }
 *
 *   return <StripeCheckout />;
 * }
 * ```
 */
export function useFeatureFlag(feature: Feature): boolean {
  return useMemo(() => FeatureFlags.isEnabled(feature), [feature]);
}

/**
 * React hook for environment mode
 *
 * @returns Current environment mode ('dev' | 'test' | 'production')
 *
 * @example
 * ```typescript
 * function DevelopmentBanner() {
 *   const mode = useEnvironmentMode();
 *
 *   if (mode === 'production') {
 *     return null;
 *   }
 *
 *   return <div>Running in {mode} mode</div>;
 * }
 * ```
 */
export function useEnvironmentMode(): EnvironmentMode {
  return useMemo(() => FeatureFlags.getEnvironmentMode(), []);
}

/**
 * React hook to get all feature flags
 *
 * @returns Object mapping all feature flags to their current states
 *
 * @example
 * ```typescript
 * function FeatureFlagDebugger() {
 *   const flags = useAllFeatureFlags();
 *
 *   return (
 *     <ul>
 *       {Object.entries(flags).map(([flag, enabled]) => (
 *         <li key={flag}>{flag}: {enabled ? 'ON' : 'OFF'}</li>
 *       ))}
 *     </ul>
 *   );
 * }
 * ```
 */
export function useAllFeatureFlags() {
  return useMemo(() => FeatureFlags.getAllFlags(), []);
}
