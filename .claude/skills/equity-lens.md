# Equity Lens Validation Skill

You are reviewing mechanisms, code, and analyses through an **equity lens** - ensuring that the HealthSystems Platform explicitly identifies, quantifies, and addresses health inequities.

## Core Principle

**Equity-centered analysis** means:
1. Explicitly identifying differential effects across populations
2. Understanding structural roots of disparities
3. Prioritizing interventions that reduce inequities
4. Centering the experiences of marginalized communities

---

## Framework

### Equity vs. Equality

**Equality:** Same intervention for everyone
**Equity:** Interventions tailored to address differential needs and structural barriers

The platform focuses on **equity** - differential effects are expected and should be quantified.

### Key Equity Dimensions

All analyses should stratify by:

1. **Race/Ethnicity**
   - Structural racism shapes differential exposures and resources
   - Intersectionality: Race × income × geography
   - Avoid: Biological race, genetic explanations
   - Focus: Racialized policies (redlining, segregation, environmental racism)

2. **Income/Socioeconomic Status**
   - Economic inequality shapes access to resources
   - Poverty is structural, not individual failure
   - Consider: Wealth (not just income), intergenerational poverty
   - Focus: Wage policy, social safety net, resource distribution

3. **Geography**
   - Rural vs. urban
   - Region (policy variation)
   - Neighborhood (historical disinvestment, segregation)
   - Environmental exposures (pollution, food deserts, transit access)

4. **Other Dimensions (as relevant)**
   - Age (life course perspective)
   - Gender (structural sexism, gender-based violence)
   - Disability status (ableism, inaccessibility)
   - Immigration status (legal vulnerability, language access)
   - Housing status (homelessness, housing insecurity)

### The Equity Imperative

Every mechanism should answer:
1. **Who is most affected** by the problem?
2. **Who benefits most** from the intervention?
3. **Who is left out** or potentially harmed?
4. **Does this reduce or exacerbate** existing disparities?

---

## Review Criteria

### For Mechanisms

#### 1. Baseline Disparity Documentation

**Check:** Does the mechanism acknowledge baseline disparities in the outcome?

✓ **Good:**
```yaml
notes: |
  Asthma burden is disproportionate in low-income communities and communities
  of color due to structural factors: substandard housing (legacy of redlining),
  proximity to pollution sources (environmental racism), lack of healthcare access.

  Baseline asthma prevalence:
  - Low-income children: 15%
  - Higher-income children: 8%
  - Black children: 16%
  - White children: 7%
```

✗ **Missing:**
```yaml
notes: |
  Housing quality affects respiratory health.
  # No mention of who is most affected or why
```

#### 2. Differential Effect Specification

**Check:** Are moderators specified for equity dimensions?

✓ **Good:**
```yaml
moderators:
  demographic:
    - factor: baseline_asthma_prevalence
      effect_direction: positive
      rationale: Populations with higher baseline burden (due to structural
                 factors like environmental racism) experience larger absolute
                 benefit from housing quality improvement.

    - factor: income_level
      effect_direction: positive
      rationale: Low-income households more likely to experience substandard
                 housing due to segregation and disinvestment. Intervention
                 addresses this structural inequity directly.

    - factor: race_structural_exposure
      effect_direction: positive
      rationale: Communities of color disproportionately exposed to housing
                 hazards due to redlining and discriminatory lending. Remediation
                 addresses racialized structural determinant.
```

✗ **Problematic:**
```yaml
moderators:
  demographic:
    - factor: race
      effect_direction: positive
      rationale: Some racial groups have genetic susceptibility
      # ^^^ WRONG: Biologizes race, ignores structural racism
```

**Correction:**
- Never attribute disparities to genetics or biology
- Always frame in terms of structural factors: racism, economic inequality, historical policies
- Use terms like "racialized exposure," "structural racism," "discriminatory policies"

#### 3. Equity Impact Projection

**Check:** Does the mechanism quantify disparity reduction?

✓ **Good:**
```yaml
effect_size:
  estimate:
    value: -0.15
    interpretation: |
      15% reduction in respiratory health events overall.

      Equity impact: Larger absolute benefit in populations with higher
      baseline burden. In low-income communities with 15% baseline prevalence,
      intervention reduces to ~13% (2 percentage point reduction).
      In higher-income communities with 8% baseline, reduction to ~7%
      (1 percentage point reduction).

      Result: Disparity narrows from 7pp to 6pp (14% disparity reduction).
```

✗ **Missing:**
```yaml
effect_size:
  estimate:
    value: -0.15
    interpretation: 15% reduction in respiratory events
    # No equity analysis
```

#### 4. Implementation Equity

**Check:** Does the mechanism consider equitable implementation?

✓ **Good:**
```yaml
moderators:
  implementation:
    - factor: enforcement_equity
      effect_direction: positive
      rationale: Code enforcement must prioritize low-income neighborhoods
                 (which have highest rates of violations) to achieve equity goals.
                 Historically, enforcement has been weaker in marginalized communities.

    - factor: tenant_protections
      effect_direction: positive
      rationale: Tenants need protection from rent increases or displacement
                 after remediation. Without protections, intervention may cause harm
                 (gentrification, eviction).

    - factor: language_access
      effect_direction: positive
      rationale: Multilingual outreach and services ensure equitable access
                 for immigrant communities.
```

✗ **Missing:**
```yaml
moderators:
  implementation:
    - factor: implementation_quality
      effect_direction: positive
      rationale: Better implementation is more effective
      # No consideration of who gets quality implementation
```

---

### For Code (Backend/Frontend)

#### 1. Data Model Equity Features

**Check SQLAlchemy models** (`backend/app/models/`):

✓ **Required equity features:**
```python
class Projection(Base):
    """Outcome projection with mandatory equity stratification"""

    # Overall projection
    overall_effect = Column(Float)

    # Stratified projections (required)
    effect_by_race = Column(JSON)  # {"white": -0.10, "black": -0.20, ...}
    effect_by_income = Column(JSON)  # {"q1": -0.25, "q2": -0.18, ...}
    effect_by_geography = Column(JSON)  # {"urban": -0.15, "rural": -0.12}

    # Disparity metrics
    disparity_baseline = Column(Float)
    disparity_post_intervention = Column(Float)
    disparity_reduction_pct = Column(Float)

    # Equity flags
    reduces_disparities = Column(Boolean)
    exacerbates_disparities = Column(Boolean)
    neutral_disparities = Column(Boolean)
```

✗ **Missing equity features:**
```python
class Projection(Base):
    overall_effect = Column(Float)
    # No stratification, no disparity tracking
```

#### 2. API Endpoint Equity

**Check API routes** (`backend/app/api/`):

✓ **Good:**
```python
@router.get("/projections/{projection_id}")
async def get_projection(
    projection_id: int,
    stratify: bool = True,  # Default to stratified view
    equity_analysis: bool = True,  # Include disparity metrics
):
    """Get projection with equity analysis"""

    projection = await get_projection_by_id(projection_id)

    response = {
        "overall_effect": projection.overall_effect,
    }

    if stratify:
        response["stratified"] = {
            "by_race": projection.effect_by_race,
            "by_income": projection.effect_by_income,
            "by_geography": projection.effect_by_geography,
        }

    if equity_analysis:
        response["equity_impact"] = {
            "disparity_baseline": projection.disparity_baseline,
            "disparity_post_intervention": projection.disparity_post_intervention,
            "disparity_reduction_pct": projection.disparity_reduction_pct,
            "reduces_disparities": projection.reduces_disparities,
        }

    return response
```

✗ **Missing:**
```python
@router.get("/projections/{projection_id}")
async def get_projection(projection_id: int):
    projection = await get_projection_by_id(projection_id)
    return {"effect": projection.overall_effect}
    # No stratification option, no equity analysis
```

#### 3. Frontend Visualization Equity

**Check React components** (`frontend/src/`):

✓ **Good:**
```tsx
<ProjectionDashboard>
  {/* Overall effect */}
  <OverallEffect value={projection.overall_effect} />

  {/* Stratified effects - prominent display */}
  <EquitySection>
    <h2>Equity Analysis</h2>

    <StratifiedChart
      data={projection.stratified.by_race}
      title="Effect by Race/Ethnicity"
      baseline={projection.baseline_by_race}
    />

    <StratifiedChart
      data={projection.stratified.by_income}
      title="Effect by Income Quartile"
      baseline={projection.baseline_by_income}
    />

    <DisparityMetrics>
      <Metric
        label="Baseline Disparity"
        value={projection.equity_impact.disparity_baseline}
      />
      <Metric
        label="Post-Intervention Disparity"
        value={projection.equity_impact.disparity_post_intervention}
      />
      <Metric
        label="Disparity Reduction"
        value={projection.equity_impact.disparity_reduction_pct}
        highlight={projection.equity_impact.reduces_disparities}
      />
    </DisparityMetrics>

    {projection.equity_impact.exacerbates_disparities && (
      <Alert severity="warning">
        This intervention may exacerbate existing disparities.
        Consider implementation modifications to ensure equitable access.
      </Alert>
    )}
  </EquitySection>
</ProjectionDashboard>
```

✗ **Missing:**
```tsx
<ProjectionDashboard>
  <h2>Projection Results</h2>
  <div>Effect: {projection.overall_effect}</div>
  {/* No equity visualization */}
</ProjectionDashboard>
```

---

### For Analyses (Bayesian Weighting)

#### 1. Stratified Modeling

**Check PyMC models** (`backend/app/services/bayesian_weighting.py`):

✓ **Required approach:**
```python
import pymc as pm

def build_bayesian_model(mechanisms, context, stratify_by=['race', 'income']):
    """Build Bayesian model with stratification"""

    with pm.Model() as model:
        # Context-specific effect sizes for each stratum
        for stratum in get_strata(context, stratify_by):
            # Base effect size
            base_effect = pm.Normal(f'base_effect_{stratum}', mu=0, sigma=1)

            # Moderator effects (stratum-specific)
            for moderator in mechanisms.moderators:
                if moderator.applies_to_stratum(stratum):
                    mod_effect = pm.Normal(
                        f'moderator_{moderator.name}_{stratum}',
                        mu=moderator.base_value,
                        sigma=moderator.uncertainty
                    )
                    # Weight by stratum-specific factors

            # Stratum-specific projection
            projection[stratum] = base_effect + sum(moderator_effects)

        # Disparity metrics
        disparity_baseline = compute_disparity(baseline_prevalence)
        disparity_post = compute_disparity(projection)
        disparity_reduction = (disparity_baseline - disparity_post) / disparity_baseline

    return model
```

✗ **Non-equity approach:**
```python
def build_bayesian_model(mechanisms, context):
    with pm.Model() as model:
        # Single overall effect
        effect = pm.Normal('effect', mu=0, sigma=1)
        # No stratification
    return model
```

#### 2. Disparity Metrics

**Require calculation of:**

1. **Absolute disparity:** Difference between groups
   ```python
   disparity_abs = max(prevalence_by_group) - min(prevalence_by_group)
   ```

2. **Relative disparity:** Ratio between groups
   ```python
   disparity_rel = max(prevalence_by_group) / min(prevalence_by_group)
   ```

3. **Disparity reduction:**
   ```python
   reduction_pct = (disparity_baseline - disparity_post) / disparity_baseline * 100
   ```

4. **Distributional measures:** Gini coefficient, Theil index, etc.

---

### For Documentation

#### 1. Use Case Equity Analysis

**Every use case should include:**

```markdown
### Use Case: Housing Quality Improvement → Respiratory Health

#### Equity Context

**Baseline Disparities:**
- Asthma prevalence: Black children (16%), White children (7%) - 9pp disparity
- Substandard housing: Low-income (35%), Higher-income (8%) - 27pp disparity
- Root causes: Redlining, segregation, disinvestment, environmental racism

**Differential Effects:**
- Low-income communities: 2pp reduction (15% → 13%)
- Higher-income communities: 1pp reduction (8% → 7%)
- Absolute benefit larger in marginalized communities

**Equity Impact:**
- Disparity reduction: 14% (9pp → 6pp)
- Intervention addresses structural determinant (housing policy)
- Implementation must prioritize under-resourced neighborhoods

**Implementation Equity Considerations:**
- Proactive enforcement in historically marginalized neighborhoods
- Tenant protections to prevent displacement
- Community-controlled oversight
- Language access for immigrant communities

**Equity Verdict:** ✓ Disparity-reducing intervention
```

#### 2. Visualization Guidelines

**Require equity visualizations:**

1. **Stratified bar charts** showing differential effects
2. **Disparity trend lines** (baseline → post-intervention)
3. **Heat maps** showing geographic disparities
4. **Distributional plots** (not just means - show full distribution)

**Examples:**
```
Intervention Effect by Income Quartile
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Q1 (lowest):  ████████████████████ -0.25
Q2:           ██████████████ -0.18
Q3:           ██████████ -0.12
Q4 (highest): ██████ -0.08

→ Larger absolute benefit in lowest-income quartile
→ Disparity-reducing effect
```

---

## Equity Review Process

### Step 1: Baseline Disparity Check

1. **Identify the outcome** being modeled
2. **Check for documented baseline disparities**:
   - By race/ethnicity
   - By income
   - By geography
3. **If missing**: Flag as critical gap, require documentation

### Step 2: Differential Effect Analysis

1. **Check moderators** for equity dimensions
2. **Verify structural framing** (not biological/behavioral)
3. **Assess direction**: Do effects amplify or reduce disparities?

### Step 3: Implementation Equity

1. **Who will receive** the intervention?
2. **Are there barriers** to equitable access?
3. **What safeguards** prevent harm (displacement, stigma, surveillance)?

### Step 4: Quantitative Assessment

1. **Calculate disparity metrics** (if data available)
2. **Classify intervention**:
   - ✓ Disparity-reducing (priority)
   - ≈ Disparity-neutral (assess further)
   - ✗ Disparity-exacerbating (red flag - redesign or reject)

### Step 5: Provide Feedback

**Format:**
```
⚖️ Equity Lens Review
════════════════════════════════════════════════

EQUITY STRENGTHS:
✓ Baseline disparities documented with structural context
✓ Differential effects modeled by race and income
✓ Implementation equity considerations included

EQUITY GAPS:
✗ Missing: Geographic stratification
✗ Missing: Quantified disparity reduction metric
⚠ Concern: No mention of tenant protections (risk of displacement)

EQUITY IMPACT ASSESSMENT:
Direction: Disparity-reducing ✓
Magnitude: Moderate (14% disparity reduction)
Implementation risk: Medium (without tenant protections)

RECOMMENDATIONS:
1. Add geographic moderator (urban/rural, regional policy variation)
2. Calculate and report disparity reduction percentage
3. Add implementation moderator: tenant_protections
4. Specify enforcement must prioritize under-resourced areas

EQUITY VERDICT: ✓ APPROVED with recommendations
```

---

## Common Equity Issues

### Issue 1: "Colorblind" Analysis

**Problem:** No mention of race/ethnicity
**Fix:** Explicitly model racialized exposures due to structural racism

### Issue 2: Biological Race

**Problem:** Attributing disparities to genetics or biology
**Fix:** Always frame in terms of structural racism, racialized exposures, discriminatory policies

### Issue 3: "Rising Tide Lifts All Boats"

**Problem:** Assuming overall benefit means equitable benefit
**Fix:** Stratify and calculate disparities - overall benefit can mask increasing inequality

### Issue 4: Implementation Blind Spots

**Problem:** No consideration of who gets access to intervention
**Fix:** Specify implementation equity (targeting, outreach, barrier reduction)

### Issue 5: Harm Potential

**Problem:** No assessment of unintended harms (displacement, surveillance, stigma)
**Fix:** Explicit harm analysis, especially for marginalized communities

---

## Equity-Centered Language

**Use:**
- "Structural racism"
- "Economic inequality"
- "Racialized exposures"
- "Historical disinvestment"
- "Discriminatory policies"
- "Marginalized communities"
- "Disparity reduction"

**Avoid:**
- "Minority" (use specific racial/ethnic groups)
- "Vulnerable populations" (suggests inherent vulnerability, not structural)
- "At-risk" (without structural context)
- "Cultural factors" (without structural explanation)
- "Health disparities" alone (always specify root causes)

---

## Integration with Other Skills

- **Structural Competency**: Equity and structural competency are intertwined - both focus on systems
- **Mechanism Discovery**: Apply equity lens during literature synthesis
- **Documentation**: Ensure all docs include equity analysis

---

## Output Requirements

Every equity review should provide:
1. **Baseline disparity documentation**: Who is most affected and why (structural reasons)
2. **Differential effect analysis**: Stratified projections by equity dimensions
3. **Disparity impact**: Quantified reduction/neutrality/exacerbation
4. **Implementation equity**: Access, barriers, safeguards
5. **Verdict**: Disparity-reducing / neutral / exacerbating
6. **Recommendations**: Specific improvements to enhance equity

---

## Success Criteria

An equity-centered mechanism/analysis should:
- ✓ Document baseline disparities with structural context
- ✓ Model differential effects by race, income, geography
- ✓ Calculate disparity reduction metrics
- ✓ Include implementation equity moderators
- ✓ Assess harm potential for marginalized communities
- ✓ Prioritize disparity-reducing interventions
- ✓ Use equity-centered language throughout
