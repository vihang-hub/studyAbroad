# ADR-0002: Feature Flag Mechanism

## Status
Accepted

## Context

The MVP requires the ability to toggle major system features (Supabase, Payments) based on the runtime environment. This enables:

1. **Local Development**: Developers can work without Supabase or payment integrations
2. **Testing Environments**: Integration tests can run with Supabase but without payments
3. **Gradual Rollout**: Production can enable features incrementally
4. **Cost Control**: Avoid unnecessary API calls in non-production environments

### Feature Flags Required (from Spec Section 10, 6)
- `ENABLE_SUPABASE`: Controls database backend (local PostgreSQL vs Supabase)
- `ENABLE_PAYMENTS`: Controls payment flow (bypass in dev/test, enforce in production)

### Requirements
- **Environment-based**: Flags controlled via environment variables
- **Type-safe**: Compile-time and runtime validation
- **Performance**: Zero overhead when flag is disabled
- **Testability**: Easy to override flags in tests
- **Auditability**: Log when flags change behavior

### Constraints
- No third-party feature flag services (LaunchDarkly, Split.io) - must be environment-based
- Must work identically in frontend (Next.js) and backend (FastAPI)
- Must support future flags without code changes

## Decision

We will implement a **simple environment-variable-based feature flag system** integrated with the configuration package (ADR-0001).

### 1. Shared Feature Flag Package (`shared/feature-flags`)

Extend the `shared/config` package with feature flag evaluation logic.

**Package Structure:**
```
shared/feature-flags/
├── src/
│   ├── flags.ts            # Flag definitions and types
│   ├── evaluator.ts        # Flag evaluation logic
│   ├── guards.ts           # Type guards and runtime checks
│   └── index.ts            # Public API
├── tests/
│   ├── flags.test.ts
│   ├── evaluator.test.ts
│   └── guards.test.ts
├── package.json
└── README.md
```

**API Design:**

```typescript
// shared/feature-flags/src/flags.ts
import { z } from 'zod';

export const FeatureFlagSchema = z.object({
  ENABLE_SUPABASE: z.boolean().default(false),
  ENABLE_PAYMENTS: z.boolean().default(false),
});

export type FeatureFlags = z.infer<typeof FeatureFlagSchema>;

export enum Feature {
  SUPABASE = 'ENABLE_SUPABASE',
  PAYMENTS = 'ENABLE_PAYMENTS',
}
```

```typescript
// shared/feature-flags/src/evaluator.ts
import { ConfigLoader } from '@study-abroad/shared-config';
import { Feature, FeatureFlags } from './flags';

export class FeatureFlagEvaluator {
  private config: FeatureFlags;

  constructor() {
    const appConfig = ConfigLoader.load();
    this.config = {
      ENABLE_SUPABASE: appConfig.ENABLE_SUPABASE,
      ENABLE_PAYMENTS: appConfig.ENABLE_PAYMENTS,
    };
  }

  /**
   * Check if a feature is enabled
   * @param feature - Feature to check
   * @returns true if enabled, false otherwise
   */
  isEnabled(feature: Feature): boolean {
    return this.config[feature] === true;
  }

  /**
   * Get all feature flags and their states
   * @returns Object with all feature flags
   */
  getAllFlags(): FeatureFlags {
    return { ...this.config };
  }

  /**
   * Require a feature to be enabled, throw if not
   * @param feature - Feature to require
   * @throws Error if feature is not enabled
   */
  requireEnabled(feature: Feature): void {
    if (!this.isEnabled(feature)) {
      throw new Error(
        `Feature ${feature} is required but not enabled. ` +
        `Set ${feature}=true in environment variables.`
      );
    }
  }
}

// Singleton instance
export const featureFlags = new FeatureFlagEvaluator();
```

```typescript
// shared/feature-flags/src/guards.ts
import { featureFlags, Feature } from './';

/**
 * Decorator to guard functions that require a feature
 * @param feature - Feature required to execute function
 */
export function requireFeature(feature: Feature) {
  return function (
    target: any,
    propertyKey: string,
    descriptor: PropertyDescriptor
  ) {
    const originalMethod = descriptor.value;

    descriptor.value = function (...args: any[]) {
      featureFlags.requireEnabled(feature);
      return originalMethod.apply(this, args);
    };

    return descriptor;
  };
}

/**
 * HOC to guard React components that require a feature
 * @param feature - Feature required to render component
 * @param fallback - Component to render if feature disabled
 */
export function withFeatureFlag<P>(
  feature: Feature,
  fallback: React.ComponentType<P> | null = null
) {
  return function (Component: React.ComponentType<P>) {
    return function GuardedComponent(props: P) {
      if (!featureFlags.isEnabled(feature)) {
        return fallback ? React.createElement(fallback, props) : null;
      }
      return React.createElement(Component, props);
    };
  };
}
```

### 2. Backend Integration (Python)

```python
# backend/src/feature_flags.py
from enum import Enum
from config import settings

class Feature(str, Enum):
    SUPABASE = "ENABLE_SUPABASE"
    PAYMENTS = "ENABLE_PAYMENTS"

class FeatureFlagEvaluator:
    def is_enabled(self, feature: Feature) -> bool:
        """Check if a feature is enabled."""
        return getattr(settings, feature.value, False)

    def require_enabled(self, feature: Feature) -> None:
        """Require a feature to be enabled, raise if not."""
        if not self.is_enabled(feature):
            raise ValueError(
                f"Feature {feature.value} is required but not enabled. "
                f"Set {feature.value}=true in environment variables."
            )

    def get_all_flags(self) -> dict[str, bool]:
        """Get all feature flags and their states."""
        return {
            Feature.SUPABASE.value: self.is_enabled(Feature.SUPABASE),
            Feature.PAYMENTS.value: self.is_enabled(Feature.PAYMENTS),
        }

# Singleton instance
feature_flags = FeatureFlagEvaluator()
```

### 3. Usage Patterns

#### Frontend (Next.js)

**Conditional Component Rendering:**
```typescript
// app/checkout/page.tsx
import { featureFlags, Feature } from '@study-abroad/shared-feature-flags';

export default function CheckoutPage() {
  if (!featureFlags.isEnabled(Feature.PAYMENTS)) {
    return <div>Payments disabled in this environment</div>;
  }

  return <StripeCheckout />;
}
```

**With HOC:**
```typescript
// components/PaymentButton.tsx
import { withFeatureFlag, Feature } from '@study-abroad/shared-feature-flags';

function PaymentButton() {
  return <button>Pay Now</button>;
}

function PaymentDisabledFallback() {
  return <button disabled>Payments Disabled</button>;
}

export default withFeatureFlag(
  Feature.PAYMENTS,
  PaymentDisabledFallback
)(PaymentButton);
```

**API Route Guard:**
```typescript
// app/api/payment/route.ts
import { featureFlags, Feature } from '@study-abroad/shared-feature-flags';

export async function POST(req: Request) {
  featureFlags.requireEnabled(Feature.PAYMENTS);

  // Payment logic here
}
```

#### Backend (FastAPI)

**Route Guard:**
```python
# src/api/routes/payment.py
from fastapi import APIRouter, HTTPException
from feature_flags import feature_flags, Feature

router = APIRouter()

@router.post("/payment")
async def create_payment():
    if not feature_flags.is_enabled(Feature.PAYMENTS):
        raise HTTPException(
            status_code=503,
            detail="Payments are disabled in this environment"
        )

    # Payment logic here
```

**Dependency Injection:**
```python
# src/api/dependencies.py
from fastapi import Depends, HTTPException
from feature_flags import feature_flags, Feature

def require_payments():
    """FastAPI dependency that requires payments to be enabled."""
    if not feature_flags.is_enabled(Feature.PAYMENTS):
        raise HTTPException(
            status_code=503,
            detail="Payments are disabled in this environment"
        )

# Usage
@router.post("/payment", dependencies=[Depends(require_payments)])
async def create_payment():
    # Payment logic here
    pass
```

**Service Layer:**
```python
# src/api/services/database_service.py
from feature_flags import feature_flags, Feature

class DatabaseService:
    def __init__(self):
        if feature_flags.is_enabled(Feature.SUPABASE):
            self.client = get_supabase_client()
        else:
            self.client = get_local_postgres_client()
```

### 4. Logging and Auditability

All feature flag evaluations should be logged (using logging infrastructure from ADR-0004):

```typescript
// shared/feature-flags/src/evaluator.ts
import { logger } from '@study-abroad/shared-logging';

export class FeatureFlagEvaluator {
  isEnabled(feature: Feature): boolean {
    const enabled = this.config[feature] === true;

    logger.debug('Feature flag evaluated', {
      feature,
      enabled,
      environment: process.env.ENVIRONMENT_MODE,
    });

    return enabled;
  }
}
```

```python
# backend/src/feature_flags.py
import structlog

logger = structlog.get_logger()

class FeatureFlagEvaluator:
    def is_enabled(self, feature: Feature) -> bool:
        enabled = getattr(settings, feature.value, False)

        logger.debug(
            "feature_flag_evaluated",
            feature=feature.value,
            enabled=enabled,
            environment=settings.ENVIRONMENT_MODE,
        )

        return enabled
```

### 5. Testing

**Test Utilities:**
```typescript
// shared/feature-flags/tests/utils.ts
export class FeatureFlagTestHelper {
  private originalEnv: NodeJS.ProcessEnv;

  beforeEach() {
    this.originalEnv = { ...process.env };
  }

  afterEach() {
    process.env = this.originalEnv;
    ConfigLoader.reset(); // From ADR-0001
  }

  setFlag(feature: Feature, enabled: boolean) {
    process.env[feature] = enabled.toString();
    ConfigLoader.reset();
  }
}
```

**Example Test:**
```typescript
// tests/payment.test.ts
import { FeatureFlagTestHelper } from '@study-abroad/shared-feature-flags/tests';
import { Feature } from '@study-abroad/shared-feature-flags';

describe('Payment Flow', () => {
  const helper = new FeatureFlagTestHelper();

  beforeEach(() => helper.beforeEach());
  afterEach(() => helper.afterEach());

  it('should bypass payment when flag is disabled', () => {
    helper.setFlag(Feature.PAYMENTS, false);

    // Test that payment is bypassed
  });

  it('should enforce payment when flag is enabled', () => {
    helper.setFlag(Feature.PAYMENTS, true);

    // Test that payment is enforced
  });
});
```

## Consequences

### Positive
1. **Simplicity**: No external dependencies, just environment variables
2. **Zero Cost**: No API calls to feature flag services
3. **Type Safety**: TypeScript enums prevent typos
4. **Consistency**: Same API across frontend and backend
5. **Testability**: Easy to mock flags in tests
6. **Auditability**: All flag evaluations are logged
7. **Performance**: Zero runtime overhead (static evaluation)
8. **Reusability**: Package works across all monorepo projects

### Negative
1. **No Dynamic Updates**: Requires application restart to change flags
2. **No Gradual Rollout**: Cannot enable for percentage of users
3. **No User Targeting**: All users in an environment see same flags
4. **Limited Observability**: No dashboard for flag states

### Trade-offs Accepted
For MVP, the simplicity of environment-based flags outweighs the lack of dynamic updates. Future iterations can introduce sophisticated feature flag services if needed.

### Mitigation
- Document clearly that flag changes require redeployment
- Consider adding `/api/feature-flags` endpoint to expose current flag states
- Plan for migration to LaunchDarkly/Split.io if dynamic flags become necessary

## Compliance

### SpeckitGovernance
- **Traceability**: Links to spec Section 6 (Environment Configuration) and Section 10 (Pricing & Payments)
- **Documentation**: `shared/feature-flags/README.md` provides usage guidelines
- **Justification**: Addresses AC-10, AC-11, AC-12, AC-13

### SecurityBaselineNIST
- **Protect (PR.AC-4)**: Flags enforce environment-appropriate security (e.g., no payments in dev)
- **Detect (DE.AE-3)**: All flag evaluations are logged for audit trail
- **Respond (RS.AN-1)**: Logs enable analysis of feature usage patterns

### RagCitationsIntegrity
- Not directly applicable to feature flags
- Feature flags support RAG pipeline by controlling which services are active

## References
- ADR-0001: Environment Configuration System (config package dependency)
- ADR-0004: Logging Infrastructure (logging dependency)
- Spec: Section 6 (Environment Configuration), Section 10 (Pricing & Payments)
- Acceptance Criteria: AC-10, AC-11, AC-12, AC-13
- Constitution: Section 6 (Prohibited Practices - no assumptions)

## Revision History
- **2025-12-31**: Initial version (Accepted)
