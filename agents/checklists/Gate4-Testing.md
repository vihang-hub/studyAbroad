# Gate 4: Test Coverage & Quality

**Purpose**: Verify tests meet Constitution thresholds and validate implementation against spec.

**When**: After tests written, before QA validation.

**Owner**: QA Tester / Test Engineer

---

## PASS/FAIL Criteria

### PASS Requirements (All must be true)

- [ ] **Code Coverage meets threshold** (Constitution Section 3, QualityGates Skill)
  - Frontend: ≥90% statement coverage, ≥90% branch coverage
  - Backend: ≥90% statement coverage, ≥90% branch coverage
  - Coverage report exists at `docs/testing/coverage.md`

- [ ] **Mutation Score meets threshold** (Constitution Section 3, QualityGates Skill)
  - JavaScript/TypeScript: >80% mutation score (Stryker Mutator)
  - Mutation report exists at `docs/testing/mutation.md`
  - Tests demonstrate ability to catch bugs (not just pass lines)

- [ ] **Test types complete**
  - Contract tests: API schemas validated (tests/contract/ or backend/tests/contract/)
  - Integration tests: User journeys validated (tests/integration/ or backend/tests/integration/)
  - Unit tests: Component/function logic validated (tests/unit/ or backend/tests/unit/)

- [ ] **All User Stories tested** (from spec.md)
  - Each P1, P2, P3 story has corresponding test
  - Independent test criteria from spec.md verified
  - Acceptance scenarios (Given/When/Then) covered

- [ ] **All Functional Requirements tested** (from spec.md)
  - Each FR-XXX has tracing test case
  - Test names/comments reference requirement IDs

- [ ] **Edge cases tested** (from spec.md)
  - Boundary conditions validated
  - Error scenarios verified
  - Data validation tested

- [ ] **CI/CD configured** (Constitution Section 6)
  - Tests run automatically on PR
  - Coverage threshold enforced (blocks merge if <90%)
  - Mutation threshold enforced (blocks merge if ≤80%)

### FAIL Conditions (Any triggers FAIL)

- Coverage <90% for any codebase component
- Mutation score ≤80% for JS/TS
- Missing test type (contract, integration, or unit)
- User story without test coverage
- Functional requirement (FR-XXX) without test
- CI/CD not enforcing thresholds
- Tests pass but don't validate spec requirements

---

## Remediation Steps (If FAIL)

**Coverage Below Threshold**:
1. Generate coverage report: `npm run test:coverage` or `pytest --cov`
2. Identify uncovered lines/branches in report
3. Write tests for uncovered code paths
4. Re-run coverage until ≥90%

**Mutation Score Below Threshold**:
1. Run Stryker: `npx stryker run`
2. Review survived mutants in report
3. Strengthen tests to kill mutants (add assertions, test edge cases)
4. Re-run until >80%

**Missing Test Types**:
1. Review spec.md for untested scenarios
2. Create test files in appropriate directory
3. Implement tests following Given/When/Then pattern
4. Verify tests fail before implementation passes

**Untested Requirements**:
1. Create traceability matrix: FR-XXX → Test Case
2. Identify gaps (requirements without tests)
3. Write tests with comments: `// Tests FR-007: System MUST retain user data`
4. Verify all FR-XXX covered

**CI/CD Not Enforcing**:
1. Update CI config (GitHub Actions, GitLab CI, etc.)
2. Add coverage check step that fails build if <90%
3. Add mutation check step that fails build if ≤80%
4. Test by submitting low-coverage PR (should be blocked)

---

## Test Quality Checklist

Additional validation:

- [ ] Tests are deterministic (no flaky tests)
- [ ] Tests use realistic data (not just "test@test.com")
- [ ] Mocks used appropriately (external APIs only)
- [ ] Test names descriptive (describe behavior, not implementation)
- [ ] Setup/teardown prevents test pollution
- [ ] Tests run in <5 minutes (optimize if slower)

---

## Output

**If PASS**:
- Documentation created:
  - `docs/testing/coverage.md` with metrics
  - `docs/testing/mutation.md` with Stryker results
- Proceed to QA validation (Gate 5)

**If FAIL**:
- Document failures with specific metrics
- Create remediation task list
- Re-validate after improvements

---

## Traceability Note

Gate 4 approval establishes test baseline. Traceability mapping: spec.md FR-XXX → Test Case → Code must be complete.

---

**Last Updated**: 2025-12-29 | **Constitution Version**: 1.0.0
