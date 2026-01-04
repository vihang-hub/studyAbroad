/**
 * API Contract Tests
 *
 * Verifies that all API routes the frontend expects exist in the backend.
 * These tests require a running backend server.
 *
 * Run with: npm run test:contracts
 */

import { describe, it, expect, beforeAll } from 'vitest';

const BACKEND_URL = process.env.BACKEND_URL || 'http://localhost:8000';
const OPENAPI_URL = `${BACKEND_URL}/openapi.json`;

/**
 * All API routes that the frontend expects to exist.
 * If you add a new API call in the frontend, add the route here.
 */
const FRONTEND_EXPECTED_ROUTES = [
  // Reports
  { path: '/reports/', methods: ['GET'] },
  { path: '/reports/initiate', methods: ['POST'] },
  { path: '/reports/{report_id}', methods: ['GET'] },

  // Streaming
  { path: '/stream/reports/{report_id}', methods: ['GET'] },

  // Health
  { path: '/health', methods: ['GET'] },

  // Webhooks
  { path: '/webhooks/stripe', methods: ['POST'] },
];

describe('API Contract Tests', () => {
  let openApiSpec: {
    paths: Record<string, Record<string, unknown>>;
    info: { title: string; version: string };
  };

  beforeAll(async () => {
    // Fetch OpenAPI spec from backend
    try {
      const response = await fetch(OPENAPI_URL);
      if (!response.ok) {
        throw new Error(`Failed to fetch OpenAPI spec: ${response.status}`);
      }
      openApiSpec = await response.json();
    } catch (error) {
      console.error('\n');
      console.error('='.repeat(60));
      console.error('CONTRACT TEST SETUP FAILED');
      console.error('='.repeat(60));
      console.error(`Could not connect to backend at: ${BACKEND_URL}`);
      console.error('Make sure the backend is running:');
      console.error('  cd backend && uvicorn src.main:app --port 8000');
      console.error('='.repeat(60));
      console.error('\n');
      throw error;
    }
  });

  it('backend is reachable and returns valid OpenAPI spec', () => {
    expect(openApiSpec).toBeDefined();
    expect(openApiSpec.paths).toBeDefined();
    expect(openApiSpec.info).toBeDefined();
  });

  describe('Route Existence', () => {
    FRONTEND_EXPECTED_ROUTES.forEach(({ path, methods }) => {
      it(`backend has route: ${methods.join(', ')} ${path}`, () => {
        const backendPaths = Object.keys(openApiSpec.paths);

        // Check if path exists
        expect(backendPaths).toContain(path);

        // Check if methods exist for that path
        const pathSpec = openApiSpec.paths[path];
        methods.forEach(method => {
          expect(pathSpec).toHaveProperty(method.toLowerCase());
        });
      });
    });
  });

  describe('No Unexpected Route Prefixes', () => {
    it('frontend does not use /api prefix (backend routes have no /api prefix)', () => {
      const backendPaths = Object.keys(openApiSpec.paths);

      // Verify no backend routes start with /api
      const apiPrefixedRoutes = backendPaths.filter(p => p.startsWith('/api/'));
      expect(apiPrefixedRoutes).toHaveLength(0);

      // Verify frontend expected routes don't have /api prefix either
      const frontendApiPrefixed = FRONTEND_EXPECTED_ROUTES.filter(r =>
        r.path.startsWith('/api/')
      );
      expect(frontendApiPrefixed).toHaveLength(0);
    });
  });

  describe('Response Schema Validation', () => {
    it('/health endpoint returns expected schema', async () => {
      const response = await fetch(`${BACKEND_URL}/health`);
      expect(response.ok).toBe(true);

      const data = await response.json();
      expect(data).toHaveProperty('status');
      expect(data).toHaveProperty('timestamp');
      expect(data).toHaveProperty('version');
    });

    it('/reports/ endpoint returns 401 without auth (not 404)', async () => {
      const response = await fetch(`${BACKEND_URL}/reports/`);

      // Should be 401 (unauthorized) not 404 (not found)
      // This catches route mismatch issues
      expect(response.status).toBe(401);
    });

    it('/reports/initiate endpoint accepts POST (returns 401 without auth)', async () => {
      const response = await fetch(`${BACKEND_URL}/reports/initiate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: 'test' }),
      });

      // Should be 401 or 422 (validation), not 404
      expect([401, 422]).toContain(response.status);
    });
  });
});

/**
 * Export routes for use in other tests
 */
export { FRONTEND_EXPECTED_ROUTES, BACKEND_URL };
