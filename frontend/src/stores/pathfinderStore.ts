/**
 * pathfinderStore - Zustand store for pathfinder state management
 *
 * Manages the state for the pathfinder feature including:
 * - Selected from/to nodes
 * - Active path selection
 * - Pathfinding options
 * - UI state (selection mode)
 *
 * @example
 * ```tsx
 * const {
 *   fromNode,
 *   toNode,
 *   setFromNode,
 *   setToNode,
 *   selectedPathId,
 *   selectPath,
 *   clear
 * } = usePathfinderStore();
 * ```
 */

import { create } from 'zustand';
import { devtools, persist } from 'zustand/middleware';
import { PathfindingAlgorithm, PathResult } from '../hooks/usePathfinding';
import { Category } from '../types/mechanism';

// ==========================================
// Types
// ==========================================

/**
 * Selected node information
 */
export interface SelectedNode {
  nodeId: string;
  label: string;
  category?: Category;
}

/**
 * Pathfinding configuration
 */
export interface PathfindingConfig {
  algorithm: PathfindingAlgorithm;
  maxDepth: number;
  maxPaths: number;
  excludeCategories: Category[];
  onlyCategories: Category[];
}

/**
 * Selection mode for node picking
 */
export type SelectionMode = 'none' | 'from' | 'to';

/**
 * Pathfinder store state
 */
interface PathfinderState {
  // Node selection
  fromNode: SelectedNode | null;
  toNode: SelectedNode | null;

  // Path results
  paths: PathResult[];
  selectedPathId: string | null;

  // Configuration
  config: PathfindingConfig;

  // UI state
  selectionMode: SelectionMode;
  isSearching: boolean;

  // Actions
  setFromNode: (node: SelectedNode | null) => void;
  setToNode: (node: SelectedNode | null) => void;
  swapNodes: () => void;
  selectPath: (pathId: string | null) => void;
  setPaths: (paths: PathResult[]) => void;
  setConfig: (config: Partial<PathfindingConfig>) => void;
  setAlgorithm: (algorithm: PathfindingAlgorithm) => void;
  setMaxDepth: (depth: number) => void;
  setMaxPaths: (count: number) => void;
  setExcludeCategories: (categories: Category[]) => void;
  setOnlyCategories: (categories: Category[]) => void;
  setSelectionMode: (mode: SelectionMode) => void;
  setIsSearching: (isSearching: boolean) => void;
  clear: () => void;
  reset: () => void;
}

// ==========================================
// Initial State
// ==========================================

const initialConfig: PathfindingConfig = {
  algorithm: 'shortest',
  maxDepth: 5,
  maxPaths: 10,
  excludeCategories: [],
  onlyCategories: [],
};

const initialState = {
  fromNode: null,
  toNode: null,
  paths: [],
  selectedPathId: null,
  config: initialConfig,
  selectionMode: 'none' as SelectionMode,
  isSearching: false,
};

// ==========================================
// Store
// ==========================================

/**
 * Pathfinder Zustand store
 *
 * Features:
 * - Node selection management
 * - Path result storage
 * - Configuration management
 * - Selection mode tracking
 * - Persistence (optional)
 * - DevTools integration (development)
 */
export const usePathfinderStore = create<PathfinderState>()(
  devtools(
    persist(
      (set, get) => ({
        ...initialState,

        // ==========================================
        // Node Selection Actions
        // ==========================================

        /**
         * Set the "from" node for pathfinding
         */
        setFromNode: (node: SelectedNode | null) => {
          set(
            { fromNode: node, selectionMode: 'none' },
            false,
            'pathfinder/setFromNode'
          );
        },

        /**
         * Set the "to" node for pathfinding
         */
        setToNode: (node: SelectedNode | null) => {
          set(
            { toNode: node, selectionMode: 'none' },
            false,
            'pathfinder/setToNode'
          );
        },

        /**
         * Swap from and to nodes
         */
        swapNodes: () => {
          const { fromNode, toNode } = get();
          set(
            {
              fromNode: toNode,
              toNode: fromNode,
              selectedPathId: null, // Clear path selection when swapping
            },
            false,
            'pathfinder/swapNodes'
          );
        },

        // ==========================================
        // Path Selection Actions
        // ==========================================

        /**
         * Select a specific path from results
         */
        selectPath: (pathId: string | null) => {
          set({ selectedPathId: pathId }, false, 'pathfinder/selectPath');
        },

        /**
         * Set path results from API
         */
        setPaths: (paths: PathResult[]) => {
          set(
            {
              paths,
              // Auto-select first path if none selected
              selectedPathId: paths.length > 0 ? paths[0].pathId : null,
            },
            false,
            'pathfinder/setPaths'
          );
        },

        // ==========================================
        // Configuration Actions
        // ==========================================

        /**
         * Update pathfinding configuration (partial)
         */
        setConfig: (newConfig: Partial<PathfindingConfig>) => {
          set(
            state => ({
              config: { ...state.config, ...newConfig },
            }),
            false,
            'pathfinder/setConfig'
          );
        },

        /**
         * Set pathfinding algorithm
         */
        setAlgorithm: (algorithm: PathfindingAlgorithm) => {
          set(
            state => ({
              config: { ...state.config, algorithm },
            }),
            false,
            'pathfinder/setAlgorithm'
          );
        },

        /**
         * Set maximum path depth
         */
        setMaxDepth: (maxDepth: number) => {
          // Clamp between 1 and 8
          const depth = Math.max(1, Math.min(8, maxDepth));
          set(
            state => ({
              config: { ...state.config, maxDepth: depth },
            }),
            false,
            'pathfinder/setMaxDepth'
          );
        },

        /**
         * Set maximum number of paths to return
         */
        setMaxPaths: (maxPaths: number) => {
          // Clamp between 1 and 50
          const count = Math.max(1, Math.min(50, maxPaths));
          set(
            state => ({
              config: { ...state.config, maxPaths: count },
            }),
            false,
            'pathfinder/setMaxPaths'
          );
        },

        /**
         * Set categories to exclude from pathfinding
         */
        setExcludeCategories: (categories: Category[]) => {
          set(
            state => ({
              config: { ...state.config, excludeCategories: categories },
            }),
            false,
            'pathfinder/setExcludeCategories'
          );
        },

        /**
         * Set categories to include (only) in pathfinding
         */
        setOnlyCategories: (categories: Category[]) => {
          set(
            state => ({
              config: { ...state.config, onlyCategories: categories },
            }),
            false,
            'pathfinder/setOnlyCategories'
          );
        },

        // ==========================================
        // UI State Actions
        // ==========================================

        /**
         * Set selection mode (for clicking nodes on graph)
         */
        setSelectionMode: (mode: SelectionMode) => {
          set({ selectionMode: mode }, false, 'pathfinder/setSelectionMode');
        },

        /**
         * Set searching state (for loading indicators)
         */
        setIsSearching: (isSearching: boolean) => {
          set({ isSearching }, false, 'pathfinder/setIsSearching');
        },

        // ==========================================
        // Utility Actions
        // ==========================================

        /**
         * Clear path results and selection (keep nodes and config)
         */
        clear: () => {
          set(
            {
              paths: [],
              selectedPathId: null,
              isSearching: false,
            },
            false,
            'pathfinder/clear'
          );
        },

        /**
         * Reset entire store to initial state
         */
        reset: () => {
          set(
            {
              ...initialState,
              config: { ...initialConfig },
            },
            false,
            'pathfinder/reset'
          );
        },
      }),

      // Persistence configuration
      {
        name: 'pathfinder-storage', // localStorage key
        partialize: (state) => ({
          // Only persist configuration and nodes, not search results
          config: state.config,
          fromNode: state.fromNode,
          toNode: state.toNode,
        }),
      }
    ),

    // DevTools configuration
    {
      name: 'PathfinderStore',
      enabled: process.env.NODE_ENV === 'development',
    }
  )
);

// ==========================================
// Selectors (for optimized re-renders)
// ==========================================

/**
 * Select only fromNode
 */
export const selectFromNode = (state: PathfinderState) => state.fromNode;

/**
 * Select only toNode
 */
export const selectToNode = (state: PathfinderState) => state.toNode;

/**
 * Select both nodes
 */
export const selectBothNodes = (state: PathfinderState) => ({
  fromNode: state.fromNode,
  toNode: state.toNode,
});

/**
 * Select paths
 */
export const selectPaths = (state: PathfinderState) => state.paths;

/**
 * Select selected path
 */
export const selectSelectedPath = (state: PathfinderState) => {
  const { paths, selectedPathId } = state;
  return paths.find(p => p.pathId === selectedPathId) || null;
};

/**
 * Select configuration
 */
export const selectConfig = (state: PathfinderState) => state.config;

/**
 * Select algorithm
 */
export const selectAlgorithm = (state: PathfinderState) => state.config.algorithm;

/**
 * Select if ready to search (both nodes selected)
 */
export const selectIsReadyToSearch = (state: PathfinderState) =>
  state.fromNode !== null && state.toNode !== null;

/**
 * Select if searching
 */
export const selectIsSearching = (state: PathfinderState) => state.isSearching;

/**
 * Select selection mode
 */
export const selectSelectionMode = (state: PathfinderState) => state.selectionMode;

// ==========================================
// Utility Functions (outside store)
// ==========================================

/**
 * Check if a node is already selected (as from or to)
 */
export function isNodeSelected(
  nodeId: string,
  state: PathfinderState
): boolean {
  return (
    state.fromNode?.nodeId === nodeId ||
    state.toNode?.nodeId === nodeId
  );
}

/**
 * Get the role of a node in selection (from/to/none)
 */
export function getNodeSelectionRole(
  nodeId: string,
  state: PathfinderState
): 'from' | 'to' | null {
  if (state.fromNode?.nodeId === nodeId) return 'from';
  if (state.toNode?.nodeId === nodeId) return 'to';
  return null;
}

/**
 * Format node for display
 */
export function formatSelectedNode(node: SelectedNode | null): string {
  return node ? node.label : 'Select a node...';
}

/**
 * Get algorithm display name
 */
export function getAlgorithmDisplayName(
  algorithm: PathfindingAlgorithm
): string {
  const names: Record<PathfindingAlgorithm, string> = {
    shortest: 'Shortest Path',
    strongest_evidence: 'Strongest Evidence',
    all_simple: 'All Simple Paths',
  };
  return names[algorithm];
}

/**
 * Get algorithm description
 */
export function getAlgorithmDescription(
  algorithm: PathfindingAlgorithm
): string {
  const descriptions: Record<PathfindingAlgorithm, string> = {
    shortest: 'Find the path with the fewest hops between nodes',
    strongest_evidence: 'Find the path with the highest quality evidence',
    all_simple: 'Find multiple alternative paths (no loops)',
  };
  return descriptions[algorithm];
}

/**
 * Validate max depth value
 */
export function validateMaxDepth(value: number): number {
  return Math.max(1, Math.min(8, Math.floor(value)));
}

/**
 * Validate max paths value
 */
export function validateMaxPaths(value: number): number {
  return Math.max(1, Math.min(50, Math.floor(value)));
}
