// Polyfills for Node.js Jest environment (must come first)
const { TextEncoder, TextDecoder } = require('util');
global.TextEncoder = TextEncoder;
global.TextDecoder = TextDecoder;

// Mock ReadableStream for MSW v2.x
if (typeof global.ReadableStream === 'undefined') {
  global.ReadableStream = class ReadableStream {
    locked: boolean;
    constructor() {
      this.locked = false;
    }
    getReader() {
      return {
        read: () => Promise.resolve({ done: true, value: undefined }),
        releaseLock: () => {},
        closed: Promise.resolve(),
      };
    }
  } as any;
}

// Jest-DOM matchers
import '@testing-library/jest-dom';

// Mock window.matchMedia (for responsive components)
Object.defineProperty(window, 'matchMedia', {
  writable: true,
  value: jest.fn().mockImplementation((query) => ({
    matches: false,
    media: query,
    onchange: null,
    addListener: jest.fn(),
    removeListener: jest.fn(),
    addEventListener: jest.fn(),
    removeEventListener: jest.fn(),
    dispatchEvent: jest.fn(),
  })),
});

// Mock IntersectionObserver
global.IntersectionObserver = class IntersectionObserver {
  constructor() {}
  disconnect() {}
  observe() {}
  takeRecords() { return []; }
  unobserve() {}
} as any;

// Import MSW server for API mocking
// TODO: Re-enable when MSW server is set up
// import './tests/mocks/server';

// Clean up after each test
afterEach(() => {
  jest.clearAllMocks();
});
