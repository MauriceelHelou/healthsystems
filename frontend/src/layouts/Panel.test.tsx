import { render, screen, fireEvent } from '@testing-library/react';
import { Panel } from './Panel';

// Mock ResizeObserver
global.ResizeObserver = class ResizeObserver {
  observe() {}
  unobserve() {}
  disconnect() {}
} as any;

describe('Panel', () => {
  const mockOnClose = jest.fn();
  const mockOnBack = jest.fn();

  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe('Basic Rendering', () => {
    it('renders panel with title', () => {
      render(
        <Panel title="Test Panel" onClose={mockOnClose}>
          <p>Panel content</p>
        </Panel>
      );

      expect(screen.getByText('Test Panel')).toBeInTheDocument();
      expect(screen.getByText('Panel content')).toBeInTheDocument();
    });

    it('renders with complementary role and aria-label', () => {
      render(
        <Panel title="Test Panel" onClose={mockOnClose}>
          <p>Content</p>
        </Panel>
      );

      const panel = screen.getByRole('complementary');
      expect(panel).toHaveAttribute('aria-label', 'Test Panel');
    });

    it('renders optional icon', () => {
      render(
        <Panel
          title="Test Panel"
          onClose={mockOnClose}
          icon={<span data-testid="test-icon">Icon</span>}
        >
          <p>Content</p>
        </Panel>
      );

      expect(screen.getByTestId('test-icon')).toBeInTheDocument();
    });

    it('renders optional footer', () => {
      render(
        <Panel
          title="Test Panel"
          onClose={mockOnClose}
          footer={<div data-testid="panel-footer">Footer content</div>}
        >
          <p>Content</p>
        </Panel>
      );

      expect(screen.getByTestId('panel-footer')).toBeInTheDocument();
    });
  });

  describe('Close Button', () => {
    it('renders close button', () => {
      render(
        <Panel title="Test Panel" onClose={mockOnClose}>
          <p>Content</p>
        </Panel>
      );

      expect(screen.getByLabelText('Close panel')).toBeInTheDocument();
    });

    it('calls onClose when close button is clicked', () => {
      render(
        <Panel title="Test Panel" onClose={mockOnClose}>
          <p>Content</p>
        </Panel>
      );

      fireEvent.click(screen.getByLabelText('Close panel'));
      expect(mockOnClose).toHaveBeenCalledTimes(1);
    });
  });

  describe('Back Button', () => {
    it('does not render back button when onBack is not provided', () => {
      render(
        <Panel title="Test Panel" onClose={mockOnClose}>
          <p>Content</p>
        </Panel>
      );

      expect(screen.queryByLabelText('Go back')).not.toBeInTheDocument();
    });

    it('renders back button when onBack is provided', () => {
      render(
        <Panel title="Test Panel" onClose={mockOnClose} onBack={mockOnBack}>
          <p>Content</p>
        </Panel>
      );

      expect(screen.getByLabelText('Go back')).toBeInTheDocument();
    });

    it('calls onBack when back button is clicked', () => {
      render(
        <Panel title="Test Panel" onClose={mockOnClose} onBack={mockOnBack}>
          <p>Content</p>
        </Panel>
      );

      fireEvent.click(screen.getByLabelText('Go back'));
      expect(mockOnBack).toHaveBeenCalledTimes(1);
    });

    it('back button appears before icon and title', () => {
      render(
        <Panel
          title="Test Panel"
          onClose={mockOnClose}
          onBack={mockOnBack}
          icon={<span data-testid="test-icon">Icon</span>}
        >
          <p>Content</p>
        </Panel>
      );

      const backButton = screen.getByLabelText('Go back');
      // Verify icon and title are present (they're used implicitly in DOM order check)
      expect(screen.getByTestId('test-icon')).toBeInTheDocument();
      expect(screen.getByText('Test Panel')).toBeInTheDocument();

      // Check DOM order - back button should come first
      const header = backButton.closest('.flex');
      const children = header?.children;

      expect(children).toBeDefined();
      if (children) {
        // Back button should be first
        expect(children[0]).toContainElement(backButton);
      }
    });
  });

  describe('Collapse Button', () => {
    it('renders collapse button when collapsible is true', () => {
      render(
        <Panel title="Test Panel" onClose={mockOnClose} collapsible>
          <p>Content</p>
        </Panel>
      );

      expect(screen.getByLabelText(/collapse panel|expand panel/i)).toBeInTheDocument();
    });

    it('does not render collapse button when collapsible is false', () => {
      render(
        <Panel title="Test Panel" onClose={mockOnClose} collapsible={false}>
          <p>Content</p>
        </Panel>
      );

      expect(screen.queryByLabelText(/collapse panel|expand panel/i)).not.toBeInTheDocument();
    });
  });

  describe('Resizing', () => {
    it('renders resize handle when resizable is true', () => {
      const { container } = render(
        <Panel title="Test Panel" onClose={mockOnClose} resizable>
          <p>Content</p>
        </Panel>
      );

      // Resize handle has cursor-col-resize class
      const resizeHandle = container.querySelector('.cursor-col-resize');
      expect(resizeHandle).toBeInTheDocument();
    });

    it('does not render resize handle when resizable is false', () => {
      const { container } = render(
        <Panel title="Test Panel" onClose={mockOnClose} resizable={false}>
          <p>Content</p>
        </Panel>
      );

      const resizeHandle = container.querySelector('.cursor-col-resize');
      expect(resizeHandle).not.toBeInTheDocument();
    });
  });

  describe('Default Props', () => {
    it('uses default width of 400px', () => {
      render(
        <Panel title="Test Panel" onClose={mockOnClose}>
          <p>Content</p>
        </Panel>
      );

      const panel = screen.getByRole('complementary');
      expect(panel).toHaveStyle({ width: '400px' });
    });

    it('renders as collapsible by default', () => {
      render(
        <Panel title="Test Panel" onClose={mockOnClose}>
          <p>Content</p>
        </Panel>
      );

      expect(screen.getByLabelText(/collapse panel|expand panel/i)).toBeInTheDocument();
    });

    it('renders as resizable by default', () => {
      const { container } = render(
        <Panel title="Test Panel" onClose={mockOnClose}>
          <p>Content</p>
        </Panel>
      );

      const resizeHandle = container.querySelector('.cursor-col-resize');
      expect(resizeHandle).toBeInTheDocument();
    });
  });

  describe('Custom Width', () => {
    it('uses custom default width', () => {
      render(
        <Panel title="Test Panel" onClose={mockOnClose} defaultWidth={500}>
          <p>Content</p>
        </Panel>
      );

      const panel = screen.getByRole('complementary');
      expect(panel).toHaveStyle({ width: '500px' });
    });
  });
});
