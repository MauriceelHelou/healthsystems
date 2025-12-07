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

/** Strip "NEW:" prefix from node names for display */
const stripNewPrefix = (name: string): string =>
  name.replace(/^NEW:/i, '').trim();

// Backend API types
export interface ApiNode {
  id: string;
  name: string;
  node_type: string;
  unit?: string;
  measurement_method?: string;
  typical_range?: string;
  category: string;
  scale?: number;  // Scale (1-7) - now provided by API
  description?: string;
}

export interface ApiMechanismListItem {
  id: string;
  name: string;
  from_node_id: string;
  from_node_name: string;
  from_node_scale: number;  // Scale of from_node (1-7)
  to_node_id: string;
  to_node_name: string;
  to_node_scale: number;  // Scale of to_node (1-7)
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
    'healthcare_access': 'healthcare_access',
    'default': 'default',
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
 * Derive scale (1-7) from category, node type, and node name
 * Based on the 7-scale hierarchy defined in NODE_SYSTEM_DEFINITIONS.md
 *
 * Pattern-based overrides (applied regardless of category):
 * - Treatment/medication nodes -> Scale 5 (individual behaviors)
 * - Infrastructure/facility nodes -> Scale 3 (institutional)
 */
function deriveScale(category: Category, stockType: StockType, nodeName: string = ''): NodeScale {
  // Crisis endpoints are always scale 7
  if (stockType === 'crisis') return 7;

  if (nodeName) {
    const nameLower = nodeName.toLowerCase();

    // Treatment/medication keywords → Scale 5 (individual behaviors)
    // Check these FIRST regardless of category - treatments are always Scale 5
    const treatmentKeywords = [
      'gabapentin', 'naltrexone', 'disulfiram', 'acamprosate',
      'baclofen', 'topiramate', 'pharmacotherapy', 'medication',
      ' therapy', 'counseling', 'detox protocol', 'rehab',
      'recovery program', 'maud', ' mat '
    ];
    if (treatmentKeywords.some(kw => nameLower.includes(kw))) return 5;

    // "treatment" alone needs more context - check it's not infrastructure
    if (nameLower.includes('treatment')) {
      const infrastructureCheck = ['facility', 'center', 'capacity', 'availability', 'density'];
      if (!infrastructureCheck.some(kw => nameLower.includes(kw))) return 5;
    }

    // Infrastructure/facilities → Scale 3 (institutional)
    // Only for healthcare_access category
    if (category === 'healthcare_access') {
      const infrastructureKeywords = [
        'facility', 'clinic', 'center', 'density', 'capacity',
        'availability', 'provider', 'workforce', 'bed', 'unit',
        'access', 'coverage', 'insurance'
      ];
      if (infrastructureKeywords.some(kw => nameLower.includes(kw))) return 3;
      // Default healthcare_access without specific patterns → Scale 6
      return 6;
    }
  }

  // Map categories to scales
  const categoryToScale: Record<Category, NodeScale> = {
    political: 1, // Structural Determinants
    built_environment: 2, // Built Environment & Infrastructure
    economic: 3, // Institutional Infrastructure
    social_environment: 4, // Individual/Household Conditions
    behavioral: 5, // Individual Behaviors & Psychosocial
    healthcare_access: 6, // Intermediate Pathways (fallback)
    biological: 7, // Crisis Endpoints
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

  // Use explicit scale from API if available, otherwise derive it from category and name
  const scale = apiNode.scale ?? deriveScale(category, stockType, apiNode.name);

  return {
    id: apiNode.id,
    label: stripNewPrefix(apiNode.name),
    weight,
    category,
    stockType,
    scale: scale as NodeScale,  // Use explicit or derived scale
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
    from_node_name: stripNewPrefix(apiMechanism.from_node_name),
    to_node_id: apiMechanism.to_node_id,
    to_node_name: stripNewPrefix(apiMechanism.to_node_name),
    direction: apiMechanism.direction,
    category: mapCategory(apiMechanism.category),
    description: apiMechanism.name, // Use name as description for keyword matching
    evidence_quality: apiMechanism.evidence_quality as EvidenceQuality,
    n_studies: 1,
    // Pass through scale values from API for graph building
    from_node_scale: apiMechanism.from_node_scale,
    to_node_scale: apiMechanism.to_node_scale,
  } as any; // Use 'as any' since Mechanism type doesn't include scale fields
}

/**
 * Parse a citation string into structured Citation object
 * Handles multiple formats:
 * - Full: "Authors. Year. \"Title.\" Journal volume(issue): pages. URL"
 * - Simple: "Title. Description."
 * - Title only: "Some descriptive title"
 */
function parseCitationString(citationStr: string, id: string, doi?: string | null): Citation {
  // Extract URL if present
  const urlMatch = citationStr.match(/https?:\/\/[^\s]+/);
  const url = urlMatch ? urlMatch[0] : (doi ? `https://doi.org/${doi}` : undefined);

  // Remove URL from string for easier parsing
  const textWithoutUrl = urlMatch ? citationStr.replace(urlMatch[0], '').trim() : citationStr;

  // Try to extract year
  const yearMatch = textWithoutUrl.match(/\b(19|20)\d{2}\b/);
  const year = yearMatch ? parseInt(yearMatch[0]) : new Date().getFullYear();

  // Try to extract title (text between quotes, or use first sentence)
  const titleMatch = textWithoutUrl.match(/"([^"]+)"/);
  let title: string;
  let authors: string;
  let journal: string;

  if (titleMatch) {
    // Standard format with quoted title
    title = titleMatch[1];

    // Extract authors (text before year or title)
    const authorsMatch = textWithoutUrl.match(/^(.+?)\.\s*(19|20)\d{2}/);
    authors = authorsMatch ? authorsMatch[1].trim() : '';

    // Extract journal (text after title, before volume/pages or end)
    const journalMatch = textWithoutUrl.match(/"[^"]+"\s+([^.]+?)(?:\s+\d+|\.|$)/);
    journal = journalMatch ? journalMatch[1].trim() : '';
  } else {
    // Simple format without quotes - use first sentence as title
    const sentences = textWithoutUrl.split(/\.\s+/);
    title = sentences[0] || textWithoutUrl;

    // Try to find authors in remaining text
    const remainingText = sentences.slice(1).join('. ');
    authors = yearMatch && textWithoutUrl.indexOf(yearMatch[0]) > 0
      ? textWithoutUrl.substring(0, textWithoutUrl.indexOf(yearMatch[0])).replace(/\.$/, '').trim()
      : '';

    // Use remaining text as journal
    journal = remainingText.replace(yearMatch ? yearMatch[0] : '', '').trim();
  }

  // Clean up empty values
  if (!authors || authors.length < 3) authors = '';
  if (!journal || journal.length < 3) journal = '';

  // Extract DOI from URL or use provided DOI
  const doiMatch = url?.match(/doi\.org\/(.+)$/);
  const extractedDoi = doiMatch ? doiMatch[1] : (doi || '');

  return {
    id,
    authors: authors || 'Citation',
    year,
    title,
    journal: journal || 'Literature review',
    doi: extractedDoi,
    url,
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
    const parsed = parseCitationString(
      apiMechanism.evidence.primary_citation,
      `${apiMechanism.id}_primary`,
      apiMechanism.evidence.doi
    );
    citations.push(parsed);
  }

  // Add supporting citations if available
  if (apiMechanism.evidence.supporting_citations) {
    apiMechanism.evidence.supporting_citations.forEach((citation, index) => {
      const parsed = parseCitationString(
        citation,
        `${apiMechanism.id}_supporting_${index}`
      );
      citations.push(parsed);
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
    from_node_name: stripNewPrefix(apiMechanism.from_node.node_name),
    to_node_id: apiMechanism.to_node.node_id,
    to_node_name: stripNewPrefix(apiMechanism.to_node.node_name),
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
