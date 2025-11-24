/**
 * Tests for SystemsMapView with force-directed layout toggle
 */

import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import { SystemsMapView } from '../../../src/views/SystemsMapView';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

// Mock the hooks
jest.mock('../../../src/hooks/useData', () => ({
  useGraphData: jest.fn(() => ({
    data: {
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
      ],
    },
    isLoading: false,
    error: null,
  })),
  useMechanismById: jest.fn(() => ({
    data: null,
    isLoading: false,
  })),
}));

// Mock MechanismGraph component
jest.mock('../visualizations/MechanismGraph', () => {
  return function MockMechanismGraph({ layoutMode, physicsSettings }: any) {
    return (
      <div data-testid="mechanism-graph">
        <div data-testid="layout-mode">{layoutMode}</div>
        {physicsSettings && (
          <div data-testid="physics-settings">
            {JSON.stringify(physicsSettings)}
          </div>
        )}
      </div>
    );
  };
});

describe('SystemsMapView', () => {
  const queryClient = new QueryClient({
    defaultOptions: {
      queries: { retry: false },
    },
  });

  const renderWithProviders = (component: React.ReactElement) => {
    return render(
      <QueryClientProvider client={queryClient}>{component}</QueryClientProvider>
    );
  };

  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe('Layout Toggle UI', () => {
    it('renders layout toggle buttons', () => {
      renderWithProviders(<SystemsMapView />);

      expect(screen.getByText('Layout')).toBeInTheDocument();
      expect(screen.getByText('Hierarchical')).toBeInTheDocument();
      expect(screen.getByText('Force-Directed')).toBeInTheDocument();
    });

    it('starts with hierarchical layout selected by default', () => {
      renderWithProviders(<SystemsMapView />);

      const hierarchicalButton = screen.getByText('Hierarchical');
      expect(hierarchicalButton).toHaveClass('bg-white');
      expect(hierarchicalButton).toHaveClass('shadow-sm');
    });

    it('switches to force-directed layout when button clicked', async () => {
      renderWithProviders(<SystemsMapView />);

      const forceDirectedButton = screen.getByText('Force-Directed');
      fireEvent.click(forceDirectedButton);

      await waitFor(() => {
        expect(forceDirectedButton).toHaveClass('bg-white');
        expect(screen.getByTestId('layout-mode')).toHaveTextContent('force-directed');
      });
    });

    it('switches back to hierarchical layout', async () => {
      renderWithProviders(<SystemsMapView />);

      const forceDirectedButton = screen.getByText('Force-Directed');
      const hierarchicalButton = screen.getByText('Hierarchical');

      // Switch to force-directed
      fireEvent.click(forceDirectedButton);
      await waitFor(() => {
        expect(screen.getByTestId('layout-mode')).toHaveTextContent('force-directed');
      });

      // Switch back to hierarchical
      fireEvent.click(hierarchicalButton);
      await waitFor(() => {
        expect(screen.getByTestId('layout-mode')).toHaveTextContent('hierarchical');
      });
    });
  });

  describe('Physics Settings Panel', () => {
    it('does not show physics settings in hierarchical mode', () => {
      renderWithProviders(<SystemsMapView />);

      expect(screen.queryByText('Physics Settings')).not.toBeInTheDocument();
    });

    it('shows physics settings in force-directed mode', async () => {
      renderWithProviders(<SystemsMapView />);

      const forceDirectedButton = screen.getByText('Force-Directed');
      fireEvent.click(forceDirectedButton);

      await waitFor(() => {
        expect(screen.getByText('Physics Settings')).toBeInTheDocument();
      });
    });

    it('displays all physics control sliders', async () => {
      renderWithProviders(<SystemsMapView />);

      fireEvent.click(screen.getByText('Force-Directed'));

      await waitFor(() => {
        expect(screen.getByText('Repulsion')).toBeInTheDocument();
        expect(screen.getByText('Link Distance')).toBeInTheDocument();
        expect(screen.getByText('Gravity')).toBeInTheDocument();
        expect(screen.getByText('Collision Buffer')).toBeInTheDocument();
      });
    });

    it('updates repulsion slider value', async () => {
      renderWithProviders(<SystemsMapView />);

      fireEvent.click(screen.getByText('Force-Directed'));

      await waitFor(() => {
        const repulsionSlider = screen.getByLabelText('Repulsion', { selector: 'input' });
        fireEvent.change(repulsionSlider, { target: { value: '-500' } });

        expect(screen.getByText('-500')).toBeInTheDocument();
      });
    });

    it('updates link distance slider value', async () => {
      renderWithProviders(<SystemsMapView />);

      fireEvent.click(screen.getByText('Force-Directed'));

      await waitFor(() => {
        const linkDistanceSlider = screen.getByLabelText('Link Distance', { selector: 'input' });
        fireEvent.change(linkDistanceSlider, { target: { value: '200' } });

        expect(screen.getByText('200')).toBeInTheDocument();
      });
    });

    it('updates gravity slider value', async () => {
      renderWithProviders(<SystemsMapView />);

      fireEvent.click(screen.getByText('Force-Directed'));

      await waitFor(() => {
        const gravitySlider = screen.getByLabelText('Gravity', { selector: 'input' });
        fireEvent.change(gravitySlider, { target: { value: '0.1' } });

        expect(screen.getByText('0.10')).toBeInTheDocument();
      });
    });

    it('updates collision buffer slider value', async () => {
      renderWithProviders(<SystemsMapView />);

      fireEvent.click(screen.getByText('Force-Directed'));

      await waitFor(() => {
        const collisionSlider = screen.getByLabelText('Collision Buffer', { selector: 'input' });
        fireEvent.change(collisionSlider, { target: { value: '30' } });

        expect(screen.getByText('30')).toBeInTheDocument();
      });
    });

    it('passes physics settings to MechanismGraph in force-directed mode', async () => {
      renderWithProviders(<SystemsMapView />);

      fireEvent.click(screen.getByText('Force-Directed'));

      await waitFor(() => {
        const physicsSettings = screen.getByTestId('physics-settings');
        const settings = JSON.parse(physicsSettings.textContent || '{}');

        expect(settings).toHaveProperty('charge');
        expect(settings).toHaveProperty('linkDistance');
        expect(settings).toHaveProperty('gravity');
        expect(settings).toHaveProperty('collision');
      });
    });

    it('does not pass physics settings in hierarchical mode', async () => {
      renderWithProviders(<SystemsMapView />);

      expect(screen.queryByTestId('physics-settings')).not.toBeInTheDocument();
    });
  });

  describe('Integration with MechanismGraph', () => {
    it('passes correct layout mode to MechanismGraph', () => {
      renderWithProviders(<SystemsMapView />);

      expect(screen.getByTestId('layout-mode')).toHaveTextContent('hierarchical');
    });

    it('updates MechanismGraph layout mode on toggle', async () => {
      renderWithProviders(<SystemsMapView />);

      fireEvent.click(screen.getByText('Force-Directed'));

      await waitFor(() => {
        expect(screen.getByTestId('layout-mode')).toHaveTextContent('force-directed');
      });
    });

    it('maintains default physics settings values', async () => {
      renderWithProviders(<SystemsMapView />);

      fireEvent.click(screen.getByText('Force-Directed'));

      await waitFor(() => {
        const physicsSettings = screen.getByTestId('physics-settings');
        const settings = JSON.parse(physicsSettings.textContent || '{}');

        expect(settings.charge).toBe(-300);
        expect(settings.linkDistance).toBe(150);
        expect(settings.gravity).toBe(0.05);
        expect(settings.collision).toBe(20);
      });
    });
  });

  describe('State Management', () => {
    it('preserves physics settings when switching modes', async () => {
      renderWithProviders(<SystemsMapView />);

      // Switch to force-directed and change settings
      fireEvent.click(screen.getByText('Force-Directed'));

      await waitFor(() => {
        const repulsionSlider = screen.getByLabelText('Repulsion', { selector: 'input' });
        fireEvent.change(repulsionSlider, { target: { value: '-600' } });
      });

      // Switch to hierarchical
      fireEvent.click(screen.getByText('Hierarchical'));

      // Switch back to force-directed
      fireEvent.click(screen.getByText('Force-Directed'));

      await waitFor(() => {
        // Settings should be preserved
        expect(screen.getByText('-600')).toBeInTheDocument();
      });
    });

    it('maintains independent state for each physics parameter', async () => {
      renderWithProviders(<SystemsMapView />);

      fireEvent.click(screen.getByText('Force-Directed'));

      await waitFor(() => {
        const repulsionSlider = screen.getByLabelText('Repulsion', { selector: 'input' });
        const linkDistanceSlider = screen.getByLabelText('Link Distance', { selector: 'input' });

        fireEvent.change(repulsionSlider, { target: { value: '-700' } });
        fireEvent.change(linkDistanceSlider, { target: { value: '250' } });

        expect(screen.getByText('-700')).toBeInTheDocument();
        expect(screen.getByText('250')).toBeInTheDocument();
      });
    });
  });

  describe('Loading and Error States', () => {
    it('shows loading state', () => {
      const useGraphData = require('../hooks/useData').useGraphData;
      useGraphData.mockReturnValue({
        data: null,
        isLoading: true,
        error: null,
      });

      renderWithProviders(<SystemsMapView />);

      expect(screen.getByText(/Loading mechanisms and nodes/i)).toBeInTheDocument();
    });

    it('shows error state', () => {
      const useGraphData = require('../hooks/useData').useGraphData;
      useGraphData.mockReturnValue({
        data: null,
        isLoading: false,
        error: new Error('Failed to load'),
      });

      renderWithProviders(<SystemsMapView />);

      expect(screen.getByText(/Failed to load data/i)).toBeInTheDocument();
    });
  });

  describe('Accessibility', () => {
    it('has accessible layout toggle buttons', () => {
      renderWithProviders(<SystemsMapView />);

      const hierarchicalButton = screen.getByText('Hierarchical');
      const forceDirectedButton = screen.getByText('Force-Directed');

      expect(hierarchicalButton.tagName).toBe('BUTTON');
      expect(forceDirectedButton.tagName).toBe('BUTTON');
    });

    it('provides clear visual feedback for active layout', () => {
      renderWithProviders(<SystemsMapView />);

      const hierarchicalButton = screen.getByText('Hierarchical');
      expect(hierarchicalButton).toHaveClass('bg-white');
      expect(hierarchicalButton).toHaveClass('text-gray-900');
    });

    it('shows current values for all sliders', async () => {
      renderWithProviders(<SystemsMapView />);

      fireEvent.click(screen.getByText('Force-Directed'));

      await waitFor(() => {
        // All current values should be displayed
        expect(screen.getByText('-300')).toBeInTheDocument(); // charge
        expect(screen.getByText('150')).toBeInTheDocument(); // linkDistance
        expect(screen.getByText('0.05')).toBeInTheDocument(); // gravity
        expect(screen.getByText('20')).toBeInTheDocument(); // collision
      });
    });
  });
});
