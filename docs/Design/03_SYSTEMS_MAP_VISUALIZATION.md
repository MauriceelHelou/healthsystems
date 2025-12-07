# Interactive Systems Map Visualization
**HealthSystems Platform - Network Graph Specification**

Version: 1.1
Last Updated: 2025-11-19
Status: MVP Scope (Topology & Direction Only)

---

## Overview

This document specifies the visual design and interaction patterns for the core network visualization - an interactive systems map showing 400 nodes and 2000+ mechanisms. The design prioritizes clarity, explorable complexity, and qualitative understanding of health system relationships.

**Key Constraint**: MVP shows topology and direction only. No quantified effect sizes, confidence intervals, or numerical projections on the visualization.

---

## 1. Visualization Philosophy

### Design Principles
1. **Clarity at Scale**: Readable with 400 nodes, navigable to individual mechanisms
2. **Category Intuition**: Color coding makes domain patterns immediately visible
3. **Direction Matters**: Visual language clearly shows causal direction (+/-)
4. **Evidence Transparency**: Quality indicators visible but not overwhelming
5. **Interactive Exploration**: Click, hover, zoom, filter - multi-modal discovery

### Visual Language Goals
- **At a glance**: Understand network structure, identify clusters
- **On hover**: See node/edge metadata, connections
- **On click**: Deep dive into mechanisms, evidence, pathways
- **On filter**: Isolate subnetworks, trace interventions

---

## 2. Node Visual Design

### Base Node Appearance

```
     Category Color (80% opacity)
           ↓
        ┌─────┐
        │     │  ← Stroke: 2px, darker shade
        │  •  │  ← Label (on zoom)
        │     │
        └─────┘
           ↑
     Radius = √(weight) × scale
```

**Shape**: Circle (consistent across all node types)
**Default Radius**: 8-40px (based on connection weight)
**Calculation**: `radius = Math.sqrt(node.weight) * 20`

### Node Size Encoding

| Weight (# Connections) | Radius | Visual Importance |
|------------------------|--------|-------------------|
| 1-5 | 8-12px | Peripheral nodes |
| 6-15 | 14-20px | Standard nodes |
| 16-30 | 22-30px | Important hubs |
| 31+ | 32-40px | Critical hubs |

**Rationale**: Square root scaling prevents extreme size differences, keeps all nodes visible

### Node Color by Category

| Category | Fill Color | Stroke Color | Opacity |
|----------|-----------|--------------|---------|
| **Built Environment** | `#0369a1` (blue) | `#1e3a8a` (darker blue) | 80% |
| **Social Environment** | `#9333ea` (purple) | `#6b21a8` (darker purple) | 80% |
| **Economic** | `#059669` (green) | `#065f46` (darker green) | 80% |
| **Political** | `#dc2626` (red) | `#991b1b` (darker red) | 80% |
| **Biological** | `#ea580c` (orange) | `#9a3412` (darker orange) | 80% |
| **Default/Mixed** | `#6b7280` (gray) | `#374151` (darker gray) | 80% |

### Node Scale Indicators

Nodes are labeled with a **1-5 scale** indicating their position in the causal hierarchy. All node IDs reference `mechanism-bank/mechanisms/canonical_nodes.json`.

**Scale Values** (with canonical node examples):
- **Scale 1**: Structural Policy (e.g., `medicaid_expansion_status`, `rent_control_stabilization_policy_strength`, `minimum_wage_level`)
- **Scale 2**: Institutional Infrastructure (e.g., `primary_care_physician_density`, `emergency_department_availability`, `eviction_legal_aid_availability`)
- **Scale 3**: Individual/Household Conditions (e.g., `uninsured_rate`, `housing_cost_burden`, `eviction_filing_rate`)
- **Scale 4**: Intermediate Pathways (e.g., `primary_care_visit_rate`, `just_cause_eviction_protection`, `mental_healthcare_access`)
- **Scale 5**: Crisis Endpoints (e.g., `emergency_department_visit_rate`, `asthma_hospitalization_rate`, `all_cause_mortality_rate`)

**Visual Representation Options:**

1. **Badge with Scale Number**
   - Badge: Small circular badge (top-right of node)
   - Content: Scale number (1-5) in white text
   - Background color based on scale:
     - Scale 1: `#1e40af` (dark blue) - Structural Policy
     - Scale 2: `#7c3aed` (purple) - Institutional
     - Scale 3: `#059669` (green) - Individual/Household
     - Scale 4: `#ea580c` (orange) - Intermediate
     - Scale 5: `#dc2626` (red) - Crisis Endpoints

2. **Crisis Endpoint Special Treatment** (Scale 5)
   - Additional alert triangle icon
   - Thicker stroke (3px)
   - Higher visual prominence
   - Examples: `emergency_department_visit_rate`, `all_cause_mortality_rate`

**Badge Positioning**:
```
    ┌─────┐
    │   [7]│  ← Badge (14px diameter, scale number)
    │  •  │
    │     │
    └─────┘
```

### Node Labels

**Default State** (Zoom < 0.8):
- No labels (too cluttered)
- Tooltip on hover

**Zoomed State** (Zoom ≥ 0.8):
- Label below node
- Font: 11px, medium weight
- Color: gray-700
- Max width: 100px, truncate with ellipsis
- Background: Semi-transparent white (70% opacity) for readability

**Label Positioning**:
```
    ┌─────┐
    │  •  │
    └─────┘
  Community Health...  ← Label (11px, truncated)
```

### Node State Variations

#### Default State
```css
fill: category-color (80% opacity)
stroke: darker-shade (2px)
cursor: pointer
filter: none
```

#### Hover State
```css
fill: category-color (100% opacity)
stroke: primary-600 (3px)
cursor: pointer
filter: drop-shadow(0 2px 4px rgba(0,0,0,0.2))
scale: 1.1
transition: 150ms ease-out
```

#### Selected State
```css
fill: category-color (100% opacity)
stroke: primary-600 (4px)
filter: drop-shadow(0 4px 8px rgba(0,0,0,0.3))
ring: 2px primary-500, offset 2px (outside stroke)
```

#### Connected State (when path is active)
```css
fill: category-color (100% opacity)
stroke: darker-shade (2px)
opacity: 1
```

#### Dimmed State (filtered out)
```css
fill: gray-300 (30% opacity)
stroke: gray-400 (1px)
opacity: 0.3
transition: 200ms ease-in-out
```

#### Focus State (keyboard navigation)
```css
stroke: primary-500 (3px)
ring: 2px primary-500, offset 4px
outline: none (custom ring replaces default)
```

---

## 3. Edge (Link) Visual Design

### Base Edge Appearance

```
Node A ────────────────────────> Node B
       │                        ↑
     Color: Source             Arrow: Direction
     Width: 1-3px              Marker: 8px triangle
     Opacity: 40-100%
```

**Shape**: Curved line (bezier) for readability, straight for short distances
**Direction**: Arrow marker at target end
**Color**: Matches source node category color

### Edge Width Encoding

**NOT Effect Size** (MVP constraint), but relational strength:

| Strength | Width | Meaning |
|----------|-------|---------|
| Weak | 1px | Single mechanism, low evidence |
| Moderate | 2px | Multiple mechanisms or moderate evidence |
| Strong | 3px | Multiple mechanisms AND high evidence |

**Calculation**:
```javascript
edgeWidth = Math.min(3, 1 + (mechanism_count * 0.5))
```

### Edge Color

**Matches Source Node Category** (where mechanism originates):
- Built Environment → Blue edges
- Social Environment → Purple edges
- Economic → Green edges
- Political → Red edges
- Biological → Orange edges

**Opacity**: 40% (default), increases on hover/selection

### Direction Indicator (Arrow)

**Arrow Marker** (SVG):
```svg
<marker id="arrow" markerWidth="8" markerHeight="8"
        refX="4" refY="4" orient="auto">
  <path d="M 0,0 L 8,4 L 0,8 Z" fill="currentColor" />
</marker>
```

**Positioning**: At target node (destination)
**Size**: 8px triangle
**Color**: Same as edge color

### Direction Type Indicators

**Positive Relationship** (+):
- Arrow: Solid triangle
- Tooltip: "Increase in [source] → Increase in [target]"

**Negative Relationship** (-):
- Arrow: Solid triangle with red tint overlay
- Additional marker: Small minus sign near arrow
- Tooltip: "Increase in [source] → Decrease in [target]"

**Bidirectional** (feedback loop):
- Two arrows (one each direction)
- Slightly curved to show both
- Color may differ if categories differ

### Edge State Variations

#### Default State
```css
stroke: source-category-color
stroke-width: 1-3px (based on strength)
opacity: 0.4
cursor: pointer
```

#### Hover State
```css
stroke: source-category-color
stroke-width: +1px (increase by 1)
opacity: 0.8
cursor: pointer
filter: drop-shadow(0 1px 2px rgba(0,0,0,0.1))
```

#### Selected/Active Path State
```css
stroke: primary-600 or source-category-color (enhanced)
stroke-width: 3px
opacity: 1.0
animation: dash-flow 2s linear infinite (optional)
```

**Animated Flow** (for active paths):
```css
stroke-dasharray: 5, 5
animation: dash-flow 1.5s linear infinite

@keyframes dash-flow {
  from { stroke-dashoffset: 0 }
  to { stroke-dashoffset: 10 }
}
```

#### Dimmed State (filtered out)
```css
stroke: gray-300
stroke-width: 1px
opacity: 0.15
pointer-events: none
```

---

## 4. Evidence Quality Indicators

### Badge Display on Edges

**Position**: Midpoint of edge
**Appearance**: Small circular badge (16px diameter)

```
Node A ─────[A]──────────> Node B
             ↑
        Evidence badge
        (Green for A, Amber for B, Red for C)
```

**Badge Design**:
- Circle: 16px diameter
- Background: White with border
- Border: 2px, evidence-quality color
- Text: Single letter (A/B/C), 10px bold
- Color: Matches border color

**Evidence Colors** (from Design System):
- **A**: `#10b981` (green) - High quality
- **B**: `#f59e0b` (amber) - Moderate quality
- **C**: `#ef4444` (red) - Low quality
- **?**: `#9ca3af` (gray) - No rating/unknown

### Multi-Mechanism Edges

If multiple mechanisms share the same source→target:
- Edge width increases (up to 3px max)
- Badge shows aggregate quality:
  - If any A: show A
  - Else if any B: show B
  - Else: show C
- Tooltip shows "3 mechanisms (2A, 1B)"
- Click edge → panel lists all mechanisms

---

## 5. Layout Algorithm

### Force-Directed Graph (D3.js)

**Algorithm**: D3 force simulation with custom constraints

**Forces**:
1. **Link Force**: Pulls connected nodes together
   - Strength: 0.3
   - Distance: 100px (default)

2. **Charge Force**: Repels all nodes from each other
   - Strength: -300 (moderate repulsion)
   - Prevents overlap

3. **Center Force**: Pulls nodes toward canvas center
   - Strength: 0.05 (gentle)

4. **Collision Force**: Prevents node overlap
   - Radius: node.radius + 5px padding

**Custom Constraints**:
- **Category Clustering**: Slight attraction within same category (optional)
- **Scale Layering**: Tendency to position nodes by scale (Scale 1 → Scale 7, left to right or top to bottom)
  - Scale 1 (Structural) → leftmost/topmost
  - Scale 3 (Institutional) → mid-left
  - Scale 4 (Individual) → center
  - Scale 6 (Intermediate) → mid-right
  - Scale 7 (Crisis) → rightmost/bottommost
- **Boundary**: Keep nodes within viewport bounds

### Initial Layout

**Options**:
1. **Random**: Fast, good for exploration
2. **Clustered**: Pre-group by category before force simulation
3. **Hierarchical**: Structural top, outcomes bottom (for pathway view)

**Recommended**: Random with force simulation, stabilizes after ~2 seconds

### Performance Optimization

**400 nodes, 2000 edges** is computationally intensive:

**Strategies**:
1. **Limit Simulation Iterations**: 300 ticks max
2. **Alpha Decay**: Faster cooldown (0.03)
3. **Static Nodes**: Allow dragging to "pin" nodes (disable force)
4. **LOD (Level of Detail)**:
   - Zoomed out: Simplify edge rendering (no curves)
   - Zoomed in: Full detail with labels
5. **Virtualization**: Only render visible nodes/edges (viewport culling)

---

## 6. Zoom and Pan Controls

### Zoom Levels

| Zoom | Scale | Visibility | Interaction |
|------|-------|------------|-------------|
| **Far** | 0.2-0.5 | Overview, no labels | Category clusters |
| **Default** | 0.8-1.0 | Structure visible, some labels | Click nodes |
| **Close** | 1.2-2.0 | Labels, details | Read labels, click edges |
| **Very Close** | 2.5-4.0 | Individual mechanisms | Detailed inspection |

**Limits**:
- Min Zoom: 0.2 (prevent infinite shrink)
- Max Zoom: 4.0 (prevent pixelation)

### Zoom Behavior

**Mouse Wheel**: Zoom in/out centered on cursor
**Pinch Gesture** (touch): Zoom at touch midpoint
**Zoom Buttons**: Zoom at canvas center
**Double Click**: Zoom to node (center and zoom to 1.5x)

### Pan Behavior

**Click + Drag** (on empty space): Pan canvas
**Touch + Drag**: Pan canvas
**Arrow Keys**: Pan 50px in direction
**Scroll Bars**: Optional (prefer drag panning)

### Fit to Screen

**Button Action**: "Fit All Nodes"
**Behavior**:
- Calculate bounding box of all visible nodes
- Set zoom to fit box + 10% padding
- Center box in viewport
- Animate transition (400ms ease-in-out)

---

## 7. Interactive Behaviors

### Hover Interactions

#### Hover on Node
**Visual**:
- Node: Hover state (enlarged, highlighted stroke)
- Connected edges: Increase opacity to 60%
- Other nodes: Slight dim to 70% opacity

**Tooltip** (appears after 300ms):
```
┌─────────────────────────────────┐
│ Community Health Workers        │
│ Scale: 3 (Institutional)        │
│ Category: Built Environment     │
│ Connections: 15 outgoing, 3 in  │
└─────────────────────────────────┘
```

#### Hover on Edge
**Visual**:
- Edge: Hover state (thicker, more opaque)
- Connected nodes: Highlight
- Evidence badge: Expand to show details

**Tooltip**:
```
┌─────────────────────────────────────┐
│ CHWs → Healthcare Continuity Index  │
│ Direction: Positive (+)             │
│ Evidence: A (12 studies)            │
│ Click to view mechanism details     │
└─────────────────────────────────────┐
```

### Click Interactions

#### Click Node
**Action**: Select node, open detail panel
**Visual**:
- Node: Selected state
- Panel: Slide in from right with node details
- Focus: Move to panel (keyboard navigation)

#### Click Edge
**Action**: Open mechanism detail panel
**Content**: Mechanism description, evidence, citations

#### Click Empty Space
**Action**: Deselect current selection
**Visual**:
- Close detail panel (if open)
- Return all nodes/edges to default state

### Drag Interactions

#### Drag Node
**Behavior**:
- Node follows cursor
- Force simulation pauses for that node
- Connected edges stretch/redraw
- Release: Node "pins" at new location (optional)
- Double-click pinned node: Unpin (resume simulation)

**Visual Feedback**:
- Cursor: Grab hand during drag
- Node: Slightly translucent during drag
- Drop shadow increases

### Multi-Select

**Modifier Key**: Shift + Click
**Behavior**:
- Select multiple nodes
- All selected nodes highlighted
- Panel shows comparison or bulk actions
- Click empty space: Clear selection

---

## 8. Filtering and Search

### Category Filter

**UI**: Legend (bottom-left), clickable category pills

**Behavior**:
```
[Built Env] [Social] [Economic] [Political] [Biological] [Default]
   (active)  (active)   (dim)     (active)    (active)    (active)

When Economic is clicked (deactivated):
- Economic nodes → Dimmed state (30% opacity)
- Edges from/to economic nodes → Dimmed
- Other nodes/edges → Full visibility
```

**Multi-Select**: Click multiple categories to isolate subnetwork

### Evidence Quality Filter

**UI**: Filter panel (sidebar or dropdown)

**Options**:
- [ ] Show only A-quality mechanisms
- [ ] Show A + B quality
- [ ] Show all (default)

**Behavior**: Dim edges that don't meet quality threshold

### Node Scale Filter

**UI**: Checkboxes in filter panel

**Options**:
- [x] Scale 1 (Structural Policy)
- [x] Scale 3 (Institutional)
- [x] Scale 4 (Individual/Household)
- [x] Scale 6 (Intermediate Pathways)
- [x] Scale 7 (Crisis Endpoints)

**Behavior**: Hide/show nodes by scale level
**Use Case**: Focus on specific levels of the system (e.g., only show structural and crisis endpoints to see macro-level pathways)

### Search Function

**UI**: Search bar (top-right controls)
**Trigger**: Click search icon, or `Cmd/Ctrl + K`

**Input**: Text field with autocomplete
**Matching**:
- Node names (fuzzy search)
- Mechanism descriptions
- Evidence keywords

**Results**:
- Highlight matching nodes (pulse animation)
- Dim non-matching nodes
- List results in sidebar panel
- Arrow keys navigate results
- Enter selects result

**Example**:
```
Search: "housing"
→ Highlights: "Affordable Housing Units", "Housing Stability Index"
→ Dims all other nodes
→ Sidebar lists matches with "View" buttons
```

---

## 9. Pathway Highlighting

### Use Case: Trace Intervention → Outcome

**User Action**:
1. Select intervention node (e.g., "Community Health Workers")
2. Select outcome node (e.g., "ED Visits")
3. Click "Find Paths" or right-click → "Trace to..."

**Visual Response**:
```
  [CHW] ──────────────> [Continuity Index] ──────> [ED Visits]
  (green)   (bold, 100%)       (green)      (bold)   (red alert)
    ↓
    └───> [Trust Index] ──────────────────> [ED Visits]
            (bold, 100%)                      (red alert)

  All other nodes/edges: Dimmed to 20% opacity
```

**Path Highlighting**:
- **Nodes in path**: Full opacity, Selected state
- **Edges in path**: Bold (3px), full opacity, animated flow
- **Other elements**: Dimmed (20% opacity)
- **Multiple paths**: Different color per path (optional) or numbered badges

**Panel Display**: List all paths with quality scores

---

## 10. Accessibility Considerations

### Keyboard Navigation

**Tab Order**:
1. Zoom controls
2. Filter controls
3. Search field
4. Graph nodes (enter graph context)
5. Graph edges (when node selected)

**Arrow Key Navigation** (when focus is on graph):
- **Arrow Keys**: Move focus to adjacent node (follow edges)
- **Enter/Space**: Select focused node
- **Shift + Arrow**: Extend selection (multi-select)
- **Escape**: Exit graph focus, return to controls

**Visual Focus**:
- Focused node: Blue ring (2px, 4px offset)
- Focused edge: Dashed outline

### Screen Reader Support

**Graph Announcement**:
```html
<div role="img" aria-label="Systems map with 400 nodes and 2000 mechanisms">
  <svg>...</svg>
</div>
```

**Node Announcement** (on focus):
```
"Community Health Workers, Scale 3 Institutional, Built Environment category.
15 outgoing connections, 3 incoming connections. Press Enter to view details."
```

**Edge Announcement**:
```
"Mechanism: Community Health Workers increases Healthcare Continuity Index.
Evidence quality: A. Press Enter for details."
```

**Alternative View**: Provide table/list view (Node Library tab) for non-visual exploration

### Color Blindness

**Deuteranopia/Protanopia** (red-green blindness):
- Don't rely solely on red vs. green
- Use shapes/icons in addition to colors
- Ensure all categories distinguishable by hue AND saturation

**Test**: Use ColorOracle or browser dev tools to simulate

**Patterns** (optional enhancement):
- Add texture patterns to nodes (stripes, dots) in addition to color
- Icons for positive/negative direction (not just color)

### High Contrast Mode

**Support** `prefers-contrast: high`:
```css
@media (prefers-contrast: high) {
  .node {
    stroke-width: 3px; /* Thicker borders */
    opacity: 1; /* Full opacity */
  }
  .edge {
    stroke-width: 2px;
    opacity: 0.8;
  }
}
```

---

## 11. Performance Optimizations

### 400 Nodes, 2000 Edges - Optimization Strategies

#### 1. Canvas Rendering (not SVG)
**Consideration**: D3 with SVG struggles at this scale
**Alternative**: Use Canvas API or WebGL for rendering
- **Pros**: Much faster, 60fps possible
- **Cons**: More complex hit detection, less accessible

**Recommendation**: Hybrid approach
- Canvas for graph rendering (performance)
- SVG overlay for interactivity (tooltips, selection)
- React-managed UI components

#### 2. Viewport Culling
**Technique**: Only render nodes/edges within current viewport + buffer

```javascript
const isInViewport = (node, viewport, buffer = 100) => {
  return (
    node.x >= viewport.x - buffer &&
    node.x <= viewport.x + viewport.width + buffer &&
    node.y >= viewport.y - buffer &&
    node.y <= viewport.y + viewport.height + buffer
  )
}

// Only render visible nodes
visibleNodes = allNodes.filter(n => isInViewport(n, currentViewport))
```

**Impact**: Reduces render from 400→~50-100 nodes typical

#### 3. Level of Detail (LOD)
**Zoom-Based Rendering**:

| Zoom Level | Nodes | Edges | Labels | Evidence Badges |
|------------|-------|-------|--------|-----------------|
| <0.5 | Simple circles | Straight lines | No | No |
| 0.5-1.0 | Full style | Curved | No | No |
| 1.0-2.0 | Full style | Full style | Yes | Yes |
| >2.0 | Full detail | Full detail | Full | Full |

#### 4. Debounced Interactions
**Hover Tooltips**: 300ms delay before showing
**Zoom/Pan**: Throttle redraw to 60fps max
**Search**: Debounce input (200ms) before filtering

#### 5. Memoization (React)
```javascript
const MemoizedNode = React.memo(Node, (prev, next) => {
  return (
    prev.x === next.x &&
    prev.y === next.y &&
    prev.selected === next.selected
  )
})
```

#### 6. Web Workers
**Force Simulation**: Run in background thread
- Main thread: Rendering and interaction
- Worker: Physics calculations
- Message passing: Updated positions

---

## 12. Legend Component

### Position and Layout

**Location**: Bottom-left, 16px margin from edges
**Style**: Glass-morphism effect (semi-transparent, backdrop blur)

```
┌─────────────────────────────────────────────────────┐
│ Legend                                      [Hide]  │
├─────────────────────────────────────────────────────┤
│ Categories                                          │
│ ● Built Environment   ● Social      ● Economic     │
│ ● Political           ● Biological  ● Default      │
├─────────────────────────────────────────────────────┤
│ Evidence Quality                                    │
│ [A] High  [B] Moderate  [C] Low  [?] Unknown       │
├─────────────────────────────────────────────────────┤
│ Direction                                           │
│ → Positive  ⊖→ Negative  ↔ Bidirectional          │
├─────────────────────────────────────────────────────┤
│ Node Scale (1-7)                                    │
│ [1] Structural  [3] Institutional  [4] Individual  │
│ [6] Intermediate  [7] Crisis                       │
└─────────────────────────────────────────────────────┘
```

### Interactive Legend

**Behavior**:
- Click category → Filter (dim others)
- Click evidence badge → Filter by quality
- Click direction → Highlight all of that type
- Hover → Preview effect without committing

**State Indicator**:
- Active filters: Highlighted (bold, blue border)
- Inactive: Gray, 60% opacity
- Disabled: Gray, 30% opacity, cursor: not-allowed

### Collapsible

**Collapsed State**: Icon-only version
```
┌─────┐
│ [≡] │  ← Click to expand
└─────┘
```

**Preference**: Remember user's collapsed/expanded choice (localStorage)

---

## 13. Export and Sharing

### Export Current View

**Button**: "Export" in top controls
**Options**:
1. **PNG Image**: Current viewport as static image
2. **SVG**: Scalable vector (for publications)
3. **JSON**: Network data (nodes + edges)
4. **PDF**: Print-friendly version with legend

**Implementation**:
```javascript
// SVG export
const svgString = new XMLSerializer().serializeToString(svgElement)
const blob = new Blob([svgString], { type: 'image/svg+xml' })
downloadBlob(blob, 'systems-map.svg')
```

### Share View State

**URL Parameters**: Encode current view state
```
/systems-map?
  geography=boston&
  zoom=1.2&
  center=450,230&
  selected=node_chw_001&
  filters=built,social
```

**Copy Link Button**: Generates shareable URL

---

## 14. Implementation Checklist

### Phase 1: Basic Rendering
- [ ] D3 force simulation setup
- [ ] Node rendering (circles with category colors)
- [ ] Edge rendering (arrows with direction)
- [ ] Zoom and pan controls
- [ ] Basic hover tooltips

### Phase 2: Styling and States
- [ ] All node states (hover, selected, dimmed, focus)
- [ ] All edge states
- [ ] Evidence quality badges on edges
- [ ] Node type indicators (icons)
- [ ] Labels (zoom-dependent)

### Phase 3: Interactivity
- [ ] Click node → detail panel
- [ ] Click edge → mechanism detail
- [ ] Drag nodes to reposition
- [ ] Multi-select (Shift+Click)
- [ ] Keyboard navigation

### Phase 4: Filtering and Search
- [ ] Category filter (legend)
- [ ] Evidence quality filter
- [ ] Node type filter
- [ ] Text search with autocomplete
- [ ] Pathway highlighting

### Phase 5: Performance
- [ ] Viewport culling
- [ ] Level of detail rendering
- [ ] Canvas/WebGL consideration
- [ ] Web Worker for simulation
- [ ] Memoization and optimization

### Phase 6: Accessibility
- [ ] Keyboard navigation
- [ ] Screen reader announcements
- [ ] Focus indicators (WCAG compliant)
- [ ] Alternative table view
- [ ] High contrast mode support

### Phase 7: Polish
- [ ] Legend component
- [ ] Export functionality
- [ ] Share URL state
- [ ] Loading states
- [ ] Empty states

---

## 15. Reference Implementation

**Technology Stack**:
- **React 18**: Component structure
- **D3.js v7**: Force simulation, data binding
- **TypeScript**: Type safety for node/edge data
- **Tailwind CSS**: Styling utilities
- **React Query**: Data fetching and caching

**Key Files**:
- `MechanismGraph.tsx`: Main graph component (already exists)
- `GraphControls.tsx`: Zoom, filter, search UI
- `GraphLegend.tsx`: Category and evidence legend
- `useForceSimulation.ts`: Custom hook for D3 force
- `graphUtils.ts`: Helper functions (layout, filtering)

**Existing Code**: `frontend/src/visualizations/MechanismGraph.tsx`
- Already has basic force-directed layout
- Needs enhancement for states, filtering, accessibility

---

## Version History

**Version 1.1 (2025-11-19):**
- Updated node taxonomy from text labels to **1-7 numeric scale system**
- Scale 1: Entirely structural (policy level)
- Scale 3: Institutional infrastructure
- Scale 4: Individual/household conditions
- Scale 6: Intermediate pathways
- Scale 7: Pure crisis endpoints
- Updated visual indicators, tooltips, and filters to use numeric scales
- Added scale-based layout layering for force-directed graph
- Scales 2 and 5 reserved for future refinement

**Version 1.0 (2025-11-16):**
- Initial specification
- MVP scope defined (topology & direction only)
- Node visual design with category colors
- Edge design with evidence quality indicators
- Interactive behaviors and accessibility

---

**Next Document**: [04_DETAIL_PANELS.md](./04_DETAIL_PANELS.md) - Specification for node and mechanism detail panels
