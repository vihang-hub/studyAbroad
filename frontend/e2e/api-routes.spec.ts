/**
 * E2E API Route Tests
 *
 * These tests specifically catch frontend/backend route mismatches.
 * They intercept network requests and verify the frontend is calling
 * the correct backend endpoints.
 */

import { test, expect } from '@playwright/test';

const BACKEND_URL = process.env.BACKEND_URL || 'http://localhost:8000';

test.describe('API Route Verification', () => {
  test('reports API calls use correct path (no /api prefix)', async ({ page }) => {
    const apiCalls: string[] = [];

    // Intercept all API calls
    await page.route(`${BACKEND_URL}/**`, route => {
      apiCalls.push(route.request().url());
      route.continue();
    });

    // Navigate to a page that fetches reports
    await page.goto('/chat');
    await page.waitForLoadState('networkidle');

    // Wait a bit for any lazy API calls
    await page.waitForTimeout(2000);

    // Check for incorrect /api/ prefix usage
    const incorrectPaths = apiCalls.filter(url =>
      url.includes('/api/reports') ||
      url.includes('/api/health')
    );

    if (incorrectPaths.length > 0) {
      console.error('Found incorrect API paths:');
      incorrectPaths.forEach(p => console.error(`  - ${p}`));
      console.error('Frontend is using /api/ prefix but backend routes do not have this prefix');
    }

    expect(incorrectPaths).toHaveLength(0);
  });

  test('verify all API endpoints frontend calls actually exist', async ({ page }) => {
    const failedRequests: { url: string; status: number }[] = [];

    // Monitor for 404 responses
    page.on('response', response => {
      const url = response.url();
      if (url.includes(BACKEND_URL) && response.status() === 404) {
        failedRequests.push({ url, status: 404 });
      }
    });

    // Navigate through the app
    await page.goto('/');
    await page.waitForLoadState('networkidle');

    await page.goto('/chat');
    await page.waitForLoadState('networkidle');
    await page.waitForTimeout(2000);

    // No API calls should return 404
    if (failedRequests.length > 0) {
      console.error('Found 404 responses (route mismatches):');
      failedRequests.forEach(r => console.error(`  - ${r.url}`));
    }

    expect(failedRequests).toHaveLength(0);
  });

  test('reports list endpoint path is correct', async ({ page }) => {
    let reportsCallMade = false;
    let reportsCallUrl = '';

    await page.route(`${BACKEND_URL}/**`, route => {
      const url = route.request().url();
      if (url.includes('reports')) {
        reportsCallMade = true;
        reportsCallUrl = url;
      }
      route.continue();
    });

    // Navigate to page that loads reports
    await page.goto('/chat');
    await page.waitForLoadState('networkidle');
    await page.waitForTimeout(2000);

    if (reportsCallMade) {
      // Verify correct path format
      expect(reportsCallUrl).not.toContain('/api/reports');
      expect(reportsCallUrl).toMatch(/\/reports\/?\?/);
    }
  });
});

test.describe('Backend Route Documentation', () => {
  test('OpenAPI spec is accessible', async ({ page }) => {
    const response = await page.request.get(`${BACKEND_URL}/openapi.json`);
    expect(response.ok()).toBe(true);

    const spec = await response.json();
    expect(spec.paths).toBeDefined();
  });

  test('all expected routes exist in OpenAPI spec', async ({ page }) => {
    const response = await page.request.get(`${BACKEND_URL}/openapi.json`);
    const spec = await response.json();

    const expectedRoutes = [
      '/reports/',
      '/reports/initiate',
      '/reports/{report_id}',
      '/health',
      '/stream/reports/{report_id}',
    ];

    const actualRoutes = Object.keys(spec.paths);

    expectedRoutes.forEach(route => {
      expect(actualRoutes).toContain(route);
    });
  });
});
