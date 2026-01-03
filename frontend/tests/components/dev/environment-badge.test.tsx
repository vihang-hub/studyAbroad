/**
 * Tests for EnvironmentBadge component
 */

import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import React from 'react';

// Mock the feature flag provider
vi.mock('../../../src/providers/feature-flag-provider', () => ({
  useFeatureFlags: vi.fn(),
}));

describe('EnvironmentBadge', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    vi.resetModules();
  });

  afterEach(() => {
    vi.clearAllMocks();
  });

  describe('visibility', () => {
    it('should return null in production environment', async () => {
      const { useFeatureFlags } = await import('../../../src/providers/feature-flag-provider');
      (useFeatureFlags as unknown as ReturnType<typeof vi.fn>).mockReturnValue({
        flags: { ENABLE_SUPABASE: true, ENABLE_PAYMENTS: true },
        environmentMode: 'production',
        isLoading: false,
      });

      const { EnvironmentBadge } = await import('../../../src/components/dev/environment-badge');
      const { container } = render(<EnvironmentBadge />);

      expect(container.firstChild).toBeNull();
    });

    it('should return null while loading', async () => {
      const { useFeatureFlags } = await import('../../../src/providers/feature-flag-provider');
      (useFeatureFlags as unknown as ReturnType<typeof vi.fn>).mockReturnValue({
        flags: {},
        environmentMode: 'development',
        isLoading: true,
      });

      const { EnvironmentBadge } = await import('../../../src/components/dev/environment-badge');
      const { container } = render(<EnvironmentBadge />);

      expect(container.firstChild).toBeNull();
    });

    it('should render in development environment', async () => {
      const { useFeatureFlags } = await import('../../../src/providers/feature-flag-provider');
      (useFeatureFlags as unknown as ReturnType<typeof vi.fn>).mockReturnValue({
        flags: { ENABLE_SUPABASE: true, ENABLE_PAYMENTS: false },
        environmentMode: 'development',
        isLoading: false,
      });

      const { EnvironmentBadge } = await import('../../../src/components/dev/environment-badge');
      render(<EnvironmentBadge />);

      expect(screen.getByText('DEVELOPMENT')).toBeInTheDocument();
    });

    it('should render in test environment', async () => {
      const { useFeatureFlags } = await import('../../../src/providers/feature-flag-provider');
      (useFeatureFlags as unknown as ReturnType<typeof vi.fn>).mockReturnValue({
        flags: { ENABLE_SUPABASE: true, ENABLE_PAYMENTS: true },
        environmentMode: 'test',
        isLoading: false,
      });

      const { EnvironmentBadge } = await import('../../../src/components/dev/environment-badge');
      render(<EnvironmentBadge />);

      expect(screen.getByText('TEST')).toBeInTheDocument();
    });
  });

  describe('collapsed state', () => {
    it('should show collapsed badge by default', async () => {
      const { useFeatureFlags } = await import('../../../src/providers/feature-flag-provider');
      (useFeatureFlags as unknown as ReturnType<typeof vi.fn>).mockReturnValue({
        flags: { ENABLE_SUPABASE: true },
        environmentMode: 'development',
        isLoading: false,
      });

      const { EnvironmentBadge } = await import('../../../src/components/dev/environment-badge');
      render(<EnvironmentBadge />);

      const button = screen.getByRole('button', { name: /expand environment info/i });
      expect(button).toBeInTheDocument();
    });

    it('should have green color for development', async () => {
      const { useFeatureFlags } = await import('../../../src/providers/feature-flag-provider');
      (useFeatureFlags as unknown as ReturnType<typeof vi.fn>).mockReturnValue({
        flags: {},
        environmentMode: 'development',
        isLoading: false,
      });

      const { EnvironmentBadge } = await import('../../../src/components/dev/environment-badge');
      render(<EnvironmentBadge />);

      const button = screen.getByRole('button', { name: /expand environment info/i });
      expect(button).toHaveClass('bg-green-600');
    });

    it('should have yellow color for test', async () => {
      const { useFeatureFlags } = await import('../../../src/providers/feature-flag-provider');
      (useFeatureFlags as unknown as ReturnType<typeof vi.fn>).mockReturnValue({
        flags: {},
        environmentMode: 'test',
        isLoading: false,
      });

      const { EnvironmentBadge } = await import('../../../src/components/dev/environment-badge');
      render(<EnvironmentBadge />);

      const button = screen.getByRole('button', { name: /expand environment info/i });
      expect(button).toHaveClass('bg-yellow-600');
    });
  });

  describe('expand/collapse interaction', () => {
    it('should expand when clicked', async () => {
      const { useFeatureFlags } = await import('../../../src/providers/feature-flag-provider');
      (useFeatureFlags as unknown as ReturnType<typeof vi.fn>).mockReturnValue({
        flags: { ENABLE_SUPABASE: true, ENABLE_PAYMENTS: false },
        environmentMode: 'development',
        isLoading: false,
      });

      const { EnvironmentBadge } = await import('../../../src/components/dev/environment-badge');
      render(<EnvironmentBadge />);

      const expandButton = screen.getByRole('button', { name: /expand environment info/i });
      fireEvent.click(expandButton);

      expect(screen.getByText('Feature Flags')).toBeInTheDocument();
    });

    it('should collapse when close button clicked', async () => {
      const { useFeatureFlags } = await import('../../../src/providers/feature-flag-provider');
      (useFeatureFlags as unknown as ReturnType<typeof vi.fn>).mockReturnValue({
        flags: { ENABLE_SUPABASE: true },
        environmentMode: 'development',
        isLoading: false,
      });

      const { EnvironmentBadge } = await import('../../../src/components/dev/environment-badge');
      render(<EnvironmentBadge />);

      // Expand
      const expandButton = screen.getByRole('button', { name: /expand environment info/i });
      fireEvent.click(expandButton);

      // Collapse
      const collapseButton = screen.getByRole('button', { name: /collapse environment info/i });
      fireEvent.click(collapseButton);

      expect(screen.getByRole('button', { name: /expand environment info/i })).toBeInTheDocument();
    });
  });

  describe('expanded panel content', () => {
    beforeEach(async () => {
      const { useFeatureFlags } = await import('../../../src/providers/feature-flag-provider');
      (useFeatureFlags as unknown as ReturnType<typeof vi.fn>).mockReturnValue({
        flags: { ENABLE_SUPABASE: true, ENABLE_PAYMENTS: false, ENABLE_RAG: true },
        environmentMode: 'development',
        isLoading: false,
      });
    });

    it('should display feature flags section', async () => {
      const { EnvironmentBadge } = await import('../../../src/components/dev/environment-badge');
      render(<EnvironmentBadge />);

      fireEvent.click(screen.getByRole('button', { name: /expand environment info/i }));

      expect(screen.getByText('Feature Flags')).toBeInTheDocument();
    });

    it('should display feature flag status as ON/OFF', async () => {
      const { EnvironmentBadge } = await import('../../../src/components/dev/environment-badge');
      render(<EnvironmentBadge />);

      fireEvent.click(screen.getByRole('button', { name: /expand environment info/i }));

      expect(screen.getAllByText('ON').length).toBeGreaterThan(0);
      expect(screen.getAllByText('OFF').length).toBeGreaterThan(0);
    });

    it('should display database status', async () => {
      const { EnvironmentBadge } = await import('../../../src/components/dev/environment-badge');
      render(<EnvironmentBadge />);

      fireEvent.click(screen.getByRole('button', { name: /expand environment info/i }));

      expect(screen.getByText('Database:')).toBeInTheDocument();
      expect(screen.getByText('Supabase')).toBeInTheDocument();
    });

    it('should display payments status', async () => {
      const { EnvironmentBadge } = await import('../../../src/components/dev/environment-badge');
      render(<EnvironmentBadge />);

      fireEvent.click(screen.getByRole('button', { name: /expand environment info/i }));

      expect(screen.getByText('Payments:')).toBeInTheDocument();
      expect(screen.getByText('Bypassed')).toBeInTheDocument();
    });
  });

  describe('environment-specific messages', () => {
    it('should show Dev Mode message in development', async () => {
      const { useFeatureFlags } = await import('../../../src/providers/feature-flag-provider');
      (useFeatureFlags as unknown as ReturnType<typeof vi.fn>).mockReturnValue({
        flags: { ENABLE_SUPABASE: true },
        environmentMode: 'development',
        isLoading: false,
      });

      const { EnvironmentBadge } = await import('../../../src/components/dev/environment-badge');
      render(<EnvironmentBadge />);

      fireEvent.click(screen.getByRole('button', { name: /expand environment info/i }));

      expect(screen.getByText('Dev Mode:')).toBeInTheDocument();
      expect(screen.getByText(/All features are mocked/)).toBeInTheDocument();
    });

    it('should show Test Mode message in test environment', async () => {
      const { useFeatureFlags } = await import('../../../src/providers/feature-flag-provider');
      (useFeatureFlags as unknown as ReturnType<typeof vi.fn>).mockReturnValue({
        flags: { ENABLE_SUPABASE: true },
        environmentMode: 'test',
        isLoading: false,
      });

      const { EnvironmentBadge } = await import('../../../src/components/dev/environment-badge');
      render(<EnvironmentBadge />);

      fireEvent.click(screen.getByRole('button', { name: /expand environment info/i }));

      expect(screen.getByText('Test Mode:')).toBeInTheDocument();
      expect(screen.getByText(/Using test database/)).toBeInTheDocument();
    });
  });

  describe('feature flag display variations', () => {
    it('should show Mock when ENABLE_SUPABASE is false', async () => {
      const { useFeatureFlags } = await import('../../../src/providers/feature-flag-provider');
      (useFeatureFlags as unknown as ReturnType<typeof vi.fn>).mockReturnValue({
        flags: { ENABLE_SUPABASE: false, ENABLE_PAYMENTS: false },
        environmentMode: 'development',
        isLoading: false,
      });

      const { EnvironmentBadge } = await import('../../../src/components/dev/environment-badge');
      render(<EnvironmentBadge />);

      fireEvent.click(screen.getByRole('button', { name: /expand environment info/i }));

      expect(screen.getByText('Mock')).toBeInTheDocument();
    });

    it('should show Stripe when ENABLE_PAYMENTS is true', async () => {
      const { useFeatureFlags } = await import('../../../src/providers/feature-flag-provider');
      (useFeatureFlags as unknown as ReturnType<typeof vi.fn>).mockReturnValue({
        flags: { ENABLE_SUPABASE: true, ENABLE_PAYMENTS: true },
        environmentMode: 'test',
        isLoading: false,
      });

      const { EnvironmentBadge } = await import('../../../src/components/dev/environment-badge');
      render(<EnvironmentBadge />);

      fireEvent.click(screen.getByRole('button', { name: /expand environment info/i }));

      expect(screen.getByText('Stripe')).toBeInTheDocument();
    });
  });

  describe('positioning', () => {
    it('should be fixed positioned at bottom-right', async () => {
      const { useFeatureFlags } = await import('../../../src/providers/feature-flag-provider');
      (useFeatureFlags as unknown as ReturnType<typeof vi.fn>).mockReturnValue({
        flags: {},
        environmentMode: 'development',
        isLoading: false,
      });

      const { EnvironmentBadge } = await import('../../../src/components/dev/environment-badge');
      render(<EnvironmentBadge />);

      const container = document.querySelector('.fixed.bottom-4.right-4');
      expect(container).toBeInTheDocument();
    });

    it('should have high z-index', async () => {
      const { useFeatureFlags } = await import('../../../src/providers/feature-flag-provider');
      (useFeatureFlags as unknown as ReturnType<typeof vi.fn>).mockReturnValue({
        flags: {},
        environmentMode: 'development',
        isLoading: false,
      });

      const { EnvironmentBadge } = await import('../../../src/components/dev/environment-badge');
      render(<EnvironmentBadge />);

      const container = document.querySelector('.z-50');
      expect(container).toBeInTheDocument();
    });
  });
});
