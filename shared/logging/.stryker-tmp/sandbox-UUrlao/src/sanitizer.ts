/**
 * Sanitizer module for redacting sensitive data from log entries
 *
 * Security baseline: Implements PR.DS-5 (Data-at-rest protection) from NIST CSF 2.0
 * by preventing sensitive data leakage in logs.
 */
// @ts-nocheck


/**
 * Sensitive field patterns to redact
 * These patterns match common sensitive field names in a case-insensitive manner
 */function stryNS_9fa48() {
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
const SENSITIVE_PATTERNS: RegExp[] = stryMutAct_9fa48("130") ? [] : (stryCov_9fa48("130"), [/password/i, /passwd/i, /pwd/i, /secret/i, /token/i, stryMutAct_9fa48("132") ? /api[^_-]?key/i : stryMutAct_9fa48("131") ? /api[_-]key/i : (stryCov_9fa48("131", "132"), /api[_-]?key/i), /apikey/i, /authorization/i, /auth/i, /cookie/i, /session/i, /ssn/i, stryMutAct_9fa48("134") ? /social[^_-]?security/i : stryMutAct_9fa48("133") ? /social[_-]security/i : (stryCov_9fa48("133", "134"), /social[_-]?security/i), stryMutAct_9fa48("136") ? /credit[^_-]?card/i : stryMutAct_9fa48("135") ? /credit[_-]card/i : (stryCov_9fa48("135", "136"), /credit[_-]?card/i), stryMutAct_9fa48("138") ? /card[^_-]?number/i : stryMutAct_9fa48("137") ? /card[_-]number/i : (stryCov_9fa48("137", "138"), /card[_-]?number/i), /cvv/i, /pin/i, stryMutAct_9fa48("140") ? /private[^_-]?key/i : stryMutAct_9fa48("139") ? /private[_-]key/i : (stryCov_9fa48("139", "140"), /private[_-]?key/i), stryMutAct_9fa48("142") ? /access[^_-]?token/i : stryMutAct_9fa48("141") ? /access[_-]token/i : (stryCov_9fa48("141", "142"), /access[_-]?token/i), stryMutAct_9fa48("144") ? /refresh[^_-]?token/i : stryMutAct_9fa48("143") ? /refresh[_-]token/i : (stryCov_9fa48("143", "144"), /refresh[_-]?token/i), /bearer/i]);

/**
 * Redaction placeholder for sensitive data
 */
const REDACTED_PLACEHOLDER = stryMutAct_9fa48("145") ? "" : (stryCov_9fa48("145"), '[REDACTED]');

/**
 * Checks if a field name matches any sensitive pattern
 */
function isSensitiveField(fieldName: string): boolean {
  if (stryMutAct_9fa48("146")) {
    {}
  } else {
    stryCov_9fa48("146");
    return stryMutAct_9fa48("147") ? SENSITIVE_PATTERNS.every(pattern => pattern.test(fieldName)) : (stryCov_9fa48("147"), SENSITIVE_PATTERNS.some(stryMutAct_9fa48("148") ? () => undefined : (stryCov_9fa48("148"), pattern => pattern.test(fieldName))));
  }
}

/**
 * Sanitizes log data by recursively redacting sensitive fields
 *
 * @param data - The data to sanitize (can be any type)
 * @returns Sanitized data with sensitive fields redacted
 *
 * @example
 * const data = {
 *   username: 'john',
 *   password: 'secret123',
 *   nested: {
 *     apiKey: 'key-123',
 *     public: 'safe-data'
 *   }
 * };
 * const sanitized = sanitizeLogData(data);
 * // Returns:
 * // {
 * //   username: 'john',
 * //   password: '[REDACTED]',
 * //   nested: {
 * //     apiKey: '[REDACTED]',
 * //     public: 'safe-data'
 * //   }
 * // }
 */
export function sanitizeLogData(data: unknown): unknown {
  if (stryMutAct_9fa48("149")) {
    {}
  } else {
    stryCov_9fa48("149");
    // Handle null and undefined
    if (stryMutAct_9fa48("152") ? data === null && data === undefined : stryMutAct_9fa48("151") ? false : stryMutAct_9fa48("150") ? true : (stryCov_9fa48("150", "151", "152"), (stryMutAct_9fa48("154") ? data !== null : stryMutAct_9fa48("153") ? false : (stryCov_9fa48("153", "154"), data === null)) || (stryMutAct_9fa48("156") ? data !== undefined : stryMutAct_9fa48("155") ? false : (stryCov_9fa48("155", "156"), data === undefined)))) {
      if (stryMutAct_9fa48("157")) {
        {}
      } else {
        stryCov_9fa48("157");
        return data;
      }
    }

    // Handle primitive types (string, number, boolean)
    if (stryMutAct_9fa48("160") ? typeof data === 'object' : stryMutAct_9fa48("159") ? false : stryMutAct_9fa48("158") ? true : (stryCov_9fa48("158", "159", "160"), typeof data !== (stryMutAct_9fa48("161") ? "" : (stryCov_9fa48("161"), 'object')))) {
      if (stryMutAct_9fa48("162")) {
        {}
      } else {
        stryCov_9fa48("162");
        return data;
      }
    }

    // Handle arrays - recursively sanitize each element
    if (stryMutAct_9fa48("164") ? false : stryMutAct_9fa48("163") ? true : (stryCov_9fa48("163", "164"), Array.isArray(data))) {
      if (stryMutAct_9fa48("165")) {
        {}
      } else {
        stryCov_9fa48("165");
        return data.map(stryMutAct_9fa48("166") ? () => undefined : (stryCov_9fa48("166"), item => sanitizeLogData(item)));
      }
    }

    // Handle Error objects specially to preserve stack traces
    if (stryMutAct_9fa48("168") ? false : stryMutAct_9fa48("167") ? true : (stryCov_9fa48("167", "168"), data instanceof Error)) {
      if (stryMutAct_9fa48("169")) {
        {}
      } else {
        stryCov_9fa48("169");
        return stryMutAct_9fa48("170") ? {} : (stryCov_9fa48("170"), {
          name: data.name,
          message: data.message,
          stack: data.stack
        });
      }
    }

    // Handle Date objects
    if (stryMutAct_9fa48("172") ? false : stryMutAct_9fa48("171") ? true : (stryCov_9fa48("171", "172"), data instanceof Date)) {
      if (stryMutAct_9fa48("173")) {
        {}
      } else {
        stryCov_9fa48("173");
        return data;
      }
    }

    // Handle plain objects - recursively sanitize each field
    const sanitized: Record<string, unknown> = {};
    for (const [key, value] of Object.entries(data)) {
      if (stryMutAct_9fa48("174")) {
        {}
      } else {
        stryCov_9fa48("174");
        if (stryMutAct_9fa48("176") ? false : stryMutAct_9fa48("175") ? true : (stryCov_9fa48("175", "176"), isSensitiveField(key))) {
          if (stryMutAct_9fa48("177")) {
            {}
          } else {
            stryCov_9fa48("177");
            // Redact sensitive fields
            sanitized[key] = REDACTED_PLACEHOLDER;
          }
        } else if (stryMutAct_9fa48("180") ? typeof value === 'object' || value !== null : stryMutAct_9fa48("179") ? false : stryMutAct_9fa48("178") ? true : (stryCov_9fa48("178", "179", "180"), (stryMutAct_9fa48("182") ? typeof value !== 'object' : stryMutAct_9fa48("181") ? true : (stryCov_9fa48("181", "182"), typeof value === (stryMutAct_9fa48("183") ? "" : (stryCov_9fa48("183"), 'object')))) && (stryMutAct_9fa48("185") ? value === null : stryMutAct_9fa48("184") ? true : (stryCov_9fa48("184", "185"), value !== null)))) {
          if (stryMutAct_9fa48("186")) {
            {}
          } else {
            stryCov_9fa48("186");
            // Recursively sanitize nested objects
            sanitized[key] = sanitizeLogData(value);
          }
        } else {
          if (stryMutAct_9fa48("187")) {
            {}
          } else {
            stryCov_9fa48("187");
            // Keep non-sensitive primitive values as-is
            sanitized[key] = value;
          }
        }
      }
    }
    return sanitized;
  }
}

/**
 * Type guard to check if data is a plain object
 */
export function isPlainObject(value: unknown): value is Record<string, unknown> {
  if (stryMutAct_9fa48("188")) {
    {}
  } else {
    stryCov_9fa48("188");
    return stryMutAct_9fa48("191") ? typeof value === 'object' && value !== null && !Array.isArray(value) && !(value instanceof Date) || !(value instanceof Error) : stryMutAct_9fa48("190") ? false : stryMutAct_9fa48("189") ? true : (stryCov_9fa48("189", "190", "191"), (stryMutAct_9fa48("193") ? typeof value === 'object' && value !== null && !Array.isArray(value) || !(value instanceof Date) : stryMutAct_9fa48("192") ? true : (stryCov_9fa48("192", "193"), (stryMutAct_9fa48("195") ? typeof value === 'object' && value !== null || !Array.isArray(value) : stryMutAct_9fa48("194") ? true : (stryCov_9fa48("194", "195"), (stryMutAct_9fa48("197") ? typeof value === 'object' || value !== null : stryMutAct_9fa48("196") ? true : (stryCov_9fa48("196", "197"), (stryMutAct_9fa48("199") ? typeof value !== 'object' : stryMutAct_9fa48("198") ? true : (stryCov_9fa48("198", "199"), typeof value === (stryMutAct_9fa48("200") ? "" : (stryCov_9fa48("200"), 'object')))) && (stryMutAct_9fa48("202") ? value === null : stryMutAct_9fa48("201") ? true : (stryCov_9fa48("201", "202"), value !== null)))) && (stryMutAct_9fa48("203") ? Array.isArray(value) : (stryCov_9fa48("203"), !Array.isArray(value))))) && (stryMutAct_9fa48("204") ? value instanceof Date : (stryCov_9fa48("204"), !(value instanceof Date))))) && (stryMutAct_9fa48("205") ? value instanceof Error : (stryCov_9fa48("205"), !(value instanceof Error))));
  }
}