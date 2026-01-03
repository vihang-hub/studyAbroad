# Security Checklist

## Overview
This document verifies that all security requirements are properly configured for the Study Abroad MVP application.

## HTTPS/TLS Enforcement

### Frontend (Vercel)

**Status**: ✅ **Automatically Enabled**

Vercel automatically enforces HTTPS for all deployments:
- All HTTP requests are automatically redirected to HTTPS
- SSL certificates are automatically provisioned and renewed
- HSTS (HTTP Strict Transport Security) is enabled by default

**Verification**:
```bash
# Test HTTP redirect to HTTPS
curl -I http://your-app.vercel.app
# Should return: HTTP/1.1 308 Permanent Redirect
# Location: https://your-app.vercel.app

# Verify HSTS header
curl -I https://your-app.vercel.app | grep -i strict
# Should return: Strict-Transport-Security: max-age=31536000
```

**Documentation**: [Vercel HTTPS Documentation](https://vercel.com/docs/concepts/edge-network/encryption)

### Backend (Google Cloud Run)

**Status**: ✅ **Automatically Enabled**

Cloud Run automatically enforces HTTPS for all public services:
- HTTP requests are automatically upgraded to HTTPS
- TLS 1.2 and 1.3 are supported
- SSL certificates are automatically managed by Google

**Configuration**:
```bash
# Deploy with HTTPS enforcement (default)
gcloud run deploy study-abroad-backend \
  --image gcr.io/$PROJECT_ID/study-abroad-backend \
  --region us-central1 \
  --allow-unauthenticated

# Verify HTTPS is enforced
gcloud run services describe study-abroad-backend \
  --region us-central1 \
  --format="value(status.url)"
# URL will always use https://
```

**Add HSTS Header** (recommended):

Update `backend/src/main.py`:

```python
from fastapi import FastAPI
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

class HSTSMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        return response

app = FastAPI()
app.add_middleware(HSTSMiddleware)
```

**Verification**:
```bash
# Test HTTPS endpoint
curl -I https://your-backend-url.run.app/health
# Should return: HTTP/2 200

# Verify HSTS header
curl -I https://your-backend-url.run.app/health | grep -i strict
# Should return: Strict-Transport-Security: max-age=31536000; includeSubDomains
```

**Documentation**: [Cloud Run HTTPS](https://cloud.google.com/run/docs/securing/using-https)

### Database (Supabase)

**Status**: ✅ **Enforced**

Supabase requires TLS for all database connections:
- All connections use TLS 1.2+
- Certificate verification is enabled
- Non-TLS connections are rejected

**Configuration**:

In `backend/src/lib/supabase.py`:
```python
from supabase import create_client

supabase = create_client(
    supabase_url=os.getenv("SUPABASE_URL"),
    supabase_key=os.getenv("SUPABASE_SERVICE_ROLE_KEY"),
    options={
        "db": {
            "ssl": {
                "rejectUnauthorized": True  # Enforce certificate validation
            }
        }
    }
)
```

### External APIs

**Status**: ✅ **All Use HTTPS**

All third-party APIs enforce HTTPS:
- **Stripe**: https://api.stripe.com (TLS 1.2+)
- **Clerk**: https://api.clerk.com (TLS 1.2+)
- **Gemini**: https://generativelanguage.googleapis.com (TLS 1.2+)

## Security Headers

### Recommended Headers (Frontend)

Add to `frontend/next.config.js`:

```javascript
const securityHeaders = [
  {
    key: 'X-DNS-Prefetch-Control',
    value: 'on'
  },
  {
    key: 'Strict-Transport-Security',
    value: 'max-age=63072000; includeSubDomains; preload'
  },
  {
    key: 'X-Frame-Options',
    value: 'SAMEORIGIN'
  },
  {
    key: 'X-Content-Type-Options',
    value: 'nosniff'
  },
  {
    key: 'X-XSS-Protection',
    value: '1; mode=block'
  },
  {
    key: 'Referrer-Policy',
    value: 'origin-when-cross-origin'
  },
  {
    key: 'Permissions-Policy',
    value: 'camera=(), microphone=(), geolocation=()'
  }
];

module.exports = {
  async headers() {
    return [
      {
        source: '/:path*',
        headers: securityHeaders,
      },
    ];
  },
};
```

### Recommended Headers (Backend)

Add to `backend/src/main.py`:

```python
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        return response

app.add_middleware(SecurityHeadersMiddleware)
```

## TLS Version Support

### Minimum TLS Version: 1.2

**Frontend (Vercel)**: Supports TLS 1.2 and 1.3
**Backend (Cloud Run)**: Supports TLS 1.2 and 1.3
**Database (Supabase)**: Requires TLS 1.2+

TLS 1.0 and 1.1 are deprecated and not supported.

## Certificate Management

### Automated Certificate Renewal

**Vercel**: Automatically renews SSL certificates 30 days before expiration
**Cloud Run**: Automatically manages certificates via Google-managed SSL
**Supabase**: Automatically manages database TLS certificates

No manual intervention required.

## Validation Checklist

### Pre-Production Checklist

- [ ] Vercel frontend URL uses https://
- [ ] Cloud Run backend URL uses https://
- [ ] All HTTP requests redirect to HTTPS
- [ ] HSTS headers are present (max-age=31536000)
- [ ] X-Frame-Options header is set to DENY or SAMEORIGIN
- [ ] X-Content-Type-Options header is set to nosniff
- [ ] Database connections use TLS
- [ ] Supabase SSL verification is enabled
- [ ] All external API calls use HTTPS
- [ ] No mixed content warnings in browser console
- [ ] SSL Labs test score is A or A+ (https://www.ssllabs.com/ssltest/)

### Production Deployment Checklist

- [ ] Custom domain configured with HTTPS (if applicable)
- [ ] HSTS preload enabled (optional but recommended)
- [ ] Certificate auto-renewal is working
- [ ] Security headers are present in all responses
- [ ] TLS 1.0 and 1.1 are disabled
- [ ] Content Security Policy (CSP) is configured
- [ ] CORS policy is restrictive (only allows frontend domain)

## Testing HTTPS/TLS

### Manual Testing

```bash
# 1. Test HTTPS enforcement
curl -I http://your-app.vercel.app
# Should redirect to https://

# 2. Test TLS version
openssl s_client -connect your-app.vercel.app:443 -tls1_2
# Should succeed

openssl s_client -connect your-app.vercel.app:443 -tls1_1
# Should fail (connection rejected)

# 3. Test security headers
curl -I https://your-app.vercel.app | grep -i "strict-transport-security"
curl -I https://your-backend-url.run.app | grep -i "x-frame-options"

# 4. Test SSL certificate validity
openssl s_client -connect your-app.vercel.app:443 -showcerts
# Should show valid certificate chain
```

### Automated Testing

Use SSL Labs for comprehensive TLS testing:

```bash
# API-based testing (requires API key)
curl "https://api.ssllabs.com/api/v3/analyze?host=your-app.vercel.app"
```

Or use the web interface:
https://www.ssllabs.com/ssltest/analyze.html?d=your-app.vercel.app

**Target Grade**: A or A+

### Browser Testing

1. Open DevTools (F12)
2. Go to Network tab
3. Verify all requests use HTTPS
4. Check Security tab:
   - Certificate is valid
   - Connection is secure
   - TLS 1.2 or 1.3 is used
   - No mixed content warnings

## Troubleshooting

### Mixed Content Warnings

**Problem**: Browser blocks HTTP resources loaded from HTTPS page

**Solution**:
1. Ensure all resources (images, scripts, stylesheets) use HTTPS URLs
2. Use protocol-relative URLs: `//example.com/script.js`
3. Or use environment variables: `NEXT_PUBLIC_API_URL=https://...`

### Certificate Errors

**Problem**: "Certificate not trusted" or "Certificate expired"

**Solution** (Vercel):
1. Check domain verification in Vercel dashboard
2. Wait for DNS propagation (up to 48 hours)
3. Contact Vercel support if issue persists

**Solution** (Cloud Run):
1. Verify service is deployed correctly: `gcloud run services list`
2. Check Cloud Run logs for SSL errors
3. Ensure custom domain mapping is correct (if using custom domain)

### HSTS Not Working

**Problem**: HSTS header not present in responses

**Solution**:
1. Verify middleware is added to `app` instance
2. Check order of middleware (security middleware should be early)
3. Clear browser HSTS cache: `chrome://net-internals/#hsts`

## CORS Configuration

### Overview

CORS (Cross-Origin Resource Sharing) controls which domains can make requests to your API. Proper CORS configuration is critical to prevent unauthorized access.

### Backend CORS Configuration

**Location**: `backend/src/main.py`

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,  # Configured via environment variable
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)
```

### Environment Configuration

**Development** (`backend/.env`):
```bash
ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

**Production** (Google Secret Manager or Cloud Run environment):
```bash
ALLOWED_ORIGINS=https://your-production-domain.vercel.app
```

### Security Best Practices

1. **Never use wildcard (*) in production**
   ```python
   # DON'T DO THIS IN PRODUCTION
   allow_origins=["*"]  # Allows ANY domain to access your API
   ```

2. **Only allow specific frontend domains**
   ```python
   # CORRECT
   allow_origins=["https://your-app.vercel.app"]
   ```

3. **Use HTTPS origins in production**
   ```python
   # DON'T: allow_origins=["http://your-app.com"]
   # DO: allow_origins=["https://your-app.com"]
   ```

4. **Be specific with allowed methods**
   - Only allow methods your API actually uses
   - Current configuration: `["GET", "POST", "PUT", "DELETE", "OPTIONS"]`
   - Remove unused methods if possible

5. **Validate credentials setting**
   - `allow_credentials=True` allows cookies and authorization headers
   - Only enable if your API uses authentication
   - Cannot be combined with `allow_origins=["*"]`

### Verification

#### Test CORS in Development

```bash
# Test from allowed origin (should succeed)
curl -X OPTIONS http://localhost:8000/health \
  -H "Origin: http://localhost:3000" \
  -H "Access-Control-Request-Method: GET" \
  -v

# Should return:
# Access-Control-Allow-Origin: http://localhost:3000
# Access-Control-Allow-Credentials: true

# Test from disallowed origin (should fail)
curl -X OPTIONS http://localhost:8000/health \
  -H "Origin: http://malicious-site.com" \
  -H "Access-Control-Request-Method: GET" \
  -v

# Should NOT return Access-Control-Allow-Origin header
```

#### Test CORS in Production

```bash
# Test from production frontend
curl -X OPTIONS https://your-backend.run.app/health \
  -H "Origin: https://your-app.vercel.app" \
  -H "Access-Control-Request-Method: GET" \
  -v

# Should return:
# Access-Control-Allow-Origin: https://your-app.vercel.app

# Test from unauthorized origin
curl -X OPTIONS https://your-backend.run.app/health \
  -H "Origin: https://evil.com" \
  -H "Access-Control-Request-Method: GET" \
  -v

# Should NOT return Access-Control-Allow-Origin header
```

#### Browser DevTools Testing

1. Open your frontend application in browser
2. Open DevTools (F12) → Network tab
3. Make API request to backend
4. Check response headers:
   ```
   Access-Control-Allow-Origin: https://your-app.vercel.app
   Access-Control-Allow-Credentials: true
   ```
5. Verify no CORS errors in console

### Common CORS Issues

#### Issue: CORS Error "No 'Access-Control-Allow-Origin' header"

**Cause**: Frontend domain not in ALLOWED_ORIGINS

**Solution**:
```bash
# Add frontend domain to ALLOWED_ORIGINS
ALLOWED_ORIGINS=https://your-app.vercel.app,https://your-staging.vercel.app
```

#### Issue: CORS Error "Credentials flag is 'true', but allow_origins is '*'"

**Cause**: Cannot use wildcard origins with credentials

**Solution**:
```python
# Change from:
allow_origins=["*"]

# To specific origins:
allow_origins=["https://your-app.vercel.app"]
```

#### Issue: OPTIONS Preflight Requests Failing

**Cause**: OPTIONS method not allowed

**Solution**:
```python
# Ensure OPTIONS is in allowed methods
allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"]
```

### Deployment Checklist

- [ ] ALLOWED_ORIGINS environment variable is set correctly
- [ ] Production ALLOWED_ORIGINS uses HTTPS (not HTTP)
- [ ] ALLOWED_ORIGINS does not include wildcard (*)
- [ ] Only necessary HTTP methods are allowed
- [ ] allow_credentials is appropriate for your auth strategy
- [ ] CORS headers present in all API responses
- [ ] OPTIONS preflight requests work correctly
- [ ] No CORS errors in browser console

### Monitoring

Monitor CORS-related errors:

```bash
# Search for CORS errors in Cloud Run logs
gcloud logging read "resource.type=cloud_run_revision AND textPayload=~\"CORS\"" \
  --limit 50 --format json

# Common error patterns:
# - "CORS policy: No 'Access-Control-Allow-Origin'"
# - "preflight request failed"
# - "Response to preflight request doesn't pass access control check"
```

## References

- [OWASP Transport Layer Protection Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Transport_Layer_Protection_Cheat_Sheet.html)
- [OWASP CORS Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cross-Origin_Resource_Sharing_Cheat_Sheet.html)
- [Mozilla TLS Configuration Guide](https://wiki.mozilla.org/Security/Server_Side_TLS)
- [Vercel Security Documentation](https://vercel.com/docs/concepts/security)
- [Cloud Run Security Best Practices](https://cloud.google.com/run/docs/securing)
- [SSL Labs Best Practices](https://github.com/ssllabs/research/wiki/SSL-and-TLS-Deployment-Best-Practices)
- [FastAPI CORS Documentation](https://fastapi.tiangolo.com/tutorial/cors/)
