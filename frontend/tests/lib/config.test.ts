/**
 * Tests for configuration management
 * Coverage target: 100% (high-impact file: ~8-10% total frontend coverage)
 */

import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import type { EnvironmentConfig } from '@study-abroad/shared-config';

// Mock console methods
const consoleLogSpy = vi.spyOn(console, 'log').mockImplementation(() => {});
const consoleErrorSpy = vi.spyOn(console, 'error').mockImplementation(() => {});

// Mock environment config factory
const createMockConfig = (overrides: Partial<EnvironmentConfig> = {}): EnvironmentConfig => ({
  ENVIRONMENT_MODE: 'test',
  NEXT_PUBLIC_API_URL: 'http://localhost:8000',
  NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY: 'pk_test_clerk',
  CLERK_SECRET_KEY: 'sk_test_clerk',
  ENABLE_SUPABASE: false,
  ENABLE_PAYMENTS: false,
  SUPABASE_URL: '',
  SUPABASE_ANON_KEY: '',
  apiUrl: 'http://localhost:8000',
  logLevel: 'info',
  mode: 'test',
  ...overrides,
});

describe('config', () => {
  let mockConfigLoaderLoad: ReturnType<typeof vi.fn>;

  beforeEach(async () => {
    vi.clearAllMocks();
    // Reset modules to clear singleton state
    vi.resetModules();

    // Create mock function
    mockConfigLoaderLoad = vi.fn();

    // Mock the shared-config module
    vi.doMock('@study-abroad/shared-config', () => ({
      ConfigLoader: {
        load: mockConfigLoaderLoad,
      },
    }));

    // Reset environment variables
    delete process.env.NEXT_PUBLIC_API_URL;
    delete process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY;
    delete process.env.CLERK_SECRET_KEY;
    delete process.env.NEXT_PUBLIC_SUPABASE_URL;
    delete process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;
    delete process.env.NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY;
  });

  afterEach(() => {
    vi.clearAllMocks();
    vi.resetModules();
  });

  describe('initializeConfig', () => {
    it('should initialize configuration successfully', async () => {
      const mockConfig = createMockConfig();
      mockConfigLoaderLoad.mockReturnValue(mockConfig);

      const { initializeConfig } = await import('../../src/lib/config');
      const config = initializeConfig();

      expect(config).toBeDefined();
      expect(config.ENVIRONMENT_MODE).toBe('test');
      expect(mockConfigLoaderLoad).toHaveBeenCalled();
    });

    it('should return same instance on multiple calls', async () => {
      const mockConfig = createMockConfig();
      mockConfigLoaderLoad.mockReturnValue(mockConfig);

      const { initializeConfig } = await import('../../src/lib/config');
      const config1 = initializeConfig();
      const config2 = initializeConfig();

      expect(config1).toBe(config2);
      expect(mockConfigLoaderLoad).toHaveBeenCalledTimes(1);
    });

    it('should log initialization in development mode', async () => {
      const mockConfig = createMockConfig({
        ENVIRONMENT_MODE: 'dev',
      });
      mockConfigLoaderLoad.mockReturnValue(mockConfig);

      const { initializeConfig } = await import('../../src/lib/config');
      initializeConfig();

      expect(consoleLogSpy).toHaveBeenCalledWith(
        '[Config] Configuration initialized successfully',
        expect.objectContaining({
          mode: 'dev',
          enableSupabase: false,
          enablePayments: false,
        })
      );
    });

    it('should not log in non-development mode', async () => {
      const mockConfig = createMockConfig({
        ENVIRONMENT_MODE: 'production',
      });
      mockConfigLoaderLoad.mockReturnValue(mockConfig);

      consoleLogSpy.mockClear();
      const { initializeConfig } = await import('../../src/lib/config');
      initializeConfig();

      expect(consoleLogSpy).not.toHaveBeenCalled();
    });

    it('should throw error if ConfigLoader fails', async () => {
      const error = new Error('Failed to load config');
      mockConfigLoaderLoad.mockImplementation(() => {
        throw error;
      });

      const { initializeConfig } = await import('../../src/lib/config');
      expect(() => initializeConfig()).toThrow('Failed to load config');
      expect(consoleErrorSpy).toHaveBeenCalledWith(
        '[Config] Failed to initialize configuration:',
        error
      );
    });

    it('should handle ConfigLoader returning null', async () => {
      mockConfigLoaderLoad.mockReturnValue(null as unknown as EnvironmentConfig);

      const { initializeConfig } = await import('../../src/lib/config');
      // When ConfigLoader returns null, accessing ENVIRONMENT_MODE will fail
      expect(() => initializeConfig()).toThrow();
    });
  });

  describe('getConfig', () => {
    it('should return initialized config', async () => {
      const mockConfig = createMockConfig();
      mockConfigLoaderLoad.mockReturnValue(mockConfig);

      const { initializeConfig, getConfig } = await import('../../src/lib/config');
      initializeConfig();
      const config = getConfig();

      expect(config).toBeDefined();
      expect(config.ENVIRONMENT_MODE).toBe('test');
    });

    it('should auto-initialize config if not initialized (lazy initialization)', async () => {
      const mockConfig = createMockConfig();
      mockConfigLoaderLoad.mockReturnValue(mockConfig);

      const { getConfig } = await import('../../src/lib/config');

      // Should NOT throw - should auto-initialize instead
      const config = getConfig();

      expect(config).toBeDefined();
      expect(config.ENVIRONMENT_MODE).toBe('test');
      expect(mockConfigLoaderLoad).toHaveBeenCalled();
    });

    it('should not re-initialize if already initialized', async () => {
      const mockConfig = createMockConfig();
      mockConfigLoaderLoad.mockReturnValue(mockConfig);

      const { initializeConfig, getConfig } = await import('../../src/lib/config');
      initializeConfig();

      // Clear call count after explicit init
      mockConfigLoaderLoad.mockClear();

      // getConfig should not call ConfigLoader.load again
      const config = getConfig();

      expect(config).toBeDefined();
      expect(mockConfigLoaderLoad).not.toHaveBeenCalled();
    });
  });

  describe('getConfigValue', () => {
    it('should return specific config value', async () => {
      const mockConfig = createMockConfig({
        ENVIRONMENT_MODE: 'production',
      });
      mockConfigLoaderLoad.mockReturnValue(mockConfig);

      const { initializeConfig, getConfigValue } = await import('../../src/lib/config');
      initializeConfig();
      const mode = getConfigValue('ENVIRONMENT_MODE');

      expect(mode).toBe('production');
    });

    it('should return different config values', async () => {
      const mockConfig = createMockConfig({
        NEXT_PUBLIC_API_URL: 'https://api.example.com',
        ENABLE_SUPABASE: true,
      });
      mockConfigLoaderLoad.mockReturnValue(mockConfig);

      const { initializeConfig, getConfigValue } = await import('../../src/lib/config');
      initializeConfig();

      expect(getConfigValue('NEXT_PUBLIC_API_URL')).toBe('https://api.example.com');
      expect(getConfigValue('ENABLE_SUPABASE')).toBe(true);
    });

    it('should maintain type safety', async () => {
      const mockConfig = createMockConfig({
        ENABLE_PAYMENTS: true,
      });
      mockConfigLoaderLoad.mockReturnValue(mockConfig);

      const { initializeConfig, getConfigValue } = await import('../../src/lib/config');
      initializeConfig();
      const enablePayments = getConfigValue('ENABLE_PAYMENTS');

      expect(typeof enablePayments).toBe('boolean');
      expect(enablePayments).toBe(true);
    });
  });

  describe('getClientConfig', () => {
    it('should return only client-safe configuration', async () => {
      const mockConfig = createMockConfig({
        ENVIRONMENT_MODE: 'dev',
        NEXT_PUBLIC_API_URL: 'http://localhost:8000',
        ENABLE_SUPABASE: true,
        ENABLE_PAYMENTS: true,
        SUPABASE_URL: 'https://supabase.example.com',
        SUPABASE_ANON_KEY: 'anon_key_123',
        CLERK_SECRET_KEY: 'secret_that_should_not_be_exposed',
      });
      mockConfigLoaderLoad.mockReturnValue(mockConfig);

      const { initializeConfig, getClientConfig } = await import('../../src/lib/config');
      initializeConfig();
      const clientConfig = getClientConfig();

      expect(clientConfig).toEqual({
        mode: 'dev',
        apiUrl: 'http://localhost:8000',
        enableSupabase: true,
        enablePayments: true,
        supabaseUrl: 'https://supabase.example.com',
        supabaseAnonKey: 'anon_key_123',
      });

      // Should not include secret keys
      expect(clientConfig).not.toHaveProperty('CLERK_SECRET_KEY');
    });

    it('should handle disabled features', async () => {
      const mockConfig = createMockConfig({
        ENABLE_SUPABASE: false,
        ENABLE_PAYMENTS: false,
      });
      mockConfigLoaderLoad.mockReturnValue(mockConfig);

      const { initializeConfig, getClientConfig } = await import('../../src/lib/config');
      initializeConfig();
      const clientConfig = getClientConfig();

      expect(clientConfig.enableSupabase).toBe(false);
      expect(clientConfig.enablePayments).toBe(false);
    });
  });

  describe('Environment mode helpers', () => {
    describe('isDevelopment', () => {
      it('should return true in development mode', async () => {
        const mockConfig = createMockConfig({
          ENVIRONMENT_MODE: 'dev',
        });
        mockConfigLoaderLoad.mockReturnValue(mockConfig);

        const { initializeConfig, isDevelopment } = await import('../../src/lib/config');
        initializeConfig();

        expect(isDevelopment()).toBe(true);
      });

      it('should return false in non-development mode', async () => {
        const mockConfig = createMockConfig({
          ENVIRONMENT_MODE: 'production',
        });
        mockConfigLoaderLoad.mockReturnValue(mockConfig);

        const { initializeConfig, isDevelopment } = await import('../../src/lib/config');
        initializeConfig();

        expect(isDevelopment()).toBe(false);
      });
    });

    describe('isProduction', () => {
      it('should return true in production mode', async () => {
        const mockConfig = createMockConfig({
          ENVIRONMENT_MODE: 'production',
        });
        mockConfigLoaderLoad.mockReturnValue(mockConfig);

        const { initializeConfig, isProduction } = await import('../../src/lib/config');
        initializeConfig();

        expect(isProduction()).toBe(true);
      });

      it('should return false in non-production mode', async () => {
        const mockConfig = createMockConfig({
          ENVIRONMENT_MODE: 'dev',
        });
        mockConfigLoaderLoad.mockReturnValue(mockConfig);

        const { initializeConfig, isProduction } = await import('../../src/lib/config');
        initializeConfig();

        expect(isProduction()).toBe(false);
      });
    });

    describe('isTest', () => {
      it('should return true in test mode', async () => {
        const mockConfig = createMockConfig({
          ENVIRONMENT_MODE: 'test',
        });
        mockConfigLoaderLoad.mockReturnValue(mockConfig);

        const { initializeConfig, isTest } = await import('../../src/lib/config');
        initializeConfig();

        expect(isTest()).toBe(true);
      });

      it('should return false in non-test mode', async () => {
        const mockConfig = createMockConfig({
          ENVIRONMENT_MODE: 'production',
        });
        mockConfigLoaderLoad.mockReturnValue(mockConfig);

        const { initializeConfig, isTest } = await import('../../src/lib/config');
        initializeConfig();

        expect(isTest()).toBe(false);
      });
    });
  });

  describe('validateEnvironment', () => {
    it('should pass validation with all required variables', async () => {
      process.env.NEXT_PUBLIC_API_URL = 'http://localhost:8000';
      process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY = 'pk_test_clerk';
      process.env.CLERK_SECRET_KEY = 'sk_test_clerk';

      const mockConfig = createMockConfig();
      mockConfigLoaderLoad.mockReturnValue(mockConfig);

      const { initializeConfig, validateEnvironment } = await import('../../src/lib/config');
      initializeConfig();
      expect(() => validateEnvironment()).not.toThrow();
    });

    it('should throw error if NEXT_PUBLIC_API_URL is missing', async () => {
      process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY = 'pk_test_clerk';
      process.env.CLERK_SECRET_KEY = 'sk_test_clerk';

      const mockConfig = createMockConfig();
      mockConfigLoaderLoad.mockReturnValue(mockConfig);

      const { initializeConfig, validateEnvironment } = await import('../../src/lib/config');
      initializeConfig();

      expect(() => validateEnvironment()).toThrow(/NEXT_PUBLIC_API_URL/);
    });

    it('should throw error if NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY is missing', async () => {
      process.env.NEXT_PUBLIC_API_URL = 'http://localhost:8000';
      process.env.CLERK_SECRET_KEY = 'sk_test_clerk';

      const mockConfig = createMockConfig();
      mockConfigLoaderLoad.mockReturnValue(mockConfig);

      const { initializeConfig, validateEnvironment } = await import('../../src/lib/config');
      initializeConfig();

      expect(() => validateEnvironment()).toThrow(/NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY/);
    });

    it('should throw error if CLERK_SECRET_KEY is missing on server', async () => {
      // Simulate server environment
      const originalWindow = global.window;
      // @ts-expect-error Testing server-side behavior
      delete global.window;

      process.env.NEXT_PUBLIC_API_URL = 'http://localhost:8000';
      process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY = 'pk_test_clerk';

      const mockConfig = createMockConfig();
      mockConfigLoaderLoad.mockReturnValue(mockConfig);

      const { initializeConfig, validateEnvironment } = await import('../../src/lib/config');
      initializeConfig();

      expect(() => validateEnvironment()).toThrow(/CLERK_SECRET_KEY/);

      // Restore
      global.window = originalWindow;
    });

    it('should not check server variables on client', async () => {
      // Simulate browser environment
      global.window = {} as Window & typeof globalThis;

      process.env.NEXT_PUBLIC_API_URL = 'http://localhost:8000';
      process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY = 'pk_test_clerk';

      const mockConfig = createMockConfig();
      mockConfigLoaderLoad.mockReturnValue(mockConfig);

      const { initializeConfig, validateEnvironment } = await import('../../src/lib/config');
      initializeConfig();

      // Should not throw because we're on client
      expect(() => validateEnvironment()).not.toThrow();
    });

    it('should throw error if multiple variables are missing', async () => {
      process.env.CLERK_SECRET_KEY = 'sk_test_clerk';

      const mockConfig = createMockConfig();
      mockConfigLoaderLoad.mockReturnValue(mockConfig);

      const { initializeConfig, validateEnvironment } = await import('../../src/lib/config');
      initializeConfig();

      try {
        validateEnvironment();
        expect.fail('Should have thrown');
      } catch (error: unknown) {
        const err = error as Error;
        expect(err.message).toContain('NEXT_PUBLIC_API_URL');
        expect(err.message).toContain('NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY');
      }
    });

    it('should validate Supabase config when enabled', async () => {
      process.env.NEXT_PUBLIC_API_URL = 'http://localhost:8000';
      process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY = 'pk_test_clerk';
      process.env.CLERK_SECRET_KEY = 'sk_test_clerk';

      const mockConfig = createMockConfig({
        ENABLE_SUPABASE: true,
        SUPABASE_URL: '',
        SUPABASE_ANON_KEY: '',
      });
      mockConfigLoaderLoad.mockReturnValue(mockConfig);

      const { initializeConfig, validateEnvironment } = await import('../../src/lib/config');
      initializeConfig();

      expect(() => validateEnvironment()).toThrow(/Supabase is enabled/);
    });

    it('should pass Supabase validation when properly configured', async () => {
      process.env.NEXT_PUBLIC_API_URL = 'http://localhost:8000';
      process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY = 'pk_test_clerk';
      process.env.CLERK_SECRET_KEY = 'sk_test_clerk';

      const mockConfig = createMockConfig({
        ENABLE_SUPABASE: true,
        SUPABASE_URL: 'https://supabase.example.com',
        SUPABASE_ANON_KEY: 'anon_key_123',
      });
      mockConfigLoaderLoad.mockReturnValue(mockConfig);

      const { initializeConfig, validateEnvironment } = await import('../../src/lib/config');
      initializeConfig();

      expect(() => validateEnvironment()).not.toThrow();
    });

    it('should not validate Supabase when disabled', async () => {
      process.env.NEXT_PUBLIC_API_URL = 'http://localhost:8000';
      process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY = 'pk_test_clerk';
      process.env.CLERK_SECRET_KEY = 'sk_test_clerk';

      const mockConfig = createMockConfig({
        ENABLE_SUPABASE: false,
        SUPABASE_URL: '',
        SUPABASE_ANON_KEY: '',
      });
      mockConfigLoaderLoad.mockReturnValue(mockConfig);

      const { initializeConfig, validateEnvironment } = await import('../../src/lib/config');
      initializeConfig();

      expect(() => validateEnvironment()).not.toThrow();
    });

    it('should validate Stripe config when payments enabled on client', async () => {
      global.window = {} as Window & typeof globalThis;

      process.env.NEXT_PUBLIC_API_URL = 'http://localhost:8000';
      process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY = 'pk_test_clerk';

      const mockConfig = createMockConfig({
        ENABLE_PAYMENTS: true,
      });
      mockConfigLoaderLoad.mockReturnValue(mockConfig);

      const { initializeConfig, validateEnvironment } = await import('../../src/lib/config');
      initializeConfig();

      expect(() => validateEnvironment()).toThrow(/NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY/);
    });

    it('should pass Stripe validation when properly configured', async () => {
      global.window = {} as Window & typeof globalThis;

      process.env.NEXT_PUBLIC_API_URL = 'http://localhost:8000';
      process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY = 'pk_test_clerk';
      process.env.NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY = 'pk_test_stripe';

      const mockConfig = createMockConfig({
        ENABLE_PAYMENTS: true,
      });
      mockConfigLoaderLoad.mockReturnValue(mockConfig);

      const { initializeConfig, validateEnvironment } = await import('../../src/lib/config');
      initializeConfig();

      expect(() => validateEnvironment()).not.toThrow();
    });

    it('should not validate Stripe on server', async () => {
      // Simulate server
      const originalWindow = global.window;
      // @ts-expect-error Testing server-side behavior
      delete global.window;

      process.env.NEXT_PUBLIC_API_URL = 'http://localhost:8000';
      process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY = 'pk_test_clerk';
      process.env.CLERK_SECRET_KEY = 'sk_test_clerk';

      const mockConfig = createMockConfig({
        ENABLE_PAYMENTS: true,
      });
      mockConfigLoaderLoad.mockReturnValue(mockConfig);

      const { initializeConfig, validateEnvironment } = await import('../../src/lib/config');
      initializeConfig();

      // Should not throw on server
      expect(() => validateEnvironment()).not.toThrow();

      global.window = originalWindow;
    });

    it('should not validate Stripe when payments disabled', async () => {
      global.window = {} as Window & typeof globalThis;

      process.env.NEXT_PUBLIC_API_URL = 'http://localhost:8000';
      process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY = 'pk_test_clerk';

      const mockConfig = createMockConfig({
        ENABLE_PAYMENTS: false,
      });
      mockConfigLoaderLoad.mockReturnValue(mockConfig);

      const { initializeConfig, validateEnvironment } = await import('../../src/lib/config');
      initializeConfig();

      expect(() => validateEnvironment()).not.toThrow();
    });
  });

  describe('ConfigLoader export', () => {
    it('should export ConfigLoader for advanced use cases', async () => {
      const mockConfig = createMockConfig();
      mockConfigLoaderLoad.mockReturnValue(mockConfig);

      const { ConfigLoader } = await import('../../src/lib/config');
      expect(ConfigLoader).toBeDefined();
      expect(ConfigLoader.load).toBeInstanceOf(Function);
    });
  });

  describe('Edge cases', () => {
    it('should handle empty string environment variables', async () => {
      process.env.NEXT_PUBLIC_API_URL = '';
      process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY = '';
      process.env.CLERK_SECRET_KEY = 'sk_test_clerk';

      const mockConfig = createMockConfig();
      mockConfigLoaderLoad.mockReturnValue(mockConfig);

      const { initializeConfig, validateEnvironment } = await import('../../src/lib/config');
      initializeConfig();

      expect(() => validateEnvironment()).toThrow();
    });

    it('should handle whitespace-only environment variables', async () => {
      process.env.NEXT_PUBLIC_API_URL = '   ';
      process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY = '   ';
      process.env.CLERK_SECRET_KEY = 'sk_test_clerk';

      const mockConfig = createMockConfig();
      mockConfigLoaderLoad.mockReturnValue(mockConfig);

      const { initializeConfig, validateEnvironment } = await import('../../src/lib/config');
      initializeConfig();

      // Whitespace values are technically set, validation should pass
      // (ConfigLoader would handle validation of actual values)
      expect(() => validateEnvironment()).not.toThrow();
    });

    it('should handle config with all features enabled', async () => {
      global.window = {} as Window & typeof globalThis;

      process.env.NEXT_PUBLIC_API_URL = 'http://localhost:8000';
      process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY = 'pk_test_clerk';
      process.env.NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY = 'pk_test_stripe';

      const mockConfig = createMockConfig({
        ENABLE_SUPABASE: true,
        ENABLE_PAYMENTS: true,
        SUPABASE_URL: 'https://supabase.example.com',
        SUPABASE_ANON_KEY: 'anon_key_123',
      });
      mockConfigLoaderLoad.mockReturnValue(mockConfig);

      const { initializeConfig, validateEnvironment } = await import('../../src/lib/config');
      initializeConfig();

      expect(() => validateEnvironment()).not.toThrow();
    });

    it('should handle different API URLs', async () => {
      const mockConfig = createMockConfig({
        NEXT_PUBLIC_API_URL: 'https://api.production.com',
        apiUrl: 'https://api.production.com',
      });
      mockConfigLoaderLoad.mockReturnValue(mockConfig);

      const { initializeConfig, getClientConfig } = await import('../../src/lib/config');
      initializeConfig();
      const clientConfig = getClientConfig();

      expect(clientConfig.apiUrl).toBe('https://api.production.com');
    });

    it('should handle config initialization errors gracefully', async () => {
      mockConfigLoaderLoad.mockImplementation(() => {
        throw new Error('Network error loading config');
      });

      const { initializeConfig } = await import('../../src/lib/config');

      expect(() => initializeConfig()).toThrow('Network error loading config');
      expect(consoleErrorSpy).toHaveBeenCalled();
    });
  });
});
