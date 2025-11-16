# 07: Time Simulation Framework
**Post-Intervention Dynamics and Convergence Analysis**

---

## 1. Overview

Post-intervention analysis uses **dual temporal logic**: the system either reaches a **new steady-state equilibrium** or runs until a **specified time horizon**—whichever occurs first. This framework details how stock levels evolve annually from intervention implementation through outcome materialization.

**Core Principle**: Interventions create capacity changes that propagate through mechanism networks over time. The system tracks how stock levels adjust annually, incorporating intervention ramp-up, mechanism latency, and feedback loop stabilization until convergence or horizon termination.

---

## 2. Temporal Logic Architecture

### 2.1 Dual Stopping Criteria

```
Post-Intervention Simulation:
├─ Initialize: Apply intervention at t=0 (baseline → new capacity)
├─ Iterate: Calculate stock changes annually (t=1, t=2, t=3, ...)
├─ Monitor: Check convergence at each time step
└─ Terminate when EITHER:
   ├─ Steady State Reached: max(ΔStock_i) < convergence_threshold
   └─ Time Horizon Expired: t ≥ user_specified_horizon (typically 3-10 years)
```

**Implementation Logic**:
- **Convergence threshold**: max(|S_i(t) - S_i(t-1)|) < 0.01 across all active nodes
- **Minimum duration**: Require t ≥ 3 years before declaring convergence (prevents premature termination during transient dynamics)
- **Maximum duration**: Cap at t = 20 years to prevent infinite loops with oscillating systems

**Output States**:
1. **Converged**: System reached equilibrium at year t_converge
2. **Horizon-terminated**: System still changing at t_horizon (report trajectory with uncertainty flag)
3. **Non-converging**: System oscillates or grows unbounded after 20 years (flag for expert review)

---

### 2.2 Annual Time Step Rationale

**Why Annual Steps?**
- Matches literature reporting (most studies report annual outcomes)
- Aligns with policy/budget cycles (fiscal years, program evaluation periods)
- Balances computational tractability with temporal resolution
- Captures latency periods spanning 6-24 months adequately

**Alternative Considerations**:
- **Quarterly steps**: Useful for short-term interventions (policy changes, emergency responses), but 4× computational cost
- **Monthly steps**: Excessive resolution for structural mechanisms (housing stability takes 6+ months to materialize)
- **Multi-year steps**: Too coarse—misses critical latency dynamics

**MVP Specification**: Annual time steps. Phase 2 may support quarterly resolution for specific intervention types.

---

## 3. Intervention Ramp-Up Functions

Interventions do not materialize instantaneously. The system models **gradual implementation** through standardized ramp-up functions that convert target capacity changes into year-by-year capacity trajectories.

### 3.1 Ramp-Up Function Types

**Type 1: Linear Ramp-Up**
```
Capacity(t) = Capacity_baseline + (t / t_full) × (Capacity_target - Capacity_baseline)

where t_full = years to full implementation

Example: CHW Expansion (50 → 200 workers over 3 years)
├─ Year 0: 50 workers (baseline)
├─ Year 1: 100 workers (50 + 1/3 × 150 = 100)
├─ Year 2: 150 workers (50 + 2/3 × 150 = 150)
└─ Year 3+: 200 workers (full implementation)
```

**When to Use**: Infrastructure interventions (facilities, workforce), phased policy rollouts

---

**Type 2: Exponential Ramp-Up**
```
Capacity(t) = Capacity_baseline + (Capacity_target - Capacity_baseline) × (1 - e^(-λt))

where λ = growth rate parameter (typically λ = 0.5 to 1.5)

Example: Community Organizing (λ = 0.6)
├─ Year 1: 45% of capacity gain (slow initial growth)
├─ Year 2: 70% of capacity gain
├─ Year 3: 86% of capacity gain
└─ Year 5: 95% of capacity gain (asymptotic approach)
```

**When to Use**: Relationship-building interventions (community trust, coalition formation), market penetration (service uptake)

---

**Type 3: Step Function**
```
Capacity(t) = {
  Capacity_baseline           if t < t_implementation
  Capacity_target             if t ≥ t_implementation
}

Example: Policy Change (Just-Cause Eviction Law)
├─ Year 0: No protection (strength = 0)
└─ Year 1+: Full protection (strength = 9, immediately upon passage)
```

**When to Use**: Regulatory changes (instant legal effect), binary policy shifts (Medicaid expansion)

---

**Type 4: Sigmoid Ramp-Up**
```
Capacity(t) = Capacity_baseline + (Capacity_target - Capacity_baseline) / (1 + e^(-k(t - t_midpoint)))

where k = steepness, t_midpoint = inflection point

Example: Service Uptake with Awareness Lag
├─ Years 0-1: Slow adoption (10-20% of target)
├─ Year 2: Rapid uptake (50% at inflection)
├─ Years 3-4: Saturation (80-95%)
└─ Year 5+: Asymptotic maximum
```

**When to Use**: Behavioral interventions (requiring awareness + trust), technology adoption curves

---

### 3.2 Ramp-Up Specification in Mechanism Bank

Each intervention type in the mechanism bank specifies its default ramp-up function:

```json
{
  "intervention_type": "community_health_worker_expansion",
  "ramp_up_function": "linear",
  "default_duration": 3,
  "parameters": {
    "t_full": 3
  },
  "user_overridable": true
}
```

**User Customization**: Users can override default ramp-up if they have implementation data:
- "Our CHW program scales exponentially due to partnership with existing clinics" → Switch to exponential
- "Policy effective Jan 1, 2026" → Use step function with t_implementation = 0

---

## 4. Mechanism Latency Integration

**Latency** quantifies the delay between intervention implementation and outcome materialization. Each mechanism encodes latency as a **fractional effect multiplier** that grows over time.

### 4.1 Latency Encoding

```json
{
  "mechanism_id": "chw_to_healthcare_continuity",
  "from_node": "Community_Health_Workers",
  "to_node": "Healthcare_Continuity",
  "latency_profile": {
    "year_1": 0.60,
    "year_2": 0.90,
    "year_3": 1.00
  },
  "latency_rationale": "CHW relationship-building requires 6-12 months; full effect by year 3"
}
```

### 4.2 Latency Application in Simulation

At each time step, stock changes are scaled by latency multipliers:

```
For mechanism m: S_i → S_j
├─ Calculate raw flow: f_ij(t) = α × g(S_i(t), parameters)
├─ Apply latency: f_ij_adjusted(t) = latency(t) × f_ij(t)
└─ Update target stock: S_j(t+1) = S_j(t) + f_ij_adjusted(t) + [other flows into S_j]
```

**Example**:
```
CHW capacity increases from 50 → 200 at t=0
├─ Year 1:
│   ├─ Capacity change: 150 workers added
│   ├─ Raw effect on Healthcare Continuity: ΔS = +0.10
│   ├─ Latency-adjusted: 0.60 × 0.10 = +0.06 (60% of effect materializes)
│   └─ Healthcare Continuity stock: 0.45 → 0.51
├─ Year 2:
│   ├─ Latency-adjusted: 0.90 × 0.10 = +0.09 (90% of effect)
│   └─ Healthcare Continuity stock: 0.51 → 0.54
└─ Year 3+:
    ├─ Latency-adjusted: 1.00 × 0.10 = +0.10 (100% of effect)
    └─ Healthcare Continuity stock: 0.54 → 0.55 (steady state reached)
```

### 4.3 Default Latency Profiles by Mechanism Type

| Mechanism Type | Year 1 | Year 2 | Year 3+ | Rationale |
|----------------|--------|--------|---------|-----------|
| **Infrastructure** (facilities, workforce) | 0.60 | 0.90 | 1.00 | Hiring lag, operational ramp-up |
| **Policy (regulatory)** | 0.70 | 1.00 | 1.00 | Awareness lag, behavioral adjustment |
| **Behavioral** (trust-building) | 0.40 | 0.70 | 1.00 | Relationship formation, habit change |
| **Organizing** (coalition, advocacy) | 0.10 | 0.40 | 0.70 | Multi-year trust-building → policy change |
| **Market** (housing, employment) | 0.50 | 0.80 | 1.00 | Supply response, market adjustment |

**Calibration**: Latency profiles are derived from longitudinal studies and expert judgment. Users can adjust based on local implementation quality.

---

## 5. Stock Evolution Equations

At each annual time step, stock levels evolve according to:

```
S_i(t+1) = S_i(t) + Σ_j [f_ji(t) × latency_ji(t)] - Σ_k [f_ik(t) × latency_ik(t)]

where:
├─ S_i(t) = stock level at time t
├─ f_ji(t) = inflow from node j to node i
├─ f_ik(t) = outflow from node i to node k
└─ latency(t) = time-dependent fractional multiplier
```

**Functional Forms for Flows** (see Section 4.4 in GUIDING_PRINCIPLES_FROM_QA.md):
```
f_ij(t) = α × functional_form(S_i(t), parameters)

Functional forms:
1. Sigmoid: α × (1 / (1 + e^(-k(S_i - threshold))))
2. Logarithmic: α × log(1 + S_i)
3. Saturating Linear: min(α × S_i, max_capacity - S_j)
4. Threshold-Activated: α × max(0, S_i - threshold)
5. Multiplicative Dampening: α × S_i × (1 - S_j / S_j_max)
```

**Bounded Updates**: All stock updates are constrained:
```
S_i(t+1) = max(S_i_min, min(S_i_max, S_i(t) + net_flow))

where:
├─ S_i_min = theoretical minimum (often 0)
└─ S_i_max = capacity ceiling (from literature or observed data)
```

---

## 6. Convergence Detection

### 6.1 Convergence Criteria

**Primary Criterion**: Maximum absolute stock change below threshold
```
Convergence declared if:
  max_i(|S_i(t) - S_i(t-1)|) < ε  for all active nodes

where ε = 0.01 (1% of stock value for indexed stocks; absolute for counted stocks)
```

**Secondary Criterion**: Stable outcome projection
```
Additional check: max_k(|Outcome_k(t) - Outcome_k(t-1)|) < 0.5% of baseline

where Outcome_k = crisis endpoint (ED visits, hospitalizations, etc.)
```

**Minimum Duration**: Convergence cannot be declared before t = 3 years (prevents premature termination during transient dynamics)

### 6.2 Non-Convergence Handling

**Oscillating Systems**: If stocks oscillate (e.g., S_i alternates between 0.50 and 0.55) without stabilizing:
```
Detection: If S_i(t) - S_i(t-2) < ε but S_i(t) - S_i(t-1) > ε for 3+ consecutive cycles
Action: 
  ├─ Report: "System exhibits oscillatory behavior"
  ├─ Output: Time-averaged values over final 5 years
  └─ Flag: Uncertainty warning for user review
```

**Unbounded Growth**: If stocks grow without saturation:
```
Detection: If any S_i(t) > 1.5 × S_i_max for indexed stocks, or S_i(t) exceeds expected population for counted stocks
Action:
  ├─ Halt simulation at t_halt
  ├─ Report: "Mechanism appears to lack saturation constraint"
  └─ Flag: Expert review required for mechanism functional form
```

**Phase 2 Enhancement**: Implement automatic diagnostic to identify which feedback loops are causing non-convergence and suggest saturation function adjustments.

---

## 7. Uncertainty Propagation Over Time

Uncertainty grows as simulation progresses due to:
1. **Cumulative parameter uncertainty**: Effect size confidence intervals compound annually
2. **Latency uncertainty**: Timing of effects varies across populations
3. **Interaction uncertainty**: Multiple mechanisms affecting same stocks may reinforce or cancel unpredictably

### 7.1 Monte Carlo Uncertainty Quantification

**Method**: Run N parallel simulations (N = 1000 for MVP) with parameter values sampled from confidence intervals

```
For each simulation run n ∈ {1, ..., N}:
  1. Sample mechanism parameters from distributions:
     α_ij ~ Normal(μ = α_mean, σ = α_SE)
  2. Sample latency profiles:
     latency_year1 ~ Uniform(latency_mean - 0.10, latency_mean + 0.10)
  3. Run time simulation with sampled parameters
  4. Record outcome trajectories: Outcome_k(t)_n

Aggregate across runs:
├─ Median trajectory: Outcome_k(t)_median = median_n(Outcome_k(t)_n)
├─ 95% CI: [percentile_2.5(Outcome_k(t)_n), percentile_97.5(Outcome_k(t)_n)]
└─ Uncertainty growth: width(CI_t) typically grows √t
```

**Computational Optimization**: Use sparse network representation and mechanism caching to run 1000 simulations in <5 minutes per scenario.

### 7.2 Reporting Uncertainty in Outputs

**Visual Representation**: Dashboard displays:
```
Year   Median ED Visits Prevented   95% CI          % Uncertainty
1      60                           [45, 78]        27%
2      90                           [65, 118]       29%
3      100                          [70, 135]       33%
5      100                          [60, 150]       45%
```

**Interpretation Guidance**: Uncertainty increases over time because:
- Early years benefit from better-studied short-term effects
- Later years compound uncertainty across multiple mechanisms
- Longer horizons involve more external factors (policy changes, economic shocks)

---

## 8. Time Horizon Selection

Users specify projection duration based on accountability needs:

| Time Horizon | Use Case | Uncertainty Level | Typical Stakeholder |
|--------------|----------|-------------------|---------------------|
| **3 years** | Program evaluation, grant cycles | Moderate (±30%) | Foundations, pilot programs |
| **5 years** | Strategic planning, municipal budgets | Moderate-High (±40%) | Health departments, CDCs |
| **10 years** | Policy impact assessment | High (±50-60%) | State agencies, academic researchers |
| **20 years** | Intergenerational effects (rare) | Very High (±70%+) | Long-term population health studies |

**Default**: 5 years (balances actionability with policy-relevant horizon)

**Discount Rate Application**: Future outcomes are discounted at 3% annually (standard public health practice):
```
NPV = Σ_t [Outcome_value(t) / (1.03)^t]

Example:
├─ Year 1: $252,000 / 1.03^1 = $244,660
├─ Year 2: $378,000 / 1.03^2 = $356,287
└─ Year 3: $420,000 / 1.03^3 = $384,430
```

Users can adjust discount rate (0-7%) based on organizational preferences or social discount rate literature.

---

## 9. Intervention Persistence and Decay

**Key Question**: What happens after the intervention ends?

### 9.1 Persistence Profiles

**Type A: Permanent Change** (e.g., policy passed, infrastructure built)
```
Capacity(t) = Capacity_target for all t ≥ t_implementation
```

**Type B: Sustained Effort Required** (e.g., CHW program, ongoing services)
```
If funding continues:
  Capacity(t) = Capacity_target
If funding ceases at t_end:
  Capacity(t) = Capacity_baseline + (Capacity_target - Capacity_baseline) × e^(-decay_rate × (t - t_end))
  
where decay_rate depends on program type (typical: 0.2-0.5 per year)
```

**Type C: Behavioral Lock-In** (e.g., community organizing, trust-building)
```
Capacity(t) decays slowly after program ends:
  Capacity(t) = Capacity_baseline + (Capacity_target - Capacity_baseline) × e^(-0.1 × (t - t_end))
  
Rationale: Relationships persist; slow erosion over 5-10 years
```

### 9.2 User Specification

```
Intervention {
  persistence_type: "sustained_effort" | "permanent" | "behavioral_lock_in"
  funding_duration: 5 years
  decay_parameters: {
    decay_rate: 0.3,
    half_life: 2.3 years
  }
}
```

**Dashboard Output**: Show projected outcomes for both:
1. **With sustained funding** (optimistic scenario)
2. **With funding cessation** (conservative scenario)

---

## 10. Feedback Loop Stabilization

Feedback loops create **dynamic interdependencies** where downstream effects influence upstream stocks. The time simulation framework handles three feedback types:

### 10.1 Balancing Loops (Self-Limiting)

**Example**: Healthcare Access → Reduced ED Visits → Lower Healthcare Costs → More Resources for Healthcare Access

```
Mechanism:
├─ Increased healthcare access reduces ED utilization
├─ Lower ED costs free budget for more access programs
└─ But: Saturation limit (can't reduce ED visits below baseline preventable rate)

Functional Form:
f_access_to_ed(t) = -α × Healthcare_Access(t) × (ED_Visits(t) / ED_Visits_baseline)
  with floor: ED_Visits(t) ≥ 0.7 × ED_Visits_baseline
```

**Stabilization**: Balancing loops converge because resource constraints and saturation functions prevent runaway growth.

---

### 10.2 Reinforcing Loops (Potentially Destabilizing)

**Example**: Community Power → Policy Wins → Trust → More Organizing → Community Power

```
Risk: Positive feedback could create exponential growth without bounds

Stabilization Mechanisms:
1. Sigmoid functional forms (asymptotic approach to maximum)
2. Resource constraints (finite population, organizing capacity)
3. Time-dependent dampening (diminishing returns to scale)

Functional Form:
f_power_to_organizing(t) = α × Community_Power(t) × (1 - Organizing(t) / Organizing_max)
```

**Convergence Check**: System monitors for S_i(t) > S_i_max and applies hard caps:
```
If S_i(t+1) > S_i_max:
  S_i(t+1) = S_i_max
  Log warning: "Stock hit capacity ceiling; consider reviewing mechanism functional form"
```

---

### 10.3 Delayed Feedback (Multi-Year Loops)

**Example**: Housing Stability → Health Improvement → Employment → Income → Housing Stability

```
Latency consideration:
├─ Housing → Health: 1-2 years (chronic disease improvement)
├─ Health → Employment: 6-12 months (job search, retention)
├─ Employment → Income: immediate
└─ Income → Housing: 6-12 months (save deposit, credit repair)

Total loop latency: ~3 years

Implication: Feedback effects don't materialize until Year 3+
  Year 1-2: Forward propagation only (intervention → outcomes)
  Year 3+: Feedback begins to influence upstream stocks
```

**Simulation Handling**: Track loop-level latency separately from mechanism-level latency to prevent premature feedback activation.

---

## 11. Computational Efficiency Strategies

### 11.1 Sparse Network Representation

**Optimization**: Only calculate flows for active mechanisms (non-zero stock changes)

```
At each time step:
  1. Identify nodes with ΔS_i(t-1) > 0.001
  2. Activate only mechanisms connected to those nodes
  3. Skip mechanisms where both source and target unchanged
  
Result: ~60% reduction in computation per time step
```

---

### 11.2 Mechanism Caching

**Pre-compute** functional form outputs for common stock values:

```
For sigmoid mechanisms:
  Cache: {S_i: f(S_i)} for S_i ∈ [0, 1] at 0.01 increments
  Lookup: O(1) retrieval instead of O(n) computation

For linear mechanisms:
  No caching needed (direct calculation faster)
```

**Storage**: ~10 MB cache per geography (negligible memory footprint)

---

### 11.3 Parallel Monte Carlo

Run uncertainty simulations in parallel:
```
Split N = 1000 simulations across 10 parallel threads
Each thread runs 100 simulations independently
Aggregate results at completion

Speedup: ~8-9× (accounting for threading overhead)
```

---

## 12. Output Structure

### 12.1 Time Series Data

```json
{
  "intervention": "CHW_expansion_50_to_200",
  "time_horizon": 5,
  "convergence": {
    "converged": true,
    "convergence_year": 3
  },
  "stock_trajectories": [
    {
      "node": "Community_Health_Workers",
      "unit": "FTE count",
      "values": [50, 100, 150, 200, 200]
    },
    {
      "node": "Healthcare_Continuity",
      "unit": "Index (0-1)",
      "values": [0.45, 0.51, 0.54, 0.55, 0.55],
      "ci_95": [[0.43, 0.47], [0.48, 0.54], [0.50, 0.58], [0.51, 0.60], [0.51, 0.60]]
    }
  ],
  "outcome_trajectories": [
    {
      "endpoint": "ED_visits_prevented",
      "values": [60, 90, 100, 100, 100],
      "ci_95": [[45, 78], [65, 118], [70, 135], [70, 135], [60, 150]],
      "monetized_value": [72000, 108000, 120000, 120000, 120000],
      "npv": 476543
    }
  ]
}
```

### 12.2 Dashboard Visualizations

**Plot 1**: Stock trajectories over time (line graph with confidence bands)
**Plot 2**: Outcome trajectories over time (bar chart with uncertainty)
**Plot 3**: Convergence diagnostic (stock change magnitudes declining to threshold)
**Plot 4**: Sensitivity analysis (tornado plot showing parameter influence on outcomes)

---

## 13. Integration with Other System Components

**Input from**: 
- `06_EQUILIBRIUM_CALCULATION_ENGINE.md`: Provides baseline stock levels (pre-intervention equilibrium)
- `05_MECHANISM_BANK_STRUCTURE.md`: Provides functional forms, latency profiles, and effect sizes
- `12_GEOGRAPHIC_CONTEXTUALIZATION.md`: Provides context-adjusted mechanism weights

**Output to**:
- `15_USER_INTERFACE_WORKFLOWS.md`: Time series data for dashboard rendering
- `16_VALIDATION_CONTINUOUS_IMPROVEMENT.md`: Predicted trajectories for comparison with observed outcomes

---

## 14. MVP Implementation Priorities

**Phase 1 (MVP)**:
- Annual time steps
- Linear and step function ramp-ups
- Default latency profiles (user cannot customize)
- Convergence detection (threshold-based)
- Monte Carlo uncertainty (N = 100 simulations for speed)

**Phase 2 Enhancements**:
- Quarterly time steps for rapid-onset interventions
- Custom latency profile specification by users
- Advanced convergence diagnostics (loop identification)
- Expanded Monte Carlo (N = 1000) with parallel computing
- Automatic persistence profile recommendation based on intervention type

---

*Document Version: 1.0*  
*Cross-References*: `[06_EQUILIBRIUM_CALCULATION_ENGINE.md]`, `[05_MECHANISM_BANK_STRUCTURE.md]`, `[12_GEOGRAPHIC_CONTEXTUALIZATION.md]`, `[08_EFFECT_SIZE_TRANSLATION.md]`  
*Status*: Technical specification for MVP implementation
