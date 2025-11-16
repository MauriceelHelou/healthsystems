# Mechanism Bank

The Mechanism Bank is a versioned database of causal pathways linking structural interventions to health outcomes. Each mechanism includes:

- Effect sizes with confidence intervals
- Evidence quality ratings
- Academic citations (Chicago style)
- Contextual moderators
- Validation history

## Directory Structure

```
mechanism-bank/
├── schemas/           # JSON schemas for validation
├── mechanisms/        # Individual mechanism files (YAML)
│   ├── built_environment/
│   ├── social_environment/
│   ├── economic/
│   ├── political/
│   └── biological/
├── evidence/          # Supporting literature, meta-analyses
├── validation/        # Validation scripts and tests
└── CHANGELOG.md       # Version history of mechanism updates
```

## Mechanism File Format

Each mechanism is stored as a YAML file with the following structure:

```yaml
id: mechanism_unique_id
name: Intervention → Intermediate → Outcome
category: built_environment | social_environment | economic | political | biological
mechanism_type: biological | psychological | social | environmental
effect_size:
  measure: odds_ratio | relative_risk | standardized_mean_difference | etc.
  point_estimate: 1.45
  confidence_interval: [1.22, 1.73]
  unit: per standard deviation improvement
evidence:
  quality_rating: A | B | C
  n_studies: 8
  citation: |
    Author, First Last. Year. "Title of Article." *Journal Name*
    Volume (Issue): Pages. https://doi.org/xxx
last_updated: YYYY-MM-DD
version: 1.0
validated_by: [initials]
description: |
  Detailed description of the causal pathway
assumptions:
  - Assumption 1
  - Assumption 2
limitations:
  - Limitation 1
  - Limitation 2
moderators:
  - name: poverty_rate
    direction: positive
    strength: moderate
```

## Evidence Quality Ratings

- **A**: Meta-analysis or multiple high-quality RCTs/longitudinal studies
- **B**: Single high-quality study or multiple moderate-quality studies
- **C**: Limited evidence, expert consensus, or theoretical basis

## Adding New Mechanisms

1. Create a new YAML file in the appropriate category directory
2. Follow the schema defined in `schemas/mechanism_schema.json`
3. Include minimum 3 peer-reviewed studies (or 1 meta-analysis) for rating A/B
4. Use Chicago-style citations
5. Run validation: `python validation/validate_mechanisms.py`
6. Submit for expert review
7. Update `CHANGELOG.md`

## Validation

```bash
# Validate all mechanisms
python validation/validate_mechanisms.py

# Validate specific mechanism
python validation/validate_mechanisms.py --file mechanisms/built_environment/housing_quality_respiratory.yml

# Check citations
python validation/check_citations.py
```

## Versioning

- Mechanisms use semantic versioning: MAJOR.MINOR
- **MAJOR** bump: Change in effect direction or magnitude > 20%
- **MINOR** bump: New evidence, updated CI, or refined moderators
- All changes documented in mechanism file `last_updated` and bank `CHANGELOG.md`

## Usage in Platform

The mechanism bank is read-only in production. Modifications go through:

1. Local testing and validation
2. Peer review by domain experts
3. Statistical review
4. Deployment to production

## License

Mechanism bank data is licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
