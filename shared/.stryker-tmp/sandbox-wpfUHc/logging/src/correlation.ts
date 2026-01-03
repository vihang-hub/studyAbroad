/**
 * Correlation ID module for request tracing across application boundaries
 *
 * Uses AsyncLocalStorage to maintain correlation context without explicit parameter passing.
 * Supports distributed tracing by propagating correlation IDs across async operations.
 */
// @ts-nocheck


import { AsyncLocalStorage } from 'async_hooks';
import { randomUUID } from 'crypto';

/**
 * Storage for correlation context within async execution chains
 */
const asyncLocalStorage = new AsyncLocalStorage<Map<string, string>>();

/**
 * Context keys for storing correlation data
 */
const CORRELATION_ID_KEY = 'correlationId';
const USER_ID_KEY = 'userId';

/**
 * Executes a function within a new correlation context
 *
 * @param fn - The function to execute with correlation context
 * @param correlationId - Optional correlation ID (auto-generated if not provided)
 * @returns The result of the function execution
 *
 * @example
 * withCorrelationId(() => {
 *   logger.info('Request received'); // Automatically includes correlationId
 *   processRequest();
 * });
 *
 * @example
 * // With explicit correlation ID from incoming request header
 * const incomingId = request.headers['x-correlation-id'];
 * withCorrelationId(() => {
 *   logger.info('Processing request');
 * }, incomingId);
 */
export function withCorrelationId<T>(
  fn: () => T,
  correlationId?: string
): T {
  const store = new Map<string, string>();
  store.set(CORRELATION_ID_KEY, correlationId || randomUUID());
  return asyncLocalStorage.run(store, fn);
}

/**
 * Retrieves the current correlation ID from async context
 *
 * @returns The current correlation ID, or a new UUID if not in a correlation context
 *
 * @example
 * const correlationId = getCorrelationId();
 * logger.info('Processing', { correlationId });
 */
export function getCorrelationId(): string {
  const store = asyncLocalStorage.getStore();
  return store?.get(CORRELATION_ID_KEY) || randomUUID();
}

/**
 * Sets the user ID in the current correlation context
 *
 * @param userId - The user ID to associate with the current request
 *
 * @example
 * withCorrelationId(() => {
 *   const user = authenticateUser(token);
 *   setUserId(user.id);
 *   logger.info('User authenticated'); // Automatically includes userId
 * });
 */
export function setUserId(userId: string): void {
  const store = asyncLocalStorage.getStore();
  if (store) {
    store.set(USER_ID_KEY, userId);
  }
}

/**
 * Retrieves the user ID from the current correlation context
 *
 * @returns The current user ID, or undefined if not set
 *
 * @example
 * const userId = getUserId();
 * if (userId) {
 *   logger.info('User action', { userId });
 * }
 */
export function getUserId(): string | undefined {
  const store = asyncLocalStorage.getStore();
  return store?.get(USER_ID_KEY);
}

/**
 * Clears all correlation context data
 *
 * @remarks
 * This is primarily useful for testing to ensure clean state between tests.
 * In production code, correlation context is automatically isolated per execution.
 */
export function clearCorrelationContext(): void {
  const store = asyncLocalStorage.getStore();
  if (store) {
    store.clear();
  }
}

/**
 * Gets all correlation context data as a plain object
 *
 * @returns An object containing all correlation context data
 *
 * @example
 * const context = getCorrelationContext();
 * // { correlationId: 'uuid', userId: '123' }
 */
export function getCorrelationContext(): Record<string, string> {
  const store = asyncLocalStorage.getStore();
  if (!store) {
    return {};
  }

  const context: Record<string, string> = {};
  store.forEach((value, key) => {
    context[key] = value;
  });
  return context;
}
