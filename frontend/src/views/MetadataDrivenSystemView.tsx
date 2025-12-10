/**
 * MetadataDrivenSystemView - Generalized domain-specific system exploration
 *
 * Supports:
 * - Domain filtering via keywords
 * - Node detail panel with connection information
 * - Category/scale filtering
 * - Hierarchical and force-directed layouts
 *
 * Uses details panel pattern like SystemsMapView (not focal node filtering).
 */

import React, { useState, useMemo } from 'react';
import MechanismGraph from '../visualizations/MechanismGraph';
import { Badge } from '../components/base/Badge';
import { Icon } from '../components/base/Icon';
import { Panel } from '../layouts/Panel';
import { Button } from '../components/base/Button';
import { CategoryBadge } from '../components/domain/CategoryBadge';
import { EvidenceBadge } from '../components/domain/EvidenceBadge';
import { useMechanismsForGraph, useMechanismById, useNodes } from '../hooks/useData';
import { buildGraphFromCanonicalNodes, filterByMinConnections } from '../utils/graphBuilder';
import { EvidenceModal } from '../components/domain/EvidenceModal';
import type { Category, NodeScale, MechanismNode, MechanismEdge, GraphLayoutMode } from '../types/mechanism';

export interface MetadataDrivenSystemViewProps {
  /** Keywords to filter domain-specific mechanisms (e.g., ['alcohol', 'ald', 'liver']) */
  domainKeywords: string[];

  /** Initial category filters */
  initialCategories?: Category[];

  /** Initial scale filters */
  initialScales?: NodeScale[];

  /** View title */
  title: string;

  /** View description */
  description?: string;

  /** Minimum number of connections required to display a node (default: 2) */
  minConnections?: number;
}

export const MetadataDrivenSystemView: React.FC<MetadataDrivenSystemViewProps> = ({
  domainKeywords,
  initialCategories,
  initialScales,
  title,
  description,
  minConnections = 2
}) => {
  // Fetch all mechanisms and canonical nodes
  const { data: allMechanisms, isLoading: mechanismsLoading, error: mechanismsError } = useMechanismsForGraph();
  const { data: canonicalNodes, isLoading: nodesLoading, error: nodesError } = useNodes({ referenced_only: true });

  // Combine loading/error states
  const isLoading = mechanismsLoading || nodesLoading;
  const error = mechanismsError || nodesError;

  // State for node/edge selection and details panel
  const [selectedNode, setSelectedNode] = useState<MechanismNode | null>(null);
  const [selectedEdge, setSelectedEdge] = useState<MechanismEdge | null>(null);
  const [showPanel, setShowPanel] = useState(false);
  const [previousNode, setPreviousNode] = useState<MechanismNode | null>(null);
  const [mechanismEntrySource, setMechanismEntrySource] = useState<'graph' | 'node-panel' | null>(null);
  const [filterCategories, setFilterCategories] = useState<Category[]>(initialCategories || []);
  const [filterScales, setFilterScales] = useState<NodeScale[]>(initialScales || []);
  const [showFilterPanel, setShowFilterPanel] = useState(false);

  // Layout state
  const [layoutMode, setLayoutMode] = useState<GraphLayoutMode>('hierarchical');

  // Filter mechanisms by domain keywords
  const domainMechanisms = useMemo(() => {
    if (!allMechanisms) return [];

    const keywordLower = domainKeywords.map(k => k.toLowerCase());
    return allMechanisms.filter(mech => {
      const searchText = [
        mech.id,
        mech.name,
        mech.from_node_name,
        mech.to_node_name,
        mech.description || ''
      ].join(' ').toLowerCase();

      return keywordLower.some(keyword => searchText.includes(keyword));
    });
  }, [allMechanisms, domainKeywords]);

  // Build base domain graph (without user filters) using canonical nodes
  const baseDomainGraph = useMemo(() => {
    if (!canonicalNodes || !domainMechanisms.length) return { nodes: [], edges: [] };

    let result = buildGraphFromCanonicalNodes(canonicalNodes, domainMechanisms, {
      includeDisconnected: false
    });

    // Apply minimum connections filter
    if (minConnections > 1) {
      result = filterByMinConnections(result, minConnections);
    }

    return result;
  }, [canonicalNodes, domainMechanisms, minConnections]);

  // Build filtered domain-specific subgraph using canonical nodes
  const displayGraph = useMemo(() => {
    if (!canonicalNodes || !domainMechanisms.length) return { nodes: [], edges: [] };

    console.log(`[${title}] Building domain subgraph with canonical nodes:`, {
      totalMechanisms: domainMechanisms.length,
      canonicalNodes: canonicalNodes.length,
      keywords: domainKeywords,
      filterCategories: filterCategories.length > 0 ? filterCategories : 'all',
      filterScales: filterScales.length > 0 ? filterScales : 'all',
      minConnections
    });

    let result = buildGraphFromCanonicalNodes(canonicalNodes, domainMechanisms, {
      filterCategories: filterCategories.length > 0 ? filterCategories : undefined,
      filterScales: filterScales.length > 0 ? filterScales : undefined,
      includeDisconnected: false
    });

    // Apply minimum connections filter
    if (minConnections > 1) {
      result = filterByMinConnections(result, minConnections);
    }

    console.log(`[${title}] Domain subgraph result:`, {
      nodes: result.nodes.length,
      edges: result.edges.length
    });

    return result;
  }, [canonicalNodes, domainMechanisms, domainKeywords, filterCategories, filterScales, title, minConnections]);

  // Handle node click - show node details panel
  const handleNodeClick = (node: MechanismNode) => {
    setSelectedNode(node);
    setSelectedEdge(null);
    setShowPanel(true);
  };

  // Handle edge click - show mechanism details panel
  const handleEdgeClick = (edge: MechanismEdge) => {
    setSelectedEdge(edge);
    setSelectedNode(null);
    setPreviousNode(null);
    setMechanismEntrySource('graph');
    setShowPanel(true);
  };

  // Navigate from node panel to mechanism panel
  const handleMechanismFromNodePanel = (edge: MechanismEdge, originNode: MechanismNode) => {
    setSelectedEdge(edge);
    setPreviousNode(originNode);
    setMechanismEntrySource('node-panel');
    setSelectedNode(null);
  };

  // Back to originating node
  const handleBackToNode = () => {
    if (previousNode) {
      setSelectedNode(previousNode);
      setSelectedEdge(null);
      setPreviousNode(null);
      setMechanismEntrySource(null);
    }
  };

  // Navigate to a different node from mechanism panel
  const handleNavigateToNode = (nodeId: string) => {
    const targetNode = displayGraph?.nodes.find(n => n.id === nodeId);
    if (targetNode) {
      setSelectedNode(targetNode);
      setSelectedEdge(null);
      setPreviousNode(null);
      setMechanismEntrySource(null);
    }
  };

  // Handle close panel
  const handleClosePanel = () => {
    setShowPanel(false);
    setSelectedNode(null);
    setSelectedEdge(null);
    setPreviousNode(null);
    setMechanismEntrySource(null);
  };

  // Handle clear filters
  const handleClearFilters = () => {
    setFilterCategories(initialCategories || []);
    setFilterScales(initialScales || []);
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="text-center">
          <p className="text-gray-500 text-lg">Loading system data...</p>
          <p className="text-gray-400 text-sm mt-2">Fetching mechanisms from API...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="text-center max-w-lg">
          <p className="text-red-500 text-lg font-semibold mb-2">Error loading data</p>
          <p className="text-gray-600 mb-4">{error.message}</p>
          <div className="bg-gray-100 rounded p-4 text-left text-sm">
            <p className="font-semibold mb-2">Troubleshooting:</p>
            <ul className="list-disc list-inside space-y-1 text-gray-700">
              <li>Check if backend server is running (port 8002)</li>
              <li>Verify API_URL environment variable</li>
              <li>Check browser console for CORS errors</li>
            </ul>
          </div>
        </div>
      </div>
    );
  }

  // Check if no data was loaded
  if (!allMechanisms || allMechanisms.length === 0) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="text-center">
          <p className="text-gray-500 text-lg">No mechanisms loaded from API</p>
          <p className="text-gray-400 text-sm mt-2">Backend may be empty or unreachable</p>
        </div>
      </div>
    );
  }

  // Check if base domain filtering resulted in empty graph (no domain-relevant data at all)
  if (baseDomainGraph.nodes.length === 0) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="text-center max-w-lg">
          <p className="text-gray-500 text-lg font-semibold mb-2">No matching nodes found</p>
          <p className="text-gray-600 mb-4">
            No mechanisms or nodes match the domain keywords for "{title}"
          </p>
          <div className="bg-gray-100 rounded p-4 text-left text-sm">
            <p className="font-semibold mb-2">Keywords being searched:</p>
            <div className="flex flex-wrap gap-2">
              {domainKeywords.map(kw => (
                <span key={kw} className="bg-blue-100 text-blue-800 px-2 py-1 rounded text-xs">
                  {kw}
                </span>
              ))}
            </div>
            <p className="mt-3 text-gray-600">
              Loaded {allMechanisms?.length || 0} total mechanisms from API.
            </p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="flex h-full">
      {/* Main content area */}
      <div className="flex flex-col flex-1">
        {/* Header */}
        <div className="border-b border-gray-200 bg-white px-6 py-4">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-semibold text-gray-900">{title}</h1>
              {description && (
                <p className="mt-1 text-sm text-gray-500">{description}</p>
              )}
            </div>

            <div className="flex items-center gap-2">
              {/* Layout toggle */}
              <div className="flex gap-1 bg-gray-100 rounded-lg p-1">
                <button
                  onClick={() => setLayoutMode('hierarchical')}
                  className={`px-3 py-1 text-sm rounded ${
                    layoutMode === 'hierarchical'
                      ? 'bg-white text-gray-900 shadow-sm'
                      : 'text-gray-600 hover:text-gray-900'
                  }`}
                >
                  Hierarchical
                </button>
                <button
                  onClick={() => setLayoutMode('force-directed')}
                  className={`px-3 py-1 text-sm rounded ${
                    layoutMode === 'force-directed'
                      ? 'bg-white text-gray-900 shadow-sm'
                      : 'text-gray-600 hover:text-gray-900'
                  }`}
                >
                  Force-Directed
                </button>
              </div>

              {/* Filter panel toggle */}
              <button
                onClick={() => setShowFilterPanel(!showFilterPanel)}
                className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50"
              >
                {showFilterPanel ? 'Hide Filters' : 'Show Filters'}
              </button>
            </div>
          </div>
        </div>

      {/* Main content */}
      <div className="flex flex-1 overflow-hidden">
        {/* Filter panel */}
        {showFilterPanel && (
          <FilterPanel
            filterCategories={filterCategories}
            onFilterCategoriesChange={setFilterCategories}
            filterScales={filterScales}
            onFilterScalesChange={setFilterScales}
            onClearFilters={handleClearFilters}
          />
        )}

        {/* Graph visualization */}
        <div className="flex-1 relative">
          {displayGraph.nodes.length === 0 ? (
            <div className="absolute inset-0 flex items-center justify-center bg-gray-50">
              <div className="text-center max-w-md p-6">
                <svg
                  className="w-16 h-16 mx-auto text-gray-300 mb-4"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z"
                  />
                </svg>
                <p className="text-gray-600 text-lg font-medium mb-2">No nodes match current filters</p>
                <p className="text-gray-500 text-sm mb-4">
                  {filterCategories.length === 0 && filterScales.length === 0
                    ? "Please select at least one category or scale to view nodes."
                    : "Try adjusting your category or scale filters to see more nodes."}
                </p>
                <button
                  onClick={handleClearFilters}
                  className="px-4 py-2 text-sm font-medium text-white bg-orange-600 rounded-lg hover:bg-orange-700"
                >
                  Reset to Default Filters
                </button>
              </div>
            </div>
          ) : (
            <MechanismGraph
              data={displayGraph}
              selectedNodeId={selectedNode?.id || null}
              selectedEdgeId={selectedEdge?.id || null}
              onNodeClick={handleNodeClick}
              onEdgeClick={handleEdgeClick}
              layoutMode={layoutMode}
            />
          )}
        </div>
      </div>

        {/* Stats footer */}
        <div className="border-t border-gray-200 bg-gray-50 px-6 py-3">
          <div className="flex items-center gap-6 text-sm text-gray-600">
            <span>{displayGraph.nodes.length} nodes</span>
            <span>{displayGraph.edges.length} mechanisms</span>
          </div>
        </div>
      </div>

      {/* Node Detail Panel */}
      {showPanel && selectedNode && (
        <Panel
          title={selectedNode.label}
          icon={<Icon name="arrow-right" size="md" className="text-primary-600" />}
          onClose={handleClosePanel}
          resizable
          collapsible
        >
          <NodeDetailPanel
            node={selectedNode}
            edges={displayGraph.edges}
            nodes={displayGraph.nodes}
            onMechanismClick={(edge) => handleMechanismFromNodePanel(edge, selectedNode)}
          />
        </Panel>
      )}

      {/* Mechanism Detail Panel */}
      {showPanel && selectedEdge && (
        <Panel
          title="Mechanism Detail"
          icon={<Icon name="arrow-right" size="md" className="text-primary-600" />}
          onClose={handleClosePanel}
          onBack={mechanismEntrySource === 'node-panel' ? handleBackToNode : undefined}
          resizable
          collapsible
        >
          <MechanismDetailPanel
            edge={selectedEdge}
            nodes={displayGraph.nodes}
            onNodeClick={handleNavigateToNode}
          />
        </Panel>
      )}
    </div>
  );
};

// ============================================
// FilterPanel Component
// ============================================

interface FilterPanelProps {
  filterCategories: Category[];
  onFilterCategoriesChange: (categories: Category[]) => void;
  filterScales: NodeScale[];
  onFilterScalesChange: (scales: NodeScale[]) => void;
  onClearFilters: () => void;
}

const FilterPanel: React.FC<FilterPanelProps> = ({
  filterCategories,
  onFilterCategoriesChange,
  filterScales,
  onFilterScalesChange,
  onClearFilters,
}) => {
  const allCategories: Category[] = [
    'political',
    'built_environment',
    'economic',
    'social_environment',
    'behavioral',
    'healthcare_access',
    'biological',
  ];

  const allScales: NodeScale[] = [1, 2, 3, 4, 5, 6, 7];

  const scaleLabels: Record<NodeScale, string> = {
    1: 'Structural Determinants',
    2: 'Built Environment',
    3: 'Institutional Infrastructure',
    4: 'Household Conditions',
    5: 'Behaviors & Psychosocial',
    6: 'Intermediate Pathways',
    7: 'Crisis Endpoints'
  };

  const toggleCategory = (category: Category) => {
    if (filterCategories.includes(category)) {
      onFilterCategoriesChange(filterCategories.filter(c => c !== category));
    } else {
      onFilterCategoriesChange([...filterCategories, category]);
    }
  };

  const toggleScale = (scale: NodeScale) => {
    if (filterScales.includes(scale)) {
      onFilterScalesChange(filterScales.filter(s => s !== scale));
    } else {
      onFilterScalesChange([...filterScales, scale]);
    }
  };

  return (
    <div className="w-80 border-r border-gray-200 bg-white overflow-y-auto">
      <div className="p-4 space-y-6">
        {/* Category Filters */}
        <div>
          <h3 className="text-sm font-semibold text-gray-900 mb-2">Categories</h3>
          <div className="space-y-1">
            {allCategories.map(category => (
              <label key={category} className="flex items-center gap-2 cursor-pointer">
                <input
                  type="checkbox"
                  checked={filterCategories.includes(category)}
                  onChange={() => toggleCategory(category)}
                  className="rounded text-orange-600 focus:ring-orange-500"
                />
                <span className="text-sm text-gray-700 capitalize">
                  {category.replace(/_/g, ' ')}
                </span>
              </label>
            ))}
          </div>
          {filterCategories.length > 0 && (
            <button
              onClick={() => onFilterCategoriesChange([])}
              className="mt-2 text-xs text-orange-600 hover:text-orange-700"
            >
              Clear all
            </button>
          )}
        </div>

        {/* Scale Filters */}
        <div>
          <h3 className="text-sm font-semibold text-gray-900 mb-2">Scales</h3>
          <div className="space-y-1">
            {allScales.map(scale => (
              <label key={scale} className="flex items-center gap-2 cursor-pointer">
                <input
                  type="checkbox"
                  checked={filterScales.includes(scale)}
                  onChange={() => toggleScale(scale)}
                  className="rounded text-orange-600 focus:ring-orange-500"
                />
                <span className="text-sm text-gray-700">
                  Scale {scale}: {scaleLabels[scale]}
                </span>
              </label>
            ))}
          </div>
          {filterScales.length > 0 && (
            <button
              onClick={() => onFilterScalesChange([])}
              className="mt-2 text-xs text-orange-600 hover:text-orange-700"
            >
              Clear all
            </button>
          )}
        </div>

        {/* Clear All Filters */}
        <div className="pt-4 border-t border-gray-200">
          <button
            onClick={onClearFilters}
            className="w-full px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50"
          >
            Clear All Filters
          </button>
        </div>
      </div>
    </div>
  );
};

// ============================================
// NodeDetailPanel Component
// ============================================

const NodeDetailPanel: React.FC<{
  node: MechanismNode
  edges: MechanismEdge[]
  nodes: MechanismNode[]
  onMechanismClick?: (edge: MechanismEdge) => void
}> = ({ node, edges, nodes, onMechanismClick }) => {
  const outgoingEdges = edges.filter((e) => {
    const source = typeof e.source === 'string' ? e.source : (e.source as any).id;
    return source === node.id;
  });
  const incomingEdges = edges.filter((e) => {
    const target = typeof e.target === 'string' ? e.target : (e.target as any).id;
    return target === node.id;
  });

  const getNodeLabel = (nodeId: string): string => {
    return nodes.find((n) => n.id === nodeId)?.label || nodeId;
  };

  return (
    <div className="space-y-6">
      {/* Quick Stats */}
      <div className="flex items-center gap-3 pb-4 border-b flex-wrap">
        {node.category && <CategoryBadge category={node.category} />}
        {node.scale && (
          <Badge color="gray" size="sm">
            Scale {node.scale}
          </Badge>
        )}
      </div>

      {/* Overview */}
      <div>
        <h3 className="text-sm font-semibold text-gray-900 mb-2">Overview</h3>
        <div className="space-y-2 text-sm text-gray-700">
          {node.scale && (
            <p>
              <span className="font-medium">Scale:</span> {node.scale}
            </p>
          )}
          <p>
            <span className="font-medium">Connections:</span> {outgoingEdges.length} outgoing, {incomingEdges.length} incoming
          </p>
        </div>
      </div>

      {/* Connections */}
      <div>
        <h3 className="text-sm font-semibold text-gray-900 mb-3">Connections</h3>

        <div className="space-y-3">
          <div>
            <p className="text-xs font-medium text-gray-600 mb-2">
              Outgoing ({outgoingEdges.length})
            </p>
            <div className="space-y-2 max-h-48 overflow-y-auto">
              {outgoingEdges.slice(0, 5).map((edge) => (
                <div
                  key={edge.id}
                  className="flex items-start gap-2 p-2 rounded border border-gray-200 hover:border-primary-300 hover:bg-gray-50 transition-colors cursor-pointer"
                  onClick={() => onMechanismClick?.(edge)}
                  role="button"
                  tabIndex={0}
                  onKeyDown={(e) => {
                    if (e.key === 'Enter' || e.key === ' ') {
                      e.preventDefault();
                      onMechanismClick?.(edge);
                    }
                  }}
                >
                  <Icon name="arrow-right" size="sm" className="text-green-600 mt-0.5 flex-shrink-0" />
                  <div className="flex-1 min-w-0">
                    <p className="text-xs font-medium text-gray-900 truncate" title={`${node.label} → ${getNodeLabel(edge.target as string)}`}>
                      {node.label} → {getNodeLabel(edge.target as string)}
                    </p>
                    <p className="text-xs text-gray-500">
                      {edge.direction === 'positive' ? 'Positive' : 'Negative'} relationship
                    </p>
                  </div>
                  {edge.evidenceQuality && (
                    <EvidenceBadge quality={edge.evidenceQuality} size="sm" />
                  )}
                </div>
              ))}
              {outgoingEdges.length > 5 && (
                <button className="text-xs text-primary-600 hover:text-primary-700 font-medium">
                  Show all {outgoingEdges.length} connections →
                </button>
              )}
            </div>
          </div>

          <div>
            <p className="text-xs font-medium text-gray-600 mb-2">
              Incoming ({incomingEdges.length})
            </p>
            <div className="space-y-2 max-h-48 overflow-y-auto">
              {incomingEdges.slice(0, 5).map((edge) => (
                <div
                  key={edge.id}
                  className="flex items-start gap-2 p-2 rounded border border-gray-200 hover:border-primary-300 hover:bg-gray-50 transition-colors cursor-pointer"
                  onClick={() => onMechanismClick?.(edge)}
                  role="button"
                  tabIndex={0}
                  onKeyDown={(e) => {
                    if (e.key === 'Enter' || e.key === ' ') {
                      e.preventDefault();
                      onMechanismClick?.(edge);
                    }
                  }}
                >
                  <Icon name="arrow-left" size="sm" className="text-blue-600 mt-0.5 flex-shrink-0" />
                  <div className="flex-1 min-w-0">
                    <p className="text-xs font-medium text-gray-900 truncate" title={`${getNodeLabel(edge.source as string)} → ${node.label}`}>
                      {getNodeLabel(edge.source as string)} → {node.label}
                    </p>
                    <p className="text-xs text-gray-500">
                      {edge.direction === 'positive' ? 'Positive' : 'Negative'} relationship
                    </p>
                  </div>
                  {edge.evidenceQuality && (
                    <EvidenceBadge quality={edge.evidenceQuality} size="sm" />
                  )}
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

// ============================================
// MechanismDetailPanel Component
// ============================================

const MechanismDetailPanel: React.FC<{
  edge: MechanismEdge
  nodes: MechanismNode[]
  onNodeClick?: (nodeId: string) => void
}> = ({ edge, nodes, onNodeClick }) => {
  const [showEvidenceModal, setShowEvidenceModal] = useState(false);

  // Fetch detailed mechanism data from API
  const { data: mechanism, isLoading } = useMechanismById(edge.id);
  const sourceNode = nodes.find((n) => n.id === edge.source);
  const targetNode = nodes.find((n) => n.id === edge.target);

  if (isLoading) {
    return (
      <div className="flex items-center justify-center py-8">
        <Icon name="refresh" size="md" className="animate-spin text-primary-600" />
      </div>
    );
  }

  if (!mechanism) {
    return (
      <div className="text-center py-8 text-gray-600">
        <p>Unable to load mechanism details.</p>
      </div>
    );
  }

  return (
    <>
      <div className="space-y-6">
        {/* Quick Stats */}
        <div className="flex items-center gap-3 pb-4 border-b">
          <Badge color={edge.direction === 'positive' ? 'success' : 'error'} size="sm">
            {edge.direction === 'positive' ? 'Positive (+)' : 'Negative (−)'}
          </Badge>
          {edge.evidenceQuality && (
            <EvidenceBadge quality={edge.evidenceQuality} size="md" showLabel />
          )}
          <Badge color="gray" size="sm">
            {mechanism.n_studies || edge.studyCount} studies
          </Badge>
        </div>

        {/* Nodes */}
        <div className="text-sm">
          <p className="text-gray-600 mb-2">From → To</p>
          <div className="flex items-center gap-2 flex-wrap">
            <button
              onClick={() => sourceNode && onNodeClick?.(sourceNode.id)}
              className="px-3 py-1.5 bg-gray-100 hover:bg-primary-100 hover:text-primary-700 rounded-md text-sm font-medium text-gray-900 transition-colors"
              title={`View details for ${sourceNode?.label}`}
            >
              {sourceNode?.label}
            </button>
            <Icon name="arrow-right" size="sm" className="text-gray-400" />
            <button
              onClick={() => targetNode && onNodeClick?.(targetNode.id)}
              className="px-3 py-1.5 bg-gray-100 hover:bg-primary-100 hover:text-primary-700 rounded-md text-sm font-medium text-gray-900 transition-colors"
              title={`View details for ${targetNode?.label}`}
            >
              {targetNode?.label}
            </button>
          </div>
        </div>

        {/* Description */}
        <div>
          <h3 className="text-sm font-semibold text-gray-900 mb-2">Mechanism</h3>
          <p className="text-sm text-gray-700 leading-relaxed">{mechanism.description}</p>
        </div>

        {/* View Full Evidence Button */}
        <div>
          <Button
            variant="primary"
            size="md"
            onClick={() => setShowEvidenceModal(true)}
            className="w-full justify-center"
          >
            <Icon name="book-open" size="md" />
            <span className="ml-2">View Full Evidence & Citations</span>
          </Button>
        </div>

        {/* Citations Preview */}
        {mechanism.citations && mechanism.citations.length > 0 && (
          <div>
            <h3 className="text-sm font-semibold text-gray-900 mb-3">
              Primary Citation
            </h3>
            <div className="p-3 border-2 border-gray-200 rounded-lg text-xs space-y-2 bg-gray-50">
              <p className="font-semibold text-gray-900">
                {mechanism.citations[0].authors} ({mechanism.citations[0].year})
              </p>
              <p className="text-sm text-gray-900 font-medium leading-snug">{mechanism.citations[0].title}</p>
              <p className="text-gray-600 italic">{mechanism.citations[0].journal}</p>
              {mechanism.citations[0].url && (
                <a
                  href={mechanism.citations[0].url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-primary-600 hover:text-primary-700 inline-flex items-center gap-1 font-medium text-sm"
                >
                  View Citation
                  <Icon name="external-link" size="xs" />
                </a>
              )}
            </div>
            {mechanism.citations.length > 1 && (
              <p className="text-xs text-gray-500 mt-2">
                + {mechanism.citations.length - 1} supporting citations (click "View Full Evidence" above)
              </p>
            )}
          </div>
        )}
      </div>

      {/* Evidence Modal */}
      {showEvidenceModal && (
        <EvidenceModal
          mechanism={mechanism}
          onClose={() => setShowEvidenceModal(false)}
        />
      )}
    </>
  );
};
