/**
 * Application-wide constants.
 * Centralized location for all constant values used throughout the app.
 */

/**
 * Visualization settings and defaults.
 */
export const VISUALIZATION = {
  defaultZoom: 1,
  minZoom: 0.1,
  maxZoom: 1000,
  zoomStep: 0.1,

  nodeRadius: {
    default: 20,
    min: 10,
    max: 50,
  },

  edgeWidth: {
    default: 2,
    min: 1,
    max: 5,
  },

  animationDuration: 300,

  layout: {
    defaultSpacing: 200,
    hierarchicalSpacing: 150,
    forceStrength: -1000,
  },
} as const;

/**
 * Node scale levels for categorizing interventions/outcomes.
 */
export const NODE_SCALES = {
  individual: { value: 1, label: 'Individual', color: '#3b82f6' },
  interpersonal: { value: 2, label: 'Interpersonal', color: '#8b5cf6' },
  organizational: { value: 3, label: 'Organizational', color: '#ec4899' },
  community: { value: 4, label: 'Community', color: '#f59e0b' },
  policy: { value: 5, label: 'Policy', color: '#10b981' },
  global: { value: 6, label: 'Global', color: '#06b6d4' },
} as const;

/**
 * Evidence quality grades and their properties.
 */
export const EVIDENCE_GRADES = {
  A: {
    label: 'Strong',
    description: 'Strong evidence from RCTs or meta-analyses',
    color: '#10b981',
    weight: 1.0,
  },
  B: {
    label: 'Moderate',
    description: 'Moderate evidence from observational studies',
    color: '#f59e0b',
    weight: 0.6,
  },
  C: {
    label: 'Limited',
    description: 'Limited evidence from case studies or expert opinion',
    color: '#f97316',
    weight: 0.3,
  },
} as const;

/**
 * Mechanism categories and their properties.
 */
export const CATEGORIES = {
  biological: {
    label: 'Biological',
    color: '#3b82f6',
    description: 'Biological and physiological mechanisms',
  },
  behavioral: {
    label: 'Behavioral',
    color: '#8b5cf6',
    description: 'Individual behavior and decision-making',
  },
  psychological: {
    label: 'Psychological',
    color: '#ec4899',
    description: 'Mental health and psychological factors',
  },
  social_environment: {
    label: 'Social Environment',
    color: '#f59e0b',
    description: 'Social relationships and community factors',
  },
  built_environment: {
    label: 'Built Environment',
    color: '#10b981',
    description: 'Physical infrastructure and spaces',
  },
  economic: {
    label: 'Economic',
    color: '#06b6d4',
    description: 'Economic factors and financial systems',
  },
  policy: {
    label: 'Policy',
    color: '#6366f1',
    description: 'Laws, regulations, and governance',
  },
  healthcare_access: {
    label: 'Healthcare Access',
    color: '#f43f5e',
    description: 'Healthcare availability and accessibility',
  },
} as const;

/**
 * Search and filter defaults.
 */
export const SEARCH_DEFAULTS = {
  minQueryLength: 2,
  debounceMs: 300,
  maxResults: 100,
} as const;

/**
 * Pagination defaults.
 */
export const PAGINATION = {
  defaultPageSize: 20,
  pageSizeOptions: [10, 20, 50, 100],
} as const;

/**
 * Data refresh intervals (in milliseconds).
 */
export const REFRESH_INTERVALS = {
  mechanisms: 300000, // 5 minutes
  nodes: 300000, // 5 minutes
  pathways: 600000, // 10 minutes
} as const;
