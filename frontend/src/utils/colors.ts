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

  // Node colors (all white with subtle variations)
  nodeDefault: '#FFFFFF',
  nodeBorder: '#E5E7EB',
  nodeHover: '#F9FAFB',
  nodeSelected: '#FED7AA',

  // Edge colors (gray)
  edgeDefault: '#D1D5DB',
  edgeHover: '#9CA3AF',
  edgeSelected: '#FB923C',

  // Text colors
  textPrimary: '#1F2937',
  textSecondary: '#6B7280',
  textTertiary: '#9CA3AF',
}

// All categories use white nodes (minimalist approach)
export const categoryColors: Record<Category, string> = {
  built_environment: colors.nodeDefault,
  social_environment: colors.nodeDefault,
  economic: colors.nodeDefault,
  political: colors.nodeDefault,
  biological: colors.nodeDefault,
  default: colors.nodeDefault,
}

// Category borders (subtle gray variations)
export const categoryBorders: Record<Category, string> = {
  built_environment: colors.nodeBorder,
  social_environment: colors.nodeBorder,
  economic: colors.nodeBorder,
  political: colors.nodeBorder,
  biological: colors.nodeBorder,
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
