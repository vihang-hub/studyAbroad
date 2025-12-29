# Environment Variables Quick Reference

## Visual Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                        MONOREPO ROOT                            │
│  .gitignore (blocks .env, .env.local, .env.production)         │
└─────────────────────────────────────────────────────────────────┘
                                 │
                ┌────────────────┴────────────────┐
                │                                 │
    ┌───────────▼──────────┐         ┌───────────▼──────────┐
    │   STUDY ABROAD APP   │         │  CAREER MATCHER APP  │
    │                      │         │                      │
    │  Frontend:           │         │  Frontend:           │
    │  ├─ .env.example ✓   │         │  ├─ .env.example ✓   │
    │  ├─ .env.local ✗     │         │  ├─ .env.local ✗     │
    │  └─ .env.production ✗│         │  └─ .env.production ✗│
    │                      │         │                      │
    │  Backend:            │         │  Backend:            │
    │  ├─ .env.example ✓   │         │  ├─ .env.example ✓   │
    │  ├─ .env ✗           │         │  ├─ .env ✗           │
    │  └─ .env.production ✗│         │  └─ .env.production ✗│
    └──────────────────────┘         └──────────────────────┘
         │          │                     │          │
         │          │                     │          │
    ┌────▼───┐  ┌──▼─────┐          ┌────▼───┐  ┌──▼─────┐
    │  DEV   │  │  PROD  │          │  DEV   │  │  PROD  │
    │        │  │        │          │        │  │        │
    │ Local  │  │ Vercel │          │ Local  │  │ Vercel │
    │ :3000  │  │ Cloud  │          │ :3001  │  │ Cloud  │
    │ :8000  │  │  Run   │          │ :8001  │  │  Run   │
    └────────┘  └────────┘          └────────┘  └────────┘

✓ = Committed to Git
✗ = NOT committed (gitignored)
```

## Environment Separation (Same App)

```
┌────────────────────────────────────────────────────────────┐
│              STUDY ABROAD - FRONTEND                       │
└────────────────────────────────────────────────────────────┘

Development (.env.local)          Production (Vercel UI)
├─ API: localhost:8000           ├─ API: api.studyabroad.com
├─ URL: localhost:3000           ├─ URL: studyabroad.com
├─ OAuth: dev-client-id          ├─ OAuth: prod-client-id
└─ Secret: dev-secret            └─ Secret: <encrypted>

┌────────────────────────────────────────────────────────────┐
│              STUDY ABROAD - BACKEND                        │
└────────────────────────────────────────────────────────────┘

Development (.env)               Production (Cloud Run)
├─ DB: localhost:5432            ├─ DB: Cloud SQL
├─ DEBUG: True                   ├─ DEBUG: False
├─ API Key: dev-key              ├─ API Key: <Secret Manager>
└─ Secret: dev-secret            └─ Secret: <Secret Manager>
```

## App Isolation (Same Environment)

```
┌──────────────────────────────────────────────────────────────┐
│                    DEVELOPMENT ENVIRONMENT                   │
└──────────────────────────────────────────────────────────────┘

Study Abroad                     Career Matcher
├─ DB: studyabroad_dev          ├─ DB: career_matcher_dev
├─ Port: 3000 (F) / 8000 (B)    ├─ Port: 3001 (F) / 8001 (B)
├─ OAuth: studyabroad-client    ├─ OAuth: career-client
└─ Tables: countries, programs  └─ Tables: skills, jobs

           ┌─────────────────────────┐
           │   SHARED INFRASTRUCTURE  │
           │                          │
           │  PostgreSQL :5432        │
           │  ├─ studyabroad_dev      │
           │  └─ career_matcher_dev   │
           │                          │
           │  Redis :6379 (shared)    │
           └─────────────────────────┘
```

## Concrete Example

### Scenario: Running Two Apps Locally

**Study Abroad**
```bash
# apps/study-abroad/frontend/.env.local
NEXT_PUBLIC_APP_NAME=Study Abroad
NEXT_PUBLIC_APP_URL=http://localhost:3000
NEXT_PUBLIC_API_URL=http://localhost:8000
GOOGLE_CLIENT_ID=123-studyabroad.apps.googleusercontent.com

# apps/study-abroad/backend/.env
DATABASE_URL=postgresql://studyabroad:pass@localhost:5432/studyabroad_dev
GOOGLE_API_KEY=AIza-studyabroad-dev-key
```

**Career Matcher**
```bash
# apps/career-matcher/frontend/.env.local
NEXT_PUBLIC_APP_NAME=Career Matcher
NEXT_PUBLIC_APP_URL=http://localhost:3001  # Different port!
NEXT_PUBLIC_API_URL=http://localhost:8001  # Different port!
GOOGLE_CLIENT_ID=456-career.apps.googleusercontent.com  # Different OAuth app!

# apps/career-matcher/backend/.env
DATABASE_URL=postgresql://studyabroad:pass@localhost:5432/career_matcher_dev  # Different DB!
GOOGLE_API_KEY=AIza-career-dev-key  # Different API key project!
```

**Start Both:**
```bash
# Terminal 1
cd apps/study-abroad/frontend && npm run dev
# → http://localhost:3000

# Terminal 2
cd apps/study-abroad/backend && uvicorn app.main:app --reload --port 8000

# Terminal 3
cd apps/career-matcher/frontend && npm run dev -- -p 3001
# → http://localhost:3001

# Terminal 4
cd apps/career-matcher/backend && uvicorn app.main:app --reload --port 8001
```

## Key Principles

### 1. File Naming Convention

| File | Purpose | Git? |
|------|---------|------|
| `.env.example` | Template for developers | ✅ Yes |
| `.env.local` | Local development (Next.js frontend) | ❌ No |
| `.env` | Local development (backend) | ❌ No |
| `.env.production` | Production config (rarely used) | ❌ No |

### 2. Variable Scoping

**Public Variables (Frontend)**
```bash
# Available in browser AND server
NEXT_PUBLIC_APP_NAME=Study Abroad
NEXT_PUBLIC_API_URL=http://localhost:8000
```

**Private Variables (Frontend)**
```bash
# Only available on server (API routes, Server Components)
NEXTAUTH_SECRET=secret-value
GOOGLE_CLIENT_SECRET=oauth-secret
```

**Backend Variables**
```bash
# All backend variables are server-side only
DATABASE_URL=postgresql://...
GOOGLE_API_KEY=api-key
SECRET_KEY=secret
```

### 3. Deployment Strategy

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│ Development │────▶│   Staging    │────▶│ Production  │
├─────────────┤     ├──────────────┤     ├─────────────┤
│ .env.local  │     │ Platform Env │     │ Platform Env│
│ .env        │     │ (Vercel/Run) │     │ (Vercel/Run)│
│             │     │              │     │             │
│ localhost   │     │ staging.com  │     │ prod.com    │
│ dev secrets │     │ test secrets │     │ real secrets│
└─────────────┘     └──────────────┘     └─────────────┘
```

## Common Patterns

### Pattern 1: App-Specific Database

Each app has its own database, but shares the same PostgreSQL instance:

```bash
# Shared Infrastructure
DB_HOST=localhost
DB_PORT=5432
DB_USER=studyabroad
DB_PASSWORD=studyabroad_dev

# App 1: Study Abroad
DATABASE_URL=postgresql://studyabroad:pass@localhost:5432/studyabroad_dev

# App 2: Career Matcher
DATABASE_URL=postgresql://studyabroad:pass@localhost:5432/career_matcher_dev
```

### Pattern 2: Shared Service, Different Keys

Apps share Redis but use different OAuth clients:

```bash
# Both apps
REDIS_URL=redis://localhost:6379

# App 1: Study Abroad
GOOGLE_CLIENT_ID=123-studyabroad.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=secret-for-studyabroad

# App 2: Career Matcher
GOOGLE_CLIENT_ID=456-career.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=secret-for-career
```

### Pattern 3: Environment-Specific Endpoints

```bash
# Development
NEXT_PUBLIC_API_URL=http://localhost:8000

# Staging
NEXT_PUBLIC_API_URL=https://api-staging.studyabroad.com

# Production
NEXT_PUBLIC_API_URL=https://api.studyabroad.com
```

## Security Checklist

- [ ] Never commit `.env`, `.env.local`, or `.env.production`
- [ ] Always commit `.env.example` as a template
- [ ] Use different secrets for dev/staging/prod
- [ ] Use different OAuth apps for each app
- [ ] Use platform secret managers (Vercel, GCP Secret Manager) for production
- [ ] Rotate secrets every 90 days
- [ ] Use `NEXT_PUBLIC_` prefix only for truly public values
- [ ] Never put API keys or secrets in public variables

## Quick Commands

```bash
# Copy template for new developer
cp .env.example .env.local

# Generate secure secret
openssl rand -base64 32

# Check what variables Next.js sees
npm run dev -- --debug

# Check what variables are set (backend)
python -c "from app.core.config import settings; print(settings.dict())"

# List Vercel environment variables
vercel env ls

# Add Vercel environment variable
vercel env add NEXTAUTH_SECRET production
```

## Troubleshooting

**Problem: Variables not loading**
- Restart dev server after changing `.env`
- Check file is named correctly (`.env.local` not `.env.local.txt`)
- Ensure variables have correct prefix (`NEXT_PUBLIC_` for browser access)

**Problem: Different values in production**
- Check platform environment variables (Vercel/Cloud Run)
- Verify `.env.production` is not being used (usually not needed)
- Check build logs for loaded variables

**Problem: Accidentally committed secrets**
1. Rotate ALL affected secrets immediately
2. Update `.gitignore` to prevent future commits
3. Consider using `git-secrets` to prevent commits

## Summary

✅ Each **app** = Separate `.env` files
✅ Each **environment** = Different values
✅ **Development** = Local `.env` files
✅ **Production** = Platform secret managers
✅ **Templates** = `.env.example` (committed)
✅ **Secrets** = Never in git, rotated regularly

See [environment-variables.md](./environment-variables.md) for the complete guide!
