# ADR-0004: Logging Infrastructure

## Status
Accepted

## Context

The MVP requires a comprehensive logging system with specific requirements for rotation, retention, structured logging, and environment-specific behavior.

### Requirements (from Spec Section 15)

**Logging Levels:**
- **Debug Mode** (dev/test): Log all events, stack traces, detailed diagnostics
- **Error Mode** (production): Log only errors and critical events

**Log Management:**
- **Directory**: Separate log directory (e.g., `/logs`)
- **Naming**: `app-YYYY-MM-DD-N.log` (date + sequence number starting from 1)
- **Rotation**: Hybrid strategy - rotate at 100MB OR daily (whichever first)
- **Retention**: Configurable via `LOG_RETENTION_DAYS` (default: 30 days)
- **Cleanup**: Automated deletion of logs older than retention period

**Structured Logging:**
- **requestId**: Unique identifier for request tracing
- **userId**: User identifier (when available)
- **timestamp**: ISO 8601 format
- **level**: DEBUG | INFO | WARN | ERROR
- **environment**: dev | test | production

**Events to Log:**
- Authentication (login, logout, failures)
- Payment transactions
- Report generation
- API errors and exceptions
- Database connection issues
- Feature flag evaluations

### Constraints
- **Security**: No sensitive data (passwords, API keys, PII) in logs
- **Performance**: Logging must not significantly impact application performance
- **Correlation**: All logs from a single request must be traceable via requestId
- **Reusability**: Logging infrastructure should work across multiple projects
- **NIST Compliance**: Logging must support Detect & Respond functions (Constitution Section 2)

## Decision

We will implement a **structured logging infrastructure** using industry-standard libraries with custom rotation and retention management.

### 1. Shared Logging Package (`shared/logging`)

Create a framework-agnostic logging library.

**Package Structure:**
```
shared/logging/
├── src/
│   ├── logger.ts               # Main logger interface
│   ├── formatters/
│   │   ├── json.ts             # JSON formatter
│   │   ├── pretty.ts           # Human-readable formatter (dev)
│   │   └── index.ts
│   ├── transports/
│   │   ├── file.ts             # File transport with rotation
│   │   ├── console.ts          # Console transport
│   │   └── index.ts
│   ├── rotation.ts             # Log rotation logic
│   ├── cleanup.ts              # Log retention/cleanup
│   ├── correlation.ts          # Request correlation
│   ├── sanitizer.ts            # Sensitive data sanitization
│   └── index.ts
├── tests/
│   ├── logger.test.ts
│   ├── rotation.test.ts
│   ├── cleanup.test.ts
│   └── sanitizer.test.ts
├── package.json
└── README.md
```

**API Design:**

```typescript
// shared/logging/src/logger.ts
import { ConfigLoader } from '@study-abroad/shared-config';
import winston from 'winston';
import DailyRotateFile from 'winston-daily-rotate-file';
import { sanitizeLogData } from './sanitizer';
import { getCorrelationId } from './correlation';

export enum LogLevel {
  DEBUG = 'debug',
  INFO = 'info',
  WARN = 'warn',
  ERROR = 'error',
}

export interface LogContext {
  requestId?: string;
  userId?: string;
  [key: string]: any;
}

class ApplicationLogger {
  private logger: winston.Logger;
  private config = ConfigLoader.load();

  constructor() {
    this.logger = this.createLogger();
  }

  private createLogger(): winston.Logger {
    const format = winston.format.combine(
      winston.format.timestamp({ format: 'YYYY-MM-DDTHH:mm:ss.SSSZ' }),
      winston.format.errors({ stack: true }),
      winston.format.metadata(),
      this.config.ENVIRONMENT_MODE === 'dev'
        ? winston.format.prettyPrint()
        : winston.format.json()
    );

    const transports: winston.transport[] = [
      new winston.transports.Console({
        level: this.config.LOG_LEVEL,
      }),
    ];

    // File transport with rotation
    if (this.config.LOG_DIR) {
      transports.push(
        new DailyRotateFile({
          filename: `${this.config.LOG_DIR}/app-%DATE%-1.log`,
          datePattern: 'YYYY-MM-DD',
          maxSize: `${this.config.LOG_MAX_SIZE_MB}m`,
          maxFiles: `${this.config.LOG_RETENTION_DAYS}d`,
          level: this.config.LOG_LEVEL,
          format,
        })
      );
    }

    return winston.createLogger({
      level: this.config.LOG_LEVEL,
      format,
      transports,
      defaultMeta: {
        environment: this.config.ENVIRONMENT_MODE,
        service: 'study-abroad',
      },
    });
  }

  private enrichContext(context?: LogContext): LogContext {
    return {
      requestId: context?.requestId || getCorrelationId(),
      userId: context?.userId,
      ...context,
    };
  }

  debug(message: string, context?: LogContext): void {
    const enrichedContext = this.enrichContext(context);
    const sanitized = sanitizeLogData(enrichedContext);
    this.logger.debug(message, sanitized);
  }

  info(message: string, context?: LogContext): void {
    const enrichedContext = this.enrichContext(context);
    const sanitized = sanitizeLogData(enrichedContext);
    this.logger.info(message, sanitized);
  }

  warn(message: string, context?: LogContext): void {
    const enrichedContext = this.enrichContext(context);
    const sanitized = sanitizeLogData(enrichedContext);
    this.logger.warn(message, sanitized);
  }

  error(message: string, error?: Error, context?: LogContext): void {
    const enrichedContext = this.enrichContext(context);
    const sanitized = sanitizeLogData({
      ...enrichedContext,
      error: error?.message,
      stack: error?.stack,
    });
    this.logger.error(message, sanitized);
  }
}

export const logger = new ApplicationLogger();
```

```typescript
// shared/logging/src/correlation.ts
import { AsyncLocalStorage } from 'async_hooks';
import { randomUUID } from 'crypto';

const asyncLocalStorage = new AsyncLocalStorage<Map<string, any>>();

export function withCorrelationId<T>(fn: () => T): T {
  const store = new Map<string, any>();
  store.set('correlationId', randomUUID());
  return asyncLocalStorage.run(store, fn);
}

export function getCorrelationId(): string {
  const store = asyncLocalStorage.getStore();
  return store?.get('correlationId') || randomUUID();
}

export function setUserId(userId: string): void {
  const store = asyncLocalStorage.getStore();
  if (store) {
    store.set('userId', userId);
  }
}

export function getUserId(): string | undefined {
  const store = asyncLocalStorage.getStore();
  return store?.get('userId');
}
```

```typescript
// shared/logging/src/sanitizer.ts
/**
 * Sensitive field patterns to redact
 */
const SENSITIVE_PATTERNS = [
  /password/i,
  /secret/i,
  /token/i,
  /api[_-]?key/i,
  /authorization/i,
  /cookie/i,
  /ssn/i,
  /credit[_-]?card/i,
];

/**
 * Sanitize log data by redacting sensitive fields
 */
export function sanitizeLogData(data: any): any {
  if (typeof data !== 'object' || data === null) {
    return data;
  }

  if (Array.isArray(data)) {
    return data.map(sanitizeLogData);
  }

  const sanitized: any = {};

  for (const [key, value] of Object.entries(data)) {
    if (SENSITIVE_PATTERNS.some(pattern => pattern.test(key))) {
      sanitized[key] = '[REDACTED]';
    } else if (typeof value === 'object' && value !== null) {
      sanitized[key] = sanitizeLogData(value);
    } else {
      sanitized[key] = value;
    }
  }

  return sanitized;
}
```

```typescript
// shared/logging/src/cleanup.ts
import fs from 'fs/promises';
import path from 'path';
import { ConfigLoader } from '@study-abroad/shared-config';

export class LogCleanupService {
  private config = ConfigLoader.load();

  /**
   * Clean up old log files based on retention policy
   */
  async cleanup(): Promise<number> {
    const logDir = this.config.LOG_DIR;
    if (!logDir) return 0;

    const retentionMs = this.config.LOG_RETENTION_DAYS * 24 * 60 * 60 * 1000;
    const cutoffTime = Date.now() - retentionMs;

    const files = await fs.readdir(logDir);
    let deletedCount = 0;

    for (const file of files) {
      if (!file.startsWith('app-') || !file.endsWith('.log')) continue;

      const filePath = path.join(logDir, file);
      const stats = await fs.stat(filePath);

      if (stats.mtimeMs < cutoffTime) {
        await fs.unlink(filePath);
        deletedCount++;
        console.log(`Deleted old log file: ${file}`);
      }
    }

    return deletedCount;
  }

  /**
   * Schedule periodic cleanup (run daily)
   */
  scheduleCleanup(): NodeJS.Timeout {
    const CLEANUP_INTERVAL = 24 * 60 * 60 * 1000; // 24 hours

    return setInterval(async () => {
      try {
        const deleted = await this.cleanup();
        console.log(`Log cleanup completed: ${deleted} files deleted`);
      } catch (error) {
        console.error('Log cleanup failed:', error);
      }
    }, CLEANUP_INTERVAL);
  }
}

export const logCleanup = new LogCleanupService();
```

### 2. Backend Integration (Python)

For Python backend, use `structlog` for structured logging:

```python
# backend/src/logging_config.py
import structlog
import logging
from logging.handlers import TimedRotatingFileHandler, RotatingFileHandler
import os
from datetime import datetime
from config import settings

def configure_logging():
    """Configure structured logging with rotation and retention."""

    # Ensure log directory exists
    os.makedirs(settings.LOG_DIR, exist_ok=True)

    # Create handlers
    handlers = []

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(settings.LOG_LEVEL)
    handlers.append(console_handler)

    # File handler with rotation
    log_filename = os.path.join(
        settings.LOG_DIR,
        f"app-{datetime.now().strftime('%Y-%m-%d')}-1.log"
    )

    # Hybrid rotation: size OR time-based
    file_handler = RotatingFileHandler(
        log_filename,
        maxBytes=settings.LOG_MAX_SIZE_MB * 1024 * 1024,
        backupCount=settings.LOG_RETENTION_DAYS,
    )
    file_handler.setLevel(settings.LOG_LEVEL)
    handlers.append(file_handler)

    # Configure structlog
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.JSONRenderer() if settings.ENVIRONMENT_MODE == "production"
            else structlog.dev.ConsoleRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(
            logging.getLevelName(settings.LOG_LEVEL)
        ),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )

    # Configure root logger
    logging.basicConfig(
        format="%(message)s",
        level=settings.LOG_LEVEL,
        handlers=handlers,
    )

    return structlog.get_logger()

logger = configure_logging()
```

```python
# backend/src/middleware/logging_middleware.py
from fastapi import Request
import structlog
import uuid

logger = structlog.get_logger()

async def logging_middleware(request: Request, call_next):
    """Middleware to add correlation ID and log requests."""

    request_id = str(uuid.uuid4())
    structlog.contextvars.bind_contextvars(
        request_id=request_id,
        environment=settings.ENVIRONMENT_MODE,
    )

    logger.info(
        "request_started",
        method=request.method,
        path=request.url.path,
    )

    try:
        response = await call_next(request)

        logger.info(
            "request_completed",
            method=request.method,
            path=request.url.path,
            status_code=response.status_code,
        )

        return response
    except Exception as e:
        logger.error(
            "request_failed",
            method=request.method,
            path=request.url.path,
            error=str(e),
        )
        raise
```

### 3. Next.js Integration

```typescript
// frontend/src/middleware.ts
import { NextRequest, NextResponse } from 'next/server';
import { logger, withCorrelationId } from '@study-abroad/shared-logging';

export function middleware(request: NextRequest) {
  return withCorrelationId(() => {
    logger.info('Request received', {
      method: request.method,
      path: request.nextUrl.pathname,
    });

    const response = NextResponse.next();

    logger.info('Request completed', {
      method: request.method,
      path: request.nextUrl.pathname,
      status: response.status,
    });

    return response;
  });
}
```

### 4. Usage Examples

**Frontend API Route:**
```typescript
// app/api/reports/route.ts
import { logger } from '@study-abroad/shared-logging';

export async function GET(req: Request) {
  const userId = getUserId(req); // From auth middleware

  logger.info('Fetching reports', { userId });

  try {
    const reports = await db.reports.listByUser(userId);

    logger.info('Reports fetched', {
      userId,
      count: reports.length,
    });

    return Response.json(reports);
  } catch (error) {
    logger.error('Failed to fetch reports', error as Error, { userId });
    throw error;
  }
}
```

**Backend Service:**
```python
# backend/src/api/services/report_service.py
import structlog

logger = structlog.get_logger()

class ReportService:
    async def generate_report(self, user_id: str, subject: str):
        logger.info("report_generation_started", user_id=user_id, subject=subject)

        try:
            report = await self._generate_with_ai(subject)

            logger.info(
                "report_generation_completed",
                user_id=user_id,
                subject=subject,
                report_id=report.report_id,
            )

            return report
        except Exception as e:
            logger.error(
                "report_generation_failed",
                user_id=user_id,
                subject=subject,
                error=str(e),
            )
            raise
```

### 5. Log Cleanup Automation

**Scheduled Cleanup (Backend):**
```python
# backend/src/scheduler.py
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from logging_cleanup import cleanup_old_logs

def start_scheduler():
    scheduler = AsyncIOScheduler()

    # Run log cleanup daily at 2 AM
    scheduler.add_job(
        cleanup_old_logs,
        'cron',
        hour=2,
        minute=0,
    )

    scheduler.start()
```

```python
# backend/src/logging_cleanup.py
import os
import time
from config import settings
from datetime import datetime, timedelta

async def cleanup_old_logs():
    """Delete log files older than retention period."""

    log_dir = settings.LOG_DIR
    retention_days = settings.LOG_RETENTION_DAYS
    cutoff_time = time.time() - (retention_days * 24 * 60 * 60)

    deleted_count = 0

    for filename in os.listdir(log_dir):
        if not filename.startswith('app-') or not filename.endswith('.log'):
            continue

        file_path = os.path.join(log_dir, filename)
        if os.path.getmtime(file_path) < cutoff_time:
            os.remove(file_path)
            deleted_count += 1
            print(f"Deleted old log file: {filename}")

    print(f"Log cleanup completed: {deleted_count} files deleted")
    return deleted_count
```

## Consequences

### Positive
1. **Traceability**: All logs from a single request can be correlated via requestId
2. **Security**: Sensitive data automatically redacted
3. **Performance**: Efficient rotation prevents disk space issues
4. **Compliance**: Structured logs support NIST Detect & Respond functions
5. **Reusability**: Logging package works across all monorepo projects
6. **Debugging**: Debug mode provides detailed diagnostics in dev/test
7. **Production Safety**: Error mode reduces log volume and noise in production
8. **Automated Maintenance**: Log cleanup runs automatically

### Negative
1. **Disk Usage**: File-based logging requires disk space management
2. **No Centralized Aggregation**: Logs are local to each instance (Cloud Run limitation)
3. **Correlation Complexity**: AsyncLocalStorage may have edge cases
4. **Winston Dependency**: Adds winston as a dependency (TypeScript)
5. **Structlog Dependency**: Adds structlog as a dependency (Python)

### Trade-offs Accepted
- **Local Logs**: Accept file-based logging for MVP; future can integrate with Cloud Logging
- **Manual Correlation**: Accept that cross-service correlation requires manual correlation ID propagation
- **No Real-time Monitoring**: Accept batch-based log analysis; future can add Datadog/New Relic

### Mitigation
- Document log file locations and rotation strategy
- Provide utilities for local log viewing and searching
- Plan for Cloud Logging integration in post-MVP
- Monitor disk usage alerts in production

## Compliance

### SpeckitGovernance
- **Traceability**: All logs are structured and queryable
- **Documentation**: `shared/logging/README.md` provides comprehensive usage guidelines
- **Justification**: Addresses AC-13, AC-14, AC-15, AC-16

### SecurityBaselineNIST
- **Detect (DE.AE-3)**: Comprehensive logging of security events (authentication, authorization failures)
- **Detect (DE.CM-1)**: Network and system monitoring through request logs
- **Respond (RS.AN-1)**: Logs support incident analysis with correlation IDs
- **Protect (PR.DS-5)**: Sensitive data redaction prevents data leaks

### RagCitationsIntegrity
- Not directly applicable to logging infrastructure
- Logging supports RAG pipeline by recording AI generation events

## References
- ADR-0001: Environment Configuration System (config dependency)
- Spec: Section 15 (Non-Functional Requirements - Observability)
- Acceptance Criteria: AC-13, AC-14, AC-15, AC-16
- Constitution: Section 2 (Security Framework - NIST CSF Detect/Respond)

## Revision History
- **2025-12-31**: Initial version (Accepted)
