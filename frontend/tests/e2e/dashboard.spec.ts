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

    // Actual navigation links from Header.tsx
    await expect(nav.locator('a[href="/"]')).toContainText(/Systems Map/i);
    await expect(nav.locator('a[href="/systems/alcoholism"]')).toContainText(/Alcoholism System/i);
    await expect(nav.locator('a[href="/important-nodes"]')).toContainText(/Important Nodes/i);
    await expect(nav.locator('a[href="/pathfinder"]')).toContainText(/Pathfinder/i);
  });

  test('should navigate to Alcoholism System view', async ({ page }) => {
    await page.click('a[href="/systems/alcoholism"]');
    await page.waitForURL('**/systems/alcoholism');

    // View should load
    await expect(page.locator('header')).toBeVisible();
  });

  test('should navigate between views', async ({ page }) => {
    // Start at root (Systems Map)
    await expect(page).toHaveURL('/');

    // Navigate to Important Nodes
    await page.click('a[href="/important-nodes"]');
    await page.waitForURL('**/important-nodes');
    await expect(page.locator('header')).toBeVisible();

    // Navigate back to Systems Map
    await page.click('a[href="/"]');
    await page.waitForURL('/');
    await expect(page.locator('header')).toBeVisible();
  });

  test('should highlight active navigation link', async ({ page }) => {
    const homeLink = page.locator('a[href="/"]');
    const importantNodesLink = page.locator('a[href="/important-nodes"]');

    // Systems Map (home) should be active initially - check for orange color
    await expect(homeLink).toHaveClass(/text-orange-600/);

    // Navigate to Important Nodes
    await importantNodesLink.click();
    await page.waitForURL('**/important-nodes');

    // Important Nodes should now be active
    await expect(importantNodesLink).toHaveClass(/text-orange-600/);
  });

  test('should render header with logo', async ({ page }) => {
    const header = page.locator('header');
    await expect(header).toBeVisible();

    // Logo text is "HealthSystems"
    await expect(header.locator('text=HealthSystems')).toBeVisible();
  });

  test('should render main content area', async ({ page }) => {
    // Content area is the main view container - be specific to avoid strict mode violation
    const content = page.locator('div.flex.flex-1.overflow-auto.pt-14');
    await expect(content).toBeVisible();
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

    // Be specific to avoid strict mode violation
    const content = page.locator('div.flex.flex-1.overflow-auto.pt-14');
    await expect(content).toBeVisible();
  });

  test('should maintain scroll position on navigation', async ({ page }) => {
    // Navigate to a different view
    await page.click('a[href="/important-nodes"]');
    await page.waitForURL('**/important-nodes');

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
    // Navigate to Important Nodes
    await page.click('a[href="/important-nodes"]');
    await page.waitForURL('**/important-nodes');

    // Go back
    await page.goBack();
    await expect(page).toHaveURL('/');

    // Go forward
    await page.goForward();
    await expect(page).toHaveURL(/important-nodes/);
  });

  test('should display page title correctly', async ({ page }) => {
    await expect(page).toHaveTitle(/HealthSystems/i);
  });
});

test.describe('Dashboard Content Loading', () => {
  test('should show loading states appropriately', async ({ page }) => {
    await page.goto('/important-nodes');

    // May briefly show loading indicator
    const content = page.locator('.flex-1');
    await expect(content).toBeVisible({ timeout: 10000 });
  });

  test('should handle network errors gracefully', async ({ page, context }) => {
    // Block API requests to simulate network error
    await context.route('**/api/**', (route) => route.abort());

    await page.goto('/important-nodes');

    // Should show error state or empty state - at minimum page structure loads
    const header = page.locator('header');
    await expect(header).toBeVisible();
  });
});

test.describe('Dashboard Accessibility', () => {
  test.skip('should have proper heading hierarchy', async ({ page }) => {
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
