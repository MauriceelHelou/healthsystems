"""
Centralized Schema Configuration

This file serves as the SINGLE SOURCE OF TRUTH for mechanism schema constants.
All validators, models, and API endpoints should import from here.

Aligned with: mechanism-bank/schemas/mechanism_schema_mvp.json
"""

from typing import Dict, List, Literal, TypedDict
from enum import Enum


# =============================================================================
# CATEGORY DEFINITIONS (DEPRECATED - use Domains instead)
# =============================================================================

class Category(str, Enum):
    """
    DEPRECATED: Use Domain enum instead.

    Mechanism category types representing the primary domain/level of intervention.
    Retained for backward compatibility during migration to domain-based system.
    """
    BUILT_ENVIRONMENT = "built_environment"
    SOCIAL_ENVIRONMENT = "social_environment"
    ECONOMIC = "economic"
    POLITICAL = "political"
    BIOLOGICAL = "biological"
    BEHAVIORAL = "behavioral"
    HEALTHCARE_ACCESS = "healthcare_access"


VALID_CATEGORIES: List[str] = [c.value for c in Category]

CATEGORY_DESCRIPTIONS: Dict[str, str] = {
    "built_environment": "Housing, air quality, neighborhood design, environmental hazards",
    "social_environment": "Social support, stigma, discrimination, community factors",
    "economic": "Employment, poverty, income, financial hardship",
    "political": "Policy interventions, regulations, taxation, enforcement",
    "biological": "Disease pathways, physiological mechanisms, organ systems",
    "behavioral": "Individual behaviors, coping patterns, health-related actions",
    "healthcare_access": "Treatment access, insurance, care integration, providers",
}


# =============================================================================
# DOMAIN DEFINITIONS (NEW - replaces Category)
# =============================================================================

class Domain(str, Enum):
    """
    Domain types representing thematic areas that span ALL 7 scales.

    Domains are root nodes (depth=0) in the hierarchy. A node's domains
    are computed from its ancestry path(s) - nodes can belong to multiple
    domains through DAG parent relationships.

    Note: Domains are NOT a separate tagging system. They ARE the top-level
    nodes in the hierarchy. A node's domain(s) are determined by its root
    ancestors in the `all_ancestors` field.
    """
    HEALTHCARE_SYSTEM = "healthcare_system"
    HOUSING = "housing"
    ECONOMIC_SECURITY = "economic_security"
    EMPLOYMENT_OCCUPATIONAL = "employment_occupational"
    FOOD_SECURITY = "food_security"
    EDUCATION = "education"
    BUILT_ENVIRONMENT_TRANSPORTATION = "built_environment_transportation"
    ENVIRONMENTAL_CLIMATE = "environmental_climate"
    CRIMINAL_JUSTICE = "criminal_justice"
    SOCIAL_ENVIRONMENT = "social_environment"
    BEHAVIORAL_HEALTH = "behavioral_health"
    LONG_TERM_SERVICES_SUPPORTS = "long_term_services_supports"
    MATERNAL_CHILD_HEALTH = "maternal_child_health"
    SPECIALIZED_CLINICAL = "specialized_clinical"
    PUBLIC_HEALTH_INFRASTRUCTURE = "public_health_infrastructure"
    DIGITAL_INFORMATION_ACCESS = "digital_information_access"
    CIVIC_POLITICAL_ENGAGEMENT = "civic_political_engagement"


VALID_DOMAINS: List[str] = [d.value for d in Domain]


class DomainInfo(TypedDict):
    name: str
    description: str
    scale_1_example: str
    scale_7_example: str


DOMAIN_DEFINITIONS: Dict[str, DomainInfo] = {
    "healthcare_system": {
        "name": "Healthcare System",
        "description": "Insurance, providers, access, utilization, outcomes",
        "scale_1_example": "medicaid_expansion_status",
        "scale_7_example": "avoidable_ed_visits"
    },
    "housing": {
        "name": "Housing",
        "description": "Policy, stock, affordability, quality, homelessness",
        "scale_1_example": "rent_control_policy",
        "scale_7_example": "homelessness_rate"
    },
    "economic_security": {
        "name": "Economic Security",
        "description": "Income, poverty, debt, safety net programs",
        "scale_1_example": "minimum_wage_level",
        "scale_7_example": "medical_bankruptcy_rate"
    },
    "employment_occupational": {
        "name": "Employment & Occupational",
        "description": "Labor laws, workplace safety, job quality",
        "scale_1_example": "osha_standards",
        "scale_7_example": "occupational_fatality_rate"
    },
    "food_security": {
        "name": "Food Security",
        "description": "SNAP, food retail, access, nutrition",
        "scale_1_example": "snap_benefit_level",
        "scale_7_example": "malnutrition_hospitalizations"
    },
    "education": {
        "name": "Education",
        "description": "Policy, schools, attainment, child development",
        "scale_1_example": "education_funding_formula",
        "scale_7_example": "school_dropout_rate"
    },
    "built_environment_transportation": {
        "name": "Built Environment & Transportation",
        "description": "Transit, parks, walkability, active transport",
        "scale_1_example": "transit_funding",
        "scale_7_example": "traffic_fatality_rate"
    },
    "environmental_climate": {
        "name": "Environmental & Climate",
        "description": "Pollution, climate, exposures, environmental health",
        "scale_1_example": "clean_air_act_enforcement",
        "scale_7_example": "heat_stroke_deaths"
    },
    "criminal_justice": {
        "name": "Criminal Justice",
        "description": "Sentencing, policing, incarceration, reentry",
        "scale_1_example": "bail_reform_policy",
        "scale_7_example": "recidivism_rate"
    },
    "social_environment": {
        "name": "Social Environment",
        "description": "Discrimination, social support, community cohesion",
        "scale_1_example": "civil_rights_enforcement",
        "scale_7_example": "social_isolation_mortality"
    },
    "behavioral_health": {
        "name": "Behavioral Health",
        "description": "Mental health, substance use, treatment, crisis",
        "scale_1_example": "mental_health_parity_law",
        "scale_7_example": "overdose_mortality"
    },
    "long_term_services_supports": {
        "name": "Long-Term Services & Supports",
        "description": "LTSS, disability, caregiving, aging",
        "scale_1_example": "medicaid_hcbs_waiver",
        "scale_7_example": "nursing_home_mortality"
    },
    "maternal_child_health": {
        "name": "Maternal & Child Health",
        "description": "Pregnancy, birth, child development, pediatrics",
        "scale_1_example": "pregnancy_medicaid",
        "scale_7_example": "infant_mortality"
    },
    "specialized_clinical": {
        "name": "Specialized Clinical",
        "description": "Cancer, kidney, transplant, oral, vision, pain, geriatrics",
        "scale_1_example": "cancer_screening_mandate",
        "scale_7_example": "cancer_mortality"
    },
    "public_health_infrastructure": {
        "name": "Public Health Infrastructure",
        "description": "Funding, departments, surveillance, preparedness",
        "scale_1_example": "public_health_funding",
        "scale_7_example": "outbreak_mortality"
    },
    "digital_information_access": {
        "name": "Digital & Information Access",
        "description": "Broadband, telehealth, digital literacy",
        "scale_1_example": "broadband_subsidy_policy",
        "scale_7_example": "digital_divide_health_disparity"
    },
    "civic_political_engagement": {
        "name": "Civic & Political Engagement",
        "description": "Voting, civic participation, political power",
        "scale_1_example": "voting_rights_law",
        "scale_7_example": "disenfranchisement_health_impact"
    }
}


# Mapping from old Category to new Domain(s)
CATEGORY_TO_DOMAIN_MAPPING: Dict[str, List[str]] = {
    "built_environment": ["housing", "built_environment_transportation", "environmental_climate"],
    "social_environment": ["social_environment"],
    "economic": ["economic_security", "employment_occupational"],
    "political": ["civic_political_engagement"],
    "biological": ["specialized_clinical"],
    "behavioral": ["behavioral_health"],
    "healthcare_access": ["healthcare_system"],
}


# =============================================================================
# EVIDENCE QUALITY GRADES
# =============================================================================

class EvidenceGrade(str, Enum):
    """Evidence quality grades (A, B, C only - no D grade)."""
    A = "A"
    B = "B"
    C = "C"


VALID_EVIDENCE_GRADES: List[str] = [g.value for g in EvidenceGrade]


class EvidenceRequirements(TypedDict):
    min_studies: int
    max_studies: int
    description: str


EVIDENCE_REQUIREMENTS: Dict[str, EvidenceRequirements] = {
    "A": {
        "min_studies": 5,
        "max_studies": 100,
        "description": "Meta-analysis or systematic review with 5+ high-quality studies"
    },
    "B": {
        "min_studies": 3,
        "max_studies": 10,
        "description": "3-4 studies or systematic review with moderate evidence"
    },
    "C": {
        "min_studies": 1,
        "max_studies": 4,
        "description": "1-2 studies or limited/emerging evidence"
    }
}


# =============================================================================
# NODE SCALE DEFINITIONS (1-7 System)
# =============================================================================

class NodeScale(int, Enum):
    """
    Node scale levels representing causal hierarchy.
    Lower numbers = more upstream/structural
    Higher numbers = more downstream/proximal to outcomes
    """
    STRUCTURAL_DETERMINANTS = 1
    BUILT_ENVIRONMENT = 2
    INSTITUTIONAL_INFRASTRUCTURE = 3
    INDIVIDUAL_CONDITIONS = 4
    BEHAVIORS_PSYCHOSOCIAL = 5
    INTERMEDIATE_PATHWAYS = 6
    CRISIS_ENDPOINTS = 7


VALID_SCALES: List[int] = [s.value for s in NodeScale]

SCALE_DESCRIPTIONS: Dict[int, Dict[str, str]] = {
    1: {
        "name": "Structural Determinants",
        "description": "Federal/state policy, systemic factors",
        "causal_distance": "Decades",
        "examples": "Tax policy, federal regulations, systemic racism"
    },
    2: {
        "name": "Built Environment & Infrastructure",
        "description": "Physical environment, regional factors",
        "causal_distance": "Years to decades",
        "examples": "Housing quality, air pollution, neighborhood design"
    },
    3: {
        "name": "Institutional Infrastructure",
        "description": "Organizations, facilities, local systems",
        "causal_distance": "Months to years",
        "examples": "Healthcare systems, schools, workplaces"
    },
    4: {
        "name": "Individual/Household Conditions",
        "description": "Material conditions, socioeconomic factors",
        "causal_distance": "Weeks to months",
        "examples": "Income, employment, housing stability"
    },
    5: {
        "name": "Individual Behaviors & Psychosocial",
        "description": "Health behaviors, psychological factors",
        "causal_distance": "Days to weeks",
        "examples": "Diet, exercise, substance use, stress"
    },
    6: {
        "name": "Intermediate Pathways",
        "description": "Clinical measures, disease prevalence",
        "causal_distance": "Hours to days",
        "examples": "Blood pressure, inflammation, biomarkers"
    },
    7: {
        "name": "Crisis Endpoints",
        "description": "Mortality, emergency care, acute outcomes",
        "causal_distance": "Immediate",
        "examples": "Death, hospitalization, ED visits"
    }
}


# =============================================================================
# NODE TYPE DEFINITIONS
# =============================================================================

class NodeType(str, Enum):
    """Types of nodes in the causal graph."""
    STOCK = "stock"
    PROXY_INDEX = "proxy_index"
    CRISIS_ENDPOINT = "crisis_endpoint"


VALID_NODE_TYPES: List[str] = [t.value for t in NodeType]


# =============================================================================
# MODERATOR DEFINITIONS
# =============================================================================

class ModeratorDirection(str, Enum):
    """How a moderator affects the mechanism."""
    STRENGTHENS = "strengthens"
    WEAKENS = "weakens"
    U_SHAPED = "u_shaped"


class ModeratorStrength(str, Enum):
    """Qualitative assessment of moderator strength."""
    WEAK = "weak"
    MODERATE = "moderate"
    STRONG = "strong"


VALID_MODERATOR_DIRECTIONS: List[str] = [d.value for d in ModeratorDirection]
VALID_MODERATOR_STRENGTHS: List[str] = [s.value for s in ModeratorStrength]


# =============================================================================
# STRUCTURAL COMPETENCY DEFINITIONS
# =============================================================================

class RootCauseLevel(str, Enum):
    """Level of structural analysis for mechanism."""
    POLICY = "policy"
    ECONOMIC_SYSTEM = "economic_system"
    SPATIAL_ARRANGEMENT = "spatial_arrangement"
    INSTITUTIONAL = "institutional"
    INTERPERSONAL = "interpersonal"


VALID_ROOT_CAUSE_LEVELS: List[str] = [r.value for r in RootCauseLevel]


# =============================================================================
# LLM EXTRACTION CONFIDENCE
# =============================================================================

class ExtractionConfidence(str, Enum):
    """LLM extraction confidence levels."""
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


VALID_EXTRACTION_CONFIDENCE: List[str] = [c.value for c in ExtractionConfidence]


# =============================================================================
# VALIDATION HELPER FUNCTIONS
# =============================================================================

def is_valid_category(category: str) -> bool:
    """Check if category is valid."""
    return category in VALID_CATEGORIES


def is_valid_evidence_grade(grade: str) -> bool:
    """Check if evidence grade is valid."""
    return grade in VALID_EVIDENCE_GRADES


def is_valid_scale(scale: int) -> bool:
    """Check if scale is valid (1-7)."""
    return scale in VALID_SCALES


def get_evidence_requirements(grade: str) -> EvidenceRequirements:
    """Get evidence requirements for a grade."""
    return EVIDENCE_REQUIREMENTS.get(grade, EVIDENCE_REQUIREMENTS["C"])


def validate_study_count_for_grade(grade: str, n_studies: int) -> bool:
    """Check if study count is appropriate for evidence grade."""
    if grade not in EVIDENCE_REQUIREMENTS:
        return False
    req = EVIDENCE_REQUIREMENTS[grade]
    return req["min_studies"] <= n_studies <= req["max_studies"]


# =============================================================================
# CATEGORY-SCALE RELATIONSHIPS
# =============================================================================

# Typical scale ranges for each category
CATEGORY_TYPICAL_SCALES: Dict[str, List[int]] = {
    "political": [1, 2],
    "built_environment": [2, 3],
    "economic": [3, 4],
    "social_environment": [3, 4, 5],
    "healthcare_access": [3, 4],
    "behavioral": [4, 5],
    "biological": [5, 6, 7],
}

# Related category pairs (mechanisms often span these)
RELATED_CATEGORY_PAIRS: List[tuple] = [
    ("built_environment", "social_environment"),
    ("built_environment", "behavioral"),
    ("economic", "social_environment"),
    ("economic", "healthcare_access"),
    ("social_environment", "behavioral"),
    ("healthcare_access", "biological"),
    ("behavioral", "biological"),
    ("political", "economic"),
    ("political", "healthcare_access"),
]


def are_categories_related(cat1: str, cat2: str) -> bool:
    """Check if two categories are typically related."""
    return (cat1, cat2) in RELATED_CATEGORY_PAIRS or (cat2, cat1) in RELATED_CATEGORY_PAIRS


# =============================================================================
# DOMAIN VALIDATION HELPER FUNCTIONS
# =============================================================================

def is_valid_domain(domain: str) -> bool:
    """Check if domain is valid."""
    return domain in VALID_DOMAINS


def get_domain_info(domain: str) -> DomainInfo:
    """Get domain information."""
    return DOMAIN_DEFINITIONS.get(domain, {
        "name": domain,
        "description": "Unknown domain",
        "scale_1_example": "",
        "scale_7_example": ""
    })


def category_to_domains(category: str) -> List[str]:
    """
    Map a deprecated category to new domain(s).

    Args:
        category: Old category value

    Returns:
        List of new domain values
    """
    return CATEGORY_TO_DOMAIN_MAPPING.get(category, [])


def domains_to_category(domains: List[str]) -> str:
    """
    Map domains back to the best-matching deprecated category.

    Used for backward compatibility during migration.

    Args:
        domains: List of domain values

    Returns:
        Best matching old category value
    """
    if not domains:
        return "behavioral"  # Default

    # Reverse the mapping
    domain_to_category = {}
    for cat, dom_list in CATEGORY_TO_DOMAIN_MAPPING.items():
        for d in dom_list:
            domain_to_category[d] = cat

    # Return the first matching category
    for domain in domains:
        if domain in domain_to_category:
            return domain_to_category[domain]

    return "behavioral"  # Default fallback


# =============================================================================
# HIERARCHY LEVEL DEFINITIONS
# =============================================================================

class HierarchyLevel(str, Enum):
    """
    Hierarchy level for mechanisms.

    Defines at what abstraction level the mechanism is defined.
    """
    LEAF = "leaf"        # Connects specific (child) nodes
    PARENT = "parent"    # Connects abstract/general (parent) nodes
    CROSS = "cross"      # Spans hierarchy levels


VALID_HIERARCHY_LEVELS: List[str] = [h.value for h in HierarchyLevel]


def is_valid_hierarchy_level(level: str) -> bool:
    """Check if hierarchy level is valid."""
    return level in VALID_HIERARCHY_LEVELS
