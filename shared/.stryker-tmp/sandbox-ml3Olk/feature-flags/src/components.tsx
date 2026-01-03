/**
 * React components for feature flag-based rendering
 *
 * @module components
 */
// @ts-nocheck


import React from 'react';
import { useFeatureFlag } from './hooks';
import { Feature } from './types';

/**
 * Props for FeatureGate component
 */
export interface FeatureGateProps {
  /**
   * Feature flag to check
   */
  feature: Feature;

  /**
   * Expected state of the feature flag (default: true)
   */
  enabled?: boolean;

  /**
   * Fallback content to render when feature is not in expected state
   */
  fallback?: React.ReactNode;

  /**
   * Children to render when feature is in expected state
   */
  children: React.ReactNode;
}

/**
 * Feature gate component for conditional rendering based on feature flags
 *
 * Renders children only when the specified feature flag matches the expected state.
 * If the feature flag doesn't match, renders the fallback (or nothing if no fallback provided).
 *
 * @param props - Component props
 * @returns React element
 *
 * @example
 * ```typescript
 * // Render only when payments are enabled
 * <FeatureGate feature={Feature.PAYMENTS}>
 *   <StripeCheckout />
 * </FeatureGate>
 *
 * // Render with fallback
 * <FeatureGate
 *   feature={Feature.PAYMENTS}
 *   fallback={<div>Payments disabled in this environment</div>}
 * >
 *   <StripeCheckout />
 * </FeatureGate>
 *
 * // Render only when feature is disabled
 * <FeatureGate feature={Feature.PAYMENTS} enabled={false}>
 *   <div>Free access (payments disabled)</div>
 * </FeatureGate>
 * ```
 */
export function FeatureGate({
  feature,
  enabled = true,
  fallback = null,
  children,
}: FeatureGateProps): React.ReactElement | null {
  const isFeatureEnabled = useFeatureFlag(feature);

  // If feature state matches expected state, render children
  if (isFeatureEnabled === enabled) {
    return <>{children}</>;
  }

  // Otherwise render fallback
  return <>{fallback}</>;
}
