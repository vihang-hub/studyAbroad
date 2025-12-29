# Gate 0: Pre-Specification Readiness

**Purpose**: Ensure the project context is ready for feature specification work.

**When**: Before running `/speckit.specify` or creating any feature spec.

**Owner**: Product Owner / Specification Author

---

## PASS/FAIL Criteria

### PASS Requirements (All must be true)

- [ ] **Project Constitution exists** at `.specify/memory/constitution.md`
  - Version number present (format: X.Y.Z)
  - All 7 sections complete (Stack, Security, Testing, Architecture, Naming, Prohibited, Governance)

- [ ] **Active Skills are documented** in `.claude/skills/`
  - Minimum: SpeckitGovernance, QualityGates, SecurityBaselineNIST, RagCitationsIntegrity
  - Each skill has clear purpose and enforcement rules

- [ ] **Template infrastructure exists** in `.specify/templates/`
  - spec-template.md (feature specification)
  - plan-template.md (implementation planning)
  - tasks-template.md (task breakdown)

- [ ] **Directory structure ready**
  - `specs/` exists for specifications
  - `docs/` exists for documentation
  - `docs/adr/` exists for Architecture Decision Records
  - `agents/checklists/` exists for gate documents

- [ ] **Feature request is clear**
  - User has provided natural language description
  - Scope is bounded (not "build entire system")
  - No conflicting requirements in request

### FAIL Conditions (Any triggers FAIL)

- Constitution missing or incomplete (less than 7 sections)
- Required Skills not present or empty
- Templates missing or corrupted
- Feature request too vague ("make it better", "add AI")
- Feature request conflicts with Constitution constraints

---

## Remediation Steps (If FAIL)

**Missing Constitution**:
1. Run `/speckit.constitution` to create from scratch
2. Verify all 7 sections populated
3. Commit constitution with version 1.0.0

**Missing Skills**:
1. Create `.claude/skills/` directory
2. Copy required skill files from project template
3. Customize enforcement rules for project

**Missing Templates**:
1. Create `.specify/templates/` directory
2. Install standard speckit templates
3. Verify placeholders match Constitution requirements

**Vague Feature Request**:
1. Ask clarifying questions to user
2. Document answers before proceeding
3. Ensure scope is testable and bounded

---

## Output

**If PASS**: Proceed to `/speckit.specify` with user's feature description.

**If FAIL**: Document violations, remediate, and re-validate Gate 0.

---

**Last Updated**: 2025-12-29 | **Constitution Version**: 1.0.0
