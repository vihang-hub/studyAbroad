/**
 * Environment Preset Configurations
 *
 * Provides preset configurations for different runtime environments.
 * Used for testing and documentation purposes.
 *
 * @module shared/config/presets
 */

import type { EnvironmentConfig, EnvironmentMode } from './schemas/environment.schema';

/**
 * Development Environment Preset
 *
 * - Local PostgreSQL database
 * - No payments (bypassed)
 * - Debug logging with pretty print
 * - All external services disabled
 */
export const DEV_PRESET: Partial<EnvironmentConfig> = {
  ENVIRONMENT_MODE: 'dev',
  NODE_ENV: 'development',

  // Feature Flags
  ENABLE_SUPABASE: false,
  ENABLE_PAYMENTS: false,
  ENABLE_RATE_LIMITING: false,
  ENABLE_OBSERVABILITY: false,

  // Database
  DATABASE_URL: 'postgresql://studyabroad:studyabroad_dev@localhost:5432/studyabroad_dev',

  // Logging
  LOG_LEVEL: 'debug',
  LOG_PRETTY_PRINT: true,
  LOG_CONSOLE_ENABLED: true,
  LOG_DIR: './logs',

  // Application
  NEXT_PUBLIC_APP_URL: 'http://localhost:3000',
  NEXT_PUBLIC_API_URL: 'http://localhost:8000',
  API_URL: 'http://localhost:8000',
  PORT: 8000,
};

/**
 * Test Environment Preset
 *
 * - Supabase database
 * - No payments (bypassed)
 * - Debug logging
 * - Supabase enabled, payments disabled
 */
export const TEST_PRESET: Partial<EnvironmentConfig> = {
  ENVIRONMENT_MODE: 'test',
  NODE_ENV: 'test',

  // Feature Flags
  ENABLE_SUPABASE: true,
  ENABLE_PAYMENTS: false,
  ENABLE_RATE_LIMITING: true,
  ENABLE_OBSERVABILITY: false,

  // Logging
  LOG_LEVEL: 'debug',
  LOG_PRETTY_PRINT: false,
  LOG_CONSOLE_ENABLED: true,
  LOG_DIR: './logs',
};

/**
 * Production Environment Preset
 *
 * - Supabase database
 * - Payments enabled
 * - Error-level logging only
 * - All production services enabled
 */
export const PRODUCTION_PRESET: Partial<EnvironmentConfig> = {
  ENVIRONMENT_MODE: 'production',
  NODE_ENV: 'production',

  // Feature Flags
  ENABLE_SUPABASE: true,
  ENABLE_PAYMENTS: true,
  ENABLE_RATE_LIMITING: true,
  ENABLE_OBSERVABILITY: true,

  // Logging
  LOG_LEVEL: 'error',
  LOG_PRETTY_PRINT: false,
  LOG_CONSOLE_ENABLED: false,
  LOG_DIR: '/var/log/app',
};

/**
 * Environment Presets Map
 *
 * Maps environment mode to preset configuration.
 */
export const EnvironmentPresets: Record<EnvironmentMode, Partial<EnvironmentConfig>> = {
  dev: DEV_PRESET,
  test: TEST_PRESET,
  production: PRODUCTION_PRESET,
};

/**
 * Get preset for environment mode
 *
 * @param mode Environment mode
 * @returns Preset configuration
 */
export function getPreset(mode: EnvironmentMode): Partial<EnvironmentConfig> {
  return EnvironmentPresets[mode];
}

/**
 * Merge preset with custom overrides
 *
 * @param mode Environment mode
 * @param overrides Custom configuration overrides
 * @returns Merged configuration
 */
export function mergePreset(
  mode: EnvironmentMode,
  overrides: Partial<EnvironmentConfig>
): Partial<EnvironmentConfig> {
  return {
    ...EnvironmentPresets[mode],
    ...overrides,
  };
}
