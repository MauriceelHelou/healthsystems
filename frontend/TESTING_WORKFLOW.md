# Testing Workflow Guide

This guide provides a comprehensive workflow for testing and iterative frontend development using the HealthSystems Platform's integrated testing infrastructure, MCP servers, and Claude Code agents.

## Table of Contents

1. [Quick Start](#quick-start)
2. [Testing Infrastructure Overview](#testing-infrastructure-overview)
3. [Development Workflow](#development-workflow)
4. [Using Claude Code Agents](#using-claude-code-agents)
5. [Running Tests](#running-tests)
6. [Continuous Integration](#continuous-integration)
7. [Best Practices](#best-practices)

---

## Quick Start

### Run All Tests
```bash
cd frontend
npm test
```

### Run Specific Test Suites
```bash
# Unit tests
npm test -- App.test.tsx

# Accessibility tests
npm test -- --config=jest-a11y.config.js

# E2E tests
npx playwright test

# Single E2E test file
npx playwright test e2e/dashboard.spec.ts

# Run with UI
npx playwright test --ui
```

### Generate Coverage Report
```bash
npm test -- --coverage
```

---

## Testing Infrastructure Overview

### MCP Servers

Three MCP (Model Context Protocol) servers are configured to support testing:

1. **academic-literature** - For epidemiological research and evidence validation
2. **public-health-data** - For accessing health metrics and population data
3. **github** - For repository operations and CI/CD integration

**Location**: `.claude/mcp_servers.json`

### Claude Code Agents

Seven specialized agents are available for automated testing tasks:

1. **test-generator** - Generates comprehensive unit and integration tests
2. **code-reviewer** - Reviews code quality, security, and best practices
3. **api-documenter** - Generates and maintains API documentation
4. **data-pipeline-builder** - Creates data integration workflows
5. **epidemiology-advisor** - Reviews scientific accuracy
6. **llm-prompt-engineer** - Optimizes LLM interactions
7. **mechanism-validator** - Validates mechanism YAML files

**Location**: `.claude/agents/`

### Testing Tools

- **Jest** - Unit testing framework
- **React Testing Library** - Component testing
- **jest-axe** - Accessibility testing (WCAG 2.1 AA)
- **MSW (Mock Service Worker)** - API mocking
- **Playwright** - End-to-end testing
- **@testing-library/user-event** - User interaction simulation

---

## Development Workflow

### 1. Feature Development Cycle

```
┌─────────────────────────────────────────────────────────────┐
│                    Feature Development                       │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  Write Component Code                                        │
│  • Create component file                                     │
│  • Define types and interfaces                               │
│  • Implement functionality                                   │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  Generate Tests with test-generator Agent                    │
│  • Unit tests for component rendering                        │
│  • Integration tests for data flow                           │
│  • Accessibility tests                                       │
│  • Edge case and error handling tests                        │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  Run Tests Locally                                           │
│  • npm test -- ComponentName.test.tsx                        │
│  • Fix failing tests                                         │
│  • Verify coverage                                           │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  Code Review with code-reviewer Agent                        │
│  • Check code quality                                        │
│  • Verify best practices                                     │
│  • Security analysis                                         │
│  • Performance review                                        │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  Run E2E Tests                                               │
│  • npx playwright test                                       │
│  • Verify user flows work end-to-end                         │
│  • Test across browsers                                      │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  Commit and Push                                             │
│  • git add .                                                 │
│  • git commit -m "feat: add new feature"                     │
│  • git push                                                  │
└─────────────────────────────────────────────────────────────┘
```

### 2. Test-Driven Development (TDD)

For critical features, use TDD:

```bash
# 1. Use test-generator agent to create test scaffold
# Ask Claude Code: "Generate tests for UserProfileComponent with email validation"

# 2. Run tests (they will fail)
npm test -- UserProfile.test.tsx

# 3. Implement feature to make tests pass
# Edit src/components/UserProfile.tsx

# 4. Run tests again
npm test -- UserProfile.test.tsx

# 5. Refactor and repeat
```

---

## Using Claude Code Agents

### test-generator Agent

**Purpose**: Generate comprehensive tests for components, hooks, and utilities.

**How to use**:

1. In Claude Code, request test generation:
   ```
   "Generate comprehensive tests for the MechanismCard component"
   ```

2. The agent will create:
   - Unit tests for rendering
   - Integration tests for user interactions
   - Accessibility tests
   - Edge case tests
   - Mock data and utilities

3. Review and customize the generated tests as needed

**Example output**: See `src/tests/layouts/Header.test.tsx` for a complete example

### code-reviewer Agent

**Purpose**: Review code quality, security, and best practices.

**How to use**:

1. After writing code, request a review:
   ```
   "Review the MechanismGraph component for quality and security"
   ```

2. The agent will analyze:
   - Code quality and maintainability
   - Security vulnerabilities (XSS, injection, etc.)
   - Performance issues
   - Accessibility compliance
   - Best practices adherence

3. Address any issues identified

### mechanism-validator Agent

**Purpose**: Validate mechanism YAML files for scientific accuracy and schema compliance.

**How to use**:

```
"Validate the housing_quality_respiratory mechanism"
```

The agent checks:
- Schema compliance
- Scientific rigor
- Evidence quality
- Structural competency notes

---

## Running Tests

### Unit Tests

```bash
# Run all unit tests
npm test

# Run specific test file
npm test -- App.test.tsx

# Run tests for a component
npm test -- SystemsMapView

# Run in watch mode (auto-rerun on changes)
npm test -- --watch

# Run with coverage
npm test -- --coverage

# Run only changed files
npm test -- --onlyChanged
```

### Accessibility Tests

```bash
# Run all accessibility tests
npm test -- --config=jest-a11y.config.js

# Run specific a11y test
npm test -- Header.a11y.test.tsx

# Run with verbose output
npm test -- --config=jest-a11y.config.js --verbose
```

### Integration Tests

```bash
# Run integration tests
npm test -- *.integration.test.tsx

# Run specific integration test
npm test -- DashboardLayout.integration.test.tsx
```

### E2E Tests

```bash
# Install Playwright browsers (first time only)
npx playwright install

# Run all E2E tests
npx playwright test

# Run specific test file
npx playwright test e2e/dashboard.spec.ts

# Run with UI mode (interactive debugging)
npx playwright test --ui

# Run specific browser
npx playwright test --project=chromium
npx playwright test --project=firefox
npx playwright test --project=webkit

# Run in headed mode (see browser)
npx playwright test --headed

# Debug mode (step through tests)
npx playwright test --debug

# Generate HTML report
npx playwright show-report
```

### Snapshot Tests

```bash
# Run snapshot tests
npm test -- Header.snapshot.test.tsx

# Update snapshots
npm test -- Header.snapshot.test.tsx -u
```

---

## Continuous Integration

### Pre-commit Checklist

Before committing code:

```bash
# 1. Run linter
npm run lint

# 2. Run unit tests with coverage
npm test -- --coverage --watchAll=false

# 3. Run accessibility tests
npm test -- --config=jest-a11y.config.js --watchAll=false

# 4. Run E2E tests (critical paths)
npx playwright test e2e/dashboard.spec.ts

# 5. Check build
npm run build
```

### CI/CD Pipeline

The project uses automated testing in CI:

```yaml
# Example: .github/workflows/test.yml
name: Test Suite

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3

      - name: Install dependencies
        run: npm ci

      - name: Run unit tests
        run: npm test -- --coverage --watchAll=false

      - name: Run accessibility tests
        run: npm test -- --config=jest-a11y.config.js --watchAll=false

      - name: Install Playwright
        run: npx playwright install --with-deps

      - name: Run E2E tests
        run: npx playwright test

      - name: Upload coverage
        uses: codecov/codecov-action@v3
```

---

## Best Practices

### 1. Test Organization

```
frontend/src/
├── components/
│   ├── MechanismCard.tsx
│   └── MechanismCard.test.tsx          # Co-located with component
├── tests/
│   ├── utils/
│   │   ├── test-utils.tsx               # Shared test utilities
│   │   └── d3-test-helpers.ts           # D3-specific helpers
│   └── mocks/
│       ├── handlers.ts                  # MSW request handlers
│       ├── mockData.ts                  # Mock data
│       └── server.ts                    # MSW server setup
└── e2e/
    ├── dashboard.spec.ts                # E2E tests
    ├── systems-map.spec.ts
    └── accessibility.spec.ts
```

### 2. Naming Conventions

- **Unit tests**: `ComponentName.test.tsx`
- **Integration tests**: `ComponentName.integration.test.tsx`
- **Accessibility tests**: `ComponentName.a11y.test.tsx`
- **Snapshot tests**: `ComponentName.snapshot.test.tsx`
- **E2E tests**: `feature-name.spec.ts`

### 3. Test Structure

Use Arrange-Act-Assert (AAA) pattern:

```typescript
test('should filter mechanisms by category', async () => {
  // Arrange
  const { getByLabelText, getAllByRole } = render(<SystemsMapView />);

  // Act
  const filter = getByLabelText(/category/i);
  await userEvent.selectOptions(filter, 'structural');

  // Assert
  const mechanisms = getAllByRole('article');
  expect(mechanisms).toHaveLength(3);
});
```

### 4. Coverage Goals

Aim for:
- **Overall coverage**: ≥80%
- **Critical paths**: ≥90%
- **Accessibility**: 100% WCAG 2.1 AA compliance
- **E2E**: All user flows covered

### 5. Test Data Management

- Use `mockData.ts` for consistent test data
- Use MSW for API mocking (not fetch mocks)
- Create focused test data for edge cases
- Use factories for generating test objects

### 6. Accessibility Testing

Always include accessibility tests:

```typescript
import { axe } from 'jest-axe';

test('should have no accessibility violations', async () => {
  const { container } = render(<MechanismCard {...mockMechanism} />);
  const results = await axe(container);
  expect(results).toHaveNoViolations();
});
```

### 7. Agent Usage Guidelines

**When to use test-generator**:
- Creating tests for new components
- Expanding test coverage
- Need comprehensive edge case coverage
- Starting a new feature

**When to use code-reviewer**:
- Before submitting PRs
- After significant refactoring
- Security-sensitive code
- Performance-critical sections

**When to use mechanism-validator**:
- Adding new mechanisms
- Updating mechanism schemas
- Ensuring scientific accuracy
- Validating evidence quality

### 8. Debugging Failed Tests

```bash
# Run single test in debug mode
node --inspect-brk node_modules/.bin/jest --runInBand ComponentName.test.tsx

# Use React Testing Library debug
import { render, screen } from '@testing-library/react';

test('debug example', () => {
  const { debug } = render(<Component />);
  debug(); // Prints DOM to console

  // Or debug specific element
  debug(screen.getByRole('button'));
});

# Playwright debug
npx playwright test --debug e2e/dashboard.spec.ts
```

### 9. Performance Testing

Monitor test performance:

```bash
# Show slowest tests
npm test -- --listTests --json | grep duration

# Run with timing
npm test -- --verbose
```

### 10. Continuous Improvement

Regular maintenance:

- **Weekly**: Review coverage reports, identify gaps
- **Sprint**: Update tests when requirements change
- **Monthly**: Run full E2E suite across all browsers
- **Quarterly**: Review and optimize test performance

---

## Troubleshooting

### Common Issues

**Issue**: Tests failing with "Cannot find module"
```bash
# Solution: Clear Jest cache
npm test -- --clearCache
```

**Issue**: MSW handlers not intercepting requests
```bash
# Solution: Verify server is started in setupTests.ts
# Check that handlers match the API base URL
```

**Issue**: Playwright tests timing out
```bash
# Solution: Increase timeout in playwright.config.ts
# Or add explicit waits: await page.waitForSelector()
```

**Issue**: Accessibility violations
```bash
# Solution: Run axe-core in browser
# Check ARIA attributes and semantic HTML
# Verify color contrast ratios
```

---

## Resources

- [Jest Documentation](https://jestjs.io/)
- [React Testing Library](https://testing-library.com/react)
- [Playwright Documentation](https://playwright.dev/)
- [jest-axe](https://github.com/nickcolley/jest-axe)
- [MSW Documentation](https://mswjs.io/)
- [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)

---

## Getting Help

- **General questions**: Check this guide and test documentation in `frontend/src/tests/`
- **Agent usage**: Consult `.claude/agents/` for agent-specific docs
- **Bug reports**: Submit issue with test output and environment details
- **Feature requests**: Discuss in team meetings or submit proposal

---

**Last Updated**: 2024-11-18
**Maintained By**: HealthSystems Platform Team
