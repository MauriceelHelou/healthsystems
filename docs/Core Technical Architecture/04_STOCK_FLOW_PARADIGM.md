# Stock-Flow Paradigm
## Node Representation, Stock Types, and Functional Forms

**Document ID**: 04_STOCK_FLOW_PARADIGM.md
**Version**: 2.0
**Last Updated**: November 15, 2025
**Tier**: 2 - Core Technical Architecture

---

## ⚠️ MVP vs. Phase 2 Scope

**MVP (Phase 1)**: Stock-Flow Structure with Topology Only
- ✓ All nodes represented as stocks with units
- ✓ Stock types (real, proxy, crisis endpoint) specified
- ✓ Mechanism directions (+/−) between stocks identified
- ✓ Functional forms documented (for Phase 2 implementation)
- ✗ **NO numerical equilibrium calculation** (requires effect sizes)
- ✗ **NO stock level simulation** (requires quantified flows)

**Phase 2**: Adds Numerical Simulation
- Effect sizes enable flow rate calculation
- Equilibrium solver computes baseline stock levels
- Time simulation projects stock changes post-intervention
- Uncertainty propagation through stock-flow network

**This Document's Role**: Establishes stock-flow conceptual framework that MVP will use for network visualization and that Phase 2 will use for numerical simulation.

---

## Table of Contents

1. [Overview](#overview)
2. [Stock Representation Principles](#stock-representation-principles)
3. [Three Stock Types](#three-stock-types)
4. [Stock Units and Measurement](#stock-units-and-measurement)
5. [Functional Forms for Stock Transitions](#functional-forms-for-stock-transitions)
6. [30+ Concrete Node Examples](#30-concrete-node-examples)
7. [Implementation Specifications](#implementation-specifications)

---

## Overview

### Core Principle

**Every node in the system is represented as a stock—a measurable quantity that can accumulate, deplete, or remain stable over time.**

There is no distinction between "node strength" and "stock level":
- **Stock level IS the node's state** at any given time
- **Mechanisms determine stock flows** (rates of change)
- **Equilibrium occurs** when all flows balance (inflows = outflows)

### Why Stock-Flow Logic

**Advantages over abstract "node strength"**:
1. **Measurability**: Stocks have units (FTE, annual count, index 0-1)
2. **Comparability**: Can compare across geographies (Boston CHW = 50 FTE vs. Mississippi CHW = 12 FTE)
3. **Accountability**: Stocks tied to observable reality (ED visits = 122,400/year from hospital data)
4. **Interventions as capacity changes**: User directly manipulates stock levels (CHW 50→200 FTE)
5. **Equilibrium is meaningful**: System balances at levels producing observed outcomes

---

## Stock Representation Principles

### Principle 1: All Nodes Are Stocks

**No exceptions**: Whether structural, intermediate, or outcome—all represented as stocks with explicit units.

```
Examples:
✓ Community_Health_Workers: 50 FTE
✓ Healthcare_Continuity_Index: 0.45 (normalized 0-1)
✓ ED_Visits_Annual: 122,400 visits
✓ Policy_Strength: 7.2 out of 10
✓ Economic_Precarity_Rate: 0.38 (proportion of population)
```

### Principle 2: Stocks Have Explicit Units

**Every stock must specify**:
- **Unit of measurement**: What is being counted/measured
- **Scale**: Range of possible values
- **Type**: Real (direct) or proxy (constructed index)

```
Stock specification template:
node_id: unique_identifier
stock_name: "Human-readable name"
stock_unit: "FTE" | "index_0_1" | "annual_count" | "rate" | "per_100k" | etc.
stock_type: "real" | "proxy" | "crisis_endpoint"
measurement: "direct" | "constructed" | "calibrated"
typical_range: [min, max]
```

### Principle 3: Node Title ≠ Stock Unit

**The title describes what the node represents conceptually. The unit describes how it's measured.**

```
Example 1:
  Node Title: "Community Health Workers"
  Stock Unit: "FTE count"
  Measurement: Direct count of full-time equivalent positions
  
Example 2:
  Node Title: "Healthcare Continuity"
  Stock Unit: "Index (0-1)"
  Measurement: Weighted composite of insurance persistence, provider retention, appointment completion
  
Example 3:
  Node Title: "Eviction Risk"
  Stock Unit: "Annual eviction filings per 1000 renter households"
  Measurement: Court records / renter population
```

### Principle 4: Stocks Can Be Observable or Latent

**Observable stocks**: Measured directly from data
```
- ED_Visits: Hospital administrative data
- CHW_Count: Organizational records
- Population: Census
```

**Latent stocks**: Not directly observed, estimated via proxy or calibration
```
- Healthcare_Continuity: Constructed index from multiple indicators
- Community_Trust: Survey-derived or calibrated from outcomes
- Economic_Precarity: Composite measure or inferred from behavior
```

---

## Three Stock Types

### Type 1: Real Stocks (Direct Measurement)

**Definition**: Stocks with natural units directly observable in the world.

**Characteristics**:
- Have clear measurement protocol
- Data sources identifiable
- No construction required (just measure)
- Examples: counts, rates, physical quantities

**Sub-categories**:

**1a. Capacity Stocks** (infrastructure, resources)
```
Community_Health_Workers: 50 FTE
Hospital_Beds: 2,500 beds
Affordable_Housing_Units: 3,200 units
Public_Transportation_Routes: 85 routes
Social_Workers: 120 FTE
```

**1b. Flow Rate Stocks** (events per time)
```
ED_Visits_Annual: 122,400 visits/year
Eviction_Filings_Annual: 8,200 filings/year
Arrests_Annual: 15,600 arrests/year
Births_Annual: 9,400 births/year
Overdose_Events_Annual: 420 events/year
```

**1c. Prevalence Stocks** (proportion of population)
```
Uninsured_Rate: 0.08 (8% of population)
Unemployment_Rate: 0.11 (11%)
Food_Insecurity_Rate: 0.22 (22%)
Chronic_Disease_Prevalence: 0.35 (35%)
Housing_Cost_Burden_Rate: 0.42 (42% paying >30% income on housing)
```

**1d. Physical Condition Stocks** (environmental, spatial)
```
Air_Quality_Index: 48 (EPA AQI scale)
Green_Space_Acres_Per_100k: 125 acres
Lead_Paint_Housing_Proportion: 0.18
Water_Quality_Index: 82 (0-100 scale)
Walkability_Score: 65 (Walk Score methodology)
```

### Type 2: Proxy Index Stocks (Constructed)

**Definition**: Stocks with no natural unit, constructed from multiple measurable components.

**Characteristics**:
- Represent abstract concepts (trust, continuity, integration)
- Normalized to common scale (typically 0-1)
- Construction formula specified explicitly
- Components weighted by importance/correlation

**Construction Formula**:
```
General form:
Proxy_Index = Σ(weight_i × normalized_component_i)

Where:
- Components normalized to 0-1 scale
- Weights sum to 1.0
- Weights evidence-based (literature, expert judgment, empirical calibration)
```

**Examples**:

**2a. Healthcare Continuity Index**
```
Construction:
  Insurance_Persistence (0-1): proportion with stable coverage over 12 months
  Provider_Retention (0-1): proportion seeing same PCP over 12 months
  Appointment_Completion (0-1): proportion completing scheduled visits
  
  Healthcare_Continuity_Index = 
    0.40 × Insurance_Persistence +
    0.30 × Provider_Retention +
    0.30 × Appointment_Completion

Typical range: [0.2, 0.8]
Boston baseline: 0.45
```

**2b. Policy Strength Index**
```
Construction (for eviction protections):
  Just_Cause_Required (0-1): 1 if law exists, 0 if not
  Notice_Period_Days: normalized by max (90 days = 1.0)
  Legal_Representation_Availability (0-1): proportion eligible for free defense
  Rent_Control_Coverage (0-1): proportion units covered
  
  Eviction_Policy_Strength = 
    0.40 × Just_Cause_Required +
    0.20 × Notice_Period_Days_Normalized +
    0.25 × Legal_Representation +
    0.15 × Rent_Control_Coverage

Typical range: [0, 1]
Boston baseline: 0.72
```

**2c. Community Trust Index**
```
Construction:
  Survey_Trust_Score (0-1): normalized survey responses
  Civic_Participation_Rate (0-1): voting + meeting attendance
  Mutual_Aid_Density (0-1): # active mutual aid networks per 10k pop, normalized
  
  Community_Trust_Index =
    0.50 × Survey_Trust +
    0.30 × Civic_Participation +
    0.20 × Mutual_Aid_Density

Typical range: [0.2, 0.9]
Boston baseline: 0.58 (estimated via calibration)
```

**2d. Healthcare System Integration Index**
```
Construction:
  EHR_Interoperability (0-1): proportion hospitals sharing records
  Care_Coordination_Programs (0-1): density of programs per 100k
  Referral_Completion_Rate (0-1): proportion successful warm handoffs
  
  Integration_Index =
    0.40 × EHR_Interoperability +
    0.35 × Care_Coordination_Density +
    0.25 × Referral_Completion_Rate

Typical range: [0.3, 0.9]
Boston baseline: 0.70
```

### Type 3: Crisis Endpoint Stocks (Outcome Measures)

**Definition**: Health outcomes with clear unit costs used for ROI calculation.

**Characteristics**:
- Observable from administrative data
- Have established unit costs (from health economics literature)
- Used as monetization targets
- Serve as equilibrium anchors (fixed at observed values in baseline)

**List of Crisis Endpoints**:

```
1. ED_Visits_Annual
   Unit: visits per year
   Unit cost: $1,200 per visit
   Data source: Hospital administrative records
   Boston baseline: 122,400 visits/year

2. Hospitalizations_Annual
   Unit: admissions per year
   Unit cost: $8,500 per admission
   Data source: Hospital administrative records
   Boston baseline: 18,500 admissions/year

3. Preventable_ED_Visits_Annual
   Unit: visits that could have been handled in primary care
   Unit cost: $1,200 (same as ED visit)
   Data source: Classification algorithms on ED data
   Typical: 30-40% of total ED visits

4. ICU_Days_Annual
   Unit: patient-days in intensive care
   Unit cost: $4,500 per day
   Data source: Hospital administrative records

5. Overdose_Events_Annual
   Unit: non-fatal overdoses requiring medical attention
   Unit cost: $25,000 (ED + hospitalization + complications)
   Data source: Syndromic surveillance, EMS records

6. Overdose_Deaths_Annual
   Unit: fatal overdoses
   Unit cost: Included in mortality valuation
   Data source: Medical examiner, death certificates

7. Suicide_Attempts_Annual
   Unit: attempts requiring hospitalization
   Unit cost: $18,000 (ED + psychiatric hospitalization)
   Data source: Hospital records, psych unit admissions

8. Deaths_Premature_Annual
   Unit: deaths before age 75
   Unit cost: $500,000 - $10M (value of statistical life, age-adjusted)
   Data source: Death certificates, vital statistics

9. Homelessness_Episodes_Annual
   Unit: person-years of homelessness
   Unit cost: $50,000 (shelter + ED + carceral contact)
   Data source: Homeless counts, shelter data, HMIS

10. Arrests_Annual
    Unit: criminal arrests
    Unit cost: $5,000 (booking + processing + short-term costs)
    Data source: Police records, court data

11. Incarcerations_Annual
    Unit: person-years of incarceration
    Unit cost: $45,000 (cost of incarceration per year)
    Data source: Corrections data

12. Adverse_Birth_Outcomes_Annual
    Unit: births requiring NICU
    Unit cost: $100,000 (NICU costs + complications)
    Data source: Birth records, hospital data
```

---

## Stock Units and Measurement

### Unit Standardization

**For comparability across geographies**, some stocks normalized per population:

```
Absolute units → Per capita units

ED_Visits_Annual: 122,400 visits
Population: 680,000
ED_Visits_Per_1000: 180 per 1000 population

Why per capita:
- Enables comparison: Boston (180/1000) vs. Mississippi (210/1000)
- Accounts for population size
- Standard in public health
```

**Standard denominators**:
- Per 1,000 population (prevalence, rates)
- Per 10,000 population (rare events)
- Per 100,000 population (very rare events, national comparisons)

### Measurement Hierarchy

**When multiple measurement methods exist, prioritize**:

```
Priority 1: Direct observation from administrative data
  Example: ED visits from hospital records

Priority 2: Survey data (representative samples)
  Example: Food insecurity from NHANES, BRFSS

Priority 3: Proxy indicators (validated indices)
  Example: Walkability score from built environment data

Priority 4: Model-based estimates (statistical imputation)
  Example: Small-area poverty estimates

Priority 5: Calibrated values (inverse calculation)
  Example: Healthcare continuity estimated to match observed ED visits
```

### Handling Missing Data

**When stock cannot be measured directly**:

**Option A: Use regional average**
```
If Boston missing "Community Trust Index":
  Use: Average of similar cities (NYC, Philadelphia, Chicago)
  Document: "Estimate based on peer cities; high uncertainty"
  Flag: Low confidence
```

**Option B: Calibrate from outcomes**
```
If missing "Healthcare Continuity":
  1. Observe: ED visits = 122,400/year
  2. Model: ED_Visits = f(Healthcare_Continuity, other_factors)
  3. Solve: What Healthcare_Continuity level produces observed ED visits?
  4. Estimate: Healthcare_Continuity ≈ 0.45
  5. Validate: Does this match other indicators (insurance data, etc.)?
```

**Option C: Use national benchmark with uncertainty**
```
National average Healthcare_Continuity: 0.50
Boston estimate: 0.50 ± 0.15 (wide CI reflects uncertainty)
Sensitivity: Test scenarios with values 0.35, 0.50, 0.65
```

---

## Functional Forms for Stock Transitions

### General Stock Transition Equation

```
Stock_j(t+1) = Stock_j(t) + ΔStock_j(t)

Where:
  ΔStock_j(t) = Σ Flow_ij(t) - Σ Flow_jk(t)
  
  Flow_ij = mechanism from stock i to stock j
  Flow_jk = mechanism from stock j to stock k
  
  Equilibrium when: ΔStock_j = 0 for all intermediate stocks j
```

### Five Standard Functional Forms

**Form 1: Sigmoid (S-Curve Growth with Saturation)**

```
Mathematical expression:
  ΔStock_j = α × (L / (1 + e^(-k(Stock_i - x₀))))

Where:
  α = effect size (literature-derived)
  L = maximum capacity/saturation level
  k = steepness of curve
  x₀ = midpoint (50% of saturation)
  Stock_i = upstream stock level

Characteristics:
  - Slow growth initially (below threshold)
  - Rapid growth in middle range
  - Saturation at high levels (diminishing returns)
  - Bounded: ΔStock ∈ [0, L×α]

Use cases:
  - Capacity building (CHW programs scale with diminishing returns)
  - Behavioral adoption (innovation diffusion)
  - Trust/social capital (takes time to build, saturates)
  - Infrastructure (physical limits on capacity)

Example:
  CHW_Capacity → Healthcare_Continuity
  
  α = 0.35 (base effect)
  L = 1.0 (max continuity = perfect)
  k = 0.15 (moderate steepness)
  x₀ = 150 FTE (midpoint at 150 CHWs)
  
  At CHW = 50: Continuity increases slowly
  At CHW = 150: Rapid increase (steepest part)
  At CHW = 300: Approaching saturation (little additional benefit)
```

**Form 2: Logarithmic (Diminishing Returns)**

```
Mathematical expression:
  ΔStock_j = α × log(1 + Stock_i)

Characteristics:
  - Large initial effect (first units matter most)
  - Continuously diminishing returns
  - Never saturates (always some benefit)
  - Bounded below: ΔStock ≥ 0

Use cases:
  - Resource allocation with scarcity
  - Housing units (first units have largest impact on homelessness)
  - Income gains (diminishing marginal utility)
  - Service coverage (expanding from 0% to 20% matters more than 80% to 100%)

Example:
  Affordable_Housing_Units → Housing_Stability
  
  α = 0.22
  
  At 0 units: ΔStability = 0
  At 100 units: ΔStability = 0.22 × log(101) ≈ 1.01
  At 1000 units: ΔStability = 0.22 × log(1001) ≈ 1.52
  At 10000 units: ΔStability = 0.22 × log(10001) ≈ 2.03
  
  (Notice: 10× increase in units only doubles effect)
```

**Form 3: Saturating Linear (Piecewise with Hard Cap)**

```
Mathematical expression:
  ΔStock_j = min(α × Stock_i, Max_Capacity_j - Stock_j)

Characteristics:
  - Linear growth until capacity reached
  - Hard stop at maximum
  - Simple to understand and implement

Use cases:
  - Physical infrastructure (can't exceed space)
  - Green space (limited by land area)
  - Beds/capacity (fixed by building size)
  - Any resource with absolute physical limit

Example:
  Green_Space_Investment → Green_Space_Acres
  
  α = 2.5 (acres per $1M investment)
  Max_Capacity = 500 acres (total available land)
  Current_Green_Space = 300 acres
  
  Investment of $50M:
    Without cap: 2.5 × 50 = 125 acres added
    With cap: min(125, 500-300) = 125 acres (fits within capacity)
  
  Investment of $100M:
    Without cap: 2.5 × 100 = 250 acres
    With cap: min(250, 500-300) = 200 acres (hits capacity limit)
```

**Form 4: Threshold-Activated (Piecewise with Minimum)**

```
Mathematical expression:
  ΔStock_j = α × max(0, Stock_i - threshold)

Characteristics:
  - No effect below threshold
  - Linear effect above threshold
  - Models tipping points, critical mass

Use cases:
  - Policy effects (law must be strong enough to matter)
  - Organizational capacity (need minimum staffing)
  - Social movements (critical mass for effectiveness)
  - Medical treatments (minimum dosage)

Example:
  Policy_Strength → Enforcement_Effectiveness
  
  α = 0.40
  threshold = 0.50 (policy must be at least moderate strength)
  
  Policy_Strength = 0.30: ΔEnforcement = 0 (policy too weak)
  Policy_Strength = 0.60: ΔEnforcement = 0.40 × (0.60 - 0.50) = 0.04
  Policy_Strength = 0.80: ΔEnforcement = 0.40 × (0.80 - 0.50) = 0.12
```

**Form 5: Multiplicative Dampening (Relative Effect)**

```
Mathematical expression:
  ΔStock_j = α × Stock_i × (1 - Stock_j / Max_Stock_j)

Characteristics:
  - Effect depends on current level of j (dampening)
  - Percentage-based changes
  - Natural saturation as Stock_j approaches maximum

Use cases:
  - Percentage improvements (10% reduction in X)
  - Market share gains (harder to gain when already high)
  - Health behavior change (easier to improve when currently poor)
  - Relative risk reductions

Example:
  Economic_Assistance → Income_Stability
  
  α = 0.25 (25% improvement potential)
  Max_Income_Stability = 1.0
  
  Current_Stability = 0.30:
    ΔStability = 0.25 × Assistance × (1 - 0.30/1.0) = 0.175 × Assistance
    (Large potential for improvement)
  
  Current_Stability = 0.80:
    ΔStability = 0.25 × Assistance × (1 - 0.80/1.0) = 0.05 × Assistance
    (Small potential for improvement, already high)
```

---

## 30+ Concrete Node Examples

> **Note**: All examples use canonical node IDs from `mechanism-bank/mechanisms/canonical_nodes.json`. See `Nodes/COMPLETE_NODE_INVENTORY.md` for complete specifications.

### Category A: Structural Capacity Nodes (Real Stocks)

**A1. Primary Care Physician Density** (Scale 2 - Institutional)
```
node_id: primary_care_physician_density
stock_name: "Primary Care Physician Density"
stock_unit: "Physicians per 100,000 population"
stock_type: "real"
measurement: "direct"
typical_range: [20, 200]
data_source: "State medical boards, HRSA data"
boston_baseline: 165 per 100k
functional_form_typical: "sigmoid" (access improvements saturate)
```

**A2. Emergency Department Availability** (Scale 2 - Institutional)
```
node_id: emergency_department_availability
stock_name: "Emergency Department Availability"
stock_unit: "ED capacity per 100,000 population"
stock_type: "real"
measurement: "direct"
typical_range: [0, 50]
data_source: "Hospital administrative records, AHA data"
boston_baseline: 28 per 100k
functional_form_typical: "saturating_linear" (limited by hospital capacity)
```

**A3. Public Housing Funding Per Capita** (Scale 1 - Structural)
```
node_id: public_housing_funding_per_capita
stock_name: "Public Housing Funding Per Capita"
stock_unit: "Dollars per capita annual allocation"
stock_type: "real"
measurement: "direct"
typical_range: [0, 500]
data_source: "HUD databases, local housing authority records"
boston_baseline: 185 per capita
functional_form_typical: "logarithmic" (diminishing returns)
```

**A4. Housing Choice Voucher Coverage Rate** (Scale 4 - Intermediate)
```
node_id: housing_choice_voucher_coverage_rate
stock_name: "Housing Choice Voucher Coverage Rate"
stock_unit: "Proportion of eligible households receiving vouchers"
stock_type: "real"
measurement: "direct"
typical_range: [0.05, 0.40]
data_source: "HUD, local housing authority records"
boston_baseline: 0.22
functional_form_typical: "saturating_linear" (limited by funding)
```

**A5. Eviction Legal Aid Availability** (Scale 2 - Institutional)
```
node_id: eviction_legal_aid_availability
stock_name: "Eviction Legal Aid Availability"
stock_unit: "Legal aid attorneys per 10,000 eviction filings"
stock_type: "real"
measurement: "direct"
typical_range: [0.5, 10]
data_source: "Legal aid organizations, court records"
boston_baseline: 3.2 per 10k filings
functional_form_typical: "threshold" (minimum capacity needed for effect)
```

### Category B: Intermediate Proxy Index Nodes

**B1. Housing Quality Index** (Scale 3 - Individual/Household)
```
node_id: housing_quality_index_revised_consolidated
stock_name: "Housing Quality Index"
stock_unit: "Index (0-1)"
stock_type: "proxy"
measurement: "constructed"
components:
  - structural_adequacy (weight: 0.35)
  - environmental_hazards_absence (weight: 0.30)
  - maintenance_quality (weight: 0.20)
  - overcrowding_absence (weight: 0.15)
typical_range: [0.2, 0.9]
boston_baseline: 0.62
functional_form_typical: "logarithmic" (from housing investment)
```

**B2. Housing Cost Burden** (Scale 3 - Individual/Household)
```
node_id: housing_cost_burden
stock_name: "Housing Cost Burden"
stock_unit: "Proportion paying >30% income on housing"
stock_type: "real"
measurement: "direct"
typical_range: [0.15, 0.60]
boston_baseline: 0.42
functional_form_typical: "threshold" (policy effects above certain strength)
```

**B3. Food Insecurity Rate** (Scale 3 - Individual/Household)
```
node_id: food_insecurity_rate
stock_name: "Food Insecurity Rate"
stock_unit: "Proportion experiencing food insecurity"
stock_type: "real"
measurement: "survey"
typical_range: [0.05, 0.30]
boston_baseline: 0.12
functional_form_typical: "multiplicative_dampening" (from assistance programs)
```

**B4. Just-Cause Eviction Protection** (Scale 4 - Policy)
```
node_id: just_cause_eviction_protection
stock_name: "Just-Cause Eviction Protection"
stock_unit: "Binary (0=no protection, 1=protection in effect)"
stock_type: "policy"
measurement: "direct"
typical_range: [0, 1]
boston_baseline: 1 (MA has just-cause protections)
functional_form_typical: "threshold" (binary policy effect)
```

**B5. Mental Healthcare Access** (Scale 3 - Individual/Household)
```
node_id: mental_healthcare_access
stock_name: "Mental Healthcare Access"
stock_unit: "Index (0-1)"
stock_type: "proxy"
measurement: "constructed"
components:
  - mental_health_provider_density (weight: 0.40)
  - insurance_mental_health_coverage (weight: 0.35)
  - geographic_accessibility (weight: 0.25)
typical_range: [0.2, 0.85]
boston_baseline: 0.65
functional_form_typical: "sigmoid" (from provider capacity)
```

### Category C: Crisis Endpoint Nodes (Outcomes)

**C1. Emergency Department Visit Rate** (Scale 5 - Crisis Endpoint)
```
node_id: emergency_department_visit_rate
stock_name: "Emergency Department Visit Rate"
stock_unit: "Visits per 1,000 population annually"
stock_type: "crisis_endpoint"
measurement: "direct"
typical_range: [100, 500]
unit_cost: "$1,200 per visit"
data_source: "Hospital administrative data, HCUP"
boston_baseline: 180 per 1,000
functional_form_incoming: "multiplicative_dampening" (from access improvements)
```

**C2. Preventable Hospitalization** (Scale 5 - Crisis Endpoint)
```
node_id: preventable_hospitalization_individual
stock_name: "Preventable Hospitalization (Individual)"
stock_unit: "ACSC admissions per 1,000 population"
stock_type: "crisis_endpoint"
measurement: "direct"
typical_range: [5, 50]
unit_cost: "$8,500 per admission"
data_source: "Hospital discharge data, AHRQ PQI"
boston_baseline: 12 per 1,000
functional_form_incoming: "multiplicative_dampening"
```

**C3. Asthma Hospitalization Rate** (Scale 5 - Crisis Endpoint)
```
node_id: asthma_hospitalization_rate
stock_name: "Asthma Hospitalization Rate"
stock_unit: "Hospitalizations per 100,000 population"
stock_type: "crisis_endpoint"
measurement: "direct"
typical_range: [20, 200]
unit_cost: "$6,500 per hospitalization"
data_source: "Hospital discharge data"
boston_baseline: 85 per 100k
functional_form_incoming: "threshold" (from housing quality, air quality)
```

**C4. All-Cause Mortality Rate** (Scale 5 - Crisis Endpoint)
```
node_id: all_cause_mortality_rate
stock_name: "All-Cause Mortality Rate"
stock_unit: "Deaths per 100,000 population"
stock_type: "crisis_endpoint"
measurement: "direct"
typical_range: [500, 1200]
unit_cost: "$500k-$10M (age-dependent VSL)"
data_source: "Vital statistics, death certificates"
boston_baseline: 720 per 100k
functional_form_incoming: "linear" (from multiple upstream sources)
```

**C5. Eviction Judgment Rate** (Scale 5 - Crisis Endpoint)
```
node_id: eviction_judgment_rate
stock_name: "Eviction Judgment Rate"
stock_unit: "Eviction judgments per 1,000 renter households"
stock_type: "crisis_endpoint"
measurement: "direct"
typical_range: [5, 100]
unit_cost: "$15,000 per eviction (including downstream costs)"
data_source: "Court records, Eviction Lab"
boston_baseline: 12 per 1,000 renters
functional_form_incoming: "threshold" (from policy protection + economic factors)
```

### Category D: Environmental/Spatial Nodes

**D1. Eviction Filing Rate** (Scale 3 - Individual/Household)
```
node_id: eviction_filing_rate
stock_name: "Eviction Filing Rate"
stock_unit: "Filings per 100 renter households annually"
stock_type: "real"
measurement: "direct"
typical_range: [1, 20]
data_source: "Court records, Eviction Lab"
boston_baseline: 3.8 per 100 renters
functional_form_typical: "threshold" (from policy + economic factors)
```

**D2. Eviction Rate** (Scale 3 - Individual/Household)
```
node_id: eviction_rate
stock_name: "Eviction Rate"
stock_unit: "Completed evictions per 100 renter households"
stock_type: "real"
measurement: "direct"
typical_range: [0.5, 10]
data_source: "Court records, Eviction Lab"
boston_baseline: 1.2 per 100 renters
functional_form_typical: "threshold" (from filing rate + legal aid)
```

**D3. Incarceration Rate** (Scale 7 - System-level)
```
node_id: incarceration_rate
stock_name: "Incarceration Rate"
stock_unit: "Incarcerated persons per 100,000 population"
stock_type: "real"
measurement: "direct"
typical_range: [100, 1000]
data_source: "Bureau of Justice Statistics, state DOC"
boston_baseline: 320 per 100k
functional_form_typical: "threshold" (from policy + enforcement)
```

### Category E: Behavioral/Utilization Nodes

**E1. Primary Care Visit Rate** (Scale 4 - Intermediate)
```
node_id: primary_care_visit_rate
stock_name: "Primary Care Visit Rate"
stock_unit: "Annual visits per 1,000 population"
stock_type: "real"
measurement: "direct"
typical_range: [500, 4000]
data_source: "Claims data, EHR, MEPS"
boston_baseline: 2,800 per 1,000
functional_form_typical: "sigmoid" (from provider density + insurance)
```

**E2. Uninsured Rate** (Scale 3 - Individual/Household)
```
node_id: uninsured_rate
stock_name: "Uninsured Rate"
stock_unit: "Proportion of population without health insurance"
stock_type: "real"
measurement: "direct"
typical_range: [0.02, 0.25]
data_source: "Census ACS, state insurance data"
boston_baseline: 0.03 (MA has near-universal coverage)
functional_form_typical: "threshold" (from Medicaid expansion)
```

### Category F: Social Determinant Nodes

**F1. Asthma Prevalence (Adults)** (Scale 5 - Crisis Endpoint)
```
node_id: asthma_prevalence_adults_revised_terminology_standardized
stock_name: "Asthma Prevalence (Adults)"
stock_unit: "Proportion of adults with asthma diagnosis"
stock_type: "real"
measurement: "survey + claims"
typical_range: [0.05, 0.15]
data_source: "BRFSS, CDC"
boston_baseline: 0.10
functional_form_typical: "threshold" (from housing quality, air quality)
```

**F2. Diabetes Prevalence** (Scale 5 - Crisis Endpoint)
```
node_id: diabetes_prevalence
stock_name: "Diabetes Prevalence"
stock_unit: "Proportion of adults with diabetes"
stock_type: "real"
measurement: "survey + claims"
typical_range: [0.05, 0.20]
data_source: "BRFSS, CDC"
boston_baseline: 0.09
functional_form_typical: "multiplicative_dampening" (from food access + care)
```

**F3. Minimum Wage Level** (Scale 1 - Structural Policy)
```
node_id: minimum_wage_level
stock_name: "Minimum Wage Level"
stock_unit: "Dollars per hour"
stock_type: "policy"
measurement: "direct"
typical_range: [7.25, 20.00]
data_source: "State labor departments"
boston_baseline: 15.00 (MA minimum wage)
functional_form_typical: "threshold" (effect above federal floor)
```

**F4. Rent Control Policy Strength** (Scale 1 - Structural Policy)
```
node_id: rent_control_stabilization_policy_strength
stock_name: "Rent Control / Stabilization Policy Strength"
stock_unit: "Index (0-10)"
stock_type: "policy"
measurement: "constructed"
typical_range: [0, 10]
data_source: "State/local housing policy analysis"
boston_baseline: 0 (MA banned rent control in 1994)
functional_form_typical: "threshold" (minimum strength for effect)
```

### Category G: Policy Environment Nodes

**G1. Medicaid Expansion Status** (Scale 1 - Structural Policy)
```
node_id: medicaid_expansion_status
stock_name: "Medicaid Expansion Status"
stock_unit: "Binary (0=not expanded, 1=expanded)"
stock_type: "policy"
measurement: "direct"
typical_range: [0, 1]
boston_baseline: 1 (MA expanded before ACA)
functional_form_typical: "threshold" (binary policy effect)
```

**G2. Medicaid Coverage Generosity Index** (Scale 4 - Intermediate)
```
node_id: medicaid_coverage_generosity_index
stock_name: "Medicaid Coverage Generosity Index"
stock_unit: "Index (0-100 scale)"
stock_type: "proxy"
measurement: "constructed"
components:
  - income_eligibility_threshold
  - optional_benefits_coverage
  - reimbursement_rates
typical_range: [0, 100]
boston_baseline: 85 (MA has generous Medicaid)
functional_form_typical: "sigmoid" (effect increases with generosity)
```

**G3. Cash Bail Reform Status** (Scale 3 - Policy)
```
node_id: cash_bail_reform_status
stock_name: "Cash Bail Reform Status"
stock_unit: "Index (0-10, higher=more reform)"
stock_type: "policy"
measurement: "constructed"
typical_range: [0, 10]
boston_baseline: 6.5 (MA has bail reform provisions)
functional_form_typical: "threshold" (reform must reach critical level)
```

---

## Implementation Specifications

### Stock Data Structure

> **Note**: All node_id values must reference canonical nodes from `mechanism-bank/mechanisms/canonical_nodes.json`.

```yaml
# Example: Full specification for one canonical node

node_id: primary_care_physician_density  # Must exist in canonical_nodes.json
node_class: institutional
stock_name: "Primary Care Physician Density"
description: "Primary care physicians per 100,000 population in service area"

# Stock specification
stock_unit: "Physicians per 100,000 population"
stock_type: "real"
measurement_method: "direct"
data_sources:
  - "State medical boards"
  - "HRSA Area Health Resources File"
  - "AMA Physician Masterfile"

# Value ranges
typical_range:
  minimum: 20
  maximum: 200
  boston_baseline: 165

validation:
  plausibility_check: "value between 10 and 300"
  consistency_check: "Must be consistent with population and physician counts"

# Functional form for mechanisms FROM this node
outgoing_mechanisms:
  default_form: "sigmoid"
  parameters:
    - alpha: "effect size (mechanism-specific)"
    - L: "saturation level (mechanism-specific)"
    - k: "steepness (typically 0.10-0.20)"
    - x0: "midpoint (typically 1.5× baseline)"

# Metadata
added_date: "2024-05-15"
last_updated: "2025-12-02"
version: "2.0"
documentation: "See: Nodes/COMPLETE_NODE_INVENTORY.md for full specification"
```

### Equilibrium Calculation Requirements

**For solving baseline equilibrium**:

1. **Fixed stocks** (known values):
   - All crisis endpoint stocks (from observed data)
   - All structural capacity stocks (from administrative data)
   
2. **Free stocks** (to be calculated):
   - All intermediate proxy stocks
   - Some behavioral/utilization stocks without direct measurement
   
3. **Constraints**:
   - Each free stock must satisfy: Σ(inflows) - Σ(outflows) = 0
   - All stock values must be within plausible ranges
   - System must reproduce observed crisis endpoint values (validation)

4. **Solution method**:
   - Linearize around initial guess
   - Solve matrix equation
   - Refine with nonlinear iteration
   - Validate convergence

### Functional Form Selection Guide

```
Decision tree for selecting functional form:

Is this a capacity-building intervention (CHW, housing, infrastructure)?
  YES → Use sigmoid (saturation effects)
  
Is this a resource allocation with clear diminishing returns?
  YES → Use logarithmic
  
Is there a physical hard limit (land, space, beds)?
  YES → Use saturating_linear
  
Is there a threshold below which nothing happens (policy, dosage)?
  YES → Use threshold
  
Is the effect proportional to current level (% improvement)?
  YES → Use multiplicative_dampening
  
DEFAULT → Use linear (simplest, most interpretable)
```

---

---

## Canonical Node Reference

All node examples in this document reference the canonical node inventory. This ensures consistency across the platform.

### Node Sources

| Source | Location | Use Case |
|--------|----------|----------|
| **Canonical Nodes JSON** | `mechanism-bank/mechanisms/canonical_nodes.json` | Quick lookup of 840 node IDs |
| **Complete Inventory** | `Nodes/COMPLETE_NODE_INVENTORY.md` | Full specifications with scales, domains, units |

### Scale Summary

| Scale | Count | Examples in This Document |
|-------|-------|---------------------------|
| 1 - Structural Policy | ~120 | `medicaid_expansion_status`, `minimum_wage_level`, `rent_control_stabilization_policy_strength` |
| 2 - Institutional | ~250 | `primary_care_physician_density`, `emergency_department_availability`, `eviction_legal_aid_availability` |
| 3 - Individual/Household | ~280 | `eviction_filing_rate`, `housing_cost_burden`, `uninsured_rate` |
| 4 - Intermediate | ~100 | `primary_care_visit_rate`, `just_cause_eviction_protection` |
| 5 - Crisis Endpoints | ~100 | `emergency_department_visit_rate`, `asthma_hospitalization_rate`, `all_cause_mortality_rate` |

---

## Document Metadata

**Version History**:
- v1.0 (2024-06): Initial stock-flow specifications
- v2.0 (2025-11): Expanded to 30+ concrete examples, clarified functional forms, added implementation specs
- v2.1 (2025-12): Updated all node examples to use canonical node IDs

**Related Documents**:
- [05_MECHANISM_BANK_STRUCTURE.md] - How mechanisms connect stocks
- [06_EQUILIBRIUM_CALCULATION_ENGINE.md] - How to solve for stock values
- [13_INITIAL_STATE_CALIBRATION.md] - Setting baseline stock levels
- [Canonical Nodes] `mechanism-bank/mechanisms/canonical_nodes.json`
- [Node Specifications] `Nodes/COMPLETE_NODE_INVENTORY.md`

**Last Reviewed**: December 2, 2025
**Next Review**: March 2, 2026 (quarterly for technical specs)

---

**END OF DOCUMENT**
