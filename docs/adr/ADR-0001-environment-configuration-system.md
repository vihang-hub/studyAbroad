# ADR-0001: Environment Configuration System

## Status
Accepted

## Context

The MVP UK Study & Migration Research App must support three distinct runtime environments (dev, test, production), each with different database configurations, feature enablement, and operational settings. The system needs to:

1. **Environment Separation**: Clearly distinguish between development (local PostgreSQL, no payments), test (Supabase, no payments), and production (Supabase with payments)
2. **Configuration Management**: Manage environment-specific settings through environment variables
3. **Developer Experience**: Enable developers to run the application locally without external dependencies
4. **Environment Parity**: Ensure database schemas are identical across environments
5. **Reusability**: Create a configuration system usable across multiple projects in the monorepo

### Requirements from Spec
- `ENVIRONMENT_MODE`: dev | test | production
- `ENABLE_SUPABASE`: true | false
- `ENABLE_PAYMENTS`: true | false
- `LOG_LEVEL`: debug | error
- `LOG_MAX_SIZE_MB`: integer (default: 100)
- `LOG_ROTATION_DAYS`: integer (default: 1)
- `LOG_RETENTION_DAYS`: integer (default: 30)
- `DATABASE_URL`: connection string (local PostgreSQL or Supabase)

### Constraints
- No secrets in source control
- Type-safe configuration access
- Fail-fast on missing required configuration
- Support for .env files (development) and platform secret managers (production)

## Decision

We will implement a **layered environment configuration system** with the following architecture:

### 1. Shared Configuration Package (`shared/config`)

Create a framework-agnostic configuration management library that:

**Core Components:**
- **Config Schema Definition**: TypeScript interfaces and validation schemas
- **Environment Loader**: Reads from process.env with type coercion
- **Validation Engine**: Uses Zod for runtime type checking and validation
- **Default Values**: Sensible defaults for non-sensitive settings
- **Multi-Environment Support**: dev/test/production presets

**Package Structure:**
```
shared/config/
├── src/
│   ├── schema.ts           # Zod schemas for all config sections
│   ├── loader.ts           # Environment variable loading
│   ├── validator.ts        # Validation logic
│   ├── presets.ts          # Environment-specific presets
│   └── index.ts            # Public API
├── tests/
│   ├── schema.test.ts
│   ├── loader.test.ts
│   └── validator.test.ts
├── package.json
├── tsconfig.json
└── README.md
```

**API Design:**
```typescript
// shared/config/src/schema.ts
import { z } from 'zod';

export const EnvironmentModeSchema = z.enum(['dev', 'test', 'production']);
export const LogLevelSchema = z.enum(['debug', 'info', 'warn', 'error']);

export const ConfigSchema = z.object({
  // Environment
  ENVIRONMENT_MODE: EnvironmentModeSchema.default('dev'),

  // Feature Flags
  ENABLE_SUPABASE: z.boolean().default(false),
  ENABLE_PAYMENTS: z.boolean().default(false),

  // Database
  DATABASE_URL: z.string().url(),

  // Logging
  LOG_LEVEL: LogLevelSchema.default('debug'),
  LOG_MAX_SIZE_MB: z.number().int().positive().default(100),
  LOG_ROTATION_DAYS: z.number().int().positive().default(1),
  LOG_RETENTION_DAYS: z.number().int().positive().default(30),
  LOG_DIR: z.string().default('./logs'),

  // API Keys
  GOOGLE_API_KEY: z.string().optional(),
  CLERK_SECRET_KEY: z.string().optional(),
  STRIPE_SECRET_KEY: z.string().optional(),
});

export type AppConfig = z.infer<typeof ConfigSchema>;
```

```typescript
// shared/config/src/loader.ts
import { ConfigSchema, AppConfig } from './schema';

export class ConfigLoader {
  private static instance: AppConfig | null = null;

  static load(): AppConfig {
    if (this.instance) return this.instance;

    const rawConfig = {
      ENVIRONMENT_MODE: process.env.ENVIRONMENT_MODE,
      ENABLE_SUPABASE: process.env.ENABLE_SUPABASE === 'true',
      ENABLE_PAYMENTS: process.env.ENABLE_PAYMENTS === 'true',
      DATABASE_URL: process.env.DATABASE_URL,
      LOG_LEVEL: process.env.LOG_LEVEL,
      LOG_MAX_SIZE_MB: parseInt(process.env.LOG_MAX_SIZE_MB || '100'),
      LOG_ROTATION_DAYS: parseInt(process.env.LOG_ROTATION_DAYS || '1'),
      LOG_RETENTION_DAYS: parseInt(process.env.LOG_RETENTION_DAYS || '30'),
      LOG_DIR: process.env.LOG_DIR || './logs',
      GOOGLE_API_KEY: process.env.GOOGLE_API_KEY,
      CLERK_SECRET_KEY: process.env.CLERK_SECRET_KEY,
      STRIPE_SECRET_KEY: process.env.STRIPE_SECRET_KEY,
    };

    const result = ConfigSchema.safeParse(rawConfig);

    if (!result.success) {
      const errors = result.error.format();
      console.error('Configuration validation failed:', errors);
      throw new Error('Invalid configuration. Check environment variables.');
    }

    this.instance = result.data;
    return this.instance;
  }

  static reset(): void {
    this.instance = null;
  }
}
```

```typescript
// shared/config/src/presets.ts
import { AppConfig } from './schema';

export const DEV_PRESET: Partial<AppConfig> = {
  ENVIRONMENT_MODE: 'dev',
  ENABLE_SUPABASE: false,
  ENABLE_PAYMENTS: false,
  LOG_LEVEL: 'debug',
  DATABASE_URL: 'postgresql://studyabroad:studyabroad_dev@localhost:5432/studyabroad_dev',
};

export const TEST_PRESET: Partial<AppConfig> = {
  ENVIRONMENT_MODE: 'test',
  ENABLE_SUPABASE: true,
  ENABLE_PAYMENTS: false,
  LOG_LEVEL: 'debug',
};

export const PRODUCTION_PRESET: Partial<AppConfig> = {
  ENVIRONMENT_MODE: 'production',
  ENABLE_SUPABASE: true,
  ENABLE_PAYMENTS: true,
  LOG_LEVEL: 'error',
};
```

### 2. Backend Integration (Python)

For the Python backend, create a similar configuration system using Pydantic:

```python
# backend/src/config.py
from pydantic_settings import BaseSettings
from typing import Literal

class Settings(BaseSettings):
    # Environment
    ENVIRONMENT_MODE: Literal['dev', 'test', 'production'] = 'dev'

    # Feature Flags
    ENABLE_SUPABASE: bool = False
    ENABLE_PAYMENTS: bool = False

    # Database
    DATABASE_URL: str

    # Logging
    LOG_LEVEL: Literal['DEBUG', 'INFO', 'WARN', 'ERROR'] = 'DEBUG'
    LOG_MAX_SIZE_MB: int = 100
    LOG_ROTATION_DAYS: int = 1
    LOG_RETENTION_DAYS: int = 30
    LOG_DIR: str = './logs'

    # API Keys
    GOOGLE_API_KEY: str | None = None
    CLERK_SECRET_KEY: str | None = None
    STRIPE_SECRET_KEY: str | None = None

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
```

### 3. Environment File Structure

```
project-root/
├── .env.example              # Template (committed)
├── .env                      # Development (gitignored)
├── .env.test                 # Test environment (gitignored)
├── .env.production           # Production template (gitignored)
├── frontend/
│   ├── .env.local.example    # Frontend template
│   └── .env.local            # Frontend dev (gitignored)
└── backend/
    ├── .env.example          # Backend template
    └── .env                  # Backend dev (gitignored)
```

### 4. Usage Examples

**Frontend (Next.js):**
```typescript
// app/api/config/route.ts
import { ConfigLoader } from '@study-abroad/shared-config';

const config = ConfigLoader.load();

if (config.ENABLE_PAYMENTS) {
  // Initialize Stripe
}

if (config.ENABLE_SUPABASE) {
  // Initialize Supabase client
}
```

**Backend (FastAPI):**
```python
# src/main.py
from config import settings

if settings.ENABLE_PAYMENTS:
    # Initialize Stripe
    pass

if settings.ENABLE_SUPABASE:
    # Initialize Supabase client
    pass
```

## Consequences

### Positive
1. **Type Safety**: Zod/Pydantic provide runtime validation and compile-time types
2. **Fail-Fast**: Application won't start with invalid configuration
3. **DRY Principle**: Single source of truth for configuration schema
4. **Reusability**: `shared/config` package can be used across all projects in monorepo
5. **Developer Experience**: Clear error messages for missing/invalid config
6. **Environment Parity**: Same configuration structure across all environments
7. **Security**: No secrets in code, enforced through validation
8. **Testability**: Easy to mock configuration in tests

### Negative
1. **Additional Dependency**: Introduces Zod as a dependency
2. **Learning Curve**: Developers must understand Zod schemas
3. **Duplication**: Some duplication between TypeScript and Python config systems
4. **Migration Effort**: Existing code must be refactored to use new config system

### Mitigation
- Comprehensive documentation in `shared/config/README.md`
- Example .env.example files with all required variables
- Validation error messages that clearly indicate what's missing
- Migration guide for existing configuration code

## Compliance

### SpeckitGovernance
- **Traceability**: This ADR documents the decision and links to spec requirements (Section 6)
- **Documentation**: `shared/config/README.md` will provide usage guidelines
- **Justification**: Addresses AC-10, AC-11, AC-12 from updated spec

### SecurityBaselineNIST
- **Protect (PR.AC-4)**: Enforces least-privilege by separating environment configurations
- **Protect (PR.DS-1)**: Ensures secrets are not hardcoded (validation fails without env vars)
- **Identify (ID.AM-1)**: Configuration schema documents all required secrets

### RagCitationsIntegrity
- Not directly applicable to configuration system
- Configuration system supports RAG pipeline by providing environment-specific API keys

## References
- Spec: `/Users/vihang/projects/study-abroad/specs/001-mvp-uk-study-migration/spec.md` (Section 6)
- Acceptance Criteria: AC-10, AC-11, AC-12
- Constitution: Section 2 (Security Framework), Section 6 (Prohibited Practices)

## Revision History
- **2025-12-31**: Initial version (Accepted)
