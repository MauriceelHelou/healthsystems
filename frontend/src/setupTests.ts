// Jest-DOM matchers
import '@testing-library/jest-dom';

// Mock window.matchMedia (for responsive components)
Object.defineProperty(window, 'matchMedia', {
  writable: true,
  value: jest.fn().mockImplementation((query) => ({
    matches: false,
    media: query,
    onchange: null,
    addListener: jest.fn(), // deprecated
    removeListener: jest.fn(), // deprecated
    addEventListener: jest.fn(),
    removeEventListener: jest.fn(),
    dispatchEvent: jest.fn(),
  })),
});

// Mock IntersectionObserver (for lazy loading, scroll-based components)
global.IntersectionObserver = class IntersectionObserver {
  constructor() {}
  disconnect() {}
  observe() {}
  takeRecords() {
    return [];
  }
  unobserve() {}
} as any;

// Mock ResizeObserver (for responsive visualizations)
global.ResizeObserver = class ResizeObserver {
  constructor() {}
  disconnect() {}
  observe() {}
  unobserve() {}
} as any;

// Mock SVGElement.prototype.getBBox (for D3.js tests)
if (typeof SVGElement !== 'undefined') {
  SVGElement.prototype.getBBox = jest.fn().mockReturnValue({
    x: 0,
    y: 0,
    width: 100,
    height: 100,
  });
}

// Mock scrollTo (for navigation tests)
window.scrollTo = jest.fn();

// Suppress console errors/warnings in tests (optional - comment out if you want to see them)
const originalError = console.error;
const originalWarn = console.warn;

beforeAll(() => {
  console.error = (...args: any[]) => {
    // Ignore specific React warnings that are expected in tests
    if (
      typeof args[0] === 'string' &&
      (args[0].includes('Warning: ReactDOM.render') ||
       args[0].includes('Warning: useLayoutEffect') ||
       args[0].includes('Not implemented: HTMLFormElement.prototype.submit'))
    ) {
      return;
    }
    originalError.call(console, ...args);
  };

  console.warn = (...args: any[]) => {
    // Ignore specific warnings
    if (
      typeof args[0] === 'string' &&
      args[0].includes('componentWillReceiveProps')
    ) {
      return;
    }
    originalWarn.call(console, ...args);
  };
});

afterAll(() => {
  console.error = originalError;
  console.warn = originalWarn;
});

// Import MSW server for API mocking
import './tests/mocks/server';

// Clean up after each test
afterEach(() => {
  jest.clearAllMocks();
});
