/**
 * Tests for PostgreSQL adapter
 */

import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';
import { Pool, PoolClient } from 'pg';
import { PostgresAdapter } from '../../src/adapters/postgres';

// Mock pg module
vi.mock('pg', () => {
  const mockQuery = vi.fn();
  const mockRelease = vi.fn();
  const mockConnect = vi.fn();
  const mockEnd = vi.fn();
  const mockOn = vi.fn();

  const MockPoolClient = vi.fn(() => ({
    query: mockQuery,
    release: mockRelease,
  }));

  const MockPool = vi.fn(() => ({
    query: mockQuery,
    connect: mockConnect,
    end: mockEnd,
    on: mockOn,
  }));

  return {
    Pool: MockPool,
    PoolClient: MockPoolClient,
  };
});

describe('PostgresAdapter', () => {
  let adapter: PostgresAdapter;
  let mockPool: any;

  beforeEach(() => {
    vi.clearAllMocks();
    adapter = new PostgresAdapter('postgresql://localhost:5432/test');
    mockPool = (adapter as any).pool;
  });

  afterEach(async () => {
    await adapter.close();
  });

  describe('constructor', () => {
    it('should create adapter with connection string', () => {
      const newAdapter = new PostgresAdapter('postgresql://localhost:5432/test');
      expect(newAdapter).toBeDefined();
      expect(newAdapter.getType()).toBe('postgres');
    });

    it('should create adapter with configuration object', () => {
      const newAdapter = new PostgresAdapter({
        connectionString: 'postgresql://localhost:5432/test',
        max: 10,
        idleTimeoutMillis: 20000,
        connectionTimeoutMillis: 1000,
      });
      expect(newAdapter).toBeDefined();
    });

    it('should use default pool configuration', () => {
      expect(Pool).toHaveBeenCalledWith(
        expect.objectContaining({
          connectionString: 'postgresql://localhost:5432/test',
          max: 20,
          idleTimeoutMillis: 30000,
          connectionTimeoutMillis: 2000,
        }),
      );
    });

    it('should register error handler on pool', () => {
      expect(mockPool.on).toHaveBeenCalledWith('error', expect.any(Function));
    });
  });

  describe('query', () => {
    it('should execute query without parameters', async () => {
      mockPool.query.mockResolvedValueOnce({
        rows: [{ id: 1, name: 'test' }],
        rowCount: 1,
      });

      const result = await adapter.query('SELECT * FROM users');

      expect(mockPool.query).toHaveBeenCalledWith('SELECT * FROM users', undefined);
      expect(result).toEqual({
        rows: [{ id: 1, name: 'test' }],
        rowCount: 1,
      });
    });

    it('should execute query with parameters', async () => {
      mockPool.query.mockResolvedValueOnce({
        rows: [{ id: 1, name: 'test' }],
        rowCount: 1,
      });

      const result = await adapter.query('SELECT * FROM users WHERE id = $1', [1]);

      expect(mockPool.query).toHaveBeenCalledWith('SELECT * FROM users WHERE id = $1', [1]);
      expect(result).toEqual({
        rows: [{ id: 1, name: 'test' }],
        rowCount: 1,
      });
    });

    it('should return empty rows when no results', async () => {
      mockPool.query.mockResolvedValueOnce({
        rows: [],
        rowCount: 0,
      });

      const result = await adapter.query('SELECT * FROM users WHERE id = $1', [999]);

      expect(result).toEqual({
        rows: [],
        rowCount: 0,
      });
    });

    it('should handle null rowCount', async () => {
      mockPool.query.mockResolvedValueOnce({
        rows: [],
        rowCount: null,
      });

      const result = await adapter.query('SELECT * FROM users');

      expect(result.rowCount).toBe(0);
    });

    it('should throw error on query failure', async () => {
      mockPool.query.mockRejectedValueOnce(new Error('Database connection failed'));

      await expect(adapter.query('SELECT * FROM users')).rejects.toThrow('Database connection failed');
    });

    it('should handle multiple concurrent queries', async () => {
      mockPool.query.mockResolvedValue({
        rows: [{ id: 1 }],
        rowCount: 1,
      });

      const queries = [
        adapter.query('SELECT * FROM users'),
        adapter.query('SELECT * FROM reports'),
        adapter.query('SELECT * FROM payments'),
      ];

      const results = await Promise.all(queries);

      expect(results).toHaveLength(3);
      expect(mockPool.query).toHaveBeenCalledTimes(3);
    });
  });

  describe('beginTransaction', () => {
    let mockClient: any;

    beforeEach(() => {
      mockClient = {
        query: vi.fn(),
        release: vi.fn(),
      };
      mockPool.connect.mockResolvedValue(mockClient);
    });

    it('should start a transaction', async () => {
      const transaction = await adapter.beginTransaction();

      expect(mockPool.connect).toHaveBeenCalled();
      expect(mockClient.query).toHaveBeenCalledWith('BEGIN');
      expect(transaction).toBeDefined();
    });

    it('should execute queries within transaction', async () => {
      mockClient.query.mockResolvedValueOnce({ rows: [], rowCount: 0 }); // BEGIN
      mockClient.query.mockResolvedValueOnce({
        rows: [{ id: 1 }],
        rowCount: 1,
      });

      const transaction = await adapter.beginTransaction();
      const result = await transaction.query('INSERT INTO users VALUES ($1)', [1]);

      expect(result).toEqual({
        rows: [{ id: 1 }],
        rowCount: 1,
      });
    });

    it('should commit transaction', async () => {
      mockClient.query.mockResolvedValue({ rows: [], rowCount: 0 });

      const transaction = await adapter.beginTransaction();
      await transaction.commit();

      expect(mockClient.query).toHaveBeenCalledWith('COMMIT');
      expect(mockClient.release).toHaveBeenCalled();
    });

    it('should rollback transaction', async () => {
      mockClient.query.mockResolvedValue({ rows: [], rowCount: 0 });

      const transaction = await adapter.beginTransaction();
      await transaction.rollback();

      expect(mockClient.query).toHaveBeenCalledWith('ROLLBACK');
      expect(mockClient.release).toHaveBeenCalled();
    });

    it('should release client on commit even if error occurs', async () => {
      mockClient.query.mockResolvedValueOnce({ rows: [], rowCount: 0 }); // BEGIN
      mockClient.query.mockRejectedValueOnce(new Error('Commit failed'));

      const transaction = await adapter.beginTransaction();

      await expect(transaction.commit()).rejects.toThrow('Commit failed');
      expect(mockClient.release).toHaveBeenCalled();
    });

    it('should release client on rollback even if error occurs', async () => {
      mockClient.query.mockResolvedValueOnce({ rows: [], rowCount: 0 }); // BEGIN
      mockClient.query.mockRejectedValueOnce(new Error('Rollback failed'));

      const transaction = await adapter.beginTransaction();

      await expect(transaction.rollback()).rejects.toThrow('Rollback failed');
      expect(mockClient.release).toHaveBeenCalled();
    });

    it('should throw error when querying completed transaction', async () => {
      mockClient.query.mockResolvedValue({ rows: [], rowCount: 0 });

      const transaction = await adapter.beginTransaction();
      await transaction.commit();

      await expect(transaction.query('SELECT 1')).rejects.toThrow('Transaction has already been completed');
    });

    it('should throw error when committing completed transaction', async () => {
      mockClient.query.mockResolvedValue({ rows: [], rowCount: 0 });

      const transaction = await adapter.beginTransaction();
      await transaction.commit();

      await expect(transaction.commit()).rejects.toThrow('Transaction has already been completed');
    });

    it('should throw error when rolling back completed transaction', async () => {
      mockClient.query.mockResolvedValue({ rows: [], rowCount: 0 });

      const transaction = await adapter.beginTransaction();
      await transaction.rollback();

      await expect(transaction.rollback()).rejects.toThrow('Transaction has already been completed');
    });

    it('should handle null rowCount in transaction query', async () => {
      mockClient.query.mockResolvedValueOnce({ rows: [], rowCount: 0 }); // BEGIN
      mockClient.query.mockResolvedValueOnce({
        rows: [{ id: 1 }],
        rowCount: null,
      });

      const transaction = await adapter.beginTransaction();
      const result = await transaction.query('SELECT * FROM users');

      expect(result.rowCount).toBe(0);
    });
  });

  describe('close', () => {
    it('should close the connection pool', async () => {
      await adapter.close();

      expect(mockPool.end).toHaveBeenCalled();
    });

    it('should be safe to call close multiple times', async () => {
      await adapter.close();
      await adapter.close();

      expect(mockPool.end).toHaveBeenCalledTimes(2);
    });
  });

  describe('getType', () => {
    it('should return postgres type', () => {
      expect(adapter.getType()).toBe('postgres');
    });
  });

  describe('error handling', () => {
    it('should handle pool error events', () => {
      const consoleSpy = vi.spyOn(console, 'error').mockImplementation(() => {});

      // Get the error handler
      const errorHandler = mockPool.on.mock.calls.find(
        (call: any[]) => call[0] === 'error',
      )?.[1];

      expect(errorHandler).toBeDefined();

      // Trigger error
      errorHandler(new Error('Pool error'));

      expect(consoleSpy).toHaveBeenCalledWith(
        'Unexpected error on idle PostgreSQL client',
        expect.any(Error),
      );

      consoleSpy.mockRestore();
    });
  });
});
