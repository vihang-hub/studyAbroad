# Gate 6: Specification Compliance & Traceability Validation

**Purpose**: Final verification that implementation has 100% parity with specification and all requirements are traceable.

**When**: After Gate 5 passes, before security review.

**Owner**: Gate6 Validator / Verification Specialist

---

## PASS/FAIL Criteria

### PASS Requirements (All must be true)

- [ ] **100% Specification Parity** (Constitution Section 3)
  - Every FR-XXX implemented and tested
  - Every user story implemented and tested
  - Every API endpoint matches contracts/
  - Every UI element documented in spec.md
  - No undocumented features exist

- [ ] **Complete Traceability Mapping**
  - `docs/traceability.md` exists with:
    - Spec Section → Test Cases → Code Modules mapping
    - Bidirectional references (spec ↔ tests ↔ code)
    - Coverage metrics (X/Y requirements traced)
  - Every FR-XXX traces to test case(s)
  - Every test case traces to code module(s)

- [ ] **Verification Report Complete**
  - `docs/verification-report.md` exists with:
    - Executive summary (PASS/FAIL with metrics)
    - Methodology and scope
    - Findings (spec parity, traceability, compliance)
    - Evidence (file paths, line numbers)
    - Recommendations
  - Report dated and version-stamped

- [ ] **Storage Retention Policies Enforced**
  - Database retention configured (30 days per Constitution)
  - Cleanup jobs scheduled (if applicable)
  - Data retention documented in data-model.md

- [ ] **Row-Level Security (RLS) Validated**
  - RLS policies implemented in Supabase
  - User access constraints verified
  - Authorization tests passing
  - Policy documentation in data-model.md

- [ ] **No Orphaned Code**
  - Every file/function maps to spec requirement
  - No "experimental" code in production branches
  - Dead code removed

- [ ] **No Orphaned Specs**
  - Every requirement maps to implementation
  - No unimplemented FR-XXX (or marked deferred with ADR)

### FAIL Conditions (Any triggers FAIL)

- Undocumented features discovered
- FR-XXX without implementation
- Implementation without tracing FR-XXX
- Traceability gaps (requirement → test → code chain broken)
- Storage retention not configured
- RLS policies missing or untested
- Orphaned code or orphaned specs present

---

## Verification Methodology

### Phase 1: Discovery and Analysis
1. Scan codebase for all features, UI components, API endpoints
2. Review spec.md for all stated requirements (FR-XXX, user stories)
3. Analyze test suites for coverage and traceability
4. Examine database for storage policies and RLS rules

### Phase 2: Gap Analysis
1. Compare implemented features against spec.md (detect undocumented)
2. Compare spec.md against implementation (detect unimplemented)
3. Map tests to requirements and code (identify coverage gaps)
4. Verify storage/retention policies enforced
5. Validate RLS and access controls implemented

### Phase 3: Documentation Generation
1. Create `docs/traceability.md` with mapping tables
2. Create `docs/verification-report.md` with findings
3. Update `agents/checklists/Gate6-Validation.md` if needed
4. Date-stamp and version all documents

### Phase 4: Final Adjudication
1. Evaluate findings against Gate 6 criteria
2. Determine PASS or FAIL
3. Document violations with remediation steps (if FAIL)
4. Sign-off report (if PASS)

---

## Remediation Steps (If FAIL)

**Undocumented Features**:
1. Document ALL discovered features in spec.md
2. Either: Add to spec with ADR OR remove from code
3. Re-validate spec (Gate 1) and design (Gate 2)
4. Update tests to cover new requirements

**Unimplemented Requirements**:
1. Create task list for missing FR-XXX
2. Either: Implement OR mark deferred with ADR
3. Update traceability mapping
4. Re-validate implementation

**Traceability Gaps**:
1. For each gap: add tracing comment in code/tests
2. Update `docs/traceability.md` with mappings
3. Verify bidirectional links complete
4. Re-validate coverage metrics

**Missing Storage Policies**:
1. Configure retention in database (SQL migration)
2. Schedule cleanup jobs (cron, Cloud Scheduler, etc.)
3. Document in data-model.md
4. Test retention enforcement

**Missing RLS Policies**:
1. Create RLS policies in Supabase (SQL)
2. Write authorization tests
3. Verify user access constraints
4. Document policies in data-model.md

**Orphaned Code**:
1. Identify files/functions without spec mapping
2. Either: Map to existing requirement OR remove
3. Update traceability documentation
4. Clean up dead code

**Orphaned Specs**:
1. Identify FR-XXX without implementation
2. Either: Implement OR mark deferred with ADR
3. Update spec.md status
4. Re-validate design and implementation gates

---

## Traceability Document Format

**Required Structure** (`docs/traceability.md`):

```markdown
# Traceability Matrix: [Feature Name]

**Version**: X.Y.Z | **Date**: YYYY-MM-DD | **Validator**: [Name]

## Summary Metrics
- Total Requirements: X
- Traced Requirements: Y
- Coverage: Y/X (Z%)
- Gaps: [List or "None"]

## Mapping Table

| Spec Section | Requirement ID | Test Cases | Code Modules | Status |
|--------------|----------------|------------|--------------|--------|
| User Story 1 | FR-001 | test_user_registration.py | src/auth/register.ts | ✅ Complete |
| User Story 1 | FR-002 | test_email_validation.py | src/auth/validators.ts | ✅ Complete |
| User Story 2 | FR-003 | test_password_reset.py | src/auth/reset.ts | ⚠️ Partial |
```

---

## Verification Report Format

**Required Structure** (`docs/verification-report.md`):

```markdown
# Verification Report: [Feature Name]

**Status**: PASS / FAIL | **Date**: YYYY-MM-DD | **Validator**: [Name]

## Executive Summary
[One-page overview with clear PASS/FAIL and key metrics]

## Methodology
[What was checked and how]

## Findings
### Specification Parity: [PASS/FAIL]
[Details with evidence]

### Traceability: [PASS/FAIL]
[Details with evidence]

### Compliance: [PASS/FAIL]
[Storage, RLS, security details]

## Recommendations
[Next steps]
```

---

## Output

**If PASS**:
- `docs/traceability.md` complete
- `docs/verification-report.md` with PASS status
- Evidence documented and dated
- Proceed to Gate 7 (Security)

**If FAIL**:
- `docs/verification-report.md` with FAIL status
- Violations documented with severity
- Remediation steps assigned
- Block progression until re-validation passes

---

**Last Updated**: 2025-12-29 | **Constitution Version**: 1.0.0
