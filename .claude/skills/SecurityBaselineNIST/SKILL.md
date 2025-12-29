Name: SecurityBaselineNIST
Purpose: Enforce baseline security rules aligned to your NIST CSF 2.0 intent.


Enforce baseline rules:
    No secrets in code or frontend
    Secrets must be in secret managers
    SBOM required
    Central logging for auth and API anomalies
    No third-party trackers/scripts unless explicitly specified in specs

Require documentation outputs:
    docs/security-controls.md mapping controls to NIST CSF (Identify/Protect/Detect/Respond)
    docs/security-logging.md describing what is logged and where

Require that any architecture/design changes touching auth/data storage mention:
    RLS strategy
    least-privilege scopes
    data retention controls (30 days for reports per your current MVP)

If security conflicts with a spec, flag as violation and require an ADR.