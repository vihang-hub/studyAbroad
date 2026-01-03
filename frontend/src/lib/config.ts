/**
 * Environment configuration integration for frontend
 * Uses @study-abroad/shared-config for type-safe configuration management
 *
 * IMPORTANT: Next.js requires environment variables used in the browser to be prefixed with NEXT_PUBLIC_
 * Server-side code can access all environment variables, but client-side code only sees NEXT_PUBLIC_ vars.
 */

import { ConfigLoader, type EnvironmentConfig } from '@study-abroad/shared-config';

// Singleton instance
let configInstance: EnvironmentConfig | null = null;

/**
 * Initialize configuration loader
 * Should be called once at app startup
 */
export function initializeConfig(): EnvironmentConfig {
  if (configInstance) {
    return configInstance;
  }

  try {
    // ConfigLoader has static methods - use ConfigLoader.load() directly
    configInstance = ConfigLoader.load();

    // In development, log successful initialization
    if (configInstance.ENVIRONMENT_MODE === 'dev') {
      console.log('[Config] Configuration initialized successfully', {
        mode: configInstance.ENVIRONMENT_MODE,
        enableSupabase: configInstance.ENABLE_SUPABASE,
        enablePayments: configInstance.ENABLE_PAYMENTS,
      });
    }

    return configInstance;
  } catch (error) {
    console.error('[Config] Failed to initialize configuration:', error);
    throw error;
  }
}

/**
 * Get the current configuration
 * Throws if configuration hasn't been initialized
 */
export function getConfig(): EnvironmentConfig {
  if (!configInstance) {
    throw new Error('Configuration not initialized. Call initializeConfig() first.');
  }
  return configInstance;
}

/**
 * Get a specific configuration value with type safety
 */
export function getConfigValue<K extends keyof EnvironmentConfig>(
  key: K,
): EnvironmentConfig[K] {
  return getConfig()[key];
}

/**
 * Client-side safe configuration getter
 * Only returns values that are safe to expose in the browser
 *
 * This should be used in client components to avoid accidentally
 * exposing server-side secrets
 */
export function getClientConfig() {
  const config = getConfig();

  return {
    mode: config.ENVIRONMENT_MODE,
    apiUrl: config.NEXT_PUBLIC_API_URL,
    enableSupabase: config.ENABLE_SUPABASE,
    enablePayments: config.ENABLE_PAYMENTS,
    supabaseUrl: config.SUPABASE_URL,
    // Note: anon key is safe to expose (it's public)
    supabaseAnonKey: config.SUPABASE_ANON_KEY,
  };
}

/**
 * Check if we're running in development mode
 */
export function isDevelopment(): boolean {
  return getConfig().ENVIRONMENT_MODE === 'dev';
}

/**
 * Check if we're running in production mode
 */
export function isProduction(): boolean {
  return getConfig().ENVIRONMENT_MODE === 'production';
}

/**
 * Check if we're running in test mode
 */
export function isTest(): boolean {
  return getConfig().ENVIRONMENT_MODE === 'test';
}

/**
 * Validate required environment variables
 * Throws descriptive errors if validation fails
 */
export function validateEnvironment(): void {
  const requiredClientVars = [
    'NEXT_PUBLIC_API_URL',
    'NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY',
  ];

  const requiredServerVars = [
    'CLERK_SECRET_KEY',
  ];

  const missing: string[] = [];

  // Check client-side variables
  requiredClientVars.forEach((varName) => {
    if (!process.env[varName]) {
      missing.push(varName);
    }
  });

  // Check server-side variables (only on server)
  if (typeof window === 'undefined') {
    requiredServerVars.forEach((varName) => {
      if (!process.env[varName]) {
        missing.push(varName);
      }
    });
  }

  if (missing.length > 0) {
    const errorMessage = `Missing required environment variables:\n${missing.join('\n')}`;
    console.error('[Config]', errorMessage);
    throw new Error(errorMessage);
  }

  // Validate optional variables based on feature flags
  const config = getConfig();

  if (config.ENABLE_SUPABASE) {
    if (!config.SUPABASE_URL || !config.SUPABASE_ANON_KEY) {
      throw new Error(
        'Supabase is enabled but NEXT_PUBLIC_SUPABASE_URL or NEXT_PUBLIC_SUPABASE_ANON_KEY is missing',
      );
    }
  }

  if (config.ENABLE_PAYMENTS && typeof window !== 'undefined') {
    if (!process.env.NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY) {
      throw new Error(
        'Payments are enabled but NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY is missing',
      );
    }
  }
}

// Export the ConfigLoader class for advanced use cases
export { ConfigLoader };
