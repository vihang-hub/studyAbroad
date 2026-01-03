# Task Completion Checklist

When a task is completed, perform the following steps in order:

## 1. Code Quality Checks

### Linting
```bash
# From project root
npm run lint

# Or workspace-specific
cd frontend && npm run lint
cd shared && npm run lint
cd backend && ruff check src
```

**Expected**: No linting errors. Fix all issues before proceeding.

### Formatting
```bash
# TypeScript (ESLint handles formatting)
npm run lint

# Python
cd backend && black src
```

**Expected**: All code properly formatted.

### Type Checking
```bash
# TypeScript (checked during build)
cd frontend && npm run build
cd shared && npm run build

# Python
cd backend && mypy src
```

**Expected**: No type errors.

## 2. Testing

### Unit Tests
```bash
# All tests
npm test

# Workspace-specific
cd frontend && npm test
cd shared && npm test
cd backend && pytest
```

**Expected**: All tests pass.

### Coverage Check
```bash
# Frontend/Shared
cd frontend && npm run test:coverage
cd shared && npm run test:coverage

# Backend
cd backend && pytest --cov=src --cov-fail-under=90
```

**Expected**: ≥90% coverage (enforced threshold).

### Mutation Testing
```bash
# Frontend/Shared
cd frontend && npm run test:mutation
cd shared && npm run test:mutation

# Backend
cd backend && mutmut run
```

**Expected**: >80% mutation score.

## 3. Build Verification

### Build All
```bash
# From root
npm run build

# Or specific workspaces
npm run build:shared
npm run build:frontend
```

**Expected**: Clean build with no errors.

### Build Artifacts Check
- Frontend: Check `/Users/vihang/projects/study-abroad/frontend/.next/` exists
- Shared: Check `/Users/vihang/projects/study-abroad/shared/dist/` exists
- Backend: No build step, but run type check with `mypy src`

## 4. Documentation Updates

### Update Affected Files
- [ ] Update README.md if public API changed
- [ ] Update quickstart.md if setup steps changed
- [ ] Create/update ADR if architectural decision made
- [ ] Update OpenAPI spec if API endpoints changed

### Code Documentation
- [ ] Ensure all public functions have JSDoc/docstrings
- [ ] Complex logic includes explanatory comments (explain "why")

## 5. Quality Gate Checklist

### Gate4: Implementation Completion
Create or update `/Users/vihang/projects/study-abroad/agents/checklists/Gate4-Implementation.md`:

```markdown
# Gate4: Implementation Completion

**Task**: [Task ID and Description]
**Date**: [Completion Date]
**Status**: PASS/FAIL

## Implementation Summary
- Files Changed: [List of files]
- Commits: [Links to commits]
- Tests Added/Updated: [Test files]

## Quality Checklist
- [ ] Implements all specification requirements
- [ ] Follows TypeScript/Python standards
- [ ] Maintains single responsibility principle
- [ ] Includes comprehensive tests (≥90% coverage)
- [ ] Passes mutation testing (>80% score)
- [ ] Passes all security checks
- [ ] Code reviewed against constitution standards

## Links
- Specification: [Link to spec file]
- Commits: [Commit hashes/links]
- Modified Files: [File paths]
```

## 6. Git Workflow

### Commit Changes
```bash
# Stage changes
git add .

# Commit with descriptive message
git commit -m "feat: implement shared-config package with Zod validation

- Add environment schema with Zod validation
- Implement ConfigLoader with singleton pattern
- Create environment presets (dev, test, production)
- Add comprehensive unit tests (95% coverage)
- Configure mutation testing with Stryker

Closes #123"
```

### Commit Message Format
```
<type>: <short summary>

<detailed description>

<footer: references, breaking changes>
```

**Types**: feat, fix, docs, style, refactor, test, chore

### Push Changes
```bash
# Push to remote
git push origin branch-name
```

## 7. Constitution Compliance Check

Verify against Constitution v1.0.0:

- [ ] **Section 1**: Uses approved tech stack (Next.js 15+, TypeScript strict, Python 3.12+, FastAPI)
- [ ] **Section 2**: Security requirements met (no secrets in code, proper encryption, RLS policies)
- [ ] **Section 3**: Testing standards met (≥90% coverage, >80% mutation score, Clean Code principles)
- [ ] **Section 4**: Architectural principles followed (stateless, RAG integrity, user-mapped persistence)
- [ ] **Section 5**: Naming conventions correct (PascalCase components, kebab-case directories, snake_case database)
- [ ] **Section 6**: No prohibited practices (no assumptions, no shadow IT, no manual deployments)

## 8. Acceptance Criteria Verification

For MVP UK Study & Migration Research App (001-mvp-uk-study-migration):

Review against spec AC-1 through AC-17:
- [ ] Relevant acceptance criteria satisfied
- [ ] Edge cases tested
- [ ] Error handling implemented

## 9. Final Checklist

Before marking task as complete:

- [ ] All linting checks pass
- [ ] All tests pass (≥90% coverage)
- [ ] Mutation score >80%
- [ ] Build succeeds with no errors
- [ ] Documentation updated
- [ ] Gate4 checklist created/updated with PASS status
- [ ] Commits pushed to remote
- [ ] Constitution compliance verified
- [ ] Acceptance criteria satisfied

**If ANY item fails**: Task is NOT complete. Fix issues and re-run checklist.

## 10. Communication

After all checks pass:
- Report completion with links to:
  - Modified files (absolute paths)
  - Commits
  - Test coverage reports
  - Gate4 checklist
  - Relevant documentation
