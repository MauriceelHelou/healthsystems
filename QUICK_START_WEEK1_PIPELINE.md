# Quick Start: Week 1 Pipeline

**Goal**: Transform raw extracted mechanisms into MVP-ready mechanisms

## What Does the Week 1 Pipeline Do?

The Week 1 pipeline takes mechanisms extracted from literature and processes them through 4 critical steps:

```
Raw Mechanisms (250+)
    ↓
[1] DEDUPLICATION: Semantic clustering + LLM consolidation
    ↓
Unique Mechanisms (~150, 40% reduction)
    ↓
[2] FUNCTIONAL FORM CLASSIFICATION: Assign sigmoid/threshold/log/etc.
    ↓
Classified Mechanisms
    ↓
[3] SCHEMA VALIDATION: Check compliance with Doc 05
    ↓
Valid Mechanisms
    ↓
[4] BIDIRECTIONAL DETECTION: Find feedback loops
    ↓
MVP-Ready Mechanisms (valid + bidirectional pairs)
```

## Prerequisites

```bash
# Install dependencies (includes sentence-transformers, scikit-learn)
pip install -r backend/requirements.txt

# Set API key
export ANTHROPIC_API_KEY=your-key-here  # Linux/Mac
# or
set ANTHROPIC_API_KEY=your-key-here     # Windows
```

## Quick Start

### Option 1: Run Full Pipeline

```bash
# Process all mechanisms in a directory
python backend/scripts/run_week1_pipeline.py \
  --input-dir mechanism-bank/mechanisms/obesity/
```

**Output**:
- Processed mechanisms saved to `mechanism-bank/mechanisms/obesity_processed/`
- Invalid mechanisms report saved as `invalid_mechanisms_report.txt`
- Console shows detailed stats

### Option 2: Dry Run (No Files Written)

```bash
# See what would happen without writing files
python backend/scripts/run_week1_pipeline.py \
  --input-dir mechanism-bank/mechanisms/obesity/ \
  --dry-run
```

**Output**: Stats only, no files written

### Option 3: Skip Bidirectional (Faster)

```bash
# Skip literature search for reverse mechanisms
python backend/scripts/run_week1_pipeline.py \
  --input-dir mechanism-bank/mechanisms/obesity/ \
  --skip-bidirectional
```

**Speed**: ~60% faster (skips literature searches)

### Option 4: Custom Output Directory

```bash
# Specify where to save results
python backend/scripts/run_week1_pipeline.py \
  --input-dir mechanism-bank/mechanisms/obesity/ \
  --output-dir mechanism-bank/mvp/obesity/
```

## Individual Components

If you want to run components separately:

### 1. Deduplication Only

```python
from backend.pipelines.mechanism_deduplication import MechanismDeduplicator

deduplicator = MechanismDeduplicator()
deduplicated, stats = deduplicator.deduplicate_from_files(
    mechanism_dir="mechanism-bank/mechanisms/obesity/",
    output_dir="mechanism-bank/mechanisms/obesity_dedup/",
    verbose=True
)

print(f"Reduction: {stats['reduction_pct']:.1f}%")
```

### 2. Functional Form Classification Only

```python
from backend.algorithms.functional_form_classifier import FunctionalFormClassifier
import yaml

classifier = FunctionalFormClassifier()

# Load mechanism
with open("mechanism.yml", 'r') as f:
    mechanism = yaml.safe_load(f)

# Classify
assignment = classifier.classify(mechanism, verbose=True)

# Apply to mechanism
updated_mechanism = classifier.apply_to_mechanism(mechanism, assignment)

print(f"Form: {assignment.form} (confidence: {assignment.confidence:.2f})")
```

### 3. Schema Validation Only

```bash
# Validate single file
python backend/scripts/validate_mechanism_schema.py \
  --file mechanism.yml

# Validate directory
python backend/scripts/validate_mechanism_schema.py \
  --dir mechanism-bank/mechanisms/obesity/

# Strict mode (warnings as errors)
python backend/scripts/validate_mechanism_schema.py \
  --dir mechanism-bank/mechanisms/ \
  --strict
```

### 4. Bidirectional Detection Only

```bash
# Detect bidirectional pairs in directory
python backend/scripts/create_bidirectional_pairs.py \
  --input-dir mechanism-bank/mechanisms/obesity/

# Single mechanism
python backend/scripts/create_bidirectional_pairs.py \
  --mechanism mechanism.yml \
  --output-dir mechanism-bank/mechanisms/

# Only assess plausibility (no literature search)
python backend/scripts/create_bidirectional_pairs.py \
  --input-dir mechanism-bank/mechanisms/obesity/ \
  --no-search
```

## Expected Output

### Console Output

```
=== Initializing Week 1 Pipeline Components ===
✓ Deduplicator initialized
✓ Functional form classifier initialized
✓ Schema validator initialized
✓ Bidirectional detector initialized

============================================================
WEEK 1 PIPELINE: mechanism-bank/mechanisms/obesity
============================================================

============================================================
STEP 1: DEDUPLICATION
============================================================
Loading mechanisms from: mechanism-bank/mechanisms/obesity
Loaded 250 mechanisms

Step 1: Embedding mechanism descriptions...
Step 2: Clustering with DBSCAN (eps=0.15)...
  Found 85 clusters
  32 clusters with 2+ mechanisms (need LLM review)

Step 3: LLM consolidation...
  Reviewing cluster 1 (3 mechanisms)...
    Decision: MERGE
  ...

✓ Deduplication complete:
  Input: 250 mechanisms
  Output: 152 mechanisms
  Reduction: 39.2%

============================================================
STEP 2: FUNCTIONAL FORM CLASSIFICATION
============================================================
  food_insecurity → obesity_prevalence: sigmoid (conf: 0.87)
  built_environment → physical_activity: logarithmic (conf: 0.82)
  ...

✓ Classification complete: 152 mechanisms classified

============================================================
STEP 3: SCHEMA VALIDATION
============================================================
  ✗ INVALID: missing_field → outcome
    - Missing required field: parameters
  ...

✓ Validation complete:
  Valid: 148 mechanisms
  Invalid: 4 mechanisms

============================================================
STEP 4: BIDIRECTIONAL DETECTION
============================================================
  ✓ Bidirectional pair: healthcare_continuity ↔ healthcare_seeking
  ✓ Bidirectional pair: ed_utilization ↔ hospital_capacity
  ...

✓ Bidirectional detection complete:
  Pairs created: 12

============================================================
STEP 5: SAVING RESULTS
============================================================
✓ Saved 160 mechanisms to: mechanism-bank/mechanisms/obesity_processed
✓ Saved invalid mechanisms report to: invalid_mechanisms_report.txt

============================================================
PIPELINE SUMMARY
============================================================

Input:  250 raw mechanisms

Step 1 (Deduplication):  152 mechanisms (39.2% reduction)
Step 2 (Classification): 152 mechanisms
Step 3 (Validation):     148 valid, 4 invalid
Step 4 (Bidirectional):  +12 reverse mechanisms

Final Output: 160 MVP-ready mechanisms

Saved to: mechanism-bank/mechanisms/obesity_processed

✓ Pipeline complete!
```

### File Output

```
mechanism-bank/mechanisms/obesity_processed/
├── behavioral/
│   ├── physical_activity_to_obesity_prevalence.yml
│   ├── diet_quality_to_bmi_continuous.yml
│   └── ...
├── economic/
│   ├── food_insecurity_to_obesity_prevalence.yml
│   ├── income_to_healthcare_access.yml
│   └── healthcare_continuity_to_healthcare_seeking_backward.yml  # Reverse mechanism
├── built_environment/
│   ├── food_environment_to_diet_quality.yml
│   └── ...
└── invalid_mechanisms_report.txt
```

**Each mechanism YAML will have**:
- ✅ `functional_form`: sigmoid, threshold, logarithmic, etc.
- ✅ `equation`: Mathematical equation
- ✅ `parameters`: alpha, L, k, x0, etc. with descriptions
- ✅ `direction`: forward, backward, or horizontal
- ✅ Valid schema (passes Doc 05 validation)

## Cost Estimates

**For ~250 mechanisms**:

| Step | API Calls | Est. Cost |
|------|-----------|-----------|
| Deduplication | ~50-100 | $5-$15 |
| Classification | ~150 | $15-$30 |
| Bidirectional | ~150 | $15-$30 |
| **Total** | **~350-400** | **$35-$75** |

**Notes**:
- Deduplication only calls LLM for multi-mechanism clusters (~30-40%)
- Skip bidirectional with `--skip-bidirectional` to save ~$15-30
- Costs assume Claude Sonnet 4.5 ($3/M input, $15/M output)

## Troubleshooting

### "ANTHROPIC_API_KEY not set"
```bash
# Set environment variable
export ANTHROPIC_API_KEY=your-key-here  # Linux/Mac
set ANTHROPIC_API_KEY=your-key-here     # Windows
```

### "No module named 'sentence_transformers'"
```bash
pip install sentence-transformers scikit-learn
```

### "ModuleNotFoundError: No module named 'backend'"
```bash
# Run from project root
cd healthsystems/
python backend/scripts/run_week1_pipeline.py --input-dir ...
```

### Pipeline takes too long
```bash
# Skip bidirectional detection (saves 40-50% time)
python backend/scripts/run_week1_pipeline.py \
  --input-dir mechanisms/ \
  --skip-bidirectional
```

### Too many invalid mechanisms
- Check that input mechanisms have basic required fields (from_node_id, to_node_id, description)
- Review `invalid_mechanisms_report.txt` for specific errors
- Use schema validator separately to identify issues:
  ```bash
  python backend/scripts/validate_mechanism_schema.py --file mechanism.yml
  ```

## Next Steps After Pipeline

1. **Review Output**:
   ```bash
   # Check valid mechanisms
   ls mechanism-bank/mechanisms/obesity_processed/

   # Review invalid mechanisms
   cat mechanism-bank/mechanisms/obesity_processed/invalid_mechanisms_report.txt
   ```

2. **Validate Schema**:
   ```bash
   python backend/scripts/validate_mechanism_schema.py \
     --dir mechanism-bank/mechanisms/obesity_processed/ \
     --strict
   ```

3. **Manual Review**:
   - Check functional form assignments make sense
   - Review bidirectional pairs for feedback loop validity
   - Verify parameters are reasonable

4. **Load to Database** (Week 3):
   - Create database tables
   - Write loader script
   - Import MVP-ready mechanisms

## Full Week 2 Workflow

```bash
# 1. Extract mechanisms for topic
python backend/scripts/run_generic_extraction_enhanced.py \
  --topic obesity \
  --limit 10 \
  --extract-all-metrics

# 2. Process with Week 1 pipeline
python backend/scripts/run_week1_pipeline.py \
  --input-dir mechanism-bank/mechanisms/obesity/

# 3. Validate output
python backend/scripts/validate_mechanism_schema.py \
  --dir mechanism-bank/mechanisms/obesity_processed/ \
  --strict

# 4. Review and iterate
# - Fix any validation errors
# - Re-run pipeline if needed
```

## Documentation

- **Full implementation details**: [WEEK1_IMPLEMENTATION_COMPLETE.md](WEEK1_IMPLEMENTATION_COMPLETE.md)
- **Alignment analysis**: [ALIGNMENT_AND_NEXT_STEPS.md](ALIGNMENT_AND_NEXT_STEPS.md)
- **Extraction guide**: [QUICK_START_GENERIC_EXTRACTION.md](QUICK_START_GENERIC_EXTRACTION.md)
- **Schema reference**: [docs/Core Technical Architecture/05_MECHANISM_BANK_STRUCTURE.md](docs/Core%20Technical%20Architecture/05_MECHANISM_BANK_STRUCTURE.md)

## Support

For issues:
1. Check [WEEK1_IMPLEMENTATION_COMPLETE.md](WEEK1_IMPLEMENTATION_COMPLETE.md) for detailed component documentation
2. Review error messages in console output
3. Check `invalid_mechanisms_report.txt` for validation issues
4. Use `--dry-run` to test before full run
