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


class TokenBucket:
    """
    Token bucket implementation for rate limiting

    Allows bursts up to capacity, then refills at a constant rate.
    """

    def __init__(self, capacity: int, refill_rate: float):
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

    def consume(self, tokens: int = 1) -> bool:
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

    def get_wait_time(self, tokens: int = 1) -> float:
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

    def __init__(self, app, requests_per_minute: int = 100):
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

    def _get_identifier(self, request: Request) -> str:
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

    def _get_bucket(self, identifier: str) -> TokenBucket:
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

    def _cleanup_old_buckets(self):
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

    async def dispatch(self, request: Request, call_next):
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
