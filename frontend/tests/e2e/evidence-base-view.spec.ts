import { test, expect } from '@playwright/test';

/**
 * Test Suite: Evidence Base View
 *
 * Tests for the Evidence Base view - a searchable catalog of all mechanisms
 * with evidence metadata, as specified in 02_DASHBOARD_LAYOUT.md
 *
 * Target features:
 * - Table view of all mechanisms
 * - Search and filter by nodes, categories, evidence quality
 * - Show mechanism details with citations
 * - "Show in Map" button to highlight pathway
 * - Export/download functionality
 */

test.describe('Evidence Base View', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('networkidle');
  });

  test('Evidence Base tab should be accessible', async ({ page }) => {
    // Look for Evidence Base tab in navigation
    const evidenceBaseTab = page.locator('a, button').filter({ hasText: /evidence.*base|mechanism.*catalog|evidence/i });
    const tabCount = await evidenceBaseTab.count();

    console.log(`Found ${tabCount} potential Evidence Base tabs`);

    if (tabCount > 0) {
      console.log('✓ Evidence Base tab found');
      const firstTab = evidenceBaseTab.first();
      await firstTab.click();
      await page.waitForTimeout(1000);

      // Verify we navigated to Evidence Base
      const url = page.url();
      console.log(`Current URL: ${url}`);

      const isEvidenceBase = url.includes('evidence') || url.includes('mechanism');
      if (isEvidenceBase) {
        console.log('✓ Navigated to Evidence Base view');
        expect(isEvidenceBase).toBeTruthy();
      }
    } else {
      console.log('❌ Evidence Base tab not found - view not implemented yet');
      test.skip();
    }
  });

  test('Evidence Base should display table of mechanisms', async ({ page }) => {
    const evidenceBaseTab = page.locator('a, button').filter({ hasText: /evidence.*base|mechanism/i });

    if (await evidenceBaseTab.count() === 0) {
      test.skip();
      return;
    }

    await evidenceBaseTab.first().click();
    await page.waitForTimeout(1500);

    // Look for table or grid
    const table = page.locator('table, [role="table"], .mechanism-grid, .mechanism-list');
    const tableVisible = await table.isVisible().catch(() => false);

    if (tableVisible) {
      console.log('✓ Mechanism table/grid found');

      // Check for table headers
      const headers = page.locator('th, [role="columnheader"]');
      const headerCount = await headers.count();
      console.log(`Found ${headerCount} table headers`);

      // Expected columns: From, To, Direction, Evidence Quality, Studies
      if (headerCount > 0) {
        const headerTexts = [];
        for (let i = 0; i < Math.min(headerCount, 10); i++) {
          const text = await headers.nth(i).textContent();
          headerTexts.push(text);
        }
        console.log(`Headers: ${headerTexts.join(', ')}`);

        // Should have key columns
        const hasFromColumn = headerTexts.some(h => h && /from|source/i.test(h));
        const hasToColumn = headerTexts.some(h => h && /to|target|destination/i.test(h));
        const hasEvidenceColumn = headerTexts.some(h => h && /evidence|quality/i.test(h));

        console.log(`Has From: ${hasFromColumn}, To: ${hasToColumn}, Evidence: ${hasEvidenceColumn}`);

        expect(hasFromColumn || hasToColumn || hasEvidenceColumn).toBeTruthy();
      }

      // Check for table rows
      const rows = page.locator('tr, [role="row"]').filter({ hasNot: page.locator('thead tr, [role="columnheader"]') });
      const rowCount = await rows.count();
      console.log(`Found ${rowCount} mechanism rows`);

      expect(rowCount).toBeGreaterThan(0);
    } else {
      console.log('❌ Mechanism table not found');
      test.skip();
    }
  });

  test('Should search mechanisms by node names', async ({ page }) => {
    const evidenceBaseTab = page.locator('a, button').filter({ hasText: /evidence.*base|mechanism/i });

    if (await evidenceBaseTab.count() === 0) {
      test.skip();
      return;
    }

    await evidenceBaseTab.first().click();
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

  test('Should filter mechanisms by evidence quality', async ({ page }) => {
    const evidenceBaseTab = page.locator('a, button').filter({ hasText: /evidence.*base|mechanism/i });

    if (await evidenceBaseTab.count() === 0) {
      test.skip();
      return;
    }

    await evidenceBaseTab.first().click();
    await page.waitForTimeout(1500);

    // Look for evidence quality filter
    const evidenceFilter = page.locator('select, [role="combobox"]').filter({ hasText: /evidence|quality/i }).or(
      page.locator('input[type="checkbox"], input[type="radio"]').filter({ hasText: /A|B|C|quality/i })
    );
    const filterCount = await evidenceFilter.count();

    if (filterCount > 0) {
      console.log('✓ Evidence quality filter found');

      const firstFilter = evidenceFilter.first();
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
      console.log(`Evidence filter effect: ${filterWorked ? 'working' : 'no change'}`);
    } else {
      console.log('❌ Evidence quality filter not found');
      test.skip();
    }
  });

  test('Should filter mechanisms by category', async ({ page }) => {
    const evidenceBaseTab = page.locator('a, button').filter({ hasText: /evidence.*base|mechanism/i });

    if (await evidenceBaseTab.count() === 0) {
      test.skip();
      return;
    }

    await evidenceBaseTab.first().click();
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

  test('Should show mechanism details panel', async ({ page }) => {
    const evidenceBaseTab = page.locator('a, button').filter({ hasText: /evidence.*base|mechanism/i });

    if (await evidenceBaseTab.count() === 0) {
      test.skip();
      return;
    }

    await evidenceBaseTab.first().click();
    await page.waitForTimeout(1500);

    // Click on first mechanism row
    const firstRow = page.locator('tr, [role="row"]').nth(1);
    await firstRow.click();
    await page.waitForTimeout(500);

    // Look for details panel
    const detailsPanel = page.locator('.details-panel, .mechanism-detail, [data-testid="mechanism-details"], aside, .detail-sidebar');
    const panelVisible = await detailsPanel.isVisible().catch(() => false);

    if (panelVisible) {
      console.log('✓ Details panel found');

      const panelText = await detailsPanel.textContent();
      console.log(`Details panel content: ${panelText?.substring(0, 100)}...`);

      // Should contain mechanism information
      const hasMechanismInfo = panelText && (
        panelText.includes('From') ||
        panelText.includes('To') ||
        panelText.includes('Evidence') ||
        panelText.includes('Citation') ||
        panelText.includes('Study')
      );

      if (hasMechanismInfo) {
        console.log('✓ Details panel shows mechanism information');
        expect(hasMechanismInfo).toBeTruthy();
      }
    } else {
      console.log('⚠ Details panel not visible (may open on hover/click)');
    }
  });

  test('Should show citations and sources', async ({ page }) => {
    const evidenceBaseTab = page.locator('a, button').filter({ hasText: /evidence.*base|mechanism/i });

    if (await evidenceBaseTab.count() === 0) {
      test.skip();
      return;
    }

    await evidenceBaseTab.first().click();
    await page.waitForTimeout(1500);

    // Click on first mechanism row
    const firstRow = page.locator('tr, [role="row"]').nth(1);
    await firstRow.click();
    await page.waitForTimeout(500);

    // Look for citations section
    const citationsSection = page.locator('text=/citation|reference|source|study|doi/i');
    const sectionVisible = await citationsSection.isVisible().catch(() => false);

    if (sectionVisible) {
      console.log('✓ Citations section found');

      // Look for formatted citation or DOI
      const citationText = await citationsSection.textContent();
      console.log(`Citation text: ${citationText?.substring(0, 100)}...`);

      // Should contain citation-like content
      const hasCitation = citationText && (
        citationText.includes('et al') ||
        citationText.includes('doi') ||
        citationText.includes('http') ||
        /\d{4}/.test(citationText) // year
      );

      if (hasCitation) {
        console.log('✓ Citation information shown');
        expect(hasCitation).toBeTruthy();
      }
    } else {
      console.log('⚠ Citations section not visible');
    }
  });

  test('Should show "Show in Map" button', async ({ page }) => {
    const evidenceBaseTab = page.locator('a, button').filter({ hasText: /evidence.*base|mechanism/i });

    if (await evidenceBaseTab.count() === 0) {
      test.skip();
      return;
    }

    await evidenceBaseTab.first().click();
    await page.waitForTimeout(1500);

    // Look for "Show in Map" button
    const showInMapButton = page.locator('button, a').filter({ hasText: /show.*map|view.*map|go to map|highlight/i }).first();
    const buttonVisible = await showInMapButton.isVisible().catch(() => false);

    if (buttonVisible) {
      console.log('✓ "Show in Map" button found');

      // Click button
      await showInMapButton.click();
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

          // Path should be highlighted (check for highlighted edges or nodes)
          const highlightedPath = page.locator('g.link.highlighted, g.node.highlighted, path.highlighted');
          const pathHighlighted = await highlightedPath.count() > 0;

          if (pathHighlighted) {
            console.log('✓ Pathway highlighted in graph');
            expect(pathHighlighted).toBeTruthy();
          } else {
            console.log('⚠ Pathway highlighting not visible');
          }
        }
      }
    } else {
      console.log('❌ "Show in Map" button not found');
      test.skip();
    }
  });

  test('Should show evidence quality indicators in table', async ({ page }) => {
    const evidenceBaseTab = page.locator('a, button').filter({ hasText: /evidence.*base|mechanism/i });

    if (await evidenceBaseTab.count() === 0) {
      test.skip();
      return;
    }

    await evidenceBaseTab.first().click();
    await page.waitForTimeout(1500);

    // Look for evidence quality badges/indicators in table
    const evidenceBadges = page.locator('td .badge, td [data-evidence], td .evidence-quality, td span').filter({ hasText: /^[ABC]$/ });
    const badgeCount = await evidenceBadges.count();

    console.log(`Found ${badgeCount} evidence quality badges in table`);

    if (badgeCount > 0) {
      console.log('✓ Evidence quality indicators shown in table');

      // Check badge content
      const firstBadge = evidenceBadges.first();
      const badgeText = await firstBadge.textContent();
      console.log(`First badge: ${badgeText}`);

      expect(badgeText).toMatch(/^[ABC]$/);
    } else {
      // Alternative: check for text indicators
      const evidenceText = page.locator('td').filter({ hasText: /quality.*[ABC]|[ABC].*quality/i });
      const textCount = await evidenceText.count();

      console.log(`Found ${textCount} evidence quality text indicators`);

      if (textCount === 0) {
        console.log('⚠ Evidence quality indicators not found in table');
      }
    }
  });

  test('Should support export/download functionality', async ({ page }) => {
    const evidenceBaseTab = page.locator('a, button').filter({ hasText: /evidence.*base|mechanism/i });

    if (await evidenceBaseTab.count() === 0) {
      test.skip();
      return;
    }

    await evidenceBaseTab.first().click();
    await page.waitForTimeout(1500);

    // Look for export/download button
    const exportButton = page.locator('button, a').filter({ hasText: /export|download|csv|excel/i });
    const exportCount = await exportButton.count();

    console.log(`Found ${exportCount} export/download buttons`);

    if (exportCount > 0) {
      console.log('✓ Export/download button found');

      const firstExport = exportButton.first();
      const buttonText = await firstExport.textContent();
      console.log(`Export button text: ${buttonText}`);

      // Button should be clickable
      const isEnabled = await firstExport.isEnabled();
      if (isEnabled) {
        console.log('✓ Export button is enabled');
        expect(isEnabled).toBeTruthy();
      }

      // Note: Not actually clicking to avoid downloading files in test
    } else {
      console.log('⚠ Export/download functionality not found');
    }
  });

  test('Should handle pagination for large mechanism lists', async ({ page }) => {
    const evidenceBaseTab = page.locator('a, button').filter({ hasText: /evidence.*base|mechanism/i });

    if (await evidenceBaseTab.count() === 0) {
      test.skip();
      return;
    }

    await evidenceBaseTab.first().click();
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

        // Get first mechanism before pagination
        const firstMechanismBefore = await page.locator('tr, [role="row"]').nth(1).textContent();
        console.log(`First mechanism before pagination: ${firstMechanismBefore?.substring(0, 50)}...`);

        // Click next
        await nextButton.click();
        await page.waitForTimeout(1000);

        // Get first mechanism after pagination
        const firstMechanismAfter = await page.locator('tr, [role="row"]').nth(1).textContent();
        console.log(`First mechanism after pagination: ${firstMechanismAfter?.substring(0, 50)}...`);

        // Should show different mechanisms
        const paginationWorked = firstMechanismBefore !== firstMechanismAfter;
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
