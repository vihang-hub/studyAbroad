/**
 * Tests for usePayment hook
 * Coverage target: 100% (high-impact hook: ~4-5% total frontend coverage)
 */

import { describe, it, expect, vi, beforeEach } from 'vitest';
import { renderHook, act, waitFor } from '@testing-library/react';
import { usePayment } from '../../src/hooks/usePayment';
import * as apiClient from '../../src/lib/api-client';
import * as logger from '../../src/lib/logger';

// Mock Clerk's useAuth
const mockGetToken = vi.fn().mockResolvedValue('mock-auth-token');
vi.mock('@clerk/nextjs', () => ({
  useAuth: () => ({
    getToken: mockGetToken,
    isSignedIn: true,
    isLoaded: true,
  }),
}));

// Mock feature flags module
vi.mock('@study-abroad/shared-feature-flags', () => ({
  Feature: {
    PAYMENTS: 'payments',
    SUPABASE: 'supabase',
    AI_STREAMING: 'ai_streaming',
  },
}));

// Mock dependencies
vi.mock('../../src/providers/feature-flag-provider', () => ({
  useFeature: vi.fn(),
}));

vi.mock('../../src/lib/api-client', () => ({
  api: {
    post: vi.fn(),
    get: vi.fn(),
    put: vi.fn(),
    patch: vi.fn(),
    delete: vi.fn(),
  },
}));

vi.mock('../../src/lib/logger', () => ({
  logInfo: vi.fn(),
  logError: vi.fn(),
}));

// Import after mocking
import { useFeature } from '../../src/providers/feature-flag-provider';

describe('usePayment', () => {
  const mockApiPost = vi.mocked(apiClient.api.post);
  const mockUseFeature = vi.mocked(useFeature);
  const mockLogInfo = vi.mocked(logger.logInfo);
  const mockLogError = vi.mocked(logger.logError);

  const defaultOptions = {
    apiEndpoint: '/reports/initiate',
    onSuccess: vi.fn(),
    onError: vi.fn(),
  };

  beforeEach(() => {
    vi.clearAllMocks();
    // Reset window.location
    delete (window as { location?: unknown }).location;
    (window as { location?: { href?: string } }).location = { href: '' };
  });

  describe('Initial state', () => {
    it('should return initial state with isLoading false and error null', () => {
      mockUseFeature.mockReturnValue(false);

      const { result } = renderHook(() => usePayment(defaultOptions));

      expect(result.current.isLoading).toBe(false);
      expect(result.current.error).toBeNull();
      expect(typeof result.current.createCheckout).toBe('function');
    });
  });

  describe('Dev/Test mode (payments disabled)', () => {
    beforeEach(() => {
      mockUseFeature.mockReturnValue(false);
    });

    it('should bypass payment and create report directly', async () => {
      const reportId = 'report-123';
      mockApiPost.mockResolvedValueOnce({
        status: 200,
        data: { reportId },
      });

      const { result } = renderHook(() => usePayment(defaultOptions));

      await act(async () => {
        await result.current.createCheckout('UK study visa requirements');
      });

      expect(mockLogInfo).toHaveBeenCalledWith(
        'Payment bypassed in dev/test mode',
        expect.objectContaining({ query: 'UK study visa requirements' }),
      );

      expect(mockApiPost).toHaveBeenCalledWith(
        '/reports/initiate',
        { query: 'UK study visa requirements' },
        expect.objectContaining({ authToken: 'mock-auth-token' }),
      );

      expect(defaultOptions.onSuccess).toHaveBeenCalledWith(reportId);
    });

    it('should handle report creation success with id field instead of reportId', async () => {
      const reportId = 'report-456';
      mockApiPost.mockResolvedValueOnce({
        status: 200,
        data: { id: reportId }, // Different field name
      });

      const { result } = renderHook(() => usePayment(defaultOptions));

      await act(async () => {
        await result.current.createCheckout('UK study costs');
      });

      expect(defaultOptions.onSuccess).toHaveBeenCalledWith(reportId);
    });

    it('should set isLoading to true during request', async () => {
      mockApiPost.mockImplementationOnce(
        () =>
          new Promise((resolve) =>
            setTimeout(
              () =>
                resolve({
                  status: 200,
                  data: { reportId: 'report-789' },
                }),
              100,
            ),
          ),
      );

      const { result } = renderHook(() => usePayment(defaultOptions));

      act(() => {
        result.current.createCheckout('UK work visa');
      });

      expect(result.current.isLoading).toBe(true);

      await waitFor(() => {
        expect(result.current.isLoading).toBe(false);
      });
    });

    it('should handle API error response', async () => {
      mockApiPost.mockResolvedValueOnce({
        status: 400,
        error: {
          message: 'Invalid query',
          code: 'INVALID_QUERY',
        },
      });

      const { result } = renderHook(() => usePayment(defaultOptions));

      await act(async () => {
        await result.current.createCheckout('');
      });

      expect(result.current.error).toBe('Invalid query');
      expect(defaultOptions.onError).toHaveBeenCalledWith('Invalid query');
      expect(mockLogError).toHaveBeenCalled();
    });

    it('should handle missing report ID in response', async () => {
      mockApiPost.mockResolvedValueOnce({
        status: 200,
        data: {}, // No reportId or id
      });

      const { result } = renderHook(() => usePayment(defaultOptions));

      await act(async () => {
        await result.current.createCheckout('UK study');
      });

      expect(result.current.error).toBe('No report ID returned');
      expect(defaultOptions.onError).toHaveBeenCalledWith('No report ID returned');
    });

    it('should handle network errors', async () => {
      mockApiPost.mockRejectedValueOnce(new Error('Network error'));

      const { result } = renderHook(() => usePayment(defaultOptions));

      await act(async () => {
        await result.current.createCheckout('UK study');
      });

      expect(result.current.error).toBe('Network error');
      expect(defaultOptions.onError).toHaveBeenCalledWith('Network error');
      expect(mockLogError).toHaveBeenCalledWith('Payment error', expect.any(Error));
    });

    it('should handle non-Error exceptions', async () => {
      mockApiPost.mockRejectedValueOnce('String error');

      const { result } = renderHook(() => usePayment(defaultOptions));

      await act(async () => {
        await result.current.createCheckout('UK study');
      });

      expect(result.current.error).toBe('Payment failed');
      expect(defaultOptions.onError).toHaveBeenCalledWith('Payment failed');
    });

    it('should clear previous error on new request', async () => {
      mockApiPost
        .mockResolvedValueOnce({
          status: 400,
          error: { message: 'First error' },
        })
        .mockResolvedValueOnce({
          status: 200,
          data: { reportId: 'report-success' },
        });

      const { result } = renderHook(() => usePayment(defaultOptions));

      // First request with error
      await act(async () => {
        await result.current.createCheckout('Bad query');
      });

      expect(result.current.error).toBe('First error');

      // Second successful request should clear error
      await act(async () => {
        await result.current.createCheckout('Good query');
      });

      expect(result.current.error).toBeNull();
    });
  });

  describe('Production mode (payments enabled)', () => {
    beforeEach(() => {
      mockUseFeature.mockReturnValue(true);
    });

    it('should create Stripe checkout and redirect', async () => {
      const checkoutUrl = 'https://checkout.stripe.com/session-123';
      mockApiPost.mockResolvedValueOnce({
        status: 200,
        data: { checkoutUrl },
      });

      const { result } = renderHook(() => usePayment(defaultOptions));

      await act(async () => {
        await result.current.createCheckout('UK study visa');
      });

      expect(mockLogInfo).toHaveBeenCalledWith(
        'Creating Stripe checkout',
        expect.objectContaining({ query: 'UK study visa' }),
      );

      expect(mockApiPost).toHaveBeenCalledWith(
        '/reports/initiate',
        { query: 'UK study visa' },
        expect.objectContaining({ authToken: 'mock-auth-token' }),
      );

      expect(window.location.href).toBe(checkoutUrl);
    });

    it('should handle missing checkout URL', async () => {
      mockApiPost.mockResolvedValueOnce({
        status: 200,
        data: {}, // No checkoutUrl
      });

      const { result } = renderHook(() => usePayment(defaultOptions));

      await act(async () => {
        await result.current.createCheckout('UK study');
      });

      expect(result.current.error).toBe('No checkout URL returned');
      expect(defaultOptions.onError).toHaveBeenCalledWith('No checkout URL returned');
    });

    it('should handle API error during checkout creation', async () => {
      mockApiPost.mockResolvedValueOnce({
        status: 500,
        error: {
          message: 'Server error',
          code: 'SERVER_ERROR',
        },
      });

      const { result } = renderHook(() => usePayment(defaultOptions));

      await act(async () => {
        await result.current.createCheckout('UK study');
      });

      expect(result.current.error).toBe('Server error');
      expect(window.location.href).toBe(''); // Should not redirect
    });

    it('should handle network errors during checkout creation', async () => {
      mockApiPost.mockRejectedValueOnce(new Error('Connection timeout'));

      const { result } = renderHook(() => usePayment(defaultOptions));

      await act(async () => {
        await result.current.createCheckout('UK study');
      });

      expect(result.current.error).toBe('Connection timeout');
      expect(window.location.href).toBe('');
    });
  });

  describe('Callback options', () => {
    beforeEach(() => {
      mockUseFeature.mockReturnValue(false);
    });

    it('should work without onSuccess callback', async () => {
      const optionsWithoutSuccess = {
        apiEndpoint: '/reports/initiate',
      };

      mockApiPost.mockResolvedValueOnce({
        status: 200,
        data: { reportId: 'report-123' },
      });

      const { result } = renderHook(() => usePayment(optionsWithoutSuccess));

      await act(async () => {
        await result.current.createCheckout('UK study');
      });

      // Should not throw error
      expect(result.current.error).toBeNull();
    });

    it('should work without onError callback', async () => {
      const optionsWithoutError = {
        apiEndpoint: '/reports/initiate',
      };

      mockApiPost.mockResolvedValueOnce({
        status: 400,
        error: { message: 'Bad request' },
      });

      const { result } = renderHook(() => usePayment(optionsWithoutError));

      await act(async () => {
        await result.current.createCheckout('');
      });

      // Should set error without throwing
      expect(result.current.error).toBe('Bad request');
    });

    it('should call callbacks in correct order', async () => {
      const callOrder: string[] = [];

      const options = {
        apiEndpoint: '/reports/initiate',
        onSuccess: vi.fn(() => callOrder.push('onSuccess')),
        onError: vi.fn(() => callOrder.push('onError')),
      };

      mockApiPost.mockResolvedValueOnce({
        status: 200,
        data: { reportId: 'report-123' },
      });

      const { result } = renderHook(() => usePayment(options));

      await act(async () => {
        await result.current.createCheckout('UK study');
      });

      expect(callOrder).toEqual(['onSuccess']);
    });
  });

  describe('Multiple requests', () => {
    beforeEach(() => {
      mockUseFeature.mockReturnValue(false);
    });

    it('should handle multiple sequential requests', async () => {
      mockApiPost
        .mockResolvedValueOnce({
          status: 200,
          data: { reportId: 'report-1' },
        })
        .mockResolvedValueOnce({
          status: 200,
          data: { reportId: 'report-2' },
        });

      const { result } = renderHook(() => usePayment(defaultOptions));

      await act(async () => {
        await result.current.createCheckout('First query');
      });

      expect(defaultOptions.onSuccess).toHaveBeenCalledWith('report-1');

      await act(async () => {
        await result.current.createCheckout('Second query');
      });

      expect(defaultOptions.onSuccess).toHaveBeenCalledWith('report-2');
      expect(defaultOptions.onSuccess).toHaveBeenCalledTimes(2);
    });
  });

  describe('Custom API endpoint', () => {
    beforeEach(() => {
      mockUseFeature.mockReturnValue(false);
    });

    it('should use custom API endpoint', async () => {
      const customOptions = {
        ...defaultOptions,
        apiEndpoint: '/custom/endpoint',
      };

      mockApiPost.mockResolvedValueOnce({
        status: 200,
        data: { reportId: 'report-123' },
      });

      const { result } = renderHook(() => usePayment(customOptions));

      await act(async () => {
        await result.current.createCheckout('UK study');
      });

      expect(mockApiPost).toHaveBeenCalledWith(
        '/custom/endpoint',
        { query: 'UK study' },
        expect.anything(),
      );
    });
  });
});
