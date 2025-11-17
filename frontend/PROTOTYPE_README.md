# HealthSystems Dashboard Prototype

**Clean, minimalist dashboard prototype with mock data**

Version: 1.0 - MVP Prototype
Last Updated: 2025-11-16

---

## Overview

This is a functional prototype of the HealthSystems dashboard featuring:
- ✅ Interactive systems map with 400 nodes and 2000+ mechanisms
- ✅ Force-directed D3.js visualization
- ✅ Node and mechanism detail panels
- ✅ Clean, minimalist design system
- ✅ Mock data generators
- ✅ Responsive layout with resizable panels
- ✅ Evidence quality badges and category colors
- ✅ Keyboard navigation and accessibility features

---

## Quick Start

### 1. Install Dependencies

```bash
cd frontend
npm install
```

### Additional Dependencies Needed

You may need to install these packages:

```bash
npm install clsx tailwind-merge
npm install -D @types/d3
```

### 2. Run Development Server

```bash
npm run dev
```

The application will start at `http://localhost:3000`

### 3. Build for Production

```bash
npm run build
```

---

## What's Included

### ✅ Completed Features

#### Core Components
- **Button** - All variants (primary, secondary, text, icon)
- **Input** - Text inputs with labels, errors, icons
- **Badge** - Pills, dots, various colors
- **Icon** - SVG icon library (16 icons)
- **EvidenceBadge** - A/B/C quality indicators
- **CategoryBadge** - 5 category colors

#### Layout Components
- **Header** - Navigation tabs, geography selector, settings
- **Panel** - Resizable, collapsible sidebar
- **DashboardLayout** - Main app structure

#### Views
- **SystemsMapView** - Interactive network graph with controls
  - Graph controls (zoom, pan, filter, search UI)
  - Legend with categories, evidence, stock types
  - Node detail panel with connections
  - Mechanism detail panel with evidence
  - Resizable panels

#### Data & Utilities
- **mockData.ts** - Generates 400 nodes, 2000+ edges
- **colors.ts** - Category and evidence color utilities
- **classNames.ts** - Tailwind merge utility

### 🚧 To Be Implemented

- Pathway Explorer view (full implementation)
- Node Library view (table/grid)
- Evidence Base tab
- Filter panel (functional)
- Search functionality (functional)
- Zoom/pan controls (wired to graph)
- Graph state management (zoom levels, filtering)
- Mobile responsive layouts
- Toast notifications
- Loading states
- Error boundaries

---

## Project Structure

```
frontend/src/
├── App.tsx                      # Main app with routing
├── components/
│   ├── base/                    # Base UI components
│   │   ├── Button.tsx           ✅
│   │   ├── Input.tsx            ✅
│   │   ├── Badge.tsx            ✅
│   │   └── Icon.tsx             ✅
│   └── domain/                  # Domain-specific components
│       ├── EvidenceBadge.tsx    ✅
│       └── CategoryBadge.tsx    ✅
├── layouts/
│   ├── DashboardLayout.tsx      ✅
│   ├── Header.tsx               ✅
│   └── Panel.tsx                ✅
├── views/
│   └── SystemsMapView.tsx       ✅
├── visualizations/
│   └── MechanismGraph.tsx       🔧 Enhanced
├── data/
│   └── mockData.ts              ✅
├── utils/
│   ├── classNames.ts            ✅
│   └── colors.ts                ✅
└── types/
    └── mechanism.ts             ✅ (existing)
```

---

## Design System

### Colors

**Category Colors:**
- Built Environment: `#0369a1` (blue)
- Social Environment: `#9333ea` (purple)
- Economic: `#059669` (green)
- Political: `#dc2626` (red)
- Biological: `#ea580c` (orange)

**Evidence Quality:**
- A (High): `#10b981` (green)
- B (Moderate): `#f59e0b` (amber)
- C (Low): `#ef4444` (red)

### Typography
- Font Family: Inter
- Base Size: 14px
- Scale: 12px, 13px, 14px, 16px, 18px, 20px, 24px, 30px

### Spacing
- Base Unit: 4px
- Common: 4px, 8px, 12px, 16px, 24px, 32px, 48px

---

## Mock Data

### Generated Data
- **400 Nodes**:
  - 5 Crisis outcomes (ED Visits, Hospitalizations, etc.)
  - 100 Built Environment nodes
  - 80 Social Environment nodes
  - 60 Economic nodes
  - 40 Political nodes
  - 35 Biological nodes
  - 80 Default/Mixed nodes

- **2000+ Edges**:
  - Structural → Proxy (800)
  - Proxy → Proxy (600)
  - Proxy → Crisis (400)
  - Structural → Crisis (200)
  - Feedback loops (50+)

### Data Properties
- Nodes have: id, label, category, stockType, weight, connections
- Edges have: id, source, target, direction, strength, evidenceQuality, studyCount
- Mechanisms have: description, citations, moderators

---

## Usage Examples

### Navigating the Dashboard

1. **Systems Map View** (Default):
   - Interactive network graph with force-directed layout
   - Click any node to see details in right panel
   - Click any edge to see mechanism details
   - Use controls (top-right) to zoom, filter, search
   - View legend (bottom-left) for categories and evidence

2. **Node Detail Panel**:
   - Shows node overview
   - Lists outgoing and incoming connections
   - Displays evidence quality for each connection
   - Click connections to view mechanism details
   - Use "View Pathways" to explore paths to outcomes

3. **Mechanism Detail Panel**:
   - Shows mechanism description
   - Displays evidence quality and study count
   - Lists supporting citations
   - Shows moderators (policy, geographic, etc.)

### Keyboard Navigation

- `Tab` - Navigate between interactive elements
- `Enter/Space` - Activate buttons, select nodes
- `Escape` - Close panels
- Arrow keys - Navigate graph (when implemented)

---

## Development Guide

### Adding New Components

1. Create component in appropriate directory
2. Follow existing patterns (TypeScript, props interface)
3. Use design system colors/spacing (via Tailwind)
4. Ensure accessibility (ARIA labels, keyboard nav)
5. Export from index file if needed

### Modifying Mock Data

Edit `frontend/src/data/mockData.ts`:

```typescript
// Change number of nodes
const nodeCount = 100 // Adjust per category

// Change number of edges
for (let i = 0; i < 500; i++) { // Adjust loop count
  edges.push(createEdge(source, target))
}

// Change evidence quality distribution
const qualities = ['A', 'A', 'B', 'C', null] // More A's = higher quality
```

### Styling with Tailwind

Use existing design system classes:

```tsx
// Primary button
className="bg-primary-600 hover:bg-primary-700"

// Category colors
style={{ backgroundColor: getCategoryColor(category) }}

// Evidence badge
<EvidenceBadge quality="A" size="md" showLabel />
```

---

## Known Issues & Limitations

### Current Limitations

1. **Graph Performance**: May be slow with 400 nodes on older devices
   - Optimize with viewport culling (not implemented)
   - Consider Canvas rendering instead of SVG

2. **Zoom/Pan Controls**: UI exists but not wired to graph
   - Need to implement D3 zoom behavior
   - Add zoom level state management

3. **Filtering**: Legend is static, doesn't filter graph yet
   - Need to implement category filtering
   - Add evidence quality filtering

4. **Search**: UI exists but not functional
   - Implement fuzzy search through nodes
   - Highlight matching nodes

5. **Mobile**: Layout exists but needs touch gestures
   - Add pinch-to-zoom
   - Implement touch-friendly controls

### Browser Compatibility

Tested on:
- ✅ Chrome 120+
- ✅ Firefox 121+
- ⚠️ Safari (may have SVG rendering quirks)
- ❌ IE11 (not supported)

---

## Next Steps

### Phase 1: Polish Current Features
- [ ] Wire zoom/pan controls to D3 zoom behavior
- [ ] Implement category filtering
- [ ] Add functional search
- [ ] Fix graph performance (viewport culling)
- [ ] Add loading states

### Phase 2: Additional Views
- [ ] Pathway Explorer (full implementation)
- [ ] Node Library (table/grid views)
- [ ] Evidence Base tab
- [ ] Filter panel (functional)

### Phase 3: Advanced Features
- [ ] Real-time pathway tracing
- [ ] Multi-select nodes
- [ ] Export to PDF/PNG
- [ ] Tour/onboarding
- [ ] User preferences (localStorage)

### Phase 4: Production Ready
- [ ] Error boundaries
- [ ] Analytics integration
- [ ] Performance optimization
- [ ] Accessibility audit (WCAG AA)
- [ ] E2E tests (Playwright)
- [ ] Browser compatibility testing

---

## Troubleshooting

### Common Issues

**Issue: "Module not found: Can't resolve 'clsx'"**
```bash
npm install clsx tailwind-merge
```

**Issue: "Property 'getCategoryColor' does not exist"**
- Ensure `utils/colors.ts` is created
- Check import paths are correct

**Issue: "Cannot find module '../types'"**
- Ensure types are exported from `types/mechanism.ts` or `types/index.ts`

**Issue: Graph not rendering**
- Check browser console for D3 errors
- Ensure mock data is generating correctly
- Verify SVG element exists in DOM

**Issue: Tailwind classes not working**
- Run `npm run dev` to rebuild
- Check `tailwind.config.js` has correct paths
- Verify `index.css` imports Tailwind directives

---

## Resources

- **Design Documentation**: `docs/Design/README.md`
- **Quick Reference**: `docs/Design/QUICK_REFERENCE.md`
- **Implementation Guide**: `docs/Design/IMPLEMENTATION_GUIDE.md`
- **React Docs**: https://react.dev
- **D3.js Docs**: https://d3js.org
- **Tailwind CSS**: https://tailwindcss.com

---

## Support

For questions or issues:
1. Check this README first
2. Review design documentation in `docs/Design/`
3. Check browser console for errors
4. Review existing code patterns

---

**Happy prototyping!** 🚀

This is a working prototype demonstrating the core functionality and design system. Continue building on this foundation to complete the full HealthSystems dashboard.
