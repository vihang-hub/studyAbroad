# Test Coverage Analysis & Action Plan
**Date:** 2026-01-03
**Analyst:** QA Testing Specialist
**Constitutional Requirement:** ≥90% statement and branch coverage

---

## Executive Summary

| Package | Current | Target | Gap | Priority | Estimated Effort |
|---------|---------|--------|-----|----------|-----------------|
| **Shared Packages** | 99.5% | 90% | ✅ +9.5% | ✅ Complete | 0 hours |
| **Frontend** | 21.93% | 90% | ❌ -68.07% | 🔴 CRITICAL | 12-16 hours |
| **Backend** | 71% | 90% | ❌ -19% | 🔴 HIGH | 10-14 hours |

**Overall Gate5-QA Status:** ❌ **FAIL**
**Total Remediation Time:** 22-30 hours
**Recommended Timeline:** 3-4 focused work days

---

## Current Coverage Metrics

### ✅ Shared Packages: 99.5% (PASSING)

All 4 shared packages exceed constitutional requirements:

```
shared/config:        99.8%  (58 tests passing)
shared/database:      99.82% (173 tests passing)
shared/feature-flags: 99%    (34 tests passing)
shared/logging:       99.47% (89 tests passing)
```

**Status:** No action required. Minor cleanup recommended for 1 logging test error.

---

### ❌ Frontend: 21.93% (FAILING - Critical Gap)

**Test Run Results:**
- Test Files: 11 (6 passed, 5 failed)
- Tests: 230 (217 passed, 13 skipped)
- Duration: 2.11s
- **Coverage Error:** 21.93% vs 40% threshold (set in vitest.config.ts)

**Coverage Breakdown:**
```
Statements: 21.93% (ERROR: -68.07% to target)
Branches:   77.77% (Better than expected)
Functions:  40%    (ERROR: -50% to target)
Lines:      21.93% (ERROR: -68.07% to target)
```

**What's Tested (100% coverage):**
- ✅ `ChatInput.tsx` - Complete
- ✅ `MessageList.tsx` - Complete
- ✅ `ReportSection.tsx` - Complete
- ✅ `CitationList.tsx` - Complete
- ✅ `ReportCard.tsx` - 97.86%
- ✅ `ReportSidebar.tsx` - Complete
- ✅ `useAuth` hook - Complete
- ✅ `useReports` hook - Complete

**Critical Gaps (0% coverage):**

1. **Pages (0%)** - 8 files, ~600 lines
   - `src/app/layout.tsx`
   - `src/app/page.tsx`
   - `src/app/(app)/layout.tsx`
   - `src/app/(app)/chat/page.tsx`
   - `src/app/(app)/chat/success/page.tsx`
   - `src/app/(app)/report/[id]/page.tsx`
   - `src/app/(app)/reports/page.tsx`
   - `src/app/(auth)/layout.tsx`
   - `src/app/sign-in/[[...rest]]/page.tsx`
   - `src/app/sign-up/[[...rest]]/page.tsx`

2. **Lib Utilities (0%)** - 7 files, ~800 lines
   - `src/lib/api-client.ts` (206 lines) - **HIGHEST IMPACT**
   - `src/lib/logger.ts` (213 lines) - **HIGH IMPACT**
   - `src/lib/config.ts` (164 lines) - **HIGH IMPACT**
   - `src/lib/clerk.ts` (59 lines)
   - `src/lib/supabase.ts` (26 lines)
   - `src/lib/runtime-setup-checks.ts` (32 lines)
   - `src/lib/utils.ts` (13 lines)

3. **Components (0%)** - 3 files
   - `src/components/ClerkWarning.tsx` (59 lines)
   - `src/components/chat/StreamingResponse.tsx` (212 lines) - **HIGH IMPACT**
   - `src/components/reports/ExecutiveSummary.tsx` (80 lines)
   - `src/components/dev/environment-badge.tsx` (126 lines)

4. **Hooks (0%)** - 1 file
   - `src/hooks/usePayment.ts` (89 lines) - **HIGH IMPACT**

5. **Providers (0%)** - 1 file
   - `src/providers/auth-provider.tsx` (163 lines) - **HIGH IMPACT**

6. **Middleware (0%)** - 1 file
   - `src/middleware.ts` (60 lines) - **MEDIUM IMPACT**

**Impact Analysis:**

Testing these files would add coverage:
- api-client.ts (206 lines) → +10-12% coverage
- logger.ts (213 lines) → +10-12% coverage
- StreamingResponse.tsx (212 lines) → +10-12% coverage
- config.ts (164 lines) → +8-10% coverage
- auth-provider.tsx (163 lines) → +8-10% coverage
- usePayment.ts (89 lines) → +4-5% coverage

**Total potential gain:** ~60-70% coverage from just 6 files

---

### ❌ Backend: 71% (FAILING - Moderate Gap)

**Test Run Results:**
- Tests: 232 total (129 passed, 91 failed, 11 errors, 1 skipped)
- Duration: 1.87s
- Coverage: 71% statements (1710 total, 496 missed)

**Test Failure Breakdown:**

| Category | Failed | Root Cause |
|----------|--------|------------|
| Stripe Webhook Security | 9 | Missing webhook endpoint implementation |
| Stripe Integration | 1 | Database setup issues |
| User Story 1 (Report Gen) | 18 | Auth/Payment/Streaming issues |
| User Story 2 (History) | 13 | RLS/Immutability issues |
| User Story 3 (Retention) | 19 | Cron endpoint not implemented |
| Report Service | 7 | Edge cases |
| Streaming | 13 | Stream chunk validation |
| Auth Service | 7 | Token validation |
| Payment Service | 3 | Webhook handling |
| **Total** | **91** | |

**Critical Coverage Gaps:**

1. **Cron Endpoints** (~0% coverage) - **HIGHEST IMPACT**
   - `/api/cron/expire-reports` - Not implemented
   - `/api/cron/delete-expired-reports` - Not implemented
   - Impact: 19 User Story 3 tests failing
   - Estimated coverage gain: +10-12%

2. **Stripe Webhook Endpoint** (~30% coverage) - **HIGH IMPACT**
   - `/api/webhooks/stripe` - Partial implementation
   - Missing: Signature validation, event handling
   - Impact: 9 webhook security tests + 1 integration test failing
   - Estimated coverage gain: +5-7%

3. **Report Service - Edge Cases** (~60% coverage) - **MEDIUM IMPACT**
   - Expiration logic edge cases
   - Deletion logic edge cases
   - RLS enforcement with multiple users
   - GDPR cascade deletion
   - Impact: 13 User Story 2 tests + 7 service tests failing
   - Estimated coverage gain: +5-7%

4. **Auth Service** (~70% coverage) - **MEDIUM IMPACT**
   - Cron secret validation
   - Token refresh logic
   - Multi-provider OAuth edge cases
   - Impact: 7 auth service tests failing
   - Estimated coverage gain: +3-4%

5. **Payment Service** (~75% coverage) - **LOW IMPACT**
   - Payment session creation errors
   - Payment failure scenarios
   - Impact: 3 payment service tests failing
   - Estimated coverage gain: +2-3%

6. **Streaming Service** (~60% coverage) - **MEDIUM IMPACT**
   - Stream chunk validation
   - Error handling in streaming
   - Impact: 13 streaming tests failing
   - Estimated coverage gain: +4-5%

---

## Strategic Action Plan

### Phase 1: Frontend - High-Impact Files (12-16 hours)

**Priority 1: Core Utilities (6-8 hours)**

1. **api-client.ts** (3-4 hours)
   - Test all HTTP methods (GET, POST, PUT, DELETE)
   - Test error handling (network errors, 4xx, 5xx)
   - Test authentication header injection
   - Test retry logic
   - Test timeout handling
   - Expected coverage gain: +10-12%

2. **logger.ts** (2-3 hours)
   - Test log levels (debug, info, warn, error)
   - Test correlation ID generation
   - Test sensitive data sanitization
   - Test file transport
   - Expected coverage gain: +10-12%

3. **config.ts** (1-2 hours)
   - Test environment variable loading
   - Test validation logic
   - Test defaults
   - Expected coverage gain: +8-10%

**Priority 2: React Components & Hooks (4-6 hours)**

4. **StreamingResponse.tsx** (2-3 hours)
   - Test chunk rendering
   - Test markdown parsing
   - Test citation links
   - Test error states
   - Expected coverage gain: +10-12%

5. **auth-provider.tsx** (1-2 hours)
   - Test Clerk integration
   - Test auth state management
   - Test loading states
   - Expected coverage gain: +8-10%

6. **usePayment.ts** (1 hour)
   - Test Stripe checkout flow
   - Test error handling
   - Test loading states
   - Expected coverage gain: +4-5%

**Priority 3: Middleware & Remaining (2 hours)**

7. **middleware.ts** (1 hour)
   - Test auth redirection
   - Test public routes
   - Expected coverage gain: +3-4%

8. **Executive Summary, Environment Badge** (1 hour)
   - Test component rendering
   - Expected coverage gain: +3-4%

**Expected Frontend Coverage After Phase 1:** 80-90%

---

### Phase 2: Backend - Critical Gaps (10-14 hours)

**Priority 1: Cron Endpoints (4-5 hours)**

1. **Implement /api/cron/expire-reports** (2-2.5 hours)
   - Add integration tests for expiration logic
   - Test cron secret authentication
   - Test bulk update operations
   - Test monitoring/logging
   - Expected coverage gain: +5-6%

2. **Implement /api/cron/delete-expired-reports** (2-2.5 hours)
   - Add integration tests for deletion logic
   - Test GDPR cascade deletion
   - Test cron secret authentication
   - Test monitoring/logging
   - Expected coverage gain: +5-6%

**Priority 2: Webhook Implementation (3-4 hours)**

3. **Complete /api/webhooks/stripe** (3-4 hours)
   - Implement signature validation
   - Implement event handling
   - Test all webhook security scenarios
   - Test idempotency
   - Expected coverage gain: +5-7%

**Priority 3: Service Edge Cases (3-4 hours)**

4. **Report Service Edge Cases** (2-3 hours)
   - Test expiration edge cases (exactly 30 days, 29, 31)
   - Test RLS with multiple users
   - Test concurrent access
   - Expected coverage gain: +3-4%

5. **Streaming Service** (1 hour)
   - Test chunk validation
   - Test error handling
   - Expected coverage gain: +2-3%

**Priority 4: Auth & Payment (2-3 hours)**

6. **Auth Service** (1-1.5 hours)
   - Test cron secret validation
   - Test token refresh edge cases
   - Expected coverage gain: +2-3%

7. **Payment Service** (1-1.5 hours)
   - Test payment creation errors
   - Test payment failure flows
   - Expected coverage gain: +1-2%

**Expected Backend Coverage After Phase 2:** 90-95%

---

### Phase 3: Mutation Testing (8-12 hours)

**After achieving 90% coverage, validate test effectiveness:**

1. **Frontend Mutation Testing** (3-4 hours)
   - Run Stryker on frontend
   - Analyze surviving mutants
   - Add targeted tests to kill mutants
   - Target: >80% mutation score

2. **Shared Mutation Testing** (2-3 hours)
   - Run Stryker on shared packages
   - Analyze surviving mutants
   - Target: >80% mutation score

3. **Backend Mutation Testing** (3-5 hours)
   - Run mutmut on backend (or pytest-mutpy)
   - Analyze surviving mutants
   - Add targeted tests
   - Target: >80% mutation score

---

## Timeline & Resource Allocation

| Phase | Focus | Hours | Days (1 engineer) |
|-------|-------|-------|-------------------|
| Phase 1 | Frontend High-Impact | 12-16 | 1.5-2 |
| Phase 2 | Backend Critical Gaps | 10-14 | 1.5-2 |
| Phase 3 | Mutation Testing | 8-12 | 1-1.5 |
| **Total** | | **30-42** | **4-5.5** |

**Recommended Approach:**
- Allocate 1 QA Engineer full-time for 4-5 days
- OR: 2 QA Engineers for 2-3 days (parallel work on frontend/backend)

---

## Success Criteria

### For Gate5-QA PASS:
- [x] Shared packages ≥90% coverage (Current: 99.5%)
- [ ] Frontend ≥90% coverage (Current: 21.93%, Need: +68.07%)
- [ ] Backend ≥90% coverage (Current: 71%, Need: +19%)
- [ ] All packages >80% mutation score (Not yet measured)
- [ ] All tests passing (Currently: 91 backend tests failing)
- [ ] Coverage reports generated and up-to-date
- [ ] Mutation reports generated

---

## Risks & Mitigations

**Risk 1:** Next.js App Router pages difficult to test
- **Mitigation:** Focus on utility functions and components first; pages contribute less to business logic

**Risk 2:** Mutation testing may reveal weak tests despite good coverage
- **Mitigation:** Allocate buffer time (8-12 hours) for mutation score remediation

**Risk 3:** Backend cron endpoints may require significant implementation work
- **Mitigation:** Implementation may need to happen before testing (not just test writing)

**Risk 4:** Flaky tests due to async operations
- **Mitigation:** Use proper async/await patterns, mock timers, isolated test fixtures

---

## Next Actions (Priority Order)

1. **Immediate (Today):**
   - [ ] Create test for `api-client.ts` (3-4 hours)
   - [ ] Create test for `logger.ts` (2-3 hours)
   - [ ] Expected frontend coverage: 21.93% → 45-50%

2. **Day 2:**
   - [ ] Create test for `config.ts` (1-2 hours)
   - [ ] Create test for `StreamingResponse.tsx` (2-3 hours)
   - [ ] Create test for `auth-provider.tsx` (1-2 hours)
   - [ ] Create test for `usePayment.ts` (1 hour)
   - [ ] Expected frontend coverage: 45-50% → 85-90%

3. **Day 3:**
   - [ ] Implement and test `/api/cron/expire-reports` (2-2.5 hours)
   - [ ] Implement and test `/api/cron/delete-expired-reports` (2-2.5 hours)
   - [ ] Complete `/api/webhooks/stripe` implementation and tests (3-4 hours)
   - [ ] Expected backend coverage: 71% → 85-90%

4. **Day 4:**
   - [ ] Add report service edge case tests (2-3 hours)
   - [ ] Add streaming service tests (1 hour)
   - [ ] Add auth/payment edge cases (2-3 hours)
   - [ ] Expected backend coverage: 85-90% → 90-95%

5. **Day 5:**
   - [ ] Run mutation testing on all packages (6-8 hours)
   - [ ] Generate final reports (1-2 hours)
   - [ ] Update Gate5-QA checklist (1 hour)

---

## Deliverables

Upon completion, the following will be updated:

1. **Coverage Reports:**
   - `/Users/vihang/projects/study-abroad/frontend/coverage/index.html`
   - `/Users/vihang/projects/study-abroad/backend/htmlcov/index.html`
   - `/Users/vihang/projects/study-abroad/shared/*/coverage/index.html`

2. **Mutation Reports:**
   - `/Users/vihang/projects/study-abroad/docs/testing/mutation-frontend.md`
   - `/Users/vihang/projects/study-abroad/docs/testing/mutation-backend.md`
   - `/Users/vihang/projects/study-abroad/docs/testing/mutation-shared.md`

3. **Updated Checklists:**
   - `/Users/vihang/projects/study-abroad/agents/checklists/Gate5-QA.md`

4. **Final Summary:**
   - `/Users/vihang/projects/study-abroad/docs/testing/coverage-final.md`

---

**Analysis Complete:** 2026-01-03 11:10 UTC
**Analyst:** QA Testing Specialist
**Status:** Ready for implementation
