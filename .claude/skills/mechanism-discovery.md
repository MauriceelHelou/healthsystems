# Mechanism Discovery Skill

You are conducting automated literature synthesis to discover and formalize causal mechanisms for the HealthSystems Platform mechanism bank.

> **Full Documentation**: See `docs/LLM & Discovery Pipeline/MECHANISM_DISCOVERY_PIPELINE.md` for complete technical details.

## Pipeline Overview

```
Topic Query → Literature Search → LLM Extraction → Quantitative Effects → Validation → YAML Output
```

## Key Components

| Component | Implementation | Purpose |
|-----------|----------------|---------|
| Literature Search | `backend/pipelines/literature_search.py` | Semantic Scholar + PubMed APIs |
| LLM Extraction | `backend/pipelines/llm_mechanism_discovery.py` | Claude mechanism extraction |
| Full Pipeline | `backend/pipelines/end_to_end_discovery.py` | End-to-end workflow |
| Citation Validation | `backend/utils/citation_validation.py` | Crossref DOI verification |
| Schema Validation | `backend/scripts/validate_mechanism_schema.py` | Schema compliance |
| Schema Config | `backend/config/schema_config.py` | Centralized constants |

## Quick Start

### Option 1: Full Pipeline (Recommended)

```python
from backend.pipelines.end_to_end_discovery import EndToEndDiscoveryPipeline

pipeline = EndToEndDiscoveryPipeline(pubmed_email="your@email.com")

mechanisms = pipeline.discover_mechanisms_for_topic(
    topic_query="food insecurity diabetes chronic disease",
    max_papers=10,
    year_range=(2015, 2024),
    min_citations=10,
    focus_area="economic determinants of health"
)

pipeline.save_mechanisms()
pipeline.print_summary()
```

### Option 2: Step-by-Step

```python
# Step 1: Literature Search
from backend.pipelines.literature_search import LiteratureSearchAggregator

aggregator = LiteratureSearchAggregator(pubmed_email="your@email.com")
papers = aggregator.search(
    query="housing quality respiratory health meta-analysis",
    limit_per_source=15,
    year_range=(2015, 2024),
    min_citations=5
)

# Step 2: LLM Extraction
from backend.pipelines.llm_mechanism_discovery import LLMMechanismDiscovery

discovery = LLMMechanismDiscovery()
for paper in papers:
    mechanisms = discovery.extract_mechanisms_from_paper(
        paper_abstract=paper.abstract,
        paper_title=paper.title,
        paper_doi=paper.doi,
        paper_citation=paper.citation,
        focus_area="housing to health"
    )
```

## Search Query Best Practices

**Good Queries**:
```
housing quality respiratory health asthma
eviction housing displacement emergency department
food insecurity diabetes chronic disease meta-analysis
medicaid expansion health outcomes mortality
community health workers healthcare access
incarceration criminal legal system chronic disease
```

**Bad Queries** (avoid):
```
# Too broad
health outcomes

# Too narrow
specific-author-name-2022-study

# Full sentences (use keywords instead)
"What is the relationship between housing and health?"
```

## Quantitative Effect Extraction

**CRITICAL**: All mechanisms should include quantitative effects when available.

### Effect Size Types

| Type | Use Case | Example |
|------|----------|---------|
| `odds_ratio` | Case-control studies | OR 3.29 (CI: 2.46-4.40) |
| `relative_risk` | Cohort studies | RR 1.45 (CI: 1.20-1.75) |
| `hazard_ratio` | Survival analysis | HR 2.14 (CI: 1.25-3.67) |
| `percentage_change` | Continuous outcomes | -0.47% A1C reduction |
| `incidence_rate_ratio` | Rate comparisons | IRR 1.30 (CI: 1.17-1.46) |
| `standardized_mean_difference` | Cohen's d | d = 0.52 |
| `beta_coefficient` | Regression | β = -0.15 |

### YAML Format

```yaml
quantitative_effects:
  effect_size:
    value: 3.29
    type: odds_ratio
    ci_lower: 2.46
    ci_upper: 4.40
    ci_level: 95
  sample_size: 1953636
  heterogeneity_i_squared: 82.5
  interpretation: "Food insecurity increases odds of psychological distress by 229%"
```

## Evidence Quality Grades

| Grade | Criteria | Study Count |
|-------|----------|-------------|
| **A** | Meta-analysis or systematic review with 5+ high-quality studies | 5-100 |
| **B** | 3-4 studies or systematic review with moderate evidence | 3-10 |
| **C** | 1-2 studies or limited/emerging evidence | 1-4 |

**IMPORTANT**: Grade D does not exist. All mechanisms require at least C-level evidence.

## Valid Categories

- `built_environment` - Housing, air quality, transportation infrastructure
- `social_environment` - Social support, community cohesion, family dynamics
- `economic` - Income, employment, food security, financial strain
- `political` - Policy, legislation, regulation, political participation
- `biological` - Physiological pathways, genetics, biomarkers
- `behavioral` - Health behaviors (MUST have structural context)
- `healthcare_access` - Insurance, providers, services, geographic access

## Structural Competency Guidelines

### Good Mechanisms (Structural Focus)

```yaml
# Policy → Outcomes
from_node: medicaid_expansion_policy
to_node: healthcare_access
mechanism_pathway:
  - "State-level policy decision expands eligibility"
  - "More residents qualify for coverage"
  - "Insurance removes financial barrier to care"

# Economic Systems → Health
from_node: food_insecurity
to_node: diabetes_outcomes
mechanism_pathway:
  - "Household food insecurity forces trade-offs between food and medications"
  - "Limited budgets result in calorie-dense but nutrient-poor foods"
  - "Chronic stress from food uncertainty elevates cortisol"
  - "Poor glycemic control leads to diabetes complications"
```

### Bad Mechanisms (Individual Blame) - AVOID

```yaml
# ❌ Blames individual behavior
from_node: health_literacy
to_node: medication_adherence
# Missing: educational inequality, healthcare system complexity

# ❌ Victim-blaming framing
from_node: patient_compliance
to_node: health_outcomes
# Missing: systemic barriers to care

# ❌ Individual behavior focus without structural context
from_node: exercise_behavior
to_node: obesity
# Missing: built environment, food access, time poverty
```

## Full YAML Output Schema

```yaml
id: from_node_to_node
name: Source Node → Target Node
from_node:
  node_id: snake_case_id
  node_name: Human Readable Name
  node_type: stock | proxy_index | crisis_endpoint
to_node:
  node_id: snake_case_id
  node_name: Human Readable Name
  node_type: stock | proxy_index | crisis_endpoint
direction: positive | negative
category: built_environment | social_environment | economic | political | biological | behavioral | healthcare_access
mechanism_pathway:
  - "Step 1: Initial cause leads to intermediate effect"
  - "Step 2: Intermediate effect produces downstream change"
  - "Step 3: Downstream change results in final outcome"
evidence:
  quality_rating: A | B | C
  n_studies: <number>
  primary_citation: "Chicago-style citation"
  supporting_citations:
    - "Additional citation 1"
    - "Additional citation 2"
  doi: "10.xxxx/xxxxx"
  journal: "Journal Name"
  year: 2024
  fulltext:
    available: true | false
    source: pubmed_central | doi | other
    url: "URL if available"
    is_open_access: true | false
  citation_verified: true | false
quantitative_effects:
  effect_size:
    value: <number>
    type: odds_ratio | relative_risk | hazard_ratio | percentage_change | incidence_rate_ratio | standardized_mean_difference | beta_coefficient
    ci_lower: <number>
    ci_upper: <number>
    ci_level: 95
  sample_size: <number>
  heterogeneity_i_squared: <number or null>
  interpretation: "Plain language interpretation"
last_updated: "YYYY-MM-DD"
version: "1.0"
description: "Detailed mechanism description"
moderators:
  - name: moderator_name
    direction: strengthens | weakens
    strength: weak | moderate | strong
    description: "How this moderator affects the mechanism"
structural_competency:
  root_cause_level: policy | economic_system | spatial_arrangement | institutional | interpersonal
  avoids_victim_blaming: true
  equity_implications: "Description of equity considerations"
assumptions:
  - "Key assumption 1"
  - "Key assumption 2"
limitations:
  - "Limitation 1"
  - "Limitation 2"
spatial_variation:
  varies_by_geography: true | false
  variation_notes: "Description of geographic variation"
  relevant_geographies:
    - "Geography 1 with specific pattern"
    - "Geography 2 with different pattern"
llm_metadata:
  extracted_by: claude-opus-4-5-20251101
  extraction_date: "YYYY-MM-DDTHH:MM:SS"
  extraction_confidence: high | medium | low
  prompt_version: "1.0-mvp"
```

## Validation

### Automated Schema Validation

```bash
cd mechanism-bank
python ../backend/scripts/validate_mechanism_schema.py
```

### Citation Validation

```python
from backend.utils.citation_validation import CitationValidator

validator = CitationValidator()
is_valid, metadata = validator.verify_doi("10.1186/s40795-024-00922-1")
citation = validator.format_chicago_citation(metadata)
```

### Quantitative Effect Verification

For high-stakes mechanisms, verify effects independently:
1. Look up the DOI via Crossref or PubMed
2. Fetch the source paper abstract/full text
3. Confirm effect size matches reported values
4. Check CI bounds and sample size accuracy

## Environment Variables

```bash
# Required
export ANTHROPIC_API_KEY="your_api_key_here"

# Optional (higher Semantic Scholar rate limits)
export SEMANTIC_SCHOLAR_API_KEY="your_key_here"

# Recommended (NCBI best practice)
export PUBMED_EMAIL="your_email@example.com"
```

## Batch Discovery Example

```python
topics = [
    ("housing quality respiratory health", "built_environment"),
    ("eviction health emergency department", "economic"),
    ("food insecurity diabetes", "economic"),
    ("incarceration chronic disease", "social_environment"),
    ("adverse childhood experiences adult health", "social_environment"),
    ("transportation barriers healthcare", "healthcare_access"),
    ("unemployment health outcomes", "economic"),
    ("medicaid expansion health", "political"),
]

all_mechanisms = []
for query, category in topics:
    mechanisms = pipeline.discover_mechanisms_for_topic(
        topic_query=query,
        max_papers=10,
        focus_area=category
    )
    all_mechanisms.extend(mechanisms)

pipeline.discovered_mechanisms = all_mechanisms
pipeline.save_mechanisms()
```

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| No papers found | Query too specific | Use keywords, widen year range |
| Error extracting | API key missing | Check `$ANTHROPIC_API_KEY` |
| Schema validation failed | Missing fields | Run validation to see errors |
| Low-quality extractions | Low-impact papers | Increase `min_citations` |
| Missing quantitative effects | Abstract lacks data | Search for meta-analyses |

## Output Locations

```
mechanism-bank/mechanisms/
├── built_environment/      # Housing, air quality, transportation
├── social_environment/     # Social support, community, family
├── economic/               # Income, employment, food security
├── political/              # Policy, legislation, regulation
├── biological/             # Physiological pathways
├── behavioral/             # Health behaviors (with structural context)
└── healthcare_access/      # Insurance, providers, services
```

## Related Resources

- **Full Documentation**: `docs/LLM & Discovery Pipeline/MECHANISM_DISCOVERY_PIPELINE.md`
- **Schema Definition**: `mechanism-bank/schemas/mechanism_schema_mvp.json`
- **Schema Config**: `backend/config/schema_config.py`
- **Mechanism Validator Agent**: `.claude/agents/mechanism-validator.md`
- **Mechanism Command**: `.claude/commands/mechanism.md`
