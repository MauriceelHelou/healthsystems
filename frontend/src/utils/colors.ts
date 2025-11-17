import type { Category } from '../types'

/**
 * Color utilities based on design system
 */

export const categoryColors: Record<Category, string> = {
  built_environment: '#0369a1',
  social_environment: '#9333ea',
  economic: '#059669',
  political: '#dc2626',
  biological: '#ea580c',
  default: '#6b7280',
}

export const categoryColorsDark: Record<Category, string> = {
  built_environment: '#1e3a8a',
  social_environment: '#6b21a8',
  economic: '#065f46',
  political: '#991b1b',
  biological: '#9a3412',
  default: '#374151',
}

export const evidenceColors = {
  A: '#10b981',
  B: '#f59e0b',
  C: '#ef4444',
  null: '#9ca3af',
}

export const evidenceLabels = {
  A: 'High',
  B: 'Moderate',
  C: 'Low',
  null: 'Unknown',
}

export function getCategoryColor(category: Category, dark: boolean = false): string {
  return dark ? categoryColorsDark[category] : categoryColors[category]
}

export function getEvidenceColor(quality: 'A' | 'B' | 'C' | null): string {
  return evidenceColors[quality || 'null']
}
