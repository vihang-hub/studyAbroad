"""
User Model

SQLAlchemy model for users table.
Maps to data-model.md users table schema.
"""

from datetime import datetime
from sqlalchemy import String, Boolean, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
import uuid


class Base(DeclarativeBase):
    """SQLAlchemy declarative base"""

    pass


class User(Base):
    """
    User Model

    Represents authenticated users from Clerk.

    Columns:
        user_id: Internal UUID (primary key)
        clerk_user_id: Clerk's unique identifier
        email: User's email address
        email_verified: Whether email is verified
        auth_provider: OAuth provider (google, apple, facebook, email)
        full_name: User's display name
        avatar_url: Profile picture URL
        created_at: Account creation timestamp
        updated_at: Last profile update
        last_login_at: Last successful authentication
    """

    __tablename__ = "users"

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    clerk_user_id: Mapped[str] = mapped_column(String, unique=True, nullable=False, index=True)
    email: Mapped[str] = mapped_column(String, nullable=False, index=True)
    email_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    auth_provider: Mapped[str] = mapped_column(String, nullable=False)
    full_name: Mapped[str | None] = mapped_column(String, nullable=True)
    avatar_url: Mapped[str | None] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    last_login_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    def __repr__(self) -> str:
        return f"<User(user_id={self.user_id}, email={self.email})>"
