/**
 * Mock implementations for shared packages
 * These mocks prevent test environment failures when shared packages
 * try to load configuration, connect to databases, etc.
 */

import { vi } from 'vitest';

// Mock configuration values for test environment
export const mockConfig = {
  api: {
    baseUrl: 'http://localhost:8000',
    timeout: 5000,
  },
  features: {
    payments: false,
    supabase: false,
    rateLimiting: false,
  },
  environment: {
    mode: 'test' as const,
    logLevel: 'debug' as const,
  },
  clerk: {
    publishableKey: 'pk_test_mock',
    secretKey: 'sk_test_mock',
  },
  stripe: {
    publishableKey: 'pk_test_mock',
    secretKey: 'sk_test_mock',
  },
};

// Mock @study-abroad/shared-config
export const mockConfigLoader = {
  load: vi.fn(() => mockConfig),
  validate: vi.fn(() => true),
  get: vi.fn((key: string) => {
    const keys = key.split('.');
    let value: any = mockConfig;
    for (const k of keys) {
      value = value?.[k];
    }
    return value;
  }),
};

// Mock @study-abroad/shared-feature-flags
export const mockFeatureFlags = {
  isEnabled: vi.fn((feature: string) => {
    const flags: Record<string, boolean> = {
      payments: false,
      supabase: false,
      rateLimiting: false,
    };
    return flags[feature] ?? false;
  }),
  getFlags: vi.fn(() => ({
    payments: false,
    supabase: false,
    rateLimiting: false,
  })),
  getAllFlags: vi.fn(() => ({
    payments: false,
    supabase: false,
    rateLimiting: false,
  })),
};

// Mock @study-abroad/shared-logging
export const mockLogger = {
  info: vi.fn((message: string, ...args: any[]) => {
    // Silent in tests unless debugging
    if (process.env.DEBUG_TESTS) {
      console.log('[INFO]', message, ...args);
    }
  }),
  warn: vi.fn((message: string, ...args: any[]) => {
    if (process.env.DEBUG_TESTS) {
      console.warn('[WARN]', message, ...args);
    }
  }),
  error: vi.fn((message: string, ...args: any[]) => {
    if (process.env.DEBUG_TESTS) {
      console.error('[ERROR]', message, ...args);
    }
  }),
  debug: vi.fn((message: string, ...args: any[]) => {
    if (process.env.DEBUG_TESTS) {
      console.debug('[DEBUG]', message, ...args);
    }
  }),
  child: vi.fn(function(this: any) {
    return this;
  }),
};

// Mock @study-abroad/shared-database
export const mockDatabase = {
  query: vi.fn(() => Promise.resolve({ rows: [], rowCount: 0 })),
  connect: vi.fn(() => Promise.resolve()),
  disconnect: vi.fn(() => Promise.resolve()),
  getClient: vi.fn(() => ({
    query: vi.fn(() => Promise.resolve({ rows: [], rowCount: 0 })),
    release: vi.fn(),
  })),
};
