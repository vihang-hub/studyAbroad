"""
Custom log rotation handler with date-sequence naming
Implements hybrid rotation (size OR time-based) per T172d requirements

Format: app-YYYY-MM-DD-N.log where:
- N starts at 1 each day
- N increments when same-day rotation triggered by size
- N resets to 1 at midnight UTC
"""

import os
import glob
import time
from datetime import datetime, timedelta
from logging.handlers import RotatingFileHandler
from pathlib import Path
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

    def xǁDateSequenceRotatingHandlerǁ__init____mutmut_orig(
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

    def xǁDateSequenceRotatingHandlerǁ__init____mutmut_1(
        self,
        log_dir: str,
        max_bytes: int = 100 * 1024 * 1024,  # 100MB
        retention_days: int = 31
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

    def xǁDateSequenceRotatingHandlerǁ__init____mutmut_2(
        self,
        log_dir: str,
        max_bytes: int = 100 * 1024 * 1024,  # 100MB
        retention_days: int = 30
    ):
        self.log_dir = None
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

    def xǁDateSequenceRotatingHandlerǁ__init____mutmut_3(
        self,
        log_dir: str,
        max_bytes: int = 100 * 1024 * 1024,  # 100MB
        retention_days: int = 30
    ):
        self.log_dir = Path(None)
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

    def xǁDateSequenceRotatingHandlerǁ__init____mutmut_4(
        self,
        log_dir: str,
        max_bytes: int = 100 * 1024 * 1024,  # 100MB
        retention_days: int = 30
    ):
        self.log_dir = Path(log_dir)
        self.max_bytes = None
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

    def xǁDateSequenceRotatingHandlerǁ__init____mutmut_5(
        self,
        log_dir: str,
        max_bytes: int = 100 * 1024 * 1024,  # 100MB
        retention_days: int = 30
    ):
        self.log_dir = Path(log_dir)
        self.max_bytes = max_bytes
        self.retention_days = None
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

    def xǁDateSequenceRotatingHandlerǁ__init____mutmut_6(
        self,
        log_dir: str,
        max_bytes: int = 100 * 1024 * 1024,  # 100MB
        retention_days: int = 30
    ):
        self.log_dir = Path(log_dir)
        self.max_bytes = max_bytes
        self.retention_days = retention_days
        self.current_date = None

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

    def xǁDateSequenceRotatingHandlerǁ__init____mutmut_7(
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
        self.log_dir.mkdir(parents=None, exist_ok=True)

        # Get initial log filename
        filename = self._get_log_filename()

        # Initialize parent RotatingFileHandler
        super().__init__(
            filename=str(filename),
            maxBytes=max_bytes,
            backupCount=0,  # We handle our own rotation
            encoding='utf-8'
        )

    def xǁDateSequenceRotatingHandlerǁ__init____mutmut_8(
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
        self.log_dir.mkdir(parents=True, exist_ok=None)

        # Get initial log filename
        filename = self._get_log_filename()

        # Initialize parent RotatingFileHandler
        super().__init__(
            filename=str(filename),
            maxBytes=max_bytes,
            backupCount=0,  # We handle our own rotation
            encoding='utf-8'
        )

    def xǁDateSequenceRotatingHandlerǁ__init____mutmut_9(
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
        self.log_dir.mkdir(exist_ok=True)

        # Get initial log filename
        filename = self._get_log_filename()

        # Initialize parent RotatingFileHandler
        super().__init__(
            filename=str(filename),
            maxBytes=max_bytes,
            backupCount=0,  # We handle our own rotation
            encoding='utf-8'
        )

    def xǁDateSequenceRotatingHandlerǁ__init____mutmut_10(
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
        self.log_dir.mkdir(parents=True, )

        # Get initial log filename
        filename = self._get_log_filename()

        # Initialize parent RotatingFileHandler
        super().__init__(
            filename=str(filename),
            maxBytes=max_bytes,
            backupCount=0,  # We handle our own rotation
            encoding='utf-8'
        )

    def xǁDateSequenceRotatingHandlerǁ__init____mutmut_11(
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
        self.log_dir.mkdir(parents=False, exist_ok=True)

        # Get initial log filename
        filename = self._get_log_filename()

        # Initialize parent RotatingFileHandler
        super().__init__(
            filename=str(filename),
            maxBytes=max_bytes,
            backupCount=0,  # We handle our own rotation
            encoding='utf-8'
        )

    def xǁDateSequenceRotatingHandlerǁ__init____mutmut_12(
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
        self.log_dir.mkdir(parents=True, exist_ok=False)

        # Get initial log filename
        filename = self._get_log_filename()

        # Initialize parent RotatingFileHandler
        super().__init__(
            filename=str(filename),
            maxBytes=max_bytes,
            backupCount=0,  # We handle our own rotation
            encoding='utf-8'
        )

    def xǁDateSequenceRotatingHandlerǁ__init____mutmut_13(
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
        filename = None

        # Initialize parent RotatingFileHandler
        super().__init__(
            filename=str(filename),
            maxBytes=max_bytes,
            backupCount=0,  # We handle our own rotation
            encoding='utf-8'
        )

    def xǁDateSequenceRotatingHandlerǁ__init____mutmut_14(
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
            filename=None,
            maxBytes=max_bytes,
            backupCount=0,  # We handle our own rotation
            encoding='utf-8'
        )

    def xǁDateSequenceRotatingHandlerǁ__init____mutmut_15(
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
            maxBytes=None,
            backupCount=0,  # We handle our own rotation
            encoding='utf-8'
        )

    def xǁDateSequenceRotatingHandlerǁ__init____mutmut_16(
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
            backupCount=None,  # We handle our own rotation
            encoding='utf-8'
        )

    def xǁDateSequenceRotatingHandlerǁ__init____mutmut_17(
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
            encoding=None
        )

    def xǁDateSequenceRotatingHandlerǁ__init____mutmut_18(
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
            maxBytes=max_bytes,
            backupCount=0,  # We handle our own rotation
            encoding='utf-8'
        )

    def xǁDateSequenceRotatingHandlerǁ__init____mutmut_19(
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
            backupCount=0,  # We handle our own rotation
            encoding='utf-8'
        )

    def xǁDateSequenceRotatingHandlerǁ__init____mutmut_20(
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
            encoding='utf-8'
        )

    def xǁDateSequenceRotatingHandlerǁ__init____mutmut_21(
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
            )

    def xǁDateSequenceRotatingHandlerǁ__init____mutmut_22(
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
            filename=str(None),
            maxBytes=max_bytes,
            backupCount=0,  # We handle our own rotation
            encoding='utf-8'
        )

    def xǁDateSequenceRotatingHandlerǁ__init____mutmut_23(
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
            backupCount=1,  # We handle our own rotation
            encoding='utf-8'
        )

    def xǁDateSequenceRotatingHandlerǁ__init____mutmut_24(
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
            encoding='XXutf-8XX'
        )

    def xǁDateSequenceRotatingHandlerǁ__init____mutmut_25(
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
            encoding='UTF-8'
        )
    
    xǁDateSequenceRotatingHandlerǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁDateSequenceRotatingHandlerǁ__init____mutmut_1': xǁDateSequenceRotatingHandlerǁ__init____mutmut_1, 
        'xǁDateSequenceRotatingHandlerǁ__init____mutmut_2': xǁDateSequenceRotatingHandlerǁ__init____mutmut_2, 
        'xǁDateSequenceRotatingHandlerǁ__init____mutmut_3': xǁDateSequenceRotatingHandlerǁ__init____mutmut_3, 
        'xǁDateSequenceRotatingHandlerǁ__init____mutmut_4': xǁDateSequenceRotatingHandlerǁ__init____mutmut_4, 
        'xǁDateSequenceRotatingHandlerǁ__init____mutmut_5': xǁDateSequenceRotatingHandlerǁ__init____mutmut_5, 
        'xǁDateSequenceRotatingHandlerǁ__init____mutmut_6': xǁDateSequenceRotatingHandlerǁ__init____mutmut_6, 
        'xǁDateSequenceRotatingHandlerǁ__init____mutmut_7': xǁDateSequenceRotatingHandlerǁ__init____mutmut_7, 
        'xǁDateSequenceRotatingHandlerǁ__init____mutmut_8': xǁDateSequenceRotatingHandlerǁ__init____mutmut_8, 
        'xǁDateSequenceRotatingHandlerǁ__init____mutmut_9': xǁDateSequenceRotatingHandlerǁ__init____mutmut_9, 
        'xǁDateSequenceRotatingHandlerǁ__init____mutmut_10': xǁDateSequenceRotatingHandlerǁ__init____mutmut_10, 
        'xǁDateSequenceRotatingHandlerǁ__init____mutmut_11': xǁDateSequenceRotatingHandlerǁ__init____mutmut_11, 
        'xǁDateSequenceRotatingHandlerǁ__init____mutmut_12': xǁDateSequenceRotatingHandlerǁ__init____mutmut_12, 
        'xǁDateSequenceRotatingHandlerǁ__init____mutmut_13': xǁDateSequenceRotatingHandlerǁ__init____mutmut_13, 
        'xǁDateSequenceRotatingHandlerǁ__init____mutmut_14': xǁDateSequenceRotatingHandlerǁ__init____mutmut_14, 
        'xǁDateSequenceRotatingHandlerǁ__init____mutmut_15': xǁDateSequenceRotatingHandlerǁ__init____mutmut_15, 
        'xǁDateSequenceRotatingHandlerǁ__init____mutmut_16': xǁDateSequenceRotatingHandlerǁ__init____mutmut_16, 
        'xǁDateSequenceRotatingHandlerǁ__init____mutmut_17': xǁDateSequenceRotatingHandlerǁ__init____mutmut_17, 
        'xǁDateSequenceRotatingHandlerǁ__init____mutmut_18': xǁDateSequenceRotatingHandlerǁ__init____mutmut_18, 
        'xǁDateSequenceRotatingHandlerǁ__init____mutmut_19': xǁDateSequenceRotatingHandlerǁ__init____mutmut_19, 
        'xǁDateSequenceRotatingHandlerǁ__init____mutmut_20': xǁDateSequenceRotatingHandlerǁ__init____mutmut_20, 
        'xǁDateSequenceRotatingHandlerǁ__init____mutmut_21': xǁDateSequenceRotatingHandlerǁ__init____mutmut_21, 
        'xǁDateSequenceRotatingHandlerǁ__init____mutmut_22': xǁDateSequenceRotatingHandlerǁ__init____mutmut_22, 
        'xǁDateSequenceRotatingHandlerǁ__init____mutmut_23': xǁDateSequenceRotatingHandlerǁ__init____mutmut_23, 
        'xǁDateSequenceRotatingHandlerǁ__init____mutmut_24': xǁDateSequenceRotatingHandlerǁ__init____mutmut_24, 
        'xǁDateSequenceRotatingHandlerǁ__init____mutmut_25': xǁDateSequenceRotatingHandlerǁ__init____mutmut_25
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁDateSequenceRotatingHandlerǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁDateSequenceRotatingHandlerǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁDateSequenceRotatingHandlerǁ__init____mutmut_orig)
    xǁDateSequenceRotatingHandlerǁ__init____mutmut_orig.__name__ = 'xǁDateSequenceRotatingHandlerǁ__init__'

    def xǁDateSequenceRotatingHandlerǁ_get_log_filename__mutmut_orig(self) -> Path:
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

    def xǁDateSequenceRotatingHandlerǁ_get_log_filename__mutmut_1(self) -> Path:
        """
        Get log filename for current date with next available sequence number

        Returns:
            Path to log file (e.g., /logs/app-2025-01-03-1.log)
        """
        date_str = None
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

    def xǁDateSequenceRotatingHandlerǁ_get_log_filename__mutmut_2(self) -> Path:
        """
        Get log filename for current date with next available sequence number

        Returns:
            Path to log file (e.g., /logs/app-2025-01-03-1.log)
        """
        date_str = self.current_date.strftime(None)
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

    def xǁDateSequenceRotatingHandlerǁ_get_log_filename__mutmut_3(self) -> Path:
        """
        Get log filename for current date with next available sequence number

        Returns:
            Path to log file (e.g., /logs/app-2025-01-03-1.log)
        """
        date_str = self.current_date.strftime('XX%Y-%m-%dXX')
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

    def xǁDateSequenceRotatingHandlerǁ_get_log_filename__mutmut_4(self) -> Path:
        """
        Get log filename for current date with next available sequence number

        Returns:
            Path to log file (e.g., /logs/app-2025-01-03-1.log)
        """
        date_str = self.current_date.strftime('%y-%m-%d')
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

    def xǁDateSequenceRotatingHandlerǁ_get_log_filename__mutmut_5(self) -> Path:
        """
        Get log filename for current date with next available sequence number

        Returns:
            Path to log file (e.g., /logs/app-2025-01-03-1.log)
        """
        date_str = self.current_date.strftime('%Y-%M-%D')
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

    def xǁDateSequenceRotatingHandlerǁ_get_log_filename__mutmut_6(self) -> Path:
        """
        Get log filename for current date with next available sequence number

        Returns:
            Path to log file (e.g., /logs/app-2025-01-03-1.log)
        """
        date_str = self.current_date.strftime('%Y-%m-%d')
        pattern = None
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

    def xǁDateSequenceRotatingHandlerǁ_get_log_filename__mutmut_7(self) -> Path:
        """
        Get log filename for current date with next available sequence number

        Returns:
            Path to log file (e.g., /logs/app-2025-01-03-1.log)
        """
        date_str = self.current_date.strftime('%Y-%m-%d')
        pattern = f"app-{date_str}-*.log"
        existing_files = None

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

    def xǁDateSequenceRotatingHandlerǁ_get_log_filename__mutmut_8(self) -> Path:
        """
        Get log filename for current date with next available sequence number

        Returns:
            Path to log file (e.g., /logs/app-2025-01-03-1.log)
        """
        date_str = self.current_date.strftime('%Y-%m-%d')
        pattern = f"app-{date_str}-*.log"
        existing_files = sorted(None)

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

    def xǁDateSequenceRotatingHandlerǁ_get_log_filename__mutmut_9(self) -> Path:
        """
        Get log filename for current date with next available sequence number

        Returns:
            Path to log file (e.g., /logs/app-2025-01-03-1.log)
        """
        date_str = self.current_date.strftime('%Y-%m-%d')
        pattern = f"app-{date_str}-*.log"
        existing_files = sorted(self.log_dir.glob(None))

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

    def xǁDateSequenceRotatingHandlerǁ_get_log_filename__mutmut_10(self) -> Path:
        """
        Get log filename for current date with next available sequence number

        Returns:
            Path to log file (e.g., /logs/app-2025-01-03-1.log)
        """
        date_str = self.current_date.strftime('%Y-%m-%d')
        pattern = f"app-{date_str}-*.log"
        existing_files = sorted(self.log_dir.glob(pattern))

        if existing_files:
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

    def xǁDateSequenceRotatingHandlerǁ_get_log_filename__mutmut_11(self) -> Path:
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
            sequence = None
        else:
            # Get highest sequence number
            last_file = existing_files[-1].stem  # e.g., "app-2025-01-03-2"
            try:
                last_sequence = int(last_file.split('-')[-1])
                sequence = last_sequence + 1
            except (ValueError, IndexError):
                sequence = 1

        return self.log_dir / f"app-{date_str}-{sequence}.log"

    def xǁDateSequenceRotatingHandlerǁ_get_log_filename__mutmut_12(self) -> Path:
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
            sequence = 2
        else:
            # Get highest sequence number
            last_file = existing_files[-1].stem  # e.g., "app-2025-01-03-2"
            try:
                last_sequence = int(last_file.split('-')[-1])
                sequence = last_sequence + 1
            except (ValueError, IndexError):
                sequence = 1

        return self.log_dir / f"app-{date_str}-{sequence}.log"

    def xǁDateSequenceRotatingHandlerǁ_get_log_filename__mutmut_13(self) -> Path:
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
            last_file = None  # e.g., "app-2025-01-03-2"
            try:
                last_sequence = int(last_file.split('-')[-1])
                sequence = last_sequence + 1
            except (ValueError, IndexError):
                sequence = 1

        return self.log_dir / f"app-{date_str}-{sequence}.log"

    def xǁDateSequenceRotatingHandlerǁ_get_log_filename__mutmut_14(self) -> Path:
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
            last_file = existing_files[+1].stem  # e.g., "app-2025-01-03-2"
            try:
                last_sequence = int(last_file.split('-')[-1])
                sequence = last_sequence + 1
            except (ValueError, IndexError):
                sequence = 1

        return self.log_dir / f"app-{date_str}-{sequence}.log"

    def xǁDateSequenceRotatingHandlerǁ_get_log_filename__mutmut_15(self) -> Path:
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
            last_file = existing_files[-2].stem  # e.g., "app-2025-01-03-2"
            try:
                last_sequence = int(last_file.split('-')[-1])
                sequence = last_sequence + 1
            except (ValueError, IndexError):
                sequence = 1

        return self.log_dir / f"app-{date_str}-{sequence}.log"

    def xǁDateSequenceRotatingHandlerǁ_get_log_filename__mutmut_16(self) -> Path:
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
                last_sequence = None
                sequence = last_sequence + 1
            except (ValueError, IndexError):
                sequence = 1

        return self.log_dir / f"app-{date_str}-{sequence}.log"

    def xǁDateSequenceRotatingHandlerǁ_get_log_filename__mutmut_17(self) -> Path:
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
                last_sequence = int(None)
                sequence = last_sequence + 1
            except (ValueError, IndexError):
                sequence = 1

        return self.log_dir / f"app-{date_str}-{sequence}.log"

    def xǁDateSequenceRotatingHandlerǁ_get_log_filename__mutmut_18(self) -> Path:
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
                last_sequence = int(last_file.split(None)[-1])
                sequence = last_sequence + 1
            except (ValueError, IndexError):
                sequence = 1

        return self.log_dir / f"app-{date_str}-{sequence}.log"

    def xǁDateSequenceRotatingHandlerǁ_get_log_filename__mutmut_19(self) -> Path:
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
                last_sequence = int(last_file.split('XX-XX')[-1])
                sequence = last_sequence + 1
            except (ValueError, IndexError):
                sequence = 1

        return self.log_dir / f"app-{date_str}-{sequence}.log"

    def xǁDateSequenceRotatingHandlerǁ_get_log_filename__mutmut_20(self) -> Path:
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
                last_sequence = int(last_file.split('-')[+1])
                sequence = last_sequence + 1
            except (ValueError, IndexError):
                sequence = 1

        return self.log_dir / f"app-{date_str}-{sequence}.log"

    def xǁDateSequenceRotatingHandlerǁ_get_log_filename__mutmut_21(self) -> Path:
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
                last_sequence = int(last_file.split('-')[-2])
                sequence = last_sequence + 1
            except (ValueError, IndexError):
                sequence = 1

        return self.log_dir / f"app-{date_str}-{sequence}.log"

    def xǁDateSequenceRotatingHandlerǁ_get_log_filename__mutmut_22(self) -> Path:
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
                sequence = None
            except (ValueError, IndexError):
                sequence = 1

        return self.log_dir / f"app-{date_str}-{sequence}.log"

    def xǁDateSequenceRotatingHandlerǁ_get_log_filename__mutmut_23(self) -> Path:
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
                sequence = last_sequence - 1
            except (ValueError, IndexError):
                sequence = 1

        return self.log_dir / f"app-{date_str}-{sequence}.log"

    def xǁDateSequenceRotatingHandlerǁ_get_log_filename__mutmut_24(self) -> Path:
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
                sequence = last_sequence + 2
            except (ValueError, IndexError):
                sequence = 1

        return self.log_dir / f"app-{date_str}-{sequence}.log"

    def xǁDateSequenceRotatingHandlerǁ_get_log_filename__mutmut_25(self) -> Path:
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
                sequence = None

        return self.log_dir / f"app-{date_str}-{sequence}.log"

    def xǁDateSequenceRotatingHandlerǁ_get_log_filename__mutmut_26(self) -> Path:
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
                sequence = 2

        return self.log_dir / f"app-{date_str}-{sequence}.log"

    def xǁDateSequenceRotatingHandlerǁ_get_log_filename__mutmut_27(self) -> Path:
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

        return self.log_dir * f"app-{date_str}-{sequence}.log"
    
    xǁDateSequenceRotatingHandlerǁ_get_log_filename__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁDateSequenceRotatingHandlerǁ_get_log_filename__mutmut_1': xǁDateSequenceRotatingHandlerǁ_get_log_filename__mutmut_1, 
        'xǁDateSequenceRotatingHandlerǁ_get_log_filename__mutmut_2': xǁDateSequenceRotatingHandlerǁ_get_log_filename__mutmut_2, 
        'xǁDateSequenceRotatingHandlerǁ_get_log_filename__mutmut_3': xǁDateSequenceRotatingHandlerǁ_get_log_filename__mutmut_3, 
        'xǁDateSequenceRotatingHandlerǁ_get_log_filename__mutmut_4': xǁDateSequenceRotatingHandlerǁ_get_log_filename__mutmut_4, 
        'xǁDateSequenceRotatingHandlerǁ_get_log_filename__mutmut_5': xǁDateSequenceRotatingHandlerǁ_get_log_filename__mutmut_5, 
        'xǁDateSequenceRotatingHandlerǁ_get_log_filename__mutmut_6': xǁDateSequenceRotatingHandlerǁ_get_log_filename__mutmut_6, 
        'xǁDateSequenceRotatingHandlerǁ_get_log_filename__mutmut_7': xǁDateSequenceRotatingHandlerǁ_get_log_filename__mutmut_7, 
        'xǁDateSequenceRotatingHandlerǁ_get_log_filename__mutmut_8': xǁDateSequenceRotatingHandlerǁ_get_log_filename__mutmut_8, 
        'xǁDateSequenceRotatingHandlerǁ_get_log_filename__mutmut_9': xǁDateSequenceRotatingHandlerǁ_get_log_filename__mutmut_9, 
        'xǁDateSequenceRotatingHandlerǁ_get_log_filename__mutmut_10': xǁDateSequenceRotatingHandlerǁ_get_log_filename__mutmut_10, 
        'xǁDateSequenceRotatingHandlerǁ_get_log_filename__mutmut_11': xǁDateSequenceRotatingHandlerǁ_get_log_filename__mutmut_11, 
        'xǁDateSequenceRotatingHandlerǁ_get_log_filename__mutmut_12': xǁDateSequenceRotatingHandlerǁ_get_log_filename__mutmut_12, 
        'xǁDateSequenceRotatingHandlerǁ_get_log_filename__mutmut_13': xǁDateSequenceRotatingHandlerǁ_get_log_filename__mutmut_13, 
        'xǁDateSequenceRotatingHandlerǁ_get_log_filename__mutmut_14': xǁDateSequenceRotatingHandlerǁ_get_log_filename__mutmut_14, 
        'xǁDateSequenceRotatingHandlerǁ_get_log_filename__mutmut_15': xǁDateSequenceRotatingHandlerǁ_get_log_filename__mutmut_15, 
        'xǁDateSequenceRotatingHandlerǁ_get_log_filename__mutmut_16': xǁDateSequenceRotatingHandlerǁ_get_log_filename__mutmut_16, 
        'xǁDateSequenceRotatingHandlerǁ_get_log_filename__mutmut_17': xǁDateSequenceRotatingHandlerǁ_get_log_filename__mutmut_17, 
        'xǁDateSequenceRotatingHandlerǁ_get_log_filename__mutmut_18': xǁDateSequenceRotatingHandlerǁ_get_log_filename__mutmut_18, 
        'xǁDateSequenceRotatingHandlerǁ_get_log_filename__mutmut_19': xǁDateSequenceRotatingHandlerǁ_get_log_filename__mutmut_19, 
        'xǁDateSequenceRotatingHandlerǁ_get_log_filename__mutmut_20': xǁDateSequenceRotatingHandlerǁ_get_log_filename__mutmut_20, 
        'xǁDateSequenceRotatingHandlerǁ_get_log_filename__mutmut_21': xǁDateSequenceRotatingHandlerǁ_get_log_filename__mutmut_21, 
        'xǁDateSequenceRotatingHandlerǁ_get_log_filename__mutmut_22': xǁDateSequenceRotatingHandlerǁ_get_log_filename__mutmut_22, 
        'xǁDateSequenceRotatingHandlerǁ_get_log_filename__mutmut_23': xǁDateSequenceRotatingHandlerǁ_get_log_filename__mutmut_23, 
        'xǁDateSequenceRotatingHandlerǁ_get_log_filename__mutmut_24': xǁDateSequenceRotatingHandlerǁ_get_log_filename__mutmut_24, 
        'xǁDateSequenceRotatingHandlerǁ_get_log_filename__mutmut_25': xǁDateSequenceRotatingHandlerǁ_get_log_filename__mutmut_25, 
        'xǁDateSequenceRotatingHandlerǁ_get_log_filename__mutmut_26': xǁDateSequenceRotatingHandlerǁ_get_log_filename__mutmut_26, 
        'xǁDateSequenceRotatingHandlerǁ_get_log_filename__mutmut_27': xǁDateSequenceRotatingHandlerǁ_get_log_filename__mutmut_27
    }
    
    def _get_log_filename(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁDateSequenceRotatingHandlerǁ_get_log_filename__mutmut_orig"), object.__getattribute__(self, "xǁDateSequenceRotatingHandlerǁ_get_log_filename__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _get_log_filename.__signature__ = _mutmut_signature(xǁDateSequenceRotatingHandlerǁ_get_log_filename__mutmut_orig)
    xǁDateSequenceRotatingHandlerǁ_get_log_filename__mutmut_orig.__name__ = 'xǁDateSequenceRotatingHandlerǁ_get_log_filename'

    def xǁDateSequenceRotatingHandlerǁshouldRollover__mutmut_orig(self, record) -> bool:
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

    def xǁDateSequenceRotatingHandlerǁshouldRollover__mutmut_1(self, record) -> bool:
        """
        Determine if rollover should occur

        Checks two conditions:
        1. Current date has changed (midnight UTC passed)
        2. File size exceeds maxBytes

        Returns:
            True if rollover needed
        """
        # Check if date has changed
        current_date = None
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

    def xǁDateSequenceRotatingHandlerǁshouldRollover__mutmut_2(self, record) -> bool:
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
        if current_date == self.current_date:
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

    def xǁDateSequenceRotatingHandlerǁshouldRollover__mutmut_3(self, record) -> bool:
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
            self.current_date = None
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

    def xǁDateSequenceRotatingHandlerǁshouldRollover__mutmut_4(self, record) -> bool:
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
            return False

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

    def xǁDateSequenceRotatingHandlerǁshouldRollover__mutmut_5(self, record) -> bool:
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
        if self.maxBytes >= 0:
            # Format the record to get accurate size
            msg = self.format(record)
            msg_size = len(msg.encode('utf-8')) + 1  # +1 for newline

            # Get current file size
            if self.stream:
                self.stream.seek(0, 2)  # Seek to end
                if self.stream.tell() + msg_size >= self.maxBytes:
                    return True

        return False

    def xǁDateSequenceRotatingHandlerǁshouldRollover__mutmut_6(self, record) -> bool:
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
        if self.maxBytes > 1:
            # Format the record to get accurate size
            msg = self.format(record)
            msg_size = len(msg.encode('utf-8')) + 1  # +1 for newline

            # Get current file size
            if self.stream:
                self.stream.seek(0, 2)  # Seek to end
                if self.stream.tell() + msg_size >= self.maxBytes:
                    return True

        return False

    def xǁDateSequenceRotatingHandlerǁshouldRollover__mutmut_7(self, record) -> bool:
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
            msg = None
            msg_size = len(msg.encode('utf-8')) + 1  # +1 for newline

            # Get current file size
            if self.stream:
                self.stream.seek(0, 2)  # Seek to end
                if self.stream.tell() + msg_size >= self.maxBytes:
                    return True

        return False

    def xǁDateSequenceRotatingHandlerǁshouldRollover__mutmut_8(self, record) -> bool:
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
            msg = self.format(None)
            msg_size = len(msg.encode('utf-8')) + 1  # +1 for newline

            # Get current file size
            if self.stream:
                self.stream.seek(0, 2)  # Seek to end
                if self.stream.tell() + msg_size >= self.maxBytes:
                    return True

        return False

    def xǁDateSequenceRotatingHandlerǁshouldRollover__mutmut_9(self, record) -> bool:
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
            msg_size = None  # +1 for newline

            # Get current file size
            if self.stream:
                self.stream.seek(0, 2)  # Seek to end
                if self.stream.tell() + msg_size >= self.maxBytes:
                    return True

        return False

    def xǁDateSequenceRotatingHandlerǁshouldRollover__mutmut_10(self, record) -> bool:
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
            msg_size = len(msg.encode('utf-8')) - 1  # +1 for newline

            # Get current file size
            if self.stream:
                self.stream.seek(0, 2)  # Seek to end
                if self.stream.tell() + msg_size >= self.maxBytes:
                    return True

        return False

    def xǁDateSequenceRotatingHandlerǁshouldRollover__mutmut_11(self, record) -> bool:
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
            msg_size = len(msg.encode('utf-8')) + 2  # +1 for newline

            # Get current file size
            if self.stream:
                self.stream.seek(0, 2)  # Seek to end
                if self.stream.tell() + msg_size >= self.maxBytes:
                    return True

        return False

    def xǁDateSequenceRotatingHandlerǁshouldRollover__mutmut_12(self, record) -> bool:
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
                self.stream.seek(None, 2)  # Seek to end
                if self.stream.tell() + msg_size >= self.maxBytes:
                    return True

        return False

    def xǁDateSequenceRotatingHandlerǁshouldRollover__mutmut_13(self, record) -> bool:
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
                self.stream.seek(0, None)  # Seek to end
                if self.stream.tell() + msg_size >= self.maxBytes:
                    return True

        return False

    def xǁDateSequenceRotatingHandlerǁshouldRollover__mutmut_14(self, record) -> bool:
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
                self.stream.seek(2)  # Seek to end
                if self.stream.tell() + msg_size >= self.maxBytes:
                    return True

        return False

    def xǁDateSequenceRotatingHandlerǁshouldRollover__mutmut_15(self, record) -> bool:
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
                self.stream.seek(0, )  # Seek to end
                if self.stream.tell() + msg_size >= self.maxBytes:
                    return True

        return False

    def xǁDateSequenceRotatingHandlerǁshouldRollover__mutmut_16(self, record) -> bool:
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
                self.stream.seek(1, 2)  # Seek to end
                if self.stream.tell() + msg_size >= self.maxBytes:
                    return True

        return False

    def xǁDateSequenceRotatingHandlerǁshouldRollover__mutmut_17(self, record) -> bool:
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
                self.stream.seek(0, 3)  # Seek to end
                if self.stream.tell() + msg_size >= self.maxBytes:
                    return True

        return False

    def xǁDateSequenceRotatingHandlerǁshouldRollover__mutmut_18(self, record) -> bool:
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
                if self.stream.tell() - msg_size >= self.maxBytes:
                    return True

        return False

    def xǁDateSequenceRotatingHandlerǁshouldRollover__mutmut_19(self, record) -> bool:
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
                if self.stream.tell() + msg_size > self.maxBytes:
                    return True

        return False

    def xǁDateSequenceRotatingHandlerǁshouldRollover__mutmut_20(self, record) -> bool:
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
                    return False

        return False

    def xǁDateSequenceRotatingHandlerǁshouldRollover__mutmut_21(self, record) -> bool:
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

        return True
    
    xǁDateSequenceRotatingHandlerǁshouldRollover__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁDateSequenceRotatingHandlerǁshouldRollover__mutmut_1': xǁDateSequenceRotatingHandlerǁshouldRollover__mutmut_1, 
        'xǁDateSequenceRotatingHandlerǁshouldRollover__mutmut_2': xǁDateSequenceRotatingHandlerǁshouldRollover__mutmut_2, 
        'xǁDateSequenceRotatingHandlerǁshouldRollover__mutmut_3': xǁDateSequenceRotatingHandlerǁshouldRollover__mutmut_3, 
        'xǁDateSequenceRotatingHandlerǁshouldRollover__mutmut_4': xǁDateSequenceRotatingHandlerǁshouldRollover__mutmut_4, 
        'xǁDateSequenceRotatingHandlerǁshouldRollover__mutmut_5': xǁDateSequenceRotatingHandlerǁshouldRollover__mutmut_5, 
        'xǁDateSequenceRotatingHandlerǁshouldRollover__mutmut_6': xǁDateSequenceRotatingHandlerǁshouldRollover__mutmut_6, 
        'xǁDateSequenceRotatingHandlerǁshouldRollover__mutmut_7': xǁDateSequenceRotatingHandlerǁshouldRollover__mutmut_7, 
        'xǁDateSequenceRotatingHandlerǁshouldRollover__mutmut_8': xǁDateSequenceRotatingHandlerǁshouldRollover__mutmut_8, 
        'xǁDateSequenceRotatingHandlerǁshouldRollover__mutmut_9': xǁDateSequenceRotatingHandlerǁshouldRollover__mutmut_9, 
        'xǁDateSequenceRotatingHandlerǁshouldRollover__mutmut_10': xǁDateSequenceRotatingHandlerǁshouldRollover__mutmut_10, 
        'xǁDateSequenceRotatingHandlerǁshouldRollover__mutmut_11': xǁDateSequenceRotatingHandlerǁshouldRollover__mutmut_11, 
        'xǁDateSequenceRotatingHandlerǁshouldRollover__mutmut_12': xǁDateSequenceRotatingHandlerǁshouldRollover__mutmut_12, 
        'xǁDateSequenceRotatingHandlerǁshouldRollover__mutmut_13': xǁDateSequenceRotatingHandlerǁshouldRollover__mutmut_13, 
        'xǁDateSequenceRotatingHandlerǁshouldRollover__mutmut_14': xǁDateSequenceRotatingHandlerǁshouldRollover__mutmut_14, 
        'xǁDateSequenceRotatingHandlerǁshouldRollover__mutmut_15': xǁDateSequenceRotatingHandlerǁshouldRollover__mutmut_15, 
        'xǁDateSequenceRotatingHandlerǁshouldRollover__mutmut_16': xǁDateSequenceRotatingHandlerǁshouldRollover__mutmut_16, 
        'xǁDateSequenceRotatingHandlerǁshouldRollover__mutmut_17': xǁDateSequenceRotatingHandlerǁshouldRollover__mutmut_17, 
        'xǁDateSequenceRotatingHandlerǁshouldRollover__mutmut_18': xǁDateSequenceRotatingHandlerǁshouldRollover__mutmut_18, 
        'xǁDateSequenceRotatingHandlerǁshouldRollover__mutmut_19': xǁDateSequenceRotatingHandlerǁshouldRollover__mutmut_19, 
        'xǁDateSequenceRotatingHandlerǁshouldRollover__mutmut_20': xǁDateSequenceRotatingHandlerǁshouldRollover__mutmut_20, 
        'xǁDateSequenceRotatingHandlerǁshouldRollover__mutmut_21': xǁDateSequenceRotatingHandlerǁshouldRollover__mutmut_21
    }
    
    def shouldRollover(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁDateSequenceRotatingHandlerǁshouldRollover__mutmut_orig"), object.__getattribute__(self, "xǁDateSequenceRotatingHandlerǁshouldRollover__mutmut_mutants"), args, kwargs, self)
        return result 
    
    shouldRollover.__signature__ = _mutmut_signature(xǁDateSequenceRotatingHandlerǁshouldRollover__mutmut_orig)
    xǁDateSequenceRotatingHandlerǁshouldRollover__mutmut_orig.__name__ = 'xǁDateSequenceRotatingHandlerǁshouldRollover'

    def xǁDateSequenceRotatingHandlerǁdoRollover__mutmut_orig(self):
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

    def xǁDateSequenceRotatingHandlerǁdoRollover__mutmut_1(self):
        """
        Perform log file rollover

        Creates new log file with incremented sequence number or new date.
        Cleans up old log files exceeding retention period.
        """
        # Close current stream
        if self.stream:
            self.stream.close()
            self.stream = ""

        # Get new filename (sequence will auto-increment or reset for new date)
        new_filename = self._get_log_filename()
        self.baseFilename = str(new_filename)

        # Open new file
        self.stream = self._open()

        # Clean up old log files
        self._cleanup_old_logs()

    def xǁDateSequenceRotatingHandlerǁdoRollover__mutmut_2(self):
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
        new_filename = None
        self.baseFilename = str(new_filename)

        # Open new file
        self.stream = self._open()

        # Clean up old log files
        self._cleanup_old_logs()

    def xǁDateSequenceRotatingHandlerǁdoRollover__mutmut_3(self):
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
        self.baseFilename = None

        # Open new file
        self.stream = self._open()

        # Clean up old log files
        self._cleanup_old_logs()

    def xǁDateSequenceRotatingHandlerǁdoRollover__mutmut_4(self):
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
        self.baseFilename = str(None)

        # Open new file
        self.stream = self._open()

        # Clean up old log files
        self._cleanup_old_logs()

    def xǁDateSequenceRotatingHandlerǁdoRollover__mutmut_5(self):
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
        self.stream = None

        # Clean up old log files
        self._cleanup_old_logs()
    
    xǁDateSequenceRotatingHandlerǁdoRollover__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁDateSequenceRotatingHandlerǁdoRollover__mutmut_1': xǁDateSequenceRotatingHandlerǁdoRollover__mutmut_1, 
        'xǁDateSequenceRotatingHandlerǁdoRollover__mutmut_2': xǁDateSequenceRotatingHandlerǁdoRollover__mutmut_2, 
        'xǁDateSequenceRotatingHandlerǁdoRollover__mutmut_3': xǁDateSequenceRotatingHandlerǁdoRollover__mutmut_3, 
        'xǁDateSequenceRotatingHandlerǁdoRollover__mutmut_4': xǁDateSequenceRotatingHandlerǁdoRollover__mutmut_4, 
        'xǁDateSequenceRotatingHandlerǁdoRollover__mutmut_5': xǁDateSequenceRotatingHandlerǁdoRollover__mutmut_5
    }
    
    def doRollover(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁDateSequenceRotatingHandlerǁdoRollover__mutmut_orig"), object.__getattribute__(self, "xǁDateSequenceRotatingHandlerǁdoRollover__mutmut_mutants"), args, kwargs, self)
        return result 
    
    doRollover.__signature__ = _mutmut_signature(xǁDateSequenceRotatingHandlerǁdoRollover__mutmut_orig)
    xǁDateSequenceRotatingHandlerǁdoRollover__mutmut_orig.__name__ = 'xǁDateSequenceRotatingHandlerǁdoRollover'

    def xǁDateSequenceRotatingHandlerǁ_cleanup_old_logs__mutmut_orig(self):
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

    def xǁDateSequenceRotatingHandlerǁ_cleanup_old_logs__mutmut_1(self):
        """
        Delete log files older than retention_days

        T172e: Log retention cleanup
        """
        # Skip cleanup if retention disabled
        if self.retention_days < 0:
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

    def xǁDateSequenceRotatingHandlerǁ_cleanup_old_logs__mutmut_2(self):
        """
        Delete log files older than retention_days

        T172e: Log retention cleanup
        """
        # Skip cleanup if retention disabled
        if self.retention_days <= 1:
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

    def xǁDateSequenceRotatingHandlerǁ_cleanup_old_logs__mutmut_3(self):
        """
        Delete log files older than retention_days

        T172e: Log retention cleanup
        """
        # Skip cleanup if retention disabled
        if self.retention_days <= 0:
            return

        cutoff_date = None
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

    def xǁDateSequenceRotatingHandlerǁ_cleanup_old_logs__mutmut_4(self):
        """
        Delete log files older than retention_days

        T172e: Log retention cleanup
        """
        # Skip cleanup if retention disabled
        if self.retention_days <= 0:
            return

        cutoff_date = datetime.utcnow().date() + timedelta(days=self.retention_days)
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

    def xǁDateSequenceRotatingHandlerǁ_cleanup_old_logs__mutmut_5(self):
        """
        Delete log files older than retention_days

        T172e: Log retention cleanup
        """
        # Skip cleanup if retention disabled
        if self.retention_days <= 0:
            return

        cutoff_date = datetime.utcnow().date() - timedelta(days=None)
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

    def xǁDateSequenceRotatingHandlerǁ_cleanup_old_logs__mutmut_6(self):
        """
        Delete log files older than retention_days

        T172e: Log retention cleanup
        """
        # Skip cleanup if retention disabled
        if self.retention_days <= 0:
            return

        cutoff_date = datetime.utcnow().date() - timedelta(days=self.retention_days)
        pattern = None

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

    def xǁDateSequenceRotatingHandlerǁ_cleanup_old_logs__mutmut_7(self):
        """
        Delete log files older than retention_days

        T172e: Log retention cleanup
        """
        # Skip cleanup if retention disabled
        if self.retention_days <= 0:
            return

        cutoff_date = datetime.utcnow().date() - timedelta(days=self.retention_days)
        pattern = "XXapp-*.logXX"

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

    def xǁDateSequenceRotatingHandlerǁ_cleanup_old_logs__mutmut_8(self):
        """
        Delete log files older than retention_days

        T172e: Log retention cleanup
        """
        # Skip cleanup if retention disabled
        if self.retention_days <= 0:
            return

        cutoff_date = datetime.utcnow().date() - timedelta(days=self.retention_days)
        pattern = "APP-*.LOG"

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

    def xǁDateSequenceRotatingHandlerǁ_cleanup_old_logs__mutmut_9(self):
        """
        Delete log files older than retention_days

        T172e: Log retention cleanup
        """
        # Skip cleanup if retention disabled
        if self.retention_days <= 0:
            return

        cutoff_date = datetime.utcnow().date() - timedelta(days=self.retention_days)
        pattern = "app-*.log"

        for log_file in self.log_dir.glob(None):
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

    def xǁDateSequenceRotatingHandlerǁ_cleanup_old_logs__mutmut_10(self):
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
                parts = None
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

    def xǁDateSequenceRotatingHandlerǁ_cleanup_old_logs__mutmut_11(self):
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
                parts = log_file.stem.split(None)
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

    def xǁDateSequenceRotatingHandlerǁ_cleanup_old_logs__mutmut_12(self):
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
                parts = log_file.stem.split('XX-XX')
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

    def xǁDateSequenceRotatingHandlerǁ_cleanup_old_logs__mutmut_13(self):
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
                if len(parts) > 4:
                    # parts = ['app', 'YYYY', 'MM', 'DD', 'N']
                    file_date_str = f"{parts[1]}-{parts[2]}-{parts[3]}"
                    file_date = datetime.strptime(file_date_str, '%Y-%m-%d').date()

                    if file_date < cutoff_date:
                        log_file.unlink()
                        print(f"Deleted old log file: {log_file}")
            except (ValueError, IndexError, OSError) as e:
                # Skip files that don't match pattern or can't be deleted
                print(f"Warning: Could not process log file {log_file}: {e}")

    def xǁDateSequenceRotatingHandlerǁ_cleanup_old_logs__mutmut_14(self):
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
                if len(parts) >= 5:
                    # parts = ['app', 'YYYY', 'MM', 'DD', 'N']
                    file_date_str = f"{parts[1]}-{parts[2]}-{parts[3]}"
                    file_date = datetime.strptime(file_date_str, '%Y-%m-%d').date()

                    if file_date < cutoff_date:
                        log_file.unlink()
                        print(f"Deleted old log file: {log_file}")
            except (ValueError, IndexError, OSError) as e:
                # Skip files that don't match pattern or can't be deleted
                print(f"Warning: Could not process log file {log_file}: {e}")

    def xǁDateSequenceRotatingHandlerǁ_cleanup_old_logs__mutmut_15(self):
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
                    file_date_str = None
                    file_date = datetime.strptime(file_date_str, '%Y-%m-%d').date()

                    if file_date < cutoff_date:
                        log_file.unlink()
                        print(f"Deleted old log file: {log_file}")
            except (ValueError, IndexError, OSError) as e:
                # Skip files that don't match pattern or can't be deleted
                print(f"Warning: Could not process log file {log_file}: {e}")

    def xǁDateSequenceRotatingHandlerǁ_cleanup_old_logs__mutmut_16(self):
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
                    file_date_str = f"{parts[2]}-{parts[2]}-{parts[3]}"
                    file_date = datetime.strptime(file_date_str, '%Y-%m-%d').date()

                    if file_date < cutoff_date:
                        log_file.unlink()
                        print(f"Deleted old log file: {log_file}")
            except (ValueError, IndexError, OSError) as e:
                # Skip files that don't match pattern or can't be deleted
                print(f"Warning: Could not process log file {log_file}: {e}")

    def xǁDateSequenceRotatingHandlerǁ_cleanup_old_logs__mutmut_17(self):
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
                    file_date_str = f"{parts[1]}-{parts[3]}-{parts[3]}"
                    file_date = datetime.strptime(file_date_str, '%Y-%m-%d').date()

                    if file_date < cutoff_date:
                        log_file.unlink()
                        print(f"Deleted old log file: {log_file}")
            except (ValueError, IndexError, OSError) as e:
                # Skip files that don't match pattern or can't be deleted
                print(f"Warning: Could not process log file {log_file}: {e}")

    def xǁDateSequenceRotatingHandlerǁ_cleanup_old_logs__mutmut_18(self):
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
                    file_date_str = f"{parts[1]}-{parts[2]}-{parts[4]}"
                    file_date = datetime.strptime(file_date_str, '%Y-%m-%d').date()

                    if file_date < cutoff_date:
                        log_file.unlink()
                        print(f"Deleted old log file: {log_file}")
            except (ValueError, IndexError, OSError) as e:
                # Skip files that don't match pattern or can't be deleted
                print(f"Warning: Could not process log file {log_file}: {e}")

    def xǁDateSequenceRotatingHandlerǁ_cleanup_old_logs__mutmut_19(self):
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
                    file_date = None

                    if file_date < cutoff_date:
                        log_file.unlink()
                        print(f"Deleted old log file: {log_file}")
            except (ValueError, IndexError, OSError) as e:
                # Skip files that don't match pattern or can't be deleted
                print(f"Warning: Could not process log file {log_file}: {e}")

    def xǁDateSequenceRotatingHandlerǁ_cleanup_old_logs__mutmut_20(self):
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
                    file_date = datetime.strptime(None, '%Y-%m-%d').date()

                    if file_date < cutoff_date:
                        log_file.unlink()
                        print(f"Deleted old log file: {log_file}")
            except (ValueError, IndexError, OSError) as e:
                # Skip files that don't match pattern or can't be deleted
                print(f"Warning: Could not process log file {log_file}: {e}")

    def xǁDateSequenceRotatingHandlerǁ_cleanup_old_logs__mutmut_21(self):
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
                    file_date = datetime.strptime(file_date_str, None).date()

                    if file_date < cutoff_date:
                        log_file.unlink()
                        print(f"Deleted old log file: {log_file}")
            except (ValueError, IndexError, OSError) as e:
                # Skip files that don't match pattern or can't be deleted
                print(f"Warning: Could not process log file {log_file}: {e}")

    def xǁDateSequenceRotatingHandlerǁ_cleanup_old_logs__mutmut_22(self):
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
                    file_date = datetime.strptime('%Y-%m-%d').date()

                    if file_date < cutoff_date:
                        log_file.unlink()
                        print(f"Deleted old log file: {log_file}")
            except (ValueError, IndexError, OSError) as e:
                # Skip files that don't match pattern or can't be deleted
                print(f"Warning: Could not process log file {log_file}: {e}")

    def xǁDateSequenceRotatingHandlerǁ_cleanup_old_logs__mutmut_23(self):
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
                    file_date = datetime.strptime(file_date_str, ).date()

                    if file_date < cutoff_date:
                        log_file.unlink()
                        print(f"Deleted old log file: {log_file}")
            except (ValueError, IndexError, OSError) as e:
                # Skip files that don't match pattern or can't be deleted
                print(f"Warning: Could not process log file {log_file}: {e}")

    def xǁDateSequenceRotatingHandlerǁ_cleanup_old_logs__mutmut_24(self):
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
                    file_date = datetime.strptime(file_date_str, 'XX%Y-%m-%dXX').date()

                    if file_date < cutoff_date:
                        log_file.unlink()
                        print(f"Deleted old log file: {log_file}")
            except (ValueError, IndexError, OSError) as e:
                # Skip files that don't match pattern or can't be deleted
                print(f"Warning: Could not process log file {log_file}: {e}")

    def xǁDateSequenceRotatingHandlerǁ_cleanup_old_logs__mutmut_25(self):
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
                    file_date = datetime.strptime(file_date_str, '%y-%m-%d').date()

                    if file_date < cutoff_date:
                        log_file.unlink()
                        print(f"Deleted old log file: {log_file}")
            except (ValueError, IndexError, OSError) as e:
                # Skip files that don't match pattern or can't be deleted
                print(f"Warning: Could not process log file {log_file}: {e}")

    def xǁDateSequenceRotatingHandlerǁ_cleanup_old_logs__mutmut_26(self):
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
                    file_date = datetime.strptime(file_date_str, '%Y-%M-%D').date()

                    if file_date < cutoff_date:
                        log_file.unlink()
                        print(f"Deleted old log file: {log_file}")
            except (ValueError, IndexError, OSError) as e:
                # Skip files that don't match pattern or can't be deleted
                print(f"Warning: Could not process log file {log_file}: {e}")

    def xǁDateSequenceRotatingHandlerǁ_cleanup_old_logs__mutmut_27(self):
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

                    if file_date <= cutoff_date:
                        log_file.unlink()
                        print(f"Deleted old log file: {log_file}")
            except (ValueError, IndexError, OSError) as e:
                # Skip files that don't match pattern or can't be deleted
                print(f"Warning: Could not process log file {log_file}: {e}")

    def xǁDateSequenceRotatingHandlerǁ_cleanup_old_logs__mutmut_28(self):
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
                        print(None)
            except (ValueError, IndexError, OSError) as e:
                # Skip files that don't match pattern or can't be deleted
                print(f"Warning: Could not process log file {log_file}: {e}")

    def xǁDateSequenceRotatingHandlerǁ_cleanup_old_logs__mutmut_29(self):
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
                print(None)
    
    xǁDateSequenceRotatingHandlerǁ_cleanup_old_logs__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁDateSequenceRotatingHandlerǁ_cleanup_old_logs__mutmut_1': xǁDateSequenceRotatingHandlerǁ_cleanup_old_logs__mutmut_1, 
        'xǁDateSequenceRotatingHandlerǁ_cleanup_old_logs__mutmut_2': xǁDateSequenceRotatingHandlerǁ_cleanup_old_logs__mutmut_2, 
        'xǁDateSequenceRotatingHandlerǁ_cleanup_old_logs__mutmut_3': xǁDateSequenceRotatingHandlerǁ_cleanup_old_logs__mutmut_3, 
        'xǁDateSequenceRotatingHandlerǁ_cleanup_old_logs__mutmut_4': xǁDateSequenceRotatingHandlerǁ_cleanup_old_logs__mutmut_4, 
        'xǁDateSequenceRotatingHandlerǁ_cleanup_old_logs__mutmut_5': xǁDateSequenceRotatingHandlerǁ_cleanup_old_logs__mutmut_5, 
        'xǁDateSequenceRotatingHandlerǁ_cleanup_old_logs__mutmut_6': xǁDateSequenceRotatingHandlerǁ_cleanup_old_logs__mutmut_6, 
        'xǁDateSequenceRotatingHandlerǁ_cleanup_old_logs__mutmut_7': xǁDateSequenceRotatingHandlerǁ_cleanup_old_logs__mutmut_7, 
        'xǁDateSequenceRotatingHandlerǁ_cleanup_old_logs__mutmut_8': xǁDateSequenceRotatingHandlerǁ_cleanup_old_logs__mutmut_8, 
        'xǁDateSequenceRotatingHandlerǁ_cleanup_old_logs__mutmut_9': xǁDateSequenceRotatingHandlerǁ_cleanup_old_logs__mutmut_9, 
        'xǁDateSequenceRotatingHandlerǁ_cleanup_old_logs__mutmut_10': xǁDateSequenceRotatingHandlerǁ_cleanup_old_logs__mutmut_10, 
        'xǁDateSequenceRotatingHandlerǁ_cleanup_old_logs__mutmut_11': xǁDateSequenceRotatingHandlerǁ_cleanup_old_logs__mutmut_11, 
        'xǁDateSequenceRotatingHandlerǁ_cleanup_old_logs__mutmut_12': xǁDateSequenceRotatingHandlerǁ_cleanup_old_logs__mutmut_12, 
        'xǁDateSequenceRotatingHandlerǁ_cleanup_old_logs__mutmut_13': xǁDateSequenceRotatingHandlerǁ_cleanup_old_logs__mutmut_13, 
        'xǁDateSequenceRotatingHandlerǁ_cleanup_old_logs__mutmut_14': xǁDateSequenceRotatingHandlerǁ_cleanup_old_logs__mutmut_14, 
        'xǁDateSequenceRotatingHandlerǁ_cleanup_old_logs__mutmut_15': xǁDateSequenceRotatingHandlerǁ_cleanup_old_logs__mutmut_15, 
        'xǁDateSequenceRotatingHandlerǁ_cleanup_old_logs__mutmut_16': xǁDateSequenceRotatingHandlerǁ_cleanup_old_logs__mutmut_16, 
        'xǁDateSequenceRotatingHandlerǁ_cleanup_old_logs__mutmut_17': xǁDateSequenceRotatingHandlerǁ_cleanup_old_logs__mutmut_17, 
        'xǁDateSequenceRotatingHandlerǁ_cleanup_old_logs__mutmut_18': xǁDateSequenceRotatingHandlerǁ_cleanup_old_logs__mutmut_18, 
        'xǁDateSequenceRotatingHandlerǁ_cleanup_old_logs__mutmut_19': xǁDateSequenceRotatingHandlerǁ_cleanup_old_logs__mutmut_19, 
        'xǁDateSequenceRotatingHandlerǁ_cleanup_old_logs__mutmut_20': xǁDateSequenceRotatingHandlerǁ_cleanup_old_logs__mutmut_20, 
        'xǁDateSequenceRotatingHandlerǁ_cleanup_old_logs__mutmut_21': xǁDateSequenceRotatingHandlerǁ_cleanup_old_logs__mutmut_21, 
        'xǁDateSequenceRotatingHandlerǁ_cleanup_old_logs__mutmut_22': xǁDateSequenceRotatingHandlerǁ_cleanup_old_logs__mutmut_22, 
        'xǁDateSequenceRotatingHandlerǁ_cleanup_old_logs__mutmut_23': xǁDateSequenceRotatingHandlerǁ_cleanup_old_logs__mutmut_23, 
        'xǁDateSequenceRotatingHandlerǁ_cleanup_old_logs__mutmut_24': xǁDateSequenceRotatingHandlerǁ_cleanup_old_logs__mutmut_24, 
        'xǁDateSequenceRotatingHandlerǁ_cleanup_old_logs__mutmut_25': xǁDateSequenceRotatingHandlerǁ_cleanup_old_logs__mutmut_25, 
        'xǁDateSequenceRotatingHandlerǁ_cleanup_old_logs__mutmut_26': xǁDateSequenceRotatingHandlerǁ_cleanup_old_logs__mutmut_26, 
        'xǁDateSequenceRotatingHandlerǁ_cleanup_old_logs__mutmut_27': xǁDateSequenceRotatingHandlerǁ_cleanup_old_logs__mutmut_27, 
        'xǁDateSequenceRotatingHandlerǁ_cleanup_old_logs__mutmut_28': xǁDateSequenceRotatingHandlerǁ_cleanup_old_logs__mutmut_28, 
        'xǁDateSequenceRotatingHandlerǁ_cleanup_old_logs__mutmut_29': xǁDateSequenceRotatingHandlerǁ_cleanup_old_logs__mutmut_29
    }
    
    def _cleanup_old_logs(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁDateSequenceRotatingHandlerǁ_cleanup_old_logs__mutmut_orig"), object.__getattribute__(self, "xǁDateSequenceRotatingHandlerǁ_cleanup_old_logs__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _cleanup_old_logs.__signature__ = _mutmut_signature(xǁDateSequenceRotatingHandlerǁ_cleanup_old_logs__mutmut_orig)
    xǁDateSequenceRotatingHandlerǁ_cleanup_old_logs__mutmut_orig.__name__ = 'xǁDateSequenceRotatingHandlerǁ_cleanup_old_logs'


def x_cleanup_old_logs__mutmut_orig(log_dir: str, retention_days: int):
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


def x_cleanup_old_logs__mutmut_1(log_dir: str, retention_days: int):
    """
    Standalone function to cleanup old log files

    Can be called manually or via cron for log maintenance.

    Args:
        log_dir: Directory containing log files
        retention_days: Number of days to retain logs (0 = no cleanup)

    Returns:
        Number of files deleted
    """
    log_path = None
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


def x_cleanup_old_logs__mutmut_2(log_dir: str, retention_days: int):
    """
    Standalone function to cleanup old log files

    Can be called manually or via cron for log maintenance.

    Args:
        log_dir: Directory containing log files
        retention_days: Number of days to retain logs (0 = no cleanup)

    Returns:
        Number of files deleted
    """
    log_path = Path(None)
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


def x_cleanup_old_logs__mutmut_3(log_dir: str, retention_days: int):
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
    if log_path.exists():
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


def x_cleanup_old_logs__mutmut_4(log_dir: str, retention_days: int):
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
        return 1

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


def x_cleanup_old_logs__mutmut_5(log_dir: str, retention_days: int):
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
    if retention_days < 0:
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


def x_cleanup_old_logs__mutmut_6(log_dir: str, retention_days: int):
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
    if retention_days <= 1:
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


def x_cleanup_old_logs__mutmut_7(log_dir: str, retention_days: int):
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
        return 1

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


def x_cleanup_old_logs__mutmut_8(log_dir: str, retention_days: int):
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

    cutoff_date = None
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


def x_cleanup_old_logs__mutmut_9(log_dir: str, retention_days: int):
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

    cutoff_date = datetime.utcnow().date() + timedelta(days=retention_days)
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


def x_cleanup_old_logs__mutmut_10(log_dir: str, retention_days: int):
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

    cutoff_date = datetime.utcnow().date() - timedelta(days=None)
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


def x_cleanup_old_logs__mutmut_11(log_dir: str, retention_days: int):
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
    pattern = None
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


def x_cleanup_old_logs__mutmut_12(log_dir: str, retention_days: int):
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
    pattern = "XXapp-*.logXX"
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


def x_cleanup_old_logs__mutmut_13(log_dir: str, retention_days: int):
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
    pattern = "APP-*.LOG"
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


def x_cleanup_old_logs__mutmut_14(log_dir: str, retention_days: int):
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
    deleted_count = None

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


def x_cleanup_old_logs__mutmut_15(log_dir: str, retention_days: int):
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
    deleted_count = 1

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


def x_cleanup_old_logs__mutmut_16(log_dir: str, retention_days: int):
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

    for log_file in log_path.glob(None):
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


def x_cleanup_old_logs__mutmut_17(log_dir: str, retention_days: int):
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
            parts = None
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


def x_cleanup_old_logs__mutmut_18(log_dir: str, retention_days: int):
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
            parts = log_file.stem.split(None)
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


def x_cleanup_old_logs__mutmut_19(log_dir: str, retention_days: int):
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
            parts = log_file.stem.split('XX-XX')
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


def x_cleanup_old_logs__mutmut_20(log_dir: str, retention_days: int):
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
            if len(parts) > 4:
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


def x_cleanup_old_logs__mutmut_21(log_dir: str, retention_days: int):
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
            if len(parts) >= 5:
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


def x_cleanup_old_logs__mutmut_22(log_dir: str, retention_days: int):
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
                file_date_str = None
                file_date = datetime.strptime(file_date_str, '%Y-%m-%d').date()

                if file_date < cutoff_date:
                    log_file.unlink()
                    deleted_count += 1
                    print(f"Deleted old log file: {log_file}")
        except (ValueError, IndexError, OSError) as e:
            print(f"Warning: Could not process log file {log_file}: {e}")

    print(f"Log cleanup complete: {deleted_count} files deleted")
    return deleted_count


def x_cleanup_old_logs__mutmut_23(log_dir: str, retention_days: int):
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
                file_date_str = f"{parts[2]}-{parts[2]}-{parts[3]}"
                file_date = datetime.strptime(file_date_str, '%Y-%m-%d').date()

                if file_date < cutoff_date:
                    log_file.unlink()
                    deleted_count += 1
                    print(f"Deleted old log file: {log_file}")
        except (ValueError, IndexError, OSError) as e:
            print(f"Warning: Could not process log file {log_file}: {e}")

    print(f"Log cleanup complete: {deleted_count} files deleted")
    return deleted_count


def x_cleanup_old_logs__mutmut_24(log_dir: str, retention_days: int):
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
                file_date_str = f"{parts[1]}-{parts[3]}-{parts[3]}"
                file_date = datetime.strptime(file_date_str, '%Y-%m-%d').date()

                if file_date < cutoff_date:
                    log_file.unlink()
                    deleted_count += 1
                    print(f"Deleted old log file: {log_file}")
        except (ValueError, IndexError, OSError) as e:
            print(f"Warning: Could not process log file {log_file}: {e}")

    print(f"Log cleanup complete: {deleted_count} files deleted")
    return deleted_count


def x_cleanup_old_logs__mutmut_25(log_dir: str, retention_days: int):
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
                file_date_str = f"{parts[1]}-{parts[2]}-{parts[4]}"
                file_date = datetime.strptime(file_date_str, '%Y-%m-%d').date()

                if file_date < cutoff_date:
                    log_file.unlink()
                    deleted_count += 1
                    print(f"Deleted old log file: {log_file}")
        except (ValueError, IndexError, OSError) as e:
            print(f"Warning: Could not process log file {log_file}: {e}")

    print(f"Log cleanup complete: {deleted_count} files deleted")
    return deleted_count


def x_cleanup_old_logs__mutmut_26(log_dir: str, retention_days: int):
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
                file_date = None

                if file_date < cutoff_date:
                    log_file.unlink()
                    deleted_count += 1
                    print(f"Deleted old log file: {log_file}")
        except (ValueError, IndexError, OSError) as e:
            print(f"Warning: Could not process log file {log_file}: {e}")

    print(f"Log cleanup complete: {deleted_count} files deleted")
    return deleted_count


def x_cleanup_old_logs__mutmut_27(log_dir: str, retention_days: int):
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
                file_date = datetime.strptime(None, '%Y-%m-%d').date()

                if file_date < cutoff_date:
                    log_file.unlink()
                    deleted_count += 1
                    print(f"Deleted old log file: {log_file}")
        except (ValueError, IndexError, OSError) as e:
            print(f"Warning: Could not process log file {log_file}: {e}")

    print(f"Log cleanup complete: {deleted_count} files deleted")
    return deleted_count


def x_cleanup_old_logs__mutmut_28(log_dir: str, retention_days: int):
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
                file_date = datetime.strptime(file_date_str, None).date()

                if file_date < cutoff_date:
                    log_file.unlink()
                    deleted_count += 1
                    print(f"Deleted old log file: {log_file}")
        except (ValueError, IndexError, OSError) as e:
            print(f"Warning: Could not process log file {log_file}: {e}")

    print(f"Log cleanup complete: {deleted_count} files deleted")
    return deleted_count


def x_cleanup_old_logs__mutmut_29(log_dir: str, retention_days: int):
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
                file_date = datetime.strptime('%Y-%m-%d').date()

                if file_date < cutoff_date:
                    log_file.unlink()
                    deleted_count += 1
                    print(f"Deleted old log file: {log_file}")
        except (ValueError, IndexError, OSError) as e:
            print(f"Warning: Could not process log file {log_file}: {e}")

    print(f"Log cleanup complete: {deleted_count} files deleted")
    return deleted_count


def x_cleanup_old_logs__mutmut_30(log_dir: str, retention_days: int):
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
                file_date = datetime.strptime(file_date_str, ).date()

                if file_date < cutoff_date:
                    log_file.unlink()
                    deleted_count += 1
                    print(f"Deleted old log file: {log_file}")
        except (ValueError, IndexError, OSError) as e:
            print(f"Warning: Could not process log file {log_file}: {e}")

    print(f"Log cleanup complete: {deleted_count} files deleted")
    return deleted_count


def x_cleanup_old_logs__mutmut_31(log_dir: str, retention_days: int):
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
                file_date = datetime.strptime(file_date_str, 'XX%Y-%m-%dXX').date()

                if file_date < cutoff_date:
                    log_file.unlink()
                    deleted_count += 1
                    print(f"Deleted old log file: {log_file}")
        except (ValueError, IndexError, OSError) as e:
            print(f"Warning: Could not process log file {log_file}: {e}")

    print(f"Log cleanup complete: {deleted_count} files deleted")
    return deleted_count


def x_cleanup_old_logs__mutmut_32(log_dir: str, retention_days: int):
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
                file_date = datetime.strptime(file_date_str, '%y-%m-%d').date()

                if file_date < cutoff_date:
                    log_file.unlink()
                    deleted_count += 1
                    print(f"Deleted old log file: {log_file}")
        except (ValueError, IndexError, OSError) as e:
            print(f"Warning: Could not process log file {log_file}: {e}")

    print(f"Log cleanup complete: {deleted_count} files deleted")
    return deleted_count


def x_cleanup_old_logs__mutmut_33(log_dir: str, retention_days: int):
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
                file_date = datetime.strptime(file_date_str, '%Y-%M-%D').date()

                if file_date < cutoff_date:
                    log_file.unlink()
                    deleted_count += 1
                    print(f"Deleted old log file: {log_file}")
        except (ValueError, IndexError, OSError) as e:
            print(f"Warning: Could not process log file {log_file}: {e}")

    print(f"Log cleanup complete: {deleted_count} files deleted")
    return deleted_count


def x_cleanup_old_logs__mutmut_34(log_dir: str, retention_days: int):
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

                if file_date <= cutoff_date:
                    log_file.unlink()
                    deleted_count += 1
                    print(f"Deleted old log file: {log_file}")
        except (ValueError, IndexError, OSError) as e:
            print(f"Warning: Could not process log file {log_file}: {e}")

    print(f"Log cleanup complete: {deleted_count} files deleted")
    return deleted_count


def x_cleanup_old_logs__mutmut_35(log_dir: str, retention_days: int):
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
                    deleted_count = 1
                    print(f"Deleted old log file: {log_file}")
        except (ValueError, IndexError, OSError) as e:
            print(f"Warning: Could not process log file {log_file}: {e}")

    print(f"Log cleanup complete: {deleted_count} files deleted")
    return deleted_count


def x_cleanup_old_logs__mutmut_36(log_dir: str, retention_days: int):
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
                    deleted_count -= 1
                    print(f"Deleted old log file: {log_file}")
        except (ValueError, IndexError, OSError) as e:
            print(f"Warning: Could not process log file {log_file}: {e}")

    print(f"Log cleanup complete: {deleted_count} files deleted")
    return deleted_count


def x_cleanup_old_logs__mutmut_37(log_dir: str, retention_days: int):
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
                    deleted_count += 2
                    print(f"Deleted old log file: {log_file}")
        except (ValueError, IndexError, OSError) as e:
            print(f"Warning: Could not process log file {log_file}: {e}")

    print(f"Log cleanup complete: {deleted_count} files deleted")
    return deleted_count


def x_cleanup_old_logs__mutmut_38(log_dir: str, retention_days: int):
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
                    print(None)
        except (ValueError, IndexError, OSError) as e:
            print(f"Warning: Could not process log file {log_file}: {e}")

    print(f"Log cleanup complete: {deleted_count} files deleted")
    return deleted_count


def x_cleanup_old_logs__mutmut_39(log_dir: str, retention_days: int):
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
            print(None)

    print(f"Log cleanup complete: {deleted_count} files deleted")
    return deleted_count


def x_cleanup_old_logs__mutmut_40(log_dir: str, retention_days: int):
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

    print(None)
    return deleted_count

x_cleanup_old_logs__mutmut_mutants : ClassVar[MutantDict] = {
'x_cleanup_old_logs__mutmut_1': x_cleanup_old_logs__mutmut_1, 
    'x_cleanup_old_logs__mutmut_2': x_cleanup_old_logs__mutmut_2, 
    'x_cleanup_old_logs__mutmut_3': x_cleanup_old_logs__mutmut_3, 
    'x_cleanup_old_logs__mutmut_4': x_cleanup_old_logs__mutmut_4, 
    'x_cleanup_old_logs__mutmut_5': x_cleanup_old_logs__mutmut_5, 
    'x_cleanup_old_logs__mutmut_6': x_cleanup_old_logs__mutmut_6, 
    'x_cleanup_old_logs__mutmut_7': x_cleanup_old_logs__mutmut_7, 
    'x_cleanup_old_logs__mutmut_8': x_cleanup_old_logs__mutmut_8, 
    'x_cleanup_old_logs__mutmut_9': x_cleanup_old_logs__mutmut_9, 
    'x_cleanup_old_logs__mutmut_10': x_cleanup_old_logs__mutmut_10, 
    'x_cleanup_old_logs__mutmut_11': x_cleanup_old_logs__mutmut_11, 
    'x_cleanup_old_logs__mutmut_12': x_cleanup_old_logs__mutmut_12, 
    'x_cleanup_old_logs__mutmut_13': x_cleanup_old_logs__mutmut_13, 
    'x_cleanup_old_logs__mutmut_14': x_cleanup_old_logs__mutmut_14, 
    'x_cleanup_old_logs__mutmut_15': x_cleanup_old_logs__mutmut_15, 
    'x_cleanup_old_logs__mutmut_16': x_cleanup_old_logs__mutmut_16, 
    'x_cleanup_old_logs__mutmut_17': x_cleanup_old_logs__mutmut_17, 
    'x_cleanup_old_logs__mutmut_18': x_cleanup_old_logs__mutmut_18, 
    'x_cleanup_old_logs__mutmut_19': x_cleanup_old_logs__mutmut_19, 
    'x_cleanup_old_logs__mutmut_20': x_cleanup_old_logs__mutmut_20, 
    'x_cleanup_old_logs__mutmut_21': x_cleanup_old_logs__mutmut_21, 
    'x_cleanup_old_logs__mutmut_22': x_cleanup_old_logs__mutmut_22, 
    'x_cleanup_old_logs__mutmut_23': x_cleanup_old_logs__mutmut_23, 
    'x_cleanup_old_logs__mutmut_24': x_cleanup_old_logs__mutmut_24, 
    'x_cleanup_old_logs__mutmut_25': x_cleanup_old_logs__mutmut_25, 
    'x_cleanup_old_logs__mutmut_26': x_cleanup_old_logs__mutmut_26, 
    'x_cleanup_old_logs__mutmut_27': x_cleanup_old_logs__mutmut_27, 
    'x_cleanup_old_logs__mutmut_28': x_cleanup_old_logs__mutmut_28, 
    'x_cleanup_old_logs__mutmut_29': x_cleanup_old_logs__mutmut_29, 
    'x_cleanup_old_logs__mutmut_30': x_cleanup_old_logs__mutmut_30, 
    'x_cleanup_old_logs__mutmut_31': x_cleanup_old_logs__mutmut_31, 
    'x_cleanup_old_logs__mutmut_32': x_cleanup_old_logs__mutmut_32, 
    'x_cleanup_old_logs__mutmut_33': x_cleanup_old_logs__mutmut_33, 
    'x_cleanup_old_logs__mutmut_34': x_cleanup_old_logs__mutmut_34, 
    'x_cleanup_old_logs__mutmut_35': x_cleanup_old_logs__mutmut_35, 
    'x_cleanup_old_logs__mutmut_36': x_cleanup_old_logs__mutmut_36, 
    'x_cleanup_old_logs__mutmut_37': x_cleanup_old_logs__mutmut_37, 
    'x_cleanup_old_logs__mutmut_38': x_cleanup_old_logs__mutmut_38, 
    'x_cleanup_old_logs__mutmut_39': x_cleanup_old_logs__mutmut_39, 
    'x_cleanup_old_logs__mutmut_40': x_cleanup_old_logs__mutmut_40
}

def cleanup_old_logs(*args, **kwargs):
    result = _mutmut_trampoline(x_cleanup_old_logs__mutmut_orig, x_cleanup_old_logs__mutmut_mutants, args, kwargs)
    return result 

cleanup_old_logs.__signature__ = _mutmut_signature(x_cleanup_old_logs__mutmut_orig)
x_cleanup_old_logs__mutmut_orig.__name__ = 'x_cleanup_old_logs'
