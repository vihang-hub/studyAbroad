/**
 * Tests for Next.js middleware
 * Tests authentication and correlation ID handling
 */

import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';

// Track headers set on response
let responseHeaders: Map<string, string>;

// Mock Next.js NextResponse
vi.mock('next/server', () => ({
  NextResponse: {
    next: vi.fn(() => {
      responseHeaders = new Map();
      return {
        headers: {
          set: (key: string, value: string) => responseHeaders.set(key, value),
          get: (key: string) => responseHeaders.get(key),
        },
      };
    }),
  },
}));

// Mock Clerk middleware
const mockAuth = {
  protect: vi.fn(),
};

// Store the handler passed to clerkMiddleware for testing
let capturedHandler: ((auth: typeof mockAuth, request: Request) => Promise<Response>) | null = null;

const mockClerkMiddleware = vi.fn((handler: (auth: typeof mockAuth, request: Request) => Promise<Response>) => {
  capturedHandler = handler;
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
    vi.resetModules();
    vi.clearAllMocks();
    responseHeaders = new Map();
    capturedHandler = null;
  });

  afterEach(() => {
    vi.clearAllMocks();
  });

  describe('correlation ID generation', () => {
    it('should generate correlation ID when not provided in request', async () => {
      // Import the middleware to trigger registration
      await import('../src/middleware');

      // Get the handler that was passed to clerkMiddleware
      expect(capturedHandler).not.toBeNull();

      const request = new Request('https://example.com/', {
        headers: new Headers(),
      });

      // Execute the middleware handler
      await capturedHandler!(mockAuth, request);

      // Verify a correlation ID was set
      expect(responseHeaders.has('X-Correlation-ID')).toBe(true);
      const correlationId = responseHeaders.get('X-Correlation-ID');
      expect(correlationId).toBeTruthy();
      expect(correlationId!.length).toBeGreaterThan(10);
    });

    it('should use existing correlation ID from request headers', async () => {
      await import('../src/middleware');

      const existingCorrelationId = 'existing-correlation-123';
      const request = new Request('https://example.com/', {
        headers: new Headers({
          'X-Correlation-ID': existingCorrelationId,
        }),
      });

      await capturedHandler!(mockAuth, request);

      expect(responseHeaders.get('X-Correlation-ID')).toBe(existingCorrelationId);
    });

    it('should generate unique correlation IDs for different requests', async () => {
      await import('../src/middleware');

      const request1 = new Request('https://example.com/page1');
      await capturedHandler!(mockAuth, request1);
      const id1 = responseHeaders.get('X-Correlation-ID');

      const request2 = new Request('https://example.com/page2');
      await capturedHandler!(mockAuth, request2);
      const id2 = responseHeaders.get('X-Correlation-ID');

      // IDs should be different (with very high probability)
      expect(id1).not.toBe(id2);
    });
  });

  describe('route protection', () => {
    it('should not call auth.protect for public routes', async () => {
      await import('../src/middleware');

      // Test public route - home page
      const homeRequest = new Request('https://example.com/');
      await capturedHandler!(mockAuth, homeRequest);
      expect(mockAuth.protect).not.toHaveBeenCalled();
    });

    it('should not call auth.protect for login route', async () => {
      vi.resetModules();
      mockAuth.protect.mockClear();

      await import('../src/middleware');

      const loginRequest = new Request('https://example.com/login');
      await capturedHandler!(mockAuth, loginRequest);
      expect(mockAuth.protect).not.toHaveBeenCalled();
    });

    it('should not call auth.protect for signup route', async () => {
      vi.resetModules();
      mockAuth.protect.mockClear();

      await import('../src/middleware');

      const signupRequest = new Request('https://example.com/signup');
      await capturedHandler!(mockAuth, signupRequest);
      expect(mockAuth.protect).not.toHaveBeenCalled();
    });

    it('should not call auth.protect for webhook routes', async () => {
      vi.resetModules();
      mockAuth.protect.mockClear();

      await import('../src/middleware');

      const webhookRequest = new Request('https://example.com/api/webhooks/clerk');
      await capturedHandler!(mockAuth, webhookRequest);
      expect(mockAuth.protect).not.toHaveBeenCalled();
    });

    it('should not call auth.protect for health check routes', async () => {
      vi.resetModules();
      mockAuth.protect.mockClear();

      await import('../src/middleware');

      const healthRequest = new Request('https://example.com/api/health');
      await capturedHandler!(mockAuth, healthRequest);
      expect(mockAuth.protect).not.toHaveBeenCalled();
    });

    it('should call auth.protect for protected routes like dashboard', async () => {
      vi.resetModules();
      mockAuth.protect.mockClear();

      await import('../src/middleware');

      const dashboardRequest = new Request('https://example.com/dashboard');
      await capturedHandler!(mockAuth, dashboardRequest);
      expect(mockAuth.protect).toHaveBeenCalled();
    });

    it('should call auth.protect for chat route', async () => {
      vi.resetModules();
      mockAuth.protect.mockClear();

      await import('../src/middleware');

      const chatRequest = new Request('https://example.com/chat');
      await capturedHandler!(mockAuth, chatRequest);
      expect(mockAuth.protect).toHaveBeenCalled();
    });

    it('should call auth.protect for reports route', async () => {
      vi.resetModules();
      mockAuth.protect.mockClear();

      await import('../src/middleware');

      const reportsRequest = new Request('https://example.com/reports');
      await capturedHandler!(mockAuth, reportsRequest);
      expect(mockAuth.protect).toHaveBeenCalled();
    });

    it('should call auth.protect for API user routes', async () => {
      vi.resetModules();
      mockAuth.protect.mockClear();

      await import('../src/middleware');

      const apiRequest = new Request('https://example.com/api/users');
      await capturedHandler!(mockAuth, apiRequest);
      expect(mockAuth.protect).toHaveBeenCalled();
    });
  });

  describe('route matching', () => {
    it('should create route matcher for public routes', async () => {
      vi.resetModules();
      mockCreateRouteMatcher.mockClear();

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

      expect(config.matcher[0]).toContain('_next');
      expect(config.matcher[0]).toContain('html');
      expect(config.matcher[0]).toContain('css');
      expect(config.matcher[0]).toContain('js');
      expect(config.matcher[0]).toContain('png');
      expect(config.matcher[0]).toContain('ico');
    });

    it('should have matcher for API routes', async () => {
      const { config } = await import('../src/middleware');

      expect(config.matcher[1]).toContain('api');
      expect(config.matcher[1]).toContain('trpc');
    });

    it('should exclude webp images', async () => {
      const { config } = await import('../src/middleware');
      expect(config.matcher[0]).toContain('webp');
    });

    it('should exclude font files', async () => {
      const { config } = await import('../src/middleware');
      expect(config.matcher[0]).toContain('ttf');
      expect(config.matcher[0]).toContain('woff');
    });

    it('should exclude document files', async () => {
      const { config } = await import('../src/middleware');
      expect(config.matcher[0]).toContain('docx');
      expect(config.matcher[0]).toContain('xlsx');
      expect(config.matcher[0]).toContain('csv');
    });
  });

  describe('clerkMiddleware integration', () => {
    it('should use clerkMiddleware function', () => {
      expect(mockClerkMiddleware).toBeDefined();
      expect(typeof mockClerkMiddleware).toBe('function');
    });

    it('should have correct clerkMiddleware signature', () => {
      const testHandler = vi.fn();
      const wrappedMiddleware = mockClerkMiddleware(testHandler);

      expect(typeof wrappedMiddleware).toBe('function');
    });

    it('should pass handler to clerkMiddleware', async () => {
      vi.resetModules();
      mockClerkMiddleware.mockClear();

      await import('../src/middleware');

      expect(mockClerkMiddleware).toHaveBeenCalledWith(expect.any(Function));
    });
  });

  describe('response handling', () => {
    it('should return NextResponse.next() for public routes', async () => {
      const { NextResponse } = await import('next/server');
      await import('../src/middleware');

      const request = new Request('https://example.com/');
      await capturedHandler!(mockAuth, request);

      expect(NextResponse.next).toHaveBeenCalled();
    });

    it('should return NextResponse.next() for protected routes after auth', async () => {
      const { NextResponse } = await import('next/server');
      vi.resetModules();

      await import('../src/middleware');

      const request = new Request('https://example.com/dashboard');
      await capturedHandler!(mockAuth, request);

      expect(NextResponse.next).toHaveBeenCalled();
    });
  });
});
