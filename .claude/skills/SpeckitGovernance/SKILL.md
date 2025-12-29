# Skill: SpeckitGovernance

This skill is always active for this repository.

## Supreme Authority
- `specs/constitution.md` supersedes all other conventions and outputs.

## Enforced Conventions
- Specs must be written to `specs/`
- Plans must be written to `specs/plans/`
- Tasks must be written to `specs/tasks/`
- Architecture, design, and security documents must be written under `docs/`
- ADRs must be written to `docs/adr/ADR-####-title.md`
- Diagrams must be written to `docs/diagrams/*.mmd` (Mermaid)

## Governance Rules
- No hidden features: forbid UI, API behavior, or workflows not explicitly specified in `specs/`
- All plans must include a section titled **Constitution Check** that verifies
1. stack alignment
2. security framework alignment
3. testing thresholds acknowledged (but not executed)
4. naming conventions applied
5. prohibited practices avoided or justified
6. Provide a lightweight spec template with sections:

Purpose, Scope, Definitions, User journeys, Functional requirements, Non-functional requirements, Data model, API surface, Retention, Out of scope, Acceptance criteria
- Constitution changes require:
  1. Amendment proposal
  2. Impact analysis
  3. Semantic version bump
  4. Migration notes

## Enforcement
- If any rule is violated, explicitly flag it and block progression to the next SDLC phase.