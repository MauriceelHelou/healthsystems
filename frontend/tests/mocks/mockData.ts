import type { Mechanism } from '../../src/types/mechanism';

/**
 * Mock mechanisms for testing - using correct API schema
 */
export const mockMechanisms: Mechanism[] = [
  {
    id: 'housing_quality_respiratory',
    name: 'Housing Quality → Respiratory Health',
    from_node_id: 'Housing_Quality',
    from_node_name: 'Housing Quality',
    to_node_id: 'Respiratory_Health',
    to_node_name: 'Respiratory Health',
    direction: 'negative',
    category: 'built_environment',
    description: 'Poor housing quality increases respiratory health issues through exposure to mold, dust, and inadequate ventilation',
    evidence_quality: 'A',
    n_studies: 15,
    mechanism_pathway: [
      'Poor housing quality',
      'Increased exposure to mold and allergens',
      'Respiratory inflammation',
      'Increased asthma incidence',
    ],
    moderators: [
      { type: 'population', description: 'Age', effect: 'strengthens' },
      { type: 'population', description: 'Existing respiratory conditions', effect: 'strengthens' },
      { type: 'geographic', description: 'Time spent indoors', effect: 'strengthens' }
    ],
  },
  {
    id: 'income_healthcare_access',
    name: 'Income → Healthcare Access',
    from_node_id: 'Income',
    from_node_name: 'Income',
    to_node_id: 'Healthcare_Access',
    to_node_name: 'Healthcare Access',
    direction: 'positive',
    category: 'economic',
    description: 'Higher income increases healthcare access through insurance coverage and ability to afford care',
    evidence_quality: 'A',
    n_studies: 50,
    mechanism_pathway: [
      'Higher income',
      'Increased ability to afford insurance',
      'Better insurance coverage',
      'Improved healthcare access',
    ],
    moderators: [
      { type: 'policy', description: 'Employment status', effect: 'strengthens' },
      { type: 'geographic', description: 'Geographic location', effect: 'modifies' },
      { type: 'policy', description: 'Insurance market', effect: 'modifies' }
    ],
  },
  {
    id: 'housing_instability_mental_health',
    name: 'Housing Instability → Mental Health',
    from_node_id: 'Housing_Instability',
    from_node_name: 'Housing Instability',
    to_node_id: 'Mental_Health',
    to_node_name: 'Mental Health',
    direction: 'negative',
    category: 'social_environment',
    description: 'Housing instability leads to mental health deterioration through chronic stress and loss of social support',
    evidence_quality: 'B',
    n_studies: 8,
    mechanism_pathway: [
      'Housing instability',
      'Chronic stress and uncertainty',
      'Loss of social support networks',
      'Depression and anxiety',
    ],
    moderators: [
      { type: 'population', description: 'Social support', effect: 'weakens' },
      { type: 'population', description: 'Prior mental health', effect: 'strengthens' },
      { type: 'policy', description: 'Financial resources', effect: 'weakens' }
    ],
  },
  {
    id: 'education_employment',
    name: 'Education → Employment',
    from_node_id: 'Education_Level',
    from_node_name: 'Education Level',
    to_node_id: 'Employment_Status',
    to_node_name: 'Employment Status',
    direction: 'positive',
    category: 'economic',
    description: 'Higher education levels increase employment opportunities through skill development and credentialing',
    evidence_quality: 'A',
    n_studies: 100,
    mechanism_pathway: [
      'Higher education level',
      'Improved skills and qualifications',
      'Increased job market competitiveness',
      'Better employment opportunities',
    ],
    moderators: [
      { type: 'policy', description: 'Labor market conditions', effect: 'modifies' },
      { type: 'geographic', description: 'Geographic location', effect: 'modifies' },
      { type: 'population', description: 'Social networks', effect: 'strengthens' }
    ],
  },
  {
    id: 'food_insecurity_diabetes',
    name: 'Food Insecurity → Diabetes',
    from_node_id: 'Food_Insecurity',
    from_node_name: 'Food Insecurity',
    to_node_id: 'Diabetes_Prevalence',
    to_node_name: 'Diabetes Prevalence',
    direction: 'positive',
    category: 'economic',
    description: 'Food insecurity increases diabetes risk through poor diet quality and chronic stress',
    evidence_quality: 'B',
    n_studies: 12,
    mechanism_pathway: [
      'Food insecurity',
      'Reliance on calorie-dense, nutrient-poor foods',
      'Poor diet quality and chronic stress',
      'Increased diabetes risk',
    ],
    moderators: [
      { type: 'policy', description: 'Access to healthcare', effect: 'weakens' },
      { type: 'population', description: 'Physical activity', effect: 'weakens' },
      { type: 'geographic', description: 'Stress levels', effect: 'strengthens' }
    ],
  },
];

/**
 * Get a single mock mechanism by ID
 */
export const getMockMechanism = (id: string): Mechanism | undefined => {
  return mockMechanisms.find((m) => m.id === id);
};

/**
 * Get mock mechanisms filtered by category
 */
export const getMockMechanismsByCategory = (category: string): Mechanism[] => {
  return mockMechanisms.filter((m) => m.category === category);
};

/**
 * Get all unique nodes from mock mechanisms
 */
export const mockNodes = Array.from(
  new Set(
    mockMechanisms.flatMap((m) => [
      { id: m.from_node_id, label: m.from_node_name },
      { id: m.to_node_id, label: m.to_node_name },
    ])
  )
);

/**
 * Mock API responses
 */
export const mockApiResponses = {
  mechanisms: {
    list: {
      items: mockMechanisms,
      total: mockMechanisms.length,
      skip: 0,
      limit: 20,
    },
    single: mockMechanisms[0],
  },
  stats: {
    total_mechanisms: mockMechanisms.length,
    by_category: {
      built_environment: 1,
      economic: 3,
      social_environment: 1,
    },
    by_direction: {
      positive: 3,
      negative: 2,
    },
    evidence_quality: {
      A: 3,
      B: 2,
    },
  },
};

/**
 * Generate a mock mechanism with specified properties
 */
export function createMockMechanism(overrides: Partial<Mechanism> = {}): Mechanism {
  return {
    id: 'test_mechanism',
    name: 'Test Mechanism',
    from_node_id: 'test_from',
    from_node_name: 'Test From Node',
    to_node_id: 'test_to',
    to_node_name: 'Test To Node',
    direction: 'positive',
    category: 'economic',
    description: 'Test mechanism description',
    evidence_quality: 'A',
    n_studies: 10,
    mechanism_pathway: ['Step 1', 'Step 2', 'Step 3'],
    moderators: [
      { type: 'policy', description: 'Test Moderator', effect: 'strengthens' }
    ],
    ...overrides,
  };
}
