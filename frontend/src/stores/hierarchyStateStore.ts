/**
 * hierarchyStateStore - Zustand store for node hierarchy state management
 *
 * Manages node expansion/collapse state for hierarchical graph visualization:
 * - Track which parent nodes are expanded vs collapsed
 * - Breadcrumb navigation path
 * - Visibility computation for child nodes
 * - Hierarchy level filtering (leaf, parent, cross)
 *
 * @example
 * ```tsx
 * const {
 *   expandedNodeIds,
 *   toggleNodeExpansion,
 *   expandNode,
 *   collapseNode,
 *   isNodeExpanded,
 *   breadcrumbPath,
 *   setBreadcrumbPath,
 * } = useHierarchyStateStore();
 * ```
 */

import { create } from 'zustand';
import { devtools, persist } from 'zustand/middleware';
import { HierarchyLevel } from '../types/mechanism';

// ==========================================
// Types
// ==========================================

/**
 * Breadcrumb item for hierarchy navigation
 */
export interface BreadcrumbItem {
  nodeId: string;
  label: string;
  depth: number;
}

/**
 * Hierarchy filter options
 */
export interface HierarchyFilter {
  /** Show mechanisms at leaf level */
  showLeaf: boolean;
  /** Show mechanisms at parent level */
  showParent: boolean;
  /** Show mechanisms that cross hierarchy levels */
  showCross: boolean;
}

/**
 * Hierarchy state for graph visualization
 */
interface HierarchyState {
  // Node expansion state
  expandedNodeIds: Set<string>;

  // Breadcrumb navigation
  breadcrumbPath: BreadcrumbItem[];

  // Hierarchy level filter
  hierarchyFilter: HierarchyFilter;

  // Visibility mode
  visibilityMode: 'show_all' | 'expand_on_demand' | 'collapsed';

  // Actions
  toggleNodeExpansion: (nodeId: string) => void;
  expandNode: (nodeId: string) => void;
  collapseNode: (nodeId: string) => void;
  expandAll: () => void;
  collapseAll: () => void;
  setExpandedNodes: (nodeIds: string[]) => void;

  // Breadcrumb actions
  setBreadcrumbPath: (path: BreadcrumbItem[]) => void;
  navigateToBreadcrumb: (index: number) => void;
  pushBreadcrumb: (item: BreadcrumbItem) => void;
  clearBreadcrumbs: () => void;

  // Filter actions
  setHierarchyFilter: (filter: Partial<HierarchyFilter>) => void;
  toggleHierarchyLevel: (level: HierarchyLevel) => void;

  // Visibility mode
  setVisibilityMode: (mode: 'show_all' | 'expand_on_demand' | 'collapsed') => void;

  // Utility
  isNodeExpanded: (nodeId: string) => boolean;
  getVisibleHierarchyLevels: () => HierarchyLevel[];
  reset: () => void;
}

// ==========================================
// Initial State
// ==========================================

const initialHierarchyFilter: HierarchyFilter = {
  showLeaf: true,
  showParent: true,
  showCross: true,
};

const initialState = {
  expandedNodeIds: new Set<string>(),
  breadcrumbPath: [],
  hierarchyFilter: initialHierarchyFilter,
  visibilityMode: 'expand_on_demand' as const,
};

// ==========================================
// Store
// ==========================================

/**
 * Hierarchy state Zustand store
 *
 * Features:
 * - Node expansion/collapse tracking
 * - Breadcrumb navigation
 * - Hierarchy level filtering
 * - Persisted across sessions
 * - DevTools integration (development)
 */
export const useHierarchyStateStore = create<HierarchyState>()(
  devtools(
    persist(
      (set, get) => ({
        ...initialState,

        // ==========================================
        // Node Expansion Actions
        // ==========================================

        /**
         * Toggle expansion state of a node
         */
        toggleNodeExpansion: (nodeId: string) => {
          set(
            (state) => {
              const newExpanded = new Set(state.expandedNodeIds);
              if (newExpanded.has(nodeId)) {
                newExpanded.delete(nodeId);
              } else {
                newExpanded.add(nodeId);
              }
              return { expandedNodeIds: newExpanded };
            },
            false,
            'hierarchy/toggleNodeExpansion'
          );
        },

        /**
         * Expand a specific node
         */
        expandNode: (nodeId: string) => {
          set(
            (state) => {
              if (state.expandedNodeIds.has(nodeId)) return state;
              const newExpanded = new Set(state.expandedNodeIds);
              newExpanded.add(nodeId);
              return { expandedNodeIds: newExpanded };
            },
            false,
            'hierarchy/expandNode'
          );
        },

        /**
         * Collapse a specific node
         */
        collapseNode: (nodeId: string) => {
          set(
            (state) => {
              if (!state.expandedNodeIds.has(nodeId)) return state;
              const newExpanded = new Set(state.expandedNodeIds);
              newExpanded.delete(nodeId);
              return { expandedNodeIds: newExpanded };
            },
            false,
            'hierarchy/collapseNode'
          );
        },

        /**
         * Expand all nodes (useful for debugging or full view)
         */
        expandAll: () => {
          // Note: This needs to be called with all grouping node IDs
          // For now, we'll just set visibility mode to show_all
          set(
            { visibilityMode: 'show_all' },
            false,
            'hierarchy/expandAll'
          );
        },

        /**
         * Collapse all nodes
         */
        collapseAll: () => {
          set(
            {
              expandedNodeIds: new Set<string>(),
              visibilityMode: 'collapsed',
            },
            false,
            'hierarchy/collapseAll'
          );
        },

        /**
         * Set specific expanded nodes
         */
        setExpandedNodes: (nodeIds: string[]) => {
          set(
            { expandedNodeIds: new Set(nodeIds) },
            false,
            'hierarchy/setExpandedNodes'
          );
        },

        // ==========================================
        // Breadcrumb Navigation Actions
        // ==========================================

        /**
         * Set the entire breadcrumb path
         */
        setBreadcrumbPath: (path: BreadcrumbItem[]) => {
          set(
            { breadcrumbPath: path },
            false,
            'hierarchy/setBreadcrumbPath'
          );
        },

        /**
         * Navigate to a specific breadcrumb (truncates path)
         */
        navigateToBreadcrumb: (index: number) => {
          set(
            (state) => {
              const newPath = state.breadcrumbPath.slice(0, index + 1);
              // Collapse nodes that are deeper than the navigation target
              const nodeIdsToKeep = new Set(newPath.map(b => b.nodeId));
              const newExpanded = new Set(
                Array.from(state.expandedNodeIds).filter(id => nodeIdsToKeep.has(id))
              );
              return {
                breadcrumbPath: newPath,
                expandedNodeIds: newExpanded,
              };
            },
            false,
            'hierarchy/navigateToBreadcrumb'
          );
        },

        /**
         * Push a new breadcrumb to the path
         */
        pushBreadcrumb: (item: BreadcrumbItem) => {
          set(
            (state) => ({
              breadcrumbPath: [...state.breadcrumbPath, item],
            }),
            false,
            'hierarchy/pushBreadcrumb'
          );
        },

        /**
         * Clear all breadcrumbs
         */
        clearBreadcrumbs: () => {
          set(
            { breadcrumbPath: [] },
            false,
            'hierarchy/clearBreadcrumbs'
          );
        },

        // ==========================================
        // Hierarchy Filter Actions
        // ==========================================

        /**
         * Update hierarchy filter
         */
        setHierarchyFilter: (filter: Partial<HierarchyFilter>) => {
          set(
            (state) => ({
              hierarchyFilter: { ...state.hierarchyFilter, ...filter },
            }),
            false,
            'hierarchy/setHierarchyFilter'
          );
        },

        /**
         * Toggle a specific hierarchy level visibility
         */
        toggleHierarchyLevel: (level: HierarchyLevel) => {
          set(
            (state) => {
              const key = `show${level.charAt(0).toUpperCase() + level.slice(1)}` as keyof HierarchyFilter;
              return {
                hierarchyFilter: {
                  ...state.hierarchyFilter,
                  [key]: !state.hierarchyFilter[key],
                },
              };
            },
            false,
            'hierarchy/toggleHierarchyLevel'
          );
        },

        // ==========================================
        // Visibility Mode Actions
        // ==========================================

        /**
         * Set visibility mode
         */
        setVisibilityMode: (mode: 'show_all' | 'expand_on_demand' | 'collapsed') => {
          set(
            { visibilityMode: mode },
            false,
            'hierarchy/setVisibilityMode'
          );
        },

        // ==========================================
        // Utility Functions
        // ==========================================

        /**
         * Check if a node is expanded
         */
        isNodeExpanded: (nodeId: string) => {
          const state = get();
          if (state.visibilityMode === 'show_all') return true;
          if (state.visibilityMode === 'collapsed') return false;
          return state.expandedNodeIds.has(nodeId);
        },

        /**
         * Get list of visible hierarchy levels based on filter
         */
        getVisibleHierarchyLevels: (): HierarchyLevel[] => {
          const { hierarchyFilter } = get();
          const levels: HierarchyLevel[] = [];
          if (hierarchyFilter.showLeaf) levels.push('leaf');
          if (hierarchyFilter.showParent) levels.push('parent');
          if (hierarchyFilter.showCross) levels.push('cross');
          return levels;
        },

        /**
         * Reset to initial state
         */
        reset: () => {
          set(
            { ...initialState },
            false,
            'hierarchy/reset'
          );
        },
      }),
      // Persist configuration
      {
        name: 'hierarchy-state-storage',
        // Custom serialization for Set
        storage: {
          getItem: (name) => {
            const str = localStorage.getItem(name);
            if (!str) return null;
            const data = JSON.parse(str);
            // Convert expandedNodeIds array back to Set
            if (data.state?.expandedNodeIds) {
              data.state.expandedNodeIds = new Set(data.state.expandedNodeIds);
            }
            return data;
          },
          setItem: (name, value) => {
            // Convert Set to array for JSON serialization
            const toStore = {
              ...value,
              state: {
                ...value.state,
                expandedNodeIds: Array.from(value.state?.expandedNodeIds || []),
              },
            };
            localStorage.setItem(name, JSON.stringify(toStore));
          },
          removeItem: (name) => localStorage.removeItem(name),
        },
        partialize: (state) => ({
          expandedNodeIds: state.expandedNodeIds,
          hierarchyFilter: state.hierarchyFilter,
          visibilityMode: state.visibilityMode,
        } as HierarchyState),
      }
    ),
    // DevTools configuration
    {
      name: 'HierarchyStateStore',
      enabled: process.env.NODE_ENV === 'development',
    }
  )
);

// ==========================================
// Selectors (for optimized re-renders)
// ==========================================

/**
 * Select expanded node IDs as array
 */
export const selectExpandedNodeIds = (state: HierarchyState) =>
  Array.from(state.expandedNodeIds);

/**
 * Select breadcrumb path
 */
export const selectBreadcrumbPath = (state: HierarchyState) =>
  state.breadcrumbPath;

/**
 * Select hierarchy filter
 */
export const selectHierarchyFilter = (state: HierarchyState) =>
  state.hierarchyFilter;

/**
 * Select visibility mode
 */
export const selectVisibilityMode = (state: HierarchyState) =>
  state.visibilityMode;

/**
 * Create selector for checking if a specific node is expanded
 */
export const createIsExpandedSelector = (nodeId: string) =>
  (state: HierarchyState) => state.isNodeExpanded(nodeId);
