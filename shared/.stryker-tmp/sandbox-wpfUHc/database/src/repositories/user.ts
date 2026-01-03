/**
 * User repository
 * Handles user CRUD operations
 */
// @ts-nocheck


import { BaseRepository } from './base';
import { User, mapToUser } from '../types';

/**
 * User repository implementation
 * Note: Users table does not have soft delete
 */
export class UserRepository extends BaseRepository {
  /**
   * Find user by ID
   */
  async findById(userId: string): Promise<User | null> {
    const { rows } = await this.db.query<any>(
      'SELECT * FROM users WHERE user_id = $1',
      [userId],
    );

    return rows[0] ? mapToUser(rows[0]) : null;
  }

  /**
   * Find user by Clerk user ID
   */
  async findByClerkUserId(clerkUserId: string): Promise<User | null> {
    const { rows } = await this.db.query<any>(
      'SELECT * FROM users WHERE clerk_user_id = $1',
      [clerkUserId],
    );

    return rows[0] ? mapToUser(rows[0]) : null;
  }

  /**
   * Find user by email
   */
  async findByEmail(email: string): Promise<User | null> {
    const { rows } = await this.db.query<any>(
      'SELECT * FROM users WHERE email = $1',
      [email],
    );

    return rows[0] ? mapToUser(rows[0]) : null;
  }

  /**
   * Create a new user
   */
  async create(data: {
    clerkUserId: string;
    email: string;
  }): Promise<User> {
    const { rows } = await this.db.query<any>(
      `INSERT INTO users (clerk_user_id, email)
       VALUES ($1, $2)
       RETURNING *`,
      [data.clerkUserId, data.email],
    );

    return mapToUser(rows[0]);
  }

  /**
   * Update user email
   */
  async updateEmail(userId: string, email: string): Promise<void> {
    await this.db.query(
      'UPDATE users SET email = $1 WHERE user_id = $2',
      [email, userId],
    );
  }

  /**
   * Delete user (hard delete)
   * Note: This is a hard delete, not soft delete
   * Should only be used for GDPR compliance or account deletion
   */
  async delete(userId: string): Promise<void> {
    await this.db.query('DELETE FROM users WHERE user_id = $1', [userId]);
  }

  /**
   * Check if user exists by Clerk ID
   */
  async existsByClerkUserId(clerkUserId: string): Promise<boolean> {
    const { rowCount } = await this.db.query(
      'SELECT 1 FROM users WHERE clerk_user_id = $1',
      [clerkUserId],
    );

    return rowCount > 0;
  }

  /**
   * Count total users
   */
  async count(): Promise<number> {
    const { rows } = await this.db.query<{ count: string }>(
      'SELECT COUNT(*) as count FROM users',
    );

    return parseInt(rows[0].count, 10);
  }
}
