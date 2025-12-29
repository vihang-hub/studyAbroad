# Local Development Setup - Quick Start

Follow these steps to start developing StudyAbroad locally.

## Prerequisites ✅

You already have:
- ✅ Docker & PostgreSQL running
- ✅ Database initialized with tables and seed data
- ✅ Node.js and npm installed
- ✅ Python 3.9+ (recommend upgrading to 3.12+ later)

## Step 1: Get API Keys (5 minutes)

You need **2 sets of credentials**:

### A. Google OAuth Credentials (for user login)

1. Go to: https://console.cloud.google.com/apis/credentials
2. Click **"Create Credentials"** → **"OAuth client ID"**
3. If prompted, configure OAuth consent screen first:
   - User Type: **External**
   - App name: **Study Abroad Dev**
   - User support email: **your-email@gmail.com**
   - Developer contact: **your-email@gmail.com**
   - Save
4. Create OAuth Client ID:
   - Application type: **Web application**
   - Name: **Study Abroad Local Dev**
   - Authorized redirect URIs: **`http://localhost:3000/api/auth/callback/google`**
   - Click **Create**
5. **Copy the Client ID and Client Secret**

### B. Google Gemini API Key (for AI features)

1. Go to: https://aistudio.google.com/app/apikey
2. Click **"Create API Key"**
3. Select your Google Cloud project (or create new)
4. **Copy the API key**

---

## Step 2: Configure Environment Variables (2 minutes)

### Frontend Configuration

Edit: `apps/study-abroad/frontend/.env.local`

**Replace these lines:**
```bash
GOOGLE_CLIENT_ID=your-google-client-id-here
GOOGLE_CLIENT_SECRET=your-google-client-secret-here
```

**With your actual values:**
```bash
GOOGLE_CLIENT_ID=123456789-abcdef.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=GOCSPX-your_actual_secret_here
```

### Backend Configuration

Edit: `apps/study-abroad/backend/.env`

**Replace this line:**
```bash
GOOGLE_API_KEY=your-google-gemini-api-key-here
```

**With your actual key:**
```bash
GOOGLE_API_KEY=AIzaSyYour_Actual_Gemini_Key_Here
```

**That's it!** Everything else is already configured with working defaults.

---

## Step 3: Install Dependencies (3 minutes)

### Frontend

```bash
cd apps/study-abroad/frontend
npm install
```

Expected output: `added XXX packages`

### Backend

```bash
cd apps/study-abroad/backend

# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

Expected output: Successfully installed packages...

---

## Step 4: Start Development Servers (1 minute)

Open **2 terminal windows**:

### Terminal 1: Frontend

```bash
cd apps/study-abroad/frontend
npm run dev
```

**Expected output:**
```
  ▲ Next.js 16.1.1
  - Local:        http://localhost:3000
  - Ready in XXXms
```

✅ Frontend running at: **http://localhost:3000**

### Terminal 2: Backend

```bash
cd apps/study-abroad/backend
source venv/bin/activate
uvicorn app.main:app --reload
```

**Expected output:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

✅ Backend running at: **http://localhost:8000**

---

## Step 5: Verify Everything Works

### Test Backend API

Open browser: http://localhost:8000

You should see:
```json
{
  "status": "ok",
  "message": "Study Abroad API is running"
}
```

### Test API Docs

Open browser: http://localhost:8000/docs

You should see: **FastAPI Swagger UI** with API documentation

### Test Frontend

Open browser: http://localhost:3000

You should see: **Next.js welcome page** or your app's home page

### Test Database Connection

```bash
docker exec study-abroad-postgres psql -U studyabroad -d studyabroad_dev -c "SELECT COUNT(*) FROM countries;"
```

Expected: `8` countries

---

## You're Ready! 🎉

### Your Development Environment

```
┌──────────────────────────────────────┐
│  Frontend: http://localhost:3000     │
│  Backend:  http://localhost:8000     │
│  API Docs: http://localhost:8000/docs│
│  Database: localhost:5432            │
└──────────────────────────────────────┘
```

### What You Can Do Now

✅ **Develop features** - Edit code and see live changes
✅ **Test authentication** - Google OAuth login works
✅ **Use AI features** - Gemini API is connected
✅ **Access database** - PostgreSQL with seed data ready
✅ **View API docs** - Interactive Swagger UI

---

## Common Issues

### Frontend won't start

**Error**: `Cannot find module 'next'`

**Solution**:
```bash
cd apps/study-abroad/frontend
rm -rf node_modules package-lock.json
npm install
```

### Backend won't start

**Error**: `ModuleNotFoundError: No module named 'fastapi'`

**Solution**:
```bash
cd apps/study-abroad/backend
source venv/bin/activate
pip install -r requirements.txt
```

### OAuth not working

**Error**: `redirect_uri_mismatch`

**Solution**: Ensure your Google OAuth redirect URI is exactly:
```
http://localhost:3000/api/auth/callback/google
```

### Database connection error

**Error**: `could not connect to server`

**Solution**:
```bash
# Check if PostgreSQL is running
docker ps | grep postgres

# If not running, start it
cd infrastructure/docker
docker-compose up -d postgres
```

---

## Next Steps

1. **Read the docs**: Check `docs/` folder for guides
2. **Create features**: Start building with the Constitution standards
3. **Run tests**: `npm run test` (frontend) / `pytest` (backend)
4. **Check quality gates**: See `agents/checklists/`

---

## Environment Variables Summary

### What's Already Configured ✅

- App URLs (localhost)
- Database connection
- CORS settings
- Development secrets
- API endpoints

### What You Added ✅

- Google OAuth Client ID & Secret
- Google Gemini API Key

### What You DON'T Need (Yet)

- Production secrets (only needed when deploying)
- Supabase credentials (using local PostgreSQL)
- Other API keys (add as you need features)

---

## Quick Reference

```bash
# Start frontend
cd apps/study-abroad/frontend && npm run dev

# Start backend
cd apps/study-abroad/backend && source venv/bin/activate && uvicorn app.main:app --reload

# Check database
docker exec study-abroad-postgres psql -U studyabroad -d studyabroad_dev -c "\dt"

# View logs
docker logs study-abroad-postgres  # Database
# Frontend logs in terminal
# Backend logs in terminal

# Stop everything
# Ctrl+C in terminals (frontend & backend)
docker-compose -f infrastructure/docker/docker-compose.yml down  # Database
```

Happy coding! 🚀
