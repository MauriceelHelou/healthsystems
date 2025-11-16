"""
Tests for Bayesian mechanism weighting algorithm.
"""

import pytest
import numpy as np

from algorithms.bayesian_weighting import BayesianMechanismWeighter


class TestBayesianMechanismWeighter:
    """Test suite for Bayesian weighting algorithm."""

    @pytest.fixture
    def weighter(self):
        """Create a weighter instance for testing."""
        return BayesianMechanismWeighter(
            mcmc_samples=100,  # Smaller for tests
            mcmc_chains=2,
            random_seed=42
        )

    def test_initialization(self, weighter):
        """Test weighter initializes with correct parameters."""
        assert weighter.mcmc_samples == 100
        assert weighter.mcmc_chains == 2
        assert weighter.random_seed == 42

    def test_calculate_weight_returns_tuple(self, weighter):
        """Test that calculate_weight returns (weight, CI)."""
        weight, ci = weighter.calculate_weight(
            mechanism_id="test_mechanism",
            prior_effect_size=1.5,
            prior_ci=(1.2, 1.8),
            context_data={}
        )

        assert isinstance(weight, float)
        assert isinstance(ci, tuple)
        assert len(ci) == 2
        assert ci[0] < weight < ci[1]  # Weight should be within CI

    def test_calculate_weight_with_context(self, weighter):
        """Test weight calculation with contextual data."""
        weight, ci = weighter.calculate_weight(
            mechanism_id="test_mechanism",
            prior_effect_size=1.5,
            prior_ci=(1.2, 1.8),
            context_data={
                "poverty_rate": 0.25,
                "housing_age": 45
            }
        )

        assert weight > 0
        assert ci[0] > 0
        assert ci[1] > ci[0]

    def test_prior_strength_affects_weight(self, weighter):
        """Test that prior_strength parameter affects the result."""
        weight_strong_prior, _ = weighter.calculate_weight(
            mechanism_id="test_mechanism",
            prior_effect_size=1.5,
            prior_ci=(1.2, 1.8),
            context_data={"poverty_rate": 0.5},
            prior_strength=0.9  # Strong prior
        )

        weight_weak_prior, _ = weighter.calculate_weight(
            mechanism_id="test_mechanism",
            prior_effect_size=1.5,
            prior_ci=(1.2, 1.8),
            context_data={"poverty_rate": 0.5},
            prior_strength=0.1  # Weak prior
        )

        # Weights should differ based on prior strength
        assert weight_strong_prior != weight_weak_prior

    def test_context_adjustment_in_range(self, weighter):
        """Test that context adjustment stays in reasonable range."""
        context_data_low = {"poverty_rate": 0.05, "housing_age": 10}
        context_data_high = {"poverty_rate": 0.50, "housing_age": 80}

        adjustment_low = weighter._calculate_context_adjustment(context_data_low)
        adjustment_high = weighter._calculate_context_adjustment(context_data_high)

        # Both should be in range [0.5, 1.5]
        assert 0.5 <= adjustment_low <= 1.5
        assert 0.5 <= adjustment_high <= 1.5

        # High-risk context should have higher adjustment
        assert adjustment_high > adjustment_low

    def test_propagate_uncertainty(self, weighter):
        """Test uncertainty propagation through network."""
        mechanism_weights = {
            "m1": (1.2, (1.0, 1.4)),
            "m2": (1.5, (1.3, 1.7)),
            "m3": (0.9, (0.7, 1.1))
        }

        network_structure = {
            "m1": ["m2"],
            "m2": ["m3"],
            "m3": []
        }

        updated_weights = weighter.propagate_uncertainty(
            mechanism_weights,
            network_structure
        )

        # Should return dict with same keys
        assert set(updated_weights.keys()) == set(mechanism_weights.keys())

        # Each value should be (weight, (ci_lower, ci_upper))
        for mechanism_id, (weight, ci) in updated_weights.items():
            assert isinstance(weight, float)
            assert isinstance(ci, tuple)
            assert len(ci) == 2

    def test_reproducibility(self, weighter):
        """Test that results are reproducible with same seed."""
        weight1, ci1 = weighter.calculate_weight(
            mechanism_id="test_mechanism",
            prior_effect_size=1.5,
            prior_ci=(1.2, 1.8),
            context_data={"poverty_rate": 0.25}
        )

        # Create new weighter with same seed
        weighter2 = BayesianMechanismWeighter(random_seed=42)
        weight2, ci2 = weighter2.calculate_weight(
            mechanism_id="test_mechanism",
            prior_effect_size=1.5,
            prior_ci=(1.2, 1.8),
            context_data={"poverty_rate": 0.25}
        )

        assert weight1 == weight2
        assert ci1 == ci2
