# Secrets Management Checklist

## Overview
This document lists all secrets required for the Study Abroad MVP application and provides setup instructions for Google Secret Manager in production.

## Required Secrets

### 1. Gemini API Key
- **Name**: `GEMINI_API_KEY`
- **Purpose**: Access to Google Gemini 2.0 Flash API for AI report generation
- **Where to get**: [Google AI Studio](https://makersuite.google.com/app/apikey)
- **Used by**: Backend (Cloud Run)
- **Format**: String (API key)

### 2. Stripe Secret Key
- **Name**: `STRIPE_SECRET_KEY`
- **Purpose**: Server-side Stripe API access for payment processing
- **Where to get**: [Stripe Dashboard](https://dashboard.stripe.com/apikeys)
- **Used by**: Backend (Cloud Run)
- **Format**: String (starts with `sk_live_` or `sk_test_`)

### 3. Stripe Webhook Secret
- **Name**: `STRIPE_WEBHOOK_SECRET`
- **Purpose**: Verify webhook signatures from Stripe
- **Where to get**: [Stripe Webhooks](https://dashboard.stripe.com/webhooks)
- **Used by**: Backend (Cloud Run)
- **Format**: String (starts with `whsec_`)

### 4. Clerk Secret Key
- **Name**: `CLERK_SECRET_KEY`
- **Purpose**: Server-side authentication and JWT verification
- **Where to get**: [Clerk Dashboard](https://dashboard.clerk.com/)
- **Used by**: Backend (Cloud Run)
- **Format**: String (starts with `sk_`)

### 5. Supabase Service Role Key
- **Name**: `SUPABASE_SERVICE_ROLE_KEY`
- **Purpose**: Backend database access with admin privileges
- **Where to get**: Supabase Project Settings > API
- **Used by**: Backend (Cloud Run)
- **Format**: String (JWT token)

### 6. Supabase Database Password
- **Name**: `SUPABASE_DB_PASSWORD`
- **Purpose**: Direct database access for migrations
- **Where to get**: Supabase Project Settings > Database
- **Used by**: Backend (migrations only)
- **Format**: String (password)

### 7. Cron Secret
- **Name**: `CRON_SECRET`
- **Purpose**: Authenticate scheduled cleanup jobs
- **Where to get**: Generate using `openssl rand -hex 32`
- **Used by**: Backend (Cloud Run) and Cloud Scheduler
- **Format**: String (random hex string)

## Development vs Production

### Development (Local .env files)
```bash
# backend/.env
GEMINI_API_KEY=your-test-key
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...
CLERK_SECRET_KEY=sk_test_...
SUPABASE_SERVICE_ROLE_KEY=your-key
SUPABASE_DB_PASSWORD=your-password
CRON_SECRET=dev-secret-123

# frontend/.env.local
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=pk_test_...
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_test_...
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Production (Google Secret Manager)
All backend secrets should be stored in Google Secret Manager and mounted to Cloud Run.

## Setup Instructions

### Step 1: Create Secrets in Google Secret Manager

```bash
# Enable Secret Manager API
gcloud services enable secretmanager.googleapis.com

# Create secrets (one-time setup)
echo -n "your-gemini-key" | gcloud secrets create GEMINI_API_KEY --data-file=-
echo -n "sk_live_..." | gcloud secrets create STRIPE_SECRET_KEY --data-file=-
echo -n "whsec_..." | gcloud secrets create STRIPE_WEBHOOK_SECRET --data-file=-
echo -n "sk_..." | gcloud secrets create CLERK_SECRET_KEY --data-file=-
echo -n "your-supabase-key" | gcloud secrets create SUPABASE_SERVICE_ROLE_KEY --data-file=-
echo -n "your-db-password" | gcloud secrets create SUPABASE_DB_PASSWORD --data-file=-
echo -n "$(openssl rand -hex 32)" | gcloud secrets create CRON_SECRET --data-file=-
```

### Step 2: Grant Cloud Run Access

```bash
# Get Cloud Run service account
PROJECT_ID=$(gcloud config get-value project)
SERVICE_ACCOUNT="${PROJECT_ID}-compute@developer.gserviceaccount.com"

# Grant access to all secrets
for SECRET in GEMINI_API_KEY STRIPE_SECRET_KEY STRIPE_WEBHOOK_SECRET \
              CLERK_SECRET_KEY SUPABASE_SERVICE_ROLE_KEY SUPABASE_DB_PASSWORD \
              CRON_SECRET; do
  gcloud secrets add-iam-policy-binding $SECRET \
    --member="serviceAccount:$SERVICE_ACCOUNT" \
    --role="roles/secretmanager.secretAccessor"
done
```

### Step 3: Mount Secrets to Cloud Run

Add to your Cloud Run deployment configuration:

```yaml
# backend/infrastructure/cloud-run.yaml
apiVersion: serving.knative.dev/v1
kind: Service
metadata:
  name: study-abroad-backend
spec:
  template:
    metadata:
      annotations:
        run.googleapis.com/secrets: |
          GEMINI_API_KEY=GEMINI_API_KEY:latest,
          STRIPE_SECRET_KEY=STRIPE_SECRET_KEY:latest,
          STRIPE_WEBHOOK_SECRET=STRIPE_WEBHOOK_SECRET:latest,
          CLERK_SECRET_KEY=CLERK_SECRET_KEY:latest,
          SUPABASE_SERVICE_ROLE_KEY=SUPABASE_SERVICE_ROLE_KEY:latest,
          SUPABASE_DB_PASSWORD=SUPABASE_DB_PASSWORD:latest,
          CRON_SECRET=CRON_SECRET:latest
```

Or via CLI:

```bash
gcloud run deploy study-abroad-backend \
  --image gcr.io/$PROJECT_ID/study-abroad-backend \
  --set-secrets="GEMINI_API_KEY=GEMINI_API_KEY:latest,STRIPE_SECRET_KEY=STRIPE_SECRET_KEY:latest,STRIPE_WEBHOOK_SECRET=STRIPE_WEBHOOK_SECRET:latest,CLERK_SECRET_KEY=CLERK_SECRET_KEY:latest,SUPABASE_SERVICE_ROLE_KEY=SUPABASE_SERVICE_ROLE_KEY:latest,SUPABASE_DB_PASSWORD=SUPABASE_DB_PASSWORD:latest,CRON_SECRET=CRON_SECRET:latest"
```

### Step 4: Verify Secrets are Loaded

```bash
# SSH into Cloud Run instance (for debugging)
gcloud run services describe study-abroad-backend --format="value(status.url)"

# Check environment variables are populated
curl https://your-backend-url.run.app/health
```

## Security Best Practices

1. **Never commit secrets to version control**
   - All `.env` files are in `.gitignore`
   - Use `.env.example` files with placeholder values only

2. **Rotate secrets regularly**
   - Stripe keys: Every 90 days
   - API keys: Every 90 days
   - CRON_SECRET: Every 180 days

3. **Use different secrets for dev/staging/production**
   - Never use production keys in development
   - Use Stripe test mode in development

4. **Limit secret access**
   - Only grant secretAccessor role to service accounts that need it
   - Use separate service accounts for different environments

5. **Audit secret access**
   ```bash
   # View audit logs
   gcloud logging read "protoPayload.serviceName=secretmanager.googleapis.com" \
     --limit 50 --format json
   ```

6. **Enable secret versioning**
   - Secret Manager automatically versions secrets
   - Always reference `:latest` in production
   - Pin specific versions for rollback if needed

## Troubleshooting

### Secret not found error
```
Error: Secret GEMINI_API_KEY not found
```
**Solution**: Verify secret exists and Cloud Run has access:
```bash
gcloud secrets describe GEMINI_API_KEY
gcloud secrets get-iam-policy GEMINI_API_KEY
```

### Permission denied error
```
Error: Permission denied on secret GEMINI_API_KEY
```
**Solution**: Grant secretAccessor role to Cloud Run service account:
```bash
gcloud secrets add-iam-policy-binding GEMINI_API_KEY \
  --member="serviceAccount:YOUR_SERVICE_ACCOUNT" \
  --role="roles/secretmanager.secretAccessor"
```

### Secret value is empty
**Solution**: Check secret was created with data:
```bash
gcloud secrets versions access latest --secret="GEMINI_API_KEY"
```

## Validation Checklist

- [ ] All 7 secrets created in Google Secret Manager
- [ ] Cloud Run service account has secretAccessor role for all secrets
- [ ] Secrets mounted to Cloud Run via `--set-secrets` flag
- [ ] Backend starts successfully and can access secrets
- [ ] Health check endpoint returns 200 OK
- [ ] Stripe webhook signature verification works
- [ ] Clerk JWT verification works
- [ ] Gemini API calls succeed
- [ ] Database connections succeed
- [ ] Cron jobs can authenticate with CRON_SECRET

## Reference Links

- [Google Secret Manager Documentation](https://cloud.google.com/secret-manager/docs)
- [Cloud Run Secrets Integration](https://cloud.google.com/run/docs/configuring/secrets)
- [Stripe API Keys](https://stripe.com/docs/keys)
- [Clerk Dashboard](https://clerk.com/docs)
- [Supabase API Settings](https://supabase.com/docs/guides/api)
