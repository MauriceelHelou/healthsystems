# Mechanism Discovery Skill

You are conducting literature synthesis to discover and formalize causal mechanisms for the HealthSystems Platform mechanism bank.

## Objective

Transform academic literature into structured, version-controlled mechanism YAML files that link structural interventions to health outcomes with quantified effect sizes.

## Workflow

### 1. Literature Search

**Use MCP servers** to search academic databases:

1. **Initial broad search**:
   - Query Semantic Scholar: `[intervention type] AND [outcome type] AND (meta-analysis OR systematic review OR RCT)`
   - Example: `housing quality improvement AND respiratory health AND (meta-analysis OR systematic review)`

2. **Refine search** based on results:
   - Filter by publication date (prefer recent)
   - Filter by study type (prefer meta-analyses, systematic reviews)
   - Filter by population (prefer structural interventions, not individual behavior)

3. **Extract candidate papers**:
   - Get DOI, title, authors, year
   - Get abstract
   - Get study type
   - Get sample size if available

4. **Present to user** for selection:
   ```
   📚 Found 15 relevant papers:

   [1] Sandel et al. (2010) - Meta-analysis - 12 RCTs
       "Housing Interventions and Control of Asthma-Related Indoor Biologic Agents"
       DOI: 10.1097/PHH.0b013e3181ddcbd9
       Effect: 15% reduction in asthma symptoms (pooled OR: 0.85, 95% CI: 0.75-0.95)

   [2] Krieger et al. (2002) - Systematic review - 18 studies
       "Housing and Health: Time Again for Public Health Action"
       DOI: 10.2105/AJPH.92.5.758
       Effect: Variable, multiple pathways identified

   [3] Thomson et al. (2013) - Cochrane review - 8 RCTs
       "Housing improvements for health and associated socio-economic outcomes"
       DOI: 10.1002/14651858.CD008657.pub2
       Effect: Moderate evidence for respiratory health improvement

   Select papers to include (e.g., "1,3"): _
   ```

### 2. Effect Size Extraction

For each selected paper:

1. **Read abstract and methods** (via MCP fetch if full-text available)

2. **Extract statistical information**:
   - Effect size measure (OR, RR, Cohen's d, correlation, mean difference)
   - Point estimate
   - Confidence interval (95% preferred)
   - Sample size
   - Population characteristics
   - Follow-up duration

3. **Convert to common metric** (log ratio for health outcomes):
   - Odds ratio → log(OR)
   - Risk ratio → log(RR)
   - Rate ratio → log(RR)
   - Cohen's d → correlation → log(OR) approximation
   - Note: Use standard conversions, document in `effect_size_derivation`

4. **Meta-analysis** (if multiple studies selected):
   - Pool effect sizes using inverse-variance weighting
   - Calculate pooled CI
   - Assess heterogeneity (I² statistic if reported)
   - Note: For initial mechanism, simple pooling is acceptable; sophisticated meta-analysis can be Phase 2

5. **Document uncertainty**:
   - If only one study: Use reported CI
   - If multiple studies: Use pooled CI
   - If CI not available: Estimate from p-value or SE
   - If no uncertainty available: Flag as limitation

### 3. Moderator Identification

Analyze the literature for factors that modify effect size:

1. **Policy environment moderators**:
   - Enforcement strength (weak vs. strong code enforcement)
   - Funding availability (subsidies, vouchers)
   - Legal protections (tenant rights, anti-discrimination)
   - Examples from papers: "Effects stronger in cities with rigorous enforcement"

2. **Demographic moderators**:
   - Age (children, elderly)
   - Race/ethnicity (structural racism, environmental justice)
   - Income (low-income more affected)
   - Pre-existing conditions (baseline health status)
   - Examples: "Larger effects in households with children"

3. **Geographic moderators**:
   - Climate (humidity, temperature)
   - Urban vs. rural
   - Region (policy variation)
   - Environmental exposures (air quality, pollution)
   - Examples: "Greater impact in humid climates due to mold"

4. **Implementation moderators**:
   - Intervention intensity (comprehensive vs. partial)
   - Quality/fidelity
   - Duration
   - Examples: "Complete remediation more effective than partial"

5. **For each moderator, document**:
   - Factor name
   - Effect direction (positive = amplifies effect, negative = dampens effect)
   - Rationale with citation

### 4. Intervention & Outcome Specification

**Intervention details**:
- Type (structured taxonomy: housing_quality, labor_standards, food_access, etc.)
- Description (clear, specific)
- Target population (who receives intervention)
- Typical implementation (how it's delivered in practice)
- Scale: structural (federal/state policy), institutional (local/organizational), individual

**Outcome details**:
- Type (structured taxonomy: respiratory_health, mental_health, cardiovascular, etc.)
- Measurement (specific metrics)
- Timeframe (when effects are observed)

**Ensure structural competency**:
- Focus on structural/institutional interventions (not individual behavior)
- Frame intervention as addressing systems/policies, not personal choices
- Avoid victim-blaming language

### 5. Evidence Quality Assessment

Assign quality tier (A/B/C):

**A-tier:**
- Meta-analysis or systematic review with ≥5 studies
- Clear effect size with narrow CI
- Low heterogeneity
- High-quality individual studies (RCTs, large cohorts)
- Consistent findings across studies

**B-tier:**
- Systematic review with <5 studies
- Single large, well-designed study (RCT, cohort)
- Moderate heterogeneity
- Reasonable effect size precision

**C-tier:**
- Single small study
- Observational study with limitations
- Wide CI or high uncertainty
- Inconsistent findings
- Preliminary evidence

Document rationale for tier assignment.

### 6. Citation Formatting

Format all citations in Chicago style:

**Format:**
```
Last name, First name, et al. "Article Title." Journal Name Volume, no. Issue (Year): Pages.
```

**Examples:**
```
Sandel, Megan, et al. "Housing Interventions and Control of Asthma-Related Indoor Biologic Agents: A Review of the Evidence." Journal of Public Health Management and Practice 16, no. 5 (2010): S11-S20.
```

Include DOI when available:
```
doi: 10.1097/PHH.0b013e3181ddcbd9
```

Classify study type:
- `meta_analysis`
- `systematic_review`
- `randomized_controlled_trial`
- `cohort_study`
- `case_control_study`
- `cross_sectional_study`
- `review`

### 7. YAML Generation

Generate mechanism file following schema exactly:

```yaml
id: [intervention]_[outcome]_v1
version: 1.0
metadata:
  created_date: [YYYY-MM-DD]
  last_updated: [YYYY-MM-DD]
  created_by: [name or "LLM-assisted synthesis"]
  status: active

mechanism:
  name: [Intervention] → [Outcome]
  description: |
    [2-3 sentence description of causal pathway]

  scale: [structural | institutional | individual]

  intervention:
    type: [taxonomy_term]
    description: [detailed description]
    target_population: [who receives intervention]
    typical_implementation: [how it's delivered]

  outcome:
    type: [taxonomy_term]
    measurement: [specific metrics]
    timeframe: [when effects observed]

effect_size:
  estimate:
    value: [numeric]
    unit: [log_rate_ratio | log_odds_ratio | correlation | standardized_mean_difference]
    interpretation: [plain language explanation]

  uncertainty:
    ci_lower: [numeric]
    ci_upper: [numeric]
    confidence_level: [0.95 typical]

  functional_form: [linear | log | threshold | dose_response]

moderators:
  policy_environment:
    - factor: [factor_name]
      effect_direction: [positive | negative]
      rationale: [explanation with citation]

  demographic:
    - factor: [factor_name]
      effect_direction: [positive | negative]
      rationale: [explanation with citation]

  geographic:
    - factor: [factor_name]
      effect_direction: [positive | negative]
      rationale: [explanation with citation]

  implementation:
    - factor: [factor_name]
      effect_direction: [positive | negative]
      rationale: [explanation with citation]

evidence:
  quality_tier: [A | B | C]

  citations:
    - citation: |
        [Chicago-style citation]
      doi: [DOI if available]
      study_type: [taxonomy_term]

  effect_size_derivation: |
    [Detailed explanation of how effect size was calculated,
     including any conversions, pooling methods, or approximations]

notes: |
  [Additional context, caveats, equity considerations,
   structural competency notes, future research needs]
```

### 8. Validation & Review

1. **Schema validation**:
   ```bash
   python mechanism-bank/scripts/validate_mechanisms.py [file]
   ```
   Fix any schema errors.

2. **Plausibility checks**:
   - Effect sizes in reasonable range (-5 to 5 for log ratios, -1 to 1 for correlations)
   - CI makes sense (lower < upper, contains point estimate)
   - Moderators have clear rationale
   - Citations properly formatted

3. **Structural competency review**:
   - Does mechanism focus on structural/institutional change?
   - Are moderators framed structurally (policy, resources) not individually (behavior)?
   - Does description avoid victim-blaming?
   - Are equity considerations explicit?

4. **Expert review checklist** (present to user):
   ```
   ✓ Effect size plausible given literature
   ✓ Uncertainty appropriately quantified
   ✓ Moderators have strong rationale
   ✓ Citations complete and accurate
   ✓ Structural competency alignment
   ✓ Equity considerations addressed
   ✓ Functional form appropriate
   ✓ Schema validation passed

   Ready to commit? (y/n)
   ```

### 9. Version Control

1. **Save YAML file**:
   - Path: `mechanism-bank/mechanisms/[id].yaml`
   - Naming: Use mechanism ID as filename

2. **Git commit**:
   ```bash
   git add mechanism-bank/mechanisms/[id].yaml
   git commit -m "mechanism: add [intervention] → [outcome] (v1)

   - Effect size: [value] ([CI])
   - Quality tier: [A/B/C]
   - Sources: [N] papers ([study types])
   - LLM-assisted synthesis from [database] search

   Co-Authored-By: Claude <noreply@anthropic.com>"
   ```

3. **Update mechanism catalog**:
   - Suggest running `/docs-sync mechanisms`

---

## Special Cases

### No Effect Sizes Available

If literature has qualitative findings but no quantified effect sizes:
1. Flag as C-tier
2. Estimate plausible range based on similar mechanisms
3. Document limitation clearly in `effect_size_derivation`
4. Note need for future quantification

### Conflicting Evidence

If studies show conflicting results:
1. Document heterogeneity
2. Use conservative (smaller) effect size
3. Widen confidence interval to reflect uncertainty
4. Lower quality tier (B or C)
5. Note conflict in `notes` section

### Mechanism Variants

If evidence suggests context-specific mechanisms (e.g., rural vs. urban):
1. Create base mechanism (v1)
2. Suggest creating variants (v1_rural, v1_urban) with different effect sizes
3. Document relationship in `notes`

---

## Output to User

At each stage, provide clear summaries:

1. **After literature search**: Table of papers with effect sizes
2. **After extraction**: Summary of pooled effect size
3. **After moderator identification**: List of moderators with rationale
4. **Before generation**: Preview of key mechanism details
5. **After validation**: Checklist of quality checks
6. **After commit**: Confirmation with file path and next steps

---

## Integration with /mechanism Command

This skill is designed to work with `/mechanism create`. The command handles:
- User interaction
- File I/O
- Git operations
- Validation scripts

This skill provides:
- Literature search strategy
- Effect size extraction logic
- Moderator identification framework
- Quality assessment criteria
- YAML structure guidance

---

## Equity & Structural Competency

Throughout the process, maintain focus on:

1. **Structural interventions**: Policy, institutional, environmental changes (not individual behavior)
2. **Equity lens**: Explicitly identify differential effects by race, income, geography
3. **Power & resources**: Frame moderators in terms of structural factors (enforcement, funding) not individual factors (compliance, motivation)
4. **Avoid harm**: Do not create mechanisms that could be used to justify victim-blaming or punitive policies

If a proposed mechanism doesn't align with structural competency principles, explain why and suggest reframing or declining to add it.
