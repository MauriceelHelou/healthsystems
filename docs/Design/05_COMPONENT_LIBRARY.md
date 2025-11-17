# Component Library Specification
**HealthSystems Platform - Reusable UI Components**

Version: 1.0
Last Updated: 2025-11-16
Status: MVP Scope (Topology & Direction Only)

---

## Overview

This document specifies the reusable UI components that form the building blocks of the HealthSystems dashboard. All components follow the design system principles, are accessible (WCAG AA), and support keyboard navigation.

**Technology**: React 18 + TypeScript + Tailwind CSS

---

## 1. Component Architecture

### Component Categories

1. **Base Components**: Atomic UI elements (Button, Input, Badge)
2. **Composite Components**: Combined elements (Card, Modal, Dropdown)
3. **Domain Components**: Domain-specific (NodeCard, MechanismList)
4. **Layout Components**: Structure (Panel, Grid, Stack)
5. **Visualization Components**: D3/Graph wrappers

### File Structure

```
frontend/src/components/
├── base/
│   ├── Button.tsx
│   ├── Input.tsx
│   ├── Badge.tsx
│   ├── Icon.tsx
│   └── Tooltip.tsx
├── composite/
│   ├── Card.tsx
│   ├── Modal.tsx
│   ├── Dropdown.tsx
│   ├── Tabs.tsx
│   └── Accordion.tsx
├── domain/
│   ├── NodeCard.tsx
│   ├── MechanismCard.tsx
│   ├── EvidenceBadge.tsx
│   ├── CategoryBadge.tsx
│   └── PathwayCard.tsx
├── layout/
│   ├── Panel.tsx
│   ├── Grid.tsx
│   ├── Stack.tsx
│   └── Container.tsx
└── visualization/
    ├── MechanismGraph.tsx (existing)
    ├── Legend.tsx
    └── GraphControls.tsx
```

---

## 2. Base Components

### Button

**Purpose**: Clickable action elements
**Variants**: Primary, Secondary, Text, Icon

#### Props
```typescript
interface ButtonProps {
  variant?: 'primary' | 'secondary' | 'text' | 'icon'
  size?: 'sm' | 'md' | 'lg'
  disabled?: boolean
  loading?: boolean
  icon?: React.ReactNode
  iconPosition?: 'left' | 'right'
  onClick?: () => void
  children: React.ReactNode
  className?: string
  ariaLabel?: string
}
```

#### Variants

**Primary Button**
```tsx
<Button variant="primary" size="md">
  Apply Filters
</Button>
```
```css
background: primary-600 (#0284c7)
color: white
padding: 8px 16px (md)
border-radius: 6px
font-weight: 600
hover: primary-700
active: primary-800, scale(0.98)
disabled: opacity 0.5, cursor not-allowed
```

**Secondary Button**
```tsx
<Button variant="secondary" size="md">
  Cancel
</Button>
```
```css
background: white
color: primary-600
border: 1px solid primary-600
padding: 8px 16px
hover: primary-50 background
```

**Text Button**
```tsx
<Button variant="text" size="sm">
  Learn More
</Button>
```
```css
background: transparent
color: primary-600
padding: 4px 8px
hover: primary-50 background
```

**Icon Button**
```tsx
<Button variant="icon" ariaLabel="Close panel">
  <XIcon />
</Button>
```
```css
background: transparent
padding: 8px (square)
border-radius: 6px
hover: gray-100 background
```

#### Sizes
| Size | Padding | Font Size | Icon Size |
|------|---------|-----------|-----------|
| sm | 4px 12px | 13px | 16px |
| md | 8px 16px | 14px | 20px |
| lg | 12px 24px | 16px | 24px |

#### States
- **Loading**: Show spinner, disable interaction
- **Disabled**: Opacity 0.5, cursor not-allowed
- **Focus**: Ring 2px primary-500, offset 2px

---

### Input

**Purpose**: Text input fields
**Variants**: Text, Search, Number

#### Props
```typescript
interface InputProps {
  type?: 'text' | 'search' | 'number' | 'email'
  placeholder?: string
  value: string
  onChange: (value: string) => void
  disabled?: boolean
  error?: string
  label?: string
  helpText?: string
  icon?: React.ReactNode
  iconPosition?: 'left' | 'right'
  className?: string
}
```

#### Design

```tsx
<Input
  label="Search nodes"
  placeholder="Type to search..."
  icon={<SearchIcon />}
  iconPosition="left"
/>
```

**Layout**:
```
Label (optional)
┌─────────────────────────────────┐
│ [🔍] Type to search...          │  ← Icon + Input
└─────────────────────────────────┘
Help text or error message (optional)
```

**Styles**:
```css
border: 1px solid gray-300
border-radius: 6px
padding: 8px 12px
font-size: 14px
background: white
placeholder: gray-400

focus:
  border: primary-500
  ring: 2px primary-500, offset 0

error:
  border: error-500
  ring: 2px error-500
```

#### States
- **Default**: Gray border
- **Focus**: Blue border + ring
- **Error**: Red border + error message below
- **Disabled**: Gray background, cursor not-allowed

---

### Badge

**Purpose**: Status indicators, labels
**Variants**: Default, Pill, Dot

#### Props
```typescript
interface BadgeProps {
  variant?: 'default' | 'pill' | 'dot'
  color?: 'primary' | 'success' | 'warning' | 'error' | 'gray'
  size?: 'sm' | 'md' | 'lg'
  children: React.ReactNode
  icon?: React.ReactNode
}
```

#### Variants

**Default Badge**
```tsx
<Badge color="primary" size="md">
  New
</Badge>
```
```css
padding: 2px 8px
border-radius: 4px
font-size: 12px
font-weight: 500
background: primary-100
color: primary-700
```

**Pill Badge**
```tsx
<Badge variant="pill" color="success">
  Evidence: A
</Badge>
```
```css
border-radius: 9999px (full)
padding: 4px 12px
```

**Dot Badge** (for notifications)
```tsx
<Badge variant="dot" color="error" />
```
```css
width: 8px
height: 8px
border-radius: 50%
background: error-500
```

#### Colors
| Color | Background | Text | Border |
|-------|------------|------|--------|
| primary | primary-100 | primary-700 | primary-200 |
| success | green-100 | green-700 | green-200 |
| warning | amber-100 | amber-700 | amber-200 |
| error | red-100 | red-700 | red-200 |
| gray | gray-100 | gray-700 | gray-200 |

---

### Icon

**Purpose**: Consistent icon rendering
**Library**: Heroicons (outline style preferred)

#### Props
```typescript
interface IconProps {
  name: string  // Icon name from Heroicons
  size?: 'xs' | 'sm' | 'md' | 'lg' | 'xl'
  color?: string  // Tailwind color class
  className?: string
}
```

#### Usage
```tsx
<Icon name="search" size="md" color="gray-500" />
<Icon name="x" size="sm" />
```

#### Sizes
| Size | Pixels |
|------|--------|
| xs | 12px |
| sm | 16px |
| md | 20px |
| lg | 24px |
| xl | 32px |

---

### Tooltip

**Purpose**: Contextual information on hover
**Variants**: Top, Bottom, Left, Right

#### Props
```typescript
interface TooltipProps {
  content: React.ReactNode
  position?: 'top' | 'bottom' | 'left' | 'right'
  delay?: number  // ms before showing
  children: React.ReactElement
}
```

#### Usage
```tsx
<Tooltip content="Click to view details" position="top">
  <Button>Learn More</Button>
</Tooltip>
```

#### Design
```
┌─────────────────────┐
│ Click to view details│  ← Tooltip (dark background)
└──────────┬──────────┘
           ▼  ← Arrow pointer
      [ Button ]
```

**Styles**:
```css
background: gray-900
color: white
padding: 6px 12px
border-radius: 6px
font-size: 12px
max-width: 200px
box-shadow: shadow-lg
arrow: 6px triangle, matching background
```

**Behavior**:
- Delay: 300ms (configurable)
- Fade in: 150ms
- Mouse leave: Fade out 100ms
- Touch: Tap to show, tap outside to hide

---

## 3. Composite Components

### Card

**Purpose**: Content container with optional header/footer
**Variants**: Default, Hover, Clickable

#### Props
```typescript
interface CardProps {
  header?: React.ReactNode
  footer?: React.ReactNode
  clickable?: boolean
  onClick?: () => void
  children: React.ReactNode
  className?: string
}
```

#### Design

```
┌─────────────────────────────────┐
│ HEADER (optional)               │
├─────────────────────────────────┤
│                                 │
│ CONTENT (children)              │
│                                 │
├─────────────────────────────────┤
│ FOOTER (optional)               │
└─────────────────────────────────┘
```

**Styles**:
```css
background: white
border: 1px solid gray-200
border-radius: 8px
padding: 16px
box-shadow: none (default)

hover (if clickable):
  border-color: primary-300
  box-shadow: shadow-md
  cursor: pointer
  transform: translateY(-2px)
  transition: 200ms ease-out
```

---

### Modal

**Purpose**: Overlay dialogs
**Variants**: Small, Medium, Large, Fullscreen

#### Props
```typescript
interface ModalProps {
  isOpen: boolean
  onClose: () => void
  title: string
  size?: 'sm' | 'md' | 'lg' | 'full'
  footer?: React.ReactNode
  children: React.ReactNode
  closeOnBackdrop?: boolean
}
```

#### Design

```
BACKDROP (rgba(0,0,0,0.5))
┌─────────────────────────────────┐
│                                 │
│   ┌─────────────────────────┐   │
│   │ Title               [X] │   │
│   ├─────────────────────────┤   │
│   │                         │   │
│   │ Content                 │   │
│   │                         │   │
│   ├─────────────────────────┤   │
│   │ [Cancel]     [Confirm]  │   │
│   └─────────────────────────┘   │
│                                 │
└─────────────────────────────────┘
```

**Styles**:
```css
backdrop:
  position: fixed
  background: rgba(0, 0, 0, 0.5)
  z-index: 40

modal:
  position: fixed
  top: 50%, left: 50%
  transform: translate(-50%, -50%)
  background: white
  border-radius: 8px
  box-shadow: shadow-xl
  max-height: 90vh
  overflow-y: auto
```

**Sizes**:
| Size | Width |
|------|-------|
| sm | 400px |
| md | 600px |
| lg | 800px |
| full | 90vw |

**Behavior**:
- **Open**: Fade in backdrop (200ms), scale in modal (200ms)
- **Close**: ESC key, X button, or backdrop click
- **Focus Trap**: Tab cycles within modal
- **Scroll Lock**: Prevent body scroll when open

---

### Dropdown

**Purpose**: Menu of selectable options
**Variants**: Default, Multi-select, Searchable

#### Props
```typescript
interface DropdownProps {
  trigger: React.ReactElement  // Button or element
  items: DropdownItem[]
  onSelect: (value: string) => void
  position?: 'bottom-left' | 'bottom-right' | 'top-left' | 'top-right'
  searchable?: boolean
  multiSelect?: boolean
}

interface DropdownItem {
  value: string
  label: string
  icon?: React.ReactNode
  disabled?: boolean
}
```

#### Design

```
[ Trigger Button ▼ ]
     ↓
┌─────────────────────────┐
│ [🔍] Search... (option) │  ← Searchable
├─────────────────────────┤
│ ☑ Option 1              │  ← Multi-select checkbox
│ ☐ Option 2              │
│ ☐ Option 3 (disabled)   │
├─────────────────────────┤
│ [Apply]      [Cancel]   │  ← Multi-select actions
└─────────────────────────┘
```

**Styles**:
```css
dropdown-menu:
  background: white
  border: 1px solid gray-200
  border-radius: 6px
  box-shadow: shadow-lg
  min-width: 200px
  max-height: 300px
  overflow-y: auto
  z-index: 10

item:
  padding: 8px 12px
  cursor: pointer
  hover: background gray-100
  active: background primary-50
  disabled: opacity 0.5, cursor not-allowed
```

---

### Tabs

**Purpose**: Switch between multiple views
**Variants**: Underline, Pills, Enclosed

#### Props
```typescript
interface TabsProps {
  variant?: 'underline' | 'pills' | 'enclosed'
  tabs: TabItem[]
  activeTab: string
  onChange: (tabId: string) => void
}

interface TabItem {
  id: string
  label: string
  icon?: React.ReactNode
  disabled?: boolean
}
```

#### Variants

**Underline Tabs** (recommended for main navigation)
```
┌─────────────────────────────────────────┐
│ Systems Map  Pathway Explorer  Library  │
│ ══════════                               │  ← Active indicator
└─────────────────────────────────────────┘
```

**Pills Tabs**
```
┌─────────────────────────────────────────┐
│ [Systems Map] [Pathway] [Library]       │
│   (filled)      (outline)  (outline)    │
└─────────────────────────────────────────┘
```

**Styles** (Underline):
```css
tab:
  padding: 12px 16px
  font-weight: 500
  color: gray-600
  border-bottom: 2px solid transparent
  cursor: pointer

active:
  color: primary-600
  border-bottom-color: primary-600

hover:
  color: gray-900
  background: gray-50
```

---

### Accordion

**Purpose**: Expandable content sections
**Variants**: Single, Multiple expand

#### Props
```typescript
interface AccordionProps {
  items: AccordionItem[]
  allowMultiple?: boolean  // Allow multiple open at once
  defaultOpen?: string[]   // Initially open item IDs
}

interface AccordionItem {
  id: string
  title: string
  content: React.ReactNode
  icon?: React.ReactNode
}
```

#### Design

```
┌─────────────────────────────────┐
│ Section 1                  [▼]  │  ← Collapsed
├─────────────────────────────────┤
│ Section 2                  [▲]  │  ← Expanded
│ ─────────────────────────────── │
│ Expanded content here...        │
│ • Detail 1                      │
│ • Detail 2                      │
├─────────────────────────────────┤
│ Section 3                  [▼]  │
└─────────────────────────────────┘
```

**Styles**:
```css
header:
  padding: 12px 16px
  cursor: pointer
  background: white
  border-bottom: 1px solid gray-200
  hover: background gray-50

content:
  padding: 16px
  background: gray-50
  animation: slideDown 200ms ease-out
```

**Animation**:
```css
@keyframes slideDown {
  from {
    max-height: 0
    opacity: 0
  }
  to {
    max-height: 500px
    opacity: 1
  }
}
```

---

## 4. Domain Components

### NodeCard

**Purpose**: Display node summary in lists/grids
**Usage**: Node Library, Search Results

#### Props
```typescript
interface NodeCardProps {
  node: MechanismNode
  onClick?: () => void
  showConnections?: boolean
  compact?: boolean
}
```

#### Design

```
┌───────────────────────────────────┐
│ [▪] Community Health Workers      │  ← Type icon + name
│ Built Environment · Structural    │  ← Category + type
│ ───────────────────────────────── │
│ 15 outgoing · 3 incoming          │  ← Connections
│                                   │
│ [View Details] [View in Map]      │  ← Actions
└───────────────────────────────────┘
```

**Compact Version**:
```
┌───────────────────────────────────┐
│ [▪] Community Health Workers      │
│ 15 → 3 ←                          │  ← Compact connections
└───────────────────────────────────┘
```

---

### MechanismCard

**Purpose**: Display mechanism summary
**Usage**: Evidence Base tab, Search Results

#### Props
```typescript
interface MechanismCardProps {
  mechanism: Mechanism
  onClick?: () => void
  showEvidence?: boolean
}
```

#### Design

```
┌───────────────────────────────────┐
│ CHWs → Healthcare Continuity  [A] │  ← Evidence badge
│ Positive relationship (+)         │
│ ───────────────────────────────── │
│ "Community health workers improve │
│ continuity through..."            │  ← Description snippet
│                                   │
│ 12 studies · Evidence: High       │  ← Meta info
│ [View Mechanism]                  │
└───────────────────────────────────┘
```

---

### EvidenceBadge

**Purpose**: Display evidence quality rating
**Usage**: Graphs, cards, lists

#### Props
```typescript
interface EvidenceBadgeProps {
  quality: 'A' | 'B' | 'C' | null
  size?: 'sm' | 'md' | 'lg'
  showLabel?: boolean
  tooltip?: boolean
}
```

#### Design

**Small (16px)**:
```
[A]  ← Circle, 16px diameter
```

**Medium (24px) with label**:
```
[A] High Quality
```

**Large (32px) with tooltip**:
```
[A]  ← Hover for tooltip
     "Evidence Quality: A - High confidence,
      based on 12 RCTs and systematic reviews"
```

**Colors** (from design system):
- A: Green border + text
- B: Amber border + text
- C: Red border + text
- null: Gray border + "?"

---

### CategoryBadge

**Purpose**: Display mechanism category
**Usage**: Node cards, filters

#### Props
```typescript
interface CategoryBadgeProps {
  category: 'built_environment' | 'social_environment' |
            'economic' | 'political' | 'biological' | 'default'
  size?: 'sm' | 'md'
  clickable?: boolean
  onClick?: () => void
}
```

#### Design

```
[Built Environment]  ← Pill shape, category color
```

**Styles**:
```css
background: category-color at 20% opacity
color: category-color (dark shade)
padding: 4px 12px
border-radius: 9999px
font-size: 12px
font-weight: 500
```

---

### PathwayCard

**Purpose**: Display pathway summary in list
**Usage**: Pathway Explorer panel

#### Props
```typescript
interface PathwayCardProps {
  pathway: Pathway
  onViewInMap: () => void
  expandable?: boolean
}
```

#### Design (see Detail Panels doc for full spec)

```
┌─────────────────────────────────────────┐
│ Path 1: Direct via Continuity  [View]  │
│ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ │
│ Evidence: A · 2 mechanisms              │
│                                         │
│ 1. CHWs → Continuity Index          [A]│
│ 2. Continuity Index → ED Visits     [A]│
│                                         │
│ Overall: CHWs reduce ED Visits ✓        │
│ [Expand Details ▼]                      │
└─────────────────────────────────────────┘
```

---

## 5. Layout Components

### Panel

**Purpose**: Resizable sidebar container
**Usage**: Detail panels, filter panels

#### Props
```typescript
interface PanelProps {
  title: string
  icon?: React.ReactNode
  defaultWidth?: number
  minWidth?: number
  maxWidth?: number
  resizable?: boolean
  collapsible?: boolean
  onClose: () => void
  children: React.ReactNode
}
```

**Features**:
- Resize handle on left edge
- Minimize/expand/close buttons
- Header with title
- Scrollable content area
- Optional footer

(See Detail Panels doc for full specification)

---

### Grid

**Purpose**: Responsive grid layout
**Usage**: Node library, card grids

#### Props
```typescript
interface GridProps {
  columns?: number | 'auto'  // Auto-fit based on item size
  gap?: number  // Tailwind spacing scale
  children: React.ReactNode
  className?: string
}
```

#### Usage
```tsx
<Grid columns="auto" gap={4}>
  <NodeCard node={node1} />
  <NodeCard node={node2} />
  <NodeCard node={node3} />
</Grid>
```

**Responsive**:
```css
grid-template-columns: repeat(auto-fit, minmax(280px, 1fr))
gap: 16px (gap-4)

@media (max-width: 768px) {
  grid-template-columns: 1fr  /* Single column */
}
```

---

### Stack

**Purpose**: Vertical or horizontal spacing
**Usage**: Consistent spacing between elements

#### Props
```typescript
interface StackProps {
  direction?: 'vertical' | 'horizontal'
  spacing?: number  // Tailwind scale (0-16)
  align?: 'start' | 'center' | 'end' | 'stretch'
  children: React.ReactNode
}
```

#### Usage
```tsx
<Stack direction="vertical" spacing={4}>
  <Header />
  <Content />
  <Footer />
</Stack>
```

---

### Container

**Purpose**: Centered content with max-width
**Usage**: Page layouts

#### Props
```typescript
interface ContainerProps {
  maxWidth?: 'sm' | 'md' | 'lg' | 'xl' | 'full'
  padding?: boolean  // Add horizontal padding
  children: React.ReactNode
}
```

**Max Widths**:
| Size | Width |
|------|-------|
| sm | 640px |
| md | 768px |
| lg | 1024px |
| xl | 1280px |
| full | 100% |

---

## 6. Visualization Components

### Legend

**Purpose**: Graph legend with category/evidence info
**Usage**: Systems Map view

#### Props
```typescript
interface LegendProps {
  categories: Category[]
  evidenceQualities: EvidenceQuality[]
  directions: Direction[]
  onCategoryClick?: (category: string) => void
  collapsible?: boolean
  position?: 'bottom-left' | 'bottom-right' | 'top-left' | 'top-right'
}
```

(See Systems Map Visualization doc for full specification)

---

### GraphControls

**Purpose**: Zoom, pan, filter controls for graph
**Usage**: Systems Map view

#### Props
```typescript
interface GraphControlsProps {
  onZoomIn: () => void
  onZoomOut: () => void
  onFitScreen: () => void
  onReset: () => void
  onSearch: () => void
  onFilter: () => void
  currentZoom: number
}
```

**Layout**:
```
┌─────────────────────────────────┐
│ [🔍] [⚙] [+] [−] [⊡] [↻]       │
│ Search Filter Zoom Fit Reset    │
└─────────────────────────────────┘
```

---

## 7. Accessibility Guidelines

### All Components Must Include:

1. **Keyboard Navigation**
   - Tab: Focus next element
   - Shift+Tab: Focus previous
   - Enter/Space: Activate
   - Arrow keys: Navigate lists/options
   - Esc: Close/cancel

2. **Focus Indicators**
   ```css
   &:focus-visible {
     outline: none;
     ring: 2px solid var(--primary-500);
     ring-offset: 2px;
   }
   ```

3. **ARIA Attributes**
   - `aria-label`: For icon buttons
   - `aria-describedby`: For help text
   - `aria-expanded`: For collapsible elements
   - `aria-selected`: For tabs
   - `role`: When semantic HTML insufficient

4. **Screen Reader Text**
   ```tsx
   <span className="sr-only">
     Close panel
   </span>
   <Icon name="x" aria-hidden="true" />
   ```

5. **Color Contrast**
   - Text: Minimum 4.5:1 ratio
   - Large text (18px+): Minimum 3:1
   - Interactive elements: 3:1 border/background

6. **Touch Targets**
   - Minimum 44×44px for mobile
   - Adequate spacing between targets

---

## 8. Testing Strategy

### Unit Tests (Jest + React Testing Library)

```tsx
// Button.test.tsx
describe('Button', () => {
  it('renders with correct variant styles', () => {
    const { getByRole } = render(
      <Button variant="primary">Click me</Button>
    )
    const button = getByRole('button')
    expect(button).toHaveClass('bg-primary-600')
  })

  it('calls onClick when clicked', () => {
    const handleClick = jest.fn()
    const { getByRole } = render(
      <Button onClick={handleClick}>Click</Button>
    )
    fireEvent.click(getByRole('button'))
    expect(handleClick).toHaveBeenCalledTimes(1)
  })

  it('is keyboard accessible', () => {
    const handleClick = jest.fn()
    const { getByRole } = render(<Button onClick={handleClick}>Click</Button>)
    const button = getByRole('button')
    button.focus()
    fireEvent.keyDown(button, { key: 'Enter' })
    expect(handleClick).toHaveBeenCalled()
  })
})
```

### Accessibility Tests (axe-core)

```tsx
import { axe, toHaveNoViolations } from 'jest-axe'
expect.extend(toHaveNoViolations)

it('should have no accessibility violations', async () => {
  const { container } = render(<Button>Click me</Button>)
  const results = await axe(container)
  expect(results).toHaveNoViolations()
})
```

### Visual Regression Tests (Playwright)

```tsx
test('Button renders correctly', async ({ page }) => {
  await page.goto('/component-library/button')
  await expect(page).toHaveScreenshot('button-primary.png')
})
```

---

## 9. Storybook Documentation

### Every component should have a Storybook story:

```tsx
// Button.stories.tsx
import { Button } from './Button'

export default {
  title: 'Base/Button',
  component: Button,
  argTypes: {
    variant: {
      control: 'select',
      options: ['primary', 'secondary', 'text', 'icon']
    },
    size: {
      control: 'select',
      options: ['sm', 'md', 'lg']
    }
  }
}

export const Primary = {
  args: {
    variant: 'primary',
    children: 'Primary Button'
  }
}

export const WithIcon = {
  args: {
    variant: 'primary',
    icon: <SearchIcon />,
    iconPosition: 'left',
    children: 'Search'
  }
}

export const Loading = {
  args: {
    variant: 'primary',
    loading: true,
    children: 'Loading...'
  }
}
```

---

## 10. Implementation Checklist

### Phase 1: Base Components
- [ ] Button (all variants)
- [ ] Input (text, search)
- [ ] Badge (all variants)
- [ ] Icon wrapper
- [ ] Tooltip

### Phase 2: Composite Components
- [ ] Card
- [ ] Modal
- [ ] Dropdown
- [ ] Tabs
- [ ] Accordion

### Phase 3: Domain Components
- [ ] NodeCard
- [ ] MechanismCard
- [ ] EvidenceBadge
- [ ] CategoryBadge
- [ ] PathwayCard

### Phase 4: Layout Components
- [ ] Panel (resizable)
- [ ] Grid
- [ ] Stack
- [ ] Container

### Phase 5: Visualization Components
- [ ] Legend
- [ ] GraphControls

### Phase 6: Testing & Documentation
- [ ] Unit tests for all components
- [ ] Accessibility tests (axe)
- [ ] Storybook stories
- [ ] Visual regression tests
- [ ] Component documentation

### Phase 7: Optimization
- [ ] Code splitting
- [ ] Lazy loading
- [ ] Memoization (React.memo)
- [ ] Bundle size analysis

---

**Next Document**: [06_MOCKUPS.md](./06_MOCKUPS.md) - Visual examples and wireframes
