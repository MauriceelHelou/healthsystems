/**
 * Custom hook for fetching and filtering the alcoholism system subgraph
 *
 * Wraps the base useMechanismsForGraph hook and applies alcoholism-specific filtering
 * to extract only mechanisms and nodes related to alcohol use and outcomes.
 */

import { useMemo } from 'react';
import { useMechanismsForGraph } from './useData';
import {
  buildAlcoholismSubgraph,
  calculateGraphStats,
} from '../utils/graphBuilder';
import type { SystemsNetwork } from '../types/mechanism';

export interface AlcoholismSystemData {
  network: SystemsNetwork;
  stats: {
    totalNodes: number;
    totalMechanisms: number;
    mechanismsByCategory: Record<string, number>;
    nodesByType: Record<string, number>;
    coreNodes: number;
    riskFactors: number;
    outcomes: number;
  };
  isLoading: boolean;
  error: Error | null;
}

/**
 * Hook that provides the filtered alcoholism system network and statistics
 *
 * @returns Alcoholism system data with loading and error states
 *
 * @example
 * ```tsx
 * function AlcoholismDiagram() {
 *   const { network, stats, isLoading, error } = useAlcoholismSystem();
 *
 *   if (isLoading) return <LoadingSpinner />;
 *   if (error) return <ErrorMessage error={error} />;
 *
 *   return (
 *     <div>
 *       <h2>Alcoholism System ({stats.totalMechanisms} mechanisms)</h2>
 *       <MechanismGraph data={network} />
 *     </div>
 *   );
 * }
 * ```
 */
export function useAlcoholismSystem(): AlcoholismSystemData {
  // Fetch all mechanisms
  const { data: mechanisms, isLoading, error } = useMechanismsForGraph();

  // Memoize filtered network to avoid recomputation on every render
  const alcoholismNetwork = useMemo(() => {
    if (!mechanisms || mechanisms.length === 0) {
      return { nodes: [], edges: [] };
    }

    return buildAlcoholismSubgraph(mechanisms);
  }, [mechanisms]);

  // Memoize statistics calculation
  const stats = useMemo(() => {
    if (!mechanisms || mechanisms.length === 0) {
      return {
        totalNodes: 0,
        totalMechanisms: 0,
        mechanismsByCategory: {},
        nodesByType: {},
        coreNodes: 0,
        riskFactors: 0,
        outcomes: 0,
      };
    }

    const graphStats = calculateGraphStats(alcoholismNetwork);

    // Map to expected format
    return {
      totalNodes: graphStats.totalNodes,
      totalMechanisms: graphStats.totalEdges,
      mechanismsByCategory: graphStats.edgesByCategory,
      nodesByType: graphStats.nodesByCategory,
      // Note: coreNodes, riskFactors, and outcomes counts can be added later if needed
      // by extending graphBuilder with alcoholism-specific node categorization
      coreNodes: 0,
      riskFactors: 0,
      outcomes: 0,
    };
  }, [mechanisms, alcoholismNetwork]);

  return {
    network: alcoholismNetwork,
    stats,
    isLoading,
    error,
  };
}
