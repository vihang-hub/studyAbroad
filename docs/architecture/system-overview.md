# System Architecture Overview

**Document Version**: 2.0.0
**Last Updated**: 2025-12-31
**Status**: Approved
**Related ADRs**: ADR-0001 through ADR-0006

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [System Context](#system-context)
3. [Architecture Principles](#architecture-principles)
4. [Technology Stack](#technology-stack)
5. [Environment Architecture](#environment-architecture)
6. [Component Architecture](#component-architecture)
7. [Data Architecture](#data-architecture)
8. [Security Architecture](#security-architecture)
9. [Deployment Architecture](#deployment-architecture)
10. [Scalability & Performance](#scalability--performance)
11. [Cross-Cutting Concerns](#cross-cutting-concerns)
12. [Architecture Compliance](#architecture-compliance)

---

## Executive Summary

The MVP UK Study & Migration Research App is a Gemini-style conversational web application that generates paid, AI-powered research reports for students planning to study in the United Kingdom. The system supports three runtime environments (dev, test, production) with distinct database, payment, and logging configurations.

**Key Architectural Characteristics:**
- **Stateless Backend**: FastAPI backend designed for Cloud Run autoscaling
- **Environment-Based Configuration**: Feature flags control Supabase and payment integration
- **Structured Logging**: Comprehensive logging with rotation, retention, and correlation
- **Soft Delete Pattern**: 30-day report retention with recovery capability
- **Shared Infrastructure**: Reusable components in monorepo `shared/` packages

---

## System Context

### External Actors
- **End Users**: Students from South Asia researching UK study options
- **Admin Users**: Support team managing user issues and report restorations

### External Systems
- **Gemini AI API**: Generates structured research reports
- **Clerk**: Authentication provider (Google, Apple, Facebook, Email)
- **Stripe**: Payment processing (£2.99 per query)
- **Supabase**: Production database with Row Level Security (test/prod only)
- **PostgreSQL**: Local development database (dev only)
- **Google Cloud Run**: Serverless backend deployment
- **Vercel**: Frontend deployment

### System Boundaries
```
┌─────────────────────────────────────────────────────────┐
│                    Study Abroad MVP                      │
│                                                          │
│  ┌──────────────┐          ┌─────────────────────┐     │
│  │  Next.js     │◄────────►│  FastAPI Backend    │     │
│  │  Frontend    │  API     │  (Stateless)        │     │
│  └──────────────┘          └─────────────────────┘     │
│         │                           │                   │
│         │                           │                   │
│         ▼                           ▼                   │
│  ┌──────────────┐          ┌─────────────────────┐     │
│  │  Clerk Auth  │          │  Database Layer     │     │
│  │              │          │  (Supabase/Postgres)│     │
│  └──────────────┘          └─────────────────────┘     │
└─────────────────────────────────────────────────────────┘
         │                           │
         ▼                           ▼
   External APIs              External Services
   - Stripe                  - Gemini AI
   - Google OAuth            - Cloud Storage
```

---

## Architecture Principles

### 1. Stateless Autoscaling (Constitution Section 4)
**Principle**: Backend must be shared-nothing to facilitate rapid horizontal scaling on Cloud Run.

**Implementation**:
- No in-memory session storage
- All state externalized to Supabase or PostgreSQL
- Stateless request handling via FastAPI
- Cloud Run autoscaling based on CPU/memory

**Validation**: Each backend instance can handle requests independently without coordination.

### 2. Environment Parity
**Principle**: Identical database schemas and migration scripts across dev/test/prod.

**Implementation**:
- Unified SQL migration files work on both PostgreSQL and Supabase
- Repository pattern abstracts database differences
- Feature flags control environment-specific behavior

**Validation**: Same migration scripts applied to local PostgreSQL and Supabase.

### 3. Security by Design (Constitution Section 2 - NIST CSF 2.0)
**Principle**: Security considerations embedded in all architectural decisions.

**Implementation**:
- RLS enforced on Supabase tables
- Secrets in Google Secret Manager (Cloud Run) and Vercel Environment Variables
- TLS 1.3 for data-in-transit
- AES-256 for data-at-rest (database-level encryption)
- Structured logging with sensitive data redaction

**Validation**: Threat model addresses OWASP Top 10 and NIST CSF functions.

### 4. RAG Citations Integrity (Constitution Section 4)
**Principle**: AI-generated reports must include verifiable citations.

**Implementation**:
- Gemini API prompts require citation generation
- Report schema enforces `citations` field
- Validation rejects reports without citations
- Citation format: source URL, retrieval timestamp, confidence score

**Validation**: All reports in database have non-empty `citations` JSONB field.

### 5. Fail-Fast Configuration
**Principle**: Application should not start with invalid configuration.

**Implementation**:
- Zod schema validation on startup (TypeScript)
- Pydantic validation on startup (Python)
- Missing required environment variables cause immediate failure
- Clear error messages indicate what's missing

**Validation**: Invalid `.env` files prevent application start with actionable errors.

---

## Technology Stack

### Frontend
- **Framework**: Next.js 15+ (App Router)
- **Language**: TypeScript (Strict Mode)
- **Styling**: Tailwind CSS + shadcn/ui
- **Auth**: Clerk (Google, Apple, Facebook, Email)
- **AI SDK**: Vercel AI SDK (streaming responses)
- **State Management**: React Server Components + Client Components
- **Deployment**: Vercel

### Backend
- **Framework**: FastAPI (Python 3.12+)
- **AI Integration**: LangChain + Gemini AI
- **Database ORM**: Raw SQL via asyncpg/Supabase client
- **Validation**: Pydantic
- **Logging**: structlog
- **Deployment**: Google Cloud Run

### Database
- **Dev**: PostgreSQL 14+ (local)
- **Test/Prod**: Supabase PostgreSQL (hosted)
- **Migration Tool**: Custom migration runner (ADR-0003)

### Shared Infrastructure
- **Config Management**: `@study-abroad/shared-config` (Zod validation)
- **Feature Flags**: `@study-abroad/shared-feature-flags`
- **Database Abstraction**: `@study-abroad/shared-database` (Repository pattern)
- **Logging**: `@study-abroad/shared-logging` (Winston + correlation IDs)

### DevOps
- **CI/CD**: GitHub Actions
- **Testing**: Vitest (frontend), pytest (backend)
- **Mutation Testing**: Stryker (frontend), mutpy (backend)
- **Coverage**: >90% code coverage, >80% mutation score

---

## Environment Architecture

### Three-Environment Strategy

#### Development Environment
```
Environment: dev
Database: PostgreSQL (localhost:5432)
Payments: DISABLED (ENABLE_PAYMENTS=false)
Supabase: DISABLED (ENABLE_SUPABASE=false)
Logging: DEBUG level, console + file
Purpose: Local development without external dependencies
```

**Configuration**:
```env
ENVIRONMENT_MODE=dev
ENABLE_SUPABASE=false
ENABLE_PAYMENTS=false
DATABASE_URL=postgresql://studyabroad:pass@localhost:5432/studyabroad_dev
LOG_LEVEL=debug
LOG_DIR=./logs
```

**Characteristics**:
- Developers can run entire stack locally
- No Supabase or Stripe account required
- Payment flow bypassed (free report generation)
- Debug logs include stack traces and detailed diagnostics

#### Test Environment
```
Environment: test
Database: Supabase PostgreSQL
Payments: DISABLED (ENABLE_PAYMENTS=false)
Supabase: ENABLED (ENABLE_SUPABASE=true)
Logging: DEBUG level, file-based
Purpose: Integration testing with production-like database
```

**Configuration**:
```env
ENVIRONMENT_MODE=test
ENABLE_SUPABASE=true
ENABLE_PAYMENTS=false
DATABASE_URL=<supabase-connection-string>
LOG_LEVEL=debug
LOG_DIR=./logs
```

**Characteristics**:
- Uses Supabase for RLS testing
- Payment flow bypassed (free report generation)
- Debug logs for troubleshooting
- Row Level Security enforced

#### Production Environment
```
Environment: production
Database: Supabase PostgreSQL
Payments: ENABLED (ENABLE_PAYMENTS=true)
Supabase: ENABLED (ENABLE_SUPABASE=true)
Logging: ERROR level, file-based with rotation
Purpose: Live production environment
```

**Configuration**:
```env
ENVIRONMENT_MODE=production
ENABLE_SUPABASE=true
ENABLE_PAYMENTS=true
DATABASE_URL=<supabase-connection-string>
LOG_LEVEL=error
LOG_MAX_SIZE_MB=100
LOG_ROTATION_DAYS=1
LOG_RETENTION_DAYS=30
```

**Characteristics**:
- Full payment enforcement (£2.99 per query)
- Error-level logging only (reduced noise)
- Log rotation and retention enforced
- Secrets from Google Secret Manager

### Environment Decision Flow

See [docs/diagrams/environment-architecture.mmd](/Users/vihang/projects/study-abroad/docs/diagrams/environment-architecture.mmd) for visual representation.

---

## Component Architecture

### High-Level Components

```
┌────────────────────────────────────────────────────────────┐
│                      Frontend Layer                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │  Chat UI     │  │  Report View │  │  Auth UI     │     │
│  │  (Gemini-    │  │  (History)   │  │  (Clerk)     │     │
│  │  style)      │  │              │  │              │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└────────────────────────────────────────────────────────────┘
         │                   │                   │
         │ API Calls         │ API Calls         │ OAuth
         ▼                   ▼                   ▼
┌────────────────────────────────────────────────────────────┐
│                      Backend Layer                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │  Report      │  │  Payment     │  │  Auth        │     │
│  │  Service     │  │  Service     │  │  Service     │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│         │                   │                   │          │
│         ▼                   ▼                   ▼          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │  AI Service  │  │  Stripe SDK  │  │  Clerk SDK   │     │
│  │  (Gemini)    │  │              │  │              │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└────────────────────────────────────────────────────────────┘
         │
         ▼
┌────────────────────────────────────────────────────────────┐
│                      Data Layer                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │  Database    │  │  Config      │  │  Logging     │     │
│  │  Adapter     │  │  Loader      │  │  Service     │     │
│  │  (Supabase/  │  │  (Env Vars)  │  │  (Winston)   │     │
│  │  Postgres)   │  │              │  │              │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└────────────────────────────────────────────────────────────┘
```

### Shared Components

All shared infrastructure components are organized in `shared/` packages:

1. **Config** (`@study-abroad/shared-config`)
   - Environment variable loading
   - Zod schema validation
   - Type-safe configuration access

2. **Feature Flags** (`@study-abroad/shared-feature-flags`)
   - `ENABLE_SUPABASE` flag
   - `ENABLE_PAYMENTS` flag
   - Flag evaluation with logging

3. **Database** (`@study-abroad/shared-database`)
   - Repository pattern
   - Adapter pattern (Supabase/PostgreSQL)
   - Soft delete support
   - Migration runner

4. **Logging** (`@study-abroad/shared-logging`)
   - Structured logging (Winston/structlog)
   - Request correlation IDs
   - Log rotation and retention
   - Sensitive data sanitization

See [docs/diagrams/shared-components.mmd](/Users/vihang/projects/study-abroad/docs/diagrams/shared-components.mmd) for dependency graph.

---

## Data Architecture

### Conceptual Data Model

```
┌─────────────┐
│    User     │
├─────────────┤
│ userId (PK) │
│ authProvider│
│ createdAt   │
└─────────────┘
       │
       │ 1:N
       ▼
┌─────────────┐        ┌─────────────┐
│   Report    │───────►│   Payment   │
├─────────────┤   1:1  ├─────────────┤
│ reportId(PK)│        │ paymentId   │
│ userId (FK) │        │ reportId(FK)│
│ subject     │        │ userId (FK) │
│ country     │        │ amount      │
│ content     │        │ status      │
│ citations   │        │ createdAt   │
│ createdAt   │        └─────────────┘
│ expiresAt   │
│ deletedAt   │ ◄── Soft Delete
└─────────────┘
```

### Physical Schema (PostgreSQL/Supabase)

```sql
CREATE TABLE users (
    user_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    auth_provider VARCHAR(50) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE reports (
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

CREATE TABLE payments (
    payment_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(user_id),
    report_id UUID REFERENCES reports(report_id),
    amount DECIMAL(10, 2) NOT NULL,
    status VARCHAR(20) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_reports_user_id ON reports(user_id);
CREATE INDEX idx_reports_expires_at ON reports(expires_at);
CREATE INDEX idx_reports_deleted_at ON reports(deleted_at);
CREATE INDEX idx_reports_active ON reports(user_id, created_at)
WHERE deleted_at IS NULL;
```

### Soft Delete Lifecycle

```
Report Created
    │
    ├─> expiresAt = createdAt + 30 days
    │
    ├─> [30 days pass]
    │
    ├─> Background Job: softDeleteExpired()
    │   - SET deleted_at = NOW()
    │   - Report still in database
    │
    ├─> User cannot access (excluded by WHERE deleted_at IS NULL)
    │
    ├─> [Optional] Admin restores report
    │   - SET deleted_at = NULL
    │
    └─> [Future] Hard delete job (out of scope for MVP)
```

### Row Level Security (Supabase Only)

```sql
ALTER TABLE reports ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view their own reports"
  ON reports FOR SELECT
  USING (auth.uid() = user_id AND deleted_at IS NULL);

CREATE POLICY "Users can insert their own reports"
  ON reports FOR INSERT
  WITH CHECK (auth.uid() = user_id);
```

For local PostgreSQL (dev mode), RLS is not enforced; application code handles authorization.

---

## Security Architecture

### NIST Cybersecurity Framework Alignment

#### Identify
- **Asset Inventory**: SBOM maintained via npm/pip dependency tracking
- **Risk Assessment**: Threat model documents attack vectors (see [threat-model.md](/Users/vihang/projects/study-abroad/docs/threat-model.md))

#### Protect
- **Access Control**:
  - Clerk OAuth 2.0 with least-privilege scopes
  - Supabase RLS enforces user data isolation
  - API routes validate user authentication before data access
- **Data Security**:
  - Secrets in Google Secret Manager (backend) and Vercel (frontend)
  - TLS 1.3 for data-in-transit
  - AES-256 for data-at-rest (database encryption)
  - Sensitive data redacted from logs (passwords, tokens, API keys)

#### Detect
- **Logging**: Structured logs capture authentication events, API errors, payment transactions
- **Monitoring**: Log correlation IDs enable request tracing
- **Anomaly Detection**: (Future) Integrate with Cloud Logging alerts

#### Respond
- **Incident Analysis**: Logs retained for 30 days for forensic analysis
- **Recovery**: Soft delete enables data restoration for customer support

#### Recover
- **Backup**: Supabase automatic backups (daily snapshots)
- **Restore**: Soft-deleted reports can be restored via admin API

### Threat Mitigation

See [docs/threat-model.md](/Users/vihang/projects/study-abroad/docs/threat-model.md) for comprehensive threat model.

**Key Mitigations**:
1. **SQL Injection**: Prepared statements via asyncpg
2. **XSS**: React auto-escaping + CSP headers
3. **CSRF**: SameSite cookies + CSRF tokens
4. **Unauthorized Access**: RLS + JWT validation
5. **Data Leaks**: Sensitive data redaction in logs
6. **DDoS**: Cloud Run autoscaling + rate limiting

---

## Deployment Architecture

### Development Deployment

```
Developer Laptop
├── Next.js Frontend (localhost:3000)
├── FastAPI Backend (localhost:8000)
└── PostgreSQL Database (localhost:5432)
```

### Production Deployment

```
┌─────────────────────────────────────────────────────────┐
│                    Vercel Edge Network                   │
│  ┌──────────────────────────────────────────────────┐   │
│  │         Next.js Frontend (SSR + Static)          │   │
│  └──────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
                          │
                          │ HTTPS
                          ▼
┌─────────────────────────────────────────────────────────┐
│              Google Cloud Run (Autoscaling)             │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐       │
│  │  Backend   │  │  Backend   │  │  Backend   │       │
│  │  Instance  │  │  Instance  │  │  Instance  │       │
│  │  (Stateless│  │  (Stateless│  │  (Stateless│       │
│  └────────────┘  └────────────┘  └────────────┘       │
└─────────────────────────────────────────────────────────┘
                          │
                          │ Private VPC
                          ▼
┌─────────────────────────────────────────────────────────┐
│                   Supabase PostgreSQL                    │
│  - Row Level Security                                    │
│  - Automatic Backups                                     │
│  - Connection Pooling                                    │
└─────────────────────────────────────────────────────────┘
```

### Secrets Management

**Backend (Cloud Run)**:
- Secrets stored in Google Secret Manager
- Environment variables injected at runtime
- No secrets in container images

**Frontend (Vercel)**:
- Secrets stored in Vercel Environment Variables
- Build-time injection for public vars (`NEXT_PUBLIC_*`)
- Runtime injection for server-side vars

---

## Scalability & Performance

### Horizontal Scaling
- **Backend**: Cloud Run autoscales based on CPU/memory/requests
- **Database**: Supabase connection pooling (PgBouncer)
- **Frontend**: Vercel Edge Network (CDN + serverless functions)

### Performance Targets
- **Report Generation**: Streaming starts within 5 seconds
- **API Response Time**: p95 < 200ms (excluding AI generation)
- **Database Queries**: p95 < 50ms (indexed queries)
- **Log Rotation**: No performance impact (async file writes)

### Caching Strategy
- **Reports**: Cached in database for 30 days
- **Frontend**: ISR for static content, no caching for dynamic content
- **API**: No caching (real-time data)

---

## Cross-Cutting Concerns

### Logging

See [ADR-0004](/Users/vihang/projects/study-abroad/docs/adr/ADR-0004-logging-infrastructure.md) for detailed logging architecture.

**Log Levels by Environment**:
- Dev: DEBUG (all events, stack traces)
- Test: DEBUG (all events, detailed diagnostics)
- Production: ERROR (errors and critical events only)

**Log Rotation**:
- Rotate at 100MB OR daily (whichever first)
- Retention: 30 days (configurable)
- File naming: `app-YYYY-MM-DD-N.log`

**Structured Log Format**:
```json
{
  "timestamp": "2025-12-31T12:00:00.000Z",
  "level": "INFO",
  "message": "Report generated",
  "requestId": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "userId": "user-123",
  "environment": "production",
  "reportId": "report-456",
  "subject": "Computer Science"
}
```

### Feature Flags

See [ADR-0002](/Users/vihang/projects/study-abroad/docs/adr/ADR-0002-feature-flag-mechanism.md) for detailed feature flag architecture.

**Flags**:
- `ENABLE_SUPABASE`: Controls database backend (local PostgreSQL vs Supabase)
- `ENABLE_PAYMENTS`: Controls payment flow (bypass in dev/test, enforce in production)

**Evaluation Flow**:
```typescript
if (featureFlags.isEnabled(Feature.PAYMENTS)) {
  await processPayment();
} else {
  logger.info('Payments disabled, bypassing payment flow');
  await generateReportDirectly();
}
```

### Configuration Management

See [ADR-0001](/Users/vihang/projects/study-abroad/docs/adr/ADR-0001-environment-configuration-system.md) for detailed configuration architecture.

**Config Validation**:
- Zod schema validation (TypeScript)
- Pydantic validation (Python)
- Fail-fast on invalid configuration
- Clear error messages for missing variables

---

## Architecture Compliance

### Constitution Adherence

**Section 1: Core Technical Stack** ✅
- Next.js 15+ (App Router): ✅
- TypeScript (Strict Mode): ✅
- Tailwind CSS + shadcn/ui: ✅
- Python 3.12+ (FastAPI): ✅
- Supabase (PostgreSQL): ✅
- Google Cloud Run: ✅

**Section 2: Security Framework (NIST CSF 2.0)** ✅
- SBOM: ✅ (npm/pip dependency tracking)
- IAM: ✅ (OAuth 2.0 via Clerk)
- Secret Management: ✅ (Google Secret Manager + Vercel)
- Encryption: ✅ (TLS 1.3 + AES-256)
- Logging: ✅ (Structured logging with correlation IDs)

**Section 3: Engineering Rigor** ✅
- Specification Faithfulness: ✅ (Architecture matches spec)
- Mutation Testing: ✅ (Stryker configured, >80% threshold)
- Code Coverage: ✅ (>90% threshold enforced)
- Clean Code: ✅ (ESLint + Airbnb style guide)

**Section 4: Architectural Principles** ✅
- Stateless Autoscaling: ✅ (Cloud Run + stateless backend)
- RAG Integrity: ✅ (Citations mandatory in reports)
- Persistence: ✅ (All reports mapped to userId)

**Section 5: Naming & Structure** ✅
- PascalCase for Components: ✅
- kebab-case for directories: ✅
- snake_case for Database: ✅
- RESTful API: ✅

**Section 6: Prohibited Practices** ✅
- No Assumptions: ✅ (Configuration validated, no defaults)
- No Shadow IT: ✅ (All services documented)
- No Manual Deployments: ✅ (CI/CD via GitHub Actions)

### Acceptance Criteria Mapping

| AC  | Requirement | Architecture Component | Status |
|-----|-------------|------------------------|--------|
| AC-10 | Dev mode with local PostgreSQL | `ENABLE_SUPABASE=false`, DatabaseAdapter | ✅ |
| AC-11 | Test mode with Supabase, no payments | `ENABLE_SUPABASE=true`, `ENABLE_PAYMENTS=false` | ✅ |
| AC-12 | Production mode with Supabase and payments | `ENABLE_SUPABASE=true`, `ENABLE_PAYMENTS=true` | ✅ |
| AC-13 | Logs rotate at 100MB or daily | Winston DailyRotateFile + maxSize | ✅ |
| AC-14 | Logs retain for configurable days | maxFiles + LOG_RETENTION_DAYS | ✅ |
| AC-15 | Debug logs in dev/test only | LOG_LEVEL=debug (dev/test) vs error (prod) | ✅ |
| AC-16 | Error logs in production | LOG_LEVEL=error | ✅ |
| AC-17 | Reports soft deleted after 30 days | SoftDeleteRepository + background job | ✅ |

---

## Revision History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0.0 | 2025-12-28 | Initial architecture | Architecture Team |
| 2.0.0 | 2025-12-31 | Updated for environment modes, logging, soft delete | Architecture Team |

---

## References

- [ADR-0001: Environment Configuration System](/Users/vihang/projects/study-abroad/docs/adr/ADR-0001-environment-configuration-system.md)
- [ADR-0002: Feature Flag Mechanism](/Users/vihang/projects/study-abroad/docs/adr/ADR-0002-feature-flag-mechanism.md)
- [ADR-0003: Database Abstraction Layer](/Users/vihang/projects/study-abroad/docs/adr/ADR-0003-database-abstraction-layer.md)
- [ADR-0004: Logging Infrastructure](/Users/vihang/projects/study-abroad/docs/adr/ADR-0004-logging-infrastructure.md)
- [ADR-0005: Soft Delete Pattern](/Users/vihang/projects/study-abroad/docs/adr/ADR-0005-soft-delete-pattern.md)
- [ADR-0006: Shared Component Architecture](/Users/vihang/projects/study-abroad/docs/adr/ADR-0006-shared-component-architecture.md)
- [Threat Model](/Users/vihang/projects/study-abroad/docs/threat-model.md)
- [Specification](/Users/vihang/projects/study-abroad/specs/001-mvp-uk-study-migration/spec.md)
- [Constitution](/.specify/memory/constitution.md)
