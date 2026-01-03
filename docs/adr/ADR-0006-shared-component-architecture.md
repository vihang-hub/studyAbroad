# ADR-0006: Shared Component Architecture

## Status
Accepted

## Context

The updated MVP specification introduces multiple infrastructure components that are not specific to the Study Abroad application but are broadly applicable across any web application in the monorepo:

1. **Environment Configuration** (ADR-0001)
2. **Feature Flags** (ADR-0002)
3. **Database Abstraction** (ADR-0003)
4. **Logging Infrastructure** (ADR-0004)
5. **Soft Delete Pattern** (ADR-0005)

### Requirements
- **Reusability**: Components should be usable across multiple projects in the monorepo
- **Framework Agnostic**: Where possible, components should not depend on specific frameworks
- **Type Safety**: All components must provide TypeScript types
- **Testing**: Each component must have >90% test coverage (Constitution Section 3)
- **Documentation**: Each package must have comprehensive README
- **Versioning**: Independent versioning for each shared package

### Current Shared Package Status
The existing `shared/` package already contains:
- Authentication components (Clerk integration)
- Payment components (Stripe integration)
- Type definitions (User, Report, Payment)

### Goals
1. **Consolidate Infrastructure**: Move new infrastructure components to `shared/`
2. **Define Package Structure**: Establish clear organization for shared packages
3. **Establish Conventions**: Define naming, versioning, and dependency conventions
4. **Enable Reuse**: Allow other projects to easily consume shared packages

## Decision

We will organize shared components into a **multi-package structure** within the `shared/` directory, with each infrastructure concern as a separate npm package.

### 1. Shared Package Structure

```
shared/
├── config/                      # Environment configuration (ADR-0001)
│   ├── src/
│   ├── tests/
│   ├── package.json
│   ├── tsconfig.json
│   └── README.md
├── feature-flags/               # Feature flag system (ADR-0002)
│   ├── src/
│   ├── tests/
│   ├── package.json
│   └── README.md
├── database/                    # Database abstraction (ADR-0003)
│   ├── src/
│   ├── migrations/
│   ├── tests/
│   ├── package.json
│   └── README.md
├── logging/                     # Logging infrastructure (ADR-0004)
│   ├── src/
│   ├── tests/
│   ├── package.json
│   └── README.md
├── auth/                        # Authentication (existing)
│   ├── src/
│   ├── tests/
│   ├── package.json
│   └── README.md
├── payments/                    # Payment processing (existing)
│   ├── src/
│   ├── tests/
│   ├── package.json
│   └── README.md
├── types/                       # Shared type definitions (existing)
│   ├── src/
│   ├── tests/
│   ├── package.json
│   └── README.md
└── ui-components/               # Shared React components (existing)
    ├── src/
    ├── tests/
    ├── package.json
    └── README.md
```

### 2. Package Naming Convention

All shared packages use the scope `@study-abroad`:

```json
// shared/config/package.json
{
  "name": "@study-abroad/shared-config",
  "version": "1.0.0",
  "main": "./dist/index.js",
  "types": "./dist/index.d.ts"
}

// shared/feature-flags/package.json
{
  "name": "@study-abroad/shared-feature-flags",
  "version": "1.0.0",
  "main": "./dist/index.js",
  "types": "./dist/index.d.ts"
}
```

**Naming Pattern**: `@study-abroad/shared-<component-name>`

**Rationale**:
- Scope prevents npm namespace collisions
- `shared-` prefix clarifies these are monorepo-shared packages
- Kebab-case aligns with npm conventions (Constitution Section 5)

### 3. Dependency Management

**Inter-Package Dependencies:**
```json
// shared/feature-flags/package.json
{
  "dependencies": {
    "@study-abroad/shared-config": "workspace:*",
    "zod": "^3.22.0"
  }
}

// shared/logging/package.json
{
  "dependencies": {
    "@study-abroad/shared-config": "workspace:*",
    "winston": "^3.11.0"
  }
}
```

**Workspace Protocol**: Use `workspace:*` for inter-package dependencies to ensure monorepo packages always use local versions during development.

**Dependency Graph:**
```
config (base)
├── feature-flags (depends on config)
├── logging (depends on config)
└── database (depends on config, feature-flags)
```

### 4. Build Configuration

**Root `package.json` Workspace:**
```json
{
  "name": "study-abroad-monorepo",
  "private": true,
  "workspaces": [
    "frontend",
    "backend",
    "shared/*"
  ],
  "scripts": {
    "build:shared": "npm run build --workspaces --if-present",
    "test:shared": "npm run test --workspaces --if-present",
    "lint:shared": "npm run lint --workspaces --if-present"
  }
}
```

**Shared Package `package.json` Template:**
```json
{
  "name": "@study-abroad/shared-<name>",
  "version": "1.0.0",
  "description": "<description>",
  "main": "./dist/index.js",
  "types": "./dist/index.d.ts",
  "scripts": {
    "build": "tsc",
    "test": "vitest run",
    "test:watch": "vitest",
    "lint": "eslint src/",
    "typecheck": "tsc --noEmit"
  },
  "files": [
    "dist",
    "README.md"
  ],
  "keywords": [
    "study-abroad",
    "shared",
    "<component-name>"
  ],
  "author": "Study Abroad Team",
  "license": "MIT"
}
```

**Shared `tsconfig.json` Template:**
```json
{
  "compilerOptions": {
    "target": "ES2020",
    "module": "ES2020",
    "moduleResolution": "node",
    "lib": ["ES2020"],
    "outDir": "./dist",
    "rootDir": "./src",
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true,
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist", "tests"]
}
```

### 5. Testing Requirements

Each shared package must meet:
- **Coverage**: ≥90% code coverage (Constitution Section 3)
- **Mutation Testing**: >80% mutation score using Stryker
- **Test Files**: Co-located in `tests/` directory
- **Test Utilities**: Export test helpers for consumers

**Example Test Structure:**
```
shared/config/
├── src/
│   ├── schema.ts
│   ├── loader.ts
│   └── index.ts
└── tests/
    ├── schema.test.ts
    ├── loader.test.ts
    ├── utils/                 # Test utilities
    │   └── mock-env.ts
    └── setup.ts
```

**Vitest Configuration:**
```typescript
// shared/config/vitest.config.ts
import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    globals: true,
    environment: 'node',
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html'],
      include: ['src/**/*.ts'],
      exclude: ['src/**/*.test.ts', 'src/**/*.spec.ts'],
      thresholds: {
        lines: 90,
        functions: 90,
        branches: 90,
        statements: 90,
      },
    },
  },
});
```

### 6. Documentation Standards

Each shared package must include:

**README.md Template:**
```markdown
# @study-abroad/shared-<name>

<Brief description>

## Installation

npm install @study-abroad/shared-<name>

## Usage

<Basic usage example>

## API Reference

### <Primary Export>

<Description>

<Code examples>

## Testing

npm run test

## Architecture Decision Record

See [ADR-000X](<link>) for design decisions and rationale.

## License

MIT
```

**Inline Documentation:**
- All public APIs must have JSDoc comments
- Include `@param`, `@returns`, `@throws`, `@example` tags
- Generate API docs using TypeDoc (future enhancement)

### 7. Versioning Strategy

**Semantic Versioning:**
- **MAJOR**: Breaking changes to public API
- **MINOR**: New features, backward compatible
- **PATCH**: Bug fixes, backward compatible

**Changelog:**
- Maintain `CHANGELOG.md` in each package
- Follow [Keep a Changelog](https://keepachangelog.com/) format

**Version Synchronization:**
- Shared packages version independently
- Consumer packages pin to specific versions
- Use `workspace:*` during development, resolve to versions at publish

### 8. Consumer Usage

**Frontend (Next.js):**
```typescript
// frontend/package.json
{
  "dependencies": {
    "@study-abroad/shared-config": "^1.0.0",
    "@study-abroad/shared-logging": "^1.0.0",
    "@study-abroad/shared-database": "^1.0.0"
  }
}

// frontend/src/lib/config.ts
import { ConfigLoader } from '@study-abroad/shared-config';

export const config = ConfigLoader.load();
```

**Backend (Python):**
For Python backend, shared infrastructure is implemented separately in Python but follows the same architectural patterns defined in the TypeScript packages.

```python
# backend/src/config.py
# Python equivalent of @study-abroad/shared-config
# (See ADR-0001 for Python implementation)
```

### 9. CI/CD Integration

**GitHub Actions Workflow:**
```yaml
# .github/workflows/shared-packages.yml
name: Shared Packages CI

on:
  push:
    paths:
      - 'shared/**'
  pull_request:
    paths:
      - 'shared/**'

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '20'

      - name: Install dependencies
        run: npm ci

      - name: Build shared packages
        run: npm run build:shared

      - name: Test shared packages
        run: npm run test:shared

      - name: Lint shared packages
        run: npm run lint:shared

      - name: Check coverage thresholds
        run: npm run coverage:check --workspaces
```

### 10. Package Registry

**NPM Registry (Future):**
- For now, packages are consumed via workspace protocol
- Future: Publish to private npm registry or GitHub Packages
- Enables sharing across multiple monorepos

**Package Publishing:**
```bash
# Publish all shared packages
npm publish --workspaces --access public

# Publish specific package
npm publish --workspace @study-abroad/shared-config
```

## Consequences

### Positive
1. **Reusability**: Infrastructure components usable across all projects
2. **Modularity**: Clear separation of concerns
3. **Independent Evolution**: Each package can version independently
4. **Type Safety**: Full TypeScript support across packages
5. **Testing**: Enforced coverage and mutation testing standards
6. **Documentation**: Comprehensive docs for each package
7. **Monorepo Benefits**: Workspace protocol enables local development
8. **Future-Proof**: Ready for external consumption via npm registry

### Negative
1. **Complexity**: More packages to maintain
2. **Build Coordination**: Must build dependencies before consumers
3. **Version Management**: Independent versioning requires careful coordination
4. **Duplication**: Python backend requires separate implementations
5. **Overhead**: Each package has its own build/test configuration

### Trade-offs Accepted
- **Granularity vs Simplicity**: Accept more packages for better modularity
- **TypeScript-Only**: Accept that Python backend reimplements patterns
- **Workspace Protocol**: Accept that external projects can't consume directly without publishing
- **Documentation Overhead**: Accept maintenance burden for better developer experience

### Mitigation
- Automate build coordination with workspace scripts
- Document dependency graph clearly
- Provide Python implementation guides alongside TypeScript packages
- Plan for npm registry publication in post-MVP
- Use shared ESLint/TypeScript configs to reduce duplication

## Compliance

### SpeckitGovernance
- **Traceability**: All ADRs (0001-0005) document component decisions
- **Documentation**: Each package has comprehensive README
- **Justification**: Supports all new acceptance criteria (AC-10 through AC-17)

### SecurityBaselineNIST
- **Identify (ID.AM-1)**: SBOM includes all shared packages and versions
- **Protect (PR.DS-4)**: Type safety prevents vulnerabilities at compile time
- **Detect (DE.CM-8)**: Automated testing catches regressions

### RagCitationsIntegrity
- Not directly applicable to shared component architecture
- Architecture supports RAG pipeline by providing reliable infrastructure

## References
- ADR-0001: Environment Configuration System
- ADR-0002: Feature Flag Mechanism
- ADR-0003: Database Abstraction Layer
- ADR-0004: Logging Infrastructure
- ADR-0005: Soft Delete Pattern
- Constitution: Section 3 (Engineering Rigor), Section 5 (Naming & Structure)

## Revision History
- **2025-12-31**: Initial version (Accepted)
