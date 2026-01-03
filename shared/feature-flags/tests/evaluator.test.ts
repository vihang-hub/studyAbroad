/**
 * Tests for FeatureFlags evaluator
 */

import { describe, it, expect, beforeEach, afterEach } from 'vitest';
import { ConfigLoader } from '@study-abroad/shared-config';
import { FeatureFlags } from '../src/evaluator';
import { Feature } from '../src/types';

describe('FeatureFlags', () => {
  const originalEnv = { ...process.env };

  beforeEach(() => {
    // Reset singleton instances before each test
    FeatureFlags.reset();
    ConfigLoader.reset();
    // Clear environment variables
    process.env = {};
  });

  afterEach(() => {
    // Restore original environment
    process.env = originalEnv;
    FeatureFlags.reset();
    ConfigLoader.reset();
  });

  describe('isEnabled()', () => {
    it('should return false for ENABLE_SUPABASE in dev mode', () => {
      // Arrange
      process.env.ENVIRONMENT_MODE = 'dev';
      process.env.DATABASE_URL = 'postgresql://localhost:5432/test';
      process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY = 'pk_test_123';
      process.env.CLERK_SECRET_KEY = 'sk_test_123';
      process.env.GEMINI_API_KEY = 'test_key';

      // Act
      const result = FeatureFlags.isEnabled(Feature.SUPABASE);

      // Assert
      expect(result).toBe(false);
    });

    it('should return false for ENABLE_PAYMENTS in dev mode', () => {
      // Arrange
      process.env.ENVIRONMENT_MODE = 'dev';
      process.env.DATABASE_URL = 'postgresql://localhost:5432/test';
      process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY = 'pk_test_123';
      process.env.CLERK_SECRET_KEY = 'sk_test_123';
      process.env.GEMINI_API_KEY = 'test_key';

      // Act
      const result = FeatureFlags.isEnabled(Feature.PAYMENTS);

      // Assert
      expect(result).toBe(false);
    });

    it('should return true for ENABLE_SUPABASE when set to true', () => {
      // Arrange
      process.env.ENVIRONMENT_MODE = 'test';
      process.env.DATABASE_URL = 'postgresql://localhost:5432/test';
      process.env.ENABLE_SUPABASE = 'true';
      process.env.SUPABASE_URL = 'https://test.supabase.co';
      process.env.SUPABASE_ANON_KEY = 'test_anon_key';
      process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY = 'pk_test_123';
      process.env.CLERK_SECRET_KEY = 'sk_test_123';
      process.env.GEMINI_API_KEY = 'test_key';

      // Act
      const result = FeatureFlags.isEnabled(Feature.SUPABASE);

      // Assert
      expect(result).toBe(true);
    });

    it('should return true for ENABLE_PAYMENTS when set to true', () => {
      // Arrange
      process.env.ENVIRONMENT_MODE = 'production';
      process.env.DATABASE_URL = 'postgresql://localhost:5432/test';
      process.env.ENABLE_SUPABASE = 'true';
      process.env.SUPABASE_URL = 'https://test.supabase.co';
      process.env.SUPABASE_ANON_KEY = 'test_anon_key';
      process.env.ENABLE_PAYMENTS = 'true';
      process.env.NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY = 'pk_test_123';
      process.env.STRIPE_SECRET_KEY = 'sk_test_123';
      process.env.STRIPE_WEBHOOK_SECRET = 'whsec_test_123';
      process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY = 'pk_test_123';
      process.env.CLERK_SECRET_KEY = 'sk_test_123';
      process.env.GEMINI_API_KEY = 'test_key';

      // Act
      const result = FeatureFlags.isEnabled(Feature.PAYMENTS);

      // Assert
      expect(result).toBe(true);
    });

    it('should return true for ENABLE_RATE_LIMITING by default', () => {
      // Arrange
      process.env.ENVIRONMENT_MODE = 'dev';
      process.env.DATABASE_URL = 'postgresql://localhost:5432/test';
      process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY = 'pk_test_123';
      process.env.CLERK_SECRET_KEY = 'sk_test_123';
      process.env.GEMINI_API_KEY = 'test_key';

      // Act
      const result = FeatureFlags.isEnabled(Feature.RATE_LIMITING);

      // Assert
      expect(result).toBe(true); // Default is true per config schema
    });

    it('should return true for ENABLE_RATE_LIMITING when set to true', () => {
      // Arrange
      process.env.ENVIRONMENT_MODE = 'production';
      process.env.DATABASE_URL = 'postgresql://localhost:5432/test';
      process.env.ENABLE_SUPABASE = 'true';
      process.env.SUPABASE_URL = 'https://test.supabase.co';
      process.env.SUPABASE_ANON_KEY = 'test_anon_key';
      process.env.ENABLE_PAYMENTS = 'true';
      process.env.NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY = 'pk_test_123';
      process.env.STRIPE_SECRET_KEY = 'sk_test_123';
      process.env.STRIPE_WEBHOOK_SECRET = 'whsec_test_123';
      process.env.ENABLE_RATE_LIMITING = 'true';
      process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY = 'pk_test_123';
      process.env.CLERK_SECRET_KEY = 'sk_test_123';
      process.env.GEMINI_API_KEY = 'test_key';

      // Act
      const result = FeatureFlags.isEnabled(Feature.RATE_LIMITING);

      // Assert
      expect(result).toBe(true);
    });

    it('should return false for ENABLE_OBSERVABILITY when not set', () => {
      // Arrange
      process.env.ENVIRONMENT_MODE = 'dev';
      process.env.DATABASE_URL = 'postgresql://localhost:5432/test';
      process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY = 'pk_test_123';
      process.env.CLERK_SECRET_KEY = 'sk_test_123';
      process.env.GEMINI_API_KEY = 'test_key';

      // Act
      const result = FeatureFlags.isEnabled(Feature.OBSERVABILITY);

      // Assert
      expect(result).toBe(false);
    });

    it('should return true for ENABLE_OBSERVABILITY when set to true', () => {
      // Arrange
      process.env.ENVIRONMENT_MODE = 'production';
      process.env.DATABASE_URL = 'postgresql://localhost:5432/test';
      process.env.ENABLE_SUPABASE = 'true';
      process.env.SUPABASE_URL = 'https://test.supabase.co';
      process.env.SUPABASE_ANON_KEY = 'test_anon_key';
      process.env.ENABLE_PAYMENTS = 'true';
      process.env.NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY = 'pk_test_123';
      process.env.STRIPE_SECRET_KEY = 'sk_test_123';
      process.env.STRIPE_WEBHOOK_SECRET = 'whsec_test_123';
      process.env.ENABLE_OBSERVABILITY = 'true';
      process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY = 'pk_test_123';
      process.env.CLERK_SECRET_KEY = 'sk_test_123';
      process.env.GEMINI_API_KEY = 'test_key';

      // Act
      const result = FeatureFlags.isEnabled(Feature.OBSERVABILITY);

      // Assert
      expect(result).toBe(true);
    });

    it('should use singleton instance across multiple calls', () => {
      // Arrange
      process.env.ENVIRONMENT_MODE = 'dev';
      process.env.DATABASE_URL = 'postgresql://localhost:5432/test';
      process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY = 'pk_test_123';
      process.env.CLERK_SECRET_KEY = 'sk_test_123';
      process.env.GEMINI_API_KEY = 'test_key';

      // Act
      const result1 = FeatureFlags.isEnabled(Feature.SUPABASE);
      const result2 = FeatureFlags.isEnabled(Feature.SUPABASE);

      // Assert
      expect(result1).toBe(result2);
    });
  });

  describe('getEnvironmentMode()', () => {
    it('should return "dev" for dev environment', () => {
      // Arrange
      process.env.ENVIRONMENT_MODE = 'dev';
      process.env.DATABASE_URL = 'postgresql://localhost:5432/test';
      process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY = 'pk_test_123';
      process.env.CLERK_SECRET_KEY = 'sk_test_123';
      process.env.GEMINI_API_KEY = 'test_key';

      // Act
      const mode = FeatureFlags.getEnvironmentMode();

      // Assert
      expect(mode).toBe('dev');
    });

    it('should return "test" for test environment', () => {
      // Arrange
      process.env.ENVIRONMENT_MODE = 'test';
      process.env.DATABASE_URL = 'postgresql://localhost:5432/test';
      process.env.ENABLE_SUPABASE = 'true';
      process.env.SUPABASE_URL = 'https://test.supabase.co';
      process.env.SUPABASE_ANON_KEY = 'test_anon_key';
      process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY = 'pk_test_123';
      process.env.CLERK_SECRET_KEY = 'sk_test_123';
      process.env.GEMINI_API_KEY = 'test_key';

      // Act
      const mode = FeatureFlags.getEnvironmentMode();

      // Assert
      expect(mode).toBe('test');
    });

    it('should return "production" for production environment', () => {
      // Arrange
      process.env.ENVIRONMENT_MODE = 'production';
      process.env.DATABASE_URL = 'postgresql://localhost:5432/test';
      process.env.ENABLE_SUPABASE = 'true';
      process.env.SUPABASE_URL = 'https://test.supabase.co';
      process.env.SUPABASE_ANON_KEY = 'test_anon_key';
      process.env.ENABLE_PAYMENTS = 'true';
      process.env.NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY = 'pk_test_123';
      process.env.STRIPE_SECRET_KEY = 'sk_test_123';
      process.env.STRIPE_WEBHOOK_SECRET = 'whsec_test_123';
      process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY = 'pk_test_123';
      process.env.CLERK_SECRET_KEY = 'sk_test_123';
      process.env.GEMINI_API_KEY = 'test_key';

      // Act
      const mode = FeatureFlags.getEnvironmentMode();

      // Assert
      expect(mode).toBe('production');
    });
  });

  describe('getAllFlags()', () => {
    it('should return flags with correct defaults in dev mode', () => {
      // Arrange
      process.env.ENVIRONMENT_MODE = 'dev';
      process.env.DATABASE_URL = 'postgresql://localhost:5432/test';
      process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY = 'pk_test_123';
      process.env.CLERK_SECRET_KEY = 'sk_test_123';
      process.env.GEMINI_API_KEY = 'test_key';

      // Act
      const flags = FeatureFlags.getAllFlags();

      // Assert
      expect(flags).toEqual({
        [Feature.SUPABASE]: false,
        [Feature.PAYMENTS]: false,
        [Feature.RATE_LIMITING]: true, // Defaults to true per config schema
        [Feature.OBSERVABILITY]: false,
      });
    });

    it('should return SUPABASE as true when enabled', () => {
      // Arrange
      process.env.ENVIRONMENT_MODE = 'test';
      process.env.DATABASE_URL = 'postgresql://localhost:5432/test';
      process.env.ENABLE_SUPABASE = 'true';
      process.env.SUPABASE_URL = 'https://test.supabase.co';
      process.env.SUPABASE_ANON_KEY = 'test_anon_key';
      process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY = 'pk_test_123';
      process.env.CLERK_SECRET_KEY = 'sk_test_123';
      process.env.GEMINI_API_KEY = 'test_key';

      // Act
      const flags = FeatureFlags.getAllFlags();

      // Assert
      expect(flags[Feature.SUPABASE]).toBe(true);
      expect(flags[Feature.PAYMENTS]).toBe(false);
    });

    it('should return all flags as true when all enabled', () => {
      // Arrange
      process.env.ENVIRONMENT_MODE = 'production';
      process.env.DATABASE_URL = 'postgresql://localhost:5432/test';
      process.env.ENABLE_SUPABASE = 'true';
      process.env.SUPABASE_URL = 'https://test.supabase.co';
      process.env.SUPABASE_ANON_KEY = 'test_anon_key';
      process.env.ENABLE_PAYMENTS = 'true';
      process.env.NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY = 'pk_test_123';
      process.env.STRIPE_SECRET_KEY = 'sk_test_123';
      process.env.STRIPE_WEBHOOK_SECRET = 'whsec_test_123';
      process.env.ENABLE_RATE_LIMITING = 'true';
      process.env.ENABLE_OBSERVABILITY = 'true';
      process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY = 'pk_test_123';
      process.env.CLERK_SECRET_KEY = 'sk_test_123';
      process.env.GEMINI_API_KEY = 'test_key';

      // Act
      const flags = FeatureFlags.getAllFlags();

      // Assert
      expect(flags).toEqual({
        [Feature.SUPABASE]: true,
        [Feature.PAYMENTS]: true,
        [Feature.RATE_LIMITING]: true,
        [Feature.OBSERVABILITY]: true,
      });
    });

    it('should include all 4 feature flags', () => {
      // Arrange
      process.env.ENVIRONMENT_MODE = 'dev';
      process.env.DATABASE_URL = 'postgresql://localhost:5432/test';
      process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY = 'pk_test_123';
      process.env.CLERK_SECRET_KEY = 'sk_test_123';
      process.env.GEMINI_API_KEY = 'test_key';

      // Act
      const flags = FeatureFlags.getAllFlags();

      // Assert
      expect(Object.keys(flags)).toHaveLength(4);
    });
  });

  describe('requireEnabled()', () => {
    it('should not throw when feature is enabled', () => {
      // Arrange
      process.env.ENVIRONMENT_MODE = 'test';
      process.env.DATABASE_URL = 'postgresql://localhost:5432/test';
      process.env.ENABLE_SUPABASE = 'true';
      process.env.SUPABASE_URL = 'https://test.supabase.co';
      process.env.SUPABASE_ANON_KEY = 'test_anon_key';
      process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY = 'pk_test_123';
      process.env.CLERK_SECRET_KEY = 'sk_test_123';
      process.env.GEMINI_API_KEY = 'test_key';

      // Act & Assert
      expect(() => FeatureFlags.requireEnabled(Feature.SUPABASE)).not.toThrow();
    });

    it('should throw when feature is disabled', () => {
      // Arrange
      process.env.ENVIRONMENT_MODE = 'dev';
      process.env.DATABASE_URL = 'postgresql://localhost:5432/test';
      process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY = 'pk_test_123';
      process.env.CLERK_SECRET_KEY = 'sk_test_123';
      process.env.GEMINI_API_KEY = 'test_key';

      // Act & Assert
      expect(() => FeatureFlags.requireEnabled(Feature.PAYMENTS)).toThrow(
        'Feature ENABLE_PAYMENTS is required but not enabled in dev environment',
      );
    });

    it('should include feature name in error message', () => {
      // Arrange
      process.env.ENVIRONMENT_MODE = 'dev';
      process.env.DATABASE_URL = 'postgresql://localhost:5432/test';
      process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY = 'pk_test_123';
      process.env.CLERK_SECRET_KEY = 'sk_test_123';
      process.env.GEMINI_API_KEY = 'test_key';

      // Act & Assert
      expect(() => FeatureFlags.requireEnabled(Feature.SUPABASE)).toThrow(/ENABLE_SUPABASE/);
    });

    it('should include environment mode in error message', () => {
      // Arrange
      process.env.ENVIRONMENT_MODE = 'test';
      process.env.DATABASE_URL = 'postgresql://localhost:5432/test';
      process.env.ENABLE_SUPABASE = 'true';
      process.env.SUPABASE_URL = 'https://test.supabase.co';
      process.env.SUPABASE_ANON_KEY = 'test_anon_key';
      process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY = 'pk_test_123';
      process.env.CLERK_SECRET_KEY = 'sk_test_123';
      process.env.GEMINI_API_KEY = 'test_key';

      // Act & Assert
      expect(() => FeatureFlags.requireEnabled(Feature.PAYMENTS)).toThrow(/test environment/);
    });

    it('should provide helpful message about setting environment variable', () => {
      // Arrange
      process.env.ENVIRONMENT_MODE = 'dev';
      process.env.DATABASE_URL = 'postgresql://localhost:5432/test';
      process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY = 'pk_test_123';
      process.env.CLERK_SECRET_KEY = 'sk_test_123';
      process.env.GEMINI_API_KEY = 'test_key';

      // Act & Assert
      expect(() => FeatureFlags.requireEnabled(Feature.PAYMENTS)).toThrow(/Set ENABLE_PAYMENTS=true/);
    });
  });

  describe('reset()', () => {
    it('should reset singleton instance', () => {
      // Arrange
      process.env.ENVIRONMENT_MODE = 'dev';
      process.env.DATABASE_URL = 'postgresql://localhost:5432/test';
      process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY = 'pk_test_123';
      process.env.CLERK_SECRET_KEY = 'sk_test_123';
      process.env.GEMINI_API_KEY = 'test_key';

      // Initialize instance
      FeatureFlags.isEnabled(Feature.SUPABASE);

      // Act
      FeatureFlags.reset();

      // Change environment to test mode with Supabase enabled
      process.env.ENVIRONMENT_MODE = 'test';
      process.env.ENABLE_SUPABASE = 'true';
      process.env.SUPABASE_URL = 'https://test.supabase.co';
      process.env.SUPABASE_ANON_KEY = 'test_anon_key';
      ConfigLoader.reset();

      // Assert - should pick up new configuration
      const result = FeatureFlags.isEnabled(Feature.SUPABASE);
      expect(result).toBe(true);
    });
  });
});
