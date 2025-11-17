import React, { useState, useRef } from 'react'
import { Panel } from '../layouts/Panel'
import MechanismGraph from '../visualizations/MechanismGraph'
import { mockNodes, mockEdges, generateMockMechanism } from '../data/mockData'
import type { MechanismNode, MechanismEdge } from '../types'
import { Button } from '../components/base/Button'
import { Icon } from '../components/base/Icon'
import { Input } from '../components/base/Input'
import { CategoryBadge } from '../components/domain/CategoryBadge'
import { EvidenceBadge } from '../components/domain/EvidenceBadge'
import { Badge } from '../components/base/Badge'

export const SystemsMapView: React.FC = () => {
  const [selectedNode, setSelectedNode] = useState<MechanismNode | null>(null)
  const [selectedEdge, setSelectedEdge] = useState<MechanismEdge | null>(null)
  const [showPanel, setShowPanel] = useState(false)
  const [searchQuery, setSearchQuery] = useState('')
  const [filteredCategories, setFilteredCategories] = useState<string[]>([])
  const containerRef = useRef<HTMLDivElement>(null)

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

  return (
    <div className="flex flex-1 overflow-hidden">
      {/* Main Canvas */}
      <div ref={containerRef} className="flex-1 relative bg-white">
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

        {/* Legend */}
        <div className="absolute bottom-4 left-4 z-10 bg-white/95 backdrop-blur rounded-lg shadow-lg p-4 max-w-sm">
          <div className="flex items-center justify-between mb-3">
            <h3 className="font-semibold text-sm text-gray-900">Legend</h3>
            <Button variant="icon" size="sm" ariaLabel="Hide legend">
              <Icon name="chevron-down" size="sm" />
            </Button>
          </div>

          <div className="space-y-3">
            {/* Categories */}
            <div>
              <p className="text-xs font-medium text-gray-700 mb-2">Categories</p>
              <div className="flex flex-wrap gap-2">
                <CategoryBadge category="built_environment" size="sm" />
                <CategoryBadge category="social_environment" size="sm" />
                <CategoryBadge category="economic" size="sm" />
                <CategoryBadge category="political" size="sm" />
                <CategoryBadge category="biological" size="sm" />
              </div>
            </div>

            {/* Evidence Quality */}
            <div>
              <p className="text-xs font-medium text-gray-700 mb-2">Evidence Quality</p>
              <div className="flex gap-3">
                <EvidenceBadge quality="A" size="sm" showLabel />
                <EvidenceBadge quality="B" size="sm" showLabel />
                <EvidenceBadge quality="C" size="sm" showLabel />
              </div>
            </div>

            {/* Node Types */}
            <div>
              <p className="text-xs font-medium text-gray-700 mb-2">Stock Types</p>
              <div className="flex gap-2 text-xs">
                <span className="flex items-center gap-1">
                  <span className="w-3 h-3 bg-blue-500 rounded-full" />
                  Structural
                </span>
                <span className="flex items-center gap-1">
                  <span className="w-3 h-3 bg-purple-500 rounded-full" />
                  Proxy
                </span>
                <span className="flex items-center gap-1">
                  <span className="w-3 h-3 bg-red-500 rounded-full" />
                  Crisis
                </span>
              </div>
            </div>
          </div>
        </div>

        {/* Graph Visualization */}
        <div className="w-full h-full">
          <MechanismGraph
            data={{ nodes: mockNodes, edges: mockEdges }}
            width={width}
            height={height}
            onNodeClick={handleNodeClick}
            onEdgeClick={handleEdgeClick}
            selectedNodeId={selectedNode?.id || null}
            filteredCategories={filteredCategories}
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
          footer={
            <div className="flex gap-2 justify-end">
              <Button variant="secondary" size="sm">
                Export Details
              </Button>
              <Button variant="primary" size="sm">
                View Pathways →
              </Button>
            </div>
          }
        >
          <NodeDetailPanel node={selectedNode} edges={mockEdges} />
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
          <MechanismDetailPanel edge={selectedEdge} nodes={mockNodes} />
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
      <div className="flex items-center gap-3 pb-4 border-b">
        <CategoryBadge category={node.category} />
        <Badge color="gray" size="sm">
          {node.stockType}
        </Badge>
      </div>

      {/* Overview */}
      <div>
        <h3 className="text-sm font-semibold text-gray-900 mb-2">Overview</h3>
        <div className="space-y-2 text-sm text-gray-700">
          <p>
            <span className="font-medium">Stock Type:</span> {node.stockType}
          </p>
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
  const mechanism = generateMockMechanism(edge, nodes)
  const sourceNode = nodes.find((n) => n.id === edge.source)
  const targetNode = nodes.find((n) => n.id === edge.target)

  return (
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
          {edge.studyCount} studies
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

      {/* Evidence Summary */}
      <div>
        <h3 className="text-sm font-semibold text-gray-900 mb-2">Evidence Summary</h3>
        <div className="space-y-2 text-sm text-gray-700">
          <p>
            <span className="font-medium">Quality Rating:</span>{' '}
            {edge.evidenceQuality || 'Unknown'}
          </p>
          <p>
            <span className="font-medium">Based on:</span> {edge.studyCount} studies
          </p>
        </div>
      </div>

      {/* Citations */}
      {mechanism.citations.length > 0 && (
        <div>
          <h3 className="text-sm font-semibold text-gray-900 mb-3">
            Supporting Literature ({mechanism.citations.length})
          </h3>
          <div className="space-y-2">
            {mechanism.citations.slice(0, 3).map((citation) => (
              <div
                key={citation.id}
                className="p-3 border border-gray-200 rounded text-xs space-y-1"
              >
                <p className="font-medium text-gray-900">
                  {citation.authors} ({citation.year})
                </p>
                <p className="text-gray-600">{citation.journal}</p>
                <p className="text-gray-700 line-clamp-2">{citation.title}</p>
                {citation.url && (
                  <a
                    href={citation.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-primary-600 hover:text-primary-700 inline-flex items-center gap-1"
                  >
                    View Citation
                    <Icon name="arrow-right" size="xs" />
                  </a>
                )}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}
