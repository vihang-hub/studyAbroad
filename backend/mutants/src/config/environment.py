"""
Environment Configuration Schema

Pydantic models for environment configuration validation.
Equivalent to TypeScript schemas/environment.schema.ts.
"""

from typing import Literal
from pydantic import BaseModel, Field, HttpUrl, field_validator, model_validator
from pydantic_settings import BaseSettings


# Type Aliases
EnvironmentMode = Literal["dev", "test", "production"]
LogLevel = Literal["DEBUG", "INFO", "WARN", "ERROR"]
AuthProvider = Literal["google", "apple", "facebook", "email"]
PaymentStatus = Literal[
    "requires_payment_method",
    "requires_confirmation",
    "processing",
    "succeeded",
    "failed",
    "canceled",
    "bypassed",
]
ReportStatus = Literal["generating", "completed", "failed"]
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


class DatabaseConfig(BaseModel):
    """Database configuration section"""

    DATABASE_URL: str = Field(..., description="PostgreSQL or Supabase connection URL")
    SUPABASE_URL: HttpUrl | None = Field(None, description="Supabase project URL")
    SUPABASE_ANON_KEY: str | None = Field(None, description="Supabase anonymous/public key")
    SUPABASE_SERVICE_ROLE_KEY: str | None = Field(
        None, description="Supabase service role key (backend only)"
    )
    DATABASE_POOL_MAX: int = Field(20, ge=1, le=100, description="Maximum connection pool size")
    DATABASE_IDLE_TIMEOUT_MS: int = Field(
        30000, ge=1000, description="Connection idle timeout (ms)"
    )
    DATABASE_CONNECTION_TIMEOUT_MS: int = Field(2000, ge=500, description="Connection timeout (ms)")


class LoggingConfig(BaseModel):
    """Logging configuration section"""

    LOG_LEVEL: LogLevel = Field("DEBUG", description="Logging level")
    LOG_DIR: str = Field("./logs", description="Directory for log files")
    LOG_MAX_SIZE_MB: int = Field(100, ge=1, le=1000, description="Max log file size (MB)")
    LOG_ROTATION_DAYS: int = Field(1, ge=1, le=365, description="Log rotation interval (days)")
    LOG_RETENTION_DAYS: int = Field(30, ge=1, le=365, description="Log retention period (days)")
    LOG_CONSOLE_ENABLED: bool = Field(True, description="Enable console logging")
    LOG_PRETTY_PRINT: bool = Field(False, description="Enable pretty printing (dev only)")


class FeatureFlagsConfig(BaseModel):
    """Feature flags configuration section"""

    ENABLE_SUPABASE: bool = Field(False, description="Enable Supabase database backend")
    ENABLE_PAYMENTS: bool = Field(False, description="Enable payment processing via Stripe")
    ENABLE_RATE_LIMITING: bool = Field(True, description="Enable rate limiting")
    ENABLE_OBSERVABILITY: bool = Field(False, description="Enable observability/monitoring")


class ClerkConfig(BaseModel):
    """Clerk authentication configuration section"""

    CLERK_PUBLISHABLE_KEY: str = Field(..., min_length=1, description="Clerk publishable key")
    CLERK_SECRET_KEY: str = Field(..., min_length=1, description="Clerk secret key")
    CLERK_WEBHOOK_SECRET: str | None = Field(
        None, description="Clerk webhook secret for signature verification"
    )


class StripeConfig(BaseModel):
    """Stripe payment configuration section"""

    STRIPE_PUBLISHABLE_KEY: str | None = Field(None, description="Stripe publishable key")
    STRIPE_SECRET_KEY: str | None = Field(None, description="Stripe secret key")
    STRIPE_WEBHOOK_SECRET: str | None = Field(
        None, description="Stripe webhook secret for signature verification"
    )
    STRIPE_PRICE_ID: str | None = Field(None, description="Stripe price ID for £2.99 report")
    PAYMENT_AMOUNT: float = Field(2.99, ge=2.99, le=2.99, description="Payment amount in GBP")
    PAYMENT_CURRENCY: Literal["GBP"] = Field("GBP", description="Payment currency")


class GeminiConfig(BaseModel):
    """Gemini AI configuration section"""

    GEMINI_API_KEY: str = Field(..., min_length=1, description="Google Gemini API key")
    GEMINI_MODEL: str = Field("gemini-1.5-pro", description="Gemini model to use")
    GEMINI_MAX_TOKENS: int = Field(8192, ge=1000, description="Maximum tokens for generation")
    GEMINI_TEMPERATURE: float = Field(0.7, ge=0.0, le=1.0, description="Temperature (0-1)")
    GEMINI_TIMEOUT_MS: int = Field(60000, ge=5000, description="Request timeout (ms)")


class AppConfig(BaseModel):
    """Application configuration section"""

    APP_NAME: str = Field("Study Abroad MVP", description="Application name")
    APP_VERSION: str = Field("1.0.0", description="Application version")
    API_URL: HttpUrl = Field("http://localhost:8000", description="Backend API URL")
    PORT: int = Field(8000, ge=1, le=65535, description="Server port")
    NODE_ENV: Literal["development", "test", "production"] = Field(
        "development", description="Node environment"
    )


class RateLimitConfig(BaseModel):
    """Rate limiting configuration section"""

    RATE_LIMIT_MAX: int = Field(100, ge=1, description="Maximum requests per window")
    RATE_LIMIT_WINDOW_SEC: int = Field(60, ge=1, description="Rate limit window (seconds)")
    RATE_LIMIT_REPORTS_PER_DAY: int = Field(
        10, ge=1, description="Report generation limit per user per day"
    )


class EnvironmentConfig(BaseSettings):
    """
    Full Environment Configuration

    Combines all configuration sections with validation rules.
    Loads from environment variables with Pydantic Settings.
    """

    # Environment
    ENVIRONMENT_MODE: EnvironmentMode = Field("dev", description="Environment mode")

    # Database
    DATABASE_URL: str = Field(..., description="PostgreSQL or Supabase connection URL")
    SUPABASE_URL: HttpUrl | None = Field(None, description="Supabase project URL")
    SUPABASE_ANON_KEY: str | None = Field(None, description="Supabase anonymous/public key")
    SUPABASE_SERVICE_ROLE_KEY: str | None = Field(
        None, description="Supabase service role key (backend only)"
    )
    DATABASE_POOL_MAX: int = Field(20, ge=1, le=100)
    DATABASE_IDLE_TIMEOUT_MS: int = Field(30000, ge=1000)
    DATABASE_CONNECTION_TIMEOUT_MS: int = Field(2000, ge=500)

    # Logging
    LOG_LEVEL: LogLevel = Field("DEBUG", description="Logging level")
    LOG_DIR: str = Field("./logs")
    LOG_MAX_SIZE_MB: int = Field(100, ge=1, le=1000)
    LOG_ROTATION_DAYS: int = Field(1, ge=1, le=365)
    LOG_RETENTION_DAYS: int = Field(30, ge=1, le=365)
    LOG_CONSOLE_ENABLED: bool = Field(True)
    LOG_PRETTY_PRINT: bool = Field(False)

    # Feature Flags
    ENABLE_SUPABASE: bool = Field(False)
    ENABLE_PAYMENTS: bool = Field(False)
    ENABLE_RATE_LIMITING: bool = Field(True)
    ENABLE_OBSERVABILITY: bool = Field(False)

    # Clerk Authentication
    CLERK_PUBLISHABLE_KEY: str = Field(..., min_length=1)
    CLERK_SECRET_KEY: str = Field(..., min_length=1)
    CLERK_WEBHOOK_SECRET: str | None = Field(None)

    # Stripe Payment
    STRIPE_PUBLISHABLE_KEY: str | None = Field(None)
    STRIPE_SECRET_KEY: str | None = Field(None)
    STRIPE_WEBHOOK_SECRET: str | None = Field(None)
    STRIPE_PRICE_ID: str | None = Field(None)
    PAYMENT_AMOUNT: float = Field(2.99, ge=2.99, le=2.99)
    PAYMENT_CURRENCY: Literal["GBP"] = Field("GBP")

    # Gemini AI
    GEMINI_API_KEY: str = Field(..., min_length=1)
    GEMINI_MODEL: str = Field("gemini-1.5-pro")
    GEMINI_MAX_TOKENS: int = Field(8192, ge=1000)
    GEMINI_TEMPERATURE: float = Field(0.7, ge=0.0, le=1.0)
    GEMINI_TIMEOUT_MS: int = Field(60000, ge=5000)

    # Application
    APP_NAME: str = Field("Study Abroad MVP")
    APP_VERSION: str = Field("1.0.0")
    API_URL: str = Field("http://localhost:8000")
    PORT: int = Field(8000, ge=1, le=65535)
    NODE_ENV: Literal["development", "test", "production"] = Field("development")

    # Rate Limiting
    RATE_LIMIT_MAX: int = Field(100, ge=1)
    RATE_LIMIT_WINDOW_SEC: int = Field(60, ge=1)
    RATE_LIMIT_REPORTS_PER_DAY: int = Field(10, ge=1)

    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "forbid"  # Reject unknown environment variables

    @field_validator("LOG_LEVEL", mode="before")
    @classmethod
    def set_log_level_from_environment(cls, v: str | None, info) -> str:
        """Set LOG_LEVEL based on ENVIRONMENT_MODE if not explicitly set"""
        if v is not None:
            return v

        # Get ENVIRONMENT_MODE from validation context
        environment_mode = info.data.get("ENVIRONMENT_MODE", "dev")
        if environment_mode == "production":
            return "ERROR"
        return "DEBUG"  # dev and test both use DEBUG

    @model_validator(mode="after")
    def validate_supabase_requirements(self):
        """Validate Supabase configuration when ENABLE_SUPABASE=true"""
        if self.ENABLE_SUPABASE:
            if not (self.SUPABASE_URL and self.SUPABASE_ANON_KEY):
                raise ValueError(
                    "SUPABASE_URL and SUPABASE_ANON_KEY are required when ENABLE_SUPABASE=true"
                )
        return self

    @model_validator(mode="after")
    def validate_payment_requirements(self):
        """Validate Stripe configuration when ENABLE_PAYMENTS=true"""
        if self.ENABLE_PAYMENTS:
            if not (
                self.STRIPE_PUBLISHABLE_KEY
                and self.STRIPE_SECRET_KEY
                and self.STRIPE_WEBHOOK_SECRET
            ):
                raise ValueError(
                    "STRIPE_PUBLISHABLE_KEY, STRIPE_SECRET_KEY, and STRIPE_WEBHOOK_SECRET "
                    "are required when ENABLE_PAYMENTS=true"
                )
        return self

    @model_validator(mode="after")
    def validate_production_requirements(self):
        """Validate production mode requirements"""
        if self.ENVIRONMENT_MODE == "production":
            if not (self.ENABLE_SUPABASE and self.ENABLE_PAYMENTS):
                raise ValueError(
                    "Production mode requires ENABLE_SUPABASE=true and ENABLE_PAYMENTS=true"
                )
        return self

    @model_validator(mode="after")
    def validate_dev_requirements(self):
        """Validate dev mode requirements"""
        if self.ENVIRONMENT_MODE == "dev":
            if self.ENABLE_SUPABASE or self.ENABLE_PAYMENTS:
                raise ValueError(
                    "Dev mode requires ENABLE_SUPABASE=false and ENABLE_PAYMENTS=false"
                )
        return self

    @model_validator(mode="after")
    def validate_test_requirements(self):
        """Validate test mode requirements"""
        if self.ENVIRONMENT_MODE == "test":
            if not self.ENABLE_SUPABASE or self.ENABLE_PAYMENTS:
                raise ValueError(
                    "Test mode requires ENABLE_SUPABASE=true and ENABLE_PAYMENTS=false"
                )
        return self
