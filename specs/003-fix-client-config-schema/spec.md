# Feature Specification: Fix Client-Side Config Schema Validation

**Feature Branch**: `003-fix-client-config-schema`
**Created**: 2026-01-03
**Status**: Draft
**Input**: User description: "Bug fix: ConfigLoader.load() Zod schema validation fails on client-side because EnvironmentConfigSchema requires server-only variables (DATABASE_URL, CLERK_SECRET_KEY) that are not available in browser context. The schema needs to make server-only fields optional or create separate client/server schemas."

## Problem Statement

The shared configuration package uses a single Zod schema (`EnvironmentConfigSchema`) that requires both client-side and server-side environment variables. When `ConfigLoader.load()` is called in the browser context (due to lazy initialization fix from feature 002), validation fails because server-only variables like `DATABASE_URL` and `CLERK_SECRET_KEY` are not available in the browser.

**Error observed**: "Configuration validation failed" with validation errors showing `DATABASE_URL` and `CLERK_SECRET_KEY` as "Required".

**Root Cause**: The schema does not distinguish between client-side and server-side environment variables, requiring all fields regardless of execution context.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Application Loads Without Errors (Priority: P1)

As a user visiting the application, I want the application to load without configuration errors so that I can use the application features.

**Why this priority**: Core functionality - if the application doesn't load, no features work.

**Independent Test**: Navigate to any page in the application and verify no "Configuration validation failed" errors appear in the browser console.

**Acceptance Scenarios**:

1. **Given** a user navigates to the application in a browser, **When** the page loads and configuration is initialized, **Then** no configuration validation errors should appear in the browser console.

2. **Given** a user is on the chat page, **When** the page initializes client-side code, **Then** the configuration should load successfully without requiring server-only variables.

3. **Given** the application is running on the server, **When** server-side code accesses configuration, **Then** all server-only variables should be validated and accessible.

---

### User Story 2 - Developer Experience Unchanged (Priority: P2)

As a developer, I want configuration errors to still be caught during development so that misconfigurations are detected early.

**Why this priority**: Maintains developer experience and prevents shipping broken configurations.

**Independent Test**: Remove a required environment variable and verify appropriate error messages appear in the correct context (server vs client).

**Acceptance Scenarios**:

1. **Given** a required client-side variable is missing, **When** configuration loads in any context, **Then** an appropriate error should indicate which variable is missing.

2. **Given** a required server-side variable is missing, **When** server-side code runs, **Then** an appropriate error should indicate which variable is missing.

3. **Given** all required variables are present, **When** configuration loads, **Then** no validation errors should occur.

---

### Edge Cases

- What happens when a client-only application calls server config methods? System should provide meaningful error or empty values.
- How does system handle partial configuration in hybrid rendering scenarios? Schema should validate context-appropriate fields only.
- What happens during server-side rendering when server variables ARE available? Full validation should occur.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST validate only client-accessible environment variables when running in browser context.
- **FR-002**: System MUST validate all environment variables (client and server) when running in server context.
- **FR-003**: System MUST distinguish between client context and server context automatically.
- **FR-004**: System MUST provide clear error messages indicating which required variables are missing.
- **FR-005**: Server-only variables MUST be optional (or excluded) in client-side schema validation.
- **FR-006**: Client-side configuration MUST include: API URL, Clerk publishable key, Supabase URL, Supabase anon key, environment mode, feature flags.
- **FR-007**: Server-side configuration MUST additionally include: Database URL, Clerk secret key, and other server-only secrets.
- **FR-008**: Existing code using configuration MUST continue to work without changes (backward compatibility).

### Key Entities

- **ClientConfig**: Configuration subset safe for browser exposure (public URLs, publishable keys, feature flags)
- **ServerConfig**: Full configuration including secrets and database credentials (extends ClientConfig)
- **EnvironmentContext**: Detection mechanism for client vs server execution context

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Application pages load without configuration validation errors in browser console (0 errors).
- **SC-002**: All existing configuration-related tests continue to pass (100% pass rate).
- **SC-003**: Server-side code can access all configuration values including server-only secrets.
- **SC-004**: Client-side code receives only client-safe configuration values.
- **SC-005**: Configuration validation errors provide actionable messages identifying missing variables.

## Assumptions

- The application uses Next.js which has distinct server and client execution contexts
- Environment variables prefixed with `NEXT_PUBLIC_` are available in client context
- Server-only variables are never prefixed with `NEXT_PUBLIC_`
- The `typeof window` check reliably distinguishes browser from server context

## Out of Scope

- Changes to environment variable naming conventions
- Migration of existing environment variables
- Changes to deployment configuration
