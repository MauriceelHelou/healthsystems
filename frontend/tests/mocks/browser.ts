import { setupWorker } from 'msw/browser';
import { handlers } from './handlers';

/**
 * Mock Service Worker for browser (development mode)
 *
 * To enable in development:
 * 1. Run: npx msw init public/ --save
 * 2. In src/index.tsx, add:
 *    if (process.env.NODE_ENV === 'development') {
 *      const { worker } = require('./tests/mocks/browser');
 *      worker.start();
 *    }
 */
export const worker = setupWorker(...handlers);
