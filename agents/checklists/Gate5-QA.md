# Gate 5: Quality Assurance Validation

**Purpose**: Human validation of feature quality, usability, and alignment with user stories.

**When**: After Gate 4 passes, before final validation.

**Owner**: QA Tester / Product Owner

---

## PASS/FAIL Criteria

### PASS Requirements (All must be true)

- [ ] **All User Stories manually validated**
  - P1 story tested end-to-end (MVP validation)
  - P2 stories tested independently
  - P3 stories tested independently
  - Each story's "Independent Test" criteria met (from spec.md)

- [ ] **Acceptance Scenarios verified**
  - Every Given/When/Then scenario executed manually
  - Results match expected outcomes
  - No unexpected behaviors observed

- [ ] **Success Criteria measured** (from spec.md SC-XXX)
  - SC-001 through SC-NNN validated with data
  - Metrics captured and documented
  - Business impact observable

- [ ] **Edge Cases validated**
  - Boundary conditions tested manually
  - Error messages clear and helpful
  - System degrades gracefully

- [ ] **Usability validated**
  - User flows intuitive (no confusion)
  - Error states provide recovery path
  - Loading states clear (no "frozen" UI)
  - Responsive design works (if web)

- [ ] **Cross-browser/platform tested** (if applicable)
  - Chrome, Firefox, Safari (web)
  - iOS/Android (mobile)
  - Minimum supported versions specified

- [ ] **Performance acceptable** (from plan.md Technical Context)
  - Response times meet targets (e.g., <200ms p95)
  - No memory leaks observed
  - Handles expected scale (e.g., 1000 users)

- [ ] **Security basics validated**
  - No secrets visible in browser/logs
  - Authentication required where expected
  - Authorization enforces RLS policies
  - HTTPS enforced (no mixed content)

### FAIL Conditions (Any triggers FAIL)

- User story fails manual test
- Acceptance scenario outcome doesn't match spec
- Success criteria not measurable or unmet
- Usability issues prevent task completion
- Performance below targets
- Security vulnerability observed
- Undocumented features discovered (violates Constitution Section 3)

---

## Remediation Steps (If FAIL)

**User Story Fails**:
1. Document failure: story ID, steps, expected vs actual
2. Create bug report with reproduction steps
3. Assign to implementation team
4. Re-test after fix

**Acceptance Scenario Mismatch**:
1. Verify spec.md scenario is correct
2. If spec correct: file bug, fix implementation
3. If spec wrong: update spec with ADR, re-validate design gates
4. Re-test scenario

**Unmet Success Criteria**:
1. Gather actual metrics vs target metrics
2. Determine root cause (performance, design, UX)
3. Create remediation plan with priority
4. Re-test after improvements

**Usability Issues**:
1. Document specific pain points with screenshots
2. Classify severity (blocker, major, minor)
3. Blocker: must fix before PASS
4. Major/Minor: consider deferring to future iteration with ADR

**Performance Issues**:
1. Run profiling tools (Chrome DevTools, py-spy, etc.)
2. Identify bottlenecks
3. Optimize or document limitation with ADR
4. Re-test with realistic load

**Security Vulnerabilities**:
1. IMMEDIATELY escalate to security review
2. Do NOT proceed to deployment
3. Fix vulnerability
4. Re-validate security gates

**Undocumented Features**:
1. Document ALL discovered features
2. Either: Add to spec.md with ADR OR remove from code
3. Re-validate spec and design gates
4. Update tests to cover new features

---

## QA Test Matrix Template

| User Story | Test Case | Status | Notes |
|------------|-----------|--------|-------|
| US1 (P1) | Manual end-to-end flow | ☐ | |
| US2 (P2) | Manual end-to-end flow | ☐ | |
| Acceptance Scenario 1 | Given/When/Then | ☐ | |
| SC-001 | Metric validation | ☐ | Target: X, Actual: Y |
| Edge Case: Boundary | Test condition | ☐ | |

---

## Output

**If PASS**:
- QA report created documenting:
  - Test matrix with all checkboxes marked
  - Measured metrics for success criteria
  - Screenshots/evidence of validation
  - Sign-off from QA Tester
- Proceed to Gate 6 (Validation)

**If FAIL**:
- QA report documenting:
  - Failures with evidence (screenshots, logs)
  - Severity classifications
  - Remediation tasks assigned
- Block progression until fixes validated

---

## Traceability Note

Gate 5 approval confirms manual validation of spec.md requirements. QA sign-off required before final validation and deployment.

---

**Last Updated**: 2025-12-29 | **Constitution Version**: 1.0.0
