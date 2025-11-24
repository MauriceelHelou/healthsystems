/**
 * graphStateStore - Zustand store for graph visualization state management
 *
 * Manages shared state across graph visualization components including:
 * - Node selection and highlighting
 * - Path highlighting
 * - Zoom/scroll to node functionality
 * - Cross-view coordination (ImportantNodesView, PathfinderView, etc.)
 *
 * @example
 * ```tsx
 * const {
 *   selectedNodeId,
 *   setSelectedNode,
 *   activePaths,
 *   setActivePaths,
 *   zoomToNodeId,
 *   requestZoomToNode
 * } = useGraphStateStore();
 * ```
 */

import { create } from 'zustand';
import { devtools } from 'zustand/middleware';
import { PathHighlight } from '../types/mechanism';

// ==========================================
// Types
// ==========================================

/**
 * Graph state for coordination between views and visualization
 */
interface GraphState {
  // Node selection
  selectedNodeId: string | null;
  highlightedNodeIds: string[];

  // Path highlighting
  activePaths: PathHighlight[];
  selectedPathId: string | null;

  // Zoom/scroll control
  zoomToNodeId: string | null;
  zoomToPaths: boolean;

  // Actions
  setSelectedNode: (nodeId: string | null) => void;
  toggleNodeHighlight: (nodeId: string) => void;
  setHighlightedNodes: (nodeIds: string[]) => void;
  clearHighlights: () => void;

  setActivePaths: (paths: PathHighlight[], selectedPathId?: string | null) => void;
  clearActivePaths: () => void;
  selectPath: (pathId: string | null) => void;

  requestZoomToNode: (nodeId: string) => void;
  clearZoomRequest: () => void;
  requestZoomToPaths: () => void;
  clearZoomToPathsRequest: () => void;

  reset: () => void;
}

// ==========================================
// Initial State
// ==========================================

const initialState = {
  selectedNodeId: null,
  highlightedNodeIds: [],
  activePaths: [],
  selectedPathId: null,
  zoomToNodeId: null,
  zoomToPaths: false,
};

// ==========================================
// Store
// ==========================================

/**
 * Graph state Zustand store
 *
 * Features:
 * - Node selection management
 * - Path highlighting coordination
 * - Zoom/scroll requests
 * - Cross-view state synchronization
 * - DevTools integration (development)
 */
export const useGraphStateStore = create<GraphState>()(
  devtools(
    (set) => ({
      ...initialState,

      // ==========================================
      // Node Selection Actions
      // ==========================================

      /**
       * Set the selected node ID (for highlighting)
       */
      setSelectedNode: (nodeId: string | null) => {
        set(
          { selectedNodeId: nodeId },
          false,
          'graph/setSelectedNode'
        );
      },

      /**
       * Toggle a node's highlight state
       */
      toggleNodeHighlight: (nodeId: string) => {
        set(
          (state) => {
            const isHighlighted = state.highlightedNodeIds.includes(nodeId);
            return {
              highlightedNodeIds: isHighlighted
                ? state.highlightedNodeIds.filter(id => id !== nodeId)
                : [...state.highlightedNodeIds, nodeId],
            };
          },
          false,
          'graph/toggleNodeHighlight'
        );
      },

      /**
       * Set multiple highlighted nodes
       */
      setHighlightedNodes: (nodeIds: string[]) => {
        set(
          { highlightedNodeIds: nodeIds },
          false,
          'graph/setHighlightedNodes'
        );
      },

      /**
       * Clear all node highlights
       */
      clearHighlights: () => {
        set(
          { highlightedNodeIds: [], selectedNodeId: null },
          false,
          'graph/clearHighlights'
        );
      },

      // ==========================================
      // Path Highlighting Actions
      // ==========================================

      /**
       * Set active paths for highlighting on graph
       */
      setActivePaths: (paths: PathHighlight[], selectedPathId: string | null = null) => {
        // If selectedPathId not provided, default to first path
        const pathId = selectedPathId !== null ? selectedPathId : (paths.length > 0 ? paths[0].pathId : null);

        set(
          {
            activePaths: paths,
            selectedPathId: pathId,
          },
          false,
          'graph/setActivePaths'
        );
      },

      /**
       * Clear active paths
       */
      clearActivePaths: () => {
        set(
          {
            activePaths: [],
            selectedPathId: null,
            zoomToPaths: false,
          },
          false,
          'graph/clearActivePaths'
        );
      },

      /**
       * Select a specific path from active paths
       */
      selectPath: (pathId: string | null) => {
        set(
          { selectedPathId: pathId },
          false,
          'graph/selectPath'
        );
      },

      // ==========================================
      // Zoom/Scroll Actions
      // ==========================================

      /**
       * Request zoom/scroll to a specific node
       * The MechanismGraph component should listen to zoomToNodeId
       * and clear it after zooming
       */
      requestZoomToNode: (nodeId: string) => {
        set(
          { zoomToNodeId: nodeId },
          false,
          'graph/requestZoomToNode'
        );
      },

      /**
       * Clear zoom request (called by MechanismGraph after zooming)
       */
      clearZoomRequest: () => {
        set(
          { zoomToNodeId: null },
          false,
          'graph/clearZoomRequest'
        );
      },

      /**
       * Request zoom to fit all active paths
       */
      requestZoomToPaths: () => {
        set(
          { zoomToPaths: true },
          false,
          'graph/requestZoomToPaths'
        );
      },

      /**
       * Clear zoom to paths request (called by MechanismGraph after zooming)
       */
      clearZoomToPathsRequest: () => {
        set(
          { zoomToPaths: false },
          false,
          'graph/clearZoomToPathsRequest'
        );
      },

      // ==========================================
      // Utility Actions
      // ==========================================

      /**
       * Reset entire store to initial state
       */
      reset: () => {
        set(
          { ...initialState },
          false,
          'graph/reset'
        );
      },
    }),

    // DevTools configuration
    {
      name: 'GraphStateStore',
      enabled: process.env.NODE_ENV === 'development',
    }
  )
);

// ==========================================
// Selectors (for optimized re-renders)
// ==========================================

/**
 * Select only selected node ID
 */
export const selectSelectedNodeId = (state: GraphState) => state.selectedNodeId;

/**
 * Select highlighted node IDs
 */
export const selectHighlightedNodeIds = (state: GraphState) => state.highlightedNodeIds;

/**
 * Select active paths
 */
export const selectActivePaths = (state: GraphState) => ({
  paths: state.activePaths,
  selectedPathId: state.selectedPathId,
});

/**
 * Select zoom request
 */
export const selectZoomRequest = (state: GraphState) => ({
  zoomToNodeId: state.zoomToNodeId,
  zoomToPaths: state.zoomToPaths,
});

/**
 * Select if any paths are active
 */
export const selectHasActivePaths = (state: GraphState) => state.activePaths.length > 0;

/**
 * Select the currently selected path
 */
export const selectSelectedPath = (state: GraphState) => {
  if (!state.selectedPathId) return null;
  return state.activePaths.find(p => p.pathId === state.selectedPathId) || null;
};
