import { FC, useState, useRef, useMemo } from 'react'
import { Panel } from '../layouts/Panel'
import MechanismGraph from '../visualizations/MechanismGraph'
import type { MechanismNode, MechanismEdge, GraphLayoutMode, PhysicsSettings } from '../types'
import { Button } from '../components/base/Button'
import { Icon } from '../components/base/Icon'
import { CategoryBadge } from '../components/domain/CategoryBadge'
import { EvidenceBadge } from '../components/domain/EvidenceBadge'
import { EvidenceModal } from '../components/domain/EvidenceModal'
import { Badge } from '../components/base/Badge'
// import { Legend } from '../components/visualization/Legend'  // Commented out - legend is hidden
import { useGraphDataWithCanonicalNodes, useMechanismById } from '../hooks/useData'
import { filterByMinConnections } from '../utils/graphBuilder'

export const SystemsMapView: FC = () => {
  const [selectedNode, setSelectedNode] = useState<MechanismNode | null>(null)
  const [selectedEdge, setSelectedEdge] = useState<MechanismEdge | null>(null)
  const [showPanel, setShowPanel] = useState(false)
  const containerRef = useRef<HTMLDivElement>(null)

  // Layout mode state
  const [layoutMode, setLayoutMode] = useState<GraphLayoutMode>('hierarchical')

  // Physics settings for force-directed mode
  const [physicsSettings, setPhysicsSettings] = useState<PhysicsSettings>({
    charge: -300,
    linkDistance: 150,
    gravity: 0.05,
    collision: 20,
  })

  // Fetch graph data from API using canonical nodes
  const { data: rawGraphData, isLoading, error } = useGraphDataWithCanonicalNodes()

  // Filter out nodes with 1 or fewer connections (minConnections = 2)
  const graphData = useMemo(() => {
    if (!rawGraphData) return null
    return filterByMinConnections(rawGraphData, 2)
  }, [rawGraphData])

  const handleNodeClick = (node: MechanismNode) => {
    setSelectedNode(node)
    setSelectedEdge(null)
    setShowPanel(true)
  }

  const handleEdgeClick = (edge: MechanismEdge) => {
    setSelectedEdge(edge)
    setSelectedNode(null)
    setShowPanel(true)
  }

  const handleClosePanel = () => {
    setShowPanel(false)
    setSelectedNode(null)
    setSelectedEdge(null)
  }

  // Get container dimensions
  const width = containerRef.current?.clientWidth || 1200
  const height = containerRef.current?.clientHeight || 800

  // Handle loading and error states
  if (isLoading) {
    return (
      <div className="flex-1 flex items-center justify-center">
        <div className="text-center">
          <Icon name="refresh" size="lg" className="animate-spin text-primary-600 mx-auto mb-4" />
          <p className="text-gray-600">Loading mechanisms and nodes...</p>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="flex-1 flex items-center justify-center">
        <div className="text-center max-w-md">
          <Icon name="alert-circle" size="lg" className="text-error-600 mx-auto mb-4" />
          <p className="text-gray-900 font-semibold mb-2">Failed to load data</p>
          <p className="text-gray-600 text-sm">
            {error instanceof Error ? error.message : 'An error occurred while loading the graph data.'}
          </p>
        </div>
      </div>
    )
  }

  if (!graphData || graphData.nodes.length === 0) {
    return (
      <div className="flex-1 flex items-center justify-center">
        <div className="text-center">
          <Icon name="info" size="lg" className="text-gray-400 mx-auto mb-4" />
          <p className="text-gray-600">No mechanisms or nodes available.</p>
        </div>
      </div>
    )
  }

  return (
    <div className="flex flex-1 overflow-hidden">
      {/* Main Canvas */}
      <div ref={containerRef} className="flex-1 relative bg-white">
        {/* Visually hidden H1 for accessibility */}
        <h1 className="sr-only">Health Systems Causal Network Map</h1>

        {/* Layout Toggle - Top Left */}
        <div className="absolute top-4 left-4 z-10 bg-white rounded-lg shadow-md p-3">
          <div className="space-y-3">
            <div className="flex items-center gap-3">
              <label className="text-xs font-semibold text-gray-700 uppercase tracking-wide">
                Layout
              </label>
              <div className="flex bg-gray-100 rounded-lg p-0.5">
                <button
                  onClick={() => setLayoutMode('hierarchical')}
                  className={`px-3 py-1.5 text-xs font-medium rounded-md transition-colors ${
                    layoutMode === 'hierarchical'
                      ? 'bg-white text-gray-900 shadow-sm'
                      : 'text-gray-600 hover:text-gray-900'
                  }`}
                >
                  Hierarchical
                </button>
                <button
                  onClick={() => setLayoutMode('force-directed')}
                  className={`px-3 py-1.5 text-xs font-medium rounded-md transition-colors ${
                    layoutMode === 'force-directed'
                      ? 'bg-white text-gray-900 shadow-sm'
                      : 'text-gray-600 hover:text-gray-900'
                  }`}
                >
                  Force-Directed
                </button>
              </div>
            </div>

            {/* Physics Settings (collapsible) */}
            {layoutMode === 'force-directed' && (
              <details className="border-t pt-3">
                <summary className="cursor-pointer text-xs font-semibold text-gray-700 uppercase tracking-wide mb-2 hover:text-gray-900">
                  Physics Settings
                </summary>
                <div className="space-y-2.5 pl-1 mt-2">
                  <div>
                    <div className="flex justify-between items-center mb-1">
                      <label className="text-xs text-gray-600 font-medium">Repulsion</label>
                      <span className="text-xs text-gray-500">{physicsSettings.charge}</span>
                    </div>
                    <input
                      type="range"
                      min="-1000"
                      max="-50"
                      step="50"
                      value={physicsSettings.charge}
                      onChange={(e) =>
                        setPhysicsSettings({ ...physicsSettings, charge: Number(e.target.value) })
                      }
                      className="w-full h-1.5 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-blue-600"
                    />
                  </div>

                  <div>
                    <div className="flex justify-between items-center mb-1">
                      <label className="text-xs text-gray-600 font-medium">Link Distance</label>
                      <span className="text-xs text-gray-500">{physicsSettings.linkDistance}</span>
                    </div>
                    <input
                      type="range"
                      min="50"
                      max="300"
                      step="10"
                      value={physicsSettings.linkDistance}
                      onChange={(e) =>
                        setPhysicsSettings({
                          ...physicsSettings,
                          linkDistance: Number(e.target.value),
                        })
                      }
                      className="w-full h-1.5 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-blue-600"
                    />
                  </div>

                  <div>
                    <div className="flex justify-between items-center mb-1">
                      <label className="text-xs text-gray-600 font-medium">Gravity</label>
                      <span className="text-xs text-gray-500">{physicsSettings.gravity.toFixed(2)}</span>
                    </div>
                    <input
                      type="range"
                      min="0"
                      max="0.2"
                      step="0.01"
                      value={physicsSettings.gravity}
                      onChange={(e) =>
                        setPhysicsSettings({ ...physicsSettings, gravity: Number(e.target.value) })
                      }
                      className="w-full h-1.5 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-blue-600"
                    />
                  </div>

                  <div>
                    <div className="flex justify-between items-center mb-1">
                      <label className="text-xs text-gray-600 font-medium">Collision Buffer</label>
                      <span className="text-xs text-gray-500">{physicsSettings.collision}</span>
                    </div>
                    <input
                      type="range"
                      min="0"
                      max="50"
                      step="5"
                      value={physicsSettings.collision}
                      onChange={(e) =>
                        setPhysicsSettings({ ...physicsSettings, collision: Number(e.target.value) })
                      }
                      className="w-full h-1.5 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-blue-600"
                    />
                  </div>
                </div>
              </details>
            )}
          </div>
        </div>

        {/* Graph Controls */}
        <div className="absolute top-4 right-4 z-10 flex gap-2 bg-white rounded-lg shadow-md p-2">
          <Button
            variant="icon"
            size="sm"
            ariaLabel="Search nodes"
            onClick={() => {}}
          >
            <Icon name="search" size="md" />
          </Button>
          <Button variant="icon" size="sm" ariaLabel="Filter">
            <Icon name="filter" size="md" />
          </Button>
          <div className="w-px bg-gray-200" />
          <Button variant="icon" size="sm" ariaLabel="Zoom in">
            <Icon name="zoom-in" size="md" />
          </Button>
          <Button variant="icon" size="sm" ariaLabel="Zoom out">
            <Icon name="zoom-out" size="md" />
          </Button>
          <Button variant="icon" size="sm" ariaLabel="Fit to screen">
            <Icon name="expand" size="md" />
          </Button>
          <Button variant="icon" size="sm" ariaLabel="Reset view">
            <Icon name="refresh" size="md" />
          </Button>
        </div>

        {/* Legend - Commented out for testing */}
        {/* <div className="absolute bottom-4 left-4 z-10 max-w-xs">
          <Legend showEvidenceQuality showScales />
        </div> */}

        {/* Graph Visualization */}
        <div className="w-full h-full">
          <MechanismGraph
            data={graphData}
            width={width}
            height={height}
            onNodeClick={handleNodeClick}
            onEdgeClick={handleEdgeClick}
            selectedNodeId={selectedNode?.id || null}
            filteredCategories={[]}
            layoutMode={layoutMode}
            physicsSettings={layoutMode === 'force-directed' ? physicsSettings : undefined}
          />
        </div>
      </div>

      {/* Detail Panel */}
      {showPanel && selectedNode && (
        <Panel
          title={selectedNode.label}
          icon={<Icon name="arrow-right" size="md" className="text-primary-600" />}
          onClose={handleClosePanel}
          resizable
          collapsible
        >
          <NodeDetailPanel node={selectedNode} edges={graphData.edges} />
        </Panel>
      )}

      {showPanel && selectedEdge && (
        <Panel
          title="Mechanism Detail"
          icon={<Icon name="arrow-right" size="md" className="text-primary-600" />}
          onClose={handleClosePanel}
          resizable
          collapsible
        >
          <MechanismDetailPanel edge={selectedEdge} nodes={graphData.nodes} />
        </Panel>
      )}
    </div>
  )
}

// Node Detail Panel Component
const NodeDetailPanel: React.FC<{ node: MechanismNode; edges: MechanismEdge[] }> = ({
  node,
  edges,
}) => {
  const outgoingEdges = edges.filter((e) => e.source === node.id)
  const incomingEdges = edges.filter((e) => e.target === node.id)

  return (
    <div className="space-y-6">
      {/* Quick Stats */}
      <div className="flex items-center gap-3 pb-4 border-b flex-wrap">
        <CategoryBadge category={node.category} />
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
            <span className="font-medium">Connections:</span> {node.connections.outgoing} outgoing, {node.connections.incoming} incoming
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
                  className="flex items-start gap-2 p-2 rounded border border-gray-200 hover:border-primary-300 transition-colors cursor-pointer"
                >
                  <Icon name="arrow-right" size="sm" className="text-green-600 mt-0.5" />
                  <div className="flex-1 min-w-0">
                    <p className="text-xs font-medium text-gray-900 truncate">
                      → Target Node
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
                  className="flex items-start gap-2 p-2 rounded border border-gray-200 hover:border-primary-300 transition-colors cursor-pointer"
                >
                  <Icon name="arrow-left" size="sm" className="text-blue-600 mt-0.5" />
                  <div className="flex-1 min-w-0">
                    <p className="text-xs font-medium text-gray-900 truncate">
                      ← Source Node
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
  )
}

// Mechanism Detail Panel Component
const MechanismDetailPanel: React.FC<{ edge: MechanismEdge; nodes: MechanismNode[] }> = ({
  edge,
  nodes,
}) => {
  const [showEvidenceModal, setShowEvidenceModal] = useState(false)

  // Fetch detailed mechanism data from API
  const { data: mechanism, isLoading } = useMechanismById(edge.id)
  const sourceNode = nodes.find((n) => n.id === edge.source)
  const targetNode = nodes.find((n) => n.id === edge.target)

  if (isLoading) {
    return (
      <div className="flex items-center justify-center py-8">
        <Icon name="refresh" size="md" className="animate-spin text-primary-600" />
      </div>
    )
  }

  if (!mechanism) {
    return (
      <div className="text-center py-8 text-gray-600">
        <p>Unable to load mechanism details.</p>
      </div>
    )
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
          <p className="text-gray-600 mb-1">From → To</p>
          <p className="font-medium text-gray-900">
            {sourceNode?.label} → {targetNode?.label}
          </p>
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
  )
}
