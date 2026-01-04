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
