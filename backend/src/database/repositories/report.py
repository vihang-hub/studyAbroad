"""
Report Repository

Repository for Report model with soft delete support.
"""

from typing import Any
from datetime import datetime
from sqlalchemy import select
from database.types import Repository, DatabaseAdapter
from database.models.report import Report, ReportStatus


class ReportRepository(Repository[Report]):
    """
    Report Repository

    Provides CRUD operations for Report model with soft delete support.
    Reports use expires_at for soft delete (status='expired').
    """

    def __init__(self, adapter: DatabaseAdapter):
        super().__init__(adapter)

    async def find_by_id(self, id: str, include_deleted: bool = False) -> Report | None:
        """
        Find report by ID

        Args:
            id: Report UUID
            include_deleted: If True, include expired reports

        Returns:
            Report instance or None
        """
        async with await self.adapter.get_session() as session:
            query = select(Report).where(Report.report_id == id)

            if not include_deleted:
                # Exclude expired reports
                query = query.where(Report.status != ReportStatus.EXPIRED)

            result = await session.execute(query)
            return result.scalar_one_or_none()

    async def find_by_user(
        self, user_id: str, skip: int = 0, limit: int = 100, include_deleted: bool = False
    ) -> list[Report]:
        """
        Find all reports for a user

        Args:
            user_id: User UUID
            skip: Number of records to skip
            limit: Maximum number of records to return
            include_deleted: If True, include expired reports

        Returns:
            List of Report instances
        """
        async with await self.adapter.get_session() as session:
            query = select(Report).where(Report.user_id == user_id)

            if not include_deleted:
                query = query.where(Report.status != ReportStatus.EXPIRED)

            query = query.offset(skip).limit(limit).order_by(Report.created_at.desc())

            result = await session.execute(query)
            return list(result.scalars().all())

    async def find_all(
        self, skip: int = 0, limit: int = 100, include_deleted: bool = False
    ) -> list[Report]:
        """
        Find all reports with pagination

        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            include_deleted: If True, include expired reports

        Returns:
            List of Report instances
        """
        async with await self.adapter.get_session() as session:
            query = select(Report)

            if not include_deleted:
                query = query.where(Report.status != ReportStatus.EXPIRED)

            query = query.offset(skip).limit(limit).order_by(Report.created_at.desc())

            result = await session.execute(query)
            return list(result.scalars().all())

    async def create(self, data: dict[str, Any]) -> Report:
        """
        Create new report

        Args:
            data: Report data dictionary

        Returns:
            Created Report instance
        """
        async with await self.adapter.get_session() as session:
            report = Report(**data)
            session.add(report)
            await session.commit()
            await session.refresh(report)
            return report

    async def update(self, id: str, data: dict[str, Any]) -> Report | None:
        """
        Update report

        Args:
            id: Report UUID
            data: Updated data dictionary

        Returns:
            Updated Report instance or None
        """
        async with await self.adapter.get_session() as session:
            report = await self.find_by_id(id, include_deleted=True)
            if not report:
                return None

            for key, value in data.items():
                if hasattr(report, key):
                    setattr(report, key, value)

            session.add(report)
            await session.commit()
            await session.refresh(report)
            return report

    async def soft_delete(self, id: str) -> Report | None:
        """
        Soft delete report (set status to EXPIRED)

        Args:
            id: Report UUID

        Returns:
            Updated Report instance or None
        """
        return await self.update(id, {"status": ReportStatus.EXPIRED})

    async def hard_delete(self, id: str) -> bool:
        """
        Hard delete report (permanent)

        Args:
            id: Report UUID

        Returns:
            True if deleted, False otherwise
        """
        async with await self.adapter.get_session() as session:
            report = await self.find_by_id(id, include_deleted=True)
            if not report:
                return False

            await session.delete(report)
            await session.commit()
            return True

    async def restore(self, id: str) -> Report | None:
        """
        Restore soft-deleted report (set status back to COMPLETED)

        Args:
            id: Report UUID

        Returns:
            Restored Report instance or None
        """
        report = await self.find_by_id(id, include_deleted=True)
        if not report or report.status != ReportStatus.EXPIRED:
            return None

        return await self.update(id, {"status": ReportStatus.COMPLETED})

    async def expire_old_reports(self) -> int:
        """
        Expire reports past their expires_at date

        Returns:
            Number of reports expired
        """
        async with await self.adapter.get_session() as session:
            query = (
                select(Report)
                .where(Report.expires_at < datetime.utcnow())
                .where(
                    Report.status.in_(
                        [
                            ReportStatus.PENDING,
                            ReportStatus.GENERATING,
                            ReportStatus.COMPLETED,
                            ReportStatus.FAILED,
                        ]
                    )
                )
            )

            result = await session.execute(query)
            reports = list(result.scalars().all())

            for report in reports:
                report.status = ReportStatus.EXPIRED

            await session.commit()
            return len(reports)

    async def delete_expired_reports(self) -> int:
        """
        Delete reports that have been expired for more than 90 days (hard delete).
        This implements the GDPR data retention requirement.

        Process:
        1. Soft delete (set status=expired): Reports past expires_at (30 days after creation)
        2. Hard delete: Reports 90 days past expires_at (120 days after creation)

        Returns:
            Number of reports permanently deleted
        """
        from datetime import timedelta

        async with await self.adapter.get_session() as session:
            # Calculate cutoff: 90 days before now
            # Reports expired 90 days ago should be deleted
            cutoff_date = datetime.utcnow() - timedelta(days=90)

            # Find expired reports where expires_at is before cutoff
            query = (
                select(Report)
                .where(Report.status == ReportStatus.EXPIRED)
                .where(Report.expires_at < cutoff_date)
            )

            result = await session.execute(query)
            reports = list(result.scalars().all())

            # Hard delete all matching reports
            for report in reports:
                await session.delete(report)

            await session.commit()
            return len(reports)
