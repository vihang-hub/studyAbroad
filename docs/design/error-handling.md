# Error Handling Design

**Version**: 1.0.0
**Created**: 2025-12-31
**Status**: Design Approved

## Overview

This document defines the comprehensive error handling strategy for the MVP UK Study & Migration Research App, including error types, error responses, logging patterns, and user-facing error messages.

---

## Error Response Format

All API errors follow a standardized JSON structure with correlation IDs for traceability.

### Standard Error Response

```json
{
  "error": {
    "code": "PAYMENT_FAILED",
    "message": "Payment processing failed. Please check your payment method and try again.",
    "correlationId": "880fa700-h51e-74g7-d049-779988772333",
    "timestamp": "2025-12-31T12:00:00.000Z",
    "details": {
      "field": "card_number",
      "reason": "card_declined"
    }
  }
}
```

### Error Response Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `error.code` | string | Yes | Machine-readable error code (uppercase snake_case) |
| `error.message` | string | Yes | Human-readable error message for end users |
| `error.correlationId` | UUID | Yes | Unique request identifier for troubleshooting |
| `error.timestamp` | ISO 8601 | Yes | When the error occurred |
| `error.details` | object | No | Additional error context (varies by error type) |

---

## Error Codes

### HTTP Status Code Mapping

| HTTP Status | Error Code | Description | User Action |
|-------------|------------|-------------|-------------|
| 400 | `VALIDATION_ERROR` | Invalid request parameters | Fix input and retry |
| 400 | `INVALID_SUBJECT` | Subject field validation failed | Enter valid subject |
| 400 | `INVALID_COUNTRY` | Country not supported (non-UK) | Select UK |
| 401 | `UNAUTHORIZED` | Missing or invalid authentication | Sign in |
| 403 | `FORBIDDEN` | User lacks permission | Contact support |
| 404 | `NOT_FOUND` | Resource not found | Check URL or ID |
| 404 | `REPORT_DELETED` | Report was soft-deleted | Cannot be recovered |
| 404 | `REPORT_EXPIRED` | Report past 30-day expiration | Generate new report |
| 402 | `PAYMENT_REQUIRED` | Payment needed before access | Complete payment |
| 402 | `PAYMENT_FAILED` | Payment processing failed | Check payment method |
| 429 | `RATE_LIMIT_EXCEEDED` | Too many requests | Wait and retry |
| 500 | `INTERNAL_SERVER_ERROR` | Unexpected server error | Retry later, contact support |
| 500 | `DATABASE_ERROR` | Database operation failed | Retry later |
| 500 | `GEMINI_API_ERROR` | AI service unavailable | Retry later |
| 503 | `SERVICE_UNAVAILABLE` | Service temporarily down | Retry later |
| 503 | `REPORT_GENERATION_FAILED` | AI generation failed | Retry report generation |

---

## Error Types by Layer

### 1. Validation Errors (400)

**Triggered by**: Invalid user input

**Examples**:
```typescript
// Missing required field
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Subject is required and cannot be empty",
    "correlationId": "...",
    "timestamp": "...",
    "details": {
      "field": "subject",
      "constraint": "required"
    }
  }
}

// Subject too long
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Subject must be between 1 and 255 characters",
    "correlationId": "...",
    "timestamp": "...",
    "details": {
      "field": "subject",
      "constraint": "maxLength",
      "max": 255,
      "actual": 300
    }
  }
}

// Invalid country
{
  "error": {
    "code": "INVALID_COUNTRY",
    "message": "This MVP currently supports the UK only. Other countries coming soon.",
    "correlationId": "...",
    "timestamp": "...",
    "details": {
      "provided": "US",
      "supported": ["UK"]
    }
  }
}
```

**Frontend Handling**:
- Display error message inline near the invalid field
- Highlight invalid field with red border
- Show constraint details (e.g., "Max 255 characters")
- Focus the invalid field

### 2. Authentication Errors (401)

**Triggered by**: Missing or invalid JWT token

**Examples**:
```json
{
  "error": {
    "code": "UNAUTHORIZED",
    "message": "Authentication required. Please sign in to continue.",
    "correlationId": "...",
    "timestamp": "...",
    "details": {
      "reason": "missing_token"
    }
  }
}
```

**Frontend Handling**:
- Redirect to `/sign-in` with return URL
- Show message: "Your session expired. Please sign in again."
- Clear local auth state

### 3. Authorization Errors (403)

**Triggered by**: User accessing another user's resources

**Examples**:
```json
{
  "error": {
    "code": "FORBIDDEN",
    "message": "You do not have permission to access this report.",
    "correlationId": "...",
    "timestamp": "...",
    "details": {
      "reportId": "550e8400-...",
      "requestedBy": "user-123",
      "ownedBy": "user-456"
    }
  }
}
```

**Frontend Handling**:
- Show error page with message
- Log attempt (potential security issue)
- Redirect to user's own reports

### 4. Not Found Errors (404)

**Triggered by**: Resource doesn't exist or was soft-deleted

**Examples**:
```json
// Report not found
{
  "error": {
    "code": "NOT_FOUND",
    "message": "Report not found. It may have been deleted or expired.",
    "correlationId": "...",
    "timestamp": "..."
  }
}

// Report expired
{
  "error": {
    "code": "REPORT_EXPIRED",
    "message": "This report expired and is no longer available. Reports are accessible for 30 days.",
    "correlationId": "...",
    "timestamp": "...",
    "details": {
      "reportId": "550e8400-...",
      "expiresAt": "2025-12-01T12:00:00.000Z"
    }
  }
}
```

**Frontend Handling**:
- Show 404 page with helpful message
- Suggest creating a new report
- Link to report list or chat page

### 5. Payment Errors (402)

**Triggered by**: Payment processing failures

**Examples**:
```json
// Payment required
{
  "error": {
    "code": "PAYMENT_REQUIRED",
    "message": "Payment is required to generate a report. Price: £2.99",
    "correlationId": "...",
    "timestamp": "..."
  }
}

// Payment failed
{
  "error": {
    "code": "PAYMENT_FAILED",
    "message": "Payment processing failed. Please check your payment method.",
    "correlationId": "...",
    "timestamp": "...",
    "details": {
      "reason": "card_declined",
      "stripeError": "Your card was declined"
    }
  }
}
```

**Frontend Handling**:
- Show payment form if not yet attempted
- Display Stripe error message if payment failed
- Offer retry option
- Provide support contact for persistent issues

### 6. Rate Limiting Errors (429)

**Triggered by**: Too many requests from user

**Examples**:
```json
{
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "Too many requests. Please try again in 60 seconds.",
    "correlationId": "...",
    "timestamp": "...",
    "details": {
      "retryAfter": 60,
      "limit": 100,
      "window": 60
    }
  }
}
```

**Frontend Handling**:
- Show countdown timer until retry allowed
- Disable submit button during countdown
- Log rate limit hit for analytics

### 7. Server Errors (500, 503)

**Triggered by**: Internal failures, external API errors

**Examples**:
```json
// Generic server error
{
  "error": {
    "code": "INTERNAL_SERVER_ERROR",
    "message": "An unexpected error occurred. Please try again later.",
    "correlationId": "880fa700-h51e-74g7-d049-779988772333",
    "timestamp": "..."
  }
}

// Database error
{
  "error": {
    "code": "DATABASE_ERROR",
    "message": "Unable to access the database. Please try again later.",
    "correlationId": "...",
    "timestamp": "..."
  }
}

// Gemini API error
{
  "error": {
    "code": "GEMINI_API_ERROR",
    "message": "AI service temporarily unavailable. Please try again in a few minutes.",
    "correlationId": "...",
    "timestamp": "...",
    "details": {
      "service": "gemini-api",
      "status": 503
    }
  }
}

// Report generation failed
{
  "error": {
    "code": "REPORT_GENERATION_FAILED",
    "message": "Report generation failed. You have not been charged. Please try again.",
    "correlationId": "...",
    "timestamp": "...",
    "details": {
      "subject": "Computer Science",
      "reason": "ai_timeout"
    }
  }
}
```

**Frontend Handling**:
- Show user-friendly error page
- Display correlation ID for support reference
- Offer retry button
- Suggest contacting support if persists

---

## Backend Error Handling Patterns

### FastAPI Exception Handlers

```python
# backend/src/exceptions.py
from fastapi import Request, status
from fastapi.responses import JSONResponse
from uuid import uuid4
from datetime import datetime

class AppException(Exception):
    """Base application exception"""
    def __init__(
        self,
        code: str,
        message: str,
        status_code: int = 500,
        details: dict = None
    ):
        self.code = code
        self.message = message
        self.status_code = status_code
        self.details = details or {}

@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    correlation_id = request.state.correlation_id or str(uuid4())

    logger.error(
        f"Error: {exc.code}",
        error=exc,
        context={
            "correlationId": correlation_id,
            "path": request.url.path,
            "method": request.method,
            **exc.details
        }
    )

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": exc.code,
                "message": exc.message,
                "correlationId": correlation_id,
                "timestamp": datetime.utcnow().isoformat(),
                "details": exc.details
            }
        }
    )

# Usage
raise AppException(
    code="PAYMENT_FAILED",
    message="Payment processing failed. Please check your payment method.",
    status_code=402,
    details={"reason": "card_declined"}
)
```

### Next.js Error Handling

```typescript
// frontend/src/lib/api-client.ts
export class APIClient {
  async request<T>(endpoint: string, options?: RequestInit): Promise<T> {
    const correlationId = crypto.randomUUID();

    try {
      const response = await fetch(`${API_URL}${endpoint}`, {
        ...options,
        headers: {
          'X-Correlation-ID': correlationId,
          ...options?.headers,
        },
      });

      if (!response.ok) {
        const error: ErrorResponse = await response.json();
        throw new APIError(error.error);
      }

      return await response.json();
    } catch (error) {
      if (error instanceof APIError) {
        throw error;
      }

      // Network error
      throw new APIError({
        code: 'NETWORK_ERROR',
        message: 'Unable to connect to the server. Please check your internet connection.',
        correlationId,
        timestamp: new Date().toISOString(),
      });
    }
  }
}

export class APIError extends Error {
  constructor(public error: ErrorDetail) {
    super(error.message);
    this.name = 'APIError';
  }
}
```

---

## Logging Patterns

### Error Logging with Correlation IDs

```typescript
// Every error logged includes correlation ID
logger.error('Payment processing failed', error, {
  correlationId: request.correlationId,
  userId: user.id,
  paymentId: payment.id,
  amount: 2.99,
});
```

### Sensitive Data Redaction

```typescript
// Automatically redact sensitive fields
logger.info('Payment created', sanitize({
  userId: 'user-123',
  cardNumber: '4242424242424242', // Redacted
  apiKey: 'sk_test_123',          // Redacted
}));

// Output:
{
  userId: 'user-123',
  cardNumber: '[REDACTED]',
  apiKey: '[REDACTED]'
}
```

---

## User-Facing Error Messages

### Guidelines

1. **Be Honest**: Don't hide errors, explain what happened
2. **Be Helpful**: Provide actionable next steps
3. **Be Concise**: Keep messages under 100 characters
4. **Be Empathetic**: Acknowledge user frustration
5. **Include Correlation ID**: For support reference (in details, not primary message)

### Examples

| Error | Bad Message | Good Message |
|-------|-------------|--------------|
| Payment failed | "Error 402" | "Payment failed. Please check your card details and try again." |
| Report expired | "Not found" | "This report expired after 30 days. Generate a new report to access updated information." |
| Rate limit | "Too many requests" | "You've reached the daily limit of 10 reports. Try again tomorrow or upgrade your account." |
| Server error | "Internal error" | "Something went wrong on our end. We've been notified and are working on it. (Ref: 880fa700...)" |

---

## Related Documentation

- [OpenAPI Specification](/Users/vihang/projects/study-abroad/docs/api/openapi.yaml)
- [Logging Infrastructure ADR](/Users/vihang/projects/study-abroad/docs/adr/ADR-0004-logging-infrastructure.md)
- [Error Response Schemas](/Users/vihang/projects/study-abroad/shared/config/src/schemas/api.schema.ts)
