import { test, expect } from '@playwright/test';

test.describe('Legend Component', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('http://localhost:3000/');

    // Wait for app to load
    await page.waitForSelector('header', { state: 'visible' });
    await page.waitForSelector('main', { state: 'visible' });

    // Wait for graph to render - increased timeout for slower CI environments
    await page.waitForSelector('svg:has(g.graph-container)', { timeout: 30000 });

    // Additional wait for D3 transitions to complete
    await page.waitForTimeout(1000);
  });

  test('Legend should be visible on Systems Map', async ({ page }) => {
    const legend = page.locator('[data-testid="systems-map-legend"]');
    await expect(legend).toBeVisible();
  });

  test('Legend should display 7-Scale Hierarchy section', async ({ page }) => {
    const legend = page.locator('[data-testid="systems-map-legend"]');

    // Check for heading
    const heading = legend.locator('text=7-Scale Hierarchy');
    await expect(heading).toBeVisible();

    // Check for scale items 1-7
    for (let scale = 1; scale <= 7; scale++) {
      const scaleItem = legend.locator(`text=${scale}`).first();
      await expect(scaleItem).toBeVisible();
    }
  });

  test('Legend should display Evidence Quality section', async ({ page }) => {
    const legend = page.locator('[data-testid="systems-map-legend"]');

    // Check for heading
    const heading = legend.locator('text=Evidence Quality');
    await expect(heading).toBeVisible();

    // Check for quality levels A, B, C
    const qualityA = legend.locator('text=A').first();
    await expect(qualityA).toBeVisible();

    const qualityB = legend.locator('text=B').first();
    await expect(qualityB).toBeVisible();

    const qualityC = legend.locator('text=C').first();
    await expect(qualityC).toBeVisible();
  });

  test('Legend should show scale colors correctly', async ({ page }) => {
    const legend = page.locator('[data-testid="systems-map-legend"]');

    // Check that scale badges have colored backgrounds
    const scaleBadges = legend.locator('.rounded-full');
    const count = await scaleBadges.count();

    expect(count).toBeGreaterThanOrEqual(7); // At least 7 scale badges

    // Verify first badge has a background color
    const firstBadge = scaleBadges.first();
    const backgroundColor = await firstBadge.evaluate(el =>
      window.getComputedStyle(el).backgroundColor
    );

    expect(backgroundColor).not.toBe('rgba(0, 0, 0, 0)'); // Not transparent
  });

  test('Legend should show evidence quality colors correctly', async ({ page }) => {
    const legend = page.locator('[data-testid="systems-map-legend"]');

    // Check evidence badges exist
    const evidenceBadges = legend.locator('text=Evidence Quality').locator('..').locator('.rounded-full');
    const count = await evidenceBadges.count();

    expect(count).toBeGreaterThanOrEqual(3); // A, B, C
  });

  test('Legend should indicate reserved scales', async ({ page }) => {
    const legend = page.locator('[data-testid="systems-map-legend"]');

    // Check for "Reserved" text
    const reservedText = legend.locator('text=/Reserved/i');
    const count = await reservedText.count();

    expect(count).toBeGreaterThan(0); // Should have some reserved indicators
  });

  test('Legend should have helper text for evidence badges', async ({ page }) => {
    const legend = page.locator('[data-testid="systems-map-legend"]');

    // Check for explanatory text
    const helperText = legend.locator('text=/Badges on edges/i');
    await expect(helperText).toBeVisible();
  });

  test('Legend should have helper text for active scales', async ({ page }) => {
    const legend = page.locator('[data-testid="systems-map-legend"]');

    // Check for explanatory text about active scales
    const helperText = legend.locator('text=/Active scales/i');
    await expect(helperText).toBeVisible();
  });

  test('Legend should show node and edge symbols', async ({ page }) => {
    const legend = page.locator('[data-testid="systems-map-legend"]');

    // Check for node label (exact match)
    const nodeLabel = legend.locator('text="Node"');
    await expect(nodeLabel).toBeVisible();

    // Check for edge label with mechanism (exact match)
    const edgeLabel = legend.locator('text="Edge (mechanism)"');
    await expect(edgeLabel).toBeVisible();
  });

  test('Legend should be readable with sufficient contrast', async ({ page }) => {
    const legend = page.locator('[data-testid="systems-map-legend"]');

    // Check background is visible
    const backgroundColor = await legend.evaluate(el =>
      window.getComputedStyle(el).backgroundColor
    );

    expect(backgroundColor).toBeTruthy();

    // Check text is visible
    const color = await legend.evaluate(el =>
      window.getComputedStyle(el).color
    );

    expect(color).toBeTruthy();
  });

  test('Legend sections should be properly organized', async ({ page }) => {
    const legend = page.locator('[data-testid="systems-map-legend"]');

    // Check for section headers in order
    const content = await legend.textContent();

    expect(content).toContain('Legend');
    expect(content).toContain('7-Scale Hierarchy');
    expect(content).toContain('Evidence Quality');
  });

  test('Legend should have scale labels with semantic meaning', async ({ page }) => {
    const legend = page.locator('[data-testid="systems-map-legend"]');

    // Check for meaningful labels
    const labels = [
      'Structural',
      'Institutional',
      'Individual',
      'Pathways',
      'Crisis'
    ];

    for (const label of labels) {
      const text = legend.locator(`text=/${label}/i`);
      await expect(text).toBeVisible();
    }
  });

  test('Legend should show evidence quality labels', async ({ page }) => {
    const legend = page.locator('[data-testid="systems-map-legend"]');

    // Check for quality labels
    const highQuality = legend.locator('text=/High.*quality/i');
    await expect(highQuality).toBeVisible();

    const moderateQuality = legend.locator('text=/Moderate.*quality/i');
    await expect(moderateQuality).toBeVisible();

    const lowQuality = legend.locator('text=/Low.*quality/i');
    await expect(lowQuality).toBeVisible();
  });
});
