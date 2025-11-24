import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import { SystemsMapView } from './SystemsMapView';

// Mock hooks
jest.mock('../hooks/useData', () => ({
  useGraphData: jest.fn().mockReturnValue({
    data: {
      nodes: [
        {
          id: 'node1',
          label: 'Test Node 1',
          category: 'built_environment',
          scale: 1,
          stockType: 'structural',
          weight: 1,
          connections: { incoming: 0, outgoing: 1 },
        },
        {
          id: 'node2',
          label: 'Test Node 2',
          category: 'behavioral',
          scale: 5,
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
    },
    isLoading: false,
    error: null,
  }),
  useMechanismById: jest.fn().mockReturnValue({
    data: null,
    isLoading: false,
    error: null,
  }),
}));

// Mock MechanismGraph component
jest.mock('../visualizations/MechanismGraph', () => {
  return function MockMechanismGraph({
    layoutMode,
    physicsSettings,
    data,
    onNodeClick,
    onEdgeClick,
  }: any) {
    return (
      <div data-testid="mechanism-graph">
        <div data-testid="layout-mode">{layoutMode}</div>
        {physicsSettings && (
          <div data-testid="physics-settings">
            <div data-testid="charge">{physicsSettings.charge}</div>
            <div data-testid="linkDistance">{physicsSettings.linkDistance}</div>
            <div data-testid="gravity">{physicsSettings.gravity}</div>
            <div data-testid="collision">{physicsSettings.collision}</div>
          </div>
        )}
        <div data-testid="node-count">{data.nodes.length}</div>
        <button
          data-testid="mock-node-click"
          onClick={() => onNodeClick && onNodeClick('node1')}
        >
          Click Node
        </button>
        <button
          data-testid="mock-edge-click"
          onClick={() => onEdgeClick && onEdgeClick('mech1')}
        >
          Click Edge
        </button>
      </div>
    );
  };
});

// Mock ResizeObserver
global.ResizeObserver = class ResizeObserver {
  observe() {}
  unobserve() {}
  disconnect() {}
} as any;

describe('SystemsMapView', () => {
  const renderWithRouter = (component: React.ReactElement) => {
    return render(<BrowserRouter>{component}</BrowserRouter>);
  };

  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe('Layout Mode Toggle', () => {
    it('renders with hierarchical layout by default', () => {
      renderWithRouter(<SystemsMapView />);

      const layoutMode = screen.getByTestId('layout-mode');
      expect(layoutMode).toHaveTextContent('hierarchical');
    });

    it('displays both layout toggle buttons', () => {
      renderWithRouter(<SystemsMapView />);

      expect(screen.getByText('Hierarchical')).toBeInTheDocument();
      expect(screen.getByText('Force-Directed')).toBeInTheDocument();
    });

    it('switches to force-directed layout when button is clicked', () => {
      renderWithRouter(<SystemsMapView />);

      const forceButton = screen.getByText('Force-Directed');
      fireEvent.click(forceButton);

      const layoutMode = screen.getByTestId('layout-mode');
      expect(layoutMode).toHaveTextContent('force-directed');
    });

    it('switches back to hierarchical layout when button is clicked', () => {
      renderWithRouter(<SystemsMapView />);

      // Switch to force-directed
      const forceButton = screen.getByText('Force-Directed');
      fireEvent.click(forceButton);

      // Switch back to hierarchical
      const hierarchicalButton = screen.getByText('Hierarchical');
      fireEvent.click(hierarchicalButton);

      const layoutMode = screen.getByTestId('layout-mode');
      expect(layoutMode).toHaveTextContent('hierarchical');
    });

    it('applies active styling to selected layout button', () => {
      renderWithRouter(<SystemsMapView />);

      const hierarchicalButton = screen.getByText('Hierarchical');
      expect(hierarchicalButton).toHaveClass('bg-white');

      const forceButton = screen.getByText('Force-Directed');
      fireEvent.click(forceButton);

      expect(forceButton).toHaveClass('bg-white');
    });
  });

  describe('Physics Settings Panel', () => {
    it('does not show physics settings in hierarchical mode', () => {
      renderWithRouter(<SystemsMapView />);

      expect(screen.queryByTestId('physics-settings')).not.toBeInTheDocument();
    });

    it('shows physics settings when in force-directed mode', () => {
      renderWithRouter(<SystemsMapView />);

      const forceButton = screen.getByText('Force-Directed');
      fireEvent.click(forceButton);

      // Open the details/summary element
      const physicsToggle = screen.getByText('Physics Settings');
      fireEvent.click(physicsToggle);

      // Should show physics sliders
      expect(screen.getByText(/Repulsion/)).toBeInTheDocument();
      expect(screen.getByText(/Link Distance/)).toBeInTheDocument();
      expect(screen.getByText(/Gravity/)).toBeInTheDocument();
      expect(screen.getByText(/Collision Buffer/)).toBeInTheDocument();
    });

    it('initializes physics settings with default values', () => {
      renderWithRouter(<SystemsMapView />);

      const forceButton = screen.getByText('Force-Directed');
      fireEvent.click(forceButton);

      const charge = screen.getByTestId('charge');
      const linkDistance = screen.getByTestId('linkDistance');
      const gravity = screen.getByTestId('gravity');
      const collision = screen.getByTestId('collision');

      expect(charge).toHaveTextContent('-300');
      expect(linkDistance).toHaveTextContent('150');
      expect(gravity).toHaveTextContent('0.05');
      expect(collision).toHaveTextContent('20');
    });

    it('updates charge (repulsion) setting when slider changes', () => {
      renderWithRouter(<SystemsMapView />);

      const forceButton = screen.getByText('Force-Directed');
      fireEvent.click(forceButton);

      // Open physics settings
      const physicsToggle = screen.getByText('Physics Settings');
      fireEvent.click(physicsToggle);

      // Find and change repulsion slider
      const repulsionSlider = screen.getByLabelText(/Repulsion/i);
      fireEvent.change(repulsionSlider, { target: { value: '-500' } });

      const charge = screen.getByTestId('charge');
      expect(charge).toHaveTextContent('-500');
    });

    it('updates link distance setting when slider changes', () => {
      renderWithRouter(<SystemsMapView />);

      const forceButton = screen.getByText('Force-Directed');
      fireEvent.click(forceButton);

      const physicsToggle = screen.getByText('Physics Settings');
      fireEvent.click(physicsToggle);

      const linkSlider = screen.getByLabelText(/Link Distance/i);
      fireEvent.change(linkSlider, { target: { value: '200' } });

      const linkDistance = screen.getByTestId('linkDistance');
      expect(linkDistance).toHaveTextContent('200');
    });

    it('updates gravity setting when slider changes', () => {
      renderWithRouter(<SystemsMapView />);

      const forceButton = screen.getByText('Force-Directed');
      fireEvent.click(forceButton);

      const physicsToggle = screen.getByText('Physics Settings');
      fireEvent.click(physicsToggle);

      const gravitySlider = screen.getByLabelText(/Gravity/i);
      fireEvent.change(gravitySlider, { target: { value: '0.1' } });

      const gravity = screen.getByTestId('gravity');
      expect(gravity).toHaveTextContent('0.1');
    });

    it('updates collision buffer setting when slider changes', () => {
      renderWithRouter(<SystemsMapView />);

      const forceButton = screen.getByText('Force-Directed');
      fireEvent.click(forceButton);

      const physicsToggle = screen.getByText('Physics Settings');
      fireEvent.click(physicsToggle);

      const collisionSlider = screen.getByLabelText(/Collision/i);
      fireEvent.change(collisionSlider, { target: { value: '30' } });

      const collision = screen.getByTestId('collision');
      expect(collision).toHaveTextContent('30');
    });

    it('does not pass physics settings to graph in hierarchical mode', () => {
      renderWithRouter(<SystemsMapView />);

      expect(screen.queryByTestId('physics-settings')).not.toBeInTheDocument();
    });

    it('passes physics settings to graph in force-directed mode', () => {
      renderWithRouter(<SystemsMapView />);

      const forceButton = screen.getByText('Force-Directed');
      fireEvent.click(forceButton);

      expect(screen.getByTestId('physics-settings')).toBeInTheDocument();
    });
  });

  describe('Graph Integration', () => {
    it('renders MechanismGraph component', () => {
      renderWithRouter(<SystemsMapView />);

      expect(screen.getByTestId('mechanism-graph')).toBeInTheDocument();
    });

    it('passes correct data to MechanismGraph', () => {
      renderWithRouter(<SystemsMapView />);

      const nodeCount = screen.getByTestId('node-count');
      expect(nodeCount).toHaveTextContent('2');
    });

    it('handles node click events', () => {
      renderWithRouter(<SystemsMapView />);

      const mockButton = screen.getByTestId('mock-node-click');
      fireEvent.click(mockButton);

      // Node details panel should appear or update (implementation dependent)
      // This is a basic smoke test
      expect(mockButton).toBeInTheDocument();
    });

    it('handles edge click events', () => {
      renderWithRouter(<SystemsMapView />);

      const mockButton = screen.getByTestId('mock-edge-click');
      fireEvent.click(mockButton);

      // Edge details should appear or update (implementation dependent)
      // This is a basic smoke test
      expect(mockButton).toBeInTheDocument();
    });
  });

  describe('State Persistence', () => {
    it('maintains layout mode when component re-renders', () => {
      const { rerender } = renderWithRouter(<SystemsMapView />);

      const forceButton = screen.getByText('Force-Directed');
      fireEvent.click(forceButton);

      rerender(
        <BrowserRouter>
          <SystemsMapView />
        </BrowserRouter>
      );

      const layoutMode = screen.getByTestId('layout-mode');
      expect(layoutMode).toHaveTextContent('force-directed');
    });

    it('maintains physics settings when sliders are adjusted', () => {
      renderWithRouter(<SystemsMapView />);

      const forceButton = screen.getByText('Force-Directed');
      fireEvent.click(forceButton);

      const physicsToggle = screen.getByText('Physics Settings');
      fireEvent.click(physicsToggle);

      const repulsionSlider = screen.getByLabelText(/Repulsion/i);
      fireEvent.change(repulsionSlider, { target: { value: '-600' } });

      const charge = screen.getByTestId('charge');
      expect(charge).toHaveTextContent('-600');
    });
  });
});
