/**
 * Hook for authenticated API calls
 * Uses Clerk's getToken to add Authorization header to requests
 */

'use client';

import { useCallback } from 'react';
import { useAuth } from '@clerk/nextjs';
import { api, FetchOptions, ApiResponse } from '@/lib/api-client';

/**
 * Hook that provides API methods with automatic Clerk authentication
 * @returns Authenticated API methods and auth state
 */
export function useAuthenticatedApi() {
  const { getToken, isSignedIn, isLoaded } = useAuth();

  /**
   * Get the current auth token
   * Returns null if not signed in
   */
  const getAuthToken = useCallback(async (): Promise<string | null> => {
    if (!isSignedIn) {
      return null;
    }
    try {
      const token = await getToken();
      return token;
    } catch {
      return null;
    }
  }, [isSignedIn, getToken]);

  /**
   * Make authenticated GET request
   */
  const authGet = useCallback(
    async <T = unknown>(
      endpoint: string,
      options?: Omit<FetchOptions, 'authToken'>
    ): Promise<ApiResponse<T>> => {
      const token = await getAuthToken();
      return api.get<T>(endpoint, {
        ...options,
        authToken: token || undefined,
      });
    },
    [getAuthToken]
  );

  /**
   * Make authenticated POST request
   */
  const authPost = useCallback(
    async <T = unknown>(
      endpoint: string,
      body?: unknown,
      options?: Omit<FetchOptions, 'authToken'>
    ): Promise<ApiResponse<T>> => {
      const token = await getAuthToken();
      return api.post<T>(endpoint, body, {
        ...options,
        authToken: token || undefined,
      });
    },
    [getAuthToken]
  );

  /**
   * Make authenticated PUT request
   */
  const authPut = useCallback(
    async <T = unknown>(
      endpoint: string,
      body?: unknown,
      options?: Omit<FetchOptions, 'authToken'>
    ): Promise<ApiResponse<T>> => {
      const token = await getAuthToken();
      return api.put<T>(endpoint, body, {
        ...options,
        authToken: token || undefined,
      });
    },
    [getAuthToken]
  );

  /**
   * Make authenticated PATCH request
   */
  const authPatch = useCallback(
    async <T = unknown>(
      endpoint: string,
      body?: unknown,
      options?: Omit<FetchOptions, 'authToken'>
    ): Promise<ApiResponse<T>> => {
      const token = await getAuthToken();
      return api.patch<T>(endpoint, body, {
        ...options,
        authToken: token || undefined,
      });
    },
    [getAuthToken]
  );

  /**
   * Make authenticated DELETE request
   */
  const authDelete = useCallback(
    async <T = unknown>(
      endpoint: string,
      options?: Omit<FetchOptions, 'authToken'>
    ): Promise<ApiResponse<T>> => {
      const token = await getAuthToken();
      return api.delete<T>(endpoint, {
        ...options,
        authToken: token || undefined,
      });
    },
    [getAuthToken]
  );

  return {
    // Auth state
    isSignedIn,
    isLoaded,
    getAuthToken,

    // Authenticated API methods
    get: authGet,
    post: authPost,
    put: authPut,
    patch: authPatch,
    delete: authDelete,
  };
}
