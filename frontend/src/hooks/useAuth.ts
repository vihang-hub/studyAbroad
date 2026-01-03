/**
 * Authentication hook for frontend
 * Uses Clerk for authentication
 */

import { useUser } from '@clerk/nextjs';

/**
 * Custom authentication hook
 * Wraps Clerk's useUser hook with consistent interface
 */
export function useAuth() {
  const { user, isLoaded, isSignedIn } = useUser();

  return {
    user,
    isLoading: !isLoaded,
    isAuthenticated: isSignedIn || false,
    userId: user?.id,
  };
}
