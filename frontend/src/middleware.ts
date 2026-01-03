/**
 * Next.js middleware for authentication and request tracking
 * Uses Clerk to protect routes (App Router)
 * Adds correlation IDs for request tracing
 *
 * IMPORTANT: This uses the latest Clerk App Router approach with clerkMiddleware()
 * See: https://clerk.com/docs/nextjs/getting-started/quickstart
 */

import { clerkMiddleware, createRouteMatcher } from '@clerk/nextjs/server';
import { NextResponse } from 'next/server';

// Define public routes (accessible without authentication)
const isPublicRoute = createRouteMatcher([
  '/',
  '/login(.*)',
  '/signup(.*)',
  '/api/webhooks(.*)',
  '/api/health(.*)',
]);

/**
 * Generate a correlation ID for request tracing
 */
function generateCorrelationId(): string {
  return `${Date.now()}-${Math.random().toString(36).substring(2, 15)}`;
}

export default clerkMiddleware(async (auth, request) => {
  // Generate correlation ID for this request
  const correlationId = request.headers.get('X-Correlation-ID') || generateCorrelationId();

  // Create response with correlation ID header
  let response: NextResponse | undefined;

  // Allow public routes without authentication
  if (isPublicRoute(request)) {
    response = NextResponse.next();
  } else {
    // Protect all other routes - redirect to sign-in if not authenticated
    await auth.protect();
    response = NextResponse.next();
  }

  // Add correlation ID to response headers
  if (response) {
    response.headers.set('X-Correlation-ID', correlationId);
  }

  return response;
});

export const config = {
  matcher: [
    // Skip Next.js internals and all static files, unless found in search params
    '/((?!_next|[^?]*\\.(?:html?|css|js(?!on)|jpe?g|webp|png|gif|svg|ttf|woff2?|ico|csv|docx?|xlsx?|zip|webmanifest)).*)',
    // Always run for API routes
    '/(api|trpc)(.*)',
  ],
};
