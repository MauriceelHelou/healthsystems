/**
 * MSW-specific polyfills for Jest test environment
 */

const { TextEncoder, TextDecoder } = require('util');

// Polyfill TextEncoder/TextDecoder
global.TextEncoder = TextEncoder;
global.TextDecoder = TextDecoder;

// Polyfill ReadableStream for MSW fetch interception
if (typeof global.ReadableStream === 'undefined') {
  global.ReadableStream = class ReadableStream {
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
  };
}
