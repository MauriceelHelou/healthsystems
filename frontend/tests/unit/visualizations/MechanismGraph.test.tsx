/**
 * Tests for MechanismGraph component with force-directed layout support
 */

import { render, waitFor, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import { SystemsNetwork, PhysicsSettings } from '../../../src/types/mechanism';

// Mock graph state store
jest.mock('../../../src/stores/graphStateStore', () => ({
  useGraphStateStore: jest.fn(() => ({
    zoomToNodeId: null,
    zoomToPaths: false,
    clearZoomRequest: jest.fn(),
    clearZoomToPathsRequest: jest.fn(),
  })),
}));

// Mock D3 completely to avoid ES module issues in Jest
jest.mock('d3', () => ({
  select: jest.fn(() => ({
    selectAll: jest.fn().mockReturnThis(),
    attr: jest.fn().mockReturnThis(),
    append: jest.fn().mockReturnThis(),
    call: jest.fn().mockReturnThis(),
    datum: jest.fn().mockReturnThis(),
    filter: jest.fn().mockReturnThis(),
    on: jest.fn().mockReturnThis(),
    text: jest.fn().mockReturnThis(),
    style: jest.fn().mockReturnThis(),
  })),
  zoom: jest.fn(() => ({
    scaleExtent: jest.fn().mockReturnThis(),
    on: jest.fn().mockReturnThis(),
  })),
  zoomIdentity: {
    translate: jest.fn().mockReturnThis(),
    scale: jest.fn().mockReturnThis(),
  },
  forceSimulation: jest.fn(() => ({
    force: jest.fn().mockReturnThis(),
    alphaDecay: jest.fn().mockReturnThis(),
    on: jest.fn().mockReturnThis(),
    stop: jest.fn(),
    restart: jest.fn(),
    alphaTarget: jest.fn().mockReturnThis(),
  })),
  forceManyBody: jest.fn(() => ({
    strength: jest.fn().mockReturnThis(),
  })),
  forceCenter: jest.fn(() => ({})),
  forceCollide: jest.fn(() => ({
    radius: jest.fn().mockReturnThis(),
  })),
  forceLink: jest.fn(() => ({
    id: jest.fn().mockReturnThis(),
    distance: jest.fn().mockReturnThis(),
    strength: jest.fn().mockReturnThis(),
  })),
  forceX: jest.fn(() => ({
    strength: jest.fn().mockReturnThis(),
  })),
  forceY: jest.fn(() => ({
    strength: jest.fn().mockReturnThis(),
  })),
  drag: jest.fn(() => ({
    on: jest.fn().mockReturnThis(),
  })),
}));

// Mock MechanismGraph to avoid complex D3 rendering in tests
jest.mock('./MechanismGraph', () => {
  return function MockMechanismGraph({ layoutMode, physicsSettings, data }: any) {
    return (
      <svg data-testid="mechanism-graph">
        <g data-testid="layout-mode">{layoutMode}</g>
        {physicsSettings && (
          <g data-testid="physics-settings">{JSON.stringify(physicsSettings)}</g>
        )}
        {data.nodes.map((node: any) => (
          <g key={node.id} className="node" data-testid={`node-${node.id}`}>
            <text>{node.label}</text>
          </g>
        ))}
      </svg>
    );
  };
});

// Re-import after mocking
import MechanismGraph from '../../../src/visualizations/MechanismGraph';

describe('MechanismGraph', () => {
  const mockData: SystemsNetwork = {
    nodes: [
      {
        id: 'node1',
        label: 'Test Node 1',
        weight: 1,
        category: 'economic',
        stockType: 'structural',
        scale: 1,
        connections: { incoming: 0, outgoing: 1 },
      },
      {
        id: 'node2',
        label: 'Test Node 2',
        weight: 1,
        category: 'social_environment',
        stockType: 'proxy',
        scale: 3,
        connections: { incoming: 1, outgoing: 1 },
      },
      {
        id: 'node3',
        label: 'Test Node 3',
        weight: 1,
        category: 'biological',
        stockType: 'crisis',
        scale: 7,
        connections: { incoming: 1, outgoing: 0 },
      },
    ],
    edges: [
      {
        id: 'edge1',
        source: 'node1',
        target: 'node2',
        strength: 0.5,
        direction: 'positive',
        evidenceQuality: 'B',
        studyCount: 5,
      },
      {
        id: 'edge2',
        source: 'node2',
        target: 'node3',
        strength: 0.7,
        direction: 'positive',
        evidenceQuality: 'A',
        studyCount: 10,
      },
    ],
  };

  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe('Hierarchical Layout (Default)', () => {
    it('renders with hierarchical layout by default', () => {
      const { container } = render(<MechanismGraph data={mockData} />);
      const svg = container.querySelector('svg');
      expect(svg).toBeInTheDocument();
    });

    it('displays level labels in hierarchical mode', async () => {
      const { container } = render(
        <MechanismGraph data={mockData} layoutMode="hierarchical" />
      );

      await waitFor(() => {
        const labels = container.querySelectorAll('text');
        const labelTexts = Array.from(labels).map((l) => l.textContent);
        expect(labelTexts).toContain('Structural\nDeterminants');
      });
    });

    it('positions nodes in vertical columns by scale', async () => {
      const { container } = render(
        <MechanismGraph data={mockData} layoutMode="hierarchical" />
      );

      await waitFor(() => {
        const nodeGroups = container.querySelectorAll('g.node');
        expect(nodeGroups.length).toBe(3);
      });
    });

    it('does not initialize force simulation in hierarchical mode', () => {
      const d3 = require('d3');
      render(<MechanismGraph data={mockData} layoutMode="hierarchical" />);
      expect(d3.forceSimulation).not.toHaveBeenCalled();
    });
  });

  describe('Force-Directed Layout', () => {
    it('initializes force simulation when layoutMode is force-directed', async () => {
      const d3 = require('d3');
      render(<MechanismGraph data={mockData} layoutMode="force-directed" />);

      await waitFor(() => {
        expect(d3.forceSimulation).toHaveBeenCalled();
      });
    });

    it('does not display level labels in force-directed mode', async () => {
      const { container } = render(
        <MechanismGraph data={mockData} layoutMode="force-directed" />
      );

      await waitFor(() => {
        const labels = container.querySelectorAll('text');
        const labelTexts = Array.from(labels).map((l) => l.textContent);
        expect(labelTexts).not.toContain('Structural\nDeterminants');
      });
    });

    it('applies default physics settings when none provided', async () => {
      const d3 = require('d3');
      render(<MechanismGraph data={mockData} layoutMode="force-directed" />);

      await waitFor(() => {
        const simulation = d3.forceSimulation.mock.results[0].value;
        expect(simulation.force).toHaveBeenCalledWith('charge', expect.anything());
        expect(simulation.force).toHaveBeenCalledWith('collision', expect.anything());
      });
    });

    it('applies custom physics settings when provided', async () => {
      const customSettings: PhysicsSettings = {
        charge: -500,
        linkDistance: 200,
        gravity: 0.1,
        collision: 30,
      };

      const d3 = require('d3');
      render(
        <MechanismGraph
          data={mockData}
          layoutMode="force-directed"
          physicsSettings={customSettings}
        />
      );

      await waitFor(() => {
        expect(d3.forceSimulation).toHaveBeenCalled();
      });
    });

    it('enables drag behavior on nodes in force-directed mode', async () => {
      const d3 = require('d3');
      render(
        <MechanismGraph data={mockData} layoutMode="force-directed" />
      );

      await waitFor(() => {
        expect(d3.drag).toHaveBeenCalled();
      });
    });

    it('stops simulation on unmount', () => {
      const d3 = require('d3');
      const { unmount } = render(
        <MechanismGraph data={mockData} layoutMode="force-directed" />
      );

      const simulation = d3.forceSimulation.mock.results[0]?.value;
      unmount();

      expect(simulation?.stop).toHaveBeenCalled();
    });

    it('restarts simulation when physics settings change', async () => {
      const d3 = require('d3');
      const { rerender } = render(
        <MechanismGraph
          data={mockData}
          layoutMode="force-directed"
          physicsSettings={{ charge: -300, linkDistance: 150, gravity: 0.05, collision: 20 }}
        />
      );

      await waitFor(() => {
        expect(d3.forceSimulation).toHaveBeenCalledTimes(1);
      });

      // Change physics settings
      rerender(
        <MechanismGraph
          data={mockData}
          layoutMode="force-directed"
          physicsSettings={{ charge: -500, linkDistance: 200, gravity: 0.1, collision: 30 }}
        />
      );

      await waitFor(() => {
        // Should create a new simulation
        expect(d3.forceSimulation).toHaveBeenCalledTimes(2);
      });
    });
  });

  describe('Layout Mode Switching', () => {
    it('switches from hierarchical to force-directed', async () => {
      const d3 = require('d3');
      const { rerender } = render(
        <MechanismGraph data={mockData} layoutMode="hierarchical" />
      );

      expect(d3.forceSimulation).not.toHaveBeenCalled();

      rerender(<MechanismGraph data={mockData} layoutMode="force-directed" />);

      await waitFor(() => {
        expect(d3.forceSimulation).toHaveBeenCalled();
      });
    });

    it('switches from force-directed to hierarchical', async () => {
      const d3 = require('d3');
      const { rerender, container } = render(
        <MechanismGraph data={mockData} layoutMode="force-directed" />
      );

      await waitFor(() => {
        expect(d3.forceSimulation).toHaveBeenCalled();
      });

      const simulation = d3.forceSimulation.mock.results[0]?.value;

      rerender(<MechanismGraph data={mockData} layoutMode="hierarchical" />);

      await waitFor(() => {
        expect(simulation?.stop).toHaveBeenCalled();
        const labels = container.querySelectorAll('text');
        const labelTexts = Array.from(labels).map((l) => l.textContent);
        expect(labelTexts).toContain('Structural\nDeterminants');
      });
    });
  });

  describe('Node Interactions', () => {
    it('calls onNodeClick when node is clicked', async () => {
      const handleNodeClick = jest.fn();
      const { container } = render(
        <MechanismGraph data={mockData} onNodeClick={handleNodeClick} />
      );

      await waitFor(() => {
        const nodeGroups = container.querySelectorAll('g.node');
        expect(nodeGroups.length).toBeGreaterThan(0);
      });

      const firstNode = container.querySelector('g.node');
      if (firstNode) {
        fireEvent.click(firstNode);
        expect(handleNodeClick).toHaveBeenCalledWith(
          expect.objectContaining({ id: 'node1' })
        );
      }
    });

    it('displays nodes with correct accessibility attributes', async () => {
      const { container } = render(<MechanismGraph data={mockData} />);

      await waitFor(() => {
        const nodeGroups = container.querySelectorAll('g.node');
        nodeGroups.forEach((node) => {
          expect(node).toHaveAttribute('role', 'button');
          expect(node).toHaveAttribute('tabindex', '0');
          expect(node).toHaveAttribute('aria-label');
        });
      });
    });
  });

  describe('Compatibility with Other Features', () => {
    it('works with importantNodes highlighting', async () => {
      const importantNodes = {
        nodeIds: ['node1'],
        ranks: { node1: 1 },
      };

      const { container } = render(
        <MechanismGraph data={mockData} importantNodes={importantNodes} />
      );

      await waitFor(() => {
        const importantNode = container.querySelector('.important-node');
        expect(importantNode).toBeInTheDocument();
      });
    });

    it('works with activePaths highlighting', async () => {
      const activePaths = {
        paths: [
          {
            pathId: 'path1',
            nodeIds: ['node1', 'node2'],
            edgeIds: ['edge1'],
          },
        ],
      };

      const { container } = render(
        <MechanismGraph data={mockData} activePaths={activePaths} />
      );

      await waitFor(() => {
        const pathNodes = container.querySelectorAll('.in-path');
        expect(pathNodes.length).toBeGreaterThan(0);
      });
    });

    it('works with crisisHighlight', async () => {
      const crisisHighlight = {
        nodeIdToDegree: new Map([['node3', 0]]),
        policyLeverIds: new Set(['node1']),
      };

      const { container } = render(
        <MechanismGraph data={mockData} crisisHighlight={crisisHighlight} />
      );

      await waitFor(() => {
        const crisisNode = container.querySelector('.crisis-node');
        expect(crisisNode).toBeInTheDocument();
      });
    });

    it('works with all highlighting features simultaneously in force-directed mode', async () => {
      const importantNodes = { nodeIds: ['node1'], ranks: { node1: 1 } };
      const activePaths = {
        paths: [{ pathId: 'path1', nodeIds: ['node2'], edgeIds: ['edge1'] }],
      };
      const crisisHighlight = {
        nodeIdToDegree: new Map([['node3', 0]]),
        policyLeverIds: new Set(['node1']),
      };

      const { container } = render(
        <MechanismGraph
          data={mockData}
          layoutMode="force-directed"
          importantNodes={importantNodes}
          activePaths={activePaths}
          crisisHighlight={crisisHighlight}
        />
      );

      await waitFor(() => {
        expect(container.querySelector('.important-node')).toBeInTheDocument();
        expect(container.querySelector('.in-path')).toBeInTheDocument();
        expect(container.querySelector('.crisis-node')).toBeInTheDocument();
      });
    });
  });

  describe('Edge Cases', () => {
    it('handles empty data gracefully', () => {
      const emptyData: SystemsNetwork = { nodes: [], edges: [] };
      const { container } = render(<MechanismGraph data={emptyData} />);
      const svg = container.querySelector('svg');
      expect(svg).toBeInTheDocument();
    });

    it('handles single node without edges', async () => {
      const singleNodeData: SystemsNetwork = {
        nodes: [
          {
            id: 'node1',
            label: 'Lonely Node',
            weight: 1,
            category: 'economic',
            stockType: 'structural',
            scale: 1,
            connections: { incoming: 0, outgoing: 0 },
          },
        ],
        edges: [],
      };

      const { container } = render(<MechanismGraph data={singleNodeData} />);
      await waitFor(() => {
        const nodeGroups = container.querySelectorAll('g.node');
        expect(nodeGroups.length).toBe(1);
      });
    });

    it('handles layout mode changes rapidly', async () => {
      const { rerender } = render(
        <MechanismGraph data={mockData} layoutMode="hierarchical" />
      );

      // Rapid switches
      rerender(<MechanismGraph data={mockData} layoutMode="force-directed" />);
      rerender(<MechanismGraph data={mockData} layoutMode="hierarchical" />);
      rerender(<MechanismGraph data={mockData} layoutMode="force-directed" />);

      await waitFor(() => {
        const d3 = require('d3');
        expect(d3.forceSimulation).toHaveBeenCalled();
      });
    });
  });
});
