/**
 * MetadataDrivenSystemView - Generalized focal node exploration component
 *
 * Supports:
 * - Domain filtering via keywords
 * - Focal node selection and exploration
 * - Category/scale filtering
 * - Upstream/downstream/both traversal modes
 * - Hierarchical and force-directed layouts
 *
 * Replaces hardcoded AlcoholismSystemDiagram with metadata-driven approach.
 */

import React, { useState, useMemo } from 'react';
import MechanismGraph from '../visualizations/MechanismGraph';
import { Badge } from '../components/base/Badge';
import { useMechanismsForGraph } from '../hooks/useData';
import { buildDomainSubgraph, buildFocalNodeSubgraph } from '../utils/graphBuilder';
import type { Category, NodeScale, MechanismNode, GraphLayoutMode } from '../types/mechanism';
import type { TraversalDirection } from '../utils/graphNeighborhood';

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
}

export const MetadataDrivenSystemView: React.FC<MetadataDrivenSystemViewProps> = ({
  domainKeywords,
  initialCategories,
  initialScales,
  title,
  description
}) => {
  // Fetch all mechanisms
  const { data: allMechanisms, isLoading, error } = useMechanismsForGraph();

  // State for focal node exploration
  const [focalNodeId, setFocalNodeId] = useState<string | null>(null);
  const [traversalDirection, setTraversalDirection] = useState<TraversalDirection>('both');
  const [filterCategories, setFilterCategories] = useState<Category[]>(initialCategories || []);
  const [filterScales, setFilterScales] = useState<NodeScale[]>(initialScales || []);
  const [showFilterPanel, setShowFilterPanel] = useState(false);

  // Layout state
  const [layoutMode, setLayoutMode] = useState<GraphLayoutMode>('hierarchical');

  // Build domain-specific subgraph
  const domainGraph = useMemo(() => {
    if (!allMechanisms) return { nodes: [], edges: [] };

    return buildDomainSubgraph(allMechanisms, domainKeywords, {
      includeCategories: filterCategories.length > 0 ? filterCategories : undefined,
      includeScales: filterScales.length > 0 ? filterScales : undefined,
      includeDisconnected: false
    });
  }, [allMechanisms, domainKeywords, filterCategories, filterScales]);

  // Build focal node subgraph if focal node selected
  const displayGraph = useMemo(() => {
    if (!focalNodeId) return domainGraph;

    return buildFocalNodeSubgraph(domainGraph, focalNodeId, {
      direction: traversalDirection,
      includeCategories: filterCategories.length > 0 ? filterCategories : undefined,
      includeScales: filterScales.length > 0 ? filterScales : undefined,
      maxHopsUpstream: null, // Unlimited
      maxHopsDownstream: null // Unlimited
    });
  }, [domainGraph, focalNodeId, traversalDirection, filterCategories, filterScales]);

  // Find focal node object
  const focalNode = focalNodeId
    ? displayGraph.nodes.find(n => n.id === focalNodeId)
    : null;

  // Handle node click
  const handleNodeClick = (node: MechanismNode) => {
    if (focalNodeId === node.id) {
      // Deselect if clicking same node
      setFocalNodeId(null);
    } else {
      setFocalNodeId(node.id);
    }
  };

  // Handle clear filters
  const handleClearFilters = () => {
    setFocalNodeId(null);
    setFilterCategories(initialCategories || []);
    setFilterScales(initialScales || []);
    setTraversalDirection('both');
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-full">
        <p className="text-gray-500">Loading system data...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex items-center justify-center h-full">
        <p className="text-red-500">Error loading data: {error.message}</p>
      </div>
    );
  }

  return (
    <div className="flex flex-col h-full">
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

        {/* Active focal node indicator */}
        {focalNode && (
          <div className="mt-4 flex items-center gap-2 p-3 bg-orange-50 border border-orange-200 rounded-lg">
            <span className="text-sm font-medium text-orange-900">Focal Node:</span>
            <Badge color="primary">{focalNode.label}</Badge>
            {focalNode.scale && <Badge color="gray">Scale {focalNode.scale}</Badge>}
            <Badge color="gray">{traversalDirection}</Badge>
            <button
              onClick={() => setFocalNodeId(null)}
              className="ml-auto text-sm text-orange-700 hover:text-orange-900"
            >
              Clear
            </button>
          </div>
        )}
      </div>

      {/* Main content */}
      <div className="flex flex-1 overflow-hidden">
        {/* Filter panel */}
        {showFilterPanel && (
          <FocalNodeFilterPanel
            focalNodeId={focalNodeId}
            traversalDirection={traversalDirection}
            onTraversalDirectionChange={setTraversalDirection}
            filterCategories={filterCategories}
            onFilterCategoriesChange={setFilterCategories}
            filterScales={filterScales}
            onFilterScalesChange={setFilterScales}
            onClearFilters={handleClearFilters}
            availableNodes={domainGraph.nodes}
            onSelectFocalNode={setFocalNodeId}
          />
        )}

        {/* Graph visualization */}
        <div className="flex-1">
          <MechanismGraph
            data={displayGraph}
            selectedNodeId={focalNodeId}
            onNodeClick={handleNodeClick}
            layoutMode={layoutMode}
            importantNodes={focalNodeId ? { nodeIds: [focalNodeId] } : undefined}
          />
        </div>
      </div>

      {/* Stats footer */}
      <div className="border-t border-gray-200 bg-gray-50 px-6 py-3">
        <div className="flex items-center gap-6 text-sm text-gray-600">
          <span>{displayGraph.nodes.length} nodes</span>
          <span>{displayGraph.edges.length} mechanisms</span>
          {focalNodeId && (
            <>
              <span className="text-orange-600">•</span>
              <span className="text-orange-600">
                Exploring from {focalNode?.label} (Scale {focalNode?.scale})
              </span>
            </>
          )}
        </div>
      </div>
    </div>
  );
};

// ============================================
// FocalNodeFilterPanel Component
// ============================================

interface FocalNodeFilterPanelProps {
  focalNodeId: string | null;
  traversalDirection: TraversalDirection;
  onTraversalDirectionChange: (direction: TraversalDirection) => void;
  filterCategories: Category[];
  onFilterCategoriesChange: (categories: Category[]) => void;
  filterScales: NodeScale[];
  onFilterScalesChange: (scales: NodeScale[]) => void;
  onClearFilters: () => void;
  availableNodes: MechanismNode[];
  onSelectFocalNode: (nodeId: string) => void;
}

const FocalNodeFilterPanel: React.FC<FocalNodeFilterPanelProps> = ({
  focalNodeId,
  traversalDirection,
  onTraversalDirectionChange,
  filterCategories,
  onFilterCategoriesChange,
  filterScales,
  onFilterScalesChange,
  onClearFilters,
  availableNodes,
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
        {/* Focal Node Selection */}
        <div>
          <h3 className="text-sm font-semibold text-gray-900 mb-2">Focal Node</h3>
          <p className="text-xs text-gray-500 mb-3">
            Select a node to explore its causal neighborhood
          </p>

          {focalNodeId ? (
            <div className="p-2 bg-orange-50 border border-orange-200 rounded text-sm">
              {availableNodes.find(n => n.id === focalNodeId)?.label || focalNodeId}
            </div>
          ) : (
            <p className="text-sm text-gray-400 italic">Click a node in the graph</p>
          )}
        </div>

        {/* Traversal Direction */}
        {focalNodeId && (
          <div>
            <h3 className="text-sm font-semibold text-gray-900 mb-2">Traversal Direction</h3>
            <div className="flex flex-col gap-2">
              {(['upstream', 'downstream', 'both'] as TraversalDirection[]).map(direction => (
                <label key={direction} className="flex items-center gap-2 cursor-pointer">
                  <input
                    type="radio"
                    checked={traversalDirection === direction}
                    onChange={() => onTraversalDirectionChange(direction)}
                    className="text-orange-600 focus:ring-orange-500"
                  />
                  <span className="text-sm capitalize text-gray-700">{direction}</span>
                  <span className="text-xs text-gray-400">
                    {direction === 'upstream' && '(causes)'}
                    {direction === 'downstream' && '(effects)'}
                    {direction === 'both' && '(full lineage)'}
                  </span>
                </label>
              ))}
            </div>
          </div>
        )}

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
