# PROMPT 4: Remove Unused Dependencies

## Context
The frontend `package.json` contains **multiple unused dependencies** that add to bundle size, installation time, and maintenance overhead. These were likely added for features that were never completed or have been replaced.

## Current State

### Unused Dependencies Identified

**From `frontend/package.json`:**

```json
{
  "dependencies": {
    "axios": "^1.6.0",           // UNUSED - fetch API used instead
    "classnames": "^2.3.2",      // UNUSED - manual className logic used
    "clsx": "^2.0.0",            // UNUSED - duplicate of classnames
    "date-fns": "^2.30.0",       // UNUSED - no date formatting found
    "lodash": "^4.17.21",        // UNUSED - native JS methods used
    "react-hot-toast": "^2.4.1", // UNUSED - no toast notifications yet
    "recharts": "^2.10.0"        // UNUSED - D3.js used for all charts
  },
  "devDependencies": {
    "@types/lodash": "^4.14.200" // UNUSED - lodash not used
  }
}
```

### Evidence of Non-Usage

**Axios** - searched entire frontend, only found in package.json:
```bash
$ grep -r "import.*axios" frontend/src
# No results

$ grep -r "from 'axios'" frontend/src
# No results
```

All API calls use native `fetch` API.

**Classnames/Clsx** - no imports found:
```bash
$ grep -r "import.*classnames" frontend/src
# No results

$ grep -r "import.*clsx" frontend/src
# No results
```

All className logic uses template literals or manual concatenation.

**date-fns** - no date formatting found:
```bash
$ grep -r "import.*date-fns" frontend/src
# No results
```

No date display or formatting in current UI.

**lodash** - no utility imports found:
```bash
$ grep -r "import.*lodash" frontend/src
# No results

$ grep -r "import.*_" frontend/src | grep lodash
# No results
```

Native array methods (`.map`, `.filter`, `.reduce`) used throughout.

**react-hot-toast** - no toast usage:
```bash
$ grep -r "import.*toast" frontend/src
# No results

$ grep -r "react-hot-toast" frontend/src
# No results
```

No toast notification system implemented yet.

**recharts** - D3.js used exclusively:
```bash
$ grep -r "import.*recharts" frontend/src
# No results

$ grep -r "from 'recharts'" frontend/src
# No results
```

All visualizations use D3.js directly (see `MechanismGraph.tsx`).

## Target State

### Clean package.json

**Remove these dependencies:**
```json
{
  "dependencies": {
    // REMOVE: axios
    // REMOVE: classnames
    // REMOVE: clsx
    // REMOVE: date-fns
    // REMOVE: lodash
    // REMOVE: react-hot-toast
    // REMOVE: recharts
  },
  "devDependencies": {
    // REMOVE: @types/lodash
  }
}
```

### Bundle Size Impact

**Current total dependency size:** ~45 MB
**Estimated savings:** ~12 MB (26% reduction)

Breakdown:
- axios: ~1.2 MB
- lodash: ~4.5 MB
- recharts: ~3.8 MB
- date-fns: ~2.1 MB
- Others: ~0.5 MB

## Implementation Steps

### Step 1: Verify Non-Usage

Run comprehensive search to confirm no usage:

```bash
cd frontend

# Search for axios
grep -r "axios" src/
grep -r "axios" *.ts *.tsx *.js

# Search for classnames/clsx
grep -r "classnames\|clsx" src/
grep -r "cn(" src/  # Common alias

# Search for date-fns
grep -r "date-fns" src/
grep -r "format.*Date\|parse.*Date" src/

# Search for lodash
grep -r "lodash\|import.*_" src/
grep -r "_.map\|_.filter\|_.reduce" src/

# Search for react-hot-toast
grep -r "toast\|react-hot-toast" src/

# Search for recharts
grep -r "recharts\|LineChart\|BarChart\|PieChart" src/
```

**Expected result:** No matches (or only comments/false positives)

### Step 2: Remove Dependencies

**Option A: Manual removal (careful approach)**

Edit `frontend/package.json`:

```bash
# Backup first
cp package.json package.json.backup

# Edit package.json - remove these lines:
# - "axios": "^1.6.0",
# - "classnames": "^2.3.2",
# - "clsx": "^2.0.0",
# - "date-fns": "^2.30.0",
# - "lodash": "^4.17.21",
# - "react-hot-toast": "^2.4.1",
# - "recharts": "^2.10.0",
# - "@types/lodash": "^4.14.200"
```

**Option B: Using npm uninstall**

```bash
cd frontend

npm uninstall axios classnames clsx date-fns lodash react-hot-toast recharts
npm uninstall --save-dev @types/lodash
```

### Step 3: Clean Install

```bash
cd frontend

# Remove existing installations
rm -rf node_modules
rm package-lock.json

# Fresh install
npm install

# Verify bundle size reduction
npm run build

# Check dist/ size
du -sh dist/
```

### Step 4: Verify Application Works

```bash
# Run dev server
npm run dev

# Run tests
npm test

# Run build
npm run build

# Test all features:
# - Systems Map View
# - Pathfinder
# - Crisis Explorer
# - Important Nodes
# - Alcoholism System View
```

### Step 5: Update Documentation

**File: `frontend/README.md`**

Add note about dependency decisions:

```markdown
## Dependencies

We intentionally use minimal dependencies:

- **No HTTP client library** - Native `fetch` API is sufficient
- **No className utility** - Template literals handle our needs
- **No date library** - Will add when needed
- **No lodash** - Native array methods are preferred
- **No charting library** - D3.js provides full control
```

## Migration Checklist

### Phase 1: Verification (1 hour)
- [ ] Run all grep searches above
- [ ] Confirm no usage in codebase
- [ ] Check for indirect dependencies (other packages depending on these)
- [ ] Review git history for removed code that might have used these

### Phase 2: Removal (30 minutes)
- [ ] Backup `package.json` and `package-lock.json`
- [ ] Remove dependencies via npm uninstall
- [ ] Verify package.json is clean
- [ ] Fresh `npm install`

### Phase 3: Testing (1 hour)
- [ ] Run all unit tests: `npm test`
- [ ] Run all e2e tests: `npm run test:e2e`
- [ ] Manual testing of all views
- [ ] Build and check for errors: `npm run build`
- [ ] Verify bundle size reduced

### Phase 4: Documentation (30 minutes)
- [ ] Update README with dependency philosophy
- [ ] Document bundle size improvement
- [ ] Commit with message: "chore: remove 8 unused dependencies (12MB savings)"

## Potential Issues & Solutions

### Issue 1: Transitive Dependencies

**Problem:** Another package might depend on these.

**Solution:** Check with:
```bash
npm ls axios
npm ls lodash
npm ls recharts
# etc.
```

If any show up, investigate if removal is safe.

### Issue 2: Type Errors After Removal

**Problem:** TypeScript errors referencing removed types.

**Solution:**
```bash
# Rebuild types
npm run build

# Check for orphaned type imports
grep -r "@types/lodash" src/
```

### Issue 3: Bundle Size Not Reduced

**Problem:** Bundle size stays same after removal.

**Solution:**
```bash
# Clear build cache
rm -rf dist/ .vite/

# Rebuild
npm run build
```

## Success Criteria

- ✅ All 8 unused dependencies removed
- ✅ `npm install` completes successfully
- ✅ `npm test` passes all tests
- ✅ `npm run build` succeeds
- ✅ Bundle size reduced by ~12MB
- ✅ All features work in manual testing
- ✅ No TypeScript errors
- ✅ Documentation updated

## Estimated Effort
**3 hours** (verification, removal, testing)

## Future Recommendations

### When to Add Dependencies

**DO add a dependency if:**
- ✅ It solves a complex problem (auth, state management)
- ✅ It's actively maintained
- ✅ It has good TypeScript support
- ✅ It's widely used (community trust)
- ✅ Native browser APIs are insufficient

**DON'T add a dependency for:**
- ❌ Simple utilities (write your own)
- ❌ "Convenience" (string manipulation, date formatting)
- ❌ Abandoned packages
- ❌ Large packages for small features

### Dependency Review Process

Add to `.github/workflows/dependency-review.yml`:

```yaml
name: Dependency Review
on: [pull_request]

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Check for new dependencies
        run: |
          git diff origin/main -- package.json | grep "^+"
          # Require manual review for any new dependencies
```

### Bundle Size Monitoring

Add to package.json:

```json
{
  "scripts": {
    "analyze": "vite-bundle-visualizer"
  }
}
```

Monitor bundle size in CI:

```bash
npm run build
du -sh dist/
# Fail if > 2MB threshold
```
