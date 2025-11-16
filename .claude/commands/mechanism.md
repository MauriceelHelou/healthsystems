# Mechanism Bank Management Command

You are assisting with the HealthSystems Platform mechanism bank - a version-controlled database of causal mechanisms linking structural interventions to health outcomes.

## Context

The mechanism bank stores YAML files in `mechanism-bank/mechanisms/` following a strict JSON schema defined in `mechanism-bank/schema/mechanism-schema.json`. Each mechanism represents a causal pathway with:
- Evidence-based effect sizes
- Context-specific moderators (policy, demographic, geographic, implementation)
- Chicago-style citations
- Quality ratings (A/B/C tiers)
- Version control via git

## Command Argument Parsing

Parse the user's command to determine the sub-command:

- **`/mechanism create [intervention] -> [outcome]`** - Create new mechanism (AI-assisted wizard)
- **`/mechanism validate [file]`** - Validate mechanism against schema
- **`/mechanism search <query>`** - Search mechanism bank
- **`/mechanism version <file>`** - Bump version and commit
- **`/mechanism lineage <id>`** - Show version history

If no sub-command is provided, show available commands.

---

## Sub-Command: CREATE

**Purpose:** Interactive wizard to create a properly formatted mechanism YAML file.

### Steps:

1. **Parse intervention and outcome** from command (e.g., `/mechanism create housing quality -> respiratory health`)

2. **Search existing mechanisms** to avoid duplicates:
   - Use Grep to search mechanism-bank/mechanisms/ for similar interventions/outcomes
   - If found, ask user if they want to add a variant or update existing

3. **Literature search** (if MCP server available):
   - Search academic literature for effect sizes
   - Look for meta-analyses, systematic reviews, RCTs
   - Extract: effect size, confidence interval, sample size, population
   - Present top 5 results to user for selection

4. **Gather mechanism details interactively:**
   - Mechanism ID (suggest: `intervention_outcome_v1`)
   - Scale level (structural/institutional/individual)
   - Intervention details (type, target population, typical implementation)
   - Outcome details (measurement, timeframe)
   - Effect size specification:
     - Point estimate (suggest from literature if available)
     - Uncertainty (95% CI or SE)
     - Functional form (linear/log/threshold/dose-response)
   - Moderators:
     - Policy environment factors
     - Demographic factors (race, income, age, etc.)
     - Geographic factors
     - Implementation quality factors
   - Evidence quality (A/B/C tier)
   - Citations (Chicago style - assist with formatting if DOI provided)

5. **Generate YAML file**:
   - Follow exact schema structure
   - Use proper indentation (2 spaces)
   - Include all required fields
   - Add helpful comments

6. **Validate against schema**:
   - Run: `python mechanism-bank/scripts/validate_mechanisms.py <file>`
   - If errors, fix and re-validate

7. **Review checklist**:
   - Effect size plausibility (compare to literature)
   - Citation completeness
   - Moderator justification
   - Structural competency alignment (not victim-blaming)
   - Equity considerations (population-specific effects)

8. **Git commit**:
   - Add file: `git add mechanism-bank/mechanisms/<file>`
   - Commit: `git commit -m "mechanism: add <intervention> -> <outcome> (v1)"`

### Example Output:

```yaml
id: housing_quality_respiratory_v1
version: 1.0
metadata:
  created_date: 2025-11-16
  last_updated: 2025-11-16
  created_by: [User Name]
  status: active

mechanism:
  name: Housing Quality Improvement → Respiratory Health Outcomes
  description: |
    Structural improvements to housing (remediation of mold, improved ventilation,
    reduced dampness) reduce respiratory health burdens, particularly asthma
    exacerbations and respiratory infections.

  scale: institutional

  intervention:
    type: housing_quality_improvement
    description: Remediation of substandard housing conditions
    target_population: Low-income households in substandard housing
    typical_implementation: Housing code enforcement, rehabilitation subsidies

  outcome:
    type: respiratory_health
    measurement: Asthma exacerbation rate, respiratory infection incidence
    timeframe: 6-12 months post-intervention

effect_size:
  estimate:
    value: -0.15
    unit: log_rate_ratio
    interpretation: 15% reduction in respiratory health events

  uncertainty:
    ci_lower: -0.25
    ci_upper: -0.05
    confidence_level: 0.95

  functional_form: linear

moderators:
  policy_environment:
    - factor: housing_code_enforcement_strength
      effect_direction: positive
      rationale: Stronger enforcement → greater compliance → larger effects

  demographic:
    - factor: child_presence
      effect_direction: positive
      rationale: Children spend more time at home, greater exposure

    - factor: baseline_asthma_prevalence
      effect_direction: positive
      rationale: Larger effect in populations with higher baseline burden

  geographic:
    - factor: climate_humidity
      effect_direction: positive
      rationale: Mold growth more prevalent in humid climates

  implementation:
    - factor: remediation_quality
      effect_direction: positive
      rationale: Comprehensive remediation more effective than partial

evidence:
  quality_tier: A

  citations:
    - citation: |
        Sandel, Megan, et al. "Housing Interventions and Control of Asthma-Related
        Indoor Biologic Agents: A Review of the Evidence." Journal of Public Health
        Management and Practice 16, no. 5 (2010): S11-S20.
      doi: 10.1097/PHH.0b013e3181ddcbd9
      study_type: systematic_review

    - citation: |
        Krieger, James, et al. "Housing and Health: Time Again for Public Health Action."
        American Journal of Public Health 92, no. 5 (2002): 758-768.
      doi: 10.2105/AJPH.92.5.758
      study_type: review

  effect_size_derivation: |
    Pooled estimate from Sandel et al. (2010) systematic review of housing
    intervention RCTs. Original studies show 10-20% reduction in asthma symptoms;
    15% (-0.15 log rate ratio) represents central tendency.

notes: |
  This mechanism represents structural intervention (housing policy) rather than
  individual behavior change. Focus on policy levers: code enforcement, rehabilitation
  funding, tenant protections.

  Equity consideration: Low-income households and communities of color disproportionately
  experience substandard housing. This intervention addresses structural determinant.
```

---

## Sub-Command: VALIDATE

**Purpose:** Run validation scripts on mechanism YAML files.

### Steps:

1. **Determine target**:
   - If file specified: validate that file
   - If no file: validate all mechanisms in mechanism-bank/mechanisms/

2. **Run validation**:
   ```bash
   python mechanism-bank/scripts/validate_mechanisms.py [file]
   ```

3. **Parse output**:
   - Report any schema violations
   - Check for required fields
   - Validate value types and ranges
   - Check citation formatting

4. **Suggest fixes** if validation fails

---

## Sub-Command: SEARCH

**Purpose:** Search mechanism bank by keywords, interventions, outcomes, or moderators.

### Steps:

1. **Parse query** to identify search intent:
   - Intervention type (e.g., "housing", "labor", "food access")
   - Outcome type (e.g., "mental health", "cardiovascular", "mortality")
   - Moderator factors (e.g., "race", "income", "policy")
   - Scale level (structural/institutional/individual)

2. **Multi-strategy search**:
   - **Keyword search**: Grep for query terms in YAML files
   - **Semantic search**: Look for related terms (e.g., "housing" → "residential", "dwelling")
   - **Tag search**: Search by intervention_type, outcome_type fields

3. **Read matching files** and extract key info:
   - Mechanism name
   - Effect size
   - Quality tier
   - Key moderators

4. **Present results** in formatted table:
   ```
   Found 3 mechanisms matching "housing":

   1. housing_quality_respiratory_v1 [A tier]
      Housing Quality → Respiratory Health
      Effect: -0.15 (CI: -0.25, -0.05)
      File: mechanism-bank/mechanisms/housing_quality_respiratory_v1.yaml

   2. housing_stability_mental_health_v1 [B tier]
      Housing Stability → Mental Health
      Effect: -0.22 (CI: -0.35, -0.09)
      File: mechanism-bank/mechanisms/housing_stability_mental_health_v1.yaml
   ```

---

## Sub-Command: VERSION

**Purpose:** Bump mechanism version and commit to git.

### Steps:

1. **Read current mechanism file**

2. **Parse current version** (e.g., 1.0 → 1.1 for minor, 1.0 → 2.0 for major)

3. **Ask user**: Minor update (evidence refinement) or Major update (effect size change)?

4. **Update file**:
   - Increment version number
   - Update last_updated date
   - Ask for change notes

5. **Validate** updated file

6. **Git commit**:
   ```bash
   git add mechanism-bank/mechanisms/<file>
   git commit -m "mechanism: update <name> v<old> -> v<new> - <change summary>"
   ```

---

## Sub-Command: LINEAGE

**Purpose:** Show full version history and provenance of a mechanism.

### Steps:

1. **Find mechanism file** by ID

2. **Git log** for that file:
   ```bash
   git log --follow --pretty=format:"%h %ad %s" --date=short -- mechanism-bank/mechanisms/<file>
   ```

3. **Show version history**:
   - All versions
   - Dates of changes
   - Commit messages
   - Who made changes

4. **Show citations** from current version (evidence provenance)

5. **Visualize lineage** if multiple variants exist (e.g., v1 → v2, v1 → v1_rural)

---

## Error Handling

- If mechanism-bank/ directory not found: explain project structure
- If schema validation fails: show specific errors with line numbers
- If git operations fail: suggest checking git status
- If MCP server unavailable: skip literature search, allow manual entry

---

## Integration with Other Tools

- **After creation**: Suggest running `/test-stack mechanisms` to validate
- **After updates**: Suggest running `/docs-sync` to update mechanism catalog
- **Reference structural competency**: Remind user to check alignment with framework

---

## Notes

- Always validate against schema before committing
- Maintain Chicago-style citations
- Version control is critical for reproducibility
- Focus on structural interventions, not individual behavior
- Consider equity implications (population-specific effects)
