/**
 * @study-abroad/shared-feature-flags
 *
 * Feature flag evaluation with React hooks for environment-based feature toggles.
 *
 * @module @study-abroad/shared-feature-flags
 */
// @ts-nocheck


// Export types
export { Feature, type EnvironmentMode, type FeatureFlagState, type FeatureFlagEvaluation } from './types';

// Export evaluator
export { FeatureFlags } from './evaluator';

// Export hooks
export { useFeatureFlag, useEnvironmentMode, useAllFeatureFlags } from './hooks';

// Export components
export { FeatureGate, type FeatureGateProps } from './components';
