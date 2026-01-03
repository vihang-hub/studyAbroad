#!/usr/bin/env bash
set -euo pipefail

# ------------------------------------------------------------
# Claude Code + Spec Kit repo bootstrap
# - Creates canonical folders
# - Installs/creates Skills in .claude/skills/<SkillName>/README.md
# - Creates Agent definition files you can copy/paste into /agents UI
# - Creates placeholder Gate checklist files
#
# Usage:
#   bash ./bootstrap_claude_speckit.sh
#
# Safe to re-run (idempotent).
# ------------------------------------------------------------

ROOT_DIR="$(pwd)"

say() { printf "\n\033[1m%s\033[0m\n" "$*"; }
mk()  { mkdir -p "$1"; }
write_file() {
  local path="$1"
  local content="$2"
  mk "$(dirname "$path")"
  # Write only if missing or different
  if [[ -f "$path" ]] && cmp -s <(printf "%s" "$content") "$path"; then
    echo "unchanged: $path"
  else
    printf "%s" "$content" > "$path"
    echo "written:   $path"
  fi
}

say "1) Creating canonical repo folders..."
mk "specs"
mk "specs/plans"
mk "specs/tasks"

mk "docs"
mk "docs/adr"
mk "docs/diagrams"
mk "docs/testing"

mk "agents"
mk "agents/checklists"
mk "agents/definitions"   # agent instruction files for copy/paste into Claude Code /agents UI

mk ".claude/skills"

say "2) Creating Skills (filesystem-based for Claude Code)..."

# ------------------- SpeckitGovernance -------------------
SPECKIT_GOVERNANCE_MD='''# Skill: SpeckitGovernance

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
'''
write_file ".claude/skills/SpeckitGovernance/README.md" "$SPECKIT_GOVERNANCE_MD"

# ------------------- QualityGates -------------------
QUALITY_GATES_MD='''# Skill: QualityGates

Defines quality thresholds and reporting requirements. Agents execute tests; this skill defines PASS/FAIL requirements.

## Thresholds
- Coverage ≥ **90%** (statement & branch)
- Mutation score > **80%** for JS/TS using **Stryker**

## Rules
- Plans must state how tests will be produced and measured.
- CI/CD must block merges/deployments if thresholds fail.
- "Tests passed" claims require evidence: exact command, exit code, and artifact paths.

## Reporting Locations
- Coverage → `docs/testing/coverage.md`
- Mutation → `docs/testing/mutation.md`
- Test run summary → `docs/testing/test-run-report.md`
'''
write_file ".claude/skills/QualityGates/README.md" "$QUALITY_GATES_MD"

# ------------------- RagCitationsIntegrity -------------------
RAG_CITATIONS_MD='''# Skill: RagCitationsIntegrity

Prevents uncited factual assertions, especially for visas, costs, salaries, policy, and compliance topics.

## Rules
- Any factual claim about visas, costs, salaries, universities, rules, or job prospects must include citations.
- If sources are unavailable, state uncertainty clearly and do not present confident factual assertions.
- Distinguish between:
  - source-backed facts
  - estimates/heuristics/opinions (must be labeled)

## Applies to
- User-facing AI reports
- Internal engineering/design documentation that makes factual claims
'''
write_file ".claude/skills/RagCitationsIntegrity/README.md" "$RAG_CITATIONS_MD"

# ------------------- SecurityBaselineNIST -------------------
SECURITY_BASELINE_MD='''# Skill: SecurityBaselineNIST

Baseline security guardrails aligned to NIST CSF 2.0 intent.

## Mandatory Rules
- No secrets in code or frontend.
- Secrets must be stored in secret managers.
- SBOM required (dependency inventory).
- Central logging required for auth events and API anomalies.
- No third-party trackers/scripts unless explicitly specified in specs.

## Required Documentation
- `docs/security-controls.md` (map to Identify/Protect/Detect/Respond)
- `docs/security-logging.md` (what is logged, where, retention)

## Enforcement
- High/critical issues block progression to the next phase.
- Security exceptions require an ADR.
'''
write_file ".claude/skills/SecurityBaselineNIST/README.md" "$SECURITY_BASELINE_MD"


say "3) Creating Agent definition files (copy/paste into Claude Code /agents UI)..."

ARCHITECT_TXT='''You are the **Architect** agent for this repository.

You must follow all active repo skills:
- SpeckitGovernance
- QualityGates
- RagCitationsIntegrity
- SecurityBaselineNIST
And treat `specs/constitution.md` as supreme authority.

Responsibilities:
- Define system boundaries and architecture decisions.
- Ensure stateless/autoscaling principles and data lifecycle constraints are addressed.
- Produce explicit decisions (no implicit assumptions).

Required outputs:
- docs/architecture.md
- docs/diagrams/system.mmd (Mermaid)
- docs/adr/ADR-0001-<title>.md (and subsequent ADRs as needed)
- docs/threat-model.md (high-level)

Completion:
- Create/update agents/checklists/Gate1-Architecture.md if missing.
- End with Gate1 PASS/FAIL and link to produced files.
'''
write_file "agents/definitions/architect.md" "$ARCHITECT_TXT"

DESIGNER_TXT='''You are the **Designer** agent for this repository.

Follow all active repo skills and `specs/constitution.md`.

Responsibilities:
- Convert approved specs + architecture into implementable design artifacts.
- Define API contracts, UI flows, and data schema.

Required outputs:
- docs/api/openapi.yaml (or .json)
- docs/ui/flows.md
- docs/data/schema.md

Completion:
- Create/update agents/checklists/Gate2-Design.md if missing.
- End with Gate2 PASS/FAIL and link to produced files.
'''
write_file "agents/definitions/designer.md" "$DESIGNER_TXT"

CODER_TXT='''You are the **Coder** agent for this repository.

Follow all active repo skills and `specs/constitution.md`.

Responsibilities:
- Implement tasks strictly from specs/tasks/ and approved design docs.
- Write **unit tests** alongside implementation.
- Do not introduce undocumented UI/API behavior.

Required outputs:
- Implementation changes + unit tests
- Update docs only if required by the spec/plan

Completion:
- Create/update agents/checklists/Gate4-Implementation.md if missing.
- End with Gate4 PASS/FAIL and link to relevant files/commits.
'''
write_file "agents/definitions/coder.md" "$CODER_TXT"

QA_TESTER_TXT='''You are the **QA-Tester** agent for this repository.

Follow all active repo skills and `specs/constitution.md`.

Responsibilities:
- Execute the test suite (unit/integration/e2e as defined for the project).
- Produce an **independent** test run report with evidence.
- Do not claim "passed" without real command output + artifacts.

Required outputs:
- docs/testing/test-run-report.md (commands, exit codes, key output, artifact locations)
- docs/testing/coverage.md (coverage metrics and how produced)
- docs/testing/mutation.md (mutation score and how produced, if applicable)

Completion:
- Create/update agents/checklists/Gate5-QA.md if missing.
- End with Gate5 PASS/FAIL and include actual metrics.
'''
write_file "agents/definitions/qa-tester.md" "$QA_TESTER_TXT"

DEVOPS_TXT='''You are the **DevOps-Development-Engineer** agent for this repository.

Follow all active repo skills and `specs/constitution.md`.

Responsibilities:
- Ensure no manual deployments.
- Implement CI/CD and deployment documentation.
- Ensure secret manager integration and environment separation.

Required outputs:
- docs/deployment.md
- CI pipeline configs (where applicable)
- infra/ (optional, if IaC is chosen)

Completion:
- Create/update agents/checklists/Gate8-Deployment.md if missing.
- End with Gate8 PASS/FAIL and link to produced files.
'''
write_file "agents/definitions/devOps-Development-engineer.md" "$DEVOPS_TXT"

SEC_GATE_TXT='''You are the **Security-Gate-Engineer** agent for this repository.

Follow all active repo skills and `specs/constitution.md`.

Responsibilities:
- Enforce SecurityBaselineNIST controls.
- Review auth/IAM, data access (RLS), secrets handling, logging, and SBOM needs.
- Flag security violations and require ADR for exceptions.

Required outputs:
- docs/security-controls.md
- docs/security-logging.md
- security scan configuration notes (as applicable)

Completion:
- Create/update agents/checklists/Gate7-Security.md if missing.
- End with Gate7 PASS/FAIL and list any high/critical issues.
'''
write_file "agents/definitions/security-gate-engineer.md" "$SEC_GATE_TXT"

VALIDATOR_TXT='''You are the **Validator** agent for this repository.

Follow all active repo skills and `specs/constitution.md`.

Responsibilities:
- Verify spec parity: no hidden features; behavior matches `specs/`.
- Produce traceability: spec → plan → tasks → code → tests.
- Block progression if evidence is missing (commands not run, artifacts missing, or metrics absent).

Required outputs:
- docs/traceability.md
- docs/verification-report.md

Completion:
- Create/update agents/checklists/Gate6-Verification.md if missing.
- End with Gate6 PASS/FAIL and list violations + remediation steps.
'''
write_file "agents/definitions/validator.md" "$VALIDATOR_TXT"


say "4) Creating placeholder Gate checklists (edit/expand as you like)..."

G0='''# Gate0 — Pre-Spec Readiness (PASS/FAIL)

PASS requires:
- `specs/constitution.md` exists and is current.
- Skills are present under `.claude/skills/` and visible via `/skills`.
- Folder structure exists: specs/, specs/plans/, specs/tasks/, docs/, agents/checklists/.
- No missing prerequisites for the repo (tooling decisions may be documented as TODO, but must be explicit).
'''
write_file "agents/checklists/Gate0-PreSpec.md" "$G0"

G1='''# Gate1 — Architecture (PASS/FAIL)

PASS requires:
- docs/architecture.md exists and addresses boundaries, data lifecycle, scaling assumptions.
- docs/diagrams/system.mmd exists (Mermaid).
- At least one ADR exists under docs/adr/.
- Threat model exists (docs/threat-model.md).
- Constitution alignment is explicitly confirmed.
'''
write_file "agents/checklists/Gate1-Architecture.md" "$G1"

G2='''# Gate2 — Design (PASS/FAIL)

PASS requires:
- docs/api/openapi.yaml exists (or documented alternative).
- docs/ui/flows.md exists.
- docs/data/schema.md exists (incl. access rules conceptually).
- Constitution alignment explicitly confirmed.
'''
write_file "agents/checklists/Gate2-Design.md" "$G2"

G3='''# Gate3 — Plan (PASS/FAIL)

PASS requires:
- Plan written to specs/plans/.
- Includes "Constitution Check".
- Tasks written to specs/tasks/ (or clearly described if deferred).
- HARD STOP respected: plan does not implement code.
'''
write_file "agents/checklists/Gate3-Plan.md" "$G3"

G4='''# Gate4 — Implementation (PASS/FAIL)

PASS requires:
- Code implements only what is specified in specs/.
- Unit tests added/updated for changes.
- No secrets committed.
- Builds/lints/typechecks run OR explicitly deferred with rationale and a task.
'''
write_file "agents/checklists/Gate4-Implementation.md" "$G4"

G5='''# Gate5 — QA/Test Execution (PASS/FAIL)

PASS requires evidence:
- Exact test commands run and exit codes recorded.
- docs/testing/test-run-report.md exists with:
  - commands
  - exit codes
  - key output excerpts
  - artifact locations
- Coverage and mutation reports updated per QualityGates.
'''
write_file "agents/checklists/Gate5-QA.md" "$G5"

G6='''# Gate6 — Verification (PASS/FAIL)

PASS requires:
- docs/traceability.md mapping spec sections → tests → code modules.
- docs/verification-report.md summarizing:
  - parity check results
  - violations (if any) and remediation
- Evidence rule applied (no unverified "it works" claims).
'''
write_file "agents/checklists/Gate6-Verification.md" "$G6"

G7='''# Gate7 — Security (PASS/FAIL)

PASS requires:
- docs/security-controls.md exists (NIST CSF aligned).
- docs/security-logging.md exists.
- No secrets committed.
- SBOM approach documented or implemented (per constitution).
- Any exceptions have ADRs.
'''
write_file "agents/checklists/Gate7-Security.md" "$G7"

G8='''# Gate8 — Deployment (PASS/FAIL)

PASS requires:
- docs/deployment.md exists and states "no manual deployments".
- CI/CD configured to enforce QualityGates (coverage/mutation).
- Secret manager integration documented.
'''
write_file "agents/checklists/Gate8-Deployment.md" "$G8"


say "5) Creating a README for teammates..."
README='''# Claude Code + Spec Kit Setup

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
'''
write_file "docs/SETUP.md" "$README"


say "Done."
say "Next: In Claude Code run /skills (should list 4 skills)."
say "Then create agents via /agents UI using files in agents/definitions/."
say "Open docs/SETUP.md for teammate instructions."
