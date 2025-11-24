import { test, expect } from '@playwright/test';

/**
 * Diagnostic test for force-directed layout issues
 */

test('Force-Directed Layout Diagnostic', async ({ page }) => {
  console.log('\n========== FORCE-DIRECTED LAYOUT DIAGNOSTIC ==========\n');

  // Enable console logging
  page.on('console', msg => {
    const type = msg.type();
    if (type === 'error' || type === 'warning') {
      console.log(`[${type}] ${msg.text()}`);
    }
  });

  // Capture page errors
  page.on('pageerror', error => {
    console.log(`[PAGE ERROR] ${error.message}`);
  });

  await page.goto('/');
  await page.waitForTimeout(2000);

  // Wait for diagram to load in hierarchical mode first
  const svg = page.locator('svg:has(g.graph-container)');
  await expect(svg).toBeVisible({ timeout: 10000 });
  console.log('✓ Diagram loaded in hierarchical mode');

  // Take screenshot of hierarchical layout
  await page.screenshot({
    path: 'test-results/force-directed-before.png',
    fullPage: true
  });

  // Find and click the "Force-Directed" button
  const forceDirectedButton = page.locator('button:has-text("Force-Directed")');
  const buttonExists = await forceDirectedButton.count();

  if (buttonExists === 0) {
    console.log('✗ Force-Directed button not found');
    expect(buttonExists).toBeGreaterThan(0);
    return;
  }

  console.log('✓ Found Force-Directed button');

  // Click to switch to force-directed mode
  await forceDirectedButton.click();
  console.log('✓ Clicked Force-Directed button');

  // Wait for layout transition
  await page.waitForTimeout(3000);

  // Check for errors in console
  console.log('\n--- Checking for JavaScript errors ---');

  // Verify nodes are still visible
  const nodeGroups = page.locator('g.node');
  const nodeCount = await nodeGroups.count();
  console.log(`Nodes in force-directed mode: ${nodeCount}`);

  if (nodeCount === 0) {
    console.log('✗ No nodes visible in force-directed mode!');
  } else {
    console.log('✓ Nodes still rendering');
  }

  // Check edges
  const edges = page.locator('g.link');
  const edgeCount = await edges.count();
  console.log(`Edges in force-directed mode: ${edgeCount}`);

  // Check if nodes have positions (fx, fy attributes)
  if (nodeCount > 0) {
    const firstNode = nodeGroups.first();
    const transform = await firstNode.getAttribute('transform');
    console.log(`First node transform: ${transform}`);
  }

  // Take screenshot of force-directed layout
  await page.screenshot({
    path: 'test-results/force-directed-after.png',
    fullPage: true
  });
  console.log('✓ Screenshots saved');

  // Try interactions
  console.log('\n--- Testing force-directed interactions ---');

  // Test node drag
  if (nodeCount > 0) {
    const firstNode = nodeGroups.first();
    const box = await firstNode.boundingBox();

    if (box) {
      console.log('Attempting to drag node...');
      await page.mouse.move(box.x + box.width / 2, box.y + box.height / 2);
      await page.mouse.down();
      await page.mouse.move(box.x + box.width / 2 + 100, box.y + box.height / 2 + 50);
      await page.mouse.up();
      await page.waitForTimeout(500);
      console.log('✓ Drag attempted');

      // Take screenshot after drag
      await page.screenshot({
        path: 'test-results/force-directed-after-drag.png',
        fullPage: true
      });
    }
  }

  // Test physics settings adjustment
  console.log('\n--- Testing physics settings ---');
  const physicsDetailsToggle = page.locator('details summary:has-text("Physics Settings")');
  const physicsExists = await physicsDetailsToggle.count();

  if (physicsExists > 0) {
    await physicsDetailsToggle.click();
    await page.waitForTimeout(500);
    console.log('✓ Physics settings panel opened');

    // Try adjusting repulsion slider
    const repulsionSlider = page.locator('input[type="range"]').first();
    if (await repulsionSlider.count() > 0) {
      await repulsionSlider.fill('-500');
      await page.waitForTimeout(1000);
      console.log('✓ Adjusted repulsion setting');

      await page.screenshot({
        path: 'test-results/force-directed-physics-adjusted.png',
        fullPage: true
      });
    }
  } else {
    console.log('✗ Physics settings not available');
  }

  // Switch back to hierarchical to compare
  console.log('\n--- Switching back to hierarchical ---');
  const hierarchicalButton = page.locator('button:has-text("Hierarchical")');
  if (await hierarchicalButton.count() > 0) {
    await hierarchicalButton.click();
    await page.waitForTimeout(2000);
    console.log('✓ Switched back to hierarchical');

    const nodesAfterSwitch = await nodeGroups.count();
    console.log(`Nodes after switching back: ${nodesAfterSwitch}`);
  }

  console.log('\n========== DIAGNOSTIC COMPLETE ==========\n');

  expect(true).toBe(true);
});
