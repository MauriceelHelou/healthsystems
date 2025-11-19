# Testing Quick Reference Card

Quick commands and tips for testing the HealthSystems Platform frontend.

---

## Installation

```bash
# First time setup
cd frontend
npm install
npm run playwright:install
```

---

## Running Tests

### Unit Tests

```bash
npm test                          # Run all unit tests (watch mode)
npm test -- App.test.tsx          # Run specific test file
npm test -- --coverage            # Run with coverage report
npm test -- --watchAll=false      # Run once (no watch)
npm test -- --onlyChanged         # Run only changed files
```

### Accessibility Tests

```bash
npm run test:a11y                 # Run all a11y tests
npm test -- Header.a11y.test.tsx  # Run specific a11y test
```

### E2E Tests

```bash
npm run test:e2e                  # Run all E2E tests
npm run test:e2e:ui               # Run with UI mode (interactive)
npm run test:e2e:headed           # Run with visible browser
npm run test:e2e:debug            # Run in debug mode

# Specific test files
npx playwright test e2e/dashboard.spec.ts
npx playwright test e2e/systems-map.spec.ts

# Specific browsers
npx playwright test --project=chromium
npx playwright test --project=firefox
```

### All Tests (CI Mode)

```bash
npm run test:ci                   # Run all tests (unit + a11y + e2e)
```

---

## Test Coverage

```bash
npm run test:coverage             # Generate coverage report
open coverage/lcov-report/index.html  # View coverage (macOS/Linux)
start coverage/lcov-report/index.html # View coverage (Windows)
```

---

## Using Claude Code Agents

### Generate Tests

```
"Generate comprehensive tests for the MechanismCard component"
```

### Review Code

```
"Review the SystemsMapView component for quality and security"
```

### Validate Mechanisms

```
"Validate the housing_quality_respiratory mechanism file"
```

---

## Common Test Patterns

### Component Test

```typescript
import { render, screen } from './tests/utils/test-utils';
import { userEvent } from '@testing-library/user-event';

test('should render component', () => {
  render(<Component />);
  expect(screen.getByRole('button')).toBeInTheDocument();
});
```

### Accessibility Test

```typescript
import { axe } from 'jest-axe';

test('should have no a11y violations', async () => {
  const { container } = render(<Component />);
  const results = await axe(container);
  expect(results).toHaveNoViolations();
});
```

### E2E Test

```typescript
import { test, expect } from '@playwright/test';

test('should navigate to systems map', async ({ page }) => {
  await page.goto('/');
  await page.click('a[href="/systems-map"]');
  await expect(page).toHaveURL(/systems-map/);
});
```

---

## Debugging

### Debug Unit Tests

```bash
# Run single test in debug mode
node --inspect-brk node_modules/.bin/jest --runInBand Component.test.tsx

# Use React Testing Library debug
const { debug } = render(<Component />);
debug(); // Prints DOM to console
```

### Debug E2E Tests

```bash
npx playwright test --debug              # Step through tests
npx playwright show-report               # View HTML report
```

---

## File Locations

```
frontend/
├── jest.config.js                    # Main Jest config
├── playwright.config.ts              # Playwright config
├── TESTING_WORKFLOW.md               # Full workflow guide
│
├── src/
│   ├── setupTests.ts                 # Global test setup
│   ├── tests/
│   │   ├── utils/test-utils.tsx      # Custom render
│   │   └── mocks/                    # MSW mocks
│   │       ├── mockData.ts
│   │       ├── handlers.ts
│   │       └── server.ts
│
└── e2e/
    ├── README.md                     # E2E guide
    ├── dashboard.spec.ts
    ├── systems-map.spec.ts
    ├── mechanism-details.spec.ts
    ├── filters-search.spec.ts
    └── accessibility.spec.ts
```

---

## Coverage Goals

- **Overall**: ≥80%
- **Functions**: ≥75%
- **Branches**: ≥75%
- **Lines**: ≥80%
- **Accessibility**: 100% WCAG 2.1 AA

---

## Pre-Commit Checklist

```bash
□ npm run lint                    # Check code style
□ npm test -- --coverage          # Run unit tests
□ npm run test:a11y               # Run a11y tests
□ npm run test:e2e                # Run E2E tests
□ npm run build                   # Verify build succeeds
```

---

## Useful Links

- [Full Testing Workflow](./TESTING_WORKFLOW.md)
- [E2E Testing Guide](./e2e/README.md)
- [Implementation Summary](../TESTING_IMPLEMENTATION_SUMMARY.md)

---

**Last Updated**: 2024-11-18
