# Security Design

**Version**: 1.0.0
**Created**: 2025-12-31
**Status**: Design Approved
**Framework**: NIST Cybersecurity Framework 2.0

## Overview

Comprehensive security design for the MVP UK Study & Migration Research App, aligned with NIST CSF 2.0 and addressing OWASP Top 10 vulnerabilities.

---

## Authentication Flow

### Clerk JWT Validation

```typescript
// frontend/middleware.ts
import { authMiddleware } from '@clerk/nextjs';

export default authMiddleware({
  publicRoutes: ['/', '/sign-in', '/sign-up', '/api/health'],
  afterAuth(auth, req) {
    // Redirect unauthenticated users to sign-in
    if (!auth.userId && !auth.isPublicRoute) {
      return redirectToSignIn({ returnBackUrl: req.url });
    }
  },
});
```

```python
# backend/src/auth.py
from clerk_backend_api import Clerk
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

clerk = Clerk(api_key=settings.CLERK_SECRET_KEY)
security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> str:
    """
    Validate Clerk JWT and return user ID
    """
    try:
        token = credentials.credentials
        # Verify JWT signature and expiration
        session = clerk.sessions.verify_token(token)
        return session.user_id
    except Exception as e:
        logger.error("JWT validation failed", error=e)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )
```

### Session Management

- **Token Expiration**: 1 hour (configurable via Clerk)
- **Refresh Token**: Handled automatically by Clerk
- **Session Revocation**: Clerk dashboard or API
- **Multi-Device**: Supported (separate sessions per device)

---

## Authorization

### Row Level Security (Supabase)

All data access enforced at database level:

```sql
-- Users can only view their own reports
CREATE POLICY "reports_select_own"
ON reports FOR SELECT
USING (
    user_id IN (
        SELECT user_id FROM users WHERE clerk_user_id = auth.jwt() ->> 'sub'
    )
    AND deleted_at IS NULL
);
```

### Authorization Matrix

| Resource | Action | Permission | RLS Policy | Application Check |
|----------|--------|------------|------------|-------------------|
| Reports | Create | Own user only | `reports_insert_own` | JWT userId validation |
| Reports | Read | Owner only | `reports_select_own` | userId = JWT sub |
| Reports | Update | Owner only | `reports_update_own` | userId = JWT sub |
| Reports | Delete | Owner only | `reports_delete_own` | userId = JWT sub |
| Payments | Create | Own user only | `payments_insert_own` | JWT userId validation |
| Payments | Read | Owner only | `payments_select_own` | userId = JWT sub |

### Local PostgreSQL Authorization

For dev mode (without Supabase RLS):

```typescript
// shared/database/src/repositories/report.ts
async findById(reportId: string, userId: string): Promise<Report | null> {
  // Application-level authorization check
  const { rows } = await this.db.query<Report>(
    `SELECT * FROM reports
     WHERE report_id = $1
       AND user_id = $2  -- Enforce ownership
       AND deleted_at IS NULL`,
    [reportId, userId]
  );
  return rows[0] || null;
}
```

---

## Data Protection

### Data-in-Transit

- **TLS 1.3**: Enforced for all HTTP traffic
- **HTTPS Only**: HTTP requests redirected to HTTPS
- **Certificate**: Managed by Vercel (frontend) and Google Cloud Run (backend)
- **HSTS**: Strict-Transport-Security header enabled

```typescript
// next.config.mjs
export default {
  async headers() {
    return [
      {
        source: '/(.*)',
        headers: [
          {
            key: 'Strict-Transport-Security',
            value: 'max-age=31536000; includeSubDomains; preload',
          },
        ],
      },
    ];
  },
};
```

### Data-at-Rest

- **Database Encryption**: AES-256 (Supabase default)
- **Secrets Encryption**: Google Secret Manager (AES-256)
- **Backup Encryption**: Automated by Supabase

### Sensitive Data Handling

```typescript
// Logging sanitization
const SENSITIVE_FIELDS = [
  'password',
  'apiKey',
  'api_key',
  'token',
  'secret',
  'creditCard',
  'card_number',
  'cvv',
  'cvc',
  'ssn',
];

export function sanitize(data: any): any {
  if (typeof data !== 'object' || data === null) return data;

  const sanitized = Array.isArray(data) ? [] : {};

  for (const [key, value] of Object.entries(data)) {
    if (SENSITIVE_FIELDS.some(field => key.toLowerCase().includes(field))) {
      sanitized[key] = '[REDACTED]';
    } else if (typeof value === 'object') {
      sanitized[key] = sanitize(value);
    } else {
      sanitized[key] = value;
    }
  }

  return sanitized;
}
```

---

## Input Validation

### Frontend Validation (Zod)

```typescript
import { z } from 'zod';

const CreateReportSchema = z.object({
  subject: z.string().min(1).max(255).trim(),
  country: z.enum(['UK']),
});

// Validate before API call
try {
  const validated = CreateReportSchema.parse(formData);
  await apiClient.createReport(validated);
} catch (error) {
  if (error instanceof z.ZodError) {
    showValidationErrors(error.errors);
  }
}
```

### Backend Validation (Pydantic)

```python
from pydantic import BaseModel, Field, field_validator

class CreateReportRequest(BaseModel):
    subject: str = Field(..., min_length=1, max_length=255)
    country: str = Field(default="UK", pattern="^UK$")

    @field_validator("subject")
    @classmethod
    def validate_subject(cls, v: str) -> str:
        # Additional validation
        if any(char in v for char in ['<', '>', '"', "'"]):
            raise ValueError("Subject contains invalid characters")
        return v.strip()
```

### SQL Injection Prevention

```typescript
// ✅ GOOD: Prepared statements (parameterized queries)
await db.query(
  'SELECT * FROM reports WHERE report_id = $1 AND user_id = $2',
  [reportId, userId]
);

// ❌ BAD: String concatenation (vulnerable to SQL injection)
await db.query(
  `SELECT * FROM reports WHERE report_id = '${reportId}'`
);
```

---

## XSS Prevention

### Content Security Policy

```typescript
// next.config.mjs
const cspHeader = `
  default-src 'self';
  script-src 'self' 'unsafe-eval' 'unsafe-inline' https://clerk.com;
  style-src 'self' 'unsafe-inline';
  img-src 'self' blob: data: https://clerk.com;
  font-src 'self';
  connect-src 'self' https://api.studyabroad.example.com https://clerk.com;
  frame-src https://clerk.com;
`;

export default {
  async headers() {
    return [
      {
        source: '/(.*)',
        headers: [
          {
            key: 'Content-Security-Policy',
            value: cspHeader.replace(/\s{2,}/g, ' ').trim(),
          },
        ],
      },
    ];
  },
};
```

### React Auto-Escaping

React automatically escapes user input in JSX:

```typescript
// Safe by default
<div>{userInput}</div>

// Dangerous (avoid unless necessary)
<div dangerouslySetInnerHTML={{ __html: sanitizedHTML }} />
```

---

## CSRF Protection

### SameSite Cookies

```typescript
// Clerk session cookies automatically use SameSite=Lax
// Custom cookies:
res.setHeader(
  'Set-Cookie',
  `session=${sessionId}; HttpOnly; Secure; SameSite=Strict; Path=/`
);
```

### CSRF Tokens (for state-changing operations)

```typescript
// Generate CSRF token
import { createCsrfToken, verifyCsrfToken } from '@/lib/csrf';

// In form
const csrfToken = createCsrfToken();
<input type="hidden" name="_csrf" value={csrfToken} />

// In API handler
const tokenValid = verifyCsrfToken(req.body._csrf, req.cookies.sessionId);
if (!tokenValid) {
  throw new Error('Invalid CSRF token');
}
```

---

## Rate Limiting

### API Rate Limiting

```python
# backend/src/middleware/rate_limit.py
from fastapi import Request
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.post("/api/reports")
@limiter.limit("10/day")  # 10 reports per user per day
async def create_report(request: Request, user_id: str = Depends(get_current_user)):
    # Rate limit by user ID, not IP
    limiter.key_func = lambda: user_id
    # ... report creation logic
```

### Report Generation Rate Limits

| User Type | Daily Limit | Per Hour | Per Minute |
|-----------|-------------|----------|------------|
| Free | 10 reports | 5 reports | 1 report |
| Premium | 100 reports | 20 reports | 5 reports |

---

## Secrets Management

### Development (Local)

```env
# .env.dev (NOT committed to git)
CLERK_SECRET_KEY=clerk_dev_xxxxx
GEMINI_API_KEY=AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXX
DATABASE_URL=postgresql://studyabroad:pass@localhost:5432/studyabroad_dev
```

### Production (Google Secret Manager)

```yaml
# cloudbuild.yaml
steps:
  - name: gcr.io/cloud-builders/gcloud
    entrypoint: bash
    args:
      - '-c'
      - |
        gcloud secrets versions access latest --secret=CLERK_SECRET_KEY > /workspace/clerk_secret.txt
        gcloud secrets versions access latest --secret=GEMINI_API_KEY > /workspace/gemini_api_key.txt
```

```python
# backend/src/config.py
from google.cloud import secretmanager

def load_secret(secret_name: str) -> str:
    """Load secret from Google Secret Manager"""
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{PROJECT_ID}/secrets/{secret_name}/versions/latest"
    response = client.access_secret_version(request={"name": name})
    return response.payload.data.decode("UTF-8")

# Usage
CLERK_SECRET_KEY = load_secret("CLERK_SECRET_KEY")
```

### Secret Rotation (Future)

- **API Keys**: Rotate every 90 days
- **Database Passwords**: Rotate every 30 days
- **JWT Signing Keys**: Handled by Clerk

---

## Logging Security

### Log Sanitization

```typescript
// Automatically redact sensitive data
logger.info('Payment created', sanitize({
  userId: 'user-123',
  cardNumber: '4242424242424242', // Redacted
  amount: 2.99,
}));

// Output:
{
  userId: 'user-123',
  cardNumber: '[REDACTED]',
  amount: 2.99
}
```

### Audit Logging

Log all security-relevant events:

```typescript
// Authentication events
logger.info('User authenticated', {
  userId: user.id,
  provider: 'google',
  ipAddress: req.ip,
  userAgent: req.headers['user-agent'],
});

// Authorization failures
logger.warn('Unauthorized access attempt', {
  userId: user.id,
  resourceId: reportId,
  action: 'view',
  ipAddress: req.ip,
});

// Payment events
logger.info('Payment succeeded', {
  userId: user.id,
  paymentId: payment.id,
  amount: 2.99,
});
```

---

## Threat Model Mitigations

### OWASP Top 10 Coverage

| Threat | Mitigation | Implementation |
|--------|------------|----------------|
| A01 Broken Access Control | RLS + Application checks | Supabase RLS policies, userId validation |
| A02 Cryptographic Failures | TLS 1.3, AES-256 | Enforced HTTPS, encrypted database |
| A03 Injection | Prepared statements | Parameterized queries, Pydantic validation |
| A04 Insecure Design | Threat modeling | Security design document (this doc) |
| A05 Security Misconfiguration | Fail-fast config | Zod/Pydantic validation on startup |
| A06 Vulnerable Components | SBOM + updates | Dependabot, npm audit, pip audit |
| A07 Authentication Failures | Clerk OAuth 2.0 | MFA support, password policies |
| A08 Software/Data Integrity | RLS + soft delete | Citations mandatory, audit trail |
| A09 Logging Failures | Structured logging | Correlation IDs, 30-day retention |
| A10 SSRF | Input validation | URL validation, whitelist external APIs |

---

## Incident Response

### Detection

1. **Monitoring**: CloudWatch logs for error spikes
2. **Alerts**: Rate limit violations, repeated auth failures
3. **Correlation IDs**: Track request flow for forensic analysis

### Response Procedure

1. **Identify**: Analyze logs with correlation ID
2. **Contain**: Revoke compromised sessions via Clerk
3. **Eradicate**: Fix vulnerability, rotate secrets
4. **Recover**: Restore from soft-deleted data if needed
5. **Lessons Learned**: Update threat model and security design

---

## Compliance

### GDPR Considerations (Future)

- **Right to Erasure**: Soft delete supports data recovery for disputes; purge after retention period
- **Data Portability**: Export reports as JSON/PDF
- **Consent**: Terms of service acceptance required

### Payment Card Industry (PCI DSS)

- **Stripe Compliance**: Stripe handles PCI compliance
- **No Card Storage**: Never store card details in our database
- **TLS Required**: All payment data transmitted over HTTPS

---

## Related Documentation

- [Threat Model](/Users/vihang/projects/study-abroad/docs/threat-model.md)
- [ADR-0001: Environment Configuration](/Users/vihang/projects/study-abroad/docs/adr/ADR-0001-environment-configuration-system.md)
- [Error Handling Design](/Users/vihang/projects/study-abroad/docs/design/error-handling.md)
- [Database RLS Policies](/Users/vihang/projects/study-abroad/docs/database/rls-policies.sql)
