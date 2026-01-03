/**
 * Database abstraction layer main export
 * Provides database adapters, repositories, and context
 */

import { ConfigLoader } from '@study-abroad/shared-config';
import { FeatureFlags, Feature } from '@study-abroad/shared-feature-flags';
import { DatabaseAdapter } from './adapters/base';
import { PostgresAdapter } from './adapters/postgres';
import { SupabaseAdapter } from './adapters/supabase';
import { UserRepository } from './repositories/user';
import { ReportRepository } from './repositories/report';
import { PaymentRepository } from './repositories/payment';

// Re-export all types and classes
export * from './adapters';
export * from './repositories';
export * from './types';

/**
 * Database factory function
 * Creates the appropriate database adapter based on feature flags
 * @returns DatabaseAdapter instance (PostgreSQL or Supabase)
 */
export function createDatabaseAdapter(): DatabaseAdapter {
  const config = ConfigLoader.load();

  if (FeatureFlags.isEnabled(Feature.SUPABASE)) {
    // Use Supabase in test/production mode
    if (!config.SUPABASE_URL || !config.SUPABASE_ANON_KEY) {
      throw new Error(
        'ENABLE_SUPABASE is true but Supabase configuration is missing. '
        + 'Required: SUPABASE_URL, SUPABASE_ANON_KEY',
      );
    }

    return new SupabaseAdapter({
      url: config.SUPABASE_URL,
      anonKey: config.SUPABASE_ANON_KEY,
      serviceRoleKey: config.SUPABASE_SERVICE_ROLE_KEY,
    });
  }

  // Use PostgreSQL in development mode
  if (!config.DATABASE_URL) {
    throw new Error(
      'ENABLE_SUPABASE is false but DATABASE_URL is not configured. '
      + 'Required for PostgreSQL adapter.',
    );
  }

  return new PostgresAdapter({
    connectionString: config.DATABASE_URL,
    max: config.DATABASE_POOL_MAX,
    idleTimeoutMillis: config.DATABASE_IDLE_TIMEOUT_MS,
    connectionTimeoutMillis: config.DATABASE_CONNECTION_TIMEOUT_MS,
  });
}

/**
 * Database context
 * Provides access to all repositories with a single database adapter
 */
export class DatabaseContext {
  private adapter: DatabaseAdapter;

  public users: UserRepository;
  public reports: ReportRepository;
  public payments: PaymentRepository;

  /**
   * Create a new database context
   * @param adapter Optional database adapter (for testing)
   */
  constructor(adapter?: DatabaseAdapter) {
    this.adapter = adapter ?? createDatabaseAdapter();

    // Initialize repositories
    this.users = new UserRepository(this.adapter);
    this.reports = new ReportRepository(this.adapter);
    this.payments = new PaymentRepository(this.adapter);
  }

  /**
   * Get the underlying database adapter
   */
  getAdapter(): DatabaseAdapter {
    return this.adapter;
  }

  /**
   * Close all database connections
   */
  async close(): Promise<void> {
    await this.adapter.close();
  }
}

/**
 * Singleton database context instance
 * Use this in application code
 */
export const db = new DatabaseContext();
