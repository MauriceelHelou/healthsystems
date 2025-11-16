"""
Database models for causal mechanisms.
"""

from sqlalchemy import Column, String, Float, Integer, DateTime, JSON, Text
from sqlalchemy.sql import func
from datetime import datetime

from models.database import Base


class Mechanism(Base):
    """
    Causal mechanism model.

    Represents a structural pathway from intervention to health outcome.
    """

    __tablename__ = "mechanisms"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    category = Column(String, nullable=False, index=True)
    mechanism_type = Column(String, nullable=False)

    # Effect size information
    effect_size_measure = Column(String)
    effect_size_point = Column(Float)
    effect_size_ci_lower = Column(Float)
    effect_size_ci_upper = Column(Float)
    effect_size_unit = Column(String)

    # Evidence metadata
    evidence_quality = Column(String)  # A, B, C rating
    evidence_n_studies = Column(Integer)
    evidence_citation = Column(Text)

    # Versioning
    version = Column(String, default="1.0")
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    validated_by = Column(JSON)  # List of validator initials

    # Additional metadata
    description = Column(Text)
    assumptions = Column(JSON)
    limitations = Column(JSON)
    moderators = Column(JSON)  # Contextual factors that modify effect

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<Mechanism {self.id}: {self.name}>"
