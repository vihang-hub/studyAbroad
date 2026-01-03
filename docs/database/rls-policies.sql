-- ============================================================================
-- Supabase Row Level Security (RLS) Policies
-- Version: 1.0.0
-- Created: 2025-12-31
-- Compatible with: Supabase PostgreSQL ONLY
-- ============================================================================

-- WARNING: This file should ONLY be applied to Supabase environments
-- Do NOT apply to local PostgreSQL development databases

-- RLS policies enforce data isolation at the database level
-- Users can only access their own data based on auth.uid()

-- ============================================================================
-- ENABLE RLS
-- ============================================================================

ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE reports ENABLE ROW LEVEL SECURITY;
ALTER TABLE payments ENABLE ROW LEVEL SECURITY;

-- ============================================================================
-- USERS TABLE POLICIES
-- ============================================================================

-- Policy: Users can view their own record
CREATE POLICY "users_select_own"
ON users
FOR SELECT
USING (
    clerk_user_id = auth.jwt() ->> 'sub'
    AND deleted_at IS NULL
);

-- Policy: Users can insert their own record (during signup)
CREATE POLICY "users_insert_own"
ON users
FOR INSERT
WITH CHECK (
    clerk_user_id = auth.jwt() ->> 'sub'
);

-- Policy: Users can update their own record
CREATE POLICY "users_update_own"
ON users
FOR UPDATE
USING (
    clerk_user_id = auth.jwt() ->> 'sub'
    AND deleted_at IS NULL
)
WITH CHECK (
    clerk_user_id = auth.jwt() ->> 'sub'
);

-- Policy: Users can soft-delete their own record
CREATE POLICY "users_delete_own"
ON users
FOR UPDATE
USING (
    clerk_user_id = auth.jwt() ->> 'sub'
);

-- ============================================================================
-- REPORTS TABLE POLICIES
-- ============================================================================

-- Policy: Users can view their own active reports
CREATE POLICY "reports_select_own"
ON reports
FOR SELECT
USING (
    user_id IN (
        SELECT user_id FROM users WHERE clerk_user_id = auth.jwt() ->> 'sub'
    )
    AND deleted_at IS NULL
);

-- Policy: Users can insert their own reports
CREATE POLICY "reports_insert_own"
ON reports
FOR INSERT
WITH CHECK (
    user_id IN (
        SELECT user_id FROM users WHERE clerk_user_id = auth.jwt() ->> 'sub'
    )
);

-- Policy: Users can update their own reports (status changes)
CREATE POLICY "reports_update_own"
ON reports
FOR UPDATE
USING (
    user_id IN (
        SELECT user_id FROM users WHERE clerk_user_id = auth.jwt() ->> 'sub'
    )
)
WITH CHECK (
    user_id IN (
        SELECT user_id FROM users WHERE clerk_user_id = auth.jwt() ->> 'sub'
    )
);

-- Policy: Users can soft-delete their own reports
CREATE POLICY "reports_delete_own"
ON reports
FOR UPDATE
USING (
    user_id IN (
        SELECT user_id FROM users WHERE clerk_user_id = auth.jwt() ->> 'sub'
    )
);

-- ============================================================================
-- PAYMENTS TABLE POLICIES
-- ============================================================================

-- Policy: Users can view their own payments
CREATE POLICY "payments_select_own"
ON payments
FOR SELECT
USING (
    user_id IN (
        SELECT user_id FROM users WHERE clerk_user_id = auth.jwt() ->> 'sub'
    )
    AND deleted_at IS NULL
);

-- Policy: Users can insert their own payments
CREATE POLICY "payments_insert_own"
ON payments
FOR INSERT
WITH CHECK (
    user_id IN (
        SELECT user_id FROM users WHERE clerk_user_id = auth.jwt() ->> 'sub'
    )
);

-- Policy: System can update payment status (via service role)
-- Note: This policy allows updates from service role key for webhook processing
CREATE POLICY "payments_update_system"
ON payments
FOR UPDATE
USING (
    auth.role() = 'service_role'
);

-- Policy: Users can view payment status updates
CREATE POLICY "payments_update_own"
ON payments
FOR UPDATE
USING (
    user_id IN (
        SELECT user_id FROM users WHERE clerk_user_id = auth.jwt() ->> 'sub'
    )
)
WITH CHECK (
    user_id IN (
        SELECT user_id FROM users WHERE clerk_user_id = auth.jwt() ->> 'sub'
    )
);

-- ============================================================================
-- ADMIN POLICIES (Future - Out of Scope for MVP)
-- ============================================================================

-- Admin users would need separate policies for customer support actions
-- Example: Restore soft-deleted reports, view all user data, etc.

-- CREATE POLICY "admin_view_all_reports"
-- ON reports
-- FOR SELECT
-- USING (
--     auth.jwt() ->> 'role' = 'admin'
-- );

-- ============================================================================
-- SERVICE ROLE BYPASS
-- ============================================================================

-- Service role (used by backend) bypasses RLS
-- This is essential for:
-- 1. Background jobs (soft-delete expired reports)
-- 2. Webhook processing (Stripe payment updates)
-- 3. Admin operations (customer support)

-- Service role key should be used ONLY in backend server environment
-- NEVER expose service role key to frontend or client applications

-- ============================================================================
-- TESTING RLS POLICIES
-- ============================================================================

-- To test RLS policies in Supabase:

-- 1. Create test user via Clerk
-- 2. Get JWT token from Clerk
-- 3. Set session in Supabase SQL editor:
--    SELECT set_config('request.jwt.claims', '{"sub": "clerk_user_id_here"}', true);
-- 4. Run queries as that user
-- 5. Verify only user's own data is accessible

-- Example test queries:

-- -- Should return only user's reports
-- SELECT * FROM reports;

-- -- Should fail (different user's report)
-- SELECT * FROM reports WHERE user_id = 'different-user-id';

-- -- Should succeed (user's own report)
-- INSERT INTO reports (user_id, subject, country, content, citations, expires_at)
-- VALUES (
--     (SELECT user_id FROM users WHERE clerk_user_id = auth.jwt() ->> 'sub'),
--     'Computer Science',
--     'UK',
--     '{"executive_summary": []}'::jsonb,
--     '[]'::jsonb,
--     NOW() + INTERVAL '30 days'
-- );

-- ============================================================================
-- CONCEPTUAL RLS RULES (for Documentation)
-- ============================================================================

-- Table: users
-- ├─ Policy: users_select_own
-- │  ├─ Target: SELECT
-- │  ├─ Rule: clerk_user_id = auth.jwt() ->> 'sub' AND deleted_at IS NULL
-- │  └─ Rationale: Users can only view their own active account
-- ├─ Policy: users_insert_own
-- │  ├─ Target: INSERT
-- │  ├─ Rule: clerk_user_id = auth.jwt() ->> 'sub'
-- │  └─ Rationale: Users can create their own account during signup
-- ├─ Policy: users_update_own
-- │  ├─ Target: UPDATE
-- │  ├─ Rule: clerk_user_id = auth.jwt() ->> 'sub' AND deleted_at IS NULL
-- │  └─ Rationale: Users can update their own active account
-- └─ Policy: users_delete_own
--    ├─ Target: UPDATE (soft delete via deleted_at)
--    ├─ Rule: clerk_user_id = auth.jwt() ->> 'sub'
--    └─ Rationale: Users can soft-delete their own account

-- Table: reports
-- ├─ Policy: reports_select_own
-- │  ├─ Target: SELECT
-- │  ├─ Rule: user_id matches authenticated user AND deleted_at IS NULL
-- │  └─ Rationale: Users can only view their own active reports
-- ├─ Policy: reports_insert_own
-- │  ├─ Target: INSERT
-- │  ├─ Rule: user_id matches authenticated user
-- │  └─ Rationale: Users can create reports for themselves
-- ├─ Policy: reports_update_own
-- │  ├─ Target: UPDATE
-- │  ├─ Rule: user_id matches authenticated user
-- │  └─ Rationale: Users can update their own reports (status changes)
-- └─ Policy: reports_delete_own
--    ├─ Target: UPDATE (soft delete via deleted_at)
--    ├─ Rule: user_id matches authenticated user
--    └─ Rationale: Users can soft-delete their own reports

-- Table: payments
-- ├─ Policy: payments_select_own
-- │  ├─ Target: SELECT
-- │  ├─ Rule: user_id matches authenticated user AND deleted_at IS NULL
-- │  └─ Rationale: Users can view their own payment history
-- ├─ Policy: payments_insert_own
-- │  ├─ Target: INSERT
-- │  ├─ Rule: user_id matches authenticated user
-- │  └─ Rationale: Users can initiate payments for themselves
-- ├─ Policy: payments_update_system
-- │  ├─ Target: UPDATE
-- │  ├─ Rule: auth.role() = 'service_role'
-- │  └─ Rationale: Backend service can update payment status from webhooks
-- └─ Policy: payments_update_own
--    ├─ Target: UPDATE
--    ├─ Rule: user_id matches authenticated user
--    └─ Rationale: Users can update their own payment records

-- ============================================================================
-- SECURITY CONSIDERATIONS
-- ============================================================================

-- 1. Service Role Key Protection:
--    - Service role key bypasses ALL RLS policies
--    - Must ONLY be used in backend server environment
--    - Never expose in frontend or client applications
--    - Store in Google Secret Manager (production)

-- 2. JWT Claims Validation:
--    - RLS policies rely on Clerk JWT 'sub' claim
--    - Clerk handles JWT validation and signing
--    - Supabase validates JWT signature before applying policies

-- 3. Soft Delete Security:
--    - Soft-deleted records (deleted_at IS NOT NULL) are excluded from SELECT
--    - Prevents accidental exposure of deleted data
--    - Admin restoration requires service role or custom policy

-- 4. Foreign Key Constraints:
--    - ON DELETE CASCADE ensures data consistency
--    - Deleting user cascades to reports and payments
--    - Prevents orphaned records

-- 5. Policy Testing:
--    - All policies should be tested before production deployment
--    - Test both positive (allowed) and negative (denied) cases
--    - Verify policies work correctly with service role bypass

-- ============================================================================
-- MAINTENANCE NOTES
-- ============================================================================

-- 1. Policy Changes:
--    - Changes to RLS policies require database migration
--    - Test policy changes in development/test environments first
--    - Monitor query performance after policy changes

-- 2. Policy Monitoring:
--    - Monitor Supabase logs for RLS policy violations
--    - Set up alerts for repeated access denials
--    - Review policies quarterly for optimization

-- 3. Performance Impact:
--    - RLS policies add overhead to every query
--    - Use indexes to optimize policy evaluation
--    - Consider partial indexes for common policy patterns

-- ============================================================================
-- END OF RLS POLICIES
-- ============================================================================
