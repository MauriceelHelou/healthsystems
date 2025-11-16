# 10: LLM Effect Quantification
**Meta-Analytic Pooling and Bayesian Uncertainty Synthesis**

---

## 1. Overview

This document specifies how Large Language Models (LLMs) extract, standardize, and synthesize effect sizes from literature to populate mechanism parameters. The process transforms diverse statistical formats (OR, RR, β, HR, %) into unified effect size estimates with confidence intervals, enabling quantitative Systems Dynamics modeling.

**Core Innovation**: LLM-mediated effect size extraction scales from researcher-led review (weeks per mechanism) to automated synthesis (hours for entire bank), while maintaining statistical rigor through meta-analytic pooling and Bayesian uncertainty quantification.

---

## 2. Architecture Overview

### 2.1 Four-Stage Quantification Pipeline

```
Stage 1: EFFECT SIZE EXTRACTION
├─ Input: Mechanism with supporting studies (from Document 09)
├─ Process: LLM parses full-text PDFs to extract effect sizes, CIs, sample sizes
├─ Output: Raw effect sizes in original reporting format (OR, RR, β, etc.)
└─ Duration: ~30 seconds per study with Claude Opus 4

Stage 2: STANDARDIZATION TO COHEN'S d
├─ Input: Raw effect sizes in diverse formats
├─ Process: Apply conversion formulas (see Document 08)
├─ Output: All effects standardized to Cohen's d with propagated CIs
└─ Duration: <1 second per effect (deterministic calculation)

Stage 3: META-ANALYTIC POOLING
├─ Input: Multiple standardized effect sizes for same mechanism
├─ Process: Inverse-variance weighted pooling (fixed or random effects)
├─ Output: Pooled effect size with confidence interval
└─ Duration: <5 seconds per mechanism

Stage 4: BAYESIAN UNCERTAINTY SYNTHESIS
├─ Input: Pooled effect size + heterogeneity statistics
├─ Process: Bayesian posterior estimation with informative priors
├─ Output: Posterior distribution for Monte Carlo sampling
└─ Duration: ~10 seconds per mechanism (MCMC sampling)

Total: ~2-5 minutes per mechanism (assuming 3-5 supporting studies)
```

**Scalability**: 100 mechanisms × 5 minutes = ~8 hours for complete effect quantification pipeline.

---

## 3. Stage 1: Effect Size Extraction

### 3.1 LLM Prompt: Full-Text Parsing

**System Prompt**:
```
You are a meta-analyst extracting effect sizes from academic papers. Your task is to identify the PRIMARY effect size for a specified mechanism and extract all relevant statistical information.

CRITICAL: Extract ONLY the effect size for the specified mechanism. Do NOT extract:
- Baseline descriptive statistics
- Covariate effects (unless the covariate IS the mechanism)
- Secondary outcomes
- Subgroup analyses (unless explicitly requested)
```

**User Prompt Template**:
```
STUDY: {full_text_or_abstract}

MECHANISM: {mechanism_description}
Example: "Community health workers improve healthcare continuity and access"

EXTRACT:
1. effect_size_value: Numeric value of primary effect
2. effect_size_type: "OR" | "RR" | "HR" | "beta" | "cohen_d" | "percentage" | "correlation"
3. confidence_interval: [lower, upper] if reported
4. standard_error: If reported (if not, calculate from CI)
5. sample_size: Total N for analysis
6. outcome_definition: How was the outcome measured?
   Example: "Healthcare continuity = ≥1 primary care visit in past 12 months"
7. exposure_definition: How was the exposure measured?
   Example: "CHW assignment = randomized to CHW contact vs. usual care"
8. adjustment_variables: List of covariates controlled in analysis
9. effect_location: Quote the exact sentence(s) reporting the effect
10. statistical_significance: p-value if reported

CONSTRAINTS:
- If multiple models reported, extract the FULLY ADJUSTED model (controls for most covariates)
- If multiple time points, extract the LONGEST FOLLOW-UP effect
- If effect not present for this mechanism, return NULL with explanation

OUTPUT: JSON only (no preamble)
{
  "effect_size_value": ...,
  "effect_size_type": ...,
  ...
}
```

**Example Extraction**:
```json
{
  "effect_size_value": 1.38,
  "effect_size_type": "OR",
  "confidence_interval": [1.12, 1.71],
  "standard_error": 0.107,
  "sample_size": 3200,
  "outcome_definition": "≥1 primary care visit in past year (binary)",
  "exposure_definition": "CHW program participation (binary)",
  "adjustment_variables": [
    "age", "sex", "race/ethnicity", "insurance_type", "baseline_health_status"
  ],
  "effect_location": "Table 3, Model 4: Adjusted OR for primary care utilization = 1.38 (95% CI: 1.12-1.71, p=0.003)",
  "statistical_significance": 0.003
}
```

### 3.2 Multi-Study Extraction Workflow

```python
def extract_effects_for_mechanism(mechanism, supporting_studies):
    """
    Extract effect sizes from all supporting studies for a mechanism
    """
    extracted_effects = []
    
    for study in supporting_studies:
        # Retrieve full text or abstract
        study_text = retrieve_document(study['doi'])
        
        # LLM extraction
        response = call_llm(
            model="claude-opus-4",
            system_prompt=EFFECT_EXTRACTION_SYSTEM,
            user_prompt=EFFECT_EXTRACTION_TEMPLATE.format(
                full_text_or_abstract=study_text,
                mechanism_description=mechanism['mechanism_description']
            ),
            temperature=0.1  # Very low for precision
        )
        
        effect = json.loads(response)
        
        # Validate extraction
        if effect and validate_effect(effect):
            effect['study_metadata'] = study
            extracted_effects.append(effect)
        else:
            log_extraction_failure(study, reason=effect.get('explanation'))
    
    return extracted_effects
```

### 3.3 Extraction Quality Checks

```python
def validate_effect(effect):
    """
    Automated validation of LLM extraction
    """
    checks = []
    
    # Check 1: Effect size in plausible range
    if effect['effect_size_type'] == "OR" and not (0.1 < effect['effect_size_value'] < 10):
        checks.append("FAIL: OR outside plausible range [0.1, 10]")
    
    # Check 2: CI properly ordered
    if effect['confidence_interval']:
        ci_lower, ci_upper = effect['confidence_interval']
        if not (ci_lower < effect['effect_size_value'] < ci_upper):
            checks.append("FAIL: CI ordering invalid")
    
    # Check 3: Sample size reasonable
    if not (10 < effect['sample_size'] < 1000000):
        checks.append("WARN: Sample size unusual")
    
    # Check 4: Effect location contains numeric value
    if effect['effect_location'] and str(effect['effect_size_value']) not in effect['effect_location']:
        checks.append("WARN: Effect value not found in quoted text")
    
    # Check 5: SE matches CI width
    if effect['standard_error'] and effect['confidence_interval']:
        expected_se = (effect['confidence_interval'][1] - effect['confidence_interval'][0]) / (2 * 1.96)
        if abs(effect['standard_error'] - expected_se) / expected_se > 0.1:
            checks.append("WARN: SE doesn't match CI width")
    
    return len([c for c in checks if c.startswith("FAIL")]) == 0
```

**Handling Failures**:
- **FAIL checks**: Quarantine effect for manual review
- **WARN checks**: Include in meta-analysis but flag uncertainty
- **NULL extractions**: Document reason (mechanism not studied in this paper)

---

## 4. Stage 2: Standardization to Cohen's d

**Process**: Apply conversion formulas from Document 08 to transform all effect sizes to common metric.

```python
from effect_size_translation import convert_to_cohens_d

def standardize_effects(extracted_effects):
    """
    Convert all effects to Cohen's d
    """
    standardized = []
    
    for effect in extracted_effects:
        # Apply conversion based on original format
        d_point, d_ci = convert_to_cohens_d(
            value=effect['effect_size_value'],
            effect_type=effect['effect_size_type'],
            ci=effect['confidence_interval'],
            baseline_risk=estimate_baseline_risk(effect)
        )
        
        standardized.append({
            "study_id": effect['study_metadata']['doi'],
            "d_point": d_point,
            "d_lower": d_ci[0],
            "d_upper": d_ci[1],
            "se": (d_ci[1] - d_ci[0]) / (2 * 1.96),
            "n": effect['sample_size'],
            "original_format": effect['effect_size_type'],
            "original_value": effect['effect_size_value']
        })
    
    return standardized
```

**Output**: All effects on comparable Cohen's d scale, ready for pooling.

---

## 5. Stage 3: Meta-Analytic Pooling

### 5.1 Fixed-Effects Meta-Analysis

**Use When**: Heterogeneity low (I² < 50%), studies measure same population/context

```python
import numpy as np

def fixed_effects_meta_analysis(standardized_effects):
    """
    Inverse-variance weighted pooling
    """
    # Calculate weights (inverse of variance)
    weights = [1 / (e['se'] ** 2) for e in standardized_effects]
    
    # Pooled effect
    d_pooled = np.sum([w * e['d_point'] for w, e in zip(weights, standardized_effects)]) / np.sum(weights)
    
    # Pooled SE
    se_pooled = np.sqrt(1 / np.sum(weights))
    
    # 95% CI
    ci_pooled = [d_pooled - 1.96 * se_pooled, d_pooled + 1.96 * se_pooled]
    
    return {
        "d_pooled": d_pooled,
        "se_pooled": se_pooled,
        "ci_pooled": ci_pooled,
        "method": "fixed_effects"
    }
```

**Example**:
```
Study 1: d = 0.32, SE = 0.08, w = 156.25
Study 2: d = 0.28, SE = 0.12, w = 69.44
Study 3: d = 0.40, SE = 0.10, w = 100.00

d_pooled = (156.25×0.32 + 69.44×0.28 + 100×0.40) / (156.25 + 69.44 + 100)
         = (50.00 + 19.44 + 40.00) / 325.69
         = 0.336

SE_pooled = √(1 / 325.69) = 0.055
CI_pooled = [0.228, 0.444]
```

---

### 5.2 Random-Effects Meta-Analysis

**Use When**: Heterogeneity moderate to high (I² ≥ 50%), studies vary in populations/contexts

```python
def random_effects_meta_analysis(standardized_effects):
    """
    DerSimonian-Laird random-effects pooling
    """
    # Step 1: Calculate Q statistic (heterogeneity)
    weights_fixed = [1 / (e['se'] ** 2) for e in standardized_effects]
    d_fixed = np.sum([w * e['d_point'] for w, e in zip(weights_fixed, standardized_effects)]) / np.sum(weights_fixed)
    
    Q = np.sum([w * (e['d_point'] - d_fixed) ** 2 for w, e in zip(weights_fixed, standardized_effects)])
    df = len(standardized_effects) - 1
    
    # Step 2: Estimate between-study variance (τ²)
    C = np.sum(weights_fixed) - np.sum([w**2 for w in weights_fixed]) / np.sum(weights_fixed)
    tau_squared = max(0, (Q - df) / C)
    
    # Step 3: Adjust weights
    weights_random = [1 / (e['se'] ** 2 + tau_squared) for e in standardized_effects]
    
    # Step 4: Pool with adjusted weights
    d_pooled = np.sum([w * e['d_point'] for w, e in zip(weights_random, standardized_effects)]) / np.sum(weights_random)
    se_pooled = np.sqrt(1 / np.sum(weights_random))
    ci_pooled = [d_pooled - 1.96 * se_pooled, d_pooled + 1.96 * se_pooled]
    
    # Step 5: Calculate I² (percent of variation due to heterogeneity)
    I_squared = max(0, 100 * (Q - df) / Q)
    
    return {
        "d_pooled": d_pooled,
        "se_pooled": se_pooled,
        "ci_pooled": ci_pooled,
        "tau_squared": tau_squared,
        "I_squared": I_squared,
        "method": "random_effects"
    }
```

**Interpretation of I²**:
```
I² < 25%:  Low heterogeneity (use fixed effects)
I² = 25-50%: Moderate heterogeneity (consider random effects)
I² = 50-75%: Substantial heterogeneity (use random effects)
I² > 75%:  High heterogeneity (investigate moderators, subgroup analyses)
```

---

### 5.3 Heterogeneity Investigation

**When I² > 50%**, investigate sources of variation:

**LLM Prompt: Heterogeneity Explanation**
```
SYSTEM: You are investigating why effect sizes vary across studies.

CONTEXT: Meta-analysis shows I² = {I_squared}%, indicating substantial heterogeneity.

STUDIES:
{list_of_studies_with_effects}

TASK: Identify potential moderators explaining effect size variation:
1. Study design differences (RCT vs. cohort vs. observational)
2. Population characteristics (age, race/ethnicity, SES, geography)
3. Intervention characteristics (intensity, duration, fidelity)
4. Outcome measurement (different definitions, follow-up periods)
5. Context factors (policy environment, time period, setting)

For EACH moderator, provide:
- Description of variation
- Which studies show higher/lower effects
- Estimated effect multiplier (if quantifiable)

OUTPUT: JSON array of moderators
[
  {
    "moderator_name": "urban_vs_rural",
    "description": "CHW programs more effective in urban settings",
    "studies_urban": ["Smith 2022", "Jones 2020"],
    "effect_urban": 0.42,
    "studies_rural": ["Garcia 2023"],
    "effect_rural": 0.15,
    "multiplier_rural": 0.36
  },
  ...
]
```

**Outcome**: Moderators identified in Stage 3 are encoded in mechanism bank (see Document 12 for geographic contextualization).

---

### 5.4 Publication Bias Detection

**Funnel Plot Asymmetry**:
```python
def assess_publication_bias(standardized_effects):
    """
    Detect systematic bias toward positive/large effects
    """
    # Egger's regression test
    from scipy.stats import linregress
    
    effect_sizes = [e['d_point'] for e in standardized_effects]
    standard_errors = [e['se'] for e in standardized_effects]
    precisions = [1/se for se in standard_errors]
    
    # Regress effect size on precision
    slope, intercept, r_value, p_value, std_err = linregress(precisions, effect_sizes)
    
    # Significant intercept suggests asymmetry
    bias_detected = p_value < 0.10
    
    # Trim-and-fill correction (if bias detected)
    if bias_detected:
        adjusted_effects = trim_and_fill(standardized_effects)
        return {
            "bias_detected": True,
            "egger_p": p_value,
            "adjustment": "trim_and_fill_applied",
            "adjusted_d": meta_analyze(adjusted_effects)['d_pooled']
        }
    else:
        return {
            "bias_detected": False,
            "egger_p": p_value
        }
```

**Interpretation**:
- **p < 0.10**: Likely publication bias (small studies with null results unpublished)
- **Action**: Report both unadjusted and trim-and-fill adjusted estimates
- **Conservative approach**: Use adjusted estimate for mechanism bank

---

## 6. Stage 4: Bayesian Uncertainty Synthesis

### 6.1 Rationale for Bayesian Approach

**Why Bayesian?**
1. **Informative priors**: Incorporate domain knowledge (e.g., "effects rarely exceed d=1.0")
2. **Uncertainty propagation**: Full posterior distribution (not just point + CI)
3. **Small sample robustness**: Stabilizes estimates when N studies is low
4. **Coherent prediction intervals**: Accounts for both within-study and between-study uncertainty

### 6.2 Prior Specification

```python
from scipy.stats import norm, halfnorm

def specify_priors(mechanism_type):
    """
    Set informative priors based on mechanism category
    """
    priors = {
        "structural_policy": {
            "d_mean": 0.30,
            "d_sd": 0.20,
            "rationale": "Structural policies show moderate effects (d~0.2-0.5)"
        },
        "healthcare_access": {
            "d_mean": 0.35,
            "d_sd": 0.25,
            "rationale": "Access interventions vary widely (d~0.1-0.6)"
        },
        "behavioral_intervention": {
            "d_mean": 0.25,
            "d_sd": 0.30,
            "rationale": "Behavioral effects smaller, more variable"
        },
        "environmental_exposure": {
            "d_mean": 0.20,
            "d_sd": 0.15,
            "rationale": "Environmental effects well-established, less variable"
        }
    }
    
    # Default: weakly informative prior
    if mechanism_type not in priors:
        return {"d_mean": 0.25, "d_sd": 0.30}
    
    return priors[mechanism_type]
```

### 6.3 Bayesian Meta-Analysis

```python
import pymc as pm

def bayesian_meta_analysis(standardized_effects, prior):
    """
    Hierarchical Bayesian model for effect size estimation
    """
    with pm.Model() as model:
        # Hyperpriors (population-level)
        mu = pm.Normal('mu', mu=prior['d_mean'], sigma=prior['d_sd'])
        tau = pm.HalfNormal('tau', sigma=0.3)  # Between-study SD
        
        # Study-level effects
        theta = pm.Normal('theta', mu=mu, sigma=tau, shape=len(standardized_effects))
        
        # Likelihood (observed effects)
        for i, effect in enumerate(standardized_effects):
            pm.Normal(f'obs_{i}', mu=theta[i], sigma=effect['se'], observed=effect['d_point'])
        
        # Sample from posterior
        trace = pm.sample(2000, tune=1000, return_inferencedata=True, progressbar=False)
    
    # Extract posterior summary
    posterior_mu = trace.posterior['mu'].values.flatten()
    
    return {
        "d_posterior_mean": float(np.mean(posterior_mu)),
        "d_posterior_median": float(np.median(posterior_mu)),
        "d_posterior_sd": float(np.std(posterior_mu)),
        "ci_95": [float(np.percentile(posterior_mu, 2.5)), float(np.percentile(posterior_mu, 97.5))],
        "prediction_interval_95": [
            float(np.percentile(posterior_mu, 2.5) - 1.96*np.mean(trace.posterior['tau'].values)),
            float(np.percentile(posterior_mu, 97.5) + 1.96*np.mean(trace.posterior['tau'].values))
        ],
        "posterior_samples": posterior_mu.tolist()  # For Monte Carlo in Document 07
    }
```

**Output Components**:
- **Posterior mean**: Best point estimate (incorporates prior + data)
- **95% credible interval**: Range of plausible population effects
- **95% prediction interval**: Range for NEW study (wider, accounts for heterogeneity)
- **Posterior samples**: 2000 draws for Monte Carlo uncertainty propagation

### 6.4 Sensitivity to Prior

```python
def prior_sensitivity_analysis(standardized_effects):
    """
    Test robustness to prior specification
    """
    priors = [
        {"d_mean": 0.25, "d_sd": 0.30, "label": "weakly_informative"},
        {"d_mean": 0.30, "d_sd": 0.20, "label": "moderately_informative"},
        {"d_mean": 0.00, "d_sd": 1.00, "label": "uninformative"}
    ]
    
    results = {}
    for prior in priors:
        bayes_result = bayesian_meta_analysis(standardized_effects, prior)
        results[prior['label']] = bayes_result['d_posterior_mean']
    
    # Check if posteriors differ by >10%
    max_diff = max(results.values()) - min(results.values())
    sensitivity = "low" if max_diff < 0.05 else "moderate" if max_diff < 0.10 else "high"
    
    return {
        "sensitivity": sensitivity,
        "results_by_prior": results,
        "interpretation": "Use weakly informative prior" if sensitivity == "low" else "Data too sparse; results sensitive to prior"
    }
```

---

## 7. Moderator Quantification

### 7.1 Subgroup Meta-Analysis

When heterogeneity investigation identifies moderators, perform **subgroup-specific pooling**:

```python
def subgroup_meta_analysis(standardized_effects, moderator):
    """
    Pool effects separately for each moderator level
    """
    subgroups = {}
    
    for effect in standardized_effects:
        # Classify study into subgroup
        subgroup_value = classify_study(effect['study_metadata'], moderator)
        
        if subgroup_value not in subgroups:
            subgroups[subgroup_value] = []
        subgroups[subgroup_value].append(effect)
    
    # Meta-analyze each subgroup
    results = {}
    for subgroup, effects in subgroups.items():
        if len(effects) >= 2:  # Need at least 2 studies
            pooled = random_effects_meta_analysis(effects)
            results[subgroup] = pooled
    
    # Calculate effect multipliers
    baseline_effect = results.get('baseline', {}).get('d_pooled', 0.30)
    for subgroup, pooled in results.items():
        results[subgroup]['multiplier'] = pooled['d_pooled'] / baseline_effect
    
    return results
```

**Example Output**:
```json
{
  "moderator": "urban_vs_rural",
  "subgroups": {
    "urban": {
      "d_pooled": 0.42,
      "ci_pooled": [0.28, 0.56],
      "n_studies": 5,
      "multiplier": 1.40
    },
    "rural": {
      "d_pooled": 0.15,
      "ci_pooled": [0.05, 0.25],
      "n_studies": 2,
      "multiplier": 0.50
    }
  }
}
```

### 7.2 Meta-Regression

**For continuous moderators** (e.g., intervention intensity, follow-up duration):

```python
from scipy.optimize import minimize

def meta_regression(standardized_effects, moderator_values):
    """
    Model effect size as function of continuous moderator
    """
    def negative_log_likelihood(params):
        beta_0, beta_1, tau_sq = params
        
        ll = 0
        for i, effect in enumerate(standardized_effects):
            predicted_d = beta_0 + beta_1 * moderator_values[i]
            variance = effect['se']**2 + tau_sq
            ll += -0.5 * np.log(2 * np.pi * variance) - 0.5 * (effect['d_point'] - predicted_d)**2 / variance
        
        return -ll
    
    # Optimize
    result = minimize(negative_log_likelihood, x0=[0.3, 0.1, 0.05], bounds=[(0, 1), (-1, 1), (0, 1)])
    beta_0, beta_1, tau_sq = result.x
    
    return {
        "intercept": beta_0,
        "slope": beta_1,
        "residual_heterogeneity": tau_sq,
        "interpretation": f"Each unit increase in {moderator_name} associated with {beta_1:.3f} increase in effect size"
    }
```

---

## 8. Uncertainty Classification

### 8.1 Confidence Rating

```python
def classify_uncertainty(pooled_result, n_studies, I_squared):
    """
    Assign confidence rating based on evidence base
    """
    # Factor 1: Number of studies
    if n_studies >= 5:
        study_score = 3
    elif n_studies >= 3:
        study_score = 2
    else:
        study_score = 1
    
    # Factor 2: Heterogeneity
    if I_squared < 25:
        hetero_score = 3
    elif I_squared < 50:
        hetero_score = 2
    else:
        hetero_score = 1
    
    # Factor 3: CI width
    ci_width = pooled_result['ci_pooled'][1] - pooled_result['ci_pooled'][0]
    if ci_width < 0.20:
        precision_score = 3
    elif ci_width < 0.40:
        precision_score = 2
    else:
        precision_score = 1
    
    # Aggregate
    total_score = study_score + hetero_score + precision_score
    
    if total_score >= 8:
        return "high_confidence"
    elif total_score >= 5:
        return "moderate_confidence"
    else:
        return "low_confidence"
```

**Interpretation**:
- **High confidence**: Use point estimate for projections; narrow uncertainty
- **Moderate confidence**: Use point estimate but widen CI by 20% for conservative projections
- **Low confidence**: Consider excluding from MVP or use only with expert review

---

## 9. Output Structure

### 9.1 Complete Mechanism Record

```json
{
  "mechanism_id": "L2_014_to_L3_028_chw_to_healthcare_continuity",
  "source_node": "Community_Health_Workers",
  "target_node": "Healthcare_Continuity",
  "effect_quantification": {
    "extraction_summary": {
      "n_studies_extracted": 5,
      "n_studies_meta_analyzed": 5,
      "extraction_failures": 0
    },
    "meta_analysis": {
      "method": "random_effects",
      "d_pooled": 0.336,
      "se_pooled": 0.055,
      "ci_95": [0.228, 0.444],
      "I_squared": 42.3,
      "tau_squared": 0.012,
      "publication_bias": {
        "detected": false,
        "egger_p": 0.23
      }
    },
    "bayesian_synthesis": {
      "d_posterior_mean": 0.340,
      "d_posterior_median": 0.339,
      "ci_95": [0.235, 0.448],
      "prediction_interval_95": [0.15, 0.53],
      "prior_used": "weakly_informative",
      "sensitivity_to_prior": "low"
    },
    "moderators": [
      {
        "moderator_name": "chw_clinic_integration",
        "subgroups": {
          "embedded_in_clinic": {
            "d_pooled": 0.442,
            "multiplier": 1.30
          },
          "standalone_program": {
            "d_pooled": 0.340,
            "multiplier": 1.00
          }
        }
      }
    ],
    "confidence_rating": "moderate_confidence",
    "uncertainty_flags": [
      "Moderate heterogeneity (I²=42%)",
      "Only 2 studies in rural settings"
    ]
  },
  "supporting_studies": [
    {
      "doi": "10.2105/AJPH.2022.306798",
      "extracted_effect": {
        "original_format": "OR",
        "original_value": 1.38,
        "standardized_d": 0.322
      }
    }
  ]
}
```

---

## 10. Quality Assurance

### 10.1 Automated Validation

```python
def validate_quantification(mechanism):
    """
    QA checks before deployment
    """
    errors = []
    warnings = []
    
    quant = mechanism['effect_quantification']
    
    # Check 1: Pooled effect in plausible range
    if abs(quant['meta_analysis']['d_pooled']) > 1.5:
        warnings.append("Unusually large effect size")
    
    # Check 2: Bayesian and frequentist agree
    diff = abs(quant['bayesian_synthesis']['d_posterior_mean'] - quant['meta_analysis']['d_pooled'])
    if diff > 0.10:
        warnings.append("Bayesian and frequentist estimates diverge")
    
    # Check 3: Sufficient studies
    if quant['extraction_summary']['n_studies_meta_analyzed'] < 2:
        errors.append("Insufficient studies for meta-analysis")
    
    # Check 4: CI properly bounded
    ci = quant['meta_analysis']['ci_95']
    if not (ci[0] < quant['meta_analysis']['d_pooled'] < ci[1]):
        errors.append("CI ordering invalid")
    
    return {"errors": errors, "warnings": warnings}
```

---

## 11. MVP Implementation Priorities

**Phase 1 (MVP)**:
- LLM extraction from full-text PDFs (Claude Opus 4)
- Fixed-effects and random-effects meta-analysis
- Bayesian synthesis with weakly informative priors
- Publication bias detection (Egger's test)
- Subgroup analysis for categorical moderators
- Confidence rating (high/moderate/low)

**Phase 2 Enhancements**:
- Meta-regression for continuous moderators
- Network meta-analysis (comparing multiple interventions)
- Individual participant data (IPD) meta-analysis
- Multivariate meta-analysis (multiple correlated outcomes)
- Prior sensitivity analysis (automated)
- Missing data imputation

---

## 12. Integration with Translation Pipeline

**Handoff to Document 08**:

Once effect sizes are quantified with confidence intervals:
1. Standardized d values translate to Systems Dynamics parameters (α terms)
2. Moderator multipliers apply to base effect sizes
3. Posterior distributions feed Monte Carlo simulations (Document 07)
4. Confidence ratings guide which mechanisms enter MVP

**Data Flow**:
```
09_LLM_TOPOLOGY_DISCOVERY.md
  ↓ (Mechanisms + literature citations)
10_LLM_EFFECT_QUANTIFICATION.md
  ↓ (d_pooled + CI + moderators)
08_EFFECT_SIZE_TRANSLATION.md
  ↓ (α parameters for functional forms)
05_MECHANISM_BANK_STRUCTURE.md
  ↓ (Deployed mechanism bank)
```

---

**Document Version**: 1.0  
**Cross-References**: `[09_LLM_TOPOLOGY_DISCOVERY.md]`, `[08_EFFECT_SIZE_TRANSLATION.md]`, `[11_LLM_MECHANISM_VALIDATION.md]`, `[07_TIME_SIMULATION_FRAMEWORK.md]`  
**Status**: Technical specification for MVP implementation
