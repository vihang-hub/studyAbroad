/**
 * Integration tests for shared packages
 * Verifies that all shared packages are properly integrated
 */

import {
  describe, it, expect, beforeEach, vi,
} from 'vitest';

// Mock environment variables for testing
const mockEnv = {
  NODE_ENV: 'test',
  NEXT_PUBLIC_API_URL: 'http://localhost:8000',
  NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY: 'pk_test_mock',
  CLERK_SECRET_KEY: 'sk_test_mock',
  NEXT_PUBLIC_SUPABASE_URL: 'http://localhost:54321',
  NEXT_PUBLIC_SUPABASE_ANON_KEY: 'mock_anon_key',
  ENABLE_SUPABASE: 'true',
  ENABLE_PAYMENTS: 'false',
  LOG_LEVEL: 'debug',
};

describe('Shared Packages Integration', () => {
  beforeEach(() => {
    // Reset environment
    vi.resetModules();
    Object.keys(mockEnv).forEach((key) => {
      process.env[key] = mockEnv[key as keyof typeof mockEnv];
    });
  });

  describe('ConfigLoader', () => {
    it('should load configuration successfully', async () => {
      const { ConfigLoader } = await import('@study-abroad/shared-config');
      const loader = new ConfigLoader();
      const config = loader.getConfig();

      expect(config).toBeDefined();
      expect(config.mode).toBe('test');
      expect(config.apiUrl).toBe('http://localhost:8000');
    });

    it('should validate required environment variables', async () => {
      const { initializeConfig, validateEnvironment } = await import('@/lib/config');

      const config = initializeConfig();
      expect(config).toBeDefined();

      // Should not throw
      expect(() => validateEnvironment()).not.toThrow();
    });

    it('should provide client-safe configuration', async () => {
      const { initializeConfig, getClientConfig } = await import('@/lib/config');

      initializeConfig();
      const clientConfig = getClientConfig();

      expect(clientConfig).toBeDefined();
      expect(clientConfig.mode).toBe('test');
      expect(clientConfig.apiUrl).toBeDefined();
      expect(clientConfig.enableSupabase).toBeDefined();
      // Should not expose server-only secrets
      expect(clientConfig).not.toHaveProperty('clerkSecretKey');
    });
  });

  describe('FeatureFlags', () => {
    it('should evaluate feature flags correctly', async () => {
      const { FeatureFlags } = await import('@study-abroad/shared-feature-flags');

      const flags = new FeatureFlags('test');

      expect(flags.isEnabled('ENABLE_SUPABASE')).toBe(true);
      expect(flags.isEnabled('ENABLE_PAYMENTS')).toBe(false);
    });

    it('should provide all feature flag states', async () => {
      const { FeatureFlags } = await import('@study-abroad/shared-feature-flags');

      const flags = new FeatureFlags('test');
      const allFlags = flags.getAllFlags();

      expect(allFlags).toBeDefined();
      expect(allFlags.ENABLE_SUPABASE).toBeDefined();
      expect(allFlags.ENABLE_PAYMENTS).toBeDefined();
    });
  });

  describe('Logger', () => {
    it('should initialize logger successfully', async () => {
      const { Logger } = await import('@study-abroad/shared-logging');

      const logger = new Logger({
        level: 'debug',
        environment: 'test',
      });

      expect(logger).toBeDefined();

      // Should not throw
      expect(() => logger.info('Test message')).not.toThrow();
      expect(() => logger.debug('Debug message', { test: true })).not.toThrow();
    });

    it('should sanitize sensitive data', async () => {
      const { sanitizeLogData } = await import('@study-abroad/shared-logging');

      const data = {
        username: 'testuser',
        password: 'secret123',
        apiKey: 'sk_test_secret',
        token: 'bearer_token',
      };

      const sanitized = sanitizeLogData(data);

      expect(sanitized.username).toBe('testuser');
      expect(sanitized.password).toBe('[REDACTED]');
      expect(sanitized.apiKey).toBe('[REDACTED]');
      expect(sanitized.token).toBe('[REDACTED]');
    });

    it('should support correlation IDs', async () => {
      const {
        withCorrelationId,
        getCorrelationId,
      } = await import('@study-abroad/shared-logging');

      let capturedId: string | null = null;

      await withCorrelationId(async () => {
        capturedId = getCorrelationId();
      });

      expect(capturedId).toBeDefined();
      expect(typeof capturedId).toBe('string');
    });
  });

  describe('API Client', () => {
    it('should include correlation IDs in requests', async () => {
      const { fetchApi } = await import('@/lib/api-client');

      // Mock fetch
      global.fetch = vi.fn().mockResolvedValue({
        ok: true,
        status: 200,
        headers: new Headers({ 'content-type': 'application/json' }),
        json: async () => ({ success: true }),
      });

      const response = await fetchApi('/test', {
        correlationId: 'test-correlation-id',
      });

      expect(response.correlationId).toBe('test-correlation-id');
      expect(global.fetch).toHaveBeenCalledWith(
        expect.any(String),
        expect.objectContaining({
          headers: expect.any(Headers),
        }),
      );
    });

    it('should log API requests and responses', async () => {
      const { api } = await import('@/lib/api-client');

      // Mock fetch
      global.fetch = vi.fn().mockResolvedValue({
        ok: true,
        status: 200,
        headers: new Headers({ 'content-type': 'application/json' }),
        json: async () => ({ data: 'test' }),
      });

      const response = await api.get('/test');

      expect(response.status).toBe(200);
      expect(response.data).toEqual({ data: 'test' });
    });

    it('should handle errors gracefully', async () => {
      const { api } = await import('@/lib/api-client');

      // Mock fetch to reject
      global.fetch = vi.fn().mockRejectedValue(new Error('Network error'));

      const response = await api.get('/test');

      expect(response.error).toBeDefined();
      expect(response.error?.message).toBe('Network error');
      expect(response.status).toBe(0);
    });
  });

  describe('Integration Flow', () => {
    it('should initialize all systems in correct order', async () => {
      // This tests that the initialization order works correctly
      const { initializeConfig } = await import('@/lib/config');
      const { initializeLogger } = await import('@/lib/logger');

      // Should not throw
      expect(() => {
        const config = initializeConfig();
        expect(config).toBeDefined();

        const logger = initializeLogger();
        expect(logger).toBeDefined();
      }).not.toThrow();
    });

    it('should provide consistent configuration across modules', async () => {
      const { initializeConfig, getConfig } = await import('@/lib/config');

      const config1 = initializeConfig();
      const config2 = getConfig();

      expect(config1).toBe(config2); // Same instance
      expect(config1.mode).toBe(config2.mode);
    });
  });
});
