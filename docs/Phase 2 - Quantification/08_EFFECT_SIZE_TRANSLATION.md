# 08: Effect Size Translation
**Converting Epidemiological Evidence to Systems Dynamics Parameters**

---

## 1. Overview

Academic literature reports causal effects in diverse formats: odds ratios, relative risks, regression coefficients, hazard ratios, percentage changes, and qualitative themes. This document specifies how to **extract**, **standardize**, and **translate** these effect sizes into Systems Dynamics mechanism parameters that govern stock flows.

**Core Challenge**: Transform epidemiological effect sizes (which describe associations between exposures and outcomes) into **functional form parameters** (α terms) that quantify how one stock level influences another in the dynamic network.

---

## 2. Effect Size Taxonomy

### 2.1 Common Reporting Formats

| Format | Symbol | Common Use | Interpretation | Example |
|--------|--------|------------|----------------|---------|
| **Odds Ratio** | OR | Case-control, logistic regression | Odds of outcome in exposed / odds in unexposed | OR = 1.34 means 34% higher odds |
| **Relative Risk** | RR | Cohort studies, prospective | Risk of outcome in exposed / risk in unexposed | RR = 1.28 means 28% higher risk |
| **Hazard Ratio** | HR | Survival analysis, time-to-event | Instantaneous risk ratio over time | HR = 1.45 means 45% higher hazard |
| **Regression Coefficient** | β | Multiple regression, SEM | Change in outcome per unit exposure | β = 0.24 means 0.24 SD increase |
| **Cohen's d** | d | Meta-analysis, intervention trials | Standardized mean difference | d = 0.50 means 0.5 SD difference |
| **Percentage Change** | % | Policy evaluations, program effects | Relative or absolute change | "15% reduction in ED visits" |
| **Correlation** | r | Cross-sectional associations | Linear association strength | r = 0.35 means moderate positive association |

### 2.2 Study Design Quality Weighting

Effect size credibility depends on study design:

```
Quality Score (0-4):
├─ RCT (Randomized Controlled Trial): 4
├─ Cohort (Prospective): 3.5
├─ Cohort (Retrospective): 3
├─ Cross-sectional with strong controls: 2.5
├─ Cross-sectional: 2
└─ Qualitative / Case study: 1

Adjustment Factor:
  If study has high selection bias, information bias, or unmeasured confounding:
    Downweight by 0.5-1.0 points
  
  If multiple studies (meta-analysis):
    Weight by inverse variance (precision-weighted pooling)
```

**Application**: Higher-quality studies receive proportionally more weight when multiple effect sizes are available for the same mechanism.

---

## 3. Standardization Pipeline

All effect sizes are converted to a **common intermediate metric** before translation to SD parameters. The primary intermediate metric is **Cohen's d** (standardized mean difference), chosen for:
- Interpretability across domains
- Established conversion formulas from other metrics
- Direct comparability in meta-analytic pooling

### 3.1 Conversion Formulas

#### **Odds Ratio → Cohen's d**

```
d = ln(OR) / (π/√3)

where π/√3 ≈ 1.814 (constant for logistic distribution assumption)

Example:
  OR = 1.34 (95% CI: 1.12 - 1.61)
  ├─ d = ln(1.34) / 1.814 = 0.293 / 1.814 = 0.162
  └─ CI: d_lower = ln(1.12) / 1.814 = 0.062
           d_upper = ln(1.61) / 1.814 = 0.262
```

**Caveat**: For high-prevalence outcomes (>20%), OR overstates effect. Apply correction:
```
If baseline prevalence p₀ known:
  Convert OR to RR first: RR = OR / [(1 - p₀) + (p₀ × OR)]
  Then convert RR → d
```

---

#### **Relative Risk → Cohen's d**

```
d = ln(RR) / √(p₀(1 - p₀))

where p₀ = baseline risk in unexposed group

Example:
  RR = 1.28 (95% CI: 1.05 - 1.56), p₀ = 0.15 (15% baseline ED visit rate)
  ├─ d = ln(1.28) / √(0.15 × 0.85)
  ├─ d = 0.247 / 0.357 = 0.692
  └─ CI: d_lower = ln(1.05) / 0.357 = 0.137
           d_upper = ln(1.56) / 0.357 = 1.245

If p₀ unknown:
  Conservative approach: Assume p₀ = 0.50
    d ≈ 2 × ln(RR)
```

**Note**: RR-to-d conversion requires baseline risk. If unavailable, use meta-analytic average or similar geography estimates.

---

#### **Hazard Ratio → Cohen's d**

```
d = ln(HR) / 1.65

(Approximation based on log-normal survival distribution)

Example:
  HR = 1.45 (95% CI: 1.18 - 1.78)
  ├─ d = ln(1.45) / 1.65 = 0.371 / 1.65 = 0.225
  └─ CI: d_lower = ln(1.18) / 1.65 = 0.101
           d_upper = ln(1.78) / 1.65 = 0.345
```

---

#### **Regression Coefficient (Standardized β) → Cohen's d**

```
Already standardized: d ≈ β

Example:
  β = 0.24 (SE = 0.06)
  ├─ d = 0.24
  └─ CI: [0.24 - 1.96×0.06, 0.24 + 1.96×0.06] = [0.12, 0.36]
```

**Unstandardized Coefficients**:
```
If b (unstandardized) reported with exposure SD (σₓ) and outcome SD (σᵧ):
  β = b × (σₓ / σᵧ)
  d = β

If SDs unavailable:
  Request user input or use domain-typical values (e.g., housing quality: σ = 2.0 on 0-10 scale)
```

---

#### **Percentage Change → Cohen's d**

```
Context-dependent conversion:

Type A: Percentage Point Change (absolute)
  "Intervention reduced ED visits from 20% to 15%" → Δ = -5 percentage points
  d = Δ / √(p₀(1 - p₀))
  d = -0.05 / √(0.20 × 0.80) = -0.05 / 0.40 = -0.125

Type B: Relative Percentage Change
  "Intervention reduced ED visits by 25%" → RR = 0.75
  Convert via RR → d formula
```

---

#### **Correlation (r) → Cohen's d**

```
d = 2r / √(1 - r²)

Example:
  r = 0.35
  ├─ d = 2(0.35) / √(1 - 0.35²) = 0.70 / 0.937 = 0.747

Caution: Correlations lack directional causality. Use only when:
  1. Temporal sequence established (exposure precedes outcome)
  2. Confounding controlled via regression
  3. No alternative effect size available
```

---

### 3.2 Confidence Interval Propagation

All conversions preserve uncertainty:

```
For any transformation f: EffectSize → d
├─ d_point = f(ES_point)
├─ d_lower = f(ES_lower)
└─ d_upper = f(ES_upper)

Standard error:
  SE_d = (d_upper - d_lower) / (2 × 1.96)

For Monte Carlo simulation:
  Sample d ~ Normal(μ = d_point, σ = SE_d)
```

---

## 4. Translation to Systems Dynamics Parameters

Once standardized to Cohen's d, effect sizes must translate to **mechanism functional form parameters** (the α terms in stock-flow equations).

### 4.1 Three Translation Approaches

The optimal approach depends on mechanism functional form and outcome type.

---

#### **Approach A: Direct Parameter Replacement**

**Use When**: Mechanism describes direct stock-to-stock influence with linear or near-linear relationship

**Method**: Set α = d (Cohen's d becomes the flow coefficient)

```
Functional Form:
  ΔS_j = α × S_i

Translation:
  α = d_standardized

Example: Healthcare Continuity → ED Visit Prevention
  Literature: d = 0.35 (improved continuity reduces ED risk)
  Mechanism: ΔED_Visits = -0.35 × ΔHealthcare_Continuity
```

**Constraints**:
- Requires outcome measured on comparable scale (0-1 index)
- Assumes linear relationship (no saturation, no threshold)
- Best for: Intermediate node → Intermediate node connections

---

#### **Approach B: Multiplicative Modifier**

**Use When**: Mechanism scales with population size or baseline event rate

**Method**: Translate d to relative risk, then apply to baseline rate

```
Functional Form:
  ΔOutcome = Baseline_Outcome × Population × (RR - 1) × f(S_i)

Translation:
  1. Convert d → RR: RR = exp(d × √(p₀(1 - p₀)))
  2. Calculate attributable risk: AR = Baseline × (RR - 1)
  3. Scale by stock change: ΔOutcome = AR × Population × ΔS_i

Example: Community Health Workers → ED Visit Reduction
  Literature: d = 0.35, p₀ = 0.20 (baseline ED visit rate)
  ├─ RR = exp(0.35 × √(0.20 × 0.80)) = exp(0.140) = 1.15
  ├─ AR = 0.20 × (1.15 - 1) = 0.03 (3% attributable increase in access)
  └─ If CHW capacity increases by ΔS = 0.20 (from 0.50 to 0.70):
      ΔED_Visits_Prevented = 5000 visits/year × 0.03 × 0.20 = 30 visits/year
```

**Constraints**:
- Requires baseline outcome rate (visits, hospitalizations, deaths)
- Assumes outcomes scale linearly with population
- Best for: Intermediate node → Crisis endpoint connections

---

#### **Approach C: Probabilistic Translation**

**Use When**: Mechanism operates via probability shifts (e.g., eviction risk, insurance loss)

**Method**: Translate effect size to probability change, then calculate expected events

```
Functional Form:
  ΔEvents = Population × (p₁ - p₀)

Translation:
  1. Calculate p₀ (baseline probability, e.g., eviction rate = 2%)
  2. Calculate p₁ from RR or OR: p₁ = p₀ × RR (or solve from OR)
  3. Multiply by population affected

Example: Eviction Protection → Housing Stability
  Literature: OR = 0.65 (protection reduces eviction odds by 35%)
  ├─ p₀ = 0.02 (2% eviction rate in unprotected tenants)
  ├─ Convert OR to RR: RR = OR / [(1 - p₀) + (p₀ × OR)] = 0.65 / 0.993 = 0.655
  ├─ p₁ = 0.02 × 0.655 = 0.0131
  ├─ Δp = p₁ - p₀ = -0.0069 (0.69 percentage point reduction)
  └─ If 10,000 tenants affected:
      Evictions prevented = 10,000 × 0.0069 = 69 evictions/year
```

**Constraints**:
- Requires population-at-risk estimation
- Assumes independent events (no clustering)
- Best for: Policy node → Intermediate node connections

---

### 4.2 Functional Form Compatibility

Different functional forms require different translation strategies:

| Functional Form | Primary Translation | Rationale |
|-----------------|---------------------|-----------|
| **Sigmoid** | Direct Parameter (α sets sigmoid steepness) | Effect size determines how quickly stock transitions from low to high |
| **Logarithmic** | Direct Parameter (α scales diminishing returns) | Effect size sets amplitude of log curve |
| **Saturating Linear** | Multiplicative Modifier (α × capacity change) | Effect size determines slope before saturation |
| **Threshold-Activated** | Multiplicative Modifier (α × above-threshold amount) | Effect size scales post-threshold effect |
| **Multiplicative Dampening** | Direct Parameter (α in dampening factor) | Effect size determines rate of saturation approach |

**Example: Sigmoid Function**
```
ΔS_j = α × [1 / (1 + e^(-k(S_i - threshold)))]

Parameter α derived from d:
  α = d_standardized × scaling_factor

where scaling_factor adjusts for stock units:
  If S_j measured on 0-1 scale: scaling_factor = 1.0
  If S_j measured as count: scaling_factor = max_expected_change
```

---

## 5. Population Stratification

Effect sizes often vary by demographic subgroups. The system must:
1. Detect stratified effects in literature
2. Store subgroup-specific effect sizes
3. Apply appropriate effect size based on user-specified population

### 5.1 Stratification Dimensions

```
Primary Stratification:
├─ Race/Ethnicity: Black, Latinx, White, Asian, Native, Multi-racial
├─ Socioeconomic Status: <100% FPL, 100-200% FPL, >200% FPL
├─ Age: 0-17, 18-39, 40-64, 65+
├─ Insurance Status: Medicaid, Medicare, Private, Uninsured
└─ Geography: Urban, Suburban, Rural

Secondary Stratification (Phase 2):
├─ Gender/Sex: Female, Male, Non-binary
├─ Immigrant Status: US-born, Foreign-born, Documented, Undocumented
├─ Disability Status: With disability, Without disability
└─ Housing Status: Renter, Owner, Unhoused
```

### 5.2 Stratified Effect Encoding

```json
{
  "mechanism_id": "housing_quality_to_respiratory_health",
  "base_effect": {
    "d": 0.28,
    "ci": [0.18, 0.38],
    "population": "general_adult"
  },
  "stratified_effects": [
    {
      "stratum": "race_black",
      "d": 0.42,
      "ci": [0.28, 0.56],
      "modifier": 1.50,
      "rationale": "Higher baseline exposure to mold, lead; structural racism in housing maintenance"
    },
    {
      "stratum": "race_white",
      "d": 0.21,
      "ci": [0.10, 0.32],
      "modifier": 0.75,
      "rationale": "Lower exposure rates; better landlord responsiveness"
    },
    {
      "stratum": "ses_below_100_fpl",
      "d": 0.38,
      "ci": [0.25, 0.51],
      "modifier": 1.36,
      "rationale": "Limited resources for remediation; concentrated in lower-quality units"
    }
  ]
}
```

### 5.3 Population-Weighted Effect Application

When user specifies target population, system applies weighted average:

```
User Input:
  Geography: Boston
  Population: 45,000 low-income adults
  Demographics: 40% Black, 35% Latinx, 20% White, 5% Other

Weighted Effect Calculation:
  d_weighted = Σ (proportion_i × d_i)
  
  Example:
    d_weighted = (0.40 × 0.42) + (0.35 × 0.35) + (0.20 × 0.21) + (0.05 × 0.28)
    d_weighted = 0.168 + 0.123 + 0.042 + 0.014 = 0.347

Alternative: Stratified Outcome Reporting
  Instead of weighted average, calculate outcomes separately for each stratum:
    Black population (18,000): Uses d = 0.42
    Latinx population (15,750): Uses d = 0.35
    White population (9,000): Uses d = 0.21
  
  Output: Stratified impact table showing differential effects
```

**Equity Insight**: Stratified effects reveal which populations benefit most from interventions, enabling equity-centered targeting.

---

## 6. Moderator Adjustment Mathematics

Moderators alter effect sizes based on contextual factors (policy environment, implementation quality, local conditions).

### 6.1 Moderator Structure

```json
{
  "mechanism_id": "chw_to_healthcare_continuity",
  "base_effect": {
    "d": 0.35,
    "ci": [0.22, 0.48]
  },
  "moderators": [
    {
      "moderator_name": "chw_clinic_integration",
      "categories": [
        {"value": "embedded_in_clinic", "multiplier": 1.30},
        {"value": "standalone_program", "multiplier": 1.00},
        {"value": "outsourced_contractor", "multiplier": 0.75}
      ]
    },
    {
      "moderator_name": "provider_continuity",
      "categories": [
        {"value": "low_turnover", "multiplier": 1.15},
        {"value": "moderate_turnover", "multiplier": 1.00},
        {"value": "high_turnover", "multiplier": 0.85}
      ]
    }
  ]
}
```

### 6.2 Multiplicative Moderator Application

```
Adjusted Effect:
  d_adjusted = d_base × Π(moderator_multipliers)

Example:
  Base effect: d = 0.35
  Context: CHW embedded in clinic (1.30×), low provider turnover (1.15×)
  
  d_adjusted = 0.35 × 1.30 × 1.15 = 0.523

Confidence Interval Adjustment:
  CI_adjusted = [d_lower × Π(moderators), d_upper × Π(moderators)]
  CI_adjusted = [0.22 × 1.495, 0.48 × 1.495] = [0.33, 0.72]
```

**Rationale**: Multiplicative adjustment assumes moderators interact (e.g., clinic integration AND provider continuity together amplify effects more than either alone).

### 6.3 Additive Moderator Application (Alternative)

```
Adjusted Effect:
  d_adjusted = d_base + Σ(moderator_increments)

Example:
  Base effect: d = 0.35
  Context: CHW embedded in clinic (+0.10), low provider turnover (+0.05)
  
  d_adjusted = 0.35 + 0.10 + 0.05 = 0.50
```

**Use When**: Moderators are independent factors that don't interact.

**MVP Decision**: Use multiplicative for most mechanisms (conservative assumption that context matters multiplicatively). Allow user override to additive if empirical evidence supports independence.

---

## 7. Meta-Analytic Pooling

When multiple studies estimate the same mechanism, pool effect sizes using inverse-variance weighting.

### 7.1 Fixed-Effects Meta-Analysis

```
Pooled Effect:
  d_pooled = Σ(w_i × d_i) / Σ(w_i)

where w_i = 1 / SE_i² (inverse variance weight)

Example:
  Study 1: d = 0.32, SE = 0.08 → w₁ = 1 / 0.08² = 156.25
  Study 2: d = 0.28, SE = 0.12 → w₂ = 1 / 0.12² = 69.44
  Study 3: d = 0.40, SE = 0.10 → w₃ = 1 / 0.10² = 100.00
  
  d_pooled = (156.25×0.32 + 69.44×0.28 + 100.00×0.40) / (156.25 + 69.44 + 100.00)
  d_pooled = (50.00 + 19.44 + 40.00) / 325.69 = 0.336

Pooled SE:
  SE_pooled = √(1 / Σ(w_i)) = √(1 / 325.69) = 0.055

95% CI:
  [0.336 - 1.96×0.055, 0.336 + 1.96×0.055] = [0.228, 0.444]
```

---

### 7.2 Random-Effects Meta-Analysis

**Use When**: Heterogeneity exists across studies (I² > 50%)

```
Step 1: Calculate between-study variance (τ²)
  Q = Σ[w_i × (d_i - d_pooled)²]
  τ² = max(0, (Q - df) / C)
  where C = Σ(w_i) - Σ(w_i²) / Σ(w_i)

Step 2: Adjust weights
  w*_i = 1 / (SE_i² + τ²)

Step 3: Pool using adjusted weights
  d_pooled_random = Σ(w*_i × d_i) / Σ(w*_i)
```

**Output**: Random-effects pooling produces wider confidence intervals, appropriately reflecting between-study heterogeneity.

---

### 7.3 Heterogeneity Assessment

```
I² Statistic:
  I² = 100% × (Q - df) / Q
  
  Interpretation:
    I² < 25%: Low heterogeneity (effects are consistent)
    I² = 25-50%: Moderate heterogeneity
    I² = 50-75%: Substantial heterogeneity
    I² > 75%: High heterogeneity (consider subgroup analysis)

Action:
  If I² > 50%:
    1. Investigate moderators (do effects differ by context?)
    2. Use random-effects pooling
    3. Report prediction interval (range of effects in future contexts)
  
  Prediction Interval:
    [d_pooled - 1.96×√(SE² + τ²), d_pooled + 1.96×√(SE² + τ²)]
```

---

## 8. Uncertainty Quantification

All effect sizes carry uncertainty that propagates through simulations.

### 8.1 Confidence Interval Storage

```json
{
  "mechanism_id": "housing_quality_to_respiratory_health",
  "effect_size": {
    "d_point": 0.28,
    "d_lower": 0.18,
    "d_upper": 0.38,
    "se": 0.051,
    "ci_type": "95%",
    "distribution": "normal"
  }
}
```

### 8.2 Monte Carlo Sampling

During simulation, sample effect sizes from distributions:

```python
import numpy as np

# For each mechanism in active network:
for mechanism in active_mechanisms:
    d_point = mechanism.effect_size.d_point
    se = mechanism.effect_size.se
    
    # Sample from normal distribution
    d_sampled = np.random.normal(loc=d_point, scale=se)
    
    # Translate to α parameter
    alpha = translate_d_to_alpha(d_sampled, mechanism.functional_form)
    
    # Calculate flow with sampled parameter
    flow = calculate_flow(source_stock, target_stock, alpha, mechanism)
```

**Monte Carlo Settings**:
- MVP: N = 100 simulations (balance speed and precision)
- Phase 2: N = 1000 simulations (high precision for publication-quality analyses)

---

## 9. Quality Assurance Checks

### 9.1 Plausibility Bounds

```
Check 1: Effect Size Magnitude
  If |d| > 1.5:
    Flag: "Unusually large effect; verify source"
  
Check 2: Confidence Interval Width
  If (d_upper - d_lower) > 1.0:
    Flag: "High uncertainty; consider additional studies"

Check 3: Direction Consistency
  If mechanism_direction = "positive" but d < 0:
    Flag: "Effect direction contradicts theory; review mechanism"

Check 4: Baseline Rate Plausibility
  If p₀ > 0.50 for supposedly rare outcome:
    Flag: "Baseline rate implausibly high; verify"
```

### 9.2 Validation Against Known Benchmarks

```
Benchmark Comparison:
  For well-studied mechanisms (e.g., smoking → lung cancer):
    Compare extracted d to established meta-analytic estimates
    If difference > 30%:
      Flag: "Effect deviates from meta-analytic consensus"
```

---

## 10. Special Cases

### 10.1 Zero Effect (Null Findings)

```json
{
  "mechanism_id": "community_gardens_to_diabetes_control",
  "effect_size": {
    "d_point": 0.02,
    "d_lower": -0.08,
    "d_upper": 0.12,
    "significance": "not_significant",
    "interpretation": "No detectable effect in literature"
  },
  "action": "exclude_from_mechanism_bank"
}
```

**Decision Rule**: Mechanisms with CI spanning zero and |d_point| < 0.10 are excluded (no evidence of effect).

---

### 10.2 Qualitative Evidence Only

```json
{
  "mechanism_id": "gentrification_to_community_displacement",
  "effect_size": {
    "type": "qualitative",
    "description": "Ethnographic studies document forced displacement, loss of social networks, increased stress",
    "quantification_method": "expert_consensus_range",
    "d_range": [0.30, 0.60],
    "confidence": "moderate"
  },
  "action": "use_with_uncertainty_flag"
}
```

**Expert Consensus Approach**:
1. Convene 3-5 domain experts
2. Present qualitative evidence
3. Request bounded effect size estimates (plausible range)
4. Use midpoint as d_point, range as CI
5. Flag as "expert-estimated" in outputs

---

### 10.3 Dose-Response Relationships

```
Non-Linear Effects:
  Literature reports: "Effect increases with exposure intensity"
  
  Encoding:
    Mechanism uses sigmoid or logarithmic functional form (not linear)
    α parameter derived from effect size at median exposure
    Functional form captures dose-response curvature
```

---

## 11. Integration with Mechanism Bank

### 11.1 Storage Schema

```json
{
  "mechanism_id": "eviction_to_healthcare_discontinuity",
  "source_node": "Housing_Stability",
  "target_node": "Healthcare_Continuity",
  "functional_form": "multiplicative_dampening",
  "literature_effect": {
    "original_format": "OR",
    "original_value": 2.34,
    "original_ci": [1.89, 2.89],
    "standardized_d": 0.468,
    "standardized_ci": [0.355, 0.581],
    "translation_method": "probabilistic",
    "alpha_parameter": 0.052,
    "studies": [
      {
        "authors": "Desmond et al.",
        "year": 2015,
        "doi": "10.1126/science.aaa4340",
        "sample_size": 8247,
        "study_design": "cohort"
      }
    ]
  },
  "moderators": [...],
  "stratified_effects": [...]
}
```

---

## 12. MVP Implementation Priorities

**Phase 1 (MVP)**:
- Support OR, RR, β, d conversions (covers 90% of literature)
- Fixed-effects meta-analysis (simpler computation)
- Multiplicative moderator adjustment
- Single translation approach per functional form (standardized mapping)
- Quality checks: magnitude bounds, direction consistency

**Phase 2 Enhancements**:
- Add HR, correlation, percentage change conversions
- Random-effects meta-analysis with heterogeneity diagnostics
- Additive and interactive moderator models
- Multi-method translation with automatic selection
- Publication bias detection (funnel plots, Egger's test)
- Bayesian meta-analysis for uncertainty refinement

---

## 13. Worked Example: End-to-End Translation

**Scenario**: Translating evidence for "Community Health Workers → Healthcare Continuity" mechanism

### Step 1: Literature Extraction
```
Study 1 (Kim et al., 2019): OR = 1.45 (95% CI: 1.18-1.78), N=3200, Cohort
Study 2 (Martinez et al., 2021): β = 0.32 (SE=0.09), N=1800, RCT
Study 3 (Johnson et al., 2020): RR = 1.28 (95% CI: 1.05-1.56), N=5000, Cohort
```

### Step 2: Standardization to Cohen's d
```
Study 1: d = ln(1.45) / 1.814 = 0.206
Study 2: d = 0.32 (already standardized)
Study 3: d = ln(1.28) / √(0.15×0.85) = 0.692 (assuming p₀=0.15)
```

### Step 3: Meta-Analytic Pooling
```
Weights: w₁ = 51.0, w₂ = 123.5, w₃ = 36.2
d_pooled = (51.0×0.206 + 123.5×0.32 + 36.2×0.692) / (51.0+123.5+36.2)
d_pooled = 0.322

SE_pooled = √(1 / 210.7) = 0.069
95% CI: [0.187, 0.457]
```

### Step 4: Moderator Adjustment
```
Context: Embedded CHW (1.30×), Low turnover (1.15×)
d_adjusted = 0.322 × 1.30 × 1.15 = 0.482
```

### Step 5: Translation to α Parameter
```
Functional Form: Multiplicative Dampening
  ΔHealthcare_Continuity = α × CHW_Capacity × (1 - HC_current / HC_max)

Translation:
  α = d_adjusted / scaling_factor
  α = 0.482 / 2.0 = 0.241 (assuming scaling normalizes to 0-1 stock range)
```

### Step 6: Storage in Mechanism Bank
```json
{
  "alpha_parameter": 0.241,
  "alpha_ci": [0.139, 0.343],
  "derived_from": "meta_analysis_3_studies",
  "context": "embedded_chw_low_turnover",
  "uncertainty": "moderate"
}
```

---

**Document Version**: 1.0  
**Cross-References**: `[05_MECHANISM_BANK_STRUCTURE.md]`, `[07_TIME_SIMULATION_FRAMEWORK.md]`, `[09_LLM_TOPOLOGY_DISCOVERY.md]`, `[10_LLM_EFFECT_QUANTIFICATION.md]`  
**Status**: Technical specification for MVP implementation
