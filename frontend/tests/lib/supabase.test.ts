/**
 * Tests for Supabase client utilities
 */

import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';

// Mock the Supabase client
vi.mock('@supabase/supabase-js', () => ({
  createClient: vi.fn(() => ({
    // Mock Supabase client instance
    from: vi.fn(),
    auth: {
      signIn: vi.fn(),
      signOut: vi.fn(),
    },
  })),
}));

// Mock the config module
vi.mock('../../src/lib/config', () => ({
  getConfig: vi.fn(),
}));

describe('supabase', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    vi.resetModules();
  });

  afterEach(() => {
    vi.resetModules();
  });

  describe('getSupabaseConfig', () => {
    it('should return Supabase configuration from config', async () => {
      const mockConfig = {
        supabaseUrl: 'https://test.supabase.co',
        supabaseAnonKey: 'test-anon-key-123',
      };

      const { getConfig } = await import('../../src/lib/config');
      (getConfig as unknown as ReturnType<typeof vi.fn>).mockReturnValue(mockConfig);

      const { getSupabaseConfig } = await import('../../src/lib/supabase');
      const config = getSupabaseConfig();

      expect(config).toEqual({
        url: 'https://test.supabase.co',
        anonKey: 'test-anon-key-123',
      });
    });

    it('should handle undefined values', async () => {
      const mockConfig = {
        supabaseUrl: undefined,
        supabaseAnonKey: undefined,
      };

      const { getConfig } = await import('../../src/lib/config');
      (getConfig as unknown as ReturnType<typeof vi.fn>).mockReturnValue(mockConfig);

      const { getSupabaseConfig } = await import('../../src/lib/supabase');
      const config = getSupabaseConfig();

      expect(config).toEqual({
        url: undefined,
        anonKey: undefined,
      });
    });

    it('should handle empty strings', async () => {
      const mockConfig = {
        supabaseUrl: '',
        supabaseAnonKey: '',
      };

      const { getConfig } = await import('../../src/lib/config');
      (getConfig as unknown as ReturnType<typeof vi.fn>).mockReturnValue(mockConfig);

      const { getSupabaseConfig } = await import('../../src/lib/supabase');
      const config = getSupabaseConfig();

      expect(config).toEqual({
        url: '',
        anonKey: '',
      });
    });
  });

  describe('getSupabase', () => {
    it('should create and return Supabase client', async () => {
      const mockConfig = {
        supabaseUrl: 'https://test.supabase.co',
        supabaseAnonKey: 'test-anon-key-123',
      };

      const { getConfig } = await import('../../src/lib/config');
      (getConfig as unknown as ReturnType<typeof vi.fn>).mockReturnValue(mockConfig);

      const { createClient } = await import('@supabase/supabase-js');
      const { getSupabase } = await import('../../src/lib/supabase');

      const client = getSupabase();

      expect(createClient).toHaveBeenCalledWith(
        'https://test.supabase.co',
        'test-anon-key-123'
      );
      expect(client).toBeDefined();
    });

    it('should create client with correct parameters', async () => {
      const mockConfig = {
        supabaseUrl: 'https://production.supabase.co',
        supabaseAnonKey: 'production-anon-key-456',
      };

      const { getConfig } = await import('../../src/lib/config');
      (getConfig as unknown as ReturnType<typeof vi.fn>).mockReturnValue(mockConfig);

      const { createClient } = await import('@supabase/supabase-js');
      const { getSupabase } = await import('../../src/lib/supabase');

      getSupabase();

      expect(createClient).toHaveBeenCalledWith(
        'https://production.supabase.co',
        'production-anon-key-456'
      );
    });

    it('should return a client with expected methods', async () => {
      const mockConfig = {
        supabaseUrl: 'https://test.supabase.co',
        supabaseAnonKey: 'test-key',
      };

      const { getConfig } = await import('../../src/lib/config');
      (getConfig as unknown as ReturnType<typeof vi.fn>).mockReturnValue(mockConfig);

      const { getSupabase } = await import('../../src/lib/supabase');
      const client = getSupabase();

      expect(client).toHaveProperty('from');
      expect(client).toHaveProperty('auth');
    });
  });
});
