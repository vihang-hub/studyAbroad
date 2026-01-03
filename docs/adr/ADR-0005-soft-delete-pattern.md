# ADR-0005: Soft Delete Pattern

## Status
Accepted

## Context

The MVP requires that reports be retained for 30 days, after which they should be marked as deleted but retained in the database for potential recovery.

### Requirements (from Spec Section 12)
- Reports are stored for 30 days from creation
- After 30 days, reports are **soft deleted** (marked as deleted, data retained)
- Soft deleted reports are not accessible to users
- Soft deleted reports remain in database with `deletedAt` timestamp
- Hard deletion/purging of soft deleted reports is out of scope for MVP

### Business Drivers
- **Data Recovery**: Support potential customer service scenarios where users request report restoration
- **Legal Compliance**: Retain data for audit/dispute resolution
- **Analytics**: Analyze usage patterns even for expired reports
- **Gradual Degradation**: Avoid sudden data loss

### Constraints
- **Performance**: Queries must exclude soft-deleted records efficiently
- **Security**: Soft-deleted data must not be accessible through normal APIs
- **Consistency**: Pattern must work across all entities (reports, payments, etc.)
- **Reusability**: Pattern should be reusable across multiple projects

## Decision

We will implement a **soft delete pattern** using a `deletedAt` nullable timestamp field with repository-level enforcement.

### 1. Database Schema

Add `deletedAt` field to all soft-deletable tables:

```sql
-- Existing tables get a new column
ALTER TABLE reports ADD COLUMN deleted_at TIMESTAMP WITH TIME ZONE DEFAULT NULL;
ALTER TABLE payments ADD COLUMN deleted_at TIMESTAMP WITH TIME ZONE DEFAULT NULL;

-- Index for efficient querying
CREATE INDEX idx_reports_deleted_at ON reports(deleted_at);
CREATE INDEX idx_payments_deleted_at ON payments(deleted_at);

-- Partial index for active records (more efficient)
CREATE INDEX idx_reports_active ON reports(user_id, created_at)
WHERE deleted_at IS NULL;
```

### 2. Shared Soft Delete Interface

Extend the database package (ADR-0003) with soft delete capabilities:

```typescript
// shared/database/src/soft-delete.ts
export interface SoftDeletable {
  deletedAt: Date | null;
}

export interface SoftDeleteRepository<T extends SoftDeletable> {
  /**
   * Soft delete an entity
   */
  softDelete(id: string, userId: string): Promise<void>;

  /**
   * Restore a soft-deleted entity
   */
  restore(id: string, userId: string): Promise<void>;

  /**
   * Find entity including soft-deleted
   */
  findByIdIncludingDeleted(id: string, userId: string): Promise<T | null>;

  /**
   * Check if entity is soft-deleted
   */
  isDeleted(entity: T): boolean;
}

/**
 * Base repository with soft delete support
 */
export abstract class SoftDeleteBaseRepository<T extends SoftDeletable>
  extends BaseRepository
  implements SoftDeleteRepository<T>
{
  protected abstract tableName: string;
  protected abstract idField: string;

  async softDelete(id: string, userId: string): Promise<void> {
    await this.db.query(
      `UPDATE ${this.tableName}
       SET deleted_at = NOW()
       WHERE ${this.idField} = $1
         AND user_id = $2
         AND deleted_at IS NULL`,
      [id, userId]
    );
  }

  async restore(id: string, userId: string): Promise<void> {
    await this.db.query(
      `UPDATE ${this.tableName}
       SET deleted_at = NULL
       WHERE ${this.idField} = $1
         AND user_id = $2
         AND deleted_at IS NOT NULL`,
      [id, userId]
    );
  }

  async findByIdIncludingDeleted(id: string, userId: string): Promise<T | null> {
    const { rows } = await this.db.query<T>(
      `SELECT * FROM ${this.tableName}
       WHERE ${this.idField} = $1
         AND user_id = $2`,
      [id, userId]
    );

    return rows[0] || null;
  }

  isDeleted(entity: T): boolean {
    return entity.deletedAt !== null;
  }

  /**
   * Helper: Add WHERE clause for active records
   */
  protected whereActive(): string {
    return 'deleted_at IS NULL';
  }
}
```

### 3. Report Repository Implementation

Update `ReportRepository` to extend `SoftDeleteBaseRepository`:

```typescript
// shared/database/src/repositories/report.ts
import { SoftDeleteBaseRepository } from '../soft-delete';
import { Report } from '../types';

export class ReportRepository extends SoftDeleteBaseRepository<Report> {
  protected tableName = 'reports';
  protected idField = 'report_id';

  /**
   * Find report by ID (excludes soft-deleted by default)
   */
  async findById(reportId: string, userId: string): Promise<Report | null> {
    const { rows } = await this.db.query<Report>(
      `SELECT * FROM reports
       WHERE report_id = $1
         AND user_id = $2
         AND ${this.whereActive()}`,
      [reportId, userId]
    );

    return rows[0] || null;
  }

  /**
   * List all active reports for a user
   */
  async listByUser(userId: string): Promise<Report[]> {
    const { rows } = await this.db.query<Report>(
      `SELECT * FROM reports
       WHERE user_id = $1
         AND ${this.whereActive()}
       ORDER BY created_at DESC`,
      [userId]
    );

    return rows;
  }

  /**
   * Soft delete expired reports (background job)
   * Returns number of reports soft-deleted
   */
  async softDeleteExpired(): Promise<number> {
    const { rowCount } = await this.db.query(
      `UPDATE reports
       SET deleted_at = NOW()
       WHERE expires_at < NOW()
         AND ${this.whereActive()}`
    );

    return rowCount;
  }

  /**
   * Count soft-deleted reports (for analytics)
   */
  async countDeleted(userId: string): Promise<number> {
    const { rows } = await this.db.query<{ count: string }>(
      `SELECT COUNT(*) as count
       FROM reports
       WHERE user_id = $1
         AND deleted_at IS NOT NULL`,
      [userId]
    );

    return parseInt(rows[0].count);
  }
}
```

### 4. Backend Integration (Python)

```python
# backend/src/database/soft_delete.py
from datetime import datetime
from typing import Protocol, TypeVar, Optional

class SoftDeletable(Protocol):
    deleted_at: Optional[datetime]

T = TypeVar('T', bound=SoftDeletable)

class SoftDeleteRepository:
    """Mixin for repositories with soft delete support."""

    table_name: str
    id_field: str

    async def soft_delete(self, id: str, user_id: str) -> None:
        await self.db.query(
            f"""UPDATE {self.table_name}
                SET deleted_at = NOW()
                WHERE {self.id_field} = $1
                  AND user_id = $2
                  AND deleted_at IS NULL""",
            [id, user_id]
        )

    async def restore(self, id: str, user_id: str) -> None:
        await self.db.query(
            f"""UPDATE {self.table_name}
                SET deleted_at = NULL
                WHERE {self.id_field} = $1
                  AND user_id = $2
                  AND deleted_at IS NOT NULL""",
            [id, user_id]
        )

    async def find_by_id_including_deleted(
        self, id: str, user_id: str
    ) -> Optional[T]:
        result = await self.db.query(
            f"""SELECT * FROM {self.table_name}
                WHERE {self.id_field} = $1
                  AND user_id = $2""",
            [id, user_id]
        )
        return result.rows[0] if result.rows else None

    def is_deleted(self, entity: T) -> bool:
        return entity.deleted_at is not None

    def where_active(self) -> str:
        return "deleted_at IS NULL"
```

```python
# backend/src/database/repositories/report.py
from database.soft_delete import SoftDeleteRepository
from database.repositories.base import BaseRepository

class ReportRepository(BaseRepository, SoftDeleteRepository):
    table_name = "reports"
    id_field = "report_id"

    async def find_by_id(self, report_id: str, user_id: str) -> Optional[Report]:
        result = await self.db.query(
            f"""SELECT * FROM reports
                WHERE report_id = $1
                  AND user_id = $2
                  AND {self.where_active()}""",
            [report_id, user_id]
        )
        return result.rows[0] if result.rows else None

    async def soft_delete_expired(self) -> int:
        result = await self.db.query(
            f"""UPDATE reports
                SET deleted_at = NOW()
                WHERE expires_at < NOW()
                  AND {self.where_active()}"""
        )
        return result.row_count
```

### 5. Background Job for Automatic Soft Deletion

```typescript
// backend/src/jobs/soft-delete-expired-reports.ts
import { db } from '@study-abroad/shared-database';
import { logger } from '@study-abroad/shared-logging';

export async function softDeleteExpiredReports(): Promise<void> {
  logger.info('Starting soft delete job for expired reports');

  try {
    const deletedCount = await db.reports.softDeleteExpired();

    logger.info('Soft delete job completed', {
      deletedCount,
      job: 'soft-delete-expired-reports',
    });
  } catch (error) {
    logger.error('Soft delete job failed', error as Error, {
      job: 'soft-delete-expired-reports',
    });
    throw error;
  }
}
```

```python
# backend/src/scheduler.py
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from jobs.soft_delete_expired_reports import soft_delete_expired_reports

def start_scheduler():
    scheduler = AsyncIOScheduler()

    # Run soft delete job daily at 1 AM
    scheduler.add_job(
        soft_delete_expired_reports,
        'cron',
        hour=1,
        minute=0,
    )

    scheduler.start()
```

### 6. API Endpoints

**Soft Delete Endpoint (Manual):**
```typescript
// app/api/reports/[id]/route.ts
import { db } from '@study-abroad/shared-database';
import { logger } from '@study-abroad/shared-logging';

export async function DELETE(
  req: Request,
  { params }: { params: { id: string } }
) {
  const userId = getUserId(req);

  logger.info('Soft deleting report', {
    reportId: params.id,
    userId,
  });

  await db.reports.softDelete(params.id, userId);

  return Response.json({ success: true });
}
```

**Restore Endpoint (Admin/Support):**
```typescript
// app/api/admin/reports/[id]/restore/route.ts
import { db } from '@study-abroad/shared-database';
import { logger } from '@study-abroad/shared-logging';

export async function POST(
  req: Request,
  { params }: { params: { id: string } }
) {
  const userId = await getAdminUserId(req); // Admin authentication

  logger.info('Restoring soft-deleted report', {
    reportId: params.id,
    adminUserId: userId,
  });

  const { userId: reportUserId } = await req.json();

  await db.reports.restore(params.id, reportUserId);

  return Response.json({ success: true });
}
```

### 7. Testing

```typescript
// shared/database/tests/repositories/report.test.ts
import { describe, it, expect, beforeEach } from 'vitest';
import { ReportRepository } from '../../src/repositories/report';

describe('ReportRepository - Soft Delete', () => {
  let repo: ReportRepository;

  beforeEach(async () => {
    // Setup test database
  });

  it('should soft delete a report', async () => {
    const report = await repo.create({
      userId: 'user-1',
      subject: 'Computer Science',
      country: 'UK',
      content: {},
      citations: [],
      expiresAt: new Date(Date.now() + 30 * 24 * 60 * 60 * 1000),
    });

    await repo.softDelete(report.reportId, 'user-1');

    const found = await repo.findById(report.reportId, 'user-1');
    expect(found).toBeNull(); // Not found in normal query

    const foundIncludingDeleted = await repo.findByIdIncludingDeleted(
      report.reportId,
      'user-1'
    );
    expect(foundIncludingDeleted).not.toBeNull();
    expect(repo.isDeleted(foundIncludingDeleted!)).toBe(true);
  });

  it('should restore a soft-deleted report', async () => {
    const report = await repo.create({
      userId: 'user-1',
      subject: 'Computer Science',
      country: 'UK',
      content: {},
      citations: [],
      expiresAt: new Date(Date.now() + 30 * 24 * 60 * 60 * 1000),
    });

    await repo.softDelete(report.reportId, 'user-1');
    await repo.restore(report.reportId, 'user-1');

    const found = await repo.findById(report.reportId, 'user-1');
    expect(found).not.toBeNull();
    expect(repo.isDeleted(found!)).toBe(false);
  });

  it('should soft delete expired reports', async () => {
    // Create expired report
    const expiredReport = await repo.create({
      userId: 'user-1',
      subject: 'Computer Science',
      country: 'UK',
      content: {},
      citations: [],
      expiresAt: new Date(Date.now() - 1000), // Already expired
    });

    const deletedCount = await repo.softDeleteExpired();
    expect(deletedCount).toBe(1);

    const found = await repo.findById(expiredReport.reportId, 'user-1');
    expect(found).toBeNull();
  });
});
```

## Consequences

### Positive
1. **Data Recovery**: Soft-deleted data can be restored for customer support
2. **Audit Trail**: Deleted data remains for compliance and analytics
3. **Gradual Degradation**: Users don't experience sudden data loss
4. **Performance**: Partial indexes make active record queries efficient
5. **Reusability**: Pattern can be applied to any entity across projects
6. **Simplicity**: Implemented at repository level, transparent to service layer
7. **Consistency**: All repositories use same soft delete pattern

### Negative
1. **Storage Cost**: Soft-deleted data consumes database storage
2. **Query Complexity**: All queries must filter out soft-deleted records
3. **Index Overhead**: Additional indexes required for performance
4. **Accidental Exposure**: Risk of exposing soft-deleted data if filter forgotten
5. **No Hard Delete**: MVP doesn't include purge mechanism

### Trade-offs Accepted
- **Storage vs Recovery**: Accept higher storage costs for data recovery capability
- **Query Complexity**: Accept filtering complexity for consistency and safety
- **No Purge**: Accept indefinite retention for MVP; future can add purge jobs

### Mitigation
- Document soft delete pattern clearly in `shared/database/README.md`
- Provide base repository class to enforce pattern
- Add linting rules to warn about queries without `whereActive()`
- Plan for automated purge jobs in post-MVP
- Monitor database size and set alerts

## Compliance

### SpeckitGovernance
- **Traceability**: Links to spec Section 12 (Data Retention & Caching)
- **Documentation**: Pattern documented in `shared/database/README.md`
- **Justification**: Addresses AC-17 (soft delete after 30 days)

### SecurityBaselineNIST
- **Protect (PR.IP-6)**: Data destruction policy defined (soft delete first)
- **Respond (RS.AN-1)**: Deleted data supports incident analysis
- **Detect (DE.AE-2)**: Deletion events logged for audit trail

### RagCitationsIntegrity
- Not directly applicable to soft delete pattern
- Soft delete supports RAG pipeline by retaining historical report data for analysis

## References
- ADR-0003: Database Abstraction Layer (repository pattern dependency)
- Spec: Section 12 (Data Retention & Caching)
- Acceptance Criteria: AC-17
- Constitution: Section 4 (Architectural Principles)

## Revision History
- **2025-12-31**: Initial version (Accepted)
