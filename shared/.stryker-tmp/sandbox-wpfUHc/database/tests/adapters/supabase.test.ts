/**
 * Tests for Supabase adapter
 */
// @ts-nocheck


import { describe, it, expect, beforeEach, vi } from 'vitest';
import { SupabaseAdapter } from '../../src/adapters/supabase';

// Mock @supabase/supabase-js
vi.mock('@supabase/supabase-js', () => {
  const mockClient = {
    rpc: vi.fn(),
    auth: {
      getSession: vi.fn(),
    },
  };

  const mockCreateClient = vi.fn(() => mockClient);

  return {
    createClient: mockCreateClient,
  };
});

let mockClient: any;
let mockCreateClient: any;

describe('SupabaseAdapter', () => {
  let adapter: SupabaseAdapter;

  beforeEach(async () => {
    vi.clearAllMocks();

    // Get the mocked module
    const supabase = await import('@supabase/supabase-js');
    mockCreateClient = supabase.createClient as any;

    // Set up mock client
    mockClient = {
      rpc: vi.fn(),
      auth: {
        getSession: vi.fn(),
      },
    };

    mockCreateClient.mockReturnValue(mockClient);

    adapter = new SupabaseAdapter({
      url: 'https://test.supabase.co',
      anonKey: 'test-anon-key',
    });
  });

  describe('constructor', () => {
    it('should create adapter with anon key', () => {
      const newAdapter = new SupabaseAdapter({
        url: 'https://test.supabase.co',
        anonKey: 'test-anon-key',
      });

      expect(newAdapter).toBeDefined();
      expect(newAdapter.getType()).toBe('supabase');
      expect(mockCreateClient).toHaveBeenCalledWith(
        'https://test.supabase.co',
        'test-anon-key',
        expect.objectContaining({
          auth: {
            persistSession: false,
            autoRefreshToken: false,
          },
        }),
      );
    });

    it('should create adapter with service role key', () => {
      const newAdapter = new SupabaseAdapter({
        url: 'https://test.supabase.co',
        anonKey: 'test-anon-key',
        serviceRoleKey: 'test-service-role-key',
      });

      expect(newAdapter).toBeDefined();
      expect(mockCreateClient).toHaveBeenCalledWith(
        'https://test.supabase.co',
        'test-service-role-key',
        expect.any(Object),
      );
    });

    it('should configure stateless client', () => {
      new SupabaseAdapter({
        url: 'https://test.supabase.co',
        anonKey: 'test-anon-key',
      });

      expect(mockCreateClient).toHaveBeenCalledWith(
        expect.any(String),
        expect.any(String),
        expect.objectContaining({
          auth: {
            persistSession: false,
            autoRefreshToken: false,
          },
        }),
      );
    });
  });

  describe('query', () => {
    it('should execute query via RPC', async () => {
      mockClient.rpc.mockResolvedValueOnce({
        data: [{ id: 1, name: 'test' }],
        error: null,
      });

      const result = await adapter.query('SELECT * FROM users');

      expect(mockClient.rpc).toHaveBeenCalledWith('exec_sql', {
        query: 'SELECT * FROM users',
        params: [],
      });
      expect(result).toEqual({
        rows: [{ id: 1, name: 'test' }],
        rowCount: 1,
      });
    });

    it('should execute query with parameters', async () => {
      mockClient.rpc.mockResolvedValueOnce({
        data: [{ id: 1, name: 'test' }],
        error: null,
      });

      const result = await adapter.query('SELECT * FROM users WHERE id = $1', [1]);

      expect(mockClient.rpc).toHaveBeenCalledWith('exec_sql', {
        query: 'SELECT * FROM users WHERE id = $1',
        params: [1],
      });
    });

    it('should return empty rows when no results', async () => {
      mockClient.rpc.mockResolvedValueOnce({
        data: [],
        error: null,
      });

      const result = await adapter.query('SELECT * FROM users WHERE id = $1', [999]);

      expect(result).toEqual({
        rows: [],
        rowCount: 0,
      });
    });

    it('should handle null data', async () => {
      mockClient.rpc.mockResolvedValueOnce({
        data: null,
        error: null,
      });

      const result = await adapter.query('SELECT * FROM users');

      expect(result).toEqual({
        rows: [],
        rowCount: 0,
      });
    });

    it('should throw error on RPC failure', async () => {
      mockClient.rpc.mockResolvedValueOnce({
        data: null,
        error: { message: 'RPC failed' },
      });

      await expect(adapter.query('SELECT * FROM users')).rejects.toThrow('Supabase query error: RPC failed');
    });

    it('should handle complex query results', async () => {
      const complexData = [
        { id: 1, name: 'User 1', metadata: { role: 'admin' } },
        { id: 2, name: 'User 2', metadata: { role: 'user' } },
        { id: 3, name: 'User 3', metadata: { role: 'user' } },
      ];

      mockClient.rpc.mockResolvedValueOnce({
        data: complexData,
        error: null,
      });

      const result = await adapter.query('SELECT * FROM users');

      expect(result.rows).toEqual(complexData);
      expect(result.rowCount).toBe(3);
    });

    it('should default to empty params array when not provided', async () => {
      mockClient.rpc.mockResolvedValueOnce({
        data: [],
        error: null,
      });

      await adapter.query('SELECT 1');

      expect(mockClient.rpc).toHaveBeenCalledWith('exec_sql', {
        query: 'SELECT 1',
        params: [],
      });
    });
  });

  describe('beginTransaction', () => {
    it('should throw error for transactions', async () => {
      await expect(adapter.beginTransaction()).rejects.toThrow(
        'Transactions not supported in Supabase adapter',
      );
    });

    it('should include helpful error message', async () => {
      await expect(adapter.beginTransaction()).rejects.toThrow(
        'Use database functions or Edge Functions for transactional operations',
      );
    });
  });

  describe('close', () => {
    it('should close without error', async () => {
      await expect(adapter.close()).resolves.toBeUndefined();
    });

    it('should be safe to call multiple times', async () => {
      await adapter.close();
      await adapter.close();
      // No error expected
    });
  });

  describe('getType', () => {
    it('should return supabase type', () => {
      expect(adapter.getType()).toBe('supabase');
    });
  });

  describe('getClient', () => {
    it('should return underlying Supabase client', () => {
      const client = adapter.getClient();

      expect(client).toBe(mockClient);
    });

    it('should expose RPC method', () => {
      const client = adapter.getClient();

      expect(client.rpc).toBeDefined();
      expect(typeof client.rpc).toBe('function');
    });
  });

  describe('setAuthContext', () => {
    it('should set auth context for RLS', async () => {
      mockClient.rpc.mockResolvedValueOnce({
        data: [],
        error: null,
      });

      await adapter.setAuthContext('user-123');

      expect(mockClient.rpc).toHaveBeenCalledWith('exec_sql', {
        query: 'SET LOCAL request.jwt.claim.sub = $1',
        params: ['user-123'],
      });
    });

    it('should handle auth context errors', async () => {
      mockClient.rpc.mockResolvedValueOnce({
        data: null,
        error: { message: 'Invalid user ID' },
      });

      await expect(adapter.setAuthContext('invalid')).rejects.toThrow('Supabase query error: Invalid user ID');
    });
  });
});
