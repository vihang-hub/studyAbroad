# Environment Setup Walkthrough

A step-by-step guide to setting up environment variables from scratch.

## Scenario

You have:
- **2 applications**: Study Abroad, Career Matcher
- **3 environments**: Development, Staging, Production
- **Shared infrastructure**: PostgreSQL, Redis

Let's set this up correctly!

---

## Part 1: Development Setup

### Step 1: Study Abroad App (Development)

```bash
cd apps/study-abroad
```

#### Frontend Setup

```bash
cd frontend

# Copy template
cp .env.example .env.local

# Edit .env.local
nano .env.local
```

Add these values:

```bash
# App Configuration
NEXT_PUBLIC_APP_NAME=Study Abroad
NEXT_PUBLIC_APP_URL=http://localhost:3000

# API Configuration
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_API_V1_PREFIX=/api/v1

# Auth.js Configuration
NEXTAUTH_URL=http://localhost:3000
NEXTAUTH_SECRET=dev-secret-change-in-production

# Google OAuth (Development App)
GOOGLE_CLIENT_ID=123456789-dev.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=GOCSPX-dev_secret_here
```

#### Backend Setup

```bash
cd ../backend

# Copy template
cp .env.example .env

# Edit .env
nano .env
```

Add these values:

```bash
# Environment
ENVIRONMENT=development
DEBUG=True

# CORS
CORS_ORIGINS=["http://localhost:3000"]

# Local PostgreSQL Database
DATABASE_URL=postgresql://studyabroad:studyabroad_dev@localhost:5432/studyabroad_dev

# Google Gemini API (Development Key)
GOOGLE_API_KEY=AIzaSyDev_Key_For_StudyAbroad_123

# Authentication
SECRET_KEY=dev-backend-secret-key-123
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

#### Test It

```bash
# Terminal 1: Frontend
cd apps/study-abroad/frontend
npm run dev
# → http://localhost:3000

# Terminal 2: Backend
cd apps/study-abroad/backend
source venv/bin/activate
uvicorn app.main:app --reload
# → http://localhost:8000
```

✅ Study Abroad running on ports 3000/8000

---

### Step 2: Career Matcher App (Development)

```bash
cd apps/career-matcher
```

#### Frontend Setup

```bash
cd frontend
cp .env.example .env.local
nano .env.local
```

**IMPORTANT: Different values!**

```bash
# App Configuration
NEXT_PUBLIC_APP_NAME=Career Matcher
NEXT_PUBLIC_APP_URL=http://localhost:3001  # ← Different port

# API Configuration
NEXT_PUBLIC_API_URL=http://localhost:8001  # ← Different port
NEXT_PUBLIC_API_V1_PREFIX=/api/v1

# Auth.js Configuration
NEXTAUTH_URL=http://localhost:3001  # ← Different port
NEXTAUTH_SECRET=dev-secret-career-matcher

# Google OAuth (Different App!)
GOOGLE_CLIENT_ID=987654321-career.apps.googleusercontent.com  # ← Different
GOOGLE_CLIENT_SECRET=GOCSPX-career_secret_here  # ← Different
```

#### Backend Setup

```bash
cd ../backend
cp .env.example .env
nano .env
```

**IMPORTANT: Different database!**

```bash
# Environment
ENVIRONMENT=development
DEBUG=True

# CORS (Different frontend port)
CORS_ORIGINS=["http://localhost:3001"]  # ← Port 3001

# Local PostgreSQL Database (Different database!)
DATABASE_URL=postgresql://studyabroad:studyabroad_dev@localhost:5432/career_matcher_dev  # ← Different DB

# Google Gemini API (Could be same or different project)
GOOGLE_API_KEY=AIzaSyDev_Key_For_CareerMatcher_456  # ← Different project

# Authentication (Different secret for security isolation!)
SECRET_KEY=dev-career-backend-secret-789  # ← Different
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

#### Create Database

```bash
# Create database for Career Matcher
createdb career_matcher_dev

# Initialize with shared schemas
psql career_matcher_dev < ../../../packages/shared-db/schemas/*.sql

# Initialize with app-specific schemas
psql career_matcher_dev < database/init/*.sql
```

#### Test It

```bash
# Terminal 3: Frontend (different port)
cd apps/career-matcher/frontend
npm run dev -- -p 3001
# → http://localhost:3001

# Terminal 4: Backend (different port)
cd apps/career-matcher/backend
source venv/bin/activate
uvicorn app.main:app --reload --port 8001
# → http://localhost:8001
```

✅ Career Matcher running on ports 3001/8001

---

## Part 2: Staging Setup

### Step 3: Deploy Study Abroad to Staging

#### Frontend (Vercel)

```bash
cd apps/study-abroad/frontend

# Link to Vercel project
vercel link

# Add staging environment variables
vercel env add NEXT_PUBLIC_APP_URL staging
# → https://staging.studyabroad.com

vercel env add NEXT_PUBLIC_API_URL staging
# → https://api-staging.studyabroad.com

vercel env add NEXTAUTH_URL staging
# → https://staging.studyabroad.com

vercel env add NEXTAUTH_SECRET staging
# → <paste generated secret: openssl rand -base64 32>

vercel env add GOOGLE_CLIENT_ID staging
# → <staging OAuth app client ID>

vercel env add GOOGLE_CLIENT_SECRET staging
# → <staging OAuth app secret>

# Deploy to staging
vercel --env staging
```

#### Backend (Cloud Run - Staging)

```bash
cd apps/study-abroad/backend

# Create secrets in Secret Manager
echo "staging-backend-secret-$(openssl rand -hex 32)" | \
  gcloud secrets create STUDYABROAD_STAGING_SECRET_KEY --data-file=-

echo "AIzaSyStaging_Key_Here" | \
  gcloud secrets create STUDYABROAD_STAGING_GOOGLE_API_KEY --data-file=-

# Deploy to Cloud Run staging
gcloud run deploy study-abroad-api-staging \
  --image gcr.io/my-project/study-abroad-api:staging \
  --region us-central1 \
  --set-env-vars "ENVIRONMENT=staging,DEBUG=True" \
  --set-env-vars "DATABASE_URL=postgresql://user:pass@staging-db:5432/studyabroad_staging" \
  --update-secrets \
    SECRET_KEY=STUDYABROAD_STAGING_SECRET_KEY:latest,\
    GOOGLE_API_KEY=STUDYABROAD_STAGING_GOOGLE_API_KEY:latest
```

✅ Study Abroad staging deployed

---

## Part 3: Production Setup

### Step 4: Deploy Study Abroad to Production

#### Frontend (Vercel Production)

```bash
cd apps/study-abroad/frontend

# Add production environment variables (different from staging!)
vercel env add NEXT_PUBLIC_APP_URL production
# → https://studyabroad.com

vercel env add NEXT_PUBLIC_API_URL production
# → https://api.studyabroad.com

vercel env add NEXTAUTH_URL production
# → https://studyabroad.com

vercel env add NEXTAUTH_SECRET production
# → <NEW secret: openssl rand -base64 32>

vercel env add GOOGLE_CLIENT_ID production
# → <production OAuth app client ID>

vercel env add GOOGLE_CLIENT_SECRET production
# → <production OAuth app secret>

# Deploy to production
vercel --prod
```

#### Backend (Cloud Run - Production)

```bash
cd apps/study-abroad/backend

# Create PRODUCTION secrets (different from staging!)
echo "production-backend-secret-$(openssl rand -hex 32)" | \
  gcloud secrets create STUDYABROAD_PROD_SECRET_KEY --data-file=-

echo "AIzaSyProduction_Real_Key_Here" | \
  gcloud secrets create STUDYABROAD_PROD_GOOGLE_API_KEY --data-file=-

# Deploy to Cloud Run production
gcloud run deploy study-abroad-api \
  --image gcr.io/my-project/study-abroad-api:latest \
  --region us-central1 \
  --set-env-vars "ENVIRONMENT=production,DEBUG=False" \
  --set-env-vars "DATABASE_URL=postgresql://user:pass@prod-db:5432/studyabroad_prod" \
  --update-secrets \
    SECRET_KEY=STUDYABROAD_PROD_SECRET_KEY:latest,\
    GOOGLE_API_KEY=STUDYABROAD_PROD_GOOGLE_API_KEY:latest
```

✅ Study Abroad production deployed

---

## Part 4: Career Matcher (Same Process)

### Step 5: Deploy Career Matcher

Repeat the same process for Career Matcher, but with **different values**:

#### Staging

```bash
# Frontend (Vercel)
NEXT_PUBLIC_APP_URL=https://staging.careermatcher.com  # ← Different domain
GOOGLE_CLIENT_ID=<career-staging-oauth-client>  # ← Different OAuth app

# Backend (Cloud Run)
STUDYABROAD_STAGING_SECRET_KEY → CAREERMATCHER_STAGING_SECRET_KEY  # ← Different secret
DATABASE_URL=postgresql://user:pass@staging-db:5432/career_matcher_staging  # ← Different DB
```

#### Production

```bash
# Frontend (Vercel)
NEXT_PUBLIC_APP_URL=https://careermatcher.com  # ← Different domain
GOOGLE_CLIENT_ID=<career-prod-oauth-client>  # ← Different OAuth app

# Backend (Cloud Run)
STUDYABROAD_PROD_SECRET_KEY → CAREERMATCHER_PROD_SECRET_KEY  # ← Different secret
DATABASE_URL=postgresql://user:pass@prod-db:5432/career_matcher_prod  # ← Different DB
```

---

## Summary Matrix

### Environment Variables by App and Environment

| Variable | Study Abroad Dev | Study Abroad Prod | Career Matcher Dev | Career Matcher Prod |
|----------|-----------------|-------------------|-------------------|---------------------|
| **Frontend Port** | 3000 | N/A (Vercel) | 3001 | N/A (Vercel) |
| **Backend Port** | 8000 | N/A (Cloud Run) | 8001 | N/A (Cloud Run) |
| **Domain** | localhost:3000 | studyabroad.com | localhost:3001 | careermatcher.com |
| **Database** | studyabroad_dev | studyabroad_prod | career_matcher_dev | career_matcher_prod |
| **OAuth Client** | Dev Client 1 | Prod Client 1 | Dev Client 2 | Prod Client 2 |
| **API Key** | Dev Key 1 | Prod Key 1 | Dev Key 2 | Prod Key 2 |
| **Secrets** | dev-secret-1 | prod-secret-1 | dev-secret-2 | prod-secret-2 |

### File Locations

```
apps/
├── study-abroad/
│   ├── frontend/
│   │   ├── .env.example ✓ (committed)
│   │   └── .env.local ✗ (dev values)
│   └── backend/
│       ├── .env.example ✓ (committed)
│       └── .env ✗ (dev values)
│
└── career-matcher/
    ├── frontend/
    │   ├── .env.example ✓ (committed)
    │   └── .env.local ✗ (dev values)
    └── backend/
        ├── .env.example ✓ (committed)
        └── .env ✗ (dev values)
```

Staging/Production values are in:
- **Vercel Dashboard** (frontend)
- **GCP Secret Manager** (backend)

---

## Verification Checklist

### Development

- [ ] Study Abroad frontend on port 3000
- [ ] Study Abroad backend on port 8000
- [ ] Career Matcher frontend on port 3001
- [ ] Career Matcher backend on port 8001
- [ ] Each app connects to its own database
- [ ] Each app uses its own OAuth client
- [ ] Can run both apps simultaneously

### Staging

- [ ] Study Abroad: staging.studyabroad.com
- [ ] Career Matcher: staging.careermatcher.com
- [ ] Different OAuth apps from production
- [ ] Different secrets from production
- [ ] Different databases from production

### Production

- [ ] Study Abroad: studyabroad.com
- [ ] Career Matcher: careermatcher.com
- [ ] Production OAuth apps
- [ ] Production secrets (never in code)
- [ ] Production databases
- [ ] All secrets in Secret Manager

---

## Common Mistakes to Avoid

❌ **Using same secrets across environments**
```bash
# WRONG: Same secret for dev and prod
NEXTAUTH_SECRET=same-secret-everywhere
```

✅ **Different secrets per environment**
```bash
# Dev: .env.local
NEXTAUTH_SECRET=dev-secret-not-secure

# Prod: Vercel dashboard
NEXTAUTH_SECRET=<generated secure secret>
```

---

❌ **Using same OAuth app across apps**
```bash
# WRONG: Same client ID for both apps
# Study Abroad: GOOGLE_CLIENT_ID=123-shared.apps.googleusercontent.com
# Career Matcher: GOOGLE_CLIENT_ID=123-shared.apps.googleusercontent.com
```

✅ **Different OAuth apps per application**
```bash
# Study Abroad: GOOGLE_CLIENT_ID=123-studyabroad.apps.googleusercontent.com
# Career Matcher: GOOGLE_CLIENT_ID=456-career.apps.googleusercontent.com
```

---

❌ **Hardcoding production URLs in development**
```bash
# WRONG: .env.local
NEXT_PUBLIC_API_URL=https://api.studyabroad.com  # Production URL!
```

✅ **Environment-specific URLs**
```bash
# Dev: .env.local
NEXT_PUBLIC_API_URL=http://localhost:8000

# Prod: Vercel
NEXT_PUBLIC_API_URL=https://api.studyabroad.com
```

---

## Quick Commands Reference

```bash
# Generate secure secret
openssl rand -base64 32

# Create database
createdb app_name_dev

# Add Vercel env var
vercel env add VAR_NAME production

# Create GCP secret
echo "value" | gcloud secrets create SECRET_NAME --data-file=-

# List environment variables
vercel env ls  # Vercel
gcloud secrets list  # GCP

# Check what's loaded (Next.js)
console.log(process.env.NEXT_PUBLIC_API_URL)

# Check what's loaded (FastAPI)
from app.core.config import settings
print(settings.dict())
```

---

You now have a complete, secure environment variable setup across development, staging, and production for multiple applications! 🎉
