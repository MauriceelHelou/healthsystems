/**
 * Unit tests for MechanismGraph component
 *
 * Note: D3.js visualization testing is complex because D3 directly manipulates the DOM.
 * These tests focus on:
 * - Component rendering and mounting
 * - Prop acceptance without errors
 * - Basic structural output
 *
 * For full visualization behavior testing, see E2E tests in tests/e2e/
 */

import { render } from '@testing-library/react';
import '@testing-library/jest-dom';
import { SystemsNetwork, MechanismNode, MechanismEdge } from '../../types/mechanism';

// Mock the graphStateStore with a simple implementation
jest.mock('../../stores/graphStateStore', () => ({
  useGraphStateStore: () => ({
    zoomToNodeId: null,
    zoomToPaths: false,
    clearZoomRequest: jest.fn(),
    clearZoomToPathsRequest: jest.fn(),
  }),
}));

// Mock D3 to prevent DOM manipulation errors in tests
// D3 visualization behavior should be tested via E2E tests
//
// Note: jest.config.js has resetMocks: true, which clears mock implementations
// between tests. We use jest.mock() to set up the initial mock, and then
// restore implementations in beforeEach via a helper function.
jest.mock('d3');

// Import after mocking
import MechanismGraph from '../MechanismGraph';
import * as d3 from 'd3';

// Helper to set up D3 mock - called in beforeEach because jest.config.js has resetMocks: true
function setupD3Mock() {
  // Create a chainable selection mock
  const mockSelection: any = {};
  ['selectAll', 'select', 'attr', 'append', 'call', 'datum', 'filter',
   'on', 'text', 'style', 'classed', 'remove', 'transition', 'duration',
   'each', 'data', 'enter', 'exit', 'merge', 'join', 'raise', 'lower'
  ].forEach(method => {
    mockSelection[method] = jest.fn(() => mockSelection);
  });
  mockSelection.node = jest.fn(() => ({
    getBoundingClientRect: () => ({ width: 800, height: 600, x: 0, y: 0, top: 0, left: 0 }),
    parentNode: null,
  }));
  mockSelection.nodes = jest.fn(() => []);
  mockSelection.empty = jest.fn(() => true);
  mockSelection.size = jest.fn(() => 0);

  // Create a chainable zoom mock
  const mockZoom: any = {};
  ['scaleExtent', 'on', 'transform', 'translateExtent', 'extent', 'filter'].forEach(m => {
    mockZoom[m] = jest.fn(() => mockZoom);
  });

  // Create a chainable simulation mock
  const mockSimulation: any = {};
  ['force', 'alphaDecay', 'velocityDecay', 'alphaMin', 'alpha', 'on', 'alphaTarget', 'tick'
  ].forEach(method => {
    mockSimulation[method] = jest.fn(() => mockSimulation);
  });
  mockSimulation.stop = jest.fn();
  mockSimulation.restart = jest.fn();
  mockSimulation.nodes = jest.fn(() => []);

  // Set up the mock implementations
  (d3.select as jest.Mock).mockImplementation(() => mockSelection);
  (d3.selectAll as jest.Mock).mockImplementation(() => mockSelection);
  (d3.zoom as jest.Mock).mockImplementation(() => mockZoom);
  (d3.forceSimulation as jest.Mock).mockImplementation(() => mockSimulation);
  (d3.forceManyBody as jest.Mock).mockImplementation(() => ({ strength: jest.fn().mockReturnThis() }));
  (d3.forceCenter as jest.Mock).mockImplementation(() => ({}));
  (d3.forceCollide as jest.Mock).mockImplementation(() => ({ radius: jest.fn().mockReturnThis() }));
  (d3.forceLink as jest.Mock).mockImplementation(() => ({
    id: jest.fn().mockReturnThis(),
    distance: jest.fn().mockReturnThis(),
    strength: jest.fn().mockReturnThis()
  }));
  (d3.forceX as jest.Mock).mockImplementation(() => ({ strength: jest.fn().mockReturnThis() }));
  (d3.forceY as jest.Mock).mockImplementation(() => ({ strength: jest.fn().mockReturnThis() }));
  (d3.drag as jest.Mock).mockImplementation(() => ({ on: jest.fn().mockReturnThis() }));

  // Set up zoomIdentity
  (d3 as any).zoomIdentity = {
    translate: jest.fn(function() { return this; }),
    scale: jest.fn(function() { return this; }),
    k: 1,
    x: 0,
    y: 0
  };
}

describe('MechanismGraph', () => {
  // Test data fixtures
  const createMockNode = (
    id: string,
    label: string,
    scale: number = 4,
    category: string = 'economic'
  ): MechanismNode => ({
    id,
    label,
    weight: 1,
    category: category as any,
    stockType: 'structural',
    scale: scale as any,
    connections: { incoming: 1, outgoing: 1 },
  });

  const createMockEdge = (
    id: string,
    source: string,
    target: string,
    direction: 'positive' | 'negative' = 'positive',
    evidenceQuality: 'A' | 'B' | 'C' = 'B'
  ): MechanismEdge => ({
    id,
    source,
    target,
    strength: evidenceQuality === 'A' ? 3 : evidenceQuality === 'B' ? 2 : 1,
    direction,
    evidenceQuality,
    studyCount: 5,
  });

  // Standard test data
  const mockData: SystemsNetwork = {
    nodes: [
      createMockNode('node1', 'Test Node 1', 1, 'political'),
      createMockNode('node2', 'Test Node 2', 3, 'healthcare_access'),
      createMockNode('node3', 'Test Node 3', 7, 'biological'),
    ],
    edges: [
      createMockEdge('edge1', 'node1', 'node2', 'positive', 'B'),
      createMockEdge('edge2', 'node2', 'node3', 'negative', 'A'),
    ],
  };

  beforeEach(() => {
    // Set up D3 mock before each test (required because resetMocks: true in jest.config.js)
    setupD3Mock();
  });

  // ==========================================
  // Basic Rendering Tests
  // ==========================================
  describe('Basic Rendering', () => {
    it('renders an SVG element', () => {
      const { container } = render(<MechanismGraph data={mockData} />);
      const svg = container.querySelector('svg');
      expect(svg).toBeInTheDocument();
    });

    it('applies correct CSS classes to SVG', () => {
      const { container } = render(<MechanismGraph data={mockData} />);
      const svg = container.querySelector('svg');
      expect(svg).toHaveClass('border', 'border-gray-300', 'rounded-lg', 'bg-white');
    });

    it('renders with custom width and height props', () => {
      const { container } = render(
        <MechanismGraph data={mockData} width={800} height={600} />
      );
      const svg = container.querySelector('svg');
      expect(svg).toBeInTheDocument();
    });
  });

  // ==========================================
  // Layout Mode Tests
  // ==========================================
  describe('Layout Mode Props', () => {
    it('accepts hierarchical layout mode', () => {
      expect(() => {
        render(<MechanismGraph data={mockData} layoutMode="hierarchical" />);
      }).not.toThrow();
    });

    it('accepts force-directed layout mode', () => {
      expect(() => {
        render(<MechanismGraph data={mockData} layoutMode="force-directed" />);
      }).not.toThrow();
    });
  });

  // ==========================================
  // Callback Props Tests
  // ==========================================
  describe('Callback Props', () => {
    it('accepts onNodeClick callback', () => {
      const handleNodeClick = jest.fn();
      expect(() => {
        render(<MechanismGraph data={mockData} onNodeClick={handleNodeClick} />);
      }).not.toThrow();
    });

    it('accepts onEdgeClick callback', () => {
      const handleEdgeClick = jest.fn();
      expect(() => {
        render(<MechanismGraph data={mockData} onEdgeClick={handleEdgeClick} />);
      }).not.toThrow();
    });

    it('accepts onNodeSelect callback', () => {
      const handleNodeSelect = jest.fn();
      expect(() => {
        render(
          <MechanismGraph
            data={mockData}
            selectionMode="from"
            onNodeSelect={handleNodeSelect}
          />
        );
      }).not.toThrow();
    });
  });

  // ==========================================
  // Selection Mode Tests
  // ==========================================
  describe('Selection Mode Props', () => {
    it('accepts selectionMode none', () => {
      expect(() => {
        render(<MechanismGraph data={mockData} selectionMode="none" />);
      }).not.toThrow();
    });

    it('accepts selectionMode from', () => {
      expect(() => {
        render(<MechanismGraph data={mockData} selectionMode="from" />);
      }).not.toThrow();
    });

    it('accepts selectionMode to', () => {
      expect(() => {
        render(<MechanismGraph data={mockData} selectionMode="to" />);
      }).not.toThrow();
    });
  });

  // ==========================================
  // Highlighting Props Tests
  // ==========================================
  describe('Highlighting Props', () => {
    it('accepts importantNodes prop', () => {
      const importantNodes = {
        nodeIds: ['node1'],
        ranks: { node1: 1 },
      };
      expect(() => {
        render(<MechanismGraph data={mockData} importantNodes={importantNodes} />);
      }).not.toThrow();
    });

    it('accepts activePaths prop', () => {
      const activePaths = {
        paths: [{ pathId: 'path1', nodeIds: ['node1', 'node2'], edgeIds: ['edge1'] }],
      };
      expect(() => {
        render(<MechanismGraph data={mockData} activePaths={activePaths} />);
      }).not.toThrow();
    });

    it('accepts crisisHighlight prop', () => {
      const crisisHighlight = {
        nodeIdToDegree: new Map([['node3', 0]]),
        policyLeverIds: new Set(['node1']),
      };
      expect(() => {
        render(<MechanismGraph data={mockData} crisisHighlight={crisisHighlight} />);
      }).not.toThrow();
    });

    it('accepts selectedNodeId prop', () => {
      expect(() => {
        render(<MechanismGraph data={mockData} selectedNodeId="node1" />);
      }).not.toThrow();
    });
  });

  // ==========================================
  // Physics Settings Tests
  // ==========================================
  describe('Physics Settings', () => {
    it('accepts physicsSettings prop', () => {
      const physicsSettings = {
        charge: -500,
        linkDistance: 200,
        gravity: 0.1,
        collision: 30,
      };
      expect(() => {
        render(
          <MechanismGraph
            data={mockData}
            layoutMode="force-directed"
            physicsSettings={physicsSettings}
          />
        );
      }).not.toThrow();
    });
  });

  // ==========================================
  // Legend Tests
  // ==========================================
  describe('Legend Props', () => {
    it('accepts showLegend prop', () => {
      expect(() => {
        render(<MechanismGraph data={mockData} showLegend={true} />);
      }).not.toThrow();
    });
  });

  // ==========================================
  // Category Filter Tests
  // ==========================================
  describe('Category Filter Props', () => {
    it('accepts filteredCategories prop', () => {
      expect(() => {
        render(
          <MechanismGraph
            data={mockData}
            filteredCategories={['economic', 'biological']}
          />
        );
      }).not.toThrow();
    });
  });

  // ==========================================
  // Edge Cases Tests
  // ==========================================
  describe('Edge Cases', () => {
    it('handles empty data gracefully', () => {
      const emptyData: SystemsNetwork = { nodes: [], edges: [] };
      const { container } = render(<MechanismGraph data={emptyData} />);
      expect(container.querySelector('svg')).toBeInTheDocument();
    });

    it('handles single node without edges', () => {
      const singleNodeData: SystemsNetwork = {
        nodes: [createMockNode('node1', 'Lonely Node')],
        edges: [],
      };
      expect(() => {
        render(<MechanismGraph data={singleNodeData} />);
      }).not.toThrow();
    });

    it('handles data with many nodes', () => {
      const nodes: MechanismNode[] = [];
      const edges: MechanismEdge[] = [];

      for (let i = 0; i < 50; i++) {
        nodes.push(createMockNode(`node${i}`, `Node ${i}`, (i % 7) + 1 as any));
      }
      for (let i = 0; i < 49; i++) {
        edges.push(createMockEdge(`edge${i}`, `node${i}`, `node${i + 1}`));
      }

      const largeData: SystemsNetwork = { nodes, edges };
      expect(() => {
        render(<MechanismGraph data={largeData} />);
      }).not.toThrow();
    });
  });

  // ==========================================
  // Data Variation Tests
  // ==========================================
  describe('Data Variations', () => {
    it('handles nodes with all scale levels (1-7)', () => {
      const dataWithAllScales: SystemsNetwork = {
        nodes: [
          createMockNode('n1', 'Scale 1', 1, 'political'),
          createMockNode('n2', 'Scale 2', 2, 'built_environment'),
          createMockNode('n3', 'Scale 3', 3, 'healthcare_access'),
          createMockNode('n4', 'Scale 4', 4, 'economic'),
          createMockNode('n5', 'Scale 5', 5, 'behavioral'),
          createMockNode('n6', 'Scale 6', 6, 'biological'),
          createMockNode('n7', 'Scale 7', 7, 'biological'),
        ],
        edges: [
          createMockEdge('e1', 'n1', 'n2'),
          createMockEdge('e2', 'n2', 'n3'),
        ],
      };
      expect(() => {
        render(<MechanismGraph data={dataWithAllScales} />);
      }).not.toThrow();
    });

    it('handles edges with different evidence qualities', () => {
      const dataWithQualities: SystemsNetwork = {
        nodes: [
          createMockNode('n1', 'Node 1'),
          createMockNode('n2', 'Node 2'),
          createMockNode('n3', 'Node 3'),
          createMockNode('n4', 'Node 4'),
        ],
        edges: [
          createMockEdge('e1', 'n1', 'n2', 'positive', 'A'),
          createMockEdge('e2', 'n2', 'n3', 'negative', 'B'),
          createMockEdge('e3', 'n3', 'n4', 'positive', 'C'),
        ],
      };
      expect(() => {
        render(<MechanismGraph data={dataWithQualities} />);
      }).not.toThrow();
    });

    it('handles different stock types', () => {
      const dataWithStockTypes: SystemsNetwork = {
        nodes: [
          { ...createMockNode('n1', 'Structural Node'), stockType: 'structural' },
          { ...createMockNode('n2', 'Crisis Node'), stockType: 'crisis' },
          { ...createMockNode('n3', 'Proxy Node'), stockType: 'proxy' },
        ],
        edges: [
          createMockEdge('e1', 'n1', 'n2'),
          createMockEdge('e2', 'n2', 'n3'),
        ],
      };
      expect(() => {
        render(<MechanismGraph data={dataWithStockTypes} />);
      }).not.toThrow();
    });
  });

  // ==========================================
  // Re-render Tests
  // ==========================================
  describe('Re-renders', () => {
    it('handles data updates', () => {
      const { rerender } = render(<MechanismGraph data={mockData} />);

      const newData: SystemsNetwork = {
        nodes: [
          createMockNode('new1', 'New Node 1'),
          createMockNode('new2', 'New Node 2'),
        ],
        edges: [createMockEdge('newEdge', 'new1', 'new2')],
      };

      expect(() => {
        rerender(<MechanismGraph data={newData} />);
      }).not.toThrow();
    });

    it('handles selectedNodeId changes', () => {
      const { rerender } = render(
        <MechanismGraph data={mockData} selectedNodeId="node1" />
      );

      expect(() => {
        rerender(<MechanismGraph data={mockData} selectedNodeId="node2" />);
      }).not.toThrow();

      expect(() => {
        rerender(<MechanismGraph data={mockData} selectedNodeId={null} />);
      }).not.toThrow();
    });

    it('handles layout mode changes', () => {
      const { rerender } = render(
        <MechanismGraph data={mockData} layoutMode="hierarchical" />
      );

      expect(() => {
        rerender(<MechanismGraph data={mockData} layoutMode="force-directed" />);
      }).not.toThrow();

      expect(() => {
        rerender(<MechanismGraph data={mockData} layoutMode="hierarchical" />);
      }).not.toThrow();
    });
  });

  // ==========================================
  // Edge Selection/Highlighting Tests
  // ==========================================
  describe('Edge Selection Props', () => {
    it('accepts selectedEdgeId prop', () => {
      expect(() => {
        render(<MechanismGraph data={mockData} selectedEdgeId="edge1" />);
      }).not.toThrow();
    });

    it('accepts selectedEdgeId as null', () => {
      expect(() => {
        render(<MechanismGraph data={mockData} selectedEdgeId={null} />);
      }).not.toThrow();
    });

    it('handles selectedEdgeId changes', () => {
      const { rerender } = render(
        <MechanismGraph data={mockData} selectedEdgeId="edge1" />
      );

      expect(() => {
        rerender(<MechanismGraph data={mockData} selectedEdgeId="edge2" />);
      }).not.toThrow();

      expect(() => {
        rerender(<MechanismGraph data={mockData} selectedEdgeId={null} />);
      }).not.toThrow();
    });

    it('handles selectedEdgeId with nonexistent edge id', () => {
      expect(() => {
        render(<MechanismGraph data={mockData} selectedEdgeId="nonexistent-edge" />);
      }).not.toThrow();
    });

    it('handles simultaneous node and edge selection', () => {
      expect(() => {
        render(
          <MechanismGraph
            data={mockData}
            selectedNodeId="node1"
            selectedEdgeId="edge1"
          />
        );
      }).not.toThrow();
    });

    it('handles switching from node to edge selection', () => {
      const { rerender } = render(
        <MechanismGraph data={mockData} selectedNodeId="node1" selectedEdgeId={null} />
      );

      expect(() => {
        rerender(
          <MechanismGraph data={mockData} selectedNodeId={null} selectedEdgeId="edge1" />
        );
      }).not.toThrow();
    });

    it('handles switching from edge to node selection', () => {
      const { rerender } = render(
        <MechanismGraph data={mockData} selectedNodeId={null} selectedEdgeId="edge1" />
      );

      expect(() => {
        rerender(
          <MechanismGraph data={mockData} selectedNodeId="node1" selectedEdgeId={null} />
        );
      }).not.toThrow();
    });

    it('handles clearing both selections', () => {
      const { rerender } = render(
        <MechanismGraph data={mockData} selectedNodeId="node1" selectedEdgeId="edge1" />
      );

      expect(() => {
        rerender(
          <MechanismGraph data={mockData} selectedNodeId={null} selectedEdgeId={null} />
        );
      }).not.toThrow();
    });
  });
});
