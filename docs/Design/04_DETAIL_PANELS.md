# Detail Panels Specification
**HealthSystems Platform - Context and Information Panels**

Version: 1.0
Last Updated: 2025-11-16
Status: MVP Scope (Topology & Direction Only)

---

## Overview

This document specifies the design for all sidebar panels and detail views that provide context, information, and actions related to nodes, mechanisms, pathways, and evidence. These panels follow the "details on demand" principle - they appear when users click elements in the systems map.

**MVP Constraint**: Show qualitative information, topology, and direction. No quantified effect sizes, ROI calculations, or numerical projections.

---

## 1. Panel Architecture

### General Panel Structure

All detail panels follow this consistent structure:

```
┌─────────────────────────────────────┐
│ PANEL HEADER (48px)                 │
│ [Icon] Title            [−] [↔] [X] │  ← Controls
├─────────────────────────────────────┤
│ QUICK STATS BAR (Optional, 40px)    │  ← Key metrics
│ Category: Built Env | Type: Stock   │
├─────────────────────────────────────┤
│                                     │
│ SCROLLABLE CONTENT AREA             │  ← Main content
│                                     │
│ Section 1 Header                    │
│ • Detail line 1                     │
│ • Detail line 2                     │
│                                     │
│ Section 2 Header                    │
│ [Expandable content...]             │
│                                     │
│                                     │
├─────────────────────────────────────┤
│ FOOTER (Optional, 56px)             │  ← Actions
│ [Secondary Action]  [Primary Action]│
└─────────────────────────────────────┘
```

### Panel Dimensions
- **Width**: 320px (default), 400px (expanded), 280-480px (resizable range)
- **Height**: `calc(100vh - 60px)` (full height minus header)
- **Padding**: 24px (sides), 16px (vertical between sections)

### Panel Header
- **Height**: 48px
- **Background**: White (light mode)
- **Border Bottom**: 1px solid gray-200
- **Layout**: Flex row
  - Left: Icon (20px) + Title (H4, 18px bold)
  - Right: Control buttons (Minimize, Resize, Close)

### Panel Content
- **Padding**: 24px all sides
- **Scroll**: Vertical overflow auto, smooth scroll
- **Max Height**: Viewport height - header - footer

### Panel Footer (Optional)
- **Height**: 56px
- **Background**: gray-50 (subtle)
- **Border Top**: 1px solid gray-200
- **Buttons**: Right-aligned, 8px gap

---

## 2. Node Detail Panel

### Trigger
- Click node in systems map
- Select node from Node Library
- Select node from search results

### Header
```
┌─────────────────────────────────────┐
│ [▪] Community Health Workers    [X] │
└─────────────────────────────────────┘
```
- Icon: Node type indicator (Structural/Proxy/Crisis)
- Title: Node name (truncated with tooltip if long)

### Quick Stats Bar
```
┌─────────────────────────────────────┐
│ Built Environment · Structural Stock│
│ 15 outgoing · 3 incoming            │
└─────────────────────────────────────┘
```
- Category (color-coded pill badge)
- Stock type
- Connection counts

### Content Sections

#### 1. Overview Section
```
Overview
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Definition
Community health workers (CHWs) provide health education,
advocacy, and care coordination within underserved communities.

Stock Type
Structural Stock (measured in FTE count)

Measurement
Typically measured as FTE count or per 100k population ratio.
Data sources: HRSA, state workforce databases.
```

**Fields**:
- **Definition**: 2-3 sentence description
- **Stock Type**: Badge with icon (Structural/Proxy/Crisis)
- **Measurement**: How it's quantified (units, data sources) - qualitative only

#### 2. Connections Section
```
Connections (18 total)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Outgoing (15)  [Show All ▼]
┌─────────────────────────────────────┐
│ → Healthcare Continuity Index    [A]│  ← Evidence badge
│   Positive relationship             │
│   12 studies support                │
├─────────────────────────────────────┤
│ → Community Trust Index          [B]│
│   Positive relationship             │
│   5 studies support                 │
├─────────────────────────────────────┤
│ → ED Visits                       [A]│
│   Negative relationship (reduces)   │
│   8 studies support                 │
└─────────────────────────────────────┘

Incoming (3)  [Show All ▼]
┌─────────────────────────────────────┐
│ ← Policy: CHW Funding             [B]│
│   Positive relationship             │
└─────────────────────────────────────┘
```

**Layout**:
- Tabs or accordion: Outgoing / Incoming
- List items: Target node name, direction, evidence quality badge
- Hover: Highlight connection in graph
- Click: Navigate to that mechanism detail
- "Show All" expands list (initially shows top 5)

**Evidence Badge**: A/B/C colored circle (from design system)

#### 3. Spatial Variation Section (MVP)
```
Geographic Variation
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠ Mechanism strength varies by location

This mechanism shows different effects across:
• Urban vs. Rural contexts
• State-level policy environments
• Community demographic composition

Select a geography to see location-specific pathways.
```

**MVP Display**:
- **Flag Icon**: If spatial variation exists
- **Qualitative Description**: What varies (no numbers)
- **Call to Action**: Prompt to select geography filter

**Phase 2**: Show quantified variation by geography

#### 4. Related Nodes Section
```
Related Nodes
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Frequently Connected
• Primary Care Physician Density
• Affordable Housing Units
• Economic Precarity Index

[View in Map]
```

**Logic**: Nodes that share many connections with this node (co-occurrence)

### Footer Actions
```
┌─────────────────────────────────────┐
│ [Export Details]   [View Pathways →]│
└─────────────────────────────────────┘
```

**Buttons**:
- **Export Details**: Download node info as PDF/JSON
- **View Pathways**: Switch to Pathway Explorer tab with this node pre-selected

---

## 3. Mechanism Detail Panel

### Trigger
- Click edge in systems map
- Select mechanism from Evidence Base tab
- Click mechanism in Node Detail panel connections list

### Header
```
┌─────────────────────────────────────┐
│ [⚡] Mechanism Detail           [X] │
└─────────────────────────────────────┘
```

### Quick Stats Bar
```
┌─────────────────────────────────────┐
│ CHWs → Healthcare Continuity Index  │
│ Positive (+) · Evidence: A · 12 St. │
└─────────────────────────────────────┘
```
- From → To nodes (clickable links)
- Direction badge (+ or −)
- Evidence quality badge
- Study count

### Content Sections

#### 1. Mechanism Description
```
Mechanism
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Community health workers improve healthcare continuity
through sustained relationship-building, care coordination,
and navigation of complex health systems. They reduce gaps
in follow-up care and increase patient-provider trust.

Direction: Positive ↑
Increase in CHWs → Increase in Healthcare Continuity Index
```

**Fields**:
- **Description**: 3-5 sentence explanation of HOW the mechanism works
- **Direction**: Explicit statement (Positive/Negative with arrow)
- **Plain Language**: From node ↑↓ To node

#### 2. Evidence Quality Section
```
Evidence Summary
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Quality Rating: A (High)  [ℹ What does this mean?]

Based on 12 studies:
• 8 Randomized Controlled Trials
• 3 Quasi-experimental studies
• 1 Systematic review

Confidence: High consistency across studies
Limitations: Limited long-term follow-up data
```

**Fields**:
- **Quality Rating**: A/B/C badge with label
- **Info Tooltip**: Explains rating criteria
- **Study Breakdown**: Types of evidence
- **Confidence Note**: Qualitative assessment
- **Limitations**: Known gaps or caveats

**MVP Constraint**: No quantified effect sizes, no confidence intervals. Only qualitative strength.

#### 3. Moderators Section
```
Moderators (Factors that Influence Strength)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Policy Context
⚠ Effect stronger when Medicaid coverage includes CHW services
⚠ Effect weaker in states without CHW certification programs

Demographic Factors  [Expand ▼]

Geographic Factors  [Expand ▼]

Implementation Quality  [Expand ▼]
```

**Layout**: Accordion/expandable sections
- **Icons**: Warning (weaker), Check (stronger), Info (varies)
- **Qualitative Descriptions**: No numerical moderator values in MVP
- **Categories**: Policy, Demographic, Geographic, Implementation

#### 4. Citations Section
```
Supporting Literature (12 studies)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[Show All ▼]  Currently showing 3 of 12

┌─────────────────────────────────────────────┐
│ Kangovi et al. (2018)                   [A] │
│ Health Affairs                              │
│ "Effect of Community Health Workers on..."  │
│ [View Citation] [📄 PDF]                    │
├─────────────────────────────────────────────┤
│ Johnson & Smith (2020)                  [A] │
│ JAMA Network Open                           │
│ "Impact of CHW interventions on..."         │
│ [View Citation] [🔗 Link]                   │
└─────────────────────────────────────────────┘

[Export Citations as BibTeX]
```

**Layout**: Expandable list
- **Citation**: Author (Year), Journal, Title
- **Quality Badge**: Study-level quality
- **Actions**: View full citation, access PDF/link
- **Export**: BibTeX, RIS, or plain text

### Footer Actions
```
┌─────────────────────────────────────┐
│ [View in Graph] [Add to Comparison] │
└─────────────────────────────────────┘
```

**Buttons**:
- **View in Graph**: Highlight this edge in map, center view
- **Add to Comparison**: Add to comparison panel (future feature)

---

## 4. Pathway Panel

### Trigger
- Pathway Explorer tab: Select intervention + outcome
- Right-click node in map → "Find pathways to..."
- Click "View Pathways" in Node Detail panel

### Header
```
┌─────────────────────────────────────┐
│ [🛤] Pathways: CHWs → ED Visits  [X]│
└─────────────────────────────────────┘
```

### Quick Stats Bar
```
┌─────────────────────────────────────┐
│ Found 4 pathways · Avg 3 mechanisms │
│ Strongest: Path 1 (A quality)       │
└─────────────────────────────────────┘
```

### Content: Path List

```
Pathways from CHWs to ED Visits
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Path 1: Direct via Healthcare Continuity  [View in Map]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Aggregate Evidence: A (High)  |  2 mechanisms

1. CHWs → Healthcare Continuity Index
   Positive (+)  |  Evidence: A (12 studies)

2. Healthcare Continuity Index → ED Visits
   Negative (−)  |  Evidence: A (15 studies)

Overall Direction: CHWs reduce ED Visits ✓
[Expand Details ▼]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Path 2: Via Community Trust  [View in Map]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Aggregate Evidence: B (Moderate)  |  3 mechanisms

1. CHWs → Community Trust Index
   Positive (+)  |  Evidence: B (5 studies)

2. Community Trust Index → Primary Care Use
   Positive (+)  |  Evidence: A (8 studies)

3. Primary Care Use → ED Visits
   Negative (−)  |  Evidence: A (20 studies)

Overall Direction: CHWs reduce ED Visits ✓
[Expand Details ▼]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[Show All Paths (4 total)]
```

**Path Card Layout**:
- **Header**: Path name/number, "View in Map" button
- **Separator Line**: Visual break between paths
- **Aggregate Evidence**: Overall quality for the path (lowest quality mechanism)
- **Mechanism Count**: Number of steps
- **Mechanism List**: Sequential steps with arrows
  - Each step: From → To, Direction, Evidence badge
- **Overall Direction**: Net effect (positive/negative)
- **Expand**: Show full mechanism details inline

**Sorting**:
- Default: By aggregate evidence quality (A > B > C)
- Option: By path length (shortest first)
- Option: By mechanism count

**Interaction**:
- **Click "View in Map"**: Highlight path in graph (animated flow)
- **Click Mechanism**: Open mechanism detail panel
- **Expand Details**: Show full description for each mechanism inline

### Footer Actions
```
┌─────────────────────────────────────┐
│ [Export Pathways] [Compare Paths]   │
└─────────────────────────────────────┘
```

---

## 5. Filter Panel

### Trigger
- Click "Filter" button in graph controls
- Press `F` keyboard shortcut
- Open from settings menu

### Header
```
┌─────────────────────────────────────┐
│ [⚙] Filters                     [X] │
└─────────────────────────────────────┘
```

### Content Sections

#### 1. Category Filter
```
Categories
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
☑ Built Environment      (123 nodes)
☑ Social Environment     (87 nodes)
☑ Economic               (64 nodes)
☑ Political              (45 nodes)
☑ Biological             (56 nodes)
☐ Uncategorized          (25 nodes)

[Select All]  [Deselect All]
```

**Layout**: Checkboxes with category color dot
**Counts**: Number of nodes in each category (dynamic)
**Actions**: Bulk select/deselect

#### 2. Evidence Quality Filter
```
Evidence Quality
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Mechanism Evidence Threshold
○ Show all mechanisms
● Show A and B quality only
○ Show A quality only

[ℹ] Filters mechanisms (edges), not nodes
```

**Layout**: Radio buttons
**Tooltip**: Explain that this filters edges, nodes remain visible

#### 3. Node Type Filter
```
Stock Types
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
☑ Structural Stocks      (150 nodes)
☑ Proxy Indices          (180 nodes)
☑ Crisis Outcomes        (70 nodes)
```

#### 4. Spatial Variation Filter
```
Geographic Variation
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
☑ Show mechanisms with spatial variation
☐ Show only universal mechanisms
```

**Tooltip**: "Spatial variation means mechanism strength differs by geography"

#### 5. Text Search Filter
```
Search
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Search nodes or mechanisms...      🔍]

Recent Searches:
• housing
• trust index
• primary care
```

**Features**:
- Autocomplete dropdown
- Recent searches (last 5)
- Clear button (X icon)

### Footer Actions
```
┌─────────────────────────────────────┐
│ [Reset Filters]     [Apply Filters] │
└─────────────────────────────────────┘
```

**Real-time vs. Apply**:
- **Option 1**: Real-time filtering (apply on change)
- **Option 2**: Staged filtering (apply on button click)
- **Recommendation**: Real-time for better UX, with debouncing for performance

---

## 6. Search Results Panel

### Trigger
- Type in search bar, press Enter
- Click search icon
- Press `Cmd/Ctrl + K`

### Header
```
┌─────────────────────────────────────┐
│ [🔍] Search: "housing"          [X] │
└─────────────────────────────────────┘
```

### Content

```
Results (8 found)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Nodes (3)
┌─────────────────────────────────────┐
│ Affordable Housing Units         [▪]│  ← Stock type icon
│ Built Environment · Structural      │
│ 23 connections                      │
│ [View Details] [View in Map]        │
├─────────────────────────────────────┤
│ Housing Stability Index          [◗]│
│ Built Environment · Proxy           │
│ 15 connections                      │
│ [View Details] [View in Map]        │
└─────────────────────────────────────┘

Mechanisms (5)
┌─────────────────────────────────────┐
│ Housing Units → Health Outcomes  [A]│  ← Evidence badge
│ Positive relationship               │
│ "Stable housing reduces..."         │
│ [View Mechanism]                    │
├─────────────────────────────────────┤
│ Policy → Housing Availability    [B]│
│ Positive relationship               │
│ "Zoning reform increases..."        │
│ [View Mechanism]                    │
└─────────────────────────────────────┘

[Show All Results]
```

**Layout**:
- Grouped by type (Nodes, Mechanisms)
- Result cards with key info
- Action buttons
- Keyword highlighting in descriptions

**Empty State**:
```
No results for "xyz"

Suggestions:
• Check spelling
• Try broader terms
• Use filters to narrow scope

[Clear Search]
```

### Footer Actions
```
┌─────────────────────────────────────┐
│ [Clear Search]      [Export Results]│
└─────────────────────────────────────┘
```

---

## 7. Settings Panel

### Trigger
- Click settings icon (gear) in header
- Keyboard shortcut: `Cmd/Ctrl + ,`

### Header
```
┌─────────────────────────────────────┐
│ [⚙] Settings                    [X] │
└─────────────────────────────────────┘
```

### Content Sections

#### 1. Display Settings
```
Display
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
☑ Show node labels (zoom ≥ 0.8)
☑ Show evidence badges on edges
☑ Animate pathway flows
☐ High contrast mode
```

#### 2. Interaction Settings
```
Interaction
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
☑ Enable node dragging
☑ Auto-save view state
☐ Confirm before closing panels

Zoom sensitivity: [────●───] (slider)
```

#### 3. Accessibility Settings
```
Accessibility
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
☐ Reduce motion
☑ Keyboard navigation hints
☑ Screen reader announcements

Color vision:
○ Default
○ Deuteranopia
○ Protanopia
○ Tritanopia
```

#### 4. Geography Selection
```
Default Geography
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Select Region ▼]
• United States (National)
• Boston, MA
• Chicago, IL
• Custom...

[ℹ] Sets default for all pathway explorations
```

### Footer Actions
```
┌─────────────────────────────────────┐
│ [Reset to Defaults]      [Save]     │
└─────────────────────────────────────┘
```

---

## 8. Common UI Patterns

### Expandable Sections

```
Section Header                       [Expand ▼]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

(Collapsed content hidden)

↓ Click to expand ↓

Section Header                       [Collapse ▲]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Expanded content visible here...
• Detail 1
• Detail 2
```

**Behavior**:
- Click header or icon to toggle
- Smooth height transition (300ms)
- Save state (remember expanded/collapsed)

### Badge Components

**Evidence Quality Badge**:
```
[A]  [B]  [C]  [?]
```
- Size: 24px circle
- Background: White
- Border: 2px, quality color
- Text: 12px bold, centered

**Category Badge**:
```
[Built Environment]
```
- Pill shape (rounded-full)
- Background: Category color (20% opacity)
- Text: Category color (dark shade)
- Padding: 4px 12px

**Direction Badge**:
```
[+] Positive    [−] Negative
```
- Icon + text
- Color: Green (+), Red (−)

### Action Buttons

**Primary Button**:
```css
background: primary-600
color: white
padding: 8px 16px
border-radius: 6px
font-weight: 600
hover: primary-700
```

**Secondary Button**:
```css
background: white
color: primary-600
border: 1px solid primary-600
padding: 8px 16px
border-radius: 6px
hover: primary-50 background
```

**Text Button**:
```css
background: transparent
color: primary-600
padding: 8px 12px
hover: primary-50 background
```

### Loading States

**Skeleton Screen** (preferred):
```
┌─────────────────────────────────────┐
│ [▮▮] ▮▮▮▮▮▮▮▮▮▮▮▮▮         [X] │  ← Header skeleton
├─────────────────────────────────────┤
│ ▮▮▮▮▮▮▮ · ▮▮▮▮▮▮▮▮▮             │  ← Stats skeleton
├─────────────────────────────────────┤
│                                     │
│ ▮▮▮▮▮▮▮▮▮                       │
│ ▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮       │  ← Content skeleton
│ ▮▮▮▮▮▮▮▮▮▮▮▮▮▮                 │
│                                     │
└─────────────────────────────────────┘
```

**Spinner** (when content unknown):
```
        [◐]
    Loading...
```

### Empty States

**No Data Selected**:
```
     [📋]
  No item selected

Select a node or mechanism
    to view details
```

**No Results**:
```
     [🔍]
  No results found

Try adjusting your filters
   or search terms
```

---

## 9. Responsive Behavior

### Desktop (>1024px)
- Panel: 320-400px sidebar, always visible option
- Content: Full layouts as specified
- Scroll: Vertical within panel

### Tablet (768-1024px)
- Panel: Overlay from right (slides over graph)
- Width: 400px (fixed)
- Backdrop: Semi-transparent, clickable to close

### Mobile (<768px)
- Panel: Full-screen modal (slides up from bottom)
- Header: Add back button (← instead of X)
- Footer: Sticky at bottom
- Scroll: Vertical, full content

**Animation** (mobile):
```css
@media (max-width: 768px) {
  .detail-panel {
    position: fixed;
    bottom: 0;
    width: 100%;
    height: 90vh;
    border-radius: 16px 16px 0 0;
    animation: slideUp 300ms ease-out;
  }
}

@keyframes slideUp {
  from { transform: translateY(100%) }
  to { transform: translateY(0) }
}
```

---

## 10. Accessibility Features

### Keyboard Navigation

**Within Panel**:
- `Tab`: Navigate interactive elements
- `Shift+Tab`: Reverse navigation
- `Enter/Space`: Activate buttons, toggle expand/collapse
- `Esc`: Close panel

**Focus Order**:
1. Close button (X)
2. Quick stats (if clickable)
3. Section headers (if expandable)
4. Interactive elements in order
5. Footer buttons

### Screen Reader Announcements

**Panel Open**:
```
"Node detail panel opened. Community Health Workers.
Built Environment category. 15 outgoing connections, 3 incoming."
```

**Section Expand**:
```
"Connections section expanded. Showing 15 outgoing mechanisms."
```

**Button Actions**:
```
"View in map button. Activates graph view centered on this node."
```

### ARIA Attributes

```html
<aside
  role="complementary"
  aria-label="Node detail panel"
  aria-modal="false"
  tabindex="-1"
>
  <header>
    <h2 id="panel-title">Community Health Workers</h2>
    <button aria-label="Close panel">×</button>
  </header>

  <section aria-labelledby="connections-header">
    <h3 id="connections-header">Connections</h3>
    ...
  </section>
</aside>
```

---

## 11. Implementation Checklist

### Phase 1: Core Panels
- [ ] Panel container component (resizable, collapsible)
- [ ] Node detail panel
- [ ] Mechanism detail panel
- [ ] Filter panel
- [ ] Search results panel

### Phase 2: Advanced Panels
- [ ] Pathway panel
- [ ] Settings panel
- [ ] Comparison panel (future)

### Phase 3: UI Components
- [ ] Expandable sections
- [ ] Badge components (evidence, category, direction)
- [ ] Action buttons (primary, secondary, text)
- [ ] Loading states (skeletons, spinners)
- [ ] Empty states

### Phase 4: Interactions
- [ ] Panel open/close animations
- [ ] Resize handle (drag to adjust width)
- [ ] Scroll behavior (sticky headers)
- [ ] Cross-panel navigation (click → open different panel)

### Phase 5: Accessibility
- [ ] Keyboard navigation
- [ ] Focus management (trap focus in panel)
- [ ] Screen reader announcements
- [ ] ARIA attributes
- [ ] High contrast mode support

### Phase 6: Responsive
- [ ] Desktop layout (sidebar)
- [ ] Tablet layout (overlay)
- [ ] Mobile layout (full-screen modal)

---

**Next Document**: [05_COMPONENT_LIBRARY.md](./05_COMPONENT_LIBRARY.md) - Reusable UI components specification
