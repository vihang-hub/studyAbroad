# Gate 7: Security Review & Audit

**Purpose**: Verify implementation meets NIST CSF 2.0 security requirements and has no vulnerabilities.

**When**: After Gate 6 passes, before deployment.

**Owner**: Security Gate Engineer / Security Reviewer

---

## PASS/FAIL Criteria

### PASS Requirements (All must be true)

- [ ] **NIST CSF 2.0 - IDENTIFY**
  - Software Bill of Materials (SBOM) generated and current
  - Dependencies tracked (package.json, requirements.txt, etc.)
  - SBOM document exists at `docs/security/sbom.md` or `.txt`
  - No known critical vulnerabilities in dependencies

- [ ] **NIST CSF 2.0 - PROTECT**
  - **Identity & Access Management (IAM)**:
    - OAuth 2.0 implemented (Google via Auth.js or Clerk)
    - Least-privileged scopes configured
    - Session management secure (httpOnly cookies, SameSite)
  - **Zero-Exposure Secrets**:
    - No secrets in code or frontend
    - All API keys in secret manager (Vercel env, GCP Secret Manager)
    - Environment variables for config
  - **Data-at-Rest Encryption**:
    - Database encrypted (AES-256 via Supabase default)
    - File storage encrypted (if applicable)
  - **Data-in-Transit Encryption**:
    - TLS 1.3 enforced for all endpoints
    - No HTTP, only HTTPS
    - HSTS headers configured

- [ ] **NIST CSF 2.0 - DETECT**
  - Authentication events logged centrally
  - API anomalies logged (rate limiting, errors, unauthorized access)
  - Logging dashboard configured or documented
  - Log retention policy stated

- [ ] **NIST CSF 2.0 - RESPOND**
  - Incident response plan documented (or referenced)
  - Security contact defined
  - Vulnerability disclosure process documented

- [ ] **Row-Level Security (RLS) Enforced**
  - Supabase RLS policies active on all tables
  - User isolation verified (users can't access others' data)
  - RLS tests passing (authorization test suite)

- [ ] **Input Validation & Sanitization**
  - All user inputs validated (frontend and backend)
  - SQL injection prevention (parameterized queries, ORM)
  - XSS prevention (escaped outputs, Content Security Policy)
  - CSRF protection enabled (tokens or SameSite cookies)

- [ ] **Security Documentation Complete**
  - `docs/security-controls.md` exists with NIST CSF mapping
  - `docs/security-logging.md` exists with logging details
  - Security testing results documented

- [ ] **No Third-Party Trackers** (unless specified in spec)
  - No Google Analytics, Facebook Pixel, etc. unless in spec.md
  - All external scripts audited and approved

### FAIL Conditions (Any triggers FAIL)

- Critical vulnerabilities in dependencies (CVSS ≥7.0)
- Secrets in code or frontend
- TLS 1.3 not enforced or HTTP accessible
- Authentication or authorization bypasses possible
- RLS disabled or bypassable
- No logging for security events
- SQL injection, XSS, or CSRF vulnerabilities present
- Undocumented third-party scripts/trackers
- Missing security documentation

---

## Security Audit Checklist

### Authentication & Authorization
- [ ] OAuth 2.0 flow tested (login, logout, token refresh)
- [ ] Least-privileged scopes verified (only read profile, not all contacts)
- [ ] Session expiration enforced
- [ ] Unauthorized access blocked (401/403 responses)
- [ ] RLS prevents cross-user data access

### Secrets Management
- [ ] No hardcoded API keys in code
- [ ] Environment variables used for all secrets
- [ ] Secrets not exposed in browser DevTools or logs
- [ ] Secret manager configured (Vercel env vars, GCP Secret Manager)

### Encryption
- [ ] HTTPS enforced (301 redirect from HTTP)
- [ ] TLS 1.3 negotiated (check with SSL Labs or curl)
- [ ] Database encryption confirmed (Supabase default AES-256)
- [ ] No sensitive data in URL parameters (use POST body)

### Input Validation
- [ ] Email validation regex correct
- [ ] Password complexity enforced
- [ ] File upload restrictions (size, type, sanitization)
- [ ] API rate limiting configured
- [ ] SQL parameterized queries (no string concatenation)

### Logging & Monitoring
- [ ] Failed login attempts logged
- [ ] API errors logged (500, 401, 403)
- [ ] Anomalies logged (unusual patterns, brute force)
- [ ] Logs centralized (not just console.log)
- [ ] Log retention configured (GDPR compliance)

### Dependency Security
- [ ] `npm audit` or `pip-audit` run (zero high/critical)
- [ ] Outdated dependencies updated
- [ ] SBOM generated (npm sbom or cyclonedx)
- [ ] License compliance checked

---

## Remediation Steps (If FAIL)

**Critical Vulnerabilities**:
1. IMMEDIATELY halt deployment
2. Update vulnerable dependencies: `npm update`, `pip install --upgrade`
3. Re-run audit until clean
4. Test application after updates

**Secrets Exposure**:
1. IMMEDIATELY rotate exposed secrets
2. Remove from code and git history (git filter-repo or BFG)
3. Move to secret manager
4. Re-deploy with new secrets

**Missing TLS/HTTPS**:
1. Configure TLS certificate (Let's Encrypt, Vercel auto, GCP managed)
2. Enforce HTTPS redirect (Next.js middleware, Cloud Run config)
3. Add HSTS header: `Strict-Transport-Security: max-age=31536000`
4. Test with SSL Labs

**RLS Bypass**:
1. Review RLS policies in Supabase
2. Add missing policies for all tables
3. Test with different user accounts
4. Verify RLS enforced on all query types (SELECT, INSERT, UPDATE, DELETE)

**Missing Logging**:
1. Implement centralized logging (Winston, Pino, Python logging)
2. Log authentication events (login, logout, failures)
3. Log API anomalies (rate limits, errors)
4. Configure log aggregation (GCP Logging, Datadog, etc.)

**Input Validation Gaps**:
1. Add validation library (Zod, Joi, Pydantic)
2. Validate all inputs at API boundaries
3. Sanitize outputs (use templating engines, not string concat)
4. Add CSRF tokens (NextAuth auto-handles)

**Third-Party Scripts**:
1. Audit all external scripts in HTML/head
2. Either: Remove OR add to spec.md with ADR
3. Implement Content Security Policy (CSP) header
4. Test CSP enforcement

---

## Security Testing Tools

- **Dependency Audit**: `npm audit`, `pip-audit`, Snyk
- **SBOM Generation**: `npm sbom`, CycloneDX
- **TLS Testing**: SSL Labs, `curl -vI https://...`
- **SAST**: ESLint security plugin, Bandit (Python)
- **DAST**: OWASP ZAP, Burp Suite
- **RLS Testing**: Manual tests with different user accounts

---

## Output

**If PASS**:
- Security documentation complete:
  - `docs/security-controls.md` with NIST CSF mapping
  - `docs/security-logging.md` with logging details
  - `docs/security/sbom.md` or `.txt` with dependency list
- Audit results documented (no critical vulnerabilities)
- Security sign-off from reviewer
- Proceed to Gate 8 (Deployment)

**If FAIL**:
- Security report documenting:
  - Vulnerabilities with CVSS scores
  - Evidence (screenshots, curl outputs, dependency reports)
  - Remediation steps with priority
  - Re-test requirements
- BLOCK deployment until all critical issues resolved

---

**Last Updated**: 2025-12-29 | **Constitution Version**: 1.0.0
