# Methodological Integration
## Synthesizing Systems Dynamics, Structural Equation Modeling, and Bayesian Inference

**Document ID**: 02_METHODOLOGICAL_INTEGRATION.md
**Version**: 2.0
**Last Updated**: November 15, 2025
**Tier**: 1 - Foundational Principles

---

## ⚠️ MVP vs. Phase 2 Scope

**This document describes the full methodological vision** integrating three frameworks:

**MVP (Phase 1) - Systems Dynamics & SEM Only**:
- ✓ **Systems Dynamics**: Stock-flow network structure
- ✓ **SEM Framework**: Causal pathways from literature (direction only)
- ✗ **Bayesian Inference**: Deferred to Phase 2

**Phase 2 - Full Integration**:
- ✓ Add Bayesian meta-analysis for effect quantification
- ✓ Add uncertainty propagation via Monte Carlo
- ✓ Add continuous updating with new evidence

**Sections marked [Phase 2]** describe Bayesian capabilities deferred from MVP.
**See**: `docs/Phase 2 - Quantification/02B_BAYESIAN_METHODOLOGY.md` for extracted Bayesian specifications.

---

## Table of Contents

1. [Integration Overview](#integration-overview)
2. [Systems Dynamics Paradigm](#systems-dynamics-paradigm)
3. [Structural Equation Modeling Integration](#structural-equation-modeling-integration)
4. [Bayesian Inference Framework](#bayesian-inference-framework)
5. [Synthesis: How Three Methodologies Combine](#synthesis-how-three-methodologies-combine)
6. [Epistemological Foundations](#epistemological-foundations)
7. [Practical Implications](#practical-implications)

---

## Integration Overview

### The Challenge

Health impact modeling requires integrating three traditionally separate methodological traditions:

**Systems Dynamics (SD)**: 
- Models complex systems with feedback loops, stocks, flows
- Excellent for capturing dynamic behavior over time
- Challenge: Typically requires hand-specification of all relationships and parameters

**Structural Equation Modeling (SEM)**:
- Estimates causal relationships from empirical data
- Provides effect sizes and uncertainty quantification
- Challenge: Assumes linear relationships, struggles with feedback loops and time dynamics

**Bayesian Inference**:
- Quantifies uncertainty through probability distributions
- Combines prior knowledge with empirical evidence
- Challenge: Computationally intensive, requires expertise to specify priors

### Our Synthesis

We integrate all three to create a unified framework:

```
Systems Dynamics provides:
├─ Stock-flow architecture (nodes and mechanisms)
├─ Feedback loop specification (reinforcing and balancing)
├─ Time dynamics and equilibrium concepts
└─ Intervention cascade logic

Structural Equation Modeling provides:
├─ Effect size estimation from literature
├─ Causal pathway identification
├─ Population stratification (demographic moderators)
└─ Multi-level modeling (structural → individual → health)

Bayesian Inference provides:
├─ Uncertainty quantification (confidence intervals → credible intervals)
├─ Prior elicitation (expert knowledge integration)
├─ Meta-analytic synthesis (pooling across studies)
└─ Parameter updating (as new evidence emerges)
```

**Result**: A system that has SD's dynamic complexity, SEM's empirical grounding, and Bayesian uncertainty quantification—without requiring users to understand the underlying mathematics.

---

## Systems Dynamics Paradigm

### Core Concepts

**Stocks**: Variables that accumulate or deplete over time. Represent system state at any moment.

```
Examples:
- Community Health Worker Capacity: 50 FTE → 200 FTE
- Healthcare Continuity Index: 0.45 → 0.63
- ED Visits per Year: 122,400 → 118,000
```

**Flows**: Rates of change in stocks. Determined by mechanisms connecting stocks.

```
Example:
Flow into Healthcare_Continuity stock = 
  f(CHW_Capacity, Healthcare_Integration, Medicaid_Rules)
```

**Feedback Loops**: Circular causal pathways that can amplify (reinforcing) or stabilize (balancing) system behavior.

```
Reinforcing Loop Example:
Community_Trust → Participation → Organizing_Success → Policy_Wins → Community_Trust
(Higher trust leads to more participation, more success, more trust...)

Balancing Loop Example:
ED_Utilization → Hospital_Capacity_Strain → Wait_Times → Care_Seeking_Delay → ED_Utilization
(Higher utilization creates strain, increases waits, reduces seeking, lowers utilization...)
```

### Stock-Flow Architecture in Our System

#### **Stock Types**

**Type 1: Real Stocks (Direct Measurement)**
- Have natural units of measurement
- Observed directly from data
- Examples:
  - CHW_Count: 50 FTE (count of workers)
  - ED_Visits: 122,400 per year (administrative data)
  - Housing_Units: 2,500 affordable units (property records)

**Type 2: Proxy Index Stocks (Constructed)**
- No natural unit of measurement
- Constructed from multiple components
- Normalized to 0-1 scale or similar
- Examples:
  - Healthcare_Continuity_Index = 0.4×Insurance_Persistence + 0.3×Provider_Retention + 0.3×Appointment_Completion
  - Policy_Strength_Index = weighted average of just-cause eviction score, rent control, tenant protections
  - Community_Trust_Index = survey-derived composite

**Type 3: Crisis Endpoint Stocks (Outcome Measures)**
- Health outcomes with unit costs
- Observable, measurable
- Used for ROI calculation
- Examples:
  - ED_Visits, Hospitalizations, Overdoses, Deaths, Arrests

#### **Flow Specification**

Flows between stocks determined by mechanism functional forms:

```
General form:
ΔStock_j(t) = Σ f_ij(Stock_i(t), Parameters, Moderators)

Where:
- ΔStock_j = change in downstream stock j
- f_ij = functional form of mechanism from stock i to stock j
- Stock_i = current level of upstream stock
- Parameters = effect size, saturation point, threshold
- Moderators = local context adjustments (policy, demographic, etc.)
```

**Five Standard Functional Forms**:

1. **Sigmoid (S-curve)**
   ```
   ΔStock_j = α × (1 / (1 + e^(-k(Stock_i - threshold))))
   ```
   Use for: Capacity building, behavioral adoption, systems with saturation
   Example: CHW capacity → healthcare continuity (diminishing returns at high capacity)

2. **Logarithmic (Diminishing Returns)**
   ```
   ΔStock_j = α × log(1 + Stock_i)
   ```
   Use for: Resource accumulation with scarcity
   Example: Housing units → housing stability (first units matter most)

3. **Saturating Linear (Piecewise)**
   ```
   ΔStock_j = min(α × Stock_i, max_capacity - Stock_j)
   ```
   Use for: Physical infrastructure with hard limits
   Example: Green space → air quality (max improvement bounded)

4. **Threshold-Activated (Piecewise)**
   ```
   ΔStock_j = α × max(0, Stock_i - threshold)
   ```
   Use for: Policy effects, tipping points
   Example: Policy strength → enforcement (only works above threshold)

5. **Multiplicative Dampening**
   ```
   ΔStock_j = α × Stock_i × (1 - Stock_j / max_stock_j)
   ```
   Use for: Percentage-based changes, relative effects
   Example: Economic assistance → income stability (effect depends on current level)

### Equilibrium Concepts

**Pre-Intervention Equilibrium**: State where system is at baseline (current observed reality)

**Characteristics**:
- Crisis endpoint stocks: Fixed at observed values (ED_Visits = 122,400/year from data)
- Structural stocks: Measured directly (CHW_Count = 50 from organizational records)
- Intermediate stocks: Calculated via inverse calibration to produce observed crisis endpoints
- All flows balance: Σ(inflows) = Σ(outflows) for each intermediate stock

**Method**: 
1. Fix crisis endpoints and structural stocks (known values)
2. Solve system of equations for intermediate stocks
3. Use linearized approximation for initial guess
4. Refine with iterative relaxation until convergence
5. Validate: Does calculated equilibrium reproduce observed crisis endpoints?

**Post-Intervention Dynamics**: Behavior after user changes a structural stock

**Two Modes**:

**Mode A: Time Simulation**
- Simulate system forward in annual time steps
- Apply intervention ramp-up (Year 1: 60%, Year 2: 90%, Year 3: 100%)
- Calculate flows at each time step
- Update stocks based on flows
- Continue until convergence or time horizon reached

**Mode B: New Equilibrium**
- User changes stock (CHW 50→200)
- System recalculates equilibrium with new stock value
- Compare new equilibrium to baseline equilibrium
- Impact = difference in crisis endpoint stocks

**Choice**: Use Mode A (time simulation) for most user scenarios; Mode B for policy analysis requiring long-term steady state

### Feedback Loop Handling

**Challenge**: Reinforcing loops can cause exponential growth without bounds

**Solution: Bounded Feedback**

All mechanisms use functional forms with saturation to ensure stable equilibria:

```
Example: Trust → Participation → Success → Trust (reinforcing)

Without bounds: Trust → ∞ (unrealistic)

With bounds:
  Trust(t+1) = Trust(t) + α × sigmoid(Success(t) - Trust(t))
  
  Where sigmoid ensures:
  - When Trust is low: Large potential for increase
  - When Trust is high: Saturated (little room for further increase)
  - Trust ∈ [0, 1] bounded
```

**Bounding Mechanisms**:
1. **Resource constraints**: Finite population, budget limits
2. **Saturation effects**: Sigmoid functions prevent infinite growth
3. **Competing loops**: Balancing loops provide negative feedback
4. **Time horizons**: Measure before exponential effects dominate
5. **Mathematical construction**: All mechanisms designed with bounds

---

## Structural Equation Modeling Integration

### SEM Contributions to Our Framework

SEM provides the empirical grounding for mechanism specifications. We use SEM concepts without requiring users to run SEM themselves.

#### **Causal Pathway Specification**

SEM's directed acyclic graph (DAG) structure maps onto our mechanism network:

```
SEM notation:
  Y = β₁X₁ + β₂X₂ + ε

Maps to our mechanism:
  Healthcare_Continuity = 
    β₁ × CHW_Capacity + 
    β₂ × Healthcare_Integration + 
    ε (unexplained variance)
```

**Key adaptation**: We extend SEM's linear additive form to nonlinear functions (sigmoid, log, etc.) while preserving SEM's causal interpretation

#### **Multi-Level Structure**

SEM excels at modeling nested effects (individual within neighborhood within state). We incorporate this:

```
Level 1: Structural (State Policy)
  ├─ Medicaid_Expansion → Healthcare_Access
  
Level 2: Institutional (Hospital System)
  ├─ Healthcare_Integration → Care_Coordination
  
Level 3: Individual (Patient Experience)
  ├─ Care_Coordination → Health_Outcomes

Cross-level interactions:
  Effect of Care_Coordination on Outcomes 
  moderated by Healthcare_Integration (Level 2)
  moderated by Medicaid_Expansion (Level 1)
```

**Implementation**: Moderators capture cross-level interactions

```
Effect = Base_Effect + 
         δ_policy × (Policy_Context) + 
         δ_institutional × (Integration_Level) + 
         δ_demographic × (Population_Characteristics)
```

#### **Mediation Analysis**

SEM's mediation framework informs our mechanism chains:

```
Direct effect: Eviction → Health (unmediated, often weak)

Indirect effect: Eviction → Economic_Precarity → Healthcare_Discontinuity → Health
(mediated, captures causal mechanism)

Total effect: Direct + Indirect
```

**Our implementation**: Mechanisms represent mediated pathways. We trace indirect effects through intermediate stocks.

```
User proposes: "Eviction prevention policy"

System calculates:
1. Direct effect on Health: Small (β = 0.03)
2. Indirect via Economic_Precarity: β₁ = 0.25
3. Indirect via Healthcare_Discontinuity: β₂ = 0.18
4. Indirect via Stress: β₃ = 0.12
5. Total effect: 0.03 + 0.25 + 0.18 + 0.12 = 0.58

System shows: "Primary pathway is economic stability (44% of effect), 
followed by healthcare continuity (31%)"
```

#### **Population Stratification**

SEM's multi-group analysis informs our population moderators:

```
SEM approach: Estimate separate models for Black vs. White populations
  β_Black = 0.35 (effect for Black population)
  β_White = 0.20 (effect for White population)
  
Our encoding:
  Base_Effect = 0.275 (average)
  Moderator_Black = +0.075 (adjustment for Black population)
  Moderator_White = -0.075 (adjustment for White population)
```

**Advantage**: Explicitly represents disparities. User sees which populations experience stronger/weaker effects.

---

## Bayesian Inference Framework [Phase 2]

**⚠️ Note**: This entire section describes **Phase 2 capabilities**. MVP does not include Bayesian inference.

**MVP Approach**: Qualitative uncertainty assessment (evidence strength ratings: strong/moderate/limited)

**Phase 2 Approach**: Quantitative uncertainty via Bayesian posterior distributions

**Full Bayesian specifications**: See `docs/Phase 2 - Quantification/02B_BAYESIAN_METHODOLOGY.md`

### Bayesian Contributions to Our Framework [Phase 2]

Bayesian methods provide rigorous uncertainty quantification without requiring users to understand Bayesian statistics.

#### **Meta-Analytic Synthesis**

**Problem**: 12 studies report effect of eviction on ED visits. Effect sizes vary: RR = 1.18 to RR = 1.52. How to synthesize?

**Frequentist approach**: Random-effects meta-analysis
- Calculate pooled effect: RR_pooled = 1.34
- Calculate 95% confidence interval: [1.12, 1.61]
- Problem: Treats parameter as fixed but unknown

**Bayesian approach**: Hierarchical model
```
For each study i:
  Observed_Effect_i ~ Normal(True_Effect_i, SE_i²)
  
True effects vary across studies:
  True_Effect_i ~ Normal(μ, τ²)
  
Where:
  μ = overall mean effect (what we want to estimate)
  τ² = between-study variance (heterogeneity)
```

**Prior specification**:
```
μ ~ Normal(0.26, 0.075²)  [from expert elicitation]
τ ~ HalfCauchy(0.05)      [weakly informative prior on heterogeneity]
```

**Posterior inference**:
```
Run MCMC (Hamiltonian Monte Carlo) to sample from:
  p(μ, τ | observed data)

Result:
  μ_posterior: median = 0.262, 95% CrI = [0.187, 0.342]
  τ_posterior: median = 0.048
```

**Advantage over frequentist**:
- Full posterior distribution (not just point estimate + CI)
- Can make probability statements: "There's 95% probability that true effect is between 0.187 and 0.342"
- Incorporates prior knowledge from experts
- Handles small sample sizes better

#### **Prior Elicitation via Expert Aggregation**

**Challenge**: How to specify priors without bias?

**Our approach**: LLM-assisted expert aggregation

1. **Expert Consultation**:
   ```
   Ask 3-5 epidemiologists:
   "Based on theory and related evidence, what effect size would you expect 
   for eviction → ED visits pathway?"
   
   Expert 1: "I'd guess around 0.25, fairly confident"
   Expert 2: "Could be 0.35, but uncertain"
   Expert 3: "Probably 0.18 based on housing stability literature"
   ```

2. **LLM Aggregation**:
   ```
   LLM prompt:
   "Given these expert estimates, specify a prior distribution that:
   - Centers on the consensus estimate
   - Has width reflecting disagreement
   - Is weakly informative (data can override if strong evidence)"
   
   LLM output:
   μ ~ Normal(0.26, 0.075²)
   [mean = average of expert estimates, 
    SD captures range of disagreement]
   ```

3. **Sensitivity Analysis**:
   ```
   Test: Does prior dominate posterior?
   
   If prior dominates: Data too weak → flag as low-confidence mechanism
   If data dominates: Prior has minimal impact → robust finding
   ```

#### **Uncertainty Propagation**

**Challenge**: User changes CHW capacity. This affects healthcare continuity (with uncertainty), which affects ED utilization (with uncertainty). How to quantify compounded uncertainty?

**Bayesian approach**: Monte Carlo simulation with posterior samples

```
1. Sample from posterior distributions:
   - Effect_CHW_to_Continuity: sample 1000 values from posterior
   - Effect_Continuity_to_ED: sample 1000 values from posterior

2. For each sample:
   - Calculate: ΔContinuity = f(ΔCHW, Effect_sample_1)
   - Calculate: ΔED = g(ΔContinuity, Effect_sample_2)
   
3. Result: 1000 estimates of ΔED (posterior predictive distribution)

4. Summarize:
   - Median ΔED = -4,200 ED visits/year
   - 95% CrI = [-6,800, -1,800]
   
User sees: "Projected ED reduction: 4,200 visits (95% probability between 1,800 and 6,800)"
```

**Advantage**: Quantifies cascade uncertainty. User understands precision of projection.

#### **Continuous Updating**

**Bayesian framework enables version evolution**:

```
Version 1.0:
  Prior: Expert opinion (μ ~ N(0.26, 0.075²))
  Data: 12 studies
  Posterior: μ = 0.262 [0.187, 0.342]

Version 1.1: Two new RCTs published
  Prior: Previous posterior becomes new prior
  Data: 2 additional RCTs
  Posterior: μ = 0.271 [0.205, 0.345]  [slight increase, narrower CI]

Version 2.0: Real-world validation from 5 cities
  Prior: Previous posterior
  Data: Observed outcomes from platform users
  Posterior: μ = 0.265 [0.220, 0.315]  [converges, tighter CI]
```

**Learning cycle**: As evidence accumulates, uncertainty decreases, estimates converge to truth.

---

## Synthesis: How Three Methodologies Combine

### Integration Architecture

```
┌─────────────────────────────────────────────────────────────┐
│               UNIFIED FRAMEWORK ARCHITECTURE                 │
└─────────────────────────────────────────────────────────────┘

LAYER 1: SYSTEMS DYNAMICS (Structure) [MVP]
├─ Stock-flow network (~400 nodes, ~2000 mechanisms)
├─ Feedback loops (reinforcing and balancing)
├─ [Phase 2] Time dynamics (simulation forward in annual steps)
└─ [Phase 2] Equilibrium concepts (pre/post intervention states)

LAYER 2: STRUCTURAL EQUATION MODELING (Empirical Grounding)
├─ [MVP] Causal pathways from literature (direction only)
├─ [MVP] Multi-level structure (structural → institutional → individual)
├─ [MVP] Mediation pathways identification (which intermediates matter)
├─ [Phase 2] Effect sizes from literature (β coefficients, standardized)
└─ [Phase 2] Population stratification (group-specific effects)

LAYER 3: BAYESIAN INFERENCE (Uncertainty Quantification) [Phase 2 Only]
├─ Meta-analytic synthesis (pooling across studies)
├─ Prior elicitation (expert knowledge integration)
├─ Posterior inference (credible intervals, probability statements)
└─ Continuous updating (Bayesian learning as evidence accumulates)

MVP INTEGRATION POINTS:
1. SD provides network structure → SEM identifies pathways → Evidence strength rated
2. SEM identifies moderators qualitatively → SD notes context-dependence
3. Network visualization shows pathway topology, not numerical simulation

PHASE 2 INTEGRATION POINTS:
1. SD provides network structure → SEM populates with effect sizes → Bayesian quantifies uncertainty
2. SEM identifies moderators → SD incorporates as context-adaptive parameters → Bayesian estimates moderation strength
3. Bayesian provides posterior samples → SD uses for Monte Carlo simulation → SEM validates against empirical patterns
```

### Concrete Example: CHW Intervention [Phase 2]

**⚠️ Note**: This example shows Phase 2 capabilities with effect sizes. MVP would show pathway topology only.

**User Scenario**: "Increase CHW capacity from 50 to 200 FTE in Boston"

**SD Contribution**:
```
1. Identify affected stocks:
   CHW_Capacity [structural]
   → Healthcare_Continuity [intermediate]
   → ED_Utilization [intermediate]  
   → ED_Visits [crisis endpoint]

2. Specify functional forms:
   CHW effect: Sigmoid (saturation at high capacity)
   Continuity effect: Linear (proportional relationship)
   ED effect: Multiplicative dampening (relative reduction)

3. Time dynamics:
   Year 1: CHW 50→100, 60% effect materialized
   Year 2: CHW 100→150, 90% effect
   Year 3: CHW 150→200, 100% effect
   Simulate forward to Year 3 equilibrium
```

**SEM Contribution**:
```
1. Effect size from literature:
   Base: β_CHW_Continuity = 0.35 [from meta-analysis of 12 studies]
   
2. Moderators from multi-group analysis:
   Healthcare_Integration: +0.12 (Boston has integrated system)
   Urban_Setting: +0.05 (urban healthcare density)
   Medicaid_Coverage: +0.08 (MA has generous Medicaid)
   
3. Adjusted effect for Boston:
   β_adjusted = 0.35 + 0.12 + 0.05 + 0.08 = 0.60

4. Mediation chain:
   CHW → Continuity → ED (indirect effect)
   NOT CHW → ED (limited direct effect)
```

**Bayesian Contribution**:
```
1. Meta-analytic synthesis:
   Prior: μ ~ N(0.35, 0.08²) [expert consensus]
   Data: 12 studies, pooled
   Posterior: μ = 0.38 [0.28, 0.48] [slightly higher than prior]

2. Boston-specific posterior:
   Adjust for moderators using hierarchical model
   Posterior: μ_Boston = 0.60 [0.45, 0.75]

3. Uncertainty propagation:
   Sample 1000 values from posterior
   For each: Simulate CHW→Continuity→ED cascade
   Result: ΔED_Visits = -4,200 [-6,800, -1,800] per year

4. Probability statements:
   P(ΔED < -2,000) = 97% [very likely to reduce ED visits]
   P(ΔED < -5,000) = 42% [chance of large reduction]
```

**Integrated Output to User**:
```
Intervention: Scale CHWs 50→200 FTE
Cost: $6M (3-year total)

Projected Impact (3-year):
├─ ED Visits Prevented: 4,200 per year (95% CrI: 1,800-6,800)
│  └─ Mechanism: CHW improves healthcare continuity → reduces ED visits
├─ Health Value: $5.04M (ED visits × $1,200 each)
├─ Cost-Effectiveness: $1,429 per ED visit prevented
├─ ROI: 0.84 (health value / cost)
└─ Equity: 68% of ED prevention benefits Black residents (literature-derived population moderator)

Sensitivity:
├─ If effect 20% lower: 3,360 ED visits prevented (ROI: 0.67)
├─ If effect 20% higher: 5,040 ED visits prevented (ROI: 1.01)
└─ Robust: All scenarios show substantial ED reduction

Confidence: HIGH
├─ 12 studies supporting CHW→Continuity pathway
├─ Effect consistent across studies (I² = 48%, moderate heterogeneity)
└─ Boston context amplifies effect (integrated system, generous Medicaid)

[Click to see mechanism chain details]
[Click to see source studies]
[Click to adjust assumptions]
```

**What the User Sees**: Clean, interpretable projection with uncertainty quantified

**What Happened Behind the Scenes**: SD structure + SEM empirics + Bayesian uncertainty = integrated inference

---

## Epistemological Foundations

### Pragmatic Realism

**Position**: We adopt pragmatic realism—models are useful simplifications of reality, not perfect representations.

**Implications**:
1. **Bounded Rationality**: We cannot model everything. Pick ~400 nodes that matter most for health outcomes.
2. **Satisficing**: Seek "good enough" accuracy, not perfect precision. 95% CrI = [1,800, 6,800] is useful even though wide.
3. **Iterative Refinement**: Models improve as evidence accumulates. Version 1.0 → 2.0 → 3.0 through Bayesian updating.
4. **Transparency Over False Precision**: Better to say "we estimate ±30% uncertainty" than pretend exact prediction.

### Causal Pluralism

**Position**: Multiple valid causal interpretations can coexist. Context matters.

**Implications**:
1. **Mechanism Heterogeneity**: Effect varies by context (policy, demographics, implementation). We model this explicitly via moderators.
2. **Multi-Scale Causation**: Structural determinants (Medicaid policy) AND individual actions (healthcare seeking) both matter. We integrate levels.
3. **No Single Truth**: Bayesian credible intervals reflect epistemic uncertainty—we don't know the true effect exactly, and that's okay.

### Structural Competency

**Position**: Health disparities are products of systems, not individual deficits.

**Implications**:
1. **Root Cause Focus**: Mechanisms trace from structural origins (policy, economic systems, spatial arrangements).
2. **Equity as Analytic Core**: Population stratification is primary, not secondary. Disparities guide intervention selection.
3. **Power and Politics Matter**: Implementation quality, enforcement, community control affect outcomes. We flag these as moderators but don't control them.

### Transparent Uncertainty

**Position**: Uncertainty is inevitable. Hiding it destroys credibility.

**Implications**:
1. **Explicit Confidence Intervals**: Every projection has CI/CrI. No point estimates without uncertainty bounds.
2. **Sensitivity Analysis**: Show how results change with assumption variations. Robustness check.
3. **Evidence Quality Flags**: High-confidence mechanisms (12+ studies, I²<50%) vs. low-confidence (2 studies, qualitative).
4. **No Black Boxes**: User can click through to source studies, understand where numbers come from.

---

## Practical Implications

### For Users

**What This Means**:
- You don't need to understand SD, SEM, or Bayesian stats to use the platform
- System handles complexity behind the scenes
- You see: projections with uncertainty, mechanism chains, source studies
- You control: intervention specifications, assumption adjustments, scenario comparisons

**What You Should Understand**:
- Wider confidence intervals = more uncertainty (use caution in decision-making)
- Mechanisms are context-dependent (effect in Boston ≠ effect in rural Mississippi)
- Models are simplifications (some local factors may not be captured)
- Validation matters (compare predictions to actual outcomes over time)

### For Developers

**Implementation Requirements**:
1. **SD Engine**: Solve equilibrium equations, simulate time dynamics, handle feedback loops
2. **SEM Integration**: Parse literature effect sizes, apply moderators, calculate mediated effects
3. **Bayesian Backend**: Run MCMC for meta-analysis, sample posteriors for uncertainty propagation
4. **Optimization**: Linearized approximation + iterative refinement for speed
5. **Validation**: Automated checks (convergence, plausibility, consistency)

**Technology Stack**:
- Python: System dynamics simulation, network operations, user interface
- R + Stan: Bayesian meta-analysis, MCMC sampling
- PostgreSQL: Mechanism bank storage
- Git: Version control for mechanisms

### For Scientists

**Research Opportunities**:
1. **Methodological Papers**: Publish integration approach in methods journals
2. **Validation Studies**: Compare predictions to real-world outcomes
3. **Mechanism Discovery**: Contribute new mechanisms via LLM-assisted literature synthesis
4. **Equity Analysis**: Use platform to identify structural leverage points for disparity reduction

**Quality Standards**:
- Every mechanism traceable to peer-reviewed literature
- Effect sizes defensible via meta-analytic synthesis
- Uncertainty quantified via Bayesian inference
- Reproducible via git version control

---

## Document Metadata

**Version History**:
- v1.0 (2024-06): Initial methodological framework
- v2.0 (2025-11): Expanded integration details, added practical implications, clarified epistemology

**Related Documents**:
- [01_PROJECT_FOUNDATIONS.md] - Why this integration matters
- [04_STOCK_FLOW_PARADIGM.md] - SD implementation details
- [08_EFFECT_SIZE_TRANSLATION.md] - SEM effect size handling
- [10_LLM_EFFECT_QUANTIFICATION.md] - Bayesian meta-analysis in LLM pipeline

**Key References**:
- Sterman, J. (2000). *Business Dynamics: Systems Thinking and Modeling for a Complex World*. McGraw-Hill.
- Kline, R. B. (2015). *Principles and Practice of Structural Equation Modeling*. Guilford Press.
- Gelman, A. et al. (2013). *Bayesian Data Analysis*. CRC Press.

**Last Reviewed**: November 15, 2025  
**Next Review**: May 15, 2026

---

**END OF DOCUMENT**
