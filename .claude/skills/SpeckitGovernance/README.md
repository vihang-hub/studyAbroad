# Skill: SpeckitGovernance

This skill is always active for this repository.

## Supreme Authority
- `specs/constitution.md` supersedes all other conventions and outputs.
- If a conflict exists, the constitution wins.

## Canonical Locations (required)
- Specs → `specs/`
- Plans → `specs/plans/`
- Tasks → `specs/tasks/`
- Docs → `docs/`
- ADRs → `docs/adr/ADR-####-title.md`
- Diagrams → `docs/diagrams/*.mmd` (Mermaid)

## Governance Rules
- **No hidden features**: do not introduce UI, API behavior, workflows, tracking, or background jobs not explicitly specified in `specs/`.
- All plans MUST include a section titled **Constitution Check** that verifies:
  - stack alignment
  - security framework alignment
  - testing thresholds acknowledged
  - naming conventions applied
  - prohibited practices avoided (or justified)
- Constitution changes require:
  1) Proposed amendment + rationale
  2) Impact analysis
  3) Semantic version bump (MAJOR/MINOR/PATCH) with justification
  4) Migration path if incompatible changes

## Enforcement
- If any rule is violated, explicitly flag it and block progression to the next SDLC phase.
