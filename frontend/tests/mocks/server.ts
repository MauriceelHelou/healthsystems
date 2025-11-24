import { setupServer } from 'msw/node';
import { handlers } from './handlers';

/**
 * Mock Service Worker server for Node.js (Jest tests)
 */
export const server = setupServer(...handlers);

// Establish API mocking before all tests
beforeAll(() => {
  server.listen({ onUnhandledRequest: 'warn' });
});

// Reset any request handlers that are declared in individual tests
afterEach(() => {
  server.resetHandlers();
});

// Clean up after all tests are complete
afterAll(() => {
  server.close();
});
