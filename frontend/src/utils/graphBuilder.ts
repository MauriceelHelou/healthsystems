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
} from '../types/mechanism';
import { calculateFilteredNeighborhood, NeighborhoodOptions } from './graphNeighborhood';

export interface GraphBuildOptions {
  filterCategories?: Category[];
  filterScales?: NodeScale[];
  includeDisconnected?: boolean;
  calculateMetrics?: boolean;
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
        label: mech.from_node_name,
        category: mech.category,
        scale: inferNodeScale(mech),
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
        label: mech.to_node_name,
        category: mech.category,
        scale: inferNodeScale(mech),
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
  const edges: MechanismEdge[] = mechanisms
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
 * Infer node scale from mechanism (placeholder logic)
 */
function inferNodeScale(_mech: Mechanism): NodeScale | undefined {
  // TODO: Implement proper scale inference based on node properties
  // For now, return undefined to use existing scale if available
  return undefined;
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
  } = {}
): SystemsNetwork {
  // Filter mechanisms by keyword
  const keywordLower = keywords.map(k => k.toLowerCase());
  const relevantMechanisms = mechanisms.filter(mech => {
    const searchText = [
      mech.name,
      mech.from_node_name,
      mech.to_node_name,
      mech.description || ''
    ].join(' ').toLowerCase();

    return keywordLower.some(keyword => searchText.includes(keyword));
  });

  // Build graph from filtered mechanisms
  return buildGraphFromMechanisms(relevantMechanisms, {
    filterCategories: options.includeCategories,
    filterScales: options.includeScales,
    includeDisconnected: options.includeDisconnected ?? false
  });
}
