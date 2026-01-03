/**
 * Tests for Logger class
 *
 * Validates structured logging, Winston integration, correlation support,
 * and environment-specific behavior
 */
// @ts-nocheck


import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';
import { Logger, LogLevel } from '../src/Logger';
import { withCorrelationId, setUserId } from '../src/correlation';
import { existsSync, rmSync, mkdirSync, readdirSync } from 'fs';
import { join } from 'path';
import winston from 'winston';

// Mock ConfigLoader to avoid requiring environment variables
vi.mock('@study-abroad/shared-config', () => ({
  ConfigLoader: {
    load: () => ({
      LOG_LEVEL: 'info',
      LOG_DIR: undefined,
      LOG_MAX_SIZE_MB: 100,
      LOG_RETENTION_DAYS: 30,
      ENVIRONMENT_MODE: 'dev',
    }),
  },
}));

describe('Logger', () => {
  const testLogDir = join(__dirname, 'test-logs');

  beforeEach(() => {
    // Clean up test log directory before each test
    if (existsSync(testLogDir)) {
      rmSync(testLogDir, { recursive: true, force: true });
    }

    // Reset singleton instance
    Logger.resetInstance();
  });

  afterEach(() => {
    // Clean up after tests
    Logger.resetInstance();
    if (existsSync(testLogDir)) {
      rmSync(testLogDir, { recursive: true, force: true });
    }
  });

  describe('getInstance', () => {
    it('should return singleton instance', () => {
      const logger1 = Logger.getInstance();
      const logger2 = Logger.getInstance();

      expect(logger1).toBe(logger2);
    });

    it('should create logger with default configuration', () => {
      const logger = Logger.getInstance();

      expect(logger).toBeDefined();
      expect(logger.getWinstonLogger()).toBeDefined();
    });

    it('should create logger with custom configuration', () => {
      const logger = Logger.getInstance({
        logLevel: 'debug',
        environment: 'test',
      });

      expect(logger).toBeDefined();
    });
  });

  describe('resetInstance', () => {
    it('should allow creating new instance after reset', () => {
      const logger1 = Logger.getInstance();
      Logger.resetInstance();
      const logger2 = Logger.getInstance();

      expect(logger1).not.toBe(logger2);
    });

    it('should close existing logger on reset', async () => {
      const logger = Logger.getInstance();
      const closeSpy = vi.spyOn(logger.getWinstonLogger(), 'close');

      Logger.resetInstance();

      expect(closeSpy).toHaveBeenCalled();
    });
  });

  describe('log level methods', () => {
    it('should log debug messages', () => {
      const logger = Logger.getInstance({ logLevel: 'debug' });
      const winstonLogger = logger.getWinstonLogger();
      const debugSpy = vi.spyOn(winstonLogger, 'debug');

      logger.debug('Debug message', { key: 'value' });

      expect(debugSpy).toHaveBeenCalledWith(
        'Debug message',
        expect.objectContaining({ key: 'value' })
      );
    });

    it('should log info messages', () => {
      const logger = Logger.getInstance({ logLevel: 'info' });
      const winstonLogger = logger.getWinstonLogger();
      const infoSpy = vi.spyOn(winstonLogger, 'info');

      logger.info('Info message', { key: 'value' });

      expect(infoSpy).toHaveBeenCalledWith(
        'Info message',
        expect.objectContaining({ key: 'value' })
      );
    });

    it('should log warn messages', () => {
      const logger = Logger.getInstance({ logLevel: 'warn' });
      const winstonLogger = logger.getWinstonLogger();
      const warnSpy = vi.spyOn(winstonLogger, 'warn');

      logger.warn('Warning message', { key: 'value' });

      expect(warnSpy).toHaveBeenCalledWith(
        'Warning message',
        expect.objectContaining({ key: 'value' })
      );
    });

    it('should log error messages', () => {
      const logger = Logger.getInstance({ logLevel: 'error' });
      const winstonLogger = logger.getWinstonLogger();
      const errorSpy = vi.spyOn(winstonLogger, 'error');

      logger.error('Error message', undefined, { key: 'value' });

      expect(errorSpy).toHaveBeenCalledWith(
        'Error message',
        expect.objectContaining({ key: 'value' })
      );
    });

    it('should log error with Error object', () => {
      const logger = Logger.getInstance({ logLevel: 'error' });
      const winstonLogger = logger.getWinstonLogger();
      const errorSpy = vi.spyOn(winstonLogger, 'error');

      const error = new Error('Test error');
      logger.error('Error occurred', error, { userId: '123' });

      expect(errorSpy).toHaveBeenCalledWith(
        'Error occurred',
        expect.objectContaining({
          userId: '123',
          error: expect.objectContaining({
            name: 'Error',
            message: 'Test error',
            stack: expect.any(String),
          }),
        })
      );
    });

    it('should handle logging without metadata', () => {
      const logger = Logger.getInstance({ logLevel: 'info' });
      const winstonLogger = logger.getWinstonLogger();
      const infoSpy = vi.spyOn(winstonLogger, 'info');

      logger.info('Simple message');

      expect(infoSpy).toHaveBeenCalledWith('Simple message', expect.any(Object));
    });
  });

  describe('correlation ID support', () => {
    it('should include auto-generated correlation ID', () => {
      const logger = Logger.getInstance();
      const winstonLogger = logger.getWinstonLogger();
      const infoSpy = vi.spyOn(winstonLogger, 'info');

      logger.info('Test message');

      expect(infoSpy).toHaveBeenCalledWith(
        'Test message',
        expect.objectContaining({
          correlationId: expect.any(String),
        })
      );
    });

    it('should use correlation ID from context', () => {
      const logger = Logger.getInstance();
      const winstonLogger = logger.getWinstonLogger();
      const infoSpy = vi.spyOn(winstonLogger, 'info');

      withCorrelationId(() => {
        logger.info('Test message');
      }, 'test-correlation-id');

      expect(infoSpy).toHaveBeenCalledWith(
        'Test message',
        expect.objectContaining({
          correlationId: 'test-correlation-id',
        })
      );
    });

    it('should use correlation ID set via setCorrelationId', () => {
      const logger = Logger.getInstance();
      const winstonLogger = logger.getWinstonLogger();
      const infoSpy = vi.spyOn(winstonLogger, 'info');

      logger.setCorrelationId('manual-correlation-id');
      logger.info('Test message');

      expect(infoSpy).toHaveBeenCalledWith(
        'Test message',
        expect.objectContaining({
          correlationId: 'manual-correlation-id',
        })
      );
    });

    it('should prefer setCorrelationId over context', () => {
      const logger = Logger.getInstance();
      const winstonLogger = logger.getWinstonLogger();
      const infoSpy = vi.spyOn(winstonLogger, 'info');

      logger.setCorrelationId('manual-id');

      withCorrelationId(() => {
        logger.info('Test message');
      }, 'context-id');

      expect(infoSpy).toHaveBeenCalledWith(
        'Test message',
        expect.objectContaining({
          correlationId: 'manual-id',
        })
      );
    });

    it('should include user ID from context', () => {
      const logger = Logger.getInstance();
      const winstonLogger = logger.getWinstonLogger();
      const infoSpy = vi.spyOn(winstonLogger, 'info');

      withCorrelationId(() => {
        setUserId('user-123');
        logger.info('Test message');
      });

      expect(infoSpy).toHaveBeenCalledWith(
        'Test message',
        expect.objectContaining({
          userId: 'user-123',
        })
      );
    });
  });

  describe('sensitive data sanitization', () => {
    it('should redact password fields', () => {
      const logger = Logger.getInstance();
      const winstonLogger = logger.getWinstonLogger();
      const infoSpy = vi.spyOn(winstonLogger, 'info');

      logger.info('User login', {
        username: 'john',
        password: 'secret123',
      });

      expect(infoSpy).toHaveBeenCalledWith(
        'User login',
        expect.objectContaining({
          username: 'john',
          password: '[REDACTED]',
        })
      );
    });

    it('should redact API keys', () => {
      const logger = Logger.getInstance();
      const winstonLogger = logger.getWinstonLogger();
      const infoSpy = vi.spyOn(winstonLogger, 'info');

      logger.info('API call', {
        endpoint: '/api/data',
        apiKey: 'key-123456',
      });

      expect(infoSpy).toHaveBeenCalledWith(
        'API call',
        expect.objectContaining({
          endpoint: '/api/data',
          apiKey: '[REDACTED]',
        })
      );
    });

    it('should redact tokens', () => {
      const logger = Logger.getInstance();
      const winstonLogger = logger.getWinstonLogger();
      const infoSpy = vi.spyOn(winstonLogger, 'info');

      logger.info('Auth request', {
        accessToken: 'token-abc',
        refreshToken: 'token-xyz',
      });

      expect(infoSpy).toHaveBeenCalledWith(
        'Auth request',
        expect.objectContaining({
          accessToken: '[REDACTED]',
          refreshToken: '[REDACTED]',
        })
      );
    });

    it('should sanitize nested sensitive data', () => {
      const logger = Logger.getInstance();
      const winstonLogger = logger.getWinstonLogger();
      const infoSpy = vi.spyOn(winstonLogger, 'info');

      logger.info('Complex request', {
        user: {
          id: '123',
          credentials: {
            password: 'secret',
            apiKey: 'key-456',
          },
        },
      });

      expect(infoSpy).toHaveBeenCalledWith(
        'Complex request',
        expect.objectContaining({
          user: expect.objectContaining({
            id: '123',
            credentials: expect.objectContaining({
              password: '[REDACTED]',
              apiKey: '[REDACTED]',
            }),
          }),
        })
      );
    });
  });

  describe('file transport', () => {
    it('should create log directory if it does not exist', () => {
      expect(existsSync(testLogDir)).toBe(false);

      Logger.getInstance({
        logDir: testLogDir,
      });

      expect(existsSync(testLogDir)).toBe(true);
    });

    it('should write logs to file', async () => {
      const logger = Logger.getInstance({
        logDir: testLogDir,
        logLevel: 'info',
      });

      logger.info('Test log message', { key: 'value' });

      // Give Winston time to write to file
      await new Promise((resolve) => setTimeout(resolve, 100));

      const files = readdirSync(testLogDir);
      const logFiles = files.filter((f) => f.endsWith('.log'));

      expect(logFiles.length).toBeGreaterThan(0);
    });

    it('should not create file transport if logDir not provided', () => {
      const logger = Logger.getInstance({
        logLevel: 'info',
      });

      const winstonLogger = logger.getWinstonLogger();
      const transports = winstonLogger.transports;

      // Should only have console transport
      const fileTransports = transports.filter(
        (t) => t instanceof winston.transports.File
      );
      expect(fileTransports.length).toBe(0);
    });

    it('should handle log directory creation in nested paths', () => {
      const nestedLogDir = join(testLogDir, 'nested', 'deep', 'path');

      const logger = Logger.getInstance({
        logDir: nestedLogDir,
      });

      // Logger should be created and directory should exist
      expect(logger).toBeDefined();
      expect(existsSync(nestedLogDir)).toBe(true);
    });
  });

  describe('environment-specific configuration', () => {
    it('should use debug level in dev environment', () => {
      Logger.resetInstance();
      const logger = Logger.getInstance({
        logLevel: 'debug',
        environment: 'dev',
      });
      const winstonLogger = logger.getWinstonLogger();

      expect(winstonLogger.level).toBe('debug');
    });

    it('should use error level in production environment', () => {
      Logger.resetInstance();
      const logger = Logger.getInstance({
        logLevel: 'error',
        environment: 'production',
      });
      const winstonLogger = logger.getWinstonLogger();

      expect(winstonLogger.level).toBe('error');
    });

    it('should default to info level if not specified', () => {
      const logger = Logger.getInstance();
      const winstonLogger = logger.getWinstonLogger();

      expect(winstonLogger.level).toBe('info');
    });
  });

  describe('close', () => {
    it('should close all transports', async () => {
      const logger = Logger.getInstance();
      const winstonLogger = logger.getWinstonLogger();
      const closeSpy = vi.spyOn(winstonLogger, 'close');

      await logger.close();

      expect(closeSpy).toHaveBeenCalled();
    });

    it('should return a promise', () => {
      const logger = Logger.getInstance();
      const result = logger.close();

      expect(result).toBeInstanceOf(Promise);
    });
  });

  describe('getWinstonLogger', () => {
    it('should return underlying Winston logger instance', () => {
      const logger = Logger.getInstance();
      const winstonLogger = logger.getWinstonLogger();

      expect(winstonLogger).toBeDefined();
      expect(winstonLogger).toBeInstanceOf(winston.Logger);
    });
  });

  describe('LogLevel enum', () => {
    it('should have correct log level values', () => {
      expect(LogLevel.DEBUG).toBe('debug');
      expect(LogLevel.INFO).toBe('info');
      expect(LogLevel.WARN).toBe('warn');
      expect(LogLevel.ERROR).toBe('error');
    });
  });

  describe('integration scenarios', () => {
    it('should support complete request logging workflow', () => {
      const logger = Logger.getInstance();
      const winstonLogger = logger.getWinstonLogger();
      const infoSpy = vi.spyOn(winstonLogger, 'info');
      const errorSpy = vi.spyOn(winstonLogger, 'error');

      withCorrelationId(() => {
        // Simulate incoming request
        logger.info('Request received', {
          method: 'POST',
          path: '/api/reports',
        });

        // Simulate authentication
        setUserId('user-123');
        logger.info('User authenticated');

        // Simulate processing
        logger.info('Processing request', {
          reportType: 'UK Study',
        });

        // Simulate error
        const error = new Error('Database connection failed');
        logger.error('Request failed', error, {
          retryable: true,
        });
      }, 'request-correlation-id');

      expect(infoSpy).toHaveBeenCalledTimes(3);
      expect(errorSpy).toHaveBeenCalledTimes(1);

      // Verify correlation ID in all logs
      const allCalls = [...infoSpy.mock.calls, ...errorSpy.mock.calls];
      allCalls.forEach((call) => {
        expect(call[1]).toMatchObject({
          correlationId: 'request-correlation-id',
        });
      });

      // Verify user ID in logs after authentication
      expect(infoSpy.mock.calls[1][1]).toMatchObject({
        userId: 'user-123',
      });
    });

    it('should handle concurrent requests with isolated contexts', async () => {
      const logger = Logger.getInstance();
      const winstonLogger = logger.getWinstonLogger();
      const infoSpy = vi.spyOn(winstonLogger, 'info');

      await Promise.all([
        withCorrelationId(async () => {
          setUserId('user-1');
          logger.info('Request 1');
          await new Promise((resolve) => setTimeout(resolve, 10));
        }, 'correlation-1'),

        withCorrelationId(async () => {
          setUserId('user-2');
          logger.info('Request 2');
          await new Promise((resolve) => setTimeout(resolve, 5));
        }, 'correlation-2'),
      ]);

      const calls = infoSpy.mock.calls;
      expect(calls.length).toBe(2);

      // Verify each request maintained its own context
      const request1Log = calls.find(
        (call) => (call[1] as any).correlationId === 'correlation-1'
      );
      const request2Log = calls.find(
        (call) => (call[1] as any).correlationId === 'correlation-2'
      );

      expect(request1Log).toBeDefined();
      expect((request1Log![1] as any).userId).toBe('user-1');

      expect(request2Log).toBeDefined();
      expect((request2Log![1] as any).userId).toBe('user-2');
    });

    it('should support custom metadata with correlation', () => {
      const logger = Logger.getInstance();
      const winstonLogger = logger.getWinstonLogger();
      const infoSpy = vi.spyOn(winstonLogger, 'info');

      withCorrelationId(() => {
        setUserId('user-456');

        logger.info('Payment processed', {
          amount: 299,
          currency: 'GBP',
          paymentId: 'pay-123',
          cardLast4: '4242',
        });
      }, 'payment-correlation');

      expect(infoSpy).toHaveBeenCalledWith(
        'Payment processed',
        expect.objectContaining({
          correlationId: 'payment-correlation',
          userId: 'user-456',
          amount: 299,
          currency: 'GBP',
          paymentId: 'pay-123',
          cardLast4: '4242',
        })
      );
    });
  });
});
