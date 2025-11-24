/**
 * Shared utilities for building graph networks from mechanisms.
 * Consolidates duplicate logic across multiple hooks.
 */
import type { Mechanism } from '../../types/mechanism';

// Minimal node interface for graph building
export interface GraphNode {
  id: string;
  label: string;
  scale?: number;
  category?: string;
  connections?: { incoming: number; outgoing: number };
}

// Minimal edge interface
export interface GraphEdge {
  source: string;
  target: string;
  direction?: string;
  category?: string;
  evidence_quality?: string;
  mechanism_id?: string;
}

// Network structure
export interface GraphNetwork {
  nodes: GraphNode[];
  edges: GraphEdge[];
}

/**
 * Build graph network from mechanism list.
 * Consolidates nodes and creates edges.
 */
export function buildNetworkFromMechanisms(mechanisms: Mechanism[]): GraphNetwork {
  const nodeMap = new Map<string, GraphNode>();
  const edges: GraphEdge[] = [];

  mechanisms.forEach(mechanism => {
    // Add from node if not exists
    if (!nodeMap.has(mechanism.from_node_id)) {
      nodeMap.set(mechanism.from_node_id, createNodeFromMechanism(mechanism, 'from'));
    }

    // Add to node if not exists
    if (!nodeMap.has(mechanism.to_node_id)) {
      nodeMap.set(mechanism.to_node_id, createNodeFromMechanism(mechanism, 'to'));
    }

    // Create edge
    edges.push({
      source: mechanism.from_node_id,
      target: mechanism.to_node_id,
      direction: mechanism.direction,
      category: mechanism.category,
      evidence_quality: mechanism.evidence_quality || undefined,
      mechanism_id: mechanism.id,
    });
  });

  // Count connections
  const nodes = Array.from(nodeMap.values());
  const connectionsMap = countNodeConnections(nodes, mechanisms);

  // Update nodes with connection counts
  nodes.forEach(node => {
    const connections = connectionsMap.get(node.id);
    if (connections) {
      node.connections = connections;
    }
  });

  return { nodes, edges };
}

/**
 * Create node object from mechanism.
 */
function createNodeFromMechanism(
  mechanism: Mechanism,
  side: 'from' | 'to'
): GraphNode {
  const isFrom = side === 'from';

  return {
    id: isFrom ? mechanism.from_node_id : mechanism.to_node_id,
    label: isFrom ? mechanism.from_node_name : mechanism.to_node_name,
    category: mechanism.category,
    connections: { incoming: 0, outgoing: 0 },
  };
}

/**
 * Count incoming and outgoing connections for each node.
 */
export function countNodeConnections(
  nodes: GraphNode[],
  mechanisms: Mechanism[]
): Map<string, { incoming: number; outgoing: number }> {
  const connections = new Map<string, { incoming: number; outgoing: number }>();

  // Initialize
  nodes.forEach(node => {
    connections.set(node.id, { incoming: 0, outgoing: 0 });
  });

  // Count from mechanisms
  mechanisms.forEach(m => {
    const from = connections.get(m.from_node_id);
    const to = connections.get(m.to_node_id);

    if (from) from.outgoing++;
    if (to) to.incoming++;
  });

  return connections;
}

/**
 * Filter nodes by scale range.
 */
export function filterNodesByScale(
  nodes: GraphNode[],
  minScale?: number,
  maxScale?: number
): GraphNode[] {
  return nodes.filter(node => {
    if (!node.scale) return true;
    if (minScale !== undefined && node.scale < minScale) return false;
    if (maxScale !== undefined && node.scale > maxScale) return false;
    return true;
  });
}

/**
 * Filter nodes by category.
 */
export function filterNodesByCategory(
  nodes: GraphNode[],
  categories: string[]
): GraphNode[] {
  if (categories.length === 0) return nodes;

  return nodes.filter(node => node.category && categories.includes(node.category));
}

/**
 * Filter mechanisms by category.
 */
export function filterMechanismsByCategory(
  mechanisms: Mechanism[],
  categories: string[]
): Mechanism[] {
  if (categories.length === 0) return mechanisms;

  return mechanisms.filter(m => categories.includes(m.category));
}

/**
 * Get only nodes that have active connections (filter orphans).
 */
export function getConnectedNodes(
  nodes: GraphNode[],
  edges: GraphEdge[]
): GraphNode[] {
  const connectedIds = new Set<string>();

  edges.forEach(edge => {
    connectedIds.add(edge.source);
    connectedIds.add(edge.target);
  });

  return nodes.filter(node => connectedIds.has(node.id));
}
