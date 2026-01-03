Spec: MVP UK — Study & Migration Research App (Gemini-style)

## 1. Purpose
Build a web application with a Gemini-style conversational interface that allows students—primarily from South Asia (India, Sri Lanka, Pakistan, Bangladesh, Nepal)—to generate a paid, structured research report about studying and working in a destination country.

MVP scope: United Kingdom only.

Each query:
* covers exactly one country and exactly one subject
* generates a structured research report using Gemini APIs
* costs £2.99 per query
* is stored and accessible for 30 days

## 2. Clarifications

### Session 2025-12-31
- Q: Which local database should dev mode use? → A: PostgreSQL locally (already installed and running)
- Q: How should feature flags be configured? → A: Environment variables (.env files per environment)
- Q: What log rotation strategy should be used? → A: Hybrid rotation (100MB OR daily, whichever first); size and duration configurable via env variables; filename format includes date and sequence number starting from 1
- Q: What should happen to reports after 30 days? → A: Soft delete (mark as deleted, keep data for recovery)
- Q: How long should rotated log files be kept? → A: Log retention configurable via env variable in days; default 30 days

## 3. Target Users
* Students planning to study in the UK
* Users researching:
    * cost of education
    * post-study work options
    * job prospects in their chosen field
    * realistic fallback job opportunities if employment in-field is not available

## 4. Definitions
| Term | Definition |
|------|------------|
| Query | A single request consisting of one destination country + one subject |
| Subject | Intended field of study (e.g. Computer Science, Nursing, Business) |
| Report | AI-generated structured output containing mandatory sections |
| Conversation | A single query + its generated report |
| Retention Period | 30 days from report generation |
| Environment Mode | Application runtime mode: dev, test, or production |

## 5. MVP Scope

### In Scope
  * UK as the only destination country
  * Gemini-style chat UI (single primary conversational surface)
  * Authentication via Clerk (see Section 9 for provider details)
  * Payment per query (see section 9 for details )
  * AI-generated research report
  * Report storage and retrieval for 30 days
  * Local development mode with PostgreSQL database
  * Environment-based configuration (dev, test, production)
  * Feature flags for Supabase and payments

### Out of Scope (Explicit)
* Multiple countries per query
* Multiple subjects per query
* Scholarship matching
* Visa application assistance
* Legal advice
* Mobile native apps
* Offline access

## 6. Environment Configuration

The MVP must support three runtime environments with distinct configurations:

### Development Mode (dev)
* **Database**: PostgreSQL running locally (already installed)
* **Payment**: Disabled (feature flag: `ENABLE_PAYMENTS=false`)
* **Supabase**: Disabled (feature flag: `ENABLE_SUPABASE=false`)
* **Logging Level**: Debug mode
* **Purpose**: Local development and testing without external dependencies

### Test Mode (test)
* **Database**: Supabase PostgreSQL
* **Payment**: Disabled (feature flag: `ENABLE_PAYMENTS=false`)
* **Supabase**: Enabled (feature flag: `ENABLE_SUPABASE=true`)
* **Logging Level**: Debug mode
* **Purpose**: Integration testing with production-like database

### Production Mode (production)
* **Database**: Supabase PostgreSQL
* **Payment**: Enabled (feature flag: `ENABLE_PAYMENTS=true`)
* **Supabase**: Enabled (feature flag: `ENABLE_SUPABASE=true`)
* **Logging Level**: Error mode
* **Purpose**: Live production environment

### Feature Flag Configuration
* All feature flags controlled via environment variables (.env files)
* Required environment variables:
    * `ENVIRONMENT_MODE`: dev | test | production
    * `ENABLE_SUPABASE`: true | false
    * `ENABLE_PAYMENTS`: true | false
    * `LOG_LEVEL`: debug | error
    * `LOG_MAX_SIZE_MB`: integer (default: 100)
    * `LOG_ROTATION_DAYS`: integer (default: 1)
    * `LOG_RETENTION_DAYS`: integer (default: 30)
    * `DATABASE_URL`: connection string (local PostgreSQL or Supabase)

### Local PostgreSQL Requirements
  * **PostgreSQL 14+** must be installed and running on developer machines
  * Database schema must match Supabase schema exactly (environment parity)
  * Migration scripts must work identically on local and Supabase databases
  * Recommended: Use Homebrew (`brew install postgresql@14`) or Docker (`postgres:14-alpine`)


## 7. UI / UX Requirements

### UI Style
* Visual and interaction pattern inspired by gemini.google.com
* Not pixel-perfect, but must include:
    * Central input box
    * Conversational layout
    * Streaming response rendering
    * Sidebar/history of past conversations
    * Ability to reopen past reports

### UX Constraints
* Each query creates one conversation
* Conversations are immutable once generated
* Reopening a report does not trigger a new AI call

## 8. Query Constraints
1. User must provide:
    * Subject (required)
2. Destination country:
    * Fixed to UK in MVP
3. System must reject:
    * Multiple countries
    * Multiple subjects
4. If user attempts a non-UK destination:
    * Show a clear message: "This MVP currently supports the UK only."

## 9. Authentication Requirements
  * Users must authenticate before submitting a paid query
  * **Authentication Provider**: Clerk (supporting multiple OAuth providers)
  * Supported login methods:
      * Google OAuth
      * Apple
      * Facebook
      * Email (magic link or password via Clerk)
  * System must assign a stable internal userId (Clerk user ID)
  * All reports must be associated with userId
  * Implementation details documented in ADR-0007

## 10. Pricing & Payments
* Default Price per query: £2.99 (GBP). 
* Price is a variable stored in env file
* Payment must succeed before report generation
* If payment fails or is cancelled:
    * No report is generated
    * No data is stored
* One successful payment → one report
* **Feature Flag Behavior**:
    * When `ENABLE_PAYMENTS=false` (dev/test modes): Skip payment flow, generate reports immediately
    * When `ENABLE_PAYMENTS=true` (production mode): Enforce payment before generation

## 11. Report Generation

### AI Behavior
  * Backend calls Gemini APIs
  * Responses are streamed to the frontend
  * Prompt must be primed for the UK
  * **Hallucination Prevention**:
      * All factual claims (statistics, dates, costs, regulations) must be sourced from grounded retrieval context
      * AI responses must include inline citations for verifiable claims
      * If data is unavailable in context, AI must explicitly state "Information not available" rather than generating unverified claims
      * Temperature set to 0.3 for factual consistency


### Mandatory Report Sections
Every report must contain all of the following sections:
1. Executive Summary (5–10 bullets)
2. Study Options in the UK
3. Estimated Cost of Studying
    * Tuition ranges
    * Living costs
4. Visa & Immigration Overview
    * High-level, non-legal
5. Post-Study Work Options
6. Job Prospects in the Chosen Subject
7. Fallback Job Prospects (Out-of-Field)
8. Risks & Reality Check
9. 30 / 60 / 90-Day Action Plan
10. Sources & Citations

### Citation Rules
  * Factual claims must include citations
  * **Citation Schema** (JSONB format):
      ```json
      {
        "url": "https://example.com/source",
        "title": "Source Title",
        "accessedDate": "2025-01-03",
        "relevantExcerpt": "Direct quote or summary from source",
        "credibilityScore": "high|medium|low (optional)"
      }
      ```
  * Minimum 1 citation per report (enforced by validation)
  * If data is uncertain, the report must state uncertainty clearly with reason
  * No uncited confident claims are allowed (validation rejects reports without citations)

## 12. Data Retention & Caching
  * Reports are stored for 30 days
  * Within 30 days:
      * Reopening a report does not trigger AI regeneration
  * After 30 days (soft delete):
      * Reports are **soft deleted**: marked as deleted but data retained for recovery
      * Soft deleted reports are not accessible to users
      * Soft deleted reports remain in database with `deletedAt` timestamp
  * After 90 days (hard delete):
      * Soft deleted reports (deletedAt > 90 days ago) are **permanently deleted**
      * Hard deletion performed by weekly cron job
      * Irreversible data removal for GDPR compliance

## 13. Data Model (Conceptual)

### Entities

**User**
* userId
* authProvider
* createdAt

 **Report**
  * reportId
  * userId
  * subject
  * country = UK
  * content (JSONB - structured 10 sections)
  * citations (JSONB array - min 1 citation with url, title, accessedDate, relevantExcerpt)
  * createdAt
  * expiresAt
  * deletedAt (nullable; set when report soft deleted after 30 days)

**Payment**
* paymentId
* userId
* amount (configurable)
* status
* createdAt
* reportId

## 14. API Surface (High-Level)
| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | /reports | Create paid query and start generation |
| GET | /reports | List user's reports (last 30 days, excluding soft deleted) |
| GET | /reports/{id} | Retrieve stored report (reject if soft deleted) |
| DELETE | /reports/{id} | (Optional MVP) Early deletion |

## 15. Non-Functional Requirements

### Security
* No secrets in frontend code
* Secrets stored in secret managers
* HTTPS/TLS enforced
* Users can only access their own reports

### Performance
* Streaming response must begin within defined SLA (e.g. ≤5s)
* Graceful failure handling for AI or payment errors

### Observability

#### Logging Levels
* **Debug Mode** (dev/test environments):
    * Log all events: authentication, payments, report generation, errors, request/response details
    * Include stack traces and detailed diagnostic information
    * Log level: DEBUG
* **Error Mode** (production environment):
    * Log only errors and critical events
    * Exclude sensitive user data from logs
    * Log level: ERROR

#### Log Management
* **Log Directory**: Separate directory for all application logs (e.g., `/logs` or `/var/log/app`)
* **Log File Naming**: `app-YYYY-MM-DD-N.log` where:
    * `YYYY-MM-DD`: Date of log creation
    * `N`: Rotation sequence number starting from 1 (e.g., `app-2025-12-31-1.log`, `app-2025-12-31-2.log`)
* **Log Rotation Strategy** (hybrid):
    * Rotate when log file reaches `LOG_MAX_SIZE_MB` (default: 100MB)
    * OR rotate when day ends (UTC timezone)
    * Whichever condition occurs first
    * Size and duration thresholds configurable via environment variables
* **Log Retention**:
    * Configurable via `LOG_RETENTION_DAYS` environment variable
    * Default: 30 days
    * Automated cleanup of logs older than retention period
* **Log Correlation**:
    * All log entries must include:
        * `requestId`: Unique identifier for request tracing
        * `userId`: User identifier (when available)
        * `timestamp`: ISO 8601 format
        * `level`: DEBUG | INFO | WARN | ERROR
        * `environment`: dev | test | production

#### Events to Log
* Authentication events (login, logout, failures)
* Payment transactions (initiated, succeeded, failed)
* Report generation (started, completed, errors)
* API errors and exceptions
* Database connection issues
* Feature flag evaluations (when flags change behavior)

## 16. Acceptance Criteria (Must Pass)
1. User can authenticate using all supported methods
2. User is charged £2.99 exactly once per query (production mode only; see Section 10)
3. Failed payment results in no report (see Section 10)
4. Successful payment produces a streamed report
5. Reports are accessible for 30 days
6. Reports cannot be accessed by other users
7. All mandatory report sections are present
8. All factual claims include citations
9. UK-only constraint is enforced
10. Application runs in dev mode with local PostgreSQL and no payments
11. Application runs in test mode with Supabase and no payments
12. Application runs in production mode with Supabase and payments
13. Logs rotate at 100MB or daily (whichever first)
14. Logs retain for configurable days (default 30)
15. Debug logs appear in dev/test modes only
16. Error logs appear in production mode
17. Reports are soft deleted after 30 days (deletedAt set, data retained)

## 17. Explicit Non-Goals
* This system does not provide legal advice
* This system does not guarantee employment
* This system does not replace official government guidance
* Log aggregation service integration (file-based logging only)
