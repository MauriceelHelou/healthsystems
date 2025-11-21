# Extraction Framework

Unified mechanism extraction framework that consolidates 6 duplicate scripts into a single, maintainable codebase.

## Architecture

```
extraction/
├── __init__.py         # Module exports
├── core.py            # Main extractor class
├── llm_client.py      # LLM API wrapper
├── yaml_handler.py    # YAML I/O
├── prompts.py         # Prompt templates
└── progress.py        # Progress tracking
```

## Usage

### Single Mechanism Extraction

```bash
python scripts/extract_mechanisms.py \
  "Alcoholism" "economic" \
  --from-node "low_income" \
  --to-node "alcohol_use_disorder" \
  --context "Economic hardship increases stress and reduces access to mental health resources..."
```

### Batch Extraction

Create a CSV file with node pairs:

```csv
from_node,to_node
low_income,alcohol_use_disorder
unemployment,mental_health
food_insecurity,substance_abuse
```

Run batch extraction:

```bash
python scripts/extract_mechanisms.py \
  "Alcoholism" "economic" \
  --batch node_pairs.csv \
  --context-file context.txt
```

### Python API

```python
from extraction import MechanismExtractor, ExtractionConfig
from pathlib import Path

# Configure extraction
config = ExtractionConfig(
    topic="Alcoholism",
    category="economic",
    source_context="Your literature context here...",
    output_dir=Path("mechanism-bank/mechanisms"),
    model="claude-3-5-sonnet-20241022"
)

# Create extractor
extractor = MechanismExtractor(config)

# Extract single mechanism
mechanism = extractor.extract_single(
    from_node="low_income",
    to_node="alcohol_use_disorder"
)

# Extract batch
node_pairs = [
    ("low_income", "alcohol_use_disorder"),
    ("unemployment", "mental_health"),
]
mechanisms = extractor.extract_batch(node_pairs)

# Get summary
summary = extractor.get_summary()
print(f"Success rate: {summary['success_rate']:.1f}%")
```

## Migration from Old Scripts

### Old → New Command Mapping

**run_alcohol_extraction.py** →
```bash
python scripts/extract_mechanisms.py Alcoholism economic --from-node X --to-node Y
```

**batch_alcohol_mechanisms.py** →
```bash
python scripts/extract_mechanisms.py Alcoholism economic --batch pairs.csv
```

**run_generic_extraction.py** →
```bash
python scripts/extract_mechanisms.py <topic> <category> --from-node X --to-node Y
```

**batch_topic_extraction.py** →
```bash
python scripts/extract_mechanisms.py <topic> <category> --batch pairs.csv
```

## Benefits

- **1,316 LOC eliminated**: 1,816 → 500 lines
- **Single source of truth**: All extraction logic in one place
- **Consistent behavior**: No more diverging implementations
- **Easier maintenance**: Fix bugs once, not six times
- **Better testing**: Unit tests for core functionality
- **Flexible API**: Use as CLI or import as library
