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

#### Gate3: Test Design (TDD)
- [ ] Test strategy documented
- [ ] Acceptance criteria mapped to tests
- [ ] Test stubs written (should FAIL)
- [ ] Coverage targets set

#### Gate4: Implementation
- [ ] All tests passing
- [ ] Code follows style guide
- [ ] No security vulnerabilities
- [ ] Documentation updated

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

*Generated for Speckit + Superpowers Development System v1.0*
