/**
 * Central export point for all utility functions
 * Import utilities from here to maintain consistency: import { buildGraphFromMechanisms, cn } from '../utils'
 */

// ==============================================
// Graph Building Utilities
// ==============================================
export {
  buildGraphFromMechanisms,
  filterGraphByCategory,
  filterGraphByScale,
  calculateNodeMetrics,
  getGraphCategories,
  getGraphScales,
  buildAlcoholismSubgraph,
  calculateGraphStats,
  type GraphBuildOptions,
  type GraphStats,
} from './graphBuilder';

// ==============================================
// Alcoholism System Filtering Utilities
// ==============================================
export {
  getAlcoholNodeCategory,
  isAlcoholRelated,
  type AlcoholNodeCategory,
} from './alcoholismFilter';

// ==============================================
// Data Transformation Utilities
// ==============================================
export {
  transformNode,
  transformMechanismToEdge,
  transformMechanismDetail,
  transformApiMechanismToMechanism,
  buildGraph,
  transformToSystemsNetwork,
  type ApiNode,
  type ApiMechanismListItem,
  type ApiMechanismDetail,
  type GraphData,
} from './transformers';

// ==============================================
// API Utilities
// ==============================================
export {
  API_ENDPOINTS,
  apiClient,
  type ApiResponse,
  type ApiErrorResponse,
} from './api';

// ==============================================
// UI Utilities
// ==============================================

// Class name merging for Tailwind CSS
export { cn } from './classNames';

// Color utilities for categories and visualizations
export {
  colors,
  categoryColors,
  categoryBorders,
  evidenceColors,
  evidenceLabels,
  scaleColors,
  scaleLabels,
  getCategoryColor,
  getCategoryBorder,
  getEvidenceColor,
} from './colors';
