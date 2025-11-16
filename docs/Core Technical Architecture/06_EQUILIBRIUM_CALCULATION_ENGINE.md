# Equilibrium Calculation Engine
## Pre-Intervention Baseline Calibration and Post-Intervention Dynamics

**Document ID**: 06_EQUILIBRIUM_CALCULATION_ENGINE.md  
**Version**: 2.0  
**Last Updated**: November 15, 2025  
**Tier**: 2 - Core Technical Architecture

---

## Table of Contents

1. [Overview](#overview)
2. [Pre-Intervention Baseline Calculation](#pre-intervention-baseline-calculation)
3. [Inverse Calibration Mathematics](#inverse-calibration-mathematics)
4. [Dampened Equilibrium with Feedback Loops](#dampened-equilibrium-with-feedback-loops)
5. [Solving for Unknown Stocks](#solving-for-unknown-stocks)
6. [Convergence Criteria and Algorithms](#convergence-criteria-and-algorithms)
7. [Implementation Pseudocode](#implementation-pseudocode)

---

## Overview

### The Equilibrium Challenge

**Problem**: Given a system with ~100 active stocks and ~500 mechanisms (many bidirectional, creating feedback loops), calculate:

1. **Pre-intervention baseline**: Current state where system is at equilibrium (observed reality)
2. **Post-intervention state**: New equilibrium OR trajectory after user changes a stock

**Constraints**:
- Crisis endpoint stocks MUST equal observed values (anchored to reality)
- Structural stocks MUST equal measured capacities
- Intermediate stocks UNKNOWN (must be calculated)
- All stocks must satisfy equilibrium condition: Σ(inflows) = Σ(outflows)
- Feedback loops must be bounded (no runaway growth)

### Solution Approach

**Hybrid method combining**:
1. **Inverse calibration**: Work backwards from crisis endpoints
2. **Linearized approximation**: Initial estimate via matrix inversion
3. **Nonlinear refinement**: Iterative relaxation with dampening
4. **Validation**: Check that calculated baseline reproduces observed data

---

## Pre-Intervention Baseline Calculation

### Input Data Structure

**Known stocks (fixed at observed/measured values)**:

```python
known_stocks = {
  # Crisis endpoints (from hospital/admin data)
  'ed_visits_annual': 122400,
  'hospitalizations_annual': 18500,
  'deaths_premature_annual': 850,
  'overdose_events_annual': 420,
  
  # Structural capacity (from organizational records)
  'chw_capacity': 50,
  'affordable_housing_units': 3200,
  'pcp_density': 165,
  
  # Demographics (from Census)
  'population': 680000,
  'poverty_rate': 0.28,
  'uninsured_rate': 0.08,
  
  # [~15 total known stocks]
}
```

**Unknown stocks (to be calculated)**:

```python
unknown_stocks = {
  # Intermediate proxies
  'healthcare_continuity': None,  # Calculate from mechanisms
  'economic_precarity': None,
  'community_trust': None,
  'housing_stability': None,
  'social_isolation': None,
  
  # Behavioral/utilization
  'healthcare_seeking_rate': None,
  'medication_adherence': None,
  
  # [~85 total unknown stocks]
}
```

### Equilibrium Condition

**For each unknown stock S_i, must satisfy**:

```
At equilibrium:
  Σ(flows into S_i) - Σ(flows out of S_i) = 0

Where:
  Flow_ji = mechanism from stock j to stock i
  Flow_ik = mechanism from stock i to stock k
  
  Σ(inflows) = Σ Flow_ji for all j connected to i
  Σ(outflows) = Σ Flow_ik for all k that i connects to
```

**Example: Healthcare Continuity stock**

```python
Inflows to Healthcare_Continuity:
  + Flow from CHW_Capacity (mechanism: chw_continuity)
  + Flow from Healthcare_Integration (mechanism: integration_continuity)
  + Flow from Insurance_Stability (mechanism: insurance_continuity)

Outflows from Healthcare_Continuity:
  - Flow to ED_Utilization (mechanism: continuity_ed)
  - Flow to Medication_Adherence (mechanism: continuity_adherence)
  - Flow to Healthcare_Seeking (mechanism: continuity_seeking)

Equilibrium condition:
  Inflows - Outflows = 0
  
  (Flow_CHW + Flow_Integration + Flow_Insurance) - 
  (Flow_ED + Flow_Adherence + Flow_Seeking) = 0
```

---

## Inverse Calibration Mathematics

### Step 1: Linearize Around Operating Point

**Approximate nonlinear mechanisms as linear near baseline**:

```
General mechanism:
  Flow_ij = f(Stock_i, parameters)
  
Linearized:
  Flow_ij ≈ f(Stock_i*) + f'(Stock_i*) × (Stock_i - Stock_i*)
  
Where:
  Stock_i* = initial guess for Stock_i
  f'(Stock_i*) = derivative at operating point
```

**Example: Sigmoid mechanism linearized**

```python
Original:
  Flow = alpha × (L / (1 + exp(-k × (S_i - x0))))

Linearized around S_i* = x0:
  Flow ≈ (alpha × L / 2) + (alpha × L × k / 4) × (S_i - x0)
  
  # At operating point x0:
  # - Function value: L/2 (midpoint of sigmoid)
  # - Derivative: L × k / 4 (steepest slope)
```

### Step 2: Express as Matrix Equation

**For N unknown stocks, create system of N linear equations**:

```
A × S = B

Where:
  S = [S_1, S_2, ..., S_N]  (vector of unknown stocks)
  A = N×N matrix of mechanism derivatives
  B = N×1 vector of boundary conditions (from known stocks)
```

**Matrix construction**:

```python
A[i,j] = ∂(Net_Flow_i) / ∂S_j

Where Net_Flow_i = Σ(inflows to i) - Σ(outflows from i)

Example for Healthcare_Continuity (row i):
  A[i, chw_capacity] = derivative of CHW→Continuity mechanism w.r.t. CHW
  A[i, continuity] = sum of derivatives of all mechanisms involving continuity
  A[i, ed_utilization] = derivative of Continuity→ED mechanism w.r.t. Continuity
  
B[i] = target value considering known stocks
```

### Step 3: Solve Matrix System

**Initial estimate via matrix inversion**:

```python
S_initial = A^(-1) × B

# Standard linear algebra
# Using NumPy: np.linalg.solve(A, B)
```

**Challenges**:
- Matrix may be ill-conditioned (feedback loops create dependencies)
- Solution may violate bounds (negative stocks, impossible values)
- Linear approximation valid only near operating point

**Solutions**:
- Regularization (add small diagonal term to A for stability)
- Constrained optimization (enforce S_i ∈ [min_i, max_i])
- Use as initial guess, refine with nonlinear iteration

---

## Dampened Equilibrium with Feedback Loops

### Feedback Loop Bounding

**All mechanisms use bounded functional forms to prevent runaway**:

1. **Sigmoid**: Natural saturation (max value L)
2. **Logarithmic**: Diminishing returns (never infinite)
3. **Saturating Linear**: Hard cap at maximum
4. **Threshold**: Zero below threshold, linear above (bounded by stock range)
5. **Multiplicative Dampening**: Self-limiting (approaches zero as stock approaches max)

**Example: Reinforcing loop with bounds**

```python
Loop: Community_Trust → Participation → Organizing_Success → Community_Trust

Without bounds:
  Trust(t+1) = Trust(t) + alpha × Success(t)
  # Can grow to infinity

With sigmoid bounds:
  Trust(t+1) = Trust(t) + alpha × sigmoid(Success(t) - Trust(t))
  # Where sigmoid saturates at Trust = 1.0
  
  # As Trust approaches 1.0:
  # - sigmoid(Success - 1.0) ≈ 0 (no room for growth)
  # - System stabilizes
```

### Balancing Loops

**Negative feedback automatically stabilizes**:

```python
Example: ED_Utilization → Hospital_Capacity_Strain → Wait_Times → Care_Avoidance → ED_Utilization

High ED use → Strain increases → Wait times increase → 
People avoid ED → ED use decreases → Strain decreases → 
Wait times decrease → People return to ED → ED use increases

Natural oscillation dampens to equilibrium
```

### Multiple Equilibria Handling

**When system has multiple stable states**:

```python
Example: Trust loop has two equilibria:
  1. Low equilibrium: Trust = 0.25, Participation = 0.15 (stable)
  2. High equilibrium: Trust = 0.80, Participation = 0.70 (stable)

Selection strategy:
  1. Use initial guess closest to empirical indicators
  2. If local data suggests "high trust community" → seed near high equilibrium
  3. If indicators suggest "low trust" → seed near low equilibrium
  4. Document which equilibrium selected and why
  5. Sensitivity: Test both equilibria, show range
```

---

## Solving for Unknown Stocks

### Algorithm: Iterative Relaxation

**Hybrid approach: Linearized initialization + nonlinear refinement**

```python
def solve_equilibrium(known_stocks, mechanisms, max_iterations=1000):
    """
    Calculate baseline equilibrium for unknown stocks.
    
    Args:
        known_stocks: dict of {stock_id: value} for measured stocks
        mechanisms: list of mechanism objects with functional forms
        max_iterations: convergence limit
        
    Returns:
        all_stocks: dict with calculated values for all stocks
    """
    
    # PHASE 1: Initialize unknown stocks
    unknown_stocks = initialize_unknowns(known_stocks, mechanisms)
    
    # PHASE 2: Linearized approximation
    A, B = construct_linear_system(known_stocks, unknown_stocks, mechanisms)
    unknown_values = solve_linear_system(A, B)
    update_stocks(unknown_stocks, unknown_values)
    
    # PHASE 3: Nonlinear refinement
    for iteration in range(max_iterations):
        # Calculate all mechanism flows
        flows = calculate_all_flows(known_stocks, unknown_stocks, mechanisms)
        
        # Calculate net flow for each unknown stock
        net_flows = calculate_net_flows(unknown_stocks, flows)
        
        # Update stocks with dampening
        for stock_id in unknown_stocks:
            delta = net_flows[stock_id]
            dampening_factor = 0.3  # Prevent oscillation
            unknown_stocks[stock_id] += dampening_factor × delta
            
            # Enforce bounds
            unknown_stocks[stock_id] = clip(
                unknown_stocks[stock_id],
                min_value[stock_id],
                max_value[stock_id]
            )
        
        # Check convergence
        if max(abs(net_flows.values())) < convergence_threshold:
            break
    
    # PHASE 4: Validation
    validate_equilibrium(known_stocks, unknown_stocks, mechanisms)
    
    return {**known_stocks, **unknown_stocks}


def initialize_unknowns(known_stocks, mechanisms):
    """
    Educated guesses for unknown stocks based on:
    1. Regional averages
    2. Proxy indicators
    3. Literature-based typical ranges
    """
    guesses = {}
    
    # Example: Healthcare continuity
    # National average: 0.50
    # Boston has generous Medicaid → adjust upward: 0.55
    guesses['healthcare_continuity'] = 0.55
    
    # Example: Economic precarity
    # Based on poverty rate (0.28) + rent burden indicators
    guesses['economic_precarity'] = 0.38
    
    return guesses


def calculate_all_flows(known, unknown, mechanisms):
    """
    Evaluate each mechanism using current stock values.
    """
    stocks = {**known, **unknown}  # Combine all stocks
    flows = {}
    
    for mechanism in mechanisms:
        from_stock = stocks[mechanism.from_node]
        to_stock = stocks[mechanism.to_node]
        
        # Apply functional form with moderators
        flow_value = mechanism.evaluate(from_stock, to_stock, moderators)
        
        flows[(mechanism.from_node, mechanism.to_node)] = flow_value
    
    return flows


def calculate_net_flows(unknown_stocks, flows):
    """
    For each unknown stock, calculate: inflows - outflows
    """
    net = {stock_id: 0.0 for stock_id in unknown_stocks}
    
    for (from_node, to_node), flow_value in flows.items():
        if to_node in unknown_stocks:
            net[to_node] += flow_value  # Inflow
        if from_node in unknown_stocks:
            net[from_node] -= flow_value  # Outflow
    
    return net


def validate_equilibrium(known, unknown, mechanisms):
    """
    Check that calculated equilibrium produces observed crisis endpoints.
    """
    # Recalculate crisis endpoint stocks from mechanisms
    predicted_ed_visits = calculate_via_mechanisms(
        {**known, **unknown},
        target='ed_visits_annual',
        mechanisms
    )
    
    observed_ed_visits = known['ed_visits_annual']
    
    error = abs(predicted_ed_visits - observed_ed_visits) / observed_ed_visits
    
    if error > 0.10:  # More than 10% error
        warn(f"Equilibrium does not reproduce observed ED visits: {error:.1%} error")
        # May need to adjust moderators or refine mechanisms
    
    return error < 0.10  # Pass if within 10%
```

---

## Convergence Criteria and Algorithms

### Convergence Definition

**System converged when all of these conditions met**:

```python
CONVERGENCE_CRITERIA = {
    'max_stock_change': 0.01,      # Largest stock change < 1%
    'max_flow_imbalance': 0.001,   # Largest net flow < 0.1%
    'min_iterations': 10,          # Run at least 10 iterations
    'max_iterations': 1000,        # Fail-safe: stop after 1000
}

def check_convergence(stocks, flows, iteration):
    # Criterion 1: Stock changes small
    stock_changes = [abs(stocks[t] - stocks[t-1]) / stocks[t-1] 
                     for t in range(1, len(stocks))]
    max_stock_change = max(stock_changes)
    
    # Criterion 2: Flow imbalances small
    net_flows = calculate_net_flows(stocks[-1], flows)
    max_imbalance = max(abs(net_flows.values()))
    
    # Criterion 3: Minimum iterations completed
    min_iters_met = iteration >= CONVERGENCE_CRITERIA['min_iterations']
    
    converged = (
        max_stock_change < CONVERGENCE_CRITERIA['max_stock_change'] and
        max_imbalance < CONVERGENCE_CRITERIA['max_flow_imbalance'] and
        min_iters_met
    )
    
    return converged, {
        'max_stock_change': max_stock_change,
        'max_imbalance': max_imbalance,
        'iteration': iteration
    }
```

### Handling Non-Convergence

**If system doesn't converge**:

```python
def handle_non_convergence(stocks, flows, mechanisms):
    """
    Diagnose why system not converging and attempt fixes.
    """
    
    # Diagnosis 1: Oscillation (alternating between values)
    if detect_oscillation(stocks):
        # Fix: Increase dampening factor
        return retry_with_dampening(dampening=0.1)  # Slower updates
    
    # Diagnosis 2: Runaway growth (unbounded mechanism)
    if detect_runaway(stocks):
        # Fix: Check mechanism bounds, add saturation
        problematic_mechanisms = find_unbounded_mechanisms(mechanisms)
        log_error(f"Unbounded mechanisms: {problematic_mechanisms}")
        return None  # Manual intervention required
    
    # Diagnosis 3: Conflicting constraints (overdetermined system)
    if detect_conflicts(stocks, flows):
        # Fix: Relax some constraints, widen tolerance
        return retry_with_relaxed_constraints()
    
    # Diagnosis 4: Poor initial guess (wrong basin of attraction)
    if iteration < 100:  # Early failure suggests bad initialization
        # Fix: Try different initial values
        return retry_with_alternative_initialization()
    
    # If all else fails: report to user
    return None
```

### Dampening Strategies

**Adaptive dampening for stability**:

```python
def adaptive_dampening(iteration, stock_changes):
    """
    Adjust dampening factor based on convergence behavior.
    """
    if iteration < 10:
        # Early iterations: aggressive updates
        return 0.5
    elif max(stock_changes) > 0.10:
        # Large changes: slow down
        return 0.2
    elif max(stock_changes) < 0.02:
        # Near convergence: can speed up slightly
        return 0.4
    else:
        # Default: moderate dampening
        return 0.3
```

---

## Implementation Pseudocode

### Complete Baseline Calculation

```python
def calculate_baseline_equilibrium(
    geography_id,
    observed_crisis_endpoints,
    measured_structural_stocks,
    mechanism_bank,
    node_bank
):
    """
    Full workflow for baseline equilibrium calculation.
    """
    
    # STEP 1: Load geographic context
    geographic_context = load_geographic_context(geography_id)
    policy_environment = geographic_context['policy']
    demographics = geographic_context['demographics']
    
    # STEP 2: Select relevant mechanisms
    active_mechanisms = prune_mechanisms(
        mechanism_bank,
        geography=geographic_context,
        threshold=relevance_threshold
    )
    print(f"Active mechanisms: {len(active_mechanisms)}")
    
    # STEP 3: Apply moderators
    adjusted_mechanisms = apply_moderators(
        active_mechanisms,
        policy=policy_environment,
        demographics=demographics
    )
    
    # STEP 4: Initialize stocks
    known_stocks = {
        **observed_crisis_endpoints,
        **measured_structural_stocks,
        **demographics
    }
    
    unknown_stocks = [node for node in node_bank 
                     if node.id not in known_stocks]
    
    # STEP 5: Solve equilibrium
    print("Solving equilibrium...")
    equilibrium_stocks = solve_equilibrium(
        known_stocks=known_stocks,
        unknown_stocks=unknown_stocks,
        mechanisms=adjusted_mechanisms,
        max_iterations=1000
    )
    
    # STEP 6: Validate
    print("Validating...")
    validation_results = validate_equilibrium(
        equilibrium_stocks,
        observed_crisis_endpoints,
        adjusted_mechanisms
    )
    
    if not validation_results['passed']:
        warn(f"Validation issues: {validation_results['errors']}")
        # Document issues but proceed with caveats
    
    # STEP 7: Store baseline
    baseline = {
        'geography_id': geography_id,
        'stocks': equilibrium_stocks,
        'mechanisms': adjusted_mechanisms,
        'validation': validation_results,
        'timestamp': datetime.now(),
        'version': '2.0'
    }
    
    save_baseline(baseline)
    
    return baseline


def validate_equilibrium(stocks, observed_endpoints, mechanisms):
    """
    Multi-level validation of calculated equilibrium.
    """
    results = {'passed': True, 'errors': [], 'warnings': []}
    
    # Validation 1: Crisis endpoints match observations
    for endpoint_id, observed_value in observed_endpoints.items():
        calculated_value = stocks[endpoint_id]
        error_pct = abs(calculated_value - observed_value) / observed_value
        
        if error_pct > 0.15:  # More than 15% error
            results['passed'] = False
            results['errors'].append({
                'endpoint': endpoint_id,
                'observed': observed_value,
                'calculated': calculated_value,
                'error_pct': error_pct
            })
        elif error_pct > 0.10:  # 10-15% error (warning)
            results['warnings'].append({
                'endpoint': endpoint_id,
                'error_pct': error_pct
            })
    
    # Validation 2: All stocks within plausible ranges
    for stock_id, value in stocks.items():
        bounds = get_bounds(stock_id)
        if value < bounds['min'] or value > bounds['max']:
            results['passed'] = False
            results['errors'].append({
                'stock': stock_id,
                'value': value,
                'bounds': bounds,
                'issue': 'out of bounds'
            })
    
    # Validation 3: Net flows near zero
    flows = calculate_all_flows(stocks, mechanisms)
    net_flows = calculate_net_flows(stocks, flows)
    max_imbalance = max(abs(net_flows.values()))
    
    if max_imbalance > 0.01:  # More than 1% imbalance
        results['warnings'].append({
            'issue': 'flow imbalance',
            'max_imbalance': max_imbalance
        })
    
    return results
```

---

## Document Metadata

**Version History**:
- v1.0 (2024-06): Initial equilibrium calculation specs
- v2.0 (2025-11): Added inverse calibration, dampening algorithms, validation methods

**Related Documents**:
- [04_STOCK_FLOW_PARADIGM.md] - Stock definitions
- [05_MECHANISM_BANK_STRUCTURE.md] - Mechanism specifications
- [07_TIME_SIMULATION_FRAMEWORK.md] - Post-intervention dynamics
- [18_REFERENCE_IMPLEMENTATION_MVP.md] - Concrete implementation

**Last Reviewed**: November 15, 2025  
**Next Review**: February 15, 2026

---

**END OF DOCUMENT**
