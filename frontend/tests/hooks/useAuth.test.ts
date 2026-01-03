/**
 * Tests for useAuth hook (frontend wrapper)
 */
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { renderHook } from '@testing-library/react';
import { useAuth } from '../../src/hooks/useAuth';
import { useUser } from '@clerk/nextjs';

// Mock @clerk/nextjs since that's what the actual implementation uses
vi.mock('@clerk/nextjs', () => ({
  useUser: vi.fn(),
}));

describe('useAuth hook', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should return loading state initially', () => {
    vi.mocked(useUser).mockReturnValue({
      isLoaded: false,
      isSignedIn: false,
      user: null,
    } as any);

    const { result } = renderHook(() => useAuth());

    expect(result.current.isLoading).toBe(true);
    expect(result.current.isAuthenticated).toBe(false);
    expect(result.current.user).toBeNull();
    expect(result.current.userId).toBeUndefined();
  });

  it('should return authenticated state when user signed in', () => {
    const mockUser = {
      id: 'user_12345',
      fullName: 'Test User',
      primaryEmailAddress: { emailAddress: 'test@example.com' },
      imageUrl: 'https://example.com/avatar.jpg',
    };

    vi.mocked(useUser).mockReturnValue({
      isLoaded: true,
      isSignedIn: true,
      user: mockUser,
    } as any);

    const { result } = renderHook(() => useAuth());

    expect(result.current.isLoading).toBe(false);
    expect(result.current.isAuthenticated).toBe(true);
    expect(result.current.user).toEqual(mockUser);
    expect(result.current.userId).toBe('user_12345');
  });

  it('should return unauthenticated state when user not signed in', () => {
    vi.mocked(useUser).mockReturnValue({
      isLoaded: true,
      isSignedIn: false,
      user: null,
    } as any);

    const { result } = renderHook(() => useAuth());

    expect(result.current.isLoading).toBe(false);
    expect(result.current.isAuthenticated).toBe(false);
    expect(result.current.user).toBeNull();
    expect(result.current.userId).toBeUndefined();
  });

  it('should return userId from user object', () => {
    const mockUser = {
      id: 'user_test_123',
      firstName: 'Test',
      lastName: 'User',
    };

    vi.mocked(useUser).mockReturnValue({
      isLoaded: true,
      isSignedIn: true,
      user: mockUser,
    } as any);

    const { result } = renderHook(() => useAuth());

    expect(result.current.userId).toBe('user_test_123');
  });

  it('should handle undefined user gracefully', () => {
    vi.mocked(useUser).mockReturnValue({
      isLoaded: true,
      isSignedIn: false,
      user: undefined,
    } as any);

    const { result } = renderHook(() => useAuth());

    expect(result.current.isLoading).toBe(false);
    expect(result.current.isAuthenticated).toBe(false);
    expect(result.current.user).toBeUndefined();
    expect(result.current.userId).toBeUndefined();
  });

  it('should correctly map isLoaded to isLoading (inverted)', () => {
    // When not loaded, isLoading should be true
    vi.mocked(useUser).mockReturnValue({
      isLoaded: false,
      isSignedIn: false,
      user: null,
    } as any);

    const { result, rerender } = renderHook(() => useAuth());
    expect(result.current.isLoading).toBe(true);

    // When loaded, isLoading should be false
    vi.mocked(useUser).mockReturnValue({
      isLoaded: true,
      isSignedIn: true,
      user: { id: 'user_123' },
    } as any);

    rerender();
    expect(result.current.isLoading).toBe(false);
  });
});
