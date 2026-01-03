/**
 * Test setup for database package
 * This package does not use React, so we don't need React-specific setup
 */
// @ts-nocheck


import { vi } from 'vitest';

// Mock environment variables
process.env.NODE_ENV = 'test';
process.env.DATABASE_URL = 'postgresql://localhost:5432/test';
process.env.ENABLE_SUPABASE = 'false';

// Configure vi.fn() to work with TypeScript
global.vi = vi;
