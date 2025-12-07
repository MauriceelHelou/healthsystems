/**
 * TypeScript types for mechanisms.
 */

/**
 * Mechanism category types - aligned with mechanism_schema_mvp.json
 * These represent the primary domain/level of intervention for a mechanism.
 * @deprecated Use Domain instead. Retained for backward compatibility.
 */
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
 * Domain types representing thematic areas that span ALL 7 scales.
 *
 * Domains are root nodes (depth=0) in the hierarchy. A node's domains
 * are computed from its ancestry path(s) - nodes can belong to multiple
 * domains through DAG parent relationships.
 */
export type Domain =
  | 'healthcare_system'
  | 'housing'
  | 'economic_security'
  | 'employment_occupational'
  | 'food_security'
  | 'education'
  | 'built_environment_transportation'
  | 'environmental_climate'
  | 'criminal_justice'
  | 'social_environment'
  | 'behavioral_health'
  | 'long_term_services_supports'
  | 'maternal_child_health'
  | 'specialized_clinical'
  | 'public_health_infrastructure'
  | 'digital_information_access'
  | 'civic_political_engagement';

/**
 * All 17 domains as an array for iteration
 */
export const ALL_DOMAINS: Domain[] = [
  'healthcare_system',
  'housing',
  'economic_security',
  'employment_occupational',
  'food_security',
  'education',
  'built_environment_transportation',
  'environmental_climate',
  'criminal_justice',
  'social_environment',
  'behavioral_health',
  'long_term_services_supports',
  'maternal_child_health',
  'specialized_clinical',
  'public_health_infrastructure',
  'digital_information_access',
  'civic_political_engagement',
];

/**
 * Domain display info
 */
export interface DomainInfo {
  name: string;
  description: string;
  scale1Example: string;
  scale7Example: string;
}

/**
 * Domain definitions with human-readable names and descriptions
 */
export const DOMAIN_INFO: Record<Domain, DomainInfo> = {
  healthcare_system: {
    name: 'Healthcare System',
    description: 'Insurance, providers, access, utilization, outcomes',
    scale1Example: 'medicaid_expansion_status',
    scale7Example: 'avoidable_ed_visits',
  },
  housing: {
    name: 'Housing',
    description: 'Policy, stock, affordability, quality, homelessness',
    scale1Example: 'rent_control_policy',
    scale7Example: 'homelessness_rate',
  },
  economic_security: {
    name: 'Economic Security',
    description: 'Income, poverty, debt, safety net programs',
    scale1Example: 'minimum_wage_level',
    scale7Example: 'medical_bankruptcy_rate',
  },
  employment_occupational: {
    name: 'Employment & Occupational',
    description: 'Labor laws, workplace safety, job quality',
    scale1Example: 'osha_standards',
    scale7Example: 'occupational_fatality_rate',
  },
  food_security: {
    name: 'Food Security',
    description: 'SNAP, food retail, access, nutrition',
    scale1Example: 'snap_benefit_level',
    scale7Example: 'malnutrition_hospitalizations',
  },
  education: {
    name: 'Education',
    description: 'Policy, schools, attainment, child development',
    scale1Example: 'education_funding_formula',
    scale7Example: 'school_dropout_rate',
  },
  built_environment_transportation: {
    name: 'Built Environment & Transportation',
    description: 'Transit, parks, walkability, active transport',
    scale1Example: 'transit_funding',
    scale7Example: 'traffic_fatality_rate',
  },
  environmental_climate: {
    name: 'Environmental & Climate',
    description: 'Pollution, climate, exposures, environmental health',
    scale1Example: 'clean_air_act_enforcement',
    scale7Example: 'heat_stroke_deaths',
  },
  criminal_justice: {
    name: 'Criminal Justice',
    description: 'Sentencing, policing, incarceration, reentry',
    scale1Example: 'bail_reform_policy',
    scale7Example: 'recidivism_rate',
  },
  social_environment: {
    name: 'Social Environment',
    description: 'Discrimination, social support, community cohesion',
    scale1Example: 'civil_rights_enforcement',
    scale7Example: 'social_isolation_mortality',
  },
  behavioral_health: {
    name: 'Behavioral Health',
    description: 'Mental health, substance use, treatment, crisis',
    scale1Example: 'mental_health_parity_law',
    scale7Example: 'overdose_mortality',
  },
  long_term_services_supports: {
    name: 'Long-Term Services & Supports',
    description: 'LTSS, disability, caregiving, aging',
    scale1Example: 'medicaid_hcbs_waiver',
    scale7Example: 'nursing_home_mortality',
  },
  maternal_child_health: {
    name: 'Maternal & Child Health',
    description: 'Pregnancy, birth, child development, pediatrics',
    scale1Example: 'pregnancy_medicaid',
    scale7Example: 'infant_mortality',
  },
  specialized_clinical: {
    name: 'Specialized Clinical',
    description: 'Cancer, kidney, transplant, oral, vision, pain, geriatrics',
    scale1Example: 'cancer_screening_mandate',
    scale7Example: 'cancer_mortality',
  },
  public_health_infrastructure: {
    name: 'Public Health Infrastructure',
    description: 'Funding, departments, surveillance, preparedness',
    scale1Example: 'public_health_funding',
    scale7Example: 'outbreak_mortality',
  },
  digital_information_access: {
    name: 'Digital & Information Access',
    description: 'Broadband, telehealth, digital literacy',
    scale1Example: 'broadband_subsidy_policy',
    scale7Example: 'digital_divide_health_disparity',
  },
  civic_political_engagement: {
    name: 'Civic & Political Engagement',
    description: 'Voting, civic participation, political power',
    scale1Example: 'voting_rights_law',
    scale7Example: 'disenfranchisement_health_impact',
  },
};

/**
 * Hierarchy level for mechanisms
 * - leaf: Connects specific (child) nodes
 * - parent: Connects abstract/general (parent) nodes
 * - cross: Spans hierarchy levels
 */
export type HierarchyLevel = 'leaf' | 'parent' | 'cross';

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

/**
 * Moderator interface - aligned with mechanism_schema_mvp.json
 * Represents factors that strengthen, weaken, or modify a mechanism's effect.
 */
export interface Moderator {
  name?: string;
  type?: string;
  category?: string;
  direction?: 'strengthens' | 'weakens' | 'u_shaped' | string;
  strength?: 'weak' | 'moderate' | 'strong';
  description?: string;
  effect?: string;
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
  /** @deprecated Use domains computed from node ancestry */
  hierarchy_level?: HierarchyLevel;
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
  /** Node description from canonical node bank */
  description?: string;
  /** Unit of measurement from canonical node bank */
  unit?: string;
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
  /** Hierarchy level of the mechanism ('leaf', 'parent', 'cross') */
  hierarchyLevel?: HierarchyLevel;
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

// ==========================================
// Canonical Node Types (Node Bank)
// ==========================================

/**
 * Canonical node from the node bank API
 * Contains authoritative node metadata
 */
export interface CanonicalNode {
  id: string;
  name: string;
  scale: NodeScale;
  /** @deprecated Use domains instead */
  category: Category;
  node_type: 'stock' | 'proxy_index' | 'crisis_endpoint';
  unit?: string;
  description?: string;
  mechanism_count?: number;

  // === HIERARCHY FIELDS ===
  /** Depth in hierarchy: 0 = root/domain node, 1+ = nested */
  depth?: number;
  /** Primary path for efficient ancestry: "root_id/parent_id/this_id" */
  primaryPath?: string;
  /** All ancestor IDs (from ALL parent paths in DAG) */
  allAncestors?: string[];
  /** Whether this is a grouping/container node vs leaf/measurable node */
  isGroupingNode?: boolean;
  /** Domain(s) this node belongs to (computed from root ancestors) */
  domains?: Domain[];
  /** Direct parent node IDs */
  parentIds?: string[];
  /** Direct child node IDs */
  childIds?: string[];
  /** Whether this node has children */
  hasChildren?: boolean;
  /** Number of direct children */
  childCount?: number;
}

/**
 * Response from GET /api/nodes/
 */
export interface NodeListResponse {
  nodes: CanonicalNode[];
  total: number;
  referenced_count: number;
}

/**
 * Options for useNodes hook
 */
export interface UseNodesOptions {
  referenced_only?: boolean;
  category?: Category;
  scale?: NodeScale;
  search?: string;
  enabled?: boolean;
}

// ==========================================
// Node Hierarchy Types (NEW)
// ==========================================

/**
 * Visual state for a node in the hierarchy visualization
 */
export type NodeVisualState =
  | 'leaf'             // No children, standard node
  | 'collapsed-parent' // Has children, showing summary
  | 'expanded-parent'  // Has children, children visible
  | 'ghost-reference'; // DAG reference (node appears under multiple parents)

/**
 * Hierarchical node with parent-child relationships
 * Extends CanonicalNode with hierarchy-specific fields
 */
export interface HierarchicalNode extends CanonicalNode {
  /** Visual state for rendering */
  visualState: NodeVisualState;
  /** Depth in the current view (may differ from absolute depth) */
  viewDepth: number;
  /** Whether this is a ghost reference (same node under different parent) */
  isGhostReference?: boolean;
  /** If ghost, the ID of the primary instance */
  primaryInstanceId?: string;
  /** Children nodes (populated when expanded) */
  children?: HierarchicalNode[];
  /** Display order among siblings */
  displayOrder?: number;
}

/**
 * Expansion state for the hierarchy
 */
export interface NodeHierarchyState {
  /** Set of expanded node IDs */
  expandedNodeIds: Set<string>;
  /** Currently focused node ID (for keyboard navigation) */
  focusedNodeId: string | null;
  /** Current viewport root (for zooming into subtrees) */
  viewportRootId: string | null;
  /** Breadcrumb path from root to viewport */
  breadcrumbPath: string[];
}

/**
 * Hierarchy node for tree structure from API
 */
export interface HierarchyTreeNode {
  id: string;
  name: string;
  scale: NodeScale;
  depth: number;
  domains: Domain[];
  isGroupingNode: boolean;
  childCount: number;
  children?: HierarchyTreeNode[];
}

/**
 * Response from GET /api/nodes/hierarchy/tree
 */
export interface HierarchyTreeResponse {
  roots: HierarchyTreeNode[];
  totalNodes: number;
  maxDepth: number;
}

/**
 * Response from GET /api/nodes/{id}/ancestors
 */
export interface NodeAncestorsResponse {
  nodeId: string;
  ancestors: CanonicalNode[];
  paths: string[][]; // Multiple paths for DAG (each path is array of node IDs)
}

/**
 * Response from GET /api/nodes/{id}/descendants
 */
export interface NodeDescendantsResponse {
  nodeId: string;
  descendants: CanonicalNode[];
  totalCount: number;
  maxDepth: number;
}

/**
 * Parent-child relationship in the hierarchy
 */
export interface NodeHierarchyRelationship {
  parentId: string;
  childId: string;
  relationshipType: 'contains' | 'specializes' | 'contextualizes';
  orderIndex: number;
}

/**
 * Options for hierarchy API requests
 */
export interface HierarchyQueryOptions {
  /** Maximum depth to traverse */
  maxDepth?: number;
  /** Include only nodes in these domains */
  domains?: Domain[];
  /** Include only nodes at these scales */
  scales?: NodeScale[];
  /** Include mechanism counts */
  includeMechanismCounts?: boolean;
}

/**
 * Props for hierarchy visualization components
 */
export interface HierarchyVisualizationProps {
  /** Root nodes to display */
  roots: HierarchyTreeNode[];
  /** Current expansion state */
  hierarchyState: NodeHierarchyState;
  /** Callback when node is expanded/collapsed */
  onToggleExpand: (nodeId: string) => void;
  /** Callback when node is selected */
  onNodeSelect?: (nodeId: string) => void;
  /** Callback for keyboard navigation */
  onNavigate?: (direction: 'up' | 'down' | 'left' | 'right') => void;
  /** Currently selected node ID */
  selectedNodeId?: string | null;
  /** Filter by domains */
  filteredDomains?: Domain[];
}
