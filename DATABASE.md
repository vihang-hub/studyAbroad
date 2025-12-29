# Database Documentation

## Overview

This project uses **PostgreSQL 16** with **Row Level Security (RLS)** for local development and production. The database design ensures data isolation, mandatory citations for RAG, and scalability.

## Schema

### Core Tables

#### users
User profiles with OAuth integration.
```sql
- id: UUID (PK)
- email: VARCHAR(255) UNIQUE NOT NULL
- google_id: VARCHAR(255) UNIQUE
- full_name: VARCHAR(255)
- avatar_url: TEXT
- created_at, updated_at, last_login: TIMESTAMP
```

#### countries
Study abroad destination countries.
```sql
- id: UUID (PK)
- code: VARCHAR(3) UNIQUE NOT NULL (e.g., "USA", "GBR")
- name: VARCHAR(255) NOT NULL
- description: TEXT
- created_at, updated_at: TIMESTAMP
```

#### subjects
Academic programs and subjects.
```sql
- id: UUID (PK)
- name: VARCHAR(255) NOT NULL
- category: VARCHAR(100)
- description: TEXT
- created_at, updated_at: TIMESTAMP
```

#### chat_sessions
User conversation sessions.
```sql
- id: UUID (PK)
- user_id: UUID (FK to users)
- title: VARCHAR(500)
- created_at, updated_at, last_message_at: TIMESTAMP
```

#### chat_messages
Individual messages in conversations.
```sql
- id: UUID (PK)
- session_id: UUID (FK to chat_sessions)
- role: VARCHAR(20) CHECK (role IN ('user', 'assistant', 'system'))
- content: TEXT NOT NULL
- created_at: TIMESTAMP
```

#### citations
RAG citations for message sources (mandatory per Constitution).
```sql
- id: UUID (PK)
- message_id: UUID (FK to chat_messages)
- source_document: VARCHAR(500)
- source_url: TEXT
- excerpt: TEXT
- relevance_score: FLOAT
- created_at: TIMESTAMP
```

#### documents
Vector store metadata for RAG.
```sql
- id: UUID (PK)
- title: VARCHAR(500) NOT NULL
- content: TEXT NOT NULL
- source_url: TEXT
- country_id: UUID (FK to countries, nullable)
- subject_id: UUID (FK to subjects, nullable)
- document_type: VARCHAR(100)
- metadata: JSONB
- created_at, updated_at: TIMESTAMP
```

## Row Level Security (RLS)

Per Constitution Section 2, all tables have RLS enabled.

### Users Table
- Users can SELECT/UPDATE only their own profile
- `user_id` set via `set_user_context(user_id)` function

### Chat Sessions & Messages
- Users can only access their own sessions and messages
- Enforced via `user_id` context in session config

### Citations
- Users can only see citations from their own messages
- Enforced via JOIN to chat_sessions

### Documents
- All authenticated users can READ (public knowledge base)
- Only service role can INSERT/UPDATE (via application)

## Setting User Context

To enable RLS in application code:

```python
from app.core.db_utils import set_rls_context

async def protected_route(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Set RLS context for this session
    await set_rls_context(db, current_user.id)

    # Now queries respect RLS policies
    sessions = await db.execute(select(ChatSession))
```

## Indexes

Performance indexes are automatically created:

### B-Tree Indexes
- `users.email`, `users.google_id`
- `chat_sessions.user_id`
- `chat_messages.session_id`
- `citations.message_id`
- `documents.country_id`, `documents.subject_id`
- `chat_sessions.last_message_at DESC` (for sorting)

### Full-Text Search Indexes (GIN)
- `documents.content` (English)
- `documents.title` (English)

## Migrations

### Creating a Migration

```bash
cd backend

# Auto-generate migration from model changes
alembic revision --autogenerate -m "add new field to users"

# Or create empty migration
alembic revision -m "custom migration"
```

### Applying Migrations

```bash
# Upgrade to latest
alembic upgrade head

# Upgrade by 1 version
alembic upgrade +1

# Downgrade by 1 version
alembic downgrade -1

# Downgrade to specific version
alembic downgrade <revision_id>
```

### Migration Best Practices

1. **Always review auto-generated migrations** - Alembic may miss custom SQL
2. **Test migrations on copy of production data** before deploying
3. **Include both upgrade() and downgrade()** functions
4. **Add indexes in separate migrations** for large tables
5. **Never delete migrations** that have been applied to production

## Seed Data

Initial seed data is in `backend/database/init/03_seed_data.sql`:

- 8 sample countries (USA, GBR, CAN, AUS, DEU, FRA, JPN, NLD)
- 8 sample subjects (CS, Business, Engineering, Medicine, etc.)

Users and chat data are created by the application.

## Backup & Restore

### Backup

```bash
# Full database backup
docker exec study-abroad-postgres pg_dump -U studyabroad studyabroad_dev > backup.sql

# Schema only
docker exec study-abroad-postgres pg_dump -U studyabroad --schema-only studyabroad_dev > schema.sql

# Data only
docker exec study-abroad-postgres pg_dump -U studyabroad --data-only studyabroad_dev > data.sql
```

### Restore

```bash
# Restore full backup
docker exec -i study-abroad-postgres psql -U studyabroad studyabroad_dev < backup.sql
```

## Troubleshooting

### Connection Issues

```bash
# Check if PostgreSQL is running
docker ps | grep postgres

# Check logs
docker logs study-abroad-postgres

# Test connection
psql postgresql://studyabroad:studyabroad_dev@localhost:5432/studyabroad_dev -c "SELECT 1"
```

### Reset Database

```bash
# Nuclear option: delete everything and start fresh
docker-compose down -v
docker-compose up -d postgres
```

### RLS Issues

If queries return empty results unexpectedly:

```sql
-- Check if RLS is enabled
SELECT tablename, rowsecurity FROM pg_tables WHERE schemaname = 'public';

-- Check current user context
SHOW app.user_id;

-- Temporarily disable RLS for debugging (admin only)
ALTER TABLE users DISABLE ROW LEVEL SECURITY;
```

## Production Considerations

### Performance

1. **Connection Pooling**: Configure `pool_size` and `max_overflow` in `app/core/database.py`
2. **Read Replicas**: For high read volume, add read replicas
3. **Query Optimization**: Use `EXPLAIN ANALYZE` to optimize slow queries
4. **Partitioning**: Consider table partitioning for chat_messages at scale

### Security

1. **Rotate Credentials**: Never use dev credentials in production
2. **TLS Required**: Enable `sslmode=require` in production DATABASE_URL
3. **Backup Encryption**: Encrypt backups at rest
4. **Audit Logs**: Enable PostgreSQL audit logging for compliance

### Monitoring

1. **Connection Pool**: Monitor pool exhaustion
2. **Slow Queries**: Log queries >100ms
3. **RLS Performance**: Monitor RLS policy evaluation overhead
4. **Disk Usage**: Alert on >80% disk usage

## Vector Store Integration

Documents table stores metadata, while vector embeddings are in ChromaDB:

```python
# Document ingestion flow
1. Insert document metadata → documents table
2. Generate embeddings → ChromaDB
3. Link via document.id
```

Citations are mandatory per Constitution Section 4 (RAG Integrity).
