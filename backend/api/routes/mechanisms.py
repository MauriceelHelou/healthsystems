"""
API routes for mechanisms (CRUD operations).

Provides REST API for accessing and managing causal mechanisms.
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, selectinload
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
    from_node_scale: int  # Scale of from_node (1-7)
    to_node_id: str
    to_node_name: str
    to_node_scale: int  # Scale of to_node (1-7)
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
    limit: int = Query(100, le=5000, description="Maximum number of results"),
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
    query = db.query(Mechanism).options(
        selectinload(Mechanism.from_node),
        selectinload(Mechanism.to_node)
    )

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
            from_node_scale=m.from_node.scale if m.from_node else 4,  # Default to scale 4 if node not found
            to_node_id=m.to_node_id,
            to_node_name=m.to_node.name if m.to_node else m.to_node_id,
            to_node_scale=m.to_node.scale if m.to_node else 4,  # Default to scale 4 if node not found
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


# ==========================================
# NOTE: Deprecated /search/pathway endpoint removed
# ==========================================
# The old 2-hop limited pathway search endpoint has been removed.
# Use the new full-featured pathfinding endpoint instead:
#   POST /api/nodes/pathfinding
# Located in: backend/api/routes/nodes.py
# Features:
#   - Full graph traversal (up to 8 hops)
#   - Multiple algorithms (shortest, strongest_evidence, all_simple)
#   - Category filtering
#   - NetworkX-powered graph operations
# ==========================================


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

def get_node_scale_from_category(category: str, node_name: str = "") -> int:
    """
    Determine node scale based on category and node name patterns.

    7-scale taxonomy mapping:
    - political -> 1 (structural determinants - policy)
    - built_environment -> 2 (built environment & infrastructure)
    - economic, social_services -> 3 (institutional infrastructure)
    - social_environment, economic_individual -> 4 (individual/household conditions)
    - behavioral, psychosocial -> 5 (individual behaviors & psychosocial)
    - healthcare_access -> varies by node type (see below)
    - clinical -> 6 (intermediate pathways)
    - biological, crisis -> 7 (crisis endpoints)

    Pattern-based overrides (applied regardless of category):
    - Treatment/medication nodes -> Scale 5 (individual behaviors)
    - Infrastructure/facility nodes -> Scale 3 (institutional)
    """
    if node_name:
        name_lower = node_name.lower()

        # Treatment/medication keywords → Scale 5 (individual behaviors)
        # Check these FIRST regardless of category - treatments are always Scale 5
        treatment_keywords = [
            'gabapentin', 'naltrexone', 'disulfiram', 'acamprosate',
            'baclofen', 'topiramate', 'pharmacotherapy', 'medication',
            ' therapy', 'counseling', 'detox protocol', 'rehab',
            'recovery program', 'maud', ' mat '
        ]
        # More specific treatment patterns that should be Scale 5
        if any(kw in name_lower for kw in treatment_keywords):
            return 5
        # "treatment" alone needs more context - check it's not infrastructure
        if 'treatment' in name_lower:
            infrastructure_check = ['facility', 'center', 'capacity', 'availability', 'density']
            if not any(kw in name_lower for kw in infrastructure_check):
                return 5

        # Infrastructure/facilities → Scale 3 (institutional)
        # Only for healthcare_access category
        if category == 'healthcare_access':
            infrastructure_keywords = [
                'facility', 'clinic', 'center', 'density', 'capacity',
                'availability', 'provider', 'workforce', 'bed', 'unit',
                'access', 'coverage', 'insurance'
            ]
            if any(kw in name_lower for kw in infrastructure_keywords):
                return 3
            # Default healthcare_access without specific patterns → Scale 6
            return 6

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

    return scale_mapping.get(category, 4)  # Default to scale 4


@router.post("/admin/load-nodes-from-yaml")
def load_nodes_from_yaml(db: Session = Depends(get_db)):
    """
    Load node definitions from mechanism-bank/nodes/*.yml files.

    This should be called BEFORE loading mechanisms, as mechanisms
    reference nodes by ID. Allows explicit node metadata including
    scale, domain, type, baseline values, and data sources.

    Returns number of nodes loaded/updated.
    """
    nodes_dir = Path(__file__).parent.parent.parent.parent / "mechanism-bank" / "nodes"

    if not nodes_dir.exists():
        # Create directory if it doesn't exist
        nodes_dir.mkdir(parents=True, exist_ok=True)
        return {
            "loaded": 0,
            "updated": 0,
            "errors": [],
            "message": "nodes directory created but empty"
        }

    loaded_count = 0
    updated_count = 0
    errors = []

    for yaml_file in nodes_dir.glob("*.yml"):
        try:
            with open(yaml_file, 'r', encoding='utf-8') as f:
                node_data = yaml.safe_load(f)

            # Validate required fields
            required_fields = ['id', 'name', 'scale', 'category']
            for field in required_fields:
                if field not in node_data:
                    raise ValueError(f"Missing required field: {field}")

            # Validate scale range
            if not (1 <= node_data['scale'] <= 7):
                raise ValueError(f"scale must be between 1 and 7, got {node_data['scale']}")

            # Check if node exists
            node = db.query(Node).filter(Node.id == node_data['id']).first()

            if node:
                # Update existing node
                node.name = node_data['name']
                node.scale = node_data['scale']
                node.category = node_data['category']
                node.node_type = node_data.get('type', node.node_type)
                node.unit = node_data.get('unit')
                node.description = node_data.get('description')
                node.measurement_method = node_data.get('measurement_method')
                node.typical_range = node_data.get('typical_range')

                # Parse data_sources if present
                if 'data_sources' in node_data:
                    node.data_sources = node_data['data_sources']

                updated_count += 1
            else:
                # Create new node
                node = Node(
                    id=node_data['id'],
                    name=node_data['name'],
                    scale=node_data['scale'],
                    category=node_data['category'],
                    node_type=node_data.get('type', 'stock'),
                    unit=node_data.get('unit'),
                    description=node_data.get('description'),
                    measurement_method=node_data.get('measurement_method'),
                    typical_range=node_data.get('typical_range'),
                    data_sources=node_data.get('data_sources')
                )
                db.add(node)
                loaded_count += 1

        except Exception as e:
            errors.append({
                "file": str(yaml_file),
                "error": str(e)
            })

    # Commit all changes
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database commit failed: {e}")

    return {
        "loaded": loaded_count,
        "updated": updated_count,
        "errors": errors,
        "total_errors": len(errors)
    }


@router.post("/admin/load-from-yaml")
def load_mechanisms_from_yaml(db: Session = Depends(get_db)):
    """
    Load mechanisms from YAML files in mechanism-bank.

    This is an admin endpoint to populate the database from
    the YAML files generated by the LLM pipeline.

    Note: If using dedicated node YAMLs, call /admin/load-nodes-from-yaml first.
    This endpoint will still auto-create nodes if they don't exist, but with
    inferred scale values based on category.

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
                category = data.get('category', 'unknown')
                from_node_name = data['from_node']['node_name']
                from_node = Node(
                    id=data['from_node']['node_id'],
                    name=from_node_name,
                    node_type='stock',  # Default, can be updated later
                    category=category,
                    scale=get_node_scale_from_category(category, from_node_name)
                )
                db.add(from_node)
                db.flush()  # Flush immediately to avoid duplicate key errors

            to_node = db.query(Node).filter(Node.id == data['to_node']['node_id']).first()
            if not to_node:
                category = data.get('category', 'unknown')
                to_node_name = data['to_node']['node_name']
                to_node = Node(
                    id=data['to_node']['node_id'],
                    name=to_node_name,
                    node_type='stock',  # Default
                    category=category,
                    scale=get_node_scale_from_category(category, to_node_name)
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
