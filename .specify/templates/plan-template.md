# Implementation Plan: [FEATURE]

**Branch**: `[###-feature-name]` | **Date**: [DATE] | **Spec**: [link]
**Input**: Feature specification from `/specs/[###-feature-name]/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

[Extract from feature spec: primary requirement + technical approach from research]

## Technical Context
BOOTSTRAP (mandatory):
- Treat `specs/constitution.md` as supreme authority.
- Apply all repository skills from `.claude/skills/`:
  - SpeckitGovernance
  - QualityGates
  - RagCitationsIntegrity
  - SecurityBaselineNIST
- Enforce: no hidden features, UK-only MVP, 30-day retention, £2.99 per query, and citations required.
- All outputs must follow SpeckitGovernance file locations:
  - Spec → specs/
  - Plan → specs/plans/
  - Tasks → specs/tasks/
<!--
  ACTION REQUIRED: Replace the content in this section with the technical details
  for the project. The structure here is presented in advisory capacity to guide
  the iteration process.
-->

**Language/Version**: [e.g., Python 3.11, Swift 5.9, Rust 1.75 or NEEDS CLARIFICATION]  
**Primary Dependencies**: [e.g., FastAPI, UIKit, LLVM or NEEDS CLARIFICATION]  
**Storage**: [if applicable, e.g., PostgreSQL, CoreData, files or N/A]  
**Testing**: [e.g., pytest, XCTest, cargo test or NEEDS CLARIFICATION]  
**Target Platform**: [e.g., Linux server, iOS 15+, WASM or NEEDS CLARIFICATION]
**Project Type**: [single/web/mobile - determines source structure]  
**Performance Goals**: [domain-specific, e.g., 1000 req/s, 10k lines/sec, 60 fps or NEEDS CLARIFICATION]  
**Constraints**: [domain-specific, e.g., <200ms p95, <100MB memory, offline-capable or NEEDS CLARIFICATION]  
**Scale/Scope**: [domain-specific, e.g., 10k users, 1M LOC, 50 screens or NEEDS CLARIFICATION]

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

Verify compliance with Study Abroad Constitution (v1.0.0):

- [ ] **Technical Stack Alignment**: Technology choices align with Section 1 requirements
  (Next.js 15+, TypeScript, Tailwind, Python 3.12+, FastAPI, Supabase, etc.)
- [ ] **Security Framework**: Security requirements follow NIST CSF 2.0 (Section 2)
  (SBOM, IAM, zero-exposure secrets, encryption standards, logging)
- [ ] **Engineering Rigor**: Testing strategy meets Section 3 standards
  (100% spec faithfulness, mutation testing >80%, code coverage ≥90%)
- [ ] **Architectural Principles**: Design follows Section 4 requirements
  (Stateless autoscaling, RAG integrity with citations, user-mapped persistence)
- [ ] **Naming & Structure**: Conventions follow Section 5 guidelines
  (PascalCase components, kebab-case dirs, snake_case DB, RESTful/GraphQL APIs)
- [ ] **Prohibited Practices**: No violations of Section 6 constraints
  (No assumptions, no shadow IT, no manual deployments)

**Violations Requiring Justification**: [List any deviations and rationale, or "None"]

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)
<!--
  ACTION REQUIRED: Replace the placeholder tree below with the concrete layout
  for this feature. Delete unused options and expand the chosen structure with
  real paths (e.g., apps/admin, packages/something). The delivered plan must
  not include Option labels.
-->

├── agents
│   ├── checklists
│   ├── commands
│   └── roles
├── apps
│   └── study-abroad
├── ARCHITECTURE.md
├── backend
│   ├── coverage.json
│   ├── Dockerfile
│   ├── pyproject.toml
│   ├── src
│   ├── supabase
│   └── tests
├── CLAUDE.md
├── DATABASE.md
├── docs
│   ├── adr
│   ├── DATABASE-COMMANDS.md
│   ├── diagrams
│   ├── guides
│   ├── setup
│   ├── testing
│   └── testing-strategy.md
├── frontend
│   ├── components.json
│   ├── coverage
│   ├── next-env.d.ts
│   ├── next.config.js
│   ├── package.json
│   ├── postcss.config.js
│   ├── src
│   ├── stryker.conf.json
│   ├── tailwind.config.ts
│   ├── tests
│   ├── tsconfig.json
│   └── vitest.config.ts
├── infrastructure
│   ├── docker
│   └── scripts
├── Makefile
├── MONOREPO-MIGRATION.md
├── package-lock.json
├── package.json
├── packages
│   ├── shared-auth
│   ├── shared-db
│   ├── shared-types
│   └── shared-ui
├── README.md
├── scripts
├── SETUP-DATABASE.md
├── SETUP-LOCAL-DEV.md
├── shared
│   ├── coverage
│   ├── dist
│   ├── package.json
│   ├── src
│   ├── stryker.conf.json
│   ├── tests
│   ├── tsconfig.json
│   └── vitest.config.ts
├── specs
│   ├── 001-mvp-uk-study-migration
│   ├── plans
│   └── tasks


**Shared components structure**:

Shared
├── auth
│   ├── backend
│   │   └── index.ts
│   ├── database
│   │   └── index.ts
│   ├── hooks
│   │   └── index.ts
│   ├── package.json
│   ├── README.md
│   ├── types
│   │   └── index.ts
│   └── ui-components
│       └── index.tsx
├── package.json
├── payments
│   ├── backend
│   │   └── index.ts
│   ├── database
│   │   └── index.ts
│   ├── hooks
│   │   └── index.ts
│   ├── package.json
│   ├── README.md
│   ├── types
│   │   └── index.ts
│   └── ui-components
│       └── index.tsx
├── README.md
├── tree-shared.md
├── types
│   └── README.md
├── ui-components
│   └── README.md
└── utils
    └── README.md


**Structure Decision**: [Document the selected structure and reference the real
directories captured above]

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |
