/**
 * MechanismGraph - Hierarchical visualization for causal mechanisms
 *
 * Left-to-right hierarchical layout showing causal progression from upstream
 * structural determinants (left) to downstream crisis outcomes (right).
 * Styled to match the reference systems map with clean white nodes and bezier curves.
 * Only displays nodes with active mechanisms (connected nodes).
 */

import React, { useEffect, useRef } from 'react';
import * as d3 from 'd3';
import { SystemsNetwork, MechanismNode, MechanismEdge, ImportantNodesHighlight, ActivePaths, GraphLayoutMode, PhysicsSettings, CrisisHighlight, HierarchyLevel } from '../types/mechanism';
import { useGraphStateStore } from '../stores/graphStateStore';
import { HierarchicalMechanismNode } from '../utils/graphBuilder';

interface MechanismGraphProps {
  data: SystemsNetwork;
  width?: number;
  height?: number;
  onNodeClick?: (node: MechanismNode) => void;
  onEdgeClick?: (edge: MechanismEdge) => void;
  selectedNodeId?: string | null;
  selectedEdgeId?: string | null;
  filteredCategories?: string[];
  showLegend?: boolean;

  // New props for node importance highlighting
  importantNodes?: ImportantNodesHighlight;

  // New props for path highlighting
  activePaths?: ActivePaths;

  // New props for crisis explorer highlighting
  crisisHighlight?: CrisisHighlight;

  // Interactive node selection for pathfinder
  selectionMode?: 'none' | 'from' | 'to';
  onNodeSelect?: (nodeId: string, nodeLabel: string) => void;

  // Layout mode props
  layoutMode?: GraphLayoutMode;
  physicsSettings?: PhysicsSettings;

  // Hierarchy props (NEW)
  /** Enable hierarchical mode with expand/collapse */
  enableHierarchy?: boolean;
  /** Set of currently expanded node IDs */
  expandedNodeIds?: Set<string>;
  /** Callback when node expand/collapse is toggled */
  onNodeToggleExpand?: (nodeId: string) => void;
  /** Filter by hierarchy levels */
  hierarchyLevelFilter?: HierarchyLevel[];
}

// Map node scale (1-7) to visualization levels (1-7) - direct mapping
const SCALE_TO_LEVEL_MAPPING: Record<number, number> = {
  1: 1, // Structural Determinants (policy)
  2: 2, // Built Environment & Infrastructure
  3: 3, // Institutional Infrastructure
  4: 4, // Individual/Household Conditions
  5: 5, // Individual Behaviors & Psychosocial
  6: 6, // Intermediate Pathways
  7: 7, // Crisis Endpoints
};

// Level descriptions (7-scale system)
const LEVEL_LABELS = [
  'Structural\nDeterminants',
  'Built\nEnvironment',
  'Institutional\nInfrastructure',
  'Individual\nConditions',
  'Individual\nBehaviors',
  'Intermediate\nPathways',
  'Crisis\nEndpoints',
];

// Assign level to each node based on category and scale
const getNodeLevel = (node: MechanismNode): number => {
  // Use scale field if available
  if (node.scale && SCALE_TO_LEVEL_MAPPING[node.scale]) {
    return SCALE_TO_LEVEL_MAPPING[node.scale];
  }

  // Map category to level (7-scale hierarchy)
  const categoryToLevel: Record<string, number> = {
    // Scale 1: Structural Determinants (policy level)
    political: 1,

    // Scale 2: Built Environment & Infrastructure
    built_environment: 2,

    // Scale 3: Institutional Infrastructure
    healthcare_access: 3,

    // Scale 4: Individual/Household Conditions
    economic: 4, // Economic security, household income
    social_environment: 4, // Social connectedness, discrimination

    // Scale 5: Individual Behaviors & Psychosocial
    behavioral: 5,

    // Scale 6: Intermediate Pathways
    biological: 6, // Clinical measures, utilization

    // Scale 7: Crisis Endpoints
    default: 4, // Default to individual conditions
  };

  if (node.category && categoryToLevel[node.category]) {
    return categoryToLevel[node.category];
  }

  // Fallback to stockType if category doesn't match
  if (node.stockType === 'structural') return 1;
  if (node.stockType === 'crisis') return 7; // Updated from 5 to 7

  // Default to middle level
  return 4; // Updated from 3 to 4
};

// Filter to show only nodes with active mechanisms (connected nodes)
const filterConnectedNodes = (
  nodes: MechanismNode[],
  edges: MechanismEdge[]
): MechanismNode[] => {
  // Create set of node IDs that appear in edges
  const connectedNodeIds = new Set<string>();

  edges.forEach((edge) => {
    const sourceId = typeof edge.source === 'string' ? edge.source : (edge.source as any).id;
    const targetId = typeof edge.target === 'string' ? edge.target : (edge.target as any).id;
    connectedNodeIds.add(sourceId);
    connectedNodeIds.add(targetId);
  });

  // Filter nodes to only include connected ones
  return nodes.filter((node) => connectedNodeIds.has(node.id));
};

// Reference map styling - uniform white nodes with gray borders
const NODE_STYLE = {
  width: 120,
  height: 35, // Will be dynamically adjusted based on text
  rx: 3,
  fill: '#FFFFFF',
  stroke: '#333',
  strokeWidth: 2, // Increased from 1 for better visibility
  fontSize: 10.8,
  fontWeight: 500,
  fontFamily: "'Nobel', 'Avenir', 'Futura', Arial, sans-serif",
  padding: 8,
};

// Edge styling
const EDGE_STYLE = {
  stroke: '#888',
  strokeWidth: 2.5, // Increased from 0.8 for better visibility at all zoom levels
  hitboxWidth: 8, // Transparent hitbox for easier clicking
};

// Hierarchy expand/collapse indicator styling
const HIERARCHY_INDICATOR_STYLE = {
  size: 14,
  strokeWidth: 1.5,
  fill: '#fff',
  stroke: '#666',
  expandedIcon: '−', // minus
  collapsedIcon: '+', // plus
  fontSize: 12,
  fontWeight: 'bold',
};

// Hover effects
const HOVER_STYLE = {
  nodeFill: '#f8f8f8',
  nodeStroke: '#FF8C00',
  nodeFontWeight: 600,
  edgeStroke: '#333',
  edgeStrokeWidth: 1.0,
  glowColor: '#FF8C00',
  glowOpacity: 0.45,
};

const MechanismGraph: React.FC<MechanismGraphProps> = ({
  data,
  width = 1200, // Responsive default
  height = 800, // Responsive default
  onNodeClick,
  onEdgeClick,
  selectedNodeId,
  selectedEdgeId,
  showLegend = false, // Disabled by default for clean look
  importantNodes,
  activePaths,
  crisisHighlight,
  selectionMode = 'none',
  onNodeSelect,
  layoutMode = 'hierarchical', // Default to hierarchical layout
  physicsSettings,
  // Hierarchy props
  enableHierarchy = false,
  expandedNodeIds,
  onNodeToggleExpand,
  hierarchyLevelFilter: _hierarchyLevelFilter,
}) => {
  const svgRef = useRef<SVGSVGElement>(null);
  const simulationRef = useRef<d3.Simulation<any, undefined> | null>(null);
  const zoomBehaviorRef = useRef<d3.ZoomBehavior<SVGSVGElement, unknown> | null>(null);
  const nodePositionsRef = useRef<Map<string, { x: number; y: number; width: number; height: number }>>(new Map());
  const zoomTransformRef = useRef<d3.ZoomTransform | null>(null); // Preserve zoom position across redraws

  // Get zoom request state from store
  const { zoomToNodeId, zoomToPaths, clearZoomRequest, clearZoomToPathsRequest } = useGraphStateStore();

  // Main effect: Draw the graph (only when data or layout mode changes)
  // CRITICAL: Don't include selectedNodeId or other interactive props in dependencies
  // to prevent complete redraw on every interaction
  useEffect(() => {
    if (!svgRef.current || !data.nodes.length) return;

    // Filter to show only connected nodes
    let connectedNodes = filterConnectedNodes(data.nodes, data.edges);

    if (connectedNodes.length === 0) {
      // Fallback: show all nodes if filtering removes everything
      connectedNodes = data.nodes;
    }

    // Clear previous visualization
    d3.select(svgRef.current).selectAll('*').remove();

    // Layout parameters
    const marginLeft = 150;
    const marginRight = 50;
    const marginTop = 80; // Increased from 60 to accommodate larger scale labels
    const marginBottom = 40;
    const numLevels = 7; // Updated for 7-scale system
    const edgeSpacing = 16; // Increased from 8 to 16 for better readability

    // Pre-calculate content dimensions to determine if we need larger canvas
    const calculateNodeHeight = (label: string): number => {
      const words = label.split(/[\s_]+/);
      const maxCharsPerLine = 18;
      let lines = 0;
      let currentLine = '';

      words.forEach((word) => {
        if ((currentLine + ' ' + word).trim().length <= maxCharsPerLine) {
          currentLine = (currentLine + ' ' + word).trim();
        } else {
          if (currentLine) lines++;
          currentLine = word;
        }
      });
      if (currentLine) lines++;

      const lineHeight = 13;
      const minLines = Math.min(lines, 3);
      return NODE_STYLE.padding * 2 + minLines * lineHeight;
    };

    // Group nodes by level to calculate required height
    const nodesByLevel: Record<number, MechanismNode[]> = {};
    connectedNodes.forEach((node) => {
      const level = getNodeLevel(node);
      if (!nodesByLevel[level]) {
        nodesByLevel[level] = [];
      }
      nodesByLevel[level].push(node);
    });

    // Find the level with most nodes and calculate required height
    let maxLevelHeight = 0;
    Object.values(nodesByLevel).forEach((nodes) => {
      const nodeHeights = nodes.map((n) => calculateNodeHeight(n.label));
      const totalHeight = nodeHeights.reduce((sum, h) => sum + h + edgeSpacing, -edgeSpacing);
      maxLevelHeight = Math.max(maxLevelHeight, totalHeight);
    });

    // Calculate actual dimensions needed (use larger of provided or calculated)
    const requiredHeight = maxLevelHeight + marginTop + marginBottom;
    const actualWidth = width;
    const actualHeight = Math.max(height, requiredHeight);

    const availableWidth = actualWidth - marginLeft - marginRight;
    const availableHeight = actualHeight - marginTop - marginBottom;
    const levelSpacing = (availableWidth / (numLevels - 1)) * 2;

    // Create SVG with calculated dimensions
    const svg = d3
      .select(svgRef.current)
      .attr('width', actualWidth)
      .attr('height', actualHeight)
      .attr('viewBox', `0 0 ${actualWidth} ${actualHeight}`)
      .attr('role', 'img')
      .attr('aria-label', 'Hierarchical causal mechanism network diagram');

    // Add description for screen readers
    svg
      .append('desc')
      .text(
        `Hierarchical network diagram showing ${connectedNodes.length} nodes ` +
        `and ${data.edges.length} causal mechanisms. ` +
        `Flows left to right from structural factors to crisis endpoints.`
      );

    // Create main graph container
    const graph = svg
      .append('g')
      .attr('class', 'graph-container')
      .attr('transform', `translate(${marginLeft}, ${marginTop})`);

    // Create zoom behavior
    const zoom = d3.zoom<SVGSVGElement, unknown>()
      .scaleExtent([0.1, 1000]) // Allow zoom from 10% to 100,000%
      .on('zoom', (event) => {
        zoomTransformRef.current = event.transform; // Save current transform to preserve across redraws
        graph.attr('transform', event.transform.toString());
      });

    // Apply zoom behavior to SVG
    svg.call(zoom as any);
    zoomBehaviorRef.current = zoom; // Store in ref for zoom effect

    // Restore previous zoom transform or set initial position
    // This prevents the view from resetting when clicking nodes/edges
    if (zoomTransformRef.current) {
      // Restore saved zoom position
      svg.call(zoom.transform as any, zoomTransformRef.current);
    } else {
      // Set initial zoom with reasonable default scale for readability
      // Use 0.8 as default, or fit to height if diagram is small enough
      const fitScale = height / actualHeight;
      const initialScale = fitScale > 0.6 ? Math.min(1, fitScale) : 0.8;

      // Center the diagram horizontally
      const translateX = (width - actualWidth * initialScale) / 2;

      svg.call(
        zoom.transform as any,
        d3.zoomIdentity.translate(translateX, marginTop).scale(initialScale)
      );
    }

    // Calculate positions for each node
    const nodePositions = new Map<string, { x: number; y: number; width: number; height: number }>();
    nodePositionsRef.current = nodePositions; // Store in ref for zoom effect

    // Hierarchical layout positioning
    if (layoutMode === 'hierarchical') {
      Object.entries(nodesByLevel).forEach(([levelStr, nodes]) => {
        const level = parseInt(levelStr);
        const x = (level - 1) * levelSpacing;

        // Calculate total height for vertical centering
        const nodeHeights = nodes.map((n) => calculateNodeHeight(n.label));
        const totalHeight = nodeHeights.reduce((sum, h) => sum + h + edgeSpacing, -edgeSpacing);
        let currentY = (availableHeight - totalHeight) / 2;

        nodes.forEach((node, i) => {
          const nodeHeight = nodeHeights[i];
          nodePositions.set(node.id, {
            x,
            y: currentY + nodeHeight / 2,
            width: NODE_STYLE.width,
            height: nodeHeight,
          });
          currentY += nodeHeight + edgeSpacing;
        });
      });
    } else {
      // Force-directed layout: Initialize with random positions
      // (Will be updated by simulation)
      connectedNodes.forEach((node) => {
        const nodeHeight = calculateNodeHeight(node.label);
        nodePositions.set(node.id, {
          x: Math.random() * availableWidth,
          y: Math.random() * availableHeight,
          width: NODE_STYLE.width,
          height: nodeHeight,
        });
      });
    }

    // Add level labels at top (only for hierarchical mode)
    if (layoutMode === 'hierarchical') {
      for (let i = 0; i < numLevels; i++) {
        graph
          .append('text')
          .text(LEVEL_LABELS[i])
          .attr('x', i * levelSpacing)
          .attr('y', -40) // Adjusted for larger font size
          .attr('text-anchor', 'middle')
          .attr('font-size', '24px') // Doubled from 12px for better readability
          .attr('font-weight', '600')
          .attr('font-family', NODE_STYLE.fontFamily)
          .attr('fill', '#666')
          .attr('pointer-events', 'none');
      }
    }

    // Create curved path for edges
    const createCurvedPath = (
      sourceX: number,
      sourceY: number,
      targetX: number,
      targetY: number
    ): string => {
      const controlX = (sourceX + targetX) / 2;
      const midY = (sourceY + targetY) / 2;
      return `M ${sourceX} ${sourceY} Q ${controlX} ${sourceY}, ${controlX} ${midY} T ${targetX} ${targetY}`;
    };

    // Create defs for arrow markers
    const defs = svg.append('defs');

    defs
      .append('marker')
      .attr('id', 'arrow-positive')
      .attr('viewBox', '0 -5 10 10')
      .attr('refX', 10)
      .attr('refY', 0)
      .attr('markerWidth', 6)
      .attr('markerHeight', 6)
      .attr('orient', 'auto')
      .append('path')
      .attr('d', 'M0,-5L10,0L0,5')
      .attr('fill', EDGE_STYLE.stroke);

    defs
      .append('marker')
      .attr('id', 'arrow-negative')
      .attr('viewBox', '0 -5 10 10')
      .attr('refX', 10)
      .attr('refY', 0)
      .attr('markerWidth', 6)
      .attr('markerHeight', 6)
      .attr('orient', 'auto')
      .append('path')
      .attr('d', 'M0,-5L10,0L0,5')
      .attr('fill', '#EF4444');

    // Draw edges with bezier curves
    const linkGroup = graph.append('g').attr('class', 'links');

    data.edges.forEach((edge) => {
      const sourceId = typeof edge.source === 'string' ? edge.source : (edge.source as any).id;
      const targetId = typeof edge.target === 'string' ? edge.target : (edge.target as any).id;

      const sourcePos = nodePositions.get(sourceId);
      const targetPos = nodePositions.get(targetId);

      if (!sourcePos || !targetPos) return;

      // Detect if this is a backwards edge (source is to the right of target)
      const isBackwardsEdge = sourcePos.x > targetPos.x;

      // Adjust edge endpoints based on flow direction
      let sourceX: number, targetX: number;
      if (isBackwardsEdge) {
        // Backwards edge: exit LEFT side of source, enter RIGHT side of target
        sourceX = sourcePos.x - sourcePos.width / 2;
        targetX = targetPos.x + targetPos.width / 2;
      } else {
        // Forward edge: exit RIGHT side of source, enter LEFT side of target
        sourceX = sourcePos.x + sourcePos.width / 2;
        targetX = targetPos.x - targetPos.width / 2;
      }
      const sourceY = sourcePos.y;
      const targetY = targetPos.y;

      const pathData = createCurvedPath(sourceX, sourceY, targetX, targetY);
      const isNegative = edge.direction === 'negative';

      // Create link group for each edge
      const linkEl = linkGroup.append('g').attr('class', 'link').datum(edge);

      // Transparent hitbox for easier clicking
      linkEl
        .append('path')
        .attr('d', pathData)
        .attr('stroke', 'transparent')
        .attr('stroke-width', EDGE_STYLE.hitboxWidth)
        .attr('fill', 'none')
        .style('cursor', onEdgeClick ? 'pointer' : 'default')
        .style('outline', 'none') // Remove browser focus outline (blue box)
        .attr('role', 'button')
        .attr('tabindex', onEdgeClick ? 0 : -1)
        .attr('aria-label', () => {
          const source = connectedNodes.find((n) => n.id === sourceId);
          const target = connectedNodes.find((n) => n.id === targetId);
          return `Mechanism from ${source?.label || sourceId} to ${target?.label || targetId}`;
        })
        .on('click', () => {
          if (onEdgeClick) onEdgeClick(edge);
        });

      // Visible edge with evidence quality indicated by opacity (subtle, no labels)
      const evidenceOpacity = edge.evidenceQuality === 'A' ? 1.0 :
                             edge.evidenceQuality === 'B' ? 0.8 :
                             edge.evidenceQuality === 'C' ? 0.6 : 0.7;

      const visiblePath = linkEl
        .append('path')
        .attr('d', pathData)
        .attr('stroke', isNegative ? '#EF4444' : EDGE_STYLE.stroke)
        .attr('stroke-width', EDGE_STYLE.strokeWidth)
        .attr('fill', 'none')
        .attr('opacity', evidenceOpacity) // Subtle evidence quality indication
        .attr('marker-end', `url(#arrow-${isNegative ? 'negative' : 'positive'})`)
        .attr('pointer-events', 'none');

      // Evidence quality removed from visual labels - clean graph
      // Quality is now subtly indicated by edge opacity only

      // Hover effects
      if (onEdgeClick) {
        linkEl.on('mouseenter', function () {
          visiblePath
            .attr('stroke', HOVER_STYLE.edgeStroke)
            .attr('stroke-width', HOVER_STYLE.edgeStrokeWidth)
            .attr('opacity', 1.0); // Full opacity on hover for visibility
        });

        linkEl.on('mouseleave', function () {
          visiblePath
            .attr('stroke', isNegative ? '#EF4444' : EDGE_STYLE.stroke)
            .attr('stroke-width', EDGE_STYLE.strokeWidth)
            .attr('opacity', evidenceOpacity); // Restore evidence-based opacity
        });
      }
    });

    // Helper function to update graph positions (used by force simulation)
    const updateGraphPositions = () => {
      // Update node group transforms
      nodeGroup.selectAll<SVGGElement, any>('g.node')
        .attr('transform', (d: any) => {
          const pos = nodePositions.get(d.id);
          return pos ? `translate(${pos.x}, ${pos.y})` : '';
        });

      // Update edge paths
      linkGroup.selectAll<SVGPathElement, MechanismEdge>('g.link path')
        .filter(function() {
          // Update only visible paths, not hitboxes
          return d3.select(this).attr('stroke') !== 'transparent';
        })
        .attr('d', (d: MechanismEdge) => {
          if (!d || !d.source || !d.target) return '';
          const sourceId = typeof d.source === 'string' ? d.source : (d.source as any).id;
          const targetId = typeof d.target === 'string' ? d.target : (d.target as any).id;
          const sourcePos = nodePositions.get(sourceId);
          const targetPos = nodePositions.get(targetId);
          if (!sourcePos || !targetPos) return '';

          // Detect backwards edge (source is to the right of target)
          const isBackwardsEdge = sourcePos.x > targetPos.x;
          let sourceX: number, targetX: number;
          if (isBackwardsEdge) {
            sourceX = sourcePos.x - sourcePos.width / 2;
            targetX = targetPos.x + targetPos.width / 2;
          } else {
            sourceX = sourcePos.x + sourcePos.width / 2;
            targetX = targetPos.x - targetPos.width / 2;
          }
          const sourceY = sourcePos.y;
          const targetY = targetPos.y;

          return createCurvedPath(sourceX, sourceY, targetX, targetY);
        });

      // Also update transparent hitboxes
      linkGroup.selectAll<SVGPathElement, MechanismEdge>('g.link path')
        .filter(function() {
          return d3.select(this).attr('stroke') === 'transparent';
        })
        .attr('d', (d: MechanismEdge) => {
          if (!d || !d.source || !d.target) return '';
          const sourceId = typeof d.source === 'string' ? d.source : (d.source as any).id;
          const targetId = typeof d.target === 'string' ? d.target : (d.target as any).id;
          const sourcePos = nodePositions.get(sourceId);
          const targetPos = nodePositions.get(targetId);
          if (!sourcePos || !targetPos) return '';

          // Detect backwards edge (source is to the right of target)
          const isBackwardsEdge = sourcePos.x > targetPos.x;
          let sourceX: number, targetX: number;
          if (isBackwardsEdge) {
            sourceX = sourcePos.x - sourcePos.width / 2;
            targetX = targetPos.x + targetPos.width / 2;
          } else {
            sourceX = sourcePos.x + sourcePos.width / 2;
            targetX = targetPos.x - targetPos.width / 2;
          }
          const sourceY = sourcePos.y;
          const targetY = targetPos.y;

          return createCurvedPath(sourceX, sourceY, targetX, targetY);
        });
    };

    // Draw nodes
    const nodeGroup = graph.append('g').attr('class', 'nodes');

    connectedNodes.forEach((node) => {
      const pos = nodePositions.get(node.id);
      if (!pos) return;

      // Check if node is important
      const isImportant = importantNodes?.nodeIds.includes(node.id) || false;
      const nodeRank = importantNodes?.ranks?.[node.id];

      // Check if node is in active paths
      const isInPath = activePaths?.paths.some(p => p.nodeIds.includes(node.id)) || false;
      const isInSelectedPath = activePaths?.selectedPathId
        ? activePaths.paths.find(p => p.pathId === activePaths.selectedPathId)?.nodeIds.includes(node.id)
        : false;

      // Check if node is in crisis highlight
      const degreeFromCrisis = crisisHighlight?.nodeIdToDegree.get(node.id);
      const isInCrisisView = degreeFromCrisis !== undefined;
      const isPolicyLever = crisisHighlight?.policyLeverIds.has(node.id) || false;

      const nodeEl = nodeGroup
        .append('g')
        .attr('class', `node ${isImportant ? 'important-node' : ''} ${isInPath ? 'in-path' : ''} ${isInCrisisView ? 'crisis-node' : ''} ${isPolicyLever ? 'policy-lever' : ''}`)
        .attr('transform', `translate(${pos.x}, ${pos.y})`)
        .datum(node) // Attach node data for selection updates
        .style('cursor', onNodeClick || onNodeSelect ? 'pointer' : 'default')
        .attr('role', 'button')
        .attr('tabindex', 0)
        .attr('aria-label', `${node.label}, ${node.connections.incoming} incoming and ${node.connections.outgoing} outgoing connections${isImportant && nodeRank ? `, rank ${nodeRank}` : ''}${isPolicyLever ? ', Policy lever' : ''}${isInCrisisView ? `, ${degreeFromCrisis} degrees from crisis` : ''}`);

      // Glow effect (initially hidden, or visible for important nodes)
      const glow = nodeEl
        .append('rect')
        .attr('class', 'node-glow')
        .attr('x', -pos.width / 2 - 8)
        .attr('y', -pos.height / 2 - 8)
        .attr('width', pos.width + 16)
        .attr('height', pos.height + 16)
        .attr('rx', 8)
        .attr('fill', isImportant ? '#FFD700' : HOVER_STYLE.glowColor) // Gold for important nodes
        .attr('opacity', isImportant ? 0.3 : 0) // Show glow for important nodes
        .attr('pointer-events', 'none'); // Don't intercept clicks - allow edges to be clickable

      // Add pulsing animation for important nodes
      if (isImportant) {
        glow
          .transition()
          .duration(2000)
          .attr('opacity', 0.6)
          .transition()
          .duration(2000)
          .attr('opacity', 0.3)
          .on('end', function repeat() {
            d3.select(this)
              .transition()
              .duration(2000)
              .attr('opacity', 0.6)
              .transition()
              .duration(2000)
              .attr('opacity', 0.3)
              .on('end', repeat);
          });
      }

      // Determine node styling
      let nodeStroke = NODE_STYLE.stroke;
      let nodeStrokeWidth = NODE_STYLE.strokeWidth;
      let nodeOpacity = 1;
      let nodeFill = NODE_STYLE.fill;

      // Crisis highlighting: color by degree from crisis
      if (isInCrisisView && degreeFromCrisis !== undefined) {
        // Color scale based on degree from crisis
        if (degreeFromCrisis === 0) {
          nodeFill = '#FEE2E2'; // Light red background for crisis nodes
          nodeStroke = '#EF4444'; // Red border
          nodeStrokeWidth = 2;
        } else if (degreeFromCrisis <= 2) {
          nodeFill = '#FFEDD5'; // Light orange background
          nodeStroke = '#F97316'; // Orange border
          nodeStrokeWidth = 1.5;
        } else if (degreeFromCrisis <= 4) {
          nodeFill = '#FEF3C7'; // Light yellow background
          nodeStroke = '#EAB308'; // Yellow border
          nodeStrokeWidth = 1.5;
        } else {
          nodeFill = '#DBEAFE'; // Light blue background
          nodeStroke = '#3B82F6'; // Blue border
          nodeStrokeWidth = 1.5;
        }

        // Override with gold stroke for policy levers
        if (isPolicyLever) {
          nodeStroke = '#FFD700'; // Gold stroke for policy levers
          nodeStrokeWidth = 3;
        }
      } else if (selectedNodeId === node.id) {
        nodeStroke = HOVER_STYLE.nodeStroke;
        nodeStrokeWidth = 2;
      } else if (isImportant) {
        nodeStroke = '#FFD700'; // Gold stroke for important nodes
        nodeStrokeWidth = 2;
      } else if (isInSelectedPath) {
        nodeStroke = '#3B82F6'; // Blue for selected path
        nodeStrokeWidth = 2.5;
      }

      // Dim nodes not in active path when path is selected
      if (activePaths?.selectedPathId && !isInSelectedPath) {
        nodeOpacity = 0.2;
      }

      // Node rectangle
      const rect = nodeEl
        .append('rect')
        .attr('x', -pos.width / 2)
        .attr('y', -pos.height / 2)
        .attr('width', pos.width)
        .attr('height', pos.height)
        .attr('rx', NODE_STYLE.rx)
        .attr('fill', nodeFill)
        .attr('stroke', nodeStroke)
        .attr('stroke-width', nodeStrokeWidth)
        .attr('opacity', nodeOpacity);

      // Add scale badge (always show if scale is available)
      if (node.scale) {
        // Scale badge colors
        const scaleColors: Record<number, string> = {
          1: '#9333EA', // Purple - Structural/Policy
          2: '#6B7280', // Gray - Built Environment (reserved)
          3: '#3B82F6', // Blue - Institutional
          4: '#10B981', // Green - Individual
          5: '#6B7280', // Gray - Behaviors (reserved)
          6: '#EAB308', // Yellow - Intermediate
          7: '#EF4444', // Red - Crisis
        };

        const scaleColor = scaleColors[node.scale] || '#6B7280';

        // Position scale badge in top-right corner
        nodeEl
          .append('circle')
          .attr('class', 'scale-badge')
          .attr('data-scale', node.scale)
          .attr('cx', pos.width / 2 - 8)
          .attr('cy', -pos.height / 2 + 8)
          .attr('r', 8)
          .attr('fill', scaleColor)
          .attr('stroke', '#fff')
          .attr('stroke-width', 1.5);

        nodeEl
          .append('text')
          .attr('class', 'scale-indicator')
          .attr('x', pos.width / 2 - 8)
          .attr('y', -pos.height / 2 + 8)
          .attr('text-anchor', 'middle')
          .attr('dominant-baseline', 'middle')
          .attr('font-size', '8px')
          .attr('font-weight', 'bold')
          .attr('fill', '#fff')
          .attr('pointer-events', 'none')
          .text(node.scale);
      }

      // Add rank badge for important nodes (bottom-right if scale badge exists)
      if (isImportant && nodeRank) {
        const badgeX = pos.width / 2 - 8;
        const badgeY = node.scale ? pos.height / 2 - 8 : -pos.height / 2 + 8; // Bottom-right if scale exists, else top-right

        nodeEl
          .append('circle')
          .attr('cx', badgeX)
          .attr('cy', badgeY)
          .attr('r', 10)
          .attr('fill', '#FFD700')
          .attr('stroke', '#FFA500')
          .attr('stroke-width', 1);

        nodeEl
          .append('text')
          .attr('x', badgeX)
          .attr('y', badgeY)
          .attr('text-anchor', 'middle')
          .attr('dominant-baseline', 'middle')
          .attr('font-size', '9px')
          .attr('font-weight', 'bold')
          .attr('fill', '#000')
          .attr('pointer-events', 'none')
          .text(nodeRank);
      }

      // Add expand/collapse indicator for hierarchical nodes with children
      const hierarchicalNode = node as unknown as HierarchicalMechanismNode;
      const hasChildren = enableHierarchy &&
        hierarchicalNode.childCount !== undefined &&
        hierarchicalNode.childCount > 0;

      if (hasChildren) {
        const isExpanded = expandedNodeIds?.has(node.id) ?? false;
        const indicatorX = -pos.width / 2 + 8;
        const indicatorY = pos.height / 2 - 8;

        // Expand/collapse button group
        const expandGroup = nodeEl
          .append('g')
          .attr('class', 'expand-indicator')
          .attr('transform', `translate(${indicatorX}, ${indicatorY})`)
          .style('cursor', 'pointer');

        // Background circle
        expandGroup
          .append('circle')
          .attr('r', HIERARCHY_INDICATOR_STYLE.size / 2)
          .attr('fill', HIERARCHY_INDICATOR_STYLE.fill)
          .attr('stroke', HIERARCHY_INDICATOR_STYLE.stroke)
          .attr('stroke-width', HIERARCHY_INDICATOR_STYLE.strokeWidth);

        // +/- icon
        expandGroup
          .append('text')
          .attr('text-anchor', 'middle')
          .attr('dominant-baseline', 'middle')
          .attr('font-size', `${HIERARCHY_INDICATOR_STYLE.fontSize}px`)
          .attr('font-weight', HIERARCHY_INDICATOR_STYLE.fontWeight)
          .attr('fill', '#333')
          .attr('pointer-events', 'none')
          .text(isExpanded ? HIERARCHY_INDICATOR_STYLE.expandedIcon : HIERARCHY_INDICATOR_STYLE.collapsedIcon);

        // Child count badge next to indicator
        expandGroup
          .append('text')
          .attr('x', HIERARCHY_INDICATOR_STYLE.size / 2 + 4)
          .attr('text-anchor', 'start')
          .attr('dominant-baseline', 'middle')
          .attr('font-size', '9px')
          .attr('fill', '#666')
          .attr('pointer-events', 'none')
          .text(`(${hierarchicalNode.childCount})`);

        // Click handler for expand/collapse
        expandGroup.on('click', (event: MouseEvent) => {
          event.stopPropagation(); // Don't trigger node click
          if (onNodeToggleExpand) {
            onNodeToggleExpand(node.id);
          }
        });

        // Hover effect
        expandGroup
          .on('mouseenter', function () {
            d3.select(this).select('circle')
              .attr('fill', '#e8e8e8')
              .attr('stroke', '#333');
          })
          .on('mouseleave', function () {
            d3.select(this).select('circle')
              .attr('fill', HIERARCHY_INDICATOR_STYLE.fill)
              .attr('stroke', HIERARCHY_INDICATOR_STYLE.stroke);
          });
      }

      // Text label (wrapped)
      const words = node.label.split(/[\s_]+/);
      const maxCharsPerLine = 18;
      let lines: string[] = [];
      let currentLine = '';

      words.forEach((word) => {
        if ((currentLine + ' ' + word).trim().length <= maxCharsPerLine) {
          currentLine = (currentLine + ' ' + word).trim();
        } else {
          if (currentLine) lines.push(currentLine);
          currentLine = word;
        }
      });
      if (currentLine) lines.push(currentLine);

      // Limit to 3 lines
      if (lines.length > 3) {
        lines = lines.slice(0, 2);
        lines.push('...');
      }

      const lineHeight = 13;
      const startY = -(lines.length - 1) * lineHeight / 2;

      const textGroup = nodeEl.append('g').attr('class', 'node-text').attr('opacity', nodeOpacity);

      lines.forEach((line, i) => {
        textGroup
          .append('text')
          .text(line)
          .attr('x', 0)
          .attr('y', startY + i * lineHeight)
          .attr('text-anchor', 'middle')
          .attr('dominant-baseline', 'middle')
          .attr('font-size', `${NODE_STYLE.fontSize}px`)
          .attr('font-weight', NODE_STYLE.fontWeight)
          .attr('font-family', NODE_STYLE.fontFamily)
          .attr('fill', '#333')
          .attr('pointer-events', 'none');
      });

      // Hover effects
      nodeEl
        .on('mouseenter', function () {
          glow.attr('opacity', HOVER_STYLE.glowOpacity);
          rect
            .attr('fill', HOVER_STYLE.nodeFill)
            .attr('stroke', HOVER_STYLE.nodeStroke)
            .attr('stroke-width', 2);
          textGroup.selectAll('text').attr('font-weight', HOVER_STYLE.nodeFontWeight);
        })
        .on('mouseleave', function () {
          glow.attr('opacity', 0);
          rect
            .attr('fill', NODE_STYLE.fill)
            .attr('stroke', selectedNodeId === node.id ? HOVER_STYLE.nodeStroke : NODE_STYLE.stroke)
            .attr('stroke-width', selectedNodeId === node.id ? 2 : NODE_STYLE.strokeWidth);
          textGroup.selectAll('text').attr('font-weight', NODE_STYLE.fontWeight);
        });

      // Click handler - supports both regular click and pathfinder selection
      const handleClick = () => {
        // Priority 1: Pathfinder selection mode
        if (selectionMode !== 'none' && onNodeSelect) {
          onNodeSelect(node.id, node.label);
        }
        // Priority 2: Regular node click
        else if (onNodeClick) {
          onNodeClick(node);
        }
      };

      nodeEl.on('click', handleClick);

      // Keyboard navigation
      nodeEl.on('keydown', (event) => {
        if (event.key === 'Enter' || event.key === ' ') {
          event.preventDefault();
          handleClick();
        }
      });

      // Add drag behavior for force-directed mode
      if (layoutMode === 'force-directed') {
        const drag = d3.drag<SVGGElement, MechanismNode>()
          .on('start', function(event, d) {
            // Fix: Don't restart simulation on drag start - prevents jumping
            // Only heat up simulation slightly if dragging actively
            if (event.active && simulationRef.current) {
              simulationRef.current.alphaTarget(0.1);
            }
            const nodeData = d as any;
            nodeData.fx = event.x;
            nodeData.fy = event.y;
          })
          .on('drag', function(event, d) {
            const nodeData = d as any;
            nodeData.fx = event.x;
            nodeData.fy = event.y;
            // Update position immediately
            const pos = nodePositions.get(d.id);
            if (pos) {
              pos.x = event.x;
              pos.y = event.y;
            }
            updateGraphPositions();
          })
          .on('end', function(event, d) {
            if (!event.active && simulationRef.current) {
              simulationRef.current.alphaTarget(0);
            }
            // Fix: Keep fixed position after drag to prevent drifting
            const nodeData = d as any;
            nodeData.fx = event.x;
            nodeData.fy = event.y;
          });

        nodeEl.call(drag);
      }
    });

    // Force-directed simulation setup
    if (layoutMode === 'force-directed') {
      // Stop any existing simulation
      if (simulationRef.current) {
        simulationRef.current.stop();
      }

      // Prepare node data with initial positions
      // Position structural determinants on left, crisis endpoints on right, others in middle
      const simNodes = connectedNodes.map((node) => {
        const pos = nodePositions.get(node.id);
        const level = getNodeLevel(node);
        const isStructural = level === 1; // Structural determinants (scale 1)
        const isCrisis = level === 7; // Crisis endpoints (scale 7)

        let initialX: number;
        if (isStructural) {
          // Position structural nodes on the left (10-20% of width)
          initialX = 0.15 * availableWidth;
        } else if (isCrisis) {
          // Position crisis nodes on the right (80-90% of width)
          initialX = 0.85 * availableWidth;
        } else {
          // Position other nodes in the middle with some randomness
          initialX = pos?.x || (0.3 + Math.random() * 0.4) * availableWidth;
        }

        return {
          ...node,
          x: initialX,
          y: pos?.y || Math.random() * availableHeight,
          level: level, // Store level for force calculations
        };
      });

      // Get physics settings with defaults
      const charge = physicsSettings?.charge || -300;
      const linkDistance = physicsSettings?.linkDistance || 150;
      const gravity = physicsSettings?.gravity || 0.05;
      const collision = physicsSettings?.collision || 20;

      // Create a copy of edges for simulation to avoid mutating original data
      // D3 force simulation mutates source/target from strings to object references
      const simEdges = data.edges.map(edge => ({
        source: edge.source,
        target: edge.target,
        id: edge.id
      }));

      // Create force simulation with horizontal positioning constraints
      const simulation = d3.forceSimulation(simNodes as any)
        .force('charge', d3.forceManyBody().strength(charge))
        .force('collision', d3.forceCollide().radius(NODE_STYLE.width / 2 + collision))
        .force('link', d3.forceLink(simEdges)
          .id((d: any) => d.id)
          .distance(linkDistance)
          .strength(0.5)
        )
        // Strong X-axis positioning for structural and crisis nodes
        .force('x', d3.forceX((d: any) => {
          if (d.level === 1) {
            // Pin structural determinants to the left
            return 0.15 * availableWidth;
          } else if (d.level === 7) {
            // Pin crisis endpoints to the right
            return 0.85 * availableWidth;
          } else {
            // Allow other nodes to float in the middle
            return availableWidth / 2;
          }
        }).strength((d: any) => {
          // Strong force for structural and crisis, weak for others
          return (d.level === 1 || d.level === 7) ? 0.8 : gravity;
        }))
        // Y-axis centering (weaker to allow vertical spreading)
        .force('y', d3.forceY(availableHeight / 2).strength(gravity * 0.5))
        .alphaDecay(0.05) // Faster settling (increased from 0.02)
        .velocityDecay(0.6) // More friction - nodes slow down faster (default is 0.4)
        .alphaMin(0.001) // Stop sooner once mostly stable (default is 0.001)
        .on('tick', () => {
          // Update node positions on each tick
          simNodes.forEach((node: any) => {
            const pos = nodePositions.get(node.id);
            if (pos) {
              pos.x = node.x;
              pos.y = node.y;
            }
          });

          // Re-render graph with updated positions
          updateGraphPositions();
        });

      // Let simulation settle for a bit before user interaction
      // Run simulation for initial layout, then slow it down
      simulation.alpha(1).restart();

      simulationRef.current = simulation;
    }

    // Optional legend (minimal, at bottom)
    if (showLegend) {
      const legend = svg
        .append('g')
        .attr('class', 'legend')
        .attr('transform', `translate(${width / 2}, ${height - 20})`);

      // Crisis view legend
      if (crisisHighlight) {
        const legendItems = [
          { label: 'Crisis (0)', color: '#EF4444' },
          { label: 'Immediate (1-2)', color: '#F97316' },
          { label: 'Intermediate (3-4)', color: '#EAB308' },
          { label: 'Structural (5+)', color: '#3B82F6' },
          { label: 'Policy Lever', color: '#FFD700', isStroke: true },
        ];

        const legendGroup = legend
          .append('g')
          .attr('transform', 'translate(-250, -10)');

        legendItems.forEach((item, i) => {
          const itemGroup = legendGroup
            .append('g')
            .attr('transform', `translate(${i * 110}, 0)`);

          if (item.isStroke) {
            // Show as border/stroke indicator
            itemGroup
              .append('rect')
              .attr('x', 0)
              .attr('y', 0)
              .attr('width', 16)
              .attr('height', 16)
              .attr('fill', 'white')
              .attr('stroke', item.color)
              .attr('stroke-width', 3)
              .attr('rx', 2);
          } else {
            // Show as filled color
            itemGroup
              .append('rect')
              .attr('x', 0)
              .attr('y', 0)
              .attr('width', 16)
              .attr('height', 16)
              .attr('fill', item.color)
              .attr('stroke', item.color)
              .attr('stroke-width', 1.5)
              .attr('rx', 2);
          }

          itemGroup
            .append('text')
            .attr('x', 20)
            .attr('y', 12)
            .attr('font-size', '10px')
            .attr('font-family', NODE_STYLE.fontFamily)
            .attr('fill', '#333')
            .text(item.label);
        });
      } else {
        // Default legend
        legend
          .append('text')
          .text(`Showing ${connectedNodes.length} nodes with active mechanisms`)
          .attr('text-anchor', 'middle')
          .attr('font-size', '10px')
          .attr('font-family', NODE_STYLE.fontFamily)
          .attr('fill', '#666');
      }
    }

    // Cleanup function
    return () => {
      if (simulationRef.current) {
        simulationRef.current.stop();
        simulationRef.current = null;
      }
    };
  }, [
    // Only redraw when these STRUCTURAL changes occur:
    data,              // Graph data changed
    width,             // Canvas size changed
    height,
    layoutMode,        // Layout type changed (hierarchical vs force-directed)
    physicsSettings,   // Physics parameters changed
    showLegend,        // Legend visibility (rarely changes, OK to redraw)
    // REMOVED from dependencies to prevent constant redraws:
    // - onNodeClick, onEdgeClick (handlers don't need redraw)
    // - importantNodes, activePaths, crisisHighlight (visual overlays, set once)
    // - selectionMode, onNodeSelect (interaction state)
    // These features render correctly on initial draw but won't update dynamically.
    // For dynamic updates, would need separate effect or use React state instead of D3.
  ]);

  // Zoom effect: Handle zoom requests from graph state store
  useEffect(() => {
    if (!svgRef.current || !zoomBehaviorRef.current) return;

    const svg = d3.select(svgRef.current);
    const zoom = zoomBehaviorRef.current;

    // Handle zoom to specific node
    if (zoomToNodeId) {
      const nodePos = nodePositionsRef.current.get(zoomToNodeId);
      if (nodePos) {
        // Calculate transform to center on node
        const scale = 1.5; // Zoom in slightly
        const translateX = width / 2 - nodePos.x * scale;
        const translateY = height / 2 - nodePos.y * scale;

        svg.transition()
          .duration(750)
          .call(
            zoom.transform as any,
            d3.zoomIdentity.translate(translateX, translateY).scale(scale)
          );
      }
      clearZoomRequest();
    }

    // Handle zoom to fit paths
    if (zoomToPaths && activePaths && activePaths.paths.length > 0) {
      // Find bounding box of all nodes in active paths
      const allNodeIds = new Set<string>();
      activePaths.paths.forEach(path => {
        path.nodeIds.forEach(nodeId => allNodeIds.add(nodeId));
      });

      let minX = Infinity, maxX = -Infinity;
      let minY = Infinity, maxY = -Infinity;

      allNodeIds.forEach(nodeId => {
        const pos = nodePositionsRef.current.get(nodeId);
        if (pos) {
          minX = Math.min(minX, pos.x - pos.width / 2);
          maxX = Math.max(maxX, pos.x + pos.width / 2);
          minY = Math.min(minY, pos.y - pos.height / 2);
          maxY = Math.max(maxY, pos.y + pos.height / 2);
        }
      });

      if (minX !== Infinity && maxX !== -Infinity) {
        // Add padding
        const padding = 100;
        const boundsWidth = maxX - minX + padding * 2;
        const boundsHeight = maxY - minY + padding * 2;
        const centerX = (minX + maxX) / 2;
        const centerY = (minY + maxY) / 2;

        // Calculate scale to fit
        const scale = Math.min(
          width / boundsWidth,
          height / boundsHeight,
          2 // Max zoom
        );

        const translateX = width / 2 - centerX * scale;
        const translateY = height / 2 - centerY * scale;

        svg.transition()
          .duration(750)
          .call(
            zoom.transform as any,
            d3.zoomIdentity.translate(translateX, translateY).scale(scale)
          );
      }
      clearZoomToPathsRequest();
    }
  }, [zoomToNodeId, zoomToPaths, activePaths, width, height, clearZoomRequest, clearZoomToPathsRequest]);

  // Selection effect: Update node styling when selection changes (without redrawing)
  useEffect(() => {
    if (!svgRef.current) return;

    const svg = d3.select(svgRef.current);

    // Update all node rectangles' stroke based on selection
    svg.selectAll<SVGRectElement, unknown>('g.node rect')
      .filter(function() {
        // Filter to only the main node rect (not glow)
        return !d3.select(this).classed('node-glow');
      })
      .attr('stroke', function(this: SVGRectElement) {
        const nodeGroup = d3.select(this.parentNode as SVGGElement);
        const nodeData = nodeGroup.datum() as MechanismNode | undefined;
        return nodeData && selectedNodeId === nodeData.id ? HOVER_STYLE.nodeStroke : NODE_STYLE.stroke;
      })
      .attr('stroke-width', function(this: SVGRectElement) {
        const nodeGroup = d3.select(this.parentNode as SVGGElement);
        const nodeData = nodeGroup.datum() as MechanismNode | undefined;
        return nodeData && selectedNodeId === nodeData.id ? 2 : NODE_STYLE.strokeWidth;
      });
  }, [selectedNodeId]);

  // Edge selection effect: Update edge styling when selection changes (without redrawing)
  useEffect(() => {
    if (!svgRef.current) return;

    const svg = d3.select(svgRef.current);

    // Reset all edge strokes to default
    svg.selectAll<SVGPathElement, unknown>('g.link path')
      .filter(function() {
        // Only update visible paths, not transparent hitboxes
        return d3.select(this).attr('stroke') !== 'transparent';
      })
      .each(function() {
        const path = d3.select(this);
        const linkGroup = d3.select(this.parentNode as SVGGElement);
        const edgeData = linkGroup.datum() as MechanismEdge | undefined;

        if (edgeData && selectedEdgeId === edgeData.id) {
          // Highlight selected edge with prominent styling and glow effect
          path
            .attr('stroke', '#2563EB') // Darker blue (blue-600) for better visibility
            .attr('stroke-width', 5)
            .attr('opacity', 1)
            .style('filter', 'drop-shadow(0 0 4px rgba(37, 99, 235, 0.6))'); // Glow effect
        } else {
          // Reset to default based on direction
          const isNegative = edgeData?.direction === 'negative';
          path
            .attr('stroke', isNegative ? '#EF4444' : EDGE_STYLE.stroke)
            .attr('stroke-width', EDGE_STYLE.strokeWidth)
            .style('filter', 'none'); // Remove any glow
        }
      });
  }, [selectedEdgeId]);

  return (
    <svg
      ref={svgRef}
      className="border border-gray-300 rounded-lg bg-white"
      style={{ width: '100%', height: '100%' }}
    />
  );
};

export default MechanismGraph;
