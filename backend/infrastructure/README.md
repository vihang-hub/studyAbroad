# Infrastructure Configuration

This directory contains infrastructure configuration files for the backend services.

## Cloud Scheduler Jobs

### Report Expiry Job (`cloud-scheduler-expire.yaml`)

**Purpose**: Soft-delete reports that have passed their expiration date.

**Schedule**: Daily at midnight UTC (`0 0 * * *`)

**Endpoint**: `POST /api/cron/expire-reports`

**Process**:
- Finds reports where `expires_at < current_time`
- Sets report status to `expired` (soft delete)
- Reports expire 30 days after creation

**Setup**:
```bash
# Set CRON_SECRET in Cloud Run environment
gcloud run services update YOUR_SERVICE \
  --set-env-vars CRON_SECRET=YOUR_SECRET

# Create the scheduler job
gcloud scheduler jobs create http expire-reports \
  --location=YOUR_REGION \
  --schedule="0 0 * * *" \
  --uri="https://YOUR_BACKEND_URL/api/cron/expire-reports" \
  --http-method=POST \
  --headers="Content-Type=application/json,X-Cron-Secret=YOUR_SECRET" \
  --attempt-deadline=300s
```

### Report Deletion Job (`cloud-scheduler-delete.yaml`)

**Purpose**: Permanently delete expired reports (GDPR compliance).

**Schedule**: Weekly on Sunday at midnight UTC (`0 0 * * 0`)

**Endpoint**: `POST /api/cron/delete-expired-reports`

**Process**:
- Finds reports with `status='expired'` AND `expires_at < (current_time - 90 days)`
- Permanently deletes these reports from the database
- Total retention: 120 days (30 days active + 90 days expired)

**Setup**:
```bash
# Create the scheduler job
gcloud scheduler jobs create http delete-expired-reports \
  --location=YOUR_REGION \
  --schedule="0 0 * * 0" \
  --uri="https://YOUR_BACKEND_URL/api/cron/delete-expired-reports" \
  --http-method=POST \
  --headers="Content-Type=application/json,X-Cron-Secret=YOUR_SECRET" \
  --attempt-deadline=600s
```

## Security

All cron endpoints require the `X-Cron-Secret` header to match the `CRON_SECRET` environment variable.

**Generate a secure secret**:
```bash
# Option 1: Using openssl
openssl rand -base64 32

# Option 2: Using Python
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

## Monitoring

### Job Execution Logs

View logs in Cloud Logging:
```bash
# View expire job logs
gcloud logging read "resource.type=cloud_scheduler_job AND resource.labels.job_id=expire-reports" --limit 50

# View delete job logs
gcloud logging read "resource.type=cloud_scheduler_job AND resource.labels.job_id=delete-expired-reports" --limit 50
```

### Application Logs

The application logs job execution with correlation IDs:
- `cron.expire_reports.started`
- `cron.expire_reports.success` (includes `expired_count`)
- `cron.expire_reports.error`
- `cron.delete_expired_reports.started`
- `cron.delete_expired_reports.success` (includes `deleted_count`)
- `cron.delete_expired_reports.error`

### Alerts

Set up monitoring alerts for:
1. Job execution failures (retry exhaustion)
2. High error rates in cron endpoints
3. Unexpected deleted/expired counts

Example alert policy (Google Cloud Monitoring):
```yaml
displayName: "Cron Job Failure Alert"
conditions:
  - displayName: "Failed cron job executions"
    conditionThreshold:
      filter: 'resource.type="cloud_scheduler_job" AND severity>=ERROR'
      comparison: COMPARISON_GT
      thresholdValue: 0
      duration: 300s
```

## Data Retention Timeline

```
Day 0:   Report created
Day 30:  Report expires (soft delete via expire job)
Day 120: Report deleted permanently (hard delete via delete job)
```

This complies with GDPR requirements for data minimization and retention limits.

## Testing Locally

Test cron endpoints locally:

```bash
# Test expire endpoint
curl -X POST http://localhost:8000/api/cron/expire-reports \
  -H "Content-Type: application/json" \
  -H "X-Cron-Secret: your_local_secret"

# Test delete endpoint
curl -X POST http://localhost:8000/api/cron/delete-expired-reports \
  -H "Content-Type: application/json" \
  -H "X-Cron-Secret: your_local_secret"
```

## Troubleshooting

### Job Not Executing

1. Check job is enabled:
   ```bash
   gcloud scheduler jobs describe expire-reports --location=YOUR_REGION
   ```

2. Verify CRON_SECRET matches between Cloud Run and Cloud Scheduler

3. Check Cloud Run logs for authentication errors

### High Error Rates

1. Check database connection pool settings
2. Verify RLS policies don't block service role operations
3. Monitor database performance during job execution

### Unexpected Counts

1. Verify `expires_at` is set correctly on report creation
2. Check timezone handling (all times should be UTC)
3. Review database data for anomalies
