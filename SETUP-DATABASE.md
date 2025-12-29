# Database Setup Guide

You have two options for running the PostgreSQL database locally:

## Option 1: Docker (Recommended for Consistency)

### Prerequisites
- Docker Desktop installed

### Installation

#### Install Docker Desktop via Homebrew
```bash
brew install --cask docker
```

Or download from: https://www.docker.com/products/docker-desktop/

#### Start Docker Desktop
1. Open Docker Desktop from Applications folder
2. Wait for it to fully start (Docker icon appears in menu bar)
3. Verify installation:
   ```bash
   docker --version
   docker-compose --version
   ```

### Setup Database
```bash
# Automated setup
./scripts/setup-local-db.sh

# Or manual
docker-compose up -d postgres pgadmin
```

### Access
- **pgAdmin**: http://localhost:5050 (admin@studyabroad.local / admin)
- **psql**: `psql postgresql://studyabroad:studyabroad_dev@localhost:5432/studyabroad_dev`

### Management
```bash
# Start
docker-compose up -d postgres

# Stop
docker-compose down

# Reset (⚠️ deletes all data)
docker-compose down -v
docker-compose up -d postgres

# Logs
docker logs study-abroad-postgres
```

---

## Option 2: Native PostgreSQL (No Docker)

### Prerequisites
- Homebrew installed
- PostgreSQL 16 (installed by script)

### Installation & Setup

#### Quick Setup
```bash
./scripts/setup-native-postgres.sh
```

#### Manual Setup
```bash
# Install PostgreSQL 16
brew install postgresql@16

# Start PostgreSQL service
brew services start postgresql@16

# Create user and database
psql postgres -c "CREATE USER studyabroad WITH PASSWORD 'studyabroad_dev';"
psql postgres -c "CREATE DATABASE studyabroad_dev OWNER studyabroad;"
psql postgres -c "GRANT ALL PRIVILEGES ON DATABASE studyabroad_dev TO studyabroad;"

# Initialize schema
cd backend/database/init
for file in *.sql; do
    psql -U studyabroad -d studyabroad_dev -f "$file"
done
```

### Access
- **psql**: `psql postgresql://studyabroad:studyabroad_dev@localhost:5432/studyabroad_dev`
- **GUI Tools**: Use any PostgreSQL client (Postico, TablePlus, DBeaver, etc.)

### Management
```bash
# Start PostgreSQL
brew services start postgresql@16

# Stop PostgreSQL
brew services stop postgresql@16

# Restart PostgreSQL
brew services restart postgresql@16

# Check status
brew services list | grep postgresql

# Reset database
dropdb -U studyabroad studyabroad_dev
createdb -U studyabroad studyabroad_dev
# Then re-run initialization scripts
```

---

## Which Option Should I Choose?

### Choose Docker if:
- ✅ You want the exact same environment across all developers
- ✅ You plan to deploy to containerized environments (Cloud Run, etc.)
- ✅ You want pgAdmin included automatically
- ✅ You want easy cleanup (just delete containers/volumes)

### Choose Native PostgreSQL if:
- ✅ You don't want to install Docker
- ✅ You prefer lighter resource usage
- ✅ You already have PostgreSQL installed
- ✅ You want faster startup times

---

## Troubleshooting

### Docker Issues

**"Docker is not running"**
```bash
# Start Docker Desktop app from Applications
# Wait for Docker icon in menu bar to show "Docker Desktop is running"

# Verify
docker ps
```

**"Cannot connect to Docker daemon"**
```bash
# Ensure Docker Desktop is running
open -a Docker

# Wait ~30 seconds for it to fully start
```

**Port 5432 already in use**
```bash
# Check what's using port 5432
lsof -i :5432

# If it's native PostgreSQL, stop it
brew services stop postgresql@16

# Then start Docker
docker-compose up -d postgres
```

### Native PostgreSQL Issues

**"psql: command not found"**
```bash
# Add PostgreSQL to PATH
echo 'export PATH="/opt/homebrew/opt/postgresql@16/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

**"Connection refused"**
```bash
# Check if PostgreSQL is running
brew services list | grep postgresql

# Start if not running
brew services start postgresql@16

# Check logs
tail -f /opt/homebrew/var/log/postgresql@16.log
```

**"Role does not exist"**
```bash
# Create the user manually
createuser -s studyabroad

# Or via psql
psql postgres -c "CREATE USER studyabroad WITH PASSWORD 'studyabroad_dev' SUPERUSER;"
```

---

## Verifying Setup

After setup, verify your database is working:

```bash
# Test connection
psql postgresql://studyabroad:studyabroad_dev@localhost:5432/studyabroad_dev -c "SELECT version();"

# Check tables were created
psql postgresql://studyabroad:studyabroad_dev@localhost:5432/studyabroad_dev -c "\dt"

# Expected output:
#              List of relations
#  Schema |      Name       | Type  |   Owner
# --------+-----------------+-------+------------
#  public | chat_messages   | table | studyabroad
#  public | chat_sessions   | table | studyabroad
#  public | citations       | table | studyabroad
#  public | countries       | table | studyabroad
#  public | documents       | table | studyabroad
#  public | subjects        | table | studyabroad
#  public | users           | table | studyabroad

# Check seed data
psql postgresql://studyabroad:studyabroad_dev@localhost:5432/studyabroad_dev -c "SELECT COUNT(*) FROM countries;"
# Expected: 8 countries

psql postgresql://studyabroad:studyabroad_dev@localhost:5432/studyabroad_dev -c "SELECT COUNT(*) FROM subjects;"
# Expected: 8 subjects
```

---

## Next Steps

Once your database is set up:

1. **Configure backend environment:**
   ```bash
   cd backend
   cp .env.example .env
   # Edit .env and add your GOOGLE_API_KEY
   ```

2. **Install backend dependencies:**
   ```bash
   cd backend
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Start the backend:**
   ```bash
   cd backend
   source venv/bin/activate
   uvicorn app.main:app --reload
   ```

4. **Verify backend can connect:**
   - Visit http://localhost:8000/health
   - Should see: `{"status": "healthy"}`

Your local database is ready! 🎉
