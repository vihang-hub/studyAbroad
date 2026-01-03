/**
 * Warning component for Clerk configuration
 * Displays a banner when Clerk is not properly configured
 */

'use client';

import { useEffect, useState } from 'react';

export function ClerkWarning() {
  const [isMounted, setIsMounted] = useState(false);
  const [configured, setConfigured] = useState(true);

  useEffect(() => {
    setIsMounted(true);
    // Only check client-accessible environment variables to avoid hydration mismatch
    const publishableKey = process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY || '';
    const hasValidKey = publishableKey
      && !publishableKey.includes('YOUR_')
      && !publishableKey.includes('your_')
      && publishableKey !== 'pk_test_your_clerk_publishable_key';

    setConfigured(hasValidKey);
  }, []);

  // Don't render anything until after hydration
  if (!isMounted || configured) {
    return null;
  }

  return (
    <div className="bg-yellow-50 border-l-4 border-yellow-400 p-4">
      <div className="flex">
        <div className="flex-shrink-0">
          <svg
            className="h-5 w-5 text-yellow-400"
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 20 20"
            fill="currentColor"
            aria-hidden="true"
          >
            <path
              fillRule="evenodd"
              d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z"
              clipRule="evenodd"
            />
          </svg>
        </div>
        <div className="ml-3">
          <p className="text-sm text-yellow-700">
            <strong>Development Mode:</strong>
            {' '}
            Clerk is using placeholder keys. Please configure real API keys in .env.local. See docs/CLERK-SETUP-GUIDE.md for instructions.
          </p>
        </div>
      </div>
    </div>
  );
}
