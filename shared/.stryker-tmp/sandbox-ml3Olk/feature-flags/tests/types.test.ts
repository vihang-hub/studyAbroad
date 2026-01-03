/**
 * Tests for feature flag types
 */
// @ts-nocheck


import { describe, it, expect } from 'vitest';
import { Feature } from '../src/types';

describe('Feature enum', () => {
  it('should have correct SUPABASE value', () => {
    expect(Feature.SUPABASE).toBe('ENABLE_SUPABASE');
  });

  it('should have correct PAYMENTS value', () => {
    expect(Feature.PAYMENTS).toBe('ENABLE_PAYMENTS');
  });

  it('should have correct RATE_LIMITING value', () => {
    expect(Feature.RATE_LIMITING).toBe('ENABLE_RATE_LIMITING');
  });

  it('should have correct OBSERVABILITY value', () => {
    expect(Feature.OBSERVABILITY).toBe('ENABLE_OBSERVABILITY');
  });

  it('should have exactly 4 features', () => {
    const features = Object.values(Feature);
    expect(features).toHaveLength(4);
  });

  it('should have unique values', () => {
    const values = Object.values(Feature);
    const uniqueValues = new Set(values);
    expect(uniqueValues.size).toBe(values.length);
  });
});
