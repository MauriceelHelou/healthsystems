/**
 * TypeScript types for mechanisms.
 */

// Category types
export type Category =
  | 'built_environment'
  | 'social_environment'
  | 'economic'
  | 'political'
  | 'biological'
  | 'behavioral'
  | 'healthcare_access'
  | 'default';

/**
 * Node scale type (1-7 system)
 * - 1: Structural Determinants (federal/state policy, decades causal distance)
 * - 2: Built Environment & Infrastructure (environmental quality, years-decades causal distance)
 * - 3: Institutional Infrastructure (organizations, facilities, months-years causal distance)
 * - 4: Individual/Household Conditions (material conditions, weeks-months causal distance)
 * - 5: Individual Behaviors & Psychosocial (health-seeking, adherence, days-weeks causal distance)
 * - 6: Intermediate Pathways (clinical measures, disease prevalence, hours-days causal distance)
 * - 7: Crisis Endpoints (mortality, emergency care, immediate causal distance)
 */
export type NodeScale = 1 | 2 | 3 | 4 | 5 | 6 | 7;

/**
 * @deprecated Use NodeScale (1-7) instead. Kept for backwards compatibility.
 */
export type StockType = 'structural' | 'proxy' | 'crisis';

export type EvidenceQuality = 'A' | 'B' | 'C' | null;

export interface EffectSize {
  measure: string;
  point_estimate: number;
  confidence_interval: [number, number];
  unit: string;
}

export interface Evidence {
  quality_rating: 'A' | 'B' | 'C';
  n_studies: number;
  citation: string;
}

export interface Citation {
  id: string;
  authors: string;
  year: number;
  title: string;
  journal: string;
  doi: string;
  url?: string;
}

export interface Moderator {
  type: 'policy' | 'geographic' | 'population';
  category?: 'policy' | 'geographic' | 'population';
  description: string;
  effect: string;
}

// API Response types - matching backend schema
export interface Mechanism {
  id: string;
  name: string;
  from_node_id: string;
  from_node_name: string;
  to_node_id: string;
  to_node_name: string;
  direction: 'positive' | 'negative';
  category: Category;
  description?: string;
  evidence_quality: EvidenceQuality;
  n_studies?: number;
  citations?: Citation[];
  moderators?: Moderator[];
  mechanism_pathway?: string[];

  // Legacy field names for backwards compatibility
  fromNode?: string;
  toNode?: string;
  evidenceQuality?: EvidenceQuality;
  studyCount?: number;
}

export interface Pathway {
  id: string;
  fromNodeId: string;
  toNodeId: string;
  interventionNodeId?: string;
  outcomeNodeId?: string;
  mechanisms: Mechanism[];
  overallEvidence: EvidenceQuality;
  aggregateQuality?: EvidenceQuality;
  overallDirection: 'positive' | 'negative';
  pathLength: number;
}

export interface MechanismWeight {
  mechanism_id: string;
  weight: number;
  confidence_interval: [number, number];
  context_data: Record<string, any>;
}

export interface SystemsNetwork {
  nodes: MechanismNode[];
  edges: MechanismEdge[];
}

export interface MechanismNode {
  id: string;
  label: string;
  weight: number;
  category: Category;
  /** @deprecated Use scale instead */
  stockType: StockType;
  /** Node scale (1-7) indicating causal hierarchy level */
  scale?: NodeScale;
  connections: {
    outgoing: number;
    incoming: number;
  };
}

export interface MechanismEdge {
  id: string;
  source: string;
  target: string;
  strength: number;
  direction: 'positive' | 'negative';
  category?: Category;
  evidenceQuality: EvidenceQuality;
  studyCount: number;
}

// ==========================================
// Node Importance Types (NEW FEATURES)
// ==========================================

/**
 * Node importance data from /api/nodes/importance endpoint
 */
export interface NodeImportance {
  nodeId: string;
  label: string;
  category: Category;
  scale: NodeScale | null;

  // Centrality measures (0-1)
  degreeScore: number;
  betweennessScore: number;
  closenessCentrality: number;
  pageRank: number;

  // Evidence-based scoring (0-1)
  evidenceScore: number;

  // Composite importance score (0-1)
  compositeScore: number;
  rank: number;

  // Metadata
  totalConnections: number;
  avgEvidenceQuality: number; // 0-3 scale
}

/**
 * Options for node importance query
 */
export interface NodeImportanceOptions {
  topN?: number;
  categories?: Category[];
  scales?: NodeScale[];
  minConnections?: number;
  enabled?: boolean;
}

// ==========================================
// Pathfinding Types (NEW FEATURES)
// ==========================================

/**
 * Pathfinding algorithm types
 */
export type PathfindingAlgorithm = 'shortest' | 'strongest_evidence' | 'all_simple';

/**
 * Node information in a path
 */
export interface PathNode {
  nodeId: string;
  label: string;
  category: Category;
  scale?: NodeScale;
}

/**
 * Mechanism information in a path
 */
export interface PathMechanism {
  mechanismId: string;
  name: string;
  fromNode: string;
  toNode: string;
  direction: 'positive' | 'negative';
  evidenceQuality: EvidenceQuality;
  category: Category;
}

/**
 * A single path result from pathfinding
 */
export interface PathResult {
  pathId: string;
  nodes: string[]; // Node IDs in path order
  nodeDetails: PathNode[];
  edges: string[]; // Mechanism IDs connecting nodes
  mechanismDetails: PathMechanism[];

  // Metrics
  pathLength: number; // Number of hops (edges)
  avgEvidenceQuality: number; // 0-3 scale
  evidenceGrade: 'A' | 'B' | 'C'; // Overall grade
  overallDirection: 'positive' | 'negative' | 'mixed';
  totalWeight: number;
}

/**
 * Pathfinding request options
 */
export interface PathfindingRequest {
  fromNode: string;
  toNode: string;
  algorithm: PathfindingAlgorithm;
  maxDepth?: number;
  maxPaths?: number;
  excludeCategories?: Category[];
  onlyCategories?: Category[];
}

/**
 * Pathfinding API response
 */
export interface PathfindingResponse {
  fromNode: string;
  toNode: string;
  algorithm: PathfindingAlgorithm;
  pathsFound: number;
  paths: PathResult[];
}

// ==========================================
// Graph Visualization Enhancement Types
// ==========================================

/**
 * Props for important nodes highlighting in MechanismGraph
 */
export interface ImportantNodesHighlight {
  nodeIds: string[];
  ranks?: Record<string, number>; // nodeId -> rank
  scores?: Record<string, number>; // nodeId -> importance score
}

/**
 * Props for path highlighting in MechanismGraph
 */
export interface PathHighlight {
  pathId: string;
  nodeIds: string[];
  edgeIds: string[];
  color?: string;
  animated?: boolean;
}

/**
 * Active paths for MechanismGraph visualization
 */
export interface ActivePaths {
  paths: PathHighlight[];
  selectedPathId?: string | null;
}

// ==========================================
// Graph Layout Types
// ==========================================

/**
 * Graph layout mode for MechanismGraph
 * - hierarchical: Fixed vertical columns by scale (1-7)
 * - force-directed: Physics-based layout with animated positioning
 */
export type GraphLayoutMode = 'hierarchical' | 'force-directed';

/**
 * Physics settings for force-directed layout
 */
export interface PhysicsSettings {
  charge: number; // Repulsion strength (-1000 to -50)
  linkDistance: number; // Target edge length (50-300)
  gravity: number; // Center pull strength (0-0.2)
  collision: number; // Collision radius buffer (0-50)
}

/**
 * Extended MechanismGraph props (for new features)
 */
export interface MechanismGraphEnhancedProps {
  // Existing props
  data: SystemsNetwork;
  width?: number;
  height?: number;
  onNodeClick?: (node: MechanismNode) => void;
  onEdgeClick?: (edge: MechanismEdge) => void;
  selectedNodeId?: string | null;
  filteredCategories?: string[];
  showLegend?: boolean;

  // New props for node importance
  importantNodes?: ImportantNodesHighlight;

  // New props for pathfinding
  activePaths?: ActivePaths;

  // Interactive selection for pathfinding
  selectionMode?: 'none' | 'from' | 'to';
  onNodeSelect?: (nodeId: string, nodeLabel: string) => void;

  // New props for layout modes
  layoutMode?: GraphLayoutMode;
  physicsSettings?: PhysicsSettings;
}

// ==========================================
// Crisis Explorer Types (NEW FEATURE)
// ==========================================

/**
 * Crisis endpoint node data from /api/nodes/crisis-endpoints
 */
export interface CrisisEndpoint {
  nodeId: string;
  label: string;
  category: Category;
  scale: 7;
  description?: string;
}

/**
 * Node with degree from crisis in subgraph
 */
export interface CrisisNodeWithDegree {
  nodeId: string;
  label: string;
  category: Category;
  scale: NodeScale;
  degreeFromCrisis: number;
  isCrisisEndpoint: boolean;
  isPolicyLever: boolean;
  description?: string;
}

/**
 * Edge in crisis subgraph
 */
export interface CrisisEdge {
  mechanismId: string;
  source: string;
  target: string;
  direction: 'positive' | 'negative';
  evidenceQuality: EvidenceQuality;
  strength: 1 | 2 | 3; // C=1, B=2, A=3
  category: Category;
  name: string;
}

/**
 * Statistics for crisis subgraph
 */
export interface CrisisSubgraphStats {
  totalNodes: number;
  totalEdges: number;
  policyLevers: number;
  avgDegree: number;
  categoryBreakdown: Record<string, number>;
}

/**
 * Request schema for crisis subgraph endpoint
 */
export interface CrisisSubgraphRequest {
  crisisNodeIds: string[]; // 1-10 nodes
  maxDegrees?: number; // 1-8, default 5
  minStrength?: number; // 1=C, 2=B, 3=A, default 2
  includeCategories?: Category[];
}

/**
 * Response schema for crisis subgraph endpoint
 */
export interface CrisisSubgraphResponse {
  nodes: CrisisNodeWithDegree[];
  edges: CrisisEdge[];
  stats: CrisisSubgraphStats;
}

/**
 * Props for crisis highlighting in MechanismGraph
 */
export interface CrisisHighlight {
  nodeIdToDegree: Map<string, number>; // Maps node ID to degree from crisis
  policyLeverIds: Set<string>; // Set of policy lever node IDs
}
