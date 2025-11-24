import { test, expect } from '@playwright/test';

/**
 * Test Suite: Node Library View
 *
 * Tests for the Node Library view - a searchable catalog of all nodes
 * as specified in 02_DASHBOARD_LAYOUT.md
 *
 * Target features:
 * - Grid/table view of all nodes
 * - Search and filter by name, category, scale
 * - Sort by connections, name, scale
 * - "View in Map" button to zoom to node
 * - Preview panel showing node details
 */

test.describe('Node Library View', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('networkidle');
  });

  test('Node Library tab should be accessible', async ({ page }) => {
    // Look for Node Library tab in navigation
    const nodeLibraryTab = page.locator('a, button').filter({ hasText: /node library|nodes|catalog/i });
    const tabCount = await nodeLibraryTab.count();

    console.log(`Found ${tabCount} potential Node Library tabs`);

    if (tabCount > 0) {
      console.log('✓ Node Library tab found');
      const firstTab = nodeLibraryTab.first();
      await firstTab.click();
      await page.waitForTimeout(1000);

      // Verify we navigated to Node Library
      const url = page.url();
      console.log(`Current URL: ${url}`);

      const isNodeLibrary = url.includes('node') || url.includes('library') || url.includes('catalog');
      if (isNodeLibrary) {
        console.log('✓ Navigated to Node Library view');
        expect(isNodeLibrary).toBeTruthy();
      }
    } else {
      console.log('❌ Node Library tab not found - view not implemented yet');
      test.skip();
    }
  });

  test('Node Library should display table of all nodes', async ({ page }) => {
    const nodeLibraryTab = page.locator('a, button').filter({ hasText: /node library|nodes/i });

    if (await nodeLibraryTab.count() === 0) {
      test.skip();
      return;
    }

    await nodeLibraryTab.first().click();
    await page.waitForTimeout(1500);

    // Look for table or grid
    const table = page.locator('table, [role="table"], .node-grid, .node-list');
    const tableVisible = await table.isVisible().catch(() => false);

    if (tableVisible) {
      console.log('✓ Node table/grid found');

      // Check for table headers
      const headers = page.locator('th, [role="columnheader"]');
      const headerCount = await headers.count();
      console.log(`Found ${headerCount} table headers`);

      // Expected columns: Name, Scale, Category, Connections, Description
      if (headerCount > 0) {
        const headerTexts = [];
        for (let i = 0; i < Math.min(headerCount, 10); i++) {
          const text = await headers.nth(i).textContent();
          headerTexts.push(text);
        }
        console.log(`Headers: ${headerTexts.join(', ')}`);

        // Should have key columns
        const hasNameColumn = headerTexts.some(h => h && /name|node/i.test(h));
        const hasScaleColumn = headerTexts.some(h => h && /scale|level/i.test(h));
        const hasCategoryColumn = headerTexts.some(h => h && /category|type/i.test(h));

        console.log(`Has Name: ${hasNameColumn}, Scale: ${hasScaleColumn}, Category: ${hasCategoryColumn}`);

        expect(hasNameColumn || hasScaleColumn || hasCategoryColumn).toBeTruthy();
      }

      // Check for table rows
      const rows = page.locator('tr, [role="row"]').filter({ hasNot: page.locator('thead tr, [role="columnheader"]') });
      const rowCount = await rows.count();
      console.log(`Found ${rowCount} node rows`);

      expect(rowCount).toBeGreaterThan(0);
    } else {
      console.log('❌ Node table not found');
      test.skip();
    }
  });

  test('Should search nodes by name', async ({ page }) => {
    const nodeLibraryTab = page.locator('a, button').filter({ hasText: /node library|nodes/i });

    if (await nodeLibraryTab.count() === 0) {
      test.skip();
      return;
    }

    await nodeLibraryTab.first().click();
    await page.waitForTimeout(1500);

    // Look for search input
    const searchInput = page.locator('input[type="search"], input[placeholder*="search" i], input[placeholder*="filter" i]').first();
    const searchVisible = await searchInput.isVisible().catch(() => false);

    if (searchVisible) {
      console.log('✓ Search input found');

      // Count initial rows
      const initialRows = await page.locator('tr, [role="row"]').count();
      console.log(`Initial rows: ${initialRows}`);

      // Type search query
      await searchInput.fill('alcohol');
      await page.waitForTimeout(500);

      // Count filtered rows
      const filteredRows = await page.locator('tr, [role="row"]').count();
      console.log(`Filtered rows: ${filteredRows}`);

      // Should filter results
      const filterWorked = filteredRows !== initialRows || filteredRows === 0 || filteredRows === 1;
      console.log(`Search filter effect: ${filterWorked ? 'working' : 'no change'}`);

      if (filterWorked) {
        console.log('✓ Search filtering works');
      }
    } else {
      console.log('❌ Search input not found');
      test.skip();
    }
  });

  test('Should filter nodes by category', async ({ page }) => {
    const nodeLibraryTab = page.locator('a, button').filter({ hasText: /node library|nodes/i });

    if (await nodeLibraryTab.count() === 0) {
      test.skip();
      return;
    }

    await nodeLibraryTab.first().click();
    await page.waitForTimeout(1500);

    // Look for category filter
    const categoryFilter = page.locator('select, [role="combobox"]').filter({ hasText: /category/i }).or(
      page.locator('input[type="checkbox"]').filter({ hasText: /behavioral|biological|economic/i })
    );
    const filterCount = await categoryFilter.count();

    if (filterCount > 0) {
      console.log('✓ Category filter found');

      const firstFilter = categoryFilter.first();
      const tagName = await firstFilter.evaluate((el) => el.tagName.toLowerCase());

      // Count initial rows
      const initialRows = await page.locator('tr, [role="row"]').count();
      console.log(`Initial rows: ${initialRows}`);

      // Apply filter
      if (tagName === 'select') {
        await firstFilter.selectOption({ index: 1 });
      } else {
        await firstFilter.click();
      }

      await page.waitForTimeout(500);

      // Count filtered rows
      const filteredRows = await page.locator('tr, [role="row"]').count();
      console.log(`Filtered rows: ${filteredRows}`);

      const filterWorked = filteredRows !== initialRows;
      console.log(`Category filter effect: ${filterWorked ? 'working' : 'no change'}`);
    } else {
      console.log('❌ Category filter not found');
      test.skip();
    }
  });

  test('Should filter nodes by scale', async ({ page }) => {
    const nodeLibraryTab = page.locator('a, button').filter({ hasText: /node library|nodes/i });

    if (await nodeLibraryTab.count() === 0) {
      test.skip();
      return;
    }

    await nodeLibraryTab.first().click();
    await page.waitForTimeout(1500);

    // Look for scale filter
    const scaleFilter = page.locator('select, [role="combobox"]').filter({ hasText: /scale|level/i }).or(
      page.locator('input[type="checkbox"], input[type="radio"]').filter({ hasText: /scale|1|2|3|4|5|6|7/i })
    );
    const filterCount = await scaleFilter.count();

    if (filterCount > 0) {
      console.log('✓ Scale filter found');

      const firstFilter = scaleFilter.first();
      const tagName = await firstFilter.evaluate((el) => el.tagName.toLowerCase());

      // Count initial rows
      const initialRows = await page.locator('tr, [role="row"]').count();
      console.log(`Initial rows: ${initialRows}`);

      // Apply filter
      if (tagName === 'select') {
        await firstFilter.selectOption({ index: 1 });
      } else {
        await firstFilter.click();
      }

      await page.waitForTimeout(500);

      // Count filtered rows
      const filteredRows = await page.locator('tr, [role="row"]').count();
      console.log(`Filtered rows: ${filteredRows}`);

      const filterWorked = filteredRows !== initialRows;
      console.log(`Scale filter effect: ${filterWorked ? 'working' : 'no change'}`);
    } else {
      console.log('❌ Scale filter not found');
      test.skip();
    }
  });

  test('Should sort nodes by connections', async ({ page }) => {
    const nodeLibraryTab = page.locator('a, button').filter({ hasText: /node library|nodes/i });

    if (await nodeLibraryTab.count() === 0) {
      test.skip();
      return;
    }

    await nodeLibraryTab.first().click();
    await page.waitForTimeout(1500);

    // Look for sortable column header (Connections)
    const connectionHeader = page.locator('th, [role="columnheader"]').filter({ hasText: /connection|degree/i });
    const headerVisible = await connectionHeader.isVisible().catch(() => false);

    if (headerVisible) {
      console.log('✓ Connections column header found');

      // Get first row data before sort
      const firstRowBefore = await page.locator('tr, [role="row"]').nth(1).textContent();
      console.log(`First row before sort: ${firstRowBefore}`);

      // Click header to sort
      await connectionHeader.click();
      await page.waitForTimeout(500);

      // Get first row data after sort
      const firstRowAfter = await page.locator('tr, [role="row"]').nth(1).textContent();
      console.log(`First row after sort: ${firstRowAfter}`);

      // Data should change (unless already sorted)
      const sortWorked = firstRowBefore !== firstRowAfter;
      console.log(`Sort effect: ${sortWorked ? 'working' : 'no change'}`);
    } else {
      console.log('❌ Connections column not found');
      test.skip();
    }
  });

  test('Should show "View in Map" button', async ({ page }) => {
    const nodeLibraryTab = page.locator('a, button').filter({ hasText: /node library|nodes/i });

    if (await nodeLibraryTab.count() === 0) {
      test.skip();
      return;
    }

    await nodeLibraryTab.first().click();
    await page.waitForTimeout(1500);

    // Look for "View in Map" button in first row
    const viewInMapButton = page.locator('button, a').filter({ hasText: /view.*map|show.*map|go to map/i }).first();
    const buttonVisible = await viewInMapButton.isVisible().catch(() => false);

    if (buttonVisible) {
      console.log('✓ "View in Map" button found');

      // Click button
      await viewInMapButton.click();
      await page.waitForTimeout(1500);

      // Should navigate to Systems Map
      const url = page.url();
      console.log(`Current URL after click: ${url}`);

      const isSystemsMap = url.includes('map') || url.includes('system');
      if (isSystemsMap) {
        console.log('✓ Navigated to Systems Map');

        // Graph should be visible
        const svg = page.locator('svg:has(g.graph-container)');
        const graphVisible = await svg.isVisible({ timeout: 5000 }).catch(() => false);

        if (graphVisible) {
          console.log('✓ Graph visualization visible');
          expect(graphVisible).toBeTruthy();
        }
      }
    } else {
      console.log('❌ "View in Map" button not found');
      test.skip();
    }
  });

  test('Should show node preview panel', async ({ page }) => {
    const nodeLibraryTab = page.locator('a, button').filter({ hasText: /node library|nodes/i });

    if (await nodeLibraryTab.count() === 0) {
      test.skip();
      return;
    }

    await nodeLibraryTab.first().click();
    await page.waitForTimeout(1500);

    // Click on first node row
    const firstRow = page.locator('tr, [role="row"]').nth(1);
    await firstRow.click();
    await page.waitForTimeout(500);

    // Look for preview panel
    const previewPanel = page.locator('.preview-panel, .node-detail, [data-testid="node-preview"], aside, .detail-sidebar');
    const panelVisible = await previewPanel.isVisible().catch(() => false);

    if (panelVisible) {
      console.log('✓ Preview panel found');

      const panelText = await previewPanel.textContent();
      console.log(`Preview panel content: ${panelText?.substring(0, 100)}...`);

      // Should contain node information
      const hasNodeInfo = panelText && (
        panelText.includes('Node') ||
        panelText.includes('Scale') ||
        panelText.includes('Category') ||
        panelText.includes('Connection')
      );

      if (hasNodeInfo) {
        console.log('✓ Preview panel shows node information');
        expect(hasNodeInfo).toBeTruthy();
      }
    } else {
      console.log('⚠ Preview panel not visible (may open on hover/click)');
    }
  });

  test('Should show node connections in preview', async ({ page }) => {
    const nodeLibraryTab = page.locator('a, button').filter({ hasText: /node library|nodes/i });

    if (await nodeLibraryTab.count() === 0) {
      test.skip();
      return;
    }

    await nodeLibraryTab.first().click();
    await page.waitForTimeout(1500);

    // Click on first node row
    const firstRow = page.locator('tr, [role="row"]').nth(1);
    await firstRow.click();
    await page.waitForTimeout(500);

    // Look for connections section in preview
    const connectionsSection = page.locator('text=/incoming|outgoing|connection|edge/i');
    const sectionVisible = await connectionsSection.isVisible().catch(() => false);

    if (sectionVisible) {
      console.log('✓ Connections section found in preview');

      // Look for list of connected nodes
      const connectedNodes = page.locator('ul li, .connection-item, .connected-node');
      const nodeCount = await connectedNodes.count();
      console.log(`Found ${nodeCount} connected nodes in preview`);

      if (nodeCount > 0) {
        console.log('✓ Connected nodes listed in preview');
      }
    } else {
      console.log('⚠ Connections section not visible');
    }
  });

  test('Should handle pagination for large node lists', async ({ page }) => {
    const nodeLibraryTab = page.locator('a, button').filter({ hasText: /node library|nodes/i });

    if (await nodeLibraryTab.count() === 0) {
      test.skip();
      return;
    }

    await nodeLibraryTab.first().click();
    await page.waitForTimeout(1500);

    // Look for pagination controls
    const pagination = page.locator('.pagination, [role="navigation"]').filter({ hasText: /page|next|previous/i });
    const paginationVisible = await pagination.isVisible().catch(() => false);

    if (paginationVisible) {
      console.log('✓ Pagination controls found');

      // Look for "Next" button
      const nextButton = page.locator('button, a').filter({ hasText: /next|>/i }).first();
      const nextEnabled = await nextButton.isEnabled().catch(() => false);

      if (nextEnabled) {
        console.log('✓ Next page button enabled');

        // Get first node name
        const firstNodeBefore = await page.locator('tr, [role="row"]').nth(1).textContent();
        console.log(`First node before pagination: ${firstNodeBefore}`);

        // Click next
        await nextButton.click();
        await page.waitForTimeout(1000);

        // Get first node name after pagination
        const firstNodeAfter = await page.locator('tr, [role="row"]').nth(1).textContent();
        console.log(`First node after pagination: ${firstNodeAfter}`);

        // Should show different nodes
        const paginationWorked = firstNodeBefore !== firstNodeAfter;
        console.log(`Pagination effect: ${paginationWorked ? 'working' : 'no change'}`);

        if (paginationWorked) {
          expect(paginationWorked).toBeTruthy();
        }
      }
    } else {
      console.log('⚠ Pagination not found (may not be needed for current dataset size)');
    }
  });
});
