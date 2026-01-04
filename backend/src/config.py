"""
Backend configuration
Environment variables and application settings
"""

from typing import List, Union
from pydantic import field_validator
from pydantic_settings import BaseSettings


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
    ALLOWED_ORIGINS: Union[List[str], str] = "http://localhost:3000,http://localhost:3001,http://127.0.0.1:3000,http://127.0.0.1:3001"

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
