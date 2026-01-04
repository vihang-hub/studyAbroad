/**
 * Vitest Configuration for Integration Tests
 *
 * Different from unit tests:
 * - No mocking of fetch
 * - Longer timeouts
 * - Requires running backend
 */

import { defineConfig } from 'vitest/config';
import react from '@vitejs/plugin-react';
import path from 'path';

export default defineConfig({
  plugins: [react()],
  test: {
    environment: 'node', // Use node for real network calls
    testTimeout: 30000, // 30 seconds for network calls
    hookTimeout: 30000,
    include: [
      'tests/contracts/**/*.test.ts',
      'tests/integration/**/*.test.ts',
    ],
    globals: true,
  },
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
});
