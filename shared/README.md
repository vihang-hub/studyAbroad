# @study-abroad/shared

Reusable component library for the Study Abroad application. This package provides portable TypeScript utilities, React components, and hooks for authentication, payments, and database operations.

## Installation

```bash
# From the monorepo root
npm install

# Or add as a dependency in another project
npm install @study-abroad/shared
```

## Package Structure

```
shared/
├── src/
│   ├── types/           # TypeScript interfaces and types
│   │   ├── user.ts      # User, AuthProvider types
│   │   ├── report.ts    # Report, ReportContent, Citation
│   │   ├── payment.ts   # Payment, PaymentStatus
│   │   └── api.ts       # API request/response types
│   │
│   ├── lib/             # Core utilities
│   │   ├── clerk.ts     # Clerk authentication client
│   │   ├── stripe.ts    # Stripe payment client
│   │   ├── supabase.ts  # Supabase database client
│   │   └── api-client.ts # Generic typed fetch wrapper
│   │
│   ├── hooks/           # React hooks
│   │   ├── useAuth.ts   # Authentication state hook
│   │   └── useSupabase.ts # Database query hooks
│   │
│   ├── components/      # React components
│   │   ├── auth/        # Authentication UI
│   │   └── payments/    # Payment UI
│   │
│   └── index.ts         # Public exports
│
├── tests/               # Unit tests (Vitest)
├── package.json
└── tsconfig.json
```

## Quick Start

### 1. Environment Configuration

Create a `.env` file with required variables:

```bash
# Authentication (Clerk)
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=pk_test_...
CLERK_SECRET_KEY=sk_test_...

# Payments (Stripe)
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...

# Database (Supabase)
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJ...
SUPABASE_SERVICE_ROLE_KEY=eyJ...

# API
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### 2. Import Components

```typescript
// Types
import { User, Report, Payment } from '@study-abroad/shared/types';

// Hooks
import { useAuth, useSupabase } from '@study-abroad/shared/hooks';

// Components
import { LoginForm, SignupForm } from '@study-abroad/shared/components/auth';
import { CheckoutButton } from '@study-abroad/shared/components/payments';

// Utilities
import { supabaseClient, stripeClient } from '@study-abroad/shared/lib';
```

### 3. Authentication Example

```tsx
import { useAuth } from '@study-abroad/shared/hooks';
import { LoginForm } from '@study-abroad/shared/components/auth';

function AuthPage() {
  const { user, isLoaded, isSignedIn } = useAuth();

  if (!isLoaded) return <div>Loading...</div>;
  if (isSignedIn) return <div>Welcome, {user?.email}</div>;

  return <LoginForm />;
}
```

### 4. Payment Example

```tsx
import { CheckoutButton } from '@study-abroad/shared/components/payments';
import { usePayment } from '@study-abroad/shared/hooks';

function PaymentPage() {
  const { createCheckout, isLoading } = usePayment();

  const handlePay = async () => {
    await createCheckout({
      priceId: 'price_299_gbp',
      successUrl: '/success',
      cancelUrl: '/cancel',
    });
  };

  return (
    <CheckoutButton
      onClick={handlePay}
      loading={isLoading}
      amount={299}
      currency="GBP"
    />
  );
}
```

## API Reference

### Types

| Type | Description |
|------|-------------|
| `User` | User profile with auth provider info |
| `Report` | Generated research report |
| `ReportContent` | Structured report sections |
| `Citation` | Source citation |
| `Payment` | Payment record |
| `PaymentStatus` | Payment state enum |

### Hooks

| Hook | Description |
|------|-------------|
| `useAuth()` | Current user, login/logout methods |
| `useSupabase()` | Database query utilities |
| `usePayment()` | Payment flow management |

### Components

| Component | Description |
|-----------|-------------|
| `LoginForm` | Combined OAuth + email login |
| `SignupForm` | Combined OAuth + email signup |
| `OAuthButtons` | Google/Apple/Facebook buttons |
| `EmailAuthForm` | Email/password form |
| `CheckoutButton` | Stripe checkout trigger |
| `PaymentStatus` | Payment state display |

## Configuration

All clients are configurable via environment variables:

| Variable | Required | Description |
|----------|----------|-------------|
| `NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY` | Yes | Clerk public key |
| `NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY` | Yes | Stripe public key |
| `NEXT_PUBLIC_SUPABASE_URL` | Yes | Supabase project URL |
| `NEXT_PUBLIC_SUPABASE_ANON_KEY` | Yes | Supabase anonymous key |
| `NEXT_PUBLIC_API_URL` | Yes | Backend API URL |

## Testing

```bash
# Run tests
npm run test

# Run with coverage
npm run test:coverage

# Run mutation tests
npm run test:mutation
```

## Quality Gates

- Code coverage: >= 90%
- Mutation score: > 80%
- ESLint: Airbnb style guide
- TypeScript: Strict mode

## License

Private - Study Abroad Application
