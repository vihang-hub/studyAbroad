# Technology Stack

## Frontend
- **Framework**: Next.js 15.1.3 (App Router with React Server Components)
- **Language**: TypeScript 5.3+ (Strict Mode)
- **React**: 19.0.0
- **Styling**: Tailwind CSS 3.4+ with shadcn/ui components
- **Authentication**: Clerk 6.36.5 (clerkMiddleware)
- **Payments**: Stripe React SDK
- **AI Streaming**: Vercel AI SDK
- **Validation**: Zod 3.23+
- **Testing**: Vitest 2.1.8 with @testing-library/react
- **Mutation Testing**: Stryker Mutator
- **Linting**: ESLint with Airbnb style guide
- **Deployment**: Vercel

## Backend
- **Framework**: FastAPI 0.115+
- **Language**: Python 3.12+
- **AI Orchestration**: LangChain 0.3+
- **AI API**: Google Generative AI SDK (Gemini 2.0 Flash)
- **Database Client**: Supabase Python Client 2.11+
- **Payments**: Stripe Python SDK
- **Validation**: Pydantic 2.10+
- **Logging**: structlog (structured logging with rotation)
- **Database Driver**: asyncpg (PostgreSQL async driver)
- **Testing**: pytest 8.3+ with pytest-asyncio, pytest-cov
- **Mutation Testing**: mutmut
- **Linting**: ruff, black
- **Type Checking**: mypy
- **Deployment**: Google Cloud Run (containerized)

## Database
- **Development**: PostgreSQL 14+ (local)
- **Test/Production**: Supabase PostgreSQL (managed, with RLS)
- **Migrations**: Alembic

## Shared Infrastructure (TypeScript)
Four shared packages in `/Users/vihang/projects/study-abroad/shared/`:
1. **@study-abroad/shared-config**: Environment configuration with Zod validation
2. **@study-abroad/shared-feature-flags**: Feature flag evaluation (ENABLE_SUPABASE, ENABLE_PAYMENTS)
3. **@study-abroad/shared-database**: Repository pattern with PostgreSQL/Supabase adapters, soft delete
4. **@study-abroad/shared-logging**: Structured logging with Winston, rotation (100MB OR daily), retention (30 days)

## Environment Configuration
- **Development Mode**: Local PostgreSQL, no payments, debug logs
- **Test Mode**: Supabase, no payments, debug logs
- **Production Mode**: Supabase, payments enabled, error logs only

## Quality Standards (Per Constitution v1.0.0)
- Code coverage: ≥90% (enforced)
- Mutation score: >80% (Stryker for TS, mutmut for Python)
- Security: NIST CSF 2.0 compliance
- Testing: Test pyramid (80% unit, 15% integration, 5% E2E)
