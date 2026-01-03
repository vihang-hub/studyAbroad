"""
Payment Repository

Repository for Payment model with CRUD operations.
"""

from typing import Any
from sqlalchemy import select
from database.types import Repository, DatabaseAdapter
from database.models.payment import Payment


class PaymentRepository(Repository[Payment]):
    """
    Payment Repository

    Provides CRUD operations for Payment model.
    Payments don't have soft delete (audit trail must be permanent).
    """

    def __init__(self, adapter: DatabaseAdapter):
        super().__init__(adapter)

    async def find_by_id(self, id: str, include_deleted: bool = False) -> Payment | None:
        """
        Find payment by ID

        Args:
            id: Payment UUID
            include_deleted: Ignored for payments (no soft delete)

        Returns:
            Payment instance or None
        """
        async with await self.adapter.get_session() as session:
            result = await session.execute(select(Payment).where(Payment.payment_id == id))
            return result.scalar_one_or_none()

    async def find_by_stripe_session_id(self, session_id: str) -> Payment | None:
        """
        Find payment by Stripe Checkout Session ID

        Args:
            session_id: Stripe session ID

        Returns:
            Payment instance or None
        """
        async with await self.adapter.get_session() as session:
            result = await session.execute(
                select(Payment).where(Payment.stripe_checkout_session_id == session_id)
            )
            return result.scalar_one_or_none()

    async def find_by_stripe_payment_intent_id(self, payment_intent_id: str) -> Payment | None:
        """
        Find payment by Stripe Payment Intent ID

        Args:
            payment_intent_id: Stripe payment intent ID

        Returns:
            Payment instance or None
        """
        async with await self.adapter.get_session() as session:
            result = await session.execute(
                select(Payment).where(Payment.stripe_payment_intent_id == payment_intent_id)
            )
            return result.scalar_one_or_none()

    async def find_by_user(
        self, user_id: str, skip: int = 0, limit: int = 100, include_deleted: bool = False
    ) -> list[Payment]:
        """
        Find all payments for a user

        Args:
            user_id: User UUID
            skip: Number of records to skip
            limit: Maximum number of records to return
            include_deleted: Ignored for payments

        Returns:
            List of Payment instances
        """
        async with await self.adapter.get_session() as session:
            query = (
                select(Payment)
                .where(Payment.user_id == user_id)
                .offset(skip)
                .limit(limit)
                .order_by(Payment.created_at.desc())
            )

            result = await session.execute(query)
            return list(result.scalars().all())

    async def find_all(
        self, skip: int = 0, limit: int = 100, include_deleted: bool = False
    ) -> list[Payment]:
        """
        Find all payments with pagination

        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            include_deleted: Ignored for payments

        Returns:
            List of Payment instances
        """
        async with await self.adapter.get_session() as session:
            query = select(Payment).offset(skip).limit(limit).order_by(Payment.created_at.desc())

            result = await session.execute(query)
            return list(result.scalars().all())

    async def create(self, data: dict[str, Any]) -> Payment:
        """
        Create new payment

        Args:
            data: Payment data dictionary

        Returns:
            Created Payment instance
        """
        async with await self.adapter.get_session() as session:
            payment = Payment(**data)
            session.add(payment)
            await session.commit()
            await session.refresh(payment)
            return payment

    async def update(self, id: str, data: dict[str, Any]) -> Payment | None:
        """
        Update payment

        Args:
            id: Payment UUID
            data: Updated data dictionary

        Returns:
            Updated Payment instance or None
        """
        async with await self.adapter.get_session() as session:
            payment = await self.find_by_id(id)
            if not payment:
                return None

            for key, value in data.items():
                if hasattr(payment, key):
                    setattr(payment, key, value)

            session.add(payment)
            await session.commit()
            await session.refresh(payment)
            return payment

    async def soft_delete(self, id: str) -> Payment | None:
        """
        Soft delete not applicable for payments (audit trail)

        Args:
            id: Payment UUID

        Returns:
            None (not implemented)
        """
        # Payments don't support soft delete (audit requirement)
        return None

    async def hard_delete(self, id: str) -> bool:
        """
        Hard delete not recommended for payments (audit trail)

        Args:
            id: Payment UUID

        Returns:
            False (not recommended to delete payments)
        """
        # Payments should not be deleted (compliance/audit requirement)
        return False

    async def restore(self, id: str) -> Payment | None:
        """
        Restore not applicable for payments

        Args:
            id: Payment UUID

        Returns:
            None (not implemented)
        """
        # Payments don't support soft delete
        return None
