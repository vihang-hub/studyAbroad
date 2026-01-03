# @study-abroad/shared-config

Environment configuration management with type-safe validation using Zod.

## Features

- Type-safe configuration loading
- Runtime validation with Zod schemas
- Environment-specific presets (dev/test/production)
- Fail-fast on invalid configuration
- Singleton pattern for performance

## Installation

```bash
npm install @study-abroad/shared-config
```

## Usage

### Basic Usage

```typescript
import { ConfigLoader } from '@study-abroad/shared-config';

// Load configuration (validates on first call)
const config = ConfigLoader.load();

console.log(config.ENVIRONMENT_MODE); // 'dev' | 'test' | 'production'
console.log(config.DATABASE_URL);
console.log(config.LOG_LEVEL);
```

### Configuration Schema

All configuration fields are validated against this schema:

```typescript
{
  // Environment
  ENVIRONMENT_MODE: 'dev' | 'test' | 'production' (default: 'dev')

  // Feature Flags
  ENABLE_SUPABASE: boolean (default: false)
  ENABLE_PAYMENTS: boolean (default: false)

  // Database
  DATABASE_URL: string (required, must be valid URL)

  // Logging
  LOG_LEVEL: 'debug' | 'info' | 'warn' | 'error' (default: 'debug')
  LOG_MAX_SIZE_MB: number (default: 100)
  LOG_ROTATION_DAYS: number (default: 1)
  LOG_RETENTION_DAYS: number (default: 30)
  LOG_DIR: string (default: './logs')

  // API Keys (optional)
  GOOGLE_API_KEY?: string
  CLERK_SECRET_KEY?: string
  STRIPE_SECRET_KEY?: string
  SUPABASE_URL?: string
  SUPABASE_ANON_KEY?: string
}
```

### Environment Variables

Create a `.env` file in your project root:

```env
# Required
ENVIRONMENT_MODE=dev
DATABASE_URL=postgresql://user:pass@localhost:5432/db

# Optional (with defaults)
ENABLE_SUPABASE=false
ENABLE_PAYMENTS=false
LOG_LEVEL=debug
LOG_MAX_SIZE_MB=100
LOG_RETENTION_DAYS=30
```

### Validation Errors

If configuration is invalid, `ConfigLoader.load()` throws with clear error messages:

```
Configuration validation failed:
{
  DATABASE_URL: { _errors: ['Invalid url'] },
  LOG_LEVEL: { _errors: ['Invalid enum value. Expected "debug" | "info" | "warn" | "error"'] }
}
```

### Testing

Reset the singleton between tests:

```typescript
import { ConfigLoader } from '@study-abroad/shared-config';

beforeEach(() => {
  ConfigLoader.reset();
});

it('should load config', () => {
  process.env.DATABASE_URL = 'postgresql://localhost:5432/test';
  const config = ConfigLoader.load();
  expect(config.DATABASE_URL).toBe('postgresql://localhost:5432/test');
});
```

## Architecture Decision Record

See [ADR-0001: Environment Configuration System](/Users/vihang/projects/study-abroad/docs/adr/ADR-0001-environment-configuration-system.md)

## License

MIT
