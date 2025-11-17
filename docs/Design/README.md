# HealthSystems Dashboard - Design Documentation

**Complete Visual Design Guidelines for the Web Application**

Version: 1.0
Last Updated: 2025-11-16
Status: MVP Scope (Topology & Direction Only)

---

## Overview

This directory contains comprehensive visual design guidelines for the HealthSystems dashboard - a clean, minimalist web application for exploring complex health system relationships through interactive network visualizations.

### Design Philosophy

**Core Principles:**
- **Clarity Over Decoration**: Every visual element serves a functional purpose
- **Accessibility First**: WCAG AA compliance, keyboard navigation essential
- **Information Density**: Balance comprehensive data with cognitive ease
- **Progressive Disclosure**: Overview first, details on demand
- **Consistent Mental Models**: Same patterns across all views

### MVP Scope Constraint

**Show topology and direction, NOT quantification**. All visual elements communicate relationships, pathways, and qualitative evidence without implying numerical precision. Phase 2 will add quantitative analysis and ROI calculations.

---

## Documentation Structure

### 1. [Design System](./01_DESIGN_SYSTEM.md) 📐
**Foundation - Start Here**

The visual design foundation including:
- Color palette (6 category colors + semantic colors)
- Typography scale (Inter font family)
- Spacing system (4px base unit)
- Borders, shadows, and elevation
- Component states (hover, focus, active, disabled)
- Iconography guidelines
- Accessibility standards (WCAG AA)
- Responsive breakpoints
- Animation and transitions

**Key Takeaways:**
- 5 category colors + default gray
- Evidence quality colors (A=green, B=amber, C=red)
- 2px focus rings with 2px offset
- Base spacing unit: 4px
- Max contrast: gray-900 on white (15.3:1)

**For:** Everyone (required reading)

---

### 2. [Dashboard Layout Architecture](./02_DASHBOARD_LAYOUT.md) 🏗️
**Screen Structure & Navigation**

Overall layout architecture including:
- Primary layout structure (header, canvas, sidebar)
- Header component (tabs, geography selector)
- Main canvas area (systems map)
- Right sidebar panel (resizable, collapsible)
- Multi-tab layouts (4 main tabs)
- Modal and overlay patterns
- Responsive layouts (desktop, tablet, mobile)
- Loading and empty states

**Key Takeaways:**
- Map-first: 60-75% screen real estate
- 4 main tabs: Systems Map, Pathway Explorer, Node Library, Evidence Base
- Sidebar: 320px default, 400px expanded, 280-480px range
- Mobile: Full-screen panels slide up from bottom
- Fixed header (60px), always visible

**For:** Product designers, frontend architects

---

### 3. [Interactive Systems Map Visualization](./03_SYSTEMS_MAP_VISUALIZATION.md) 🕸️
**Network Graph Specification**

Detailed visualization design including:
- Node visual design (circles, color-coded, 3 stock types)
- Edge visual design (arrows, width encoding, direction)
- Evidence quality indicators (badges on edges)
- Layout algorithm (D3 force-directed)
- Zoom and pan controls (0.2x - 4.0x range)
- Interactive behaviors (hover, click, drag, multi-select)
- Filtering and search (category, quality, type)
- Pathway highlighting (intervention → outcome)
- Performance optimizations (viewport culling, LOD)
- Legend component
- Export and sharing

**Key Takeaways:**
- 400 nodes, 2000+ edges at scale
- Node radius: √(weight) × 20
- Category colors with 80% opacity
- Evidence badges: 16px circles on edges
- Force-directed layout with collision detection
- Keyboard navigation with arrow keys
- Canvas rendering for performance

**For:** Data visualization developers, D3.js engineers

---

### 4. [Detail Panels Specification](./04_DETAIL_PANELS.md) 📋
**Context & Information Panels**

All sidebar panels and detail views including:
- Panel architecture (header, content, footer)
- Node detail panel (overview, connections, spatial variation)
- Mechanism detail panel (description, evidence, moderators, citations)
- Pathway panel (path list, mechanism steps)
- Filter panel (category, quality, type, search)
- Search results panel
- Settings panel
- Common UI patterns (expandable sections, badges, buttons)
- Responsive behavior (overlay on tablet, full-screen on mobile)
- Accessibility features (keyboard nav, screen reader)

**Key Takeaways:**
- Panel width: 320-400px, resizable
- Consistent header with minimize/expand/close controls
- Scrollable content area
- Optional footer with actions
- Touch-friendly on mobile (swipe to close)
- ARIA landmarks and live regions

**For:** Frontend developers, UX designers

---

### 5. [Component Library Specification](./05_COMPONENT_LIBRARY.md) 🧩
**Reusable UI Components**

Building blocks of the application including:
- **Base components**: Button, Input, Badge, Icon, Tooltip
- **Composite components**: Card, Modal, Dropdown, Tabs, Accordion
- **Domain components**: NodeCard, MechanismCard, EvidenceBadge, CategoryBadge, PathwayCard
- **Layout components**: Panel, Grid, Stack, Container
- **Visualization components**: Legend, GraphControls
- TypeScript props interfaces
- Accessibility guidelines (all components)
- Testing strategy (Jest, axe, Playwright)
- Storybook documentation

**Key Takeaways:**
- React 18 + TypeScript + Tailwind CSS
- All components keyboard accessible
- Minimum 44×44px touch targets
- Focus indicators on all interactive elements
- Unit tests + accessibility tests required
- Storybook stories for documentation

**For:** Frontend developers, design system maintainers

---

### 6. [Visual Mockups & Examples](./06_MOCKUPS.md) 🎨
**Wireframes & User Flows**

Visual examples and interaction flows including:
- Full dashboard view (desktop)
- Pathway Explorer view
- Node Library view
- Mobile view (responsive)
- Interaction examples (exploring mechanisms, filtering, searching)
- Empty and error states
- User flows (onboarding, policy analyst, researcher)
- Responsive breakpoint examples
- Accessibility examples (keyboard nav, screen reader)
- Print view

**Key Takeaways:**
- Complete user flows from start to finish
- All major states demonstrated
- Mobile-first responsive adaptations
- Accessibility patterns in practice
- Print-friendly output

**For:** UX designers, product managers, stakeholders

---

## Quick Reference

### Color Palette

| Category | Hex | Usage |
|----------|-----|-------|
| Built Environment | `#0369a1` | Blue nodes/edges |
| Social Environment | `#9333ea` | Purple nodes/edges |
| Economic | `#059669` | Green nodes/edges |
| Political | `#dc2626` | Red nodes/edges |
| Biological | `#ea580c` | Orange nodes/edges |
| Default | `#6b7280` | Gray nodes/edges |

**Evidence Quality:**
- **A** (High): `#10b981` Green
- **B** (Moderate): `#f59e0b` Amber
- **C** (Low): `#ef4444` Red

### Typography Scale

| Name | Size | Weight | Usage |
|------|------|--------|-------|
| H1 | 30px | 700 | Section headers |
| H2 | 24px | 600 | Panel titles |
| H3 | 20px | 600 | Subsection headers |
| Body | 14px | 400 | Default text |
| Caption | 12px | 400 | Metadata |

### Spacing

Base unit: **4px**

Common values: 4px, 8px, 12px, 16px, 24px, 32px, 48px, 64px

### Breakpoints

| Name | Width | Layout |
|------|-------|--------|
| Mobile | <640px | Single column, stacked |
| Tablet | 640-1024px | Hybrid, collapsible sidebar |
| Desktop | 1024-1536px | Two-column, fixed sidebar |
| Large | >1536px | Multi-panel, expandable |

---

## Implementation Roadmap

### Phase 1: Foundation (Weeks 1-2)
- [ ] Set up design system (Tailwind config)
- [ ] Create base components (Button, Input, Badge, etc.)
- [ ] Implement layout components (Panel, Grid, Stack)
- [ ] Set up Storybook for component documentation
- [ ] Establish accessibility testing workflow

### Phase 2: Core Visualization (Weeks 3-4)
- [ ] Implement D3 force-directed graph
- [ ] Build node and edge rendering with all states
- [ ] Add zoom, pan, and navigation controls
- [ ] Implement legend component
- [ ] Optimize for 400 nodes performance

### Phase 3: Interactions (Weeks 5-6)
- [ ] Click handlers (nodes, edges, empty space)
- [ ] Hover behaviors and tooltips
- [ ] Drag-to-reposition nodes
- [ ] Multi-select functionality
- [ ] Keyboard navigation (Tab, Arrow keys)

### Phase 4: Panels (Weeks 7-8)
- [ ] Node detail panel
- [ ] Mechanism detail panel
- [ ] Filter panel
- [ ] Search results panel
- [ ] Panel resize/collapse functionality

### Phase 5: Advanced Features (Weeks 9-10)
- [ ] Pathway Explorer tab
- [ ] Node Library tab
- [ ] Evidence Base tab
- [ ] Pathway highlighting
- [ ] Export functionality

### Phase 6: Polish & Accessibility (Weeks 11-12)
- [ ] Responsive layouts (tablet, mobile)
- [ ] Loading and empty states
- [ ] Error handling
- [ ] Complete keyboard navigation
- [ ] Screen reader optimization
- [ ] Accessibility audit (WCAG AA)

### Phase 7: Testing & Launch (Weeks 13-14)
- [ ] Unit tests (Jest)
- [ ] Integration tests (React Testing Library)
- [ ] E2E tests (Playwright)
- [ ] Visual regression tests
- [ ] Performance optimization
- [ ] Browser compatibility testing
- [ ] User acceptance testing
- [ ] Production deployment

---

## Design Tokens

### Installation

```bash
cd frontend
npm install
```

### Tailwind Configuration

The design system is implemented in `frontend/tailwind.config.js`:

```javascript
module.exports = {
  theme: {
    extend: {
      colors: {
        primary: {
          500: '#0ea5e9',
          600: '#0284c7',
          700: '#0369a1',
        },
        category: {
          built: '#0369a1',
          social: '#9333ea',
          economic: '#059669',
          political: '#dc2626',
          biological: '#ea580c',
        },
        evidence: {
          A: '#10b981',
          B: '#f59e0b',
          C: '#ef4444',
        },
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
        mono: ['Monaco', 'monospace'],
      },
    },
  },
}
```

---

## Component Usage Examples

### Button Component

```tsx
import { Button } from '@/components/base/Button'

// Primary button
<Button variant="primary" size="md" onClick={handleClick}>
  Apply Filters
</Button>

// With icon
<Button variant="primary" icon={<SearchIcon />} iconPosition="left">
  Search
</Button>

// Loading state
<Button variant="primary" loading>
  Loading...
</Button>
```

### Node Card Component

```tsx
import { NodeCard } from '@/components/domain/NodeCard'

<NodeCard
  node={nodeData}
  onClick={() => handleNodeClick(nodeData.id)}
  showConnections={true}
/>
```

### Evidence Badge Component

```tsx
import { EvidenceBadge } from '@/components/domain/EvidenceBadge'

<EvidenceBadge
  quality="A"
  size="md"
  showLabel={true}
  tooltip={true}
/>
```

---

## Accessibility Checklist

Every component and view must meet these requirements:

- [ ] **Keyboard Navigation**: All interactive elements accessible via Tab, Enter/Space
- [ ] **Focus Indicators**: Visible 2px ring on all focused elements
- [ ] **Color Contrast**: Minimum 4.5:1 for text, 3:1 for interactive elements
- [ ] **ARIA Labels**: All icon buttons and complex widgets labeled
- [ ] **Screen Reader**: Meaningful announcements for dynamic content
- [ ] **Touch Targets**: Minimum 44×44px on mobile
- [ ] **Reduced Motion**: Respect `prefers-reduced-motion` setting
- [ ] **Alt Text**: All meaningful images have descriptive alt text
- [ ] **Semantic HTML**: Use proper heading hierarchy, landmarks
- [ ] **Error Messages**: Clear, actionable error descriptions

---

## Design Review Process

### Before Implementation
1. Review relevant design docs in this directory
2. Check existing components in Storybook
3. Validate against design system (colors, spacing, typography)
4. Ensure accessibility requirements are clear

### During Implementation
1. Build component in isolation (Storybook)
2. Test all states (default, hover, focus, active, disabled)
3. Run accessibility tests (axe-core)
4. Test keyboard navigation
5. Test responsive behavior

### Before Merge
1. Unit tests passing (Jest)
2. Accessibility tests passing (axe)
3. Visual regression tests passing (Playwright)
4. Code review by design system maintainer
5. UX review by designer
6. Documentation updated (Storybook, README)

---

## Resources

### Design Tools
- **Figma**: High-fidelity mockups (based on these docs)
- **Storybook**: Component library documentation and testing
- **ColorOracle**: Color blindness simulation
- **axe DevTools**: Accessibility testing browser extension

### Development Tools
- **React 18**: UI framework
- **TypeScript**: Type safety
- **Tailwind CSS**: Utility-first styling
- **D3.js**: Data visualization
- **Cytoscape**: Graph algorithms
- **Zustand**: State management
- **React Query**: Server state

### Testing Tools
- **Jest**: Unit testing
- **React Testing Library**: Component testing
- **Playwright**: E2E testing
- **axe-core**: Accessibility testing

### Documentation
- [React Documentation](https://react.dev/)
- [Tailwind CSS Docs](https://tailwindcss.com/docs)
- [D3.js Documentation](https://d3js.org/)
- [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
- [ARIA Authoring Practices](https://www.w3.org/WAI/ARIA/apg/)

---

## Contributing

### Adding New Components

1. Create component in appropriate directory (`base/`, `composite/`, `domain/`)
2. Write TypeScript interface for props
3. Implement all required states
4. Add accessibility attributes (ARIA, keyboard support)
5. Write unit tests (Jest)
6. Write accessibility tests (axe)
7. Create Storybook story with all variants
8. Update this documentation

### Modifying Design System

1. Propose change in design review meeting
2. Update relevant documentation first
3. Update Tailwind config
4. Update affected components
5. Run full test suite
6. Update Storybook examples
7. Communicate changes to team

---

## FAQ

**Q: What's the difference between MVP and Phase 2?**
A: MVP shows topology and direction only (qualitative). Phase 2 adds quantification (effect sizes, ROI, simulations).

**Q: Why force-directed layout instead of hierarchical?**
A: Health systems have complex feedback loops and lateral relationships that don't fit strict hierarchies.

**Q: How do we handle 400 nodes and 2000 edges performance?**
A: Viewport culling, level-of-detail rendering, Canvas API (not SVG), and Web Workers for physics calculations.

**Q: What browsers do we support?**
A: Modern evergreen browsers (Chrome, Firefox, Safari, Edge). IE11 not supported.

**Q: How do we ensure accessibility with complex graphs?**
A: Keyboard navigation (arrow keys), screen reader announcements, alternative table view, and ARIA labels on all elements.

**Q: Can users customize the layout?**
A: Yes - resizable panels, collapsible sidebars, filter preferences saved to localStorage.

**Q: How do we handle mobile interactions?**
A: Touch gestures (pinch zoom, drag pan), full-screen panels, simplified controls, larger touch targets (44×44px).

**Q: What's the data update frequency?**
A: MVP uses static data loaded on page load. Phase 2 may add real-time updates via WebSocket.

---

## Support

### For Designers
- Questions about visual design: Review [01_DESIGN_SYSTEM.md](./01_DESIGN_SYSTEM.md)
- Questions about layouts: Review [02_DASHBOARD_LAYOUT.md](./02_DASHBOARD_LAYOUT.md)
- Questions about interactions: Review [06_MOCKUPS.md](./06_MOCKUPS.md)

### For Developers
- Questions about components: Review [05_COMPONENT_LIBRARY.md](./05_COMPONENT_LIBRARY.md)
- Questions about graph visualization: Review [03_SYSTEMS_MAP_VISUALIZATION.md](./03_SYSTEMS_MAP_VISUALIZATION.md)
- Questions about panels: Review [04_DETAIL_PANELS.md](./04_DETAIL_PANELS.md)

### For Product Managers
- Questions about user flows: Review [06_MOCKUPS.md](./06_MOCKUPS.md)
- Questions about features: Review [02_DASHBOARD_LAYOUT.md](./02_DASHBOARD_LAYOUT.md)
- Questions about scope: Review MVP constraints in all documents

---

## Version History

**v1.0** (2025-11-16)
- Initial design documentation
- All 6 core documents completed
- MVP scope defined
- Component library specified
- Accessibility standards established

**Future Versions**
- v1.1: High-fidelity Figma mockups
- v1.2: User testing feedback incorporated
- v2.0: Phase 2 quantification features

---

## License

Internal documentation for the HealthSystems platform.
Not for external distribution.

---

**Ready to implement?** Start with the [Design System](./01_DESIGN_SYSTEM.md), then move through the documents in order. Each document builds on the previous one.

**Questions?** Contact the design team or open an issue in the project repository.
