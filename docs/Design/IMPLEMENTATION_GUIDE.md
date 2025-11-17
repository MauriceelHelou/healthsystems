# Implementation Guide
**Step-by-Step Guide for Frontend Development Team**

Version: 1.0
Last Updated: 2025-11-16

---

## Overview

This guide provides a practical, step-by-step approach to implementing the HealthSystems dashboard based on the design documentation. It's organized by implementation phases with clear deliverables and dependencies.

---

## Prerequisites

### Required Reading
1. ✅ [Design System](./01_DESIGN_SYSTEM.md) - Foundation
2. ✅ [Dashboard Layout](./02_DASHBOARD_LAYOUT.md) - Screen structure
3. ✅ [Quick Reference](./QUICK_REFERENCE.md) - Developer cheat sheet

### Technical Stack Confirmation
- ✅ React 18.2.0
- ✅ TypeScript 4.9+
- ✅ Tailwind CSS 3.3.6
- ✅ D3.js 7.8.5
- ✅ Cytoscape 3.28.1
- ✅ Zustand 4.4.7 (state management)
- ✅ React Query 5.12.2 (data fetching)
- ✅ React Router 6.20.1

### Development Environment
```bash
cd frontend
npm install
npm run dev  # Starts at http://localhost:3000
```

---

## Phase 1: Foundation Setup (Week 1)

### 1.1 Tailwind Configuration

**File:** `frontend/tailwind.config.js`

**Action:** Extend the existing config with design system values:

```javascript
module.exports = {
  content: ['./src/**/*.{js,jsx,ts,tsx}'],
  theme: {
    extend: {
      colors: {
        // Category colors
        category: {
          built: '#0369a1',
          social: '#9333ea',
          economic: '#059669',
          political: '#dc2626',
          biological: '#ea580c',
          default: '#6b7280',
        },
        // Evidence quality
        evidence: {
          A: '#10b981',
          B: '#f59e0b',
          C: '#ef4444',
        },
      },
      fontFamily: {
        sans: ['Inter', '-apple-system', 'BlinkMacSystemFont', 'sans-serif'],
        mono: ['Monaco', 'Menlo', 'monospace'],
      },
      spacing: {
        // Already has 0-96 scale, confirm 4px base
      },
      borderRadius: {
        sm: '4px',
        md: '6px',
        lg: '8px',
        xl: '12px',
      },
      boxShadow: {
        sm: '0 1px 2px 0 rgba(0, 0, 0, 0.05)',
        md: '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
        lg: '0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)',
        xl: '0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)',
      },
    },
  },
  plugins: [],
}
```

**Test:** Run `npm run dev` and verify no errors

---

### 1.2 Global Styles

**File:** `frontend/src/index.css`

**Action:** Add accessibility and custom styles:

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  /* Font imports */
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

  /* Focus ring customization */
  *:focus-visible {
    @apply outline-none ring-2 ring-primary-500 ring-offset-2;
  }

  /* Reduced motion */
  @media (prefers-reduced-motion: reduce) {
    *,
    *::before,
    *::after {
      animation-duration: 0.01ms !important;
      animation-iteration-count: 1 !important;
      transition-duration: 0.01ms !important;
    }
  }

  /* Scrollbar styling */
  ::-webkit-scrollbar {
    width: 8px;
    height: 8px;
  }

  ::-webkit-scrollbar-track {
    @apply bg-gray-100;
  }

  ::-webkit-scrollbar-thumb {
    @apply bg-gray-300 rounded-full;
  }

  ::-webkit-scrollbar-thumb:hover {
    @apply bg-gray-400;
  }
}

@layer utilities {
  /* Screen reader only */
  .sr-only {
    position: absolute;
    width: 1px;
    height: 1px;
    padding: 0;
    margin: -1px;
    overflow: hidden;
    clip: rect(0, 0, 0, 0);
    white-space: nowrap;
    border-width: 0;
  }
}
```

**Test:** Verify fonts load and focus rings appear on Tab navigation

---

### 1.3 TypeScript Types

**File:** `frontend/src/types/index.ts`

**Action:** Create comprehensive type definitions:

```typescript
// Node types
export type StockType = 'structural' | 'proxy' | 'crisis'
export type Category = 'built_environment' | 'social_environment' |
                       'economic' | 'political' | 'biological' | 'default'

export interface MechanismNode {
  id: string
  label: string
  category: Category
  stockType: StockType
  weight: number
  x?: number
  y?: number
  connections: {
    outgoing: number
    incoming: number
  }
}

export interface MechanismEdge {
  id: string
  source: string
  target: string
  direction: 'positive' | 'negative'
  strength: number
  evidenceQuality: 'A' | 'B' | 'C' | null
  studyCount: number
}

export interface Mechanism {
  id: string
  fromNode: string
  toNode: string
  direction: 'positive' | 'negative'
  description: string
  evidenceQuality: 'A' | 'B' | 'C' | null
  studyCount: number
  citations: Citation[]
  moderators: Moderator[]
}

export interface Citation {
  id: string
  authors: string
  year: number
  title: string
  journal: string
  url?: string
  pdfUrl?: string
}

export interface Moderator {
  category: 'policy' | 'demographic' | 'geographic' | 'implementation'
  description: string
  effect: 'strengthens' | 'weakens' | 'varies'
}

export interface Pathway {
  id: string
  interventionNodeId: string
  outcomeNodeId: string
  mechanisms: Mechanism[]
  aggregateQuality: 'A' | 'B' | 'C'
  overallDirection: 'positive' | 'negative'
}

export interface SystemsNetwork {
  nodes: MechanismNode[]
  edges: MechanismEdge[]
}
```

**Test:** Run `npm run type-check` (if configured) or verify no TypeScript errors

---

### 1.4 Storybook Setup

**Action:** Initialize Storybook for component development:

```bash
npx storybook@latest init
```

**Configure:** Edit `.storybook/preview.ts`:

```typescript
import '../src/index.css'

export const parameters = {
  actions: { argTypesRegex: '^on[A-Z].*' },
  controls: {
    matchers: {
      color: /(background|color)$/i,
      date: /Date$/,
    },
  },
}
```

**Test:** Run `npm run storybook` and verify it loads

---

**Phase 1 Deliverables:**
- ✅ Tailwind configured with design tokens
- ✅ Global styles with accessibility
- ✅ TypeScript types defined
- ✅ Storybook initialized
- ✅ Development environment running

---

## Phase 2: Base Components (Week 2)

### 2.1 Button Component

**File:** `frontend/src/components/base/Button.tsx`

```typescript
import React from 'react'
import { cn } from '@/utils/classNames'

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'text' | 'icon'
  size?: 'sm' | 'md' | 'lg'
  loading?: boolean
  icon?: React.ReactNode
  iconPosition?: 'left' | 'right'
  children?: React.ReactNode
  ariaLabel?: string
}

export const Button: React.FC<ButtonProps> = ({
  variant = 'primary',
  size = 'md',
  loading = false,
  icon,
  iconPosition = 'left',
  children,
  className,
  disabled,
  ariaLabel,
  ...props
}) => {
  const baseStyles = 'inline-flex items-center justify-center font-semibold rounded-md transition-all duration-200 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary-500 focus-visible:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed'

  const variantStyles = {
    primary: 'bg-primary-600 text-white hover:bg-primary-700 active:bg-primary-800',
    secondary: 'bg-white text-primary-600 border border-primary-600 hover:bg-primary-50',
    text: 'bg-transparent text-primary-600 hover:bg-primary-50',
    icon: 'bg-transparent hover:bg-gray-100 text-gray-700',
  }

  const sizeStyles = {
    sm: 'px-3 py-1.5 text-sm gap-1.5',
    md: 'px-4 py-2 text-sm gap-2',
    lg: 'px-6 py-3 text-base gap-2',
  }

  return (
    <button
      className={cn(baseStyles, variantStyles[variant], sizeStyles[size], className)}
      disabled={disabled || loading}
      aria-label={ariaLabel}
      {...props}
    >
      {loading && <LoadingSpinner size={size} />}
      {!loading && icon && iconPosition === 'left' && icon}
      {children}
      {!loading && icon && iconPosition === 'right' && icon}
    </button>
  )
}

const LoadingSpinner: React.FC<{ size: 'sm' | 'md' | 'lg' }> = ({ size }) => {
  const sizeClasses = {
    sm: 'w-4 h-4',
    md: 'w-5 h-5',
    lg: 'w-6 h-6',
  }

  return (
    <svg
      className={cn('animate-spin', sizeClasses[size])}
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
      viewBox="0 0 24 24"
    >
      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
    </svg>
  )
}
```

**Utility:** `frontend/src/utils/classNames.ts`

```typescript
import { clsx, type ClassValue } from 'clsx'
import { twMerge } from 'tailwind-merge'

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}
```

**Story:** `frontend/src/components/base/Button.stories.tsx`

```typescript
import type { Meta, StoryObj } from '@storybook/react'
import { Button } from './Button'

const meta: Meta<typeof Button> = {
  title: 'Base/Button',
  component: Button,
  tags: ['autodocs'],
}

export default meta
type Story = StoryObj<typeof Button>

export const Primary: Story = {
  args: {
    variant: 'primary',
    children: 'Primary Button',
  },
}

export const Secondary: Story = {
  args: {
    variant: 'secondary',
    children: 'Secondary Button',
  },
}

export const Loading: Story = {
  args: {
    variant: 'primary',
    loading: true,
    children: 'Loading...',
  },
}
```

**Test:** `frontend/src/components/base/Button.test.tsx`

```typescript
import { render, fireEvent } from '@testing-library/react'
import { Button } from './Button'

describe('Button', () => {
  it('renders correctly', () => {
    const { getByRole } = render(<Button>Click me</Button>)
    expect(getByRole('button')).toBeInTheDocument()
  })

  it('calls onClick when clicked', () => {
    const handleClick = jest.fn()
    const { getByRole } = render(<Button onClick={handleClick}>Click</Button>)
    fireEvent.click(getByRole('button'))
    expect(handleClick).toHaveBeenCalledTimes(1)
  })

  it('is disabled when loading', () => {
    const { getByRole } = render(<Button loading>Loading</Button>)
    expect(getByRole('button')).toBeDisabled()
  })
})
```

---

### 2.2 Other Base Components

**Complete in this order:**
1. ✅ Button (above)
2. Input - Similar pattern, add label and error states
3. Badge - Simpler, just styling variants
4. Icon - Wrapper for Heroicons or custom SVG
5. Tooltip - Use Radix UI or Floating UI library

**Reference:** See [Component Library doc](./05_COMPONENT_LIBRARY.md) for full specifications

---

**Phase 2 Deliverables:**
- ✅ Button component with all variants
- ✅ Input component
- ✅ Badge component
- ✅ Icon component
- ✅ Tooltip component
- ✅ Storybook stories for each
- ✅ Unit tests for each

---

## Phase 3: Layout Components (Week 3)

### 3.1 Dashboard Layout

**File:** `frontend/src/layouts/DashboardLayout.tsx`

```typescript
import React, { useState } from 'react'
import { Header } from './Header'
import { Sidebar } from './Sidebar'

interface DashboardLayoutProps {
  children: React.ReactNode
}

export const DashboardLayout: React.FC<DashboardLayoutProps> = ({ children }) => {
  const [sidebarOpen, setSidebarOpen] = useState(false)
  const [sidebarWidth, setSidebarWidth] = useState(320)

  return (
    <div className="flex flex-col h-screen bg-gray-50">
      <Header />

      <div className="flex flex-1 overflow-hidden">
        <main className="flex-1 overflow-auto">
          {children}
        </main>

        {sidebarOpen && (
          <Sidebar
            width={sidebarWidth}
            onWidthChange={setSidebarWidth}
            onClose={() => setSidebarOpen(false)}
          />
        )}
      </div>
    </div>
  )
}
```

### 3.2 Header Component

**File:** `frontend/src/layouts/Header.tsx`

```typescript
import React from 'react'
import { NavLink } from 'react-router-dom'
import { Button } from '@/components/base/Button'

export const Header: React.FC = () => {
  return (
    <header className="h-15 bg-white border-b border-gray-200 px-6 flex items-center justify-between">
      <div className="flex items-center gap-6">
        <div className="text-xl font-bold text-gray-900">HealthSystems</div>

        <nav className="flex gap-1">
          <NavLink
            to="/"
            className={({ isActive }) =>
              `px-4 py-2 text-sm font-medium transition-colors ${
                isActive
                  ? 'text-primary-600 border-b-2 border-primary-600'
                  : 'text-gray-600 hover:text-gray-900'
              }`
            }
          >
            Systems Map
          </NavLink>
          <NavLink
            to="/pathways"
            className={({ isActive }) =>
              `px-4 py-2 text-sm font-medium transition-colors ${
                isActive
                  ? 'text-primary-600 border-b-2 border-primary-600'
                  : 'text-gray-600 hover:text-gray-900'
              }`
            }
          >
            Pathway Explorer
          </NavLink>
          <NavLink
            to="/library"
            className={({ isActive }) =>
              `px-4 py-2 text-sm font-medium transition-colors ${
                isActive
                  ? 'text-primary-600 border-b-2 border-primary-600'
                  : 'text-gray-600 hover:text-gray-900'
              }`
            }
          >
            Library
          </NavLink>
        </nav>
      </div>

      <div className="flex items-center gap-3">
        {/* Geography selector, settings, user menu */}
      </div>
    </header>
  )
}
```

---

**Phase 3 Deliverables:**
- ✅ DashboardLayout component
- ✅ Header with tab navigation
- ✅ Sidebar/Panel container
- ✅ Routing setup (React Router)
- ✅ Responsive behavior (mobile/tablet)

---

## Phase 4: Graph Visualization (Weeks 4-5)

### 4.1 Force Simulation Hook

**File:** `frontend/src/hooks/useForceSimulation.ts`

```typescript
import { useEffect, useRef } from 'react'
import * as d3 from 'd3'
import { MechanismNode, MechanismEdge } from '@/types'

export const useForceSimulation = (
  nodes: MechanismNode[],
  edges: MechanismEdge[],
  width: number,
  height: number
) => {
  const simulationRef = useRef<d3.Simulation<MechanismNode, MechanismEdge>>()

  useEffect(() => {
    if (!nodes.length) return

    // Create simulation
    const simulation = d3.forceSimulation(nodes)
      .force('link', d3.forceLink(edges)
        .id((d: any) => d.id)
        .distance(100)
        .strength(0.3)
      )
      .force('charge', d3.forceManyBody().strength(-300))
      .force('center', d3.forceCenter(width / 2, height / 2))
      .force('collision', d3.forceCollide().radius((d: any) => d.radius + 5))

    simulationRef.current = simulation

    return () => {
      simulation.stop()
    }
  }, [nodes, edges, width, height])

  return simulationRef.current
}
```

### 4.2 MechanismGraph Component

**File:** `frontend/src/visualizations/MechanismGraph.tsx`

*(This file already exists - enhance it based on [Systems Map Visualization doc](./03_SYSTEMS_MAP_VISUALIZATION.md))*

**Key enhancements needed:**
1. Add all node states (hover, selected, dimmed, focus)
2. Add edge states with evidence badges
3. Implement zoom/pan controls
4. Add keyboard navigation
5. Optimize for 400+ nodes (viewport culling)

**Reference:** See existing `frontend/src/visualizations/MechanismGraph.tsx` and enhance incrementally

---

**Phase 4 Deliverables:**
- ✅ Force simulation working with D3
- ✅ Node rendering with category colors
- ✅ Edge rendering with arrows
- ✅ Evidence badges on edges
- ✅ Zoom/pan controls
- ✅ Basic interactivity (click, hover)
- ✅ Performance optimization (>30 FPS with 400 nodes)

---

## Phase 5: Detail Panels (Week 6)

### 5.1 Panel Container Component

**File:** `frontend/src/components/layout/Panel.tsx`

```typescript
import React, { useRef, useState } from 'react'
import { Button } from '@/components/base/Button'

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

export const Panel: React.FC<PanelProps> = ({
  title,
  icon,
  defaultWidth = 320,
  minWidth = 280,
  maxWidth = 480,
  resizable = true,
  collapsible = true,
  onClose,
  children,
}) => {
  const [width, setWidth] = useState(defaultWidth)
  const [isResizing, setIsResizing] = useState(false)
  const panelRef = useRef<HTMLDivElement>(null)

  const handleMouseDown = () => {
    setIsResizing(true)
  }

  useEffect(() => {
    const handleMouseMove = (e: MouseEvent) => {
      if (!isResizing) return
      const newWidth = window.innerWidth - e.clientX
      setWidth(Math.max(minWidth, Math.min(maxWidth, newWidth)))
    }

    const handleMouseUp = () => {
      setIsResizing(false)
    }

    if (isResizing) {
      document.addEventListener('mousemove', handleMouseMove)
      document.addEventListener('mouseup', handleMouseUp)
    }

    return () => {
      document.removeEventListener('mousemove', handleMouseMove)
      document.removeEventListener('mouseup', handleMouseUp)
    }
  }, [isResizing, minWidth, maxWidth])

  return (
    <aside
      ref={panelRef}
      className="bg-white border-l border-gray-200 flex flex-col overflow-hidden"
      style={{ width: `${width}px` }}
      role="complementary"
      aria-label={title}
    >
      {/* Resize handle */}
      {resizable && (
        <div
          className="absolute left-0 top-0 bottom-0 w-1 cursor-col-resize hover:bg-primary-300 transition-colors"
          onMouseDown={handleMouseDown}
        />
      )}

      {/* Header */}
      <div className="h-12 flex items-center justify-between px-6 border-b border-gray-200">
        <div className="flex items-center gap-2">
          {icon}
          <h2 className="text-lg font-semibold text-gray-900">{title}</h2>
        </div>
        <div className="flex items-center gap-1">
          {collapsible && (
            <Button variant="icon" size="sm" ariaLabel="Minimize panel">
              {/* Minimize icon */}
            </Button>
          )}
          <Button variant="icon" size="sm" onClick={onClose} ariaLabel="Close panel">
            {/* Close icon */}
          </Button>
        </div>
      </div>

      {/* Content */}
      <div className="flex-1 overflow-y-auto p-6">
        {children}
      </div>
    </aside>
  )
}
```

### 5.2 Node Detail Panel

**Reference:** [Detail Panels doc](./04_DETAIL_PANELS.md) Section 2

**Implementation:** Create `NodeDetailPanel.tsx` with sections for:
- Overview
- Connections (outgoing/incoming)
- Spatial variation
- Related nodes

---

**Phase 5 Deliverables:**
- ✅ Panel container (resizable, collapsible)
- ✅ Node detail panel
- ✅ Mechanism detail panel
- ✅ Filter panel
- ✅ Search results panel

---

## Phases 6-7: Advanced Features & Polish (Weeks 7-10)

**Reference full docs for:**
- Pathway Explorer implementation
- Node Library table/grid views
- Evidence Base tab
- Mobile responsive layouts
- Accessibility audit
- Performance optimization
- Testing (unit, integration, E2E)

---

## Testing Strategy

### Unit Tests (Jest + React Testing Library)
```bash
npm test
```

**What to test:**
- Component rendering
- User interactions (click, type, etc.)
- State changes
- Props variations

### Accessibility Tests (jest-axe)
```bash
npm run test:a11y
```

**What to test:**
- No axe violations
- Keyboard navigation
- ARIA attributes
- Color contrast

### E2E Tests (Playwright)
```bash
npm run test:e2e
```

**What to test:**
- Complete user flows
- Cross-browser compatibility
- Mobile responsiveness

---

## Deployment Checklist

- [ ] All tests passing
- [ ] Accessibility audit complete (WCAG AA)
- [ ] Performance metrics met (Lighthouse score >90)
- [ ] Browser testing (Chrome, Firefox, Safari, Edge)
- [ ] Mobile testing (iOS, Android)
- [ ] Error handling implemented
- [ ] Loading states implemented
- [ ] Empty states implemented
- [ ] Analytics integrated (if required)
- [ ] Documentation updated

---

## Getting Help

**Stuck on:**
- **Design questions:** Review relevant design doc or ask UX team
- **Technical issues:** Check existing codebase, ask senior dev
- **Accessibility:** Review WCAG guidelines, use axe DevTools
- **Performance:** Profile with Chrome DevTools, optimize renders

**Resources:**
- [Design Documentation](./README.md)
- [Quick Reference](./QUICK_REFERENCE.md)
- [React Docs](https://react.dev/)
- [D3.js Gallery](https://observablehq.com/@d3/gallery)
- [Tailwind CSS Docs](https://tailwindcss.com/)

---

**Start implementing today!** Begin with Phase 1 and work sequentially. Each phase builds on the previous one.

Good luck! 🚀
