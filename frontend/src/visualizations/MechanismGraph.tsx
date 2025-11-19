/**
 * Interactive force-directed graph visualization for causal mechanisms.
 * Uses D3.js for accessible, interactive network diagrams.
 * Enhanced with design system colors, states, and interactions.
 */

import React, { useEffect, useRef } from 'react';
import * as d3 from 'd3';
import { SystemsNetwork, MechanismNode, MechanismEdge } from '../types/mechanism';
import { colors, getCategoryBorder } from '../utils/colors';

interface MechanismGraphProps {
  data: SystemsNetwork;
  width?: number;
  height?: number;
  onNodeClick?: (node: MechanismNode) => void;
  onEdgeClick?: (edge: MechanismEdge) => void;
  selectedNodeId?: string | null;
  filteredCategories?: string[];
}

const MechanismGraph: React.FC<MechanismGraphProps> = ({
  data,
  width = 800,
  height = 600,
  onNodeClick,
}) => {
  const svgRef = useRef<SVGSVGElement>(null);

  useEffect(() => {
    if (!svgRef.current || !data.nodes.length) return;

    // Clear previous visualization
    d3.select(svgRef.current).selectAll('*').remove();

    // Create SVG
    const svg = d3
      .select(svgRef.current)
      .attr('width', width)
      .attr('height', height)
      .attr('role', 'img')
      .attr('aria-label', 'Causal mechanism network diagram');

    // Add description for screen readers
    svg
      .append('desc')
      .text(
        `Interactive network diagram showing ${data.nodes.length} causal mechanisms ` +
        `and ${data.edges.length} relationships between them. ` +
        `Use arrow keys to navigate between nodes.`
      );

    // Create force simulation
    const simulation = d3
      .forceSimulation(data.nodes as any)
      .force(
        'link',
        d3
          .forceLink(data.edges)
          .id((d: any) => d.id)
          .distance(100)
      )
      .force('charge', d3.forceManyBody().strength(-300))
      .force('center', d3.forceCenter(width / 2, height / 2))
      .force('collision', d3.forceCollide().radius(50));

    // Create links (gray edges)
    const link = svg
      .append('g')
      .attr('class', 'links')
      .selectAll('line')
      .data(data.edges)
      .enter()
      .append('line')
      .attr('stroke', colors.edgeDefault)
      .attr('stroke-opacity', 0.4)
      .attr('stroke-width', 1);

    // Create nodes
    const node = svg
      .append('g')
      .attr('class', 'nodes')
      .selectAll('g')
      .data(data.nodes)
      .enter()
      .append('g')
      .attr('role', 'button')
      .attr('tabindex', 0)
      .attr('aria-label', (d) => `Mechanism: ${d.label}, Weight: ${d.weight.toFixed(2)}`)
      .call(
        d3
          .drag<SVGGElement, MechanismNode>()
          .on('start', dragStarted)
          .on('drag', dragged)
          .on('end', dragEnded) as any
      );

    // Add rectangles to nodes (white with gray border)
    const nodeWidth = 80;
    const nodeHeight = 40;

    node
      .append('rect')
      .attr('width', nodeWidth)
      .attr('height', nodeHeight)
      .attr('x', -nodeWidth / 2)
      .attr('y', -nodeHeight / 2)
      .attr('rx', 4) // Rounded corners
      .attr('fill', colors.nodeDefault)
      .attr('stroke', (d) => getCategoryBorder(d.category))
      .attr('stroke-width', 1)
      .style('filter', 'drop-shadow(0 1px 2px rgba(0, 0, 0, 0.05))');

    // Add labels (compact, centered text)
    node
      .append('text')
      .text((d) => {
        // Truncate long labels
        const maxLength = 12;
        return d.label.length > maxLength
          ? d.label.substring(0, maxLength) + '...'
          : d.label;
      })
      .attr('x', 0)
      .attr('y', 4)
      .attr('text-anchor', 'middle')
      .attr('font-size', '11px')
      .attr('font-weight', '500')
      .attr('fill', colors.textPrimary)
      .attr('pointer-events', 'none');

    // Add hover states (orange accent)
    node
      .on('mouseenter', function () {
        d3.select(this)
          .select('rect')
          .attr('fill', colors.nodeHover)
          .attr('stroke', colors.orange)
          .attr('stroke-width', 2);
      })
      .on('mouseleave', function () {
        d3.select(this)
          .select('rect')
          .attr('fill', colors.nodeDefault)
          .attr('stroke', colors.nodeBorder)
          .attr('stroke-width', 1);
      });

    // Add click handler
    node.on('click', (_event, d) => {
      if (onNodeClick) {
        onNodeClick(d);
      }
    });

    // Add keyboard navigation
    node.on('keydown', (event, d) => {
      if (event.key === 'Enter' || event.key === ' ') {
        event.preventDefault();
        if (onNodeClick) {
          onNodeClick(d);
        }
      }
    });

    // Update positions on each tick
    simulation.on('tick', () => {
      link
        .attr('x1', (d: any) => d.source.x)
        .attr('y1', (d: any) => d.source.y)
        .attr('x2', (d: any) => d.target.x)
        .attr('y2', (d: any) => d.target.y);

      node.attr('transform', (d: any) => `translate(${d.x},${d.y})`);
    });

    // Drag functions
    function dragStarted(event: any) {
      if (!event.active) simulation.alphaTarget(0.3).restart();
      event.subject.fx = event.subject.x;
      event.subject.fy = event.subject.y;
    }

    function dragged(event: any) {
      event.subject.fx = event.x;
      event.subject.fy = event.y;
    }

    function dragEnded(event: any) {
      if (!event.active) simulation.alphaTarget(0);
      event.subject.fx = null;
      event.subject.fy = null;
    }

    // Cleanup
    return () => {
      simulation.stop();
    };
  }, [data, width, height, onNodeClick]);

  return (
    <svg
      ref={svgRef}
      className="border border-gray-300 rounded-lg"
      style={{ maxWidth: '100%', height: 'auto' }}
    />
  );
};

export default MechanismGraph;
