# @study-abroad/shared-logging

Structured logging package with Winston, hybrid log rotation, correlation ID support, and automatic sensitive data sanitization.

[![Coverage](https://img.shields.io/badge/coverage-99.47%25-brightgreen)](./coverage)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.3-blue)](https://www.typescriptlang.org/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](./LICENSE)

## Features

- **Structured JSON Logging**: Production-ready JSON format with human-readable console output for development
- **Hybrid Log Rotation**: Automatic rotation at 100MB OR daily (whichever occurs first)
- **Configurable Retention**: Auto-cleanup of logs older than retention period (default 30 days)
- **Sensitive Data Sanitization**: Automatic redaction of passwords, tokens, API keys, and other sensitive fields
- **Correlation ID Support**: Request tracing across async operations using AsyncLocalStorage
- **Environment-Specific Configuration**: Different log levels and formats for dev, test, and production
- **TypeScript Strict Mode**: Full type safety with comprehensive type definitions

## Installation

```bash
npm install @study-abroad/shared-logging
```

## Usage

### Basic Logging

```typescript
import { logger } from '@study-abroad/shared-logging';

// Log levels
logger.debug('Debug message', { key: 'value' });
logger.info('Info message', { userId: '123' });
logger.warn('Warning message', { issue: 'timeout' });
logger.error('Error message', new Error('Something failed'), { context: 'data' });
```

### With Request Correlation

```typescript
import { logger, withCorrelationId } from '@study-abroad/shared-logging';

export function handleRequest(req: Request) {
  return withCorrelationId(() => {
    logger.info('Request started', {
      method: req.method,
      path: req.url,
    });

    // All logs within this scope share the same requestId
    processRequest();

    logger.info('Request completed');
  });
}
```

### Setting User Context

```typescript
import { logger, setUserId } from '@study-abroad/shared-logging';

export function authenticateUser(userId: string) {
  setUserId(userId);

  logger.info('User authenticated');
  // Logs will automatically include userId
}
```

### Structured Log Output

**Development Mode** (pretty printing):
```
[2025-12-31 12:00:00.000] INFO: User authenticated
  requestId: "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
  userId: "user-123"
  environment: "dev"
```

**Production Mode** (JSON):
```json
{
  "timestamp": "2025-12-31T12:00:00.000Z",
  "level": "INFO",
  "message": "User authenticated",
  "requestId": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "userId": "user-123",
  "environment": "production"
}
```

### Sensitive Data Sanitization

Sensitive fields are automatically redacted:

```typescript
logger.info('Payment processed', {
  userId: '123',
  amount: 2.99,
  apiKey: 'sk_test_123',        // Redacted
  password: 'secret123',         // Redacted
  creditCard: '4242424242424242', // Redacted
});

// Output:
{
  "userId": "123",
  "amount": 2.99,
  "apiKey": "[REDACTED]",
  "password": "[REDACTED]",
  "creditCard": "[REDACTED]"
}
```

### Log Rotation

Logs automatically rotate based on:
- **Size**: When file reaches 100MB (configurable via `LOG_MAX_SIZE_MB`)
- **Time**: Daily at midnight UTC (configurable via `LOG_ROTATION_DAYS`)

File naming pattern: `app-YYYY-MM-DD-N.log`

Example:
```
logs/
├── app-2025-12-30-1.log  (100MB, rotated by size)
├── app-2025-12-30-2.log  (50MB, rotated by day change)
├── app-2025-12-31-1.log  (current)
```

### Log Retention

Old logs are automatically deleted:

```typescript
import { logCleanup } from '@study-abroad/shared-logging';

// Manual cleanup
const deletedCount = await logCleanup.cleanup();
console.log(`Deleted ${deletedCount} old log files`);

// Scheduled cleanup (runs daily)
const interval = logCleanup.scheduleCleanup();
```

### Environment Configuration

Configure logging via environment variables:

```env
LOG_LEVEL=debug           # debug | info | warn | error
LOG_DIR=./logs            # Directory for log files
LOG_MAX_SIZE_MB=100       # Max file size before rotation
LOG_ROTATION_DAYS=1       # Rotate daily
LOG_RETENTION_DAYS=30     # Keep logs for 30 days
```

### Testing

Capture logs in tests:

```typescript
import { logger } from '@study-abroad/shared-logging';

describe('UserService', () => {
  it('should log user creation', () => {
    const logs: any[] = [];

    // Mock the logger
    jest.spyOn(logger, 'info').mockImplementation((msg, ctx) => {
      logs.push({ message: msg, ...ctx });
    });

    createUser('user-123');

    expect(logs).toContainEqual({
      message: 'User created',
      userId: 'user-123',
    });
  });
});
```

## Log Patterns

### Authentication Events

```typescript
logger.info('Authentication attempt', { provider: 'google', email: 'user@example.com' });
logger.info('Authentication success', { userId: '123', provider: 'google' });
logger.warn('Authentication failed', { provider: 'google', reason: 'invalid_token' });
```

### Payment Transactions

```typescript
logger.info('Payment initiated', { userId: '123', amount: 2.99, currency: 'GBP' });
logger.info('Payment succeeded', { userId: '123', paymentId: 'pi_123', reportId: 'report-456' });
logger.error('Payment failed', new Error('Card declined'), { userId: '123', reason: 'insufficient_funds' });
```

### Report Generation

```typescript
logger.info('Report generation started', { userId: '123', subject: 'Computer Science' });
logger.info('Report generation completed', { userId: '123', reportId: 'report-456', duration: 3500 });
logger.error('Report generation failed', new Error('AI service timeout'), { userId: '123', subject: 'Computer Science' });
```

### API Errors

```typescript
logger.error('Database connection failed', new Error('Connection timeout'), {
  database: 'postgresql',
  host: 'localhost',
  port: 5432,
});
```

## API Reference

### Logger Class

#### Static Methods

- `Logger.getInstance(config?: LoggerConfig): Logger` - Get singleton logger instance
- `Logger.resetInstance(): void` - Reset singleton (primarily for testing)

#### Instance Methods

- `debug(message: string, metadata?: LogMetadata): void` - Log debug message
- `info(message: string, metadata?: LogMetadata): void` - Log info message
- `warn(message: string, metadata?: LogMetadata): void` - Log warning message
- `error(message: string, error?: Error, metadata?: LogMetadata): void` - Log error with optional Error object
- `setCorrelationId(id: string): void` - Set correlation ID for this logger instance
- `close(): Promise<void>` - Close all transports and flush pending logs

### Correlation Functions

- `withCorrelationId<T>(fn: () => T, correlationId?: string): T` - Execute function with correlation context
- `getCorrelationId(): string` - Get current correlation ID (auto-generated if not in context)
- `setUserId(userId: string): void` - Set user ID in current context
- `getUserId(): string | undefined` - Get user ID from current context
- `getCorrelationContext(): Record<string, string>` - Get all correlation context data
- `clearCorrelationContext(): void` - Clear correlation context (primarily for testing)

### Sanitization Functions

- `sanitizeLogData(data: unknown): unknown` - Recursively sanitize sensitive data
- `isPlainObject(value: unknown): boolean` - Type guard for plain objects

## Security

### NIST CSF 2.0 Compliance

This package implements the following NIST Cybersecurity Framework controls:

- **PR.DS-5 (Data-at-rest protection)**: Sensitive data redaction prevents leakage in logs
- **DE.AE-3 (Event data collection)**: Comprehensive logging of security-relevant events
- **DE.CM-1 (Network monitoring)**: Request/response logging with correlation IDs
- **RS.AN-1 (Investigation support)**: Structured logs support incident analysis

### Best Practices

1. **Never bypass sanitization**: Use the provided logger methods; don't serialize sensitive data manually
2. **Use correlation IDs**: Always wrap request handlers with `withCorrelationId`
3. **Set user context**: Call `setUserId` after authentication for user-scoped logging
4. **Log errors properly**: Always pass Error objects to `logger.error()` to capture stack traces
5. **Review log levels**: Use `debug` for development diagnostics, `error` for production to minimize log volume

## Testing

### Unit Tests

```bash
npm test                  # Run tests
npm run test:coverage     # Run tests with coverage
npm run test:mutation     # Run mutation tests
```

### Coverage Requirements

- **Line Coverage**: ≥90% (Currently: 99.47%)
- **Branch Coverage**: ≥90% (Currently: 92.40%)
- **Function Coverage**: ≥90% (Currently: 100%)
- **Mutation Score**: >80%

## Troubleshooting

### Logs not appearing

- Check `LOG_LEVEL` environment variable
- Verify `LOG_DIR` is writable
- Ensure logger is not silenced by test framework

### File rotation not working

- Verify `LOG_MAX_SIZE_MB` and `LOG_RETENTION_DAYS` are set
- Check file permissions on `LOG_DIR`
- Review `.audit.json` for rotation metadata

### Correlation IDs not propagating

- Ensure async operations are within `withCorrelationId` callback
- Verify AsyncLocalStorage is supported (Node.js 13.10.0+)
- Check that correlation context is set before logging

## Architecture Decision Record

See [ADR-0004: Logging Infrastructure](../../docs/adr/ADR-0004-logging-infrastructure.md)

## Related Packages

- `@study-abroad/shared-config` - Environment configuration with Zod validation
- `@study-abroad/shared-feature-flags` - Feature flag evaluation
- `@study-abroad/shared-database` - Database abstraction with soft delete

## License

MIT
