# Migration Guide: Reusing @study-abroad/shared

This guide explains how to migrate the shared package to a new project.

## Overview

The `@study-abroad/shared` package is designed as a portable component library that can be reused across projects. It provides:

- Authentication components (Clerk)
- Payment components (Stripe)
- Database utilities (Supabase)
- Type definitions
- React hooks

## Step 1: Copy the Package

```bash
# Option A: Copy as a local package
cp -r study-abroad/shared your-project/packages/shared

# Option B: Publish to npm (private registry)
cd study-abroad/shared
npm publish --access restricted
```

## Step 2: Update Dependencies

In your new project's `package.json`:

```json
{
  "dependencies": {
    "@your-org/shared": "file:./packages/shared"
  }
}
```

Or if published:

```json
{
  "dependencies": {
    "@your-org/shared": "^0.1.0"
  }
}
```

## Step 3: Configure Environment Variables

Create `.env` in your project root:

```bash
# Authentication - Update with your Clerk project
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=pk_test_YOUR_KEY
CLERK_SECRET_KEY=sk_test_YOUR_KEY

# Payments - Update with your Stripe account
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_test_YOUR_KEY
STRIPE_SECRET_KEY=sk_test_YOUR_KEY
STRIPE_WEBHOOK_SECRET=whsec_YOUR_SECRET

# Database - Update with your Supabase project
NEXT_PUBLIC_SUPABASE_URL=https://YOUR_PROJECT.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=YOUR_ANON_KEY
SUPABASE_SERVICE_ROLE_KEY=YOUR_SERVICE_KEY

# API - Update with your backend URL
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Step 4: Customize Branding

### 4.1 Update Package Name

In `shared/package.json`:

```json
{
  "name": "@your-org/shared",
  "description": "Your project description"
}
```

### 4.2 Update Component Styling

Components use Tailwind CSS classes that can be customized:

```tsx
// shared/src/components/auth/LoginForm.tsx
// Modify className props as needed
<Button className="bg-your-brand-color hover:bg-your-brand-hover">
  Sign In
</Button>
```

### 4.3 Update OAuth Providers

In `shared/src/components/auth/OAuthButtons.tsx`:

```tsx
// Enable/disable providers as needed
const ENABLED_PROVIDERS = ['google', 'apple']; // Remove or add providers
```

## Step 5: Customize Types

Update types to match your domain:

```typescript
// shared/src/types/report.ts
export interface Report {
  id: string;
  user_id: string;
  // Add your custom fields
  your_custom_field: string;
}
```

## Step 6: Database Schema

Ensure your Supabase schema matches the expected tables:

```sql
-- Required tables (see backend/supabase/migrations/)
CREATE TABLE users (...);
CREATE TABLE reports (...);
CREATE TABLE payments (...);
```

Or modify the types to match your existing schema.

## Step 7: Update Imports

Replace import paths in your application:

```typescript
// Before (study-abroad)
import { useAuth } from '@study-abroad/shared/hooks';

// After (your project)
import { useAuth } from '@your-org/shared/hooks';
```

## Step 8: Testing

1. Run the shared package tests:
   ```bash
   cd packages/shared
   npm run test
   ```

2. Verify integration:
   ```bash
   cd your-app
   npm run dev
   ```

## Customization Points

| File | Purpose | Common Changes |
|------|---------|----------------|
| `lib/clerk.ts` | Auth client | Add custom claims |
| `lib/stripe.ts` | Payment client | Change price IDs |
| `lib/supabase.ts` | DB client | Add RLS policies |
| `components/auth/*` | Login UI | Branding, providers |
| `components/payments/*` | Payment UI | Currency, amounts |
| `types/*.ts` | Data models | Add custom fields |

## Removing Features

To remove unused features:

### Remove Payments (if not needed)

1. Delete `shared/src/components/payments/`
2. Delete `shared/src/hooks/usePayment.ts`
3. Remove Stripe from `package.json`
4. Remove exports from `index.ts`

### Remove Authentication (if using different provider)

1. Replace `lib/clerk.ts` with your auth provider
2. Update `useAuth.ts` hook interface
3. Update `components/auth/*` components

## Troubleshooting

### Environment Variables Not Loading

Ensure variables are prefixed correctly:
- Client-side: `NEXT_PUBLIC_*`
- Server-side only: No prefix

### Type Errors After Migration

Run TypeScript check:
```bash
npm run type-check
```

Update imports and ensure all types are exported from `index.ts`.

### Supabase Connection Errors

1. Check `NEXT_PUBLIC_SUPABASE_URL` format
2. Verify RLS policies allow access
3. Check service role key for admin operations

## Support

For issues specific to this package, check:
- `shared/tests/` for usage examples
- TypeScript types for API contracts
- README.md for quick reference
