"""
SLA Monitoring Service
Tracks streaming response latency and calculates percentiles (p50/p95/p99)
Per requirements T172a-c
"""

import time
from typing import List, Dict, Any
from collections import deque
from dataclasses import dataclass, field
from logging_lib.logger import get_logger

logger = get_logger()
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


@dataclass
class LatencyMetric:
    """
    Individual latency measurement
    """
    timestamp: float
    first_token_latency_ms: float
    total_latency_ms: float
    report_id: str


@dataclass
class SLAStats:
    """
    SLA statistics with percentiles
    """
    p50: float
    p95: float
    p99: float
    count: int
    violations: int  # Number of p95 > 5000ms
    last_violation_timestamp: float | None = None


class SLAMonitor:
    """
    Monitors streaming SLA performance and calculates percentiles

    Features:
    - Rolling window of last N measurements (default: 1000)
    - Percentile calculation (p50/p95/p99)
    - SLA violation detection (p95 > 5s)
    - Automated alerts

    Thread-safe for concurrent requests.
    """

    def xǁSLAMonitorǁ__init____mutmut_orig(self, window_size: int = 1000, sla_threshold_ms: float = 5000):
        """
        Initialize SLA monitor

        Args:
            window_size: Number of recent measurements to track
            sla_threshold_ms: p95 threshold in milliseconds (default: 5000ms = 5s)
        """
        self.window_size = window_size
        self.sla_threshold_ms = sla_threshold_ms
        self.metrics: deque[LatencyMetric] = deque(maxlen=window_size)
        self._violation_count = 0

    def xǁSLAMonitorǁ__init____mutmut_1(self, window_size: int = 1001, sla_threshold_ms: float = 5000):
        """
        Initialize SLA monitor

        Args:
            window_size: Number of recent measurements to track
            sla_threshold_ms: p95 threshold in milliseconds (default: 5000ms = 5s)
        """
        self.window_size = window_size
        self.sla_threshold_ms = sla_threshold_ms
        self.metrics: deque[LatencyMetric] = deque(maxlen=window_size)
        self._violation_count = 0

    def xǁSLAMonitorǁ__init____mutmut_2(self, window_size: int = 1000, sla_threshold_ms: float = 5001):
        """
        Initialize SLA monitor

        Args:
            window_size: Number of recent measurements to track
            sla_threshold_ms: p95 threshold in milliseconds (default: 5000ms = 5s)
        """
        self.window_size = window_size
        self.sla_threshold_ms = sla_threshold_ms
        self.metrics: deque[LatencyMetric] = deque(maxlen=window_size)
        self._violation_count = 0

    def xǁSLAMonitorǁ__init____mutmut_3(self, window_size: int = 1000, sla_threshold_ms: float = 5000):
        """
        Initialize SLA monitor

        Args:
            window_size: Number of recent measurements to track
            sla_threshold_ms: p95 threshold in milliseconds (default: 5000ms = 5s)
        """
        self.window_size = None
        self.sla_threshold_ms = sla_threshold_ms
        self.metrics: deque[LatencyMetric] = deque(maxlen=window_size)
        self._violation_count = 0

    def xǁSLAMonitorǁ__init____mutmut_4(self, window_size: int = 1000, sla_threshold_ms: float = 5000):
        """
        Initialize SLA monitor

        Args:
            window_size: Number of recent measurements to track
            sla_threshold_ms: p95 threshold in milliseconds (default: 5000ms = 5s)
        """
        self.window_size = window_size
        self.sla_threshold_ms = None
        self.metrics: deque[LatencyMetric] = deque(maxlen=window_size)
        self._violation_count = 0

    def xǁSLAMonitorǁ__init____mutmut_5(self, window_size: int = 1000, sla_threshold_ms: float = 5000):
        """
        Initialize SLA monitor

        Args:
            window_size: Number of recent measurements to track
            sla_threshold_ms: p95 threshold in milliseconds (default: 5000ms = 5s)
        """
        self.window_size = window_size
        self.sla_threshold_ms = sla_threshold_ms
        self.metrics: deque[LatencyMetric] = None
        self._violation_count = 0

    def xǁSLAMonitorǁ__init____mutmut_6(self, window_size: int = 1000, sla_threshold_ms: float = 5000):
        """
        Initialize SLA monitor

        Args:
            window_size: Number of recent measurements to track
            sla_threshold_ms: p95 threshold in milliseconds (default: 5000ms = 5s)
        """
        self.window_size = window_size
        self.sla_threshold_ms = sla_threshold_ms
        self.metrics: deque[LatencyMetric] = deque(maxlen=None)
        self._violation_count = 0

    def xǁSLAMonitorǁ__init____mutmut_7(self, window_size: int = 1000, sla_threshold_ms: float = 5000):
        """
        Initialize SLA monitor

        Args:
            window_size: Number of recent measurements to track
            sla_threshold_ms: p95 threshold in milliseconds (default: 5000ms = 5s)
        """
        self.window_size = window_size
        self.sla_threshold_ms = sla_threshold_ms
        self.metrics: deque[LatencyMetric] = deque(maxlen=window_size)
        self._violation_count = None

    def xǁSLAMonitorǁ__init____mutmut_8(self, window_size: int = 1000, sla_threshold_ms: float = 5000):
        """
        Initialize SLA monitor

        Args:
            window_size: Number of recent measurements to track
            sla_threshold_ms: p95 threshold in milliseconds (default: 5000ms = 5s)
        """
        self.window_size = window_size
        self.sla_threshold_ms = sla_threshold_ms
        self.metrics: deque[LatencyMetric] = deque(maxlen=window_size)
        self._violation_count = 1
    
    xǁSLAMonitorǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁSLAMonitorǁ__init____mutmut_1': xǁSLAMonitorǁ__init____mutmut_1, 
        'xǁSLAMonitorǁ__init____mutmut_2': xǁSLAMonitorǁ__init____mutmut_2, 
        'xǁSLAMonitorǁ__init____mutmut_3': xǁSLAMonitorǁ__init____mutmut_3, 
        'xǁSLAMonitorǁ__init____mutmut_4': xǁSLAMonitorǁ__init____mutmut_4, 
        'xǁSLAMonitorǁ__init____mutmut_5': xǁSLAMonitorǁ__init____mutmut_5, 
        'xǁSLAMonitorǁ__init____mutmut_6': xǁSLAMonitorǁ__init____mutmut_6, 
        'xǁSLAMonitorǁ__init____mutmut_7': xǁSLAMonitorǁ__init____mutmut_7, 
        'xǁSLAMonitorǁ__init____mutmut_8': xǁSLAMonitorǁ__init____mutmut_8
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁSLAMonitorǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁSLAMonitorǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁSLAMonitorǁ__init____mutmut_orig)
    xǁSLAMonitorǁ__init____mutmut_orig.__name__ = 'xǁSLAMonitorǁ__init__'

    def xǁSLAMonitorǁrecord_streaming_latency__mutmut_orig(
        self,
        report_id: str,
        start_time: float,
        first_token_time: float | None,
        completion_time: float
    ) -> None:
        """
        Record streaming latency measurement

        Args:
            report_id: Unique report identifier
            start_time: Time when request started (time.time())
            first_token_time: Time when first token received (None if streaming failed)
            completion_time: Time when streaming completed
        """
        if first_token_time is None:
            # Streaming failed - record error
            logger.error(
                "Streaming failed - no first token received",
                {"report_id": report_id, "start_time": start_time}
            )
            return

        first_token_latency_ms = (first_token_time - start_time) * 1000
        total_latency_ms = (completion_time - start_time) * 1000

        metric = LatencyMetric(
            timestamp=completion_time,
            first_token_latency_ms=first_token_latency_ms,
            total_latency_ms=total_latency_ms,
            report_id=report_id
        )

        self.metrics.append(metric)

        # Log structured data
        logger.info(
            "Streaming latency recorded",
            {
                "report_id": report_id,
                "first_token_latency_ms": round(first_token_latency_ms, 2),
                "total_latency_ms": round(total_latency_ms, 2),
                "start_time": start_time,
                "first_token_time": first_token_time,
                "completion_time": completion_time,
            }
        )

        # Check for SLA violations
        self._check_sla_violation()

    def xǁSLAMonitorǁrecord_streaming_latency__mutmut_1(
        self,
        report_id: str,
        start_time: float,
        first_token_time: float | None,
        completion_time: float
    ) -> None:
        """
        Record streaming latency measurement

        Args:
            report_id: Unique report identifier
            start_time: Time when request started (time.time())
            first_token_time: Time when first token received (None if streaming failed)
            completion_time: Time when streaming completed
        """
        if first_token_time is not None:
            # Streaming failed - record error
            logger.error(
                "Streaming failed - no first token received",
                {"report_id": report_id, "start_time": start_time}
            )
            return

        first_token_latency_ms = (first_token_time - start_time) * 1000
        total_latency_ms = (completion_time - start_time) * 1000

        metric = LatencyMetric(
            timestamp=completion_time,
            first_token_latency_ms=first_token_latency_ms,
            total_latency_ms=total_latency_ms,
            report_id=report_id
        )

        self.metrics.append(metric)

        # Log structured data
        logger.info(
            "Streaming latency recorded",
            {
                "report_id": report_id,
                "first_token_latency_ms": round(first_token_latency_ms, 2),
                "total_latency_ms": round(total_latency_ms, 2),
                "start_time": start_time,
                "first_token_time": first_token_time,
                "completion_time": completion_time,
            }
        )

        # Check for SLA violations
        self._check_sla_violation()

    def xǁSLAMonitorǁrecord_streaming_latency__mutmut_2(
        self,
        report_id: str,
        start_time: float,
        first_token_time: float | None,
        completion_time: float
    ) -> None:
        """
        Record streaming latency measurement

        Args:
            report_id: Unique report identifier
            start_time: Time when request started (time.time())
            first_token_time: Time when first token received (None if streaming failed)
            completion_time: Time when streaming completed
        """
        if first_token_time is None:
            # Streaming failed - record error
            logger.error(
                None,
                {"report_id": report_id, "start_time": start_time}
            )
            return

        first_token_latency_ms = (first_token_time - start_time) * 1000
        total_latency_ms = (completion_time - start_time) * 1000

        metric = LatencyMetric(
            timestamp=completion_time,
            first_token_latency_ms=first_token_latency_ms,
            total_latency_ms=total_latency_ms,
            report_id=report_id
        )

        self.metrics.append(metric)

        # Log structured data
        logger.info(
            "Streaming latency recorded",
            {
                "report_id": report_id,
                "first_token_latency_ms": round(first_token_latency_ms, 2),
                "total_latency_ms": round(total_latency_ms, 2),
                "start_time": start_time,
                "first_token_time": first_token_time,
                "completion_time": completion_time,
            }
        )

        # Check for SLA violations
        self._check_sla_violation()

    def xǁSLAMonitorǁrecord_streaming_latency__mutmut_3(
        self,
        report_id: str,
        start_time: float,
        first_token_time: float | None,
        completion_time: float
    ) -> None:
        """
        Record streaming latency measurement

        Args:
            report_id: Unique report identifier
            start_time: Time when request started (time.time())
            first_token_time: Time when first token received (None if streaming failed)
            completion_time: Time when streaming completed
        """
        if first_token_time is None:
            # Streaming failed - record error
            logger.error(
                "Streaming failed - no first token received",
                None
            )
            return

        first_token_latency_ms = (first_token_time - start_time) * 1000
        total_latency_ms = (completion_time - start_time) * 1000

        metric = LatencyMetric(
            timestamp=completion_time,
            first_token_latency_ms=first_token_latency_ms,
            total_latency_ms=total_latency_ms,
            report_id=report_id
        )

        self.metrics.append(metric)

        # Log structured data
        logger.info(
            "Streaming latency recorded",
            {
                "report_id": report_id,
                "first_token_latency_ms": round(first_token_latency_ms, 2),
                "total_latency_ms": round(total_latency_ms, 2),
                "start_time": start_time,
                "first_token_time": first_token_time,
                "completion_time": completion_time,
            }
        )

        # Check for SLA violations
        self._check_sla_violation()

    def xǁSLAMonitorǁrecord_streaming_latency__mutmut_4(
        self,
        report_id: str,
        start_time: float,
        first_token_time: float | None,
        completion_time: float
    ) -> None:
        """
        Record streaming latency measurement

        Args:
            report_id: Unique report identifier
            start_time: Time when request started (time.time())
            first_token_time: Time when first token received (None if streaming failed)
            completion_time: Time when streaming completed
        """
        if first_token_time is None:
            # Streaming failed - record error
            logger.error(
                {"report_id": report_id, "start_time": start_time}
            )
            return

        first_token_latency_ms = (first_token_time - start_time) * 1000
        total_latency_ms = (completion_time - start_time) * 1000

        metric = LatencyMetric(
            timestamp=completion_time,
            first_token_latency_ms=first_token_latency_ms,
            total_latency_ms=total_latency_ms,
            report_id=report_id
        )

        self.metrics.append(metric)

        # Log structured data
        logger.info(
            "Streaming latency recorded",
            {
                "report_id": report_id,
                "first_token_latency_ms": round(first_token_latency_ms, 2),
                "total_latency_ms": round(total_latency_ms, 2),
                "start_time": start_time,
                "first_token_time": first_token_time,
                "completion_time": completion_time,
            }
        )

        # Check for SLA violations
        self._check_sla_violation()

    def xǁSLAMonitorǁrecord_streaming_latency__mutmut_5(
        self,
        report_id: str,
        start_time: float,
        first_token_time: float | None,
        completion_time: float
    ) -> None:
        """
        Record streaming latency measurement

        Args:
            report_id: Unique report identifier
            start_time: Time when request started (time.time())
            first_token_time: Time when first token received (None if streaming failed)
            completion_time: Time when streaming completed
        """
        if first_token_time is None:
            # Streaming failed - record error
            logger.error(
                "Streaming failed - no first token received",
                )
            return

        first_token_latency_ms = (first_token_time - start_time) * 1000
        total_latency_ms = (completion_time - start_time) * 1000

        metric = LatencyMetric(
            timestamp=completion_time,
            first_token_latency_ms=first_token_latency_ms,
            total_latency_ms=total_latency_ms,
            report_id=report_id
        )

        self.metrics.append(metric)

        # Log structured data
        logger.info(
            "Streaming latency recorded",
            {
                "report_id": report_id,
                "first_token_latency_ms": round(first_token_latency_ms, 2),
                "total_latency_ms": round(total_latency_ms, 2),
                "start_time": start_time,
                "first_token_time": first_token_time,
                "completion_time": completion_time,
            }
        )

        # Check for SLA violations
        self._check_sla_violation()

    def xǁSLAMonitorǁrecord_streaming_latency__mutmut_6(
        self,
        report_id: str,
        start_time: float,
        first_token_time: float | None,
        completion_time: float
    ) -> None:
        """
        Record streaming latency measurement

        Args:
            report_id: Unique report identifier
            start_time: Time when request started (time.time())
            first_token_time: Time when first token received (None if streaming failed)
            completion_time: Time when streaming completed
        """
        if first_token_time is None:
            # Streaming failed - record error
            logger.error(
                "XXStreaming failed - no first token receivedXX",
                {"report_id": report_id, "start_time": start_time}
            )
            return

        first_token_latency_ms = (first_token_time - start_time) * 1000
        total_latency_ms = (completion_time - start_time) * 1000

        metric = LatencyMetric(
            timestamp=completion_time,
            first_token_latency_ms=first_token_latency_ms,
            total_latency_ms=total_latency_ms,
            report_id=report_id
        )

        self.metrics.append(metric)

        # Log structured data
        logger.info(
            "Streaming latency recorded",
            {
                "report_id": report_id,
                "first_token_latency_ms": round(first_token_latency_ms, 2),
                "total_latency_ms": round(total_latency_ms, 2),
                "start_time": start_time,
                "first_token_time": first_token_time,
                "completion_time": completion_time,
            }
        )

        # Check for SLA violations
        self._check_sla_violation()

    def xǁSLAMonitorǁrecord_streaming_latency__mutmut_7(
        self,
        report_id: str,
        start_time: float,
        first_token_time: float | None,
        completion_time: float
    ) -> None:
        """
        Record streaming latency measurement

        Args:
            report_id: Unique report identifier
            start_time: Time when request started (time.time())
            first_token_time: Time when first token received (None if streaming failed)
            completion_time: Time when streaming completed
        """
        if first_token_time is None:
            # Streaming failed - record error
            logger.error(
                "streaming failed - no first token received",
                {"report_id": report_id, "start_time": start_time}
            )
            return

        first_token_latency_ms = (first_token_time - start_time) * 1000
        total_latency_ms = (completion_time - start_time) * 1000

        metric = LatencyMetric(
            timestamp=completion_time,
            first_token_latency_ms=first_token_latency_ms,
            total_latency_ms=total_latency_ms,
            report_id=report_id
        )

        self.metrics.append(metric)

        # Log structured data
        logger.info(
            "Streaming latency recorded",
            {
                "report_id": report_id,
                "first_token_latency_ms": round(first_token_latency_ms, 2),
                "total_latency_ms": round(total_latency_ms, 2),
                "start_time": start_time,
                "first_token_time": first_token_time,
                "completion_time": completion_time,
            }
        )

        # Check for SLA violations
        self._check_sla_violation()

    def xǁSLAMonitorǁrecord_streaming_latency__mutmut_8(
        self,
        report_id: str,
        start_time: float,
        first_token_time: float | None,
        completion_time: float
    ) -> None:
        """
        Record streaming latency measurement

        Args:
            report_id: Unique report identifier
            start_time: Time when request started (time.time())
            first_token_time: Time when first token received (None if streaming failed)
            completion_time: Time when streaming completed
        """
        if first_token_time is None:
            # Streaming failed - record error
            logger.error(
                "STREAMING FAILED - NO FIRST TOKEN RECEIVED",
                {"report_id": report_id, "start_time": start_time}
            )
            return

        first_token_latency_ms = (first_token_time - start_time) * 1000
        total_latency_ms = (completion_time - start_time) * 1000

        metric = LatencyMetric(
            timestamp=completion_time,
            first_token_latency_ms=first_token_latency_ms,
            total_latency_ms=total_latency_ms,
            report_id=report_id
        )

        self.metrics.append(metric)

        # Log structured data
        logger.info(
            "Streaming latency recorded",
            {
                "report_id": report_id,
                "first_token_latency_ms": round(first_token_latency_ms, 2),
                "total_latency_ms": round(total_latency_ms, 2),
                "start_time": start_time,
                "first_token_time": first_token_time,
                "completion_time": completion_time,
            }
        )

        # Check for SLA violations
        self._check_sla_violation()

    def xǁSLAMonitorǁrecord_streaming_latency__mutmut_9(
        self,
        report_id: str,
        start_time: float,
        first_token_time: float | None,
        completion_time: float
    ) -> None:
        """
        Record streaming latency measurement

        Args:
            report_id: Unique report identifier
            start_time: Time when request started (time.time())
            first_token_time: Time when first token received (None if streaming failed)
            completion_time: Time when streaming completed
        """
        if first_token_time is None:
            # Streaming failed - record error
            logger.error(
                "Streaming failed - no first token received",
                {"XXreport_idXX": report_id, "start_time": start_time}
            )
            return

        first_token_latency_ms = (first_token_time - start_time) * 1000
        total_latency_ms = (completion_time - start_time) * 1000

        metric = LatencyMetric(
            timestamp=completion_time,
            first_token_latency_ms=first_token_latency_ms,
            total_latency_ms=total_latency_ms,
            report_id=report_id
        )

        self.metrics.append(metric)

        # Log structured data
        logger.info(
            "Streaming latency recorded",
            {
                "report_id": report_id,
                "first_token_latency_ms": round(first_token_latency_ms, 2),
                "total_latency_ms": round(total_latency_ms, 2),
                "start_time": start_time,
                "first_token_time": first_token_time,
                "completion_time": completion_time,
            }
        )

        # Check for SLA violations
        self._check_sla_violation()

    def xǁSLAMonitorǁrecord_streaming_latency__mutmut_10(
        self,
        report_id: str,
        start_time: float,
        first_token_time: float | None,
        completion_time: float
    ) -> None:
        """
        Record streaming latency measurement

        Args:
            report_id: Unique report identifier
            start_time: Time when request started (time.time())
            first_token_time: Time when first token received (None if streaming failed)
            completion_time: Time when streaming completed
        """
        if first_token_time is None:
            # Streaming failed - record error
            logger.error(
                "Streaming failed - no first token received",
                {"REPORT_ID": report_id, "start_time": start_time}
            )
            return

        first_token_latency_ms = (first_token_time - start_time) * 1000
        total_latency_ms = (completion_time - start_time) * 1000

        metric = LatencyMetric(
            timestamp=completion_time,
            first_token_latency_ms=first_token_latency_ms,
            total_latency_ms=total_latency_ms,
            report_id=report_id
        )

        self.metrics.append(metric)

        # Log structured data
        logger.info(
            "Streaming latency recorded",
            {
                "report_id": report_id,
                "first_token_latency_ms": round(first_token_latency_ms, 2),
                "total_latency_ms": round(total_latency_ms, 2),
                "start_time": start_time,
                "first_token_time": first_token_time,
                "completion_time": completion_time,
            }
        )

        # Check for SLA violations
        self._check_sla_violation()

    def xǁSLAMonitorǁrecord_streaming_latency__mutmut_11(
        self,
        report_id: str,
        start_time: float,
        first_token_time: float | None,
        completion_time: float
    ) -> None:
        """
        Record streaming latency measurement

        Args:
            report_id: Unique report identifier
            start_time: Time when request started (time.time())
            first_token_time: Time when first token received (None if streaming failed)
            completion_time: Time when streaming completed
        """
        if first_token_time is None:
            # Streaming failed - record error
            logger.error(
                "Streaming failed - no first token received",
                {"report_id": report_id, "XXstart_timeXX": start_time}
            )
            return

        first_token_latency_ms = (first_token_time - start_time) * 1000
        total_latency_ms = (completion_time - start_time) * 1000

        metric = LatencyMetric(
            timestamp=completion_time,
            first_token_latency_ms=first_token_latency_ms,
            total_latency_ms=total_latency_ms,
            report_id=report_id
        )

        self.metrics.append(metric)

        # Log structured data
        logger.info(
            "Streaming latency recorded",
            {
                "report_id": report_id,
                "first_token_latency_ms": round(first_token_latency_ms, 2),
                "total_latency_ms": round(total_latency_ms, 2),
                "start_time": start_time,
                "first_token_time": first_token_time,
                "completion_time": completion_time,
            }
        )

        # Check for SLA violations
        self._check_sla_violation()

    def xǁSLAMonitorǁrecord_streaming_latency__mutmut_12(
        self,
        report_id: str,
        start_time: float,
        first_token_time: float | None,
        completion_time: float
    ) -> None:
        """
        Record streaming latency measurement

        Args:
            report_id: Unique report identifier
            start_time: Time when request started (time.time())
            first_token_time: Time when first token received (None if streaming failed)
            completion_time: Time when streaming completed
        """
        if first_token_time is None:
            # Streaming failed - record error
            logger.error(
                "Streaming failed - no first token received",
                {"report_id": report_id, "START_TIME": start_time}
            )
            return

        first_token_latency_ms = (first_token_time - start_time) * 1000
        total_latency_ms = (completion_time - start_time) * 1000

        metric = LatencyMetric(
            timestamp=completion_time,
            first_token_latency_ms=first_token_latency_ms,
            total_latency_ms=total_latency_ms,
            report_id=report_id
        )

        self.metrics.append(metric)

        # Log structured data
        logger.info(
            "Streaming latency recorded",
            {
                "report_id": report_id,
                "first_token_latency_ms": round(first_token_latency_ms, 2),
                "total_latency_ms": round(total_latency_ms, 2),
                "start_time": start_time,
                "first_token_time": first_token_time,
                "completion_time": completion_time,
            }
        )

        # Check for SLA violations
        self._check_sla_violation()

    def xǁSLAMonitorǁrecord_streaming_latency__mutmut_13(
        self,
        report_id: str,
        start_time: float,
        first_token_time: float | None,
        completion_time: float
    ) -> None:
        """
        Record streaming latency measurement

        Args:
            report_id: Unique report identifier
            start_time: Time when request started (time.time())
            first_token_time: Time when first token received (None if streaming failed)
            completion_time: Time when streaming completed
        """
        if first_token_time is None:
            # Streaming failed - record error
            logger.error(
                "Streaming failed - no first token received",
                {"report_id": report_id, "start_time": start_time}
            )
            return

        first_token_latency_ms = None
        total_latency_ms = (completion_time - start_time) * 1000

        metric = LatencyMetric(
            timestamp=completion_time,
            first_token_latency_ms=first_token_latency_ms,
            total_latency_ms=total_latency_ms,
            report_id=report_id
        )

        self.metrics.append(metric)

        # Log structured data
        logger.info(
            "Streaming latency recorded",
            {
                "report_id": report_id,
                "first_token_latency_ms": round(first_token_latency_ms, 2),
                "total_latency_ms": round(total_latency_ms, 2),
                "start_time": start_time,
                "first_token_time": first_token_time,
                "completion_time": completion_time,
            }
        )

        # Check for SLA violations
        self._check_sla_violation()

    def xǁSLAMonitorǁrecord_streaming_latency__mutmut_14(
        self,
        report_id: str,
        start_time: float,
        first_token_time: float | None,
        completion_time: float
    ) -> None:
        """
        Record streaming latency measurement

        Args:
            report_id: Unique report identifier
            start_time: Time when request started (time.time())
            first_token_time: Time when first token received (None if streaming failed)
            completion_time: Time when streaming completed
        """
        if first_token_time is None:
            # Streaming failed - record error
            logger.error(
                "Streaming failed - no first token received",
                {"report_id": report_id, "start_time": start_time}
            )
            return

        first_token_latency_ms = (first_token_time - start_time) / 1000
        total_latency_ms = (completion_time - start_time) * 1000

        metric = LatencyMetric(
            timestamp=completion_time,
            first_token_latency_ms=first_token_latency_ms,
            total_latency_ms=total_latency_ms,
            report_id=report_id
        )

        self.metrics.append(metric)

        # Log structured data
        logger.info(
            "Streaming latency recorded",
            {
                "report_id": report_id,
                "first_token_latency_ms": round(first_token_latency_ms, 2),
                "total_latency_ms": round(total_latency_ms, 2),
                "start_time": start_time,
                "first_token_time": first_token_time,
                "completion_time": completion_time,
            }
        )

        # Check for SLA violations
        self._check_sla_violation()

    def xǁSLAMonitorǁrecord_streaming_latency__mutmut_15(
        self,
        report_id: str,
        start_time: float,
        first_token_time: float | None,
        completion_time: float
    ) -> None:
        """
        Record streaming latency measurement

        Args:
            report_id: Unique report identifier
            start_time: Time when request started (time.time())
            first_token_time: Time when first token received (None if streaming failed)
            completion_time: Time when streaming completed
        """
        if first_token_time is None:
            # Streaming failed - record error
            logger.error(
                "Streaming failed - no first token received",
                {"report_id": report_id, "start_time": start_time}
            )
            return

        first_token_latency_ms = (first_token_time + start_time) * 1000
        total_latency_ms = (completion_time - start_time) * 1000

        metric = LatencyMetric(
            timestamp=completion_time,
            first_token_latency_ms=first_token_latency_ms,
            total_latency_ms=total_latency_ms,
            report_id=report_id
        )

        self.metrics.append(metric)

        # Log structured data
        logger.info(
            "Streaming latency recorded",
            {
                "report_id": report_id,
                "first_token_latency_ms": round(first_token_latency_ms, 2),
                "total_latency_ms": round(total_latency_ms, 2),
                "start_time": start_time,
                "first_token_time": first_token_time,
                "completion_time": completion_time,
            }
        )

        # Check for SLA violations
        self._check_sla_violation()

    def xǁSLAMonitorǁrecord_streaming_latency__mutmut_16(
        self,
        report_id: str,
        start_time: float,
        first_token_time: float | None,
        completion_time: float
    ) -> None:
        """
        Record streaming latency measurement

        Args:
            report_id: Unique report identifier
            start_time: Time when request started (time.time())
            first_token_time: Time when first token received (None if streaming failed)
            completion_time: Time when streaming completed
        """
        if first_token_time is None:
            # Streaming failed - record error
            logger.error(
                "Streaming failed - no first token received",
                {"report_id": report_id, "start_time": start_time}
            )
            return

        first_token_latency_ms = (first_token_time - start_time) * 1001
        total_latency_ms = (completion_time - start_time) * 1000

        metric = LatencyMetric(
            timestamp=completion_time,
            first_token_latency_ms=first_token_latency_ms,
            total_latency_ms=total_latency_ms,
            report_id=report_id
        )

        self.metrics.append(metric)

        # Log structured data
        logger.info(
            "Streaming latency recorded",
            {
                "report_id": report_id,
                "first_token_latency_ms": round(first_token_latency_ms, 2),
                "total_latency_ms": round(total_latency_ms, 2),
                "start_time": start_time,
                "first_token_time": first_token_time,
                "completion_time": completion_time,
            }
        )

        # Check for SLA violations
        self._check_sla_violation()

    def xǁSLAMonitorǁrecord_streaming_latency__mutmut_17(
        self,
        report_id: str,
        start_time: float,
        first_token_time: float | None,
        completion_time: float
    ) -> None:
        """
        Record streaming latency measurement

        Args:
            report_id: Unique report identifier
            start_time: Time when request started (time.time())
            first_token_time: Time when first token received (None if streaming failed)
            completion_time: Time when streaming completed
        """
        if first_token_time is None:
            # Streaming failed - record error
            logger.error(
                "Streaming failed - no first token received",
                {"report_id": report_id, "start_time": start_time}
            )
            return

        first_token_latency_ms = (first_token_time - start_time) * 1000
        total_latency_ms = None

        metric = LatencyMetric(
            timestamp=completion_time,
            first_token_latency_ms=first_token_latency_ms,
            total_latency_ms=total_latency_ms,
            report_id=report_id
        )

        self.metrics.append(metric)

        # Log structured data
        logger.info(
            "Streaming latency recorded",
            {
                "report_id": report_id,
                "first_token_latency_ms": round(first_token_latency_ms, 2),
                "total_latency_ms": round(total_latency_ms, 2),
                "start_time": start_time,
                "first_token_time": first_token_time,
                "completion_time": completion_time,
            }
        )

        # Check for SLA violations
        self._check_sla_violation()

    def xǁSLAMonitorǁrecord_streaming_latency__mutmut_18(
        self,
        report_id: str,
        start_time: float,
        first_token_time: float | None,
        completion_time: float
    ) -> None:
        """
        Record streaming latency measurement

        Args:
            report_id: Unique report identifier
            start_time: Time when request started (time.time())
            first_token_time: Time when first token received (None if streaming failed)
            completion_time: Time when streaming completed
        """
        if first_token_time is None:
            # Streaming failed - record error
            logger.error(
                "Streaming failed - no first token received",
                {"report_id": report_id, "start_time": start_time}
            )
            return

        first_token_latency_ms = (first_token_time - start_time) * 1000
        total_latency_ms = (completion_time - start_time) / 1000

        metric = LatencyMetric(
            timestamp=completion_time,
            first_token_latency_ms=first_token_latency_ms,
            total_latency_ms=total_latency_ms,
            report_id=report_id
        )

        self.metrics.append(metric)

        # Log structured data
        logger.info(
            "Streaming latency recorded",
            {
                "report_id": report_id,
                "first_token_latency_ms": round(first_token_latency_ms, 2),
                "total_latency_ms": round(total_latency_ms, 2),
                "start_time": start_time,
                "first_token_time": first_token_time,
                "completion_time": completion_time,
            }
        )

        # Check for SLA violations
        self._check_sla_violation()

    def xǁSLAMonitorǁrecord_streaming_latency__mutmut_19(
        self,
        report_id: str,
        start_time: float,
        first_token_time: float | None,
        completion_time: float
    ) -> None:
        """
        Record streaming latency measurement

        Args:
            report_id: Unique report identifier
            start_time: Time when request started (time.time())
            first_token_time: Time when first token received (None if streaming failed)
            completion_time: Time when streaming completed
        """
        if first_token_time is None:
            # Streaming failed - record error
            logger.error(
                "Streaming failed - no first token received",
                {"report_id": report_id, "start_time": start_time}
            )
            return

        first_token_latency_ms = (first_token_time - start_time) * 1000
        total_latency_ms = (completion_time + start_time) * 1000

        metric = LatencyMetric(
            timestamp=completion_time,
            first_token_latency_ms=first_token_latency_ms,
            total_latency_ms=total_latency_ms,
            report_id=report_id
        )

        self.metrics.append(metric)

        # Log structured data
        logger.info(
            "Streaming latency recorded",
            {
                "report_id": report_id,
                "first_token_latency_ms": round(first_token_latency_ms, 2),
                "total_latency_ms": round(total_latency_ms, 2),
                "start_time": start_time,
                "first_token_time": first_token_time,
                "completion_time": completion_time,
            }
        )

        # Check for SLA violations
        self._check_sla_violation()

    def xǁSLAMonitorǁrecord_streaming_latency__mutmut_20(
        self,
        report_id: str,
        start_time: float,
        first_token_time: float | None,
        completion_time: float
    ) -> None:
        """
        Record streaming latency measurement

        Args:
            report_id: Unique report identifier
            start_time: Time when request started (time.time())
            first_token_time: Time when first token received (None if streaming failed)
            completion_time: Time when streaming completed
        """
        if first_token_time is None:
            # Streaming failed - record error
            logger.error(
                "Streaming failed - no first token received",
                {"report_id": report_id, "start_time": start_time}
            )
            return

        first_token_latency_ms = (first_token_time - start_time) * 1000
        total_latency_ms = (completion_time - start_time) * 1001

        metric = LatencyMetric(
            timestamp=completion_time,
            first_token_latency_ms=first_token_latency_ms,
            total_latency_ms=total_latency_ms,
            report_id=report_id
        )

        self.metrics.append(metric)

        # Log structured data
        logger.info(
            "Streaming latency recorded",
            {
                "report_id": report_id,
                "first_token_latency_ms": round(first_token_latency_ms, 2),
                "total_latency_ms": round(total_latency_ms, 2),
                "start_time": start_time,
                "first_token_time": first_token_time,
                "completion_time": completion_time,
            }
        )

        # Check for SLA violations
        self._check_sla_violation()

    def xǁSLAMonitorǁrecord_streaming_latency__mutmut_21(
        self,
        report_id: str,
        start_time: float,
        first_token_time: float | None,
        completion_time: float
    ) -> None:
        """
        Record streaming latency measurement

        Args:
            report_id: Unique report identifier
            start_time: Time when request started (time.time())
            first_token_time: Time when first token received (None if streaming failed)
            completion_time: Time when streaming completed
        """
        if first_token_time is None:
            # Streaming failed - record error
            logger.error(
                "Streaming failed - no first token received",
                {"report_id": report_id, "start_time": start_time}
            )
            return

        first_token_latency_ms = (first_token_time - start_time) * 1000
        total_latency_ms = (completion_time - start_time) * 1000

        metric = None

        self.metrics.append(metric)

        # Log structured data
        logger.info(
            "Streaming latency recorded",
            {
                "report_id": report_id,
                "first_token_latency_ms": round(first_token_latency_ms, 2),
                "total_latency_ms": round(total_latency_ms, 2),
                "start_time": start_time,
                "first_token_time": first_token_time,
                "completion_time": completion_time,
            }
        )

        # Check for SLA violations
        self._check_sla_violation()

    def xǁSLAMonitorǁrecord_streaming_latency__mutmut_22(
        self,
        report_id: str,
        start_time: float,
        first_token_time: float | None,
        completion_time: float
    ) -> None:
        """
        Record streaming latency measurement

        Args:
            report_id: Unique report identifier
            start_time: Time when request started (time.time())
            first_token_time: Time when first token received (None if streaming failed)
            completion_time: Time when streaming completed
        """
        if first_token_time is None:
            # Streaming failed - record error
            logger.error(
                "Streaming failed - no first token received",
                {"report_id": report_id, "start_time": start_time}
            )
            return

        first_token_latency_ms = (first_token_time - start_time) * 1000
        total_latency_ms = (completion_time - start_time) * 1000

        metric = LatencyMetric(
            timestamp=None,
            first_token_latency_ms=first_token_latency_ms,
            total_latency_ms=total_latency_ms,
            report_id=report_id
        )

        self.metrics.append(metric)

        # Log structured data
        logger.info(
            "Streaming latency recorded",
            {
                "report_id": report_id,
                "first_token_latency_ms": round(first_token_latency_ms, 2),
                "total_latency_ms": round(total_latency_ms, 2),
                "start_time": start_time,
                "first_token_time": first_token_time,
                "completion_time": completion_time,
            }
        )

        # Check for SLA violations
        self._check_sla_violation()

    def xǁSLAMonitorǁrecord_streaming_latency__mutmut_23(
        self,
        report_id: str,
        start_time: float,
        first_token_time: float | None,
        completion_time: float
    ) -> None:
        """
        Record streaming latency measurement

        Args:
            report_id: Unique report identifier
            start_time: Time when request started (time.time())
            first_token_time: Time when first token received (None if streaming failed)
            completion_time: Time when streaming completed
        """
        if first_token_time is None:
            # Streaming failed - record error
            logger.error(
                "Streaming failed - no first token received",
                {"report_id": report_id, "start_time": start_time}
            )
            return

        first_token_latency_ms = (first_token_time - start_time) * 1000
        total_latency_ms = (completion_time - start_time) * 1000

        metric = LatencyMetric(
            timestamp=completion_time,
            first_token_latency_ms=None,
            total_latency_ms=total_latency_ms,
            report_id=report_id
        )

        self.metrics.append(metric)

        # Log structured data
        logger.info(
            "Streaming latency recorded",
            {
                "report_id": report_id,
                "first_token_latency_ms": round(first_token_latency_ms, 2),
                "total_latency_ms": round(total_latency_ms, 2),
                "start_time": start_time,
                "first_token_time": first_token_time,
                "completion_time": completion_time,
            }
        )

        # Check for SLA violations
        self._check_sla_violation()

    def xǁSLAMonitorǁrecord_streaming_latency__mutmut_24(
        self,
        report_id: str,
        start_time: float,
        first_token_time: float | None,
        completion_time: float
    ) -> None:
        """
        Record streaming latency measurement

        Args:
            report_id: Unique report identifier
            start_time: Time when request started (time.time())
            first_token_time: Time when first token received (None if streaming failed)
            completion_time: Time when streaming completed
        """
        if first_token_time is None:
            # Streaming failed - record error
            logger.error(
                "Streaming failed - no first token received",
                {"report_id": report_id, "start_time": start_time}
            )
            return

        first_token_latency_ms = (first_token_time - start_time) * 1000
        total_latency_ms = (completion_time - start_time) * 1000

        metric = LatencyMetric(
            timestamp=completion_time,
            first_token_latency_ms=first_token_latency_ms,
            total_latency_ms=None,
            report_id=report_id
        )

        self.metrics.append(metric)

        # Log structured data
        logger.info(
            "Streaming latency recorded",
            {
                "report_id": report_id,
                "first_token_latency_ms": round(first_token_latency_ms, 2),
                "total_latency_ms": round(total_latency_ms, 2),
                "start_time": start_time,
                "first_token_time": first_token_time,
                "completion_time": completion_time,
            }
        )

        # Check for SLA violations
        self._check_sla_violation()

    def xǁSLAMonitorǁrecord_streaming_latency__mutmut_25(
        self,
        report_id: str,
        start_time: float,
        first_token_time: float | None,
        completion_time: float
    ) -> None:
        """
        Record streaming latency measurement

        Args:
            report_id: Unique report identifier
            start_time: Time when request started (time.time())
            first_token_time: Time when first token received (None if streaming failed)
            completion_time: Time when streaming completed
        """
        if first_token_time is None:
            # Streaming failed - record error
            logger.error(
                "Streaming failed - no first token received",
                {"report_id": report_id, "start_time": start_time}
            )
            return

        first_token_latency_ms = (first_token_time - start_time) * 1000
        total_latency_ms = (completion_time - start_time) * 1000

        metric = LatencyMetric(
            timestamp=completion_time,
            first_token_latency_ms=first_token_latency_ms,
            total_latency_ms=total_latency_ms,
            report_id=None
        )

        self.metrics.append(metric)

        # Log structured data
        logger.info(
            "Streaming latency recorded",
            {
                "report_id": report_id,
                "first_token_latency_ms": round(first_token_latency_ms, 2),
                "total_latency_ms": round(total_latency_ms, 2),
                "start_time": start_time,
                "first_token_time": first_token_time,
                "completion_time": completion_time,
            }
        )

        # Check for SLA violations
        self._check_sla_violation()

    def xǁSLAMonitorǁrecord_streaming_latency__mutmut_26(
        self,
        report_id: str,
        start_time: float,
        first_token_time: float | None,
        completion_time: float
    ) -> None:
        """
        Record streaming latency measurement

        Args:
            report_id: Unique report identifier
            start_time: Time when request started (time.time())
            first_token_time: Time when first token received (None if streaming failed)
            completion_time: Time when streaming completed
        """
        if first_token_time is None:
            # Streaming failed - record error
            logger.error(
                "Streaming failed - no first token received",
                {"report_id": report_id, "start_time": start_time}
            )
            return

        first_token_latency_ms = (first_token_time - start_time) * 1000
        total_latency_ms = (completion_time - start_time) * 1000

        metric = LatencyMetric(
            first_token_latency_ms=first_token_latency_ms,
            total_latency_ms=total_latency_ms,
            report_id=report_id
        )

        self.metrics.append(metric)

        # Log structured data
        logger.info(
            "Streaming latency recorded",
            {
                "report_id": report_id,
                "first_token_latency_ms": round(first_token_latency_ms, 2),
                "total_latency_ms": round(total_latency_ms, 2),
                "start_time": start_time,
                "first_token_time": first_token_time,
                "completion_time": completion_time,
            }
        )

        # Check for SLA violations
        self._check_sla_violation()

    def xǁSLAMonitorǁrecord_streaming_latency__mutmut_27(
        self,
        report_id: str,
        start_time: float,
        first_token_time: float | None,
        completion_time: float
    ) -> None:
        """
        Record streaming latency measurement

        Args:
            report_id: Unique report identifier
            start_time: Time when request started (time.time())
            first_token_time: Time when first token received (None if streaming failed)
            completion_time: Time when streaming completed
        """
        if first_token_time is None:
            # Streaming failed - record error
            logger.error(
                "Streaming failed - no first token received",
                {"report_id": report_id, "start_time": start_time}
            )
            return

        first_token_latency_ms = (first_token_time - start_time) * 1000
        total_latency_ms = (completion_time - start_time) * 1000

        metric = LatencyMetric(
            timestamp=completion_time,
            total_latency_ms=total_latency_ms,
            report_id=report_id
        )

        self.metrics.append(metric)

        # Log structured data
        logger.info(
            "Streaming latency recorded",
            {
                "report_id": report_id,
                "first_token_latency_ms": round(first_token_latency_ms, 2),
                "total_latency_ms": round(total_latency_ms, 2),
                "start_time": start_time,
                "first_token_time": first_token_time,
                "completion_time": completion_time,
            }
        )

        # Check for SLA violations
        self._check_sla_violation()

    def xǁSLAMonitorǁrecord_streaming_latency__mutmut_28(
        self,
        report_id: str,
        start_time: float,
        first_token_time: float | None,
        completion_time: float
    ) -> None:
        """
        Record streaming latency measurement

        Args:
            report_id: Unique report identifier
            start_time: Time when request started (time.time())
            first_token_time: Time when first token received (None if streaming failed)
            completion_time: Time when streaming completed
        """
        if first_token_time is None:
            # Streaming failed - record error
            logger.error(
                "Streaming failed - no first token received",
                {"report_id": report_id, "start_time": start_time}
            )
            return

        first_token_latency_ms = (first_token_time - start_time) * 1000
        total_latency_ms = (completion_time - start_time) * 1000

        metric = LatencyMetric(
            timestamp=completion_time,
            first_token_latency_ms=first_token_latency_ms,
            report_id=report_id
        )

        self.metrics.append(metric)

        # Log structured data
        logger.info(
            "Streaming latency recorded",
            {
                "report_id": report_id,
                "first_token_latency_ms": round(first_token_latency_ms, 2),
                "total_latency_ms": round(total_latency_ms, 2),
                "start_time": start_time,
                "first_token_time": first_token_time,
                "completion_time": completion_time,
            }
        )

        # Check for SLA violations
        self._check_sla_violation()

    def xǁSLAMonitorǁrecord_streaming_latency__mutmut_29(
        self,
        report_id: str,
        start_time: float,
        first_token_time: float | None,
        completion_time: float
    ) -> None:
        """
        Record streaming latency measurement

        Args:
            report_id: Unique report identifier
            start_time: Time when request started (time.time())
            first_token_time: Time when first token received (None if streaming failed)
            completion_time: Time when streaming completed
        """
        if first_token_time is None:
            # Streaming failed - record error
            logger.error(
                "Streaming failed - no first token received",
                {"report_id": report_id, "start_time": start_time}
            )
            return

        first_token_latency_ms = (first_token_time - start_time) * 1000
        total_latency_ms = (completion_time - start_time) * 1000

        metric = LatencyMetric(
            timestamp=completion_time,
            first_token_latency_ms=first_token_latency_ms,
            total_latency_ms=total_latency_ms,
            )

        self.metrics.append(metric)

        # Log structured data
        logger.info(
            "Streaming latency recorded",
            {
                "report_id": report_id,
                "first_token_latency_ms": round(first_token_latency_ms, 2),
                "total_latency_ms": round(total_latency_ms, 2),
                "start_time": start_time,
                "first_token_time": first_token_time,
                "completion_time": completion_time,
            }
        )

        # Check for SLA violations
        self._check_sla_violation()

    def xǁSLAMonitorǁrecord_streaming_latency__mutmut_30(
        self,
        report_id: str,
        start_time: float,
        first_token_time: float | None,
        completion_time: float
    ) -> None:
        """
        Record streaming latency measurement

        Args:
            report_id: Unique report identifier
            start_time: Time when request started (time.time())
            first_token_time: Time when first token received (None if streaming failed)
            completion_time: Time when streaming completed
        """
        if first_token_time is None:
            # Streaming failed - record error
            logger.error(
                "Streaming failed - no first token received",
                {"report_id": report_id, "start_time": start_time}
            )
            return

        first_token_latency_ms = (first_token_time - start_time) * 1000
        total_latency_ms = (completion_time - start_time) * 1000

        metric = LatencyMetric(
            timestamp=completion_time,
            first_token_latency_ms=first_token_latency_ms,
            total_latency_ms=total_latency_ms,
            report_id=report_id
        )

        self.metrics.append(None)

        # Log structured data
        logger.info(
            "Streaming latency recorded",
            {
                "report_id": report_id,
                "first_token_latency_ms": round(first_token_latency_ms, 2),
                "total_latency_ms": round(total_latency_ms, 2),
                "start_time": start_time,
                "first_token_time": first_token_time,
                "completion_time": completion_time,
            }
        )

        # Check for SLA violations
        self._check_sla_violation()

    def xǁSLAMonitorǁrecord_streaming_latency__mutmut_31(
        self,
        report_id: str,
        start_time: float,
        first_token_time: float | None,
        completion_time: float
    ) -> None:
        """
        Record streaming latency measurement

        Args:
            report_id: Unique report identifier
            start_time: Time when request started (time.time())
            first_token_time: Time when first token received (None if streaming failed)
            completion_time: Time when streaming completed
        """
        if first_token_time is None:
            # Streaming failed - record error
            logger.error(
                "Streaming failed - no first token received",
                {"report_id": report_id, "start_time": start_time}
            )
            return

        first_token_latency_ms = (first_token_time - start_time) * 1000
        total_latency_ms = (completion_time - start_time) * 1000

        metric = LatencyMetric(
            timestamp=completion_time,
            first_token_latency_ms=first_token_latency_ms,
            total_latency_ms=total_latency_ms,
            report_id=report_id
        )

        self.metrics.append(metric)

        # Log structured data
        logger.info(
            None,
            {
                "report_id": report_id,
                "first_token_latency_ms": round(first_token_latency_ms, 2),
                "total_latency_ms": round(total_latency_ms, 2),
                "start_time": start_time,
                "first_token_time": first_token_time,
                "completion_time": completion_time,
            }
        )

        # Check for SLA violations
        self._check_sla_violation()

    def xǁSLAMonitorǁrecord_streaming_latency__mutmut_32(
        self,
        report_id: str,
        start_time: float,
        first_token_time: float | None,
        completion_time: float
    ) -> None:
        """
        Record streaming latency measurement

        Args:
            report_id: Unique report identifier
            start_time: Time when request started (time.time())
            first_token_time: Time when first token received (None if streaming failed)
            completion_time: Time when streaming completed
        """
        if first_token_time is None:
            # Streaming failed - record error
            logger.error(
                "Streaming failed - no first token received",
                {"report_id": report_id, "start_time": start_time}
            )
            return

        first_token_latency_ms = (first_token_time - start_time) * 1000
        total_latency_ms = (completion_time - start_time) * 1000

        metric = LatencyMetric(
            timestamp=completion_time,
            first_token_latency_ms=first_token_latency_ms,
            total_latency_ms=total_latency_ms,
            report_id=report_id
        )

        self.metrics.append(metric)

        # Log structured data
        logger.info(
            "Streaming latency recorded",
            None
        )

        # Check for SLA violations
        self._check_sla_violation()

    def xǁSLAMonitorǁrecord_streaming_latency__mutmut_33(
        self,
        report_id: str,
        start_time: float,
        first_token_time: float | None,
        completion_time: float
    ) -> None:
        """
        Record streaming latency measurement

        Args:
            report_id: Unique report identifier
            start_time: Time when request started (time.time())
            first_token_time: Time when first token received (None if streaming failed)
            completion_time: Time when streaming completed
        """
        if first_token_time is None:
            # Streaming failed - record error
            logger.error(
                "Streaming failed - no first token received",
                {"report_id": report_id, "start_time": start_time}
            )
            return

        first_token_latency_ms = (first_token_time - start_time) * 1000
        total_latency_ms = (completion_time - start_time) * 1000

        metric = LatencyMetric(
            timestamp=completion_time,
            first_token_latency_ms=first_token_latency_ms,
            total_latency_ms=total_latency_ms,
            report_id=report_id
        )

        self.metrics.append(metric)

        # Log structured data
        logger.info(
            {
                "report_id": report_id,
                "first_token_latency_ms": round(first_token_latency_ms, 2),
                "total_latency_ms": round(total_latency_ms, 2),
                "start_time": start_time,
                "first_token_time": first_token_time,
                "completion_time": completion_time,
            }
        )

        # Check for SLA violations
        self._check_sla_violation()

    def xǁSLAMonitorǁrecord_streaming_latency__mutmut_34(
        self,
        report_id: str,
        start_time: float,
        first_token_time: float | None,
        completion_time: float
    ) -> None:
        """
        Record streaming latency measurement

        Args:
            report_id: Unique report identifier
            start_time: Time when request started (time.time())
            first_token_time: Time when first token received (None if streaming failed)
            completion_time: Time when streaming completed
        """
        if first_token_time is None:
            # Streaming failed - record error
            logger.error(
                "Streaming failed - no first token received",
                {"report_id": report_id, "start_time": start_time}
            )
            return

        first_token_latency_ms = (first_token_time - start_time) * 1000
        total_latency_ms = (completion_time - start_time) * 1000

        metric = LatencyMetric(
            timestamp=completion_time,
            first_token_latency_ms=first_token_latency_ms,
            total_latency_ms=total_latency_ms,
            report_id=report_id
        )

        self.metrics.append(metric)

        # Log structured data
        logger.info(
            "Streaming latency recorded",
            )

        # Check for SLA violations
        self._check_sla_violation()

    def xǁSLAMonitorǁrecord_streaming_latency__mutmut_35(
        self,
        report_id: str,
        start_time: float,
        first_token_time: float | None,
        completion_time: float
    ) -> None:
        """
        Record streaming latency measurement

        Args:
            report_id: Unique report identifier
            start_time: Time when request started (time.time())
            first_token_time: Time when first token received (None if streaming failed)
            completion_time: Time when streaming completed
        """
        if first_token_time is None:
            # Streaming failed - record error
            logger.error(
                "Streaming failed - no first token received",
                {"report_id": report_id, "start_time": start_time}
            )
            return

        first_token_latency_ms = (first_token_time - start_time) * 1000
        total_latency_ms = (completion_time - start_time) * 1000

        metric = LatencyMetric(
            timestamp=completion_time,
            first_token_latency_ms=first_token_latency_ms,
            total_latency_ms=total_latency_ms,
            report_id=report_id
        )

        self.metrics.append(metric)

        # Log structured data
        logger.info(
            "XXStreaming latency recordedXX",
            {
                "report_id": report_id,
                "first_token_latency_ms": round(first_token_latency_ms, 2),
                "total_latency_ms": round(total_latency_ms, 2),
                "start_time": start_time,
                "first_token_time": first_token_time,
                "completion_time": completion_time,
            }
        )

        # Check for SLA violations
        self._check_sla_violation()

    def xǁSLAMonitorǁrecord_streaming_latency__mutmut_36(
        self,
        report_id: str,
        start_time: float,
        first_token_time: float | None,
        completion_time: float
    ) -> None:
        """
        Record streaming latency measurement

        Args:
            report_id: Unique report identifier
            start_time: Time when request started (time.time())
            first_token_time: Time when first token received (None if streaming failed)
            completion_time: Time when streaming completed
        """
        if first_token_time is None:
            # Streaming failed - record error
            logger.error(
                "Streaming failed - no first token received",
                {"report_id": report_id, "start_time": start_time}
            )
            return

        first_token_latency_ms = (first_token_time - start_time) * 1000
        total_latency_ms = (completion_time - start_time) * 1000

        metric = LatencyMetric(
            timestamp=completion_time,
            first_token_latency_ms=first_token_latency_ms,
            total_latency_ms=total_latency_ms,
            report_id=report_id
        )

        self.metrics.append(metric)

        # Log structured data
        logger.info(
            "streaming latency recorded",
            {
                "report_id": report_id,
                "first_token_latency_ms": round(first_token_latency_ms, 2),
                "total_latency_ms": round(total_latency_ms, 2),
                "start_time": start_time,
                "first_token_time": first_token_time,
                "completion_time": completion_time,
            }
        )

        # Check for SLA violations
        self._check_sla_violation()

    def xǁSLAMonitorǁrecord_streaming_latency__mutmut_37(
        self,
        report_id: str,
        start_time: float,
        first_token_time: float | None,
        completion_time: float
    ) -> None:
        """
        Record streaming latency measurement

        Args:
            report_id: Unique report identifier
            start_time: Time when request started (time.time())
            first_token_time: Time when first token received (None if streaming failed)
            completion_time: Time when streaming completed
        """
        if first_token_time is None:
            # Streaming failed - record error
            logger.error(
                "Streaming failed - no first token received",
                {"report_id": report_id, "start_time": start_time}
            )
            return

        first_token_latency_ms = (first_token_time - start_time) * 1000
        total_latency_ms = (completion_time - start_time) * 1000

        metric = LatencyMetric(
            timestamp=completion_time,
            first_token_latency_ms=first_token_latency_ms,
            total_latency_ms=total_latency_ms,
            report_id=report_id
        )

        self.metrics.append(metric)

        # Log structured data
        logger.info(
            "STREAMING LATENCY RECORDED",
            {
                "report_id": report_id,
                "first_token_latency_ms": round(first_token_latency_ms, 2),
                "total_latency_ms": round(total_latency_ms, 2),
                "start_time": start_time,
                "first_token_time": first_token_time,
                "completion_time": completion_time,
            }
        )

        # Check for SLA violations
        self._check_sla_violation()

    def xǁSLAMonitorǁrecord_streaming_latency__mutmut_38(
        self,
        report_id: str,
        start_time: float,
        first_token_time: float | None,
        completion_time: float
    ) -> None:
        """
        Record streaming latency measurement

        Args:
            report_id: Unique report identifier
            start_time: Time when request started (time.time())
            first_token_time: Time when first token received (None if streaming failed)
            completion_time: Time when streaming completed
        """
        if first_token_time is None:
            # Streaming failed - record error
            logger.error(
                "Streaming failed - no first token received",
                {"report_id": report_id, "start_time": start_time}
            )
            return

        first_token_latency_ms = (first_token_time - start_time) * 1000
        total_latency_ms = (completion_time - start_time) * 1000

        metric = LatencyMetric(
            timestamp=completion_time,
            first_token_latency_ms=first_token_latency_ms,
            total_latency_ms=total_latency_ms,
            report_id=report_id
        )

        self.metrics.append(metric)

        # Log structured data
        logger.info(
            "Streaming latency recorded",
            {
                "XXreport_idXX": report_id,
                "first_token_latency_ms": round(first_token_latency_ms, 2),
                "total_latency_ms": round(total_latency_ms, 2),
                "start_time": start_time,
                "first_token_time": first_token_time,
                "completion_time": completion_time,
            }
        )

        # Check for SLA violations
        self._check_sla_violation()

    def xǁSLAMonitorǁrecord_streaming_latency__mutmut_39(
        self,
        report_id: str,
        start_time: float,
        first_token_time: float | None,
        completion_time: float
    ) -> None:
        """
        Record streaming latency measurement

        Args:
            report_id: Unique report identifier
            start_time: Time when request started (time.time())
            first_token_time: Time when first token received (None if streaming failed)
            completion_time: Time when streaming completed
        """
        if first_token_time is None:
            # Streaming failed - record error
            logger.error(
                "Streaming failed - no first token received",
                {"report_id": report_id, "start_time": start_time}
            )
            return

        first_token_latency_ms = (first_token_time - start_time) * 1000
        total_latency_ms = (completion_time - start_time) * 1000

        metric = LatencyMetric(
            timestamp=completion_time,
            first_token_latency_ms=first_token_latency_ms,
            total_latency_ms=total_latency_ms,
            report_id=report_id
        )

        self.metrics.append(metric)

        # Log structured data
        logger.info(
            "Streaming latency recorded",
            {
                "REPORT_ID": report_id,
                "first_token_latency_ms": round(first_token_latency_ms, 2),
                "total_latency_ms": round(total_latency_ms, 2),
                "start_time": start_time,
                "first_token_time": first_token_time,
                "completion_time": completion_time,
            }
        )

        # Check for SLA violations
        self._check_sla_violation()

    def xǁSLAMonitorǁrecord_streaming_latency__mutmut_40(
        self,
        report_id: str,
        start_time: float,
        first_token_time: float | None,
        completion_time: float
    ) -> None:
        """
        Record streaming latency measurement

        Args:
            report_id: Unique report identifier
            start_time: Time when request started (time.time())
            first_token_time: Time when first token received (None if streaming failed)
            completion_time: Time when streaming completed
        """
        if first_token_time is None:
            # Streaming failed - record error
            logger.error(
                "Streaming failed - no first token received",
                {"report_id": report_id, "start_time": start_time}
            )
            return

        first_token_latency_ms = (first_token_time - start_time) * 1000
        total_latency_ms = (completion_time - start_time) * 1000

        metric = LatencyMetric(
            timestamp=completion_time,
            first_token_latency_ms=first_token_latency_ms,
            total_latency_ms=total_latency_ms,
            report_id=report_id
        )

        self.metrics.append(metric)

        # Log structured data
        logger.info(
            "Streaming latency recorded",
            {
                "report_id": report_id,
                "XXfirst_token_latency_msXX": round(first_token_latency_ms, 2),
                "total_latency_ms": round(total_latency_ms, 2),
                "start_time": start_time,
                "first_token_time": first_token_time,
                "completion_time": completion_time,
            }
        )

        # Check for SLA violations
        self._check_sla_violation()

    def xǁSLAMonitorǁrecord_streaming_latency__mutmut_41(
        self,
        report_id: str,
        start_time: float,
        first_token_time: float | None,
        completion_time: float
    ) -> None:
        """
        Record streaming latency measurement

        Args:
            report_id: Unique report identifier
            start_time: Time when request started (time.time())
            first_token_time: Time when first token received (None if streaming failed)
            completion_time: Time when streaming completed
        """
        if first_token_time is None:
            # Streaming failed - record error
            logger.error(
                "Streaming failed - no first token received",
                {"report_id": report_id, "start_time": start_time}
            )
            return

        first_token_latency_ms = (first_token_time - start_time) * 1000
        total_latency_ms = (completion_time - start_time) * 1000

        metric = LatencyMetric(
            timestamp=completion_time,
            first_token_latency_ms=first_token_latency_ms,
            total_latency_ms=total_latency_ms,
            report_id=report_id
        )

        self.metrics.append(metric)

        # Log structured data
        logger.info(
            "Streaming latency recorded",
            {
                "report_id": report_id,
                "FIRST_TOKEN_LATENCY_MS": round(first_token_latency_ms, 2),
                "total_latency_ms": round(total_latency_ms, 2),
                "start_time": start_time,
                "first_token_time": first_token_time,
                "completion_time": completion_time,
            }
        )

        # Check for SLA violations
        self._check_sla_violation()

    def xǁSLAMonitorǁrecord_streaming_latency__mutmut_42(
        self,
        report_id: str,
        start_time: float,
        first_token_time: float | None,
        completion_time: float
    ) -> None:
        """
        Record streaming latency measurement

        Args:
            report_id: Unique report identifier
            start_time: Time when request started (time.time())
            first_token_time: Time when first token received (None if streaming failed)
            completion_time: Time when streaming completed
        """
        if first_token_time is None:
            # Streaming failed - record error
            logger.error(
                "Streaming failed - no first token received",
                {"report_id": report_id, "start_time": start_time}
            )
            return

        first_token_latency_ms = (first_token_time - start_time) * 1000
        total_latency_ms = (completion_time - start_time) * 1000

        metric = LatencyMetric(
            timestamp=completion_time,
            first_token_latency_ms=first_token_latency_ms,
            total_latency_ms=total_latency_ms,
            report_id=report_id
        )

        self.metrics.append(metric)

        # Log structured data
        logger.info(
            "Streaming latency recorded",
            {
                "report_id": report_id,
                "first_token_latency_ms": round(None, 2),
                "total_latency_ms": round(total_latency_ms, 2),
                "start_time": start_time,
                "first_token_time": first_token_time,
                "completion_time": completion_time,
            }
        )

        # Check for SLA violations
        self._check_sla_violation()

    def xǁSLAMonitorǁrecord_streaming_latency__mutmut_43(
        self,
        report_id: str,
        start_time: float,
        first_token_time: float | None,
        completion_time: float
    ) -> None:
        """
        Record streaming latency measurement

        Args:
            report_id: Unique report identifier
            start_time: Time when request started (time.time())
            first_token_time: Time when first token received (None if streaming failed)
            completion_time: Time when streaming completed
        """
        if first_token_time is None:
            # Streaming failed - record error
            logger.error(
                "Streaming failed - no first token received",
                {"report_id": report_id, "start_time": start_time}
            )
            return

        first_token_latency_ms = (first_token_time - start_time) * 1000
        total_latency_ms = (completion_time - start_time) * 1000

        metric = LatencyMetric(
            timestamp=completion_time,
            first_token_latency_ms=first_token_latency_ms,
            total_latency_ms=total_latency_ms,
            report_id=report_id
        )

        self.metrics.append(metric)

        # Log structured data
        logger.info(
            "Streaming latency recorded",
            {
                "report_id": report_id,
                "first_token_latency_ms": round(first_token_latency_ms, None),
                "total_latency_ms": round(total_latency_ms, 2),
                "start_time": start_time,
                "first_token_time": first_token_time,
                "completion_time": completion_time,
            }
        )

        # Check for SLA violations
        self._check_sla_violation()

    def xǁSLAMonitorǁrecord_streaming_latency__mutmut_44(
        self,
        report_id: str,
        start_time: float,
        first_token_time: float | None,
        completion_time: float
    ) -> None:
        """
        Record streaming latency measurement

        Args:
            report_id: Unique report identifier
            start_time: Time when request started (time.time())
            first_token_time: Time when first token received (None if streaming failed)
            completion_time: Time when streaming completed
        """
        if first_token_time is None:
            # Streaming failed - record error
            logger.error(
                "Streaming failed - no first token received",
                {"report_id": report_id, "start_time": start_time}
            )
            return

        first_token_latency_ms = (first_token_time - start_time) * 1000
        total_latency_ms = (completion_time - start_time) * 1000

        metric = LatencyMetric(
            timestamp=completion_time,
            first_token_latency_ms=first_token_latency_ms,
            total_latency_ms=total_latency_ms,
            report_id=report_id
        )

        self.metrics.append(metric)

        # Log structured data
        logger.info(
            "Streaming latency recorded",
            {
                "report_id": report_id,
                "first_token_latency_ms": round(2),
                "total_latency_ms": round(total_latency_ms, 2),
                "start_time": start_time,
                "first_token_time": first_token_time,
                "completion_time": completion_time,
            }
        )

        # Check for SLA violations
        self._check_sla_violation()

    def xǁSLAMonitorǁrecord_streaming_latency__mutmut_45(
        self,
        report_id: str,
        start_time: float,
        first_token_time: float | None,
        completion_time: float
    ) -> None:
        """
        Record streaming latency measurement

        Args:
            report_id: Unique report identifier
            start_time: Time when request started (time.time())
            first_token_time: Time when first token received (None if streaming failed)
            completion_time: Time when streaming completed
        """
        if first_token_time is None:
            # Streaming failed - record error
            logger.error(
                "Streaming failed - no first token received",
                {"report_id": report_id, "start_time": start_time}
            )
            return

        first_token_latency_ms = (first_token_time - start_time) * 1000
        total_latency_ms = (completion_time - start_time) * 1000

        metric = LatencyMetric(
            timestamp=completion_time,
            first_token_latency_ms=first_token_latency_ms,
            total_latency_ms=total_latency_ms,
            report_id=report_id
        )

        self.metrics.append(metric)

        # Log structured data
        logger.info(
            "Streaming latency recorded",
            {
                "report_id": report_id,
                "first_token_latency_ms": round(first_token_latency_ms, ),
                "total_latency_ms": round(total_latency_ms, 2),
                "start_time": start_time,
                "first_token_time": first_token_time,
                "completion_time": completion_time,
            }
        )

        # Check for SLA violations
        self._check_sla_violation()

    def xǁSLAMonitorǁrecord_streaming_latency__mutmut_46(
        self,
        report_id: str,
        start_time: float,
        first_token_time: float | None,
        completion_time: float
    ) -> None:
        """
        Record streaming latency measurement

        Args:
            report_id: Unique report identifier
            start_time: Time when request started (time.time())
            first_token_time: Time when first token received (None if streaming failed)
            completion_time: Time when streaming completed
        """
        if first_token_time is None:
            # Streaming failed - record error
            logger.error(
                "Streaming failed - no first token received",
                {"report_id": report_id, "start_time": start_time}
            )
            return

        first_token_latency_ms = (first_token_time - start_time) * 1000
        total_latency_ms = (completion_time - start_time) * 1000

        metric = LatencyMetric(
            timestamp=completion_time,
            first_token_latency_ms=first_token_latency_ms,
            total_latency_ms=total_latency_ms,
            report_id=report_id
        )

        self.metrics.append(metric)

        # Log structured data
        logger.info(
            "Streaming latency recorded",
            {
                "report_id": report_id,
                "first_token_latency_ms": round(first_token_latency_ms, 3),
                "total_latency_ms": round(total_latency_ms, 2),
                "start_time": start_time,
                "first_token_time": first_token_time,
                "completion_time": completion_time,
            }
        )

        # Check for SLA violations
        self._check_sla_violation()

    def xǁSLAMonitorǁrecord_streaming_latency__mutmut_47(
        self,
        report_id: str,
        start_time: float,
        first_token_time: float | None,
        completion_time: float
    ) -> None:
        """
        Record streaming latency measurement

        Args:
            report_id: Unique report identifier
            start_time: Time when request started (time.time())
            first_token_time: Time when first token received (None if streaming failed)
            completion_time: Time when streaming completed
        """
        if first_token_time is None:
            # Streaming failed - record error
            logger.error(
                "Streaming failed - no first token received",
                {"report_id": report_id, "start_time": start_time}
            )
            return

        first_token_latency_ms = (first_token_time - start_time) * 1000
        total_latency_ms = (completion_time - start_time) * 1000

        metric = LatencyMetric(
            timestamp=completion_time,
            first_token_latency_ms=first_token_latency_ms,
            total_latency_ms=total_latency_ms,
            report_id=report_id
        )

        self.metrics.append(metric)

        # Log structured data
        logger.info(
            "Streaming latency recorded",
            {
                "report_id": report_id,
                "first_token_latency_ms": round(first_token_latency_ms, 2),
                "XXtotal_latency_msXX": round(total_latency_ms, 2),
                "start_time": start_time,
                "first_token_time": first_token_time,
                "completion_time": completion_time,
            }
        )

        # Check for SLA violations
        self._check_sla_violation()

    def xǁSLAMonitorǁrecord_streaming_latency__mutmut_48(
        self,
        report_id: str,
        start_time: float,
        first_token_time: float | None,
        completion_time: float
    ) -> None:
        """
        Record streaming latency measurement

        Args:
            report_id: Unique report identifier
            start_time: Time when request started (time.time())
            first_token_time: Time when first token received (None if streaming failed)
            completion_time: Time when streaming completed
        """
        if first_token_time is None:
            # Streaming failed - record error
            logger.error(
                "Streaming failed - no first token received",
                {"report_id": report_id, "start_time": start_time}
            )
            return

        first_token_latency_ms = (first_token_time - start_time) * 1000
        total_latency_ms = (completion_time - start_time) * 1000

        metric = LatencyMetric(
            timestamp=completion_time,
            first_token_latency_ms=first_token_latency_ms,
            total_latency_ms=total_latency_ms,
            report_id=report_id
        )

        self.metrics.append(metric)

        # Log structured data
        logger.info(
            "Streaming latency recorded",
            {
                "report_id": report_id,
                "first_token_latency_ms": round(first_token_latency_ms, 2),
                "TOTAL_LATENCY_MS": round(total_latency_ms, 2),
                "start_time": start_time,
                "first_token_time": first_token_time,
                "completion_time": completion_time,
            }
        )

        # Check for SLA violations
        self._check_sla_violation()

    def xǁSLAMonitorǁrecord_streaming_latency__mutmut_49(
        self,
        report_id: str,
        start_time: float,
        first_token_time: float | None,
        completion_time: float
    ) -> None:
        """
        Record streaming latency measurement

        Args:
            report_id: Unique report identifier
            start_time: Time when request started (time.time())
            first_token_time: Time when first token received (None if streaming failed)
            completion_time: Time when streaming completed
        """
        if first_token_time is None:
            # Streaming failed - record error
            logger.error(
                "Streaming failed - no first token received",
                {"report_id": report_id, "start_time": start_time}
            )
            return

        first_token_latency_ms = (first_token_time - start_time) * 1000
        total_latency_ms = (completion_time - start_time) * 1000

        metric = LatencyMetric(
            timestamp=completion_time,
            first_token_latency_ms=first_token_latency_ms,
            total_latency_ms=total_latency_ms,
            report_id=report_id
        )

        self.metrics.append(metric)

        # Log structured data
        logger.info(
            "Streaming latency recorded",
            {
                "report_id": report_id,
                "first_token_latency_ms": round(first_token_latency_ms, 2),
                "total_latency_ms": round(None, 2),
                "start_time": start_time,
                "first_token_time": first_token_time,
                "completion_time": completion_time,
            }
        )

        # Check for SLA violations
        self._check_sla_violation()

    def xǁSLAMonitorǁrecord_streaming_latency__mutmut_50(
        self,
        report_id: str,
        start_time: float,
        first_token_time: float | None,
        completion_time: float
    ) -> None:
        """
        Record streaming latency measurement

        Args:
            report_id: Unique report identifier
            start_time: Time when request started (time.time())
            first_token_time: Time when first token received (None if streaming failed)
            completion_time: Time when streaming completed
        """
        if first_token_time is None:
            # Streaming failed - record error
            logger.error(
                "Streaming failed - no first token received",
                {"report_id": report_id, "start_time": start_time}
            )
            return

        first_token_latency_ms = (first_token_time - start_time) * 1000
        total_latency_ms = (completion_time - start_time) * 1000

        metric = LatencyMetric(
            timestamp=completion_time,
            first_token_latency_ms=first_token_latency_ms,
            total_latency_ms=total_latency_ms,
            report_id=report_id
        )

        self.metrics.append(metric)

        # Log structured data
        logger.info(
            "Streaming latency recorded",
            {
                "report_id": report_id,
                "first_token_latency_ms": round(first_token_latency_ms, 2),
                "total_latency_ms": round(total_latency_ms, None),
                "start_time": start_time,
                "first_token_time": first_token_time,
                "completion_time": completion_time,
            }
        )

        # Check for SLA violations
        self._check_sla_violation()

    def xǁSLAMonitorǁrecord_streaming_latency__mutmut_51(
        self,
        report_id: str,
        start_time: float,
        first_token_time: float | None,
        completion_time: float
    ) -> None:
        """
        Record streaming latency measurement

        Args:
            report_id: Unique report identifier
            start_time: Time when request started (time.time())
            first_token_time: Time when first token received (None if streaming failed)
            completion_time: Time when streaming completed
        """
        if first_token_time is None:
            # Streaming failed - record error
            logger.error(
                "Streaming failed - no first token received",
                {"report_id": report_id, "start_time": start_time}
            )
            return

        first_token_latency_ms = (first_token_time - start_time) * 1000
        total_latency_ms = (completion_time - start_time) * 1000

        metric = LatencyMetric(
            timestamp=completion_time,
            first_token_latency_ms=first_token_latency_ms,
            total_latency_ms=total_latency_ms,
            report_id=report_id
        )

        self.metrics.append(metric)

        # Log structured data
        logger.info(
            "Streaming latency recorded",
            {
                "report_id": report_id,
                "first_token_latency_ms": round(first_token_latency_ms, 2),
                "total_latency_ms": round(2),
                "start_time": start_time,
                "first_token_time": first_token_time,
                "completion_time": completion_time,
            }
        )

        # Check for SLA violations
        self._check_sla_violation()

    def xǁSLAMonitorǁrecord_streaming_latency__mutmut_52(
        self,
        report_id: str,
        start_time: float,
        first_token_time: float | None,
        completion_time: float
    ) -> None:
        """
        Record streaming latency measurement

        Args:
            report_id: Unique report identifier
            start_time: Time when request started (time.time())
            first_token_time: Time when first token received (None if streaming failed)
            completion_time: Time when streaming completed
        """
        if first_token_time is None:
            # Streaming failed - record error
            logger.error(
                "Streaming failed - no first token received",
                {"report_id": report_id, "start_time": start_time}
            )
            return

        first_token_latency_ms = (first_token_time - start_time) * 1000
        total_latency_ms = (completion_time - start_time) * 1000

        metric = LatencyMetric(
            timestamp=completion_time,
            first_token_latency_ms=first_token_latency_ms,
            total_latency_ms=total_latency_ms,
            report_id=report_id
        )

        self.metrics.append(metric)

        # Log structured data
        logger.info(
            "Streaming latency recorded",
            {
                "report_id": report_id,
                "first_token_latency_ms": round(first_token_latency_ms, 2),
                "total_latency_ms": round(total_latency_ms, ),
                "start_time": start_time,
                "first_token_time": first_token_time,
                "completion_time": completion_time,
            }
        )

        # Check for SLA violations
        self._check_sla_violation()

    def xǁSLAMonitorǁrecord_streaming_latency__mutmut_53(
        self,
        report_id: str,
        start_time: float,
        first_token_time: float | None,
        completion_time: float
    ) -> None:
        """
        Record streaming latency measurement

        Args:
            report_id: Unique report identifier
            start_time: Time when request started (time.time())
            first_token_time: Time when first token received (None if streaming failed)
            completion_time: Time when streaming completed
        """
        if first_token_time is None:
            # Streaming failed - record error
            logger.error(
                "Streaming failed - no first token received",
                {"report_id": report_id, "start_time": start_time}
            )
            return

        first_token_latency_ms = (first_token_time - start_time) * 1000
        total_latency_ms = (completion_time - start_time) * 1000

        metric = LatencyMetric(
            timestamp=completion_time,
            first_token_latency_ms=first_token_latency_ms,
            total_latency_ms=total_latency_ms,
            report_id=report_id
        )

        self.metrics.append(metric)

        # Log structured data
        logger.info(
            "Streaming latency recorded",
            {
                "report_id": report_id,
                "first_token_latency_ms": round(first_token_latency_ms, 2),
                "total_latency_ms": round(total_latency_ms, 3),
                "start_time": start_time,
                "first_token_time": first_token_time,
                "completion_time": completion_time,
            }
        )

        # Check for SLA violations
        self._check_sla_violation()

    def xǁSLAMonitorǁrecord_streaming_latency__mutmut_54(
        self,
        report_id: str,
        start_time: float,
        first_token_time: float | None,
        completion_time: float
    ) -> None:
        """
        Record streaming latency measurement

        Args:
            report_id: Unique report identifier
            start_time: Time when request started (time.time())
            first_token_time: Time when first token received (None if streaming failed)
            completion_time: Time when streaming completed
        """
        if first_token_time is None:
            # Streaming failed - record error
            logger.error(
                "Streaming failed - no first token received",
                {"report_id": report_id, "start_time": start_time}
            )
            return

        first_token_latency_ms = (first_token_time - start_time) * 1000
        total_latency_ms = (completion_time - start_time) * 1000

        metric = LatencyMetric(
            timestamp=completion_time,
            first_token_latency_ms=first_token_latency_ms,
            total_latency_ms=total_latency_ms,
            report_id=report_id
        )

        self.metrics.append(metric)

        # Log structured data
        logger.info(
            "Streaming latency recorded",
            {
                "report_id": report_id,
                "first_token_latency_ms": round(first_token_latency_ms, 2),
                "total_latency_ms": round(total_latency_ms, 2),
                "XXstart_timeXX": start_time,
                "first_token_time": first_token_time,
                "completion_time": completion_time,
            }
        )

        # Check for SLA violations
        self._check_sla_violation()

    def xǁSLAMonitorǁrecord_streaming_latency__mutmut_55(
        self,
        report_id: str,
        start_time: float,
        first_token_time: float | None,
        completion_time: float
    ) -> None:
        """
        Record streaming latency measurement

        Args:
            report_id: Unique report identifier
            start_time: Time when request started (time.time())
            first_token_time: Time when first token received (None if streaming failed)
            completion_time: Time when streaming completed
        """
        if first_token_time is None:
            # Streaming failed - record error
            logger.error(
                "Streaming failed - no first token received",
                {"report_id": report_id, "start_time": start_time}
            )
            return

        first_token_latency_ms = (first_token_time - start_time) * 1000
        total_latency_ms = (completion_time - start_time) * 1000

        metric = LatencyMetric(
            timestamp=completion_time,
            first_token_latency_ms=first_token_latency_ms,
            total_latency_ms=total_latency_ms,
            report_id=report_id
        )

        self.metrics.append(metric)

        # Log structured data
        logger.info(
            "Streaming latency recorded",
            {
                "report_id": report_id,
                "first_token_latency_ms": round(first_token_latency_ms, 2),
                "total_latency_ms": round(total_latency_ms, 2),
                "START_TIME": start_time,
                "first_token_time": first_token_time,
                "completion_time": completion_time,
            }
        )

        # Check for SLA violations
        self._check_sla_violation()

    def xǁSLAMonitorǁrecord_streaming_latency__mutmut_56(
        self,
        report_id: str,
        start_time: float,
        first_token_time: float | None,
        completion_time: float
    ) -> None:
        """
        Record streaming latency measurement

        Args:
            report_id: Unique report identifier
            start_time: Time when request started (time.time())
            first_token_time: Time when first token received (None if streaming failed)
            completion_time: Time when streaming completed
        """
        if first_token_time is None:
            # Streaming failed - record error
            logger.error(
                "Streaming failed - no first token received",
                {"report_id": report_id, "start_time": start_time}
            )
            return

        first_token_latency_ms = (first_token_time - start_time) * 1000
        total_latency_ms = (completion_time - start_time) * 1000

        metric = LatencyMetric(
            timestamp=completion_time,
            first_token_latency_ms=first_token_latency_ms,
            total_latency_ms=total_latency_ms,
            report_id=report_id
        )

        self.metrics.append(metric)

        # Log structured data
        logger.info(
            "Streaming latency recorded",
            {
                "report_id": report_id,
                "first_token_latency_ms": round(first_token_latency_ms, 2),
                "total_latency_ms": round(total_latency_ms, 2),
                "start_time": start_time,
                "XXfirst_token_timeXX": first_token_time,
                "completion_time": completion_time,
            }
        )

        # Check for SLA violations
        self._check_sla_violation()

    def xǁSLAMonitorǁrecord_streaming_latency__mutmut_57(
        self,
        report_id: str,
        start_time: float,
        first_token_time: float | None,
        completion_time: float
    ) -> None:
        """
        Record streaming latency measurement

        Args:
            report_id: Unique report identifier
            start_time: Time when request started (time.time())
            first_token_time: Time when first token received (None if streaming failed)
            completion_time: Time when streaming completed
        """
        if first_token_time is None:
            # Streaming failed - record error
            logger.error(
                "Streaming failed - no first token received",
                {"report_id": report_id, "start_time": start_time}
            )
            return

        first_token_latency_ms = (first_token_time - start_time) * 1000
        total_latency_ms = (completion_time - start_time) * 1000

        metric = LatencyMetric(
            timestamp=completion_time,
            first_token_latency_ms=first_token_latency_ms,
            total_latency_ms=total_latency_ms,
            report_id=report_id
        )

        self.metrics.append(metric)

        # Log structured data
        logger.info(
            "Streaming latency recorded",
            {
                "report_id": report_id,
                "first_token_latency_ms": round(first_token_latency_ms, 2),
                "total_latency_ms": round(total_latency_ms, 2),
                "start_time": start_time,
                "FIRST_TOKEN_TIME": first_token_time,
                "completion_time": completion_time,
            }
        )

        # Check for SLA violations
        self._check_sla_violation()

    def xǁSLAMonitorǁrecord_streaming_latency__mutmut_58(
        self,
        report_id: str,
        start_time: float,
        first_token_time: float | None,
        completion_time: float
    ) -> None:
        """
        Record streaming latency measurement

        Args:
            report_id: Unique report identifier
            start_time: Time when request started (time.time())
            first_token_time: Time when first token received (None if streaming failed)
            completion_time: Time when streaming completed
        """
        if first_token_time is None:
            # Streaming failed - record error
            logger.error(
                "Streaming failed - no first token received",
                {"report_id": report_id, "start_time": start_time}
            )
            return

        first_token_latency_ms = (first_token_time - start_time) * 1000
        total_latency_ms = (completion_time - start_time) * 1000

        metric = LatencyMetric(
            timestamp=completion_time,
            first_token_latency_ms=first_token_latency_ms,
            total_latency_ms=total_latency_ms,
            report_id=report_id
        )

        self.metrics.append(metric)

        # Log structured data
        logger.info(
            "Streaming latency recorded",
            {
                "report_id": report_id,
                "first_token_latency_ms": round(first_token_latency_ms, 2),
                "total_latency_ms": round(total_latency_ms, 2),
                "start_time": start_time,
                "first_token_time": first_token_time,
                "XXcompletion_timeXX": completion_time,
            }
        )

        # Check for SLA violations
        self._check_sla_violation()

    def xǁSLAMonitorǁrecord_streaming_latency__mutmut_59(
        self,
        report_id: str,
        start_time: float,
        first_token_time: float | None,
        completion_time: float
    ) -> None:
        """
        Record streaming latency measurement

        Args:
            report_id: Unique report identifier
            start_time: Time when request started (time.time())
            first_token_time: Time when first token received (None if streaming failed)
            completion_time: Time when streaming completed
        """
        if first_token_time is None:
            # Streaming failed - record error
            logger.error(
                "Streaming failed - no first token received",
                {"report_id": report_id, "start_time": start_time}
            )
            return

        first_token_latency_ms = (first_token_time - start_time) * 1000
        total_latency_ms = (completion_time - start_time) * 1000

        metric = LatencyMetric(
            timestamp=completion_time,
            first_token_latency_ms=first_token_latency_ms,
            total_latency_ms=total_latency_ms,
            report_id=report_id
        )

        self.metrics.append(metric)

        # Log structured data
        logger.info(
            "Streaming latency recorded",
            {
                "report_id": report_id,
                "first_token_latency_ms": round(first_token_latency_ms, 2),
                "total_latency_ms": round(total_latency_ms, 2),
                "start_time": start_time,
                "first_token_time": first_token_time,
                "COMPLETION_TIME": completion_time,
            }
        )

        # Check for SLA violations
        self._check_sla_violation()
    
    xǁSLAMonitorǁrecord_streaming_latency__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁSLAMonitorǁrecord_streaming_latency__mutmut_1': xǁSLAMonitorǁrecord_streaming_latency__mutmut_1, 
        'xǁSLAMonitorǁrecord_streaming_latency__mutmut_2': xǁSLAMonitorǁrecord_streaming_latency__mutmut_2, 
        'xǁSLAMonitorǁrecord_streaming_latency__mutmut_3': xǁSLAMonitorǁrecord_streaming_latency__mutmut_3, 
        'xǁSLAMonitorǁrecord_streaming_latency__mutmut_4': xǁSLAMonitorǁrecord_streaming_latency__mutmut_4, 
        'xǁSLAMonitorǁrecord_streaming_latency__mutmut_5': xǁSLAMonitorǁrecord_streaming_latency__mutmut_5, 
        'xǁSLAMonitorǁrecord_streaming_latency__mutmut_6': xǁSLAMonitorǁrecord_streaming_latency__mutmut_6, 
        'xǁSLAMonitorǁrecord_streaming_latency__mutmut_7': xǁSLAMonitorǁrecord_streaming_latency__mutmut_7, 
        'xǁSLAMonitorǁrecord_streaming_latency__mutmut_8': xǁSLAMonitorǁrecord_streaming_latency__mutmut_8, 
        'xǁSLAMonitorǁrecord_streaming_latency__mutmut_9': xǁSLAMonitorǁrecord_streaming_latency__mutmut_9, 
        'xǁSLAMonitorǁrecord_streaming_latency__mutmut_10': xǁSLAMonitorǁrecord_streaming_latency__mutmut_10, 
        'xǁSLAMonitorǁrecord_streaming_latency__mutmut_11': xǁSLAMonitorǁrecord_streaming_latency__mutmut_11, 
        'xǁSLAMonitorǁrecord_streaming_latency__mutmut_12': xǁSLAMonitorǁrecord_streaming_latency__mutmut_12, 
        'xǁSLAMonitorǁrecord_streaming_latency__mutmut_13': xǁSLAMonitorǁrecord_streaming_latency__mutmut_13, 
        'xǁSLAMonitorǁrecord_streaming_latency__mutmut_14': xǁSLAMonitorǁrecord_streaming_latency__mutmut_14, 
        'xǁSLAMonitorǁrecord_streaming_latency__mutmut_15': xǁSLAMonitorǁrecord_streaming_latency__mutmut_15, 
        'xǁSLAMonitorǁrecord_streaming_latency__mutmut_16': xǁSLAMonitorǁrecord_streaming_latency__mutmut_16, 
        'xǁSLAMonitorǁrecord_streaming_latency__mutmut_17': xǁSLAMonitorǁrecord_streaming_latency__mutmut_17, 
        'xǁSLAMonitorǁrecord_streaming_latency__mutmut_18': xǁSLAMonitorǁrecord_streaming_latency__mutmut_18, 
        'xǁSLAMonitorǁrecord_streaming_latency__mutmut_19': xǁSLAMonitorǁrecord_streaming_latency__mutmut_19, 
        'xǁSLAMonitorǁrecord_streaming_latency__mutmut_20': xǁSLAMonitorǁrecord_streaming_latency__mutmut_20, 
        'xǁSLAMonitorǁrecord_streaming_latency__mutmut_21': xǁSLAMonitorǁrecord_streaming_latency__mutmut_21, 
        'xǁSLAMonitorǁrecord_streaming_latency__mutmut_22': xǁSLAMonitorǁrecord_streaming_latency__mutmut_22, 
        'xǁSLAMonitorǁrecord_streaming_latency__mutmut_23': xǁSLAMonitorǁrecord_streaming_latency__mutmut_23, 
        'xǁSLAMonitorǁrecord_streaming_latency__mutmut_24': xǁSLAMonitorǁrecord_streaming_latency__mutmut_24, 
        'xǁSLAMonitorǁrecord_streaming_latency__mutmut_25': xǁSLAMonitorǁrecord_streaming_latency__mutmut_25, 
        'xǁSLAMonitorǁrecord_streaming_latency__mutmut_26': xǁSLAMonitorǁrecord_streaming_latency__mutmut_26, 
        'xǁSLAMonitorǁrecord_streaming_latency__mutmut_27': xǁSLAMonitorǁrecord_streaming_latency__mutmut_27, 
        'xǁSLAMonitorǁrecord_streaming_latency__mutmut_28': xǁSLAMonitorǁrecord_streaming_latency__mutmut_28, 
        'xǁSLAMonitorǁrecord_streaming_latency__mutmut_29': xǁSLAMonitorǁrecord_streaming_latency__mutmut_29, 
        'xǁSLAMonitorǁrecord_streaming_latency__mutmut_30': xǁSLAMonitorǁrecord_streaming_latency__mutmut_30, 
        'xǁSLAMonitorǁrecord_streaming_latency__mutmut_31': xǁSLAMonitorǁrecord_streaming_latency__mutmut_31, 
        'xǁSLAMonitorǁrecord_streaming_latency__mutmut_32': xǁSLAMonitorǁrecord_streaming_latency__mutmut_32, 
        'xǁSLAMonitorǁrecord_streaming_latency__mutmut_33': xǁSLAMonitorǁrecord_streaming_latency__mutmut_33, 
        'xǁSLAMonitorǁrecord_streaming_latency__mutmut_34': xǁSLAMonitorǁrecord_streaming_latency__mutmut_34, 
        'xǁSLAMonitorǁrecord_streaming_latency__mutmut_35': xǁSLAMonitorǁrecord_streaming_latency__mutmut_35, 
        'xǁSLAMonitorǁrecord_streaming_latency__mutmut_36': xǁSLAMonitorǁrecord_streaming_latency__mutmut_36, 
        'xǁSLAMonitorǁrecord_streaming_latency__mutmut_37': xǁSLAMonitorǁrecord_streaming_latency__mutmut_37, 
        'xǁSLAMonitorǁrecord_streaming_latency__mutmut_38': xǁSLAMonitorǁrecord_streaming_latency__mutmut_38, 
        'xǁSLAMonitorǁrecord_streaming_latency__mutmut_39': xǁSLAMonitorǁrecord_streaming_latency__mutmut_39, 
        'xǁSLAMonitorǁrecord_streaming_latency__mutmut_40': xǁSLAMonitorǁrecord_streaming_latency__mutmut_40, 
        'xǁSLAMonitorǁrecord_streaming_latency__mutmut_41': xǁSLAMonitorǁrecord_streaming_latency__mutmut_41, 
        'xǁSLAMonitorǁrecord_streaming_latency__mutmut_42': xǁSLAMonitorǁrecord_streaming_latency__mutmut_42, 
        'xǁSLAMonitorǁrecord_streaming_latency__mutmut_43': xǁSLAMonitorǁrecord_streaming_latency__mutmut_43, 
        'xǁSLAMonitorǁrecord_streaming_latency__mutmut_44': xǁSLAMonitorǁrecord_streaming_latency__mutmut_44, 
        'xǁSLAMonitorǁrecord_streaming_latency__mutmut_45': xǁSLAMonitorǁrecord_streaming_latency__mutmut_45, 
        'xǁSLAMonitorǁrecord_streaming_latency__mutmut_46': xǁSLAMonitorǁrecord_streaming_latency__mutmut_46, 
        'xǁSLAMonitorǁrecord_streaming_latency__mutmut_47': xǁSLAMonitorǁrecord_streaming_latency__mutmut_47, 
        'xǁSLAMonitorǁrecord_streaming_latency__mutmut_48': xǁSLAMonitorǁrecord_streaming_latency__mutmut_48, 
        'xǁSLAMonitorǁrecord_streaming_latency__mutmut_49': xǁSLAMonitorǁrecord_streaming_latency__mutmut_49, 
        'xǁSLAMonitorǁrecord_streaming_latency__mutmut_50': xǁSLAMonitorǁrecord_streaming_latency__mutmut_50, 
        'xǁSLAMonitorǁrecord_streaming_latency__mutmut_51': xǁSLAMonitorǁrecord_streaming_latency__mutmut_51, 
        'xǁSLAMonitorǁrecord_streaming_latency__mutmut_52': xǁSLAMonitorǁrecord_streaming_latency__mutmut_52, 
        'xǁSLAMonitorǁrecord_streaming_latency__mutmut_53': xǁSLAMonitorǁrecord_streaming_latency__mutmut_53, 
        'xǁSLAMonitorǁrecord_streaming_latency__mutmut_54': xǁSLAMonitorǁrecord_streaming_latency__mutmut_54, 
        'xǁSLAMonitorǁrecord_streaming_latency__mutmut_55': xǁSLAMonitorǁrecord_streaming_latency__mutmut_55, 
        'xǁSLAMonitorǁrecord_streaming_latency__mutmut_56': xǁSLAMonitorǁrecord_streaming_latency__mutmut_56, 
        'xǁSLAMonitorǁrecord_streaming_latency__mutmut_57': xǁSLAMonitorǁrecord_streaming_latency__mutmut_57, 
        'xǁSLAMonitorǁrecord_streaming_latency__mutmut_58': xǁSLAMonitorǁrecord_streaming_latency__mutmut_58, 
        'xǁSLAMonitorǁrecord_streaming_latency__mutmut_59': xǁSLAMonitorǁrecord_streaming_latency__mutmut_59
    }
    
    def record_streaming_latency(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁSLAMonitorǁrecord_streaming_latency__mutmut_orig"), object.__getattribute__(self, "xǁSLAMonitorǁrecord_streaming_latency__mutmut_mutants"), args, kwargs, self)
        return result 
    
    record_streaming_latency.__signature__ = _mutmut_signature(xǁSLAMonitorǁrecord_streaming_latency__mutmut_orig)
    xǁSLAMonitorǁrecord_streaming_latency__mutmut_orig.__name__ = 'xǁSLAMonitorǁrecord_streaming_latency'

    def xǁSLAMonitorǁget_stats__mutmut_orig(self) -> SLAStats:
        """
        Calculate current SLA statistics

        Returns:
            SLAStats with percentiles and violation count
        """
        if not self.metrics:
            return SLAStats(p50=0, p95=0, p99=0, count=0, violations=self._violation_count)

        latencies = sorted([m.first_token_latency_ms for m in self.metrics])
        count = len(latencies)

        p50 = self._percentile(latencies, 50)
        p95 = self._percentile(latencies, 95)
        p99 = self._percentile(latencies, 99)

        # Find last violation timestamp
        last_violation_timestamp = None
        for metric in reversed(self.metrics):
            if metric.first_token_latency_ms > self.sla_threshold_ms:
                last_violation_timestamp = metric.timestamp
                break

        return SLAStats(
            p50=round(p50, 2),
            p95=round(p95, 2),
            p99=round(p99, 2),
            count=count,
            violations=self._violation_count,
            last_violation_timestamp=last_violation_timestamp
        )

    def xǁSLAMonitorǁget_stats__mutmut_1(self) -> SLAStats:
        """
        Calculate current SLA statistics

        Returns:
            SLAStats with percentiles and violation count
        """
        if self.metrics:
            return SLAStats(p50=0, p95=0, p99=0, count=0, violations=self._violation_count)

        latencies = sorted([m.first_token_latency_ms for m in self.metrics])
        count = len(latencies)

        p50 = self._percentile(latencies, 50)
        p95 = self._percentile(latencies, 95)
        p99 = self._percentile(latencies, 99)

        # Find last violation timestamp
        last_violation_timestamp = None
        for metric in reversed(self.metrics):
            if metric.first_token_latency_ms > self.sla_threshold_ms:
                last_violation_timestamp = metric.timestamp
                break

        return SLAStats(
            p50=round(p50, 2),
            p95=round(p95, 2),
            p99=round(p99, 2),
            count=count,
            violations=self._violation_count,
            last_violation_timestamp=last_violation_timestamp
        )

    def xǁSLAMonitorǁget_stats__mutmut_2(self) -> SLAStats:
        """
        Calculate current SLA statistics

        Returns:
            SLAStats with percentiles and violation count
        """
        if not self.metrics:
            return SLAStats(p50=None, p95=0, p99=0, count=0, violations=self._violation_count)

        latencies = sorted([m.first_token_latency_ms for m in self.metrics])
        count = len(latencies)

        p50 = self._percentile(latencies, 50)
        p95 = self._percentile(latencies, 95)
        p99 = self._percentile(latencies, 99)

        # Find last violation timestamp
        last_violation_timestamp = None
        for metric in reversed(self.metrics):
            if metric.first_token_latency_ms > self.sla_threshold_ms:
                last_violation_timestamp = metric.timestamp
                break

        return SLAStats(
            p50=round(p50, 2),
            p95=round(p95, 2),
            p99=round(p99, 2),
            count=count,
            violations=self._violation_count,
            last_violation_timestamp=last_violation_timestamp
        )

    def xǁSLAMonitorǁget_stats__mutmut_3(self) -> SLAStats:
        """
        Calculate current SLA statistics

        Returns:
            SLAStats with percentiles and violation count
        """
        if not self.metrics:
            return SLAStats(p50=0, p95=None, p99=0, count=0, violations=self._violation_count)

        latencies = sorted([m.first_token_latency_ms for m in self.metrics])
        count = len(latencies)

        p50 = self._percentile(latencies, 50)
        p95 = self._percentile(latencies, 95)
        p99 = self._percentile(latencies, 99)

        # Find last violation timestamp
        last_violation_timestamp = None
        for metric in reversed(self.metrics):
            if metric.first_token_latency_ms > self.sla_threshold_ms:
                last_violation_timestamp = metric.timestamp
                break

        return SLAStats(
            p50=round(p50, 2),
            p95=round(p95, 2),
            p99=round(p99, 2),
            count=count,
            violations=self._violation_count,
            last_violation_timestamp=last_violation_timestamp
        )

    def xǁSLAMonitorǁget_stats__mutmut_4(self) -> SLAStats:
        """
        Calculate current SLA statistics

        Returns:
            SLAStats with percentiles and violation count
        """
        if not self.metrics:
            return SLAStats(p50=0, p95=0, p99=None, count=0, violations=self._violation_count)

        latencies = sorted([m.first_token_latency_ms for m in self.metrics])
        count = len(latencies)

        p50 = self._percentile(latencies, 50)
        p95 = self._percentile(latencies, 95)
        p99 = self._percentile(latencies, 99)

        # Find last violation timestamp
        last_violation_timestamp = None
        for metric in reversed(self.metrics):
            if metric.first_token_latency_ms > self.sla_threshold_ms:
                last_violation_timestamp = metric.timestamp
                break

        return SLAStats(
            p50=round(p50, 2),
            p95=round(p95, 2),
            p99=round(p99, 2),
            count=count,
            violations=self._violation_count,
            last_violation_timestamp=last_violation_timestamp
        )

    def xǁSLAMonitorǁget_stats__mutmut_5(self) -> SLAStats:
        """
        Calculate current SLA statistics

        Returns:
            SLAStats with percentiles and violation count
        """
        if not self.metrics:
            return SLAStats(p50=0, p95=0, p99=0, count=None, violations=self._violation_count)

        latencies = sorted([m.first_token_latency_ms for m in self.metrics])
        count = len(latencies)

        p50 = self._percentile(latencies, 50)
        p95 = self._percentile(latencies, 95)
        p99 = self._percentile(latencies, 99)

        # Find last violation timestamp
        last_violation_timestamp = None
        for metric in reversed(self.metrics):
            if metric.first_token_latency_ms > self.sla_threshold_ms:
                last_violation_timestamp = metric.timestamp
                break

        return SLAStats(
            p50=round(p50, 2),
            p95=round(p95, 2),
            p99=round(p99, 2),
            count=count,
            violations=self._violation_count,
            last_violation_timestamp=last_violation_timestamp
        )

    def xǁSLAMonitorǁget_stats__mutmut_6(self) -> SLAStats:
        """
        Calculate current SLA statistics

        Returns:
            SLAStats with percentiles and violation count
        """
        if not self.metrics:
            return SLAStats(p50=0, p95=0, p99=0, count=0, violations=None)

        latencies = sorted([m.first_token_latency_ms for m in self.metrics])
        count = len(latencies)

        p50 = self._percentile(latencies, 50)
        p95 = self._percentile(latencies, 95)
        p99 = self._percentile(latencies, 99)

        # Find last violation timestamp
        last_violation_timestamp = None
        for metric in reversed(self.metrics):
            if metric.first_token_latency_ms > self.sla_threshold_ms:
                last_violation_timestamp = metric.timestamp
                break

        return SLAStats(
            p50=round(p50, 2),
            p95=round(p95, 2),
            p99=round(p99, 2),
            count=count,
            violations=self._violation_count,
            last_violation_timestamp=last_violation_timestamp
        )

    def xǁSLAMonitorǁget_stats__mutmut_7(self) -> SLAStats:
        """
        Calculate current SLA statistics

        Returns:
            SLAStats with percentiles and violation count
        """
        if not self.metrics:
            return SLAStats(p95=0, p99=0, count=0, violations=self._violation_count)

        latencies = sorted([m.first_token_latency_ms for m in self.metrics])
        count = len(latencies)

        p50 = self._percentile(latencies, 50)
        p95 = self._percentile(latencies, 95)
        p99 = self._percentile(latencies, 99)

        # Find last violation timestamp
        last_violation_timestamp = None
        for metric in reversed(self.metrics):
            if metric.first_token_latency_ms > self.sla_threshold_ms:
                last_violation_timestamp = metric.timestamp
                break

        return SLAStats(
            p50=round(p50, 2),
            p95=round(p95, 2),
            p99=round(p99, 2),
            count=count,
            violations=self._violation_count,
            last_violation_timestamp=last_violation_timestamp
        )

    def xǁSLAMonitorǁget_stats__mutmut_8(self) -> SLAStats:
        """
        Calculate current SLA statistics

        Returns:
            SLAStats with percentiles and violation count
        """
        if not self.metrics:
            return SLAStats(p50=0, p99=0, count=0, violations=self._violation_count)

        latencies = sorted([m.first_token_latency_ms for m in self.metrics])
        count = len(latencies)

        p50 = self._percentile(latencies, 50)
        p95 = self._percentile(latencies, 95)
        p99 = self._percentile(latencies, 99)

        # Find last violation timestamp
        last_violation_timestamp = None
        for metric in reversed(self.metrics):
            if metric.first_token_latency_ms > self.sla_threshold_ms:
                last_violation_timestamp = metric.timestamp
                break

        return SLAStats(
            p50=round(p50, 2),
            p95=round(p95, 2),
            p99=round(p99, 2),
            count=count,
            violations=self._violation_count,
            last_violation_timestamp=last_violation_timestamp
        )

    def xǁSLAMonitorǁget_stats__mutmut_9(self) -> SLAStats:
        """
        Calculate current SLA statistics

        Returns:
            SLAStats with percentiles and violation count
        """
        if not self.metrics:
            return SLAStats(p50=0, p95=0, count=0, violations=self._violation_count)

        latencies = sorted([m.first_token_latency_ms for m in self.metrics])
        count = len(latencies)

        p50 = self._percentile(latencies, 50)
        p95 = self._percentile(latencies, 95)
        p99 = self._percentile(latencies, 99)

        # Find last violation timestamp
        last_violation_timestamp = None
        for metric in reversed(self.metrics):
            if metric.first_token_latency_ms > self.sla_threshold_ms:
                last_violation_timestamp = metric.timestamp
                break

        return SLAStats(
            p50=round(p50, 2),
            p95=round(p95, 2),
            p99=round(p99, 2),
            count=count,
            violations=self._violation_count,
            last_violation_timestamp=last_violation_timestamp
        )

    def xǁSLAMonitorǁget_stats__mutmut_10(self) -> SLAStats:
        """
        Calculate current SLA statistics

        Returns:
            SLAStats with percentiles and violation count
        """
        if not self.metrics:
            return SLAStats(p50=0, p95=0, p99=0, violations=self._violation_count)

        latencies = sorted([m.first_token_latency_ms for m in self.metrics])
        count = len(latencies)

        p50 = self._percentile(latencies, 50)
        p95 = self._percentile(latencies, 95)
        p99 = self._percentile(latencies, 99)

        # Find last violation timestamp
        last_violation_timestamp = None
        for metric in reversed(self.metrics):
            if metric.first_token_latency_ms > self.sla_threshold_ms:
                last_violation_timestamp = metric.timestamp
                break

        return SLAStats(
            p50=round(p50, 2),
            p95=round(p95, 2),
            p99=round(p99, 2),
            count=count,
            violations=self._violation_count,
            last_violation_timestamp=last_violation_timestamp
        )

    def xǁSLAMonitorǁget_stats__mutmut_11(self) -> SLAStats:
        """
        Calculate current SLA statistics

        Returns:
            SLAStats with percentiles and violation count
        """
        if not self.metrics:
            return SLAStats(p50=0, p95=0, p99=0, count=0, )

        latencies = sorted([m.first_token_latency_ms for m in self.metrics])
        count = len(latencies)

        p50 = self._percentile(latencies, 50)
        p95 = self._percentile(latencies, 95)
        p99 = self._percentile(latencies, 99)

        # Find last violation timestamp
        last_violation_timestamp = None
        for metric in reversed(self.metrics):
            if metric.first_token_latency_ms > self.sla_threshold_ms:
                last_violation_timestamp = metric.timestamp
                break

        return SLAStats(
            p50=round(p50, 2),
            p95=round(p95, 2),
            p99=round(p99, 2),
            count=count,
            violations=self._violation_count,
            last_violation_timestamp=last_violation_timestamp
        )

    def xǁSLAMonitorǁget_stats__mutmut_12(self) -> SLAStats:
        """
        Calculate current SLA statistics

        Returns:
            SLAStats with percentiles and violation count
        """
        if not self.metrics:
            return SLAStats(p50=1, p95=0, p99=0, count=0, violations=self._violation_count)

        latencies = sorted([m.first_token_latency_ms for m in self.metrics])
        count = len(latencies)

        p50 = self._percentile(latencies, 50)
        p95 = self._percentile(latencies, 95)
        p99 = self._percentile(latencies, 99)

        # Find last violation timestamp
        last_violation_timestamp = None
        for metric in reversed(self.metrics):
            if metric.first_token_latency_ms > self.sla_threshold_ms:
                last_violation_timestamp = metric.timestamp
                break

        return SLAStats(
            p50=round(p50, 2),
            p95=round(p95, 2),
            p99=round(p99, 2),
            count=count,
            violations=self._violation_count,
            last_violation_timestamp=last_violation_timestamp
        )

    def xǁSLAMonitorǁget_stats__mutmut_13(self) -> SLAStats:
        """
        Calculate current SLA statistics

        Returns:
            SLAStats with percentiles and violation count
        """
        if not self.metrics:
            return SLAStats(p50=0, p95=1, p99=0, count=0, violations=self._violation_count)

        latencies = sorted([m.first_token_latency_ms for m in self.metrics])
        count = len(latencies)

        p50 = self._percentile(latencies, 50)
        p95 = self._percentile(latencies, 95)
        p99 = self._percentile(latencies, 99)

        # Find last violation timestamp
        last_violation_timestamp = None
        for metric in reversed(self.metrics):
            if metric.first_token_latency_ms > self.sla_threshold_ms:
                last_violation_timestamp = metric.timestamp
                break

        return SLAStats(
            p50=round(p50, 2),
            p95=round(p95, 2),
            p99=round(p99, 2),
            count=count,
            violations=self._violation_count,
            last_violation_timestamp=last_violation_timestamp
        )

    def xǁSLAMonitorǁget_stats__mutmut_14(self) -> SLAStats:
        """
        Calculate current SLA statistics

        Returns:
            SLAStats with percentiles and violation count
        """
        if not self.metrics:
            return SLAStats(p50=0, p95=0, p99=1, count=0, violations=self._violation_count)

        latencies = sorted([m.first_token_latency_ms for m in self.metrics])
        count = len(latencies)

        p50 = self._percentile(latencies, 50)
        p95 = self._percentile(latencies, 95)
        p99 = self._percentile(latencies, 99)

        # Find last violation timestamp
        last_violation_timestamp = None
        for metric in reversed(self.metrics):
            if metric.first_token_latency_ms > self.sla_threshold_ms:
                last_violation_timestamp = metric.timestamp
                break

        return SLAStats(
            p50=round(p50, 2),
            p95=round(p95, 2),
            p99=round(p99, 2),
            count=count,
            violations=self._violation_count,
            last_violation_timestamp=last_violation_timestamp
        )

    def xǁSLAMonitorǁget_stats__mutmut_15(self) -> SLAStats:
        """
        Calculate current SLA statistics

        Returns:
            SLAStats with percentiles and violation count
        """
        if not self.metrics:
            return SLAStats(p50=0, p95=0, p99=0, count=1, violations=self._violation_count)

        latencies = sorted([m.first_token_latency_ms for m in self.metrics])
        count = len(latencies)

        p50 = self._percentile(latencies, 50)
        p95 = self._percentile(latencies, 95)
        p99 = self._percentile(latencies, 99)

        # Find last violation timestamp
        last_violation_timestamp = None
        for metric in reversed(self.metrics):
            if metric.first_token_latency_ms > self.sla_threshold_ms:
                last_violation_timestamp = metric.timestamp
                break

        return SLAStats(
            p50=round(p50, 2),
            p95=round(p95, 2),
            p99=round(p99, 2),
            count=count,
            violations=self._violation_count,
            last_violation_timestamp=last_violation_timestamp
        )

    def xǁSLAMonitorǁget_stats__mutmut_16(self) -> SLAStats:
        """
        Calculate current SLA statistics

        Returns:
            SLAStats with percentiles and violation count
        """
        if not self.metrics:
            return SLAStats(p50=0, p95=0, p99=0, count=0, violations=self._violation_count)

        latencies = None
        count = len(latencies)

        p50 = self._percentile(latencies, 50)
        p95 = self._percentile(latencies, 95)
        p99 = self._percentile(latencies, 99)

        # Find last violation timestamp
        last_violation_timestamp = None
        for metric in reversed(self.metrics):
            if metric.first_token_latency_ms > self.sla_threshold_ms:
                last_violation_timestamp = metric.timestamp
                break

        return SLAStats(
            p50=round(p50, 2),
            p95=round(p95, 2),
            p99=round(p99, 2),
            count=count,
            violations=self._violation_count,
            last_violation_timestamp=last_violation_timestamp
        )

    def xǁSLAMonitorǁget_stats__mutmut_17(self) -> SLAStats:
        """
        Calculate current SLA statistics

        Returns:
            SLAStats with percentiles and violation count
        """
        if not self.metrics:
            return SLAStats(p50=0, p95=0, p99=0, count=0, violations=self._violation_count)

        latencies = sorted(None)
        count = len(latencies)

        p50 = self._percentile(latencies, 50)
        p95 = self._percentile(latencies, 95)
        p99 = self._percentile(latencies, 99)

        # Find last violation timestamp
        last_violation_timestamp = None
        for metric in reversed(self.metrics):
            if metric.first_token_latency_ms > self.sla_threshold_ms:
                last_violation_timestamp = metric.timestamp
                break

        return SLAStats(
            p50=round(p50, 2),
            p95=round(p95, 2),
            p99=round(p99, 2),
            count=count,
            violations=self._violation_count,
            last_violation_timestamp=last_violation_timestamp
        )

    def xǁSLAMonitorǁget_stats__mutmut_18(self) -> SLAStats:
        """
        Calculate current SLA statistics

        Returns:
            SLAStats with percentiles and violation count
        """
        if not self.metrics:
            return SLAStats(p50=0, p95=0, p99=0, count=0, violations=self._violation_count)

        latencies = sorted([m.first_token_latency_ms for m in self.metrics])
        count = None

        p50 = self._percentile(latencies, 50)
        p95 = self._percentile(latencies, 95)
        p99 = self._percentile(latencies, 99)

        # Find last violation timestamp
        last_violation_timestamp = None
        for metric in reversed(self.metrics):
            if metric.first_token_latency_ms > self.sla_threshold_ms:
                last_violation_timestamp = metric.timestamp
                break

        return SLAStats(
            p50=round(p50, 2),
            p95=round(p95, 2),
            p99=round(p99, 2),
            count=count,
            violations=self._violation_count,
            last_violation_timestamp=last_violation_timestamp
        )

    def xǁSLAMonitorǁget_stats__mutmut_19(self) -> SLAStats:
        """
        Calculate current SLA statistics

        Returns:
            SLAStats with percentiles and violation count
        """
        if not self.metrics:
            return SLAStats(p50=0, p95=0, p99=0, count=0, violations=self._violation_count)

        latencies = sorted([m.first_token_latency_ms for m in self.metrics])
        count = len(latencies)

        p50 = None
        p95 = self._percentile(latencies, 95)
        p99 = self._percentile(latencies, 99)

        # Find last violation timestamp
        last_violation_timestamp = None
        for metric in reversed(self.metrics):
            if metric.first_token_latency_ms > self.sla_threshold_ms:
                last_violation_timestamp = metric.timestamp
                break

        return SLAStats(
            p50=round(p50, 2),
            p95=round(p95, 2),
            p99=round(p99, 2),
            count=count,
            violations=self._violation_count,
            last_violation_timestamp=last_violation_timestamp
        )

    def xǁSLAMonitorǁget_stats__mutmut_20(self) -> SLAStats:
        """
        Calculate current SLA statistics

        Returns:
            SLAStats with percentiles and violation count
        """
        if not self.metrics:
            return SLAStats(p50=0, p95=0, p99=0, count=0, violations=self._violation_count)

        latencies = sorted([m.first_token_latency_ms for m in self.metrics])
        count = len(latencies)

        p50 = self._percentile(None, 50)
        p95 = self._percentile(latencies, 95)
        p99 = self._percentile(latencies, 99)

        # Find last violation timestamp
        last_violation_timestamp = None
        for metric in reversed(self.metrics):
            if metric.first_token_latency_ms > self.sla_threshold_ms:
                last_violation_timestamp = metric.timestamp
                break

        return SLAStats(
            p50=round(p50, 2),
            p95=round(p95, 2),
            p99=round(p99, 2),
            count=count,
            violations=self._violation_count,
            last_violation_timestamp=last_violation_timestamp
        )

    def xǁSLAMonitorǁget_stats__mutmut_21(self) -> SLAStats:
        """
        Calculate current SLA statistics

        Returns:
            SLAStats with percentiles and violation count
        """
        if not self.metrics:
            return SLAStats(p50=0, p95=0, p99=0, count=0, violations=self._violation_count)

        latencies = sorted([m.first_token_latency_ms for m in self.metrics])
        count = len(latencies)

        p50 = self._percentile(latencies, None)
        p95 = self._percentile(latencies, 95)
        p99 = self._percentile(latencies, 99)

        # Find last violation timestamp
        last_violation_timestamp = None
        for metric in reversed(self.metrics):
            if metric.first_token_latency_ms > self.sla_threshold_ms:
                last_violation_timestamp = metric.timestamp
                break

        return SLAStats(
            p50=round(p50, 2),
            p95=round(p95, 2),
            p99=round(p99, 2),
            count=count,
            violations=self._violation_count,
            last_violation_timestamp=last_violation_timestamp
        )

    def xǁSLAMonitorǁget_stats__mutmut_22(self) -> SLAStats:
        """
        Calculate current SLA statistics

        Returns:
            SLAStats with percentiles and violation count
        """
        if not self.metrics:
            return SLAStats(p50=0, p95=0, p99=0, count=0, violations=self._violation_count)

        latencies = sorted([m.first_token_latency_ms for m in self.metrics])
        count = len(latencies)

        p50 = self._percentile(50)
        p95 = self._percentile(latencies, 95)
        p99 = self._percentile(latencies, 99)

        # Find last violation timestamp
        last_violation_timestamp = None
        for metric in reversed(self.metrics):
            if metric.first_token_latency_ms > self.sla_threshold_ms:
                last_violation_timestamp = metric.timestamp
                break

        return SLAStats(
            p50=round(p50, 2),
            p95=round(p95, 2),
            p99=round(p99, 2),
            count=count,
            violations=self._violation_count,
            last_violation_timestamp=last_violation_timestamp
        )

    def xǁSLAMonitorǁget_stats__mutmut_23(self) -> SLAStats:
        """
        Calculate current SLA statistics

        Returns:
            SLAStats with percentiles and violation count
        """
        if not self.metrics:
            return SLAStats(p50=0, p95=0, p99=0, count=0, violations=self._violation_count)

        latencies = sorted([m.first_token_latency_ms for m in self.metrics])
        count = len(latencies)

        p50 = self._percentile(latencies, )
        p95 = self._percentile(latencies, 95)
        p99 = self._percentile(latencies, 99)

        # Find last violation timestamp
        last_violation_timestamp = None
        for metric in reversed(self.metrics):
            if metric.first_token_latency_ms > self.sla_threshold_ms:
                last_violation_timestamp = metric.timestamp
                break

        return SLAStats(
            p50=round(p50, 2),
            p95=round(p95, 2),
            p99=round(p99, 2),
            count=count,
            violations=self._violation_count,
            last_violation_timestamp=last_violation_timestamp
        )

    def xǁSLAMonitorǁget_stats__mutmut_24(self) -> SLAStats:
        """
        Calculate current SLA statistics

        Returns:
            SLAStats with percentiles and violation count
        """
        if not self.metrics:
            return SLAStats(p50=0, p95=0, p99=0, count=0, violations=self._violation_count)

        latencies = sorted([m.first_token_latency_ms for m in self.metrics])
        count = len(latencies)

        p50 = self._percentile(latencies, 51)
        p95 = self._percentile(latencies, 95)
        p99 = self._percentile(latencies, 99)

        # Find last violation timestamp
        last_violation_timestamp = None
        for metric in reversed(self.metrics):
            if metric.first_token_latency_ms > self.sla_threshold_ms:
                last_violation_timestamp = metric.timestamp
                break

        return SLAStats(
            p50=round(p50, 2),
            p95=round(p95, 2),
            p99=round(p99, 2),
            count=count,
            violations=self._violation_count,
            last_violation_timestamp=last_violation_timestamp
        )

    def xǁSLAMonitorǁget_stats__mutmut_25(self) -> SLAStats:
        """
        Calculate current SLA statistics

        Returns:
            SLAStats with percentiles and violation count
        """
        if not self.metrics:
            return SLAStats(p50=0, p95=0, p99=0, count=0, violations=self._violation_count)

        latencies = sorted([m.first_token_latency_ms for m in self.metrics])
        count = len(latencies)

        p50 = self._percentile(latencies, 50)
        p95 = None
        p99 = self._percentile(latencies, 99)

        # Find last violation timestamp
        last_violation_timestamp = None
        for metric in reversed(self.metrics):
            if metric.first_token_latency_ms > self.sla_threshold_ms:
                last_violation_timestamp = metric.timestamp
                break

        return SLAStats(
            p50=round(p50, 2),
            p95=round(p95, 2),
            p99=round(p99, 2),
            count=count,
            violations=self._violation_count,
            last_violation_timestamp=last_violation_timestamp
        )

    def xǁSLAMonitorǁget_stats__mutmut_26(self) -> SLAStats:
        """
        Calculate current SLA statistics

        Returns:
            SLAStats with percentiles and violation count
        """
        if not self.metrics:
            return SLAStats(p50=0, p95=0, p99=0, count=0, violations=self._violation_count)

        latencies = sorted([m.first_token_latency_ms for m in self.metrics])
        count = len(latencies)

        p50 = self._percentile(latencies, 50)
        p95 = self._percentile(None, 95)
        p99 = self._percentile(latencies, 99)

        # Find last violation timestamp
        last_violation_timestamp = None
        for metric in reversed(self.metrics):
            if metric.first_token_latency_ms > self.sla_threshold_ms:
                last_violation_timestamp = metric.timestamp
                break

        return SLAStats(
            p50=round(p50, 2),
            p95=round(p95, 2),
            p99=round(p99, 2),
            count=count,
            violations=self._violation_count,
            last_violation_timestamp=last_violation_timestamp
        )

    def xǁSLAMonitorǁget_stats__mutmut_27(self) -> SLAStats:
        """
        Calculate current SLA statistics

        Returns:
            SLAStats with percentiles and violation count
        """
        if not self.metrics:
            return SLAStats(p50=0, p95=0, p99=0, count=0, violations=self._violation_count)

        latencies = sorted([m.first_token_latency_ms for m in self.metrics])
        count = len(latencies)

        p50 = self._percentile(latencies, 50)
        p95 = self._percentile(latencies, None)
        p99 = self._percentile(latencies, 99)

        # Find last violation timestamp
        last_violation_timestamp = None
        for metric in reversed(self.metrics):
            if metric.first_token_latency_ms > self.sla_threshold_ms:
                last_violation_timestamp = metric.timestamp
                break

        return SLAStats(
            p50=round(p50, 2),
            p95=round(p95, 2),
            p99=round(p99, 2),
            count=count,
            violations=self._violation_count,
            last_violation_timestamp=last_violation_timestamp
        )

    def xǁSLAMonitorǁget_stats__mutmut_28(self) -> SLAStats:
        """
        Calculate current SLA statistics

        Returns:
            SLAStats with percentiles and violation count
        """
        if not self.metrics:
            return SLAStats(p50=0, p95=0, p99=0, count=0, violations=self._violation_count)

        latencies = sorted([m.first_token_latency_ms for m in self.metrics])
        count = len(latencies)

        p50 = self._percentile(latencies, 50)
        p95 = self._percentile(95)
        p99 = self._percentile(latencies, 99)

        # Find last violation timestamp
        last_violation_timestamp = None
        for metric in reversed(self.metrics):
            if metric.first_token_latency_ms > self.sla_threshold_ms:
                last_violation_timestamp = metric.timestamp
                break

        return SLAStats(
            p50=round(p50, 2),
            p95=round(p95, 2),
            p99=round(p99, 2),
            count=count,
            violations=self._violation_count,
            last_violation_timestamp=last_violation_timestamp
        )

    def xǁSLAMonitorǁget_stats__mutmut_29(self) -> SLAStats:
        """
        Calculate current SLA statistics

        Returns:
            SLAStats with percentiles and violation count
        """
        if not self.metrics:
            return SLAStats(p50=0, p95=0, p99=0, count=0, violations=self._violation_count)

        latencies = sorted([m.first_token_latency_ms for m in self.metrics])
        count = len(latencies)

        p50 = self._percentile(latencies, 50)
        p95 = self._percentile(latencies, )
        p99 = self._percentile(latencies, 99)

        # Find last violation timestamp
        last_violation_timestamp = None
        for metric in reversed(self.metrics):
            if metric.first_token_latency_ms > self.sla_threshold_ms:
                last_violation_timestamp = metric.timestamp
                break

        return SLAStats(
            p50=round(p50, 2),
            p95=round(p95, 2),
            p99=round(p99, 2),
            count=count,
            violations=self._violation_count,
            last_violation_timestamp=last_violation_timestamp
        )

    def xǁSLAMonitorǁget_stats__mutmut_30(self) -> SLAStats:
        """
        Calculate current SLA statistics

        Returns:
            SLAStats with percentiles and violation count
        """
        if not self.metrics:
            return SLAStats(p50=0, p95=0, p99=0, count=0, violations=self._violation_count)

        latencies = sorted([m.first_token_latency_ms for m in self.metrics])
        count = len(latencies)

        p50 = self._percentile(latencies, 50)
        p95 = self._percentile(latencies, 96)
        p99 = self._percentile(latencies, 99)

        # Find last violation timestamp
        last_violation_timestamp = None
        for metric in reversed(self.metrics):
            if metric.first_token_latency_ms > self.sla_threshold_ms:
                last_violation_timestamp = metric.timestamp
                break

        return SLAStats(
            p50=round(p50, 2),
            p95=round(p95, 2),
            p99=round(p99, 2),
            count=count,
            violations=self._violation_count,
            last_violation_timestamp=last_violation_timestamp
        )

    def xǁSLAMonitorǁget_stats__mutmut_31(self) -> SLAStats:
        """
        Calculate current SLA statistics

        Returns:
            SLAStats with percentiles and violation count
        """
        if not self.metrics:
            return SLAStats(p50=0, p95=0, p99=0, count=0, violations=self._violation_count)

        latencies = sorted([m.first_token_latency_ms for m in self.metrics])
        count = len(latencies)

        p50 = self._percentile(latencies, 50)
        p95 = self._percentile(latencies, 95)
        p99 = None

        # Find last violation timestamp
        last_violation_timestamp = None
        for metric in reversed(self.metrics):
            if metric.first_token_latency_ms > self.sla_threshold_ms:
                last_violation_timestamp = metric.timestamp
                break

        return SLAStats(
            p50=round(p50, 2),
            p95=round(p95, 2),
            p99=round(p99, 2),
            count=count,
            violations=self._violation_count,
            last_violation_timestamp=last_violation_timestamp
        )

    def xǁSLAMonitorǁget_stats__mutmut_32(self) -> SLAStats:
        """
        Calculate current SLA statistics

        Returns:
            SLAStats with percentiles and violation count
        """
        if not self.metrics:
            return SLAStats(p50=0, p95=0, p99=0, count=0, violations=self._violation_count)

        latencies = sorted([m.first_token_latency_ms for m in self.metrics])
        count = len(latencies)

        p50 = self._percentile(latencies, 50)
        p95 = self._percentile(latencies, 95)
        p99 = self._percentile(None, 99)

        # Find last violation timestamp
        last_violation_timestamp = None
        for metric in reversed(self.metrics):
            if metric.first_token_latency_ms > self.sla_threshold_ms:
                last_violation_timestamp = metric.timestamp
                break

        return SLAStats(
            p50=round(p50, 2),
            p95=round(p95, 2),
            p99=round(p99, 2),
            count=count,
            violations=self._violation_count,
            last_violation_timestamp=last_violation_timestamp
        )

    def xǁSLAMonitorǁget_stats__mutmut_33(self) -> SLAStats:
        """
        Calculate current SLA statistics

        Returns:
            SLAStats with percentiles and violation count
        """
        if not self.metrics:
            return SLAStats(p50=0, p95=0, p99=0, count=0, violations=self._violation_count)

        latencies = sorted([m.first_token_latency_ms for m in self.metrics])
        count = len(latencies)

        p50 = self._percentile(latencies, 50)
        p95 = self._percentile(latencies, 95)
        p99 = self._percentile(latencies, None)

        # Find last violation timestamp
        last_violation_timestamp = None
        for metric in reversed(self.metrics):
            if metric.first_token_latency_ms > self.sla_threshold_ms:
                last_violation_timestamp = metric.timestamp
                break

        return SLAStats(
            p50=round(p50, 2),
            p95=round(p95, 2),
            p99=round(p99, 2),
            count=count,
            violations=self._violation_count,
            last_violation_timestamp=last_violation_timestamp
        )

    def xǁSLAMonitorǁget_stats__mutmut_34(self) -> SLAStats:
        """
        Calculate current SLA statistics

        Returns:
            SLAStats with percentiles and violation count
        """
        if not self.metrics:
            return SLAStats(p50=0, p95=0, p99=0, count=0, violations=self._violation_count)

        latencies = sorted([m.first_token_latency_ms for m in self.metrics])
        count = len(latencies)

        p50 = self._percentile(latencies, 50)
        p95 = self._percentile(latencies, 95)
        p99 = self._percentile(99)

        # Find last violation timestamp
        last_violation_timestamp = None
        for metric in reversed(self.metrics):
            if metric.first_token_latency_ms > self.sla_threshold_ms:
                last_violation_timestamp = metric.timestamp
                break

        return SLAStats(
            p50=round(p50, 2),
            p95=round(p95, 2),
            p99=round(p99, 2),
            count=count,
            violations=self._violation_count,
            last_violation_timestamp=last_violation_timestamp
        )

    def xǁSLAMonitorǁget_stats__mutmut_35(self) -> SLAStats:
        """
        Calculate current SLA statistics

        Returns:
            SLAStats with percentiles and violation count
        """
        if not self.metrics:
            return SLAStats(p50=0, p95=0, p99=0, count=0, violations=self._violation_count)

        latencies = sorted([m.first_token_latency_ms for m in self.metrics])
        count = len(latencies)

        p50 = self._percentile(latencies, 50)
        p95 = self._percentile(latencies, 95)
        p99 = self._percentile(latencies, )

        # Find last violation timestamp
        last_violation_timestamp = None
        for metric in reversed(self.metrics):
            if metric.first_token_latency_ms > self.sla_threshold_ms:
                last_violation_timestamp = metric.timestamp
                break

        return SLAStats(
            p50=round(p50, 2),
            p95=round(p95, 2),
            p99=round(p99, 2),
            count=count,
            violations=self._violation_count,
            last_violation_timestamp=last_violation_timestamp
        )

    def xǁSLAMonitorǁget_stats__mutmut_36(self) -> SLAStats:
        """
        Calculate current SLA statistics

        Returns:
            SLAStats with percentiles and violation count
        """
        if not self.metrics:
            return SLAStats(p50=0, p95=0, p99=0, count=0, violations=self._violation_count)

        latencies = sorted([m.first_token_latency_ms for m in self.metrics])
        count = len(latencies)

        p50 = self._percentile(latencies, 50)
        p95 = self._percentile(latencies, 95)
        p99 = self._percentile(latencies, 100)

        # Find last violation timestamp
        last_violation_timestamp = None
        for metric in reversed(self.metrics):
            if metric.first_token_latency_ms > self.sla_threshold_ms:
                last_violation_timestamp = metric.timestamp
                break

        return SLAStats(
            p50=round(p50, 2),
            p95=round(p95, 2),
            p99=round(p99, 2),
            count=count,
            violations=self._violation_count,
            last_violation_timestamp=last_violation_timestamp
        )

    def xǁSLAMonitorǁget_stats__mutmut_37(self) -> SLAStats:
        """
        Calculate current SLA statistics

        Returns:
            SLAStats with percentiles and violation count
        """
        if not self.metrics:
            return SLAStats(p50=0, p95=0, p99=0, count=0, violations=self._violation_count)

        latencies = sorted([m.first_token_latency_ms for m in self.metrics])
        count = len(latencies)

        p50 = self._percentile(latencies, 50)
        p95 = self._percentile(latencies, 95)
        p99 = self._percentile(latencies, 99)

        # Find last violation timestamp
        last_violation_timestamp = ""
        for metric in reversed(self.metrics):
            if metric.first_token_latency_ms > self.sla_threshold_ms:
                last_violation_timestamp = metric.timestamp
                break

        return SLAStats(
            p50=round(p50, 2),
            p95=round(p95, 2),
            p99=round(p99, 2),
            count=count,
            violations=self._violation_count,
            last_violation_timestamp=last_violation_timestamp
        )

    def xǁSLAMonitorǁget_stats__mutmut_38(self) -> SLAStats:
        """
        Calculate current SLA statistics

        Returns:
            SLAStats with percentiles and violation count
        """
        if not self.metrics:
            return SLAStats(p50=0, p95=0, p99=0, count=0, violations=self._violation_count)

        latencies = sorted([m.first_token_latency_ms for m in self.metrics])
        count = len(latencies)

        p50 = self._percentile(latencies, 50)
        p95 = self._percentile(latencies, 95)
        p99 = self._percentile(latencies, 99)

        # Find last violation timestamp
        last_violation_timestamp = None
        for metric in reversed(None):
            if metric.first_token_latency_ms > self.sla_threshold_ms:
                last_violation_timestamp = metric.timestamp
                break

        return SLAStats(
            p50=round(p50, 2),
            p95=round(p95, 2),
            p99=round(p99, 2),
            count=count,
            violations=self._violation_count,
            last_violation_timestamp=last_violation_timestamp
        )

    def xǁSLAMonitorǁget_stats__mutmut_39(self) -> SLAStats:
        """
        Calculate current SLA statistics

        Returns:
            SLAStats with percentiles and violation count
        """
        if not self.metrics:
            return SLAStats(p50=0, p95=0, p99=0, count=0, violations=self._violation_count)

        latencies = sorted([m.first_token_latency_ms for m in self.metrics])
        count = len(latencies)

        p50 = self._percentile(latencies, 50)
        p95 = self._percentile(latencies, 95)
        p99 = self._percentile(latencies, 99)

        # Find last violation timestamp
        last_violation_timestamp = None
        for metric in reversed(self.metrics):
            if metric.first_token_latency_ms >= self.sla_threshold_ms:
                last_violation_timestamp = metric.timestamp
                break

        return SLAStats(
            p50=round(p50, 2),
            p95=round(p95, 2),
            p99=round(p99, 2),
            count=count,
            violations=self._violation_count,
            last_violation_timestamp=last_violation_timestamp
        )

    def xǁSLAMonitorǁget_stats__mutmut_40(self) -> SLAStats:
        """
        Calculate current SLA statistics

        Returns:
            SLAStats with percentiles and violation count
        """
        if not self.metrics:
            return SLAStats(p50=0, p95=0, p99=0, count=0, violations=self._violation_count)

        latencies = sorted([m.first_token_latency_ms for m in self.metrics])
        count = len(latencies)

        p50 = self._percentile(latencies, 50)
        p95 = self._percentile(latencies, 95)
        p99 = self._percentile(latencies, 99)

        # Find last violation timestamp
        last_violation_timestamp = None
        for metric in reversed(self.metrics):
            if metric.first_token_latency_ms > self.sla_threshold_ms:
                last_violation_timestamp = None
                break

        return SLAStats(
            p50=round(p50, 2),
            p95=round(p95, 2),
            p99=round(p99, 2),
            count=count,
            violations=self._violation_count,
            last_violation_timestamp=last_violation_timestamp
        )

    def xǁSLAMonitorǁget_stats__mutmut_41(self) -> SLAStats:
        """
        Calculate current SLA statistics

        Returns:
            SLAStats with percentiles and violation count
        """
        if not self.metrics:
            return SLAStats(p50=0, p95=0, p99=0, count=0, violations=self._violation_count)

        latencies = sorted([m.first_token_latency_ms for m in self.metrics])
        count = len(latencies)

        p50 = self._percentile(latencies, 50)
        p95 = self._percentile(latencies, 95)
        p99 = self._percentile(latencies, 99)

        # Find last violation timestamp
        last_violation_timestamp = None
        for metric in reversed(self.metrics):
            if metric.first_token_latency_ms > self.sla_threshold_ms:
                last_violation_timestamp = metric.timestamp
                return

        return SLAStats(
            p50=round(p50, 2),
            p95=round(p95, 2),
            p99=round(p99, 2),
            count=count,
            violations=self._violation_count,
            last_violation_timestamp=last_violation_timestamp
        )

    def xǁSLAMonitorǁget_stats__mutmut_42(self) -> SLAStats:
        """
        Calculate current SLA statistics

        Returns:
            SLAStats with percentiles and violation count
        """
        if not self.metrics:
            return SLAStats(p50=0, p95=0, p99=0, count=0, violations=self._violation_count)

        latencies = sorted([m.first_token_latency_ms for m in self.metrics])
        count = len(latencies)

        p50 = self._percentile(latencies, 50)
        p95 = self._percentile(latencies, 95)
        p99 = self._percentile(latencies, 99)

        # Find last violation timestamp
        last_violation_timestamp = None
        for metric in reversed(self.metrics):
            if metric.first_token_latency_ms > self.sla_threshold_ms:
                last_violation_timestamp = metric.timestamp
                break

        return SLAStats(
            p50=None,
            p95=round(p95, 2),
            p99=round(p99, 2),
            count=count,
            violations=self._violation_count,
            last_violation_timestamp=last_violation_timestamp
        )

    def xǁSLAMonitorǁget_stats__mutmut_43(self) -> SLAStats:
        """
        Calculate current SLA statistics

        Returns:
            SLAStats with percentiles and violation count
        """
        if not self.metrics:
            return SLAStats(p50=0, p95=0, p99=0, count=0, violations=self._violation_count)

        latencies = sorted([m.first_token_latency_ms for m in self.metrics])
        count = len(latencies)

        p50 = self._percentile(latencies, 50)
        p95 = self._percentile(latencies, 95)
        p99 = self._percentile(latencies, 99)

        # Find last violation timestamp
        last_violation_timestamp = None
        for metric in reversed(self.metrics):
            if metric.first_token_latency_ms > self.sla_threshold_ms:
                last_violation_timestamp = metric.timestamp
                break

        return SLAStats(
            p50=round(p50, 2),
            p95=None,
            p99=round(p99, 2),
            count=count,
            violations=self._violation_count,
            last_violation_timestamp=last_violation_timestamp
        )

    def xǁSLAMonitorǁget_stats__mutmut_44(self) -> SLAStats:
        """
        Calculate current SLA statistics

        Returns:
            SLAStats with percentiles and violation count
        """
        if not self.metrics:
            return SLAStats(p50=0, p95=0, p99=0, count=0, violations=self._violation_count)

        latencies = sorted([m.first_token_latency_ms for m in self.metrics])
        count = len(latencies)

        p50 = self._percentile(latencies, 50)
        p95 = self._percentile(latencies, 95)
        p99 = self._percentile(latencies, 99)

        # Find last violation timestamp
        last_violation_timestamp = None
        for metric in reversed(self.metrics):
            if metric.first_token_latency_ms > self.sla_threshold_ms:
                last_violation_timestamp = metric.timestamp
                break

        return SLAStats(
            p50=round(p50, 2),
            p95=round(p95, 2),
            p99=None,
            count=count,
            violations=self._violation_count,
            last_violation_timestamp=last_violation_timestamp
        )

    def xǁSLAMonitorǁget_stats__mutmut_45(self) -> SLAStats:
        """
        Calculate current SLA statistics

        Returns:
            SLAStats with percentiles and violation count
        """
        if not self.metrics:
            return SLAStats(p50=0, p95=0, p99=0, count=0, violations=self._violation_count)

        latencies = sorted([m.first_token_latency_ms for m in self.metrics])
        count = len(latencies)

        p50 = self._percentile(latencies, 50)
        p95 = self._percentile(latencies, 95)
        p99 = self._percentile(latencies, 99)

        # Find last violation timestamp
        last_violation_timestamp = None
        for metric in reversed(self.metrics):
            if metric.first_token_latency_ms > self.sla_threshold_ms:
                last_violation_timestamp = metric.timestamp
                break

        return SLAStats(
            p50=round(p50, 2),
            p95=round(p95, 2),
            p99=round(p99, 2),
            count=None,
            violations=self._violation_count,
            last_violation_timestamp=last_violation_timestamp
        )

    def xǁSLAMonitorǁget_stats__mutmut_46(self) -> SLAStats:
        """
        Calculate current SLA statistics

        Returns:
            SLAStats with percentiles and violation count
        """
        if not self.metrics:
            return SLAStats(p50=0, p95=0, p99=0, count=0, violations=self._violation_count)

        latencies = sorted([m.first_token_latency_ms for m in self.metrics])
        count = len(latencies)

        p50 = self._percentile(latencies, 50)
        p95 = self._percentile(latencies, 95)
        p99 = self._percentile(latencies, 99)

        # Find last violation timestamp
        last_violation_timestamp = None
        for metric in reversed(self.metrics):
            if metric.first_token_latency_ms > self.sla_threshold_ms:
                last_violation_timestamp = metric.timestamp
                break

        return SLAStats(
            p50=round(p50, 2),
            p95=round(p95, 2),
            p99=round(p99, 2),
            count=count,
            violations=None,
            last_violation_timestamp=last_violation_timestamp
        )

    def xǁSLAMonitorǁget_stats__mutmut_47(self) -> SLAStats:
        """
        Calculate current SLA statistics

        Returns:
            SLAStats with percentiles and violation count
        """
        if not self.metrics:
            return SLAStats(p50=0, p95=0, p99=0, count=0, violations=self._violation_count)

        latencies = sorted([m.first_token_latency_ms for m in self.metrics])
        count = len(latencies)

        p50 = self._percentile(latencies, 50)
        p95 = self._percentile(latencies, 95)
        p99 = self._percentile(latencies, 99)

        # Find last violation timestamp
        last_violation_timestamp = None
        for metric in reversed(self.metrics):
            if metric.first_token_latency_ms > self.sla_threshold_ms:
                last_violation_timestamp = metric.timestamp
                break

        return SLAStats(
            p50=round(p50, 2),
            p95=round(p95, 2),
            p99=round(p99, 2),
            count=count,
            violations=self._violation_count,
            last_violation_timestamp=None
        )

    def xǁSLAMonitorǁget_stats__mutmut_48(self) -> SLAStats:
        """
        Calculate current SLA statistics

        Returns:
            SLAStats with percentiles and violation count
        """
        if not self.metrics:
            return SLAStats(p50=0, p95=0, p99=0, count=0, violations=self._violation_count)

        latencies = sorted([m.first_token_latency_ms for m in self.metrics])
        count = len(latencies)

        p50 = self._percentile(latencies, 50)
        p95 = self._percentile(latencies, 95)
        p99 = self._percentile(latencies, 99)

        # Find last violation timestamp
        last_violation_timestamp = None
        for metric in reversed(self.metrics):
            if metric.first_token_latency_ms > self.sla_threshold_ms:
                last_violation_timestamp = metric.timestamp
                break

        return SLAStats(
            p95=round(p95, 2),
            p99=round(p99, 2),
            count=count,
            violations=self._violation_count,
            last_violation_timestamp=last_violation_timestamp
        )

    def xǁSLAMonitorǁget_stats__mutmut_49(self) -> SLAStats:
        """
        Calculate current SLA statistics

        Returns:
            SLAStats with percentiles and violation count
        """
        if not self.metrics:
            return SLAStats(p50=0, p95=0, p99=0, count=0, violations=self._violation_count)

        latencies = sorted([m.first_token_latency_ms for m in self.metrics])
        count = len(latencies)

        p50 = self._percentile(latencies, 50)
        p95 = self._percentile(latencies, 95)
        p99 = self._percentile(latencies, 99)

        # Find last violation timestamp
        last_violation_timestamp = None
        for metric in reversed(self.metrics):
            if metric.first_token_latency_ms > self.sla_threshold_ms:
                last_violation_timestamp = metric.timestamp
                break

        return SLAStats(
            p50=round(p50, 2),
            p99=round(p99, 2),
            count=count,
            violations=self._violation_count,
            last_violation_timestamp=last_violation_timestamp
        )

    def xǁSLAMonitorǁget_stats__mutmut_50(self) -> SLAStats:
        """
        Calculate current SLA statistics

        Returns:
            SLAStats with percentiles and violation count
        """
        if not self.metrics:
            return SLAStats(p50=0, p95=0, p99=0, count=0, violations=self._violation_count)

        latencies = sorted([m.first_token_latency_ms for m in self.metrics])
        count = len(latencies)

        p50 = self._percentile(latencies, 50)
        p95 = self._percentile(latencies, 95)
        p99 = self._percentile(latencies, 99)

        # Find last violation timestamp
        last_violation_timestamp = None
        for metric in reversed(self.metrics):
            if metric.first_token_latency_ms > self.sla_threshold_ms:
                last_violation_timestamp = metric.timestamp
                break

        return SLAStats(
            p50=round(p50, 2),
            p95=round(p95, 2),
            count=count,
            violations=self._violation_count,
            last_violation_timestamp=last_violation_timestamp
        )

    def xǁSLAMonitorǁget_stats__mutmut_51(self) -> SLAStats:
        """
        Calculate current SLA statistics

        Returns:
            SLAStats with percentiles and violation count
        """
        if not self.metrics:
            return SLAStats(p50=0, p95=0, p99=0, count=0, violations=self._violation_count)

        latencies = sorted([m.first_token_latency_ms for m in self.metrics])
        count = len(latencies)

        p50 = self._percentile(latencies, 50)
        p95 = self._percentile(latencies, 95)
        p99 = self._percentile(latencies, 99)

        # Find last violation timestamp
        last_violation_timestamp = None
        for metric in reversed(self.metrics):
            if metric.first_token_latency_ms > self.sla_threshold_ms:
                last_violation_timestamp = metric.timestamp
                break

        return SLAStats(
            p50=round(p50, 2),
            p95=round(p95, 2),
            p99=round(p99, 2),
            violations=self._violation_count,
            last_violation_timestamp=last_violation_timestamp
        )

    def xǁSLAMonitorǁget_stats__mutmut_52(self) -> SLAStats:
        """
        Calculate current SLA statistics

        Returns:
            SLAStats with percentiles and violation count
        """
        if not self.metrics:
            return SLAStats(p50=0, p95=0, p99=0, count=0, violations=self._violation_count)

        latencies = sorted([m.first_token_latency_ms for m in self.metrics])
        count = len(latencies)

        p50 = self._percentile(latencies, 50)
        p95 = self._percentile(latencies, 95)
        p99 = self._percentile(latencies, 99)

        # Find last violation timestamp
        last_violation_timestamp = None
        for metric in reversed(self.metrics):
            if metric.first_token_latency_ms > self.sla_threshold_ms:
                last_violation_timestamp = metric.timestamp
                break

        return SLAStats(
            p50=round(p50, 2),
            p95=round(p95, 2),
            p99=round(p99, 2),
            count=count,
            last_violation_timestamp=last_violation_timestamp
        )

    def xǁSLAMonitorǁget_stats__mutmut_53(self) -> SLAStats:
        """
        Calculate current SLA statistics

        Returns:
            SLAStats with percentiles and violation count
        """
        if not self.metrics:
            return SLAStats(p50=0, p95=0, p99=0, count=0, violations=self._violation_count)

        latencies = sorted([m.first_token_latency_ms for m in self.metrics])
        count = len(latencies)

        p50 = self._percentile(latencies, 50)
        p95 = self._percentile(latencies, 95)
        p99 = self._percentile(latencies, 99)

        # Find last violation timestamp
        last_violation_timestamp = None
        for metric in reversed(self.metrics):
            if metric.first_token_latency_ms > self.sla_threshold_ms:
                last_violation_timestamp = metric.timestamp
                break

        return SLAStats(
            p50=round(p50, 2),
            p95=round(p95, 2),
            p99=round(p99, 2),
            count=count,
            violations=self._violation_count,
            )

    def xǁSLAMonitorǁget_stats__mutmut_54(self) -> SLAStats:
        """
        Calculate current SLA statistics

        Returns:
            SLAStats with percentiles and violation count
        """
        if not self.metrics:
            return SLAStats(p50=0, p95=0, p99=0, count=0, violations=self._violation_count)

        latencies = sorted([m.first_token_latency_ms for m in self.metrics])
        count = len(latencies)

        p50 = self._percentile(latencies, 50)
        p95 = self._percentile(latencies, 95)
        p99 = self._percentile(latencies, 99)

        # Find last violation timestamp
        last_violation_timestamp = None
        for metric in reversed(self.metrics):
            if metric.first_token_latency_ms > self.sla_threshold_ms:
                last_violation_timestamp = metric.timestamp
                break

        return SLAStats(
            p50=round(None, 2),
            p95=round(p95, 2),
            p99=round(p99, 2),
            count=count,
            violations=self._violation_count,
            last_violation_timestamp=last_violation_timestamp
        )

    def xǁSLAMonitorǁget_stats__mutmut_55(self) -> SLAStats:
        """
        Calculate current SLA statistics

        Returns:
            SLAStats with percentiles and violation count
        """
        if not self.metrics:
            return SLAStats(p50=0, p95=0, p99=0, count=0, violations=self._violation_count)

        latencies = sorted([m.first_token_latency_ms for m in self.metrics])
        count = len(latencies)

        p50 = self._percentile(latencies, 50)
        p95 = self._percentile(latencies, 95)
        p99 = self._percentile(latencies, 99)

        # Find last violation timestamp
        last_violation_timestamp = None
        for metric in reversed(self.metrics):
            if metric.first_token_latency_ms > self.sla_threshold_ms:
                last_violation_timestamp = metric.timestamp
                break

        return SLAStats(
            p50=round(p50, None),
            p95=round(p95, 2),
            p99=round(p99, 2),
            count=count,
            violations=self._violation_count,
            last_violation_timestamp=last_violation_timestamp
        )

    def xǁSLAMonitorǁget_stats__mutmut_56(self) -> SLAStats:
        """
        Calculate current SLA statistics

        Returns:
            SLAStats with percentiles and violation count
        """
        if not self.metrics:
            return SLAStats(p50=0, p95=0, p99=0, count=0, violations=self._violation_count)

        latencies = sorted([m.first_token_latency_ms for m in self.metrics])
        count = len(latencies)

        p50 = self._percentile(latencies, 50)
        p95 = self._percentile(latencies, 95)
        p99 = self._percentile(latencies, 99)

        # Find last violation timestamp
        last_violation_timestamp = None
        for metric in reversed(self.metrics):
            if metric.first_token_latency_ms > self.sla_threshold_ms:
                last_violation_timestamp = metric.timestamp
                break

        return SLAStats(
            p50=round(2),
            p95=round(p95, 2),
            p99=round(p99, 2),
            count=count,
            violations=self._violation_count,
            last_violation_timestamp=last_violation_timestamp
        )

    def xǁSLAMonitorǁget_stats__mutmut_57(self) -> SLAStats:
        """
        Calculate current SLA statistics

        Returns:
            SLAStats with percentiles and violation count
        """
        if not self.metrics:
            return SLAStats(p50=0, p95=0, p99=0, count=0, violations=self._violation_count)

        latencies = sorted([m.first_token_latency_ms for m in self.metrics])
        count = len(latencies)

        p50 = self._percentile(latencies, 50)
        p95 = self._percentile(latencies, 95)
        p99 = self._percentile(latencies, 99)

        # Find last violation timestamp
        last_violation_timestamp = None
        for metric in reversed(self.metrics):
            if metric.first_token_latency_ms > self.sla_threshold_ms:
                last_violation_timestamp = metric.timestamp
                break

        return SLAStats(
            p50=round(p50, ),
            p95=round(p95, 2),
            p99=round(p99, 2),
            count=count,
            violations=self._violation_count,
            last_violation_timestamp=last_violation_timestamp
        )

    def xǁSLAMonitorǁget_stats__mutmut_58(self) -> SLAStats:
        """
        Calculate current SLA statistics

        Returns:
            SLAStats with percentiles and violation count
        """
        if not self.metrics:
            return SLAStats(p50=0, p95=0, p99=0, count=0, violations=self._violation_count)

        latencies = sorted([m.first_token_latency_ms for m in self.metrics])
        count = len(latencies)

        p50 = self._percentile(latencies, 50)
        p95 = self._percentile(latencies, 95)
        p99 = self._percentile(latencies, 99)

        # Find last violation timestamp
        last_violation_timestamp = None
        for metric in reversed(self.metrics):
            if metric.first_token_latency_ms > self.sla_threshold_ms:
                last_violation_timestamp = metric.timestamp
                break

        return SLAStats(
            p50=round(p50, 3),
            p95=round(p95, 2),
            p99=round(p99, 2),
            count=count,
            violations=self._violation_count,
            last_violation_timestamp=last_violation_timestamp
        )

    def xǁSLAMonitorǁget_stats__mutmut_59(self) -> SLAStats:
        """
        Calculate current SLA statistics

        Returns:
            SLAStats with percentiles and violation count
        """
        if not self.metrics:
            return SLAStats(p50=0, p95=0, p99=0, count=0, violations=self._violation_count)

        latencies = sorted([m.first_token_latency_ms for m in self.metrics])
        count = len(latencies)

        p50 = self._percentile(latencies, 50)
        p95 = self._percentile(latencies, 95)
        p99 = self._percentile(latencies, 99)

        # Find last violation timestamp
        last_violation_timestamp = None
        for metric in reversed(self.metrics):
            if metric.first_token_latency_ms > self.sla_threshold_ms:
                last_violation_timestamp = metric.timestamp
                break

        return SLAStats(
            p50=round(p50, 2),
            p95=round(None, 2),
            p99=round(p99, 2),
            count=count,
            violations=self._violation_count,
            last_violation_timestamp=last_violation_timestamp
        )

    def xǁSLAMonitorǁget_stats__mutmut_60(self) -> SLAStats:
        """
        Calculate current SLA statistics

        Returns:
            SLAStats with percentiles and violation count
        """
        if not self.metrics:
            return SLAStats(p50=0, p95=0, p99=0, count=0, violations=self._violation_count)

        latencies = sorted([m.first_token_latency_ms for m in self.metrics])
        count = len(latencies)

        p50 = self._percentile(latencies, 50)
        p95 = self._percentile(latencies, 95)
        p99 = self._percentile(latencies, 99)

        # Find last violation timestamp
        last_violation_timestamp = None
        for metric in reversed(self.metrics):
            if metric.first_token_latency_ms > self.sla_threshold_ms:
                last_violation_timestamp = metric.timestamp
                break

        return SLAStats(
            p50=round(p50, 2),
            p95=round(p95, None),
            p99=round(p99, 2),
            count=count,
            violations=self._violation_count,
            last_violation_timestamp=last_violation_timestamp
        )

    def xǁSLAMonitorǁget_stats__mutmut_61(self) -> SLAStats:
        """
        Calculate current SLA statistics

        Returns:
            SLAStats with percentiles and violation count
        """
        if not self.metrics:
            return SLAStats(p50=0, p95=0, p99=0, count=0, violations=self._violation_count)

        latencies = sorted([m.first_token_latency_ms for m in self.metrics])
        count = len(latencies)

        p50 = self._percentile(latencies, 50)
        p95 = self._percentile(latencies, 95)
        p99 = self._percentile(latencies, 99)

        # Find last violation timestamp
        last_violation_timestamp = None
        for metric in reversed(self.metrics):
            if metric.first_token_latency_ms > self.sla_threshold_ms:
                last_violation_timestamp = metric.timestamp
                break

        return SLAStats(
            p50=round(p50, 2),
            p95=round(2),
            p99=round(p99, 2),
            count=count,
            violations=self._violation_count,
            last_violation_timestamp=last_violation_timestamp
        )

    def xǁSLAMonitorǁget_stats__mutmut_62(self) -> SLAStats:
        """
        Calculate current SLA statistics

        Returns:
            SLAStats with percentiles and violation count
        """
        if not self.metrics:
            return SLAStats(p50=0, p95=0, p99=0, count=0, violations=self._violation_count)

        latencies = sorted([m.first_token_latency_ms for m in self.metrics])
        count = len(latencies)

        p50 = self._percentile(latencies, 50)
        p95 = self._percentile(latencies, 95)
        p99 = self._percentile(latencies, 99)

        # Find last violation timestamp
        last_violation_timestamp = None
        for metric in reversed(self.metrics):
            if metric.first_token_latency_ms > self.sla_threshold_ms:
                last_violation_timestamp = metric.timestamp
                break

        return SLAStats(
            p50=round(p50, 2),
            p95=round(p95, ),
            p99=round(p99, 2),
            count=count,
            violations=self._violation_count,
            last_violation_timestamp=last_violation_timestamp
        )

    def xǁSLAMonitorǁget_stats__mutmut_63(self) -> SLAStats:
        """
        Calculate current SLA statistics

        Returns:
            SLAStats with percentiles and violation count
        """
        if not self.metrics:
            return SLAStats(p50=0, p95=0, p99=0, count=0, violations=self._violation_count)

        latencies = sorted([m.first_token_latency_ms for m in self.metrics])
        count = len(latencies)

        p50 = self._percentile(latencies, 50)
        p95 = self._percentile(latencies, 95)
        p99 = self._percentile(latencies, 99)

        # Find last violation timestamp
        last_violation_timestamp = None
        for metric in reversed(self.metrics):
            if metric.first_token_latency_ms > self.sla_threshold_ms:
                last_violation_timestamp = metric.timestamp
                break

        return SLAStats(
            p50=round(p50, 2),
            p95=round(p95, 3),
            p99=round(p99, 2),
            count=count,
            violations=self._violation_count,
            last_violation_timestamp=last_violation_timestamp
        )

    def xǁSLAMonitorǁget_stats__mutmut_64(self) -> SLAStats:
        """
        Calculate current SLA statistics

        Returns:
            SLAStats with percentiles and violation count
        """
        if not self.metrics:
            return SLAStats(p50=0, p95=0, p99=0, count=0, violations=self._violation_count)

        latencies = sorted([m.first_token_latency_ms for m in self.metrics])
        count = len(latencies)

        p50 = self._percentile(latencies, 50)
        p95 = self._percentile(latencies, 95)
        p99 = self._percentile(latencies, 99)

        # Find last violation timestamp
        last_violation_timestamp = None
        for metric in reversed(self.metrics):
            if metric.first_token_latency_ms > self.sla_threshold_ms:
                last_violation_timestamp = metric.timestamp
                break

        return SLAStats(
            p50=round(p50, 2),
            p95=round(p95, 2),
            p99=round(None, 2),
            count=count,
            violations=self._violation_count,
            last_violation_timestamp=last_violation_timestamp
        )

    def xǁSLAMonitorǁget_stats__mutmut_65(self) -> SLAStats:
        """
        Calculate current SLA statistics

        Returns:
            SLAStats with percentiles and violation count
        """
        if not self.metrics:
            return SLAStats(p50=0, p95=0, p99=0, count=0, violations=self._violation_count)

        latencies = sorted([m.first_token_latency_ms for m in self.metrics])
        count = len(latencies)

        p50 = self._percentile(latencies, 50)
        p95 = self._percentile(latencies, 95)
        p99 = self._percentile(latencies, 99)

        # Find last violation timestamp
        last_violation_timestamp = None
        for metric in reversed(self.metrics):
            if metric.first_token_latency_ms > self.sla_threshold_ms:
                last_violation_timestamp = metric.timestamp
                break

        return SLAStats(
            p50=round(p50, 2),
            p95=round(p95, 2),
            p99=round(p99, None),
            count=count,
            violations=self._violation_count,
            last_violation_timestamp=last_violation_timestamp
        )

    def xǁSLAMonitorǁget_stats__mutmut_66(self) -> SLAStats:
        """
        Calculate current SLA statistics

        Returns:
            SLAStats with percentiles and violation count
        """
        if not self.metrics:
            return SLAStats(p50=0, p95=0, p99=0, count=0, violations=self._violation_count)

        latencies = sorted([m.first_token_latency_ms for m in self.metrics])
        count = len(latencies)

        p50 = self._percentile(latencies, 50)
        p95 = self._percentile(latencies, 95)
        p99 = self._percentile(latencies, 99)

        # Find last violation timestamp
        last_violation_timestamp = None
        for metric in reversed(self.metrics):
            if metric.first_token_latency_ms > self.sla_threshold_ms:
                last_violation_timestamp = metric.timestamp
                break

        return SLAStats(
            p50=round(p50, 2),
            p95=round(p95, 2),
            p99=round(2),
            count=count,
            violations=self._violation_count,
            last_violation_timestamp=last_violation_timestamp
        )

    def xǁSLAMonitorǁget_stats__mutmut_67(self) -> SLAStats:
        """
        Calculate current SLA statistics

        Returns:
            SLAStats with percentiles and violation count
        """
        if not self.metrics:
            return SLAStats(p50=0, p95=0, p99=0, count=0, violations=self._violation_count)

        latencies = sorted([m.first_token_latency_ms for m in self.metrics])
        count = len(latencies)

        p50 = self._percentile(latencies, 50)
        p95 = self._percentile(latencies, 95)
        p99 = self._percentile(latencies, 99)

        # Find last violation timestamp
        last_violation_timestamp = None
        for metric in reversed(self.metrics):
            if metric.first_token_latency_ms > self.sla_threshold_ms:
                last_violation_timestamp = metric.timestamp
                break

        return SLAStats(
            p50=round(p50, 2),
            p95=round(p95, 2),
            p99=round(p99, ),
            count=count,
            violations=self._violation_count,
            last_violation_timestamp=last_violation_timestamp
        )

    def xǁSLAMonitorǁget_stats__mutmut_68(self) -> SLAStats:
        """
        Calculate current SLA statistics

        Returns:
            SLAStats with percentiles and violation count
        """
        if not self.metrics:
            return SLAStats(p50=0, p95=0, p99=0, count=0, violations=self._violation_count)

        latencies = sorted([m.first_token_latency_ms for m in self.metrics])
        count = len(latencies)

        p50 = self._percentile(latencies, 50)
        p95 = self._percentile(latencies, 95)
        p99 = self._percentile(latencies, 99)

        # Find last violation timestamp
        last_violation_timestamp = None
        for metric in reversed(self.metrics):
            if metric.first_token_latency_ms > self.sla_threshold_ms:
                last_violation_timestamp = metric.timestamp
                break

        return SLAStats(
            p50=round(p50, 2),
            p95=round(p95, 2),
            p99=round(p99, 3),
            count=count,
            violations=self._violation_count,
            last_violation_timestamp=last_violation_timestamp
        )
    
    xǁSLAMonitorǁget_stats__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁSLAMonitorǁget_stats__mutmut_1': xǁSLAMonitorǁget_stats__mutmut_1, 
        'xǁSLAMonitorǁget_stats__mutmut_2': xǁSLAMonitorǁget_stats__mutmut_2, 
        'xǁSLAMonitorǁget_stats__mutmut_3': xǁSLAMonitorǁget_stats__mutmut_3, 
        'xǁSLAMonitorǁget_stats__mutmut_4': xǁSLAMonitorǁget_stats__mutmut_4, 
        'xǁSLAMonitorǁget_stats__mutmut_5': xǁSLAMonitorǁget_stats__mutmut_5, 
        'xǁSLAMonitorǁget_stats__mutmut_6': xǁSLAMonitorǁget_stats__mutmut_6, 
        'xǁSLAMonitorǁget_stats__mutmut_7': xǁSLAMonitorǁget_stats__mutmut_7, 
        'xǁSLAMonitorǁget_stats__mutmut_8': xǁSLAMonitorǁget_stats__mutmut_8, 
        'xǁSLAMonitorǁget_stats__mutmut_9': xǁSLAMonitorǁget_stats__mutmut_9, 
        'xǁSLAMonitorǁget_stats__mutmut_10': xǁSLAMonitorǁget_stats__mutmut_10, 
        'xǁSLAMonitorǁget_stats__mutmut_11': xǁSLAMonitorǁget_stats__mutmut_11, 
        'xǁSLAMonitorǁget_stats__mutmut_12': xǁSLAMonitorǁget_stats__mutmut_12, 
        'xǁSLAMonitorǁget_stats__mutmut_13': xǁSLAMonitorǁget_stats__mutmut_13, 
        'xǁSLAMonitorǁget_stats__mutmut_14': xǁSLAMonitorǁget_stats__mutmut_14, 
        'xǁSLAMonitorǁget_stats__mutmut_15': xǁSLAMonitorǁget_stats__mutmut_15, 
        'xǁSLAMonitorǁget_stats__mutmut_16': xǁSLAMonitorǁget_stats__mutmut_16, 
        'xǁSLAMonitorǁget_stats__mutmut_17': xǁSLAMonitorǁget_stats__mutmut_17, 
        'xǁSLAMonitorǁget_stats__mutmut_18': xǁSLAMonitorǁget_stats__mutmut_18, 
        'xǁSLAMonitorǁget_stats__mutmut_19': xǁSLAMonitorǁget_stats__mutmut_19, 
        'xǁSLAMonitorǁget_stats__mutmut_20': xǁSLAMonitorǁget_stats__mutmut_20, 
        'xǁSLAMonitorǁget_stats__mutmut_21': xǁSLAMonitorǁget_stats__mutmut_21, 
        'xǁSLAMonitorǁget_stats__mutmut_22': xǁSLAMonitorǁget_stats__mutmut_22, 
        'xǁSLAMonitorǁget_stats__mutmut_23': xǁSLAMonitorǁget_stats__mutmut_23, 
        'xǁSLAMonitorǁget_stats__mutmut_24': xǁSLAMonitorǁget_stats__mutmut_24, 
        'xǁSLAMonitorǁget_stats__mutmut_25': xǁSLAMonitorǁget_stats__mutmut_25, 
        'xǁSLAMonitorǁget_stats__mutmut_26': xǁSLAMonitorǁget_stats__mutmut_26, 
        'xǁSLAMonitorǁget_stats__mutmut_27': xǁSLAMonitorǁget_stats__mutmut_27, 
        'xǁSLAMonitorǁget_stats__mutmut_28': xǁSLAMonitorǁget_stats__mutmut_28, 
        'xǁSLAMonitorǁget_stats__mutmut_29': xǁSLAMonitorǁget_stats__mutmut_29, 
        'xǁSLAMonitorǁget_stats__mutmut_30': xǁSLAMonitorǁget_stats__mutmut_30, 
        'xǁSLAMonitorǁget_stats__mutmut_31': xǁSLAMonitorǁget_stats__mutmut_31, 
        'xǁSLAMonitorǁget_stats__mutmut_32': xǁSLAMonitorǁget_stats__mutmut_32, 
        'xǁSLAMonitorǁget_stats__mutmut_33': xǁSLAMonitorǁget_stats__mutmut_33, 
        'xǁSLAMonitorǁget_stats__mutmut_34': xǁSLAMonitorǁget_stats__mutmut_34, 
        'xǁSLAMonitorǁget_stats__mutmut_35': xǁSLAMonitorǁget_stats__mutmut_35, 
        'xǁSLAMonitorǁget_stats__mutmut_36': xǁSLAMonitorǁget_stats__mutmut_36, 
        'xǁSLAMonitorǁget_stats__mutmut_37': xǁSLAMonitorǁget_stats__mutmut_37, 
        'xǁSLAMonitorǁget_stats__mutmut_38': xǁSLAMonitorǁget_stats__mutmut_38, 
        'xǁSLAMonitorǁget_stats__mutmut_39': xǁSLAMonitorǁget_stats__mutmut_39, 
        'xǁSLAMonitorǁget_stats__mutmut_40': xǁSLAMonitorǁget_stats__mutmut_40, 
        'xǁSLAMonitorǁget_stats__mutmut_41': xǁSLAMonitorǁget_stats__mutmut_41, 
        'xǁSLAMonitorǁget_stats__mutmut_42': xǁSLAMonitorǁget_stats__mutmut_42, 
        'xǁSLAMonitorǁget_stats__mutmut_43': xǁSLAMonitorǁget_stats__mutmut_43, 
        'xǁSLAMonitorǁget_stats__mutmut_44': xǁSLAMonitorǁget_stats__mutmut_44, 
        'xǁSLAMonitorǁget_stats__mutmut_45': xǁSLAMonitorǁget_stats__mutmut_45, 
        'xǁSLAMonitorǁget_stats__mutmut_46': xǁSLAMonitorǁget_stats__mutmut_46, 
        'xǁSLAMonitorǁget_stats__mutmut_47': xǁSLAMonitorǁget_stats__mutmut_47, 
        'xǁSLAMonitorǁget_stats__mutmut_48': xǁSLAMonitorǁget_stats__mutmut_48, 
        'xǁSLAMonitorǁget_stats__mutmut_49': xǁSLAMonitorǁget_stats__mutmut_49, 
        'xǁSLAMonitorǁget_stats__mutmut_50': xǁSLAMonitorǁget_stats__mutmut_50, 
        'xǁSLAMonitorǁget_stats__mutmut_51': xǁSLAMonitorǁget_stats__mutmut_51, 
        'xǁSLAMonitorǁget_stats__mutmut_52': xǁSLAMonitorǁget_stats__mutmut_52, 
        'xǁSLAMonitorǁget_stats__mutmut_53': xǁSLAMonitorǁget_stats__mutmut_53, 
        'xǁSLAMonitorǁget_stats__mutmut_54': xǁSLAMonitorǁget_stats__mutmut_54, 
        'xǁSLAMonitorǁget_stats__mutmut_55': xǁSLAMonitorǁget_stats__mutmut_55, 
        'xǁSLAMonitorǁget_stats__mutmut_56': xǁSLAMonitorǁget_stats__mutmut_56, 
        'xǁSLAMonitorǁget_stats__mutmut_57': xǁSLAMonitorǁget_stats__mutmut_57, 
        'xǁSLAMonitorǁget_stats__mutmut_58': xǁSLAMonitorǁget_stats__mutmut_58, 
        'xǁSLAMonitorǁget_stats__mutmut_59': xǁSLAMonitorǁget_stats__mutmut_59, 
        'xǁSLAMonitorǁget_stats__mutmut_60': xǁSLAMonitorǁget_stats__mutmut_60, 
        'xǁSLAMonitorǁget_stats__mutmut_61': xǁSLAMonitorǁget_stats__mutmut_61, 
        'xǁSLAMonitorǁget_stats__mutmut_62': xǁSLAMonitorǁget_stats__mutmut_62, 
        'xǁSLAMonitorǁget_stats__mutmut_63': xǁSLAMonitorǁget_stats__mutmut_63, 
        'xǁSLAMonitorǁget_stats__mutmut_64': xǁSLAMonitorǁget_stats__mutmut_64, 
        'xǁSLAMonitorǁget_stats__mutmut_65': xǁSLAMonitorǁget_stats__mutmut_65, 
        'xǁSLAMonitorǁget_stats__mutmut_66': xǁSLAMonitorǁget_stats__mutmut_66, 
        'xǁSLAMonitorǁget_stats__mutmut_67': xǁSLAMonitorǁget_stats__mutmut_67, 
        'xǁSLAMonitorǁget_stats__mutmut_68': xǁSLAMonitorǁget_stats__mutmut_68
    }
    
    def get_stats(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁSLAMonitorǁget_stats__mutmut_orig"), object.__getattribute__(self, "xǁSLAMonitorǁget_stats__mutmut_mutants"), args, kwargs, self)
        return result 
    
    get_stats.__signature__ = _mutmut_signature(xǁSLAMonitorǁget_stats__mutmut_orig)
    xǁSLAMonitorǁget_stats__mutmut_orig.__name__ = 'xǁSLAMonitorǁget_stats'

    def xǁSLAMonitorǁ_percentile__mutmut_orig(self, sorted_values: List[float], percentile: int) -> float:
        """
        Calculate percentile from sorted values

        Uses linear interpolation between closest ranks.

        Args:
            sorted_values: Sorted list of values
            percentile: Percentile to calculate (0-100)

        Returns:
            Percentile value
        """
        if not sorted_values:
            return 0.0

        if len(sorted_values) == 1:
            return sorted_values[0]

        # Calculate rank (using "nearest rank" method)
        rank = (percentile / 100) * (len(sorted_values) - 1)
        lower_index = int(rank)
        upper_index = min(lower_index + 1, len(sorted_values) - 1)

        # Linear interpolation
        weight = rank - lower_index
        return sorted_values[lower_index] * (1 - weight) + sorted_values[upper_index] * weight

    def xǁSLAMonitorǁ_percentile__mutmut_1(self, sorted_values: List[float], percentile: int) -> float:
        """
        Calculate percentile from sorted values

        Uses linear interpolation between closest ranks.

        Args:
            sorted_values: Sorted list of values
            percentile: Percentile to calculate (0-100)

        Returns:
            Percentile value
        """
        if sorted_values:
            return 0.0

        if len(sorted_values) == 1:
            return sorted_values[0]

        # Calculate rank (using "nearest rank" method)
        rank = (percentile / 100) * (len(sorted_values) - 1)
        lower_index = int(rank)
        upper_index = min(lower_index + 1, len(sorted_values) - 1)

        # Linear interpolation
        weight = rank - lower_index
        return sorted_values[lower_index] * (1 - weight) + sorted_values[upper_index] * weight

    def xǁSLAMonitorǁ_percentile__mutmut_2(self, sorted_values: List[float], percentile: int) -> float:
        """
        Calculate percentile from sorted values

        Uses linear interpolation between closest ranks.

        Args:
            sorted_values: Sorted list of values
            percentile: Percentile to calculate (0-100)

        Returns:
            Percentile value
        """
        if not sorted_values:
            return 1.0

        if len(sorted_values) == 1:
            return sorted_values[0]

        # Calculate rank (using "nearest rank" method)
        rank = (percentile / 100) * (len(sorted_values) - 1)
        lower_index = int(rank)
        upper_index = min(lower_index + 1, len(sorted_values) - 1)

        # Linear interpolation
        weight = rank - lower_index
        return sorted_values[lower_index] * (1 - weight) + sorted_values[upper_index] * weight

    def xǁSLAMonitorǁ_percentile__mutmut_3(self, sorted_values: List[float], percentile: int) -> float:
        """
        Calculate percentile from sorted values

        Uses linear interpolation between closest ranks.

        Args:
            sorted_values: Sorted list of values
            percentile: Percentile to calculate (0-100)

        Returns:
            Percentile value
        """
        if not sorted_values:
            return 0.0

        if len(sorted_values) != 1:
            return sorted_values[0]

        # Calculate rank (using "nearest rank" method)
        rank = (percentile / 100) * (len(sorted_values) - 1)
        lower_index = int(rank)
        upper_index = min(lower_index + 1, len(sorted_values) - 1)

        # Linear interpolation
        weight = rank - lower_index
        return sorted_values[lower_index] * (1 - weight) + sorted_values[upper_index] * weight

    def xǁSLAMonitorǁ_percentile__mutmut_4(self, sorted_values: List[float], percentile: int) -> float:
        """
        Calculate percentile from sorted values

        Uses linear interpolation between closest ranks.

        Args:
            sorted_values: Sorted list of values
            percentile: Percentile to calculate (0-100)

        Returns:
            Percentile value
        """
        if not sorted_values:
            return 0.0

        if len(sorted_values) == 2:
            return sorted_values[0]

        # Calculate rank (using "nearest rank" method)
        rank = (percentile / 100) * (len(sorted_values) - 1)
        lower_index = int(rank)
        upper_index = min(lower_index + 1, len(sorted_values) - 1)

        # Linear interpolation
        weight = rank - lower_index
        return sorted_values[lower_index] * (1 - weight) + sorted_values[upper_index] * weight

    def xǁSLAMonitorǁ_percentile__mutmut_5(self, sorted_values: List[float], percentile: int) -> float:
        """
        Calculate percentile from sorted values

        Uses linear interpolation between closest ranks.

        Args:
            sorted_values: Sorted list of values
            percentile: Percentile to calculate (0-100)

        Returns:
            Percentile value
        """
        if not sorted_values:
            return 0.0

        if len(sorted_values) == 1:
            return sorted_values[1]

        # Calculate rank (using "nearest rank" method)
        rank = (percentile / 100) * (len(sorted_values) - 1)
        lower_index = int(rank)
        upper_index = min(lower_index + 1, len(sorted_values) - 1)

        # Linear interpolation
        weight = rank - lower_index
        return sorted_values[lower_index] * (1 - weight) + sorted_values[upper_index] * weight

    def xǁSLAMonitorǁ_percentile__mutmut_6(self, sorted_values: List[float], percentile: int) -> float:
        """
        Calculate percentile from sorted values

        Uses linear interpolation between closest ranks.

        Args:
            sorted_values: Sorted list of values
            percentile: Percentile to calculate (0-100)

        Returns:
            Percentile value
        """
        if not sorted_values:
            return 0.0

        if len(sorted_values) == 1:
            return sorted_values[0]

        # Calculate rank (using "nearest rank" method)
        rank = None
        lower_index = int(rank)
        upper_index = min(lower_index + 1, len(sorted_values) - 1)

        # Linear interpolation
        weight = rank - lower_index
        return sorted_values[lower_index] * (1 - weight) + sorted_values[upper_index] * weight

    def xǁSLAMonitorǁ_percentile__mutmut_7(self, sorted_values: List[float], percentile: int) -> float:
        """
        Calculate percentile from sorted values

        Uses linear interpolation between closest ranks.

        Args:
            sorted_values: Sorted list of values
            percentile: Percentile to calculate (0-100)

        Returns:
            Percentile value
        """
        if not sorted_values:
            return 0.0

        if len(sorted_values) == 1:
            return sorted_values[0]

        # Calculate rank (using "nearest rank" method)
        rank = (percentile / 100) / (len(sorted_values) - 1)
        lower_index = int(rank)
        upper_index = min(lower_index + 1, len(sorted_values) - 1)

        # Linear interpolation
        weight = rank - lower_index
        return sorted_values[lower_index] * (1 - weight) + sorted_values[upper_index] * weight

    def xǁSLAMonitorǁ_percentile__mutmut_8(self, sorted_values: List[float], percentile: int) -> float:
        """
        Calculate percentile from sorted values

        Uses linear interpolation between closest ranks.

        Args:
            sorted_values: Sorted list of values
            percentile: Percentile to calculate (0-100)

        Returns:
            Percentile value
        """
        if not sorted_values:
            return 0.0

        if len(sorted_values) == 1:
            return sorted_values[0]

        # Calculate rank (using "nearest rank" method)
        rank = (percentile * 100) * (len(sorted_values) - 1)
        lower_index = int(rank)
        upper_index = min(lower_index + 1, len(sorted_values) - 1)

        # Linear interpolation
        weight = rank - lower_index
        return sorted_values[lower_index] * (1 - weight) + sorted_values[upper_index] * weight

    def xǁSLAMonitorǁ_percentile__mutmut_9(self, sorted_values: List[float], percentile: int) -> float:
        """
        Calculate percentile from sorted values

        Uses linear interpolation between closest ranks.

        Args:
            sorted_values: Sorted list of values
            percentile: Percentile to calculate (0-100)

        Returns:
            Percentile value
        """
        if not sorted_values:
            return 0.0

        if len(sorted_values) == 1:
            return sorted_values[0]

        # Calculate rank (using "nearest rank" method)
        rank = (percentile / 101) * (len(sorted_values) - 1)
        lower_index = int(rank)
        upper_index = min(lower_index + 1, len(sorted_values) - 1)

        # Linear interpolation
        weight = rank - lower_index
        return sorted_values[lower_index] * (1 - weight) + sorted_values[upper_index] * weight

    def xǁSLAMonitorǁ_percentile__mutmut_10(self, sorted_values: List[float], percentile: int) -> float:
        """
        Calculate percentile from sorted values

        Uses linear interpolation between closest ranks.

        Args:
            sorted_values: Sorted list of values
            percentile: Percentile to calculate (0-100)

        Returns:
            Percentile value
        """
        if not sorted_values:
            return 0.0

        if len(sorted_values) == 1:
            return sorted_values[0]

        # Calculate rank (using "nearest rank" method)
        rank = (percentile / 100) * (len(sorted_values) + 1)
        lower_index = int(rank)
        upper_index = min(lower_index + 1, len(sorted_values) - 1)

        # Linear interpolation
        weight = rank - lower_index
        return sorted_values[lower_index] * (1 - weight) + sorted_values[upper_index] * weight

    def xǁSLAMonitorǁ_percentile__mutmut_11(self, sorted_values: List[float], percentile: int) -> float:
        """
        Calculate percentile from sorted values

        Uses linear interpolation between closest ranks.

        Args:
            sorted_values: Sorted list of values
            percentile: Percentile to calculate (0-100)

        Returns:
            Percentile value
        """
        if not sorted_values:
            return 0.0

        if len(sorted_values) == 1:
            return sorted_values[0]

        # Calculate rank (using "nearest rank" method)
        rank = (percentile / 100) * (len(sorted_values) - 2)
        lower_index = int(rank)
        upper_index = min(lower_index + 1, len(sorted_values) - 1)

        # Linear interpolation
        weight = rank - lower_index
        return sorted_values[lower_index] * (1 - weight) + sorted_values[upper_index] * weight

    def xǁSLAMonitorǁ_percentile__mutmut_12(self, sorted_values: List[float], percentile: int) -> float:
        """
        Calculate percentile from sorted values

        Uses linear interpolation between closest ranks.

        Args:
            sorted_values: Sorted list of values
            percentile: Percentile to calculate (0-100)

        Returns:
            Percentile value
        """
        if not sorted_values:
            return 0.0

        if len(sorted_values) == 1:
            return sorted_values[0]

        # Calculate rank (using "nearest rank" method)
        rank = (percentile / 100) * (len(sorted_values) - 1)
        lower_index = None
        upper_index = min(lower_index + 1, len(sorted_values) - 1)

        # Linear interpolation
        weight = rank - lower_index
        return sorted_values[lower_index] * (1 - weight) + sorted_values[upper_index] * weight

    def xǁSLAMonitorǁ_percentile__mutmut_13(self, sorted_values: List[float], percentile: int) -> float:
        """
        Calculate percentile from sorted values

        Uses linear interpolation between closest ranks.

        Args:
            sorted_values: Sorted list of values
            percentile: Percentile to calculate (0-100)

        Returns:
            Percentile value
        """
        if not sorted_values:
            return 0.0

        if len(sorted_values) == 1:
            return sorted_values[0]

        # Calculate rank (using "nearest rank" method)
        rank = (percentile / 100) * (len(sorted_values) - 1)
        lower_index = int(None)
        upper_index = min(lower_index + 1, len(sorted_values) - 1)

        # Linear interpolation
        weight = rank - lower_index
        return sorted_values[lower_index] * (1 - weight) + sorted_values[upper_index] * weight

    def xǁSLAMonitorǁ_percentile__mutmut_14(self, sorted_values: List[float], percentile: int) -> float:
        """
        Calculate percentile from sorted values

        Uses linear interpolation between closest ranks.

        Args:
            sorted_values: Sorted list of values
            percentile: Percentile to calculate (0-100)

        Returns:
            Percentile value
        """
        if not sorted_values:
            return 0.0

        if len(sorted_values) == 1:
            return sorted_values[0]

        # Calculate rank (using "nearest rank" method)
        rank = (percentile / 100) * (len(sorted_values) - 1)
        lower_index = int(rank)
        upper_index = None

        # Linear interpolation
        weight = rank - lower_index
        return sorted_values[lower_index] * (1 - weight) + sorted_values[upper_index] * weight

    def xǁSLAMonitorǁ_percentile__mutmut_15(self, sorted_values: List[float], percentile: int) -> float:
        """
        Calculate percentile from sorted values

        Uses linear interpolation between closest ranks.

        Args:
            sorted_values: Sorted list of values
            percentile: Percentile to calculate (0-100)

        Returns:
            Percentile value
        """
        if not sorted_values:
            return 0.0

        if len(sorted_values) == 1:
            return sorted_values[0]

        # Calculate rank (using "nearest rank" method)
        rank = (percentile / 100) * (len(sorted_values) - 1)
        lower_index = int(rank)
        upper_index = min(None, len(sorted_values) - 1)

        # Linear interpolation
        weight = rank - lower_index
        return sorted_values[lower_index] * (1 - weight) + sorted_values[upper_index] * weight

    def xǁSLAMonitorǁ_percentile__mutmut_16(self, sorted_values: List[float], percentile: int) -> float:
        """
        Calculate percentile from sorted values

        Uses linear interpolation between closest ranks.

        Args:
            sorted_values: Sorted list of values
            percentile: Percentile to calculate (0-100)

        Returns:
            Percentile value
        """
        if not sorted_values:
            return 0.0

        if len(sorted_values) == 1:
            return sorted_values[0]

        # Calculate rank (using "nearest rank" method)
        rank = (percentile / 100) * (len(sorted_values) - 1)
        lower_index = int(rank)
        upper_index = min(lower_index + 1, None)

        # Linear interpolation
        weight = rank - lower_index
        return sorted_values[lower_index] * (1 - weight) + sorted_values[upper_index] * weight

    def xǁSLAMonitorǁ_percentile__mutmut_17(self, sorted_values: List[float], percentile: int) -> float:
        """
        Calculate percentile from sorted values

        Uses linear interpolation between closest ranks.

        Args:
            sorted_values: Sorted list of values
            percentile: Percentile to calculate (0-100)

        Returns:
            Percentile value
        """
        if not sorted_values:
            return 0.0

        if len(sorted_values) == 1:
            return sorted_values[0]

        # Calculate rank (using "nearest rank" method)
        rank = (percentile / 100) * (len(sorted_values) - 1)
        lower_index = int(rank)
        upper_index = min(len(sorted_values) - 1)

        # Linear interpolation
        weight = rank - lower_index
        return sorted_values[lower_index] * (1 - weight) + sorted_values[upper_index] * weight

    def xǁSLAMonitorǁ_percentile__mutmut_18(self, sorted_values: List[float], percentile: int) -> float:
        """
        Calculate percentile from sorted values

        Uses linear interpolation between closest ranks.

        Args:
            sorted_values: Sorted list of values
            percentile: Percentile to calculate (0-100)

        Returns:
            Percentile value
        """
        if not sorted_values:
            return 0.0

        if len(sorted_values) == 1:
            return sorted_values[0]

        # Calculate rank (using "nearest rank" method)
        rank = (percentile / 100) * (len(sorted_values) - 1)
        lower_index = int(rank)
        upper_index = min(lower_index + 1, )

        # Linear interpolation
        weight = rank - lower_index
        return sorted_values[lower_index] * (1 - weight) + sorted_values[upper_index] * weight

    def xǁSLAMonitorǁ_percentile__mutmut_19(self, sorted_values: List[float], percentile: int) -> float:
        """
        Calculate percentile from sorted values

        Uses linear interpolation between closest ranks.

        Args:
            sorted_values: Sorted list of values
            percentile: Percentile to calculate (0-100)

        Returns:
            Percentile value
        """
        if not sorted_values:
            return 0.0

        if len(sorted_values) == 1:
            return sorted_values[0]

        # Calculate rank (using "nearest rank" method)
        rank = (percentile / 100) * (len(sorted_values) - 1)
        lower_index = int(rank)
        upper_index = min(lower_index - 1, len(sorted_values) - 1)

        # Linear interpolation
        weight = rank - lower_index
        return sorted_values[lower_index] * (1 - weight) + sorted_values[upper_index] * weight

    def xǁSLAMonitorǁ_percentile__mutmut_20(self, sorted_values: List[float], percentile: int) -> float:
        """
        Calculate percentile from sorted values

        Uses linear interpolation between closest ranks.

        Args:
            sorted_values: Sorted list of values
            percentile: Percentile to calculate (0-100)

        Returns:
            Percentile value
        """
        if not sorted_values:
            return 0.0

        if len(sorted_values) == 1:
            return sorted_values[0]

        # Calculate rank (using "nearest rank" method)
        rank = (percentile / 100) * (len(sorted_values) - 1)
        lower_index = int(rank)
        upper_index = min(lower_index + 2, len(sorted_values) - 1)

        # Linear interpolation
        weight = rank - lower_index
        return sorted_values[lower_index] * (1 - weight) + sorted_values[upper_index] * weight

    def xǁSLAMonitorǁ_percentile__mutmut_21(self, sorted_values: List[float], percentile: int) -> float:
        """
        Calculate percentile from sorted values

        Uses linear interpolation between closest ranks.

        Args:
            sorted_values: Sorted list of values
            percentile: Percentile to calculate (0-100)

        Returns:
            Percentile value
        """
        if not sorted_values:
            return 0.0

        if len(sorted_values) == 1:
            return sorted_values[0]

        # Calculate rank (using "nearest rank" method)
        rank = (percentile / 100) * (len(sorted_values) - 1)
        lower_index = int(rank)
        upper_index = min(lower_index + 1, len(sorted_values) + 1)

        # Linear interpolation
        weight = rank - lower_index
        return sorted_values[lower_index] * (1 - weight) + sorted_values[upper_index] * weight

    def xǁSLAMonitorǁ_percentile__mutmut_22(self, sorted_values: List[float], percentile: int) -> float:
        """
        Calculate percentile from sorted values

        Uses linear interpolation between closest ranks.

        Args:
            sorted_values: Sorted list of values
            percentile: Percentile to calculate (0-100)

        Returns:
            Percentile value
        """
        if not sorted_values:
            return 0.0

        if len(sorted_values) == 1:
            return sorted_values[0]

        # Calculate rank (using "nearest rank" method)
        rank = (percentile / 100) * (len(sorted_values) - 1)
        lower_index = int(rank)
        upper_index = min(lower_index + 1, len(sorted_values) - 2)

        # Linear interpolation
        weight = rank - lower_index
        return sorted_values[lower_index] * (1 - weight) + sorted_values[upper_index] * weight

    def xǁSLAMonitorǁ_percentile__mutmut_23(self, sorted_values: List[float], percentile: int) -> float:
        """
        Calculate percentile from sorted values

        Uses linear interpolation between closest ranks.

        Args:
            sorted_values: Sorted list of values
            percentile: Percentile to calculate (0-100)

        Returns:
            Percentile value
        """
        if not sorted_values:
            return 0.0

        if len(sorted_values) == 1:
            return sorted_values[0]

        # Calculate rank (using "nearest rank" method)
        rank = (percentile / 100) * (len(sorted_values) - 1)
        lower_index = int(rank)
        upper_index = min(lower_index + 1, len(sorted_values) - 1)

        # Linear interpolation
        weight = None
        return sorted_values[lower_index] * (1 - weight) + sorted_values[upper_index] * weight

    def xǁSLAMonitorǁ_percentile__mutmut_24(self, sorted_values: List[float], percentile: int) -> float:
        """
        Calculate percentile from sorted values

        Uses linear interpolation between closest ranks.

        Args:
            sorted_values: Sorted list of values
            percentile: Percentile to calculate (0-100)

        Returns:
            Percentile value
        """
        if not sorted_values:
            return 0.0

        if len(sorted_values) == 1:
            return sorted_values[0]

        # Calculate rank (using "nearest rank" method)
        rank = (percentile / 100) * (len(sorted_values) - 1)
        lower_index = int(rank)
        upper_index = min(lower_index + 1, len(sorted_values) - 1)

        # Linear interpolation
        weight = rank + lower_index
        return sorted_values[lower_index] * (1 - weight) + sorted_values[upper_index] * weight

    def xǁSLAMonitorǁ_percentile__mutmut_25(self, sorted_values: List[float], percentile: int) -> float:
        """
        Calculate percentile from sorted values

        Uses linear interpolation between closest ranks.

        Args:
            sorted_values: Sorted list of values
            percentile: Percentile to calculate (0-100)

        Returns:
            Percentile value
        """
        if not sorted_values:
            return 0.0

        if len(sorted_values) == 1:
            return sorted_values[0]

        # Calculate rank (using "nearest rank" method)
        rank = (percentile / 100) * (len(sorted_values) - 1)
        lower_index = int(rank)
        upper_index = min(lower_index + 1, len(sorted_values) - 1)

        # Linear interpolation
        weight = rank - lower_index
        return sorted_values[lower_index] * (1 - weight) - sorted_values[upper_index] * weight

    def xǁSLAMonitorǁ_percentile__mutmut_26(self, sorted_values: List[float], percentile: int) -> float:
        """
        Calculate percentile from sorted values

        Uses linear interpolation between closest ranks.

        Args:
            sorted_values: Sorted list of values
            percentile: Percentile to calculate (0-100)

        Returns:
            Percentile value
        """
        if not sorted_values:
            return 0.0

        if len(sorted_values) == 1:
            return sorted_values[0]

        # Calculate rank (using "nearest rank" method)
        rank = (percentile / 100) * (len(sorted_values) - 1)
        lower_index = int(rank)
        upper_index = min(lower_index + 1, len(sorted_values) - 1)

        # Linear interpolation
        weight = rank - lower_index
        return sorted_values[lower_index] / (1 - weight) + sorted_values[upper_index] * weight

    def xǁSLAMonitorǁ_percentile__mutmut_27(self, sorted_values: List[float], percentile: int) -> float:
        """
        Calculate percentile from sorted values

        Uses linear interpolation between closest ranks.

        Args:
            sorted_values: Sorted list of values
            percentile: Percentile to calculate (0-100)

        Returns:
            Percentile value
        """
        if not sorted_values:
            return 0.0

        if len(sorted_values) == 1:
            return sorted_values[0]

        # Calculate rank (using "nearest rank" method)
        rank = (percentile / 100) * (len(sorted_values) - 1)
        lower_index = int(rank)
        upper_index = min(lower_index + 1, len(sorted_values) - 1)

        # Linear interpolation
        weight = rank - lower_index
        return sorted_values[lower_index] * (1 + weight) + sorted_values[upper_index] * weight

    def xǁSLAMonitorǁ_percentile__mutmut_28(self, sorted_values: List[float], percentile: int) -> float:
        """
        Calculate percentile from sorted values

        Uses linear interpolation between closest ranks.

        Args:
            sorted_values: Sorted list of values
            percentile: Percentile to calculate (0-100)

        Returns:
            Percentile value
        """
        if not sorted_values:
            return 0.0

        if len(sorted_values) == 1:
            return sorted_values[0]

        # Calculate rank (using "nearest rank" method)
        rank = (percentile / 100) * (len(sorted_values) - 1)
        lower_index = int(rank)
        upper_index = min(lower_index + 1, len(sorted_values) - 1)

        # Linear interpolation
        weight = rank - lower_index
        return sorted_values[lower_index] * (2 - weight) + sorted_values[upper_index] * weight

    def xǁSLAMonitorǁ_percentile__mutmut_29(self, sorted_values: List[float], percentile: int) -> float:
        """
        Calculate percentile from sorted values

        Uses linear interpolation between closest ranks.

        Args:
            sorted_values: Sorted list of values
            percentile: Percentile to calculate (0-100)

        Returns:
            Percentile value
        """
        if not sorted_values:
            return 0.0

        if len(sorted_values) == 1:
            return sorted_values[0]

        # Calculate rank (using "nearest rank" method)
        rank = (percentile / 100) * (len(sorted_values) - 1)
        lower_index = int(rank)
        upper_index = min(lower_index + 1, len(sorted_values) - 1)

        # Linear interpolation
        weight = rank - lower_index
        return sorted_values[lower_index] * (1 - weight) + sorted_values[upper_index] / weight
    
    xǁSLAMonitorǁ_percentile__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁSLAMonitorǁ_percentile__mutmut_1': xǁSLAMonitorǁ_percentile__mutmut_1, 
        'xǁSLAMonitorǁ_percentile__mutmut_2': xǁSLAMonitorǁ_percentile__mutmut_2, 
        'xǁSLAMonitorǁ_percentile__mutmut_3': xǁSLAMonitorǁ_percentile__mutmut_3, 
        'xǁSLAMonitorǁ_percentile__mutmut_4': xǁSLAMonitorǁ_percentile__mutmut_4, 
        'xǁSLAMonitorǁ_percentile__mutmut_5': xǁSLAMonitorǁ_percentile__mutmut_5, 
        'xǁSLAMonitorǁ_percentile__mutmut_6': xǁSLAMonitorǁ_percentile__mutmut_6, 
        'xǁSLAMonitorǁ_percentile__mutmut_7': xǁSLAMonitorǁ_percentile__mutmut_7, 
        'xǁSLAMonitorǁ_percentile__mutmut_8': xǁSLAMonitorǁ_percentile__mutmut_8, 
        'xǁSLAMonitorǁ_percentile__mutmut_9': xǁSLAMonitorǁ_percentile__mutmut_9, 
        'xǁSLAMonitorǁ_percentile__mutmut_10': xǁSLAMonitorǁ_percentile__mutmut_10, 
        'xǁSLAMonitorǁ_percentile__mutmut_11': xǁSLAMonitorǁ_percentile__mutmut_11, 
        'xǁSLAMonitorǁ_percentile__mutmut_12': xǁSLAMonitorǁ_percentile__mutmut_12, 
        'xǁSLAMonitorǁ_percentile__mutmut_13': xǁSLAMonitorǁ_percentile__mutmut_13, 
        'xǁSLAMonitorǁ_percentile__mutmut_14': xǁSLAMonitorǁ_percentile__mutmut_14, 
        'xǁSLAMonitorǁ_percentile__mutmut_15': xǁSLAMonitorǁ_percentile__mutmut_15, 
        'xǁSLAMonitorǁ_percentile__mutmut_16': xǁSLAMonitorǁ_percentile__mutmut_16, 
        'xǁSLAMonitorǁ_percentile__mutmut_17': xǁSLAMonitorǁ_percentile__mutmut_17, 
        'xǁSLAMonitorǁ_percentile__mutmut_18': xǁSLAMonitorǁ_percentile__mutmut_18, 
        'xǁSLAMonitorǁ_percentile__mutmut_19': xǁSLAMonitorǁ_percentile__mutmut_19, 
        'xǁSLAMonitorǁ_percentile__mutmut_20': xǁSLAMonitorǁ_percentile__mutmut_20, 
        'xǁSLAMonitorǁ_percentile__mutmut_21': xǁSLAMonitorǁ_percentile__mutmut_21, 
        'xǁSLAMonitorǁ_percentile__mutmut_22': xǁSLAMonitorǁ_percentile__mutmut_22, 
        'xǁSLAMonitorǁ_percentile__mutmut_23': xǁSLAMonitorǁ_percentile__mutmut_23, 
        'xǁSLAMonitorǁ_percentile__mutmut_24': xǁSLAMonitorǁ_percentile__mutmut_24, 
        'xǁSLAMonitorǁ_percentile__mutmut_25': xǁSLAMonitorǁ_percentile__mutmut_25, 
        'xǁSLAMonitorǁ_percentile__mutmut_26': xǁSLAMonitorǁ_percentile__mutmut_26, 
        'xǁSLAMonitorǁ_percentile__mutmut_27': xǁSLAMonitorǁ_percentile__mutmut_27, 
        'xǁSLAMonitorǁ_percentile__mutmut_28': xǁSLAMonitorǁ_percentile__mutmut_28, 
        'xǁSLAMonitorǁ_percentile__mutmut_29': xǁSLAMonitorǁ_percentile__mutmut_29
    }
    
    def _percentile(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁSLAMonitorǁ_percentile__mutmut_orig"), object.__getattribute__(self, "xǁSLAMonitorǁ_percentile__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _percentile.__signature__ = _mutmut_signature(xǁSLAMonitorǁ_percentile__mutmut_orig)
    xǁSLAMonitorǁ_percentile__mutmut_orig.__name__ = 'xǁSLAMonitorǁ_percentile'

    def xǁSLAMonitorǁ_check_sla_violation__mutmut_orig(self) -> None:
        """
        Check if current p95 violates SLA threshold and alert if needed

        Violation: p95 > 5000ms (5 seconds)
        """
        stats = self.get_stats()

        if stats.p95 > self.sla_threshold_ms:
            self._violation_count += 1

            logger.warn(
                "SLA VIOLATION: p95 latency exceeds threshold",
                {
                    "p50_ms": stats.p50,
                    "p95_ms": stats.p95,
                    "p99_ms": stats.p99,
                    "threshold_ms": self.sla_threshold_ms,
                    "sample_count": stats.count,
                    "total_violations": self._violation_count,
                }
            )

    def xǁSLAMonitorǁ_check_sla_violation__mutmut_1(self) -> None:
        """
        Check if current p95 violates SLA threshold and alert if needed

        Violation: p95 > 5000ms (5 seconds)
        """
        stats = None

        if stats.p95 > self.sla_threshold_ms:
            self._violation_count += 1

            logger.warn(
                "SLA VIOLATION: p95 latency exceeds threshold",
                {
                    "p50_ms": stats.p50,
                    "p95_ms": stats.p95,
                    "p99_ms": stats.p99,
                    "threshold_ms": self.sla_threshold_ms,
                    "sample_count": stats.count,
                    "total_violations": self._violation_count,
                }
            )

    def xǁSLAMonitorǁ_check_sla_violation__mutmut_2(self) -> None:
        """
        Check if current p95 violates SLA threshold and alert if needed

        Violation: p95 > 5000ms (5 seconds)
        """
        stats = self.get_stats()

        if stats.p95 >= self.sla_threshold_ms:
            self._violation_count += 1

            logger.warn(
                "SLA VIOLATION: p95 latency exceeds threshold",
                {
                    "p50_ms": stats.p50,
                    "p95_ms": stats.p95,
                    "p99_ms": stats.p99,
                    "threshold_ms": self.sla_threshold_ms,
                    "sample_count": stats.count,
                    "total_violations": self._violation_count,
                }
            )

    def xǁSLAMonitorǁ_check_sla_violation__mutmut_3(self) -> None:
        """
        Check if current p95 violates SLA threshold and alert if needed

        Violation: p95 > 5000ms (5 seconds)
        """
        stats = self.get_stats()

        if stats.p95 > self.sla_threshold_ms:
            self._violation_count = 1

            logger.warn(
                "SLA VIOLATION: p95 latency exceeds threshold",
                {
                    "p50_ms": stats.p50,
                    "p95_ms": stats.p95,
                    "p99_ms": stats.p99,
                    "threshold_ms": self.sla_threshold_ms,
                    "sample_count": stats.count,
                    "total_violations": self._violation_count,
                }
            )

    def xǁSLAMonitorǁ_check_sla_violation__mutmut_4(self) -> None:
        """
        Check if current p95 violates SLA threshold and alert if needed

        Violation: p95 > 5000ms (5 seconds)
        """
        stats = self.get_stats()

        if stats.p95 > self.sla_threshold_ms:
            self._violation_count -= 1

            logger.warn(
                "SLA VIOLATION: p95 latency exceeds threshold",
                {
                    "p50_ms": stats.p50,
                    "p95_ms": stats.p95,
                    "p99_ms": stats.p99,
                    "threshold_ms": self.sla_threshold_ms,
                    "sample_count": stats.count,
                    "total_violations": self._violation_count,
                }
            )

    def xǁSLAMonitorǁ_check_sla_violation__mutmut_5(self) -> None:
        """
        Check if current p95 violates SLA threshold and alert if needed

        Violation: p95 > 5000ms (5 seconds)
        """
        stats = self.get_stats()

        if stats.p95 > self.sla_threshold_ms:
            self._violation_count += 2

            logger.warn(
                "SLA VIOLATION: p95 latency exceeds threshold",
                {
                    "p50_ms": stats.p50,
                    "p95_ms": stats.p95,
                    "p99_ms": stats.p99,
                    "threshold_ms": self.sla_threshold_ms,
                    "sample_count": stats.count,
                    "total_violations": self._violation_count,
                }
            )

    def xǁSLAMonitorǁ_check_sla_violation__mutmut_6(self) -> None:
        """
        Check if current p95 violates SLA threshold and alert if needed

        Violation: p95 > 5000ms (5 seconds)
        """
        stats = self.get_stats()

        if stats.p95 > self.sla_threshold_ms:
            self._violation_count += 1

            logger.warn(
                None,
                {
                    "p50_ms": stats.p50,
                    "p95_ms": stats.p95,
                    "p99_ms": stats.p99,
                    "threshold_ms": self.sla_threshold_ms,
                    "sample_count": stats.count,
                    "total_violations": self._violation_count,
                }
            )

    def xǁSLAMonitorǁ_check_sla_violation__mutmut_7(self) -> None:
        """
        Check if current p95 violates SLA threshold and alert if needed

        Violation: p95 > 5000ms (5 seconds)
        """
        stats = self.get_stats()

        if stats.p95 > self.sla_threshold_ms:
            self._violation_count += 1

            logger.warn(
                "SLA VIOLATION: p95 latency exceeds threshold",
                None
            )

    def xǁSLAMonitorǁ_check_sla_violation__mutmut_8(self) -> None:
        """
        Check if current p95 violates SLA threshold and alert if needed

        Violation: p95 > 5000ms (5 seconds)
        """
        stats = self.get_stats()

        if stats.p95 > self.sla_threshold_ms:
            self._violation_count += 1

            logger.warn(
                {
                    "p50_ms": stats.p50,
                    "p95_ms": stats.p95,
                    "p99_ms": stats.p99,
                    "threshold_ms": self.sla_threshold_ms,
                    "sample_count": stats.count,
                    "total_violations": self._violation_count,
                }
            )

    def xǁSLAMonitorǁ_check_sla_violation__mutmut_9(self) -> None:
        """
        Check if current p95 violates SLA threshold and alert if needed

        Violation: p95 > 5000ms (5 seconds)
        """
        stats = self.get_stats()

        if stats.p95 > self.sla_threshold_ms:
            self._violation_count += 1

            logger.warn(
                "SLA VIOLATION: p95 latency exceeds threshold",
                )

    def xǁSLAMonitorǁ_check_sla_violation__mutmut_10(self) -> None:
        """
        Check if current p95 violates SLA threshold and alert if needed

        Violation: p95 > 5000ms (5 seconds)
        """
        stats = self.get_stats()

        if stats.p95 > self.sla_threshold_ms:
            self._violation_count += 1

            logger.warn(
                "XXSLA VIOLATION: p95 latency exceeds thresholdXX",
                {
                    "p50_ms": stats.p50,
                    "p95_ms": stats.p95,
                    "p99_ms": stats.p99,
                    "threshold_ms": self.sla_threshold_ms,
                    "sample_count": stats.count,
                    "total_violations": self._violation_count,
                }
            )

    def xǁSLAMonitorǁ_check_sla_violation__mutmut_11(self) -> None:
        """
        Check if current p95 violates SLA threshold and alert if needed

        Violation: p95 > 5000ms (5 seconds)
        """
        stats = self.get_stats()

        if stats.p95 > self.sla_threshold_ms:
            self._violation_count += 1

            logger.warn(
                "sla violation: p95 latency exceeds threshold",
                {
                    "p50_ms": stats.p50,
                    "p95_ms": stats.p95,
                    "p99_ms": stats.p99,
                    "threshold_ms": self.sla_threshold_ms,
                    "sample_count": stats.count,
                    "total_violations": self._violation_count,
                }
            )

    def xǁSLAMonitorǁ_check_sla_violation__mutmut_12(self) -> None:
        """
        Check if current p95 violates SLA threshold and alert if needed

        Violation: p95 > 5000ms (5 seconds)
        """
        stats = self.get_stats()

        if stats.p95 > self.sla_threshold_ms:
            self._violation_count += 1

            logger.warn(
                "SLA VIOLATION: P95 LATENCY EXCEEDS THRESHOLD",
                {
                    "p50_ms": stats.p50,
                    "p95_ms": stats.p95,
                    "p99_ms": stats.p99,
                    "threshold_ms": self.sla_threshold_ms,
                    "sample_count": stats.count,
                    "total_violations": self._violation_count,
                }
            )

    def xǁSLAMonitorǁ_check_sla_violation__mutmut_13(self) -> None:
        """
        Check if current p95 violates SLA threshold and alert if needed

        Violation: p95 > 5000ms (5 seconds)
        """
        stats = self.get_stats()

        if stats.p95 > self.sla_threshold_ms:
            self._violation_count += 1

            logger.warn(
                "SLA VIOLATION: p95 latency exceeds threshold",
                {
                    "XXp50_msXX": stats.p50,
                    "p95_ms": stats.p95,
                    "p99_ms": stats.p99,
                    "threshold_ms": self.sla_threshold_ms,
                    "sample_count": stats.count,
                    "total_violations": self._violation_count,
                }
            )

    def xǁSLAMonitorǁ_check_sla_violation__mutmut_14(self) -> None:
        """
        Check if current p95 violates SLA threshold and alert if needed

        Violation: p95 > 5000ms (5 seconds)
        """
        stats = self.get_stats()

        if stats.p95 > self.sla_threshold_ms:
            self._violation_count += 1

            logger.warn(
                "SLA VIOLATION: p95 latency exceeds threshold",
                {
                    "P50_MS": stats.p50,
                    "p95_ms": stats.p95,
                    "p99_ms": stats.p99,
                    "threshold_ms": self.sla_threshold_ms,
                    "sample_count": stats.count,
                    "total_violations": self._violation_count,
                }
            )

    def xǁSLAMonitorǁ_check_sla_violation__mutmut_15(self) -> None:
        """
        Check if current p95 violates SLA threshold and alert if needed

        Violation: p95 > 5000ms (5 seconds)
        """
        stats = self.get_stats()

        if stats.p95 > self.sla_threshold_ms:
            self._violation_count += 1

            logger.warn(
                "SLA VIOLATION: p95 latency exceeds threshold",
                {
                    "p50_ms": stats.p50,
                    "XXp95_msXX": stats.p95,
                    "p99_ms": stats.p99,
                    "threshold_ms": self.sla_threshold_ms,
                    "sample_count": stats.count,
                    "total_violations": self._violation_count,
                }
            )

    def xǁSLAMonitorǁ_check_sla_violation__mutmut_16(self) -> None:
        """
        Check if current p95 violates SLA threshold and alert if needed

        Violation: p95 > 5000ms (5 seconds)
        """
        stats = self.get_stats()

        if stats.p95 > self.sla_threshold_ms:
            self._violation_count += 1

            logger.warn(
                "SLA VIOLATION: p95 latency exceeds threshold",
                {
                    "p50_ms": stats.p50,
                    "P95_MS": stats.p95,
                    "p99_ms": stats.p99,
                    "threshold_ms": self.sla_threshold_ms,
                    "sample_count": stats.count,
                    "total_violations": self._violation_count,
                }
            )

    def xǁSLAMonitorǁ_check_sla_violation__mutmut_17(self) -> None:
        """
        Check if current p95 violates SLA threshold and alert if needed

        Violation: p95 > 5000ms (5 seconds)
        """
        stats = self.get_stats()

        if stats.p95 > self.sla_threshold_ms:
            self._violation_count += 1

            logger.warn(
                "SLA VIOLATION: p95 latency exceeds threshold",
                {
                    "p50_ms": stats.p50,
                    "p95_ms": stats.p95,
                    "XXp99_msXX": stats.p99,
                    "threshold_ms": self.sla_threshold_ms,
                    "sample_count": stats.count,
                    "total_violations": self._violation_count,
                }
            )

    def xǁSLAMonitorǁ_check_sla_violation__mutmut_18(self) -> None:
        """
        Check if current p95 violates SLA threshold and alert if needed

        Violation: p95 > 5000ms (5 seconds)
        """
        stats = self.get_stats()

        if stats.p95 > self.sla_threshold_ms:
            self._violation_count += 1

            logger.warn(
                "SLA VIOLATION: p95 latency exceeds threshold",
                {
                    "p50_ms": stats.p50,
                    "p95_ms": stats.p95,
                    "P99_MS": stats.p99,
                    "threshold_ms": self.sla_threshold_ms,
                    "sample_count": stats.count,
                    "total_violations": self._violation_count,
                }
            )

    def xǁSLAMonitorǁ_check_sla_violation__mutmut_19(self) -> None:
        """
        Check if current p95 violates SLA threshold and alert if needed

        Violation: p95 > 5000ms (5 seconds)
        """
        stats = self.get_stats()

        if stats.p95 > self.sla_threshold_ms:
            self._violation_count += 1

            logger.warn(
                "SLA VIOLATION: p95 latency exceeds threshold",
                {
                    "p50_ms": stats.p50,
                    "p95_ms": stats.p95,
                    "p99_ms": stats.p99,
                    "XXthreshold_msXX": self.sla_threshold_ms,
                    "sample_count": stats.count,
                    "total_violations": self._violation_count,
                }
            )

    def xǁSLAMonitorǁ_check_sla_violation__mutmut_20(self) -> None:
        """
        Check if current p95 violates SLA threshold and alert if needed

        Violation: p95 > 5000ms (5 seconds)
        """
        stats = self.get_stats()

        if stats.p95 > self.sla_threshold_ms:
            self._violation_count += 1

            logger.warn(
                "SLA VIOLATION: p95 latency exceeds threshold",
                {
                    "p50_ms": stats.p50,
                    "p95_ms": stats.p95,
                    "p99_ms": stats.p99,
                    "THRESHOLD_MS": self.sla_threshold_ms,
                    "sample_count": stats.count,
                    "total_violations": self._violation_count,
                }
            )

    def xǁSLAMonitorǁ_check_sla_violation__mutmut_21(self) -> None:
        """
        Check if current p95 violates SLA threshold and alert if needed

        Violation: p95 > 5000ms (5 seconds)
        """
        stats = self.get_stats()

        if stats.p95 > self.sla_threshold_ms:
            self._violation_count += 1

            logger.warn(
                "SLA VIOLATION: p95 latency exceeds threshold",
                {
                    "p50_ms": stats.p50,
                    "p95_ms": stats.p95,
                    "p99_ms": stats.p99,
                    "threshold_ms": self.sla_threshold_ms,
                    "XXsample_countXX": stats.count,
                    "total_violations": self._violation_count,
                }
            )

    def xǁSLAMonitorǁ_check_sla_violation__mutmut_22(self) -> None:
        """
        Check if current p95 violates SLA threshold and alert if needed

        Violation: p95 > 5000ms (5 seconds)
        """
        stats = self.get_stats()

        if stats.p95 > self.sla_threshold_ms:
            self._violation_count += 1

            logger.warn(
                "SLA VIOLATION: p95 latency exceeds threshold",
                {
                    "p50_ms": stats.p50,
                    "p95_ms": stats.p95,
                    "p99_ms": stats.p99,
                    "threshold_ms": self.sla_threshold_ms,
                    "SAMPLE_COUNT": stats.count,
                    "total_violations": self._violation_count,
                }
            )

    def xǁSLAMonitorǁ_check_sla_violation__mutmut_23(self) -> None:
        """
        Check if current p95 violates SLA threshold and alert if needed

        Violation: p95 > 5000ms (5 seconds)
        """
        stats = self.get_stats()

        if stats.p95 > self.sla_threshold_ms:
            self._violation_count += 1

            logger.warn(
                "SLA VIOLATION: p95 latency exceeds threshold",
                {
                    "p50_ms": stats.p50,
                    "p95_ms": stats.p95,
                    "p99_ms": stats.p99,
                    "threshold_ms": self.sla_threshold_ms,
                    "sample_count": stats.count,
                    "XXtotal_violationsXX": self._violation_count,
                }
            )

    def xǁSLAMonitorǁ_check_sla_violation__mutmut_24(self) -> None:
        """
        Check if current p95 violates SLA threshold and alert if needed

        Violation: p95 > 5000ms (5 seconds)
        """
        stats = self.get_stats()

        if stats.p95 > self.sla_threshold_ms:
            self._violation_count += 1

            logger.warn(
                "SLA VIOLATION: p95 latency exceeds threshold",
                {
                    "p50_ms": stats.p50,
                    "p95_ms": stats.p95,
                    "p99_ms": stats.p99,
                    "threshold_ms": self.sla_threshold_ms,
                    "sample_count": stats.count,
                    "TOTAL_VIOLATIONS": self._violation_count,
                }
            )
    
    xǁSLAMonitorǁ_check_sla_violation__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁSLAMonitorǁ_check_sla_violation__mutmut_1': xǁSLAMonitorǁ_check_sla_violation__mutmut_1, 
        'xǁSLAMonitorǁ_check_sla_violation__mutmut_2': xǁSLAMonitorǁ_check_sla_violation__mutmut_2, 
        'xǁSLAMonitorǁ_check_sla_violation__mutmut_3': xǁSLAMonitorǁ_check_sla_violation__mutmut_3, 
        'xǁSLAMonitorǁ_check_sla_violation__mutmut_4': xǁSLAMonitorǁ_check_sla_violation__mutmut_4, 
        'xǁSLAMonitorǁ_check_sla_violation__mutmut_5': xǁSLAMonitorǁ_check_sla_violation__mutmut_5, 
        'xǁSLAMonitorǁ_check_sla_violation__mutmut_6': xǁSLAMonitorǁ_check_sla_violation__mutmut_6, 
        'xǁSLAMonitorǁ_check_sla_violation__mutmut_7': xǁSLAMonitorǁ_check_sla_violation__mutmut_7, 
        'xǁSLAMonitorǁ_check_sla_violation__mutmut_8': xǁSLAMonitorǁ_check_sla_violation__mutmut_8, 
        'xǁSLAMonitorǁ_check_sla_violation__mutmut_9': xǁSLAMonitorǁ_check_sla_violation__mutmut_9, 
        'xǁSLAMonitorǁ_check_sla_violation__mutmut_10': xǁSLAMonitorǁ_check_sla_violation__mutmut_10, 
        'xǁSLAMonitorǁ_check_sla_violation__mutmut_11': xǁSLAMonitorǁ_check_sla_violation__mutmut_11, 
        'xǁSLAMonitorǁ_check_sla_violation__mutmut_12': xǁSLAMonitorǁ_check_sla_violation__mutmut_12, 
        'xǁSLAMonitorǁ_check_sla_violation__mutmut_13': xǁSLAMonitorǁ_check_sla_violation__mutmut_13, 
        'xǁSLAMonitorǁ_check_sla_violation__mutmut_14': xǁSLAMonitorǁ_check_sla_violation__mutmut_14, 
        'xǁSLAMonitorǁ_check_sla_violation__mutmut_15': xǁSLAMonitorǁ_check_sla_violation__mutmut_15, 
        'xǁSLAMonitorǁ_check_sla_violation__mutmut_16': xǁSLAMonitorǁ_check_sla_violation__mutmut_16, 
        'xǁSLAMonitorǁ_check_sla_violation__mutmut_17': xǁSLAMonitorǁ_check_sla_violation__mutmut_17, 
        'xǁSLAMonitorǁ_check_sla_violation__mutmut_18': xǁSLAMonitorǁ_check_sla_violation__mutmut_18, 
        'xǁSLAMonitorǁ_check_sla_violation__mutmut_19': xǁSLAMonitorǁ_check_sla_violation__mutmut_19, 
        'xǁSLAMonitorǁ_check_sla_violation__mutmut_20': xǁSLAMonitorǁ_check_sla_violation__mutmut_20, 
        'xǁSLAMonitorǁ_check_sla_violation__mutmut_21': xǁSLAMonitorǁ_check_sla_violation__mutmut_21, 
        'xǁSLAMonitorǁ_check_sla_violation__mutmut_22': xǁSLAMonitorǁ_check_sla_violation__mutmut_22, 
        'xǁSLAMonitorǁ_check_sla_violation__mutmut_23': xǁSLAMonitorǁ_check_sla_violation__mutmut_23, 
        'xǁSLAMonitorǁ_check_sla_violation__mutmut_24': xǁSLAMonitorǁ_check_sla_violation__mutmut_24
    }
    
    def _check_sla_violation(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁSLAMonitorǁ_check_sla_violation__mutmut_orig"), object.__getattribute__(self, "xǁSLAMonitorǁ_check_sla_violation__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _check_sla_violation.__signature__ = _mutmut_signature(xǁSLAMonitorǁ_check_sla_violation__mutmut_orig)
    xǁSLAMonitorǁ_check_sla_violation__mutmut_orig.__name__ = 'xǁSLAMonitorǁ_check_sla_violation'

    def xǁSLAMonitorǁget_summary__mutmut_orig(self) -> Dict[str, Any]:
        """
        Get human-readable summary of SLA metrics

        Returns:
            Dictionary with formatted SLA statistics
        """
        stats = self.get_stats()

        return {
            "percentiles": {
                "p50_ms": stats.p50,
                "p95_ms": stats.p95,
                "p99_ms": stats.p99,
            },
            "threshold_ms": self.sla_threshold_ms,
            "violations": {
                "count": stats.violations,
                "last_occurrence": stats.last_violation_timestamp,
            },
            "sample_size": stats.count,
            "sla_met": stats.p95 <= self.sla_threshold_ms,
        }

    def xǁSLAMonitorǁget_summary__mutmut_1(self) -> Dict[str, Any]:
        """
        Get human-readable summary of SLA metrics

        Returns:
            Dictionary with formatted SLA statistics
        """
        stats = None

        return {
            "percentiles": {
                "p50_ms": stats.p50,
                "p95_ms": stats.p95,
                "p99_ms": stats.p99,
            },
            "threshold_ms": self.sla_threshold_ms,
            "violations": {
                "count": stats.violations,
                "last_occurrence": stats.last_violation_timestamp,
            },
            "sample_size": stats.count,
            "sla_met": stats.p95 <= self.sla_threshold_ms,
        }

    def xǁSLAMonitorǁget_summary__mutmut_2(self) -> Dict[str, Any]:
        """
        Get human-readable summary of SLA metrics

        Returns:
            Dictionary with formatted SLA statistics
        """
        stats = self.get_stats()

        return {
            "XXpercentilesXX": {
                "p50_ms": stats.p50,
                "p95_ms": stats.p95,
                "p99_ms": stats.p99,
            },
            "threshold_ms": self.sla_threshold_ms,
            "violations": {
                "count": stats.violations,
                "last_occurrence": stats.last_violation_timestamp,
            },
            "sample_size": stats.count,
            "sla_met": stats.p95 <= self.sla_threshold_ms,
        }

    def xǁSLAMonitorǁget_summary__mutmut_3(self) -> Dict[str, Any]:
        """
        Get human-readable summary of SLA metrics

        Returns:
            Dictionary with formatted SLA statistics
        """
        stats = self.get_stats()

        return {
            "PERCENTILES": {
                "p50_ms": stats.p50,
                "p95_ms": stats.p95,
                "p99_ms": stats.p99,
            },
            "threshold_ms": self.sla_threshold_ms,
            "violations": {
                "count": stats.violations,
                "last_occurrence": stats.last_violation_timestamp,
            },
            "sample_size": stats.count,
            "sla_met": stats.p95 <= self.sla_threshold_ms,
        }

    def xǁSLAMonitorǁget_summary__mutmut_4(self) -> Dict[str, Any]:
        """
        Get human-readable summary of SLA metrics

        Returns:
            Dictionary with formatted SLA statistics
        """
        stats = self.get_stats()

        return {
            "percentiles": {
                "XXp50_msXX": stats.p50,
                "p95_ms": stats.p95,
                "p99_ms": stats.p99,
            },
            "threshold_ms": self.sla_threshold_ms,
            "violations": {
                "count": stats.violations,
                "last_occurrence": stats.last_violation_timestamp,
            },
            "sample_size": stats.count,
            "sla_met": stats.p95 <= self.sla_threshold_ms,
        }

    def xǁSLAMonitorǁget_summary__mutmut_5(self) -> Dict[str, Any]:
        """
        Get human-readable summary of SLA metrics

        Returns:
            Dictionary with formatted SLA statistics
        """
        stats = self.get_stats()

        return {
            "percentiles": {
                "P50_MS": stats.p50,
                "p95_ms": stats.p95,
                "p99_ms": stats.p99,
            },
            "threshold_ms": self.sla_threshold_ms,
            "violations": {
                "count": stats.violations,
                "last_occurrence": stats.last_violation_timestamp,
            },
            "sample_size": stats.count,
            "sla_met": stats.p95 <= self.sla_threshold_ms,
        }

    def xǁSLAMonitorǁget_summary__mutmut_6(self) -> Dict[str, Any]:
        """
        Get human-readable summary of SLA metrics

        Returns:
            Dictionary with formatted SLA statistics
        """
        stats = self.get_stats()

        return {
            "percentiles": {
                "p50_ms": stats.p50,
                "XXp95_msXX": stats.p95,
                "p99_ms": stats.p99,
            },
            "threshold_ms": self.sla_threshold_ms,
            "violations": {
                "count": stats.violations,
                "last_occurrence": stats.last_violation_timestamp,
            },
            "sample_size": stats.count,
            "sla_met": stats.p95 <= self.sla_threshold_ms,
        }

    def xǁSLAMonitorǁget_summary__mutmut_7(self) -> Dict[str, Any]:
        """
        Get human-readable summary of SLA metrics

        Returns:
            Dictionary with formatted SLA statistics
        """
        stats = self.get_stats()

        return {
            "percentiles": {
                "p50_ms": stats.p50,
                "P95_MS": stats.p95,
                "p99_ms": stats.p99,
            },
            "threshold_ms": self.sla_threshold_ms,
            "violations": {
                "count": stats.violations,
                "last_occurrence": stats.last_violation_timestamp,
            },
            "sample_size": stats.count,
            "sla_met": stats.p95 <= self.sla_threshold_ms,
        }

    def xǁSLAMonitorǁget_summary__mutmut_8(self) -> Dict[str, Any]:
        """
        Get human-readable summary of SLA metrics

        Returns:
            Dictionary with formatted SLA statistics
        """
        stats = self.get_stats()

        return {
            "percentiles": {
                "p50_ms": stats.p50,
                "p95_ms": stats.p95,
                "XXp99_msXX": stats.p99,
            },
            "threshold_ms": self.sla_threshold_ms,
            "violations": {
                "count": stats.violations,
                "last_occurrence": stats.last_violation_timestamp,
            },
            "sample_size": stats.count,
            "sla_met": stats.p95 <= self.sla_threshold_ms,
        }

    def xǁSLAMonitorǁget_summary__mutmut_9(self) -> Dict[str, Any]:
        """
        Get human-readable summary of SLA metrics

        Returns:
            Dictionary with formatted SLA statistics
        """
        stats = self.get_stats()

        return {
            "percentiles": {
                "p50_ms": stats.p50,
                "p95_ms": stats.p95,
                "P99_MS": stats.p99,
            },
            "threshold_ms": self.sla_threshold_ms,
            "violations": {
                "count": stats.violations,
                "last_occurrence": stats.last_violation_timestamp,
            },
            "sample_size": stats.count,
            "sla_met": stats.p95 <= self.sla_threshold_ms,
        }

    def xǁSLAMonitorǁget_summary__mutmut_10(self) -> Dict[str, Any]:
        """
        Get human-readable summary of SLA metrics

        Returns:
            Dictionary with formatted SLA statistics
        """
        stats = self.get_stats()

        return {
            "percentiles": {
                "p50_ms": stats.p50,
                "p95_ms": stats.p95,
                "p99_ms": stats.p99,
            },
            "XXthreshold_msXX": self.sla_threshold_ms,
            "violations": {
                "count": stats.violations,
                "last_occurrence": stats.last_violation_timestamp,
            },
            "sample_size": stats.count,
            "sla_met": stats.p95 <= self.sla_threshold_ms,
        }

    def xǁSLAMonitorǁget_summary__mutmut_11(self) -> Dict[str, Any]:
        """
        Get human-readable summary of SLA metrics

        Returns:
            Dictionary with formatted SLA statistics
        """
        stats = self.get_stats()

        return {
            "percentiles": {
                "p50_ms": stats.p50,
                "p95_ms": stats.p95,
                "p99_ms": stats.p99,
            },
            "THRESHOLD_MS": self.sla_threshold_ms,
            "violations": {
                "count": stats.violations,
                "last_occurrence": stats.last_violation_timestamp,
            },
            "sample_size": stats.count,
            "sla_met": stats.p95 <= self.sla_threshold_ms,
        }

    def xǁSLAMonitorǁget_summary__mutmut_12(self) -> Dict[str, Any]:
        """
        Get human-readable summary of SLA metrics

        Returns:
            Dictionary with formatted SLA statistics
        """
        stats = self.get_stats()

        return {
            "percentiles": {
                "p50_ms": stats.p50,
                "p95_ms": stats.p95,
                "p99_ms": stats.p99,
            },
            "threshold_ms": self.sla_threshold_ms,
            "XXviolationsXX": {
                "count": stats.violations,
                "last_occurrence": stats.last_violation_timestamp,
            },
            "sample_size": stats.count,
            "sla_met": stats.p95 <= self.sla_threshold_ms,
        }

    def xǁSLAMonitorǁget_summary__mutmut_13(self) -> Dict[str, Any]:
        """
        Get human-readable summary of SLA metrics

        Returns:
            Dictionary with formatted SLA statistics
        """
        stats = self.get_stats()

        return {
            "percentiles": {
                "p50_ms": stats.p50,
                "p95_ms": stats.p95,
                "p99_ms": stats.p99,
            },
            "threshold_ms": self.sla_threshold_ms,
            "VIOLATIONS": {
                "count": stats.violations,
                "last_occurrence": stats.last_violation_timestamp,
            },
            "sample_size": stats.count,
            "sla_met": stats.p95 <= self.sla_threshold_ms,
        }

    def xǁSLAMonitorǁget_summary__mutmut_14(self) -> Dict[str, Any]:
        """
        Get human-readable summary of SLA metrics

        Returns:
            Dictionary with formatted SLA statistics
        """
        stats = self.get_stats()

        return {
            "percentiles": {
                "p50_ms": stats.p50,
                "p95_ms": stats.p95,
                "p99_ms": stats.p99,
            },
            "threshold_ms": self.sla_threshold_ms,
            "violations": {
                "XXcountXX": stats.violations,
                "last_occurrence": stats.last_violation_timestamp,
            },
            "sample_size": stats.count,
            "sla_met": stats.p95 <= self.sla_threshold_ms,
        }

    def xǁSLAMonitorǁget_summary__mutmut_15(self) -> Dict[str, Any]:
        """
        Get human-readable summary of SLA metrics

        Returns:
            Dictionary with formatted SLA statistics
        """
        stats = self.get_stats()

        return {
            "percentiles": {
                "p50_ms": stats.p50,
                "p95_ms": stats.p95,
                "p99_ms": stats.p99,
            },
            "threshold_ms": self.sla_threshold_ms,
            "violations": {
                "COUNT": stats.violations,
                "last_occurrence": stats.last_violation_timestamp,
            },
            "sample_size": stats.count,
            "sla_met": stats.p95 <= self.sla_threshold_ms,
        }

    def xǁSLAMonitorǁget_summary__mutmut_16(self) -> Dict[str, Any]:
        """
        Get human-readable summary of SLA metrics

        Returns:
            Dictionary with formatted SLA statistics
        """
        stats = self.get_stats()

        return {
            "percentiles": {
                "p50_ms": stats.p50,
                "p95_ms": stats.p95,
                "p99_ms": stats.p99,
            },
            "threshold_ms": self.sla_threshold_ms,
            "violations": {
                "count": stats.violations,
                "XXlast_occurrenceXX": stats.last_violation_timestamp,
            },
            "sample_size": stats.count,
            "sla_met": stats.p95 <= self.sla_threshold_ms,
        }

    def xǁSLAMonitorǁget_summary__mutmut_17(self) -> Dict[str, Any]:
        """
        Get human-readable summary of SLA metrics

        Returns:
            Dictionary with formatted SLA statistics
        """
        stats = self.get_stats()

        return {
            "percentiles": {
                "p50_ms": stats.p50,
                "p95_ms": stats.p95,
                "p99_ms": stats.p99,
            },
            "threshold_ms": self.sla_threshold_ms,
            "violations": {
                "count": stats.violations,
                "LAST_OCCURRENCE": stats.last_violation_timestamp,
            },
            "sample_size": stats.count,
            "sla_met": stats.p95 <= self.sla_threshold_ms,
        }

    def xǁSLAMonitorǁget_summary__mutmut_18(self) -> Dict[str, Any]:
        """
        Get human-readable summary of SLA metrics

        Returns:
            Dictionary with formatted SLA statistics
        """
        stats = self.get_stats()

        return {
            "percentiles": {
                "p50_ms": stats.p50,
                "p95_ms": stats.p95,
                "p99_ms": stats.p99,
            },
            "threshold_ms": self.sla_threshold_ms,
            "violations": {
                "count": stats.violations,
                "last_occurrence": stats.last_violation_timestamp,
            },
            "XXsample_sizeXX": stats.count,
            "sla_met": stats.p95 <= self.sla_threshold_ms,
        }

    def xǁSLAMonitorǁget_summary__mutmut_19(self) -> Dict[str, Any]:
        """
        Get human-readable summary of SLA metrics

        Returns:
            Dictionary with formatted SLA statistics
        """
        stats = self.get_stats()

        return {
            "percentiles": {
                "p50_ms": stats.p50,
                "p95_ms": stats.p95,
                "p99_ms": stats.p99,
            },
            "threshold_ms": self.sla_threshold_ms,
            "violations": {
                "count": stats.violations,
                "last_occurrence": stats.last_violation_timestamp,
            },
            "SAMPLE_SIZE": stats.count,
            "sla_met": stats.p95 <= self.sla_threshold_ms,
        }

    def xǁSLAMonitorǁget_summary__mutmut_20(self) -> Dict[str, Any]:
        """
        Get human-readable summary of SLA metrics

        Returns:
            Dictionary with formatted SLA statistics
        """
        stats = self.get_stats()

        return {
            "percentiles": {
                "p50_ms": stats.p50,
                "p95_ms": stats.p95,
                "p99_ms": stats.p99,
            },
            "threshold_ms": self.sla_threshold_ms,
            "violations": {
                "count": stats.violations,
                "last_occurrence": stats.last_violation_timestamp,
            },
            "sample_size": stats.count,
            "XXsla_metXX": stats.p95 <= self.sla_threshold_ms,
        }

    def xǁSLAMonitorǁget_summary__mutmut_21(self) -> Dict[str, Any]:
        """
        Get human-readable summary of SLA metrics

        Returns:
            Dictionary with formatted SLA statistics
        """
        stats = self.get_stats()

        return {
            "percentiles": {
                "p50_ms": stats.p50,
                "p95_ms": stats.p95,
                "p99_ms": stats.p99,
            },
            "threshold_ms": self.sla_threshold_ms,
            "violations": {
                "count": stats.violations,
                "last_occurrence": stats.last_violation_timestamp,
            },
            "sample_size": stats.count,
            "SLA_MET": stats.p95 <= self.sla_threshold_ms,
        }

    def xǁSLAMonitorǁget_summary__mutmut_22(self) -> Dict[str, Any]:
        """
        Get human-readable summary of SLA metrics

        Returns:
            Dictionary with formatted SLA statistics
        """
        stats = self.get_stats()

        return {
            "percentiles": {
                "p50_ms": stats.p50,
                "p95_ms": stats.p95,
                "p99_ms": stats.p99,
            },
            "threshold_ms": self.sla_threshold_ms,
            "violations": {
                "count": stats.violations,
                "last_occurrence": stats.last_violation_timestamp,
            },
            "sample_size": stats.count,
            "sla_met": stats.p95 < self.sla_threshold_ms,
        }
    
    xǁSLAMonitorǁget_summary__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁSLAMonitorǁget_summary__mutmut_1': xǁSLAMonitorǁget_summary__mutmut_1, 
        'xǁSLAMonitorǁget_summary__mutmut_2': xǁSLAMonitorǁget_summary__mutmut_2, 
        'xǁSLAMonitorǁget_summary__mutmut_3': xǁSLAMonitorǁget_summary__mutmut_3, 
        'xǁSLAMonitorǁget_summary__mutmut_4': xǁSLAMonitorǁget_summary__mutmut_4, 
        'xǁSLAMonitorǁget_summary__mutmut_5': xǁSLAMonitorǁget_summary__mutmut_5, 
        'xǁSLAMonitorǁget_summary__mutmut_6': xǁSLAMonitorǁget_summary__mutmut_6, 
        'xǁSLAMonitorǁget_summary__mutmut_7': xǁSLAMonitorǁget_summary__mutmut_7, 
        'xǁSLAMonitorǁget_summary__mutmut_8': xǁSLAMonitorǁget_summary__mutmut_8, 
        'xǁSLAMonitorǁget_summary__mutmut_9': xǁSLAMonitorǁget_summary__mutmut_9, 
        'xǁSLAMonitorǁget_summary__mutmut_10': xǁSLAMonitorǁget_summary__mutmut_10, 
        'xǁSLAMonitorǁget_summary__mutmut_11': xǁSLAMonitorǁget_summary__mutmut_11, 
        'xǁSLAMonitorǁget_summary__mutmut_12': xǁSLAMonitorǁget_summary__mutmut_12, 
        'xǁSLAMonitorǁget_summary__mutmut_13': xǁSLAMonitorǁget_summary__mutmut_13, 
        'xǁSLAMonitorǁget_summary__mutmut_14': xǁSLAMonitorǁget_summary__mutmut_14, 
        'xǁSLAMonitorǁget_summary__mutmut_15': xǁSLAMonitorǁget_summary__mutmut_15, 
        'xǁSLAMonitorǁget_summary__mutmut_16': xǁSLAMonitorǁget_summary__mutmut_16, 
        'xǁSLAMonitorǁget_summary__mutmut_17': xǁSLAMonitorǁget_summary__mutmut_17, 
        'xǁSLAMonitorǁget_summary__mutmut_18': xǁSLAMonitorǁget_summary__mutmut_18, 
        'xǁSLAMonitorǁget_summary__mutmut_19': xǁSLAMonitorǁget_summary__mutmut_19, 
        'xǁSLAMonitorǁget_summary__mutmut_20': xǁSLAMonitorǁget_summary__mutmut_20, 
        'xǁSLAMonitorǁget_summary__mutmut_21': xǁSLAMonitorǁget_summary__mutmut_21, 
        'xǁSLAMonitorǁget_summary__mutmut_22': xǁSLAMonitorǁget_summary__mutmut_22
    }
    
    def get_summary(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁSLAMonitorǁget_summary__mutmut_orig"), object.__getattribute__(self, "xǁSLAMonitorǁget_summary__mutmut_mutants"), args, kwargs, self)
        return result 
    
    get_summary.__signature__ = _mutmut_signature(xǁSLAMonitorǁget_summary__mutmut_orig)
    xǁSLAMonitorǁget_summary__mutmut_orig.__name__ = 'xǁSLAMonitorǁget_summary'


# Global singleton instance
_sla_monitor: SLAMonitor | None = None


def x_get_sla_monitor__mutmut_orig() -> SLAMonitor:
    """
    Get global SLA monitor instance (singleton)

    Returns:
        Configured SLA monitor
    """
    global _sla_monitor
    if _sla_monitor is None:
        _sla_monitor = SLAMonitor()
    return _sla_monitor


def x_get_sla_monitor__mutmut_1() -> SLAMonitor:
    """
    Get global SLA monitor instance (singleton)

    Returns:
        Configured SLA monitor
    """
    global _sla_monitor
    if _sla_monitor is not None:
        _sla_monitor = SLAMonitor()
    return _sla_monitor


def x_get_sla_monitor__mutmut_2() -> SLAMonitor:
    """
    Get global SLA monitor instance (singleton)

    Returns:
        Configured SLA monitor
    """
    global _sla_monitor
    if _sla_monitor is None:
        _sla_monitor = None
    return _sla_monitor

x_get_sla_monitor__mutmut_mutants : ClassVar[MutantDict] = {
'x_get_sla_monitor__mutmut_1': x_get_sla_monitor__mutmut_1, 
    'x_get_sla_monitor__mutmut_2': x_get_sla_monitor__mutmut_2
}

def get_sla_monitor(*args, **kwargs):
    result = _mutmut_trampoline(x_get_sla_monitor__mutmut_orig, x_get_sla_monitor__mutmut_mutants, args, kwargs)
    return result 

get_sla_monitor.__signature__ = _mutmut_signature(x_get_sla_monitor__mutmut_orig)
x_get_sla_monitor__mutmut_orig.__name__ = 'x_get_sla_monitor'
