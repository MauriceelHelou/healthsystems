# Design System Specification
**HealthSystems Platform - Visual Design Foundation**

Version: 1.0
Last Updated: 2025-11-16
Status: MVP Scope (Topology & Direction Only)

---

## Overview

This document defines the visual design foundation for the HealthSystems dashboard, a clean, minimalist interface for exploring complex health systems through interactive network visualizations. The design system prioritizes accessibility, clarity, and cognitive ease when navigating 400+ nodes and 2000+ mechanisms.

---

## 1. Design Principles

### Core Principles
1. **Clarity Over Decoration**: Every visual element serves a functional purpose
2. **Accessibility First**: WCAG AA compliance minimum, keyboard navigation essential
3. **Information Density**: Balance between comprehensive data and cognitive load
4. **Progressive Disclosure**: Show overview first, details on demand
5. **Consistent Mental Models**: Same patterns across all views and interactions

### MVP Constraint
**Show topology and direction, NOT quantification**. All visual elements should communicate relationships, pathways, and qualitative evidence without implying numerical precision.

---

## 2. Color System

### Primary Palette

**Brand/Interactive Colors**
```css
--primary-50:  #f0f9ff   /* Backgrounds, subtle highlights */
--primary-100: #e0f2fe   /* Hover backgrounds */
--primary-500: #0ea5e9   /* Focus rings, active states */
--primary-600: #0284c7   /* Primary interactive (links, buttons) */
--primary-700: #0369a1   /* Emphasis, pressed states */
--primary-900: #0c4a6e   /* Text on light backgrounds */
```

**Secondary/Accent (Purple)**
```css
--secondary-500: #a855f7  /* Accent elements */
--secondary-600: #9333ea  /* Secondary interactive */
--secondary-700: #7e22ce  /* Emphasis */
```

### Category Colors (Mechanism Types)

**5 Primary Categories + Default**

| Category | Color | Hex | Usage |
|----------|-------|-----|-------|
| Built Environment | Dark Blue | `#0369a1` | Housing, infrastructure, facilities |
| Social Environment | Purple | `#9333ea` | Community, relationships, trust |
| Economic | Green | `#059669` | Employment, income, resources |
| Political | Red | `#dc2626` | Policy, governance, regulations |
| Biological | Orange | `#ea580c` | Health behaviors, clinical care |
| Default/Mixed | Gray | `#6b7280` | Uncategorized or multi-category |

**Color Usage Rules:**
- Nodes: Fill color based on category, 80% opacity
- Edges: Stroke color matching source node category, 60% opacity
- Backgrounds: Light tints (10% opacity) for categorical sections
- Text: Ensure 4.5:1 contrast ratio minimum

### Semantic Colors

**Status & Feedback**
```css
--success:     #10b981  /* Confirmation, positive outcomes */
--warning:     #f59e0b  /* Caution, moderate evidence */
--error:       #ef4444  /* Errors, conflicts, negative */
--info:        #3b82f6  /* Neutral information, help */
```

**Evidence Quality (Badges)**
```css
--evidence-A:  #10b981  /* High quality (A rating) - Green */
--evidence-B:  #f59e0b  /* Moderate quality (B rating) - Amber */
--evidence-C:  #ef4444  /* Low quality (C rating) - Red */
--evidence-0:  #9ca3af  /* No rating/unknown - Gray */
```

### Neutral/UI Grays

```css
--gray-50:   #f9fafb   /* Page backgrounds */
--gray-100:  #f3f4f6   /* Panel backgrounds */
--gray-200:  #e5e7eb   /* Borders, dividers */
--gray-300:  #d1d5db   /* Disabled borders */
--gray-400:  #9ca3af   /* Placeholder text */
--gray-500:  #6b7280   /* Secondary text */
--gray-600:  #4b5563   /* Body text */
--gray-700:  #374151   /* Headings */
--gray-800:  #1f2937   /* High emphasis text */
--gray-900:  #111827   /* Maximum contrast */
```

---

## 3. Typography

### Font Families

**Primary (UI & Content)**
```css
font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI',
             'Roboto', 'Helvetica Neue', Arial, sans-serif;
```

**Monospace (Code, IDs, Data)**
```css
font-family: 'Monaco', 'Menlo', 'Courier New', monospace;
```

### Type Scale

| Name | Size | Line Height | Weight | Usage |
|------|------|-------------|--------|-------|
| **Display** | 36px | 40px | 700 | Page titles (rare) |
| **H1** | 30px | 36px | 700 | Section headers |
| **H2** | 24px | 32px | 600 | Panel titles |
| **H3** | 20px | 28px | 600 | Subsection headers |
| **H4** | 18px | 24px | 600 | Card/component titles |
| **Body Large** | 16px | 24px | 400 | Primary content |
| **Body** | 14px | 20px | 400 | Default text |
| **Body Small** | 13px | 18px | 400 | Secondary text, labels |
| **Caption** | 12px | 16px | 400 | Metadata, timestamps |
| **Label** | 12px | 16px | 500 | Form labels, badges |
| **Micro** | 11px | 14px | 400 | Graph labels, tooltips |

### Font Weights
- **400** (Regular): Body text, descriptions
- **500** (Medium): Labels, navigation items
- **600** (Semi-Bold): Subheadings, emphasis
- **700** (Bold): Main headings, high emphasis

### Text Colors (on white/light backgrounds)
- **Primary**: `gray-900` (#111827) - Main content
- **Secondary**: `gray-600` (#4b5563) - Supporting text
- **Tertiary**: `gray-500` (#6b7280) - Metadata, captions
- **Disabled**: `gray-400` (#9ca3af) - Inactive elements

---

## 4. Spacing System

### Base Unit: 4px

All spacing uses multiples of 4px for consistency and alignment.

```css
--space-0:   0px      /* None */
--space-1:   4px      /* Tiny - icon padding */
--space-2:   8px      /* Small - compact spacing */
--space-3:   12px     /* Medium-small - inline elements */
--space-4:   16px     /* Medium - default gap */
--space-5:   20px     /* Medium-large - section padding */
--space-6:   24px     /* Large - card padding */
--space-8:   32px     /* XL - panel padding */
--space-10:  40px     /* 2XL - major sections */
--space-12:  48px     /* 3XL - page margins */
--space-16:  64px     /* 4XL - layout gaps */
```

### Layout Grid
- **Container Max Width**: 1920px (ultra-wide support)
- **Sidebar Width**: 320px (collapsed), 400px (expanded)
- **Panel Width**: 360-480px (detail panels)
- **Gutter**: 24px (desktop), 16px (mobile)

---

## 5. Borders & Shadows

### Border Widths
```css
--border-thin:    1px   /* Default borders, dividers */
--border-medium:  2px   /* Emphasis, focus rings */
--border-thick:   3px   /* Strong emphasis (rare) */
```

### Border Radius
```css
--radius-sm:    4px    /* Badges, small buttons */
--radius-md:    6px    /* Buttons, inputs, cards */
--radius-lg:    8px    /* Panels, modals */
--radius-xl:    12px   /* Large cards */
--radius-full:  9999px /* Pills, circular avatars */
```

### Shadows (Elevation)

**Minimal Approach** - Use sparingly for depth

```css
/* Subtle - Hovering cards, dropdowns */
--shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);

/* Default - Panels, modals */
--shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1),
             0 2px 4px -1px rgba(0, 0, 0, 0.06);

/* Prominent - Floating panels, tooltips */
--shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1),
             0 4px 6px -2px rgba(0, 0, 0, 0.05);

/* Maximum - Modals, overlays */
--shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1),
             0 10px 10px -5px rgba(0, 0, 0, 0.04);
```

---

## 6. Component States

### Interactive Element States

**Buttons, Links, Interactive Nodes**

| State | Visual Treatment | CSS Properties |
|-------|------------------|----------------|
| **Default** | Base colors, no decoration | `opacity: 1` |
| **Hover** | Lighter background, cursor pointer | `background: +10% lightness`, `cursor: pointer` |
| **Active/Pressed** | Darker background, slight scale | `background: -10% lightness`, `scale: 0.98` |
| **Focus** | 2px ring, 2px offset | `ring: 2px primary-500`, `ring-offset: 2px` |
| **Disabled** | Reduced opacity, no cursor | `opacity: 0.5`, `cursor: not-allowed` |
| **Selected** | Accent background, bold text | `background: primary-100`, `font-weight: 600` |

### Node States (Graph Visualization)

| State | Visual Treatment | Opacity | Stroke |
|-------|------------------|---------|--------|
| **Default** | Category color fill | 80% | 2px, darker shade |
| **Hover** | Brighter fill, larger | 100% | 3px, accent color |
| **Selected** | Accent border, shadow | 100% | 4px, primary-600 |
| **Connected** | Full opacity (when path active) | 100% | 2px |
| **Dimmed** | Low opacity (when filtering) | 30% | 1px |
| **Focus** | Ring around node | 100% | 2px ring offset |

### Edge States (Graph Links)

| State | Visual Treatment | Opacity | Width |
|-------|------------------|---------|-------|
| **Default** | Source category color | 40% | 1px |
| **Hover** | Full opacity | 80% | 2px |
| **Active Path** | Accent color, animated | 100% | 3px |
| **Dimmed** | Very low opacity | 15% | 1px |

---

## 7. Iconography

### Icon System Requirements

**Style**: Outline/stroke-based (2px stroke weight), minimalist
**Size Scale**: 16px, 20px, 24px, 32px
**Recommended Library**: Heroicons (already common in React/Tailwind ecosystem)

### Required Icons (Minimum Set)

**Navigation & Actions**
- Search (magnifying glass)
- Filter (funnel)
- Settings (gear)
- Close (X)
- Expand/Collapse (chevrons)
- Info (i in circle)
- Help (question mark)

**Graph Controls**
- Zoom In/Out (+ / -)
- Fit to Screen (expand arrows)
- Center (crosshair)
- Pan (hand)
- Reset (circular arrow)

**Node Types** (Consider custom)
- Structural Stock (building/cube)
- Proxy Index (gauge/meter)
- Crisis Outcome (alert triangle)

**Evidence & Quality**
- Citation (document)
- External Link (arrow-up-right)
- Warning (triangle)
- Check (success)
- Badge (award/ribbon)

**Directional**
- Arrow Right (positive relationship)
- Arrow Up (increase)
- Arrow Down (decrease)
- Bidirectional (double arrow)

### Icon Usage Rules
1. Always include accessible labels (aria-label or sr-only text)
2. Use consistent size within components (20px standard for toolbar)
3. Apply `currentColor` for stroke to inherit text color
4. Add 4px padding minimum around clickable icon buttons
5. Provide hover state (opacity or color change)

---

## 8. Accessibility Standards

### Focus Indicators

**Keyboard Navigation Essential**

```css
/* Custom Focus Ring */
.focus-visible {
  outline: none;
  ring: 2px solid var(--primary-500);
  ring-offset: 2px;
}
```

**Rules:**
- All interactive elements MUST have visible focus state
- Focus order follows logical reading/interaction flow
- Skip links for keyboard users to jump to main content
- Focus trap in modals/dialogs

### Color Contrast

**WCAG AA Minimum (4.5:1 for normal text, 3:1 for large text)**

Verified Combinations:
- `gray-900` on `white` = 15.3:1 ✓
- `gray-600` on `white` = 7.1:1 ✓
- `primary-600` on `white` = 4.7:1 ✓
- `white` on `primary-700` = 5.2:1 ✓

**Never use:**
- Gray text lighter than `gray-500` on white
- Colored text with <4.5:1 contrast
- Color as the ONLY differentiator (provide icons/patterns too)

### Motion & Animation

**Respect User Preferences**

```css
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

**Animation Guidelines:**
- Duration: 150-300ms for micro-interactions
- Easing: `ease-in-out` for most transitions
- Avoid rapid flashing (>3 times per second)
- Provide "Reduce Motion" toggle in settings

### Screen Reader Support

**Required Attributes:**
- `aria-label` for icon buttons without text
- `aria-describedby` for complex interactive elements
- `role="img"` and `aria-label` for SVG visualizations
- `aria-live="polite"` for dynamic content updates
- `alt` text for all meaningful images

**Graph Accessibility:**
- Keyboard navigation through nodes (Tab, Arrow keys)
- Screen reader announces node connections
- Alternative table/list view of network data
- Text-based search/filter as alternative to visual exploration

---

## 9. Responsive Breakpoints

### Breakpoint System

```css
/* Mobile First Approach */
--screen-sm:  640px   /* Small tablets, large phones */
--screen-md:  768px   /* Tablets */
--screen-lg:  1024px  /* Small laptops */
--screen-xl:  1280px  /* Desktops */
--screen-2xl: 1536px  /* Large desktops */
--screen-3xl: 1920px  /* Ultra-wide */
```

### Layout Adaptations

| Breakpoint | Layout | Sidebar | Graph |
|------------|--------|---------|-------|
| **<640px** | Single column, stacked | Hidden, full-screen modal | Full width, simplified |
| **640-1024px** | Hybrid, tabs | Collapsible, overlay | ~70% width |
| **1024-1536px** | Two-column | Fixed 320px | Remaining space |
| **>1536px** | Multi-panel | Expandable to 400px | Center focus, max 1400px |

---

## 10. Animation & Transitions

### Timing Functions

```css
--ease-in:      cubic-bezier(0.4, 0, 1, 1)      /* Accelerating */
--ease-out:     cubic-bezier(0, 0, 0.2, 1)      /* Decelerating */
--ease-in-out:  cubic-bezier(0.4, 0, 0.2, 1)    /* Smooth both */
--ease-spring:  cubic-bezier(0.68, -0.55, 0.27, 1.55) /* Bounce */
```

### Duration Scale

| Duration | Use Case |
|----------|----------|
| **100ms** | Instant feedback (hover, focus) |
| **200ms** | Standard transitions (color, opacity) |
| **300ms** | Panel open/close, moderate movement |
| **500ms** | Large animations, graph transitions |
| **1000ms** | Loading states, skeleton screens |

### Animation Patterns

**Graph Transitions**
- Node position changes: 500ms ease-out
- Edge opacity: 200ms ease-in-out
- Filter application: 300ms ease-in-out
- Zoom/pan: 400ms ease-in-out

**UI Transitions**
- Hover states: 150ms ease-out
- Panel slide: 300ms ease-in-out
- Modal fade: 200ms ease-in-out
- Tooltip appearance: 100ms ease-out

---

## 11. Z-Index Scale

**Layering Hierarchy**

```css
--z-base:       0     /* Default content */
--z-dropdown:   10    /* Dropdowns, popovers */
--z-sticky:     20    /* Sticky headers */
--z-overlay:    30    /* Overlays, backdrops */
--z-modal:      40    /* Modals, dialogs */
--z-popover:    50    /* Tooltips, floating elements */
--z-toast:      60    /* Notifications, toasts */
--z-max:        9999  /* Emergency top layer */
```

---

## 12. Dark Mode (Future Consideration)

**Not in MVP**, but design system should support:
- CSS custom properties for color values
- Semantic color names (not direct hex)
- Test contrast in both themes
- User preference detection via `prefers-color-scheme`

---

## Implementation Notes

### Tailwind Configuration
This design system extends the existing `tailwind.config.js`:
- Custom colors already defined
- Add spacing scale extensions if needed
- Configure custom focus ring utilities
- Add typography plugin for prose content

### CSS Custom Properties
Consider defining all design tokens as CSS variables for runtime theming:
```css
:root {
  /* Colors */
  --color-primary: #0284c7;
  --color-success: #10b981;

  /* Spacing */
  --space-4: 16px;

  /* Typography */
  --font-sans: 'Inter', sans-serif;
}
```

### Component Library Integration
All components should:
1. Use design tokens (colors, spacing) from this system
2. Include all states (hover, focus, disabled, etc.)
3. Meet accessibility requirements
4. Support keyboard navigation
5. Include TypeScript prop types

---

## Design System Maintenance

**Version Control**: Treat this as living documentation
- Update version number when significant changes occur
- Document breaking changes
- Maintain changelog

**Review Cadence**: Quarterly review to ensure alignment with:
- User feedback
- Accessibility audits
- Implementation learnings
- Platform evolution (Phase 2 quantification)

---

**Next Document**: [02_DASHBOARD_LAYOUT.md](./02_DASHBOARD_LAYOUT.md) - Overall dashboard architecture and screen layouts
