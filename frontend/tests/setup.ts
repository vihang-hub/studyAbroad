import { expect, afterEach, beforeAll, vi } from 'vitest';
import { cleanup } from '@testing-library/react';
import * as matchers from '@testing-library/jest-dom/matchers';
import * as dotenv from 'dotenv';
import { resolve } from 'path';
import {
  mockConfig,
  mockConfigLoader,
  mockFeatureFlags,
  mockLogger,
  mockDatabase,
} from './mocks/shared-packages';
import { setupFetchMock, resetFetchMock } from './mocks/api-responses';

// Helper to reset all mocks between tests
function resetAllMocks(): void {
  mockConfigLoader.load.mockClear();
  mockConfigLoader.validate.mockClear();
  mockConfigLoader.get.mockClear();

  mockFeatureFlags.isEnabled.mockClear();
  mockFeatureFlags.getFlags.mockClear();
  mockFeatureFlags.getAllFlags.mockClear();

  mockLogger.info.mockClear();
  mockLogger.warn.mockClear();
  mockLogger.error.mockClear();
  mockLogger.debug.mockClear();

  mockDatabase.query.mockClear();
  mockDatabase.connect.mockClear();
  mockDatabase.disconnect.mockClear();
}

// Mock shared packages before all tests
vi.mock('@study-abroad/shared-config', () => ({
  ConfigLoader: {
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
  },
  getConfig: vi.fn(() => mockConfig),
  loadConfig: vi.fn(() => mockConfig),
}));

vi.mock('@study-abroad/shared-feature-flags', () => ({
  FeatureFlagEvaluator: vi.fn(() => mockFeatureFlags),
  isFeatureEnabled: mockFeatureFlags.isEnabled,
  getFlags: mockFeatureFlags.getFlags,
}));

vi.mock('@study-abroad/shared-logging', () => ({
  Logger: vi.fn(() => mockLogger),
  createLogger: vi.fn(() => mockLogger),
  getLogger: vi.fn(() => mockLogger),
}));

vi.mock('@study-abroad/shared-database', () => ({
  Database: vi.fn(() => mockDatabase),
  getDatabase: vi.fn(() => mockDatabase),
}));

// Mock Clerk authentication
vi.mock('@clerk/nextjs', () => ({
  useAuth: vi.fn(() => ({
    isSignedIn: true,
    userId: 'test-user-123',
    signOut: vi.fn(),
    getToken: vi.fn(() => Promise.resolve('mock-token')),
  })),
  useUser: vi.fn(() => ({
    user: {
      id: 'test-user-123',
      primaryEmailAddress: { emailAddress: 'test@example.com' },
      firstName: 'Test',
      lastName: 'User',
      fullName: 'Test User',
      imageUrl: 'https://example.com/avatar.jpg',
    },
    isLoaded: true,
    isSignedIn: true,
  })),
  useClerk: vi.fn(() => ({
    signOut: vi.fn(() => Promise.resolve()),
    openSignIn: vi.fn(),
    openSignUp: vi.fn(),
  })),
  ClerkProvider: ({ children }: { children: React.ReactNode }) => children,
  SignIn: () => null,
  SignUp: () => null,
  SignedIn: ({ children }: { children: React.ReactNode }) => children,
  SignedOut: () => null,
  RedirectToSignIn: () => null,
}));

// Mock @clerk/clerk-react (used by shared packages)
vi.mock('@clerk/clerk-react', () => ({
  useUser: vi.fn(() => ({
    isLoaded: true,
    isSignedIn: true,
    user: {
      id: 'test-user-123',
      fullName: 'Test User',
      primaryEmailAddress: { emailAddress: 'test@example.com' },
      imageUrl: 'https://example.com/avatar.jpg',
    },
  })),
  useClerk: vi.fn(() => ({
    signOut: vi.fn(),
    openSignIn: vi.fn(),
    openSignUp: vi.fn(),
  })),
}));

// Load test environment variables
beforeAll(() => {
  // Load .env.test file
  dotenv.config({ path: resolve(__dirname, '../.env.test') });

  // Set required Next.js env vars for testing
  process.env.NODE_ENV = 'test';
  process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY = process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY || 'pk_test_mock';
  process.env.NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY = process.env.NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY || 'pk_test_mock';
  process.env.NEXT_PUBLIC_API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
  process.env.CLERK_SECRET_KEY = process.env.CLERK_SECRET_KEY || 'sk_test_mock';

  // Setup global fetch mock
  setupFetchMock();
});

// Extend Vitest's expect with jest-dom matchers
expect.extend(matchers);

// Cleanup after each test
afterEach(() => {
  cleanup();
  resetAllMocks();
  resetFetchMock();
});
