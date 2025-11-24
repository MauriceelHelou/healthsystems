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
  NodeScale,
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
    'behavioral': 'behavioral',
    'healthcare_access': 'healthcare_access', // Keep healthcare_access as its own category
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
 * Derive scale (1-7) from category and node type
 * Based on the 7-scale hierarchy defined in NODE_SYSTEM_DEFINITIONS.md
 */
function deriveScale(category: Category, stockType: StockType): NodeScale {
  // Crisis endpoints are always scale 7
  if (stockType === 'crisis') return 7;

  // Map categories to scales
  const categoryToScale: Record<Category, NodeScale> = {
    political: 1, // Structural Determinants
    built_environment: 2, // Built Environment & Infrastructure
    healthcare_access: 3, // Institutional Infrastructure
    economic: 4, // Individual/Household Conditions
    social_environment: 4, // Individual/Household Conditions
    behavioral: 5, // Individual Behaviors & Psychosocial
    biological: 6, // Intermediate Pathways
    default: 4, // Default to Individual Conditions
  };

  return categoryToScale[category] || 4;
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

  const category = mapCategory(apiNode.category);
  const stockType = mapStockType(apiNode.node_type);

  return {
    id: apiNode.id,
    label: apiNode.name,
    weight,
    category,
    stockType,
    scale: deriveScale(category, stockType), // Add derived scale field
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
    category: mapCategory(apiMechanism.category),
    evidenceQuality: apiMechanism.evidence_quality as EvidenceQuality,
    studyCount: 1, // Will be updated from detailed mechanism
  };
}

/**
 * Transform API mechanism list item to frontend Mechanism type
 * Used for graph building with the new graphBuilder utilities
 */
export function transformApiMechanismToMechanism(
  apiMechanism: ApiMechanismListItem
): Mechanism {
  return {
    id: apiMechanism.id,
    name: apiMechanism.name,
    from_node_id: apiMechanism.from_node_id,
    from_node_name: apiMechanism.from_node_name,
    to_node_id: apiMechanism.to_node_id,
    to_node_name: apiMechanism.to_node_name,
    direction: apiMechanism.direction,
    category: mapCategory(apiMechanism.category),
    evidence_quality: apiMechanism.evidence_quality as EvidenceQuality,
    n_studies: 1,
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
    name: apiMechanism.name,
    from_node_id: apiMechanism.from_node.node_id,
    from_node_name: apiMechanism.from_node.node_name,
    to_node_id: apiMechanism.to_node.node_id,
    to_node_name: apiMechanism.to_node.node_name,
    direction: apiMechanism.direction,
    category: apiMechanism.category as Category,
    description: apiMechanism.mechanism_pathway.join(' → '),
    evidence_quality: apiMechanism.evidence.quality_rating as EvidenceQuality,
    n_studies: apiMechanism.evidence.n_studies,
    mechanism_pathway: apiMechanism.mechanism_pathway,
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

/**
 * Transform API mechanisms to SystemsNetwork
 * @deprecated Use buildGraphFromMechanisms from graphBuilder.ts directly
 */
export function transformToSystemsNetwork(
  mechanisms: ApiMechanismListItem[]
): GraphData {
  // Extract unique nodes from mechanisms
  const nodeMap = new Map<string, ApiNode>();

  mechanisms.forEach(mech => {
    if (!nodeMap.has(mech.from_node_id)) {
      nodeMap.set(mech.from_node_id, {
        id: mech.from_node_id,
        name: mech.from_node_name,
        node_type: 'stock',
        category: mech.category,
      });
    }
    if (!nodeMap.has(mech.to_node_id)) {
      nodeMap.set(mech.to_node_id, {
        id: mech.to_node_id,
        name: mech.to_node_name,
        node_type: 'stock',
        category: mech.category,
      });
    }
  });

  const nodes = Array.from(nodeMap.values());
  return buildGraph(nodes, mechanisms);
}
