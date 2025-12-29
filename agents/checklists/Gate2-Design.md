# Gate 2: Design Artifact Validation

**Purpose**: Ensure implementation plan and design artifacts are complete, constitutional, and executable.

**When**: After `/speckit.plan` completes, before `/speckit.tasks`.

**Owner**: Design Architect / Technical Lead

---

## PASS/FAIL Criteria

### PASS Requirements (All must be true)

- [ ] **Implementation Plan exists** at `specs/[###-feature-name]/plan.md`
  - Follows plan-template.md structure
  - All mandatory sections complete

- [ ] **Constitution Check PASSES**
  - All 6 checkboxes marked (Stack, Security, Engineering, Architecture, Naming, Prohibited)
  - Violations section either "None" or justified with rationale
  - If violations exist: ADR created in `docs/adr/` explaining exception

- [ ] **Technical Context is concrete**
  - No [NEEDS CLARIFICATION] placeholders remain
  - Language/version specified (Python 3.12+, Next.js 15+, etc.)
  - Dependencies listed match Constitution allowed tools
  - Performance goals quantified (e.g., "<200ms p95", "1000 req/s")

- [ ] **Project Structure defined**
  - Source tree shows real paths (not template placeholders)
  - Structure matches Constitution conventions (PascalCase components, kebab-case dirs, etc.)
  - Test directory layout specified (contract/, integration/, unit/)

- [ ] **Research artifacts complete** at `specs/[###-feature-name]/research.md`
  - Phase 0 research output present
  - Technology choices justified
  - Alternatives considered and documented

- [ ] **Data Model documented** at `specs/[###-feature-name]/data-model.md`
  - Key entities identified
  - Relationships specified
  - RLS strategy stated (if applicable)
  - Retention policy stated (30 days for reports per Constitution)

- [ ] **API Contracts defined** in `specs/[###-feature-name]/contracts/`
  - Request/response schemas documented
  - Error conditions specified
  - Authentication/authorization requirements stated

- [ ] **Quickstart documented** at `specs/[###-feature-name]/quickstart.md`
  - Setup instructions concrete
  - Validation steps testable
  - Success criteria measurable

### FAIL Conditions (Any triggers FAIL)

- Constitution Check has unchecked boxes
- Constitution violations without ADR justification
- Technical Context has unresolved placeholders
- Dependencies include tools not in Constitution allowed list
- Project Structure uses incorrect naming conventions
- Data Model missing RLS or retention policy
- API Contracts lack error handling specifications
- Quickstart instructions not executable

---

## Remediation Steps (If FAIL)

**Incomplete Constitution Check**:
1. Review each unchecked section
2. Either: Align design to Constitution OR create ADR for exception
3. Check all boxes or document violation

**Unresolved Placeholders**:
1. Run `/speckit.clarify` if specification unclear
2. Research and specify concrete values
3. Update plan.md with resolutions

**Missing RLS/Retention**:
1. Define Row-Level Security policies for each entity
2. Specify retention period (default: 30 days per Constitution)
3. Document in data-model.md

**Invalid Dependencies**:
1. Check dependency against Constitution Section 1 allowed tools
2. Either: Replace with allowed tool OR create ADR justifying exception
3. Update dependencies list

---

## Output

**If PASS**:
- Design approved for task breakdown
- Proceed to `/speckit.tasks`

**If FAIL**:
- Document specific gaps with artifact names
- Assign design refinement tasks
- Re-validate after updates

---

## Traceability Note

Gate 2 approval establishes the design baseline. All tasks and implementation must trace back to plan.md, data-model.md, and contracts/.

---

**Last Updated**: 2025-12-29 | **Constitution Version**: 1.0.0
