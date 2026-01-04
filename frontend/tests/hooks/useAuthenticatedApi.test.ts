/**
 * Tests for useAuthenticatedApi hook
 * Provides authenticated API methods using Clerk tokens
 */

import { describe, it, expect, vi, beforeEach } from 'vitest';
import { renderHook, act } from '@testing-library/react';
import { useAuthenticatedApi } from '@/hooks/useAuthenticatedApi';

// Mock Clerk's useAuth with hoisted variables
vi.mock('@clerk/nextjs', () => {
  return {
    useAuth: () => ({
      getToken: vi.fn().mockResolvedValue('test-auth-token'),
      isSignedIn: true,
      isLoaded: true,
    }),
  };
});

// Mock API client
vi.mock('@/lib/api-client', () => ({
  api: {
    get: vi.fn().mockResolvedValue({ data: {}, status: 200 }),
    post: vi.fn().mockResolvedValue({ data: {}, status: 200 }),
    put: vi.fn().mockResolvedValue({ data: {}, status: 200 }),
    patch: vi.fn().mockResolvedValue({ data: {}, status: 200 }),
    delete: vi.fn().mockResolvedValue({ data: {}, status: 200 }),
  },
}));

// Import mocked module for test access
import * as apiClientModule from '@/lib/api-client';

describe('useAuthenticatedApi', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  describe('Auth state', () => {
    it('returns isSignedIn from Clerk', () => {
      const { result } = renderHook(() => useAuthenticatedApi());
      expect(result.current.isSignedIn).toBe(true);
    });

    it('returns isLoaded from Clerk', () => {
      const { result } = renderHook(() => useAuthenticatedApi());
      expect(result.current.isLoaded).toBe(true);
    });

    it('returns getAuthToken function', () => {
      const { result } = renderHook(() => useAuthenticatedApi());
      expect(typeof result.current.getAuthToken).toBe('function');
    });
  });

  describe('getAuthToken', () => {
    it('returns token when signed in', async () => {
      const { result } = renderHook(() => useAuthenticatedApi());

      let token: string | null = null;
      await act(async () => {
        token = await result.current.getAuthToken();
      });

      expect(token).toBe('test-auth-token');
    });
  });

  describe('Authenticated GET', () => {
    it('includes auth token in request', async () => {
      const { result } = renderHook(() => useAuthenticatedApi());

      await act(async () => {
        await result.current.get('/test-endpoint');
      });

      expect(apiClientModule.api.get).toHaveBeenCalledWith('/test-endpoint', {
        authToken: 'test-auth-token',
      });
    });

    it('returns API response', async () => {
      vi.mocked(apiClientModule.api.get).mockResolvedValueOnce({
        data: { id: 1 },
        status: 200,
        correlationId: 'test-123',
      });

      const { result } = renderHook(() => useAuthenticatedApi());

      let response;
      await act(async () => {
        response = await result.current.get('/test');
      });

      expect(response).toEqual({
        data: { id: 1 },
        status: 200,
        correlationId: 'test-123',
      });
    });
  });

  describe('Authenticated POST', () => {
    it('includes auth token and body in request', async () => {
      const { result } = renderHook(() => useAuthenticatedApi());

      const body = { name: 'Test' };
      await act(async () => {
        await result.current.post('/create', body);
      });

      expect(apiClientModule.api.post).toHaveBeenCalledWith('/create', body, {
        authToken: 'test-auth-token',
      });
    });

    it('handles POST without body', async () => {
      const { result } = renderHook(() => useAuthenticatedApi());

      await act(async () => {
        await result.current.post('/trigger');
      });

      expect(apiClientModule.api.post).toHaveBeenCalledWith('/trigger', undefined, {
        authToken: 'test-auth-token',
      });
    });
  });

  describe('Authenticated PUT', () => {
    it('includes auth token and body in request', async () => {
      const { result } = renderHook(() => useAuthenticatedApi());

      const body = { name: 'Updated' };
      await act(async () => {
        await result.current.put('/update/1', body);
      });

      expect(apiClientModule.api.put).toHaveBeenCalledWith('/update/1', body, {
        authToken: 'test-auth-token',
      });
    });
  });

  describe('Authenticated PATCH', () => {
    it('includes auth token and body in request', async () => {
      const { result } = renderHook(() => useAuthenticatedApi());

      const body = { field: 'value' };
      await act(async () => {
        await result.current.patch('/patch/1', body);
      });

      expect(apiClientModule.api.patch).toHaveBeenCalledWith('/patch/1', body, {
        authToken: 'test-auth-token',
      });
    });
  });

  describe('Authenticated DELETE', () => {
    it('includes auth token in request', async () => {
      const { result } = renderHook(() => useAuthenticatedApi());

      await act(async () => {
        await result.current.delete('/delete/1');
      });

      expect(apiClientModule.api.delete).toHaveBeenCalledWith('/delete/1', {
        authToken: 'test-auth-token',
      });
    });
  });

  describe('All HTTP methods', () => {
    it('exports all HTTP method functions', () => {
      const { result } = renderHook(() => useAuthenticatedApi());

      expect(typeof result.current.get).toBe('function');
      expect(typeof result.current.post).toBe('function');
      expect(typeof result.current.put).toBe('function');
      expect(typeof result.current.patch).toBe('function');
      expect(typeof result.current.delete).toBe('function');
    });
  });
});
