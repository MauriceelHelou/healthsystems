/**
 * Main configuration exports.
 * Single entry point for all configuration modules.
 */

export * from './features';
export * from './constants';

/**
 * Combined configuration object for convenience.
 * Note: API configuration moved to src/utils/api.ts for better organization
 */
import { features } from './features';
import * as constants from './constants';

export const config = {
  features,
  constants,
} as const;

export default config;
