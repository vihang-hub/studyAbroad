# ADR-0003: Database Abstraction Layer

## Status
Accepted

## Context

The MVP must support two different database backends depending on the environment:
- **Development**: Local PostgreSQL (localhost)
- **Test/Production**: Supabase PostgreSQL

Both databases must have identical schemas to ensure environment parity. The application code should work transparently regardless of which database is active.

### Requirements (from Spec Section 6)
- **Dev Mode**: PostgreSQL running locally (already installed)
- **Test/Prod Mode**: Supabase PostgreSQL
- **Schema Parity**: Identical schema across all environments
- **Migration Parity**: Same migration scripts work on both databases
- **Feature Flag Integration**: Use `ENABLE_SUPABASE` flag to determine backend

### Constraints
- **Stateless Design**: Backend must be stateless for Cloud Run autoscaling (Constitution Section 4)
- **RLS Enforcement**: Supabase Row Level Security must be respected
- **Connection Pooling**: Support for connection pooling in production
- **Type Safety**: Database queries must be type-safe
- **Reusability**: Abstraction layer should work across multiple projects

### Challenges
- Supabase client has additional features (RLS, auth integration) not in vanilla PostgreSQL
- Local PostgreSQL requires manual connection management
- Different connection string formats
- RLS policies must be tested locally without Supabase-specific features

## Decision

We will implement a **Repository Pattern with Database Adapter** architecture that abstracts database operations behind a common interface.

### 1. Shared Database Package (`shared/database`)

Create a framework-agnostic database abstraction layer.

**Package Structure:**
```
shared/database/
├── src/
│   ├── adapters/
│   │   ├── base.ts              # Base adapter interface
│   │   ├── supabase.ts          # Supabase adapter
│   │   ├── postgres.ts          # PostgreSQL adapter
│   │   └── index.ts
│   ├── repositories/
│   │   ├── base.ts              # Base repository
│   │   ├── user.ts              # User repository
│   │   ├── report.ts            # Report repository
│   │   ├── payment.ts           # Payment repository
│   │   └── index.ts
│   ├── migrations/
│   │   ├── runner.ts            # Migration runner
│   │   └── index.ts
│   ├── types.ts                 # Shared types
│   └── index.ts
├── migrations/                   # SQL migration files
│   ├── 001_initial_schema.sql
│   ├── 002_add_soft_delete.sql
│   └── README.md
├── tests/
│   ├── adapters/
│   ├── repositories/
│   └── setup.ts
├── package.json
└── README.md
```

**API Design:**

```typescript
// shared/database/src/adapters/base.ts
export interface QueryResult<T = any> {
  rows: T[];
  rowCount: number;
}

export interface Transaction {
  query<T>(sql: string, params?: any[]): Promise<QueryResult<T>>;
  commit(): Promise<void>;
  rollback(): Promise<void>;
}

export interface DatabaseAdapter {
  /**
   * Execute a query
   */
  query<T>(sql: string, params?: any[]): Promise<QueryResult<T>>;

  /**
   * Start a transaction
   */
  beginTransaction(): Promise<Transaction>;

  /**
   * Close all connections
   */
  close(): Promise<void>;

  /**
   * Get adapter type
   */
  getType(): 'supabase' | 'postgres';
}
```

```typescript
// shared/database/src/adapters/postgres.ts
import { Pool, PoolConfig } from 'pg';
import { DatabaseAdapter, QueryResult, Transaction } from './base';

export class PostgresAdapter implements DatabaseAdapter {
  private pool: Pool;

  constructor(connectionString: string) {
    this.pool = new Pool({
      connectionString,
      max: 20,
      idleTimeoutMillis: 30000,
      connectionTimeoutMillis: 2000,
    });
  }

  async query<T>(sql: string, params?: any[]): Promise<QueryResult<T>> {
    const result = await this.pool.query(sql, params);
    return {
      rows: result.rows as T[],
      rowCount: result.rowCount || 0,
    };
  }

  async beginTransaction(): Promise<Transaction> {
    const client = await this.pool.connect();
    await client.query('BEGIN');

    return {
      query: async <T>(sql: string, params?: any[]) => {
        const result = await client.query(sql, params);
        return {
          rows: result.rows as T[],
          rowCount: result.rowCount || 0,
        };
      },
      commit: async () => {
        await client.query('COMMIT');
        client.release();
      },
      rollback: async () => {
        await client.query('ROLLBACK');
        client.release();
      },
    };
  }

  async close(): Promise<void> {
    await this.pool.end();
  }

  getType(): 'postgres' {
    return 'postgres';
  }
}
```

```typescript
// shared/database/src/adapters/supabase.ts
import { createClient, SupabaseClient } from '@supabase/supabase-js';
import { DatabaseAdapter, QueryResult, Transaction } from './base';

export class SupabaseAdapter implements DatabaseAdapter {
  private client: SupabaseClient;

  constructor(url: string, anonKey: string) {
    this.client = createClient(url, anonKey);
  }

  async query<T>(sql: string, params?: any[]): Promise<QueryResult<T>> {
    // Supabase doesn't support raw SQL in the same way
    // We'll use the RPC mechanism for custom queries
    const { data, error } = await this.client.rpc('exec_sql', {
      query: sql,
      params: params || [],
    });

    if (error) throw error;

    return {
      rows: (data as T[]) || [],
      rowCount: data?.length || 0,
    };
  }

  async beginTransaction(): Promise<Transaction> {
    // Supabase doesn't support manual transactions in the client
    // Transactions are handled at the RPC/Edge Function level
    throw new Error('Transactions not supported in Supabase adapter. Use Edge Functions.');
  }

  async close(): Promise<void> {
    // Supabase client doesn't require explicit closing
  }

  getType(): 'supabase' {
    return 'supabase';
  }

  /**
   * Get the underlying Supabase client for RLS-aware queries
   */
  getClient(): SupabaseClient {
    return this.client;
  }
}
```

```typescript
// shared/database/src/repositories/base.ts
import { DatabaseAdapter } from '../adapters/base';

export abstract class BaseRepository {
  protected db: DatabaseAdapter;

  constructor(db: DatabaseAdapter) {
    this.db = db;
  }

  /**
   * Check if using Supabase (for RLS-specific logic)
   */
  protected isSupabase(): boolean {
    return this.db.getType() === 'supabase';
  }
}
```

```typescript
// shared/database/src/repositories/report.ts
import { BaseRepository } from './base';
import { Report } from '../types';

export class ReportRepository extends BaseRepository {
  /**
   * Find report by ID (with soft delete filtering)
   */
  async findById(reportId: string, userId: string): Promise<Report | null> {
    const { rows } = await this.db.query<Report>(
      `SELECT * FROM reports
       WHERE report_id = $1
         AND user_id = $2
         AND deleted_at IS NULL`,
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
         AND deleted_at IS NULL
       ORDER BY created_at DESC`,
      [userId]
    );

    return rows;
  }

  /**
   * Create a new report
   */
  async create(data: Omit<Report, 'reportId' | 'createdAt'>): Promise<Report> {
    const { rows } = await this.db.query<Report>(
      `INSERT INTO reports (user_id, subject, country, content, citations, expires_at)
       VALUES ($1, $2, $3, $4, $5, $6)
       RETURNING *`,
      [
        data.userId,
        data.subject,
        data.country,
        JSON.stringify(data.content),
        JSON.stringify(data.citations),
        data.expiresAt,
      ]
    );

    return rows[0];
  }

  /**
   * Soft delete a report
   */
  async softDelete(reportId: string, userId: string): Promise<void> {
    await this.db.query(
      `UPDATE reports
       SET deleted_at = NOW()
       WHERE report_id = $1
         AND user_id = $2`,
      [reportId, userId]
    );
  }

  /**
   * Mark expired reports as soft deleted (background job)
   */
  async softDeleteExpired(): Promise<number> {
    const { rowCount } = await this.db.query(
      `UPDATE reports
       SET deleted_at = NOW()
       WHERE expires_at < NOW()
         AND deleted_at IS NULL`
    );

    return rowCount;
  }
}
```

```typescript
// shared/database/src/index.ts
import { ConfigLoader } from '@study-abroad/shared-config';
import { featureFlags, Feature } from '@study-abroad/shared-feature-flags';
import { DatabaseAdapter } from './adapters/base';
import { PostgresAdapter } from './adapters/postgres';
import { SupabaseAdapter } from './adapters/supabase';
import { UserRepository } from './repositories/user';
import { ReportRepository } from './repositories/report';
import { PaymentRepository } from './repositories/payment';

/**
 * Database factory - creates the appropriate adapter
 */
export function createDatabaseAdapter(): DatabaseAdapter {
  const config = ConfigLoader.load();

  if (featureFlags.isEnabled(Feature.SUPABASE)) {
    if (!config.SUPABASE_URL || !config.SUPABASE_ANON_KEY) {
      throw new Error('Supabase configuration missing');
    }
    return new SupabaseAdapter(config.SUPABASE_URL, config.SUPABASE_ANON_KEY);
  } else {
    if (!config.DATABASE_URL) {
      throw new Error('DATABASE_URL not configured');
    }
    return new PostgresAdapter(config.DATABASE_URL);
  }
}

/**
 * Database context - provides all repositories
 */
export class DatabaseContext {
  private adapter: DatabaseAdapter;

  public users: UserRepository;
  public reports: ReportRepository;
  public payments: PaymentRepository;

  constructor(adapter?: DatabaseAdapter) {
    this.adapter = adapter || createDatabaseAdapter();

    this.users = new UserRepository(this.adapter);
    this.reports = new ReportRepository(this.adapter);
    this.payments = new PaymentRepository(this.adapter);
  }

  async close(): Promise<void> {
    await this.adapter.close();
  }
}

// Singleton instance
export const db = new DatabaseContext();
```

### 2. Backend Integration (Python)

For Python backend, create a similar abstraction:

```python
# backend/src/database/adapters/base.py
from abc import ABC, abstractmethod
from typing import Any, List, Dict, Optional

class QueryResult:
    def __init__(self, rows: List[Dict[str, Any]], row_count: int):
        self.rows = rows
        self.row_count = row_count

class DatabaseAdapter(ABC):
    @abstractmethod
    async def query(self, sql: str, params: Optional[List[Any]] = None) -> QueryResult:
        pass

    @abstractmethod
    async def close(self) -> None:
        pass

    @abstractmethod
    def get_type(self) -> str:
        pass
```

```python
# backend/src/database/adapters/postgres.py
import asyncpg
from .base import DatabaseAdapter, QueryResult

class PostgresAdapter(DatabaseAdapter):
    def __init__(self, connection_string: str):
        self.connection_string = connection_string
        self.pool: Optional[asyncpg.Pool] = None

    async def _ensure_pool(self):
        if not self.pool:
            self.pool = await asyncpg.create_pool(self.connection_string)

    async def query(self, sql: str, params: Optional[List[Any]] = None) -> QueryResult:
        await self._ensure_pool()
        rows = await self.pool.fetch(sql, *(params or []))
        return QueryResult(
            rows=[dict(row) for row in rows],
            row_count=len(rows)
        )

    async def close(self) -> None:
        if self.pool:
            await self.pool.close()

    def get_type(self) -> str:
        return "postgres"
```

```python
# backend/src/database/__init__.py
from config import settings
from feature_flags import feature_flags, Feature
from .adapters.postgres import PostgresAdapter
from .adapters.supabase import SupabaseAdapter
from .repositories.user import UserRepository
from .repositories.report import ReportRepository
from .repositories.payment import PaymentRepository

def create_database_adapter() -> DatabaseAdapter:
    if feature_flags.is_enabled(Feature.SUPABASE):
        return SupabaseAdapter(settings.SUPABASE_URL, settings.SUPABASE_ANON_KEY)
    else:
        return PostgresAdapter(settings.DATABASE_URL)

class DatabaseContext:
    def __init__(self):
        self.adapter = create_database_adapter()
        self.users = UserRepository(self.adapter)
        self.reports = ReportRepository(self.adapter)
        self.payments = PaymentRepository(self.adapter)

    async def close(self):
        await self.adapter.close()

db = DatabaseContext()
```

### 3. Migration Strategy

**Unified Migration Files:**
```sql
-- migrations/001_initial_schema.sql
-- This SQL works on both PostgreSQL and Supabase

CREATE TABLE IF NOT EXISTS users (
    user_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    auth_provider VARCHAR(50) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS reports (
    report_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(user_id),
    subject VARCHAR(255) NOT NULL,
    country VARCHAR(2) DEFAULT 'UK',
    content JSONB NOT NULL,
    citations JSONB NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
    deleted_at TIMESTAMP WITH TIME ZONE DEFAULT NULL
);

CREATE INDEX idx_reports_user_id ON reports(user_id);
CREATE INDEX idx_reports_expires_at ON reports(expires_at);
CREATE INDEX idx_reports_deleted_at ON reports(deleted_at);

CREATE TABLE IF NOT EXISTS payments (
    payment_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(user_id),
    report_id UUID REFERENCES reports(report_id),
    amount DECIMAL(10, 2) NOT NULL,
    status VARCHAR(20) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

**Migration Runner:**
```typescript
// shared/database/src/migrations/runner.ts
import { DatabaseAdapter } from '../adapters/base';
import fs from 'fs/promises';
import path from 'path';

export class MigrationRunner {
  constructor(private db: DatabaseAdapter) {}

  async runMigrations(migrationsDir: string): Promise<void> {
    // Create migrations table if not exists
    await this.db.query(`
      CREATE TABLE IF NOT EXISTS schema_migrations (
        version INTEGER PRIMARY KEY,
        applied_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
      )
    `);

    // Get applied migrations
    const { rows } = await this.db.query<{ version: number }>(
      'SELECT version FROM schema_migrations ORDER BY version'
    );
    const appliedVersions = new Set(rows.map(r => r.version));

    // Read migration files
    const files = await fs.readdir(migrationsDir);
    const migrations = files
      .filter(f => f.endsWith('.sql'))
      .sort();

    // Apply pending migrations
    for (const file of migrations) {
      const version = parseInt(file.split('_')[0]);
      if (appliedVersions.has(version)) continue;

      const sql = await fs.readFile(path.join(migrationsDir, file), 'utf-8');

      const tx = await this.db.beginTransaction();
      try {
        await tx.query(sql);
        await tx.query('INSERT INTO schema_migrations (version) VALUES ($1)', [version]);
        await tx.commit();
        console.log(`Applied migration: ${file}`);
      } catch (error) {
        await tx.rollback();
        throw error;
      }
    }
  }
}
```

### 4. Row Level Security (RLS) Handling

For Supabase, RLS policies must be defined separately:

```sql
-- migrations/supabase/001_rls_policies.sql
-- This file is ONLY applied to Supabase

ALTER TABLE reports ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view their own reports"
  ON reports FOR SELECT
  USING (auth.uid() = user_id);

CREATE POLICY "Users can insert their own reports"
  ON reports FOR INSERT
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update their own reports"
  ON reports FOR UPDATE
  USING (auth.uid() = user_id);
```

For local PostgreSQL, RLS is not enforced, so application code must handle authorization.

## Consequences

### Positive
1. **Environment Parity**: Same schema and migrations across all environments
2. **Portability**: Easy to switch between local PostgreSQL and Supabase
3. **Type Safety**: Repository pattern provides type-safe database access
4. **Testability**: Easy to mock database adapter in tests
5. **Reusability**: Package works across all monorepo projects
6. **Separation of Concerns**: Business logic separated from database implementation
7. **Migration Safety**: Unified migration files prevent schema drift

### Negative
1. **Complexity**: Additional abstraction layer
2. **Supabase Limitations**: Cannot fully leverage Supabase-specific features (RPC, realtime)
3. **Transaction Limitations**: Supabase doesn't support client-side transactions
4. **Performance**: Extra abstraction may add minimal overhead
5. **Learning Curve**: Developers must understand repository pattern

### Trade-offs Accepted
- **Supabase Feature Loss**: Accept that we cannot use realtime subscriptions or some RPC features
- **Manual RLS**: Local development requires manual authorization checks
- **Transaction Limitation**: Supabase transactions handled via Edge Functions only

### Mitigation
- Comprehensive documentation in `shared/database/README.md`
- Example repositories for common patterns
- Migration guide for existing code
- RLS testing utilities for local development

## Compliance

### SpeckitGovernance
- **Traceability**: Links to spec Section 6 (Environment Configuration) and Section 13 (Data Model)
- **Documentation**: `shared/database/README.md` provides comprehensive usage guidelines
- **Justification**: Addresses AC-10 (dev mode), AC-11 (test mode), AC-12 (production mode)

### SecurityBaselineNIST
- **Protect (PR.AC-4)**: RLS enforced in Supabase, application-level authorization in PostgreSQL
- **Protect (PR.DS-1)**: Prepared statements prevent SQL injection
- **Protect (PR.DS-2)**: Data-at-rest encryption via database-level encryption

### RagCitationsIntegrity
- Not directly applicable to database layer
- Repository pattern supports RAG pipeline by providing structured data access

## References
- ADR-0001: Environment Configuration System (config dependency)
- ADR-0002: Feature Flag Mechanism (feature flag dependency)
- Spec: Section 6 (Environment Configuration), Section 13 (Data Model)
- Acceptance Criteria: AC-10, AC-11, AC-12
- Constitution: Section 4 (Architectural Principles - Stateless Autoscaling)

## Revision History
- **2025-12-31**: Initial version (Accepted)
