import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';

// Mock filterByMinConnections to pass through data without filtering
jest.mock('../utils/graphBuilder', () => ({
  ...jest.requireActual('../utils/graphBuilder'),
  filterByMinConnections: (data: any) => data,
}));

// Mock the hooks module - use simple function mocks that return data directly
jest.mock('../hooks/useData', () => ({
  __esModule: true,
  useGraphData: () => ({
    data: {
      nodes: [
        { id: 'node1', label: 'Test Node 1', category: 'built_environment', scale: 1, stockType: 'structural', weight: 1, connections: { incoming: 0, outgoing: 1 } },
        { id: 'node2', label: 'Test Node 2', category: 'behavioral', scale: 5, stockType: 'structural', weight: 1, connections: { incoming: 1, outgoing: 0 } },
        { id: 'node3', label: 'Test Node 3', category: 'economic', scale: 4, stockType: 'structural', weight: 1, connections: { incoming: 1, outgoing: 1 } },
      ],
      edges: [
        { id: 'mech1', source: 'node1', target: 'node2', direction: 'positive', evidenceQuality: 'A', strength: 3, studyCount: 5 },
        { id: 'mech2', source: 'node2', target: 'node3', direction: 'negative', evidenceQuality: 'B', strength: 2, studyCount: 3 },
      ],
    },
    isLoading: false,
    error: null,
  }),
  useGraphDataWithCanonicalNodes: () => ({
    data: {
      nodes: [
        { id: 'node1', label: 'Test Node 1', category: 'built_environment', scale: 1, stockType: 'structural', weight: 1, connections: { incoming: 0, outgoing: 1 } },
        { id: 'node2', label: 'Test Node 2', category: 'behavioral', scale: 5, stockType: 'structural', weight: 1, connections: { incoming: 1, outgoing: 0 } },
        { id: 'node3', label: 'Test Node 3', category: 'economic', scale: 4, stockType: 'structural', weight: 1, connections: { incoming: 1, outgoing: 1 } },
      ],
      edges: [
        { id: 'mech1', source: 'node1', target: 'node2', direction: 'positive', evidenceQuality: 'A', strength: 3, studyCount: 5 },
        { id: 'mech2', source: 'node2', target: 'node3', direction: 'negative', evidenceQuality: 'B', strength: 2, studyCount: 3 },
      ],
    },
    isLoading: false,
    error: null,
  }),
  useMechanismById: () => ({
    data: {
      id: 'mech1',
      name: 'Test Mechanism',
      from_node_id: 'node1',
      from_node_name: 'Test Node 1',
      to_node_id: 'node2',
      to_node_name: 'Test Node 2',
      direction: 'positive',
      category: 'built_environment',
      description: 'This is a test mechanism description.',
      evidence_quality: 'A',
      n_studies: 5,
      citations: [
        { id: 'cite1', authors: 'Smith et al.', year: 2023, title: 'Test Citation', journal: 'Journal of Testing', doi: '10.1234/test', url: 'https://example.com/test' },
      ],
    },
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
    selectedNodeId,
    selectedEdgeId,
  }: any) {
    return (
      <div data-testid="mechanism-graph">
        <div data-testid="layout-mode">{layoutMode}</div>
        <div data-testid="selected-node-id">{selectedNodeId || 'none'}</div>
        <div data-testid="selected-edge-id">{selectedEdgeId || 'none'}</div>
        {physicsSettings && (
          <div data-testid="physics-settings">
            <div data-testid="charge">{physicsSettings.charge}</div>
            <div data-testid="linkDistance">{physicsSettings.linkDistance}</div>
            <div data-testid="gravity">{physicsSettings.gravity}</div>
            <div data-testid="collision">{physicsSettings.collision}</div>
          </div>
        )}
        <div data-testid="node-count">{data.nodes.length}</div>
        {/* Node click buttons */}
        {data.nodes.map((node: any) => (
          <button
            key={node.id}
            data-testid={`mock-node-click-${node.id}`}
            onClick={() => onNodeClick && onNodeClick(node)}
          >
            Click {node.label}
          </button>
        ))}
        {/* Edge click buttons */}
        {data.edges.map((edge: any) => (
          <button
            key={edge.id}
            data-testid={`mock-edge-click-${edge.id}`}
            onClick={() => onEdgeClick && onEdgeClick(edge)}
          >
            Click Edge {edge.id}
          </button>
        ))}
      </div>
    );
  };
});

// Import component after mocks are defined
import { SystemsMapView } from './SystemsMapView';

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

      // Find slider by its value (charge starts at -300)
      const sliders = screen.getAllByRole('slider');
      const repulsionSlider = sliders[0]; // First slider is Repulsion
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

      const sliders = screen.getAllByRole('slider');
      const linkSlider = sliders[1]; // Second slider is Link Distance
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

      const sliders = screen.getAllByRole('slider');
      const gravitySlider = sliders[2]; // Third slider is Gravity
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

      const sliders = screen.getAllByRole('slider');
      const collisionSlider = sliders[3]; // Fourth slider is Collision Buffer
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
      expect(nodeCount).toHaveTextContent('3');
    });

    it('handles node click events and shows node panel', () => {
      renderWithRouter(<SystemsMapView />);

      const mockButton = screen.getByTestId('mock-node-click-node1');
      fireEvent.click(mockButton);

      // Node details panel should appear with node title
      expect(screen.getByText('Test Node 1')).toBeInTheDocument();
      // Selected node should be passed to graph
      expect(screen.getByTestId('selected-node-id')).toHaveTextContent('node1');
    });

    it('handles edge click events and shows mechanism panel', () => {
      renderWithRouter(<SystemsMapView />);

      const mockButton = screen.getByTestId('mock-edge-click-mech1');
      fireEvent.click(mockButton);

      // Mechanism details panel should appear
      expect(screen.getByText('Mechanism Detail')).toBeInTheDocument();
      // Selected edge should be passed to graph
      expect(screen.getByTestId('selected-edge-id')).toHaveTextContent('mech1');
    });
  });

  describe('Panel Navigation', () => {
    it('shows node panel when clicking a node', () => {
      renderWithRouter(<SystemsMapView />);

      fireEvent.click(screen.getByTestId('mock-node-click-node1'));

      // Panel should show with node title
      expect(screen.getByRole('complementary')).toBeInTheDocument();
      expect(screen.getByText('Test Node 1')).toBeInTheDocument();
    });

    it('shows mechanism panel with back button when navigating from node panel', async () => {
      renderWithRouter(<SystemsMapView />);

      // Click node to open node panel
      fireEvent.click(screen.getByTestId('mock-node-click-node1'));
      expect(screen.getByText('Test Node 1')).toBeInTheDocument();

      // Node panel should show mechanisms with actual node labels
      // Look for the mechanism item that shows "Test Node 1 → Test Node 2"
      const mechanismItem = screen.getByText(/Test Node 1 → Test Node 2/);
      expect(mechanismItem).toBeInTheDocument();

      // Click on mechanism in node panel
      fireEvent.click(mechanismItem.closest('div[role="button"]') || mechanismItem);

      // Should now show mechanism detail panel with back button
      expect(screen.getByText('Mechanism Detail')).toBeInTheDocument();
      expect(screen.getByLabelText('Go back')).toBeInTheDocument();
    });

    it('does not show back button when mechanism clicked directly on graph', () => {
      renderWithRouter(<SystemsMapView />);

      // Click edge directly on graph (not from node panel)
      fireEvent.click(screen.getByTestId('mock-edge-click-mech1'));

      // Should show mechanism panel without back button
      expect(screen.getByText('Mechanism Detail')).toBeInTheDocument();
      expect(screen.queryByLabelText('Go back')).not.toBeInTheDocument();
    });

    it('returns to node panel when clicking back button', async () => {
      renderWithRouter(<SystemsMapView />);

      // Click node to open node panel
      fireEvent.click(screen.getByTestId('mock-node-click-node1'));

      // Click on mechanism in node panel
      const mechanismItem = screen.getByText(/Test Node 1 → Test Node 2/);
      fireEvent.click(mechanismItem.closest('div[role="button"]') || mechanismItem);

      // Verify we're in mechanism panel
      expect(screen.getByText('Mechanism Detail')).toBeInTheDocument();

      // Click back button
      fireEvent.click(screen.getByLabelText('Go back'));

      // Should return to node panel
      expect(screen.getByText('Test Node 1')).toBeInTheDocument();
      expect(screen.queryByText('Mechanism Detail')).not.toBeInTheDocument();
    });

    it('highlights edge when mechanism is selected from node panel', () => {
      renderWithRouter(<SystemsMapView />);

      // Click node to open node panel
      fireEvent.click(screen.getByTestId('mock-node-click-node1'));

      // Click on mechanism in node panel
      const mechanismItem = screen.getByText(/Test Node 1 → Test Node 2/);
      fireEvent.click(mechanismItem.closest('div[role="button"]') || mechanismItem);

      // Edge should be highlighted in graph
      expect(screen.getByTestId('selected-edge-id')).toHaveTextContent('mech1');
    });

    it('shows clickable from/to nodes in mechanism panel', () => {
      renderWithRouter(<SystemsMapView />);

      // Click edge to open mechanism panel
      fireEvent.click(screen.getByTestId('mock-edge-click-mech1'));

      // From and To nodes should be clickable buttons (use title to distinguish from mock buttons)
      const sourceButton = screen.getByTitle('View details for Test Node 1');
      const targetButton = screen.getByTitle('View details for Test Node 2');

      expect(sourceButton).toBeInTheDocument();
      expect(targetButton).toBeInTheDocument();
    });

    it('navigates to source node when clicking from node in mechanism panel', () => {
      renderWithRouter(<SystemsMapView />);

      // Click edge to open mechanism panel
      fireEvent.click(screen.getByTestId('mock-edge-click-mech1'));

      // Click on source node button
      const sourceButton = screen.getByTitle('View details for Test Node 1');
      fireEvent.click(sourceButton);

      // Should navigate to node panel for source node
      expect(screen.getByTestId('selected-node-id')).toHaveTextContent('node1');
      // Mechanism panel should be gone, node panel should show
      expect(screen.queryByText('Mechanism Detail')).not.toBeInTheDocument();
    });

    it('navigates to target node when clicking to node in mechanism panel', () => {
      renderWithRouter(<SystemsMapView />);

      // Click edge to open mechanism panel
      fireEvent.click(screen.getByTestId('mock-edge-click-mech1'));

      // Click on target node button
      const targetButton = screen.getByTitle('View details for Test Node 2');
      fireEvent.click(targetButton);

      // Should navigate to node panel for target node
      expect(screen.getByTestId('selected-node-id')).toHaveTextContent('node2');
    });

    it('closes panel when clicking close button', () => {
      renderWithRouter(<SystemsMapView />);

      // Open node panel
      fireEvent.click(screen.getByTestId('mock-node-click-node1'));
      expect(screen.getByRole('complementary')).toBeInTheDocument();

      // Click close button
      fireEvent.click(screen.getByLabelText('Close panel'));

      // Panel should be closed
      expect(screen.queryByRole('complementary')).not.toBeInTheDocument();
    });

    it('clears selection state when closing panel', () => {
      renderWithRouter(<SystemsMapView />);

      // Open node panel
      fireEvent.click(screen.getByTestId('mock-node-click-node1'));
      expect(screen.getByTestId('selected-node-id')).toHaveTextContent('node1');

      // Close panel
      fireEvent.click(screen.getByLabelText('Close panel'));

      // Selection should be cleared
      expect(screen.getByTestId('selected-node-id')).toHaveTextContent('none');
      expect(screen.getByTestId('selected-edge-id')).toHaveTextContent('none');
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

      const sliders = screen.getAllByRole('slider');
      const repulsionSlider = sliders[0]; // First slider is Repulsion
      fireEvent.change(repulsionSlider, { target: { value: '-600' } });

      const charge = screen.getByTestId('charge');
      expect(charge).toHaveTextContent('-600');
    });
  });
});
