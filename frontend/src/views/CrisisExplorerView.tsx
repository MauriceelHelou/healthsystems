/**
 * CrisisExplorerView - Explore upstream causal pathways leading to crisis endpoints
 *
 * Features:
 * - Select multiple crisis endpoints (scale=7 nodes)
 * - Configure upstream traversal (max degrees, evidence strength)
 * - Visualize crisis subgraph with policy levers
 * - View statistics and policy intervention points
 */

import React, { useState, useMemo } from 'react';
import { useCrisisEndpoints } from '../hooks/useCrisisEndpoints';
import { useCrisisSubgraph, getDegreeColor, getDegreeLabel } from '../hooks/useCrisisSubgraph';
import MechanismGraph from '../visualizations/MechanismGraph';
import { CategoryBadge } from '../components/domain/CategoryBadge';
import { CrisisNodeWithDegree, SystemsNetwork, CrisisHighlight } from '../types/mechanism';

// ==========================================
// Component
// ==========================================

export const CrisisExplorerView: React.FC = () => {
  // API hooks
  const { data: crisisEndpoints, isLoading: loadingEndpoints, error: endpointsError } = useCrisisEndpoints();
  const { mutate: explorePathways, data: subgraphData, isPending, error: explorationError } = useCrisisSubgraph();

  // Local state
  const [selectedCrisisIds, setSelectedCrisisIds] = useState<string[]>([]);
  const [maxDegrees, setMaxDegrees] = useState<number>(5);
  const [minStrength, setMinStrength] = useState<number>(2); // 1=C, 2=B, 3=A
  const [showAdvanced, setShowAdvanced] = useState(false);
  const [activeTab, setActiveTab] = useState<'all' | 'policy-levers'>('all');

  // ==========================================
  // Computed Values
  // ==========================================

  // Transform subgraph data to SystemsNetwork format for MechanismGraph
  const networkData: SystemsNetwork | null = useMemo(() => {
    if (!subgraphData) return null;

    return {
      nodes: subgraphData.nodes.map(node => ({
        id: node.nodeId,
        label: node.label,
        weight: 1,
        category: node.category,
        stockType: 'proxy' as const,
        scale: node.scale,
        connections: {
          outgoing: 0,
          incoming: 0,
        },
      })),
      edges: subgraphData.edges.map(edge => ({
        id: edge.mechanismId,
        source: edge.source,
        target: edge.target,
        strength: edge.strength,
        direction: edge.direction,
        category: edge.category,
        evidenceQuality: edge.evidenceQuality,
        studyCount: 0,
      })),
    };
  }, [subgraphData]);

  // Create crisis highlight data for MechanismGraph
  const crisisHighlight: CrisisHighlight | undefined = useMemo(() => {
    if (!subgraphData) return undefined;

    const nodeIdToDegree = new Map<string, number>();
    const policyLeverIds = new Set<string>();

    subgraphData.nodes.forEach(node => {
      nodeIdToDegree.set(node.nodeId, node.degreeFromCrisis);
      if (node.isPolicyLever) {
        policyLeverIds.add(node.nodeId);
      }
    });

    return { nodeIdToDegree, policyLeverIds };
  }, [subgraphData]);

  // Filtered nodes for display
  const displayedNodes = useMemo(() => {
    if (!subgraphData) return [];

    if (activeTab === 'policy-levers') {
      return subgraphData.nodes.filter(node => node.isPolicyLever);
    }

    return subgraphData.nodes;
  }, [subgraphData, activeTab]);

  // ==========================================
  // Handlers
  // ==========================================

  const handleCrisisToggle = (nodeId: string) => {
    setSelectedCrisisIds(prev => {
      if (prev.includes(nodeId)) {
        return prev.filter(id => id !== nodeId);
      } else {
        // Max 10 crisis nodes
        if (prev.length >= 10) return prev;
        return [...prev, nodeId];
      }
    });
  };

  const handleExplore = () => {
    if (selectedCrisisIds.length === 0) return;

    explorePathways({
      crisisNodeIds: selectedCrisisIds,
      maxDegrees,
      minStrength,
    });
  };

  const handleReset = () => {
    setSelectedCrisisIds([]);
    setMaxDegrees(5);
    setMinStrength(2);
  };

  const isReadyToExplore = selectedCrisisIds.length > 0;

  // ==========================================
  // Render Helpers
  // ==========================================

  const renderCrisisSelection = () => {
    if (loadingEndpoints) {
      return (
        <div className="text-sm text-gray-600 py-4 text-center">
          Loading crisis endpoints...
        </div>
      );
    }

    if (endpointsError) {
      return (
        <div className="text-sm text-red-600 py-4">
          Error loading crisis endpoints: {endpointsError.message}
        </div>
      );
    }

    if (!crisisEndpoints || crisisEndpoints.length === 0) {
      return (
        <div className="text-sm text-gray-600 py-4">
          No crisis endpoints found
        </div>
      );
    }

    return (
      <div className="space-y-2 max-h-64 overflow-y-auto">
        {crisisEndpoints.map(crisis => (
          <label
            key={crisis.nodeId}
            className="flex items-start p-3 border rounded-lg cursor-pointer hover:bg-gray-50 transition-colors"
          >
            <input
              type="checkbox"
              checked={selectedCrisisIds.includes(crisis.nodeId)}
              onChange={() => handleCrisisToggle(crisis.nodeId)}
              disabled={!selectedCrisisIds.includes(crisis.nodeId) && selectedCrisisIds.length >= 10}
              className="mt-1 mr-3"
            />
            <div className="flex-1">
              <div className="font-medium text-sm text-gray-900">
                {crisis.label}
              </div>
              <div className="mt-1">
                <CategoryBadge category={crisis.category} />
              </div>
              {crisis.description && (
                <div className="text-xs text-gray-600 mt-2">
                  {crisis.description}
                </div>
              )}
            </div>
          </label>
        ))}
      </div>
    );
  };

  const renderNodeCard = (node: CrisisNodeWithDegree) => {
    return (
      <div
        key={node.nodeId}
        className="border rounded-lg p-4 hover:shadow transition-shadow"
        style={{
          borderLeftWidth: '4px',
          borderLeftColor: getDegreeColor(node.degreeFromCrisis),
        }}
      >
        {/* Node Header */}
        <div className="flex items-start justify-between mb-2">
          <div className="flex-1">
            <div className="font-medium text-gray-900">
              {node.label}
            </div>
            <div className="flex items-center gap-2 mt-1">
              <CategoryBadge category={node.category} />
              <span className="text-xs text-gray-500">
                Scale {node.scale}
              </span>
            </div>
          </div>
          {node.isPolicyLever && (
            <span className="px-2 py-1 text-xs font-bold rounded bg-yellow-100 text-yellow-800 border border-yellow-300">
              Policy Lever
            </span>
          )}
        </div>

        {/* Degree Info */}
        <div className="text-sm text-gray-700 mb-2">
          <span className="font-medium">
            {getDegreeLabel(node.degreeFromCrisis)}
          </span>
          <span className="text-gray-500 ml-2">
            ({node.degreeFromCrisis} {node.degreeFromCrisis === 1 ? 'degree' : 'degrees'} from crisis)
          </span>
        </div>

        {/* Description */}
        {node.description && (
          <div className="text-xs text-gray-600 mt-2 bg-gray-50 rounded p-2">
            {node.description}
          </div>
        )}
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
          Crisis Endpoint Explorer
        </h1>
        <p className="text-gray-600">
          Select crisis outcomes to discover upstream causal pathways and policy levers
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left Column: Control Panel */}
        <div className="lg:col-span-1">
          <div className="bg-white rounded-lg shadow p-6 sticky top-4">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">
              Configuration
            </h2>

            {/* Crisis Selection */}
            <div className="mb-6">
              <div className="flex items-center justify-between mb-3">
                <label className="block text-sm font-medium text-gray-700">
                  Crisis Endpoints
                </label>
                {selectedCrisisIds.length > 0 && (
                  <span className="text-xs text-gray-600">
                    {selectedCrisisIds.length} / 10 selected
                  </span>
                )}
              </div>
              {renderCrisisSelection()}
              {selectedCrisisIds.length > 0 && (
                <button
                  onClick={() => setSelectedCrisisIds([])}
                  className="mt-3 text-sm text-blue-600 hover:text-blue-700"
                >
                  Clear selection
                </button>
              )}
            </div>

            {/* Filters */}
            <div className="mb-6">
              <h3 className="text-sm font-medium text-gray-700 mb-3">
                Upstream Traversal
              </h3>

              {/* Max Degrees */}
              <div className="mb-4">
                <label className="block text-sm text-gray-600 mb-2">
                  Maximum Distance: {maxDegrees} {maxDegrees === 1 ? 'degree' : 'degrees'}
                </label>
                <input
                  type="range"
                  min="1"
                  max="8"
                  step="1"
                  value={maxDegrees}
                  onChange={(e) => setMaxDegrees(Number(e.target.value))}
                  className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"
                />
                <div className="flex justify-between text-xs text-gray-500 mt-1">
                  <span>1</span>
                  <span>8</span>
                </div>
                <p className="text-xs text-gray-500 mt-2">
                  Maximum upstream distance from crisis endpoints
                </p>
              </div>

              {/* Evidence Strength */}
              <div className="mb-4">
                <label className="block text-sm text-gray-600 mb-2">
                  Minimum Evidence Strength
                </label>
                <div className="space-y-2">
                  {[
                    { value: 3, label: 'High (A)', desc: 'Strong evidence only' },
                    { value: 2, label: 'Medium (B+)', desc: 'Good to strong evidence' },
                    { value: 1, label: 'Low (C+)', desc: 'All evidence levels' },
                  ].map(option => (
                    <label
                      key={option.value}
                      className="flex items-start p-2 border rounded cursor-pointer hover:bg-gray-50 transition-colors"
                    >
                      <input
                        type="radio"
                        name="minStrength"
                        value={option.value}
                        checked={minStrength === option.value}
                        onChange={() => setMinStrength(option.value)}
                        className="mt-1 mr-3"
                      />
                      <div className="flex-1">
                        <div className="text-sm font-medium text-gray-900">
                          {option.label}
                        </div>
                        <div className="text-xs text-gray-600">
                          {option.desc}
                        </div>
                      </div>
                    </label>
                  ))}
                </div>
              </div>
            </div>

            {/* Advanced Filters */}
            <button
              onClick={() => setShowAdvanced(!showAdvanced)}
              className="text-sm text-blue-600 hover:text-blue-700 mb-4"
            >
              {showAdvanced ? '− Hide' : '+ Show'} Advanced Filters
            </button>

            {showAdvanced && (
              <div className="mb-6 p-3 bg-gray-50 rounded-lg">
                <p className="text-xs text-gray-600">
                  Category filters (future enhancement)
                </p>
              </div>
            )}

            {/* Action Buttons */}
            <div className="space-y-2">
              <button
                onClick={handleExplore}
                disabled={!isReadyToExplore || isPending}
                className="w-full px-4 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors font-medium"
              >
                {isPending ? (
                  <span className="flex items-center justify-center">
                    <span className="inline-block animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></span>
                    Exploring...
                  </span>
                ) : (
                  'Explore Pathways'
                )}
              </button>
              <button
                onClick={handleReset}
                className="w-full px-4 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 transition-colors"
              >
                Reset
              </button>
            </div>

            {/* Error Display */}
            {explorationError && (
              <div className="mt-4 p-3 bg-red-50 border border-red-200 rounded-lg">
                <div className="text-sm font-medium text-red-800 mb-1">
                  Error
                </div>
                <div className="text-xs text-red-600">{explorationError.message}</div>
              </div>
            )}
          </div>
        </div>

        {/* Right Column: Results & Visualization */}
        <div className="lg:col-span-2">
          {/* Empty State */}
          {!isPending && !subgraphData && (
            <div className="bg-white rounded-lg shadow p-12 text-center">
              <div className="text-gray-400 text-6xl mb-4">🎯</div>
              <h3 className="text-lg font-medium text-gray-900 mb-2">
                Select crisis endpoints to explore
              </h3>
              <p className="text-gray-600 mb-6">
                Choose one or more crisis outcomes to discover upstream causal pathways and policy levers
              </p>
              <div className="text-sm text-gray-500">
                <p className="font-medium mb-2">How it works:</p>
                <ul className="mt-2 space-y-1 text-left max-w-md mx-auto">
                  <li>• Select one or more crisis endpoints from the left panel</li>
                  <li>• Configure how far upstream to search (1-8 degrees)</li>
                  <li>• Filter by evidence quality</li>
                  <li>• Discover policy levers and intervention points</li>
                </ul>
              </div>
            </div>
          )}

          {/* Loading State */}
          {isPending && (
            <div className="bg-white rounded-lg shadow p-12 text-center">
              <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mb-4"></div>
              <div className="text-gray-600">Exploring upstream pathways...</div>
            </div>
          )}

          {/* Results */}
          {subgraphData && networkData && (
            <div className="space-y-6">
              {/* Statistics Card */}
              <div className="bg-white rounded-lg shadow p-6">
                <h2 className="text-lg font-semibold text-gray-900 mb-4">
                  Subgraph Statistics
                </h2>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                  <div>
                    <div className="text-2xl font-bold text-blue-600">
                      {subgraphData.stats.totalNodes}
                    </div>
                    <div className="text-sm text-gray-600">Total Nodes</div>
                  </div>
                  <div>
                    <div className="text-2xl font-bold text-green-600">
                      {subgraphData.stats.policyLevers}
                    </div>
                    <div className="text-sm text-gray-600">Policy Levers</div>
                  </div>
                  <div>
                    <div className="text-2xl font-bold text-purple-600">
                      {subgraphData.stats.totalEdges}
                    </div>
                    <div className="text-sm text-gray-600">Mechanisms</div>
                  </div>
                  <div>
                    <div className="text-2xl font-bold text-orange-600">
                      {subgraphData.stats.avgDegree.toFixed(1)}
                    </div>
                    <div className="text-sm text-gray-600">Avg Degree</div>
                  </div>
                </div>

                {/* Category Breakdown */}
                <div className="mt-4 pt-4 border-t">
                  <h3 className="text-sm font-medium text-gray-700 mb-2">
                    Category Breakdown
                  </h3>
                  <div className="flex flex-wrap gap-2">
                    {Object.entries(subgraphData.stats.categoryBreakdown)
                      .sort(([, a], [, b]) => b - a)
                      .slice(0, 5)
                      .map(([category, count]) => (
                        <span
                          key={category}
                          className="px-2 py-1 text-xs rounded bg-gray-100 text-gray-700"
                        >
                          {category}: {count}
                        </span>
                      ))}
                  </div>
                </div>
              </div>

              {/* Visualization */}
              <div className="bg-white rounded-lg shadow p-6">
                <h2 className="text-lg font-semibold text-gray-900 mb-4">
                  Crisis Pathway Network
                </h2>
                <div className="border rounded">
                  <MechanismGraph
                    data={networkData}
                    width={800}
                    height={600}
                    showLegend={true}
                    crisisHighlight={crisisHighlight}
                  />
                </div>
              </div>

              {/* Node List */}
              <div className="bg-white rounded-lg shadow p-6">
                <div className="flex items-center justify-between mb-4">
                  <h2 className="text-lg font-semibold text-gray-900">
                    Nodes
                  </h2>
                  <div className="flex gap-2">
                    <button
                      onClick={() => setActiveTab('all')}
                      className={`px-3 py-1 text-sm rounded transition-colors ${
                        activeTab === 'all'
                          ? 'bg-blue-600 text-white'
                          : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                      }`}
                    >
                      All Nodes ({subgraphData.nodes.length})
                    </button>
                    <button
                      onClick={() => setActiveTab('policy-levers')}
                      className={`px-3 py-1 text-sm rounded transition-colors ${
                        activeTab === 'policy-levers'
                          ? 'bg-blue-600 text-white'
                          : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                      }`}
                    >
                      Policy Levers ({subgraphData.stats.policyLevers})
                    </button>
                  </div>
                </div>

                <div className="space-y-3">
                  {displayedNodes.length > 0 ? (
                    displayedNodes.map(node => renderNodeCard(node))
                  ) : (
                    <div className="text-center py-8 text-gray-600">
                      No {activeTab === 'policy-levers' ? 'policy levers' : 'nodes'} found
                    </div>
                  )}
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default CrisisExplorerView;
