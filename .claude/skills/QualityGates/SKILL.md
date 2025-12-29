Name: QualityGates
Purpose: Define and enforce the quality thresholds and how they’re reported (agents execute, this skill defines).

Applies to all code and test work in this repo.

Thresholds:
    1. Coverage must be ≥ 90% statement and branch (frontend + backend separately if possible).
    2. Mutation score must be > 80% for JS/TS (Stryker).

Required behavior:
    1. Any plan must include how tests will be produced and measured.
    2. Any implementation must include tests sufficient to meet thresholds.
    3. CI/CD must block deploys if thresholds fail.

Reporting format:
    1. Test/coverage summary should be documented in docs/testing/coverage.md
    2. Mutation summary should be documented in docs/testing/mutation.md

Tooling (preferred, can be specified later in plan):
    1. Frontend: Vitest + Stryker
    2. Backend: pytest (or equivalent) + coverage reporting

When thresholds are not met:
    Require explicit failure report + remediation steps; do not mark gate PASS.