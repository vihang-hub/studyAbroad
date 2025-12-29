# Environment Variables Guide

Complete guide to managing environment variables across development/production and multiple applications in the monorepo.

## Table of Contents

1. [Overview](#overview)
2. [File Structure](#file-structure)
3. [Development vs Production](#development-vs-production)
4. [Multiple Applications](#multiple-applications)
5. [Shared vs App-Specific Variables](#shared-vs-app-specific-variables)
6. [Security Best Practices](#security-best-practices)
7. [Deployment Workflows](#deployment-workflows)

---

## Overview

### Key Principles

1. **Separate by Environment** - Dev, Staging, Production have different values
2. **Separate by Application** - Each app has its own variables
3. **Never Commit Secrets** - Use `.env.example` as templates, `.env` files are gitignored
4. **Use Platform Secret Managers** - Vercel/Cloud Run for production secrets

### File Hierarchy

```
StudyAbroad/
├── .env.example                    # Root-level shared defaults (optional)
│
├── apps/
│   ├── study-abroad/
│   │   ├── frontend/
│   │   │   ├── .env.example        # Template (committed to git)
│   │   │   ├── .env.local          # Development (gitignored)
│   │   │   ├── .env.production     # Production override (gitignored)
│   │   │   └── .env.test           # Testing (gitignored)
│   │   └── backend/
│   │       ├── .env.example        # Template (committed)
│   │       ├── .env                # Development (gitignored)
│   │       └── .env.production     # Production (gitignored)
│   │
│   └── career-matcher/
│       ├── frontend/
│       │   ├── .env.example
│       │   └── .env.local
│       └── backend/
│           ├── .env.example
│           └── .env
│
└── infrastructure/
    └── environments/               # Shared environment configs
        ├── development.env
        ├── staging.env
        └── production.env
```

---

## Development vs Production

### Frontend (Next.js)

Next.js has built-in environment variable support with different files for different environments.

#### Load Order (Next.js Priority)

1. `.env.$(NODE_ENV).local` (e.g., `.env.production.local`)
2. `.env.local` (Not loaded when `NODE_ENV=test`)
3. `.env.$(NODE_ENV)` (e.g., `.env.production`)
4. `.env`

#### Example: Study Abroad Frontend

**`.env.example` (Template - Committed)**
```bash
# App Configuration
NEXT_PUBLIC_APP_NAME=Study Abroad
NEXT_PUBLIC_APP_URL=http://localhost:3000

# API Configuration
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_API_V1_PREFIX=/api/v1

# Auth.js Configuration
NEXTAUTH_URL=http://localhost:3000
NEXTAUTH_SECRET=your-secret-here

# Google OAuth
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
```

**`.env.local` (Development - NOT Committed)**
```bash
# Development-specific values
NEXT_PUBLIC_APP_URL=http://localhost:3000
NEXT_PUBLIC_API_URL=http://localhost:8000

NEXTAUTH_URL=http://localhost:3000
NEXTAUTH_SECRET=dev-secret-123-not-secure

# Development OAuth app
GOOGLE_CLIENT_ID=123456-dev.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=dev-secret-abc123
```

**`.env.production` (Production - NOT Committed)**
```bash
# Production values (or use platform environment variables)
NEXT_PUBLIC_APP_URL=https://studyabroad.com
NEXT_PUBLIC_API_URL=https://api.studyabroad.com

NEXTAUTH_URL=https://studyabroad.com
NEXTAUTH_SECRET=prod-secret-from-secret-manager

# Production OAuth app
GOOGLE_CLIENT_ID=123456-prod.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=prod-secret-xyz789
```

#### Using Environment Variables

```typescript
// Frontend code
export function HomePage() {
  // Public variables (available in browser)
  const appName = process.env.NEXT_PUBLIC_APP_NAME
  const apiUrl = process.env.NEXT_PUBLIC_API_URL

  // Private variables (server-side only)
  // Access in API routes or Server Components
  const secret = process.env.NEXTAUTH_SECRET // Only available on server

  return <div>Welcome to {appName}</div>
}
```

### Backend (FastAPI)

FastAPI uses Python's `python-dotenv` and `pydantic-settings`.

#### Example: Study Abroad Backend

**`.env.example` (Template - Committed)**
```bash
# Environment
ENVIRONMENT=development
DEBUG=True

# Database
DATABASE_URL=postgresql://studyabroad:studyabroad_dev@localhost:5432/studyabroad_dev

# API Keys
GOOGLE_API_KEY=your-gemini-api-key

# Auth
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

**`.env` (Development - NOT Committed)**
```bash
ENVIRONMENT=development
DEBUG=True

# Local database
DATABASE_URL=postgresql://studyabroad:studyabroad_dev@localhost:5432/studyabroad_dev

# Development API key
GOOGLE_API_KEY=AIzaSyDev_Key_123

SECRET_KEY=dev-secret-key-not-secure-123
```

**`.env.production` (Production - NOT Committed)**
```bash
ENVIRONMENT=production
DEBUG=False

# Production database (Cloud SQL)
DATABASE_URL=postgresql://user:pass@10.1.2.3:5432/studyabroad_prod

# Production API key (from Secret Manager)
GOOGLE_API_KEY=${GOOGLE_API_KEY}  # Injected by Cloud Run

SECRET_KEY=${SECRET_KEY}  # Injected by Secret Manager
```

#### Using Environment Variables

```python
# app/core/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    DATABASE_URL: str
    GOOGLE_API_KEY: str
    SECRET_KEY: str

    class Config:
        env_file = ".env"  # Load from .env in development

settings = Settings()

# Usage
from app.core.config import settings

if settings.DEBUG:
    print(f"Running in {settings.ENVIRONMENT} mode")
```

---

## Multiple Applications

Each application maintains its **own isolated environment variables**.

### Example: Two Apps with Different Databases

#### Study Abroad App
```bash
# apps/study-abroad/frontend/.env.local
NEXT_PUBLIC_APP_NAME=Study Abroad
NEXT_PUBLIC_API_URL=http://localhost:8000

# apps/study-abroad/backend/.env
DATABASE_URL=postgresql://studyabroad:pass@localhost:5432/studyabroad_dev
GOOGLE_CLIENT_ID=123-studyabroad.apps.googleusercontent.com
```

#### Career Matcher App
```bash
# apps/career-matcher/frontend/.env.local
NEXT_PUBLIC_APP_NAME=Career Matcher
NEXT_PUBLIC_API_URL=http://localhost:8001  # Different port!

# apps/career-matcher/backend/.env
DATABASE_URL=postgresql://studyabroad:pass@localhost:5432/career_matcher_dev  # Different DB!
GOOGLE_CLIENT_ID=456-careermatcher.apps.googleusercontent.com  # Different OAuth app!
```

### Running Multiple Apps Simultaneously

```bash
# Terminal 1: Study Abroad Frontend
cd apps/study-abroad/frontend
npm run dev  # Port 3000

# Terminal 2: Study Abroad Backend
cd apps/study-abroad/backend
uvicorn app.main:app --reload --port 8000

# Terminal 3: Career Matcher Frontend
cd apps/career-matcher/frontend
npm run dev -- -p 3001  # Port 3001 (different!)

# Terminal 4: Career Matcher Backend
cd apps/career-matcher/backend
uvicorn app.main:app --reload --port 8001  # Port 8001 (different!)
```

---

## Shared vs App-Specific Variables

### Shared Variables (Same Across Apps)

Some values can be shared across applications:

```bash
# infrastructure/environments/development.env
# Shared development settings

# Shared database host (different databases per app)
DB_HOST=localhost
DB_PORT=5432
DB_USER=studyabroad
DB_PASSWORD=studyabroad_dev

# Shared Redis
REDIS_URL=redis://localhost:6379

# Shared monitoring
SENTRY_DSN=https://...@sentry.io/...
```

Apps can source this file:

```bash
# apps/study-abroad/backend/.env
# Load shared variables
set -a
source ../../../infrastructure/environments/development.env
set +a

# App-specific overrides
DATABASE_URL=postgresql://${DB_USER}:${DB_PASSWORD}@${DB_HOST}:${DB_PORT}/studyabroad_dev
```

### App-Specific Variables (Different Per App)

These should be **unique to each app**:

| Variable | Why Different? | Example |
|----------|---------------|---------|
| `DATABASE_URL` | Each app has its own database | `studyabroad_dev` vs `career_matcher_dev` |
| `GOOGLE_CLIENT_ID` | Each app needs its own OAuth app | Different redirect URLs |
| `NEXTAUTH_URL` | Each app has different domain | `studyabroad.com` vs `careermatcher.com` |
| `API_URL` | Apps run on different ports/domains | `localhost:8000` vs `localhost:8001` |
| `SECRET_KEY` | Security isolation | Different secrets per app |

---

## Security Best Practices

### 1. Never Commit Secrets

**`.gitignore`**
```gitignore
# Environment files with secrets
.env
.env.local
.env.*.local
.env.production
.env.staging

# Except templates
!.env.example
```

### 2. Use `.env.example` as Templates

```bash
# apps/study-abroad/frontend/.env.example
NEXT_PUBLIC_APP_NAME=Study Abroad
NEXT_PUBLIC_API_URL=http://localhost:8000

# Replace these with real values:
NEXTAUTH_SECRET=generate-with-openssl-rand-base64-32
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
```

### 3. Generate Secure Secrets

```bash
# Generate secure secret for NEXTAUTH_SECRET
openssl rand -base64 32

# Generate secure secret for backend SECRET_KEY
openssl rand -hex 32

# Example output:
# RW9vZGJhcmtlcmJhemluZ2E=  (use this value)
```

### 4. Use Platform Secret Managers

**Production: Never hardcode secrets**

#### Vercel (Frontend)
```bash
# Add via Vercel Dashboard or CLI
vercel env add NEXTAUTH_SECRET production
vercel env add GOOGLE_CLIENT_SECRET production
```

#### Cloud Run (Backend)
```bash
# Store in Secret Manager
gcloud secrets create GOOGLE_API_KEY --data-file=-
# (paste key, then Ctrl+D)

# Reference in Cloud Run
gcloud run services update study-abroad-api \
  --update-secrets GOOGLE_API_KEY=GOOGLE_API_KEY:latest
```

### 5. Rotate Secrets Regularly

```bash
# Every 90 days:
# 1. Generate new secret
openssl rand -base64 32

# 2. Update in Secret Manager
gcloud secrets versions add NEXTAUTH_SECRET --data-file=-

# 3. Deploy new version
vercel --prod
```

---

## Deployment Workflows

### Development Environment

```bash
# Setup for new developer
cd apps/study-abroad

# 1. Copy templates
cp frontend/.env.example frontend/.env.local
cp backend/.env.example backend/.env

# 2. Fill in development values
# Edit .env.local and .env with dev credentials

# 3. Start development
npm run dev  # Uses .env.local automatically
```

### Staging Environment

```bash
# apps/study-abroad/frontend/.env.staging
NEXT_PUBLIC_APP_URL=https://staging.studyabroad.com
NEXT_PUBLIC_API_URL=https://api-staging.studyabroad.com

# Deploy to Vercel staging
vercel --env staging
```

### Production Environment

#### Vercel (Frontend)

```bash
# Set production environment variables via Dashboard or CLI
vercel env add NEXTAUTH_SECRET production
vercel env add GOOGLE_CLIENT_ID production
vercel env add GOOGLE_CLIENT_SECRET production

# Deploy
vercel --prod
```

Environment variables are stored in Vercel's encrypted storage, NOT in code.

#### Cloud Run (Backend)

```bash
# Option 1: Via Secret Manager (Recommended)
gcloud secrets create DATABASE_URL --data-file=-
gcloud secrets create GOOGLE_API_KEY --data-file=-

gcloud run deploy study-abroad-api \
  --image gcr.io/project/study-abroad-api \
  --update-secrets \
    DATABASE_URL=DATABASE_URL:latest,\
    GOOGLE_API_KEY=GOOGLE_API_KEY:latest

# Option 2: Via environment variables (less secure)
gcloud run deploy study-abroad-api \
  --set-env-vars "ENVIRONMENT=production,DEBUG=False"
```

---

## Complete Example: Three Environments

### Study Abroad Frontend

**Development (`.env.local`)**
```bash
NEXT_PUBLIC_APP_URL=http://localhost:3000
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXTAUTH_URL=http://localhost:3000
NEXTAUTH_SECRET=dev-secret
GOOGLE_CLIENT_ID=123-dev.apps.googleusercontent.com
```

**Staging (Vercel Environment)**
```bash
NEXT_PUBLIC_APP_URL=https://staging.studyabroad.com
NEXT_PUBLIC_API_URL=https://api-staging.studyabroad.com
NEXTAUTH_URL=https://staging.studyabroad.com
NEXTAUTH_SECRET=<from Vercel Secret>
GOOGLE_CLIENT_ID=123-staging.apps.googleusercontent.com
```

**Production (Vercel Environment)**
```bash
NEXT_PUBLIC_APP_URL=https://studyabroad.com
NEXT_PUBLIC_API_URL=https://api.studyabroad.com
NEXTAUTH_URL=https://studyabroad.com
NEXTAUTH_SECRET=<from Vercel Secret>
GOOGLE_CLIENT_ID=123-prod.apps.googleusercontent.com
```

### Study Abroad Backend

**Development (`.env`)**
```bash
ENVIRONMENT=development
DEBUG=True
DATABASE_URL=postgresql://studyabroad:pass@localhost:5432/studyabroad_dev
GOOGLE_API_KEY=dev-key
```

**Staging (Cloud Run Secrets)**
```bash
ENVIRONMENT=staging
DEBUG=True
DATABASE_URL=<from Secret Manager>
GOOGLE_API_KEY=<from Secret Manager>
```

**Production (Cloud Run Secrets)**
```bash
ENVIRONMENT=production
DEBUG=False
DATABASE_URL=<from Secret Manager>
GOOGLE_API_KEY=<from Secret Manager>
```

---

## Quick Reference

### When to Use Each File

| File | Use Case | Committed? |
|------|----------|-----------|
| `.env.example` | Template for developers | ✅ Yes |
| `.env.local` | Local development | ❌ No |
| `.env.development` | Development defaults | ❌ No |
| `.env.staging` | Staging overrides | ❌ No |
| `.env.production` | Production overrides | ❌ No |
| `.env.test` | Testing environment | ❌ No |

### Environment Variable Prefixes (Next.js)

| Prefix | Available Where? |
|--------|------------------|
| `NEXT_PUBLIC_` | Browser + Server |
| No prefix | Server only |

### Setup Checklist for New App

- [ ] Copy `.env.example` to `.env.local` (frontend)
- [ ] Copy `.env.example` to `.env` (backend)
- [ ] Fill in development credentials
- [ ] Generate secrets: `openssl rand -base64 32`
- [ ] Add `.env*` to `.gitignore` (except `.env.example`)
- [ ] Document required variables in README
- [ ] Set up production secrets in Vercel/Cloud Run
- [ ] Test in all environments (dev, staging, prod)

---

## Troubleshooting

### Variables Not Loading

```bash
# Next.js: Restart dev server after changing .env
npm run dev

# FastAPI: Restart uvicorn
uvicorn app.main:app --reload
```

### Different Values in Production

```bash
# Check what Vercel is using
vercel env ls

# Check what Cloud Run is using
gcloud run services describe study-abroad-api --format="value(spec.template.spec.containers[0].env)"
```

### Secret Leaks

```bash
# If you accidentally commit secrets:
# 1. Rotate ALL secrets immediately
# 2. Use git-filter-branch to remove from history (complex!)
# 3. Better: Use tools like git-secrets to prevent commits

# Install git-secrets
brew install git-secrets

# Prevent commits with secrets
git secrets --install
git secrets --register-aws
```

---

## Summary

✅ **Each app** has its own `.env` files
✅ **Each environment** (dev/staging/prod) has different values
✅ **Never commit** real secrets (use `.env.example`)
✅ **Use platform secret managers** for production
✅ **Rotate secrets** every 90 days
✅ **Test in all environments** before deploying

Your monorepo is now set up for secure, scalable environment variable management across multiple apps and environments!
