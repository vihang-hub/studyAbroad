/**
 * Generic typed fetch wrapper for backend API calls
 * Configurable backend URL via environment variables
 */

import type { ApiResponse, ApiError, FetchOptions } from '../types/api';

export interface ApiClientConfig {
  baseUrl: string;
  defaultHeaders?: Record<string, string>;
}

/**
 * Get API client configuration from environment variables
 */
export function getApiConfig(): ApiClientConfig {
  const baseUrl = process.env.NEXT_PUBLIC_API_URL
    || process.env.API_URL
    || 'http://localhost:8000';

  return {
    baseUrl,
    defaultHeaders: {
      'Content-Type': 'application/json',
    },
  };
}

/**
 * Generic typed fetch function
 * @param endpoint - API endpoint (e.g., '/reports')
 * @param options - Fetch options
 * @returns Typed API response
 */
export async function fetchApi<T>(
  endpoint: string,
  options: FetchOptions = {},
): Promise<ApiResponse<T>> {
  const config = getApiConfig();
  const { baseUrl = config.baseUrl, token, ...fetchOptions } = options;

  const url = `${baseUrl}${endpoint}`;

  const headers: Record<string, string> = {
    ...config.defaultHeaders,
    ...((fetchOptions.headers as Record<string, string>) || {}),
  };

  if (token) {
    headers.Authorization = `Bearer ${token}`;
  }

  try {
    const response = await fetch(url, {
      ...fetchOptions,
      headers,
    });

    const data = await response.json().catch(() => null);

    if (!response.ok) {
      const error: ApiError = {
        code: data?.code || 'UNKNOWN_ERROR',
        message: data?.message || response.statusText,
        details: data?.details,
        statusCode: response.status,
      };

      return {
        success: false,
        error,
      };
    }

    return {
      success: true,
      data: data as T,
    };
  } catch (error) {
    const apiError: ApiError = {
      code: 'NETWORK_ERROR',
      message: error instanceof Error ? error.message : 'Network request failed',
      statusCode: 0,
    };

    return {
      success: false,
      error: apiError,
    };
  }
}

/**
 * Convenience methods for common HTTP verbs
 */
export const api = {
  get: <T>(endpoint: string, options?: FetchOptions) => fetchApi<T>(endpoint, { ...options, method: 'GET' }),

  post: <T>(endpoint: string, body?: unknown, options?: FetchOptions) => fetchApi<T>(endpoint, { ...options, method: 'POST', body: JSON.stringify(body) }),

  put: <T>(endpoint: string, body?: unknown, options?: FetchOptions) => fetchApi<T>(endpoint, { ...options, method: 'PUT', body: JSON.stringify(body) }),

  patch: <T>(endpoint: string, body?: unknown, options?: FetchOptions) => fetchApi<T>(endpoint, { ...options, method: 'PATCH', body: JSON.stringify(body) }),

  delete: <T>(endpoint: string, options?: FetchOptions) => fetchApi<T>(endpoint, { ...options, method: 'DELETE' }),
};
