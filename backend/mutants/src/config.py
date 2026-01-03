"""
Backend configuration
Environment variables and application settings
"""

from typing import List, Union
from pydantic import field_validator
from pydantic_settings import BaseSettings
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


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    # Application
    ENV: str = "development"
    DEBUG: bool = True
    LOG_LEVEL: str = "DEBUG"
    APP_VERSION: str = "0.1.0"

    # Gemini AI (Google AI Studio)
    GOOGLE_API_KEY: str

    # Supabase
    SUPABASE_URL: str
    SUPABASE_ANON_KEY: str
    SUPABASE_SERVICE_ROLE_KEY: str
    DATABASE_URL: str

    # Clerk Authentication
    CLERK_SECRET_KEY: str
    CLERK_PUBLISHABLE_KEY: str

    # Stripe Payments
    STRIPE_SECRET_KEY: str
    STRIPE_WEBHOOK_SECRET: str
    STRIPE_PRICE_ID: str
    STRIPE_PRICE_AMOUNT: int = 299  # £2.99 in pence
    STRIPE_CURRENCY: str = "gbp"

    # CORS
    ALLOWED_ORIGINS: Union[List[str], str] = "http://localhost:3000,http://127.0.0.1:3000"

    # Cron Secret (for scheduled jobs)
    CRON_SECRET: str

    # Report settings
    REPORT_EXPIRY_DAYS: int = 30
    REPORT_SOFT_DELETE_DAYS: int = 60
    REPORT_HARD_DELETE_DAYS: int = 30  # After soft delete

    # Rate Limiting (aligned with shared config schema)
    ENABLE_RATE_LIMITING: bool = True
    RATE_LIMIT_MAX: int = 100
    RATE_LIMIT_WINDOW_SEC: int = 60
    RATE_LIMIT_REPORTS_PER_DAY: int = 10

    @field_validator("ALLOWED_ORIGINS", mode="before")
    @classmethod
    def parse_allowed_origins(cls, v):
        """Parse ALLOWED_ORIGINS from comma-separated string or list"""
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v

    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()
