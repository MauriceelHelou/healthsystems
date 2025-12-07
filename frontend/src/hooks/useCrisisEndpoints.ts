/**
 * useCrisisEndpoints - Hook for fetching crisis endpoint nodes (scale=7)
 *
 * Fetches all crisis endpoint nodes from the backend API.
 * Results are cached for 10 minutes.
 *
 * @example
 * ```tsx
 * const { data, isLoading, error } = useCrisisEndpoints();
 *
 * if (isLoading) return <div>Loading...</div>;
 * if (error) return <div>Error: {error.message}</div>;
 *
 * return (
 *   <ul>
 *     {data?.map(crisis => (
 *       <li key={crisis.nodeId}>{crisis.label}</li>
 *     ))}
 *   </ul>
 * );
 * ```
 */

import { UseQueryResult } from '@tanstack/react-query';
import { CrisisEndpoint } from '../types/mechanism';
import { createGetQuery } from './utils/queryHelpers';
import { API_ENDPOINTS } from '../utils/api';

/** Strip "NEW:" prefix from node names for display */
const stripNewPrefix = (name: string): string =>
  name.replace(/^NEW:/i, '').trim();

// ==========================================
// Hook
// ==========================================

/**
 * Hook for fetching crisis endpoint nodes
 *
 * Uses React Query's useQuery for automatic caching and background refetching.
 * Data is cached for 10 minutes.
 *
 * Features:
 * - Automatic caching (10 minute stale time)
 * - Background refetching
 * - Error handling
 * - Loading states
 *
 * @returns Query result with crisis endpoints data
 */
export function useCrisisEndpoints(): UseQueryResult<CrisisEndpoint[], Error> {
  return createGetQuery<CrisisEndpoint[]>(
    API_ENDPOINTS.nodes.crisisEndpoints,
    undefined,
    {
      meta: { errorContext: 'Crisis endpoints' },
      staleTime: 10 * 60 * 1000,
      retry: 1,
      select: (data) => data.map(endpoint => ({
        ...endpoint,
        label: stripNewPrefix(endpoint.label),
      })),
    }
  );
}
