/**
 * Tests for useAuth hook (frontend wrapper)
 */
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { renderHook, waitFor } from '@testing-library/react';
import { useAuth } from '../../src/hooks/useAuth';
import { useUser, useClerk } from '@clerk/clerk-react';

// Mock the Clerk module - must mock @clerk/clerk-react since that's what shared package uses
vi.mock('@clerk/clerk-react', () => ({
  useUser: vi.fn(),
  useClerk: vi.fn(),
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

  it('should return authenticated state when user signed in', async () => {
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
    });
    vi.mocked(useClerk).mockReturnValue({
      signOut: vi.fn(),
      openSignIn: vi.fn(),
      openSignUp: vi.fn(),
    });

    const { result } = renderHook(() => useAuth());

    await waitFor(() => {
      expect(result.current.isLoading).toBe(false);
      expect(result.current.isAuthenticated).toBe(true);
      expect(result.current.user).not.toBeNull();
      expect(result.current.user?.userId).toBe('user_12345');
      expect(result.current.user?.email).toBe('test@example.com');
    });
  });

  it('should return unauthenticated state when user not signed in', () => {
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

  it('should provide signOut function', () => {
    const mockSignOut = vi.fn();

    vi.mocked(useUser).mockReturnValue({
      isLoaded: true,
      isSignedIn: false,
      user: null,
    });
    vi.mocked(useClerk).mockReturnValue({
      signOut: mockSignOut,
      openSignIn: vi.fn(),
      openSignUp: vi.fn(),
    });

    const { result } = renderHook(() => useAuth());

    expect(result.current.signOut).toBeDefined();
    expect(typeof result.current.signOut).toBe('function');
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

    expect(result.current.openSignIn).toBeDefined();
    expect(typeof result.current.openSignIn).toBe('function');
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

    expect(result.current.openSignUp).toBeDefined();
    expect(typeof result.current.openSignUp).toBe('function');
  });
});
