"""
API routes for mechanisms (CRUD operations).

Provides REST API for accessing and managing causal mechanisms.
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from pathlib import Path
import yaml

from models import Mechanism, Node, get_db
from pydantic import BaseModel


router = APIRouter(prefix="/api/mechanisms", tags=["mechanisms"])


# Pydantic schemas for request/response validation
class MechanismResponse(BaseModel):
    """Response schema for mechanism"""
    id: str
    name: str
    from_node: dict
    to_node: dict
    direction: str
    category: str
    mechanism_pathway: List[str]
    evidence: dict
    spatial_variation: Optional[dict] = None
    moderators: Optional[List[dict]] = None
    structural_competency: Optional[dict] = None
    description: str
    version: str
    last_updated: Optional[str] = None
    validated_by: Optional[List[str]] = None

    class Config:
        from_attributes = True


class MechanismListItem(BaseModel):
    """Minimal mechanism info for list view"""
    id: str
    name: str
    from_node_id: str
    from_node_name: str
    to_node_id: str
    to_node_name: str
    direction: str
    category: str
    evidence_quality: str

    class Config:
        from_attributes = True


# ==========================================
# GET Endpoints
# ==========================================

@router.get("/", response_model=List[MechanismListItem])
def list_mechanisms(
    category: Optional[str] = Query(None, description="Filter by category"),
    direction: Optional[str] = Query(None, description="Filter by direction (positive/negative)"),
    from_node: Optional[str] = Query(None, description="Filter by source node ID"),
    to_node: Optional[str] = Query(None, description="Filter by target node ID"),
    evidence_quality: Optional[str] = Query(None, description="Filter by evidence quality (A/B/C)"),
    limit: int = Query(100, le=1000, description="Maximum number of results"),
    offset: int = Query(0, ge=0, description="Offset for pagination"),
    db: Session = Depends(get_db)
):
    """
    List mechanisms with optional filtering.

    Supports filtering by:
    - category (built_environment, economic, political, etc.)
    - direction (positive, negative)
    - from_node (source node ID)
    - to_node (target node ID)
    - evidence_quality (A, B, C)

    Returns minimal mechanism info for efficient list views.
    """
    query = db.query(Mechanism)

    # Apply filters
    if category:
        query = query.filter(Mechanism.category == category)
    if direction:
        query = query.filter(Mechanism.direction == direction)
    if from_node:
        query = query.filter(Mechanism.from_node_id == from_node)
    if to_node:
        query = query.filter(Mechanism.to_node_id == to_node)
    if evidence_quality:
        query = query.filter(Mechanism.evidence_quality == evidence_quality)

    # Paginate
    mechanisms = query.offset(offset).limit(limit).all()

    # Format response
    return [
        MechanismListItem(
            id=m.id,
            name=m.name,
            from_node_id=m.from_node_id,
            from_node_name=m.from_node.name if m.from_node else m.from_node_id,
            to_node_id=m.to_node_id,
            to_node_name=m.to_node.name if m.to_node else m.to_node_id,
            direction=m.direction,
            category=m.category,
            evidence_quality=m.evidence_quality
        )
        for m in mechanisms
    ]


@router.get("/{mechanism_id}", response_model=MechanismResponse)
def get_mechanism(mechanism_id: str, db: Session = Depends(get_db)):
    """
    Get detailed information for a specific mechanism.

    Returns full mechanism data including:
    - Complete pathway description
    - Evidence details with citations
    - Moderators
    - Structural competency analysis
    - LLM metadata (if applicable)
    """
    mechanism = db.query(Mechanism).filter(Mechanism.id == mechanism_id).first()

    if not mechanism:
        raise HTTPException(status_code=404, detail=f"Mechanism {mechanism_id} not found")

    return mechanism.to_dict()


@router.get("/search/pathway")
def search_pathway(
    from_node: str = Query(..., description="Starting node ID"),
    to_node: str = Query(..., description="Ending node ID"),
    max_depth: int = Query(3, ge=1, le=5, description="Maximum pathway depth"),
    db: Session = Depends(get_db)
):
    """
    Find causal pathways between two nodes.

    Returns all possible pathways from `from_node` to `to_node`
    up to `max_depth` mechanisms deep.

    Useful for:
    - Tracing intervention impacts
    - Understanding causal chains
    - Identifying leverage points
    """
    # TODO: Implement graph traversal algorithm
    # For MVP, return direct connections only
    direct = db.query(Mechanism).filter(
        Mechanism.from_node_id == from_node,
        Mechanism.to_node_id == to_node
    ).all()

    if not direct:
        # Try finding one-hop pathways
        intermediates = db.query(Mechanism).filter(
            Mechanism.from_node_id == from_node
        ).all()

        pathways = []
        for intermediate in intermediates:
            second_hop = db.query(Mechanism).filter(
                Mechanism.from_node_id == intermediate.to_node_id,
                Mechanism.to_node_id == to_node
            ).all()

            for hop in second_hop:
                pathways.append({
                    "pathway_length": 2,
                    "mechanisms": [
                        intermediate.to_dict(),
                        hop.to_dict()
                    ]
                })

        return {
            "from_node": from_node,
            "to_node": to_node,
            "pathways_found": len(pathways),
            "pathways": pathways[:10]  # Limit to 10 pathways
        }

    return {
        "from_node": from_node,
        "to_node": to_node,
        "pathways_found": len(direct),
        "pathways": [{
            "pathway_length": 1,
            "mechanisms": [m.to_dict() for m in direct]
        }]
    }


@router.get("/stats/summary")
def get_stats(db: Session = Depends(get_db)):
    """
    Get summary statistics about the mechanism bank.

    Returns:
    - Total mechanisms
    - Mechanisms by category
    - Mechanisms by direction
    - Evidence quality distribution
    - Total nodes
    """
    total_mechanisms = db.query(Mechanism).count()
    total_nodes = db.query(Node).count()

    # Count by category
    from sqlalchemy import func
    by_category = db.query(
        Mechanism.category,
        func.count(Mechanism.id)
    ).group_by(Mechanism.category).all()

    # Count by direction
    by_direction = db.query(
        Mechanism.direction,
        func.count(Mechanism.id)
    ).group_by(Mechanism.direction).all()

    # Count by evidence quality
    by_evidence = db.query(
        Mechanism.evidence_quality,
        func.count(Mechanism.id)
    ).group_by(Mechanism.evidence_quality).all()

    return {
        "total_mechanisms": total_mechanisms,
        "total_nodes": total_nodes,
        "by_category": {cat: count for cat, count in by_category},
        "by_direction": {dir: count for dir, count in by_direction},
        "by_evidence_quality": {qual: count for qual, count in by_evidence}
    }


# ==========================================
# Utility: Load mechanisms from YAML files
# ==========================================

@router.post("/admin/load-from-yaml")
def load_mechanisms_from_yaml(db: Session = Depends(get_db)):
    """
    Load mechanisms from YAML files in mechanism-bank.

    This is an admin endpoint to populate the database from
    the YAML files generated by the LLM pipeline.

    Returns number of mechanisms loaded.
    """
    mechanism_bank_path = Path(__file__).parent.parent.parent.parent / "mechanism-bank" / "mechanisms"

    if not mechanism_bank_path.exists():
        raise HTTPException(status_code=404, detail="Mechanism bank directory not found")

    loaded_count = 0
    errors = []

    # Walk through all YAML files
    for yaml_file in mechanism_bank_path.rglob("*.yml"):
        try:
            with open(yaml_file, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)

            # Check if mechanism already exists
            existing = db.query(Mechanism).filter(Mechanism.id == data['id']).first()
            if existing:
                continue  # Skip existing mechanisms

            # Create nodes if they don't exist
            from_node = db.query(Node).filter(Node.id == data['from_node']['node_id']).first()
            if not from_node:
                from_node = Node(
                    id=data['from_node']['node_id'],
                    name=data['from_node']['node_name'],
                    node_type='stock',  # Default, can be updated later
                    category=data.get('category', 'unknown')
                )
                db.add(from_node)
                db.flush()  # Flush immediately to avoid duplicate key errors

            to_node = db.query(Node).filter(Node.id == data['to_node']['node_id']).first()
            if not to_node:
                to_node = Node(
                    id=data['to_node']['node_id'],
                    name=data['to_node']['node_name'],
                    node_type='stock',  # Default
                    category=data.get('category', 'unknown')
                )
                db.add(to_node)
                db.flush()  # Flush immediately to avoid duplicate key errors

            # Create mechanism
            mechanism = Mechanism(
                id=data['id'],
                name=data['name'],
                from_node_id=data['from_node']['node_id'],
                to_node_id=data['to_node']['node_id'],
                direction=data['direction'],
                category=data['category'],
                mechanism_pathway=data.get('mechanism_pathway', []),
                evidence_quality=data['evidence']['quality_rating'],
                evidence_n_studies=data['evidence']['n_studies'],
                evidence_primary_citation=data['evidence']['primary_citation'],
                evidence_supporting_citations=data['evidence'].get('supporting_citations'),
                evidence_doi=data['evidence'].get('doi'),
                varies_by_geography=data.get('spatial_variation', {}).get('varies_by_geography', False),
                variation_notes=data.get('spatial_variation', {}).get('variation_notes'),
                relevant_geographies=data.get('spatial_variation', {}).get('relevant_geographies'),
                moderators=data.get('moderators'),
                structural_competency_equity_implications=data.get('structural_competency', {}).get('equity_implications'),
                description=data.get('description', ''),
                version=data.get('version', '1.0'),
                validated_by=data.get('validated_by'),
                llm_extracted_by=data.get('llm_metadata', {}).get('extracted_by'),
                llm_extraction_confidence=data.get('llm_metadata', {}).get('extraction_confidence'),
                llm_prompt_version=data.get('llm_metadata', {}).get('prompt_version')
            )

            db.add(mechanism)
            loaded_count += 1

        except Exception as e:
            errors.append({
                "file": str(yaml_file),
                "error": str(e)
            })

    # Commit all at once
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database commit failed: {e}")

    return {
        "loaded": loaded_count,
        "errors": errors,
        "total_errors": len(errors)
    }
