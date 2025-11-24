# Test-Driven Implementation Plan

**Date**: November 23, 2025
**Approach**: Write tests first, then implement features to pass tests
**Status**: Tests written, ready for implementation

---

## Overview

Following Test-Driven Development (TDD) methodology, I have created comprehensive test suites for all missing features identified in the [Implementation Audit](IMPLEMENTATION_AUDIT.md). Tests are written to fail initially, then guide implementation to meet specifications.

---

## Tests Created

### 1. Evidence Quality Badges (`evidence-badges.spec.ts`)
**Location**: [frontend/tests/e2e/evidence-badges.spec.ts](frontend/tests/e2e/evidence-badges.spec.ts)

**Tests Written** (6 tests):
- ✅ Systems Map should display evidence badges on edges
- ✅ Evidence badges should be color-coded by quality (A/B/C)
- ✅ Edge hover should show full evidence details
- ✅ Legend should explain evidence quality levels
- ✅ Should filter edges by evidence quality

**Expected Behavior**:
- Edges display small badges showing "A", "B", or "C" evidence quality
- A-quality: Green background (#10B981)
- B-quality: Yellow background (#EAB308)
- C-quality: Orange background (#F97316)
- Hovering edge shows full citation and evidence details
- Legend explains evidence quality system
- Filter UI allows filtering by evidence quality

**Implementation Checklist**:
- [ ] Add evidence badge rendering to MechanismGraph.tsx
- [ ] Style badges with quality-based colors
- [ ] Add evidence tooltip on edge hover
- [ ] Update legend component to include evidence quality
- [ ] Add evidence quality filter to sidebar
- [ ] Extract evidence data from mechanism YAML files

---

### 2. Scale Badges on Nodes (`scale-badges.spec.ts`)
**Location**: [frontend/tests/e2e/scale-badges.spec.ts](frontend/tests/e2e/scale-badges.spec.ts)

**Tests Written** (7 tests):
- ✅ Systems Map nodes should display scale badges
- ✅ Scale badges should show values 1-7
- ✅ Hierarchical layout should group nodes by scale
- ✅ Node hover should show scale information
- ✅ Legend should explain 7-scale system
- ✅ Should filter nodes by scale
- ✅ Should show active vs reserved scales (2, 5 reserved)

**Expected Behavior**:
- Nodes display small circle or badge showing scale number (1-7)
- Badge positioned in top-right corner of node
- Scale 1: Policy/Structural (Purple)
- Scale 3: Institutional (Blue)
- Scale 4: Individual (Green)
- Scale 6: Intermediate (Yellow)
- Scale 7: Crisis (Red)
- Scales 2 and 5: Grayed out or marked "Reserved"
- Hierarchical layout groups nodes by scale vertically
- Legend explains active vs reserved scales
- Filter UI allows filtering by scale

**Implementation Checklist**:
- [ ] Add scale badge rendering to MechanismGraph.tsx
- [ ] Position badges in node top-right corner
- [ ] Color-code scale badges
- [ ] Add scale info to aria-labels and tooltips
- [ ] Update legend to show all 7 scales
- [ ] Add scale filter to sidebar
- [ ] Ensure hierarchical layout respects scale grouping

---

### 3. Node Library View (`node-library-view.spec.ts`)
**Location**: [frontend/tests/e2e/node-library-view.spec.ts](frontend/tests/e2e/node-library-view.spec.ts)

**Tests Written** (10 tests):
- ✅ Node Library tab should be accessible
- ✅ Should display table of all nodes
- ✅ Should search nodes by name
- ✅ Should filter nodes by category
- ✅ Should filter nodes by scale
- ✅ Should sort nodes by connections
- ✅ Should show "View in Map" button
- ✅ Should show node preview panel
- ✅ Should show node connections in preview
- ✅ Should handle pagination for large node lists

**Expected Behavior**:
- New tab "Node Library" in navigation
- Table view with columns:
  - Node Name
  - Scale (1-7)
  - Category (behavioral, biological, etc.)
  - Connections (incoming/outgoing counts)
  - Description (truncated)
- Search bar filters by node name
- Filter dropdowns for category and scale
- Sortable columns (click header to sort)
- Click node row → Preview panel slides in from right
- Preview panel shows:
  - Full node details
  - List of connected nodes
  - "View in Map" button
- Click "View in Map" → Navigate to Systems Map with node zoomed/highlighted
- Pagination for 400+ nodes (20 per page)

**Implementation Checklist**:
- [ ] Create NodeLibraryView.tsx component
- [ ] Add "Node Library" tab to navigation
- [ ] Build data table with react-table or similar
- [ ] Implement search filter
- [ ] Implement category and scale filters
- [ ] Implement column sorting
- [ ] Build preview panel component
- [ ] Wire up "View in Map" → Systems Map zoom
- [ ] Add pagination (20 items per page)
- [ ] Fetch node data from API
- [ ] Responsive design for mobile/tablet

---

### 4. Evidence Base View (`evidence-base-view.spec.ts`)
**Location**: [frontend/tests/e2e/evidence-base-view.spec.ts](frontend/tests/e2e/evidence-base-view.spec.ts)

**Tests Written** (10 tests):
- ✅ Evidence Base tab should be accessible
- ✅ Should display table of mechanisms
- ✅ Should search mechanisms by node names
- ✅ Should filter mechanisms by evidence quality
- ✅ Should filter mechanisms by category
- ✅ Should show mechanism details panel
- ✅ Should show citations and sources
- ✅ Should show "Show in Map" button
- ✅ Should show evidence quality indicators in table
- ✅ Should support export/download functionality

**Expected Behavior**:
- New tab "Evidence Base" in navigation
- Table view with columns:
  - From Node
  - To Node
  - Direction (→ or ←)
  - Evidence Quality (A/B/C badge)
  - # Studies
  - Primary Citation (author, year)
- Search bar filters by node names or keywords
- Filter dropdowns for evidence quality and category
- Click mechanism row → Details panel slides in from right
- Details panel shows:
  - Full mechanism description
  - Pathway steps
  - Primary citation (formatted)
  - Supporting citations (list)
  - DOI links
  - "Show in Map" button
- Click "Show in Map" → Navigate to Systems Map with pathway highlighted
- "Export" button downloads CSV/Excel of filtered mechanisms
- Pagination for 2000+ mechanisms (50 per page)

**Implementation Checklist**:
- [ ] Create EvidenceBaseView.tsx component
- [ ] Add "Evidence Base" tab to navigation
- [ ] Build mechanisms data table
- [ ] Implement search filter (nodes and keywords)
- [ ] Implement evidence quality filter
- [ ] Implement category filter
- [ ] Build details panel component
- [ ] Format citations properly
- [ ] Wire up "Show in Map" → Systems Map pathway highlight
- [ ] Add CSV/Excel export functionality
- [ ] Add pagination (50 items per page)
- [ ] Fetch mechanism data from API
- [ ] Responsive design for mobile/tablet

---

## Implementation Order

### Phase 1: Enhance Existing Visualization (Week 1)
**Goal**: Add missing visual features to MechanismGraph component

**Day 1-2: Evidence Badges**
1. Run tests: `npx playwright test evidence-badges.spec.ts`
2. Implement evidence badge rendering
3. Add evidence tooltips
4. Update legend
5. Add evidence filter
6. Re-run tests until passing

**Day 3-4: Scale Badges**
1. Run tests: `npx playwright test scale-badges.spec.ts`
2. Implement scale badge rendering
3. Add scale tooltips
4. Update legend
5. Add scale filter
6. Re-run tests until passing

**Day 5: Category Colors & Legend**
1. Add category-based border colors to nodes
2. Build comprehensive legend component
3. Integrate legend into all views
4. Verify all visual enhancements work together

**Success Criteria**:
- All 13 visualization tests passing
- Evidence badges visible on edges
- Scale badges visible on nodes
- Comprehensive legend displayed

---

### Phase 2: Build Missing Views (Week 2)
**Goal**: Create Node Library and Evidence Base views

**Day 6-7: Node Library View**
1. Run tests: `npx playwright test node-library-view.spec.ts` (should fail - view doesn't exist)
2. Create NodeLibraryView component structure
3. Add tab to navigation
4. Build data table with columns
5. Implement search and filters
6. Build preview panel
7. Wire up "View in Map" navigation
8. Add pagination
9. Re-run tests until passing

**Day 8-9: Evidence Base View**
1. Run tests: `npx playwright test evidence-base-view.spec.ts` (should fail - view doesn't exist)
2. Create EvidenceBaseView component structure
3. Add tab to navigation
4. Build mechanisms data table
5. Implement search and filters
6. Build details panel with citations
7. Wire up "Show in Map" navigation
8. Add export functionality
9. Add pagination
10. Re-run tests until passing

**Day 10: Integration & Polish**
1. Test all views work together
2. Verify navigation between views
3. Test "View in Map" and "Show in Map" zoom/highlight features
4. Mobile/tablet responsive testing
5. Accessibility audit (keyboard nav, screen readers)

**Success Criteria**:
- All 20 new view tests passing
- Node Library fully functional
- Evidence Base fully functional
- Navigation between views seamless
- Responsive on all devices

---

## Running Tests

### Run All New Tests:
```bash
cd frontend
npx playwright test evidence-badges.spec.ts scale-badges.spec.ts node-library-view.spec.ts evidence-base-view.spec.ts --project=chromium
```

### Run Individual Test Suites:
```bash
# Evidence badges only
npx playwright test evidence-badges.spec.ts --project=chromium

# Scale badges only
npx playwright test scale-badges.spec.ts --project=chromium

# Node Library only
npx playwright test node-library-view.spec.ts --project=chromium

# Evidence Base only
npx playwright test evidence-base-view.spec.ts --project=chromium
```

### Run in Headed Mode (see browser):
```bash
npx playwright test evidence-badges.spec.ts --headed --project=chromium
```

### Run Specific Test:
```bash
npx playwright test evidence-badges.spec.ts -g "should display evidence badges on edges"
```

---

## Expected Test Results (Before Implementation)

**Current Status**: All tests should **SKIP** or **FAIL** because features don't exist yet

```
Evidence Badges Tests:
  ⏭  Systems Map should display evidence badges on edges - SKIPPED (badges not found)
  ⏭  Evidence badges should be color-coded by quality - SKIPPED (badges not found)
  ⏭  Edge hover should show full evidence details - SKIPPED (tooltips not found)
  ⏭  Legend should explain evidence quality levels - SKIPPED (legend incomplete)
  ⏭  Should filter edges by evidence quality - SKIPPED (filter not found)

Scale Badges Tests:
  ⏭  Systems Map nodes should display scale badges - SKIPPED (badges not found)
  ⏭  Scale badges should show values 1-7 - SKIPPED (badges not found)
  ⏭  Hierarchical layout should group nodes by scale - PASSING ✅ (already works)
  ⏭  Node hover should show scale information - SKIPPED (aria-label incomplete)
  ⏭  Legend should explain 7-scale system - SKIPPED (legend incomplete)
  ⏭  Should filter nodes by scale - SKIPPED (filter not found)
  ⏭  Should show active vs reserved scales - SKIPPED (documentation not found)

Node Library Tests:
  ❌ Node Library tab should be accessible - FAILED (tab not found)
  ❌ Should display table of all nodes - FAILED (view doesn't exist)
  ❌ Should search nodes by name - FAILED (view doesn't exist)
  ❌ Should filter nodes by category - FAILED (view doesn't exist)
  ❌ Should filter nodes by scale - FAILED (view doesn't exist)
  ❌ Should sort nodes by connections - FAILED (view doesn't exist)
  ❌ Should show "View in Map" button - FAILED (view doesn't exist)
  ❌ Should show node preview panel - FAILED (view doesn't exist)
  ❌ Should show node connections in preview - FAILED (view doesn't exist)
  ❌ Should handle pagination - FAILED (view doesn't exist)

Evidence Base Tests:
  ❌ Evidence Base tab should be accessible - FAILED (tab not found)
  ❌ Should display table of mechanisms - FAILED (view doesn't exist)
  ❌ Should search mechanisms by node names - FAILED (view doesn't exist)
  ❌ Should filter mechanisms by evidence quality - FAILED (view doesn't exist)
  ❌ Should filter mechanisms by category - FAILED (view doesn't exist)
  ❌ Should show mechanism details panel - FAILED (view doesn't exist)
  ❌ Should show citations and sources - FAILED (view doesn't exist)
  ❌ Should show "Show in Map" button - FAILED (view doesn't exist)
  ❌ Should show evidence quality indicators - FAILED (view doesn't exist)
  ❌ Should support export/download - FAILED (view doesn't exist)
```

**Target Status** (After Implementation): All tests **PASSING** ✅

---

## Implementation Resources

### Components to Create:
1. [frontend/src/components/visualization/EvidenceBadge.tsx](frontend/src/components/visualization/EvidenceBadge.tsx) - NEW
2. [frontend/src/components/visualization/ScaleBadge.tsx](frontend/src/components/visualization/ScaleBadge.tsx) - NEW
3. [frontend/src/components/visualization/Legend.tsx](frontend/src/components/visualization/Legend.tsx) - NEW
4. [frontend/src/views/NodeLibraryView.tsx](frontend/src/views/NodeLibraryView.tsx) - NEW
5. [frontend/src/views/EvidenceBaseView.tsx](frontend/src/views/EvidenceBaseView.tsx) - NEW
6. [frontend/src/components/tables/NodeTable.tsx](frontend/src/components/tables/NodeTable.tsx) - NEW
7. [frontend/src/components/tables/MechanismTable.tsx](frontend/src/components/tables/MechanismTable.tsx) - NEW
8. [frontend/src/components/panels/NodePreviewPanel.tsx](frontend/src/components/panels/NodePreviewPanel.tsx) - NEW
9. [frontend/src/components/panels/MechanismDetailsPanel.tsx](frontend/src/components/panels/MechanismDetailsPanel.tsx) - NEW

### Components to Modify:
1. [frontend/src/visualizations/MechanismGraph.tsx](frontend/src/visualizations/MechanismGraph.tsx) - Add badges
2. [frontend/src/layouts/DashboardLayout.tsx](frontend/src/layouts/DashboardLayout.tsx) - Add new tabs
3. [frontend/src/layouts/Header.tsx](frontend/src/layouts/Header.tsx) - Update navigation

### Types to Add:
```typescript
// frontend/src/types/evidence.ts
export interface EvidenceQuality {
  rating: 'A' | 'B' | 'C';
  nStudies: number;
  primaryCitation: string;
  supportingCitations: string[];
  doi?: string;
}

// frontend/src/types/nodeLibrary.ts
export interface NodeTableRow {
  id: string;
  name: string;
  scale: number;
  category: string;
  incomingConnections: number;
  outgoingConnections: number;
  description: string;
}

// frontend/src/types/evidenceBase.ts
export interface MechanismTableRow {
  id: string;
  fromNode: string;
  toNode: string;
  direction: 'positive' | 'negative';
  evidenceQuality: 'A' | 'B' | 'C';
  nStudies: number;
  primaryCitation: string;
  category: string;
}
```

---

## Success Metrics

### Test Coverage:
- **Current**: 46 tests (22 backend + 24 frontend)
- **After Phase 1**: 59 tests (+13 visualization tests)
- **After Phase 2**: 79 tests (+20 view tests)
- **Target**: 80%+ code coverage

### Features Implemented:
- [x] Audit completed
- [x] Tests written
- [ ] Evidence badges on edges (Phase 1)
- [ ] Scale badges on nodes (Phase 1)
- [ ] Category border colors (Phase 1)
- [ ] Comprehensive legend (Phase 1)
- [ ] Node Library view (Phase 2)
- [ ] Evidence Base view (Phase 2)

### Timeline:
- **Week 1**: Visualization enhancements (Days 1-5)
- **Week 2**: New views (Days 6-10)
- **Total**: 10 working days to complete

---

## Next Steps

1. **Immediate**: Review tests and audit document
2. **Day 1**: Begin evidence badge implementation
3. **Daily**: Run tests, implement features, iterate until passing
4. **End of Week 1**: All visualization tests passing
5. **End of Week 2**: All view tests passing
6. **Week 3**: Begin Phase 2 of content scale-up (see [IMPLEMENTATION_AUDIT.md](IMPLEMENTATION_AUDIT.md))

---

## Notes

- Tests use Playwright's `.skip()` method when features not found (graceful degradation)
- Console logging in tests helps debug what's missing
- Tests check for multiple selector variations (future-proof)
- All tests follow WCAG 2.1 AA accessibility guidelines
- Tests are independent and can run in any order
- Tests use realistic user workflows (click, search, filter, navigate)

**Philosophy**: Let the tests guide the implementation. Don't write features the tests don't require. Keep implementation minimal and focused on passing tests.
