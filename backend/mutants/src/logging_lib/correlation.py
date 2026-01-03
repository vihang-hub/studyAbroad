"""
Correlation ID Management

Context-based correlation ID tracking for request tracing.
Equivalent to TypeScript correlation.ts using contextvars.
"""

import uuid
from contextvars import ContextVar
from typing import Optional

# Context variable for correlation ID
_correlation_id_var: ContextVar[Optional[str]] = ContextVar("correlation_id", default=None)
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


def x_get_correlation_id__mutmut_orig() -> str:
    """
    Get current correlation ID

    Returns:
        Current correlation ID or generates new one
    """
    correlation_id = _correlation_id_var.get()
    if correlation_id is None:
        correlation_id = str(uuid.uuid4())
        _correlation_id_var.set(correlation_id)
    return correlation_id


def x_get_correlation_id__mutmut_1() -> str:
    """
    Get current correlation ID

    Returns:
        Current correlation ID or generates new one
    """
    correlation_id = None
    if correlation_id is None:
        correlation_id = str(uuid.uuid4())
        _correlation_id_var.set(correlation_id)
    return correlation_id


def x_get_correlation_id__mutmut_2() -> str:
    """
    Get current correlation ID

    Returns:
        Current correlation ID or generates new one
    """
    correlation_id = _correlation_id_var.get()
    if correlation_id is not None:
        correlation_id = str(uuid.uuid4())
        _correlation_id_var.set(correlation_id)
    return correlation_id


def x_get_correlation_id__mutmut_3() -> str:
    """
    Get current correlation ID

    Returns:
        Current correlation ID or generates new one
    """
    correlation_id = _correlation_id_var.get()
    if correlation_id is None:
        correlation_id = None
        _correlation_id_var.set(correlation_id)
    return correlation_id


def x_get_correlation_id__mutmut_4() -> str:
    """
    Get current correlation ID

    Returns:
        Current correlation ID or generates new one
    """
    correlation_id = _correlation_id_var.get()
    if correlation_id is None:
        correlation_id = str(None)
        _correlation_id_var.set(correlation_id)
    return correlation_id


def x_get_correlation_id__mutmut_5() -> str:
    """
    Get current correlation ID

    Returns:
        Current correlation ID or generates new one
    """
    correlation_id = _correlation_id_var.get()
    if correlation_id is None:
        correlation_id = str(uuid.uuid4())
        _correlation_id_var.set(None)
    return correlation_id

x_get_correlation_id__mutmut_mutants : ClassVar[MutantDict] = {
'x_get_correlation_id__mutmut_1': x_get_correlation_id__mutmut_1, 
    'x_get_correlation_id__mutmut_2': x_get_correlation_id__mutmut_2, 
    'x_get_correlation_id__mutmut_3': x_get_correlation_id__mutmut_3, 
    'x_get_correlation_id__mutmut_4': x_get_correlation_id__mutmut_4, 
    'x_get_correlation_id__mutmut_5': x_get_correlation_id__mutmut_5
}

def get_correlation_id(*args, **kwargs):
    result = _mutmut_trampoline(x_get_correlation_id__mutmut_orig, x_get_correlation_id__mutmut_mutants, args, kwargs)
    return result 

get_correlation_id.__signature__ = _mutmut_signature(x_get_correlation_id__mutmut_orig)
x_get_correlation_id__mutmut_orig.__name__ = 'x_get_correlation_id'


def x_set_correlation_id__mutmut_orig(correlation_id: str) -> None:
    """
    Set correlation ID for current context

    Args:
        correlation_id: Correlation ID to set
    """
    _correlation_id_var.set(correlation_id)


def x_set_correlation_id__mutmut_1(correlation_id: str) -> None:
    """
    Set correlation ID for current context

    Args:
        correlation_id: Correlation ID to set
    """
    _correlation_id_var.set(None)

x_set_correlation_id__mutmut_mutants : ClassVar[MutantDict] = {
'x_set_correlation_id__mutmut_1': x_set_correlation_id__mutmut_1
}

def set_correlation_id(*args, **kwargs):
    result = _mutmut_trampoline(x_set_correlation_id__mutmut_orig, x_set_correlation_id__mutmut_mutants, args, kwargs)
    return result 

set_correlation_id.__signature__ = _mutmut_signature(x_set_correlation_id__mutmut_orig)
x_set_correlation_id__mutmut_orig.__name__ = 'x_set_correlation_id'


def clear_correlation_id() -> None:
    """Clear correlation ID from current context"""
    _correlation_id_var.set(None)


class CorrelationContext:
    """
    Context manager for correlation ID

    Usage:
        with CorrelationContext():
            logger.info("Request started")
            # All logs in this context will have same correlation_id

        with CorrelationContext(correlation_id="custom-id"):
            logger.info("Custom correlation ID")
    """

    def xǁCorrelationContextǁ__init____mutmut_orig(self, correlation_id: Optional[str] = None):
        """
        Initialize correlation context

        Args:
            correlation_id: Optional correlation ID (generates new one if not provided)
        """
        self.correlation_id = correlation_id or str(uuid.uuid4())
        self.previous_id: Optional[str] = None

    def xǁCorrelationContextǁ__init____mutmut_1(self, correlation_id: Optional[str] = None):
        """
        Initialize correlation context

        Args:
            correlation_id: Optional correlation ID (generates new one if not provided)
        """
        self.correlation_id = None
        self.previous_id: Optional[str] = None

    def xǁCorrelationContextǁ__init____mutmut_2(self, correlation_id: Optional[str] = None):
        """
        Initialize correlation context

        Args:
            correlation_id: Optional correlation ID (generates new one if not provided)
        """
        self.correlation_id = correlation_id and str(uuid.uuid4())
        self.previous_id: Optional[str] = None

    def xǁCorrelationContextǁ__init____mutmut_3(self, correlation_id: Optional[str] = None):
        """
        Initialize correlation context

        Args:
            correlation_id: Optional correlation ID (generates new one if not provided)
        """
        self.correlation_id = correlation_id or str(None)
        self.previous_id: Optional[str] = None

    def xǁCorrelationContextǁ__init____mutmut_4(self, correlation_id: Optional[str] = None):
        """
        Initialize correlation context

        Args:
            correlation_id: Optional correlation ID (generates new one if not provided)
        """
        self.correlation_id = correlation_id or str(uuid.uuid4())
        self.previous_id: Optional[str] = ""
    
    xǁCorrelationContextǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁCorrelationContextǁ__init____mutmut_1': xǁCorrelationContextǁ__init____mutmut_1, 
        'xǁCorrelationContextǁ__init____mutmut_2': xǁCorrelationContextǁ__init____mutmut_2, 
        'xǁCorrelationContextǁ__init____mutmut_3': xǁCorrelationContextǁ__init____mutmut_3, 
        'xǁCorrelationContextǁ__init____mutmut_4': xǁCorrelationContextǁ__init____mutmut_4
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁCorrelationContextǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁCorrelationContextǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁCorrelationContextǁ__init____mutmut_orig)
    xǁCorrelationContextǁ__init____mutmut_orig.__name__ = 'xǁCorrelationContextǁ__init__'

    def xǁCorrelationContextǁ__enter____mutmut_orig(self):
        """Enter context and set correlation ID"""
        self.previous_id = _correlation_id_var.get()
        _correlation_id_var.set(self.correlation_id)
        return self

    def xǁCorrelationContextǁ__enter____mutmut_1(self):
        """Enter context and set correlation ID"""
        self.previous_id = None
        _correlation_id_var.set(self.correlation_id)
        return self

    def xǁCorrelationContextǁ__enter____mutmut_2(self):
        """Enter context and set correlation ID"""
        self.previous_id = _correlation_id_var.get()
        _correlation_id_var.set(None)
        return self
    
    xǁCorrelationContextǁ__enter____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁCorrelationContextǁ__enter____mutmut_1': xǁCorrelationContextǁ__enter____mutmut_1, 
        'xǁCorrelationContextǁ__enter____mutmut_2': xǁCorrelationContextǁ__enter____mutmut_2
    }
    
    def __enter__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁCorrelationContextǁ__enter____mutmut_orig"), object.__getattribute__(self, "xǁCorrelationContextǁ__enter____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __enter__.__signature__ = _mutmut_signature(xǁCorrelationContextǁ__enter____mutmut_orig)
    xǁCorrelationContextǁ__enter____mutmut_orig.__name__ = 'xǁCorrelationContextǁ__enter__'

    def xǁCorrelationContextǁ__exit____mutmut_orig(self, exc_type, exc_val, exc_tb):
        """Exit context and restore previous correlation ID"""
        _correlation_id_var.set(self.previous_id)

    def xǁCorrelationContextǁ__exit____mutmut_1(self, exc_type, exc_val, exc_tb):
        """Exit context and restore previous correlation ID"""
        _correlation_id_var.set(None)
    
    xǁCorrelationContextǁ__exit____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁCorrelationContextǁ__exit____mutmut_1': xǁCorrelationContextǁ__exit____mutmut_1
    }
    
    def __exit__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁCorrelationContextǁ__exit____mutmut_orig"), object.__getattribute__(self, "xǁCorrelationContextǁ__exit____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __exit__.__signature__ = _mutmut_signature(xǁCorrelationContextǁ__exit____mutmut_orig)
    xǁCorrelationContextǁ__exit____mutmut_orig.__name__ = 'xǁCorrelationContextǁ__exit__'
