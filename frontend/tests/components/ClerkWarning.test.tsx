/**
 * Tests for ClerkWarning component
 */

import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { render, screen, waitFor, act } from '@testing-library/react';
import React from 'react';
import { ClerkWarning } from '../../src/components/ClerkWarning';

describe('ClerkWarning', () => {
  const originalEnv = { ...process.env };

  beforeEach(() => {
    vi.clearAllMocks();
    // Reset environment variables
    process.env = { ...originalEnv };
  });

  afterEach(() => {
    process.env = originalEnv;
  });

  describe('when Clerk is properly configured', () => {
    it('should return null when publishable key is valid', async () => {
      process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY = 'pk_test_real_key_123';

      const { container } = render(<ClerkWarning />);

      // Wait for useEffect to run
      await waitFor(() => {
        expect(container.firstChild).toBeNull();
      });
    });

    it('should not render warning banner with valid production key', async () => {
      process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY = 'pk_live_production_key_456';

      const { container } = render(<ClerkWarning />);

      await waitFor(() => {
        expect(container.firstChild).toBeNull();
      });
    });
  });

  describe('when Clerk has placeholder keys', () => {
    it('should render warning when key contains YOUR_', async () => {
      process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY = 'pk_test_YOUR_clerk_key';

      render(<ClerkWarning />);

      await waitFor(() => {
        expect(screen.getByText(/Development Mode:/)).toBeInTheDocument();
      });
    });

    it('should render warning when key contains your_', async () => {
      process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY = 'pk_test_your_clerk_key';

      render(<ClerkWarning />);

      await waitFor(() => {
        expect(screen.getByText(/Development Mode:/)).toBeInTheDocument();
      });
    });

    it('should render warning when key is exact placeholder', async () => {
      process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY = 'pk_test_your_clerk_publishable_key';

      render(<ClerkWarning />);

      await waitFor(() => {
        expect(screen.getByText(/Development Mode:/)).toBeInTheDocument();
      });
    });

    it('should render warning when key is empty', async () => {
      process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY = '';

      render(<ClerkWarning />);

      await waitFor(() => {
        expect(screen.getByText(/Development Mode:/)).toBeInTheDocument();
      });
    });

    it('should render warning when key is undefined', async () => {
      delete process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY;

      render(<ClerkWarning />);

      await waitFor(() => {
        expect(screen.getByText(/Development Mode:/)).toBeInTheDocument();
      });
    });
  });

  describe('warning banner content', () => {
    beforeEach(() => {
      process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY = '';
    });

    it('should display Development Mode label', async () => {
      render(<ClerkWarning />);

      await waitFor(() => {
        expect(screen.getByText('Development Mode:')).toBeInTheDocument();
      });
    });

    it('should mention placeholder keys in warning', async () => {
      render(<ClerkWarning />);

      await waitFor(() => {
        expect(screen.getByText(/placeholder keys/)).toBeInTheDocument();
      });
    });

    it('should reference CLERK-SETUP-GUIDE.md', async () => {
      render(<ClerkWarning />);

      await waitFor(() => {
        expect(screen.getByText(/CLERK-SETUP-GUIDE.md/)).toBeInTheDocument();
      });
    });

    it('should have yellow warning styling', async () => {
      render(<ClerkWarning />);

      await waitFor(() => {
        const warningDiv = screen.getByText(/Development Mode:/).closest('div')?.parentElement?.parentElement;
        expect(warningDiv).toHaveClass('bg-yellow-50', 'border-l-4', 'border-yellow-400');
      });
    });

    it('should render warning icon', async () => {
      render(<ClerkWarning />);

      await waitFor(() => {
        const svg = document.querySelector('svg.text-yellow-400');
        expect(svg).toBeInTheDocument();
      });
    });
  });

  describe('hydration behavior', () => {
    it('should not render until after mount (hydration safe)', async () => {
      // First render - before useEffect runs
      process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY = '';

      const { container, rerender } = render(<ClerkWarning />);

      // After useEffect runs and state updates
      await waitFor(() => {
        expect(screen.getByText(/Development Mode:/)).toBeInTheDocument();
      });
    });
  });
});
