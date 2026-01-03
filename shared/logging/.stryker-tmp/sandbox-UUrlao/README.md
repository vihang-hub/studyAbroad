# @study-abroad/shared-logging

Structured logging infrastructure with rotation, retention, and correlation.

## Features

- Structured logging (JSON in production, pretty in dev)
- Request correlation IDs
- Log rotation (size-based and time-based)
- Automated log retention cleanup
- Sensitive data sanitization
- Environment-specific log levels

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

## Architecture Decision Record

See [ADR-0004: Logging Infrastructure](/Users/vihang/projects/study-abroad/docs/adr/ADR-0004-logging-infrastructure.md)

## License

MIT
