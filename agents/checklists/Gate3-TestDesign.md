# Gate3: Test Design Checklist

**Feature**: _{feature_name}_
**Date**: _{date}_
**Agent**: test-designer

---

## Prerequisites

- [ ] Gate2-Design.md passed
- [ ] spec.md has acceptance criteria defined
- [ ] docs/api/openapi.yaml exists (API contracts)
- [ ] docs/database/schema.sql exists (if DB changes)

---

## Phase 1: Test Infrastructure Prerequisites

**CRITICAL**: Complete this section BEFORE writing any tests. Missing infrastructure blocks all testing.

### Step 1: Identify Dependencies to Mock

Analyze your codebase and list all external dependencies:

| Dependency Type | Package/Service | Mock File | Status |
|-----------------|-----------------|-----------|--------|
| Auth provider | _{e.g., Clerk, Auth0, NextAuth}_ | tests/mocks/auth.ts | ⏳ |
| External APIs | _{e.g., Stripe, Twilio, OpenAI}_ | tests/mocks/external-apis.ts | ⏳ |
| Database | _{e.g., Supabase, Prisma, Postgres}_ | tests/mocks/database.ts | ⏳ |
| Shared packages | _{e.g., @company/config, @company/logging}_ | tests/mocks/shared-packages.ts | ⏳ |
| Environment/Config | _{e.g., env vars, feature flags}_ | tests/setup.ts | ⏳ |

### Step 2: Create Mock Infrastructure

- [ ] `tests/mocks/` directory exists
- [ ] Each dependency has a mock implementation
- [ ] Mock exports match real interface signatures exactly
- [ ] `tests/setup.ts` imports and registers all mocks
- [ ] Mock data fixtures created in `tests/fixtures/`

### Step 3: Verify Infrastructure Works

```bash
# Run test framework with no tests to verify setup
npx vitest run --passWithNoTests  # or: pytest --collect-only
```

- [ ] Test runner starts without import errors
- [ ] No "module not found" errors for mocked packages
- [ ] No configuration/environment errors
- [ ] Framework reports "0 tests" (not errors)

**BLOCKING**: Do not proceed to Phase 2 until infrastructure verification passes.

---

## Phase 2: Integration Boundary Tests

Test the boundaries between major components BEFORE unit tests.

### Identify Architecture Boundaries

| Boundary | Components | Risk Level | Test File |
|----------|------------|------------|-----------|
| Auth → API | _{auth provider → api client}_ | HIGH | tests/integration/auth-api.test.ts |
| Frontend → Backend | _{fetch calls → API routes}_ | HIGH | tests/integration/api-contracts.test.ts |
| App → Database | _{repositories → database}_ | MEDIUM | tests/integration/database.test.ts |
| Config → Runtime | _{config loader → app code}_ | MEDIUM | tests/integration/config.test.ts |

### Boundary Test Requirements

For each HIGH risk boundary:
- [ ] Integration test file exists
- [ ] Happy path tested (data flows correctly)
- [ ] Error path tested (failures handled gracefully)
- [ ] Both sides of boundary verified

### Example Boundary Test Pattern

```typescript
// tests/integration/auth-api.test.ts
describe('Auth → API Integration', () => {
  it('authenticated requests include auth header', async () => {
    // Setup: Mock auth to return token
    // Action: Call API method
    // Assert: Request included Authorization header
  });

  it('unauthenticated requests are rejected', async () => {
    // Setup: Clear auth state
    // Action: Call protected endpoint
    // Assert: 401 response received
  });
});
```

---

## Phase 3: Environment Matrix Testing

Test code in all environments where it will run.

### Identify Target Environments

| Environment | Characteristics | Test Config |
|-------------|-----------------|-------------|
| Server (Node.js) | Full env vars, no window | `@vitest-environment node` |
| Client (Browser) | Limited env, window exists | `@vitest-environment jsdom` |
| Edge (if applicable) | Restricted APIs | `@vitest-environment edge-runtime` |

### Environment-Specific Tests

- [ ] Server-only code tested in Node environment
- [ ] Client-only code tested in jsdom environment
- [ ] Shared code tested in both environments
- [ ] Environment detection logic tested

### Example Environment Tests

```typescript
// tests/environments/config-client.test.ts
/**
 * @vitest-environment jsdom
 */
describe('Config in Client Environment', () => {
  it('initializes without server-only variables', () => {
    // Server vars (DATABASE_URL, API_KEYS) not required
  });
});

// tests/environments/config-server.test.ts
/**
 * @vitest-environment node
 */
describe('Config in Server Environment', () => {
  it('requires server variables', () => {
    // Server vars must be present
  });
});
```

---

## Phase 4: Acceptance Criteria Coverage

Map each acceptance criterion from spec.md to tests:

| AC ID | Description | Test File | Test Function | Status |
|-------|-------------|-----------|---------------|--------|
| AC-1  | _{description}_ | _{path}_ | _{function}_ | ⏳/✅/❌ |
| AC-2  | _{description}_ | _{path}_ | _{function}_ | ⏳/✅/❌ |

---

## Phase 5: Unit Test Categories

### Unit Tests
- [ ] Backend services have unit tests
- [ ] Frontend components have unit tests
- [ ] Shared packages have unit tests
- [ ] Each unit test uses mocks (no real dependencies)

### Edge Cases
- [ ] Invalid input handling tested
- [ ] Error scenarios tested
- [ ] Boundary conditions tested
- [ ] Empty/null states tested

---

## Phase 6: Test Quality Standards

- [ ] Tests are deterministic (no flaky tests)
- [ ] Tests are independent (can run in any order)
- [ ] Tests have clear assertions (one concept per test)
- [ ] Tests have descriptive names (describe what, not how)
- [ ] Test data fixtures are defined and reusable

---

## TDD Verification

- [ ] Tests written BEFORE implementation code
- [ ] All tests initially FAIL (RED phase)
- [ ] Tests verify behavior, not implementation details

---

## Artifacts Created

- [ ] `tests/mocks/` - Mock implementations
- [ ] `tests/fixtures/` - Test data
- [ ] `tests/setup.ts` - Test configuration
- [ ] `tests/integration/` - Boundary tests
- [ ] `docs/testing/test-strategy.md` - Test approach
- [ ] `docs/testing/acceptance-criteria-mapping.md` - AC traceability

---

## Gate Result

**Status**: ⏳ PENDING | ✅ PASS | ❌ FAIL

**Phase Completion**:
| Phase | Status |
|-------|--------|
| 1. Test Infrastructure | ⏳/✅/❌ |
| 2. Integration Boundaries | ⏳/✅/❌ |
| 3. Environment Matrix | ⏳/✅/❌ |
| 4. AC Coverage | ⏳/✅/❌ |
| 5. Unit Tests | ⏳/✅/❌ |
| 6. Quality Standards | ⏳/✅/❌ |

**Summary**:
- Test infrastructure verified: _{yes/no}_
- Boundaries tested: _{count}_
- Environments covered: _{list}_
- Acceptance criteria mapped: _{count}/{total}_
- Estimated coverage: _{percent}_

**Notes**:
_{any issues, decisions, or blockers}_

---

**Reviewed by**: test-designer agent
**Date**: _{date}_
