/**
 * PostgreSQL database adapter using node-postgres (pg) driver
 * Used for local development and environments where Supabase is not enabled
 */

import { Pool, PoolClient, PoolConfig } from 'pg';
import { DatabaseAdapter, QueryResult, Transaction } from './base';

/**
 * PostgreSQL adapter configuration
 */
export interface PostgresAdapterConfig {
  connectionString: string;
  max?: number;
  idleTimeoutMillis?: number;
  connectionTimeoutMillis?: number;
}

/**
 * PostgreSQL adapter implementation
 */
export class PostgresAdapter implements DatabaseAdapter {
  private pool: Pool;

  /**
   * Create a new PostgreSQL adapter
   * @param config Connection configuration
   */
  constructor(config: string | PostgresAdapterConfig) {
    const poolConfig: PoolConfig = typeof config === 'string'
      ? {
        connectionString: config,
        max: 20,
        idleTimeoutMillis: 30000,
        connectionTimeoutMillis: 2000,
      }
      : {
        connectionString: config.connectionString,
        max: config.max ?? 20,
        idleTimeoutMillis: config.idleTimeoutMillis ?? 30000,
        connectionTimeoutMillis: config.connectionTimeoutMillis ?? 2000,
      };

    this.pool = new Pool(poolConfig);

    // Handle pool errors
    this.pool.on('error', (err: Error) => {
      // eslint-disable-next-line no-console
      console.error('Unexpected error on idle PostgreSQL client', err);
    });
  }

  /**
   * Execute a SQL query
   */
  async query<T>(sql: string, params?: any[]): Promise<QueryResult<T>> {
    const result = await this.pool.query(sql, params);
    return {
      rows: result.rows as T[],
      rowCount: result.rowCount ?? 0,
    };
  }

  /**
   * Begin a transaction
   */
  async beginTransaction(): Promise<Transaction> {
    const client = await this.pool.connect();
    await client.query('BEGIN');

    return new PostgresTransaction(client);
  }

  /**
   * Close all connections in the pool
   */
  async close(): Promise<void> {
    await this.pool.end();
  }

  /**
   * Get adapter type
   */
  getType(): 'postgres' {
    return 'postgres';
  }
}

/**
 * PostgreSQL transaction implementation
 */
class PostgresTransaction implements Transaction {
  private client: PoolClient;
  private isCompleted: boolean = false;

  constructor(client: PoolClient) {
    this.client = client;
  }

  /**
   * Execute a query within the transaction
   */
  async query<T>(sql: string, params?: any[]): Promise<QueryResult<T>> {
    if (this.isCompleted) {
      throw new Error('Transaction has already been completed');
    }

    const result = await this.client.query(sql, params);
    return {
      rows: result.rows as T[],
      rowCount: result.rowCount ?? 0,
    };
  }

  /**
   * Commit the transaction and release the client
   */
  async commit(): Promise<void> {
    if (this.isCompleted) {
      throw new Error('Transaction has already been completed');
    }

    try {
      await this.client.query('COMMIT');
    } finally {
      this.isCompleted = true;
      this.client.release();
    }
  }

  /**
   * Rollback the transaction and release the client
   */
  async rollback(): Promise<void> {
    if (this.isCompleted) {
      throw new Error('Transaction has already been completed');
    }

    try {
      await this.client.query('ROLLBACK');
    } finally {
      this.isCompleted = true;
      this.client.release();
    }
  }
}
