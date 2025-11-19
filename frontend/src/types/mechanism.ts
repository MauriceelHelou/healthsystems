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
  | 'default';

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

export interface Mechanism {
  id: string;
  fromNode: string;
  toNode: string;
  direction: 'positive' | 'negative';
  description: string;
  evidenceQuality: EvidenceQuality;
  studyCount: number;
  citations: Citation[];
  moderators: Moderator[];
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
  stockType: StockType;
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
  evidenceQuality: EvidenceQuality;
  studyCount: number;
}
