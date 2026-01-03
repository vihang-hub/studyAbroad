/**
 * Clerk authentication hook
 * Provides user state, login, and logout functionality
 */

import { useUser, useClerk } from '@clerk/clerk-react';
import { useMemo } from 'react';
import type { AuthState, UserProfile } from '../types/user';

export function useAuth(): AuthState & {
  signOut: () => Promise<void>;
  openSignIn: () => void;
  openSignUp: () => void;
} {
  const { user, isLoaded, isSignedIn } = useUser();
  const { signOut, openSignIn, openSignUp } = useClerk();

  const authState: AuthState = useMemo(() => {
    if (!isLoaded) {
      return {
        isAuthenticated: false,
        isLoading: true,
        user: null,
        error: null,
      };
    }

    if (!isSignedIn || !user) {
      return {
        isAuthenticated: false,
        isLoading: false,
        user: null,
        error: null,
      };
    }

    const userProfile: UserProfile = {
      userId: user.id,
      displayName: user.fullName || user.username || 'User',
      email: user.primaryEmailAddress?.emailAddress || '',
      avatarUrl: user.imageUrl,
      isSubscribed: false, // Will be determined by backend
    };

    return {
      isAuthenticated: true,
      isLoading: false,
      user: userProfile,
      error: null,
    };
  }, [isLoaded, isSignedIn, user]);

  return {
    ...authState,
    signOut: () => signOut(),
    openSignIn: () => openSignIn(),
    openSignUp: () => openSignUp(),
  };
}
