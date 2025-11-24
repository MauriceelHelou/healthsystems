/**
 * useCrisisSubgraph - Hook for exploring upstream pathways to crisis endpoints
 *
 * Performs BFS upstream traversal from selected crisis nodes to discover
 * causal pathways and policy levers.
 *
 * @example
 * ```tsx
 * const { mutate, data, isPending } = useCrisisSubgraph();
 *
 * // Trigger crisis exploration
 * mutate({
 *   crisisNodeIds: ['mortality', 'emergency_dept_visits'],
 *   maxDegrees: 5,
 *   minStrength: 2
 * });
 * ```
 */

import { UseMutationResult, useQueryClient } from '@tanstack/react-query';
import {
  CrisisSubgraphRequest,
  CrisisSubgraphResponse,
  Category,
} from '../types/mechanism';
import { createPostMutation } from './utils/queryHelpers';
import { API_ENDPOINTS } from '../utils/api';

// ==========================================
// Hook
// ==========================================

/**
 * Transform frontend request to backend format
 */
function transformRequest(request: CrisisSubgraphRequest) {
  return {
    crisisNodeIds: request.crisisNodeIds,
    maxDegrees: request.maxDegrees ?? 5,
    minStrength: request.minStrength ?? 2,
    includeCategories: request.includeCategories,
  };
}

/**
 * Hook for crisis subgraph exploration
 *
 * Uses React Query's useMutation for on-demand crisis pathway queries.
 * Results are cached by crisis node IDs combination.
 *
 * Features:
 * - BFS upstream traversal from crisis nodes
 * - Configurable maximum degrees (distance)
 * - Evidence quality filtering
 * - Category filtering
 * - Automatic identification of policy levers (scale=1 nodes)
 * - Result caching
 *
 * @returns Mutation result with crisis subgraph data
 */
export function useCrisisSubgraph(): UseMutationResult<
  CrisisSubgraphResponse,
  Error,
  CrisisSubgraphRequest
> {
  const queryClient = useQueryClient();

  const mutation = createPostMutation<CrisisSubgraphResponse, ReturnType<typeof transformRequest>>(
    API_ENDPOINTS.nodes.crisisSubgraph,
    {
      meta: {
        errorContext: 'Crisis subgraph',
      },
      onSuccess: (data, variables) => {
        // Cache with query key based on request parameters
        const queryKey = [
          'crisis-subgraph',
          (variables as any).crisisNodeIds.sort().join(','),
          (variables as any).maxDegrees,
          (variables as any).minStrength,
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
    mutate: (variables: CrisisSubgraphRequest, options?: any) => {
      mutation.mutate(transformRequest(variables), options);
    },
    mutateAsync: async (variables: CrisisSubgraphRequest, options?: any) => {
      return mutation.mutateAsync(transformRequest(variables), options);
    },
  } as UseMutationResult<CrisisSubgraphResponse, Error, CrisisSubgraphRequest>;
}

// ==========================================
// Utility Functions
// ==========================================

/**
 * Get color for degree from crisis (for visualization)
 */
export function getDegreeColor(degree: number): string {
  if (degree === 0) return '#EF4444'; // Red - crisis itself
  if (degree <= 2) return '#F97316'; // Orange - immediate causes
  if (degree <= 4) return '#EAB308'; // Yellow - intermediate
  return '#3B82F6'; // Blue - structural
}

/**
 * Get human-readable label for degree from crisis
 */
export function getDegreeLabel(degree: number): string {
  if (degree === 0) return 'Crisis Endpoint';
  if (degree === 1) return 'Immediate Cause';
  if (degree <= 2) return 'Direct Upstream';
  if (degree <= 4) return 'Intermediate Upstream';
  return 'Structural Upstream';
}

/**
 * Format crisis subgraph stats for display
 */
export function formatCrisisStats(stats: CrisisSubgraphResponse['stats']): string[] {
  return [
    `${stats.totalNodes} nodes`,
    `${stats.totalEdges} edges`,
    `${stats.policyLevers} policy levers`,
    `Avg degree: ${stats.avgDegree.toFixed(1)}`,
  ];
}

/**
 * Get top categories from breakdown
 */
export function getTopCategories(
  breakdown: Record<string, number>,
  topN: number = 3
): Array<{ category: string; count: number }> {
  return Object.entries(breakdown)
    .sort(([, a], [, b]) => b - a)
    .slice(0, topN)
    .map(([category, count]) => ({ category, count }));
}

/**
 * Filter nodes by policy lever status
 */
export function filterPolicyLevers(
  nodes: CrisisSubgraphResponse['nodes']
): CrisisSubgraphResponse['nodes'] {
  return nodes.filter(node => node.isPolicyLever);
}

/**
 * Filter nodes by degree range
 */
export function filterByDegree(
  nodes: CrisisSubgraphResponse['nodes'],
  minDegree: number,
  maxDegree: number
): CrisisSubgraphResponse['nodes'] {
  return nodes.filter(
    node => node.degreeFromCrisis >= minDegree && node.degreeFromCrisis <= maxDegree
  );
}

/**
 * Group nodes by degree from crisis
 */
export function groupByDegree(
  nodes: CrisisSubgraphResponse['nodes']
): Record<number, CrisisSubgraphResponse['nodes']> {
  return nodes.reduce((groups, node) => {
    const degree = node.degreeFromCrisis;
    if (!groups[degree]) {
      groups[degree] = [];
    }
    groups[degree].push(node);
    return groups;
  }, {} as Record<number, CrisisSubgraphResponse['nodes']>);
}

/**
 * Sort nodes by degree from crisis
 */
export function sortByDegree(
  nodes: CrisisSubgraphResponse['nodes'],
  ascending: boolean = true
): CrisisSubgraphResponse['nodes'] {
  return [...nodes].sort((a, b) => {
    return ascending
      ? a.degreeFromCrisis - b.degreeFromCrisis
      : b.degreeFromCrisis - a.degreeFromCrisis;
  });
}

/**
 * Get unique categories from nodes
 */
export function getUniqueCategories(nodes: CrisisSubgraphResponse['nodes']): Category[] {
  const categories = new Set<Category>();
  nodes.forEach(node => categories.add(node.category));
  return Array.from(categories);
}

/**
 * Validate crisis subgraph request
 */
export function validateCrisisRequest(
  request: Partial<CrisisSubgraphRequest>
): { valid: boolean; error?: string } {
  if (!request.crisisNodeIds || request.crisisNodeIds.length === 0) {
    return { valid: false, error: 'At least one crisis node must be selected' };
  }

  if (request.crisisNodeIds.length > 10) {
    return { valid: false, error: 'Maximum 10 crisis nodes allowed' };
  }

  if (request.maxDegrees && (request.maxDegrees < 1 || request.maxDegrees > 8)) {
    return { valid: false, error: 'Max degrees must be between 1 and 8' };
  }

  if (request.minStrength && (request.minStrength < 1 || request.minStrength > 3)) {
    return { valid: false, error: 'Min strength must be 1 (C), 2 (B), or 3 (A)' };
  }

  return { valid: true };
}
