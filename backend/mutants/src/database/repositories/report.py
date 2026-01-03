"""
Report Repository

Repository for Report model with soft delete support.
"""

from typing import Any
from datetime import datetime
from sqlalchemy import select
from database.types import Repository, DatabaseAdapter
from database.models.report import Report, ReportStatus
from inspect import signature as _mutmut_signature
from typing import Annotated
from typing import Callable
from typing import ClassVar


MutantDict = Annotated[dict[str, Callable], "Mutant"]


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg = None):
    """Forward call to original or mutated function, depending on the environment"""
    import os
    mutant_under_test = os.environ['MUTANT_UNDER_TEST']
    if mutant_under_test == 'fail':
        from mutmut.__main__ import MutmutProgrammaticFailException
        raise MutmutProgrammaticFailException('Failed programmatically')      
    elif mutant_under_test == 'stats':
        from mutmut.__main__ import record_trampoline_hit
        record_trampoline_hit(orig.__module__ + '.' + orig.__name__)
        result = orig(*call_args, **call_kwargs)
        return result
    prefix = orig.__module__ + '.' + orig.__name__ + '__mutmut_'
    if not mutant_under_test.startswith(prefix):
        result = orig(*call_args, **call_kwargs)
        return result
    mutant_name = mutant_under_test.rpartition('.')[-1]
    if self_arg is not None:
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs)
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs)
    return result


class ReportRepository(Repository[Report]):
    """
    Report Repository

    Provides CRUD operations for Report model with soft delete support.
    Reports use expires_at for soft delete (status='expired').
    """

    def xǁReportRepositoryǁ__init____mutmut_orig(self, adapter: DatabaseAdapter):
        super().__init__(adapter)

    def xǁReportRepositoryǁ__init____mutmut_1(self, adapter: DatabaseAdapter):
        super().__init__(None)
    
    xǁReportRepositoryǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁReportRepositoryǁ__init____mutmut_1': xǁReportRepositoryǁ__init____mutmut_1
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁReportRepositoryǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁReportRepositoryǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁReportRepositoryǁ__init____mutmut_orig)
    xǁReportRepositoryǁ__init____mutmut_orig.__name__ = 'xǁReportRepositoryǁ__init__'

    async def xǁReportRepositoryǁfind_by_id__mutmut_orig(self, id: str, include_deleted: bool = False) -> Report | None:
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

    async def xǁReportRepositoryǁfind_by_id__mutmut_1(self, id: str, include_deleted: bool = True) -> Report | None:
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

    async def xǁReportRepositoryǁfind_by_id__mutmut_2(self, id: str, include_deleted: bool = False) -> Report | None:
        """
        Find report by ID

        Args:
            id: Report UUID
            include_deleted: If True, include expired reports

        Returns:
            Report instance or None
        """
        async with await self.adapter.get_session() as session:
            query = None

            if not include_deleted:
                # Exclude expired reports
                query = query.where(Report.status != ReportStatus.EXPIRED)

            result = await session.execute(query)
            return result.scalar_one_or_none()

    async def xǁReportRepositoryǁfind_by_id__mutmut_3(self, id: str, include_deleted: bool = False) -> Report | None:
        """
        Find report by ID

        Args:
            id: Report UUID
            include_deleted: If True, include expired reports

        Returns:
            Report instance or None
        """
        async with await self.adapter.get_session() as session:
            query = select(Report).where(None)

            if not include_deleted:
                # Exclude expired reports
                query = query.where(Report.status != ReportStatus.EXPIRED)

            result = await session.execute(query)
            return result.scalar_one_or_none()

    async def xǁReportRepositoryǁfind_by_id__mutmut_4(self, id: str, include_deleted: bool = False) -> Report | None:
        """
        Find report by ID

        Args:
            id: Report UUID
            include_deleted: If True, include expired reports

        Returns:
            Report instance or None
        """
        async with await self.adapter.get_session() as session:
            query = select(None).where(Report.report_id == id)

            if not include_deleted:
                # Exclude expired reports
                query = query.where(Report.status != ReportStatus.EXPIRED)

            result = await session.execute(query)
            return result.scalar_one_or_none()

    async def xǁReportRepositoryǁfind_by_id__mutmut_5(self, id: str, include_deleted: bool = False) -> Report | None:
        """
        Find report by ID

        Args:
            id: Report UUID
            include_deleted: If True, include expired reports

        Returns:
            Report instance or None
        """
        async with await self.adapter.get_session() as session:
            query = select(Report).where(Report.report_id != id)

            if not include_deleted:
                # Exclude expired reports
                query = query.where(Report.status != ReportStatus.EXPIRED)

            result = await session.execute(query)
            return result.scalar_one_or_none()

    async def xǁReportRepositoryǁfind_by_id__mutmut_6(self, id: str, include_deleted: bool = False) -> Report | None:
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

            if include_deleted:
                # Exclude expired reports
                query = query.where(Report.status != ReportStatus.EXPIRED)

            result = await session.execute(query)
            return result.scalar_one_or_none()

    async def xǁReportRepositoryǁfind_by_id__mutmut_7(self, id: str, include_deleted: bool = False) -> Report | None:
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
                query = None

            result = await session.execute(query)
            return result.scalar_one_or_none()

    async def xǁReportRepositoryǁfind_by_id__mutmut_8(self, id: str, include_deleted: bool = False) -> Report | None:
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
                query = query.where(None)

            result = await session.execute(query)
            return result.scalar_one_or_none()

    async def xǁReportRepositoryǁfind_by_id__mutmut_9(self, id: str, include_deleted: bool = False) -> Report | None:
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
                query = query.where(Report.status == ReportStatus.EXPIRED)

            result = await session.execute(query)
            return result.scalar_one_or_none()

    async def xǁReportRepositoryǁfind_by_id__mutmut_10(self, id: str, include_deleted: bool = False) -> Report | None:
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

            result = None
            return result.scalar_one_or_none()

    async def xǁReportRepositoryǁfind_by_id__mutmut_11(self, id: str, include_deleted: bool = False) -> Report | None:
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

            result = await session.execute(None)
            return result.scalar_one_or_none()
    
    xǁReportRepositoryǁfind_by_id__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁReportRepositoryǁfind_by_id__mutmut_1': xǁReportRepositoryǁfind_by_id__mutmut_1, 
        'xǁReportRepositoryǁfind_by_id__mutmut_2': xǁReportRepositoryǁfind_by_id__mutmut_2, 
        'xǁReportRepositoryǁfind_by_id__mutmut_3': xǁReportRepositoryǁfind_by_id__mutmut_3, 
        'xǁReportRepositoryǁfind_by_id__mutmut_4': xǁReportRepositoryǁfind_by_id__mutmut_4, 
        'xǁReportRepositoryǁfind_by_id__mutmut_5': xǁReportRepositoryǁfind_by_id__mutmut_5, 
        'xǁReportRepositoryǁfind_by_id__mutmut_6': xǁReportRepositoryǁfind_by_id__mutmut_6, 
        'xǁReportRepositoryǁfind_by_id__mutmut_7': xǁReportRepositoryǁfind_by_id__mutmut_7, 
        'xǁReportRepositoryǁfind_by_id__mutmut_8': xǁReportRepositoryǁfind_by_id__mutmut_8, 
        'xǁReportRepositoryǁfind_by_id__mutmut_9': xǁReportRepositoryǁfind_by_id__mutmut_9, 
        'xǁReportRepositoryǁfind_by_id__mutmut_10': xǁReportRepositoryǁfind_by_id__mutmut_10, 
        'xǁReportRepositoryǁfind_by_id__mutmut_11': xǁReportRepositoryǁfind_by_id__mutmut_11
    }
    
    def find_by_id(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁReportRepositoryǁfind_by_id__mutmut_orig"), object.__getattribute__(self, "xǁReportRepositoryǁfind_by_id__mutmut_mutants"), args, kwargs, self)
        return result 
    
    find_by_id.__signature__ = _mutmut_signature(xǁReportRepositoryǁfind_by_id__mutmut_orig)
    xǁReportRepositoryǁfind_by_id__mutmut_orig.__name__ = 'xǁReportRepositoryǁfind_by_id'

    async def xǁReportRepositoryǁfind_by_user__mutmut_orig(
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

    async def xǁReportRepositoryǁfind_by_user__mutmut_1(
        self, user_id: str, skip: int = 1, limit: int = 100, include_deleted: bool = False
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

    async def xǁReportRepositoryǁfind_by_user__mutmut_2(
        self, user_id: str, skip: int = 0, limit: int = 101, include_deleted: bool = False
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

    async def xǁReportRepositoryǁfind_by_user__mutmut_3(
        self, user_id: str, skip: int = 0, limit: int = 100, include_deleted: bool = True
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

    async def xǁReportRepositoryǁfind_by_user__mutmut_4(
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
            query = None

            if not include_deleted:
                query = query.where(Report.status != ReportStatus.EXPIRED)

            query = query.offset(skip).limit(limit).order_by(Report.created_at.desc())

            result = await session.execute(query)
            return list(result.scalars().all())

    async def xǁReportRepositoryǁfind_by_user__mutmut_5(
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
            query = select(Report).where(None)

            if not include_deleted:
                query = query.where(Report.status != ReportStatus.EXPIRED)

            query = query.offset(skip).limit(limit).order_by(Report.created_at.desc())

            result = await session.execute(query)
            return list(result.scalars().all())

    async def xǁReportRepositoryǁfind_by_user__mutmut_6(
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
            query = select(None).where(Report.user_id == user_id)

            if not include_deleted:
                query = query.where(Report.status != ReportStatus.EXPIRED)

            query = query.offset(skip).limit(limit).order_by(Report.created_at.desc())

            result = await session.execute(query)
            return list(result.scalars().all())

    async def xǁReportRepositoryǁfind_by_user__mutmut_7(
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
            query = select(Report).where(Report.user_id != user_id)

            if not include_deleted:
                query = query.where(Report.status != ReportStatus.EXPIRED)

            query = query.offset(skip).limit(limit).order_by(Report.created_at.desc())

            result = await session.execute(query)
            return list(result.scalars().all())

    async def xǁReportRepositoryǁfind_by_user__mutmut_8(
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

            if include_deleted:
                query = query.where(Report.status != ReportStatus.EXPIRED)

            query = query.offset(skip).limit(limit).order_by(Report.created_at.desc())

            result = await session.execute(query)
            return list(result.scalars().all())

    async def xǁReportRepositoryǁfind_by_user__mutmut_9(
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
                query = None

            query = query.offset(skip).limit(limit).order_by(Report.created_at.desc())

            result = await session.execute(query)
            return list(result.scalars().all())

    async def xǁReportRepositoryǁfind_by_user__mutmut_10(
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
                query = query.where(None)

            query = query.offset(skip).limit(limit).order_by(Report.created_at.desc())

            result = await session.execute(query)
            return list(result.scalars().all())

    async def xǁReportRepositoryǁfind_by_user__mutmut_11(
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
                query = query.where(Report.status == ReportStatus.EXPIRED)

            query = query.offset(skip).limit(limit).order_by(Report.created_at.desc())

            result = await session.execute(query)
            return list(result.scalars().all())

    async def xǁReportRepositoryǁfind_by_user__mutmut_12(
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

            query = None

            result = await session.execute(query)
            return list(result.scalars().all())

    async def xǁReportRepositoryǁfind_by_user__mutmut_13(
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

            query = query.offset(skip).limit(limit).order_by(None)

            result = await session.execute(query)
            return list(result.scalars().all())

    async def xǁReportRepositoryǁfind_by_user__mutmut_14(
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

            query = query.offset(skip).limit(None).order_by(Report.created_at.desc())

            result = await session.execute(query)
            return list(result.scalars().all())

    async def xǁReportRepositoryǁfind_by_user__mutmut_15(
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

            query = query.offset(None).limit(limit).order_by(Report.created_at.desc())

            result = await session.execute(query)
            return list(result.scalars().all())

    async def xǁReportRepositoryǁfind_by_user__mutmut_16(
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

            result = None
            return list(result.scalars().all())

    async def xǁReportRepositoryǁfind_by_user__mutmut_17(
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

            result = await session.execute(None)
            return list(result.scalars().all())

    async def xǁReportRepositoryǁfind_by_user__mutmut_18(
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
            return list(None)
    
    xǁReportRepositoryǁfind_by_user__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁReportRepositoryǁfind_by_user__mutmut_1': xǁReportRepositoryǁfind_by_user__mutmut_1, 
        'xǁReportRepositoryǁfind_by_user__mutmut_2': xǁReportRepositoryǁfind_by_user__mutmut_2, 
        'xǁReportRepositoryǁfind_by_user__mutmut_3': xǁReportRepositoryǁfind_by_user__mutmut_3, 
        'xǁReportRepositoryǁfind_by_user__mutmut_4': xǁReportRepositoryǁfind_by_user__mutmut_4, 
        'xǁReportRepositoryǁfind_by_user__mutmut_5': xǁReportRepositoryǁfind_by_user__mutmut_5, 
        'xǁReportRepositoryǁfind_by_user__mutmut_6': xǁReportRepositoryǁfind_by_user__mutmut_6, 
        'xǁReportRepositoryǁfind_by_user__mutmut_7': xǁReportRepositoryǁfind_by_user__mutmut_7, 
        'xǁReportRepositoryǁfind_by_user__mutmut_8': xǁReportRepositoryǁfind_by_user__mutmut_8, 
        'xǁReportRepositoryǁfind_by_user__mutmut_9': xǁReportRepositoryǁfind_by_user__mutmut_9, 
        'xǁReportRepositoryǁfind_by_user__mutmut_10': xǁReportRepositoryǁfind_by_user__mutmut_10, 
        'xǁReportRepositoryǁfind_by_user__mutmut_11': xǁReportRepositoryǁfind_by_user__mutmut_11, 
        'xǁReportRepositoryǁfind_by_user__mutmut_12': xǁReportRepositoryǁfind_by_user__mutmut_12, 
        'xǁReportRepositoryǁfind_by_user__mutmut_13': xǁReportRepositoryǁfind_by_user__mutmut_13, 
        'xǁReportRepositoryǁfind_by_user__mutmut_14': xǁReportRepositoryǁfind_by_user__mutmut_14, 
        'xǁReportRepositoryǁfind_by_user__mutmut_15': xǁReportRepositoryǁfind_by_user__mutmut_15, 
        'xǁReportRepositoryǁfind_by_user__mutmut_16': xǁReportRepositoryǁfind_by_user__mutmut_16, 
        'xǁReportRepositoryǁfind_by_user__mutmut_17': xǁReportRepositoryǁfind_by_user__mutmut_17, 
        'xǁReportRepositoryǁfind_by_user__mutmut_18': xǁReportRepositoryǁfind_by_user__mutmut_18
    }
    
    def find_by_user(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁReportRepositoryǁfind_by_user__mutmut_orig"), object.__getattribute__(self, "xǁReportRepositoryǁfind_by_user__mutmut_mutants"), args, kwargs, self)
        return result 
    
    find_by_user.__signature__ = _mutmut_signature(xǁReportRepositoryǁfind_by_user__mutmut_orig)
    xǁReportRepositoryǁfind_by_user__mutmut_orig.__name__ = 'xǁReportRepositoryǁfind_by_user'

    async def xǁReportRepositoryǁfind_all__mutmut_orig(
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

    async def xǁReportRepositoryǁfind_all__mutmut_1(
        self, skip: int = 1, limit: int = 100, include_deleted: bool = False
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

    async def xǁReportRepositoryǁfind_all__mutmut_2(
        self, skip: int = 0, limit: int = 101, include_deleted: bool = False
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

    async def xǁReportRepositoryǁfind_all__mutmut_3(
        self, skip: int = 0, limit: int = 100, include_deleted: bool = True
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

    async def xǁReportRepositoryǁfind_all__mutmut_4(
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
            query = None

            if not include_deleted:
                query = query.where(Report.status != ReportStatus.EXPIRED)

            query = query.offset(skip).limit(limit).order_by(Report.created_at.desc())

            result = await session.execute(query)
            return list(result.scalars().all())

    async def xǁReportRepositoryǁfind_all__mutmut_5(
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
            query = select(None)

            if not include_deleted:
                query = query.where(Report.status != ReportStatus.EXPIRED)

            query = query.offset(skip).limit(limit).order_by(Report.created_at.desc())

            result = await session.execute(query)
            return list(result.scalars().all())

    async def xǁReportRepositoryǁfind_all__mutmut_6(
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

            if include_deleted:
                query = query.where(Report.status != ReportStatus.EXPIRED)

            query = query.offset(skip).limit(limit).order_by(Report.created_at.desc())

            result = await session.execute(query)
            return list(result.scalars().all())

    async def xǁReportRepositoryǁfind_all__mutmut_7(
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
                query = None

            query = query.offset(skip).limit(limit).order_by(Report.created_at.desc())

            result = await session.execute(query)
            return list(result.scalars().all())

    async def xǁReportRepositoryǁfind_all__mutmut_8(
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
                query = query.where(None)

            query = query.offset(skip).limit(limit).order_by(Report.created_at.desc())

            result = await session.execute(query)
            return list(result.scalars().all())

    async def xǁReportRepositoryǁfind_all__mutmut_9(
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
                query = query.where(Report.status == ReportStatus.EXPIRED)

            query = query.offset(skip).limit(limit).order_by(Report.created_at.desc())

            result = await session.execute(query)
            return list(result.scalars().all())

    async def xǁReportRepositoryǁfind_all__mutmut_10(
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

            query = None

            result = await session.execute(query)
            return list(result.scalars().all())

    async def xǁReportRepositoryǁfind_all__mutmut_11(
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

            query = query.offset(skip).limit(limit).order_by(None)

            result = await session.execute(query)
            return list(result.scalars().all())

    async def xǁReportRepositoryǁfind_all__mutmut_12(
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

            query = query.offset(skip).limit(None).order_by(Report.created_at.desc())

            result = await session.execute(query)
            return list(result.scalars().all())

    async def xǁReportRepositoryǁfind_all__mutmut_13(
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

            query = query.offset(None).limit(limit).order_by(Report.created_at.desc())

            result = await session.execute(query)
            return list(result.scalars().all())

    async def xǁReportRepositoryǁfind_all__mutmut_14(
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

            result = None
            return list(result.scalars().all())

    async def xǁReportRepositoryǁfind_all__mutmut_15(
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

            result = await session.execute(None)
            return list(result.scalars().all())

    async def xǁReportRepositoryǁfind_all__mutmut_16(
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
            return list(None)
    
    xǁReportRepositoryǁfind_all__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁReportRepositoryǁfind_all__mutmut_1': xǁReportRepositoryǁfind_all__mutmut_1, 
        'xǁReportRepositoryǁfind_all__mutmut_2': xǁReportRepositoryǁfind_all__mutmut_2, 
        'xǁReportRepositoryǁfind_all__mutmut_3': xǁReportRepositoryǁfind_all__mutmut_3, 
        'xǁReportRepositoryǁfind_all__mutmut_4': xǁReportRepositoryǁfind_all__mutmut_4, 
        'xǁReportRepositoryǁfind_all__mutmut_5': xǁReportRepositoryǁfind_all__mutmut_5, 
        'xǁReportRepositoryǁfind_all__mutmut_6': xǁReportRepositoryǁfind_all__mutmut_6, 
        'xǁReportRepositoryǁfind_all__mutmut_7': xǁReportRepositoryǁfind_all__mutmut_7, 
        'xǁReportRepositoryǁfind_all__mutmut_8': xǁReportRepositoryǁfind_all__mutmut_8, 
        'xǁReportRepositoryǁfind_all__mutmut_9': xǁReportRepositoryǁfind_all__mutmut_9, 
        'xǁReportRepositoryǁfind_all__mutmut_10': xǁReportRepositoryǁfind_all__mutmut_10, 
        'xǁReportRepositoryǁfind_all__mutmut_11': xǁReportRepositoryǁfind_all__mutmut_11, 
        'xǁReportRepositoryǁfind_all__mutmut_12': xǁReportRepositoryǁfind_all__mutmut_12, 
        'xǁReportRepositoryǁfind_all__mutmut_13': xǁReportRepositoryǁfind_all__mutmut_13, 
        'xǁReportRepositoryǁfind_all__mutmut_14': xǁReportRepositoryǁfind_all__mutmut_14, 
        'xǁReportRepositoryǁfind_all__mutmut_15': xǁReportRepositoryǁfind_all__mutmut_15, 
        'xǁReportRepositoryǁfind_all__mutmut_16': xǁReportRepositoryǁfind_all__mutmut_16
    }
    
    def find_all(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁReportRepositoryǁfind_all__mutmut_orig"), object.__getattribute__(self, "xǁReportRepositoryǁfind_all__mutmut_mutants"), args, kwargs, self)
        return result 
    
    find_all.__signature__ = _mutmut_signature(xǁReportRepositoryǁfind_all__mutmut_orig)
    xǁReportRepositoryǁfind_all__mutmut_orig.__name__ = 'xǁReportRepositoryǁfind_all'

    async def xǁReportRepositoryǁcreate__mutmut_orig(self, data: dict[str, Any]) -> Report:
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

    async def xǁReportRepositoryǁcreate__mutmut_1(self, data: dict[str, Any]) -> Report:
        """
        Create new report

        Args:
            data: Report data dictionary

        Returns:
            Created Report instance
        """
        async with await self.adapter.get_session() as session:
            report = None
            session.add(report)
            await session.commit()
            await session.refresh(report)
            return report

    async def xǁReportRepositoryǁcreate__mutmut_2(self, data: dict[str, Any]) -> Report:
        """
        Create new report

        Args:
            data: Report data dictionary

        Returns:
            Created Report instance
        """
        async with await self.adapter.get_session() as session:
            report = Report(**data)
            session.add(None)
            await session.commit()
            await session.refresh(report)
            return report

    async def xǁReportRepositoryǁcreate__mutmut_3(self, data: dict[str, Any]) -> Report:
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
            await session.refresh(None)
            return report
    
    xǁReportRepositoryǁcreate__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁReportRepositoryǁcreate__mutmut_1': xǁReportRepositoryǁcreate__mutmut_1, 
        'xǁReportRepositoryǁcreate__mutmut_2': xǁReportRepositoryǁcreate__mutmut_2, 
        'xǁReportRepositoryǁcreate__mutmut_3': xǁReportRepositoryǁcreate__mutmut_3
    }
    
    def create(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁReportRepositoryǁcreate__mutmut_orig"), object.__getattribute__(self, "xǁReportRepositoryǁcreate__mutmut_mutants"), args, kwargs, self)
        return result 
    
    create.__signature__ = _mutmut_signature(xǁReportRepositoryǁcreate__mutmut_orig)
    xǁReportRepositoryǁcreate__mutmut_orig.__name__ = 'xǁReportRepositoryǁcreate'

    async def xǁReportRepositoryǁupdate__mutmut_orig(self, id: str, data: dict[str, Any]) -> Report | None:
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

    async def xǁReportRepositoryǁupdate__mutmut_1(self, id: str, data: dict[str, Any]) -> Report | None:
        """
        Update report

        Args:
            id: Report UUID
            data: Updated data dictionary

        Returns:
            Updated Report instance or None
        """
        async with await self.adapter.get_session() as session:
            report = None
            if not report:
                return None

            for key, value in data.items():
                if hasattr(report, key):
                    setattr(report, key, value)

            session.add(report)
            await session.commit()
            await session.refresh(report)
            return report

    async def xǁReportRepositoryǁupdate__mutmut_2(self, id: str, data: dict[str, Any]) -> Report | None:
        """
        Update report

        Args:
            id: Report UUID
            data: Updated data dictionary

        Returns:
            Updated Report instance or None
        """
        async with await self.adapter.get_session() as session:
            report = await self.find_by_id(None, include_deleted=True)
            if not report:
                return None

            for key, value in data.items():
                if hasattr(report, key):
                    setattr(report, key, value)

            session.add(report)
            await session.commit()
            await session.refresh(report)
            return report

    async def xǁReportRepositoryǁupdate__mutmut_3(self, id: str, data: dict[str, Any]) -> Report | None:
        """
        Update report

        Args:
            id: Report UUID
            data: Updated data dictionary

        Returns:
            Updated Report instance or None
        """
        async with await self.adapter.get_session() as session:
            report = await self.find_by_id(id, include_deleted=None)
            if not report:
                return None

            for key, value in data.items():
                if hasattr(report, key):
                    setattr(report, key, value)

            session.add(report)
            await session.commit()
            await session.refresh(report)
            return report

    async def xǁReportRepositoryǁupdate__mutmut_4(self, id: str, data: dict[str, Any]) -> Report | None:
        """
        Update report

        Args:
            id: Report UUID
            data: Updated data dictionary

        Returns:
            Updated Report instance or None
        """
        async with await self.adapter.get_session() as session:
            report = await self.find_by_id(include_deleted=True)
            if not report:
                return None

            for key, value in data.items():
                if hasattr(report, key):
                    setattr(report, key, value)

            session.add(report)
            await session.commit()
            await session.refresh(report)
            return report

    async def xǁReportRepositoryǁupdate__mutmut_5(self, id: str, data: dict[str, Any]) -> Report | None:
        """
        Update report

        Args:
            id: Report UUID
            data: Updated data dictionary

        Returns:
            Updated Report instance or None
        """
        async with await self.adapter.get_session() as session:
            report = await self.find_by_id(id, )
            if not report:
                return None

            for key, value in data.items():
                if hasattr(report, key):
                    setattr(report, key, value)

            session.add(report)
            await session.commit()
            await session.refresh(report)
            return report

    async def xǁReportRepositoryǁupdate__mutmut_6(self, id: str, data: dict[str, Any]) -> Report | None:
        """
        Update report

        Args:
            id: Report UUID
            data: Updated data dictionary

        Returns:
            Updated Report instance or None
        """
        async with await self.adapter.get_session() as session:
            report = await self.find_by_id(id, include_deleted=False)
            if not report:
                return None

            for key, value in data.items():
                if hasattr(report, key):
                    setattr(report, key, value)

            session.add(report)
            await session.commit()
            await session.refresh(report)
            return report

    async def xǁReportRepositoryǁupdate__mutmut_7(self, id: str, data: dict[str, Any]) -> Report | None:
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
            if report:
                return None

            for key, value in data.items():
                if hasattr(report, key):
                    setattr(report, key, value)

            session.add(report)
            await session.commit()
            await session.refresh(report)
            return report

    async def xǁReportRepositoryǁupdate__mutmut_8(self, id: str, data: dict[str, Any]) -> Report | None:
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
                if hasattr(None, key):
                    setattr(report, key, value)

            session.add(report)
            await session.commit()
            await session.refresh(report)
            return report

    async def xǁReportRepositoryǁupdate__mutmut_9(self, id: str, data: dict[str, Any]) -> Report | None:
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
                if hasattr(report, None):
                    setattr(report, key, value)

            session.add(report)
            await session.commit()
            await session.refresh(report)
            return report

    async def xǁReportRepositoryǁupdate__mutmut_10(self, id: str, data: dict[str, Any]) -> Report | None:
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
                if hasattr(key):
                    setattr(report, key, value)

            session.add(report)
            await session.commit()
            await session.refresh(report)
            return report

    async def xǁReportRepositoryǁupdate__mutmut_11(self, id: str, data: dict[str, Any]) -> Report | None:
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
                if hasattr(report, ):
                    setattr(report, key, value)

            session.add(report)
            await session.commit()
            await session.refresh(report)
            return report

    async def xǁReportRepositoryǁupdate__mutmut_12(self, id: str, data: dict[str, Any]) -> Report | None:
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
                    setattr(None, key, value)

            session.add(report)
            await session.commit()
            await session.refresh(report)
            return report

    async def xǁReportRepositoryǁupdate__mutmut_13(self, id: str, data: dict[str, Any]) -> Report | None:
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
                    setattr(report, None, value)

            session.add(report)
            await session.commit()
            await session.refresh(report)
            return report

    async def xǁReportRepositoryǁupdate__mutmut_14(self, id: str, data: dict[str, Any]) -> Report | None:
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
                    setattr(report, key, None)

            session.add(report)
            await session.commit()
            await session.refresh(report)
            return report

    async def xǁReportRepositoryǁupdate__mutmut_15(self, id: str, data: dict[str, Any]) -> Report | None:
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
                    setattr(key, value)

            session.add(report)
            await session.commit()
            await session.refresh(report)
            return report

    async def xǁReportRepositoryǁupdate__mutmut_16(self, id: str, data: dict[str, Any]) -> Report | None:
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
                    setattr(report, value)

            session.add(report)
            await session.commit()
            await session.refresh(report)
            return report

    async def xǁReportRepositoryǁupdate__mutmut_17(self, id: str, data: dict[str, Any]) -> Report | None:
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
                    setattr(report, key, )

            session.add(report)
            await session.commit()
            await session.refresh(report)
            return report

    async def xǁReportRepositoryǁupdate__mutmut_18(self, id: str, data: dict[str, Any]) -> Report | None:
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

            session.add(None)
            await session.commit()
            await session.refresh(report)
            return report

    async def xǁReportRepositoryǁupdate__mutmut_19(self, id: str, data: dict[str, Any]) -> Report | None:
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
            await session.refresh(None)
            return report
    
    xǁReportRepositoryǁupdate__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁReportRepositoryǁupdate__mutmut_1': xǁReportRepositoryǁupdate__mutmut_1, 
        'xǁReportRepositoryǁupdate__mutmut_2': xǁReportRepositoryǁupdate__mutmut_2, 
        'xǁReportRepositoryǁupdate__mutmut_3': xǁReportRepositoryǁupdate__mutmut_3, 
        'xǁReportRepositoryǁupdate__mutmut_4': xǁReportRepositoryǁupdate__mutmut_4, 
        'xǁReportRepositoryǁupdate__mutmut_5': xǁReportRepositoryǁupdate__mutmut_5, 
        'xǁReportRepositoryǁupdate__mutmut_6': xǁReportRepositoryǁupdate__mutmut_6, 
        'xǁReportRepositoryǁupdate__mutmut_7': xǁReportRepositoryǁupdate__mutmut_7, 
        'xǁReportRepositoryǁupdate__mutmut_8': xǁReportRepositoryǁupdate__mutmut_8, 
        'xǁReportRepositoryǁupdate__mutmut_9': xǁReportRepositoryǁupdate__mutmut_9, 
        'xǁReportRepositoryǁupdate__mutmut_10': xǁReportRepositoryǁupdate__mutmut_10, 
        'xǁReportRepositoryǁupdate__mutmut_11': xǁReportRepositoryǁupdate__mutmut_11, 
        'xǁReportRepositoryǁupdate__mutmut_12': xǁReportRepositoryǁupdate__mutmut_12, 
        'xǁReportRepositoryǁupdate__mutmut_13': xǁReportRepositoryǁupdate__mutmut_13, 
        'xǁReportRepositoryǁupdate__mutmut_14': xǁReportRepositoryǁupdate__mutmut_14, 
        'xǁReportRepositoryǁupdate__mutmut_15': xǁReportRepositoryǁupdate__mutmut_15, 
        'xǁReportRepositoryǁupdate__mutmut_16': xǁReportRepositoryǁupdate__mutmut_16, 
        'xǁReportRepositoryǁupdate__mutmut_17': xǁReportRepositoryǁupdate__mutmut_17, 
        'xǁReportRepositoryǁupdate__mutmut_18': xǁReportRepositoryǁupdate__mutmut_18, 
        'xǁReportRepositoryǁupdate__mutmut_19': xǁReportRepositoryǁupdate__mutmut_19
    }
    
    def update(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁReportRepositoryǁupdate__mutmut_orig"), object.__getattribute__(self, "xǁReportRepositoryǁupdate__mutmut_mutants"), args, kwargs, self)
        return result 
    
    update.__signature__ = _mutmut_signature(xǁReportRepositoryǁupdate__mutmut_orig)
    xǁReportRepositoryǁupdate__mutmut_orig.__name__ = 'xǁReportRepositoryǁupdate'

    async def xǁReportRepositoryǁsoft_delete__mutmut_orig(self, id: str) -> Report | None:
        """
        Soft delete report (set status to EXPIRED)

        Args:
            id: Report UUID

        Returns:
            Updated Report instance or None
        """
        return await self.update(id, {"status": ReportStatus.EXPIRED})

    async def xǁReportRepositoryǁsoft_delete__mutmut_1(self, id: str) -> Report | None:
        """
        Soft delete report (set status to EXPIRED)

        Args:
            id: Report UUID

        Returns:
            Updated Report instance or None
        """
        return await self.update(None, {"status": ReportStatus.EXPIRED})

    async def xǁReportRepositoryǁsoft_delete__mutmut_2(self, id: str) -> Report | None:
        """
        Soft delete report (set status to EXPIRED)

        Args:
            id: Report UUID

        Returns:
            Updated Report instance or None
        """
        return await self.update(id, None)

    async def xǁReportRepositoryǁsoft_delete__mutmut_3(self, id: str) -> Report | None:
        """
        Soft delete report (set status to EXPIRED)

        Args:
            id: Report UUID

        Returns:
            Updated Report instance or None
        """
        return await self.update({"status": ReportStatus.EXPIRED})

    async def xǁReportRepositoryǁsoft_delete__mutmut_4(self, id: str) -> Report | None:
        """
        Soft delete report (set status to EXPIRED)

        Args:
            id: Report UUID

        Returns:
            Updated Report instance or None
        """
        return await self.update(id, )

    async def xǁReportRepositoryǁsoft_delete__mutmut_5(self, id: str) -> Report | None:
        """
        Soft delete report (set status to EXPIRED)

        Args:
            id: Report UUID

        Returns:
            Updated Report instance or None
        """
        return await self.update(id, {"XXstatusXX": ReportStatus.EXPIRED})

    async def xǁReportRepositoryǁsoft_delete__mutmut_6(self, id: str) -> Report | None:
        """
        Soft delete report (set status to EXPIRED)

        Args:
            id: Report UUID

        Returns:
            Updated Report instance or None
        """
        return await self.update(id, {"STATUS": ReportStatus.EXPIRED})
    
    xǁReportRepositoryǁsoft_delete__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁReportRepositoryǁsoft_delete__mutmut_1': xǁReportRepositoryǁsoft_delete__mutmut_1, 
        'xǁReportRepositoryǁsoft_delete__mutmut_2': xǁReportRepositoryǁsoft_delete__mutmut_2, 
        'xǁReportRepositoryǁsoft_delete__mutmut_3': xǁReportRepositoryǁsoft_delete__mutmut_3, 
        'xǁReportRepositoryǁsoft_delete__mutmut_4': xǁReportRepositoryǁsoft_delete__mutmut_4, 
        'xǁReportRepositoryǁsoft_delete__mutmut_5': xǁReportRepositoryǁsoft_delete__mutmut_5, 
        'xǁReportRepositoryǁsoft_delete__mutmut_6': xǁReportRepositoryǁsoft_delete__mutmut_6
    }
    
    def soft_delete(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁReportRepositoryǁsoft_delete__mutmut_orig"), object.__getattribute__(self, "xǁReportRepositoryǁsoft_delete__mutmut_mutants"), args, kwargs, self)
        return result 
    
    soft_delete.__signature__ = _mutmut_signature(xǁReportRepositoryǁsoft_delete__mutmut_orig)
    xǁReportRepositoryǁsoft_delete__mutmut_orig.__name__ = 'xǁReportRepositoryǁsoft_delete'

    async def xǁReportRepositoryǁhard_delete__mutmut_orig(self, id: str) -> bool:
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

    async def xǁReportRepositoryǁhard_delete__mutmut_1(self, id: str) -> bool:
        """
        Hard delete report (permanent)

        Args:
            id: Report UUID

        Returns:
            True if deleted, False otherwise
        """
        async with await self.adapter.get_session() as session:
            report = None
            if not report:
                return False

            await session.delete(report)
            await session.commit()
            return True

    async def xǁReportRepositoryǁhard_delete__mutmut_2(self, id: str) -> bool:
        """
        Hard delete report (permanent)

        Args:
            id: Report UUID

        Returns:
            True if deleted, False otherwise
        """
        async with await self.adapter.get_session() as session:
            report = await self.find_by_id(None, include_deleted=True)
            if not report:
                return False

            await session.delete(report)
            await session.commit()
            return True

    async def xǁReportRepositoryǁhard_delete__mutmut_3(self, id: str) -> bool:
        """
        Hard delete report (permanent)

        Args:
            id: Report UUID

        Returns:
            True if deleted, False otherwise
        """
        async with await self.adapter.get_session() as session:
            report = await self.find_by_id(id, include_deleted=None)
            if not report:
                return False

            await session.delete(report)
            await session.commit()
            return True

    async def xǁReportRepositoryǁhard_delete__mutmut_4(self, id: str) -> bool:
        """
        Hard delete report (permanent)

        Args:
            id: Report UUID

        Returns:
            True if deleted, False otherwise
        """
        async with await self.adapter.get_session() as session:
            report = await self.find_by_id(include_deleted=True)
            if not report:
                return False

            await session.delete(report)
            await session.commit()
            return True

    async def xǁReportRepositoryǁhard_delete__mutmut_5(self, id: str) -> bool:
        """
        Hard delete report (permanent)

        Args:
            id: Report UUID

        Returns:
            True if deleted, False otherwise
        """
        async with await self.adapter.get_session() as session:
            report = await self.find_by_id(id, )
            if not report:
                return False

            await session.delete(report)
            await session.commit()
            return True

    async def xǁReportRepositoryǁhard_delete__mutmut_6(self, id: str) -> bool:
        """
        Hard delete report (permanent)

        Args:
            id: Report UUID

        Returns:
            True if deleted, False otherwise
        """
        async with await self.adapter.get_session() as session:
            report = await self.find_by_id(id, include_deleted=False)
            if not report:
                return False

            await session.delete(report)
            await session.commit()
            return True

    async def xǁReportRepositoryǁhard_delete__mutmut_7(self, id: str) -> bool:
        """
        Hard delete report (permanent)

        Args:
            id: Report UUID

        Returns:
            True if deleted, False otherwise
        """
        async with await self.adapter.get_session() as session:
            report = await self.find_by_id(id, include_deleted=True)
            if report:
                return False

            await session.delete(report)
            await session.commit()
            return True

    async def xǁReportRepositoryǁhard_delete__mutmut_8(self, id: str) -> bool:
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
                return True

            await session.delete(report)
            await session.commit()
            return True

    async def xǁReportRepositoryǁhard_delete__mutmut_9(self, id: str) -> bool:
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

            await session.delete(None)
            await session.commit()
            return True

    async def xǁReportRepositoryǁhard_delete__mutmut_10(self, id: str) -> bool:
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
            return False
    
    xǁReportRepositoryǁhard_delete__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁReportRepositoryǁhard_delete__mutmut_1': xǁReportRepositoryǁhard_delete__mutmut_1, 
        'xǁReportRepositoryǁhard_delete__mutmut_2': xǁReportRepositoryǁhard_delete__mutmut_2, 
        'xǁReportRepositoryǁhard_delete__mutmut_3': xǁReportRepositoryǁhard_delete__mutmut_3, 
        'xǁReportRepositoryǁhard_delete__mutmut_4': xǁReportRepositoryǁhard_delete__mutmut_4, 
        'xǁReportRepositoryǁhard_delete__mutmut_5': xǁReportRepositoryǁhard_delete__mutmut_5, 
        'xǁReportRepositoryǁhard_delete__mutmut_6': xǁReportRepositoryǁhard_delete__mutmut_6, 
        'xǁReportRepositoryǁhard_delete__mutmut_7': xǁReportRepositoryǁhard_delete__mutmut_7, 
        'xǁReportRepositoryǁhard_delete__mutmut_8': xǁReportRepositoryǁhard_delete__mutmut_8, 
        'xǁReportRepositoryǁhard_delete__mutmut_9': xǁReportRepositoryǁhard_delete__mutmut_9, 
        'xǁReportRepositoryǁhard_delete__mutmut_10': xǁReportRepositoryǁhard_delete__mutmut_10
    }
    
    def hard_delete(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁReportRepositoryǁhard_delete__mutmut_orig"), object.__getattribute__(self, "xǁReportRepositoryǁhard_delete__mutmut_mutants"), args, kwargs, self)
        return result 
    
    hard_delete.__signature__ = _mutmut_signature(xǁReportRepositoryǁhard_delete__mutmut_orig)
    xǁReportRepositoryǁhard_delete__mutmut_orig.__name__ = 'xǁReportRepositoryǁhard_delete'

    async def xǁReportRepositoryǁrestore__mutmut_orig(self, id: str) -> Report | None:
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

    async def xǁReportRepositoryǁrestore__mutmut_1(self, id: str) -> Report | None:
        """
        Restore soft-deleted report (set status back to COMPLETED)

        Args:
            id: Report UUID

        Returns:
            Restored Report instance or None
        """
        report = None
        if not report or report.status != ReportStatus.EXPIRED:
            return None

        return await self.update(id, {"status": ReportStatus.COMPLETED})

    async def xǁReportRepositoryǁrestore__mutmut_2(self, id: str) -> Report | None:
        """
        Restore soft-deleted report (set status back to COMPLETED)

        Args:
            id: Report UUID

        Returns:
            Restored Report instance or None
        """
        report = await self.find_by_id(None, include_deleted=True)
        if not report or report.status != ReportStatus.EXPIRED:
            return None

        return await self.update(id, {"status": ReportStatus.COMPLETED})

    async def xǁReportRepositoryǁrestore__mutmut_3(self, id: str) -> Report | None:
        """
        Restore soft-deleted report (set status back to COMPLETED)

        Args:
            id: Report UUID

        Returns:
            Restored Report instance or None
        """
        report = await self.find_by_id(id, include_deleted=None)
        if not report or report.status != ReportStatus.EXPIRED:
            return None

        return await self.update(id, {"status": ReportStatus.COMPLETED})

    async def xǁReportRepositoryǁrestore__mutmut_4(self, id: str) -> Report | None:
        """
        Restore soft-deleted report (set status back to COMPLETED)

        Args:
            id: Report UUID

        Returns:
            Restored Report instance or None
        """
        report = await self.find_by_id(include_deleted=True)
        if not report or report.status != ReportStatus.EXPIRED:
            return None

        return await self.update(id, {"status": ReportStatus.COMPLETED})

    async def xǁReportRepositoryǁrestore__mutmut_5(self, id: str) -> Report | None:
        """
        Restore soft-deleted report (set status back to COMPLETED)

        Args:
            id: Report UUID

        Returns:
            Restored Report instance or None
        """
        report = await self.find_by_id(id, )
        if not report or report.status != ReportStatus.EXPIRED:
            return None

        return await self.update(id, {"status": ReportStatus.COMPLETED})

    async def xǁReportRepositoryǁrestore__mutmut_6(self, id: str) -> Report | None:
        """
        Restore soft-deleted report (set status back to COMPLETED)

        Args:
            id: Report UUID

        Returns:
            Restored Report instance or None
        """
        report = await self.find_by_id(id, include_deleted=False)
        if not report or report.status != ReportStatus.EXPIRED:
            return None

        return await self.update(id, {"status": ReportStatus.COMPLETED})

    async def xǁReportRepositoryǁrestore__mutmut_7(self, id: str) -> Report | None:
        """
        Restore soft-deleted report (set status back to COMPLETED)

        Args:
            id: Report UUID

        Returns:
            Restored Report instance or None
        """
        report = await self.find_by_id(id, include_deleted=True)
        if not report and report.status != ReportStatus.EXPIRED:
            return None

        return await self.update(id, {"status": ReportStatus.COMPLETED})

    async def xǁReportRepositoryǁrestore__mutmut_8(self, id: str) -> Report | None:
        """
        Restore soft-deleted report (set status back to COMPLETED)

        Args:
            id: Report UUID

        Returns:
            Restored Report instance or None
        """
        report = await self.find_by_id(id, include_deleted=True)
        if report or report.status != ReportStatus.EXPIRED:
            return None

        return await self.update(id, {"status": ReportStatus.COMPLETED})

    async def xǁReportRepositoryǁrestore__mutmut_9(self, id: str) -> Report | None:
        """
        Restore soft-deleted report (set status back to COMPLETED)

        Args:
            id: Report UUID

        Returns:
            Restored Report instance or None
        """
        report = await self.find_by_id(id, include_deleted=True)
        if not report or report.status == ReportStatus.EXPIRED:
            return None

        return await self.update(id, {"status": ReportStatus.COMPLETED})

    async def xǁReportRepositoryǁrestore__mutmut_10(self, id: str) -> Report | None:
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

        return await self.update(None, {"status": ReportStatus.COMPLETED})

    async def xǁReportRepositoryǁrestore__mutmut_11(self, id: str) -> Report | None:
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

        return await self.update(id, None)

    async def xǁReportRepositoryǁrestore__mutmut_12(self, id: str) -> Report | None:
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

        return await self.update({"status": ReportStatus.COMPLETED})

    async def xǁReportRepositoryǁrestore__mutmut_13(self, id: str) -> Report | None:
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

        return await self.update(id, )

    async def xǁReportRepositoryǁrestore__mutmut_14(self, id: str) -> Report | None:
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

        return await self.update(id, {"XXstatusXX": ReportStatus.COMPLETED})

    async def xǁReportRepositoryǁrestore__mutmut_15(self, id: str) -> Report | None:
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

        return await self.update(id, {"STATUS": ReportStatus.COMPLETED})
    
    xǁReportRepositoryǁrestore__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁReportRepositoryǁrestore__mutmut_1': xǁReportRepositoryǁrestore__mutmut_1, 
        'xǁReportRepositoryǁrestore__mutmut_2': xǁReportRepositoryǁrestore__mutmut_2, 
        'xǁReportRepositoryǁrestore__mutmut_3': xǁReportRepositoryǁrestore__mutmut_3, 
        'xǁReportRepositoryǁrestore__mutmut_4': xǁReportRepositoryǁrestore__mutmut_4, 
        'xǁReportRepositoryǁrestore__mutmut_5': xǁReportRepositoryǁrestore__mutmut_5, 
        'xǁReportRepositoryǁrestore__mutmut_6': xǁReportRepositoryǁrestore__mutmut_6, 
        'xǁReportRepositoryǁrestore__mutmut_7': xǁReportRepositoryǁrestore__mutmut_7, 
        'xǁReportRepositoryǁrestore__mutmut_8': xǁReportRepositoryǁrestore__mutmut_8, 
        'xǁReportRepositoryǁrestore__mutmut_9': xǁReportRepositoryǁrestore__mutmut_9, 
        'xǁReportRepositoryǁrestore__mutmut_10': xǁReportRepositoryǁrestore__mutmut_10, 
        'xǁReportRepositoryǁrestore__mutmut_11': xǁReportRepositoryǁrestore__mutmut_11, 
        'xǁReportRepositoryǁrestore__mutmut_12': xǁReportRepositoryǁrestore__mutmut_12, 
        'xǁReportRepositoryǁrestore__mutmut_13': xǁReportRepositoryǁrestore__mutmut_13, 
        'xǁReportRepositoryǁrestore__mutmut_14': xǁReportRepositoryǁrestore__mutmut_14, 
        'xǁReportRepositoryǁrestore__mutmut_15': xǁReportRepositoryǁrestore__mutmut_15
    }
    
    def restore(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁReportRepositoryǁrestore__mutmut_orig"), object.__getattribute__(self, "xǁReportRepositoryǁrestore__mutmut_mutants"), args, kwargs, self)
        return result 
    
    restore.__signature__ = _mutmut_signature(xǁReportRepositoryǁrestore__mutmut_orig)
    xǁReportRepositoryǁrestore__mutmut_orig.__name__ = 'xǁReportRepositoryǁrestore'

    async def xǁReportRepositoryǁexpire_old_reports__mutmut_orig(self) -> int:
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

    async def xǁReportRepositoryǁexpire_old_reports__mutmut_1(self) -> int:
        """
        Expire reports past their expires_at date

        Returns:
            Number of reports expired
        """
        async with await self.adapter.get_session() as session:
            query = None

            result = await session.execute(query)
            reports = list(result.scalars().all())

            for report in reports:
                report.status = ReportStatus.EXPIRED

            await session.commit()
            return len(reports)

    async def xǁReportRepositoryǁexpire_old_reports__mutmut_2(self) -> int:
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
                    None
                )
            )

            result = await session.execute(query)
            reports = list(result.scalars().all())

            for report in reports:
                report.status = ReportStatus.EXPIRED

            await session.commit()
            return len(reports)

    async def xǁReportRepositoryǁexpire_old_reports__mutmut_3(self) -> int:
        """
        Expire reports past their expires_at date

        Returns:
            Number of reports expired
        """
        async with await self.adapter.get_session() as session:
            query = (
                select(Report)
                .where(None)
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

    async def xǁReportRepositoryǁexpire_old_reports__mutmut_4(self) -> int:
        """
        Expire reports past their expires_at date

        Returns:
            Number of reports expired
        """
        async with await self.adapter.get_session() as session:
            query = (
                select(None)
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

    async def xǁReportRepositoryǁexpire_old_reports__mutmut_5(self) -> int:
        """
        Expire reports past their expires_at date

        Returns:
            Number of reports expired
        """
        async with await self.adapter.get_session() as session:
            query = (
                select(Report)
                .where(Report.expires_at <= datetime.utcnow())
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

    async def xǁReportRepositoryǁexpire_old_reports__mutmut_6(self) -> int:
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
                        None
                    )
                )
            )

            result = await session.execute(query)
            reports = list(result.scalars().all())

            for report in reports:
                report.status = ReportStatus.EXPIRED

            await session.commit()
            return len(reports)

    async def xǁReportRepositoryǁexpire_old_reports__mutmut_7(self) -> int:
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

            result = None
            reports = list(result.scalars().all())

            for report in reports:
                report.status = ReportStatus.EXPIRED

            await session.commit()
            return len(reports)

    async def xǁReportRepositoryǁexpire_old_reports__mutmut_8(self) -> int:
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

            result = await session.execute(None)
            reports = list(result.scalars().all())

            for report in reports:
                report.status = ReportStatus.EXPIRED

            await session.commit()
            return len(reports)

    async def xǁReportRepositoryǁexpire_old_reports__mutmut_9(self) -> int:
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
            reports = None

            for report in reports:
                report.status = ReportStatus.EXPIRED

            await session.commit()
            return len(reports)

    async def xǁReportRepositoryǁexpire_old_reports__mutmut_10(self) -> int:
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
            reports = list(None)

            for report in reports:
                report.status = ReportStatus.EXPIRED

            await session.commit()
            return len(reports)

    async def xǁReportRepositoryǁexpire_old_reports__mutmut_11(self) -> int:
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
                report.status = None

            await session.commit()
            return len(reports)
    
    xǁReportRepositoryǁexpire_old_reports__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁReportRepositoryǁexpire_old_reports__mutmut_1': xǁReportRepositoryǁexpire_old_reports__mutmut_1, 
        'xǁReportRepositoryǁexpire_old_reports__mutmut_2': xǁReportRepositoryǁexpire_old_reports__mutmut_2, 
        'xǁReportRepositoryǁexpire_old_reports__mutmut_3': xǁReportRepositoryǁexpire_old_reports__mutmut_3, 
        'xǁReportRepositoryǁexpire_old_reports__mutmut_4': xǁReportRepositoryǁexpire_old_reports__mutmut_4, 
        'xǁReportRepositoryǁexpire_old_reports__mutmut_5': xǁReportRepositoryǁexpire_old_reports__mutmut_5, 
        'xǁReportRepositoryǁexpire_old_reports__mutmut_6': xǁReportRepositoryǁexpire_old_reports__mutmut_6, 
        'xǁReportRepositoryǁexpire_old_reports__mutmut_7': xǁReportRepositoryǁexpire_old_reports__mutmut_7, 
        'xǁReportRepositoryǁexpire_old_reports__mutmut_8': xǁReportRepositoryǁexpire_old_reports__mutmut_8, 
        'xǁReportRepositoryǁexpire_old_reports__mutmut_9': xǁReportRepositoryǁexpire_old_reports__mutmut_9, 
        'xǁReportRepositoryǁexpire_old_reports__mutmut_10': xǁReportRepositoryǁexpire_old_reports__mutmut_10, 
        'xǁReportRepositoryǁexpire_old_reports__mutmut_11': xǁReportRepositoryǁexpire_old_reports__mutmut_11
    }
    
    def expire_old_reports(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁReportRepositoryǁexpire_old_reports__mutmut_orig"), object.__getattribute__(self, "xǁReportRepositoryǁexpire_old_reports__mutmut_mutants"), args, kwargs, self)
        return result 
    
    expire_old_reports.__signature__ = _mutmut_signature(xǁReportRepositoryǁexpire_old_reports__mutmut_orig)
    xǁReportRepositoryǁexpire_old_reports__mutmut_orig.__name__ = 'xǁReportRepositoryǁexpire_old_reports'

    async def xǁReportRepositoryǁdelete_expired_reports__mutmut_orig(self) -> int:
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

    async def xǁReportRepositoryǁdelete_expired_reports__mutmut_1(self) -> int:
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
            cutoff_date = None

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

    async def xǁReportRepositoryǁdelete_expired_reports__mutmut_2(self) -> int:
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
            cutoff_date = datetime.utcnow() + timedelta(days=90)

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

    async def xǁReportRepositoryǁdelete_expired_reports__mutmut_3(self) -> int:
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
            cutoff_date = datetime.utcnow() - timedelta(days=None)

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

    async def xǁReportRepositoryǁdelete_expired_reports__mutmut_4(self) -> int:
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
            cutoff_date = datetime.utcnow() - timedelta(days=91)

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

    async def xǁReportRepositoryǁdelete_expired_reports__mutmut_5(self) -> int:
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
            query = None

            result = await session.execute(query)
            reports = list(result.scalars().all())

            # Hard delete all matching reports
            for report in reports:
                await session.delete(report)

            await session.commit()
            return len(reports)

    async def xǁReportRepositoryǁdelete_expired_reports__mutmut_6(self) -> int:
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
                .where(None)
            )

            result = await session.execute(query)
            reports = list(result.scalars().all())

            # Hard delete all matching reports
            for report in reports:
                await session.delete(report)

            await session.commit()
            return len(reports)

    async def xǁReportRepositoryǁdelete_expired_reports__mutmut_7(self) -> int:
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
                .where(None)
                .where(Report.expires_at < cutoff_date)
            )

            result = await session.execute(query)
            reports = list(result.scalars().all())

            # Hard delete all matching reports
            for report in reports:
                await session.delete(report)

            await session.commit()
            return len(reports)

    async def xǁReportRepositoryǁdelete_expired_reports__mutmut_8(self) -> int:
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
                select(None)
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

    async def xǁReportRepositoryǁdelete_expired_reports__mutmut_9(self) -> int:
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
                .where(Report.status != ReportStatus.EXPIRED)
                .where(Report.expires_at < cutoff_date)
            )

            result = await session.execute(query)
            reports = list(result.scalars().all())

            # Hard delete all matching reports
            for report in reports:
                await session.delete(report)

            await session.commit()
            return len(reports)

    async def xǁReportRepositoryǁdelete_expired_reports__mutmut_10(self) -> int:
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
                .where(Report.expires_at <= cutoff_date)
            )

            result = await session.execute(query)
            reports = list(result.scalars().all())

            # Hard delete all matching reports
            for report in reports:
                await session.delete(report)

            await session.commit()
            return len(reports)

    async def xǁReportRepositoryǁdelete_expired_reports__mutmut_11(self) -> int:
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

            result = None
            reports = list(result.scalars().all())

            # Hard delete all matching reports
            for report in reports:
                await session.delete(report)

            await session.commit()
            return len(reports)

    async def xǁReportRepositoryǁdelete_expired_reports__mutmut_12(self) -> int:
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

            result = await session.execute(None)
            reports = list(result.scalars().all())

            # Hard delete all matching reports
            for report in reports:
                await session.delete(report)

            await session.commit()
            return len(reports)

    async def xǁReportRepositoryǁdelete_expired_reports__mutmut_13(self) -> int:
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
            reports = None

            # Hard delete all matching reports
            for report in reports:
                await session.delete(report)

            await session.commit()
            return len(reports)

    async def xǁReportRepositoryǁdelete_expired_reports__mutmut_14(self) -> int:
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
            reports = list(None)

            # Hard delete all matching reports
            for report in reports:
                await session.delete(report)

            await session.commit()
            return len(reports)

    async def xǁReportRepositoryǁdelete_expired_reports__mutmut_15(self) -> int:
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
                await session.delete(None)

            await session.commit()
            return len(reports)
    
    xǁReportRepositoryǁdelete_expired_reports__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁReportRepositoryǁdelete_expired_reports__mutmut_1': xǁReportRepositoryǁdelete_expired_reports__mutmut_1, 
        'xǁReportRepositoryǁdelete_expired_reports__mutmut_2': xǁReportRepositoryǁdelete_expired_reports__mutmut_2, 
        'xǁReportRepositoryǁdelete_expired_reports__mutmut_3': xǁReportRepositoryǁdelete_expired_reports__mutmut_3, 
        'xǁReportRepositoryǁdelete_expired_reports__mutmut_4': xǁReportRepositoryǁdelete_expired_reports__mutmut_4, 
        'xǁReportRepositoryǁdelete_expired_reports__mutmut_5': xǁReportRepositoryǁdelete_expired_reports__mutmut_5, 
        'xǁReportRepositoryǁdelete_expired_reports__mutmut_6': xǁReportRepositoryǁdelete_expired_reports__mutmut_6, 
        'xǁReportRepositoryǁdelete_expired_reports__mutmut_7': xǁReportRepositoryǁdelete_expired_reports__mutmut_7, 
        'xǁReportRepositoryǁdelete_expired_reports__mutmut_8': xǁReportRepositoryǁdelete_expired_reports__mutmut_8, 
        'xǁReportRepositoryǁdelete_expired_reports__mutmut_9': xǁReportRepositoryǁdelete_expired_reports__mutmut_9, 
        'xǁReportRepositoryǁdelete_expired_reports__mutmut_10': xǁReportRepositoryǁdelete_expired_reports__mutmut_10, 
        'xǁReportRepositoryǁdelete_expired_reports__mutmut_11': xǁReportRepositoryǁdelete_expired_reports__mutmut_11, 
        'xǁReportRepositoryǁdelete_expired_reports__mutmut_12': xǁReportRepositoryǁdelete_expired_reports__mutmut_12, 
        'xǁReportRepositoryǁdelete_expired_reports__mutmut_13': xǁReportRepositoryǁdelete_expired_reports__mutmut_13, 
        'xǁReportRepositoryǁdelete_expired_reports__mutmut_14': xǁReportRepositoryǁdelete_expired_reports__mutmut_14, 
        'xǁReportRepositoryǁdelete_expired_reports__mutmut_15': xǁReportRepositoryǁdelete_expired_reports__mutmut_15
    }
    
    def delete_expired_reports(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁReportRepositoryǁdelete_expired_reports__mutmut_orig"), object.__getattribute__(self, "xǁReportRepositoryǁdelete_expired_reports__mutmut_mutants"), args, kwargs, self)
        return result 
    
    delete_expired_reports.__signature__ = _mutmut_signature(xǁReportRepositoryǁdelete_expired_reports__mutmut_orig)
    xǁReportRepositoryǁdelete_expired_reports__mutmut_orig.__name__ = 'xǁReportRepositoryǁdelete_expired_reports'
