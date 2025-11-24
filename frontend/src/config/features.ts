/**
 * Feature flags for enabling/disabling application features.
 * Allows runtime toggling of features via environment variables.
 */

export const features = {
  /**
   * Enable pathfinding feature for finding paths between nodes.
   */
  enablePathfinding: process.env.REACT_APP_ENABLE_PATHFINDING !== 'false',

  /**
   * Enable crisis explorer for analyzing crisis endpoints.
   */
  enableCrisisExplorer: process.env.REACT_APP_ENABLE_CRISIS_EXPLORER !== 'false',

  /**
   * Enable pathway explorer for browsing mechanism pathways.
   */
  enablePathwayExplorer: process.env.REACT_APP_ENABLE_PATHWAY_EXPLORER !== 'false',

  /**
   * Enable node importance analysis.
   */
  enableNodeImportance: process.env.REACT_APP_ENABLE_NODE_IMPORTANCE !== 'false',

  /**
   * Enable alcoholism system view.
   */
  enableAlcoholismSystem: process.env.REACT_APP_ENABLE_ALCOHOLISM_SYSTEM !== 'false',

  /**
   * Enable systems map visualization.
   */
  enableSystemsMap: process.env.REACT_APP_ENABLE_SYSTEMS_MAP !== 'false',

  /**
   * Enable experimental features (hidden by default).
   */
  enableExperimentalFeatures: process.env.REACT_APP_ENABLE_EXPERIMENTAL === 'true',

  /**
   * Enable debug mode with additional logging and dev tools.
   */
  enableDebugMode: process.env.REACT_APP_ENABLE_DEBUG === 'true',
} as const;

/**
 * Check if a feature is enabled.
 */
export function isFeatureEnabled(featureName: keyof typeof features): boolean {
  return features[featureName];
}

/**
 * Get list of all enabled features.
 */
export function getEnabledFeatures(): string[] {
  return Object.entries(features)
    .filter(([_, enabled]) => enabled)
    .map(([name, _]) => name);
}
