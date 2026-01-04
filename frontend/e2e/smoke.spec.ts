/**
 * E2E Smoke Tests
 *
 * Quick sanity tests that verify:
 * 1. App loads without console errors
 * 2. Configuration initializes correctly
 * 3. API calls don't fail with network errors
 * 4. Basic navigation works
 *
 * These tests catch the issues we've been experiencing:
 * - "Configuration validation failed"
 * - "Failed to fetch"
 * - Route mismatches
 */

import { test, expect, type ConsoleMessage } from '@playwright/test';

const BACKEND_URL = process.env.BACKEND_URL || 'http://localhost:8000';

/**
 * Collect console errors during test
 */
function setupConsoleErrorCapture(page: any) {
  const errors: string[] = [];
  const warnings: string[] = [];

  page.on('console', (msg: ConsoleMessage) => {
    if (msg.type() === 'error') {
      errors.push(msg.text());
    }
    if (msg.type() === 'warning') {
      warnings.push(msg.text());
    }
  });

  return { errors, warnings };
}

test.describe('Smoke Tests - App Initialization', () => {
  test.beforeAll(async () => {
    // Verify backend is running before E2E tests
    try {
      const response = await fetch(`${BACKEND_URL}/health`);
      if (!response.ok) {
        throw new Error('Backend health check failed');
      }
    } catch (error) {
      console.error('\n');
      console.error('='.repeat(60));
      console.error('E2E TEST SETUP FAILED');
      console.error('='.repeat(60));
      console.error(`Backend not reachable at: ${BACKEND_URL}`);
      console.error('Start the backend:');
      console.error('  cd backend && uvicorn src.main:app --port 8000');
      console.error('='.repeat(60));
      console.error('\n');
      throw error;
    }
  });

  test('homepage loads without configuration errors', async ({ page }) => {
    const { errors } = setupConsoleErrorCapture(page);

    await page.goto('/');
    await page.waitForLoadState('networkidle');

    // Check for specific errors we've encountered
    const configErrors = errors.filter(e =>
      e.includes('Configuration validation failed') ||
      e.includes('Invalid environment configuration')
    );

    expect(configErrors).toHaveLength(0);
  });

  test('homepage shows successful config initialization', async ({ page }) => {
    const logs: string[] = [];

    page.on('console', (msg: ConsoleMessage) => {
      if (msg.type() === 'log') {
        logs.push(msg.text());
      }
    });

    await page.goto('/');
    await page.waitForLoadState('networkidle');

    // Should see config initialization success
    const configSuccess = logs.some(log =>
      log.includes('Configuration initialized successfully')
    );

    expect(configSuccess).toBe(true);
  });

  test('app does not have "Failed to fetch" errors on load', async ({ page }) => {
    const { errors } = setupConsoleErrorCapture(page);

    await page.goto('/');
    await page.waitForLoadState('networkidle');

    // Filter for network/fetch errors
    const fetchErrors = errors.filter(e =>
      e.includes('Failed to fetch') ||
      e.includes('NetworkError') ||
      e.includes('ECONNREFUSED')
    );

    expect(fetchErrors).toHaveLength(0);
  });
});

test.describe('Smoke Tests - Navigation', () => {
  test('can navigate to login page', async ({ page }) => {
    const { errors } = setupConsoleErrorCapture(page);

    await page.goto('/');
    await page.waitForLoadState('networkidle');

    // Look for login link and click it
    const loginLink = page.locator('a[href*="login"], a[href*="sign-in"]').first();
    if (await loginLink.isVisible()) {
      await loginLink.click();
      await page.waitForLoadState('networkidle');
    } else {
      // Direct navigation
      await page.goto('/login');
    }

    // Should not have critical errors
    const criticalErrors = errors.filter(e =>
      e.includes('Configuration validation failed') ||
      e.includes('Cannot read properties of undefined')
    );

    expect(criticalErrors).toHaveLength(0);
  });
});

test.describe('Smoke Tests - API Connectivity', () => {
  test('health endpoint is reachable from browser context', async ({ page }) => {
    // Make API call from browser context
    const healthResponse = await page.evaluate(async (backendUrl) => {
      const response = await fetch(`${backendUrl}/health`);
      return {
        status: response.status,
        ok: response.ok,
      };
    }, BACKEND_URL);

    expect(healthResponse.ok).toBe(true);
    expect(healthResponse.status).toBe(200);
  });

  test('reports endpoint returns 401 not 404 (route exists)', async ({ page }) => {
    const response = await page.evaluate(async (backendUrl) => {
      const resp = await fetch(`${backendUrl}/reports/`);
      return { status: resp.status };
    }, BACKEND_URL);

    // 401 means route exists but needs auth
    // 404 would mean route doesn't exist (which is the bug we're catching)
    expect(response.status).toBe(401);
  });
});

test.describe('Smoke Tests - Error States', () => {
  test('app handles missing auth gracefully (no crash)', async ({ page }) => {
    const { errors } = setupConsoleErrorCapture(page);

    // Try to access authenticated route
    await page.goto('/chat');
    await page.waitForLoadState('networkidle');

    // App should redirect to login or show auth required
    // Should NOT crash with uncaught errors
    const crashErrors = errors.filter(e =>
      e.includes('Uncaught') ||
      e.includes('Unhandled') ||
      e.includes('Cannot read properties of null')
    );

    expect(crashErrors).toHaveLength(0);
  });
});
