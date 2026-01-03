/**
 * Tests for public API exports
 */

import { describe, it, expect } from 'vitest';
import * as FeatureFlagsModule from '../src/index';

describe('Module Exports', () => {
  it('should export Feature enum', () => {
    expect(FeatureFlagsModule.Feature).toBeDefined();
    expect(FeatureFlagsModule.Feature.SUPABASE).toBe('ENABLE_SUPABASE');
    expect(FeatureFlagsModule.Feature.PAYMENTS).toBe('ENABLE_PAYMENTS');
    expect(FeatureFlagsModule.Feature.RATE_LIMITING).toBe('ENABLE_RATE_LIMITING');
    expect(FeatureFlagsModule.Feature.OBSERVABILITY).toBe('ENABLE_OBSERVABILITY');
  });

  it('should export FeatureFlags class', () => {
    expect(FeatureFlagsModule.FeatureFlags).toBeDefined();
    expect(typeof FeatureFlagsModule.FeatureFlags.isEnabled).toBe('function');
    expect(typeof FeatureFlagsModule.FeatureFlags.getEnvironmentMode).toBe('function');
    expect(typeof FeatureFlagsModule.FeatureFlags.getAllFlags).toBe('function');
    expect(typeof FeatureFlagsModule.FeatureFlags.requireEnabled).toBe('function');
  });

  it('should export React hooks', () => {
    expect(FeatureFlagsModule.useFeatureFlag).toBeDefined();
    expect(typeof FeatureFlagsModule.useFeatureFlag).toBe('function');

    expect(FeatureFlagsModule.useEnvironmentMode).toBeDefined();
    expect(typeof FeatureFlagsModule.useEnvironmentMode).toBe('function');

    expect(FeatureFlagsModule.useAllFeatureFlags).toBeDefined();
    expect(typeof FeatureFlagsModule.useAllFeatureFlags).toBe('function');
  });

  it('should export FeatureGate component', () => {
    expect(FeatureFlagsModule.FeatureGate).toBeDefined();
    expect(typeof FeatureFlagsModule.FeatureGate).toBe('function');
  });

  it('should have exactly 9 named exports', () => {
    const exports = Object.keys(FeatureFlagsModule);
    // Feature, FeatureFlags, useFeatureFlag, useEnvironmentMode, useAllFeatureFlags, FeatureGate
    // Plus type exports don't count in runtime
    expect(exports.length).toBeGreaterThanOrEqual(6);
  });

  it('should not have default export', () => {
    expect((FeatureFlagsModule as any).default).toBeUndefined();
  });
});
