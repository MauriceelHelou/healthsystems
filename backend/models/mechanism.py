"""
Database models for causal mechanisms (MVP - Topology & Direction).

MVP Scope: Focuses on network topology and directionality.
Phase 2: Will add quantitative effect sizes and meta-analysis data.

Hierarchy Support:
- Nodes can have parent-child relationships (DAG structure)
- Domains are root nodes (depth=0) in the hierarchy
- Mechanisms reference nodes that must exist in the node bank
"""

from sqlalchemy import Column, String, Integer, DateTime, JSON, Text, Boolean, ForeignKey, Float, CheckConstraint, Table, UniqueConstraint, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
from typing import List, Optional

from models.database import Base


# Junction table for node hierarchy (DAG support - nodes can have multiple parents)
node_hierarchy = Table(
    'node_hierarchy',
    Base.metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('parent_node_id', String, ForeignKey('nodes.id', ondelete='CASCADE'), nullable=False),
    Column('child_node_id', String, ForeignKey('nodes.id', ondelete='CASCADE'), nullable=False),
    Column('relationship_type', String, default='contains'),  # contains, specializes, contextualizes
    Column('order_index', Integer, default=0),  # For ordering siblings
    Column('created_at', DateTime, server_default=func.now()),
    UniqueConstraint('parent_node_id', 'child_node_id', name='unique_parent_child'),
    Index('ix_node_hierarchy_parent', 'parent_node_id'),
    Index('ix_node_hierarchy_child', 'child_node_id'),
)


class Node(Base):
    """
    Nodes in the causal network (stocks in stock-flow paradigm).

    Represents measurable constructs like:
    - Real stocks: eviction_rate, healthcare_continuity, housing_quality
    - Proxy indices: health_access_index, economic_security_index
    - Crisis endpoints: mortality_rate, ed_utilization

    Hierarchy:
    - Nodes can have parent-child relationships (DAG structure)
    - depth=0 nodes are "domains" (root-level organizational nodes)
    - A node's domains are computed from its root ancestors
    """

    __tablename__ = "nodes"

    id = Column(String, primary_key=True, index=True)  # snake_case node ID
    name = Column(String, nullable=False)  # Human-readable name
    node_type = Column(String, nullable=False)  # stock, proxy_index, crisis_endpoint

    # Measurement details
    unit = Column(String)  # e.g., "per 100 renter households", "index 0-100"
    measurement_method = Column(Text)  # How to measure this node
    typical_range = Column(String)  # e.g., "0-50", "0-100"

    # Data source mapping
    data_sources = Column(JSON)  # List of census variables, CDC metrics, etc.

    # Scale (7-level taxonomy: 1=policy, 2=built_env, 3=institutional, 4=individual, 5=behavioral, 6=intermediate, 7=crisis)
    scale = Column(Integer, nullable=False, index=True)

    # Category (deprecated - use domains computed from hierarchy ancestry)
    # Retained for backward compatibility with existing data and APIs
    category = Column(String, nullable=True, index=True, default='default')

    # === HIERARCHY FIELDS (NEW) ===
    # Depth in hierarchy: 0 = root/domain node, 1+ = nested
    depth = Column(Integer, default=0, index=True)

    # Primary path for efficient ancestry queries: "root_id/parent_id/this_id"
    primary_path = Column(String, index=True)

    # All ancestor IDs (from ALL parent paths in DAG) - denormalized for query efficiency
    all_ancestors = Column(JSON, default=list)  # ["grandparent_id", "parent1_id", "parent2_id"]

    # Is this a grouping/container node (abstract) vs leaf/measurable node?
    is_grouping_node = Column(Boolean, default=False, index=True)

    # Display ordering within parent
    display_order = Column(Integer, default=0)

    # Metadata
    description = Column(Text)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # Table constraints
    # Note: Individual column indexes are created via index=True on each column
    # Only composite indexes are defined here
    __table_args__ = (
        CheckConstraint('scale >= 1 AND scale <= 7', name='scale_range'),
        CheckConstraint('depth >= 0', name='depth_non_negative'),
        Index('ix_nodes_scale_depth', 'scale', 'depth'),
    )

    # Relationships
    mechanisms_from = relationship("Mechanism", foreign_keys="Mechanism.from_node_id", back_populates="from_node")
    mechanisms_to = relationship("Mechanism", foreign_keys="Mechanism.to_node_id", back_populates="to_node")

    # Hierarchy relationships (via junction table)
    parents = relationship(
        "Node",
        secondary=node_hierarchy,
        primaryjoin="Node.id == node_hierarchy.c.child_node_id",
        secondaryjoin="Node.id == node_hierarchy.c.parent_node_id",
        backref="children"
    )

    @property
    def domains(self) -> List[str]:
        """
        Return domain IDs (root ancestors at depth=0).

        Since this is a DAG, a node can belong to multiple domains
        through different parent paths.
        """
        if self.depth == 0:
            return [self.id]  # Root node is its own domain
        if not self.all_ancestors:
            return []
        # Filter ancestors to only include root nodes (depth=0)
        # Note: In practice, root nodes are identified by their position in all_ancestors
        # The first element(s) of each path are the root(s)
        # For efficiency, we store root IDs at the start of all_ancestors
        return [a for a in (self.all_ancestors or []) if '/' not in a]

    @property
    def is_root(self) -> bool:
        """Check if this is a root/domain node (no parents)."""
        return self.depth == 0

    @property
    def is_leaf(self) -> bool:
        """Check if this is a leaf node (no children)."""
        return not self.children if hasattr(self, 'children') else True

    @property
    def parent_ids(self) -> List[str]:
        """Get all parent node IDs."""
        return [p.id for p in self.parents] if self.parents else []

    @property
    def child_ids(self) -> List[str]:
        """Get all child node IDs."""
        return [c.id for c in self.children] if hasattr(self, 'children') and self.children else []

    def __repr__(self):
        return f"<Node {self.id}: {self.name} (depth={self.depth})>"


class Mechanism(Base):
    """
    Causal mechanism model (MVP - Topology & Direction Only).

    Represents a directed causal pathway from one node to another.
    MVP focuses on WHAT connects and HOW (direction), not HOW MUCH (effect size).
    """

    __tablename__ = "mechanisms"

    # Primary identification
    id = Column(String, primary_key=True, index=True)  # from_node_id_to_to_node_id
    name = Column(String, nullable=False)  # Human-readable name

    # Topology: FROM -> TO relationship
    from_node_id = Column(String, ForeignKey("nodes.id"), nullable=False, index=True)
    to_node_id = Column(String, ForeignKey("nodes.id"), nullable=False, index=True)

    # Direction: positive (increase -> increase) or negative (increase -> decrease)
    direction = Column(String, nullable=False)  # 'positive' or 'negative'

    # Category (deprecated - use domains computed from node ancestry)
    category = Column(String, nullable=False, index=True)
    # built_environment, social_environment, economic, political, healthcare_access, biological, behavioral

    # Hierarchy level: what abstraction level this mechanism operates at
    # - 'leaf': connects specific/detailed nodes (default)
    # - 'parent': connects abstract/general nodes
    # - 'cross': spans hierarchy levels (abstract -> specific or vice versa)
    hierarchy_level = Column(String, default='leaf', index=True)

    # Mechanism pathway (step-by-step description)
    mechanism_pathway = Column(JSON)  # List of strings describing causal steps

    # Evidence (MVP: qualitative assessment)
    evidence_quality = Column(String, nullable=False)  # A, B, or C rating
    evidence_n_studies = Column(Integer, nullable=False)  # Number of supporting studies
    evidence_primary_citation = Column(Text, nullable=False)  # Chicago-style citation
    evidence_supporting_citations = Column(JSON)  # Additional citations
    evidence_doi = Column(String)  # DOI of primary citation

    # Spatial variation (MVP: qualitative flags)
    varies_by_geography = Column(Boolean, default=False)
    variation_notes = Column(Text)  # Qualitative description of geographic variation
    relevant_geographies = Column(JSON)  # List of geographic contexts studied

    # Moderators (MVP: qualitative, not quantified)
    moderators = Column(JSON)  # List of {name, direction, strength, description}

    # Structural competency
    structural_competency_root_cause = Column(String)  # policy, economic_system, spatial_arrangement, etc.
    structural_competency_avoids_victim_blaming = Column(Boolean, default=True)
    structural_competency_equity_implications = Column(Text)

    # Versioning
    version = Column(String, default="1.0")
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    validated_by = Column(JSON)  # List of validator initials

    # LLM metadata (for mechanisms extracted by LLM)
    llm_extracted_by = Column(String)  # Model name
    llm_extraction_date = Column(DateTime)
    llm_extraction_confidence = Column(String)  # high, medium, low
    llm_prompt_version = Column(String)

    # Additional metadata
    description = Column(Text, nullable=False)
    assumptions = Column(JSON)
    limitations = Column(JSON)

    # Timestamps
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # Relationships
    from_node = relationship("Node", foreign_keys=[from_node_id], back_populates="mechanisms_from")
    to_node = relationship("Node", foreign_keys=[to_node_id], back_populates="mechanisms_to")

    def __repr__(self):
        return f"<Mechanism {self.id}: {self.from_node_id} -> {self.to_node_id} ({self.direction})>"

    def to_dict(self):
        """Convert mechanism to dictionary for API responses"""
        return {
            "id": self.id,
            "name": self.name,
            "from_node": {
                "node_id": self.from_node_id,
                "node_name": self.from_node.name if self.from_node else None
            },
            "to_node": {
                "node_id": self.to_node_id,
                "node_name": self.to_node.name if self.to_node else None
            },
            "direction": self.direction,
            "category": self.category,
            "hierarchy_level": self.hierarchy_level or "leaf",
            "mechanism_pathway": self.mechanism_pathway,
            "evidence": {
                "quality_rating": self.evidence_quality,
                "n_studies": self.evidence_n_studies,
                "primary_citation": self.evidence_primary_citation,
                "supporting_citations": self.evidence_supporting_citations,
                "doi": self.evidence_doi
            },
            "spatial_variation": {
                "varies_by_geography": self.varies_by_geography,
                "variation_notes": self.variation_notes,
                "relevant_geographies": self.relevant_geographies
            } if self.varies_by_geography else None,
            "moderators": self.moderators,
            "structural_competency": {
                "root_cause_level": self.structural_competency_root_cause,
                "avoids_victim_blaming": self.structural_competency_avoids_victim_blaming,
                "equity_implications": self.structural_competency_equity_implications
            } if self.structural_competency_equity_implications else None,
            "description": self.description,
            "version": self.version,
            "last_updated": self.last_updated.isoformat() if self.last_updated else None,
            "validated_by": self.validated_by
        }


class GeographicContext(Base):
    """
    Geographic context for mechanism activation.

    Represents policy environment, demographics, and baseline conditions
    that affect which mechanisms are active and how strong they are.
    """

    __tablename__ = "geographic_contexts"

    # Identification
    id = Column(String, primary_key=True, index=True)  # e.g., "boston_ma", "rural_mississippi"
    name = Column(String, nullable=False)  # Human-readable name
    geography_type = Column(String, nullable=False)  # city, county, state, region

    # Geographic identifiers
    fips_code = Column(String)  # FIPS code for counties/states
    census_tract = Column(String)  # Census tract if applicable
    state = Column(String, index=True)
    county = Column(String)

    # Policy environment
    medicaid_expansion = Column(Boolean)  # Did state expand Medicaid?
    medicaid_eligibility_threshold = Column(Integer)  # % FPL
    housing_code_enforcement_strength = Column(String)  # weak, moderate, strong
    rental_assistance_availability = Column(String)  # Description of programs
    minimum_wage = Column(Float)  # Local minimum wage

    # Demographics (baseline)
    population = Column(Integer)
    poverty_rate = Column(Float)  # %
    median_income = Column(Float)
    uninsurance_rate = Column(Float)  # %
    racial_composition = Column(JSON)  # {white: %, black: %, hispanic: %, etc.}

    # Baseline health outcomes
    baseline_mortality_rate = Column(Float)  # per 100,000
    baseline_asthma_rate = Column(Float)  # %
    baseline_diabetes_rate = Column(Float)  # %
    baseline_ed_utilization = Column(Float)  # visits per 1000

    # Built environment
    housing_quality_index = Column(Float)  # 0-100 scale
    air_quality_index = Column(Float)  # AQI
    walkability_index = Column(Float)  # 0-100 scale

    # Data sources
    data_year = Column(Integer)  # Year of data
    data_sources = Column(JSON)  # List of data sources used

    # Metadata
    description = Column(Text)
    notes = Column(Text)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<GeographicContext {self.id}: {self.name}>"

    def to_dict(self):
        """Convert geographic context to dictionary"""
        return {
            "id": self.id,
            "name": self.name,
            "geography_type": self.geography_type,
            "state": self.state,
            "county": self.county,
            "policy_environment": {
                "medicaid_expansion": self.medicaid_expansion,
                "medicaid_eligibility_threshold": self.medicaid_eligibility_threshold,
                "housing_code_enforcement_strength": self.housing_code_enforcement_strength,
                "minimum_wage": self.minimum_wage
            },
            "demographics": {
                "population": self.population,
                "poverty_rate": self.poverty_rate,
                "median_income": self.median_income,
                "uninsurance_rate": self.uninsurance_rate,
                "racial_composition": self.racial_composition
            },
            "baseline_health": {
                "mortality_rate": self.baseline_mortality_rate,
                "asthma_rate": self.baseline_asthma_rate,
                "diabetes_rate": self.baseline_diabetes_rate,
                "ed_utilization": self.baseline_ed_utilization
            },
            "built_environment": {
                "housing_quality_index": self.housing_quality_index,
                "air_quality_index": self.air_quality_index,
                "walkability_index": self.walkability_index
            },
            "data_year": self.data_year
        }
