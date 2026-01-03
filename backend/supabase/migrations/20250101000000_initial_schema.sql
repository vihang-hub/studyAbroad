-- ========================================
-- MVP UK Study & Migration Research App
-- Initial Database Schema
-- ========================================

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ========================================
-- ENUMs
-- ========================================

-- Report status lifecycle
CREATE TYPE report_status AS ENUM (
  'pending',      -- Payment received, queued for generation
  'generating',   -- AI is actively generating the report
  'completed',    -- Report successfully generated
  'failed',       -- Generation failed
  'expired'       -- Report expired after 30 days
);

-- Payment status (Stripe integration)
CREATE TYPE payment_status AS ENUM (
  'pending',      -- Payment intent created
  'succeeded',    -- Payment succeeded
  'failed',       -- Payment failed
  'refunded'      -- Payment refunded
);

-- ========================================
-- TABLES
-- ========================================

-- Users table (synced with Clerk)
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  clerk_user_id VARCHAR(255) UNIQUE NOT NULL,
  email VARCHAR(255) NOT NULL,
  first_name VARCHAR(100),
  last_name VARCHAR(100),
  profile_image_url TEXT,
  auth_provider VARCHAR(50) NOT NULL,
  email_verified BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  deleted_at TIMESTAMPTZ DEFAULT NULL
);

-- Reports table (AI-generated research reports)
CREATE TABLE reports (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  query TEXT NOT NULL,
  status report_status DEFAULT 'pending',
  content JSONB DEFAULT NULL,
  error TEXT DEFAULT NULL,
  expires_at TIMESTAMPTZ NOT NULL DEFAULT (NOW() + INTERVAL '30 days'),
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  deleted_at TIMESTAMPTZ DEFAULT NULL
);

-- Payments table (£2.99 per query)
CREATE TABLE payments (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  report_id UUID NOT NULL REFERENCES reports(id) ON DELETE CASCADE,
  stripe_payment_intent_id VARCHAR(255) UNIQUE NOT NULL,
  amount INTEGER NOT NULL, -- In pence (e.g., 299 for £2.99)
  currency VARCHAR(3) DEFAULT 'gbp',
  status payment_status DEFAULT 'pending',
  error_message TEXT DEFAULT NULL,
  refunded_at TIMESTAMPTZ DEFAULT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- ========================================
-- ROW LEVEL SECURITY (RLS) POLICIES
-- ========================================

-- Enable RLS on all tables
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE reports ENABLE ROW LEVEL SECURITY;
ALTER TABLE payments ENABLE ROW LEVEL SECURITY;

-- Users table policies
CREATE POLICY "Users can view their own profile"
  ON users FOR SELECT
  USING (clerk_user_id = current_setting('app.current_user_id', TRUE));

CREATE POLICY "Users can update their own profile"
  ON users FOR UPDATE
  USING (clerk_user_id = current_setting('app.current_user_id', TRUE));

-- Reports table policies
CREATE POLICY "Users can view their own reports"
  ON reports FOR SELECT
  USING (user_id IN (
    SELECT id FROM users WHERE clerk_user_id = current_setting('app.current_user_id', TRUE)
  ));

CREATE POLICY "Users can create reports"
  ON reports FOR INSERT
  WITH CHECK (user_id IN (
    SELECT id FROM users WHERE clerk_user_id = current_setting('app.current_user_id', TRUE)
  ));

CREATE POLICY "Users can soft delete their own reports"
  ON reports FOR UPDATE
  USING (user_id IN (
    SELECT id FROM users WHERE clerk_user_id = current_setting('app.current_user_id', TRUE)
  ));

-- Payments table policies
CREATE POLICY "Users can view their own payments"
  ON payments FOR SELECT
  USING (user_id IN (
    SELECT id FROM users WHERE clerk_user_id = current_setting('app.current_user_id', TRUE)
  ));

CREATE POLICY "Users can create payments"
  ON payments FOR INSERT
  WITH CHECK (user_id IN (
    SELECT id FROM users WHERE clerk_user_id = current_setting('app.current_user_id', TRUE)
  ));

-- ========================================
-- FUNCTIONS
-- ========================================

-- Function to expire old reports (30 days accessible)
CREATE OR REPLACE FUNCTION expire_old_reports()
RETURNS void
LANGUAGE plpgsql
AS $$
BEGIN
  UPDATE reports
  SET status = 'expired',
      updated_at = NOW()
  WHERE status = 'completed'
    AND expires_at <= NOW()
    AND deleted_at IS NULL;
END;
$$;

-- Function to hard delete expired reports (90 days total: 30 accessible + 60 archived)
CREATE OR REPLACE FUNCTION delete_expired_reports()
RETURNS void
LANGUAGE plpgsql
AS $$
BEGIN
  -- Soft delete reports that expired 60 days ago
  UPDATE reports
  SET deleted_at = NOW(),
      updated_at = NOW()
  WHERE status = 'expired'
    AND expires_at <= (NOW() - INTERVAL '60 days')
    AND deleted_at IS NULL;

  -- Hard delete soft-deleted reports after 90 days total
  DELETE FROM reports
  WHERE deleted_at IS NOT NULL
    AND deleted_at <= (NOW() - INTERVAL '30 days');
END;
$$;

-- Function to automatically update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$;

-- ========================================
-- TRIGGERS
-- ========================================

-- Auto-update updated_at on users table
CREATE TRIGGER update_users_updated_at
  BEFORE UPDATE ON users
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at_column();

-- Auto-update updated_at on reports table
CREATE TRIGGER update_reports_updated_at
  BEFORE UPDATE ON reports
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at_column();

-- Auto-update updated_at on payments table
CREATE TRIGGER update_payments_updated_at
  BEFORE UPDATE ON payments
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at_column();

-- ========================================
-- INDEXES
-- ========================================

-- Users table indexes
CREATE INDEX idx_users_clerk_user_id ON users(clerk_user_id);
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_created_at ON users(created_at);
CREATE INDEX idx_users_deleted_at ON users(deleted_at) WHERE deleted_at IS NOT NULL;

-- Reports table indexes
CREATE INDEX idx_reports_user_id ON reports(user_id);
CREATE INDEX idx_reports_status ON reports(status);
CREATE INDEX idx_reports_expires_at ON reports(expires_at);
CREATE INDEX idx_reports_created_at ON reports(created_at);
CREATE INDEX idx_reports_deleted_at ON reports(deleted_at) WHERE deleted_at IS NOT NULL;

-- Payments table indexes
CREATE INDEX idx_payments_user_id ON payments(user_id);
CREATE INDEX idx_payments_report_id ON payments(report_id);
CREATE INDEX idx_payments_stripe_payment_intent_id ON payments(stripe_payment_intent_id);
CREATE INDEX idx_payments_status ON payments(status);
CREATE INDEX idx_payments_created_at ON payments(created_at);

-- ========================================
-- COMMENTS
-- ========================================

COMMENT ON TABLE users IS 'User accounts synced with Clerk authentication';
COMMENT ON TABLE reports IS 'AI-generated research reports (£2.99 per query, 30-day retention)';
COMMENT ON TABLE payments IS 'Stripe payment records for report generation';

COMMENT ON FUNCTION expire_old_reports() IS 'Mark reports as expired after 30 days (run daily via cron)';
COMMENT ON FUNCTION delete_expired_reports() IS 'Soft delete reports after 60 days archived, hard delete after 90 days total (run daily via cron)';
