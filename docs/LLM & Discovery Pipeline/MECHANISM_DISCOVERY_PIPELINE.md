# Mechanism Discovery Pipeline

**Complete Guide to Automated Literature-Driven Mechanism Extraction**

**Document Version**: 2.0
**Last Updated**: 2025-11-30
**Status**: Production

---

## Table of Contents

1. [Overview](#1-overview)
2. [Architecture](#2-architecture)
3. [Literature Search](#3-literature-search)
4. [LLM Mechanism Extraction](#4-llm-mechanism-extraction)
5. [End-to-End Pipeline](#5-end-to-end-pipeline)
6. [Batch Processing (50% Cost Savings)](#6-batch-processing-50-cost-savings)
   - [6.8 Paper Caching](#68-paper-caching)
   - [6.9 Output Locations](#69-output-locations)
   - [6.10 Tracking New Mechanisms](#610-tracking-new-mechanisms)
6A. [**Node-Pair Driven Discovery (V4) - RECOMMENDED**](#6a-node-pair-driven-discovery-v4---recommended)
7. [Output Schema (MVP)](#7-output-schema-mvp)
8. [Validation & Quality Control](#8-validation--quality-control)
9. [Structural Competency Guidelines](#9-structural-competency-guidelines)
10. [Cost & Performance](#10-cost--performance)
11. [Troubleshooting](#11-troubleshooting)
12. [Implementation Reference](#12-implementation-reference)
13. [Bidirectional Mechanism Search Requirements](#13-bidirectional-mechanism-search-requirements)

---

## 1. Overview

The Mechanism Discovery Pipeline automates the extraction of causal mechanisms from scientific literature using:

| Component | Technology | Purpose |
|-----------|------------|---------|
| Literature Search | Semantic Scholar + PubMed APIs | Find relevant papers |
| LLM Extraction | Claude Sonnet 4.5 | Extract mechanisms from abstracts |
| Citation Validation | Crossref API | Verify DOIs and citations |
| Output | YAML files | Populate mechanism bank |

### MVP Scope

**Included (Phase 1)**:
- Node identification (what variables exist)
- Mechanism existence (does pathway A→B exist?)
- Directionality (positive or negative relationship)
- Spatial variation flags
- Evidence quality rating (A/B/C)
- Moderator identification (qualitative)

**Excluded (Phase 2)**:
- Exact effect sizes (β = 0.35)
- Confidence intervals
- Meta-analytic pooling
- Quantified moderators

> **Note**: Quantitative effect data is extracted separately by `backend/scripts/extract_quantitative_effects.py` and stored in `mechanism-bank/quantitative_effects.json` for future use.

---

## 2. Architecture

### 2.1 Three-Stage Pipeline

```
┌─────────────────────────────────────────────────────────────────┐
│                    MECHANISM DISCOVERY PIPELINE                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Stage 1: LITERATURE SEARCH                                     │
│  ├─ Input: Topic query (e.g., "housing quality respiratory")    │
│  ├─ Process: Semantic Scholar + PubMed API queries              │
│  ├─ Output: 10-50 relevant papers with abstracts                │
│  └─ Duration: ~5-10 seconds per query                           │
│                                                                 │
│                           ↓                                     │
│                                                                 │
│  Stage 2: LLM MECHANISM EXTRACTION                              │
│  ├─ Input: Paper abstracts + titles                             │
│  ├─ Process: Claude Sonnet extracts mechanisms via prompts      │
│  ├─ Output: Structured mechanism data (JSON)                    │
│  └─ Duration: ~10-15 seconds per paper                          │
│                                                                 │
│                           ↓                                     │
│                                                                 │
│  Stage 3: VALIDATION & DEDUPLICATION                            │
│  ├─ Input: Raw extracted mechanisms                             │
│  ├─ Process: Schema validation, DOI verification, dedup         │
│  ├─ Output: Clean YAML files in mechanism bank                  │
│  └─ Duration: ~1-2 seconds per mechanism                        │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 2.2 Data Flow

```
Topic Query
    │
    ▼
┌──────────────────┐     ┌──────────────────┐
│ Semantic Scholar │────▶│   Paper List     │
│      API         │     │  (deduplicated)  │
└──────────────────┘     └────────┬─────────┘
                                  │
┌──────────────────┐              │
│    PubMed API    │──────────────┘
└──────────────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │  Claude Sonnet   │
                         │   Extraction     │
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │ Crossref DOI     │
                         │  Validation      │
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │  YAML Output     │
                         │ mechanism-bank/  │
                         └──────────────────┘
```

---

## 3. Literature Search

### 3.1 Semantic Scholar API

**Implementation**: `backend/pipelines/literature_search.py` → `SemanticScholarSearch`

```python
from literature_search import SemanticScholarSearch

search = SemanticScholarSearch(api_key="optional_key")

papers = search.search_papers(
    query="housing quality respiratory health asthma",
    limit=20,
    year_range=(2015, 2024),
    min_citations=10
)
```

**Features**:
- Free tier: 100 requests / 5 minutes
- Optional API key for higher limits
- Filters: year range, minimum citations, fields of study
- Returns: title, abstract, authors, DOI, citation count

### 3.2 PubMed API

**Implementation**: `backend/pipelines/literature_search.py` → `PubMedSearch`

```python
from literature_search import PubMedSearch

search = PubMedSearch(email="your_email@example.com")

papers = search.search_papers(
    query="housing quality AND respiratory health",
    limit=20,
    year_range=(2015, 2024)
)
```

**Features**:
- Free, no API key required
- NCBI E-utilities with configurable email
- MeSH term support for precise medical queries
- Returns: title, abstract, authors, PMID, DOI

### 3.3 Aggregated Search

**Implementation**: `backend/pipelines/literature_search.py` → `LiteratureSearchAggregator`

```python
from literature_search import LiteratureSearchAggregator

aggregator = LiteratureSearchAggregator(
    pubmed_email="your_email@example.com",
    semantic_scholar_api_key=None  # Optional
)

papers = aggregator.search(
    query="eviction housing displacement health",
    limit_per_source=15,
    year_range=(2015, 2024),
    min_citations=5
)
```

**Features**:
- Combines results from both sources
- Deduplicates by DOI
- Ranks by citation count
- Filters low-quality results

### 3.4 Search Query Best Practices

**Node-Based Search Strategy**: To discover mechanisms between canonical nodes, construct search queries from node names in `mechanism-bank/mechanisms/canonical_nodes.json`. The goal is to find literature supporting causal pathways between specific node pairs.

**Good Queries** (derived from canonical node names):
```
# From: housing_quality_index → To: asthma_prevalence_adults
housing quality asthma prevalence respiratory health

# From: eviction_filing_rate → To: emergency_department_visit_rate
eviction emergency department healthcare utilization

# From: medicaid_expansion_status → To: all_cause_mortality_rate
medicaid expansion mortality health outcomes

# From: primary_care_physician_density → To: preventable_hospitalization_individual
primary care access preventable hospitalization

# From: food_insecurity_rate → To: diabetes_prevalence
food insecurity diabetes chronic disease
```

**Bad Queries**:
```
# Too broad - not targeting specific node pairs
health outcomes

# Too narrow - won't find generalizable evidence
specific-author-name-2022-study

# Full sentences (use keywords from node names instead)
"What is the relationship between housing and health?"

# Not referencing canonical nodes
"patient compliance medication adherence"  # Individual-blame framing
```

> **Tip**: Review `Nodes/COMPLETE_NODE_INVENTORY.md` for the full list of ~840 canonical nodes organized by scale and domain. Prioritize searches between nodes at different scales (e.g., Scale 1 structural → Scale 5 crisis endpoints).

---

## 4. LLM Mechanism Extraction

### 4.1 Core Extraction

**Implementation**: `backend/pipelines/llm_mechanism_discovery.py` → `LLMMechanismDiscovery`

```python
from llm_mechanism_discovery import LLMMechanismDiscovery

discovery = LLMMechanismDiscovery()

mechanisms = discovery.extract_mechanisms_from_paper(
    paper_abstract="Your abstract text here...",
    paper_title="Paper Title",
    paper_doi="10.xxxx/xxxxx",
    paper_citation="Author et al. (2024). Title. Journal.",
    focus_area="housing to health"
)
```

### 4.2 Extraction Prompt Strategy

The LLM receives structured prompts designed to:

1. **Focus on structural determinants** (not individual behavior)
2. **Extract causal pathways** (step-by-step mechanisms)
3. **Identify directionality** (positive/negative)
4. **Assess evidence quality** (A/B/C based on study count)
5. **Flag spatial variation** (geographic differences)
6. **Capture moderators** (factors that strengthen/weaken)

**Key Prompt Elements**:
```
SYSTEM: You are a public health researcher analyzing literature
on structural determinants of health.

TASK: Extract causal mechanisms from this paper abstract.
Focus on STRUCTURAL factors (policy, environment, systems)
not individual behaviors.

For each mechanism, provide:
- Source node (upstream factor)
- Target node (downstream outcome)
- Direction (positive or negative)
- Mechanism pathway (step-by-step causal chain)
- Evidence quality (A/B/C)
- Moderators (factors that modify the effect)
```

### 4.3 Citation Validation (V2)

**Implementation**: `backend/utils/citation_validation.py`

The V2 pipeline validates citations to prevent fabrication:

```python
from utils.citation_validation import CitationValidator

validator = CitationValidator()

# Verify DOI exists
is_valid, metadata = validator.verify_doi("10.1097/PHH.0b013e3181ddcbd9")

# Format citation from DOI
citation = validator.format_chicago_citation(metadata)
```

**Validation Steps**:
1. DOI format check (regex)
2. Crossref API lookup
3. Metadata extraction (authors, title, journal, year)
4. Chicago-style citation formatting

---

## 5. End-to-End Pipeline

### 5.1 Complete Pipeline

**Implementation**: `backend/pipelines/end_to_end_discovery.py`

```python
from end_to_end_discovery import EndToEndDiscoveryPipeline

# Initialize
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
report = pipeline.generate_discovery_report(
    output_file="discovery_report.json"
)
```

### 5.2 Batch Discovery

```python
# Discover mechanisms between canonical node pairs
# Reference: mechanism-bank/mechanisms/canonical_nodes.json

node_pair_topics = [
    # (search query based on node names, category, from_node_id, to_node_id)
    ("housing quality asthma respiratory", "built_environment",
     "housing_quality_index_revised_consolidated", "asthma_prevalence_adults_revised_terminology_standardized"),
    ("eviction emergency department utilization", "economic",
     "eviction_filing_rate", "emergency_department_visit_rate"),
    ("medicaid expansion mortality outcomes", "political",
     "medicaid_expansion_status", "all_cause_mortality_rate"),
    ("primary care access hospitalization", "healthcare_access",
     "primary_care_physician_density", "preventable_hospitalization_individual"),
]

all_mechanisms = []
for query, category, from_node, to_node in node_pair_topics:
    mechanisms = pipeline.discover_mechanisms_for_topic(
        topic_query=query,
        max_papers=10,
        focus_area=f"{from_node} to {to_node}"
    )
    # Ensure discovered mechanisms reference canonical nodes
    for m in mechanisms:
        m['from_node']['node_id'] = from_node
        m['to_node']['node_id'] = to_node
    all_mechanisms.extend(mechanisms)

pipeline.discovered_mechanisms = all_mechanisms
pipeline.save_mechanisms()
```

### 5.3 Environment Setup

```bash
# Required
export ANTHROPIC_API_KEY="your_api_key_here"

# Optional (higher rate limits)
export SEMANTIC_SCHOLAR_API_KEY="your_key_here"

# Recommended (NCBI policy)
export PUBMED_EMAIL="your_email@example.com"
```

---

## 6. Batch Processing (50% Cost Savings)

Claude's Message Batches API enables **50% cost reduction** for bulk mechanism discovery. Use batch processing for scheduled runs, large-scale literature reviews, and cost-sensitive workloads.

### 6.1 When to Use Batch vs. Real-Time

| Use Case | Recommended | Rationale |
|----------|-------------|-----------|
| Bulk discovery (50+ papers) | **Batch** | 50% cost savings, parallel processing |
| Nightly/weekly scheduled runs | **Batch** | Unattended, cost-effective |
| Large literature reviews | **Batch** | Process 1000s of papers efficiently |
| Interactive single-paper extraction | Real-time | Immediate results needed |
| Testing/debugging prompts | Real-time | Quick iteration |
| Urgent discoveries | Real-time | Results needed in <1 hour |

### 6.2 Batch Processing Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                 BATCH-ENABLED DISCOVERY PIPELINE                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Stage 1: LITERATURE SEARCH (unchanged)                         │
│  ├─ Semantic Scholar + PubMed APIs                              │
│  └─ Output: List of papers with citation contexts               │
│                                                                 │
│                           ↓                                     │
│                                                                 │
│  Stage 2: BATCH PREPARATION                                     │
│  ├─ Create extraction prompts for ALL papers                    │
│  ├─ Assign custom_id to each (paper DOI or index)               │
│  └─ Submit single batch request (up to 100k papers)             │
│                                                                 │
│                           ↓                                     │
│                                                                 │
│  Stage 3: ASYNC POLLING                                         │
│  ├─ Poll batch status every 60 seconds                          │
│  ├─ Typical completion: <1 hour for most batches                │
│  └─ Maximum wait: 24 hours                                      │
│                                                                 │
│                           ↓                                     │
│                                                                 │
│  Stage 4: RESULT PROCESSING                                     │
│  ├─ Stream JSONL results                                        │
│  ├─ Match results to papers via custom_id                       │
│  ├─ Validate citations (unchanged)                              │
│  └─ Save to mechanism bank                                      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 6.3 Basic Batch Usage

```python
from backend.pipelines.batch_mechanism_discovery import (
    BatchMechanismDiscovery,
    PaperInput,
    papers_from_literature_search
)
from backend.pipelines.literature_search import LiteratureSearchAggregator

# 1. Search for papers
aggregator = LiteratureSearchAggregator(pubmed_email="your@email.edu")
papers = aggregator.search(
    query="housing quality respiratory health asthma",
    limit_per_source=50,
    year_range=(2015, 2024)
)

# 2. Convert to batch format
batch_papers = papers_from_literature_search(papers)

# 3. Run batch discovery (50% cheaper!)
batch_discovery = BatchMechanismDiscovery()
result = batch_discovery.discover_mechanisms_batch(
    papers=batch_papers,
    output_dir=Path("mechanism-bank/mechanisms"),
    wait_for_completion=True
)

print(f"Extracted {len(result.mechanisms)} mechanisms")
print(f"Cost: ${result.cost_estimate_usd}")
```

### 6.4 Submit and Poll Later

For unattended/scheduled runs:

```python
# Submit batch (returns immediately)
batch_id = batch_discovery.submit_batch(batch_papers)
print(f"Batch submitted: {batch_id}")

# ... later (or in another process) ...

# Check status
status = batch_discovery.get_batch_status(batch_id)
print(f"Status: {status['status']}")

# When complete, process results
if status['status'] == 'ended':
    mechanisms = batch_discovery.process_results(batch_id, paper_lookup)
```

### 6.5 Scheduled Discovery Script

For nightly/weekly runs, use the scheduled script:

```bash
# Single topic
python backend/scripts/scheduled_batch_discovery.py \
    --topic "housing quality respiratory health"

# Multiple topics from config
python backend/scripts/scheduled_batch_discovery.py \
    --config discovery_topics.json

# Use default comprehensive topics
python backend/scripts/scheduled_batch_discovery.py --default-topics

# Check existing batch
python backend/scripts/scheduled_batch_discovery.py \
    --check-batch msgbatch_xxx

# List recent batches
python backend/scripts/scheduled_batch_discovery.py --list-batches
```

**Cron example (Linux/Mac - nightly at 2 AM):**
```bash
0 2 * * * cd /path/to/healthsystems && python backend/scripts/scheduled_batch_discovery.py --default-topics
```

**Windows Task Scheduler:**
```cmd
schtasks /create /tn "MechanismDiscovery" /tr "python backend/scripts/scheduled_batch_discovery.py --default-topics" /sc weekly /d SUN /st 02:00
```

### 6.6 Batch API Limits & Pricing

| Limit | Value |
|-------|-------|
| Max requests per batch | 100,000 |
| Max batch size | 256 MB |
| Processing time | Typically <1 hour, max 24 hours |
| Result availability | 29 days |

**Pricing (50% discount vs. real-time):**

| Model | Input (per 1M tokens) | Output (per 1M tokens) |
|-------|----------------------|------------------------|
| Claude Sonnet 4.5 | $1.50 | $7.50 |
| Claude Opus 4.5 | $2.50 | $12.50 |
| Claude Haiku 4.5 | $0.50 | $2.50 |

### 6.7 Cost Comparison Examples

| Papers | Real-Time Cost | Batch Cost | Savings |
|--------|----------------|------------|---------|
| 50 | ~$0.42 | ~$0.21 | $0.21 (50%) |
| 200 | ~$1.68 | ~$0.84 | $0.84 (50%) |
| 500 | ~$4.20 | ~$2.10 | $2.10 (50%) |
| 2000 | ~$16.80 | ~$8.40 | $8.40 (50%) |

### 6.8 Paper Caching

All papers used in batch processing are automatically cached to enable:
- **Reproducibility**: Re-run extractions on the same paper set
- **Skip search**: Speed up re-runs by skipping literature search
- **Audit trail**: Track which papers contributed to which mechanisms

**Cache Location**:
```
backend/data/
├── {topic}_papers_{YYYYMMDD}.json     # Cached papers from search
├── alcohol_papers_20251206.json        # Example: alcohol batch
└── housing_papers_20251201.json        # Example: housing batch
```

**Cache Format**:
```json
[
  {
    "title": "Paper Title",
    "abstract": "Full abstract text...",
    "year": 2024,
    "doi": "10.xxxx/xxxxx",
    "authors": ["Author 1", "Author 2"],
    "journal": "Journal Name"
  }
]
```

**Using Cached Papers**:
```bash
# Skip literature search, use cached papers
python backend/scripts/run_alcohol_batch_discovery.py \
    --skip-search \
    --papers-cache backend/data/alcohol_papers_20251206.json
```

### 6.9 Output Locations

Batch discovery produces outputs in multiple locations:

| Output Type | Location | Description |
|-------------|----------|-------------|
| **Mechanism YAMLs** | `mechanism-bank/mechanisms/{category}/` | Individual mechanism files by category |
| **Paper Cache** | `backend/data/{topic}_papers_{date}.json` | Cached papers from literature search |
| **Discovery Report** | `backend/reports/alcohol_discovery_report_{timestamp}.json` | Comprehensive extraction report |
| **Batch Report** | `discovery_batch_report.json` (default) | Low-level batch API results |

**Mechanism Bank Structure**:
```
mechanism-bank/mechanisms/
├── behavioral/
│   ├── alcohol_consumption_to_colorectal_cancer_incidence.yaml
│   └── ...
├── biological/
├── built_environment/
├── economic/
├── healthcare_access/
├── political/
│   ├── alcohol_taxation_to_alcohol_consumption.yaml
│   ├── minimum_unit_pricing_to_alcohol_consumption.yaml
│   └── ...
└── social_environment/
```

### 6.10 Tracking New Mechanisms

To track which mechanisms were added in a batch run:

**1. Discovery Report** (`backend/reports/`):
```json
{
  "timestamp": "2025-12-06T18:30:45",
  "batch_id": "msgbatch_xxx",
  "summary": {
    "papers_submitted": 669,
    "mechanisms_extracted": 200,
    "target_met": true
  },
  "mechanisms": [
    {
      "id": "alcohol_taxation_to_alcohol_consumption",
      "from": "Alcohol Taxation",
      "to": "Alcohol Consumption",
      "category": "political",
      "citation_verified": true
    }
  ]
}
```

**2. Git-Based Tracking**:
```bash
# List new mechanism files added since last commit
git status --porcelain mechanism-bank/mechanisms/ | grep "^??" | cut -c4-

# List mechanisms modified/added today
find mechanism-bank/mechanisms -name "*.yaml" -mtime -1

# Count new mechanisms by category
for dir in mechanism-bank/mechanisms/*/; do
  echo "$(basename $dir): $(ls "$dir"*.yaml 2>/dev/null | wc -l)"
done
```

**3. Programmatic Tracking**:
```python
from pathlib import Path
from datetime import datetime, timedelta

def list_new_mechanisms(since_hours: int = 24) -> list:
    """List mechanism files created in the last N hours."""
    cutoff = datetime.now() - timedelta(hours=since_hours)
    mechanism_dir = Path("mechanism-bank/mechanisms")

    new_files = []
    for yaml_file in mechanism_dir.rglob("*.yaml"):
        mtime = datetime.fromtimestamp(yaml_file.stat().st_mtime)
        if mtime > cutoff:
            new_files.append({
                "file": str(yaml_file),
                "category": yaml_file.parent.name,
                "modified": mtime.isoformat()
            })

    return sorted(new_files, key=lambda x: x["modified"], reverse=True)

# Usage
new_mechs = list_new_mechanisms(since_hours=24)
print(f"Added {len(new_mechs)} mechanisms in last 24 hours")
```

---

## 6A. Node-Pair Driven Discovery (V4) - RECOMMENDED

The **Node-Pair Driven Discovery Pipeline (V4)** is the **recommended approach** for mechanism discovery. It addresses key limitations of paper-centric approaches by:

1. **Using only existing nodes** from `nodes/by_scale/` - no invented nodes
2. **Consolidating multiple papers** into ONE mechanism per node pair
3. **Not forcing mechanisms** when evidence is insufficient
4. **Using node-adjacent keywords** for better search coverage

### 6A.1 V4 vs. Earlier Approaches

| Aspect | V1-V3 (Paper-Centric) | V4 (Node-Pair Driven) |
|--------|----------------------|----------------------|
| Starting point | Papers → discover pathways | Node pairs → find evidence |
| Node validation | Post-hoc (often creates NEW: nodes) | Upfront (only existing nodes) |
| Evidence consolidation | Post-extraction grouping | Built-in multi-paper synthesis |
| Insufficient evidence | May force low-quality mechanisms | Returns null explicitly |
| Search coverage | Generic queries | Node-specific keywords |

### 6A.2 Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│             NODE-PAIR DRIVEN DISCOVERY PIPELINE (V4)            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Stage 1: LOAD NODE PAIRS FROM CONFIG                           │
│  ├─ Input: Config file (e.g., alcohol_node_pairs.json)          │
│  ├─ Validate: Both nodes exist in nodes/by_scale/               │
│  └─ Output: List of validated NodePair objects                  │
│                                                                 │
│                           ↓                                     │
│                                                                 │
│  Stage 2: SEARCH WITH NODE KEYWORDS                             │
│  ├─ Build queries from node-adjacent keywords                   │
│  ├─ Search Semantic Scholar + PubMed                            │
│  └─ Output: Papers per node pair                                │
│                                                                 │
│                           ↓                                     │
│                                                                 │
│  Stage 3: CONSOLIDATE & EXTRACT (BATCH)                         │
│  ├─ For each node pair with ≥3 papers:                          │
│  │   ├─ Send ALL papers to LLM in ONE request                   │
│  │   ├─ LLM synthesizes evidence across papers                  │
│  │   └─ Returns ONE mechanism OR null                           │
│  └─ Output: Consolidated mechanisms or explicit "no evidence"   │
│                                                                 │
│                           ↓                                     │
│                                                                 │
│  Stage 4: SAVE TO MECHANISM BANK                                │
│  ├─ Validate node IDs match config exactly                      │
│  ├─ Save YAML files by category                                 │
│  └─ Generate discovery report                                   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 6A.3 Configuration File Structure

Create a config file in `backend/configs/`:

```json
{
  "name": "alcohol_node_pair_discovery",
  "version": "2.1",
  "description": "Node-pair driven discovery for alcohol pathways",
  "node_source": "nodes/by_scale/",
  "budget": {
    "max_usd": 25.0,
    "max_pairs": 50
  },
  "node_keywords": {
    "alcohol_taxation": ["alcohol tax", "excise tax", "minimum unit pricing"],
    "binge_drinking": ["heavy episodic drinking", "excessive drinking"],
    "alcohol_use_disorder": ["AUD", "alcohol dependence", "alcoholism"]
  },
  "node_pairs": [
    {
      "from_node_id": "alcohol_taxation",
      "to_node_id": "binge_drinking",
      "expected_direction": "negative",
      "priority": 1,
      "category": "political"
    }
  ],
  "search_config": {
    "papers_per_pair": 30,
    "min_papers_required": 3,
    "year_range": [2010, 2025],
    "prioritize_meta_analyses": true,
    "use_node_keywords": true
  },
  "llm_config": {
    "model": "claude-sonnet-4-20250514",
    "consolidate_papers": true,
    "min_citations_per_mechanism": 3,
    "force_mechanism_if_no_evidence": false,
    "return_null_if_insufficient_evidence": true,
    "only_use_existing_nodes": true
  }
}
```

### 6A.4 Usage

```bash
# Dry run to validate config and see stats
python backend/scripts/run_node_pair_discovery.py \
    --config backend/configs/alcohol_node_pairs.json \
    --dry-run

# Full run with paper search
python backend/scripts/run_node_pair_discovery.py \
    --config backend/configs/alcohol_node_pairs.json

# Skip search, use cached papers
python backend/scripts/run_node_pair_discovery.py \
    --config backend/configs/alcohol_node_pairs.json \
    --no-search \
    --cache backend/data/alcohol_papers.json
```

### 6A.5 Node Keyword Guidelines

Node-adjacent keywords improve search coverage:

```json
"node_keywords": {
  // Policy nodes - include legislative terms
  "alcohol_taxation": [
    "alcohol tax", "excise tax", "minimum unit pricing",
    "alcohol price policy", "beverage tax"
  ],

  // Behavioral nodes - include clinical terms
  "alcohol_use_disorder": [
    "AUD", "alcohol dependence", "alcoholism",
    "alcohol addiction", "problem drinking"
  ],

  // Outcome nodes - include ICD codes and synonyms
  "liver_cirrhosis_hospitalization_rate": [
    "cirrhosis hospitalization", "alcoholic liver disease",
    "hepatic cirrhosis", "liver disease admission"
  ]
}
```

### 6A.6 Critical: No Forced Mechanisms

The V4 pipeline explicitly handles insufficient evidence:

```python
# LLM prompt instructs:
# "If evidence is insufficient, return:
#  {"mechanism": null, "reason": "Insufficient evidence"}"

# Pipeline respects this:
if result.mechanism is None:
    log.info(f"No mechanism found for {pair}: {result.reason}")
    # Does NOT create a low-quality placeholder
```

### 6A.7 Discovery Report

Each run generates a comprehensive report:

```json
{
  "config_name": "alcohol_node_pair_discovery",
  "timestamp": "2025-12-06T20:30:00",
  "processing_time_seconds": 3600,
  "pairs_configured": 30,
  "pairs_with_evidence": 24,
  "total_papers_found": 450,
  "mechanisms_extracted": 20,
  "insufficient_evidence": 4,
  "errors": 0,
  "extraction_method": "node_pair_discovery_v4"
}
```

### 6A.8 Files

| File | Purpose |
|------|---------|
| `backend/pipelines/node_pair_discovery.py` | V4 pipeline implementation |
| `backend/scripts/run_node_pair_discovery.py` | CLI runner script |
| `backend/configs/alcohol_node_pairs.json` | Example config for alcohol topic |
| `backend/reports/node_pair_discovery_*.json` | Discovery reports |

---

## 7. Output Schema (MVP)

### 7.1 Required Fields

> **Important**: All `node_id` values MUST reference entries in `mechanism-bank/mechanisms/canonical_nodes.json`. See `Nodes/COMPLETE_NODE_INVENTORY.md` for full node specifications.

```yaml
# Example: Mechanism from housing quality to asthma prevalence
id: housing_quality_index_revised_consolidated_to_asthma_prevalence_adults_revised_terminology_standardized
name: Housing Quality Index → Asthma Prevalence (Adults)
from_node:
  node_id: housing_quality_index_revised_consolidated  # Must exist in canonical_nodes.json
  node_name: Housing Quality Index
  node_type: proxy_index
to_node:
  node_id: asthma_prevalence_adults_revised_terminology_standardized  # Must exist in canonical_nodes.json
  node_name: Asthma Prevalence (Adults)
  node_type: crisis_endpoint
direction: negative  # Better housing quality → lower asthma prevalence
category: built_environment
mechanism_pathway:
  - "Step 1: Poor housing conditions increase exposure to mold, dust, and allergens"
  - "Step 2: Chronic allergen exposure triggers airway inflammation"
  - "Step 3: Repeated inflammation leads to asthma development or exacerbation"
evidence:
  quality_rating: A | B | C
  n_studies: <number>
  primary_citation: "Chicago-style citation"
  doi: "10.xxxx/xxxxx"
last_updated: YYYY-MM-DD
version: "1.0"
```

**Schema Template** (with placeholders):
```yaml
id: {from_node_id}_to_{to_node_id}
name: {From Node Name} → {To Node Name}
from_node:
  node_id: {canonical_node_id}  # From canonical_nodes.json
  node_name: {Human Readable Name}
  node_type: stock | proxy_index | crisis_endpoint
to_node:
  node_id: {canonical_node_id}  # From canonical_nodes.json
  node_name: {Human Readable Name}
  node_type: stock | proxy_index | crisis_endpoint
direction: positive | negative
category: built_environment | social_environment | economic | political | biological | behavioral | healthcare_access
```

### 7.2 Optional Fields

```yaml
description: "Detailed mechanism description"
spatial_variation:
  varies_by_geography: true | false
  variation_notes: "Description of geographic variation"
  relevant_geographies:
    - "Geography 1 with specific pattern"
    - "Geography 2 with different pattern"
moderators:
  - name: moderator_name
    direction: strengthens | weakens | u_shaped
    strength: weak | moderate | strong
    description: "How this moderator affects the mechanism"
structural_competency:
  root_cause_level: policy | economic_system | spatial_arrangement | institutional | interpersonal
  avoids_victim_blaming: true
  equity_implications: "Description of equity considerations"
assumptions:
  - "Key assumption 1"
  - "Key assumption 2"
limitations:
  - "Limitation 1"
  - "Limitation 2"
llm_metadata:
  extracted_by: claude-sonnet-4-5-20250929
  extraction_date: "YYYY-MM-DDTHH:MM:SS"
  extraction_confidence: high | medium | low
  prompt_version: "1.0-mvp"
```

### 7.3 Evidence Quality Grades

| Grade | Criteria | Study Count |
|-------|----------|-------------|
| **A** | Meta-analysis or systematic review with 5+ high-quality studies | 5-100 |
| **B** | 3-4 studies or systematic review with moderate evidence | 3-10 |
| **C** | 1-2 studies or limited/emerging evidence | 1-4 |

> **Note**: Grade D does not exist. All mechanisms must have at least C-level evidence.

---

## 8. Validation & Quality Control

### 8.1 Automated Validation

**Implementation**: `backend/scripts/validate_mechanism_schema.py`

```bash
cd mechanism-bank
python ../backend/scripts/validate_mechanism_schema.py
```

**Checks**:
- JSON schema compliance
- Required fields present
- Enum values valid (category, direction, evidence grade)
- Node scale consistency (1-7)
- DOI format validation
- Citation format check

### 8.2 Mechanism Validator Agent

**Implementation**: `backend/agents/mechanism_validator.py`

Provides comprehensive validation:
- Category alignment with node types
- Scale consistency (source → target progression)
- Evidence plausibility (study count matches grade)
- Structural competency review
- Equity implications check

### 8.3 Quality Control Workflow

```
1. LLM extracts mechanism
         │
         ▼
2. Schema validation (automated)
   ├─ PASS → Continue
   └─ FAIL → Fix or reject
         │
         ▼
3. DOI verification (Crossref)
   ├─ VALID → Continue
   └─ INVALID → Flag for manual review
         │
         ▼
4. Confidence check
   ├─ HIGH → Auto-approve
   ├─ MEDIUM → Quick review
   └─ LOW → Full manual review
         │
         ▼
5. Structural competency check
   ├─ PASS → Save to mechanism bank
   └─ FAIL → Reject or reframe
```

### 8.4 Manual Review Checklist

For mechanisms requiring human review:

- [ ] Effect direction matches literature
- [ ] Mechanism pathway is scientifically plausible
- [ ] Citations are accurate and relevant
- [ ] Category assignment is correct
- [ ] No victim-blaming language
- [ ] Equity implications addressed
- [ ] Node naming is consistent with existing bank

---

## 9. Structural Competency Guidelines

> **Note**: All examples use canonical node IDs from `mechanism-bank/mechanisms/canonical_nodes.json`.

### 9.1 Good Mechanisms (Structural Focus)

**Policy → Outcomes** (Scale 1 → Scale 5):
```yaml
# Good: Focuses on policy structure using canonical nodes
from_node:
  node_id: medicaid_expansion_status  # Scale 1 structural policy
  node_name: Medicaid Expansion Status
to_node:
  node_id: uninsured_rate  # Scale 3 individual condition
  node_name: Uninsured Rate
mechanism_pathway:
  - "State-level policy decision expands Medicaid eligibility"
  - "More residents qualify for coverage up to 138% FPL"
  - "Insurance removes financial barrier to care"
```

**Economic Systems → Health** (Scale 3 → Scale 5):
```yaml
# Good: Focuses on structural economic factors using canonical nodes
from_node:
  node_id: eviction_filing_rate  # Scale 3 individual/household condition
  node_name: Eviction Filing Rate
to_node:
  node_id: emergency_department_visit_rate  # Scale 5 crisis endpoint
  node_name: Emergency Department Visit Rate
mechanism_pathway:
  - "Housing market pressure leads to increased eviction filings"
  - "Displacement disrupts established care relationships"
  - "Lost records and provider changes lead to ED utilization for non-emergencies"
```

**Spatial Arrangements → Exposures** (Scale 1 → Scale 3):
```yaml
# Good: Focuses on environmental structure using canonical nodes
from_node:
  node_id: single_family_zoning_restriction_prevalence  # Scale 1 policy
  node_name: Single-Family Zoning Restriction Prevalence
to_node:
  node_id: housing_cost_burden  # Scale 3 individual condition
  node_name: Housing Cost Burden
mechanism_pathway:
  - "Exclusionary zoning restricts housing supply in desirable areas"
  - "Limited supply drives up housing costs"
  - "Households pay disproportionate income share on housing"
```

### 9.2 Bad Mechanisms (Individual Blame)

**Avoid These Framings** (these node concepts should NOT be discovery targets):

```yaml
# Bad: Blames individual behavior - NOT in canonical nodes
from_node: health_literacy  # Not a canonical node - too individual-focused
to_node: medication_adherence
# This ignores educational inequality, healthcare system complexity
# INSTEAD: Focus on healthcare_literacy_support_availability → medication_adherence_rate

# Bad: Victim-blaming framing - NOT in canonical nodes
from_node: patient_compliance  # Not a canonical node - blame framing
to_node: health_outcomes
# This ignores systemic barriers to care
# INSTEAD: Focus on care_coordination_quality → treatment_completion_rate

# Bad: Individual behavior focus - NOT in canonical nodes
from_node: exercise_behavior  # Not a canonical node
to_node: obesity_prevalence
# This ignores built environment, food access, time poverty
# INSTEAD: Focus on walkability_score → physical_activity_rate
#          or food_desert_prevalence → obesity_prevalence_adults
```

> **Key Principle**: The canonical node inventory intentionally excludes individual-blame nodes. If you find yourself searching for mechanisms with "patient compliance," "personal responsibility," or similar terms, reframe to identify the STRUCTURAL factors that create the observed patterns.

### 9.3 Equity Lens

For every mechanism, consider:

1. **Differential Exposure**: Who is more likely to experience this mechanism?
2. **Differential Vulnerability**: Who is more affected by it?
3. **Root Causes**: What structural factors create these patterns?
4. **Historical Context**: How did policies create current disparities?

---

## 10. Cost & Performance

### 10.1 API Rate Limits

| Service | Free Tier | With API Key |
|---------|-----------|--------------|
| Semantic Scholar | 100 req / 5 min | Higher limits |
| PubMed | 3 req / sec | Same |
| Claude API | Varies by tier | Varies |
| Crossref | 50 req / sec | Same |

### 10.2 Cost Estimates (Claude API)

Assuming average paper abstract = 300 words (~400 tokens):

| Papers | Input Tokens | Output Tokens | Estimated Cost |
|--------|--------------|---------------|----------------|
| 10 | ~6,000 | ~8,000 | ~$0.08 |
| 100 | ~60,000 | ~80,000 | ~$0.84 |
| 500 | ~300,000 | ~400,000 | ~$4.20 |
| 2000 | ~1.2M | ~1.6M | ~$16.80 |

*Costs based on Claude Sonnet 4.5 real-time pricing as of 2025. Use batch processing for 50% savings (see Section 6).*

### 10.3 Processing Time

| Stage | Time per Item |
|-------|---------------|
| Literature search | 5-10 sec / query |
| LLM extraction | 10-15 sec / paper |
| DOI validation | 0.5-1 sec / DOI |
| Schema validation | <0.1 sec / mechanism |

**Total Pipeline Time**:
- 10 papers: ~3-5 minutes
- 100 papers: ~30-45 minutes
- 500 papers: ~3-4 hours
- 2000 papers: ~12-15 hours

**Batch Processing Times:**
| Papers | Typical Time | Maximum Time |
|--------|--------------|--------------|
| 50 | ~15-30 min | 24 hours |
| 500 | ~30-60 min | 24 hours |
| 2000 | ~1-2 hours | 24 hours |

---

## 11. Troubleshooting

### 11.1 "No papers found"

**Causes**:
- Query too specific or uses full sentences
- Year range too narrow
- Citation threshold too high

**Solutions**:
```python
# Use keywords, not sentences
query = "housing quality respiratory health"  # Good
query = "What is the effect of housing on health?"  # Bad

# Widen year range
year_range = (2010, 2024)  # Instead of (2020, 2024)

# Lower citation threshold
min_citations = 5  # Instead of 50
```

### 11.2 "Error extracting mechanisms"

**Causes**:
- Invalid or missing ANTHROPIC_API_KEY
- Rate limit exceeded
- Paper has no abstract

**Solutions**:
```bash
# Check API key
echo $ANTHROPIC_API_KEY

# Wait for rate limit reset (usually 1-5 minutes)

# Skip papers without abstracts
if paper.abstract:
    mechanisms = discovery.extract_mechanisms_from_paper(...)
```

### 11.3 "Schema validation failed"

**Causes**:
- Missing required fields
- Invalid enum values
- Malformed YAML

**Solutions**:
```bash
# Run validation to see specific errors
python backend/scripts/validate_mechanism_schema.py

# Check enum values
# category must be one of: built_environment, social_environment,
#   economic, political, biological, behavioral, healthcare_access
# direction must be: positive or negative
# evidence.quality_rating must be: A, B, or C
```

### 11.4 "Low-quality extractions"

**Causes**:
- Low-impact papers (few citations)
- Vague abstracts
- Off-topic results

**Solutions**:
```python
# Increase citation threshold
min_citations = 20

# Add focus_area hint
focus_area = "housing interventions and respiratory health outcomes"

# Filter by study type in query
query = "housing quality asthma meta-analysis OR systematic review"
```

### 11.5 Batch Processing Issues

**"Batch timeout"**:
- Most batches complete in <1 hour
- If timeout occurs, check batch status and process partial results
- Consider splitting into smaller batches

**"Cannot resume batch"**:
- Ensure you save the batch_id and paper_lookup when submitting
- Use `--check-batch` and `--process-batch` CLI options

**"Results expired"**:
- Batch results are available for 29 days
- Process and save results promptly after completion

---

## 12. Implementation Reference

### 12.1 File Locations

```
backend/
├── pipelines/
│   ├── README.md                      # Pipeline overview
│   ├── literature_search.py           # Semantic Scholar + PubMed
│   ├── llm_mechanism_discovery.py     # Claude extraction (real-time)
│   ├── batch_mechanism_discovery.py   # Claude batch extraction (50% savings)
│   ├── end_to_end_discovery.py        # Complete pipeline
│   └── mechanism_deduplication.py     # Deduplication logic
├── utils/
│   ├── citation_validation.py         # DOI verification
│   └── canonical_nodes.py             # Node lookup and fuzzy matching
├── scripts/
│   ├── validate_mechanism_schema.py   # Schema validation
│   ├── extract_quantitative_effects.py # Effect size extraction
│   └── scheduled_batch_discovery.py   # Scheduled batch runs
├── agents/
│   └── mechanism_validator.py         # Comprehensive validation
├── config/
│   └── schema_config.py               # Centralized schema constants
└── data/
    └── canonical_nodes.json           # Enriched node data (840 nodes)

mechanism-bank/
├── schemas/
│   ├── mechanism_schema_mvp.json      # MVP schema definition
│   └── quantitative_effects_schema.json # Effect size schema
├── mechanisms/
│   ├── canonical_nodes.json           # Canonical node reference (840 nodes)
│   ├── built_environment/             # By category
│   ├── social_environment/
│   ├── economic/
│   ├── political/
│   ├── biological/
│   ├── behavioral/
│   └── healthcare_access/
└── quantitative_effects.json          # Extracted effect data

Nodes/
└── COMPLETE_NODE_INVENTORY.md         # Full specifications for 840 nodes

docs/
└── LLM & Discovery Pipeline/
    └── MECHANISM_DISCOVERY_PIPELINE.md # This document
```

### 12.2 Key Classes

| Class | File | Purpose |
|-------|------|---------|
| `SemanticScholarSearch` | `literature_search.py` | Search Semantic Scholar API |
| `PubMedSearch` | `literature_search.py` | Search PubMed API |
| `LiteratureSearchAggregator` | `literature_search.py` | Combine search sources |
| `LLMMechanismDiscoveryV2` | `llm_mechanism_discovery.py` | Extract via Claude (real-time) |
| `BatchMechanismDiscovery` | `batch_mechanism_discovery.py` | Extract via Claude Batch API (50% savings) |
| `MechanismExtraction` | `llm_mechanism_discovery.py` | Pydantic model for extracted data |
| `EndToEndDiscoveryPipeline` | `end_to_end_discovery.py` | Complete workflow |
| `ScheduledBatchDiscovery` | `scheduled_batch_discovery.py` | Scheduled batch runs |
| `CitationValidator` | `citation_validation.py` | DOI verification |
| `MechanismValidator` | `mechanism_validator.py` | Comprehensive validation |

### 12.3 Environment Variables

```bash
# Required
ANTHROPIC_API_KEY=sk-ant-...      # Claude API access

# Optional
SEMANTIC_SCHOLAR_API_KEY=...       # Higher rate limits
PUBMED_EMAIL=your@email.com        # NCBI best practice
```

### 12.4 Quick Start Commands

```bash
# Install dependencies
cd backend
pip install -r requirements.txt

# Set API key
export ANTHROPIC_API_KEY="your_key_here"

# Run demo discovery
cd pipelines
python end_to_end_discovery.py

# Validate mechanism bank
cd ../..
python backend/scripts/validate_mechanism_schema.py

# Extract quantitative effects
python backend/scripts/extract_quantitative_effects.py \
    --output mechanism-bank/quantitative_effects.json

# Batch discovery (50% cost savings)
python backend/scripts/scheduled_batch_discovery.py --default-topics

# Check batch status
python backend/scripts/scheduled_batch_discovery.py --list-batches
```

---

## Canonical Node Reference

All mechanism discovery MUST reference nodes from the canonical inventory. This ensures consistency across the platform.

### Node Sources

| Source | Location | Use Case |
|--------|----------|----------|
| **Canonical Nodes JSON** | `mechanism-bank/mechanisms/canonical_nodes.json` | Quick lookup of node IDs (840 nodes) |
| **Complete Inventory** | `Nodes/COMPLETE_NODE_INVENTORY.md` | Full specifications with scales, domains, units |
| **Backend Utilities** | `backend/utils/canonical_nodes.py` | Programmatic node lookup and fuzzy matching |

### Node Scale Hierarchy

When discovering mechanisms, consider the scale flow (typically upstream → downstream):

| Scale | Level | Example Nodes |
|-------|-------|---------------|
| **1** | Structural Policy | `medicaid_expansion_status`, `rent_control_stabilization_policy_strength`, `minimum_wage_level` |
| **2** | Institutional | `primary_care_physician_density`, `emergency_department_availability` |
| **3** | Individual/Household | `eviction_filing_rate`, `housing_cost_burden`, `food_insecurity_rate` |
| **4** | Intermediate | `preventable_hospitalization_individual`, `mental_healthcare_access` |
| **5** | Crisis Endpoints | `emergency_department_visit_rate`, `all_cause_mortality_rate`, `asthma_hospitalization_rate` |

### Using Nodes in Discovery

```python
from backend.utils.canonical_nodes import get_all_nodes, find_matching_node

# Get all canonical nodes
nodes = get_all_nodes()

# Fuzzy match extracted text to canonical node
match, score = find_matching_node("housing quality", threshold=0.7)
# Returns: ('housing_quality_index_revised_consolidated', 0.85)

# Get nodes by scale for targeted searches
scale_1_nodes = get_nodes_by_scale(1)  # Structural policy nodes
scale_5_nodes = get_nodes_by_scale(5)  # Crisis endpoints
```

---

---

## 13. Bidirectional Mechanism Search Requirements

All mechanism discovery MUST search for pathways in **both directions** for each node pair. This ensures comprehensive coverage of causal relationships, including feedback loops where outcomes influence upstream determinants.

### 13.1 Bidirectional Search Principle

For each node pair (A, B), execute searches in both directions:

| Search Direction | Scale Flow | Example |
|------------------|-----------|---------|
| **Forward** | Upstream → Downstream | `alcohol_taxation` → `heavy_alcohol_use` → `liver_cirrhosis_hospitalization_rate` |
| **Backward** | Downstream → Upstream | `alcohol_use_disorder` → `unemployment_rate` → `housing_instability` |

### 13.2 Why Bidirectional Search Matters

1. **Feedback Loops**: Many health systems exhibit bidirectional causality
   - Example: Housing instability → AUD, but also AUD → job loss → housing instability

2. **Policy Feedback**: Outcomes can influence policy adoption
   - Example: High mortality rates → policy change → mortality reduction

3. **Completeness**: Ensures mechanism bank captures all evidence-supported pathways

### 13.3 Implementation

```python
# For each node pair (A, B), search both directions

# Forward search: A → B
forward_query = f"{node_A_name} AND {node_B_name} AND causal effect"

# Backward search: B → A
backward_query = f"{node_B_name} causes {node_A_name}"

# Use bidirectional detection script post-extraction
# backend/scripts/create_bidirectional_pairs.py
```

### 13.4 Direction Assignment Rules

Direction is assigned based on **evidence strength**, not arbitrary convention:

1. **Extract from literature**: Let the evidence determine direction
2. **Mark backward mechanisms**: Use `direction: "backward"` field
3. **Create separate files**: Each direction gets its own YAML file
4. **Link bidirectional pairs**: Use `bidirectional_pair_id` field

### 13.5 Mechanism File Naming

```
# Forward mechanism
mechanism-bank/mechanisms/category/node_a_to_node_b.yml

# Backward mechanism (same pathway, reverse direction)
mechanism-bank/mechanisms/category/node_b_to_node_a_backward.yml
```

### 13.6 Evidence Quality for Backward Mechanisms

Backward mechanisms often have different evidence bases:

| Direction | Typical Evidence | Common Grades |
|-----------|-----------------|---------------|
| Forward (Policy→Outcomes) | RCTs, natural experiments | A, B |
| Backward (Outcomes→Determinants) | Observational, time-series | B, C |

> **Note**: Lower evidence quality for backward mechanisms is acceptable—the goal is documenting plausible feedback loops, not proving causation.

### 13.7 Bidirectional Detection Script

```bash
# Run bidirectional detection on new mechanisms
python backend/scripts/create_bidirectional_pairs.py \
    --input mechanism-bank/mechanisms/ \
    --output mechanism-bank/mechanisms/ \
    --search-reverse  # Actively search for reverse direction evidence
```

### 13.8 Supporting Citations Requirement

All mechanisms (forward and backward) require:

- **Minimum 3 supporting citations** per mechanism
- For meta-analyses: Extract citations of 3+ key included studies
- For systematic reviews: Extract 3+ representative primary studies
- For primary studies: Extract 3+ prior studies cited in abstract

---

## Related Documents

- **Schema Definition**: `mechanism-bank/schemas/mechanism_schema_mvp.json`
- **Schema Config**: `backend/config/schema_config.py`
- **Canonical Nodes**: `mechanism-bank/mechanisms/canonical_nodes.json`
- **Node Specifications**: `Nodes/COMPLETE_NODE_INVENTORY.md`
- **Mechanism Bank Structure**: `docs/Core Technical Architecture/05_MECHANISM_BANK_STRUCTURE.md`
- **Effect Quantification (Phase 2)**: `docs/Phase 2 - Quantification/10_LLM_EFFECT_QUANTIFICATION.md`
- **Mechanism Validation**: `docs/LLM & Discovery Pipeline/11_LLM_MECHANISM_VALIDATION.md`
- **Bidirectional Encoding**: `docs/Core Technical Architecture/05_MECHANISM_BANK_STRUCTURE.md#2-bidirectional-mechanism-encoding`

---

**Document Maintainer**: HealthSystems Platform Team
**Last Review**: 2025-12-06
**Next Review**: 2026-03-06
