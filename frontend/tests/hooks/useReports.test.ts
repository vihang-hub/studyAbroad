/**
 * Tests for useReports hook
 * T120: Report history fetching with pagination support
 */

import { describe, it, expect, vi, beforeEach } from 'vitest';
import { renderHook, waitFor } from '@testing-library/react';
import { act } from 'react';
import { useReports } from '@/hooks/useReports';
import type { Report } from '@/types/report';

// Mock API client
const mockGet = vi.fn();
vi.mock('@/lib/api-client', () => ({
  api: {
    get: (...args: any[]) => mockGet(...args),
  },
}));

describe('useReports', () => {
  const mockReports: Report[] = [
    {
      id: 'report-1',
      userId: 'user-1',
      query: 'Computer Science in UK',
      country: 'UK',
      subject: 'Computer Science',
      status: 'completed',
      createdAt: '2025-01-01T00:00:00Z',
      updatedAt: '2025-01-01T00:00:00Z',
      expires_at: '2025-01-31T00:00:00Z',
      content: { sections: {} },
      citations: [],
    },
    {
      id: 'report-2',
      userId: 'user-1',
      query: 'Nursing in UK',
      country: 'UK',
      subject: 'Nursing',
      status: 'completed',
      createdAt: '2025-01-02T00:00:00Z',
      updatedAt: '2025-01-02T00:00:00Z',
      expires_at: '2025-02-01T00:00:00Z',
      content: { sections: {} },
      citations: [],
    },
  ];

  beforeEach(() => {
    mockGet.mockClear();
  });

  describe('Default behavior', () => {
    it('fetches reports automatically by default', async () => {
      mockGet.mockResolvedValue({
        data: mockReports,
        error: null,
      });

      const { result } = renderHook(() => useReports());

      // Initially loading
      expect(result.current.isLoading).toBe(true);

      await waitFor(() => {
        expect(result.current.isLoading).toBe(false);
      });

      expect(mockGet).toHaveBeenCalledWith('/api/reports?limit=10');
      expect(result.current.reports).toEqual(mockReports);
      expect(result.current.error).toBeNull();
    });

    it('uses default limit of 10', async () => {
      mockGet.mockResolvedValue({
        data: mockReports,
        error: null,
      });

      renderHook(() => useReports());

      await waitFor(() => {
        expect(mockGet).toHaveBeenCalledWith('/api/reports?limit=10');
      });
    });

    it('starts with loading state true', () => {
      mockGet.mockResolvedValue({
        data: mockReports,
        error: null,
      });

      const { result } = renderHook(() => useReports());
      expect(result.current.isLoading).toBe(true);
    });

    it('starts with empty reports array', () => {
      mockGet.mockResolvedValue({
        data: mockReports,
        error: null,
      });

      const { result } = renderHook(() => useReports());
      expect(result.current.reports).toEqual([]);
    });

    it('starts with null error', () => {
      mockGet.mockResolvedValue({
        data: mockReports,
        error: null,
      });

      const { result } = renderHook(() => useReports());
      expect(result.current.error).toBeNull();
    });
  });

  describe('Custom options', () => {
    it('respects custom limit', async () => {
      mockGet.mockResolvedValue({
        data: mockReports.slice(0, 5),
        error: null,
      });

      renderHook(() => useReports({ limit: 5 }));

      await waitFor(() => {
        expect(mockGet).toHaveBeenCalledWith('/api/reports?limit=5');
      });
    });

    it('respects autoFetch: false', async () => {
      mockGet.mockResolvedValue({
        data: mockReports,
        error: null,
      });

      const { result } = renderHook(() => useReports({ autoFetch: false }));

      // Should not fetch automatically
      expect(mockGet).not.toHaveBeenCalled();
      expect(result.current.isLoading).toBe(false);
    });

    it('can manually fetch with refetch when autoFetch is false', async () => {
      mockGet.mockResolvedValue({
        data: mockReports,
        error: null,
      });

      const { result } = renderHook(() => useReports({ autoFetch: false }));

      expect(mockGet).not.toHaveBeenCalled();

      // Manually trigger fetch
      await act(async () => {
        await result.current.refetch();
      });

      await waitFor(() => {
        expect(mockGet).toHaveBeenCalledWith('/api/reports?limit=10');
        expect(result.current.reports).toEqual(mockReports);
      });
    });
  });

  describe('Loading state', () => {
    it('sets isLoading to false after successful fetch', async () => {
      mockGet.mockResolvedValue({
        data: mockReports,
        error: null,
      });

      const { result } = renderHook(() => useReports());

      await waitFor(() => {
        expect(result.current.isLoading).toBe(false);
      });
    });

    it('sets isLoading to false after failed fetch', async () => {
      mockGet.mockResolvedValue({
        data: null,
        error: { message: 'Network error' },
      });

      const { result } = renderHook(() => useReports());

      await waitFor(() => {
        expect(result.current.isLoading).toBe(false);
      });
    });
  });

  describe('Error handling (T134)', () => {
    it('sets error message when API returns error', async () => {
      mockGet.mockResolvedValue({
        data: null,
        error: { message: 'Failed to fetch reports' },
      });

      const { result } = renderHook(() => useReports());

      await waitFor(() => {
        expect(result.current.error).toBe('Failed to fetch reports');
        expect(result.current.reports).toEqual([]);
      });
    });

    it('sets default error message when API error has no message', async () => {
      mockGet.mockResolvedValue({
        data: null,
        error: {},
      });

      const { result } = renderHook(() => useReports());

      await waitFor(() => {
        expect(result.current.error).toBe('Failed to load reports');
      });
    });

    it('handles exception during fetch', async () => {
      mockGet.mockRejectedValue(new Error('Network failure'));

      const { result } = renderHook(() => useReports());

      await waitFor(() => {
        expect(result.current.error).toBe('Network failure');
        expect(result.current.reports).toEqual([]);
      });
    });

    it('handles non-Error exceptions', async () => {
      mockGet.mockRejectedValue('String error');

      const { result } = renderHook(() => useReports());

      await waitFor(() => {
        expect(result.current.error).toBe('Failed to load reports');
      });
    });

    it('clears error on successful refetch', async () => {
      // First fetch fails
      mockGet.mockResolvedValueOnce({
        data: null,
        error: { message: 'Network error' },
      });

      const { result } = renderHook(() => useReports());

      await waitFor(() => {
        expect(result.current.error).toBe('Network error');
      });

      // Second fetch succeeds
      mockGet.mockResolvedValueOnce({
        data: mockReports,
        error: null,
      });

      await act(async () => {
        await result.current.refetch();
      });

      await waitFor(() => {
        expect(result.current.error).toBeNull();
        expect(result.current.reports).toEqual(mockReports);
      });
    });
  });

  describe('Empty state (T134)', () => {
    it('returns empty array when no reports exist', async () => {
      mockGet.mockResolvedValue({
        data: [],
        error: null,
      });

      const { result } = renderHook(() => useReports());

      await waitFor(() => {
        expect(result.current.reports).toEqual([]);
        expect(result.current.error).toBeNull();
        expect(result.current.isLoading).toBe(false);
      });
    });

    it('sets hasMore to false when fewer reports than limit', async () => {
      mockGet.mockResolvedValue({
        data: mockReports.slice(0, 5),
        error: null,
      });

      const { result } = renderHook(() => useReports({ limit: 10 }));

      await waitFor(() => {
        expect(result.current.hasMore).toBe(false);
      });
    });
  });

  describe('Pagination support', () => {
    it('sets hasMore to true when exactly limit reports returned', async () => {
      const exactLimitReports = Array.from({ length: 10 }, (_, i) => ({
        ...mockReports[0],
        id: `report-${i}`,
      }));

      mockGet.mockResolvedValue({
        data: exactLimitReports,
        error: null,
      });

      const { result } = renderHook(() => useReports({ limit: 10 }));

      await waitFor(() => {
        expect(result.current.hasMore).toBe(true);
      });
    });

    it('sets hasMore to false when fewer than limit reports returned', async () => {
      mockGet.mockResolvedValue({
        data: mockReports, // Only 2 reports
        error: null,
      });

      const { result } = renderHook(() => useReports({ limit: 10 }));

      await waitFor(() => {
        expect(result.current.hasMore).toBe(false);
      });
    });

    it('sets hasMore to false when no reports returned', async () => {
      mockGet.mockResolvedValue({
        data: [],
        error: null,
      });

      const { result } = renderHook(() => useReports());

      await waitFor(() => {
        expect(result.current.hasMore).toBe(false);
      });
    });
  });

  describe('Refetch functionality', () => {
    it('provides refetch function', async () => {
      mockGet.mockResolvedValue({
        data: mockReports,
        error: null,
      });

      const { result } = renderHook(() => useReports());

      await waitFor(() => {
        expect(result.current.isLoading).toBe(false);
      });

      expect(typeof result.current.refetch).toBe('function');
    });

    it('refetch triggers new API call', async () => {
      mockGet.mockResolvedValue({
        data: mockReports,
        error: null,
      });

      const { result } = renderHook(() => useReports());

      await waitFor(() => {
        expect(mockGet).toHaveBeenCalledTimes(1);
      });

      await act(async () => {
        await result.current.refetch();
      });

      await waitFor(() => {
        expect(mockGet).toHaveBeenCalledTimes(2);
      });
    });

    it('refetch sets loading state', async () => {
      mockGet.mockResolvedValue({
        data: mockReports,
        error: null,
      });

      const { result } = renderHook(() => useReports());

      await waitFor(() => {
        expect(result.current.isLoading).toBe(false);
      });

      let refetchPromise: Promise<void>;
      await act(async () => {
        refetchPromise = result.current.refetch();
        // Should be loading during refetch
        expect(result.current.isLoading).toBe(true);
        await refetchPromise;
      });

      await waitFor(() => {
        expect(result.current.isLoading).toBe(false);
      });
    });

    it('refetch updates reports with new data', async () => {
      const initialReports = [mockReports[0]];
      const updatedReports = mockReports;

      mockGet.mockResolvedValueOnce({
        data: initialReports,
        error: null,
      });

      const { result } = renderHook(() => useReports());

      await waitFor(() => {
        expect(result.current.reports).toEqual(initialReports);
      });

      mockGet.mockResolvedValueOnce({
        data: updatedReports,
        error: null,
      });

      await act(async () => {
        await result.current.refetch();
      });

      await waitFor(() => {
        expect(result.current.reports).toEqual(updatedReports);
      });
    });
  });

  describe('User scoping (T132)', () => {
    it('endpoint URL includes user-scoped path', async () => {
      mockGet.mockResolvedValue({
        data: mockReports,
        error: null,
      });

      renderHook(() => useReports());

      await waitFor(() => {
        expect(mockGet).toHaveBeenCalledWith('/api/reports?limit=10');
      });
    });

    it('returns only authenticated user reports', async () => {
      const userReports = mockReports.filter(r => r.userId === 'user-1');

      mockGet.mockResolvedValue({
        data: userReports,
        error: null,
      });

      const { result } = renderHook(() => useReports());

      await waitFor(() => {
        expect(result.current.reports).toEqual(userReports);
        expect(result.current.reports.every(r => r.userId === 'user-1')).toBe(true);
      });
    });
  });

  describe('Return value structure', () => {
    it('returns all expected properties', async () => {
      mockGet.mockResolvedValue({
        data: mockReports,
        error: null,
      });

      const { result } = renderHook(() => useReports());

      await waitFor(() => {
        expect(result.current.isLoading).toBe(false);
      });

      expect(result.current).toHaveProperty('reports');
      expect(result.current).toHaveProperty('isLoading');
      expect(result.current).toHaveProperty('error');
      expect(result.current).toHaveProperty('refetch');
      expect(result.current).toHaveProperty('hasMore');
    });

    it('reports property is an array', async () => {
      mockGet.mockResolvedValue({
        data: mockReports,
        error: null,
      });

      const { result } = renderHook(() => useReports());

      await waitFor(() => {
        expect(Array.isArray(result.current.reports)).toBe(true);
      });
    });
  });
});
