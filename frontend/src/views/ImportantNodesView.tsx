/**
 * ImportantNodesView - Display and manage important nodes in the causal network
 *
 * Features:
 * - Ranked table of important nodes with sortable columns
 * - Filters for category, scale, and minimum connections
 * - Adjustable top N slider (10-50 nodes)
 * - Click nodes to highlight on integrated graph
 * - Export functionality
 * - Responsive design
 */

import React, { useState, useMemo } from 'react';
import { useNodeImportance, formatImportanceScore, sortNodeImportance, calculateImportanceStats } from '../hooks/useNodeImportance';
import { NodeScale, NodeImportance } from '../types/mechanism';
import { CategoryBadge } from '../components/domain/CategoryBadge';
import { useGraphStateStore } from '../stores/graphStateStore';

// ==========================================
// Types
// ==========================================

type SortField = keyof NodeImportance;
type SortDirection = 'asc' | 'desc';

interface FilterState {
  scales: NodeScale[];
  minConnections: number;
}

// ==========================================
// Component
// ==========================================

export const ImportantNodesView: React.FC = () => {
  // Graph state store (shared with graph visualization)
  const { selectedNodeId, setSelectedNode, requestZoomToNode } = useGraphStateStore();

  // Local state
  const [topN, setTopN] = useState<number>(20);
  const [filters, setFilters] = useState<FilterState>({
    scales: [],
    minConnections: 0,
  });
  const [sortField, setSortField] = useState<SortField>('rank');
  const [sortDirection, setSortDirection] = useState<SortDirection>('asc');

  // Fetch data
  const {
    data: nodes,
    isLoading,
    error,
    refetch,
  } = useNodeImportance({
    topN,
    scales: filters.scales.length > 0 ? filters.scales : undefined,
    minConnections: filters.minConnections > 0 ? filters.minConnections : undefined,
  });

  // Sorted nodes
  const sortedNodes = useMemo(() => {
    if (!nodes) return [];
    return sortNodeImportance(nodes, sortField, sortDirection === 'asc');
  }, [nodes, sortField, sortDirection]);

  // Statistics
  const stats = useMemo(() => {
    return calculateImportanceStats(nodes || []);
  }, [nodes]);

  // ==========================================
  // Handlers
  // ==========================================

  const handleSort = (field: SortField) => {
    if (sortField === field) {
      // Toggle direction
      setSortDirection(sortDirection === 'asc' ? 'desc' : 'asc');
    } else {
      // New field, default to descending for scores, ascending for others
      setSortField(field);
      setSortDirection(
        field === 'rank' || field === 'label' ? 'asc' : 'desc'
      );
    }
  };

  const handleNodeClick = (node: NodeImportance) => {
    const newSelectedId = node.nodeId === selectedNodeId ? null : node.nodeId;
    setSelectedNode(newSelectedId);

    // Request zoom/scroll to the selected node on graph
    if (newSelectedId) {
      requestZoomToNode(newSelectedId);
    }
  };

  const handleScaleFilter = (scale: NodeScale) => {
    setFilters(prev => ({
      ...prev,
      scales: prev.scales.includes(scale)
        ? prev.scales.filter(s => s !== scale)
        : [...prev.scales, scale],
    }));
  };

  const handleClearFilters = () => {
    setFilters({
      scales: [],
      minConnections: 0,
    });
  };

  const handleExport = () => {
    if (!nodes) return;

    // Export as CSV
    const headers = [
      'Rank',
      'Node',
      'Category',
      'Scale',
      'Importance Score',
      'Connections',
      'Evidence Quality',
    ].join(',');

    const rows = nodes.map(node =>
      [
        node.rank,
        `"${node.label}"`,
        node.category,
        node.scale || 'N/A',
        formatImportanceScore(node.compositeScore),
        node.totalConnections,
        node.avgEvidenceQuality.toFixed(2),
      ].join(',')
    );

    const csv = [headers, ...rows].join('\n');
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `important-nodes-${new Date().toISOString().split('T')[0]}.csv`;
    a.click();
    URL.revokeObjectURL(url);
  };

  // ==========================================
  // Render Helpers
  // ==========================================

  const renderSortIcon = (field: SortField) => {
    if (sortField !== field) {
      return <span className="text-gray-400">⇅</span>;
    }
    return sortDirection === 'asc' ? (
      <span className="text-blue-600">↑</span>
    ) : (
      <span className="text-blue-600">↓</span>
    );
  };

  const getScaleLabel = (scale: NodeScale | null): string => {
    if (!scale) return 'Unknown';
    const labels: Record<NodeScale, string> = {
      1: 'Structural',
      2: 'Built Environment',
      3: 'Institutional',
      4: 'Individual',
      5: 'Behaviors',
      6: 'Intermediate',
      7: 'Crisis',
    };
    return labels[scale];
  };

  const getScaleColor = (scale: NodeScale | null): string => {
    if (!scale) return 'bg-gray-100 text-gray-800';
    const colors: Record<NodeScale, string> = {
      1: 'bg-purple-100 text-purple-800', // Structural Determinants
      2: 'bg-emerald-100 text-emerald-800', // Built Environment
      3: 'bg-cyan-100 text-cyan-800', // Institutional
      4: 'bg-blue-100 text-blue-800', // Individual Conditions
      5: 'bg-rose-100 text-rose-800', // Individual Behaviors
      6: 'bg-orange-100 text-orange-800', // Intermediate Pathways
      7: 'bg-red-100 text-red-800', // Crisis Endpoints
    };
    return colors[scale];
  };

  // ==========================================
  // Render
  // ==========================================

  return (
    <div className="container mx-auto px-4 py-8">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">
          Important Nodes
        </h1>
        <p className="text-gray-600">
          Nodes ranked by composite importance score (connectivity, centrality, evidence quality)
        </p>
      </div>

      {/* Statistics Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
        <div className="bg-white rounded-lg shadow p-4">
          <div className="text-sm text-gray-600">Total Nodes</div>
          <div className="text-2xl font-bold text-gray-900">{stats.count}</div>
        </div>
        <div className="bg-white rounded-lg shadow p-4">
          <div className="text-sm text-gray-600">Avg Importance</div>
          <div className="text-2xl font-bold text-gray-900">
            {formatImportanceScore(stats.avgCompositeScore)}
          </div>
        </div>
        <div className="bg-white rounded-lg shadow p-4">
          <div className="text-sm text-gray-600">Avg Connections</div>
          <div className="text-2xl font-bold text-gray-900">
            {stats.avgConnections.toFixed(1)}
          </div>
        </div>
        <div className="bg-white rounded-lg shadow p-4">
          <div className="text-sm text-gray-600">Avg Evidence</div>
          <div className="text-2xl font-bold text-gray-900">
            {stats.avgEvidenceQuality.toFixed(2)}
          </div>
        </div>
      </div>

      {/* Controls */}
      <div className="bg-white rounded-lg shadow p-6 mb-6">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {/* Top N Slider */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Number of Nodes: {topN}
            </label>
            <input
              type="range"
              min="10"
              max="50"
              step="5"
              value={topN}
              onChange={(e) => setTopN(Number(e.target.value))}
              className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"
            />
            <div className="flex justify-between text-xs text-gray-500 mt-1">
              <span>10</span>
              <span>50</span>
            </div>
          </div>

          {/* Min Connections */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Min Connections: {filters.minConnections}
            </label>
            <input
              type="range"
              min="0"
              max="10"
              step="1"
              value={filters.minConnections}
              onChange={(e) =>
                setFilters(prev => ({ ...prev, minConnections: Number(e.target.value) }))
              }
              className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"
            />
            <div className="flex justify-between text-xs text-gray-500 mt-1">
              <span>0</span>
              <span>10+</span>
            </div>
          </div>

          {/* Actions */}
          <div className="flex items-end gap-2">
            <button
              onClick={() => refetch()}
              disabled={isLoading}
              className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-400 transition-colors"
            >
              {isLoading ? 'Loading...' : 'Refresh'}
            </button>
            <button
              onClick={handleExport}
              disabled={!nodes || nodes.length === 0}
              className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:bg-gray-400 transition-colors"
            >
              Export CSV
            </button>
          </div>

          {/* Clear Filters */}
          {(filters.scales.length > 0 || filters.minConnections > 0) && (
            <div className="flex items-end">
              <button
                onClick={handleClearFilters}
                className="px-4 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 transition-colors"
              >
                Clear Filters
              </button>
            </div>
          )}
        </div>

        {/* Scale Filters */}
        <div className="mt-4">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Filter by Scale
          </label>
          <div className="flex flex-wrap gap-2">
            {([1, 2, 3, 4, 5, 6, 7] as NodeScale[]).map(scale => (
              <button
                key={scale}
                onClick={() => handleScaleFilter(scale)}
                className={`px-3 py-1 rounded-full text-sm transition-colors ${
                  filters.scales.includes(scale)
                    ? 'bg-purple-600 text-white'
                    : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                }`}
              >
                {getScaleLabel(scale)}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Table */}
      <div className="bg-white rounded-lg shadow overflow-hidden">
        {isLoading && (
          <div className="p-12 text-center text-gray-500">
            <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mb-4"></div>
            <div>Loading important nodes...</div>
          </div>
        )}

        {error && (
          <div className="p-12 text-center text-red-600">
            <div className="text-lg font-semibold mb-2">Error loading nodes</div>
            <div className="text-sm">{error.message}</div>
            <button
              onClick={() => refetch()}
              className="mt-4 px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors"
            >
              Retry
            </button>
          </div>
        )}

        {!isLoading && !error && sortedNodes.length === 0 && (
          <div className="p-12 text-center text-gray-500">
            <div className="text-lg font-semibold mb-2">No nodes found</div>
            <div className="text-sm">Try adjusting your filters</div>
          </div>
        )}

        {!isLoading && !error && sortedNodes.length > 0 && (
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th
                    className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100"
                    onClick={() => handleSort('rank')}
                  >
                    Rank {renderSortIcon('rank')}
                  </th>
                  <th
                    className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100"
                    onClick={() => handleSort('label')}
                  >
                    Node {renderSortIcon('label')}
                  </th>
                  <th
                    className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100"
                    onClick={() => handleSort('category')}
                  >
                    Category {renderSortIcon('category')}
                  </th>
                  <th
                    className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100"
                    onClick={() => handleSort('scale')}
                  >
                    Scale {renderSortIcon('scale')}
                  </th>
                  <th
                    className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100"
                    onClick={() => handleSort('compositeScore')}
                  >
                    Importance {renderSortIcon('compositeScore')}
                  </th>
                  <th
                    className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100"
                    onClick={() => handleSort('totalConnections')}
                  >
                    Connections {renderSortIcon('totalConnections')}
                  </th>
                  <th
                    className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100"
                    onClick={() => handleSort('avgEvidenceQuality')}
                  >
                    Evidence {renderSortIcon('avgEvidenceQuality')}
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {sortedNodes.map(node => (
                  <tr
                    key={node.nodeId}
                    onClick={() => handleNodeClick(node)}
                    className={`cursor-pointer transition-colors ${
                      selectedNodeId === node.nodeId
                        ? 'bg-blue-50'
                        : 'hover:bg-gray-50'
                    }`}
                  >
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                      #{node.rank}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {node.label}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <CategoryBadge category={node.category} />
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className={`px-2 py-1 text-xs font-medium rounded-full ${getScaleColor(node.scale)}`}>
                        {getScaleLabel(node.scale)}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      <div className="flex items-center">
                        <div className="w-24 bg-gray-200 rounded-full h-2 mr-2">
                          <div
                            className="bg-blue-600 h-2 rounded-full"
                            style={{ width: `${node.compositeScore * 100}%` }}
                          ></div>
                        </div>
                        <span className="text-xs font-medium">
                          {formatImportanceScore(node.compositeScore)}
                        </span>
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {node.totalConnections}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {node.avgEvidenceQuality.toFixed(2)}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
};

export default ImportantNodesView;
