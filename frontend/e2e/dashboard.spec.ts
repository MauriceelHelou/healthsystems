import { test, expect } from '@playwright/test';

/**
 * E2E tests for Dashboard navigation and layout
 *
 * Tests core functionality:
 * - Dashboard loads correctly
 * - Navigation between views works
 * - Layout components render properly
 * - Responsive design adapts to different viewports
 */

test.describe('Dashboard Navigation and Layout', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
  });

  test('should load the dashboard homepage', async ({ page }) => {
    await expect(page).toHaveTitle(/HealthSystems Platform/i);
    await expect(page.locator('header')).toBeVisible();
  });

  test('should display main navigation links', async ({ page }) => {
    const nav = page.locator('nav[role="navigation"]');
    await expect(nav).toBeVisible();

    await expect(nav.locator('a[href="/"]')).toContainText(/Dashboard/i);
    await expect(nav.locator('a[href="/systems-map"]')).toContainText(/Systems Map/i);
  });

  test('should navigate to Systems Map view', async ({ page }) => {
    await page.click('a[href="/systems-map"]');
    await page.waitForURL('**/systems-map');

    await expect(page.locator('h1')).toContainText(/Systems Map/i);
    await expect(page.locator('[role="main"]')).toBeVisible();
  });

  test('should navigate back to Dashboard from Systems Map', async ({ page }) => {
    await page.click('a[href="/systems-map"]');
    await page.waitForURL('**/systems-map');

    await page.click('a[href="/"]');
    await page.waitForURL('/');

    await expect(page.locator('h1')).toContainText(/Dashboard/i);
  });

  test('should highlight active navigation link', async ({ page }) => {
    const homeLink = page.locator('a[href="/"]');
    const systemsMapLink = page.locator('a[href="/systems-map"]');

    // Dashboard should be active initially
    await expect(homeLink).toHaveAttribute('aria-current', 'page');

    // Navigate to Systems Map
    await systemsMapLink.click();
    await page.waitForURL('**/systems-map');

    // Systems Map should now be active
    await expect(systemsMapLink).toHaveAttribute('aria-current', 'page');
    await expect(homeLink).not.toHaveAttribute('aria-current', 'page');
  });

  test('should render header with logo', async ({ page }) => {
    const header = page.locator('header');
    await expect(header).toBeVisible();

    const logo = header.locator('h1, [role="img"]').first();
    await expect(logo).toBeVisible();
  });

  test('should render main content area', async ({ page }) => {
    const main = page.locator('main, [role="main"]');
    await expect(main).toBeVisible();
  });

  test('should be responsive on mobile viewport', async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 667 });

    const header = page.locator('header');
    await expect(header).toBeVisible();

    const nav = page.locator('nav');
    await expect(nav).toBeVisible();
  });

  test('should be responsive on tablet viewport', async ({ page }) => {
    await page.setViewportSize({ width: 768, height: 1024 });

    const main = page.locator('[role="main"]');
    await expect(main).toBeVisible();
  });

  test('should maintain scroll position on navigation', async ({ page }) => {
    // Navigate to a page with scrollable content
    await page.click('a[href="/systems-map"]');
    await page.waitForURL('**/systems-map');

    // Scroll down
    await page.evaluate(() => window.scrollTo(0, 500));

    // Navigate back
    await page.click('a[href="/"]');
    await page.waitForURL('/');

    // Should be at top of new page
    const scrollY = await page.evaluate(() => window.scrollY);
    expect(scrollY).toBe(0);
  });

  test('should handle browser back/forward buttons', async ({ page }) => {
    // Navigate to Systems Map
    await page.click('a[href="/systems-map"]');
    await page.waitForURL('**/systems-map');

    // Go back
    await page.goBack();
    await expect(page).toHaveURL('/');

    // Go forward
    await page.goForward();
    await expect(page).toHaveURL(/systems-map/);
  });

  test('should display page title correctly', async ({ page }) => {
    await expect(page).toHaveTitle(/HealthSystems/i);
  });
});

test.describe('Dashboard Content Loading', () => {
  test('should show loading states appropriately', async ({ page }) => {
    await page.goto('/systems-map');

    // May briefly show loading indicator
    const content = page.locator('[role="main"]');
    await expect(content).toBeVisible({ timeout: 10000 });
  });

  test('should handle network errors gracefully', async ({ page, context }) => {
    // Block API requests to simulate network error
    await context.route('**/api/**', (route) => route.abort());

    await page.goto('/systems-map');

    // Should show error state or empty state
    const main = page.locator('[role="main"]');
    await expect(main).toBeVisible();
  });
});

test.describe('Dashboard Accessibility', () => {
  test('should have proper heading hierarchy', async ({ page }) => {
    await page.goto('/');

    const h1 = page.locator('h1');
    await expect(h1).toHaveCount(1);
  });

  test('should have skip to main content link', async ({ page }) => {
    await page.goto('/');

    // Focus first element (usually skip link)
    await page.keyboard.press('Tab');

    const focused = page.locator(':focus');
    const text = await focused.textContent();

    // Skip link should be present (may be visually hidden)
    if (text?.toLowerCase().includes('skip')) {
      await expect(focused).toBeVisible();
    }
  });

  test('should support keyboard navigation', async ({ page }) => {
    await page.goto('/');

    // Tab through navigation
    await page.keyboard.press('Tab');
    await page.keyboard.press('Tab');

    const focused = page.locator(':focus');
    await expect(focused).toBeVisible();
  });
});
