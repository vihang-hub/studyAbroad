# Skill: QualityGates

Defines quality thresholds and reporting requirements. Agents execute tests; this skill defines PASS/FAIL requirements.

## Thresholds
- Coverage ≥ **90%** (statement & branch)
- Mutation score > **80%** for JS/TS using **Stryker**

## Rules
- Plans must state how tests will be produced and measured.
- CI/CD must block merges/deployments if thresholds fail.
- "Tests passed" claims require evidence: exact command, exit code, and artifact paths.

## Reporting Locations
- Coverage → `docs/testing/coverage.md`
- Mutation → `docs/testing/mutation.md`
- Test run summary → `docs/testing/test-run-report.md`
