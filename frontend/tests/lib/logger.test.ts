/**
 * Tests for logger utility
 * Coverage target: 100% (high-impact file: ~10-12% total frontend coverage)
 */

import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import {
  initializeLogger,
  getLogger,
  logDebug,
  logInfo,
  logWarn,
  logError,
  logApiRequest,
  logApiResponse,
  logApiError,
  logUserAction,
  logPageView,
  setLoggerUserId,
  createChildLogger,
  type Logger,
} from '../../src/lib/logger';

// Mock dependencies
const mockGetConfig = vi.fn();
const mockIsDevelopment = vi.fn();

const mockConfig = {
  apiUrl: 'http://localhost:8000',
  logLevel: 'info',
  mode: 'test',
  environment: 'test',
};

vi.mock('../../src/lib/config', () => ({
  getConfig: () => mockGetConfig(),
  isDevelopment: () => mockIsDevelopment(),
}));

// Mock console methods
const consoleDebugSpy = vi.spyOn(console, 'debug').mockImplementation(() => {});
const consoleInfoSpy = vi.spyOn(console, 'info').mockImplementation(() => {});
const consoleWarnSpy = vi.spyOn(console, 'warn').mockImplementation(() => {});
const consoleErrorSpy = vi.spyOn(console, 'error').mockImplementation(() => {});
const consoleLogSpy = vi.spyOn(console, 'log').mockImplementation(() => {});

describe('logger', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    mockGetConfig.mockReturnValue(mockConfig);
    mockIsDevelopment.mockReturnValue(false);
    // Reset the logger instance between tests
    // Note: This is a workaround since we can't directly reset the singleton
  });

  afterEach(() => {
    vi.clearAllMocks();
  });

  describe('initializeLogger', () => {
    it('should initialize and return a logger instance', () => {
      const logger = initializeLogger();

      expect(logger).toBeDefined();
      expect(logger.debug).toBeInstanceOf(Function);
      expect(logger.info).toBeInstanceOf(Function);
      expect(logger.warn).toBeInstanceOf(Function);
      expect(logger.error).toBeInstanceOf(Function);
    });

    it('should return the same instance on multiple calls', () => {
      const logger1 = initializeLogger();
      const logger2 = initializeLogger();

      expect(logger1).toBe(logger2);
    });

    it('should not log initialization message in non-development mode', () => {
      mockIsDevelopment.mockReturnValue(false);

      initializeLogger();

      // Should not log in test mode
      expect(consoleLogSpy).not.toHaveBeenCalledWith(
        expect.stringContaining('[Logger] Logger initialized'),
        expect.any(Object)
      );
    });

    it('should log initialization message in development mode', async () => {
      mockIsDevelopment.mockReturnValue(true);

      // Reset modules to get fresh logger instance
      vi.resetModules();
      const { initializeLogger: freshInit } = await import('../../src/lib/logger');

      freshInit();

      expect(consoleLogSpy).toHaveBeenCalledWith(
        expect.stringContaining('[Logger] Logger initialized'),
        expect.objectContaining({
          level: expect.any(String),
          environment: expect.any(String),
        })
      );
    });
  });

  describe('getLogger', () => {
    it('should return existing logger instance', () => {
      const logger = getLogger();

      expect(logger).toBeDefined();
      expect(logger.debug).toBeInstanceOf(Function);
    });

    it('should auto-initialize if logger not initialized', () => {
      const logger = getLogger();

      expect(logger).toBeDefined();
    });
  });

  describe('Logger methods', () => {
    describe('debug', () => {
      it('should log debug message with metadata when log level is debug', () => {
        const debugConfig = { ...mockConfig, logLevel: 'debug' };
        mockGetConfig.mockReturnValue(debugConfig);
        mockIsDevelopment.mockReturnValue(false);

        const logger = getLogger();
        const metadata = { userId: '123', action: 'test' };

        logger.debug('Debug message', metadata);

        expect(consoleDebugSpy).toHaveBeenCalledWith(
          '[DEBUG] Debug message',
          metadata
        );
      });

      it('should log debug message in development mode', () => {
        mockGetConfig.mockReturnValue({ ...mockConfig, logLevel: 'info' });
        mockIsDevelopment.mockReturnValue(true);

        const logger = getLogger();
        logger.debug('Dev debug message');

        expect(consoleDebugSpy).toHaveBeenCalledWith(
          '[DEBUG] Dev debug message',
          {}
        );
      });

      it('should not log debug message in production with info level', () => {
        mockGetConfig.mockReturnValue({ ...mockConfig, logLevel: 'info' });
        mockIsDevelopment.mockReturnValue(false);

        consoleDebugSpy.mockClear();

        const logger = getLogger();
        logger.debug('Should not appear');

        expect(consoleDebugSpy).not.toHaveBeenCalled();
      });

      it('should handle debug without metadata', () => {
        mockGetConfig.mockReturnValue({ ...mockConfig, logLevel: 'debug' });

        const logger = getLogger();
        logger.debug('Debug without metadata');

        expect(consoleDebugSpy).toHaveBeenCalledWith(
          '[DEBUG] Debug without metadata',
          {}
        );
      });
    });

    describe('info', () => {
      it('should log info message with metadata', () => {
        const logger = getLogger();
        const metadata = { correlationId: 'abc123' };

        logger.info('Info message', metadata);

        expect(consoleInfoSpy).toHaveBeenCalledWith(
          '[INFO] Info message',
          metadata
        );
      });

      it('should log info without metadata', () => {
        const logger = getLogger();

        logger.info('Simple info');

        expect(consoleInfoSpy).toHaveBeenCalledWith('[INFO] Simple info', {});
      });
    });

    describe('warn', () => {
      it('should log warning message with metadata', () => {
        const logger = getLogger();
        const metadata = { warningType: 'deprecation' };

        logger.warn('Warning message', metadata);

        expect(consoleWarnSpy).toHaveBeenCalledWith(
          '[WARN] Warning message',
          metadata
        );
      });

      it('should log warning without metadata', () => {
        const logger = getLogger();

        logger.warn('Simple warning');

        expect(consoleWarnSpy).toHaveBeenCalledWith('[WARN] Simple warning', {});
      });
    });

    describe('error', () => {
      it('should log error message with Error object and metadata', () => {
        const logger = getLogger();
        const error = new Error('Test error');
        const metadata = { context: 'test' };

        logger.error('Error occurred', error, metadata);

        expect(consoleErrorSpy).toHaveBeenCalledWith(
          '[ERROR] Error occurred',
          error,
          metadata
        );
      });

      it('should log error without Error object', () => {
        const logger = getLogger();

        logger.error('Error message');

        expect(consoleErrorSpy).toHaveBeenCalledWith(
          '[ERROR] Error message',
          undefined,
          {}
        );
      });

      it('should log error with unknown error type', () => {
        const logger = getLogger();
        const unknownError = 'String error';

        logger.error('Unknown error', unknownError);

        expect(consoleErrorSpy).toHaveBeenCalledWith(
          '[ERROR] Unknown error',
          unknownError,
          {}
        );
      });

      it('should handle error with metadata but no error object', () => {
        const logger = getLogger();
        const metadata = { userId: '456' };

        logger.error('Error with metadata', undefined, metadata);

        expect(consoleErrorSpy).toHaveBeenCalledWith(
          '[ERROR] Error with metadata',
          undefined,
          metadata
        );
      });
    });
  });

  describe('Helper functions', () => {
    describe('logDebug', () => {
      it('should call logger.debug', () => {
        mockGetConfig.mockReturnValue({ ...mockConfig, logLevel: 'debug' });

        logDebug('Debug via helper', { test: true });

        expect(consoleDebugSpy).toHaveBeenCalledWith(
          '[DEBUG] Debug via helper',
          { test: true }
        );
      });
    });

    describe('logInfo', () => {
      it('should call logger.info', () => {
        logInfo('Info via helper', { test: true });

        expect(consoleInfoSpy).toHaveBeenCalledWith(
          '[INFO] Info via helper',
          { test: true }
        );
      });
    });

    describe('logWarn', () => {
      it('should call logger.warn', () => {
        logWarn('Warn via helper', { test: true });

        expect(consoleWarnSpy).toHaveBeenCalledWith(
          '[WARN] Warn via helper',
          { test: true }
        );
      });
    });

    describe('logError', () => {
      it('should call logger.error with error', () => {
        const error = new Error('Helper error');

        logError('Error via helper', error, { test: true });

        expect(consoleErrorSpy).toHaveBeenCalledWith(
          '[ERROR] Error via helper',
          error,
          { test: true }
        );
      });

      it('should call logger.error without error object', () => {
        logError('Error message only');

        expect(consoleErrorSpy).toHaveBeenCalledWith(
          '[ERROR] Error message only',
          undefined,
          {}
        );
      });
    });
  });

  describe('API logging functions', () => {
    describe('logApiRequest', () => {
      it('should log API request with method and URL', () => {
        logApiRequest('GET', '/api/users');

        expect(consoleInfoSpy).toHaveBeenCalledWith(
          '[INFO] API Request: GET /api/users',
          expect.objectContaining({
            method: 'GET',
            url: '/api/users',
            type: 'api_request',
          })
        );
      });

      it('should include correlation ID in metadata', () => {
        logApiRequest('POST', '/api/posts', { correlationId: 'req-123' });

        expect(consoleInfoSpy).toHaveBeenCalledWith(
          '[INFO] API Request: POST /api/posts',
          expect.objectContaining({
            method: 'POST',
            url: '/api/posts',
            correlationId: expect.any(String),
            type: 'api_request',
          })
        );
      });

      it('should merge additional metadata', () => {
        logApiRequest('DELETE', '/api/items/1', { userId: 'user-456' });

        expect(consoleInfoSpy).toHaveBeenCalledWith(
          '[INFO] API Request: DELETE /api/items/1',
          expect.objectContaining({
            method: 'DELETE',
            url: '/api/items/1',
            userId: 'user-456',
            type: 'api_request',
          })
        );
      });
    });

    describe('logApiResponse', () => {
      it('should log successful API response as info', () => {
        logApiResponse('GET', '/api/users', 200, 150);

        expect(consoleInfoSpy).toHaveBeenCalledWith(
          '[INFO] API Response: GET /api/users 200',
          expect.objectContaining({
            method: 'GET',
            url: '/api/users',
            status: 200,
            duration: 150,
            type: 'api_response',
          })
        );
      });

      it('should log 4xx response as error', () => {
        logApiResponse('POST', '/api/posts', 400, 100);

        expect(consoleErrorSpy).toHaveBeenCalledWith(
          '[ERROR] API Response: POST /api/posts 400',
          undefined,
          expect.objectContaining({
            method: 'POST',
            url: '/api/posts',
            status: 400,
            duration: 100,
            type: 'api_response',
          })
        );
      });

      it('should log 5xx response as error', () => {
        logApiResponse('GET', '/api/error', 500, 200);

        expect(consoleErrorSpy).toHaveBeenCalledWith(
          '[ERROR] API Response: GET /api/error 500',
          undefined,
          expect.objectContaining({
            status: 500,
            type: 'api_response',
          })
        );
      });

      it('should include additional metadata', () => {
        logApiResponse('PATCH', '/api/items/1', 204, 80, {
          userId: 'user-789',
        });

        expect(consoleInfoSpy).toHaveBeenCalledWith(
          '[INFO] API Response: PATCH /api/items/1 204',
          expect.objectContaining({
            method: 'PATCH',
            url: '/api/items/1',
            status: 204,
            duration: 80,
            userId: 'user-789',
          })
        );
      });

      it('should distinguish between 3xx and 4xx status codes', () => {
        consoleInfoSpy.mockClear();
        consoleErrorSpy.mockClear();

        logApiResponse('GET', '/redirect', 301, 50);
        expect(consoleInfoSpy).toHaveBeenCalled();
        expect(consoleErrorSpy).not.toHaveBeenCalled();

        consoleInfoSpy.mockClear();
        logApiResponse('GET', '/not-found', 404, 50);
        expect(consoleErrorSpy).toHaveBeenCalled();
      });
    });

    describe('logApiError', () => {
      it('should log API error with Error object', () => {
        const error = new Error('Network failure');

        logApiError('GET', '/api/users', error);

        expect(consoleErrorSpy).toHaveBeenCalledWith(
          '[ERROR] API Error: GET /api/users',
          error,
          expect.objectContaining({
            method: 'GET',
            url: '/api/users',
            type: 'api_error',
          })
        );
      });

      it('should handle unknown error type', () => {
        logApiError('POST', '/api/posts', 'Unknown error');

        expect(consoleErrorSpy).toHaveBeenCalledWith(
          '[ERROR] API Error: POST /api/posts',
          'Unknown error',
          expect.objectContaining({
            method: 'POST',
            url: '/api/posts',
            type: 'api_error',
          })
        );
      });

      it('should include additional metadata', () => {
        const error = new Error('Timeout');

        logApiError('DELETE', '/api/items/1', error, { timeout: 5000 });

        expect(consoleErrorSpy).toHaveBeenCalledWith(
          '[ERROR] API Error: DELETE /api/items/1',
          error,
          expect.objectContaining({
            method: 'DELETE',
            url: '/api/items/1',
            timeout: 5000,
            type: 'api_error',
          })
        );
      });
    });
  });

  describe('User action logging', () => {
    describe('logUserAction', () => {
      it('should log user action', () => {
        logUserAction('button_click', { buttonId: 'submit' });

        expect(consoleInfoSpy).toHaveBeenCalledWith(
          '[INFO] User Action: button_click',
          expect.objectContaining({
            action: 'button_click',
            buttonId: 'submit',
            type: 'user_action',
          })
        );
      });

      it('should log user action without metadata', () => {
        logUserAction('page_scroll');

        expect(consoleInfoSpy).toHaveBeenCalledWith(
          '[INFO] User Action: page_scroll',
          expect.objectContaining({
            action: 'page_scroll',
            type: 'user_action',
          })
        );
      });
    });

    describe('logPageView', () => {
      it('should log page view', () => {
        logPageView('/dashboard', { referrer: '/home' });

        expect(consoleInfoSpy).toHaveBeenCalledWith(
          '[INFO] Page View: /dashboard',
          expect.objectContaining({
            path: '/dashboard',
            referrer: '/home',
            type: 'page_view',
          })
        );
      });

      it('should log page view without metadata', () => {
        logPageView('/profile');

        expect(consoleInfoSpy).toHaveBeenCalledWith(
          '[INFO] Page View: /profile',
          expect.objectContaining({
            path: '/profile',
            type: 'page_view',
          })
        );
      });
    });

    describe('setLoggerUserId', () => {
      it('should log user context being set', () => {
        setLoggerUserId('user-123');

        expect(consoleInfoSpy).toHaveBeenCalledWith(
          '[INFO] User context set for logging',
          expect.objectContaining({
            userId: 'user-123',
          })
        );
      });
    });
  });

  describe('createChildLogger', () => {
    it('should create logger with additional context', () => {
      const context = { component: 'ChatInput', sessionId: 'sess-123' };
      const childLogger = createChildLogger(context);

      childLogger.info('Child log message', { extraData: 'test' });

      expect(consoleInfoSpy).toHaveBeenCalledWith(
        '[INFO] Child log message',
        expect.objectContaining({
          component: 'ChatInput',
          sessionId: 'sess-123',
          extraData: 'test',
        })
      );
    });

    it('should merge child context with message metadata', () => {
      const context = { module: 'auth' };
      const childLogger = createChildLogger(context);

      childLogger.debug('Auth debug', { step: 'validate' });

      // Should include both context and metadata
      expect(consoleDebugSpy).toHaveBeenCalledWith(
        expect.stringContaining('Auth debug'),
        expect.objectContaining({
          module: 'auth',
          step: 'validate',
        })
      );
    });

    it('should work with all log levels', () => {
      mockGetConfig.mockReturnValue({ ...mockConfig, logLevel: 'debug' });
      const context = { service: 'api' };
      const childLogger = createChildLogger(context);

      childLogger.debug('Debug message');
      childLogger.info('Info message');
      childLogger.warn('Warn message');
      childLogger.error('Error message', new Error('Test'));

      expect(consoleDebugSpy).toHaveBeenCalledWith(
        expect.any(String),
        expect.objectContaining({ service: 'api' })
      );
      expect(consoleInfoSpy).toHaveBeenCalledWith(
        expect.any(String),
        expect.objectContaining({ service: 'api' })
      );
      expect(consoleWarnSpy).toHaveBeenCalledWith(
        expect.any(String),
        expect.objectContaining({ service: 'api' })
      );
      expect(consoleErrorSpy).toHaveBeenCalledWith(
        expect.any(String),
        expect.any(Error),
        expect.objectContaining({ service: 'api' })
      );
    });

    it('should override parent context with message metadata', () => {
      const context = { correlationId: 'parent-123' };
      const childLogger = createChildLogger(context);

      childLogger.info('Override test', { correlationId: 'child-456' });

      expect(consoleInfoSpy).toHaveBeenCalledWith(
        '[INFO] Override test',
        expect.objectContaining({
          correlationId: 'child-456', // Child metadata takes precedence
        })
      );
    });
  });

  describe('Edge cases', () => {
    it('should handle null metadata gracefully', () => {
      const logger = getLogger();

      // @ts-expect-error Testing runtime behavior with null
      logger.info('Message', null);

      expect(consoleInfoSpy).toHaveBeenCalledWith('[INFO] Message', {});
    });

    it('should handle undefined metadata gracefully', () => {
      const logger = getLogger();

      logger.info('Message', undefined);

      expect(consoleInfoSpy).toHaveBeenCalledWith('[INFO] Message', {});
    });

    it('should handle empty metadata object', () => {
      const logger = getLogger();

      logger.info('Message', {});

      expect(consoleInfoSpy).toHaveBeenCalledWith('[INFO] Message', {});
    });

    it('should handle complex metadata objects', () => {
      const logger = getLogger();
      const complexMetadata = {
        nested: { deep: { value: 123 } },
        array: [1, 2, 3],
        nullValue: null,
        undefinedValue: undefined,
      };

      logger.info('Complex metadata', complexMetadata);

      expect(consoleInfoSpy).toHaveBeenCalledWith(
        '[INFO] Complex metadata',
        complexMetadata
      );
    });

    it('should handle very long messages', () => {
      const logger = getLogger();
      const longMessage = 'A'.repeat(10000);

      logger.info(longMessage);

      expect(consoleInfoSpy).toHaveBeenCalledWith(`[INFO] ${longMessage}`, {});
    });

    it('should handle special characters in messages', () => {
      const logger = getLogger();
      const specialMessage = 'Test\n\t\r\\"Special\'Chars';

      logger.info(specialMessage);

      expect(consoleInfoSpy).toHaveBeenCalledWith(
        `[INFO] ${specialMessage}`,
        {}
      );
    });
  });
});
