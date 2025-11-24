# PROMPT 1: Consolidate Extraction Scripts

## Context
The codebase contains **6 duplicate extraction scripts** with 85-95% code overlap, totaling **1,816 lines of code**. Each script reimplements the same core functionality: LLM prompting, mechanism extraction, YAML serialization, and error handling. This redundancy creates maintenance burden and inconsistent behavior.

## Current State

### Files to Consolidate (1,816 LOC → 500 LOC target)

**Topic-specific scripts:**
- `backend/scripts/run_alcohol_extraction.py` (112 LOC)
- `backend/scripts/batch_alcohol_mechanisms.py` (737 LOC)
- `backend/scripts/test_extraction.py` (112 LOC)

**Generic scripts:**
- `backend/scripts/run_generic_extraction.py` (350 LOC)
- `backend/scripts/batch_topic_extraction.py` (332 LOC)
- `backend/scripts/example_generic_extraction.py` (173 LOC)

### Redundancy Examples

**Example 1: LLM Client Setup (duplicated 6 times)**
```python
# run_alcohol_extraction.py (lines 23-28)
client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
response = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=16000,
    temperature=0.0,
    messages=[{"role": "user", "content": prompt}]
)

# batch_topic_extraction.py (lines 156-161) - IDENTICAL
client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
response = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=16000,
    temperature=0.0,
    messages=[{"role": "user", "content": prompt}]
)
```

**Example 2: YAML Writing (duplicated 6 times)**
```python
# run_generic_extraction.py (lines 89-97)
output_dir = Path("mechanism-bank/mechanisms") / category
output_dir.mkdir(parents=True, exist_ok=True)
output_file = output_dir / f"{mechanism['id']}.yml"
with open(output_file, 'w', encoding='utf-8') as f:
    yaml.dump(mechanism, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

# batch_alcohol_mechanisms.py (lines 201-209) - IDENTICAL
output_dir = Path("mechanism-bank/mechanisms") / category
output_dir.mkdir(parents=True, exist_ok=True)
output_file = output_dir / f"{mechanism['id']}.yml"
with open(output_file, 'w', encoding='utf-8') as f:
    yaml.dump(mechanism, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
```

**Example 3: Progress Tracking (duplicated 5 times)**
```python
# batch_topic_extraction.py (lines 223-234)
print(f"\n{'='*60}")
print(f"BATCH EXTRACTION COMPLETE")
print(f"{'='*60}")
print(f"Total mechanisms extracted: {total_extracted}")
print(f"Total errors: {total_errors}")
print(f"Success rate: {success_rate:.1f}%")

# batch_alcohol_mechanisms.py (lines 267-278) - IDENTICAL
print(f"\n{'='*60}")
print(f"BATCH EXTRACTION COMPLETE")
print(f"{'='*60}")
print(f"Total mechanisms extracted: {total_extracted}")
print(f"Total errors: {total_errors}")
print(f"Success rate: {success_rate:.1f}%")
```

## Target Architecture

```
backend/
├── extraction/
│   ├── __init__.py                    # Module exports
│   ├── core.py                        # 200 LOC - Core extraction logic
│   │   ├── MechanismExtractor         # Main extractor class
│   │   ├── extract_mechanisms()       # Single mechanism extraction
│   │   └── batch_extract()            # Batch extraction
│   │
│   ├── llm_client.py                  # 80 LOC - LLM interaction
│   │   ├── create_llm_client()
│   │   ├── call_llm()
│   │   └── parse_llm_response()
│   │
│   ├── yaml_handler.py                # 60 LOC - YAML I/O
│   │   ├── write_mechanism_yaml()
│   │   ├── read_mechanism_yaml()
│   │   └── validate_mechanism_schema()
│   │
│   ├── prompts.py                     # 100 LOC - Prompt templates
│   │   ├── GENERIC_EXTRACTION_PROMPT
│   │   ├── TOPIC_EXTRACTION_PROMPT
│   │   └── build_extraction_prompt()
│   │
│   └── progress.py                    # 60 LOC - Progress tracking
│       ├── ExtractionProgress
│       └── print_summary()
│
└── scripts/
    ├── extract_mechanisms.py          # 50 LOC - Unified CLI entry point
    └── (delete 6 old scripts)
```

## Implementation Steps

### Step 1: Create Core Extraction Module

**File: `backend/extraction/core.py`**

```python
"""
Core mechanism extraction logic.
Unified interface for single and batch extraction.
"""
from pathlib import Path
from typing import List, Dict, Optional, Callable
from dataclasses import dataclass
import json

from .llm_client import LLMClient
from .yaml_handler import write_mechanism_yaml
from .prompts import build_extraction_prompt
from .progress import ExtractionProgress


@dataclass
class ExtractionConfig:
    """Configuration for mechanism extraction."""
    topic: str
    category: str
    source_context: str
    output_dir: Path = Path("mechanism-bank/mechanisms")
    model: str = "claude-3-5-sonnet-20241022"
    max_tokens: int = 16000
    temperature: float = 0.0
    max_retries: int = 3


class MechanismExtractor:
    """
    Unified mechanism extraction engine.
    Handles both single and batch extractions.
    """

    def __init__(self, config: ExtractionConfig):
        self.config = config
        self.llm_client = LLMClient(
            model=config.model,
            max_tokens=config.max_tokens,
            temperature=config.temperature
        )
        self.progress = ExtractionProgress()

    def extract_single(
        self,
        from_node: str,
        to_node: str,
        context: Optional[str] = None
    ) -> Optional[Dict]:
        """
        Extract a single mechanism between two nodes.

        Args:
            from_node: Source node identifier
            to_node: Target node identifier
            context: Optional additional context

        Returns:
            Mechanism dict or None if extraction failed
        """
        # Build prompt
        prompt = build_extraction_prompt(
            topic=self.config.topic,
            category=self.config.category,
            from_node=from_node,
            to_node=to_node,
            source_context=context or self.config.source_context
        )

        # Call LLM with retries
        for attempt in range(self.config.max_retries):
            try:
                response = self.llm_client.call(prompt)
                mechanism = self._parse_response(response)

                if mechanism:
                    self.progress.record_success()
                    return mechanism

            except Exception as e:
                self.progress.record_error(str(e))
                if attempt == self.config.max_retries - 1:
                    print(f"Failed after {self.config.max_retries} attempts: {e}")
                    return None

        return None

    def extract_batch(
        self,
        node_pairs: List[tuple[str, str]],
        on_progress: Optional[Callable[[int, int], None]] = None
    ) -> List[Dict]:
        """
        Extract multiple mechanisms in batch.

        Args:
            node_pairs: List of (from_node, to_node) tuples
            on_progress: Optional callback for progress updates

        Returns:
            List of successfully extracted mechanisms
        """
        mechanisms = []

        for i, (from_node, to_node) in enumerate(node_pairs):
            mechanism = self.extract_single(from_node, to_node)

            if mechanism:
                mechanisms.append(mechanism)
                # Write immediately to avoid data loss
                self._write_mechanism(mechanism)

            # Progress callback
            if on_progress:
                on_progress(i + 1, len(node_pairs))

        return mechanisms

    def _parse_response(self, response: str) -> Optional[Dict]:
        """Parse LLM response into mechanism dict."""
        try:
            # Extract JSON from response
            start = response.find('{')
            end = response.rfind('}') + 1
            if start == -1 or end == 0:
                return None

            mechanism = json.loads(response[start:end])

            # Validate required fields
            required = ['id', 'name', 'from_node', 'to_node', 'category', 'direction']
            if not all(field in mechanism for field in required):
                return None

            return mechanism

        except json.JSONDecodeError:
            return None

    def _write_mechanism(self, mechanism: Dict):
        """Write mechanism to YAML file."""
        category_dir = self.config.output_dir / self.config.category
        write_mechanism_yaml(mechanism, category_dir)

    def get_summary(self) -> Dict:
        """Get extraction summary statistics."""
        return self.progress.get_summary()
```

### Step 2: Create LLM Client Module

**File: `backend/extraction/llm_client.py`**

```python
"""
LLM client for mechanism extraction.
Handles API calls to Anthropic Claude.
"""
import os
from anthropic import Anthropic
from typing import Optional


class LLMClient:
    """Wrapper for Anthropic Claude API."""

    def __init__(
        self,
        model: str = "claude-3-5-sonnet-20241022",
        max_tokens: int = 16000,
        temperature: float = 0.0,
        api_key: Optional[str] = None
    ):
        self.model = model
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.client = Anthropic(api_key=api_key or os.environ.get("ANTHROPIC_API_KEY"))

    def call(self, prompt: str) -> str:
        """
        Call LLM with prompt and return response text.

        Args:
            prompt: Input prompt

        Returns:
            Response text content

        Raises:
            Exception: If API call fails
        """
        response = self.client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            messages=[{"role": "user", "content": prompt}]
        )

        return response.content[0].text
```

### Step 3: Create YAML Handler Module

**File: `backend/extraction/yaml_handler.py`**

```python
"""
YAML file handling for mechanism storage.
Handles reading, writing, and validation.
"""
from pathlib import Path
from typing import Dict, Optional
import yaml


def write_mechanism_yaml(mechanism: Dict, category_dir: Path) -> Path:
    """
    Write mechanism to YAML file.

    Args:
        mechanism: Mechanism dict with 'id' and 'category'
        category_dir: Category directory path

    Returns:
        Path to written file
    """
    # Create category directory
    category_dir.mkdir(parents=True, exist_ok=True)

    # Generate filename from mechanism ID
    output_file = category_dir / f"{mechanism['id']}.yml"

    # Write YAML with proper formatting
    with open(output_file, 'w', encoding='utf-8') as f:
        yaml.dump(
            mechanism,
            f,
            default_flow_style=False,
            allow_unicode=True,
            sort_keys=False,
            width=120
        )

    return output_file


def read_mechanism_yaml(yaml_file: Path) -> Optional[Dict]:
    """
    Read mechanism from YAML file.

    Args:
        yaml_file: Path to YAML file

    Returns:
        Mechanism dict or None if read fails
    """
    try:
        with open(yaml_file, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"Error reading {yaml_file}: {e}")
        return None


def validate_mechanism_schema(mechanism: Dict) -> tuple[bool, Optional[str]]:
    """
    Validate mechanism has required fields.

    Args:
        mechanism: Mechanism dict to validate

    Returns:
        (is_valid, error_message)
    """
    required_fields = [
        'id', 'name', 'from_node', 'to_node',
        'category', 'direction', 'evidence'
    ]

    for field in required_fields:
        if field not in mechanism:
            return False, f"Missing required field: {field}"

    # Validate nested structures
    if not isinstance(mechanism.get('from_node'), dict):
        return False, "from_node must be a dict"

    if not isinstance(mechanism.get('to_node'), dict):
        return False, "to_node must be a dict"

    if 'node_id' not in mechanism['from_node']:
        return False, "from_node missing node_id"

    if 'node_id' not in mechanism['to_node']:
        return False, "to_node missing node_id"

    return True, None
```

### Step 4: Create Prompts Module

**File: `backend/extraction/prompts.py`**

```python
"""
Prompt templates for mechanism extraction.
"""

GENERIC_EXTRACTION_PROMPT = """You are an expert in social epidemiology and public health systems.

Extract a causal mechanism from the following context.

TOPIC: {topic}
CATEGORY: {category}
FROM NODE: {from_node}
TO NODE: {to_node}

CONTEXT:
{source_context}

Return a valid JSON object with this exact structure:
{{
  "id": "unique_mechanism_id",
  "name": "Brief descriptive name",
  "from_node": {{
    "node_id": "{from_node}",
    "node_name": "Full name"
  }},
  "to_node": {{
    "node_id": "{to_node}",
    "node_name": "Full name"
  }},
  "category": "{category}",
  "direction": "positive or negative",
  "mechanism_pathway": ["step 1", "step 2", "step 3"],
  "evidence": {{
    "quality_rating": "A, B, or C",
    "n_studies": 0,
    "primary_citation": "Author et al. (Year). Title. Journal.",
    "supporting_citations": ["Citation 1", "Citation 2"],
    "doi": "10.xxxx/xxxxx"
  }},
  "description": "Detailed description of the mechanism"
}}
"""


def build_extraction_prompt(
    topic: str,
    category: str,
    from_node: str,
    to_node: str,
    source_context: str
) -> str:
    """
    Build extraction prompt from template.

    Args:
        topic: Topic area (e.g., "Alcoholism", "Obesity")
        category: Mechanism category
        from_node: Source node ID
        to_node: Target node ID
        source_context: Background context/literature

    Returns:
        Formatted prompt string
    """
    return GENERIC_EXTRACTION_PROMPT.format(
        topic=topic,
        category=category,
        from_node=from_node,
        to_node=to_node,
        source_context=source_context
    )
```

### Step 5: Create Progress Tracking Module

**File: `backend/extraction/progress.py`**

```python
"""
Progress tracking for extraction jobs.
"""
from dataclasses import dataclass, field
from typing import List
import time


@dataclass
class ExtractionProgress:
    """Tracks progress and errors during extraction."""

    start_time: float = field(default_factory=time.time)
    success_count: int = 0
    error_count: int = 0
    errors: List[str] = field(default_factory=list)

    def record_success(self):
        """Record a successful extraction."""
        self.success_count += 1

    def record_error(self, error: str):
        """Record an extraction error."""
        self.error_count += 1
        self.errors.append(error)

    def get_summary(self) -> dict:
        """Get summary statistics."""
        total = self.success_count + self.error_count
        success_rate = (self.success_count / total * 100) if total > 0 else 0
        duration = time.time() - self.start_time

        return {
            "total": total,
            "success": self.success_count,
            "errors": self.error_count,
            "success_rate": success_rate,
            "duration_seconds": duration
        }

    def print_summary(self):
        """Print formatted summary."""
        summary = self.get_summary()

        print(f"\n{'='*60}")
        print(f"EXTRACTION COMPLETE")
        print(f"{'='*60}")
        print(f"Total: {summary['total']}")
        print(f"Successful: {summary['success']}")
        print(f"Errors: {summary['errors']}")
        print(f"Success rate: {summary['success_rate']:.1f}%")
        print(f"Duration: {summary['duration_seconds']:.1f}s")

        if self.errors:
            print(f"\nError details:")
            for i, error in enumerate(self.errors[:5], 1):
                print(f"  {i}. {error}")
            if len(self.errors) > 5:
                print(f"  ... and {len(self.errors) - 5} more")
```

### Step 6: Create Unified CLI Entry Point

**File: `backend/scripts/extract_mechanisms.py`**

```python
#!/usr/bin/env python3
"""
Unified CLI for mechanism extraction.
Replaces 6 separate extraction scripts.
"""
import argparse
from pathlib import Path
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from extraction.core import MechanismExtractor, ExtractionConfig


def main():
    parser = argparse.ArgumentParser(
        prog='extract_mechanisms',
        description='Extract causal mechanisms using LLM'
    )

    # Required arguments
    parser.add_argument('topic', help='Topic area (e.g., Alcoholism)')
    parser.add_argument('category', help='Mechanism category')
    parser.add_argument('--from-node', required=True, help='Source node')
    parser.add_argument('--to-node', required=True, help='Target node')

    # Optional arguments
    parser.add_argument('--context', help='Source context/literature')
    parser.add_argument('--context-file', help='File containing context')
    parser.add_argument('--output-dir', default='mechanism-bank/mechanisms', help='Output directory')
    parser.add_argument('--model', default='claude-3-5-sonnet-20241022', help='LLM model')
    parser.add_argument('--batch', help='CSV file with node pairs for batch extraction')

    args = parser.parse_args()

    # Load context
    if args.context_file:
        with open(args.context_file, 'r') as f:
            context = f.read()
    else:
        context = args.context or ""

    # Create config
    config = ExtractionConfig(
        topic=args.topic,
        category=args.category,
        source_context=context,
        output_dir=Path(args.output_dir),
        model=args.model
    )

    # Create extractor
    extractor = MechanismExtractor(config)

    # Single or batch extraction
    if args.batch:
        # Batch mode
        import csv
        with open(args.batch, 'r') as f:
            reader = csv.DictReader(f)
            node_pairs = [(row['from_node'], row['to_node']) for row in reader]

        print(f"Starting batch extraction of {len(node_pairs)} mechanisms...")

        def progress_callback(current, total):
            print(f"Progress: {current}/{total} ({current/total*100:.1f}%)")

        extractor.extract_batch(node_pairs, on_progress=progress_callback)

    else:
        # Single mode
        print(f"Extracting mechanism: {args.from_node} → {args.to_node}")
        mechanism = extractor.extract_single(args.from_node, args.to_node)

        if mechanism:
            print(f"✓ Success! Mechanism ID: {mechanism['id']}")
        else:
            print(f"✗ Extraction failed")
            sys.exit(1)

    # Print summary
    extractor.progress.print_summary()


if __name__ == "__main__":
    main()
```

### Step 7: Create Package Init

**File: `backend/extraction/__init__.py`**

```python
"""
Mechanism extraction framework.
Unified interface for LLM-based causal mechanism discovery.
"""
from .core import MechanismExtractor, ExtractionConfig
from .llm_client import LLMClient
from .yaml_handler import write_mechanism_yaml, read_mechanism_yaml
from .prompts import build_extraction_prompt

__all__ = [
    'MechanismExtractor',
    'ExtractionConfig',
    'LLMClient',
    'write_mechanism_yaml',
    'read_mechanism_yaml',
    'build_extraction_prompt',
]
```

## Migration Checklist

### Phase 1: Setup (Day 1)
- [ ] Create `backend/extraction/` directory
- [ ] Create all module files with code above
- [ ] Create unified CLI script
- [ ] Test imports: `python -c "from extraction import MechanismExtractor"`

### Phase 2: Testing (Day 1-2)
- [ ] Test single extraction: `python scripts/extract_mechanisms.py Alcoholism economic --from-node SES --to-node health`
- [ ] Test batch extraction with small CSV (3-5 mechanisms)
- [ ] Verify YAML output matches old format
- [ ] Compare output quality with old scripts

### Phase 3: Migration (Day 2)
- [ ] Update documentation to reference new CLI
- [ ] Create migration guide for existing workflows
- [ ] Update any CI/CD scripts that call old scripts

### Phase 4: Cleanup (Day 2)
- [ ] Delete 6 old extraction scripts:
  - `run_alcohol_extraction.py`
  - `batch_alcohol_mechanisms.py`
  - `test_extraction.py`
  - `run_generic_extraction.py`
  - `batch_topic_extraction.py`
  - `example_generic_extraction.py`
- [ ] Update `.gitignore` if needed
- [ ] Commit with message: "refactor: consolidate 6 extraction scripts into unified framework"

## Testing Requirements

### Unit Tests
Create `backend/extraction/tests/test_core.py`:

```python
import pytest
from extraction.core import MechanismExtractor, ExtractionConfig

def test_extraction_config_defaults():
    config = ExtractionConfig(
        topic="Test",
        category="economic",
        source_context="Test context"
    )
    assert config.model == "claude-3-5-sonnet-20241022"
    assert config.max_tokens == 16000

def test_extractor_initialization():
    config = ExtractionConfig(
        topic="Test",
        category="economic",
        source_context="Test"
    )
    extractor = MechanismExtractor(config)
    assert extractor.config == config
    assert extractor.llm_client is not None
```

### Integration Test
```bash
# Test single extraction
python scripts/extract_mechanisms.py \
  "Alcoholism" "economic" \
  --from-node "low_income" \
  --to-node "alcohol_use_disorder" \
  --context "Economic hardship increases stress..."

# Verify output
ls mechanism-bank/mechanisms/economic/
cat mechanism-bank/mechanisms/economic/low_income_to_alcohol_use_disorder.yml
```

## Success Criteria

- ✅ All 6 old scripts deleted
- ✅ Single unified CLI works for all use cases
- ✅ YAML output format unchanged
- ✅ Batch extraction matches old behavior
- ✅ Error handling preserved
- ✅ Progress tracking working
- ✅ Documentation updated
- ✅ **1,316 LOC eliminated** (1,816 → 500)

## Estimated Effort
**2 days** (1 day implementation, 1 day testing/migration)
