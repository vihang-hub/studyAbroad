/**
 * Supabase query hooks
 * Provides typed data fetching and mutations
 */

import { useEffect, useState, useCallback } from 'react';
import type { SupabaseClient, PostgrestFilterBuilder } from '@supabase/supabase-js';
import { getSupabase } from '../lib/supabase';

// eslint-disable-next-line @typescript-eslint/no-explicit-any
type QueryFilter = PostgrestFilterBuilder<any, any, any>;

export interface UseSupabaseQueryOptions<T> {
  table: string;
  select?: string;
  filter?: (query: QueryFilter) => QueryFilter;
  enabled?: boolean;
  onSuccess?: (data: T[]) => void;
  onError?: (error: Error) => void;
}

export interface UseSupabaseQueryResult<T> {
  data: T[] | null;
  isLoading: boolean;
  error: Error | null;
  refetch: () => Promise<void>;
}

/**
 * Generic Supabase query hook
 * @param options - Query configuration
 * @returns Query result with data, loading state, and refetch function
 */
export function useSupabaseQuery<T>(
  options: UseSupabaseQueryOptions<T>,
): UseSupabaseQueryResult<T> {
  const [data, setData] = useState<T[] | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [error, setError] = useState<Error | null>(null);

  const supabase = getSupabase();

  const fetchData = useCallback(async () => {
    if (options.enabled === false) {
      setIsLoading(false);
      return;
    }

    try {
      setIsLoading(true);
      setError(null);

      let query = supabase
        .from(options.table)
        .select(options.select || '*');

      if (options.filter) {
        query = options.filter(query);
      }

      const { data: result, error: queryError } = await query;

      if (queryError) {
        throw new Error(queryError.message);
      }

      setData(result as T[]);
      if (options.onSuccess) {
        options.onSuccess(result as T[]);
      }
    } catch (err) {
      const queryError = err instanceof Error ? err : new Error('Unknown error');
      setError(queryError);
      if (options.onError) {
        options.onError(queryError);
      }
    } finally {
      setIsLoading(false);
    }
  }, [options, supabase]);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  return {
    data,
    isLoading,
    error,
    refetch: fetchData,
  };
}

/**
 * Get Supabase client instance
 * Use this for imperative operations
 */
export function useSupabaseClient(): SupabaseClient {
  return getSupabase();
}
