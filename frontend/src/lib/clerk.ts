/**
 * Clerk client for frontend
 * Provides Clerk configuration utilities
 */

import { getConfig } from './config';

/**
 * Get Clerk configuration
 */
export function getClerkConfig() {
  const config = getConfig();
  return {
    publishableKey: config.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY,
    secretKey: config.CLERK_SECRET_KEY,
  };
}

/**
 * Check if Clerk is properly configured with real API keys
 * @returns true if Clerk has real keys, false if using placeholders
 */
export function isClerkConfigured(): boolean {
  const publishableKey = process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY || '';
  const secretKey = process.env.CLERK_SECRET_KEY || '';

  // Check if keys contain placeholder text
  const hasPlaceholderPublishable = publishableKey.includes('YOUR_')
    || publishableKey.includes('your_')
    || publishableKey === ''
    || publishableKey === 'pk_test_your_clerk_publishable_key';

  const hasPlaceholderSecret = secretKey.includes('YOUR_')
    || secretKey.includes('your_')
    || secretKey === ''
    || secretKey === 'sk_test_your_clerk_secret_key';

  return !hasPlaceholderPublishable && !hasPlaceholderSecret;
}

/**
 * Get Clerk configuration status message
 * @returns object with configured status and message
 */
export function getClerkStatus(): { configured: boolean; message: string } {
  const configured = isClerkConfigured();

  if (configured) {
    return {
      configured: true,
      message: 'Clerk authentication is properly configured',
    };
  }

  return {
    configured: false,
    message: 'Clerk is using placeholder keys. Please configure real API keys in .env.local. See docs/CLERK-SETUP-GUIDE.md for instructions.',
  };
}
