import { calculateFilteredNeighborhood } from '../graphNeighborhood';
import type { MechanismNode, MechanismEdge } from '../../types/mechanism';

describe('calculateFilteredNeighborhood', () => {
  const nodes: MechanismNode[] = [
    {
      id: 'policy',
      label: 'Policy',
      scale: 1,
      category: 'political',
      stockType: 'structural',
      weight: 1,
      connections: { incoming: 0, outgoing: 1 }
    },
    {
      id: 'environment',
      label: 'Environment',
      scale: 2,
      category: 'built_environment',
      stockType: 'structural',
      weight: 1,
      connections: { incoming: 1, outgoing: 1 }
    },
    {
      id: 'condition',
      label: 'Condition',
      scale: 4,
      category: 'economic',
      stockType: 'structural',
      weight: 1,
      connections: { incoming: 1, outgoing: 1 }
    },
    {
      id: 'behavior',
      label: 'Behavior',
      scale: 5,
      category: 'behavioral',
      stockType: 'structural',
      weight: 1,
      connections: { incoming: 1, outgoing: 1 }
    },
    {
      id: 'crisis',
      label: 'Crisis',
      scale: 7,
      category: 'biological',
      stockType: 'structural',
      weight: 1,
      connections: { incoming: 1, outgoing: 0 }
    }
  ];

  const edges: MechanismEdge[] = [
    {
      id: 'edge1',
      source: 'policy',
      target: 'environment',
      category: 'political',
      direction: 'positive',
      evidenceQuality: 'A',
      strength: 3,
      studyCount: 5
    },
    {
      id: 'edge2',
      source: 'environment',
      target: 'condition',
      category: 'economic',
      direction: 'positive',
      evidenceQuality: 'B',
      strength: 2,
      studyCount: 3
    },
    {
      id: 'edge3',
      source: 'condition',
      target: 'behavior',
      category: 'behavioral',
      direction: 'positive',
      evidenceQuality: 'A',
      strength: 3,
      studyCount: 4
    },
    {
      id: 'edge4',
      source: 'behavior',
      target: 'crisis',
      category: 'biological',
      direction: 'positive',
      evidenceQuality: 'B',
      strength: 2,
      studyCount: 2
    }
  ];

  test('both directions - includes upstream and downstream', () => {
    const { visibleNodeIds } = calculateFilteredNeighborhood('condition', nodes, edges, {
      direction: 'both'
    });

    expect(visibleNodeIds).toContain('condition');
    expect(visibleNodeIds).toContain('environment'); // upstream
    expect(visibleNodeIds).toContain('policy'); // upstream
    expect(visibleNodeIds).toContain('behavior'); // downstream
    expect(visibleNodeIds).toContain('crisis'); // downstream
    expect(visibleNodeIds.size).toBe(5); // All nodes
  });

  test('upstream only - includes only predecessors', () => {
    const { visibleNodeIds } = calculateFilteredNeighborhood('condition', nodes, edges, {
      direction: 'upstream'
    });

    expect(visibleNodeIds).toContain('condition');
    expect(visibleNodeIds).toContain('environment');
    expect(visibleNodeIds).toContain('policy');
    expect(visibleNodeIds).not.toContain('behavior');
    expect(visibleNodeIds).not.toContain('crisis');
    expect(visibleNodeIds.size).toBe(3);
  });

  test('downstream only - includes only successors', () => {
    const { visibleNodeIds } = calculateFilteredNeighborhood('condition', nodes, edges, {
      direction: 'downstream'
    });

    expect(visibleNodeIds).toContain('condition');
    expect(visibleNodeIds).not.toContain('environment');
    expect(visibleNodeIds).not.toContain('policy');
    expect(visibleNodeIds).toContain('behavior');
    expect(visibleNodeIds).toContain('crisis');
    expect(visibleNodeIds.size).toBe(3);
  });

  test('category filter - only follows specified categories', () => {
    const { visibleNodeIds } = calculateFilteredNeighborhood('condition', nodes, edges, {
      direction: 'both',
      includeCategories: ['economic', 'behavioral']
    });

    expect(visibleNodeIds).toContain('condition');
    expect(visibleNodeIds).toContain('behavior'); // behavioral edge exists
    expect(visibleNodeIds).toContain('environment'); // economic edge exists from environment→condition
    expect(visibleNodeIds).not.toContain('policy'); // political edge excluded
    expect(visibleNodeIds).not.toContain('crisis'); // biological edge excluded
  });

  test('scale filter - only includes specified scales', () => {
    const { visibleNodeIds } = calculateFilteredNeighborhood('condition', nodes, edges, {
      direction: 'both',
      includeScales: [1, 4, 7] // policy, condition, crisis only
    });

    expect(visibleNodeIds).toContain('condition'); // scale 4
    expect(visibleNodeIds).toContain('policy'); // scale 1
    expect(visibleNodeIds).toContain('crisis'); // scale 7
    expect(visibleNodeIds).not.toContain('environment'); // scale 2 excluded
    expect(visibleNodeIds).not.toContain('behavior'); // scale 5 excluded
  });

  test('hop limit - respects max hops upstream', () => {
    const { visibleNodeIds } = calculateFilteredNeighborhood('condition', nodes, edges, {
      direction: 'upstream',
      maxHopsUpstream: 1
    });

    expect(visibleNodeIds).toContain('condition');
    expect(visibleNodeIds).toContain('environment'); // 1 hop away
    expect(visibleNodeIds).not.toContain('policy'); // 2 hops away, exceeds limit
    expect(visibleNodeIds.size).toBe(2);
  });

  test('hop limit - respects max hops downstream', () => {
    const { visibleNodeIds } = calculateFilteredNeighborhood('condition', nodes, edges, {
      direction: 'downstream',
      maxHopsDownstream: 1
    });

    expect(visibleNodeIds).toContain('condition');
    expect(visibleNodeIds).toContain('behavior'); // 1 hop away
    expect(visibleNodeIds).not.toContain('crisis'); // 2 hops away, exceeds limit
    expect(visibleNodeIds.size).toBe(2);
  });

  test('dimmed nodes - contains all non-visible nodes', () => {
    const { visibleNodeIds, dimmedNodeIds } = calculateFilteredNeighborhood('condition', nodes, edges, {
      direction: 'upstream',
      maxHopsUpstream: 1
    });

    expect(visibleNodeIds).toContain('condition');
    expect(visibleNodeIds).toContain('environment');
    expect(dimmedNodeIds).toContain('policy'); // not visible
    expect(dimmedNodeIds).toContain('behavior'); // not visible
    expect(dimmedNodeIds).toContain('crisis'); // not visible
    expect(dimmedNodeIds).not.toContain('condition'); // visible
    expect(dimmedNodeIds).not.toContain('environment'); // visible
    expect(dimmedNodeIds.size).toBe(3);
  });

  test('siblings - includes sibling nodes when enabled', () => {
    // Create a graph with siblings
    const nodesWithSiblings: MechanismNode[] = [
      {
        id: 'parent',
        label: 'Parent',
        scale: 1,
        category: 'political',
        stockType: 'structural',
        weight: 1,
        connections: { incoming: 0, outgoing: 2 }
      },
      {
        id: 'child1',
        label: 'Child 1',
        scale: 2,
        category: 'economic',
        stockType: 'structural',
        weight: 1,
        connections: { incoming: 1, outgoing: 0 }
      },
      {
        id: 'child2',
        label: 'Child 2',
        scale: 2,
        category: 'economic',
        stockType: 'structural',
        weight: 1,
        connections: { incoming: 1, outgoing: 0 }
      }
    ];

    const edgesWithSiblings: MechanismEdge[] = [
      {
        id: 'edge1',
        source: 'parent',
        target: 'child1',
        category: 'economic',
        direction: 'positive',
        evidenceQuality: 'A',
        strength: 3,
        studyCount: 2
      },
      {
        id: 'edge2',
        source: 'parent',
        target: 'child2',
        category: 'economic',
        direction: 'positive',
        evidenceQuality: 'A',
        strength: 3,
        studyCount: 2
      }
    ];

    const { visibleNodeIds } = calculateFilteredNeighborhood('child1', nodesWithSiblings, edgesWithSiblings, {
      direction: 'both',
      includeSiblings: true
    });

    expect(visibleNodeIds).toContain('child1');
    expect(visibleNodeIds).toContain('parent'); // upstream
    expect(visibleNodeIds).toContain('child2'); // sibling
    expect(visibleNodeIds.size).toBe(3);
  });

  test('no siblings - excludes sibling nodes when disabled', () => {
    const nodesWithSiblings: MechanismNode[] = [
      {
        id: 'parent',
        label: 'Parent',
        scale: 1,
        category: 'political',
        stockType: 'structural',
        weight: 1,
        connections: { incoming: 0, outgoing: 2 }
      },
      {
        id: 'child1',
        label: 'Child 1',
        scale: 2,
        category: 'economic',
        stockType: 'structural',
        weight: 1,
        connections: { incoming: 1, outgoing: 0 }
      },
      {
        id: 'child2',
        label: 'Child 2',
        scale: 2,
        category: 'economic',
        stockType: 'structural',
        weight: 1,
        connections: { incoming: 1, outgoing: 0 }
      }
    ];

    const edgesWithSiblings: MechanismEdge[] = [
      {
        id: 'edge1',
        source: 'parent',
        target: 'child1',
        category: 'economic',
        direction: 'positive',
        evidenceQuality: 'A',
        strength: 3,
        studyCount: 2
      },
      {
        id: 'edge2',
        source: 'parent',
        target: 'child2',
        category: 'economic',
        direction: 'positive',
        evidenceQuality: 'A',
        strength: 3,
        studyCount: 2
      }
    ];

    const { visibleNodeIds } = calculateFilteredNeighborhood('child1', nodesWithSiblings, edgesWithSiblings, {
      direction: 'both',
      includeSiblings: false
    });

    expect(visibleNodeIds).toContain('child1');
    expect(visibleNodeIds).toContain('parent'); // upstream
    expect(visibleNodeIds).not.toContain('child2'); // sibling excluded
    expect(visibleNodeIds.size).toBe(2);
  });
});
