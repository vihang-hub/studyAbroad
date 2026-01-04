# study-abroad Development Guidelines

Auto-generated from all feature plans. Last updated: 2025-12-29

## Active Technologies
- TypeScript 5.3+ (Next.js 15+ App Router, Strict Mode) (001-mvp-uk-study-migration)
- None (stateless, all data in backend/Supabase) (001-mvp-uk-study-migration)

- TypeScript (Next.js 15+ App Router, Strict Mode), Python 3.12+ (001-mvp-uk-study-migration)

## Project Structure

```text
src/
tests/
```

## Commands

cd src [ONLY COMMANDS FOR ACTIVE TECHNOLOGIES][ONLY COMMANDS FOR ACTIVE TECHNOLOGIES] pytest [ONLY COMMANDS FOR ACTIVE TECHNOLOGIES][ONLY COMMANDS FOR ACTIVE TECHNOLOGIES] ruff check .

## Code Style

TypeScript (Next.js 15+ App Router, Strict Mode), Python 3.12+: Follow standard conventions

## Recent Changes
- 001-mvp-uk-study-migration: Added TypeScript 5.3+ (Next.js 15+ App Router, Strict Mode)

- 001-mvp-uk-study-migration: Added TypeScript (Next.js 15+ App Router, Strict Mode), Python 3.12+

<!-- MANUAL ADDITIONS START -->

## Speckit Workflow Requirements

**CRITICAL**: ALL development activities MUST be framed within the Speckit framework.

### Always Show Context

When suggesting next steps or asking questions, ALWAYS include:

```
┌─────────────────────────────────────────────────────────────────┐
│ SPECKIT CONTEXT                                                 │
├─────────────────────────────────────────────────────────────────┤
│ Current Gate: Gate{N} - {GateName}                              │
│ Agent: {agent_name}                                             │
│ Skill: {skill_name} (if applicable)                             │
│ Task: {current_task_id} - {description}                         │
└─────────────────────────────────────────────────────────────────┘
```

### Gate → Agent → Skill Mapping

| Gate | Name | Agent | Primary Skills |
|------|------|-------|----------------|
| Gate0 | Pre-Specification | - | `speckit.specify`, `superpowers:brainstorming` |
| Gate1 | Architecture | `architect` | - |
| Gate2 | Design | `designer` | `speckit.plan`, `superpowers:writing-plans` |
| Gate3 | Test Design | `test-designer` | `superpowers:test-driven-development` |
| Gate4 | Implementation | `coder` | `speckit.implement`, `superpowers:executing-plans`, `superpowers:dispatching-parallel-agents` |
| Gate5 | QA | `qa-tester` | `superpowers:systematic-debugging`, `superpowers:verification-before-completion` |
| Gate6 | Validation | `validator` | `superpowers:verification-before-completion` |
| Gate7 | Security | `security-gate-engineer` | - |
| Gate8 | Deployment | `devops-deployment-engineer` | `superpowers:finishing-a-development-branch` |

### Presenting Options

When presenting next step options, format as:

```
NEXT STEPS (Gate{N} - {GateName}):

[1] {Action description}
    → Agent: {agent}
    → Skill: {skill}
    → Command: {/command or "Use the {agent} agent to..."}

[2] {Action description}
    → Agent: {agent}
    → Skill: {skill}
    → Command: {/command}
```

### Activity Classification

Before ANY activity, determine:
1. Which gate does this belong to?
2. Which agent should handle it?
3. Which skill(s) apply?
4. Is this a new feature (→ /speckit.specify) or continuation?

### Session State

Always check `.specify/session/state.json` to understand:
- Current pipeline status
- Active gate and progress
- Next task in queue
- Recent activity

Use `/primer` at session start to load context.

### Bug Fixes and Ad-Hoc Work

Even bug fixes follow speckit:
- Simple bug → Gate4 (coder) + `superpowers:systematic-debugging`
- Test failures → Gate5 (qa-tester) + `superpowers:systematic-debugging`
- Security issue → Gate7 (security-gate-engineer)
- New feature request → Gate0 (start with /speckit.specify)

<!-- MANUAL ADDITIONS END -->
