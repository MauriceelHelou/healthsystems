# Mechanism Bank Structure
## Encoding Causal Pathways with Functional Forms, Parameters, and Moderators

**Document ID**: 05_MECHANISM_BANK_STRUCTURE.md  
**Version**: 2.1
**Last Updated**: December 6, 2025  
**Tier**: 2 - Core Technical Architecture

---

## Table of Contents

1. [Mechanism Definition](#mechanism-definition)
2. [Bidirectional Mechanism Encoding](#bidirectional-mechanism-encoding)
3. [Functional Form Specification](#functional-form-specification)
4. [Parameter Structure](#parameter-structure)
5. [Moderator Framework](#moderator-framework)
6. [Example Mechanisms](#example-mechanisms)
7. [Referential Integrity and Hierarchy](#referential-integrity-and-hierarchy)
8. [Version Control and Lineage](#version-control-and-lineage)

---

## Mechanism Definition

### What Is a Mechanism

**A mechanism is a directed causal edge connecting two stocks in the system, specifying how changes in the upstream stock affect the downstream stock.**

```
Mechanism = {
  from_node: Stock_i (upstream, causal)
  to_node: Stock_j (downstream, affected)
  functional_form: How Stock_i affects Stock_j
  parameters: Effect size, thresholds, saturation points
  moderators: Contextual factors that strengthen/weaken effect
  evidence: Literature sources, effect sizes, confidence intervals
  metadata: Version, reviewers, deployment status
}
```

**Key Principle**: Mechanisms are atomic causal relationships. Each mechanism represents ONE pathway from ONE stock to ONE other stock.

**Complex causal chains** are represented as sequences of mechanisms:
```
Eviction → Economic_Precarity [Mechanism 1]
Economic_Precarity → Healthcare_Discontinuity [Mechanism 2]
Healthcare_Discontinuity → ED_Visits [Mechanism 3]

Total pathway: Eviction → ED_Visits (via 3 mechanisms)
```

---

## Bidirectional Mechanism Encoding

### Two Separate Mechanism Records

**When Stock A and Stock B have bidirectional causal relationship, encode as TWO DISTINCT mechanisms.**

**Why**: Functional forms and parameters typically differ in each direction.

**Example: Healthcare Continuity ↔ Healthcare Seeking**

```yaml
# Forward mechanism: Continuity → Seeking
mechanism_id: "continuity_to_seeking"
from_node: "healthcare_continuity"
to_node: "healthcare_seeking_rate"
direction: "forward"

functional_form: "sigmoid"
# Logic: Better continuity encourages seeking (sigmoid: builds trust gradually)

parameters:
  alpha: 2.8  # Effect size: at full continuity, seeking = 2.8 visits/year/person
  L: 4.0      # Saturation: max seeking = 4 visits/year (realistic limit)
  k: 3.5      # Steepness
  x0: 0.60    # Midpoint: continuity = 0.60

equation: |
  ΔSeeking = alpha × (L / (1 + exp(-k × (Continuity - x0))))
```

```yaml
# Backward mechanism: Seeking → Continuity
mechanism_id: "seeking_to_continuity"
from_node: "healthcare_seeking_rate"
to_node: "healthcare_continuity"
direction: "backward"

functional_form: "threshold"
# Logic: Only if seeking rate exceeds threshold does it reinforce continuity
# (sporadic visits don't build continuity, regular engagement does)

parameters:
  alpha: 0.15
  threshold: 2.0  # Must seek at least 2 visits/year to affect continuity

equation: |
  ΔContinuity = alpha × max(0, Seeking - threshold)
```

**Implications**:
- Different functional forms appropriate for each direction
- Effect sizes differ (continuity → seeking stronger than seeking → continuity)
- Moderators may differ by direction
- Feedback loop behavior emerges from combination of both mechanisms

### Mechanism Directionality Labels

**For all mechanisms, specify direction explicitly**:

```yaml
direction: "forward" | "backward" | "horizontal"

Where:
  forward: Upstream (structural) → Downstream (outcomes)
  backward: Downstream → Upstream (feedback)
  horizontal: Same level of system (peer effects, lateral relationships)
```

**Examples by direction**:

**Forward (Structural → Outcomes)**:
```
Policy_Strength → Eviction_Rate
CHW_Capacity → Healthcare_Continuity
Housing_Quality → Respiratory_Health
Green_Space → Air_Quality
```

**Backward (Outcomes → Structural, feedback)**:
```
ED_Utilization → Hospital_Capacity_Expansion
Health_Status → Healthcare_Seeking
Income_Stability → Job_Training_Demand
```

**Horizontal (Peer/lateral)**:
```
Community_Trust → Organizing_Capacity
Neighborhood_Safety → Social_Cohesion
Provider_Network_Density → Referral_Completion
```

### Bidirectional Search Requirements (Discovery Pipeline)

**All mechanism discovery MUST search for evidence in BOTH directions for each node pair.**

This is a pipeline requirement—not just an encoding convention. The discovery process must:

1. **Search A→B**: Query literature for evidence that node A causes changes in node B
2. **Search B→A**: Query literature for evidence that node B causes changes in node A
3. **Create mechanisms in direction(s) with sufficient evidence**

**Direction Selection Rules**:
| Evidence Scenario | Action |
|-------------------|--------|
| Strong A→B, weak B→A | Create forward mechanism A→B only |
| Weak A→B, strong B→A | Create backward mechanism B→A only |
| Strong both directions | Create TWO separate mechanisms (one forward, one backward) |
| Weak both directions | Do not create mechanism |

**Evidence Strength Criteria**:
- **Strong**: ≥3 supporting citations, meta-analysis or multiple primary studies
- **Weak**: <3 citations or single observational study

**Why Bidirectional Search Matters**:
- Many relationships are bidirectional (e.g., unemployment ↔ alcohol use)
- Literature often studies one direction while feedback loop exists
- Structural interventions may have unexpected reverse effects
- Feedback loops are critical for system dynamics modeling

**File Naming for Backward Mechanisms**:
```
# Forward mechanism
{from_node}_to_{to_node}.yaml

# Backward mechanism (same nodes, reversed)
{to_node}_to_{from_node}.yaml
```

**Required YAML Field**:
```yaml
direction: "backward"  # Explicitly mark backward mechanisms
```

**Supporting Citations Requirement**:
All mechanisms must have **minimum 3 supporting citations**:
- For meta-analyses: Extract citations of key included studies
- For systematic reviews: Extract citations of representative primary studies
- For primary studies: Extract citations of corroborating prior studies

---

## Functional Form Specification

### Standard Template

```yaml
functional_form: "sigmoid" | "logarithmic" | "saturating_linear" | "threshold" | "multiplicative_dampening" | "linear"

equation: |
  # Mathematical expression
  # Using standard notation
  # With clear variable definitions

parameters:
  # List all parameters used in equation
  # With descriptions and typical ranges
```

### Form-Specific Templates

**Template 1: Sigmoid**
```yaml
functional_form: "sigmoid"
equation: |
  ΔStock_j = alpha × (L / (1 + exp(-k × (Stock_i - x0))))

parameters:
  alpha:
    value: 0.35
    description: "Base effect size from literature"
    confidence_interval: [0.22, 0.50]
    source: "Meta-analysis of 12 studies"
    
  L:
    value: 1.0
    description: "Saturation level (maximum achievable Stock_j)"
    source: "Theoretical maximum"
    
  k:
    value: 0.15
    description: "Steepness parameter (controls transition speed)"
    source: "Calibrated from typical intervention trajectories"
    
  x0:
    value: 150
    description: "Midpoint (50% of max effect at this Stock_i level)"
    source: "Expert judgment + literature on capacity thresholds"
```

**Template 2: Threshold**
```yaml
functional_form: "threshold"
equation: |
  ΔStock_j = alpha × max(0, Stock_i - threshold)

parameters:
  alpha:
    value: 0.28
    confidence_interval: [0.18, 0.38]
    source: "Meta-analysis"
    
  threshold:
    value: 0.50
    description: "Minimum Stock_i value for effect to occur"
    source: "Policy analysis literature"
    sensitivity: "Test range [0.40, 0.60]"
```

**Template 3: Multiplicative Dampening**
```yaml
functional_form: "multiplicative_dampening"
equation: |
  ΔStock_j = alpha × Stock_i × (1 - Stock_j / Max_Stock_j)

parameters:
  alpha:
    value: 0.25
    description: "Maximum proportional effect"
    confidence_interval: [0.18, 0.32]
    
  Max_Stock_j:
    value: 1.0
    description: "Theoretical maximum for Stock_j"
    source: "Normalized scale definition"
```

---

## Parameter Structure

### Base Parameters

**Every mechanism has base parameters from literature**:

```yaml
base_parameters:
  effect_size:
    metric: "Cohen's d" | "relative_risk" | "beta_coefficient" | "percentage_change"
    value: [point estimate]
    confidence_interval: [lower, upper]
    source_studies: [list of DOIs]
    heterogeneity: 
      i_squared: [0-100%]
      interpretation: "low" | "moderate" | "high"
    
  functional_form_parameters:
    # Specific to form (L, k, x0 for sigmoid; threshold for threshold; etc.)
```

### Context-Adjustment Parameters (Moderators)

**Parameters adjusted based on local context**:

```yaml
moderators:
  - moderator_type: "policy" | "demographic" | "geographic" | "implementation"
    factor_name: "specific moderator"
    adjustment_type: "additive" | "multiplicative"
    adjustment_value: [numeric]
    condition: "when this factor is present/high/etc."
    evidence: "source for this moderation"
```

**Example: CHW → Healthcare Continuity with moderators**

```yaml
base_effect_size: 0.35

moderators:
  - moderator_type: "policy"
    factor_name: "medicaid_work_requirements_absent"
    adjustment_type: "additive"
    adjustment_value: +0.08
    condition: "when Medicaid does not have work requirements"
    evidence: "Subgroup analysis in 3 studies showed stronger effects in expansion states"
    
  - moderator_type: "implementation"
    factor_name: "healthcare_system_integration"
    adjustment_type: "additive"
    adjustment_value: +0.12
    condition: "when CHWs embedded in integrated care system"
    evidence: "RCT comparison: integrated vs. standalone programs"
    
  - moderator_type: "geographic"
    factor_name: "urban_setting"
    adjustment_type: "multiplicative"
    adjustment_value: 0.95  # Slight reduction
    condition: "urban vs. rural"
    evidence: "Meta-regression shows 5% lower effect in urban areas (access baseline differences)"
    
  - moderator_type: "demographic"
    factor_name: "population_proportion_black"
    adjustment_type: "additive"
    adjustment_value: +0.09
    condition: "for Black populations specifically"
    evidence: "Stratified analysis in 6 studies"

# Boston calculation:
# Base: 0.35
# + Medicaid (no work req): +0.08
# + Integration (high): +0.12
# × Urban: ×0.95
# + Black pop moderator: +0.09
# = (0.35 + 0.08 + 0.12) × 0.95 + 0.09 = 0.6125 (Boston-specific effect)
```

### Parameter Bounds and Validation

**All parameters must have plausibility bounds**:

```yaml
validation:
  effect_size_bounds:
    minimum: -2.0  # Cohen's d: large negative effect
    maximum: 2.0   # Cohen's d: large positive effect
    plausibility_flag: "if |d| > 1.5, require extra scrutiny"
    
  functional_parameters:
    L_bounds: [0, 2.0]  # Saturation level
    k_bounds: [0.01, 5.0]  # Steepness
    threshold_bounds: [0, max_stock_value]
    
  consistency_checks:
    - "Confidence interval must contain point estimate"
    - "Heterogeneity I² must be between 0 and 100"
    - "Moderator adjustments must not produce implausible total effects"
```

---

## Moderator Framework

### Four Moderator Types

**Type 1: Policy Moderators**

Context-dependent policy features that reshape mechanism strength.

```yaml
Examples:
  - Medicaid expansion status (expanded vs. not)
  - Medicaid work requirements (present vs. absent)
  - Just-cause eviction protection (strong vs. weak)
  - Rent control coverage (high vs. low)
  - Healthcare reimbursement rates (adequate vs. low)
  - Criminal justice approach (reform vs. punitive)
```

**Application**: 
- User selects geography
- System auto-detects policy environment (or user inputs)
- Relevant policy moderators applied to all mechanisms

**Type 2: Demographic Moderators**

Population characteristics that modify effects.

```yaml
Examples:
  - Race/ethnicity (Black, Latinx, White, Asian, etc.)
  - Age group (children, working-age, elderly)
  - Insurance status (Medicaid, private, uninsured)
  - Income level (poverty, low-income, middle-income)
  - Language (English-speaking vs. limited English proficiency)
  - Immigration status (documented, undocumented, refugee)
```

**Application**:
- From literature: "Effect size for Black populations: 0.35 + 0.09"
- System applies population-specific effects
- Enables equity stratification: outcomes distributed by demographics

**Type 3: Geographic Moderators**

Place-based factors affecting mechanisms.

```yaml
Examples:
  - Urban vs. rural
  - Region (Northeast, South, Midwest, West)
  - Population density (high-density vs. low-density)
  - Healthcare access baseline (high vs. low)
  - Environmental conditions (pollution levels, climate)
```

**Application**:
- Based on geography specification
- Adjust mechanisms for place-based context
- Example: CHW effects differ in rural (transportation barriers) vs. urban (different access patterns)

**Type 4: Implementation Moderators**

Program/intervention quality factors.

```yaml
Examples:
  - Program fidelity (high vs. low adherence to model)
  - Staffing level (adequate vs. understaffed)
  - Integration into existing systems (integrated vs. standalone)
  - Funding stability (consistent vs. volatile)
  - Community engagement (high vs. low)
  - Training quality (comprehensive vs. minimal)
```

**Application**:
- User can specify implementation characteristics
- System adjusts projected effects accordingly
- Sensitivity analysis: test scenarios with high vs. low implementation quality

### Moderator Encoding in Mechanism File

```yaml
mechanism_id: "chw_healthcare_continuity"

base_effect:
  value: 0.35
  ci: [0.22, 0.50]

moderators:
  policy:
    - factor: "medicaid_work_requirements"
      present: -0.08
      absent: +0.08
      evidence: "doi:10.xxxx, stratified by Medicaid policy"
      
  demographic:
    - factor: "race_black"
      adjustment: +0.09
      interpretation: "Effect 1.26× stronger for Black populations"
      evidence: "doi:10.yyyy, race-stratified analysis"
      
    - factor: "age_elderly"
      adjustment: +0.05
      interpretation: "Slightly stronger for 65+ (trust-building easier)"
      evidence: "doi:10.zzzz, age subgroup analysis"
      
  geographic:
    - factor: "rural"
      adjustment: -0.05
      interpretation: "Slightly weaker in rural (transportation access matters)"
      evidence: "doi:10.aaaa, urban/rural comparison"
      
  implementation:
    - factor: "integration_level"
      low: -0.10
      medium: +0.00
      high: +0.12
      evidence: "doi:10.bbbb, RCT comparison integrated vs. standalone"
      
    - factor: "chw_training_quality"
      low: -0.08
      high: +0.06
      evidence: "doi:10.cccc, fidelity analysis"
```

---

## Example Mechanisms

> **Note**: All examples use canonical node IDs from `mechanism-bank/mechanisms/canonical_nodes.json`. See `Nodes/COMPLETE_NODE_INVENTORY.md` for complete node specifications.

### Example 1: Eviction Filing Rate → Emergency Department Visit Rate (Forward)

```yaml
mechanism_id: "eviction_filing_rate_to_emergency_department_visit_rate"
mechanism_class: "housing_to_health"
direction: "forward"

from_node:
  node_id: "eviction_filing_rate"  # Canonical node from inventory
  node_name: "Eviction Filing Rate"
  stock_unit: "Filings per 100 renter households annually"

to_node:
  node_id: "emergency_department_visit_rate"  # Canonical node from inventory
  node_name: "Emergency Department Visit Rate"
  stock_unit: "Visits per 1,000 population annually"

functional_form: "multiplicative_dampening"
equation: |
  ΔED_Visits = alpha × Eviction_Filing_Rate × (1 - ED_Visit_Rate / Max_ED_Rate)

  # Positive effect: higher eviction filings increase ED visits
  # Multiplicative: effect dampens as ED utilization approaches maximum
  # Captures displacement-induced healthcare disruption

base_parameters:
  alpha:
    value: 0.028
    interpretation: "Per-unit eviction rate increases ED utilization proportionally"
    confidence_interval: [0.018, 0.038]
    metric: "Standardized effect"
    source_studies:
      - doi: "10.1111/2024-eviction-health-smith"
        effect: "RR=1.34 for ED visits"
        converted_to: "d=0.28"
      - doi: "10.2222/2023-housing-instability-jones"
        effect: "β=0.24"
      # [10 more studies]

    meta_analysis:
      method: "Bayesian random-effects"
      heterogeneity_i2: 62%
      publication_bias: "Egger test p=0.18 (minimal bias)"

  Max_ED_Rate:
    value: 500
    description: "Maximum plausible ED visits per 1,000 population"

moderators:
  policy:
    - factor: "just_cause_eviction_protection"  # Canonical node
      strong_protection: -0.08  # Reduces effect by 0.08
      weak_protection: 0.00
      condition: "just_cause_eviction_protection = 1 (policy in effect)"
      evidence: "doi:10.3333/2024-eviction-policy"
      mechanism_explanation: "Just-cause protection reduces eviction instability, blunts health disruption"

  demographic:
    - factor: "race_black"
      adjustment: +0.09  # Effect 1.32× stronger for Black populations
      evidence: "doi:10.4444/2024-racial-disparities"
      mechanism_explanation: "Eviction effects compound with discrimination, limited wealth reserves"

  geographic:
    - factor: "medicaid_coverage_generosity_index"  # Canonical node
      generous: -0.05  # Reduces effect when index > 70
      restrictive: +0.03  # Amplifies effect when index < 40
      evidence: "doi:10.5555/2023-medicaid-eviction"

temporal_dynamics:
  immediate_effect: 0.05  # Acute stress, immediate disruption
  cumulative_effect: 0.28  # Full effect over 12 months
  latency: "Effects materialize over 6-12 months as housing instability cascades"

validation:
  expert_reviews:
    - reviewer: "Dr. Sarah Chen, Housing & Health Epidemiology"
      date: "2024-06-15"
      status: "Approved"
      comments: "Effect size plausible, moderators well-justified, temporal dynamics align with literature"
      
    - reviewer: "James Martinez, Community Organizer"
      date: "2024-06-16"
      status: "Approved"
      comments: "Mechanism reflects lived experience of tenants; racial disparity moderator critical"

  sensitivity_analysis:
    effect_size_range: [0.018, 0.038]
    robust_to_outliers: true
    geographic_validation: "Effect consistent across 5 cities studied"

version: "1.2"
git_commit: "8f3a2e1"
deployment_date: "2024-06-17"
last_updated: "2025-10-12"
update_notes: "Added temporal dynamics specification, refined moderators based on 2025 literature"
```

### Example 2: Primary Care Physician Density → Preventable Hospitalization (Forward, Sigmoid)

```yaml
mechanism_id: "primary_care_physician_density_to_preventable_hospitalization_individual"
mechanism_class: "healthcare_infrastructure_to_outcomes"
direction: "forward"

from_node:
  node_id: "primary_care_physician_density"  # Canonical node
  node_name: "Primary Care Physician Density"
  stock_unit: "Physicians per 100,000 population"

to_node:
  node_id: "preventable_hospitalization_individual"  # Canonical node
  node_name: "Preventable Hospitalization (Individual)"
  stock_unit: "ACSC admissions per 1,000 population"

functional_form: "sigmoid"
equation: |
  ΔPreventable_Hosp = -alpha × (L / (1 + exp(-k × (PCP_Density - x0))))

rationale: "Sigmoid captures: slow initial effect (minimal access), rapid mid-range reduction (critical mass of providers), saturation at high density (diminishing returns)"

base_parameters:
  alpha:
    value: 0.35
    confidence_interval: [0.22, 0.50]
    source_studies: [12 RCTs and cohort studies]
    meta_analysis: "Bayesian random-effects, I²=48%"

  L:
    value: 0.70
    description: "Maximum reduction: 70% of preventable hospitalizations can be averted"

  k:
    value: 0.08
    description: "Steepness: moderate transition rate"

  x0:
    value: 80
    description: "Midpoint: 80 PCPs per 100k is inflection point"
    source: "Calibrated from HRSA shortage area thresholds"

moderators:
  policy:
    - factor: "medicaid_expansion_status"  # Canonical node
      expanded: +0.08
      not_expanded: -0.05

  implementation:
    - factor: "care_coordination_quality"
      low: -0.10
      medium: 0.00
      high: +0.12

  demographic:
    - factor: "population_black"
      adjustment: +0.09  # Effect stronger for historically underserved populations

# [Additional sections similar to Example 1]
```

### Example 3: Housing Quality Index → Asthma Hospitalization Rate (Forward, Threshold)

```yaml
mechanism_id: "housing_quality_index_to_asthma_hospitalization_rate"
mechanism_class: "built_environment_to_health"
direction: "forward"

from_node:
  node_id: "housing_quality_index_revised_consolidated"  # Canonical node
  node_name: "Housing Quality Index"
  stock_unit: "Index (0-1)"

to_node:
  node_id: "asthma_hospitalization_rate"  # Canonical node
  node_name: "Asthma Hospitalization Rate"
  stock_unit: "Hospitalizations per 100,000 population"

functional_form: "threshold"
equation: |
  ΔAsthma_Hosp = -alpha × max(0, Housing_Quality - threshold)

  # Negative relationship: higher housing quality reduces asthma hospitalizations
  # Threshold: quality must exceed minimum for protective effect

base_parameters:
  alpha:
    value: 0.25
    interpretation: "Each 0.10 increase in housing quality above threshold reduces asthma hospitalizations by 2.5%"
    confidence_interval: [0.18, 0.32]

  threshold:
    value: 0.40
    description: "Minimum housing quality for protective effect"
    source: "Based on EPA/HUD healthy homes standards"

moderators:
  policy:
    - factor: "housing_code_enforcement_stringency"
      high: +0.08  # Amplifies housing quality benefit
      low: -0.05

  demographic:
    - factor: "children_under_18"
      present: +0.12  # Stronger effect in households with children
      absent: 0.00

# [Additional sections]
```

---

## Referential Integrity and Hierarchy

### Node Bank Referential Integrity

**CRITICAL**: Mechanisms MUST reference nodes that exist in the Node Bank.

```python
# Validation rule (enforced at YAML load and API write)
def validate_mechanism_nodes(mechanism, node_bank):
    """Ensure mechanism nodes exist in node bank."""
    if mechanism.from_node_id not in node_bank:
        raise ValidationError(f"from_node '{mechanism.from_node_id}' not in Node Bank")
    if mechanism.to_node_id not in node_bank:
        raise ValidationError(f"to_node '{mechanism.to_node_id}' not in Node Bank")
```

**Why**: This constraint ensures:
- All mechanism endpoints are defined, validated nodes
- No orphan mechanisms referencing ad-hoc node names
- Consistent node metadata (scale, category, domains) across mechanisms
- Ability to query all mechanisms affecting a node

### Hierarchy Level Field

Mechanisms include a `hierarchy_level` field indicating the abstraction level:

| Level | Description | When to Use |
|-------|-------------|-------------|
| **leaf** | Connects specific/detailed nodes (default) | Most mechanisms |
| **parent** | Connects abstract/general nodes | Aggregated relationships |
| **cross** | Spans hierarchy levels | Abstract → specific pathways |

```yaml
# Example: Parent-level mechanism
mechanism_id: "substance_use_to_liver_disease"
hierarchy_level: "parent"  # Connects general concepts
from_node:
  node_id: "substance_use_disorder"  # Abstract parent node
to_node:
  node_id: "liver_disease"  # Abstract parent node

# Example: Leaf-level mechanism
mechanism_id: "binge_drinking_to_alcohol_poisoning"
hierarchy_level: "leaf"  # Connects specific nodes
from_node:
  node_id: "binge_drinking"  # Specific child node
to_node:
  node_id: "alcohol_poisoning"  # Specific child node
```

### No Automatic Aggregation

**Key principle**: Child mechanisms don't automatically "roll up" to parent levels.

If you want a mechanism visible at the parent level, you must explicitly define it. This ensures:
- Clear evidence attribution at each level
- Different effect sizes can be specified for abstract vs specific relationships
- No false precision from aggregation

---

## Version Control and Lineage

### Git-Based Version Control

**Every mechanism tracked in git repository**:

```
mechanisms/
├─ housing_to_health/
│   ├─ eviction_healthcare_discontinuity.yaml
│   ├─ housing_quality_respiratory.yaml
│   └─ README.md
├─ healthcare_to_outcomes/
└─ [organized by domain]

Git workflow:
1. Mechanism proposed (new file or update to existing)
2. Automated validation (schema check, parameter bounds)
3. Expert review (Pull Request with reviewers assigned)
4. Approval + merge to main branch
5. Deploy to production mechanism bank
6. Tag version (v1.2, v2.0, etc.)
```

### Lineage Tracking

**Every mechanism file includes full lineage**:

```yaml
lineage:
  discovery:
    method: "LLM-assisted literature synthesis"
    llm_version: "claude-3.5-sonnet-20241022"
    prompt_version: "v2.3"
    date: "2024-05-20"
    literature_corpus: "300+ papers on housing and health"
    
  effect_quantification:
    method: "Bayesian meta-analysis"
    studies_included: 12
    primary_studies: [DOI list]
    pooling_method: "Random-effects hierarchical model"
    software: "R cmdstanr v2.32"
    date: "2024-06-01"
    
  validation:
    automated_checks:
      - date: "2024-06-14"
        status: "PASSED"
        checks: ["schema valid", "parameters plausible", "citations valid"]
        
    expert_reviews:
      - reviewer: "Dr. Sarah Chen"
        expertise: "Housing and health epidemiology"
        date: "2024-06-15"
        status: "Approved"
        
      - reviewer: "James Martinez"
        expertise: "Community organizing, lived experience"
        date: "2024-06-16"
        status: "Approved"
        
  deployment:
    initial_version: "1.0"
    initial_deployment_date: "2024-06-17"
    git_commit: "8f3a2e1"
    
  updates:
    - version: "1.1"
      date: "2024-09-10"
      reason: "Added two new RCTs to meta-analysis"
      effect_change: "0.28 → 0.29 (minimal)"
      git_commit: "a4b2c8d"
      
    - version: "1.2"
      date: "2025-10-12"
      reason: "Refined moderators based on 2025 systematic review"
      changes: ["Added temporal dynamics", "Updated policy moderator"]
      git_commit: "e5f9g1h"
```

### Deprecation and Retirement

**When mechanisms need replacement**:

```yaml
status: "deprecated"
deprecation:
  date: "2026-01-15"
  reason: "New RCT evidence shows mechanism pathway incorrect"
  replacement_mechanism: "eviction_economic_stress_v2"
  transition_period: "6 months (allow users to update scenarios)"
  
sunset_date: "2026-07-15"  # After this, mechanism removed from active bank
archived_location: "mechanisms/deprecated/eviction_healthcare_discontinuity_v1.yaml"
```

---

---

## Canonical Node Reference

All mechanism definitions MUST reference canonical nodes from the node inventory. This ensures consistency and enables automated validation.

### Node Sources

| Source | Location | Use Case |
|--------|----------|----------|
| **Canonical Nodes JSON** | `mechanism-bank/mechanisms/canonical_nodes.json` | Quick lookup of 840 node IDs |
| **Complete Inventory** | `Nodes/COMPLETE_NODE_INVENTORY.md` | Full specifications with scales, domains, units |
| **Backend Utilities** | `backend/utils/canonical_nodes.py` | Programmatic node lookup |

### Mechanism ID Convention

Mechanism IDs should follow the pattern: `{from_node_id}_to_{to_node_id}`

Examples from this document:
- `eviction_filing_rate_to_emergency_department_visit_rate`
- `primary_care_physician_density_to_preventable_hospitalization_individual`
- `housing_quality_index_to_asthma_hospitalization_rate`

### Validation

Before saving a mechanism to the bank, verify:
1. `from_node.node_id` exists in `canonical_nodes.json`
2. `to_node.node_id` exists in `canonical_nodes.json`
3. Moderator node references (if any) exist in `canonical_nodes.json`

---

## Document Metadata

**Version History**:
- v1.0 (2024-06): Initial mechanism bank structure
- v2.0 (2025-11): Added bidirectional encoding, expanded moderator framework, version control specs
- v2.1 (2025-12): Updated all examples to use canonical node IDs
- v2.2 (2025-12): Added bidirectional search requirements for discovery pipeline, 3+ supporting citations requirement

**Related Documents**:
- [04_STOCK_FLOW_PARADIGM.md] - Node/stock specifications
- [08_EFFECT_SIZE_TRANSLATION.md] - Converting literature effects to parameters
- [09_LLM_TOPOLOGY_DISCOVERY.md] - How mechanisms discovered
- [10_LLM_EFFECT_QUANTIFICATION.md] - How effect sizes extracted
- [Canonical Nodes] `mechanism-bank/mechanisms/canonical_nodes.json`
- [Node Specifications] `Nodes/COMPLETE_NODE_INVENTORY.md`

**Last Reviewed**: December 2, 2025
**Next Review**: March 2, 2026

---

**END OF DOCUMENT**
