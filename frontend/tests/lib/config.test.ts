/**
 * Tests for configuration management
 * Coverage target: 100% (high-impact file: ~8-10% total frontend coverage)
 */

import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import {
  initializeConfig,
  getConfig,
  getConfigValue,
  getClientConfig,
  isDevelopment,
  isProduction,
  isTest,
  validateEnvironment,
  ConfigLoader,
} from '../../src/lib/config';
import type { EnvironmentConfig } from '@study-abroad/shared-config';

// Mock the ConfigLoader
vi.mock('@study-abroad/shared-config', () => {
  const mockLoad = vi.fn();
  return {
    ConfigLoader: {
      load: mockLoad,
    },
  };
});

// Mock console methods
const consoleLogSpy = vi.spyOn(console, 'log').mockImplementation(() => {});
const consoleErrorSpy = vi.spyOn(console, 'error').mockImplementation(() => {});

// Mock environment config
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
  beforeEach(() => {
    vi.clearAllMocks();
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
  });

  describe('initializeConfig', () => {
    it('should initialize configuration successfully', () => {
      const mockConfig = createMockConfig();
      ConfigLoader.load.mockReturnValue(mockConfig);

      const config = initializeConfig();

      expect(config).toBeDefined();
      expect(config.ENVIRONMENT_MODE).toBe('test');
      expect(ConfigLoader.load).toHaveBeenCalled();
    });

    it('should return same instance on multiple calls', () => {
      const mockConfig = createMockConfig();
      ConfigLoader.load.mockReturnValue(mockConfig);

      const config1 = initializeConfig();
      const config2 = initializeConfig();

      expect(config1).toBe(config2);
      expect(ConfigLoader.load).toHaveBeenCalledTimes(1);
    });

    it('should log initialization in development mode', () => {
      const mockConfig = createMockConfig({
        ENVIRONMENT_MODE: 'dev',
      });
      ConfigLoader.load.mockReturnValue(mockConfig);

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

    it('should not log in non-development mode', () => {
      const mockConfig = createMockConfig({
        ENVIRONMENT_MODE: 'production',
      });
      ConfigLoader.load.mockReturnValue(mockConfig);

      consoleLogSpy.mockClear();
      initializeConfig();

      expect(consoleLogSpy).not.toHaveBeenCalled();
    });

    it('should throw error if ConfigLoader fails', () => {
      const error = new Error('Failed to load config');
      ConfigLoader.load.mockImplementation(() => {
        throw error;
      });

      expect(() => initializeConfig()).toThrow('Failed to load config');
      expect(consoleErrorSpy).toHaveBeenCalledWith(
        '[Config] Failed to initialize configuration:',
        error
      );
    });

    it('should handle ConfigLoader returning null', () => {
      ConfigLoader.load.mockReturnValue(null as any);

      expect(() => initializeConfig()).not.toThrow();
    });
  });

  describe('getConfig', () => {
    it('should return initialized config', () => {
      const mockConfig = createMockConfig();
      ConfigLoader.load.mockReturnValue(mockConfig);

      initializeConfig();
      const config = getConfig();

      expect(config).toBeDefined();
      expect(config.ENVIRONMENT_MODE).toBe('test');
    });

    it('should throw error if config not initialized', () => {
      // Reset module to clear singleton
      vi.resetModules();
      const { getConfig: freshGetConfig } = require('../../src/lib/config');

      expect(() => freshGetConfig()).toThrow(
        'Configuration not initialized. Call initializeConfig() first.'
      );
    });
  });

  describe('getConfigValue', () => {
    it('should return specific config value', () => {
      const mockConfig = createMockConfig({
        ENVIRONMENT_MODE: 'production',
      });
      ConfigLoader.load.mockReturnValue(mockConfig);

      initializeConfig();
      const mode = getConfigValue('ENVIRONMENT_MODE');

      expect(mode).toBe('production');
    });

    it('should return different config values', () => {
      const mockConfig = createMockConfig({
        NEXT_PUBLIC_API_URL: 'https://api.example.com',
        ENABLE_SUPABASE: true,
      });
      ConfigLoader.load.mockReturnValue(mockConfig);

      initializeConfig();

      expect(getConfigValue('NEXT_PUBLIC_API_URL')).toBe('https://api.example.com');
      expect(getConfigValue('ENABLE_SUPABASE')).toBe(true);
    });

    it('should maintain type safety', () => {
      const mockConfig = createMockConfig({
        ENABLE_PAYMENTS: true,
      });
      ConfigLoader.load.mockReturnValue(mockConfig);

      initializeConfig();
      const enablePayments = getConfigValue('ENABLE_PAYMENTS');

      expect(typeof enablePayments).toBe('boolean');
      expect(enablePayments).toBe(true);
    });
  });

  describe('getClientConfig', () => {
    it('should return only client-safe configuration', () => {
      const mockConfig = createMockConfig({
        ENVIRONMENT_MODE: 'dev',
        NEXT_PUBLIC_API_URL: 'http://localhost:8000',
        ENABLE_SUPABASE: true,
        ENABLE_PAYMENTS: true,
        SUPABASE_URL: 'https://supabase.example.com',
        SUPABASE_ANON_KEY: 'anon_key_123',
        CLERK_SECRET_KEY: 'secret_that_should_not_be_exposed',
      });
      ConfigLoader.load.mockReturnValue(mockConfig);

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

    it('should handle disabled features', () => {
      const mockConfig = createMockConfig({
        ENABLE_SUPABASE: false,
        ENABLE_PAYMENTS: false,
      });
      ConfigLoader.load.mockReturnValue(mockConfig);

      initializeConfig();
      const clientConfig = getClientConfig();

      expect(clientConfig.enableSupabase).toBe(false);
      expect(clientConfig.enablePayments).toBe(false);
    });
  });

  describe('Environment mode helpers', () => {
    describe('isDevelopment', () => {
      it('should return true in development mode', () => {
        const mockConfig = createMockConfig({
          ENVIRONMENT_MODE: 'dev',
        });
        ConfigLoader.load.mockReturnValue(mockConfig);

        initializeConfig();

        expect(isDevelopment()).toBe(true);
      });

      it('should return false in non-development mode', () => {
        const mockConfig = createMockConfig({
          ENVIRONMENT_MODE: 'production',
        });
        ConfigLoader.load.mockReturnValue(mockConfig);

        initializeConfig();

        expect(isDevelopment()).toBe(false);
      });
    });

    describe('isProduction', () => {
      it('should return true in production mode', () => {
        const mockConfig = createMockConfig({
          ENVIRONMENT_MODE: 'production',
        });
        ConfigLoader.load.mockReturnValue(mockConfig);

        initializeConfig();

        expect(isProduction()).toBe(true);
      });

      it('should return false in non-production mode', () => {
        const mockConfig = createMockConfig({
          ENVIRONMENT_MODE: 'dev',
        });
        ConfigLoader.load.mockReturnValue(mockConfig);

        initializeConfig();

        expect(isProduction()).toBe(false);
      });
    });

    describe('isTest', () => {
      it('should return true in test mode', () => {
        const mockConfig = createMockConfig({
          ENVIRONMENT_MODE: 'test',
        });
        ConfigLoader.load.mockReturnValue(mockConfig);

        initializeConfig();

        expect(isTest()).toBe(true);
      });

      it('should return false in non-test mode', () => {
        const mockConfig = createMockConfig({
          ENVIRONMENT_MODE: 'production',
        });
        ConfigLoader.load.mockReturnValue(mockConfig);

        initializeConfig();

        expect(isTest()).toBe(false);
      });
    });
  });

  describe('validateEnvironment', () => {
    beforeEach(() => {
      // Set up valid environment
      process.env.NEXT_PUBLIC_API_URL = 'http://localhost:8000';
      process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY = 'pk_test_clerk';
      process.env.CLERK_SECRET_KEY = 'sk_test_clerk';

      const mockConfig = createMockConfig();
      ConfigLoader.load.mockReturnValue(mockConfig);
      initializeConfig();
    });

    it('should pass validation with all required variables', () => {
      expect(() => validateEnvironment()).not.toThrow();
    });

    it('should throw error if NEXT_PUBLIC_API_URL is missing', () => {
      delete process.env.NEXT_PUBLIC_API_URL;

      expect(() => validateEnvironment()).toThrow(
        expect.stringContaining('NEXT_PUBLIC_API_URL')
      );
    });

    it('should throw error if NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY is missing', () => {
      delete process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY;

      expect(() => validateEnvironment()).toThrow(
        expect.stringContaining('NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY')
      );
    });

    it('should throw error if CLERK_SECRET_KEY is missing on server', () => {
      // Simulate server environment
      const originalWindow = global.window;
      // @ts-expect-error Testing server-side behavior
      delete global.window;

      delete process.env.CLERK_SECRET_KEY;

      expect(() => validateEnvironment()).toThrow(
        expect.stringContaining('CLERK_SECRET_KEY')
      );

      // Restore
      global.window = originalWindow;
    });

    it('should not check server variables on client', () => {
      // Simulate browser environment
      global.window = {} as any;

      delete process.env.CLERK_SECRET_KEY;

      // Should not throw because we're on client
      expect(() => validateEnvironment()).not.toThrow();
    });

    it('should throw error if multiple variables are missing', () => {
      delete process.env.NEXT_PUBLIC_API_URL;
      delete process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY;

      try {
        validateEnvironment();
        expect.fail('Should have thrown');
      } catch (error: any) {
        expect(error.message).toContain('NEXT_PUBLIC_API_URL');
        expect(error.message).toContain('NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY');
      }
    });

    it('should validate Supabase config when enabled', () => {
      const mockConfig = createMockConfig({
        ENABLE_SUPABASE: true,
        SUPABASE_URL: '',
        SUPABASE_ANON_KEY: '',
      });
      ConfigLoader.load.mockReturnValue(mockConfig);

      expect(() => validateEnvironment()).toThrow(
        expect.stringContaining('Supabase is enabled')
      );
    });

    it('should pass Supabase validation when properly configured', () => {
      const mockConfig = createMockConfig({
        ENABLE_SUPABASE: true,
        SUPABASE_URL: 'https://supabase.example.com',
        SUPABASE_ANON_KEY: 'anon_key_123',
      });
      ConfigLoader.load.mockReturnValue(mockConfig);

      expect(() => validateEnvironment()).not.toThrow();
    });

    it('should not validate Supabase when disabled', () => {
      const mockConfig = createMockConfig({
        ENABLE_SUPABASE: false,
        SUPABASE_URL: '',
        SUPABASE_ANON_KEY: '',
      });
      ConfigLoader.load.mockReturnValue(mockConfig);

      expect(() => validateEnvironment()).not.toThrow();
    });

    it('should validate Stripe config when payments enabled on client', () => {
      global.window = {} as any;

      const mockConfig = createMockConfig({
        ENABLE_PAYMENTS: true,
      });
      ConfigLoader.load.mockReturnValue(mockConfig);

      delete process.env.NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY;

      expect(() => validateEnvironment()).toThrow(
        expect.stringContaining('NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY')
      );
    });

    it('should pass Stripe validation when properly configured', () => {
      global.window = {} as any;

      const mockConfig = createMockConfig({
        ENABLE_PAYMENTS: true,
      });
      ConfigLoader.load.mockReturnValue(mockConfig);

      process.env.NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY = 'pk_test_stripe';

      expect(() => validateEnvironment()).not.toThrow();
    });

    it('should not validate Stripe on server', () => {
      // Simulate server
      const originalWindow = global.window;
      // @ts-expect-error Testing server-side behavior
      delete global.window;

      const mockConfig = createMockConfig({
        ENABLE_PAYMENTS: true,
      });
      ConfigLoader.load.mockReturnValue(mockConfig);

      delete process.env.NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY;

      // Should not throw on server
      expect(() => validateEnvironment()).not.toThrow();

      global.window = originalWindow;
    });

    it('should not validate Stripe when payments disabled', () => {
      global.window = {} as any;

      const mockConfig = createMockConfig({
        ENABLE_PAYMENTS: false,
      });
      ConfigLoader.load.mockReturnValue(mockConfig);

      delete process.env.NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY;

      expect(() => validateEnvironment()).not.toThrow();
    });
  });

  describe('ConfigLoader export', () => {
    it('should export ConfigLoader for advanced use cases', () => {
      expect(ConfigLoader).toBeDefined();
      expect(ConfigLoader.load).toBeInstanceOf(Function);
    });
  });

  describe('Edge cases', () => {
    it('should handle empty string environment variables', () => {
      process.env.NEXT_PUBLIC_API_URL = '';
      process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY = '';

      expect(() => validateEnvironment()).toThrow();
    });

    it('should handle whitespace-only environment variables', () => {
      process.env.NEXT_PUBLIC_API_URL = '   ';
      process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY = '   ';

      // Whitespace values are technically set, validation should pass
      // (ConfigLoader would handle validation of actual values)
      expect(() => validateEnvironment()).not.toThrow();
    });

    it('should handle config with all features enabled', () => {
      global.window = {} as any;

      const mockConfig = createMockConfig({
        ENABLE_SUPABASE: true,
        ENABLE_PAYMENTS: true,
        SUPABASE_URL: 'https://supabase.example.com',
        SUPABASE_ANON_KEY: 'anon_key_123',
      });
      ConfigLoader.load.mockReturnValue(mockConfig);

      process.env.NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY = 'pk_test_stripe';

      expect(() => validateEnvironment()).not.toThrow();
    });

    it('should handle different API URLs', () => {
      const mockConfig = createMockConfig({
        NEXT_PUBLIC_API_URL: 'https://api.production.com',
        apiUrl: 'https://api.production.com',
      });
      ConfigLoader.load.mockReturnValue(mockConfig);

      initializeConfig();
      const clientConfig = getClientConfig();

      expect(clientConfig.apiUrl).toBe('https://api.production.com');
    });

    it('should handle config initialization errors gracefully', () => {
      ConfigLoader.load.mockImplementation(() => {
        throw new Error('Network error loading config');
      });

      expect(() => initializeConfig()).toThrow('Network error loading config');
      expect(consoleErrorSpy).toHaveBeenCalled();
    });
  });
});
