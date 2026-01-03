# Speckit Autopilot - Automated Implementation Pipeline

**Trigger**: User says "start implementation" or runs `/speckit.autopilot`

**Prerequisites**:
- Approved `spec.md` exists in `specs/{feature}/`
- User has confirmed they want automated execution

---

## Session State Management

### On Start - Load State

**FIRST**, read `.specify/session/state.json` to check for existing progress:

```javascript
const state = JSON.parse(readFile('.specify/session/state.json'));

if (state.pipeline.status === 'in_progress') {
  // Resume from last checkpoint
  const currentGate = state.pipeline.current_stage;
  const nextTask = state.gates[currentGate].last_completed_task;

  console.log(`Resuming from: ${currentGate}, task ${nextTask}`);
  startFromGate(currentGate);
} else {
  // Fresh start
  startFromGate('gate1_architecture');
}
```

### Checkpoint Function

Call this after EVERY significant action:

```javascript
function checkpoint(gate, status, details) {
  const state = JSON.parse(readFile('.specify/session/state.json'));

  state.last_updated = new Date().toISOString();
  state.pipeline.current_stage = gate;
  state.gates[gate].status = status;
  state.gates[gate] = { ...state.gates[gate], ...details };

  // Add to recent activity
  state.recent_activity.unshift({
    timestamp: new Date().toISOString(),
    action: `${gate}: ${status}`,
    details: details
  });

  // Keep only last 20 activities
  state.recent_activity = state.recent_activity.slice(0, 20);

  writeFile('.specify/session/state.json', JSON.stringify(state, null, 2));
}
```

### Resume Logic

When `--from={gate}` is specified OR resuming from state:

```javascript
function startFromGate(gate) {
  const gateOrder = [
    'gate1_architecture',
    'gate2_design',
    'gate3_testdesign',
    'gate4_implementation',
    'gate5_qa',
    'gate6_validation',
    'gate7_security',
    'gate8_deployment'
  ];

  const startIndex = gateOrder.indexOf(gate);
  for (let i = startIndex; i < gateOrder.length; i++) {
    runGate(gateOrder[i]);
  }
}
```

---

## Superpowers Integration

This pipeline integrates with [Superpowers skills](https://github.com/obra/superpowers) at key points:

### Skill → Gate Mapping

| Superpowers Skill | When to Use | Speckit Gate |
|-------------------|-------------|--------------|
| `superpowers:brainstorming` | Before specification | Pre-Gate0 |
| `superpowers:writing-plans` | During planning | Gate2 → Gate3 |
| `superpowers:using-git-worktrees` | Before implementation | Gate4 start |
| `superpowers:test-driven-development` | During implementation | Gate4 |
| `superpowers:executing-plans` | Task execution | Gate4 |
| `superpowers:systematic-debugging` | When tests fail | Gate4/Gate5 |
| `superpowers:verification-before-completion` | Before marking done | Every gate |
| `superpowers:requesting-code-review` | After implementation | Gate5 |
| `superpowers:dispatching-parallel-agents` | Parallel tasks | Gate4 [P] tasks |
| `superpowers:finishing-a-development-branch` | Deployment prep | Gate8 |

### Auto-Invocation Rules

The pipeline automatically invokes Superpowers skills when appropriate:

1. **Gate4 Start**: Invoke `superpowers:using-git-worktrees` to create isolated branch
2. **Each Task**: Invoke `superpowers:test-driven-development` for TDD approach
3. **Parallel Tasks**: Invoke `superpowers:dispatching-parallel-agents` for [P] marked tasks
4. **Test Failures**: Invoke `superpowers:systematic-debugging` to find root cause
5. **Gate Completion**: Invoke `superpowers:verification-before-completion` before marking PASS
6. **Gate8**: Invoke `superpowers:finishing-a-development-branch` for merge decision

---

## Pipeline Stages

Execute the following stages **sequentially**. Each stage:
1. Spawns a specialized agent via Task tool
2. Follows the corresponding Gate checklist
3. Invokes relevant Superpowers skills
4. Creates required artifacts
5. Checkpoints progress to state.json
6. Reports PASS/FAIL before proceeding
7. **STOPS on FAIL** - returns control to user

---

### Pre-Stage: Brainstorming (Optional)

**Skill**: `superpowers:brainstorming`
**When**: User hasn't fully defined requirements

If the specification seems incomplete or ambiguous:
```
Invoke: superpowers:brainstorming

Follow the brainstorming workflow:
1. Ask clarifying questions (one at a time)
2. Present 2-3 solution approaches with trade-offs
3. Break down design into 200-300 word sections
4. Validate each section before proceeding
```

**Output**: Refined requirements fed into `/speckit.specify`

---

### Stage 1: Architecture (architect agent)

**Agent**: `architect` (Task tool with subagent_type="architect")
**Gate**: `agents/checklists/Gate1-Architecture.md`
**Skills**: None (architecture is human-guided)
**Input**: `specs/{feature}/spec.md`

**Prompt for agent**:
```
You are the Architect agent. Read the specification at specs/{feature}/spec.md.

Follow the checklist at agents/checklists/Gate1-Architecture.md.

Required outputs:
- docs/architecture/system-overview.md (if not exists, create/update)
- docs/adr/ADR-NNNN-{decision}.md (for any new architectural decisions)
- docs/diagrams/{relevant}.mmd (Mermaid diagrams)
- docs/threat-model.md (security analysis)

Before marking complete, invoke: superpowers:verification-before-completion

Update agents/checklists/Gate1-Architecture.md with results.
End with: "Gate1: PASS" or "Gate1: FAIL - {reason}"
```

**Checkpoint**: Update state.json with Gate1 status

---

### Stage 2: Design (designer agent)

**Agent**: `designer` (Task tool with subagent_type="designer")
**Gate**: `agents/checklists/Gate2-Design.md`
**Skills**: `superpowers:writing-plans` (for detailed design)
**Input**: Gate1 outputs + spec.md

**Prompt for agent**:
```
You are the Designer agent. Read:
- specs/{feature}/spec.md
- docs/architecture/system-overview.md
- All relevant ADRs in docs/adr/

Invoke: superpowers:writing-plans for detailed component design

Follow the checklist at agents/checklists/Gate2-Design.md.

Required outputs:
- docs/api/openapi.yaml (or update existing)
- docs/database/schema.sql (if database changes)
- docs/database/rls-policies.sql (if RLS needed)
- docs/design/shared-component-interfaces.md (component contracts)
- docs/flows/{flow-name}.mmd (UX flow diagrams)

Before marking complete, invoke: superpowers:verification-before-completion

Update agents/checklists/Gate2-Design.md with results.
End with: "Gate2: PASS" or "Gate2: FAIL - {reason}"
```

**Checkpoint**: Update state.json with Gate2 status

---

### Stage 3: Test Design (test-designer agent) - TDD

**Agent**: `test-designer` (Task tool)
**Gate**: `agents/checklists/Gate3-TestDesign.md`
**Skills**: `superpowers:test-driven-development` (TDD approach)
**Input**: Gate2 outputs + spec.md

**Prompt for agent**:
```
You are the Test Designer agent.

MANDATORY: Invoke superpowers:test-driven-development first.

Follow TDD: Write tests BEFORE implementation (RED phase).

Read:
- specs/{feature}/spec.md (acceptance criteria)
- docs/api/openapi.yaml (API contracts)
- docs/database/schema.sql (data model)

Required outputs:
- docs/testing/test-strategy.md (update with new tests)
- docs/testing/acceptance-criteria-mapping.md (AC → test mapping)
- backend/tests/test_{feature}.py (pytest test stubs - should FAIL)
- frontend/tests/{feature}/*.test.tsx (Vitest test stubs - should FAIL)
- shared/tests/{package}/*.test.ts (if shared changes - should FAIL)

Tests MUST:
- Fail initially (no implementation yet) - this is the RED phase
- Cover all acceptance criteria from spec
- Include edge cases and error scenarios

Before marking complete, invoke: superpowers:verification-before-completion

Update agents/checklists/Gate3-TestDesign.md with results.
End with: "Gate3: PASS" or "Gate3: FAIL - {reason}"
```

**Checkpoint**: Update state.json with Gate3 status

---

### Stage 4: Plan Generation (speckit.tasks)

**Tool**: Run `/speckit.tasks` skill
**Output**: `specs/{feature}/tasks.md`

This generates the implementation task list from the design artifacts.

**Checkpoint**: Update state.json with tasks generated

---

### Stage 5: Implementation (coder agent)

**Agent**: `coder` (Task tool with subagent_type="coder")
**Gate**: `agents/checklists/Gate4-Implementation.md`
**Skills**:
- `superpowers:using-git-worktrees` (at start)
- `superpowers:test-driven-development` (each task)
- `superpowers:executing-plans` (task execution)
- `superpowers:dispatching-parallel-agents` (for [P] tasks)
**Input**: tasks.md + all design artifacts

**Prompt for agent**:
```
You are the Coder agent.

AT START: Invoke superpowers:using-git-worktrees to create isolated branch.

Read:
- specs/{feature}/tasks.md (implementation tasks)
- specs/{feature}/spec.md (requirements)
- docs/api/openapi.yaml (API contracts)
- docs/database/schema.sql (data model)
- Existing tests in backend/tests/, frontend/tests/, shared/tests/

FOR EACH TASK:
1. Invoke superpowers:test-driven-development
2. Follow RED-GREEN-REFACTOR:
   - RED: Verify test fails (from Gate3)
   - GREEN: Write minimal code to pass
   - REFACTOR: Clean up while keeping tests green

FOR PARALLEL TASKS [P]:
- Invoke superpowers:dispatching-parallel-agents
- Launch independent tasks concurrently

Invoke superpowers:executing-plans for batch execution with checkpoints.

Follow the checklist at agents/checklists/Gate4-Implementation.md.

Rules:
- Make tests pass (TDD - tests already exist from Gate3)
- Do NOT introduce undocumented features
- Follow constitution.md code style
- Commit after each logical unit of work

After each batch:
- Run tests: `cd backend && pytest` and `cd frontend && npm test`
- Invoke superpowers:verification-before-completion
- Checkpoint to state.json

Update agents/checklists/Gate4-Implementation.md with results.
End with: "Gate4: PASS" or "Gate4: FAIL - {reason}"
```

**Checkpoint**: Update state.json after EACH task completion

---

### Stage 6: QA Testing (qa-tester agent)

**Agent**: `qa-tester` (Task tool with subagent_type="qa-tester")
**Gate**: `agents/checklists/Gate5-QA.md`
**Skills**:
- `superpowers:verification-before-completion` (before marking pass)
- `superpowers:systematic-debugging` (if tests fail)
**Input**: Implementation from Stage 5

**Prompt for agent**:
```
You are the QA Tester agent. Execute comprehensive testing.

Follow the checklist at agents/checklists/Gate5-QA.md.

Required actions:
1. Run full test suites:
   - `cd backend && pytest --cov=src --cov-report=html`
   - `cd frontend && npm run test:coverage`
   - `cd shared && npm run test:coverage`

2. Run mutation testing:
   - `cd frontend && npm run test:mutation`
   - `cd shared && npm run test:mutation`
   - `cd backend && mutmut run`

3. If tests fail:
   - Invoke superpowers:systematic-debugging
   - Follow root cause analysis
   - Return to coder agent for fixes

4. Generate reports:
   - docs/testing/coverage.md (actual coverage numbers)
   - docs/testing/mutation.md (mutation scores)
   - docs/testing/test-run-report.md (full output)

Thresholds (from constitution):
- Coverage: ≥90%
- Mutation score: >80%

Before marking complete:
- Invoke superpowers:verification-before-completion
- Verify with actual command output, not assumptions

Update agents/checklists/Gate5-QA.md with results.
End with: "Gate5: PASS" or "Gate5: FAIL - {reason}"
```

**Checkpoint**: Update state.json with Gate5 status + metrics

---

### Stage 7: Bug Fixes (coder agent - iteration)

**Condition**: Only if Stage 6 reports failures

**Agent**: `coder`
**Skills**: `superpowers:systematic-debugging`
**Input**: Test failures from Stage 6

**Prompt for agent**:
```
You are the Coder agent (bug fix mode).

MANDATORY: Invoke superpowers:systematic-debugging first.

The QA agent found the following issues:
{insert failures from Stage 6}

Follow systematic debugging:
1. Reproduce the failure
2. Identify root cause (not symptoms)
3. Fix the implementation (not the test)
4. Verify fix with specific test

Do NOT:
- Change tests unless they are genuinely wrong
- Skip or disable tests
- Introduce new features while fixing

After fixes:
- Invoke superpowers:verification-before-completion
- Return to Stage 6 (QA Testing) for re-verification
```

**Loop**: Stages 6-7 repeat until Gate5 passes (max 3 iterations)

**Checkpoint**: Update state.json with each iteration

---

### Stage 8: Validation (validator agent)

**Agent**: `validator` (Task tool with subagent_type="validator")
**Gate**: `agents/checklists/Gate6-Validation.md`
**Skills**: `superpowers:verification-before-completion`
**Input**: All artifacts

**Prompt for agent**:
```
You are the Validator agent. Verify specification compliance.

Follow the checklist at agents/checklists/Gate6-Validation.md.

Verify:
1. Spec Parity: Every requirement in spec.md is implemented
2. Traceability: Every AC has a passing test
3. No Hidden Features: No undocumented functionality exists
4. API Compliance: Implementation matches openapi.yaml exactly
5. Data Model: Database matches schema.sql

Create:
- docs/compliance-summary.md (verification matrix)
- Update agents/checklists/Gate6-Validation.md

Before marking complete:
- Invoke superpowers:verification-before-completion
- Provide evidence for each claim

End with: "Gate6: PASS" or "Gate6: FAIL - {reason}"
```

**Checkpoint**: Update state.json with Gate6 status

---

### Stage 9: Security Review (security-gate-engineer agent)

**Agent**: `security-gate-engineer` (Task tool with subagent_type="security-gate-engineer")
**Gate**: `agents/checklists/Gate7-Security.md`
**Skills**: `superpowers:verification-before-completion`
**Input**: All code + threat model

**Prompt for agent**:
```
You are the Security Gate Engineer. Perform security audit.

Follow the checklist at agents/checklists/Gate7-Security.md.

Review:
1. Secret Management: No hardcoded secrets, all in Secret Manager
2. Authentication: Clerk integration secure, JWT validation correct
3. Authorization: RLS policies enforce user isolation
4. Input Validation: All inputs sanitized (Zod/Pydantic)
5. Dependencies: Run `npm audit` and `pip-audit`
6. OWASP Top 10: Check for common vulnerabilities

Create/Update:
- docs/deployment/security-checklist.md
- SBOM (software bill of materials) if needed
- Update agents/checklists/Gate7-Security.md

Before marking complete:
- Invoke superpowers:verification-before-completion

End with: "Gate7: PASS" or "Gate7: FAIL - {reason}"
```

**Checkpoint**: Update state.json with Gate7 status

---

### Stage 10: Code Review (requesting-code-review)

**Skills**:
- `superpowers:requesting-code-review`
- `superpowers:receiving-code-review` (for feedback)

**Prompt**:
```
Invoke superpowers:requesting-code-review

Present the implementation for review:
- Summary of changes
- Key architectural decisions
- Test coverage metrics
- Known limitations

If feedback received:
- Invoke superpowers:receiving-code-review
- Process feedback with technical rigor
- Do NOT blindly implement suggestions
- Verify feedback is technically sound
```

---

### Stage 11: Documentation (documentation agent)

**Agent**: `documentation` (custom agent)
**Input**: All artifacts

**Prompt for agent**:
```
You are the Documentation agent. Create/update documentation.

Required outputs:
1. API Documentation:
   - Ensure docs/api/openapi.yaml is complete
   - Add examples for each endpoint

2. Code Documentation:
   - Add JSDoc to all exported functions in shared/
   - Add docstrings to Python services

3. User Documentation:
   - Update README.md with current features
   - Update docs/SETUP.md with setup instructions
   - Verify quickstart.md is accurate

4. Package Documentation:
   - shared/README.md for each package
   - MIGRATION.md for reuse instructions

Do NOT over-document. Keep it concise and accurate.

End with: "Documentation: COMPLETE"
```

**Checkpoint**: Update state.json

---

### Stage 12: Deployment (devops-deployment-engineer agent)

**Agent**: `devops-deployment-engineer` (Task tool with subagent_type="devops-deployment-engineer")
**Gate**: `agents/checklists/Gate8-Deployment.md`
**Skills**: `superpowers:finishing-a-development-branch`
**Input**: All code + infrastructure configs

**Prompt for agent**:
```
You are the DevOps Deployment Engineer. Prepare for deployment.

FIRST: Invoke superpowers:finishing-a-development-branch
- Choose: merge directly, create PR, or cleanup

Follow the checklist at agents/checklists/Gate8-Deployment.md.

Environment: {staging OR production}

Actions:
1. Verify Docker builds: `docker build -t backend ./backend`
2. Verify frontend builds: `cd frontend && npm run build`
3. Create/update infrastructure configs:
   - backend/infrastructure/*.yaml (Cloud Run, Cloud Scheduler)
   - .github/workflows/*.yml (CI/CD)
4. Verify secrets are configured in target environment
5. Run deployment checklist

For staging:
- Deploy to staging environment
- Run smoke tests
- Report deployment URL

For production:
- Create deployment PR
- Await approval before deploying

Update agents/checklists/Gate8-Deployment.md with results.
End with: "Gate8: PASS - Deployed to {environment}" or "Gate8: FAIL - {reason}"
```

**Checkpoint**: Update state.json with Gate8 status + deployment URL

---

## Pipeline Completion

After all stages complete successfully:

```
╔═══════════════════════════════════════════════════════════════════╗
║                    PIPELINE COMPLETE                              ║
╠═══════════════════════════════════════════════════════════════════╣
║                                                                   ║
║  Feature: {feature_name}                                          ║
║  Duration: {start_time} → {end_time}                              ║
║                                                                   ║
║  GATE RESULTS                                                     ║
║  ────────────────────────────────────────────────────────────     ║
║  Gate0 PreSpec      ✅ PASS                                       ║
║  Gate1 Architecture ✅ PASS                                       ║
║  Gate2 Design       ✅ PASS                                       ║
║  Gate3 Test Design  ✅ PASS                                       ║
║  Gate4 Implementation ✅ PASS                                     ║
║  Gate5 QA           ✅ PASS (Coverage: 92%, Mutation: 84%)        ║
║  Gate6 Validation   ✅ PASS                                       ║
║  Gate7 Security     ✅ PASS                                       ║
║  Gate8 Deployment   ✅ PASS (Deployed to: staging)                ║
║                                                                   ║
║  ARTIFACTS CREATED                                                ║
║  ────────────────────────────────────────────────────────────     ║
║  - {list of files created/modified}                               ║
║                                                                   ║
║  NEXT STEPS                                                       ║
║  ────────────────────────────────────────────────────────────     ║
║  1. Review deployment at: {url}                                   ║
║  2. Run manual acceptance testing                                 ║
║  3. Promote to production when ready                              ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝
```

Update state.json:
```json
{
  "pipeline": {
    "status": "completed",
    "completed_at": "ISO_TIMESTAMP"
  }
}
```

---

## Configuration

The pipeline can be customized via `specs/{feature}/pipeline.yaml`:

```yaml
# pipeline.yaml - Pipeline configuration for this feature
feature: 001-mvp-uk-study-migration
spec: spec.md

# Superpowers integration
superpowers:
  enabled: true
  auto_invoke:
    brainstorming: true
    tdd: true
    debugging: true
    verification: true
    git_worktrees: true

stages:
  - name: architect
    gate: Gate1-Architecture
    skip: false

  - name: designer
    gate: Gate2-Design
    skip: false
    skills: [superpowers:writing-plans]

  - name: test-designer
    gate: Gate3-TestDesign
    skip: false
    skills: [superpowers:test-driven-development]

  - name: tasks
    type: skill
    skill: speckit.tasks

  - name: coder
    gate: Gate4-Implementation
    max_iterations: 3
    skills:
      - superpowers:using-git-worktrees
      - superpowers:test-driven-development
      - superpowers:executing-plans
      - superpowers:dispatching-parallel-agents

  - name: qa-tester
    gate: Gate5-QA
    thresholds:
      coverage: 90
      mutation: 80
    skills:
      - superpowers:systematic-debugging
      - superpowers:verification-before-completion

  - name: validator
    gate: Gate6-Validation

  - name: security
    gate: Gate7-Security

  - name: code-review
    skills:
      - superpowers:requesting-code-review
      - superpowers:receiving-code-review
    skip: false

  - name: documentation
    skip: false

  - name: deployment
    gate: Gate8-Deployment
    target: staging
    skills: [superpowers:finishing-a-development-branch]

# Stop conditions
stop_on_fail: true
max_qa_iterations: 3
```
