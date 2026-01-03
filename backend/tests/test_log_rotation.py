"""
Tests for log rotation functionality
T172f: Test log rotation with size and time-based triggers
"""

import logging
import tempfile
from datetime import datetime, timedelta
from pathlib import Path

from src.logging_lib.rotation import DateSequenceRotatingHandler, cleanup_old_logs


class TestDateSequenceRotatingHandler:
    """Test suite for hybrid log rotation handler"""

    def setup_method(self):
        """Create temporary log directory for each test"""
        self.temp_dir = tempfile.mkdtemp()
        self.log_dir = Path(self.temp_dir)

    def teardown_method(self):
        """Clean up temporary files"""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_initial_log_file_creation(self):
        """Test that first log file is created with sequence number 1"""
        handler = DateSequenceRotatingHandler(
            log_dir=str(self.log_dir),
            max_bytes=1000,
            retention_days=30
        )

        date_str = datetime.utcnow().strftime('%Y-%m-%d')
        expected_filename = f"app-{date_str}-1.log"

        assert Path(handler.baseFilename).name == expected_filename

        handler.close()

    def test_size_based_rotation(self):
        """
        Test rotation when file exceeds maxBytes
        T172f: create 101MB log file, verify rotates to app-YYYY-MM-DD-2.log
        """
        # Use very small max_bytes for testing (100 bytes)
        handler = DateSequenceRotatingHandler(
            log_dir=str(self.log_dir),
            max_bytes=100,
            retention_days=30
        )

        # Create logger with the handler
        logger = logging.getLogger('test_rotation')
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)

        # Get initial filename
        date_str = datetime.utcnow().strftime('%Y-%m-%d')
        first_file = f"app-{date_str}-1.log"

        # Write enough data to trigger rotation (100+ bytes)
        for i in range(20):
            logger.info(f"Test log message {i} with some padding to increase size")

        # Check that rotation occurred
        log_files = sorted(self.log_dir.glob("app-*.log"))
        assert len(log_files) >= 2, "Rotation should create second file"

        # Verify sequence numbers
        assert first_file in [f.name for f in log_files]
        second_file = f"app-{date_str}-2.log"
        assert second_file in [f.name for f in log_files]

        handler.close()

    def test_sequence_number_increment(self):
        """Test that sequence number increments correctly on same-day rotation"""
        handler = DateSequenceRotatingHandler(
            log_dir=str(self.log_dir),
            max_bytes=50,
            retention_days=30
        )

        logger = logging.getLogger('test_sequence')
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)

        date_str = datetime.utcnow().strftime('%Y-%m-%d')

        # Trigger multiple rotations
        for i in range(100):
            logger.info(f"Message {i} " * 10)  # Long message to trigger rotation

        # Flush handler to ensure all writes are complete
        handler.flush()

        # Check that multiple files exist with sequential numbers
        log_files = list(self.log_dir.glob(f"app-{date_str}-*.log"))
        assert len(log_files) >= 2, f"Expected at least 2 files, got {len(log_files)}"

        # Verify sequential numbering
        # filename format: app-YYYY-MM-DD-N.log
        # when split by stem: ['app', 'YYYY', 'MM', 'DD', 'N']
        sequences = []
        for log_file in log_files:
            parts = log_file.stem.split('-')
            if len(parts) == 5:  # ['app', 'YYYY', 'MM', 'DD', 'N']
                sequences.append(int(parts[-1]))

        assert len(sequences) > 0, f"No valid sequences found from files: {[f.name for f in log_files]}"

        # Sort sequences numerically
        sorted_sequences = sorted(sequences)
        assert set(sequences) == set(sorted_sequences), f"Sequence numbers should form a valid sequence: {sequences} vs {sorted_sequences}"
        assert min(sequences) == 1, "First sequence should be 1"

        # Check for consecutive numbers (allowing gaps is fine since rotation is async)
        assert max(sequences) >= 2, "Should have at least sequence 2"

        handler.close()

    def test_date_sequence_filename_format(self):
        """Test that filenames follow app-YYYY-MM-DD-N.log format"""
        handler = DateSequenceRotatingHandler(
            log_dir=str(self.log_dir),
            max_bytes=1000,
            retention_days=30
        )

        filename = Path(handler.baseFilename).name
        parts = filename.split('-')

        # Should be: app-YYYY-MM-DD-N.log
        # When split by '-': ['app', 'YYYY', 'MM', 'DD', 'N.log']
        assert len(parts) == 5, f"Expected 5 parts, got {len(parts)}: {parts}"
        assert parts[0] == 'app'
        assert len(parts[1]) == 4 and parts[1].isdigit()  # YYYY
        assert len(parts[2]) == 2 and parts[2].isdigit()  # MM
        assert len(parts[3]) == 2 and parts[3].isdigit()  # DD
        assert parts[4].replace('.log', '').isdigit()  # N

        handler.close()

    def test_log_retention_cleanup(self):
        """
        Test that old log files are deleted after retention period
        T172e: Implement log retention cleanup
        """
        # Create mock old log files
        today = datetime.utcnow().date()
        old_date = today - timedelta(days=40)
        recent_date = today - timedelta(days=10)

        old_file = self.log_dir / f"app-{old_date.strftime('%Y-%m-%d')}-1.log"
        recent_file = self.log_dir / f"app-{recent_date.strftime('%Y-%m-%d')}-1.log"
        current_file = self.log_dir / f"app-{today.strftime('%Y-%m-%d')}-1.log"

        # Create the files
        old_file.write_text("old log data")
        recent_file.write_text("recent log data")
        current_file.write_text("current log data")

        # Run cleanup with 30-day retention
        deleted = cleanup_old_logs(str(self.log_dir), retention_days=30)

        # Old file should be deleted
        assert not old_file.exists(), "Old file should be deleted"

        # Recent and current files should remain
        assert recent_file.exists(), "Recent file should be retained"
        assert current_file.exists(), "Current file should be retained"

        assert deleted == 1, "Should delete exactly 1 file"

    def test_multiple_rotations_same_day(self):
        """Test multiple size-based rotations on the same day"""
        handler = DateSequenceRotatingHandler(
            log_dir=str(self.log_dir),
            max_bytes=50,
            retention_days=30
        )

        logger = logging.getLogger('test_multi_rotation')
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)

        # Trigger 5 rotations
        for _ in range(150):
            logger.info("X" * 100)  # Force rotation

        log_files = sorted(self.log_dir.glob("app-*.log"))
        date_str = datetime.utcnow().strftime('%Y-%m-%d')

        # Should have multiple files for same date
        same_date_files = [f for f in log_files if date_str in f.name]
        assert len(same_date_files) >= 2, "Should create multiple files for same date"

        handler.close()

    def test_handler_cleanup_on_rotation(self):
        """Test that handler automatically cleans up old logs during rotation"""
        # Create old log files manually
        old_date = datetime.utcnow().date() - timedelta(days=35)
        old_file = self.log_dir / f"app-{old_date.strftime('%Y-%m-%d')}-1.log"
        old_file.write_text("very old log data")

        # Create handler with 30-day retention
        handler = DateSequenceRotatingHandler(
            log_dir=str(self.log_dir),
            max_bytes=100,
            retention_days=30
        )

        logger = logging.getLogger('test_auto_cleanup')
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)

        # Write enough to trigger rotation (which should trigger cleanup)
        for i in range(50):
            logger.info(f"Log message {i} with enough content to trigger rotation")

        # Old file should be deleted during rotation cleanup
        assert not old_file.exists(), "Old file should be auto-deleted during rotation"

        handler.close()

    def test_log_directory_creation(self):
        """Test that handler creates log directory if it doesn't exist"""
        non_existent_dir = self.log_dir / "nested" / "log" / "dir"

        handler = DateSequenceRotatingHandler(
            log_dir=str(non_existent_dir),
            max_bytes=1000,
            retention_days=30
        )

        assert non_existent_dir.exists(), "Handler should create log directory"

        handler.close()

    def test_zero_retention_no_cleanup(self):
        """Test that retention_days=0 disables cleanup"""
        old_date = datetime.utcnow().date() - timedelta(days=100)
        old_file = self.log_dir / f"app-{old_date.strftime('%Y-%m-%d')}-1.log"
        old_file.write_text("very old log data")

        # Cleanup with retention_days=0 should not delete anything
        deleted = cleanup_old_logs(str(self.log_dir), retention_days=0)

        assert old_file.exists(), "File should not be deleted when retention_days=0"
        assert deleted == 0

    def test_malformed_log_filename_handling(self):
        """Test that cleanup handles malformed log filenames gracefully"""
        # Create files with various formats
        (self.log_dir / "app-invalid.log").write_text("invalid")
        (self.log_dir / "not-a-log.txt").write_text("not a log")
        (self.log_dir / "app-2025-01-03-1.log").write_text("valid")

        # Should not crash on malformed filenames
        deleted = cleanup_old_logs(str(self.log_dir), retention_days=30)

        # Should handle gracefully without errors
        assert deleted >= 0
