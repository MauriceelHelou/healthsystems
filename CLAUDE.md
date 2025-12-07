# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

HealthSystems Platform is a decision support tool for quantifying how structural interventions propagate through social-spatial-biological systems to affect health outcomes. It focuses on **structural determinants of health** - policy, housing, economic systems - not individual behavior change.

## Build & Run Commands

### Backend (Python/FastAPI)
```bash
cd backend
pip install -r requirements.txt          # Install dependencies
uvicorn api.main:app --reload             # Run API server (http://localhost:8000)
pytest tests/ --cov=. --cov-report=html   # Run tests with coverage
black . && isort .                        # Format code
```

### Frontend (React/TypeScript)
```bash
cd frontend
npm install                    # Install dependencies
npm run dev                    # Dev server (http://localhost:3000)
npm test                       # Run Jest tests
npm run test:e2e               # Run Playwright E2E tests
npm run lint && npm run format # Lint and format
npm run type-check             # TypeScript check
```

### CLI Commands
```bash
python -m backend.cli.main classify <file> --dry-run   # Classify nodes
python -m backend.cli.main extract generic --config config.json
python -m backend.cli.main validate mechanism-bank/mechanisms/
python -m backend.cli.main regrade --input mechanism-bank/ --dry-run
```

### Mechanism Validation
```bash
python backend/scripts/validate_mechanism_schema.py    # Validate all YAML files
python mechanism-bank/validation/validate_mechanisms.py --file <specific_file>
```

## Architecture

### Three-Tier Structure

1. **Backend** (`backend/`)
   - FastAPI REST API (`api/main.py`, `api/routes/`)
   - Bayesian weighting algorithms (`algorithms/bayesian_weighting.py`)
   - LLM mechanism discovery pipeline (`pipelines/llm_mechanism_discovery.py`)
   - SQLAlchemy models with PostgreSQL (`models/database.py`)
   - CLI tools (`cli/main.py`)

2. **Frontend** (`frontend/src/`)
   - React 18 with TypeScript and TailwindCSS
   - Cytoscape.js for graph visualization (`visualizations/MechanismGraph.tsx`)
   - React Query for data fetching (`hooks/useData.ts`)
   - Zustand for state management (`stores/`)
   - Key views: `SystemsMapView`, `AlcoholismSystemView`, `PathfinderView`

3. **Mechanism Bank** (`mechanism-bank/`)
   - YAML files storing causal pathways with effect sizes and citations
   - Categories: `built_environment/`, `social_environment/`, `economic/`, `political/`, `healthcare_access/`, `biological/`
   - JSON schema validation (`schemas/`)

### Data Flow
```
Literature APIs (Semantic Scholar, PubMed)
  → Full-Text Fetcher (Unpaywall, PMC, Elsevier, Wiley, etc.)
  → LLM Extraction (Claude)
  → Mechanism YAML files
  → SQLite/PostgreSQL database
  → FastAPI endpoints
  → React frontend visualization
```

### Full-Text Paper Access (V3)

The pipeline now includes multi-source full-text retrieval via `backend/utils/fulltext_fetcher.py`:

| Source | Type | Coverage |
|--------|------|----------|
| Unpaywall | Open Access | 30-40% of papers |
| PubMed Central | NIH OA | 20-30% (health research) |
| Europe PMC | European OA | 10-15% |
| CORE | Repository aggregator | 15-20% |
| OpenAlex | Metadata + OA links | 225M+ works |
| Elsevier | Publisher API | Institutional access |
| Wiley TDM | Publisher API | Institutional access |
| Harvard Proxy | Fallback | Manual browser access |

See `docs/LLM & Discovery Pipeline/FULLTEXT_API_INTEGRATION.md` for details.

## Key Concepts

### Structural Competency
- **DO**: Focus on policy, institutional, environmental interventions
- **DON'T**: Frame mechanisms around individual compliance, behavior, or "cultural factors"
- Example: "Housing code enforcement → indoor air quality → respiratory health" (structural)
- Anti-example: "Patient non-compliance → poor outcomes" (individual blame)

### Mechanism Schema (MVP)
```yaml
id: from_node_to_node
from_node: { node_id, node_name }
to_node: { node_id, node_name }
direction: positive|negative      # positive: A↑→B↑; negative: A↑→B↓
category: built_environment|economic|political|...
evidence:
  quality_rating: A|B|C           # A: meta-analysis, B: multiple studies, C: limited
  n_studies: <number>
  primary_citation: "Chicago-style"
```

### Node Scale Classification (1-7 Scale)
Nodes are classified by structural level per `nodes/NODE_SYSTEM_DEFINITIONS.md`:
- **Scale 1 - Structural Determinants**: Federal/state policy (e.g., "medicaid_expansion")
- **Scale 2 - Built Environment**: Physical infrastructure (e.g., "air_pollution_pm25")
- **Scale 3 - Institutional**: Organizations, service delivery (e.g., "fqhc_density")
- **Scale 4 - Individual/Household**: Lived experiences (e.g., "housing_cost_burden")
- **Scale 5 - Behaviors/Psychosocial**: Health-seeking, adherence (e.g., "medication_adherence")
- **Scale 6 - Intermediate Pathways**: Clinical measures (e.g., "hypertension_control")
- **Scale 7 - Crisis Endpoints**: Acute outcomes, mortality (e.g., "alcohol_use_disorder")

## Environment Variables

```bash
# LLM & Core
ANTHROPIC_API_KEY=sk-ant-...      # Required for LLM extraction
DATABASE_URL=postgresql://...     # Production database

# Literature Search
SEMANTIC_SCHOLAR_API_KEY=...      # Optional (higher rate limits)
PUBMED_EMAIL=your@email.edu       # Required for PubMed/Unpaywall

# Full-Text Access (V3)
UNPAYWALL_EMAIL=your@email.edu    # For OA link lookup (100k/day)
ELSEVIER_API_KEY=...              # ScienceDirect API
ELSEVIER_INST_TOKEN=...           # Institutional token (contact Elsevier)
WILEY_TDM_TOKEN=...               # Wiley Text & Data Mining
CORE_API_KEY=...                  # CORE API (optional, higher limits)
OPENALEX_EMAIL=your@email.edu     # For polite pool (10 req/sec)
```

## Custom Subagents

This project has specialized Claude Code agents in `.claude/agents/`:
- `mechanism-validator`: Validates YAML files for schema and structural competency
- `epidemiology-advisor`: Reviews causal logic and scientific soundness
- `data-pipeline-builder`: Creates ETL pipelines for Census/CDC/EPA data
- `code-reviewer`: Reviews for quality, security, accessibility
- `test-generator`: Generates pytest/Jest test suites

## Test Coverage Requirements

- Backend: Minimum 80% coverage
- Frontend: Jest unit tests + Playwright E2E + Axe accessibility tests
- Mechanisms: Schema validation required before commit
