#!/bin/bash
# Native PostgreSQL Setup Script (No Docker Required)
# Sets up PostgreSQL directly on macOS using Homebrew

set -e

echo "🗄️  Study Abroad - Native PostgreSQL Setup"
echo "=========================================="
echo ""

# Check if Homebrew is installed
if ! command -v brew &> /dev/null; then
    echo "❌ Homebrew is not installed. Please install it first:"
    echo "   /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
    exit 1
fi

echo "✅ Homebrew is installed"

# Check if PostgreSQL is already installed
if brew list postgresql@16 &> /dev/null; then
    echo "✅ PostgreSQL 16 is already installed"
else
    echo "📦 Installing PostgreSQL 16..."
    brew install postgresql@16
fi

# Start PostgreSQL service
echo "🚀 Starting PostgreSQL service..."
brew services start postgresql@16

# Wait a moment for PostgreSQL to start
sleep 3

# Create database and user
echo "👤 Creating database user and database..."

# Create user (if doesn't exist)
psql postgres -c "CREATE USER studyabroad WITH PASSWORD 'studyabroad_dev';" 2>/dev/null || echo "  User 'studyabroad' already exists"

# Create database (if doesn't exist)
psql postgres -c "CREATE DATABASE studyabroad_dev OWNER studyabroad;" 2>/dev/null || echo "  Database 'studyabroad_dev' already exists"

# Grant privileges
psql postgres -c "GRANT ALL PRIVILEGES ON DATABASE studyabroad_dev TO studyabroad;"

echo "📝 Initializing database schema..."

# Run initialization scripts
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

if [ -d "$PROJECT_ROOT/backend/database/init" ]; then
    for sql_file in "$PROJECT_ROOT/backend/database/init"/*.sql; do
        if [ -f "$sql_file" ]; then
            echo "  Running $(basename "$sql_file")..."
            psql -U studyabroad -d studyabroad_dev -f "$sql_file"
        fi
    done
else
    echo "⚠️  Warning: Database init scripts not found at $PROJECT_ROOT/backend/database/init"
fi

# Check if .env exists in backend
if [ ! -f "$PROJECT_ROOT/backend/.env" ]; then
    echo "📝 Creating backend .env file..."
    cp "$PROJECT_ROOT/backend/.env.example" "$PROJECT_ROOT/backend/.env"
    echo "⚠️  Please edit backend/.env and add your API keys"
fi

echo ""
echo "✅ Native PostgreSQL setup complete!"
echo ""
echo "Database Information:"
echo "  Host:     localhost"
echo "  Port:     5432"
echo "  Database: studyabroad_dev"
echo "  Username: studyabroad"
echo "  Password: studyabroad_dev"
echo ""
echo "PostgreSQL Management:"
echo "  Start:    brew services start postgresql@16"
echo "  Stop:     brew services stop postgresql@16"
echo "  Restart:  brew services restart postgresql@16"
echo "  Status:   brew services list | grep postgresql"
echo ""
echo "Connect via psql:"
echo "  psql postgresql://studyabroad:studyabroad_dev@localhost:5432/studyabroad_dev"
echo ""
echo "Next steps:"
echo "  1. Edit backend/.env with your API keys (especially GOOGLE_API_KEY)"
echo "  2. Install backend dependencies: cd backend && pip install -r requirements.txt"
echo "  3. Start the backend: cd backend && uvicorn app.main:app --reload"
