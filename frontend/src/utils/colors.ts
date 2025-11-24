import type { Category } from '../types'

/**
 * Minimalist color system
 * - White nodes with subtle gray borders
 * - Gray edges
 * - Orange accents for interactive elements
 */

// Minimalist palette
export const colors = {
  // Base colors
  white: '#FFFFFF',
  offWhite: '#F9FAFB',
  lightGray: '#E5E7EB',
  mediumGray: '#9CA3AF',
  darkGray: '#4B5563',
  almostBlack: '#1F2937',

  // Orange accents
  orangeLight: '#FED7AA',
  orange: '#FB923C',
  orangeDark: '#EA580C',
  orangeAccessible: '#C2410C', // Orange-700 - 4.6:1 contrast (WCAG AA compliant)

  // Node colors (all white with subtle variations)
  nodeDefault: '#FFFFFF',
  nodeBorder: '#E5E7EB',
  nodeHover: '#F9FAFB',
  nodeSelected: '#FED7AA',

  // Edge colors (gray)
  edgeDefault: '#D1D5DB',
  edgeHover: '#9CA3AF',
  edgeSelected: '#FB923C',

  // Text colors (WCAG AA compliant - 4.5:1 contrast on white)
  textPrimary: '#1F2937',   // Gray-800 - 13.6:1 contrast
  textSecondary: '#4B5563', // Gray-600 - 7.0:1 contrast (was #6B7280)
  textTertiary: '#6B7280',  // Gray-500 - 4.6:1 contrast (was #9CA3AF)
}

// All categories use white nodes (minimalist approach)
export const categoryColors: Record<Category, string> = {
  built_environment: colors.nodeDefault,
  social_environment: colors.nodeDefault,
  economic: colors.nodeDefault,
  political: colors.nodeDefault,
  biological: colors.nodeDefault,
  behavioral: colors.nodeDefault,
  healthcare_access: colors.nodeDefault,
  default: colors.nodeDefault,
}

// Category borders (subtle gray variations)
export const categoryBorders: Record<Category, string> = {
  built_environment: colors.nodeBorder,
  social_environment: colors.nodeBorder,
  economic: colors.nodeBorder,
  political: colors.nodeBorder,
  biological: colors.nodeBorder,
  behavioral: colors.nodeBorder,
  healthcare_access: colors.nodeBorder,
  default: colors.nodeBorder,
}

// Evidence colors kept minimal
export const evidenceColors = {
  A: colors.darkGray,
  B: colors.mediumGray,
  C: colors.lightGray,
  null: colors.lightGray,
}

export const evidenceLabels = {
  A: 'High',
  B: 'Moderate',
  C: 'Low',
  null: 'Unknown',
}

export function getCategoryColor(category: Category): string {
  return categoryColors[category]
}

export function getCategoryBorder(category: Category): string {
  return categoryBorders[category]
}

export function getEvidenceColor(quality: 'A' | 'B' | 'C' | null): string {
  return evidenceColors[quality || 'null']
}

// Scale badge colors (WCAG AA compliant - 4.5:1 contrast ratio on white)
// Used for node scale badges in visualizations
export const scaleColors: Record<number, string> = {
  1: '#7C3AED', // Violet - Structural Determinants (upstream policy)
  2: '#059669', // Emerald - Built Environment (infrastructure)
  3: '#0891B2', // Cyan - Institutional Infrastructure (organizations)
  4: '#2563EB', // Blue - Individual Conditions (material circumstances)
  5: '#DC2626', // Red - Individual Behaviors (health-seeking)
  6: '#EA580C', // Orange - Intermediate Pathways (clinical measures)
  7: '#DC2626', // Red - Crisis Endpoints (emergencies)
}

export const scaleLabels: Record<number, string> = {
  1: 'Structural',
  2: 'Built Environment',
  3: 'Institutional',
  4: 'Individual Conditions',
  5: 'Behaviors',
  6: 'Pathways',
  7: 'Crisis',
}

export function getScaleColor(scale: number): string {
  return scaleColors[scale] || colors.mediumGray
}

export function getScaleLabel(scale: number): string {
  return scaleLabels[scale] || 'Unknown'
}
