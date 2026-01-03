# Threat Model: MVP UK Study & Migration Research App

**Document Version**: 2.0.0
**Last Updated**: 2025-12-31
**Related**: [System Architecture Overview](/Users/vihang/projects/study-abroad/docs/architecture/system-overview.md)

## Table of Contents

1. [Assets](#assets)
2. [Threat Actors](#threat-actors)
3. [Attack Vectors](#attack-vectors)
4. [Mitigations](#mitigations)
5. [Residual Risks](#residual-risks)
6. [NIST CSF Alignment](#nist-csf-alignment)

---

## Assets

### Critical Assets Requiring Protection

1. **User Personal Data (PII)**
   - User IDs, email addresses (from Clerk)
   - Authentication tokens (JWT, OAuth tokens)
   - Payment information (Stripe customer IDs, payment intents)
   - **Classification**: High sensitivity
   - **Location**: Clerk (external), Supabase database

2. **Generated Reports**
   - AI-generated research content
   - Subject matter, country preferences
   - Citations and source data
   - **Classification**: Medium sensitivity (paid content)
   - **Location**: Supabase/PostgreSQL database

3. **API Keys and Secrets**
   - Gemini AI API key
   - Stripe API keys (secret, publishable)
   - Clerk API keys
   - Supabase credentials (URL, anon key, service role key)
   - **Classification**: Critical (system compromise if leaked)
   - **Location**: Google Secret Manager, Vercel Environment Variables

4. **Application Logs**
   - Request logs with correlation IDs
   - Error logs with stack traces
   - Authentication event logs
   - Payment transaction logs
   - **Classification**: High sensitivity (may contain PII, debugging data)
   - **Location**: File system (`/logs`), potentially Cloud Logging

5. **Database**
   - User records
   - Report records (including soft-deleted)
   - Payment records
   - **Classification**: High sensitivity (multi-tenant data)
   - **Location**: Supabase (test/prod), PostgreSQL (dev)

---

## Threat Actors

### External Threat Actors

1. **Opportunistic Attackers**
   - **Motivation**: Financial gain, credential theft
   - **Capabilities**: Automated scanning tools, known exploit databases
   - **Likelihood**: High
   - **Impact**: Medium to High

2. **Targeted Attackers**
   - **Motivation**: Competitive intelligence, data exfiltration
   - **Capabilities**: Custom exploits, social engineering
   - **Likelihood**: Low to Medium
   - **Impact**: High

3. **Script Kiddies**
   - **Motivation**: Curiosity, reputation
   - **Capabilities**: Publicly available exploit tools
   - **Likelihood**: High
   - **Impact**: Low to Medium

### Internal Threat Actors

4. **Malicious Insiders**
   - **Motivation**: Financial gain, sabotage
   - **Capabilities**: Access to internal systems, codebase
   - **Likelihood**: Low
   - **Impact**: Critical

5. **Negligent Insiders**
   - **Motivation**: None (accidental)
   - **Capabilities**: Accidental secret exposure, misconfigurations
   - **Likelihood**: Medium
   - **Impact**: Medium to High

---

## Attack Vectors

### OWASP Top 10 Mapping

#### A01:2021 - Broken Access Control

**Vector**: Unauthorized access to other users' reports

**Attack Scenario**:
1. Attacker obtains valid JWT token
2. Attacker modifies `reportId` in API request to access another user's report
3. Backend fails to validate `userId` ownership

**Likelihood**: Medium
**Impact**: High (data breach)

**Mitigation**:
- ✅ Row Level Security (RLS) enforced on Supabase
- ✅ Repository pattern enforces `userId` filtering in all queries
- ✅ All `findById` methods require both `reportId` AND `userId`

**Validation**:
```sql
-- RLS Policy
CREATE POLICY "Users can view their own reports"
  ON reports FOR SELECT
  USING (auth.uid() = user_id AND deleted_at IS NULL);
```

#### A02:2021 - Cryptographic Failures

**Vector**: Sensitive data exposure in logs, storage, or transit

**Attack Scenario**:
1. API keys or passwords logged in debug logs
2. Attacker gains access to log files
3. Attacker extracts secrets and compromises system

**Likelihood**: Medium
**Impact**: Critical

**Mitigation**:
- ✅ Sensitive data sanitization in logging (ADR-0004)
- ✅ TLS 1.3 for data-in-transit
- ✅ AES-256 database encryption for data-at-rest
- ✅ Secrets in Google Secret Manager / Vercel (not in code)
- ✅ Log files have restricted file permissions (600)

**Validation**:
```typescript
// shared/logging/src/sanitizer.ts
const SENSITIVE_PATTERNS = [
  /password/i, /secret/i, /token/i, /api[_-]?key/i,
  /authorization/i, /cookie/i, /ssn/i, /credit[_-]?card/i
];

export function sanitizeLogData(data: any): any {
  // Redacts sensitive fields before logging
}
```

#### A03:2021 - Injection

**Vector**: SQL Injection via user input in report queries

**Attack Scenario**:
1. Attacker provides malicious subject name: `'; DROP TABLE reports; --`
2. Backend constructs SQL query with string concatenation
3. Database executes malicious SQL

**Likelihood**: Low (mitigated by design)
**Impact**: Critical

**Mitigation**:
- ✅ Prepared statements via asyncpg (Python)
- ✅ Parameterized queries in repository pattern
- ✅ No raw SQL string concatenation
- ✅ Zod/Pydantic input validation

**Validation**:
```typescript
// All queries use parameterization
await this.db.query(
  `SELECT * FROM reports WHERE report_id = $1 AND user_id = $2`,
  [reportId, userId]  // ← Parameters, not concatenation
);
```

#### A04:2021 - Insecure Design

**Vector**: Payment bypass in dev/test environments

**Attack Scenario**:
1. Attacker discovers `ENABLE_PAYMENTS=false` in test environment
2. Attacker generates unlimited free reports
3. System loses revenue

**Likelihood**: Medium
**Impact**: Medium (revenue loss)

**Mitigation**:
- ✅ Feature flags logged for audit trail
- ✅ Test environment access restricted (not public)
- ✅ Production always enforces payments (`ENABLE_PAYMENTS=true`)
- ✅ Environment configuration validated on startup

**Validation**:
```env
# Production .env (enforced)
ENVIRONMENT_MODE=production
ENABLE_PAYMENTS=true  # ← Must be true in production
```

#### A05:2021 - Security Misconfiguration

**Vector**: Debug logs enabled in production

**Attack Scenario**:
1. Developer forgets to set `LOG_LEVEL=error` in production
2. Debug logs expose sensitive request/response data
3. Attacker accesses log files

**Likelihood**: Low (mitigated by presets)
**Impact**: High

**Mitigation**:
- ✅ Environment presets enforce correct log levels (ADR-0001)
- ✅ Production preset: `LOG_LEVEL=error`
- ✅ CI/CD validation of environment configuration
- ✅ Configuration schema validation (Zod/Pydantic)

**Validation**:
```typescript
// shared/config/src/presets.ts
export const PRODUCTION_PRESET: Partial<AppConfig> = {
  ENVIRONMENT_MODE: 'production',
  LOG_LEVEL: 'error',  // ← Enforced
};
```

#### A06:2021 - Vulnerable and Outdated Components

**Vector**: Dependency vulnerabilities

**Attack Scenario**:
1. Application uses vulnerable version of library
2. Attacker exploits known CVE
3. Remote code execution or data breach

**Likelihood**: Medium
**Impact**: Critical

**Mitigation**:
- ✅ SBOM maintained via npm/pip (Constitution Section 2)
- ✅ Dependabot enabled for automated security updates
- ✅ `npm audit` / `pip-audit` in CI/CD pipeline
- ✅ Quarterly dependency review

**Validation**:
```bash
# CI/CD check
npm audit --audit-level=high
pip-audit
```

#### A07:2021 - Identification and Authentication Failures

**Vector**: Authentication bypass or session hijacking

**Attack Scenario**:
1. Attacker steals JWT token via XSS or network interception
2. Attacker impersonates user
3. Attacker accesses user's reports and payment data

**Likelihood**: Low (mitigated by Clerk)
**Impact**: High

**Mitigation**:
- ✅ Clerk handles authentication (battle-tested library)
- ✅ JWT tokens short-lived (15 minutes)
- ✅ HTTPS/TLS enforced (no HTTP)
- ✅ SameSite cookies prevent CSRF
- ✅ Authentication events logged

**Validation**:
- Clerk security: [https://clerk.com/security](https://clerk.com/security)
- JWT expiration enforced

#### A08:2021 - Software and Data Integrity Failures

**Vector**: Compromised CI/CD pipeline or npm packages

**Attack Scenario**:
1. Attacker compromises npm package dependency
2. Malicious code injected into build
3. Application compromised in production

**Likelihood**: Low
**Impact**: Critical

**Mitigation**:
- ✅ npm audit in CI/CD
- ✅ Lock files (package-lock.json, poetry.lock)
- ✅ Code review for dependency changes
- ✅ GitHub Actions security scanning

**Validation**:
```bash
# Lock files prevent unexpected updates
npm ci  # Uses package-lock.json exactly
```

#### A09:2021 - Security Logging and Monitoring Failures

**Vector**: Security events not logged or monitored

**Attack Scenario**:
1. Attacker performs reconnaissance scans
2. No logs or alerts generated
3. Attacker proceeds to exploitation undetected

**Likelihood**: Medium
**Impact**: Medium

**Mitigation**:
- ✅ Structured logging with correlation IDs (ADR-0004)
- ✅ Authentication events logged
- ✅ Payment transactions logged
- ✅ API errors logged
- ✅ Log retention for 30 days

**Validation**:
```typescript
logger.warn('Authentication failed', {
  provider: 'google',
  reason: 'invalid_token',
  ipAddress: req.ip,
});
```

#### A10:2021 - Server-Side Request Forgery (SSRF)

**Vector**: SSRF via Gemini AI API prompts

**Attack Scenario**:
1. Attacker crafts malicious subject input
2. AI service fetches internal resources
3. Internal data leaked

**Likelihood**: Low (LangChain/Gemini handles this)
**Impact**: Medium

**Mitigation**:
- ✅ Input validation on subject field
- ✅ LangChain/Gemini handles prompt safety
- ✅ No user-controlled URLs in backend

---

## Additional Attack Vectors

### Log File Exposure

**Vector**: Unauthorized access to log files

**Attack Scenario**:
1. Log files stored with world-readable permissions
2. Attacker accesses server or container
3. Attacker reads logs containing sensitive data

**Likelihood**: Low
**Impact**: High

**Mitigation**:
- ✅ Log files have restricted permissions (600, owner-only)
- ✅ Sensitive data sanitization before logging
- ✅ Logs not accessible via HTTP
- ✅ Cloud Run containers have ephemeral file systems

**Validation**:
```bash
# Log file permissions
-rw------- 1 app app  100M Dec 31 12:00 app-2025-12-31-1.log
```

### Soft-Deleted Data Exposure

**Vector**: Soft-deleted reports accessible via direct query

**Attack Scenario**:
1. Developer writes query without `WHERE deleted_at IS NULL`
2. Soft-deleted reports exposed to users
3. Users access expired content without payment

**Likelihood**: Medium
**Impact**: Medium

**Mitigation**:
- ✅ Repository pattern enforces `whereActive()` filter
- ✅ RLS policies exclude soft-deleted records
- ✅ Partial indexes optimize active record queries
- ✅ Linting rules warn about missing filters

**Validation**:
```typescript
// All queries use whereActive()
protected whereActive(): string {
  return 'deleted_at IS NULL';
}
```

### Environment Variable Leakage

**Vector**: `.env` files committed to git

**Attack Scenario**:
1. Developer commits `.env` with production secrets
2. Git history contains secrets
3. Attacker clones repository and extracts secrets

**Likelihood**: Low (mitigated by .gitignore)
**Impact**: Critical

**Mitigation**:
- ✅ `.env` files in `.gitignore`
- ✅ Only `.env.example` committed (no secrets)
- ✅ git-secrets pre-commit hook (future)
- ✅ Secret rotation policy (90 days)

**Validation**:
```gitignore
.env
.env.local
.env.*.local
.env.production
!.env.example
```

---

## Mitigations

### By NIST CSF Function

#### Identify
- ✅ **Asset Inventory**: SBOM via npm/pip
- ✅ **Risk Assessment**: This threat model
- ✅ **Vulnerability Scanning**: Dependabot, npm audit, pip-audit

#### Protect
- ✅ **Access Control**: Clerk OAuth 2.0, Supabase RLS
- ✅ **Data Security**: TLS 1.3, AES-256, sensitive data redaction
- ✅ **Secrets Management**: Google Secret Manager, Vercel
- ✅ **Input Validation**: Zod, Pydantic, prepared statements

#### Detect
- ✅ **Logging**: Structured logs with correlation IDs
- ✅ **Monitoring**: Authentication failures, payment failures, API errors
- ✅ **Anomaly Detection**: (Future) Cloud Logging alerts

#### Respond
- ✅ **Incident Analysis**: 30-day log retention
- ✅ **Recovery**: Soft delete enables data restoration

#### Recover
- ✅ **Backup**: Supabase automatic backups
- ✅ **Restore**: Admin restore API for soft-deleted reports

---

## Residual Risks

### Accepted Risks

1. **Local Development Without RLS**
   - **Risk**: Local PostgreSQL doesn't enforce Row Level Security
   - **Mitigation**: Application-level authorization checks
   - **Justification**: Dev environment not exposed to internet

2. **No Real-Time Monitoring**
   - **Risk**: Security events not monitored in real-time
   - **Mitigation**: Batch log analysis, 30-day retention
   - **Justification**: MVP prioritizes core functionality; monitoring deferred to post-MVP

3. **No Web Application Firewall (WAF)**
   - **Risk**: No DDoS protection or advanced threat detection
   - **Mitigation**: Cloud Run autoscaling, rate limiting (future)
   - **Justification**: MVP traffic volume doesn't justify WAF cost

4. **File-Based Logging (No Centralized Aggregation)**
   - **Risk**: Logs local to each Cloud Run instance
   - **Mitigation**: Cloud Run instances write to ephemeral storage; logs lost on restart
   - **Justification**: MVP uses file-based logging; Cloud Logging integration deferred

5. **No Hard Delete of Soft-Deleted Reports**
   - **Risk**: Soft-deleted data accumulates indefinitely
   - **Mitigation**: None in MVP
   - **Justification**: Purge mechanism deferred to post-MVP

---

## NIST CSF Alignment

| NIST Function | Controls Implemented | Evidence |
|---------------|---------------------|----------|
| **Identify** | SBOM, Threat Model, Dependency Scanning | npm audit, pip-audit, this document |
| **Protect** | OAuth 2.0, RLS, TLS 1.3, AES-256, Secrets Management | Clerk, Supabase policies, ADR-0001 |
| **Detect** | Structured Logging, Authentication Event Logging | ADR-0004, correlation IDs |
| **Respond** | Log Analysis, Incident Response Procedures | 30-day log retention |
| **Recover** | Database Backups, Soft Delete Restoration | Supabase backups, ADR-0005 |

---

## Revision History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0.0 | 2025-12-28 | Initial threat model | Security Team |
| 2.0.0 | 2025-12-31 | Updated for logging security, soft delete, environment configs | Security Team |

---

## References

- [OWASP Top 10 2021](https://owasp.org/Top10/)
- [NIST Cybersecurity Framework 2.0](https://www.nist.gov/cyberframework)
- [System Architecture Overview](/Users/vihang/projects/study-abroad/docs/architecture/system-overview.md)
- [ADR-0001: Environment Configuration System](/Users/vihang/projects/study-abroad/docs/adr/ADR-0001-environment-configuration-system.md)
- [ADR-0004: Logging Infrastructure](/Users/vihang/projects/study-abroad/docs/adr/ADR-0004-logging-infrastructure.md)
- [ADR-0005: Soft Delete Pattern](/Users/vihang/projects/study-abroad/docs/adr/ADR-0005-soft-delete-pattern.md)
