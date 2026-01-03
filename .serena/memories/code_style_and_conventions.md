# Code Style and Conventions

## General Principles (from Constitution v1.0.0)

### Clean Code
- Functions should be small, single-responsibility, and pure where possible
- Use Functional Programming patterns (immutability, map/filter/reduce) over imperative loops
- Follow Clean Code principles

### Naming Conventions
- **PascalCase**: React Components (e.g., ChatInput.tsx, ReportSection.tsx)
- **camelCase**: Variables and functions (e.g., getUserData, reportCount)
- **kebab-case**: Directories and files (e.g., src/app/chat/, shared-config/)
- **snake_case**: Database tables and columns (e.g., users, created_at, deleted_at)
- **UPPER_SNAKE_CASE**: Constants (e.g., MAX_RETRIES, DEFAULT_TIMEOUT)

## TypeScript Style

### Strict Mode
- TypeScript strict mode ENABLED
- No `any` types unless explicitly justified
- Leverage type inference where appropriate
- Proper typing for all function parameters and return values

### Linting
- ESLint with Airbnb JavaScript Style Guide
- Located in: `.eslintrc.json` in each workspace
- Run: `npm run lint`

### Functional Programming
- Prefer immutability (use `readonly` for TypeScript)
- Pure functions where possible
- Map/filter/reduce over imperative loops
- Avoid side effects

### Component Structure (React)
```typescript
// Example React component structure
import { useState } from 'react';

interface ComponentProps {
  prop1: string;
  prop2?: number;
}

export function ComponentName({ prop1, prop2 = 0 }: ComponentProps) {
  const [state, setState] = useState<string>('');

  // Pure helper functions
  const helperFunction = (input: string): string => {
    return input.toUpperCase();
  };

  return (
    <div>
      {/* Component JSX */}
    </div>
  );
}
```

### File Organization
```
component-name/
├── ComponentName.tsx       # Main component
├── ComponentName.test.tsx  # Tests
└── index.ts                # Re-export
```

## Python Style

### Version
- Python 3.12+

### Linting and Formatting
- **Linter**: ruff (run: `ruff check src`)
- **Formatter**: black (run: `black src`)
- **Type Checker**: mypy (run: `mypy src`)
- Line length: 100 characters

### Naming
- **snake_case**: Functions, variables, modules
- **PascalCase**: Classes
- **UPPER_SNAKE_CASE**: Constants

### Type Hints
- All functions must have type hints
- Use Python 3.12+ modern type syntax (e.g., `str | None` instead of `Optional[str]`)

### Function Structure
```python
# Example function structure
from typing import Any

def function_name(param1: str, param2: int = 0) -> dict[str, Any]:
    """
    Brief description.

    Args:
        param1: Description
        param2: Description (default: 0)

    Returns:
        Dictionary with result data
    """
    # Implementation
    return {"result": "data"}
```

### Module Structure
```
src/
├── api/
│   ├── routes/
│   ├── services/
│   └── models/
├── database/
│   ├── repositories/
│   └── adapters/
├── config.py
├── feature_flags.py
└── logging_config.py
```

## Testing Conventions

### Test File Naming
- TypeScript: `ComponentName.test.ts` or `function-name.test.ts`
- Python: `test_module_name.py`

### Test Structure
```typescript
// TypeScript (Vitest)
describe('ComponentName', () => {
  it('should render correctly', () => {
    // Arrange
    const props = { /* ... */ };

    // Act
    render(<ComponentName {...props} />);

    // Assert
    expect(screen.getByText('...')).toBeInTheDocument();
  });
});
```

```python
# Python (pytest)
def test_function_name():
    """Test description."""
    # Arrange
    input_data = "test"

    # Act
    result = function_name(input_data)

    # Assert
    assert result == expected_value
```

### Coverage Requirements
- **Minimum**: 90% statement/branch coverage (enforced by CI)
- **Mutation Score**: >80% (Stryker for TypeScript, mutmut for Python)
- **Test Pyramid**: 80% unit, 15% integration, 5% E2E

## API Design

### RESTful Conventions
- Use proper HTTP methods (GET, POST, PUT, DELETE)
- Documented with OpenAPI 3.1 spec
- Location: `/Users/vihang/projects/study-abroad/docs/api/openapi.yaml`

### Endpoints
```
GET    /api/resources       # List resources
POST   /api/resources       # Create resource
GET    /api/resources/:id   # Get resource
PUT    /api/resources/:id   # Update resource
DELETE /api/resources/:id   # Delete resource
```

## Documentation

### Comments
- Explain "why" not "what"
- Self-documenting code preferred
- Use JSDoc/docstrings for public APIs

### ADRs
- All architectural decisions documented in `/Users/vihang/projects/study-abroad/docs/adr/`
- Use ADR template format
- Reference constitution compliance

## Security Conventions

### NIST CSF 2.0 Compliance
- No secrets in source code
- All API keys in Secret Managers (Google Secret Manager for production)
- TLS 1.3 for data in transit
- AES-256 for data at rest
- Row Level Security (RLS) on all database tables

### Prohibited Practices
- No hardcoded secrets
- No shadow IT (third-party trackers without documentation)
- No manual deployments (use CI/CD)
- No assumptions not backed by specification
