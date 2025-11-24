"""
API routes for browsing curated pathways.

Pathways are sequences of mechanisms that form notable causal chains,
such as "Poverty → Health Outcomes" or "Housing Policy → Disease Burden".
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional, Dict, Set, Tuple
from pydantic import BaseModel, Field
from collections import defaultdict
import json

from models import Mechanism, Node, get_db


router = APIRouter(prefix="/api/pathways", tags=["pathways"])


# ==========================================
# Schemas
# ==========================================

class PathwayMechanism(BaseModel):
    """Mechanism within a pathway"""
    mechanismId: str
    name: str
    fromNode: str
    toNode: str
    direction: str
    evidenceQuality: str

    class Config:
        from_attributes = True


class PathwaySummary(BaseModel):
    """Summary information for pathway list view"""
    pathwayId: str
    title: str
    description: str
    fromNodeLabel: str
    toNodeLabel: str
    category: str  # Primary category
    pathLength: int
    avgEvidenceQuality: float
    overallDirection: str
    tags: List[str] = Field(default_factory=list)

    class Config:
        from_attributes = True


class PathwayDetail(BaseModel):
    """Full pathway information"""
    pathwayId: str
    title: str
    description: str
    fromNodeId: str
    toNodeId: str
    mechanisms: List[PathwayMechanism]
    pathLength: int
    avgEvidenceQuality: float
    evidenceGrade: str
    overallDirection: str
    tags: List[str]
    curatedBy: Optional[str] = None
    dateCreated: Optional[str] = None

    class Config:
        from_attributes = True


# ==========================================
# Helper Functions
# ==========================================

def calculate_evidence_score(quality: str) -> float:
    """Convert evidence quality to numeric score"""
    quality_map = {
        'A': 3.0,
        'B': 2.0,
        'C': 1.0,
    }
    return quality_map.get(quality.upper(), 0.0)


def get_evidence_grade(avg_score: float) -> str:
    """Convert average score to letter grade"""
    if avg_score >= 2.5:
        return 'A'
    elif avg_score >= 1.5:
        return 'B'
    else:
        return 'C'


def build_pathway_graph(mechanisms: List[Mechanism]) -> Dict[str, List[Tuple[str, Mechanism]]]:
    """Build adjacency list from mechanisms"""
    graph = defaultdict(list)
    for mech in mechanisms:
        graph[mech.from_node_id].append((mech.to_node_id, mech))
    return graph


def find_paths(
    graph: Dict[str, List[Tuple[str, Mechanism]]],
    start: str,
    end: str,
    max_length: int = 4,
    current_path: Optional[List[Mechanism]] = None,
    visited: Optional[Set[str]] = None
) -> List[List[Mechanism]]:
    """Find all paths between two nodes (DFS with cycle detection)"""
    if current_path is None:
        current_path = []
    if visited is None:
        visited = set()

    # Avoid cycles
    if start in visited:
        return []

    # Path too long
    if len(current_path) >= max_length:
        return []

    # Found target
    if start == end and current_path:
        return [current_path.copy()]

    visited.add(start)
    all_paths = []

    for next_node, mechanism in graph.get(start, []):
        current_path.append(mechanism)
        paths = find_paths(graph, next_node, end, max_length, current_path, visited.copy())
        all_paths.extend(paths)
        current_path.pop()

    return all_paths


def generate_curated_pathways(db: Session) -> List[PathwaySummary]:
    """
    Generate curated pathways from mechanism bank.

    For MVP: Dynamically discover interesting pathways.
    For production: Pre-compute and store in database.
    """
    # Fetch all mechanisms
    mechanisms = db.query(Mechanism).all()

    # Fetch all nodes for labels
    nodes = db.query(Node).all()
    node_map = {node.node_id: node for node in nodes}

    # Build pathway graph
    graph = build_pathway_graph(mechanisms)

    # Define key intervention nodes (starting points)
    intervention_nodes = [
        "housing_policy",
        "minimum_wage",
        "healthcare_access",
        "education_funding",
        "social_safety_net",
        "neighborhood_investment"
    ]

    # Define key outcome nodes (endpoints)
    outcome_nodes = [
        "health_outcomes",
        "mortality",
        "disease_burden",
        "life_expectancy",
        "health_equity",
        "ald_mortality"
    ]

    # Find pathways between interventions and outcomes
    pathways = []
    pathway_id = 1

    for start_node in intervention_nodes:
        if start_node not in node_map:
            continue

        for end_node in outcome_nodes:
            if end_node not in node_map:
                continue

            # Find all paths (max 4 steps)
            paths = find_paths(graph, start_node, end_node, max_length=4)

            # Convert each path to PathwaySummary
            for path in paths:
                if not path:
                    continue

                # Calculate metrics
                evidence_scores = [calculate_evidence_score(m.evidence_quality or 'C') for m in path]
                avg_evidence = sum(evidence_scores) / len(evidence_scores) if evidence_scores else 0.0

                # Determine overall direction
                positive_count = sum(1 for m in path if m.direction == 'positive')
                negative_count = sum(1 for m in path if m.direction == 'negative')
                if positive_count > negative_count:
                    overall_direction = 'positive'
                elif negative_count > positive_count:
                    overall_direction = 'negative'
                else:
                    overall_direction = 'mixed'

                # Get primary category (most common)
                categories = [m.category for m in path if m.category]
                primary_category = max(set(categories), key=categories.count) if categories else 'unknown'

                # Generate tags
                tags = []
                for m in path:
                    if m.tags:
                        try:
                            if isinstance(m.tags, str):
                                mechanism_tags = json.loads(m.tags)
                            else:
                                mechanism_tags = m.tags
                            tags.extend(mechanism_tags)
                        except:
                            pass
                tags = list(set(tags))[:5]  # Unique, max 5

                # Create summary
                start_label = node_map[start_node].label
                end_label = node_map[end_node].label

                pathway = PathwaySummary(
                    pathwayId=f"pathway_{pathway_id}",
                    title=f"{start_label} to {end_label}",
                    description=f"Causal pathway from {start_label} to {end_label} through {len(path)} mechanisms",
                    fromNodeLabel=start_label,
                    toNodeLabel=end_label,
                    category=primary_category,
                    pathLength=len(path),
                    avgEvidenceQuality=avg_evidence,
                    overallDirection=overall_direction,
                    tags=tags
                )
                pathways.append(pathway)
                pathway_id += 1

    return pathways


# ==========================================
# Endpoints
# ==========================================

@router.get("/", response_model=List[PathwaySummary])
def list_pathways(
    category: Optional[str] = Query(None),
    tag: Optional[str] = Query(None),
    min_evidence: Optional[str] = Query(None, regex="^[ABC]$"),
    limit: int = Query(50, le=100),
    db: Session = Depends(get_db)
):
    """
    List curated pathways with optional filtering.

    For MVP: Returns common pathways discovered from mechanism bank.
    For production: Store pre-curated pathways in database.
    """

    # Generate pathways dynamically
    pathways = generate_curated_pathways(db)

    # Apply filters
    filtered = pathways

    if category:
        filtered = [p for p in filtered if p.category == category]

    if tag:
        filtered = [p for p in filtered if tag in p.tags]

    if min_evidence:
        min_score = calculate_evidence_score(min_evidence)
        filtered = [p for p in filtered if p.avgEvidenceQuality >= min_score]

    # Sort by evidence quality (descending)
    filtered.sort(key=lambda p: p.avgEvidenceQuality, reverse=True)

    # Apply limit
    return filtered[:limit]


@router.get("/{pathway_id}", response_model=PathwayDetail)
def get_pathway(
    pathway_id: str,
    db: Session = Depends(get_db)
):
    """Get detailed information for a specific pathway."""

    # For MVP: Reconstruct pathway from ID
    # Format: pathway_123
    try:
        pathway_index = int(pathway_id.split('_')[1]) - 1
    except (IndexError, ValueError):
        raise HTTPException(status_code=400, detail="Invalid pathway ID format")

    # Generate all pathways and find the one matching the ID
    all_pathways = generate_curated_pathways(db)

    if pathway_index < 0 or pathway_index >= len(all_pathways):
        raise HTTPException(status_code=404, detail="Pathway not found")

    summary = all_pathways[pathway_index]

    # Fetch mechanisms for this pathway
    # We need to reconstruct the path again (this is inefficient, but works for MVP)
    mechanisms = db.query(Mechanism).all()
    nodes = db.query(Node).all()
    node_map = {node.node_id: node for node in nodes}

    graph = build_pathway_graph(mechanisms)

    # Find the start and end nodes from labels
    start_node_id = None
    end_node_id = None
    for node_id, node in node_map.items():
        if node.label == summary.fromNodeLabel:
            start_node_id = node_id
        if node.label == summary.toNodeLabel:
            end_node_id = node_id

    if not start_node_id or not end_node_id:
        raise HTTPException(status_code=404, detail="Pathway nodes not found")

    # Find paths and get the one at the correct index
    paths = find_paths(graph, start_node_id, end_node_id, max_length=4)

    # Calculate which path matches (skip to correct index)
    # This is a simplification - in production, store pathway definitions
    pathway_mechanisms = []
    if pathway_index < len(paths):
        for mech in paths[pathway_index]:
            pathway_mechanisms.append(PathwayMechanism(
                mechanismId=mech.mechanism_id,
                name=mech.name or f"{mech.from_node_id} → {mech.to_node_id}",
                fromNode=node_map[mech.from_node_id].label,
                toNode=node_map[mech.to_node_id].label,
                direction=mech.direction or 'unknown',
                evidenceQuality=mech.evidence_quality or 'C'
            ))

    # Build detail object
    detail = PathwayDetail(
        pathwayId=summary.pathwayId,
        title=summary.title,
        description=summary.description,
        fromNodeId=start_node_id,
        toNodeId=end_node_id,
        mechanisms=pathway_mechanisms,
        pathLength=summary.pathLength,
        avgEvidenceQuality=summary.avgEvidenceQuality,
        evidenceGrade=get_evidence_grade(summary.avgEvidenceQuality),
        overallDirection=summary.overallDirection,
        tags=summary.tags,
        curatedBy="System",
        dateCreated="2025-01-15"
    )

    return detail


@router.get("/search", response_model=List[PathwaySummary])
def search_pathways(
    query: str = Query(..., min_length=2),
    db: Session = Depends(get_db)
):
    """Search pathways by keyword in title or description."""

    # Generate pathways
    pathways = generate_curated_pathways(db)

    # Filter by search query
    query_lower = query.lower()
    results = [
        p for p in pathways
        if query_lower in p.title.lower() or
           query_lower in p.description.lower() or
           any(query_lower in tag.lower() for tag in p.tags)
    ]

    return results[:50]
