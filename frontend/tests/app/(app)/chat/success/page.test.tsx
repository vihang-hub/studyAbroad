/**
 * Tests for payment success page
 */

import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { render, screen, waitFor, act } from '@testing-library/react';
import React from 'react';

// Mock next/navigation
const mockPush = vi.fn();
const mockSearchParams = new Map<string, string>();

vi.mock('next/navigation', () => ({
  useRouter: () => ({
    push: mockPush,
  }),
  useSearchParams: () => ({
    get: (key: string) => mockSearchParams.get(key) || null,
  }),
}));

// Mock API client
const mockApiGet = vi.fn();
vi.mock('../../../../../src/lib/api-client', () => ({
  api: {
    get: mockApiGet,
  },
}));

describe('PaymentSuccessPage', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    vi.useFakeTimers();
    mockSearchParams.clear();
  });

  afterEach(() => {
    vi.useRealTimers();
  });

  describe('rendering', () => {
    it('should render success heading', async () => {
      mockSearchParams.set('reportId', 'test-123');
      mockApiGet.mockResolvedValue({ data: { status: 'pending' }, error: null });

      const PaymentSuccessPage = (await import('../../../../../src/app/(app)/chat/success/page')).default;
      render(<PaymentSuccessPage />);

      expect(screen.getByRole('heading', { level: 1 })).toHaveTextContent('Payment Successful!');
    });

    it('should render loading message', async () => {
      mockSearchParams.set('reportId', 'test-123');
      mockApiGet.mockResolvedValue({ data: { status: 'pending' }, error: null });

      const PaymentSuccessPage = (await import('../../../../../src/app/(app)/chat/success/page')).default;
      render(<PaymentSuccessPage />);

      expect(screen.getByText('Your report is being generated...')).toBeInTheDocument();
    });

    it('should display initial pending status', async () => {
      mockSearchParams.set('reportId', 'test-123');
      mockApiGet.mockResolvedValue({ data: { status: 'pending' }, error: null });

      const PaymentSuccessPage = (await import('../../../../../src/app/(app)/chat/success/page')).default;
      render(<PaymentSuccessPage />);

      expect(screen.getByText(/Status:/)).toBeInTheDocument();
      expect(screen.getByText('pending')).toBeInTheDocument();
    });

    it('should show wait message', async () => {
      mockSearchParams.set('reportId', 'test-123');
      mockApiGet.mockResolvedValue({ data: { status: 'pending' }, error: null });

      const PaymentSuccessPage = (await import('../../../../../src/app/(app)/chat/success/page')).default;
      render(<PaymentSuccessPage />);

      expect(screen.getByText(/60 seconds/)).toBeInTheDocument();
    });

    it('should render success icon', async () => {
      mockSearchParams.set('reportId', 'test-123');
      mockApiGet.mockResolvedValue({ data: { status: 'pending' }, error: null });

      const PaymentSuccessPage = (await import('../../../../../src/app/(app)/chat/success/page')).default;
      render(<PaymentSuccessPage />);

      const greenIcon = document.querySelector('.bg-green-100');
      expect(greenIcon).toBeInTheDocument();
    });
  });

  describe('redirect without reportId', () => {
    it('should redirect to chat if no reportId', async () => {
      // No reportId set
      const PaymentSuccessPage = (await import('../../../../../src/app/(app)/chat/success/page')).default;
      render(<PaymentSuccessPage />);

      expect(mockPush).toHaveBeenCalledWith('/chat');
    });
  });

  describe('polling behavior', () => {
    it('should poll for report status', async () => {
      mockSearchParams.set('reportId', 'test-report-123');
      mockApiGet.mockResolvedValue({ data: { status: 'processing' }, error: null });

      const PaymentSuccessPage = (await import('../../../../../src/app/(app)/chat/success/page')).default;
      render(<PaymentSuccessPage />);

      // Advance timer to trigger poll
      await act(async () => {
        vi.advanceTimersByTime(2100);
        await Promise.resolve();
      });

      expect(mockApiGet).toHaveBeenCalledWith('/reports/test-report-123');
    });

    it('should redirect to report when completed', async () => {
      mockSearchParams.set('reportId', 'completed-report');
      mockApiGet.mockResolvedValue({ data: { status: 'completed' }, error: null });

      const PaymentSuccessPage = (await import('../../../../../src/app/(app)/chat/success/page')).default;
      render(<PaymentSuccessPage />);

      await act(async () => {
        vi.advanceTimersByTime(2100);
        await Promise.resolve();
      });

      // Wait for state update and redirect
      await act(async () => {
        await Promise.resolve();
      });

      expect(mockPush).toHaveBeenCalledWith('/report/completed-report');
    });

    it('should update status to processing', async () => {
      mockSearchParams.set('reportId', 'processing-report');
      mockApiGet.mockResolvedValue({ data: { status: 'processing' }, error: null });

      const PaymentSuccessPage = (await import('../../../../../src/app/(app)/chat/success/page')).default;
      render(<PaymentSuccessPage />);

      await act(async () => {
        vi.advanceTimersByTime(2100);
        await Promise.resolve();
      });

      // The component will update state after API returns
      await act(async () => {
        await Promise.resolve();
      });

      expect(screen.getByText('processing')).toBeInTheDocument();
    });
  });

  describe('error handling', () => {
    it('should display error when API returns error', async () => {
      mockSearchParams.set('reportId', 'error-report');
      mockApiGet.mockResolvedValue({ data: null, error: { message: 'API Error' } });

      const PaymentSuccessPage = (await import('../../../../../src/app/(app)/chat/success/page')).default;
      render(<PaymentSuccessPage />);

      await act(async () => {
        vi.advanceTimersByTime(2100);
        await Promise.resolve();
      });

      await act(async () => {
        await Promise.resolve();
      });

      expect(screen.getByText('API Error')).toBeInTheDocument();
    });

    it('should display error when report generation fails', async () => {
      mockSearchParams.set('reportId', 'failed-report');
      mockApiGet.mockResolvedValue({ data: { status: 'failed' }, error: null });

      const PaymentSuccessPage = (await import('../../../../../src/app/(app)/chat/success/page')).default;
      render(<PaymentSuccessPage />);

      await act(async () => {
        vi.advanceTimersByTime(2100);
        await Promise.resolve();
      });

      await act(async () => {
        await Promise.resolve();
      });

      expect(screen.getByText('Report generation failed')).toBeInTheDocument();
    });

    it('should show return to chat button on error', async () => {
      mockSearchParams.set('reportId', 'error-report');
      mockApiGet.mockResolvedValue({ data: null, error: { message: 'Error' } });

      const PaymentSuccessPage = (await import('../../../../../src/app/(app)/chat/success/page')).default;
      render(<PaymentSuccessPage />);

      await act(async () => {
        vi.advanceTimersByTime(2100);
        await Promise.resolve();
      });

      await act(async () => {
        await Promise.resolve();
      });

      expect(screen.getByText('Return to chat')).toBeInTheDocument();
    });

    it('should have error styling', async () => {
      mockSearchParams.set('reportId', 'error-report');
      mockApiGet.mockResolvedValue({ data: null, error: { message: 'Error' } });

      const PaymentSuccessPage = (await import('../../../../../src/app/(app)/chat/success/page')).default;
      render(<PaymentSuccessPage />);

      await act(async () => {
        vi.advanceTimersByTime(2100);
        await Promise.resolve();
      });

      await act(async () => {
        await Promise.resolve();
      });

      const errorDiv = screen.getByText('Error').closest('div');
      expect(errorDiv).toHaveClass('bg-red-50', 'border-red-200');
    });
  });

  describe('styling', () => {
    it('should have centered layout', async () => {
      mockSearchParams.set('reportId', 'test-123');
      mockApiGet.mockResolvedValue({ data: { status: 'pending' }, error: null });

      const PaymentSuccessPage = (await import('../../../../../src/app/(app)/chat/success/page')).default;
      const { container } = render(<PaymentSuccessPage />);

      const mainDiv = container.firstChild;
      expect(mainDiv).toHaveClass('max-w-2xl', 'mx-auto', 'text-center');
    });
  });
});
