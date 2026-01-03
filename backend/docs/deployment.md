# Backend Deployment Guide

This guide covers deploying the FastAPI backend to Google Cloud Run.

## Prerequisites

- Google Cloud SDK installed (`gcloud`)
- Docker installed
- GCP project with billing enabled
- Required APIs enabled:
  - Cloud Run API
  - Container Registry API
  - Secret Manager API
  - Cloud Scheduler API

## Environment Setup

### 1. Configure GCP Project

```bash
# Set project
gcloud config set project YOUR_PROJECT_ID

# Enable required APIs
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com
gcloud services enable secretmanager.googleapis.com
gcloud services enable cloudscheduler.googleapis.com
```

### 2. Create Secrets in Secret Manager

```bash
# Store sensitive values
gcloud secrets create GEMINI_API_KEY --data-file=-
gcloud secrets create STRIPE_SECRET_KEY --data-file=-
gcloud secrets create STRIPE_WEBHOOK_SECRET --data-file=-
gcloud secrets create CLERK_SECRET_KEY --data-file=-
gcloud secrets create SUPABASE_SERVICE_ROLE_KEY --data-file=-
gcloud secrets create DATABASE_URL --data-file=-
gcloud secrets create CRON_SECRET --data-file=-
```

### 3. Grant Secret Access

```bash
# Get the service account email
SA_EMAIL=$(gcloud iam service-accounts list --filter="displayName:Compute Engine default" --format="value(email)")

# Grant access to secrets
for secret in GEMINI_API_KEY STRIPE_SECRET_KEY STRIPE_WEBHOOK_SECRET CLERK_SECRET_KEY SUPABASE_SERVICE_ROLE_KEY DATABASE_URL CRON_SECRET; do
  gcloud secrets add-iam-policy-binding $secret \
    --member="serviceAccount:$SA_EMAIL" \
    --role="roles/secretmanager.secretAccessor"
done
```

## Build and Deploy

### 1. Build Docker Image

```bash
cd backend

# Build image
docker build -t gcr.io/YOUR_PROJECT_ID/study-abroad-backend:latest .

# Push to Container Registry
docker push gcr.io/YOUR_PROJECT_ID/study-abroad-backend:latest
```

### 2. Deploy to Cloud Run

```bash
gcloud run deploy study-abroad-backend \
  --image gcr.io/YOUR_PROJECT_ID/study-abroad-backend:latest \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 512Mi \
  --cpu 1 \
  --min-instances 0 \
  --max-instances 100 \
  --concurrency 80 \
  --timeout 300 \
  --set-env-vars "ENVIRONMENT_MODE=production" \
  --set-env-vars "LOG_LEVEL=ERROR" \
  --set-env-vars "ENABLE_SUPABASE=true" \
  --set-env-vars "ENABLE_PAYMENTS=true" \
  --set-secrets "GEMINI_API_KEY=GEMINI_API_KEY:latest" \
  --set-secrets "STRIPE_SECRET_KEY=STRIPE_SECRET_KEY:latest" \
  --set-secrets "STRIPE_WEBHOOK_SECRET=STRIPE_WEBHOOK_SECRET:latest" \
  --set-secrets "CLERK_SECRET_KEY=CLERK_SECRET_KEY:latest" \
  --set-secrets "SUPABASE_SERVICE_ROLE_KEY=SUPABASE_SERVICE_ROLE_KEY:latest" \
  --set-secrets "DATABASE_URL=DATABASE_URL:latest"
```

### 3. Get Service URL

```bash
BACKEND_URL=$(gcloud run services describe study-abroad-backend \
  --platform managed \
  --region us-central1 \
  --format="value(status.url)")
echo "Backend URL: $BACKEND_URL"
```

## Cloud Scheduler Setup

### 1. Deploy Expire Reports Job

```bash
# Create scheduler job for daily report expiry
gcloud scheduler jobs create http expire-reports \
  --schedule="0 0 * * *" \
  --time-zone="UTC" \
  --uri="${BACKEND_URL}/api/cron/expire-reports" \
  --http-method=POST \
  --headers="Content-Type=application/json,X-Cron-Secret=YOUR_CRON_SECRET" \
  --attempt-deadline=300s \
  --max-retry-attempts=3
```

### 2. Deploy Delete Expired Reports Job

```bash
# Create scheduler job for weekly hard delete
gcloud scheduler jobs create http delete-expired-reports \
  --schedule="0 0 * * 0" \
  --time-zone="UTC" \
  --uri="${BACKEND_URL}/api/cron/delete-expired-reports" \
  --http-method=POST \
  --headers="Content-Type=application/json,X-Cron-Secret=YOUR_CRON_SECRET" \
  --attempt-deadline=600s \
  --max-retry-attempts=3
```

## Monitoring

### View Logs

```bash
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=study-abroad-backend" \
  --limit=50 \
  --format="table(timestamp,jsonPayload.message)"
```

### Check Service Status

```bash
gcloud run services describe study-abroad-backend \
  --platform managed \
  --region us-central1
```

## CI/CD Integration

Add to GitHub Actions (`.github/workflows/deploy-backend.yml`):

```yaml
name: Deploy Backend

on:
  push:
    branches: [main]
    paths:
      - 'backend/**'

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: google-github-actions/auth@v2
        with:
          credentials_json: ${{ secrets.GCP_SA_KEY }}

      - uses: google-github-actions/setup-gcloud@v2

      - name: Build and Push
        run: |
          cd backend
          gcloud builds submit --tag gcr.io/${{ secrets.GCP_PROJECT }}/study-abroad-backend

      - name: Deploy
        run: |
          gcloud run deploy study-abroad-backend \
            --image gcr.io/${{ secrets.GCP_PROJECT }}/study-abroad-backend \
            --platform managed \
            --region us-central1
```

## Rollback

```bash
# List revisions
gcloud run revisions list --service study-abroad-backend --platform managed --region us-central1

# Rollback to specific revision
gcloud run services update-traffic study-abroad-backend \
  --to-revisions=study-abroad-backend-REVISION_ID=100 \
  --platform managed \
  --region us-central1
```

## Troubleshooting

### Cold Start Issues

If cold starts exceed 2 seconds:
1. Increase `--min-instances` to 1
2. Use Cloud Run warmup requests

### Memory Errors

Increase `--memory` to 1Gi for large reports.

### Timeout Errors

Increase `--timeout` for long AI generations.

### Database Connection Issues

1. Verify DATABASE_URL secret is correct
2. Check Supabase connection pooling settings
3. Ensure IP allowlist includes Cloud Run IPs

## Health Check

```bash
curl -s ${BACKEND_URL}/health | jq
```

Expected response:
```json
{
  "status": "healthy",
  "version": "0.1.0",
  "environment": "production"
}
```
