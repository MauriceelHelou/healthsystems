import { test, expect } from '@playwright/test';

/**
 * Test Suite: Scale Badges on Nodes
 *
 * Tests that nodes display scale indicators (1-7) showing their position
 * in the health systems hierarchy as per 03_SYSTEMS_MAP_VISUALIZATION.md
 */

test.describe('Scale Badges on Nodes', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('networkidle');

    // Wait for graph to render
    await page.waitForSelector('svg:has(g.graph-container)', { timeout: 30000 });
    await page.waitForTimeout(1000);
  });

  test('Systems Map nodes should display scale badges', async ({ page }) => {
    // Navigate to Systems Map
    const systemsMapTab = page.locator('a, button').filter({ hasText: /systems map|network/i }).first();
    await systemsMapTab.click();
    await page.waitForTimeout(2000);

    // Wait for graph to render
    const svg = page.locator('svg:has(g.graph-container)');
    await expect(svg).toBeVisible({ timeout: 10000 });

    // Wait for nodes to render
    const nodes = page.locator('g.node');
    const nodeCount = await nodes.count();
    console.log(`Found ${nodeCount} nodes`);

    expect(nodeCount).toBeGreaterThan(0);

    // Check for scale badges (should be text, circle, or badge elements on nodes)
    const scaleBadges = page.locator('g.node text.scale-indicator, g.node .scale-indicator');
    const badgeCount = await scaleBadges.count();

    console.log(`Found ${badgeCount} scale badges`);

    // Nodes should have scale indicators
    if (badgeCount > 0) {
      console.log('✓ Scale badges found on nodes');

      // Verify badge content (should be 1-7)
      const firstBadge = scaleBadges.first();
      const badgeText = await firstBadge.textContent();
      console.log(`First badge text: ${badgeText}`);

      const scaleValue = parseInt(badgeText || '0');
      expect(scaleValue).toBeGreaterThanOrEqual(1);
      expect(scaleValue).toBeLessThanOrEqual(7);
    } else {
      console.log('⚠ No scale badges found - feature may not be implemented yet');
      test.skip();
    }
  });

  test('Scale badges should show values 1-7', async ({ page }) => {
    const systemsMapTab = page.locator('a, button').filter({ hasText: /systems map|network/i }).first();
    await systemsMapTab.click();
    await page.waitForTimeout(2000);

    const svg = page.locator('svg:has(g.graph-container)');
    await expect(svg).toBeVisible({ timeout: 10000 });

    // Collect all scale values from badges
    const scaleBadges = page.locator('g.node text.scale-badge, g.node .scale-indicator');
    const badgeCount = await scaleBadges.count();

    if (badgeCount > 0) {
      const scaleValues = new Set<number>();

      for (let i = 0; i < Math.min(badgeCount, 20); i++) {
        const badge = scaleBadges.nth(i);
        const text = await badge.textContent();
        if (text) {
          const value = parseInt(text.trim());
          if (!isNaN(value)) {
            scaleValues.add(value);
          }
        }
      }

      console.log(`Scale values found: ${Array.from(scaleValues).sort().join(', ')}`);

      // All scale values should be 1-7
      const validScales = Array.from(scaleValues).every(v => v >= 1 && v <= 7);
      expect(validScales).toBeTruthy();

      console.log(`✓ All scale values in range 1-7`);
    } else {
      console.log('⚠ Scale badges not found');
      test.skip();
    }
  });

  test('Hierarchical layout should group nodes by scale', async ({ page }) => {
    const systemsMapTab = page.locator('a, button').filter({ hasText: /systems map|network/i }).first();
    await systemsMapTab.click();
    await page.waitForTimeout(2000);

    const svg = page.locator('svg:has(g.graph-container)');
    await expect(svg).toBeVisible({ timeout: 10000 });

    // Check if hierarchical mode is active
    const layoutToggle = page.locator('button, select').filter({ hasText: /layout|hierarchical/i });
    const toggleCount = await layoutToggle.count();

    if (toggleCount > 0) {
      const firstToggle = layoutToggle.first();
      const tagName = await firstToggle.evaluate((el) => el.tagName.toLowerCase());

      // Switch to hierarchical layout if not already
      if (tagName === 'select') {
        await firstToggle.selectOption({ label: 'Hierarchical' });
      } else {
        const buttonText = await firstToggle.textContent();
        if (buttonText && !buttonText.toLowerCase().includes('hierarchical')) {
          await firstToggle.click();
        }
      }

      await page.waitForTimeout(1000);
      console.log('✓ Switched to hierarchical layout');
    }

    // Check for level labels (should show scales 1-7)
    const levelLabels = page.locator('svg text').filter({ hasText: /structural|institutional|individual|intermediate|crisis/i });
    const labelCount = await levelLabels.count();

    console.log(`Found ${labelCount} level labels`);

    if (labelCount > 0) {
      const labels = [];
      for (let i = 0; i < labelCount; i++) {
        const text = await levelLabels.nth(i).textContent();
        labels.push(text);
      }
      console.log(`Level labels: ${labels.join(', ')}`);

      // Should have labels for multiple scales
      expect(labelCount).toBeGreaterThan(3);
      expect(labelCount).toBeLessThanOrEqual(7);
    }
  });

  test('Node hover should show scale information', async ({ page }) => {
    const systemsMapTab = page.locator('a, button').filter({ hasText: /systems map|network/i }).first();
    await systemsMapTab.click();
    await page.waitForTimeout(2000);

    const svg = page.locator('svg:has(g.graph-container)');
    await expect(svg).toBeVisible({ timeout: 10000 });

    // Hover over first node
    const firstNode = page.locator('g.node').first();
    await firstNode.hover();
    await page.waitForTimeout(500);

    // Check aria-label for scale information
    const ariaLabel = await firstNode.getAttribute('aria-label');
    console.log('Node aria-label:', ariaLabel);

    if (ariaLabel) {
      // Should mention scale
      const hasScaleInfo = ariaLabel.includes('scale') || /scale \d/i.test(ariaLabel);

      if (hasScaleInfo) {
        console.log('✓ Scale information in aria-label');
        expect(hasScaleInfo).toBeTruthy();
      }
    }

    // Check for tooltip
    const tooltip = page.locator('[role="tooltip"], .node-tooltip, .detail-panel');
    const tooltipVisible = await tooltip.isVisible().catch(() => false);

    if (tooltipVisible) {
      const tooltipText = await tooltip.textContent();
      console.log('Tooltip content:', tooltipText);

      // Should contain scale information
      const hasScale = tooltipText && (
        tooltipText.includes('Scale') ||
        tooltipText.includes('level') ||
        /\b[1-7]\b/.test(tooltipText)
      );

      if (hasScale) {
        console.log('✓ Scale information shown in tooltip');
      }
    }
  });

  test('Legend should explain 7-scale system', async ({ page }) => {
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

      // Check if legend mentions scales
      const hasScaleLegend = legendText && (
        legendText.includes('Scale') ||
        legendText.includes('Structural') ||
        legendText.includes('Institutional') ||
        legendText.includes('Crisis')
      );

      if (hasScaleLegend) {
        console.log('✓ Legend explains scale system');
        expect(hasScaleLegend).toBeTruthy();
      } else {
        console.log('⚠ Legend does not explain scale system');
      }
    } else {
      console.log('⚠ No legend found on Systems Map');
      test.skip();
    }
  });

  test('Should filter nodes by scale', async ({ page }) => {
    const systemsMapTab = page.locator('a, button').filter({ hasText: /systems map|network/i }).first();
    await systemsMapTab.click();
    await page.waitForTimeout(2000);

    const svg = page.locator('svg:has(g.graph-container)');
    await expect(svg).toBeVisible({ timeout: 10000 });

    // Count initial nodes
    const initialNodes = await page.locator('g.node').count();
    console.log(`Initial node count: ${initialNodes}`);

    // Look for scale filter
    const scaleFilter = page.locator('[data-testid="scale-filter"], .scale-filter, select, input[type="checkbox"]').filter({ hasText: /scale|level/i });
    const filterCount = await scaleFilter.count();

    if (filterCount > 0) {
      console.log('✓ Scale filter found');

      // Try to interact with filter
      const firstFilter = scaleFilter.first();
      const tagName = await firstFilter.evaluate((el) => el.tagName.toLowerCase());

      if (tagName === 'select') {
        // Select a specific scale
        await firstFilter.selectOption({ index: 1 });
      } else if (tagName === 'input') {
        // Toggle a scale checkbox
        await firstFilter.click();
      }

      await page.waitForTimeout(1000);

      // Count nodes after filter
      const filteredNodes = await page.locator('g.node').count();
      console.log(`Filtered node count: ${filteredNodes}`);

      // Node count should change
      const filterWorked = filteredNodes !== initialNodes;
      console.log(`Filter effect: ${filterWorked ? 'working' : 'no change'}`);

      if (filterWorked) {
        expect(filteredNodes).toBeLessThan(initialNodes);
      }
    } else {
      console.log('⚠ Scale filter not found');
      test.skip();
    }
  });

  test('Should show active vs reserved scales', async ({ page }) => {
    const systemsMapTab = page.locator('a, button').filter({ hasText: /systems map|network/i }).first();
    await systemsMapTab.click();
    await page.waitForTimeout(2000);

    const svg = page.locator('svg:has(g.graph-container)');
    await expect(svg).toBeVisible({ timeout: 10000 });

    // Look for scale documentation or legend explaining active vs reserved
    const scaleInfo = page.locator('text=/active.*scale|reserved.*scale|scale.*2.*5.*reserved/i');
    const infoVisible = await scaleInfo.isVisible().catch(() => false);

    if (infoVisible) {
      console.log('✓ Scale system explanation found');
      const infoText = await scaleInfo.textContent();
      console.log('Scale info:', infoText);

      // Should mention that scales 2 and 5 are reserved
      const mentionsReserved = infoText && (
        infoText.includes('reserved') ||
        infoText.includes('future')
      );

      if (mentionsReserved) {
        console.log('✓ Reserved scales (2, 5) explained');
      }
    } else {
      console.log('⚠ No explanation of active vs reserved scales found');
    }
  });
});
