#!/bin/bash

#===============================================================================
# Speckit + Superpowers System Installer
#===============================================================================
#
# This script sets up the complete Speckit development workflow system with:
# - Session state management (checkpoint/resume)
# - Specialized agents (architect, designer, coder, qa-tester, etc.)
# - Quality gate checklists (Gate0-Gate8)
# - Superpowers skill integration
# - Graceful stop/resume commands
#
# Usage:
#   ./install-speckit-system.sh [project-root] [feature-name]
#
# Examples:
#   ./install-speckit-system.sh                           # Current dir, default feature
#   ./install-speckit-system.sh ~/projects/my-app         # Specific project
#   ./install-speckit-system.sh . my-feature-001          # Current dir, named feature
#
# Requirements:
#   - Claude Code installed
#   - Git repository initialized
#
# After installation:
#   1. Run: /primer (to see status)
#   2. Run: /speckit.specify (to create specification)
#   3. Say: "Start implementation" (to run automated pipeline)
#
#===============================================================================

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
PROJECT_ROOT="${1:-.}"
FEATURE_NAME="${2:-001-initial-feature}"
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
DATE_SIMPLE=$(date +"%Y-%m-%d")

echo -e "${BLUE}"
echo "╔═══════════════════════════════════════════════════════════════════╗"
echo "║         Speckit + Superpowers System Installer                    ║"
echo "╠═══════════════════════════════════════════════════════════════════╣"
echo "║  Project: $PROJECT_ROOT"
echo "║  Feature: $FEATURE_NAME"
echo "╚═══════════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Resolve to absolute path
PROJECT_ROOT=$(cd "$PROJECT_ROOT" && pwd)
echo -e "${YELLOW}Installing to: $PROJECT_ROOT${NC}"

# Create directory structure
echo -e "\n${GREEN}Creating directory structure...${NC}"

mkdir -p "$PROJECT_ROOT/.claude/commands"
mkdir -p "$PROJECT_ROOT/.specify/session/checkpoints"
mkdir -p "$PROJECT_ROOT/.specify/session/logs"
mkdir -p "$PROJECT_ROOT/.specify/memory"
mkdir -p "$PROJECT_ROOT/.specify/templates"
mkdir -p "$PROJECT_ROOT/.specify/scripts/bash"
mkdir -p "$PROJECT_ROOT/agents/definitions"
mkdir -p "$PROJECT_ROOT/agents/checklists"
mkdir -p "$PROJECT_ROOT/specs/$FEATURE_NAME"
mkdir -p "$PROJECT_ROOT/docs/adr"
mkdir -p "$PROJECT_ROOT/docs/api"
mkdir -p "$PROJECT_ROOT/docs/architecture"
mkdir -p "$PROJECT_ROOT/docs/testing"

echo "  ✓ Directories created"

#===============================================================================
# Create Agent Definitions
#===============================================================================
echo -e "\n${GREEN}Creating agent definitions...${NC}"

# Architect Agent
cat > "$PROJECT_ROOT/agents/definitions/architect.md" << 'EOF'
You are the **Architect** agent for this repository.

You must follow all active repo skills:
- SpeckitGovernance
- QualityGates
- RagCitationsIntegrity
- SecurityBaselineNIST
And treat `specs/constitution.md` as supreme authority.

Responsibilities:
- Define system boundaries and architecture decisions.
- Ensure stateless/autoscaling principles and data lifecycle constraints are addressed.
- Produce explicit decisions (no implicit assumptions).

Required outputs:
- docs/architecture/system-overview.md
- docs/diagrams/system.mmd (Mermaid)
- docs/adr/ADR-0001-<title>.md (and subsequent ADRs as needed)
- docs/threat-model.md (high-level)

Completion:
- Create/update agents/checklists/Gate1-Architecture.md if missing.
- End with Gate1 PASS/FAIL and link to produced files.
EOF

# Designer Agent
cat > "$PROJECT_ROOT/agents/definitions/designer.md" << 'EOF'
You are the **Designer** agent for this repository.

Follow all active repo skills and `specs/constitution.md`.

Responsibilities:
- Convert approved specs + architecture into implementable design artifacts.
- Define API contracts, UI flows, and data schema.

Required outputs:
- docs/api/openapi.yaml (or .json)
- docs/ui/flows.md
- docs/data/schema.md

Completion:
- Create/update agents/checklists/Gate2-Design.md if missing.
- End with Gate2 PASS/FAIL and link to produced files.
EOF

# Test Designer Agent
cat > "$PROJECT_ROOT/agents/definitions/test-designer.md" << 'EOF'
You are the **Test-Designer** agent for this repository.

Follow all active repo skills and `specs/constitution.md`.

**Approach**: Test-Driven Development (TDD) - Write tests BEFORE implementation.

Responsibilities:
- Create test cases from acceptance criteria in spec.md
- Map each acceptance criterion to one or more test cases
- Write test stubs that FAIL initially (no implementation exists yet)
- Ensure comprehensive coverage of happy paths and edge cases
- Define test data fixtures and mocks

Required outputs:
- docs/testing/test-strategy.md (test pyramid, approach)
- docs/testing/acceptance-criteria-mapping.md (AC → test traceability)
- backend/tests/test_{feature}.py (pytest test files)
- frontend/tests/{feature}/*.test.tsx (Vitest test files)
- shared/tests/{package}/*.test.ts (for shared package changes)

Test Requirements (from constitution):
- Coverage target: ≥90%
- Mutation score target: >80%
- Test pyramid: 80% unit, 15% integration, 5% E2E

Completion:
- Create/update agents/checklists/Gate3-TestDesign.md if missing.
- End with Gate3 PASS/FAIL and summary of tests created.
EOF

# Coder Agent
cat > "$PROJECT_ROOT/agents/definitions/coder.md" << 'EOF'
You are the **Coder** agent for this repository.

Follow all active repo skills and `specs/constitution.md`.

Responsibilities:
- Implement tasks strictly from specs/tasks/ and approved design docs.
- Write **unit tests** alongside implementation.
- Do not introduce undocumented UI/API behavior.

Required outputs:
- Implementation changes + unit tests
- Update docs only if required by the spec/plan

Completion:
- Create/update agents/checklists/Gate4-Implementation.md if missing.
- End with Gate4 PASS/FAIL and link to relevant files/commits.
EOF

# QA Tester Agent
cat > "$PROJECT_ROOT/agents/definitions/qa-tester.md" << 'EOF'
You are the **QA-Tester** agent for this repository.

Follow all active repo skills and `specs/constitution.md`.

Responsibilities:
- Execute the test suite (unit/integration/e2e as defined for the project).
- Produce an **independent** test run report with evidence.
- Do not claim "passed" without real command output + artifacts.

Required outputs:
- docs/testing/test-run-report.md (commands, exit codes, key output, artifact locations)
- docs/testing/coverage.md (coverage metrics and how produced)
- docs/testing/mutation.md (mutation score and how produced, if applicable)

Completion:
- Create/update agents/checklists/Gate5-QA.md if missing.
- End with Gate5 PASS/FAIL and include actual metrics.
EOF

# Validator Agent
cat > "$PROJECT_ROOT/agents/definitions/validator.md" << 'EOF'
You are the **Validator** agent for this repository.

Follow all active repo skills and `specs/constitution.md`.

Responsibilities:
- Verify implementation matches specification 100%.
- Check traceability: every AC has a passing test.
- Ensure no hidden features exist.

Required outputs:
- docs/compliance-summary.md (verification matrix)
- Update agents/checklists/Gate6-Validation.md

Completion:
- End with Gate6 PASS/FAIL and evidence for each claim.
EOF

# Security Gate Engineer Agent
cat > "$PROJECT_ROOT/agents/definitions/security-gate-engineer.md" << 'EOF'
You are the **Security Gate Engineer** agent for this repository.

Follow all active repo skills and `specs/constitution.md`.

Responsibilities:
- Perform security audit of implementation.
- Check for OWASP Top 10 vulnerabilities.
- Verify secret management and authentication.

Required outputs:
- docs/deployment/security-checklist.md
- SBOM (software bill of materials) if needed
- Update agents/checklists/Gate7-Security.md

Completion:
- End with Gate7 PASS/FAIL and audit summary.
EOF

# Documentation Agent
cat > "$PROJECT_ROOT/agents/definitions/documentation.md" << 'EOF'
You are the **Documentation** agent for this repository.

Follow all active repo skills and `specs/constitution.md`.

Responsibilities:
- Create and maintain accurate, concise documentation
- Ensure API documentation matches implementation
- Document code with appropriate JSDoc/docstrings
- Keep README files up to date
- Document setup and deployment procedures

Required outputs (create/update as needed):
- README.md (project overview, quick start)
- docs/SETUP.md (detailed setup instructions)
- docs/api/openapi.yaml (complete API specification)
- JSDoc comments on all exported TypeScript functions
- Python docstrings on all public functions/classes

Documentation Principles:
- Accurate > Comprehensive (never document incorrectly)
- Concise > Verbose (respect reader's time)
- Examples > Explanations (show, don't just tell)
- Current > Historical (remove outdated content)

Do NOT:
- Over-document internal implementation details
- Add comments that repeat what code already says
- Create documentation for documentation's sake
- Use marketing language or superlatives

Completion:
- End with "Documentation: COMPLETE" and list of files updated.
EOF

# DevOps Agent
cat > "$PROJECT_ROOT/agents/definitions/devops-deployment-engineer.md" << 'EOF'
You are the **DevOps Deployment Engineer** agent for this repository.

Follow all active repo skills and `specs/constitution.md`.

Responsibilities:
- Prepare deployment configurations.
- Verify builds succeed.
- Manage CI/CD pipelines.

Required outputs:
- Infrastructure configuration files
- CI/CD workflow files
- Deployment documentation

Completion:
- Create/update agents/checklists/Gate8-Deployment.md if missing.
- End with Gate8 PASS/FAIL and deployment URL (if deployed).
EOF

echo "  ✓ Agent definitions created (8 agents)"

#===============================================================================
# Create Gate Checklists
#===============================================================================
echo -e "\n${GREEN}Creating gate checklists...${NC}"

# Gate0 - PreSpec
cat > "$PROJECT_ROOT/agents/checklists/Gate0-PreSpec.md" << 'EOF'
# Gate0: Pre-Specification Checklist

**Feature**: _{feature_name}_
**Date**: _{date}_

## Prerequisites

- [ ] Project repository exists
- [ ] Constitution defined (.specify/memory/constitution.md)
- [ ] User requirements gathered

## Specification Readiness

- [ ] Problem statement clear
- [ ] Target users identified
- [ ] Success criteria defined
- [ ] Scope boundaries established
- [ ] Out of scope items listed

## Gate Result

**Status**: ⏳ PENDING | ✅ PASS | ❌ FAIL

---
**Reviewed by**: _{agent/human}_
**Date**: _{date}_
EOF

# Gate1 - Architecture
cat > "$PROJECT_ROOT/agents/checklists/Gate1-Architecture.md" << 'EOF'
# Gate1: Architecture Checklist

**Feature**: _{feature_name}_
**Date**: _{date}_
**Agent**: architect

## Prerequisites

- [ ] Gate0-PreSpec.md passed
- [ ] spec.md exists and is approved

## Architecture Artifacts

- [ ] docs/architecture/system-overview.md created
- [ ] System boundaries defined
- [ ] Component interactions documented
- [ ] Data flow diagrams created
- [ ] Technology choices justified

## ADRs (Architecture Decision Records)

- [ ] ADR-0001 created for first major decision
- [ ] Each decision has rationale documented
- [ ] Alternatives considered and rejected documented

## Security

- [ ] docs/threat-model.md created
- [ ] OWASP Top 10 considered
- [ ] Authentication approach defined
- [ ] Authorization approach defined

## Gate Result

**Status**: ⏳ PENDING | ✅ PASS | ❌ FAIL

---
**Reviewed by**: architect agent
**Date**: _{date}_
EOF

# Gate2 - Design
cat > "$PROJECT_ROOT/agents/checklists/Gate2-Design.md" << 'EOF'
# Gate2: Design Checklist

**Feature**: _{feature_name}_
**Date**: _{date}_
**Agent**: designer

---

## Prerequisites

- [ ] Gate1-Architecture.md passed
- [ ] spec.md approved with acceptance criteria
- [ ] System overview and ADRs exist

---

## API Design

### OpenAPI Specification

- [ ] `docs/api/openapi.yaml` exists
- [ ] All endpoints documented
- [ ] Request/response schemas defined
- [ ] Authentication requirements specified
- [ ] Error responses documented

### Endpoint Inventory

| Endpoint | Method | Auth Required | Request Schema | Response Schema |
|----------|--------|---------------|----------------|-----------------|
| _{path}_ | GET/POST/etc | Yes/No | _{schema}_ | _{schema}_ |

---

## UI/UX Design

### User Flows

- [ ] `docs/ui/flows.md` exists
- [ ] Primary user journey documented
- [ ] Error states designed
- [ ] Loading states designed
- [ ] Edge cases covered

---

## Data Design

### Schema Definition

- [ ] `docs/data/schema.md` exists
- [ ] All entities documented
- [ ] Relationships defined
- [ ] Indexes planned

### Access Control

- [ ] Row Level Security (RLS) policies defined
- [ ] User isolation documented

---

## Contract Testing Requirements

**CRITICAL**: Contracts must be defined BEFORE implementation to prevent frontend/backend mismatches.

### API Path Contracts

| Frontend Path | Backend Route | Match | Notes |
|---------------|---------------|-------|-------|
| _{path}_ | _{route}_ | ✅/❌ | _{notes}_ |

### Authentication Contract

| Aspect | Specification |
|--------|---------------|
| Header Name | `Authorization` |
| Header Format | `Bearer {token}` |
| Token Provider | _{provider}_ |
| Token Retrieval | _{method}_ |

### Contract Verification Approach

- [ ] **Generated Types**: Types generated from OpenAPI spec (recommended)
- [ ] **Contract Tests**: Tests verify contracts at build time
- [ ] **Manual Verification**: Types manually kept in sync

---

## Gate Result

**Status**: ⏳ PENDING | ✅ PASS | ❌ FAIL

**Contract Status**:
| Contract Type | Status |
|---------------|--------|
| API Paths | ✅/❌ |
| Request/Response | ✅/❌ |
| Authentication | ✅/❌ |

---
**Reviewed by**: designer agent
**Date**: _{date}_
EOF

# Gate3 - Test Design
cat > "$PROJECT_ROOT/agents/checklists/Gate3-TestDesign.md" << 'EOF'
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
EOF

# Gate4 - Implementation
cat > "$PROJECT_ROOT/agents/checklists/Gate4-Implementation.md" << 'EOF'
# Gate4: Implementation Checklist

**Feature**: _{feature_name}_
**Date**: _{date}_
**Agent**: coder

---

## Prerequisites

- [ ] Gate3-TestDesign.md passed
- [ ] Test infrastructure verified (mocks, fixtures, setup)
- [ ] Tests exist and FAIL (TDD RED phase)
- [ ] tasks.md generated with implementation tasks

---

## Implementation Rules

### Core Requirements

- [ ] Code implements ONLY what is specified in specs/
- [ ] Unit tests added/updated for all changes
- [ ] No secrets committed (use environment variables)
- [ ] No undocumented features or "improvements"

### TDD Compliance

- [ ] Each task follows RED → GREEN → REFACTOR
- [ ] Tests pass after implementation (GREEN phase)
- [ ] Code refactored while keeping tests green

---

## Continuous Validation Checkpoints

**CRITICAL**: Validation must pass after every implementation batch. Errors accumulate and become harder to fix.

### Checkpoint Commands

Run these commands after every 3-5 tasks (or after each complex task):

**TypeScript/JavaScript Projects:**
```bash
# Type checking - MUST exit 0
npm run typecheck   # or: npx tsc --noEmit

# Linting - MUST exit 0 (warnings OK)
npm run lint        # or: npx eslint .

# Build verification - MUST exit 0
npm run build       # or: npx next build
```

**Python Projects:**
```bash
# Type checking - MUST exit 0
mypy src/           # or: pyright src/

# Linting - MUST exit 0
ruff check src/     # or: flake8 src/

# Import verification
python -c "from src import main"
```

**Multi-Package/Monorepo:**
```bash
# Run for each package
cd frontend && npm run typecheck && npm run lint && npm run build
cd backend && ruff check src && mypy src
cd shared && npm run typecheck && npm run lint
```

### Checkpoint Frequency

| Task Complexity | Lines Changed | Checkpoint After |
|-----------------|---------------|------------------|
| Simple | < 50 LOC | Every 5 tasks |
| Medium | 50-200 LOC | Every 3 tasks |
| Complex | > 200 LOC | Every task |
| Refactoring | Any | Every task |

### Validation Log

Track checkpoint results:

| Checkpoint | Tasks | TypeCheck | Lint | Build | Tests | Status |
|------------|-------|-----------|------|-------|-------|--------|
| CP-1 | T001-T005 | ✅ | ✅ | ✅ | ✅ | PASS |
| CP-2 | T006-T010 | _{result}_ | _{result}_ | _{result}_ | _{result}_ | _{status}_ |

### Enforcement Rules

**BLOCKING**: If any validation fails:

1. **STOP** implementation immediately
2. **FIX** the validation error before continuing
3. **RE-RUN** all validation commands
4. **VERIFY** all pass before proceeding

**NO DEFERRAL** is allowed for:
- Type errors (breaks build)
- Import errors (breaks runtime)
- Build failures (blocks deployment)

**Deferral allowed ONLY for** (with documented rationale):
- Linting warnings (not errors)
- Style issues
- Documentation gaps

---

## Task Execution Tracking

| Task ID | Description | Tests Pass | Validation | Status |
|---------|-------------|------------|------------|--------|
| T001 | _{description}_ | ✅/❌ | ✅/❌ | ⏳/✅/❌ |
| T002 | _{description}_ | ✅/❌ | ✅/❌ | ⏳/✅/❌ |

---

## Code Quality Standards

### Clean Code
- [ ] Functions are small and single-responsibility
- [ ] Variable names are descriptive
- [ ] No magic numbers or strings
- [ ] Complex logic has comments explaining WHY

### Architecture
- [ ] Code follows existing patterns in codebase
- [ ] New patterns documented in ADR if introduced
- [ ] Dependencies injected, not hardcoded
- [ ] No circular dependencies

### Security
- [ ] Input validation on all user data
- [ ] No SQL injection vulnerabilities
- [ ] No XSS vulnerabilities
- [ ] Secrets in environment variables only

---

## Commit Discipline

### Commit Frequency
- [ ] Commit after each logical unit of work
- [ ] Each commit passes all validations
- [ ] Commit messages follow conventional format

### Commit Message Format
```
type(scope): description

- Detail 1
- Detail 2

Refs: T001, T002
```

Types: `feat`, `fix`, `refactor`, `test`, `docs`, `chore`

---

## Progress Checkpoints

### Batch 1 (Tasks T001-T010)
- [ ] All tasks completed
- [ ] Validation checkpoint passed
- [ ] Tests passing
- [ ] Committed

### Batch 2 (Tasks T011-T020)
- [ ] All tasks completed
- [ ] Validation checkpoint passed
- [ ] Tests passing
- [ ] Committed

_(Add more batches as needed)_

---

## Final Validation

Before marking Gate4 complete:

```bash
# Full test suite
npm test            # or: pytest

# Full type check
npm run typecheck   # or: mypy src/

# Full lint
npm run lint        # or: ruff check src/

# Full build
npm run build       # or: python -m build
```

- [ ] All tests pass
- [ ] Type checking passes
- [ ] Linting passes (0 errors)
- [ ] Build succeeds
- [ ] No uncommitted changes

---

## Gate Result

**Status**: ⏳ PENDING | ✅ PASS | ❌ FAIL

**Summary**:
- Tasks completed: _{count}/{total}_
- Validation checkpoints passed: _{count}_
- Tests passing: _{count}/{total}_
- Coverage: _{percent}_

**Validation Results**:
| Check | Result |
|-------|--------|
| TypeCheck | ✅/❌ |
| Lint | ✅/❌ |
| Build | ✅/❌ |
| Tests | ✅/❌ |

**Notes**:
_{any issues, decisions, deferred items with rationale}_

---

**Reviewed by**: coder agent
**Date**: _{date}_
EOF

# Gate5 - QA
cat > "$PROJECT_ROOT/agents/checklists/Gate5-QA.md" << 'EOF'
# Gate5: QA Checklist

**Feature**: _{feature_name}_
**Date**: _{date}_
**Agent**: qa-tester

## Prerequisites

- [ ] Gate4-Implementation.md passed

## Test Execution

- [ ] All unit tests executed
- [ ] All integration tests executed
- [ ] E2E tests executed (if applicable)

## Metrics

| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
| Coverage | ≥90% | _{X}%_ | ⏳/✅/❌ |
| Mutation Score | >80% | _{Y}%_ | ⏳/✅/❌ |
| Tests Passing | 100% | _{Z}%_ | ⏳/✅/❌ |

## Evidence

- [ ] docs/testing/test-run-report.md created
- [ ] docs/testing/coverage.md updated
- [ ] docs/testing/mutation.md updated

## Gate Result

**Status**: ⏳ PENDING | ✅ PASS | ❌ FAIL

---
**Reviewed by**: qa-tester agent
**Date**: _{date}_
EOF

# Gate6 - Validation
cat > "$PROJECT_ROOT/agents/checklists/Gate6-Validation.md" << 'EOF'
# Gate6: Validation Checklist

**Feature**: _{feature_name}_
**Date**: _{date}_
**Agent**: validator

## Prerequisites

- [ ] Gate5-QA.md passed

## Spec Parity

- [ ] Every requirement in spec.md is implemented
- [ ] No undocumented features exist
- [ ] API matches openapi.yaml exactly

## Traceability

- [ ] Every AC has at least one test
- [ ] All tests are passing

## Documentation

- [ ] README up to date
- [ ] API docs match implementation

## Gate Result

**Status**: ⏳ PENDING | ✅ PASS | ❌ FAIL

---
**Reviewed by**: validator agent
**Date**: _{date}_
EOF

# Gate7 - Security
cat > "$PROJECT_ROOT/agents/checklists/Gate7-Security.md" << 'EOF'
# Gate7: Security Checklist

**Feature**: _{feature_name}_
**Date**: _{date}_
**Agent**: security-gate-engineer

## Prerequisites

- [ ] Gate6-Validation.md passed

## Secret Management

- [ ] No hardcoded secrets in code
- [ ] Secrets in environment/secret manager
- [ ] .env files in .gitignore

## Authentication & Authorization

- [ ] Auth implementation secure
- [ ] JWT/session handling correct
- [ ] RLS policies enforce isolation

## Input Validation

- [ ] All inputs validated
- [ ] SQL injection prevented
- [ ] XSS prevented

## Dependencies

- [ ] npm audit clean (or issues documented)
- [ ] pip-audit clean (or issues documented)
- [ ] No critical vulnerabilities

## Gate Result

**Status**: ⏳ PENDING | ✅ PASS | ❌ FAIL

---
**Reviewed by**: security-gate-engineer agent
**Date**: _{date}_
EOF

# Gate8 - Deployment
cat > "$PROJECT_ROOT/agents/checklists/Gate8-Deployment.md" << 'EOF'
# Gate8: Deployment Checklist

**Feature**: _{feature_name}_
**Date**: _{date}_
**Agent**: devops-deployment-engineer

## Prerequisites

- [ ] Gate7-Security.md passed

## Build Verification

- [ ] Frontend builds successfully
- [ ] Backend builds successfully
- [ ] Docker images build (if applicable)

## Configuration

- [ ] Environment variables documented
- [ ] Secrets configured in target environment
- [ ] Database migrations ready

## CI/CD

- [ ] CI pipeline passing
- [ ] CD pipeline configured
- [ ] Rollback strategy defined

## Deployment

- [ ] Staging deployment successful
- [ ] Smoke tests passing
- [ ] Production deployment (if applicable)

## Gate Result

**Status**: ⏳ PENDING | ✅ PASS | ❌ FAIL
**Deployed to**: _{environment}_
**URL**: _{url}_

---
**Reviewed by**: devops-deployment-engineer agent
**Date**: _{date}_
EOF

# README for checklists
cat > "$PROJECT_ROOT/agents/checklists/README.md" << 'EOF'
# Quality Gate Checklists

This directory contains quality gate checklists for the development workflow.

## Gates

| Gate | Purpose | Agent |
|------|---------|-------|
| Gate0 | Pre-Specification | - |
| Gate1 | Architecture | architect |
| Gate2 | Design | designer |
| Gate3 | Test Design | test-designer |
| Gate4 | Implementation | coder |
| Gate5 | QA | qa-tester |
| Gate6 | Validation | validator |
| Gate7 | Security | security-gate-engineer |
| Gate8 | Deployment | devops-deployment-engineer |

## Usage

Each gate must pass before proceeding to the next stage.
The `/speckit.autopilot` command runs through all gates automatically.
EOF

echo "  ✓ Gate checklists created (9 gates)"

#===============================================================================
# Create Session State
#===============================================================================
echo -e "\n${GREEN}Creating session state management...${NC}"

# State JSON
cat > "$PROJECT_ROOT/.specify/session/state.json" << EOF
{
  "version": "1.0.0",
  "feature": "$FEATURE_NAME",
  "feature_path": "specs/$FEATURE_NAME",
  "last_updated": "$TIMESTAMP",
  "last_session_id": null,

  "pipeline": {
    "status": "not_started",
    "current_stage": null,
    "started_at": null,
    "completed_at": null
  },

  "gates": {
    "gate0_prespec": {
      "status": "pending",
      "completed_at": null,
      "agent": null,
      "artifacts": []
    },
    "gate1_architecture": {
      "status": "pending",
      "completed_at": null,
      "agent": "architect",
      "artifacts": []
    },
    "gate2_design": {
      "status": "pending",
      "completed_at": null,
      "agent": "designer",
      "artifacts": []
    },
    "gate3_testdesign": {
      "status": "pending",
      "completed_at": null,
      "agent": "test-designer",
      "artifacts": []
    },
    "gate4_implementation": {
      "status": "pending",
      "completed_at": null,
      "agent": "coder",
      "progress": {
        "total_tasks": 0,
        "completed_tasks": 0,
        "percentage": 0
      },
      "current_phase": null,
      "last_completed_task": null,
      "next_task": null,
      "blockers": []
    },
    "gate5_qa": {
      "status": "pending",
      "completed_at": null,
      "agent": "qa-tester",
      "metrics": {
        "backend_coverage": null,
        "frontend_coverage": null,
        "shared_coverage": null,
        "mutation_score": null
      },
      "thresholds": {
        "coverage": 90,
        "mutation": 80
      }
    },
    "gate6_validation": {
      "status": "pending",
      "completed_at": null,
      "agent": "validator",
      "artifacts": []
    },
    "gate7_security": {
      "status": "pending",
      "completed_at": null,
      "agent": "security-gate-engineer",
      "artifacts": []
    },
    "gate8_deployment": {
      "status": "pending",
      "completed_at": null,
      "agent": "devops-deployment-engineer",
      "artifacts": []
    }
  },

  "tasks": {
    "remaining": [],
    "in_progress": [],
    "blocked": []
  },

  "recent_activity": [],

  "recommendations": {
    "next_action": "Create specification with /speckit.specify",
    "suggested_agent": null,
    "estimated_effort": null,
    "blockers_to_resolve": []
  },

  "resume_context": {
    "next_task": null,
    "next_task_description": null,
    "context_notes": "New project - start with /primer",
    "last_test_run": null,
    "uncommitted_work": false,
    "wip_commit": null
  },

  "session_end": null
}
EOF

# Session README
cat > "$PROJECT_ROOT/.specify/session/README.md" << 'EOF'
# Session State Management

This directory tracks implementation progress across Claude Code sessions.

## Files

- `state.json` - Current pipeline state (auto-updated)
- `checkpoints/` - Snapshots at each gate completion
- `logs/` - Execution logs for debugging

## How It Works

1. **Checkpoint on completion**: After each gate passes, state is saved
2. **Resume on primer**: `/primer` reads state and offers to continue
3. **Manual override**: User can restart from any stage

## State Schema

See `state.json` for current progress.
EOF

# Create empty sessions log
touch "$PROJECT_ROOT/.specify/session/logs/sessions.jsonl"

echo "  ✓ Session state created"

#===============================================================================
# Create Claude Commands
#===============================================================================
echo -e "\n${GREEN}Creating Claude commands...${NC}"

# Primer command
cat > "$PROJECT_ROOT/.claude/commands/primer.md" << 'PRIMER_EOF'
# Prime Context for Claude Code

## Step 1: Load Session State

**FIRST**, read the session state file to understand where we left off:

```
.specify/session/state.json
```

Parse and display the following status table:

```
╔═══════════════════════════════════════════════════════════════════╗
║                    SESSION RESUME STATUS                          ║
╠═══════════════════════════════════════════════════════════════════╣
║ Feature: {feature}                                                ║
║ Last Activity: {last_updated}                                     ║
║ Pipeline Status: {pipeline.status}                                ║
╠═══════════════════════════════════════════════════════════════════╣
║ GATE STATUS                                                       ║
╠════════════════════╦══════════╦═══════════════════════════════════╣
║ Gate               ║ Status   ║ Details                           ║
╠════════════════════╬══════════╬═══════════════════════════════════╣
║ Gate0 PreSpec      ║ ✅/⏳/❌ ║ spec.md                           ║
║ Gate1 Architecture ║ ✅/⏳/❌ ║ {artifact_count} artifacts        ║
║ Gate2 Design       ║ ✅/⏳/❌ ║ {artifact_count} artifacts        ║
║ Gate3 Test Design  ║ ✅/⏳/❌ ║ TDD tests created                 ║
║ Gate4 Implementation║ ⚠️ {X}% ║ {completed}/{total} tasks         ║
║ Gate5 QA           ║ ⏳       ║ Coverage: {X}%, Mutation: {Y}%    ║
║ Gate6 Validation   ║ ⏳       ║ Pending                           ║
║ Gate7 Security     ║ ✅/⏳/❌ ║ Audit complete                    ║
║ Gate8 Deployment   ║ ⏳       ║ Pending                           ║
╚════════════════════╩══════════╩═══════════════════════════════════╝
```

## Step 2: Show Current Position

Display where we are in the pipeline:

```
Pipeline Progress:
[████████████████████░░░░] {X}% Complete

Current Stage: {current_stage}
Last Completed: {last_task}
Next Task: {next_task}

Recent Activity:
• {recent_activity[0]}
• {recent_activity[1]}
• {recent_activity[2]}
```

## Step 3: Present Resume Options

Based on the session state, present these options:

```
╔═══════════════════════════════════════════════════════════════════╗
║                     RESUME OPTIONS                                ║
╠═══════════════════════════════════════════════════════════════════╣
║                                                                   ║
║  [1] CONTINUE where we left off                                   ║
║      → Resume from: {next_task}                                   ║
║                                                                   ║
║  [2] RUN specific agent                                           ║
║      → "Use the {agent} agent to..."                              ║
║                                                                   ║
║  [3] RESTART from a specific gate                                 ║
║      → /speckit.autopilot --from={gate}                           ║
║                                                                   ║
║  [4] START new feature                                            ║
║      → /speckit.specify                                           ║
║                                                                   ║
║  [5] VIEW detailed status                                         ║
║      → Show all remaining tasks                                   ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝

What would you like to do?
```

## Quick Reference

### Available Commands:

| Command | Purpose |
|---------|---------|
| `/speckit.autopilot` | Run full automated pipeline |
| `/speckit.implement` | Execute remaining tasks |
| `/speckit.specify` | Create new specification |
| `/speckit.stop` | Graceful session end |

### Agent Shortcuts:

Say any of these to invoke a specialized agent:
- "Use the architect agent to..."
- "Use the designer agent to..."
- "Use the coder agent to..."
- "Use the qa-tester agent to..."
- "Use the validator agent to..."
- "Use the security agent to..."
- "Use the devops agent to..."
PRIMER_EOF

# Stop command
cat > "$PROJECT_ROOT/.claude/commands/speckit.stop.md" << 'STOP_EOF'
# Speckit Stop - Graceful Session End

**Trigger**: User says "stop for the day", "pause", "save and quit", or runs `/speckit.stop`

## Step 1: Save Current State

Update `.specify/session/state.json` with current progress.

## Step 2: Commit Work In Progress

If there are uncommitted changes, ask user:

```
╔═══════════════════════════════════════════════════════════════════╗
║                 UNCOMMITTED CHANGES DETECTED                       ║
╠═══════════════════════════════════════════════════════════════════╣
║  Options:                                                         ║
║  [1] Commit as WIP (recommended)                                  ║
║  [2] Stash changes                                                ║
║  [3] Leave uncommitted                                            ║
╚═══════════════════════════════════════════════════════════════════╝
```

## Step 3: Generate Session Summary

```
╔═══════════════════════════════════════════════════════════════════╗
║                    SESSION SUMMARY                                 ║
╠═══════════════════════════════════════════════════════════════════╣
║  Session: {start_time} → {end_time}                               ║
║  Feature: {feature_name}                                          ║
║                                                                   ║
║  WORK COMPLETED                                                   ║
║  • Tasks completed: {count}                                       ║
║  • Gates progressed: {list}                                       ║
║  • Files modified: {count}                                        ║
║                                                                   ║
║  TOMORROW'S STARTING POINT                                        ║
║  • Next task: {next_task}                                         ║
║  • Remaining: {count} tasks                                       ║
║                                                                   ║
║  Run /primer to resume. See you next time! 👋                     ║
╚═══════════════════════════════════════════════════════════════════╝
```

## Quick Stop

For `/speckit.stop --quick`:
1. Auto-commit as WIP
2. Save state
3. Show brief summary
STOP_EOF

echo "  ✓ Claude commands created"

#===============================================================================
# Create Constitution Template
#===============================================================================
echo -e "\n${GREEN}Creating constitution template...${NC}"

cat > "$PROJECT_ROOT/.specify/memory/constitution.md" << 'EOF'
# Project Constitution

## 1. Core Technical Stack

*Define your technology choices here*

- **Frontend**:
- **Backend**:
- **Database**:
- **Auth**:
- **Infrastructure**:

## 2. Security Framework

- All secrets in environment variables or secret manager
- HTTPS/TLS enforced
- Input validation on all endpoints
- OWASP Top 10 considered

## 3. Engineering Rigor & Testing

- **Specification Faithfulness**: 100% parity with specs/
- **Code Coverage**: ≥90%
- **Mutation Score**: >80% (if applicable)

## 4. Architectural Principles

- Stateless where possible
- Document all decisions in ADRs
- No implicit assumptions

## 5. Naming & Structure

- **Components**: PascalCase
- **Files/Directories**: kebab-case
- **Database**: snake_case
- **API**: RESTful with OpenAPI spec

## 6. Prohibited Practices

- No hardcoded secrets
- No undocumented features
- No manual deployments

## 7. Governance

This constitution supersedes all other conventions.
Changes require documented rationale.

**Version**: 1.0.0 | **Date**: {date}
EOF

echo "  ✓ Constitution template created"

#===============================================================================
# Create CLAUDE.md with Speckit Workflow Requirements
#===============================================================================
echo -e "\n${GREEN}Creating CLAUDE.md...${NC}"

cat > "$PROJECT_ROOT/CLAUDE.md" << 'EOF'
# Project Development Guidelines

## Speckit Workflow Requirements

**CRITICAL**: ALL development activities MUST be framed within the Speckit framework.

### Always Show Context

When suggesting next steps or asking questions, ALWAYS include:

```
┌─────────────────────────────────────────────────────────────────┐
│ SPECKIT CONTEXT                                                 │
├─────────────────────────────────────────────────────────────────┤
│ Current Gate: Gate{N} - {GateName}                              │
│ Agent: {agent_name}                                             │
│ Skill: {skill_name} (if applicable)                             │
│ Task: {current_task_id} - {description}                         │
└─────────────────────────────────────────────────────────────────┘
```

### Gate → Agent → Skill Mapping

| Gate | Name | Agent | Primary Skills |
|------|------|-------|----------------|
| Gate0 | Pre-Specification | - | `speckit.specify`, `superpowers:brainstorming` |
| Gate1 | Architecture | `architect` | - |
| Gate2 | Design | `designer` | `speckit.plan`, `superpowers:writing-plans` |
| Gate3 | Test Design | `test-designer` | `superpowers:test-driven-development` |
| Gate4 | Implementation | `coder` | `speckit.implement`, `superpowers:executing-plans`, `superpowers:dispatching-parallel-agents` |
| Gate5 | QA | `qa-tester` | `superpowers:systematic-debugging`, `superpowers:verification-before-completion` |
| Gate6 | Validation | `validator` | `superpowers:verification-before-completion` |
| Gate7 | Security | `security-gate-engineer` | - |
| Gate8 | Deployment | `devops-deployment-engineer` | `superpowers:finishing-a-development-branch` |

### Presenting Options

When presenting next step options, format as:

```
NEXT STEPS (Gate{N} - {GateName}):

[1] {Action description}
    → Agent: {agent}
    → Skill: {skill}
    → Command: {/command or "Use the {agent} agent to..."}

[2] {Action description}
    → Agent: {agent}
    → Skill: {skill}
    → Command: {/command}
```

### Activity Classification

Before ANY activity, determine:
1. Which gate does this belong to?
2. Which agent should handle it?
3. Which skill(s) apply?
4. Is this a new feature (→ /speckit.specify) or continuation?

### Session State

Always check `.specify/session/state.json` to understand:
- Current pipeline status
- Active gate and progress
- Next task in queue
- Recent activity

Use `/primer` at session start to load context.

### Bug Fixes and Ad-Hoc Work

Even bug fixes follow speckit:
- Simple bug → Gate4 (coder) + `superpowers:systematic-debugging`
- Test failures → Gate5 (qa-tester) + `superpowers:systematic-debugging`
- Security issue → Gate7 (security-gate-engineer)
- New feature request → Gate0 (start with /speckit.specify)

<!-- MANUAL ADDITIONS START -->
<!-- MANUAL ADDITIONS END -->
EOF

echo "  ✓ CLAUDE.md created with Speckit workflow requirements"

#===============================================================================
# Create Feature Spec Template
#===============================================================================
echo -e "\n${GREEN}Creating feature templates...${NC}"

cat > "$PROJECT_ROOT/specs/$FEATURE_NAME/spec.md" << EOF
# Specification: $FEATURE_NAME

## 1. Purpose

*Describe what this feature does and why*

## 2. Target Users

*Who will use this feature?*

## 3. Scope

### In Scope
-

### Out of Scope
-

## 4. Requirements

### Functional Requirements
1.

### Non-Functional Requirements
1.

## 5. Acceptance Criteria

| AC ID | Description | Priority |
|-------|-------------|----------|
| AC-1 | | P1 |

## 6. Data Model

*Entities and relationships*

## 7. API Surface

| Method | Endpoint | Purpose |
|--------|----------|---------|

## 8. UI/UX Requirements

*User interface requirements*

---
**Status**: Draft
**Created**: $DATE_SIMPLE
EOF

cat > "$PROJECT_ROOT/specs/$FEATURE_NAME/plan.md" << EOF
# Implementation Plan: $FEATURE_NAME

**Branch**: \`$FEATURE_NAME\`
**Date**: $DATE_SIMPLE
**Spec**: [spec.md](./spec.md)

## Summary

*Brief description of implementation approach*

## Technical Context

### Stack
- **Frontend**:
- **Backend**:
- **Database**:

## Constitution Check

- [ ] Technical Stack Alignment
- [ ] Security Framework
- [ ] Engineering Rigor
- [ ] Architectural Principles
- [ ] Naming & Structure
- [ ] Prohibited Practices

## Phase 0: Research

*Research findings*

## Phase 1: Data Model & Contracts

*Data model and API design*

## Phase 2: Implementation Tasks

*See tasks.md*

---
**Status**: Draft
EOF

cat > "$PROJECT_ROOT/specs/$FEATURE_NAME/tasks.md" << EOF
# Tasks: $FEATURE_NAME

**Input**: spec.md, plan.md
**Date**: $DATE_SIMPLE

## Format: \`[ID] [P?] Description\`

- **[P]**: Can run in parallel

---

## Phase 1: Setup

- [ ] T001 Initialize project structure
- [ ] T002 [P] Configure linting
- [ ] T003 [P] Configure testing

## Phase 2: Core Implementation

- [ ] T004 Implement core feature
- [ ] T005 Add tests

## Phase 3: Polish

- [ ] T006 Documentation
- [ ] T007 Final review

---

**Total Tasks**: 7
EOF

echo "  ✓ Feature templates created"

#===============================================================================
# Create .gitignore additions
#===============================================================================
echo -e "\n${GREEN}Updating .gitignore...${NC}"

if [ -f "$PROJECT_ROOT/.gitignore" ]; then
  # Check if our entries already exist
  if ! grep -q ".specify/session/logs" "$PROJECT_ROOT/.gitignore" 2>/dev/null; then
    cat >> "$PROJECT_ROOT/.gitignore" << 'EOF'

# Speckit session files
.specify/session/logs/*.jsonl
.specify/session/checkpoints/*
!.specify/session/checkpoints/.gitkeep
EOF
    echo "  ✓ .gitignore updated"
  else
    echo "  ✓ .gitignore already configured"
  fi
else
  cat > "$PROJECT_ROOT/.gitignore" << 'EOF'
# Speckit session files
.specify/session/logs/*.jsonl
.specify/session/checkpoints/*
!.specify/session/checkpoints/.gitkeep
EOF
  echo "  ✓ .gitignore created"
fi

# Create gitkeep
touch "$PROJECT_ROOT/.specify/session/checkpoints/.gitkeep"

#===============================================================================
# Final Summary
#===============================================================================
echo -e "\n${GREEN}"
echo "╔═══════════════════════════════════════════════════════════════════╗"
echo "║                    INSTALLATION COMPLETE                          ║"
echo "╠═══════════════════════════════════════════════════════════════════╣"
echo "║                                                                   ║"
echo "║  Created:                                                         ║"
echo "║  • 8 agent definitions (agents/definitions/)                      ║"
echo "║  • 9 gate checklists (agents/checklists/)                         ║"
echo "║  • Session state management (.specify/session/)                   ║"
echo "║  • Claude commands (.claude/commands/)                            ║"
echo "║  • Feature templates (specs/$FEATURE_NAME/)                       ║"
echo "║  • Project constitution (.specify/memory/constitution.md)         ║"
echo "║                                                                   ║"
echo "╠═══════════════════════════════════════════════════════════════════╣"
echo "║                                                                   ║"
echo "║  NEXT STEPS:                                                      ║"
echo "║                                                                   ║"
echo "║  1. Edit constitution:                                            ║"
echo "║     vim .specify/memory/constitution.md                           ║"
echo "║                                                                   ║"
echo "║  2. Start Claude Code and run:                                    ║"
echo "║     /primer                                                       ║"
echo "║                                                                   ║"
echo "║  3. Create your specification:                                    ║"
echo "║     /speckit.specify                                              ║"
echo "║                                                                   ║"
echo "║  4. Start automated implementation:                               ║"
echo "║     \"Start implementation\"                                        ║"
echo "║                                                                   ║"
echo "║  5. End your session gracefully:                                  ║"
echo "║     /speckit.stop                                                 ║"
echo "║                                                                   ║"
echo "╠═══════════════════════════════════════════════════════════════════╣"
echo "║                                                                   ║"
echo "║  OPTIONAL: Install Superpowers plugin for enhanced skills         ║"
echo "║                                                                   ║"
echo "║  In Claude Code:                                                  ║"
echo "║  /plugin marketplace add obra/superpowers-marketplace             ║"
echo "║  /plugin install superpowers@superpowers-marketplace              ║"
echo "║                                                                   ║"
echo "╚═══════════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

echo -e "\n${BLUE}Installation complete! Happy coding! 🚀${NC}\n"
