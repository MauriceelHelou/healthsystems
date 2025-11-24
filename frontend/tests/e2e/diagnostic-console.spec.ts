import { test, expect } from '@playwright/test';

/**
 * Console diagnostic test to see what's happening
 */

test('capture console logs from systems-map', async ({ page }) => {
  const logs: string[] = [];
  const errors: string[] = [];
  const warnings: string[] = [];

  // Listen to console events
  page.on('console', msg => {
    const text = msg.text();
    logs.push(`[${msg.type()}] ${text}`);

    if (msg.type() === 'error') {
      errors.push(text);
    } else if (msg.type() === 'warning') {
      warnings.push(text);
    }
  });

  // Listen to page errors
  page.on('pageerror', error => {
    errors.push(`PAGE ERROR: ${error.message}`);
  });

  // Go to page (root path shows SystemsMapView)
  await page.goto('/');

  // Wait for rendering
  await page.waitForTimeout(3000);

  // Take screenshot
  await page.screenshot({
    path: 'test-results/diagnostic-console-screenshot.png',
    fullPage: true
  });

  // Print all logs
  console.log('\n========== CONSOLE LOGS ==========');
  logs.forEach(log => console.log(log));

  console.log('\n========== ERRORS ==========');
  errors.forEach(err => console.log(err));

  console.log('\n========== WARNINGS ==========');
  warnings.forEach(warn => console.log(warn));

  // Check for MechanismGraph logs
  const mechanismGraphLogs = logs.filter(log => log.includes('[MechanismGraph]'));
  console.log('\n========== MECHANISM GRAPH LOGS ==========');
  mechanismGraphLogs.forEach(log => console.log(log));

  // Get SVG info - find the graph SVG specifically (has .graph-container inside)
  const allSvgs = page.locator('svg');
  const svgCount = await allSvgs.count();
  console.log(`\nFound ${svgCount} total SVG elements`);

  // Find the graph SVG (should have g.graph-container)
  const svg = page.locator('svg:has(g.graph-container)');
  const svgExists = await svg.count() > 0;

  if (svgExists) {
    const width = await svg.getAttribute('width');
    const height = await svg.getAttribute('height');
    const innerHTML = await svg.innerHTML();

    console.log('\n========== SVG INFO ==========');
    console.log(`SVG dimensions: ${width} x ${height}`);
    console.log(`SVG innerHTML length: ${innerHTML.length} chars`);
    console.log(`SVG innerHTML preview: ${innerHTML.substring(0, 500)}...`);
  } else {
    console.log('\n========== SVG INFO ==========');
    console.log('NO SVG FOUND!');
  }

  expect(true).toBe(true);
});
