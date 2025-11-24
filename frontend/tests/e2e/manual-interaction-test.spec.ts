import { test, expect } from '@playwright/test';

/**
 * Manual Interaction Testing for Diagram Manipulation
 *
 * This test provides visibility into actual user interactions with the diagram:
 * - Zoom in/out
 * - Pan/drag
 * - Node hover/click
 * - Edge visibility
 * - Label readability
 */

test('Manual Diagram Interaction Test', async ({ page }) => {
  console.log('\n========== STARTING MANUAL INTERACTION TEST ==========\n');

  // Navigate to page
  await page.goto('/');

  // Wait for diagram to render
  const svg = page.locator('svg:has(g.graph-container)');
  await expect(svg).toBeVisible({ timeout: 10000 });

  console.log('✓ Diagram loaded');

  // Get initial transform state
  const initialTransform = await svg.evaluate((el) => {
    const g = el.querySelector('g.graph-container');
    return g?.getAttribute('transform') || '';
  });
  console.log(`Initial transform: ${initialTransform}`);

  // Count nodes
  const nodeCount = await page.locator('circle, rect[data-node-id]').count();
  console.log(`✓ Found ${nodeCount} nodes`);

  // Count edges
  const edgeCount = await page.locator('g.link path, g.links path').count();
  console.log(`✓ Found ${edgeCount} edges`);

  // Count labels
  const labelCount = await page.locator('text').count();
  console.log(`✓ Found ${labelCount} text labels`);

  console.log('\n--- Testing ZOOM functionality ---');

  // Get SVG bounding box
  const box = await svg.boundingBox();
  if (box) {
    // Move mouse to center of SVG
    await page.mouse.move(box.x + box.width / 2, box.y + box.height / 2);

    // Zoom IN (wheel down, negative delta)
    await page.mouse.wheel(0, -300);
    await page.waitForTimeout(500);

    const zoomedInTransform = await svg.evaluate((el) => {
      const g = el.querySelector('g.graph-container');
      return g?.getAttribute('transform') || '';
    });
    console.log(`After zoom IN: ${zoomedInTransform}`);

    // Check if transform changed
    if (zoomedInTransform !== initialTransform) {
      console.log('✓ Zoom IN works - transform changed');
    } else {
      console.log('✗ ISSUE: Zoom IN did not change transform');
    }

    // Zoom OUT (wheel up, positive delta)
    await page.mouse.wheel(0, 300);
    await page.waitForTimeout(500);

    const zoomedOutTransform = await svg.evaluate((el) => {
      const g = el.querySelector('g.graph-container');
      return g?.getAttribute('transform') || '';
    });
    console.log(`After zoom OUT: ${zoomedOutTransform}`);

    if (zoomedOutTransform !== zoomedInTransform) {
      console.log('✓ Zoom OUT works - transform changed');
    } else {
      console.log('✗ ISSUE: Zoom OUT did not change transform');
    }
  }

  console.log('\n--- Testing PAN functionality ---');

  // Reset to center
  await svg.hover();
  const beforePanTransform = await svg.evaluate((el) => {
    const g = el.querySelector('g.graph-container');
    return g?.getAttribute('transform') || '';
  });

  if (box) {
    // Pan by dragging
    const startX = box.x + box.width / 2;
    const startY = box.y + box.height / 2;
    const endX = startX + 100;
    const endY = startY + 100;

    await page.mouse.move(startX, startY);
    await page.mouse.down();
    await page.mouse.move(endX, endY);
    await page.mouse.up();
    await page.waitForTimeout(500);

    const afterPanTransform = await svg.evaluate((el) => {
      const g = el.querySelector('g.graph-container');
      return g?.getAttribute('transform') || '';
    });
    console.log(`After PAN: ${afterPanTransform}`);

    if (afterPanTransform !== beforePanTransform) {
      console.log('✓ Pan works - transform changed');
    } else {
      console.log('✗ ISSUE: Pan did not change transform');
    }
  }

  console.log('\n--- Testing NODE interactions ---');

  // Find first visible node
  const firstNode = page.locator('circle, rect[data-node-id]').first();

  // Test hover
  const nodeId = await firstNode.getAttribute('data-node-id').catch(() => null);
  console.log(`Testing node: ${nodeId || 'unknown'}`);

  const beforeHoverOpacity = await firstNode.evaluate((el) =>
    window.getComputedStyle(el).opacity
  );

  await firstNode.hover();
  await page.waitForTimeout(300);

  const afterHoverOpacity = await firstNode.evaluate((el) =>
    window.getComputedStyle(el).opacity
  );

  console.log(`Opacity before hover: ${beforeHoverOpacity}, after: ${afterHoverOpacity}`);

  if (beforeHoverOpacity !== afterHoverOpacity) {
    console.log('✓ Node hover effect works');
  } else {
    console.log('⚠ Node hover may not have visual feedback (opacity unchanged)');
  }

  // Test click
  await firstNode.click();
  await page.waitForTimeout(500);

  const hasSelection = await firstNode.evaluate((el) => {
    return (
      el.classList.contains('selected') ||
      el.getAttribute('stroke-width') !== null ||
      parseFloat(el.getAttribute('stroke-width') || '0') > 0
    );
  });

  if (hasSelection) {
    console.log('✓ Node click selection works');
  } else {
    console.log('⚠ Node click may not show selection (no selected class or stroke-width)');
  }

  console.log('\n--- Testing EDGE visibility ---');

  const firstEdge = page.locator('g.link path, g.links path').first();
  const edgeVisible = await firstEdge.isVisible();

  if (edgeVisible) {
    const edgeStyle = await firstEdge.evaluate((el) => {
      const computed = window.getComputedStyle(el);
      return {
        stroke: computed.stroke,
        strokeWidth: computed.strokeWidth,
        opacity: computed.opacity
      };
    });
    console.log(`✓ Edges visible with style:`, edgeStyle);
  } else {
    console.log('✗ ISSUE: Edges not visible');
  }

  console.log('\n--- Testing LABEL readability ---');

  const firstLabel = page.locator('text').first();
  const labelText = await firstLabel.textContent();
  const labelStyle = await firstLabel.evaluate((el) => {
    const computed = window.getComputedStyle(el);
    return {
      fontSize: computed.fontSize,
      fill: computed.fill,
      fontFamily: computed.fontFamily
    };
  });

  console.log(`✓ Label text: "${labelText}"`);
  console.log(`Label style:`, labelStyle);

  console.log('\n--- Taking screenshot for manual review ---');
  await page.screenshot({
    path: 'test-results/manual-interaction-screenshot.png',
    fullPage: true
  });
  console.log('✓ Screenshot saved to test-results/manual-interaction-screenshot.png');

  console.log('\n========== INTERACTION TEST COMPLETE ==========\n');

  expect(true).toBe(true);
});
