/**
 * Data transformation layer
 * Transforms backend API responses to frontend types
 */

import type {
  MechanismNode,
  MechanismEdge,
  Mechanism,
  Citation,
  Moderator,
  EvidenceQuality,
  Category,
  StockType,
} from '../types/mechanism';

// Backend API types
export interface ApiNode {
  id: string;
  name: string;
  node_type: string;
  unit?: string;
  measurement_method?: string;
  typical_range?: string;
  category: string;
  description?: string;
}

export interface ApiMechanismListItem {
  id: string;
  name: string;
  from_node_id: string;
  from_node_name: string;
  to_node_id: string;
  to_node_name: string;
  direction: 'positive' | 'negative';
  category: string;
  evidence_quality: 'A' | 'B' | 'C';
}

export interface ApiMechanismDetail {
  id: string;
  name: string;
  from_node: {
    node_id: string;
    node_name: string;
  };
  to_node: {
    node_id: string;
    node_name: string;
  };
  direction: 'positive' | 'negative';
  category: string;
  mechanism_pathway: string[];
  evidence: {
    quality_rating: 'A' | 'B' | 'C';
    n_studies: number;
    primary_citation: string;
    supporting_citations?: string[] | null;
    doi?: string | null;
  };
  spatial_variation: {
    varies_by_geography: boolean;
    variation_notes?: string | null;
    relevant_geographies?: string[] | null;
  };
  moderators?: Array<{
    name: string;
    direction: string;
    strength: string;
    description: string;
  }> | null;
  structural_competency: {
    root_cause_level?: string | null;
    avoids_victim_blaming?: boolean;
    equity_implications?: string | null;
  };
  description: string;
  version: string;
  last_updated: string;
  validated_by?: any | null;
}

/**
 * Map backend category to frontend Category type
 */
function mapCategory(backendCategory: string): Category {
  const categoryMap: Record<string, Category> = {
    'built_environment': 'built_environment',
    'social_environment': 'social_environment',
    'economic': 'economic',
    'political': 'political',
    'biological': 'biological',
    'healthcare_access': 'built_environment', // Map to closest category
  };
  return categoryMap[backendCategory] || 'default';
}

/**
 * Map backend node_type to frontend StockType
 */
function mapStockType(nodeType: string): StockType {
  if (nodeType === 'crisis_endpoint') return 'crisis';
  if (nodeType === 'proxy_index') return 'proxy';
  return 'structural';
}

/**
 * Transform API node to frontend MechanismNode
 */
export function transformNode(
  apiNode: ApiNode,
  allMechanisms: ApiMechanismListItem[]
): MechanismNode {
  // Calculate connections
  const outgoing = allMechanisms.filter(m => m.from_node_id === apiNode.id).length;
  const incoming = allMechanisms.filter(m => m.to_node_id === apiNode.id).length;

  // Calculate weight based on total connections
  const weight = Math.max(1, outgoing + incoming);

  return {
    id: apiNode.id,
    label: apiNode.name,
    weight,
    category: mapCategory(apiNode.category),
    stockType: mapStockType(apiNode.node_type),
    connections: {
      outgoing,
      incoming,
    },
  };
}

/**
 * Transform API mechanism to frontend MechanismEdge
 */
export function transformMechanismToEdge(
  apiMechanism: ApiMechanismListItem
): MechanismEdge {
  return {
    id: apiMechanism.id,
    source: apiMechanism.from_node_id,
    target: apiMechanism.to_node_id,
    strength: apiMechanism.evidence_quality === 'A' ? 3 : apiMechanism.evidence_quality === 'B' ? 2 : 1,
    direction: apiMechanism.direction,
    evidenceQuality: apiMechanism.evidence_quality as EvidenceQuality,
    studyCount: 1, // Will be updated from detailed mechanism
  };
}

/**
 * Transform API mechanism detail to frontend Mechanism type
 */
export function transformMechanismDetail(
  apiMechanism: ApiMechanismDetail
): Mechanism {
  // Transform citations
  const citations: Citation[] = [];
  if (apiMechanism.evidence.primary_citation) {
    citations.push({
      id: `${apiMechanism.id}_primary`,
      authors: 'Authors et al.', // Backend doesn't provide this granularity
      year: new Date(apiMechanism.last_updated).getFullYear(),
      title: apiMechanism.evidence.primary_citation,
      journal: 'Various',
      doi: apiMechanism.evidence.doi || `10.1001/${apiMechanism.id}`,
      url: apiMechanism.evidence.doi ? `https://doi.org/${apiMechanism.evidence.doi}` : undefined,
    });
  }

  // Add supporting citations if available
  if (apiMechanism.evidence.supporting_citations) {
    apiMechanism.evidence.supporting_citations.forEach((citation, index) => {
      citations.push({
        id: `${apiMechanism.id}_supporting_${index}`,
        authors: 'Authors et al.',
        year: new Date(apiMechanism.last_updated).getFullYear(),
        title: citation,
        journal: 'Various',
        doi: `10.1001/${apiMechanism.id}_${index}`,
      });
    });
  }

  // Transform moderators
  const moderators: Moderator[] = [];
  if (apiMechanism.moderators) {
    apiMechanism.moderators.forEach(mod => {
      // Map moderator name to type
      let type: 'policy' | 'geographic' | 'population' = 'population';
      if (mod.name.toLowerCase().includes('policy')) {
        type = 'policy';
      } else if (mod.name.toLowerCase().includes('geograph')) {
        type = 'geographic';
      }

      moderators.push({
        type,
        category: type,
        description: mod.description,
        effect: mod.direction,
      });
    });
  }

  return {
    id: apiMechanism.id,
    fromNode: apiMechanism.from_node.node_name,
    toNode: apiMechanism.to_node.node_name,
    direction: apiMechanism.direction,
    description: apiMechanism.mechanism_pathway.join(' → '),
    evidenceQuality: apiMechanism.evidence.quality_rating as EvidenceQuality,
    studyCount: apiMechanism.evidence.n_studies,
    citations,
    moderators,
  };
}

/**
 * Build a graph from nodes and mechanisms
 */
export interface GraphData {
  nodes: MechanismNode[];
  edges: MechanismEdge[];
}

export function buildGraph(
  apiNodes: ApiNode[],
  apiMechanisms: ApiMechanismListItem[]
): GraphData {
  // Transform nodes
  const nodes = apiNodes.map(node => transformNode(node, apiMechanisms));

  // Transform mechanisms to edges
  const edges = apiMechanisms.map(transformMechanismToEdge);

  return { nodes, edges };
}
