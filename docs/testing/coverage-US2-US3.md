# Test Coverage Report - User Stories 2 & 3
## MVP UK Study & Migration Research App
### Generated: 2026-01-02
### Scope: Report History & Data Retention

---

## Executive Summary

**Overall Backend Coverage**: 53% (Target: 90% - **FAIL**)
**Lines Covered**: 764 / 1454
**Gap to Target**: 37 percentage points (-545 lines)

---

## Coverage by Critical Module

| Module | Coverage | Target | Gap | Priority |
|--------|----------|--------|-----|----------|
| `src/database/repositories/report.py` | 20% | 90% | -70% | 🔴 CRITICAL |
| `src/api/services/report_service.py` | 27% | 90% | -63% | 🔴 CRITICAL |
| `src/api/routes/reports.py` | 36% | 90% | -54% | 🔴 CRITICAL |
| `src/api/routes/cron.py` | 38% | 90% | -52% | 🔴 CRITICAL |
| `src/api/models/report.py` | 80% | 90% | -10% | ⚠️ NEAR TARGET |

**Average Critical Path Coverage**: 30%

---

## Remediation Plan (11 hours → 90%)

### Phase 1: Quick Fixes (2.5 hrs → +15%)
- Fix Pydantic validation (15 min)
- Fix async mocking (2 hrs)
- Run all unit tests (15 min)

### Phase 2: Integration Tests (4 hrs → +15%)
- Add route endpoint tests (2 hrs)
- Add repository tests (2 hrs)

### Phase 3: Edge Cases (2 hrs → +7%)
- Error handling (1 hr)
- Edge cases (1 hr)

**Total**: 11 hours → **90% coverage**

---

## Commands

### Measure Coverage
```bash
cd /Users/vihang/projects/study-abroad/backend
source venv/bin/activate
pytest tests/ --cov=src --cov-report=html --cov-report=term
```

### View Report
```bash
open /Users/vihang/projects/study-abroad/backend/htmlcov/index.html
```

---

**Status**: BELOW TARGET - Remediation Required
**Path to PASS**: Execute 3-phase plan above
