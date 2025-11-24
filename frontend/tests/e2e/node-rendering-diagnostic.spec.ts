import { test, expect } from '@playwright/test';

/**
 * Diagnostic test to understand why nodes aren't visible
 */

test('Node Rendering Diagnostic', async ({ page }) => {
  console.log('\n========== NODE RENDERING DIAGNOSTIC ==========\n');

  await page.goto('/');
  await page.waitForTimeout(3000);

  // Check if SVG exists
  const svg = page.locator('svg:has(g.graph-container)');
  await expect(svg).toBeVisible({ timeout: 10000 });
  console.log('✓ SVG with graph-container found');

  // Check node groups
  const nodeGroups = page.locator('g.nodes');
  const nodeGroupCount = await nodeGroups.count();
  console.log(`Found ${nodeGroupCount} g.nodes groups`);

  // Check individual node elements
  const nodes = page.locator('g.node');
  const nodeCount = await nodes.count();
  console.log(`Found ${nodeCount} g.node elements`);

  // Check rectangles inside nodes
  const nodeRects = page.locator('g.node rect:not(.node-glow)');
  const nodeRectCount = await nodeRects.count();
  console.log(`Found ${nodeRectCount} rect elements inside g.node`);

  // Check node-glow rectangles
  const glowRects = page.locator('g.node rect.node-glow');
  const glowCount = await glowRects.count();
  console.log(`Found ${glowCount} node-glow rects`);

  if (nodeRectCount > 0) {
    // Get first node rect details
    const firstRect = nodeRects.first();
    const rectAttrs = await firstRect.evaluate((el) => {
      const computed = window.getComputedStyle(el);
      return {
        x: el.getAttribute('x'),
        y: el.getAttribute('y'),
        width: el.getAttribute('width'),
        height: el.getAttribute('height'),
        fill: el.getAttribute('fill'),
        stroke: el.getAttribute('stroke'),
        strokeWidth: el.getAttribute('stroke-width'),
        opacity: el.getAttribute('opacity'),
        computedDisplay: computed.display,
        computedVisibility: computed.visibility,
        computedOpacity: computed.opacity,
        computedFill: computed.fill,
        computedStroke: computed.stroke
      };
    });
    console.log('\nFirst node rect attributes:', JSON.stringify(rectAttrs, null, 2));

    // Check bounding box
    const bbox = await firstRect.boundingBox();
    console.log('First rect bounding box:', bbox);
  }

  // Check text labels
  const textLabels = page.locator('g.node-text text');
  const textCount = await textLabels.count();
  console.log(`\nFound ${textCount} text labels inside g.node-text`);

  if (textCount > 0) {
    const firstText = textLabels.first();
    // @ts-expect-error - stored for potential future use
    const _textContent = await firstText.textContent();
    const textAttrs = await firstText.evaluate((el) => {
      const computed = window.getComputedStyle(el);
      return {
        content: el.textContent,
        x: el.getAttribute('x'),
        y: el.getAttribute('y'),
        fontSize: el.getAttribute('font-size'),
        fill: el.getAttribute('fill'),
        computedFontSize: computed.fontSize,
        computedFill: computed.fill
      };
    });
    console.log('\nFirst text label:', JSON.stringify(textAttrs, null, 2));
  }

  // Check edges
  const edges = page.locator('g.links path, g.link path');
  const edgeCount = await edges.count();
  console.log(`\nFound ${edgeCount} edge paths`);

  if (edgeCount > 0) {
    const firstEdge = edges.first();
    const edgeAttrs = await firstEdge.evaluate((el) => {
      const computed = window.getComputedStyle(el);
      return {
        d: el.getAttribute('d')?.substring(0, 100) + '...',
        stroke: el.getAttribute('stroke'),
        strokeWidth: el.getAttribute('stroke-width'),
        fill: el.getAttribute('fill'),
        opacity: el.getAttribute('opacity'),
        computedStroke: computed.stroke,
        computedStrokeWidth: computed.strokeWidth,
        computedOpacity: computed.opacity,
        computedDisplay: computed.display,
        computedVisibility: computed.visibility
      };
    });
    console.log('\nFirst edge attributes:', JSON.stringify(edgeAttrs, null, 2));
  }

  // Take screenshot
  await page.screenshot({
    path: 'test-results/node-rendering-diagnostic.png',
    fullPage: true
  });
  console.log('\n✓ Screenshot saved');

  console.log('\n========== DIAGNOSTIC COMPLETE ==========\n');

  expect(true).toBe(true);
});
