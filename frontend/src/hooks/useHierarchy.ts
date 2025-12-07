/**
 * useHierarchy - React hook for node hierarchy management
 *
 * Combines the hierarchy state store with API data fetching for:
 * - Fetching hierarchy tree from backend
 * - Getting node ancestors and descendants
 * - Computing visible nodes based on expansion state
 * - Managing expand/collapse interactions
 *
 * @example
 * ```tsx
 * const {
 *   hierarchyTree,
 *   isLoading,
 *   expandedNodeIds,
 *   toggleNodeExpansion,
 *   getVisibleNodes,
 *   getNodeAncestors,
 * } = useHierarchy();
 * ```
 */

import { useQuery } from '@tanstack/react-query';
import { useCallback } from 'react';
import axios from 'axios';
import {
  useHierarchyStateStore,
  selectExpandedNodeIds,
  selectVisibilityMode,
} from '../stores/hierarchyStateStore';
import type {
  HierarchyTreeResponse,
  NodeAncestorsResponse,
  NodeDescendantsResponse,
  CanonicalNode,
} from '../types/mechanism';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8002';

// API client
const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: { 'Content-Type': 'application/json' },
});

// ==========================================
// API Functions
// ==========================================

/**
 * Fetch hierarchy tree from API
 */
async function fetchHierarchyTree(maxDepth?: number): Promise<HierarchyTreeResponse> {
  const params = maxDepth !== undefined ? { max_depth: maxDepth } : {};
  const response = await api.get<HierarchyTreeResponse>('/api/nodes/hierarchy/tree', { params });
  return response.data;
}

/**
 * Fetch root nodes (domains)
 */
async function fetchRootNodes(): Promise<CanonicalNode[]> {
  const response = await api.get<CanonicalNode[]>('/api/nodes/hierarchy/roots');
  return response.data;
}

/**
 * Fetch ancestors for a node
 */
async function fetchNodeAncestors(nodeId: string): Promise<NodeAncestorsResponse> {
  const response = await api.get<NodeAncestorsResponse>(`/api/nodes/${nodeId}/ancestors`);
  return response.data;
}

/**
 * Fetch descendants for a node
 */
async function fetchNodeDescendants(
  nodeId: string,
  maxDepth?: number
): Promise<NodeDescendantsResponse> {
  const params = maxDepth !== undefined ? { max_depth: maxDepth } : {};
  const response = await api.get<NodeDescendantsResponse>(
    `/api/nodes/${nodeId}/descendants`,
    { params }
  );
  return response.data;
}

/**
 * Fetch children for a node (direct only)
 */
async function fetchNodeChildren(nodeId: string): Promise<CanonicalNode[]> {
  const response = await api.get<CanonicalNode[]>(`/api/nodes/${nodeId}/children`);
  return response.data;
}

// ==========================================
// Hook
// ==========================================

export interface UseHierarchyOptions {
  /** Maximum depth to fetch in tree */
  maxDepth?: number;
  /** Whether to enable hierarchy features */
  enabled?: boolean;
}

export interface UseHierarchyResult {
  // Data
  hierarchyTree: HierarchyTreeResponse | undefined;
  rootNodes: CanonicalNode[] | undefined;

  // Loading states
  isLoading: boolean;
  isLoadingTree: boolean;
  isLoadingRoots: boolean;

  // Errors
  error: Error | null;

  // State from store
  expandedNodeIds: string[];
  visibilityMode: 'show_all' | 'expand_on_demand' | 'collapsed';

  // Actions
  toggleNodeExpansion: (nodeId: string) => void;
  expandNode: (nodeId: string) => void;
  collapseNode: (nodeId: string) => void;
  expandAll: () => void;
  collapseAll: () => void;
  isNodeExpanded: (nodeId: string) => boolean;

  // Computed helpers
  getVisibleNodes: (allNodes: CanonicalNode[]) => CanonicalNode[];
  getVisibleNodeIds: (allNodes: CanonicalNode[]) => Set<string>;

  // API queries (for on-demand fetching)
  fetchAncestors: (nodeId: string) => Promise<NodeAncestorsResponse>;
  fetchDescendants: (nodeId: string, maxDepth?: number) => Promise<NodeDescendantsResponse>;
  fetchChildren: (nodeId: string) => Promise<CanonicalNode[]>;
}

/**
 * Hook for managing node hierarchy state and fetching hierarchy data
 */
export function useHierarchy(options: UseHierarchyOptions = {}): UseHierarchyResult {
  const { maxDepth, enabled = true } = options;

  // Get state and actions from store
  const {
    toggleNodeExpansion,
    expandNode,
    collapseNode,
    expandAll,
    collapseAll,
    isNodeExpanded,
  } = useHierarchyStateStore();

  const expandedNodeIds = useHierarchyStateStore(selectExpandedNodeIds);
  const visibilityMode = useHierarchyStateStore(selectVisibilityMode);

  // Fetch hierarchy tree
  const {
    data: hierarchyTree,
    isLoading: isLoadingTree,
    error: treeError,
  } = useQuery({
    queryKey: ['hierarchy-tree', maxDepth],
    queryFn: () => fetchHierarchyTree(maxDepth),
    enabled,
    staleTime: 5 * 60 * 1000, // 5 minutes
  });

  // Fetch root nodes
  const {
    data: rootNodes,
    isLoading: isLoadingRoots,
    error: rootsError,
  } = useQuery({
    queryKey: ['hierarchy-roots'],
    queryFn: fetchRootNodes,
    enabled,
    staleTime: 5 * 60 * 1000, // 5 minutes
  });

  // Compute visible nodes based on expansion state
  const getVisibleNodeIds = useCallback(
    (allNodes: CanonicalNode[]): Set<string> => {
      if (visibilityMode === 'show_all') {
        return new Set(allNodes.map((n) => n.id));
      }

      if (visibilityMode === 'collapsed') {
        // Only show root nodes when collapsed
        return new Set(allNodes.filter((n) => n.depth === 0).map((n) => n.id));
      }

      // expand_on_demand: Show nodes based on parent expansion state
      const expandedSet = new Set(expandedNodeIds);
      const visibleIds = new Set<string>();

      // Build parent-child map for efficient lookup
      const childrenByParent = new Map<string, string[]>();
      allNodes.forEach((node) => {
        if (node.parentIds) {
          node.parentIds.forEach((parentId) => {
            const children = childrenByParent.get(parentId) || [];
            children.push(node.id);
            childrenByParent.set(parentId, children);
          });
        }
      });

      // Always show root nodes
      allNodes
        .filter((n) => n.depth === 0)
        .forEach((n) => visibleIds.add(n.id));

      // Add children of expanded nodes
      const addVisibleChildren = (parentId: string) => {
        const children = childrenByParent.get(parentId) || [];
        children.forEach((childId) => {
          visibleIds.add(childId);
          // Recursively add children if this node is also expanded
          if (expandedSet.has(childId)) {
            addVisibleChildren(childId);
          }
        });
      };

      expandedNodeIds.forEach((nodeId) => {
        visibleIds.add(nodeId);
        addVisibleChildren(nodeId);
      });

      return visibleIds;
    },
    [expandedNodeIds, visibilityMode]
  );

  const getVisibleNodes = useCallback(
    (allNodes: CanonicalNode[]): CanonicalNode[] => {
      const visibleIds = getVisibleNodeIds(allNodes);
      return allNodes.filter((n) => visibleIds.has(n.id));
    },
    [getVisibleNodeIds]
  );

  // Combine loading and error states
  const isLoading = isLoadingTree || isLoadingRoots;
  const error = treeError || rootsError || null;

  return {
    // Data
    hierarchyTree,
    rootNodes,

    // Loading states
    isLoading,
    isLoadingTree,
    isLoadingRoots,

    // Errors
    error: error as Error | null,

    // State from store
    expandedNodeIds,
    visibilityMode,

    // Actions
    toggleNodeExpansion,
    expandNode,
    collapseNode,
    expandAll,
    collapseAll,
    isNodeExpanded,

    // Computed helpers
    getVisibleNodes,
    getVisibleNodeIds,

    // API queries
    fetchAncestors: fetchNodeAncestors,
    fetchDescendants: fetchNodeDescendants,
    fetchChildren: fetchNodeChildren,
  };
}

// ==========================================
// Additional Hooks
// ==========================================

/**
 * Hook for fetching ancestors of a specific node
 */
export function useNodeAncestors(nodeId: string | null) {
  return useQuery({
    queryKey: ['node-ancestors', nodeId],
    queryFn: () => (nodeId ? fetchNodeAncestors(nodeId) : Promise.resolve(null)),
    enabled: !!nodeId,
    staleTime: 5 * 60 * 1000,
  });
}

/**
 * Hook for fetching descendants of a specific node
 */
export function useNodeDescendants(nodeId: string | null, maxDepth?: number) {
  return useQuery({
    queryKey: ['node-descendants', nodeId, maxDepth],
    queryFn: () => (nodeId ? fetchNodeDescendants(nodeId, maxDepth) : Promise.resolve(null)),
    enabled: !!nodeId,
    staleTime: 5 * 60 * 1000,
  });
}

/**
 * Hook for fetching children of a specific node
 */
export function useNodeChildren(nodeId: string | null) {
  return useQuery({
    queryKey: ['node-children', nodeId],
    queryFn: () => (nodeId ? fetchNodeChildren(nodeId) : Promise.resolve([])),
    enabled: !!nodeId,
    staleTime: 5 * 60 * 1000,
  });
}

export default useHierarchy;
