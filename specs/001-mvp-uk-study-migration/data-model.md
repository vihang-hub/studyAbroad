# Data Model: MVP UK Study & Migration App

**Generated**: 2025-12-29
**Database**: Supabase (PostgreSQL 15+)
**Security**: Row Level Security (RLS) enabled on all tables

## Schema Design Principles

1. **Naming Convention**: `snake_case` for tables and columns (Constitution Section 5)
2. **Security**: RLS policies enforce user-scoped access
3. **Soft Deletes**: Reports use status-based expiry (not hard deletes)
4. **Audit Trail**: All tables include `created_at`, critical tables include `updated_at`
5. **Foreign Keys**: Enforce referential integrity with CASCADE/RESTRICT appropriately

---

## Entity Relationship Diagram

```
┌─────────────────┐
│     users       │
└────────┬────────┘
         │ 1
         │
         │ N
┌────────▼────────┐         ┌──────────────────┐
│    reports      │─────────│  report_sections │
└────────┬────────┘ 1     N └──────────────────┘
         │ 1
         │
         │ 1
┌────────▼────────┐
│    payments     │
└─────────────────┘
```

---

## 1. `users` Table

**Purpose**: Store authenticated user information (Clerk integration)

```sql
CREATE TABLE users (
  user_id         UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  clerk_user_id   TEXT NOT NULL UNIQUE,  -- Clerk's unique identifier
  email           TEXT NOT NULL,
  email_verified  BOOLEAN DEFAULT FALSE,
  auth_provider   TEXT NOT NULL,         -- 'google', 'apple', 'facebook', 'email'
  full_name       TEXT,
  avatar_url      TEXT,
  created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  last_login_at   TIMESTAMPTZ
);

-- Indexes
CREATE UNIQUE INDEX idx_users_clerk_user_id ON users(clerk_user_id);
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_created_at ON users(created_at);

-- RLS Policies
ALTER TABLE users ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own profile"
ON users FOR SELECT
USING (auth.uid() = clerk_user_id);

CREATE POLICY "Users can update own profile"
ON users FOR UPDATE
USING (auth.uid() = clerk_user_id)
WITH CHECK (auth.uid() = clerk_user_id);
```

**Fields**:
- `user_id`: Internal UUID (primary key)
- `clerk_user_id`: Clerk's user identifier (maps to JWT `sub` claim)
- `email`: User's email address
- `email_verified`: Whether email is verified (synced from Clerk)
- `auth_provider`: OAuth provider used (`google`, `apple`, `facebook`, `email`)
- `full_name`: User's display name
- `avatar_url`: Profile picture URL (from OAuth or Clerk)
- `created_at`: Account creation timestamp
- `updated_at`: Last profile update
- `last_login_at`: Last successful authentication

**Validation Rules**:
- `email` must be valid email format (enforced by Clerk)
- `auth_provider` must be one of: `google`, `apple`, `facebook`, `email`
- `clerk_user_id` is immutable after creation

---

## 2. `reports` Table

**Purpose**: Store AI-generated study & migration reports

```sql
CREATE TYPE report_status AS ENUM (
  'pending',      -- Payment succeeded, waiting for generation
  'generating',   -- AI generation in progress
  'completed',    -- Successfully generated
  'failed',       -- Generation failed
  'expired'       -- Past 30-day retention period
);

CREATE TABLE reports (
  report_id       UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id         UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
  subject         TEXT NOT NULL,                -- e.g., "Computer Science", "Nursing"
  country         TEXT NOT NULL DEFAULT 'UK',   -- Fixed to 'UK' in MVP
  status          report_status NOT NULL DEFAULT 'pending',
  content         JSONB,                        -- Structured report content
  citations       JSONB,                        -- Array of sources [{title, url}]
  generation_metadata JSONB,                    -- {model, tokens, duration_ms}
  created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  completed_at    TIMESTAMPTZ,                  -- When generation finished
  expires_at      TIMESTAMPTZ NOT NULL DEFAULT (NOW() + INTERVAL '30 days'),
  error_message   TEXT,                         -- If status='failed'
  updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_reports_user_id ON reports(user_id);
CREATE INDEX idx_reports_status ON reports(status);
CREATE INDEX idx_reports_expires_at ON reports(expires_at) WHERE status = 'completed';
CREATE INDEX idx_reports_created_at ON reports(created_at DESC);

-- RLS Policies
ALTER TABLE reports ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own active reports"
ON reports FOR SELECT
USING (
  auth.uid() = (SELECT clerk_user_id FROM users WHERE user_id = reports.user_id)
  AND status IN ('pending', 'generating', 'completed')
  AND expires_at > NOW()
);

CREATE POLICY "Backend can create reports"
ON reports FOR INSERT
WITH CHECK (TRUE);  -- Backend service role bypasses RLS

CREATE POLICY "Backend can update reports"
ON reports FOR UPDATE
USING (TRUE);  -- Backend service role bypasses RLS
```

**Fields**:
- `report_id`: Unique identifier
- `user_id`: Owner of the report (foreign key to `users`)
- `subject`: Field of study (e.g., "Computer Science")
- `country`: Destination country (always "UK" in MVP)
- `status`: Current state of report generation
- `content`: JSON structure containing all 10 mandatory sections (see schema below)
- `citations`: Array of source references
- `generation_metadata`: AI model details (model name, token count, duration)
- `created_at`: When payment succeeded and report was created
- `completed_at`: When AI generation finished
- `expires_at`: 30 days from creation (after this, status → 'expired')
- `error_message`: Details if generation failed
- `updated_at`: Last modification timestamp

**Content Schema** (JSONB):
```json
{
  "executive_summary": ["bullet point 1", "bullet point 2", ...],
  "study_options": "markdown content",
  "estimated_costs": {
    "tuition_ranges": "markdown content",
    "living_costs": "markdown content"
  },
  "visa_immigration": "markdown content",
  "post_study_work": "markdown content",
  "job_prospects_in_field": "markdown content",
  "fallback_job_prospects": "markdown content",
  "risks_reality_check": "markdown content",
  "action_plan": {
    "30_days": "markdown content",
    "60_days": "markdown content",
    "90_days": "markdown content"
  },
  "sources": "markdown content"
}
```

**Citations Schema** (JSONB):
```json
[
  {"title": "UK Gov - Student Visa Guide", "url": "https://..."},
  {"title": "HESA - Graduate Outcomes", "url": "https://..."}
]
```

**Validation Rules**:
- `subject` must be non-empty (max 200 chars)
- `country` must be 'UK' in MVP
- `content` must contain all 10 mandatory sections when status='completed'
- `citations` must be non-empty array when status='completed'
- `expires_at` is auto-set to `created_at + 30 days`

**State Transitions**:
```
pending → generating → completed
        ↘ failed

(any state) → expired (after expires_at)
```

---

## 3. `payments` Table

**Purpose**: Track Stripe payment transactions

```sql
CREATE TYPE payment_status AS ENUM (
  'pending',      -- Checkout session created, waiting for payment
  'succeeded',    -- Payment successful
  'failed',       -- Payment failed or cancelled
  'refunded'      -- Full refund issued
);

CREATE TABLE payments (
  payment_id             UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id                UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
  report_id              UUID REFERENCES reports(report_id) ON DELETE SET NULL,
  stripe_checkout_session_id TEXT NOT NULL UNIQUE,
  stripe_payment_intent_id   TEXT UNIQUE,
  amount_gbp             DECIMAL(10, 2) NOT NULL DEFAULT 2.99,
  currency               TEXT NOT NULL DEFAULT 'GBP',
  status                 payment_status NOT NULL DEFAULT 'pending',
  payment_method         TEXT,          -- 'card', 'apple_pay', 'google_pay'
  stripe_customer_id     TEXT,
  refund_reason          TEXT,          -- If status='refunded'
  created_at             TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  succeeded_at           TIMESTAMPTZ,
  refunded_at            TIMESTAMPTZ,
  metadata               JSONB          -- Additional Stripe webhook data
);

-- Indexes
CREATE INDEX idx_payments_user_id ON payments(user_id);
CREATE INDEX idx_payments_report_id ON payments(report_id);
CREATE INDEX idx_payments_status ON payments(status);
CREATE UNIQUE INDEX idx_payments_stripe_session ON payments(stripe_checkout_session_id);
CREATE INDEX idx_payments_created_at ON payments(created_at DESC);

-- RLS Policies
ALTER TABLE payments ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own payments"
ON payments FOR SELECT
USING (auth.uid() = (SELECT clerk_user_id FROM users WHERE user_id = payments.user_id));

CREATE POLICY "Backend can manage payments"
ON payments FOR ALL
USING (TRUE);  -- Backend service role bypasses RLS
```

**Fields**:
- `payment_id`: Internal unique identifier
- `user_id`: Paying user (foreign key)
- `report_id`: Associated report (nullable until report created)
- `stripe_checkout_session_id`: Stripe Checkout Session ID
- `stripe_payment_intent_id`: Stripe Payment Intent ID (set after payment)
- `amount_gbp`: Payment amount (£2.99 fixed in MVP)
- `currency`: Always 'GBP' in MVP
- `status`: Payment state
- `payment_method`: How user paid (card, Apple Pay, Google Pay)
- `stripe_customer_id`: Stripe customer ID (for future use)
- `refund_reason`: Explanation if refunded (e.g., "Report generation failed")
- `created_at`: When checkout session created
- `succeeded_at`: When payment succeeded
- `refunded_at`: When refund issued
- `metadata`: Additional Stripe data (webhook payload, etc.)

**Validation Rules**:
- `amount_gbp` must be 2.99 (fixed price)
- `currency` must be 'GBP'
- `stripe_checkout_session_id` is immutable and unique
- `report_id` is set only after payment succeeds

**State Transitions**:
```
pending → succeeded
        ↘ failed

succeeded → refunded
```

---

## 4. `report_sections` Table (Optional - Normalized Approach)

**Purpose**: If we want to store report sections separately for analytics

*Note: This is OPTIONAL. For MVP, storing in `reports.content` JSONB is simpler.*

```sql
CREATE TABLE report_sections (
  section_id      UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  report_id       UUID NOT NULL REFERENCES reports(report_id) ON DELETE CASCADE,
  section_name    TEXT NOT NULL,  -- 'executive_summary', 'study_options', etc.
  content         TEXT NOT NULL,
  word_count      INT,
  created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_report_sections_report_id ON report_sections(report_id);
CREATE INDEX idx_report_sections_section_name ON report_sections(section_name);
```

**Recommendation**: Skip this table for MVP. Use JSONB in `reports.content` for simplicity.

---

## Database Functions

### 1. Expire Old Reports (Scheduled Cleanup)

```sql
CREATE OR REPLACE FUNCTION expire_old_reports()
RETURNS TABLE(expired_count INT) AS $$
DECLARE
  affected_rows INT;
BEGIN
  UPDATE reports
  SET status = 'expired', updated_at = NOW()
  WHERE expires_at < NOW()
    AND status IN ('pending', 'generating', 'completed', 'failed');

  GET DIAGNOSTICS affected_rows = ROW_COUNT;
  RETURN QUERY SELECT affected_rows;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;
```

**Usage**: Called by Cloud Scheduler daily
```bash
curl -X POST https://backend-url/cron/expire-reports \
  -H "Authorization: Bearer ${CRON_SECRET}"
```

### 2. Hard Delete Expired Reports (90-day cleanup)

```sql
CREATE OR REPLACE FUNCTION delete_expired_reports()
RETURNS TABLE(deleted_count INT) AS $$
DECLARE
  affected_rows INT;
BEGIN
  DELETE FROM reports
  WHERE status = 'expired'
    AND expires_at < NOW() - INTERVAL '60 days';  -- 30 + 60 = 90 days total

  GET DIAGNOSTICS affected_rows = ROW_COUNT;
  RETURN QUERY SELECT affected_rows;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;
```

---

## Triggers

### Auto-update `updated_at` timestamp

```sql
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_users_updated_at
BEFORE UPDATE ON users
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_reports_updated_at
BEFORE UPDATE ON reports
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();
```

---

## Migrations Strategy

**Tool**: Supabase Migrations (SQL files)

**Initial Migration** (`001_initial_schema.sql`):
1. Create ENUM types (`report_status`, `payment_status`)
2. Create tables in order: `users` → `reports` → `payments`
3. Create indexes
4. Enable RLS and create policies
5. Create functions and triggers

**Rollback Plan**:
- Each migration includes DROP statements for rollback
- Use Supabase CLI: `supabase db reset` (dev), manual rollback (prod)

---

## Data Retention Summary

| Table | Retention Policy | Cleanup Method |
|-------|------------------|----------------|
| `users` | Indefinite (until user deletes account) | User-initiated deletion |
| `reports` | 30 days accessible, 60 days archived (soft delete), hard delete after 90 days | `expire_old_reports()` daily, `delete_expired_reports()` weekly |
| `payments` | Indefinite (audit/compliance) | No auto-deletion |

**GDPR Compliance**:
- Users can request data export (GET /users/me/export)
- Users can request data deletion (DELETE /users/me) → cascades to reports/payments

---

## Performance Considerations

1. **Indexes**: All foreign keys indexed, plus common query patterns (user_id, status, expires_at)
2. **Partitioning**: For future scale, consider partitioning `reports` by created_at (monthly)
3. **JSONB**: Use GIN indexes on `content` if we need to query specific sections
   ```sql
   CREATE INDEX idx_reports_content ON reports USING GIN (content);
   ```
4. **Connection Pooling**: Supabase provides built-in pgBouncer (transaction mode)

---

## Security Summary

| Security Control | Implementation |
|------------------|----------------|
| **Authentication** | Clerk JWT verification → Supabase auth.uid() |
| **Authorization** | RLS policies (user-scoped SELECT) |
| **Encryption at Rest** | AES-256 (Supabase default) |
| **Encryption in Transit** | TLS 1.3 (enforced) |
| **Audit Logging** | created_at, updated_at on all tables |
| **Data Isolation** | RLS prevents cross-user data access |

---

## Next Steps

1. Create migration file: `specs/001-mvp-uk-study-migration/migrations/001_initial_schema.sql`
2. Run migration: `supabase db push`
3. Seed test data for development
4. Document API contracts that interact with this schema
