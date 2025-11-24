/**
 * Central export point for all TypeScript types
 * Import types from here to maintain consistency: import { Category, Mechanism } from '../types'
 */

// Export all types from mechanism module
export * from './mechanism';

// Explicitly re-export commonly used types for convenience and documentation
export type {
  // Core type enums
  Category,
  NodeScale,
  StockType,
  EvidenceQuality,

  // Mechanism types
  Mechanism,
  MechanismNode,
  MechanismEdge,
  SystemsNetwork,

  // Supporting types
  Citation,
  Moderator,
  Evidence,
  EffectSize,
  Pathway,
  MechanismWeight,

  // Node importance types
  NodeImportance,
  NodeImportanceOptions,

  // Pathfinding types
  PathfindingAlgorithm,
  PathNode,
  PathMechanism,
  PathResult,
  PathfindingRequest,
  PathfindingResponse,

  // Graph visualization types
  GraphLayoutMode,
  PhysicsSettings,
  ImportantNodesHighlight,
  PathHighlight,
  ActivePaths,
  MechanismGraphEnhancedProps,

  // Crisis explorer types
  CrisisEndpoint,
  CrisisNodeWithDegree,
  CrisisEdge,
  CrisisSubgraphStats,
  CrisisSubgraphRequest,
  CrisisSubgraphResponse,
  CrisisHighlight,
} from './mechanism';
