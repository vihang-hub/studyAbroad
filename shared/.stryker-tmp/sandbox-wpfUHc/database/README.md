# @study-abroad/shared-database

Database abstraction layer supporting both PostgreSQL and Supabase with repository pattern.

## Features

- Adapter pattern for multiple database backends
- Repository pattern for data access
- Soft delete support
- Migration runner
- Type-safe queries
- Environment-based database selection

## Installation

```bash
npm install @study-abroad/shared-database
```

## Usage

### Database Context (Recommended)

```typescript
import { db } from '@study-abroad/shared-database';

// Query via repositories
const report = await db.reports.findById(reportId, userId);
const reports = await db.reports.listByUser(userId);

// Create
const newReport = await db.reports.create({
  userId: 'user-123',
  subject: 'Computer Science',
  country: 'UK',
  content: { /* ... */ },
  citations: [ /* ... */ ],
  expiresAt: new Date(Date.now() + 30 * 24 * 60 * 60 * 1000),
});

// Soft delete
await db.reports.softDelete(reportId, userId);
```

### Manual Adapter Creation

```typescript
import { createDatabaseAdapter } from '@study-abroad/shared-database';

const adapter = createDatabaseAdapter();
// Returns PostgresAdapter or SupabaseAdapter based on ENABLE_SUPABASE flag
```

### Repository Pattern

All repositories extend `BaseRepository` or `SoftDeleteBaseRepository`:

```typescript
import { SoftDeleteBaseRepository } from '@study-abroad/shared-database';
import { Report } from '@study-abroad/shared-types';

export class ReportRepository extends SoftDeleteBaseRepository<Report> {
  protected tableName = 'reports';
  protected idField = 'report_id';

  async findById(id: string, userId: string): Promise<Report | null> {
    const { rows } = await this.db.query<Report>(
      `SELECT * FROM reports
       WHERE report_id = $1
         AND user_id = $2
         AND ${this.whereActive()}`,  // Excludes soft-deleted
      [id, userId]
    );
    return rows[0] || null;
  }
}
```

### Soft Delete Pattern

```typescript
// Soft delete a report
await db.reports.softDelete(reportId, userId);

// Report is not accessible via normal queries
const report = await db.reports.findById(reportId, userId);
// => null

// But can be accessed with special method
const deletedReport = await db.reports.findByIdIncludingDeleted(reportId, userId);
// => { ...report, deletedAt: '2025-12-31T12:00:00Z' }

// Check if deleted
db.reports.isDeleted(deletedReport); // => true

// Restore (admin/support only)
await db.reports.restore(reportId, userId);
```

### Migrations

Run migrations on application startup:

```typescript
import { MigrationRunner } from '@study-abroad/shared-database';

const runner = new MigrationRunner(db.adapter);
await runner.runMigrations('./migrations');
```

Migration files are standard SQL:

```sql
-- migrations/001_initial_schema.sql
CREATE TABLE IF NOT EXISTS reports (
    report_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL,
    subject VARCHAR(255) NOT NULL,
    content JSONB NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    deleted_at TIMESTAMP WITH TIME ZONE DEFAULT NULL
);

CREATE INDEX idx_reports_user_id ON reports(user_id);
```

### Environment Configuration

Database backend is selected based on `ENABLE_SUPABASE` flag:

```env
# Development (local PostgreSQL)
ENABLE_SUPABASE=false
DATABASE_URL=postgresql://user:pass@localhost:5432/db

# Test/Production (Supabase)
ENABLE_SUPABASE=true
SUPABASE_URL=https://xyz.supabase.co
SUPABASE_ANON_KEY=your-anon-key
```

### Testing

Mock the database adapter in tests:

```typescript
import { DatabaseContext } from '@study-abroad/shared-database';
import { MockDatabaseAdapter } from '@study-abroad/shared-database/tests';

describe('ReportService', () => {
  let db: DatabaseContext;

  beforeEach(() => {
    const mockAdapter = new MockDatabaseAdapter();
    db = new DatabaseContext(mockAdapter);
  });

  it('should create report', async () => {
    const report = await db.reports.create({ /* ... */ });
    expect(report.reportId).toBeDefined();
  });
});
```

## Architecture Decision Records

- [ADR-0003: Database Abstraction Layer](/Users/vihang/projects/study-abroad/docs/adr/ADR-0003-database-abstraction-layer.md)
- [ADR-0005: Soft Delete Pattern](/Users/vihang/projects/study-abroad/docs/adr/ADR-0005-soft-delete-pattern.md)

## License

MIT
