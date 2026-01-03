# Quickstart Guide: MVP UK Study & Migration App

**Last Updated**: 2025-12-29
**Estimated Setup Time**: 30-45 minutes

This guide helps you set up the development environment for the Study Abroad MVP.

---

## Prerequisites

### Required Tools

- **Node.js** 20.x+ (with npm/pnpm)
- **Python** 3.12+
- **Docker** & Docker Compose (for local Supabase)
- **Git**
- **Supabase CLI**: `npm install -g supabase`
- **Stripe CLI**: For webhook testing

### Required Accounts

1. **Clerk**: [Sign up](https://clerk.com) for free account
2. **Stripe**: [Sign up](https://stripe.com) for test account
3. **Google AI Studio**: [Get Gemini API key](https://aistudio.google.com)
4. **Supabase** (optional): Can use local instance or cloud

---

## Quick Start (5 minutes)

```bash
# 1. Clone repository
git clone <repo-url>
cd study-abroad
git checkout 001-mvp-uk-study-migration

# 2. Install dependencies
cd frontend && pnpm install && cd ..
cd backend && pip install -e ".[dev]" && cd ..

# 3. Start local Supabase
supabase start

# 4. Copy environment templates
cp frontend/.env.example frontend/.env.local
cp backend/.env.example backend/.env

# 5. Configure secrets (see below)
# Edit frontend/.env.local and backend/.env

# 6. Run migrations
cd backend && alembic upgrade head && cd ..

# 7. Start dev servers
# Terminal 1: Backend
cd backend && uvicorn src.main:app --reload --port 8000

# Terminal 2: Frontend
cd frontend && pnpm dev

# 8. Open browser: http://localhost:3000
```

---

## Detailed Setup

### 1. Repository Structure

Ensure you're on the correct feature branch:

```bash
git checkout 001-mvp-uk-study-migration
```

Expected structure:
```
study-abroad/
├── backend/         # FastAPI + Python 3.12
├── frontend/        # Next.js 15 + TypeScript
├── shared/          # Shared TypeScript types (optional)
└── specs/           # Feature specifications
    └── 001-mvp-uk-study-migration/
        ├── spec.md
        ├── plan.md
        ├── research.md
        ├── data-model.md
        └── contracts/
```

---

### 2. Backend Setup (FastAPI)

#### Install Dependencies

```bash
cd backend

# Create virtual environment
python3.12 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install with dev dependencies
pip install -e ".[dev]"
```

#### Environment Configuration

Create `backend/.env`:

```bash
# === Application ===
ENV=development
DEBUG=True
LOG_LEVEL=DEBUG

# === Database (Supabase) ===
SUPABASE_URL=http://localhost:54321
SUPABASE_ANON_KEY=<from supabase start output>
SUPABASE_SERVICE_ROLE_KEY=<from supabase start output>
DATABASE_URL=postgresql://postgres:postgres@localhost:54322/postgres

# === Clerk Authentication ===
CLERK_SECRET_KEY=sk_test_...  # Get from Clerk Dashboard > API Keys
CLERK_PUBLISHABLE_KEY=pk_test_...

# === Stripe ===
STRIPE_SECRET_KEY=sk_test_...  # Get from Stripe Dashboard > Developers > API Keys
STRIPE_WEBHOOK_SECRET=whsec_...  # Get after setting up webhook (see below)
STRIPE_PRICE_ID=price_...  # Create £2.99 price in Stripe Dashboard

# === Google Gemini ===
GOOGLE_API_KEY=AIza...  # Get from Google AI Studio

# === CORS ===
ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# === Cron Secret ===
CRON_SECRET=<generate-random-secret>
```

#### Run Migrations

```bash
# Apply database schema
alembic upgrade head

# Verify tables created
supabase db diff
```

#### Start Backend Server

```bash
uvicorn src.main:app --reload --port 8000
```

**Test**: Visit http://localhost:8000/health

Expected response:
```json
{"status": "healthy", "version": "1.0.0", "timestamp": "2025-12-29T..."}
```

---

### 3. Frontend Setup (Next.js)

#### Install Dependencies

```bash
cd frontend
pnpm install  # or npm install
```

#### Environment Configuration

Create `frontend/.env.local`:

```bash
# === Next.js ===
NEXT_PUBLIC_APP_URL=http://localhost:3000

# === Backend API ===
NEXT_PUBLIC_API_URL=http://localhost:8000

# === Clerk Authentication ===
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=pk_test_...
CLERK_SECRET_KEY=sk_test_...
NEXT_PUBLIC_CLERK_SIGN_IN_URL=/login
NEXT_PUBLIC_CLERK_SIGN_UP_URL=/signup
NEXT_PUBLIC_CLERK_AFTER_SIGN_IN_URL=/chat
NEXT_PUBLIC_CLERK_AFTER_SIGN_UP_URL=/chat

# === Supabase (Client) ===
NEXT_PUBLIC_SUPABASE_URL=http://localhost:54321
NEXT_PUBLIC_SUPABASE_ANON_KEY=<from supabase start output>

# === Stripe (Client) ===
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_test_...
```

#### Start Frontend Server

```bash
pnpm dev
```

**Test**: Visit http://localhost:3000

You should see the login page.

---

### 4. Clerk Setup

#### Configure Clerk Application

1. Go to [Clerk Dashboard](https://dashboard.clerk.com)
2. Create new application: "Study Abroad MVP"
3. Enable OAuth providers:
   - **Google**: Enable and configure OAuth
   - **Apple**: Enable (requires Apple Developer account)
   - **Facebook**: Enable and configure OAuth
4. Enable **Email** authentication:
   - Enable "Email address"
   - Enable "Password" or "Email link" (magic link)
5. Copy API keys to `.env` files

#### Test Authentication

1. Start frontend: http://localhost:3000
2. Click "Sign up"
3. Sign up with email or OAuth
4. Verify redirect to `/chat`

---

### 5. Supabase Setup

#### Local Instance (Recommended for Dev)

```bash
# Start Supabase (runs Docker containers)
supabase start

# Output shows:
# - API URL: http://localhost:54321
# - DB URL: postgresql://postgres:postgres@localhost:54322/postgres
# - Studio URL: http://localhost:54323 (DB GUI)
# - Anon key: eyJh...
# - Service role key: eyJh...

# Apply migrations
cd backend
alembic upgrade head

# Verify in Supabase Studio: http://localhost:54323
```

#### Cloud Instance (Optional)

1. Go to [Supabase Dashboard](https://supabase.com/dashboard)
2. Create new project: "study-abroad-mvp"
3. Copy connection details to `.env` files
4. Apply migrations:
   ```bash
   supabase db push
   ```

---

### 6. Stripe Setup

#### Create Products & Prices

1. Go to [Stripe Dashboard](https://dashboard.stripe.com/test/products)
2. Create product: "UK Study Report"
   - Price: £2.99 GBP (one-time)
   - Copy Price ID → `STRIPE_PRICE_ID` in `.env`

#### Configure Webhooks (Local Testing)

```bash
# Install Stripe CLI
brew install stripe/stripe-cli/stripe  # macOS
# or download from https://stripe.com/docs/stripe-cli

# Login to Stripe
stripe login

# Forward webhooks to local backend
stripe listen --forward-to localhost:8000/webhooks/stripe

# Copy webhook secret from output → STRIPE_WEBHOOK_SECRET in .env
```

**Output**:
```
> Ready! Your webhook signing secret is whsec_abc123...
```

#### Test Payment Flow

1. Visit http://localhost:3000/chat
2. Enter subject: "Computer Science"
3. Click "Generate Report (£2.99)"
4. Use Stripe test card: `4242 4242 4242 4242`
5. Verify payment succeeds and report generates

---

### 7. Google Gemini API Setup

#### Get API Key

1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Click "Create API Key"
3. Copy key → `GOOGLE_API_KEY` in `backend/.env`

#### Test API

```bash
# From backend directory
python -c "
import os
from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(model='gemini-2.0-flash-exp', google_api_key=os.getenv('GOOGLE_API_KEY'))
result = llm.invoke('Say hello')
print(result.content)
"
```

Expected: AI response printed to console

---

## Development Workflow

### Running the Full Stack

**Terminal 1: Supabase**
```bash
supabase start
```

**Terminal 2: Backend**
```bash
cd backend
source venv/bin/activate
uvicorn src.main:app --reload --port 8000
```

**Terminal 3: Frontend**
```bash
cd frontend
pnpm dev
```

**Terminal 4: Stripe Webhooks**
```bash
stripe listen --forward-to localhost:8000/webhooks/stripe
```

### Testing the Flow

1. **Authentication**:
   - Visit http://localhost:3000
   - Sign up with Google or email
   - Verify redirect to `/chat`

2. **Payment & Report Generation**:
   - Enter subject: "Computer Science"
   - Click "Generate Report"
   - Complete payment with test card
   - Verify streaming report generation
   - Check report appears in sidebar

3. **Report Retrieval**:
   - Refresh page
   - Verify reports persist
   - Click on past report → verify content loads

---

## Database Migrations

### Create New Migration

```bash
cd backend

# Auto-generate from SQLAlchemy models
alembic revision --autogenerate -m "Add new column to reports"

# Edit migration file in backend/alembic/versions/

# Apply migration
alembic upgrade head
```

### Rollback Migration

```bash
alembic downgrade -1  # Rollback one migration
alembic downgrade base  # Rollback all migrations
```

---

## Testing

### Backend Tests

```bash
cd backend

# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test
pytest tests/unit/test_report_service.py -v

# Mutation testing
stryker run
```

### Frontend Tests

```bash
cd frontend

# Run unit tests
pnpm test

# Run E2E tests (requires backend running)
pnpm test:e2e

# Coverage report
pnpm test:coverage

# Mutation testing
pnpm test:mutation
```

---

## Common Issues

### Issue: Clerk JWT verification fails

**Solution**:
```bash
# Ensure Clerk secret key is correct in backend/.env
CLERK_SECRET_KEY=sk_test_...

# Verify JWT in request headers:
curl -H "Authorization: Bearer <jwt>" http://localhost:8000/reports
```

### Issue: Supabase connection refused

**Solution**:
```bash
# Check Supabase is running
docker ps | grep supabase

# Restart Supabase
supabase stop
supabase start
```

### Issue: Stripe webhook signature mismatch

**Solution**:
```bash
# Ensure Stripe CLI is forwarding webhooks
stripe listen --forward-to localhost:8000/webhooks/stripe

# Copy new webhook secret to backend/.env
STRIPE_WEBHOOK_SECRET=whsec_...

# Restart backend server
```

### Issue: Gemini API rate limit

**Solution**:
- Use API key with sufficient quota
- Implement exponential backoff in `ai_service.py`
- Consider caching common queries

---

## Next Steps

1. ✅ **Setup Complete**: All services running locally
2. **Read Implementation Guide**: See `/specs/001-mvp-uk-study-migration/tasks.md` (after running `/speckit.tasks`)
3. **Review Data Model**: See `data-model.md`
4. **Review API Contracts**: See `contracts/backend-api.openapi.yaml`
5. **Start Coding**: Begin with backend API routes or frontend components

---

## Helpful Commands

```bash
# Backend
cd backend
source venv/bin/activate
uvicorn src.main:app --reload        # Start server
pytest                               # Run tests
alembic upgrade head                 # Apply migrations
python -m src.scripts.seed_data      # Seed test data

# Frontend
cd frontend
pnpm dev                             # Start server
pnpm build                           # Build for production
pnpm lint                            # Run linter
pnpm test                            # Run tests

# Supabase
supabase start                       # Start local instance
supabase stop                        # Stop local instance
supabase db reset                    # Reset database
supabase db diff                     # Show schema changes

# Stripe
stripe listen --forward-to localhost:8000/webhooks/stripe  # Forward webhooks
stripe trigger checkout.session.completed                  # Test webhook
```

---

## Support

- **Spec Issues**: See `/specs/001-mvp-uk-study-migration/spec.md`
- **API Reference**: See `contracts/backend-api.openapi.yaml`
- **Constitution**: See `.specify/memory/constitution.md`
