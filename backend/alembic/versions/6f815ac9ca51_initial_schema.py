"""initial_schema

Create initial database schema for MVP UK Study & Migration App.

Tables:
- users: Authenticated user information (Clerk integration)
- reports: AI-generated study & migration reports
- payments: Stripe payment transactions

Enums:
- report_status: Report generation states
- payment_status: Payment states

Indexes:
- All foreign keys are indexed
- Common query patterns (user_id, status, expires_at, etc.)

Triggers:
- Auto-update updated_at timestamp on UPDATE

Revision ID: 6f815ac9ca51
Revises: 
Create Date: 2026-01-01 13:25:18.495402

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '6f815ac9ca51'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """
    Upgrade schema.
    
    Creates all tables, indexes, and triggers for the initial schema.
    """
    # Create ENUM types
    report_status = postgresql.ENUM(
        'pending', 'generating', 'completed', 'failed', 'expired',
        name='reportstatus',
        create_type=True
    )
    payment_status = postgresql.ENUM(
        'pending', 'succeeded', 'failed', 'refunded',
        name='paymentstatus',
        create_type=True
    )
    
    # Create users table
    op.create_table(
        'users',
        sa.Column('user_id', postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column('clerk_user_id', sa.String(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('email_verified', sa.Boolean(), server_default=sa.text('false'), nullable=False),
        sa.Column('auth_provider', sa.String(), nullable=False),
        sa.Column('full_name', sa.String(), nullable=True),
        sa.Column('avatar_url', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('last_login_at', sa.DateTime(timezone=True), nullable=True),
    )
    
    # Create users indexes
    op.create_index('idx_users_clerk_user_id', 'users', ['clerk_user_id'], unique=True)
    op.create_index('idx_users_email', 'users', ['email'], unique=False)
    
    # Create reports table
    op.create_table(
        'reports',
        sa.Column('report_id', postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('subject', sa.String(length=200), nullable=False),
        sa.Column('country', sa.String(length=50), server_default='UK', nullable=False),
        sa.Column('status', report_status, server_default='pending', nullable=False),
        sa.Column('content', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('citations', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('generation_metadata', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('completed_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('expires_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('error_message', sa.Text(), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ondelete='CASCADE'),
    )
    
    # Create reports indexes
    op.create_index('idx_reports_user_id', 'reports', ['user_id'], unique=False)
    op.create_index('idx_reports_status', 'reports', ['status'], unique=False)
    op.create_index('idx_reports_expires_at', 'reports', ['expires_at'], unique=False)
    
    # Create payments table
    op.create_table(
        'payments',
        sa.Column('payment_id', postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('report_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('stripe_checkout_session_id', sa.String(), nullable=False),
        sa.Column('stripe_payment_intent_id', sa.String(), nullable=True),
        sa.Column('amount_gbp', sa.Numeric(precision=10, scale=2), server_default='2.99', nullable=False),
        sa.Column('currency', sa.String(length=3), server_default='GBP', nullable=False),
        sa.Column('status', payment_status, server_default='pending', nullable=False),
        sa.Column('payment_method', sa.String(), nullable=True),
        sa.Column('stripe_customer_id', sa.String(), nullable=True),
        sa.Column('refund_reason', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('succeeded_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('refunded_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('metadata', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['report_id'], ['reports.report_id'], ondelete='SET NULL'),
    )
    
    # Create payments indexes
    op.create_index('idx_payments_user_id', 'payments', ['user_id'], unique=False)
    op.create_index('idx_payments_report_id', 'payments', ['report_id'], unique=False)
    op.create_index('idx_payments_stripe_session', 'payments', ['stripe_checkout_session_id'], unique=True)
    op.create_index('idx_payments_stripe_intent', 'payments', ['stripe_payment_intent_id'], unique=True)
    
    # Create trigger function for auto-updating updated_at
    op.execute("""
        CREATE OR REPLACE FUNCTION update_updated_at_column()
        RETURNS TRIGGER AS $$
        BEGIN
            NEW.updated_at = NOW();
            RETURN NEW;
        END;
        $$ language 'plpgsql';
    """)
    
    # Create triggers for users and reports tables
    op.execute("""
        CREATE TRIGGER update_users_updated_at
        BEFORE UPDATE ON users
        FOR EACH ROW
        EXECUTE FUNCTION update_updated_at_column();
    """)
    
    op.execute("""
        CREATE TRIGGER update_reports_updated_at
        BEFORE UPDATE ON reports
        FOR EACH ROW
        EXECUTE FUNCTION update_updated_at_column();
    """)


def downgrade() -> None:
    """
    Downgrade schema.
    
    Drops all tables, triggers, and ENUM types.
    """
    # Drop triggers
    op.execute("DROP TRIGGER IF EXISTS update_reports_updated_at ON reports;")
    op.execute("DROP TRIGGER IF EXISTS update_users_updated_at ON users;")
    
    # Drop trigger function
    op.execute("DROP FUNCTION IF EXISTS update_updated_at_column();")
    
    # Drop tables (in reverse order of creation due to foreign keys)
    op.drop_table('payments')
    op.drop_table('reports')
    op.drop_table('users')
    
    # Drop ENUM types
    sa.Enum(name='paymentstatus').drop(op.get_bind(), checkfirst=True)
    sa.Enum(name='reportstatus').drop(op.get_bind(), checkfirst=True)
