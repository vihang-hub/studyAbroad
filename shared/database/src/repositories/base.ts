/**
 * Base repository classes providing common database operations
 */

import { DatabaseAdapter } from '../adapters/base';
import { SoftDeletable } from '../types';

/**
 * Base repository class
 * All repositories should extend this class
 */
export abstract class BaseRepository {
  protected db: DatabaseAdapter;

  constructor(db: DatabaseAdapter) {
    this.db = db;
  }

  /**
   * Check if using Supabase adapter
   * Useful for adapter-specific logic (e.g., RLS)
   */
  protected isSupabase(): boolean {
    return this.db.getType() === 'supabase';
  }
}

/**
 * Soft delete repository interface
 */
export interface SoftDeleteRepository<T extends SoftDeletable> {
  softDelete(id: string, userId: string): Promise<void>;
  restore(id: string, userId: string): Promise<void>;
  findByIdIncludingDeleted(id: string, userId: string): Promise<T | null>;
  isDeleted(entity: T): boolean;
}

/**
 * Base repository with soft delete support
 */
export abstract class SoftDeleteBaseRepository<T extends SoftDeletable>
  extends BaseRepository
  implements SoftDeleteRepository<T>
{
  protected abstract tableName: string;
  protected abstract idField: string;

  /**
   * Soft delete an entity
   * Sets deletedAt to current timestamp
   */
  async softDelete(id: string, userId: string): Promise<void> {
    await this.db.query(
      `UPDATE ${this.tableName}
       SET deleted_at = NOW()
       WHERE ${this.idField} = $1
         AND user_id = $2
         AND deleted_at IS NULL`,
      [id, userId],
    );
  }

  /**
   * Restore a soft-deleted entity
   * Sets deletedAt to NULL
   */
  async restore(id: string, userId: string): Promise<void> {
    await this.db.query(
      `UPDATE ${this.tableName}
       SET deleted_at = NULL
       WHERE ${this.idField} = $1
         AND user_id = $2
         AND deleted_at IS NOT NULL`,
      [id, userId],
    );
  }

  /**
   * Find entity by ID including soft-deleted records
   */
  abstract findByIdIncludingDeleted(id: string, userId: string): Promise<T | null>;

  /**
   * Check if an entity is soft-deleted
   */
  isDeleted(entity: T): boolean {
    return entity.deletedAt !== null;
  }

  /**
   * Get WHERE clause for filtering out soft-deleted records
   * Use in SQL queries: WHERE ${this.whereActive()}
   */
  protected whereActive(): string {
    return 'deleted_at IS NULL';
  }

  /**
   * Get WHERE clause for soft-deleted records only
   */
  protected whereDeleted(): string {
    return 'deleted_at IS NOT NULL';
  }
}
