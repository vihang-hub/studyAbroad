/**
 * Tests for correlation module
 *
 * Validates correlation ID propagation and context management for request tracing
 */
// @ts-nocheck


import { describe, it, expect, beforeEach } from 'vitest';
import {
  withCorrelationId,
  getCorrelationId,
  setUserId,
  getUserId,
  clearCorrelationContext,
  getCorrelationContext,
} from '../src/correlation';

describe('correlation', () => {
  beforeEach(() => {
    // Clear correlation context before each test
    clearCorrelationContext();
  });

  describe('withCorrelationId', () => {
    it('should execute function within correlation context', () => {
      let capturedId: string | undefined;

      withCorrelationId(() => {
        capturedId = getCorrelationId();
      });

      expect(capturedId).toBeDefined();
      expect(typeof capturedId).toBe('string');
      expect(capturedId?.length).toBeGreaterThan(0);
    });

    it('should auto-generate correlation ID if not provided', () => {
      const ids: string[] = [];

      withCorrelationId(() => {
        ids.push(getCorrelationId());
      });

      withCorrelationId(() => {
        ids.push(getCorrelationId());
      });

      expect(ids).toHaveLength(2);
      expect(ids[0]).not.toBe(ids[1]);
    });

    it('should use provided correlation ID', () => {
      const customId = 'custom-correlation-id';
      let capturedId: string | undefined;

      withCorrelationId(() => {
        capturedId = getCorrelationId();
      }, customId);

      expect(capturedId).toBe(customId);
    });

    it('should isolate correlation context between calls', () => {
      const id1 = 'correlation-1';
      const id2 = 'correlation-2';
      const captured: string[] = [];

      withCorrelationId(() => {
        captured.push(getCorrelationId());
      }, id1);

      withCorrelationId(() => {
        captured.push(getCorrelationId());
      }, id2);

      expect(captured[0]).toBe(id1);
      expect(captured[1]).toBe(id2);
    });

    it('should return the result of the executed function', () => {
      const result = withCorrelationId(() => 42);
      expect(result).toBe(42);

      const stringResult = withCorrelationId(() => 'test');
      expect(stringResult).toBe('test');

      const objectResult = withCorrelationId(() => ({ key: 'value' }));
      expect(objectResult).toEqual({ key: 'value' });
    });

    it('should propagate correlation ID to nested calls', () => {
      const capturedIds: string[] = [];

      withCorrelationId(() => {
        capturedIds.push(getCorrelationId());

        // Nested synchronous call
        const nestedId = getCorrelationId();
        capturedIds.push(nestedId);
      }, 'parent-id');

      expect(capturedIds).toHaveLength(2);
      expect(capturedIds[0]).toBe('parent-id');
      expect(capturedIds[1]).toBe('parent-id');
    });

    it('should handle async functions', async () => {
      const capturedIds: string[] = [];

      await withCorrelationId(async () => {
        capturedIds.push(getCorrelationId());

        await new Promise((resolve) => setTimeout(resolve, 10));

        capturedIds.push(getCorrelationId());
      }, 'async-id');

      expect(capturedIds).toHaveLength(2);
      expect(capturedIds[0]).toBe('async-id');
      expect(capturedIds[1]).toBe('async-id');
    });
  });

  describe('getCorrelationId', () => {
    it('should return correlation ID within context', () => {
      withCorrelationId(() => {
        const id = getCorrelationId();
        expect(id).toBeDefined();
        expect(typeof id).toBe('string');
      });
    });

    it('should return new UUID outside of context', () => {
      const id1 = getCorrelationId();
      const id2 = getCorrelationId();

      expect(id1).toBeDefined();
      expect(id2).toBeDefined();
      expect(id1).not.toBe(id2);
    });

    it('should return consistent ID within same context', () => {
      withCorrelationId(() => {
        const id1 = getCorrelationId();
        const id2 = getCorrelationId();
        const id3 = getCorrelationId();

        expect(id1).toBe(id2);
        expect(id2).toBe(id3);
      });
    });
  });

  describe('setUserId and getUserId', () => {
    it('should set and retrieve user ID within context', () => {
      withCorrelationId(() => {
        setUserId('user-123');
        const userId = getUserId();

        expect(userId).toBe('user-123');
      });
    });

    it('should return undefined when no user ID is set', () => {
      withCorrelationId(() => {
        const userId = getUserId();
        expect(userId).toBeUndefined();
      });
    });

    it('should return undefined outside of context', () => {
      setUserId('user-456');
      const userId = getUserId();
      expect(userId).toBeUndefined();
    });

    it('should isolate user ID between contexts', () => {
      const userIds: Array<string | undefined> = [];

      withCorrelationId(() => {
        setUserId('user-1');
        userIds.push(getUserId());
      });

      withCorrelationId(() => {
        setUserId('user-2');
        userIds.push(getUserId());
      });

      expect(userIds[0]).toBe('user-1');
      expect(userIds[1]).toBe('user-2');
    });

    it('should allow updating user ID within same context', () => {
      withCorrelationId(() => {
        setUserId('user-initial');
        expect(getUserId()).toBe('user-initial');

        setUserId('user-updated');
        expect(getUserId()).toBe('user-updated');
      });
    });

    it('should persist user ID across async operations', async () => {
      await withCorrelationId(async () => {
        setUserId('user-async');

        await new Promise((resolve) => setTimeout(resolve, 10));

        const userId = getUserId();
        expect(userId).toBe('user-async');
      });
    });
  });

  describe('getCorrelationContext', () => {
    it('should return empty object outside of context', () => {
      const context = getCorrelationContext();
      expect(context).toEqual({});
    });

    it('should return correlation ID in context', () => {
      withCorrelationId(() => {
        const context = getCorrelationContext();

        expect(context.correlationId).toBeDefined();
        expect(typeof context.correlationId).toBe('string');
      }, 'test-id');
    });

    it('should include user ID when set', () => {
      withCorrelationId(() => {
        setUserId('user-789');
        const context = getCorrelationContext();

        expect(context.correlationId).toBeDefined();
        expect(context.userId).toBe('user-789');
      });
    });

    it('should return all context data', () => {
      withCorrelationId(() => {
        setUserId('context-user');
        const context = getCorrelationContext();

        expect(Object.keys(context)).toContain('correlationId');
        expect(Object.keys(context)).toContain('userId');
        expect(context.correlationId).toBe('context-correlation');
        expect(context.userId).toBe('context-user');
      }, 'context-correlation');
    });
  });

  describe('clearCorrelationContext', () => {
    it('should clear user ID when called within context', () => {
      withCorrelationId(() => {
        setUserId('user-to-clear');
        expect(getUserId()).toBe('user-to-clear');

        clearCorrelationContext();

        // After clearing, correlation ID still exists but user ID is gone
        const userId = getUserId();
        expect(userId).toBeUndefined();
      });
    });

    it('should not affect other contexts', () => {
      const capturedUserIds: Array<string | undefined> = [];

      withCorrelationId(() => {
        setUserId('user-1');
        capturedUserIds.push(getUserId());
      });

      withCorrelationId(() => {
        setUserId('user-2');
        clearCorrelationContext();
        capturedUserIds.push(getUserId());
      });

      withCorrelationId(() => {
        setUserId('user-3');
        capturedUserIds.push(getUserId());
      });

      expect(capturedUserIds[0]).toBe('user-1');
      expect(capturedUserIds[1]).toBeUndefined();
      expect(capturedUserIds[2]).toBe('user-3');
    });

    it('should handle being called outside of context', () => {
      // Should not throw error
      expect(() => clearCorrelationContext()).not.toThrow();
    });
  });

  describe('integration scenarios', () => {
    it('should support HTTP request simulation', () => {
      // Simulate incoming HTTP request with correlation ID from header
      const incomingCorrelationId = 'req-from-client';

      withCorrelationId(() => {
        // Simulate extracting user from JWT token
        setUserId('authenticated-user-123');

        // Simulate logging during request processing
        const context = getCorrelationContext();

        expect(context.correlationId).toBe(incomingCorrelationId);
        expect(context.userId).toBe('authenticated-user-123');

        // Simulate nested service calls maintaining context
        const nestedContext = getCorrelationContext();
        expect(nestedContext.correlationId).toBe(incomingCorrelationId);
        expect(nestedContext.userId).toBe('authenticated-user-123');
      }, incomingCorrelationId);
    });

    it('should support multiple concurrent contexts', async () => {
      const results: Array<{ correlationId: string; userId: string | undefined }> = [];

      // Simulate multiple concurrent requests
      const promises = [
        withCorrelationId(async () => {
          setUserId('user-1');
          await new Promise((resolve) => setTimeout(resolve, 10));
          results.push({
            correlationId: getCorrelationId(),
            userId: getUserId(),
          });
        }, 'correlation-1'),

        withCorrelationId(async () => {
          setUserId('user-2');
          await new Promise((resolve) => setTimeout(resolve, 5));
          results.push({
            correlationId: getCorrelationId(),
            userId: getUserId(),
          });
        }, 'correlation-2'),

        withCorrelationId(async () => {
          setUserId('user-3');
          await new Promise((resolve) => setTimeout(resolve, 15));
          results.push({
            correlationId: getCorrelationId(),
            userId: getUserId(),
          });
        }, 'correlation-3'),
      ];

      await Promise.all(promises);

      // Verify each context maintained its own correlation ID and user ID
      expect(results).toHaveLength(3);

      const correlation1 = results.find((r) => r.correlationId === 'correlation-1');
      const correlation2 = results.find((r) => r.correlationId === 'correlation-2');
      const correlation3 = results.find((r) => r.correlationId === 'correlation-3');

      expect(correlation1?.userId).toBe('user-1');
      expect(correlation2?.userId).toBe('user-2');
      expect(correlation3?.userId).toBe('user-3');
    });

    it('should support unauthenticated requests (no user ID)', () => {
      withCorrelationId(() => {
        // No setUserId called (unauthenticated request)
        const context = getCorrelationContext();

        expect(context.correlationId).toBeDefined();
        expect(context.userId).toBeUndefined();
      });
    });

    it('should support late authentication (user ID set after correlation)', () => {
      withCorrelationId(() => {
        // Initial request without authentication
        let context = getCorrelationContext();
        expect(context.userId).toBeUndefined();

        // User authenticates mid-request
        setUserId('late-auth-user');

        // Context now includes user ID
        context = getCorrelationContext();
        expect(context.userId).toBe('late-auth-user');
      });
    });
  });
});
