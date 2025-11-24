/**
 * Evidence quality scoring utilities.
 * Consolidates evidence assessment logic.
 */
import type { Mechanism } from '../../types/mechanism';

// Quality grade weights
export const EVIDENCE_QUALITY_WEIGHTS = {
  A: 1.0,   // Strong evidence (RCTs, meta-analyses)
  B: 0.6,   // Moderate evidence (observational)
  C: 0.3,   // Limited evidence (case studies)
} as const;

/**
 * Calculate comprehensive evidence score.
 * Considers quality grade and number of studies.
 */
export function calculateEvidenceScore(mechanism: Mechanism): number {
  const qualityWeight = getQualityWeight(mechanism.evidence_quality);
  const studyBonus = calculateStudyBonus(mechanism.n_studies || 0);

  return Math.min(qualityWeight + studyBonus, 1.0);
}

/**
 * Get weight for evidence quality grade.
 */
export function getQualityWeight(grade: string | null): number {
  if (!grade) return 0.3;
  return EVIDENCE_QUALITY_WEIGHTS[grade as keyof typeof EVIDENCE_QUALITY_WEIGHTS] || 0.3;
}

/**
 * Calculate bonus based on number of studies.
 * Logarithmic scale to avoid overweighting high study counts.
 */
export function calculateStudyBonus(nStudies: number): number {
  if (nStudies === 0) return 0;

  // Logarithmic bonus: log10(n+1) / 10
  // e.g., 1 study = 0.03, 10 studies = 0.10, 100 studies = 0.20
  return Math.log10(nStudies + 1) / 10;
}

/**
 * Aggregate evidence scores across a path.
 * Returns average score weighted by position (later = more weight).
 */
export function aggregatePathEvidence(mechanisms: Mechanism[]): number {
  if (mechanisms.length === 0) return 0;

  let totalScore = 0;
  let totalWeight = 0;

  mechanisms.forEach((mechanism, index) => {
    const score = calculateEvidenceScore(mechanism);
    const weight = index + 1; // Later mechanisms weighted more
    totalScore += score * weight;
    totalWeight += weight;
  });

  return totalScore / totalWeight;
}

/**
 * Classify evidence strength.
 */
export function getEvidenceStrength(score: number): 'strong' | 'moderate' | 'weak' {
  if (score >= 0.7) return 'strong';
  if (score >= 0.4) return 'moderate';
  return 'weak';
}

/**
 * Get color for evidence quality display.
 */
export function getEvidenceColor(grade: string): string {
  switch (grade) {
    case 'A': return 'text-green-600';
    case 'B': return 'text-yellow-600';
    case 'C': return 'text-orange-600';
    default: return 'text-gray-600';
  }
}

/**
 * Get background color for evidence quality badges.
 */
export function getEvidenceBadgeColor(grade: string): string {
  switch (grade) {
    case 'A': return 'bg-green-100 text-green-800';
    case 'B': return 'bg-yellow-100 text-yellow-800';
    case 'C': return 'bg-orange-100 text-orange-800';
    default: return 'bg-gray-100 text-gray-800';
  }
}
