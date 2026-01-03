# Speckit Stop - Graceful Session End

**Trigger**: User says "stop for the day", "pause", "save and quit", or runs `/speckit.stop`

**Purpose**: Safely checkpoint progress, summarize work done, and prepare for next session resume.

---

## Step 1: Save Current State

Update `.specify/session/state.json` with current progress:

```javascript
const state = JSON.parse(readFile('.specify/session/state.json'));

state.last_updated = new Date().toISOString();
state.session_end = {
  timestamp: new Date().toISOString(),
  reason: "graceful_stop",
  initiated_by: "user"
};

writeFile('.specify/session/state.json', JSON.stringify(state, null, 2));
```

---

## Step 2: Commit Work In Progress (Optional)

If there are uncommitted changes:

```bash
# Check for uncommitted work
git status --porcelain
```

**If changes exist**, ask user:

```
╔═══════════════════════════════════════════════════════════════════╗
║                 UNCOMMITTED CHANGES DETECTED                       ║
╠═══════════════════════════════════════════════════════════════════╣
║                                                                   ║
║  Modified files:                                                  ║
║  - backend/src/api/services/ai_service.py                        ║
║  - frontend/src/components/chat/ChatInput.tsx                    ║
║                                                                   ║
║  Options:                                                         ║
║  [1] Commit as WIP (recommended)                                  ║
║      → Creates: "WIP: {current_task} - session pause"             ║
║                                                                   ║
║  [2] Stash changes                                                ║
║      → Creates: git stash with descriptive message                ║
║                                                                   ║
║  [3] Leave uncommitted                                            ║
║      → Changes remain in working directory                        ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝
```

**If user chooses [1] - WIP Commit**:
```bash
git add -A
git commit -m "WIP: {last_task_description} - session pause

Session paused at: {timestamp}
Current gate: {current_gate}
Progress: {completed}/{total} tasks

Next task: {next_task_id} - {next_task_description}

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

**If user chooses [2] - Stash**:
```bash
git stash push -m "speckit-session-{timestamp}: {current_task}"
```

---

## Step 3: Generate Session Summary

Create a summary of today's work:

```
╔═══════════════════════════════════════════════════════════════════╗
║                    SESSION SUMMARY                                 ║
╠═══════════════════════════════════════════════════════════════════╣
║                                                                   ║
║  Session: {start_time} → {end_time} ({duration})                  ║
║  Feature: {feature_name}                                          ║
║                                                                   ║
║  ════════════════════════════════════════════════════════════     ║
║  WORK COMPLETED                                                   ║
║  ════════════════════════════════════════════════════════════     ║
║                                                                   ║
║  Tasks completed: {count}                                         ║
║  ────────────────────────────────────────────────────────────     ║
║  • T142 - Create cloud-scheduler-expire.yaml                      ║
║  • T143 - Create cloud-scheduler-delete.yaml                      ║
║  • T172a - Implement streaming SLA monitoring                     ║
║                                                                   ║
║  Gates progressed:                                                ║
║  ────────────────────────────────────────────────────────────     ║
║  • Gate4 Implementation: 86% → 92%                                ║
║  • Gate5 QA: Started coverage analysis                            ║
║                                                                   ║
║  Files modified: {count}                                          ║
║  ────────────────────────────────────────────────────────────     ║
║  • backend/infrastructure/cloud-scheduler-expire.yaml (new)       ║
║  • backend/infrastructure/cloud-scheduler-delete.yaml (new)       ║
║  • backend/src/api/services/ai_service.py (modified)              ║
║                                                                   ║
║  Tests: {passed}/{total} passing                                  ║
║                                                                   ║
║  ════════════════════════════════════════════════════════════     ║
║  TOMORROW'S STARTING POINT                                        ║
║  ════════════════════════════════════════════════════════════     ║
║                                                                   ║
║  Current gate: Gate4 Implementation (92%)                         ║
║  Next task: T172b - Add AI service structured logging             ║
║                                                                   ║
║  Remaining work:                                                  ║
║  ────────────────────────────────────────────────────────────     ║
║  • 15 tasks remaining in Gate4                                    ║
║  • Gate5 QA pending (coverage + mutation testing)                 ║
║  • Gate6-8 pending                                                ║
║                                                                   ║
║  Blockers/Notes:                                                  ║
║  ────────────────────────────────────────────────────────────     ║
║  • None currently                                                 ║
║                                                                   ║
║  ════════════════════════════════════════════════════════════     ║
║  RESUME COMMAND                                                   ║
║  ════════════════════════════════════════════════════════════     ║
║                                                                   ║
║  Next session, run:                                               ║
║                                                                   ║
║    /primer                                                        ║
║                                                                   ║
║  This will show current state and offer to continue.              ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝

Session saved. See you next time! 👋
```

---

## Step 4: Save Session Log

Append session details to `.specify/session/logs/sessions.jsonl`:

```json
{
  "session_id": "2025-01-03-001",
  "started_at": "2025-01-03T09:00:00Z",
  "ended_at": "2025-01-03T17:30:00Z",
  "duration_hours": 8.5,
  "feature": "001-mvp-uk-study-migration",
  "tasks_completed": ["T142", "T143", "T172a"],
  "tasks_attempted": 3,
  "gates_progressed": {
    "gate4_implementation": {"from": 86, "to": 92}
  },
  "commits": ["abc1234", "def5678"],
  "files_modified": 5,
  "files_created": 2,
  "tests": {"passed": 215, "failed": 0, "skipped": 3},
  "blockers": [],
  "notes": "",
  "next_task": "T172b",
  "end_reason": "graceful_stop"
}
```

---

## Step 5: Update State for Resume

Update state.json with resume context:

```json
{
  "last_updated": "2025-01-03T17:30:00Z",
  "pipeline": {
    "status": "paused",
    "current_stage": "gate4_implementation",
    "paused_at": "2025-01-03T17:30:00Z"
  },
  "resume_context": {
    "next_task": "T172b",
    "next_task_description": "Add AI service structured logging",
    "context_notes": "Working on Phase 6 performance monitoring tasks",
    "last_test_run": {
      "passed": 215,
      "failed": 0,
      "coverage": 70
    },
    "uncommitted_work": false,
    "wip_commit": "abc1234"
  }
}
```

---

## Optional: Create Handoff Note

If complex work is in progress, create a markdown handoff:

```markdown
<!-- .specify/session/handoff-2025-01-03.md -->

# Session Handoff: 2025-01-03

## Context
Working on Phase 6 performance monitoring for feature 001-mvp-uk-study-migration.

## What I Was Doing
Implementing SLA monitoring for the streaming AI service (T172a-c).
- T172a complete: First-token latency tracking added
- T172b next: Need to add structured logging for start/complete times

## Key Decisions Made
- Using structlog for Python backend (consistent with existing)
- P50/P95/P99 percentiles stored in memory, flushed every 5 minutes

## Watch Out For
- The ai_service.py has a new `SLAMonitor` class - tests not yet written
- Need to verify log format matches existing correlation ID pattern

## Files In Progress
- `backend/src/api/services/ai_service.py` - SLA monitoring added
- `backend/src/api/services/sla_monitor.py` - New file, needs tests

## To Resume
1. Run `/primer` to see current state
2. Continue from T172b
3. After T172b-c, run tests to verify SLA monitoring works
```

---

## Quick Stop (No Prompt)

For a fast exit without prompts, use `/speckit.stop --quick`:

1. Auto-commit as WIP (if changes exist)
2. Save state
3. Show brief summary
4. Exit

```
╔═══════════════════════════════════════════════════════════════════╗
║  ✓ Progress saved                                                 ║
║  ✓ WIP commit created: abc1234                                    ║
║  ✓ Next: T172b - Add AI service structured logging                ║
║                                                                   ║
║  Run /primer to resume. See you next time! 👋                     ║
╚═══════════════════════════════════════════════════════════════════╝
```

---

## State Diagram

```
                    ┌─────────────────┐
                    │   User working  │
                    └────────┬────────┘
                             │
                    "stop for the day"
                             │
                             ▼
                    ┌─────────────────┐
                    │ Check uncommitted│
                    │    changes      │
                    └────────┬────────┘
                             │
              ┌──────────────┼──────────────┐
              │              │              │
              ▼              ▼              ▼
        ┌─────────┐   ┌─────────┐   ┌─────────┐
        │   WIP   │   │  Stash  │   │  Leave  │
        │ Commit  │   │         │   │         │
        └────┬────┘   └────┬────┘   └────┬────┘
              │              │              │
              └──────────────┼──────────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │  Update state   │
                    │    .json        │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ Generate summary│
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │  Save session   │
                    │     log         │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ Create handoff  │
                    │ (if complex)    │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │  Display final  │
                    │    summary      │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │   Session End   │
                    │      👋         │
                    └─────────────────┘
```

---

## Triggers

The stop command activates when user says:
- `/speckit.stop`
- "stop for the day"
- "pause"
- "save and quit"
- "that's enough for today"
- "let's wrap up"
- "end session"
- "take a break"
- "see you tomorrow"
