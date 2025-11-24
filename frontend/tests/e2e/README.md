# End-to-End (E2E) Tests

This directory contains Playwright E2E tests for the HealthSystems Platform frontend.

## Test Files

- **dashboard.spec.ts** - Dashboard navigation, layout, and content loading
- **systems-map.spec.ts** - Interactive graph visualization and interactions
- **mechanism-details.spec.ts** - Mechanism detail views and navigation
- **filters-search.spec.ts** - Search and filtering functionality
- **accessibility.spec.ts** - WCAG 2.1 AA compliance and keyboard navigation

## Running Tests

### Prerequisites

```bash
# Install Playwright browsers (first time only)
npx playwright install

# Or install with system dependencies
npx playwright install --with-deps
```

### Basic Commands

```bash
# Run all E2E tests
npx playwright test

# Run specific test file
npx playwright test e2e/dashboard.spec.ts

# Run with UI mode (interactive)
npx playwright test --ui

# Run in headed mode (see browser)
npx playwright test --headed

# Debug mode (step through)
npx playwright test --debug

# Run specific browser
npx playwright test --project=chromium
npx playwright test --project=firefox
npx playwright test --project=webkit
```

### Advanced Options

```bash
# Run tests in parallel (default)
npx playwright test --workers=4

# Run tests serially
npx playwright test --workers=1

# Run with specific timeout
npx playwright test --timeout=60000

# Run only tests matching pattern
npx playwright test --grep="should navigate"

# Skip tests matching pattern
npx playwright test --grep-invert="mobile"

# Generate HTML report
npx playwright show-report

# Update snapshots
npx playwright test --update-snapshots
```

## Test Structure

### Dashboard Tests

Tests basic navigation and layout:
- Page loads correctly
- Navigation links work
- Active route highlighting
- Responsive design
- Browser history navigation

### Systems Map Tests

Tests interactive visualization:
- Graph rendering (SVG, nodes, edges)
- Node/mechanism interactions (hover, click, select)
- Zoom and pan functionality
- Filtering by category
- Search mechanisms
- Performance with large datasets

### Mechanism Details Tests

Tests detail view functionality:
- Details display when selecting mechanism
- All mechanism fields render
- Evidence and pathway information
- Navigation to/from details
- Close/escape functionality
- Keyboard accessibility

### Filters and Search Tests

Tests filtering and search:
- Search input functionality
- Category filtering
- Directionality filtering
- Combined filters
- Clear/reset functionality
- Real-time results updates
- Empty state handling

### Accessibility Tests

Tests WCAG 2.1 AA compliance:
- Keyboard navigation (Tab, Shift+Tab, Enter, Space, Escape)
- Screen reader support (ARIA, landmarks, headings)
- Focus management (modal trapping, restoration)
- Color contrast (automated checks with axe-core)
- Touch targets (minimum 44x44px on mobile)
- Zoom support

## Writing New Tests

### Test Template

```typescript
import { test, expect } from '@playwright/test';

test.describe('Feature Name', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/route');
  });

  test('should do something', async ({ page }) => {
    // Arrange
    const element = page.locator('selector');

    // Act
    await element.click();

    // Assert
    await expect(element).toBeVisible();
  });
});
```

### Best Practices

1. **Use semantic selectors**:
   ```typescript
   // Good
   page.getByRole('button', { name: 'Submit' })
   page.getByLabel('Email address')
   page.getByText('Welcome')

   // Avoid
   page.locator('.btn-primary')
   page.locator('#email-input')
   ```

2. **Wait for elements explicitly**:
   ```typescript
   await page.waitForSelector('svg', { timeout: 10000 });
   await page.waitForURL('**/systems-map');
   await page.waitForLoadState('networkidle');
   ```

3. **Use test isolation**:
   ```typescript
   test.beforeEach(async ({ page }) => {
     // Each test starts fresh
     await page.goto('/');
   });
   ```

4. **Handle async properly**:
   ```typescript
   // Wait for actions to complete
   await page.click('button');
   await page.waitForTimeout(300); // Allow transitions

   // Check visibility before interacting
   const isVisible = await element.isVisible();
   if (isVisible) {
     await element.click();
   }
   ```

5. **Test user flows, not implementation**:
   ```typescript
   // Good - tests user behavior
   test('user can filter mechanisms by category', async ({ page }) => {
     await page.selectOption('[name="category"]', 'structural');
     await expect(page.locator('.mechanism-card')).toHaveCount(3);
   });

   // Avoid - tests implementation details
   test('filter function is called with correct params', async () => {
     // Don't test internal function calls in E2E
   });
   ```

## Debugging Tests

### Interactive Debugging

```bash
# Launch Playwright Inspector
npx playwright test --debug

# Debug specific test
npx playwright test --debug e2e/dashboard.spec.ts
```

### Screenshots and Videos

Playwright automatically captures:
- Screenshots on failure
- Videos on retry (configurable)
- Traces for debugging

```typescript
// Manual screenshot
await page.screenshot({ path: 'screenshot.png' });

// Full page screenshot
await page.screenshot({ path: 'full.png', fullPage: true });
```

### Console Logs

```typescript
// Capture console messages
page.on('console', (msg) => console.log('Browser:', msg.text()));

// Capture page errors
page.on('pageerror', (error) => console.log('Page error:', error));

// Capture network requests
page.on('request', (request) => console.log('Request:', request.url()));
page.on('response', (response) => console.log('Response:', response.url()));
```

### Test Artifacts

After running tests, check:
- `playwright-report/` - HTML report
- `test-results/` - Screenshots and traces
- `videos/` - Test recordings (if enabled)

## CI/CD Integration

### GitHub Actions

```yaml
- name: Install Playwright
  run: npx playwright install --with-deps

- name: Run E2E tests
  run: npx playwright test

- name: Upload report
  if: always()
  uses: actions/upload-artifact@v3
  with:
    name: playwright-report
    path: playwright-report/
```

### Environment Variables

```bash
# Set base URL for tests
export PLAYWRIGHT_BASE_URL=https://staging.example.com

# Run headless (default in CI)
export CI=true

# Custom timeout
export PLAYWRIGHT_TIMEOUT=30000
```

## Performance Optimization

### Parallel Execution

```typescript
// playwright.config.ts
export default defineConfig({
  workers: process.env.CI ? 2 : 4, // Adjust for CI
  fullyParallel: true,
});
```

### Reuse Authentication

```typescript
// auth.setup.ts
test('authenticate', async ({ page }) => {
  await page.goto('/login');
  await page.fill('[name="email"]', 'user@example.com');
  await page.fill('[name="password"]', 'password');
  await page.click('button[type="submit"]');

  // Save authentication state
  await page.context().storageState({ path: 'auth.json' });
});

// Use in tests
test.use({ storageState: 'auth.json' });
```

### Sharding

```bash
# Split tests across 3 machines
npx playwright test --shard=1/3
npx playwright test --shard=2/3
npx playwright test --shard=3/3
```

## Troubleshooting

### Common Issues

**Tests timing out**:
```typescript
// Increase timeout
test.setTimeout(60000);

// Or in config
export default defineConfig({
  timeout: 30000,
});
```

**Element not found**:
```typescript
// Wait for element
await page.waitForSelector('button', { timeout: 10000 });

// Check if exists first
const count = await page.locator('button').count();
if (count > 0) {
  await page.click('button');
}
```

**Flaky tests**:
```typescript
// Use waitFor instead of timeout
await page.waitForSelector('.loaded');

// Wait for network to settle
await page.waitForLoadState('networkidle');

// Retry specific assertions
await expect(element).toBeVisible({ timeout: 5000 });
```

**Browser launch fails**:
```bash
# Reinstall browsers
npx playwright install --force

# Install system dependencies
npx playwright install-deps
```

## Resources

- [Playwright Documentation](https://playwright.dev/)
- [Best Practices](https://playwright.dev/docs/best-practices)
- [API Reference](https://playwright.dev/docs/api/class-playwright)
- [Debugging Guide](https://playwright.dev/docs/debug)
- [CI/CD Examples](https://playwright.dev/docs/ci)

---

**Last Updated**: 2024-11-18
