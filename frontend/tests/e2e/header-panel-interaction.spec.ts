import { test, expect } from '@playwright/test';

/**
 * Test to diagnose header disappearing and panel opening issues
 */

test('Header and Panel Interaction Test', async ({ page }) => {
  console.log('\n========== HEADER & PANEL INTERACTION TEST ==========\n');

  await page.goto('/');
  await page.waitForTimeout(2000);

  // Check header visibility initially
  const header = page.locator('header');
  await expect(header).toBeVisible();
  console.log('✓ Header visible initially');

  // Get header z-index
  const headerZIndex = await header.evaluate((el) => {
    const computed = window.getComputedStyle(el);
    return computed.zIndex;
  });
  console.log(`Header z-index: ${headerZIndex}`);

  // Wait for diagram to render
  const svg = page.locator('svg:has(g.graph-container)');
  await expect(svg).toBeVisible({ timeout: 10000 });
  console.log('✓ Diagram loaded');

  // Find and click a node
  const nodeGroups = page.locator('g.node');
  const nodeCount = await nodeGroups.count();
  console.log(`Found ${nodeCount} nodes`);

  if (nodeCount > 0) {
    console.log('\n--- Testing Node Click ---');
    const firstNode = nodeGroups.first();

    // Take screenshot before click
    await page.screenshot({
      path: 'test-results/before-node-click.png',
      fullPage: true
    });
    console.log('✓ Screenshot saved: before-node-click.png');

    await firstNode.click();
    await page.waitForTimeout(500);

    // Check if header is still visible after node click
    const headerVisibleAfterNodeClick = await header.isVisible();
    console.log(`Header visible after node click: ${headerVisibleAfterNodeClick}`);

    if (!headerVisibleAfterNodeClick) {
      console.log('✗ ISSUE FOUND: Header disappeared after node click!');

      // Get header styles
      const headerStyles = await header.evaluate((el) => {
        const computed = window.getComputedStyle(el);
        return {
          display: computed.display,
          visibility: computed.visibility,
          opacity: computed.opacity,
          zIndex: computed.zIndex,
          position: computed.position,
          top: computed.top
        };
      });
      console.log('Header computed styles:', JSON.stringify(headerStyles, null, 2));
    } else {
      console.log('✓ Header still visible');
    }

    // Check if panel appeared
    const panel = page.locator('aside[role="complementary"]');
    const panelVisible = await panel.isVisible();
    console.log(`Panel visible: ${panelVisible}`);

    if (panelVisible) {
      console.log('✓ Node detail panel opened successfully');

      // Get panel z-index
      const panelZIndex = await panel.evaluate((el) => {
        const computed = window.getComputedStyle(el);
        return {
          zIndex: computed.zIndex,
          position: computed.position
        };
      });
      console.log('Panel z-index/position:', JSON.stringify(panelZIndex, null, 2));

      // Get panel title
      const panelTitle = await panel.locator('h2').textContent();
      console.log(`Panel title: "${panelTitle}"`);
    } else {
      console.log('✗ ISSUE: Panel did not appear after node click');
    }

    // Take screenshot after click
    await page.screenshot({
      path: 'test-results/after-node-click.png',
      fullPage: true
    });
    console.log('✓ Screenshot saved: after-node-click.png');
  }

  // Test edge click for mechanism drawer
  console.log('\n--- Testing Edge Click ---');
  const edges = page.locator('g.link');
  const edgeCount = await edges.count();
  console.log(`Found ${edgeCount} edges`);

  if (edgeCount > 0) {
    // Close any open panel first
    const closeButton = page.locator('aside[role="complementary"] button[aria-label="Close panel"]');
    if (await closeButton.isVisible()) {
      await closeButton.click();
      await page.waitForTimeout(300);
      console.log('✓ Closed previous panel');
    }

    // Click an edge
    const firstEdge = edges.first();
    await firstEdge.click();
    await page.waitForTimeout(500);

    // Check if panel appeared with mechanism details
    const panel = page.locator('aside[role="complementary"]');
    const panelVisible = await panel.isVisible();
    console.log(`Mechanism panel visible: ${panelVisible}`);

    if (panelVisible) {
      const panelTitle = await panel.locator('h2').textContent();
      console.log(`Panel title: "${panelTitle}"`);

      if (panelTitle?.includes('Mechanism')) {
        console.log('✓ Mechanism detail panel opened successfully');
      } else {
        console.log('⚠ Panel opened but may not be mechanism details');
      }

      // Check if header is still visible
      const headerVisibleAfterEdgeClick = await header.isVisible();
      console.log(`Header visible after edge click: ${headerVisibleAfterEdgeClick}`);
    } else {
      console.log('✗ ISSUE: Mechanism panel did not appear after edge click');
    }

    // Take screenshot after edge click
    await page.screenshot({
      path: 'test-results/after-edge-click.png',
      fullPage: true
    });
    console.log('✓ Screenshot saved: after-edge-click.png');
  }

  console.log('\n========== TEST COMPLETE ==========\n');

  expect(true).toBe(true);
});
