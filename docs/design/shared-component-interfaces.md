## Shared Component Interface Definitions

**Version**: 1.0.0
**Created**: 2025-12-31
**Status**: Design Approved

This document defines the TypeScript/JavaScript interfaces for all shared packages in the monorepo.

---

## Table of Contents

1. [Config Package Interface](#1-config-package-interface)
2. [Feature Flags Package Interface](#2-feature-flags-package-interface)
3. [Database Package Interface](#3-database-package-interface)
4. [Logging Package Interface](#4-logging-package-interface)

---

## 1. Config Package Interface

**Package**: `@study-abroad/shared-config`
**Location**: `/Users/vihang/projects/study-abroad/shared/config`

### 1.1 Configuration Loader

```typescript
/**
 * Configuration loader with validation
 */
export class ConfigLoader {
  /**
   * Load and validate environment configuration
   * @throws {ZodError} If validation fails
   * @returns Validated configuration object
   */
  static load(): EnvironmentConfig;

  /**
   * Get specific configuration value
   * @param key Configuration key
   * @returns Configuration value
   */
  static get<K extends keyof EnvironmentConfig>(key: K): EnvironmentConfig[K];

  /**
   * Check if configuration is loaded
   */
  static isLoaded(): boolean;

  /**
   * Reload configuration (for testing)
   */
  static reload(): void;
}
```

### 1.2 Environment Configuration Type

```typescript
/**
 * Full environment configuration (inferred from Zod schema)
 */
export type EnvironmentConfig = {
  // Environment
  ENVIRONMENT_MODE: 'dev' | 'test' | 'production';
  NODE_ENV: 'development' | 'test' | 'production';

  // Application
  APP_NAME: string;
  APP_VERSION: string;
  NEXT_PUBLIC_APP_URL: string;
  NEXT_PUBLIC_API_URL: string;
  API_URL: string;
  PORT: number;

  // Database
  DATABASE_URL: string;
  SUPABASE_URL?: string;
  SUPABASE_ANON_KEY?: string;
  SUPABASE_SERVICE_ROLE_KEY?: string;
  DATABASE_POOL_MAX: number;
  DATABASE_IDLE_TIMEOUT_MS: number;
  DATABASE_CONNECTION_TIMEOUT_MS: number;

  // Logging
  LOG_LEVEL: 'debug' | 'info' | 'warn' | 'error';
  LOG_DIR: string;
  LOG_MAX_SIZE_MB: number;
  LOG_ROTATION_DAYS: number;
  LOG_RETENTION_DAYS: number;
  LOG_CONSOLE_ENABLED: boolean;
  LOG_PRETTY_PRINT: boolean;

  // Feature Flags
  ENABLE_SUPABASE: boolean;
  ENABLE_PAYMENTS: boolean;
  ENABLE_RATE_LIMITING: boolean;
  ENABLE_OBSERVABILITY: boolean;

  // Clerk Authentication
  NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY: string;
  CLERK_SECRET_KEY: string;
  CLERK_WEBHOOK_SECRET?: string;
  NEXT_PUBLIC_CLERK_SIGN_IN_URL: string;
  NEXT_PUBLIC_CLERK_SIGN_UP_URL: string;
  NEXT_PUBLIC_CLERK_AFTER_SIGN_IN_URL: string;
  NEXT_PUBLIC_CLERK_AFTER_SIGN_UP_URL: string;

  // Stripe Payment
  NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY?: string;
  STRIPE_SECRET_KEY?: string;
  STRIPE_WEBHOOK_SECRET?: string;
  STRIPE_PRICE_ID?: string;
  PAYMENT_AMOUNT: number;
  PAYMENT_CURRENCY: 'GBP';

  // Gemini AI
  GEMINI_API_KEY: string;
  GEMINI_MODEL: string;
  GEMINI_MAX_TOKENS: number;
  GEMINI_TEMPERATURE: number;
  GEMINI_TIMEOUT_MS: number;

  // Rate Limiting
  RATE_LIMIT_MAX: number;
  RATE_LIMIT_WINDOW_SEC: number;
  RATE_LIMIT_REPORTS_PER_DAY: number;
};
```

### 1.3 Usage Example

```typescript
import { ConfigLoader } from '@study-abroad/shared-config';

// Load configuration (throws if invalid)
const config = ConfigLoader.load();

// Get specific value
const apiUrl = ConfigLoader.get('NEXT_PUBLIC_API_URL');

// Use configuration
console.log(`Environment: ${config.ENVIRONMENT_MODE}`);
console.log(`Database: ${config.ENABLE_SUPABASE ? 'Supabase' : 'PostgreSQL'}`);
```

---

## 2. Feature Flags Package Interface

**Package**: `@study-abroad/shared-feature-flags`
**Location**: `/Users/vihang/projects/study-abroad/shared/feature-flags`

### 2.1 Feature Flag Enums

```typescript
/**
 * Available feature flags
 */
export enum Feature {
  SUPABASE = 'ENABLE_SUPABASE',
  PAYMENTS = 'ENABLE_PAYMENTS',
  RATE_LIMITING = 'ENABLE_RATE_LIMITING',
  OBSERVABILITY = 'ENABLE_OBSERVABILITY',
}
```

### 2.2 Feature Flag Evaluator

```typescript
/**
 * Feature flag evaluation service
 */
export class FeatureFlags {
  /**
   * Check if a feature is enabled
   * @param feature Feature flag to check
   * @returns True if feature is enabled
   */
  static isEnabled(feature: Feature): boolean;

  /**
   * Get current environment mode
   * @returns Environment mode
   */
  static getEnvironmentMode(): 'dev' | 'test' | 'production';

  /**
   * Get all feature flag states
   * @returns Object with all feature flags and their states
   */
  static getAllFlags(): Record<Feature, boolean>;

  /**
   * Log feature flag evaluation (for audit trail)
   * @param feature Feature that was evaluated
   * @param enabled Whether it's enabled
   */
  private static logEvaluation(feature: Feature, enabled: boolean): void;
}
```

### 2.3 React Hooks (Frontend Only)

```typescript
/**
 * React hook for feature flag evaluation
 * @param feature Feature flag to check
 * @returns True if feature is enabled
 */
export function useFeatureFlag(feature: Feature): boolean;

/**
 * React hook for environment mode
 * @returns Current environment mode
 */
export function useEnvironmentMode(): 'dev' | 'test' | 'production';

/**
 * React component for conditional rendering based on feature flags
 */
export function FeatureGate(props: {
  feature: Feature;
  enabled?: boolean;
  fallback?: React.ReactNode;
  children: React.ReactNode;
}): React.ReactElement;
```

### 2.4 Usage Example

```typescript
import { FeatureFlags, Feature, useFeatureFlag } from '@study-abroad/shared-feature-flags';

// Server-side
if (FeatureFlags.isEnabled(Feature.PAYMENTS)) {
  await processPayment();
} else {
  logger.info('Payments disabled, bypassing payment flow');
}

// Client-side (React)
function PaymentSection() {
  const paymentsEnabled = useFeatureFlag(Feature.PAYMENTS);

  if (!paymentsEnabled) {
    return <div>Payments disabled (dev/test mode)</div>;
  }

  return <StripePaymentForm />;
}

// Component-based gating
<FeatureGate feature={Feature.PAYMENTS} fallback={<div>Free access</div>}>
  <StripeCheckout />
</FeatureGate>
```

---

## 3. Database Package Interface

**Package**: `@study-abroad/shared-database`
**Location**: `/Users/vihang/projects/study-abroad/shared/database`

### 3.1 Database Adapter Interface

```typescript
/**
 * Query result structure
 */
export interface QueryResult<T = any> {
  rows: T[];
  rowCount: number;
}

/**
 * Transaction interface
 */
export interface Transaction {
  query<T>(sql: string, params?: any[]): Promise<QueryResult<T>>;
  commit(): Promise<void>;
  rollback(): Promise<void>;
}

/**
 * Database adapter interface
 */
export interface DatabaseAdapter {
  /**
   * Execute a query
   * @param sql SQL query
   * @param params Query parameters
   */
  query<T>(sql: string, params?: any[]): Promise<QueryResult<T>>;

  /**
   * Begin a transaction
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

### 3.2 Repository Base Classes

```typescript
/**
 * Base repository class
 */
export abstract class BaseRepository {
  protected db: DatabaseAdapter;

  constructor(db: DatabaseAdapter);

  /**
   * Check if using Supabase (for RLS-specific logic)
   */
  protected isSupabase(): boolean;
}

/**
 * Soft-deletable entity interface
 */
export interface SoftDeletable {
  deletedAt: Date | null;
}

/**
 * Soft delete repository interface
 */
export interface SoftDeleteRepository<T extends SoftDeletable> {
  softDelete(id: string, userId: string): Promise<void>;
  restore(id: string, userId: string): Promise<void>;
  findByIdIncludingDeleted(id: string, userId: string): Promise<T | null>;
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

  async softDelete(id: string, userId: string): Promise<void>;
  async restore(id: string, userId: string): Promise<void>;
  async findByIdIncludingDeleted(id: string, userId: string): Promise<T | null>;
  isDeleted(entity: T): boolean;
  protected whereActive(): string;
}
```

### 3.3 Report Repository Interface

```typescript
/**
 * Report entity
 */
export interface Report extends SoftDeletable {
  reportId: string;
  userId: string;
  subject: string;
  country: string;
  content: any;
  citations: any[];
  status: 'generating' | 'completed' | 'failed';
  createdAt: Date;
  expiresAt: Date;
  updatedAt: Date;
  deletedAt: Date | null;
}

/**
 * Report repository
 */
export class ReportRepository extends SoftDeleteBaseRepository<Report> {
  /**
   * Find report by ID (excludes soft-deleted)
   */
  async findById(reportId: string, userId: string): Promise<Report | null>;

  /**
   * List all active reports for a user
   */
  async listByUser(userId: string, limit?: number, offset?: number): Promise<Report[]>;

  /**
   * Count total reports for a user
   */
  async countByUser(userId: string): Promise<number>;

  /**
   * Create a new report
   */
  async create(data: Omit<Report, 'reportId' | 'createdAt' | 'updatedAt' | 'deletedAt'>): Promise<Report>;

  /**
   * Update report status
   */
  async updateStatus(reportId: string, userId: string, status: Report['status']): Promise<void>;

  /**
   * Update report content and citations
   */
  async updateContent(reportId: string, userId: string, content: any, citations: any[]): Promise<void>;

  /**
   * Soft delete expired reports (background job)
   */
  async softDeleteExpired(): Promise<number>;
}
```

### 3.4 Database Context

```typescript
/**
 * Database context - provides all repositories
 */
export class DatabaseContext {
  public users: UserRepository;
  public reports: ReportRepository;
  public payments: PaymentRepository;

  constructor(adapter?: DatabaseAdapter);

  /**
   * Close all database connections
   */
  async close(): Promise<void>;
}

/**
 * Singleton database context instance
 */
export const db: DatabaseContext;

/**
 * Create database adapter based on feature flags
 */
export function createDatabaseAdapter(): DatabaseAdapter;
```

### 3.5 Usage Example

```typescript
import { db } from '@study-abroad/shared-database';

// Query via repositories
const report = await db.reports.findById(reportId, userId);

// Create report
const newReport = await db.reports.create({
  userId: 'user-123',
  subject: 'Computer Science',
  country: 'UK',
  content: { /* ... */ },
  citations: [ /* ... */ ],
  status: 'generating',
  expiresAt: new Date(Date.now() + 30 * 24 * 60 * 60 * 1000),
});

// List reports with pagination
const reports = await db.reports.listByUser(userId, 50, 0);

// Soft delete
await db.reports.softDelete(reportId, userId);
```

---

## 4. Logging Package Interface

**Package**: `@study-abroad/shared-logging`
**Location**: `/Users/vihang/projects/study-abroad/shared/logging`

### 4.1 Logger Interface

```typescript
/**
 * Log context (metadata attached to log entries)
 */
export interface LogContext {
  [key: string]: any;
}

/**
 * Logger interface
 */
export interface Logger {
  /**
   * Log debug message
   */
  debug(message: string, context?: LogContext): void;

  /**
   * Log info message
   */
  info(message: string, context?: LogContext): void;

  /**
   * Log warning message
   */
  warn(message: string, context?: LogContext): void;

  /**
   * Log error message
   */
  error(message: string, error: Error, context?: LogContext): void;
}
```

### 4.2 Logger Implementation

```typescript
/**
 * Singleton logger instance
 */
export const logger: Logger;

/**
 * Create a child logger with preset context
 * @param context Context to attach to all logs
 */
export function createChildLogger(context: LogContext): Logger;

/**
 * Set user ID for current context (attaches to all logs)
 * @param userId User ID
 */
export function setUserId(userId: string): void;

/**
 * Clear user ID from context
 */
export function clearUserId(): void;

/**
 * Execute function with correlation ID
 * @param fn Function to execute
 */
export function withCorrelationId<T>(fn: () => T): T;

/**
 * Get current correlation ID
 */
export function getCorrelationId(): string | null;

/**
 * Create a new correlation ID
 */
export function createCorrelationId(): string;
```

### 4.3 Sensitive Data Sanitization

```typescript
/**
 * Sanitize sensitive data from objects
 * @param data Data to sanitize
 * @returns Sanitized data (redacted sensitive fields)
 */
export function sanitize(data: any): any;

/**
 * Add custom sensitive field patterns
 * @param patterns Regex patterns to match sensitive fields
 */
export function addSensitivePatterns(patterns: RegExp[]): void;

/**
 * Default sensitive fields (passwords, tokens, keys, etc.)
 */
export const SENSITIVE_FIELDS: string[];
```

### 4.4 Log Cleanup

```typescript
/**
 * Log cleanup service
 */
export class LogCleanup {
  /**
   * Delete logs older than retention period
   * @returns Number of files deleted
   */
  static cleanup(): Promise<number>;

  /**
   * Schedule automatic cleanup (runs daily)
   * @returns Cleanup interval ID
   */
  static scheduleCleanup(): NodeJS.Timeout;

  /**
   * Stop scheduled cleanup
   */
  static stopCleanup(): void;
}
```

### 4.5 Usage Example

```typescript
import {
  logger,
  setUserId,
  withCorrelationId,
  sanitize,
} from '@study-abroad/shared-logging';

// Basic logging
logger.info('User authenticated', { provider: 'google' });

// With user context
setUserId('user-123');
logger.info('Report generated', { reportId: 'report-456' });

// With correlation ID
withCorrelationId(() => {
  logger.info('Request started', { method: 'POST', path: '/api/reports' });
  processRequest();
  logger.info('Request completed');
});

// Error logging
try {
  await generateReport();
} catch (error) {
  logger.error('Report generation failed', error as Error, {
    subject: 'Computer Science',
  });
}

// Sanitize sensitive data
const sanitized = sanitize({
  userId: '123',
  password: 'secret123', // Will be redacted
  apiKey: 'sk_test_123',  // Will be redacted
});
```

---

## Type Exports

All packages export their types for external consumption:

```typescript
// @study-abroad/shared-config
export type { EnvironmentConfig, EnvironmentMode, LogLevel };
export { EnvironmentConfigSchema, EnvironmentPresets };

// @study-abroad/shared-feature-flags
export { Feature, FeatureFlags, useFeatureFlag, FeatureGate };

// @study-abroad/shared-database
export type {
  DatabaseAdapter,
  QueryResult,
  Transaction,
  Report,
  User,
  Payment,
};
export {
  db,
  createDatabaseAdapter,
  ReportRepository,
  UserRepository,
  PaymentRepository,
};

// @study-abroad/shared-logging
export type { Logger, LogContext };
export {
  logger,
  createChildLogger,
  setUserId,
  withCorrelationId,
  sanitize,
  LogCleanup,
};
```

---

## Related Documentation

- [ADR-0001: Environment Configuration System](/Users/vihang/projects/study-abroad/docs/adr/ADR-0001-environment-configuration-system.md)
- [ADR-0002: Feature Flag Mechanism](/Users/vihang/projects/study-abroad/docs/adr/ADR-0002-feature-flag-mechanism.md)
- [ADR-0003: Database Abstraction Layer](/Users/vihang/projects/study-abroad/docs/adr/ADR-0003-database-abstraction-layer.md)
- [ADR-0004: Logging Infrastructure](/Users/vihang/projects/study-abroad/docs/adr/ADR-0004-logging-infrastructure.md)
- [ADR-0006: Shared Component Architecture](/Users/vihang/projects/study-abroad/docs/adr/ADR-0006-shared-component-architecture.md)
