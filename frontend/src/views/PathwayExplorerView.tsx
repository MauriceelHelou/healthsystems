import React, { useState, useMemo } from 'react';
import { usePathways, usePathwayDetail, PathwaySummary, PathwayDetail } from '../hooks/usePathways';
import { CategoryBadge } from '../components/domain/CategoryBadge';

export const PathwayExplorerView: React.FC = () => {
  // State
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState<string | undefined>();
  const [selectedTag, setSelectedTag] = useState<string | undefined>();
  const [minEvidence, setMinEvidence] = useState<'A' | 'B' | 'C' | undefined>();
  const [selectedPathwayId, setSelectedPathwayId] = useState<string | null>(null);

  // Queries
  const { data: pathways, isLoading, error } = usePathways({
    category: selectedCategory,
    tag: selectedTag,
    minEvidence,
  });

  const { data: selectedPathway, isLoading: loadingDetail } = usePathwayDetail(selectedPathwayId);

  // Filter pathways by search query (client-side)
  const filteredPathways = useMemo(() => {
    if (!pathways) return [];
    if (!searchQuery) return pathways;

    const query = searchQuery.toLowerCase();
    return pathways.filter(p =>
      p.title.toLowerCase().includes(query) ||
      p.description.toLowerCase().includes(query) ||
      p.tags.some(tag => tag.toLowerCase().includes(query))
    );
  }, [pathways, searchQuery]);

  // Handlers
  const handlePathwayClick = (pathwayId: string) => {
    setSelectedPathwayId(pathwayId);
  };

  const clearFilters = () => {
    setSelectedCategory(undefined);
    setSelectedTag(undefined);
    setMinEvidence(undefined);
    setSearchQuery('');
  };

  // Render
  return (
    <div className="container mx-auto px-4 py-8">
      {/* Header */}
      <div className="mb-6">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">
          Pathway Explorer
        </h1>
        <p className="text-gray-600">
          Browse curated causal pathways connecting interventions to outcomes
        </p>
      </div>

      {/* Search & Filters Bar */}
      <div className="bg-white rounded-lg shadow p-4 mb-6">
        <div className="flex flex-col md:flex-row gap-4">
          {/* Search Input */}
          <div className="flex-1">
            <input
              type="text"
              placeholder="Search pathways..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              aria-label="Search pathways"
            />
          </div>

          {/* Category Filter */}
          <select
            value={selectedCategory || ''}
            onChange={(e) => setSelectedCategory(e.target.value || undefined)}
            className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
            aria-label="Filter by category"
          >
            <option value="">All Categories</option>
            <option value="political">Political</option>
            <option value="economic">Economic</option>
            <option value="social_environment">Social Environment</option>
            <option value="healthcare_access">Healthcare Access</option>
            <option value="behavioral">Behavioral</option>
            <option value="biological">Biological</option>
          </select>

          {/* Evidence Filter */}
          <select
            value={minEvidence || ''}
            onChange={(e) => setMinEvidence(e.target.value as any || undefined)}
            className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
            aria-label="Filter by minimum evidence quality"
          >
            <option value="">Any Evidence</option>
            <option value="A">High Quality (A)</option>
            <option value="B">Medium Quality (B+)</option>
            <option value="C">Lower Quality (C+)</option>
          </select>
        </div>

        {/* Active Filters Display */}
        {(selectedCategory || selectedTag || minEvidence || searchQuery) && (
          <div className="flex gap-2 mt-3 items-center">
            <span className="text-sm text-gray-600">Active filters:</span>
            {selectedCategory && (
              <span className="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm inline-flex items-center gap-2">
                Category: {selectedCategory}
                <button
                  onClick={() => setSelectedCategory(undefined)}
                  className="hover:text-blue-900"
                  aria-label="Remove category filter"
                >
                  ✕
                </button>
              </span>
            )}
            {minEvidence && (
              <span className="px-3 py-1 bg-green-100 text-green-800 rounded-full text-sm inline-flex items-center gap-2">
                Evidence: {minEvidence}+
                <button
                  onClick={() => setMinEvidence(undefined)}
                  className="hover:text-green-900"
                  aria-label="Remove evidence filter"
                >
                  ✕
                </button>
              </span>
            )}
            {searchQuery && (
              <span className="px-3 py-1 bg-purple-100 text-purple-800 rounded-full text-sm inline-flex items-center gap-2">
                Search: "{searchQuery}"
                <button
                  onClick={() => setSearchQuery('')}
                  className="hover:text-purple-900"
                  aria-label="Clear search"
                >
                  ✕
                </button>
              </span>
            )}
            <button
              onClick={clearFilters}
              className="ml-2 text-sm text-gray-600 hover:text-gray-900 underline"
            >
              Clear all
            </button>
          </div>
        )}
      </div>

      {/* Main Content: Two Columns */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left: Pathway List */}
        <div className="lg:col-span-1">
          <div className="bg-white rounded-lg shadow">
            {/* Header */}
            <div className="p-4 border-b border-gray-200">
              <h2 className="text-lg font-semibold text-gray-900">
                Pathways ({filteredPathways.length})
              </h2>
            </div>

            {/* List */}
            <div className="divide-y divide-gray-200 max-h-[calc(100vh-350px)] overflow-y-auto">
              {isLoading && (
                <div className="p-8 text-center text-gray-600">
                  <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mb-2"></div>
                  <div>Loading pathways...</div>
                </div>
              )}

              {error && (
                <div className="p-4 bg-red-50 text-red-800">
                  Error loading pathways: {error.message}
                </div>
              )}

              {filteredPathways.map(pathway => (
                <PathwayListItem
                  key={pathway.pathwayId}
                  pathway={pathway}
                  isSelected={selectedPathwayId === pathway.pathwayId}
                  onClick={() => handlePathwayClick(pathway.pathwayId)}
                />
              ))}

              {!isLoading && filteredPathways.length === 0 && (
                <div className="p-8 text-center text-gray-600">
                  <div className="text-4xl mb-2">🔍</div>
                  <div className="font-medium mb-1">No pathways found</div>
                  <div className="text-sm">Try adjusting your filters</div>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Right: Pathway Details */}
        <div className="lg:col-span-2">
          {!selectedPathwayId && (
            <div className="bg-white rounded-lg shadow p-12 text-center">
              <div className="text-gray-400 text-6xl mb-4">🗺️</div>
              <h3 className="text-lg font-medium text-gray-900 mb-2">
                Select a pathway to view details
              </h3>
              <p className="text-gray-600">
                Click on a pathway from the list to see its mechanisms and evidence
              </p>
            </div>
          )}

          {selectedPathwayId && (
            <PathwayDetailPanel
              pathway={selectedPathway}
              isLoading={loadingDetail}
            />
          )}
        </div>
      </div>
    </div>
  );
};

// ==========================================
// Sub-Components
// ==========================================

interface PathwayListItemProps {
  pathway: PathwaySummary;
  isSelected: boolean;
  onClick: () => void;
}

const PathwayListItem: React.FC<PathwayListItemProps> = ({
  pathway,
  isSelected,
  onClick,
}) => {
  return (
    <div
      onClick={onClick}
      className={`p-4 cursor-pointer hover:bg-gray-50 transition-colors ${
        isSelected ? 'bg-blue-50 border-l-4 border-blue-600' : ''
      }`}
      role="button"
      tabIndex={0}
      onKeyDown={(e) => {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          onClick();
        }
      }}
    >
      {/* Title */}
      <div className="font-medium text-gray-900 mb-1">
        {pathway.title}
      </div>

      {/* From → To */}
      <div className="text-sm text-gray-600 mb-2">
        {pathway.fromNodeLabel} → {pathway.toNodeLabel}
      </div>

      {/* Badges */}
      <div className="flex items-center gap-2 flex-wrap">
        <CategoryBadge category={pathway.category as any} size="sm" />
        <span className="text-xs px-2 py-1 bg-gray-100 text-gray-700 rounded">
          {pathway.pathLength} steps
        </span>
        <span
          className={`text-xs px-2 py-1 rounded font-bold ${
            pathway.avgEvidenceQuality >= 2.5
              ? 'bg-green-100 text-green-800'
              : pathway.avgEvidenceQuality >= 1.5
              ? 'bg-yellow-100 text-yellow-800'
              : 'bg-red-100 text-red-800'
          }`}
        >
          Evidence: {pathway.avgEvidenceQuality.toFixed(1)}
        </span>
      </div>

      {/* Tags */}
      {pathway.tags.length > 0 && (
        <div className="flex gap-1 mt-2 flex-wrap">
          {pathway.tags.slice(0, 3).map(tag => (
            <span
              key={tag}
              className="text-xs px-2 py-1 bg-blue-50 text-blue-700 rounded"
            >
              {tag}
            </span>
          ))}
          {pathway.tags.length > 3 && (
            <span className="text-xs px-2 py-1 text-gray-500">
              +{pathway.tags.length - 3} more
            </span>
          )}
        </div>
      )}
    </div>
  );
};

interface PathwayDetailPanelProps {
  pathway?: PathwayDetail;
  isLoading: boolean;
}

const PathwayDetailPanel: React.FC<PathwayDetailPanelProps> = ({
  pathway,
  isLoading,
}) => {
  if (isLoading) {
    return (
      <div className="bg-white rounded-lg shadow p-8 text-center">
        <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
        <div className="mt-2 text-gray-600">Loading pathway details...</div>
      </div>
    );
  }

  if (!pathway) return null;

  return (
    <div className="bg-white rounded-lg shadow">
      {/* Header */}
      <div className="p-6 border-b border-gray-200">
        <h2 className="text-2xl font-bold text-gray-900 mb-2">
          {pathway.title}
        </h2>
        <p className="text-gray-600">{pathway.description}</p>
      </div>

      {/* Metrics */}
      <div className="grid grid-cols-4 gap-4 p-6 bg-gray-50 border-b border-gray-200">
        <div>
          <div className="text-xs text-gray-600 uppercase mb-1">Length</div>
          <div className="text-2xl font-bold text-gray-900">
            {pathway.pathLength}
          </div>
          <div className="text-xs text-gray-500">steps</div>
        </div>
        <div>
          <div className="text-xs text-gray-600 uppercase mb-1">Evidence</div>
          <div className={`text-2xl font-bold ${
            pathway.evidenceGrade === 'A' ? 'text-green-600' :
            pathway.evidenceGrade === 'B' ? 'text-yellow-600' :
            'text-red-600'
          }`}>
            {pathway.evidenceGrade}
          </div>
          <div className="text-xs text-gray-500">grade</div>
        </div>
        <div>
          <div className="text-xs text-gray-600 uppercase mb-1">Direction</div>
          <div className={`text-2xl font-bold ${
            pathway.overallDirection === 'positive' ? 'text-green-600' :
            pathway.overallDirection === 'negative' ? 'text-red-600' :
            'text-gray-600'
          }`}>
            {pathway.overallDirection === 'positive' ? '↑' :
             pathway.overallDirection === 'negative' ? '↓' : '~'}
          </div>
          <div className="text-xs text-gray-500 capitalize">{pathway.overallDirection}</div>
        </div>
        <div>
          <div className="text-xs text-gray-600 uppercase mb-1">Avg Quality</div>
          <div className="text-2xl font-bold text-gray-900">
            {pathway.avgEvidenceQuality.toFixed(1)}
          </div>
          <div className="text-xs text-gray-500">out of 3.0</div>
        </div>
      </div>

      {/* Mechanisms List */}
      <div className="p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">
          Causal Mechanisms
        </h3>
        <div className="space-y-3">
          {pathway.mechanisms.map((mech, index) => (
            <div
              key={mech.mechanismId}
              className="border-l-4 border-blue-500 pl-4 py-2 hover:bg-gray-50 transition-colors"
            >
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <div className="flex items-start gap-2">
                    <span className="inline-flex items-center justify-center w-6 h-6 rounded-full bg-blue-100 text-blue-800 text-xs font-bold flex-shrink-0">
                      {index + 1}
                    </span>
                    <div>
                      <div className="font-medium text-sm text-gray-900">
                        {mech.name}
                      </div>
                      <div className="text-xs text-gray-600 mt-1">
                        {mech.fromNode} → {mech.toNode}
                      </div>
                    </div>
                  </div>
                </div>
                <div className="flex items-center gap-2 ml-4">
                  <span className={`px-2 py-1 text-xs font-medium rounded ${
                    mech.direction === 'positive'
                      ? 'bg-green-100 text-green-800'
                      : mech.direction === 'negative'
                      ? 'bg-red-100 text-red-800'
                      : 'bg-gray-100 text-gray-800'
                  }`}>
                    {mech.direction === 'positive' ? '↑ Positive' :
                     mech.direction === 'negative' ? '↓ Negative' : 'Unknown'}
                  </span>
                  <span className={`px-2 py-1 text-xs font-bold rounded ${
                    mech.evidenceQuality === 'A' ? 'bg-green-600 text-white' :
                    mech.evidenceQuality === 'B' ? 'bg-yellow-600 text-white' :
                    'bg-red-600 text-white'
                  }`}>
                    {mech.evidenceQuality}
                  </span>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Tags Section */}
      {pathway.tags.length > 0 && (
        <div className="p-6 border-t border-gray-200">
          <h3 className="text-sm font-semibold text-gray-900 mb-2">Tags</h3>
          <div className="flex gap-2 flex-wrap">
            {pathway.tags.map(tag => (
              <span
                key={tag}
                className="px-3 py-1 bg-blue-50 text-blue-700 rounded-full text-sm"
              >
                {tag}
              </span>
            ))}
          </div>
        </div>
      )}

      {/* Metadata */}
      {(pathway.curatedBy || pathway.dateCreated) && (
        <div className="p-6 bg-gray-50 border-t border-gray-200 text-sm text-gray-600">
          {pathway.curatedBy && (
            <div>Curated by: {pathway.curatedBy}</div>
          )}
          {pathway.dateCreated && (
            <div>Created: {new Date(pathway.dateCreated).toLocaleDateString()}</div>
          )}
        </div>
      )}
    </div>
  );
};

export default PathwayExplorerView;
