/**
 * Startup checks for development environment
 * Logs warnings for missing configuration
 */

import { getClerkStatus } from './clerk';

/**
 * Run startup checks and log warnings
 * Call this in server components or API routes
 */
export function runStartupChecks() {
  if (process.env.NODE_ENV === 'production') {
    return; // Skip checks in production
  }

  const clerkStatus = getClerkStatus();

  if (!clerkStatus.configured) {
    console.warn('\n========================================');
    console.warn('⚠️  CLERK CONFIGURATION WARNING');
    console.warn('========================================');
    console.warn(clerkStatus.message);
    console.warn('\nQuick setup (2 minutes):');
    console.warn('1. Create free account: https://clerk.com');
    console.warn('2. Get API keys: https://dashboard.clerk.com/last-active?path=api-keys');
    console.warn('3. Update: frontend/.env.local');
    console.warn('4. Restart dev server');
    console.warn('\nDetailed guide: docs/CLERK-SETUP-GUIDE.md');
    console.warn('========================================\n');
  }
}
