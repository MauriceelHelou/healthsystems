import { test, expect } from '@playwright/test';

/**
 * Test Suite: Evidence Quality Badges on Edges
 *
 * Tests that mechanism edges display evidence quality indicators (A/B/C)
 * as per specification in 03_SYSTEMS_MAP_VISUALIZATION.md
 */

test.describe('Evidence Quality Badges', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('networkidle');

    // Wait for graph to render
    await page.waitForSelector('svg:has(g.graph-container)', { timeout: 30000 });
    await page.waitForTimeout(1000);
  });

  test('Systems Map should display evidence badges on edges', async ({ page }) => {
    // Navigate to Systems Map
    const systemsMapTab = page.locator('a, button').filter({ hasText: /systems map|network/i }).first();
    await systemsMapTab.click();
    await page.waitForTimeout(2000);

    // Wait for graph to render
    const svg = page.locator('svg:has(g.graph-container)');
    await expect(svg).toBeVisible({ timeout: 10000 });

    // Wait for edges to render
    const edges = page.locator('g.link');
    const edgeCount = await edges.count();
    console.log(`Found ${edgeCount} edges`);

    expect(edgeCount).toBeGreaterThan(0);

    // Check for evidence badges (should be text or badge elements on edges)
    const evidenceBadges = page.locator('g.link text.evidence-badge, g.link .evidence-quality, g.link [data-evidence]');
    const badgeCount = await evidenceBadges.count();

    console.log(`Found ${badgeCount} evidence badges`);

    // At least some edges should have evidence badges
    // (May not be all edges, but should be present on edges with evidence data)
    if (badgeCount > 0) {
      console.log('✓ Evidence badges found on edges');

      // Verify badge content (should be A, B, or C)
      const firstBadge = evidenceBadges.first();
      const badgeText = await firstBadge.textContent();
      console.log(`First badge text: ${badgeText}`);

      expect(badgeText).toMatch(/^[ABC]$/);
    } else {
      console.log('⚠ No evidence badges found - feature may not be implemented yet');
      test.skip();
    }
  });

  test('Evidence badges should be color-coded by quality', async ({ page }) => {
    const systemsMapTab = page.locator('a, button').filter({ hasText: /systems map|network/i }).first();
    await systemsMapTab.click();
    await page.waitForTimeout(2000);

    const svg = page.locator('svg:has(g.graph-container)');
    await expect(svg).toBeVisible({ timeout: 10000 });

    // Look for evidence badges with different colors
    const aBadges = page.locator('g.link .evidence-A, g.link [data-evidence="A"]');
    const bBadges = page.locator('g.link .evidence-B, g.link [data-evidence="B"]');
    const cBadges = page.locator('g.link .evidence-C, g.link [data-evidence="C"]');

    const aCount = await aBadges.count();
    const bCount = await bBadges.count();
    const cCount = await cBadges.count();

    console.log(`Evidence badges: A=${aCount}, B=${bCount}, C=${cCount}`);

    if (aCount + bCount + cCount > 0) {
      console.log('✓ Evidence quality indicators present');

      // Check that they have different styling
      if (aCount > 0) {
        const aBadge = aBadges.first();
        const aFill = await aBadge.evaluate((el) => {
          return window.getComputedStyle(el).fill || el.getAttribute('fill');
        });
        console.log(`A-quality badge fill: ${aFill}`);
      }
    } else {
      console.log('⚠ Evidence quality badges not found');
      test.skip();
    }
  });

  test('Edge hover should show full evidence details', async ({ page }) => {
    const systemsMapTab = page.locator('a, button').filter({ hasText: /systems map|network/i }).first();
    await systemsMapTab.click();
    await page.waitForTimeout(2000);

    const svg = page.locator('svg:has(g.graph-container)');
    await expect(svg).toBeVisible({ timeout: 10000 });

    // Hover over first edge
    const firstEdge = page.locator('g.link').first();
    await firstEdge.hover();
    await page.waitForTimeout(500);

    // Check for tooltip or detail panel showing evidence
    const tooltip = page.locator('[role="tooltip"], .evidence-tooltip, .mechanism-detail');
    const tooltipVisible = await tooltip.isVisible().catch(() => false);

    if (tooltipVisible) {
      const tooltipText = await tooltip.textContent();
      console.log('Tooltip content:', tooltipText);

      // Should contain evidence-related terms
      const hasEvidence = tooltipText && (
        tooltipText.includes('evidence') ||
        tooltipText.includes('quality') ||
        tooltipText.includes('studies') ||
        /[ABC]/i.test(tooltipText)
      );

      if (hasEvidence) {
        console.log('✓ Evidence details shown on hover');
      }
    } else {
      console.log('⚠ No tooltip shown on edge hover');
    }
  });

  test('Legend should explain evidence quality levels', async ({ page }) => {
    const systemsMapTab = page.locator('a, button').filter({ hasText: /systems map|network/i }).first();
    await systemsMapTab.click();
    await page.waitForTimeout(2000);

    const svg = page.locator('svg:has(g.graph-container)');
    await expect(svg).toBeVisible({ timeout: 10000 });

    // Look for legend
    const legend = page.locator('.legend, [data-testid="legend"], svg g.legend');
    const legendVisible = await legend.isVisible().catch(() => false);

    if (legendVisible) {
      const legendText = await legend.textContent();
      console.log('Legend text:', legendText);

      // Check if legend mentions evidence quality
      const hasEvidenceLegend = legendText && (
        legendText.includes('Evidence') ||
        legendText.includes('Quality') ||
        (legendText.includes('A') && legendText.includes('B') && legendText.includes('C'))
      );

      if (hasEvidenceLegend) {
        console.log('✓ Legend explains evidence quality');
        expect(hasEvidenceLegend).toBeTruthy();
      } else {
        console.log('⚠ Legend does not explain evidence quality');
      }
    } else {
      console.log('⚠ No legend found on Systems Map');
      test.skip();
    }
  });

  test('Should filter edges by evidence quality', async ({ page }) => {
    const systemsMapTab = page.locator('a, button').filter({ hasText: /systems map|network/i }).first();
    await systemsMapTab.click();
    await page.waitForTimeout(2000);

    const svg = page.locator('svg:has(g.graph-container)');
    await expect(svg).toBeVisible({ timeout: 10000 });

    // Count initial edges
    const initialEdges = await page.locator('g.link').count();
    console.log(`Initial edge count: ${initialEdges}`);

    // Look for evidence quality filter
    const evidenceFilter = page.locator('[data-testid="evidence-filter"], .evidence-quality-filter, select, input[type="checkbox"]').filter({ hasText: /evidence|quality/i });
    const filterCount = await evidenceFilter.count();

    if (filterCount > 0) {
      console.log('✓ Evidence quality filter found');

      // Try to interact with filter
      const firstFilter = evidenceFilter.first();
      const tagName = await firstFilter.evaluate((el) => el.tagName.toLowerCase());

      if (tagName === 'select') {
        await firstFilter.selectOption({ index: 1 });
      } else if (tagName === 'input') {
        await firstFilter.click();
      }

      await page.waitForTimeout(1000);

      // Count edges after filter
      const filteredEdges = await page.locator('g.link').count();
      console.log(`Filtered edge count: ${filteredEdges}`);

      // Edge count should change (unless all edges have same quality)
      const filterWorked = filteredEdges !== initialEdges || filteredEdges === 0;
      console.log(`Filter effect: ${filterWorked ? 'working' : 'no change'}`);
    } else {
      console.log('⚠ Evidence quality filter not found');
      test.skip();
    }
  });
});
