#!/bin/bash
# Local Database Setup Script
# This script helps set up the local PostgreSQL database for development

set -e

echo "🗄️  Study Abroad - Local Database Setup"
echo "======================================"
echo ""

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Error: Docker is not running. Please start Docker and try again."
    exit 1
fi

echo "✅ Docker is running"
echo ""

# Check if database is already running
if docker ps | grep -q study-abroad-postgres; then
    echo "⚠️  Database container is already running"
    read -p "Do you want to stop and recreate it? (y/N) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "🛑 Stopping existing containers..."
        docker-compose down
    else
        echo "Exiting..."
        exit 0
    fi
fi

# Start PostgreSQL and pgAdmin
echo "🚀 Starting PostgreSQL and pgAdmin..."
docker-compose up -d postgres pgadmin

# Wait for PostgreSQL to be healthy
echo "⏳ Waiting for PostgreSQL to be ready..."
until docker exec study-abroad-postgres pg_isready -U studyabroad -d studyabroad_dev > /dev/null 2>&1; do
    echo -n "."
    sleep 1
done
echo ""
echo "✅ PostgreSQL is ready!"

# Check if .env exists in backend
if [ ! -f backend/.env ]; then
    echo "📝 Creating backend .env file..."
    cp backend/.env.example backend/.env
    echo "⚠️  Please edit backend/.env and add your API keys"
fi

echo ""
echo "✅ Local database setup complete!"
echo ""
echo "Database Information:"
echo "  Host:     localhost"
echo "  Port:     5432"
echo "  Database: studyabroad_dev"
echo "  Username: studyabroad"
echo "  Password: studyabroad_dev"
echo ""
echo "Access Points:"
echo "  📊 pgAdmin:   http://localhost:5050"
echo "              Email: admin@studyabroad.local"
echo "              Password: admin"
echo ""
echo "  💻 psql:      psql postgresql://studyabroad:studyabroad_dev@localhost:5432/studyabroad_dev"
echo ""
echo "Next steps:"
echo "  1. Edit backend/.env with your API keys (especially GOOGLE_API_KEY)"
echo "  2. Install backend dependencies: cd backend && pip install -r requirements.txt"
echo "  3. Run migrations: cd backend && alembic upgrade head"
echo "  4. Start the backend: cd backend && uvicorn app.main:app --reload"
echo ""
echo "To stop the database: docker-compose down"
echo "To reset the database: docker-compose down -v && $0"
