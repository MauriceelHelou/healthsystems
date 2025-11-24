/**
 * useNodeImportance - Hook for fetching node importance rankings
 *
 * Fetches and manages node importance data from the backend API with
 * caching, loading states, and error handling via React Query.
 *
 * @example
 * ```tsx
 * const { data, isLoading, error } = useNodeImportance({
 *   topN: 20,
 *   categories: ['economic', 'healthcare_access'],
 *   scales: [1, 3],
 *   minConnections: 2
 * });
 * ```
 */

import { useMemo } from 'react';
import { UseQueryResult } from '@tanstack/react-query';
import { Category, NodeScale } from '../types/mechanism';
import { createGetQuery } from './utils/queryHelpers';
import { API_ENDPOINTS } from '../utils/api';

// ==========================================
// Types
// ==========================================

/**
 * Node importance data returned from API
 */
export interface NodeImportance {
  nodeId: string;
  label: string;
  category: Category;
  scale: NodeScale | null;

  // Centrality measures (0-1)
  degreeScore: number;
  betweennessScore: number;
  closenessCentrality: number;
  pageRank: number;

  // Evidence-based scoring (0-1)
  evidenceScore: number;

  // Composite importance score (0-1)
  compositeScore: number;
  rank: number;

  // Metadata
  totalConnections: number;
  avgEvidenceQuality: number;
}

/**
 * Options for node importance query
 */
export interface NodeImportanceOptions {
  /** Number of top nodes to return (default: 20, max: 100) */
  topN?: number;
  /** Filter by categories */
  categories?: Category[];
  /** Filter by scales (1,3,4,6,7) */
  scales?: NodeScale[];
  /** Minimum connection threshold */
  minConnections?: number;
  /** Enable/disable query (default: true) */
  enabled?: boolean;
}

/**
 * API response type
 */
interface NodeImportanceResponse {
  nodes: NodeImportance[];
}

// ==========================================
// Hook
// ==========================================

/**
 * Hook for fetching node importance rankings
 *
 * Features:
 * - Automatic caching (10 min stale time)
 * - Loading and error states
 * - Refetch on window focus
 * - Query invalidation support
 * - TypeScript type safety
 *
 * @param options - Query options and filters
 * @returns React Query result with node importance data
 */
export function useNodeImportance(
  options: NodeImportanceOptions = {}
): UseQueryResult<NodeImportance[], Error> {
  const {
    topN = 20,
    categories,
    scales,
    minConnections,
    enabled = true
  } = options;

  // Build query parameters
  const params: Record<string, string | number | boolean> = {
    top_n: topN,
  };

  if (categories && categories.length > 0) {
    params.categories = categories.join(',');
  }

  if (scales && scales.length > 0) {
    params.scales = scales.join(',');
  }

  if (minConnections !== undefined) {
    params.min_connections = minConnections;
  }

  const result = createGetQuery<NodeImportanceResponse>(
    API_ENDPOINTS.nodes.importance,
    params,
    {
      meta: { errorContext: 'Node importance' },
      staleTime: 10 * 60 * 1000,
      gcTime: 30 * 60 * 1000,
      refetchOnWindowFocus: false,
      refetchOnReconnect: false,
      enabled,
      retry: 2,
    }
  );

  // Transform response to return just the nodes array
  const transformedData = useMemo(() => {
    if (!result.data) return undefined;
    return result.data.nodes || (result.data as unknown as NodeImportance[]);
  }, [result.data]);

  return {
    ...result,
    data: transformedData,
  } as unknown as UseQueryResult<NodeImportance[], Error>;
}

// ==========================================
// Utility Functions
// ==========================================

/**
 * Get scale multiplier for importance calculation
 * NOTE: Scale multipliers have been removed from backend calculations (Phase 4).
 * This function is kept for backwards compatibility but is not currently used.
 */
export function getScaleMultiplier(scale: NodeScale | null): number {
  const multipliers: Record<NodeScale, number> = {
    1: 1.5, // Structural Determinants (policy)
    2: 1.2, // Built Environment & Infrastructure
    3: 1.3, // Institutional Infrastructure
    4: 1.0, // Individual/Household Conditions (baseline)
    5: 1.1, // Individual Behaviors & Psychosocial
    6: 1.1, // Intermediate Pathways
    7: 1.5, // Crisis Endpoints (critical outcomes)
  };

  return scale ? multipliers[scale] : 1.0;
}

/**
 * Format importance score for display
 */
export function formatImportanceScore(score: number): string {
  return (score * 100).toFixed(1) + '%';
}

/**
 * Get evidence quality label
 */
export function getEvidenceQualityLabel(avgQuality: number): 'A' | 'B' | 'C' {
  if (avgQuality >= 2.5) return 'A';
  if (avgQuality >= 1.5) return 'B';
  return 'C';
}

/**
 * Sort node importance by specified field
 */
export function sortNodeImportance(
  nodes: NodeImportance[],
  field: keyof NodeImportance,
  ascending: boolean = false
): NodeImportance[] {
  return [...nodes].sort((a, b) => {
    const aVal = a[field];
    const bVal = b[field];

    if (typeof aVal === 'number' && typeof bVal === 'number') {
      return ascending ? aVal - bVal : bVal - aVal;
    }

    if (typeof aVal === 'string' && typeof bVal === 'string') {
      return ascending
        ? aVal.localeCompare(bVal)
        : bVal.localeCompare(aVal);
    }

    return 0;
  });
}

/**
 * Filter nodes by minimum importance score
 */
export function filterByMinScore(
  nodes: NodeImportance[],
  minScore: number
): NodeImportance[] {
  return nodes.filter(node => node.compositeScore >= minScore);
}

/**
 * Group nodes by category
 */
export function groupByCategory(
  nodes: NodeImportance[]
): Record<Category, NodeImportance[]> {
  return nodes.reduce((groups, node) => {
    const category = node.category;
    if (!groups[category]) {
      groups[category] = [];
    }
    groups[category].push(node);
    return groups;
  }, {} as Record<Category, NodeImportance[]>);
}

/**
 * Group nodes by scale
 */
export function groupByScale(
  nodes: NodeImportance[]
): Record<string, NodeImportance[]> {
  return nodes.reduce((groups, node) => {
    const scale = node.scale?.toString() || 'unknown';
    if (!groups[scale]) {
      groups[scale] = [];
    }
    groups[scale].push(node);
    return groups;
  }, {} as Record<string, NodeImportance[]>);
}

/**
 * Calculate aggregate statistics for node importance data
 */
export function calculateImportanceStats(nodes: NodeImportance[]) {
  if (nodes.length === 0) {
    return {
      count: 0,
      avgCompositeScore: 0,
      avgConnections: 0,
      avgEvidenceQuality: 0,
      topCategory: null as Category | null,
      topScale: null as NodeScale | null,
    };
  }

  const avgCompositeScore = nodes.reduce((sum, n) => sum + n.compositeScore, 0) / nodes.length;
  const avgConnections = nodes.reduce((sum, n) => sum + n.totalConnections, 0) / nodes.length;
  const avgEvidenceQuality = nodes.reduce((sum, n) => sum + n.avgEvidenceQuality, 0) / nodes.length;

  // Most common category
  const categoryCounts = nodes.reduce((counts, node) => {
    counts[node.category] = (counts[node.category] || 0) + 1;
    return counts;
  }, {} as Record<Category, number>);
  const topCategory = Object.entries(categoryCounts)
    .sort(([, a], [, b]) => b - a)[0]?.[0] as Category | undefined;

  // Most common scale
  const scaleCounts = nodes.reduce((counts, node) => {
    if (node.scale) {
      counts[node.scale] = (counts[node.scale] || 0) + 1;
    }
    return counts;
  }, {} as Record<NodeScale, number>);
  const topScale = Object.entries(scaleCounts)
    .sort(([, a], [, b]) => b - a)[0]?.[0] as unknown as NodeScale | undefined;

  return {
    count: nodes.length,
    avgCompositeScore,
    avgConnections,
    avgEvidenceQuality,
    topCategory: topCategory || null,
    topScale: topScale || null,
  };
}
