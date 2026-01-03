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
║ Gate4 Implementation║ ⚠️ 86%  ║ {completed}/{total} tasks         ║
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
[████████████████████░░░░] 86% Complete

Current Stage: Gate4 Implementation
Last Completed: T168 - Run ESLint Airbnb on shared/
Next Task: T142 - Create cloud-scheduler-expire.yaml

Recent Activity:
• 2025-01-03: Fixed 17 failing frontend tests (a867d73)
• 2025-01-02: Fixed frontend test infrastructure (f1e5642)
• 2025-01-01: Updated monorepo configuration (e9f37ff)
```

## Step 3: Present Resume Options

Based on the session state, present these options:

```
╔═══════════════════════════════════════════════════════════════════╗
║                     RESUME OPTIONS                                ║
╠═══════════════════════════════════════════════════════════════════╣
║                                                                   ║
║  [1] CONTINUE where we left off                                   ║
║      → Resume from: T142 (Create cloud-scheduler-expire.yaml)     ║
║      → 27 tasks remaining                                         ║
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

## Step 4: If User Chooses "Continue"

Execute the appropriate next action:

1. **If in Gate4 (Implementation)**:
   - Run `/speckit.implement` to continue tasks
   - Update `state.json` after each completed task

2. **If in Gate5 (QA)**:
   - Spawn `qa-tester` agent
   - Run coverage and mutation tests

3. **If in any other gate**:
   - Spawn the appropriate agent from `state.json`

## Step 5: Checkpoint After Each Action

After EVERY significant action (task completion, gate pass/fail), update the session state:

```javascript
// Update state.json with:
{
  "last_updated": "ISO_TIMESTAMP",
  "gates.{current_gate}.status": "passed|in_progress|failed",
  "gates.{current_gate}.progress": { ... },
  "tasks.remaining": [...updated list...],
  "recent_activity": [...prepend new entry...]
}
```

---

## Quick Reference

### Read These Files (in order):

1. `.specify/session/state.json` - **Session state (FIRST)**
2. `.specify/memory/constitution.md` - Project rules
3. `specs/{feature}/spec.md` - Current specification
4. `specs/{feature}/plan.md` - Implementation plan
5. `specs/{feature}/tasks.md` - Task breakdown

### Available Commands:

| Command | Purpose |
|---------|---------|
| `/speckit.autopilot` | Run full automated pipeline |
| `/speckit.implement` | Execute remaining tasks |
| `/speckit.specify` | Create new specification |
| `/speckit.clarify` | Clarify existing spec |

### Agent Shortcuts:

Say any of these to invoke a specialized agent:
- "Use the architect agent to..."
- "Use the designer agent to..."
- "Use the coder agent to..."
- "Use the qa-tester agent to..."
- "Use the validator agent to..."
- "Use the security agent to..."
- "Use the devops agent to..."

---

## Session State File Location

```
.specify/session/state.json    ← Current progress
.specify/session/checkpoints/  ← Gate completion snapshots
.specify/session/logs/         ← Execution history
```

**IMPORTANT**: Always update `state.json` after:
- Completing a task
- Passing/failing a gate
- Starting a new stage
- Encountering a blocker
