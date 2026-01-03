# Suggested Commands

## Root-Level Commands (from /Users/vihang/projects/study-abroad/)

### Development
```bash
# Run all workspaces in dev mode
npm run dev

# Run specific workspace
npm run dev:frontend
npm run dev:shared
```

### Building
```bash
# Build all workspaces
npm run build

# Build specific workspace
npm run build:shared
npm run build:frontend
```

### Testing
```bash
# Run all tests (frontend + shared + backend)
npm test

# Run specific workspace tests
npm run test:frontend
npm run test:shared
npm run test:backend
```

### Linting
```bash
# Lint all workspaces
npm run lint

# Lint specific workspace
npm run lint:frontend
npm run lint:shared
npm run lint:backend
```

### Cleanup
```bash
# Clean all build artifacts and node_modules
npm run clean
```

## Frontend Commands (from /Users/vihang/projects/study-abroad/frontend/)
```bash
# Development
npm run dev

# Build
npm run build

# Lint
npm run lint

# Test
npm test
npm run test:coverage

# Mutation testing
npm run test:mutation
```

## Shared Package Commands (from /Users/vihang/projects/study-abroad/shared/)
```bash
# Build TypeScript
npm run build

# Watch mode for development
npm run dev

# Lint
npm run lint

# Test
npm test
npm run test:coverage

# Mutation testing
npm run test:mutation
```

## Backend Commands (from /Users/vihang/projects/study-abroad/backend/)
```bash
# Activate virtual environment (if not already activated)
source venv/bin/activate  # or `. venv/bin/activate`

# Install dependencies
pip install -e ".[dev]"

# Run development server
uvicorn src.main:app --reload

# Lint
ruff check src

# Format
black src

# Type check
mypy src

# Test
pytest

# Test with coverage
pytest --cov=src --cov-report=html

# Test coverage must pass 90% threshold
pytest --cov=src --cov-fail-under=90
```

## Git Commands (macOS/Darwin)
```bash
# Standard git commands work on Darwin
git status
git add .
git commit -m "message"
git push
git pull
git branch
git checkout -b branch-name
```

## System Commands (macOS/Darwin specific)
```bash
# List files
ls -la

# Find files
find . -name "*.ts"

# Search in files
grep -r "pattern" src/

# Change directory
cd path/to/directory

# Print working directory
pwd

# View file contents
cat filename

# View file with pagination
less filename

# Create directory
mkdir directory-name

# Remove files/directories
rm -rf directory-name
```

## Task Completion Workflow
After completing a task:
1. Run linting: `npm run lint` (root) or workspace-specific
2. Run tests: `npm test` (root) or workspace-specific
3. Check coverage: Ensure ≥90% coverage
4. Run mutation tests: Ensure >80% mutation score
5. Build: `npm run build` to ensure no build errors
6. Commit changes: `git add . && git commit -m "message"`

## Quality Gates
Commands referenced in quality gates:
- **Gate3 (Implementation)**: `npm test`, `npm run test:coverage`, `npm run test:mutation`
- **Gate4 (Implementation Completion)**: All of above + `npm run build` + `npm run lint`
- **Gate5 (QA)**: E2E tests, performance tests, security scans
