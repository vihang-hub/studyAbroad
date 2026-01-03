# Mutation Testing Report

**Project**: UK Study & Migration Research App MVP
**Framework**: Stryker Mutator
**Analysis Date**: 2025-12-29
**Analyzed By**: QA Testing Specialist Agent
**Status**: Configuration Ready

---

## 1. Executive Summary

This document describes the mutation testing strategy and reports for the UK Study & Migration Research App. Mutation testing validates that our test suite is effective at catching bugs by introducing small changes (mutations) to the source code and verifying that tests fail appropriately.

### Constitutional Requirements

- **Mutation Score Target**: >80% (as mandated by constitution Section 3)
- **Scope**: TypeScript/JavaScript code (Frontend + Shared packages)
- **Tool**: Stryker Mutator
- **Frequency**: Before releases and major PRs

---

## 2. What is Mutation Testing?

### 2.1 Concept

Mutation testing answers the question: **"Are our tests actually effective at detecting bugs?"**

**Process**:
1. **Mutate**: Stryker modifies source code (e.g., changes `>` to `<`, removes conditions)
2. **Test**: Run test suite against mutated code
3. **Evaluate**:
   - If tests **FAIL**: Mutant is "killed" (good - tests caught the bug)
   - If tests **PASS**: Mutant "survived" (bad - tests missed the bug)

**Mutation Score** = (Killed Mutants / Total Mutants) × 100

### 2.2 Why Mutation Testing Matters

**Code Coverage Limitation**:
- 100% code coverage ≠ effective tests
- Tests might execute code but not verify behavior

**Example**:
```typescript
// Source code
function isUKQuery(query: string): boolean {
  return query.includes('UK'); // Original
}

// Mutation 1: Remove method call
function isUKQuery(query: string): boolean {
  return true; // Mutated - always returns true
}

// Mutation 2: Negate return
function isUKQuery(query: string): boolean {
  return !query.includes('UK'); // Mutated - inverted logic
}
```

**Weak Test** (survives mutations):
```typescript
it('should work', () => {
  isUKQuery('UK university'); // Just executes, doesn't assert
});
```

**Strong Test** (kills mutations):
```typescript
it('should return true for UK queries', () => {
  expect(isUKQuery('UK university')).toBe(true);
});

it('should return false for non-UK queries', () => {
  expect(isUKQuery('USA university')).toBe(false);
});
```

---

## 3. Stryker Mutator Configuration

### 3.1 Installation

```bash
# Install Stryker and plugins
npm install --save-dev \
  @stryker-mutator/core \
  @stryker-mutator/vitest-runner \
  @stryker-mutator/typescript-checker
```

### 3.2 Configuration Files

#### Frontend: `/Users/vihang/projects/study-abroad/frontend/stryker.conf.json`

```json
{
  "$schema": "./node_modules/@stryker-mutator/core/schema/stryker-schema.json",
  "packageManager": "npm",
  "testRunner": "vitest",
  "vitest": {
    "configFile": "vitest.config.ts"
  },
  "checkers": ["typescript"],
  "tsconfigFile": "tsconfig.json",
  "mutate": [
    "src/**/*.ts",
    "src/**/*.tsx",
    "!src/**/*.test.ts",
    "!src/**/*.test.tsx",
    "!src/**/*.d.ts",
    "!src/**/types/**"
  ],
  "coverageAnalysis": "perTest",
  "thresholds": {
    "high": 85,
    "low": 75,
    "break": 80
  },
  "timeoutMS": 60000,
  "concurrency": 4,
  "reporters": ["html", "clear-text", "progress", "json"]
}
```

#### Shared: `/Users/vihang/projects/study-abroad/shared/stryker.conf.json`

```json
{
  "$schema": "./node_modules/@stryker-mutator/core/schema/stryker-schema.json",
  "packageManager": "npm",
  "testRunner": "vitest",
  "vitest": {
    "configFile": "vitest.config.ts"
  },
  "checkers": ["typescript"],
  "tsconfigFile": "tsconfig.json",
  "mutate": [
    "src/**/*.ts",
    "src/**/*.tsx",
    "!src/**/*.test.ts",
    "!src/**/*.test.tsx",
    "!src/**/*.d.ts",
    "!src/**/types/**",
    "!src/index.ts"
  ],
  "coverageAnalysis": "perTest",
  "thresholds": {
    "high": 85,
    "low": 75,
    "break": 80
  },
  "timeoutMS": 60000,
  "concurrency": 4,
  "reporters": ["html", "clear-text", "progress", "json"]
}
```

### 3.3 Configuration Explanation

| Setting | Purpose |
|---------|---------|
| `mutate` | Files to mutate (excludes tests, types, configs) |
| `testRunner` | Use Vitest to run tests |
| `checkers` | TypeScript type checking to avoid invalid mutations |
| `coverageAnalysis` | "perTest" for faster analysis |
| `thresholds.break` | Fail if mutation score < 80% |
| `thresholds.high` | Excellent: ≥85% |
| `thresholds.low` | Warning: <75% |
| `concurrency` | Run 4 mutants in parallel |
| `timeoutMS` | Kill mutant if test runs >60s |

---

## 4. Mutation Operators

Stryker applies various mutation operators to source code:

### 4.1 Arithmetic Operators

| Original | Mutated |
|----------|---------|
| `a + b` | `a - b` |
| `a - b` | `a + b` |
| `a * b` | `a / b` |
| `a / b` | `a * b` |
| `a % b` | `a * b` |

### 4.2 Logical Operators

| Original | Mutated |
|----------|---------|
| `a && b` | `a \|\| b` |
| `a \|\| b` | `a && b` |
| `!a` | `a` |

### 4.3 Relational Operators

| Original | Mutated |
|----------|---------|
| `a > b` | `a < b`, `a >= b`, `a <= b` |
| `a >= b` | `a > b`, `a < b`, `a <= b` |
| `a == b` | `a != b` |
| `a === b` | `a !== b` |

### 4.4 Conditional Operators

| Original | Mutated |
|----------|---------|
| `if (condition)` | `if (true)`, `if (false)` |
| `condition ? a : b` | `true ? a : b`, `false ? a : b` |

### 4.5 String Mutations

| Original | Mutated |
|----------|---------|
| `"string"` | `""` (empty string) |
| `'string'` | `""` |

### 4.6 Array Mutations

| Original | Mutated |
|----------|---------|
| `[]` | `["Stryker was here"]` |
| `[1, 2, 3]` | `[]` |

---

## 5. Running Mutation Tests

### 5.1 Commands

```bash
# Frontend mutation testing
cd frontend
npx stryker run

# Shared package mutation testing
cd shared
npx stryker run

# Run with specific configuration
npx stryker run --configFile stryker.conf.json

# Dry run (show what will be mutated)
npx stryker run --dryRun

# Incremental run (only changed files)
npx stryker run --incremental
```

### 5.2 Output Interpretation

**Terminal Output**:
```
Mutation testing complete.
─────────────────────────────────────────────────────────────────
│ File                     │ % score │ # killed │ # timeout │ # survived │ # no cov │
├──────────────────────────┼─────────┼──────────┼───────────┼────────────┼──────────┤
│ All files                │   82.50 │       33 │         0 │          7 │        0 │
│  src/hooks/useAuth.ts    │   90.00 │       18 │         0 │          2 │        0 │
│  src/hooks/usePayment.ts │   75.00 │       15 │         0 │          5 │        0 │
└──────────────────────────┴─────────┴──────────┴───────────┴────────────┴──────────┘
```

**Interpretation**:
- **% score**: Percentage of mutants killed
- **# killed**: Mutants caught by tests (good)
- **# timeout**: Mutants that caused infinite loops (treated as killed)
- **# survived**: Mutants that passed tests (bad - need better tests)
- **# no cov**: Mutants in uncovered code (need tests first)

---

## 6. Initial Mutation Testing Results

### 6.1 Status

**Current Status**: 🔴 **BLOCKED - Cannot Run Due to Failing Test Suites**

**Analysis Date**: 2025-12-31

**Blocking Issues**:
1. ❌ Backend: 48 out of 76 tests failing (63% pass rate) - async/mock configuration issues
2. ❌ Frontend: 8 out of 90 tests failing (91% pass rate) - missing dependencies
3. ❌ Shared: 36 out of 42 tests failing (14% pass rate) - missing @testing-library/jest-dom setup

**Why Blocked**:
Mutation testing requires a **100% passing test suite** to function correctly. Running Stryker with failing tests will produce unreliable results because:
- Mutants may appear "killed" when tests fail for unrelated reasons
- Cannot differentiate between legitimate test failures and mutation-induced failures
- Mutation score calculation becomes meaningless

**Prerequisites for Mutation Testing**:
1. ✅ Test suite is complete (DONE)
2. ❌ All tests must pass (BLOCKED - only 116/208 tests passing)
3. ❌ Code coverage meets ≥90% (BLOCKED - currently 69% backend)
4. ✅ Stryker configuration files created (DONE)
5. ⏳ First mutation run (WAITING on items 2 & 3)

### 6.2 Expected Results (Baseline)

Based on test suite analysis, we expect:

| Package | Estimated Mutation Score | Expected Survivors |
|---------|--------------------------|-------------------|
| Frontend Hooks | ~85% | ~5-10 mutants |
| Shared Hooks | ~88% | ~3-7 mutants |
| Shared Components | ~82% | ~8-12 mutants |

**Confidence Level**: Medium (based on test thoroughness analysis)

---

## 7. Analyzing Survived Mutants

### 7.1 Common Survival Patterns

**Pattern 1: Weak Assertions**
```typescript
// Weak test (survives many mutations)
it('should return user', () => {
  const user = getUser();
  expect(user).toBeDefined(); // Only checks existence
});

// Strong test (kills mutations)
it('should return user with correct properties', () => {
  const user = getUser();
  expect(user.id).toBe('user_123');
  expect(user.email).toBe('test@example.com');
  expect(user.isAuthenticated).toBe(true);
});
```

**Pattern 2: Missing Negative Tests**
```typescript
// Missing test for false case
it('should return true for UK query', () => {
  expect(isUKQuery('UK university')).toBe(true);
});

// Add negative test to kill negation mutations
it('should return false for non-UK query', () => {
  expect(isUKQuery('USA university')).toBe(false);
});
```

**Pattern 3: Unchecked Edge Cases**
```typescript
// Test doesn't check boundary
it('should validate amount', () => {
  expect(validateAmount(300)).toBe(true);
});

// Add boundary tests
it('should reject amounts below minimum', () => {
  expect(validateAmount(299)).toBe(false);
});

it('should reject amounts above maximum', () => {
  expect(validateAmount(1000001)).toBe(false);
});
```

### 7.2 Fixing Survived Mutants

**Process**:
1. Open HTML report: `frontend/reports/mutation/html/index.html`
2. Find survived mutants (highlighted in yellow/red)
3. Understand what mutation was made
4. Add/strengthen tests to catch that mutation
5. Re-run mutation testing
6. Verify mutant is now killed

---

## 8. Mutation Score Thresholds

### 8.1 Constitutional Requirement

**Minimum**: >80% mutation score (Section 3: Engineering Rigor & Testing)

### 8.2 Quality Tiers

| Tier | Mutation Score | Assessment |
|------|----------------|------------|
| Excellent | ≥85% | Strong, effective test suite |
| Good | 80-84% | Meets requirements, room for improvement |
| Warning | 75-79% | Below target, action needed |
| Fail | <75% | Unacceptable, must improve |

### 8.3 Breaking Builds

**CI/CD Configuration**:
- Mutation score <80% → **Build FAILS**
- Mutation score 80-85% → **Build PASSES with warning**
- Mutation score ≥85% → **Build PASSES**

---

## 9. Mutation Testing Best Practices

### 9.1 DO

- ✅ Run mutation tests before releases
- ✅ Focus on high-value code (business logic, services)
- ✅ Analyze survived mutants to improve tests
- ✅ Use mutation testing to validate test quality
- ✅ Set realistic thresholds (80% is challenging)
- ✅ Run incrementally to save time
- ✅ Ignore trivial mutations (logging, simple getters)

### 9.2 DON'T

- ❌ Run mutation tests on every commit (too slow)
- ❌ Aim for 100% mutation score (diminishing returns)
- ❌ Mutate auto-generated code
- ❌ Mutate type definitions
- ❌ Add meaningless tests just to kill mutants
- ❌ Ignore consistent survival patterns

---

## 10. Performance Optimization

### 10.1 Speed Improvements

Mutation testing is slow (minutes to hours). Optimize with:

1. **Incremental Mode**:
   ```bash
   npx stryker run --incremental
   ```
   Only mutates changed files since last run.

2. **File Filtering**:
   ```bash
   npx stryker run --mutate "src/hooks/**/*.ts"
   ```
   Focus on specific modules.

3. **Concurrency**:
   ```json
   { "concurrency": 8 }
   ```
   Increase based on CPU cores.

4. **Coverage Analysis**:
   ```json
   { "coverageAnalysis": "perTest" }
   ```
   Faster than "all" mode.

5. **Timeout Reduction**:
   ```json
   { "timeoutMS": 30000 }
   ```
   Kill slow mutants faster.

### 10.2 CI/CD Integration

**Strategy**: Don't run on every commit

**Recommended Schedule**:
- **Daily**: Run overnight on main branch
- **Weekly**: Full mutation analysis + report
- **Pre-release**: Mandatory mutation testing gate
- **PR**: Optional, only for critical changes

---

## 11. Mutation Testing Workflow

### 11.1 Weekly Workflow

**Monday**:
1. Review last week's mutation report
2. Identify top 5 survived mutants
3. Create tickets to add tests

**Wednesday**:
1. Run incremental mutation testing
2. Check if new code has adequate tests

**Friday**:
1. Full mutation run
2. Generate HTML report
3. Update this document with latest scores

### 11.2 Pre-Release Workflow

**1 Week Before Release**:
1. Run full mutation testing
2. Analyze all survived mutants
3. Prioritize fixes for business-critical code

**3 Days Before Release**:
1. Re-run mutation testing
2. Verify mutation score ≥80%
3. Document any acceptable survivals

**Release Day**:
1. Final mutation check
2. Include mutation score in release notes

---

## 12. Known Limitations

### 12.1 Stryker Limitations

1. **Slow**: Can take hours for large codebases
2. **False Positives**: Some mutations are semantically equivalent
3. **Timeout Issues**: Some mutants cause hangs
4. **TypeScript Complexity**: Generic types may cause issues

### 12.2 Mutation Testing Limitations

1. **Not a Silver Bullet**: High score doesn't guarantee bug-free code
2. **Diminishing Returns**: 90%+ is very expensive to achieve
3. **Ignores Integration**: Only tests unit-level logic
4. **Context Blind**: Doesn't understand business requirements

---

## 13. Next Steps

### 13.1 Immediate Actions

1. ⏳ Install Stryker dependencies
   ```bash
   cd frontend && npm install --save-dev @stryker-mutator/core @stryker-mutator/vitest-runner @stryker-mutator/typescript-checker
   cd ../shared && npm install --save-dev @stryker-mutator/core @stryker-mutator/vitest-runner @stryker-mutator/typescript-checker
   ```

2. ⏳ Create configuration files
   - `frontend/stryker.conf.json`
   - `shared/stryker.conf.json`

3. ⏳ Run first mutation test
   ```bash
   cd frontend && npx stryker run
   ```

4. ⏳ Analyze results and update this document

### 13.2 Short-term Goals (Week 1-2)

1. Achieve ≥80% mutation score in shared package
2. Achieve ≥80% mutation score in frontend package
3. Document common survival patterns
4. Create mutation testing guide for developers

### 13.3 Long-term Goals (Month 2+)

1. Integrate mutation testing into CI/CD
2. Set up automated weekly reports
3. Track mutation score trends over time
4. Expand mutation testing to backend (if tooling available)

---

## 14. Resources and References

### 14.1 Documentation

- **Stryker Docs**: https://stryker-mutator.io/docs/
- **Vitest Runner**: https://stryker-mutator.io/docs/stryker-js/vitest-runner/
- **Mutation Testing Intro**: https://stryker-mutator.io/docs/mutation-testing-introduction/

### 14.2 Reports Location

- **HTML Reports**:
  - Frontend: `/Users/vihang/projects/study-abroad/frontend/reports/mutation/html/`
  - Shared: `/Users/vihang/projects/study-abroad/shared/reports/mutation/html/`

- **JSON Reports**:
  - Frontend: `/Users/vihang/projects/study-abroad/frontend/reports/mutation/mutation.json`
  - Shared: `/Users/vihang/projects/study-abroad/shared/reports/mutation/mutation.json`

### 14.3 Commands Reference

```bash
# Run mutation testing
npx stryker run

# Dry run (analyze only, don't mutate)
npx stryker run --dryRun

# Incremental run
npx stryker run --incremental

# Filter specific files
npx stryker run --mutate "src/hooks/**/*.ts"

# Generate report
npx stryker run --reporters html,clear-text

# Clear cache
npx stryker run --force
```

---

## 15. Conclusion

### 15.1 Summary

Mutation testing is a critical component of our quality assurance strategy, ensuring that our test suite is not just comprehensive but **effective** at catching bugs. By targeting >80% mutation score, we validate that our tests truly verify behavior rather than just executing code paths.

### 15.2 Current Status

🟡 **Test Suites Created, Awaiting Execution**

**Progress Update (2026-01-02)**:

**Completed**:
- ✅ Comprehensive integration test suites created for User Story 1
- ✅ Backend: 18 acceptance criteria test cases
- ✅ Frontend: 15 E2E integration test cases
- ✅ Stryker configuration files exist
- ✅ Test design ensures strong assertions (not just execution)

**Pending**:
- ⏳ Fix environment configuration (Python 3.10+, frontend dependencies)
- ⏳ Execute test suites and achieve 100% pass rate
- ⏳ Run first Stryker mutation analysis
- ⏳ Analyze survived mutants
- ⏳ Achieve ≥80% mutation score target

**Expected Mutation Score**: Based on test quality analysis, expecting **82-88%** mutation score

**Rationale**:
- Strong assertions throughout test suites
- Both positive and negative test cases implemented
- Edge cases and boundary conditions tested
- Error handling paths validated
- Streaming behavior explicitly tested

Next steps:
1. Fix Python version compatibility
2. Install frontend dependencies
3. Execute test suites (target: 100% pass rate)
4. Run Stryker mutation testing
5. Analyze and fix survived mutants
6. Achieve ≥80% mutation score target

### 15.3 Quality Gate Impact

Mutation testing is a **mandatory quality gate** for:
- MVP release
- Major feature releases
- Post-MVP production deployment

Mutation score <80% will **block deployment** until improved.

---

**Last Updated**: 2026-01-02
**Next Review**: After environment fixes and mutation test execution
**Status**: 🟡 **In Progress - Test Suites Created, Execution Pending**
