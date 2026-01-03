/**
 * Tests for database package main exports
 */

import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';
import { ConfigLoader } from '@study-abroad/shared-config';
import { FeatureFlags, Feature } from '@study-abroad/shared-feature-flags';

// Mock dependencies
vi.mock('@study-abroad/shared-config');
vi.mock('@study-abroad/shared-feature-flags');
vi.mock('pg');
vi.mock('@supabase/supabase-js', () => ({
  createClient: vi.fn(() => ({
    rpc: vi.fn(),
    auth: { getSession: vi.fn() },
  })),
}));

describe('Database Package Integration', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    // Reset mocks to prevent side effects from singleton db instance
    (FeatureFlags.isEnabled as any).mockReturnValue(false);
    (ConfigLoader.load as any).mockReturnValue({
      DATABASE_URL: 'postgresql://localhost:5432/test',
      DATABASE_POOL_MAX: 20,
      DATABASE_IDLE_TIMEOUT_MS: 30000,
      DATABASE_CONNECTION_TIMEOUT_MS: 2000,
    });
  });

  describe('Package Exports', () => {
    it('should export createDatabaseAdapter function', async () => {
      const pkg = await import('../src/index');
      expect(pkg.createDatabaseAdapter).toBeDefined();
      expect(typeof pkg.createDatabaseAdapter).toBe('function');
    });

    it('should export DatabaseContext class', async () => {
      const pkg = await import('../src/index');
      expect(pkg.DatabaseContext).toBeDefined();
      expect(typeof pkg.DatabaseContext).toBe('function');
    });

    it('should export singleton db instance', async () => {
      const pkg = await import('../src/index');
      expect(pkg.db).toBeDefined();
    });

    it('should export adapter types', async () => {
      const pkg = await import('../src/adapters');
      expect(pkg.PostgresAdapter).toBeDefined();
      expect(pkg.SupabaseAdapter).toBeDefined();
    });

    it('should export repository types', async () => {
      const pkg = await import('../src/repositories');
      expect(pkg.UserRepository).toBeDefined();
      expect(pkg.ReportRepository).toBeDefined();
      expect(pkg.PaymentRepository).toBeDefined();
      expect(pkg.BaseRepository).toBeDefined();
      expect(pkg.SoftDeleteBaseRepository).toBeDefined();
    });

    it('should export type definitions', async () => {
      const pkg = await import('../src/types');
      expect(pkg.mapToUser).toBeDefined();
      expect(pkg.mapToReport).toBeDefined();
      expect(pkg.mapToPayment).toBeDefined();
    });
  });

  describe('createDatabaseAdapter', () => {
    it('should create PostgreSQL adapter when ENABLE_SUPABASE is false', async () => {
      (FeatureFlags.isEnabled as any).mockReturnValue(false);
      (ConfigLoader.load as any).mockReturnValue({
        DATABASE_URL: 'postgresql://localhost:5432/test',
        DATABASE_POOL_MAX: 20,
        DATABASE_IDLE_TIMEOUT_MS: 30000,
        DATABASE_CONNECTION_TIMEOUT_MS: 2000,
      });

      const { createDatabaseAdapter } = await import('../src/index');
      const adapter = createDatabaseAdapter();

      expect(adapter.getType()).toBe('postgres');
      expect(FeatureFlags.isEnabled).toHaveBeenCalledWith(Feature.SUPABASE);
    });

    it('should create Supabase adapter when ENABLE_SUPABASE is true', async () => {
      (FeatureFlags.isEnabled as any).mockReturnValue(true);
      (ConfigLoader.load as any).mockReturnValue({
        SUPABASE_URL: 'https://test.supabase.co',
        SUPABASE_ANON_KEY: 'test-anon-key',
        SUPABASE_SERVICE_ROLE_KEY: 'test-service-role-key',
      });

      const { createDatabaseAdapter } = await import('../src/index');
      const adapter = createDatabaseAdapter();

      expect(adapter.getType()).toBe('supabase');
    });

    it('should throw error when ENABLE_SUPABASE is true but config missing', async () => {
      (FeatureFlags.isEnabled as any).mockReturnValue(true);
      (ConfigLoader.load as any).mockReturnValue({});

      const { createDatabaseAdapter } = await import('../src/index');
      expect(() => createDatabaseAdapter()).toThrow(
        'ENABLE_SUPABASE is true but Supabase configuration is missing',
      );
    });

    it('should throw error when ENABLE_SUPABASE is false but DATABASE_URL missing', async () => {
      (FeatureFlags.isEnabled as any).mockReturnValue(false);
      (ConfigLoader.load as any).mockReturnValue({});

      const { createDatabaseAdapter } = await import('../src/index');
      expect(() => createDatabaseAdapter()).toThrow(
        'ENABLE_SUPABASE is false but DATABASE_URL is not configured',
      );
    });

    it('should include helpful error message for Supabase config', async () => {
      (FeatureFlags.isEnabled as any).mockReturnValue(true);
      (ConfigLoader.load as any).mockReturnValue({
        SUPABASE_URL: 'https://test.supabase.co',
      });

      const { createDatabaseAdapter } = await import('../src/index');
      expect(() => createDatabaseAdapter()).toThrow(/Required: SUPABASE_URL, SUPABASE_ANON_KEY/);
    });

    it('should include helpful error message for PostgreSQL config', async () => {
      (FeatureFlags.isEnabled as any).mockReturnValue(false);
      (ConfigLoader.load as any).mockReturnValue({});

      const { createDatabaseAdapter } = await import('../src/index');
      expect(() => createDatabaseAdapter()).toThrow(/Required for PostgreSQL adapter/);
    });
  });

  describe('DatabaseContext', () => {
    let context: any;

    afterEach(async () => {
      if (context) {
        await context.close();
      }
    });

    it('should create context with default adapter', async () => {
      const { DatabaseContext } = await import('../src/index');
      context = new DatabaseContext();

      expect(context).toBeDefined();
      expect(context.users).toBeDefined();
      expect(context.reports).toBeDefined();
      expect(context.payments).toBeDefined();
    });

    it('should create context with custom adapter', async () => {
      const mockAdapter: any = {
        query: vi.fn(),
        beginTransaction: vi.fn(),
        close: vi.fn(),
        getType: vi.fn(() => 'postgres'),
      };

      const { DatabaseContext } = await import('../src/index');
      context = new DatabaseContext(mockAdapter);

      expect(context.getAdapter()).toBe(mockAdapter);
    });

    it('should initialize all repositories', async () => {
      const { DatabaseContext } = await import('../src/index');
      context = new DatabaseContext();

      expect(context.users).toBeInstanceOf(Object);
      expect(context.reports).toBeInstanceOf(Object);
      expect(context.payments).toBeInstanceOf(Object);
    });

    it('should provide access to underlying adapter', async () => {
      const { DatabaseContext } = await import('../src/index');
      context = new DatabaseContext();
      const adapter = context.getAdapter();

      expect(adapter).toBeDefined();
      expect(adapter.getType()).toBe('postgres');
    });

    it('should close adapter when context is closed', async () => {
      const mockAdapter: any = {
        query: vi.fn(),
        beginTransaction: vi.fn(),
        close: vi.fn(),
        getType: vi.fn(() => 'postgres'),
      };

      const { DatabaseContext } = await import('../src/index');
      context = new DatabaseContext(mockAdapter);
      await context.close();

      expect(mockAdapter.close).toHaveBeenCalled();
    });

    it('should share adapter across all repositories', async () => {
      const { DatabaseContext } = await import('../src/index');
      context = new DatabaseContext();
      const adapter = context.getAdapter();

      // All repositories should use the same adapter instance
      expect((context.users as any).db).toBe(adapter);
      expect((context.reports as any).db).toBe(adapter);
      expect((context.payments as any).db).toBe(adapter);
    });
  });

  describe('Singleton db instance', () => {
    it('should have all repository properties', async () => {
      const { db } = await import('../src/index');
      expect(db.users).toBeDefined();
      expect(db.reports).toBeDefined();
      expect(db.payments).toBeDefined();
    });

    it('should have getAdapter method', async () => {
      const { db } = await import('../src/index');
      expect(typeof db.getAdapter).toBe('function');
    });

    it('should have close method', async () => {
      const { db } = await import('../src/index');
      expect(typeof db.close).toBe('function');
    });
  });

  describe('Repository Integration', () => {
    let context: any;
    let mockAdapter: any;

    beforeEach(() => {
      mockAdapter = {
        query: vi.fn(),
        beginTransaction: vi.fn(),
        close: vi.fn(),
        getType: vi.fn(() => 'postgres'),
      };
    });

    afterEach(async () => {
      if (context) {
        await context.close();
      }
    });

    it('should execute user repository queries through adapter', async () => {
      const { DatabaseContext } = await import('../src/index');
      context = new DatabaseContext(mockAdapter);

      mockAdapter.query.mockResolvedValueOnce({
        rows: [],
        rowCount: 0,
      });

      await context.users.findById('user-123');

      expect(mockAdapter.query).toHaveBeenCalledWith(
        expect.stringContaining('SELECT * FROM users'),
        ['user-123'],
      );
    });

    it('should execute report repository queries through adapter', async () => {
      const { DatabaseContext } = await import('../src/index');
      context = new DatabaseContext(mockAdapter);

      mockAdapter.query.mockResolvedValueOnce({
        rows: [],
        rowCount: 0,
      });

      await context.reports.findById('report-123', 'user-123');

      expect(mockAdapter.query).toHaveBeenCalledWith(
        expect.stringContaining('SELECT * FROM reports'),
        expect.any(Array),
      );
    });

    it('should execute payment repository queries through adapter', async () => {
      const { DatabaseContext } = await import('../src/index');
      context = new DatabaseContext(mockAdapter);

      mockAdapter.query.mockResolvedValueOnce({
        rows: [],
        rowCount: 0,
      });

      await context.payments.findById('payment-123', 'user-123');

      expect(mockAdapter.query).toHaveBeenCalledWith(
        expect.stringContaining('SELECT * FROM payments'),
        expect.any(Array),
      );
    });

    it('should handle concurrent queries across repositories', async () => {
      const { DatabaseContext } = await import('../src/index');
      context = new DatabaseContext(mockAdapter);

      mockAdapter.query.mockResolvedValue({
        rows: [],
        rowCount: 0,
      });

      await Promise.all([
        context.users.findById('user-123'),
        context.reports.findById('report-123', 'user-123'),
        context.payments.findById('payment-123', 'user-123'),
      ]);

      expect(mockAdapter.query).toHaveBeenCalledTimes(3);
    });
  });

  describe('Error Handling', () => {
    it('should propagate adapter query errors', async () => {
      const mockAdapter: any = {
        query: vi.fn().mockRejectedValue(new Error('Connection failed')),
        beginTransaction: vi.fn(),
        close: vi.fn(),
        getType: vi.fn(() => 'postgres'),
      };

      const { DatabaseContext } = await import('../src/index');
      const context = new DatabaseContext(mockAdapter);

      await expect(context.users.findById('user-123')).rejects.toThrow('Connection failed');
    });

    it('should handle missing configuration gracefully', async () => {
      (FeatureFlags.isEnabled as any).mockReturnValue(false);
      (ConfigLoader.load as any).mockReturnValue({});

      const { DatabaseContext } = await import('../src/index');
      expect(() => new DatabaseContext()).toThrow();
    });
  });

  describe('Type Safety', () => {
    it('should return typed results from repositories', async () => {
      const mockAdapter: any = {
        query: vi.fn().mockResolvedValue({
          rows: [
            {
              user_id: 'user-123',
              clerk_user_id: 'clerk-123',
              email: 'test@example.com',
              created_at: new Date(),
            },
          ],
          rowCount: 1,
        }),
        beginTransaction: vi.fn(),
        close: vi.fn(),
        getType: vi.fn(() => 'postgres'),
      };

      const { DatabaseContext } = await import('../src/index');
      const context = new DatabaseContext(mockAdapter);
      const user = await context.users.findById('user-123');

      expect(user).toBeDefined();
      expect(user?.userId).toBe('user-123');
      expect(user?.clerkUserId).toBe('clerk-123');
      expect(user?.email).toBe('test@example.com');
    });
  });
});
