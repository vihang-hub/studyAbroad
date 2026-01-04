# Gate2: Design Checklist

**Feature**: _{feature_name}_
**Date**: _{date}_
**Agent**: designer

---

## Prerequisites

- [ ] Gate1-Architecture.md passed
- [ ] spec.md approved with acceptance criteria
- [ ] System overview and ADRs exist

---

## API Design

### OpenAPI Specification

- [ ] `docs/api/openapi.yaml` exists
- [ ] All endpoints documented
- [ ] Request/response schemas defined
- [ ] Authentication requirements specified
- [ ] Error responses documented

### Endpoint Inventory

| Endpoint | Method | Auth Required | Request Schema | Response Schema |
|----------|--------|---------------|----------------|-----------------|
| _{path}_ | GET/POST/etc | Yes/No | _{schema}_ | _{schema}_ |

---

## UI/UX Design

### User Flows

- [ ] `docs/ui/flows.md` exists
- [ ] Primary user journey documented
- [ ] Error states designed
- [ ] Loading states designed
- [ ] Edge cases covered

### Flow Diagrams

| Flow | Description | Diagram | Status |
|------|-------------|---------|--------|
| _{flow_name}_ | _{description}_ | _{path}_ | ⏳/✅ |

---

## Data Design

### Schema Definition

- [ ] `docs/data/schema.md` exists
- [ ] All entities documented
- [ ] Relationships defined
- [ ] Indexes planned
- [ ] Migrations planned

### Access Control

- [ ] Row Level Security (RLS) policies defined
- [ ] User isolation documented
- [ ] Admin access documented

---

## Contract Testing Requirements

**CRITICAL**: Contracts must be defined BEFORE implementation to prevent frontend/backend mismatches.

### API Path Contracts

Define the exact paths that frontend will call and backend will serve:

| Frontend Path | Backend Route | Match | Notes |
|---------------|---------------|-------|-------|
| `/api/users` | `GET /users` | ✅/❌ | _{any path transformation}_ |
| `/api/reports/{id}` | `GET /reports/{id}` | ✅/❌ | _{notes}_ |

### Request/Response Contracts

For each endpoint, verify types match:

| Endpoint | Frontend Type | Backend Schema | Match |
|----------|---------------|----------------|-------|
| `POST /auth/login` | `LoginRequest` | `LoginRequestSchema` | ✅/❌ |
| `GET /reports` | `Report[]` | `ReportListResponse` | ✅/❌ |

### Authentication Contract

Document the exact auth mechanism:

| Aspect | Specification |
|--------|---------------|
| Header Name | `Authorization` |
| Header Format | `Bearer {token}` |
| Token Provider | _{Clerk, Auth0, Custom JWT}_ |
| Token Retrieval | _{e.g., getToken() from useAuth()}_ |

### Error Contract

Document error response format:

```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human readable message",
    "details": {}
  }
}
```

- [ ] Frontend error handling matches backend error format
- [ ] Error codes are documented
- [ ] HTTP status codes are consistent

### Contract Verification Approach

Choose one:

- [ ] **Generated Types**: Types generated from OpenAPI spec (recommended)
  - Tool: _{openapi-typescript, swagger-codegen}_
  - Generated files: _{paths}_

- [ ] **Contract Tests**: Tests verify contracts at build time
  - Test file: `tests/contracts/api-contracts.test.ts`
  - Runs in: CI pipeline

- [ ] **Manual Verification**: Types manually kept in sync
  - Review checklist in PR template
  - Risk: Higher chance of drift

### Contract Test Template

```typescript
// tests/contracts/api-contracts.test.ts
import { paths } from '../generated/api-types'; // If using generated types
import spec from '../docs/api/openapi.yaml';

describe('API Contracts', () => {
  describe('Path Contracts', () => {
    it('frontend paths match OpenAPI spec', () => {
      const frontendPaths = ['/reports', '/reports/:id', '/auth/login'];
      const specPaths = Object.keys(spec.paths);

      frontendPaths.forEach(path => {
        expect(specPaths).toContain(path);
      });
    });
  });

  describe('Auth Contracts', () => {
    it('protected endpoints require Bearer token', () => {
      const protectedEndpoints = ['/reports', '/users/me'];

      protectedEndpoints.forEach(endpoint => {
        expect(spec.paths[endpoint].security).toBeDefined();
      });
    });
  });
});
```

---

## Constitution Alignment

- [ ] Technical stack matches constitution
- [ ] Security requirements met
- [ ] Naming conventions followed
- [ ] No prohibited practices

---

## Artifacts Created

- [ ] `docs/api/openapi.yaml` - API specification
- [ ] `docs/ui/flows.md` - User flow documentation
- [ ] `docs/data/schema.md` - Data model
- [ ] `docs/data/rls-policies.md` - Access control (if applicable)
- [ ] `tests/contracts/` - Contract tests (if using contract testing)

---

## Gate Result

**Status**: ⏳ PENDING | ✅ PASS | ❌ FAIL

**Summary**:
- API endpoints defined: _{count}_
- User flows documented: _{count}_
- Data entities defined: _{count}_
- Contracts verified: _{yes/no}_

**Contract Status**:
| Contract Type | Status |
|---------------|--------|
| API Paths | ✅/❌ |
| Request/Response | ✅/❌ |
| Authentication | ✅/❌ |
| Errors | ✅/❌ |

**Notes**:
_{any issues, decisions, or open questions}_

---

**Reviewed by**: designer agent
**Date**: _{date}_
