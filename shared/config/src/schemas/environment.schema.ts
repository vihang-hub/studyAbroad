/**
 * Environment Configuration Schema
 *
 * Validates all environment variables required for the application.
 * Uses Zod for compile-time type safety and runtime validation.
 *
 * @module shared/config/schemas/environment
 */

import { z } from 'zod';

/**
 * Environment Mode Enum
 */
export const EnvironmentMode = z.enum(['dev', 'test', 'production']);
export type EnvironmentMode = z.infer<typeof EnvironmentMode>;

/**
 * Log Level Enum
 */
export const LogLevel = z.enum(['debug', 'info', 'warn', 'error']);
export type LogLevel = z.infer<typeof LogLevel>;

/**
 * Auth Provider Enum
 */
export const AuthProvider = z.enum(['google', 'apple', 'facebook', 'email']);
export type AuthProvider = z.infer<typeof AuthProvider>;

/**
 * Payment Status Enum
 */
export const PaymentStatus = z.enum([
  'requires_payment_method',
  'requires_confirmation',
  'processing',
  'succeeded',
  'failed',
  'canceled',
  'bypassed',
]);
export type PaymentStatus = z.infer<typeof PaymentStatus>;

/**
 * Report Status Enum
 */
export const ReportStatus = z.enum(['generating', 'completed', 'failed']);
export type ReportStatus = z.infer<typeof ReportStatus>;

/**
 * Database Configuration Schema
 */
const DatabaseConfigSchema = z.object({
  /** Database connection URL */
  DATABASE_URL: z.string().url().describe('PostgreSQL or Supabase connection URL'),

  /** Supabase URL (required when ENABLE_SUPABASE=true) */
  SUPABASE_URL: z.string().url().optional().describe('Supabase project URL'),

  /** Supabase Anonymous Key (required when ENABLE_SUPABASE=true) */
  SUPABASE_ANON_KEY: z.string().optional().describe('Supabase anonymous/public key'),

  /** Supabase Service Role Key (backend only, bypasses RLS) */
  SUPABASE_SERVICE_ROLE_KEY: z.string().optional().describe('Supabase service role key (backend only)'),

  /** Maximum database connection pool size */
  DATABASE_POOL_MAX: z.coerce.number().int().min(1).max(100).default(20),

  /** Database connection idle timeout (milliseconds) */
  DATABASE_IDLE_TIMEOUT_MS: z.coerce.number().int().min(1000).default(30000),

  /** Database connection timeout (milliseconds) */
  DATABASE_CONNECTION_TIMEOUT_MS: z.coerce.number().int().min(500).default(2000),
});

/**
 * Logging Configuration Schema
 */
const LoggingConfigSchema = z.object({
  /** Logging level */
  LOG_LEVEL: LogLevel.default('debug'),

  /** Directory for log files */
  LOG_DIR: z.string().default('./logs'),

  /** Maximum log file size before rotation (MB) */
  LOG_MAX_SIZE_MB: z.coerce.number().int().min(1).max(1000).default(100),

  /** Log rotation interval (days) */
  LOG_ROTATION_DAYS: z.coerce.number().int().min(1).max(365).default(1),

  /** Log retention period (days) */
  LOG_RETENTION_DAYS: z.coerce.number().int().min(1).max(365).default(30),

  /** Enable console logging (in addition to file) */
  LOG_CONSOLE_ENABLED: z.coerce.boolean().default(true),

  /** Enable pretty printing for console logs (dev only) */
  LOG_PRETTY_PRINT: z.coerce.boolean().default(false),
});

/**
 * Feature Flags Configuration Schema
 */
const FeatureFlagsConfigSchema = z.object({
  /** Enable Supabase database backend */
  ENABLE_SUPABASE: z.coerce.boolean().default(false),

  /** Enable payment processing via Stripe */
  ENABLE_PAYMENTS: z.coerce.boolean().default(false),

  /** Enable rate limiting */
  ENABLE_RATE_LIMITING: z.coerce.boolean().default(true),

  /** Enable observability/monitoring */
  ENABLE_OBSERVABILITY: z.coerce.boolean().default(false),
});

/**
 * Clerk Authentication Configuration Schema
 */
const ClerkConfigSchema = z.object({
  /** Clerk publishable key (frontend) */
  NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY: z.string().min(1).describe('Clerk publishable key'),

  /** Clerk secret key (backend) */
  CLERK_SECRET_KEY: z.string().min(1).describe('Clerk secret key'),

  /** Clerk webhook secret for signature verification */
  CLERK_WEBHOOK_SECRET: z.string().optional().describe('Clerk webhook secret'),

  /** Sign-in URL */
  NEXT_PUBLIC_CLERK_SIGN_IN_URL: z.string().default('/sign-in'),

  /** Sign-up URL */
  NEXT_PUBLIC_CLERK_SIGN_UP_URL: z.string().default('/sign-up'),

  /** After sign-in redirect URL */
  NEXT_PUBLIC_CLERK_AFTER_SIGN_IN_URL: z.string().default('/chat'),

  /** After sign-up redirect URL */
  NEXT_PUBLIC_CLERK_AFTER_SIGN_UP_URL: z.string().default('/chat'),
});

/**
 * Stripe Payment Configuration Schema
 */
const StripeConfigSchema = z.object({
  /** Stripe publishable key (frontend) */
  NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY: z.string().optional().describe('Stripe publishable key'),

  /** Stripe secret key (backend) */
  STRIPE_SECRET_KEY: z.string().optional().describe('Stripe secret key'),

  /** Stripe webhook secret for signature verification */
  STRIPE_WEBHOOK_SECRET: z.string().optional().describe('Stripe webhook secret'),

  /** Stripe price ID for report purchase */
  STRIPE_PRICE_ID: z.string().optional().describe('Stripe price ID for £2.99 report'),

  /** Payment amount in GBP (2.99) */
  PAYMENT_AMOUNT: z.coerce.number().min(2.99).max(2.99).default(2.99),

  /** Payment currency */
  PAYMENT_CURRENCY: z.enum(['GBP']).default('GBP'),
});

/**
 * Gemini AI Configuration Schema
 */
const GeminiConfigSchema = z.object({
  /** Google AI API key */
  GEMINI_API_KEY: z.string().min(1).describe('Google Gemini API key'),

  /** Gemini model to use */
  GEMINI_MODEL: z.string().default('gemini-1.5-pro'),

  /** Maximum tokens for generation */
  GEMINI_MAX_TOKENS: z.coerce.number().int().min(1000).default(8192),

  /** Temperature for generation (0-1) */
  GEMINI_TEMPERATURE: z.coerce.number().min(0).max(1).default(0.7),

  /** Request timeout (milliseconds) */
  GEMINI_TIMEOUT_MS: z.coerce.number().int().min(5000).default(60000),
});

/**
 * Application Configuration Schema
 */
const AppConfigSchema = z.object({
  /** Application name */
  APP_NAME: z.string().default('Study Abroad MVP'),

  /** Application version */
  APP_VERSION: z.string().default('1.0.0'),

  /** Frontend URL */
  NEXT_PUBLIC_APP_URL: z.string().url().default('http://localhost:3000'),

  /** Backend API URL */
  NEXT_PUBLIC_API_URL: z.string().url().default('http://localhost:8000'),

  /** Backend API URL (server-side) */
  API_URL: z.string().url().default('http://localhost:8000'),

  /** Port for backend server */
  PORT: z.coerce.number().int().min(1).max(65535).default(8000),

  /** Node environment */
  NODE_ENV: z.enum(['development', 'test', 'production']).default('development'),
});

/**
 * Rate Limiting Configuration Schema
 */
const RateLimitConfigSchema = z.object({
  /** Maximum requests per window */
  RATE_LIMIT_MAX: z.coerce.number().int().min(1).default(100),

  /** Rate limit window (seconds) */
  RATE_LIMIT_WINDOW_SEC: z.coerce.number().int().min(1).default(60),

  /** Report generation rate limit (per user per day) */
  RATE_LIMIT_REPORTS_PER_DAY: z.coerce.number().int().min(1).default(10),
});

/**
 * Full Environment Configuration Schema
 *
 * Combines all configuration sections with validation rules.
 */
export const EnvironmentConfigSchema = DatabaseConfigSchema.merge(LoggingConfigSchema)
  .merge(FeatureFlagsConfigSchema)
  .merge(ClerkConfigSchema)
  .merge(StripeConfigSchema)
  .merge(GeminiConfigSchema)
  .merge(AppConfigSchema)
  .merge(RateLimitConfigSchema)
  .extend({
    /** Environment mode */
    ENVIRONMENT_MODE: EnvironmentMode.default('dev'),
  })
  .transform((config) => {
    // Apply environment-specific defaults for LOG_LEVEL if not explicitly set
    if (!process.env.LOG_LEVEL) {
      if (config.ENVIRONMENT_MODE === 'production') {
        return { ...config, LOG_LEVEL: 'error' as const };
      }
      // dev and test both use debug
      return { ...config, LOG_LEVEL: 'debug' as const };
    }
    return config;
  })
  .refine(
    (config) => {
      // If ENABLE_SUPABASE is true, require Supabase config
      if (config.ENABLE_SUPABASE) {
        return !!(config.SUPABASE_URL && config.SUPABASE_ANON_KEY);
      }
      return true;
    },
    {
      message: 'SUPABASE_URL and SUPABASE_ANON_KEY are required when ENABLE_SUPABASE=true',
      path: ['ENABLE_SUPABASE'],
    }
  )
  .refine(
    (config) => {
      // If ENABLE_PAYMENTS is true, require Stripe config
      if (config.ENABLE_PAYMENTS) {
        return !!(
          config.NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY &&
          config.STRIPE_SECRET_KEY &&
          config.STRIPE_WEBHOOK_SECRET
        );
      }
      return true;
    },
    {
      message:
        'NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY, STRIPE_SECRET_KEY, and STRIPE_WEBHOOK_SECRET are required when ENABLE_PAYMENTS=true',
      path: ['ENABLE_PAYMENTS'],
    }
  )
  .refine(
    (config) => {
      // Production mode must have ENABLE_SUPABASE and ENABLE_PAYMENTS
      if (config.ENVIRONMENT_MODE === 'production') {
        return config.ENABLE_SUPABASE === true && config.ENABLE_PAYMENTS === true;
      }
      return true;
    },
    {
      message: 'Production mode requires ENABLE_SUPABASE=true and ENABLE_PAYMENTS=true',
      path: ['ENVIRONMENT_MODE'],
    }
  )
  .refine(
    (config) => {
      // Dev mode must disable Supabase and payments
      if (config.ENVIRONMENT_MODE === 'dev') {
        return config.ENABLE_SUPABASE === false && config.ENABLE_PAYMENTS === false;
      }
      return true;
    },
    {
      message: 'Dev mode requires ENABLE_SUPABASE=false and ENABLE_PAYMENTS=false',
      path: ['ENVIRONMENT_MODE'],
    }
  )
  .refine(
    (config) => {
      // Test mode must enable Supabase but disable payments
      if (config.ENVIRONMENT_MODE === 'test') {
        return config.ENABLE_SUPABASE === true && config.ENABLE_PAYMENTS === false;
      }
      return true;
    },
    {
      message: 'Test mode requires ENABLE_SUPABASE=true and ENABLE_PAYMENTS=false',
      path: ['ENVIRONMENT_MODE'],
    }
  );

/**
 * Inferred TypeScript type for environment configuration
 */
export type EnvironmentConfig = z.infer<typeof EnvironmentConfigSchema>;

/**
 * Environment Preset Configurations
 */
export const EnvironmentPresets: Record<EnvironmentMode, Partial<EnvironmentConfig>> = {
  dev: {
    ENVIRONMENT_MODE: 'dev',
    ENABLE_SUPABASE: false,
    ENABLE_PAYMENTS: false,
    LOG_LEVEL: 'debug',
    LOG_PRETTY_PRINT: true,
    DATABASE_URL: 'postgresql://studyabroad:pass@localhost:5432/studyabroad_dev',
  },
  test: {
    ENVIRONMENT_MODE: 'test',
    ENABLE_SUPABASE: true,
    ENABLE_PAYMENTS: false,
    LOG_LEVEL: 'debug',
    LOG_PRETTY_PRINT: false,
  },
  production: {
    ENVIRONMENT_MODE: 'production',
    ENABLE_SUPABASE: true,
    ENABLE_PAYMENTS: true,
    LOG_LEVEL: 'error',
    LOG_PRETTY_PRINT: false,
    LOG_CONSOLE_ENABLED: false,
  },
};
