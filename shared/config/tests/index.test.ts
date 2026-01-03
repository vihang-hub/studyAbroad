/**
 * Tests for package exports
 *
 * Verifies all public API exports are accessible.
 */

import { describe, it, expect } from 'vitest';
import * as configPackage from '../src/index';

describe('Package Exports', () => {
  it('should export ConfigLoader', () => {
    expect(configPackage.ConfigLoader).toBeDefined();
    expect(typeof configPackage.ConfigLoader.load).toBe('function');
    expect(typeof configPackage.ConfigLoader.get).toBe('function');
    expect(typeof configPackage.ConfigLoader.isLoaded).toBe('function');
    expect(typeof configPackage.ConfigLoader.reset).toBe('function');
  });

  it('should export environment schemas', () => {
    expect(configPackage.EnvironmentConfigSchema).toBeDefined();
    expect(configPackage.EnvironmentMode).toBeDefined();
    expect(configPackage.LogLevel).toBeDefined();
    expect(configPackage.AuthProvider).toBeDefined();
    expect(configPackage.PaymentStatus).toBeDefined();
    expect(configPackage.ReportStatus).toBeDefined();
  });

  it('should export API schemas', () => {
    expect(configPackage.Country).toBeDefined();
    expect(configPackage.CostRangeSchema).toBeDefined();
    expect(configPackage.ActionPlanSchema).toBeDefined();
    expect(configPackage.ReportContentSchema).toBeDefined();
    expect(configPackage.CitationSchema).toBeDefined();
    expect(configPackage.CreateReportRequestSchema).toBeDefined();
    expect(configPackage.CreateReportResponseSchema).toBeDefined();
    expect(configPackage.ReportSummarySchema).toBeDefined();
    expect(configPackage.ListReportsResponseSchema).toBeDefined();
    expect(configPackage.ReportResponseSchema).toBeDefined();
    expect(configPackage.CreatePaymentRequestSchema).toBeDefined();
    expect(configPackage.CreatePaymentResponseSchema).toBeDefined();
    expect(configPackage.HealthResponseSchema).toBeDefined();
    expect(configPackage.HealthCheckSchema).toBeDefined();
    expect(configPackage.DetailedHealthResponseSchema).toBeDefined();
    expect(configPackage.ErrorResponseSchema).toBeDefined();
    expect(configPackage.SSEEventType).toBeDefined();
    expect(configPackage.SSEEventSchema).toBeDefined();
    expect(configPackage.PaginationParamsSchema).toBeDefined();
    expect(configPackage.ErrorCode).toBeDefined();
  });

  it('should export preset utilities', () => {
    expect(configPackage.EnvironmentPresets).toBeDefined();
    expect(configPackage.DEV_PRESET).toBeDefined();
    expect(configPackage.TEST_PRESET).toBeDefined();
    expect(configPackage.PRODUCTION_PRESET).toBeDefined();
    expect(typeof configPackage.getPreset).toBe('function');
    expect(typeof configPackage.mergePreset).toBe('function');
  });

  it('should have valid preset structure', () => {
    expect(configPackage.EnvironmentPresets.dev).toBe(configPackage.DEV_PRESET);
    expect(configPackage.EnvironmentPresets.test).toBe(configPackage.TEST_PRESET);
    expect(configPackage.EnvironmentPresets.production).toBe(configPackage.PRODUCTION_PRESET);
  });
});
