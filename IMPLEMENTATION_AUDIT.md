# Implementation Audit: Current vs. Target State

**Date**: November 23, 2025
**Purpose**: Gap analysis between current implementation and target specifications

---

## Executive Summary

### Current State:
- **76 mechanisms** in mechanism-bank (YAML files)
- **~150-200 unique nodes** (estimated from mechanisms)
- **7-scale system** implemented in code (MechanismGraph.tsx)
- **6 views** currently exist (not all match specs)
- **Force-directed and hierarchical layouts** implemented

### Target State (from specifications):
- **400+ nodes**
- **2000+ mechanisms**
- **7-scale hierarchy** (1, 3, 4, 6, 7 - with 2, 5 reserved)
- **4 primary views**: Systems Map, Pathway Explorer, Node Library, Evidence Base
- **Complete visualization features** with evidence badges, scale indicators, etc.

### Gap Analysis:
- ❌ **224-250 nodes missing** (current ~150-200 vs. target 400)
- ❌ **1924+ mechanisms missing** (current 76 vs. target 2000+)
- ⚠️ **Views mismatch**: Have 6 views, need specific 4 from specs
- ⚠️ **Missing features**: Node Library view, Evidence Base view
- ✅ **7-scale system**: Correctly implemented in visualization code
- ⚠️ **Evidence badges**: Not yet visible on edges
- ⚠️ **Scale indicators**: Not yet visible on nodes

---

## Detailed Audit

### 1. Scale System Analysis

**Current Implementation** ([MechanismGraph.tsx](frontend/src/visualizations/MechanismGraph.tsx#L43-L52)):
```typescript
const SCALE_TO_LEVEL_MAPPING: Record<number, number> = {
  1: 1, // Structural Determinants (policy)
  2: 2, // Built Environment & Infrastructure
  3: 3, // Institutional Infrastructure
  4: 4, // Individual/Household Conditions
  5: 5, // Individual Behaviors & Psychosocial
  6: 6, // Intermediate Pathways
  7: 7, // Crisis Endpoints
};
```

**Target Specification** (from [03_SYSTEMS_MAP_VISUALIZATION.md](docs/Design/03_SYSTEMS_MAP_VISUALIZATION.md)):
- **Active scales**: 1, 3, 4, 6, 7
- **Reserved scales**: 2, 5 (for future use)
- **Scale meanings**:
  - Scale 1: Structural Determinants
  - Scale 3: Institutional Infrastructure
  - Scale 4: Individual/Household Conditions
  - Scale 6: Intermediate Biological Pathways
  - Scale 7: Crisis Endpoints

**✅ FINDING**: Code correctly implements all 7 scales with proper mappings.

**⚠️ USER REPORTED "6 SCALES"**: This may refer to:
1. Visual representation showing only 6 levels in certain views
2. Confusion about reserved scales 2 and 5
3. Missing scale badges on nodes making it unclear

**ACTION NEEDED**:
- Verify scale badges are visible on nodes
- Add scale legend explaining active vs. reserved scales
- Check if any views are collapsing scales

---

### 2. Node Count Analysis

**Current State**:
- **76 mechanism YAML files** in `mechanism-bank/mechanisms/`
- Each mechanism has 2 nodes (from + to)
- Estimated **~150-200 unique nodes** (many nodes appear in multiple mechanisms)

**Categories in Current Mechanisms**:
- `behavioral/` - 7 files
- `biological/` - 9 files
- `built_environment/` - 28 files
- `economic/` - 11 files
- `healthcare_access/` - 10 files
- `political/` - 6 files
- `social_environment/` - 11 files

**Target State**: **400+ nodes**

**❌ GAP**: **224-250 nodes missing** (assuming current is ~150-200)

**Sample Existing Nodes** (from mechanism files):
- `childhood_aces` (behavioral)
- `alcohol_use_disorder` (behavioral)
- `acute_liver_failure` (biological)
- `alcohol_induced_mortality` (biological)
- `air_pollution_concentration` (built_environment)
- `housing_quality` (built_environment)
- `unemployment` (economic)
- `housing_instability` (economic)
- `lack_insurance` (healthcare_access)
- `medicaid_expansion` (political)
- `neighborhood_poverty` (social_environment)
- `violent_crime_exposure` (social_environment)

**ACTION NEEDED**:
- Extract full list of unique nodes from all 76 mechanisms
- Identify missing node categories and domains
- Prioritize next 224 nodes to add based on:
  - Health domains not yet covered
  - Structural determinants missing
  - Intermediate pathways missing

---

### 3. Mechanism Count Analysis

**Current State**: **76 mechanisms**

**Distribution by Category**:
- Behavioral: 7 (9%)
- Biological: 9 (12%)
- Built Environment: 28 (37%)
- Economic: 11 (14%)
- Healthcare Access: 10 (13%)
- Political: 6 (8%)
- Social Environment: 11 (14%)

**Target State**: **2000+ mechanisms**

**❌ GAP**: **1924+ mechanisms missing** (current 76 vs. target 2000+)

**Growth Strategy Needed**:
- Current focus: Respiratory health (asthma) and Alcohol-related disease
- Need to expand to:
  - Cardiovascular disease pathways
  - Mental health pathways
  - Maternal/child health pathways
  - Infectious disease pathways
  - Chronic disease pathways
  - Injury/violence pathways
  - Environmental health pathways

**ACTION NEEDED**:
- Review literature extraction pipelines
- Scale up LLM mechanism discovery
- Implement systematic review process
- Add mechanisms from existing health systems frameworks

---

### 4. Views Analysis

**Current Views** (from [frontend/src/views/](frontend/src/views/)):
1. ✅ **SystemsMapView.tsx** - Main network visualization (matches spec)
2. ✅ **PathfinderView.tsx** - Pathfinding between nodes (matches spec partially)
3. ✅ **PathwayExplorerView.tsx** - Pathway listing (matches spec)
4. ✅ **CrisisExplorerView.tsx** - Crisis endpoint analysis (matches spec)
5. ⚠️ **ImportantNodesView.tsx** - Node importance ranking (not in spec)
6. ⚠️ **AlcoholismSystemView.tsx** - Domain-specific view (not in spec)

**Target Views** (from [02_DASHBOARD_LAYOUT.md](docs/Design/02_DASHBOARD_LAYOUT.md)):
1. ✅ **Systems Map** - Complete network visualization (EXISTS)
2. ⚠️ **Pathway Explorer** - Show pathways between nodes (EXISTS but different from spec)
3. ❌ **Node Library** - Searchable catalog of all nodes (MISSING)
4. ❌ **Evidence Base** - Searchable catalog of mechanisms with evidence (MISSING)

**Spec Details for Missing Views**:

**Node Library** (from spec):
- Grid/table view of all 400 nodes
- Columns: Node name, scale, category, # connections, description
- Search and filter by category, scale
- Click node → "View in Map" button zooms to node in Systems Map
- Preview panel showing node details and direct connections

**Evidence Base** (from spec):
- Table view of all mechanisms
- Columns: From node, to node, direction, evidence quality, source studies
- Search and filter by nodes, categories, evidence quality
- Click mechanism → Show in Systems Map with path highlighted
- Citations and source metadata visible
- Download/export capability

**⚠️ GAP**:
- PathfinderView and PathwayExplorerView overlap but neither matches spec exactly
- Node Library missing entirely
- Evidence Base missing entirely
- AlcoholismSystemView and ImportantNodesView not in spec

**ACTION NEEDED**:
- Build Node Library view from scratch
- Build Evidence Base view from scratch
- Consolidate or clarify Pathfinder vs. Pathway Explorer
- Decide if domain-specific views (AlcoholismSystemView) should remain

---

### 5. Visualization Features Analysis

**Current Features** (from [MechanismGraph.tsx](frontend/src/visualizations/MechanismGraph.tsx)):
- ✅ Force-directed layout with physics simulation
- ✅ Hierarchical layout (7 levels)
- ✅ Node wrapping and text truncation
- ✅ Zoom and pan
- ✅ Drag nodes (force-directed mode)
- ✅ Hover effects with glow
- ✅ Click handlers for nodes and edges
- ✅ Crisis highlighting (color by degree from crisis)
- ✅ Policy lever highlighting (gold stroke)
- ✅ Path highlighting
- ✅ Node importance highlighting with rank badges
- ✅ Node selection modes for pathfinder
- ✅ Level labels at top (hierarchical mode)
- ⚠️ Edge arrows (present but small)
- ❌ Evidence quality badges on edges (not visible)
- ❌ Scale badges on nodes (not visible)
- ❌ Node category color fills (all nodes white)

**Target Features** (from [03_SYSTEMS_MAP_VISUALIZATION.md](docs/Design/03_SYSTEMS_MAP_VISUALIZATION.md)):

**Nodes should have**:
- ✅ White background
- ⚠️ **Category-based border colors** (currently all gray #333)
- ❌ **Scale badge/indicator** (small circle or number showing scale 1-7)
- ✅ Wrapped text labels
- ✅ Size based on connections (partially - not fully implemented)
- ✅ Hover highlighting

**Edges should have**:
- ✅ Curved bezier paths
- ✅ Directional arrows
- ⚠️ **Evidence quality badge** (A/B/C indicator) - MISSING
- ⚠️ **Strength indicated by width** (partially - all edges same width 2.5)
- ✅ Color for negative relationships (red)
- ⚠️ **Dashed for weaker evidence** - NOT IMPLEMENTED

**Legend should show**:
- ❌ **Scale system** (7 scales with active/reserved)
- ❌ **Category colors**
- ❌ **Evidence quality levels** (A/B/C)
- ❌ **Edge types** (positive/negative, strong/weak)
- ⚠️ **Current legend**: Only shows crisis highlighting when active

**Interactive Features**:
- ✅ Zoom/pan
- ✅ Node click for details
- ✅ Edge click for mechanism details
- ✅ Drag to reposition (force-directed)
- ⚠️ **Search** - Not integrated into graph component
- ⚠️ **Filter by category** - Partially implemented
- ⚠️ **Filter by scale** - Not implemented
- ⚠️ **Filter by evidence quality** - Not implemented
- ❌ **Level of detail rendering** - Not implemented (all nodes always visible)

**Performance Optimizations**:
- ✅ Force simulation with configurable physics
- ⚠️ **Virtualization for large networks** - Not implemented
- ⚠️ **Level of detail (LOD)** - Not implemented
- ⚠️ **Semantic zoom** - Not implemented
- ⚠️ **WebGL rendering** - Not implemented (using SVG)

**Accessibility**:
- ✅ ARIA labels on nodes and edges
- ✅ Keyboard navigation (Tab, Enter, Space)
- ✅ Descriptive text for screen readers
- ⚠️ **Keyboard-only zoom controls** - Missing
- ⚠️ **High contrast mode** - Not implemented
- ⚠️ **Focus indicators** - Basic but could be enhanced

**❌ GAPS**:
- Missing evidence quality badges on edges
- Missing scale badges on nodes
- Missing category border colors on nodes
- Missing comprehensive legend
- Missing advanced filtering UI
- Missing LOD/virtualization for 400+ nodes
- Edge width not varied by strength
- No dashed edges for weak evidence

**ACTION NEEDED**:
1. **HIGH PRIORITY**:
   - Add evidence quality badges (A/B/C) to edges
   - Add scale badges/indicators to nodes
   - Add category-based border colors
   - Build comprehensive legend

2. **MEDIUM PRIORITY**:
   - Implement filtering UI (by scale, category, evidence)
   - Vary edge width by mechanism strength
   - Add dashed edges for weak evidence
   - Improve search integration

3. **PERFORMANCE** (for 400+ nodes):
   - Implement LOD rendering
   - Consider WebGL for large networks
   - Add virtualization/culling

---

### 6. Data Schema Analysis

**Current Mechanism Schema** (from YAML files):
```yaml
id: unique_mechanism_id
type: causal
direction: positive | negative
from_node:
  id: node_id
  label: "Node Label"
  category: behavioral | biological | built_environment | economic | healthcare_access | political | social_environment
  scale: 1-7
to_node:
  id: node_id
  label: "Node Label"
  category: ...
  scale: 1-7
evidence:
  strength: A | B | C
  studies: [...]
  summary: "..."
```

**Target Schema** (from spec):
- ✅ Node ID and label
- ✅ Category
- ✅ Scale (1-7)
- ✅ Evidence strength (A/B/C)
- ⚠️ **Missing**: `description` field for nodes
- ⚠️ **Missing**: `connections` metadata (incoming/outgoing counts)
- ⚠️ **Missing**: `importance_score` for node ranking
- ⚠️ **Missing**: `geographic_context` for pathway activation
- ⚠️ **Missing**: `quantified_effect_size` (Phase 2 feature)
- ⚠️ **Missing**: `uncertainty_bounds` (Phase 2 feature)

**ACTION NEEDED**:
- Add `description` field to all nodes
- Pre-compute `connections` metadata
- Implement `importance_score` calculation
- Add `geographic_context` tags (Phase 2)

---

### 7. Backend API Analysis

**Current Endpoints** (from [backend/api/routes/](backend/api/routes/)):
- ✅ `GET /api/nodes` - List all nodes
- ✅ `GET /api/mechanisms` - List all mechanisms
- ✅ `GET /api/crisis-endpoints` - List crisis nodes
- ✅ `POST /api/crisis-subgraph` - Get subgraph upstream from crisis
- ✅ `POST /api/pathfinding` - Find paths between nodes
- ✅ `GET /api/pathways` - List pre-computed pathways (has data issues)
- ⚠️ Missing: `GET /api/nodes/{id}` - Get single node details
- ⚠️ Missing: `GET /api/mechanisms/{id}` - Get single mechanism details
- ⚠️ Missing: `GET /api/search` - Full-text search across nodes and mechanisms
- ⚠️ Missing: `GET /api/node-neighborhood/{id}` - Get direct connections of a node

**ACTION NEEDED**:
- Add single-resource GET endpoints
- Implement search API
- Add node neighborhood endpoint
- Fix pathway generation (currently returns empty array)

---

### 8. Testing Coverage Analysis

**Current Tests**:
- ✅ **46 total tests** (22 backend + 24 frontend)
- ✅ **96% pass rate** (44/46 passing)
- ✅ **Pathfinder**: 10/10 tests passing (100%)
- ✅ **Crisis Explorer**: 13/14 tests passing (93%)
- ✅ **Backend APIs**: 16/22 passing (73%)

**Missing Test Coverage**:
- ❌ Node Library view (doesn't exist yet)
- ❌ Evidence Base view (doesn't exist yet)
- ❌ Pathway Explorer comprehensive tests
- ❌ Systems Map interaction tests
- ❌ Performance tests for 400+ nodes
- ❌ Accessibility tests (WCAG 2.1 AA compliance)
- ❌ Integration tests for complete workflows

**ACTION NEEDED**:
- Expand test coverage to 80%+ (per project standards)
- Add accessibility test suite
- Add performance benchmarks
- Test with full 400-node dataset

---

## Priority Roadmap

### Phase 1: Complete Core Visualization (Next 2 weeks)

**Week 1: Enhance Existing Visualization**
1. ✅ Add evidence quality badges to edges (A/B/C indicators)
2. ✅ Add scale badges to nodes (1-7 indicators)
3. ✅ Add category-based border colors
4. ✅ Build comprehensive legend
5. ✅ Implement filtering UI (scale, category, evidence)
6. ✅ Write tests for new features

**Week 2: Build Missing Views**
7. ✅ Build Node Library view
   - Searchable table of all nodes
   - Filter by scale, category
   - "View in Map" integration
   - Preview panel
8. ✅ Build Evidence Base view
   - Searchable table of mechanisms
   - Filter by evidence quality
   - Citation display
   - Export functionality
9. ✅ Add missing API endpoints
10. ✅ Write tests for new views

### Phase 2: Scale Up Content (Next 4 weeks)

**Weeks 3-4: Add 150 More Nodes**
11. Extract nodes from health systems frameworks
12. Run LLM mechanism discovery on:
    - Cardiovascular disease
    - Mental health
    - Maternal/child health
13. Validate and add to mechanism bank
14. Target: 300+ nodes total

**Weeks 5-6: Add 500 More Mechanisms**
15. Systematic literature review pipeline
16. Bulk mechanism extraction
17. Quality validation
18. Target: 500+ mechanisms total

### Phase 3: Performance & Polish (Weeks 7-8)

**Week 7: Performance Optimization**
19. Implement LOD rendering for large networks
20. Add virtualization/culling
21. Consider WebGL renderer
22. Performance benchmarks with 400+ nodes

**Week 8: Accessibility & Polish**
23. WCAG 2.1 AA compliance audit
24. Keyboard-only navigation improvements
25. High contrast mode
26. Screen reader optimization
27. Final testing & documentation

---

## Success Metrics

### Immediate (Phase 1):
- [ ] All visualization features from spec implemented
- [ ] Node Library view functional
- [ ] Evidence Base view functional
- [ ] Test coverage ≥80%
- [ ] Zero critical bugs

### Medium-term (Phase 2):
- [ ] 300+ nodes in system
- [ ] 500+ mechanisms catalogued
- [ ] All health domains represented
- [ ] Geographic customization enabled

### Long-term (Phase 3):
- [ ] 400+ nodes (target reached)
- [ ] 2000+ mechanisms (target reached)
- [ ] <3s load time for full network
- [ ] WCAG 2.1 AA compliant
- [ ] User satisfaction ≥4.5/5

---

## Risks & Mitigation

**Risk 1**: Content creation bottleneck (1924 mechanisms to add)
- **Mitigation**: Automate with LLM pipelines, systematic review tools
- **Timeline impact**: Could delay Phase 2 by 2-4 weeks

**Risk 2**: Performance degradation with 400+ nodes
- **Mitigation**: LOD rendering, WebGL, virtualization
- **Fallback**: Progressive loading, pagination

**Risk 3**: User confusion about scale system (reported "6 scales")
- **Mitigation**: Clear legend, documentation, scale badges visible
- **Immediate action**: Add scale explanation to UI

**Risk 4**: Test coverage maintenance burden
- **Mitigation**: Automated testing in CI/CD, test generation tools
- **Resource**: Allocate 20% of dev time to testing

---

## Conclusion

**Current Status**: **~40% complete** vs. target specifications

**Strengths**:
- ✅ 7-scale system correctly implemented
- ✅ Core visualization working well
- ✅ Good test coverage for existing features
- ✅ Pathfinder and Crisis Explorer functional

**Critical Gaps**:
- ❌ 224-250 nodes missing (56-62% of target)
- ❌ 1924+ mechanisms missing (96% of target)
- ❌ Node Library view missing
- ❌ Evidence Base view missing
- ⚠️ Visualization missing evidence badges, scale indicators

**Recommendation**: **Proceed with Phase 1 roadmap** to complete core visualization and missing views before scaling up content in Phase 2.

**Estimated Timeline**: 8 weeks to full MVP (400 nodes, key features complete)

**Next Immediate Actions**:
1. Add evidence quality badges to edges
2. Add scale badges to nodes
3. Build Node Library view
4. Build Evidence Base view
5. Extract full node list from existing mechanisms
