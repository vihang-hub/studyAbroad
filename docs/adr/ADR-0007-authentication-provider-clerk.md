# ADR-0007: Clerk as Authentication Provider

  **Date**: 2025-01-03
  **Status**: Accepted
  **Context**: MVP UK Study & Migration Research App
  **Supersedes**: None

  ## Context

  The MVP specification requires authentication via Google, Apple, Facebook, and Email providers. The project constitution (Section 1) permits either "Auth.js (NextAuth) or Clerk" as the OAuth 2.0 implementation.

  ## Decision

  We will use **Clerk 6.36.5** as the authentication provider.

  ## Rationale

  ### Clerk Advantages
  1. **Multi-Provider Out-of-Box**: Supports Google, Apple, Facebook, Email without custom configuration
  2. **Production-Ready**: Enterprise-grade security, session management, and user management
  3. **Developer Experience**: Simple integration with Next.js 15 App Router via `@clerk/nextjs`
  4. **Built-in UI Components**: Pre-built sign-in/sign-up flows reduce frontend development time
  5. **Row-Level Security Integration**: Easy userId extraction for Supabase RLS policies
  6. **Magic Link Support**: Email authentication includes passwordless magic links
  7. **Active Maintenance**: Regular updates and security patches

  ### NextAuth Considered But Rejected
  - **Configuration Complexity**: Requires manual OAuth provider setup for each social login
  - **Session Management**: Requires additional JWT/database session handling
  - **UI Implementation**: No pre-built components, requires custom auth UI development
  - **Maintenance**: Requires ongoing OAuth credential management per provider

  ## Consequences

  ### Positive
  - Faster MVP development (2-3 days saved on auth implementation)
  - Reduced security surface area (Clerk handles token refresh, session rotation)
  - Simplified RLS integration via stable Clerk user IDs
  - Professional authentication UX without custom UI development

  ### Negative
  - **Vendor Lock-in**: Migration to NextAuth would require significant refactoring
  - **Cost**: Clerk has usage-based pricing (free tier: 10,000 MAU, then $25/1000 MAU)
    - MVP projection: 100-500 users → **free tier sufficient**
    - Scale projection: 10,000 users → ~$250/month
  - **Third-Party Dependency**: Relies on Clerk service availability (99.9% SLA)

  ### Mitigation
  - Abstract auth logic behind shared `useAuth` hook (future provider swap possible)
  - Monitor Clerk costs; evaluate NextAuth migration if costs exceed $500/month
  - Implement graceful degradation if Clerk API unavailable (cache last-known session)

  ## Compliance

  **Constitution Section 1**: ✅ "Auth.js (NextAuth) **or** Clerk" - Clerk choice permitted

  **Constitution Section 2 (Security)**:
  - ✅ OAuth 2.0 with least-privileged scopes (Clerk manages scopes)
  - ✅ Zero-exposure: Clerk API keys in Secret Manager
  - ✅ TLS 1.3 enforced (Clerk default)

  ## References

  - Clerk Documentation: https://clerk.com/docs
  - Clerk Next.js Integration: https://clerk.com/docs/quickstarts/nextjs
  - Constitution: `.specify/memory/constitution.md` Section 1