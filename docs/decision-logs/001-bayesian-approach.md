# Decision Log 001: Bayesian Weighting Approach

**Date**: 2024-01-15
**Decision**: Use Bayesian inference for mechanism weighting
**Status**: Accepted
**Deciders**: [Team members]

## Context

We need a method to combine:
1. Prior evidence from scientific literature
2. Contextual data specific to a geography
3. Uncertainty from both sources

To produce mechanism weights that are:
- Evidence-based
- Context-sensitive
- Transparent about uncertainty

## Decision

Adopt a Bayesian approach using hierarchical models implemented in PyMC.

## Alternatives Considered

### 1. Fixed Effect Sizes (NOT CHOSEN)

**Pros:**
- Simple to implement
- Easy to understand
- Fast computation

**Cons:**
- Ignores contextual variation
- No uncertainty quantification
- Not credible for diverse geographies

**Why rejected**: Fails core requirement for geographic adaptation.

### 2. Meta-Regression (NOT CHOSEN)

**Pros:**
- Can include moderators
- Well-established methodology
- Confidence intervals available

**Cons:**
- Requires many studies with reported moderators
- Assumes linear relationships
- Doesn't naturally combine prior + context

**Why rejected**: Insufficient moderator data in most literature.

### 3. Machine Learning (e.g., Random Forests) (NOT CHOSEN)

**Pros:**
- Can discover complex patterns
- Handles non-linearity
- No parametric assumptions

**Cons:**
- "Black box" - difficult to interpret
- Requires large training data
- Doesn't incorporate prior knowledge
- Uncertainty quantification challenging

**Why rejected**: Interpretability crucial for public health decision-making.

### 4. Bayesian Approach (CHOSEN)

**Pros:**
- Naturally combines prior + likelihood
- Transparent uncertainty propagation
- Can incorporate expert knowledge
- Credible intervals well-defined
- Hierarchical models fit our structure

**Cons:**
- Computationally intensive (MCMC)
- Requires statistical expertise
- Can be sensitive to prior specification

**Why chosen**: Best balance of rigor, transparency, and contextual adaptation.

## Implementation Details

### Prior Specification

```python
# For mechanism m with effect size θ
θₘ ~ Normal(
    μ = literature_effect_size,
    σ = SE_from_confidence_interval
)
```

**Prior strength parameter** (α):
- User-adjustable
- Default: 0.5 (equal weight to prior and context)
- Sensitivity analysis across range

### Likelihood from Context

```python
# Context adjustment via moderators
adjustment = Π βᵢ · contextᵢ

# Adjusted effect
θₘ_adjusted = θₘ · adjustment
```

### Posterior

Full MCMC sampling with PyMC:
- 2000 samples per chain
- 4 chains for convergence diagnostics
- Gelman-Rubin R̂ < 1.01 required

## Consequences

### Positive

- **Scientific credibility**: Grounded in established statistical methodology
- **Transparency**: All assumptions explicit and adjustable
- **Uncertainty**: Properly quantified and propagated
- **Flexibility**: Can incorporate new evidence easily
- **Defensibility**: Standard practice in epidemiology and decision science

### Negative

- **Performance**: MCMC can be slow for complex networks
- **Expertise**: Requires statistical knowledge to interpret diagnostics
- **Communication**: Credible intervals less familiar than p-values
- **Priors**: Debate about "objectivity" of prior specification

## Mitigation Strategies

### For Performance
- Cache computed weights
- Precompute for common geographies
- Offer "quick estimate" mode (MAP instead of full MCMC)
- Parallelize chains

### For Expertise
- Provide diagnostic dashboards
- Auto-flag convergence issues
- Offer simplified interpretations
- Training materials for users

### For Communication
- Visualize uncertainty (not just point estimates)
- Use familiar language ("confidence" instead of "credible")
- Provide plain-English summaries
- Show sensitivity to assumptions

### For Priors
- Document all prior sources with citations
- Sensitivity analysis showing robustness
- Allow user to adjust prior strength
- Offer "weakly informative" default priors

## Success Metrics

- Posterior predictive checks show good calibration
- Cross-validation accuracy > 0.8
- User satisfaction with uncertainty communication
- Computational time < 30 seconds for typical query

## Review Date

Review this decision: 2025-01-15 (one year)

Re-evaluate if:
- New statistical methods emerge
- Performance becomes bottleneck
- Users struggle with interpretation
- Validation studies show poor calibration

## References

- Gelman et al. (2013). *Bayesian Data Analysis*
- Spiegelhalter et al. (2004). "Bayesian approaches to clinical trials and health-care evaluation"
- Lunn et al. (2012). "The BUGS Book: A Practical Introduction to Bayesian Analysis"

## Notes

This decision builds on decades of Bayesian methods in epidemiology and public health. While computationally demanding, the transparency and rigor justify the complexity.

Future consideration: Explore variational inference for faster approximations if MCMC becomes prohibitive.
