"""
Rate Limiting Middleware

Implements token bucket algorithm for rate limiting API requests.
Limits: 100 requests per minute per user (identified by user_id or IP address).
"""

import time
from typing import Dict
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
import structlog

logger = structlog.get_logger(__name__)
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


class TokenBucket:
    """
    Token bucket implementation for rate limiting

    Allows bursts up to capacity, then refills at a constant rate.
    """

    def xǁTokenBucketǁ__init____mutmut_orig(self, capacity: int, refill_rate: float):
        """
        Initialize token bucket

        Args:
            capacity: Maximum number of tokens (max burst size)
            refill_rate: Tokens added per second
        """
        self.capacity = capacity
        self.refill_rate = refill_rate
        self.tokens = capacity
        self.last_refill = time.time()

    def xǁTokenBucketǁ__init____mutmut_1(self, capacity: int, refill_rate: float):
        """
        Initialize token bucket

        Args:
            capacity: Maximum number of tokens (max burst size)
            refill_rate: Tokens added per second
        """
        self.capacity = None
        self.refill_rate = refill_rate
        self.tokens = capacity
        self.last_refill = time.time()

    def xǁTokenBucketǁ__init____mutmut_2(self, capacity: int, refill_rate: float):
        """
        Initialize token bucket

        Args:
            capacity: Maximum number of tokens (max burst size)
            refill_rate: Tokens added per second
        """
        self.capacity = capacity
        self.refill_rate = None
        self.tokens = capacity
        self.last_refill = time.time()

    def xǁTokenBucketǁ__init____mutmut_3(self, capacity: int, refill_rate: float):
        """
        Initialize token bucket

        Args:
            capacity: Maximum number of tokens (max burst size)
            refill_rate: Tokens added per second
        """
        self.capacity = capacity
        self.refill_rate = refill_rate
        self.tokens = None
        self.last_refill = time.time()

    def xǁTokenBucketǁ__init____mutmut_4(self, capacity: int, refill_rate: float):
        """
        Initialize token bucket

        Args:
            capacity: Maximum number of tokens (max burst size)
            refill_rate: Tokens added per second
        """
        self.capacity = capacity
        self.refill_rate = refill_rate
        self.tokens = capacity
        self.last_refill = None
    
    xǁTokenBucketǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁTokenBucketǁ__init____mutmut_1': xǁTokenBucketǁ__init____mutmut_1, 
        'xǁTokenBucketǁ__init____mutmut_2': xǁTokenBucketǁ__init____mutmut_2, 
        'xǁTokenBucketǁ__init____mutmut_3': xǁTokenBucketǁ__init____mutmut_3, 
        'xǁTokenBucketǁ__init____mutmut_4': xǁTokenBucketǁ__init____mutmut_4
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁTokenBucketǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁTokenBucketǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁTokenBucketǁ__init____mutmut_orig)
    xǁTokenBucketǁ__init____mutmut_orig.__name__ = 'xǁTokenBucketǁ__init__'

    def xǁTokenBucketǁconsume__mutmut_orig(self, tokens: int = 1) -> bool:
        """
        Attempt to consume tokens from bucket

        Args:
            tokens: Number of tokens to consume

        Returns:
            True if tokens were consumed, False if insufficient tokens
        """
        # Refill tokens based on time elapsed
        now = time.time()
        elapsed = now - self.last_refill
        self.tokens = min(self.capacity, self.tokens + (elapsed * self.refill_rate))
        self.last_refill = now

        # Try to consume tokens
        if self.tokens >= tokens:
            self.tokens -= tokens
            return True
        return False

    def xǁTokenBucketǁconsume__mutmut_1(self, tokens: int = 2) -> bool:
        """
        Attempt to consume tokens from bucket

        Args:
            tokens: Number of tokens to consume

        Returns:
            True if tokens were consumed, False if insufficient tokens
        """
        # Refill tokens based on time elapsed
        now = time.time()
        elapsed = now - self.last_refill
        self.tokens = min(self.capacity, self.tokens + (elapsed * self.refill_rate))
        self.last_refill = now

        # Try to consume tokens
        if self.tokens >= tokens:
            self.tokens -= tokens
            return True
        return False

    def xǁTokenBucketǁconsume__mutmut_2(self, tokens: int = 1) -> bool:
        """
        Attempt to consume tokens from bucket

        Args:
            tokens: Number of tokens to consume

        Returns:
            True if tokens were consumed, False if insufficient tokens
        """
        # Refill tokens based on time elapsed
        now = None
        elapsed = now - self.last_refill
        self.tokens = min(self.capacity, self.tokens + (elapsed * self.refill_rate))
        self.last_refill = now

        # Try to consume tokens
        if self.tokens >= tokens:
            self.tokens -= tokens
            return True
        return False

    def xǁTokenBucketǁconsume__mutmut_3(self, tokens: int = 1) -> bool:
        """
        Attempt to consume tokens from bucket

        Args:
            tokens: Number of tokens to consume

        Returns:
            True if tokens were consumed, False if insufficient tokens
        """
        # Refill tokens based on time elapsed
        now = time.time()
        elapsed = None
        self.tokens = min(self.capacity, self.tokens + (elapsed * self.refill_rate))
        self.last_refill = now

        # Try to consume tokens
        if self.tokens >= tokens:
            self.tokens -= tokens
            return True
        return False

    def xǁTokenBucketǁconsume__mutmut_4(self, tokens: int = 1) -> bool:
        """
        Attempt to consume tokens from bucket

        Args:
            tokens: Number of tokens to consume

        Returns:
            True if tokens were consumed, False if insufficient tokens
        """
        # Refill tokens based on time elapsed
        now = time.time()
        elapsed = now + self.last_refill
        self.tokens = min(self.capacity, self.tokens + (elapsed * self.refill_rate))
        self.last_refill = now

        # Try to consume tokens
        if self.tokens >= tokens:
            self.tokens -= tokens
            return True
        return False

    def xǁTokenBucketǁconsume__mutmut_5(self, tokens: int = 1) -> bool:
        """
        Attempt to consume tokens from bucket

        Args:
            tokens: Number of tokens to consume

        Returns:
            True if tokens were consumed, False if insufficient tokens
        """
        # Refill tokens based on time elapsed
        now = time.time()
        elapsed = now - self.last_refill
        self.tokens = None
        self.last_refill = now

        # Try to consume tokens
        if self.tokens >= tokens:
            self.tokens -= tokens
            return True
        return False

    def xǁTokenBucketǁconsume__mutmut_6(self, tokens: int = 1) -> bool:
        """
        Attempt to consume tokens from bucket

        Args:
            tokens: Number of tokens to consume

        Returns:
            True if tokens were consumed, False if insufficient tokens
        """
        # Refill tokens based on time elapsed
        now = time.time()
        elapsed = now - self.last_refill
        self.tokens = min(None, self.tokens + (elapsed * self.refill_rate))
        self.last_refill = now

        # Try to consume tokens
        if self.tokens >= tokens:
            self.tokens -= tokens
            return True
        return False

    def xǁTokenBucketǁconsume__mutmut_7(self, tokens: int = 1) -> bool:
        """
        Attempt to consume tokens from bucket

        Args:
            tokens: Number of tokens to consume

        Returns:
            True if tokens were consumed, False if insufficient tokens
        """
        # Refill tokens based on time elapsed
        now = time.time()
        elapsed = now - self.last_refill
        self.tokens = min(self.capacity, None)
        self.last_refill = now

        # Try to consume tokens
        if self.tokens >= tokens:
            self.tokens -= tokens
            return True
        return False

    def xǁTokenBucketǁconsume__mutmut_8(self, tokens: int = 1) -> bool:
        """
        Attempt to consume tokens from bucket

        Args:
            tokens: Number of tokens to consume

        Returns:
            True if tokens were consumed, False if insufficient tokens
        """
        # Refill tokens based on time elapsed
        now = time.time()
        elapsed = now - self.last_refill
        self.tokens = min(self.tokens + (elapsed * self.refill_rate))
        self.last_refill = now

        # Try to consume tokens
        if self.tokens >= tokens:
            self.tokens -= tokens
            return True
        return False

    def xǁTokenBucketǁconsume__mutmut_9(self, tokens: int = 1) -> bool:
        """
        Attempt to consume tokens from bucket

        Args:
            tokens: Number of tokens to consume

        Returns:
            True if tokens were consumed, False if insufficient tokens
        """
        # Refill tokens based on time elapsed
        now = time.time()
        elapsed = now - self.last_refill
        self.tokens = min(self.capacity, )
        self.last_refill = now

        # Try to consume tokens
        if self.tokens >= tokens:
            self.tokens -= tokens
            return True
        return False

    def xǁTokenBucketǁconsume__mutmut_10(self, tokens: int = 1) -> bool:
        """
        Attempt to consume tokens from bucket

        Args:
            tokens: Number of tokens to consume

        Returns:
            True if tokens were consumed, False if insufficient tokens
        """
        # Refill tokens based on time elapsed
        now = time.time()
        elapsed = now - self.last_refill
        self.tokens = min(self.capacity, self.tokens - (elapsed * self.refill_rate))
        self.last_refill = now

        # Try to consume tokens
        if self.tokens >= tokens:
            self.tokens -= tokens
            return True
        return False

    def xǁTokenBucketǁconsume__mutmut_11(self, tokens: int = 1) -> bool:
        """
        Attempt to consume tokens from bucket

        Args:
            tokens: Number of tokens to consume

        Returns:
            True if tokens were consumed, False if insufficient tokens
        """
        # Refill tokens based on time elapsed
        now = time.time()
        elapsed = now - self.last_refill
        self.tokens = min(self.capacity, self.tokens + (elapsed / self.refill_rate))
        self.last_refill = now

        # Try to consume tokens
        if self.tokens >= tokens:
            self.tokens -= tokens
            return True
        return False

    def xǁTokenBucketǁconsume__mutmut_12(self, tokens: int = 1) -> bool:
        """
        Attempt to consume tokens from bucket

        Args:
            tokens: Number of tokens to consume

        Returns:
            True if tokens were consumed, False if insufficient tokens
        """
        # Refill tokens based on time elapsed
        now = time.time()
        elapsed = now - self.last_refill
        self.tokens = min(self.capacity, self.tokens + (elapsed * self.refill_rate))
        self.last_refill = None

        # Try to consume tokens
        if self.tokens >= tokens:
            self.tokens -= tokens
            return True
        return False

    def xǁTokenBucketǁconsume__mutmut_13(self, tokens: int = 1) -> bool:
        """
        Attempt to consume tokens from bucket

        Args:
            tokens: Number of tokens to consume

        Returns:
            True if tokens were consumed, False if insufficient tokens
        """
        # Refill tokens based on time elapsed
        now = time.time()
        elapsed = now - self.last_refill
        self.tokens = min(self.capacity, self.tokens + (elapsed * self.refill_rate))
        self.last_refill = now

        # Try to consume tokens
        if self.tokens > tokens:
            self.tokens -= tokens
            return True
        return False

    def xǁTokenBucketǁconsume__mutmut_14(self, tokens: int = 1) -> bool:
        """
        Attempt to consume tokens from bucket

        Args:
            tokens: Number of tokens to consume

        Returns:
            True if tokens were consumed, False if insufficient tokens
        """
        # Refill tokens based on time elapsed
        now = time.time()
        elapsed = now - self.last_refill
        self.tokens = min(self.capacity, self.tokens + (elapsed * self.refill_rate))
        self.last_refill = now

        # Try to consume tokens
        if self.tokens >= tokens:
            self.tokens = tokens
            return True
        return False

    def xǁTokenBucketǁconsume__mutmut_15(self, tokens: int = 1) -> bool:
        """
        Attempt to consume tokens from bucket

        Args:
            tokens: Number of tokens to consume

        Returns:
            True if tokens were consumed, False if insufficient tokens
        """
        # Refill tokens based on time elapsed
        now = time.time()
        elapsed = now - self.last_refill
        self.tokens = min(self.capacity, self.tokens + (elapsed * self.refill_rate))
        self.last_refill = now

        # Try to consume tokens
        if self.tokens >= tokens:
            self.tokens += tokens
            return True
        return False

    def xǁTokenBucketǁconsume__mutmut_16(self, tokens: int = 1) -> bool:
        """
        Attempt to consume tokens from bucket

        Args:
            tokens: Number of tokens to consume

        Returns:
            True if tokens were consumed, False if insufficient tokens
        """
        # Refill tokens based on time elapsed
        now = time.time()
        elapsed = now - self.last_refill
        self.tokens = min(self.capacity, self.tokens + (elapsed * self.refill_rate))
        self.last_refill = now

        # Try to consume tokens
        if self.tokens >= tokens:
            self.tokens -= tokens
            return False
        return False

    def xǁTokenBucketǁconsume__mutmut_17(self, tokens: int = 1) -> bool:
        """
        Attempt to consume tokens from bucket

        Args:
            tokens: Number of tokens to consume

        Returns:
            True if tokens were consumed, False if insufficient tokens
        """
        # Refill tokens based on time elapsed
        now = time.time()
        elapsed = now - self.last_refill
        self.tokens = min(self.capacity, self.tokens + (elapsed * self.refill_rate))
        self.last_refill = now

        # Try to consume tokens
        if self.tokens >= tokens:
            self.tokens -= tokens
            return True
        return True
    
    xǁTokenBucketǁconsume__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁTokenBucketǁconsume__mutmut_1': xǁTokenBucketǁconsume__mutmut_1, 
        'xǁTokenBucketǁconsume__mutmut_2': xǁTokenBucketǁconsume__mutmut_2, 
        'xǁTokenBucketǁconsume__mutmut_3': xǁTokenBucketǁconsume__mutmut_3, 
        'xǁTokenBucketǁconsume__mutmut_4': xǁTokenBucketǁconsume__mutmut_4, 
        'xǁTokenBucketǁconsume__mutmut_5': xǁTokenBucketǁconsume__mutmut_5, 
        'xǁTokenBucketǁconsume__mutmut_6': xǁTokenBucketǁconsume__mutmut_6, 
        'xǁTokenBucketǁconsume__mutmut_7': xǁTokenBucketǁconsume__mutmut_7, 
        'xǁTokenBucketǁconsume__mutmut_8': xǁTokenBucketǁconsume__mutmut_8, 
        'xǁTokenBucketǁconsume__mutmut_9': xǁTokenBucketǁconsume__mutmut_9, 
        'xǁTokenBucketǁconsume__mutmut_10': xǁTokenBucketǁconsume__mutmut_10, 
        'xǁTokenBucketǁconsume__mutmut_11': xǁTokenBucketǁconsume__mutmut_11, 
        'xǁTokenBucketǁconsume__mutmut_12': xǁTokenBucketǁconsume__mutmut_12, 
        'xǁTokenBucketǁconsume__mutmut_13': xǁTokenBucketǁconsume__mutmut_13, 
        'xǁTokenBucketǁconsume__mutmut_14': xǁTokenBucketǁconsume__mutmut_14, 
        'xǁTokenBucketǁconsume__mutmut_15': xǁTokenBucketǁconsume__mutmut_15, 
        'xǁTokenBucketǁconsume__mutmut_16': xǁTokenBucketǁconsume__mutmut_16, 
        'xǁTokenBucketǁconsume__mutmut_17': xǁTokenBucketǁconsume__mutmut_17
    }
    
    def consume(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁTokenBucketǁconsume__mutmut_orig"), object.__getattribute__(self, "xǁTokenBucketǁconsume__mutmut_mutants"), args, kwargs, self)
        return result 
    
    consume.__signature__ = _mutmut_signature(xǁTokenBucketǁconsume__mutmut_orig)
    xǁTokenBucketǁconsume__mutmut_orig.__name__ = 'xǁTokenBucketǁconsume'

    def xǁTokenBucketǁget_wait_time__mutmut_orig(self, tokens: int = 1) -> float:
        """
        Calculate how long to wait until tokens are available

        Args:
            tokens: Number of tokens needed

        Returns:
            Wait time in seconds
        """
        tokens_needed = tokens - self.tokens
        if tokens_needed <= 0:
            return 0.0
        return tokens_needed / self.refill_rate

    def xǁTokenBucketǁget_wait_time__mutmut_1(self, tokens: int = 2) -> float:
        """
        Calculate how long to wait until tokens are available

        Args:
            tokens: Number of tokens needed

        Returns:
            Wait time in seconds
        """
        tokens_needed = tokens - self.tokens
        if tokens_needed <= 0:
            return 0.0
        return tokens_needed / self.refill_rate

    def xǁTokenBucketǁget_wait_time__mutmut_2(self, tokens: int = 1) -> float:
        """
        Calculate how long to wait until tokens are available

        Args:
            tokens: Number of tokens needed

        Returns:
            Wait time in seconds
        """
        tokens_needed = None
        if tokens_needed <= 0:
            return 0.0
        return tokens_needed / self.refill_rate

    def xǁTokenBucketǁget_wait_time__mutmut_3(self, tokens: int = 1) -> float:
        """
        Calculate how long to wait until tokens are available

        Args:
            tokens: Number of tokens needed

        Returns:
            Wait time in seconds
        """
        tokens_needed = tokens + self.tokens
        if tokens_needed <= 0:
            return 0.0
        return tokens_needed / self.refill_rate

    def xǁTokenBucketǁget_wait_time__mutmut_4(self, tokens: int = 1) -> float:
        """
        Calculate how long to wait until tokens are available

        Args:
            tokens: Number of tokens needed

        Returns:
            Wait time in seconds
        """
        tokens_needed = tokens - self.tokens
        if tokens_needed < 0:
            return 0.0
        return tokens_needed / self.refill_rate

    def xǁTokenBucketǁget_wait_time__mutmut_5(self, tokens: int = 1) -> float:
        """
        Calculate how long to wait until tokens are available

        Args:
            tokens: Number of tokens needed

        Returns:
            Wait time in seconds
        """
        tokens_needed = tokens - self.tokens
        if tokens_needed <= 1:
            return 0.0
        return tokens_needed / self.refill_rate

    def xǁTokenBucketǁget_wait_time__mutmut_6(self, tokens: int = 1) -> float:
        """
        Calculate how long to wait until tokens are available

        Args:
            tokens: Number of tokens needed

        Returns:
            Wait time in seconds
        """
        tokens_needed = tokens - self.tokens
        if tokens_needed <= 0:
            return 1.0
        return tokens_needed / self.refill_rate

    def xǁTokenBucketǁget_wait_time__mutmut_7(self, tokens: int = 1) -> float:
        """
        Calculate how long to wait until tokens are available

        Args:
            tokens: Number of tokens needed

        Returns:
            Wait time in seconds
        """
        tokens_needed = tokens - self.tokens
        if tokens_needed <= 0:
            return 0.0
        return tokens_needed * self.refill_rate
    
    xǁTokenBucketǁget_wait_time__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁTokenBucketǁget_wait_time__mutmut_1': xǁTokenBucketǁget_wait_time__mutmut_1, 
        'xǁTokenBucketǁget_wait_time__mutmut_2': xǁTokenBucketǁget_wait_time__mutmut_2, 
        'xǁTokenBucketǁget_wait_time__mutmut_3': xǁTokenBucketǁget_wait_time__mutmut_3, 
        'xǁTokenBucketǁget_wait_time__mutmut_4': xǁTokenBucketǁget_wait_time__mutmut_4, 
        'xǁTokenBucketǁget_wait_time__mutmut_5': xǁTokenBucketǁget_wait_time__mutmut_5, 
        'xǁTokenBucketǁget_wait_time__mutmut_6': xǁTokenBucketǁget_wait_time__mutmut_6, 
        'xǁTokenBucketǁget_wait_time__mutmut_7': xǁTokenBucketǁget_wait_time__mutmut_7
    }
    
    def get_wait_time(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁTokenBucketǁget_wait_time__mutmut_orig"), object.__getattribute__(self, "xǁTokenBucketǁget_wait_time__mutmut_mutants"), args, kwargs, self)
        return result 
    
    get_wait_time.__signature__ = _mutmut_signature(xǁTokenBucketǁget_wait_time__mutmut_orig)
    xǁTokenBucketǁget_wait_time__mutmut_orig.__name__ = 'xǁTokenBucketǁget_wait_time'


class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    Rate limiting middleware using token bucket algorithm

    Configuration:
    - RATE_LIMIT_REQUESTS_PER_MINUTE: Max requests per minute (default: 100)
    - RATE_LIMIT_ENABLED: Enable/disable rate limiting (default: True)

    Headers added to response:
    - X-RateLimit-Limit: Maximum requests allowed
    - X-RateLimit-Remaining: Requests remaining in current window
    - X-RateLimit-Reset: Seconds until bucket refills
    - Retry-After: Seconds to wait (only on 429 responses)
    """

    def xǁRateLimitMiddlewareǁ__init____mutmut_orig(self, app, requests_per_minute: int = 100):
        """
        Initialize rate limiter

        Args:
            app: FastAPI application
            requests_per_minute: Maximum requests allowed per minute per user
        """
        super().__init__(app)
        self.requests_per_minute = requests_per_minute
        # Convert to requests per second for token bucket
        self.refill_rate = requests_per_minute / 60.0
        # Allow burst of up to the per-minute limit
        self.capacity = requests_per_minute
        # Store buckets per user (user_id or IP address)
        self.buckets: Dict[str, TokenBucket] = {}

        logger.info(
            "rate_limiter_initialized",
            requests_per_minute=requests_per_minute,
            refill_rate=self.refill_rate,
            capacity=self.capacity,
        )

    def xǁRateLimitMiddlewareǁ__init____mutmut_1(self, app, requests_per_minute: int = 101):
        """
        Initialize rate limiter

        Args:
            app: FastAPI application
            requests_per_minute: Maximum requests allowed per minute per user
        """
        super().__init__(app)
        self.requests_per_minute = requests_per_minute
        # Convert to requests per second for token bucket
        self.refill_rate = requests_per_minute / 60.0
        # Allow burst of up to the per-minute limit
        self.capacity = requests_per_minute
        # Store buckets per user (user_id or IP address)
        self.buckets: Dict[str, TokenBucket] = {}

        logger.info(
            "rate_limiter_initialized",
            requests_per_minute=requests_per_minute,
            refill_rate=self.refill_rate,
            capacity=self.capacity,
        )

    def xǁRateLimitMiddlewareǁ__init____mutmut_2(self, app, requests_per_minute: int = 100):
        """
        Initialize rate limiter

        Args:
            app: FastAPI application
            requests_per_minute: Maximum requests allowed per minute per user
        """
        super().__init__(None)
        self.requests_per_minute = requests_per_minute
        # Convert to requests per second for token bucket
        self.refill_rate = requests_per_minute / 60.0
        # Allow burst of up to the per-minute limit
        self.capacity = requests_per_minute
        # Store buckets per user (user_id or IP address)
        self.buckets: Dict[str, TokenBucket] = {}

        logger.info(
            "rate_limiter_initialized",
            requests_per_minute=requests_per_minute,
            refill_rate=self.refill_rate,
            capacity=self.capacity,
        )

    def xǁRateLimitMiddlewareǁ__init____mutmut_3(self, app, requests_per_minute: int = 100):
        """
        Initialize rate limiter

        Args:
            app: FastAPI application
            requests_per_minute: Maximum requests allowed per minute per user
        """
        super().__init__(app)
        self.requests_per_minute = None
        # Convert to requests per second for token bucket
        self.refill_rate = requests_per_minute / 60.0
        # Allow burst of up to the per-minute limit
        self.capacity = requests_per_minute
        # Store buckets per user (user_id or IP address)
        self.buckets: Dict[str, TokenBucket] = {}

        logger.info(
            "rate_limiter_initialized",
            requests_per_minute=requests_per_minute,
            refill_rate=self.refill_rate,
            capacity=self.capacity,
        )

    def xǁRateLimitMiddlewareǁ__init____mutmut_4(self, app, requests_per_minute: int = 100):
        """
        Initialize rate limiter

        Args:
            app: FastAPI application
            requests_per_minute: Maximum requests allowed per minute per user
        """
        super().__init__(app)
        self.requests_per_minute = requests_per_minute
        # Convert to requests per second for token bucket
        self.refill_rate = None
        # Allow burst of up to the per-minute limit
        self.capacity = requests_per_minute
        # Store buckets per user (user_id or IP address)
        self.buckets: Dict[str, TokenBucket] = {}

        logger.info(
            "rate_limiter_initialized",
            requests_per_minute=requests_per_minute,
            refill_rate=self.refill_rate,
            capacity=self.capacity,
        )

    def xǁRateLimitMiddlewareǁ__init____mutmut_5(self, app, requests_per_minute: int = 100):
        """
        Initialize rate limiter

        Args:
            app: FastAPI application
            requests_per_minute: Maximum requests allowed per minute per user
        """
        super().__init__(app)
        self.requests_per_minute = requests_per_minute
        # Convert to requests per second for token bucket
        self.refill_rate = requests_per_minute * 60.0
        # Allow burst of up to the per-minute limit
        self.capacity = requests_per_minute
        # Store buckets per user (user_id or IP address)
        self.buckets: Dict[str, TokenBucket] = {}

        logger.info(
            "rate_limiter_initialized",
            requests_per_minute=requests_per_minute,
            refill_rate=self.refill_rate,
            capacity=self.capacity,
        )

    def xǁRateLimitMiddlewareǁ__init____mutmut_6(self, app, requests_per_minute: int = 100):
        """
        Initialize rate limiter

        Args:
            app: FastAPI application
            requests_per_minute: Maximum requests allowed per minute per user
        """
        super().__init__(app)
        self.requests_per_minute = requests_per_minute
        # Convert to requests per second for token bucket
        self.refill_rate = requests_per_minute / 61.0
        # Allow burst of up to the per-minute limit
        self.capacity = requests_per_minute
        # Store buckets per user (user_id or IP address)
        self.buckets: Dict[str, TokenBucket] = {}

        logger.info(
            "rate_limiter_initialized",
            requests_per_minute=requests_per_minute,
            refill_rate=self.refill_rate,
            capacity=self.capacity,
        )

    def xǁRateLimitMiddlewareǁ__init____mutmut_7(self, app, requests_per_minute: int = 100):
        """
        Initialize rate limiter

        Args:
            app: FastAPI application
            requests_per_minute: Maximum requests allowed per minute per user
        """
        super().__init__(app)
        self.requests_per_minute = requests_per_minute
        # Convert to requests per second for token bucket
        self.refill_rate = requests_per_minute / 60.0
        # Allow burst of up to the per-minute limit
        self.capacity = None
        # Store buckets per user (user_id or IP address)
        self.buckets: Dict[str, TokenBucket] = {}

        logger.info(
            "rate_limiter_initialized",
            requests_per_minute=requests_per_minute,
            refill_rate=self.refill_rate,
            capacity=self.capacity,
        )

    def xǁRateLimitMiddlewareǁ__init____mutmut_8(self, app, requests_per_minute: int = 100):
        """
        Initialize rate limiter

        Args:
            app: FastAPI application
            requests_per_minute: Maximum requests allowed per minute per user
        """
        super().__init__(app)
        self.requests_per_minute = requests_per_minute
        # Convert to requests per second for token bucket
        self.refill_rate = requests_per_minute / 60.0
        # Allow burst of up to the per-minute limit
        self.capacity = requests_per_minute
        # Store buckets per user (user_id or IP address)
        self.buckets: Dict[str, TokenBucket] = None

        logger.info(
            "rate_limiter_initialized",
            requests_per_minute=requests_per_minute,
            refill_rate=self.refill_rate,
            capacity=self.capacity,
        )

    def xǁRateLimitMiddlewareǁ__init____mutmut_9(self, app, requests_per_minute: int = 100):
        """
        Initialize rate limiter

        Args:
            app: FastAPI application
            requests_per_minute: Maximum requests allowed per minute per user
        """
        super().__init__(app)
        self.requests_per_minute = requests_per_minute
        # Convert to requests per second for token bucket
        self.refill_rate = requests_per_minute / 60.0
        # Allow burst of up to the per-minute limit
        self.capacity = requests_per_minute
        # Store buckets per user (user_id or IP address)
        self.buckets: Dict[str, TokenBucket] = {}

        logger.info(
            None,
            requests_per_minute=requests_per_minute,
            refill_rate=self.refill_rate,
            capacity=self.capacity,
        )

    def xǁRateLimitMiddlewareǁ__init____mutmut_10(self, app, requests_per_minute: int = 100):
        """
        Initialize rate limiter

        Args:
            app: FastAPI application
            requests_per_minute: Maximum requests allowed per minute per user
        """
        super().__init__(app)
        self.requests_per_minute = requests_per_minute
        # Convert to requests per second for token bucket
        self.refill_rate = requests_per_minute / 60.0
        # Allow burst of up to the per-minute limit
        self.capacity = requests_per_minute
        # Store buckets per user (user_id or IP address)
        self.buckets: Dict[str, TokenBucket] = {}

        logger.info(
            "rate_limiter_initialized",
            requests_per_minute=None,
            refill_rate=self.refill_rate,
            capacity=self.capacity,
        )

    def xǁRateLimitMiddlewareǁ__init____mutmut_11(self, app, requests_per_minute: int = 100):
        """
        Initialize rate limiter

        Args:
            app: FastAPI application
            requests_per_minute: Maximum requests allowed per minute per user
        """
        super().__init__(app)
        self.requests_per_minute = requests_per_minute
        # Convert to requests per second for token bucket
        self.refill_rate = requests_per_minute / 60.0
        # Allow burst of up to the per-minute limit
        self.capacity = requests_per_minute
        # Store buckets per user (user_id or IP address)
        self.buckets: Dict[str, TokenBucket] = {}

        logger.info(
            "rate_limiter_initialized",
            requests_per_minute=requests_per_minute,
            refill_rate=None,
            capacity=self.capacity,
        )

    def xǁRateLimitMiddlewareǁ__init____mutmut_12(self, app, requests_per_minute: int = 100):
        """
        Initialize rate limiter

        Args:
            app: FastAPI application
            requests_per_minute: Maximum requests allowed per minute per user
        """
        super().__init__(app)
        self.requests_per_minute = requests_per_minute
        # Convert to requests per second for token bucket
        self.refill_rate = requests_per_minute / 60.0
        # Allow burst of up to the per-minute limit
        self.capacity = requests_per_minute
        # Store buckets per user (user_id or IP address)
        self.buckets: Dict[str, TokenBucket] = {}

        logger.info(
            "rate_limiter_initialized",
            requests_per_minute=requests_per_minute,
            refill_rate=self.refill_rate,
            capacity=None,
        )

    def xǁRateLimitMiddlewareǁ__init____mutmut_13(self, app, requests_per_minute: int = 100):
        """
        Initialize rate limiter

        Args:
            app: FastAPI application
            requests_per_minute: Maximum requests allowed per minute per user
        """
        super().__init__(app)
        self.requests_per_minute = requests_per_minute
        # Convert to requests per second for token bucket
        self.refill_rate = requests_per_minute / 60.0
        # Allow burst of up to the per-minute limit
        self.capacity = requests_per_minute
        # Store buckets per user (user_id or IP address)
        self.buckets: Dict[str, TokenBucket] = {}

        logger.info(
            requests_per_minute=requests_per_minute,
            refill_rate=self.refill_rate,
            capacity=self.capacity,
        )

    def xǁRateLimitMiddlewareǁ__init____mutmut_14(self, app, requests_per_minute: int = 100):
        """
        Initialize rate limiter

        Args:
            app: FastAPI application
            requests_per_minute: Maximum requests allowed per minute per user
        """
        super().__init__(app)
        self.requests_per_minute = requests_per_minute
        # Convert to requests per second for token bucket
        self.refill_rate = requests_per_minute / 60.0
        # Allow burst of up to the per-minute limit
        self.capacity = requests_per_minute
        # Store buckets per user (user_id or IP address)
        self.buckets: Dict[str, TokenBucket] = {}

        logger.info(
            "rate_limiter_initialized",
            refill_rate=self.refill_rate,
            capacity=self.capacity,
        )

    def xǁRateLimitMiddlewareǁ__init____mutmut_15(self, app, requests_per_minute: int = 100):
        """
        Initialize rate limiter

        Args:
            app: FastAPI application
            requests_per_minute: Maximum requests allowed per minute per user
        """
        super().__init__(app)
        self.requests_per_minute = requests_per_minute
        # Convert to requests per second for token bucket
        self.refill_rate = requests_per_minute / 60.0
        # Allow burst of up to the per-minute limit
        self.capacity = requests_per_minute
        # Store buckets per user (user_id or IP address)
        self.buckets: Dict[str, TokenBucket] = {}

        logger.info(
            "rate_limiter_initialized",
            requests_per_minute=requests_per_minute,
            capacity=self.capacity,
        )

    def xǁRateLimitMiddlewareǁ__init____mutmut_16(self, app, requests_per_minute: int = 100):
        """
        Initialize rate limiter

        Args:
            app: FastAPI application
            requests_per_minute: Maximum requests allowed per minute per user
        """
        super().__init__(app)
        self.requests_per_minute = requests_per_minute
        # Convert to requests per second for token bucket
        self.refill_rate = requests_per_minute / 60.0
        # Allow burst of up to the per-minute limit
        self.capacity = requests_per_minute
        # Store buckets per user (user_id or IP address)
        self.buckets: Dict[str, TokenBucket] = {}

        logger.info(
            "rate_limiter_initialized",
            requests_per_minute=requests_per_minute,
            refill_rate=self.refill_rate,
            )

    def xǁRateLimitMiddlewareǁ__init____mutmut_17(self, app, requests_per_minute: int = 100):
        """
        Initialize rate limiter

        Args:
            app: FastAPI application
            requests_per_minute: Maximum requests allowed per minute per user
        """
        super().__init__(app)
        self.requests_per_minute = requests_per_minute
        # Convert to requests per second for token bucket
        self.refill_rate = requests_per_minute / 60.0
        # Allow burst of up to the per-minute limit
        self.capacity = requests_per_minute
        # Store buckets per user (user_id or IP address)
        self.buckets: Dict[str, TokenBucket] = {}

        logger.info(
            "XXrate_limiter_initializedXX",
            requests_per_minute=requests_per_minute,
            refill_rate=self.refill_rate,
            capacity=self.capacity,
        )

    def xǁRateLimitMiddlewareǁ__init____mutmut_18(self, app, requests_per_minute: int = 100):
        """
        Initialize rate limiter

        Args:
            app: FastAPI application
            requests_per_minute: Maximum requests allowed per minute per user
        """
        super().__init__(app)
        self.requests_per_minute = requests_per_minute
        # Convert to requests per second for token bucket
        self.refill_rate = requests_per_minute / 60.0
        # Allow burst of up to the per-minute limit
        self.capacity = requests_per_minute
        # Store buckets per user (user_id or IP address)
        self.buckets: Dict[str, TokenBucket] = {}

        logger.info(
            "RATE_LIMITER_INITIALIZED",
            requests_per_minute=requests_per_minute,
            refill_rate=self.refill_rate,
            capacity=self.capacity,
        )
    
    xǁRateLimitMiddlewareǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁRateLimitMiddlewareǁ__init____mutmut_1': xǁRateLimitMiddlewareǁ__init____mutmut_1, 
        'xǁRateLimitMiddlewareǁ__init____mutmut_2': xǁRateLimitMiddlewareǁ__init____mutmut_2, 
        'xǁRateLimitMiddlewareǁ__init____mutmut_3': xǁRateLimitMiddlewareǁ__init____mutmut_3, 
        'xǁRateLimitMiddlewareǁ__init____mutmut_4': xǁRateLimitMiddlewareǁ__init____mutmut_4, 
        'xǁRateLimitMiddlewareǁ__init____mutmut_5': xǁRateLimitMiddlewareǁ__init____mutmut_5, 
        'xǁRateLimitMiddlewareǁ__init____mutmut_6': xǁRateLimitMiddlewareǁ__init____mutmut_6, 
        'xǁRateLimitMiddlewareǁ__init____mutmut_7': xǁRateLimitMiddlewareǁ__init____mutmut_7, 
        'xǁRateLimitMiddlewareǁ__init____mutmut_8': xǁRateLimitMiddlewareǁ__init____mutmut_8, 
        'xǁRateLimitMiddlewareǁ__init____mutmut_9': xǁRateLimitMiddlewareǁ__init____mutmut_9, 
        'xǁRateLimitMiddlewareǁ__init____mutmut_10': xǁRateLimitMiddlewareǁ__init____mutmut_10, 
        'xǁRateLimitMiddlewareǁ__init____mutmut_11': xǁRateLimitMiddlewareǁ__init____mutmut_11, 
        'xǁRateLimitMiddlewareǁ__init____mutmut_12': xǁRateLimitMiddlewareǁ__init____mutmut_12, 
        'xǁRateLimitMiddlewareǁ__init____mutmut_13': xǁRateLimitMiddlewareǁ__init____mutmut_13, 
        'xǁRateLimitMiddlewareǁ__init____mutmut_14': xǁRateLimitMiddlewareǁ__init____mutmut_14, 
        'xǁRateLimitMiddlewareǁ__init____mutmut_15': xǁRateLimitMiddlewareǁ__init____mutmut_15, 
        'xǁRateLimitMiddlewareǁ__init____mutmut_16': xǁRateLimitMiddlewareǁ__init____mutmut_16, 
        'xǁRateLimitMiddlewareǁ__init____mutmut_17': xǁRateLimitMiddlewareǁ__init____mutmut_17, 
        'xǁRateLimitMiddlewareǁ__init____mutmut_18': xǁRateLimitMiddlewareǁ__init____mutmut_18
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁRateLimitMiddlewareǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁRateLimitMiddlewareǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁRateLimitMiddlewareǁ__init____mutmut_orig)
    xǁRateLimitMiddlewareǁ__init____mutmut_orig.__name__ = 'xǁRateLimitMiddlewareǁ__init__'

    def xǁRateLimitMiddlewareǁ_get_identifier__mutmut_orig(self, request: Request) -> str:
        """
        Get unique identifier for rate limiting

        Priority:
        1. user_id from request state (set by auth middleware)
        2. X-User-ID header
        3. Client IP address

        Args:
            request: FastAPI request object

        Returns:
            Unique identifier string
        """
        # Try to get user_id from request state (set by auth middleware)
        if hasattr(request.state, "user_id"):
            return f"user:{request.state.user_id}"

        # Try to get from header
        user_id = request.headers.get("X-User-ID")
        if user_id:
            return f"user:{user_id}"

        # Fall back to IP address
        if request.client:
            return f"ip:{request.client.host}"

        # Default identifier (should rarely happen)
        return "unknown"

    def xǁRateLimitMiddlewareǁ_get_identifier__mutmut_1(self, request: Request) -> str:
        """
        Get unique identifier for rate limiting

        Priority:
        1. user_id from request state (set by auth middleware)
        2. X-User-ID header
        3. Client IP address

        Args:
            request: FastAPI request object

        Returns:
            Unique identifier string
        """
        # Try to get user_id from request state (set by auth middleware)
        if hasattr(None, "user_id"):
            return f"user:{request.state.user_id}"

        # Try to get from header
        user_id = request.headers.get("X-User-ID")
        if user_id:
            return f"user:{user_id}"

        # Fall back to IP address
        if request.client:
            return f"ip:{request.client.host}"

        # Default identifier (should rarely happen)
        return "unknown"

    def xǁRateLimitMiddlewareǁ_get_identifier__mutmut_2(self, request: Request) -> str:
        """
        Get unique identifier for rate limiting

        Priority:
        1. user_id from request state (set by auth middleware)
        2. X-User-ID header
        3. Client IP address

        Args:
            request: FastAPI request object

        Returns:
            Unique identifier string
        """
        # Try to get user_id from request state (set by auth middleware)
        if hasattr(request.state, None):
            return f"user:{request.state.user_id}"

        # Try to get from header
        user_id = request.headers.get("X-User-ID")
        if user_id:
            return f"user:{user_id}"

        # Fall back to IP address
        if request.client:
            return f"ip:{request.client.host}"

        # Default identifier (should rarely happen)
        return "unknown"

    def xǁRateLimitMiddlewareǁ_get_identifier__mutmut_3(self, request: Request) -> str:
        """
        Get unique identifier for rate limiting

        Priority:
        1. user_id from request state (set by auth middleware)
        2. X-User-ID header
        3. Client IP address

        Args:
            request: FastAPI request object

        Returns:
            Unique identifier string
        """
        # Try to get user_id from request state (set by auth middleware)
        if hasattr("user_id"):
            return f"user:{request.state.user_id}"

        # Try to get from header
        user_id = request.headers.get("X-User-ID")
        if user_id:
            return f"user:{user_id}"

        # Fall back to IP address
        if request.client:
            return f"ip:{request.client.host}"

        # Default identifier (should rarely happen)
        return "unknown"

    def xǁRateLimitMiddlewareǁ_get_identifier__mutmut_4(self, request: Request) -> str:
        """
        Get unique identifier for rate limiting

        Priority:
        1. user_id from request state (set by auth middleware)
        2. X-User-ID header
        3. Client IP address

        Args:
            request: FastAPI request object

        Returns:
            Unique identifier string
        """
        # Try to get user_id from request state (set by auth middleware)
        if hasattr(request.state, ):
            return f"user:{request.state.user_id}"

        # Try to get from header
        user_id = request.headers.get("X-User-ID")
        if user_id:
            return f"user:{user_id}"

        # Fall back to IP address
        if request.client:
            return f"ip:{request.client.host}"

        # Default identifier (should rarely happen)
        return "unknown"

    def xǁRateLimitMiddlewareǁ_get_identifier__mutmut_5(self, request: Request) -> str:
        """
        Get unique identifier for rate limiting

        Priority:
        1. user_id from request state (set by auth middleware)
        2. X-User-ID header
        3. Client IP address

        Args:
            request: FastAPI request object

        Returns:
            Unique identifier string
        """
        # Try to get user_id from request state (set by auth middleware)
        if hasattr(request.state, "XXuser_idXX"):
            return f"user:{request.state.user_id}"

        # Try to get from header
        user_id = request.headers.get("X-User-ID")
        if user_id:
            return f"user:{user_id}"

        # Fall back to IP address
        if request.client:
            return f"ip:{request.client.host}"

        # Default identifier (should rarely happen)
        return "unknown"

    def xǁRateLimitMiddlewareǁ_get_identifier__mutmut_6(self, request: Request) -> str:
        """
        Get unique identifier for rate limiting

        Priority:
        1. user_id from request state (set by auth middleware)
        2. X-User-ID header
        3. Client IP address

        Args:
            request: FastAPI request object

        Returns:
            Unique identifier string
        """
        # Try to get user_id from request state (set by auth middleware)
        if hasattr(request.state, "USER_ID"):
            return f"user:{request.state.user_id}"

        # Try to get from header
        user_id = request.headers.get("X-User-ID")
        if user_id:
            return f"user:{user_id}"

        # Fall back to IP address
        if request.client:
            return f"ip:{request.client.host}"

        # Default identifier (should rarely happen)
        return "unknown"

    def xǁRateLimitMiddlewareǁ_get_identifier__mutmut_7(self, request: Request) -> str:
        """
        Get unique identifier for rate limiting

        Priority:
        1. user_id from request state (set by auth middleware)
        2. X-User-ID header
        3. Client IP address

        Args:
            request: FastAPI request object

        Returns:
            Unique identifier string
        """
        # Try to get user_id from request state (set by auth middleware)
        if hasattr(request.state, "user_id"):
            return f"user:{request.state.user_id}"

        # Try to get from header
        user_id = None
        if user_id:
            return f"user:{user_id}"

        # Fall back to IP address
        if request.client:
            return f"ip:{request.client.host}"

        # Default identifier (should rarely happen)
        return "unknown"

    def xǁRateLimitMiddlewareǁ_get_identifier__mutmut_8(self, request: Request) -> str:
        """
        Get unique identifier for rate limiting

        Priority:
        1. user_id from request state (set by auth middleware)
        2. X-User-ID header
        3. Client IP address

        Args:
            request: FastAPI request object

        Returns:
            Unique identifier string
        """
        # Try to get user_id from request state (set by auth middleware)
        if hasattr(request.state, "user_id"):
            return f"user:{request.state.user_id}"

        # Try to get from header
        user_id = request.headers.get(None)
        if user_id:
            return f"user:{user_id}"

        # Fall back to IP address
        if request.client:
            return f"ip:{request.client.host}"

        # Default identifier (should rarely happen)
        return "unknown"

    def xǁRateLimitMiddlewareǁ_get_identifier__mutmut_9(self, request: Request) -> str:
        """
        Get unique identifier for rate limiting

        Priority:
        1. user_id from request state (set by auth middleware)
        2. X-User-ID header
        3. Client IP address

        Args:
            request: FastAPI request object

        Returns:
            Unique identifier string
        """
        # Try to get user_id from request state (set by auth middleware)
        if hasattr(request.state, "user_id"):
            return f"user:{request.state.user_id}"

        # Try to get from header
        user_id = request.headers.get("XXX-User-IDXX")
        if user_id:
            return f"user:{user_id}"

        # Fall back to IP address
        if request.client:
            return f"ip:{request.client.host}"

        # Default identifier (should rarely happen)
        return "unknown"

    def xǁRateLimitMiddlewareǁ_get_identifier__mutmut_10(self, request: Request) -> str:
        """
        Get unique identifier for rate limiting

        Priority:
        1. user_id from request state (set by auth middleware)
        2. X-User-ID header
        3. Client IP address

        Args:
            request: FastAPI request object

        Returns:
            Unique identifier string
        """
        # Try to get user_id from request state (set by auth middleware)
        if hasattr(request.state, "user_id"):
            return f"user:{request.state.user_id}"

        # Try to get from header
        user_id = request.headers.get("x-user-id")
        if user_id:
            return f"user:{user_id}"

        # Fall back to IP address
        if request.client:
            return f"ip:{request.client.host}"

        # Default identifier (should rarely happen)
        return "unknown"

    def xǁRateLimitMiddlewareǁ_get_identifier__mutmut_11(self, request: Request) -> str:
        """
        Get unique identifier for rate limiting

        Priority:
        1. user_id from request state (set by auth middleware)
        2. X-User-ID header
        3. Client IP address

        Args:
            request: FastAPI request object

        Returns:
            Unique identifier string
        """
        # Try to get user_id from request state (set by auth middleware)
        if hasattr(request.state, "user_id"):
            return f"user:{request.state.user_id}"

        # Try to get from header
        user_id = request.headers.get("X-USER-ID")
        if user_id:
            return f"user:{user_id}"

        # Fall back to IP address
        if request.client:
            return f"ip:{request.client.host}"

        # Default identifier (should rarely happen)
        return "unknown"

    def xǁRateLimitMiddlewareǁ_get_identifier__mutmut_12(self, request: Request) -> str:
        """
        Get unique identifier for rate limiting

        Priority:
        1. user_id from request state (set by auth middleware)
        2. X-User-ID header
        3. Client IP address

        Args:
            request: FastAPI request object

        Returns:
            Unique identifier string
        """
        # Try to get user_id from request state (set by auth middleware)
        if hasattr(request.state, "user_id"):
            return f"user:{request.state.user_id}"

        # Try to get from header
        user_id = request.headers.get("X-User-ID")
        if user_id:
            return f"user:{user_id}"

        # Fall back to IP address
        if request.client:
            return f"ip:{request.client.host}"

        # Default identifier (should rarely happen)
        return "XXunknownXX"

    def xǁRateLimitMiddlewareǁ_get_identifier__mutmut_13(self, request: Request) -> str:
        """
        Get unique identifier for rate limiting

        Priority:
        1. user_id from request state (set by auth middleware)
        2. X-User-ID header
        3. Client IP address

        Args:
            request: FastAPI request object

        Returns:
            Unique identifier string
        """
        # Try to get user_id from request state (set by auth middleware)
        if hasattr(request.state, "user_id"):
            return f"user:{request.state.user_id}"

        # Try to get from header
        user_id = request.headers.get("X-User-ID")
        if user_id:
            return f"user:{user_id}"

        # Fall back to IP address
        if request.client:
            return f"ip:{request.client.host}"

        # Default identifier (should rarely happen)
        return "UNKNOWN"
    
    xǁRateLimitMiddlewareǁ_get_identifier__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁRateLimitMiddlewareǁ_get_identifier__mutmut_1': xǁRateLimitMiddlewareǁ_get_identifier__mutmut_1, 
        'xǁRateLimitMiddlewareǁ_get_identifier__mutmut_2': xǁRateLimitMiddlewareǁ_get_identifier__mutmut_2, 
        'xǁRateLimitMiddlewareǁ_get_identifier__mutmut_3': xǁRateLimitMiddlewareǁ_get_identifier__mutmut_3, 
        'xǁRateLimitMiddlewareǁ_get_identifier__mutmut_4': xǁRateLimitMiddlewareǁ_get_identifier__mutmut_4, 
        'xǁRateLimitMiddlewareǁ_get_identifier__mutmut_5': xǁRateLimitMiddlewareǁ_get_identifier__mutmut_5, 
        'xǁRateLimitMiddlewareǁ_get_identifier__mutmut_6': xǁRateLimitMiddlewareǁ_get_identifier__mutmut_6, 
        'xǁRateLimitMiddlewareǁ_get_identifier__mutmut_7': xǁRateLimitMiddlewareǁ_get_identifier__mutmut_7, 
        'xǁRateLimitMiddlewareǁ_get_identifier__mutmut_8': xǁRateLimitMiddlewareǁ_get_identifier__mutmut_8, 
        'xǁRateLimitMiddlewareǁ_get_identifier__mutmut_9': xǁRateLimitMiddlewareǁ_get_identifier__mutmut_9, 
        'xǁRateLimitMiddlewareǁ_get_identifier__mutmut_10': xǁRateLimitMiddlewareǁ_get_identifier__mutmut_10, 
        'xǁRateLimitMiddlewareǁ_get_identifier__mutmut_11': xǁRateLimitMiddlewareǁ_get_identifier__mutmut_11, 
        'xǁRateLimitMiddlewareǁ_get_identifier__mutmut_12': xǁRateLimitMiddlewareǁ_get_identifier__mutmut_12, 
        'xǁRateLimitMiddlewareǁ_get_identifier__mutmut_13': xǁRateLimitMiddlewareǁ_get_identifier__mutmut_13
    }
    
    def _get_identifier(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁRateLimitMiddlewareǁ_get_identifier__mutmut_orig"), object.__getattribute__(self, "xǁRateLimitMiddlewareǁ_get_identifier__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _get_identifier.__signature__ = _mutmut_signature(xǁRateLimitMiddlewareǁ_get_identifier__mutmut_orig)
    xǁRateLimitMiddlewareǁ_get_identifier__mutmut_orig.__name__ = 'xǁRateLimitMiddlewareǁ_get_identifier'

    def xǁRateLimitMiddlewareǁ_get_bucket__mutmut_orig(self, identifier: str) -> TokenBucket:
        """
        Get or create token bucket for identifier

        Args:
            identifier: Unique user/IP identifier

        Returns:
            TokenBucket instance
        """
        if identifier not in self.buckets:
            self.buckets[identifier] = TokenBucket(
                capacity=self.capacity, refill_rate=self.refill_rate
            )
        return self.buckets[identifier]

    def xǁRateLimitMiddlewareǁ_get_bucket__mutmut_1(self, identifier: str) -> TokenBucket:
        """
        Get or create token bucket for identifier

        Args:
            identifier: Unique user/IP identifier

        Returns:
            TokenBucket instance
        """
        if identifier in self.buckets:
            self.buckets[identifier] = TokenBucket(
                capacity=self.capacity, refill_rate=self.refill_rate
            )
        return self.buckets[identifier]

    def xǁRateLimitMiddlewareǁ_get_bucket__mutmut_2(self, identifier: str) -> TokenBucket:
        """
        Get or create token bucket for identifier

        Args:
            identifier: Unique user/IP identifier

        Returns:
            TokenBucket instance
        """
        if identifier not in self.buckets:
            self.buckets[identifier] = None
        return self.buckets[identifier]

    def xǁRateLimitMiddlewareǁ_get_bucket__mutmut_3(self, identifier: str) -> TokenBucket:
        """
        Get or create token bucket for identifier

        Args:
            identifier: Unique user/IP identifier

        Returns:
            TokenBucket instance
        """
        if identifier not in self.buckets:
            self.buckets[identifier] = TokenBucket(
                capacity=None, refill_rate=self.refill_rate
            )
        return self.buckets[identifier]

    def xǁRateLimitMiddlewareǁ_get_bucket__mutmut_4(self, identifier: str) -> TokenBucket:
        """
        Get or create token bucket for identifier

        Args:
            identifier: Unique user/IP identifier

        Returns:
            TokenBucket instance
        """
        if identifier not in self.buckets:
            self.buckets[identifier] = TokenBucket(
                capacity=self.capacity, refill_rate=None
            )
        return self.buckets[identifier]

    def xǁRateLimitMiddlewareǁ_get_bucket__mutmut_5(self, identifier: str) -> TokenBucket:
        """
        Get or create token bucket for identifier

        Args:
            identifier: Unique user/IP identifier

        Returns:
            TokenBucket instance
        """
        if identifier not in self.buckets:
            self.buckets[identifier] = TokenBucket(
                refill_rate=self.refill_rate
            )
        return self.buckets[identifier]

    def xǁRateLimitMiddlewareǁ_get_bucket__mutmut_6(self, identifier: str) -> TokenBucket:
        """
        Get or create token bucket for identifier

        Args:
            identifier: Unique user/IP identifier

        Returns:
            TokenBucket instance
        """
        if identifier not in self.buckets:
            self.buckets[identifier] = TokenBucket(
                capacity=self.capacity, )
        return self.buckets[identifier]
    
    xǁRateLimitMiddlewareǁ_get_bucket__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁRateLimitMiddlewareǁ_get_bucket__mutmut_1': xǁRateLimitMiddlewareǁ_get_bucket__mutmut_1, 
        'xǁRateLimitMiddlewareǁ_get_bucket__mutmut_2': xǁRateLimitMiddlewareǁ_get_bucket__mutmut_2, 
        'xǁRateLimitMiddlewareǁ_get_bucket__mutmut_3': xǁRateLimitMiddlewareǁ_get_bucket__mutmut_3, 
        'xǁRateLimitMiddlewareǁ_get_bucket__mutmut_4': xǁRateLimitMiddlewareǁ_get_bucket__mutmut_4, 
        'xǁRateLimitMiddlewareǁ_get_bucket__mutmut_5': xǁRateLimitMiddlewareǁ_get_bucket__mutmut_5, 
        'xǁRateLimitMiddlewareǁ_get_bucket__mutmut_6': xǁRateLimitMiddlewareǁ_get_bucket__mutmut_6
    }
    
    def _get_bucket(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁRateLimitMiddlewareǁ_get_bucket__mutmut_orig"), object.__getattribute__(self, "xǁRateLimitMiddlewareǁ_get_bucket__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _get_bucket.__signature__ = _mutmut_signature(xǁRateLimitMiddlewareǁ_get_bucket__mutmut_orig)
    xǁRateLimitMiddlewareǁ_get_bucket__mutmut_orig.__name__ = 'xǁRateLimitMiddlewareǁ_get_bucket'

    def xǁRateLimitMiddlewareǁ_cleanup_old_buckets__mutmut_orig(self):
        """
        Remove buckets that haven't been used recently

        Runs periodically to prevent memory leaks.
        Removes buckets that are full (indicating no recent activity).
        """
        # Only cleanup if we have many buckets
        if len(self.buckets) < 1000:
            return

        now = time.time()
        to_remove = []

        for identifier, bucket in self.buckets.items():
            # Remove if bucket is full and hasn't been used in 10 minutes
            if bucket.tokens >= bucket.capacity:
                elapsed = now - bucket.last_refill
                if elapsed > 600:  # 10 minutes
                    to_remove.append(identifier)

        for identifier in to_remove:
            del self.buckets[identifier]

        if to_remove:
            logger.info(
                "rate_limiter_cleaned_up_buckets",
                removed_count=len(to_remove),
                remaining_buckets=len(self.buckets),
            )

    def xǁRateLimitMiddlewareǁ_cleanup_old_buckets__mutmut_1(self):
        """
        Remove buckets that haven't been used recently

        Runs periodically to prevent memory leaks.
        Removes buckets that are full (indicating no recent activity).
        """
        # Only cleanup if we have many buckets
        if len(self.buckets) <= 1000:
            return

        now = time.time()
        to_remove = []

        for identifier, bucket in self.buckets.items():
            # Remove if bucket is full and hasn't been used in 10 minutes
            if bucket.tokens >= bucket.capacity:
                elapsed = now - bucket.last_refill
                if elapsed > 600:  # 10 minutes
                    to_remove.append(identifier)

        for identifier in to_remove:
            del self.buckets[identifier]

        if to_remove:
            logger.info(
                "rate_limiter_cleaned_up_buckets",
                removed_count=len(to_remove),
                remaining_buckets=len(self.buckets),
            )

    def xǁRateLimitMiddlewareǁ_cleanup_old_buckets__mutmut_2(self):
        """
        Remove buckets that haven't been used recently

        Runs periodically to prevent memory leaks.
        Removes buckets that are full (indicating no recent activity).
        """
        # Only cleanup if we have many buckets
        if len(self.buckets) < 1001:
            return

        now = time.time()
        to_remove = []

        for identifier, bucket in self.buckets.items():
            # Remove if bucket is full and hasn't been used in 10 minutes
            if bucket.tokens >= bucket.capacity:
                elapsed = now - bucket.last_refill
                if elapsed > 600:  # 10 minutes
                    to_remove.append(identifier)

        for identifier in to_remove:
            del self.buckets[identifier]

        if to_remove:
            logger.info(
                "rate_limiter_cleaned_up_buckets",
                removed_count=len(to_remove),
                remaining_buckets=len(self.buckets),
            )

    def xǁRateLimitMiddlewareǁ_cleanup_old_buckets__mutmut_3(self):
        """
        Remove buckets that haven't been used recently

        Runs periodically to prevent memory leaks.
        Removes buckets that are full (indicating no recent activity).
        """
        # Only cleanup if we have many buckets
        if len(self.buckets) < 1000:
            return

        now = None
        to_remove = []

        for identifier, bucket in self.buckets.items():
            # Remove if bucket is full and hasn't been used in 10 minutes
            if bucket.tokens >= bucket.capacity:
                elapsed = now - bucket.last_refill
                if elapsed > 600:  # 10 minutes
                    to_remove.append(identifier)

        for identifier in to_remove:
            del self.buckets[identifier]

        if to_remove:
            logger.info(
                "rate_limiter_cleaned_up_buckets",
                removed_count=len(to_remove),
                remaining_buckets=len(self.buckets),
            )

    def xǁRateLimitMiddlewareǁ_cleanup_old_buckets__mutmut_4(self):
        """
        Remove buckets that haven't been used recently

        Runs periodically to prevent memory leaks.
        Removes buckets that are full (indicating no recent activity).
        """
        # Only cleanup if we have many buckets
        if len(self.buckets) < 1000:
            return

        now = time.time()
        to_remove = None

        for identifier, bucket in self.buckets.items():
            # Remove if bucket is full and hasn't been used in 10 minutes
            if bucket.tokens >= bucket.capacity:
                elapsed = now - bucket.last_refill
                if elapsed > 600:  # 10 minutes
                    to_remove.append(identifier)

        for identifier in to_remove:
            del self.buckets[identifier]

        if to_remove:
            logger.info(
                "rate_limiter_cleaned_up_buckets",
                removed_count=len(to_remove),
                remaining_buckets=len(self.buckets),
            )

    def xǁRateLimitMiddlewareǁ_cleanup_old_buckets__mutmut_5(self):
        """
        Remove buckets that haven't been used recently

        Runs periodically to prevent memory leaks.
        Removes buckets that are full (indicating no recent activity).
        """
        # Only cleanup if we have many buckets
        if len(self.buckets) < 1000:
            return

        now = time.time()
        to_remove = []

        for identifier, bucket in self.buckets.items():
            # Remove if bucket is full and hasn't been used in 10 minutes
            if bucket.tokens > bucket.capacity:
                elapsed = now - bucket.last_refill
                if elapsed > 600:  # 10 minutes
                    to_remove.append(identifier)

        for identifier in to_remove:
            del self.buckets[identifier]

        if to_remove:
            logger.info(
                "rate_limiter_cleaned_up_buckets",
                removed_count=len(to_remove),
                remaining_buckets=len(self.buckets),
            )

    def xǁRateLimitMiddlewareǁ_cleanup_old_buckets__mutmut_6(self):
        """
        Remove buckets that haven't been used recently

        Runs periodically to prevent memory leaks.
        Removes buckets that are full (indicating no recent activity).
        """
        # Only cleanup if we have many buckets
        if len(self.buckets) < 1000:
            return

        now = time.time()
        to_remove = []

        for identifier, bucket in self.buckets.items():
            # Remove if bucket is full and hasn't been used in 10 minutes
            if bucket.tokens >= bucket.capacity:
                elapsed = None
                if elapsed > 600:  # 10 minutes
                    to_remove.append(identifier)

        for identifier in to_remove:
            del self.buckets[identifier]

        if to_remove:
            logger.info(
                "rate_limiter_cleaned_up_buckets",
                removed_count=len(to_remove),
                remaining_buckets=len(self.buckets),
            )

    def xǁRateLimitMiddlewareǁ_cleanup_old_buckets__mutmut_7(self):
        """
        Remove buckets that haven't been used recently

        Runs periodically to prevent memory leaks.
        Removes buckets that are full (indicating no recent activity).
        """
        # Only cleanup if we have many buckets
        if len(self.buckets) < 1000:
            return

        now = time.time()
        to_remove = []

        for identifier, bucket in self.buckets.items():
            # Remove if bucket is full and hasn't been used in 10 minutes
            if bucket.tokens >= bucket.capacity:
                elapsed = now + bucket.last_refill
                if elapsed > 600:  # 10 minutes
                    to_remove.append(identifier)

        for identifier in to_remove:
            del self.buckets[identifier]

        if to_remove:
            logger.info(
                "rate_limiter_cleaned_up_buckets",
                removed_count=len(to_remove),
                remaining_buckets=len(self.buckets),
            )

    def xǁRateLimitMiddlewareǁ_cleanup_old_buckets__mutmut_8(self):
        """
        Remove buckets that haven't been used recently

        Runs periodically to prevent memory leaks.
        Removes buckets that are full (indicating no recent activity).
        """
        # Only cleanup if we have many buckets
        if len(self.buckets) < 1000:
            return

        now = time.time()
        to_remove = []

        for identifier, bucket in self.buckets.items():
            # Remove if bucket is full and hasn't been used in 10 minutes
            if bucket.tokens >= bucket.capacity:
                elapsed = now - bucket.last_refill
                if elapsed >= 600:  # 10 minutes
                    to_remove.append(identifier)

        for identifier in to_remove:
            del self.buckets[identifier]

        if to_remove:
            logger.info(
                "rate_limiter_cleaned_up_buckets",
                removed_count=len(to_remove),
                remaining_buckets=len(self.buckets),
            )

    def xǁRateLimitMiddlewareǁ_cleanup_old_buckets__mutmut_9(self):
        """
        Remove buckets that haven't been used recently

        Runs periodically to prevent memory leaks.
        Removes buckets that are full (indicating no recent activity).
        """
        # Only cleanup if we have many buckets
        if len(self.buckets) < 1000:
            return

        now = time.time()
        to_remove = []

        for identifier, bucket in self.buckets.items():
            # Remove if bucket is full and hasn't been used in 10 minutes
            if bucket.tokens >= bucket.capacity:
                elapsed = now - bucket.last_refill
                if elapsed > 601:  # 10 minutes
                    to_remove.append(identifier)

        for identifier in to_remove:
            del self.buckets[identifier]

        if to_remove:
            logger.info(
                "rate_limiter_cleaned_up_buckets",
                removed_count=len(to_remove),
                remaining_buckets=len(self.buckets),
            )

    def xǁRateLimitMiddlewareǁ_cleanup_old_buckets__mutmut_10(self):
        """
        Remove buckets that haven't been used recently

        Runs periodically to prevent memory leaks.
        Removes buckets that are full (indicating no recent activity).
        """
        # Only cleanup if we have many buckets
        if len(self.buckets) < 1000:
            return

        now = time.time()
        to_remove = []

        for identifier, bucket in self.buckets.items():
            # Remove if bucket is full and hasn't been used in 10 minutes
            if bucket.tokens >= bucket.capacity:
                elapsed = now - bucket.last_refill
                if elapsed > 600:  # 10 minutes
                    to_remove.append(None)

        for identifier in to_remove:
            del self.buckets[identifier]

        if to_remove:
            logger.info(
                "rate_limiter_cleaned_up_buckets",
                removed_count=len(to_remove),
                remaining_buckets=len(self.buckets),
            )

    def xǁRateLimitMiddlewareǁ_cleanup_old_buckets__mutmut_11(self):
        """
        Remove buckets that haven't been used recently

        Runs periodically to prevent memory leaks.
        Removes buckets that are full (indicating no recent activity).
        """
        # Only cleanup if we have many buckets
        if len(self.buckets) < 1000:
            return

        now = time.time()
        to_remove = []

        for identifier, bucket in self.buckets.items():
            # Remove if bucket is full and hasn't been used in 10 minutes
            if bucket.tokens >= bucket.capacity:
                elapsed = now - bucket.last_refill
                if elapsed > 600:  # 10 minutes
                    to_remove.append(identifier)

        for identifier in to_remove:
            del self.buckets[identifier]

        if to_remove:
            logger.info(
                None,
                removed_count=len(to_remove),
                remaining_buckets=len(self.buckets),
            )

    def xǁRateLimitMiddlewareǁ_cleanup_old_buckets__mutmut_12(self):
        """
        Remove buckets that haven't been used recently

        Runs periodically to prevent memory leaks.
        Removes buckets that are full (indicating no recent activity).
        """
        # Only cleanup if we have many buckets
        if len(self.buckets) < 1000:
            return

        now = time.time()
        to_remove = []

        for identifier, bucket in self.buckets.items():
            # Remove if bucket is full and hasn't been used in 10 minutes
            if bucket.tokens >= bucket.capacity:
                elapsed = now - bucket.last_refill
                if elapsed > 600:  # 10 minutes
                    to_remove.append(identifier)

        for identifier in to_remove:
            del self.buckets[identifier]

        if to_remove:
            logger.info(
                "rate_limiter_cleaned_up_buckets",
                removed_count=None,
                remaining_buckets=len(self.buckets),
            )

    def xǁRateLimitMiddlewareǁ_cleanup_old_buckets__mutmut_13(self):
        """
        Remove buckets that haven't been used recently

        Runs periodically to prevent memory leaks.
        Removes buckets that are full (indicating no recent activity).
        """
        # Only cleanup if we have many buckets
        if len(self.buckets) < 1000:
            return

        now = time.time()
        to_remove = []

        for identifier, bucket in self.buckets.items():
            # Remove if bucket is full and hasn't been used in 10 minutes
            if bucket.tokens >= bucket.capacity:
                elapsed = now - bucket.last_refill
                if elapsed > 600:  # 10 minutes
                    to_remove.append(identifier)

        for identifier in to_remove:
            del self.buckets[identifier]

        if to_remove:
            logger.info(
                "rate_limiter_cleaned_up_buckets",
                removed_count=len(to_remove),
                remaining_buckets=None,
            )

    def xǁRateLimitMiddlewareǁ_cleanup_old_buckets__mutmut_14(self):
        """
        Remove buckets that haven't been used recently

        Runs periodically to prevent memory leaks.
        Removes buckets that are full (indicating no recent activity).
        """
        # Only cleanup if we have many buckets
        if len(self.buckets) < 1000:
            return

        now = time.time()
        to_remove = []

        for identifier, bucket in self.buckets.items():
            # Remove if bucket is full and hasn't been used in 10 minutes
            if bucket.tokens >= bucket.capacity:
                elapsed = now - bucket.last_refill
                if elapsed > 600:  # 10 minutes
                    to_remove.append(identifier)

        for identifier in to_remove:
            del self.buckets[identifier]

        if to_remove:
            logger.info(
                removed_count=len(to_remove),
                remaining_buckets=len(self.buckets),
            )

    def xǁRateLimitMiddlewareǁ_cleanup_old_buckets__mutmut_15(self):
        """
        Remove buckets that haven't been used recently

        Runs periodically to prevent memory leaks.
        Removes buckets that are full (indicating no recent activity).
        """
        # Only cleanup if we have many buckets
        if len(self.buckets) < 1000:
            return

        now = time.time()
        to_remove = []

        for identifier, bucket in self.buckets.items():
            # Remove if bucket is full and hasn't been used in 10 minutes
            if bucket.tokens >= bucket.capacity:
                elapsed = now - bucket.last_refill
                if elapsed > 600:  # 10 minutes
                    to_remove.append(identifier)

        for identifier in to_remove:
            del self.buckets[identifier]

        if to_remove:
            logger.info(
                "rate_limiter_cleaned_up_buckets",
                remaining_buckets=len(self.buckets),
            )

    def xǁRateLimitMiddlewareǁ_cleanup_old_buckets__mutmut_16(self):
        """
        Remove buckets that haven't been used recently

        Runs periodically to prevent memory leaks.
        Removes buckets that are full (indicating no recent activity).
        """
        # Only cleanup if we have many buckets
        if len(self.buckets) < 1000:
            return

        now = time.time()
        to_remove = []

        for identifier, bucket in self.buckets.items():
            # Remove if bucket is full and hasn't been used in 10 minutes
            if bucket.tokens >= bucket.capacity:
                elapsed = now - bucket.last_refill
                if elapsed > 600:  # 10 minutes
                    to_remove.append(identifier)

        for identifier in to_remove:
            del self.buckets[identifier]

        if to_remove:
            logger.info(
                "rate_limiter_cleaned_up_buckets",
                removed_count=len(to_remove),
                )

    def xǁRateLimitMiddlewareǁ_cleanup_old_buckets__mutmut_17(self):
        """
        Remove buckets that haven't been used recently

        Runs periodically to prevent memory leaks.
        Removes buckets that are full (indicating no recent activity).
        """
        # Only cleanup if we have many buckets
        if len(self.buckets) < 1000:
            return

        now = time.time()
        to_remove = []

        for identifier, bucket in self.buckets.items():
            # Remove if bucket is full and hasn't been used in 10 minutes
            if bucket.tokens >= bucket.capacity:
                elapsed = now - bucket.last_refill
                if elapsed > 600:  # 10 minutes
                    to_remove.append(identifier)

        for identifier in to_remove:
            del self.buckets[identifier]

        if to_remove:
            logger.info(
                "XXrate_limiter_cleaned_up_bucketsXX",
                removed_count=len(to_remove),
                remaining_buckets=len(self.buckets),
            )

    def xǁRateLimitMiddlewareǁ_cleanup_old_buckets__mutmut_18(self):
        """
        Remove buckets that haven't been used recently

        Runs periodically to prevent memory leaks.
        Removes buckets that are full (indicating no recent activity).
        """
        # Only cleanup if we have many buckets
        if len(self.buckets) < 1000:
            return

        now = time.time()
        to_remove = []

        for identifier, bucket in self.buckets.items():
            # Remove if bucket is full and hasn't been used in 10 minutes
            if bucket.tokens >= bucket.capacity:
                elapsed = now - bucket.last_refill
                if elapsed > 600:  # 10 minutes
                    to_remove.append(identifier)

        for identifier in to_remove:
            del self.buckets[identifier]

        if to_remove:
            logger.info(
                "RATE_LIMITER_CLEANED_UP_BUCKETS",
                removed_count=len(to_remove),
                remaining_buckets=len(self.buckets),
            )
    
    xǁRateLimitMiddlewareǁ_cleanup_old_buckets__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁRateLimitMiddlewareǁ_cleanup_old_buckets__mutmut_1': xǁRateLimitMiddlewareǁ_cleanup_old_buckets__mutmut_1, 
        'xǁRateLimitMiddlewareǁ_cleanup_old_buckets__mutmut_2': xǁRateLimitMiddlewareǁ_cleanup_old_buckets__mutmut_2, 
        'xǁRateLimitMiddlewareǁ_cleanup_old_buckets__mutmut_3': xǁRateLimitMiddlewareǁ_cleanup_old_buckets__mutmut_3, 
        'xǁRateLimitMiddlewareǁ_cleanup_old_buckets__mutmut_4': xǁRateLimitMiddlewareǁ_cleanup_old_buckets__mutmut_4, 
        'xǁRateLimitMiddlewareǁ_cleanup_old_buckets__mutmut_5': xǁRateLimitMiddlewareǁ_cleanup_old_buckets__mutmut_5, 
        'xǁRateLimitMiddlewareǁ_cleanup_old_buckets__mutmut_6': xǁRateLimitMiddlewareǁ_cleanup_old_buckets__mutmut_6, 
        'xǁRateLimitMiddlewareǁ_cleanup_old_buckets__mutmut_7': xǁRateLimitMiddlewareǁ_cleanup_old_buckets__mutmut_7, 
        'xǁRateLimitMiddlewareǁ_cleanup_old_buckets__mutmut_8': xǁRateLimitMiddlewareǁ_cleanup_old_buckets__mutmut_8, 
        'xǁRateLimitMiddlewareǁ_cleanup_old_buckets__mutmut_9': xǁRateLimitMiddlewareǁ_cleanup_old_buckets__mutmut_9, 
        'xǁRateLimitMiddlewareǁ_cleanup_old_buckets__mutmut_10': xǁRateLimitMiddlewareǁ_cleanup_old_buckets__mutmut_10, 
        'xǁRateLimitMiddlewareǁ_cleanup_old_buckets__mutmut_11': xǁRateLimitMiddlewareǁ_cleanup_old_buckets__mutmut_11, 
        'xǁRateLimitMiddlewareǁ_cleanup_old_buckets__mutmut_12': xǁRateLimitMiddlewareǁ_cleanup_old_buckets__mutmut_12, 
        'xǁRateLimitMiddlewareǁ_cleanup_old_buckets__mutmut_13': xǁRateLimitMiddlewareǁ_cleanup_old_buckets__mutmut_13, 
        'xǁRateLimitMiddlewareǁ_cleanup_old_buckets__mutmut_14': xǁRateLimitMiddlewareǁ_cleanup_old_buckets__mutmut_14, 
        'xǁRateLimitMiddlewareǁ_cleanup_old_buckets__mutmut_15': xǁRateLimitMiddlewareǁ_cleanup_old_buckets__mutmut_15, 
        'xǁRateLimitMiddlewareǁ_cleanup_old_buckets__mutmut_16': xǁRateLimitMiddlewareǁ_cleanup_old_buckets__mutmut_16, 
        'xǁRateLimitMiddlewareǁ_cleanup_old_buckets__mutmut_17': xǁRateLimitMiddlewareǁ_cleanup_old_buckets__mutmut_17, 
        'xǁRateLimitMiddlewareǁ_cleanup_old_buckets__mutmut_18': xǁRateLimitMiddlewareǁ_cleanup_old_buckets__mutmut_18
    }
    
    def _cleanup_old_buckets(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁRateLimitMiddlewareǁ_cleanup_old_buckets__mutmut_orig"), object.__getattribute__(self, "xǁRateLimitMiddlewareǁ_cleanup_old_buckets__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _cleanup_old_buckets.__signature__ = _mutmut_signature(xǁRateLimitMiddlewareǁ_cleanup_old_buckets__mutmut_orig)
    xǁRateLimitMiddlewareǁ_cleanup_old_buckets__mutmut_orig.__name__ = 'xǁRateLimitMiddlewareǁ_cleanup_old_buckets'

    async def xǁRateLimitMiddlewareǁdispatch__mutmut_orig(self, request: Request, call_next):
        """
        Process request with rate limiting

        Args:
            request: FastAPI request
            call_next: Next middleware in chain

        Returns:
            Response or 429 Too Many Requests
        """
        # Skip rate limiting for health checks
        if request.url.path in ["/health", "/", "/docs", "/redoc", "/openapi.json"]:
            return await call_next(request)

        # Get identifier and bucket
        identifier = self._get_identifier(request)
        bucket = self._get_bucket(identifier)

        # Try to consume token
        if bucket.consume():
            # Request allowed
            remaining = int(bucket.tokens)
            reset_seconds = int(bucket.capacity / bucket.refill_rate)

            logger.debug(
                "rate_limit_allowed",
                identifier=identifier,
                remaining=remaining,
                path=request.url.path,
            )

            # Process request
            response = await call_next(request)

            # Add rate limit headers
            response.headers["X-RateLimit-Limit"] = str(self.requests_per_minute)
            response.headers["X-RateLimit-Remaining"] = str(remaining)
            response.headers["X-RateLimit-Reset"] = str(reset_seconds)

            # Periodic cleanup
            self._cleanup_old_buckets()

            return response
        else:
            # Rate limit exceeded
            wait_time = bucket.get_wait_time()
            retry_after = int(wait_time) + 1  # Round up

            logger.warning(
                "rate_limit_exceeded",
                identifier=identifier,
                path=request.url.path,
                wait_time_seconds=retry_after,
            )

            # Return 429 Too Many Requests
            return JSONResponse(
                status_code=429,
                content={
                    "error": "Rate limit exceeded",
                    "message": f"Too many requests. Please retry after {retry_after} seconds.",
                    "retry_after": retry_after,
                    "limit": self.requests_per_minute,
                },
                headers={
                    "X-RateLimit-Limit": str(self.requests_per_minute),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(retry_after),
                    "Retry-After": str(retry_after),
                },
            )

    async def xǁRateLimitMiddlewareǁdispatch__mutmut_1(self, request: Request, call_next):
        """
        Process request with rate limiting

        Args:
            request: FastAPI request
            call_next: Next middleware in chain

        Returns:
            Response or 429 Too Many Requests
        """
        # Skip rate limiting for health checks
        if request.url.path not in ["/health", "/", "/docs", "/redoc", "/openapi.json"]:
            return await call_next(request)

        # Get identifier and bucket
        identifier = self._get_identifier(request)
        bucket = self._get_bucket(identifier)

        # Try to consume token
        if bucket.consume():
            # Request allowed
            remaining = int(bucket.tokens)
            reset_seconds = int(bucket.capacity / bucket.refill_rate)

            logger.debug(
                "rate_limit_allowed",
                identifier=identifier,
                remaining=remaining,
                path=request.url.path,
            )

            # Process request
            response = await call_next(request)

            # Add rate limit headers
            response.headers["X-RateLimit-Limit"] = str(self.requests_per_minute)
            response.headers["X-RateLimit-Remaining"] = str(remaining)
            response.headers["X-RateLimit-Reset"] = str(reset_seconds)

            # Periodic cleanup
            self._cleanup_old_buckets()

            return response
        else:
            # Rate limit exceeded
            wait_time = bucket.get_wait_time()
            retry_after = int(wait_time) + 1  # Round up

            logger.warning(
                "rate_limit_exceeded",
                identifier=identifier,
                path=request.url.path,
                wait_time_seconds=retry_after,
            )

            # Return 429 Too Many Requests
            return JSONResponse(
                status_code=429,
                content={
                    "error": "Rate limit exceeded",
                    "message": f"Too many requests. Please retry after {retry_after} seconds.",
                    "retry_after": retry_after,
                    "limit": self.requests_per_minute,
                },
                headers={
                    "X-RateLimit-Limit": str(self.requests_per_minute),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(retry_after),
                    "Retry-After": str(retry_after),
                },
            )

    async def xǁRateLimitMiddlewareǁdispatch__mutmut_2(self, request: Request, call_next):
        """
        Process request with rate limiting

        Args:
            request: FastAPI request
            call_next: Next middleware in chain

        Returns:
            Response or 429 Too Many Requests
        """
        # Skip rate limiting for health checks
        if request.url.path in ["XX/healthXX", "/", "/docs", "/redoc", "/openapi.json"]:
            return await call_next(request)

        # Get identifier and bucket
        identifier = self._get_identifier(request)
        bucket = self._get_bucket(identifier)

        # Try to consume token
        if bucket.consume():
            # Request allowed
            remaining = int(bucket.tokens)
            reset_seconds = int(bucket.capacity / bucket.refill_rate)

            logger.debug(
                "rate_limit_allowed",
                identifier=identifier,
                remaining=remaining,
                path=request.url.path,
            )

            # Process request
            response = await call_next(request)

            # Add rate limit headers
            response.headers["X-RateLimit-Limit"] = str(self.requests_per_minute)
            response.headers["X-RateLimit-Remaining"] = str(remaining)
            response.headers["X-RateLimit-Reset"] = str(reset_seconds)

            # Periodic cleanup
            self._cleanup_old_buckets()

            return response
        else:
            # Rate limit exceeded
            wait_time = bucket.get_wait_time()
            retry_after = int(wait_time) + 1  # Round up

            logger.warning(
                "rate_limit_exceeded",
                identifier=identifier,
                path=request.url.path,
                wait_time_seconds=retry_after,
            )

            # Return 429 Too Many Requests
            return JSONResponse(
                status_code=429,
                content={
                    "error": "Rate limit exceeded",
                    "message": f"Too many requests. Please retry after {retry_after} seconds.",
                    "retry_after": retry_after,
                    "limit": self.requests_per_minute,
                },
                headers={
                    "X-RateLimit-Limit": str(self.requests_per_minute),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(retry_after),
                    "Retry-After": str(retry_after),
                },
            )

    async def xǁRateLimitMiddlewareǁdispatch__mutmut_3(self, request: Request, call_next):
        """
        Process request with rate limiting

        Args:
            request: FastAPI request
            call_next: Next middleware in chain

        Returns:
            Response or 429 Too Many Requests
        """
        # Skip rate limiting for health checks
        if request.url.path in ["/HEALTH", "/", "/docs", "/redoc", "/openapi.json"]:
            return await call_next(request)

        # Get identifier and bucket
        identifier = self._get_identifier(request)
        bucket = self._get_bucket(identifier)

        # Try to consume token
        if bucket.consume():
            # Request allowed
            remaining = int(bucket.tokens)
            reset_seconds = int(bucket.capacity / bucket.refill_rate)

            logger.debug(
                "rate_limit_allowed",
                identifier=identifier,
                remaining=remaining,
                path=request.url.path,
            )

            # Process request
            response = await call_next(request)

            # Add rate limit headers
            response.headers["X-RateLimit-Limit"] = str(self.requests_per_minute)
            response.headers["X-RateLimit-Remaining"] = str(remaining)
            response.headers["X-RateLimit-Reset"] = str(reset_seconds)

            # Periodic cleanup
            self._cleanup_old_buckets()

            return response
        else:
            # Rate limit exceeded
            wait_time = bucket.get_wait_time()
            retry_after = int(wait_time) + 1  # Round up

            logger.warning(
                "rate_limit_exceeded",
                identifier=identifier,
                path=request.url.path,
                wait_time_seconds=retry_after,
            )

            # Return 429 Too Many Requests
            return JSONResponse(
                status_code=429,
                content={
                    "error": "Rate limit exceeded",
                    "message": f"Too many requests. Please retry after {retry_after} seconds.",
                    "retry_after": retry_after,
                    "limit": self.requests_per_minute,
                },
                headers={
                    "X-RateLimit-Limit": str(self.requests_per_minute),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(retry_after),
                    "Retry-After": str(retry_after),
                },
            )

    async def xǁRateLimitMiddlewareǁdispatch__mutmut_4(self, request: Request, call_next):
        """
        Process request with rate limiting

        Args:
            request: FastAPI request
            call_next: Next middleware in chain

        Returns:
            Response or 429 Too Many Requests
        """
        # Skip rate limiting for health checks
        if request.url.path in ["/health", "XX/XX", "/docs", "/redoc", "/openapi.json"]:
            return await call_next(request)

        # Get identifier and bucket
        identifier = self._get_identifier(request)
        bucket = self._get_bucket(identifier)

        # Try to consume token
        if bucket.consume():
            # Request allowed
            remaining = int(bucket.tokens)
            reset_seconds = int(bucket.capacity / bucket.refill_rate)

            logger.debug(
                "rate_limit_allowed",
                identifier=identifier,
                remaining=remaining,
                path=request.url.path,
            )

            # Process request
            response = await call_next(request)

            # Add rate limit headers
            response.headers["X-RateLimit-Limit"] = str(self.requests_per_minute)
            response.headers["X-RateLimit-Remaining"] = str(remaining)
            response.headers["X-RateLimit-Reset"] = str(reset_seconds)

            # Periodic cleanup
            self._cleanup_old_buckets()

            return response
        else:
            # Rate limit exceeded
            wait_time = bucket.get_wait_time()
            retry_after = int(wait_time) + 1  # Round up

            logger.warning(
                "rate_limit_exceeded",
                identifier=identifier,
                path=request.url.path,
                wait_time_seconds=retry_after,
            )

            # Return 429 Too Many Requests
            return JSONResponse(
                status_code=429,
                content={
                    "error": "Rate limit exceeded",
                    "message": f"Too many requests. Please retry after {retry_after} seconds.",
                    "retry_after": retry_after,
                    "limit": self.requests_per_minute,
                },
                headers={
                    "X-RateLimit-Limit": str(self.requests_per_minute),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(retry_after),
                    "Retry-After": str(retry_after),
                },
            )

    async def xǁRateLimitMiddlewareǁdispatch__mutmut_5(self, request: Request, call_next):
        """
        Process request with rate limiting

        Args:
            request: FastAPI request
            call_next: Next middleware in chain

        Returns:
            Response or 429 Too Many Requests
        """
        # Skip rate limiting for health checks
        if request.url.path in ["/health", "/", "XX/docsXX", "/redoc", "/openapi.json"]:
            return await call_next(request)

        # Get identifier and bucket
        identifier = self._get_identifier(request)
        bucket = self._get_bucket(identifier)

        # Try to consume token
        if bucket.consume():
            # Request allowed
            remaining = int(bucket.tokens)
            reset_seconds = int(bucket.capacity / bucket.refill_rate)

            logger.debug(
                "rate_limit_allowed",
                identifier=identifier,
                remaining=remaining,
                path=request.url.path,
            )

            # Process request
            response = await call_next(request)

            # Add rate limit headers
            response.headers["X-RateLimit-Limit"] = str(self.requests_per_minute)
            response.headers["X-RateLimit-Remaining"] = str(remaining)
            response.headers["X-RateLimit-Reset"] = str(reset_seconds)

            # Periodic cleanup
            self._cleanup_old_buckets()

            return response
        else:
            # Rate limit exceeded
            wait_time = bucket.get_wait_time()
            retry_after = int(wait_time) + 1  # Round up

            logger.warning(
                "rate_limit_exceeded",
                identifier=identifier,
                path=request.url.path,
                wait_time_seconds=retry_after,
            )

            # Return 429 Too Many Requests
            return JSONResponse(
                status_code=429,
                content={
                    "error": "Rate limit exceeded",
                    "message": f"Too many requests. Please retry after {retry_after} seconds.",
                    "retry_after": retry_after,
                    "limit": self.requests_per_minute,
                },
                headers={
                    "X-RateLimit-Limit": str(self.requests_per_minute),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(retry_after),
                    "Retry-After": str(retry_after),
                },
            )

    async def xǁRateLimitMiddlewareǁdispatch__mutmut_6(self, request: Request, call_next):
        """
        Process request with rate limiting

        Args:
            request: FastAPI request
            call_next: Next middleware in chain

        Returns:
            Response or 429 Too Many Requests
        """
        # Skip rate limiting for health checks
        if request.url.path in ["/health", "/", "/DOCS", "/redoc", "/openapi.json"]:
            return await call_next(request)

        # Get identifier and bucket
        identifier = self._get_identifier(request)
        bucket = self._get_bucket(identifier)

        # Try to consume token
        if bucket.consume():
            # Request allowed
            remaining = int(bucket.tokens)
            reset_seconds = int(bucket.capacity / bucket.refill_rate)

            logger.debug(
                "rate_limit_allowed",
                identifier=identifier,
                remaining=remaining,
                path=request.url.path,
            )

            # Process request
            response = await call_next(request)

            # Add rate limit headers
            response.headers["X-RateLimit-Limit"] = str(self.requests_per_minute)
            response.headers["X-RateLimit-Remaining"] = str(remaining)
            response.headers["X-RateLimit-Reset"] = str(reset_seconds)

            # Periodic cleanup
            self._cleanup_old_buckets()

            return response
        else:
            # Rate limit exceeded
            wait_time = bucket.get_wait_time()
            retry_after = int(wait_time) + 1  # Round up

            logger.warning(
                "rate_limit_exceeded",
                identifier=identifier,
                path=request.url.path,
                wait_time_seconds=retry_after,
            )

            # Return 429 Too Many Requests
            return JSONResponse(
                status_code=429,
                content={
                    "error": "Rate limit exceeded",
                    "message": f"Too many requests. Please retry after {retry_after} seconds.",
                    "retry_after": retry_after,
                    "limit": self.requests_per_minute,
                },
                headers={
                    "X-RateLimit-Limit": str(self.requests_per_minute),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(retry_after),
                    "Retry-After": str(retry_after),
                },
            )

    async def xǁRateLimitMiddlewareǁdispatch__mutmut_7(self, request: Request, call_next):
        """
        Process request with rate limiting

        Args:
            request: FastAPI request
            call_next: Next middleware in chain

        Returns:
            Response or 429 Too Many Requests
        """
        # Skip rate limiting for health checks
        if request.url.path in ["/health", "/", "/docs", "XX/redocXX", "/openapi.json"]:
            return await call_next(request)

        # Get identifier and bucket
        identifier = self._get_identifier(request)
        bucket = self._get_bucket(identifier)

        # Try to consume token
        if bucket.consume():
            # Request allowed
            remaining = int(bucket.tokens)
            reset_seconds = int(bucket.capacity / bucket.refill_rate)

            logger.debug(
                "rate_limit_allowed",
                identifier=identifier,
                remaining=remaining,
                path=request.url.path,
            )

            # Process request
            response = await call_next(request)

            # Add rate limit headers
            response.headers["X-RateLimit-Limit"] = str(self.requests_per_minute)
            response.headers["X-RateLimit-Remaining"] = str(remaining)
            response.headers["X-RateLimit-Reset"] = str(reset_seconds)

            # Periodic cleanup
            self._cleanup_old_buckets()

            return response
        else:
            # Rate limit exceeded
            wait_time = bucket.get_wait_time()
            retry_after = int(wait_time) + 1  # Round up

            logger.warning(
                "rate_limit_exceeded",
                identifier=identifier,
                path=request.url.path,
                wait_time_seconds=retry_after,
            )

            # Return 429 Too Many Requests
            return JSONResponse(
                status_code=429,
                content={
                    "error": "Rate limit exceeded",
                    "message": f"Too many requests. Please retry after {retry_after} seconds.",
                    "retry_after": retry_after,
                    "limit": self.requests_per_minute,
                },
                headers={
                    "X-RateLimit-Limit": str(self.requests_per_minute),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(retry_after),
                    "Retry-After": str(retry_after),
                },
            )

    async def xǁRateLimitMiddlewareǁdispatch__mutmut_8(self, request: Request, call_next):
        """
        Process request with rate limiting

        Args:
            request: FastAPI request
            call_next: Next middleware in chain

        Returns:
            Response or 429 Too Many Requests
        """
        # Skip rate limiting for health checks
        if request.url.path in ["/health", "/", "/docs", "/REDOC", "/openapi.json"]:
            return await call_next(request)

        # Get identifier and bucket
        identifier = self._get_identifier(request)
        bucket = self._get_bucket(identifier)

        # Try to consume token
        if bucket.consume():
            # Request allowed
            remaining = int(bucket.tokens)
            reset_seconds = int(bucket.capacity / bucket.refill_rate)

            logger.debug(
                "rate_limit_allowed",
                identifier=identifier,
                remaining=remaining,
                path=request.url.path,
            )

            # Process request
            response = await call_next(request)

            # Add rate limit headers
            response.headers["X-RateLimit-Limit"] = str(self.requests_per_minute)
            response.headers["X-RateLimit-Remaining"] = str(remaining)
            response.headers["X-RateLimit-Reset"] = str(reset_seconds)

            # Periodic cleanup
            self._cleanup_old_buckets()

            return response
        else:
            # Rate limit exceeded
            wait_time = bucket.get_wait_time()
            retry_after = int(wait_time) + 1  # Round up

            logger.warning(
                "rate_limit_exceeded",
                identifier=identifier,
                path=request.url.path,
                wait_time_seconds=retry_after,
            )

            # Return 429 Too Many Requests
            return JSONResponse(
                status_code=429,
                content={
                    "error": "Rate limit exceeded",
                    "message": f"Too many requests. Please retry after {retry_after} seconds.",
                    "retry_after": retry_after,
                    "limit": self.requests_per_minute,
                },
                headers={
                    "X-RateLimit-Limit": str(self.requests_per_minute),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(retry_after),
                    "Retry-After": str(retry_after),
                },
            )

    async def xǁRateLimitMiddlewareǁdispatch__mutmut_9(self, request: Request, call_next):
        """
        Process request with rate limiting

        Args:
            request: FastAPI request
            call_next: Next middleware in chain

        Returns:
            Response or 429 Too Many Requests
        """
        # Skip rate limiting for health checks
        if request.url.path in ["/health", "/", "/docs", "/redoc", "XX/openapi.jsonXX"]:
            return await call_next(request)

        # Get identifier and bucket
        identifier = self._get_identifier(request)
        bucket = self._get_bucket(identifier)

        # Try to consume token
        if bucket.consume():
            # Request allowed
            remaining = int(bucket.tokens)
            reset_seconds = int(bucket.capacity / bucket.refill_rate)

            logger.debug(
                "rate_limit_allowed",
                identifier=identifier,
                remaining=remaining,
                path=request.url.path,
            )

            # Process request
            response = await call_next(request)

            # Add rate limit headers
            response.headers["X-RateLimit-Limit"] = str(self.requests_per_minute)
            response.headers["X-RateLimit-Remaining"] = str(remaining)
            response.headers["X-RateLimit-Reset"] = str(reset_seconds)

            # Periodic cleanup
            self._cleanup_old_buckets()

            return response
        else:
            # Rate limit exceeded
            wait_time = bucket.get_wait_time()
            retry_after = int(wait_time) + 1  # Round up

            logger.warning(
                "rate_limit_exceeded",
                identifier=identifier,
                path=request.url.path,
                wait_time_seconds=retry_after,
            )

            # Return 429 Too Many Requests
            return JSONResponse(
                status_code=429,
                content={
                    "error": "Rate limit exceeded",
                    "message": f"Too many requests. Please retry after {retry_after} seconds.",
                    "retry_after": retry_after,
                    "limit": self.requests_per_minute,
                },
                headers={
                    "X-RateLimit-Limit": str(self.requests_per_minute),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(retry_after),
                    "Retry-After": str(retry_after),
                },
            )

    async def xǁRateLimitMiddlewareǁdispatch__mutmut_10(self, request: Request, call_next):
        """
        Process request with rate limiting

        Args:
            request: FastAPI request
            call_next: Next middleware in chain

        Returns:
            Response or 429 Too Many Requests
        """
        # Skip rate limiting for health checks
        if request.url.path in ["/health", "/", "/docs", "/redoc", "/OPENAPI.JSON"]:
            return await call_next(request)

        # Get identifier and bucket
        identifier = self._get_identifier(request)
        bucket = self._get_bucket(identifier)

        # Try to consume token
        if bucket.consume():
            # Request allowed
            remaining = int(bucket.tokens)
            reset_seconds = int(bucket.capacity / bucket.refill_rate)

            logger.debug(
                "rate_limit_allowed",
                identifier=identifier,
                remaining=remaining,
                path=request.url.path,
            )

            # Process request
            response = await call_next(request)

            # Add rate limit headers
            response.headers["X-RateLimit-Limit"] = str(self.requests_per_minute)
            response.headers["X-RateLimit-Remaining"] = str(remaining)
            response.headers["X-RateLimit-Reset"] = str(reset_seconds)

            # Periodic cleanup
            self._cleanup_old_buckets()

            return response
        else:
            # Rate limit exceeded
            wait_time = bucket.get_wait_time()
            retry_after = int(wait_time) + 1  # Round up

            logger.warning(
                "rate_limit_exceeded",
                identifier=identifier,
                path=request.url.path,
                wait_time_seconds=retry_after,
            )

            # Return 429 Too Many Requests
            return JSONResponse(
                status_code=429,
                content={
                    "error": "Rate limit exceeded",
                    "message": f"Too many requests. Please retry after {retry_after} seconds.",
                    "retry_after": retry_after,
                    "limit": self.requests_per_minute,
                },
                headers={
                    "X-RateLimit-Limit": str(self.requests_per_minute),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(retry_after),
                    "Retry-After": str(retry_after),
                },
            )

    async def xǁRateLimitMiddlewareǁdispatch__mutmut_11(self, request: Request, call_next):
        """
        Process request with rate limiting

        Args:
            request: FastAPI request
            call_next: Next middleware in chain

        Returns:
            Response or 429 Too Many Requests
        """
        # Skip rate limiting for health checks
        if request.url.path in ["/health", "/", "/docs", "/redoc", "/openapi.json"]:
            return await call_next(None)

        # Get identifier and bucket
        identifier = self._get_identifier(request)
        bucket = self._get_bucket(identifier)

        # Try to consume token
        if bucket.consume():
            # Request allowed
            remaining = int(bucket.tokens)
            reset_seconds = int(bucket.capacity / bucket.refill_rate)

            logger.debug(
                "rate_limit_allowed",
                identifier=identifier,
                remaining=remaining,
                path=request.url.path,
            )

            # Process request
            response = await call_next(request)

            # Add rate limit headers
            response.headers["X-RateLimit-Limit"] = str(self.requests_per_minute)
            response.headers["X-RateLimit-Remaining"] = str(remaining)
            response.headers["X-RateLimit-Reset"] = str(reset_seconds)

            # Periodic cleanup
            self._cleanup_old_buckets()

            return response
        else:
            # Rate limit exceeded
            wait_time = bucket.get_wait_time()
            retry_after = int(wait_time) + 1  # Round up

            logger.warning(
                "rate_limit_exceeded",
                identifier=identifier,
                path=request.url.path,
                wait_time_seconds=retry_after,
            )

            # Return 429 Too Many Requests
            return JSONResponse(
                status_code=429,
                content={
                    "error": "Rate limit exceeded",
                    "message": f"Too many requests. Please retry after {retry_after} seconds.",
                    "retry_after": retry_after,
                    "limit": self.requests_per_minute,
                },
                headers={
                    "X-RateLimit-Limit": str(self.requests_per_minute),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(retry_after),
                    "Retry-After": str(retry_after),
                },
            )

    async def xǁRateLimitMiddlewareǁdispatch__mutmut_12(self, request: Request, call_next):
        """
        Process request with rate limiting

        Args:
            request: FastAPI request
            call_next: Next middleware in chain

        Returns:
            Response or 429 Too Many Requests
        """
        # Skip rate limiting for health checks
        if request.url.path in ["/health", "/", "/docs", "/redoc", "/openapi.json"]:
            return await call_next(request)

        # Get identifier and bucket
        identifier = None
        bucket = self._get_bucket(identifier)

        # Try to consume token
        if bucket.consume():
            # Request allowed
            remaining = int(bucket.tokens)
            reset_seconds = int(bucket.capacity / bucket.refill_rate)

            logger.debug(
                "rate_limit_allowed",
                identifier=identifier,
                remaining=remaining,
                path=request.url.path,
            )

            # Process request
            response = await call_next(request)

            # Add rate limit headers
            response.headers["X-RateLimit-Limit"] = str(self.requests_per_minute)
            response.headers["X-RateLimit-Remaining"] = str(remaining)
            response.headers["X-RateLimit-Reset"] = str(reset_seconds)

            # Periodic cleanup
            self._cleanup_old_buckets()

            return response
        else:
            # Rate limit exceeded
            wait_time = bucket.get_wait_time()
            retry_after = int(wait_time) + 1  # Round up

            logger.warning(
                "rate_limit_exceeded",
                identifier=identifier,
                path=request.url.path,
                wait_time_seconds=retry_after,
            )

            # Return 429 Too Many Requests
            return JSONResponse(
                status_code=429,
                content={
                    "error": "Rate limit exceeded",
                    "message": f"Too many requests. Please retry after {retry_after} seconds.",
                    "retry_after": retry_after,
                    "limit": self.requests_per_minute,
                },
                headers={
                    "X-RateLimit-Limit": str(self.requests_per_minute),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(retry_after),
                    "Retry-After": str(retry_after),
                },
            )

    async def xǁRateLimitMiddlewareǁdispatch__mutmut_13(self, request: Request, call_next):
        """
        Process request with rate limiting

        Args:
            request: FastAPI request
            call_next: Next middleware in chain

        Returns:
            Response or 429 Too Many Requests
        """
        # Skip rate limiting for health checks
        if request.url.path in ["/health", "/", "/docs", "/redoc", "/openapi.json"]:
            return await call_next(request)

        # Get identifier and bucket
        identifier = self._get_identifier(None)
        bucket = self._get_bucket(identifier)

        # Try to consume token
        if bucket.consume():
            # Request allowed
            remaining = int(bucket.tokens)
            reset_seconds = int(bucket.capacity / bucket.refill_rate)

            logger.debug(
                "rate_limit_allowed",
                identifier=identifier,
                remaining=remaining,
                path=request.url.path,
            )

            # Process request
            response = await call_next(request)

            # Add rate limit headers
            response.headers["X-RateLimit-Limit"] = str(self.requests_per_minute)
            response.headers["X-RateLimit-Remaining"] = str(remaining)
            response.headers["X-RateLimit-Reset"] = str(reset_seconds)

            # Periodic cleanup
            self._cleanup_old_buckets()

            return response
        else:
            # Rate limit exceeded
            wait_time = bucket.get_wait_time()
            retry_after = int(wait_time) + 1  # Round up

            logger.warning(
                "rate_limit_exceeded",
                identifier=identifier,
                path=request.url.path,
                wait_time_seconds=retry_after,
            )

            # Return 429 Too Many Requests
            return JSONResponse(
                status_code=429,
                content={
                    "error": "Rate limit exceeded",
                    "message": f"Too many requests. Please retry after {retry_after} seconds.",
                    "retry_after": retry_after,
                    "limit": self.requests_per_minute,
                },
                headers={
                    "X-RateLimit-Limit": str(self.requests_per_minute),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(retry_after),
                    "Retry-After": str(retry_after),
                },
            )

    async def xǁRateLimitMiddlewareǁdispatch__mutmut_14(self, request: Request, call_next):
        """
        Process request with rate limiting

        Args:
            request: FastAPI request
            call_next: Next middleware in chain

        Returns:
            Response or 429 Too Many Requests
        """
        # Skip rate limiting for health checks
        if request.url.path in ["/health", "/", "/docs", "/redoc", "/openapi.json"]:
            return await call_next(request)

        # Get identifier and bucket
        identifier = self._get_identifier(request)
        bucket = None

        # Try to consume token
        if bucket.consume():
            # Request allowed
            remaining = int(bucket.tokens)
            reset_seconds = int(bucket.capacity / bucket.refill_rate)

            logger.debug(
                "rate_limit_allowed",
                identifier=identifier,
                remaining=remaining,
                path=request.url.path,
            )

            # Process request
            response = await call_next(request)

            # Add rate limit headers
            response.headers["X-RateLimit-Limit"] = str(self.requests_per_minute)
            response.headers["X-RateLimit-Remaining"] = str(remaining)
            response.headers["X-RateLimit-Reset"] = str(reset_seconds)

            # Periodic cleanup
            self._cleanup_old_buckets()

            return response
        else:
            # Rate limit exceeded
            wait_time = bucket.get_wait_time()
            retry_after = int(wait_time) + 1  # Round up

            logger.warning(
                "rate_limit_exceeded",
                identifier=identifier,
                path=request.url.path,
                wait_time_seconds=retry_after,
            )

            # Return 429 Too Many Requests
            return JSONResponse(
                status_code=429,
                content={
                    "error": "Rate limit exceeded",
                    "message": f"Too many requests. Please retry after {retry_after} seconds.",
                    "retry_after": retry_after,
                    "limit": self.requests_per_minute,
                },
                headers={
                    "X-RateLimit-Limit": str(self.requests_per_minute),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(retry_after),
                    "Retry-After": str(retry_after),
                },
            )

    async def xǁRateLimitMiddlewareǁdispatch__mutmut_15(self, request: Request, call_next):
        """
        Process request with rate limiting

        Args:
            request: FastAPI request
            call_next: Next middleware in chain

        Returns:
            Response or 429 Too Many Requests
        """
        # Skip rate limiting for health checks
        if request.url.path in ["/health", "/", "/docs", "/redoc", "/openapi.json"]:
            return await call_next(request)

        # Get identifier and bucket
        identifier = self._get_identifier(request)
        bucket = self._get_bucket(None)

        # Try to consume token
        if bucket.consume():
            # Request allowed
            remaining = int(bucket.tokens)
            reset_seconds = int(bucket.capacity / bucket.refill_rate)

            logger.debug(
                "rate_limit_allowed",
                identifier=identifier,
                remaining=remaining,
                path=request.url.path,
            )

            # Process request
            response = await call_next(request)

            # Add rate limit headers
            response.headers["X-RateLimit-Limit"] = str(self.requests_per_minute)
            response.headers["X-RateLimit-Remaining"] = str(remaining)
            response.headers["X-RateLimit-Reset"] = str(reset_seconds)

            # Periodic cleanup
            self._cleanup_old_buckets()

            return response
        else:
            # Rate limit exceeded
            wait_time = bucket.get_wait_time()
            retry_after = int(wait_time) + 1  # Round up

            logger.warning(
                "rate_limit_exceeded",
                identifier=identifier,
                path=request.url.path,
                wait_time_seconds=retry_after,
            )

            # Return 429 Too Many Requests
            return JSONResponse(
                status_code=429,
                content={
                    "error": "Rate limit exceeded",
                    "message": f"Too many requests. Please retry after {retry_after} seconds.",
                    "retry_after": retry_after,
                    "limit": self.requests_per_minute,
                },
                headers={
                    "X-RateLimit-Limit": str(self.requests_per_minute),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(retry_after),
                    "Retry-After": str(retry_after),
                },
            )

    async def xǁRateLimitMiddlewareǁdispatch__mutmut_16(self, request: Request, call_next):
        """
        Process request with rate limiting

        Args:
            request: FastAPI request
            call_next: Next middleware in chain

        Returns:
            Response or 429 Too Many Requests
        """
        # Skip rate limiting for health checks
        if request.url.path in ["/health", "/", "/docs", "/redoc", "/openapi.json"]:
            return await call_next(request)

        # Get identifier and bucket
        identifier = self._get_identifier(request)
        bucket = self._get_bucket(identifier)

        # Try to consume token
        if bucket.consume():
            # Request allowed
            remaining = None
            reset_seconds = int(bucket.capacity / bucket.refill_rate)

            logger.debug(
                "rate_limit_allowed",
                identifier=identifier,
                remaining=remaining,
                path=request.url.path,
            )

            # Process request
            response = await call_next(request)

            # Add rate limit headers
            response.headers["X-RateLimit-Limit"] = str(self.requests_per_minute)
            response.headers["X-RateLimit-Remaining"] = str(remaining)
            response.headers["X-RateLimit-Reset"] = str(reset_seconds)

            # Periodic cleanup
            self._cleanup_old_buckets()

            return response
        else:
            # Rate limit exceeded
            wait_time = bucket.get_wait_time()
            retry_after = int(wait_time) + 1  # Round up

            logger.warning(
                "rate_limit_exceeded",
                identifier=identifier,
                path=request.url.path,
                wait_time_seconds=retry_after,
            )

            # Return 429 Too Many Requests
            return JSONResponse(
                status_code=429,
                content={
                    "error": "Rate limit exceeded",
                    "message": f"Too many requests. Please retry after {retry_after} seconds.",
                    "retry_after": retry_after,
                    "limit": self.requests_per_minute,
                },
                headers={
                    "X-RateLimit-Limit": str(self.requests_per_minute),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(retry_after),
                    "Retry-After": str(retry_after),
                },
            )

    async def xǁRateLimitMiddlewareǁdispatch__mutmut_17(self, request: Request, call_next):
        """
        Process request with rate limiting

        Args:
            request: FastAPI request
            call_next: Next middleware in chain

        Returns:
            Response or 429 Too Many Requests
        """
        # Skip rate limiting for health checks
        if request.url.path in ["/health", "/", "/docs", "/redoc", "/openapi.json"]:
            return await call_next(request)

        # Get identifier and bucket
        identifier = self._get_identifier(request)
        bucket = self._get_bucket(identifier)

        # Try to consume token
        if bucket.consume():
            # Request allowed
            remaining = int(None)
            reset_seconds = int(bucket.capacity / bucket.refill_rate)

            logger.debug(
                "rate_limit_allowed",
                identifier=identifier,
                remaining=remaining,
                path=request.url.path,
            )

            # Process request
            response = await call_next(request)

            # Add rate limit headers
            response.headers["X-RateLimit-Limit"] = str(self.requests_per_minute)
            response.headers["X-RateLimit-Remaining"] = str(remaining)
            response.headers["X-RateLimit-Reset"] = str(reset_seconds)

            # Periodic cleanup
            self._cleanup_old_buckets()

            return response
        else:
            # Rate limit exceeded
            wait_time = bucket.get_wait_time()
            retry_after = int(wait_time) + 1  # Round up

            logger.warning(
                "rate_limit_exceeded",
                identifier=identifier,
                path=request.url.path,
                wait_time_seconds=retry_after,
            )

            # Return 429 Too Many Requests
            return JSONResponse(
                status_code=429,
                content={
                    "error": "Rate limit exceeded",
                    "message": f"Too many requests. Please retry after {retry_after} seconds.",
                    "retry_after": retry_after,
                    "limit": self.requests_per_minute,
                },
                headers={
                    "X-RateLimit-Limit": str(self.requests_per_minute),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(retry_after),
                    "Retry-After": str(retry_after),
                },
            )

    async def xǁRateLimitMiddlewareǁdispatch__mutmut_18(self, request: Request, call_next):
        """
        Process request with rate limiting

        Args:
            request: FastAPI request
            call_next: Next middleware in chain

        Returns:
            Response or 429 Too Many Requests
        """
        # Skip rate limiting for health checks
        if request.url.path in ["/health", "/", "/docs", "/redoc", "/openapi.json"]:
            return await call_next(request)

        # Get identifier and bucket
        identifier = self._get_identifier(request)
        bucket = self._get_bucket(identifier)

        # Try to consume token
        if bucket.consume():
            # Request allowed
            remaining = int(bucket.tokens)
            reset_seconds = None

            logger.debug(
                "rate_limit_allowed",
                identifier=identifier,
                remaining=remaining,
                path=request.url.path,
            )

            # Process request
            response = await call_next(request)

            # Add rate limit headers
            response.headers["X-RateLimit-Limit"] = str(self.requests_per_minute)
            response.headers["X-RateLimit-Remaining"] = str(remaining)
            response.headers["X-RateLimit-Reset"] = str(reset_seconds)

            # Periodic cleanup
            self._cleanup_old_buckets()

            return response
        else:
            # Rate limit exceeded
            wait_time = bucket.get_wait_time()
            retry_after = int(wait_time) + 1  # Round up

            logger.warning(
                "rate_limit_exceeded",
                identifier=identifier,
                path=request.url.path,
                wait_time_seconds=retry_after,
            )

            # Return 429 Too Many Requests
            return JSONResponse(
                status_code=429,
                content={
                    "error": "Rate limit exceeded",
                    "message": f"Too many requests. Please retry after {retry_after} seconds.",
                    "retry_after": retry_after,
                    "limit": self.requests_per_minute,
                },
                headers={
                    "X-RateLimit-Limit": str(self.requests_per_minute),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(retry_after),
                    "Retry-After": str(retry_after),
                },
            )

    async def xǁRateLimitMiddlewareǁdispatch__mutmut_19(self, request: Request, call_next):
        """
        Process request with rate limiting

        Args:
            request: FastAPI request
            call_next: Next middleware in chain

        Returns:
            Response or 429 Too Many Requests
        """
        # Skip rate limiting for health checks
        if request.url.path in ["/health", "/", "/docs", "/redoc", "/openapi.json"]:
            return await call_next(request)

        # Get identifier and bucket
        identifier = self._get_identifier(request)
        bucket = self._get_bucket(identifier)

        # Try to consume token
        if bucket.consume():
            # Request allowed
            remaining = int(bucket.tokens)
            reset_seconds = int(None)

            logger.debug(
                "rate_limit_allowed",
                identifier=identifier,
                remaining=remaining,
                path=request.url.path,
            )

            # Process request
            response = await call_next(request)

            # Add rate limit headers
            response.headers["X-RateLimit-Limit"] = str(self.requests_per_minute)
            response.headers["X-RateLimit-Remaining"] = str(remaining)
            response.headers["X-RateLimit-Reset"] = str(reset_seconds)

            # Periodic cleanup
            self._cleanup_old_buckets()

            return response
        else:
            # Rate limit exceeded
            wait_time = bucket.get_wait_time()
            retry_after = int(wait_time) + 1  # Round up

            logger.warning(
                "rate_limit_exceeded",
                identifier=identifier,
                path=request.url.path,
                wait_time_seconds=retry_after,
            )

            # Return 429 Too Many Requests
            return JSONResponse(
                status_code=429,
                content={
                    "error": "Rate limit exceeded",
                    "message": f"Too many requests. Please retry after {retry_after} seconds.",
                    "retry_after": retry_after,
                    "limit": self.requests_per_minute,
                },
                headers={
                    "X-RateLimit-Limit": str(self.requests_per_minute),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(retry_after),
                    "Retry-After": str(retry_after),
                },
            )

    async def xǁRateLimitMiddlewareǁdispatch__mutmut_20(self, request: Request, call_next):
        """
        Process request with rate limiting

        Args:
            request: FastAPI request
            call_next: Next middleware in chain

        Returns:
            Response or 429 Too Many Requests
        """
        # Skip rate limiting for health checks
        if request.url.path in ["/health", "/", "/docs", "/redoc", "/openapi.json"]:
            return await call_next(request)

        # Get identifier and bucket
        identifier = self._get_identifier(request)
        bucket = self._get_bucket(identifier)

        # Try to consume token
        if bucket.consume():
            # Request allowed
            remaining = int(bucket.tokens)
            reset_seconds = int(bucket.capacity * bucket.refill_rate)

            logger.debug(
                "rate_limit_allowed",
                identifier=identifier,
                remaining=remaining,
                path=request.url.path,
            )

            # Process request
            response = await call_next(request)

            # Add rate limit headers
            response.headers["X-RateLimit-Limit"] = str(self.requests_per_minute)
            response.headers["X-RateLimit-Remaining"] = str(remaining)
            response.headers["X-RateLimit-Reset"] = str(reset_seconds)

            # Periodic cleanup
            self._cleanup_old_buckets()

            return response
        else:
            # Rate limit exceeded
            wait_time = bucket.get_wait_time()
            retry_after = int(wait_time) + 1  # Round up

            logger.warning(
                "rate_limit_exceeded",
                identifier=identifier,
                path=request.url.path,
                wait_time_seconds=retry_after,
            )

            # Return 429 Too Many Requests
            return JSONResponse(
                status_code=429,
                content={
                    "error": "Rate limit exceeded",
                    "message": f"Too many requests. Please retry after {retry_after} seconds.",
                    "retry_after": retry_after,
                    "limit": self.requests_per_minute,
                },
                headers={
                    "X-RateLimit-Limit": str(self.requests_per_minute),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(retry_after),
                    "Retry-After": str(retry_after),
                },
            )

    async def xǁRateLimitMiddlewareǁdispatch__mutmut_21(self, request: Request, call_next):
        """
        Process request with rate limiting

        Args:
            request: FastAPI request
            call_next: Next middleware in chain

        Returns:
            Response or 429 Too Many Requests
        """
        # Skip rate limiting for health checks
        if request.url.path in ["/health", "/", "/docs", "/redoc", "/openapi.json"]:
            return await call_next(request)

        # Get identifier and bucket
        identifier = self._get_identifier(request)
        bucket = self._get_bucket(identifier)

        # Try to consume token
        if bucket.consume():
            # Request allowed
            remaining = int(bucket.tokens)
            reset_seconds = int(bucket.capacity / bucket.refill_rate)

            logger.debug(
                None,
                identifier=identifier,
                remaining=remaining,
                path=request.url.path,
            )

            # Process request
            response = await call_next(request)

            # Add rate limit headers
            response.headers["X-RateLimit-Limit"] = str(self.requests_per_minute)
            response.headers["X-RateLimit-Remaining"] = str(remaining)
            response.headers["X-RateLimit-Reset"] = str(reset_seconds)

            # Periodic cleanup
            self._cleanup_old_buckets()

            return response
        else:
            # Rate limit exceeded
            wait_time = bucket.get_wait_time()
            retry_after = int(wait_time) + 1  # Round up

            logger.warning(
                "rate_limit_exceeded",
                identifier=identifier,
                path=request.url.path,
                wait_time_seconds=retry_after,
            )

            # Return 429 Too Many Requests
            return JSONResponse(
                status_code=429,
                content={
                    "error": "Rate limit exceeded",
                    "message": f"Too many requests. Please retry after {retry_after} seconds.",
                    "retry_after": retry_after,
                    "limit": self.requests_per_minute,
                },
                headers={
                    "X-RateLimit-Limit": str(self.requests_per_minute),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(retry_after),
                    "Retry-After": str(retry_after),
                },
            )

    async def xǁRateLimitMiddlewareǁdispatch__mutmut_22(self, request: Request, call_next):
        """
        Process request with rate limiting

        Args:
            request: FastAPI request
            call_next: Next middleware in chain

        Returns:
            Response or 429 Too Many Requests
        """
        # Skip rate limiting for health checks
        if request.url.path in ["/health", "/", "/docs", "/redoc", "/openapi.json"]:
            return await call_next(request)

        # Get identifier and bucket
        identifier = self._get_identifier(request)
        bucket = self._get_bucket(identifier)

        # Try to consume token
        if bucket.consume():
            # Request allowed
            remaining = int(bucket.tokens)
            reset_seconds = int(bucket.capacity / bucket.refill_rate)

            logger.debug(
                "rate_limit_allowed",
                identifier=None,
                remaining=remaining,
                path=request.url.path,
            )

            # Process request
            response = await call_next(request)

            # Add rate limit headers
            response.headers["X-RateLimit-Limit"] = str(self.requests_per_minute)
            response.headers["X-RateLimit-Remaining"] = str(remaining)
            response.headers["X-RateLimit-Reset"] = str(reset_seconds)

            # Periodic cleanup
            self._cleanup_old_buckets()

            return response
        else:
            # Rate limit exceeded
            wait_time = bucket.get_wait_time()
            retry_after = int(wait_time) + 1  # Round up

            logger.warning(
                "rate_limit_exceeded",
                identifier=identifier,
                path=request.url.path,
                wait_time_seconds=retry_after,
            )

            # Return 429 Too Many Requests
            return JSONResponse(
                status_code=429,
                content={
                    "error": "Rate limit exceeded",
                    "message": f"Too many requests. Please retry after {retry_after} seconds.",
                    "retry_after": retry_after,
                    "limit": self.requests_per_minute,
                },
                headers={
                    "X-RateLimit-Limit": str(self.requests_per_minute),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(retry_after),
                    "Retry-After": str(retry_after),
                },
            )

    async def xǁRateLimitMiddlewareǁdispatch__mutmut_23(self, request: Request, call_next):
        """
        Process request with rate limiting

        Args:
            request: FastAPI request
            call_next: Next middleware in chain

        Returns:
            Response or 429 Too Many Requests
        """
        # Skip rate limiting for health checks
        if request.url.path in ["/health", "/", "/docs", "/redoc", "/openapi.json"]:
            return await call_next(request)

        # Get identifier and bucket
        identifier = self._get_identifier(request)
        bucket = self._get_bucket(identifier)

        # Try to consume token
        if bucket.consume():
            # Request allowed
            remaining = int(bucket.tokens)
            reset_seconds = int(bucket.capacity / bucket.refill_rate)

            logger.debug(
                "rate_limit_allowed",
                identifier=identifier,
                remaining=None,
                path=request.url.path,
            )

            # Process request
            response = await call_next(request)

            # Add rate limit headers
            response.headers["X-RateLimit-Limit"] = str(self.requests_per_minute)
            response.headers["X-RateLimit-Remaining"] = str(remaining)
            response.headers["X-RateLimit-Reset"] = str(reset_seconds)

            # Periodic cleanup
            self._cleanup_old_buckets()

            return response
        else:
            # Rate limit exceeded
            wait_time = bucket.get_wait_time()
            retry_after = int(wait_time) + 1  # Round up

            logger.warning(
                "rate_limit_exceeded",
                identifier=identifier,
                path=request.url.path,
                wait_time_seconds=retry_after,
            )

            # Return 429 Too Many Requests
            return JSONResponse(
                status_code=429,
                content={
                    "error": "Rate limit exceeded",
                    "message": f"Too many requests. Please retry after {retry_after} seconds.",
                    "retry_after": retry_after,
                    "limit": self.requests_per_minute,
                },
                headers={
                    "X-RateLimit-Limit": str(self.requests_per_minute),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(retry_after),
                    "Retry-After": str(retry_after),
                },
            )

    async def xǁRateLimitMiddlewareǁdispatch__mutmut_24(self, request: Request, call_next):
        """
        Process request with rate limiting

        Args:
            request: FastAPI request
            call_next: Next middleware in chain

        Returns:
            Response or 429 Too Many Requests
        """
        # Skip rate limiting for health checks
        if request.url.path in ["/health", "/", "/docs", "/redoc", "/openapi.json"]:
            return await call_next(request)

        # Get identifier and bucket
        identifier = self._get_identifier(request)
        bucket = self._get_bucket(identifier)

        # Try to consume token
        if bucket.consume():
            # Request allowed
            remaining = int(bucket.tokens)
            reset_seconds = int(bucket.capacity / bucket.refill_rate)

            logger.debug(
                "rate_limit_allowed",
                identifier=identifier,
                remaining=remaining,
                path=None,
            )

            # Process request
            response = await call_next(request)

            # Add rate limit headers
            response.headers["X-RateLimit-Limit"] = str(self.requests_per_minute)
            response.headers["X-RateLimit-Remaining"] = str(remaining)
            response.headers["X-RateLimit-Reset"] = str(reset_seconds)

            # Periodic cleanup
            self._cleanup_old_buckets()

            return response
        else:
            # Rate limit exceeded
            wait_time = bucket.get_wait_time()
            retry_after = int(wait_time) + 1  # Round up

            logger.warning(
                "rate_limit_exceeded",
                identifier=identifier,
                path=request.url.path,
                wait_time_seconds=retry_after,
            )

            # Return 429 Too Many Requests
            return JSONResponse(
                status_code=429,
                content={
                    "error": "Rate limit exceeded",
                    "message": f"Too many requests. Please retry after {retry_after} seconds.",
                    "retry_after": retry_after,
                    "limit": self.requests_per_minute,
                },
                headers={
                    "X-RateLimit-Limit": str(self.requests_per_minute),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(retry_after),
                    "Retry-After": str(retry_after),
                },
            )

    async def xǁRateLimitMiddlewareǁdispatch__mutmut_25(self, request: Request, call_next):
        """
        Process request with rate limiting

        Args:
            request: FastAPI request
            call_next: Next middleware in chain

        Returns:
            Response or 429 Too Many Requests
        """
        # Skip rate limiting for health checks
        if request.url.path in ["/health", "/", "/docs", "/redoc", "/openapi.json"]:
            return await call_next(request)

        # Get identifier and bucket
        identifier = self._get_identifier(request)
        bucket = self._get_bucket(identifier)

        # Try to consume token
        if bucket.consume():
            # Request allowed
            remaining = int(bucket.tokens)
            reset_seconds = int(bucket.capacity / bucket.refill_rate)

            logger.debug(
                identifier=identifier,
                remaining=remaining,
                path=request.url.path,
            )

            # Process request
            response = await call_next(request)

            # Add rate limit headers
            response.headers["X-RateLimit-Limit"] = str(self.requests_per_minute)
            response.headers["X-RateLimit-Remaining"] = str(remaining)
            response.headers["X-RateLimit-Reset"] = str(reset_seconds)

            # Periodic cleanup
            self._cleanup_old_buckets()

            return response
        else:
            # Rate limit exceeded
            wait_time = bucket.get_wait_time()
            retry_after = int(wait_time) + 1  # Round up

            logger.warning(
                "rate_limit_exceeded",
                identifier=identifier,
                path=request.url.path,
                wait_time_seconds=retry_after,
            )

            # Return 429 Too Many Requests
            return JSONResponse(
                status_code=429,
                content={
                    "error": "Rate limit exceeded",
                    "message": f"Too many requests. Please retry after {retry_after} seconds.",
                    "retry_after": retry_after,
                    "limit": self.requests_per_minute,
                },
                headers={
                    "X-RateLimit-Limit": str(self.requests_per_minute),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(retry_after),
                    "Retry-After": str(retry_after),
                },
            )

    async def xǁRateLimitMiddlewareǁdispatch__mutmut_26(self, request: Request, call_next):
        """
        Process request with rate limiting

        Args:
            request: FastAPI request
            call_next: Next middleware in chain

        Returns:
            Response or 429 Too Many Requests
        """
        # Skip rate limiting for health checks
        if request.url.path in ["/health", "/", "/docs", "/redoc", "/openapi.json"]:
            return await call_next(request)

        # Get identifier and bucket
        identifier = self._get_identifier(request)
        bucket = self._get_bucket(identifier)

        # Try to consume token
        if bucket.consume():
            # Request allowed
            remaining = int(bucket.tokens)
            reset_seconds = int(bucket.capacity / bucket.refill_rate)

            logger.debug(
                "rate_limit_allowed",
                remaining=remaining,
                path=request.url.path,
            )

            # Process request
            response = await call_next(request)

            # Add rate limit headers
            response.headers["X-RateLimit-Limit"] = str(self.requests_per_minute)
            response.headers["X-RateLimit-Remaining"] = str(remaining)
            response.headers["X-RateLimit-Reset"] = str(reset_seconds)

            # Periodic cleanup
            self._cleanup_old_buckets()

            return response
        else:
            # Rate limit exceeded
            wait_time = bucket.get_wait_time()
            retry_after = int(wait_time) + 1  # Round up

            logger.warning(
                "rate_limit_exceeded",
                identifier=identifier,
                path=request.url.path,
                wait_time_seconds=retry_after,
            )

            # Return 429 Too Many Requests
            return JSONResponse(
                status_code=429,
                content={
                    "error": "Rate limit exceeded",
                    "message": f"Too many requests. Please retry after {retry_after} seconds.",
                    "retry_after": retry_after,
                    "limit": self.requests_per_minute,
                },
                headers={
                    "X-RateLimit-Limit": str(self.requests_per_minute),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(retry_after),
                    "Retry-After": str(retry_after),
                },
            )

    async def xǁRateLimitMiddlewareǁdispatch__mutmut_27(self, request: Request, call_next):
        """
        Process request with rate limiting

        Args:
            request: FastAPI request
            call_next: Next middleware in chain

        Returns:
            Response or 429 Too Many Requests
        """
        # Skip rate limiting for health checks
        if request.url.path in ["/health", "/", "/docs", "/redoc", "/openapi.json"]:
            return await call_next(request)

        # Get identifier and bucket
        identifier = self._get_identifier(request)
        bucket = self._get_bucket(identifier)

        # Try to consume token
        if bucket.consume():
            # Request allowed
            remaining = int(bucket.tokens)
            reset_seconds = int(bucket.capacity / bucket.refill_rate)

            logger.debug(
                "rate_limit_allowed",
                identifier=identifier,
                path=request.url.path,
            )

            # Process request
            response = await call_next(request)

            # Add rate limit headers
            response.headers["X-RateLimit-Limit"] = str(self.requests_per_minute)
            response.headers["X-RateLimit-Remaining"] = str(remaining)
            response.headers["X-RateLimit-Reset"] = str(reset_seconds)

            # Periodic cleanup
            self._cleanup_old_buckets()

            return response
        else:
            # Rate limit exceeded
            wait_time = bucket.get_wait_time()
            retry_after = int(wait_time) + 1  # Round up

            logger.warning(
                "rate_limit_exceeded",
                identifier=identifier,
                path=request.url.path,
                wait_time_seconds=retry_after,
            )

            # Return 429 Too Many Requests
            return JSONResponse(
                status_code=429,
                content={
                    "error": "Rate limit exceeded",
                    "message": f"Too many requests. Please retry after {retry_after} seconds.",
                    "retry_after": retry_after,
                    "limit": self.requests_per_minute,
                },
                headers={
                    "X-RateLimit-Limit": str(self.requests_per_minute),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(retry_after),
                    "Retry-After": str(retry_after),
                },
            )

    async def xǁRateLimitMiddlewareǁdispatch__mutmut_28(self, request: Request, call_next):
        """
        Process request with rate limiting

        Args:
            request: FastAPI request
            call_next: Next middleware in chain

        Returns:
            Response or 429 Too Many Requests
        """
        # Skip rate limiting for health checks
        if request.url.path in ["/health", "/", "/docs", "/redoc", "/openapi.json"]:
            return await call_next(request)

        # Get identifier and bucket
        identifier = self._get_identifier(request)
        bucket = self._get_bucket(identifier)

        # Try to consume token
        if bucket.consume():
            # Request allowed
            remaining = int(bucket.tokens)
            reset_seconds = int(bucket.capacity / bucket.refill_rate)

            logger.debug(
                "rate_limit_allowed",
                identifier=identifier,
                remaining=remaining,
                )

            # Process request
            response = await call_next(request)

            # Add rate limit headers
            response.headers["X-RateLimit-Limit"] = str(self.requests_per_minute)
            response.headers["X-RateLimit-Remaining"] = str(remaining)
            response.headers["X-RateLimit-Reset"] = str(reset_seconds)

            # Periodic cleanup
            self._cleanup_old_buckets()

            return response
        else:
            # Rate limit exceeded
            wait_time = bucket.get_wait_time()
            retry_after = int(wait_time) + 1  # Round up

            logger.warning(
                "rate_limit_exceeded",
                identifier=identifier,
                path=request.url.path,
                wait_time_seconds=retry_after,
            )

            # Return 429 Too Many Requests
            return JSONResponse(
                status_code=429,
                content={
                    "error": "Rate limit exceeded",
                    "message": f"Too many requests. Please retry after {retry_after} seconds.",
                    "retry_after": retry_after,
                    "limit": self.requests_per_minute,
                },
                headers={
                    "X-RateLimit-Limit": str(self.requests_per_minute),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(retry_after),
                    "Retry-After": str(retry_after),
                },
            )

    async def xǁRateLimitMiddlewareǁdispatch__mutmut_29(self, request: Request, call_next):
        """
        Process request with rate limiting

        Args:
            request: FastAPI request
            call_next: Next middleware in chain

        Returns:
            Response or 429 Too Many Requests
        """
        # Skip rate limiting for health checks
        if request.url.path in ["/health", "/", "/docs", "/redoc", "/openapi.json"]:
            return await call_next(request)

        # Get identifier and bucket
        identifier = self._get_identifier(request)
        bucket = self._get_bucket(identifier)

        # Try to consume token
        if bucket.consume():
            # Request allowed
            remaining = int(bucket.tokens)
            reset_seconds = int(bucket.capacity / bucket.refill_rate)

            logger.debug(
                "XXrate_limit_allowedXX",
                identifier=identifier,
                remaining=remaining,
                path=request.url.path,
            )

            # Process request
            response = await call_next(request)

            # Add rate limit headers
            response.headers["X-RateLimit-Limit"] = str(self.requests_per_minute)
            response.headers["X-RateLimit-Remaining"] = str(remaining)
            response.headers["X-RateLimit-Reset"] = str(reset_seconds)

            # Periodic cleanup
            self._cleanup_old_buckets()

            return response
        else:
            # Rate limit exceeded
            wait_time = bucket.get_wait_time()
            retry_after = int(wait_time) + 1  # Round up

            logger.warning(
                "rate_limit_exceeded",
                identifier=identifier,
                path=request.url.path,
                wait_time_seconds=retry_after,
            )

            # Return 429 Too Many Requests
            return JSONResponse(
                status_code=429,
                content={
                    "error": "Rate limit exceeded",
                    "message": f"Too many requests. Please retry after {retry_after} seconds.",
                    "retry_after": retry_after,
                    "limit": self.requests_per_minute,
                },
                headers={
                    "X-RateLimit-Limit": str(self.requests_per_minute),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(retry_after),
                    "Retry-After": str(retry_after),
                },
            )

    async def xǁRateLimitMiddlewareǁdispatch__mutmut_30(self, request: Request, call_next):
        """
        Process request with rate limiting

        Args:
            request: FastAPI request
            call_next: Next middleware in chain

        Returns:
            Response or 429 Too Many Requests
        """
        # Skip rate limiting for health checks
        if request.url.path in ["/health", "/", "/docs", "/redoc", "/openapi.json"]:
            return await call_next(request)

        # Get identifier and bucket
        identifier = self._get_identifier(request)
        bucket = self._get_bucket(identifier)

        # Try to consume token
        if bucket.consume():
            # Request allowed
            remaining = int(bucket.tokens)
            reset_seconds = int(bucket.capacity / bucket.refill_rate)

            logger.debug(
                "RATE_LIMIT_ALLOWED",
                identifier=identifier,
                remaining=remaining,
                path=request.url.path,
            )

            # Process request
            response = await call_next(request)

            # Add rate limit headers
            response.headers["X-RateLimit-Limit"] = str(self.requests_per_minute)
            response.headers["X-RateLimit-Remaining"] = str(remaining)
            response.headers["X-RateLimit-Reset"] = str(reset_seconds)

            # Periodic cleanup
            self._cleanup_old_buckets()

            return response
        else:
            # Rate limit exceeded
            wait_time = bucket.get_wait_time()
            retry_after = int(wait_time) + 1  # Round up

            logger.warning(
                "rate_limit_exceeded",
                identifier=identifier,
                path=request.url.path,
                wait_time_seconds=retry_after,
            )

            # Return 429 Too Many Requests
            return JSONResponse(
                status_code=429,
                content={
                    "error": "Rate limit exceeded",
                    "message": f"Too many requests. Please retry after {retry_after} seconds.",
                    "retry_after": retry_after,
                    "limit": self.requests_per_minute,
                },
                headers={
                    "X-RateLimit-Limit": str(self.requests_per_minute),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(retry_after),
                    "Retry-After": str(retry_after),
                },
            )

    async def xǁRateLimitMiddlewareǁdispatch__mutmut_31(self, request: Request, call_next):
        """
        Process request with rate limiting

        Args:
            request: FastAPI request
            call_next: Next middleware in chain

        Returns:
            Response or 429 Too Many Requests
        """
        # Skip rate limiting for health checks
        if request.url.path in ["/health", "/", "/docs", "/redoc", "/openapi.json"]:
            return await call_next(request)

        # Get identifier and bucket
        identifier = self._get_identifier(request)
        bucket = self._get_bucket(identifier)

        # Try to consume token
        if bucket.consume():
            # Request allowed
            remaining = int(bucket.tokens)
            reset_seconds = int(bucket.capacity / bucket.refill_rate)

            logger.debug(
                "rate_limit_allowed",
                identifier=identifier,
                remaining=remaining,
                path=request.url.path,
            )

            # Process request
            response = None

            # Add rate limit headers
            response.headers["X-RateLimit-Limit"] = str(self.requests_per_minute)
            response.headers["X-RateLimit-Remaining"] = str(remaining)
            response.headers["X-RateLimit-Reset"] = str(reset_seconds)

            # Periodic cleanup
            self._cleanup_old_buckets()

            return response
        else:
            # Rate limit exceeded
            wait_time = bucket.get_wait_time()
            retry_after = int(wait_time) + 1  # Round up

            logger.warning(
                "rate_limit_exceeded",
                identifier=identifier,
                path=request.url.path,
                wait_time_seconds=retry_after,
            )

            # Return 429 Too Many Requests
            return JSONResponse(
                status_code=429,
                content={
                    "error": "Rate limit exceeded",
                    "message": f"Too many requests. Please retry after {retry_after} seconds.",
                    "retry_after": retry_after,
                    "limit": self.requests_per_minute,
                },
                headers={
                    "X-RateLimit-Limit": str(self.requests_per_minute),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(retry_after),
                    "Retry-After": str(retry_after),
                },
            )

    async def xǁRateLimitMiddlewareǁdispatch__mutmut_32(self, request: Request, call_next):
        """
        Process request with rate limiting

        Args:
            request: FastAPI request
            call_next: Next middleware in chain

        Returns:
            Response or 429 Too Many Requests
        """
        # Skip rate limiting for health checks
        if request.url.path in ["/health", "/", "/docs", "/redoc", "/openapi.json"]:
            return await call_next(request)

        # Get identifier and bucket
        identifier = self._get_identifier(request)
        bucket = self._get_bucket(identifier)

        # Try to consume token
        if bucket.consume():
            # Request allowed
            remaining = int(bucket.tokens)
            reset_seconds = int(bucket.capacity / bucket.refill_rate)

            logger.debug(
                "rate_limit_allowed",
                identifier=identifier,
                remaining=remaining,
                path=request.url.path,
            )

            # Process request
            response = await call_next(None)

            # Add rate limit headers
            response.headers["X-RateLimit-Limit"] = str(self.requests_per_minute)
            response.headers["X-RateLimit-Remaining"] = str(remaining)
            response.headers["X-RateLimit-Reset"] = str(reset_seconds)

            # Periodic cleanup
            self._cleanup_old_buckets()

            return response
        else:
            # Rate limit exceeded
            wait_time = bucket.get_wait_time()
            retry_after = int(wait_time) + 1  # Round up

            logger.warning(
                "rate_limit_exceeded",
                identifier=identifier,
                path=request.url.path,
                wait_time_seconds=retry_after,
            )

            # Return 429 Too Many Requests
            return JSONResponse(
                status_code=429,
                content={
                    "error": "Rate limit exceeded",
                    "message": f"Too many requests. Please retry after {retry_after} seconds.",
                    "retry_after": retry_after,
                    "limit": self.requests_per_minute,
                },
                headers={
                    "X-RateLimit-Limit": str(self.requests_per_minute),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(retry_after),
                    "Retry-After": str(retry_after),
                },
            )

    async def xǁRateLimitMiddlewareǁdispatch__mutmut_33(self, request: Request, call_next):
        """
        Process request with rate limiting

        Args:
            request: FastAPI request
            call_next: Next middleware in chain

        Returns:
            Response or 429 Too Many Requests
        """
        # Skip rate limiting for health checks
        if request.url.path in ["/health", "/", "/docs", "/redoc", "/openapi.json"]:
            return await call_next(request)

        # Get identifier and bucket
        identifier = self._get_identifier(request)
        bucket = self._get_bucket(identifier)

        # Try to consume token
        if bucket.consume():
            # Request allowed
            remaining = int(bucket.tokens)
            reset_seconds = int(bucket.capacity / bucket.refill_rate)

            logger.debug(
                "rate_limit_allowed",
                identifier=identifier,
                remaining=remaining,
                path=request.url.path,
            )

            # Process request
            response = await call_next(request)

            # Add rate limit headers
            response.headers["X-RateLimit-Limit"] = None
            response.headers["X-RateLimit-Remaining"] = str(remaining)
            response.headers["X-RateLimit-Reset"] = str(reset_seconds)

            # Periodic cleanup
            self._cleanup_old_buckets()

            return response
        else:
            # Rate limit exceeded
            wait_time = bucket.get_wait_time()
            retry_after = int(wait_time) + 1  # Round up

            logger.warning(
                "rate_limit_exceeded",
                identifier=identifier,
                path=request.url.path,
                wait_time_seconds=retry_after,
            )

            # Return 429 Too Many Requests
            return JSONResponse(
                status_code=429,
                content={
                    "error": "Rate limit exceeded",
                    "message": f"Too many requests. Please retry after {retry_after} seconds.",
                    "retry_after": retry_after,
                    "limit": self.requests_per_minute,
                },
                headers={
                    "X-RateLimit-Limit": str(self.requests_per_minute),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(retry_after),
                    "Retry-After": str(retry_after),
                },
            )

    async def xǁRateLimitMiddlewareǁdispatch__mutmut_34(self, request: Request, call_next):
        """
        Process request with rate limiting

        Args:
            request: FastAPI request
            call_next: Next middleware in chain

        Returns:
            Response or 429 Too Many Requests
        """
        # Skip rate limiting for health checks
        if request.url.path in ["/health", "/", "/docs", "/redoc", "/openapi.json"]:
            return await call_next(request)

        # Get identifier and bucket
        identifier = self._get_identifier(request)
        bucket = self._get_bucket(identifier)

        # Try to consume token
        if bucket.consume():
            # Request allowed
            remaining = int(bucket.tokens)
            reset_seconds = int(bucket.capacity / bucket.refill_rate)

            logger.debug(
                "rate_limit_allowed",
                identifier=identifier,
                remaining=remaining,
                path=request.url.path,
            )

            # Process request
            response = await call_next(request)

            # Add rate limit headers
            response.headers["XXX-RateLimit-LimitXX"] = str(self.requests_per_minute)
            response.headers["X-RateLimit-Remaining"] = str(remaining)
            response.headers["X-RateLimit-Reset"] = str(reset_seconds)

            # Periodic cleanup
            self._cleanup_old_buckets()

            return response
        else:
            # Rate limit exceeded
            wait_time = bucket.get_wait_time()
            retry_after = int(wait_time) + 1  # Round up

            logger.warning(
                "rate_limit_exceeded",
                identifier=identifier,
                path=request.url.path,
                wait_time_seconds=retry_after,
            )

            # Return 429 Too Many Requests
            return JSONResponse(
                status_code=429,
                content={
                    "error": "Rate limit exceeded",
                    "message": f"Too many requests. Please retry after {retry_after} seconds.",
                    "retry_after": retry_after,
                    "limit": self.requests_per_minute,
                },
                headers={
                    "X-RateLimit-Limit": str(self.requests_per_minute),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(retry_after),
                    "Retry-After": str(retry_after),
                },
            )

    async def xǁRateLimitMiddlewareǁdispatch__mutmut_35(self, request: Request, call_next):
        """
        Process request with rate limiting

        Args:
            request: FastAPI request
            call_next: Next middleware in chain

        Returns:
            Response or 429 Too Many Requests
        """
        # Skip rate limiting for health checks
        if request.url.path in ["/health", "/", "/docs", "/redoc", "/openapi.json"]:
            return await call_next(request)

        # Get identifier and bucket
        identifier = self._get_identifier(request)
        bucket = self._get_bucket(identifier)

        # Try to consume token
        if bucket.consume():
            # Request allowed
            remaining = int(bucket.tokens)
            reset_seconds = int(bucket.capacity / bucket.refill_rate)

            logger.debug(
                "rate_limit_allowed",
                identifier=identifier,
                remaining=remaining,
                path=request.url.path,
            )

            # Process request
            response = await call_next(request)

            # Add rate limit headers
            response.headers["x-ratelimit-limit"] = str(self.requests_per_minute)
            response.headers["X-RateLimit-Remaining"] = str(remaining)
            response.headers["X-RateLimit-Reset"] = str(reset_seconds)

            # Periodic cleanup
            self._cleanup_old_buckets()

            return response
        else:
            # Rate limit exceeded
            wait_time = bucket.get_wait_time()
            retry_after = int(wait_time) + 1  # Round up

            logger.warning(
                "rate_limit_exceeded",
                identifier=identifier,
                path=request.url.path,
                wait_time_seconds=retry_after,
            )

            # Return 429 Too Many Requests
            return JSONResponse(
                status_code=429,
                content={
                    "error": "Rate limit exceeded",
                    "message": f"Too many requests. Please retry after {retry_after} seconds.",
                    "retry_after": retry_after,
                    "limit": self.requests_per_minute,
                },
                headers={
                    "X-RateLimit-Limit": str(self.requests_per_minute),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(retry_after),
                    "Retry-After": str(retry_after),
                },
            )

    async def xǁRateLimitMiddlewareǁdispatch__mutmut_36(self, request: Request, call_next):
        """
        Process request with rate limiting

        Args:
            request: FastAPI request
            call_next: Next middleware in chain

        Returns:
            Response or 429 Too Many Requests
        """
        # Skip rate limiting for health checks
        if request.url.path in ["/health", "/", "/docs", "/redoc", "/openapi.json"]:
            return await call_next(request)

        # Get identifier and bucket
        identifier = self._get_identifier(request)
        bucket = self._get_bucket(identifier)

        # Try to consume token
        if bucket.consume():
            # Request allowed
            remaining = int(bucket.tokens)
            reset_seconds = int(bucket.capacity / bucket.refill_rate)

            logger.debug(
                "rate_limit_allowed",
                identifier=identifier,
                remaining=remaining,
                path=request.url.path,
            )

            # Process request
            response = await call_next(request)

            # Add rate limit headers
            response.headers["X-RATELIMIT-LIMIT"] = str(self.requests_per_minute)
            response.headers["X-RateLimit-Remaining"] = str(remaining)
            response.headers["X-RateLimit-Reset"] = str(reset_seconds)

            # Periodic cleanup
            self._cleanup_old_buckets()

            return response
        else:
            # Rate limit exceeded
            wait_time = bucket.get_wait_time()
            retry_after = int(wait_time) + 1  # Round up

            logger.warning(
                "rate_limit_exceeded",
                identifier=identifier,
                path=request.url.path,
                wait_time_seconds=retry_after,
            )

            # Return 429 Too Many Requests
            return JSONResponse(
                status_code=429,
                content={
                    "error": "Rate limit exceeded",
                    "message": f"Too many requests. Please retry after {retry_after} seconds.",
                    "retry_after": retry_after,
                    "limit": self.requests_per_minute,
                },
                headers={
                    "X-RateLimit-Limit": str(self.requests_per_minute),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(retry_after),
                    "Retry-After": str(retry_after),
                },
            )

    async def xǁRateLimitMiddlewareǁdispatch__mutmut_37(self, request: Request, call_next):
        """
        Process request with rate limiting

        Args:
            request: FastAPI request
            call_next: Next middleware in chain

        Returns:
            Response or 429 Too Many Requests
        """
        # Skip rate limiting for health checks
        if request.url.path in ["/health", "/", "/docs", "/redoc", "/openapi.json"]:
            return await call_next(request)

        # Get identifier and bucket
        identifier = self._get_identifier(request)
        bucket = self._get_bucket(identifier)

        # Try to consume token
        if bucket.consume():
            # Request allowed
            remaining = int(bucket.tokens)
            reset_seconds = int(bucket.capacity / bucket.refill_rate)

            logger.debug(
                "rate_limit_allowed",
                identifier=identifier,
                remaining=remaining,
                path=request.url.path,
            )

            # Process request
            response = await call_next(request)

            # Add rate limit headers
            response.headers["X-RateLimit-Limit"] = str(None)
            response.headers["X-RateLimit-Remaining"] = str(remaining)
            response.headers["X-RateLimit-Reset"] = str(reset_seconds)

            # Periodic cleanup
            self._cleanup_old_buckets()

            return response
        else:
            # Rate limit exceeded
            wait_time = bucket.get_wait_time()
            retry_after = int(wait_time) + 1  # Round up

            logger.warning(
                "rate_limit_exceeded",
                identifier=identifier,
                path=request.url.path,
                wait_time_seconds=retry_after,
            )

            # Return 429 Too Many Requests
            return JSONResponse(
                status_code=429,
                content={
                    "error": "Rate limit exceeded",
                    "message": f"Too many requests. Please retry after {retry_after} seconds.",
                    "retry_after": retry_after,
                    "limit": self.requests_per_minute,
                },
                headers={
                    "X-RateLimit-Limit": str(self.requests_per_minute),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(retry_after),
                    "Retry-After": str(retry_after),
                },
            )

    async def xǁRateLimitMiddlewareǁdispatch__mutmut_38(self, request: Request, call_next):
        """
        Process request with rate limiting

        Args:
            request: FastAPI request
            call_next: Next middleware in chain

        Returns:
            Response or 429 Too Many Requests
        """
        # Skip rate limiting for health checks
        if request.url.path in ["/health", "/", "/docs", "/redoc", "/openapi.json"]:
            return await call_next(request)

        # Get identifier and bucket
        identifier = self._get_identifier(request)
        bucket = self._get_bucket(identifier)

        # Try to consume token
        if bucket.consume():
            # Request allowed
            remaining = int(bucket.tokens)
            reset_seconds = int(bucket.capacity / bucket.refill_rate)

            logger.debug(
                "rate_limit_allowed",
                identifier=identifier,
                remaining=remaining,
                path=request.url.path,
            )

            # Process request
            response = await call_next(request)

            # Add rate limit headers
            response.headers["X-RateLimit-Limit"] = str(self.requests_per_minute)
            response.headers["X-RateLimit-Remaining"] = None
            response.headers["X-RateLimit-Reset"] = str(reset_seconds)

            # Periodic cleanup
            self._cleanup_old_buckets()

            return response
        else:
            # Rate limit exceeded
            wait_time = bucket.get_wait_time()
            retry_after = int(wait_time) + 1  # Round up

            logger.warning(
                "rate_limit_exceeded",
                identifier=identifier,
                path=request.url.path,
                wait_time_seconds=retry_after,
            )

            # Return 429 Too Many Requests
            return JSONResponse(
                status_code=429,
                content={
                    "error": "Rate limit exceeded",
                    "message": f"Too many requests. Please retry after {retry_after} seconds.",
                    "retry_after": retry_after,
                    "limit": self.requests_per_minute,
                },
                headers={
                    "X-RateLimit-Limit": str(self.requests_per_minute),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(retry_after),
                    "Retry-After": str(retry_after),
                },
            )

    async def xǁRateLimitMiddlewareǁdispatch__mutmut_39(self, request: Request, call_next):
        """
        Process request with rate limiting

        Args:
            request: FastAPI request
            call_next: Next middleware in chain

        Returns:
            Response or 429 Too Many Requests
        """
        # Skip rate limiting for health checks
        if request.url.path in ["/health", "/", "/docs", "/redoc", "/openapi.json"]:
            return await call_next(request)

        # Get identifier and bucket
        identifier = self._get_identifier(request)
        bucket = self._get_bucket(identifier)

        # Try to consume token
        if bucket.consume():
            # Request allowed
            remaining = int(bucket.tokens)
            reset_seconds = int(bucket.capacity / bucket.refill_rate)

            logger.debug(
                "rate_limit_allowed",
                identifier=identifier,
                remaining=remaining,
                path=request.url.path,
            )

            # Process request
            response = await call_next(request)

            # Add rate limit headers
            response.headers["X-RateLimit-Limit"] = str(self.requests_per_minute)
            response.headers["XXX-RateLimit-RemainingXX"] = str(remaining)
            response.headers["X-RateLimit-Reset"] = str(reset_seconds)

            # Periodic cleanup
            self._cleanup_old_buckets()

            return response
        else:
            # Rate limit exceeded
            wait_time = bucket.get_wait_time()
            retry_after = int(wait_time) + 1  # Round up

            logger.warning(
                "rate_limit_exceeded",
                identifier=identifier,
                path=request.url.path,
                wait_time_seconds=retry_after,
            )

            # Return 429 Too Many Requests
            return JSONResponse(
                status_code=429,
                content={
                    "error": "Rate limit exceeded",
                    "message": f"Too many requests. Please retry after {retry_after} seconds.",
                    "retry_after": retry_after,
                    "limit": self.requests_per_minute,
                },
                headers={
                    "X-RateLimit-Limit": str(self.requests_per_minute),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(retry_after),
                    "Retry-After": str(retry_after),
                },
            )

    async def xǁRateLimitMiddlewareǁdispatch__mutmut_40(self, request: Request, call_next):
        """
        Process request with rate limiting

        Args:
            request: FastAPI request
            call_next: Next middleware in chain

        Returns:
            Response or 429 Too Many Requests
        """
        # Skip rate limiting for health checks
        if request.url.path in ["/health", "/", "/docs", "/redoc", "/openapi.json"]:
            return await call_next(request)

        # Get identifier and bucket
        identifier = self._get_identifier(request)
        bucket = self._get_bucket(identifier)

        # Try to consume token
        if bucket.consume():
            # Request allowed
            remaining = int(bucket.tokens)
            reset_seconds = int(bucket.capacity / bucket.refill_rate)

            logger.debug(
                "rate_limit_allowed",
                identifier=identifier,
                remaining=remaining,
                path=request.url.path,
            )

            # Process request
            response = await call_next(request)

            # Add rate limit headers
            response.headers["X-RateLimit-Limit"] = str(self.requests_per_minute)
            response.headers["x-ratelimit-remaining"] = str(remaining)
            response.headers["X-RateLimit-Reset"] = str(reset_seconds)

            # Periodic cleanup
            self._cleanup_old_buckets()

            return response
        else:
            # Rate limit exceeded
            wait_time = bucket.get_wait_time()
            retry_after = int(wait_time) + 1  # Round up

            logger.warning(
                "rate_limit_exceeded",
                identifier=identifier,
                path=request.url.path,
                wait_time_seconds=retry_after,
            )

            # Return 429 Too Many Requests
            return JSONResponse(
                status_code=429,
                content={
                    "error": "Rate limit exceeded",
                    "message": f"Too many requests. Please retry after {retry_after} seconds.",
                    "retry_after": retry_after,
                    "limit": self.requests_per_minute,
                },
                headers={
                    "X-RateLimit-Limit": str(self.requests_per_minute),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(retry_after),
                    "Retry-After": str(retry_after),
                },
            )

    async def xǁRateLimitMiddlewareǁdispatch__mutmut_41(self, request: Request, call_next):
        """
        Process request with rate limiting

        Args:
            request: FastAPI request
            call_next: Next middleware in chain

        Returns:
            Response or 429 Too Many Requests
        """
        # Skip rate limiting for health checks
        if request.url.path in ["/health", "/", "/docs", "/redoc", "/openapi.json"]:
            return await call_next(request)

        # Get identifier and bucket
        identifier = self._get_identifier(request)
        bucket = self._get_bucket(identifier)

        # Try to consume token
        if bucket.consume():
            # Request allowed
            remaining = int(bucket.tokens)
            reset_seconds = int(bucket.capacity / bucket.refill_rate)

            logger.debug(
                "rate_limit_allowed",
                identifier=identifier,
                remaining=remaining,
                path=request.url.path,
            )

            # Process request
            response = await call_next(request)

            # Add rate limit headers
            response.headers["X-RateLimit-Limit"] = str(self.requests_per_minute)
            response.headers["X-RATELIMIT-REMAINING"] = str(remaining)
            response.headers["X-RateLimit-Reset"] = str(reset_seconds)

            # Periodic cleanup
            self._cleanup_old_buckets()

            return response
        else:
            # Rate limit exceeded
            wait_time = bucket.get_wait_time()
            retry_after = int(wait_time) + 1  # Round up

            logger.warning(
                "rate_limit_exceeded",
                identifier=identifier,
                path=request.url.path,
                wait_time_seconds=retry_after,
            )

            # Return 429 Too Many Requests
            return JSONResponse(
                status_code=429,
                content={
                    "error": "Rate limit exceeded",
                    "message": f"Too many requests. Please retry after {retry_after} seconds.",
                    "retry_after": retry_after,
                    "limit": self.requests_per_minute,
                },
                headers={
                    "X-RateLimit-Limit": str(self.requests_per_minute),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(retry_after),
                    "Retry-After": str(retry_after),
                },
            )

    async def xǁRateLimitMiddlewareǁdispatch__mutmut_42(self, request: Request, call_next):
        """
        Process request with rate limiting

        Args:
            request: FastAPI request
            call_next: Next middleware in chain

        Returns:
            Response or 429 Too Many Requests
        """
        # Skip rate limiting for health checks
        if request.url.path in ["/health", "/", "/docs", "/redoc", "/openapi.json"]:
            return await call_next(request)

        # Get identifier and bucket
        identifier = self._get_identifier(request)
        bucket = self._get_bucket(identifier)

        # Try to consume token
        if bucket.consume():
            # Request allowed
            remaining = int(bucket.tokens)
            reset_seconds = int(bucket.capacity / bucket.refill_rate)

            logger.debug(
                "rate_limit_allowed",
                identifier=identifier,
                remaining=remaining,
                path=request.url.path,
            )

            # Process request
            response = await call_next(request)

            # Add rate limit headers
            response.headers["X-RateLimit-Limit"] = str(self.requests_per_minute)
            response.headers["X-RateLimit-Remaining"] = str(None)
            response.headers["X-RateLimit-Reset"] = str(reset_seconds)

            # Periodic cleanup
            self._cleanup_old_buckets()

            return response
        else:
            # Rate limit exceeded
            wait_time = bucket.get_wait_time()
            retry_after = int(wait_time) + 1  # Round up

            logger.warning(
                "rate_limit_exceeded",
                identifier=identifier,
                path=request.url.path,
                wait_time_seconds=retry_after,
            )

            # Return 429 Too Many Requests
            return JSONResponse(
                status_code=429,
                content={
                    "error": "Rate limit exceeded",
                    "message": f"Too many requests. Please retry after {retry_after} seconds.",
                    "retry_after": retry_after,
                    "limit": self.requests_per_minute,
                },
                headers={
                    "X-RateLimit-Limit": str(self.requests_per_minute),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(retry_after),
                    "Retry-After": str(retry_after),
                },
            )

    async def xǁRateLimitMiddlewareǁdispatch__mutmut_43(self, request: Request, call_next):
        """
        Process request with rate limiting

        Args:
            request: FastAPI request
            call_next: Next middleware in chain

        Returns:
            Response or 429 Too Many Requests
        """
        # Skip rate limiting for health checks
        if request.url.path in ["/health", "/", "/docs", "/redoc", "/openapi.json"]:
            return await call_next(request)

        # Get identifier and bucket
        identifier = self._get_identifier(request)
        bucket = self._get_bucket(identifier)

        # Try to consume token
        if bucket.consume():
            # Request allowed
            remaining = int(bucket.tokens)
            reset_seconds = int(bucket.capacity / bucket.refill_rate)

            logger.debug(
                "rate_limit_allowed",
                identifier=identifier,
                remaining=remaining,
                path=request.url.path,
            )

            # Process request
            response = await call_next(request)

            # Add rate limit headers
            response.headers["X-RateLimit-Limit"] = str(self.requests_per_minute)
            response.headers["X-RateLimit-Remaining"] = str(remaining)
            response.headers["X-RateLimit-Reset"] = None

            # Periodic cleanup
            self._cleanup_old_buckets()

            return response
        else:
            # Rate limit exceeded
            wait_time = bucket.get_wait_time()
            retry_after = int(wait_time) + 1  # Round up

            logger.warning(
                "rate_limit_exceeded",
                identifier=identifier,
                path=request.url.path,
                wait_time_seconds=retry_after,
            )

            # Return 429 Too Many Requests
            return JSONResponse(
                status_code=429,
                content={
                    "error": "Rate limit exceeded",
                    "message": f"Too many requests. Please retry after {retry_after} seconds.",
                    "retry_after": retry_after,
                    "limit": self.requests_per_minute,
                },
                headers={
                    "X-RateLimit-Limit": str(self.requests_per_minute),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(retry_after),
                    "Retry-After": str(retry_after),
                },
            )

    async def xǁRateLimitMiddlewareǁdispatch__mutmut_44(self, request: Request, call_next):
        """
        Process request with rate limiting

        Args:
            request: FastAPI request
            call_next: Next middleware in chain

        Returns:
            Response or 429 Too Many Requests
        """
        # Skip rate limiting for health checks
        if request.url.path in ["/health", "/", "/docs", "/redoc", "/openapi.json"]:
            return await call_next(request)

        # Get identifier and bucket
        identifier = self._get_identifier(request)
        bucket = self._get_bucket(identifier)

        # Try to consume token
        if bucket.consume():
            # Request allowed
            remaining = int(bucket.tokens)
            reset_seconds = int(bucket.capacity / bucket.refill_rate)

            logger.debug(
                "rate_limit_allowed",
                identifier=identifier,
                remaining=remaining,
                path=request.url.path,
            )

            # Process request
            response = await call_next(request)

            # Add rate limit headers
            response.headers["X-RateLimit-Limit"] = str(self.requests_per_minute)
            response.headers["X-RateLimit-Remaining"] = str(remaining)
            response.headers["XXX-RateLimit-ResetXX"] = str(reset_seconds)

            # Periodic cleanup
            self._cleanup_old_buckets()

            return response
        else:
            # Rate limit exceeded
            wait_time = bucket.get_wait_time()
            retry_after = int(wait_time) + 1  # Round up

            logger.warning(
                "rate_limit_exceeded",
                identifier=identifier,
                path=request.url.path,
                wait_time_seconds=retry_after,
            )

            # Return 429 Too Many Requests
            return JSONResponse(
                status_code=429,
                content={
                    "error": "Rate limit exceeded",
                    "message": f"Too many requests. Please retry after {retry_after} seconds.",
                    "retry_after": retry_after,
                    "limit": self.requests_per_minute,
                },
                headers={
                    "X-RateLimit-Limit": str(self.requests_per_minute),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(retry_after),
                    "Retry-After": str(retry_after),
                },
            )

    async def xǁRateLimitMiddlewareǁdispatch__mutmut_45(self, request: Request, call_next):
        """
        Process request with rate limiting

        Args:
            request: FastAPI request
            call_next: Next middleware in chain

        Returns:
            Response or 429 Too Many Requests
        """
        # Skip rate limiting for health checks
        if request.url.path in ["/health", "/", "/docs", "/redoc", "/openapi.json"]:
            return await call_next(request)

        # Get identifier and bucket
        identifier = self._get_identifier(request)
        bucket = self._get_bucket(identifier)

        # Try to consume token
        if bucket.consume():
            # Request allowed
            remaining = int(bucket.tokens)
            reset_seconds = int(bucket.capacity / bucket.refill_rate)

            logger.debug(
                "rate_limit_allowed",
                identifier=identifier,
                remaining=remaining,
                path=request.url.path,
            )

            # Process request
            response = await call_next(request)

            # Add rate limit headers
            response.headers["X-RateLimit-Limit"] = str(self.requests_per_minute)
            response.headers["X-RateLimit-Remaining"] = str(remaining)
            response.headers["x-ratelimit-reset"] = str(reset_seconds)

            # Periodic cleanup
            self._cleanup_old_buckets()

            return response
        else:
            # Rate limit exceeded
            wait_time = bucket.get_wait_time()
            retry_after = int(wait_time) + 1  # Round up

            logger.warning(
                "rate_limit_exceeded",
                identifier=identifier,
                path=request.url.path,
                wait_time_seconds=retry_after,
            )

            # Return 429 Too Many Requests
            return JSONResponse(
                status_code=429,
                content={
                    "error": "Rate limit exceeded",
                    "message": f"Too many requests. Please retry after {retry_after} seconds.",
                    "retry_after": retry_after,
                    "limit": self.requests_per_minute,
                },
                headers={
                    "X-RateLimit-Limit": str(self.requests_per_minute),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(retry_after),
                    "Retry-After": str(retry_after),
                },
            )

    async def xǁRateLimitMiddlewareǁdispatch__mutmut_46(self, request: Request, call_next):
        """
        Process request with rate limiting

        Args:
            request: FastAPI request
            call_next: Next middleware in chain

        Returns:
            Response or 429 Too Many Requests
        """
        # Skip rate limiting for health checks
        if request.url.path in ["/health", "/", "/docs", "/redoc", "/openapi.json"]:
            return await call_next(request)

        # Get identifier and bucket
        identifier = self._get_identifier(request)
        bucket = self._get_bucket(identifier)

        # Try to consume token
        if bucket.consume():
            # Request allowed
            remaining = int(bucket.tokens)
            reset_seconds = int(bucket.capacity / bucket.refill_rate)

            logger.debug(
                "rate_limit_allowed",
                identifier=identifier,
                remaining=remaining,
                path=request.url.path,
            )

            # Process request
            response = await call_next(request)

            # Add rate limit headers
            response.headers["X-RateLimit-Limit"] = str(self.requests_per_minute)
            response.headers["X-RateLimit-Remaining"] = str(remaining)
            response.headers["X-RATELIMIT-RESET"] = str(reset_seconds)

            # Periodic cleanup
            self._cleanup_old_buckets()

            return response
        else:
            # Rate limit exceeded
            wait_time = bucket.get_wait_time()
            retry_after = int(wait_time) + 1  # Round up

            logger.warning(
                "rate_limit_exceeded",
                identifier=identifier,
                path=request.url.path,
                wait_time_seconds=retry_after,
            )

            # Return 429 Too Many Requests
            return JSONResponse(
                status_code=429,
                content={
                    "error": "Rate limit exceeded",
                    "message": f"Too many requests. Please retry after {retry_after} seconds.",
                    "retry_after": retry_after,
                    "limit": self.requests_per_minute,
                },
                headers={
                    "X-RateLimit-Limit": str(self.requests_per_minute),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(retry_after),
                    "Retry-After": str(retry_after),
                },
            )

    async def xǁRateLimitMiddlewareǁdispatch__mutmut_47(self, request: Request, call_next):
        """
        Process request with rate limiting

        Args:
            request: FastAPI request
            call_next: Next middleware in chain

        Returns:
            Response or 429 Too Many Requests
        """
        # Skip rate limiting for health checks
        if request.url.path in ["/health", "/", "/docs", "/redoc", "/openapi.json"]:
            return await call_next(request)

        # Get identifier and bucket
        identifier = self._get_identifier(request)
        bucket = self._get_bucket(identifier)

        # Try to consume token
        if bucket.consume():
            # Request allowed
            remaining = int(bucket.tokens)
            reset_seconds = int(bucket.capacity / bucket.refill_rate)

            logger.debug(
                "rate_limit_allowed",
                identifier=identifier,
                remaining=remaining,
                path=request.url.path,
            )

            # Process request
            response = await call_next(request)

            # Add rate limit headers
            response.headers["X-RateLimit-Limit"] = str(self.requests_per_minute)
            response.headers["X-RateLimit-Remaining"] = str(remaining)
            response.headers["X-RateLimit-Reset"] = str(None)

            # Periodic cleanup
            self._cleanup_old_buckets()

            return response
        else:
            # Rate limit exceeded
            wait_time = bucket.get_wait_time()
            retry_after = int(wait_time) + 1  # Round up

            logger.warning(
                "rate_limit_exceeded",
                identifier=identifier,
                path=request.url.path,
                wait_time_seconds=retry_after,
            )

            # Return 429 Too Many Requests
            return JSONResponse(
                status_code=429,
                content={
                    "error": "Rate limit exceeded",
                    "message": f"Too many requests. Please retry after {retry_after} seconds.",
                    "retry_after": retry_after,
                    "limit": self.requests_per_minute,
                },
                headers={
                    "X-RateLimit-Limit": str(self.requests_per_minute),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(retry_after),
                    "Retry-After": str(retry_after),
                },
            )

    async def xǁRateLimitMiddlewareǁdispatch__mutmut_48(self, request: Request, call_next):
        """
        Process request with rate limiting

        Args:
            request: FastAPI request
            call_next: Next middleware in chain

        Returns:
            Response or 429 Too Many Requests
        """
        # Skip rate limiting for health checks
        if request.url.path in ["/health", "/", "/docs", "/redoc", "/openapi.json"]:
            return await call_next(request)

        # Get identifier and bucket
        identifier = self._get_identifier(request)
        bucket = self._get_bucket(identifier)

        # Try to consume token
        if bucket.consume():
            # Request allowed
            remaining = int(bucket.tokens)
            reset_seconds = int(bucket.capacity / bucket.refill_rate)

            logger.debug(
                "rate_limit_allowed",
                identifier=identifier,
                remaining=remaining,
                path=request.url.path,
            )

            # Process request
            response = await call_next(request)

            # Add rate limit headers
            response.headers["X-RateLimit-Limit"] = str(self.requests_per_minute)
            response.headers["X-RateLimit-Remaining"] = str(remaining)
            response.headers["X-RateLimit-Reset"] = str(reset_seconds)

            # Periodic cleanup
            self._cleanup_old_buckets()

            return response
        else:
            # Rate limit exceeded
            wait_time = None
            retry_after = int(wait_time) + 1  # Round up

            logger.warning(
                "rate_limit_exceeded",
                identifier=identifier,
                path=request.url.path,
                wait_time_seconds=retry_after,
            )

            # Return 429 Too Many Requests
            return JSONResponse(
                status_code=429,
                content={
                    "error": "Rate limit exceeded",
                    "message": f"Too many requests. Please retry after {retry_after} seconds.",
                    "retry_after": retry_after,
                    "limit": self.requests_per_minute,
                },
                headers={
                    "X-RateLimit-Limit": str(self.requests_per_minute),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(retry_after),
                    "Retry-After": str(retry_after),
                },
            )

    async def xǁRateLimitMiddlewareǁdispatch__mutmut_49(self, request: Request, call_next):
        """
        Process request with rate limiting

        Args:
            request: FastAPI request
            call_next: Next middleware in chain

        Returns:
            Response or 429 Too Many Requests
        """
        # Skip rate limiting for health checks
        if request.url.path in ["/health", "/", "/docs", "/redoc", "/openapi.json"]:
            return await call_next(request)

        # Get identifier and bucket
        identifier = self._get_identifier(request)
        bucket = self._get_bucket(identifier)

        # Try to consume token
        if bucket.consume():
            # Request allowed
            remaining = int(bucket.tokens)
            reset_seconds = int(bucket.capacity / bucket.refill_rate)

            logger.debug(
                "rate_limit_allowed",
                identifier=identifier,
                remaining=remaining,
                path=request.url.path,
            )

            # Process request
            response = await call_next(request)

            # Add rate limit headers
            response.headers["X-RateLimit-Limit"] = str(self.requests_per_minute)
            response.headers["X-RateLimit-Remaining"] = str(remaining)
            response.headers["X-RateLimit-Reset"] = str(reset_seconds)

            # Periodic cleanup
            self._cleanup_old_buckets()

            return response
        else:
            # Rate limit exceeded
            wait_time = bucket.get_wait_time()
            retry_after = None  # Round up

            logger.warning(
                "rate_limit_exceeded",
                identifier=identifier,
                path=request.url.path,
                wait_time_seconds=retry_after,
            )

            # Return 429 Too Many Requests
            return JSONResponse(
                status_code=429,
                content={
                    "error": "Rate limit exceeded",
                    "message": f"Too many requests. Please retry after {retry_after} seconds.",
                    "retry_after": retry_after,
                    "limit": self.requests_per_minute,
                },
                headers={
                    "X-RateLimit-Limit": str(self.requests_per_minute),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(retry_after),
                    "Retry-After": str(retry_after),
                },
            )

    async def xǁRateLimitMiddlewareǁdispatch__mutmut_50(self, request: Request, call_next):
        """
        Process request with rate limiting

        Args:
            request: FastAPI request
            call_next: Next middleware in chain

        Returns:
            Response or 429 Too Many Requests
        """
        # Skip rate limiting for health checks
        if request.url.path in ["/health", "/", "/docs", "/redoc", "/openapi.json"]:
            return await call_next(request)

        # Get identifier and bucket
        identifier = self._get_identifier(request)
        bucket = self._get_bucket(identifier)

        # Try to consume token
        if bucket.consume():
            # Request allowed
            remaining = int(bucket.tokens)
            reset_seconds = int(bucket.capacity / bucket.refill_rate)

            logger.debug(
                "rate_limit_allowed",
                identifier=identifier,
                remaining=remaining,
                path=request.url.path,
            )

            # Process request
            response = await call_next(request)

            # Add rate limit headers
            response.headers["X-RateLimit-Limit"] = str(self.requests_per_minute)
            response.headers["X-RateLimit-Remaining"] = str(remaining)
            response.headers["X-RateLimit-Reset"] = str(reset_seconds)

            # Periodic cleanup
            self._cleanup_old_buckets()

            return response
        else:
            # Rate limit exceeded
            wait_time = bucket.get_wait_time()
            retry_after = int(wait_time) - 1  # Round up

            logger.warning(
                "rate_limit_exceeded",
                identifier=identifier,
                path=request.url.path,
                wait_time_seconds=retry_after,
            )

            # Return 429 Too Many Requests
            return JSONResponse(
                status_code=429,
                content={
                    "error": "Rate limit exceeded",
                    "message": f"Too many requests. Please retry after {retry_after} seconds.",
                    "retry_after": retry_after,
                    "limit": self.requests_per_minute,
                },
                headers={
                    "X-RateLimit-Limit": str(self.requests_per_minute),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(retry_after),
                    "Retry-After": str(retry_after),
                },
            )

    async def xǁRateLimitMiddlewareǁdispatch__mutmut_51(self, request: Request, call_next):
        """
        Process request with rate limiting

        Args:
            request: FastAPI request
            call_next: Next middleware in chain

        Returns:
            Response or 429 Too Many Requests
        """
        # Skip rate limiting for health checks
        if request.url.path in ["/health", "/", "/docs", "/redoc", "/openapi.json"]:
            return await call_next(request)

        # Get identifier and bucket
        identifier = self._get_identifier(request)
        bucket = self._get_bucket(identifier)

        # Try to consume token
        if bucket.consume():
            # Request allowed
            remaining = int(bucket.tokens)
            reset_seconds = int(bucket.capacity / bucket.refill_rate)

            logger.debug(
                "rate_limit_allowed",
                identifier=identifier,
                remaining=remaining,
                path=request.url.path,
            )

            # Process request
            response = await call_next(request)

            # Add rate limit headers
            response.headers["X-RateLimit-Limit"] = str(self.requests_per_minute)
            response.headers["X-RateLimit-Remaining"] = str(remaining)
            response.headers["X-RateLimit-Reset"] = str(reset_seconds)

            # Periodic cleanup
            self._cleanup_old_buckets()

            return response
        else:
            # Rate limit exceeded
            wait_time = bucket.get_wait_time()
            retry_after = int(None) + 1  # Round up

            logger.warning(
                "rate_limit_exceeded",
                identifier=identifier,
                path=request.url.path,
                wait_time_seconds=retry_after,
            )

            # Return 429 Too Many Requests
            return JSONResponse(
                status_code=429,
                content={
                    "error": "Rate limit exceeded",
                    "message": f"Too many requests. Please retry after {retry_after} seconds.",
                    "retry_after": retry_after,
                    "limit": self.requests_per_minute,
                },
                headers={
                    "X-RateLimit-Limit": str(self.requests_per_minute),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(retry_after),
                    "Retry-After": str(retry_after),
                },
            )

    async def xǁRateLimitMiddlewareǁdispatch__mutmut_52(self, request: Request, call_next):
        """
        Process request with rate limiting

        Args:
            request: FastAPI request
            call_next: Next middleware in chain

        Returns:
            Response or 429 Too Many Requests
        """
        # Skip rate limiting for health checks
        if request.url.path in ["/health", "/", "/docs", "/redoc", "/openapi.json"]:
            return await call_next(request)

        # Get identifier and bucket
        identifier = self._get_identifier(request)
        bucket = self._get_bucket(identifier)

        # Try to consume token
        if bucket.consume():
            # Request allowed
            remaining = int(bucket.tokens)
            reset_seconds = int(bucket.capacity / bucket.refill_rate)

            logger.debug(
                "rate_limit_allowed",
                identifier=identifier,
                remaining=remaining,
                path=request.url.path,
            )

            # Process request
            response = await call_next(request)

            # Add rate limit headers
            response.headers["X-RateLimit-Limit"] = str(self.requests_per_minute)
            response.headers["X-RateLimit-Remaining"] = str(remaining)
            response.headers["X-RateLimit-Reset"] = str(reset_seconds)

            # Periodic cleanup
            self._cleanup_old_buckets()

            return response
        else:
            # Rate limit exceeded
            wait_time = bucket.get_wait_time()
            retry_after = int(wait_time) + 2  # Round up

            logger.warning(
                "rate_limit_exceeded",
                identifier=identifier,
                path=request.url.path,
                wait_time_seconds=retry_after,
            )

            # Return 429 Too Many Requests
            return JSONResponse(
                status_code=429,
                content={
                    "error": "Rate limit exceeded",
                    "message": f"Too many requests. Please retry after {retry_after} seconds.",
                    "retry_after": retry_after,
                    "limit": self.requests_per_minute,
                },
                headers={
                    "X-RateLimit-Limit": str(self.requests_per_minute),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(retry_after),
                    "Retry-After": str(retry_after),
                },
            )

    async def xǁRateLimitMiddlewareǁdispatch__mutmut_53(self, request: Request, call_next):
        """
        Process request with rate limiting

        Args:
            request: FastAPI request
            call_next: Next middleware in chain

        Returns:
            Response or 429 Too Many Requests
        """
        # Skip rate limiting for health checks
        if request.url.path in ["/health", "/", "/docs", "/redoc", "/openapi.json"]:
            return await call_next(request)

        # Get identifier and bucket
        identifier = self._get_identifier(request)
        bucket = self._get_bucket(identifier)

        # Try to consume token
        if bucket.consume():
            # Request allowed
            remaining = int(bucket.tokens)
            reset_seconds = int(bucket.capacity / bucket.refill_rate)

            logger.debug(
                "rate_limit_allowed",
                identifier=identifier,
                remaining=remaining,
                path=request.url.path,
            )

            # Process request
            response = await call_next(request)

            # Add rate limit headers
            response.headers["X-RateLimit-Limit"] = str(self.requests_per_minute)
            response.headers["X-RateLimit-Remaining"] = str(remaining)
            response.headers["X-RateLimit-Reset"] = str(reset_seconds)

            # Periodic cleanup
            self._cleanup_old_buckets()

            return response
        else:
            # Rate limit exceeded
            wait_time = bucket.get_wait_time()
            retry_after = int(wait_time) + 1  # Round up

            logger.warning(
                None,
                identifier=identifier,
                path=request.url.path,
                wait_time_seconds=retry_after,
            )

            # Return 429 Too Many Requests
            return JSONResponse(
                status_code=429,
                content={
                    "error": "Rate limit exceeded",
                    "message": f"Too many requests. Please retry after {retry_after} seconds.",
                    "retry_after": retry_after,
                    "limit": self.requests_per_minute,
                },
                headers={
                    "X-RateLimit-Limit": str(self.requests_per_minute),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(retry_after),
                    "Retry-After": str(retry_after),
                },
            )

    async def xǁRateLimitMiddlewareǁdispatch__mutmut_54(self, request: Request, call_next):
        """
        Process request with rate limiting

        Args:
            request: FastAPI request
            call_next: Next middleware in chain

        Returns:
            Response or 429 Too Many Requests
        """
        # Skip rate limiting for health checks
        if request.url.path in ["/health", "/", "/docs", "/redoc", "/openapi.json"]:
            return await call_next(request)

        # Get identifier and bucket
        identifier = self._get_identifier(request)
        bucket = self._get_bucket(identifier)

        # Try to consume token
        if bucket.consume():
            # Request allowed
            remaining = int(bucket.tokens)
            reset_seconds = int(bucket.capacity / bucket.refill_rate)

            logger.debug(
                "rate_limit_allowed",
                identifier=identifier,
                remaining=remaining,
                path=request.url.path,
            )

            # Process request
            response = await call_next(request)

            # Add rate limit headers
            response.headers["X-RateLimit-Limit"] = str(self.requests_per_minute)
            response.headers["X-RateLimit-Remaining"] = str(remaining)
            response.headers["X-RateLimit-Reset"] = str(reset_seconds)

            # Periodic cleanup
            self._cleanup_old_buckets()

            return response
        else:
            # Rate limit exceeded
            wait_time = bucket.get_wait_time()
            retry_after = int(wait_time) + 1  # Round up

            logger.warning(
                "rate_limit_exceeded",
                identifier=None,
                path=request.url.path,
                wait_time_seconds=retry_after,
            )

            # Return 429 Too Many Requests
            return JSONResponse(
                status_code=429,
                content={
                    "error": "Rate limit exceeded",
                    "message": f"Too many requests. Please retry after {retry_after} seconds.",
                    "retry_after": retry_after,
                    "limit": self.requests_per_minute,
                },
                headers={
                    "X-RateLimit-Limit": str(self.requests_per_minute),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(retry_after),
                    "Retry-After": str(retry_after),
                },
            )

    async def xǁRateLimitMiddlewareǁdispatch__mutmut_55(self, request: Request, call_next):
        """
        Process request with rate limiting

        Args:
            request: FastAPI request
            call_next: Next middleware in chain

        Returns:
            Response or 429 Too Many Requests
        """
        # Skip rate limiting for health checks
        if request.url.path in ["/health", "/", "/docs", "/redoc", "/openapi.json"]:
            return await call_next(request)

        # Get identifier and bucket
        identifier = self._get_identifier(request)
        bucket = self._get_bucket(identifier)

        # Try to consume token
        if bucket.consume():
            # Request allowed
            remaining = int(bucket.tokens)
            reset_seconds = int(bucket.capacity / bucket.refill_rate)

            logger.debug(
                "rate_limit_allowed",
                identifier=identifier,
                remaining=remaining,
                path=request.url.path,
            )

            # Process request
            response = await call_next(request)

            # Add rate limit headers
            response.headers["X-RateLimit-Limit"] = str(self.requests_per_minute)
            response.headers["X-RateLimit-Remaining"] = str(remaining)
            response.headers["X-RateLimit-Reset"] = str(reset_seconds)

            # Periodic cleanup
            self._cleanup_old_buckets()

            return response
        else:
            # Rate limit exceeded
            wait_time = bucket.get_wait_time()
            retry_after = int(wait_time) + 1  # Round up

            logger.warning(
                "rate_limit_exceeded",
                identifier=identifier,
                path=None,
                wait_time_seconds=retry_after,
            )

            # Return 429 Too Many Requests
            return JSONResponse(
                status_code=429,
                content={
                    "error": "Rate limit exceeded",
                    "message": f"Too many requests. Please retry after {retry_after} seconds.",
                    "retry_after": retry_after,
                    "limit": self.requests_per_minute,
                },
                headers={
                    "X-RateLimit-Limit": str(self.requests_per_minute),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(retry_after),
                    "Retry-After": str(retry_after),
                },
            )

    async def xǁRateLimitMiddlewareǁdispatch__mutmut_56(self, request: Request, call_next):
        """
        Process request with rate limiting

        Args:
            request: FastAPI request
            call_next: Next middleware in chain

        Returns:
            Response or 429 Too Many Requests
        """
        # Skip rate limiting for health checks
        if request.url.path in ["/health", "/", "/docs", "/redoc", "/openapi.json"]:
            return await call_next(request)

        # Get identifier and bucket
        identifier = self._get_identifier(request)
        bucket = self._get_bucket(identifier)

        # Try to consume token
        if bucket.consume():
            # Request allowed
            remaining = int(bucket.tokens)
            reset_seconds = int(bucket.capacity / bucket.refill_rate)

            logger.debug(
                "rate_limit_allowed",
                identifier=identifier,
                remaining=remaining,
                path=request.url.path,
            )

            # Process request
            response = await call_next(request)

            # Add rate limit headers
            response.headers["X-RateLimit-Limit"] = str(self.requests_per_minute)
            response.headers["X-RateLimit-Remaining"] = str(remaining)
            response.headers["X-RateLimit-Reset"] = str(reset_seconds)

            # Periodic cleanup
            self._cleanup_old_buckets()

            return response
        else:
            # Rate limit exceeded
            wait_time = bucket.get_wait_time()
            retry_after = int(wait_time) + 1  # Round up

            logger.warning(
                "rate_limit_exceeded",
                identifier=identifier,
                path=request.url.path,
                wait_time_seconds=None,
            )

            # Return 429 Too Many Requests
            return JSONResponse(
                status_code=429,
                content={
                    "error": "Rate limit exceeded",
                    "message": f"Too many requests. Please retry after {retry_after} seconds.",
                    "retry_after": retry_after,
                    "limit": self.requests_per_minute,
                },
                headers={
                    "X-RateLimit-Limit": str(self.requests_per_minute),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(retry_after),
                    "Retry-After": str(retry_after),
                },
            )

    async def xǁRateLimitMiddlewareǁdispatch__mutmut_57(self, request: Request, call_next):
        """
        Process request with rate limiting

        Args:
            request: FastAPI request
            call_next: Next middleware in chain

        Returns:
            Response or 429 Too Many Requests
        """
        # Skip rate limiting for health checks
        if request.url.path in ["/health", "/", "/docs", "/redoc", "/openapi.json"]:
            return await call_next(request)

        # Get identifier and bucket
        identifier = self._get_identifier(request)
        bucket = self._get_bucket(identifier)

        # Try to consume token
        if bucket.consume():
            # Request allowed
            remaining = int(bucket.tokens)
            reset_seconds = int(bucket.capacity / bucket.refill_rate)

            logger.debug(
                "rate_limit_allowed",
                identifier=identifier,
                remaining=remaining,
                path=request.url.path,
            )

            # Process request
            response = await call_next(request)

            # Add rate limit headers
            response.headers["X-RateLimit-Limit"] = str(self.requests_per_minute)
            response.headers["X-RateLimit-Remaining"] = str(remaining)
            response.headers["X-RateLimit-Reset"] = str(reset_seconds)

            # Periodic cleanup
            self._cleanup_old_buckets()

            return response
        else:
            # Rate limit exceeded
            wait_time = bucket.get_wait_time()
            retry_after = int(wait_time) + 1  # Round up

            logger.warning(
                identifier=identifier,
                path=request.url.path,
                wait_time_seconds=retry_after,
            )

            # Return 429 Too Many Requests
            return JSONResponse(
                status_code=429,
                content={
                    "error": "Rate limit exceeded",
                    "message": f"Too many requests. Please retry after {retry_after} seconds.",
                    "retry_after": retry_after,
                    "limit": self.requests_per_minute,
                },
                headers={
                    "X-RateLimit-Limit": str(self.requests_per_minute),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(retry_after),
                    "Retry-After": str(retry_after),
                },
            )

    async def xǁRateLimitMiddlewareǁdispatch__mutmut_58(self, request: Request, call_next):
        """
        Process request with rate limiting

        Args:
            request: FastAPI request
            call_next: Next middleware in chain

        Returns:
            Response or 429 Too Many Requests
        """
        # Skip rate limiting for health checks
        if request.url.path in ["/health", "/", "/docs", "/redoc", "/openapi.json"]:
            return await call_next(request)

        # Get identifier and bucket
        identifier = self._get_identifier(request)
        bucket = self._get_bucket(identifier)

        # Try to consume token
        if bucket.consume():
            # Request allowed
            remaining = int(bucket.tokens)
            reset_seconds = int(bucket.capacity / bucket.refill_rate)

            logger.debug(
                "rate_limit_allowed",
                identifier=identifier,
                remaining=remaining,
                path=request.url.path,
            )

            # Process request
            response = await call_next(request)

            # Add rate limit headers
            response.headers["X-RateLimit-Limit"] = str(self.requests_per_minute)
            response.headers["X-RateLimit-Remaining"] = str(remaining)
            response.headers["X-RateLimit-Reset"] = str(reset_seconds)

            # Periodic cleanup
            self._cleanup_old_buckets()

            return response
        else:
            # Rate limit exceeded
            wait_time = bucket.get_wait_time()
            retry_after = int(wait_time) + 1  # Round up

            logger.warning(
                "rate_limit_exceeded",
                path=request.url.path,
                wait_time_seconds=retry_after,
            )

            # Return 429 Too Many Requests
            return JSONResponse(
                status_code=429,
                content={
                    "error": "Rate limit exceeded",
                    "message": f"Too many requests. Please retry after {retry_after} seconds.",
                    "retry_after": retry_after,
                    "limit": self.requests_per_minute,
                },
                headers={
                    "X-RateLimit-Limit": str(self.requests_per_minute),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(retry_after),
                    "Retry-After": str(retry_after),
                },
            )

    async def xǁRateLimitMiddlewareǁdispatch__mutmut_59(self, request: Request, call_next):
        """
        Process request with rate limiting

        Args:
            request: FastAPI request
            call_next: Next middleware in chain

        Returns:
            Response or 429 Too Many Requests
        """
        # Skip rate limiting for health checks
        if request.url.path in ["/health", "/", "/docs", "/redoc", "/openapi.json"]:
            return await call_next(request)

        # Get identifier and bucket
        identifier = self._get_identifier(request)
        bucket = self._get_bucket(identifier)

        # Try to consume token
        if bucket.consume():
            # Request allowed
            remaining = int(bucket.tokens)
            reset_seconds = int(bucket.capacity / bucket.refill_rate)

            logger.debug(
                "rate_limit_allowed",
                identifier=identifier,
                remaining=remaining,
                path=request.url.path,
            )

            # Process request
            response = await call_next(request)

            # Add rate limit headers
            response.headers["X-RateLimit-Limit"] = str(self.requests_per_minute)
            response.headers["X-RateLimit-Remaining"] = str(remaining)
            response.headers["X-RateLimit-Reset"] = str(reset_seconds)

            # Periodic cleanup
            self._cleanup_old_buckets()

            return response
        else:
            # Rate limit exceeded
            wait_time = bucket.get_wait_time()
            retry_after = int(wait_time) + 1  # Round up

            logger.warning(
                "rate_limit_exceeded",
                identifier=identifier,
                wait_time_seconds=retry_after,
            )

            # Return 429 Too Many Requests
            return JSONResponse(
                status_code=429,
                content={
                    "error": "Rate limit exceeded",
                    "message": f"Too many requests. Please retry after {retry_after} seconds.",
                    "retry_after": retry_after,
                    "limit": self.requests_per_minute,
                },
                headers={
                    "X-RateLimit-Limit": str(self.requests_per_minute),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(retry_after),
                    "Retry-After": str(retry_after),
                },
            )

    async def xǁRateLimitMiddlewareǁdispatch__mutmut_60(self, request: Request, call_next):
        """
        Process request with rate limiting

        Args:
            request: FastAPI request
            call_next: Next middleware in chain

        Returns:
            Response or 429 Too Many Requests
        """
        # Skip rate limiting for health checks
        if request.url.path in ["/health", "/", "/docs", "/redoc", "/openapi.json"]:
            return await call_next(request)

        # Get identifier and bucket
        identifier = self._get_identifier(request)
        bucket = self._get_bucket(identifier)

        # Try to consume token
        if bucket.consume():
            # Request allowed
            remaining = int(bucket.tokens)
            reset_seconds = int(bucket.capacity / bucket.refill_rate)

            logger.debug(
                "rate_limit_allowed",
                identifier=identifier,
                remaining=remaining,
                path=request.url.path,
            )

            # Process request
            response = await call_next(request)

            # Add rate limit headers
            response.headers["X-RateLimit-Limit"] = str(self.requests_per_minute)
            response.headers["X-RateLimit-Remaining"] = str(remaining)
            response.headers["X-RateLimit-Reset"] = str(reset_seconds)

            # Periodic cleanup
            self._cleanup_old_buckets()

            return response
        else:
            # Rate limit exceeded
            wait_time = bucket.get_wait_time()
            retry_after = int(wait_time) + 1  # Round up

            logger.warning(
                "rate_limit_exceeded",
                identifier=identifier,
                path=request.url.path,
                )

            # Return 429 Too Many Requests
            return JSONResponse(
                status_code=429,
                content={
                    "error": "Rate limit exceeded",
                    "message": f"Too many requests. Please retry after {retry_after} seconds.",
                    "retry_after": retry_after,
                    "limit": self.requests_per_minute,
                },
                headers={
                    "X-RateLimit-Limit": str(self.requests_per_minute),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(retry_after),
                    "Retry-After": str(retry_after),
                },
            )

    async def xǁRateLimitMiddlewareǁdispatch__mutmut_61(self, request: Request, call_next):
        """
        Process request with rate limiting

        Args:
            request: FastAPI request
            call_next: Next middleware in chain

        Returns:
            Response or 429 Too Many Requests
        """
        # Skip rate limiting for health checks
        if request.url.path in ["/health", "/", "/docs", "/redoc", "/openapi.json"]:
            return await call_next(request)

        # Get identifier and bucket
        identifier = self._get_identifier(request)
        bucket = self._get_bucket(identifier)

        # Try to consume token
        if bucket.consume():
            # Request allowed
            remaining = int(bucket.tokens)
            reset_seconds = int(bucket.capacity / bucket.refill_rate)

            logger.debug(
                "rate_limit_allowed",
                identifier=identifier,
                remaining=remaining,
                path=request.url.path,
            )

            # Process request
            response = await call_next(request)

            # Add rate limit headers
            response.headers["X-RateLimit-Limit"] = str(self.requests_per_minute)
            response.headers["X-RateLimit-Remaining"] = str(remaining)
            response.headers["X-RateLimit-Reset"] = str(reset_seconds)

            # Periodic cleanup
            self._cleanup_old_buckets()

            return response
        else:
            # Rate limit exceeded
            wait_time = bucket.get_wait_time()
            retry_after = int(wait_time) + 1  # Round up

            logger.warning(
                "XXrate_limit_exceededXX",
                identifier=identifier,
                path=request.url.path,
                wait_time_seconds=retry_after,
            )

            # Return 429 Too Many Requests
            return JSONResponse(
                status_code=429,
                content={
                    "error": "Rate limit exceeded",
                    "message": f"Too many requests. Please retry after {retry_after} seconds.",
                    "retry_after": retry_after,
                    "limit": self.requests_per_minute,
                },
                headers={
                    "X-RateLimit-Limit": str(self.requests_per_minute),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(retry_after),
                    "Retry-After": str(retry_after),
                },
            )

    async def xǁRateLimitMiddlewareǁdispatch__mutmut_62(self, request: Request, call_next):
        """
        Process request with rate limiting

        Args:
            request: FastAPI request
            call_next: Next middleware in chain

        Returns:
            Response or 429 Too Many Requests
        """
        # Skip rate limiting for health checks
        if request.url.path in ["/health", "/", "/docs", "/redoc", "/openapi.json"]:
            return await call_next(request)

        # Get identifier and bucket
        identifier = self._get_identifier(request)
        bucket = self._get_bucket(identifier)

        # Try to consume token
        if bucket.consume():
            # Request allowed
            remaining = int(bucket.tokens)
            reset_seconds = int(bucket.capacity / bucket.refill_rate)

            logger.debug(
                "rate_limit_allowed",
                identifier=identifier,
                remaining=remaining,
                path=request.url.path,
            )

            # Process request
            response = await call_next(request)

            # Add rate limit headers
            response.headers["X-RateLimit-Limit"] = str(self.requests_per_minute)
            response.headers["X-RateLimit-Remaining"] = str(remaining)
            response.headers["X-RateLimit-Reset"] = str(reset_seconds)

            # Periodic cleanup
            self._cleanup_old_buckets()

            return response
        else:
            # Rate limit exceeded
            wait_time = bucket.get_wait_time()
            retry_after = int(wait_time) + 1  # Round up

            logger.warning(
                "RATE_LIMIT_EXCEEDED",
                identifier=identifier,
                path=request.url.path,
                wait_time_seconds=retry_after,
            )

            # Return 429 Too Many Requests
            return JSONResponse(
                status_code=429,
                content={
                    "error": "Rate limit exceeded",
                    "message": f"Too many requests. Please retry after {retry_after} seconds.",
                    "retry_after": retry_after,
                    "limit": self.requests_per_minute,
                },
                headers={
                    "X-RateLimit-Limit": str(self.requests_per_minute),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(retry_after),
                    "Retry-After": str(retry_after),
                },
            )

    async def xǁRateLimitMiddlewareǁdispatch__mutmut_63(self, request: Request, call_next):
        """
        Process request with rate limiting

        Args:
            request: FastAPI request
            call_next: Next middleware in chain

        Returns:
            Response or 429 Too Many Requests
        """
        # Skip rate limiting for health checks
        if request.url.path in ["/health", "/", "/docs", "/redoc", "/openapi.json"]:
            return await call_next(request)

        # Get identifier and bucket
        identifier = self._get_identifier(request)
        bucket = self._get_bucket(identifier)

        # Try to consume token
        if bucket.consume():
            # Request allowed
            remaining = int(bucket.tokens)
            reset_seconds = int(bucket.capacity / bucket.refill_rate)

            logger.debug(
                "rate_limit_allowed",
                identifier=identifier,
                remaining=remaining,
                path=request.url.path,
            )

            # Process request
            response = await call_next(request)

            # Add rate limit headers
            response.headers["X-RateLimit-Limit"] = str(self.requests_per_minute)
            response.headers["X-RateLimit-Remaining"] = str(remaining)
            response.headers["X-RateLimit-Reset"] = str(reset_seconds)

            # Periodic cleanup
            self._cleanup_old_buckets()

            return response
        else:
            # Rate limit exceeded
            wait_time = bucket.get_wait_time()
            retry_after = int(wait_time) + 1  # Round up

            logger.warning(
                "rate_limit_exceeded",
                identifier=identifier,
                path=request.url.path,
                wait_time_seconds=retry_after,
            )

            # Return 429 Too Many Requests
            return JSONResponse(
                status_code=None,
                content={
                    "error": "Rate limit exceeded",
                    "message": f"Too many requests. Please retry after {retry_after} seconds.",
                    "retry_after": retry_after,
                    "limit": self.requests_per_minute,
                },
                headers={
                    "X-RateLimit-Limit": str(self.requests_per_minute),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(retry_after),
                    "Retry-After": str(retry_after),
                },
            )

    async def xǁRateLimitMiddlewareǁdispatch__mutmut_64(self, request: Request, call_next):
        """
        Process request with rate limiting

        Args:
            request: FastAPI request
            call_next: Next middleware in chain

        Returns:
            Response or 429 Too Many Requests
        """
        # Skip rate limiting for health checks
        if request.url.path in ["/health", "/", "/docs", "/redoc", "/openapi.json"]:
            return await call_next(request)

        # Get identifier and bucket
        identifier = self._get_identifier(request)
        bucket = self._get_bucket(identifier)

        # Try to consume token
        if bucket.consume():
            # Request allowed
            remaining = int(bucket.tokens)
            reset_seconds = int(bucket.capacity / bucket.refill_rate)

            logger.debug(
                "rate_limit_allowed",
                identifier=identifier,
                remaining=remaining,
                path=request.url.path,
            )

            # Process request
            response = await call_next(request)

            # Add rate limit headers
            response.headers["X-RateLimit-Limit"] = str(self.requests_per_minute)
            response.headers["X-RateLimit-Remaining"] = str(remaining)
            response.headers["X-RateLimit-Reset"] = str(reset_seconds)

            # Periodic cleanup
            self._cleanup_old_buckets()

            return response
        else:
            # Rate limit exceeded
            wait_time = bucket.get_wait_time()
            retry_after = int(wait_time) + 1  # Round up

            logger.warning(
                "rate_limit_exceeded",
                identifier=identifier,
                path=request.url.path,
                wait_time_seconds=retry_after,
            )

            # Return 429 Too Many Requests
            return JSONResponse(
                status_code=429,
                content=None,
                headers={
                    "X-RateLimit-Limit": str(self.requests_per_minute),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(retry_after),
                    "Retry-After": str(retry_after),
                },
            )

    async def xǁRateLimitMiddlewareǁdispatch__mutmut_65(self, request: Request, call_next):
        """
        Process request with rate limiting

        Args:
            request: FastAPI request
            call_next: Next middleware in chain

        Returns:
            Response or 429 Too Many Requests
        """
        # Skip rate limiting for health checks
        if request.url.path in ["/health", "/", "/docs", "/redoc", "/openapi.json"]:
            return await call_next(request)

        # Get identifier and bucket
        identifier = self._get_identifier(request)
        bucket = self._get_bucket(identifier)

        # Try to consume token
        if bucket.consume():
            # Request allowed
            remaining = int(bucket.tokens)
            reset_seconds = int(bucket.capacity / bucket.refill_rate)

            logger.debug(
                "rate_limit_allowed",
                identifier=identifier,
                remaining=remaining,
                path=request.url.path,
            )

            # Process request
            response = await call_next(request)

            # Add rate limit headers
            response.headers["X-RateLimit-Limit"] = str(self.requests_per_minute)
            response.headers["X-RateLimit-Remaining"] = str(remaining)
            response.headers["X-RateLimit-Reset"] = str(reset_seconds)

            # Periodic cleanup
            self._cleanup_old_buckets()

            return response
        else:
            # Rate limit exceeded
            wait_time = bucket.get_wait_time()
            retry_after = int(wait_time) + 1  # Round up

            logger.warning(
                "rate_limit_exceeded",
                identifier=identifier,
                path=request.url.path,
                wait_time_seconds=retry_after,
            )

            # Return 429 Too Many Requests
            return JSONResponse(
                status_code=429,
                content={
                    "error": "Rate limit exceeded",
                    "message": f"Too many requests. Please retry after {retry_after} seconds.",
                    "retry_after": retry_after,
                    "limit": self.requests_per_minute,
                },
                headers=None,
            )

    async def xǁRateLimitMiddlewareǁdispatch__mutmut_66(self, request: Request, call_next):
        """
        Process request with rate limiting

        Args:
            request: FastAPI request
            call_next: Next middleware in chain

        Returns:
            Response or 429 Too Many Requests
        """
        # Skip rate limiting for health checks
        if request.url.path in ["/health", "/", "/docs", "/redoc", "/openapi.json"]:
            return await call_next(request)

        # Get identifier and bucket
        identifier = self._get_identifier(request)
        bucket = self._get_bucket(identifier)

        # Try to consume token
        if bucket.consume():
            # Request allowed
            remaining = int(bucket.tokens)
            reset_seconds = int(bucket.capacity / bucket.refill_rate)

            logger.debug(
                "rate_limit_allowed",
                identifier=identifier,
                remaining=remaining,
                path=request.url.path,
            )

            # Process request
            response = await call_next(request)

            # Add rate limit headers
            response.headers["X-RateLimit-Limit"] = str(self.requests_per_minute)
            response.headers["X-RateLimit-Remaining"] = str(remaining)
            response.headers["X-RateLimit-Reset"] = str(reset_seconds)

            # Periodic cleanup
            self._cleanup_old_buckets()

            return response
        else:
            # Rate limit exceeded
            wait_time = bucket.get_wait_time()
            retry_after = int(wait_time) + 1  # Round up

            logger.warning(
                "rate_limit_exceeded",
                identifier=identifier,
                path=request.url.path,
                wait_time_seconds=retry_after,
            )

            # Return 429 Too Many Requests
            return JSONResponse(
                content={
                    "error": "Rate limit exceeded",
                    "message": f"Too many requests. Please retry after {retry_after} seconds.",
                    "retry_after": retry_after,
                    "limit": self.requests_per_minute,
                },
                headers={
                    "X-RateLimit-Limit": str(self.requests_per_minute),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(retry_after),
                    "Retry-After": str(retry_after),
                },
            )

    async def xǁRateLimitMiddlewareǁdispatch__mutmut_67(self, request: Request, call_next):
        """
        Process request with rate limiting

        Args:
            request: FastAPI request
            call_next: Next middleware in chain

        Returns:
            Response or 429 Too Many Requests
        """
        # Skip rate limiting for health checks
        if request.url.path in ["/health", "/", "/docs", "/redoc", "/openapi.json"]:
            return await call_next(request)

        # Get identifier and bucket
        identifier = self._get_identifier(request)
        bucket = self._get_bucket(identifier)

        # Try to consume token
        if bucket.consume():
            # Request allowed
            remaining = int(bucket.tokens)
            reset_seconds = int(bucket.capacity / bucket.refill_rate)

            logger.debug(
                "rate_limit_allowed",
                identifier=identifier,
                remaining=remaining,
                path=request.url.path,
            )

            # Process request
            response = await call_next(request)

            # Add rate limit headers
            response.headers["X-RateLimit-Limit"] = str(self.requests_per_minute)
            response.headers["X-RateLimit-Remaining"] = str(remaining)
            response.headers["X-RateLimit-Reset"] = str(reset_seconds)

            # Periodic cleanup
            self._cleanup_old_buckets()

            return response
        else:
            # Rate limit exceeded
            wait_time = bucket.get_wait_time()
            retry_after = int(wait_time) + 1  # Round up

            logger.warning(
                "rate_limit_exceeded",
                identifier=identifier,
                path=request.url.path,
                wait_time_seconds=retry_after,
            )

            # Return 429 Too Many Requests
            return JSONResponse(
                status_code=429,
                headers={
                    "X-RateLimit-Limit": str(self.requests_per_minute),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(retry_after),
                    "Retry-After": str(retry_after),
                },
            )

    async def xǁRateLimitMiddlewareǁdispatch__mutmut_68(self, request: Request, call_next):
        """
        Process request with rate limiting

        Args:
            request: FastAPI request
            call_next: Next middleware in chain

        Returns:
            Response or 429 Too Many Requests
        """
        # Skip rate limiting for health checks
        if request.url.path in ["/health", "/", "/docs", "/redoc", "/openapi.json"]:
            return await call_next(request)

        # Get identifier and bucket
        identifier = self._get_identifier(request)
        bucket = self._get_bucket(identifier)

        # Try to consume token
        if bucket.consume():
            # Request allowed
            remaining = int(bucket.tokens)
            reset_seconds = int(bucket.capacity / bucket.refill_rate)

            logger.debug(
                "rate_limit_allowed",
                identifier=identifier,
                remaining=remaining,
                path=request.url.path,
            )

            # Process request
            response = await call_next(request)

            # Add rate limit headers
            response.headers["X-RateLimit-Limit"] = str(self.requests_per_minute)
            response.headers["X-RateLimit-Remaining"] = str(remaining)
            response.headers["X-RateLimit-Reset"] = str(reset_seconds)

            # Periodic cleanup
            self._cleanup_old_buckets()

            return response
        else:
            # Rate limit exceeded
            wait_time = bucket.get_wait_time()
            retry_after = int(wait_time) + 1  # Round up

            logger.warning(
                "rate_limit_exceeded",
                identifier=identifier,
                path=request.url.path,
                wait_time_seconds=retry_after,
            )

            # Return 429 Too Many Requests
            return JSONResponse(
                status_code=429,
                content={
                    "error": "Rate limit exceeded",
                    "message": f"Too many requests. Please retry after {retry_after} seconds.",
                    "retry_after": retry_after,
                    "limit": self.requests_per_minute,
                },
                )

    async def xǁRateLimitMiddlewareǁdispatch__mutmut_69(self, request: Request, call_next):
        """
        Process request with rate limiting

        Args:
            request: FastAPI request
            call_next: Next middleware in chain

        Returns:
            Response or 429 Too Many Requests
        """
        # Skip rate limiting for health checks
        if request.url.path in ["/health", "/", "/docs", "/redoc", "/openapi.json"]:
            return await call_next(request)

        # Get identifier and bucket
        identifier = self._get_identifier(request)
        bucket = self._get_bucket(identifier)

        # Try to consume token
        if bucket.consume():
            # Request allowed
            remaining = int(bucket.tokens)
            reset_seconds = int(bucket.capacity / bucket.refill_rate)

            logger.debug(
                "rate_limit_allowed",
                identifier=identifier,
                remaining=remaining,
                path=request.url.path,
            )

            # Process request
            response = await call_next(request)

            # Add rate limit headers
            response.headers["X-RateLimit-Limit"] = str(self.requests_per_minute)
            response.headers["X-RateLimit-Remaining"] = str(remaining)
            response.headers["X-RateLimit-Reset"] = str(reset_seconds)

            # Periodic cleanup
            self._cleanup_old_buckets()

            return response
        else:
            # Rate limit exceeded
            wait_time = bucket.get_wait_time()
            retry_after = int(wait_time) + 1  # Round up

            logger.warning(
                "rate_limit_exceeded",
                identifier=identifier,
                path=request.url.path,
                wait_time_seconds=retry_after,
            )

            # Return 429 Too Many Requests
            return JSONResponse(
                status_code=430,
                content={
                    "error": "Rate limit exceeded",
                    "message": f"Too many requests. Please retry after {retry_after} seconds.",
                    "retry_after": retry_after,
                    "limit": self.requests_per_minute,
                },
                headers={
                    "X-RateLimit-Limit": str(self.requests_per_minute),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(retry_after),
                    "Retry-After": str(retry_after),
                },
            )

    async def xǁRateLimitMiddlewareǁdispatch__mutmut_70(self, request: Request, call_next):
        """
        Process request with rate limiting

        Args:
            request: FastAPI request
            call_next: Next middleware in chain

        Returns:
            Response or 429 Too Many Requests
        """
        # Skip rate limiting for health checks
        if request.url.path in ["/health", "/", "/docs", "/redoc", "/openapi.json"]:
            return await call_next(request)

        # Get identifier and bucket
        identifier = self._get_identifier(request)
        bucket = self._get_bucket(identifier)

        # Try to consume token
        if bucket.consume():
            # Request allowed
            remaining = int(bucket.tokens)
            reset_seconds = int(bucket.capacity / bucket.refill_rate)

            logger.debug(
                "rate_limit_allowed",
                identifier=identifier,
                remaining=remaining,
                path=request.url.path,
            )

            # Process request
            response = await call_next(request)

            # Add rate limit headers
            response.headers["X-RateLimit-Limit"] = str(self.requests_per_minute)
            response.headers["X-RateLimit-Remaining"] = str(remaining)
            response.headers["X-RateLimit-Reset"] = str(reset_seconds)

            # Periodic cleanup
            self._cleanup_old_buckets()

            return response
        else:
            # Rate limit exceeded
            wait_time = bucket.get_wait_time()
            retry_after = int(wait_time) + 1  # Round up

            logger.warning(
                "rate_limit_exceeded",
                identifier=identifier,
                path=request.url.path,
                wait_time_seconds=retry_after,
            )

            # Return 429 Too Many Requests
            return JSONResponse(
                status_code=429,
                content={
                    "XXerrorXX": "Rate limit exceeded",
                    "message": f"Too many requests. Please retry after {retry_after} seconds.",
                    "retry_after": retry_after,
                    "limit": self.requests_per_minute,
                },
                headers={
                    "X-RateLimit-Limit": str(self.requests_per_minute),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(retry_after),
                    "Retry-After": str(retry_after),
                },
            )

    async def xǁRateLimitMiddlewareǁdispatch__mutmut_71(self, request: Request, call_next):
        """
        Process request with rate limiting

        Args:
            request: FastAPI request
            call_next: Next middleware in chain

        Returns:
            Response or 429 Too Many Requests
        """
        # Skip rate limiting for health checks
        if request.url.path in ["/health", "/", "/docs", "/redoc", "/openapi.json"]:
            return await call_next(request)

        # Get identifier and bucket
        identifier = self._get_identifier(request)
        bucket = self._get_bucket(identifier)

        # Try to consume token
        if bucket.consume():
            # Request allowed
            remaining = int(bucket.tokens)
            reset_seconds = int(bucket.capacity / bucket.refill_rate)

            logger.debug(
                "rate_limit_allowed",
                identifier=identifier,
                remaining=remaining,
                path=request.url.path,
            )

            # Process request
            response = await call_next(request)

            # Add rate limit headers
            response.headers["X-RateLimit-Limit"] = str(self.requests_per_minute)
            response.headers["X-RateLimit-Remaining"] = str(remaining)
            response.headers["X-RateLimit-Reset"] = str(reset_seconds)

            # Periodic cleanup
            self._cleanup_old_buckets()

            return response
        else:
            # Rate limit exceeded
            wait_time = bucket.get_wait_time()
            retry_after = int(wait_time) + 1  # Round up

            logger.warning(
                "rate_limit_exceeded",
                identifier=identifier,
                path=request.url.path,
                wait_time_seconds=retry_after,
            )

            # Return 429 Too Many Requests
            return JSONResponse(
                status_code=429,
                content={
                    "ERROR": "Rate limit exceeded",
                    "message": f"Too many requests. Please retry after {retry_after} seconds.",
                    "retry_after": retry_after,
                    "limit": self.requests_per_minute,
                },
                headers={
                    "X-RateLimit-Limit": str(self.requests_per_minute),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(retry_after),
                    "Retry-After": str(retry_after),
                },
            )

    async def xǁRateLimitMiddlewareǁdispatch__mutmut_72(self, request: Request, call_next):
        """
        Process request with rate limiting

        Args:
            request: FastAPI request
            call_next: Next middleware in chain

        Returns:
            Response or 429 Too Many Requests
        """
        # Skip rate limiting for health checks
        if request.url.path in ["/health", "/", "/docs", "/redoc", "/openapi.json"]:
            return await call_next(request)

        # Get identifier and bucket
        identifier = self._get_identifier(request)
        bucket = self._get_bucket(identifier)

        # Try to consume token
        if bucket.consume():
            # Request allowed
            remaining = int(bucket.tokens)
            reset_seconds = int(bucket.capacity / bucket.refill_rate)

            logger.debug(
                "rate_limit_allowed",
                identifier=identifier,
                remaining=remaining,
                path=request.url.path,
            )

            # Process request
            response = await call_next(request)

            # Add rate limit headers
            response.headers["X-RateLimit-Limit"] = str(self.requests_per_minute)
            response.headers["X-RateLimit-Remaining"] = str(remaining)
            response.headers["X-RateLimit-Reset"] = str(reset_seconds)

            # Periodic cleanup
            self._cleanup_old_buckets()

            return response
        else:
            # Rate limit exceeded
            wait_time = bucket.get_wait_time()
            retry_after = int(wait_time) + 1  # Round up

            logger.warning(
                "rate_limit_exceeded",
                identifier=identifier,
                path=request.url.path,
                wait_time_seconds=retry_after,
            )

            # Return 429 Too Many Requests
            return JSONResponse(
                status_code=429,
                content={
                    "error": "XXRate limit exceededXX",
                    "message": f"Too many requests. Please retry after {retry_after} seconds.",
                    "retry_after": retry_after,
                    "limit": self.requests_per_minute,
                },
                headers={
                    "X-RateLimit-Limit": str(self.requests_per_minute),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(retry_after),
                    "Retry-After": str(retry_after),
                },
            )

    async def xǁRateLimitMiddlewareǁdispatch__mutmut_73(self, request: Request, call_next):
        """
        Process request with rate limiting

        Args:
            request: FastAPI request
            call_next: Next middleware in chain

        Returns:
            Response or 429 Too Many Requests
        """
        # Skip rate limiting for health checks
        if request.url.path in ["/health", "/", "/docs", "/redoc", "/openapi.json"]:
            return await call_next(request)

        # Get identifier and bucket
        identifier = self._get_identifier(request)
        bucket = self._get_bucket(identifier)

        # Try to consume token
        if bucket.consume():
            # Request allowed
            remaining = int(bucket.tokens)
            reset_seconds = int(bucket.capacity / bucket.refill_rate)

            logger.debug(
                "rate_limit_allowed",
                identifier=identifier,
                remaining=remaining,
                path=request.url.path,
            )

            # Process request
            response = await call_next(request)

            # Add rate limit headers
            response.headers["X-RateLimit-Limit"] = str(self.requests_per_minute)
            response.headers["X-RateLimit-Remaining"] = str(remaining)
            response.headers["X-RateLimit-Reset"] = str(reset_seconds)

            # Periodic cleanup
            self._cleanup_old_buckets()

            return response
        else:
            # Rate limit exceeded
            wait_time = bucket.get_wait_time()
            retry_after = int(wait_time) + 1  # Round up

            logger.warning(
                "rate_limit_exceeded",
                identifier=identifier,
                path=request.url.path,
                wait_time_seconds=retry_after,
            )

            # Return 429 Too Many Requests
            return JSONResponse(
                status_code=429,
                content={
                    "error": "rate limit exceeded",
                    "message": f"Too many requests. Please retry after {retry_after} seconds.",
                    "retry_after": retry_after,
                    "limit": self.requests_per_minute,
                },
                headers={
                    "X-RateLimit-Limit": str(self.requests_per_minute),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(retry_after),
                    "Retry-After": str(retry_after),
                },
            )

    async def xǁRateLimitMiddlewareǁdispatch__mutmut_74(self, request: Request, call_next):
        """
        Process request with rate limiting

        Args:
            request: FastAPI request
            call_next: Next middleware in chain

        Returns:
            Response or 429 Too Many Requests
        """
        # Skip rate limiting for health checks
        if request.url.path in ["/health", "/", "/docs", "/redoc", "/openapi.json"]:
            return await call_next(request)

        # Get identifier and bucket
        identifier = self._get_identifier(request)
        bucket = self._get_bucket(identifier)

        # Try to consume token
        if bucket.consume():
            # Request allowed
            remaining = int(bucket.tokens)
            reset_seconds = int(bucket.capacity / bucket.refill_rate)

            logger.debug(
                "rate_limit_allowed",
                identifier=identifier,
                remaining=remaining,
                path=request.url.path,
            )

            # Process request
            response = await call_next(request)

            # Add rate limit headers
            response.headers["X-RateLimit-Limit"] = str(self.requests_per_minute)
            response.headers["X-RateLimit-Remaining"] = str(remaining)
            response.headers["X-RateLimit-Reset"] = str(reset_seconds)

            # Periodic cleanup
            self._cleanup_old_buckets()

            return response
        else:
            # Rate limit exceeded
            wait_time = bucket.get_wait_time()
            retry_after = int(wait_time) + 1  # Round up

            logger.warning(
                "rate_limit_exceeded",
                identifier=identifier,
                path=request.url.path,
                wait_time_seconds=retry_after,
            )

            # Return 429 Too Many Requests
            return JSONResponse(
                status_code=429,
                content={
                    "error": "RATE LIMIT EXCEEDED",
                    "message": f"Too many requests. Please retry after {retry_after} seconds.",
                    "retry_after": retry_after,
                    "limit": self.requests_per_minute,
                },
                headers={
                    "X-RateLimit-Limit": str(self.requests_per_minute),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(retry_after),
                    "Retry-After": str(retry_after),
                },
            )

    async def xǁRateLimitMiddlewareǁdispatch__mutmut_75(self, request: Request, call_next):
        """
        Process request with rate limiting

        Args:
            request: FastAPI request
            call_next: Next middleware in chain

        Returns:
            Response or 429 Too Many Requests
        """
        # Skip rate limiting for health checks
        if request.url.path in ["/health", "/", "/docs", "/redoc", "/openapi.json"]:
            return await call_next(request)

        # Get identifier and bucket
        identifier = self._get_identifier(request)
        bucket = self._get_bucket(identifier)

        # Try to consume token
        if bucket.consume():
            # Request allowed
            remaining = int(bucket.tokens)
            reset_seconds = int(bucket.capacity / bucket.refill_rate)

            logger.debug(
                "rate_limit_allowed",
                identifier=identifier,
                remaining=remaining,
                path=request.url.path,
            )

            # Process request
            response = await call_next(request)

            # Add rate limit headers
            response.headers["X-RateLimit-Limit"] = str(self.requests_per_minute)
            response.headers["X-RateLimit-Remaining"] = str(remaining)
            response.headers["X-RateLimit-Reset"] = str(reset_seconds)

            # Periodic cleanup
            self._cleanup_old_buckets()

            return response
        else:
            # Rate limit exceeded
            wait_time = bucket.get_wait_time()
            retry_after = int(wait_time) + 1  # Round up

            logger.warning(
                "rate_limit_exceeded",
                identifier=identifier,
                path=request.url.path,
                wait_time_seconds=retry_after,
            )

            # Return 429 Too Many Requests
            return JSONResponse(
                status_code=429,
                content={
                    "error": "Rate limit exceeded",
                    "XXmessageXX": f"Too many requests. Please retry after {retry_after} seconds.",
                    "retry_after": retry_after,
                    "limit": self.requests_per_minute,
                },
                headers={
                    "X-RateLimit-Limit": str(self.requests_per_minute),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(retry_after),
                    "Retry-After": str(retry_after),
                },
            )

    async def xǁRateLimitMiddlewareǁdispatch__mutmut_76(self, request: Request, call_next):
        """
        Process request with rate limiting

        Args:
            request: FastAPI request
            call_next: Next middleware in chain

        Returns:
            Response or 429 Too Many Requests
        """
        # Skip rate limiting for health checks
        if request.url.path in ["/health", "/", "/docs", "/redoc", "/openapi.json"]:
            return await call_next(request)

        # Get identifier and bucket
        identifier = self._get_identifier(request)
        bucket = self._get_bucket(identifier)

        # Try to consume token
        if bucket.consume():
            # Request allowed
            remaining = int(bucket.tokens)
            reset_seconds = int(bucket.capacity / bucket.refill_rate)

            logger.debug(
                "rate_limit_allowed",
                identifier=identifier,
                remaining=remaining,
                path=request.url.path,
            )

            # Process request
            response = await call_next(request)

            # Add rate limit headers
            response.headers["X-RateLimit-Limit"] = str(self.requests_per_minute)
            response.headers["X-RateLimit-Remaining"] = str(remaining)
            response.headers["X-RateLimit-Reset"] = str(reset_seconds)

            # Periodic cleanup
            self._cleanup_old_buckets()

            return response
        else:
            # Rate limit exceeded
            wait_time = bucket.get_wait_time()
            retry_after = int(wait_time) + 1  # Round up

            logger.warning(
                "rate_limit_exceeded",
                identifier=identifier,
                path=request.url.path,
                wait_time_seconds=retry_after,
            )

            # Return 429 Too Many Requests
            return JSONResponse(
                status_code=429,
                content={
                    "error": "Rate limit exceeded",
                    "MESSAGE": f"Too many requests. Please retry after {retry_after} seconds.",
                    "retry_after": retry_after,
                    "limit": self.requests_per_minute,
                },
                headers={
                    "X-RateLimit-Limit": str(self.requests_per_minute),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(retry_after),
                    "Retry-After": str(retry_after),
                },
            )

    async def xǁRateLimitMiddlewareǁdispatch__mutmut_77(self, request: Request, call_next):
        """
        Process request with rate limiting

        Args:
            request: FastAPI request
            call_next: Next middleware in chain

        Returns:
            Response or 429 Too Many Requests
        """
        # Skip rate limiting for health checks
        if request.url.path in ["/health", "/", "/docs", "/redoc", "/openapi.json"]:
            return await call_next(request)

        # Get identifier and bucket
        identifier = self._get_identifier(request)
        bucket = self._get_bucket(identifier)

        # Try to consume token
        if bucket.consume():
            # Request allowed
            remaining = int(bucket.tokens)
            reset_seconds = int(bucket.capacity / bucket.refill_rate)

            logger.debug(
                "rate_limit_allowed",
                identifier=identifier,
                remaining=remaining,
                path=request.url.path,
            )

            # Process request
            response = await call_next(request)

            # Add rate limit headers
            response.headers["X-RateLimit-Limit"] = str(self.requests_per_minute)
            response.headers["X-RateLimit-Remaining"] = str(remaining)
            response.headers["X-RateLimit-Reset"] = str(reset_seconds)

            # Periodic cleanup
            self._cleanup_old_buckets()

            return response
        else:
            # Rate limit exceeded
            wait_time = bucket.get_wait_time()
            retry_after = int(wait_time) + 1  # Round up

            logger.warning(
                "rate_limit_exceeded",
                identifier=identifier,
                path=request.url.path,
                wait_time_seconds=retry_after,
            )

            # Return 429 Too Many Requests
            return JSONResponse(
                status_code=429,
                content={
                    "error": "Rate limit exceeded",
                    "message": f"Too many requests. Please retry after {retry_after} seconds.",
                    "XXretry_afterXX": retry_after,
                    "limit": self.requests_per_minute,
                },
                headers={
                    "X-RateLimit-Limit": str(self.requests_per_minute),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(retry_after),
                    "Retry-After": str(retry_after),
                },
            )

    async def xǁRateLimitMiddlewareǁdispatch__mutmut_78(self, request: Request, call_next):
        """
        Process request with rate limiting

        Args:
            request: FastAPI request
            call_next: Next middleware in chain

        Returns:
            Response or 429 Too Many Requests
        """
        # Skip rate limiting for health checks
        if request.url.path in ["/health", "/", "/docs", "/redoc", "/openapi.json"]:
            return await call_next(request)

        # Get identifier and bucket
        identifier = self._get_identifier(request)
        bucket = self._get_bucket(identifier)

        # Try to consume token
        if bucket.consume():
            # Request allowed
            remaining = int(bucket.tokens)
            reset_seconds = int(bucket.capacity / bucket.refill_rate)

            logger.debug(
                "rate_limit_allowed",
                identifier=identifier,
                remaining=remaining,
                path=request.url.path,
            )

            # Process request
            response = await call_next(request)

            # Add rate limit headers
            response.headers["X-RateLimit-Limit"] = str(self.requests_per_minute)
            response.headers["X-RateLimit-Remaining"] = str(remaining)
            response.headers["X-RateLimit-Reset"] = str(reset_seconds)

            # Periodic cleanup
            self._cleanup_old_buckets()

            return response
        else:
            # Rate limit exceeded
            wait_time = bucket.get_wait_time()
            retry_after = int(wait_time) + 1  # Round up

            logger.warning(
                "rate_limit_exceeded",
                identifier=identifier,
                path=request.url.path,
                wait_time_seconds=retry_after,
            )

            # Return 429 Too Many Requests
            return JSONResponse(
                status_code=429,
                content={
                    "error": "Rate limit exceeded",
                    "message": f"Too many requests. Please retry after {retry_after} seconds.",
                    "RETRY_AFTER": retry_after,
                    "limit": self.requests_per_minute,
                },
                headers={
                    "X-RateLimit-Limit": str(self.requests_per_minute),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(retry_after),
                    "Retry-After": str(retry_after),
                },
            )

    async def xǁRateLimitMiddlewareǁdispatch__mutmut_79(self, request: Request, call_next):
        """
        Process request with rate limiting

        Args:
            request: FastAPI request
            call_next: Next middleware in chain

        Returns:
            Response or 429 Too Many Requests
        """
        # Skip rate limiting for health checks
        if request.url.path in ["/health", "/", "/docs", "/redoc", "/openapi.json"]:
            return await call_next(request)

        # Get identifier and bucket
        identifier = self._get_identifier(request)
        bucket = self._get_bucket(identifier)

        # Try to consume token
        if bucket.consume():
            # Request allowed
            remaining = int(bucket.tokens)
            reset_seconds = int(bucket.capacity / bucket.refill_rate)

            logger.debug(
                "rate_limit_allowed",
                identifier=identifier,
                remaining=remaining,
                path=request.url.path,
            )

            # Process request
            response = await call_next(request)

            # Add rate limit headers
            response.headers["X-RateLimit-Limit"] = str(self.requests_per_minute)
            response.headers["X-RateLimit-Remaining"] = str(remaining)
            response.headers["X-RateLimit-Reset"] = str(reset_seconds)

            # Periodic cleanup
            self._cleanup_old_buckets()

            return response
        else:
            # Rate limit exceeded
            wait_time = bucket.get_wait_time()
            retry_after = int(wait_time) + 1  # Round up

            logger.warning(
                "rate_limit_exceeded",
                identifier=identifier,
                path=request.url.path,
                wait_time_seconds=retry_after,
            )

            # Return 429 Too Many Requests
            return JSONResponse(
                status_code=429,
                content={
                    "error": "Rate limit exceeded",
                    "message": f"Too many requests. Please retry after {retry_after} seconds.",
                    "retry_after": retry_after,
                    "XXlimitXX": self.requests_per_minute,
                },
                headers={
                    "X-RateLimit-Limit": str(self.requests_per_minute),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(retry_after),
                    "Retry-After": str(retry_after),
                },
            )

    async def xǁRateLimitMiddlewareǁdispatch__mutmut_80(self, request: Request, call_next):
        """
        Process request with rate limiting

        Args:
            request: FastAPI request
            call_next: Next middleware in chain

        Returns:
            Response or 429 Too Many Requests
        """
        # Skip rate limiting for health checks
        if request.url.path in ["/health", "/", "/docs", "/redoc", "/openapi.json"]:
            return await call_next(request)

        # Get identifier and bucket
        identifier = self._get_identifier(request)
        bucket = self._get_bucket(identifier)

        # Try to consume token
        if bucket.consume():
            # Request allowed
            remaining = int(bucket.tokens)
            reset_seconds = int(bucket.capacity / bucket.refill_rate)

            logger.debug(
                "rate_limit_allowed",
                identifier=identifier,
                remaining=remaining,
                path=request.url.path,
            )

            # Process request
            response = await call_next(request)

            # Add rate limit headers
            response.headers["X-RateLimit-Limit"] = str(self.requests_per_minute)
            response.headers["X-RateLimit-Remaining"] = str(remaining)
            response.headers["X-RateLimit-Reset"] = str(reset_seconds)

            # Periodic cleanup
            self._cleanup_old_buckets()

            return response
        else:
            # Rate limit exceeded
            wait_time = bucket.get_wait_time()
            retry_after = int(wait_time) + 1  # Round up

            logger.warning(
                "rate_limit_exceeded",
                identifier=identifier,
                path=request.url.path,
                wait_time_seconds=retry_after,
            )

            # Return 429 Too Many Requests
            return JSONResponse(
                status_code=429,
                content={
                    "error": "Rate limit exceeded",
                    "message": f"Too many requests. Please retry after {retry_after} seconds.",
                    "retry_after": retry_after,
                    "LIMIT": self.requests_per_minute,
                },
                headers={
                    "X-RateLimit-Limit": str(self.requests_per_minute),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(retry_after),
                    "Retry-After": str(retry_after),
                },
            )

    async def xǁRateLimitMiddlewareǁdispatch__mutmut_81(self, request: Request, call_next):
        """
        Process request with rate limiting

        Args:
            request: FastAPI request
            call_next: Next middleware in chain

        Returns:
            Response or 429 Too Many Requests
        """
        # Skip rate limiting for health checks
        if request.url.path in ["/health", "/", "/docs", "/redoc", "/openapi.json"]:
            return await call_next(request)

        # Get identifier and bucket
        identifier = self._get_identifier(request)
        bucket = self._get_bucket(identifier)

        # Try to consume token
        if bucket.consume():
            # Request allowed
            remaining = int(bucket.tokens)
            reset_seconds = int(bucket.capacity / bucket.refill_rate)

            logger.debug(
                "rate_limit_allowed",
                identifier=identifier,
                remaining=remaining,
                path=request.url.path,
            )

            # Process request
            response = await call_next(request)

            # Add rate limit headers
            response.headers["X-RateLimit-Limit"] = str(self.requests_per_minute)
            response.headers["X-RateLimit-Remaining"] = str(remaining)
            response.headers["X-RateLimit-Reset"] = str(reset_seconds)

            # Periodic cleanup
            self._cleanup_old_buckets()

            return response
        else:
            # Rate limit exceeded
            wait_time = bucket.get_wait_time()
            retry_after = int(wait_time) + 1  # Round up

            logger.warning(
                "rate_limit_exceeded",
                identifier=identifier,
                path=request.url.path,
                wait_time_seconds=retry_after,
            )

            # Return 429 Too Many Requests
            return JSONResponse(
                status_code=429,
                content={
                    "error": "Rate limit exceeded",
                    "message": f"Too many requests. Please retry after {retry_after} seconds.",
                    "retry_after": retry_after,
                    "limit": self.requests_per_minute,
                },
                headers={
                    "XXX-RateLimit-LimitXX": str(self.requests_per_minute),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(retry_after),
                    "Retry-After": str(retry_after),
                },
            )

    async def xǁRateLimitMiddlewareǁdispatch__mutmut_82(self, request: Request, call_next):
        """
        Process request with rate limiting

        Args:
            request: FastAPI request
            call_next: Next middleware in chain

        Returns:
            Response or 429 Too Many Requests
        """
        # Skip rate limiting for health checks
        if request.url.path in ["/health", "/", "/docs", "/redoc", "/openapi.json"]:
            return await call_next(request)

        # Get identifier and bucket
        identifier = self._get_identifier(request)
        bucket = self._get_bucket(identifier)

        # Try to consume token
        if bucket.consume():
            # Request allowed
            remaining = int(bucket.tokens)
            reset_seconds = int(bucket.capacity / bucket.refill_rate)

            logger.debug(
                "rate_limit_allowed",
                identifier=identifier,
                remaining=remaining,
                path=request.url.path,
            )

            # Process request
            response = await call_next(request)

            # Add rate limit headers
            response.headers["X-RateLimit-Limit"] = str(self.requests_per_minute)
            response.headers["X-RateLimit-Remaining"] = str(remaining)
            response.headers["X-RateLimit-Reset"] = str(reset_seconds)

            # Periodic cleanup
            self._cleanup_old_buckets()

            return response
        else:
            # Rate limit exceeded
            wait_time = bucket.get_wait_time()
            retry_after = int(wait_time) + 1  # Round up

            logger.warning(
                "rate_limit_exceeded",
                identifier=identifier,
                path=request.url.path,
                wait_time_seconds=retry_after,
            )

            # Return 429 Too Many Requests
            return JSONResponse(
                status_code=429,
                content={
                    "error": "Rate limit exceeded",
                    "message": f"Too many requests. Please retry after {retry_after} seconds.",
                    "retry_after": retry_after,
                    "limit": self.requests_per_minute,
                },
                headers={
                    "x-ratelimit-limit": str(self.requests_per_minute),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(retry_after),
                    "Retry-After": str(retry_after),
                },
            )

    async def xǁRateLimitMiddlewareǁdispatch__mutmut_83(self, request: Request, call_next):
        """
        Process request with rate limiting

        Args:
            request: FastAPI request
            call_next: Next middleware in chain

        Returns:
            Response or 429 Too Many Requests
        """
        # Skip rate limiting for health checks
        if request.url.path in ["/health", "/", "/docs", "/redoc", "/openapi.json"]:
            return await call_next(request)

        # Get identifier and bucket
        identifier = self._get_identifier(request)
        bucket = self._get_bucket(identifier)

        # Try to consume token
        if bucket.consume():
            # Request allowed
            remaining = int(bucket.tokens)
            reset_seconds = int(bucket.capacity / bucket.refill_rate)

            logger.debug(
                "rate_limit_allowed",
                identifier=identifier,
                remaining=remaining,
                path=request.url.path,
            )

            # Process request
            response = await call_next(request)

            # Add rate limit headers
            response.headers["X-RateLimit-Limit"] = str(self.requests_per_minute)
            response.headers["X-RateLimit-Remaining"] = str(remaining)
            response.headers["X-RateLimit-Reset"] = str(reset_seconds)

            # Periodic cleanup
            self._cleanup_old_buckets()

            return response
        else:
            # Rate limit exceeded
            wait_time = bucket.get_wait_time()
            retry_after = int(wait_time) + 1  # Round up

            logger.warning(
                "rate_limit_exceeded",
                identifier=identifier,
                path=request.url.path,
                wait_time_seconds=retry_after,
            )

            # Return 429 Too Many Requests
            return JSONResponse(
                status_code=429,
                content={
                    "error": "Rate limit exceeded",
                    "message": f"Too many requests. Please retry after {retry_after} seconds.",
                    "retry_after": retry_after,
                    "limit": self.requests_per_minute,
                },
                headers={
                    "X-RATELIMIT-LIMIT": str(self.requests_per_minute),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(retry_after),
                    "Retry-After": str(retry_after),
                },
            )

    async def xǁRateLimitMiddlewareǁdispatch__mutmut_84(self, request: Request, call_next):
        """
        Process request with rate limiting

        Args:
            request: FastAPI request
            call_next: Next middleware in chain

        Returns:
            Response or 429 Too Many Requests
        """
        # Skip rate limiting for health checks
        if request.url.path in ["/health", "/", "/docs", "/redoc", "/openapi.json"]:
            return await call_next(request)

        # Get identifier and bucket
        identifier = self._get_identifier(request)
        bucket = self._get_bucket(identifier)

        # Try to consume token
        if bucket.consume():
            # Request allowed
            remaining = int(bucket.tokens)
            reset_seconds = int(bucket.capacity / bucket.refill_rate)

            logger.debug(
                "rate_limit_allowed",
                identifier=identifier,
                remaining=remaining,
                path=request.url.path,
            )

            # Process request
            response = await call_next(request)

            # Add rate limit headers
            response.headers["X-RateLimit-Limit"] = str(self.requests_per_minute)
            response.headers["X-RateLimit-Remaining"] = str(remaining)
            response.headers["X-RateLimit-Reset"] = str(reset_seconds)

            # Periodic cleanup
            self._cleanup_old_buckets()

            return response
        else:
            # Rate limit exceeded
            wait_time = bucket.get_wait_time()
            retry_after = int(wait_time) + 1  # Round up

            logger.warning(
                "rate_limit_exceeded",
                identifier=identifier,
                path=request.url.path,
                wait_time_seconds=retry_after,
            )

            # Return 429 Too Many Requests
            return JSONResponse(
                status_code=429,
                content={
                    "error": "Rate limit exceeded",
                    "message": f"Too many requests. Please retry after {retry_after} seconds.",
                    "retry_after": retry_after,
                    "limit": self.requests_per_minute,
                },
                headers={
                    "X-RateLimit-Limit": str(None),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(retry_after),
                    "Retry-After": str(retry_after),
                },
            )

    async def xǁRateLimitMiddlewareǁdispatch__mutmut_85(self, request: Request, call_next):
        """
        Process request with rate limiting

        Args:
            request: FastAPI request
            call_next: Next middleware in chain

        Returns:
            Response or 429 Too Many Requests
        """
        # Skip rate limiting for health checks
        if request.url.path in ["/health", "/", "/docs", "/redoc", "/openapi.json"]:
            return await call_next(request)

        # Get identifier and bucket
        identifier = self._get_identifier(request)
        bucket = self._get_bucket(identifier)

        # Try to consume token
        if bucket.consume():
            # Request allowed
            remaining = int(bucket.tokens)
            reset_seconds = int(bucket.capacity / bucket.refill_rate)

            logger.debug(
                "rate_limit_allowed",
                identifier=identifier,
                remaining=remaining,
                path=request.url.path,
            )

            # Process request
            response = await call_next(request)

            # Add rate limit headers
            response.headers["X-RateLimit-Limit"] = str(self.requests_per_minute)
            response.headers["X-RateLimit-Remaining"] = str(remaining)
            response.headers["X-RateLimit-Reset"] = str(reset_seconds)

            # Periodic cleanup
            self._cleanup_old_buckets()

            return response
        else:
            # Rate limit exceeded
            wait_time = bucket.get_wait_time()
            retry_after = int(wait_time) + 1  # Round up

            logger.warning(
                "rate_limit_exceeded",
                identifier=identifier,
                path=request.url.path,
                wait_time_seconds=retry_after,
            )

            # Return 429 Too Many Requests
            return JSONResponse(
                status_code=429,
                content={
                    "error": "Rate limit exceeded",
                    "message": f"Too many requests. Please retry after {retry_after} seconds.",
                    "retry_after": retry_after,
                    "limit": self.requests_per_minute,
                },
                headers={
                    "X-RateLimit-Limit": str(self.requests_per_minute),
                    "XXX-RateLimit-RemainingXX": "0",
                    "X-RateLimit-Reset": str(retry_after),
                    "Retry-After": str(retry_after),
                },
            )

    async def xǁRateLimitMiddlewareǁdispatch__mutmut_86(self, request: Request, call_next):
        """
        Process request with rate limiting

        Args:
            request: FastAPI request
            call_next: Next middleware in chain

        Returns:
            Response or 429 Too Many Requests
        """
        # Skip rate limiting for health checks
        if request.url.path in ["/health", "/", "/docs", "/redoc", "/openapi.json"]:
            return await call_next(request)

        # Get identifier and bucket
        identifier = self._get_identifier(request)
        bucket = self._get_bucket(identifier)

        # Try to consume token
        if bucket.consume():
            # Request allowed
            remaining = int(bucket.tokens)
            reset_seconds = int(bucket.capacity / bucket.refill_rate)

            logger.debug(
                "rate_limit_allowed",
                identifier=identifier,
                remaining=remaining,
                path=request.url.path,
            )

            # Process request
            response = await call_next(request)

            # Add rate limit headers
            response.headers["X-RateLimit-Limit"] = str(self.requests_per_minute)
            response.headers["X-RateLimit-Remaining"] = str(remaining)
            response.headers["X-RateLimit-Reset"] = str(reset_seconds)

            # Periodic cleanup
            self._cleanup_old_buckets()

            return response
        else:
            # Rate limit exceeded
            wait_time = bucket.get_wait_time()
            retry_after = int(wait_time) + 1  # Round up

            logger.warning(
                "rate_limit_exceeded",
                identifier=identifier,
                path=request.url.path,
                wait_time_seconds=retry_after,
            )

            # Return 429 Too Many Requests
            return JSONResponse(
                status_code=429,
                content={
                    "error": "Rate limit exceeded",
                    "message": f"Too many requests. Please retry after {retry_after} seconds.",
                    "retry_after": retry_after,
                    "limit": self.requests_per_minute,
                },
                headers={
                    "X-RateLimit-Limit": str(self.requests_per_minute),
                    "x-ratelimit-remaining": "0",
                    "X-RateLimit-Reset": str(retry_after),
                    "Retry-After": str(retry_after),
                },
            )

    async def xǁRateLimitMiddlewareǁdispatch__mutmut_87(self, request: Request, call_next):
        """
        Process request with rate limiting

        Args:
            request: FastAPI request
            call_next: Next middleware in chain

        Returns:
            Response or 429 Too Many Requests
        """
        # Skip rate limiting for health checks
        if request.url.path in ["/health", "/", "/docs", "/redoc", "/openapi.json"]:
            return await call_next(request)

        # Get identifier and bucket
        identifier = self._get_identifier(request)
        bucket = self._get_bucket(identifier)

        # Try to consume token
        if bucket.consume():
            # Request allowed
            remaining = int(bucket.tokens)
            reset_seconds = int(bucket.capacity / bucket.refill_rate)

            logger.debug(
                "rate_limit_allowed",
                identifier=identifier,
                remaining=remaining,
                path=request.url.path,
            )

            # Process request
            response = await call_next(request)

            # Add rate limit headers
            response.headers["X-RateLimit-Limit"] = str(self.requests_per_minute)
            response.headers["X-RateLimit-Remaining"] = str(remaining)
            response.headers["X-RateLimit-Reset"] = str(reset_seconds)

            # Periodic cleanup
            self._cleanup_old_buckets()

            return response
        else:
            # Rate limit exceeded
            wait_time = bucket.get_wait_time()
            retry_after = int(wait_time) + 1  # Round up

            logger.warning(
                "rate_limit_exceeded",
                identifier=identifier,
                path=request.url.path,
                wait_time_seconds=retry_after,
            )

            # Return 429 Too Many Requests
            return JSONResponse(
                status_code=429,
                content={
                    "error": "Rate limit exceeded",
                    "message": f"Too many requests. Please retry after {retry_after} seconds.",
                    "retry_after": retry_after,
                    "limit": self.requests_per_minute,
                },
                headers={
                    "X-RateLimit-Limit": str(self.requests_per_minute),
                    "X-RATELIMIT-REMAINING": "0",
                    "X-RateLimit-Reset": str(retry_after),
                    "Retry-After": str(retry_after),
                },
            )

    async def xǁRateLimitMiddlewareǁdispatch__mutmut_88(self, request: Request, call_next):
        """
        Process request with rate limiting

        Args:
            request: FastAPI request
            call_next: Next middleware in chain

        Returns:
            Response or 429 Too Many Requests
        """
        # Skip rate limiting for health checks
        if request.url.path in ["/health", "/", "/docs", "/redoc", "/openapi.json"]:
            return await call_next(request)

        # Get identifier and bucket
        identifier = self._get_identifier(request)
        bucket = self._get_bucket(identifier)

        # Try to consume token
        if bucket.consume():
            # Request allowed
            remaining = int(bucket.tokens)
            reset_seconds = int(bucket.capacity / bucket.refill_rate)

            logger.debug(
                "rate_limit_allowed",
                identifier=identifier,
                remaining=remaining,
                path=request.url.path,
            )

            # Process request
            response = await call_next(request)

            # Add rate limit headers
            response.headers["X-RateLimit-Limit"] = str(self.requests_per_minute)
            response.headers["X-RateLimit-Remaining"] = str(remaining)
            response.headers["X-RateLimit-Reset"] = str(reset_seconds)

            # Periodic cleanup
            self._cleanup_old_buckets()

            return response
        else:
            # Rate limit exceeded
            wait_time = bucket.get_wait_time()
            retry_after = int(wait_time) + 1  # Round up

            logger.warning(
                "rate_limit_exceeded",
                identifier=identifier,
                path=request.url.path,
                wait_time_seconds=retry_after,
            )

            # Return 429 Too Many Requests
            return JSONResponse(
                status_code=429,
                content={
                    "error": "Rate limit exceeded",
                    "message": f"Too many requests. Please retry after {retry_after} seconds.",
                    "retry_after": retry_after,
                    "limit": self.requests_per_minute,
                },
                headers={
                    "X-RateLimit-Limit": str(self.requests_per_minute),
                    "X-RateLimit-Remaining": "XX0XX",
                    "X-RateLimit-Reset": str(retry_after),
                    "Retry-After": str(retry_after),
                },
            )

    async def xǁRateLimitMiddlewareǁdispatch__mutmut_89(self, request: Request, call_next):
        """
        Process request with rate limiting

        Args:
            request: FastAPI request
            call_next: Next middleware in chain

        Returns:
            Response or 429 Too Many Requests
        """
        # Skip rate limiting for health checks
        if request.url.path in ["/health", "/", "/docs", "/redoc", "/openapi.json"]:
            return await call_next(request)

        # Get identifier and bucket
        identifier = self._get_identifier(request)
        bucket = self._get_bucket(identifier)

        # Try to consume token
        if bucket.consume():
            # Request allowed
            remaining = int(bucket.tokens)
            reset_seconds = int(bucket.capacity / bucket.refill_rate)

            logger.debug(
                "rate_limit_allowed",
                identifier=identifier,
                remaining=remaining,
                path=request.url.path,
            )

            # Process request
            response = await call_next(request)

            # Add rate limit headers
            response.headers["X-RateLimit-Limit"] = str(self.requests_per_minute)
            response.headers["X-RateLimit-Remaining"] = str(remaining)
            response.headers["X-RateLimit-Reset"] = str(reset_seconds)

            # Periodic cleanup
            self._cleanup_old_buckets()

            return response
        else:
            # Rate limit exceeded
            wait_time = bucket.get_wait_time()
            retry_after = int(wait_time) + 1  # Round up

            logger.warning(
                "rate_limit_exceeded",
                identifier=identifier,
                path=request.url.path,
                wait_time_seconds=retry_after,
            )

            # Return 429 Too Many Requests
            return JSONResponse(
                status_code=429,
                content={
                    "error": "Rate limit exceeded",
                    "message": f"Too many requests. Please retry after {retry_after} seconds.",
                    "retry_after": retry_after,
                    "limit": self.requests_per_minute,
                },
                headers={
                    "X-RateLimit-Limit": str(self.requests_per_minute),
                    "X-RateLimit-Remaining": "0",
                    "XXX-RateLimit-ResetXX": str(retry_after),
                    "Retry-After": str(retry_after),
                },
            )

    async def xǁRateLimitMiddlewareǁdispatch__mutmut_90(self, request: Request, call_next):
        """
        Process request with rate limiting

        Args:
            request: FastAPI request
            call_next: Next middleware in chain

        Returns:
            Response or 429 Too Many Requests
        """
        # Skip rate limiting for health checks
        if request.url.path in ["/health", "/", "/docs", "/redoc", "/openapi.json"]:
            return await call_next(request)

        # Get identifier and bucket
        identifier = self._get_identifier(request)
        bucket = self._get_bucket(identifier)

        # Try to consume token
        if bucket.consume():
            # Request allowed
            remaining = int(bucket.tokens)
            reset_seconds = int(bucket.capacity / bucket.refill_rate)

            logger.debug(
                "rate_limit_allowed",
                identifier=identifier,
                remaining=remaining,
                path=request.url.path,
            )

            # Process request
            response = await call_next(request)

            # Add rate limit headers
            response.headers["X-RateLimit-Limit"] = str(self.requests_per_minute)
            response.headers["X-RateLimit-Remaining"] = str(remaining)
            response.headers["X-RateLimit-Reset"] = str(reset_seconds)

            # Periodic cleanup
            self._cleanup_old_buckets()

            return response
        else:
            # Rate limit exceeded
            wait_time = bucket.get_wait_time()
            retry_after = int(wait_time) + 1  # Round up

            logger.warning(
                "rate_limit_exceeded",
                identifier=identifier,
                path=request.url.path,
                wait_time_seconds=retry_after,
            )

            # Return 429 Too Many Requests
            return JSONResponse(
                status_code=429,
                content={
                    "error": "Rate limit exceeded",
                    "message": f"Too many requests. Please retry after {retry_after} seconds.",
                    "retry_after": retry_after,
                    "limit": self.requests_per_minute,
                },
                headers={
                    "X-RateLimit-Limit": str(self.requests_per_minute),
                    "X-RateLimit-Remaining": "0",
                    "x-ratelimit-reset": str(retry_after),
                    "Retry-After": str(retry_after),
                },
            )

    async def xǁRateLimitMiddlewareǁdispatch__mutmut_91(self, request: Request, call_next):
        """
        Process request with rate limiting

        Args:
            request: FastAPI request
            call_next: Next middleware in chain

        Returns:
            Response or 429 Too Many Requests
        """
        # Skip rate limiting for health checks
        if request.url.path in ["/health", "/", "/docs", "/redoc", "/openapi.json"]:
            return await call_next(request)

        # Get identifier and bucket
        identifier = self._get_identifier(request)
        bucket = self._get_bucket(identifier)

        # Try to consume token
        if bucket.consume():
            # Request allowed
            remaining = int(bucket.tokens)
            reset_seconds = int(bucket.capacity / bucket.refill_rate)

            logger.debug(
                "rate_limit_allowed",
                identifier=identifier,
                remaining=remaining,
                path=request.url.path,
            )

            # Process request
            response = await call_next(request)

            # Add rate limit headers
            response.headers["X-RateLimit-Limit"] = str(self.requests_per_minute)
            response.headers["X-RateLimit-Remaining"] = str(remaining)
            response.headers["X-RateLimit-Reset"] = str(reset_seconds)

            # Periodic cleanup
            self._cleanup_old_buckets()

            return response
        else:
            # Rate limit exceeded
            wait_time = bucket.get_wait_time()
            retry_after = int(wait_time) + 1  # Round up

            logger.warning(
                "rate_limit_exceeded",
                identifier=identifier,
                path=request.url.path,
                wait_time_seconds=retry_after,
            )

            # Return 429 Too Many Requests
            return JSONResponse(
                status_code=429,
                content={
                    "error": "Rate limit exceeded",
                    "message": f"Too many requests. Please retry after {retry_after} seconds.",
                    "retry_after": retry_after,
                    "limit": self.requests_per_minute,
                },
                headers={
                    "X-RateLimit-Limit": str(self.requests_per_minute),
                    "X-RateLimit-Remaining": "0",
                    "X-RATELIMIT-RESET": str(retry_after),
                    "Retry-After": str(retry_after),
                },
            )

    async def xǁRateLimitMiddlewareǁdispatch__mutmut_92(self, request: Request, call_next):
        """
        Process request with rate limiting

        Args:
            request: FastAPI request
            call_next: Next middleware in chain

        Returns:
            Response or 429 Too Many Requests
        """
        # Skip rate limiting for health checks
        if request.url.path in ["/health", "/", "/docs", "/redoc", "/openapi.json"]:
            return await call_next(request)

        # Get identifier and bucket
        identifier = self._get_identifier(request)
        bucket = self._get_bucket(identifier)

        # Try to consume token
        if bucket.consume():
            # Request allowed
            remaining = int(bucket.tokens)
            reset_seconds = int(bucket.capacity / bucket.refill_rate)

            logger.debug(
                "rate_limit_allowed",
                identifier=identifier,
                remaining=remaining,
                path=request.url.path,
            )

            # Process request
            response = await call_next(request)

            # Add rate limit headers
            response.headers["X-RateLimit-Limit"] = str(self.requests_per_minute)
            response.headers["X-RateLimit-Remaining"] = str(remaining)
            response.headers["X-RateLimit-Reset"] = str(reset_seconds)

            # Periodic cleanup
            self._cleanup_old_buckets()

            return response
        else:
            # Rate limit exceeded
            wait_time = bucket.get_wait_time()
            retry_after = int(wait_time) + 1  # Round up

            logger.warning(
                "rate_limit_exceeded",
                identifier=identifier,
                path=request.url.path,
                wait_time_seconds=retry_after,
            )

            # Return 429 Too Many Requests
            return JSONResponse(
                status_code=429,
                content={
                    "error": "Rate limit exceeded",
                    "message": f"Too many requests. Please retry after {retry_after} seconds.",
                    "retry_after": retry_after,
                    "limit": self.requests_per_minute,
                },
                headers={
                    "X-RateLimit-Limit": str(self.requests_per_minute),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(None),
                    "Retry-After": str(retry_after),
                },
            )

    async def xǁRateLimitMiddlewareǁdispatch__mutmut_93(self, request: Request, call_next):
        """
        Process request with rate limiting

        Args:
            request: FastAPI request
            call_next: Next middleware in chain

        Returns:
            Response or 429 Too Many Requests
        """
        # Skip rate limiting for health checks
        if request.url.path in ["/health", "/", "/docs", "/redoc", "/openapi.json"]:
            return await call_next(request)

        # Get identifier and bucket
        identifier = self._get_identifier(request)
        bucket = self._get_bucket(identifier)

        # Try to consume token
        if bucket.consume():
            # Request allowed
            remaining = int(bucket.tokens)
            reset_seconds = int(bucket.capacity / bucket.refill_rate)

            logger.debug(
                "rate_limit_allowed",
                identifier=identifier,
                remaining=remaining,
                path=request.url.path,
            )

            # Process request
            response = await call_next(request)

            # Add rate limit headers
            response.headers["X-RateLimit-Limit"] = str(self.requests_per_minute)
            response.headers["X-RateLimit-Remaining"] = str(remaining)
            response.headers["X-RateLimit-Reset"] = str(reset_seconds)

            # Periodic cleanup
            self._cleanup_old_buckets()

            return response
        else:
            # Rate limit exceeded
            wait_time = bucket.get_wait_time()
            retry_after = int(wait_time) + 1  # Round up

            logger.warning(
                "rate_limit_exceeded",
                identifier=identifier,
                path=request.url.path,
                wait_time_seconds=retry_after,
            )

            # Return 429 Too Many Requests
            return JSONResponse(
                status_code=429,
                content={
                    "error": "Rate limit exceeded",
                    "message": f"Too many requests. Please retry after {retry_after} seconds.",
                    "retry_after": retry_after,
                    "limit": self.requests_per_minute,
                },
                headers={
                    "X-RateLimit-Limit": str(self.requests_per_minute),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(retry_after),
                    "XXRetry-AfterXX": str(retry_after),
                },
            )

    async def xǁRateLimitMiddlewareǁdispatch__mutmut_94(self, request: Request, call_next):
        """
        Process request with rate limiting

        Args:
            request: FastAPI request
            call_next: Next middleware in chain

        Returns:
            Response or 429 Too Many Requests
        """
        # Skip rate limiting for health checks
        if request.url.path in ["/health", "/", "/docs", "/redoc", "/openapi.json"]:
            return await call_next(request)

        # Get identifier and bucket
        identifier = self._get_identifier(request)
        bucket = self._get_bucket(identifier)

        # Try to consume token
        if bucket.consume():
            # Request allowed
            remaining = int(bucket.tokens)
            reset_seconds = int(bucket.capacity / bucket.refill_rate)

            logger.debug(
                "rate_limit_allowed",
                identifier=identifier,
                remaining=remaining,
                path=request.url.path,
            )

            # Process request
            response = await call_next(request)

            # Add rate limit headers
            response.headers["X-RateLimit-Limit"] = str(self.requests_per_minute)
            response.headers["X-RateLimit-Remaining"] = str(remaining)
            response.headers["X-RateLimit-Reset"] = str(reset_seconds)

            # Periodic cleanup
            self._cleanup_old_buckets()

            return response
        else:
            # Rate limit exceeded
            wait_time = bucket.get_wait_time()
            retry_after = int(wait_time) + 1  # Round up

            logger.warning(
                "rate_limit_exceeded",
                identifier=identifier,
                path=request.url.path,
                wait_time_seconds=retry_after,
            )

            # Return 429 Too Many Requests
            return JSONResponse(
                status_code=429,
                content={
                    "error": "Rate limit exceeded",
                    "message": f"Too many requests. Please retry after {retry_after} seconds.",
                    "retry_after": retry_after,
                    "limit": self.requests_per_minute,
                },
                headers={
                    "X-RateLimit-Limit": str(self.requests_per_minute),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(retry_after),
                    "retry-after": str(retry_after),
                },
            )

    async def xǁRateLimitMiddlewareǁdispatch__mutmut_95(self, request: Request, call_next):
        """
        Process request with rate limiting

        Args:
            request: FastAPI request
            call_next: Next middleware in chain

        Returns:
            Response or 429 Too Many Requests
        """
        # Skip rate limiting for health checks
        if request.url.path in ["/health", "/", "/docs", "/redoc", "/openapi.json"]:
            return await call_next(request)

        # Get identifier and bucket
        identifier = self._get_identifier(request)
        bucket = self._get_bucket(identifier)

        # Try to consume token
        if bucket.consume():
            # Request allowed
            remaining = int(bucket.tokens)
            reset_seconds = int(bucket.capacity / bucket.refill_rate)

            logger.debug(
                "rate_limit_allowed",
                identifier=identifier,
                remaining=remaining,
                path=request.url.path,
            )

            # Process request
            response = await call_next(request)

            # Add rate limit headers
            response.headers["X-RateLimit-Limit"] = str(self.requests_per_minute)
            response.headers["X-RateLimit-Remaining"] = str(remaining)
            response.headers["X-RateLimit-Reset"] = str(reset_seconds)

            # Periodic cleanup
            self._cleanup_old_buckets()

            return response
        else:
            # Rate limit exceeded
            wait_time = bucket.get_wait_time()
            retry_after = int(wait_time) + 1  # Round up

            logger.warning(
                "rate_limit_exceeded",
                identifier=identifier,
                path=request.url.path,
                wait_time_seconds=retry_after,
            )

            # Return 429 Too Many Requests
            return JSONResponse(
                status_code=429,
                content={
                    "error": "Rate limit exceeded",
                    "message": f"Too many requests. Please retry after {retry_after} seconds.",
                    "retry_after": retry_after,
                    "limit": self.requests_per_minute,
                },
                headers={
                    "X-RateLimit-Limit": str(self.requests_per_minute),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(retry_after),
                    "RETRY-AFTER": str(retry_after),
                },
            )

    async def xǁRateLimitMiddlewareǁdispatch__mutmut_96(self, request: Request, call_next):
        """
        Process request with rate limiting

        Args:
            request: FastAPI request
            call_next: Next middleware in chain

        Returns:
            Response or 429 Too Many Requests
        """
        # Skip rate limiting for health checks
        if request.url.path in ["/health", "/", "/docs", "/redoc", "/openapi.json"]:
            return await call_next(request)

        # Get identifier and bucket
        identifier = self._get_identifier(request)
        bucket = self._get_bucket(identifier)

        # Try to consume token
        if bucket.consume():
            # Request allowed
            remaining = int(bucket.tokens)
            reset_seconds = int(bucket.capacity / bucket.refill_rate)

            logger.debug(
                "rate_limit_allowed",
                identifier=identifier,
                remaining=remaining,
                path=request.url.path,
            )

            # Process request
            response = await call_next(request)

            # Add rate limit headers
            response.headers["X-RateLimit-Limit"] = str(self.requests_per_minute)
            response.headers["X-RateLimit-Remaining"] = str(remaining)
            response.headers["X-RateLimit-Reset"] = str(reset_seconds)

            # Periodic cleanup
            self._cleanup_old_buckets()

            return response
        else:
            # Rate limit exceeded
            wait_time = bucket.get_wait_time()
            retry_after = int(wait_time) + 1  # Round up

            logger.warning(
                "rate_limit_exceeded",
                identifier=identifier,
                path=request.url.path,
                wait_time_seconds=retry_after,
            )

            # Return 429 Too Many Requests
            return JSONResponse(
                status_code=429,
                content={
                    "error": "Rate limit exceeded",
                    "message": f"Too many requests. Please retry after {retry_after} seconds.",
                    "retry_after": retry_after,
                    "limit": self.requests_per_minute,
                },
                headers={
                    "X-RateLimit-Limit": str(self.requests_per_minute),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(retry_after),
                    "Retry-After": str(None),
                },
            )
    
    xǁRateLimitMiddlewareǁdispatch__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁRateLimitMiddlewareǁdispatch__mutmut_1': xǁRateLimitMiddlewareǁdispatch__mutmut_1, 
        'xǁRateLimitMiddlewareǁdispatch__mutmut_2': xǁRateLimitMiddlewareǁdispatch__mutmut_2, 
        'xǁRateLimitMiddlewareǁdispatch__mutmut_3': xǁRateLimitMiddlewareǁdispatch__mutmut_3, 
        'xǁRateLimitMiddlewareǁdispatch__mutmut_4': xǁRateLimitMiddlewareǁdispatch__mutmut_4, 
        'xǁRateLimitMiddlewareǁdispatch__mutmut_5': xǁRateLimitMiddlewareǁdispatch__mutmut_5, 
        'xǁRateLimitMiddlewareǁdispatch__mutmut_6': xǁRateLimitMiddlewareǁdispatch__mutmut_6, 
        'xǁRateLimitMiddlewareǁdispatch__mutmut_7': xǁRateLimitMiddlewareǁdispatch__mutmut_7, 
        'xǁRateLimitMiddlewareǁdispatch__mutmut_8': xǁRateLimitMiddlewareǁdispatch__mutmut_8, 
        'xǁRateLimitMiddlewareǁdispatch__mutmut_9': xǁRateLimitMiddlewareǁdispatch__mutmut_9, 
        'xǁRateLimitMiddlewareǁdispatch__mutmut_10': xǁRateLimitMiddlewareǁdispatch__mutmut_10, 
        'xǁRateLimitMiddlewareǁdispatch__mutmut_11': xǁRateLimitMiddlewareǁdispatch__mutmut_11, 
        'xǁRateLimitMiddlewareǁdispatch__mutmut_12': xǁRateLimitMiddlewareǁdispatch__mutmut_12, 
        'xǁRateLimitMiddlewareǁdispatch__mutmut_13': xǁRateLimitMiddlewareǁdispatch__mutmut_13, 
        'xǁRateLimitMiddlewareǁdispatch__mutmut_14': xǁRateLimitMiddlewareǁdispatch__mutmut_14, 
        'xǁRateLimitMiddlewareǁdispatch__mutmut_15': xǁRateLimitMiddlewareǁdispatch__mutmut_15, 
        'xǁRateLimitMiddlewareǁdispatch__mutmut_16': xǁRateLimitMiddlewareǁdispatch__mutmut_16, 
        'xǁRateLimitMiddlewareǁdispatch__mutmut_17': xǁRateLimitMiddlewareǁdispatch__mutmut_17, 
        'xǁRateLimitMiddlewareǁdispatch__mutmut_18': xǁRateLimitMiddlewareǁdispatch__mutmut_18, 
        'xǁRateLimitMiddlewareǁdispatch__mutmut_19': xǁRateLimitMiddlewareǁdispatch__mutmut_19, 
        'xǁRateLimitMiddlewareǁdispatch__mutmut_20': xǁRateLimitMiddlewareǁdispatch__mutmut_20, 
        'xǁRateLimitMiddlewareǁdispatch__mutmut_21': xǁRateLimitMiddlewareǁdispatch__mutmut_21, 
        'xǁRateLimitMiddlewareǁdispatch__mutmut_22': xǁRateLimitMiddlewareǁdispatch__mutmut_22, 
        'xǁRateLimitMiddlewareǁdispatch__mutmut_23': xǁRateLimitMiddlewareǁdispatch__mutmut_23, 
        'xǁRateLimitMiddlewareǁdispatch__mutmut_24': xǁRateLimitMiddlewareǁdispatch__mutmut_24, 
        'xǁRateLimitMiddlewareǁdispatch__mutmut_25': xǁRateLimitMiddlewareǁdispatch__mutmut_25, 
        'xǁRateLimitMiddlewareǁdispatch__mutmut_26': xǁRateLimitMiddlewareǁdispatch__mutmut_26, 
        'xǁRateLimitMiddlewareǁdispatch__mutmut_27': xǁRateLimitMiddlewareǁdispatch__mutmut_27, 
        'xǁRateLimitMiddlewareǁdispatch__mutmut_28': xǁRateLimitMiddlewareǁdispatch__mutmut_28, 
        'xǁRateLimitMiddlewareǁdispatch__mutmut_29': xǁRateLimitMiddlewareǁdispatch__mutmut_29, 
        'xǁRateLimitMiddlewareǁdispatch__mutmut_30': xǁRateLimitMiddlewareǁdispatch__mutmut_30, 
        'xǁRateLimitMiddlewareǁdispatch__mutmut_31': xǁRateLimitMiddlewareǁdispatch__mutmut_31, 
        'xǁRateLimitMiddlewareǁdispatch__mutmut_32': xǁRateLimitMiddlewareǁdispatch__mutmut_32, 
        'xǁRateLimitMiddlewareǁdispatch__mutmut_33': xǁRateLimitMiddlewareǁdispatch__mutmut_33, 
        'xǁRateLimitMiddlewareǁdispatch__mutmut_34': xǁRateLimitMiddlewareǁdispatch__mutmut_34, 
        'xǁRateLimitMiddlewareǁdispatch__mutmut_35': xǁRateLimitMiddlewareǁdispatch__mutmut_35, 
        'xǁRateLimitMiddlewareǁdispatch__mutmut_36': xǁRateLimitMiddlewareǁdispatch__mutmut_36, 
        'xǁRateLimitMiddlewareǁdispatch__mutmut_37': xǁRateLimitMiddlewareǁdispatch__mutmut_37, 
        'xǁRateLimitMiddlewareǁdispatch__mutmut_38': xǁRateLimitMiddlewareǁdispatch__mutmut_38, 
        'xǁRateLimitMiddlewareǁdispatch__mutmut_39': xǁRateLimitMiddlewareǁdispatch__mutmut_39, 
        'xǁRateLimitMiddlewareǁdispatch__mutmut_40': xǁRateLimitMiddlewareǁdispatch__mutmut_40, 
        'xǁRateLimitMiddlewareǁdispatch__mutmut_41': xǁRateLimitMiddlewareǁdispatch__mutmut_41, 
        'xǁRateLimitMiddlewareǁdispatch__mutmut_42': xǁRateLimitMiddlewareǁdispatch__mutmut_42, 
        'xǁRateLimitMiddlewareǁdispatch__mutmut_43': xǁRateLimitMiddlewareǁdispatch__mutmut_43, 
        'xǁRateLimitMiddlewareǁdispatch__mutmut_44': xǁRateLimitMiddlewareǁdispatch__mutmut_44, 
        'xǁRateLimitMiddlewareǁdispatch__mutmut_45': xǁRateLimitMiddlewareǁdispatch__mutmut_45, 
        'xǁRateLimitMiddlewareǁdispatch__mutmut_46': xǁRateLimitMiddlewareǁdispatch__mutmut_46, 
        'xǁRateLimitMiddlewareǁdispatch__mutmut_47': xǁRateLimitMiddlewareǁdispatch__mutmut_47, 
        'xǁRateLimitMiddlewareǁdispatch__mutmut_48': xǁRateLimitMiddlewareǁdispatch__mutmut_48, 
        'xǁRateLimitMiddlewareǁdispatch__mutmut_49': xǁRateLimitMiddlewareǁdispatch__mutmut_49, 
        'xǁRateLimitMiddlewareǁdispatch__mutmut_50': xǁRateLimitMiddlewareǁdispatch__mutmut_50, 
        'xǁRateLimitMiddlewareǁdispatch__mutmut_51': xǁRateLimitMiddlewareǁdispatch__mutmut_51, 
        'xǁRateLimitMiddlewareǁdispatch__mutmut_52': xǁRateLimitMiddlewareǁdispatch__mutmut_52, 
        'xǁRateLimitMiddlewareǁdispatch__mutmut_53': xǁRateLimitMiddlewareǁdispatch__mutmut_53, 
        'xǁRateLimitMiddlewareǁdispatch__mutmut_54': xǁRateLimitMiddlewareǁdispatch__mutmut_54, 
        'xǁRateLimitMiddlewareǁdispatch__mutmut_55': xǁRateLimitMiddlewareǁdispatch__mutmut_55, 
        'xǁRateLimitMiddlewareǁdispatch__mutmut_56': xǁRateLimitMiddlewareǁdispatch__mutmut_56, 
        'xǁRateLimitMiddlewareǁdispatch__mutmut_57': xǁRateLimitMiddlewareǁdispatch__mutmut_57, 
        'xǁRateLimitMiddlewareǁdispatch__mutmut_58': xǁRateLimitMiddlewareǁdispatch__mutmut_58, 
        'xǁRateLimitMiddlewareǁdispatch__mutmut_59': xǁRateLimitMiddlewareǁdispatch__mutmut_59, 
        'xǁRateLimitMiddlewareǁdispatch__mutmut_60': xǁRateLimitMiddlewareǁdispatch__mutmut_60, 
        'xǁRateLimitMiddlewareǁdispatch__mutmut_61': xǁRateLimitMiddlewareǁdispatch__mutmut_61, 
        'xǁRateLimitMiddlewareǁdispatch__mutmut_62': xǁRateLimitMiddlewareǁdispatch__mutmut_62, 
        'xǁRateLimitMiddlewareǁdispatch__mutmut_63': xǁRateLimitMiddlewareǁdispatch__mutmut_63, 
        'xǁRateLimitMiddlewareǁdispatch__mutmut_64': xǁRateLimitMiddlewareǁdispatch__mutmut_64, 
        'xǁRateLimitMiddlewareǁdispatch__mutmut_65': xǁRateLimitMiddlewareǁdispatch__mutmut_65, 
        'xǁRateLimitMiddlewareǁdispatch__mutmut_66': xǁRateLimitMiddlewareǁdispatch__mutmut_66, 
        'xǁRateLimitMiddlewareǁdispatch__mutmut_67': xǁRateLimitMiddlewareǁdispatch__mutmut_67, 
        'xǁRateLimitMiddlewareǁdispatch__mutmut_68': xǁRateLimitMiddlewareǁdispatch__mutmut_68, 
        'xǁRateLimitMiddlewareǁdispatch__mutmut_69': xǁRateLimitMiddlewareǁdispatch__mutmut_69, 
        'xǁRateLimitMiddlewareǁdispatch__mutmut_70': xǁRateLimitMiddlewareǁdispatch__mutmut_70, 
        'xǁRateLimitMiddlewareǁdispatch__mutmut_71': xǁRateLimitMiddlewareǁdispatch__mutmut_71, 
        'xǁRateLimitMiddlewareǁdispatch__mutmut_72': xǁRateLimitMiddlewareǁdispatch__mutmut_72, 
        'xǁRateLimitMiddlewareǁdispatch__mutmut_73': xǁRateLimitMiddlewareǁdispatch__mutmut_73, 
        'xǁRateLimitMiddlewareǁdispatch__mutmut_74': xǁRateLimitMiddlewareǁdispatch__mutmut_74, 
        'xǁRateLimitMiddlewareǁdispatch__mutmut_75': xǁRateLimitMiddlewareǁdispatch__mutmut_75, 
        'xǁRateLimitMiddlewareǁdispatch__mutmut_76': xǁRateLimitMiddlewareǁdispatch__mutmut_76, 
        'xǁRateLimitMiddlewareǁdispatch__mutmut_77': xǁRateLimitMiddlewareǁdispatch__mutmut_77, 
        'xǁRateLimitMiddlewareǁdispatch__mutmut_78': xǁRateLimitMiddlewareǁdispatch__mutmut_78, 
        'xǁRateLimitMiddlewareǁdispatch__mutmut_79': xǁRateLimitMiddlewareǁdispatch__mutmut_79, 
        'xǁRateLimitMiddlewareǁdispatch__mutmut_80': xǁRateLimitMiddlewareǁdispatch__mutmut_80, 
        'xǁRateLimitMiddlewareǁdispatch__mutmut_81': xǁRateLimitMiddlewareǁdispatch__mutmut_81, 
        'xǁRateLimitMiddlewareǁdispatch__mutmut_82': xǁRateLimitMiddlewareǁdispatch__mutmut_82, 
        'xǁRateLimitMiddlewareǁdispatch__mutmut_83': xǁRateLimitMiddlewareǁdispatch__mutmut_83, 
        'xǁRateLimitMiddlewareǁdispatch__mutmut_84': xǁRateLimitMiddlewareǁdispatch__mutmut_84, 
        'xǁRateLimitMiddlewareǁdispatch__mutmut_85': xǁRateLimitMiddlewareǁdispatch__mutmut_85, 
        'xǁRateLimitMiddlewareǁdispatch__mutmut_86': xǁRateLimitMiddlewareǁdispatch__mutmut_86, 
        'xǁRateLimitMiddlewareǁdispatch__mutmut_87': xǁRateLimitMiddlewareǁdispatch__mutmut_87, 
        'xǁRateLimitMiddlewareǁdispatch__mutmut_88': xǁRateLimitMiddlewareǁdispatch__mutmut_88, 
        'xǁRateLimitMiddlewareǁdispatch__mutmut_89': xǁRateLimitMiddlewareǁdispatch__mutmut_89, 
        'xǁRateLimitMiddlewareǁdispatch__mutmut_90': xǁRateLimitMiddlewareǁdispatch__mutmut_90, 
        'xǁRateLimitMiddlewareǁdispatch__mutmut_91': xǁRateLimitMiddlewareǁdispatch__mutmut_91, 
        'xǁRateLimitMiddlewareǁdispatch__mutmut_92': xǁRateLimitMiddlewareǁdispatch__mutmut_92, 
        'xǁRateLimitMiddlewareǁdispatch__mutmut_93': xǁRateLimitMiddlewareǁdispatch__mutmut_93, 
        'xǁRateLimitMiddlewareǁdispatch__mutmut_94': xǁRateLimitMiddlewareǁdispatch__mutmut_94, 
        'xǁRateLimitMiddlewareǁdispatch__mutmut_95': xǁRateLimitMiddlewareǁdispatch__mutmut_95, 
        'xǁRateLimitMiddlewareǁdispatch__mutmut_96': xǁRateLimitMiddlewareǁdispatch__mutmut_96
    }
    
    def dispatch(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁRateLimitMiddlewareǁdispatch__mutmut_orig"), object.__getattribute__(self, "xǁRateLimitMiddlewareǁdispatch__mutmut_mutants"), args, kwargs, self)
        return result 
    
    dispatch.__signature__ = _mutmut_signature(xǁRateLimitMiddlewareǁdispatch__mutmut_orig)
    xǁRateLimitMiddlewareǁdispatch__mutmut_orig.__name__ = 'xǁRateLimitMiddlewareǁdispatch'
