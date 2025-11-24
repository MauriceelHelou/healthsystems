/**
 * Alcoholism system filtering utilities
 * Categorizes nodes in the alcoholism causal system
 */

/**
 * Types of nodes in the alcoholism system
 */
export type AlcoholNodeCategory =
  | 'core'          // Central alcohol use node
  | 'crisis'        // Crisis endpoint (e.g., mortality, emergency care)
  | 'risk_factor'   // Risk factor for alcohol use
  | 'policy_lever'  // Policy-modifiable structural factor
  | 'outcome'       // Downstream outcome
  | 'other';        // Related node

/**
 * Keywords for identifying different node types in the alcoholism system
 */
const ALCOHOL_KEYWORDS = {
  core: ['alcohol', 'ald', 'drinking', 'aud', 'alcohol use disorder'],
  crisis: ['mortality', 'death', 'emergency', 'hospitalization', 'overdose', 'cirrhosis'],
  risk_factor: ['stress', 'trauma', 'unemployment', 'poverty', 'depression', 'anxiety'],
  policy_lever: ['policy', 'tax', 'regulation', 'zoning', 'access control', 'treatment availability'],
  outcome: ['liver disease', 'hepatitis', 'health outcome', 'disability', 'morbidity'],
};

/**
 * Determine the category of a node in the alcoholism system
 * @param nodeId - The node ID or label to categorize
 * @returns The node category
 */
export function getAlcoholNodeCategory(nodeId: string): AlcoholNodeCategory {
  const searchText = nodeId.toLowerCase();

  // Check for core alcohol nodes (highest priority)
  if (ALCOHOL_KEYWORDS.core.some(kw => searchText.includes(kw))) {
    return 'core';
  }

  // Check for crisis endpoints
  if (ALCOHOL_KEYWORDS.crisis.some(kw => searchText.includes(kw))) {
    return 'crisis';
  }

  // Check for policy levers
  if (ALCOHOL_KEYWORDS.policy_lever.some(kw => searchText.includes(kw))) {
    return 'policy_lever';
  }

  // Check for outcomes
  if (ALCOHOL_KEYWORDS.outcome.some(kw => searchText.includes(kw))) {
    return 'outcome';
  }

  // Check for risk factors
  if (ALCOHOL_KEYWORDS.risk_factor.some(kw => searchText.includes(kw))) {
    return 'risk_factor';
  }

  return 'other';
}

/**
 * Check if a node is part of the alcoholism system
 * @param nodeId - The node ID or label to check
 * @returns True if the node is alcohol-related
 */
export function isAlcoholRelated(nodeId: string): boolean {
  const searchText = nodeId.toLowerCase();
  const allKeywords = [
    ...ALCOHOL_KEYWORDS.core,
    ...ALCOHOL_KEYWORDS.crisis,
    ...ALCOHOL_KEYWORDS.risk_factor,
    ...ALCOHOL_KEYWORDS.policy_lever,
    ...ALCOHOL_KEYWORDS.outcome,
  ];

  return allKeywords.some(kw => searchText.includes(kw));
}
