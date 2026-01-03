/**
 * @study-abroad/shared
 * Portable, reusable components for plug-and-play across projects
 *
 * Exports:
 * - Types (User, Report, Payment, API contracts)
 * - Lib (Clerk, Stripe, Supabase clients)
 * - Hooks (useAuth, useSupabase)
 * - Components (LoginForm, SignupForm, CheckoutButton, etc.)
 */

// Types
export * from './types/user';
export * from './types/report';
export * from './types/payment';
export * from './types/api';

// Lib (Portable client initialization)
export * from './lib/clerk';
export * from './lib/stripe';
export * from './lib/supabase';
export * from './lib/api-client';

// Hooks
export * from './hooks/useAuth';
export * from './hooks/useSupabase';
export * from './hooks/usePayment';

// Components - Authentication
export * from './components/auth';

// Components - Payments
export * from './components/payments';

export const SHARED_VERSION = '0.1.0';
