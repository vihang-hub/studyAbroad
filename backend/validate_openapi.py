#!/usr/bin/env python3
"""
OpenAPI Spec Validation Script (T170)
Validates that backend implementation matches OpenAPI specification

Checks:
1. All spec endpoints are implemented
2. All implemented endpoints are documented in spec
3. HTTP methods match
4. Path parameters match
5. Authentication requirements match
"""

import sys
from pathlib import Path

# Define expected routes from OpenAPI spec
OPENAPI_ROUTES = {
    ("GET", "/health"): {
        "auth_required": False,
        "description": "Health check endpoint",
    },
    ("POST", "/reports/initiate"): {
        "auth_required": True,
        "description": "Initiate paid report generation",
    },
    ("GET", "/reports"): {
        "auth_required": True,
        "description": "List user's reports",
    },
    ("GET", "/reports/{reportId}"): {
        "auth_required": True,
        "description": "Get single report",
    },
    ("DELETE", "/reports/{reportId}"): {
        "auth_required": True,
        "description": "Delete report",
    },
    ("GET", "/reports/{reportId}/stream"): {
        "auth_required": True,
        "description": "Stream report generation (SSE)",
    },
    ("POST", "/webhooks/stripe"): {
        "auth_required": False,  # Uses Stripe signature instead
        "description": "Stripe webhook handler",
    },
    ("POST", "/cron/expire-reports"): {
        "auth_required": False,  # Uses cron secret instead
        "description": "Expire old reports (scheduled job)",
    },
}

# Define actual implementation routes
IMPLEMENTATION_ROUTES = {
    ("GET", "/health"): {
        "file": "src/api/routes/health.py",
        "line": 149,
        "auth_required": False,
    },
    ("POST", "/reports/initiate"): {
        "file": "src/api/routes/reports.py",
        "line": 39,
        "auth_required": True,
    },
    ("GET", "/reports/"): {
        "file": "src/api/routes/reports.py",
        "line": 147,
        "auth_required": True,
    },
    ("GET", "/reports/{report_id}"): {
        "file": "src/api/routes/reports.py",
        "line": 124,
        "auth_required": True,
    },
    ("DELETE", "/reports/{report_id}"): {
        "file": "src/api/routes/reports.py",
        "line": 165,
        "auth_required": True,
    },
    ("GET", "/stream/reports/{report_id}"): {
        "file": "src/api/routes/stream.py",
        "line": 26,
        "auth_required": True,
    },
    ("POST", "/webhooks/stripe"): {
        "file": "src/api/routes/webhooks.py",
        "line": 30,
        "auth_required": False,
    },
    ("POST", "/cron/expire-reports"): {
        "file": "src/api/routes/cron.py",
        "line": 37,
        "auth_required": False,
    },
    ("POST", "/cron/delete-expired-reports"): {
        "file": "src/api/routes/cron.py",
        "line": 82,
        "auth_required": False,
    },
}


def normalize_path(path: str) -> str:
    """Normalize path for comparison (remove trailing slashes, normalize params)"""
    path = path.rstrip("/")
    # Normalize parameter names: {reportId} -> {report_id}
    path = path.replace("{reportId}", "{report_id}")
    path = path.replace("{id}", "{report_id}")
    return path


def validate_openapi_compliance():
    """
    Validate OpenAPI spec matches implementation

    Returns:
        tuple: (is_valid, issues_list)
    """
    issues = []

    print("=" * 80)
    print("OpenAPI Specification Validation (T170)")
    print("=" * 80)
    print()

    # Check 1: All spec endpoints are implemented
    print("Check 1: Spec endpoints implemented in backend")
    print("-" * 80)

    for (method, path), spec_details in OPENAPI_ROUTES.items():
        normalized_path = normalize_path(path)

        # Find matching implementation route
        found = False
        for (impl_method, impl_path), impl_details in IMPLEMENTATION_ROUTES.items():
            if method == impl_method and normalize_path(impl_path) == normalized_path:
                found = True
                print(f"✓ {method:6} {path:40} -> {impl_details['file']}")

                # Check auth requirements match
                if spec_details["auth_required"] != impl_details["auth_required"]:
                    issue = f"AUTH MISMATCH: {method} {path} - Spec requires auth={spec_details['auth_required']}, Implementation has auth={impl_details['auth_required']}"
                    issues.append(issue)
                    print(f"  ⚠️  {issue}")
                break

        if not found:
            issue = f"MISSING IMPLEMENTATION: {method} {path} - Defined in spec but not implemented"
            issues.append(issue)
            print(f"✗ {method:6} {path:40} -> NOT IMPLEMENTED")

    print()

    # Check 2: All implemented endpoints are in spec
    print("Check 2: Implementation endpoints documented in spec")
    print("-" * 80)

    for (method, path), impl_details in IMPLEMENTATION_ROUTES.items():
        normalized_path = normalize_path(path)

        # Find matching spec route
        found = False
        for (spec_method, spec_path) in OPENAPI_ROUTES.keys():
            if method == spec_method and normalize_path(spec_path) == normalized_path:
                found = True
                print(f"✓ {method:6} {path:40} -> Documented in spec")
                break

        if not found:
            # Check if this is an undocumented but intentional route
            if path == "/cron/delete-expired-reports":
                issue = f"MISSING DOCUMENTATION: {method} {path} - Implemented but not in OpenAPI spec (T140-T141)"
                issues.append(issue)
                print(f"⚠️  {method:6} {path:40} -> NOT IN SPEC (needs documentation)")
            else:
                issue = f"UNDOCUMENTED ENDPOINT: {method} {path} - Implemented but not in spec"
                issues.append(issue)
                print(f"✗ {method:6} {path:40} -> NOT IN SPEC")

    print()

    # Check 3: Path structure validation
    print("Check 3: Path structure validation")
    print("-" * 80)

    # Known path mismatches
    path_issues = []

    # SSE streaming endpoint path mismatch
    if ("GET", "/stream/reports/{report_id}") in IMPLEMENTATION_ROUTES:
        issue = "PATH MISMATCH: SSE streaming endpoint"
        issue_detail = (
            "  Spec:           GET /reports/{reportId}/stream\n"
            "  Implementation: GET /stream/reports/{report_id}\n"
            "  Impact: Frontend must use /stream/reports/{id}, not /reports/{id}/stream"
        )
        path_issues.append((issue, issue_detail))
        issues.append(f"{issue} - {issue_detail}")

    if path_issues:
        for issue, detail in path_issues:
            print(f"⚠️  {issue}")
            print(detail)
    else:
        print("✓ All paths match spec structure")

    print()

    # Summary
    print("=" * 80)
    print("Validation Summary")
    print("=" * 80)

    total_spec_routes = len(OPENAPI_ROUTES)
    total_impl_routes = len(IMPLEMENTATION_ROUTES)

    print(f"OpenAPI Spec Routes:       {total_spec_routes}")
    print(f"Implementation Routes:     {total_impl_routes}")
    print(f"Issues Found:              {len(issues)}")
    print()

    if issues:
        print("Issues Detail:")
        print("-" * 80)
        for i, issue in enumerate(issues, 1):
            print(f"{i}. {issue}")
        print()

        print("Recommendations:")
        print("-" * 80)
        print("1. Update OpenAPI spec to include POST /cron/delete-expired-reports")
        print("2. Consider aligning SSE path: /reports/{id}/stream vs /stream/reports/{id}")
        print("   (Current implementation works, but spec mismatch may confuse developers)")
        print()

        return False, issues
    else:
        print("✓ All validations passed!")
        print()
        return True, []


if __name__ == "__main__":
    is_valid, issues = validate_openapi_compliance()

    # Exit with appropriate code
    sys.exit(0 if is_valid else 1)
