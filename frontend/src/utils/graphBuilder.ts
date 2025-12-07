/**
 * Unified graph construction utilities
 * Consolidates graph building logic from multiple components
 */

import type {
  Mechanism,
  MechanismNode,
  MechanismEdge,
  Category,
  SystemsNetwork,
  NodeScale,
  CanonicalNode,
  HierarchyLevel,
} from '../types/mechanism';
import { calculateFilteredNeighborhood, NeighborhoodOptions } from './graphNeighborhood';

/** Strip "NEW:" prefix from node names for display */
const stripNewPrefix = (name: string): string =>
  name.replace(/^NEW:/i, '').trim();

export interface GraphBuildOptions {
  filterCategories?: Category[];
  filterScales?: NodeScale[];
  includeDisconnected?: boolean;
  calculateMetrics?: boolean;
  /** Filter by hierarchy levels (leaf, parent, cross) */
  filterHierarchyLevels?: HierarchyLevel[];
  /** Only include nodes at these depths */
  filterDepths?: number[];
  /** Set of node IDs that are currently visible (based on expansion state) */
  visibleNodeIds?: Set<string>;
  /** Set of node IDs that are currently expanded */
  expandedNodeIds?: Set<string>;
}

/**
 * Build complete graph from mechanisms list
 */
export function buildGraphFromMechanisms(
  mechanisms: Mechanism[],
  options: GraphBuildOptions = {}
): SystemsNetwork {
  const {
    filterCategories,
    filterScales,
    includeDisconnected = false,
  } = options;

  // Build nodes map
  const nodeMap = new Map<string, MechanismNode>();
  const connectionCounts = new Map<string, { incoming: number; outgoing: number }>();

  mechanisms.forEach(mech => {
    // Apply category filter
    if (filterCategories && filterCategories.length > 0 && !filterCategories.includes(mech.category)) {
      return;
    }

    // Add from_node
    if (!nodeMap.has(mech.from_node_id)) {
      nodeMap.set(mech.from_node_id, {
        id: mech.from_node_id,
        label: stripNewPrefix(mech.from_node_name),
        category: mech.category,
        scale: (mech as any).from_node_scale || inferNodeScale(mech.category, mech.from_node_name),
        stockType: 'structural', // Default
        weight: 1,
        connections: { incoming: 0, outgoing: 0 },
      });
      connectionCounts.set(mech.from_node_id, { incoming: 0, outgoing: 0 });
    }

    // Add to_node
    if (!nodeMap.has(mech.to_node_id)) {
      nodeMap.set(mech.to_node_id, {
        id: mech.to_node_id,
        label: stripNewPrefix(mech.to_node_name),
        category: mech.category,
        scale: (mech as any).to_node_scale || inferNodeScale(mech.category, mech.to_node_name),
        stockType: 'structural',
        weight: 1,
        connections: { incoming: 0, outgoing: 0 },
      });
      connectionCounts.set(mech.to_node_id, { incoming: 0, outgoing: 0 });
    }

    // Count connections
    const fromCounts = connectionCounts.get(mech.from_node_id)!;
    const toCounts = connectionCounts.get(mech.to_node_id)!;
    fromCounts.outgoing++;
    toCounts.incoming++;
  });

  // Update nodes with connection counts and weights
  nodeMap.forEach((node, id) => {
    const counts = connectionCounts.get(id)!;
    node.connections = counts;
    node.weight = Math.max(1, counts.incoming + counts.outgoing);
  });

  // Build edges
  let edges: MechanismEdge[] = mechanisms
    .filter(mech => {
      // Apply category filter
      if (filterCategories && filterCategories.length > 0 && !filterCategories.includes(mech.category)) {
        return false;
      }
      // Ensure both nodes exist
      return nodeMap.has(mech.from_node_id) && nodeMap.has(mech.to_node_id);
    })
    .map(mech => ({
      id: mech.id,
      source: mech.from_node_id,
      target: mech.to_node_id,
      direction: mech.direction,
      category: mech.category,
      evidenceQuality: mech.evidence_quality,
      strength: mech.evidence_quality === 'A' ? 3 : mech.evidence_quality === 'B' ? 2 : 1,
      studyCount: mech.n_studies || 1,
    }));

  let nodes = Array.from(nodeMap.values());

  // Apply scale filter
  if (filterScales && filterScales.length > 0) {
    nodes = nodes.filter(n => n.scale && filterScales.includes(n.scale));

    // Remove edges that reference filtered-out nodes
    const nodeIds = new Set(nodes.map(n => n.id));
    edges = edges.filter(e => {
      const sourceId = typeof e.source === 'string' ? e.source : (e.source as any).id;
      const targetId = typeof e.target === 'string' ? e.target : (e.target as any).id;
      return nodeIds.has(sourceId) && nodeIds.has(targetId);
    });
  }

  // Filter disconnected nodes if requested
  if (!includeDisconnected) {
    const connectedNodeIds = new Set<string>();
    edges.forEach(e => {
      connectedNodeIds.add(typeof e.source === 'string' ? e.source : (e.source as any).id);
      connectedNodeIds.add(typeof e.target === 'string' ? e.target : (e.target as any).id);
    });
    nodes = nodes.filter(n => connectedNodeIds.has(n.id));
  }

  return { nodes, edges };
}

/**
 * Build graph from canonical nodes and mechanisms
 *
 * This function uses canonical nodes as the source of truth for node properties,
 * with mechanisms providing only the edge/connection data.
 *
 * @param canonicalNodes - Nodes from GET /api/nodes/
 * @param mechanisms - Mechanisms from GET /api/mechanisms/
 * @param options - Build options
 */
export function buildGraphFromCanonicalNodes(
  canonicalNodes: CanonicalNode[],
  mechanisms: Mechanism[],
  options: GraphBuildOptions = {}
): SystemsNetwork {
  const {
    filterCategories,
    filterScales,
    includeDisconnected = false,
  } = options;

  // Create node lookup map from canonical nodes
  const canonicalNodeMap = new Map<string, CanonicalNode>();
  canonicalNodes.forEach(node => {
    canonicalNodeMap.set(node.id, node);
  });

  // Track which nodes are connected by mechanisms
  const connectedNodeIds = new Set<string>();
  const connectionCounts = new Map<string, { incoming: number; outgoing: number }>();

  // Initialize connection counts for all canonical nodes
  canonicalNodes.forEach(node => {
    connectionCounts.set(node.id, { incoming: 0, outgoing: 0 });
  });

  // Process mechanisms to build edges and count connections
  const edges: MechanismEdge[] = [];

  mechanisms.forEach(mech => {
    // Apply category filter to mechanism
    if (filterCategories?.length && !filterCategories.includes(mech.category)) {
      return;
    }

    // Get canonical node data (or create fallback)
    const fromCanonical = canonicalNodeMap.get(mech.from_node_id);
    const toCanonical = canonicalNodeMap.get(mech.to_node_id);

    // Apply scale filter (use canonical scale if available)
    if (filterScales?.length) {
      const fromScale = fromCanonical?.scale ?? (mech as any).from_node_scale;
      const toScale = toCanonical?.scale ?? (mech as any).to_node_scale;
      if (!filterScales.includes(fromScale) && !filterScales.includes(toScale)) {
        return;
      }
    }

    // Track connected nodes
    connectedNodeIds.add(mech.from_node_id);
    connectedNodeIds.add(mech.to_node_id);

    // Update connection counts
    const fromCounts = connectionCounts.get(mech.from_node_id) || { incoming: 0, outgoing: 0 };
    const toCounts = connectionCounts.get(mech.to_node_id) || { incoming: 0, outgoing: 0 };
    fromCounts.outgoing++;
    toCounts.incoming++;
    connectionCounts.set(mech.from_node_id, fromCounts);
    connectionCounts.set(mech.to_node_id, toCounts);

    // Create edge
    edges.push({
      id: mech.id,
      source: mech.from_node_id,
      target: mech.to_node_id,
      direction: mech.direction,
      category: mech.category,
      evidenceQuality: mech.evidence_quality,
      strength: mech.evidence_quality === 'A' ? 3 : mech.evidence_quality === 'B' ? 2 : 1,
      studyCount: mech.n_studies || 1,
    });
  });

  // Build nodes from canonical data
  const nodes: MechanismNode[] = [];
  const processedNodeIds = new Set<string>();

  canonicalNodes.forEach(canonical => {
    // Skip disconnected nodes unless requested
    if (!includeDisconnected && !connectedNodeIds.has(canonical.id)) {
      return;
    }

    // Apply scale filter to nodes
    if (filterScales?.length && !filterScales.includes(canonical.scale)) {
      return;
    }

    const counts = connectionCounts.get(canonical.id) || { incoming: 0, outgoing: 0 };
    processedNodeIds.add(canonical.id);

    nodes.push({
      id: canonical.id,
      label: stripNewPrefix(canonical.name),
      category: canonical.category as Category,
      scale: canonical.scale,
      stockType: canonical.node_type === 'crisis_endpoint' ? 'crisis' :
                 canonical.node_type === 'proxy_index' ? 'proxy' : 'structural',
      weight: Math.max(1, counts.incoming + counts.outgoing),
      connections: counts,
      // Extended properties from canonical node
      description: canonical.description,
      unit: canonical.unit,
    });
  });

  // Handle orphan nodes (in mechanisms but not in canonical node bank)
  mechanisms.forEach(mech => {
    // Check from_node
    if (!canonicalNodeMap.has(mech.from_node_id) &&
        connectedNodeIds.has(mech.from_node_id) &&
        !processedNodeIds.has(mech.from_node_id)) {
      console.warn(`Orphan node in mechanism: ${mech.from_node_id} - not in canonical node bank`);

      // Create fallback node from mechanism data
      const counts = connectionCounts.get(mech.from_node_id) || { incoming: 0, outgoing: 0 };
      processedNodeIds.add(mech.from_node_id);

      nodes.push({
        id: mech.from_node_id,
        label: stripNewPrefix(mech.from_node_name),
        category: mech.category,
        scale: (mech as any).from_node_scale || 4,
        stockType: 'structural',
        weight: Math.max(1, counts.incoming + counts.outgoing),
        connections: counts,
      });
    }

    // Check to_node
    if (!canonicalNodeMap.has(mech.to_node_id) &&
        connectedNodeIds.has(mech.to_node_id) &&
        !processedNodeIds.has(mech.to_node_id)) {
      console.warn(`Orphan node in mechanism: ${mech.to_node_id} - not in canonical node bank`);

      const counts = connectionCounts.get(mech.to_node_id) || { incoming: 0, outgoing: 0 };
      processedNodeIds.add(mech.to_node_id);

      nodes.push({
        id: mech.to_node_id,
        label: stripNewPrefix(mech.to_node_name),
        category: mech.category,
        scale: (mech as any).to_node_scale || 4,
        stockType: 'structural',
        weight: Math.max(1, counts.incoming + counts.outgoing),
        connections: counts,
      });
    }
  });

  return { nodes, edges };
}

/**
 * Filter existing graph by category
 */
export function filterGraphByCategory(
  graph: SystemsNetwork,
  categories: Category[]
): SystemsNetwork {
  if (categories.length === 0) return graph;

  const filteredEdges = graph.edges.filter(e => e.category && categories.includes(e.category));
  const connectedNodeIds = new Set<string>();

  filteredEdges.forEach(e => {
    connectedNodeIds.add(typeof e.source === 'string' ? e.source : (e.source as any).id);
    connectedNodeIds.add(typeof e.target === 'string' ? e.target : (e.target as any).id);
  });

  const filteredNodes = graph.nodes.filter(n => connectedNodeIds.has(n.id));

  return { nodes: filteredNodes, edges: filteredEdges };
}

/**
 * Filter graph by scale levels
 */
export function filterGraphByScale(
  graph: SystemsNetwork,
  scales: NodeScale[]
): SystemsNetwork {
  if (scales.length === 0) return graph;

  const filteredNodes = graph.nodes.filter(n => n.scale && scales.includes(n.scale));
  const nodeIds = new Set(filteredNodes.map(n => n.id));

  const filteredEdges = graph.edges.filter(e => {
    const sourceId = typeof e.source === 'string' ? e.source : (e.source as any).id;
    const targetId = typeof e.target === 'string' ? e.target : (e.target as any).id;
    return nodeIds.has(sourceId) && nodeIds.has(targetId);
  });

  return { nodes: filteredNodes, edges: filteredEdges };
}

/**
 * Calculate additional node metrics
 */
export function calculateNodeMetrics(graph: SystemsNetwork): SystemsNetwork {
  const nodes = graph.nodes.map(node => {
    const degree = node.connections.incoming + node.connections.outgoing;
    const centrality = graph.nodes.length > 0 ? degree / graph.nodes.length : 0;

    return {
      ...node,
      degree,
      centrality,
    } as any;
  });

  return { ...graph, nodes };
}

/**
 * Infer node scale from category and node name using pattern-based logic.
 *
 * Pattern-based overrides (applied regardless of category):
 * - Treatment/medication nodes -> Scale 5 (individual behaviors)
 * - Infrastructure/facility nodes -> Scale 3 (institutional)
 */
function inferNodeScale(category: Category, nodeName: string): NodeScale {
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
 * Get all unique categories from graph
 */
export function getGraphCategories(graph: SystemsNetwork): Category[] {
  const categories = new Set<Category>();
  graph.edges.forEach(e => {
    if (e.category) {
      categories.add(e.category);
    }
  });
  return Array.from(categories);
}

/**
 * Get all unique scales from graph
 */
export function getGraphScales(graph: SystemsNetwork): NodeScale[] {
  const scales = new Set<NodeScale>();
  graph.nodes.forEach(n => {
    if (n.scale) {
      scales.add(n.scale);
    }
  });
  return Array.from(scales).sort();
}

/**
 * Filter graph to only include nodes with at least minConnections total connections.
 * Iteratively removes nodes and recalculates until stable.
 */
export function filterByMinConnections(
  graph: SystemsNetwork,
  minConnections: number
): SystemsNetwork {
  if (minConnections <= 1) return graph;

  let nodes = [...graph.nodes];
  let edges = [...graph.edges];
  let changed = true;

  // Iteratively filter until stable (removing a node may cause others to drop below threshold)
  while (changed) {
    changed = false;

    // Recalculate connection counts based on current edges
    const connectionCounts = new Map<string, number>();
    nodes.forEach(n => connectionCounts.set(n.id, 0));

    edges.forEach(e => {
      const sourceId = typeof e.source === 'string' ? e.source : (e.source as any).id;
      const targetId = typeof e.target === 'string' ? e.target : (e.target as any).id;
      connectionCounts.set(sourceId, (connectionCounts.get(sourceId) || 0) + 1);
      connectionCounts.set(targetId, (connectionCounts.get(targetId) || 0) + 1);
    });

    // Filter nodes with fewer than minConnections
    const prevNodeCount = nodes.length;
    nodes = nodes.filter(n => (connectionCounts.get(n.id) || 0) >= minConnections);

    if (nodes.length < prevNodeCount) {
      changed = true;

      // Update edges to only include those between remaining nodes
      const nodeIds = new Set(nodes.map(n => n.id));
      edges = edges.filter(e => {
        const sourceId = typeof e.source === 'string' ? e.source : (e.source as any).id;
        const targetId = typeof e.target === 'string' ? e.target : (e.target as any).id;
        return nodeIds.has(sourceId) && nodeIds.has(targetId);
      });
    }
  }

  // Update node connection counts to reflect final state
  const finalCounts = new Map<string, { incoming: number; outgoing: number }>();
  nodes.forEach(n => finalCounts.set(n.id, { incoming: 0, outgoing: 0 }));

  edges.forEach(e => {
    const sourceId = typeof e.source === 'string' ? e.source : (e.source as any).id;
    const targetId = typeof e.target === 'string' ? e.target : (e.target as any).id;
    const sourceCounts = finalCounts.get(sourceId);
    const targetCounts = finalCounts.get(targetId);
    if (sourceCounts) sourceCounts.outgoing++;
    if (targetCounts) targetCounts.incoming++;
  });

  const updatedNodes = nodes.map(n => ({
    ...n,
    connections: finalCounts.get(n.id) || n.connections,
    weight: Math.max(1, (finalCounts.get(n.id)?.incoming || 0) + (finalCounts.get(n.id)?.outgoing || 0))
  }));

  return { nodes: updatedNodes, edges };
}

/**
 * Build alcoholism-specific subgraph
 */
export function buildAlcoholismSubgraph(mechanisms: Mechanism[]): SystemsNetwork {
  const alcoholismKeywords = [
    'alcohol', 'ald', 'liver', 'drinking', 'substance',
    'addiction', 'hepatitis', 'cirrhosis', 'binge', 'aud'
  ];

  const filtered = mechanisms.filter(m =>
    alcoholismKeywords.some(kw =>
      m.name.toLowerCase().includes(kw) ||
      m.from_node_name.toLowerCase().includes(kw) ||
      m.to_node_name.toLowerCase().includes(kw) ||
      (m.description && m.description.toLowerCase().includes(kw))
    )
  );

  return buildGraphFromMechanisms(filtered);
}

/**
 * Get statistics for a graph
 */
export interface GraphStats {
  totalNodes: number;
  totalEdges: number;
  nodesByCategory: Record<string, number>;
  edgesByCategory: Record<string, number>;
  avgDegree: number;
  maxDegree: number;
  minDegree: number;
}

export function calculateGraphStats(graph: SystemsNetwork): GraphStats {
  const nodesByCategory: Record<string, number> = {};
  const edgesByCategory: Record<string, number> = {};

  graph.nodes.forEach(node => {
    const cat = node.category || 'unknown';
    nodesByCategory[cat] = (nodesByCategory[cat] || 0) + 1;
  });

  graph.edges.forEach(edge => {
    const cat = edge.category || 'unknown';
    edgesByCategory[cat] = (edgesByCategory[cat] || 0) + 1;
  });

  const degrees = graph.nodes.map(n => n.connections.incoming + n.connections.outgoing);
  const avgDegree = degrees.length > 0 ? degrees.reduce((a, b) => a + b, 0) / degrees.length : 0;
  const maxDegree = degrees.length > 0 ? Math.max(...degrees) : 0;
  const minDegree = degrees.length > 0 ? Math.min(...degrees) : 0;

  return {
    totalNodes: graph.nodes.length,
    totalEdges: graph.edges.length,
    nodesByCategory,
    edgesByCategory,
    avgDegree,
    maxDegree,
    minDegree,
  };
}

export interface FocalNodeOptions extends NeighborhoodOptions {
  /** Include disconnected nodes in the result */
  includeDisconnected?: boolean;
}

/**
 * Build a subgraph around a focal node with filtering.
 *
 * This is the main function for focal node exploration. It:
 * 1. Calculates filtered neighborhood around focal node
 * 2. Extracts relevant nodes and edges
 * 3. Returns a pruned SystemsNetwork
 *
 * @param graph - The full graph
 * @param focalNodeId - ID of the focal node
 * @param options - Filtering and traversal options
 * @returns Pruned subgraph containing only relevant nodes/edges
 */
export function buildFocalNodeSubgraph(
  graph: SystemsNetwork,
  focalNodeId: string,
  options: FocalNodeOptions = {}
): SystemsNetwork {
  // Calculate filtered neighborhood
  const { visibleNodeIds } = calculateFilteredNeighborhood(
    focalNodeId,
    graph.nodes,
    graph.edges,
    options
  );

  // Extract relevant nodes
  const filteredNodes = graph.nodes.filter(node => visibleNodeIds.has(node.id));

  // Extract relevant edges (both endpoints must be visible)
  const filteredEdges = graph.edges.filter(edge => {
    const source = typeof edge.source === 'string' ? edge.source : (edge.source as any).id;
    const target = typeof edge.target === 'string' ? edge.target : (edge.target as any).id;
    return visibleNodeIds.has(source) && visibleNodeIds.has(target);
  });

  return {
    nodes: filteredNodes,
    edges: filteredEdges
  };
}

/**
 * Build a subgraph for a specific domain using keyword filtering.
 * This is useful for creating domain-specific views (alcoholism, obesity, etc.)
 *
 * @param mechanisms - All mechanisms
 * @param keywords - Keywords to match in mechanism/node names
 * @param options - Additional filtering options
 */
export function buildDomainSubgraph(
  mechanisms: Mechanism[],
  keywords: string[],
  options: {
    includeCategories?: Category[];
    includeScales?: NodeScale[];
    includeDisconnected?: boolean;
    minConnections?: number;
  } = {}
): SystemsNetwork {
  // Filter mechanisms by keyword
  const keywordLower = keywords.map(k => k.toLowerCase());
  const relevantMechanisms = mechanisms.filter(mech => {
    const searchText = [
      mech.id,
      mech.name,
      mech.from_node_name,
      mech.to_node_name,
      mech.description || ''
    ].join(' ').toLowerCase();

    return keywordLower.some(keyword => searchText.includes(keyword));
  });

  // Build graph from filtered mechanisms
  let graph = buildGraphFromMechanisms(relevantMechanisms, {
    filterCategories: options.includeCategories,
    filterScales: options.includeScales,
    includeDisconnected: options.includeDisconnected ?? false
  });

  // Apply minimum connections filter if specified
  if (options.minConnections && options.minConnections > 1) {
    graph = filterByMinConnections(graph, options.minConnections);
  }

  return graph;
}

// ==========================================
// HIERARCHY-SPECIFIC FUNCTIONS
// ==========================================

/**
 * Extended MechanismNode with hierarchy information
 */
export interface HierarchicalMechanismNode extends MechanismNode {
  /** Depth in hierarchy (0 = root/domain) */
  depth: number;
  /** Is this node a grouping/container node? */
  isGroupingNode: boolean;
  /** Is this node currently expanded? */
  isExpanded: boolean;
  /** Number of children (for expand indicator) */
  childCount: number;
  /** Parent node IDs (for DAG support) */
  parentIds: string[];
  /** Primary path in hierarchy */
  primaryPath?: string;
  /** All domains this node belongs to */
  domains: string[];
}

/**
 * Extended SystemsNetwork with hierarchy information
 */
export interface HierarchicalSystemsNetwork extends SystemsNetwork {
  nodes: HierarchicalMechanismNode[];
}

/**
 * Build hierarchical graph from canonical nodes with hierarchy data
 *
 * @param canonicalNodes - Nodes from API with hierarchy fields
 * @param mechanisms - Mechanisms with optional hierarchy_level
 * @param expandedNodeIds - Set of expanded node IDs
 * @param options - Build options
 */
export function buildHierarchicalGraph(
  canonicalNodes: CanonicalNode[],
  mechanisms: Mechanism[],
  expandedNodeIds: Set<string>,
  options: GraphBuildOptions = {}
): HierarchicalSystemsNetwork {
  const {
    filterCategories,
    filterScales,
    filterHierarchyLevels,
    filterDepths,
    includeDisconnected = false,
  } = options;

  // Create node lookup map from canonical nodes
  const canonicalNodeMap = new Map<string, CanonicalNode>();
  canonicalNodes.forEach(node => {
    canonicalNodeMap.set(node.id, node);
  });

  // Build parent-child relationships for visibility calculation
  const childrenByParent = new Map<string, string[]>();
  canonicalNodes.forEach(node => {
    const parentIds = node.parentIds || [];
    parentIds.forEach(parentId => {
      const children = childrenByParent.get(parentId) || [];
      children.push(node.id);
      childrenByParent.set(parentId, children);
    });
  });

  // Calculate visible node IDs based on expansion state
  const visibleNodeIds = calculateVisibleNodeIds(
    canonicalNodes,
    expandedNodeIds,
    childrenByParent
  );

  // Track connected nodes and connection counts
  const connectedNodeIds = new Set<string>();
  const connectionCounts = new Map<string, { incoming: number; outgoing: number }>();

  // Initialize connection counts
  canonicalNodes.forEach(node => {
    connectionCounts.set(node.id, { incoming: 0, outgoing: 0 });
  });

  // Process mechanisms to build edges
  const edges: MechanismEdge[] = [];

  mechanisms.forEach(mech => {
    // Apply category filter
    if (filterCategories?.length && !filterCategories.includes(mech.category)) {
      return;
    }

    // Apply hierarchy level filter
    const mechHierarchyLevel = mech.hierarchy_level || 'leaf';
    if (filterHierarchyLevels?.length && !filterHierarchyLevels.includes(mechHierarchyLevel)) {
      return;
    }

    // Get canonical node data
    const fromCanonical = canonicalNodeMap.get(mech.from_node_id);
    const toCanonical = canonicalNodeMap.get(mech.to_node_id);

    // Apply scale filter
    if (filterScales?.length) {
      const fromScale = fromCanonical?.scale ?? (mech as any).from_node_scale;
      const toScale = toCanonical?.scale ?? (mech as any).to_node_scale;
      if (!filterScales.includes(fromScale) && !filterScales.includes(toScale)) {
        return;
      }
    }

    // Apply depth filter
    if (filterDepths?.length) {
      const fromDepth = fromCanonical?.depth ?? 0;
      const toDepth = toCanonical?.depth ?? 0;
      if (!filterDepths.includes(fromDepth) && !filterDepths.includes(toDepth)) {
        return;
      }
    }

    // Skip edges where either node is not visible
    if (!visibleNodeIds.has(mech.from_node_id) || !visibleNodeIds.has(mech.to_node_id)) {
      return;
    }

    // Track connected nodes
    connectedNodeIds.add(mech.from_node_id);
    connectedNodeIds.add(mech.to_node_id);

    // Update connection counts
    const fromCounts = connectionCounts.get(mech.from_node_id) || { incoming: 0, outgoing: 0 };
    const toCounts = connectionCounts.get(mech.to_node_id) || { incoming: 0, outgoing: 0 };
    fromCounts.outgoing++;
    toCounts.incoming++;
    connectionCounts.set(mech.from_node_id, fromCounts);
    connectionCounts.set(mech.to_node_id, toCounts);

    // Create edge with hierarchy level
    edges.push({
      id: mech.id,
      source: mech.from_node_id,
      target: mech.to_node_id,
      direction: mech.direction,
      category: mech.category,
      evidenceQuality: mech.evidence_quality,
      strength: mech.evidence_quality === 'A' ? 3 : mech.evidence_quality === 'B' ? 2 : 1,
      studyCount: mech.n_studies || 1,
      hierarchyLevel: mechHierarchyLevel,
    });
  });

  // Build hierarchical nodes
  const nodes: HierarchicalMechanismNode[] = [];
  const processedNodeIds = new Set<string>();

  canonicalNodes.forEach(canonical => {
    // Skip non-visible nodes
    if (!visibleNodeIds.has(canonical.id)) {
      return;
    }

    // Skip disconnected nodes unless requested
    if (!includeDisconnected && !connectedNodeIds.has(canonical.id)) {
      return;
    }

    // Apply depth filter
    if (filterDepths?.length && !filterDepths.includes(canonical.depth ?? 0)) {
      return;
    }

    const counts = connectionCounts.get(canonical.id) || { incoming: 0, outgoing: 0 };
    const childCount = childrenByParent.get(canonical.id)?.length || 0;
    processedNodeIds.add(canonical.id);

    nodes.push({
      id: canonical.id,
      label: stripNewPrefix(canonical.name),
      category: canonical.category as Category,
      scale: canonical.scale,
      stockType: canonical.node_type === 'crisis_endpoint' ? 'crisis' :
                 canonical.node_type === 'proxy_index' ? 'proxy' : 'structural',
      weight: Math.max(1, counts.incoming + counts.outgoing),
      connections: counts,
      description: canonical.description,
      unit: canonical.unit,
      // Hierarchy fields
      depth: canonical.depth ?? 0,
      isGroupingNode: canonical.isGroupingNode ?? false,
      isExpanded: expandedNodeIds.has(canonical.id),
      childCount,
      parentIds: canonical.parentIds || [],
      primaryPath: canonical.primaryPath,
      domains: canonical.domains || [],
    });
  });

  return { nodes, edges };
}

/**
 * Calculate which node IDs should be visible based on expansion state
 *
 * Rules:
 * - Root nodes (depth=0) are always visible
 * - Children of expanded nodes are visible
 * - Recursively apply for nested expansions
 */
export function calculateVisibleNodeIds(
  nodes: CanonicalNode[],
  expandedNodeIds: Set<string>,
  childrenByParent?: Map<string, string[]>
): Set<string> {
  const visibleIds = new Set<string>();

  // Build children map if not provided
  if (!childrenByParent) {
    childrenByParent = new Map<string, string[]>();
    nodes.forEach(node => {
      const parentIds = node.parentIds || [];
      parentIds.forEach(parentId => {
        const children = childrenByParent!.get(parentId) || [];
        children.push(node.id);
        childrenByParent!.set(parentId, children);
      });
    });
  }

  // Root nodes are always visible
  nodes.forEach(node => {
    if ((node.depth ?? 0) === 0) {
      visibleIds.add(node.id);
    }
  });

  // Add children of expanded nodes recursively
  const addVisibleChildren = (parentId: string) => {
    const children = childrenByParent!.get(parentId) || [];
    children.forEach(childId => {
      visibleIds.add(childId);
      // Recursively add children if this node is also expanded
      if (expandedNodeIds.has(childId)) {
        addVisibleChildren(childId);
      }
    });
  };

  expandedNodeIds.forEach(nodeId => {
    visibleIds.add(nodeId);
    addVisibleChildren(nodeId);
  });

  return visibleIds;
}

/**
 * Filter graph by hierarchy levels (leaf, parent, cross)
 */
export function filterGraphByHierarchyLevel(
  graph: SystemsNetwork,
  levels: HierarchyLevel[]
): SystemsNetwork {
  if (levels.length === 0) return graph;

  const filteredEdges = graph.edges.filter(e =>
    e.hierarchyLevel && levels.includes(e.hierarchyLevel)
  );

  // Get nodes connected by filtered edges
  const connectedNodeIds = new Set<string>();
  filteredEdges.forEach(e => {
    connectedNodeIds.add(typeof e.source === 'string' ? e.source : (e.source as any).id);
    connectedNodeIds.add(typeof e.target === 'string' ? e.target : (e.target as any).id);
  });

  const filteredNodes = graph.nodes.filter(n => connectedNodeIds.has(n.id));

  return { nodes: filteredNodes, edges: filteredEdges };
}

/**
 * Filter graph by node depth
 */
export function filterGraphByDepth(
  graph: HierarchicalSystemsNetwork,
  depths: number[]
): HierarchicalSystemsNetwork {
  if (depths.length === 0) return graph;

  const filteredNodes = graph.nodes.filter(n => depths.includes(n.depth));
  const nodeIds = new Set(filteredNodes.map(n => n.id));

  const filteredEdges = graph.edges.filter(e => {
    const sourceId = typeof e.source === 'string' ? e.source : (e.source as any).id;
    const targetId = typeof e.target === 'string' ? e.target : (e.target as any).id;
    return nodeIds.has(sourceId) && nodeIds.has(targetId);
  });

  return { nodes: filteredNodes, edges: filteredEdges };
}

/**
 * Get child count for each node in the graph
 */
export function getNodeChildCounts(
  nodes: CanonicalNode[]
): Map<string, number> {
  const childCounts = new Map<string, number>();

  // Initialize all nodes with 0
  nodes.forEach(node => childCounts.set(node.id, 0));

  // Count children
  nodes.forEach(node => {
    const parentIds = node.parentIds || [];
    parentIds.forEach(parentId => {
      const current = childCounts.get(parentId) || 0;
      childCounts.set(parentId, current + 1);
    });
  });

  return childCounts;
}

/**
 * Get all ancestors of a node (for breadcrumb navigation)
 */
export function getNodeAncestorPath(
  nodeId: string,
  nodes: CanonicalNode[]
): CanonicalNode[] {
  const nodeMap = new Map(nodes.map(n => [n.id, n]));
  const ancestors: CanonicalNode[] = [];
  const visited = new Set<string>();

  const collectAncestors = (id: string) => {
    const node = nodeMap.get(id);
    if (!node || visited.has(id)) return;
    visited.add(id);

    // Follow primary parent (first in parentIds list)
    const primaryParentId = node.parentIds?.[0];
    if (primaryParentId) {
      collectAncestors(primaryParentId);
    }

    ancestors.push(node);
  };

  collectAncestors(nodeId);
  return ancestors;
}

/**
 * Calculate hierarchical layout positions for nodes
 *
 * Positions nodes in a grid where:
 * - X position is determined by scale (1-7)
 * - Y position is determined by depth within hierarchy
 * - Siblings are distributed vertically within their scale column
 */
export function calculateHierarchicalPositions(
  nodes: HierarchicalMechanismNode[],
  options: {
    scaleColumnWidth?: number;
    depthRowHeight?: number;
    nodeSpacing?: number;
    startX?: number;
    startY?: number;
  } = {}
): Map<string, { x: number; y: number }> {
  const {
    scaleColumnWidth = 200,
    depthRowHeight = 100,
    nodeSpacing = 50,
    startX = 0,
    startY = 0,
  } = options;

  const positions = new Map<string, { x: number; y: number }>();

  // Group nodes by scale and depth
  const nodesByScaleAndDepth = new Map<string, HierarchicalMechanismNode[]>();

  nodes.forEach(node => {
    const key = `${node.scale}-${node.depth}`;
    const group = nodesByScaleAndDepth.get(key) || [];
    group.push(node);
    nodesByScaleAndDepth.set(key, group);
  });

  // Position each group
  nodesByScaleAndDepth.forEach((groupNodes, key) => {
    const [scale, depth] = key.split('-').map(Number);

    const x = startX + (scale - 1) * scaleColumnWidth;
    const baseY = startY + depth * depthRowHeight;

    // Distribute nodes vertically within the cell
    groupNodes.forEach((node, index) => {
      const y = baseY + index * nodeSpacing;
      positions.set(node.id, { x, y });
    });
  });

  return positions;
}
