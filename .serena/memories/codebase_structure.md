# Codebase Structure

## Repository Root: `/Users/vihang/projects/study-abroad/`

```
study-abroad/
├── .specify/                       # Speckit framework
│   ├── memory/
│   │   └── constitution.md        # Project constitution (v1.0.0)
│   ├── scripts/bash/              # Plan/task automation scripts
│   └── templates/                 # Spec/plan/task templates
├── .claude/                        # Claude Code configuration
│   ├── commands/                  # Custom skills (primer)
│   └── skills/                    # Repository skills
├── agents/                         # Agent definitions
│   ├── checklists/
│   │   ├── Gate1-Architecture.md  # Architecture quality gate (PASS)
│   │   ├── Gate2-Design.md        # Design quality gate (PASS)
│   │   └── Gate5-QA.md            # QA quality gate (for testing phase)
│   ├── commands/                  # Agent command definitions
│   └── roles/                     # Agent role definitions
├── docs/                           # Comprehensive documentation
│   ├── adr/                       # Architectural Decision Records (6 ADRs)
│   ├── api/
│   │   └── openapi.yaml           # Complete OpenAPI 3.1 specification
│   ├── architecture/
│   │   └── system-overview.md     # System architecture (v2.0.0)
│   ├── database/
│   │   ├── schema.sql             # PostgreSQL DDL (users, reports, payments)
│   │   └── rls-policies.sql       # Supabase Row-Level Security policies
│   ├── design/
│   │   ├── shared-component-interfaces.md  # TypeScript interfaces for shared packages
│   │   ├── error-handling.md      # Error codes, response format, correlation IDs
│   │   └── security.md            # NIST CSF 2.0, OWASP Top 10 mitigations
│   ├── diagrams/                  # Mermaid architecture diagrams (4 total)
│   ├── flows/                     # UX flow diagrams (4 Mermaid)
│   ├── deployment/
│   │   ├── .env.dev.template      # Dev environment configuration
│   │   ├── .env.test.template     # Test environment configuration
│   │   └── .env.production.template  # Production environment configuration
│   ├── testing/
│   │   ├── test-strategy.md       # Test pyramid, coverage goals, mutation testing
│   │   └── coverage-status.md     # Current coverage tracking
│   └── threat-model.md            # Security analysis (NIST CSF 2.0, OWASP Top 10)
├── frontend/                       # Next.js 15+ App Router application
│   ├── src/
│   │   ├── app/                   # App Router pages
│   │   ├── components/            # React components
│   │   ├── lib/                   # Utilities
│   │   └── middleware.ts          # Clerk authentication middleware
│   ├── tests/                     # Vitest tests
│   ├── .env.local                 # Local environment variables (gitignored)
│   ├── next.config.js             # Next.js configuration
│   ├── tailwind.config.ts         # Tailwind CSS configuration
│   ├── vitest.config.ts           # Vitest configuration
│   ├── stryker.conf.json          # Stryker Mutator configuration
│   └── package.json               # Frontend dependencies
├── backend/                        # FastAPI Python backend
│   ├── src/
│   │   ├── api/
│   │   │   ├── routes/            # API route handlers
│   │   │   ├── services/          # Business logic
│   │   │   └── models/            # Pydantic models
│   │   ├── config.py              # Pydantic settings (environment config)
│   │   ├── database/              # Database layer
│   │   └── logging_config.py      # Structlog configuration
│   ├── tests/                     # pytest tests
│   ├── Dockerfile                 # Cloud Run container definition
│   ├── pyproject.toml             # Python dependencies (Poetry)
│   └── pytest.ini                 # pytest configuration
├── shared/                         # Shared TypeScript packages
│   ├── config/                    # @study-abroad/shared-config
│   ├── feature-flags/             # @study-abroad/shared-feature-flags
│   ├── database/                  # @study-abroad/shared-database
│   ├── logging/                   # @study-abroad/shared-logging
│   ├── package.json               # Shared workspace configuration
│   ├── vitest.config.ts           # Shared Vitest configuration
│   └── stryker.conf.json          # Shared Stryker configuration
├── specs/                          # Feature specifications
│   └── 001-mvp-uk-study-migration/
│       ├── spec.md                # Feature specification (COMPLETE)
│       └── plan.md                # Implementation plan (COMPLETE)
├── infrastructure/                 # Infrastructure as Code
│   ├── docker/
│   └── scripts/
├── .github/
│   └── workflows/                 # CI/CD workflows
├── package.json                   # Monorepo root package.json (workspaces)
├── CLAUDE.md                      # Claude Code context (auto-updated)
└── README.md                      # Project overview
```

## Key Directories

### `/docs/` - Documentation Hub
All design documentation, ADRs, API specs, database schemas, security docs, and testing strategies.

### `/specs/` - Feature Specifications
Contains all feature specs following Speckit governance. Current spec: `001-mvp-uk-study-migration/`

### `/frontend/` - Next.js Application
Next.js 15+ App Router with TypeScript strict mode, Tailwind CSS, Clerk authentication.

### `/backend/` - FastAPI Backend
Python 3.12+ FastAPI backend with LangChain, Gemini AI integration, Stripe payments, Supabase database.

### `/shared/` - Shared Infrastructure Packages
Four reusable TypeScript packages:
1. `config/` - Environment configuration with Zod validation
2. `feature-flags/` - Feature flag evaluation
3. `database/` - Repository pattern with database adapters
4. `logging/` - Structured logging with rotation

### `/.specify/` - Speckit Framework
Constitutional governance, templates for specs/plans/tasks.

### `/.claude/` - Claude Code Configuration
Skills and commands for Claude Code.

### `/agents/` - Quality Gates
Checklists for Gate1 through Gate8 quality assurance.

## Workspace Configuration

Root `package.json` defines workspaces:
```json
{
  "workspaces": [
    "frontend",
    "shared"
  ]
}
```

Backend is Python-based (pyproject.toml) and not part of npm workspaces.

## Important Files

### Configuration Files
- `.env.local` - Frontend environment (gitignored)
- `.env` - Backend environment (gitignored)
- `.env.example` - Templates (committed)

### Build Outputs
- `frontend/.next/` - Next.js build (gitignored)
- `shared/dist/` - Compiled TypeScript (gitignored)
- `backend/__pycache__/` - Python cache (gitignored)

### Testing Artifacts
- `frontend/coverage/` - Frontend test coverage
- `shared/coverage/` - Shared package test coverage
- `backend/htmlcov/` - Backend test coverage HTML report
- `backend/.coverage` - Backend coverage data

## Monorepo Commands

All commands run from root (`/Users/vihang/projects/study-abroad/`):
- `npm run dev` - Run all dev servers
- `npm run build` - Build all workspaces
- `npm test` - Run all tests
- `npm run lint` - Lint all workspaces
