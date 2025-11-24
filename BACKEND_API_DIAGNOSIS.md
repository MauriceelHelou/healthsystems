# Backend API Diagnosis

**Date**: November 22, 2025
**Status**: Backend API Fully Implemented ✅ | Frontend Integration Issues ⚠️

---

## Summary

The backend API is fully implemented with all required endpoints for Crisis Explorer and Pathway Explorer. However, the frontend is reporting that these features "don't work" or are "slow to load". This diagnosis explores potential causes.

---

## Backend API Status

### ✅ Pathways API (`/api/pathways`)
**File**: `backend/api/routes/pathways.py`

**Endpoints**:
1. `GET /api/pathways` - List curated pathways (lines 261-296)
2. `GET /api/pathways/{pathway_id}` - Get pathway details (lines 299-375)
3. `GET /api/pathways/search` - Search pathways (lines 378-398)

**Implementation**:
- ✅ Full implementation with dynamic pathway generation
- ✅ Discovers pathways between intervention nodes and outcome nodes
- ✅ Uses DFS algorithm (`find_paths`) with max path length of 4
- ✅ Calculates evidence scores, directions, and tags
- ✅ Filters by category, tag, and minimum evidence

**Potential Issues**:
1. **Performance** - Dynamic pathway generation runs on every request
   - Queries all mechanisms from database (line 154)
   - Builds graph structure (line 161)
   - Runs DFS for every intervention→outcome pair (lines 187-252)
   - For production: Pre-compute and store pathways (lines 151-152)

2. **Hardcoded Node IDs** - Intervention/outcome nodes are hardcoded (lines 164-181)
   ```python
   intervention_nodes = [
       "housing_policy",
       "minimum_wage",
       "healthcare_access",
       # etc...
   ]
   outcome_nodes = [
       "health_outcomes",
       "mortality",
       "disease_burden",
       # etc...
   ]
   ```
   - If these node IDs don't exist in database, NO pathways will be generated
   - Empty result would appear as "slow" to user (waiting for nothing)

---

### ✅ Crisis Endpoints API (`/api/nodes/crisis-endpoints`)
**File**: `backend/api/routes/nodes.py`

**Endpoint**: `GET /api/nodes/crisis-endpoints` (lines 641-673)

**Implementation**:
- ✅ Queries all nodes from database
- ✅ Filters to scale=7 nodes using `get_node_scale()` function
- ✅ Returns crisis endpoints sorted alphabetically
- ✅ Includes categories: `crisis`, `biological` (if they map to scale=7)

**Scale Mapping** (lines 222-253):
```python
scale_mapping = {
    'political': 1,
    'built_environment': 2,
    'economic': 3,
    'social_services': 3,
    'social_environment': 4,
    'economic_individual': 4,
    'behavioral': 5,
    'psychosocial': 5,
    'healthcare_access': 6,
    'clinical': 6,
    'biological': 7,
    'crisis': 7
}
```

**Potential Issues**:
1. **No crisis nodes in database** - If no nodes have `category='crisis'` or `category='biological'`, the endpoint returns empty array `[]`
   - This would cause Crisis Explorer to show "No crisis endpoints found"
   - User would see empty selection panel

2. **Database not initialized** - If database is empty, no nodes exist

---

### ✅ Crisis Subgraph API (`/api/nodes/crisis-subgraph`)
**File**: `backend/api/routes/nodes.py`

**Endpoint**: `POST /api/nodes/crisis-subgraph` (lines 878-941)

**Implementation**:
- ✅ Full implementation with BFS upstream traversal
- ✅ Evidence quality filtering
- ✅ Category filtering
- ✅ Identifies policy levers (scale=1 nodes)
- ✅ Annotates nodes with degree from crisis
- ✅ Returns comprehensive stats

**Algorithm** (lines 332-516):
1. Filter edges by evidence strength
2. Build reverse graph (child → parent)
3. BFS upstream from each crisis node
4. Prune disconnected branches
5. Calculate statistics

**Potential Issues**:
1. **Missing mechanisms** - If no mechanisms exist in database, returns empty subgraph
2. **Crisis node validation** - Validates that selected nodes are actually scale=7 (lines 910-920)
   - If user somehow selects non-crisis nodes, returns 400 error

---

## Frontend API Integration

### Crisis Explorer View
**File**: `frontend/src/views/CrisisExplorerView.tsx`

**API Calls**:
1. `useCrisisEndpoints()` - Fetches crisis endpoints on mount
2. `useCrisisSubgraph()` - POST request when user clicks "Explore Pathways"

**Hook Implementation**:
- ✅ Correct endpoint: `/api/nodes/crisis-endpoints`
- ✅ Correct request transformation (snake_case)
- ✅ Error handling present
- ✅ Loading states present

**UI Flow**:
1. User opens Crisis Explorer → `useCrisisEndpoints()` fires
2. If endpoints load, user sees checkboxes
3. User selects endpoints + configures filters
4. User clicks "Explore Pathways" → `explorePathways()` fires
5. If successful, visualization renders

**Potential Issues**:
1. **No data to click** - If `/api/nodes/crisis-endpoints` returns `[]`, there are no checkboxes to click
2. **CORS issues** - If backend CORS not configured properly
3. **Wrong backend URL** - Frontend might be pointing to wrong backend

---

### Pathway Explorer View
**File**: `frontend/src/views/PathwayExplorerView.tsx` (not yet reviewed)

**Expected Hook**: `usePathways()`
**Expected Endpoint**: `/api/pathways`

**Potential Issues**:
1. **Slow loading** - Dynamic pathway generation is computationally expensive
   - Each request rebuilds entire graph
   - Runs DFS for all intervention→outcome pairs
   - Could take 5-10 seconds for large mechanism banks

2. **No pathways found** - If intervention/outcome node IDs don't exist in database
   - Returns empty array `[]`
   - Appears as "slow" or "not loading"

---

## Root Cause Diagnosis

### Most Likely Issue: **Empty Database**

If the database has not been populated with:
- ✅ Nodes (with proper categories)
- ✅ Mechanisms (with evidence quality)

Then:
1. **Crisis Explorer**: `/api/nodes/crisis-endpoints` returns `[]` → No endpoints to select
2. **Pathway Explorer**: `/api/pathways` returns `[]` → No pathways to display

### Second Most Likely: **Hardcoded Node IDs Don't Exist**

Pathways endpoint relies on hardcoded node IDs:
```python
"housing_policy", "minimum_wage", "healthcare_access",
"education_funding", "social_safety_net", "neighborhood_investment"
```

If these exact node IDs don't exist in the `nodes` table, the pathways endpoint returns `[]`.

### Third Most Likely: **Performance Issues**

Pathway generation is expensive. For a mechanism bank with:
- 500+ mechanisms
- 6 intervention nodes
- 6 outcome nodes

The algorithm runs 36 DFS searches (6×6), each checking up to depth 4. This could take 10-30 seconds on first request.

---

## Recommended Actions

### 1. Check Database Population
```bash
# Connect to database and check:
SELECT COUNT(*) FROM nodes;
SELECT COUNT(*) FROM mechanisms;
SELECT category, COUNT(*) FROM nodes GROUP BY category;
```

**Expected**:
- At least 50+ nodes
- At least 20+ mechanisms
- Some nodes with `category='crisis'` or `category='biological'`

### 2. Check Node IDs Match Hardcoded Values
```sql
SELECT id FROM nodes WHERE id IN (
  'housing_policy', 'minimum_wage', 'healthcare_access',
  'education_funding', 'social_safety_net', 'neighborhood_investment',
  'health_outcomes', 'mortality', 'disease_burden',
  'life_expectancy', 'health_equity', 'ald_mortality'
);
```

**Expected**: At least 2-3 intervention nodes and 2-3 outcome nodes should exist

### 3. Test Backend Endpoints Directly
```bash
# Test crisis endpoints
curl http://localhost:8002/api/nodes/crisis-endpoints

# Test pathways
curl http://localhost:8002/api/pathways?limit=5

# Test crisis subgraph (if crisis endpoints exist)
curl -X POST http://localhost:8002/api/nodes/crisis-subgraph \
  -H "Content-Type: application/json" \
  -d '{
    "crisis_node_ids": ["ald_mortality"],
    "max_degrees": 5,
    "min_strength": 2
  }'
```

**Expected**: Non-empty responses with actual data

### 4. Check Backend Server is Running
```bash
# Check if backend is listening on port 8002
curl http://localhost:8002/health

# Expected: {"status": "healthy", ...}
```

### 5. Check Frontend API Configuration
**File**: `frontend/src/utils/api.ts`

Verify `BASE_URL` is correctly pointing to backend:
```typescript
const BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8002';
```

### 6. Monitor Network Requests
Open browser DevTools → Network tab:
- Check if requests are being sent
- Check response status codes (200, 404, 500?)
- Check response bodies (empty arrays? error messages?)
- Check request timings (how long do requests take?)

---

## Next Steps

1. **Run database queries** to verify data exists
2. **Test backend endpoints directly** with curl
3. **Check frontend Network tab** for actual API calls and responses
4. **Add backend logging** to trace pathway generation performance
5. **Consider pre-computing pathways** for production (store in `pathways` table)

---

## Performance Optimization Recommendations

### For Pathway Explorer:
1. **Pre-compute pathways** on mechanism bank updates
2. **Cache pathway results** in Redis
3. **Limit DFS search depth** based on request (currently hardcoded to 4)
4. **Add pagination** to pathway list

### For Crisis Explorer:
1. **Cache crisis endpoints** (they rarely change)
2. **Optimize BFS traversal** with early termination
3. **Add query timeout** to prevent long-running requests

---

**Status**: Backend API is production-ready ✅
**Blockers**: Need to verify database is populated with nodes and mechanisms

