# Gate3: Test Design Checklist

**Feature**: _{feature_name}_
**Date**: _{date}_
**Agent**: test-designer

## Prerequisites

- [ ] Gate2-Design.md passed
- [ ] spec.md has acceptance criteria defined
- [ ] docs/api/openapi.yaml exists (API contracts)
- [ ] docs/database/schema.sql exists (if DB changes)

## Acceptance Criteria Coverage

For each acceptance criterion in spec.md:

| AC ID | Description | Test File | Test Function | Status |
|-------|-------------|-----------|---------------|--------|
| AC-1  | _{description}_ | _{path}_ | _{function}_ | ⏳/✅/❌ |
| AC-2  | _{description}_ | _{path}_ | _{function}_ | ⏳/✅/❌ |

## Test Categories

### Unit Tests
- [ ] Backend services have unit tests
- [ ] Frontend components have unit tests
- [ ] Shared packages have unit tests
- [ ] Mocks/stubs are properly isolated

### Integration Tests
- [ ] API endpoints have integration tests
- [ ] Database operations are tested
- [ ] External service integrations are mocked

### Edge Cases
- [ ] Invalid input handling tested
- [ ] Error scenarios tested
- [ ] Boundary conditions tested
- [ ] Empty/null states tested

## Test Quality

- [ ] Tests are deterministic (no flaky tests)
- [ ] Tests are independent (can run in any order)
- [ ] Tests have clear assertions
- [ ] Tests have descriptive names
- [ ] Test data fixtures are defined

## TDD Verification

- [ ] Tests were written BEFORE implementation
- [ ] All tests initially FAIL (proving they test real behavior)
- [ ] No implementation code exists yet for new features

## Artifacts Created

- [ ] docs/testing/acceptance-criteria-mapping.md updated
- [ ] docs/testing/test-strategy.md updated (if needed)
- [ ] Backend tests: `backend/tests/test_*.py`
- [ ] Frontend tests: `frontend/tests/**/*.test.tsx`
- [ ] Shared tests: `shared/tests/**/*.test.ts`

## Gate Result

**Status**: ⏳ PENDING | ✅ PASS | ❌ FAIL

**Summary**:
- Total acceptance criteria: _{count}_
- Tests created: _{count}_
- Coverage estimate: _{percent}_

**Notes**:
_{any issues or decisions made}_

---

**Reviewed by**: test-designer agent
**Date**: _{date}_
