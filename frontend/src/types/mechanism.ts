/**
 * TypeScript types for mechanisms.
 */

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

export interface Mechanism {
  id: string;
  name: string;
  category: string;
  mechanism_type: string;
  effect_size: EffectSize;
  evidence: Evidence;
  version: string;
  last_updated: string;
  validated_by: string[];
  description?: string;
  assumptions?: string[];
  limitations?: string[];
  moderators?: Record<string, any>;
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
  confidence_interval: [number, number];
  category: string;
}

export interface MechanismEdge {
  source: string;
  target: string;
  strength: number;
}
