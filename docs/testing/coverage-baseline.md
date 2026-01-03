# Coverage Baseline Report

**Report Date:** 2026-01-03
**Target Coverage:** ≥90% (statement and branch)

## Summary

| Package | Statements | Branches | Functions | Lines | Status |
|---------|-----------|----------|-----------|-------|--------|
| **shared/config** | 99.8% | 97.29% | 100% | 99.8% | ✅ PASS |
| **shared/database** | 99.82% | 97.36% | 98.36% | 99.82% | ✅ PASS |
| **shared/logging** | 99.47% | 92.4% | 100% | 99.47% | ✅ PASS |
| **shared/feature-flags** | 99% | 94.44% | 100% | 99% | ✅ PASS |
| **frontend** | N/A | N/A | N/A | N/A | ❌ BLOCKED (test setup issues) |
| **backend** | 70% | N/A | N/A | 70% | ❌ FAIL (-20%) |

## Detailed Results

### ✅ Shared Packages (ALL PASSING)

All four shared packages exceed the 90% coverage threshold:

#### shared/config (99.8% coverage)
- **Test Files:** 4 (58 tests passed)
- **Uncovered Lines:** 2 lines in `environment.schema.ts` (253-254)
- **Status:** Excellent coverage

```
 % Coverage report from v8
-------------------|---------|----------|---------|---------|-------------------
File               | % Stmts | % Branch | % Funcs | % Lines | Uncovered Line #s
-------------------|---------|----------|---------|---------|-------------------
All files          |    99.8 |    97.29 |     100 |    99.8 |
 src               |     100 |      100 |     100 |     100 |
  index.ts         |     100 |      100 |     100 |     100 |
  loader.ts        |     100 |      100 |     100 |     100 |
  presets.ts       |     100 |      100 |     100 |     100 |
 src/schemas       |   99.68 |    95.65 |     100 |   99.68 |
  api.schema.ts    |     100 |      100 |     100 |     100 |
  ...ent.schema.ts |   99.44 |    95.65 |     100 |   99.44 | 253-254
-------------------|---------|----------|---------|---------|-------------------
```

#### shared/database (99.82% coverage)
- **Test Files:** 7 (173 tests passed)
- **Uncovered Lines:** 3 lines total (base.ts: 24-25, postgres.ts: 39-41)
- **Status:** Excellent coverage

```
 % Coverage report from v8
------------------|---------|----------|---------|---------|-------------------
File              | % Stmts | % Branch | % Funcs | % Lines | Uncovered Line #s
------------------|---------|----------|---------|---------|-------------------
All files         |   99.82 |    97.36 |   98.36 |   99.82 |
 src              |     100 |      100 |     100 |     100 |
  index.ts        |     100 |      100 |     100 |     100 |
  types.ts        |     100 |      100 |     100 |     100 |
 src/adapters     |     100 |    92.68 |     100 |     100 |
  base.ts         |     100 |      100 |     100 |     100 |
  index.ts        |     100 |      100 |     100 |     100 |
  postgres.ts     |     100 |    89.28 |     100 |     100 | 39-41
  supabase.ts     |     100 |      100 |     100 |     100 |
 src/repositories |   99.66 |      100 |   97.36 |   99.66 |
  base.ts         |   98.07 |      100 |   85.71 |   98.07 | 24-25
  index.ts        |     100 |      100 |     100 |     100 |
  payment.ts      |     100 |      100 |     100 |     100 |
  report.ts       |     100 |      100 |     100 |     100 |
  user.ts         |     100 |      100 |     100 |     100 |
------------------|---------|----------|---------|---------|-------------------
```

#### shared/logging (99.47% coverage)
- **Test Files:** 3 (89 tests passed, 1 unhandled error)
- **Uncovered Lines:** 3 lines in Logger.ts (115, 175-176)
- **Issues:** One unhandled error in file logging test (ENOENT for nested directory)
- **Status:** Excellent coverage, minor test cleanup needed

```
 % Coverage report from v8
----------------|---------|----------|---------|---------|-------------------
File            | % Stmts | % Branch | % Funcs | % Lines | Uncovered Line #s
----------------|---------|----------|---------|---------|-------------------
All files       |   99.47 |     92.4 |     100 |   99.47 |
 Logger.ts      |      99 |    83.78 |     100 |      99 | 115,175-176
 correlation.ts |     100 |      100 |     100 |     100 |
 sanitizer.ts   |     100 |      100 |     100 |     100 |
----------------|---------|----------|---------|---------|-------------------
```

#### shared/feature-flags (99% coverage)
- **Test Files:** 3 (34 tests passed)
- **Uncovered Lines:** 2 lines in evaluator.ts (143-144)
- **Status:** Excellent coverage

```
 % Coverage report from v8
--------------|---------|----------|---------|---------|-------------------
File          | % Stmts | % Branch | % Funcs | % Lines | Uncovered Line #s
--------------|---------|----------|---------|---------|-------------------
All files     |      99 |    94.44 |     100 |      99 |
 evaluator.ts |   98.63 |    94.11 |     100 |   98.63 | 143-144
 index.ts     |     100 |      100 |     100 |     100 |
 types.ts     |     100 |      100 |     100 |     100 |
--------------|---------|----------|---------|---------|-------------------
```

### ❌ Frontend (BLOCKED)

**Status:** Tests cannot run due to missing dependencies and environment setup issues

**Blocking Issues:**
1. ✅ FIXED: Missing `@testing-library/dom` (installed)
2. ❌ PENDING: Tests require environment variables (DATABASE_URL, GEMINI_API_KEY)
3. ❌ PENDING: React hook tests have `act()` warnings
4. ❌ PENDING: 11 test suites failing due to config initialization

**Test Files Affected:**
- `tests/components/ChatInput.test.tsx`
- `tests/components/CitationList.test.tsx`
- `tests/components/MessageList.test.tsx`
- `tests/components/ReportCard.test.tsx`
- `tests/components/ReportSection.test.tsx`
- `tests/components/ReportSidebar.test.tsx`
- `tests/hooks/useAuth.test.ts`
- `tests/hooks/useReports.test.ts`
- `src/__tests__/integration/shared-packages.test.ts`
- `src/__tests__/integration/user-story-1-acceptance.test.tsx`
- `src/__tests__/integration/user-story-2-acceptance.test.tsx`

**Next Steps:**
1. Create `.env.test` file for frontend with mock values
2. Mock config initialization in test setup
3. Fix React `act()` warnings in hook tests
4. Re-run coverage measurement

### ❌ Backend (70% coverage - FAIL)

**Status:** 20 percentage points below target (need +20% to reach 90%)

**Test Results:**
- **Total Statements:** 1534
- **Missed Statements:** 464
- **Coverage:** 70%
- **Tests:** 129 passed, 91 failed, 1 skipped, 1 error

**Major Coverage Gaps:**

The backend has the largest coverage gap. Based on test failures, the following areas need additional tests:

1. **Cron Endpoints** (User Story 3 - Report Expiration)
   - `/api/cron/expire-reports`
   - `/api/cron/delete-expired-reports`
   - All 47 cron-related tests failing

2. **Report Service**
   - Report expiration logic
   - Report deletion logic
   - RLS (Row Level Security) enforcement
   - GDPR compliance (cascade delete)

3. **Payment Service**
   - Stripe webhook handling
   - Payment session creation
   - Payment failure scenarios

4. **Auth Service**
   - Cron secret validation
   - Multi-provider OAuth (Google, Apple, Facebook)

5. **Integration Tests**
   - 47 integration tests failing in user story acceptance tests
   - Stripe webhook security tests

**Configuration Issues Fixed:**
- ✅ Aligned `ENABLE_RATE_LIMITING` config (was `RATE_LIMIT_ENABLED`)
- ✅ Installed `email-validator` and `pytest-timeout` packages

**Test Failures Breakdown:**
- User Story 1 Acceptance: 18 failures (auth, payment, streaming)
- User Story 2 Acceptance: 13 failures (report history, RLS)
- User Story 3 Acceptance: 19 failures (expiration, deletion, GDPR)
- Unit Tests: 12 failures (services, repositories)
- Integration Tests: 29 failures (webhooks, security)

## Gap Analysis

### Critical Gaps to Address

1. **Backend: +20% coverage needed**
   - **Focus Area 1:** Cron endpoints (highest priority - new code, 0% coverage)
   - **Focus Area 2:** Report service edge cases (expiration, deletion)
   - **Focus Area 3:** Payment webhook scenarios
   - **Focus Area 4:** Auth service error handling

2. **Frontend: Blocked by test setup**
   - Must fix environment setup before measuring coverage
   - Estimated 50-100 tests waiting to run

3. **Shared Packages: Already passing** ✅
   - No action needed (all >99% coverage)

## Recommendations

### Priority 1: Fix Frontend Test Setup (2-4 hours)
1. Create `frontend/.env.test` with mock values
2. Mock config loader in test setup
3. Fix React `act()` warnings
4. Measure baseline coverage

### Priority 2: Improve Backend Coverage (12-18 hours)
1. **Cron Endpoints** (6-8 hours)
   - Add integration tests for expire/delete endpoints
   - Test cron secret authentication
   - Test monitoring/logging

2. **Report Service** (3-4 hours)
   - Test expiration edge cases
   - Test deletion logic
   - Test RLS enforcement

3. **Payment Service** (2-3 hours)
   - Test webhook validation
   - Test payment failures
   - Test session creation errors

4. **Auth Service** (1-2 hours)
   - Test cron secret validation
   - Test OAuth providers (mock)

### Priority 3: Close Remaining Gaps (2-4 hours)
1. Fix logging test unhandled error
2. Add tests for uncovered edge cases in shared packages
3. Final validation run

## Timeline Estimate

- **Frontend Setup:** 2-4 hours
- **Backend Coverage:** 12-18 hours
- **Cleanup:** 2-4 hours
- **Total:** 16-26 hours

## Success Criteria

- ✅ All shared packages: ≥90% coverage (COMPLETE)
- ❌ Frontend: ≥90% coverage (BLOCKED)
- ❌ Backend: ≥90% coverage (70% - need +20%)
- ❌ All tests passing
- ❌ Coverage report generated

## Notes

- Backend test failures are primarily in integration tests, which suggests the implementation may have issues beyond just coverage gaps
- Many test failures are related to database interactions and mocking
- Some tests use `@pytest.mark.timeout` which requires `pytest-timeout` package (now installed)
- Frontend tests are well-structured but blocked by environment setup
- Shared packages demonstrate excellent test quality and coverage
