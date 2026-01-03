# MVP UK Study & Migration App - Backend

FastAPI backend service for the UK Study & Migration Research Application.

## Quick Start

### Prerequisites

- Python 3.12+
- PostgreSQL 15+ (local) or Supabase account
- Virtual environment (venv)

### Setup

```bash
# Create and activate virtual environment
python3.12 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -e ".[dev]"

# Copy environment template
cp .env.example .env

# Edit .env with your configuration
# Set DATABASE_URL, GOOGLE_API_KEY, CLERK keys, STRIPE keys, etc.
```

### Database Migrations

```bash
# Apply all migrations
./scripts/migrate.sh upgrade

# Check migration status
./scripts/migrate.sh status

# Create new migration (after modifying models)
./scripts/migrate.sh create "description_of_change"

# See alembic/README.md for detailed migration documentation
```

### Running the Backend

```bash
# Development mode with auto-reload
uvicorn src.main:app --reload --port 8000

# Production mode
uvicorn src.main:app --host 0.0.0.0 --port 8000
```

## Project Structure

```
backend/
├── src/
│   ├── config/           # Configuration management (Pydantic)
│   ├── database/         # SQLAlchemy models, repositories, adapters
│   ├── feature_flags/    # Feature flag module
│   ├── logging_lib/      # Structured logging (structlog)
│   └── main.py           # FastAPI application entry point
├── alembic/              # Database migrations
│   ├── versions/         # Migration files
│   ├── env.py           # Alembic environment config
│   └── README.md        # Migration documentation
├── tests/                # Pytest test suite
├── scripts/              # Helper scripts
│   └── migrate.sh       # Database migration helper
├── pyproject.toml        # Project dependencies and config
└── .env                  # Environment variables (not in git)
```

## Database Schema

The application uses PostgreSQL with the following tables:

- **users**: Authenticated user data (Clerk integration)
- **reports**: AI-generated study & migration reports
- **payments**: Stripe payment transactions

See `alembic/README.md` for complete schema documentation and migration guides.

## Environment Variables

Required variables in `.env`:

```bash
# Application
ENV=development
DEBUG=True
LOG_LEVEL=DEBUG

# Database
DATABASE_URL=postgresql://postgres:postgres@localhost:54322/postgres

# Google Gemini AI
GOOGLE_API_KEY=your_gemini_api_key_here

# Clerk Authentication
CLERK_SECRET_KEY=sk_test_your_clerk_secret_key
CLERK_PUBLISHABLE_KEY=pk_test_your_clerk_publishable_key

# Stripe Payments
STRIPE_SECRET_KEY=sk_test_your_stripe_secret_key
STRIPE_WEBHOOK_SECRET=whsec_your_stripe_webhook_secret
STRIPE_PRICE_ID=price_your_stripe_price_id

# Supabase (optional)
SUPABASE_URL=http://localhost:54321
SUPABASE_ANON_KEY=your_supabase_anon_key
SUPABASE_SERVICE_ROLE_KEY=your_supabase_service_role_key

# CORS
ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# Cron Secret
CRON_SECRET=your_random_cron_secret_here
```

See `.env.example` for complete template.

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_database.py

# Run mutation tests (slower)
mutmut run
```

## Code Quality

```bash
# Format code
black src tests

# Lint code
ruff check src tests

# Type check
mypy src
```

## Modules

### 1. Config (`src/config/`)

Environment-based configuration using Pydantic:

```python
from config import config_loader

config = config_loader.load()
print(config.DATABASE_URL)
```

### 2. Database (`src/database/`)

SQLAlchemy ORM models and repositories:

```python
from database.models import User, Report, Payment
from database.repositories import UserRepository

# Use repositories for database operations
user_repo = UserRepository(adapter)
user = await user_repo.get_by_clerk_id("user_123")
```

### 3. Feature Flags (`src/feature_flags/`)

Runtime feature toggles:

```python
from feature_flags import FeatureFlags

flags = FeatureFlags()
if flags.is_enabled("ENABLE_SUPABASE"):
    # Use Supabase
else:
    # Use PostgreSQL
```

### 4. Logging (`src/logging_lib/`)

Structured logging with structlog:

```python
from logging_lib import get_logger

logger = get_logger(__name__)
logger.info("user_created", user_id=user.user_id, email=user.email)
```

## API Endpoints

(To be documented as endpoints are implemented)

- `POST /api/auth/webhook` - Clerk webhook for user sync
- `POST /api/payments/create-checkout` - Create Stripe checkout session
- `POST /api/payments/webhook` - Stripe webhook handler
- `GET /api/reports/:id` - Retrieve report by ID
- `POST /api/reports/generate` - Generate new report

## Deployment

### Docker

```bash
# Build image
docker build -t study-abroad-backend .

# Run container
docker run -p 8000:8000 --env-file .env study-abroad-backend
```

### Supabase Edge Functions

(To be documented when implemented)

## Contributing

1. Create feature branch from `main`
2. Implement changes with tests
3. Run code quality checks (`black`, `ruff`, `mypy`)
4. Ensure tests pass (`pytest`)
5. Create pull request

## License

Proprietary - All Rights Reserved

## Support

For issues or questions, refer to:
- Project Specification: `/specs/001-mvp-uk-study-migration/`
- Migration Guide: `alembic/README.md`
- Data Model: `/specs/001-mvp-uk-study-migration/data-model.md`
