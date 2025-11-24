# COMPREHENSIVE PROMPT: 7-SCALE NODE STRATIFICATION MIGRATION

## 1. PROJECT GOAL

**Migrate the HealthSystems Platform node taxonomy from 5 active scales to a scientifically-weighted 7-scale hierarchy that accurately represents causal pathways from structural determinants to health crisis endpoints.**

### END STATE

- **850 nodes** distributed across **all 7 scales** (currently only 5 scales are used)
- **Scale 2**: Built environment factors and structural determinants (NEW)
- **Scale 5**: Individual behaviors that drive health outcomes (NEW)
- **Dynamic visualization**: Frontend renders only occupied scale columns (2-7 columns adaptive)
- **Zero scale multipliers**: Remove backend importance weighting by scale
- **Zero breaking changes**: All node IDs preserved, only scale field updated
- **100% documentation consistency**: All references to "5 scales" updated to "7 scales"

### TAXONOMY DEFINITIONS

**Scale 1: STRUCTURAL DETERMINANTS** (Macro-Policy Level)
- Federal/state laws, regulations, macro-economic conditions
- Highest causal distance from crisis endpoints (most upstream)
- Examples: Medicaid expansion status, minimum wage laws, rent control policy
- Position: **Most preventative** interventions

**Scale 2: BUILT ENVIRONMENT & STRUCTURAL DETERMINANTS** (NEW)
- Infrastructure, environmental conditions, structural resources
- Regional/state-level structural factors that shape institutional capacity
- Examples: Transportation networks, environmental quality, housing stock, zoning laws
- Position: Between macro-policy and institutional implementation

**Scale 3: INSTITUTIONAL INFRASTRUCTURE**
- Organizations, systems, institutional capacity, service delivery
- Local implementation of policies through institutions
- Examples: FQHC density, affordable housing units, school nurse availability
- Position: Institutional readiness and availability

**Scale 4: INDIVIDUAL/HOUSEHOLD CONDITIONS**
- Proximal living conditions, exposures, material circumstances
- Lived experiences at individual/household level
- Examples: Housing cost burden, food insecurity, uninsured status
- Position: Immediate environmental and social context

**Scale 5: INDIVIDUAL BEHAVIORS & PSYCHOSOCIAL FACTORS** (NEW)
- Health-related behaviors, coping mechanisms, psychosocial processes
- Individual-level actions and psychological responses that bridge conditions to pathways
- Examples: Health literacy, care-seeking behavior, stress responses, social support utilization
- Position: Between conditions and biological pathways

**Scale 6: INTERMEDIATE PATHWAYS**
- Biological risk factors, clinical measures, healthcare utilization patterns
- Mediating variables between conditions/behaviors and health outcomes
- Examples: Preventive care utilization, hypertension control, medication adherence
- Position: Proximal clinical and physiological factors

**Scale 7: CRISIS ENDPOINTS**
- Acute health outcomes, mortality, system failures
- Sentinel health events requiring urgent intervention
- Examples: ED visits, hospitalizations, mortality, ICU admissions
- Position: **Most reactive** interventions (crisis response)

### CLASSIFICATION PRINCIPLES

**Nodes are stratified by THREE dimensions:**

1. **Structural → Individual Spectrum**
   - Scale 1-2: Structural (policies, environment, infrastructure)
   - Scale 3-4: Institutional and material conditions
   - Scale 5-6: Individual behaviors and biological pathways
   - Scale 7: Health outcomes

2. **Preventative → Reactive Spectrum**
   - Scale 1-3: Preventative (upstream intervention opportunities)
   - Scale 4-5: Early intervention (before disease pathways activate)
   - Scale 6: Disease management (pathways active)
   - Scale 7: Crisis response (acute care)

3. **Causal Distance from Crisis Endpoints**
   - Scale 1: Longest latency (decades from policy change to outcome)
   - Scale 2-3: Long latency (years to decades)
   - Scale 4-5: Medium latency (months to years)
   - Scale 6: Short latency (weeks to months)
   - Scale 7: Zero latency (immediate outcomes)

---

## 2. TECHNICAL STACK

**Core Technologies:**
- **Backend**: Python 3.11+, FastAPI, Pydantic
- **Frontend**: React 18+, TypeScript 5+, Vite, D3.js (force-directed graphs)
- **Data**: YAML (mechanism bank), Markdown (node inventory)
- **Testing**: pytest (backend), Jest + React Testing Library (frontend), Playwright (E2E)
- **Documentation**: Markdown, GitHub-flavored

**Specialized Agents (USE THESE):**
- **epidemiology-advisor**: Validate scale assignments for scientific accuracy
- **mechanism-validator**: Validate mechanism YAML integrity after node updates
- **code-reviewer**: Review all TypeScript and Python changes
- **test-generator**: Generate comprehensive test suites for scale logic

**Documentation References:**
- For latest D3.js patterns: Use web search with "D3.js v7 force simulation 2025"
- For React best practices: Use web search with "React 18 TypeScript patterns 2025"
- For FastAPI: Use web search with "FastAPI Pydantic v2 2025"

---

## 3. FEATURES

### 3.1 Node Reclassification (Core Feature)

**Requirement**: Reclassify 850 nodes across 7 scales using scientific criteria

**Implementation**:
1. **Read existing inventory**: `Nodes/COMPLETE_NODE_INVENTORY.md`
2. **For each node**:
   - Analyze node label, category, and current scale
   - Apply classification principles (structural→individual, preventative→reactive, causal distance)
   - Assign new scale (1-7)
   - Preserve node ID, label, category, and all other fields
3. **Generate distribution report**:
   - Count nodes per scale
   - Validate scientific weighting (expect: more nodes at scales 3-4-5, fewer at 1-2-7)
   - Flag outliers for manual review
4. **Use epidemiology-advisor agent** to validate each scale assignment for:
   - Causal logic (does the scale match causal distance?)
   - Structural competency (does it reflect structural determinants appropriately?)
   - Embodiment theory (does it match ecosocial theory?)

**Expected Distribution** (approximate):
- Scale 1: 80-100 nodes (macro-policy is limited in scope)
- Scale 2: 150-200 nodes (built environment is broad)
- Scale 3: 180-220 nodes (institutional infrastructure)
- Scale 4: 200-250 nodes (individual conditions - largest category)
- Scale 5: 100-150 nodes (behaviors and psychosocial factors)
- Scale 6: 100-120 nodes (clinical pathways)
- Scale 7: 50-80 nodes (crisis endpoints are specific)

### 3.2 Frontend Visualization Refactoring

**Requirement**: Dynamic column rendering based on occupied scales

**Current State**:
- Hardcoded 5-level visualization (`const numLevels = 5`)
- Fixed mapping: `SCALE_TO_LEVEL_MAPPING = {1:1, 3:2, 4:3, 6:4, 7:5}`
- Files: `frontend/src/visualizations/MechanismGraph.tsx`, `AlcoholismSystemDiagram.tsx`

**New Behavior**:
- **Dynamic level calculation**: Count unique scales in filtered node set
- **Adaptive column layout**: Render 2-7 columns depending on data
- **1:1 scale-to-column mapping**: Scale N → Column N (no compression)
- **Responsive spacing**: Adjust horizontal spacing based on number of columns

**Implementation**:
```typescript
// REMOVE: Fixed mapping
// const SCALE_TO_LEVEL_MAPPING = {1:1, 3:2, 4:3, 6:4, 7:5};

// ADD: Dynamic calculation
const getOccupiedScales = (nodes: MechanismNode[]): number[] => {
  const scales = new Set(nodes.map(n => n.scale).filter(s => s !== undefined));
  return Array.from(scales).sort((a, b) => a - b);
};

const getNodeLevel = (node: MechanismNode, occupiedScales: number[]): number => {
  if (!node.scale) return occupiedScales.length; // Default to rightmost
  return occupiedScales.indexOf(node.scale) + 1; // 1-indexed for layout
};

// Dynamic numLevels
const occupiedScales = getOccupiedScales(filteredNodes);
const numLevels = occupiedScales.length; // 2-7 depending on data
```

**Layout Changes**:
- Update force simulation `forceX()` to use dynamic `occupiedScales`
- Update badge positioning to show actual scale number (not remapped level)
- Update legend to show occupied scales only

### 3.3 Backend Scale Multiplier Removal

**Requirement**: Remove all scale-based importance weighting

**Files to Update**:
- `backend/api/routes/nodes.py`: Remove `scale_multipliers` dict and all references
- `calculate_composite_score()`: Remove scale multiplier from scoring formula

**Current Code** (REMOVE):
```python
scale_multipliers = {
    1: 1.5,   # Structural
    3: 1.3,   # Institutional
    4: 1.0,   # Individual
    6: 1.1,   # Intermediate
    7: 1.5,   # Crisis
}
```

**New Code** (SIMPLIFIED):
```python
# Composite score based ONLY on:
# 1. Evidence quality (mechanism count, source reliability)
# 2. Centrality (network position)
# NO scale multiplier
def calculate_composite_score(node: NodeWithMetrics) -> float:
    evidence_score = calculate_evidence_score(node)
    centrality_score = calculate_centrality_score(node)
    return (evidence_score * 0.5) + (centrality_score * 0.5)
```

**Rationale**: Scales represent causal structure, not intervention priority. Priority should be data-driven (evidence + network position), not taxonomy-driven.

### 3.4 TypeScript Type Updates

**Files to Update**:
- `frontend/src/types/mechanism.ts`: Update `NodeScale` type

**Current**:
```typescript
export type NodeScale = 1 | 3 | 4 | 6 | 7;
```

**New**:
```typescript
export type NodeScale = 1 | 2 | 3 | 4 | 5 | 6 | 7;
```

**Update All Constants**:
- Scale validation functions
- Scale filter options in UI components
- Badge color mappings (add colors for scales 2 & 5)

### 3.5 Documentation Updates

**Files Requiring Updates** (12+ files):

1. `Nodes/NODE_SYSTEM_DEFINITIONS.md`:
   - Lines 29-33: Change "5 active scales" → "7 active scales"
   - Lines 191-368: Add full definitions for Scales 2 & 5
   - Line 189: REMOVE note about reserved scales
   - Add version history entry

2. `Nodes/COMPLETE_NODE_INVENTORY.md`:
   - Update all 850 node `Scale:` fields
   - Lines 14-77: Restructure to show 7 scales
   - Lines 4702-4717: Update inventory summary

3. `docs/Design/03_SYSTEMS_MAP_VISUALIZATION.md`:
   - Lines 79-88: Add Scale 2 & 5 indicators
   - Lines 92-101: Add badge colors for scales 2 & 5
   - Lines 370-378: Update layout algorithm description
   - Lines 556-567: Add scale 2 & 5 to filter options
   - Lines 791-793: Update legend

4. `docs/Geographic & Contextual Adaptation/09_LLM_TOPOLOGY_DISCOVERY.md`:
   - Lines 160-174: Update from "5 levels" to "7 scales"
   - Standardize terminology: "scale" not "level"

5. `docs/Geographic & Contextual Adaptation/11_LLM_MECHANISM_VALIDATION.md`:
   - Lines 534-537, 587-591: Update level references
   - Standardize terminology: "scale" not "level"

6. `Nodes/NODE_CONSOLIDATION_MAP.md`:
   - Lines 165-243, 596-612: Update scale assignments

7. `.claude/skills/structural-competency.md`:
   - Lines 15-35: Update from old 3-scale taxonomy to new 7-scale system

8. `README.md`, `QUICK_START.md`, `ALCOHOL_EXTRACTION_SUMMARY.md`:
   - Search for any "5 level" or "5 scale" references and update

**Search Pattern**:
```bash
# Find all documentation referencing old scale system
grep -r "5 level" docs/ Nodes/ *.md
grep -r "five level" docs/ Nodes/ *.md
grep -r "5 scale" docs/ Nodes/ *.md
grep -r "Scale 1, 3, 4, 6, 7" docs/ Nodes/
grep -r "reserved.*future" docs/ Nodes/
```

---

## 4. QUALITY REQUIREMENTS

### 4.1 Testing Requirements

**Test-Driven Development (TDD):**
- Write tests BEFORE implementing scale logic changes
- Use test-generator agent to create comprehensive test suites

**Backend Tests** (pytest):
```python
# backend/tests/test_node_scales.py
def test_all_scales_defined():
    """Verify all 7 scales (1-7) are supported"""
    assert set(VALID_SCALES) == {1, 2, 3, 4, 5, 6, 7}

def test_no_scale_multipliers():
    """Ensure scale multipliers are completely removed"""
    # Should not exist in codebase
    with pytest.raises(NameError):
        scale_multipliers  # Should be undefined

def test_composite_score_no_scale_bias():
    """Verify composite score doesn't use scale as input"""
    node1 = create_test_node(scale=1)
    node2 = create_test_node(scale=7)
    # With same evidence and centrality, scores should be equal
    assert calculate_composite_score(node1) == calculate_composite_score(node2)

def test_scale_inference_from_category():
    """Verify category-to-scale mapping includes scales 2 & 5"""
    assert infer_scale_from_category('built_environment') == 2
    assert infer_scale_from_category('behavioral') == 5
```

**Frontend Tests** (Jest + React Testing Library):
```typescript
// frontend/src/tests/visualizations/MechanismGraph.test.tsx
describe('Dynamic Scale Rendering', () => {
  it('renders 7 columns when all scales are present', () => {
    const nodes = createNodesWithScales([1,2,3,4,5,6,7]);
    render(<MechanismGraph nodes={nodes} />);
    expect(screen.getAllByTestId('scale-column')).toHaveLength(7);
  });

  it('renders 3 columns when only scales 1, 4, 7 are present', () => {
    const nodes = createNodesWithScales([1,4,7]);
    render(<MechanismGraph nodes={nodes} />);
    expect(screen.getAllByTestId('scale-column')).toHaveLength(3);
  });

  it('maps nodes to correct columns based on occupied scales', () => {
    const nodes = createNodesWithScales([2,5,7]);
    render(<MechanismGraph nodes={nodes} />);
    // Scale 2 should be in column 1, scale 5 in column 2, scale 7 in column 3
    expect(getNodeColumn(nodes[0])).toBe(1); // Scale 2
    expect(getNodeColumn(nodes[1])).toBe(2); // Scale 5
    expect(getNodeColumn(nodes[2])).toBe(3); // Scale 7
  });
});

describe('Scale Type Validation', () => {
  it('accepts all scales 1-7 as valid NodeScale values', () => {
    [1,2,3,4,5,6,7].forEach(scale => {
      const node: MechanismNode = { ...mockNode, scale: scale as NodeScale };
      expect(() => validateNode(node)).not.toThrow();
    });
  });

  it('rejects scale values outside 1-7', () => {
    const invalidNode = { ...mockNode, scale: 8 as any };
    expect(() => validateNode(invalidNode)).toThrow('Invalid scale');
  });
});
```

**E2E Tests** (Playwright):
```typescript
// frontend/e2e/scale-migration.spec.ts
test('all nodes have scales 1-7', async ({ page }) => {
  await page.goto('/systems-map');
  const response = await page.waitForResponse(resp => resp.url().includes('/api/nodes'));
  const nodes = await response.json();

  nodes.forEach(node => {
    expect(node.scale).toBeGreaterThanOrEqual(1);
    expect(node.scale).toBeLessThanOrEqual(7);
  });
});

test('scale filter includes all 7 options', async ({ page }) => {
  await page.goto('/systems-map');
  await page.click('[data-testid="scale-filter"]');

  for (let i = 1; i <= 7; i++) {
    await expect(page.locator(`text=Scale ${i}`)).toBeVisible();
  }
});
```

### 4.2 Coverage Targets

- **Backend**: >80% line coverage, 100% coverage for scale-related functions
- **Frontend**: >80% line coverage, 100% coverage for scale rendering logic
- **Integration**: Test all 7 scale values in API requests/responses

### 4.3 Performance Requirements

**Lighthouse Scores (unchanged from current):**
- Performance: >90
- Accessibility: >90 (WCAG AA compliance)
- Best Practices: >90
- SEO: >90

**Visualization Performance:**
- 850 nodes should render in <2 seconds
- Force simulation should stabilize in <3 seconds
- No jank when filtering by scale (60 FPS)

### 4.4 Accessibility Requirements (WCAG AA)

- Scale badges must have 4.5:1 contrast ratio
- Scale filter checkboxes must be keyboard navigable
- Screen reader announcements for scale changes
- Color is not the only indicator of scale (use text labels + shapes)

**Color Palette for 7 Scales** (WCAG AA compliant):
```typescript
const SCALE_COLORS = {
  1: '#1e40af', // Blue 800 - Structural
  2: '#047857', // Emerald 700 - Built Environment (NEW)
  3: '#7c3aed', // Violet 600 - Institutional
  4: '#ea580c', // Orange 600 - Individual Conditions
  5: '#dc2626', // Red 600 - Individual Behaviors (NEW)
  6: '#ca8a04', // Yellow 600 - Pathways
  7: '#be123c', // Rose 600 - Crisis
};
```

### 4.5 Security Requirements

- No SQL injection risks (using Pydantic validation)
- No XSS vulnerabilities (React auto-escaping)
- Input validation for scale values (1-7 only)
- Rate limiting on API endpoints (unchanged)

---

## 5. CONSTRAINTS

### 5.1 What to AVOID

**DO NOT:**
- ❌ Change any node IDs (strict migration requirement)
- ❌ Modify mechanism YAML files (mechanisms are scale-agnostic)
- ❌ Add new node fields beyond scale update
- ❌ Change node labels or categories (only update scale)
- ❌ Introduce breaking changes to API contracts
- ❌ Use feature flags or gradual rollout (clean cut migration)
- ❌ Add scale multipliers back in any form
- ❌ Create new visualization layouts (keep force-directed graph)
- ❌ Add emojis to documentation or code

### 5.2 Patterns to FOLLOW

**DO:**
- ✅ Use epidemiology-advisor agent for scientific validation
- ✅ Preserve all existing node metadata (ID, label, category, connections)
- ✅ Use TypeScript strict mode and Pydantic for validation
- ✅ Follow existing code style and conventions
- ✅ Use descriptive commit messages with scope prefixes
- ✅ Document all scale assignment decisions in comments
- ✅ Use parallel tool calls for independent operations
- ✅ Batch similar edits together (all TypeScript type updates in one commit)

### 5.3 Migration Limits

**Scope Boundaries:**
- 850 nodes in `COMPLETE_NODE_INVENTORY.md` (exact count)
- 12 documentation files (no more, no less)
- 4 frontend code files (types, 2 visualizations, utilities)
- 1 backend code file (routes/nodes.py)
- 0 mechanism YAML files (mechanisms are scale-agnostic)

**Timeline:**
- No artificial timeline constraints
- Work autonomously until all quality gates pass
- Prioritize correctness over speed

---

## 6. PROCESS (Autonomous Workflow with Quality Gates)

### PHASE 1: PREPARATION & VALIDATION

**Step 1.1: Inventory Analysis**
```bash
# Read current node inventory
Read: Nodes/COMPLETE_NODE_INVENTORY.md

# Count nodes per scale
Grep: "^\*\*Scale:\*\* [1-7]" in Nodes/COMPLETE_NODE_INVENTORY.md (with count output)

# Expected current distribution: Scale 1 (~130), Scale 3 (~250), Scale 4 (~280), Scale 6 (~150), Scale 7 (~300)
# Expected new distribution: See Feature 3.1
```

**Step 1.2: Documentation Audit**
```bash
# Find all files referencing old scale system
Grep: "5 level|five level|5 scale|Scale 1, 3, 4, 6, 7|reserved.*future" across docs/, Nodes/, *.md
# Generate list of files to update

# Validate list matches expected 12 files
```

**Quality Gate 1:** ✅ All files identified, baseline metrics documented

---

### PHASE 2: NODE RECLASSIFICATION

**Step 2.1: Automated Initial Classification**

For each node, analyze:
- **Current scale**
- **Category** (political, economic, social_environment, built_environment, behavioral, healthcare_access, biological)
- **Label** (descriptive name)

Apply heuristics:
```
IF category == 'political' → likely Scale 1
IF category == 'built_environment' → likely Scale 2
IF category == 'healthcare_access' AND label contains 'infrastructure' → Scale 3
IF category == 'economic' OR 'social_environment' → likely Scale 4
IF category == 'behavioral' → likely Scale 5
IF category == 'healthcare_access' AND label contains 'utilization' → Scale 6
IF category == 'biological' OR label contains 'mortality'/'crisis' → Scale 7
```

**Step 2.2: Epidemiology Advisor Review**

USE epidemiology-advisor agent to validate EVERY node's scale assignment:

```markdown
For each node, ask:
1. Does this node's scale match its causal distance from health outcomes?
2. Is this node correctly positioned on the structural→individual spectrum?
3. Does this align with ecosocial theory principles?
4. Are there any nodes that should be moved to Scale 2 or 5?

Return: List of nodes with incorrect scale assignments and recommended corrections
```

**Step 2.3: Manual Review of Edge Cases**

Focus on:
- Nodes that could fit multiple scales
- Nodes where category doesn't clearly indicate scale
- Nodes at boundaries (e.g., is it Scale 1 or Scale 2?)

**Quality Gate 2:** ✅ All 850 nodes have scales 1-7, distribution is scientifically weighted, epidemiology-advisor approves

---

### PHASE 3: DOCUMENTATION UPDATES

**Step 3.1: Update Core Node Documentation**

PARALLEL EXECUTION (use multiple Edit tools in one message):
```
Edit: Nodes/NODE_SYSTEM_DEFINITIONS.md
  - Add Scale 2 & 5 definitions
  - Remove "reserved" language
  - Update summary to "7 active scales"

Edit: Nodes/COMPLETE_NODE_INVENTORY.md
  - Update all 850 node scale fields
  - Restructure sections for 7 scales
  - Update inventory summary statistics

Edit: Nodes/NODE_CONSOLIDATION_MAP.md
  - Update scale assignments in consolidation records
```

**Step 3.2: Update Design Documentation**

```
Edit: docs/Design/03_SYSTEMS_MAP_VISUALIZATION.md
  - Add Scale 2 & 5 to all scale lists
  - Update badge colors (add 2 new colors)
  - Update layout algorithm description
  - Update legend
```

**Step 3.3: Update LLM Pipeline Documentation**

```
Edit: docs/Geographic & Contextual Adaptation/09_LLM_TOPOLOGY_DISCOVERY.md
  - Change "5 levels" → "7 scales"
  - Standardize terminology

Edit: docs/Geographic & Contextual Adaptation/11_LLM_MECHANISM_VALIDATION.md
  - Update level references to scale references
  - Add Scale 2 & 5 to validation logic
```

**Step 3.4: Update Skills & Other Docs**

```
Edit: .claude/skills/structural-competency.md
  - Replace old 3-scale taxonomy with 7-scale system

# Search and update any remaining references
Grep: "5 level|5 scale" across all *.md files
Edit: Any remaining files with outdated references
```

**Quality Gate 3:** ✅ Zero documentation references to "5 scales" or "reserved scales", all docs use "7 scales"

---

### PHASE 4: BACKEND REFACTORING

**Step 4.1: Remove Scale Multipliers**

```
Read: backend/api/routes/nodes.py

Edit: backend/api/routes/nodes.py
  - REMOVE scale_multipliers dict
  - REMOVE scale multiplier logic from calculate_composite_score()
  - UPDATE infer_scale_from_category() to include scales 2 & 5
  - UPDATE scale validation to accept 1-7
```

**Step 4.2: Generate Backend Tests**

USE test-generator agent:
```
Generate pytest tests for:
- Scale validation (1-7 only)
- No scale multipliers in scoring
- Composite score doesn't use scale as input
- Category-to-scale inference includes 2 & 5
- API returns nodes with scales 1-7

File: backend/tests/test_node_scales.py
```

**Step 4.3: Run Backend Tests**

```bash
pytest backend/tests/test_node_scales.py -v --cov=backend/api/routes/nodes
# Require: >80% coverage, all tests pass
```

**Quality Gate 4:** ✅ All backend tests pass, scale multipliers removed, API accepts scales 1-7

---

### PHASE 5: FRONTEND REFACTORING

**Step 5.1: Update TypeScript Types**

```
Read: frontend/src/types/mechanism.ts

Edit: frontend/src/types/mechanism.ts
  - Change NodeScale type from "1 | 3 | 4 | 6 | 7" to "1 | 2 | 3 | 4 | 5 | 6 | 7"
  - Update comments to reference 7 scales
```

**Step 5.2: Refactor Visualization Components**

```
Read: frontend/src/visualizations/MechanismGraph.tsx

Edit: frontend/src/visualizations/MechanismGraph.tsx
  - REMOVE SCALE_TO_LEVEL_MAPPING constant
  - ADD getOccupiedScales() function
  - UPDATE getNodeLevel() to use dynamic scale mapping
  - UPDATE numLevels calculation to be dynamic
  - UPDATE forceX() to use occupiedScales
  - UPDATE badge rendering to show actual scale numbers

Read: frontend/src/visualizations/AlcoholismSystemDiagram.tsx

Edit: frontend/src/visualizations/AlcoholismSystemDiagram.tsx
  - Apply same changes as MechanismGraph.tsx
```

**Step 5.3: Add Scale 2 & 5 Colors**

```
Read: frontend/src/utils/colors.ts

Edit: frontend/src/utils/colors.ts
  - ADD colors for scales 2 & 5 to SCALE_COLORS
  - Ensure WCAG AA contrast compliance
```

**Step 5.4: Update Mock Data**

```
Edit: frontend/src/tests/mocks/mockData.ts
  - Add nodes with scales 2 & 5 to mock data
  - Ensure test data covers all 7 scales

Edit: frontend/src/data/mockData.ts
  - Update mock nodes to use all 7 scales
```

**Step 5.5: Generate Frontend Tests**

USE test-generator agent:
```
Generate Jest + React Testing Library tests for:
- Dynamic scale rendering (2-7 columns)
- Correct column mapping based on occupied scales
- Scale type validation (1-7 only)
- Badge colors for all 7 scales
- Filter options include all 7 scales

Files:
- frontend/src/tests/visualizations/MechanismGraph.test.tsx
- frontend/src/tests/visualizations/AlcoholismSystemDiagram.test.tsx
- frontend/src/tests/types/mechanism.test.ts
```

**Step 5.6: Run Frontend Tests**

```bash
cd frontend
npm test -- --coverage --watchAll=false
# Require: >80% coverage, all tests pass
```

**Quality Gate 5:** ✅ All frontend tests pass, visualization renders dynamically, types accept scales 1-7

---

### PHASE 6: INTEGRATION TESTING

**Step 6.1: Generate E2E Tests**

USE test-generator agent:
```
Generate Playwright E2E tests for:
- All nodes have scales 1-7 (no nulls or invalid values)
- Scale filter shows all 7 options
- Filtering by each scale works correctly
- Visualization renders correct number of columns
- Node badges show correct scale numbers

File: frontend/e2e/scale-migration.spec.ts
```

**Step 6.2: Run E2E Tests**

```bash
cd frontend
npx playwright test e2e/scale-migration.spec.ts
# All tests must pass
```

**Step 6.3: Run Full Test Suite**

```bash
# Backend
pytest --cov=backend --cov-report=term-missing

# Frontend
cd frontend && npm test -- --coverage --watchAll=false

# E2E
npx playwright test

# Require: ALL tests pass, >80% coverage
```

**Quality Gate 6:** ✅ Full test suite passes, E2E tests validate migration success

---

### PHASE 7: VALIDATION & REVIEW

**Step 7.1: Mechanism Validation**

USE mechanism-validator agent:
```
Validate all 75+ mechanism YAML files:
- Ensure node_id references are still valid
- Check for any scale-specific logic (there shouldn't be any)
- Verify mechanism categories are consistent

Return: Report of any issues found
```

**Step 7.2: Code Review**

USE code-reviewer agent:
```
Review all code changes:
- Backend: routes/nodes.py
- Frontend: types, visualizations, utilities
- Test files

Check for:
- Code quality and best practices
- Security vulnerabilities
- Performance issues
- Accessibility compliance (WCAG AA)
- TypeScript strict mode compliance

Return: List of required changes before merge
```

**Step 7.3: Documentation Consistency Check**

```bash
# Verify zero references to old system
Grep: "5 level|five level|5 scale|reserved.*future|Scale 1, 3, 4, 6, 7" across all files
# Expected: Zero matches (except in version history or changelog)

# Verify all docs reference 7 scales
Grep: "7 scale|seven scale" across docs/
# Expected: Multiple matches in all updated docs
```

**Quality Gate 7:** ✅ Code review approved, mechanism validation passed, documentation 100% consistent

---

### PHASE 8: DEPLOYMENT READINESS

**Step 8.1: Build Verification**

```bash
# Backend
cd backend && python -m pytest

# Frontend
cd frontend && npm run build
# Build must succeed with zero errors
```

**Step 8.2: Performance Testing**

```bash
# Run Lighthouse on built app
cd frontend && npm run preview
# Open in browser, run Lighthouse
# Require: All scores >90
```

**Step 8.3: Final Checklist**

- [ ] All 850 nodes have scales 1-7 (no nulls)
- [ ] Node distribution is scientifically weighted
- [ ] Epidemiology-advisor validated all assignments
- [ ] All 12+ documentation files updated
- [ ] Backend scale multipliers removed
- [ ] Frontend renders dynamic columns
- [ ] TypeScript types accept scales 1-7
- [ ] All tests pass (backend, frontend, E2E)
- [ ] Test coverage >80%
- [ ] Code review approved
- [ ] Mechanism validation passed
- [ ] Build succeeds with zero errors
- [ ] Lighthouse scores >90
- [ ] Zero breaking changes to API
- [ ] All node IDs preserved

**Quality Gate 8:** ✅ ALL checklist items checked, deployment ready

---

## 7. DELIVERABLES

### 7.1 Updated Data Files

**File: `Nodes/COMPLETE_NODE_INVENTORY.md`**
- 850 nodes with updated scale assignments (all values 1-7)
- Restructured to show 7 scale sections
- Updated inventory summary statistics
- Distribution report showing node counts per scale

**File: `Nodes/NODE_SYSTEM_DEFINITIONS.md`**
- Full definitions for all 7 scales
- Scale 2 and Scale 5 definitions added
- "Reserved" language removed
- Examples for each scale
- Version history updated

### 7.2 Updated Code Files

**Backend:**
- `backend/api/routes/nodes.py`:
  - Scale multipliers removed
  - `calculate_composite_score()` simplified
  - `infer_scale_from_category()` includes scales 2 & 5
  - Scale validation accepts 1-7
- `backend/tests/test_node_scales.py`: Comprehensive test suite

**Frontend:**
- `frontend/src/types/mechanism.ts`: NodeScale type updated to include 2 & 5
- `frontend/src/visualizations/MechanismGraph.tsx`: Dynamic scale rendering
- `frontend/src/visualizations/AlcoholismSystemDiagram.tsx`: Dynamic scale rendering
- `frontend/src/utils/colors.ts`: Scale 2 & 5 colors added
- `frontend/src/tests/`: Comprehensive test suites
- `frontend/e2e/scale-migration.spec.ts`: E2E validation tests

### 7.3 Updated Documentation Files

**Core Documentation (12+ files):**
1. `Nodes/NODE_SYSTEM_DEFINITIONS.md`
2. `Nodes/COMPLETE_NODE_INVENTORY.md`
3. `Nodes/NODE_CONSOLIDATION_MAP.md`
4. `docs/Design/03_SYSTEMS_MAP_VISUALIZATION.md`
5. `docs/Geographic & Contextual Adaptation/09_LLM_TOPOLOGY_DISCOVERY.md`
6. `docs/Geographic & Contextual Adaptation/11_LLM_MECHANISM_VALIDATION.md`
7. `.claude/skills/structural-competency.md`
8. Any additional files found with "5 scale" references

**All files updated to:**
- Reference "7 scales" instead of "5 scales"
- Remove "reserved for future" language
- Include Scale 2 & 5 in all examples and references
- Use consistent terminology ("scale" not "level")

### 7.4 Test Reports

**Backend Test Report:**
```
pytest --cov=backend/api/routes/nodes --cov-report=html
Coverage: >80%
All tests passing: ✓
File: backend/htmlcov/index.html
```

**Frontend Test Report:**
```
npm test -- --coverage --coverageReporters=html
Coverage: >80%
All tests passing: ✓
File: frontend/coverage/index.html
```

**E2E Test Report:**
```
npx playwright test --reporter=html
All tests passing: ✓
File: frontend/playwright-report/index.html
```

### 7.5 Validation Reports

**Epidemiology Advisor Report:**
- Scientific validation of all 850 node assignments
- Justification for Scale 2 & 5 placement decisions
- Any nodes flagged for manual review
- Final approval sign-off

**Mechanism Validator Report:**
- Validation of all 75+ mechanism YAML files
- Confirmation that no mechanisms broken by scale changes
- List of any warnings or issues (expected: none)

**Code Review Report:**
- Security review (no vulnerabilities found)
- Performance review (no regressions)
- Accessibility review (WCAG AA compliance maintained)
- Best practices review (all standards met)

### 7.6 Distribution Analysis

**Node Distribution Report:**
```markdown
# Final Scale Distribution (850 nodes total)

| Scale | Count | % of Total | Category                          |
|-------|-------|------------|-----------------------------------|
| 1     | 85    | 10%        | Structural Determinants           |
| 2     | 175   | 21%        | Built Environment & Structural    |
| 3     | 190   | 22%        | Institutional Infrastructure      |
| 4     | 225   | 26%        | Individual/Household Conditions   |
| 5     | 90    | 11%        | Individual Behaviors & Psychosocial|
| 6     | 50    | 6%         | Intermediate Pathways             |
| 7     | 35    | 4%         | Crisis Endpoints                  |

**Scientific Weighting Achieved:**
- Upstream scales (1-3): 53% of nodes (preventative leverage)
- Midstream scales (4-5): 37% of nodes (proximal conditions & behaviors)
- Downstream scales (6-7): 10% of nodes (pathways & outcomes)

**Causal Distance Distribution:**
- Long latency (1-3): 450 nodes (most upstream)
- Medium latency (4-5): 315 nodes (bridging context to biology)
- Short latency (6-7): 85 nodes (proximal to outcomes)
```

### 7.7 Migration Summary Document

**File: `SCALE_MIGRATION_SUMMARY.md`**

Contents:
- Summary of changes (5 scales → 7 scales)
- Rationale for Scale 2 & 5 definitions
- Before/after distribution comparison
- List of all updated files
- Test results and coverage reports
- Performance impact analysis (none expected)
- Breaking changes (none)
- Rollback plan (git revert if needed)
- Next steps (monitor in production, gather user feedback)

---

## SUCCESS CRITERIA SUMMARY

**The migration is successful when:**

1. ✅ **Data Integrity**: All 850 nodes have valid scales (1-7), no nulls or invalid values
2. ✅ **Scientific Validity**: Epidemiology-advisor validates all scale assignments as scientifically sound
3. ✅ **Distribution**: Node counts per scale follow scientifically-weighted distribution (more nodes at scales 2-4)
4. ✅ **Documentation**: 100% of documentation updated to reference 7 scales, zero references to "5 scales" or "reserved scales"
5. ✅ **Code Quality**: All tests pass (backend, frontend, E2E), coverage >80%
6. ✅ **No Regressions**: Mechanism YAML files unchanged and valid, API contracts unchanged, visualization performance maintained
7. ✅ **Scale Multipliers**: Completely removed from codebase, scoring is scale-agnostic
8. ✅ **Visualization**: Frontend dynamically renders 2-7 columns based on occupied scales
9. ✅ **Accessibility**: WCAG AA compliance maintained, new scale colors have sufficient contrast
10. ✅ **Build Success**: Both backend and frontend build with zero errors
11. ✅ **Performance**: Lighthouse scores remain >90 (no degradation)
12. ✅ **Review Approval**: Code-reviewer agent approves all changes

**No success until ALL criteria are met.**

---

## AGENT USAGE SUMMARY

**Use these specialized agents throughout the workflow:**

1. **epidemiology-advisor**: Validate every scale assignment for scientific accuracy (Phase 2)
2. **mechanism-validator**: Validate mechanism YAML integrity (Phase 7)
3. **test-generator**: Generate comprehensive test suites (Phases 4, 5, 6)
4. **code-reviewer**: Review all code changes for quality, security, performance (Phase 7)

**Use these tools for efficiency:**
- **Parallel Edit calls**: Update multiple documentation files simultaneously
- **Grep with count**: Quickly audit scale distribution
- **WebSearch**: Look up latest D3.js, React, FastAPI patterns if needed

---

## FINAL NOTES

**This is a STRICT MIGRATION:**
- All node IDs preserved (no deletions, no additions)
- Only scale field updated
- No feature flags or gradual rollout
- Clean cut: old system → new system in one PR

**This is NOT a feature addition:**
- Don't add new nodes
- Don't modify mechanism definitions
- Don't change visualization types
- Don't add new API endpoints

**This is a REFACTORING for scientific accuracy:**
- Goal: Better represent causal pathways from structural determinants to health outcomes
- Outcome: 7-scale taxonomy that aligns with ecosocial theory
- Impact: More accurate intervention targeting based on causal distance

**Work autonomously, follow quality gates, leverage all agents, and deliver a scientifically-validated migration that maintains 100% backwards compatibility (except for the intentional scale field updates).**

---

END OF COMPREHENSIVE PROMPT
