# Installation Checklist
**Quick setup guide for running the HealthSystems prototype**

---

## ✅ Prerequisites

- [ ] Node.js 18+ installed
- [ ] npm or yarn installed
- [ ] Code editor (VS Code recommended)
- [ ] Modern browser (Chrome, Firefox, Safari, Edge)

---

## 📦 Required npm Packages

### Already in package.json
- [x] react (18.2.0)
- [x] react-dom (18.2.0)
- [x] react-router-dom (6.20.1)
- [x] @tanstack/react-query (5.12.2)
- [x] zustand (4.4.7)
- [x] d3 (7.8.5)
- [x] tailwindcss (3.3.6)
- [x] typescript (4.9+)

### Need to Install
```bash
npm install clsx tailwind-merge
```

### Type Definitions (if missing)
```bash
npm install -D @types/d3
```

---

## 🚀 Step-by-Step Setup

### 1. Navigate to Frontend Directory
```bash
cd c:\Users\mauri\OneDrive - Harvard University\New folder (2)\healthsystems\frontend
```

### 2. Install Dependencies
```bash
npm install
```

### 3. Install Additional Packages
```bash
npm install clsx tailwind-merge
npm install -D @types/d3
```

### 4. Verify Tailwind Config

Check that `tailwind.config.js` includes:
```javascript
module.exports = {
  content: ['./src/**/*.{js,jsx,ts,tsx}'],
  theme: {
    extend: {
      colors: {
        category: {
          built: '#0369a1',
          social: '#9333ea',
          economic: '#059669',
          political: '#dc2626',
          biological: '#ea580c',
          default: '#6b7280',
        },
        evidence: {
          A: '#10b981',
          B: '#f59e0b',
          C: '#ef4444',
        },
      },
    },
  },
}
```

### 5. Verify index.css

Check that `src/index.css` includes:
```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

### 6. Start Development Server
```bash
npm run dev
```

### 7. Open Browser
Navigate to: `http://localhost:3000`

---

## 🔍 Troubleshooting

### Issue: Module not found errors

**Error**: `Module not found: Can't resolve 'clsx'`

**Fix**:
```bash
npm install clsx tailwind-merge
```

---

**Error**: `Module not found: Can't resolve '../utils/classNames'`

**Fix**: Ensure `src/utils/classNames.ts` exists with content:
```typescript
import { clsx, type ClassValue } from 'clsx'
import { twMerge } from 'tailwind-merge'

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}
```

---

**Error**: `Module not found: Can't resolve '../utils/colors'`

**Fix**: Ensure `src/utils/colors.ts` exists (already created in prototype)

---

**Error**: `Module not found: Can't resolve '../types'`

**Fix**: Ensure `src/types/index.ts` or `src/types/mechanism.ts` exports all types

---

### Issue: TypeScript errors

**Error**: `Property 'getCategoryColor' does not exist`

**Fix**: Check import in files using this function:
```typescript
import { getCategoryColor } from '../utils/colors'
```

---

**Error**: Type errors in MechanismGraph.tsx

**Fix**: Ensure types are properly imported:
```typescript
import type { MechanismNode, MechanismEdge, SystemsNetwork } from '../types/mechanism'
```

---

### Issue: Tailwind classes not working

**Symptoms**: Buttons/components have no styling

**Fix**:
1. Check `tailwind.config.js` content paths
2. Restart dev server (`Ctrl+C`, then `npm run dev`)
3. Clear browser cache
4. Check `index.css` imports Tailwind

---

### Issue: Graph not rendering

**Symptoms**: Blank canvas where graph should be

**Checks**:
1. Open browser DevTools (F12)
2. Check Console for errors
3. Verify mock data is loading:
   ```typescript
   console.log('Nodes:', mockNodes.length) // Should be 400
   console.log('Edges:', mockEdges.length) // Should be 2000+
   ```
4. Check Network tab for failed imports

---

### Issue: D3 errors

**Error**: `Cannot read property 'forceSimulation' of undefined`

**Fix**:
```bash
npm install d3
npm install -D @types/d3
```

Verify import:
```typescript
import * as d3 from 'd3'
```

---

### Issue: React Router errors

**Error**: `Uncaught Error: useRoutes() may be used only in the context of a <Router> component`

**Fix**: Ensure `App.tsx` wraps routes in `<Router>`:
```typescript
<Router>
  <DashboardLayout>
    <Routes>
      <Route path="/" element={<SystemsMapView />} />
    </Routes>
  </DashboardLayout>
</Router>
```

---

### Issue: Panel not resizable

**Symptoms**: Can't drag panel edge to resize

**Check**:
1. Ensure Panel component imported correctly
2. Verify `resizable={true}` prop is passed
3. Check CSS allows pointer events on resize handle

---

## ✨ Verification Checklist

After setup, verify these work:

- [ ] App loads at `http://localhost:3000`
- [ ] Header shows "HealthSystems" with 3 tabs
- [ ] Systems Map tab is active (underline)
- [ ] Graph renders with many colored circles (nodes)
- [ ] Lines connect nodes (edges)
- [ ] Legend appears in bottom-left corner
- [ ] Controls appear in top-right corner
- [ ] Click a node opens detail panel on right
- [ ] Panel shows node name, category, connections
- [ ] Panel can be closed with X button
- [ ] Panel can be resized by dragging left edge
- [ ] Clicking other tabs shows "Coming soon" placeholder
- [ ] No errors in browser console

---

## 🎯 Expected Results

### On Load
- Clean dashboard with header
- Large interactive graph in center
- Legend in bottom-left
- Controls in top-right
- All nodes visible and colored

### On Interaction
- Click node → Panel slides in from right
- Click edge → Panel shows mechanism details
- Drag node → Node moves and edges follow
- Hover controls → Buttons highlight
- Click tabs → Navigation works

### Performance
- Graph loads in < 2 seconds
- Interactions feel smooth (no lag)
- Panel animations are fluid
- No errors in console

---

## 📚 Quick Reference

### Key Files to Check
```
frontend/src/
├── App.tsx                  # Main routing
├── index.css                # Tailwind imports
├── tailwind.config.js       # Tailwind config
├── components/base/         # All should exist
├── layouts/                 # All should exist
├── views/SystemsMapView.tsx # Main view
├── data/mockData.ts         # 400 nodes, 2000+ edges
└── utils/                   # colors.ts, classNames.ts
```

### Common Commands
```bash
npm run dev          # Start dev server
npm run build        # Build for production
npm run lint         # Check code quality
npm install <pkg>    # Install package
```

### Ports
- Dev server: `http://localhost:3000`
- Vite HMR: `http://localhost:3000/__vite_hmr`

---

## 🆘 Still Having Issues?

1. **Check Node version**: `node -v` (should be 18+)
2. **Clear node_modules**:
   ```bash
   rm -rf node_modules package-lock.json
   npm install
   ```
3. **Check for port conflicts**: Another app on port 3000?
4. **Review console errors**: F12 → Console tab
5. **Check file paths**: Imports use correct relative paths?

---

## ✅ Installation Complete!

Once you see:
```
  VITE v5.x.x  ready in xxx ms

  ➜  Local:   http://localhost:3000/
  ➜  Network: use --host to expose
  ➜  press h to show help
```

And the browser shows the dashboard with an interactive graph, you're all set! 🎉

---

**Next**: Explore the prototype, click around, and start building additional features!

Refer to `PROTOTYPE_README.md` for detailed usage instructions.
