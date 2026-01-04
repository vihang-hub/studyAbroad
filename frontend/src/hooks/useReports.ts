/**
 * Custom hook for fetching user's reports
 * T120: Report history fetching with pagination support
 */

'use client';

import { useState, useEffect, useCallback } from 'react';
import { useAuthenticatedApi } from './useAuthenticatedApi';
import type { Report } from '@/types/report';

export interface UseReportsOptions {
  limit?: number;
  autoFetch?: boolean;
}

export interface UseReportsResult {
  reports: Report[];
  isLoading: boolean;
  error: string | null;
  refetch: () => Promise<void>;
  hasMore: boolean;
}

/**
 * Hook to fetch and manage user's report history
 * @param options Configuration options for fetching reports
 * @returns Report data, loading state, and refetch function
 */
export function useReports(options: UseReportsOptions = {}): UseReportsResult {
  const { limit = 10, autoFetch = true } = options;

  const [reports, setReports] = useState<Report[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [hasMore, setHasMore] = useState(false);

  const { get: authGet, isSignedIn, isLoaded } = useAuthenticatedApi();

  const fetchReports = useCallback(async () => {
    // Don't fetch if auth not loaded yet
    if (!isLoaded) {
      return;
    }

    // Don't fetch if not signed in
    if (!isSignedIn) {
      setReports([]);
      setHasMore(false);
      return;
    }

    try {
      setIsLoading(true);
      setError(null);

      const endpoint = `/reports/?limit=${limit}`;
      const response = await authGet<Report[]>(endpoint);

      // Handle 401/403 gracefully - user not authenticated, return empty list
      if (response.status === 401 || response.status === 403) {
        setReports([]);
        setHasMore(false);
        // Don't set error - this is expected for unauthenticated users
        return;
      }

      if (response.error || !response.data) {
        setError(response.error?.message || 'Failed to load reports');
        setReports([]);
        return;
      }

      setReports(response.data);
      // If we received exactly 'limit' reports, there might be more
      setHasMore(response.data.length === limit);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load reports');
      setReports([]);
    } finally {
      setIsLoading(false);
    }
  }, [limit, authGet, isSignedIn, isLoaded]);

  useEffect(() => {
    if (autoFetch && isLoaded) {
      fetchReports();
    }
  }, [autoFetch, fetchReports, isLoaded]);

  return {
    reports,
    isLoading,
    error,
    refetch: fetchReports,
    hasMore,
  };
}
