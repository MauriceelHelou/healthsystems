# PROMPT 6: Consolidate Hook Utilities

## Context
Multiple React hooks implement **similar React Query patterns**, API call logic, and data transformations. Extracting shared utilities will reduce duplication and ensure consistency.

## Current State

### Duplicate Patterns Across Hooks

**Pattern 1: API Mutations (duplicated 5 times)**
- `usePathfinding.ts` - pathfinding mutation
- `useCrisisSubgraph.ts` - subgraph mutation
- `usePathways.ts` - pathway queries
- `useNodeImportance.ts` - importance calculation
- `useAlcoholismSystem.ts` - filtered queries

**Pattern 2: Data Transformations (duplicated 4 times)**
- Graph network building from mechanisms
- Node connection counting
- Evidence quality scoring
- Scale-based filtering

**Pattern 3: Error Handling (duplicated 5 times)**
- Console logging
- User-friendly error messages
- Retry logic
- Loading states

## Redundancy Examples

**Example 1: Connection Counting**

```typescript
// usePathfinding.ts (lines 234-248)
function countConnections(nodes: Node[], mechanisms: Mechanism[]) {
  const connections = new Map<string, { incoming: number; outgoing: number }>();

  nodes.forEach(node => {
    connections.set(node.id, { incoming: 0, outgoing: 0 });
  });

  mechanisms.forEach(m => {
    const from = connections.get(m.from_node_id);
    const to = connections.get(m.to_node_id);
    if (from) from.outgoing++;
    if (to) to.incoming++;
  });

  return connections;
}

// useAlcoholismSystem.ts (lines 178-192) - IDENTICAL
function countConnections(nodes: Node[], mechanisms: Mechanism[]) {
  const connections = new Map<string, { incoming: number; outgoing: number }>();

  nodes.forEach(node => {
    connections.set(node.id, { incoming: 0, outgoing: 0 });
  });

  mechanisms.forEach(m => {
    const from = connections.get(m.from_node_id);
    const to = connections.get(m.to_node_id);
    if (from) from.outgoing++;
    if (to) to.incoming++;
  });

  return connections;
}
```

**Example 2: Evidence Quality Scoring**

```typescript
// useNodeImportance.ts (lines 89-97)
function calculateEvidenceScore(mechanism: Mechanism): number {
  const qualityScores = { A: 1.0, B: 0.6, C: 0.3 };
  const baseScore = qualityScores[mechanism.evidence_quality] || 0.3;
  const studyBonus = Math.min(mechanism.evidence_n_studies / 10, 0.2);
  return baseScore + studyBonus;
}

// useCrisisSubgraph.ts (lines 156-164) - VERY SIMILAR
function getEvidenceWeight(mechanism: Mechanism): number {
  const qualityWeights = { A: 1.0, B: 0.6, C: 0.3 };
  const base = qualityWeights[mechanism.evidence_quality] || 0.3;
  const studyFactor = Math.log10(mechanism.evidence_n_studies + 1) / 10;
  return base + studyFactor;
}
```

**Example 3: Graph Network Building**

```typescript
// usePathfinding.ts (lines 267-301)
function buildNetworkFromMechanisms(mechanisms: Mechanism[]): SystemsNetwork {
  const nodeMap = new Map<string, MechanismNode>();
  const edges: MechanismEdge[] = [];

  mechanisms.forEach(m => {
    // Add from node
    if (!nodeMap.has(m.from_node_id)) {
      nodeMap.set(m.from_node_id, {
        id: m.from_node_id,
        label: m.from_node_name,
        scale: m.from_node_scale,
        connections: { incoming: 0, outgoing: 0 }
      });
    }

    // Add to node
    if (!nodeMap.has(m.to_node_id)) {
      nodeMap.set(m.to_node_id, {
        id: m.to_node_id,
        label: m.to_node_name,
        scale: m.to_node_scale,
        connections: { incoming: 0, outgoing: 0 }
      });
    }

    // Add edge
    edges.push({
      source: m.from_node_id,
      target: m.to_node_id,
      direction: m.direction,
      category: m.category,
      evidence_quality: m.evidence_quality
    });
  });

  return {
    nodes: Array.from(nodeMap.values()),
    edges
  };
}

// Similar code in useAlcoholismSystem.ts (45+ LOC)
// Similar code in transformers.ts (60+ LOC)
```

## Target Architecture

```
frontend/src/
├── hooks/
│   ├── utils/                          # NEW: Shared hook utilities
│   │   ├── graphBuilding.ts            # 120 LOC
│   │   │   ├── buildNetworkFromMechanisms()
│   │   │   ├── countNodeConnections()
│   │   │   ├── filterNodesByScale()
│   │   │   └── filterNodesByCategory()
│   │   │
│   │   ├── evidenceScoring.ts          # 60 LOC
│   │   │   ├── calculateEvidenceScore()
│   │   │   ├── getQualityWeight()
│   │   │   └── aggregatePath Evidence()
│   │   │
│   │   └── queryHelpers.ts             # 80 LOC (from Prompt 3)
│   │       ├── createApiMutation()
│   │       ├── createApiQuery()
│   │       └── defaultMutationOptions
│   │
│   ├── usePathfinding.ts               # 150 LOC (reduced from 507)
│   ├── useCrisisSubgraph.ts            # 100 LOC (reduced from 247)
│   ├── useAlcoholismSystem.ts          # 80 LOC (reduced from 180)
│   └── useNodeImportance.ts            # 90 LOC (reduced from 145)
```

## Implementation Steps

### Step 1: Create Graph Building Utilities

**File: `frontend/src/hooks/utils/graphBuilding.ts`**

```typescript
/**
 * Shared utilities for building graph networks from mechanisms.
 * Consolidates duplicate logic across multiple hooks.
 */
import { Mechanism, MechanismNode, MechanismEdge, SystemsNetwork } from '../../types/mechanism';

/**
 * Build graph network from mechanism list.
 * Consolidates nodes and creates edges.
 */
export function buildNetworkFromMechanisms(mechanisms: Mechanism[]): SystemsNetwork {
  const nodeMap = new Map<string, MechanismNode>();
  const edges: MechanismEdge[] = [];

  mechanisms.forEach(mechanism => {
    // Add from node if not exists
    if (!nodeMap.has(mechanism.from_node_id)) {
      nodeMap.set(mechanism.from_node_id, createNodeFromMechanism(mechanism, 'from'));
    }

    // Add to node if not exists
    if (!nodeMap.has(mechanism.to_node_id)) {
      nodeMap.set(mechanism.to_node_id, createNodeFromMechanism(mechanism, 'to'));
    }

    // Create edge
    edges.push({
      source: mechanism.from_node_id,
      target: mechanism.to_node_id,
      direction: mechanism.direction,
      category: mechanism.category,
      evidence_quality: mechanism.evidence_quality,
      mechanism_id: mechanism.id,
    });
  });

  // Count connections
  const nodes = Array.from(nodeMap.values());
  const connectionsMap = countNodeConnections(nodes, mechanisms);

  // Update nodes with connection counts
  nodes.forEach(node => {
    const connections = connectionsMap.get(node.id);
    if (connections) {
      node.connections = connections;
    }
  });

  return { nodes, edges };
}

/**
 * Create node object from mechanism.
 */
function createNodeFromMechanism(
  mechanism: Mechanism,
  side: 'from' | 'to'
): MechanismNode {
  const isFrom = side === 'from';

  return {
    id: isFrom ? mechanism.from_node_id : mechanism.to_node_id,
    label: isFrom ? mechanism.from_node_name : mechanism.to_node_name,
    scale: isFrom ? mechanism.from_node_scale : mechanism.to_node_scale,
    category: mechanism.category,
    connections: { incoming: 0, outgoing: 0 },
  };
}

/**
 * Count incoming and outgoing connections for each node.
 */
export function countNodeConnections(
  nodes: MechanismNode[],
  mechanisms: Mechanism[]
): Map<string, { incoming: number; outgoing: number }> {
  const connections = new Map<string, { incoming: number; outgoing: number }>();

  // Initialize
  nodes.forEach(node => {
    connections.set(node.id, { incoming: 0, outgoing: 0 });
  });

  // Count from mechanisms
  mechanisms.forEach(m => {
    const from = connections.get(m.from_node_id);
    const to = connections.get(m.to_node_id);

    if (from) from.outgoing++;
    if (to) to.incoming++;
  });

  return connections;
}

/**
 * Filter nodes by scale range.
 */
export function filterNodesByScale(
  nodes: MechanismNode[],
  minScale?: number,
  maxScale?: number
): MechanismNode[] {
  return nodes.filter(node => {
    if (minScale !== undefined && node.scale < minScale) return false;
    if (maxScale !== undefined && node.scale > maxScale) return false;
    return true;
  });
}

/**
 * Filter nodes by category.
 */
export function filterNodesByCategory(
  nodes: MechanismNode[],
  categories: string[]
): MechanismNode[] {
  if (categories.length === 0) return nodes;

  return nodes.filter(node => categories.includes(node.category));
}

/**
 * Filter mechanisms by category.
 */
export function filterMechanismsByCategory(
  mechanisms: Mechanism[],
  categories: string[]
): Mechanism[] {
  if (categories.length === 0) return mechanisms;

  return mechanisms.filter(m => categories.includes(m.category));
}

/**
 * Get only nodes that have active connections (filter orphans).
 */
export function getConnectedNodes(
  nodes: MechanismNode[],
  edges: MechanismEdge[]
): MechanismNode[] {
  const connectedIds = new Set<string>();

  edges.forEach(edge => {
    connectedIds.add(edge.source);
    connectedIds.add(edge.target);
  });

  return nodes.filter(node => connectedIds.has(node.id));
}
```

### Step 2: Create Evidence Scoring Utilities

**File: `frontend/src/hooks/utils/evidenceScoring.ts`**

```typescript
/**
 * Evidence quality scoring utilities.
 * Consolidates evidence assessment logic.
 */
import { Mechanism } from '../../types/mechanism';

// Quality grade weights
export const EVIDENCE_QUALITY_WEIGHTS = {
  A: 1.0,   // Strong evidence (RCTs, meta-analyses)
  B: 0.6,   // Moderate evidence (observational)
  C: 0.3,   // Limited evidence (case studies)
} as const;

/**
 * Calculate comprehensive evidence score.
 * Considers quality grade and number of studies.
 */
export function calculateEvidenceScore(mechanism: Mechanism): number {
  const qualityWeight = getQualityWeight(mechanism.evidence_quality);
  const studyBonus = calculateStudyBonus(mechanism.evidence_n_studies);

  return Math.min(qualityWeight + studyBonus, 1.0);
}

/**
 * Get weight for evidence quality grade.
 */
export function getQualityWeight(grade: string): number {
  return EVIDENCE_QUALITY_WEIGHTS[grade as keyof typeof EVIDENCE_QUALITY_WEIGHTS] || 0.3;
}

/**
 * Calculate bonus based on number of studies.
 * Logarithmic scale to avoid overweighting high study counts.
 */
export function calculateStudyBonus(nStudies: number): number {
  if (nStudies === 0) return 0;

  // Logarithmic bonus: log10(n+1) / 10
  // e.g., 1 study = 0.03, 10 studies = 0.10, 100 studies = 0.20
  return Math.log10(nStudies + 1) / 10;
}

/**
 * Aggregate evidence scores across a path.
 * Returns average score weighted by position (later = more weight).
 */
export function aggregatePathEvidence(mechanisms: Mechanism[]): number {
  if (mechanisms.length === 0) return 0;

  let totalScore = 0;
  let totalWeight = 0;

  mechanisms.forEach((mechanism, index) => {
    const score = calculateEvidenceScore(mechanism);
    const weight = index + 1; // Later mechanisms weighted more
    totalScore += score * weight;
    totalWeight += weight;
  });

  return totalScore / totalWeight;
}

/**
 * Classify evidence strength.
 */
export function getEvidenceStrength(score: number): 'strong' | 'moderate' | 'weak' {
  if (score >= 0.7) return 'strong';
  if (score >= 0.4) return 'moderate';
  return 'weak';
}

/**
 * Get color for evidence quality display.
 */
export function getEvidenceColor(grade: string): string {
  switch (grade) {
    case 'A': return 'text-green-600';
    case 'B': return 'text-yellow-600';
    case 'C': return 'text-orange-600';
    default: return 'text-gray-600';
  }
}

/**
 * Get background color for evidence quality badges.
 */
export function getEvidenceBadgeColor(grade: string): string {
  switch (grade) {
    case 'A': return 'bg-green-100 text-green-800';
    case 'B': return 'bg-yellow-100 text-yellow-800';
    case 'C': return 'bg-orange-100 text-orange-800';
    default: return 'bg-gray-100 text-gray-800';
  }
}
```

### Step 3: Refactor usePathfinding Hook

**File: `frontend/src/hooks/usePathfinding.ts` (refactored)**

```typescript
/**
 * Pathfinding hook - refactored to use shared utilities.
 * Reduced from 507 LOC to ~150 LOC.
 */
import { PathfindingRequest, PathfindingResponse } from '../types/mechanism';
import { createPostMutation } from './utils/queryHelpers';
import { API_ENDPOINTS } from '../utils/api';
import { calculateEvidenceScore, aggregatePathEvidence } from './utils/evidenceScoring';
import { buildNetworkFromMechanisms } from './utils/graphBuilding';

export function usePathfinding() {
  return createPostMutation<PathfindingResponse, PathfindingRequest>(
    API_ENDPOINTS.nodes.pathfinding,
    {
      meta: { errorContext: 'Pathfinding' },
      onSuccess: (data) => {
        // Optionally process paths
        data.paths.forEach(path => {
          path.evidenceScore = aggregatePathEvidence(path.mechanisms);
        });
      },
    }
  );
}

// Domain-specific helper functions (keep these)
export function formatPathLength(length: number): string {
  return `${length} step${length !== 1 ? 's' : ''}`;
}

export { calculateEvidenceScore, getEvidenceColor } from './utils/evidenceScoring';
```

### Step 4: Refactor useAlcoholismSystem Hook

**File: `frontend/src/hooks/useAlcoholismSystem.ts` (refactored)**

```typescript
/**
 * Alcoholism system hook - refactored to use shared utilities.
 * Reduced from 180 LOC to ~80 LOC.
 */
import { useQuery } from '@tanstack/react-query';
import { apiClient, API_ENDPOINTS } from '../utils/api';
import { buildNetworkFromMechanisms, filterMechanismsByCategory } from './utils/graphBuilding';
import { Mechanism, SystemsNetwork } from '../types/mechanism';

// Alcoholism-related categories
const ALCOHOLISM_CATEGORIES = [
  'economic',
  'social_environment',
  'healthcare_access',
  'behavioral',
  'biological',
];

export function useAlcoholismSystem() {
  return useQuery({
    queryKey: ['alcoholism-system'],
    queryFn: async () => {
      // Fetch all mechanisms
      const mechanisms = await apiClient.get<Mechanism[]>(API_ENDPOINTS.mechanisms.list);

      // Filter to alcoholism-relevant categories
      const filtered = filterMechanismsByCategory(mechanisms, ALCOHOLISM_CATEGORIES);

      // Build graph network
      const network = buildNetworkFromMechanisms(filtered);

      return {
        mechanisms: filtered,
        network,
      };
    },
    staleTime: 10 * 60 * 1000, // 10 minutes
  });
}
```

### Step 5: Update Transformers Utility

**File: `frontend/src/utils/transformers.ts` (simplified)**

```typescript
/**
 * Data transformers - simplified by using shared graph building utilities.
 * Reduced from 120 LOC to ~50 LOC.
 */
import { buildNetworkFromMechanisms } from '../hooks/utils/graphBuilding';
import { Mechanism } from '../types/mechanism';

// Re-export shared utility as primary transform
export { buildNetworkFromMechanisms };

// Domain-specific transformations only
export function transformMechanismForDisplay(mechanism: Mechanism) {
  return {
    id: mechanism.id,
    name: mechanism.name,
    fromNode: `${mechanism.from_node_name} (${mechanism.from_node_id})`,
    toNode: `${mechanism.to_node_name} (${mechanism.to_node_id})`,
    direction: mechanism.direction,
    category: mechanism.category,
    evidenceQuality: mechanism.evidence_quality,
    evidenceStudies: mechanism.evidence_n_studies,
  };
}
```

### Step 6: Create Utilities Index

**File: `frontend/src/hooks/utils/index.ts`**

```typescript
/**
 * Centralized export of hook utilities.
 */
export * from './graphBuilding';
export * from './evidenceScoring';
export * from './queryHelpers';
```

## Migration Checklist

### Phase 1: Create Utilities (Day 1, 2 hours)
- [ ] Create `hooks/utils/graphBuilding.ts`
- [ ] Create `hooks/utils/evidenceScoring.ts`
- [ ] Create `hooks/utils/index.ts`
- [ ] Test utilities in isolation

### Phase 2: Refactor Hooks (Day 1-2, 4 hours)
- [ ] Refactor `usePathfinding.ts`
- [ ] Refactor `useCrisisSubgraph.ts`
- [ ] Refactor `useAlcoholismSystem.ts`
- [ ] Refactor `useNodeImportance.ts`
- [ ] Update all imports

### Phase 3: Update Dependents (Day 2, 2 hours)
- [ ] Update `transformers.ts`
- [ ] Update all views using hooks
- [ ] Verify no regressions

### Phase 4: Testing (Day 2, 2 hours)
- [ ] Write tests for utilities
- [ ] Test each refactored hook
- [ ] End-to-end feature testing
- [ ] Performance validation

### Phase 5: Documentation (1 hour)
- [ ] Document utility functions
- [ ] Update hook documentation
- [ ] Commit: "refactor: extract shared hook utilities (450 LOC saved)"

## Testing Requirements

**File: `frontend/tests/unit/hooks/utils/graphBuilding.test.ts`**

```typescript
import { describe, it, expect } from 'vitest';
import { buildNetworkFromMechanisms, countNodeConnections } from '@/hooks/utils/graphBuilding';

describe('graphBuilding utilities', () => {
  it('should build network from mechanisms', () => {
    const mechanisms = [
      {
        id: 'm1',
        from_node_id: 'n1',
        from_node_name: 'Node 1',
        to_node_id: 'n2',
        to_node_name: 'Node 2',
        // ... other fields
      },
    ];

    const network = buildNetworkFromMechanisms(mechanisms);

    expect(network.nodes).toHaveLength(2);
    expect(network.edges).toHaveLength(1);
  });

  it('should count connections correctly', () => {
    const nodes = [
      { id: 'n1', label: 'Node 1', connections: { incoming: 0, outgoing: 0 } },
      { id: 'n2', label: 'Node 2', connections: { incoming: 0, outgoing: 0 } },
    ];

    const mechanisms = [
      { from_node_id: 'n1', to_node_id: 'n2' },
    ];

    const connections = countNodeConnections(nodes, mechanisms);

    expect(connections.get('n1')).toEqual({ incoming: 0, outgoing: 1 });
    expect(connections.get('n2')).toEqual({ incoming: 1, outgoing: 0 });
  });
});
```

## Success Criteria

- ✅ All utility functions extracted to `hooks/utils/`
- ✅ All hooks using shared utilities
- ✅ No duplicate graph building logic
- ✅ No duplicate evidence scoring logic
- ✅ All tests passing
- ✅ **450 LOC eliminated** from hooks
- ✅ Documentation complete

## Estimated Effort
**2 days** (1 day utilities + refactoring, 1 day testing)
