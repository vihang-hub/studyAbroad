/**
 * Portable Clerk client initialization
 * Configurable via environment variables for different projects
 */

export interface ClerkConfig {
  publishableKey: string;
  signInUrl?: string;
  signUpUrl?: string;
  afterSignInUrl?: string;
  afterSignUpUrl?: string;
}

/**
 * Get Clerk configuration from environment variables
 * Defaults can be overridden by consuming projects
 */
export function getClerkConfig(): ClerkConfig {
  const publishableKey = process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY
    || process.env.CLERK_PUBLISHABLE_KEY
    || '';

  if (!publishableKey) {
    throw new Error('Clerk publishable key is required. Set NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY or CLERK_PUBLISHABLE_KEY');
  }

  return {
    publishableKey,
    signInUrl: process.env.NEXT_PUBLIC_CLERK_SIGN_IN_URL || '/login',
    signUpUrl: process.env.NEXT_PUBLIC_CLERK_SIGN_UP_URL || '/signup',
    afterSignInUrl: process.env.NEXT_PUBLIC_CLERK_AFTER_SIGN_IN_URL || '/chat',
    afterSignUpUrl: process.env.NEXT_PUBLIC_CLERK_AFTER_SIGN_UP_URL || '/chat',
  };
}

/**
 * Validate Clerk JWT token (backend use)
 * @param _token - JWT token from Authorization header
 * @returns Decoded user ID if valid
 */
export async function validateClerkToken(_token: string): Promise<string | null> {
  // This will be implemented in backend using Clerk SDK
  // Kept here as a shared interface contract
  throw new Error('validateClerkToken should be implemented in backend');
}
