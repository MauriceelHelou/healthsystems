"""
API routes for node analysis (importance and pathfinding).

Provides endpoints for:
- Node importance ranking based on centrality measures and evidence quality
- Pathfinding between nodes using multiple algorithms
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Set, Tuple, Literal
from pydantic import BaseModel, Field
from enum import Enum
import networkx as nx
from collections import defaultdict, deque

from models import Mechanism, Node, get_db


router = APIRouter(prefix="/api/nodes", tags=["nodes"])


# ==========================================
# Pydantic Schemas
# ==========================================

class NodeImportance(BaseModel):
    """Response schema for node importance ranking"""
    nodeId: str = Field(..., description="Node identifier")
    label: str = Field(..., description="Human-readable node name")
    category: str = Field(..., description="Node category")
    scale: Optional[int] = Field(None, ge=1, le=7, description="Node scale (1-7): 1=Structural, 2=Built Env, 3=Institutional, 4=Individual, 5=Behaviors, 6=Pathways, 7=Crisis")

    # Centrality measures
    degreeScore: float = Field(..., description="Normalized degree centrality (0-1)")
    betweennessScore: float = Field(..., description="Normalized betweenness centrality (0-1)")
    closenessCentrality: float = Field(..., description="Closeness centrality (0-1)")
    pageRank: float = Field(..., description="PageRank score (0-1)")

    # Evidence-based scoring
    evidenceScore: float = Field(..., description="Average evidence quality score (0-1)")

    # Composite
    compositeScore: float = Field(..., description="Composite importance score (0-1)")
    rank: int = Field(..., description="Rank by composite score (1 = most important)")

    # Metadata
    totalConnections: int = Field(..., description="Total incoming + outgoing connections")
    avgEvidenceQuality: float = Field(..., description="Average evidence quality (0-3)")

    class Config:
        from_attributes = True


class PathNode(BaseModel):
    """Node information in a path"""
    nodeId: str
    label: str
    category: str
    scale: Optional[int] = None


class PathMechanism(BaseModel):
    """Mechanism information in a path"""
    mechanismId: str
    name: str
    fromNode: str
    toNode: str
    direction: str
    evidenceQuality: Optional[str]
    category: str


class PathResult(BaseModel):
    """Result for a single path between two nodes"""
    pathId: str = Field(..., description="Unique path identifier")
    nodes: List[str] = Field(..., description="List of node IDs in path order")
    nodeDetails: List[PathNode] = Field(..., description="Detailed node information")
    edges: List[str] = Field(..., description="List of mechanism IDs connecting nodes")
    mechanismDetails: List[PathMechanism] = Field(..., description="Detailed mechanism information")

    # Metrics
    pathLength: int = Field(..., description="Number of hops (edges) in path")
    avgEvidenceQuality: float = Field(..., description="Average evidence quality score (0-3)")
    evidenceGrade: str = Field(..., description="Overall evidence grade (A/B/C)")
    overallDirection: str = Field(..., description="Net direction (positive/negative/mixed)")
    totalWeight: float = Field(..., description="Total path weight")


class PathfindingRequest(BaseModel):
    """Request schema for pathfinding"""
    from_node: str = Field(..., description="Starting node ID")
    to_node: str = Field(..., description="Target node ID")
    algorithm: str = Field('shortest', description="Algorithm: shortest, strongest_evidence, or all_simple")
    max_depth: int = Field(5, ge=1, le=8, description="Maximum path length")
    max_paths: int = Field(10, ge=1, le=50, description="Maximum paths to return (for all_simple)")
    exclude_categories: Optional[List[str]] = Field(None, description="Categories to exclude")
    only_categories: Optional[List[str]] = Field(None, description="Only include these categories")


class PathfindingResponse(BaseModel):
    """Response schema for pathfinding"""
    fromNode: str
    toNode: str
    algorithm: str
    pathsFound: int
    paths: List[PathResult]


class CrisisEndpoint(BaseModel):
    """Response schema for crisis endpoint nodes"""
    nodeId: str = Field(..., description="Node identifier")
    label: str = Field(..., description="Human-readable node name")
    category: str = Field(..., description="Node category")
    scale: int = Field(7, description="Node scale (always 7 for crisis endpoints)")
    description: Optional[str] = Field(None, description="Node description")

    class Config:
        from_attributes = True


class CrisisSubgraphRequest(BaseModel):
    """Request schema for crisis subgraph analysis"""
    crisisNodeIds: List[str] = Field(..., min_length=1, max_length=10, description="List of crisis endpoint node IDs (1-10 nodes)")
    maxDegrees: int = Field(5, ge=1, le=8, description="Maximum degrees of separation from crisis endpoints")
    minStrength: int = Field(2, ge=1, le=3, description="Minimum evidence strength (1=C, 2=B, 3=A)")
    includeCategories: Optional[List[str]] = Field(None, description="Optional: Only include these categories")


class CrisisNodeWithDegree(BaseModel):
    """Node with degree-from-crisis metadata"""
    nodeId: str
    label: str
    category: str
    scale: int
    degreeFromCrisis: int = Field(..., description="Shortest distance to any selected crisis endpoint")
    isCrisisEndpoint: bool = Field(..., description="Is this one of the selected crisis endpoints?")
    isPolicyLever: bool = Field(..., description="Is this a policy lever (scale=1)?")
    description: Optional[str] = None

    class Config:
        from_attributes = True


class CrisisEdge(BaseModel):
    """Edge in crisis subgraph"""
    mechanismId: str
    source: str = Field(..., description="From node ID")
    target: str = Field(..., description="To node ID")
    direction: str
    evidenceQuality: str
    strength: int = Field(..., description="Numeric strength (A=3, B=2, C=1)")
    category: str
    name: str


class CrisisSubgraphStats(BaseModel):
    """Statistics for crisis subgraph"""
    totalNodes: int
    totalEdges: int
    policyLevers: int = Field(..., description="Number of scale=1 policy nodes")
    avgDegree: float = Field(..., description="Average degree from crisis")
    categoryBreakdown: Dict[str, int] = Field(..., description="Count of nodes by category")


class CrisisSubgraphResponse(BaseModel):
    """Response schema for crisis subgraph"""
    nodes: List[CrisisNodeWithDegree]
    edges: List[CrisisEdge]
    stats: CrisisSubgraphStats
    filters: CrisisSubgraphRequest = Field(..., description="Echo back applied filters")


class TraversalDirection(str, Enum):
    """Direction for focal subgraph traversal"""
    UPSTREAM = "upstream"
    DOWNSTREAM = "downstream"
    BOTH = "both"


class NodeResponse(BaseModel):
    """Detailed node information for focal subgraph"""
    id: str
    name: str
    category: str
    scale: int
    description: Optional[str] = None

    class Config:
        from_attributes = True


class MechanismResponse(BaseModel):
    """Detailed mechanism information for focal subgraph"""
    id: str
    name: str
    from_node_id: str
    to_node_id: str
    direction: str
    evidence_quality: Optional[str]
    category: str

    class Config:
        from_attributes = True


class FocalSubgraphRequest(BaseModel):
    """Request schema for focal subgraph analysis"""
    focal_node_id: str = Field(..., description="ID of the focal node to explore from")
    traversal_direction: TraversalDirection = Field(
        default=TraversalDirection.BOTH,
        description="Direction to traverse: upstream (causes), downstream (effects), or both"
    )
    max_hops_upstream: Optional[int] = Field(
        default=None,
        ge=1,
        le=10,
        description="Maximum hops to traverse upstream (null = unlimited)"
    )
    max_hops_downstream: Optional[int] = Field(
        default=None,
        ge=1,
        le=10,
        description="Maximum hops to traverse downstream (null = unlimited)"
    )
    include_categories: Optional[List[str]] = Field(
        default=None,
        description="Only follow mechanisms in these categories (null = all)"
    )
    include_scales: Optional[List[int]] = Field(
        default=None,
        description="Only include nodes at these scale levels (null = all)"
    )
    min_evidence_quality: Optional[str] = Field(
        default=None,
        description="Minimum evidence quality: A, B, or C (null = all)"
    )


class FocalSubgraphResponse(BaseModel):
    """Response schema for focal subgraph"""
    focal_node: NodeResponse
    nodes: List[NodeResponse]
    edges: List[MechanismResponse]
    stats: dict


class CanonicalNodeResponse(BaseModel):
    """Response schema for canonical node from node bank"""
    id: str = Field(..., description="Node identifier (snake_case)")
    name: str = Field(..., description="Human-readable node name")
    scale: int = Field(..., ge=1, le=7, description="Node scale (1-7)")
    category: str = Field(..., description="Node category")
    node_type: Optional[str] = Field("stock", description="Node type: stock, proxy_index, crisis_endpoint")
    unit: Optional[str] = Field(None, description="Unit of measurement")
    description: Optional[str] = Field(None, description="Node description")
    mechanism_count: Optional[int] = Field(None, description="Number of mechanisms referencing this node")

    class Config:
        from_attributes = True


class NodeListResponse(BaseModel):
    """Response schema for node list"""
    nodes: List[CanonicalNodeResponse]
    total: int
    referenced_count: int = Field(..., description="Nodes referenced by at least one mechanism")


# ==========================================
# Helper Functions
# ==========================================

def build_graph(db: Session, exclude_categories: Optional[List[str]] = None,
                only_categories: Optional[List[str]] = None) -> nx.DiGraph:
    """
    Build a NetworkX directed graph from database mechanisms.

    Args:
        db: Database session
        exclude_categories: Categories to exclude from graph
        only_categories: Only include these categories

    Returns:
        NetworkX DiGraph with nodes and edges
    """
    G = nx.DiGraph()

    # Query all mechanisms
    query = db.query(Mechanism)

    # Apply category filters
    if exclude_categories:
        query = query.filter(~Mechanism.category.in_(exclude_categories))
    if only_categories:
        query = query.filter(Mechanism.category.in_(only_categories))

    mechanisms = query.all()

    # Add edges to graph
    for m in mechanisms:
        # Map evidence quality to numeric weight (A=3, B=2, C=1)
        evidence_weight = {'A': 3, 'B': 2, 'C': 1}.get(m.evidence_quality, 1)

        # Add edge with attributes
        G.add_edge(
            m.from_node_id,
            m.to_node_id,
            mechanism_id=m.id,
            weight=evidence_weight,
            direction=m.direction,
            category=m.category,
            evidence_quality=m.evidence_quality
        )

    return G


def get_node_scale(node: Node) -> int:
    """
    Determine node scale.

    Priority:
    1. Use node.scale from database if it exists (trust the database)
    2. Fall back to category-based inference only if scale is NULL

    7-scale taxonomy mapping (fallback only):
    - political -> 1 (structural determinants - policy)
    - built_environment -> 2 (built environment & infrastructure)
    - economic, social_services -> 3 (institutional infrastructure)
    - social_environment, economic_individual -> 4 (individual/household conditions)
    - behavioral, psychosocial -> 5 (individual behaviors & psychosocial)
    - healthcare_access, clinical -> 6 (intermediate pathways)
    - biological, crisis -> 7 (crisis endpoints)
    """
    # If node has explicit scale in database, use it (trust the data)
    if hasattr(node, 'scale') and node.scale is not None:
        return node.scale

    # Fall back to category-based inference only if scale is NULL
    scale_mapping = {
        'political': 1,
        'built_environment': 2,
        'economic': 3,
        'social_services': 3,
        'social_environment': 4,
        'economic_individual': 4,
        'behavioral': 5,
        'psychosocial': 5,
        'healthcare_access': 6,
        'clinical': 6,
        'biological': 7,
        'crisis': 7
    }

    return scale_mapping.get(node.category, 4)


def calculate_composite_score(degree: float, betweenness: float, closeness: float,
                              pagerank: float, evidence: float, scale: int) -> float:
    """
    Calculate composite importance score based purely on network position and evidence.

    Formula:
    composite_score = (
        0.25 * degree +
        0.30 * betweenness +
        0.15 * closeness +
        0.20 * pagerank +
        0.10 * evidence
    )

    No scale multipliers are applied. Node importance is determined by:
    - Network centrality (how connected/influential the node is)
    - Evidence quality (strength of mechanisms involving this node)

    Scale is used for filtering and categorization, not for weighting importance.
    This ensures data-driven prioritization rather than taxonomy-driven bias.
    """
    # Composite score (weighted average of centrality measures)
    composite_score = (
        0.25 * degree +
        0.30 * betweenness +
        0.15 * closeness +
        0.20 * pagerank +
        0.10 * evidence
    )

    return composite_score


def normalize_scores(scores: dict) -> dict:
    """Normalize a dictionary of scores to 0-1 range"""
    if not scores:
        return {}

    max_score = max(scores.values()) if scores.values() else 1.0
    min_score = min(scores.values()) if scores.values() else 0.0

    # Avoid division by zero
    if max_score == min_score:
        return {k: 1.0 for k in scores.keys()}

    return {
        k: (v - min_score) / (max_score - min_score)
        for k, v in scores.items()
    }


def calculate_evidence_scores(db: Session, G: nx.DiGraph) -> dict:
    """
    Calculate average evidence quality for each node.

    Returns:
        Dictionary mapping node_id -> average evidence score (0-1)
    """
    node_evidence = defaultdict(list)

    # Collect evidence scores for each node's mechanisms
    for from_node, to_node, data in G.edges(data=True):
        evidence_weight = data.get('weight', 1)
        node_evidence[from_node].append(evidence_weight)
        node_evidence[to_node].append(evidence_weight)

    # Calculate averages and normalize to 0-1
    evidence_scores = {}
    for node_id, scores in node_evidence.items():
        avg = sum(scores) / len(scores)
        # Normalize: A=3 -> 1.0, B=2 -> 0.67, C=1 -> 0.33
        evidence_scores[node_id] = (avg - 1) / 2  # Maps [1,3] to [0,1]

    return evidence_scores


def bfs_upstream(G: nx.DiGraph, start_node: str, max_hops: Optional[int]) -> set:
    """
    BFS traversal following edges backwards (predecessors).

    Args:
        G: NetworkX directed graph
        start_node: Starting node ID
        max_hops: Maximum hops to traverse (None = unlimited)

    Returns:
        Set of node IDs found upstream (excluding start_node)
    """
    visited = set()
    queue = deque([(start_node, 0)])  # (node_id, hop_count)

    while queue:
        node_id, hops = queue.popleft()

        if node_id in visited:
            continue

        visited.add(node_id)

        # Stop if we've reached max hops
        if max_hops is not None and hops >= max_hops:
            continue

        # Add predecessors (nodes with edges TO current node)
        for predecessor in G.predecessors(node_id):
            if predecessor not in visited:
                queue.append((predecessor, hops + 1))

    return visited - {start_node}  # Exclude start node


def bfs_downstream(G: nx.DiGraph, start_node: str, max_hops: Optional[int]) -> set:
    """
    BFS traversal following edges forward (successors).

    Args:
        G: NetworkX directed graph
        start_node: Starting node ID
        max_hops: Maximum hops to traverse (None = unlimited)

    Returns:
        Set of node IDs found downstream (excluding start_node)
    """
    visited = set()
    queue = deque([(start_node, 0)])

    while queue:
        node_id, hops = queue.popleft()

        if node_id in visited:
            continue

        visited.add(node_id)

        if max_hops is not None and hops >= max_hops:
            continue

        # Add successors (nodes that current node points TO)
        for successor in G.successors(node_id):
            if successor not in visited:
                queue.append((successor, hops + 1))

    return visited - {start_node}


def compute_crisis_subgraph(
    db: Session,
    crisis_node_ids: List[str],
    max_degrees: int,
    min_strength: int,
    include_categories: Optional[List[str]] = None
) -> Tuple[List[Dict], List[Dict], Dict]:
    """
    Compute filtered subgraph showing upstream pathways to crisis endpoints.

    Algorithm:
    1. FILTER: Remove all edges with strength < min_strength
    2. TRAVERSE: BFS upstream from each crisis node up to max_degrees hops
    3. PRUNE: Remove nodes whose paths don't ultimately lead to selected crises
    4. ANNOTATE: Add 'degreeFromCrisis' metadata to each node

    Args:
        db: Database session
        crisis_node_ids: List of crisis endpoint node IDs
        max_degrees: Maximum degrees of separation to traverse
        min_strength: Minimum evidence strength (1=C, 2=B, 3=A)
        include_categories: Optional list of categories to include

    Returns:
        Tuple of (nodes_list, edges_list, stats_dict)
    """
    # Step 1: Filter edges by strength and build graph
    query = db.query(Mechanism)

    # Filter by evidence strength (A=3, B=2, C=1)
    if min_strength == 3:
        query = query.filter(Mechanism.evidence_quality == 'A')
    elif min_strength == 2:
        query = query.filter(Mechanism.evidence_quality.in_(['A', 'B']))
    # min_strength == 1 includes all (A, B, C)

    # Apply category filter if specified
    if include_categories:
        query = query.filter(Mechanism.category.in_(include_categories))

    mechanisms = query.all()

    if not mechanisms:
        return [], [], {
            'totalNodes': 0,
            'totalEdges': 0,
            'policyLevers': 0,
            'avgDegree': 0,
            'categoryBreakdown': {}
        }

    # Step 2: Build reverse graph (child → parent direction for upstream traversal)
    reverse_graph = defaultdict(list)  # Maps node_id -> list of parent node_ids
    mechanism_map = {}  # Maps (from_id, to_id) -> mechanism

    for m in mechanisms:
        reverse_graph[m.to_node_id].append(m.from_node_id)
        mechanism_map[(m.from_node_id, m.to_node_id)] = m

    # Step 3: BFS upstream from each crisis node
    relevant_nodes = set(crisis_node_ids)
    node_degrees = {cid: 0 for cid in crisis_node_ids}

    for crisis_id in crisis_node_ids:
        if crisis_id not in reverse_graph and crisis_id not in [m.to_node_id for m in mechanisms]:
            # Crisis node might not have incoming edges, but should still be included
            relevant_nodes.add(crisis_id)
            continue

        queue = deque([(crisis_id, 0)])
        visited = set()

        while queue:
            node_id, degree = queue.popleft()

            if degree >= max_degrees or node_id in visited:
                continue

            visited.add(node_id)
            relevant_nodes.add(node_id)

            # Update degree (keep minimum degree across all paths)
            if node_id not in node_degrees:
                node_degrees[node_id] = degree
            else:
                node_degrees[node_id] = min(node_degrees[node_id], degree)

            # Add parent nodes to queue
            for parent_id in reverse_graph.get(node_id, []):
                if parent_id not in visited:
                    queue.append((parent_id, degree + 1))

    # Step 4: Prune disconnected branches
    # Build forward graph to verify connectivity
    forward_graph = defaultdict(set)
    for from_id, to_id in mechanism_map.keys():
        if from_id in relevant_nodes and to_id in relevant_nodes:
            forward_graph[from_id].add(to_id)

    # Find all nodes that have at least one path to a crisis endpoint
    connected_nodes = set(crisis_node_ids)
    for crisis_id in crisis_node_ids:
        # Find all ancestors using reverse graph
        queue = deque([crisis_id])
        ancestors = set([crisis_id])
        visited_ancestors = set()

        while queue:
            node = queue.popleft()
            if node in visited_ancestors:
                continue
            visited_ancestors.add(node)
            ancestors.add(node)

            for parent in reverse_graph.get(node, []):
                if parent in relevant_nodes:
                    ancestors.add(parent)
                    queue.append(parent)

        connected_nodes.update(ancestors)

    final_nodes = relevant_nodes.intersection(connected_nodes)

    # Step 5: Get node details from database
    nodes_in_subgraph = db.query(Node).filter(Node.id.in_(final_nodes)).all()
    node_map = {n.id: n for n in nodes_in_subgraph}

    # Build nodes list with metadata
    nodes_list = []
    category_counts = defaultdict(int)
    policy_lever_count = 0

    for node_id in final_nodes:
        node = node_map.get(node_id)
        if not node:
            continue

        scale = get_node_scale(node)
        is_policy_lever = (scale == 1)
        is_crisis = node_id in crisis_node_ids

        if is_policy_lever:
            policy_lever_count += 1

        category_counts[node.category] += 1

        nodes_list.append({
            'nodeId': node_id,
            'label': node.name,
            'category': node.category,
            'scale': scale,
            'degreeFromCrisis': node_degrees.get(node_id, 0),
            'isCrisisEndpoint': is_crisis,
            'isPolicyLever': is_policy_lever,
            'description': node.description
        })

    # Build edges list
    edges_list = []
    for (from_id, to_id), mechanism in mechanism_map.items():
        if from_id in final_nodes and to_id in final_nodes:
            strength_map = {'A': 3, 'B': 2, 'C': 1}
            edges_list.append({
                'mechanismId': mechanism.id,
                'source': from_id,
                'target': to_id,
                'direction': mechanism.direction,
                'evidenceQuality': mechanism.evidence_quality,
                'strength': strength_map.get(mechanism.evidence_quality, 1),
                'category': mechanism.category,
                'name': mechanism.name
            })

    # Calculate stats
    avg_degree = sum(node_degrees.values()) / len(node_degrees) if node_degrees else 0

    stats = {
        'totalNodes': len(nodes_list),
        'totalEdges': len(edges_list),
        'policyLevers': policy_lever_count,
        'avgDegree': round(avg_degree, 2),
        'categoryBreakdown': dict(category_counts)
    }

    return nodes_list, edges_list, stats


def compute_focal_subgraph(
    db: Session,
    focal_node_id: str,
    traversal_direction: TraversalDirection,
    max_hops_upstream: Optional[int],
    max_hops_downstream: Optional[int],
    include_categories: Optional[List[str]],
    include_scales: Optional[List[int]],
    min_evidence_quality: Optional[str]
) -> FocalSubgraphResponse:
    """
    Build subgraph around a focal node using BFS traversal.

    Algorithm:
    1. Build filtered graph (category + evidence filters)
    2. BFS upstream from focal node (limited by max_hops_upstream)
    3. BFS downstream from focal node (limited by max_hops_downstream)
    4. Combine results + filter by scale
    5. Extract relevant mechanisms
    6. Return annotated subgraph

    Args:
        db: Database session
        focal_node_id: ID of focal node to explore from
        traversal_direction: Direction to traverse (upstream/downstream/both)
        max_hops_upstream: Maximum hops upstream (None = unlimited)
        max_hops_downstream: Maximum hops downstream (None = unlimited)
        include_categories: Only include mechanisms in these categories
        include_scales: Only include nodes at these scale levels
        min_evidence_quality: Minimum evidence quality (A/B/C)

    Returns:
        FocalSubgraphResponse with nodes, edges, and statistics
    """
    # Step 1: Build graph with category filters
    G = build_graph(
        db,
        exclude_categories=None,
        only_categories=include_categories
    )

    # Apply evidence filtering
    if min_evidence_quality:
        evidence_order = {'A': 3, 'B': 2, 'C': 1, None: 0}
        min_strength = evidence_order[min_evidence_quality]
        edges_to_remove = [
            (u, v) for u, v, data in G.edges(data=True)
            if evidence_order.get(data.get('evidence_quality')) < min_strength
        ]
        G.remove_edges_from(edges_to_remove)

    # Verify focal node exists
    if focal_node_id not in G:
        raise HTTPException(
            status_code=404,
            detail=f"Focal node '{focal_node_id}' not found in graph"
        )

    # Step 2: BFS Upstream (following edges backwards)
    upstream_nodes = set()
    if traversal_direction in [TraversalDirection.UPSTREAM, TraversalDirection.BOTH]:
        upstream_nodes = bfs_upstream(
            G,
            start_node=focal_node_id,
            max_hops=max_hops_upstream
        )

    # Step 3: BFS Downstream (following edges forward)
    downstream_nodes = set()
    if traversal_direction in [TraversalDirection.DOWNSTREAM, TraversalDirection.BOTH]:
        downstream_nodes = bfs_downstream(
            G,
            start_node=focal_node_id,
            max_hops=max_hops_downstream
        )

    # Step 4: Combine results
    relevant_nodes = upstream_nodes | downstream_nodes | {focal_node_id}

    # Apply scale filter
    if include_scales:
        node_map = {n.id: n for n in db.query(Node).filter(Node.id.in_(relevant_nodes)).all()}
        relevant_nodes = {
            node_id for node_id in relevant_nodes
            if get_node_scale(node_map.get(node_id)) in include_scales
        }

    # Step 5: Extract mechanisms between relevant nodes
    mechanisms = db.query(Mechanism).filter(
        Mechanism.from_node_id.in_(relevant_nodes),
        Mechanism.to_node_id.in_(relevant_nodes)
    ).all()

    # Step 6: Fetch node details
    nodes = db.query(Node).filter(Node.id.in_(relevant_nodes)).all()
    focal_node = db.query(Node).filter(Node.id == focal_node_id).first()

    if not focal_node:
        raise HTTPException(
            status_code=404,
            detail=f"Focal node '{focal_node_id}' not found in database"
        )

    # Step 7: Compute stats
    focal_node_scale = get_node_scale(focal_node)
    scales_present = sorted(set(get_node_scale(n) for n in nodes))

    stats = {
        "focal_node_id": focal_node_id,
        "focal_node_scale": focal_node_scale,
        "total_nodes": len(nodes),
        "total_mechanisms": len(mechanisms),
        "nodes_upstream": len(upstream_nodes),
        "nodes_downstream": len(downstream_nodes),
        "traversal_direction": traversal_direction.value,
        "scales_present": scales_present
    }

    # Build response objects
    focal_node_response = NodeResponse(
        id=focal_node.id,
        name=focal_node.name,
        category=focal_node.category,
        scale=focal_node_scale,
        description=focal_node.description
    )

    node_responses = [
        NodeResponse(
            id=n.id,
            name=n.name,
            category=n.category,
            scale=get_node_scale(n),
            description=n.description
        )
        for n in nodes
    ]

    mechanism_responses = [
        MechanismResponse(
            id=m.id,
            name=m.name,
            from_node_id=m.from_node_id,
            to_node_id=m.to_node_id,
            direction=m.direction,
            evidence_quality=m.evidence_quality,
            category=m.category
        )
        for m in mechanisms
    ]

    return FocalSubgraphResponse(
        focal_node=focal_node_response,
        nodes=node_responses,
        edges=mechanism_responses,
        stats=stats
    )


# ==========================================
# GET Endpoints
# ==========================================

@router.get("/", response_model=NodeListResponse)
def list_nodes(
    referenced_only: bool = Query(True, description="Only return nodes referenced by mechanisms"),
    category: Optional[str] = Query(None, description="Filter by category"),
    scale: Optional[int] = Query(None, ge=1, le=7, description="Filter by scale (1-7)"),
    search: Optional[str] = Query(None, description="Search by name or ID (case-insensitive)"),
    limit: int = Query(1000, le=2000, description="Maximum results"),
    offset: int = Query(0, ge=0, description="Offset for pagination"),
    db: Session = Depends(get_db)
):
    """
    List canonical nodes from the node bank.

    Returns nodes with their full metadata including scale, category,
    description, and unit. By default returns only nodes referenced
    by at least one mechanism.

    Query Parameters:
    - referenced_only: If true (default), only return nodes that appear in mechanisms
    - category: Filter by category (built_environment, economic, political, etc.)
    - scale: Filter by scale level (1-7)
    - search: Search by node name or ID (case-insensitive partial match)
    """
    from sqlalchemy import or_, func

    query = db.query(Node)

    # Apply filters
    if category:
        query = query.filter(Node.category == category)
    if scale:
        query = query.filter(Node.scale == scale)
    if search:
        search_pattern = f"%{search}%"
        query = query.filter(
            or_(
                Node.id.ilike(search_pattern),
                Node.name.ilike(search_pattern)
            )
        )

    # Get all matching nodes
    all_nodes = query.all()

    # Get referenced node IDs (nodes that appear in at least one mechanism)
    from_ids = db.query(Mechanism.from_node_id).distinct()
    to_ids = db.query(Mechanism.to_node_id).distinct()
    referenced_node_ids = {r[0] for r in from_ids.all()} | {r[0] for r in to_ids.all()}

    # Count mechanisms per node for mechanism_count field
    mechanism_counts = {}
    from_counts = db.query(
        Mechanism.from_node_id,
        func.count(Mechanism.id)
    ).group_by(Mechanism.from_node_id).all()
    to_counts = db.query(
        Mechanism.to_node_id,
        func.count(Mechanism.id)
    ).group_by(Mechanism.to_node_id).all()

    for node_id, count in from_counts:
        mechanism_counts[node_id] = mechanism_counts.get(node_id, 0) + count
    for node_id, count in to_counts:
        mechanism_counts[node_id] = mechanism_counts.get(node_id, 0) + count

    # Filter to referenced nodes if requested
    if referenced_only:
        all_nodes = [n for n in all_nodes if n.id in referenced_node_ids]

    # Apply pagination
    total = len(all_nodes)
    paginated_nodes = all_nodes[offset:offset + limit]

    # Build response
    nodes_response = []
    for n in paginated_nodes:
        # Use get_node_scale for consistent scale handling
        node_scale = get_node_scale(n)

        nodes_response.append(CanonicalNodeResponse(
            id=n.id,
            name=n.name,
            scale=node_scale,
            category=n.category,
            node_type=n.node_type or "stock",
            unit=n.unit,
            description=n.description,
            mechanism_count=mechanism_counts.get(n.id, 0)
        ))

    return NodeListResponse(
        nodes=nodes_response,
        total=total,
        referenced_count=len(referenced_node_ids)
    )


@router.get("/importance", response_model=List[NodeImportance])
def get_node_importance(
    top_n: int = Query(20, ge=1, le=100, description="Number of top nodes to return"),
    categories: Optional[str] = Query(None, description="Filter by categories (comma-separated)"),
    scales: Optional[str] = Query(None, description="Filter by scale levels (comma-separated: 1,2,3,4,5,6,7)"),
    min_connections: Optional[int] = Query(None, ge=0, description="Minimum connection threshold"),
    db: Session = Depends(get_db)
):
    """
    Get the most important nodes based on centrality measures and evidence quality.

    Importance is calculated using a composite score that combines:
    - Degree centrality (25%)
    - Betweenness centrality (30%)
    - Closeness centrality (15%)
    - PageRank (20%)
    - Evidence quality (10%)

    No scale multipliers are applied. Importance is purely data-driven based on
    network position and evidence quality, not taxonomy classification.

    Returns nodes ranked by composite importance score.
    """
    # Parse filters
    category_filter = categories.split(',') if categories else None
    scale_filter = [int(s) for s in scales.split(',')] if scales else None

    # Build graph
    G = build_graph(db, only_categories=category_filter)

    if len(G.nodes()) == 0:
        return []

    # Calculate centrality measures
    degree_centrality = nx.degree_centrality(G)
    betweenness_centrality = nx.betweenness_centrality(G)
    closeness_centrality = nx.closeness_centrality(G)
    pagerank = nx.pagerank(G)

    # Calculate evidence scores
    evidence_scores = calculate_evidence_scores(db, G)

    # Normalize all scores to 0-1 range
    degree_norm = normalize_scores(degree_centrality)
    betweenness_norm = normalize_scores(betweenness_centrality)
    closeness_norm = normalize_scores(closeness_centrality)
    pagerank_norm = normalize_scores(pagerank)

    # Get node details from database
    node_ids = list(G.nodes())
    nodes = db.query(Node).filter(Node.id.in_(node_ids)).all()
    node_map = {n.id: n for n in nodes}

    # Calculate composite scores for each node
    node_scores = []

    for node_id in G.nodes():
        node = node_map.get(node_id)
        if not node:
            continue

        # Get scale for this node
        scale = get_node_scale(node)

        # Apply scale filter if specified
        if scale_filter and scale not in scale_filter:
            continue

        # Calculate connections
        in_degree = G.in_degree(node_id)
        out_degree = G.out_degree(node_id)
        total_connections = in_degree + out_degree

        # Apply minimum connections filter
        if min_connections and total_connections < min_connections:
            continue

        # Get normalized scores
        degree = degree_norm.get(node_id, 0)
        betweenness = betweenness_norm.get(node_id, 0)
        closeness = closeness_norm.get(node_id, 0)
        pr = pagerank_norm.get(node_id, 0)
        evidence = evidence_scores.get(node_id, 0)

        # Calculate composite score
        composite = calculate_composite_score(
            degree, betweenness, closeness, pr, evidence, scale
        )

        # Calculate average evidence quality (0-3 scale)
        avg_evidence_quality = evidence * 2 + 1  # Map [0,1] back to [1,3]

        node_scores.append({
            'nodeId': node_id,
            'label': node.name,
            'category': node.category,
            'scale': scale,
            'degreeScore': degree,
            'betweennessScore': betweenness,
            'closenessCentrality': closeness,
            'pageRank': pr,
            'evidenceScore': evidence,
            'compositeScore': composite,
            'totalConnections': total_connections,
            'avgEvidenceQuality': avg_evidence_quality
        })

    # Sort by composite score (descending)
    node_scores.sort(key=lambda x: x['compositeScore'], reverse=True)

    # Assign ranks
    for i, node in enumerate(node_scores[:top_n], start=1):
        node['rank'] = i

    # Return top N
    return [NodeImportance(**node) for node in node_scores[:top_n]]


@router.get("/crisis-endpoints", response_model=List[CrisisEndpoint])
def get_crisis_endpoints(
    db: Session = Depends(get_db)
):
    """
    Get all crisis endpoint nodes (scale=7).

    Crisis endpoints are nodes with scale=7, which include:
    - category='crisis': Acute crisis events, adverse health outcomes, mortality
    - category='biological': Biological pathways that represent crisis states

    Returns all crisis endpoint nodes sorted alphabetically by label.
    """
    # Query all nodes
    all_nodes = db.query(Node).all()

    # Filter to scale=7 nodes (crisis and biological categories)
    crisis_nodes = []
    for node in all_nodes:
        scale = get_node_scale(node)
        if scale == 7:
            crisis_nodes.append(CrisisEndpoint(
                nodeId=node.id,
                label=node.name,
                category=node.category,
                scale=7,
                description=node.description
            ))

    # Sort alphabetically by label
    crisis_nodes.sort(key=lambda x: x.label)

    return crisis_nodes


# ==========================================
# POST Endpoints
# ==========================================

@router.post("/pathfinding", response_model=PathfindingResponse)
def find_paths(
    request: PathfindingRequest,
    db: Session = Depends(get_db)
):
    """
    Find causal pathways between two nodes using various algorithms.

    Algorithms:
    - shortest: Minimize number of hops (unweighted shortest path)
    - strongest_evidence: Optimize for evidence quality (weighted shortest path)
    - all_simple: Find multiple simple paths (no cycles)

    Returns list of paths with detailed node and mechanism information.
    """
    # Build graph with filters
    G = build_graph(
        db,
        exclude_categories=request.exclude_categories,
        only_categories=request.only_categories
    )

    # Validate nodes exist
    if request.from_node not in G:
        raise HTTPException(
            status_code=404,
            detail=f"Source node '{request.from_node}' not found in graph"
        )
    if request.to_node not in G:
        raise HTTPException(
            status_code=404,
            detail=f"Target node '{request.to_node}' not found in graph"
        )

    # Find paths based on algorithm
    paths = []

    try:
        if request.algorithm == 'shortest':
            # Shortest path (minimize hops)
            path = nx.shortest_path(G, request.from_node, request.to_node)
            paths = [path]

        elif request.algorithm == 'strongest_evidence':
            # Weighted shortest path (maximize evidence quality)
            # Use inverse weights: A=1/3, B=1/2, C=1
            G_weighted = G.copy()
            for u, v, data in G_weighted.edges(data=True):
                weight = data.get('weight', 1)
                # Invert weight so higher evidence = lower cost
                G_weighted[u][v]['cost'] = 1.0 / weight

            path = nx.shortest_path(
                G_weighted,
                request.from_node,
                request.to_node,
                weight='cost'
            )
            paths = [path]

        elif request.algorithm == 'all_simple':
            # Find all simple paths up to max_depth
            paths_generator = nx.all_simple_paths(
                G,
                request.from_node,
                request.to_node,
                cutoff=request.max_depth
            )
            paths = list(paths_generator)[:request.max_paths]

        else:
            raise HTTPException(
                status_code=400,
                detail=f"Unknown algorithm '{request.algorithm}'. Use: shortest, strongest_evidence, or all_simple"
            )

    except nx.NetworkXNoPath:
        # No path exists
        return PathfindingResponse(
            fromNode=request.from_node,
            toNode=request.to_node,
            algorithm=request.algorithm,
            pathsFound=0,
            paths=[]
        )

    # Get node and mechanism details
    all_node_ids = set()
    all_mechanism_ids = set()

    for path in paths:
        all_node_ids.update(path)
        for i in range(len(path) - 1):
            edge_data = G[path[i]][path[i + 1]]
            all_mechanism_ids.add(edge_data['mechanism_id'])

    # Query database for details
    nodes = db.query(Node).filter(Node.id.in_(all_node_ids)).all()
    node_map = {n.id: n for n in nodes}

    mechanisms = db.query(Mechanism).filter(Mechanism.id.in_(all_mechanism_ids)).all()
    mechanism_map = {m.id: m for m in mechanisms}

    # Build PathResult objects
    path_results = []

    for idx, path in enumerate(paths):
        # Collect mechanisms in path order
        mechanism_ids = []
        mechanism_details = []

        for i in range(len(path) - 1):
            edge_data = G[path[i]][path[i + 1]]
            mech_id = edge_data['mechanism_id']
            mechanism_ids.append(mech_id)

            mech = mechanism_map.get(mech_id)
            if mech:
                mechanism_details.append(PathMechanism(
                    mechanismId=mech.id,
                    name=mech.name,
                    fromNode=mech.from_node_id,
                    toNode=mech.to_node_id,
                    direction=mech.direction,
                    evidenceQuality=mech.evidence_quality,
                    category=mech.category
                ))

        # Collect node details
        node_details = []
        for node_id in path:
            node = node_map.get(node_id)
            if node:
                node_details.append(PathNode(
                    nodeId=node.id,
                    label=node.name,
                    category=node.category,
                    scale=get_node_scale(node)
                ))

        # Calculate metrics
        path_length = len(path) - 1

        # Average evidence quality
        evidence_weights = [
            G[path[i]][path[i + 1]].get('weight', 1)
            for i in range(len(path) - 1)
        ]
        avg_evidence = sum(evidence_weights) / len(evidence_weights) if evidence_weights else 0

        # Evidence grade (A >= 2.5, B >= 1.5, C < 1.5)
        if avg_evidence >= 2.5:
            evidence_grade = 'A'
        elif avg_evidence >= 1.5:
            evidence_grade = 'B'
        else:
            evidence_grade = 'C'

        # Overall direction
        directions = [
            G[path[i]][path[i + 1]].get('direction', 'positive')
            for i in range(len(path) - 1)
        ]
        positive_count = sum(1 for d in directions if d == 'positive')
        negative_count = len(directions) - positive_count

        if negative_count == 0:
            overall_direction = 'positive'
        elif positive_count == 0:
            overall_direction = 'negative'
        else:
            overall_direction = 'mixed'

        # Total weight
        total_weight = sum(evidence_weights)

        path_results.append(PathResult(
            pathId=f"path_{idx + 1}",
            nodes=path,
            nodeDetails=node_details,
            edges=mechanism_ids,
            mechanismDetails=mechanism_details,
            pathLength=path_length,
            avgEvidenceQuality=avg_evidence,
            evidenceGrade=evidence_grade,
            overallDirection=overall_direction,
            totalWeight=total_weight
        ))

    return PathfindingResponse(
        fromNode=request.from_node,
        toNode=request.to_node,
        algorithm=request.algorithm,
        pathsFound=len(path_results),
        paths=path_results
    )


@router.post("/crisis-subgraph", response_model=CrisisSubgraphResponse)
def get_crisis_subgraph(
    request: CrisisSubgraphRequest,
    db: Session = Depends(get_db)
):
    """
    Compute filtered subgraph showing upstream pathways to crisis endpoints.

    This endpoint analyzes causal pathways leading to selected crisis endpoints,
    intelligently pruning based on:
    - Degrees of separation (max hops from crisis)
    - Evidence strength (minimum quality threshold)
    - Category filtering (optional)

    The algorithm performs upstream BFS traversal from each crisis endpoint,
    identifies policy levers (scale=1 nodes), and annotates each node with
    its shortest distance to any crisis endpoint.

    Returns a pruned subgraph containing only mechanistically-relevant nodes
    and edges, along with statistics and metadata.
    """
    # Validate crisis node IDs exist
    crisis_nodes = db.query(Node).filter(Node.id.in_(request.crisisNodeIds)).all()
    found_ids = {n.id for n in crisis_nodes}
    missing_ids = set(request.crisisNodeIds) - found_ids

    if missing_ids:
        raise HTTPException(
            status_code=404,
            detail=f"Crisis node(s) not found: {', '.join(missing_ids)}"
        )

    # Validate crisis nodes are actually scale=7
    invalid_nodes = []
    for node in crisis_nodes:
        if get_node_scale(node) != 7:
            invalid_nodes.append(f"{node.id} (scale={get_node_scale(node)})")

    if invalid_nodes:
        raise HTTPException(
            status_code=400,
            detail=f"Selected nodes are not crisis endpoints (scale=7): {', '.join(invalid_nodes)}"
        )

    # Compute crisis subgraph
    nodes_list, edges_list, stats = compute_crisis_subgraph(
        db=db,
        crisis_node_ids=request.crisisNodeIds,
        max_degrees=request.maxDegrees,
        min_strength=request.minStrength,
        include_categories=request.includeCategories
    )

    # Convert to Pydantic models
    nodes_response = [CrisisNodeWithDegree(**node) for node in nodes_list]
    edges_response = [CrisisEdge(**edge) for edge in edges_list]
    stats_response = CrisisSubgraphStats(**stats)

    return CrisisSubgraphResponse(
        nodes=nodes_response,
        edges=edges_response,
        stats=stats_response,
        filters=request
    )


@router.post("/focal-subgraph", response_model=FocalSubgraphResponse)
def get_focal_subgraph(
    request: FocalSubgraphRequest,
    db: Session = Depends(get_db)
):
    """
    Get subgraph around a focal node with configurable traversal.

    This endpoint enables exploring causal pathways from any node:
    - Upstream: What causes this node? (predecessors)
    - Downstream: What effects does this node have? (successors)
    - Both: Full causal chain through this node

    Examples:
    - Policy impact analysis: focal_node = policy lever (scale=1), direction=downstream
    - Root cause analysis: focal_node = condition (scale=4), direction=upstream
    - Full pathway: focal_node = intermediate (scale=6), direction=both

    Filters:
    - include_categories: Only follow mechanisms in specified categories
    - include_scales: Only show nodes at specified scale levels
    - min_evidence_quality: Only follow high-quality evidence links
    - max_hops: Limit traversal depth in each direction
    """
    try:
        return compute_focal_subgraph(
            db=db,
            focal_node_id=request.focal_node_id,
            traversal_direction=request.traversal_direction,
            max_hops_upstream=request.max_hops_upstream,
            max_hops_downstream=request.max_hops_downstream,
            include_categories=request.include_categories,
            include_scales=request.include_scales,
            min_evidence_quality=request.min_evidence_quality
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# ==========================================
# Hierarchy API Endpoints (NEW)
# ==========================================

class HierarchyNodeResponse(BaseModel):
    """Response schema for a node with hierarchy information"""
    id: str
    name: str
    scale: int
    category: str
    node_type: Optional[str] = "stock"
    unit: Optional[str] = None
    description: Optional[str] = None

    # Hierarchy fields
    depth: int = Field(0, description="Depth in hierarchy: 0 = root/domain node")
    primaryPath: Optional[str] = Field(None, description="Primary path: root_id/parent_id/this_id")
    allAncestors: List[str] = Field(default_factory=list, description="All ancestor node IDs")
    isGroupingNode: bool = Field(False, description="Whether this is a grouping/container node")
    domains: List[str] = Field(default_factory=list, description="Domain(s) this node belongs to")
    parentIds: List[str] = Field(default_factory=list, description="Direct parent node IDs")
    childIds: List[str] = Field(default_factory=list, description="Direct child node IDs")
    hasChildren: bool = Field(False, description="Whether this node has children")
    childCount: int = Field(0, description="Number of direct children")

    class Config:
        from_attributes = True


class HierarchyTreeNode(BaseModel):
    """Hierarchy tree node for nested structure"""
    id: str
    name: str
    scale: int
    depth: int
    domains: List[str]
    isGroupingNode: bool
    childCount: int
    children: Optional[List["HierarchyTreeNode"]] = None

    class Config:
        from_attributes = True


# Enable self-referencing
HierarchyTreeNode.model_rebuild()


class HierarchyTreeResponse(BaseModel):
    """Response schema for hierarchy tree"""
    roots: List[HierarchyTreeNode]
    totalNodes: int
    maxDepth: int


class NodeAncestorsResponse(BaseModel):
    """Response schema for node ancestors"""
    nodeId: str
    ancestors: List[HierarchyNodeResponse]
    paths: List[List[str]] = Field(description="Multiple paths for DAG (each path is array of node IDs)")


class NodeDescendantsResponse(BaseModel):
    """Response schema for node descendants"""
    nodeId: str
    descendants: List[HierarchyNodeResponse]
    totalCount: int
    maxDepth: int


class AddHierarchyRelationshipRequest(BaseModel):
    """Request to add a parent-child relationship"""
    parentId: str = Field(..., description="Parent node ID")
    childId: str = Field(..., description="Child node ID")
    relationshipType: str = Field("contains", description="Relationship type: contains, specializes, contextualizes")
    orderIndex: int = Field(0, description="Order among siblings")


class HierarchyRelationshipResponse(BaseModel):
    """Response for hierarchy relationship operations"""
    success: bool
    message: str
    parentId: str
    childId: str


def node_to_hierarchy_response(node: Node) -> HierarchyNodeResponse:
    """Convert a Node model to HierarchyNodeResponse"""
    parent_ids = [p.id for p in node.parents] if hasattr(node, 'parents') and node.parents else []
    child_ids = [c.id for c in node.children] if hasattr(node, 'children') and node.children else []

    # Compute domains from ancestors (root nodes at depth=0)
    domains = node.domains if hasattr(node, 'domains') else []

    return HierarchyNodeResponse(
        id=node.id,
        name=node.name,
        scale=get_node_scale(node),
        category=node.category,
        node_type=node.node_type or "stock",
        unit=node.unit,
        description=node.description,
        depth=node.depth or 0,
        primaryPath=node.primary_path,
        allAncestors=node.all_ancestors or [],
        isGroupingNode=node.is_grouping_node or False,
        domains=domains,
        parentIds=parent_ids,
        childIds=child_ids,
        hasChildren=len(child_ids) > 0,
        childCount=len(child_ids)
    )


@router.get("/hierarchy/roots", response_model=List[HierarchyNodeResponse])
def get_hierarchy_roots(
    domain: Optional[str] = Query(None, description="Filter by domain"),
    db: Session = Depends(get_db)
):
    """
    Get all root nodes (depth=0) in the hierarchy.

    Root nodes are domain nodes that have no parents. These form the
    top level of the hierarchy tree.

    Query Parameters:
    - domain: Filter by specific domain (e.g., 'healthcare_system', 'housing')
    """
    # Filter for actual domain root nodes (depth=0 AND is_grouping_node=True)
    query = db.query(Node).filter(
        Node.depth == 0,
        Node.is_grouping_node == True
    )

    if domain:
        # Filter by specific domain ID
        query = query.filter(Node.id == domain)

    roots = query.order_by(Node.display_order, Node.name).all()

    return [node_to_hierarchy_response(node) for node in roots]


@router.get("/hierarchy/tree", response_model=HierarchyTreeResponse)
def get_hierarchy_tree(
    max_depth: int = Query(3, ge=1, le=10, description="Maximum depth to traverse"),
    domains: Optional[str] = Query(None, description="Filter by domains (comma-separated)"),
    scales: Optional[str] = Query(None, description="Filter by scales (comma-separated: 1,2,3,4,5,6,7)"),
    db: Session = Depends(get_db)
):
    """
    Get the full hierarchy tree structure.

    Returns a nested tree structure starting from root nodes (depth=0)
    down to the specified max_depth.

    Query Parameters:
    - max_depth: Maximum depth to traverse (default 3)
    - domains: Filter by domains (comma-separated)
    - scales: Filter by scales (comma-separated)
    """
    domain_filter = domains.split(',') if domains else None
    scale_filter = [int(s) for s in scales.split(',')] if scales else None

    # Get root nodes (depth=0 AND is_grouping_node=True)
    root_query = db.query(Node).filter(
        Node.depth == 0,
        Node.is_grouping_node == True
    )

    if domain_filter:
        root_query = root_query.filter(Node.id.in_(domain_filter))

    roots = root_query.order_by(Node.display_order, Node.name).all()

    def build_tree_node(node: Node, current_depth: int) -> HierarchyTreeNode:
        """Recursively build tree node structure"""
        # Get children
        children = []
        if current_depth < max_depth and hasattr(node, 'children') and node.children:
            for child in sorted(node.children, key=lambda c: (c.display_order or 0, c.name)):
                # Apply scale filter
                if scale_filter and get_node_scale(child) not in scale_filter:
                    continue
                children.append(build_tree_node(child, current_depth + 1))

        return HierarchyTreeNode(
            id=node.id,
            name=node.name,
            scale=get_node_scale(node),
            depth=node.depth or 0,
            domains=node.domains if hasattr(node, 'domains') else [],
            isGroupingNode=node.is_grouping_node or False,
            childCount=len(node.children) if hasattr(node, 'children') and node.children else 0,
            children=children if children else None
        )

    tree_roots = [build_tree_node(root, 0) for root in roots]

    # Calculate total nodes and max depth
    total_nodes = 0
    actual_max_depth = 0

    def count_nodes(tree_node: HierarchyTreeNode, depth: int):
        nonlocal total_nodes, actual_max_depth
        total_nodes += 1
        actual_max_depth = max(actual_max_depth, depth)
        if tree_node.children:
            for child in tree_node.children:
                count_nodes(child, depth + 1)

    for root in tree_roots:
        count_nodes(root, 0)

    return HierarchyTreeResponse(
        roots=tree_roots,
        totalNodes=total_nodes,
        maxDepth=actual_max_depth
    )


@router.get("/{node_id}/ancestors", response_model=NodeAncestorsResponse)
def get_node_ancestors(
    node_id: str,
    db: Session = Depends(get_db)
):
    """
    Get all ancestors of a node.

    Returns all parent nodes in the hierarchy, including multiple
    paths for DAG structures where a node has multiple parents.
    """
    node = db.query(Node).filter(Node.id == node_id).first()

    if not node:
        raise HTTPException(status_code=404, detail=f"Node '{node_id}' not found")

    # Get ancestors from all_ancestors field or compute from parents
    ancestor_ids = node.all_ancestors or []

    if ancestor_ids:
        ancestors = db.query(Node).filter(Node.id.in_(ancestor_ids)).all()
    else:
        ancestors = []

    # Build paths (each path is a list of node IDs from root to parent)
    paths = []
    if node.primary_path:
        # Primary path: "root/parent/this" -> ["root", "parent"]
        path_parts = node.primary_path.split('/')
        if len(path_parts) > 1:
            paths.append(path_parts[:-1])  # Exclude self

    # For DAG, we could have multiple paths - simplified for now

    return NodeAncestorsResponse(
        nodeId=node_id,
        ancestors=[node_to_hierarchy_response(a) for a in ancestors],
        paths=paths
    )


@router.get("/{node_id}/descendants", response_model=NodeDescendantsResponse)
def get_node_descendants(
    node_id: str,
    max_depth: int = Query(10, ge=1, le=20, description="Maximum depth to traverse"),
    db: Session = Depends(get_db)
):
    """
    Get all descendants of a node.

    Returns all child nodes recursively up to max_depth.
    """
    from utils.hierarchy import get_all_descendants

    node = db.query(Node).filter(Node.id == node_id).first()

    if not node:
        raise HTTPException(status_code=404, detail=f"Node '{node_id}' not found")

    # Get all descendants recursively
    descendant_ids = get_all_descendants(db, node_id, Node)

    if descendant_ids:
        descendants = db.query(Node).filter(Node.id.in_(descendant_ids)).all()
    else:
        descendants = []

    # Calculate max depth among descendants
    max_found_depth = 0
    for d in descendants:
        if d.depth and d.depth > max_found_depth:
            max_found_depth = d.depth

    return NodeDescendantsResponse(
        nodeId=node_id,
        descendants=[node_to_hierarchy_response(d) for d in descendants],
        totalCount=len(descendants),
        maxDepth=max_found_depth - (node.depth or 0)
    )


@router.get("/{node_id}/children", response_model=List[HierarchyNodeResponse])
def get_node_children(
    node_id: str,
    db: Session = Depends(get_db)
):
    """
    Get direct children of a node.

    Returns only immediate children, not all descendants.
    """
    node = db.query(Node).filter(Node.id == node_id).first()

    if not node:
        raise HTTPException(status_code=404, detail=f"Node '{node_id}' not found")

    children = node.children if hasattr(node, 'children') and node.children else []
    children_sorted = sorted(children, key=lambda c: (c.display_order or 0, c.name))

    return [node_to_hierarchy_response(child) for child in children_sorted]


@router.get("/{node_id}/parents", response_model=List[HierarchyNodeResponse])
def get_node_parents(
    node_id: str,
    db: Session = Depends(get_db)
):
    """
    Get direct parents of a node.

    In a DAG structure, a node can have multiple parents.
    """
    node = db.query(Node).filter(Node.id == node_id).first()

    if not node:
        raise HTTPException(status_code=404, detail=f"Node '{node_id}' not found")

    parents = node.parents if hasattr(node, 'parents') and node.parents else []

    return [node_to_hierarchy_response(parent) for parent in parents]


@router.get("/{node_id}/hierarchy", response_model=HierarchyNodeResponse)
def get_node_hierarchy_info(
    node_id: str,
    db: Session = Depends(get_db)
):
    """
    Get a single node with full hierarchy information.

    Returns the node with all hierarchy fields populated including
    parents, children, ancestors, and domains.
    """
    node = db.query(Node).filter(Node.id == node_id).first()

    if not node:
        raise HTTPException(status_code=404, detail=f"Node '{node_id}' not found")

    return node_to_hierarchy_response(node)


@router.post("/hierarchy/relationship", response_model=HierarchyRelationshipResponse)
def add_hierarchy_relationship(
    request: AddHierarchyRelationshipRequest,
    db: Session = Depends(get_db)
):
    """
    Add a parent-child relationship between nodes.

    Creates a new hierarchy relationship with cycle detection
    to maintain DAG integrity.
    """
    from utils.hierarchy import add_parent_child_relationship
    from models.mechanism import node_hierarchy

    success, message = add_parent_child_relationship(
        db=db,
        parent_id=request.parentId,
        child_id=request.childId,
        node_model=Node,
        node_hierarchy_table=node_hierarchy,
        relationship_type=request.relationshipType,
        order_index=request.orderIndex
    )

    if not success:
        raise HTTPException(status_code=400, detail=message)

    return HierarchyRelationshipResponse(
        success=success,
        message=message,
        parentId=request.parentId,
        childId=request.childId
    )


@router.delete("/hierarchy/relationship", response_model=HierarchyRelationshipResponse)
def remove_hierarchy_relationship(
    parent_id: str = Query(..., description="Parent node ID"),
    child_id: str = Query(..., description="Child node ID"),
    db: Session = Depends(get_db)
):
    """
    Remove a parent-child relationship between nodes.

    Deletes the hierarchy relationship and updates descendant
    hierarchy fields accordingly.
    """
    from utils.hierarchy import remove_parent_child_relationship
    from models.mechanism import node_hierarchy

    success, message = remove_parent_child_relationship(
        db=db,
        parent_id=parent_id,
        child_id=child_id,
        node_model=Node,
        node_hierarchy_table=node_hierarchy
    )

    if not success:
        raise HTTPException(status_code=400, detail=message)

    return HierarchyRelationshipResponse(
        success=success,
        message=message,
        parentId=parent_id,
        childId=child_id
    )


@router.get("/validate/{node_id}")
def validate_node_exists(
    node_id: str,
    db: Session = Depends(get_db)
):
    """
    Check if a node exists in the Node Bank.

    Used for mechanism validation to ensure referenced nodes exist.
    Returns 200 if exists, 404 if not.
    """
    node = db.query(Node).filter(Node.id == node_id).first()

    if not node:
        raise HTTPException(status_code=404, detail=f"Node '{node_id}' not found in Node Bank")

    return {
        "exists": True,
        "nodeId": node_id,
        "name": node.name,
        "scale": get_node_scale(node),
        "category": node.category
    }
