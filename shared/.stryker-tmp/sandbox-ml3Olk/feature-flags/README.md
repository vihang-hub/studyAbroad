# @study-abroad/shared-feature-flags

Feature flag evaluation with React hooks for environment-based feature toggles.

## Overview

This package provides type-safe feature flag evaluation integrated with `@study-abroad/shared-config`. It enables environment-based feature toggles for the Study Abroad monorepo, supporting development, test, and production modes with different feature enablement.

## Features

- Type-safe feature flag enum (prevents typos)
- Singleton evaluator for consistent flag state
- React hooks for easy component integration
- Feature-gated component rendering
- Environment mode detection
- Zero configuration (integrates with shared-config)
- Comprehensive test coverage (99%)
- High mutation test score (88%)

## Installation

```bash
npm install @study-abroad/shared-feature-flags
```

## Available Feature Flags

| Flag | Purpose | Default |
|------|---------|---------|
| `ENABLE_SUPABASE` | Use Supabase backend vs local PostgreSQL | `false` |
| `ENABLE_PAYMENTS` | Enable Stripe payment processing | `false` |
| `ENABLE_RATE_LIMITING` | Enable request rate limiting | `true` |
| `ENABLE_OBSERVABILITY` | Enable monitoring/observability features | `false` |

## Usage

### Basic Feature Flag Evaluation

```typescript
import { FeatureFlags, Feature } from '@study-abroad/shared-feature-flags';

// Check if a feature is enabled
if (FeatureFlags.isEnabled(Feature.PAYMENTS)) {
  await processPayment();
} else {
  console.log('Payments disabled, bypassing payment flow');
}

// Get current environment mode
const mode = FeatureFlags.getEnvironmentMode();
console.log(`Running in ${mode} mode`); // 'dev' | 'test' | 'production'

// Get all feature flags
const flags = FeatureFlags.getAllFlags();
console.log(flags);
// {
//   ENABLE_SUPABASE: false,
//   ENABLE_PAYMENTS: false,
//   ENABLE_RATE_LIMITING: true,
//   ENABLE_OBSERVABILITY: false
// }

// Require a feature (throws if not enabled)
FeatureFlags.requireEnabled(Feature.PAYMENTS);
// Throws: "Feature ENABLE_PAYMENTS is required but not enabled in dev environment..."
```

### React Hooks

```typescript
import { useFeatureFlag, useEnvironmentMode, useAllFeatureFlags } from '@study-abroad/shared-feature-flags';
import { Feature } from '@study-abroad/shared-feature-flags';

function PaymentSection() {
  const paymentsEnabled = useFeatureFlag(Feature.PAYMENTS);
  const mode = useEnvironmentMode();

  if (!paymentsEnabled) {
    return <div>Payments disabled ({mode} mode)</div>;
  }

  return <StripeCheckout />;
}

function FeatureDebugger() {
  const flags = useAllFeatureFlags();

  return (
    <ul>
      {Object.entries(flags).map(([flag, enabled]) => (
        <li key={flag}>
          {flag}: {enabled ? 'ON' : 'OFF'}
        </li>
      ))}
    </ul>
  );
}
```

### FeatureGate Component

```typescript
import { FeatureGate, Feature } from '@study-abroad/shared-feature-flags';

// Render only when feature is enabled
function App() {
  return (
    <div>
      <h1>Study Abroad App</h1>

      <FeatureGate feature={Feature.PAYMENTS}>
        <StripeCheckout />
      </FeatureGate>

      {/* With fallback */}
      <FeatureGate
        feature={Feature.PAYMENTS}
        fallback={<div>Payments disabled in this environment</div>}
      >
        <StripeCheckout />
      </FeatureGate>

      {/* Render only when feature is disabled */}
      <FeatureGate feature={Feature.PAYMENTS} enabled={false}>
        <div>Free access (payments disabled)</div>
      </FeatureGate>
    </div>
  );
}
```

### API Route Guards (Next.js)

```typescript
import { FeatureFlags, Feature } from '@study-abroad/shared-feature-flags';
import { NextResponse } from 'next/server';

export async function POST(req: Request) {
  // Require payment feature to be enabled
  try {
    FeatureFlags.requireEnabled(Feature.PAYMENTS);
  } catch (error) {
    return NextResponse.json(
      { error: 'Payments are disabled in this environment' },
      { status: 503 }
    );
  }

  // Payment logic here
  const payment = await createPayment();
  return NextResponse.json(payment);
}
```

## API Reference

### `FeatureFlags` Class

#### Static Methods

**`isEnabled(feature: Feature): boolean`**
- Check if a feature flag is enabled
- Returns: `true` if enabled, `false` otherwise

**`getEnvironmentMode(): EnvironmentMode`**
- Get current environment mode
- Returns: `'dev' | 'test' | 'production'`

**`getAllFlags(): FeatureFlagState`**
- Get all feature flags and their states
- Returns: Object mapping each `Feature` to its boolean state

**`requireEnabled(feature: Feature): void`**
- Require a feature to be enabled, throw if not
- Throws: `Error` with helpful message if feature is disabled

**`reset(): void`** (internal)
- Reset singleton instance (for testing only)

### React Hooks

**`useFeatureFlag(feature: Feature): boolean`**
- React hook for feature flag evaluation
- Returns: `true` if feature is enabled
- Memoized for performance

**`useEnvironmentMode(): EnvironmentMode`**
- React hook for environment mode
- Returns: Current environment mode
- Memoized for performance

**`useAllFeatureFlags(): FeatureFlagState`**
- React hook to get all feature flags
- Returns: Object with all feature flags and their states
- Memoized for performance

### Components

**`<FeatureGate>`**

Props:
- `feature: Feature` - Feature flag to check (required)
- `enabled?: boolean` - Expected state (default: `true`)
- `fallback?: React.ReactNode` - Content to render when feature doesn't match expected state
- `children: React.ReactNode` - Content to render when feature matches expected state (required)

## Environment Configuration

Feature flags are automatically loaded from environment variables via `@study-abroad/shared-config`:

```bash
# Development (.env.local)
ENVIRONMENT_MODE=dev
ENABLE_SUPABASE=false
ENABLE_PAYMENTS=false
ENABLE_RATE_LIMITING=true
ENABLE_OBSERVABILITY=false

# Test (.env.test)
ENVIRONMENT_MODE=test
ENABLE_SUPABASE=true
SUPABASE_URL=https://test.supabase.co
SUPABASE_ANON_KEY=test_key
ENABLE_PAYMENTS=false
ENABLE_RATE_LIMITING=true
ENABLE_OBSERVABILITY=false

# Production (.env.production)
ENVIRONMENT_MODE=production
ENABLE_SUPABASE=true
ENABLE_PAYMENTS=true
ENABLE_RATE_LIMITING=true
ENABLE_OBSERVABILITY=true
```

## Testing

The package includes comprehensive tests:

```bash
# Run unit tests
npm test

# Run tests with coverage (99% coverage)
npm run test:coverage

# Run mutation tests (88% mutation score)
npm run test:mutation
```

## Architecture Decisions

See [ADR-0002: Feature Flag Mechanism](../../docs/adr/ADR-0002-feature-flag-mechanism.md) for the full architectural decision record.

**Key Decisions:**
- **Environment-based**: Flags controlled via environment variables (no external service)
- **Simple design**: No percentage rollouts or user targeting (not needed for MVP)
- **Type-safe**: TypeScript enum prevents typos and provides autocomplete
- **Zero cost**: No API calls or external dependencies

**Trade-offs:**
- Flags require app restart to change (acceptable for MVP)
- No dynamic updates (can migrate to LaunchDarkly/Split.io later if needed)
- No per-user targeting (all users in an environment see same flags)

## Dependencies

- `@study-abroad/shared-config`: Environment configuration and validation
- `react`: React library (peer dependency for hooks/components)

## License

MIT
