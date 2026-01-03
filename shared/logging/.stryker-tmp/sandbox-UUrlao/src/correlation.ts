/**
 * Correlation ID module for request tracing across application boundaries
 *
 * Uses AsyncLocalStorage to maintain correlation context without explicit parameter passing.
 * Supports distributed tracing by propagating correlation IDs across async operations.
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
import { AsyncLocalStorage } from 'async_hooks';
import { randomUUID } from 'crypto';

/**
 * Storage for correlation context within async execution chains
 */
const asyncLocalStorage = new AsyncLocalStorage<Map<string, string>>();

/**
 * Context keys for storing correlation data
 */
const CORRELATION_ID_KEY = stryMutAct_9fa48("103") ? "" : (stryCov_9fa48("103"), 'correlationId');
const USER_ID_KEY = stryMutAct_9fa48("104") ? "" : (stryCov_9fa48("104"), 'userId');

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
export function withCorrelationId<T>(fn: () => T, correlationId?: string): T {
  if (stryMutAct_9fa48("105")) {
    {}
  } else {
    stryCov_9fa48("105");
    const store = new Map<string, string>();
    store.set(CORRELATION_ID_KEY, stryMutAct_9fa48("108") ? correlationId && randomUUID() : stryMutAct_9fa48("107") ? false : stryMutAct_9fa48("106") ? true : (stryCov_9fa48("106", "107", "108"), correlationId || randomUUID()));
    return asyncLocalStorage.run(store, fn);
  }
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
  if (stryMutAct_9fa48("109")) {
    {}
  } else {
    stryCov_9fa48("109");
    const store = asyncLocalStorage.getStore();
    return stryMutAct_9fa48("112") ? store?.get(CORRELATION_ID_KEY) && randomUUID() : stryMutAct_9fa48("111") ? false : stryMutAct_9fa48("110") ? true : (stryCov_9fa48("110", "111", "112"), (stryMutAct_9fa48("113") ? store.get(CORRELATION_ID_KEY) : (stryCov_9fa48("113"), store?.get(CORRELATION_ID_KEY))) || randomUUID());
  }
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
  if (stryMutAct_9fa48("114")) {
    {}
  } else {
    stryCov_9fa48("114");
    const store = asyncLocalStorage.getStore();
    if (stryMutAct_9fa48("116") ? false : stryMutAct_9fa48("115") ? true : (stryCov_9fa48("115", "116"), store)) {
      if (stryMutAct_9fa48("117")) {
        {}
      } else {
        stryCov_9fa48("117");
        store.set(USER_ID_KEY, userId);
      }
    }
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
  if (stryMutAct_9fa48("118")) {
    {}
  } else {
    stryCov_9fa48("118");
    const store = asyncLocalStorage.getStore();
    return stryMutAct_9fa48("119") ? store.get(USER_ID_KEY) : (stryCov_9fa48("119"), store?.get(USER_ID_KEY));
  }
}

/**
 * Clears all correlation context data
 *
 * @remarks
 * This is primarily useful for testing to ensure clean state between tests.
 * In production code, correlation context is automatically isolated per execution.
 */
export function clearCorrelationContext(): void {
  if (stryMutAct_9fa48("120")) {
    {}
  } else {
    stryCov_9fa48("120");
    const store = asyncLocalStorage.getStore();
    if (stryMutAct_9fa48("122") ? false : stryMutAct_9fa48("121") ? true : (stryCov_9fa48("121", "122"), store)) {
      if (stryMutAct_9fa48("123")) {
        {}
      } else {
        stryCov_9fa48("123");
        store.clear();
      }
    }
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
  if (stryMutAct_9fa48("124")) {
    {}
  } else {
    stryCov_9fa48("124");
    const store = asyncLocalStorage.getStore();
    if (stryMutAct_9fa48("127") ? false : stryMutAct_9fa48("126") ? true : stryMutAct_9fa48("125") ? store : (stryCov_9fa48("125", "126", "127"), !store)) {
      if (stryMutAct_9fa48("128")) {
        {}
      } else {
        stryCov_9fa48("128");
        return {};
      }
    }
    const context: Record<string, string> = {};
    store.forEach((value, key) => {
      if (stryMutAct_9fa48("129")) {
        {}
      } else {
        stryCov_9fa48("129");
        context[key] = value;
      }
    });
    return context;
  }
}