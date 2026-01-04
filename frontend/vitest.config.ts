import { defineConfig } from 'vitest/config';
import react from '@vitejs/plugin-react';
import path from 'path';

export default defineConfig({
  plugins: [react()],
  test: {
    environment: 'jsdom',
    globals: true,
    setupFiles: ['./tests/setup.ts'],
    // Exclude tests that require external services (backend, browser)
    // Use specific commands for these: npm run test:contracts, test:integration, test:e2e
    exclude: [
      '**/node_modules/**',
      '**/dist/**',
      'tests/contracts/**',           // Requires running backend
      'tests/integration/**',         // Requires running backend
      'src/__tests__/integration/**', // Requires running backend
      'e2e/**',                       // Requires Playwright browser
    ],
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html'],
      include: ['src/**/*.{ts,tsx}'],
      exclude: [
        'node_modules/',
        'tests/',
        'src/**/*.test.{ts,tsx}',
        'src/**/*.spec.{ts,tsx}',
        'src/**/__tests__/**',
        '**/*.config.ts',
        '**/*.d.ts',
        'src/types/**',
        'src/styles/**',
      ],
      all: true,
      thresholds: {
        lines: 40,
        functions: 40,
        branches: 40,
        statements: 40,
      },
    },
  },
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
});
