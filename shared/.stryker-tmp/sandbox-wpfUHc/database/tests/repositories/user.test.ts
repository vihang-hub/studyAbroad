/**
 * Tests for User repository
 */
// @ts-nocheck


import { describe, it, expect, beforeEach, vi } from 'vitest';
import { UserRepository } from '../../src/repositories/user';
import { DatabaseAdapter } from '../../src/adapters/base';
import { User } from '../../src/types';

describe('UserRepository', () => {
  let repository: UserRepository;
  let mockAdapter: DatabaseAdapter;

  beforeEach(() => {
    mockAdapter = {
      query: vi.fn(),
      beginTransaction: vi.fn(),
      close: vi.fn(),
      getType: vi.fn(() => 'postgres'),
    } as any;

    repository = new UserRepository(mockAdapter);
  });

  describe('findById', () => {
    it('should find user by ID', async () => {
      const mockRow = {
        user_id: 'user-123',
        clerk_user_id: 'clerk-123',
        email: 'test@example.com',
        created_at: new Date('2025-01-01'),
      };

      (mockAdapter.query as any).mockResolvedValueOnce({
        rows: [mockRow],
        rowCount: 1,
      });

      const result = await repository.findById('user-123');

      expect(mockAdapter.query).toHaveBeenCalledWith(
        'SELECT * FROM users WHERE user_id = $1',
        ['user-123'],
      );
      expect(result).toEqual({
        userId: 'user-123',
        clerkUserId: 'clerk-123',
        email: 'test@example.com',
        createdAt: new Date('2025-01-01'),
      });
    });

    it('should return null when user not found', async () => {
      (mockAdapter.query as any).mockResolvedValueOnce({
        rows: [],
        rowCount: 0,
      });

      const result = await repository.findById('nonexistent');

      expect(result).toBeNull();
    });

    it('should handle query errors', async () => {
      (mockAdapter.query as any).mockRejectedValueOnce(new Error('Database error'));

      await expect(repository.findById('user-123')).rejects.toThrow('Database error');
    });
  });

  describe('findByClerkUserId', () => {
    it('should find user by Clerk user ID', async () => {
      const mockRow = {
        user_id: 'user-123',
        clerk_user_id: 'clerk-123',
        email: 'test@example.com',
        created_at: new Date('2025-01-01'),
      };

      (mockAdapter.query as any).mockResolvedValueOnce({
        rows: [mockRow],
        rowCount: 1,
      });

      const result = await repository.findByClerkUserId('clerk-123');

      expect(mockAdapter.query).toHaveBeenCalledWith(
        'SELECT * FROM users WHERE clerk_user_id = $1',
        ['clerk-123'],
      );
      expect(result?.clerkUserId).toBe('clerk-123');
    });

    it('should return null when user not found', async () => {
      (mockAdapter.query as any).mockResolvedValueOnce({
        rows: [],
        rowCount: 0,
      });

      const result = await repository.findByClerkUserId('nonexistent');

      expect(result).toBeNull();
    });
  });

  describe('findByEmail', () => {
    it('should find user by email', async () => {
      const mockRow = {
        user_id: 'user-123',
        clerk_user_id: 'clerk-123',
        email: 'test@example.com',
        created_at: new Date('2025-01-01'),
      };

      (mockAdapter.query as any).mockResolvedValueOnce({
        rows: [mockRow],
        rowCount: 1,
      });

      const result = await repository.findByEmail('test@example.com');

      expect(mockAdapter.query).toHaveBeenCalledWith(
        'SELECT * FROM users WHERE email = $1',
        ['test@example.com'],
      );
      expect(result?.email).toBe('test@example.com');
    });

    it('should return null when user not found', async () => {
      (mockAdapter.query as any).mockResolvedValueOnce({
        rows: [],
        rowCount: 0,
      });

      const result = await repository.findByEmail('nonexistent@example.com');

      expect(result).toBeNull();
    });

    it('should handle case-sensitive email search', async () => {
      (mockAdapter.query as any).mockResolvedValueOnce({
        rows: [],
        rowCount: 0,
      });

      await repository.findByEmail('Test@Example.com');

      expect(mockAdapter.query).toHaveBeenCalledWith(
        'SELECT * FROM users WHERE email = $1',
        ['Test@Example.com'],
      );
    });
  });

  describe('create', () => {
    it('should create a new user', async () => {
      const mockRow = {
        user_id: 'user-123',
        clerk_user_id: 'clerk-123',
        email: 'test@example.com',
        created_at: new Date('2025-01-01'),
      };

      (mockAdapter.query as any).mockResolvedValueOnce({
        rows: [mockRow],
        rowCount: 1,
      });

      const result = await repository.create({
        clerkUserId: 'clerk-123',
        email: 'test@example.com',
      });

      expect(mockAdapter.query).toHaveBeenCalledWith(
        'INSERT INTO users (clerk_user_id, email)\n       VALUES ($1, $2)\n       RETURNING *',
        ['clerk-123', 'test@example.com'],
      );
      expect(result).toEqual({
        userId: 'user-123',
        clerkUserId: 'clerk-123',
        email: 'test@example.com',
        createdAt: new Date('2025-01-01'),
      });
    });

    it('should handle duplicate clerk_user_id', async () => {
      (mockAdapter.query as any).mockRejectedValueOnce(new Error('duplicate key value'));

      await expect(
        repository.create({
          clerkUserId: 'clerk-123',
          email: 'test@example.com',
        }),
      ).rejects.toThrow('duplicate key value');
    });

    it('should handle duplicate email', async () => {
      (mockAdapter.query as any).mockRejectedValueOnce(new Error('duplicate key value'));

      await expect(
        repository.create({
          clerkUserId: 'clerk-456',
          email: 'existing@example.com',
        }),
      ).rejects.toThrow('duplicate key value');
    });
  });

  describe('updateEmail', () => {
    it('should update user email', async () => {
      (mockAdapter.query as any).mockResolvedValueOnce({
        rows: [],
        rowCount: 1,
      });

      await repository.updateEmail('user-123', 'newemail@example.com');

      expect(mockAdapter.query).toHaveBeenCalledWith(
        'UPDATE users SET email = $1 WHERE user_id = $2',
        ['newemail@example.com', 'user-123'],
      );
    });

    it('should handle nonexistent user', async () => {
      (mockAdapter.query as any).mockResolvedValueOnce({
        rows: [],
        rowCount: 0,
      });

      await repository.updateEmail('nonexistent', 'newemail@example.com');

      // Should not throw, just silently fail
      expect(mockAdapter.query).toHaveBeenCalled();
    });

    it('should handle duplicate email', async () => {
      (mockAdapter.query as any).mockRejectedValueOnce(new Error('duplicate key value'));

      await expect(repository.updateEmail('user-123', 'existing@example.com')).rejects.toThrow(
        'duplicate key value',
      );
    });
  });

  describe('delete', () => {
    it('should delete user', async () => {
      (mockAdapter.query as any).mockResolvedValueOnce({
        rows: [],
        rowCount: 1,
      });

      await repository.delete('user-123');

      expect(mockAdapter.query).toHaveBeenCalledWith(
        'DELETE FROM users WHERE user_id = $1',
        ['user-123'],
      );
    });

    it('should handle nonexistent user', async () => {
      (mockAdapter.query as any).mockResolvedValueOnce({
        rows: [],
        rowCount: 0,
      });

      await repository.delete('nonexistent');

      // Should not throw
      expect(mockAdapter.query).toHaveBeenCalled();
    });

    it('should cascade delete related records', async () => {
      // This is a database-level cascade, repository just deletes the user
      (mockAdapter.query as any).mockResolvedValueOnce({
        rows: [],
        rowCount: 1,
      });

      await repository.delete('user-123');

      expect(mockAdapter.query).toHaveBeenCalledWith(
        'DELETE FROM users WHERE user_id = $1',
        ['user-123'],
      );
    });
  });

  describe('existsByClerkUserId', () => {
    it('should return true when user exists', async () => {
      (mockAdapter.query as any).mockResolvedValueOnce({
        rows: [{ exists: true }],
        rowCount: 1,
      });

      const result = await repository.existsByClerkUserId('clerk-123');

      expect(mockAdapter.query).toHaveBeenCalledWith(
        'SELECT 1 FROM users WHERE clerk_user_id = $1',
        ['clerk-123'],
      );
      expect(result).toBe(true);
    });

    it('should return false when user does not exist', async () => {
      (mockAdapter.query as any).mockResolvedValueOnce({
        rows: [],
        rowCount: 0,
      });

      const result = await repository.existsByClerkUserId('nonexistent');

      expect(result).toBe(false);
    });
  });

  describe('count', () => {
    it('should return total user count', async () => {
      (mockAdapter.query as any).mockResolvedValueOnce({
        rows: [{ count: '42' }],
        rowCount: 1,
      });

      const result = await repository.count();

      expect(mockAdapter.query).toHaveBeenCalledWith('SELECT COUNT(*) as count FROM users');
      expect(result).toBe(42);
    });

    it('should return zero when no users', async () => {
      (mockAdapter.query as any).mockResolvedValueOnce({
        rows: [{ count: '0' }],
        rowCount: 1,
      });

      const result = await repository.count();

      expect(result).toBe(0);
    });

    it('should handle large counts', async () => {
      (mockAdapter.query as any).mockResolvedValueOnce({
        rows: [{ count: '1000000' }],
        rowCount: 1,
      });

      const result = await repository.count();

      expect(result).toBe(1000000);
    });
  });
});
