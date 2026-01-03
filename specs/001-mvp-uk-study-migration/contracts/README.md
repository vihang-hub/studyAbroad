# API Contracts

This directory contains pointers to the centralized API contracts for the MVP UK Study & Migration Research App.

## Centralized OpenAPI Specification

The complete API contract is maintained in the main documentation directory:

**Location**: `../../docs/api/openapi.yaml`

**Absolute Path**: `/Users/vihang/projects/study-abroad/docs/api/openapi.yaml`

## Why Centralized?

Following Speckit governance and DRY principles, API contracts are centralized to:
1. **Single Source of Truth**: Avoid duplication across feature specs
2. **Consistency**: All features reference the same versioned specification
3. **Tooling**: Enable automatic validation, code generation, and documentation
4. **Maintenance**: Updates in one place propagate to all consumers

## Viewing the API Specification

### Online Documentation (via Redocly)

```bash
npx @redocly/cli preview-docs ../../docs/api/openapi.yaml
```

Open `http://localhost:8080` to view interactive API documentation.

### Command Line Validation

```bash
npx @redocly/cli lint ../../docs/api/openapi.yaml
```

### VS Code Extension

Install "OpenAPI (Swagger) Editor" extension to view/edit with IntelliSense.

## API Overview

The OpenAPI specification documents 10 core endpoints:

### Authentication & Users
- `POST /api/auth/signup` - Create new user account (Clerk webhook)
- `GET /api/users/me` - Get current user profile

### Reports
- `POST /api/reports` - Create new report (requires payment)
- `GET /api/reports` - List user's reports (paginated)
- `GET /api/reports/{id}` - Retrieve specific report
- `DELETE /api/reports/{id}` - Early deletion (optional)
- `GET /api/stream/reports/{id}` - Server-Sent Events stream for generation progress

### Payments
- `POST /api/payments/create-intent` - Create Stripe PaymentIntent
- `POST /api/webhooks/stripe` - Stripe webhook handler (signature-verified)

### Health & Monitoring
- `GET /api/health` - Environment-aware health check

## Key Features

### Feature Flag Support
Endpoints automatically adapt based on environment variables:
- `ENABLE_PAYMENTS=false` → Bypass payment checks (dev/test modes)
- `ENABLE_SUPABASE=false` → Use local PostgreSQL (dev mode)

### Security
- All endpoints require Clerk JWT authentication (except webhooks)
- Row-Level Security (RLS) enforced at database level
- Correlation IDs in all error responses

### Streaming
- Server-Sent Events (SSE) for real-time report generation updates
- Progress tracking via `section` events
- Graceful fallback to polling if stream fails

### Error Handling
Standardized error response format:
```json
{
  "error": {
    "code": "PAYMENT_FAILED",
    "message": "User-friendly message",
    "correlationId": "uuid-v4",
    "timestamp": "2025-12-31T12:00:00Z"
  }
}
```

## Schema Validation

### TypeScript (Frontend)

Zod schemas are auto-generated from OpenAPI spec:

```typescript
// Generated from openapi.yaml
import { z } from 'zod';

export const CreateReportRequestSchema = z.object({
  subject: z.string().min(1).max(200),
  paymentIntentId: z.string().optional()
});
```

Location: `shared/config/src/schemas/api.schema.ts`

### Python (Backend)

Pydantic models match OpenAPI spec:

```python
# backend/src/models/schemas.py
from pydantic import BaseModel, Field

class CreateReportRequest(BaseModel):
    subject: str = Field(..., min_length=1, max_length=200)
    payment_intent_id: str | None = None
```

## Related Documentation

- **Database Schema**: `../../docs/database/schema.sql`
- **RLS Policies**: `../../docs/database/rls-policies.sql`
- **Error Handling**: `../../docs/design/error-handling.md`
- **Security Design**: `../../docs/design/security.md`
- **UX Flows**: `../../docs/flows/`

## Implementation Checklist

When implementing endpoints:

- [ ] Request/response matches OpenAPI spec exactly
- [ ] Feature flags respected (`ENABLE_PAYMENTS`, `ENABLE_SUPABASE`)
- [ ] Authentication verified (Clerk JWT)
- [ ] RLS policies enforced (database level)
- [ ] Correlation IDs added to logs
- [ ] Error responses use standard format
- [ ] Tests cover all response codes (200, 400, 401, 404, 500)
- [ ] OpenAPI spec updated if endpoint changes

## Code Generation

### Generate TypeScript Types

```bash
npx openapi-typescript ../../docs/api/openapi.yaml -o shared/config/src/types/api.types.ts
```

### Generate Python Models

```bash
datamodel-codegen \
  --input ../../docs/api/openapi.yaml \
  --output backend/src/models/generated.py \
  --input-file-type openapi
```

## Versioning

API follows semantic versioning:
- **Current Version**: `v1` (MVP)
- **Breaking Changes**: Require new version (`v2`)
- **Non-Breaking Changes**: Can update `v1` spec

Version is included in base path: `/api/v1/...`

## Testing

### Manual API Testing (via curl)

```bash
# Health check
curl http://localhost:8000/api/health

# Create report (dev mode, no payment)
curl -X POST http://localhost:8000/api/reports \
  -H "Authorization: Bearer ${CLERK_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"subject": "Computer Science"}'

# List reports
curl http://localhost:8000/api/reports \
  -H "Authorization: Bearer ${CLERK_TOKEN}"
```

### Integration Tests

See `backend/tests/test_api_endpoints.py` for comprehensive API tests covering:
- All endpoints
- All response codes
- Feature flag variations
- Error conditions

## OpenAPI Specification Highlights

**Spec Version**: OpenAPI 3.1
**Base URL**: `http://localhost:8000/api` (dev), `https://api.studyabroad.com/api` (production)
**Authentication**: Bearer token (Clerk JWT)
**Content-Type**: `application/json` (except SSE endpoints)

**Tags**:
- `Authentication` - User management
- `Reports` - Report CRUD and streaming
- `Payments` - Payment processing
- `Health` - Monitoring

---

**For the complete, authoritative API specification, always refer to:**

`../../docs/api/openapi.yaml` (28,903 bytes, ~800 lines)
