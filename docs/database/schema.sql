-- ============================================================================
-- Study Abroad MVP - Database Schema
-- Version: 1.0.0
-- Created: 2025-12-31
-- Compatible with: PostgreSQL 14+, Supabase PostgreSQL
-- ============================================================================

-- This schema works identically on both local PostgreSQL and Supabase.
-- Row Level Security (RLS) policies are defined separately for Supabase.

-- ============================================================================
-- EXTENSIONS
-- ============================================================================

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- ============================================================================
-- TABLES
-- ============================================================================

-- ----------------------------------------------------------------------------
-- Users Table
-- ----------------------------------------------------------------------------
-- Stores user account information from Clerk authentication
-- Each user has exactly one record mapped to their Clerk userId

CREATE TABLE IF NOT EXISTS users (
    -- Primary Key
    user_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    -- Clerk Integration
    clerk_user_id VARCHAR(255) NOT NULL UNIQUE,

    -- Authentication
    auth_provider VARCHAR(50) NOT NULL CHECK (auth_provider IN ('google', 'apple', 'facebook', 'email')),
    email VARCHAR(255) NOT NULL,

    -- Metadata
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,

    -- Soft Delete
    deleted_at TIMESTAMP WITH TIME ZONE DEFAULT NULL
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_users_clerk_user_id ON users(clerk_user_id);
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_deleted_at ON users(deleted_at);
CREATE INDEX IF NOT EXISTS idx_users_active ON users(user_id, created_at) WHERE deleted_at IS NULL;

-- Comments
COMMENT ON TABLE users IS 'User accounts synced from Clerk authentication';
COMMENT ON COLUMN users.clerk_user_id IS 'Clerk user ID from JWT (stable identifier)';
COMMENT ON COLUMN users.auth_provider IS 'Primary authentication method used';
COMMENT ON COLUMN users.deleted_at IS 'Soft delete timestamp (NULL = active)';

-- ----------------------------------------------------------------------------
-- Reports Table
-- ----------------------------------------------------------------------------
-- Stores generated research reports for users
-- Reports are soft-deleted after 30 days (expiresAt < NOW)

CREATE TABLE IF NOT EXISTS reports (
    -- Primary Key
    report_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    -- Foreign Keys
    user_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,

    -- Report Data
    subject VARCHAR(255) NOT NULL,
    country VARCHAR(2) NOT NULL DEFAULT 'UK' CHECK (country = 'UK'),

    -- Report Content (JSONB for flexible structure)
    content JSONB NOT NULL,
    citations JSONB NOT NULL,

    -- Status
    status VARCHAR(20) NOT NULL DEFAULT 'generating' CHECK (status IN ('generating', 'completed', 'failed')),

    -- Timestamps
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,

    -- Soft Delete
    deleted_at TIMESTAMP WITH TIME ZONE DEFAULT NULL,

    -- Constraints
    CONSTRAINT valid_expires_at CHECK (expires_at > created_at),
    CONSTRAINT valid_content CHECK (jsonb_typeof(content) = 'object'),
    CONSTRAINT valid_citations CHECK (jsonb_typeof(citations) = 'array')
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_reports_user_id ON reports(user_id);
CREATE INDEX IF NOT EXISTS idx_reports_expires_at ON reports(expires_at);
CREATE INDEX IF NOT EXISTS idx_reports_deleted_at ON reports(deleted_at);
CREATE INDEX IF NOT EXISTS idx_reports_status ON reports(status);
CREATE INDEX IF NOT EXISTS idx_reports_created_at ON reports(created_at DESC);

-- Partial Index for Active Reports (most common query)
CREATE INDEX IF NOT EXISTS idx_reports_active ON reports(user_id, created_at DESC)
WHERE deleted_at IS NULL AND status = 'completed';

-- GIN Index for JSONB Content Search (optional, for future features)
CREATE INDEX IF NOT EXISTS idx_reports_content_gin ON reports USING GIN(content);
CREATE INDEX IF NOT EXISTS idx_reports_citations_gin ON reports USING GIN(citations);

-- Comments
COMMENT ON TABLE reports IS 'AI-generated research reports for users';
COMMENT ON COLUMN reports.content IS 'Structured report content (executive_summary, study_options, etc.)';
COMMENT ON COLUMN reports.citations IS 'Array of citation objects with source, url, confidence';
COMMENT ON COLUMN reports.expires_at IS 'Auto-calculated as created_at + 30 days';
COMMENT ON COLUMN reports.deleted_at IS 'Soft delete timestamp (set after expiration)';

-- ----------------------------------------------------------------------------
-- Payments Table
-- ----------------------------------------------------------------------------
-- Stores payment transaction records from Stripe
-- Each report has exactly one successful payment (in production mode)

CREATE TABLE IF NOT EXISTS payments (
    -- Primary Key
    payment_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    -- Foreign Keys
    user_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    report_id UUID REFERENCES reports(report_id) ON DELETE SET NULL,

    -- Stripe Integration
    stripe_payment_intent_id VARCHAR(255) UNIQUE,
    stripe_client_secret VARCHAR(255),

    -- Payment Details
    amount DECIMAL(10, 2) NOT NULL CHECK (amount > 0),
    currency VARCHAR(3) NOT NULL DEFAULT 'GBP' CHECK (currency = 'GBP'),

    -- Status
    status VARCHAR(50) NOT NULL CHECK (status IN (
        'requires_payment_method',
        'requires_confirmation',
        'processing',
        'succeeded',
        'failed',
        'canceled',
        'bypassed'
    )),

    -- Metadata
    bypassed BOOLEAN DEFAULT FALSE NOT NULL,
    failure_reason TEXT,

    -- Timestamps
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    completed_at TIMESTAMP WITH TIME ZONE,

    -- Soft Delete
    deleted_at TIMESTAMP WITH TIME ZONE DEFAULT NULL
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_payments_user_id ON payments(user_id);
CREATE INDEX IF NOT EXISTS idx_payments_report_id ON payments(report_id);
CREATE INDEX IF NOT EXISTS idx_payments_stripe_payment_intent_id ON payments(stripe_payment_intent_id);
CREATE INDEX IF NOT EXISTS idx_payments_status ON payments(status);
CREATE INDEX IF NOT EXISTS idx_payments_created_at ON payments(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_payments_deleted_at ON payments(deleted_at);

-- Comments
COMMENT ON TABLE payments IS 'Payment transactions for report generation';
COMMENT ON COLUMN payments.stripe_payment_intent_id IS 'Stripe PaymentIntent ID (NULL in dev/test modes)';
COMMENT ON COLUMN payments.bypassed IS 'TRUE if payment bypassed in dev/test mode';
COMMENT ON COLUMN payments.status IS 'Payment status from Stripe or bypassed';

-- ============================================================================
-- FUNCTIONS
-- ============================================================================

-- ----------------------------------------------------------------------------
-- Function: update_updated_at_column
-- ----------------------------------------------------------------------------
-- Automatically updates updated_at timestamp on row modification

CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

COMMENT ON FUNCTION update_updated_at_column() IS 'Automatically updates updated_at timestamp';

-- ----------------------------------------------------------------------------
-- Function: set_report_expires_at
-- ----------------------------------------------------------------------------
-- Automatically sets expires_at to created_at + 30 days

CREATE OR REPLACE FUNCTION set_report_expires_at()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.expires_at IS NULL OR NEW.expires_at = NEW.created_at THEN
        NEW.expires_at = NEW.created_at + INTERVAL '30 days';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

COMMENT ON FUNCTION set_report_expires_at() IS 'Sets expires_at to created_at + 30 days if not provided';

-- ============================================================================
-- TRIGGERS
-- ============================================================================

-- Auto-update updated_at on users
CREATE TRIGGER update_users_updated_at
    BEFORE UPDATE ON users
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Auto-update updated_at on reports
CREATE TRIGGER update_reports_updated_at
    BEFORE UPDATE ON reports
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Auto-update updated_at on payments
CREATE TRIGGER update_payments_updated_at
    BEFORE UPDATE ON payments
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Auto-set expires_at on reports
CREATE TRIGGER set_reports_expires_at
    BEFORE INSERT ON reports
    FOR EACH ROW
    EXECUTE FUNCTION set_report_expires_at();

-- ============================================================================
-- ROW LEVEL SECURITY (RLS) - SUPABASE ONLY
-- ============================================================================
-- Note: RLS policies are applied separately via migration scripts
-- See: migrations/supabase/002_enable_rls.sql

-- For local PostgreSQL development, RLS is NOT enabled
-- Application code handles authorization checks

-- ============================================================================
-- INITIAL DATA / SEED (Optional)
-- ============================================================================

-- No seed data required for MVP

-- ============================================================================
-- PERFORMANCE OPTIMIZATION
-- ============================================================================

-- Analyze tables for query planner
ANALYZE users;
ANALYZE reports;
ANALYZE payments;

-- ============================================================================
-- SECURITY NOTES
-- ============================================================================

-- 1. All timestamps use TIMESTAMP WITH TIME ZONE for consistency across regions
-- 2. Soft delete pattern prevents accidental data loss
-- 3. Foreign keys enforce referential integrity
-- 4. CHECK constraints validate data at database level
-- 5. RLS policies (Supabase) enforce row-level access control
-- 6. Indexes optimize common query patterns
-- 7. JSONB validation ensures content/citations are properly structured

-- ============================================================================
-- MIGRATION NOTES
-- ============================================================================

-- This schema is version-controlled and applied via migration runner
-- Changes must be made through new migration files, not direct edits
-- Migration sequence:
--   001_initial_schema.sql       (this file)
--   002_enable_rls.sql           (Supabase only)
--   003_add_audit_log.sql        (future)
