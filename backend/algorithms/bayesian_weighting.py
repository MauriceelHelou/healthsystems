"""
Bayesian mechanism weighting algorithm.

Combines prior evidence from literature with contextual data to produce
posterior mechanism weights with uncertainty quantification.
"""

import numpy as np
from typing import Dict, Tuple, Any, Optional, List
import logging

logger = logging.getLogger(__name__)


class BayesianMechanismWeighter:
    """
    Calculate posterior weights for causal mechanisms using Bayesian inference.

    Combines:
    - Prior: Effect sizes from literature
    - Likelihood: Context-specific data (demographics, environment, etc.)
    - Posterior: Updated mechanism weight with uncertainty
    """

    def __init__(
        self,
        mcmc_samples: int = 2000,
        mcmc_chains: int = 4,
        random_seed: int = 42
    ):
        """
        Initialize Bayesian weighter.

        Args:
            mcmc_samples: Number of MCMC samples per chain
            mcmc_chains: Number of parallel chains
            random_seed: Random seed for reproducibility
        """
        self.mcmc_samples = mcmc_samples
        self.mcmc_chains = mcmc_chains
        self.random_seed = random_seed
        np.random.seed(random_seed)

    def calculate_weight(
        self,
        mechanism_id: str,
        prior_effect_size: float,
        prior_ci: Tuple[float, float],
        context_data: Dict[str, Any],
        prior_strength: float = 0.5,
        use_pymc: bool = False
    ) -> Tuple[float, Tuple[float, float]]:
        """
        Calculate Bayesian posterior weight for a mechanism.

        Args:
            mechanism_id: Unique identifier for mechanism
            prior_effect_size: Point estimate from literature
            prior_ci: 95% confidence interval (lower, upper)
            context_data: Geographic/demographic context
            prior_strength: Weight given to prior vs. data (0-1)
            use_pymc: If True, use full PyMC model (requires pymc installed)

        Returns:
            Tuple of (posterior_weight, (ci_lower, ci_upper))

        Example:
            >>> weighter = BayesianMechanismWeighter()
            >>> weight, ci = weighter.calculate_weight(
            ...     "housing_quality_respiratory",
            ...     prior_effect_size=1.34,
            ...     prior_ci=(1.18, 1.52),
            ...     context_data={"poverty_rate": 0.25, "housing_age": 45}
            ... )
        """
        logger.info(f"Calculating weight for mechanism: {mechanism_id}")

        if use_pymc:
            try:
                return self._calculate_weight_pymc(
                    mechanism_id=mechanism_id,
                    prior_effect_size=prior_effect_size,
                    prior_ci=prior_ci,
                    context_data=context_data
                )
            except ImportError:
                logger.warning("PyMC not installed, falling back to simplified calculation")

        # Extract prior parameters
        prior_mean = prior_effect_size
        prior_se = (prior_ci[1] - prior_ci[0]) / (2 * 1.96)  # Approximate SE

        # Context adjustment (placeholder - should be data-driven)
        context_adjustment = self._calculate_context_adjustment(context_data)

        # Simple Bayesian update (simplified)
        posterior_mean = (
            prior_strength * prior_mean +
            (1 - prior_strength) * (prior_mean * context_adjustment)
        )

        # Uncertainty increases with context variation
        posterior_se = prior_se * (1 + 0.1 * abs(context_adjustment - 1))

        # Calculate 95% CI
        ci_lower = posterior_mean - 1.96 * posterior_se
        ci_upper = posterior_mean + 1.96 * posterior_se

        logger.info(
            f"Posterior weight: {posterior_mean:.3f} "
            f"(95% CI: {ci_lower:.3f}-{ci_upper:.3f})"
        )

        return posterior_mean, (ci_lower, ci_upper)

    def _calculate_weight_pymc(
        self,
        mechanism_id: str,
        prior_effect_size: float,
        prior_ci: Tuple[float, float],
        context_data: Dict[str, Any]
    ) -> Tuple[float, Tuple[float, float]]:
        """
        Calculate weight using full PyMC Bayesian hierarchical model.

        Args:
            mechanism_id: Mechanism identifier
            prior_effect_size: Literature effect size
            prior_ci: Confidence interval
            context_data: Context for adjustment

        Returns:
            Posterior mean and credible interval
        """
        import pymc as pm
        import arviz as az

        # Prior parameters
        prior_mean = prior_effect_size
        prior_sd = (prior_ci[1] - prior_ci[0]) / (2 * 1.96)

        # Context adjustment factor
        context_factor = self._calculate_context_adjustment(context_data)

        with pm.Model() as model:
            # Prior on base effect
            base_effect = pm.Normal(
                'base_effect',
                mu=prior_mean,
                sigma=prior_sd
            )

            # Context modification
            context_modifier = pm.Normal(
                'context_modifier',
                mu=0,
                sigma=0.1
            )

            # Adjusted effect (log scale for multiplicative effects)
            if prior_mean > 0:
                log_adjusted = pm.Deterministic(
                    'log_adjusted',
                    pm.math.log(base_effect) + context_modifier
                )
                adjusted_effect = pm.Deterministic(
                    'adjusted_effect',
                    pm.math.exp(log_adjusted)
                )
            else:
                # For negative/additive effects
                adjusted_effect = pm.Deterministic(
                    'adjusted_effect',
                    base_effect + context_modifier
                )

            # Sample posterior
            trace = pm.sample(
                draws=self.mcmc_samples,
                tune=1000,
                chains=self.mcmc_chains,
                random_seed=self.random_seed,
                return_inferencedata=True,
                progressbar=False
            )

        # Extract results
        posterior = trace.posterior['adjusted_effect'].values.flatten()
        mean_weight = float(np.mean(posterior))
        ci_lower, ci_upper = np.percentile(posterior, [2.5, 97.5])

        logger.info(
            f"PyMC posterior: {mean_weight:.3f} "
            f"(95% CrI: {ci_lower:.3f}-{ci_upper:.3f})"
        )

        return mean_weight, (float(ci_lower), float(ci_upper))

    def _calculate_context_adjustment(
        self,
        context_data: Dict[str, Any]
    ) -> float:
        """
        Calculate adjustment factor based on contextual data.

        This is a placeholder. Real implementation would use:
        - Machine learning models
        - Expert knowledge graphs
        - Meta-regression on moderators

        Args:
            context_data: Geographic/demographic context

        Returns:
            Adjustment factor (typically 0.5-1.5)
        """
        # Placeholder: simple linear combination
        # Real implementation would be much more sophisticated

        adjustment = 1.0

        if "poverty_rate" in context_data:
            # Higher poverty may amplify some mechanisms
            adjustment += context_data["poverty_rate"] * 0.2

        if "housing_age" in context_data:
            # Older housing may increase environmental exposures
            adjustment += (context_data["housing_age"] - 30) / 100

        # Keep adjustment in reasonable range
        return np.clip(adjustment, 0.5, 1.5)

    def propagate_uncertainty(
        self,
        mechanism_weights: Dict[str, Tuple[float, Tuple[float, float]]],
        network_structure: Dict[str, list],
        n_simulations: int = 1000
    ) -> Dict[str, Dict[str, Any]]:
        """
        Propagate uncertainty through causal network using Monte Carlo simulation.

        Uses Monte Carlo simulation to propagate uncertainty from
        individual mechanisms through the full systems model.

        Args:
            mechanism_weights: Dict of {mechanism_id: (weight, (ci_lower, ci_upper))}
            network_structure: Dict of {mechanism_id: [downstream_mechanisms]}
            n_simulations: Number of Monte Carlo samples

        Returns:
            Dict with pathway-level uncertainty estimates

        Example:
            >>> weights = {
            ...     "m1": (1.2, (1.0, 1.4)),
            ...     "m2": (1.5, (1.3, 1.7))
            ... }
            >>> structure = {"m1": ["m2"]}
            >>> updated = weighter.propagate_uncertainty(weights, structure)
        """
        logger.info(f"Propagating uncertainty through network ({n_simulations} simulations)")

        # Sample weights for each mechanism
        mechanism_samples = {}

        for mech_id, (mean, (ci_lower, ci_upper)) in mechanism_weights.items():
            # Approximate standard deviation from CI
            sd = (ci_upper - ci_lower) / (2 * 1.96)

            # Draw samples from normal distribution
            samples = np.random.normal(mean, sd, n_simulations)

            # Clip to reasonable range (0.1 to 10 for multiplicative effects)
            samples = np.clip(samples, 0.1, 10.0)

            mechanism_samples[mech_id] = samples

        # Find all pathways through network
        pathways = self._identify_pathways(network_structure)

        # Calculate uncertainty for each pathway
        pathway_uncertainty = {}

        for pathway_id, mechanism_chain in pathways.items():
            if not mechanism_chain:
                continue

            # Get samples for mechanisms in this pathway
            pathway_samples = [
                mechanism_samples[m_id]
                for m_id in mechanism_chain
                if m_id in mechanism_samples
            ]

            if not pathway_samples:
                continue

            pathway_samples = np.array(pathway_samples)

            # Method 1: Weakest link (minimum)
            pathway_min = np.min(pathway_samples, axis=0)

            # Method 2: Geometric mean (compound effect)
            pathway_geomean = np.exp(np.mean(np.log(pathway_samples + 1e-10), axis=0))

            # Method 3: Product (full attenuation)
            pathway_product = np.prod(pathway_samples, axis=0)

            pathway_uncertainty[pathway_id] = {
                'weakest_link': {
                    'mean': float(np.mean(pathway_min)),
                    'median': float(np.median(pathway_min)),
                    'ci': [float(np.percentile(pathway_min, 2.5)),
                           float(np.percentile(pathway_min, 97.5))],
                    'probability_strong': float(np.mean(pathway_min > 1.0))
                },
                'geometric_mean': {
                    'mean': float(np.mean(pathway_geomean)),
                    'median': float(np.median(pathway_geomean)),
                    'ci': [float(np.percentile(pathway_geomean, 2.5)),
                           float(np.percentile(pathway_geomean, 97.5))],
                    'probability_strong': float(np.mean(pathway_geomean > 1.0))
                },
                'compound_effect': {
                    'mean': float(np.mean(pathway_product)),
                    'median': float(np.median(pathway_product)),
                    'ci': [float(np.percentile(pathway_product, 2.5)),
                           float(np.percentile(pathway_product, 97.5))],
                    'probability_strong': float(np.mean(pathway_product > 1.0))
                },
                'mechanisms': mechanism_chain,
                'n_simulations': n_simulations
            }

        logger.info(f"Computed uncertainty for {len(pathway_uncertainty)} pathways")

        return pathway_uncertainty

    def _identify_pathways(
        self,
        network_structure: Dict[str, list],
        max_depth: int = 5
    ) -> Dict[str, List[str]]:
        """
        Identify all pathways through a causal network.

        Args:
            network_structure: Dict mapping mechanism_id to list of downstream mechanisms
            max_depth: Maximum pathway length to consider

        Returns:
            Dict of {pathway_id: [mechanism_ids in order]}
        """
        pathways = {}
        pathway_counter = 0

        # Find root nodes (nodes with no incoming edges)
        all_nodes = set(network_structure.keys())
        downstream_nodes = set()
        for downstream_list in network_structure.values():
            downstream_nodes.update(downstream_list)

        root_nodes = all_nodes - downstream_nodes

        # DFS to find all paths
        def dfs(node, current_path, depth):
            nonlocal pathway_counter

            if depth > max_depth:
                return

            # Add current node to path
            new_path = current_path + [node]

            # If this is a leaf node or we've reached max depth, save pathway
            if node not in network_structure or not network_structure[node]:
                if len(new_path) > 1:  # Only save multi-step pathways
                    pathway_id = f"pathway_{pathway_counter}"
                    pathways[pathway_id] = new_path
                    pathway_counter += 1
                return

            # Continue DFS for downstream nodes
            for downstream_node in network_structure.get(node, []):
                if downstream_node not in current_path:  # Avoid cycles
                    dfs(downstream_node, new_path, depth + 1)

        # Start DFS from each root node
        for root in root_nodes:
            dfs(root, [], 0)

        return pathways
