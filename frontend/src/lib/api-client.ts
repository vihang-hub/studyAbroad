/**
 * API client for frontend
 * Enhanced with correlation IDs, logging, and error handling
 */

import { getClientConfig } from './config';
import {
  logApiRequest,
  logApiResponse,
  logApiError,
} from './logger';

export interface ApiError {
  message: string;
  code?: string;
  status?: number;
  correlationId?: string;
}

export interface ApiResponse<T = unknown> {
  data?: T;
  error?: ApiError;
  status: number;
  correlationId?: string;
}

export interface FetchOptions extends RequestInit {
  timeout?: number;
  correlationId?: string;
}

/**
 * Enhanced fetch wrapper with logging and correlation IDs
 */
export async function fetchApi<T = unknown>(
  endpoint: string,
  options: FetchOptions = {},
): Promise<ApiResponse<T>> {
  const config = getClientConfig();
  const url = `${config.apiUrl}${endpoint}`;
  const method = options.method || 'GET';

  // Generate or use provided correlation ID
  const correlationId = options.correlationId || generateCorrelationId();

  // Start timing
  const startTime = Date.now();

  // Log the request
  logApiRequest(method, endpoint, { correlationId });

  try {
    // Add correlation ID to headers
    const headers = new Headers(options.headers);
    headers.set('X-Correlation-ID', correlationId);
    headers.set('Content-Type', 'application/json');

    // Make the request with timeout
    const controller = new AbortController();
    const timeoutId = options.timeout
      ? setTimeout(() => controller.abort(), options.timeout)
      : null;

    const response = await fetch(url, {
      ...options,
      headers,
      signal: controller.signal,
    });

    if (timeoutId) {
      clearTimeout(timeoutId);
    }

    // Calculate duration
    const duration = Date.now() - startTime;

    // Parse response
    let data: T | undefined;
    let error: ApiError | undefined;

    const contentType = response.headers.get('content-type');
    const isJson = contentType?.includes('application/json');

    if (isJson) {
      const json = await response.json();

      if (response.ok) {
        data = json as T;
      } else {
        error = {
          message: json.message || 'An error occurred',
          code: json.code,
          status: response.status,
          correlationId,
        };
      }
    } else if (!response.ok) {
      error = {
        message: response.statusText || 'An error occurred',
        status: response.status,
        correlationId,
      };
    }

    // Log the response
    logApiResponse(method, endpoint, response.status, duration, {
      correlationId,
      error: error?.message,
    });

    return {
      data,
      error,
      status: response.status,
      correlationId,
    };
  } catch (err) {
    const duration = Date.now() - startTime;

    // Handle timeout
    if (err instanceof Error && err.name === 'AbortError') {
      const error: ApiError = {
        message: 'Request timeout',
        code: 'TIMEOUT',
        correlationId,
      };

      logApiError(method, endpoint, err, { correlationId, duration });

      return {
        error,
        status: 408,
        correlationId,
      };
    }

    // Handle other errors
    const error: ApiError = {
      message: err instanceof Error ? err.message : 'Network error',
      code: 'NETWORK_ERROR',
      correlationId,
    };

    logApiError(method, endpoint, err, { correlationId, duration });

    return {
      error,
      status: 0,
      correlationId,
    };
  }
}

/**
 * Convenience methods for common HTTP verbs
 */
export const api = {
  get: <T = unknown>(endpoint: string, options?: FetchOptions) => fetchApi<T>(endpoint, { ...options, method: 'GET' }),

  post: <T = unknown>(endpoint: string, body?: unknown, options?: FetchOptions) => fetchApi<T>(endpoint, {
    ...options,
    method: 'POST',
    body: body ? JSON.stringify(body) : undefined,
  }),

  put: <T = unknown>(endpoint: string, body?: unknown, options?: FetchOptions) => fetchApi<T>(endpoint, {
    ...options,
    method: 'PUT',
    body: body ? JSON.stringify(body) : undefined,
  }),

  patch: <T = unknown>(endpoint: string, body?: unknown, options?: FetchOptions) => fetchApi<T>(endpoint, {
    ...options,
    method: 'PATCH',
    body: body ? JSON.stringify(body) : undefined,
  }),

  delete: <T = unknown>(endpoint: string, options?: FetchOptions) => fetchApi<T>(endpoint, { ...options, method: 'DELETE' }),
};

/**
 * Get API configuration
 */
export function getApiConfig() {
  const config = getClientConfig();
  return {
    apiUrl: config.apiUrl,
    timeout: 30000, // 30 seconds default
  };
}

/**
 * Generate a correlation ID
 */
function generateCorrelationId(): string {
  return `${Date.now()}-${Math.random().toString(36).substring(2, 11)}`;
}

/**
 * Execute API call with generated correlation ID
 */
export async function apiWithContext<T>(
  fn: () => Promise<ApiResponse<T>>,
): Promise<ApiResponse<T>> {
  return fn();
}
