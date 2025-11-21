# Core Business Logic

Unified core modules for node classification and mechanism grading operations.

## Architecture

```
core/
├── __init__.py                # Module exports
├── node_classification.py     # Node scale classification
└── mechanism_grading.py       # Evidence quality grading
```

## Node Classification

### NodeClassifier

Handles node reclassification, scale validation, and migration across the 7-scale system:

1. Structural Determinants (policy, law)
2. Built Environment & Infrastructure
3. Institutional Infrastructure
4. Individual/Household Conditions
5. Individual Health Behaviors
6. Biological/Physiological Processes
7. Health Outcomes & Crisis Endpoints

### Usage Examples

**Auto-classify all nodes by keywords:**
```bash
python scripts/classify_nodes.py reclassify --auto --dry-run
```

**Migrate nodes from scale 2 to scale 3:**
```bash
python scripts/classify_nodes.py reclassify --migrate 2 3
```

**Show node scale distribution:**
```bash
python scripts/classify_nodes.py stats --type nodes
```

**Python API:**
```python
from core import NodeClassifier
from models import get_db

db = next(get_db())
classifier = NodeClassifier(db, dry_run=True)

# Auto-classify all nodes
results = classifier.auto_classify_all()

# Migrate scale
results = classifier.migrate_scale_range(old_scale=2, new_scale=3)

# Get statistics
stats = classifier.get_scale_distribution()

classifier.commit()
classifier.stats.print_summary()
```

## Mechanism Grading

### MechanismGrader

Assesses and updates evidence quality ratings based on:
- Number of supporting studies
- DOI availability
- Citation quality
- Supporting evidence

**Grading Criteria:**
- **Grade A**: 10+ studies with DOI
- **Grade B**: 3-9 studies with primary citation, or strong single study with support
- **Grade C**: Limited evidence

### Usage Examples

**Regrade all mechanisms:**
```bash
python scripts/classify_nodes.py regrade --dry-run
```

**Regrade specific category:**
```bash
python scripts/classify_nodes.py regrade --category economic
```

**Show grade distribution:**
```bash
python scripts/classify_nodes.py stats --type mechanisms
```

**Python API:**
```python
from core import MechanismGrader
from models import get_db

db = next(get_db())
grader = MechanismGrader(db, dry_run=True)

# Regrade all mechanisms
results = grader.regrade_all()

# Regrade specific category
results = grader.regrade_category("economic")

# Get statistics
stats = grader.get_grade_distribution()

grader.commit()
grader.stats.print_summary()
```

## Migration from Old Scripts

### Old → New Command Mapping

**reclassify_nodes_v2.py** →
```bash
python scripts/classify_nodes.py reclassify --auto
```

**apply_node_reclassification.py** →
```bash
python scripts/classify_nodes.py reclassify --migrate <from> <to>
```

**aggressive_redistribution.py** →
```bash
# Use Python API for custom distributions
from core import NodeClassifier
classifier.redistribute_scale(target_scale, distribution_dict)
```

**regrade_mechanisms.py** →
```bash
python scripts/classify_nodes.py regrade
```

## Benefits

- **876 LOC eliminated**: 1,576 → 700 lines
- **Single source of truth**: All classification logic centralized
- **Consistent behavior**: No diverging implementations
- **Dry-run support**: Preview changes before committing
- **Better testing**: Clean module structure
- **Flexible API**: Use as CLI or import as library
