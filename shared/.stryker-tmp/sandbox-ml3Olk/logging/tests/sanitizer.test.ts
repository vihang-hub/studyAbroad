/**
 * Tests for sanitizer module
 *
 * Validates that sensitive data is properly redacted from log entries
 * to prevent data leakage (NIST CSF 2.0 PR.DS-5)
 */
// @ts-nocheck


import { describe, it, expect } from 'vitest';
import { sanitizeLogData, isPlainObject } from '../src/sanitizer';

describe('sanitizer', () => {
  describe('sanitizeLogData', () => {
    it('should return primitive values unchanged', () => {
      expect(sanitizeLogData('test')).toBe('test');
      expect(sanitizeLogData(123)).toBe(123);
      expect(sanitizeLogData(true)).toBe(true);
      expect(sanitizeLogData(false)).toBe(false);
    });

    it('should return null and undefined unchanged', () => {
      expect(sanitizeLogData(null)).toBe(null);
      expect(sanitizeLogData(undefined)).toBe(undefined);
    });

    it('should redact password fields (case-insensitive)', () => {
      const data = {
        username: 'john',
        password: 'secret123',
        PASSWORD: 'secret456',
        userPassword: 'secret789',
      };

      const sanitized = sanitizeLogData(data) as Record<string, unknown>;

      expect(sanitized.username).toBe('john');
      expect(sanitized.password).toBe('[REDACTED]');
      expect(sanitized.PASSWORD).toBe('[REDACTED]');
      expect(sanitized.userPassword).toBe('[REDACTED]');
    });

    it('should redact token fields', () => {
      const data = {
        accessToken: 'token-123',
        refreshToken: 'refresh-456',
        bearer_token: 'bearer-789',
        apiToken: 'api-token-abc',
      };

      const sanitized = sanitizeLogData(data) as Record<string, unknown>;

      expect(sanitized.accessToken).toBe('[REDACTED]');
      expect(sanitized.refreshToken).toBe('[REDACTED]');
      expect(sanitized.bearer_token).toBe('[REDACTED]');
      expect(sanitized.apiToken).toBe('[REDACTED]');
    });

    it('should redact API key fields', () => {
      const data = {
        apiKey: 'key-123',
        api_key: 'key-456',
        API_KEY: 'key-789',
        apikey: 'key-abc',
      };

      const sanitized = sanitizeLogData(data) as Record<string, unknown>;

      expect(sanitized.apiKey).toBe('[REDACTED]');
      expect(sanitized.api_key).toBe('[REDACTED]');
      expect(sanitized.API_KEY).toBe('[REDACTED]');
      expect(sanitized.apikey).toBe('[REDACTED]');
    });

    it('should redact secret fields', () => {
      const data = {
        secret: 'my-secret',
        clientSecret: 'client-secret-123',
        SECRET_KEY: 'secret-key-456',
      };

      const sanitized = sanitizeLogData(data) as Record<string, unknown>;

      expect(sanitized.secret).toBe('[REDACTED]');
      expect(sanitized.clientSecret).toBe('[REDACTED]');
      expect(sanitized.SECRET_KEY).toBe('[REDACTED]');
    });

    it('should redact authorization fields', () => {
      const data = {
        authorization: 'Bearer token',
        Authorization: 'Bearer token',
        auth: 'auth-data',
      };

      const sanitized = sanitizeLogData(data) as Record<string, unknown>;

      expect(sanitized.authorization).toBe('[REDACTED]');
      expect(sanitized.Authorization).toBe('[REDACTED]');
      expect(sanitized.auth).toBe('[REDACTED]');
    });

    it('should redact cookie and session fields', () => {
      const data = {
        cookie: 'session-cookie',
        cookies: 'all-cookies',
        session: 'session-id',
        sessionId: 'session-123',
      };

      const sanitized = sanitizeLogData(data) as Record<string, unknown>;

      expect(sanitized.cookie).toBe('[REDACTED]');
      expect(sanitized.cookies).toBe('[REDACTED]');
      expect(sanitized.session).toBe('[REDACTED]');
      expect(sanitized.sessionId).toBe('[REDACTED]');
    });

    it('should redact sensitive personal information', () => {
      const data = {
        ssn: '123-45-6789',
        socialSecurity: '987-65-4321',
        creditCard: '4111-1111-1111-1111',
        cardNumber: '5555-5555-5555-4444',
        cvv: '123',
        pin: '1234',
      };

      const sanitized = sanitizeLogData(data) as Record<string, unknown>;

      expect(sanitized.ssn).toBe('[REDACTED]');
      expect(sanitized.socialSecurity).toBe('[REDACTED]');
      expect(sanitized.creditCard).toBe('[REDACTED]');
      expect(sanitized.cardNumber).toBe('[REDACTED]');
      expect(sanitized.cvv).toBe('[REDACTED]');
      expect(sanitized.pin).toBe('[REDACTED]');
    });

    it('should redact private key fields', () => {
      const data = {
        privateKey: 'private-key-data',
        private_key: 'another-private-key',
      };

      const sanitized = sanitizeLogData(data) as Record<string, unknown>;

      expect(sanitized.privateKey).toBe('[REDACTED]');
      expect(sanitized.private_key).toBe('[REDACTED]');
    });

    it('should recursively sanitize nested objects', () => {
      const data = {
        user: {
          username: 'john',
          password: 'secret123',
          profile: {
            email: 'john@example.com',
            apiKey: 'key-123',
          },
        },
      };

      const sanitized = sanitizeLogData(data) as Record<string, unknown>;
      const user = sanitized.user as Record<string, unknown>;
      const profile = user.profile as Record<string, unknown>;

      expect(user.username).toBe('john');
      expect(user.password).toBe('[REDACTED]');
      expect(profile.email).toBe('john@example.com');
      expect(profile.apiKey).toBe('[REDACTED]');
    });

    it('should sanitize arrays of objects', () => {
      const data = {
        users: [
          { username: 'john', password: 'secret1' },
          { username: 'jane', password: 'secret2' },
        ],
      };

      const sanitized = sanitizeLogData(data) as Record<string, unknown>;
      const users = sanitized.users as Array<Record<string, unknown>>;

      expect(users[0].username).toBe('john');
      expect(users[0].password).toBe('[REDACTED]');
      expect(users[1].username).toBe('jane');
      expect(users[1].password).toBe('[REDACTED]');
    });

    it('should handle arrays of primitives', () => {
      const data = {
        numbers: [1, 2, 3],
        strings: ['a', 'b', 'c'],
      };

      const sanitized = sanitizeLogData(data) as Record<string, unknown>;

      expect(sanitized.numbers).toEqual([1, 2, 3]);
      expect(sanitized.strings).toEqual(['a', 'b', 'c']);
    });

    it('should preserve Error objects with stack traces', () => {
      const error = new Error('Test error');
      const data = { error };

      const sanitized = sanitizeLogData(data) as Record<string, unknown>;
      const sanitizedError = sanitized.error as Record<string, unknown>;

      expect(sanitizedError.name).toBe('Error');
      expect(sanitizedError.message).toBe('Test error');
      expect(sanitizedError.stack).toBeDefined();
      expect(typeof sanitizedError.stack).toBe('string');
    });

    it('should preserve Date objects', () => {
      const date = new Date('2025-01-01T00:00:00Z');
      const data = { timestamp: date };

      const sanitized = sanitizeLogData(data) as Record<string, unknown>;

      expect(sanitized.timestamp).toBe(date);
    });

    it('should handle complex nested structures with deep nesting', () => {
      const data = {
        level1: {
          level2: {
            level3: {
              username: 'john',
              password: 'secret',
              publicData: 'safe',
            },
          },
        },
      };

      const sanitized = sanitizeLogData(data) as Record<string, unknown>;
      const level1 = sanitized.level1 as Record<string, unknown>;
      const level2 = level1.level2 as Record<string, unknown>;
      const level3 = level2.level3 as Record<string, unknown>;

      expect(level3.username).toBe('john');
      expect(level3.password).toBe('[REDACTED]');
      expect(level3.publicData).toBe('safe');
    });

    it('should sanitize arrays containing sensitive objects', () => {
      const data = {
        items: [
          { id: 1, apiKey: 'key-1', name: 'item1' },
          { id: 2, apiKey: 'key-2', name: 'item2' },
        ],
      };

      const sanitized = sanitizeLogData(data) as Record<string, unknown>;
      const items = sanitized.items as Array<Record<string, unknown>>;

      expect(Array.isArray(items)).toBe(true);
      expect(items.length).toBe(2);
      expect(items[0].id).toBe(1);
      expect(items[0].apiKey).toBe('[REDACTED]');
      expect(items[0].name).toBe('item1');
      expect(items[1].id).toBe(2);
      expect(items[1].apiKey).toBe('[REDACTED]');
      expect(items[1].name).toBe('item2');
    });

    it('should handle empty objects and arrays', () => {
      const data = {
        emptyObject: {},
        emptyArray: [],
      };

      const sanitized = sanitizeLogData(data) as Record<string, unknown>;

      expect(sanitized.emptyObject).toEqual({});
      expect(sanitized.emptyArray).toEqual([]);
    });

    it('should not modify non-sensitive fields', () => {
      const data = {
        userId: '123',
        email: 'test@example.com',
        requestId: 'req-456',
        timestamp: '2025-01-01T00:00:00Z',
        count: 42,
        active: true,
      };

      const sanitized = sanitizeLogData(data) as Record<string, unknown>;

      expect(sanitized).toEqual(data);
    });

    it('should handle mixed sensitive and non-sensitive fields', () => {
      const data = {
        userId: '123',
        password: 'secret',
        email: 'test@example.com',
        apiKey: 'key-123',
        requestId: 'req-456',
      };

      const sanitized = sanitizeLogData(data) as Record<string, unknown>;

      expect(sanitized.userId).toBe('123');
      expect(sanitized.password).toBe('[REDACTED]');
      expect(sanitized.email).toBe('test@example.com');
      expect(sanitized.apiKey).toBe('[REDACTED]');
      expect(sanitized.requestId).toBe('req-456');
    });

    it('should handle passwd and pwd variations', () => {
      const data = {
        passwd: 'secret1',
        pwd: 'secret2',
        userPasswd: 'secret3',
      };

      const sanitized = sanitizeLogData(data) as Record<string, unknown>;

      expect(sanitized.passwd).toBe('[REDACTED]');
      expect(sanitized.pwd).toBe('[REDACTED]');
      expect(sanitized.userPasswd).toBe('[REDACTED]');
    });
  });

  describe('isPlainObject', () => {
    it('should return true for plain objects', () => {
      expect(isPlainObject({})).toBe(true);
      expect(isPlainObject({ key: 'value' })).toBe(true);
      expect(isPlainObject({ nested: { key: 'value' } })).toBe(true);
    });

    it('should return false for null', () => {
      expect(isPlainObject(null)).toBe(false);
    });

    it('should return false for undefined', () => {
      expect(isPlainObject(undefined)).toBe(false);
    });

    it('should return false for arrays', () => {
      expect(isPlainObject([])).toBe(false);
      expect(isPlainObject([1, 2, 3])).toBe(false);
    });

    it('should return false for Date objects', () => {
      expect(isPlainObject(new Date())).toBe(false);
    });

    it('should return false for Error objects', () => {
      expect(isPlainObject(new Error('test'))).toBe(false);
    });

    it('should return false for primitive types', () => {
      expect(isPlainObject('string')).toBe(false);
      expect(isPlainObject(123)).toBe(false);
      expect(isPlainObject(true)).toBe(false);
    });
  });
});
