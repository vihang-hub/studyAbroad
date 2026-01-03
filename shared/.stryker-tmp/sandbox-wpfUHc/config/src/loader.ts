/**
 * Configuration Loader
 *
 * Loads and validates environment configuration using Zod schemas.
 * Implements singleton pattern for performance.
 *
 * @module shared/config/loader
 */
// @ts-nocheck


import { EnvironmentConfigSchema, type EnvironmentConfig } from './schemas/environment.schema';

/**
 * Configuration Loader Class
 *
 * Provides singleton access to validated environment configuration.
 */
export class ConfigLoader {
  private static instance: EnvironmentConfig | null = null;

  /**
   * Load and validate environment configuration
   *
   * This method validates all environment variables against the schema.
   * On validation failure, it logs detailed error messages and throws.
   * Subsequent calls return the cached instance for performance.
   *
   * @throws {Error} If configuration validation fails
   * @returns Validated configuration object
   */
  static load(): EnvironmentConfig {
    if (this.instance) {
      return this.instance;
    }

    // Gather raw environment variables
    const rawConfig = {
      // Environment
      ENVIRONMENT_MODE: process.env.ENVIRONMENT_MODE,
      NODE_ENV: process.env.NODE_ENV,

      // Application
      APP_NAME: process.env.APP_NAME,
      APP_VERSION: process.env.APP_VERSION,
      NEXT_PUBLIC_APP_URL: process.env.NEXT_PUBLIC_APP_URL,
      NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL,
      API_URL: process.env.API_URL,
      PORT: process.env.PORT,

      // Database
      DATABASE_URL: process.env.DATABASE_URL,
      SUPABASE_URL: process.env.SUPABASE_URL,
      SUPABASE_ANON_KEY: process.env.SUPABASE_ANON_KEY,
      SUPABASE_SERVICE_ROLE_KEY: process.env.SUPABASE_SERVICE_ROLE_KEY,
      DATABASE_POOL_MAX: process.env.DATABASE_POOL_MAX,
      DATABASE_IDLE_TIMEOUT_MS: process.env.DATABASE_IDLE_TIMEOUT_MS,
      DATABASE_CONNECTION_TIMEOUT_MS: process.env.DATABASE_CONNECTION_TIMEOUT_MS,

      // Logging
      LOG_LEVEL: process.env.LOG_LEVEL,
      LOG_DIR: process.env.LOG_DIR,
      LOG_MAX_SIZE_MB: process.env.LOG_MAX_SIZE_MB,
      LOG_ROTATION_DAYS: process.env.LOG_ROTATION_DAYS,
      LOG_RETENTION_DAYS: process.env.LOG_RETENTION_DAYS,
      LOG_CONSOLE_ENABLED: process.env.LOG_CONSOLE_ENABLED,
      LOG_PRETTY_PRINT: process.env.LOG_PRETTY_PRINT,

      // Feature Flags
      ENABLE_SUPABASE: process.env.ENABLE_SUPABASE,
      ENABLE_PAYMENTS: process.env.ENABLE_PAYMENTS,
      ENABLE_RATE_LIMITING: process.env.ENABLE_RATE_LIMITING,
      ENABLE_OBSERVABILITY: process.env.ENABLE_OBSERVABILITY,

      // Clerk Authentication
      NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY: process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY,
      CLERK_SECRET_KEY: process.env.CLERK_SECRET_KEY,
      CLERK_WEBHOOK_SECRET: process.env.CLERK_WEBHOOK_SECRET,
      NEXT_PUBLIC_CLERK_SIGN_IN_URL: process.env.NEXT_PUBLIC_CLERK_SIGN_IN_URL,
      NEXT_PUBLIC_CLERK_SIGN_UP_URL: process.env.NEXT_PUBLIC_CLERK_SIGN_UP_URL,
      NEXT_PUBLIC_CLERK_AFTER_SIGN_IN_URL: process.env.NEXT_PUBLIC_CLERK_AFTER_SIGN_IN_URL,
      NEXT_PUBLIC_CLERK_AFTER_SIGN_UP_URL: process.env.NEXT_PUBLIC_CLERK_AFTER_SIGN_UP_URL,

      // Stripe Payment
      NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY: process.env.NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY,
      STRIPE_SECRET_KEY: process.env.STRIPE_SECRET_KEY,
      STRIPE_WEBHOOK_SECRET: process.env.STRIPE_WEBHOOK_SECRET,
      STRIPE_PRICE_ID: process.env.STRIPE_PRICE_ID,
      PAYMENT_AMOUNT: process.env.PAYMENT_AMOUNT,
      PAYMENT_CURRENCY: process.env.PAYMENT_CURRENCY,

      // Gemini AI
      GEMINI_API_KEY: process.env.GEMINI_API_KEY,
      GEMINI_MODEL: process.env.GEMINI_MODEL,
      GEMINI_MAX_TOKENS: process.env.GEMINI_MAX_TOKENS,
      GEMINI_TEMPERATURE: process.env.GEMINI_TEMPERATURE,
      GEMINI_TIMEOUT_MS: process.env.GEMINI_TIMEOUT_MS,

      // Rate Limiting
      RATE_LIMIT_MAX: process.env.RATE_LIMIT_MAX,
      RATE_LIMIT_WINDOW_SEC: process.env.RATE_LIMIT_WINDOW_SEC,
      RATE_LIMIT_REPORTS_PER_DAY: process.env.RATE_LIMIT_REPORTS_PER_DAY,
    };

    // Validate using Zod schema
    const result = EnvironmentConfigSchema.safeParse(rawConfig);

    if (!result.success) {
      const errors = result.error.format();
      console.error('❌ Configuration validation failed:');
      console.error(JSON.stringify(errors, null, 2));
      throw new Error(
        'Invalid environment configuration. Please check your environment variables.'
      );
    }

    this.instance = result.data;
    return this.instance;
  }

  /**
   * Get specific configuration value
   *
   * @param key Configuration key
   * @returns Configuration value
   * @throws {Error} If configuration not loaded
   */
  static get<K extends keyof EnvironmentConfig>(key: K): EnvironmentConfig[K] {
    if (!this.instance) {
      throw new Error('Configuration not loaded. Call ConfigLoader.load() first.');
    }
    return this.instance[key];
  }

  /**
   * Check if configuration is loaded
   *
   * @returns True if configuration is loaded
   */
  static isLoaded(): boolean {
    return this.instance !== null;
  }

  /**
   * Reload configuration
   *
   * Clears cached instance and forces re-validation.
   * Useful for testing or dynamic configuration updates.
   */
  static reload(): void {
    this.instance = null;
  }

  /**
   * Reset configuration (alias for reload)
   *
   * Primarily used in test environments to clear state between tests.
   */
  static reset(): void {
    this.reload();
  }
}
