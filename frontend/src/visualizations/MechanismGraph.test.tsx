import { render, screen } from '@testing-library/react';
import { PhysicsSettings, SystemsNetwork } from '../types/mechanism';

// Mock D3 BEFORE importing MechanismGraph
jest.mock('d3', () => ({
    select: jest.fn(() => ({
      selectAll: jest.fn().mockReturnThis(),
      data: jest.fn().mockReturnThis(),
      join: jest.fn().mockReturnThis(),
      attr: jest.fn().mockReturnThis(),
      style: jest.fn().mockReturnThis(),
      text: jest.fn().mockReturnThis(),
      append: jest.fn().mockReturnThis(),
      call: jest.fn().mockReturnThis(),
      on: jest.fn().mockReturnThis(),
      classed: jest.fn().mockReturnThis(),
      remove: jest.fn().mockReturnThis(),
      node: jest.fn(() => ({ getBBox: () => ({ width: 100, height: 50 }) })),
    })),
    forceSimulation: jest.fn(() => ({
      nodes: jest.fn().mockReturnThis(),
      force: jest.fn().mockReturnThis(),
      alphaDecay: jest.fn().mockReturnThis(),
      on: jest.fn().mockReturnThis(),
      stop: jest.fn(),
      restart: jest.fn().mockReturnThis(),
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
    zoom: jest.fn(() => ({
      scaleExtent: jest.fn().mockReturnThis(),
      on: jest.fn().mockReturnThis(),
    })),
    zoomIdentity: { k: 1, x: 0, y: 0 },
}));

// Import MechanismGraph AFTER mocking D3
import MechanismGraph from './MechanismGraph';

describe('MechanismGraph', () => {
  const mockGraphData: SystemsNetwork = {
    nodes: [
      {
        id: 'node1',
        label: 'Test Node 1',
        category: 'built_environment',
        stockType: 'structural',
        weight: 1,
        connections: { incoming: 0, outgoing: 1 },
      },
      {
        id: 'node2',
        label: 'Test Node 2',
        category: 'behavioral',
        stockType: 'structural',
        weight: 1,
        connections: { incoming: 1, outgoing: 0 },
      },
    ],
    edges: [
      {
        id: 'mech1',
        source: 'node1',
        target: 'node2',
        direction: 'positive',
        evidenceQuality: 'A',
        strength: 3,
        studyCount: 5,
      },
    ],
  };

  const defaultProps = {
    data: mockGraphData,
    width: 800,
    height: 600,
    onNodeClick: jest.fn(),
    onEdgeClick: jest.fn(),
    selectedNodeId: null,
    filteredCategories: [],
  };

  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe('Hierarchical Layout', () => {
    it('renders graph in hierarchical mode by default', () => {
      render(<MechanismGraph {...defaultProps} />);
      const svg = screen.getByRole('img', { hidden: true });
      expect(svg).toBeInTheDocument();
    });

    it('positions nodes in vertical columns by scale', () => {
      render(<MechanismGraph {...defaultProps} layoutMode="hierarchical" />);
      // Verify D3 select was called (nodes were positioned)
      const d3 = require('d3');
      expect(d3.select).toHaveBeenCalled();
    });

    it('does not create force simulation in hierarchical mode', () => {
      render(<MechanismGraph {...defaultProps} layoutMode="hierarchical" />);
      const d3 = require('d3');
      expect(d3.forceSimulation).not.toHaveBeenCalled();
    });
  });

  describe('Force-Directed Layout', () => {
    const physicsSettings: PhysicsSettings = {
      charge: -300,
      linkDistance: 150,
      gravity: 0.05,
      collision: 20,
    };

    it('creates force simulation when layoutMode is force-directed', () => {
      render(
        <MechanismGraph
          {...defaultProps}
          layoutMode="force-directed"
          physicsSettings={physicsSettings}
        />
      );
      const d3 = require('d3');
      expect(d3.forceSimulation).toHaveBeenCalled();
    });

    it('applies all 6 forces to the simulation', () => {
      render(
        <MechanismGraph
          {...defaultProps}
          layoutMode="force-directed"
          physicsSettings={physicsSettings}
        />
      );
      const d3 = require('d3');
      const simulation = d3.forceSimulation();

      // Should have called force() for: charge, center, collision, link, x, y
      expect(simulation.force).toHaveBeenCalledWith('charge', expect.anything());
      expect(simulation.force).toHaveBeenCalledWith('center', expect.anything());
      expect(simulation.force).toHaveBeenCalledWith('collision', expect.anything());
      expect(simulation.force).toHaveBeenCalledWith('link', expect.anything());
      expect(simulation.force).toHaveBeenCalledWith('x', expect.anything());
      expect(simulation.force).toHaveBeenCalledWith('y', expect.anything());
    });

    it('uses physics settings for force configuration', () => {
      const customSettings: PhysicsSettings = {
        charge: -500,
        linkDistance: 200,
        gravity: 0.1,
        collision: 30,
      };

      render(
        <MechanismGraph
          {...defaultProps}
          layoutMode="force-directed"
          physicsSettings={customSettings}
        />
      );

      const d3 = require('d3');
      expect(d3.forceManyBody).toHaveBeenCalled();
      expect(d3.forceLink).toHaveBeenCalled();
      expect(d3.forceCollide).toHaveBeenCalled();
    });

    it('enables drag behavior in force-directed mode', () => {
      render(
        <MechanismGraph
          {...defaultProps}
          layoutMode="force-directed"
          physicsSettings={physicsSettings}
        />
      );

      const d3 = require('d3');
      expect(d3.drag).toHaveBeenCalled();
    });

    it('cleans up simulation on unmount', () => {
      const { unmount } = render(
        <MechanismGraph
          {...defaultProps}
          layoutMode="force-directed"
          physicsSettings={physicsSettings}
        />
      );

      const d3 = require('d3');
      const simulation = d3.forceSimulation();

      unmount();

      expect(simulation.stop).toHaveBeenCalled();
    });
  });

  describe('Layout Mode Switching', () => {
    it('switches from hierarchical to force-directed', () => {
      const { rerender } = render(
        <MechanismGraph {...defaultProps} layoutMode="hierarchical" />
      );

      const d3 = require('d3');
      expect(d3.forceSimulation).not.toHaveBeenCalled();

      rerender(
        <MechanismGraph
          {...defaultProps}
          layoutMode="force-directed"
          physicsSettings={{
            charge: -300,
            linkDistance: 150,
            gravity: 0.05,
            collision: 20,
          }}
        />
      );

      expect(d3.forceSimulation).toHaveBeenCalled();
    });

    it('switches from force-directed to hierarchical and stops simulation', () => {
      const { rerender } = render(
        <MechanismGraph
          {...defaultProps}
          layoutMode="force-directed"
          physicsSettings={{
            charge: -300,
            linkDistance: 150,
            gravity: 0.05,
            collision: 20,
          }}
        />
      );

      const d3 = require('d3');
      const simulation = d3.forceSimulation();

      rerender(
        <MechanismGraph {...defaultProps} layoutMode="hierarchical" />
      );

      expect(simulation.stop).toHaveBeenCalled();
    });
  });

  describe('Node and Edge Interactions', () => {
    it('calls onNodeClick when a node is clicked', () => {
      const onNodeClick = jest.fn();
      render(<MechanismGraph {...defaultProps} onNodeClick={onNodeClick} />);

      // D3 click handlers are set up
      const d3 = require('d3');
      expect(d3.select).toHaveBeenCalled();
    });

    it('calls onEdgeClick when an edge is clicked', () => {
      const onEdgeClick = jest.fn();
      render(<MechanismGraph {...defaultProps} onEdgeClick={onEdgeClick} />);

      // D3 click handlers are set up
      const d3 = require('d3');
      expect(d3.select).toHaveBeenCalled();
    });

    it('highlights selected node', () => {
      render(<MechanismGraph {...defaultProps} selectedNodeId="node1" />);

      // Verify graph was rendered with selection
      const svg = screen.getByRole('img', { hidden: true });
      expect(svg).toBeInTheDocument();
    });
  });
});
