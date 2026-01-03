/**
 * User-related TypeScript interfaces
 * Portable across projects using Clerk authentication
 */

export type AuthProvider = 'google' | 'apple' | 'facebook' | 'email';

export interface User {
  id: string;
  clerkUserId: string;
  email: string;
  firstName?: string;
  lastName?: string;
  profileImageUrl?: string;
  authProvider: AuthProvider;
  emailVerified: boolean;
  createdAt: Date;
  updatedAt: Date;
  deletedAt?: Date | null;
}

export interface UserProfile {
  userId: string;
  displayName: string;
  email: string;
  avatarUrl?: string;
  isSubscribed: boolean;
}

export interface AuthState {
  isAuthenticated: boolean;
  isLoading: boolean;
  user: UserProfile | null;
  error: string | null;
}
