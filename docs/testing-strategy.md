# Testing Strategy: UK Study & Migration Research App MVP

**Last Updated**: 2025-12-29  
**Version**: 1.0.0  
**Owner**: QA Testing Specialist

---

## Executive Summary

This document outlines the comprehensive testing strategy for the UK Study & Migration Research App MVP. Our approach combines unit testing, integration testing, and mutation testing to ensure code quality and reliability across all three packages: backend (Python/FastAPI), frontend (Next.js/React), and shared (TypeScript).

### Quality Targets

- **Code Coverage**: ≥90% across all metrics (lines, functions, branches, statements)
- **Mutation Score**: >80% (validates test effectiveness, not just coverage)
- **Test Pass Rate**: 100% in CI/CD pipeline before deployment

---

## Testing Philosophy

### Core Principles

1. **Test-Driven Development (TDD)**: Write tests that derive directly from acceptance criteria
2. **Behavior Over Implementation**: Test what the code does, not how it does it
3. **Fast and Isolated**: Tests must be independent, repeatable, and fast
4. **Meaningful Coverage**: Focus on meaningful test scenarios, not just coverage metrics
5. **Mutation Testing**: Validate test effectiveness through mutation analysis

### AAA Pattern

All tests follow the **Arrange-Act-Assert** pattern for clarity and consistency.

---

## Test Stack

### Backend (Python/FastAPI)

- **pytest**: Test runner and framework (≥7.4.0)
- **pytest-asyncio**: Async test support (≥0.21.0)
- **pytest-cov**: Coverage measurement (≥4.1.0)
- **unittest.mock**: Mocking external dependencies
- **FastAPI TestClient**: API endpoint testing

### Frontend (Next.js/React)

- **Vitest**: Test runner (^1.1.0)
- **@testing-library/react**: Component testing
- **@testing-library/jest-dom**: DOM matchers
- **@vitest/coverage-v8**: Coverage via V8
- **@stryker-mutator/core**: Mutation testing (^8.0.0)
- **jsdom**: DOM environment

### Shared (TypeScript)

- **Vitest**: Test runner (^1.1.0)
- **@testing-library/react**: Hook and component testing
- **@vitest/coverage-v8**: Coverage measurement
- **@stryker-mutator/core**: Mutation testing (^8.0.0)

---

## Test Coverage by Package

### Backend Tests

- **Health Endpoints**: `/health` route validation
- **Auth Service**: Clerk JWT verification, token validation
- **Payment Service**: Stripe checkout creation, webhook handling
- **AI Service**: UK query validation, report generation
- **Report Service**: CRUD operations, ownership checks, soft delete
- **API Endpoints**: Integration tests for all routes

### Frontend Tests

- **ChatInput**: UK validation, character limits, error handling
- **MessageList**: Message rendering, timestamps, alignment
- **ReportSection**: Markdown rendering, citations display
- **CitationList**: Source formatting, links, accessibility

### Shared Tests

- **useAuth Hook**: Clerk authentication state, sign in/out
- **usePayment Hook**: Stripe checkout flow, error handling
- **LoginForm**: OAuth and email auth flows
- **CheckoutButton**: Payment initiation

---

## Running Tests

### Backend

```bash
cd backend
python3 -m pytest --cov=src --cov-report=term --cov-report=html
```

### Frontend

```bash
cd frontend
npm test -- --coverage
```

### Shared

```bash
cd shared
npm test -- --coverage
```

---

## Mutation Testing

Mutation testing validates test effectiveness by introducing code mutations and checking if tests fail.

**Target**: >80% mutation score

```bash
# Frontend
cd frontend
npm run test:mutation

# Shared
cd shared
npm run test:mutation
```

---

## Best Practices

### DO

- Write tests before or alongside code (TDD approach)
- Test behavior, not implementation details
- Use descriptive test names following: `should [expected behavior] when [condition]`
- Keep tests simple and focused
- Mock external dependencies (Clerk, Stripe, Supabase, Gemini)
- Test edge cases and error paths
- Run tests locally before committing

### DON'T

- Test library code (e.g., React, FastAPI internals)
- Write tests that depend on execution order
- Use real API keys or production data
- Skip negative testing (error cases)
- Ignore failing tests
- Game coverage metrics

---

## Resources

- [Coverage Report](/Users/vihang/projects/study-abroad/docs/testing/coverage.md)
- [Mutation Testing Results](/Users/vihang/projects/study-abroad/docs/testing/mutation.md)
- [Quality Gate Checklist](/Users/vihang/projects/study-abroad/agents/checklists/Gate5-QA.md)

---

**Document Version**: 1.0.0  
**Last Review**: 2025-12-29
