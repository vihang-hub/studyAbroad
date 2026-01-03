# Alembic Database Migrations

This directory contains database migration scripts for the MVP UK Study & Migration App backend using Alembic.

## Overview

**Migration Tool**: Alembic 1.13+  
**Database**: PostgreSQL 15+ (local) or Supabase (test/production)  
**Driver**: psycopg2 (synchronous migrations), asyncpg (runtime)

## Quick Start

### Prerequisites

1. Ensure PostgreSQL or Supabase is running
2. Set `DATABASE_URL` in `.env` file:
   ```bash
   # Local PostgreSQL
   DATABASE_URL=postgresql://postgres:postgres@localhost:54322/postgres
   
   # Supabase
   DATABASE_URL=postgresql://postgres:[PASSWORD]@db.[PROJECT_REF].supabase.co:5432/postgres
   ```

### Running Migrations

```bash
# Activate virtual environment
source venv/bin/activate

# Apply all pending migrations (upgrade to head)
alembic upgrade head

# Rollback one migration
alembic downgrade -1

# View current migration status
alembic current

# View migration history
alembic history --verbose
```

## Migration Files

### Initial Schema (`6f815ac9ca51_initial_schema.py`)

Creates the complete database schema:

**Tables**:
- `users`: Authenticated user data (Clerk integration)
- `reports`: AI-generated study & migration reports
- `payments`: Stripe payment transactions

**ENUM Types**:
- `reportstatus`: `pending`, `generating`, `completed`, `failed`, `expired`
- `paymentstatus`: `pending`, `succeeded`, `failed`, `refunded`

**Indexes**:
- `idx_users_clerk_user_id` (unique)
- `idx_users_email`
- `idx_reports_user_id`
- `idx_reports_status`
- `idx_reports_expires_at`
- `idx_payments_user_id`
- `idx_payments_report_id`
- `idx_payments_stripe_session` (unique)
- `idx_payments_stripe_intent` (unique)

**Triggers**:
- `update_users_updated_at`: Auto-update `updated_at` on user changes
- `update_reports_updated_at`: Auto-update `updated_at` on report changes

## Creating New Migrations

### Automatic (Recommended when possible)

```bash
# Autogenerate migration from model changes
alembic revision --autogenerate -m "description_of_change"

# Review the generated file in alembic/versions/
# Edit if necessary, then apply:
alembic upgrade head
```

**Note**: Autogenerate requires a running database connection and may not detect all changes (e.g., server defaults, triggers). Always review generated migrations.

### Manual

```bash
# Create blank migration file
alembic revision -m "description_of_change"

# Edit the file in alembic/versions/
# Implement upgrade() and downgrade() functions
# Apply migration:
alembic upgrade head
```

## Common Operations

### Reset Database (Development Only)

```bash
# Downgrade all migrations
alembic downgrade base

# Reapply all migrations
alembic upgrade head
```

**Warning**: This will DROP all tables and data!

### Check Migration Status

```bash
# Show current revision
alembic current

# Show all migrations and their status
alembic history

# Show pending migrations
alembic heads
```

### Rollback to Specific Revision

```bash
# Rollback to specific revision
alembic downgrade <revision_id>

# Example:
alembic downgrade 6f815ac9ca51
```

## Environment Configuration

The `env.py` file is configured to:

1. Load environment variables from `.env` file using `python-dotenv`
2. Import SQLAlchemy models from `database.models`
3. Support both local PostgreSQL and Supabase connection strings
4. Use `psycopg2` for synchronous migrations
5. Enable type and server default comparison for autogenerate

### Important Notes

- **Database URL**: Always loaded from `DATABASE_URL` environment variable
- **Model Import**: Models are imported from `database.models.user`, `database.models.report`, `database.models.payment`
- **Python Version**: Requires Python 3.12+ (due to type hints in models)

## Feature Flag Integration

Migrations support both local PostgreSQL and Supabase:

```python
# In .env
ENABLE_SUPABASE=false  # Use local PostgreSQL
DATABASE_URL=postgresql://postgres:postgres@localhost:54322/postgres

# OR for Supabase
ENABLE_SUPABASE=true
DATABASE_URL=postgresql://postgres:[PASSWORD]@db.[PROJECT_REF].supabase.co:5432/postgres
```

## Troubleshooting

### Connection Refused Error

```bash
psycopg2.OperationalError: connection to server at "localhost", port 54322 failed
```

**Solution**: Ensure PostgreSQL or Supabase local instance is running:

```bash
# Start Supabase (if using Supabase CLI)
supabase start

# OR ensure PostgreSQL service is running
brew services start postgresql@15
```

### Module Import Errors

```bash
ModuleNotFoundError: No module named 'database'
```

**Solution**: Ensure virtual environment is activated and dependencies are installed:

```bash
source venv/bin/activate
pip install -e ".[dev]"
```

### Autogenerate Doesn't Detect Changes

**Causes**:
- Server defaults (`server_default`) are not always detected
- Triggers and functions are never auto-detected
- ENUM changes may require manual intervention

**Solution**: Create manual migrations for:
- Trigger functions
- Server-side defaults
- ENUM type modifications

## Best Practices

1. **Always Review Autogenerated Migrations**: Autogenerate is helpful but not perfect
2. **Test Migrations Locally First**: Run `upgrade` and `downgrade` to ensure they work
3. **One Logical Change Per Migration**: Keep migrations focused and atomic
4. **Never Edit Applied Migrations**: Create new migrations instead
5. **Use Descriptive Names**: `add_user_preferences` not `update_schema`
6. **Include Downgrade Logic**: Always implement `downgrade()` for rollback capability
7. **Version Control**: Commit migration files to git
8. **Production Safety**: Test migrations on staging before production

## Migration Workflow

### Development

```bash
# 1. Modify SQLAlchemy models in src/database/models/
# 2. Create migration
alembic revision --autogenerate -m "add_user_preferences_table"

# 3. Review and edit migration file
# 4. Test upgrade
alembic upgrade head

# 5. Test downgrade
alembic downgrade -1

# 6. Re-upgrade
alembic upgrade head

# 7. Commit migration file to git
```

### Production

```bash
# 1. Pull latest migrations from git
# 2. Review migrations to be applied
alembic history

# 3. Backup database (CRITICAL!)
# 4. Apply migrations
alembic upgrade head

# 5. Verify success
alembic current
```

## ADR References

This migration setup follows:

- **ADR-0003**: Database Abstraction Layer
  - Migrations use SQLAlchemy models as source of truth
  - Support for both PostgreSQL and Supabase

- **ADR-0005**: Soft Delete Pattern
  - Reports use `status='expired'` instead of hard deletes
  - `expires_at` timestamp for data retention

## Support

For migration issues, refer to:
- [Alembic Documentation](https://alembic.sqlalchemy.org/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- Project Specification: `/Users/vihang/projects/study-abroad/specs/001-mvp-uk-study-migration/data-model.md`
