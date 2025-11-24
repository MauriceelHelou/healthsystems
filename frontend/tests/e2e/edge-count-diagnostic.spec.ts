import { test, expect } from '@playwright/test';

test('Edge Count Diagnostic', async ({ page }) => {
  console.log('\n========== EDGE COUNT DIAGNOSTIC ==========\n');

  await page.goto('/');
  await page.waitForTimeout(3000);

  // Count all paths in links group
  const allPaths = page.locator('g.links path');
  const allPathCount = await allPaths.count();
  console.log(`Total paths in g.links: ${allPathCount}`);

  // Count paths per link group
  const linkGroups = page.locator('g.link');
  const linkGroupCount = await linkGroups.count();
  console.log(`Total g.link groups: ${linkGroupCount}`);

  if (linkGroupCount > 0) {
    // Check first link group
    const firstLink = linkGroups.first();
    const pathsInFirstLink = firstLink.locator('path');
    const pathsInFirstLinkCount = await pathsInFirstLink.count();
    console.log(`Paths in first g.link: ${pathsInFirstLinkCount}`);

    // Get details of each path in first link
    for (let i = 0; i < pathsInFirstLinkCount; i++) {
      const path = pathsInFirstLink.nth(i);
      const attrs = await path.evaluate((el) => ({
        stroke: el.getAttribute('stroke'),
        strokeWidth: el.getAttribute('stroke-width'),
        fill: el.getAttribute('fill'),
        markerEnd: el.getAttribute('marker-end'),
        pointerEvents: el.getAttribute('pointer-events')
      }));
      console.log(`  Path ${i}:`, JSON.stringify(attrs));
    }
  }

  // Count transparent paths
  const transparentPaths = await page.locator('g.links path').evaluateAll((paths) => {
    return paths.filter(p => p.getAttribute('stroke') === 'transparent').length;
  });
  console.log(`\nTransparent hitbox paths: ${transparentPaths}`);

  // Count visible paths
  const visiblePaths = await page.locator('g.links path').evaluateAll((paths) => {
    return paths.filter(p => p.getAttribute('stroke') !== 'transparent').length;
  });
  console.log(`Visible stroke paths: ${visiblePaths}`);

  console.log('\n========== DIAGNOSTIC COMPLETE ==========\n');

  expect(true).toBe(true);
});
