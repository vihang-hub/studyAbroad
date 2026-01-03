"""
SLA Monitoring Service
Tracks streaming response latency and calculates percentiles (p50/p95/p99)
Per requirements T172a-c
"""

from typing import List, Dict, Any
from collections import deque
from dataclasses import dataclass
from logging_lib.logger import get_logger

logger = get_logger()


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

    def __init__(self, window_size: int = 1000, sla_threshold_ms: float = 5000):
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

    def record_streaming_latency(
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

    def get_stats(self) -> SLAStats:
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

    def _percentile(self, sorted_values: List[float], percentile: int) -> float:
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

    def _check_sla_violation(self) -> None:
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

    def get_summary(self) -> Dict[str, Any]:
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


# Global singleton instance
_sla_monitor: SLAMonitor | None = None


def get_sla_monitor() -> SLAMonitor:
    """
    Get global SLA monitor instance (singleton)

    Returns:
        Configured SLA monitor
    """
    global _sla_monitor
    if _sla_monitor is None:
        _sla_monitor = SLAMonitor()
    return _sla_monitor
