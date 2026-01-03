# Testing Strategy

**Version**: 1.0.0
**Created**: 2025-12-31
**Status**: Design Approved

## Overview

Comprehensive testing strategy for the MVP UK Study & Migration Research App, designed to achieve ≥90% code coverage and >80% mutation testing score.

---

## Test Pyramid

```
                    ┌─────────────┐
                    │   E2E (5%)  │ ← Critical user flows
                    │             │
                    └─────────────┘
                  ┌─────────────────┐
                  │ Integration (15%)│ ← API + DB + External services
                  │                 │
                  └─────────────────┘
              ┌─────────────────────────┐
              │    Unit Tests (80%)     │ ← Business logic, repositories, utilities
              │                         │
              └─────────────────────────┘
```

---

## Testing Tools

### Frontend (Next.js + TypeScript)
- **Unit/Integration**: Vitest + React Testing Library
- **E2E**: Playwright
- **Mutation Testing**: Stryker
- **Coverage**: c8 (built into Vitest)
- **Component Testing**: Storybook

### Backend (FastAPI + Python)
- **Unit/Integration**: pytest + pytest-asyncio
- **E2E**: pytest + httpx
- **Mutation Testing**: mutpy or cosmic-ray
- **Coverage**: pytest-cov
- **API Testing**: httpx.AsyncClient

### Shared Packages (TypeScript)
- **Unit**: Vitest
- **Integration**: Vitest with test databases
- **Mutation**: Stryker

---

## Test Coverage Goals

| Layer | Coverage Target | Mutation Score | Notes |
|-------|----------------|----------------|-------|
| Business Logic | ≥95% | >85% | Core report generation, payment flows |
| API Routes | ≥90% | >80% | All endpoints tested |
| Repositories | ≥95% | >85% | Database operations critical |
| Shared Packages | ≥90% | >80% | Config, feature flags, logging, database |
| UI Components | ≥85% | >75% | Focus on logic, less on visual |
| E2E Flows | 100% of critical paths | N/A | Auth, payment, report generation |

---

## Unit Tests (80% of Tests)

### What to Test
- Business logic functions
- Repository methods
- Validation logic
- Utility functions
- Pure functions (no side effects)

### Frontend Unit Test Example

```typescript
// frontend/tests/unit/validation.test.ts
import { describe, it, expect } from 'vitest';
import { validateSubject } from '@/lib/validation';

describe('validateSubject', () => {
  it('should accept valid subjects', () => {
    expect(validateSubject('Computer Science')).toBe(true);
    expect(validateSubject('Nursing')).toBe(true);
  });

  it('should reject empty subjects', () => {
    expect(validateSubject('')).toBe(false);
    expect(validateSubject('   ')).toBe(false);
  });

  it('should reject subjects longer than 255 characters', () => {
    const longSubject = 'a'.repeat(256);
    expect(validateSubject(longSubject)).toBe(false);
  });

  it('should trim whitespace', () => {
    expect(validateSubject('  Computer Science  ')).toBe(true);
  });
});
```

### Backend Unit Test Example

```python
# backend/tests/unit/test_validation.py
import pytest
from models.schemas import CreateReportRequest
from pydantic import ValidationError

def test_create_report_request_valid():
    """Test valid report creation request"""
    request = CreateReportRequest(subject="Computer Science", country="UK")
    assert request.subject == "Computer Science"
    assert request.country == "UK"

def test_create_report_request_empty_subject():
    """Test empty subject validation"""
    with pytest.raises(ValidationError) as exc_info:
        CreateReportRequest(subject="", country="UK")
    assert "subject" in str(exc_info.value)

def test_create_report_request_subject_too_long():
    """Test subject length validation"""
    long_subject = "a" * 256
    with pytest.raises(ValidationError) as exc_info:
        CreateReportRequest(subject=long_subject, country="UK")
    assert "max_length" in str(exc_info.value)

def test_create_report_request_invalid_country():
    """Test country validation (MVP: UK only)"""
    with pytest.raises(ValidationError) as exc_info:
        CreateReportRequest(subject="Computer Science", country="US")
    assert "country" in str(exc_info.value)
```

### Shared Package Unit Test Example

```typescript
// shared/database/tests/repositories/report.test.ts
import { describe, it, expect, beforeEach, afterEach } from 'vitest';
import { ReportRepository } from '../../src/repositories/report';
import { MockDatabaseAdapter } from '../mocks/database-adapter';

describe('ReportRepository', () => {
  let repo: ReportRepository;
  let mockDb: MockDatabaseAdapter;

  beforeEach(() => {
    mockDb = new MockDatabaseAdapter();
    repo = new ReportRepository(mockDb);
  });

  afterEach(async () => {
    await mockDb.close();
  });

  it('should create a report', async () => {
    const report = await repo.create({
      userId: 'user-123',
      subject: 'Computer Science',
      country: 'UK',
      content: {},
      citations: [],
      status: 'generating',
      expiresAt: new Date(Date.now() + 30 * 24 * 60 * 60 * 1000),
    });

    expect(report.reportId).toBeDefined();
    expect(report.subject).toBe('Computer Science');
  });

  it('should soft delete a report', async () => {
    const report = await repo.create({ /* ... */ });
    await repo.softDelete(report.reportId, 'user-123');

    const found = await repo.findById(report.reportId, 'user-123');
    expect(found).toBeNull(); // Soft-deleted reports not returned
  });

  it('should restore a soft-deleted report', async () => {
    const report = await repo.create({ /* ... */ });
    await repo.softDelete(report.reportId, 'user-123');
    await repo.restore(report.reportId, 'user-123');

    const found = await repo.findById(report.reportId, 'user-123');
    expect(found).not.toBeNull();
  });
});
```

---

## Integration Tests (15% of Tests)

### What to Test
- API endpoints with database
- Repository with real database
- External API integrations (Gemini, Stripe)
- Feature flag behavior
- Environment mode switching

### Backend Integration Test Example

```python
# backend/tests/integration/test_reports_api.py
import pytest
from httpx import AsyncClient
from main import app
from database import db

@pytest.fixture
async def client():
    """Create test client"""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

@pytest.fixture
async def authenticated_headers(client):
    """Create authenticated headers with Clerk JWT"""
    # Create test user and get JWT
    token = await create_test_user_jwt()
    return {"Authorization": f"Bearer {token}"}

@pytest.mark.asyncio
async def test_create_report_success(client, authenticated_headers):
    """Test successful report creation"""
    response = await client.post(
        "/api/reports",
        json={"subject": "Computer Science", "country": "UK"},
        headers=authenticated_headers
    )

    assert response.status_code == 201
    data = response.json()
    assert "reportId" in data
    assert data["status"] == "generating"

@pytest.mark.asyncio
async def test_create_report_unauthorized(client):
    """Test report creation without authentication"""
    response = await client.post(
        "/api/reports",
        json={"subject": "Computer Science", "country": "UK"}
    )

    assert response.status_code == 401
    data = response.json()
    assert data["error"]["code"] == "UNAUTHORIZED"

@pytest.mark.asyncio
async def test_get_report_success(client, authenticated_headers):
    """Test retrieving a report"""
    # Create report first
    create_response = await client.post(
        "/api/reports",
        json={"subject": "Computer Science", "country": "UK"},
        headers=authenticated_headers
    )
    report_id = create_response.json()["reportId"]

    # Retrieve report
    response = await client.get(
        f"/api/reports/{report_id}",
        headers=authenticated_headers
    )

    assert response.status_code == 200
    data = response.json()
    assert data["reportId"] == report_id
    assert data["subject"] == "Computer Science"

@pytest.mark.asyncio
async def test_soft_delete_report(client, authenticated_headers):
    """Test soft deleting a report"""
    # Create report
    create_response = await client.post(
        "/api/reports",
        json={"subject": "Computer Science", "country": "UK"},
        headers=authenticated_headers
    )
    report_id = create_response.json()["reportId"]

    # Soft delete
    delete_response = await client.delete(
        f"/api/reports/{report_id}",
        headers=authenticated_headers
    )
    assert delete_response.status_code == 204

    # Verify not accessible
    get_response = await client.get(
        f"/api/reports/{report_id}",
        headers=authenticated_headers
    )
    assert get_response.status_code == 404
```

### Frontend Integration Test Example

```typescript
// frontend/tests/integration/report-creation.test.ts
import { describe, it, expect, beforeEach } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { ReportCreationPage } from '@/app/chat/page';
import { mockApiClient } from '../mocks/api-client';

describe('Report Creation Flow', () => {
  beforeEach(() => {
    mockApiClient.reset();
  });

  it('should create a report with payment (production mode)', async () => {
    mockApiClient.setEnvironmentMode('production');
    mockApiClient.setFeatureFlag('ENABLE_PAYMENTS', true);

    const user = userEvent.setup();
    render(<ReportCreationPage />);

    // Enter subject
    const subjectInput = screen.getByLabelText(/subject/i);
    await user.type(subjectInput, 'Computer Science');

    // Submit
    const submitButton = screen.getByRole('button', { name: /generate report/i });
    await user.click(submitButton);

    // Payment modal should appear
    await waitFor(() => {
      expect(screen.getByText(/payment required/i)).toBeInTheDocument();
    });

    // Enter payment details
    const cardInput = screen.getByLabelText(/card number/i);
    await user.type(cardInput, '4242424242424242');

    // Submit payment
    const payButton = screen.getByRole('button', { name: /pay £2.99/i });
    await user.click(payButton);

    // Report generation should start
    await waitFor(() => {
      expect(screen.getByText(/generating report/i)).toBeInTheDocument();
    });
  });

  it('should bypass payment in dev mode', async () => {
    mockApiClient.setEnvironmentMode('dev');
    mockApiClient.setFeatureFlag('ENABLE_PAYMENTS', false);

    const user = userEvent.setup();
    render(<ReportCreationPage />);

    // Enter subject
    const subjectInput = screen.getByLabelText(/subject/i);
    await user.type(subjectInput, 'Computer Science');

    // Submit
    const submitButton = screen.getByRole('button', { name: /generate report/i });
    await user.click(submitButton);

    // Should go directly to generation (no payment)
    await waitFor(() => {
      expect(screen.getByText(/generating report/i)).toBeInTheDocument();
    });

    // Payment modal should NOT appear
    expect(screen.queryByText(/payment required/i)).not.toBeInTheDocument();
  });
});
```

---

## End-to-End Tests (5% of Tests)

### Critical User Flows to Test

1. **Authentication Flow**
   - Sign up with email → Verify email → Redirect to /chat
   - Sign in with Google → Redirect to /chat
   - Session expiration → Redirect to /sign-in

2. **Report Generation Flow**
   - User enters subject → Payment (prod) → AI generation → Report saved → Report accessible

3. **Report Access Flow**
   - View report list → Click report → View full content → Verify citations

4. **Soft Delete Flow**
   - Create report → Wait 30 days (simulate) → Verify soft deleted → Cannot access

### E2E Test Example (Playwright)

```typescript
// frontend/tests/e2e/report-generation.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Report Generation E2E', () => {
  test.beforeEach(async ({ page }) => {
    // Sign in
    await page.goto('/sign-in');
    await page.fill('[name="email"]', 'test@example.com');
    await page.fill('[name="password"]', 'password123');
    await page.click('button[type="submit"]');
    await page.waitForURL('/chat');
  });

  test('should generate a report in production mode', async ({ page }) => {
    // Set environment to production (via test config)
    process.env.ENVIRONMENT_MODE = 'production';

    // Enter subject
    await page.fill('[name="subject"]', 'Computer Science');
    await page.click('button:has-text("Generate Report")');

    // Payment modal should appear
    await expect(page.locator('text=Payment Required')).toBeVisible();

    // Enter test card details (Stripe test mode)
    await page.fill('[name="cardNumber"]', '4242424242424242');
    await page.fill('[name="expiry"]', '12/25');
    await page.fill('[name="cvc"]', '123');
    await page.click('button:has-text("Pay £2.99")');

    // Wait for payment success
    await expect(page.locator('text=Payment Successful')).toBeVisible();

    // Report generation should start
    await expect(page.locator('text=Generating Report')).toBeVisible();

    // Wait for streaming to complete (max 60s)
    await expect(page.locator('text=Report Complete')).toBeVisible({
      timeout: 60000,
    });

    // Verify sections are rendered
    await expect(page.locator('text=Executive Summary')).toBeVisible();
    await expect(page.locator('text=Study Options')).toBeVisible();
    await expect(page.locator('text=Citations')).toBeVisible();
  });

  test('should bypass payment in dev mode', async ({ page }) => {
    // Set environment to dev (via test config)
    process.env.ENVIRONMENT_MODE = 'dev';

    // Enter subject
    await page.fill('[name="subject"]', 'Computer Science');
    await page.click('button:has-text("Generate Report")');

    // Payment modal should NOT appear
    await expect(page.locator('text=Payment Required')).not.toBeVisible();

    // Report generation should start immediately
    await expect(page.locator('text=Generating Report')).toBeVisible();
  });
});
```

---

## Mutation Testing

### What is Mutation Testing?

Mutation testing verifies the quality of tests by introducing small changes (mutations) to code and checking if tests catch them.

### Configuration

```typescript
// frontend/stryker.config.mjs
export default {
  mutate: [
    'src/**/*.ts',
    'src/**/*.tsx',
    '!src/**/*.test.ts',
    '!src/**/*.spec.ts',
  ],
  mutator: {
    plugins: ['@stryker-mutator/typescript-checker'],
  },
  testRunner: 'vitest',
  thresholds: {
    high: 85,
    low: 80,
    break: 75, // CI fails if mutation score < 75%
  },
  coverageAnalysis: 'perTest',
};
```

```python
# backend/mutmut.config.py
MUTMUT_CONFIG = {
    'paths_to_mutate': ['src/'],
    'paths_to_exclude': ['src/tests/', 'src/__pycache__/'],
    'runner': 'pytest',
    'test_command': 'pytest tests/',
    'mutation_score_threshold': 80,  # CI fails if < 80%
}
```

---

## Test Data Management

### Fixtures for Dev/Test Environments

```sql
-- shared/database/migrations/fixtures/test_data.sql
-- Test users
INSERT INTO users (user_id, clerk_user_id, auth_provider, email)
VALUES
  ('11111111-1111-1111-1111-111111111111', 'clerk_test_user_1', 'email', 'test1@example.com'),
  ('22222222-2222-2222-2222-222222222222', 'clerk_test_user_2', 'email', 'test2@example.com');

-- Test reports
INSERT INTO reports (report_id, user_id, subject, country, content, citations, status, expires_at)
VALUES
  (
    '33333333-3333-3333-3333-333333333333',
    '11111111-1111-1111-1111-111111111111',
    'Computer Science',
    'UK',
    '{"executive_summary": ["Test summary"]}'::jsonb,
    '[{"source": "Test", "url": "https://test.com", "confidence": 0.9}]'::jsonb,
    'completed',
    NOW() + INTERVAL '30 days'
  );
```

### Mock Payment Strategy

```typescript
// frontend/tests/mocks/stripe.ts
export class MockStripe {
  async confirmCardPayment(clientSecret: string, paymentMethod: any) {
    // Always succeed in dev/test
    if (process.env.ENVIRONMENT_MODE !== 'production') {
      return {
        paymentIntent: {
          id: 'pi_mock_123',
          status: 'succeeded',
        },
      };
    }

    // Use Stripe test mode in production tests
    return realStripe.confirmCardPayment(clientSecret, paymentMethod);
  }
}
```

---

## CI/CD Test Pipeline

```yaml
# .github/workflows/test.yml
name: Test Suite

on: [push, pull_request]

jobs:
  test-frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
      - run: npm ci
      - run: npm run test:unit
      - run: npm run test:integration
      - run: npm run test:mutation
      - name: Check coverage
        run: npx c8 check-coverage --lines 90 --branches 85 --functions 90

  test-backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.12'
      - run: pip install -r requirements.txt
      - run: pytest tests/ --cov=src --cov-report=term --cov-fail-under=90
      - run: mutmut run --paths-to-mutate=src/

  test-e2e:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: npm ci
      - run: npx playwright install
      - run: npm run test:e2e
```

---

## Related Documentation

- [Shared Component Interfaces](/Users/vihang/projects/study-abroad/docs/design/shared-component-interfaces.md)
- [Error Handling Design](/Users/vihang/projects/study-abroad/docs/design/error-handling.md)
- [Database Schema](/Users/vihang/projects/study-abroad/docs/database/schema.sql)
