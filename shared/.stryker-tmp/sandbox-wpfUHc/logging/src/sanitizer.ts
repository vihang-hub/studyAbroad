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
 */
const SENSITIVE_PATTERNS: RegExp[] = [
  /password/i,
  /passwd/i,
  /pwd/i,
  /secret/i,
  /token/i,
  /api[_-]?key/i,
  /apikey/i,
  /authorization/i,
  /auth/i,
  /cookie/i,
  /session/i,
  /ssn/i,
  /social[_-]?security/i,
  /credit[_-]?card/i,
  /card[_-]?number/i,
  /cvv/i,
  /pin/i,
  /private[_-]?key/i,
  /access[_-]?token/i,
  /refresh[_-]?token/i,
  /bearer/i,
];

/**
 * Redaction placeholder for sensitive data
 */
const REDACTED_PLACEHOLDER = '[REDACTED]';

/**
 * Checks if a field name matches any sensitive pattern
 */
function isSensitiveField(fieldName: string): boolean {
  return SENSITIVE_PATTERNS.some((pattern) => pattern.test(fieldName));
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
  // Handle null and undefined
  if (data === null || data === undefined) {
    return data;
  }

  // Handle primitive types (string, number, boolean)
  if (typeof data !== 'object') {
    return data;
  }

  // Handle arrays - recursively sanitize each element
  if (Array.isArray(data)) {
    return data.map((item) => sanitizeLogData(item));
  }

  // Handle Error objects specially to preserve stack traces
  if (data instanceof Error) {
    return {
      name: data.name,
      message: data.message,
      stack: data.stack,
    };
  }

  // Handle Date objects
  if (data instanceof Date) {
    return data;
  }

  // Handle plain objects - recursively sanitize each field
  const sanitized: Record<string, unknown> = {};

  for (const [key, value] of Object.entries(data)) {
    if (isSensitiveField(key)) {
      // Redact sensitive fields
      sanitized[key] = REDACTED_PLACEHOLDER;
    } else if (typeof value === 'object' && value !== null) {
      // Recursively sanitize nested objects
      sanitized[key] = sanitizeLogData(value);
    } else {
      // Keep non-sensitive primitive values as-is
      sanitized[key] = value;
    }
  }

  return sanitized;
}

/**
 * Type guard to check if data is a plain object
 */
export function isPlainObject(value: unknown): value is Record<string, unknown> {
  return (
    typeof value === 'object' &&
    value !== null &&
    !Array.isArray(value) &&
    !(value instanceof Date) &&
    !(value instanceof Error)
  );
}
