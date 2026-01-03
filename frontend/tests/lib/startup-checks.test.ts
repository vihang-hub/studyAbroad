/**
 * Tests for startup checks
 */

import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';

// Mock clerk module
vi.mock('../../src/lib/clerk', () => ({
  getClerkStatus: vi.fn(),
}));

describe('startup-checks', () => {
  const originalEnv = process.env.NODE_ENV;
  let consoleWarnSpy: ReturnType<typeof vi.spyOn>;

  beforeEach(() => {
    vi.clearAllMocks();
    vi.resetModules();
    consoleWarnSpy = vi.spyOn(console, 'warn').mockImplementation(() => {});
  });

  afterEach(() => {
    process.env.NODE_ENV = originalEnv;
    consoleWarnSpy.mockRestore();
  });

  describe('runStartupChecks', () => {
    it('should skip checks in production environment', async () => {
      process.env.NODE_ENV = 'production';

      const { getClerkStatus } = await import('../../src/lib/clerk');
      const { runStartupChecks } = await import('../../src/lib/startup-checks');

      runStartupChecks();

      expect(getClerkStatus).not.toHaveBeenCalled();
      expect(consoleWarnSpy).not.toHaveBeenCalled();
    });

    it('should run checks in development environment', async () => {
      process.env.NODE_ENV = 'development';

      const { getClerkStatus } = await import('../../src/lib/clerk');
      (getClerkStatus as unknown as ReturnType<typeof vi.fn>).mockReturnValue({
        configured: true,
        message: 'Clerk is configured',
      });

      const { runStartupChecks } = await import('../../src/lib/startup-checks');

      runStartupChecks();

      expect(getClerkStatus).toHaveBeenCalled();
    });

    it('should run checks in test environment', async () => {
      process.env.NODE_ENV = 'test';

      const { getClerkStatus } = await import('../../src/lib/clerk');
      (getClerkStatus as unknown as ReturnType<typeof vi.fn>).mockReturnValue({
        configured: true,
        message: 'Clerk is configured',
      });

      const { runStartupChecks } = await import('../../src/lib/startup-checks');

      runStartupChecks();

      expect(getClerkStatus).toHaveBeenCalled();
    });

    it('should not log warnings when Clerk is configured', async () => {
      process.env.NODE_ENV = 'development';

      const { getClerkStatus } = await import('../../src/lib/clerk');
      (getClerkStatus as unknown as ReturnType<typeof vi.fn>).mockReturnValue({
        configured: true,
        message: 'Clerk authentication is properly configured',
      });

      const { runStartupChecks } = await import('../../src/lib/startup-checks');

      runStartupChecks();

      expect(consoleWarnSpy).not.toHaveBeenCalled();
    });

    it('should log warnings when Clerk is not configured', async () => {
      process.env.NODE_ENV = 'development';

      const { getClerkStatus } = await import('../../src/lib/clerk');
      (getClerkStatus as unknown as ReturnType<typeof vi.fn>).mockReturnValue({
        configured: false,
        message: 'Clerk is using placeholder keys',
      });

      const { runStartupChecks } = await import('../../src/lib/startup-checks');

      runStartupChecks();

      expect(consoleWarnSpy).toHaveBeenCalled();
    });

    it('should display configuration warning header', async () => {
      process.env.NODE_ENV = 'development';

      const { getClerkStatus } = await import('../../src/lib/clerk');
      (getClerkStatus as unknown as ReturnType<typeof vi.fn>).mockReturnValue({
        configured: false,
        message: 'Clerk is not configured',
      });

      const { runStartupChecks } = await import('../../src/lib/startup-checks');

      runStartupChecks();

      expect(consoleWarnSpy).toHaveBeenCalledWith(expect.stringContaining('CLERK CONFIGURATION WARNING'));
    });

    it('should display Clerk status message', async () => {
      process.env.NODE_ENV = 'development';
      const statusMessage = 'Custom clerk status message';

      const { getClerkStatus } = await import('../../src/lib/clerk');
      (getClerkStatus as unknown as ReturnType<typeof vi.fn>).mockReturnValue({
        configured: false,
        message: statusMessage,
      });

      const { runStartupChecks } = await import('../../src/lib/startup-checks');

      runStartupChecks();

      expect(consoleWarnSpy).toHaveBeenCalledWith(statusMessage);
    });

    it('should display quick setup instructions', async () => {
      process.env.NODE_ENV = 'development';

      const { getClerkStatus } = await import('../../src/lib/clerk');
      (getClerkStatus as unknown as ReturnType<typeof vi.fn>).mockReturnValue({
        configured: false,
        message: 'Not configured',
      });

      const { runStartupChecks } = await import('../../src/lib/startup-checks');

      runStartupChecks();

      expect(consoleWarnSpy).toHaveBeenCalledWith(expect.stringContaining('Quick setup'));
      expect(consoleWarnSpy).toHaveBeenCalledWith(expect.stringContaining('clerk.com'));
    });

    it('should reference CLERK-SETUP-GUIDE.md', async () => {
      process.env.NODE_ENV = 'development';

      const { getClerkStatus } = await import('../../src/lib/clerk');
      (getClerkStatus as unknown as ReturnType<typeof vi.fn>).mockReturnValue({
        configured: false,
        message: 'Not configured',
      });

      const { runStartupChecks } = await import('../../src/lib/startup-checks');

      runStartupChecks();

      expect(consoleWarnSpy).toHaveBeenCalledWith(expect.stringContaining('CLERK-SETUP-GUIDE.md'));
    });

    it('should display numbered setup steps', async () => {
      process.env.NODE_ENV = 'development';

      const { getClerkStatus } = await import('../../src/lib/clerk');
      (getClerkStatus as unknown as ReturnType<typeof vi.fn>).mockReturnValue({
        configured: false,
        message: 'Not configured',
      });

      const { runStartupChecks } = await import('../../src/lib/startup-checks');

      runStartupChecks();

      // Check for numbered steps
      expect(consoleWarnSpy).toHaveBeenCalledWith(expect.stringContaining('1.'));
      expect(consoleWarnSpy).toHaveBeenCalledWith(expect.stringContaining('2.'));
      expect(consoleWarnSpy).toHaveBeenCalledWith(expect.stringContaining('3.'));
      expect(consoleWarnSpy).toHaveBeenCalledWith(expect.stringContaining('4.'));
    });
  });
});
