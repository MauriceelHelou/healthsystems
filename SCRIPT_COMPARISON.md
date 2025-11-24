# Extraction Script Comparison & Usage Guide

## Available Scripts

### 1. Original: `run_generic_extraction.py` (Base Version)
**Best for**: Quick extraction, simple use cases

```bash
python backend/scripts/run_generic_extraction.py --topic obesity
```

**Features**:
- ✅ Topic-agnostic extraction
- ✅ PubMed + Semantic Scholar search
- ✅ Comprehensive LLM prompt for quantitative metrics
- ✅ YAML file generation
- ❌ No grey literature
- ❌ No paper quality filtering
- ❌ No validation during extraction
- ❌ No analytics reporting

---

### 2. Enhanced: `run_generic_extraction_enhanced.py` (Production Version)
**Best for**: High-quality extraction, research projects

```bash
python backend/scripts/run_generic_extraction_enhanced.py \
  --topic obesity \
  --quality-threshold 0.7 \
  --include-grey-literature \
  --extract-all-metrics \
  --apply-bayesian-weighting
```

**Features**:
- ✅ Everything from base version
- ✅ **Grey literature** (curated government reports, preprints)
- ✅ **Paper quality filtering** (saves 30-50% API costs)
- ✅ **Study type detection** (meta-analysis, RCT, cohort)
- ✅ **Real-time validation** (confidence scoring during extraction)
- ✅ **Bayesian weighting** (optional, for uncertainty quantification)
- ✅ **Comprehensive analytics** (JSON report with quality metrics)
- ✅ **Enhanced quantitative extraction** (tailored prompts by study type)

---

## Quick Comparison Table

| Feature | Base Script | Enhanced Script |
|---------|-------------|-----------------|
| **Literature Sources** | PubMed, Semantic Scholar | + Grey literature |
| **Papers Processed** | All retrieved | Quality-filtered |
| **API Efficiency** | 100% of papers | 50-70% of papers |
| **Study Type Awareness** | No | Yes |
| **Validation** | Post-hoc | Real-time |
| **Bayesian Weighting** | No | Optional |
| **Analytics** | Basic stats | JSON report |
| **Recommended For** | Quick tests | Production use |

---

## When to Use Which Script

### Use Base Script (`run_generic_extraction.py`) When:

✅ **Quick prototyping**
- Testing topic configurations
- Dry runs before large extraction
- Validating node pairs

✅ **Simple use cases**
- No need for quality filtering
- Peer-reviewed literature only
- Basic extraction needs

✅ **Teaching/Demo**
- Simpler codebase to understand
- Fewer dependencies
- Clearer code flow

**Example**:
```bash
# Quick test with 3 papers per query
python backend/scripts/run_generic_extraction.py \
  --topic diabetes \
  --limit 3 \
  --dry-run
```

---

### Use Enhanced Script (`run_generic_extraction_enhanced.py`) When:

✅ **Production extraction**
- Need high-quality mechanisms
- Want to minimize API costs
- Require validation and analytics

✅ **Research projects**
- Publishing results
- Need provenance tracking
- Want comprehensive evidence

✅ **Policy-relevant topics**
- Include government reports
- Need grey literature
- Want Bayesian uncertainty

✅ **Limited API budget**
- Quality filtering reduces costs 30-50%
- Process only high-evidence papers
- Maximize extraction efficiency

**Example**:
```bash
# Production extraction with all features
python backend/scripts/run_generic_extraction_enhanced.py \
  --topic obesity \
  --quality-threshold 0.7 \
  --include-grey-literature \
  --extract-all-metrics \
  --apply-bayesian-weighting \
  --limit 10
```

---

## Cost Comparison

### Scenario: Extract 100 Node Pairs

#### Base Script
```
100 queries × 10 papers/query = 1000 papers
1000 papers × $0.03/paper = $30
```

#### Enhanced Script (Quality Filtered)
```
100 queries × 10 papers/query = 1000 papers retrieved
1000 papers × 0.6 quality pass rate = 600 papers processed
600 papers × $0.03/paper = $18

Savings: $12 (40%)
```

#### Enhanced Script + Grey Literature
```
Peer-reviewed: 600 papers × $0.03 = $18
Grey literature: 30 sources × $0.03 = $1
Total: $19

Benefit: +30 grey lit sources for $1
```

---

## Migration Path

### Step 1: Start with Base Script
```bash
# Test with base version
python backend/scripts/run_generic_extraction.py \
  --topic your_topic \
  --limit 3 \
  --dry-run
```

### Step 2: Review Results
- Check extracted mechanisms in `mechanism-bank/mechanisms/your_topic/`
- Assess quality manually
- Identify papers with weak abstracts

### Step 3: Switch to Enhanced
```bash
# Add quality filtering
python backend/scripts/run_generic_extraction_enhanced.py \
  --topic your_topic \
  --quality-threshold 0.5 \
  --limit 3
```

### Step 4: Add Features Incrementally
```bash
# Add grey literature
python backend/scripts/run_generic_extraction_enhanced.py \
  --topic your_topic \
  --quality-threshold 0.5 \
  --include-grey-literature \
  --limit 5
```

### Step 5: Production Run
```bash
# Full extraction with all features
python backend/scripts/run_generic_extraction_enhanced.py \
  --topic your_topic \
  --quality-threshold 0.7 \
  --include-grey-literature \
  --extract-all-metrics \
  --apply-bayesian-weighting \
  --limit 10
```

---

## Feature-by-Feature Guide

### Quality Threshold (`--quality-threshold`)

**What it does**: Filters papers before extraction based on quality score (0-1)

**Quality Score Formula**:
```
score = 0.3 (abstract present)
      + 0.3 (high citations ≥50)
      + 0.2 (recent year ≥2015)
      + 0.2 (meta-analysis)
      + 0.15 (RCT)
      + 0.1 (cohort)
      + 0.1 (rigorous methods)
```

**Recommended Values**:
- `0.3`: Inclusive (most papers pass)
- `0.5`: **Balanced (default)**
- `0.7`: Strict (only high-quality)
- `0.9`: Very strict (meta-analyses + RCTs only)

**Example**:
```bash
# Only process meta-analyses and RCTs
python backend/scripts/run_generic_extraction_enhanced.py \
  --topic obesity \
  --quality-threshold 0.9
```

---

### Grey Literature (`--include-grey-literature`)

**What it does**: Searches grey literature sources + loads curated collection

**Sources**:
- Automated: medRxiv, bioRxiv preprints
- Curated: Government reports (CDC, NIH, WHO)

**Workflow**:
1. Create curated template:
   ```bash
   python backend/pipelines/grey_literature_search.py
   ```

2. Edit template:
   `backend/data/grey_literature/{topic}_grey_literature.yaml`

3. Run with flag:
   ```bash
   python backend/scripts/run_generic_extraction_enhanced.py \
     --topic obesity \
     --include-grey-literature
   ```

**When to use**:
- Policy-relevant topics (housing, food policy)
- Topics with important government reports
- Want comprehensive evidence base

---

### Extract All Metrics (`--extract-all-metrics`)

**What it does**: Adds emphasis to LLM prompt for quantitative extraction

**Prompt modification**:
```
[EXTRACT ALL QUANTITATIVE METRICS]
```

**Use when**:
- Need complete statistical data
- Building evidence database
- Meta-analysis downstream

---

### Bayesian Weighting (`--apply-bayesian-weighting`)

**What it does**: Calculates Bayesian posterior weights during extraction

**Output**:
```python
{
  'bayesian_weight': {
    'weight': 1.42,
    'ci': [1.21, 1.65]
  }
}
```

**Use when**:
- Need uncertainty quantification
- Planning intervention prioritization
- Building decision support tool

**Note**: Requires extracted effect sizes (not all mechanisms have them)

---

## Analytics Reporting

### Base Script Output
```
Total queries: 320
Mechanisms extracted: 87
Errors: 3
```

### Enhanced Script Output
```json
{
  "queries_processed": 320,
  "papers_retrieved": 3200,
  "papers_quality_filtered": 800,
  "papers_processed": 2400,
  "mechanisms_extracted": 178,
  "high_confidence_mechanisms": 142,
  "meta_analyses_found": 32,
  "effect_sizes_extracted": 156,
  "grey_literature_found": 15,
  "success_rate": 0.556
}
```

**Saved to**: `mechanism-bank/{topic}_extraction_analytics.json`

---

## Troubleshooting

### Too many API calls / High cost

**Solution**: Use enhanced script with quality filtering
```bash
python backend/scripts/run_generic_extraction_enhanced.py \
  --topic your_topic \
  --quality-threshold 0.7 \  # Increase threshold
  --limit 5                  # Reduce papers per query
```

### Low success rate (<30%)

**Solution**: Check query templates, lower quality threshold
```bash
python backend/scripts/run_generic_extraction_enhanced.py \
  --topic your_topic \
  --quality-threshold 0.3    # More inclusive
  --limit 15                 # More papers
```

### Missing important evidence

**Solution**: Add grey literature + lower threshold
```bash
python backend/scripts/run_generic_extraction_enhanced.py \
  --topic your_topic \
  --include-grey-literature \
  --quality-threshold 0.4
```

### Want quantitative mechanisms only

**Solution**: High threshold + meta-analysis focus
```bash
python backend/scripts/run_generic_extraction_enhanced.py \
  --topic your_topic \
  --quality-threshold 0.8 \  # Meta-analyses + RCTs
  --extract-all-metrics
```

---

## Recommendations by Use Case

### Academic Research Paper
```bash
# Enhanced: Quality + Grey Lit + Metrics + Bayesian
python backend/scripts/run_generic_extraction_enhanced.py \
  --topic your_topic \
  --quality-threshold 0.7 \
  --include-grey-literature \
  --extract-all-metrics \
  --apply-bayesian-weighting
```

### Policy Brief
```bash
# Enhanced: Lower threshold + Grey Lit (breadth over precision)
python backend/scripts/run_generic_extraction_enhanced.py \
  --topic your_topic \
  --quality-threshold 0.4 \
  --include-grey-literature
```

### Quick Exploratory Analysis
```bash
# Base script: Fast and simple
python backend/scripts/run_generic_extraction.py \
  --topic your_topic \
  --limit 5
```

### Cost-Constrained Project
```bash
# Enhanced: High threshold + Small limit
python backend/scripts/run_generic_extraction_enhanced.py \
  --topic your_topic \
  --quality-threshold 0.8 \
  --limit 5
```

---

## Summary

**Base Script** = Simple, fast, educational
**Enhanced Script** = Production-ready, cost-efficient, comprehensive

For **most use cases**, use the **enhanced script** with default settings:
```bash
python backend/scripts/run_generic_extraction_enhanced.py --topic your_topic
```

Only use base script for quick tests or learning the system.
