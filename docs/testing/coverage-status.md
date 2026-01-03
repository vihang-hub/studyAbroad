# Test Coverage Status

**Generated:** 2025-12-31
**Project:** Study Abroad MVP - UK Study & Migration Research App

---

## Executive Summary

**Overall Status:** ⚠️ PARTIAL (Below 90% requirement)

- **Backend Coverage:** 81% (Target: ≥90%)
- **Frontend Coverage:** Unmeasured (tests failing)
- **Constitution Requirement:** ≥90% statement and branch coverage

---

## Backend Coverage (Python)

### Overall Metrics

```
Name                                  Stmts   Miss  Cover
---------------------------------------------------------
src/__init__.py                           0      0   100%
src/api/__init__.py                       0      0   100%
src/api/models/__init__.py                0      0   100%
src/api/models/payment.py                35      0   100%
src/api/models/report.py                 76     11    86%
src/api/models/user.py                   31     31     0%
src/api/routes/__init__.py                0      0   100%
src/api/routes/health.py                 17      0   100%
src/api/routes/reports.py                33     10    70%
src/api/routes/webhooks.py               53     32    40%
src/api/services/__init__.py              0      0   100%
src/api/services/ai_service.py           40      7    82%
src/api/services/auth_service.py         24      0   100%
src/api/services/payment_service.py      41      0   100%
src/api/services/report_service.py       42      0   100%
src/config.py                            36      1    97%
src/lib/__init__.py                       0      0   100%
src/lib/supabase.py                      10      1    90%
src/main.py                              42      0   100%
---------------------------------------------------------
TOTAL                                   480     93    81%
```

**Status:** ❌ FAIL (Required: 90%, Actual: 81%)

### Coverage Gaps Analysis

#### Critical Gaps (0-70% coverage)

1. **src/api/models/user.py: 0% (31 statements uncovered)**
   - **Impact:** HIGH - User model has no test coverage
   - **Risk:** User validation, serialization bugs could go undetected
   - **Required Tests:**
     - User model validation (email format, required fields)
     - Clerk integration data mapping
     - User creation edge cases
   - **Estimated Effort:** 2 hours

2. **src/api/routes/webhooks.py: 40% (32 statements uncovered)**
   - **Impact:** HIGH - Payment webhooks are critical path
   - **Risk:** Webhook failures could result in unpaid reports or lost revenue
   - **Required Tests:**
     - All Stripe event types (payment_succeeded, failed, refunded)
     - Webhook signature verification
     - Invalid event handling
     - Database state transitions
   - **Estimated Effort:** 3 hours

3. **src/api/routes/reports.py: 70% (10 statements uncovered)**
   - **Impact:** MEDIUM - Core report API endpoints
   - **Required Tests:**
     - Error handling paths
     - Edge cases for report retrieval
     - Authorization failures
   - **Estimated Effort:** 1-2 hours

#### Moderate Gaps (71-89% coverage)

4. **src/api/services/ai_service.py: 82% (7 statements uncovered)**
   - **Impact:** MEDIUM
   - **Required Tests:**
     - Streaming error handling
     - JSON parsing failures
     - Citation validation edge cases
   - **Estimated Effort:** 1 hour

5. **src/api/models/report.py: 86% (11 statements uncovered)**
   - **Impact:** MEDIUM
   - **Required Tests:**
     - Pydantic validation error messages
     - Citation count edge cases
     - Section ordering validation
   - **Estimated Effort:** 1 hour

### Test Execution Results

**Total Tests:** 76
- **Passed:** 56
- **Failed:** 20 (due to new Pydantic validation - expected)

**Failed Test Categories:**
1. AI service tests (5 failures) - New section validation
2. API endpoint tests (13 failures) - Dependencies on AI service
3. Webhook tests (2 failures) - Dependencies on report service

**Note:** Test failures are expected after implementing strict section validation. Tests need updating to match new requirements.

---

## Frontend Coverage (TypeScript)

### Overall Status

**Status:** ❌ CANNOT MEASURE (prerequisite: fix failing tests)

**Blocker:** 11 failing tests prevent coverage tool from running

### Test Execution Results

```
Test Files:  4 failed | 1 passed (5)
Tests:      11 failed | 105 passed (116)
```

**Failure Rate:** 9.5% (11/116 tests failing)

### Failed Test Analysis

**File:** `tests/components/ReportSection.test.tsx`

**Failures:**
1. Markdown content multiline handling (whitespace assertion)
2. Markdown list rendering (newline handling)
3. Long content rendering (trailing whitespace)

**Root Cause:** Test assertions expect exact text content including newlines, but rendered HTML collapses whitespace

**Fix Required:**
- Update test assertions to use `.toContain()` instead of `.toHaveTextContent()` for multiline content
- Or update assertions to match actual HTML rendering behavior

**Estimated Effort:** 1-2 hours

---

## Mutation Testing Status

### Backend (Python)

**Status:** ⚠️ NOT CONFIGURED

**Recommendation:** Use `mutmut` or `cosmic-ray` for Python mutation testing

**Setup:**
```bash
cd backend
pip install mutmut
mutmut run --paths-to-mutate=src/
mutmut results
```

**Expected First Run:** 3-4 hours (including mutant analysis)

### Frontend (TypeScript)

**Status:** ⚠️ CONFIGURED BUT NOT RUN

**Blocker:** Missing Stryker vitest runner plugin

**Error:**
```
Cannot find TestRunner plugin "vitest".
In fact, no TestRunner plugins were loaded.
```

**Fix:**
```bash
cd frontend
npm install --save-dev @stryker-mutator/vitest-runner
npm run test:mutation
```

**Expected Runtime:** 15-30 minutes (289 mutants configured)

**Estimated Effort:** 2-3 hours (including analysis and fixing surviving mutants)

---

## Action Plan to Reach 90% Coverage

### Phase 1: Backend Critical Gaps (Priority P0)

**Estimated Total:** 6-7 hours

1. **Add User Model Tests** (2 hours)
   - Create `tests/test_user_model.py`
   - Test all validation rules
   - Test Clerk data mapping

2. **Add Webhook Integration Tests** (3 hours)
   - Test all Stripe event types
   - Test signature verification
   - Test database state changes

3. **Complete Reports Endpoint Tests** (1-2 hours)
   - Test error paths
   - Test authorization edge cases

### Phase 2: Backend Moderate Gaps (Priority P1)

**Estimated Total:** 2 hours

4. **Complete AI Service Tests** (1 hour)
   - Test streaming errors
   - Test validation edge cases

5. **Complete Report Model Tests** (1 hour)
   - Test Pydantic validators
   - Test citation validation

### Phase 3: Frontend (Priority P1)

**Estimated Total:** 3-4 hours

6. **Fix Failing Frontend Tests** (1-2 hours)
   - Fix ReportSection test assertions
   - Ensure all tests pass

7. **Measure Frontend Coverage** (30 min)
   - Run `npm test -- --coverage`
   - Identify gaps

8. **Add Frontend Tests** (2 hours)
   - Target uncovered components
   - Reach 90% coverage

### Phase 4: Mutation Testing (Priority P1)

**Estimated Total:** 5-7 hours

9. **Run Backend Mutation Tests** (3-4 hours)
   - Install and configure mutmut
   - Run mutation testing
   - Kill surviving mutants

10. **Run Frontend Mutation Tests** (2-3 hours)
    - Install vitest runner
    - Run Stryker
    - Kill surviving mutants

---

## Timeline

**Total Estimated Effort:** 16-20 hours

**Recommended Schedule:**

- **Day 1 (6-8 hours):** Backend critical gaps
- **Day 2 (4-6 hours):** Backend moderate gaps + frontend fixes
- **Day 3 (6-8 hours):** Mutation testing

**Blockers Removed By:**
- End of Day 1: Backend coverage ≥90%
- End of Day 2: Frontend coverage ≥90%
- End of Day 3: Mutation score >80%

---

## Success Criteria

- [ ] Backend coverage ≥90%
- [ ] Frontend coverage ≥90%
- [ ] Backend mutation score >80%
- [ ] Frontend mutation score >80%
- [ ] All tests passing
- [ ] Coverage reports documented
- [ ] Mutation reports documented

**Current Progress:** 2/7 criteria met (29%)

---

## References

**Constitution Requirement:** `.specify/memory/constitution.md` Section 3
- "Mandatory 90% statement/branch coverage"
- ">80% mutation score threshold"

**Test Strategy:** `/docs/testing-strategy.md`

**Coverage Commands:**
```bash
# Backend
cd backend
pytest --cov=src --cov-report=html --cov-report=term

# Frontend
cd frontend
npm test -- --coverage
```

---

**Document Version:** 1.0.0
**Last Updated:** 2025-12-31
**Next Update:** After Phase 1 completion
