# Monorepo Architecture

This is a monorepo containing multiple applications with shared packages for common functionality.

## Structure

```
StudyAbroad/
├── apps/                          # Individual applications
│   └── study-abroad/              # Study Abroad application (first app)
│       ├── frontend/              # Next.js frontend
│       ├── backend/               # FastAPI backend
│       └── README.md              # App-specific documentation
│
├── packages/                      # Shared/reusable packages
│   ├── shared-auth/               # Authentication module
│   │   ├── frontend/              # Next.js auth components, hooks, providers
│   │   │   ├── components/        # Login, Logout, AuthProvider
│   │   │   ├── hooks/             # useAuth, useSession
│   │   │   └── lib/               # Auth.js config, utilities
│   │   ├── backend/               # FastAPI auth middleware
│   │   │   ├── middleware/        # JWT validation, RLS context
│   │   │   ├── dependencies/      # get_current_user dependency
│   │   │   └── utils/             # Token generation, validation
│   │   └── README.md
│   │
│   ├── shared-db/                 # Database utilities and schemas
│   │   ├── schemas/               # Common database schemas
│   │   │   ├── users.sql          # User table definition
│   │   │   ├── base_tables.sql    # Common tables (audit logs, etc.)
│   │   │   └── rls_policies.sql   # Standard RLS policies
│   │   ├── migrations/            # Alembic migration templates
│   │   ├── utils/                 # DB utilities
│   │   │   ├── connection.py      # SQLAlchemy async engine setup
│   │   │   ├── rls.py             # RLS helper functions
│   │   │   └── base_model.py      # Base SQLAlchemy model
│   │   └── README.md
│   │
│   ├── shared-ui/                 # Shared UI components
│   │   ├── components/            # Reusable React components
│   │   │   ├── layout/            # Header, Footer, Sidebar
│   │   │   ├── forms/             # Form components
│   │   │   └── ui/                # shadcn/ui components
│   │   ├── styles/                # Shared styles, themes
│   │   ├── lib/                   # UI utilities (cn, etc.)
│   │   └── README.md
│   │
│   └── shared-types/              # TypeScript type definitions
│       ├── api/                   # API request/response types
│       ├── database/              # Database model types
│       └── README.md
│
├── infrastructure/                # Shared infrastructure
│   ├── docker/                    # Docker configurations
│   │   ├── docker-compose.yml     # Base services (Postgres, Redis, etc.)
│   │   ├── postgres/              # Postgres config
│   │   └── README.md
│   ├── scripts/                   # Automation scripts
│   │   ├── create-new-app.sh      # Create new application from template
│   │   ├── setup-database.sh      # Setup shared database
│   │   └── deploy.sh              # Deployment scripts
│   └── terraform/                 # Infrastructure as Code (optional)
│
├── docs/                          # Documentation
│   ├── architecture/              # Architecture Decision Records
│   ├── guides/                    # Development guides
│   │   ├── creating-new-app.md    # How to create a new app
│   │   ├── using-shared-auth.md   # Using shared auth
│   │   └── using-shared-db.md     # Using shared database
│   └── DATABASE.md
│
├── .github/                       # GitHub configuration
│   └── workflows/                 # CI/CD pipelines
│
├── package.json                   # Root package.json (for workspace)
├── pnpm-workspace.yaml            # PNPM workspace config
├── Makefile                       # Common tasks
└── README.md                      # Main documentation
```

## Design Principles

### 1. Separation of Concerns
- **Apps**: Application-specific business logic
- **Packages**: Reusable, framework-agnostic components
- **Infrastructure**: Deployment and operational concerns

### 2. Shared Packages Philosophy

**shared-auth**
- ✅ Google OAuth integration
- ✅ JWT token generation/validation
- ✅ Auth.js configuration
- ✅ User session management
- ✅ RLS context helpers
- ❌ App-specific permissions (kept in apps/)

**shared-db**
- ✅ Database connection setup
- ✅ Common tables (users, audit_logs)
- ✅ RLS policy templates
- ✅ Migration utilities
- ❌ App-specific tables (defined in apps/)

**shared-ui**
- ✅ Layout components (Header, Footer)
- ✅ shadcn/ui components
- ✅ Form components
- ✅ Theme configuration
- ❌ App-specific pages/views

### 3. Independence
Each app should be:
- Independently deployable
- Have its own database schema (extending shared base)
- Have its own CI/CD pipeline
- Able to version independently

### 4. Shared Database Strategy

**Option A: Shared Postgres Instance, Separate Schemas**
```sql
-- Each app has its own schema
study_abroad.users (extends shared.users)
study_abroad.countries
study_abroad.programs

next_app.users (extends shared.users)
next_app.specific_tables
```

**Option B: Separate Databases per App** (Recommended)
```sql
-- Database: studyabroad_dev
users (from shared-db)
countries (app-specific)
programs (app-specific)

-- Database: nextapp_dev
users (from shared-db)
app_specific_tables
```

## Creating a New Application

```bash
# 1. Use the script to create a new app
./infrastructure/scripts/create-new-app.sh my-new-app

# 2. The script will:
#    - Create apps/my-new-app/frontend
#    - Create apps/my-new-app/backend
#    - Link shared packages
#    - Setup database with shared schemas
#    - Configure auth

# 3. Start development
cd apps/my-new-app
make dev
```

## Package Dependencies

### Frontend Apps
```json
{
  "dependencies": {
    "@my-org/shared-auth": "workspace:*",
    "@my-org/shared-ui": "workspace:*",
    "@my-org/shared-types": "workspace:*"
  }
}
```

### Backend Apps
```python
# requirements.txt
shared-auth @ file:../../../packages/shared-auth/backend
shared-db @ file:../../../packages/shared-db
```

## Technology Stack

### Shared Stack (Consistent across all apps)
- **Frontend**: Next.js 15+ (App Router), TypeScript, Tailwind CSS
- **Backend**: FastAPI (Python 3.12+), SQLAlchemy
- **Database**: PostgreSQL 16+ with RLS
- **Auth**: Auth.js (NextAuth) + Google OAuth
- **Deployment**: Vercel (Frontend) + Cloud Run (Backend)

### App-Specific
- Apps can add their own dependencies
- Must follow Constitution guidelines
- Must maintain test coverage (90%+) and mutation score (>80%)

## Development Workflow

### Working on Shared Packages
```bash
# Make changes to shared-auth
cd packages/shared-auth/frontend
npm run build

# All apps using it will pick up changes
cd apps/study-abroad/frontend
npm run dev  # Uses latest shared-auth
```

### Working on Individual Apps
```bash
cd apps/study-abroad
make dev  # Starts both frontend and backend
```

## Benefits

1. **Code Reuse**: Write auth once, use everywhere
2. **Consistency**: Same patterns across all applications
3. **Faster Development**: New apps bootstrap in minutes
4. **Maintainability**: Fix bugs in one place
5. **Scalability**: Add apps without architectural changes
6. **Team Collaboration**: Clear boundaries between shared and app code

## Migration Plan

Current structure → Monorepo structure:

1. Create new folder structure
2. Move current code to `apps/study-abroad`
3. Extract shared components to `packages/`
4. Update imports and dependencies
5. Test that everything works
6. Document the process for future apps

## Future Applications Ideas

- **CareerPath**: Career guidance platform
- **SkillMatch**: Skills assessment and job matching
- **MentorConnect**: Mentorship platform
- **ResearchHub**: Academic research collaboration

All sharing the same auth, database patterns, and UI components!
