/**
 * PathfinderView - Find and visualize paths between nodes in the causal network
 *
 * Features:
 * - Hybrid node selection (autocomplete search + click on graph)
 * - Three pathfinding algorithms
 * - Configurable search depth and path count
 * - Category filtering
 * - Path results with metrics
 * - Graph visualization with path highlighting
 */

import React, { useState, useMemo } from 'react';
import { usePathfinding, PathResult, formatPathLength, getEvidenceGradeColor, getDirectionColor } from '../hooks/usePathfinding';
import { usePathfinderStore, getAlgorithmDisplayName, getAlgorithmDescription } from '../stores/pathfinderStore';
import { PathfindingAlgorithm } from '../types/mechanism';
import { useGraphStateStore } from '../stores/graphStateStore';
import { useGraphData } from '../hooks/useData';
import MechanismGraph from '../visualizations/MechanismGraph';

// ==========================================
// Component
// ==========================================

export const PathfinderView: React.FC = () => {
  // Pathfinder store
  const {
    fromNode,
    toNode,
    paths,
    selectedPathId,
    config,
    setFromNode,
    setToNode,
    swapNodes,
    selectPath,
    setPaths,
    setAlgorithm,
    setMaxDepth,
    setMaxPaths,
    setExcludeCategories,
    setOnlyCategories,
    clear,
  } = usePathfinderStore();

  // Graph state store (for highlighting paths on graph)
  const { setActivePaths, requestZoomToPaths } = useGraphStateStore();

  // Pathfinding mutation
  const { mutate: findPaths, isPending, error } = usePathfinding();

  // Graph data for visualization
  const { data: graphData, isLoading: loadingGraph } = useGraphData();

  // Local UI state
  const [showFilters, setShowFilters] = useState(false);
  const [selectionMode, setSelectionMode] = useState<'from' | 'to'>('from');

  // Selected path object
  const selectedPath = useMemo(() => {
    return paths.find(p => p.pathId === selectedPathId) || null;
  }, [paths, selectedPathId]);

  // ==========================================
  // Handlers
  // ==========================================

  const handleFindPaths = () => {
    if (!fromNode || !toNode) return;

    findPaths(
      {
        fromNode: fromNode.nodeId,
        toNode: toNode.nodeId,
        algorithm: config.algorithm,
        maxDepth: config.maxDepth,
        maxPaths: config.maxPaths,
        excludeCategories: config.excludeCategories.length > 0 ? config.excludeCategories : undefined,
        onlyCategories: config.onlyCategories.length > 0 ? config.onlyCategories : undefined,
      },
      {
        onSuccess: (data) => {
          setPaths(data.paths);
        },
      }
    );
  };

  const handleClear = () => {
    clear();
  };

  const handleHighlightOnGraph = () => {
    // Convert path results to PathHighlight format for graph visualization
    const pathHighlights = paths.map(path => ({
      pathId: path.pathId,
      nodeIds: path.nodes,
      edgeIds: path.edges,
    }));

    // Set active paths in graph state store
    setActivePaths(pathHighlights, selectedPathId);

    // Request zoom to fit all paths
    requestZoomToPaths();
  };

  const handleNodeSelect = (node: any) => {
    if (selectionMode === 'from') {
      setFromNode({ nodeId: node.id, label: node.label });
      setSelectionMode('to'); // Auto-switch to selecting "to" node
    } else {
      setToNode({ nodeId: node.id, label: node.label });
    }
  };

  const isReadyToSearch = fromNode !== null && toNode !== null;

  // ==========================================
  // Render Helpers
  // ==========================================

  const renderPathCard = (path: PathResult) => {
    const isSelected = selectedPathId === path.pathId;

    return (
      <div
        key={path.pathId}
        onClick={() => selectPath(path.pathId)}
        className={`border rounded-lg p-4 cursor-pointer transition-all ${
          isSelected
            ? 'border-blue-500 bg-blue-50 shadow-md'
            : 'border-gray-200 hover:border-gray-300 hover:shadow'
        }`}
      >
        {/* Path Header */}
        <div className="flex items-start justify-between mb-3">
          <div className="flex-1">
            <div className="font-medium text-gray-900">
              Path {path.pathId.replace('path_', '')}
            </div>
            <div className="text-sm text-gray-600 mt-1">
              {path.nodeDetails[0]?.label} → {path.nodeDetails[path.nodeDetails.length - 1]?.label}
            </div>
          </div>
          <div className="flex items-center gap-2">
            {/* Evidence Grade Badge */}
            <span
              className="px-2 py-1 text-xs font-bold rounded"
              style={{
                backgroundColor: getEvidenceGradeColor(path.evidenceGrade),
                color: 'white',
              }}
            >
              Grade {path.evidenceGrade}
            </span>
          </div>
        </div>

        {/* Path Metrics */}
        <div className="grid grid-cols-2 gap-2 text-sm mb-3">
          <div>
            <span className="text-gray-600">Length:</span>{' '}
            <span className="font-medium">{formatPathLength(path.pathLength)}</span>
          </div>
          <div>
            <span className="text-gray-600">Evidence:</span>{' '}
            <span className="font-medium">{path.avgEvidenceQuality.toFixed(2)}</span>
          </div>
          <div>
            <span className="text-gray-600">Direction:</span>{' '}
            <span
              className="font-medium"
              style={{ color: getDirectionColor(path.overallDirection) }}
            >
              {path.overallDirection}
            </span>
          </div>
          <div>
            <span className="text-gray-600">Weight:</span>{' '}
            <span className="font-medium">{path.totalWeight.toFixed(2)}</span>
          </div>
        </div>

        {/* Path Preview */}
        <div className="text-xs text-gray-600 bg-gray-50 rounded p-2">
          {path.nodeDetails.map((node, index) => (
            <React.Fragment key={node.nodeId}>
              <span className="font-medium">{node.label}</span>
              {index < path.nodeDetails.length - 1 && (
                <span className="mx-1">→</span>
              )}
            </React.Fragment>
          ))}
        </div>

        {/* Mechanisms Count */}
        <div className="text-xs text-gray-500 mt-2">
          {path.mechanismDetails.length} mechanism{path.mechanismDetails.length !== 1 ? 's' : ''}
        </div>
      </div>
    );
  };

  // ==========================================
  // Render
  // ==========================================

  return (
    <div className="container mx-auto px-4 py-8">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">
          Pathfinder
        </h1>
        <p className="text-gray-600">
          Find causal pathways between nodes using multiple algorithms
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left Column: Search Controls */}
        <div className="lg:col-span-1">
          <div className="bg-white rounded-lg shadow p-6 sticky top-4">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">
              Search Configuration
            </h2>

            {/* Node Selection */}
            <div className="space-y-4 mb-6">
              {/* From Node */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  From Node
                </label>
                <div className="relative">
                  <input
                    type="text"
                    value={fromNode?.label || ''}
                    readOnly
                    placeholder="Select starting node..."
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-gray-50"
                  />
                  {fromNode && (
                    <button
                      onClick={() => setFromNode(null)}
                      className="absolute right-2 top-2 text-gray-400 hover:text-gray-600"
                    >
                      ✕
                    </button>
                  )}
                </div>
                <p className="mt-1 text-xs text-gray-500">
                  Click a node on the graph to select
                </p>
              </div>

              {/* Swap Button */}
              <div className="flex justify-center">
                <button
                  onClick={swapNodes}
                  disabled={!fromNode && !toNode}
                  className="p-2 text-gray-600 hover:text-gray-900 disabled:text-gray-300 transition-colors"
                  title="Swap nodes"
                >
                  ⇅
                </button>
              </div>

              {/* To Node */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  To Node
                </label>
                <div className="relative">
                  <input
                    type="text"
                    value={toNode?.label || ''}
                    readOnly
                    placeholder="Select target node..."
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-gray-50"
                  />
                  {toNode && (
                    <button
                      onClick={() => setToNode(null)}
                      className="absolute right-2 top-2 text-gray-400 hover:text-gray-600"
                    >
                      ✕
                    </button>
                  )}
                </div>
                <p className="mt-1 text-xs text-gray-500">
                  Click a node on the graph to select
                </p>
              </div>
            </div>

            {/* Algorithm Selection */}
            <div className="mb-6">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Algorithm
              </label>
              <div className="space-y-2">
                {(['shortest', 'strongest_evidence', 'all_simple'] as PathfindingAlgorithm[]).map(
                  (algo) => (
                    <label
                      key={algo}
                      className="flex items-start p-3 border rounded-lg cursor-pointer hover:bg-gray-50 transition-colors"
                    >
                      <input
                        type="radio"
                        name="algorithm"
                        value={algo}
                        checked={config.algorithm === algo}
                        onChange={() => setAlgorithm(algo)}
                        className="mt-1 mr-3"
                      />
                      <div className="flex-1">
                        <div className="font-medium text-sm text-gray-900">
                          {getAlgorithmDisplayName(algo)}
                        </div>
                        <div className="text-xs text-gray-600 mt-1">
                          {getAlgorithmDescription(algo)}
                        </div>
                      </div>
                    </label>
                  )
                )}
              </div>
            </div>

            {/* Max Depth */}
            <div className="mb-6">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Maximum Depth: {config.maxDepth} hops
              </label>
              <input
                type="range"
                min="2"
                max="8"
                step="1"
                value={config.maxDepth}
                onChange={(e) => setMaxDepth(Number(e.target.value))}
                className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"
              />
              <div className="flex justify-between text-xs text-gray-500 mt-1">
                <span>2</span>
                <span>8</span>
              </div>
            </div>

            {/* Max Paths (for all_simple) */}
            {config.algorithm === 'all_simple' && (
              <div className="mb-6">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Maximum Paths: {config.maxPaths}
                </label>
                <input
                  type="range"
                  min="5"
                  max="50"
                  step="5"
                  value={config.maxPaths}
                  onChange={(e) => setMaxPaths(Number(e.target.value))}
                  className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"
                />
                <div className="flex justify-between text-xs text-gray-500 mt-1">
                  <span>5</span>
                  <span>50</span>
                </div>
              </div>
            )}

            {/* Advanced Filters Toggle */}
            <button
              onClick={() => setShowFilters(!showFilters)}
              className="text-sm text-blue-600 hover:text-blue-700 mb-4"
            >
              {showFilters ? '− Hide' : '+ Show'} Advanced Filters
            </button>

            {/* Advanced Filters */}
            {showFilters && (
              <div className="mb-6 p-4 bg-gray-50 rounded-lg border border-gray-200">
                <h3 className="text-sm font-medium text-gray-700 mb-3">
                  Category Filters
                </h3>

                {/* Exclude Categories */}
                <div className="mb-4">
                  <label className="block text-xs font-medium text-gray-600 mb-2">
                    Exclude Categories (avoid these in paths)
                  </label>
                  <div className="flex flex-wrap gap-2">
                    {(['economic', 'healthcare_access', 'social_environment', 'built_environment', 'political', 'behavioral', 'biological'] as const).map(
                      category => (
                        <button
                          key={category}
                          onClick={() => {
                            const current = config.excludeCategories;
                            if (current.includes(category)) {
                              setExcludeCategories(current.filter(c => c !== category));
                            } else {
                              setExcludeCategories([...current, category]);
                            }
                          }}
                          className={`px-2 py-1 rounded text-xs transition-colors ${
                            config.excludeCategories.includes(category)
                              ? 'bg-red-600 text-white'
                              : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                          }`}
                        >
                          {category.replace('_', ' ')}
                        </button>
                      )
                    )}
                  </div>
                </div>

                {/* Only Categories */}
                <div>
                  <label className="block text-xs font-medium text-gray-600 mb-2">
                    Only Categories (require these in paths)
                  </label>
                  <div className="flex flex-wrap gap-2">
                    {(['economic', 'healthcare_access', 'social_environment', 'built_environment', 'political', 'behavioral', 'biological'] as const).map(
                      category => (
                        <button
                          key={category}
                          onClick={() => {
                            const current = config.onlyCategories;
                            if (current.includes(category)) {
                              setOnlyCategories(current.filter(c => c !== category));
                            } else {
                              setOnlyCategories([...current, category]);
                            }
                          }}
                          className={`px-2 py-1 rounded text-xs transition-colors ${
                            config.onlyCategories.includes(category)
                              ? 'bg-green-600 text-white'
                              : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                          }`}
                        >
                          {category.replace('_', ' ')}
                        </button>
                      )
                    )}
                  </div>
                </div>

                {/* Clear filters button */}
                {(config.excludeCategories.length > 0 || config.onlyCategories.length > 0) && (
                  <button
                    onClick={() => {
                      setExcludeCategories([]);
                      setOnlyCategories([]);
                    }}
                    className="mt-3 text-xs text-blue-600 hover:text-blue-700"
                  >
                    Clear category filters
                  </button>
                )}
              </div>
            )}

            {/* Action Buttons */}
            <div className="space-y-2">
              <button
                onClick={handleFindPaths}
                disabled={!isReadyToSearch || isPending}
                className="w-full px-4 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors font-medium"
              >
                {isPending ? (
                  <span className="flex items-center justify-center">
                    <span className="inline-block animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></span>
                    Searching...
                  </span>
                ) : (
                  'Find Paths'
                )}
              </button>
              <button
                onClick={handleClear}
                className="w-full px-4 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 transition-colors"
              >
                Clear
              </button>
            </div>

            {/* Error Display */}
            {error && (
              <div className="mt-4 p-3 bg-red-50 border border-red-200 rounded-lg">
                <div className="text-sm font-medium text-red-800 mb-1">
                  Error
                </div>
                <div className="text-xs text-red-600">{error.message}</div>
              </div>
            )}
          </div>
        </div>

        {/* Right Column: Results */}
        <div className="lg:col-span-2">
          {/* Results Header */}
          {paths.length > 0 && (
            <div className="bg-white rounded-lg shadow p-4 mb-6">
              <div className="flex items-center justify-between">
                <div>
                  <h2 className="text-lg font-semibold text-gray-900">
                    Found {paths.length} path{paths.length !== 1 ? 's' : ''}
                  </h2>
                  <p className="text-sm text-gray-600">
                    From <span className="font-medium">{fromNode?.label}</span> to{' '}
                    <span className="font-medium">{toNode?.label}</span>
                  </p>
                </div>
                {selectedPath && (
                  <button
                    onClick={handleHighlightOnGraph}
                    className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
                  >
                    Highlight on Graph
                  </button>
                )}
              </div>
            </div>
          )}

          {/* Graph Visualization for Node Selection */}
          {!isPending && paths.length === 0 && !error && (
            <div className="bg-white rounded-lg shadow p-6">
              <div className="mb-4">
                <h3 className="text-lg font-semibold text-gray-900 mb-2">
                  Select Nodes on Graph
                </h3>
                <p className="text-sm text-gray-600 mb-3">
                  Currently selecting: <span className="font-medium text-blue-600">
                    {selectionMode === 'from' ? 'Starting Node' : 'Target Node'}
                  </span>
                </p>
                <div className="flex gap-2">
                  <button
                    onClick={() => setSelectionMode('from')}
                    className={`px-3 py-1 text-sm rounded ${
                      selectionMode === 'from'
                        ? 'bg-blue-600 text-white'
                        : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                    }`}
                  >
                    Select From Node
                  </button>
                  <button
                    onClick={() => setSelectionMode('to')}
                    className={`px-3 py-1 text-sm rounded ${
                      selectionMode === 'to'
                        ? 'bg-blue-600 text-white'
                        : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                    }`}
                  >
                    Select To Node
                  </button>
                </div>
              </div>
              {loadingGraph ? (
                <div className="flex items-center justify-center py-12">
                  <div className="text-center">
                    <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mb-2"></div>
                    <p className="text-sm text-gray-600">Loading graph...</p>
                  </div>
                </div>
              ) : graphData ? (
                <div className="border rounded">
                  <MechanismGraph
                    data={graphData}
                    width={800}
                    height={600}
                    onNodeClick={handleNodeSelect}
                    selectionMode={selectionMode === 'from' ? 'from' : 'to'}
                  />
                </div>
              ) : (
                <div className="text-center py-12 text-gray-600">
                  No graph data available
                </div>
              )}
            </div>
          )}

          {/* Path Results */}
          {paths.length > 0 && (
            <div className="space-y-4">
              {paths.map(path => renderPathCard(path))}
            </div>
          )}

          {/* Loading State */}
          {isPending && (
            <div className="bg-white rounded-lg shadow p-12 text-center">
              <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mb-4"></div>
              <div className="text-gray-600">Searching for paths...</div>
            </div>
          )}

          {/* Selected Path Details */}
          {selectedPath && (
            <div className="mt-6 bg-white rounded-lg shadow p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">
                Path Details
              </h3>

              {/* Mechanisms List */}
              <div className="space-y-3">
                {selectedPath.mechanismDetails.map((mechanism, index) => (
                  <div
                    key={mechanism.mechanismId}
                    className="border-l-4 border-blue-500 pl-4 py-2"
                  >
                    <div className="flex items-start justify-between">
                      <div className="flex-1">
                        <div className="font-medium text-sm text-gray-900">
                          {index + 1}. {mechanism.name}
                        </div>
                        <div className="text-xs text-gray-600 mt-1">
                          {mechanism.fromNode} → {mechanism.toNode}
                        </div>
                      </div>
                      <div className="flex items-center gap-2 ml-4">
                        <span
                          className={`px-2 py-1 text-xs font-medium rounded ${
                            mechanism.direction === 'positive'
                              ? 'bg-green-100 text-green-800'
                              : 'bg-red-100 text-red-800'
                          }`}
                        >
                          {mechanism.direction === 'positive' ? '↑' : '↓'}
                        </span>
                        {mechanism.evidenceQuality && (
                          <span
                            className="px-2 py-1 text-xs font-bold rounded"
                            style={{
                              backgroundColor: getEvidenceGradeColor(mechanism.evidenceQuality),
                              color: 'white',
                            }}
                          >
                            {mechanism.evidenceQuality}
                          </span>
                        )}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default PathfinderView;
