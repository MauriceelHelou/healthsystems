# HealthSystems Platform - Quick Start Guide

**Goal**: Get the LLM mechanism discovery pipeline running in 5 minutes.

---

## What You'll Need

- Python 3.11+
- Claude API key from [console.anthropic.com](https://console.anthropic.com/)
- 5 minutes

---

## Step 1: Install Dependencies (2 minutes)

Open your terminal and run:

```bash
cd backend
pip install anthropic pyyaml jsonschema requests pydantic
```

**Expected output**:
```
Successfully installed anthropic-0.39.0 ...
```

---

## Step 2: Set Your API Key (1 minute)

### Option A: Environment Variable (Quick)

**Windows (PowerShell)**:
```powershell
$env:ANTHROPIC_API_KEY="your_api_key_here"
$env:PUBMED_EMAIL="your_email@example.com"
```

**Mac/Linux**:
```bash
export ANTHROPIC_API_KEY="your_api_key_here"
export PUBMED_EMAIL="your_email@example.com"
```

### Option B: .env File (Recommended)

```bash
# Copy example file
cp .env.example .env

# Edit .env and add your key
# (Use notepad, nano, vim, or any text editor)
```

---

## Step 3: Run the Demo (2 minutes)

```bash
cd pipelines
python end_to_end_discovery.py
```

**What happens**:
1. Searches for papers on "housing quality → respiratory health"
2. Extracts mechanisms from 5-8 papers using Claude
3. Validates mechanisms for quality and structural competency
4. Saves to `mechanism-bank/mechanisms/`

**Expected output**:
```
================================================================================
DEMO: Housing Quality → Health Mechanism Discovery
================================================================================

[1/4] Searching for papers...
Searching Semantic Scholar for: housing quality respiratory health asthma children
  Found 5 papers
Searching PubMed for: housing quality respiratory health asthma children
  Found 3 papers

Total unique papers: 7

[2/4] Extracting mechanisms from papers...

  Processing paper 1/7: Housing Quality and Asthma in Children...
    ✓ Extracted 2 mechanism(s)

  Processing paper 2/7: Indoor Air Quality and Respiratory Health...
    ✓ Extracted 1 mechanism(s)

  ...

[3/4] Validating mechanisms...
  ✓ 6/7 mechanisms passed validation

[4/4] Deduplicating mechanisms...
  ✓ 5 unique mechanisms after deduplication

Saving 5 mechanisms to bank...
✓ Saved mechanism: mechanism-bank/mechanisms/built_environment/housing_quality_to_respiratory_health.yml
✓ Saved mechanism: mechanism-bank/mechanisms/built_environment/housing_quality_to_asthma_incidence.yml
...

================================================================================
DISCOVERY SUMMARY
================================================================================

Papers processed: 7
Mechanisms discovered: 5
Errors encountered: 0

Mechanisms by category:
  built_environment: 4
  biological: 1

Mechanisms by confidence:
  high: 3
  medium: 2

✓ Demo complete!
  Mechanisms saved to: mechanism-bank/mechanisms
  Report saved to: discovery_report_housing_health.json
```

---

## Step 4: Review Generated Mechanisms

```bash
# List generated mechanisms
ls ../../mechanism-bank/mechanisms/built_environment/

# Read a mechanism
cat ../../mechanism-bank/mechanisms/built_environment/housing_quality_to_respiratory_health.yml
```

**Example mechanism**:
```yaml
id: housing_quality_to_respiratory_health
name: Housing Quality → Respiratory Health
from_node:
  node_id: housing_quality
  node_name: Housing Quality Index
to_node:
  node_id: respiratory_health
  node_name: Respiratory Health Outcomes
direction: negative  # Poor housing → worse respiratory health
category: built_environment
mechanism_pathway:
  - 'Step 1: Poor housing quality leads to dampness and mold growth'
  - 'Step 2: Mold releases allergens and irritants into indoor air'
  - 'Step 3: Prolonged exposure triggers respiratory inflammation'
  - 'Step 4: Increased asthma incidence and COPD exacerbations'
evidence:
  quality_rating: A
  n_studies: 8
  primary_citation: 'Krieger, James, and Donna L. Higgins. 2002. ...'
  doi: '10.2105/AJPH.92.5.758'
last_updated: '2025-01-16'
version: '1.0'
...
```

---

## Step 5: Try Your Own Topic (Optional)

Edit `end_to_end_discovery.py` or create a new script:

```python
from end_to_end_discovery import EndToEndDiscoveryPipeline

pipeline = EndToEndDiscoveryPipeline(
    pubmed_email='your_email@example.com'
)

# Choose your topic!
mechanisms = pipeline.discover_mechanisms_for_topic(
    topic_query="eviction health outcomes",  # <-- Change this
    max_papers=10,
    year_range=(2015, 2024),
    min_citations=5,
    focus_area="housing policy to health"
)

pipeline.save_mechanisms()
pipeline.print_summary()
```

**Topic ideas**:
- `"food insecurity diabetes"`
- `"medicaid expansion health outcomes"`
- `"air pollution childhood asthma"`
- `"incarceration family health"`
- `"minimum wage health"`

---

## Troubleshooting

### Error: `ModuleNotFoundError: No module named 'anthropic'`

```bash
pip install anthropic
```

### Error: `ValueError: ANTHROPIC_API_KEY environment variable not set`

Set the environment variable (see Step 2 above).

### Error: `No papers found`

Try a broader search query:
```python
mechanisms = pipeline.discover_mechanisms_for_topic(
    topic_query="housing health",  # Simpler query
    max_papers=5
)
```

### Pipeline runs but no mechanisms extracted

- Check that papers have abstracts (some don't)
- Lower the confidence threshold
- Review extraction logs for errors

---

## What's Next?

### Immediate Testing

1. **Manual review**: Read 3-5 generated mechanisms and assess quality
2. **Structural competency check**: Verify no individual-blame mechanisms
3. **Citation accuracy**: Check if DOIs and citations are correct
4. **Node consistency**: Are node names reasonable and consistent?

### Quality Assessment Questions

- [ ] Are mechanisms scientifically accurate?
- [ ] Are directions (positive/negative) correct?
- [ ] Are pathways plausible and well-explained?
- [ ] Are citations properly formatted?
- [ ] Do mechanisms avoid individual blame?
- [ ] Are moderators relevant and insightful?

### If Quality is Good (80%+ accuracy)

✅ **Scale up**: Run on 50 papers across 3 topics
✅ **Expert validation**: Have domain expert review 10-20 mechanisms
✅ **Iterate on prompts**: Refine based on feedback
✅ **Build API**: Start backend development (Week 2-3 plan)

### If Quality is Poor (<80% accuracy)

⚠️ **Iterate on prompts**: Refine LLM instructions
⚠️ **Add examples**: Include more good/bad mechanism examples
⚠️ **Manual curation**: Use LLM as assistant, not autonomous
⚠️ **Expert loop**: Add human validation step

---

## Cost Tracking

Monitor your Claude API usage at [console.anthropic.com](https://console.anthropic.com/)

**Rough estimates**:
- Demo (5-10 papers): **$0.05 - $0.10**
- Testing (50 papers): **$0.40 - $0.50**
- MVP scaling (2000 papers): **$15 - $20**

Very affordable for the value generated!

---

## Getting Help

- **Setup issues**: See [backend/SETUP.md](backend/SETUP.md)
- **Pipeline docs**: See [backend/pipelines/README.md](backend/pipelines/README.md)
- **Architecture**: See `/docs` folder
- **Progress report**: See [PROGRESS_REPORT.md](PROGRESS_REPORT.md)

---

## You're All Set!

The pipeline is ready to use. The critical next step is **validating quality** on real papers.

**Recommended first task**: Run the demo, review 3-5 mechanisms manually, assess if quality meets your standards.

Good luck! 🚀
