/**
 * usePathfinding - Hook for finding paths between nodes in the causal network
 *
 * Performs pathfinding queries to the backend API using various algorithms
 * (shortest path, strongest evidence, all simple paths).
 *
 * @example
 * ```tsx
 * const { mutate, data, isLoading } = usePathfinding();
 *
 * // Trigger pathfinding
 * mutate({
 *   fromNode: 'housing_quality',
 *   toNode: 'health_outcomes',
 *   algorithm: 'strongest_evidence',
 *   maxDepth: 5
 * });
 * ```
 */

import { UseMutationResult, useQueryClient } from '@tanstack/react-query';
import { Category, EvidenceQuality } from '../types/mechanism';
import { createPostMutation } from './utils/queryHelpers';
import { API_ENDPOINTS } from '../utils/api';

// ==========================================
// Types
// ==========================================

/**
 * Pathfinding algorithm types
 */
export type PathfindingAlgorithm = 'shortest' | 'strongest_evidence' | 'all_simple';

/**
 * Node information in a path
 */
export interface PathNode {
  nodeId: string;
  label: string;
  category: Category;
  scale?: number;
}

/**
 * Mechanism information in a path
 */
export interface PathMechanism {
  mechanismId: string;
  name: string;
  fromNode: string;
  toNode: string;
  direction: 'positive' | 'negative';
  evidenceQuality: EvidenceQuality;
  category: Category;
}

/**
 * A single path result
 */
export interface PathResult {
  pathId: string;
  nodes: string[]; // Node IDs in path order
  nodeDetails: PathNode[];
  edges: string[]; // Mechanism IDs connecting nodes
  mechanismDetails: PathMechanism[];

  // Metrics
  pathLength: number; // Number of hops (edges)
  avgEvidenceQuality: number; // 0-3 scale
  evidenceGrade: 'A' | 'B' | 'C'; // Overall grade
  overallDirection: 'positive' | 'negative' | 'mixed';
  totalWeight: number;
}

/**
 * Pathfinding request options
 */
export interface PathfindingRequest {
  /** Starting node ID */
  fromNode: string;
  /** Target node ID */
  toNode: string;
  /** Algorithm to use */
  algorithm: PathfindingAlgorithm;
  /** Maximum path depth (default: 5, max: 8) */
  maxDepth?: number;
  /** Maximum paths to return for 'all_simple' (default: 10, max: 50) */
  maxPaths?: number;
  /** Categories to exclude */
  excludeCategories?: Category[];
  /** Only include these categories */
  onlyCategories?: Category[];
}

/**
 * Pathfinding API response
 */
export interface PathfindingResponse {
  fromNode: string;
  toNode: string;
  algorithm: PathfindingAlgorithm;
  pathsFound: number;
  paths: PathResult[];
}

// ==========================================
// Hook
// ==========================================

/**
 * Transform frontend request to backend format
 */
function transformRequest(request: PathfindingRequest) {
  return {
    from_node: request.fromNode,
    to_node: request.toNode,
    algorithm: request.algorithm,
    max_depth: request.maxDepth || 5,
    max_paths: request.maxPaths || 10,
    exclude_categories: request.excludeCategories,
    only_categories: request.onlyCategories,
  };
}

/**
 * Hook for pathfinding between nodes
 *
 * Uses React Query's useMutation for on-demand pathfinding queries.
 * Results are cached by source-target-algorithm combination.
 *
 * Features:
 * - Three pathfinding algorithms
 * - Automatic error handling
 * - Loading states
 * - Result caching
 * - Query invalidation
 *
 * @returns Mutation result with pathfinding data
 */
export function usePathfinding(): UseMutationResult<
  PathfindingResponse,
  Error,
  PathfindingRequest
> {
  const queryClient = useQueryClient();

  const mutation = createPostMutation<PathfindingResponse, ReturnType<typeof transformRequest>>(
    API_ENDPOINTS.nodes.pathfinding,
    {
      meta: {
        errorContext: 'Pathfinding',
      },
      onSuccess: (data, variables) => {
        // Cache with query key based on request parameters
        const queryKey = [
          'pathfinding',
          (variables as any).from_node,
          (variables as any).to_node,
          (variables as any).algorithm,
          (variables as any).max_depth,
        ];

        queryClient.setQueryData(queryKey, data);
      },
      retry: 1,
      retryDelay: 1000,
    }
  );

  // Wrap to transform request before sending
  return {
    ...mutation,
    mutate: (variables: PathfindingRequest, options?: any) => {
      mutation.mutate(transformRequest(variables), options);
    },
    mutateAsync: async (variables: PathfindingRequest, options?: any) => {
      return mutation.mutateAsync(transformRequest(variables), options);
    },
  } as UseMutationResult<PathfindingResponse, Error, PathfindingRequest>;
}

// ==========================================
// Utility Functions
// ==========================================

/**
 * Check if a path exists between two nodes in a list of paths
 */
export function hasPath(
  paths: PathResult[],
  fromNode: string,
  toNode: string
): boolean {
  return paths.some(
    path => path.nodes[0] === fromNode && path.nodes[path.nodes.length - 1] === toNode
  );
}

/**
 * Get the shortest path by number of hops
 */
export function getShortestPath(paths: PathResult[]): PathResult | null {
  if (paths.length === 0) return null;

  return paths.reduce((shortest, current) =>
    current.pathLength < shortest.pathLength ? current : shortest
  );
}

/**
 * Get the highest quality path by evidence
 */
export function getHighestQualityPath(paths: PathResult[]): PathResult | null {
  if (paths.length === 0) return null;

  return paths.reduce((best, current) =>
    current.avgEvidenceQuality > best.avgEvidenceQuality ? current : best
  );
}

/**
 * Filter paths by maximum length
 */
export function filterByMaxLength(
  paths: PathResult[],
  maxLength: number
): PathResult[] {
  return paths.filter(path => path.pathLength <= maxLength);
}

/**
 * Filter paths by minimum evidence quality
 */
export function filterByMinQuality(
  paths: PathResult[],
  minQuality: number
): PathResult[] {
  return paths.filter(path => path.avgEvidenceQuality >= minQuality);
}

/**
 * Filter paths by direction (positive/negative/mixed)
 */
export function filterByDirection(
  paths: PathResult[],
  direction: 'positive' | 'negative' | 'mixed'
): PathResult[] {
  return paths.filter(path => path.overallDirection === direction);
}

/**
 * Sort paths by a specified field
 */
export function sortPaths(
  paths: PathResult[],
  field: 'length' | 'quality' | 'weight',
  ascending: boolean = true
): PathResult[] {
  return [...paths].sort((a, b) => {
    let aVal: number, bVal: number;

    switch (field) {
      case 'length':
        aVal = a.pathLength;
        bVal = b.pathLength;
        break;
      case 'quality':
        aVal = a.avgEvidenceQuality;
        bVal = b.avgEvidenceQuality;
        break;
      case 'weight':
        aVal = a.totalWeight;
        bVal = b.totalWeight;
        break;
      default:
        return 0;
    }

    return ascending ? aVal - bVal : bVal - aVal;
  });
}

/**
 * Group paths by length
 */
export function groupByLength(
  paths: PathResult[]
): Record<number, PathResult[]> {
  return paths.reduce((groups, path) => {
    const length = path.pathLength;
    if (!groups[length]) {
      groups[length] = [];
    }
    groups[length].push(path);
    return groups;
  }, {} as Record<number, PathResult[]>);
}

/**
 * Get all unique nodes across all paths
 */
export function getUniqueNodes(paths: PathResult[]): Set<string> {
  const nodes = new Set<string>();

  paths.forEach(path => {
    path.nodes.forEach(nodeId => nodes.add(nodeId));
  });

  return nodes;
}

/**
 * Get all unique mechanisms across all paths
 */
export function getUniqueMechanisms(paths: PathResult[]): Set<string> {
  const mechanisms = new Set<string>();

  paths.forEach(path => {
    path.edges.forEach(mechId => mechanisms.add(mechId));
  });

  return mechanisms;
}

/**
 * Calculate statistics for a set of paths
 */
export function calculatePathStats(paths: PathResult[]) {
  if (paths.length === 0) {
    return {
      count: 0,
      avgLength: 0,
      avgQuality: 0,
      avgWeight: 0,
      shortestLength: 0,
      longestLength: 0,
      positiveCount: 0,
      negativeCount: 0,
      mixedCount: 0,
    };
  }

  const lengths = paths.map(p => p.pathLength);
  const qualities = paths.map(p => p.avgEvidenceQuality);
  const weights = paths.map(p => p.totalWeight);

  const avgLength = lengths.reduce((sum, l) => sum + l, 0) / lengths.length;
  const avgQuality = qualities.reduce((sum, q) => sum + q, 0) / qualities.length;
  const avgWeight = weights.reduce((sum, w) => sum + w, 0) / weights.length;

  const shortestLength = Math.min(...lengths);
  const longestLength = Math.max(...lengths);

  const directionCounts = paths.reduce(
    (counts, path) => {
      counts[path.overallDirection]++;
      return counts;
    },
    { positive: 0, negative: 0, mixed: 0 }
  );

  return {
    count: paths.length,
    avgLength,
    avgQuality,
    avgWeight,
    shortestLength,
    longestLength,
    positiveCount: directionCounts.positive,
    negativeCount: directionCounts.negative,
    mixedCount: directionCounts.mixed,
  };
}

/**
 * Format path length for display
 */
export function formatPathLength(length: number): string {
  return `${length} ${length === 1 ? 'hop' : 'hops'}`;
}

/**
 * Format evidence quality for display
 */
export function formatEvidenceQuality(quality: number): string {
  return quality.toFixed(2);
}

/**
 * Get color for evidence grade
 */
export function getEvidenceGradeColor(grade: 'A' | 'B' | 'C'): string {
  const colors = {
    A: '#10B981', // Green
    B: '#F59E0B', // Amber
    C: '#EF4444', // Red
  };
  return colors[grade];
}

/**
 * Get color for direction
 */
export function getDirectionColor(
  direction: 'positive' | 'negative' | 'mixed'
): string {
  const colors = {
    positive: '#10B981', // Green
    negative: '#EF4444', // Red
    mixed: '#6B7280', // Gray
  };
  return colors[direction];
}

/**
 * Get arrow symbol for direction
 */
export function getDirectionSymbol(
  direction: 'positive' | 'negative' | 'mixed'
): string {
  const symbols = {
    positive: '↑',
    negative: '↓',
    mixed: '↕',
  };
  return symbols[direction];
}

/**
 * Check if two paths are equivalent (same nodes)
 */
export function arePathsEquivalent(path1: PathResult, path2: PathResult): boolean {
  if (path1.nodes.length !== path2.nodes.length) return false;

  return path1.nodes.every((nodeId, index) => nodeId === path2.nodes[index]);
}

/**
 * Deduplicate paths (remove equivalent paths)
 */
export function deduplicatePaths(paths: PathResult[]): PathResult[] {
  const uniquePaths: PathResult[] = [];

  paths.forEach(path => {
    const isDuplicate = uniquePaths.some(uniquePath =>
      arePathsEquivalent(path, uniquePath)
    );

    if (!isDuplicate) {
      uniquePaths.push(path);
    }
  });

  return uniquePaths;
}

/**
 * Find paths that contain a specific node
 */
export function findPathsContainingNode(
  paths: PathResult[],
  nodeId: string
): PathResult[] {
  return paths.filter(path => path.nodes.includes(nodeId));
}

/**
 * Find paths that contain a specific mechanism
 */
export function findPathsContainingMechanism(
  paths: PathResult[],
  mechanismId: string
): PathResult[] {
  return paths.filter(path => path.edges.includes(mechanismId));
}

/**
 * Generate a human-readable path description
 */
export function generatePathDescription(path: PathResult): string {
  const nodeLabels = path.nodeDetails.map(n => n.label);

  if (nodeLabels.length === 0) return 'Empty path';
  if (nodeLabels.length === 1) return nodeLabels[0];
  if (nodeLabels.length === 2) return `${nodeLabels[0]} → ${nodeLabels[1]}`;

  return `${nodeLabels[0]} → ... → ${nodeLabels[nodeLabels.length - 1]} (${path.pathLength} hops)`;
}
