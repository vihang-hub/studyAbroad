/**
 * Supabase database adapter
 * Used for test and production environments with Row-Level Security
 */

import { createClient, SupabaseClient } from '@supabase/supabase-js';
import { DatabaseAdapter, QueryResult, Transaction } from './base';

/**
 * Supabase adapter configuration
 */
export interface SupabaseAdapterConfig {
  url: string;
  anonKey: string;
  serviceRoleKey?: string;
}

/**
 * Supabase adapter implementation
 * Note: This adapter uses Supabase's PostgreSQL REST API, not raw SQL
 * For complex queries, you may need to create database functions
 */
export class SupabaseAdapter implements DatabaseAdapter {
  private client: SupabaseClient;

  /**
   * Create a new Supabase adapter
   * @param config Supabase configuration
   */
  constructor(config: SupabaseAdapterConfig) {
    // Use service role key if available (bypasses RLS for backend operations)
    // Otherwise use anon key (RLS enforced)
    const key = config.serviceRoleKey ?? config.anonKey;

    this.client = createClient(config.url, key, {
      auth: {
        persistSession: false, // Stateless backend
        autoRefreshToken: false,
      },
    });
  }

  /**
   * Execute a SQL query via Supabase RPC
   * Note: This requires a database function 'exec_sql' to be created
   * For production use, prefer using Supabase's query builder or specific RPC functions
   */
  async query<T>(sql: string, params?: any[]): Promise<QueryResult<T>> {
    // Supabase doesn't support raw SQL queries directly
    // We use RPC to execute SQL via a stored function
    const { data, error } = await this.client.rpc('exec_sql', {
      query: sql,
      params: params ?? [],
    });

    if (error) {
      throw new Error(`Supabase query error: ${error.message}`);
    }

    const rows = (data as T[]) ?? [];
    return {
      rows,
      rowCount: rows.length,
    };
  }

  /**
   * Begin a transaction
   * Note: Supabase does not support client-side transactions
   * Transactions must be handled via Edge Functions or database functions
   */
  async beginTransaction(): Promise<Transaction> {
    throw new Error(
      'Transactions not supported in Supabase adapter. '
      + 'Use database functions or Edge Functions for transactional operations.',
    );
  }

  /**
   * Close the Supabase client
   * Note: Supabase client doesn't require explicit closing
   */
  async close(): Promise<void> {
    // Supabase client handles connection management automatically
    // No explicit close needed
  }

  /**
   * Get adapter type
   */
  getType(): 'supabase' {
    return 'supabase';
  }

  /**
   * Get the underlying Supabase client
   * Use this for RLS-aware queries and Supabase-specific features
   * @returns Supabase client
   */
  getClient(): SupabaseClient {
    return this.client;
  }

  /**
   * Set the auth context (user) for RLS queries
   * @param userId User ID to set in auth context
   */
  async setAuthContext(userId: string): Promise<void> {
    // This would typically be handled by setting the JWT token
    // For service role operations, you can use SET LOCAL to set session variables
    await this.query('SET LOCAL request.jwt.claim.sub = $1', [userId]);
  }
}
