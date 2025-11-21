# Alcohol Mechanism Batch Extraction Guide

## Overview

This guide explains how to run the comprehensive alcohol mechanism extraction pipeline that will create 90-130 new mechanisms covering 1-hop, 2-hop, and 3-hop connections to alcohol use disorder.

## Created Files

1. **`batch_alcohol_mechanisms.py`** - Main batch extraction script with all 6 phases
2. **`run_alcohol_extraction.py`** - Simplified runner script
3. **`test_extraction.py`** - Test script to validate pipeline

## Prerequisites

### 1. Set Environment Variables

```bash
# Required: Anthropic API key
export ANTHROPIC_API_KEY="your-key-here"

# Optional: For higher rate limits
export SEMANTIC_SCHOLAR_API_KEY="your-key-here"  # Optional
export PUBMED_EMAIL="your-email@example.com"     # Recommended
export PUBMED_API_KEY="your-key-here"            # Optional
```

### 2. Install Dependencies

All dependencies should already be installed from `backend/requirements.txt`:
- `anthropic>=0.39.0`
- `pyyaml>=6.0.1`
- `requests>=2.31.0`
- `pydantic>=2.5.0`

## Quick Start

### Option 1: Test Run (Recommended First)

Test the pipeline with a single query:

```bash
cd backend
python scripts/test_extraction.py
```

This will:
- Search for 3-5 papers on "alcohol use disorder liver cirrhosis"
- Extract mechanisms from the first paper
- Save to `mechanism-bank/mechanisms/`
- Validate the entire pipeline works

### Option 2: Run Specific Phases

Run only Phase 1 (direct health consequences):

```bash
cd backend
python scripts/run_alcohol_extraction.py --phases 1 --limit 10
```

Run Phases 1-3:

```bash
cd backend
python scripts/run_alcohol_extraction.py --phases 1 2 3 --limit 10
```

### Option 3: Full Extraction (All 6 Phases)

**WARNING: This will take 3-6 hours and cost $50-100 in API credits**

```bash
cd backend
python scripts/batch_alcohol_mechanisms.py
```

Or with the runner:

```bash
cd backend
python scripts/run_alcohol_extraction.py --phases 1 2 3 4 5 6 --limit 15
```

### Option 4: Test Mode (Limited Queries)

Run in test mode with only 2 queries per phase:

```bash
cd backend
python scripts/run_alcohol_extraction.py --test --phases 1 2
```

## Phase Breakdown

### Phase 1: Direct Health Consequences (15 queries)
**Expected: 15-20 mechanisms**

- Alcohol → Liver cirrhosis
- Alcohol → Hypertension
- Alcohol → Falls/injuries
- Alcohol → Motor vehicle crashes
- Alcohol → Suicide
- Alcohol → Cancer
- Alcohol → Cardiomyopathy
- Alcohol → Pancreatitis
- Alcohol → GI bleeding
- Alcohol → Cognitive impairment
- And more...

### Phase 2: Missing Risk Factors (17 queries)
**Expected: 20-25 mechanisms**

- Anxiety → Alcohol
- PTSD → Alcohol
- Chronic pain → Alcohol
- Discrimination → Stress → Alcohol
- IPV exposure → PTSD → Alcohol
- Homelessness → Alcohol
- Outlet density → Alcohol
- Sleep disorders → Alcohol
- And more...

### Phase 3: Social/Behavioral Consequences (10 queries)
**Expected: 10-15 mechanisms**

- Alcohol → IPV perpetration
- Alcohol → Child neglect/abuse
- Alcohol → Incarceration
- Alcohol → Homelessness
- Alcohol → Social isolation
- Alcohol → Medication non-adherence
- And more...

### Phase 4: Protective/Treatment Mechanisms (14 queries)
**Expected: 12-15 mechanisms**

- Medication for AUD → Recovery
- SBIRT → Reduced drinking
- Mental health treatment → Reduced alcohol
- Social support → Prevention
- Alcohol taxation → Reduced consumption
- Outlet restrictions → Reduced harm
- Housing stability → Reduced alcohol
- And more...

### Phase 5: Two-Hop Chains (14 queries)
**Expected: 20-30 mechanisms**

- Eviction → Housing instability → AUD
- Alcohol → Liver disease → Transplant
- Alcohol → Hypertension → Stroke
- Alcohol → Falls → Hip fracture
- Unemployment → Poverty → Homelessness
- Discrimination → Stress → Health
- And more...

### Phase 6: Three-Hop Structural Pathways (10 queries)
**Expected: 15-20 mechanisms**

- Medicaid expansion → Insurance → Treatment
- Minimum wage → Poverty → Health
- Housing policy → Rent burden → Health
- Mass incarceration → Family disruption → ACEs
- Education funding → Employment → Health
- And more...

## Output

### Mechanism Files

Mechanisms are saved to:
```
mechanism-bank/mechanisms/
  ├── behavioral/
  ├── biological/
  ├── built_environment/
  ├── economic/
  ├── healthcare_access/
  ├── political/
  └── social_environment/
```

Each mechanism is a YAML file named: `{from_node_id}_to_{to_node_id}.yml`

### Progress Reports

During extraction, progress reports are saved to:
- `mechanism-bank/extraction_progress.json` - Updated after each phase
- `mechanism-bank/extraction_final_report.json` - Final summary
- `mechanism-bank/extraction_errors.json` - Any errors encountered

## After Extraction

### 1. Validate Mechanisms

```bash
python mechanism-bank/validation/validate_mechanisms.py
```

This checks:
- JSON schema compliance
- Required fields present
- CI ordering correct
- Evidence quality standards met
- Citation format valid

### 2. Review Mechanisms

Manually review extracted mechanisms for:
- Accuracy of pathway descriptions
- Appropriate moderators
- Structural competency alignment
- Evidence quality ratings
- Citation completeness

### 3. Load to Database

Start backend:
```bash
cd backend
uvicorn app.main:app --reload
```

Load mechanisms:
```bash
curl -X POST http://localhost:8000/api/mechanisms/admin/load-from-yaml
```

### 4. Test API

```bash
# List all mechanisms
curl http://localhost:8000/api/mechanisms/

# Filter by category
curl http://localhost:8000/api/mechanisms/?category=biological

# Search pathways
curl "http://localhost:8000/api/mechanisms/search/pathway?from_node=alcohol_use_disorder&to_node=liver_disease_mortality"

# Get statistics
curl http://localhost:8000/api/mechanisms/stats/summary
```

### 5. Run Backend Tests

```bash
cd backend
pytest tests/test_mechanisms_api.py -v
```

### 6. Commit to Git

```bash
git status

# Add new mechanisms
git add mechanism-bank/mechanisms/

# Commit Phase 1
git commit -m "mechanism: add Phase 1 alcohol health consequences (20 mechanisms)

- Direct health outcomes: liver disease, cardiovascular, injuries, suicide
- Evidence quality: Tier A (meta-analyses and systematic reviews)
- Sources: 45 papers from Semantic Scholar and PubMed
- LLM-assisted extraction using claude-sonnet-4

🤖 Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>"

# Repeat for other phases...

# Push when ready
git push
```

## Troubleshooting

### API Key Error

```
ERROR: ANTHROPIC_API_KEY environment variable not set
```

**Solution:** Set the environment variable:
```bash
export ANTHROPIC_API_KEY="your-key-here"
```

### Rate Limit Errors

If you hit rate limits on Semantic Scholar or PubMed:
- Script includes automatic delays between requests
- Semantic Scholar: 100 requests per 5 minutes (built-in 1s delay)
- PubMed: 3 requests per second (built-in 0.5s delay)

To reduce rate limit issues:
- Set `SEMANTIC_SCHOLAR_API_KEY` for 10x higher limits
- Set `PUBMED_API_KEY` for 10 requests/sec

### No Papers Found

If a query returns no papers:
- Check your internet connection
- Verify API endpoints are accessible
- Try broadening the search query
- Check year_range isn't too restrictive

### Extraction Errors

If mechanism extraction fails for a paper:
- Error is logged to `extraction_errors.json`
- Script continues with next paper
- Review errors after completion
- Can manually extract from failed papers

### Schema Validation Errors

If saved mechanisms fail validation:
- Check `extraction_errors.json` for details
- Common issues:
  - Missing required fields
  - Invalid category values
  - Incorrect CI ordering
  - Missing DOI or URL in citations
- Fix manually or re-extract

## Advanced Usage

### Custom Phase Configuration

Edit `batch_alcohol_mechanisms.py` to modify queries:

```python
PHASE_1_QUERIES = {
    "name": "Direct Health Consequences",
    "queries": [
        "your custom query here",
        # Add more queries...
    ],
    "focus_area": "alcohol to health outcomes",
    "expected_count": "15-20 mechanisms"
}
```

### Adjust Search Parameters

Modify search parameters in the script:

```python
extractor.run_all_phases(
    limit_per_query=20,  # More papers per query
    year_range=(2015, 2024),  # More recent papers only
    min_citations=20  # Higher citation threshold
)
```

### Run Individual Phases

```python
from scripts.batch_alcohol_mechanisms import (
    AlcoholMechanismBatchExtractor,
    PHASE_1_QUERIES
)

extractor = AlcoholMechanismBatchExtractor(output_dir=Path("mechanism-bank/mechanisms"))

# Run only Phase 1
summary = extractor.run_phase(
    phase_config=PHASE_1_QUERIES,
    limit_per_query=15,
    year_range=(2010, 2024),
    min_citations=10
)
```

## Cost Estimation

### API Costs

**Semantic Scholar:** Free (no API key required)
**PubMed:** Free (no API key required)
**Anthropic Claude:**

- ~300-500 papers × ~4000 tokens per extraction
- ~1.2-2M tokens total
- At $3 per 1M input tokens + $15 per 1M output tokens
- **Estimated cost: $50-100**

### Time Estimation

- Literature search: ~30-60 minutes
- Mechanism extraction: ~2-4 hours (depends on API latency)
- Validation & review: ~2-3 hours
- **Total: ~5-8 hours** (mostly automated)

## Support

If you encounter issues:

1. Check this README for troubleshooting steps
2. Review `extraction_errors.json` for specific error messages
3. Test with `test_extraction.py` to isolate the problem
4. Check backend logs for API-related errors
5. Verify all dependencies are installed: `pip install -r requirements.txt`

## Next Steps After Extraction

1. ✅ Run validation script
2. ✅ Manual quality review
3. ✅ Load to database
4. ✅ Test API endpoints
5. ✅ Run backend tests
6. ✅ Update AlcoholismSystemView with new nodes
7. ✅ Test frontend visualization
8. ✅ Commit to git
9. ✅ Update documentation
10. ✅ Celebrate! 🎉

---

**Created:** 2025-01-19
**Author:** Claude Code + HealthSystems Team
**Version:** 1.0
