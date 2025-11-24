import { test, expect } from '@playwright/test';

/**
 * Debug test for Crisis Explorer
 *
 * This test will help identify why visualization doesn't render
 */

test.describe('Crisis Explorer Debug', () => {
  test('Debug visualization rendering', async ({ page }) => {
    // Enable console logging
    page.on('console', msg => console.log('BROWSER:', msg.text()));
    page.on('pageerror', error => console.log('PAGE ERROR:', error.message));

    await page.goto('/');
    await page.waitForLoadState('networkidle');

    // Navigate to Crisis Explorer
    const crisisTab = page.locator('a, button').filter({ hasText: /crisis/i });
    await crisisTab.click();
    await page.waitForTimeout(2000);

    console.log('\n=== STEP 1: Page loaded ===');

    // Wait for crisis endpoints
    await page.waitForTimeout(3000);
    const checkboxes = page.locator('input[type="checkbox"]');
    const count = await checkboxes.count();
    console.log(`Found ${count} crisis endpoints`);

    // Select first endpoint
    await checkboxes.first().click();
    await page.waitForTimeout(300);
    console.log('✓ Selected crisis endpoint');

    // Configure
    const slider = page.locator('input[type="range"]').first();
    await slider.fill('3');
    await page.waitForTimeout(200);
    console.log('✓ Set max degrees to 3');

    // Click explore
    const exploreButton = page.locator('button').filter({ hasText: /explore/i });
    await exploreButton.click();
    console.log('✓ Clicked Explore button');

    console.log('\n=== STEP 2: Waiting for API response ===');

    // Wait longer for response
    await page.waitForTimeout(8000);

    console.log('\n=== STEP 3: Checking DOM state ===');

    // Check for ANY text on page
    const bodyText = await page.locator('body').textContent();
    console.log('Body contains "Total Nodes":', bodyText?.includes('Total Nodes'));
    console.log('Body contains "Subgraph Statistics":', bodyText?.includes('Subgraph Statistics'));
    console.log('Body contains "Policy Levers":', bodyText?.includes('Policy Levers'));
    console.log('Body contains "Exploring":', bodyText?.includes('Exploring'));
    console.log('Body contains "Loading":', bodyText?.includes('Loading'));

    // Check for stats section with multiple selectors
    const statsSelectors = [
      'text=/subgraph statistics/i',
      'text=/total nodes/i',
      'text=/total edges/i',
      'text=/policy levers/i',
      '[data-testid="crisis-stats"]',
      '.crisis-stats',
      'div:has-text("Total Nodes")',
      'div:has-text("Subgraph")',
    ];

    for (const selector of statsSelectors) {
      const elem = page.locator(selector);
      const count = await elem.count();
      const visible = count > 0 && await elem.first().isVisible().catch(() => false);
      console.log(`Selector "${selector}": count=${count}, visible=${visible}`);
    }

    // Check for SVG
    const svgSelectors = [
      'svg',
      'svg:has(g.graph-container)',
      'svg g.graph-container',
      '[data-testid="mechanism-graph"]',
      '.mechanism-graph svg',
    ];

    console.log('\n=== Checking for SVG elements ===');
    for (const selector of svgSelectors) {
      const elem = page.locator(selector);
      const count = await elem.count();
      const visible = count > 0 && await elem.first().isVisible().catch(() => false);
      console.log(`SVG "${selector}": count=${count}, visible=${visible}`);
    }

    // Check network requests
    console.log('\n=== Checking network activity ===');

    // Take screenshot for visual inspection
    await page.screenshot({
      path: 'test-results/crisis-explorer-debug-state.png',
      fullPage: true
    });
    console.log('✓ Screenshot saved to test-results/crisis-explorer-debug-state.png');

    // Get all divs with text content
    const allDivs = await page.locator('div').all();
    console.log(`\nTotal div elements: ${allDivs.length}`);

    // Check for React error boundary
    const errorBoundary = page.locator('text=/something went wrong/i');
    if (await errorBoundary.count() > 0) {
      console.log('⚠️ ERROR BOUNDARY TRIGGERED');
    }

    // Log current URL
    console.log('\nCurrent URL:', page.url());

    // This test always passes - it's for debugging
    expect(true).toBeTruthy();
  });

  test('Debug API call directly', async ({ page }) => {
    page.on('response', async (response) => {
      if (response.url().includes('/api/')) {
        console.log(`API Response: ${response.url()}`);
        console.log(`  Status: ${response.status()}`);
        try {
          const body = await response.text();
          console.log(`  Body preview: ${body.substring(0, 200)}...`);
        } catch (e) {
          console.log('  Could not read body');
        }
      }
    });

    await page.goto('/');
    await page.waitForLoadState('networkidle');

    const crisisTab = page.locator('a, button').filter({ hasText: /crisis/i });
    await crisisTab.click();
    await page.waitForTimeout(3000);

    const checkboxes = page.locator('input[type="checkbox"]');
    await checkboxes.first().click();
    await page.waitForTimeout(300);

    const exploreButton = page.locator('button').filter({ hasText: /explore/i });
    await exploreButton.click();

    // Wait to capture API calls
    await page.waitForTimeout(10000);

    expect(true).toBeTruthy();
  });
});
