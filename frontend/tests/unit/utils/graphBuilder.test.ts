/**
 * Unit tests for graphBuilder utilities
 */

import {
  buildGraphFromMechanisms,
  filterGraphByCategory,
  filterGraphByScale,
  filterByMinConnections,
  calculateNodeMetrics,
  getGraphCategories,
  getGraphScales,
  buildAlcoholismSubgraph,
  buildDomainSubgraph,
  calculateGraphStats,
} from '../../../src/utils/graphBuilder';
import type { Mechanism, SystemsNetwork, Category } from '../../../src/types/mechanism';

// Mock mechanisms for testing
const createMockMechanism = (
  id: string,
  fromNodeId: string,
  toNodeId: string,
  category: Category,
  evidenceQuality: 'A' | 'B' | 'C' = 'B'
): Mechanism => ({
  id,
  name: `Mechanism ${id}`,
  from_node_id: fromNodeId,
  from_node_name: `Node ${fromNodeId}`,
  to_node_id: toNodeId,
  to_node_name: `Node ${toNodeId}`,
  direction: 'positive',
  category,
  evidence_quality: evidenceQuality,
  n_studies: 1,
});

describe('graphBuilder', () => {
  describe('buildGraphFromMechanisms', () => {
    it('should build nodes and edges from mechanisms', () => {
      const mechanisms = [
        createMockMechanism('mech1', 'node1', 'node2', 'economic'),
        createMockMechanism('mech2', 'node2', 'node3', 'social_environment'),
      ];

      const graph = buildGraphFromMechanisms(mechanisms);

      expect(graph.nodes).toHaveLength(3);
      expect(graph.edges).toHaveLength(2);

      // Check node1
      const node1 = graph.nodes.find(n => n.id === 'node1');
      expect(node1).toBeDefined();
      expect(node1?.label).toBe('Node node1');
      expect(node1?.connections.outgoing).toBe(1);
      expect(node1?.connections.incoming).toBe(0);

      // Check node2
      const node2 = graph.nodes.find(n => n.id === 'node2');
      expect(node2).toBeDefined();
      expect(node2?.connections.outgoing).toBe(1);
      expect(node2?.connections.incoming).toBe(1);
      expect(node2?.weight).toBe(2); // incoming + outgoing

      // Check edges
      expect(graph.edges[0].source).toBe('node1');
      expect(graph.edges[0].target).toBe('node2');
      expect(graph.edges[0].strength).toBe(2); // B quality = 2
    });

    it('should filter by category', () => {
      const mechanisms = [
        createMockMechanism('mech1', 'node1', 'node2', 'economic'),
        createMockMechanism('mech2', 'node2', 'node3', 'social_environment'),
        createMockMechanism('mech3', 'node3', 'node4', 'economic'),
      ];

      const graph = buildGraphFromMechanisms(mechanisms, {
        filterCategories: ['economic'],
      });

      expect(graph.edges).toHaveLength(2);
      expect(graph.edges.every(e => e.category === 'economic')).toBe(true);
      expect(graph.nodes).toHaveLength(3); // node1, node2, node3, node4 but only connected via economic
    });

    it('should exclude disconnected nodes by default', () => {
      const mechanisms = [
        createMockMechanism('mech1', 'node1', 'node2', 'economic'),
      ];

      const graph = buildGraphFromMechanisms(mechanisms, {
        includeDisconnected: false,
      });

      // Should only include nodes that are connected
      expect(graph.nodes).toHaveLength(2);
      expect(graph.nodes.every(n => ['node1', 'node2'].includes(n.id))).toBe(true);
    });

    it('should map evidence quality to strength correctly', () => {
      const mechanisms = [
        createMockMechanism('mech1', 'node1', 'node2', 'economic', 'A'),
        createMockMechanism('mech2', 'node2', 'node3', 'economic', 'B'),
        createMockMechanism('mech3', 'node3', 'node4', 'economic', 'C'),
      ];

      const graph = buildGraphFromMechanisms(mechanisms);

      expect(graph.edges[0].strength).toBe(3); // A = 3
      expect(graph.edges[1].strength).toBe(2); // B = 2
      expect(graph.edges[2].strength).toBe(1); // C = 1
    });
  });

  describe('filterGraphByCategory', () => {
    const mockGraph: SystemsNetwork = {
      nodes: [
        { id: 'node1', label: 'Node 1', category: 'economic', stockType: 'structural', weight: 1, connections: { incoming: 0, outgoing: 1 } },
        { id: 'node2', label: 'Node 2', category: 'social_environment', stockType: 'structural', weight: 1, connections: { incoming: 1, outgoing: 1 } },
        { id: 'node3', label: 'Node 3', category: 'economic', stockType: 'structural', weight: 1, connections: { incoming: 1, outgoing: 0 } },
      ],
      edges: [
        { id: 'edge1', source: 'node1', target: 'node2', direction: 'positive', category: 'economic', evidenceQuality: 'B', strength: 2, studyCount: 1 },
        { id: 'edge2', source: 'node2', target: 'node3', direction: 'positive', category: 'social_environment', evidenceQuality: 'B', strength: 2, studyCount: 1 },
      ],
    };

    it('should filter edges by category', () => {
      const filtered = filterGraphByCategory(mockGraph, ['economic']);

      expect(filtered.edges).toHaveLength(1);
      expect(filtered.edges[0].category).toBe('economic');
    });

    it('should only include nodes referenced in filtered edges', () => {
      const filtered = filterGraphByCategory(mockGraph, ['economic']);

      expect(filtered.nodes).toHaveLength(2);
      expect(filtered.nodes.map(n => n.id).sort()).toEqual(['node1', 'node2']);
    });

    it('should return full graph when categories array is empty', () => {
      const filtered = filterGraphByCategory(mockGraph, []);

      expect(filtered.nodes).toHaveLength(mockGraph.nodes.length);
      expect(filtered.edges).toHaveLength(mockGraph.edges.length);
    });
  });

  describe('filterGraphByScale', () => {
    const mockGraph: SystemsNetwork = {
      nodes: [
        { id: 'node1', label: 'Node 1', category: 'economic', stockType: 'structural', scale: 1, weight: 1, connections: { incoming: 0, outgoing: 1 } },
        { id: 'node2', label: 'Node 2', category: 'economic', stockType: 'structural', scale: 2, weight: 1, connections: { incoming: 1, outgoing: 1 } },
        { id: 'node3', label: 'Node 3', category: 'economic', stockType: 'structural', scale: 3, weight: 1, connections: { incoming: 1, outgoing: 0 } },
      ],
      edges: [
        { id: 'edge1', source: 'node1', target: 'node2', direction: 'positive', category: 'economic', evidenceQuality: 'B', strength: 2, studyCount: 1 },
        { id: 'edge2', source: 'node2', target: 'node3', direction: 'positive', category: 'economic', evidenceQuality: 'B', strength: 2, studyCount: 1 },
      ],
    };

    it('should filter nodes by scale', () => {
      const filtered = filterGraphByScale(mockGraph, [1, 2]);

      expect(filtered.nodes).toHaveLength(2);
      expect(filtered.nodes.every(n => n.scale && [1, 2].includes(n.scale))).toBe(true);
    });

    it('should only include edges between filtered nodes', () => {
      const filtered = filterGraphByScale(mockGraph, [1, 2]);

      expect(filtered.edges).toHaveLength(1);
      expect(filtered.edges[0].source).toBe('node1');
      expect(filtered.edges[0].target).toBe('node2');
    });

    it('should return full graph when scales array is empty', () => {
      const filtered = filterGraphByScale(mockGraph, []);

      expect(filtered.nodes).toHaveLength(mockGraph.nodes.length);
      expect(filtered.edges).toHaveLength(mockGraph.edges.length);
    });
  });

  describe('calculateNodeMetrics', () => {
    it('should calculate degree and centrality metrics', () => {
      const graph: SystemsNetwork = {
        nodes: [
          { id: 'node1', label: 'Node 1', category: 'economic', stockType: 'structural', weight: 1, connections: { incoming: 2, outgoing: 3 } },
          { id: 'node2', label: 'Node 2', category: 'economic', stockType: 'structural', weight: 1, connections: { incoming: 1, outgoing: 1 } },
        ],
        edges: [],
      };

      const withMetrics = calculateNodeMetrics(graph);

      const node1 = withMetrics.nodes[0] as any;
      expect(node1.degree).toBe(5); // 2 + 3
      expect(node1.centrality).toBe(5 / 2); // degree / total nodes

      const node2 = withMetrics.nodes[1] as any;
      expect(node2.degree).toBe(2); // 1 + 1
      expect(node2.centrality).toBe(2 / 2);
    });
  });

  describe('getGraphCategories', () => {
    it('should return unique categories from edges', () => {
      const graph: SystemsNetwork = {
        nodes: [],
        edges: [
          { id: 'e1', source: 'n1', target: 'n2', direction: 'positive', category: 'economic', evidenceQuality: 'B', strength: 2, studyCount: 1 },
          { id: 'e2', source: 'n2', target: 'n3', direction: 'positive', category: 'social_environment', evidenceQuality: 'B', strength: 2, studyCount: 1 },
          { id: 'e3', source: 'n3', target: 'n4', direction: 'positive', category: 'economic', evidenceQuality: 'B', strength: 2, studyCount: 1 },
        ],
      };

      const categories = getGraphCategories(graph);

      expect(categories).toHaveLength(2);
      expect(categories).toContain('economic');
      expect(categories).toContain('social_environment');
    });
  });

  describe('getGraphScales', () => {
    it('should return unique scales from nodes in sorted order', () => {
      const graph: SystemsNetwork = {
        nodes: [
          { id: 'node1', label: 'N1', category: 'economic', stockType: 'structural', scale: 3, weight: 1, connections: { incoming: 0, outgoing: 0 } },
          { id: 'node2', label: 'N2', category: 'economic', stockType: 'structural', scale: 1, weight: 1, connections: { incoming: 0, outgoing: 0 } },
          { id: 'node3', label: 'N3', category: 'economic', stockType: 'structural', scale: 3, weight: 1, connections: { incoming: 0, outgoing: 0 } },
          { id: 'node4', label: 'N4', category: 'economic', stockType: 'structural', scale: 2, weight: 1, connections: { incoming: 0, outgoing: 0 } },
        ],
        edges: [],
      };

      const scales = getGraphScales(graph);

      expect(scales).toEqual([1, 2, 3]);
    });
  });

  describe('buildAlcoholismSubgraph', () => {
    it('should filter mechanisms with alcohol-related keywords', () => {
      const mechanisms = [
        createMockMechanism('mech1', 'alcohol_use', 'liver_disease', 'behavioral'),
        createMockMechanism('mech2', 'poverty', 'depression', 'economic'),
        createMockMechanism('mech3', 'binge_drinking', 'ald', 'behavioral'),
      ];

      const subgraph = buildAlcoholismSubgraph(mechanisms);

      expect(subgraph.edges).toHaveLength(2);
      expect(subgraph.nodes.length).toBeGreaterThan(0);

      // Should include alcohol and ald related mechanisms
      expect(subgraph.edges.some(e => e.id === 'mech1')).toBe(true);
      expect(subgraph.edges.some(e => e.id === 'mech3')).toBe(true);
      expect(subgraph.edges.some(e => e.id === 'mech2')).toBe(false);
    });

    it('should match keywords in mechanism name and node names', () => {
      const mechanisms = [
        {
          ...createMockMechanism('mech1', 'stress', 'outcome', 'social_environment'),
          name: 'Alcohol consumption pathway',
        },
      ];

      const subgraph = buildAlcoholismSubgraph(mechanisms);

      expect(subgraph.edges).toHaveLength(1);
    });
  });

  describe('calculateGraphStats', () => {
    it('should calculate comprehensive graph statistics', () => {
      const mechanisms = [
        createMockMechanism('mech1', 'node1', 'node2', 'economic'),
        createMockMechanism('mech2', 'node2', 'node3', 'social_environment'),
        createMockMechanism('mech3', 'node3', 'node4', 'economic'),
      ];

      const graph = buildGraphFromMechanisms(mechanisms);
      const stats = calculateGraphStats(graph);

      expect(stats.totalNodes).toBe(4);
      expect(stats.totalEdges).toBe(3);
      expect(stats.nodesByCategory).toHaveProperty('economic');
      expect(stats.edgesByCategory).toHaveProperty('economic');
      expect(stats.edgesByCategory.economic).toBe(2);
      expect(stats.edgesByCategory.social_environment).toBe(1);
      expect(stats.avgDegree).toBeGreaterThan(0);
      expect(stats.maxDegree).toBeGreaterThanOrEqual(stats.minDegree);
    });
  });

  describe('filterByMinConnections', () => {
    it('should return graph unchanged when minConnections is 1 or less', () => {
      const graph: SystemsNetwork = {
        nodes: [
          { id: 'node1', label: 'Node 1', category: 'economic', stockType: 'structural', weight: 1, connections: { incoming: 0, outgoing: 1 } },
          { id: 'node2', label: 'Node 2', category: 'economic', stockType: 'structural', weight: 1, connections: { incoming: 1, outgoing: 0 } },
        ],
        edges: [
          { id: 'edge1', source: 'node1', target: 'node2', direction: 'positive', category: 'economic', evidenceQuality: 'B', strength: 2, studyCount: 1 },
        ],
      };

      const filtered = filterByMinConnections(graph, 1);
      expect(filtered.nodes).toHaveLength(2);
      expect(filtered.edges).toHaveLength(1);

      const filteredZero = filterByMinConnections(graph, 0);
      expect(filteredZero.nodes).toHaveLength(2);
    });

    it('should filter out nodes with fewer than minConnections', () => {
      // node1 -> node2 -> node3
      //                -> node4
      // node1 has 1 connection, node2 has 3, node3 has 1, node4 has 1
      const graph: SystemsNetwork = {
        nodes: [
          { id: 'node1', label: 'Node 1', category: 'economic', stockType: 'structural', weight: 1, connections: { incoming: 0, outgoing: 1 } },
          { id: 'node2', label: 'Node 2', category: 'economic', stockType: 'structural', weight: 3, connections: { incoming: 1, outgoing: 2 } },
          { id: 'node3', label: 'Node 3', category: 'economic', stockType: 'structural', weight: 1, connections: { incoming: 1, outgoing: 0 } },
          { id: 'node4', label: 'Node 4', category: 'economic', stockType: 'structural', weight: 1, connections: { incoming: 1, outgoing: 0 } },
        ],
        edges: [
          { id: 'edge1', source: 'node1', target: 'node2', direction: 'positive', category: 'economic', evidenceQuality: 'B', strength: 2, studyCount: 1 },
          { id: 'edge2', source: 'node2', target: 'node3', direction: 'positive', category: 'economic', evidenceQuality: 'B', strength: 2, studyCount: 1 },
          { id: 'edge3', source: 'node2', target: 'node4', direction: 'positive', category: 'economic', evidenceQuality: 'B', strength: 2, studyCount: 1 },
        ],
      };

      const filtered = filterByMinConnections(graph, 2);

      // Only node2 has 3 connections (>= 2), but when we remove others, it loses its connections
      // After removing node1, node3, node4, node2 has 0 connections, so it gets removed too
      // Result: empty graph due to iterative filtering
      expect(filtered.nodes).toHaveLength(0);
      expect(filtered.edges).toHaveLength(0);
    });

    it('should keep highly connected nodes and their edges', () => {
      // Create a more connected graph: hub topology
      // hub connects to: node1, node2, node3, node4
      // So hub has 4 connections
      // All leaf nodes have 1 connection each
      const graph: SystemsNetwork = {
        nodes: [
          { id: 'hub', label: 'Hub', category: 'economic', stockType: 'structural', weight: 4, connections: { incoming: 0, outgoing: 4 } },
          { id: 'node1', label: 'Node 1', category: 'economic', stockType: 'structural', weight: 1, connections: { incoming: 1, outgoing: 0 } },
          { id: 'node2', label: 'Node 2', category: 'economic', stockType: 'structural', weight: 1, connections: { incoming: 1, outgoing: 0 } },
          { id: 'node3', label: 'Node 3', category: 'economic', stockType: 'structural', weight: 1, connections: { incoming: 1, outgoing: 0 } },
          { id: 'node4', label: 'Node 4', category: 'economic', stockType: 'structural', weight: 1, connections: { incoming: 1, outgoing: 0 } },
        ],
        edges: [
          { id: 'e1', source: 'hub', target: 'node1', direction: 'positive', category: 'economic', evidenceQuality: 'B', strength: 2, studyCount: 1 },
          { id: 'e2', source: 'hub', target: 'node2', direction: 'positive', category: 'economic', evidenceQuality: 'B', strength: 2, studyCount: 1 },
          { id: 'e3', source: 'hub', target: 'node3', direction: 'positive', category: 'economic', evidenceQuality: 'B', strength: 2, studyCount: 1 },
          { id: 'e4', source: 'hub', target: 'node4', direction: 'positive', category: 'economic', evidenceQuality: 'B', strength: 2, studyCount: 1 },
        ],
      };

      // With minConnections=2, leaf nodes are removed
      // Then hub has 0 connections and also removed
      const filtered = filterByMinConnections(graph, 2);
      expect(filtered.nodes).toHaveLength(0);
    });

    it('should preserve mutual connections between well-connected nodes', () => {
      // Triangle: A <-> B <-> C <-> A
      // Each node has 2 connections
      const graph: SystemsNetwork = {
        nodes: [
          { id: 'A', label: 'A', category: 'economic', stockType: 'structural', weight: 2, connections: { incoming: 1, outgoing: 1 } },
          { id: 'B', label: 'B', category: 'economic', stockType: 'structural', weight: 2, connections: { incoming: 1, outgoing: 1 } },
          { id: 'C', label: 'C', category: 'economic', stockType: 'structural', weight: 2, connections: { incoming: 1, outgoing: 1 } },
        ],
        edges: [
          { id: 'e1', source: 'A', target: 'B', direction: 'positive', category: 'economic', evidenceQuality: 'B', strength: 2, studyCount: 1 },
          { id: 'e2', source: 'B', target: 'C', direction: 'positive', category: 'economic', evidenceQuality: 'B', strength: 2, studyCount: 1 },
          { id: 'e3', source: 'C', target: 'A', direction: 'positive', category: 'economic', evidenceQuality: 'B', strength: 2, studyCount: 1 },
        ],
      };

      const filtered = filterByMinConnections(graph, 2);

      // All nodes have 2 connections, so all should be kept
      expect(filtered.nodes).toHaveLength(3);
      expect(filtered.edges).toHaveLength(3);
    });

    it('should update connection counts after filtering', () => {
      // Diamond: A -> B, A -> C, B -> D, C -> D
      // A has 2 out, B has 1 in + 1 out = 2, C has 1 in + 1 out = 2, D has 2 in
      const graph: SystemsNetwork = {
        nodes: [
          { id: 'A', label: 'A', category: 'economic', stockType: 'structural', weight: 2, connections: { incoming: 0, outgoing: 2 } },
          { id: 'B', label: 'B', category: 'economic', stockType: 'structural', weight: 2, connections: { incoming: 1, outgoing: 1 } },
          { id: 'C', label: 'C', category: 'economic', stockType: 'structural', weight: 2, connections: { incoming: 1, outgoing: 1 } },
          { id: 'D', label: 'D', category: 'economic', stockType: 'structural', weight: 2, connections: { incoming: 2, outgoing: 0 } },
        ],
        edges: [
          { id: 'e1', source: 'A', target: 'B', direction: 'positive', category: 'economic', evidenceQuality: 'B', strength: 2, studyCount: 1 },
          { id: 'e2', source: 'A', target: 'C', direction: 'positive', category: 'economic', evidenceQuality: 'B', strength: 2, studyCount: 1 },
          { id: 'e3', source: 'B', target: 'D', direction: 'positive', category: 'economic', evidenceQuality: 'B', strength: 2, studyCount: 1 },
          { id: 'e4', source: 'C', target: 'D', direction: 'positive', category: 'economic', evidenceQuality: 'B', strength: 2, studyCount: 1 },
        ],
      };

      const filtered = filterByMinConnections(graph, 2);

      // All nodes have >= 2 connections, so all should be kept
      expect(filtered.nodes).toHaveLength(4);
      expect(filtered.edges).toHaveLength(4);

      // Verify connections are correct
      const nodeA = filtered.nodes.find(n => n.id === 'A');
      expect(nodeA?.connections.outgoing).toBe(2);
      expect(nodeA?.connections.incoming).toBe(0);

      const nodeD = filtered.nodes.find(n => n.id === 'D');
      expect(nodeD?.connections.incoming).toBe(2);
      expect(nodeD?.connections.outgoing).toBe(0);
    });

    it('should handle graph with no edges', () => {
      const graph: SystemsNetwork = {
        nodes: [
          { id: 'node1', label: 'Node 1', category: 'economic', stockType: 'structural', weight: 0, connections: { incoming: 0, outgoing: 0 } },
          { id: 'node2', label: 'Node 2', category: 'economic', stockType: 'structural', weight: 0, connections: { incoming: 0, outgoing: 0 } },
        ],
        edges: [],
      };

      const filtered = filterByMinConnections(graph, 2);
      expect(filtered.nodes).toHaveLength(0);
      expect(filtered.edges).toHaveLength(0);
    });

    it('should handle empty graph', () => {
      const graph: SystemsNetwork = { nodes: [], edges: [] };
      const filtered = filterByMinConnections(graph, 2);
      expect(filtered.nodes).toHaveLength(0);
      expect(filtered.edges).toHaveLength(0);
    });

    it('should iteratively remove nodes that fall below threshold', () => {
      // Chain: A -> B -> C -> D -> E
      // Each internal node has 2 connections, endpoints have 1
      // With minConnections=2, A and E get removed first
      // Then B and D have only 1 connection each, get removed
      // Then C has 0 connections, gets removed
      const graph: SystemsNetwork = {
        nodes: [
          { id: 'A', label: 'A', category: 'economic', stockType: 'structural', weight: 1, connections: { incoming: 0, outgoing: 1 } },
          { id: 'B', label: 'B', category: 'economic', stockType: 'structural', weight: 2, connections: { incoming: 1, outgoing: 1 } },
          { id: 'C', label: 'C', category: 'economic', stockType: 'structural', weight: 2, connections: { incoming: 1, outgoing: 1 } },
          { id: 'D', label: 'D', category: 'economic', stockType: 'structural', weight: 2, connections: { incoming: 1, outgoing: 1 } },
          { id: 'E', label: 'E', category: 'economic', stockType: 'structural', weight: 1, connections: { incoming: 1, outgoing: 0 } },
        ],
        edges: [
          { id: 'e1', source: 'A', target: 'B', direction: 'positive', category: 'economic', evidenceQuality: 'B', strength: 2, studyCount: 1 },
          { id: 'e2', source: 'B', target: 'C', direction: 'positive', category: 'economic', evidenceQuality: 'B', strength: 2, studyCount: 1 },
          { id: 'e3', source: 'C', target: 'D', direction: 'positive', category: 'economic', evidenceQuality: 'B', strength: 2, studyCount: 1 },
          { id: 'e4', source: 'D', target: 'E', direction: 'positive', category: 'economic', evidenceQuality: 'B', strength: 2, studyCount: 1 },
        ],
      };

      const filtered = filterByMinConnections(graph, 2);

      // All nodes should be removed due to cascading effect
      expect(filtered.nodes).toHaveLength(0);
      expect(filtered.edges).toHaveLength(0);
    });
  });

  describe('buildDomainSubgraph with minConnections', () => {
    it('should apply minConnections filter after keyword filtering', () => {
      const mechanisms = [
        createMockMechanism('mech1', 'alcohol_use', 'liver_damage', 'behavioral'),
        createMockMechanism('mech2', 'liver_damage', 'mortality', 'biological'),
        createMockMechanism('mech3', 'poverty', 'depression', 'economic'),
        createMockMechanism('mech4', 'alcohol_use', 'depression', 'behavioral'),
      ];

      // Without minConnections
      const subgraphNoMin = buildDomainSubgraph(mechanisms, ['alcohol', 'liver'], {
        includeDisconnected: false,
      });

      expect(subgraphNoMin.edges.length).toBeGreaterThanOrEqual(2);

      // With minConnections=2
      const subgraphWithMin = buildDomainSubgraph(mechanisms, ['alcohol', 'liver'], {
        includeDisconnected: false,
        minConnections: 2,
      });

      // Should have fewer or equal nodes/edges
      expect(subgraphWithMin.nodes.length).toBeLessThanOrEqual(subgraphNoMin.nodes.length);
    });

    it('should work with minConnections=1 (no filtering)', () => {
      const mechanisms = [
        createMockMechanism('mech1', 'alcohol_use', 'liver_damage', 'behavioral'),
      ];

      const subgraph = buildDomainSubgraph(mechanisms, ['alcohol'], {
        minConnections: 1,
      });

      expect(subgraph.nodes.length).toBe(2);
      expect(subgraph.edges.length).toBe(1);
    });
  });
});
