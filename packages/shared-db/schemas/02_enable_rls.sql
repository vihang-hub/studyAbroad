-- Row Level Security (RLS) Policies
-- As required by Constitution Section 2: Security Framework

-- Enable RLS on all tables
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE chat_sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE chat_messages ENABLE ROW LEVEL SECURITY;
ALTER TABLE citations ENABLE ROW LEVEL SECURITY;
ALTER TABLE documents ENABLE ROW LEVEL SECURITY;

-- Users table policies
-- Users can only see their own profile
CREATE POLICY users_select_own ON users
    FOR SELECT
    USING (id = current_setting('app.user_id', true)::UUID);

-- Users can update their own profile
CREATE POLICY users_update_own ON users
    FOR UPDATE
    USING (id = current_setting('app.user_id', true)::UUID);

-- Chat sessions policies
-- Users can only see their own chat sessions
CREATE POLICY chat_sessions_select_own ON chat_sessions
    FOR SELECT
    USING (user_id = current_setting('app.user_id', true)::UUID);

-- Users can insert their own chat sessions
CREATE POLICY chat_sessions_insert_own ON chat_sessions
    FOR INSERT
    WITH CHECK (user_id = current_setting('app.user_id', true)::UUID);

-- Users can update their own chat sessions
CREATE POLICY chat_sessions_update_own ON chat_sessions
    FOR UPDATE
    USING (user_id = current_setting('app.user_id', true)::UUID);

-- Users can delete their own chat sessions
CREATE POLICY chat_sessions_delete_own ON chat_sessions
    FOR DELETE
    USING (user_id = current_setting('app.user_id', true)::UUID);

-- Chat messages policies
-- Users can only see messages from their own sessions
CREATE POLICY chat_messages_select_own ON chat_messages
    FOR SELECT
    USING (
        session_id IN (
            SELECT id FROM chat_sessions
            WHERE user_id = current_setting('app.user_id', true)::UUID
        )
    );

-- Users can insert messages to their own sessions
CREATE POLICY chat_messages_insert_own ON chat_messages
    FOR INSERT
    WITH CHECK (
        session_id IN (
            SELECT id FROM chat_sessions
            WHERE user_id = current_setting('app.user_id', true)::UUID
        )
    );

-- Citations policies
-- Users can only see citations from their own messages
CREATE POLICY citations_select_own ON citations
    FOR SELECT
    USING (
        message_id IN (
            SELECT cm.id FROM chat_messages cm
            JOIN chat_sessions cs ON cm.session_id = cs.id
            WHERE cs.user_id = current_setting('app.user_id', true)::UUID
        )
    );

-- Documents policies
-- All authenticated users can read documents (public knowledge base)
CREATE POLICY documents_select_all ON documents
    FOR SELECT
    USING (true);

-- Only service role can insert/update documents
-- (This will be handled by the application, not by RLS)

-- Create a function to set user context
CREATE OR REPLACE FUNCTION set_user_context(user_uuid UUID)
RETURNS void AS $$
BEGIN
    PERFORM set_config('app.user_id', user_uuid::text, false);
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Grant execute permission on the function
GRANT EXECUTE ON FUNCTION set_user_context(UUID) TO PUBLIC;
