# Design Quick Reference
**One-Page Cheat Sheet for Developers**

---

## Colors

### Category Colors
```css
Built Environment:  #0369a1  (blue)
Social Environment: #9333ea  (purple)
Economic:           #059669  (green)
Political:          #dc2626  (red)
Biological:         #ea580c  (orange)
Default:            #6b7280  (gray)
```

### Evidence Quality
```css
A (High):      #10b981  (green)
B (Moderate):  #f59e0b  (amber)
C (Low):       #ef4444  (red)
```

### Primary Interactive
```css
Primary:   #0284c7
Hover:     #0369a1
Active:    #1e3a8a
```

### Semantic
```css
Success:   #10b981
Warning:   #f59e0b
Error:     #ef4444
Info:      #3b82f6
```

---

## Typography

```css
Font Family: 'Inter', sans-serif

H1:       30px / 700
H2:       24px / 600
H3:       20px / 600
H4:       18px / 600
Body:     14px / 400
Caption:  12px / 400
```

---

## Spacing

**Base: 4px**

```css
1  = 4px    /* Tiny */
2  = 8px    /* Small */
3  = 12px
4  = 16px   /* Default */
6  = 24px   /* Large */
8  = 32px
12 = 48px
16 = 64px
```

---

## Component Sizes

### Buttons
```css
sm: 4px 12px, 13px text, 16px icon
md: 8px 16px, 14px text, 20px icon  ← Default
lg: 12px 24px, 16px text, 24px icon
```

### Badges
```css
sm: 16px circle
md: 24px circle  ← Default
lg: 32px circle
```

### Icons
```css
xs: 12px
sm: 16px
md: 20px  ← Default
lg: 24px
xl: 32px
```

---

## Layout Dimensions

```css
Header Height:        60px
Sidebar Width:        320px (default), 400px (expanded)
Sidebar Range:        280-480px
Bottom Bar:           40px
Panel Padding:        24px (sides), 16px (vertical)
```

---

## Breakpoints

```css
sm:   640px   /* Tablet */
md:   768px   /* Small laptop */
lg:   1024px  /* Desktop */
xl:   1280px  /* Large desktop */
2xl:  1536px  /* Ultra-wide */
```

---

## Graph Visualization

### Node Sizing
```javascript
radius = Math.sqrt(node.weight) * 20
min: 8px, max: 40px
```

### Node States
```css
default:  80% opacity, 2px stroke
hover:    100% opacity, 3px stroke, scale 1.1
selected: 100% opacity, 4px stroke, ring 2px
dimmed:   30% opacity, 1px stroke
```

### Edge States
```css
default:  40% opacity, 1-3px width
hover:    80% opacity, +1px width
active:   100% opacity, 3px width, animated
dimmed:   15% opacity, 1px width
```

### Zoom Levels
```css
min:  0.2x
max:  4.0x
default: 1.0x
```

---

## Accessibility

### Focus Ring
```css
outline: none
ring: 2px solid #0ea5e9
ring-offset: 2px
```

### Contrast Ratios
```css
Text:              4.5:1  (WCAG AA)
Large Text (18px): 3:1   (WCAG AA)
Interactive:       3:1
```

### Touch Targets
```css
Mobile minimum: 44×44px
Desktop minimum: 32×32px
```

### Keyboard Shortcuts
```
Cmd/Ctrl+K:  Search
F:           Filter
+/-:         Zoom
0:           Reset zoom
R:           Reset view
Esc:         Close panel
Tab:         Navigate
Arrow Keys:  Navigate graph
```

---

## Animation Timing

```css
Instant:   100ms  (hover, focus)
Fast:      200ms  (color, opacity)
Default:   300ms  (panel, modal)
Moderate:  500ms  (graph transitions)
Slow:      1000ms (loading states)
```

### Easing
```css
ease-in:      cubic-bezier(0.4, 0, 1, 1)
ease-out:     cubic-bezier(0, 0, 0.2, 1)      ← Default
ease-in-out:  cubic-bezier(0.4, 0, 0.2, 1)
```

---

## Z-Index Scale

```css
base:      0
dropdown:  10
sticky:    20
overlay:   30
modal:     40
popover:   50
toast:     60
max:       9999
```

---

## Common Patterns

### Button
```tsx
<Button variant="primary" size="md" onClick={fn}>
  Click Me
</Button>
```

### Input
```tsx
<Input
  label="Search"
  placeholder="Type..."
  value={value}
  onChange={setValue}
/>
```

### Badge
```tsx
<Badge variant="pill" color="success">
  Evidence: A
</Badge>
```

### Modal
```tsx
<Modal
  isOpen={open}
  onClose={close}
  title="Node Details"
  size="md"
>
  Content...
</Modal>
```

### Tooltip
```tsx
<Tooltip content="Helpful hint" position="top">
  <Button>Hover Me</Button>
</Tooltip>
```

---

## Panel Structure

```tsx
<Panel
  title="Node Details"
  icon={<Icon name="node" />}
  defaultWidth={320}
  resizable
  collapsible
  onClose={handleClose}
>
  <PanelSection title="Overview">
    Content...
  </PanelSection>
  <PanelSection title="Connections">
    Content...
  </PanelSection>
</Panel>
```

---

## Tailwind Utilities

### Common Classes
```css
/* Layout */
flex flex-col gap-4
grid grid-cols-3 gap-6

/* Spacing */
p-4 px-6 py-3 m-2 mx-auto

/* Typography */
text-sm font-medium text-gray-700
text-lg font-bold text-gray-900

/* Colors */
bg-primary-600 text-white
border border-gray-200

/* Borders */
rounded-md shadow-md
ring-2 ring-primary-500 ring-offset-2

/* States */
hover:bg-primary-700
focus:ring-2 focus:ring-primary-500
disabled:opacity-50
```

---

## ARIA Patterns

### Button
```tsx
<button aria-label="Close panel">
  <XIcon aria-hidden="true" />
</button>
```

### Modal
```tsx
<div
  role="dialog"
  aria-modal="true"
  aria-labelledby="modal-title"
>
  <h2 id="modal-title">Title</h2>
  ...
</div>
```

### Accordion
```tsx
<button
  aria-expanded={isOpen}
  aria-controls="section-1"
>
  Section Header
</button>
<div id="section-1" hidden={!isOpen}>
  Content...
</div>
```

### Graph
```tsx
<svg
  role="img"
  aria-label="Systems map with 400 nodes"
>
  <circle
    role="button"
    aria-label="Community Health Workers node"
    tabIndex={0}
  />
</svg>
```

---

## Testing Snippets

### Unit Test
```tsx
import { render, fireEvent } from '@testing-library/react'

test('button calls onClick', () => {
  const handleClick = jest.fn()
  const { getByRole } = render(
    <Button onClick={handleClick}>Click</Button>
  )
  fireEvent.click(getByRole('button'))
  expect(handleClick).toHaveBeenCalled()
})
```

### Accessibility Test
```tsx
import { axe, toHaveNoViolations } from 'jest-axe'
expect.extend(toHaveNoViolations)

test('no a11y violations', async () => {
  const { container } = render(<Button>Click</Button>)
  expect(await axe(container)).toHaveNoViolations()
})
```

---

## Performance Tips

1. **Memoize expensive computations**
   ```tsx
   const nodes = useMemo(() => filterNodes(data), [data])
   ```

2. **Virtualize long lists**
   ```tsx
   import { FixedSizeList } from 'react-window'
   ```

3. **Debounce search inputs**
   ```tsx
   const debouncedSearch = useDebouncedValue(search, 200)
   ```

4. **Lazy load routes**
   ```tsx
   const PathwayExplorer = lazy(() => import('./PathwayExplorer'))
   ```

5. **Use React.memo for pure components**
   ```tsx
   export const NodeCard = React.memo(NodeCardComponent)
   ```

---

## File Paths Reference

```
frontend/src/
├── components/
│   ├── base/           # Button, Input, Badge, etc.
│   ├── composite/      # Card, Modal, Dropdown, etc.
│   ├── domain/         # NodeCard, MechanismCard, etc.
│   ├── layout/         # Panel, Grid, Stack, etc.
│   └── visualization/  # MechanismGraph, Legend, etc.
├── views/
│   ├── SystemsMapView.tsx
│   ├── PathwayExplorerView.tsx
│   ├── NodeLibraryView.tsx
│   └── EvidenceBaseView.tsx
├── hooks/
│   ├── useForceSimulation.ts
│   ├── useNodeSelection.ts
│   └── usePathwayFinder.ts
├── utils/
│   ├── graphUtils.ts
│   ├── colorUtils.ts
│   └── accessibilityUtils.ts
└── types/
    ├── mechanism.ts
    ├── node.ts
    └── pathway.ts
```

---

## Common Issues & Solutions

### Issue: Graph performance slow with 400 nodes
**Solution:** Use viewport culling, Canvas rendering, Web Workers

### Issue: Focus ring not visible
**Solution:** Ensure `ring-2 ring-primary-500 ring-offset-2` on `:focus-visible`

### Issue: Colors not accessible
**Solution:** Check contrast ratio with WebAIM tool, ensure 4.5:1 minimum

### Issue: Mobile touch targets too small
**Solution:** Ensure minimum 44×44px, add `p-3` if needed

### Issue: Panel resize not smooth
**Solution:** Use `transition-all duration-300 ease-out`

---

## Useful Commands

```bash
# Start development
npm run dev

# Run tests
npm test

# Run accessibility tests
npm run test:a11y

# Build for production
npm run build

# Run Storybook
npm run storybook

# Lint code
npm run lint

# Format code
npm run format
```

---

**Print this page for quick desk reference!**

For full details, see the complete design docs in this directory.
