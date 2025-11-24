import { UseQueryResult } from '@tanstack/react-query';
import { createGetQuery } from './utils/queryHelpers';
import { API_ENDPOINTS } from '../utils/api';

export interface PathwaySummary {
  pathwayId: string;
  title: string;
  description: string;
  fromNodeLabel: string;
  toNodeLabel: string;
  category: string;
  pathLength: number;
  avgEvidenceQuality: number;
  overallDirection: 'positive' | 'negative' | 'mixed';
  tags: string[];
}

export interface PathwayDetail extends PathwaySummary {
  fromNodeId: string;
  toNodeId: string;
  mechanisms: PathwayMechanism[];
  evidenceGrade: 'A' | 'B' | 'C';
  curatedBy?: string;
  dateCreated?: string;
}

export interface PathwayMechanism {
  mechanismId: string;
  name: string;
  fromNode: string;
  toNode: string;
  direction: string;
  evidenceQuality: string;
}

interface PathwaysFilters {
  category?: string;
  tag?: string;
  minEvidence?: 'A' | 'B' | 'C';
  limit?: number;
}

export function usePathways(
  filters?: PathwaysFilters
): UseQueryResult<PathwaySummary[], Error> {
  const params: Record<string, string | number | boolean> = {};
  if (filters?.category) params.category = filters.category;
  if (filters?.tag) params.tag = filters.tag;
  if (filters?.minEvidence) params.min_evidence = filters.minEvidence;
  if (filters?.limit) params.limit = filters.limit;

  return createGetQuery<PathwaySummary[]>(
    API_ENDPOINTS.pathways.list,
    Object.keys(params).length > 0 ? params : undefined,
    {
      meta: { errorContext: 'Pathways' },
      staleTime: 5 * 60 * 1000,
    }
  );
}

export function usePathwayDetail(
  pathwayId: string | null
): UseQueryResult<PathwayDetail, Error> {
  return createGetQuery<PathwayDetail>(
    pathwayId ? API_ENDPOINTS.pathways.detail(pathwayId) : '',
    undefined,
    {
      enabled: !!pathwayId,
      meta: { errorContext: 'Pathway detail' },
    }
  );
}
