# Database Commands Reference

Quick reference for checking and managing your PostgreSQL database.

## Current Setup

- **Container**: `study-abroad-postgres`
- **Host**: `localhost:5432`
- **User**: `studyabroad`
- **Password**: `studyabroad_dev`
- **Databases**:
  - `studyabroad_dev` (main)
  - `postgres` (default)

---

## Quick Commands

### List All Databases

```bash
docker exec study-abroad-postgres psql -U studyabroad -l
```

### Connect to Database

```bash
# Interactive psql session
docker exec -it study-abroad-postgres psql -U studyabroad -d studyabroad_dev

# Or from your local machine (if psql installed)
psql postgresql://studyabroad:studyabroad_dev@localhost:5432/studyabroad_dev
```

### List Tables

```bash
docker exec study-abroad-postgres psql -U studyabroad -d studyabroad_dev -c "\dt"
```

### Describe a Table

```bash
docker exec study-abroad-postgres psql -U studyabroad -d studyabroad_dev -c "\d users"
docker exec study-abroad-postgres psql -U studyabroad -d studyabroad_dev -c "\d countries"
```

### Count Rows in Tables

```bash
# All tables at once
docker exec study-abroad-postgres psql -U studyabroad -d studyabroad_dev -c "
SELECT
  schemaname,
  tablename,
  (SELECT COUNT(*) FROM users) as users_count,
  (SELECT COUNT(*) FROM countries) as countries_count,
  (SELECT COUNT(*) FROM subjects) as subjects_count,
  (SELECT COUNT(*) FROM chat_sessions) as sessions_count,
  (SELECT COUNT(*) FROM chat_messages) as messages_count,
  (SELECT COUNT(*) FROM citations) as citations_count,
  (SELECT COUNT(*) FROM documents) as documents_count
FROM pg_tables
WHERE schemaname = 'public'
LIMIT 1;
"

# Or one table at a time
docker exec study-abroad-postgres psql -U studyabroad -d studyabroad_dev -c "SELECT COUNT(*) FROM countries;"
```

### View Data

```bash
# View all countries
docker exec study-abroad-postgres psql -U studyabroad -d studyabroad_dev -c "SELECT * FROM countries;"

# View all subjects
docker exec study-abroad-postgres psql -U studyabroad -d studyabroad_dev -c "SELECT * FROM subjects;"

# View specific columns
docker exec study-abroad-postgres psql -U studyabroad -d studyabroad_dev -c "SELECT code, name FROM countries;"

# Limit results
docker exec study-abroad-postgres psql -U studyabroad -d studyabroad_dev -c "SELECT * FROM countries LIMIT 5;"

# With WHERE clause
docker exec study-abroad-postgres psql -U studyabroad -d studyabroad_dev -c "SELECT * FROM countries WHERE code = 'USA';"
```

---

## Interactive psql Session

For more complex queries, use interactive mode:

```bash
# Enter psql
docker exec -it study-abroad-postgres psql -U studyabroad -d studyabroad_dev

# Now you're in psql prompt: studyabroad_dev=#
```

### Useful psql Commands

Once inside psql:

```sql
-- List all databases
\l

-- List all tables
\dt

-- Describe a table (show columns)
\d users
\d countries

-- Show table with additional info
\d+ users

-- List all schemas
\dn

-- List all functions
\df

-- List all views
\dv

-- See current database
SELECT current_database();

-- See current user
SELECT current_user;

-- Run a query
SELECT * FROM countries;

-- Pretty format
\x
SELECT * FROM countries LIMIT 1;
\x  -- toggle off

-- Exit psql
\q
```

---

## Common Database Operations

### Check Database Size

```bash
docker exec study-abroad-postgres psql -U studyabroad -d studyabroad_dev -c "
SELECT
  pg_database.datname,
  pg_size_pretty(pg_database_size(pg_database.datname)) AS size
FROM pg_database
WHERE datname = 'studyabroad_dev';
"
```

### Check Table Sizes

```bash
docker exec study-abroad-postgres psql -U studyabroad -d studyabroad_dev -c "
SELECT
  schemaname,
  tablename,
  pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;
"
```

### Check Indexes

```bash
docker exec study-abroad-postgres psql -U studyabroad -d studyabroad_dev -c "\di"
```

### Check Row Level Security Policies

```bash
docker exec study-abroad-postgres psql -U studyabroad -d studyabroad_dev -c "
SELECT
  schemaname,
  tablename,
  policyname,
  permissive,
  roles,
  cmd
FROM pg_policies
WHERE schemaname = 'public';
"
```

---

## Data Inspection

### Check Seed Data

```bash
# Countries (should have 8)
docker exec study-abroad-postgres psql -U studyabroad -d studyabroad_dev -c "
SELECT code, name, description FROM countries;
"

# Subjects (should have 8)
docker exec study-abroad-postgres psql -U studyabroad -d studyabroad_dev -c "
SELECT name, category FROM subjects;
"
```

### Check for Users

```bash
docker exec study-abroad-postgres psql -U studyabroad -d studyabroad_dev -c "
SELECT id, email, full_name, created_at FROM users;
"
```

### Check Recent Activity

```bash
# Recent chat sessions
docker exec study-abroad-postgres psql -U studyabroad -d studyabroad_dev -c "
SELECT id, title, created_at, last_message_at
FROM chat_sessions
ORDER BY last_message_at DESC
LIMIT 10;
"
```

---

## Database Management

### Create a Backup

```bash
# Full backup
docker exec study-abroad-postgres pg_dump -U studyabroad studyabroad_dev > backup_$(date +%Y%m%d).sql

# Schema only
docker exec study-abroad-postgres pg_dump -U studyabroad --schema-only studyabroad_dev > schema_backup.sql

# Data only
docker exec study-abroad-postgres pg_dump -U studyabroad --data-only studyabroad_dev > data_backup.sql
```

### Restore from Backup

```bash
# Restore
docker exec -i study-abroad-postgres psql -U studyabroad studyabroad_dev < backup_20231229.sql
```

### Reset Database (⚠️ Deletes All Data)

```bash
# Stop containers
docker-compose -f infrastructure/docker/docker-compose.yml down

# Remove volumes (⚠️ DELETES ALL DATA)
docker volume rm study-abroad_postgres_data

# Start fresh
docker-compose -f infrastructure/docker/docker-compose.yml up -d postgres
```

---

## Creating New Databases for New Apps

```bash
# Create database for a new app
docker exec study-abroad-postgres psql -U studyabroad -c "CREATE DATABASE career_matcher_dev OWNER studyabroad;"

# Initialize with shared schemas
docker exec study-abroad-postgres psql -U studyabroad -d career_matcher_dev < /docker-entrypoint-initdb.d/01_init_schema.sql
docker exec study-abroad-postgres psql -U studyabroad -d career_matcher_dev < /docker-entrypoint-initdb.d/02_enable_rls.sql
docker exec study-abroad-postgres psql -U studyabroad -d career_matcher_dev < /docker-entrypoint-initdb.d/03_seed_data.sql

# Or from your local machine
createdb -U studyabroad career_matcher_dev
psql -U studyabroad -d career_matcher_dev < packages/shared-db/schemas/01_init_schema.sql
```

---

## Troubleshooting

### Check if PostgreSQL is Running

```bash
docker ps | grep postgres
```

### Check PostgreSQL Logs

```bash
docker logs study-abroad-postgres

# Follow logs in real-time
docker logs -f study-abroad-postgres
```

### Test Connection

```bash
docker exec study-abroad-postgres pg_isready -U studyabroad
# Output: /var/run/postgresql:5432 - accepting connections
```

### Connection Issues

```bash
# Check if port is open
lsof -i :5432

# Restart PostgreSQL
docker restart study-abroad-postgres

# Check health
docker inspect study-abroad-postgres | grep -A 5 Health
```

---

## GUI Tools (Alternative to Command Line)

### pgAdmin (Web-Based)

**Start pgAdmin:**
```bash
docker-compose -f infrastructure/docker/docker-compose.yml up -d pgadmin
```

**Access:**
- URL: http://localhost:5050
- Email: admin@studyabroad.local
- Password: admin

**Connect to Database:**
1. Click "Add New Server"
2. Name: Study Abroad Local
3. Host: postgres (container name)
4. Port: 5432
5. Database: studyabroad_dev
6. Username: studyabroad
7. Password: studyabroad_dev

### Other GUI Tools (macOS)

- **Postico** - https://eggerapps.at/postico/
- **TablePlus** - https://tableplus.com/
- **DBeaver** - https://dbeaver.io/ (free)

**Connection Details:**
- Host: localhost
- Port: 5432
- Database: studyabroad_dev
- User: studyabroad
- Password: studyabroad_dev

---

## Monitoring

### Active Connections

```bash
docker exec study-abroad-postgres psql -U studyabroad -d studyabroad_dev -c "
SELECT
  pid,
  usename,
  application_name,
  client_addr,
  state,
  query
FROM pg_stat_activity
WHERE datname = 'studyabroad_dev';
"
```

### Current Queries

```bash
docker exec study-abroad-postgres psql -U studyabroad -d studyabroad_dev -c "
SELECT
  pid,
  now() - query_start as duration,
  query,
  state
FROM pg_stat_activity
WHERE state != 'idle'
ORDER BY duration DESC;
"
```

---

## Quick Reference Card

```bash
# List databases
docker exec study-abroad-postgres psql -U studyabroad -l

# List tables
docker exec study-abroad-postgres psql -U studyabroad -d studyabroad_dev -c "\dt"

# Interactive psql
docker exec -it study-abroad-postgres psql -U studyabroad -d studyabroad_dev

# Run query
docker exec study-abroad-postgres psql -U studyabroad -d studyabroad_dev -c "YOUR QUERY HERE"

# Backup
docker exec study-abroad-postgres pg_dump -U studyabroad studyabroad_dev > backup.sql

# Restore
docker exec -i study-abroad-postgres psql -U studyabroad studyabroad_dev < backup.sql

# Check logs
docker logs study-abroad-postgres
```

---

Save this file for easy reference when working with your database!
