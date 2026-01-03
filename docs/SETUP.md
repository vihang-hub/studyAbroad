# Claude Code + Spec Kit Setup

## What this script created
- Skills under `.claude/skills/` (visible via `/skills`)
- Agent definition files under `agents/definitions/` (copy/paste into `/agents` UI)
- Gate checklists under `agents/checklists/`
- Canonical folders under specs/ and docs/

## Next steps (manual, inside Claude Code)
1) Run `/skills` and confirm:
   - SpeckitGovernance
   - RagCitationsIntegrity
   - QualityGates
   - SecurityBaselineNIST

2) Create agents via `/agents` → Create new agent
   - Use the matching files in `agents/definitions/*.md` as the instruction text.

3) Write your first spec in `specs/`.
4) Use Spec Kit `/plan` (ensure it stops at planning and outputs tasks).
5) Run agents in order:
   Architect → Designer → Coder → QA-Tester → Validator → Security → DevOps
