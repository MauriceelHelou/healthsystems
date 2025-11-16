# Scientific Methodology

## Overview

The HealthSystems Platform uses Bayesian inference to combine prior evidence from scientific literature with contextual geographic and demographic data to produce mechanism weights that reflect local conditions.

## Conceptual Framework

### Structural Determinants of Health

We operationalize structural determinants as:

1. **Structural interventions**: Policies, laws, and systems that shape living conditions (e.g., housing policy, labor law, environmental regulation)

2. **Causal mechanisms**: Pathways through which structural factors affect health (e.g., housing quality → indoor air quality → respiratory health)

3. **Contextual moderators**: Geographic, demographic, and temporal factors that strengthen or weaken mechanisms

## Mechanism Specification

Each mechanism includes:

```
Intervention → Intermediate outcomes → Health outcome
```

**Example:**
```
Minimum wage increase
  ↓
Household income ↑
  ↓
Food security ↑, stress ↓
  ↓
Nutrition ↑, mental health ↑
  ↓
Chronic disease ↓
```

### Effect Size Specification

We prioritize:
- **Odds ratios** (OR) for binary outcomes
- **Relative risks** (RR) for cohort studies
- **Hazard ratios** (HR) for time-to-event
- **Standardized mean differences** (SMD) for continuous outcomes

All effect sizes require 95% confidence intervals.

## Bayesian Weighting Algorithm

### Step 1: Prior Distribution

For mechanism *m*, the prior distribution is based on literature:

```
θₘ ~ Normal(μprior, σprior²)

where:
  μprior = effect size point estimate from literature
  σprior = standard error derived from confidence interval
```

**Prior strength** (α ∈ [0,1]) determines weight given to literature vs. context:
- α = 1: Trust literature completely
- α = 0: Trust context completely
- α = 0.5: Equal weighting (default)

### Step 2: Likelihood from Context

Contextual data *C* modulates the mechanism through moderators:

```
P(Y | θₘ, C) = f(θₘ, β₁·C₁, β₂·C₂, ..., βₖ·Cₖ)

where:
  C₁, C₂, ..., Cₖ = contextual variables (poverty rate, housing age, etc.)
  β₁, β₂, ..., βₖ = moderator coefficients from meta-regression
```

**Example:**
```python
# Housing quality → respiratory health
# Moderators:
- Humidity: β₁ = 0.15 (wetter climates amplify effect)
- Building age: β₂ = 0.10 (older buildings worse)
- Poverty rate: β₃ = 0.25 (resource constraints amplify)

Context adjustment = 1 + β₁·humidity + β₂·age + β₃·poverty
```

### Step 3: Posterior Distribution

Combine prior and likelihood:

```
θₘ | C ~ Normal(μposterior, σposterior²)

μposterior = α·μprior + (1-α)·μcontext
σposterior² = α·σprior² + (1-α)·σcontext² + uncertainty_inflation
```

**Uncertainty inflation** accounts for:
- Model uncertainty
- Unmeasured confounding
- Transportability concerns (external validity)

### Step 4: Network Propagation

For causal chains (M₁ → M₂ → M₃), propagate uncertainty:

```
Monte Carlo simulation:
1. Draw θ₁ ~ Posterior(M₁)
2. Draw θ₂ ~ Posterior(M₂)
3. Draw θ₃ ~ Posterior(M₃)
4. Compute joint effect: θtotal = θ₁ × θ₂ × θ₃
5. Repeat 10,000 times
6. Report mean and 95% credible interval
```

## Evidence Quality Ratings

### Rating Criteria

**A: High Quality**
- Meta-analysis of RCTs or high-quality cohort studies
- ≥ 3 independent studies
- Low risk of bias
- Consistent direction of effect
- Narrow confidence intervals

**B: Moderate Quality**
- Single high-quality study or multiple moderate-quality studies
- Some risk of bias or inconsistency
- Wider confidence intervals

**C: Limited Quality**
- Limited empirical evidence
- Expert consensus
- Theoretical reasoning
- Proxy evidence from related mechanisms

### Downgrading Criteria

Start at A, downgrade for:
- Study limitations (−1 level)
- Inconsistency across studies (−1 level)
- Indirectness/transportability concerns (−1 level)
- Imprecision (wide CIs) (−1 level)
- Publication bias suspected (−1 level)

## Assumptions

### Core Assumptions

1. **Linearity**: Effect sizes are approximately linear within observed ranges
2. **Additivity**: Multiple mechanisms combine multiplicatively on OR/RR scale
3. **Transportability**: Literature effects apply to new contexts with moderator adjustments
4. **Measurement**: Contextual data validly represents constructs
5. **Causal identification**: Literature effects represent causal relationships (not just associations)

### Limitations

- Cannot detect mechanisms not in literature
- Moderators may be incompletely specified
- Unmeasured confounding in observational studies
- Publication bias may inflate prior estimates
- Temporal lags not fully modeled

## Validation

### Internal Validation

- Cross-validation of Bayesian models
- Sensitivity analysis to prior specification
- Posterior predictive checks

### External Validation

- Compare predictions to held-out health outcomes
- Geographic validation (test in new locations)
- Temporal validation (test in new time periods)

## Uncertainty Quantification

All outputs include:
- **Point estimates**: Posterior mean
- **Credible intervals**: 95% Bayesian CIs
- **Evidence quality**: A/B/C rating
- **Heterogeneity**: I² statistic if meta-analysis

## Reproducibility

To ensure computational reproducibility:
- Random seeds specified
- MCMC diagnostics reported (R-hat, effective sample size)
- Software versions documented
- Data provenance tracked

## Statistical Software

- **PyMC**: Bayesian inference and MCMC sampling
- **ArviZ**: Bayesian model diagnostics
- **Statsmodels**: Classical statistical tests
- **NetworkX**: Graph analysis
- **NumPy/SciPy**: Numerical computing

## References

Key methodological sources:

[To be added: Citations for Bayesian methods, meta-analysis, causal inference, structural determinants frameworks]

## Future Methodological Developments

- Machine learning for mechanism discovery
- Dynamic Bayesian networks for temporal dynamics
- Causal forests for heterogeneous treatment effects
- Instrumental variable approaches
- Difference-in-differences for policy evaluation
