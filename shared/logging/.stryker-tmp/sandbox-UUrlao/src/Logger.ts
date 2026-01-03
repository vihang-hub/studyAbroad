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
// @ts-nocheck
function stryNS_9fa48() {
  var g = typeof globalThis === 'object' && globalThis && globalThis.Math === Math && globalThis || new Function("return this")();
  var ns = g.__stryker__ || (g.__stryker__ = {});
  if (ns.activeMutant === undefined && g.process && g.process.env && g.process.env.__STRYKER_ACTIVE_MUTANT__) {
    ns.activeMutant = g.process.env.__STRYKER_ACTIVE_MUTANT__;
  }
  function retrieveNS() {
    return ns;
  }
  stryNS_9fa48 = retrieveNS;
  return retrieveNS();
}
stryNS_9fa48();
function stryCov_9fa48() {
  var ns = stryNS_9fa48();
  var cov = ns.mutantCoverage || (ns.mutantCoverage = {
    static: {},
    perTest: {}
  });
  function cover() {
    var c = cov.static;
    if (ns.currentTestId) {
      c = cov.perTest[ns.currentTestId] = cov.perTest[ns.currentTestId] || {};
    }
    var a = arguments;
    for (var i = 0; i < a.length; i++) {
      c[a[i]] = (c[a[i]] || 0) + 1;
    }
  }
  stryCov_9fa48 = cover;
  cover.apply(null, arguments);
}
function stryMutAct_9fa48(id) {
  var ns = stryNS_9fa48();
  function isActive(id) {
    if (ns.activeMutant === id) {
      if (ns.hitCount !== void 0 && ++ns.hitCount > ns.hitLimit) {
        throw new Error('Stryker: Hit count limit reached (' + ns.hitCount + ')');
      }
      return true;
    }
    return false;
  }
  stryMutAct_9fa48 = isActive;
  return isActive(id);
}
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
    if (stryMutAct_9fa48("0")) {
      {}
    } else {
      stryCov_9fa48("0");
      this.config = ConfigLoader.load();
      this.logger = this.createLogger(customConfig);
    }
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
    if (stryMutAct_9fa48("1")) {
      {}
    } else {
      stryCov_9fa48("1");
      if (stryMutAct_9fa48("4") ? false : stryMutAct_9fa48("3") ? true : stryMutAct_9fa48("2") ? Logger.instance : (stryCov_9fa48("2", "3", "4"), !Logger.instance)) {
        if (stryMutAct_9fa48("5")) {
          {}
        } else {
          stryCov_9fa48("5");
          Logger.instance = new Logger(customConfig);
        }
      }
      return Logger.instance;
    }
  }

  /**
   * Resets the singleton instance (primarily for testing)
   */
  public static resetInstance(): void {
    if (stryMutAct_9fa48("6")) {
      {}
    } else {
      stryCov_9fa48("6");
      if (stryMutAct_9fa48("8") ? false : stryMutAct_9fa48("7") ? true : (stryCov_9fa48("7", "8"), Logger.instance)) {
        if (stryMutAct_9fa48("9")) {
          {}
        } else {
          stryCov_9fa48("9");
          Logger.instance.logger.close();
          Logger.instance = undefined as unknown as Logger;
        }
      }
    }
  }

  /**
   * Creates and configures the Winston logger instance
   */
  private createLogger(customConfig?: LoggerConfig): winston.Logger {
    if (stryMutAct_9fa48("10")) {
      {}
    } else {
      stryCov_9fa48("10");
      const logLevel = stryMutAct_9fa48("13") ? (customConfig?.logLevel || this.config.LOG_LEVEL) && 'info' : stryMutAct_9fa48("12") ? false : stryMutAct_9fa48("11") ? true : (stryCov_9fa48("11", "12", "13"), (stryMutAct_9fa48("15") ? customConfig?.logLevel && this.config.LOG_LEVEL : stryMutAct_9fa48("14") ? false : (stryCov_9fa48("14", "15"), (stryMutAct_9fa48("16") ? customConfig.logLevel : (stryCov_9fa48("16"), customConfig?.logLevel)) || this.config.LOG_LEVEL)) || (stryMutAct_9fa48("17") ? "" : (stryCov_9fa48("17"), 'info')));
      const environment = stryMutAct_9fa48("20") ? (customConfig?.environment || this.config.ENVIRONMENT_MODE) && 'dev' : stryMutAct_9fa48("19") ? false : stryMutAct_9fa48("18") ? true : (stryCov_9fa48("18", "19", "20"), (stryMutAct_9fa48("22") ? customConfig?.environment && this.config.ENVIRONMENT_MODE : stryMutAct_9fa48("21") ? false : (stryCov_9fa48("21", "22"), (stryMutAct_9fa48("23") ? customConfig.environment : (stryCov_9fa48("23"), customConfig?.environment)) || this.config.ENVIRONMENT_MODE)) || (stryMutAct_9fa48("24") ? "" : (stryCov_9fa48("24"), 'dev')));
      const logDir = stryMutAct_9fa48("27") ? customConfig?.logDir && this.config.LOG_DIR : stryMutAct_9fa48("26") ? false : stryMutAct_9fa48("25") ? true : (stryCov_9fa48("25", "26", "27"), (stryMutAct_9fa48("28") ? customConfig.logDir : (stryCov_9fa48("28"), customConfig?.logDir)) || this.config.LOG_DIR);

      // Create log format based on environment
      const format = winston.format.combine(winston.format.timestamp(stryMutAct_9fa48("29") ? {} : (stryCov_9fa48("29"), {
        format: stryMutAct_9fa48("30") ? "" : (stryCov_9fa48("30"), 'YYYY-MM-DDTHH:mm:ss.SSSZ')
      })), winston.format.errors(stryMutAct_9fa48("31") ? {} : (stryCov_9fa48("31"), {
        stack: stryMutAct_9fa48("32") ? false : (stryCov_9fa48("32"), true)
      })), (stryMutAct_9fa48("35") ? environment !== 'dev' : stryMutAct_9fa48("34") ? false : stryMutAct_9fa48("33") ? true : (stryCov_9fa48("33", "34", "35"), environment === (stryMutAct_9fa48("36") ? "" : (stryCov_9fa48("36"), 'dev')))) ? winston.format.combine(winston.format.colorize(), winston.format.printf(({
        timestamp,
        level,
        message,
        ...meta
      }) => {
        if (stryMutAct_9fa48("37")) {
          {}
        } else {
          stryCov_9fa48("37");
          const metaStr = (stryMutAct_9fa48("41") ? Object.keys(meta).length <= 0 : stryMutAct_9fa48("40") ? Object.keys(meta).length >= 0 : stryMutAct_9fa48("39") ? false : stryMutAct_9fa48("38") ? true : (stryCov_9fa48("38", "39", "40", "41"), Object.keys(meta).length > 0)) ? stryMutAct_9fa48("42") ? `` : (stryCov_9fa48("42"), `\n${JSON.stringify(meta, null, 2)}`) : stryMutAct_9fa48("43") ? "Stryker was here!" : (stryCov_9fa48("43"), '');
          return stryMutAct_9fa48("44") ? `` : (stryCov_9fa48("44"), `${timestamp} [${level}]: ${message}${metaStr}`);
        }
      })) : winston.format.json());

      // Console transport (always enabled)
      const transports: winston.transport[] = stryMutAct_9fa48("45") ? [] : (stryCov_9fa48("45"), [new winston.transports.Console(stryMutAct_9fa48("46") ? {} : (stryCov_9fa48("46"), {
        level: logLevel,
        format
      }))]);

      // File transport with hybrid rotation (if log directory specified)
      if (stryMutAct_9fa48("48") ? false : stryMutAct_9fa48("47") ? true : (stryCov_9fa48("47", "48"), logDir)) {
        if (stryMutAct_9fa48("49")) {
          {}
        } else {
          stryCov_9fa48("49");
          // Ensure log directory exists
          this.ensureLogDirectoryExists(logDir);
          const maxSize = stryMutAct_9fa48("52") ? (customConfig?.logMaxSizeMb || this.config.LOG_MAX_SIZE_MB) && 100 : stryMutAct_9fa48("51") ? false : stryMutAct_9fa48("50") ? true : (stryCov_9fa48("50", "51", "52"), (stryMutAct_9fa48("54") ? customConfig?.logMaxSizeMb && this.config.LOG_MAX_SIZE_MB : stryMutAct_9fa48("53") ? false : (stryCov_9fa48("53", "54"), (stryMutAct_9fa48("55") ? customConfig.logMaxSizeMb : (stryCov_9fa48("55"), customConfig?.logMaxSizeMb)) || this.config.LOG_MAX_SIZE_MB)) || 100);
          const maxFiles = stryMutAct_9fa48("58") ? (customConfig?.logRetentionDays || this.config.LOG_RETENTION_DAYS) && 30 : stryMutAct_9fa48("57") ? false : stryMutAct_9fa48("56") ? true : (stryCov_9fa48("56", "57", "58"), (stryMutAct_9fa48("60") ? customConfig?.logRetentionDays && this.config.LOG_RETENTION_DAYS : stryMutAct_9fa48("59") ? false : (stryCov_9fa48("59", "60"), (stryMutAct_9fa48("61") ? customConfig.logRetentionDays : (stryCov_9fa48("61"), customConfig?.logRetentionDays)) || this.config.LOG_RETENTION_DAYS)) || 30);
          transports.push(new DailyRotateFile(stryMutAct_9fa48("62") ? {} : (stryCov_9fa48("62"), {
            filename: stryMutAct_9fa48("63") ? `` : (stryCov_9fa48("63"), `${logDir}/app-%DATE%.log`),
            datePattern: stryMutAct_9fa48("64") ? "" : (stryCov_9fa48("64"), 'YYYY-MM-DD'),
            maxSize: stryMutAct_9fa48("65") ? `` : (stryCov_9fa48("65"), `${maxSize}m`),
            maxFiles: stryMutAct_9fa48("66") ? `` : (stryCov_9fa48("66"), `${maxFiles}d`),
            level: logLevel,
            format: winston.format.combine(winston.format.timestamp(stryMutAct_9fa48("67") ? {} : (stryCov_9fa48("67"), {
              format: stryMutAct_9fa48("68") ? "" : (stryCov_9fa48("68"), 'YYYY-MM-DDTHH:mm:ss.SSSZ')
            })), winston.format.json()),
            auditFile: stryMutAct_9fa48("69") ? `` : (stryCov_9fa48("69"), `${logDir}/.audit.json`)
          })));
        }
      }
      return winston.createLogger(stryMutAct_9fa48("70") ? {} : (stryCov_9fa48("70"), {
        level: logLevel,
        format,
        transports,
        defaultMeta: stryMutAct_9fa48("71") ? {} : (stryCov_9fa48("71"), {
          environment,
          service: stryMutAct_9fa48("72") ? "" : (stryCov_9fa48("72"), 'study-abroad')
        }),
        exitOnError: stryMutAct_9fa48("73") ? true : (stryCov_9fa48("73"), false)
      }));
    }
  }

  /**
   * Ensures the log directory exists, creating it if necessary
   */
  private ensureLogDirectoryExists(logDir: string): void {
    if (stryMutAct_9fa48("74")) {
      {}
    } else {
      stryCov_9fa48("74");
      try {
        if (stryMutAct_9fa48("75")) {
          {}
        } else {
          stryCov_9fa48("75");
          if (stryMutAct_9fa48("78") ? false : stryMutAct_9fa48("77") ? true : stryMutAct_9fa48("76") ? existsSync(logDir) : (stryCov_9fa48("76", "77", "78"), !existsSync(logDir))) {
            if (stryMutAct_9fa48("79")) {
              {}
            } else {
              stryCov_9fa48("79");
              mkdirSync(logDir, stryMutAct_9fa48("80") ? {} : (stryCov_9fa48("80"), {
                recursive: stryMutAct_9fa48("81") ? false : (stryCov_9fa48("81"), true)
              }));
            }
          }
        }
      } catch (error) {
        if (stryMutAct_9fa48("82")) {
          {}
        } else {
          stryCov_9fa48("82");
          console.error(stryMutAct_9fa48("83") ? `` : (stryCov_9fa48("83"), `Failed to create log directory ${logDir}:`), error);
        }
      }
    }
  }

  /**
   * Enriches log metadata with correlation context
   */
  private enrichMetadata(metadata?: LogMetadata): LogMetadata {
    if (stryMutAct_9fa48("84")) {
      {}
    } else {
      stryCov_9fa48("84");
      return stryMutAct_9fa48("85") ? {} : (stryCov_9fa48("85"), {
        correlationId: stryMutAct_9fa48("88") ? this.correlationIdValue && getCorrelationId() : stryMutAct_9fa48("87") ? false : stryMutAct_9fa48("86") ? true : (stryCov_9fa48("86", "87", "88"), this.correlationIdValue || getCorrelationId()),
        userId: getUserId(),
        ...metadata
      });
    }
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
    if (stryMutAct_9fa48("89")) {
      {}
    } else {
      stryCov_9fa48("89");
      this.correlationIdValue = correlationId;
    }
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
    if (stryMutAct_9fa48("90")) {
      {}
    } else {
      stryCov_9fa48("90");
      const enriched = this.enrichMetadata(metadata);
      const sanitized = sanitizeLogData(enriched);
      this.logger.debug(message, sanitized);
    }
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
    if (stryMutAct_9fa48("91")) {
      {}
    } else {
      stryCov_9fa48("91");
      const enriched = this.enrichMetadata(metadata);
      const sanitized = sanitizeLogData(enriched);
      this.logger.info(message, sanitized);
    }
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
    if (stryMutAct_9fa48("92")) {
      {}
    } else {
      stryCov_9fa48("92");
      const enriched = this.enrichMetadata(metadata);
      const sanitized = sanitizeLogData(enriched);
      this.logger.warn(message, sanitized);
    }
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
    if (stryMutAct_9fa48("93")) {
      {}
    } else {
      stryCov_9fa48("93");
      const enriched = this.enrichMetadata(stryMutAct_9fa48("94") ? {} : (stryCov_9fa48("94"), {
        ...metadata,
        ...(stryMutAct_9fa48("97") ? error || {
          error: {
            name: error.name,
            message: error.message,
            stack: error.stack
          }
        } : stryMutAct_9fa48("96") ? false : stryMutAct_9fa48("95") ? true : (stryCov_9fa48("95", "96", "97"), error && (stryMutAct_9fa48("98") ? {} : (stryCov_9fa48("98"), {
          error: stryMutAct_9fa48("99") ? {} : (stryCov_9fa48("99"), {
            name: error.name,
            message: error.message,
            stack: error.stack
          })
        }))))
      }));
      const sanitized = sanitizeLogData(enriched);
      this.logger.error(message, sanitized);
    }
  }

  /**
   * Gets the underlying Winston logger instance
   * (Useful for advanced use cases or testing)
   */
  public getWinstonLogger(): winston.Logger {
    if (stryMutAct_9fa48("100")) {
      {}
    } else {
      stryCov_9fa48("100");
      return this.logger;
    }
  }

  /**
   * Closes all transports and flushes any pending logs
   */
  public close(): Promise<void> {
    if (stryMutAct_9fa48("101")) {
      {}
    } else {
      stryCov_9fa48("101");
      return new Promise(resolve => {
        if (stryMutAct_9fa48("102")) {
          {}
        } else {
          stryCov_9fa48("102");
          this.logger.close();
          resolve();
        }
      });
    }
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