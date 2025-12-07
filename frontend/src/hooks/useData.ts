/**
 * React Query hooks for data fetching
 */

import { useQuery } from '@tanstack/react-query';
import { useMemo } from 'react';
import axios from 'axios';
import type {
  ApiNode,
  ApiMechanismListItem,
  ApiMechanismDetail,
  GraphData,
} from '../utils/transformers';
import {
  buildGraph as buildGraphFn,
  transformMechanismDetail as transformDetailFn,
  transformApiMechanismToMechanism,
} from '../utils/transformers';
import { buildGraphFromCanonicalNodes } from '../utils/graphBuilder';
import type { Mechanism, CanonicalNode, NodeListResponse, UseNodesOptions, SystemsNetwork } from '../types/mechanism';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8002';

// API client
const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: { 'Content-Type': 'application/json' },
});

/**
 * Fetch all mechanisms from the API
 */
async function fetchMechanisms(): Promise<ApiMechanismListItem[]> {
  const response = await api.get<ApiMechanismListItem[]>('/api/mechanisms/', {
    params: { limit: 1000 }, // Get all mechanisms
  });
  return response.data;
}

/**
 * Fetch mechanism by ID with full details
 */
async function fetchMechanismById(id: string): Promise<ApiMechanismDetail> {
  const response = await api.get<ApiMechanismDetail>(`/api/mechanisms/${id}`);
  return response.data;
}

/**
 * Fetch summary statistics
 */
interface ApiStats {
  total_mechanisms: number;
  total_nodes: number;
  by_category: Record<string, number>;
  by_direction: Record<string, number>;
  by_evidence_quality: Record<string, number>;
}

async function fetchStats(): Promise<ApiStats> {
  const response = await api.get<ApiStats>('/api/mechanisms/stats/summary');
  return response.data;
}


/**
 * Build graph data from mechanisms
 * Now uses scale information from the API instead of deriving it
 */
async function fetchGraphData(): Promise<GraphData> {
  const mechanisms = await fetchMechanisms();

  // Extract unique nodes from mechanisms with their scale values
  const nodeMap = new Map<string, ApiNode & { scale: number }>();

  mechanisms.forEach(mech => {
    if (!nodeMap.has(mech.from_node_id)) {
      nodeMap.set(mech.from_node_id, {
        id: mech.from_node_id,
        name: mech.from_node_name,
        node_type: 'stock', // Default
        category: mech.category,
        scale: mech.from_node_scale, // Use scale from API
      });
    }
    if (!nodeMap.has(mech.to_node_id)) {
      nodeMap.set(mech.to_node_id, {
        id: mech.to_node_id,
        name: mech.to_node_name,
        node_type: 'stock', // Default
        category: mech.category,
        scale: mech.to_node_scale, // Use scale from API
      });
    }
  });

  const nodes = Array.from(nodeMap.values());
  return buildGraphFn(nodes, mechanisms);
}

// React Query Hooks

/**
 * Hook to fetch all mechanisms
 */
export function useMechanisms() {
  return useQuery({
    queryKey: ['mechanisms'],
    queryFn: fetchMechanisms,
    staleTime: 5 * 60 * 1000, // 5 minutes
  });
}

/**
 * Hook to fetch mechanism details by ID
 */
export function useMechanismById(id: string | null) {
  return useQuery({
    queryKey: ['mechanism', id],
    queryFn: () => fetchMechanismById(id!),
    enabled: !!id,
    staleTime: 5 * 60 * 1000,
    select: transformDetailFn, // Transform to frontend type
  });
}

/**
 * Hook to fetch summary statistics
 */
export function useStats() {
  return useQuery({
    queryKey: ['stats'],
    queryFn: fetchStats,
    staleTime: 5 * 60 * 1000,
  });
}


/**
 * Hook to fetch graph data (nodes + edges)
 */
export function useGraphData() {
  return useQuery({
    queryKey: ['graph'],
    queryFn: fetchGraphData,
    staleTime: 5 * 60 * 1000,
  });
}

/**
 * Hook to fetch mechanisms in Mechanism format (for use with graphBuilder)
 */
export function useMechanismsForGraph() {
  return useQuery({
    queryKey: ['mechanisms-for-graph'],
    queryFn: async (): Promise<Mechanism[]> => {
      const apiMechanisms = await fetchMechanisms();
      return apiMechanisms.map(transformApiMechanismToMechanism);
    },
    staleTime: 5 * 60 * 1000,
  });
}

// ==========================================
// Canonical Node Hooks (Node Bank)
// ==========================================

/**
 * Fetch canonical nodes from the node bank
 */
async function fetchNodes(options: Omit<UseNodesOptions, 'enabled'> = {}): Promise<CanonicalNode[]> {
  const params = new URLSearchParams();

  if (options.referenced_only !== undefined) {
    params.append('referenced_only', String(options.referenced_only));
  }
  if (options.category) {
    params.append('category', options.category);
  }
  if (options.scale) {
    params.append('scale', String(options.scale));
  }
  if (options.search) {
    params.append('search', options.search);
  }

  const response = await api.get<NodeListResponse>('/api/nodes/', { params });
  return response.data.nodes;
}

/**
 * Hook to fetch canonical nodes from the node bank
 *
 * @param options - Filter and configuration options
 * @returns Query result with canonical nodes
 */
export function useNodes(options: UseNodesOptions = {}) {
  const { enabled = true, ...filterOptions } = options;

  return useQuery({
    queryKey: ['nodes', filterOptions],
    queryFn: () => fetchNodes(filterOptions),
    enabled,
    staleTime: 10 * 60 * 1000, // 10 minutes (nodes change less frequently)
  });
}

/**
 * Hook to fetch graph data with canonical nodes
 * Fetches nodes and mechanisms in parallel, merges with canonical node data
 *
 * This is the preferred way to build graphs - it uses the canonical node bank
 * as the source of truth for node properties (scale, category, description, unit)
 */
export function useGraphDataWithCanonicalNodes() {
  const nodesQuery = useNodes({ referenced_only: true });
  const mechanismsQuery = useMechanismsForGraph();

  // Combine loading/error states
  const isLoading = nodesQuery.isLoading || mechanismsQuery.isLoading;
  const error = nodesQuery.error || mechanismsQuery.error;

  // Build graph when both are ready
  const graphData = useMemo((): SystemsNetwork | null => {
    if (!nodesQuery.data || !mechanismsQuery.data) {
      return null;
    }

    return buildGraphFromCanonicalNodes(
      nodesQuery.data,
      mechanismsQuery.data
    );
  }, [nodesQuery.data, mechanismsQuery.data]);

  return {
    data: graphData,
    isLoading,
    error,
    nodesCount: nodesQuery.data?.length ?? 0,
    mechanismsCount: mechanismsQuery.data?.length ?? 0,
  };
}
