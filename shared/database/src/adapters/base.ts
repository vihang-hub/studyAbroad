/**
 * Database adapter base interfaces
 * Provides abstraction over different database backends (PostgreSQL, Supabase)
 */

/**
 * Query result structure returned by all adapters
 */
export interface QueryResult<T = any> {
  rows: T[];
  rowCount: number;
}

/**
 * Transaction interface for managing database transactions
 * Note: Supabase adapter does not support manual transactions
 */
export interface Transaction {
  /**
   * Execute a query within the transaction
   */
  query<T>(sql: string, params?: any[]): Promise<QueryResult<T>>;

  /**
   * Commit the transaction
   */
  commit(): Promise<void>;

  /**
   * Rollback the transaction
   */
  rollback(): Promise<void>;
}

/**
 * Database adapter interface
 * All database adapters must implement this interface
 */
export interface DatabaseAdapter {
  /**
   * Execute a SQL query
   * @param sql SQL query string (parameterized with $1, $2, etc.)
   * @param params Query parameters
   * @returns Query result with rows and row count
   */
  query<T>(sql: string, params?: any[]): Promise<QueryResult<T>>;

  /**
   * Begin a database transaction
   * @throws Error if adapter does not support transactions (Supabase)
   * @returns Transaction object
   */
  beginTransaction(): Promise<Transaction>;

  /**
   * Close all database connections
   */
  close(): Promise<void>;

  /**
   * Get the adapter type identifier
   * @returns Adapter type
   */
  getType(): 'supabase' | 'postgres';
}
