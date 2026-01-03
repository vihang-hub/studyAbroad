# Database Migration Checklist

Use this checklist when applying database migrations to ensure safe deployment.

## Pre-Migration Checklist

### Development Environment

- [ ] Virtual environment activated (`source venv/bin/activate`)
- [ ] All dependencies installed (`pip install -e ".[dev]"`)
- [ ] `.env` file configured with correct `DATABASE_URL`
- [ ] Database is running (PostgreSQL or Supabase)
- [ ] Current migration status checked (`alembic current`)
- [ ] Migration files reviewed for correctness
- [ ] Downgrade logic tested locally

### Staging/Production Environment

- [ ] Database backup completed and verified
- [ ] Backup restoration tested
- [ ] Migration files reviewed and approved
- [ ] Downtime window scheduled (if required)
- [ ] Rollback plan documented
- [ ] Team notified of migration
- [ ] Monitoring alerts configured

## Migration Steps

### Local Development

```bash
# 1. Check current status
./scripts/migrate.sh status

# 2. Review pending migrations
alembic history

# 3. Apply migrations
./scripts/migrate.sh upgrade

# 4. Verify success
./scripts/migrate.sh status

# 5. Test application
pytest
```

### Staging Environment

```bash
# 1. Backup database
pg_dump $DATABASE_URL > backup_$(date +%Y%m%d_%H%M%S).sql

# 2. Test backup restoration (on separate test DB)
createdb test_restore
psql test_restore < backup_*.sql

# 3. Check current migration status
alembic current

# 4. Review migrations to be applied
alembic history --verbose

# 5. Apply migrations
alembic upgrade head

# 6. Verify success
alembic current
psql $DATABASE_URL -c "\dt"  # List tables

# 7. Run smoke tests
pytest tests/integration/

# 8. Monitor application logs
```

### Production Environment

```bash
# 1. Enable maintenance mode (if applicable)
# PUT /api/maintenance/enable

# 2. Backup database
# Use automated backup + manual backup
pg_dump $DATABASE_URL > backup_$(date +%Y%m%d_%H%M%S).sql
# Upload to S3/secure storage

# 3. Verify backup
# Test restoration on staging

# 4. Apply migrations
alembic upgrade head 2>&1 | tee migration_$(date +%Y%m%d_%H%M%S).log

# 5. Verify migration success
alembic current
psql $DATABASE_URL -c "SELECT COUNT(*) FROM users;"
psql $DATABASE_URL -c "SELECT COUNT(*) FROM reports;"
psql $DATABASE_URL -c "SELECT COUNT(*) FROM payments;"

# 6. Run post-migration tests
pytest tests/integration/ --production

# 7. Monitor application health
# Check logs, metrics, error rates

# 8. Disable maintenance mode
# DELETE /api/maintenance/disable

# 9. Monitor for issues (15-30 minutes)
# Watch error rates, response times, database connections
```

## Post-Migration Verification

### Data Integrity Checks

```sql
-- Verify table structure
SELECT table_name, column_name, data_type 
FROM information_schema.columns 
WHERE table_schema = 'public' 
ORDER BY table_name, ordinal_position;

-- Check foreign key constraints
SELECT
    tc.table_name, 
    kcu.column_name, 
    ccu.table_name AS foreign_table_name,
    ccu.column_name AS foreign_column_name 
FROM information_schema.table_constraints AS tc 
JOIN information_schema.key_column_usage AS kcu
  ON tc.constraint_name = kcu.constraint_name
JOIN information_schema.constraint_column_usage AS ccu
  ON ccu.constraint_name = tc.constraint_name
WHERE tc.constraint_type = 'FOREIGN KEY';

-- Verify indexes
SELECT
    tablename,
    indexname,
    indexdef
FROM pg_indexes
WHERE schemaname = 'public'
ORDER BY tablename, indexname;

-- Check triggers
SELECT
    event_object_table AS table_name,
    trigger_name,
    event_manipulation AS event
FROM information_schema.triggers
WHERE trigger_schema = 'public';
```

### Application Health Checks

- [ ] Users can authenticate
- [ ] Payments can be created
- [ ] Reports can be generated
- [ ] API endpoints respond correctly
- [ ] Database queries perform within SLA
- [ ] No error spikes in logs
- [ ] Background jobs running

## Rollback Procedure

### If Migration Fails

```bash
# 1. Check error message
cat migration_*.log

# 2. Identify failed migration
alembic current

# 3. Rollback to previous version
alembic downgrade -1

# 4. Verify rollback success
alembic current

# 5. Restore from backup (if needed)
psql $DATABASE_URL < backup_*.sql

# 6. Investigate and fix migration
# Edit migration file
# Test locally

# 7. Retry migration
alembic upgrade head
```

### If Application Issues After Migration

```bash
# 1. Enable maintenance mode
# PUT /api/maintenance/enable

# 2. Rollback database
alembic downgrade -1

# 3. Deploy previous application version
git checkout <previous-tag>
# Redeploy

# 4. Verify application health

# 5. Disable maintenance mode
# DELETE /api/maintenance/disable

# 6. Investigate root cause
# Review logs, database state, migration code
```

## Common Issues

### Issue: Connection Refused

**Symptom**: `psycopg2.OperationalError: connection refused`

**Solution**:
```bash
# Check database is running
supabase status  # For Supabase
brew services list  # For local PostgreSQL

# Verify DATABASE_URL in .env
echo $DATABASE_URL

# Start database
supabase start  # For Supabase
brew services start postgresql@15  # For PostgreSQL
```

### Issue: Migration Already Applied

**Symptom**: `alembic.util.exc.CommandError: Target database is not up to date`

**Solution**:
```bash
# Check current status
alembic current

# View history
alembic history

# If database is ahead, stamp it
alembic stamp head
```

### Issue: Autogenerate Not Detecting Changes

**Symptom**: `alembic revision --autogenerate` creates empty migration

**Solution**:
- Ensure models are imported in `alembic/env.py`
- Check database connection is working
- Verify models have changed from current schema
- Create manual migration for triggers, functions, ENUM changes

### Issue: ENUM Type Already Exists

**Symptom**: `DuplicateObject: type "reportstatus" already exists`

**Solution**:
```sql
-- Check existing types
SELECT typname FROM pg_type WHERE typname LIKE '%status';

-- Drop existing type (careful!)
DROP TYPE IF EXISTS reportstatus CASCADE;
DROP TYPE IF EXISTS paymentstatus CASCADE;

-- Re-run migration
alembic upgrade head
```

## Migration Best Practices

1. Always backup before migrations
2. Test migrations on staging first
3. Review autogenerated migrations carefully
4. Include both upgrade and downgrade logic
5. Keep migrations atomic (one logical change)
6. Document breaking changes
7. Schedule migrations during low-traffic periods
8. Monitor application health post-migration
9. Keep migration logs for audit trail
10. Version control all migration files

## Emergency Contacts

- Database Team: [contact info]
- DevOps Team: [contact info]
- On-call Engineer: [contact info]

## Post-Migration Tasks

- [ ] Update migration status in project tracker
- [ ] Document any manual steps taken
- [ ] Update runbook if new issues discovered
- [ ] Share migration results with team
- [ ] Archive migration logs
- [ ] Update database documentation
- [ ] Schedule next migration review

---

**Last Updated**: 2026-01-01  
**Owner**: Backend Team
