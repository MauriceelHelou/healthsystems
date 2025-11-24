import type { MechanismNode, MechanismEdge, Category, NodeScale } from '../types';

export interface NeighborhoodResult {
  visibleNodeIds: Set<string>;
  dimmedNodeIds: Set<string>;
}

export type TraversalDirection = 'upstream' | 'downstream' | 'both';

export interface NeighborhoodOptions {
  direction?: TraversalDirection;
  includeCategories?: Category[];
  includeScales?: NodeScale[];
  maxHopsUpstream?: number | null;
  maxHopsDownstream?: number | null;
  includeSiblings?: boolean;
}

export function calculateFilteredNeighborhood(
  focalNodeId: string,
  nodes: MechanismNode[],
  edges: MechanismEdge[],
  options: NeighborhoodOptions = {}
): NeighborhoodResult {
  const {
    direction = 'both',
    includeCategories,
    includeScales,
    maxHopsUpstream,
    maxHopsDownstream,
    includeSiblings = false
  } = options;

  const { forwardEdges, backwardEdges } = buildAdjacencyLists(edges, includeCategories);
  const nodeMap = new Map(nodes.map(n => [n.id, n]));
  const visibleNodeIds = new Set<string>();
  visibleNodeIds.add(focalNodeId);

  if (direction === 'upstream' || direction === 'both') {
    const upstreamNodes = bfsUpstream(
      focalNodeId,
      backwardEdges,
      maxHopsUpstream ?? Infinity
    );
    upstreamNodes.forEach(nodeId => {
      if (passesScaleFilter(nodeId, nodeMap, includeScales)) {
        visibleNodeIds.add(nodeId);
      }
    });
  }

  if (direction === 'downstream' || direction === 'both') {
    const downstreamNodes = bfsDownstream(
      focalNodeId,
      forwardEdges,
      maxHopsDownstream ?? Infinity
    );
    downstreamNodes.forEach(nodeId => {
      if (passesScaleFilter(nodeId, nodeMap, includeScales)) {
        visibleNodeIds.add(nodeId);
      }
    });
  }

  if (includeSiblings) {
    const siblings = findSiblings(focalNodeId, forwardEdges, backwardEdges);
    siblings.forEach(nodeId => {
      if (passesScaleFilter(nodeId, nodeMap, includeScales)) {
        visibleNodeIds.add(nodeId);
      }
    });
  }

  const dimmedNodeIds = new Set<string>();
  nodes.forEach(node => {
    if (!visibleNodeIds.has(node.id)) {
      dimmedNodeIds.add(node.id);
    }
  });

  return { visibleNodeIds, dimmedNodeIds };
}

function buildAdjacencyLists(
  edges: MechanismEdge[],
  includeCategories?: Category[]
): {
  forwardEdges: Map<string, string[]>;
  backwardEdges: Map<string, string[]>;
} {
  const forwardEdges = new Map<string, string[]>();
  const backwardEdges = new Map<string, string[]>();

  for (const edge of edges) {
    if (includeCategories && includeCategories.length > 0 && edge.category && !includeCategories.includes(edge.category)) {
      continue;
    }

    const source = typeof edge.source === 'string' ? edge.source : (edge.source as any).id;
    const target = typeof edge.target === 'string' ? edge.target : (edge.target as any).id;

    if (!forwardEdges.has(source)) forwardEdges.set(source, []);
    forwardEdges.get(source)!.push(target);

    if (!backwardEdges.has(target)) backwardEdges.set(target, []);
    backwardEdges.get(target)!.push(source);
  }

  return { forwardEdges, backwardEdges };
}

function bfsUpstream(
  startNodeId: string,
  backwardEdges: Map<string, string[]>,
  maxHops: number
): Set<string> {
  const visited = new Set<string>();
  const queue: Array<{ nodeId: string; hops: number }> = [{ nodeId: startNodeId, hops: 0 }];

  while (queue.length > 0) {
    const { nodeId, hops } = queue.shift()!;

    if (visited.has(nodeId)) continue;
    visited.add(nodeId);

    if (hops >= maxHops) continue;

    const predecessors = backwardEdges.get(nodeId) || [];
    for (const pred of predecessors) {
      if (!visited.has(pred)) {
        queue.push({ nodeId: pred, hops: hops + 1 });
      }
    }
  }

  visited.delete(startNodeId);
  return visited;
}

function bfsDownstream(
  startNodeId: string,
  forwardEdges: Map<string, string[]>,
  maxHops: number
): Set<string> {
  const visited = new Set<string>();
  const queue: Array<{ nodeId: string; hops: number }> = [{ nodeId: startNodeId, hops: 0 }];

  while (queue.length > 0) {
    const { nodeId, hops } = queue.shift()!;

    if (visited.has(nodeId)) continue;
    visited.add(nodeId);

    if (hops >= maxHops) continue;

    const successors = forwardEdges.get(nodeId) || [];
    for (const succ of successors) {
      if (!visited.has(succ)) {
        queue.push({ nodeId: succ, hops: hops + 1 });
      }
    }
  }

  visited.delete(startNodeId);
  return visited;
}

function findSiblings(
  focalNodeId: string,
  forwardEdges: Map<string, string[]>,
  backwardEdges: Map<string, string[]>
): Set<string> {
  const siblings = new Set<string>();

  const parents = backwardEdges.get(focalNodeId) || [];

  for (const parent of parents) {
    const children = forwardEdges.get(parent) || [];
    children.forEach(child => {
      if (child !== focalNodeId) {
        siblings.add(child);
      }
    });
  }

  return siblings;
}

function passesScaleFilter(
  nodeId: string,
  nodeMap: Map<string, MechanismNode>,
  includeScales?: NodeScale[]
): boolean {
  if (!includeScales || includeScales.length === 0) return true;

  const node = nodeMap.get(nodeId);
  if (!node || !node.scale) return true;

  return includeScales.includes(node.scale);
}

export function calculateNodeNeighborhood(
  selectedNodeId: string,
  nodes: MechanismNode[],
  edges: MechanismEdge[]
): NeighborhoodResult {
  return calculateFilteredNeighborhood(selectedNodeId, nodes, edges, {
    direction: 'both',
    includeSiblings: true
  });
}

export function getNodeLevel(
  nodeId: string,
  parentsMap: Map<string, Set<string>>
): number {
  const parents = parentsMap.get(nodeId);
  if (!parents || parents.size === 0) {
    return 0;
  }

  let maxParentLevel = -1;
  parents.forEach(parentId => {
    const parentLevel = getNodeLevel(parentId, parentsMap);
    maxParentLevel = Math.max(maxParentLevel, parentLevel);
  });

  return maxParentLevel + 1;
}
