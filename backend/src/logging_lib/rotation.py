"""
Custom log rotation handler with date-sequence naming
Implements hybrid rotation (size OR time-based) per T172d requirements

Format: app-YYYY-MM-DD-N.log where:
- N starts at 1 each day
- N increments when same-day rotation triggered by size
- N resets to 1 at midnight UTC
"""

from datetime import datetime, timedelta
from logging.handlers import RotatingFileHandler
from pathlib import Path


class DateSequenceRotatingHandler(RotatingFileHandler):
    """
    Custom rotating file handler with date-sequence naming

    Implements hybrid rotation:
    - Rotates when file reaches maxBytes
    - Rotates at midnight UTC (checked on each write)
    - File naming: app-YYYY-MM-DD-N.log

    Args:
        log_dir: Directory for log files
        max_bytes: Maximum file size before rotation (bytes)
        retention_days: Number of days to retain logs
    """

    def __init__(
        self,
        log_dir: str,
        max_bytes: int = 100 * 1024 * 1024,  # 100MB
        retention_days: int = 30
    ):
        self.log_dir = Path(log_dir)
        self.max_bytes = max_bytes
        self.retention_days = retention_days
        self.current_date = datetime.utcnow().date()

        # Ensure log directory exists
        self.log_dir.mkdir(parents=True, exist_ok=True)

        # Get initial log filename
        filename = self._get_log_filename()

        # Initialize parent RotatingFileHandler
        super().__init__(
            filename=str(filename),
            maxBytes=max_bytes,
            backupCount=0,  # We handle our own rotation
            encoding='utf-8'
        )

    def _get_log_filename(self) -> Path:
        """
        Get log filename for current date with next available sequence number

        Returns:
            Path to log file (e.g., /logs/app-2025-01-03-1.log)
        """
        date_str = self.current_date.strftime('%Y-%m-%d')
        pattern = f"app-{date_str}-*.log"
        existing_files = sorted(self.log_dir.glob(pattern))

        if not existing_files:
            # First file of the day
            sequence = 1
        else:
            # Get highest sequence number
            last_file = existing_files[-1].stem  # e.g., "app-2025-01-03-2"
            try:
                last_sequence = int(last_file.split('-')[-1])
                sequence = last_sequence + 1
            except (ValueError, IndexError):
                sequence = 1

        return self.log_dir / f"app-{date_str}-{sequence}.log"

    def shouldRollover(self, record) -> bool:
        """
        Determine if rollover should occur

        Checks two conditions:
        1. Current date has changed (midnight UTC passed)
        2. File size exceeds maxBytes

        Returns:
            True if rollover needed
        """
        # Check if date has changed
        current_date = datetime.utcnow().date()
        if current_date != self.current_date:
            self.current_date = current_date
            return True

        # Check size-based rollover (parent class logic)
        if self.maxBytes > 0:
            # Format the record to get accurate size
            msg = self.format(record)
            msg_size = len(msg.encode('utf-8')) + 1  # +1 for newline

            # Get current file size
            if self.stream:
                self.stream.seek(0, 2)  # Seek to end
                if self.stream.tell() + msg_size >= self.maxBytes:
                    return True

        return False

    def doRollover(self):
        """
        Perform log file rollover

        Creates new log file with incremented sequence number or new date.
        Cleans up old log files exceeding retention period.
        """
        # Close current stream
        if self.stream:
            self.stream.close()
            self.stream = None

        # Get new filename (sequence will auto-increment or reset for new date)
        new_filename = self._get_log_filename()
        self.baseFilename = str(new_filename)

        # Open new file
        self.stream = self._open()

        # Clean up old log files
        self._cleanup_old_logs()

    def _cleanup_old_logs(self):
        """
        Delete log files older than retention_days

        T172e: Log retention cleanup
        """
        # Skip cleanup if retention disabled
        if self.retention_days <= 0:
            return

        cutoff_date = datetime.utcnow().date() - timedelta(days=self.retention_days)
        pattern = "app-*.log"

        for log_file in self.log_dir.glob(pattern):
            try:
                # Parse date from filename (app-YYYY-MM-DD-N.log)
                # Use stem to remove .log extension first
                parts = log_file.stem.split('-')
                if len(parts) >= 4:
                    # parts = ['app', 'YYYY', 'MM', 'DD', 'N']
                    file_date_str = f"{parts[1]}-{parts[2]}-{parts[3]}"
                    file_date = datetime.strptime(file_date_str, '%Y-%m-%d').date()

                    if file_date < cutoff_date:
                        log_file.unlink()
                        print(f"Deleted old log file: {log_file}")
            except (ValueError, IndexError, OSError) as e:
                # Skip files that don't match pattern or can't be deleted
                print(f"Warning: Could not process log file {log_file}: {e}")


def cleanup_old_logs(log_dir: str, retention_days: int):
    """
    Standalone function to cleanup old log files

    Can be called manually or via cron for log maintenance.

    Args:
        log_dir: Directory containing log files
        retention_days: Number of days to retain logs (0 = no cleanup)

    Returns:
        Number of files deleted
    """
    log_path = Path(log_dir)
    if not log_path.exists():
        return 0

    # Skip cleanup if retention disabled
    if retention_days <= 0:
        return 0

    cutoff_date = datetime.utcnow().date() - timedelta(days=retention_days)
    pattern = "app-*.log"
    deleted_count = 0

    for log_file in log_path.glob(pattern):
        try:
            # Parse date from filename (app-YYYY-MM-DD-N.log)
            # Use stem to remove .log extension first
            parts = log_file.stem.split('-')
            if len(parts) >= 4:
                # parts = ['app', 'YYYY', 'MM', 'DD', 'N']
                file_date_str = f"{parts[1]}-{parts[2]}-{parts[3]}"
                file_date = datetime.strptime(file_date_str, '%Y-%m-%d').date()

                if file_date < cutoff_date:
                    log_file.unlink()
                    deleted_count += 1
                    print(f"Deleted old log file: {log_file}")
        except (ValueError, IndexError, OSError) as e:
            print(f"Warning: Could not process log file {log_file}: {e}")

    print(f"Log cleanup complete: {deleted_count} files deleted")
    return deleted_count
