/**
 * Tests for usePayment hook
 */
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { renderHook, waitFor, act } from '@testing-library/react';
import { usePayment } from '../../src/hooks/usePayment';
import { api } from '../../src/lib/api-client';

// Mock the API client
vi.mock('../../src/lib/api-client', () => ({
  api: {
    post: vi.fn(),
  },
}));

describe('usePayment hook', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should initialize with default state', () => {
    const { result } = renderHook(() => usePayment());

    expect(result.current.isLoading).toBe(false);
    expect(result.current.error).toBeNull();
    expect(typeof result.current.createCheckout).toBe('function');
    expect(typeof result.current.clearError).toBe('function');
  });

  it('should create checkout successfully', async () => {
    const mockOnSuccess = vi.fn();

    vi.mocked(api.post).mockResolvedValue({
      success: true,
      data: {
        payment_intent_id: 'pi_12345',
        report_id: 'report_12345',
        client_secret: 'secret_12345',
      },
    });

    const { result } = renderHook(() =>
      usePayment({
        onSuccess: mockOnSuccess,
      })
    );

    await act(async () => {
      await result.current.createCheckout('Test query about UK universities');
    });

    await waitFor(() => {
      expect(result.current.isLoading).toBe(false);
      expect(result.current.error).toBeNull();
      expect(mockOnSuccess).toHaveBeenCalledWith('report_12345');
    });
  });

  it('should handle API errors', async () => {
    const mockOnError = vi.fn();

    vi.mocked(api.post).mockResolvedValue({
      success: false,
      error: { message: 'Payment failed' },
    });

    const { result } = renderHook(() =>
      usePayment({
        onError: mockOnError,
      })
    );

    await act(async () => {
      await result.current.createCheckout('Test query');
    });

    await waitFor(() => {
      expect(result.current.isLoading).toBe(false);
      expect(result.current.error).toBe('Payment failed');
      expect(mockOnError).toHaveBeenCalledWith('Payment failed');
    });
  });

  it('should handle network errors', async () => {
    const mockOnError = vi.fn();

    vi.mocked(api.post).mockRejectedValue(new Error('Network error'));

    const { result } = renderHook(() =>
      usePayment({
        onError: mockOnError,
      })
    );

    await act(async () => {
      await result.current.createCheckout('Test query');
    });

    await waitFor(() => {
      expect(result.current.isLoading).toBe(false);
      expect(result.current.error).toBe('Network error');
      expect(mockOnError).toHaveBeenCalledWith('Network error');
    });
  });

  it('should set loading state during checkout', async () => {
    let resolvePromise: any;
    const promise = new Promise((resolve) => {
      resolvePromise = resolve;
    });

    vi.mocked(api.post).mockReturnValue(promise);

    const { result } = renderHook(() => usePayment());

    act(() => {
      result.current.createCheckout('Test query');
    });

    expect(result.current.isLoading).toBe(true);

    act(() => {
      resolvePromise({
        success: true,
        data: { report_id: 'report_123' },
      });
    });

    await waitFor(() => {
      expect(result.current.isLoading).toBe(false);
    });
  });

  it('should clear error', async () => {
    const mockOnError = vi.fn();

    vi.mocked(api.post).mockResolvedValue({
      success: false,
      error: { message: 'Test error' },
    });

    const { result } = renderHook(() =>
      usePayment({
        onError: mockOnError,
      })
    );

    await act(async () => {
      await result.current.createCheckout('Test query');
    });

    await waitFor(() => {
      expect(result.current.error).toBe('Test error');
    });

    act(() => {
      result.current.clearError();
    });

    expect(result.current.error).toBeNull();
  });

  it('should use custom API endpoint', async () => {
    vi.mocked(api.post).mockResolvedValue({
      success: true,
      data: { report_id: 'report_123' },
    });

    const customEndpoint = '/custom/endpoint';

    const { result } = renderHook(() =>
      usePayment({
        apiEndpoint: customEndpoint,
      })
    );

    await act(async () => {
      await result.current.createCheckout('Test query');
    });

    expect(api.post).toHaveBeenCalledWith(
      customEndpoint,
      expect.objectContaining({ query: 'Test query' })
    );
  });

  it('should handle missing report_id in response', async () => {
    const mockOnSuccess = vi.fn();

    vi.mocked(api.post).mockResolvedValue({
      success: true,
      data: {
        payment_intent_id: 'pi_12345',
        // Missing report_id
      },
    });

    const { result } = renderHook(() =>
      usePayment({
        onSuccess: mockOnSuccess,
      })
    );

    await act(async () => {
      await result.current.createCheckout('Test query');
    });

    await waitFor(() => {
      expect(result.current.isLoading).toBe(false);
      expect(mockOnSuccess).not.toHaveBeenCalled();
    });
  });

  it('should call onSuccess with correct report ID', async () => {
    const mockOnSuccess = vi.fn();

    vi.mocked(api.post).mockResolvedValue({
      success: true,
      data: {
        payment_intent_id: 'pi_12345',
        report_id: 'report_abcdef',
        client_secret: 'secret_12345',
      },
    });

    const { result } = renderHook(() =>
      usePayment({
        onSuccess: mockOnSuccess,
      })
    );

    await act(async () => {
      await result.current.createCheckout('UK university query');
    });

    await waitFor(() => {
      expect(mockOnSuccess).toHaveBeenCalledWith('report_abcdef');
    });
  });
});
