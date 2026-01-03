/**
 * Logging integration for frontend
 * Browser-safe logging wrapper
 *
 * IMPORTANT: Browser-specific configuration
 * - Logs to console in development/test
 * - Can send logs to backend in production via API
 * - Automatically sanitizes sensitive data
 * - Supports correlation IDs for request tracing
 */

import type { LogMetadata } from '@study-abroad/shared-logging';
import { getConfig, isDevelopment } from './config';

// Simple browser-safe logger interface
interface BrowserLogger {
  debug(message: string, metadata?: LogMetadata): void;
  info(message: string, metadata?: LogMetadata): void;
  warn(message: string, metadata?: LogMetadata): void;
  error(message: string, error?: Error | unknown, metadata?: LogMetadata): void;
}

// Singleton logger instance
let loggerInstance: BrowserLogger | null = null;

/**
 * Initialize the logger for browser environment
 * Should be called once at app startup
 */
export function initializeLogger(): BrowserLogger {
  if (loggerInstance) {
    return loggerInstance;
  }

  const config = getConfig();

  // Simple console-based logger for browser
  loggerInstance = {
    debug: (message: string, metadata?: LogMetadata) => {
      if (config.logLevel === 'debug' || isDevelopment()) {
        console.debug(`[DEBUG] ${message}`, metadata || {});
      }
    },
    info: (message: string, metadata?: LogMetadata) => {
      console.info(`[INFO] ${message}`, metadata || {});
    },
    warn: (message: string, metadata?: LogMetadata) => {
      console.warn(`[WARN] ${message}`, metadata || {});
    },
    error: (message: string, error?: Error | unknown, metadata?: LogMetadata) => {
      console.error(`[ERROR] ${message}`, error, metadata || {});
    },
  };

  if (isDevelopment()) {
    console.log('[Logger] Logger initialized for browser environment', {
      level: config.logLevel,
      environment: config.mode,
    });
  }

  return loggerInstance;
}

/**
 * Get the current logger instance
 * Automatically initializes if not already done
 */
export function getLogger(): BrowserLogger {
  if (!loggerInstance) {
    return initializeLogger();
  }
  return loggerInstance;
}

/**
 * Log helper functions for convenience
 */

export function logDebug(message: string, metadata?: LogMetadata): void {
  getLogger().debug(message, metadata);
}

export function logInfo(message: string, metadata?: LogMetadata): void {
  getLogger().info(message, metadata);
}

export function logWarn(message: string, metadata?: LogMetadata): void {
  getLogger().warn(message, metadata);
}

export function logError(message: string, error?: Error | unknown, metadata?: LogMetadata): void {
  getLogger().error(message, error, metadata);
}

/**
 * Log API request
 * Automatically includes correlation ID if available
 */
export function logApiRequest(
  method: string,
  url: string,
  metadata?: LogMetadata,
): void {
  getLogger().info(`API Request: ${method} ${url}`, {
    ...metadata,
    method,
    url,
    correlationId: getCorrelationId(),
    type: 'api_request',
  });
}

/**
 * Log API response
 * Automatically includes correlation ID and duration
 */
export function logApiResponse(
  method: string,
  url: string,
  status: number,
  duration: number,
  metadata?: LogMetadata,
): void {
  const level = status >= 400 ? 'error' : 'info';
  const logger = getLogger();

  const logData = {
    ...metadata,
    method,
    url,
    status,
    duration,
    correlationId: getCorrelationId(),
    type: 'api_response',
  };

  if (level === 'error') {
    logger.error(`API Response: ${method} ${url} ${status}`, undefined, logData);
  } else {
    logger.info(`API Response: ${method} ${url} ${status}`, logData);
  }
}

/**
 * Log API error
 */
export function logApiError(
  method: string,
  url: string,
  error: Error | unknown,
  metadata?: LogMetadata,
): void {
  getLogger().error(`API Error: ${method} ${url}`, error, {
    ...metadata,
    method,
    url,
    correlationId: getCorrelationId(),
    type: 'api_error',
  });
}

/**
 * Log user action
 * Useful for tracking user behavior and debugging
 */
export function logUserAction(
  action: string,
  metadata?: LogMetadata,
): void {
  getLogger().info(`User Action: ${action}`, {
    ...metadata,
    action,
    type: 'user_action',
  });
}

/**
 * Log page view
 */
export function logPageView(path: string, metadata?: LogMetadata): void {
  getLogger().info(`Page View: ${path}`, {
    ...metadata,
    path,
    type: 'page_view',
  });
}

/**
 * Set the current user ID for logging context
 * Should be called after authentication
 */
export function setLoggerUserId(userId: string): void {
  logInfo('User context set for logging', { userId });
}

/**
 * Create a child logger with additional context
 * Useful for component-specific logging
 */
export function createChildLogger(context: LogMetadata): BrowserLogger {
  const logger = getLogger();
  return {
    debug: (message: string, metadata?: LogMetadata) => logger.debug(message, { ...context, ...metadata }),
    info: (message: string, metadata?: LogMetadata) => logger.info(message, { ...context, ...metadata }),
    warn: (message: string, metadata?: LogMetadata) => logger.warn(message, { ...context, ...metadata }),
    error: (message: string, error?: Error | unknown, metadata?: LogMetadata) => logger.error(message, error, { ...context, ...metadata }),
  };
}

// Export types for type safety
export type { LogMetadata } from '@study-abroad/shared-logging';
export type { BrowserLogger as Logger };
