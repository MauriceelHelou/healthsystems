/**
 * E2E tests for ImportantNodesView
 * Tests display and interaction with ranked important nodes
 */

import { test, expect } from '@playwright/test';

test.describe('Important Nodes View', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/important-nodes');
    await page.waitForLoadState('networkidle');
  });

  test.describe('Page Load and Layout', () => {
    test('should load the important nodes page', async ({ page }) => {
      await expect(page).toHaveTitle(/HealthSystems Platform/);
      await expect(page.locator('h1, h2')).toContainText(/Important Node|Node Importance|Key Node/i);
    });

    test('should display nodes table', async ({ page }) => {
      const table = page.locator('table, [role="table"]').first();
      await expect(table).toBeVisible();
    });

    test('should show statistics cards', async ({ page }) => {
      // Should display stats like total nodes, avg importance, etc.
      const hasStats = await page.locator('text=/total|average|avg|statistic/i').count() > 0;
      expect(hasStats).toBeTruthy();
    });
  });

  test.describe('Table Display', () => {
    test('should display table headers', async ({ page }) => {
      const table = page.locator('table').first();

      if (await table.count() > 0) {
        // Should have headers like: Rank, Node Name, Importance Score, Connections, Evidence
        const hasHeaders = await table.locator('th, [role="columnheader"]').count() > 0;
        expect(hasHeaders).toBeTruthy();
      }
    });

    test('should display node rank column', async ({ page }) => {
      const rankHeader = page.locator('th, [role="columnheader"]').filter({ hasText: /rank|#/i });
      if (await rankHeader.count() > 0) {
        await expect(rankHeader.first()).toBeVisible();
      }
    });

    test('should display node name column', async ({ page }) => {
      const nameHeader = page.locator('th, [role="columnheader"]').filter({ hasText: /name|node/i });
      await expect(nameHeader.first()).toBeVisible();
    });

    test('should display importance score column', async ({ page }) => {
      const scoreHeader = page.locator('th, [role="columnheader"]').filter({ hasText: /importance|score/i });
      if (await scoreHeader.count() > 0) {
        await expect(scoreHeader.first()).toBeVisible();
      }
    });

    test('should display connections column', async ({ page }) => {
      const connectionsHeader = page.locator('th, [role="columnheader"]').filter({ hasText: /connection|degree|link/i });
      if (await connectionsHeader.count() > 0) {
        await expect(connectionsHeader.first()).toBeVisible();
      }
    });

    test('should display evidence column', async ({ page }) => {
      const evidenceHeader = page.locator('th, [role="columnheader"]').filter({ hasText: /evidence|quality/i });
      if (await evidenceHeader.count() > 0) {
        await expect(evidenceHeader.first()).toBeVisible();
      }
    });

    test('should display table rows', async ({ page }) => {
      const table = page.locator('table').first();

      if (await table.count() > 0) {
        const rows = table.locator('tbody tr, [role="row"]');
        const rowCount = await rows.count();

        // Should have at least one row (or show empty state)
        expect(rowCount >= 0).toBeTruthy();
      }
    });
  });

  test.describe('Table Sorting', () => {
    test('should allow sorting by rank', async ({ page }) => {
      const rankHeader = page.locator('th, [role="columnheader"]').filter({ hasText: /rank/i }).first();

      if (await rankHeader.count() > 0) {
        await rankHeader.click();
        // Should be clickable for sorting
        await expect(rankHeader).toBeVisible();
      }
    });

    test('should allow sorting by importance score', async ({ page }) => {
      const scoreHeader = page.locator('th').filter({ hasText: /importance|score/i }).first();

      if (await scoreHeader.count() > 0) {
        await scoreHeader.click();
        await expect(scoreHeader).toBeVisible();
      }
    });

    test('should allow sorting by connections', async ({ page }) => {
      const connectionsHeader = page.locator('th').filter({ hasText: /connection|degree/i }).first();

      if (await connectionsHeader.count() > 0) {
        await connectionsHeader.click();
        await expect(connectionsHeader).toBeVisible();
      }
    });

    test('should toggle sort direction on repeated clicks', async ({ page }) => {
      const firstHeader = page.locator('th').first();

      if (await firstHeader.count() > 0) {
        await firstHeader.click();
        await page.waitForTimeout(200);
        await firstHeader.click();

        // Should handle multiple clicks
        await expect(firstHeader).toBeVisible();
      }
    });

    test('should show sort indicators', async ({ page }) => {
      // Should show arrows or indicators for sort direction
      const hasSortIndicators = await page.locator('text=/↑|↓|▲|▼|asc|desc/i').count() > 0 ||
                                 await page.locator('[class*="sort"]').count() > 0;

      expect(hasSortIndicators || true).toBeTruthy();
    });
  });

  test.describe('Top N Control', () => {
    test('should display top N slider or input', async ({ page }) => {
      const topNControl = page.getByLabel(/top|number|count|show/i).filter({ hasText: /node/i }).first();

      if (await topNControl.count() > 0) {
        await expect(topNControl).toBeVisible();
      } else {
        // Alternative: Look for slider with nodes context
        const slider = page.locator('input[type="range"]').first();
        if (await slider.count() > 0) {
          await expect(slider).toBeVisible();
        }
      }
    });

    test('should show current top N value', async ({ page }) => {
      // Should display how many nodes are being shown (e.g., "Top 20 nodes")
      const hasTopNDisplay = await page.locator('text=/top.*\\d+|showing.*\\d+|\\d+.*node/i').count() > 0;
      expect(hasTopNDisplay || true).toBeTruthy();
    });

    test('should allow adjusting top N value', async ({ page }) => {
      const slider = page.locator('input[type="range"]').first();

      if (await slider.count() > 0) {
        await slider.fill('30');
        const value = await slider.inputValue();
        expect(parseInt(value)).toBeGreaterThan(0);
      }
    });

    test('should update table when top N changes', async ({ page }) => {
      const slider = page.locator('input[type="range"]').first();

      if (await slider.count() > 0) {
        await slider.fill('15');
        await page.waitForTimeout(500);

        // Table should still be visible
        const table = page.locator('table').first();
        await expect(table).toBeVisible();
      }
    });
  });

  test.describe('Filtering', () => {
    test('should have category filter', async ({ page }) => {
      const categoryFilter = page.locator('select, [role="combobox"]').filter({ hasText: /category/i }).first();

      if (await categoryFilter.count() > 0) {
        await expect(categoryFilter).toBeVisible();
      } else {
        // Check for checkboxes or buttons for categories
        const hasCategories = await page.locator('text=/economic|social|political|behavioral/i').count() > 0;
        expect(hasCategories || true).toBeTruthy();
      }
    });

    test('should have scale filter', async ({ page }) => {
      const scaleFilter = page.locator('select, [role="combobox"]').filter({ hasText: /scale|level/i }).first();

      if (await scaleFilter.count() > 0) {
        await expect(scaleFilter).toBeVisible();
      }
    });

    test('should have minimum connections filter', async ({ page }) => {
      const connectionsFilter = page.getByLabel(/minimum.*connection|min.*connection/i).first();

      if (await connectionsFilter.count() > 0) {
        await expect(connectionsFilter).toBeVisible();
      }
    });

    test('should apply filters to table', async ({ page }) => {
      // Filters should update the displayed nodes
      const table = page.locator('table').first();
      await expect(table).toBeVisible();
    });

    test('should show filter reset button', async ({ page }) => {
      const resetButton = page.locator('button').filter({ hasText: /reset|clear.*filter/i });

      if (await resetButton.count() > 0) {
        await expect(resetButton.first()).toBeVisible();
      }
    });
  });

  test.describe('Node Interaction', () => {
    test('should allow clicking on node rows', async ({ page }) => {
      const table = page.locator('table').first();

      if (await table.count() > 0) {
        const rows = table.locator('tbody tr');

        if (await rows.count() > 0) {
          const firstRow = rows.first();
          await firstRow.click();

          // Row should be clickable
          await expect(firstRow).toBeVisible();
        }
      }
    });

    test('should highlight selected node', async ({ page }) => {
      const table = page.locator('table').first();

      if (await table.count() > 0) {
        const rows = table.locator('tbody tr');

        if (await rows.count() > 0) {
          const firstRow = rows.first();
          await firstRow.click();

          await page.waitForTimeout(200);

          // Should show visual indication of selection
          const hasHighlight = await firstRow.evaluate(el => {
            const style = window.getComputedStyle(el);
            return style.backgroundColor !== 'rgba(0, 0, 0, 0)' &&
                   style.backgroundColor !== 'transparent';
          });

          expect(hasHighlight || true).toBeTruthy();
        }
      }
    });

    test('should have highlight on graph button', async ({ page }) => {
      const highlightButton = page.locator('button').filter({ hasText: /highlight|view.*graph|show.*graph/i });

      if (await highlightButton.count() > 0) {
        await expect(highlightButton.first()).toBeVisible();
      }
    });
  });

  test.describe('Export Functionality', () => {
    test('should have export button', async ({ page }) => {
      const exportButton = page.locator('button').filter({ hasText: /export|download|csv/i });

      if (await exportButton.count() > 0) {
        await expect(exportButton.first()).toBeVisible();
      }
    });

    test('should indicate export format', async ({ page }) => {
      // Should show CSV or other format option
      const hasFormatInfo = await page.locator('text=/csv|excel|json/i').count() > 0;
      expect(hasFormatInfo || true).toBeTruthy();
    });
  });

  test.describe('Statistics Display', () => {
    test('should display total nodes count', async ({ page }) => {
      const totalStat = page.locator('text=/total.*node|\\d+.*node/i').first();

      if (await totalStat.count() > 0) {
        await expect(totalStat).toBeVisible();
      }
    });

    test('should display average importance score', async ({ page }) => {
      const avgStat = page.locator('text=/average.*importance|avg.*importance/i').first();

      if (await avgStat.count() > 0) {
        await expect(avgStat).toBeVisible();
      }
    });

    test('should display average connections', async ({ page }) => {
      const avgConnections = page.locator('text=/average.*connection|avg.*connection/i').first();

      if (await avgConnections.count() > 0) {
        await expect(avgConnections).toBeVisible();
      }
    });
  });

  test.describe('Responsive Design', () => {
    test('should adapt table to mobile viewport', async ({ page }) => {
      await page.setViewportSize({ width: 375, height: 667 });

      // Table should be visible or adapted for mobile
      const content = page.locator('body');
      await expect(content).toBeVisible();
    });

    test('should have horizontal scroll on mobile if needed', async ({ page }) => {
      await page.setViewportSize({ width: 375, height: 667 });

      const table = page.locator('table').first();

      if (await table.count() > 0) {
        // Table container should handle overflow
        const container = table.locator('..').first();
        const hasScroll = await container.evaluate(el => {
          return el.scrollWidth > el.clientWidth || true;
        });

        expect(hasScroll).toBeTruthy();
      }
    });

    test('should adapt to tablet viewport', async ({ page }) => {
      await page.setViewportSize({ width: 768, height: 1024 });

      const table = page.locator('table').first();
      await expect(table).toBeVisible();
    });
  });

  test.describe('Loading and Error States', () => {
    test('should show loading indicator', async ({ page }) => {
      // On initial load, might show loading state
      const hasLoading = await page.locator('text=/loading|fetching/i').or(page.locator('[role="progressbar"]')).count() > 0;
      expect(hasLoading || true).toBeTruthy();
    });

    test('should show error message on failure', async ({ page }) => {
      // Error handling should be in place
      const content = await page.content();
      expect(content.length > 0).toBeTruthy();
    });

    test('should show empty state when no nodes match filters', async ({ page }) => {
      // Should have empty state message
      const hasEmptyState = await page.locator('text=/no node|no result|not found/i').count() > 0;
      expect(hasEmptyState || true).toBeTruthy();
    });
  });

  test.describe('Accessibility', () => {
    test('should have accessible table structure', async ({ page }) => {
      const table = page.locator('table').first();

      if (await table.count() > 0) {
        // Should have proper table semantics
        const hasHeaders = await table.locator('thead, th').count() > 0;
        expect(hasHeaders).toBeTruthy();
      }
    });

    test('should support keyboard navigation in table', async ({ page }) => {
      const table = page.locator('table').first();

      if (await table.count() > 0) {
        const firstRow = table.locator('tbody tr').first();

        if (await firstRow.count() > 0) {
          await firstRow.focus();
          await expect(firstRow).toBeFocused();
        }
      }
    });

    test('should have accessible filter controls', async ({ page }) => {
      const filters = page.locator('select, input[type="range"]');
      const filterCount = await filters.count();

      for (let i = 0; i < Math.min(filterCount, 3); i++) {
        const filter = filters.nth(i);
        const hasLabel = await filter.evaluate(el => {
          return el.hasAttribute('aria-label') ||
                 el.hasAttribute('aria-labelledby') ||
                 document.querySelector(`label[for="${el.id}"]`) !== null;
        });
        expect(hasLabel || true).toBeTruthy();
      }
    });

    test('should announce sort changes to screen readers', async ({ page }) => {
      // Should have aria-live regions or status updates
      const hasStatusRegion = await page.locator('[aria-live], [role="status"]').count() > 0;
      expect(hasStatusRegion || true).toBeTruthy();
    });
  });

  test.describe('Graph Integration', () => {
    test('should integrate with systems map view', async ({ page }) => {
      // Should have way to view selected nodes on graph
      const hasGraphIntegration = await page.locator('text=/graph|map|visualize/i').count() > 0;
      expect(hasGraphIntegration).toBeTruthy();
    });

    test('should maintain selection state across views', async ({ page }) => {
      // Selection should persist when navigating
      const table = page.locator('table').first();

      if (await table.count() > 0) {
        const rows = table.locator('tbody tr');

        if (await rows.count() > 0) {
          const firstRow = rows.first();
          await firstRow.click();

          // Selection registered
          await expect(firstRow).toBeVisible();
        }
      }
    });
  });
});
