#!/bin/bash
# Create New Application Script
# Usage: ./infrastructure/scripts/create-new-app.sh <app-name>

set -e

APP_NAME=$1

if [ -z "$APP_NAME" ]; then
    echo "❌ Error: Please provide an app name"
    echo "Usage: ./infrastructure/scripts/create-new-app.sh <app-name>"
    exit 1
fi

# Validate app name (lowercase, hyphens only)
if ! [[ "$APP_NAME" =~ ^[a-z][a-z0-9-]*$ ]]; then
    echo "❌ Error: App name must be lowercase with hyphens only (e.g., 'my-new-app')"
    exit 1
fi

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
APP_DIR="$PROJECT_ROOT/apps/$APP_NAME"

echo "🚀 Creating new application: $APP_NAME"
echo "================================================"
echo ""

# Check if app already exists
if [ -d "$APP_DIR" ]; then
    echo "❌ Error: App '$APP_NAME' already exists at $APP_DIR"
    exit 1
fi

# Create app directory
echo "📁 Creating directory structure..."
mkdir -p "$APP_DIR"/{frontend,backend}

# ============================================================================
# FRONTEND SETUP
# ============================================================================

echo "⚛️  Setting up Next.js frontend..."
cd "$APP_DIR/frontend"

# Create Next.js app
npx create-next-app@latest . \
    --ts \
    --tailwind \
    --eslint \
    --app \
    --src-dir \
    --import-alias "@/*" \
    --use-npm \
    --no-git \
    --skip-install

# Add shared packages to package.json
cat > package.json.tmp << EOF
{
  "name": "$APP_NAME-frontend",
  "version": "0.1.0",
  "private": true,
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "eslint",
    "test": "vitest",
    "test:coverage": "vitest run --coverage",
    "type-check": "tsc --noEmit"
  },
  "dependencies": {
    "@studyabroad/shared-auth-frontend": "workspace:*",
    "@studyabroad/shared-ui": "workspace:*",
    "@studyabroad/shared-types": "workspace:*",
    "@ai-sdk/react": "^3.0.3",
    "ai": "^6.0.3",
    "class-variance-authority": "^0.7.1",
    "clsx": "^2.1.1",
    "lucide-react": "^0.562.0",
    "next": "16.1.1",
    "next-auth": "^5.0.0-beta",
    "react": "19.2.3",
    "react-dom": "19.2.3",
    "tailwind-merge": "^3.4.0"
  },
  "devDependencies": {
    "@tailwindcss/postcss": "^4",
    "@types/node": "^20",
    "@types/react": "^19",
    "@types/react-dom": "^19",
    "@vitejs/plugin-react": "^4",
    "@vitest/ui": "^2",
    "eslint": "^9",
    "eslint-config-next": "16.1.1",
    "tailwindcss": "^4",
    "typescript": "^5",
    "vitest": "^2"
  }
}
EOF
mv package.json.tmp package.json

# Create .env.example
cat > .env.example << 'EOF'
# App Configuration
NEXT_PUBLIC_APP_NAME=$APP_NAME
NEXT_PUBLIC_APP_URL=http://localhost:3000

# API Configuration
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_API_V1_PREFIX=/api/v1

# Auth.js Configuration
NEXTAUTH_URL=http://localhost:3000
NEXTAUTH_SECRET=generate-with-openssl-rand-base64-32

# Google OAuth
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
EOF

# Create auth.ts using shared auth
mkdir -p src
cat > src/auth.ts << 'EOF'
import NextAuth from "next-auth"
import Google from "next-auth/providers/google"

export const { handlers, signIn, signOut, auth } = NextAuth({
  providers: [
    Google({
      clientId: process.env.GOOGLE_CLIENT_ID!,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
    }),
  ],
  callbacks: {
    async jwt({ token, account, profile }) {
      if (account && profile) {
        token.id = profile.sub
        token.email = profile.email
      }
      return token
    },
    async session({ session, token }) {
      if (session.user) {
        session.user.id = token.id as string
      }
      return session
    },
  },
})
EOF

echo "✅ Frontend created"

# ============================================================================
# BACKEND SETUP
# ============================================================================

echo "🐍 Setting up FastAPI backend..."
cd "$APP_DIR/backend"

# Create directory structure
mkdir -p app/{api,core,models,services} tests database/init

# Create requirements.txt
cat > requirements.txt << 'EOF'
# FastAPI and Web Framework
fastapi==0.115.6
uvicorn[standard]==0.34.0
python-multipart==0.0.20
pydantic==2.10.5
pydantic-settings==2.7.1

# CORS and Security
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-dotenv==1.0.1

# LangChain for AI/RAG
langchain==0.3.16
langchain-google-genai==2.0.8

# Database
asyncpg==0.30.0
sqlalchemy==2.0.36
alembic==1.14.0
psycopg2-binary==2.9.10

# Google Cloud
google-generativeai==0.8.3

# Development
pytest==8.3.4
pytest-asyncio==0.24.0
black==24.10.0
ruff==0.8.5

# Shared packages (local)
-e ../../../packages/shared-db
EOF

# Create .env.example
DB_NAME="${APP_NAME//-/_}_dev"
cat > .env.example << EOF
# API Configuration
API_V1_PREFIX=/api/v1
PROJECT_NAME=$APP_NAME API
ENVIRONMENT=development
DEBUG=True

# CORS Configuration
CORS_ORIGINS=["http://localhost:3000"]

# Local PostgreSQL Database
DATABASE_URL=postgresql://studyabroad:studyabroad_dev@localhost:5432/$DB_NAME

# Google Gemini API
GOOGLE_API_KEY=your-google-api-key

# Authentication
SECRET_KEY=generate-with-openssl-rand-hex-32
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
EOF

# Create main.py
cat > app/main.py << 'EOF'
"""
$APP_NAME FastAPI Application
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="$APP_NAME API",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"status": "ok", "message": "$APP_NAME API is running"}

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "$APP_NAME-api",
        "version": "0.1.0",
    }
EOF

# Create config.py
cat > app/core/config.py << 'EOF'
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    API_V1_PREFIX: str = "/api/v1"
    PROJECT_NAME: str = "$APP_NAME API"
    CORS_ORIGINS: List[str] = ["http://localhost:3000"]
    DATABASE_URL: str = ""
    GOOGLE_API_KEY: str = ""
    SECRET_KEY: str = ""
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ENVIRONMENT: str = "development"
    DEBUG: bool = True

settings = Settings()
EOF

# Create __init__.py files
touch app/__init__.py app/core/__init__.py app/api/__init__.py app/models/__init__.py app/services/__init__.py

echo "✅ Backend created"

# ============================================================================
# DATABASE SETUP
# ============================================================================

echo "🗄️  Setting up database..."

# Link shared database schemas
ln -s ../../../packages/shared-db/schemas/*.sql database/init/

# Create app-specific schema
cat > database/init/10_app_tables.sql << 'EOF'
-- $APP_NAME specific tables
-- Add your application-specific tables here

-- Example table
-- CREATE TABLE app_data (
--     id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
--     user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
--     data JSONB,
--     created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
-- );
--
-- ALTER TABLE app_data ENABLE ROW LEVEL SECURITY;
--
-- CREATE POLICY app_data_select_own ON app_data
--     FOR SELECT
--     USING (user_id = current_setting('app.user_id', true)::UUID);
EOF

echo "✅ Database schemas configured"

# ============================================================================
# CREATE APP README
# ============================================================================

cat > "$APP_DIR/README.md" << EOF
# $APP_NAME

[Brief description of your application]

## Tech Stack

- **Frontend**: Next.js 16+ (App Router) with TypeScript
- **Backend**: FastAPI (Python 3.12+)
- **Database**: PostgreSQL 16+ with RLS
- **Auth**: Auth.js (Google OAuth)

## Getting Started

\`\`\`bash
# Install dependencies
cd apps/$APP_NAME/frontend && npm install
cd ../backend && python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt

# Setup environment
cp frontend/.env.example frontend/.env.local
cp backend/.env.example backend/.env

# Create database
createdb $DB_NAME
psql $DB_NAME < backend/database/init/*.sql

# Start development
cd frontend && npm run dev  # http://localhost:3000
cd backend && uvicorn app.main:app --reload  # http://localhost:8000
\`\`\`

## Development

\`\`\`bash
# From project root
cd apps/$APP_NAME

# Frontend
cd frontend
npm run dev
npm run build
npm run test

# Backend
cd backend
source venv/bin/activate
uvicorn app.main:app --reload
pytest
\`\`\`

## Shared Packages Used

- \`@studyabroad/shared-auth-frontend\` - Authentication components
- \`@studyabroad/shared-ui\` - UI components
- \`shared-db\` - Database utilities and schemas

## Database

Database: \`$DB_NAME\`

Uses shared schemas:
- users (from shared-db)
- [Add your app-specific tables here]

## Deployment

- Frontend: Vercel
- Backend: Google Cloud Run
- Database: Supabase or Cloud SQL

EOF

echo ""
echo "✅ Application '$APP_NAME' created successfully!"
echo ""
echo "📍 Location: $APP_DIR"
echo ""
echo "Next steps:"
echo "  1. cd apps/$APP_NAME"
echo "  2. Setup environment variables:"
echo "     cp frontend/.env.example frontend/.env.local"
echo "     cp backend/.env.example backend/.env"
echo "  3. Create database:"
echo "     createdb $DB_NAME"
echo "     psql $DB_NAME < backend/database/init/*.sql"
echo "  4. Install dependencies:"
echo "     cd frontend && npm install"
echo "     cd ../backend && python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt"
echo "  5. Start development:"
echo "     # Terminal 1: cd frontend && npm run dev"
echo "     # Terminal 2: cd backend && uvicorn app.main:app --reload"
echo ""
echo "Happy coding! 🎉"
