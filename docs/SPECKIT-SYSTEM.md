# Speckit + Superpowers Development System

A comprehensive automated development workflow that combines specification-driven development with AI-powered agents and quality gates.

---

## Table of Contents

1. [Overview](#overview)
2. [Installation](#installation)
3. [Quick Start](#quick-start)
4. [Daily Workflow](#daily-workflow)
5. [Commands Reference](#commands-reference)
6. [Agents](#agents)
7. [Quality Gates](#quality-gates)
8. [Session Management](#session-management)
9. [Superpowers Integration](#superpowers-integration)
10. [Configuration](#configuration)
11. [Troubleshooting](#troubleshooting)
12. [Testing Best Practices](#testing-best-practices) (NEW)

---

## Overview

### What is this system?

This system automates the entire software development lifecycle from specification to deployment using specialized AI agents. You only need to interact during the specification phase - everything else runs automatically.

### Key Features

- **Specification-Driven**: Start with requirements, get working code
- **Multi-Agent Pipeline**: Specialized agents for each phase (architect, designer, coder, tester, etc.)
- **Quality Gates**: Checklists at each stage ensure nothing is missed
- **Session Continuity**: Checkpoint progress and resume across sessions
- **TDD Integration**: Test-driven development built into the workflow
- **Superpowers Skills**: Integrated debugging, planning, and verification skills

### Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                        USER INTERACTION                              │
│                                                                      │
│   /primer → /speckit.specify → "start implementation" → /speckit.stop│
└─────────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼
┌─────────────────────────────────────────────────────────────────────┐
│                     AUTOMATED PIPELINE                               │
│                                                                      │
│  Gate0 → Gate1 → Gate2 → Gate3 → Gate4 → Gate5 → Gate6 → Gate7 → Gate8│
│  Spec   Arch    Design  Tests   Code    QA      Valid   Sec    Deploy│
│                                                                      │
│  Each gate uses a specialized agent + follows a checklist           │
└─────────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      SESSION STATE                                   │
│                                                                      │
│  .specify/session/state.json - Tracks progress, enables resume      │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Installation

### Prerequisites

- macOS or Linux
- Claude Code CLI installed
- Git

### Install Script

Run the installation script to set up the system:

```bash
# Clone or download install-speckit-system.sh

# Make executable
chmod +x install-speckit-system.sh

# Run with project root and feature name
./install-speckit-system.sh /path/to/your/project your-feature-name

# Example
./install-speckit-system.sh ~/projects/my-app user-authentication
```

### What Gets Created

```
your-project/
├── .claude/
│   └── commands/
│       ├── primer.md              # Session start/resume
│       └── speckit.stop.md        # Graceful session end
├── .specify/
│   ├── constitution.md            # Project principles
│   ├── pipeline.yaml              # Pipeline configuration
│   ├── session/
│   │   ├── state.json             # Progress checkpoint
│   │   ├── README.md              # Session docs
│   │   └── logs/
│   │       └── sessions.jsonl     # Session history
│   └── templates/
│       ├── spec-template.md       # Specification template
│       └── plan-template.md       # Plan template
├── agents/
│   ├── definitions/               # Agent markdown files
│   │   ├── architect.md
│   │   ├── designer.md
│   │   ├── test-designer.md
│   │   ├── coder.md
│   │   ├── qa-tester.md
│   │   ├── validator.md
│   │   ├── security-gate-engineer.md
│   │   └── documentation.md
│   └── checklists/                # Gate checklists
│       ├── Gate0-PreSpec.md
│       ├── Gate1-Architecture.md
│       ├── Gate2-Design.md
│       ├── Gate3-TestDesign.md
│       ├── Gate4-Implementation.md
│       ├── Gate5-QA.md
│       ├── Gate6-Validation.md
│       ├── Gate7-Security.md
│       └── Gate8-Deployment.md
└── specs/
    └── {feature-name}/
        ├── spec.md                # Feature specification
        ├── plan.md                # Implementation plan
        └── tasks.md               # Task list
```

---

## Quick Start

### 1. Start a New Project

```bash
# Install the system
./install-speckit-system.sh ~/projects/my-app my-feature

# Navigate to project
cd ~/projects/my-app

# Start Claude Code
claude
```

### 2. Begin Session

```
/primer
```

This loads the project context and shows your options.

### 3. Create Specification

```
/speckit.specify

# Or clarify existing spec
/speckit.clarify
```

### 4. Start Automated Pipeline

Once your specification is complete:

```
/speckit.autopilot
```

Or simply say: **"start implementation"**

### 5. End Session

When you're done for the day:

```
/speckit.stop
```

Or say: **"stop for the day"**

---

## Daily Workflow

### Starting Your Day

```
┌─────────────────────────────────────────────────────────────────────┐
│  1. Open terminal, navigate to project                              │
│  2. Run: claude                                                     │
│  3. Run: /primer                                                    │
│  4. Choose: [1] CONTINUE where we left off                          │
│  5. Pipeline resumes automatically                                  │
└─────────────────────────────────────────────────────────────────────┘
```

### During the Day

The pipeline runs automatically. You'll see:

- Progress updates for each gate
- Test results
- Any blockers that need attention

If you need to intervene:

```
# Pause and get status
"what's the current status?"

# Run specific agent
"run the qa-tester agent"

# Debug an issue
"investigate the failing test in auth.test.ts"
```

### Ending Your Day

```
/speckit.stop
```

You'll see options:

```
╔═══════════════════════════════════════════════════════════════════╗
║                 UNCOMMITTED CHANGES DETECTED                       ║
╠═══════════════════════════════════════════════════════════════════╣
║  [1] Commit as WIP (recommended)                                   ║
║  [2] Stash changes                                                 ║
║  [3] Leave uncommitted                                             ║
╚═══════════════════════════════════════════════════════════════════╝
```

Then a session summary:

```
╔═══════════════════════════════════════════════════════════════════╗
║                    SESSION SUMMARY                                 ║
╠═══════════════════════════════════════════════════════════════════╣
║  Tasks completed: 5                                                ║
║  Gate4 progress: 86% → 92%                                         ║
║  Tests: 215/215 passing                                            ║
║  Next: T172b - Add AI service structured logging                   ║
╚═══════════════════════════════════════════════════════════════════╝
```

---

## Commands Reference

### Core Commands

| Command | Description | When to Use |
|---------|-------------|-------------|
| `/primer` | Load project context, show status, offer resume options | Start of every session |
| `/speckit.specify` | Create or update feature specification | Beginning of new feature |
| `/speckit.clarify` | Ask clarifying questions about spec | When requirements are unclear |
| `/speckit.plan` | Generate implementation plan from spec | After specification is complete |
| `/speckit.tasks` | Generate task list from plan | After planning is complete |
| `/speckit.implement` | Execute implementation tasks | After tasks are generated |
| `/speckit.autopilot` | Run full automated pipeline | When spec is ready, run everything |
| `/speckit.stop` | Graceful session end with checkpoint | End of work session |

### Trigger Phrases

These natural language phrases also trigger commands:

| Phrase | Equivalent Command |
|--------|-------------------|
| "start implementation" | `/speckit.autopilot` |
| "stop for the day" | `/speckit.stop` |
| "pause" | `/speckit.stop` |
| "save and quit" | `/speckit.stop` |
| "let's wrap up" | `/speckit.stop` |

---

## Agents

### Agent Definitions

Each agent is a specialized AI persona with specific responsibilities:

| Agent | Gate | Responsibilities |
|-------|------|------------------|
| **architect** | Gate1 | System design, ADRs, threat model |
| **designer** | Gate2 | API contracts, database schema, UX flows |
| **test-designer** | Gate3 | TDD test design, acceptance criteria mapping |
| **coder** | Gate4 | Implementation following TDD, clean code |
| **qa-tester** | Gate5 | Test execution, coverage, mutation testing |
| **validator** | Gate6 | Spec parity, traceability, compliance |
| **security-gate-engineer** | Gate7 | Security audit, SBOM, vulnerability scan |
| **documentation** | Gate4+ | API docs, README, user guides |
| **devops-deployment-engineer** | Gate8 | CI/CD, infrastructure, deployment |

### Using Agents Manually

```bash
# Run specific agent using Task tool
"run the architect agent to review the current design"
"use the qa-tester agent to check coverage"
"launch the security-gate-engineer for audit"
```

### Agent Definition Format

Agent definitions live in `agents/definitions/` as markdown files:

```markdown
# Agent: {Name}

You are the **{Name}** agent for this repository.

## Responsibilities
- Task 1
- Task 2

## Required Inputs
- spec.md
- plan.md

## Required Outputs
- output1.md
- output2.yaml

## Checklist
Reference: agents/checklists/Gate{N}-{Name}.md
```

---

## Quality Gates

### Gate Overview

```
Gate0 ─────► Gate1 ─────► Gate2 ─────► Gate3 ─────► Gate4
PreSpec      Arch         Design       TestDesign   Implement
   │            │            │            │            │
   ▼            ▼            ▼            ▼            ▼
Spec.md     ADRs         OpenAPI      Test stubs   Working code
            Threat       Schema       Coverage     Passing tests
            model        Flows        plan

Gate5 ─────► Gate6 ─────► Gate7 ─────► Gate8
QA           Validate     Security     Deploy
   │            │            │            │
   ▼            ▼            ▼            ▼
Coverage     Spec         SBOM         CI/CD
Mutation     parity       Audit        Staging
report       Trace        Scan         Production
```

### Gate Details

#### Gate0: Pre-Specification
- [ ] Problem statement defined
- [ ] User stories captured
- [ ] Acceptance criteria written
- [ ] Out of scope documented

#### Gate1: Architecture
- [ ] System overview diagram
- [ ] ADR for each major decision
- [ ] Threat model created
- [ ] Data lifecycle documented

#### Gate2: Design
- [ ] OpenAPI spec complete
- [ ] Database schema defined
- [ ] RLS policies documented
- [ ] UX flows diagrammed
- [ ] **Contract testing requirements defined** (NEW)
- [ ] **Auth contract documented** (NEW)

#### Gate3: Test Design (TDD)
- [ ] **Test infrastructure created first** (NEW)
- [ ] **Mock inventory complete** (NEW)
- [ ] **Integration boundary tests defined** (NEW)
- [ ] **Environment matrix identified** (NEW)
- [ ] Test strategy documented
- [ ] Acceptance criteria mapped to tests
- [ ] Test stubs written (should FAIL)
- [ ] Coverage targets set

#### Gate4: Implementation
- [ ] All tests passing
- [ ] Code follows style guide
- [ ] No security vulnerabilities
- [ ] Documentation updated
- [ ] **Continuous validation checkpoints passed** (NEW)
- [ ] **No deferred type/build errors** (NEW)

#### Gate5: QA
- [ ] Coverage >= 90%
- [ ] Mutation score >= 80%
- [ ] All edge cases tested
- [ ] Performance benchmarks met

#### Gate6: Validation
- [ ] Spec parity verified
- [ ] All acceptance criteria met
- [ ] Traceability complete
- [ ] User acceptance passed

#### Gate7: Security
- [ ] SBOM generated
- [ ] No critical vulnerabilities
- [ ] Secrets properly managed
- [ ] Auth/AuthZ verified

#### Gate8: Deployment
- [ ] CI/CD pipeline working
- [ ] Staging deployment successful
- [ ] Rollback tested
- [ ] Production deployed

---

## Session Management

### State File

The system tracks progress in `.specify/session/state.json`:

```json
{
  "version": "1.0.0",
  "feature": "your-feature-name",
  "pipeline": {
    "status": "in_progress",
    "current_stage": "implementation"
  },
  "gates": {
    "gate4_implementation": {
      "status": "in_progress",
      "progress": {
        "total_tasks": 50,
        "completed_tasks": 35,
        "percentage": 70
      },
      "next_task": "T036"
    }
  },
  "resume_context": {
    "next_task": "T036",
    "next_task_description": "Add input validation",
    "context_notes": "Working on API endpoints",
    "uncommitted_work": false
  }
}
```

### Session Logs

Session history is stored in `.specify/session/logs/sessions.jsonl`:

```json
{
  "session_id": "2025-01-03-001",
  "started_at": "2025-01-03T09:00:00Z",
  "ended_at": "2025-01-03T17:30:00Z",
  "tasks_completed": ["T030", "T031", "T032"],
  "gates_progressed": {"gate4_implementation": {"from": 60, "to": 70}},
  "end_reason": "graceful_stop"
}
```

### Resume Options

When running `/primer`, you'll see:

```
╔═══════════════════════════════════════════════════════════════════╗
║                     RESUME OPTIONS                                ║
╠═══════════════════════════════════════════════════════════════════╣
║  [1] CONTINUE where we left off                                   ║
║      → Resume T036: Add input validation                          ║
║                                                                   ║
║  [2] RUN specific agent                                           ║
║      → architect, designer, coder, qa-tester, etc.                ║
║                                                                   ║
║  [3] RESTART from a specific gate                                 ║
║      → Gate1, Gate2, Gate3, etc.                                  ║
║                                                                   ║
║  [4] START new feature                                            ║
║      → Begin fresh specification                                  ║
║                                                                   ║
║  [5] VIEW detailed status                                         ║
║      → See all gates, tasks, blockers                             ║
╚═══════════════════════════════════════════════════════════════════╝
```

---

## Superpowers Integration

### What are Superpowers?

Superpowers is a Claude Code skills library from Obra that provides specialized workflows for common development tasks.

### Skill → Gate Mapping

| Superpowers Skill | When to Use | Speckit Gate |
|-------------------|-------------|--------------|
| `superpowers:brainstorming` | Before specification | Pre-Gate0 |
| `superpowers:writing-plans` | During planning | Gate2 → Gate3 |
| `superpowers:using-git-worktrees` | Before implementation | Gate4 start |
| `superpowers:test-driven-development` | During implementation | Gate4 |
| `superpowers:executing-plans` | Task execution | Gate4 |
| `superpowers:dispatching-parallel-agents` | Independent tasks | Gate4 |
| `superpowers:systematic-debugging` | When tests fail | Gate4/Gate5 |
| `superpowers:verification-before-completion` | Before marking done | Every gate |
| `superpowers:requesting-code-review` | After implementation | Gate5/Gate6 |
| `superpowers:finishing-a-development-branch` | Ready to merge | Gate8 |

### Automatic Skill Invocation

The `/speckit.autopilot` command automatically invokes appropriate Superpowers skills at each stage:

```
Gate3 (Test Design):
  → Invoke: superpowers:test-driven-development
  → Write tests BEFORE implementation

Gate4 (Implementation):
  → Invoke: superpowers:executing-plans
  → Invoke: superpowers:dispatching-parallel-agents (for independent tasks)

Gate4/5 (Debugging):
  → Invoke: superpowers:systematic-debugging
  → Follow structured debugging workflow

Every Gate Completion:
  → Invoke: superpowers:verification-before-completion
  → Verify before claiming done
```

---

## Configuration

### Pipeline Configuration

Edit `.specify/pipeline.yaml`:

```yaml
pipeline:
  name: "Feature Development Pipeline"
  version: "1.0.0"

stages:
  - name: specification
    gate: Gate0-PreSpec
    agent: null  # Human interaction

  - name: architecture
    gate: Gate1-Architecture
    agent: architect
    auto_proceed: true

  - name: design
    gate: Gate2-Design
    agent: designer
    auto_proceed: true

  # ... more stages

settings:
  auto_commit: true
  test_on_save: true
  coverage_threshold: 90
  mutation_threshold: 80
```

### Constitution

Edit `.specify/constitution.md` to define project principles:

```markdown
# Project Constitution

## Core Principles
1. Test-driven development
2. Security by design
3. Clean code standards

## Technology Choices
- Frontend: Next.js 15+
- Backend: FastAPI
- Database: Supabase

## Quality Standards
- Coverage: >= 90%
- Mutation score: >= 80%
- No critical vulnerabilities
```

---

## Troubleshooting

### Common Issues

#### "Pipeline stuck at gate"

```bash
# Check current status
/primer

# View detailed gate status
"show me Gate4 status in detail"

# Check for blockers
cat .specify/session/state.json | jq '.tasks.blocked'
```

#### "Tests failing"

```bash
# Invoke debugging skill
"use systematic-debugging to investigate"

# Or manually run tests
npm test
pytest
```

#### "Can't resume from previous session"

```bash
# Check state file exists
cat .specify/session/state.json

# Reset if corrupted
"reset session state"
```

#### "Agent not following checklist"

```bash
# Verify checklist exists
cat agents/checklists/Gate4-Implementation.md

# Run agent with explicit checklist
"run coder agent, strictly follow Gate4-Implementation checklist"
```

### Debug Mode

For verbose output:

```bash
# Set debug mode in Claude Code
export CLAUDE_DEBUG=1

# Or in session
"enable verbose logging"
```

---

## Examples

### Example 1: New Feature

```bash
# Day 1: Specification
/primer
/speckit.specify
# Describe your feature, answer clarifying questions

# Day 1: Start Implementation
"start implementation"
# Pipeline runs through Gate1-4

# Day 1: End of day
/speckit.stop
# Choose [1] Commit as WIP

# Day 2: Resume
/primer
# Choose [1] CONTINUE
# Pipeline continues from where it stopped
```

### Example 2: Bug Fix

```bash
/primer
"There's a bug in the login flow"

# System will:
# 1. Invoke superpowers:systematic-debugging
# 2. Identify the issue
# 3. Write a failing test
# 4. Fix the bug
# 5. Verify test passes
```

### Example 3: Security Audit

```bash
/primer
"run security gate"

# System will:
# 1. Launch security-gate-engineer agent
# 2. Generate SBOM
# 3. Scan for vulnerabilities
# 4. Audit secrets management
# 5. Produce security report
```

---

## Testing Best Practices

The speckit system enforces testing discipline through structured gates. These practices prevent common issues that block testing and cause integration failures.

### Test Infrastructure First (Gate3)

**Problem**: Tests written before infrastructure exists get blocked by missing mocks.

**Solution**: Gate3 now requires test infrastructure BEFORE writing tests:

1. **Identify all dependencies** that need mocking (auth, APIs, databases, shared packages)
2. **Create mock files** in `tests/mocks/`
3. **Verify infrastructure** by running test framework with no tests
4. **Only then** write actual tests

```bash
# Verify infrastructure works before writing tests
npx vitest run --passWithNoTests  # Should exit 0, not error
```

### Integration Boundary Testing (Gate3)

**Problem**: Components work in isolation but fail when integrated.

**Solution**: Test boundaries between major components explicitly:

| Boundary | What to Test |
|----------|-------------|
| Auth → API | Token attached, auth errors handled |
| Frontend → Backend | Paths match, types align |
| Config → Runtime | Values available in all contexts |

### Environment Matrix Testing (Gate3)

**Problem**: Code works on server but fails on client (or vice versa).

**Solution**: Test in all target environments:

```typescript
// Client environment test
/** @vitest-environment jsdom */
describe('Client', () => { ... });

// Server environment test
/** @vitest-environment node */
describe('Server', () => { ... });
```

### Contract Testing (Gate2)

**Problem**: Frontend expects `/api/reports`, backend serves `/reports`.

**Solution**: Define contracts in Gate2 BEFORE implementation:

1. Document exact API paths
2. Document request/response types
3. Document auth header format
4. Verify contracts match in tests

### Continuous Validation (Gate4)

**Problem**: Type errors and build failures accumulate during implementation.

**Solution**: Mandatory validation checkpoints every 3-5 tasks:

```bash
npm run typecheck && npm run lint && npm run build
```

**No deferral allowed** for type errors or build failures.

### Common Testing Issues & Solutions

| Issue | Symptom | Solution |
|-------|---------|----------|
| Missing mocks | "Module not found" errors | Create mocks in Gate3 Phase 1 |
| Auth not sent | 401 errors after login | Test auth → API boundary |
| Type mismatch | Build fails at end | Run validation checkpoints |
| Path mismatch | 404 errors | Define contracts in Gate2 |
| Env context | Works on server, fails on client | Test environment matrix |

---

## Cross-Layer Integration Testing (NEW)

These checks prevent the most common integration bugs found during manual testing. Added based on retrospective analysis of debugging sessions.

### The 7 Classes of Integration Bugs

| Issue | Category | Symptom | Prevention |
|-------|----------|---------|------------|
| #1 | Browser Compatibility | Chrome modal auth fails | Don't use `mode="modal"` for Clerk SignInButton |
| #2 | Type Conversion | Pydantic HttpUrl breaks Supabase | Convert HttpUrl to `str` at library boundaries |
| #3 | Feature Flags | DB connection refused in dev | Check `_is_*_enabled()` before external calls |
| #4 | Config Fields | AttributeError on settings | Define ALL config fields referenced in code |
| #5 | Field Naming | JSON parsing errors | Use snake_case consistently in API responses |
| #6 | Auth Pattern | 401 errors on protected pages | Use `useAuthenticatedApi()` hook, not raw fetch |
| #7 | Mock Data | "Content not available" errors | Mock data must be COMPLETE, never `None` |

### Gate4: Cross-Layer Integration Checks

Add these checks to every Gate4 implementation:

#### Cross-Library Type Safety
```python
# ❌ BAD - HttpUrl incompatible with Supabase client
supabase.storage.from_("bucket").upload(file, settings.API_URL)

# ✅ GOOD - Convert to string first
supabase.storage.from_("bucket").upload(file, str(settings.API_URL))
```

#### Feature Flag Pattern
```python
# REQUIRED pattern for every service function
async def get_report(report_id: str, user_id: str) -> Report:
    if not _is_supabase_enabled():
        return _create_mock_report()  # Mock MUST be complete
    return await _get_real_report()
```

#### API Field Naming
```python
# All response models MUST use snake_case
class ReportResponse(BaseModel):
    report_id: str      # ✅ snake_case
    created_at: datetime  # ✅ snake_case
    # reportId: str     # ❌ WRONG - camelCase
```

### Gate5: Integration Testing Tasks

| Task | Description | Priority |
|------|-------------|----------|
| T180 | Cross-Browser Compatibility Testing | HIGH |
| T181 | API Contract Validation Testing | CRITICAL |
| T182 | Architectural Pattern Compliance Testing | HIGH |
| T183 | Mock/Dev Mode Data Integrity Testing | HIGH |
| T184 | Cross-Library Type Safety Testing | MEDIUM |
| T185 | Configuration Completeness Testing | MEDIUM |
| T186 | Regression Test Suite for Debugging Fixes | HIGH |

### Gate6: Cross-Layer Verification Checklists

Before marking Gate6 PASS, verify:

- [ ] Backend uses snake_case for ALL response fields
- [ ] Frontend types match backend field names exactly
- [ ] All `HttpUrl` types converted to `str` before library calls
- [ ] All service functions check feature flags before external calls
- [ ] All mock return values have complete data (not `None`)
- [ ] All protected endpoints use `Depends(get_current_user)`
- [ ] All frontend API calls use `useAuthenticatedApi()` hook
- [ ] No `mode="modal"` for Clerk SignInButton (Chrome incompatible)
- [ ] Every `settings.FIELD_NAME` reference has corresponding config field

### Regression Test Suite

Create `backend/tests/test_debugging_regressions.py` with tests for each issue class:

```python
class TestIssue2HttpUrlTypeConversion:
    """Prevent HttpUrl → Supabase incompatibility"""
    def test_httpurl_can_be_converted_to_string(self): ...

class TestIssue3FeatureFlagsInServices:
    """Prevent dev mode DB connection errors"""
    def test_report_service_checks_supabase_flag(self): ...

class TestIssue5SnakeCaseFieldNaming:
    """Prevent JSON parsing errors from naming mismatch"""
    def test_report_model_uses_snake_case(self): ...

class TestIssue7MockReportContentCompleteness:
    """Prevent 'content not available' errors in dev mode"""
    def test_mock_report_content_is_not_none(self): ...
```

---

## License

This system is provided as-is for development automation purposes.

---

## Contributing

To extend this system:

1. Add new agents in `agents/definitions/`
2. Add new checklists in `agents/checklists/`
3. Update pipeline stages in `.specify/pipeline.yaml`
4. Add new commands in `.claude/commands/`

---

*Generated for Speckit + Superpowers Development System v1.2*

---

## Changelog

### v1.2 (2026-01-04)
- **NEW SECTION**: Cross-Layer Integration Testing - 7 classes of integration bugs with prevention strategies
- **Gate4**: Added cross-layer integration checks (type safety, feature flags, field naming, mock completeness)
- **Gate5**: Added Phase 5 integration testing with 7 new tasks (T180-T186)
- **Gate6**: Added cross-layer verification checklists (9 mandatory checks before PASS)
- **Regression Tests**: Created `backend/tests/test_debugging_regressions.py` (20 tests covering 5 issue classes)
- **Docs**: Documented the 7 classes of bugs from debugging retrospective

### v1.1 (2026-01-04)
- **Gate2**: Added contract testing requirements (API paths, auth contracts, error formats)
- **Gate3**: Added test infrastructure prerequisites (mock inventory, verification step)
- **Gate3**: Added integration boundary testing (auth→API, frontend→backend)
- **Gate3**: Added environment matrix testing (server/client/edge)
- **Gate4**: Added continuous validation checkpoints (type, lint, build after every batch)
- **Gate4**: Removed "deferral" escape hatch for type/build errors
- **Docs**: Added Testing Best Practices section with common issues & solutions

### v1.0 (2025-12-28)
- Initial release with 8-gate pipeline
- Superpowers integration
- Session management
