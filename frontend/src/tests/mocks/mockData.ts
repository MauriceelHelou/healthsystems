import { Mechanism } from '../../types/mechanism';

/**
 * Mock mechanisms for testing
 */
export const mockMechanisms: Mechanism[] = [
  {
    id: 'housing_quality_respiratory',
    name: 'Housing Quality → Respiratory Health',
    description: 'Poor housing quality increases respiratory health issues through exposure to mold, dust, and inadequate ventilation',
    source_node: 'Housing_Quality',
    target_node: 'Respiratory_Health',
    source_node_label: 'Housing Quality',
    target_node_label: 'Respiratory Health',
    directionality: 'negative',
    category: 'structural',
    mechanism_type: 'causal_pathway',
    causal_pathway: [
      'Poor housing quality',
      'Increased exposure to mold and allergens',
      'Respiratory inflammation',
      'Increased asthma incidence',
    ],
    moderators: ['Age', 'Existing respiratory conditions', 'Time spent indoors'],
    evidence_quality: 'A',
    n_studies: 15,
    spatial_variation: 'high',
    temporal_variation: 'medium',
    structural_competency_notes: 'Housing quality is heavily influenced by systemic factors including redlining, discriminatory lending, and exclusionary zoning',
    created_at: '2024-11-17T10:00:00Z',
    updated_at: '2024-11-17T10:00:00Z',
  },
  {
    id: 'income_healthcare_access',
    name: 'Income → Healthcare Access',
    description: 'Higher income increases healthcare access through insurance coverage and ability to afford care',
    source_node: 'Income',
    target_node: 'Healthcare_Access',
    source_node_label: 'Income',
    target_node_label: 'Healthcare Access',
    directionality: 'positive',
    category: 'economic',
    mechanism_type: 'causal_pathway',
    causal_pathway: [
      'Higher income',
      'Increased ability to afford insurance',
      'Better insurance coverage',
      'Improved healthcare access',
    ],
    moderators: ['Employment status', 'Geographic location', 'Insurance market'],
    evidence_quality: 'A',
    n_studies: 50,
    spatial_variation: 'high',
    temporal_variation: 'low',
    structural_competency_notes: 'Income-based healthcare access reflects systemic inequities in healthcare financing and labor market segmentation',
    created_at: '2024-11-17T10:00:00Z',
    updated_at: '2024-11-17T10:00:00Z',
  },
  {
    id: 'eviction_mental_health',
    name: 'Eviction → Mental Health',
    description: 'Eviction negatively impacts mental health through stress, housing instability, and trauma',
    source_node: 'Eviction',
    target_node: 'Mental_Health',
    source_node_label: 'Eviction',
    target_node_label: 'Mental Health',
    directionality: 'negative',
    category: 'structural',
    mechanism_type: 'causal_pathway',
    causal_pathway: [
      'Eviction event',
      'Housing instability and stress',
      'Chronic psychological distress',
      'Depression and anxiety',
    ],
    moderators: ['Social support', 'Prior mental health', 'Financial resources'],
    evidence_quality: 'B',
    n_studies: 8,
    spatial_variation: 'medium',
    temporal_variation: 'medium',
    structural_competency_notes: 'Eviction patterns reflect racialized housing discrimination and landlord-tenant power imbalances',
    created_at: '2024-11-17T10:00:00Z',
    updated_at: '2024-11-17T10:00:00Z',
  },
  {
    id: 'education_employment',
    name: 'Education → Employment Opportunities',
    description: 'Higher educational attainment increases employment opportunities',
    source_node: 'Education',
    target_node: 'Employment_Opportunities',
    source_node_label: 'Education',
    target_node_label: 'Employment Opportunities',
    directionality: 'positive',
    category: 'intermediate',
    mechanism_type: 'causal_pathway',
    causal_pathway: [
      'Educational attainment',
      'Skill development',
      'Increased job qualifications',
      'Better employment opportunities',
    ],
    moderators: ['Labor market conditions', 'Geographic location', 'Social networks'],
    evidence_quality: 'A',
    n_studies: 100,
    spatial_variation: 'medium',
    temporal_variation: 'low',
    structural_competency_notes: 'Educational returns vary by race and gender due to labor market discrimination',
    created_at: '2024-11-17T10:00:00Z',
    updated_at: '2024-11-17T10:00:00Z',
  },
  {
    id: 'food_insecurity_diabetes',
    name: 'Food Insecurity → Type 2 Diabetes',
    description: 'Food insecurity increases type 2 diabetes risk through poor diet quality and stress',
    source_node: 'Food_Insecurity',
    target_node: 'Type_2_Diabetes',
    source_node_label: 'Food Insecurity',
    target_node_label: 'Type 2 Diabetes',
    directionality: 'positive',
    category: 'structural',
    mechanism_type: 'causal_pathway',
    causal_pathway: [
      'Food insecurity',
      'Reliance on calorie-dense, nutrient-poor foods',
      'Poor glycemic control',
      'Increased diabetes risk',
    ],
    moderators: ['Access to healthcare', 'Physical activity', 'Stress levels'],
    evidence_quality: 'B',
    n_studies: 12,
    spatial_variation: 'high',
    temporal_variation: 'medium',
    structural_competency_notes: 'Food insecurity is shaped by food apartheid, SNAP policy, and minimum wage levels',
    created_at: '2024-11-17T10:00:00Z',
    updated_at: '2024-11-17T10:00:00Z',
  },
];

/**
 * Get a single mock mechanism by ID
 */
export const getMockMechanism = (id: string): Mechanism | undefined => {
  return mockMechanisms.find((m) => m.id === id);
};

/**
 * Filter mock mechanisms by category
 */
export const getMockMechanismsByCategory = (category: string): Mechanism[] => {
  return mockMechanisms.filter((m) => m.category === category);
};

/**
 * Mock nodes derived from mechanisms
 */
export const mockNodes = Array.from(
  new Set(
    mockMechanisms.flatMap((m) => [
      { id: m.source_node, label: m.source_node_label },
      { id: m.target_node, label: m.target_node_label },
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
      structural: 3,
      economic: 1,
      intermediate: 1,
    },
    by_directionality: {
      positive: 2,
      negative: 3,
    },
    evidence_quality: {
      A: 3,
      B: 2,
    },
  },
};

/**
 * Generate a mock mechanism with custom properties
 */
export const createMockMechanism = (
  overrides: Partial<Mechanism> = {}
): Mechanism => {
  return {
    id: 'test_mechanism',
    name: 'Test Mechanism',
    description: 'A test mechanism for testing purposes',
    source_node: 'Test_Source',
    target_node: 'Test_Target',
    source_node_label: 'Test Source',
    target_node_label: 'Test Target',
    directionality: 'positive',
    category: 'structural',
    mechanism_type: 'causal_pathway',
    causal_pathway: ['Step 1', 'Step 2', 'Step 3'],
    moderators: ['Moderator 1'],
    evidence_quality: 'A',
    n_studies: 10,
    spatial_variation: 'medium',
    temporal_variation: 'medium',
    structural_competency_notes: 'Test notes',
    created_at: '2024-11-17T10:00:00Z',
    updated_at: '2024-11-17T10:00:00Z',
    ...overrides,
  };
};
