/**
 * Tests for FeatureFlagProvider
 */

import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { render, screen, waitFor, act } from '@testing-library/react';
import React from 'react';

// Mock dependencies
vi.mock('../../src/lib/config', () => ({
  getConfig: vi.fn(),
}));

vi.mock('../../src/lib/logger', () => ({
  logInfo: vi.fn(),
}));

vi.mock('@study-abroad/shared-feature-flags', () => ({
  FeatureFlags: vi.fn().mockImplementation(() => ({
    isEnabled: vi.fn((feature: string) => feature === 'ENABLE_SUPABASE'),
  })),
  Feature: {},
}));

describe('FeatureFlagProvider', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    vi.resetModules();
  });

  afterEach(() => {
    vi.clearAllMocks();
    vi.resetModules();
  });

  describe('FeatureFlagProvider component', () => {
    it('should render children', async () => {
      const mockConfig = {
        mode: 'development',
      };

      const { getConfig } = await import('../../src/lib/config');
      (getConfig as unknown as ReturnType<typeof vi.fn>).mockReturnValue(mockConfig);

      const { FeatureFlagProvider } = await import('../../src/providers/feature-flag-provider');

      render(
        <FeatureFlagProvider>
          <div data-testid="child">Child content</div>
        </FeatureFlagProvider>
      );

      expect(screen.getByTestId('child')).toBeInTheDocument();
      expect(screen.getByText('Child content')).toBeInTheDocument();
    });

    it('should initialize feature flags from config', async () => {
      const mockConfig = {
        mode: 'development',
      };

      const { getConfig } = await import('../../src/lib/config');
      (getConfig as unknown as ReturnType<typeof vi.fn>).mockReturnValue(mockConfig);

      const { FeatureFlags } = await import('@study-abroad/shared-feature-flags');
      const { logInfo } = await import('../../src/lib/logger');
      const { FeatureFlagProvider } = await import('../../src/providers/feature-flag-provider');

      render(
        <FeatureFlagProvider>
          <div>Test</div>
        </FeatureFlagProvider>
      );

      await waitFor(() => {
        expect(FeatureFlags).toHaveBeenCalledWith('development');
        expect(logInfo).toHaveBeenCalledWith(
          'Feature flags initialized',
          expect.objectContaining({
            environmentMode: 'development',
          })
        );
      });
    });

    it('should handle config errors gracefully', async () => {
      const consoleErrorSpy = vi.spyOn(console, 'error').mockImplementation(() => {});

      const { getConfig } = await import('../../src/lib/config');
      (getConfig as unknown as ReturnType<typeof vi.fn>).mockImplementation(() => {
        throw new Error('Config error');
      });

      const { FeatureFlagProvider } = await import('../../src/providers/feature-flag-provider');

      render(
        <FeatureFlagProvider>
          <div data-testid="child">Child</div>
        </FeatureFlagProvider>
      );

      await waitFor(() => {
        expect(consoleErrorSpy).toHaveBeenCalledWith(
          '[FeatureFlagProvider] Failed to initialize feature flags:',
          expect.any(Error)
        );
      });

      // Should still render children
      expect(screen.getByTestId('child')).toBeInTheDocument();

      consoleErrorSpy.mockRestore();
    });
  });

  describe('useFeatureFlags hook', () => {
    it('should throw error when used outside provider', async () => {
      const { useFeatureFlags } = await import('../../src/providers/feature-flag-provider');

      // Create a test component that uses the hook
      const TestComponent = () => {
        useFeatureFlags();
        return null;
      };

      // Expect render to throw
      expect(() => {
        render(<TestComponent />);
      }).toThrow('useFeatureFlags must be used within a FeatureFlagProvider');
    });

    it('should return feature flag context when used within provider', async () => {
      const mockConfig = {
        mode: 'development',
      };

      const { getConfig } = await import('../../src/lib/config');
      (getConfig as unknown as ReturnType<typeof vi.fn>).mockReturnValue(mockConfig);

      const { FeatureFlagProvider, useFeatureFlags } = await import('../../src/providers/feature-flag-provider');

      let contextValue: ReturnType<typeof useFeatureFlags> | undefined;

      const TestComponent = () => {
        contextValue = useFeatureFlags();
        return <div>Loaded: {String(!contextValue.isLoading)}</div>;
      };

      render(
        <FeatureFlagProvider>
          <TestComponent />
        </FeatureFlagProvider>
      );

      await waitFor(() => {
        expect(contextValue).toBeDefined();
        expect(contextValue?.flags).toBeDefined();
        expect(contextValue?.environmentMode).toBeDefined();
        expect(contextValue?.isFeatureEnabled).toBeInstanceOf(Function);
      });
    });
  });

  describe('useFeature hook', () => {
    it('should return feature status', async () => {
      const mockConfig = {
        mode: 'development',
      };

      const { getConfig } = await import('../../src/lib/config');
      (getConfig as unknown as ReturnType<typeof vi.fn>).mockReturnValue(mockConfig);

      const { FeatureFlagProvider, useFeature } = await import('../../src/providers/feature-flag-provider');

      let supabaseEnabled: boolean | undefined;

      const TestComponent = () => {
        supabaseEnabled = useFeature('ENABLE_SUPABASE');
        return <div>Supabase: {String(supabaseEnabled)}</div>;
      };

      render(
        <FeatureFlagProvider>
          <TestComponent />
        </FeatureFlagProvider>
      );

      await waitFor(() => {
        expect(supabaseEnabled).toBe(true);
      });
    });
  });

  describe('useEnvironment hook', () => {
    it('should return current environment', async () => {
      const mockConfig = {
        mode: 'production',
      };

      const { getConfig } = await import('../../src/lib/config');
      (getConfig as unknown as ReturnType<typeof vi.fn>).mockReturnValue(mockConfig);

      const { FeatureFlagProvider, useEnvironment } = await import('../../src/providers/feature-flag-provider');

      let environment: string | undefined;

      const TestComponent = () => {
        environment = useEnvironment();
        return <div>Env: {environment}</div>;
      };

      render(
        <FeatureFlagProvider>
          <TestComponent />
        </FeatureFlagProvider>
      );

      await waitFor(() => {
        expect(environment).toBe('production');
      });
    });
  });

  describe('FeatureGate component', () => {
    it('should render children when feature is enabled', async () => {
      const mockConfig = {
        mode: 'development',
      };

      const { getConfig } = await import('../../src/lib/config');
      (getConfig as unknown as ReturnType<typeof vi.fn>).mockReturnValue(mockConfig);

      const { FeatureFlagProvider, FeatureGate } = await import('../../src/providers/feature-flag-provider');

      render(
        <FeatureFlagProvider>
          <FeatureGate feature="ENABLE_SUPABASE">
            <div data-testid="gated-content">Supabase Feature</div>
          </FeatureGate>
        </FeatureFlagProvider>
      );

      await waitFor(() => {
        expect(screen.getByTestId('gated-content')).toBeInTheDocument();
      });
    });

    it('should not render children when feature is disabled', async () => {
      const mockConfig = {
        mode: 'development',
      };

      const { getConfig } = await import('../../src/lib/config');
      (getConfig as unknown as ReturnType<typeof vi.fn>).mockReturnValue(mockConfig);

      const { FeatureFlagProvider, FeatureGate } = await import('../../src/providers/feature-flag-provider');

      render(
        <FeatureFlagProvider>
          <FeatureGate feature="ENABLE_PAYMENTS">
            <div data-testid="gated-content">Payment Feature</div>
          </FeatureGate>
        </FeatureFlagProvider>
      );

      await waitFor(() => {
        expect(screen.queryByTestId('gated-content')).not.toBeInTheDocument();
      });
    });

    it('should render fallback when feature is disabled', async () => {
      const mockConfig = {
        mode: 'development',
      };

      const { getConfig } = await import('../../src/lib/config');
      (getConfig as unknown as ReturnType<typeof vi.fn>).mockReturnValue(mockConfig);

      const { FeatureFlagProvider, FeatureGate } = await import('../../src/providers/feature-flag-provider');

      render(
        <FeatureFlagProvider>
          <FeatureGate
            feature="ENABLE_PAYMENTS"
            fallback={<div data-testid="fallback">Coming Soon</div>}
          >
            <div data-testid="gated-content">Payment Feature</div>
          </FeatureGate>
        </FeatureFlagProvider>
      );

      await waitFor(() => {
        expect(screen.queryByTestId('gated-content')).not.toBeInTheDocument();
        expect(screen.getByTestId('fallback')).toBeInTheDocument();
        expect(screen.getByText('Coming Soon')).toBeInTheDocument();
      });
    });
  });

  describe('EnvironmentGate component', () => {
    it('should render children when in allowed environment', async () => {
      const mockConfig = {
        mode: 'development',
      };

      const { getConfig } = await import('../../src/lib/config');
      (getConfig as unknown as ReturnType<typeof vi.fn>).mockReturnValue(mockConfig);

      const { FeatureFlagProvider, EnvironmentGate } = await import('../../src/providers/feature-flag-provider');

      render(
        <FeatureFlagProvider>
          <EnvironmentGate environments={['development', 'staging']}>
            <div data-testid="env-content">Dev Content</div>
          </EnvironmentGate>
        </FeatureFlagProvider>
      );

      await waitFor(() => {
        expect(screen.getByTestId('env-content')).toBeInTheDocument();
      });
    });

    it('should not render children when not in allowed environment', async () => {
      const mockConfig = {
        mode: 'development',
      };

      const { getConfig } = await import('../../src/lib/config');
      (getConfig as unknown as ReturnType<typeof vi.fn>).mockReturnValue(mockConfig);

      const { FeatureFlagProvider, EnvironmentGate } = await import('../../src/providers/feature-flag-provider');

      render(
        <FeatureFlagProvider>
          <EnvironmentGate environments={['production']}>
            <div data-testid="env-content">Production Only</div>
          </EnvironmentGate>
        </FeatureFlagProvider>
      );

      await waitFor(() => {
        expect(screen.queryByTestId('env-content')).not.toBeInTheDocument();
      });
    });

    it('should render fallback when not in allowed environment', async () => {
      const mockConfig = {
        mode: 'development',
      };

      const { getConfig } = await import('../../src/lib/config');
      (getConfig as unknown as ReturnType<typeof vi.fn>).mockReturnValue(mockConfig);

      const { FeatureFlagProvider, EnvironmentGate } = await import('../../src/providers/feature-flag-provider');

      render(
        <FeatureFlagProvider>
          <EnvironmentGate
            environments={['production']}
            fallback={<div data-testid="fallback">Dev Mode</div>}
          >
            <div data-testid="env-content">Production Only</div>
          </EnvironmentGate>
        </FeatureFlagProvider>
      );

      await waitFor(() => {
        expect(screen.queryByTestId('env-content')).not.toBeInTheDocument();
        expect(screen.getByTestId('fallback')).toBeInTheDocument();
      });
    });
  });
});
