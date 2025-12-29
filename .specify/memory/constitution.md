<!--
  SYNC IMPACT REPORT
  ==================
  Version Change: [UNVERSIONED] → 1.0.0
  Rationale: Initial constitution ratification with governance framework addition

  Modified Principles: None (governance section added)

  Added Sections:
    - Section 7: Governance (Constitutional Authority, Amendment Process,
      Compliance Review, Versioning Policy)
    - Version metadata (1.0.0 | Ratified: 2025-12-28 | Last Amended: 2025-12-28)

  Removed Sections: None

  Template Consistency Status:
    ✅ .specify/templates/plan-template.md - Constitution Check aligned
    ✅ .specify/templates/spec-template.md - Requirements structure aligned
    ✅ .specify/templates/tasks-template.md - Task categorization aligned
    ⚠️  .claude/commands/*.md - Command files reviewed, no updates needed
    ⚠️  Runtime docs - No README.md exists yet in repository root

  Deferred Items: None

  Follow-up Actions:
    - Create README.md to document project overview and reference constitution
    - Ensure all future feature plans include Constitution Check section
    - Review existing templates to ensure compliance checking references all 6 sections
-->

# Project Constitution: Study Abroad (High-Integrity Edition)

## 1. Core Technical Stack
*   **Frontend:** Next.js 15+ (App Router) | TypeScript (Strict Mode).
*   **Styling:** Tailwind CSS | shadcn/ui.
*   **AI SDK:** Vercel AI SDK (Streaming & RSC support).
*   **Backend/AI Logic:** Python 3.12+ (FastAPI) | LangChain.
*   **Database:** Supabase (PostgreSQL) with Row Level Security (RLS).
*   **Auth:** Google OAuth 2.0 via Auth.js (NextAuth) or Clerk.
*   **Infrastructure:** Serverless / Autoscaling (Vercel + Google Cloud Run).

## 2. Security Framework (NIST CSF 2.0)
*   **Identify:** Maintain an automated Software Bill of Materials (SBOM) to track dependencies.
*   **Protect:**
    *   Implement **Identity and Access Management (IAM)** using OAuth 2.0 with least-privileged scopes.
    *   Zero-exposure policy: All Gemini API keys and Database secrets must reside in encrypted Secret Managers.
    *   Data-at-rest must be encrypted via AES-256; Data-in-transit via TLS 1.3.
*   **Detect/Respond:** Continuous logging of authentication events and API anomalies to a centralized security dashboard.

## 3. Engineering Rigor & Testing
*   **Specification Faithfulness:** The implementation must achieve 100% parity with the `specs/` directory. No "hidden" features or undocumented UI elements are permitted.
*   **Mutation Testing:**
    *   **JavaScript/TS:** Use **Stryker Mutator**. All PRs must maintain a Mutation Score threshold of >80%.
    *   **Objective:** Ensure tests are actually capable of catching bugs, not just passing lines.
*   **Code Coverage Validation:**
    *   Mandatory 90% statement/branch coverage.
    *   **No Assumptions:** Coverage must be verified via automated CI reports (e.g., Codecov or Vitest coverage reports). Failure to meet thresholds will block deployments.
*   **JavaScript Best Practices:**
    *   Follow **Clean Code** principles: Functions should be small, single-responsibility, and pure where possible.
    *   Use Functional Programming patterns (immutability, map/filter/reduce) over imperative loops.
    *   Enforce Airbnb JavaScript Style Guide via ESLint.

## 4. Architectural Principles
*   **Stateless Autoscaling:** The backend must be shared-nothing to facilitate rapid horizontal scaling on Cloud Run.
*   **RAG Integrity:** For the focused subject matter, citations must be mandatory. The AI cannot "hallucinate" outside the provided vector context.
*   **Persistence:** All chat interactions must be mapped to a verified `userId`.

## 5. Naming & Structure
*   **File Naming:** PascalCase for Components; kebab-case for directories/files; snake_case for Database.
*   **API Design:** Strictly RESTful or GraphQL with documented schemas (OpenAPI/Swagger).

## 6. Prohibited Practices
*   **No Assumptions:** Do not write code based on "standard industry practice" if it contradicts the project specification.
*   **No Shadow IT:** No third-party scripts or trackers (e.g., Google Analytics) unless explicitly defined in the security spec.
*   **No Manual Deployments:** All infrastructure must be managed via Infrastructure as Code (IaC) or automated CI/CD pipelines.

## 7. Governance

### Constitutional Authority

This constitution supersedes all other development practices, style guides, and team conventions.
When conflicts arise, constitution principles take precedence.

### Amendment Process

Constitution changes require:
1. Proposed amendment with rationale documented
2. Impact analysis on existing templates and workflows
3. Semantic version bump (MAJOR/MINOR/PATCH) with justification
4. Update to all dependent templates and command files
5. Documentation of migration path for incompatible changes

Use `/speckit.constitution` command to maintain consistency across artifacts.

### Compliance Review

Every feature plan MUST include "Constitution Check" section verifying:
- Technical stack alignment (Section 1)
- Security framework compliance (Section 2)
- Testing standards met (Section 3)
- Architectural principles followed (Section 4)
- Naming conventions applied (Section 5)
- Prohibited practices avoided (Section 6)

Plan approval is blocked until all constitutional gates pass or violations are justified.

### Versioning Policy

**MAJOR** (X.0.0): Backward incompatible governance changes
- Changing required technical stack incompatibly
- Removing or relaxing security requirements
- Changing testing thresholds significantly

**MINOR** (x.Y.0): Additive governance enhancements
- Adding new security requirements
- Expanding testing coverage expectations
- Adding new architectural constraints

**PATCH** (x.y.Z): Non-semantic refinements
- Clarifying existing requirements
- Fixing typos or formatting
- Adding examples without changing rules

**Allowed Tools List** (explicitly): Vercel, Cloud Run, Supabase, Auth.js/Clerk, FastAPI, LangChain, Vitest, Stryker, ESLint Airbnb, Codecov, SBOM tooling.

**Decision Log Rule**: “Any change that affects architecture, security, data model, auth, or CI gates requires an ADR in docs/adr/.”

**Version**: 1.0.0 | **Ratified**: 2025-12-28 | **Last Amended**: 2025-12-28