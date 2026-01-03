/**
 * Tests for Clerk configuration utilities
 */

import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';

// Mock the config module
vi.mock('../../src/lib/config', () => ({
  getConfig: vi.fn(),
}));

describe('clerk', () => {
  const originalEnv = { ...process.env };

  beforeEach(() => {
    vi.clearAllMocks();
    vi.resetModules();
    // Reset environment variables
    process.env = { ...originalEnv };
  });

  afterEach(() => {
    process.env = originalEnv;
    vi.resetModules();
  });

  describe('getClerkConfig', () => {
    it('should return Clerk configuration from config', async () => {
      const mockConfig = {
        clerkPublishableKey: 'pk_test_xxx',
        clerkSecretKey: 'sk_test_xxx',
      };

      const { getConfig } = await import('../../src/lib/config');
      (getConfig as unknown as ReturnType<typeof vi.fn>).mockReturnValue(mockConfig);

      const { getClerkConfig } = await import('../../src/lib/clerk');
      const config = getClerkConfig();

      expect(config).toEqual({
        publishableKey: 'pk_test_xxx',
        secretKey: 'sk_test_xxx',
      });
    });

    it('should handle undefined values', async () => {
      const mockConfig = {
        clerkPublishableKey: undefined,
        clerkSecretKey: undefined,
      };

      const { getConfig } = await import('../../src/lib/config');
      (getConfig as unknown as ReturnType<typeof vi.fn>).mockReturnValue(mockConfig);

      const { getClerkConfig } = await import('../../src/lib/clerk');
      const config = getClerkConfig();

      expect(config).toEqual({
        publishableKey: undefined,
        secretKey: undefined,
      });
    });
  });

  describe('isClerkConfigured', () => {
    it('should return true when both keys are properly configured', async () => {
      process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY = 'pk_test_real_key_123';
      process.env.CLERK_SECRET_KEY = 'sk_test_real_key_456';

      const { isClerkConfigured } = await import('../../src/lib/clerk');
      expect(isClerkConfigured()).toBe(true);
    });

    it('should return false when publishable key is empty', async () => {
      process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY = '';
      process.env.CLERK_SECRET_KEY = 'sk_test_real_key_456';

      const { isClerkConfigured } = await import('../../src/lib/clerk');
      expect(isClerkConfigured()).toBe(false);
    });

    it('should return false when secret key is empty', async () => {
      process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY = 'pk_test_real_key_123';
      process.env.CLERK_SECRET_KEY = '';

      const { isClerkConfigured } = await import('../../src/lib/clerk');
      expect(isClerkConfigured()).toBe(false);
    });

    it('should return false when publishable key contains YOUR_', async () => {
      process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY = 'pk_test_YOUR_clerk_key';
      process.env.CLERK_SECRET_KEY = 'sk_test_real_key_456';

      const { isClerkConfigured } = await import('../../src/lib/clerk');
      expect(isClerkConfigured()).toBe(false);
    });

    it('should return false when publishable key contains your_', async () => {
      process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY = 'pk_test_your_clerk_key';
      process.env.CLERK_SECRET_KEY = 'sk_test_real_key_456';

      const { isClerkConfigured } = await import('../../src/lib/clerk');
      expect(isClerkConfigured()).toBe(false);
    });

    it('should return false when secret key contains YOUR_', async () => {
      process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY = 'pk_test_real_key_123';
      process.env.CLERK_SECRET_KEY = 'sk_test_YOUR_secret_key';

      const { isClerkConfigured } = await import('../../src/lib/clerk');
      expect(isClerkConfigured()).toBe(false);
    });

    it('should return false when secret key contains your_', async () => {
      process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY = 'pk_test_real_key_123';
      process.env.CLERK_SECRET_KEY = 'sk_test_your_secret_key';

      const { isClerkConfigured } = await import('../../src/lib/clerk');
      expect(isClerkConfigured()).toBe(false);
    });

    it('should return false when publishable key is placeholder', async () => {
      process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY = 'pk_test_your_clerk_publishable_key';
      process.env.CLERK_SECRET_KEY = 'sk_test_real_key_456';

      const { isClerkConfigured } = await import('../../src/lib/clerk');
      expect(isClerkConfigured()).toBe(false);
    });

    it('should return false when secret key is placeholder', async () => {
      process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY = 'pk_test_real_key_123';
      process.env.CLERK_SECRET_KEY = 'sk_test_your_clerk_secret_key';

      const { isClerkConfigured } = await import('../../src/lib/clerk');
      expect(isClerkConfigured()).toBe(false);
    });

    it('should return false when both keys are missing', async () => {
      delete process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY;
      delete process.env.CLERK_SECRET_KEY;

      const { isClerkConfigured } = await import('../../src/lib/clerk');
      expect(isClerkConfigured()).toBe(false);
    });
  });

  describe('getClerkStatus', () => {
    it('should return configured status when Clerk is properly configured', async () => {
      process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY = 'pk_test_real_key_123';
      process.env.CLERK_SECRET_KEY = 'sk_test_real_key_456';

      const { getClerkStatus } = await import('../../src/lib/clerk');
      const status = getClerkStatus();

      expect(status.configured).toBe(true);
      expect(status.message).toBe('Clerk authentication is properly configured');
    });

    it('should return not configured status when Clerk has placeholder keys', async () => {
      process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY = 'pk_test_your_clerk_publishable_key';
      process.env.CLERK_SECRET_KEY = 'sk_test_your_clerk_secret_key';

      const { getClerkStatus } = await import('../../src/lib/clerk');
      const status = getClerkStatus();

      expect(status.configured).toBe(false);
      expect(status.message).toContain('placeholder keys');
      expect(status.message).toContain('CLERK-SETUP-GUIDE.md');
    });

    it('should return not configured status when keys are empty', async () => {
      process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY = '';
      process.env.CLERK_SECRET_KEY = '';

      const { getClerkStatus } = await import('../../src/lib/clerk');
      const status = getClerkStatus();

      expect(status.configured).toBe(false);
      expect(status.message).toContain('placeholder keys');
    });
  });
});
