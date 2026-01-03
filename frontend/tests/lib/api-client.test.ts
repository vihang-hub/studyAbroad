/**
 * Tests for API client
 * Coverage target: 100% (high-impact file: ~10-12% total frontend coverage)
 */

import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import {
  fetchApi,
  api,
  getApiConfig,
  type ApiResponse,
  type ApiError,
} from '../../src/lib/api-client';

// Mock dependencies
vi.mock('../../src/lib/config', () => ({
  getConfig: vi.fn(() => ({
    apiUrl: 'http://localhost:8000',
    environment: 'test',
  })),
}));

vi.mock('../../src/lib/logger', () => ({
  logApiRequest: vi.fn(),
  logApiResponse: vi.fn(),
  logApiError: vi.fn(),
}));

// Mock global fetch
global.fetch = vi.fn();

describe('api-client', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    vi.useFakeTimers();
  });

  afterEach(() => {
    vi.useRealTimers();
  });

  describe('fetchApi', () => {
    describe('Successful requests', () => {
      it('should make GET request and return JSON data', async () => {
        const mockData = { id: 1, name: 'Test' };
        (global.fetch as ReturnType<typeof vi.fn>).mockResolvedValueOnce({
          ok: true,
          status: 200,
          headers: new Headers({ 'content-type': 'application/json' }),
          json: async () => mockData,
        });

        const result = await fetchApi('/test');

        expect(result.data).toEqual(mockData);
        expect(result.status).toBe(200);
        expect(result.error).toBeUndefined();
        expect(result.correlationId).toBeDefined();
      });

      it('should make POST request with body', async () => {
        const mockData = { success: true };
        const requestBody = { name: 'New Item' };

        (global.fetch as ReturnType<typeof vi.fn>).mockResolvedValueOnce({
          ok: true,
          status: 201,
          headers: new Headers({ 'content-type': 'application/json' }),
          json: async () => mockData,
        });

        const result = await fetchApi('/items', {
          method: 'POST',
          body: JSON.stringify(requestBody),
        });

        expect(result.data).toEqual(mockData);
        expect(result.status).toBe(201);

        const fetchCall = (global.fetch as ReturnType<typeof vi.fn>).mock.calls[0];
        expect(fetchCall[1].method).toBe('POST');
        expect(fetchCall[1].body).toBe(JSON.stringify(requestBody));
      });

      it('should include correlation ID in request headers', async () => {
        const customCorrelationId = 'test-correlation-123';

        (global.fetch as ReturnType<typeof vi.fn>).mockResolvedValueOnce({
          ok: true,
          status: 200,
          headers: new Headers({ 'content-type': 'application/json' }),
          json: async () => ({}),
        });

        const result = await fetchApi('/test', {
          correlationId: customCorrelationId,
        });

        expect(result.correlationId).toBe(customCorrelationId);

        const fetchCall = (global.fetch as ReturnType<typeof vi.fn>).mock.calls[0];
        const headers = fetchCall[1].headers as Headers;
        expect(headers.get('X-Correlation-ID')).toBe(customCorrelationId);
      });

      it('should generate correlation ID if not provided', async () => {
        (global.fetch as ReturnType<typeof vi.fn>).mockResolvedValueOnce({
          ok: true,
          status: 200,
          headers: new Headers({ 'content-type': 'application/json' }),
          json: async () => ({}),
        });

        const result = await fetchApi('/test');

        expect(result.correlationId).toBeDefined();
        expect(typeof result.correlationId).toBe('string');
        expect(result.correlationId?.length).toBeGreaterThan(0);
      });

      it('should set Content-Type header to application/json', async () => {
        (global.fetch as ReturnType<typeof vi.fn>).mockResolvedValueOnce({
          ok: true,
          status: 200,
          headers: new Headers({ 'content-type': 'application/json' }),
          json: async () => ({}),
        });

        await fetchApi('/test');

        const fetchCall = (global.fetch as ReturnType<typeof vi.fn>).mock.calls[0];
        const headers = fetchCall[1].headers as Headers;
        expect(headers.get('Content-Type')).toBe('application/json');
      });
    });

    describe('Error responses', () => {
      it('should handle 400 error with JSON error message', async () => {
        const errorResponse = {
          message: 'Invalid request',
          code: 'INVALID_REQUEST',
        };

        (global.fetch as ReturnType<typeof vi.fn>).mockResolvedValueOnce({
          ok: false,
          status: 400,
          headers: new Headers({ 'content-type': 'application/json' }),
          json: async () => errorResponse,
        });

        const result = await fetchApi('/test');

        expect(result.data).toBeUndefined();
        expect(result.error).toBeDefined();
        expect(result.error?.message).toBe('Invalid request');
        expect(result.error?.code).toBe('INVALID_REQUEST');
        expect(result.error?.status).toBe(400);
        expect(result.status).toBe(400);
      });

      it('should handle 401 unauthorized error', async () => {
        (global.fetch as ReturnType<typeof vi.fn>).mockResolvedValueOnce({
          ok: false,
          status: 401,
          statusText: 'Unauthorized',
          headers: new Headers({ 'content-type': 'application/json' }),
          json: async () => ({ message: 'Unauthorized' }),
        });

        const result = await fetchApi('/protected');

        expect(result.error?.status).toBe(401);
        expect(result.error?.message).toBe('Unauthorized');
      });

      it('should handle 404 not found error', async () => {
        (global.fetch as ReturnType<typeof vi.fn>).mockResolvedValueOnce({
          ok: false,
          status: 404,
          headers: new Headers({ 'content-type': 'application/json' }),
          json: async () => ({ message: 'Not found' }),
        });

        const result = await fetchApi('/nonexistent');

        expect(result.error?.status).toBe(404);
        expect(result.error?.message).toBe('Not found');
      });

      it('should handle 500 server error', async () => {
        (global.fetch as ReturnType<typeof vi.fn>).mockResolvedValueOnce({
          ok: false,
          status: 500,
          headers: new Headers({ 'content-type': 'application/json' }),
          json: async () => ({ message: 'Internal server error' }),
        });

        const result = await fetchApi('/error');

        expect(result.error?.status).toBe(500);
        expect(result.error?.message).toBe('Internal server error');
      });

      it('should handle error without JSON response', async () => {
        (global.fetch as ReturnType<typeof vi.fn>).mockResolvedValueOnce({
          ok: false,
          status: 503,
          statusText: 'Service Unavailable',
          headers: new Headers({ 'content-type': 'text/plain' }),
        });

        const result = await fetchApi('/unavailable');

        expect(result.error?.status).toBe(503);
        expect(result.error?.message).toBe('Service Unavailable');
      });

      it('should provide default error message if none available', async () => {
        (global.fetch as ReturnType<typeof vi.fn>).mockResolvedValueOnce({
          ok: false,
          status: 500,
          statusText: '',
          headers: new Headers({ 'content-type': 'text/plain' }),
        });

        const result = await fetchApi('/error');

        expect(result.error?.message).toBe('An error occurred');
      });
    });

    describe('Timeout handling', () => {
      it('should timeout request after specified duration', async () => {
        // Mock a delayed fetch that never resolves
        const abortError = new Error('The operation was aborted');
        abortError.name = 'AbortError';
        
        (global.fetch as ReturnType<typeof vi.fn>).mockRejectedValueOnce(abortError);

        const result = await fetchApi('/slow', { timeout: 1000 });

        expect(result.error).toBeDefined();
        expect(result.error?.code).toBe('TIMEOUT');
        expect(result.error?.message).toBe('Request timeout');
        expect(result.status).toBe(408);
      });

      it('should not timeout if request completes in time', async () => {
        (global.fetch as ReturnType<typeof vi.fn>).mockResolvedValueOnce({
          ok: true,
          status: 200,
          headers: new Headers({ 'content-type': 'application/json' }),
          json: async () => ({ data: 'fast' }),
        });

        const result = await fetchApi('/fast', { timeout: 5000 });

        expect(result.error).toBeUndefined();
        expect(result.data).toEqual({ data: 'fast' });
      });
    });

    describe('Network errors', () => {
      it('should handle network error', async () => {
        (global.fetch as ReturnType<typeof vi.fn>).mockRejectedValueOnce(
          new Error('Network error'),
        );

        const result = await fetchApi('/test');

        expect(result.error).toBeDefined();
        expect(result.error?.code).toBe('NETWORK_ERROR');
        expect(result.error?.message).toBe('Network error');
        expect(result.status).toBe(0);
      });

      it('should handle non-Error exceptions', async () => {
        (global.fetch as ReturnType<typeof vi.fn>).mockRejectedValueOnce('String error');

        const result = await fetchApi('/test');

        expect(result.error).toBeDefined();
        expect(result.error?.code).toBe('NETWORK_ERROR');
        expect(result.error?.message).toBe('Network error');
      });

      it('should handle abort error as timeout', async () => {
        const abortError = new Error('The operation was aborted');
        abortError.name = 'AbortError';

        (global.fetch as ReturnType<typeof vi.fn>).mockRejectedValueOnce(abortError);

        const result = await fetchApi('/test');

        expect(result.error?.code).toBe('TIMEOUT');
        expect(result.error?.message).toBe('Request timeout');
        expect(result.status).toBe(408);
      });
    });
  });

  describe('api convenience methods', () => {
    beforeEach(() => {
      (global.fetch as ReturnType<typeof vi.fn>).mockResolvedValue({
        ok: true,
        status: 200,
        headers: new Headers({ 'content-type': 'application/json' }),
        json: async () => ({ success: true }),
      });
    });

    describe('api.get', () => {
      it('should make GET request', async () => {
        await api.get('/users');

        const fetchCall = (global.fetch as ReturnType<typeof vi.fn>).mock.calls[0];
        expect(fetchCall[1].method).toBe('GET');
      });

      it('should pass through options', async () => {
        const correlationId = 'test-123';
        await api.get('/users', { correlationId });

        const fetchCall = (global.fetch as ReturnType<typeof vi.fn>).mock.calls[0];
        const headers = fetchCall[1].headers as Headers;
        expect(headers.get('X-Correlation-ID')).toBe(correlationId);
      });
    });

    describe('api.post', () => {
      it('should make POST request with body', async () => {
        const body = { name: 'Test User' };
        await api.post('/users', body);

        const fetchCall = (global.fetch as ReturnType<typeof vi.fn>).mock.calls[0];
        expect(fetchCall[1].method).toBe('POST');
        expect(fetchCall[1].body).toBe(JSON.stringify(body));
      });

      it('should make POST request without body', async () => {
        await api.post('/users');

        const fetchCall = (global.fetch as ReturnType<typeof vi.fn>).mock.calls[0];
        expect(fetchCall[1].method).toBe('POST');
        expect(fetchCall[1].body).toBeUndefined();
      });
    });

    describe('api.put', () => {
      it('should make PUT request with body', async () => {
        const body = { name: 'Updated User' };
        await api.put('/users/1', body);

        const fetchCall = (global.fetch as ReturnType<typeof vi.fn>).mock.calls[0];
        expect(fetchCall[1].method).toBe('PUT');
        expect(fetchCall[1].body).toBe(JSON.stringify(body));
      });

      it('should make PUT request without body', async () => {
        await api.put('/users/1');

        const fetchCall = (global.fetch as ReturnType<typeof vi.fn>).mock.calls[0];
        expect(fetchCall[1].method).toBe('PUT');
        expect(fetchCall[1].body).toBeUndefined();
      });
    });

    describe('api.patch', () => {
      it('should make PATCH request with body', async () => {
        const body = { status: 'active' };
        await api.patch('/users/1', body);

        const fetchCall = (global.fetch as ReturnType<typeof vi.fn>).mock.calls[0];
        expect(fetchCall[1].method).toBe('PATCH');
        expect(fetchCall[1].body).toBe(JSON.stringify(body));
      });
    });

    describe('api.delete', () => {
      it('should make DELETE request', async () => {
        await api.delete('/users/1');

        const fetchCall = (global.fetch as ReturnType<typeof vi.fn>).mock.calls[0];
        expect(fetchCall[1].method).toBe('DELETE');
      });

      it('should pass through options', async () => {
        const correlationId = 'delete-123';
        await api.delete('/users/1', { correlationId });

        const fetchCall = (global.fetch as ReturnType<typeof vi.fn>).mock.calls[0];
        const headers = fetchCall[1].headers as Headers;
        expect(headers.get('X-Correlation-ID')).toBe(correlationId);
      });
    });
  });

  describe('getApiConfig', () => {
    it('should return API configuration', () => {
      const config = getApiConfig();

      expect(config).toEqual({
        apiUrl: 'http://localhost:8000',
        timeout: 30000,
      });
    });

    it('should return timeout default', () => {
      const config = getApiConfig();

      expect(config.timeout).toBe(30000);
    });
  });

  describe('TypeScript types', () => {
    it('should support typed responses', async () => {
      interface User {
        id: number;
        name: string;
      }

      const mockUser: User = { id: 1, name: 'Test User' };

      (global.fetch as ReturnType<typeof vi.fn>).mockResolvedValueOnce({
        ok: true,
        status: 200,
        headers: new Headers({ 'content-type': 'application/json' }),
        json: async () => mockUser,
      });

      const result: ApiResponse<User> = await fetchApi<User>('/users/1');

      expect(result.data).toEqual(mockUser);
      expect(result.data?.id).toBe(1);
      expect(result.data?.name).toBe('Test User');
    });

    it('should support typed POST bodies', async () => {
      interface CreateUserRequest {
        name: string;
        email: string;
      }

      const requestBody: CreateUserRequest = {
        name: 'New User',
        email: 'new@example.com',
      };

      (global.fetch as ReturnType<typeof vi.fn>).mockResolvedValueOnce({
        ok: true,
        status: 201,
        headers: new Headers({ 'content-type': 'application/json' }),
        json: async () => ({ id: 1, ...requestBody }),
      });

      const result = await api.post<{ id: number } & CreateUserRequest>(
        '/users',
        requestBody,
      );

      expect(result.data?.id).toBeDefined();
      expect(result.data?.name).toBe(requestBody.name);
    });
  });

  describe('Edge cases', () => {
    it('should handle empty response body', async () => {
      (global.fetch as ReturnType<typeof vi.fn>).mockResolvedValueOnce({
        ok: true,
        status: 204,
        headers: new Headers({ 'content-type': 'application/json' }),
        json: async () => null,
      });

      const result = await fetchApi('/test');

      expect(result.status).toBe(204);
      expect(result.data).toBeNull();
    });

    it('should handle missing content-type header', async () => {
      (global.fetch as ReturnType<typeof vi.fn>).mockResolvedValueOnce({
        ok: true,
        status: 200,
        headers: new Headers(),
        json: async () => ({ data: 'test' }),
      });

      const result = await fetchApi('/test');

      expect(result.status).toBe(200);
    });

    it('should include correlation ID in error responses', async () => {
      const correlationId = 'error-123';

      (global.fetch as ReturnType<typeof vi.fn>).mockResolvedValueOnce({
        ok: false,
        status: 400,
        headers: new Headers({ 'content-type': 'application/json' }),
        json: async () => ({ message: 'Bad request' }),
      });

      const result = await fetchApi('/test', { correlationId });

      expect(result.error?.correlationId).toBe(correlationId);
      expect(result.correlationId).toBe(correlationId);
    });
  });
});
