# LLM Mechanism Discovery Pipeline

This directory contains the automated mechanism discovery pipeline for the HealthSystems Platform MVP.

## Overview

The pipeline automates the discovery of causal mechanisms from scientific literature using:
- **Literature search**: Semantic Scholar + PubMed APIs
- **LLM extraction**: Claude Sonnet 4.5 for topology and direction extraction
- **Validation**: Structural competency checks and quality filters
- **Output**: YAML files for the mechanism bank

**MVP Scope**: Topology and direction only (not quantification)

## Files

### Core Modules

- **`llm_mechanism_discovery.py`**: Claude API integration for extracting mechanisms from paper abstracts
- **`literature_search.py`**: Semantic Scholar and PubMed search integration
- **`end_to_end_discovery.py`**: Complete pipeline combining search + extraction + validation

### Usage

- Run demos and tests directly from the module files
- Import classes for custom workflows

---

## Quick Start

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Set Environment Variables

```bash
# Required: Claude API key
export ANTHROPIC_API_KEY="your_api_key_here"

# Optional: Semantic Scholar API key (for higher rate limits)
export SEMANTIC_SCHOLAR_API_KEY="your_key_here"

# Optional: PubMed email (recommended by NCBI)
export PUBMED_EMAIL="your_email@example.com"
```

### 3. Run Demo

```bash
cd pipelines
python end_to_end_discovery.py
```

This will:
1. Search for papers on "housing quality → respiratory health"
2. Extract mechanisms from each paper
3. Validate and deduplicate
4. Save mechanisms to `mechanism-bank/mechanisms/`
5. Generate a discovery report

---

## Usage Examples

### Example 1: Housing → Health Mechanisms

```python
from end_to_end_discovery import EndToEndDiscoveryPipeline

# Initialize pipeline
pipeline = EndToEndDiscoveryPipeline(
    pubmed_email="your_email@example.com"
)

# Discover mechanisms
mechanisms = pipeline.discover_mechanisms_for_topic(
    topic_query="housing quality respiratory health asthma",
    max_papers=10,
    year_range=(2015, 2024),
    min_citations=10,
    focus_area="housing to health"
)

# Save to mechanism bank
pipeline.save_mechanisms()

# Generate report
pipeline.print_summary()
```

### Example 2: Eviction → Health Mechanisms

```python
mechanisms = pipeline.discover_mechanisms_for_topic(
    topic_query="eviction housing displacement health emergency department",
    max_papers=10,
    year_range=(2015, 2024),
    min_citations=5,
    focus_area="housing policy to health"
)

pipeline.save_mechanisms()
report = pipeline.generate_discovery_report(
    output_file="eviction_health_report.json"
)
```

### Example 3: Medicaid Expansion → Health

```python
mechanisms = pipeline.discover_mechanisms_for_topic(
    topic_query="medicaid expansion health outcomes mortality insurance coverage",
    max_papers=15,
    year_range=(2014, 2024),
    min_citations=20,
    focus_area="health policy to outcomes"
)

pipeline.save_mechanisms()
```

### Example 4: Custom Literature Search Only

```python
from literature_search import LiteratureSearchAggregator

# Initialize search
search = LiteratureSearchAggregator(
    pubmed_email="your_email@example.com"
)

# Search for papers
papers = search.search(
    query="food insecurity diabetes",
    limit_per_source=20,
    year_range=(2010, 2024),
    min_citations=5
)

# Process papers
for paper in papers:
    print(f"{paper.title} ({paper.year})")
    print(f"  DOI: {paper.doi}")
    print(f"  Citations: {paper.citation_count}")
```

### Example 5: Extract from Single Paper

```python
from llm_mechanism_discovery import LLMMechanismDiscovery

# Initialize LLM discovery
discovery = LLMMechanismDiscovery()

# Extract from abstract
mechanisms = discovery.extract_mechanisms_from_paper(
    paper_abstract="Your abstract text here...",
    paper_title="Paper title",
    focus_area="housing to health"
)

# Save mechanisms
from pathlib import Path
output_dir = Path("../../mechanism-bank/mechanisms")

for mech in mechanisms:
    discovery.save_mechanism(mech, output_dir)
```

---

## MVP Schema

Mechanisms extracted in MVP focus on **topology and direction**, not quantification:

### Required Fields

```yaml
id: from_node_to_node
name: Source Node → Target Node
from_node:
  node_id: snake_case_id
  node_name: Human Readable Name
to_node:
  node_id: snake_case_id
  node_name: Human Readable Name
direction: positive|negative  # positive: ↑A → ↑B; negative: ↑A → ↓B
category: built_environment|social_environment|economic|political|healthcare_access|biological
mechanism_pathway:
  - Step 1: ...
  - Step 2: ...
evidence:
  quality_rating: A|B|C  # A: 5+ studies, B: 3-4, C: 1-2
  n_studies: <number>
  primary_citation: "Chicago-style citation"
  doi: "10.xxxx/xxxxx"
last_updated: YYYY-MM-DD
version: "1.0"
```

### Optional Fields

```yaml
spatial_variation:
  varies_by_geography: true|false
  variation_notes: "Description..."
moderators:
  - name: moderator_name
    direction: strengthens|weakens
    strength: weak|moderate|strong
    description: "How it operates"
structural_competency:
  equity_implications: "How this relates to health equity"
llm_metadata:
  extracted_by: claude-sonnet-4.5
  extraction_confidence: high|medium|low
```

---

## Structural Competency Guidelines

The pipeline is designed to prioritize **structural determinants** over individual-level factors.

### ✓ GOOD Mechanisms (Structural)

- **Policy → Outcomes**: Medicaid expansion → insurance coverage → healthcare access
- **Economic Systems → Health**: Eviction → housing displacement → healthcare discontinuity
- **Spatial Arrangements → Exposures**: Residential segregation → environmental pollution → respiratory disease

### ✗ BAD Mechanisms (Individual Blame)

- "Poor health literacy → medication non-adherence" (ignores educational inequality)
- "Lack of exercise → obesity" (ignores built environment constraints)
- "Non-compliance → poor outcomes" (blames patients for systemic failures)

### Equity Lens

Always consider:
- **Differential exposure**: Who is more likely to experience this mechanism?
- **Differential vulnerability**: Who is more affected by it?
- **Root causes**: What structural factors create these patterns?

---

## Output Structure

Mechanisms are saved to the mechanism bank:

```
mechanism-bank/
└── mechanisms/
    ├── built_environment/
    │   ├── housing_quality_to_respiratory_health.yml
    │   └── eviction_rate_to_ed_utilization.yml
    ├── economic/
    │   └── poverty_rate_to_healthcare_access.yml
    ├── political/
    │   └── medicaid_expansion_to_insurance_coverage.yml
    └── healthcare_access/
        └── healthcare_continuity_to_chronic_disease_control.yml
```

---

## Quality Control

### Automatic Validation

1. **Schema validation**: JSON schema for required fields
2. **Confidence filtering**: Low-confidence extractions flagged
3. **Structural competency check**: Individual-level blame mechanisms rejected
4. **Deduplication**: Duplicate node pairs merged

### Manual Review

After automatic extraction:
1. Review mechanisms with `confidence: medium`
2. Verify citations and evidence quality
3. Check for structural competency alignment
4. Validate node naming consistency

### Validation Script

```bash
cd ../../mechanism-bank
python scripts/validate_mechanisms.py
```

---

## Performance & Costs

### Rate Limits

- **Semantic Scholar**: 100 requests / 5 minutes (free tier)
- **PubMed**: 3 requests / second (free tier)
- **Claude API**: 40,000 tokens/min (rate varies by tier)

### Cost Estimates (Claude API)

Assuming average paper abstract = 300 words (~400 tokens):

- **Input**: ~600 tokens per paper (prompt + abstract)
- **Output**: ~800 tokens per paper (mechanisms extracted)
- **Total**: ~1,400 tokens per paper

**Example costs** (using Claude Sonnet 4.5 pricing):
- 100 papers: ~140,000 tokens ≈ **$0.84**
- 500 papers: ~700,000 tokens ≈ **$4.20**
- 2000 papers (for 2000 mechanisms): ~2.8M tokens ≈ **$16.80**

*Prices as of 2025. Check current Anthropic pricing.*

### Processing Time

- Literature search: ~5-10 seconds per query
- LLM extraction: ~10-15 seconds per paper
- **Total**: ~20-25 seconds per paper

**Example timelines**:
- 100 papers: ~40 minutes
- 500 papers: ~3.5 hours
- 2000 papers: ~14 hours

---

## Troubleshooting

### "No papers found"

- Check query syntax (use keywords, not full sentences)
- Widen year range
- Lower min_citations threshold
- Try different search terms

### "Error extracting mechanisms"

- Check ANTHROPIC_API_KEY is set
- Verify API key is valid and has credits
- Check rate limits (wait and retry)
- Verify paper has abstract (some papers don't)

### "Schema validation failed"

- Check mechanism YAML against schema
- Verify all required fields present
- Check enum values (direction, category, etc.)

### Low-quality extractions

- Increase min_citations to filter for higher-impact papers
- Add more specific focus_area hints
- Review and reject low-confidence mechanisms
- Adjust prompt for your domain (edit `create_topology_extraction_prompt`)

---

## Customization

### Custom Prompt Templates

Edit the prompt in `llm_mechanism_discovery.py` > `create_topology_extraction_prompt()`:

```python
def create_topology_extraction_prompt(self, paper_abstract, paper_title, focus_area):
    # Customize this prompt for your domain
    prompt = f"""
    Your custom instructions here...
    """
    return prompt
```

### Custom Validation Rules

Edit validation in `end_to_end_discovery.py` > `_validate_mechanisms()`:

```python
def _validate_mechanisms(self, mechanisms):
    valid = []
    for mech in mechanisms:
        # Add your custom validation logic
        if your_custom_check(mech):
            valid.append(mech)
    return valid
```

### Custom Search Queries

Create topic-specific search functions:

```python
def discover_environmental_justice_mechanisms():
    pipeline = EndToEndDiscoveryPipeline()

    queries = [
        "environmental pollution health disparities race",
        "industrial facilities residential proximity health",
        "air quality inequality asthma"
    ]

    all_mechanisms = []
    for query in queries:
        mechanisms = pipeline.discover_mechanisms_for_topic(
            topic_query=query,
            max_papers=10,
            focus_area="environmental justice"
        )
        all_mechanisms.extend(mechanisms)

    pipeline.discovered_mechanisms = all_mechanisms
    pipeline.save_mechanisms()
```

---

## Next Steps

### Phase 1 (Current - MVP)

- [x] Build LLM extraction pipeline
- [x] Integrate literature search
- [x] Create end-to-end workflow
- [ ] **Test on 50-100 papers**
- [ ] **Iterate on prompt quality**
- [ ] **Expert validation workflow**
- [ ] **Scale to 500 mechanisms**
- [ ] **Reach 2000 mechanisms**

### Phase 2 (Future - Quantification)

- [ ] Extract effect sizes (OR, RR, β, etc.)
- [ ] Meta-analytic pooling
- [ ] Bayesian synthesis
- [ ] Quantified moderators
- [ ] Uncertainty propagation

---

## Contributing

When adding new mechanisms:

1. Run the discovery pipeline
2. Review extracted mechanisms manually
3. Validate with `validate_mechanisms.py`
4. Create git commit with mechanism additions
5. Include discovery report in commit message

Example commit:

```bash
git add mechanism-bank/mechanisms/
git commit -m "Add 15 housing → health mechanisms

Discovery run: housing quality → respiratory health
Papers processed: 10
Evidence quality: A/B tier only
Validated by: [Your initials]

Report: discovery_report_housing_health.json"
```

---

## Support

For questions or issues:
- Review documentation in `/docs`
- Check validation errors with `validate_mechanisms.py`
- Review LLM extraction confidence scores
- Consult structural competency framework in docs

---

**Last Updated**: 2025-01-16
**MVP Version**: 1.0
**Pipeline Status**: Proof of Concept → Testing Phase
