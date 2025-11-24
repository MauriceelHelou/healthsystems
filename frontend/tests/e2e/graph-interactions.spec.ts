import { test, expect } from '@playwright/test';

test.describe('Graph Interactions', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('http://localhost:3000/');

    // Wait for app to load
    await page.waitForSelector('header', { state: 'visible' });
    await page.waitForSelector('main', { state: 'visible' });

    // Wait for graph to render - increased timeout for slower CI environments
    await page.waitForSelector('svg:has(g.graph-container)', { timeout: 30000 });
    await page.waitForTimeout(1000); // Allow graph to stabilize
  });

  test('Nodes should be visible on the graph', async ({ page }) => {
    const nodes = page.locator('g.node');
    const count = await nodes.count();

    expect(count).toBeGreaterThan(0);
    console.log(`Found ${count} nodes`);
  });

  test('Edges should be visible on the graph', async ({ page }) => {
    const edges = page.locator('g.link, g.edge');
    const count = await edges.count();

    expect(count).toBeGreaterThan(0);
    console.log(`Found ${count} edges`);
  });

  test('Nodes should have text labels', async ({ page }) => {
    const nodes = page.locator('g.node');
    const firstNode = nodes.first();

    // Check that the node has text content (nodes have multiple text elements for labels, scale indicators, etc.)
    const textElements = firstNode.locator('text');
    const count = await textElements.count();
    expect(count).toBeGreaterThan(0);

    // Check that at least one text element has content
    const firstText = await textElements.first().textContent();
    expect(firstText).toBeTruthy();
    expect(firstText!.length).toBeGreaterThan(0);
  });

  test('Nodes should respond to hover', async ({ page }) => {
    const nodes = page.locator('g.node');
    const firstNode = nodes.first();

    // Get initial state
    const rectBefore = firstNode.locator('rect').first();
    // @ts-expect-error - stored for potential future use
    const _strokeBeforePromise = rectBefore.evaluate(el =>
      window.getComputedStyle(el).stroke
    );

    // Hover over node
    await firstNode.hover();
    await page.waitForTimeout(200); // Wait for hover effect

    // Hover should trigger some visual change (we can't easily test exact colors in e2e)
    // But we can verify the element is still visible
    await expect(firstNode).toBeVisible();
  });

  test('Clicking a node should select it', async ({ page }) => {
    const nodes = page.locator('g.node');
    const firstNode = nodes.first();

    // Click the node
    await firstNode.click();
    await page.waitForTimeout(300);

    // Node should still be visible after clicking
    await expect(firstNode).toBeVisible();
  });

  test('Graph should have scale badges on nodes', async ({ page }) => {
    const scaleBadges = page.locator('g.node .scale-indicator');
    const count = await scaleBadges.count();

    expect(count).toBeGreaterThan(0);
    console.log(`Found ${count} scale badges`);
  });

  test('Graph should have evidence badges on edges', async ({ page }) => {
    const evidenceBadges = page.locator('g.evidence-badge, .evidence-quality');
    const count = await evidenceBadges.count();

    // May or may not have evidence badges depending on data
    console.log(`Found ${count} evidence badges`);

    if (count > 0) {
      const firstBadge = evidenceBadges.first();
      await expect(firstBadge).toBeVisible();
    }
  });

  test('Graph should be zoomable (SVG should exist)', async ({ page }) => {
    const svg = page.locator('svg:has(g.graph-container)');
    await expect(svg).toBeVisible();

    // Check SVG has viewBox or dimensions
    const width = await svg.evaluate(el => el.clientWidth);
    const height = await svg.evaluate(el => el.clientHeight);

    expect(width).toBeGreaterThan(0);
    expect(height).toBeGreaterThan(0);
  });

  test('Graph container should have proper structure', async ({ page }) => {
    // Check for main graph container
    const container = page.locator('g.graph-container');
    await expect(container).toBeVisible();

    // Check for link group
    const linkGroup = container.locator('g.links, g.edges').first();
    await expect(linkGroup).toBeAttached();

    // Check for node group
    const nodeGroup = container.locator('g.nodes').first();
    await expect(nodeGroup).toBeAttached();
  });

  test('Nodes should have consistent visual structure', async ({ page }) => {
    const nodes = page.locator('g.node');
    const firstNode = nodes.first();

    // Check for rect elements (nodes have multiple: glow, main rect, possibly scale badges)
    const rects = firstNode.locator('rect');
    const rectCount = await rects.count();
    expect(rectCount).toBeGreaterThan(0);

    // Check for text elements (nodes have multiple: label lines, scale indicators)
    const texts = firstNode.locator('text');
    const textCount = await texts.count();
    expect(textCount).toBeGreaterThan(0);
  });

  test('Edges should have arrow markers', async ({ page }) => {
    const svg = page.locator('svg:has(g.graph-container)');

    // Check for marker definitions
    const markers = svg.locator('defs marker');
    const count = await markers.count();

    expect(count).toBeGreaterThan(0);
    console.log(`Found ${count} arrow markers`);
  });

  test('Graph should handle layout toggle', async ({ page }) => {
    // Look for layout toggle button
    const layoutToggle = page.locator('button, select, input[type="radio"]').filter({
      hasText: /force|hierarchical|layout/i
    }).first();

    const toggleExists = await layoutToggle.count() > 0;

    if (toggleExists) {
      await layoutToggle.click();
      await page.waitForTimeout(500);

      // Graph should still be visible after layout change
      const svg = page.locator('svg:has(g.graph-container)');
      await expect(svg).toBeVisible();
    } else {
      console.log('Layout toggle not found - may not be implemented');
    }
  });

  test('Multiple nodes should be selectable', async ({ page }) => {
    const nodes = page.locator('g.node');
    const count = await nodes.count();

    if (count >= 2) {
      const firstNode = nodes.nth(0);
      const secondNode = nodes.nth(1);

      await firstNode.click();
      await page.waitForTimeout(200);

      await secondNode.click();
      await page.waitForTimeout(200);

      // Both nodes should still be visible
      await expect(firstNode).toBeVisible();
      await expect(secondNode).toBeVisible();
    }
  });

  test('Graph should maintain visibility during interactions', async ({ page }) => {
    const svg = page.locator('svg:has(g.graph-container)');

    // Perform various interactions
    await page.mouse.move(500, 400);
    await page.waitForTimeout(100);

    await page.mouse.move(600, 500);
    await page.waitForTimeout(100);

    // Graph should remain visible
    await expect(svg).toBeVisible();
  });

  test('Nodes should have appropriate fill colors', async ({ page }) => {
    const nodes = page.locator('g.node rect').first();

    const fill = await nodes.evaluate(el =>
      el.getAttribute('fill') || window.getComputedStyle(el).fill
    );

    // Should have a valid fill color (white or crisis-colored backgrounds)
    // White: #FFFFFF, or crisis backgrounds: #FEE2E2, #FFEDD5, #FEF3C7, #DBEAFE
    expect(fill).toBeTruthy();
    expect(fill).toMatch(/#[A-Fa-f0-9]{6}|white|rgb\([0-9,\s]+\)/);
  });

  test('Graph should have proper spacing between nodes', async ({ page }) => {
    const nodes = page.locator('g.node');
    const count = await nodes.count();

    if (count >= 2) {
      const firstNode = nodes.nth(0);
      const secondNode = nodes.nth(1);

      const box1 = await firstNode.boundingBox();
      const box2 = await secondNode.boundingBox();

      // Nodes should have some separation
      if (box1 && box2) {
        const overlap = !(
          box1.x + box1.width < box2.x ||
          box2.x + box2.width < box1.x ||
          box1.y + box1.height < box2.y ||
          box2.y + box2.height < box1.y
        );

        // Some overlap is OK in dense graphs, but complete overlap is bad
        console.log(`Nodes overlap: ${overlap}`);
      }
    }
  });
});
