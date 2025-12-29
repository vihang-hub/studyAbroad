# StudyAbroad Monorepo

A monorepo containing multiple applications with shared packages for authentication, database, and UI components.

## Structure

```
StudyAbroad/
├── apps/                      # Individual applications
│   └── study-abroad/          # Study Abroad application
├── packages/                  # Shared/reusable packages
│   ├── shared-auth/           # Authentication (Google OAuth)
│   ├── shared-db/             # Database utilities & schemas
│   └── shared-ui/             # UI components
├── infrastructure/            # Shared infrastructure
│   ├── docker/                # Docker configurations
│   └── scripts/               # Automation scripts
└── docs/                      # Documentation
```

See [ARCHITECTURE.md](./ARCHITECTURE.md) for detailed architecture documentation.

## Quick Start

### Prerequisites

- **Node.js** 18+ and npm
- **Python** 3.12+
- **Docker** & Docker Compose
- **PostgreSQL** 16+ (or use Docker)

### 1. Install Dependencies

```bash
# Install all workspace dependencies
npm install
```

### 2. Start Shared Infrastructure

```bash
# Start PostgreSQL and pgAdmin
cd infrastructure/docker
docker-compose up -d
```

### 3. Run an Application

```bash
# Study Abroad app
cd apps/study-abroad

# Setup environment
cp frontend/.env.example frontend/.env.local
cp backend/.env.example backend/.env

# Install app dependencies
cd frontend && npm install
cd ../backend && python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt

# Start development servers
# Terminal 1: cd frontend && npm run dev
# Terminal 2: cd backend && uvicorn app.main:app --reload
```

## Creating a New Application

Use the automated script to create a new application:

```bash
./infrastructure/scripts/create-new-app.sh my-new-app
```

This will:
- ✅ Create frontend (Next.js) and backend (FastAPI) structure
- ✅ Link shared packages (auth, db, ui)
- ✅ Setup database schemas
- ✅ Configure environment files
- ✅ Create README with instructions

See [docs/guides/creating-new-app.md](./docs/guides/creating-new-app.md) for details.

## Shared Packages

### shared-auth
Authentication components and utilities for Google OAuth via Auth.js.

**Frontend**: Login/Logout buttons, Auth hooks, Session management
**Backend**: JWT validation, User context, RLS helpers

### shared-db
Database utilities, common schemas, and RLS policies.

**Includes**: User table, RLS policies, Alembic templates, Connection utilities

### shared-ui
Reusable UI components built with shadcn/ui.

**Includes**: Layout components, Form components, Utility functions

## Database

### Shared PostgreSQL Instance

All apps share a PostgreSQL instance with separate databases:

```bash
# Create database for new app
createdb myapp_dev

# Initialize with shared schemas
psql myapp_dev < packages/shared-db/schemas/*.sql

# Add app-specific schemas
psql myapp_dev < apps/my-app/backend/database/init/*.sql
```

### Access

- **pgAdmin**: http://localhost:5050 (admin@studyabroad.local / admin)
- **psql**: `psql postgresql://studyabroad:studyabroad_dev@localhost:5432/postgres`

## Development Commands

```bash
# Root level
npm run dev:study-abroad       # Start Study Abroad app
npm run build:all              # Build all packages & apps
npm run test:all               # Test all packages & apps
npm run lint:all               # Lint all packages & apps
npm run clean                  # Clean all node_modules and build artifacts
npm run create-app <name>      # Create new application

# Per-app
cd apps/study-abroad
make dev                       # Start both frontend & backend
make test                      # Run all tests
make build                     # Build for production
```

## Applications

### Study Abroad (apps/study-abroad)
AI-powered study abroad platform with RAG for accurate, citation-backed information.

**Status**: ✅ Active Development
**URL**: http://localhost:3000 (dev)

[Add more applications here as you create them]

## Technology Stack

### Shared Stack
- **Frontend**: Next.js 16+, TypeScript, Tailwind CSS, shadcn/ui
- **Backend**: FastAPI, SQLAlchemy, Alembic
- **Database**: PostgreSQL 16+ with Row Level Security
- **Auth**: Auth.js (Google OAuth 2.0)
- **Testing**: Vitest (90% coverage), Stryker (>80% mutation score)
- **Deployment**: Vercel (frontend) + Cloud Run (backend)

### Quality Standards
Per [Constitution](./.specify/memory/constitution.md):
- ✅ 100% specification faithfulness
- ✅ 90%+ test coverage
- ✅ >80% mutation score
- ✅ Row Level Security on all tables
- ✅ NIST CSF 2.0 security compliance

## Documentation

- [ARCHITECTURE.md](./ARCHITECTURE.md) - Monorepo architecture
- [DATABASE.md](./DATABASE.md) - Database documentation
- [SETUP-DATABASE.md](./SETUP-DATABASE.md) - Database setup guide
- [Constitution](./.specify/memory/constitution.md) - Project standards
- [Quality Gates](./agents/checklists/) - Gate0 through Gate8

## Contributing

1. Follow the Constitution and Quality Gates
2. Use shared packages for common functionality
3. Maintain test coverage and mutation score
4. Update documentation for new features

## License

[Your License Here]
