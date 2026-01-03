/**
 * @study-abroad/shared-logging
 *
 * Structured logging package with Winston, hybrid log rotation, and correlation ID support.
 *
 * Features:
 * - Structured JSON logging for production, human-readable for development
 * - Hybrid log rotation: 100MB OR daily (whichever occurs first)
 * - Configurable retention period (default 30 days)
 * - Automatic sensitive data sanitization (passwords, tokens, API keys)
 * - Correlation ID support for request tracing
 * - Environment-specific log levels (debug for dev/test, error for production)
 *
 * @example
 * import { logger, withCorrelationId } from '@study-abroad/shared-logging';
 *
 * // Basic logging
 * logger.info('User logged in', { userId: '123' });
 * logger.error('Payment failed', error, { amount: 299 });
 *
 * // With correlation context
 * withCorrelationId(() => {
 *   logger.info('Processing request');
 *   processRequest();
 * });
 *
 * @packageDocumentation
 */
// @ts-nocheck


// Export logger class and default instance
export { Logger, logger, LogLevel, LogMetadata, LoggerConfig } from './Logger';

// Export correlation utilities
export {
  withCorrelationId,
  getCorrelationId,
  setUserId,
  getUserId,
  clearCorrelationContext,
  getCorrelationContext,
} from './correlation';

// Export sanitization utilities (for advanced use cases)
export { sanitizeLogData, isPlainObject } from './sanitizer';
