# Dashboard Layout Architecture
**HealthSystems Platform - Screen Structure & Navigation**

Version: 1.0
Last Updated: 2025-11-16
Status: MVP Scope (Topology & Direction Only)

---

## Overview

This document defines the overall layout architecture for the HealthSystems dashboard - a clean, minimalist interface designed for exploring complex health system relationships. The layout prioritizes the interactive systems map while providing efficient access to node details, pathway exploration, and evidence review.

---

## 1. Layout Philosophy

### Design Goals
1. **Map-First**: The network visualization is the primary interface, occupying majority screen space
2. **Context on Demand**: Details appear in panels/modals, not separate pages
3. **Minimal Navigation**: Few top-level tabs, deep exploration within each
4. **Flexible Workspace**: Resizable, collapsible panels for user customization
5. **Persistent Context**: Geography selection and filters persist across views

### Screen Real Estate Priorities
1. Systems Map Canvas (60-75%)
2. Detail/Context Panel (20-30%)
3. Navigation/Filters (5-10%)
4. Status/Breadcrumbs (minimal)

---

## 2. Primary Layout Structure

### Desktop Layout (>1024px)

```
┌─────────────────────────────────────────────────────────────────────┐
│  HEADER (60px)                                                       │
│  [Logo] [Tab Navigation] ············· [Geography] [User] [Settings]│
├─────────────────────────────────────────────────────────────────────┤
│                              │                                       │
│                              │  RIGHT SIDEBAR (320-400px)            │
│                              │  ┌──────────────────────────────────┐│
│                              │  │ Panel Header      [Collapse] [X] ││
│                              │  ├──────────────────────────────────┤│
│  MAIN CANVAS                 │  │                                  ││
│  (Interactive Systems Map)   │  │  Detail Content                  ││
│                              │  │  - Node/Mechanism Details        ││
│  - Network Graph             │  │  - Evidence                      ││
│  - Zoom/Pan Controls         │  │  - Related Items                 ││
│  - Legend                    │  │  - Actions                       ││
│                              │  │                                  ││
│                              │  │                                  ││
│                              │  └──────────────────────────────────┘│
│                              │                                       │
├──────────────────────────────┴───────────────────────────────────────┤
│  BOTTOM BAR (40px) - Optional                                        │
│  Breadcrumb / Selected Path / Status                                 │
└─────────────────────────────────────────────────────────────────────┘
```

### Component Dimensions (Desktop)

| Component | Width | Height | Behavior |
|-----------|-------|--------|----------|
| Header | 100% | 60px | Fixed, always visible |
| Main Canvas | Flex (60-80%) | calc(100vh - 60px) | Responsive to sidebar |
| Right Sidebar | 320px (min) - 400px (max) | calc(100vh - 60px) | Resizable, collapsible |
| Bottom Bar | 100% | 40px | Optional, auto-hide |

---

## 3. Header Component

### Structure

```
┌─────────────────────────────────────────────────────────────────────┐
│ [HS Logo]  [Systems Map] [Pathway Explorer] [Library] ··· [Filters] │
│  (120px)        TAB NAVIGATION (flex)              RIGHT SECTION     │
└─────────────────────────────────────────────────────────────────────┘
```

### Header Sections

**Left: Branding (120px)**
- HealthSystems logo/wordmark
- Click returns to default map view
- Subtle, doesn't compete with content

**Center: Tab Navigation (flex)**
- Primary navigation tabs (3-5 max)
- Active tab highlighted (border-bottom, bold)
- Icons optional, text labels required

**Right: Global Controls (~300px)**
- Geography selector (dropdown)
- Filter toggle (icon button)
- User menu (avatar/icon)
- Settings (icon)

### Tab Navigation Items

**MVP Tabs (Recommended 4)**

1. **Systems Map** (Default/Home)
   - Icon: Network/nodes
   - Full network visualization
   - Default landing page

2. **Pathway Explorer**
   - Icon: Route/path
   - Intervention → Outcome tracing
   - Guided exploration mode

3. **Node Library**
   - Icon: Library/collection
   - Searchable list of all ~840 canonical nodes (from `mechanism-bank/mechanisms/canonical_nodes.json`)
   - Table/card view toggle
   - Filter by scale (1-5) and domain

4. **Evidence Base**
   - Icon: Document/citation
   - Literature review
   - Mechanism evidence quality overview

**Future Tabs (Phase 2)**
- ROI Calculator (quantification)
- Scenario Builder (simulations)

### Header Behavior
- **Fixed Position**: Stays visible when scrolling (graph pans underneath)
- **Shadow**: Subtle shadow when scrolled (z-index context)
- **Responsive**: Collapses to hamburger menu <768px

---

## 4. Main Canvas Area

### Systems Map View (Default)

```
┌───────────────────────────────────────────────────────────┐
│ CONTROLS (Floating, Top-Right)                            │
│ [Search] [Filter] [Zoom +/-] [Fit] [Reset]                │
├───────────────────────────────────────────────────────────┤
│                                                            │
│              NETWORK GRAPH (SVG Canvas)                    │
│                                                            │
│    • Nodes (circles, color-coded)                          │
│    • Edges (directional arrows)                            │
│    • Labels (on zoom)                                      │
│                                                            │
│                                                            │
│                                                            │
├───────────────────────────────────────────────────────────┤
│ LEGEND (Floating, Bottom-Left)                             │
│ [Built Env] [Social] [Economic] [Political] [Biological]  │
│ [Evidence: A B C] [+/-] [Stock Types]                     │
└───────────────────────────────────────────────────────────┘
```

### Canvas Controls (Floating Toolbar)

**Position**: Top-right, 16px margin
**Style**: White background, shadow-md, rounded-lg
**Layout**: Horizontal button group

| Control | Icon | Function | Shortcut |
|---------|------|----------|----------|
| Search | Magnifying glass | Find node by name | Cmd/Ctrl+K |
| Filter | Funnel | Show filter panel | F |
| Zoom In | + | Increase zoom level | + or = |
| Zoom Out | - | Decrease zoom level | - |
| Fit Screen | Expand | Fit all nodes in view | 0 |
| Reset | Circular arrow | Reset pan/zoom | R |
| Fullscreen | Expand arrows | Enter fullscreen | F11 |

### Legend (Floating Panel)

**Position**: Bottom-left, 16px margin
**Style**: Semi-transparent background (glass effect), compact
**Content**:
- Category colors (clickable to filter)
- Evidence quality badges (A/B/C)
- Direction indicators (+/-)
- Stock type icons
- Edge thickness meaning

**Behavior**:
- Collapsible (hide icon)
- Hover to highlight category
- Click to filter/isolate

---

## 5. Right Sidebar Panel

### Panel Structure

```
┌─────────────────────────────────────┐
│ PANEL HEADER (48px)                 │
│ [Icon] Title            [−] [↔] [X] │
├─────────────────────────────────────┤
│                                     │
│ SCROLLABLE CONTENT AREA             │
│                                     │
│ • Sections with headers             │
│ • Expandable/collapsible groups     │
│ • Data display (text, lists, etc)   │
│ • Action buttons at bottom          │
│                                     │
│                                     │
│                                     │
│                                     │
│                                     │
├─────────────────────────────────────┤
│ FOOTER (Optional, 56px)             │
│ [Secondary Action]  [Primary Action]│
└─────────────────────────────────────┘
```

### Panel Header Controls

| Icon | Function | Behavior |
|------|----------|----------|
| **−** | Minimize | Collapse to tab on right edge |
| **↔** | Resize | Toggle 320px ↔ 400px |
| **X** | Close | Hide panel, return focus to map |

### Panel Content Types

**1. Node Detail Panel** (Most Common)
- Node name and category
- Stock type and units
- Connected mechanisms (in/out)
- Evidence summary
- Related nodes

**2. Mechanism Detail Panel**
- Mechanism description
- From → To nodes
- Direction and rationale
- Evidence quality and citations
- Moderators (qualitative flags)

**3. Pathway Panel**
- Selected intervention node
- Target outcome node
- All paths between them (list)
- Activated mechanisms
- Aggregate evidence quality

**4. Filter Panel**
- Category checkboxes
- Evidence quality filters
- Node type filters
- Spatial variation toggle
- Search/text filter

**5. Search Results Panel**
- Query at top
- Results list (nodes/mechanisms)
- Click to select/highlight
- Clear/refine search

### Panel Behavior

**Opening**:
- Slide in from right (300ms ease-out)
- Pushes main canvas left (responsive resize)
- Focus moves to panel content

**Closing**:
- Slide out to right (300ms ease-in)
- Main canvas expands (smooth transition)
- Focus returns to map

**Resizing**:
- Drag handle on left edge
- Min: 280px, Max: 480px
- Default: 320px (compact), 400px (expanded)
- Snap to default sizes

**State Persistence**:
- Last panel state saved (open/closed, size)
- Panel content preserved on tab switch
- Re-opening shows last viewed item

---

## 6. Responsive Layouts

### Tablet (768px - 1024px)

```
┌─────────────────────────────────────┐
│ HEADER (Condensed, 56px)            │
│ [☰] [Tabs] ········ [Geography] [•] │
├─────────────────────────────────────┤
│                                     │
│                                     │
│  FULL-WIDTH CANVAS                  │
│  (Sidebar overlay on demand)        │
│                                     │
│                                     │
│                                     │
│                                     │
└─────────────────────────────────────┘

// Panel opens as overlay from right
```

**Changes**:
- Sidebar becomes overlay (slides over canvas)
- Tab labels may hide, show icons only
- Controls consolidate into menus
- Legend becomes collapsible by default

### Mobile (< 768px)

```
┌─────────────────────┐
│ HEADER (48px)       │
│ [☰] HS    [⚙] [•]  │
├─────────────────────┤
│                     │
│  MAP VIEW           │
│  (Touch gestures)   │
│                     │
│  • Pinch to zoom    │
│  • Tap for detail   │
│  • Swipe panels     │
│                     │
└─────────────────────┘

// Full-screen panels (slide up from bottom)
```

**Changes**:
- Header minimal (logo + hamburger menu)
- Tabs become drawer menu
- Canvas full-screen
- Details open as full-screen modal (slide up)
- Touch gestures replace mouse interactions
- Simplified legend (icon only, tap to expand)

---

## 7. Multi-Tab Layouts

### Tab 1: Systems Map (Default)

**Layout**: Canvas + Sidebar (as described above)
**Purpose**: Free-form exploration of full network
**Key Features**:
- Full 400 nodes, 2000 mechanisms
- Filter and search
- Click node → detail panel
- Click edge → mechanism panel

---

### Tab 2: Pathway Explorer

```
┌─────────────────────────────────────────────────────────────┐
│ PATHWAY SETUP BAR (80px)                                    │
│ Select Intervention: [Dropdown/Search ▼]                    │
│ Select Outcome:      [Dropdown/Search ▼]     [Find Paths]  │
├──────────────────────────────────┬──────────────────────────┤
│                                  │ RIGHT PANEL (400px)      │
│  MAP WITH HIGHLIGHTED PATHS      │                          │
│                                  │ PATH LIST                │
│  • Intervention node (green)     │ ┌──────────────────────┐ │
│  • Outcome node (red)            │ │ Path 1: Direct       │ │
│  • Active paths (bold edges)     │ │ ✓ Quality: A (3)     │ │
│  • Inactive nodes (dimmed)       │ │ • 2 mechanisms       │ │
│                                  │ └──────────────────────┘ │
│                                  │ ┌──────────────────────┐ │
│                                  │ │ Path 2: Via Social   │ │
│                                  │ │ ⚠ Quality: B (2)     │ │
│                                  │ │ • 4 mechanisms       │ │
│                                  │ └──────────────────────┘ │
│                                  │                          │
│                                  │ [Export Paths]           │
└──────────────────────────────────┴──────────────────────────┘
```

**Purpose**: Guided exploration - intervention to outcome tracing
**Interaction**:
1. User selects intervention (e.g., "Community Health Workers")
2. User selects outcome (e.g., "ED Visits")
3. System highlights all paths connecting them
4. Panel lists paths ranked by evidence quality
5. Click path to view mechanism details

---

### Tab 3: Node Library

```
┌─────────────────────────────────────────────────────────────┐
│ TOOLBAR (56px)                                              │
│ [Search: ___________] [Category ▼] [Type ▼]  [⊞ Grid] [≡]  │
├─────────────────────────────────────────────────────────────┤
│                                  │                          │
│  TABLE/GRID VIEW                 │  PREVIEW PANEL (300px)   │
│                                  │                          │
│  ┌─────────────────────────────┐ │  [Selected Node]        │
│  │ Name       │ Category │ #   │ │  • Category             │
│  ├─────────────────────────────┤ │  • Type                 │
│  │ CHWs       │ Built    │ 15  │ │  • Connections          │
│  │ Housing    │ Built    │ 23  │ │  • Evidence             │
│  │ Trust Idx  │ Social   │ 8   │ │                         │
│  │ ED Visits  │ Crisis   │ 42  │ │  [View in Map]          │
│  │ ...        │ ...      │ ... │ │                         │
│  └─────────────────────────────┘ │                          │
│                                  │                          │
│  [Pagination: 1 2 3 ... 20]      │                          │
└──────────────────────────────────┴──────────────────────────┘
```

**Purpose**: Browse/search all nodes in structured format
**View Modes**:
- **Table View**: Sortable columns (name, category, # connections)
- **Grid View**: Cards with icons and quick stats
**Actions**:
- Click row → preview panel
- Double-click → navigate to map view (centered on node)
- Multi-select → compare nodes

---

### Tab 4: Evidence Base

```
┌─────────────────────────────────────────────────────────────┐
│ FILTERS (56px)                                              │
│ [Category ▼] [Quality ▼] [Search Citations: _________]     │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  MECHANISM LIST (with evidence metadata)                    │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ CHWs → Healthcare Continuity Index                  │   │
│  │ Direction: Positive (+)  Quality: A  Studies: 12   │   │
│  │ "Community health workers improve care continuity   │   │
│  │  through relationship building..." [Expand ▼]       │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ Housing Units → Health Outcomes                     │   │
│  │ Direction: Positive (+)  Quality: B  Studies: 8    │   │
│  │ "Stable housing reduces acute care..." [Expand ▼]  │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  [Load More...]                                             │
└─────────────────────────────────────────────────────────────┘
```

**Purpose**: Review evidence for all mechanisms
**Features**:
- Searchable/filterable mechanism list
- Expand to see citations
- Link to source studies
- Evidence quality overview dashboard

---

## 8. Modal & Overlay Patterns

### Modal Sizes

| Size | Width | Use Case |
|------|-------|----------|
| **Small** | 400px | Confirmations, simple forms |
| **Medium** | 600px | Node/mechanism details (alternative to sidebar) |
| **Large** | 800px | Evidence review, complex forms |
| **Full** | 90% | Image/graph viewer, documentation |

### Modal Structure

```
┌─────────────────────────────────────┐
│ BACKDROP (semi-transparent black)   │
│                                     │
│   ┌───────────────────────────┐     │
│   │ MODAL HEADER          [X] │     │
│   ├───────────────────────────┤     │
│   │                           │     │
│   │ CONTENT                   │     │
│   │                           │     │
│   │                           │     │
│   ├───────────────────────────┤     │
│   │  [Cancel]    [Confirm]    │     │
│   └───────────────────────────┘     │
│                                     │
└─────────────────────────────────────┘
```

**Behavior**:
- Center screen
- Backdrop click closes (or prompt if unsaved changes)
- ESC key closes
- Focus trap within modal
- Animate: fade in (200ms)

### Toast Notifications

**Position**: Top-right, 16px margin, stacking vertically
**Types**: Success, Error, Warning, Info
**Duration**: 4s (auto-dismiss), 8s (error), ∞ (manual dismiss)

```
┌───────────────────────────────────┐
│ ✓ Node added to pathway      [X] │
└───────────────────────────────────┘
```

---

## 9. Loading & Empty States

### Loading States

**Full Page Load**
```
┌─────────────────────────────────────┐
│ HEADER (visible)                    │
├─────────────────────────────────────┤
│                                     │
│          [Spinner]                  │
│     Loading systems map...          │
│                                     │
└─────────────────────────────────────┘
```

**Skeleton Screens** (Preferred)
- Show layout structure immediately
- Gray placeholder blocks for content
- Animated shimmer effect
- Replace with real content when loaded

**Progress Indicators**
- Spinner: Indeterminate loading
- Progress bar: Known duration (e.g., file processing)
- Node count: "Loading 237/400 nodes..."

### Empty States

**No Results**
```
┌─────────────────────────────────────┐
│                                     │
│         [Icon: Empty Box]           │
│                                     │
│      No mechanisms found            │
│   Try adjusting your filters        │
│                                     │
│      [Clear Filters]                │
└─────────────────────────────────────┘
```

**No Selection**
```
┌─────────────────────────────────────┐
│  Detail Panel                   [X] │
├─────────────────────────────────────┤
│                                     │
│   [Icon: Click cursor]              │
│                                     │
│   Select a node to view details     │
│                                     │
└─────────────────────────────────────┘
```

---

## 10. Accessibility Features

### Keyboard Navigation

**Global Shortcuts**
- `Cmd/Ctrl + K`: Open search
- `F`: Toggle filters
- `Tab`: Navigate interactive elements
- `ESC`: Close panel/modal
- `?`: Show keyboard shortcuts help

**Graph Navigation**
- `Arrow Keys`: Move between nodes
- `Enter/Space`: Select node
- `+/-`: Zoom in/out
- `0`: Reset zoom
- `R`: Reset view

### Screen Reader Support

**Landmark Regions**
```html
<header role="banner">...</header>
<nav role="navigation">...</nav>
<main role="main">...</main>
<aside role="complementary">...</aside>
```

**Live Regions**
- Search results: `aria-live="polite"`
- Error messages: `aria-live="assertive"`
- Node selection: Announce "Selected: [node name]"

### Skip Links

```
[Skip to main content]
[Skip to navigation]
[Skip to graph]
```

Hidden visually, visible on focus (keyboard users)

---

## 11. Layout Variations & Special Cases

### Fullscreen Mode

**Trigger**: Fullscreen button or F11
**Behavior**:
- Header hides (or minimal version)
- Canvas expands to 100% viewport
- ESC to exit
- Controls still accessible (floating)

### Print View

**Trigger**: Print button or Cmd/Ctrl+P
**Layout Changes**:
- Hide interactive controls
- Flatten sidebar content below map
- Ensure adequate contrast (no transparency)
- Include URL and timestamp footer

### Embed Mode (Future)

**Use Case**: Iframe embed in external site
**Layout**: Minimal header, no navigation, specific view locked
**Parameters**: `?embed=true&view=pathway&intervention=X&outcome=Y`

---

## 12. Implementation Checklist

### Phase 1: Core Layout
- [ ] Header component with tab navigation
- [ ] Main canvas container (responsive)
- [ ] Right sidebar (collapsible, resizable)
- [ ] Basic responsive breakpoints
- [ ] Modal system
- [ ] Toast notifications

### Phase 2: Tab Views
- [ ] Systems Map view (default)
- [ ] Pathway Explorer view
- [ ] Node Library view
- [ ] Evidence Base view

### Phase 3: Enhancements
- [ ] Keyboard shortcuts
- [ ] Screen reader optimizations
- [ ] Loading states (skeleton screens)
- [ ] Empty states
- [ ] Print styles

### Phase 4: Polish
- [ ] Fullscreen mode
- [ ] Preference persistence (sidebar size, etc.)
- [ ] Tour/onboarding overlay
- [ ] Performance optimization (virtualization for large lists)

---

## 13. File Structure (React Components)

```
frontend/src/
├── layouts/
│   ├── DashboardLayout.tsx        # Main wrapper
│   ├── Header.tsx                 # Top navigation
│   ├── Sidebar.tsx                # Right panel
│   └── BottomBar.tsx              # Optional status bar
├── views/
│   ├── SystemsMapView.tsx         # Tab 1
│   ├── PathwayExplorerView.tsx    # Tab 2
│   ├── NodeLibraryView.tsx        # Tab 3
│   └── EvidenceBaseView.tsx       # Tab 4
├── components/
│   ├── common/
│   │   ├── Modal.tsx
│   │   ├── Toast.tsx
│   │   └── EmptyState.tsx
│   ├── controls/
│   │   ├── ZoomControls.tsx
│   │   ├── Legend.tsx
│   │   └── FilterPanel.tsx
│   └── panels/
│       ├── NodeDetailPanel.tsx
│       ├── MechanismDetailPanel.tsx
│       └── PathwayPanel.tsx
└── visualizations/
    └── MechanismGraph.tsx         # D3/Cytoscape graph
```

---

**Next Document**: [03_SYSTEMS_MAP_VISUALIZATION.md](./03_SYSTEMS_MAP_VISUALIZATION.md) - Detailed network graph visualization specifications
