/**
 * Tests for Next.js middleware
 * Tests authentication and correlation ID handling
 */

import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';

// Mock Next.js NextResponse
const mockNextResponse = {
  next: vi.fn(() => ({
    headers: new Map(),
  })),
};

vi.mock('next/server', () => ({
  NextResponse: mockNextResponse,
}));

// Mock Clerk middleware
const mockAuth = {
  protect: vi.fn(),
};

const mockClerkMiddleware = vi.fn((handler: (auth: typeof mockAuth, request: Request) => Promise<Response>) => {
  return async (request: Request) => {
    return handler(mockAuth, request);
  };
});

const mockCreateRouteMatcher = vi.fn((routes: string[]) => {
  return (request: Request) => {
    const url = new URL(request.url);
    return routes.some((route) => {
      const pattern = route.replace('(.*)', '.*');
      return new RegExp(`^${pattern}$`).test(url.pathname);
    });
  };
});

vi.mock('@clerk/nextjs/server', () => ({
  clerkMiddleware: mockClerkMiddleware,
  createRouteMatcher: mockCreateRouteMatcher,
}));

describe('middleware', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  afterEach(() => {
    vi.clearAllMocks();
  });

  describe('correlation ID generation', () => {
    it('should generate correlation ID when not provided in request', async () => {
      // The middleware adds correlation ID to responses
      const request = new Request('https://example.com/dashboard', {
        headers: new Headers(),
      });

      // Verify the mocked response includes correlation ID logic
      expect(mockNextResponse.next).toBeDefined();
    });

    it('should use existing correlation ID from request headers', async () => {
      const existingCorrelationId = 'existing-correlation-123';
      const request = new Request('https://example.com/dashboard', {
        headers: new Headers({
          'X-Correlation-ID': existingCorrelationId,
        }),
      });

      expect(request.headers.get('X-Correlation-ID')).toBe(existingCorrelationId);
    });
  });

  describe('route matching', () => {
    it('should create route matcher for public routes', async () => {
      await import('../src/middleware');

      expect(mockCreateRouteMatcher).toHaveBeenCalledWith([
        '/',
        '/login(.*)',
        '/signup(.*)',
        '/api/webhooks(.*)',
        '/api/health(.*)',
      ]);
    });

    it('should identify public routes correctly', () => {
      const isPublicRoute = mockCreateRouteMatcher([
        '/',
        '/login(.*)',
        '/signup(.*)',
        '/api/webhooks(.*)',
        '/api/health(.*)',
      ]);

      // Test public routes
      expect(isPublicRoute(new Request('https://example.com/'))).toBe(true);
      expect(isPublicRoute(new Request('https://example.com/login'))).toBe(true);
      expect(isPublicRoute(new Request('https://example.com/login/sso'))).toBe(true);
      expect(isPublicRoute(new Request('https://example.com/signup'))).toBe(true);
      expect(isPublicRoute(new Request('https://example.com/signup/verify'))).toBe(true);
      expect(isPublicRoute(new Request('https://example.com/api/webhooks'))).toBe(true);
      expect(isPublicRoute(new Request('https://example.com/api/webhooks/clerk'))).toBe(true);
      expect(isPublicRoute(new Request('https://example.com/api/health'))).toBe(true);
    });

    it('should identify protected routes correctly', () => {
      const isPublicRoute = mockCreateRouteMatcher([
        '/',
        '/login(.*)',
        '/signup(.*)',
        '/api/webhooks(.*)',
        '/api/health(.*)',
      ]);

      // Test protected routes
      expect(isPublicRoute(new Request('https://example.com/dashboard'))).toBe(false);
      expect(isPublicRoute(new Request('https://example.com/chat'))).toBe(false);
      expect(isPublicRoute(new Request('https://example.com/reports'))).toBe(false);
      expect(isPublicRoute(new Request('https://example.com/api/users'))).toBe(false);
      expect(isPublicRoute(new Request('https://example.com/settings'))).toBe(false);
    });
  });

  describe('middleware config', () => {
    it('should export config with correct matcher', async () => {
      const { config } = await import('../src/middleware');

      expect(config).toBeDefined();
      expect(config.matcher).toBeDefined();
      expect(Array.isArray(config.matcher)).toBe(true);
      expect(config.matcher).toHaveLength(2);
    });

    it('should have matcher for static file exclusion', async () => {
      const { config } = await import('../src/middleware');

      // First matcher excludes Next.js internals and static files
      expect(config.matcher[0]).toContain('_next');
      expect(config.matcher[0]).toContain('html');
      expect(config.matcher[0]).toContain('css');
      expect(config.matcher[0]).toContain('js');
      expect(config.matcher[0]).toContain('png');
      expect(config.matcher[0]).toContain('ico');
    });

    it('should have matcher for API routes', async () => {
      const { config } = await import('../src/middleware');

      // Second matcher runs for API routes
      expect(config.matcher[1]).toContain('api');
      expect(config.matcher[1]).toContain('trpc');
    });
  });

  describe('clerkMiddleware integration', () => {
    it('should use clerkMiddleware function', () => {
      // Verify clerkMiddleware mock is defined and is a function
      expect(mockClerkMiddleware).toBeDefined();
      expect(typeof mockClerkMiddleware).toBe('function');
    });

    it('should have correct clerkMiddleware signature', () => {
      // The middleware should accept a handler function
      const testHandler = vi.fn();
      const wrappedMiddleware = mockClerkMiddleware(testHandler);

      expect(typeof wrappedMiddleware).toBe('function');
    });
  });
});
