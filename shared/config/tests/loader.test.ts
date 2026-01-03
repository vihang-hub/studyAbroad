/**
 * Tests for ConfigLoader
 *
 * Verifies environment configuration loading and validation.
 */

import { describe, it, expect, beforeEach, afterEach } from 'vitest';
import { ConfigLoader } from '../src/loader';

describe('ConfigLoader', () => {
  const originalEnv = { ...process.env };

  beforeEach(() => {
    // Reset singleton before each test
    ConfigLoader.reset();
    // Clear environment variables
    process.env = {};
  });

  afterEach(() => {
    // Restore original environment
    process.env = originalEnv;
    ConfigLoader.reset();
  });

  describe('load()', () => {
    it('should load valid dev configuration', () => {
      // Arrange
      process.env.ENVIRONMENT_MODE = 'dev';
      process.env.DATABASE_URL = 'postgresql://localhost:5432/test';
      process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY = 'pk_test_123';
      process.env.CLERK_SECRET_KEY = 'sk_test_123';
      process.env.GEMINI_API_KEY = 'test_key';

      // Act
      const config = ConfigLoader.load();

      // Assert
      expect(config.ENVIRONMENT_MODE).toBe('dev');
      expect(config.DATABASE_URL).toBe('postgresql://localhost:5432/test');
      expect(config.ENABLE_SUPABASE).toBe(false);
      expect(config.ENABLE_PAYMENTS).toBe(false);
      expect(config.LOG_LEVEL).toBe('debug');
    });

    it('should load valid test configuration', () => {
      // Arrange
      process.env.ENVIRONMENT_MODE = 'test';
      process.env.DATABASE_URL = 'postgresql://localhost:5432/test';
      process.env.ENABLE_SUPABASE = 'true';
      process.env.SUPABASE_URL = 'https://test.supabase.co';
      process.env.SUPABASE_ANON_KEY = 'anon_key';
      process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY = 'pk_test_123';
      process.env.CLERK_SECRET_KEY = 'sk_test_123';
      process.env.GEMINI_API_KEY = 'test_key';

      // Act
      const config = ConfigLoader.load();

      // Assert
      expect(config.ENVIRONMENT_MODE).toBe('test');
      expect(config.ENABLE_SUPABASE).toBe(true);
      expect(config.ENABLE_PAYMENTS).toBe(false);
      expect(config.SUPABASE_URL).toBe('https://test.supabase.co');
    });

    it('should load valid production configuration', () => {
      // Arrange
      process.env.ENVIRONMENT_MODE = 'production';
      process.env.DATABASE_URL = 'postgresql://prod:5432/app';
      process.env.ENABLE_SUPABASE = 'true';
      process.env.ENABLE_PAYMENTS = 'true';
      process.env.SUPABASE_URL = 'https://prod.supabase.co';
      process.env.SUPABASE_ANON_KEY = 'anon_key';
      process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY = 'pk_live_123';
      process.env.CLERK_SECRET_KEY = 'sk_live_123';
      process.env.NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY = 'pk_live_stripe';
      process.env.STRIPE_SECRET_KEY = 'sk_live_stripe';
      process.env.STRIPE_WEBHOOK_SECRET = 'whsec_stripe';
      process.env.GEMINI_API_KEY = 'prod_key';

      // Act
      const config = ConfigLoader.load();

      // Assert
      expect(config.ENVIRONMENT_MODE).toBe('production');
      expect(config.ENABLE_SUPABASE).toBe(true);
      expect(config.ENABLE_PAYMENTS).toBe(true);
      expect(config.LOG_LEVEL).toBe('error');
    });

    it('should cache configuration on subsequent calls', () => {
      // Arrange
      process.env.ENVIRONMENT_MODE = 'dev';
      process.env.DATABASE_URL = 'postgresql://localhost:5432/test';
      process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY = 'pk_test_123';
      process.env.CLERK_SECRET_KEY = 'sk_test_123';
      process.env.GEMINI_API_KEY = 'test_key';

      // Act
      const config1 = ConfigLoader.load();
      const config2 = ConfigLoader.load();

      // Assert
      expect(config1).toBe(config2); // Same object reference
    });

    it('should apply default values', () => {
      // Arrange
      process.env.ENVIRONMENT_MODE = 'dev';
      process.env.DATABASE_URL = 'postgresql://localhost:5432/test';
      process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY = 'pk_test_123';
      process.env.CLERK_SECRET_KEY = 'sk_test_123';
      process.env.GEMINI_API_KEY = 'test_key';

      // Act
      const config = ConfigLoader.load();

      // Assert
      expect(config.LOG_MAX_SIZE_MB).toBe(100);
      expect(config.LOG_ROTATION_DAYS).toBe(1);
      expect(config.LOG_RETENTION_DAYS).toBe(30);
      expect(config.LOG_DIR).toBe('./logs');
      expect(config.APP_NAME).toBe('Study Abroad MVP');
    });

    it('should throw on missing required DATABASE_URL', () => {
      // Arrange
      process.env.ENVIRONMENT_MODE = 'dev';
      process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY = 'pk_test_123';
      process.env.CLERK_SECRET_KEY = 'sk_test_123';
      process.env.GEMINI_API_KEY = 'test_key';

      // Act & Assert
      expect(() => ConfigLoader.load()).toThrow('Invalid environment configuration');
    });

    it('should throw on invalid DATABASE_URL', () => {
      // Arrange
      process.env.ENVIRONMENT_MODE = 'dev';
      process.env.DATABASE_URL = 'not-a-valid-url';
      process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY = 'pk_test_123';
      process.env.CLERK_SECRET_KEY = 'sk_test_123';
      process.env.GEMINI_API_KEY = 'test_key';

      // Act & Assert
      expect(() => ConfigLoader.load()).toThrow('Invalid environment configuration');
    });

    it('should throw on missing CLERK_SECRET_KEY', () => {
      // Arrange
      process.env.ENVIRONMENT_MODE = 'dev';
      process.env.DATABASE_URL = 'postgresql://localhost:5432/test';
      process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY = 'pk_test_123';
      process.env.GEMINI_API_KEY = 'test_key';

      // Act & Assert
      expect(() => ConfigLoader.load()).toThrow('Invalid environment configuration');
    });

    it('should throw on missing GEMINI_API_KEY', () => {
      // Arrange
      process.env.ENVIRONMENT_MODE = 'dev';
      process.env.DATABASE_URL = 'postgresql://localhost:5432/test';
      process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY = 'pk_test_123';
      process.env.CLERK_SECRET_KEY = 'sk_test_123';

      // Act & Assert
      expect(() => ConfigLoader.load()).toThrow('Invalid environment configuration');
    });

    it('should enforce dev mode constraints (no Supabase, no payments)', () => {
      // Arrange
      process.env.ENVIRONMENT_MODE = 'dev';
      process.env.DATABASE_URL = 'postgresql://localhost:5432/test';
      process.env.ENABLE_SUPABASE = 'true'; // Should fail validation
      process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY = 'pk_test_123';
      process.env.CLERK_SECRET_KEY = 'sk_test_123';
      process.env.GEMINI_API_KEY = 'test_key';

      // Act & Assert
      expect(() => ConfigLoader.load()).toThrow();
    });

    it('should enforce test mode constraints (Supabase required, no payments)', () => {
      // Arrange
      process.env.ENVIRONMENT_MODE = 'test';
      process.env.DATABASE_URL = 'postgresql://localhost:5432/test';
      process.env.ENABLE_SUPABASE = 'false'; // Should fail validation
      process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY = 'pk_test_123';
      process.env.CLERK_SECRET_KEY = 'sk_test_123';
      process.env.GEMINI_API_KEY = 'test_key';

      // Act & Assert
      expect(() => ConfigLoader.load()).toThrow();
    });

    it('should enforce production mode constraints (Supabase and payments required)', () => {
      // Arrange
      process.env.ENVIRONMENT_MODE = 'production';
      process.env.DATABASE_URL = 'postgresql://prod:5432/app';
      process.env.ENABLE_SUPABASE = 'true';
      process.env.ENABLE_PAYMENTS = 'false'; // Should fail validation
      process.env.SUPABASE_URL = 'https://prod.supabase.co';
      process.env.SUPABASE_ANON_KEY = 'anon_key';
      process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY = 'pk_live_123';
      process.env.CLERK_SECRET_KEY = 'sk_live_123';
      process.env.GEMINI_API_KEY = 'prod_key';

      // Act & Assert
      expect(() => ConfigLoader.load()).toThrow();
    });

    it('should require Supabase config when ENABLE_SUPABASE=true', () => {
      // Arrange
      process.env.ENVIRONMENT_MODE = 'test';
      process.env.DATABASE_URL = 'postgresql://localhost:5432/test';
      process.env.ENABLE_SUPABASE = 'true';
      // Missing SUPABASE_URL and SUPABASE_ANON_KEY
      process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY = 'pk_test_123';
      process.env.CLERK_SECRET_KEY = 'sk_test_123';
      process.env.GEMINI_API_KEY = 'test_key';

      // Act & Assert
      expect(() => ConfigLoader.load()).toThrow();
    });

    it('should require Stripe config when ENABLE_PAYMENTS=true', () => {
      // Arrange
      process.env.ENVIRONMENT_MODE = 'production';
      process.env.DATABASE_URL = 'postgresql://prod:5432/app';
      process.env.ENABLE_SUPABASE = 'true';
      process.env.ENABLE_PAYMENTS = 'true';
      process.env.SUPABASE_URL = 'https://prod.supabase.co';
      process.env.SUPABASE_ANON_KEY = 'anon_key';
      process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY = 'pk_live_123';
      process.env.CLERK_SECRET_KEY = 'sk_live_123';
      process.env.GEMINI_API_KEY = 'prod_key';
      // Missing Stripe keys

      // Act & Assert
      expect(() => ConfigLoader.load()).toThrow();
    });
  });

  describe('get()', () => {
    it('should return specific configuration value', () => {
      // Arrange
      process.env.ENVIRONMENT_MODE = 'dev';
      process.env.DATABASE_URL = 'postgresql://localhost:5432/test';
      process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY = 'pk_test_123';
      process.env.CLERK_SECRET_KEY = 'sk_test_123';
      process.env.GEMINI_API_KEY = 'test_key';
      ConfigLoader.load();

      // Act
      const mode = ConfigLoader.get('ENVIRONMENT_MODE');
      const dbUrl = ConfigLoader.get('DATABASE_URL');

      // Assert
      expect(mode).toBe('dev');
      expect(dbUrl).toBe('postgresql://localhost:5432/test');
    });

    it('should throw if configuration not loaded', () => {
      // Act & Assert
      expect(() => ConfigLoader.get('ENVIRONMENT_MODE')).toThrow(
        'Configuration not loaded'
      );
    });
  });

  describe('isLoaded()', () => {
    it('should return false before load()', () => {
      // Act & Assert
      expect(ConfigLoader.isLoaded()).toBe(false);
    });

    it('should return true after load()', () => {
      // Arrange
      process.env.ENVIRONMENT_MODE = 'dev';
      process.env.DATABASE_URL = 'postgresql://localhost:5432/test';
      process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY = 'pk_test_123';
      process.env.CLERK_SECRET_KEY = 'sk_test_123';
      process.env.GEMINI_API_KEY = 'test_key';
      ConfigLoader.load();

      // Act & Assert
      expect(ConfigLoader.isLoaded()).toBe(true);
    });

    it('should return false after reset()', () => {
      // Arrange
      process.env.ENVIRONMENT_MODE = 'dev';
      process.env.DATABASE_URL = 'postgresql://localhost:5432/test';
      process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY = 'pk_test_123';
      process.env.CLERK_SECRET_KEY = 'sk_test_123';
      process.env.GEMINI_API_KEY = 'test_key';
      ConfigLoader.load();

      // Act
      ConfigLoader.reset();

      // Assert
      expect(ConfigLoader.isLoaded()).toBe(false);
    });
  });

  describe('reload()', () => {
    it('should clear cached instance', () => {
      // Arrange
      process.env.ENVIRONMENT_MODE = 'dev';
      process.env.DATABASE_URL = 'postgresql://localhost:5432/test';
      process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY = 'pk_test_123';
      process.env.CLERK_SECRET_KEY = 'sk_test_123';
      process.env.GEMINI_API_KEY = 'test_key';
      const config1 = ConfigLoader.load();

      // Act
      ConfigLoader.reload();
      const config2 = ConfigLoader.load();

      // Assert
      expect(config1).not.toBe(config2); // Different object references
    });
  });

  describe('reset()', () => {
    it('should be an alias for reload()', () => {
      // Arrange
      process.env.ENVIRONMENT_MODE = 'dev';
      process.env.DATABASE_URL = 'postgresql://localhost:5432/test';
      process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY = 'pk_test_123';
      process.env.CLERK_SECRET_KEY = 'sk_test_123';
      process.env.GEMINI_API_KEY = 'test_key';
      ConfigLoader.load();

      // Act
      ConfigLoader.reset();

      // Assert
      expect(ConfigLoader.isLoaded()).toBe(false);
    });
  });
});
