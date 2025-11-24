/**
 * React Query hooks for data fetching
 */

import { useQuery } from '@tanstack/react-query';
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
import type { Mechanism } from '../types/mechanism';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

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
 */
async function fetchGraphData(): Promise<GraphData> {
  const mechanisms = await fetchMechanisms();

  // Extract unique nodes from mechanisms
  const nodeMap = new Map<string, ApiNode>();

  mechanisms.forEach(mech => {
    if (!nodeMap.has(mech.from_node_id)) {
      nodeMap.set(mech.from_node_id, {
        id: mech.from_node_id,
        name: mech.from_node_name,
        node_type: 'stock', // Default
        category: mech.category,
      });
    }
    if (!nodeMap.has(mech.to_node_id)) {
      nodeMap.set(mech.to_node_id, {
        id: mech.to_node_id,
        name: mech.to_node_name,
        node_type: 'stock', // Default
        category: mech.category,
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
