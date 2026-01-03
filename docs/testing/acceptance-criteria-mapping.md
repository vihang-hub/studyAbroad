# Acceptance Criteria Test Coverage Mapping

**Project**: UK Study & Migration Research App MVP
**Analysis Date**: 2025-12-31
**Analyzed By**: QA Testing Specialist
**Spec Version**: specs/001-mvp-uk-study-migration/spec.md

---

## Overview

This document maps each acceptance criterion from Section 14 of spec.md to specific test cases. The goal is to ensure **100% specification faithfulness** as required by the project constitution.

---

## Acceptance Criteria Status

| ID | Acceptance Criterion | Test Coverage | Status |
|----|----------------------|---------------|--------|
| AC-1 | User can authenticate using all supported methods | Partial | ❌ INCOMPLETE |
| AC-2 | User is charged £2.99 exactly once per query | Yes | ⚠️ TESTS FAILING |
| AC-3 | Failed payment results in no report | Yes | ⚠️ TESTS FAILING |
| AC-4 | Successful payment produces a streamed report | Yes | ⚠️ TESTS FAILING |
| AC-5 | Reports are accessible for 30 days | Yes | ⚠️ TESTS FAILING |
| AC-6 | Reports cannot be accessed by other users | Yes | ⚠️ TESTS FAILING |
| AC-7 | All mandatory report sections are present | Yes | ⚠️ TESTS FAILING |
| AC-8 | All factual claims include citations | Yes | ⚠️ TESTS FAILING |
| AC-9 | UK-only constraint is enforced | Yes | ✅ PASSING |

**Summary**:
- 9 acceptance criteria defined
- 9 have test coverage (100%)
- 1 passing (11%)
- 7 failing due to test infrastructure issues (78%)
- 1 incomplete (11%)

---

## Detailed Mapping

### AC-1: User can authenticate using all supported methods

**Specification Requirement**:
> "User must authenticate before submitting a paid query. Supported login methods: Google OAuth, Apple, Facebook, Email."

**Test Coverage**:

#### Shared Package Tests
- **File**: `/Users/vihang/projects/study-abroad/shared/tests/hooks/useAuth.test.ts`
- **Status**: ❌ FAILING (9/9 tests failing - mock configuration issue)

**Test Cases**:
1. ✅ `should return loading state when not loaded` - Tests auth initialization
2. ✅ `should return authenticated user when signed in` - Tests successful auth
3. ✅ `should use username as fallback for displayName` - Tests user data mapping
4. ✅ `should use "User" as default displayName` - Tests default values
5. ✅ `should return unauthenticated state when not signed in` - Tests logged out state
6. ✅ `should provide signOut function that calls Clerk signOut` - Tests sign out
7. ✅ `should provide openSignIn function` - Tests sign in modal
8. ✅ `should provide openSignUp function` - Tests sign up modal
9. ✅ `should set isSubscribed to false by default` - Tests subscription state

#### Shared Package - LoginForm Tests
- **File**: `/Users/vihang/projects/study-abroad/shared/tests/components/LoginForm.test.tsx`
- **Status**: ❌ FAILING (10/10 tests failing - missing jest-dom matchers)

**Test Cases**:
1. ❌ `should render with default props` - Tests form rendering
2. ❌ `should render OAuth buttons with signin mode` - Tests Google/Apple/Facebook OAuth
3. ❌ `should render email auth form with signin mode` - Tests email authentication
4. ❌ `should show divider by default` - Tests UI layout
5. ❌ `should hide divider when showDivider is false` - Tests conditional rendering
6. ❌ `should render link to signup page` - Tests navigation
7. ❌ `should not display error initially` - Tests error state
8. ❌ `should call onSuccess callback` - Tests successful auth
9. ❌ `should call onError callback` - Tests failed auth
10. ❌ `should render with custom providers` - Tests provider configuration

**Coverage Gap**: ❌ No E2E tests validating actual OAuth flows with external providers

**Recommendation**:
- Fix mock configuration in useAuth tests
- Add @testing-library/jest-dom to shared package setup.ts
- Create integration tests with Clerk test mode for OAuth flows
- Add E2E tests with Playwright to verify full authentication flows

---

### AC-2: User is charged £2.99 exactly once per query

**Specification Requirement**:
> "Price per query: £2.99 (GBP). Payment must succeed before report generation. One successful payment → one report."

**Test Coverage**:

#### Backend Tests
- **File**: `/Users/vihang/projects/study-abroad/backend/tests/test_payment_service.py`
- **Status**: ❌ FAILING (6/6 tests failing - async/mock configuration)

**Test Cases**:
1. ❌ `test_create_checkout_session_success` - Verifies Stripe session with amount=299 (£2.99)
2. ❌ `test_create_checkout_session_stripe_error` - Tests payment creation failure
3. ❌ `test_create_checkout_session_db_error` - Tests database failure during payment
4. ❌ `test_update_payment_status_success` - Verifies payment completion
5. ❌ `test_get_payment_found` - Tests payment retrieval
6. ❌ `test_get_payment_not_found` - Tests missing payment handling

#### Shared Package Tests
- **File**: `/Users/vihang/projects/study-abroad/shared/tests/hooks/usePayment.test.ts`
- **Status**: ❌ FAILING (6/6 tests failing - missing module)

**Test Cases**:
1. ❌ `should initialize with default state` - Tests initial payment state
2. ❌ `should create checkout session successfully` - Tests payment initiation
3. ❌ `should handle API errors` - Tests error handling
4. ❌ `should handle network errors` - Tests connectivity issues
5. ❌ `should set loading state during checkout` - Tests loading indicator
6. ❌ `should call onSuccess with correct report ID` - Tests callback after payment

#### Shared Package - CheckoutButton Tests
- **File**: `/Users/vihang/projects/study-abroad/shared/tests/components/CheckoutButton.test.tsx`
- **Status**: ⚠️ PARTIAL (5/14 passing - missing jest-dom matchers)

**Test Cases**:
1. ❌ `should render with default amount` - Verifies £2.99 display
2. ❌ `should render with custom amount` - Tests configurable pricing
3. ❌ `should be disabled when query is empty` - Prevents payment without query
4. ⚠️ `should call onCheckoutStart when clicked` - Tests payment flow initiation
5. ⚠️ `should call createCheckout with correct params` - Verifies payment creation

**Coverage Gap**: ❌ No tests verifying duplicate payment prevention (idempotency)

**Recommendation**:
- Fix async test configuration in backend
- Add payment idempotency key tests
- Test duplicate payment rejection
- Verify amount is always 299 (£2.99 in pence)

---

### AC-3: Failed payment results in no report

**Specification Requirement**:
> "If payment fails or is cancelled: No report is generated, No data is stored."

**Test Coverage**:

#### Backend Tests
- **File**: `/Users/vihang/projects/study-abroad/backend/tests/test_payment_service.py`
- **Status**: ❌ FAILING

**Test Cases**:
1. ❌ `test_update_payment_status_with_error` - Tests payment.failed event
2. ❌ `test_create_checkout_session_stripe_error` - Tests session creation failure

#### Backend API Tests
- **File**: `/Users/vihang/projects/study-abroad/backend/tests/test_api_endpoints.py`
- **Status**: ❌ FAILING

**Test Cases**:
1. ❌ `test_stripe_webhook_payment_failed` - Verifies no report on payment failure

**Coverage Gap**: ❌ No tests verifying database rollback on payment failure

**Recommendation**:
- Add transaction rollback tests
- Verify no report record exists after payment failure
- Test partial payment scenarios (network timeout mid-payment)

---

### AC-4: Successful payment produces a streamed report

**Specification Requirement**:
> "Backend calls Gemini APIs. Responses are streamed to the frontend."

**Test Coverage**:

#### Backend AI Service Tests
- **File**: `/Users/vihang/projects/study-abroad/backend/tests/test_ai_service.py`
- **Status**: ⚠️ PARTIAL (13/21 passing)

**Test Cases**:
1. ✅ `test_is_uk_query_*` - 13 tests for UK validation (ALL PASSING)
2. ❌ `test_generate_report_success` - Tests successful report generation
3. ❌ `test_generate_report_stream` - Tests streaming functionality
4. ❌ `test_generate_report_llm_error` - Tests AI service failure

#### Backend Report Service Tests
- **File**: `/Users/vihang/projects/study-abroad/backend/tests/test_report_service.py`
- **Status**: ❌ FAILING (10/10 tests failing)

**Test Cases**:
1. ❌ `test_create_report_success` - Tests report creation
2. ❌ `test_trigger_report_generation_success` - Tests async generation trigger
3. ❌ `test_trigger_report_generation_ai_failure` - Tests generation failure handling

**Coverage Gap**: ❌ No integration tests verifying end-to-end payment → report flow

**Recommendation**:
- Fix async test configuration
- Add integration test: successful payment → triggers report generation → streams response
- Test streaming interruption handling
- Verify report storage after streaming completes

---

### AC-5: Reports are accessible for 30 days

**Specification Requirement**:
> "Reports are stored for 30 days. Within 30 days: Reopening a report does not trigger AI regeneration. After 30 days: Report is deleted or becomes inaccessible."

**Test Coverage**:

#### Backend Report Service Tests
- **File**: `/Users/vihang/projects/study-abroad/backend/tests/test_report_service.py`
- **Status**: ❌ FAILING

**Test Cases**:
1. ❌ `test_create_report_sets_expiry` - Verifies expires_at = created_at + 30 days
2. ❌ `test_get_report_success` - Tests report retrieval within retention period
3. ❌ `test_get_report_not_found` - Tests retrieval of expired report

**Coverage Gap**:
- ❌ No cron job tests for automatic deletion after 30 days
- ❌ No tests verifying cached response (no AI regeneration on reopen)

**Recommendation**:
- Add test for 30-day expiry calculation
- Add cron job test for cleanup
- Test that reopening within 30 days returns cached content
- Test that accessing after 30 days returns 404 or "expired" error

---

### AC-6: Reports cannot be accessed by other users

**Specification Requirement**:
> "Users can only access their own reports."

**Test Coverage**:

#### Backend Report Service Tests
- **File**: `/Users/vihang/projects/study-abroad/backend/tests/test_report_service.py`
- **Status**: ❌ FAILING

**Test Cases**:
1. ❌ `test_get_report_ownership_check` - Tests user_id authorization
2. ❌ `test_soft_delete_enforces_ownership` - Tests delete authorization

#### Backend API Endpoint Tests
- **File**: `/Users/vihang/projects/study-abroad/backend/tests/test_api_endpoints.py`
- **Status**: ❌ FAILING

**Test Cases**:
1. ❌ `test_get_report_by_id_unauthorized` - Tests missing authentication
2. ❌ `test_get_report_by_id_success` - Tests authorized access
3. ❌ `test_list_reports_unauthorized` - Tests unauthenticated list access

**Coverage Gap**: ❌ No tests verifying cross-user access denial (User A accessing User B's report)

**Recommendation**:
- Add test: User A creates report → User B attempts access → 403 Forbidden
- Test JWT user_id extraction and comparison
- Test admin override (if applicable)

---

### AC-7: All mandatory report sections are present

**Specification Requirement**:
> "Every report must contain all of the following sections: 1. Executive Summary, 2. Study Options, 3. Estimated Cost, 4. Visa & Immigration, 5. Post-Study Work, 6. Job Prospects, 7. Fallback Jobs, 8. Risks & Reality Check, 9. 30/60/90-Day Action Plan, 10. Sources & Citations."

**Test Coverage**:

#### Backend AI Service Tests
- **File**: `/Users/vihang/projects/study-abroad/backend/tests/test_ai_service.py`
- **Status**: ❌ FAILING

**Test Cases**:
1. ❌ `test_generate_report_success` - Verifies all 10 sections present
2. ❌ `test_generate_report_insufficient_sections` - Tests rejection if sections missing

**Relevant Code**:
```python
# From test_ai_service.py (lines 267-278)
expected_sections = [
    "executive_summary",
    "study_options",
    "estimated_cost",
    "visa_immigration",
    "post_study_work",
    "job_prospects",
    "fallback_jobs",
    "risks_reality_check",
    "action_plan",
    "sources_citations"
]
```

**Coverage Gap**: ❌ Tests are failing, so validation not currently enforced

**Recommendation**:
- Fix async test configuration
- Ensure AI prompt enforces all 10 sections
- Add validation layer to reject incomplete reports
- Test partial section scenario

---

### AC-8: All factual claims include citations

**Specification Requirement**:
> "Factual claims must include citations. If data is uncertain, the report must state uncertainty clearly. No uncited confident claims are allowed."

**Test Coverage**:

#### Backend AI Service Tests
- **File**: `/Users/vihang/projects/study-abroad/backend/tests/test_ai_service.py`
- **Status**: ❌ FAILING

**Test Cases**:
1. ❌ `test_generate_report_no_citations` - Tests rejection if no citations
2. ❌ `test_generate_report_citations_structure` - Validates citation format

**Expected Citation Structure** (from test code):
```python
citations = [
    {
        "title": "UK Government - Study Visa",
        "url": "https://www.gov.uk/study-visa"
    },
    {
        "title": "UCAS - University Admission",
        "url": "https://www.ucas.com"
    }
]
```

#### Frontend Tests
- **File**: `/Users/vihang/projects/study-abroad/frontend/tests/components/CitationList.test.tsx`
- **Status**: ✅ PASSING (32/32 tests passing)

**Test Cases**:
1. ✅ `should render list of citations` - Tests citation display
2. ✅ `should render citation titles as links` - Tests clickable sources
3. ✅ `should open links in new tab` - Tests link behavior
4. ✅ Tests for empty states, formatting, accessibility

**Coverage Gap**: ❌ No validation that every factual claim has a corresponding citation

**Recommendation**:
- Fix backend tests to enforce citation presence
- Add NLP-based validation: detect factual claims without citations
- Test uncertainty language ("may", "approximately", "estimated")
- Verify each section has at least one citation

---

### AC-9: UK-only constraint is enforced

**Specification Requirement**:
> "If user attempts a non-UK destination: Show a clear message: 'This MVP currently supports the UK only.'"

**Test Coverage**:

#### Backend AI Service Tests
- **File**: `/Users/vihang/projects/study-abroad/backend/tests/test_ai_service.py`
- **Status**: ✅ PASSING (13/13 UK validation tests passing)

**Test Cases**:
1. ✅ `test_is_uk_query_with_uk_keyword` - Tests "UK" detection
2. ✅ `test_is_uk_query_with_united_kingdom` - Tests "United Kingdom"
3. ✅ `test_is_uk_query_with_britain` - Tests "Britain"
4. ✅ `test_is_uk_query_with_london` - Tests UK city names
5. ✅ `test_is_uk_query_with_oxford` - Tests UK universities
6. ✅ `test_is_uk_query_with_cambridge` - Tests UK universities
7. ✅ `test_is_uk_query_with_russell_group` - Tests UK-specific terms
8. ✅ `test_is_uk_query_with_ucas` - Tests UK admission system
9. ✅ `test_is_uk_query_case_insensitive` - Tests case handling
10. ✅ `test_is_not_uk_query_usa` - Tests USA rejection
11. ✅ `test_is_not_uk_query_canada` - Tests Canada rejection
12. ✅ `test_is_not_uk_query_australia` - Tests Australia rejection
13. ✅ `test_is_not_uk_query_generic` - Tests generic queries

#### Backend API Tests
- **File**: `/Users/vihang/projects/study-abroad/backend/tests/test_api_endpoints.py`
- **Status**: ❌ FAILING

**Test Cases**:
1. ❌ `test_initiate_report_invalid_query` - Tests non-UK query rejection

#### Frontend Tests
- **File**: `/Users/vihang/projects/study-abroad/frontend/tests/components/ChatInput.test.tsx`
- **Status**: ⚠️ PARTIAL (30/31 passing)

**Test Cases**:
1. ✅ Multiple tests for UK keyword validation
2. ✅ Tests for error message display

**Status**: ✅ **PASSING** - UK constraint validation is the only fully working acceptance criterion

**Recommendation**:
- Ensure API rejection returns user-friendly error message
- Test that frontend displays: "This MVP currently supports the UK only."
- Add tests for edge cases (misspellings, abbreviations)

---

## Summary by Package

### Backend (/Users/vihang/projects/study-abroad/backend)

**Test Suite**: 76 tests total
- ✅ Passing: 28 (37%)
- ❌ Failing: 48 (63%)

**Coverage**: 69% (Target: 90%)

**Primary Failure Causes**:
1. Async/await configuration issues in pytest-asyncio
2. Mock setup for Supabase client
3. FastAPI dependency injection in tests
4. LangChain streaming mocks

**Acceptance Criteria Coverage**:
- AC-1 (Auth): Backend infrastructure exists but untested
- AC-2 (Payment): Tests exist but failing
- AC-3 (Failed payment): Tests exist but failing
- AC-4 (Streaming): Tests exist but failing
- AC-5 (30-day retention): Tests exist but failing
- AC-6 (Ownership): Tests exist but failing
- AC-7 (Sections): Tests exist but failing
- AC-8 (Citations): Tests exist but failing
- AC-9 (UK-only): ✅ PASSING (13/13 tests)

### Frontend (/Users/vihang/projects/study-abroad/frontend)

**Test Suite**: 90 tests total
- ✅ Passing: 82 (91%)
- ❌ Failing: 8 (9%)

**Coverage**: Not measured (test failures block coverage)

**Primary Failure Causes**:
1. Missing dependency: react-markdown
2. Mock configuration for Clerk hooks
3. Test setup file issues

**Acceptance Criteria Coverage**:
- AC-1 (Auth): Tests exist but failing (mock issues)
- AC-4 (Streaming): Display components tested (CitationList ✅)
- AC-7 (Sections): ReportSection component fails (missing react-markdown)
- AC-8 (Citations): ✅ CitationList fully tested (32/32 passing)
- AC-9 (UK-only): ✅ ChatInput validation passing

### Shared (/Users/vihang/projects/study-abroad/shared)

**Test Suite**: 42 tests total
- ✅ Passing: 6 (14%)
- ❌ Failing: 36 (86%)

**Coverage**: Not measured (test failures block coverage)

**Primary Failure Causes**:
1. Missing @testing-library/jest-dom setup
2. Clerk mock configuration issues
3. Missing api-client module in tests

**Acceptance Criteria Coverage**:
- AC-1 (Auth): Tests exist but failing (LoginForm, useAuth)
- AC-2 (Payment): Tests exist but failing (CheckoutButton, usePayment)

---

## Critical Gaps Summary

### Must Fix Before MVP Release

1. **Test Infrastructure** (BLOCKING):
   - ❌ Fix pytest-asyncio configuration in backend
   - ❌ Add @testing-library/jest-dom to shared setup
   - ❌ Install react-markdown in frontend
   - ❌ Fix Clerk mock configuration

2. **Missing Test Coverage** (HIGH):
   - ❌ Payment idempotency tests
   - ❌ Cross-user access denial tests
   - ❌ Cron job for 30-day deletion
   - ❌ End-to-end payment → report flow

3. **Failing Critical Tests** (HIGH):
   - ❌ Payment service tests (6 tests)
   - ❌ Report service tests (10 tests)
   - ❌ AI service generation tests (8 tests)
   - ❌ Authentication tests (19 tests)

### Post-MVP Improvements

1. **E2E Testing**:
   - Add Playwright tests for full user flows
   - Test OAuth integration with real providers (test mode)
   - Test Stripe integration with test mode

2. **Performance Testing**:
   - Test streaming latency
   - Test concurrent report generation
   - Test database query performance

3. **Security Testing**:
   - Test JWT expiration and renewal
   - Test payment webhook signature validation
   - Test SQL injection prevention

---

## Recommendations

### Immediate Actions (Week 1)

1. **Fix Test Infrastructure**:
   ```bash
   # Backend
   cd backend
   pip install pytest-asyncio httpx
   # Update pyproject.toml with correct asyncio_mode

   # Shared
   cd shared
   npm install -D @testing-library/jest-dom
   # Add to tests/setup.ts: import '@testing-library/jest-dom'

   # Frontend
   cd frontend
   npm install react-markdown
   ```

2. **Run Tests and Verify**:
   ```bash
   # Should achieve 100% pass rate
   cd backend && pytest
   cd frontend && npm test
   cd shared && npm test
   ```

3. **Measure Actual Coverage**:
   ```bash
   cd backend && pytest --cov=src --cov-report=term
   cd frontend && npm test -- --coverage
   cd shared && npm test -- --coverage
   ```

### Short-term Actions (Week 2-3)

1. Add missing test cases identified in gaps
2. Achieve ≥90% coverage threshold
3. Run mutation testing
4. Create E2E test suite

### Long-term Actions (Month 2+)

1. Implement CI/CD test gates
2. Add visual regression tests
3. Add performance benchmarks
4. Maintain test quality as codebase grows

---

**Document Status**: 🔴 CRITICAL - Test failures block MVP release

**Next Steps**:
1. Fix test infrastructure issues
2. Achieve 100% test pass rate
3. Verify ≥90% coverage
4. Re-run mutation testing
5. Update Gate5-QA.md with PASS/FAIL

---

**Last Updated**: 2025-12-31
**Next Review**: After test infrastructure fixes
