# FastAPI Backend Module Integration Guide

## Overview

This guide documents the integration of all Python modules (configuration, feature flags, database, logging) into the FastAPI backend for the MVP UK Study & Migration App.

## Changes Made

### 1. New Files Created

#### `/backend/src/dependencies.py`
Dependency injection module providing FastAPI dependencies for:
- `get_config()` - Returns validated EnvironmentConfig
- `get_feature_flags()` - Returns FeatureFlagEvaluator
- `get_logger()` - Returns structured logger
- `get_db()` - Returns database adapter from app state
- `get_db_session()` - Returns database session with cleanup
- `get_correlation_id()` - Returns correlation ID from request
- `get_request_logger()` - Returns logger bound to request context

### 2. Updated Files

#### `/backend/src/main.py`
**Changes:**
- Added environment variable loading with `python-dotenv`
- Initialized logging first before any other modules
- Rewrote `lifespan()` context manager to:
  - Load and validate configuration
  - Initialize feature flags and log active flags
  - Initialize database adapter
  - Validate environment-specific requirements
  - Handle graceful shutdown
- Added `correlation_id_middleware` for request tracing
- Added `request_logging_middleware` for comprehensive request/response logging
- Updated root endpoint to show dynamic configuration and features

#### `/backend/src/api/routes/health.py`
**Changes:**
- Implemented actual health checks for:
  - Database connectivity
  - Gemini AI service configuration
  - Stripe payment service configuration
- Added dependency injection for config, feature flags, and database
- Returns detailed service status with response times
- Overall status: "healthy", "degraded", or "unhealthy"

#### `/backend/src/api/routes/reports.py`
**Changes:**
- Added dependency injection for all endpoints
- Integrated structured logging with correlation IDs
- Added feature flag checks for payments
- Dev mode: Bypasses payment when ENABLE_PAYMENTS=false
- Comprehensive logging for all operations

#### `/backend/src/api/routes/webhooks.py`
**Changes:**
- Added dependency injection
- Feature flag check: Only processes webhooks if ENABLE_PAYMENTS=true
- Enhanced logging for webhook events
- Passes logger to handler functions

#### `/backend/src/api/routes/stream.py`
**Changes:**
- Added dependency injection for database and logger
- Integrated with request logging context

### 3. Environment Variables

**Old variables (deprecated):**
- `ENV` → `ENVIRONMENT_MODE`
- `DEBUG` → removed (determined by ENVIRONMENT_MODE)
- `GOOGLE_API_KEY` → `GEMINI_API_KEY`
- `LOG_LEVEL` → still used, but optional (defaults based on ENVIRONMENT_MODE)
- `ALLOWED_ORIGINS` → removed (will be handled differently)
- `CRON_SECRET` → removed (not part of core config)

**New required variables:**
See `/backend/.env.example.new` for complete list.

**Key new variables:**
- `ENVIRONMENT_MODE` - "dev", "test", or "production"
- `GEMINI_API_KEY` - Replaces GOOGLE_API_KEY
- `ENABLE_SUPABASE` - Feature flag for Supabase backend
- `ENABLE_PAYMENTS` - Feature flag for Stripe payments
- `LOG_DIR`, `LOG_MAX_SIZE_MB`, `LOG_ROTATION_DAYS`, etc. - Logging configuration

## Architecture

### Module Initialization Flow

```
1. Load .env file (python-dotenv)
2. Initialize logging (logging_lib.logger)
3. Load configuration (config.loader)
4. Initialize feature flags (feature_flags.evaluator)
5. Initialize database adapter (database.adapters.factory)
6. Start FastAPI application
```

### Request Flow

```
1. Request arrives
2. Correlation ID middleware extracts/generates correlation ID
3. Request logging middleware logs request with sanitization
4. Route handler executes with dependency injection
5. Response logging middleware logs response
6. Correlation ID added to response headers
```

### Dependency Injection

All route handlers now use FastAPI's `Depends()` for:
- Configuration access
- Database connections
- Logging with request context
- Feature flag evaluation

Example:
```python
@router.get("/example")
async def example_endpoint(
    db: DatabaseAdapter = Depends(get_db),
    logger: structlog.BoundLogger = Depends(get_request_logger),
    feature_flags: FeatureFlagEvaluator = Depends(get_feature_flags),
):
    logger.info("processing_request")
    if feature_flags.is_enabled(Feature.PAYMENTS):
        # Payment-specific logic
    ...
```

## Environment Modes

### Development (ENVIRONMENT_MODE=dev)
- ENABLE_SUPABASE=false (uses local PostgreSQL)
- ENABLE_PAYMENTS=false (bypasses payment)
- LOG_LEVEL=DEBUG
- Pretty-printed logs
- Detailed error messages

### Test (ENVIRONMENT_MODE=test)
- ENABLE_SUPABASE=true (uses Supabase)
- ENABLE_PAYMENTS=false (mock payments)
- LOG_LEVEL=DEBUG
- JSON-formatted logs

### Production (ENVIRONMENT_MODE=production)
- ENABLE_SUPABASE=true (required)
- ENABLE_PAYMENTS=true (required)
- LOG_LEVEL=ERROR
- JSON-formatted logs
- Minimal error details in responses

## Migration Steps

### 1. Update Environment Variables

```bash
# Backup existing .env
cp .env .env.backup

# Update .env with new variables
# Use .env.example.new as reference

# Required changes:
ENV → ENVIRONMENT_MODE=dev
GOOGLE_API_KEY → GEMINI_API_KEY=your_key
# Add new variables: ENABLE_SUPABASE, ENABLE_PAYMENTS, etc.
```

### 2. Install Dependencies (if not already installed)

```bash
cd backend
pip install -r requirements.txt
# or
pip install fastapi uvicorn pydantic pydantic-settings structlog python-dotenv sqlalchemy asyncpg
```

### 3. Test Configuration

```bash
cd backend
python test_integration.py
```

All tests should pass if environment is configured correctly.

### 4. Run Application

```bash
cd backend
uvicorn src.main:app --reload --port 8000
```

Visit:
- http://localhost:8000 - API root (shows config and features)
- http://localhost:8000/health - Health check
- http://localhost:8000/docs - API documentation

## Testing

### Integration Test

Run the integration test to verify all modules are properly wired:

```bash
cd backend
source venv/bin/activate  # if using virtualenv
python test_integration.py
```

Expected output:
```
Configuration........................... ✓ PASS
Feature Flags........................... ✓ PASS
Logging................................. ✓ PASS
Database................................ ✓ PASS
Dependencies............................ ✓ PASS
API Imports............................. ✓ PASS
```

### Manual Testing

1. **Health Check:**
   ```bash
   curl http://localhost:8000/health
   ```
   
   Should return status for all services.

2. **Configuration:**
   ```bash
   curl http://localhost:8000
   ```
   
   Should show environment mode and active features.

3. **Logs:**
   Check `backend/logs/` for structured log files with correlation IDs.

## Troubleshooting

### Configuration Validation Errors

**Error:** "Extra inputs are not permitted"
**Solution:** Remove old environment variables (ENV, DEBUG, GOOGLE_API_KEY, etc.)

**Error:** "Field required"
**Solution:** Add missing required variables (see .env.example.new)

### Import Errors

**Error:** "No module named 'fastapi'"
**Solution:** Install dependencies: `pip install -r requirements.txt`

### Database Connection Errors

**Error:** Database not initialized
**Solution:** Ensure DATABASE_URL is set and PostgreSQL/Supabase is running

### Logging Errors

**Error:** Permission denied for log directory
**Solution:** Create log directory: `mkdir -p backend/logs`

## Best Practices

1. **Always use dependency injection** for database, logger, and config access
2. **Check feature flags** before executing feature-specific code
3. **Use correlation IDs** in all log messages (automatically added by middleware)
4. **Sanitize sensitive data** in logs (automatically handled by sanitizer)
5. **Handle errors gracefully** with appropriate HTTP status codes
6. **Log all important operations** with structured context

## API Changes

### Backward Compatibility

All existing API endpoints remain functional with the same contracts.

### New Features

1. **Correlation ID Tracking:** All responses include `X-Correlation-ID` header
2. **Enhanced Health Checks:** `/health` now returns detailed service status
3. **Dynamic Feature Configuration:** Root endpoint shows active features
4. **Structured Logging:** All operations logged with correlation IDs

## Next Steps

1. **Update .env file** with new variable names
2. **Run integration tests** to verify setup
3. **Test API endpoints** manually
4. **Review logs** to ensure proper formatting
5. **Monitor health endpoint** for service status

## Support

For issues or questions, refer to:
- ADRs in `/docs/adr/`
- Database schema in `/backend/migrations/`
- TypeScript shared packages in `/shared/`
