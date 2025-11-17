# HealthSystems Platform - Setup Guide

This guide will help you get the LLM mechanism discovery pipeline running in **under 10 minutes**.

## Prerequisites

- Python 3.11+
- pip
- Anthropic Claude API key ([Get one here](https://console.anthropic.com/))
- (Optional) Git for version control

---

## Quick Setup (5 minutes)

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

**Expected output**:
```
Successfully installed anthropic-0.39.0 fastapi-0.104.1 ...
```

### 2. Configure Environment

```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your API key
# (Use your favorite text editor)
nano .env
```

**Add your Anthropic API key**:
```bash
ANTHROPIC_API_KEY=sk-ant-api03-...
PUBMED_EMAIL=your_email@example.com
```

### 3. Test the Pipeline

```bash
cd pipelines
python end_to_end_discovery.py
```

**Expected output**:
```
================================================================================
DEMO: Housing Quality → Health Mechanism Discovery
================================================================================

[1/4] Searching for papers...
Searching Semantic Scholar for: housing quality respiratory health asthma children
  Found 5 papers
Searching PubMed for: housing quality respiratory health asthma children
  Found 5 papers

Total unique papers: 8

[2/4] Extracting mechanisms from papers...
  Processing paper 1/8: Housing Quality and Pediatric Asthma...
    ✓ Extracted 2 mechanism(s)
  ...

[3/4] Validating mechanisms...
  ✓ 7/8 mechanisms passed validation

[4/4] Deduplicating mechanisms...
  ✓ 6 unique mechanisms after deduplication

Saving 6 mechanisms to bank...
✓ Saved mechanism: mechanism-bank/mechanisms/built_environment/housing_quality_to_respiratory_health.yml
...

✓ Demo complete!
```

**You're done!** Check `mechanism-bank/mechanisms/` for generated YAML files.

---

## Detailed Setup

### Option 1: Using Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate (Linux/Mac)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your keys
```

### Option 2: Using Conda

```bash
# Create conda environment
conda create -n healthsystems python=3.11
conda activate healthsystems

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your keys
```

### Option 3: Using Docker

```bash
# Build image
docker build -t healthsystems-backend .

# Run container
docker run -it --env-file .env healthsystems-backend

# Inside container
cd pipelines
python end_to_end_discovery.py
```

---

## Testing Your Setup

### Test 1: Literature Search Only

```bash
cd pipelines
python -c "
from literature_search import LiteratureSearchAggregator

search = LiteratureSearchAggregator(pubmed_email='your_email@example.com')
papers = search.search('housing health', limit_per_source=2)
print(f'Found {len(papers)} papers')
for p in papers:
    print(f'  - {p.title}')
"
```

**Expected**: Prints 2-4 paper titles

### Test 2: LLM Extraction Only

```bash
python -c "
import os
os.environ['ANTHROPIC_API_KEY'] = 'your_key_here'

from llm_mechanism_discovery import LLMMechanismDiscovery

discovery = LLMMechanismDiscovery()

test_abstract = '''
Poor housing quality increases asthma risk in children through exposure
to mold, dust mites, and poor ventilation. A study of 500 families found
children in substandard housing had 2x higher asthma rates.
'''

mechanisms = discovery.extract_mechanisms_from_paper(
    paper_abstract=test_abstract,
    paper_title='Housing and Asthma',
    focus_area='housing to health'
)

print(f'Extracted {len(mechanisms)} mechanisms')
for m in mechanisms:
    print(f'  {m.from_node_name} → {m.to_node_name} ({m.direction})')
"
```

**Expected**: Extracts 1-2 mechanisms from the test abstract

### Test 3: End-to-End Pipeline

```bash
cd pipelines
python end_to_end_discovery.py
```

**Expected**: Completes full demo and saves mechanisms to mechanism bank

---

## Troubleshooting

### Issue: `ImportError: No module named 'anthropic'`

**Solution**:
```bash
pip install anthropic
# Or reinstall all dependencies
pip install -r requirements.txt
```

### Issue: `ValueError: ANTHROPIC_API_KEY environment variable not set`

**Solution**:
```bash
# Option 1: Set in .env file
echo "ANTHROPIC_API_KEY=your_key_here" >> .env

# Option 2: Set in terminal (temporary)
export ANTHROPIC_API_KEY=your_key_here  # Linux/Mac
set ANTHROPIC_API_KEY=your_key_here     # Windows CMD
$env:ANTHROPIC_API_KEY="your_key_here"  # Windows PowerShell
```

### Issue: `No papers found`

**Possible causes**:
1. **Network issue**: Check internet connection
2. **API rate limit**: Wait 1 minute and retry
3. **Query too specific**: Try broader search terms

**Solution**:
```python
# Try simpler query
papers = search.search('housing health', limit_per_source=5)
```

### Issue: `Error extracting mechanisms: 401 Unauthorized`

**Cause**: Invalid or expired API key

**Solution**:
1. Check API key at https://console.anthropic.com/
2. Verify key is correctly set in `.env`
3. Ensure no extra spaces or quotes in `.env` file

### Issue: `Rate limit exceeded`

**Cause**: Too many requests to Claude API

**Solution**:
```python
# Add delay between extractions
import time

for paper in papers:
    mechanisms = discovery.extract_mechanisms_from_paper(...)
    time.sleep(2)  # Wait 2 seconds between calls
```

### Issue: Pipeline runs but generates poor-quality mechanisms

**Solutions**:
1. **Filter for higher-quality papers**:
   ```python
   papers = search.search(query, min_citations=20, year_range=(2015, 2024))
   ```

2. **Add more specific focus area**:
   ```python
   mechanisms = discovery.extract_mechanisms_from_paper(
       paper_abstract=abstract,
       paper_title=title,
       focus_area="housing policy interventions to child respiratory health outcomes"
   )
   ```

3. **Review and validate manually**:
   ```bash
   # Check extracted mechanisms
   ls ../../mechanism-bank/mechanisms/built_environment/

   # Validate schema
   cd ../../mechanism-bank
   python scripts/validate_mechanisms.py
   ```

---

## Verifying Installation

Run this comprehensive test:

```bash
cd backend
python -c "
import sys

print('Python version:', sys.version)
print()

# Test imports
try:
    import anthropic
    print('✓ anthropic installed')
except ImportError:
    print('✗ anthropic NOT installed')

try:
    import fastapi
    print('✓ fastapi installed')
except ImportError:
    print('✗ fastapi NOT installed')

try:
    import yaml
    print('✓ pyyaml installed')
except ImportError:
    print('✗ pyyaml NOT installed')

try:
    import requests
    print('✓ requests installed')
except ImportError:
    print('✗ requests NOT installed')

print()

# Test environment
import os
if os.getenv('ANTHROPIC_API_KEY'):
    print('✓ ANTHROPIC_API_KEY set')
else:
    print('✗ ANTHROPIC_API_KEY NOT set')

if os.getenv('PUBMED_EMAIL'):
    print('✓ PUBMED_EMAIL set')
else:
    print('⚠ PUBMED_EMAIL not set (optional)')

print()
print('Setup verification complete!')
"
```

**Expected output**:
```
Python version: 3.11.x
✓ anthropic installed
✓ fastapi installed
✓ pyyaml installed
✓ requests installed
✓ ANTHROPIC_API_KEY set
✓ PUBMED_EMAIL set
Setup verification complete!
```

---

## Next Steps After Setup

### 1. Run Initial Mechanism Discovery

Pick a topic and generate your first mechanisms:

```bash
cd pipelines
python -c "
from end_to_end_discovery import EndToEndDiscoveryPipeline

pipeline = EndToEndDiscoveryPipeline(pubmed_email='your_email@example.com')

# Choose your topic
mechanisms = pipeline.discover_mechanisms_for_topic(
    topic_query='YOUR TOPIC HERE',  # e.g., 'eviction health'
    max_papers=10,
    year_range=(2015, 2024),
    min_citations=5
)

pipeline.save_mechanisms()
pipeline.print_summary()
"
```

**Topic suggestions**:
- `"eviction housing displacement health"`
- `"medicaid expansion health outcomes"`
- `"food insecurity diabetes"`
- `"pollution respiratory health children"`
- `"incarceration family health"`

### 2. Review Generated Mechanisms

```bash
# View generated YAML files
ls ../../mechanism-bank/mechanisms/

# Read a mechanism
cat ../../mechanism-bank/mechanisms/built_environment/housing_quality_to_respiratory_health.yml
```

### 3. Validate Mechanisms

```bash
cd ../../mechanism-bank
python scripts/validate_mechanisms.py
```

### 4. Iterate on Topics

Create a batch script:

```python
# batch_discovery.py
from end_to_end_discovery import EndToEndDiscoveryPipeline

pipeline = EndToEndDiscoveryPipeline(pubmed_email='your_email@example.com')

topics = [
    "housing quality respiratory health",
    "eviction health outcomes",
    "food insecurity chronic disease",
    "pollution environmental health children"
]

for topic in topics:
    print(f"\n{'='*80}\nProcessing: {topic}\n{'='*80}\n")

    mechanisms = pipeline.discover_mechanisms_for_topic(
        topic_query=topic,
        max_papers=10,
        year_range=(2015, 2024)
    )

    pipeline.save_mechanisms()

    # Clear for next topic
    pipeline.discovered_mechanisms = []
    pipeline.processed_papers = []

print("\n✓ Batch discovery complete!")
```

Run it:
```bash
python batch_discovery.py
```

### 5. Monitor Costs

Track your Claude API usage:
- Visit https://console.anthropic.com/
- Check "Usage" tab
- Review token consumption and costs

**Estimate**: 10 papers ≈ 14,000 tokens ≈ $0.08

### 6. Build Towards MVP Goal (2000 Mechanisms)

**Recommended approach**:
1. **Week 1**: Test on 50 papers, validate quality
2. **Week 2-3**: Scale to 200 mechanisms across 5 topic areas
3. **Month 2-3**: Reach 500 mechanisms
4. **Month 4-6**: Scale to 2000 mechanisms

**Topics to cover** (for comprehensive mechanism bank):
- Housing (quality, eviction, homelessness)
- Healthcare access (insurance, Medicaid, providers)
- Economic security (poverty, employment, wages)
- Built environment (pollution, green space, walkability)
- Social environment (discrimination, segregation, social capital)
- Criminal justice (incarceration, policing, legal debt)
- Education (quality, funding, segregation)
- Food systems (insecurity, access, quality)

---

## Development Workflow

### Daily Development

```bash
# 1. Activate environment
source venv/bin/activate  # or conda activate healthsystems

# 2. Pull latest changes (if using git)
git pull

# 3. Run discovery pipeline
cd backend/pipelines
python your_discovery_script.py

# 4. Validate new mechanisms
cd ../../mechanism-bank
python scripts/validate_mechanisms.py

# 5. Commit new mechanisms (if valid)
git add mechanisms/
git commit -m "Add X mechanisms for Y topic"
```

### Testing Changes

```bash
# Run unit tests
cd backend
pytest tests/

# Run specific test
pytest tests/test_llm_discovery.py

# Run with coverage
pytest --cov=pipelines tests/
```

### Code Quality

```bash
# Format code
black pipelines/

# Type checking
mypy pipelines/

# Linting
flake8 pipelines/
```

---

## Getting Help

### Check Logs

```bash
# Pipeline logs
tail -f logs/discovery_pipeline.log

# API logs (when running backend)
tail -f logs/api.log
```

### Documentation

- **Pipeline README**: `backend/pipelines/README.md`
- **Architecture docs**: `docs/Core Technical Architecture/`
- **MVP scope**: `docs/Phase 2 - Quantification/README.md`

### Common Commands Reference

```bash
# Search literature
python -m pipelines.literature_search

# Test LLM extraction
python -m pipelines.llm_mechanism_discovery

# Run full pipeline
python -m pipelines.end_to_end_discovery

# Validate mechanisms
cd ../mechanism-bank && python scripts/validate_mechanisms.py

# Run tests
pytest tests/

# Format code
black .
```

---

## Performance Optimization

### Speed up Literature Search

```python
# Use only Semantic Scholar (faster, better structured data)
papers = search.search(query, sources=["semantic_scholar"])

# Or only PubMed (medical focus)
papers = search.search(query, sources=["pubmed"])
```

### Reduce LLM Costs

```python
# Use shorter max_tokens for simple extractions
mechanisms = discovery.extract_mechanisms_from_paper(
    ...,
    max_tokens=2000  # Default is 4000
)

# Filter papers before extraction (only high-impact)
papers = [p for p in papers if p.citation_count > 50]
```

### Parallel Processing

```python
from concurrent.futures import ThreadPoolExecutor

def process_paper(paper):
    return discovery.extract_mechanisms_from_paper(
        paper.abstract, paper.title
    )

with ThreadPoolExecutor(max_workers=5) as executor:
    results = executor.map(process_paper, papers)
```

---

## Production Deployment

For production use:

1. **Use environment variables** (not `.env` file)
2. **Set up monitoring** (Sentry, logging)
3. **Configure rate limiting** (respect API limits)
4. **Add retry logic** (for network failures)
5. **Implement caching** (avoid re-processing papers)

See `docs/Implementation & Operations/14_COMPUTATIONAL_INFRASTRUCTURE.md` for deployment guide.

---

**Setup complete!** You're ready to start discovering mechanisms.

For questions: Review docs or check troubleshooting section above.
