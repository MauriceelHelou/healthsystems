"""
Tests for scale_inference utility.

These tests verify that the keyword-based scale inference correctly
classifies nodes into the 7-scale taxonomy defined in NODE_SYSTEM_DEFINITIONS.md.
"""

import pytest
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.scale_inference import (
    infer_scale_from_name,
    get_scale_from_node,
    get_scale_name,
)


class TestInferScaleFromName:
    """Tests for infer_scale_from_name function."""

    # Scale 7: Crisis Endpoints
    @pytest.mark.parametrize("node_id,expected", [
        ("cardiovascular_disease_mortality", 7),
        ("sepsis_mortality", 7),
        ("motor_vehicle_crash_mortality", 7),
        ("all_cause_mortality_rate", 7),
        ("infant_mortality_rate", 7),
        ("maternal_mortality_ratio", 7),
        ("opioid_overdose_deaths", 7),
        ("suicide_rate", 7),
        ("homicide_rate", 7),
        ("alcohol_related_drowning", 7),
        ("ed_visit_rate", 7),
        ("hospitalization_rate", 7),
        ("stroke_mortality", 7),
        ("heart_failure_hospitalization", 7),
        ("low_birthweight_rate", 7),
        ("preterm_birth_rate", 7),
        ("cirrhosis_mortality", 7),
        ("sepsis_hospitalization", 7),
    ])
    def test_scale_7_crisis_endpoints(self, node_id, expected):
        """Mortality, hospitalization, and acute outcomes should be Scale 7."""
        assert infer_scale_from_name(node_id) == expected

    # Scale 6: Intermediate Pathways
    @pytest.mark.parametrize("node_id,expected", [
        ("diabetes_diagnosis_rate", 6),
        ("hypertension_prevalence", 6),
        ("hypertension_control_rate", 6),
        ("diabetes_control", 6),
        ("ggt_elevated", 6),
        ("hba1c_level", 6),
        ("treatment_completion_rate", 6),
        ("abstinence_rate", 6),
        ("screening_rate_colonoscopy", 6),
        ("vaccination_coverage", 6),
        ("preventive_care_utilization", 6),
    ])
    def test_scale_6_intermediate_pathways(self, node_id, expected):
        """Clinical measures, biomarkers, and utilization should be Scale 6."""
        assert infer_scale_from_name(node_id) == expected

    # Scale 5: Behaviors/Psychosocial
    @pytest.mark.parametrize("node_id,expected", [
        ("medication_adherence_rate", 5),
        ("treatment_adherence", 5),
        ("binge_drinking_rate", 5),
        ("tobacco_use_prevalence", 5),
        ("physical_activity_rate", 5),
        ("sedentary_behavior", 5),
        ("fruit_vegetable_consumption", 5),
        ("help_seeking_behavior", 5),
        ("treatment_seeking_delay", 5),
        ("anxiety_disorder_prevalence", 5),
        ("depression_screening_positive", 5),
        ("health_literacy_score", 5),
        ("self_efficacy_score", 5),
        ("coping_behavior", 5),
    ])
    def test_scale_5_behaviors_psychosocial(self, node_id, expected):
        """Behaviors, mental health, and psychosocial factors should be Scale 5."""
        assert infer_scale_from_name(node_id) == expected

    # Scale 4: Individual/Household
    @pytest.mark.parametrize("node_id,expected", [
        ("household_income_median", 4),
        ("poverty_rate", 4),
        ("housing_cost_burden", 4),
        ("rent_burden_rate", 4),
        ("eviction_rate", 4),
        ("food_insecurity_rate", 4),
        ("uninsured_rate", 4),
        ("social_isolation_index", 4),
        ("social_support_score", 4),
        ("adverse_childhood_experiences", 4),
        ("unemployment_rate", 4),
        ("job_loss_rate", 4),
        ("financial_stress_index", 4),
        ("medical_debt_prevalence", 4),
    ])
    def test_scale_4_individual_household(self, node_id, expected):
        """Lived conditions and socioeconomic factors should be Scale 4."""
        assert infer_scale_from_name(node_id) == expected

    # Scale 3: Institutional
    @pytest.mark.parametrize("node_id,expected", [
        ("hospital_beds_per_capita", 3),
        ("provider_density", 3),
        ("treatment_capacity", 3),
        ("specialist_availability", 3),
        ("workforce_shortage", 3),
        ("clinic_density", 3),
        ("program_coverage_sbirt", 3),
        ("mat_availability", 3),
    ])
    def test_scale_3_institutional(self, node_id, expected):
        """Facilities, workforce, and capacity should be Scale 3."""
        assert infer_scale_from_name(node_id) == expected

    # Scale 2: Built Environment
    @pytest.mark.parametrize("node_id,expected", [
        ("alcohol_outlet_density", 2),
        ("bar_density", 2),
        ("liquor_store_density", 2),
        ("walkability_score", 2),
        ("bike_lane_miles", 2),
        ("transit_access_score", 2),
        ("green_space_access", 2),
        ("park_access", 2),
        ("air_pollution_pm25", 2),
        ("food_desert_score", 2),
        ("supermarket_access", 2),
    ])
    def test_scale_2_built_environment(self, node_id, expected):
        """Physical infrastructure should be Scale 2."""
        assert infer_scale_from_name(node_id) == expected

    # Scale 1: Structural Determinants (Policy)
    @pytest.mark.parametrize("node_id,expected", [
        ("medicaid_expansion_status", 1),
        ("aca_premium_tax_credit", 1),
        ("minimum_wage_level", 1),
        ("paid_family_leave_policy", 1),
        ("alcohol_taxation_rate", 1),
        ("zoning_regulation_stringency", 1),
        ("licensing_requirement", 1),
        ("mental_health_parity_enforcement", 1),
        ("snap_eligibility_threshold", 1),
    ])
    def test_scale_1_structural_determinants(self, node_id, expected):
        """Policy and regulations should be Scale 1."""
        assert infer_scale_from_name(node_id) == expected

    def test_default_fallback(self):
        """Unknown nodes should return the default (4)."""
        assert infer_scale_from_name("unknown_random_thing") == 4
        assert infer_scale_from_name("xyz_abc_123") == 4

    def test_custom_default(self):
        """Custom default should be used for unmatched nodes."""
        assert infer_scale_from_name("unknown_node", default=5) == 5

    def test_name_parameter_used(self):
        """Node name should be used in addition to ID for matching."""
        # ID doesn't match, but name does
        assert infer_scale_from_name("some_rate", "Cardiovascular Mortality") == 7
        assert infer_scale_from_name("measure_x", "Medicaid Policy Status") == 1

    def test_empty_input(self):
        """Empty input should return default."""
        assert infer_scale_from_name("") == 4
        assert infer_scale_from_name("", "") == 4

    def test_case_insensitive(self):
        """Matching should be case insensitive."""
        assert infer_scale_from_name("MORTALITY_RATE") == 7
        assert infer_scale_from_name("Hospitalization_Rate") == 7


class TestGetScaleFromNode:
    """Tests for get_scale_from_node function."""

    def test_explicit_scale_respected(self):
        """Explicit scale in node dict should be used."""
        node = {"id": "mortality_rate", "scale": 3}  # Wrong scale but explicit
        assert get_scale_from_node(node) == 3

    def test_missing_scale_inferred(self):
        """Missing scale should be inferred from name."""
        node = {"id": "mortality_rate", "name": "All-Cause Mortality"}
        assert get_scale_from_node(node) == 7

    def test_invalid_scale_inferred(self):
        """Invalid scale should trigger inference."""
        node = {"id": "mortality_rate", "scale": 10}  # Invalid
        assert get_scale_from_node(node) == 7

        node = {"id": "policy_adoption", "scale": -1}  # Invalid
        assert get_scale_from_node(node) == 1

    def test_none_scale_inferred(self):
        """None scale should trigger inference."""
        node = {"id": "hospitalization_rate", "scale": None}
        assert get_scale_from_node(node) == 7

    def test_valid_scale_range(self):
        """Valid scales (1-7) should be accepted."""
        for scale in range(1, 8):
            node = {"id": "some_node", "scale": scale}
            assert get_scale_from_node(node) == scale


class TestGetScaleName:
    """Tests for get_scale_name function."""

    def test_all_scales_have_names(self):
        """All scales 1-7 should have human-readable names."""
        for scale in range(1, 8):
            name = get_scale_name(scale)
            assert name is not None
            assert "Unknown" not in name

    def test_scale_names_descriptive(self):
        """Scale names should be descriptive."""
        assert "Policy" in get_scale_name(1)
        assert "Built" in get_scale_name(2) or "Environment" in get_scale_name(2)
        assert "Institutional" in get_scale_name(3)
        assert "Individual" in get_scale_name(4) or "Household" in get_scale_name(4)
        assert "Behavior" in get_scale_name(5) or "Psychosocial" in get_scale_name(5)
        assert "Intermediate" in get_scale_name(6) or "Pathway" in get_scale_name(6)
        assert "Crisis" in get_scale_name(7) or "Endpoint" in get_scale_name(7)

    def test_invalid_scale(self):
        """Invalid scale should return 'Unknown'."""
        assert "Unknown" in get_scale_name(0)
        assert "Unknown" in get_scale_name(8)
        assert "Unknown" in get_scale_name(-1)


class TestRealWorldExamples:
    """Test with real node IDs from the codebase."""

    @pytest.mark.parametrize("node_id,expected_scale", [
        # Known misclassified nodes that were Scale 4 but should be different
        ("cardiovascular_disease_mortality", 7),
        ("sepsis_mortality", 7),
        ("motor_vehicle_crash_mortality", 7),
        ("low_birthweight_rate", 7),
        # Alcohol-related nodes
        ("alcohol_use_disorder", 5),  # Behavior/condition
        ("alcoholic_hepatitis_hospitalization", 7),
        ("alcohol_outlet_density", 2),
        ("alcohol_taxation", 1),
        # Housing-related
        ("housing_cost_burden", 4),
        ("eviction_rate", 4),
        # Healthcare
        ("fqhc_density", 3),
        ("primary_care_provider_density", 3),
    ])
    def test_real_node_classification(self, node_id, expected_scale):
        """Real nodes from the codebase should be correctly classified."""
        assert infer_scale_from_name(node_id) == expected_scale
