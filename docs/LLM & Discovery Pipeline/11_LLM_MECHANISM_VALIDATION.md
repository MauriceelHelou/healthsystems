# 11: LLM Mechanism Validation
**Automated Quality Assurance and Continuous Monitoring**

---

## ⚠️ MVP Scope: Topology Validation Only

**This document describes validation for both MVP and Phase 2**. Scope differs:

**MVP Validation** (Current):
- ✓ **Topology validation**: Does pathway exist in literature?
- ✓ **Direction validation**: Is +/− consistent with evidence?
- ✓ **Logic validation**: No contradictions, circular dependencies
- ✓ **Citation validation**: Source studies exist and are accessible
- ✓ **Evidence strength**: Strong/moderate/limited rating appropriate

**Phase 2 Validation** (Future):
- ✗ **Effect size validation**: Numeric plausibility checks
- ✗ **Statistical validation**: CI ordering, heterogeneity, outliers
- ✗ **Meta-analytic validation**: Publication bias, sensitivity analysis
- ✗ **Moderator validation**: Quantified moderator consistency

**This Document Structure**:
- **Sections marked [MVP]** apply now
- **Sections marked [Phase 2]** deferred to quantification phase

---

## 1. Overview

This document specifies the validation framework that ensures mechanism bank integrity through **automated statistical checks** [Phase 2], **causal logic verification** [MVP], and **structural competency audits** [MVP]. The system operates as a **multi-stage gate** where mechanisms must pass validation checkpoints before deployment, with continuous monitoring post-release.

**Core Principle**: Validation is primarily **automated** to maintain scalability, with expert consultation available for edge cases. All checks are **reproducible** and **auditable**, generating structured validation reports for transparency.

---

## 2. Validation Architecture

### 2.1 Four-Layer Validation Framework

```
Layer 1: EXTRACTION VALIDATION [MVP]
├─ Trigger: Immediately after LLM topology discovery
├─ Checks: Data completeness, citation validity, direction specified
├─ Outcome: PASS → Stage 2 | FAIL → Quarantine for correction
└─ Gate: ~5% mechanisms quarantined at this stage
└─ [Phase 2]: Add numeric plausibility checks for effect sizes

Layer 2: STATISTICAL VALIDATION [Phase 2 Only]
├─ Trigger: After standardization and meta-analytic pooling
├─ Checks: CI ordering, heterogeneity assessment, outlier detection
├─ Outcome: PASS → Stage 3 | WARN → Flag but proceed | FAIL → Exclude
└─ Gate: ~10% mechanisms flagged with warnings
└─ MVP: SKIPPED (no effect sizes to validate)

Layer 3: CAUSAL LOGIC VALIDATION [MVP]
├─ Trigger: After complete mechanism record creation
├─ Checks: Direction consistency, feedback loop stability, network connectivity
├─ Outcome: PASS → Stage 4 | FAIL → Exclude or revise
└─ Gate: ~3% mechanisms fail causal logic checks

Layer 4: STRUCTURAL COMPETENCY AUDIT
├─ Trigger: Before mechanism bank deployment
├─ Checks: Structural origins traced, equity implications assessed
├─ Outcome: PASS → Deploy | FAIL → Revise or exclude
└─ Gate: ~2% mechanisms fail competency audit

Post-Deployment: CONTINUOUS MONITORING
├─ Trigger: Quarterly updates, new literature, user feedback
├─ Process: Re-validate all mechanisms against new evidence
├─ Outcome: Version updates, deprecation flags
```

**Cumulative Pass Rate**: ~80-85% of initially discovered mechanisms pass all validation gates and enter deployed mechanism bank.

---

## 3. Layer 1: Extraction Validation

### 3.1 Data Completeness Checks

```python
def validate_extraction_completeness(effect):
    """
    Ensure all required fields present and non-null
    """
    required_fields = [
        'effect_size_value',
        'effect_size_type',
        'sample_size',
        'outcome_definition',
        'exposure_definition'
    ]
    
    missing = [f for f in required_fields if f not in effect or effect[f] is None]
    
    if missing:
        return {
            "status": "FAIL",
            "reason": f"Missing required fields: {missing}",
            "action": "Re-extract with explicit field requirements"
        }
    
    return {"status": "PASS"}
```

### 3.2 Numeric Plausibility Checks

```python
def validate_numeric_plausibility(effect):
    """
    Check if extracted values are in plausible ranges
    """
    checks = []
    
    # Check 1: Effect size magnitude
    bounds = {
        "OR": (0.05, 20),
        "RR": (0.05, 10),
        "HR": (0.1, 10),
        "beta": (-3, 3),
        "cohen_d": (-3, 3),
        "percentage": (-100, 100),
        "correlation": (-1, 1)
    }
    
    effect_type = effect['effect_size_type']
    value = effect['effect_size_value']
    
    if effect_type in bounds:
        lower, upper = bounds[effect_type]
        if not (lower <= value <= upper):
            checks.append({
                "severity": "FAIL",
                "check": "effect_size_range",
                "message": f"{effect_type} = {value} outside plausible range [{lower}, {upper}]"
            })
    
    # Check 2: Sample size
    if not (10 <= effect['sample_size'] <= 10000000):
        checks.append({
            "severity": "WARN",
            "check": "sample_size",
            "message": f"Sample size = {effect['sample_size']} unusual"
        })
    
    # Check 3: CI ordering (if present)
    if 'confidence_interval' in effect and effect['confidence_interval']:
        ci_lower, ci_upper = effect['confidence_interval']
        
        # CI must bracket point estimate
        if not (ci_lower < value < ci_upper):
            checks.append({
                "severity": "FAIL",
                "check": "ci_ordering",
                "message": f"CI [{ci_lower}, {ci_upper}] doesn't bracket point estimate {value}"
            })
        
        # CI width sanity check (not collapsed to point)
        if abs(ci_upper - ci_lower) < 0.01 * abs(value):
            checks.append({
                "severity": "WARN",
                "check": "ci_width",
                "message": "CI suspiciously narrow"
            })
    
    # Check 4: SE calculation consistency
    if 'standard_error' in effect and 'confidence_interval' in effect:
        se_reported = effect['standard_error']
        ci_lower, ci_upper = effect['confidence_interval']
        se_from_ci = (ci_upper - ci_lower) / (2 * 1.96)
        
        if abs(se_reported - se_from_ci) / se_from_ci > 0.15:
            checks.append({
                "severity": "WARN",
                "check": "se_consistency",
                "message": f"Reported SE ({se_reported:.3f}) differs from CI-derived SE ({se_from_ci:.3f})"
            })
    
    # Aggregate
    fails = [c for c in checks if c['severity'] == "FAIL"]
    warns = [c for c in checks if c['severity'] == "WARN"]
    
    if fails:
        return {"status": "FAIL", "checks": checks}
    elif warns:
        return {"status": "WARN", "checks": checks}
    else:
        return {"status": "PASS"}
```

### 3.3 Citation Validity Checks

```python
import requests

def validate_citations(effect):
    """
    Verify DOI resolves and metadata matches
    """
    checks = []
    
    doi = effect.get('study_metadata', {}).get('doi')
    
    if not doi:
        checks.append({
            "severity": "WARN",
            "check": "doi_present",
            "message": "No DOI provided (acceptable for grey literature)"
        })
        return {"status": "PASS", "checks": checks}
    
    # Check DOI resolves
    try:
        response = requests.get(f"https://doi.org/{doi}", timeout=5)
        if response.status_code != 200:
            checks.append({
                "severity": "FAIL",
                "check": "doi_resolution",
                "message": f"DOI {doi} does not resolve (HTTP {response.status_code})"
            })
    except Exception as e:
        checks.append({
            "severity": "FAIL",
            "check": "doi_resolution",
            "message": f"DOI {doi} resolution error: {str(e)}"
        })
    
    # Check metadata consistency (if available)
    if 'authors' in effect['study_metadata'] and 'year' in effect['study_metadata']:
        # Fetch CrossRef metadata
        try:
            cr_response = requests.get(f"https://api.crossref.org/works/{doi}", timeout=5)
            if cr_response.status_code == 200:
                cr_data = cr_response.json()['message']
                
                # Check year matches
                cr_year = cr_data.get('published-print', {}).get('date-parts', [[None]])[0][0]
                extracted_year = effect['study_metadata']['year']
                
                if cr_year and abs(cr_year - extracted_year) > 1:
                    checks.append({
                        "severity": "WARN",
                        "check": "year_mismatch",
                        "message": f"Extracted year ({extracted_year}) differs from CrossRef ({cr_year})"
                    })
        except:
            pass  # CrossRef lookup optional
    
    fails = [c for c in checks if c['severity'] == "FAIL"]
    return {"status": "FAIL" if fails else "PASS", "checks": checks}
```

**Quarantine Process**:
```
If extraction validation fails:
  1. Log failure details (which checks failed, error messages)
  2. Generate re-extraction prompt with explicit corrections:
     "Previous extraction had {issue}. When extracting, ensure {correction}."
  3. Re-attempt extraction with corrected prompt (max 2 retries)
  4. If still fails: Exclude study from meta-analysis, document exclusion reason
```

---

## 4. Layer 2: Statistical Validation

### 4.1 Meta-Analysis Consistency Checks

```python
def validate_meta_analysis(pooled_result, standardized_effects):
    """
    Check statistical validity of pooled estimates
    """
    checks = []
    
    # Check 1: Pooled effect in reasonable range given individual studies
    individual_effects = [e['d_point'] for e in standardized_effects]
    min_effect = min(individual_effects)
    max_effect = max(individual_effects)
    pooled = pooled_result['d_pooled']
    
    if not (min_effect <= pooled <= max_effect):
        checks.append({
            "severity": "FAIL",
            "check": "pooled_within_range",
            "message": f"Pooled effect ({pooled:.3f}) outside individual study range [{min_effect:.3f}, {max_effect:.3f}]"
        })
    
    # Check 2: CI properly bounded
    ci_lower, ci_upper = pooled_result['ci_pooled']
    if not (ci_lower < pooled < ci_upper):
        checks.append({
            "severity": "FAIL",
            "check": "ci_ordering",
            "message": "Pooled CI doesn't bracket point estimate"
        })
    
    # Check 3: Heterogeneity assessment
    if 'I_squared' in pooled_result:
        I_squared = pooled_result['I_squared']
        
        if I_squared > 75:
            checks.append({
                "severity": "WARN",
                "check": "high_heterogeneity",
                "message": f"I² = {I_squared:.1f}% indicates high heterogeneity; consider moderator analysis"
            })
    
    # Check 4: Effect size symmetry (forest plot balance)
    positive_effects = sum(1 for e in individual_effects if e > 0)
    negative_effects = sum(1 for e in individual_effects if e < 0)
    
    if pooled > 0 and negative_effects > positive_effects:
        checks.append({
            "severity": "WARN",
            "check": "direction_imbalance",
            "message": "Pooled effect positive but majority of studies negative"
        })
    
    # Check 5: Standard error plausibility
    se_pooled = pooled_result['se_pooled']
    se_individual = [e['se'] for e in standardized_effects]
    min_se = min(se_individual)
    
    if se_pooled > min_se:
        checks.append({
            "severity": "WARN",
            "check": "se_inflation",
            "message": "Pooled SE larger than smallest individual SE (expected for random effects)"
        })
    
    fails = [c for c in checks if c['severity'] == "FAIL"]
    warns = [c for c in checks if c['severity'] == "WARN"]
    
    if fails:
        return {"status": "FAIL", "checks": checks}
    elif warns:
        return {"status": "WARN", "checks": checks}
    else:
        return {"status": "PASS"}
```

### 4.2 Outlier Detection

```python
def detect_outliers(standardized_effects, pooled_d):
    """
    Identify studies with unusually large deviations from pooled estimate
    """
    outliers = []
    
    for effect in standardized_effects:
        # Calculate standardized residual
        residual = effect['d_point'] - pooled_d
        z_score = residual / effect['se']
        
        if abs(z_score) > 3:
            outliers.append({
                "study_id": effect['study_id'],
                "d_point": effect['d_point'],
                "pooled_d": pooled_d,
                "z_score": z_score,
                "action": "Investigate study characteristics (different population? different outcome?)"
            })
    
    return outliers
```

**Outlier Handling**:
```
If outliers detected:
  1. Review study characteristics (population, context, outcome definition)
  2. If study differs meaningfully: Create separate subgroup or exclude with documentation
  3. If study similar: Include but note uncertainty
  4. Never exclude outliers solely due to statistical deviation
```

### 4.3 Publication Bias Assessment

```python
def assess_publication_bias(standardized_effects):
    """
    Detect and correct for publication bias
    """
    from scipy.stats import linregress
    
    n_studies = len(standardized_effects)
    
    if n_studies < 10:
        return {
            "status": "INSUFFICIENT_DATA",
            "message": "Publication bias tests require ≥10 studies"
        }
    
    # Egger's test
    effect_sizes = [e['d_point'] for e in standardized_effects]
    standard_errors = [e['se'] for e in standardized_effects]
    precisions = [1/se for se in standard_errors]
    
    slope, intercept, r_value, p_value, std_err = linregress(precisions, effect_sizes)
    
    bias_detected = p_value < 0.10
    
    result = {
        "egger_test": {
            "intercept": intercept,
            "p_value": p_value,
            "interpretation": "Asymmetry detected" if bias_detected else "No asymmetry"
        }
    }
    
    # If bias detected, apply trim-and-fill
    if bias_detected:
        adjusted_effects, n_imputed = trim_and_fill_correction(standardized_effects)
        adjusted_pooled = meta_analyze(adjusted_effects)
        
        result["correction"] = {
            "method": "trim_and_fill",
            "n_studies_imputed": n_imputed,
            "adjusted_d": adjusted_pooled['d_pooled'],
            "recommendation": "Use adjusted estimate for conservative projections"
        }
    
    return result
```

---

## 5. Layer 3: Causal Logic Validation

### 5.1 Direction Consistency Checks

```python
def validate_causal_direction(mechanism):
    """
    Verify mechanism description matches statistical directionality
    """
    description = mechanism['mechanism_description'].lower()
    directionality = mechanism['directionality']
    effect_sign = np.sign(mechanism['effect_quantification']['meta_analysis']['d_pooled'])
    
    # Keywords suggesting positive relationship
    positive_keywords = ['increase', 'improve', 'enhance', 'strengthen', 'promote']
    
    # Keywords suggesting negative relationship  
    negative_keywords = ['decrease', 'reduce', 'worsen', 'weaken', 'prevent', 'lower']
    
    pos_count = sum(1 for kw in positive_keywords if kw in description)
    neg_count = sum(1 for kw in negative_keywords if kw in description)
    
    # Check consistency
    if directionality == "positive":
        if neg_count > pos_count:
            return {
                "status": "WARN",
                "message": "Mechanism labeled 'positive' but description contains negative keywords",
                "action": "Review mechanism description for accuracy"
            }
        if effect_sign < 0:
            return {
                "status": "FAIL",
                "message": "Mechanism labeled 'positive' but effect size negative",
                "action": "Correct directionality or investigate sign error"
            }
    
    elif directionality == "negative":
        if pos_count > neg_count:
            return {
                "status": "WARN",
                "message": "Mechanism labeled 'negative' but description contains positive keywords"
            }
        if effect_sign > 0:
            return {
                "status": "FAIL",
                "message": "Mechanism labeled 'negative' but effect size positive"
            }
    
    return {"status": "PASS"}
```

### 5.2 Feedback Loop Stability Analysis

```python
import networkx as nx

def validate_feedback_loops(mechanisms, nodes):
    """
    Identify feedback loops and check for stabilization mechanisms
    """
    # Build directed graph
    G = nx.DiGraph()
    for mech in mechanisms:
        G.add_edge(
            mech['source_node'],
            mech['target_node'],
            mechanism_id=mech['mechanism_id'],
            functional_form=mech.get('functional_form', 'linear')
        )
    
    # Find all cycles
    cycles = list(nx.simple_cycles(G))
    
    unstable_loops = []
    
    for cycle in cycles:
        # Check if reinforcing (all positive) or balancing (mix of signs)
        edges_in_cycle = []
        for i in range(len(cycle)):
            source = cycle[i]
            target = cycle[(i+1) % len(cycle)]
            
            # Find mechanism for this edge
            mech = next(m for m in mechanisms if m['source_node'] == source and m['target_node'] == target)
            edges_in_cycle.append(mech)
        
        # Count positive/negative relationships
        positive_edges = sum(1 for m in edges_in_cycle if m['directionality'] == 'positive')
        
        # Reinforcing loop: all positive or even number of negatives
        is_reinforcing = (positive_edges == len(edges_in_cycle)) or (len(edges_in_cycle) - positive_edges) % 2 == 0
        
        if is_reinforcing:
            # Check for saturation mechanisms
            has_saturation = any(
                m.get('functional_form') in ['sigmoid', 'logarithmic', 'saturating_linear']
                for m in edges_in_cycle
            )
            
            if not has_saturation:
                unstable_loops.append({
                    "cycle": cycle,
                    "type": "reinforcing",
                    "issue": "No saturation function; may grow unbounded",
                    "recommendation": "Add sigmoid or logarithmic functional form to at least one mechanism"
                })
    
    if unstable_loops:
        return {
            "status": "FAIL",
            "unstable_loops": unstable_loops,
            "action": "Review functional forms and add saturation mechanisms"
        }
    
    return {"status": "PASS", "cycles_detected": len(cycles)}
```

### 5.3 Network Connectivity Validation

> **Note**: All node references must exist in `mechanism-bank/mechanisms/canonical_nodes.json`. Node levels correspond to the scale hierarchy (1=Structural Policy, 2=Institutional, 3=Individual/Household, 4=Intermediate, 5=Crisis Endpoints).

```python
def validate_network_connectivity(mechanisms, nodes):
    """
    Ensure all nodes reachable from intervention points
    Node references: mechanism-bank/mechanisms/canonical_nodes.json
    """
    G = nx.DiGraph()
    for mech in mechanisms:
        G.add_edge(mech['source_node'], mech['target_node'])

    # Identify intervention nodes (Scale 1-2: structural/institutional)
    # Examples: medicaid_expansion_status, primary_care_physician_density
    intervention_nodes = [n['node_id'] for n in nodes if n['node_level'] <= 2]

    # Identify outcome nodes (Scale 5: crisis endpoints)
    # Examples: emergency_department_visit_rate, asthma_hospitalization_rate
    outcome_nodes = [n['node_id'] for n in nodes if n['node_level'] == 5]
    
    # Check if all outcomes reachable from interventions
    unreachable_outcomes = []
    for outcome in outcome_nodes:
        reachable = False
        for intervention in intervention_nodes:
            if nx.has_path(G, intervention, outcome):
                reachable = True
                break
        
        if not reachable:
            unreachable_outcomes.append(outcome)
    
    if unreachable_outcomes:
        return {
            "status": "WARN",
            "message": f"{len(unreachable_outcomes)} outcome nodes not reachable from interventions",
            "unreachable": unreachable_outcomes,
            "action": "Add missing mechanisms or verify node hierarchy"
        }
    
    # Check for isolated nodes (no connections)
    isolated = list(nx.isolates(G))
    if isolated:
        return {
            "status": "FAIL",
            "message": f"{len(isolated)} nodes have no connections",
            "isolated_nodes": isolated,
            "action": "Remove isolated nodes or add connecting mechanisms"
        }
    
    return {"status": "PASS"}
```

---

## 6. Layer 4: Structural Competency Audit

### 6.1 Structural Origins Verification

```python
def audit_structural_origins(mechanism):
    """
    Verify mechanism traces to structural determinants (not individual behaviors)
    """
    source_node = mechanism['source_node']
    node_level = get_node_level(source_node)
    
    # Level 1-2 nodes are inherently structural
    if node_level <= 2:
        return {"status": "PASS"}
    
    # Level 3+ nodes must have documented structural origins
    if 'structural_origin' not in get_node_metadata(source_node):
        return {
            "status": "FAIL",
            "message": f"Node {source_node} (Level {node_level}) lacks structural origin documentation",
            "action": "Document how this proximal condition is shaped by policy/economic/spatial structures"
        }
    
    # Check if structural origin is substantive (not just "individual choice")
    origin = get_node_metadata(source_node)['structural_origin']
    
    behavioral_keywords = ['individual choice', 'personal behavior', 'lifestyle', 'preference']
    if any(kw in origin.lower() for kw in behavioral_keywords):
        return {
            "status": "WARN",
            "message": "Structural origin emphasizes individual behavior; may not align with structural competency framework",
            "action": "Reframe origin to highlight structural constraints (policy, economics, built environment)"
        }
    
    return {"status": "PASS"}
```

### 6.2 Equity Implications Assessment

```python
def assess_equity_implications(mechanism):
    """
    Verify mechanism encodes differential effects by race/ethnicity, SES, or other equity dimensions
    """
    # Check if stratified effects present
    if 'stratified_effects' not in mechanism['effect_quantification']:
        return {
            "status": "WARN",
            "message": "No stratified effects encoded; mechanism assumes universal effect",
            "recommendation": "Search literature for differential effects by race, SES, age"
        }
    
    stratified = mechanism['effect_quantification']['stratified_effects']
    
    # Prioritize race/ethnicity and SES stratification
    priority_strata = ['race', 'ethnicity', 'ses', 'income']
    has_priority = any(s['stratum_type'] in priority_strata for s in stratified)
    
    if not has_priority:
        return {
            "status": "WARN",
            "message": "Stratified effects present but don't include race/ethnicity or SES",
            "recommendation": "Prioritize equity-relevant stratification"
        }
    
    return {"status": "PASS", "n_strata": len(stratified)}
```

### 6.3 Mechanism Plausibility Review

**LLM Self-Critique**:
```python
def llm_self_critique(mechanism):
    """
    Use LLM to identify potential issues in mechanism logic
    """
    prompt = f"""
    SYSTEM: You are critically evaluating a causal mechanism for plausibility.
    
    MECHANISM:
    {json.dumps(mechanism, indent=2)}
    
    TASK: Identify potential issues:
    1. Is the mechanism biologically/socially plausible?
    2. Could there be reverse causation (does target actually cause source)?
    3. Are there likely confounders not mentioned?
    4. Does the effect size seem reasonable given the mechanism?
    5. Are there known exceptions or boundary conditions?
    
    OUTPUT: JSON with criticisms
    {{
      "plausibility": "high" | "moderate" | "low",
      "concerns": [list of specific concerns],
      "confidence": "This mechanism is well-established" | "This mechanism is plausible but understudied" | "This mechanism seems unlikely"
    }}
    """
    
    response = call_llm(model="claude-opus-4", prompt=prompt, temperature=0.3)
    critique = json.loads(response)
    
    if critique['plausibility'] == 'low':
        return {
            "status": "WARN",
            "critique": critique,
            "action": "Review mechanism logic; consider excluding or revising"
        }
    
    return {"status": "PASS", "critique": critique}
```

---

## 7. Continuous Monitoring Post-Deployment

### 7.1 New Literature Integration

```python
def monitor_new_literature(mechanism, quarterly_corpus_update):
    """
    Check if new studies affect mechanism parameters
    """
    # Search for new studies on this mechanism
    new_studies = search_literature(
        query=mechanism['mechanism_description'],
        date_range=(mechanism['last_updated'], 'now'),
        min_quality='cohort'
    )
    
    if len(new_studies) == 0:
        return {"status": "NO_UPDATE", "message": "No new relevant studies"}
    
    # Extract effects from new studies
    new_effects = [extract_effect(study, mechanism) for study in new_studies]
    
    # Re-run meta-analysis with new studies included
    combined_effects = mechanism['supporting_studies'] + new_effects
    updated_pooled = meta_analyze(combined_effects)
    
    # Check if effect size changed significantly
    old_d = mechanism['effect_quantification']['meta_analysis']['d_pooled']
    new_d = updated_pooled['d_pooled']
    
    change_magnitude = abs(new_d - old_d)
    change_percent = change_magnitude / abs(old_d) * 100
    
    if change_percent > 20:
        return {
            "status": "SIGNIFICANT_UPDATE",
            "old_d": old_d,
            "new_d": new_d,
            "change_percent": change_percent,
            "n_new_studies": len(new_studies),
            "action": "Update mechanism bank; notify users of change"
        }
    elif change_percent > 10:
        return {
            "status": "MINOR_UPDATE",
            "old_d": old_d,
            "new_d": new_d,
            "change_percent": change_percent,
            "action": "Update mechanism bank in next release"
        }
    else:
        return {
            "status": "NO_SIGNIFICANT_CHANGE",
            "message": "New studies confirm existing estimate"
        }
```

### 7.2 User Feedback Integration

```python
def process_user_feedback(mechanism, feedback_log):
    """
    Analyze user-reported issues with mechanism
    """
    # Aggregate feedback by type
    feedback_types = {
        "inaccurate_prediction": [],
        "missing_moderator": [],
        "direction_error": [],
        "magnitude_error": []
    }
    
    for feedback in feedback_log:
        if feedback['mechanism_id'] == mechanism['mechanism_id']:
            feedback_types[feedback['issue_type']].append(feedback)
    
    # If multiple users report same issue, flag for review
    critical_threshold = 3  # 3+ users reporting same issue
    
    issues = []
    for issue_type, reports in feedback_types.items():
        if len(reports) >= critical_threshold:
            issues.append({
                "issue_type": issue_type,
                "n_reports": len(reports),
                "example_reports": reports[:3],
                "action": "Priority review required"
            })
    
    if issues:
        return {
            "status": "REVIEW_REQUIRED",
            "issues": issues
        }
    
    return {"status": "NO_ISSUES"}
```

### 7.3 Real-World Validation Tracking

```python
def track_prediction_accuracy(mechanism, intervention_outcomes):
    """
    Compare mechanism predictions to observed outcomes
    """
    predictions = []
    
    for intervention in intervention_outcomes:
        # Did this intervention use this mechanism?
        if mechanism['mechanism_id'] in intervention['mechanisms_applied']:
            
            # Compare predicted vs. observed
            predicted = intervention['predicted_outcome']
            observed = intervention['observed_outcome']
            
            error = abs(observed - predicted) / predicted
            
            predictions.append({
                "intervention_id": intervention['id'],
                "predicted": predicted,
                "observed": observed,
                "error_percent": error * 100
            })
    
    if len(predictions) == 0:
        return {"status": "NO_REAL_WORLD_DATA"}
    
    # Calculate average prediction error
    avg_error = np.mean([p['error_percent'] for p in predictions])
    
    if avg_error > 50:
        return {
            "status": "HIGH_PREDICTION_ERROR",
            "avg_error_percent": avg_error,
            "n_predictions": len(predictions),
            "action": "Mechanism may be mis-specified; review functional form and moderators"
        }
    elif avg_error > 30:
        return {
            "status": "MODERATE_PREDICTION_ERROR",
            "avg_error_percent": avg_error,
            "action": "Widen confidence intervals or add context-specific moderators"
        }
    else:
        return {
            "status": "PREDICTIONS_ACCURATE",
            "avg_error_percent": avg_error
        }
```

---

## 8. Validation Reporting

### 8.1 Mechanism Validation Report

```json
{
  "mechanism_id": "L2_014_to_L3_028",
  "validation_timestamp": "2026-01-15T10:30:00Z",
  "validation_version": "1.0",
  "overall_status": "PASS_WITH_WARNINGS",
  "layer_results": {
    "extraction_validation": {
      "status": "PASS",
      "checks_performed": 8,
      "checks_passed": 8
    },
    "statistical_validation": {
      "status": "WARN",
      "checks_performed": 5,
      "checks_passed": 4,
      "warnings": [
        {
          "check": "high_heterogeneity",
          "message": "I² = 62% indicates substantial heterogeneity"
        }
      ]
    },
    "causal_logic_validation": {
      "status": "PASS",
      "checks_performed": 3,
      "checks_passed": 3
    },
    "structural_competency_audit": {
      "status": "PASS",
      "checks_performed": 3,
      "checks_passed": 3
    }
  },
  "deployment_recommendation": "DEPLOY",
  "notes": "Mechanism validated for deployment. Monitor heterogeneity in future updates."
}
```

### 8.2 Aggregate Bank Health Metrics

```python
def generate_bank_health_report(mechanism_bank):
    """
    Summarize validation status across entire bank
    """
    total = len(mechanism_bank)
    
    status_counts = {
        "PASS": 0,
        "PASS_WITH_WARNINGS": 0,
        "FAIL": 0,
        "UNDER_REVIEW": 0
    }
    
    for mech in mechanism_bank:
        status_counts[mech['validation_status']] += 1
    
    return {
        "total_mechanisms": total,
        "pass_rate": status_counts["PASS"] / total * 100,
        "warn_rate": status_counts["PASS_WITH_WARNINGS"] / total * 100,
        "fail_rate": status_counts["FAIL"] / total * 100,
        "avg_n_studies_per_mechanism": np.mean([len(m['supporting_studies']) for m in mechanism_bank]),
        "avg_confidence": calculate_avg_confidence(mechanism_bank),
        "mechanisms_requiring_attention": [
            m['mechanism_id'] for m in mechanism_bank
            if m['validation_status'] in ["FAIL", "UNDER_REVIEW"]
        ]
    }
```

---

## 9. MVP Implementation Priorities

**Phase 1 (MVP)**:
- Automated validation for all 4 layers
- LLM self-critique for plausibility assessment
- Validation reports generated for each mechanism
- Deployment gates (fail = exclude from bank)
- Quarterly monitoring for new literature
- Basic user feedback collection

**Phase 2 Enhancements**:
- Real-world validation tracking (compare predictions to outcomes)
- Automated mechanism revision suggestions
- Advanced causal inference checks (instrumental variables, natural experiments)
- Cross-mechanism consistency checks (do related mechanisms align?)
- Community validation (crowdsourced review from epidemiologists)

---

## 10. Integration with Deployment Pipeline

**Validation as Gate**:
```
09_LLM_TOPOLOGY_DISCOVERY.md
  ↓ (Mechanisms discovered)
10_LLM_EFFECT_QUANTIFICATION.md
  ↓ (Effects quantified)
11_LLM_MECHANISM_VALIDATION.md ← YOU ARE HERE
  ↓ (Validated mechanisms only)
05_MECHANISM_BANK_STRUCTURE.md
  ↓ (Deployed in production)
```

**Only validated mechanisms** (status = PASS or PASS_WITH_WARNINGS) enter the deployed mechanism bank. Failed mechanisms are:
1. Logged with failure reasons
2. Flagged for optional manual review
3. Excluded from user-facing system

---

---

## Canonical Node Reference

All validation checks reference canonical nodes from `mechanism-bank/mechanisms/canonical_nodes.json`. Key node categories for validation:

| Scale | Level | Examples | Validation Role |
|-------|-------|----------|-----------------|
| 1 | Structural Policy | `medicaid_expansion_status`, `just_cause_eviction_protection` | Intervention entry points |
| 2 | Institutional | `primary_care_physician_density`, `emergency_department_availability` | Capacity nodes |
| 3 | Individual/Household | `eviction_filing_rate`, `housing_cost_burden` | Intermediate states |
| 5 | Crisis Endpoints | `emergency_department_visit_rate`, `all_cause_mortality_rate` | Outcome validation targets |

---

**Document Version**: 1.1
**Cross-References**: `[09_LLM_TOPOLOGY_DISCOVERY.md]`, `[10_LLM_EFFECT_QUANTIFICATION.md]`, `[05_MECHANISM_BANK_STRUCTURE.md]`, `[16_VALIDATION_CONTINUOUS_IMPROVEMENT.md]`, `mechanism-bank/mechanisms/canonical_nodes.json`
**Status**: Technical specification for MVP implementation
**Last Updated**: December 2, 2025
