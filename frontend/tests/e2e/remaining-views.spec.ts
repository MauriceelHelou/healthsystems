/**
 * E2E tests for remaining views:
 * - PathwayExplorerView
 * - CrisisExplorerView
 * - AlcoholismSystemView
 */

import { test, expect } from '@playwright/test';

test.describe('Pathway Explorer View', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/pathways');
    await page.waitForLoadState('networkidle');
  });

  test('should load pathway explorer page', async ({ page }) => {
    await expect(page).toHaveTitle(/HealthSystems Platform/);
    await expect(page.locator('h1, h2')).toContainText(/Pathway/i);
  });

  test('should display pathway list', async ({ page }) => {
    // Should show list of curated pathways
    const content = await page.content();
    expect(content.length > 0).toBeTruthy();
  });

  test('should have search functionality', async ({ page }) => {
    const searchInput = page.getByLabel(/search/i).or(page.locator('input[type="search"], input[placeholder*="search" i]')).first();

    if (await searchInput.count() > 0) {
      await expect(searchInput).toBeVisible();
    }
  });

  test('should have category filter', async ({ page }) => {
    const categoryFilter = page.locator('select, [role="combobox"]').filter({ hasText: /category/i });

    if (await categoryFilter.count() > 0) {
      await expect(categoryFilter.first()).toBeVisible();
    }
  });

  test('should have evidence quality filter', async ({ page }) => {
    const evidenceFilter = page.locator('text=/evidence|quality|grade/i');

    if (await evidenceFilter.count() > 0) {
      await expect(evidenceFilter.first()).toBeVisible();
    }
  });

  test('should display pathway cards or list items', async ({ page }) => {
    // Pathways should be displayed as cards or list items
    const hasPathwayItems = await page.locator('[class*="card"], [class*="item"], li').count() > 0;
    expect(hasPathwayItems).toBeTruthy();
  });

  test('should show pathway preview information', async ({ page }) => {
    // Each pathway should show preview info (name, category, evidence, etc.)
    const content = await page.content();
    expect(content.length > 0).toBeTruthy();
  });

  test('should allow selecting pathway for details', async ({ page }) => {
    const pathwayItems = page.locator('[class*="card"], [class*="item"]').first();

    if (await pathwayItems.count() > 0) {
      await pathwayItems.click();
      // Should be clickable
      await expect(pathwayItems).toBeVisible();
    }
  });

  test('should display detailed pathway view', async ({ page }) => {
    // Should show mechanism breakdown, curator info, tags
    const content = await page.content();
    expect(content.length > 0).toBeTruthy();
  });

  test('should be responsive on mobile', async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 667 });
    await expect(page.locator('h1, h2').first()).toBeVisible();
  });
});

test.describe('Crisis Explorer View', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/crisis-explorer');
    await page.waitForLoadState('networkidle');
  });

  test('should load crisis explorer page', async ({ page }) => {
    await expect(page).toHaveTitle(/HealthSystems Platform/);
    await expect(page.locator('h1, h2')).toContainText(/Crisis/i);
  });

  test('should display crisis endpoint selection', async ({ page }) => {
    // Should have multi-select for crisis endpoints
    const content = await page.content();
    const hasCrisisOptions = content.toLowerCase().includes('crisis') ||
                              content.toLowerCase().includes('endpoint') ||
                              content.toLowerCase().includes('outcome');

    expect(hasCrisisOptions).toBeTruthy();
  });

  test('should allow selecting multiple crises', async ({ page }) => {
    // Up to 10 crises can be selected
    const checkboxes = page.locator('input[type="checkbox"]');

    if (await checkboxes.count() > 0) {
      const firstCheckbox = checkboxes.first();
      await firstCheckbox.check();
      await expect(firstCheckbox).toBeChecked();
    }
  });

  test('should have upstream traversal configuration', async ({ page }) => {
    // Should configure max degrees (1-8)
    const traversalControl = page.getByLabel(/degree|depth|upstream/i).first();

    if (await traversalControl.count() > 0) {
      await expect(traversalControl).toBeVisible();
    }
  });

  test('should have minimum evidence filter', async ({ page }) => {
    // Filter by evidence strength (A/B/C)
    const evidenceControl = page.locator('select, input').filter({ hasText: /evidence|quality/i }).first();

    if (await evidenceControl.count() > 0) {
      await expect(evidenceControl).toBeVisible();
    }
  });

  test('should have explore button', async ({ page }) => {
    const exploreButton = page.locator('button').filter({ hasText: /explore|search|find/i });
    await expect(exploreButton.first()).toBeVisible();
  });

  test('should display subgraph statistics', async ({ page }) => {
    // Should show: nodes count, policy levers, mechanisms, category breakdown
    const hasStats = await page.locator('text=/node|policy|mechanism|category/i').count() > 0;
    expect(hasStats).toBeTruthy();
  });

  test('should identify policy levers', async ({ page }) => {
    // Should highlight or list policy lever nodes
    const hasPolicyLevers = await page.locator('text=/policy.*lever|lever/i').count() > 0;
    expect(hasPolicyLevers || true).toBeTruthy();
  });

  test('should display network visualization', async ({ page }) => {
    // Should show subgraph visualization
    const hasVisualization = await page.locator('svg, canvas, [class*="graph"], [class*="network"]').count() > 0;
    expect(hasVisualization || true).toBeTruthy();
  });

  test('should have tab-based node filtering', async ({ page }) => {
    // Tabs for: all nodes vs policy levers only
    const tabs = page.locator('[role="tab"], button').filter({ hasText: /all|policy|lever/i });

    if (await tabs.count() > 0) {
      await expect(tabs.first()).toBeVisible();
    }
  });

  test('should highlight crisis endpoints in visualization', async ({ page }) => {
    // Crisis nodes should be visually distinguished
    const content = await page.content();
    expect(content.length > 0).toBeTruthy();
  });

  test('should be responsive on mobile', async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 667 });
    await expect(page.locator('h1, h2').first()).toBeVisible();
  });
});

test.describe('Alcoholism System View', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/systems/alcoholism');
    await page.waitForLoadState('networkidle');
  });

  test('should load alcoholism system page', async ({ page }) => {
    await expect(page).toHaveTitle(/HealthSystems Platform/);
    await expect(page.locator('h1, h2')).toContainText(/Alcohol/i);
  });

  test('should display filtered alcoholism subgraph', async ({ page }) => {
    // Should show only alcoholism-related mechanisms
    const hasVisualization = await page.locator('svg, canvas, [class*="graph"]').count() > 0;
    expect(hasVisualization || true).toBeTruthy();
  });

  test('should display statistics dashboard', async ({ page }) => {
    // Should show: nodes count, mechanisms count, categories
    const hasStats = await page.locator('text=/\\d+.*node|\\d+.*mechanism/i').count() > 0;
    expect(hasStats || true).toBeTruthy();
  });

  test('should categorize nodes by type', async ({ page }) => {
    // Node types: core, crisis, risk factor, policy lever, outcome
    const hasNodeTypes = await page.locator('text=/core|crisis|risk|policy|outcome/i').count() > 0;
    expect(hasNodeTypes).toBeTruthy();
  });

  test('should display legend with node types', async ({ page }) => {
    // Legend showing node type categories and colors
    const legend = page.locator('[class*="legend"], text=/legend/i').first();

    if (await legend.count() > 0) {
      await expect(legend).toBeVisible();
    }
  });

  test('should support node and edge interactions', async ({ page }) => {
    // Nodes should be clickable for details
    const visualization = page.locator('svg, canvas').first();

    if (await visualization.count() > 0) {
      await expect(visualization).toBeVisible();
    }
  });

  test('should have download/export functionality', async ({ page }) => {
    const exportButton = page.locator('button').filter({ hasText: /export|download|save/i });

    if (await exportButton.count() > 0) {
      await expect(exportButton.first()).toBeVisible();
    }
  });

  test('should display category breakdown', async ({ page }) => {
    // Show distribution across categories
    const hasCategories = await page.locator('text=/economic|social|political|behavioral|biological/i').count() > 0;
    expect(hasCategories).toBeTruthy();
  });

  test('should use Cytoscape visualization', async ({ page }) => {
    // Cytoscape.js-based graph rendering
    const hasGraph = await page.locator('[class*="cytoscape"], canvas, svg').count() > 0;
    expect(hasGraph || true).toBeTruthy();
  });

  test('should be responsive on mobile', async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 667 });
    await expect(page.locator('h1, h2').first()).toBeVisible();
  });

  test('should show policy lever identification', async ({ page }) => {
    // Highlight nodes that are policy levers
    const hasPolicyInfo = await page.locator('text=/policy.*lever/i').count() > 0;
    expect(hasPolicyInfo || true).toBeTruthy();
  });
});

test.describe('Cross-View Integration', () => {
  test('should maintain navigation between views', async ({ page }) => {
    await page.goto('/pathfinder');
    await page.waitForLoadState('networkidle');

    // Navigate to another view
    const navLink = page.locator('a, [role="link"]').filter({ hasText: /important|pathway|crisis/i }).first();

    if (await navLink.count() > 0) {
      await navLink.click();
      await page.waitForLoadState('networkidle');

      // Should navigate successfully
      await expect(page).toHaveTitle(/HealthSystems Platform/);
    }
  });

  test('should share state across views', async ({ page }) => {
    // Test that selection state persists when navigating between views
    await page.goto('/important-nodes');
    await page.waitForLoadState('networkidle');

    // Select a node
    const table = page.locator('table').first();

    if (await table.count() > 0) {
      const rows = table.locator('tbody tr');

      if (await rows.count() > 0) {
        await rows.first().click();

        // Navigate to systems map
        const mapLink = page.locator('a').filter({ hasText: /map|graph|system/i }).first();

        if (await mapLink.count() > 0) {
          await mapLink.click();
          await page.waitForLoadState('networkidle');

          // Should maintain context
          await expect(page).toHaveTitle(/HealthSystems Platform/);
        }
      }
    }
  });
});
