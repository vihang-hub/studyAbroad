/**
 * Tests for useAuth hook (shared package)
 */
// @ts-nocheck

import { describe, it, expect, vi, beforeEach } from 'vitest';
import { renderHook, waitFor } from '@testing-library/react';
import { useAuth } from '../../src/hooks/useAuth';
import { useUser, useClerk } from '@clerk/clerk-react';

// Mock Clerk React
vi.mock('@clerk/clerk-react', () => ({
  useUser: vi.fn(),
  useClerk: vi.fn(),
}));

describe('useAuth hook (shared)', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should return loading state when not loaded', () => {
    vi.mocked(useUser).mockReturnValue({
      isLoaded: false,
      isSignedIn: false,
      user: null,
    });

    vi.mocked(useClerk).mockReturnValue({
      signOut: vi.fn(),
      openSignIn: vi.fn(),
      openSignUp: vi.fn(),
    });

    const { result } = renderHook(() => useAuth());

    expect(result.current.isLoading).toBe(true);
    expect(result.current.isAuthenticated).toBe(false);
    expect(result.current.user).toBeNull();
  });

  it('should return authenticated user when signed in', () => {
    const mockUser = {
      id: 'user_test_12345',
      fullName: 'John Doe',
      username: 'johndoe',
      primaryEmailAddress: {
        emailAddress: 'john@example.com',
      },
      imageUrl: 'https://example.com/avatar.png',
    };

    vi.mocked(useUser).mockReturnValue({
      isLoaded: true,
      isSignedIn: true,
      user: mockUser,
    });

    vi.mocked(useClerk).mockReturnValue({
      signOut: vi.fn().mockResolvedValue(undefined),
      openSignIn: vi.fn(),
      openSignUp: vi.fn(),
    });

    const { result } = renderHook(() => useAuth());

    expect(result.current.isLoading).toBe(false);
    expect(result.current.isAuthenticated).toBe(true);
    expect(result.current.user).not.toBeNull();
    expect(result.current.user?.userId).toBe('user_test_12345');
    expect(result.current.user?.displayName).toBe('John Doe');
    expect(result.current.user?.email).toBe('john@example.com');
    expect(result.current.user?.avatarUrl).toBe('https://example.com/avatar.png');
  });

  it('should use username as fallback for displayName', () => {
    const mockUser = {
      id: 'user_test_12345',
      fullName: null,
      username: 'johndoe',
      primaryEmailAddress: {
        emailAddress: 'john@example.com',
      },
      imageUrl: null,
    };

    vi.mocked(useUser).mockReturnValue({
      isLoaded: true,
      isSignedIn: true,
      user: mockUser,
    });

    vi.mocked(useClerk).mockReturnValue({
      signOut: vi.fn(),
      openSignIn: vi.fn(),
      openSignUp: vi.fn(),
    });

    const { result } = renderHook(() => useAuth());

    expect(result.current.user?.displayName).toBe('johndoe');
  });

  it('should use "User" as default displayName', () => {
    const mockUser = {
      id: 'user_test_12345',
      fullName: null,
      username: null,
      primaryEmailAddress: {
        emailAddress: 'john@example.com',
      },
      imageUrl: null,
    };

    vi.mocked(useUser).mockReturnValue({
      isLoaded: true,
      isSignedIn: true,
      user: mockUser,
    });

    vi.mocked(useClerk).mockReturnValue({
      signOut: vi.fn(),
      openSignIn: vi.fn(),
      openSignUp: vi.fn(),
    });

    const { result } = renderHook(() => useAuth());

    expect(result.current.user?.displayName).toBe('User');
  });

  it('should return unauthenticated state when not signed in', () => {
    vi.mocked(useUser).mockReturnValue({
      isLoaded: true,
      isSignedIn: false,
      user: null,
    });

    vi.mocked(useClerk).mockReturnValue({
      signOut: vi.fn(),
      openSignIn: vi.fn(),
      openSignUp: vi.fn(),
    });

    const { result } = renderHook(() => useAuth());

    expect(result.current.isLoading).toBe(false);
    expect(result.current.isAuthenticated).toBe(false);
    expect(result.current.user).toBeNull();
  });

  it('should provide signOut function that calls Clerk signOut', async () => {
    const mockSignOut = vi.fn().mockResolvedValue(undefined);

    vi.mocked(useUser).mockReturnValue({
      isLoaded: true,
      isSignedIn: true,
      user: { id: 'user_123' },
    });

    vi.mocked(useClerk).mockReturnValue({
      signOut: mockSignOut,
      openSignIn: vi.fn(),
      openSignUp: vi.fn(),
    });

    const { result } = renderHook(() => useAuth());

    await result.current.signOut();

    expect(mockSignOut).toHaveBeenCalledTimes(1);
  });

  it('should provide openSignIn function', () => {
    const mockOpenSignIn = vi.fn();

    vi.mocked(useUser).mockReturnValue({
      isLoaded: true,
      isSignedIn: false,
      user: null,
    });

    vi.mocked(useClerk).mockReturnValue({
      signOut: vi.fn(),
      openSignIn: mockOpenSignIn,
      openSignUp: vi.fn(),
    });

    const { result } = renderHook(() => useAuth());

    result.current.openSignIn();

    expect(mockOpenSignIn).toHaveBeenCalledTimes(1);
  });

  it('should provide openSignUp function', () => {
    const mockOpenSignUp = vi.fn();

    vi.mocked(useUser).mockReturnValue({
      isLoaded: true,
      isSignedIn: false,
      user: null,
    });

    vi.mocked(useClerk).mockReturnValue({
      signOut: vi.fn(),
      openSignIn: vi.fn(),
      openSignUp: mockOpenSignUp,
    });

    const { result } = renderHook(() => useAuth());

    result.current.openSignUp();

    expect(mockOpenSignUp).toHaveBeenCalledTimes(1);
  });

  it('should set isSubscribed to false by default', () => {
    vi.mocked(useUser).mockReturnValue({
      isLoaded: true,
      isSignedIn: true,
      user: {
        id: 'user_123',
        fullName: 'Test User',
        primaryEmailAddress: { emailAddress: 'test@example.com' },
      },
    });

    vi.mocked(useClerk).mockReturnValue({
      signOut: vi.fn(),
      openSignIn: vi.fn(),
      openSignUp: vi.fn(),
    });

    const { result } = renderHook(() => useAuth());

    expect(result.current.user?.isSubscribed).toBe(false);
  });
});
