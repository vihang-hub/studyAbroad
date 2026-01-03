# Skill: SecurityBaselineNIST

Baseline security guardrails aligned to NIST CSF 2.0 intent.

## Mandatory Rules
- No secrets in code or frontend.
- Secrets must be stored in secret managers.
- SBOM required (dependency inventory).
- Central logging required for auth events and API anomalies.
- No third-party trackers/scripts unless explicitly specified in specs.

## Required Documentation
- `docs/security-controls.md` (map to Identify/Protect/Detect/Respond)
- `docs/security-logging.md` (what is logged, where, retention)

## Enforcement
- High/critical issues block progression to the next phase.
- Security exceptions require an ADR.
