"""
Scale inference utility for node classification.
Based on NODE_SYSTEM_DEFINITIONS.md 7-scale taxonomy.

This module provides keyword-based scale inference for nodes that don't have
explicit scale assignments. The patterns are designed to match common node
naming conventions and classify them into the correct scale.

Scale Definitions:
- Scale 1: Structural Determinants - Federal/state policy, regulations
- Scale 2: Built Environment - Physical infrastructure, geographic features
- Scale 3: Institutional - Healthcare facilities, workforce, service capacity
- Scale 4: Individual/Household - Lived conditions, socioeconomic status
- Scale 5: Behaviors/Psychosocial - Health behaviors, mental health, coping
- Scale 6: Intermediate Pathways - Clinical measures, biomarkers, utilization
- Scale 7: Crisis Endpoints - Mortality, hospitalization, acute outcomes
"""

from typing import Optional

# Scale 7: Crisis Endpoints - mortality, hospitalization, acute outcomes
SCALE_7_PATTERNS = [
    # Mortality patterns
    'mortality', 'death', 'fatality', 'fatal', 'deaths_per',
    # Hospitalization patterns
    'hospitalization', 'hospital_admission', 'ed_visit', 'emergency_department',
    'er_visit', 'inpatient', 'readmission',
    # Acute events
    'overdose', 'suicide', 'homicide', 'drowning', 'poisoning',
    'crisis', 'acute_', 'severe_',
    # Criminal justice crisis
    'incarceration_rate', 'jail_admission', 'prison_admission',
    # Specific disease endpoints
    'cirrhosis', 'hepatitis_hospitalization', 'pancreatitis',
    'stroke', 'heart_attack', 'myocardial_infarction', 'heart_failure',
    'cardiomyopathy', 'cardiac_arrest',
    # Birth outcomes
    'preterm_birth', 'low_birthweight', 'infant_mortality', 'maternal_mortality',
    'stillbirth', 'neonatal_mortality',
    # Infections/acute illness
    'sepsis', 'infection_hospitalization',
    # Injuries
    'injury_hospitalization', 'trauma_admission',
]

# Scale 6: Intermediate Pathways - clinical measures, biomarkers, utilization
SCALE_6_PATTERNS = [
    # Clinical diagnoses (not acute)
    'diagnosis', 'diagnosed',
    # Clinical prevalence (specific disease states, not behavioral)
    'diabetes_prevalence', 'hypertension_prevalence', 'copd_prevalence',
    'asthma_prevalence', 'heart_disease_prevalence', 'obesity_prevalence',
    # Disease management
    'control', 'controlled', 'management', 'managed',
    # Biomarkers
    'biomarker', 'ggt', 'mcv', 'cdt', 'ast_alt', 'hba1c', 'a1c',
    'ldl', 'hdl', 'triglyceride', 'creatinine', 'egfr',
    # Treatment outcomes
    'withdrawal_severity', 'craving', 'withdrawal',
    'treatment_completion', 'abstinence_rate', 'recovery_rate',
    'remission', 'relapse_rate',
    # Vital signs/clinical measures
    'blood_pressure', 'cholesterol', 'glucose', 'bmi',
    'hypertension_control', 'diabetes_control',
    # Healthcare utilization (non-emergency)
    'screening_rate', 'utilization', 'visit_rate',
    'immunization', 'vaccination', 'preventive_care',
]

# Scale 5: Behaviors/Psychosocial - health behaviors, adherence, coping
SCALE_5_PATTERNS = [
    # Medication/treatment adherence
    'adherence', 'compliance', 'nonadherence', 'noncompliance',
    # Substance use behaviors and disorders
    'drinking_behavior', 'smoking_behavior', 'tobacco_use', 'cannabis_use',
    'drug_use', 'substance_use', 'binge_drinking', 'heavy_drinking',
    'alcohol_use_disorder', 'substance_abuse', 'nicotine_dependence',
    # Physical activity
    'physical_activity', 'sedentary', 'exercise', 'active_transport',
    # Diet behaviors
    'diet_quality', 'nutrition', 'fruit_vegetable', 'sugar_intake',
    'fast_food', 'healthy_eating',
    # Psychological factors
    'coping', 'self_efficacy', 'expectancy', 'motivation',
    'stigma', 'help_seeking', 'treatment_seeking',
    'health_literacy', 'patient_activation',
    # Mental health conditions (non-crisis behavioral)
    'anxiety_disorder', 'depression_screening', 'ptsd_prevalence',
    'anxiety_prevalence', 'depression_prevalence',
    'stress_level', 'psychological_distress',
    # Sleep
    'sleep_quality', 'insomnia',
]

# Scale 4: Individual/Household - lived conditions, exposures
SCALE_4_PATTERNS = [
    # Economic conditions
    'household_income', 'poverty_rate', 'wealth', 'net_worth',
    'income_inequality', 'gini',
    # Housing
    'housing_cost', 'rent_burden', 'eviction', 'homelessness',
    'housing_instability', 'crowding',
    # Food security
    'food_insecurity', 'food_security', 'hunger',
    # Insurance/coverage
    'uninsured', 'insurance_status', 'coverage_rate', 'underinsured',
    # Social conditions
    'social_isolation', 'social_support', 'loneliness',
    'social_cohesion', 'community_trust',
    # Trauma/adversity
    'aces', 'adverse_childhood', 'childhood_trauma',
    # Employment
    'employment_status', 'job_loss', 'unemployment_rate',
    'underemployment', 'job_insecurity',
    # Discrimination
    'discrimination', 'racism', 'segregation',
    # Financial stress
    'debt', 'bankruptcy', 'financial_stress', 'medical_debt',
    # Education level
    'education_level', 'educational_attainment', 'high_school_completion',
]

# Scale 3: Institutional - facilities, workforce, capacity
SCALE_3_PATTERNS = [
    # Facility density/availability
    'facility_density', 'clinic_density', 'hospital_density',
    'provider_density', 'per_capita',
    # Capacity
    'capacity', 'beds_per', 'slots_per', 'treatment_capacity',
    # Workforce
    'workforce', 'provider_ratio', 'specialist_availability',
    'physician_density', 'nurse_density',
    # Service availability
    'program_coverage', 'service_availability',
    'treatment_availability', 'mat_availability',
    # Access barriers
    'waitlist', 'wait_time', 'shortage', 'desert',
    # Institutional quality
    'accreditation', 'quality_score',
]

# Scale 2: Built Environment - physical infrastructure
SCALE_2_PATTERNS = [
    # Alcohol/substance environment
    'outlet_density', 'bar_density', 'liquor_store', 'alcohol_outlet',
    # Transportation infrastructure
    'walkability', 'bike_lane', 'transit_access', 'public_transit',
    'sidewalk', 'crosswalk',
    # Green space
    'green_space', 'park_access', 'tree_canopy', 'recreation',
    # Environmental quality
    'air_quality', 'air_pollution', 'pm25', 'ozone',
    'water_quality', 'noise_pollution', 'lead_exposure',
    # Food environment
    'food_desert', 'grocery_store', 'supermarket_access',
    'fast_food_density', 'healthy_food_access',
    # Housing infrastructure
    'housing_stock', 'housing_age', 'building_condition',
    # General infrastructure
    'infrastructure_quality', 'broadband_access',
]

# Scale 1: Structural Determinants - policy
SCALE_1_PATTERNS = [
    # Policy terms
    'policy', 'law', 'mandate', 'regulation', 'legislation',
    'ordinance', 'statute', 'act_',
    # Tax/fiscal policy
    'taxation', 'tax_credit', 'tax_rate', 'subsidy', 'funding',
    # Healthcare policy
    'medicaid_expansion', 'aca_', 'chip_', 'medicare_',
    'insurance_mandate', 'coverage_expansion',
    # Labor policy
    'minimum_wage', 'paid_leave', 'family_leave', 'sick_leave',
    'labor_protection', 'union_',
    # Land use policy
    'zoning', 'licensing', 'land_use', 'permitting',
    # Enforcement
    'enforcement', 'compliance_rate', 'inspection',
    # Parity/equity policy
    'parity', 'equity_policy', 'antidiscrimination',
    # Specific policies
    'snap_', 'wic_', 'tanf_', 'eitc_',
]


def infer_scale_from_name(node_id: str, node_name: Optional[str] = None, default: int = 4) -> int:
    """
    Infer scale from node ID/name using keyword patterns.

    The function checks patterns in order of specificity, starting with
    Scale 7 (crisis endpoints) which are the most specific, down to
    Scale 1 (policy) which can be more ambiguous.

    Args:
        node_id: Snake_case node identifier (e.g., 'cardiovascular_disease_mortality')
        node_name: Human-readable name (optional, e.g., 'Cardiovascular Disease Mortality')
        default: Fallback scale if no pattern matches (default 4)

    Returns:
        Scale 1-7

    Examples:
        >>> infer_scale_from_name('cardiovascular_disease_mortality')
        7
        >>> infer_scale_from_name('housing_cost_burden')
        4
        >>> infer_scale_from_name('medicaid_expansion_status')
        1
    """
    if not node_id:
        return default

    # Normalize to lowercase for matching
    text = node_id.lower()
    if node_name:
        text += ' ' + node_name.lower()

    # Check patterns in order of specificity (crisis endpoints first, policy last)
    # This order matters because some terms could match multiple scales
    pattern_scale_pairs = [
        (SCALE_7_PATTERNS, 7),
        (SCALE_6_PATTERNS, 6),
        (SCALE_5_PATTERNS, 5),
        (SCALE_4_PATTERNS, 4),
        (SCALE_3_PATTERNS, 3),
        (SCALE_2_PATTERNS, 2),
        (SCALE_1_PATTERNS, 1),
    ]

    for patterns, scale in pattern_scale_pairs:
        for pattern in patterns:
            if pattern in text:
                return scale

    return default


def get_scale_from_node(node: dict, default: int = 4) -> int:
    """
    Get scale from node dict, inferring if not present or invalid.

    This is the primary function to use when processing node dictionaries.
    It respects explicit scale assignments when valid, otherwise infers.

    Args:
        node: Node dictionary with 'id', 'name', optionally 'scale'
        default: Fallback scale if inference fails

    Returns:
        Scale 1-7

    Examples:
        >>> get_scale_from_node({'id': 'mortality_rate', 'scale': 7})
        7
        >>> get_scale_from_node({'id': 'mortality_rate'})  # No scale set
        7
        >>> get_scale_from_node({'id': 'unknown_node'})  # No pattern match
        4
    """
    # If scale is explicitly set and valid, use it
    if 'scale' in node:
        scale = node['scale']
        if isinstance(scale, int) and 1 <= scale <= 7:
            return scale

    # Otherwise infer from name
    return infer_scale_from_name(
        node.get('id', ''),
        node.get('name', ''),
        default
    )


def get_scale_name(scale: int) -> str:
    """
    Get human-readable name for a scale.

    Args:
        scale: Scale number 1-7

    Returns:
        Scale name string
    """
    scale_names = {
        1: 'Structural Determinants (Policy)',
        2: 'Built Environment & Infrastructure',
        3: 'Institutional Infrastructure',
        4: 'Individual/Household Conditions',
        5: 'Behaviors & Psychosocial',
        6: 'Intermediate Pathways',
        7: 'Crisis Endpoints',
    }
    return scale_names.get(scale, f'Unknown Scale {scale}')
