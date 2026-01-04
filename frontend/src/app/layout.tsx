/**
 * Root layout for Next.js app
 * Uses Clerk for authentication (App Router)
 *
 * IMPORTANT: This uses the latest Clerk App Router approach with ClerkProvider
 * See: https://clerk.com/docs/nextjs/getting-started/quickstart
 */

import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import Link from 'next/link';
import {
  ClerkProvider,
  SignedIn,
  SignedOut,
  UserButton,
} from '@clerk/nextjs';
import { ClerkWarning } from '@/components/ClerkWarning';
import { FeatureFlagProvider } from '@/providers/feature-flag-provider';
import { EnvironmentBadge } from '@/components/dev/environment-badge';
import { runStartupChecks } from '@/lib/startup-checks';
import { initializeConfig, validateEnvironment } from '@/lib/config';
import { initializeLogger } from '@/lib/logger';
import './globals.css';

const inter = Inter({ subsets: ['latin'] });

// Initialize configuration and logging
// This runs on the server during build/request time
try {
  initializeConfig();
  initializeLogger();
  validateEnvironment();
  runStartupChecks();
} catch (error) {
  console.error('[Layout] Initialization failed:', error);
  // Re-throw to prevent app from running with invalid config
  throw error;
}

export const metadata: Metadata = {
  title: 'UK Study & Migration Research',
  description: 'AI-powered research reports for students studying in the UK',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <ClerkProvider>
      <html lang="en">
        <body className={inter.className}>
          <FeatureFlagProvider>
            <EnvironmentBadge />
            <header className="border-b border-gray-200 bg-white">
              <div className="container mx-auto flex items-center justify-between px-4 py-3">
                <div className="text-xl font-bold text-gray-900">
                  UK Study & Migration
                </div>
                <div className="flex items-center gap-4">
                  <SignedOut>
                    {/* Use path-based navigation instead of modal to avoid third-party cookie issues in Chrome */}
                    <Link
                      href="/login"
                      className="rounded-lg bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700"
                    >
                      Sign In
                    </Link>
                    <Link
                      href="/signup"
                      className="rounded-lg border border-gray-300 px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50"
                    >
                      Sign Up
                    </Link>
                  </SignedOut>
                  <SignedIn>
                    <UserButton afterSignOutUrl="/" />
                  </SignedIn>
                </div>
              </div>
            </header>
            <ClerkWarning />
            {children}
          </FeatureFlagProvider>
        </body>
      </html>
    </ClerkProvider>
  );
}
