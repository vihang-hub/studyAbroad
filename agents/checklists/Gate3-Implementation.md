# Gate 3: Code Implementation Standards

**Purpose**: Verify implementation meets Constitution coding standards and matches design.

**When**: After implementation completes, before testing phase.

**Owner**: Implementation Coder / Code Reviewer

---

## PASS/FAIL Criteria

### PASS Requirements (All must be true)

- [ ] **All tasks completed** from `specs/[###-feature-name]/tasks.md`
  - Every checkbox marked complete
  - No skipped tasks without justification

- [ ] **Code follows Constitution naming conventions** (Section 5)
  - PascalCase for React/Next.js components
  - kebab-case for directories and filenames
  - snake_case for database tables/columns
  - Consistent across frontend and backend

- [ ] **TypeScript strict mode enabled** (Section 1)
  - `tsconfig.json` has `"strict": true`
  - No `any` types without explicit justification
  - All props/functions typed

- [ ] **Python type hints present** (Section 1)
  - Python 3.12+ compatible
  - Function signatures typed
  - Mypy or similar linter passing

- [ ] **Clean Code principles applied** (Section 3)
  - Functions small and single-responsibility
  - Pure functions where possible
  - Immutability preferred (map/filter/reduce over loops)
  - No "clever" code without comments

- [ ] **ESLint Airbnb rules passing** (Section 3)
  - Zero linting errors
  - Warnings documented with justification

- [ ] **No secrets in code** (Section 2, Section 6)
  - API keys in secret manager only
  - No hardcoded credentials
  - Environment variables for all sensitive config

- [ ] **Logging implemented** (Section 2)
  - Authentication events logged
  - API anomalies logged
  - Centralized logging configured

- [ ] **File structure matches plan.md**
  - Code organized per Project Structure section
  - No surprise directories or files
  - Test structure matches (contract/, integration/, unit/)

### FAIL Conditions (Any triggers FAIL)

- Tasks incomplete or skipped without ADR
- Naming conventions violated (camelCase dirs, snake_case components, etc.)
- TypeScript strict mode disabled or `any` types widespread
- Python without type hints
- Secrets hardcoded in frontend or backend
- Linting errors present
- Code structure deviates from plan.md without justification

---

## Remediation Steps (If FAIL)

**Naming Convention Violations**:
1. Create file rename mapping
2. Use IDE refactoring tools to bulk rename
3. Update imports/references
4. Re-run linter to verify

**Secrets in Code**:
1. IMMEDIATELY remove from code and git history
2. Rotate compromised secrets
3. Move to secret manager (Vercel env vars, GCP Secret Manager)
4. Update deployment config

**Linting Errors**:
1. Run `npm run lint` or `flake8`/`mypy`
2. Fix errors or justify with inline comments
3. Re-run until clean

**Incomplete Tasks**:
1. Review tasks.md checklist
2. Either: Complete remaining tasks OR create ADR explaining why skipped
3. Update tasks.md with status

**Structure Mismatch**:
1. Compare actual file tree to plan.md Project Structure
2. Either: Refactor to match plan OR update plan.md with ADR
3. Ensure consistency

---

## Code Review Checklist

Additional human review points:

- [ ] No TODO/FIXME comments without issue tracking
- [ ] Error handling comprehensive (try/catch, error boundaries)
- [ ] Input validation on all user data
- [ ] No console.log in production code
- [ ] Dependencies match package.json/requirements.txt
- [ ] No commented-out code blocks
- [ ] Functions < 50 lines (guideline, not hard rule)

---

## Output

**If PASS**:
- Code ready for testing phase
- Proceed to test development and Gate 4

**If FAIL**:
- Document violations with file paths and line numbers
- Assign remediation tasks
- Re-validate after fixes

---

## Traceability Note

Gate 3 approval confirms implementation traces to tasks.md and plan.md. Every file created should map to a task ID.

---

**Last Updated**: 2025-12-29 | **Constitution Version**: 1.0.0
