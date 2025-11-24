/**
 * Mock Data Generator for HealthSystems Dashboard
 * Generates realistic test data for 400 nodes and 2000+ mechanisms
 */

import type { MechanismNode, MechanismEdge, Mechanism, Citation, Moderator, Pathway, Category, StockType, NodeScale } from '../types'

const categories: Category[] = [
  'built_environment',
  'social_environment',
  'economic',
  'political',
  'biological',
  'behavioral',
  'healthcare_access',
]

// Removed unused constants to fix TS6133 errors
// const stockTypes: StockType[] = ['structural', 'proxy', 'crisis']
// const categoryLabels: Record<Category, string> = {...}

// Sample node names by category
const nodeNamesByCategory: Record<Category | 'default', string[]> = {
  built_environment: [
    'Community Health Workers',
    'Affordable Housing Units',
    'Primary Care Facilities',
    'Public Transit Access',
    'Green Space Availability',
    'Walkability Index',
    'Food Retail Access',
    'Healthcare Facility Density',
  ],
  social_environment: [
    'Community Trust Index',
    'Social Cohesion Score',
    'Healthcare Continuity Index',
    'Provider Trust Score',
    'Social Support Networks',
    'Community Engagement',
    'Civic Participation',
  ],
  economic: [
    'Employment Rate',
    'Income Stability',
    'Economic Precarity Index',
    'Housing Affordability',
    'Wage Growth',
    'Job Quality Index',
    'Financial Security',
  ],
  political: [
    'Medicaid Expansion',
    'CHW Certification Programs',
    'Zoning Regulations',
    'Healthcare Policy',
    'Public Health Funding',
    'Regulatory Environment',
  ],
  biological: [
    'Primary Care Visits',
    'Preventive Care Utilization',
    'Chronic Disease Management',
    'Medication Adherence',
    'Health Behaviors',
  ],
  behavioral: [
    'Physical Activity',
    'Diet Quality',
    'Smoking Behavior',
    'Alcohol Use',
    'Stress Management',
  ],
  healthcare_access: [
    'Insurance Coverage',
    'Provider Availability',
    'Transportation to Care',
    'Telehealth Access',
    'Appointment Wait Times',
  ],
  default: [],
}

const crisisOutcomes = [
  'ED Visits',
  'Hospitalizations',
  'Premature Deaths',
  'Chronic Disease Burden',
  'Mental Health Crises',
]

// Generate deterministic random numbers (seeded)
let seed = 12345
function random() {
  const x = Math.sin(seed++) * 10000
  return x - Math.floor(x)
}

function randomInt(min: number, max: number): number {
  return Math.floor(random() * (max - min + 1)) + min
}

function randomChoice<T>(array: T[]): T {
  return array[Math.floor(random() * array.length)]
}

// Removed unused helper function randomSample to fix TS6133
// function randomSample<T>(array: T[], count: number): T[] {
//   const shuffled = [...array].sort(() => random() - 0.5)
//   return shuffled.slice(0, count)
// }

/**
 * Generate mock nodes (400 total)
 */
export function generateMockNodes(): MechanismNode[] {
  const nodes: MechanismNode[] = []
  let idCounter = 1

  // Generate crisis outcomes first (5% of nodes)
  crisisOutcomes.forEach((name) => {
    nodes.push({
      id: `node_${String(idCounter).padStart(3, '0')}`,
      label: name,
      category: 'default',
      stockType: 'crisis',
      scale: 7, // Crisis Endpoints
      weight: randomInt(30, 50), // High connection count
      connections: { outgoing: 0, incoming: randomInt(30, 50) },
    })
    idCounter++
  })

  // Generate nodes for each category
  categories.forEach((category) => {
    const baseNames = nodeNamesByCategory[category]
    const nodeCount = category === 'built_environment' ? 100 :
                      category === 'social_environment' ? 80 :
                      category === 'economic' ? 60 :
                      category === 'political' ? 40 : 35

    // Map categories to scales (distribute across 1-6, crisis is already 7)
    const categoryToScales: Record<Category, number[]> = {
      political: [1, 1, 1, 3], // Mostly Scale 1 (Structural), some Scale 3 (Institutional)
      built_environment: [2, 2, 2, 3], // Mostly Scale 2 (Built Environment), some Scale 3
      economic: [1, 3, 4, 4], // Mix of Structural, Institutional, Individual Conditions
      social_environment: [4, 4, 4, 5], // Mostly Scale 4 (Conditions), some Scale 5 (Behaviors)
      behavioral: [5, 5, 5, 6], // Mostly Scale 5 (Behaviors), some Scale 6 (Pathways)
      healthcare_access: [3, 4, 6, 6], // Mix of Institutional, Conditions, Pathways
      biological: [6, 6, 6, 6], // Mostly Scale 6 (Intermediate Pathways)
      default: [4, 4, 5, 6], // Default fallback
    }

    for (let i = 0; i < nodeCount; i++) {
      const baseName = randomChoice(baseNames)
      const suffix = i > baseNames.length - 1 ? ` ${i + 1}` : ''
      const stockType: StockType = i < nodeCount * 0.4 ? 'structural' : 'proxy'
      const scaleOptions = categoryToScales[category] || [4, 4, 5, 6]
      const scale = randomChoice(scaleOptions) as NodeScale

      nodes.push({
        id: `node_${String(idCounter).padStart(3, '0')}`,
        label: `${baseName}${suffix}`,
        category,
        stockType,
        scale,
        weight: randomInt(5, 30),
        connections: { outgoing: randomInt(3, 25), incoming: randomInt(2, 20) },
      })
      idCounter++
    }
  })

  // Pad to 400 nodes with default category
  while (nodes.length < 400) {
    const scales: NodeScale[] = [1, 2, 3, 4, 5, 6, 7]
    nodes.push({
      id: `node_${String(idCounter).padStart(3, '0')}`,
      label: `Node ${idCounter}`,
      category: 'default',
      stockType: 'structural',
      scale: randomChoice(scales),
      weight: randomInt(5, 15),
      connections: { outgoing: randomInt(3, 15), incoming: randomInt(2, 12) },
    })
    idCounter++
  }

  return nodes
}

/**
 * Generate mock edges (2000+ total)
 */
export function generateMockEdges(nodes: MechanismNode[]): MechanismEdge[] {
  const edges: MechanismEdge[] = []
  let edgeIdCounter = 1

  const structuralNodes = nodes.filter(n => n.stockType === 'structural')
  const proxyNodes = nodes.filter(n => n.stockType === 'proxy')
  const crisisNodes = nodes.filter(n => n.stockType === 'crisis')

  // Helper to create edge
  const createEdge = (source: MechanismNode, target: MechanismNode): MechanismEdge => {
    const qualities: Array<'A' | 'B' | 'C' | null> = ['A', 'B', 'C', null]
    const quality = randomChoice(qualities)

    return {
      id: `edge_${String(edgeIdCounter++).padStart(4, '0')}`,
      source: source.id,
      target: target.id,
      direction: random() > 0.3 ? 'positive' : 'negative',
      strength: random() * 0.8 + 0.2,
      evidenceQuality: quality,
      studyCount: quality ? randomInt(3, 25) : 0,
    }
  }

  // Generate edges: Structural → Proxy (40% of edges)
  for (let i = 0; i < 800; i++) {
    const source = randomChoice(structuralNodes)
    const target = randomChoice(proxyNodes)
    if (source.id !== target.id) {
      edges.push(createEdge(source, target))
    }
  }

  // Generate edges: Proxy → Proxy (30% of edges)
  for (let i = 0; i < 600; i++) {
    const source = randomChoice(proxyNodes)
    const target = randomChoice(proxyNodes)
    if (source.id !== target.id) {
      edges.push(createEdge(source, target))
    }
  }

  // Generate edges: Proxy → Crisis (20% of edges)
  for (let i = 0; i < 400; i++) {
    const source = randomChoice(proxyNodes)
    const target = randomChoice(crisisNodes)
    edges.push(createEdge(source, target))
  }

  // Generate edges: Structural → Crisis (10% of edges)
  for (let i = 0; i < 200; i++) {
    const source = randomChoice(structuralNodes)
    const target = randomChoice(crisisNodes)
    edges.push(createEdge(source, target))
  }

  // Add some feedback loops (Proxy → Structural)
  for (let i = 0; i < 50; i++) {
    const source = randomChoice(proxyNodes)
    const target = randomChoice(structuralNodes)
    if (source.id !== target.id) {
      edges.push(createEdge(source, target))
    }
  }

  return edges
}

/**
 * Generate mock mechanism details
 */
export function generateMockMechanism(edge: MechanismEdge, nodes: MechanismNode[]): Mechanism {
  const sourceNode = nodes.find(n => n.id === edge.source)!
  const targetNode = nodes.find(n => n.id === edge.target)!

  const citations: Citation[] = []
  for (let i = 0; i < edge.studyCount; i++) {
    citations.push({
      id: `citation_${edge.id}_${i}`,
      authors: randomChoice(['Smith et al.', 'Johnson et al.', 'Williams et al.', 'Brown et al.', 'Davis et al.']),
      year: randomInt(2010, 2024),
      title: `Impact of ${sourceNode.label} on ${targetNode.label}`,
      journal: randomChoice(['Health Affairs', 'JAMA', 'NEJM', 'Lancet', 'Am J Public Health']),
      doi: `10.1001/jama.${randomInt(2010, 2024)}.${randomInt(1000, 9999)}`,
      url: `https://pubmed.ncbi.nlm.nih.gov/${randomInt(10000000, 40000000)}`,
    })
  }

  const moderators: Moderator[] = []
  if (random() > 0.5) {
    moderators.push({
      type: 'policy',
      category: 'policy',
      description: 'Effect stronger when supportive policies are in place',
      effect: 'strengthens',
    })
  }
  if (random() > 0.6) {
    moderators.push({
      type: 'geographic',
      category: 'geographic',
      description: 'Effect varies between urban and rural contexts',
      effect: 'varies',
    })
  }

  const directionText = edge.direction === 'positive' ? 'increases' : 'decreases'
  const mechanismPathway = [
    sourceNode.label,
    'Improved access and coordination',
    'Sustained engagement',
    targetNode.label,
  ]

  return {
    id: edge.id,
    name: `${sourceNode.label} → ${targetNode.label}`,
    from_node_id: edge.source,
    from_node_name: sourceNode.label,
    to_node_id: edge.target,
    to_node_name: targetNode.label,
    direction: edge.direction,
    category: edge.category || 'default',
    description: `${sourceNode.label} ${directionText} ${targetNode.label} through improved access, coordination, and sustained engagement. Research shows consistent effects across diverse populations and settings.`,
    evidence_quality: edge.evidenceQuality,
    n_studies: edge.studyCount,
    mechanism_pathway: mechanismPathway,
    citations,
    moderators,
  }
}

/**
 * Generate mock pathways
 */
export function generateMockPathways(
  interventionNodeId: string,
  outcomeNodeId: string,
  nodes: MechanismNode[],
  edges: MechanismEdge[]
): Pathway[] {
  const pathways: Pathway[] = []

  // Simple BFS to find paths
  const findPaths = (start: string, end: string, maxDepth: number = 4): string[][] => {
    const paths: string[][] = []
    const queue: { nodeId: string; path: string[] }[] = [{ nodeId: start, path: [start] }]
    const visited = new Set<string>()

    while (queue.length > 0 && paths.length < 5) {
      const { nodeId, path } = queue.shift()!

      if (nodeId === end) {
        paths.push(path)
        continue
      }

      if (path.length >= maxDepth) continue
      if (visited.has(nodeId)) continue
      visited.add(nodeId)

      const outgoingEdges = edges.filter(e => e.source === nodeId)
      for (const edge of outgoingEdges) {
        if (!path.includes(edge.target)) {
          queue.push({ nodeId: edge.target, path: [...path, edge.target] })
        }
      }
    }

    return paths
  }

  const nodePaths = findPaths(interventionNodeId, outcomeNodeId)

  nodePaths.forEach((nodePath, index) => {
    const mechanisms: Mechanism[] = []
    let lowestQuality: 'A' | 'B' | 'C' = 'A'

    for (let i = 0; i < nodePath.length - 1; i++) {
      const edge = edges.find(e => e.source === nodePath[i] && e.target === nodePath[i + 1])
      if (edge) {
        mechanisms.push(generateMockMechanism(edge, nodes))
        if (edge.evidenceQuality === 'C') lowestQuality = 'C'
        else if (edge.evidenceQuality === 'B' && lowestQuality !== 'C') lowestQuality = 'B'
      }
    }

    // Determine overall direction
    const negativeCount = mechanisms.filter(m => m.direction === 'negative').length
    const overallDirection = negativeCount % 2 === 0 ? 'positive' : 'negative'

    pathways.push({
      id: `pathway_${index + 1}`,
      fromNodeId: interventionNodeId,
      toNodeId: outcomeNodeId,
      interventionNodeId,
      outcomeNodeId,
      mechanisms,
      overallEvidence: lowestQuality,
      aggregateQuality: lowestQuality,
      overallDirection,
      pathLength: mechanisms.length,
    })
  })

  return pathways
}

/**
 * Main mock data generation
 */
export function generateMockData() {
  const nodes = generateMockNodes()
  const edges = generateMockEdges(nodes)

  return {
    nodes,
    edges,
    network: { nodes, edges },
  }
}

// Generate and export the data
export const mockData = generateMockData()
export const mockNodes = mockData.nodes
export const mockEdges = mockData.edges
