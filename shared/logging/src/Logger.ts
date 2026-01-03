/**
 * Logger module providing structured logging with Winston
 *
 * Features:
 * - Hybrid log rotation (100MB OR daily, whichever occurs first)
 * - Configurable retention period (default 30 days)
 * - Automatic sensitive data sanitization
 * - Correlation ID support for request tracing
 * - Environment-specific log levels and formats
 */

import winston from 'winston';
import DailyRotateFile from 'winston-daily-rotate-file';
import { ConfigLoader } from '@study-abroad/shared-config';
import { sanitizeLogData } from './sanitizer';
import { getCorrelationId, getUserId } from './correlation';
import { existsSync, mkdirSync } from 'fs';

/**
 * Log levels supported by the logger
 */
export enum LogLevel {
  DEBUG = 'debug',
  INFO = 'info',
  WARN = 'warn',
  ERROR = 'error',
}

/**
 * Metadata that can be attached to log entries
 */
export interface LogMetadata {
  [key: string]: unknown;
  correlationId?: string;
  userId?: string;
}

/**
 * Configuration for the logger instance
 */
export interface LoggerConfig {
  logLevel?: string;
  logDir?: string;
  logMaxSizeMb?: number;
  logRotationDays?: number;
  logRetentionDays?: number;
  environment?: string;
}

/**
 * Application logger with structured logging and correlation support
 *
 * Implements a singleton pattern to ensure consistent logging across the application.
 * Uses Winston for transport management and formatting.
 */
export class Logger {
  private static instance: Logger;
  private logger: winston.Logger;
  private config: ReturnType<typeof ConfigLoader.load>;
  private correlationIdValue?: string;

  /**
   * Private constructor to enforce singleton pattern
   */
  private constructor(customConfig?: LoggerConfig) {
    this.config = ConfigLoader.load();
    this.logger = this.createLogger(customConfig);
  }

  /**
   * Gets the singleton logger instance
   *
   * @param customConfig - Optional custom configuration (only used on first call)
   * @returns The logger instance
   *
   * @example
   * const logger = Logger.getInstance();
   * logger.info('Application started');
   */
  public static getInstance(customConfig?: LoggerConfig): Logger {
    if (!Logger.instance) {
      Logger.instance = new Logger(customConfig);
    }
    return Logger.instance;
  }

  /**
   * Resets the singleton instance (primarily for testing)
   */
  public static resetInstance(): void {
    if (Logger.instance) {
      Logger.instance.logger.close();
      Logger.instance = undefined as unknown as Logger;
    }
  }

  /**
   * Creates and configures the Winston logger instance
   */
  private createLogger(customConfig?: LoggerConfig): winston.Logger {
    const logLevel = customConfig?.logLevel || this.config.LOG_LEVEL || 'info';
    const environment = customConfig?.environment || this.config.ENVIRONMENT_MODE || 'dev';
    const logDir = customConfig?.logDir || this.config.LOG_DIR;

    // Create log format based on environment
    const format = winston.format.combine(
      winston.format.timestamp({ format: 'YYYY-MM-DDTHH:mm:ss.SSSZ' }),
      winston.format.errors({ stack: true }),
      environment === 'dev'
        ? winston.format.combine(
            winston.format.colorize(),
            winston.format.printf(({ timestamp, level, message, ...meta }) => {
              const metaStr = Object.keys(meta).length > 0
                ? `\n${JSON.stringify(meta, null, 2)}`
                : '';
              return `${timestamp} [${level}]: ${message}${metaStr}`;
            })
          )
        : winston.format.json()
    );

    // Console transport (always enabled)
    const transports: winston.transport[] = [
      new winston.transports.Console({
        level: logLevel,
        format,
      }),
    ];

    // File transport with hybrid rotation (if log directory specified)
    if (logDir) {
      // Ensure log directory exists
      this.ensureLogDirectoryExists(logDir);

      const maxSize = customConfig?.logMaxSizeMb || this.config.LOG_MAX_SIZE_MB || 100;
      const maxFiles = customConfig?.logRetentionDays || this.config.LOG_RETENTION_DAYS || 30;

      transports.push(
        new DailyRotateFile({
          filename: `${logDir}/app-%DATE%.log`,
          datePattern: 'YYYY-MM-DD',
          maxSize: `${maxSize}m`,
          maxFiles: `${maxFiles}d`,
          level: logLevel,
          format: winston.format.combine(
            winston.format.timestamp({ format: 'YYYY-MM-DDTHH:mm:ss.SSSZ' }),
            winston.format.json()
          ),
          auditFile: `${logDir}/.audit.json`,
        })
      );
    }

    return winston.createLogger({
      level: logLevel,
      format,
      transports,
      defaultMeta: {
        environment,
        service: 'study-abroad',
      },
      exitOnError: false,
    });
  }

  /**
   * Ensures the log directory exists, creating it if necessary
   */
  private ensureLogDirectoryExists(logDir: string): void {
    try {
      if (!existsSync(logDir)) {
        mkdirSync(logDir, { recursive: true });
      }
    } catch (error) {
      console.error(`Failed to create log directory ${logDir}:`, error);
    }
  }

  /**
   * Enriches log metadata with correlation context
   */
  private enrichMetadata(metadata?: LogMetadata): LogMetadata {
    return {
      correlationId: this.correlationIdValue || getCorrelationId(),
      userId: getUserId(),
      ...metadata,
    };
  }

  /**
   * Sets a correlation ID for this logger instance
   *
   * @param correlationId - The correlation ID to use
   *
   * @example
   * logger.setCorrelationId(request.headers['x-correlation-id']);
   * logger.info('Processing request'); // Will include the correlation ID
   */
  public setCorrelationId(correlationId: string): void {
    this.correlationIdValue = correlationId;
  }

  /**
   * Logs a debug message
   *
   * @param message - The log message
   * @param metadata - Optional metadata to include
   *
   * @example
   * logger.debug('Database query executed', { query: 'SELECT * FROM users', duration: 42 });
   */
  public debug(message: string, metadata?: LogMetadata): void {
    const enriched = this.enrichMetadata(metadata);
    const sanitized = sanitizeLogData(enriched);
    this.logger.debug(message, sanitized);
  }

  /**
   * Logs an info message
   *
   * @param message - The log message
   * @param metadata - Optional metadata to include
   *
   * @example
   * logger.info('User logged in', { userId: '123', method: 'google' });
   */
  public info(message: string, metadata?: LogMetadata): void {
    const enriched = this.enrichMetadata(metadata);
    const sanitized = sanitizeLogData(enriched);
    this.logger.info(message, sanitized);
  }

  /**
   * Logs a warning message
   *
   * @param message - The log message
   * @param metadata - Optional metadata to include
   *
   * @example
   * logger.warn('API rate limit approaching', { remaining: 10, limit: 100 });
   */
  public warn(message: string, metadata?: LogMetadata): void {
    const enriched = this.enrichMetadata(metadata);
    const sanitized = sanitizeLogData(enriched);
    this.logger.warn(message, sanitized);
  }

  /**
   * Logs an error message
   *
   * @param message - The log message
   * @param error - Optional error object
   * @param metadata - Optional metadata to include
   *
   * @example
   * try {
   *   await processPayment();
   * } catch (error) {
   *   logger.error('Payment processing failed', error, { userId: '123', amount: 299 });
   * }
   */
  public error(message: string, error?: Error, metadata?: LogMetadata): void {
    const enriched = this.enrichMetadata({
      ...metadata,
      ...(error && {
        error: {
          name: error.name,
          message: error.message,
          stack: error.stack,
        },
      }),
    });
    const sanitized = sanitizeLogData(enriched);
    this.logger.error(message, sanitized);
  }

  /**
   * Gets the underlying Winston logger instance
   * (Useful for advanced use cases or testing)
   */
  public getWinstonLogger(): winston.Logger {
    return this.logger;
  }

  /**
   * Closes all transports and flushes any pending logs
   */
  public close(): Promise<void> {
    return new Promise((resolve) => {
      this.logger.close();
      resolve();
    });
  }
}

/**
 * Default logger instance for convenient access
 *
 * @example
 * import { logger } from '@study-abroad/shared-logging';
 * logger.info('Application started');
 */
export const logger = Logger.getInstance();
