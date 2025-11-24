# HEALTHSYSTEMS PLATFORM - CONSOLIDATION IMPLEMENTATION PROMPTS

**Complete guide for refactoring and consolidating the codebase**

---

## Table of Contents

**HIGH PRIORITY (Week 1-2)**
1. [Consolidate Extraction Scripts](#prompt-1-consolidate-extraction-scripts) ✅ COMPLETE → See [CONSOLIDATION_PROMPT_1_EXTRACTION.md](./CONSOLIDATION_PROMPT_1_EXTRACTION.md)
2. [Consolidate Node Classification](#prompt-2-consolidate-node-classification) ✅ COMPLETE → See [CONSOLIDATION_PROMPT_2_CLASSIFICATION.md](./CONSOLIDATION_PROMPT_2_CLASSIFICATION.md)
3. [Unify Pathfinding Logic](#prompt-3-unify-pathfinding-logic) ✅ COMPLETE → See [CONSOLIDATION_PROMPT_3_PATHFINDING.md](./CONSOLIDATION_PROMPT_3_PATHFINDING.md)
4. [Remove Unused Dependencies](#prompt-4-remove-unused-dependencies) ✅ COMPLETE → See [CONSOLIDATION_PROMPT_4_DEPENDENCIES.md](./CONSOLIDATION_PROMPT_4_DEPENDENCIES.md)
5. [Reorganize Test Files](#prompt-5-reorganize-test-files) ✅ COMPLETE → See [CONSOLIDATION_PROMPT_5_TEST_ORGANIZATION.md](./CONSOLIDATION_PROMPT_5_TEST_ORGANIZATION.md)
6. [Consolidate Hook Utilities](#prompt-6-consolidate-hook-utilities) ✅ COMPLETE → See [CONSOLIDATION_PROMPT_6_HOOK_UTILITIES.md](./CONSOLIDATION_PROMPT_6_HOOK_UTILITIES.md)
7. [Centralize Configuration](#prompt-7-centralize-configuration) ✅ COMPLETE → See [CONSOLIDATION_PROMPT_7_CONFIGURATION.md](./CONSOLIDATION_PROMPT_7_CONFIGURATION.md)

**MEDIUM PRIORITY (Week 2-3)**
8. [Consolidate Graph Building](#prompt-8-consolidate-graph-building)
9. [Create Unified CLI](#prompt-9-create-unified-cli)

**LOW PRIORITY (Week 3+)**
10. [Remove Deprecated Code](#prompt-10-remove-deprecated-code)
11. [Consolidate Type Definitions](#prompt-11-consolidate-type-definitions)
12. [Standardize Utilities](#prompt-12-standardize-utilities)

---

# PROMPT 8: Consolidate Graph Building Logic

## Context
Graph construction logic duplicated across 4+ components. Each visualization builds its own nodes/edges from mechanisms, calculates weights differently, filters inconsistently.

## Current State

**Duplication Locations:**
- `frontend/src/utils/transformers.ts` (120 LOC): Main transformer
- `frontend/src/visualizations/MechanismGraph.tsx` (lines 156-162): Filter connected nodes
- `frontend/src/hooks/useAlcoholismSystem.ts` (90 LOC): Alcoholism filter
- `frontend/src/views/SystemsMapView.tsx` (lines 45-89): Transform + filter

**Common Operations (all duplicated):**
1. Transform API mechanisms → graph nodes
2. Calculate node connection counts (incoming/outgoing)
3. Filter nodes by category/scale
4. Build edges list from mechanisms
5. Calculate evidence strengths

## Redundancy Example

```typescript
// transformers.ts (lines 45-67)
function buildNodes(mechanisms: Mechanism[]): MechanismNode[] {
  const nodeMap = new Map<string, MechanismNode>();
  mechanisms.forEach(m => {
    if (!nodeMap.has(m.from_node_id)) {
      nodeMap.set(m.from_node_id, {
        id: m.from_node_id,
        label: m.from_node_name,
        connections: { incoming: 0, outgoing: 0 }
      });
    }
    // ... count connections
  });
}

// useAlcoholismSystem.ts (lines 34-55) - IDENTICAL PATTERN
const buildAlcoholismNodes = (mechanisms: Mechanism[]) => {
  const nodeMap = new Map<string, Node>();
  mechanisms.forEach(m => {
    if (!nodeMap.has(m.from_node_id)) {
      nodeMap.set(m.from_node_id, {
        id: m.from_node_id,
        label: m.from_node_name,
        connections: { incoming: 0, outgoing: 0 }
      });
    }
    // ... same logic
  });
}
```

## Target Architecture

```
frontend/src/utils/
├── graphBuilder.ts              # NEW: 250 LOC (unified)
│   ├── buildGraphFromMechanisms()
│   ├── filterGraphByCategory()
│   ├── filterGraphByScale()
│   ├── calculateNodeMetrics()
│   └── buildEdgeList()
│
├── transformers.ts              # 50 LOC (reduced from 120)
└── alcoholismFilter.ts          # DELETE (logic moved to graphBuilder)
```

## Implementation Steps

### Step 1: Create Unified Graph Builder

**File:** `frontend/src/utils/graphBuilder.ts`

```typescript
/**
 * Unified graph construction utilities
 * Consolidates graph building logic from multiple components
 */
import { Mechanism, MechanismNode, MechanismEdge, Category, SystemsNetwork } from '../types/mechanism';

export interface GraphBuildOptions {
  filterCategories?: Category[];
  filterScales?: number[];
  includeDisconnected?: boolean;
  calculateMetrics?: boolean;
}

/**
 * Build complete graph from mechanisms list
 */
export function buildGraphFromMechanisms(
  mechanisms: Mechanism[],
  options: GraphBuildOptions = {}
): SystemsNetwork {
  const {
    filterCategories,
    filterScales,
    includeDisconnected = false,
    calculateMetrics = true,
  } = options;

  // Build nodes map
  const nodeMap = new Map<string, MechanismNode>();
  const connectionCounts = new Map<string, { incoming: number; outgoing: number }>();

  mechanisms.forEach(mech => {
    // Apply category filter
    if (filterCategories && !filterCategories.includes(mech.category)) {
      return;
    }

    // Add from_node
    if (!nodeMap.has(mech.from_node_id)) {
      nodeMap.set(mech.from_node_id, {
        id: mech.from_node_id,
        label: mech.from_node_name,
        category: mech.category,
        scale: inferNodeScale(mech),
        stockType: 'structural', // Default
        connections: { incoming: 0, outgoing: 0 },
      });
      connectionCounts.set(mech.from_node_id, { incoming: 0, outgoing: 0 });
    }

    // Add to_node
    if (!nodeMap.has(mech.to_node_id)) {
      nodeMap.set(mech.to_node_id, {
        id: mech.to_node_id,
        label: mech.to_node_name,
        category: mech.category,
        scale: inferNodeScale(mech),
        stockType: 'structural',
        connections: { incoming: 0, outgoing: 0 },
      });
      connectionCounts.set(mech.to_node_id, { incoming: 0, outgoing: 0 });
    }

    // Count connections
    const fromCounts = connectionCounts.get(mech.from_node_id)!;
    const toCounts = connectionCounts.get(mech.to_node_id)!;
    fromCounts.outgoing++;
    toCounts.incoming++;
  });

  // Update nodes with connection counts
  nodeMap.forEach((node, id) => {
    node.connections = connectionCounts.get(id)!;
  });

  // Build edges
  const edges: MechanismEdge[] = mechanisms
    .filter(mech => {
      // Apply category filter
      if (filterCategories && !filterCategories.includes(mech.category)) {
        return false;
      }
      // Ensure both nodes exist
      return nodeMap.has(mech.from_node_id) && nodeMap.has(mech.to_node_id);
    })
    .map(mech => ({
      id: mech.id,
      source: mech.from_node_id,
      target: mech.to_node_id,
      direction: mech.direction,
      category: mech.category,
      evidenceQuality: mech.evidence_quality,
      name: mech.name,
    }));

  let nodes = Array.from(nodeMap.values());

  // Apply scale filter
  if (filterScales && filterScales.length > 0) {
    nodes = nodes.filter(n => n.scale && filterScales.includes(n.scale));
  }

  // Filter disconnected nodes if requested
  if (!includeDisconnected) {
    const connectedNodeIds = new Set<string>();
    edges.forEach(e => {
      connectedNodeIds.add(typeof e.source === 'string' ? e.source : e.source.id);
      connectedNodeIds.add(typeof e.target === 'string' ? e.target : e.target.id);
    });
    nodes = nodes.filter(n => connectedNodeIds.has(n.id));
  }

  return { nodes, edges };
}

/**
 * Filter existing graph by category
 */
export function filterGraphByCategory(
  graph: SystemsNetwork,
  categories: Category[]
): SystemsNetwork {
  if (categories.length === 0) return graph;

  const filteredEdges = graph.edges.filter(e => categories.includes(e.category));
  const connectedNodeIds = new Set<string>();

  filteredEdges.forEach(e => {
    connectedNodeIds.add(typeof e.source === 'string' ? e.source : e.source.id);
    connectedNodeIds.add(typeof e.target === 'string' ? e.target : e.target.id);
  });

  const filteredNodes = graph.nodes.filter(n => connectedNodeIds.has(n.id));

  return { nodes: filteredNodes, edges: filteredEdges };
}

/**
 * Filter graph by scale levels
 */
export function filterGraphByScale(
  graph: SystemsNetwork,
  scales: number[]
): SystemsNetwork {
  if (scales.length === 0) return graph;

  const filteredNodes = graph.nodes.filter(n => n.scale && scales.includes(n.scale));
  const nodeIds = new Set(filteredNodes.map(n => n.id));

  const filteredEdges = graph.edges.filter(e => {
    const sourceId = typeof e.source === 'string' ? e.source : e.source.id;
    const targetId = typeof e.target === 'string' ? e.target : e.target.id;
    return nodeIds.has(sourceId) && nodeIds.has(targetId);
  });

  return { nodes: filteredNodes, edges: filteredEdges };
}

/**
 * Calculate additional node metrics
 */
export function calculateNodeMetrics(graph: SystemsNetwork): SystemsNetwork {
  const nodes = graph.nodes.map(node => {
    const degree = node.connections.incoming + node.connections.outgoing;
    const centrality = degree / graph.nodes.length;

    return {
      ...node,
      degree,
      centrality,
    };
  });

  return { ...graph, nodes };
}

/**
 * Infer node scale from mechanism (placeholder logic)
 */
function inferNodeScale(mech: Mechanism): number {
  // TODO: Implement proper scale inference
  // For now, return default
  return 4;
}

/**
 * Get all unique categories from graph
 */
export function getGraphCategories(graph: SystemsNetwork): Category[] {
  const categories = new Set<Category>();
  graph.edges.forEach(e => categories.add(e.category));
  return Array.from(categories);
}

/**
 * Get all unique scales from graph
 */
export function getGraphScales(graph: SystemsNetwork): number[] {
  const scales = new Set<number>();
  graph.nodes.forEach(n => {
    if (n.scale) scales.add(n.scale);
  });
  return Array.from(scales).sort();
}

/**
 * Build alcoholism-specific subgraph
 */
export function buildAlcoholismSubgraph(mechanisms: Mechanism[]): SystemsNetwork {
  const alcoholismKeywords = [
    'alcohol', 'ald', 'liver', 'drinking', 'substance',
    'addiction', 'hepatitis', 'cirrhosis'
  ];

  const filtered = mechanisms.filter(m =>
    alcoholismKeywords.some(kw =>
      m.name.toLowerCase().includes(kw) ||
      m.from_node_name.toLowerCase().includes(kw) ||
      m.to_node_name.toLowerCase().includes(kw)
    )
  );

  return buildGraphFromMechanisms(filtered);
}
```

### Step 2: Update Transformers to Use Graph Builder

**File:** `frontend/src/utils/transformers.ts` (simplify)

```typescript
/**
 * Simplified transformers - delegates to graphBuilder
 */
import { Mechanism, SystemsNetwork } from '../types/mechanism';
import { buildGraphFromMechanisms, GraphBuildOptions } from './graphBuilder';

/**
 * Transform mechanisms to systems network
 * @deprecated Use buildGraphFromMechanisms directly
 */
export function transformToSystemsNetwork(
  mechanisms: Mechanism[],
  options?: GraphBuildOptions
): SystemsNetwork {
  return buildGraphFromMechanisms(mechanisms, options);
}
```

### Step 3: Update Components

**File:** `frontend/src/views/SystemsMapView.tsx` (lines 45-89)

```typescript
// BEFORE (lines 45-89):
const transformedData = useMemo(() => {
  if (!mechanisms) return { nodes: [], edges: [] };
  return transformToSystemsNetwork(mechanisms, {
    filterCategories: selectedCategories,
  });
}, [mechanisms, selectedCategories]);

// AFTER:
import { buildGraphFromMechanisms, filterGraphByCategory } from '../utils/graphBuilder';

const transformedData = useMemo(() => {
  if (!mechanisms) return { nodes: [], edges: [] };

  const graph = buildGraphFromMechanisms(mechanisms);

  if (selectedCategories.length > 0) {
    return filterGraphByCategory(graph, selectedCategories);
  }

  return graph;
}, [mechanisms, selectedCategories]);
```

### Step 4: Remove Alcoholism Filter (Consolidate)

**Delete:** `frontend/src/utils/alcoholismFilter.ts`

**Update:** `frontend/src/hooks/useAlcoholismSystem.ts`

```typescript
// BEFORE: Entire custom filter implementation (90 LOC)

// AFTER:
import { buildAlcoholismSubgraph } from '../utils/graphBuilder';

export function useAlcoholismSystem() {
  const { data: mechanisms } = useData();

  const alcoholismGraph = useMemo(() => {
    if (!mechanisms) return { nodes: [], edges: [] };
    return buildAlcoholismSubgraph(mechanisms);
  }, [mechanisms]);

  return alcoholismGraph;
}
```

## Migration Checklist

- [ ] Create `frontend/src/utils/graphBuilder.ts` (250 LOC)
- [ ] Simplify `transformers.ts` (reduce to 50 LOC)
- [ ] Update `SystemsMapView.tsx` to use graphBuilder
- [ ] Update `useAlcoholismSystem.ts` to use graphBuilder
- [ ] Update `MechanismGraph.tsx` if using custom filters
- [ ] Delete `alcoholismFilter.ts` (60 LOC removed)
- [ ] Write unit tests for graphBuilder (150 LOC)
- [ ] Run full test suite
- [ ] Verify all visualizations render correctly

## Testing

```typescript
// Test graph building
describe('graphBuilder', () => {
  test('builds nodes and edges from mechanisms', () => {
    const mechanisms = [mockMechanism1, mockMechanism2];
    const graph = buildGraphFromMechanisms(mechanisms);

    expect(graph.nodes).toHaveLength(3); // 2 unique nodes
    expect(graph.edges).toHaveLength(2);
  });

  test('filters by category', () => {
    const graph = buildGraphFromMechanisms(mechanisms);
    const filtered = filterGraphByCategory(graph, ['social']);

    expect(filtered.edges.every(e => e.category === 'social')).toBe(true);
  });
});
```

## Success Criteria

- [ ] **LOC Reduction**: 270 LOC → 250 LOC in single module (20 duplicates removed)
- [ ] **Single Source**: All graph building uses graphBuilder
- [ ] **Consistent**: Same node counts/weights across all views
- [ ] **Tests Pass**: 100% existing functionality preserved
- [ ] **Performance**: No regression in render times

**Effort:** 1 day (6 hours)

---

# PROMPT 9: Create Unified CLI

## Context
Backend scripts lack consistent CLI interface. Each script has custom argument parsing, no shared help text, inconsistent error handling. Need unified CLI tooling.

## Current State

**Scripts with Custom CLI:**
- `backend/scripts/regrade_mechanisms.py`: No args, interactive prompts
- `backend/scripts/classify_nodes.py` (Prompt 1): argparse
- `backend/scripts/run_generic_extraction.py`: argparse with different style
- `backend/scripts/apply_node_reclassification.py`: Hardcoded paths
- Multiple scripts: No CLI at all

**Issues:**
1. No consistent `--help` format
2. No `--version` flag
3. No `--verbose` logging control
4. No dry-run across all scripts
5. No unified error handling

## Target Architecture

```
backend/
├── cli/
│   ├── __init__.py
│   ├── main.py                    # Entry point: `healthsystems` command
│   ├── base.py                    # BaseCLI class
│   └── commands/
│       ├── __init__.py
│       ├── classify.py            # healthsystems classify
│       ├── extract.py             # healthsystems extract
│       ├── regrade.py             # healthsystems regrade
│       └── validate.py            # healthsystems validate
│
└── pyproject.toml                 # Add CLI entry point
```

## Implementation

### Step 1: Create Base CLI

**File:** `backend/cli/base.py`

```python
"""
Base CLI infrastructure for consistent command-line tools
"""
import argparse
import logging
import sys
from abc import ABC, abstractmethod
from pathlib import Path

class BaseCLI(ABC):
    """Base class for CLI commands with consistent interface."""

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    @abstractmethod
    def get_name(self) -> str:
        """Command name (e.g., 'classify', 'extract')."""
        pass

    @abstractmethod
    def get_description(self) -> str:
        """Command description for help text."""
        pass

    @abstractmethod
    def add_arguments(self, parser: argparse.ArgumentParser):
        """Add command-specific arguments to parser."""
        pass

    @abstractmethod
    def run(self, args: argparse.Namespace) -> int:
        """Execute command. Return 0 for success, non-zero for error."""
        pass

    def setup_logging(self, verbose: bool = False):
        """Configure logging based on verbosity."""
        level = logging.DEBUG if verbose else logging.INFO
        logging.basicConfig(
            level=level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

    def error_exit(self, message: str, code: int = 1):
        """Print error and exit."""
        self.logger.error(message)
        sys.exit(code)

def add_common_arguments(parser: argparse.ArgumentParser):
    """Add arguments common to all commands."""
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be done without making changes'
    )
```

### Step 2: Create Main CLI Entry Point

**File:** `backend/cli/main.py`

```python
"""
Main CLI entry point for healthsystems command
"""
import argparse
import sys
from pathlib import Path

from .commands.classify import ClassifyCommand
from .commands.extract import ExtractCommand
from .commands.regrade import RegradeCommand
from .commands.validate import ValidateCommand

__version__ = "1.0.0"

def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        prog='healthsystems',
        description='HealthSystems Platform CLI Tools'
    )
    parser.add_argument(
        '--version',
        action='version',
        version=f'healthsystems {__version__}'
    )

    # Subcommands
    subparsers = parser.add_subparsers(dest='command', required=True)

    # Register commands
    commands = [
        ClassifyCommand(),
        ExtractCommand(),
        RegradeCommand(),
        ValidateCommand(),
    ]

    for cmd in commands:
        cmd_parser = subparsers.add_parser(
            cmd.get_name(),
            help=cmd.get_description()
        )
        cmd.add_arguments(cmd_parser)
        cmd_parser.set_defaults(func=cmd.run)

    # Parse and execute
    args = parser.parse_args()

    # Setup logging for selected command
    for cmd in commands:
        if cmd.get_name() == args.command:
            cmd.setup_logging(getattr(args, 'verbose', False))
            break

    # Execute command
    try:
        exit_code = args.func(args)
        sys.exit(exit_code)
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
```

### Step 3: Create Command Modules

**File:** `backend/cli/commands/classify.py`

```python
"""Node classification command."""
import argparse
from pathlib import Path
from ..base import BaseCLI, add_common_arguments

class ClassifyCommand(BaseCLI):
    def get_name(self) -> str:
        return 'classify'

    def get_description(self) -> str:
        return 'Classify nodes in inventory file using 7-scale taxonomy'

    def add_arguments(self, parser: argparse.ArgumentParser):
        parser.add_argument(
            'input_file',
            type=Path,
            help='Input node inventory file'
        )
        parser.add_argument(
            '-o', '--output',
            type=Path,
            help='Output file (default: overwrite input)'
        )
        parser.add_argument(
            '--format',
            choices=['numeric', 'text'],
            default='numeric',
            help='Scale format (default: numeric)'
        )
        add_common_arguments(parser)

    def run(self, args: argparse.Namespace) -> int:
        self.logger.info(f"Classifying nodes in: {args.input_file}")

        if args.dry_run:
            self.logger.info("[DRY RUN] No changes will be made")
            return 0

        # Import and run classification
        from backend.core.node_classification import NumericScaleClassifier

        classifier = NumericScaleClassifier()
        # ... run classification logic

        self.logger.info("Classification complete")
        return 0
```

**File:** `backend/cli/commands/extract.py`

```python
"""Mechanism extraction command."""
import argparse
from ..base import BaseCLI, add_common_arguments

class ExtractCommand(BaseCLI):
    def get_name(self) -> str:
        return 'extract'

    def get_description(self) -> str:
        return 'Extract mechanisms using LLM pipeline'

    def add_arguments(self, parser: argparse.ArgumentParser):
        parser.add_argument(
            'extractor',
            choices=['alcohol', 'generic'],
            help='Extraction type'
        )
        parser.add_argument(
            '--config',
            type=Path,
            help='Config file for generic extraction'
        )
        parser.add_argument(
            '--phases',
            type=str,
            help='Comma-separated phase numbers (e.g., "1,2,3")'
        )
        add_common_arguments(parser)

    def run(self, args: argparse.Namespace) -> int:
        if args.extractor == 'generic' and not args.config:
            self.error_exit("--config required for generic extraction")

        self.logger.info(f"Running {args.extractor} extraction")

        # Import and run extraction
        from backend.extraction import AlcoholExtractor, GenericTopicExtractor

        # ... run extraction logic

        return 0
```

### Step 4: Add CLI Entry Point to pyproject.toml

**File:** `backend/pyproject.toml`

```toml
[project]
name = "healthsystems"
version = "1.0.0"
description = "HealthSystems Platform Backend"

[project.scripts]
healthsystems = "backend.cli.main:main"

[build-system]
requires = ["setuptools>=45", "wheel"]
build-backend = "setuptools.build_meta"
```

### Step 5: Install and Test

```bash
# Install in development mode
cd backend
pip install -e .

# Test CLI
healthsystems --version
healthsystems --help

# Test subcommands
healthsystems classify --help
healthsystems extract --help

# Run commands
healthsystems classify Nodes/COMPLETE_NODE_INVENTORY.md --dry-run
healthsystems extract alcohol --phases 1,2 --dry-run --verbose
```

## Migration Checklist

- [ ] Create `backend/cli/` directory structure
- [ ] Implement `base.py` with BaseCLI class
- [ ] Implement `main.py` entry point
- [ ] Implement command modules (classify, extract, regrade, validate)
- [ ] Update `pyproject.toml` with CLI entry point
- [ ] Install package in development mode
- [ ] Test all commands with `--help`
- [ ] Test all commands with `--dry-run`
- [ ] Update documentation with CLI usage
- [ ] Update CI/CD to use new CLI commands

## Success Criteria

- [ ] **Consistent Interface**: All scripts accessible via `healthsystems` command
- [ ] **Help Text**: Comprehensive `--help` for all commands
- [ ] **Dry Run**: All commands support `--dry-run`
- [ ] **Logging**: Unified logging with `--verbose` flag
- [ ] **Error Handling**: Consistent exit codes and error messages
- [ ] **Versioning**: `--version` flag works
- [ ] **Documentation**: Complete CLI reference guide

**Effort:** 1 day (6 hours)

---

# PROMPT 10: Remove Deprecated Code

## Context
Codebase contains deprecated functions, commented code, outdated TODOs. These create confusion and maintenance burden.

## Deprecated Code Locations

### Backend
1. `backend/api/routes/mechanisms.py` (lines 140-152): Deprecated `/search/pathway` endpoint (already removed)
2. `backend/algorithms/bayesian_weighting.py` (lines 79-80, 171-172): TODO stubs
3. Multiple scripts: Old extraction scripts after consolidation

### Frontend
1. `frontend/src/hooks/useNodeImportance.ts` (line 186): Deprecated `getScaleMultiplier` function
2. Old hook files after consolidation
3. Test files with outdated patterns

## Actions

### Backend Cleanup

```python
# DELETE these after consolidation (Prompt 1):
# backend/scripts/apply_node_reclassification.py
# backend/scripts/reclassify_nodes_v2.py
# backend/scripts/aggressive_redistribution.py

# DELETE these after consolidation (Extraction):
# backend/scripts/run_alcohol_extraction.py
# backend/scripts/batch_alcohol_mechanisms.py
# backend/scripts/test_extraction.py
# etc.

# IMPLEMENT stubbed TODOs in bayesian_weighting.py
```

### Frontend Cleanup

```typescript
// REMOVE deprecated exports
// frontend/src/hooks/useNodeImportance.ts (lines 186-200)
/**
 * @deprecated Scale multipliers removed in Phase 4
 */
export function getScaleMultiplier(scale: NodeScale | null): number {
  // DELETE THIS
}

// DELETE old utility files after consolidation:
// frontend/src/utils/alcoholismFilter.ts (consolidated into graphBuilder)
```

## Implementation

```bash
# Backend
find backend/ -name "*.py" -exec grep -l "TODO\|FIXME\|DEPRECATED" {} \;
# Review and either implement or remove

# Frontend
find frontend/src/ -name "*.ts*" -exec grep -l "@deprecated\|TODO\|FIXME" {} \;
# Review and remove
```

## Success Criteria

- [ ] All deprecated functions removed
- [ ] All TODO comments resolved or ticketed
- [ ] All commented-out code blocks removed
- [ ] Zero deprecation warnings in build

**Effort:** 0.5 days (3 hours)

---

# PROMPT 11: Consolidate Type Definitions

## Context
TypeScript types defined in multiple locations with slight variations, causing inconsistencies and type errors.

## Current State

**Type Duplication:**
- `Category` type: Defined in 3 files
- `EvidenceQuality`: Defined in 2 files
- Path-related types: Defined inline in hooks
- Graph types: Split across multiple files

## Target Architecture

```
frontend/src/types/
├── index.ts              # Central exports
├── mechanism.ts          # Core types (already main file)
├── graph.ts              # Graph-specific types
├── pathway.ts            # Pathway types
└── api.ts                # API request/response types
```

## Implementation

**File:** `frontend/src/types/index.ts`

```typescript
/**
 * Central type exports
 */

// Re-export from mechanism.ts
export type {
  Category,
  NodeScale,
  EvidenceQuality,
  Mechanism,
  MechanismNode,
  MechanismEdge,
  SystemsNetwork,
} from './mechanism';

// Re-export from graph.ts
export type {
  GraphLayoutMode,
  PhysicsSettings,
  CrisisHighlight,
} from './graph';

// Re-export from pathway.ts
export type {
  PathResult,
  PathNode,
  PathMechanism,
  PathfindingRequest,
  PathfindingResponse,
} from './pathway';

// Re-export from api.ts
export type {
  ApiError,
  ApiResponse,
} from './api';
```

## Migration

```typescript
// BEFORE: Multiple imports
import { Category } from '../types/mechanism';
import { PathResult } from '../hooks/usePathfinding';
import { GraphLayoutMode } from '../visualizations/MechanismGraph';

// AFTER: Single import
import { Category, PathResult, GraphLayoutMode } from '../types';
```

## Success Criteria

- [ ] All types centralized in `types/` directory
- [ ] Single `import { ... } from '../types'` pattern
- [ ] Zero type duplication
- [ ] All components type-check correctly

**Effort:** 0.5 days (3 hours)

---

# PROMPT 12: Standardize Utility Functions

## Context
Utility functions scattered across codebase with inconsistent naming and patterns.

## Target Standard

```
frontend/src/utils/
├── index.ts              # Central exports
├── graphBuilder.ts       # Graph operations (Prompt 8)
├── graphFilters.ts       # Filter utilities (Prompt 6)
├── graphTransforms.ts    # Transform utilities (Prompt 6)
├── colors.ts             # Color utilities (KEEP - already good)
├── classNames.ts         # Class utilities (KEEP)
└── validation.ts         # NEW: Validation helpers
```

## Actions

1. **Move API helpers** from inline to `utils/apiHelpers.ts` (done in Prompt 6)
2. **Consolidate array utilities** into `graphTransforms.ts` (done in Prompt 6)
3. **Create validation utils** for form/data validation
4. **Remove duplicate helpers** after consolidation

## Implementation

**File:** `frontend/src/utils/validation.ts`

```typescript
/**
 * Validation utilities
 */

export function isValidNodeId(id: string): boolean {
  return id.length > 0 && /^[a-z0-9_]+$/.test(id);
}

export function isValidScale(scale: number): boolean {
  return Number.isInteger(scale) && scale >= 1 && scale <= 7;
}

export function isValidCategory(category: string): boolean {
  const validCategories = [
    'economic', 'healthcare_access', 'social_environment',
    'built_environment', 'political', 'behavioral', 'biological'
  ];
  return validCategories.includes(category);
}
```

**File:** `frontend/src/utils/index.ts` (update)

```typescript
/**
 * Central utility exports
 */

// Graph utilities
export * from './graphBuilder';
export * from './graphFilters';
export * from './graphTransforms';

// API utilities
export * from './apiHelpers';

// UI utilities
export { classNames } from './classNames';
export * from './colors';

// Validation
export * from './validation';
```

## Success Criteria

- [ ] All utilities organized by domain
- [ ] Single `import { ... } from '../utils'` pattern
- [ ] Zero duplicate utility functions
- [ ] Clear naming conventions followed

**Effort:** 0.5 days (3 hours)

---

# SUMMARY TABLE

| Prompt | Priority | LOC Saved | Files Changed | Effort (days) | Status |
|--------|----------|-----------|---------------|---------------|---------|
| 1. Extraction Scripts | HIGH | 1,316 | 6 → 5 | 2-3 | ✅ Detailed |
| 2. Node Classification | HIGH | 992 | 4 → 2 | 2 | ✅ Detailed |
| 3. Pathfinding Logic | HIGH | 121 | 3 → 1 | 1.5 | ✅ Detailed |
| 4. Dependencies | HIGH | 0* | 1 | 0.5 | ✅ Detailed |
| 5. Test Organization | HIGH | 0* | 8 → organized | 0.5 | ✅ Detailed |
| 6. Hook Utilities | HIGH | 450 | 5 → refactored | 2 | ✅ Detailed |
| 7. Configuration | MEDIUM | 0* | 15+ → centralized | 1 | ✅ Detailed |
| 8. Graph Building | MEDIUM | 20 | 4 → 1 | 1 | ✅ |
| 9. Unified CLI | MEDIUM | 0* | 11+ → CLI | 1 | ✅ |
| 10. Deprecated Code | LOW | ~200 | cleanup | 0.5 | ✅ |
| 11. Type Definitions | LOW | ~50 | 5+ → 5 | 0.5 | ✅ |
| 12. Standard Utilities | LOW | 0* | organized | 0.5 | ✅ |
| **TOTAL** | | **3,149** | **50+** | **13-14** | |

\* LOC saved reflected in code organization/maintainability rather than raw line count

---

# IMPLEMENTATION ORDER

## Week 1: High Priority
**Day 1-2:** Extraction Scripts (Prompt 1)
**Day 3-4:** Node Classification (Prompt 2)
**Day 5:** Pathfinding + Dependencies (Prompts 3, 4)

## Week 2: High Priority Continued
**Day 1:** Test Organization (Prompt 5)
**Day 2-3:** Hook Utilities (Prompt 6)
**Day 4-5:** Configuration (Prompt 7)

## Week 3: Medium + Low Priority
**Day 1:** Graph Building (Prompt 8)
**Day 2:** Unified CLI (Prompt 9)
**Day 3:** Cleanup (Prompts 10, 11, 12)

**Total Estimated Effort:** 13-14 days (~3 weeks)

---

# VALIDATION CHECKLIST

After completing all prompts:

- [ ] Run full backend test suite: `pytest`
- [ ] Run full frontend test suite: `npm test`
- [ ] Build frontend: `npm run build`
- [ ] Check bundle size reduction
- [ ] Run linting: `npm run lint` / `flake8`
- [ ] Verify API endpoints work
- [ ] Test all CLI commands
- [ ] Manual QA of all features
- [ ] Update all documentation
- [ ] Create migration guide for team

---

**Document Version:** 1.0
**Last Updated:** 2025
**Maintainer:** HealthSystems Platform Team
