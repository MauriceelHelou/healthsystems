# 09: LLM Topology Discovery
**Literature-Driven Node and Edge Generation**

---

## ⚠️ MVP Scope: Topology & Direction Only

**This document describes MVP functionality**: Discovering which mechanisms exist and their direction (+/−).

**MVP Includes**:
- ✓ Node identification (what variables exist)
- ✓ Mechanism existence (does pathway A→B exist in literature?)
- ✓ Directionality (positive or negative relationship)
- ✓ Spatial variation flags (geographic differences noted)
- ✓ Evidence quality (strong/moderate/limited)

**MVP Excludes** (deferred to Phase 2):
- ✗ Effect size extraction (exact magnitudes like β = 0.35)
- ✗ Confidence intervals
- ✗ Meta-analytic pooling (see Document 10 in Phase 2)
- ✗ Quantified moderators (see Document 08 in Phase 2)

**See**: `docs/Phase 2 - Quantification/10_LLM_EFFECT_QUANTIFICATION.md` for effect size extraction specifications.

---

## 1. Overview

This document specifies how Large Language Models (LLMs) systematically extract causal pathways from academic literature to construct the **mechanism bank**: a structured database of ~2000 mechanisms connecting ~400 nodes. The process converts unstructured epidemiological knowledge into a versioned, auditable network topology that grounds the platform in empirical evidence.

**Core Innovation**: LLM-mediated synthesis scales literature review from months-per-mechanism (traditional expert curation) to days-for-entire-bank, while maintaining traceability to source studies and enabling continuous refinement.

**MVP Focus**: Topology (which nodes connect) and direction (+/−), NOT effect magnitude.

---

## 2. Architecture Overview

### 2.1 Three-Stage Discovery Pipeline

```
Stage 1: GUIDED TOPOLOGY DISCOVERY
├─ Input: 300-500 PDFs + abstracts (PubMed, Google Scholar, grey literature)
├─ Process: LLM identifies node-to-node connections using structured prompts
├─ Output: ~200-300 candidate mechanisms (with redundancy)
└─ Duration: 2-3 days with Claude Opus 4

Stage 2: INDUCTIVE PATHWAY SYNTHESIS  
├─ Input: Literature corpus + Stage 1 mechanisms
├─ Process: LLM discovers novel pathways not captured by guided prompts
├─ Output: ~20-50 additional mechanisms (feedback loops, interaction effects)
└─ Duration: 1 day

Stage 3: DEDUPLICATION & CLUSTERING
├─ Input: ~250-350 candidate mechanisms
├─ Process: Semantic clustering + LLM consolidation
├─ Output: ~100-150 deduplicated mechanisms per geographic domain
└─ Duration: 1-2 days

Total: ~5-7 days from literature corpus to mechanism bank v1.0
```

**Iteration**: Mechanism bank evolves through quarterly updates as new literature emerges and expert feedback accumulates.

---

## 3. Literature Corpus Management

### 3.1 Source Selection

**Primary Sources** (85% of corpus):
```
PubMed/MEDLINE:
├─ MeSH terms: "Social Determinants of Health", "Health Equity", "Housing and Health", 
│                "Community Health Workers", "Food Security", "Eviction", "Incarceration and Health"
├─ Publication types: RCT, Cohort Study, Cross-Sectional Study, Systematic Review
├─ Date range: 2000-present (emphasize 2015+)
└─ Language: English (MVP), Spanish (Phase 2)

Google Scholar / Institutional Repositories:
├─ Urban planning journals (housing, transportation, built environment)
├─ Sociology (racial capitalism, neighborhood effects, social cohesion)
├─ Economics (labor markets, income inequality, housing markets)
└─ Policy evaluations (Medicaid expansion, minimum wage, eviction protections)
```

**Grey Literature** (15% of corpus):
```
Government reports (CDC, HUD, DOJ)
Foundation evaluations (Robert Wood Johnson, Annie E. Casey, Ford)
Think tank briefs (Urban Institute, Brookings, Center for Budget Priorities)
Community-based research (participatory action research with non-profits)
```

**Exclusion Criteria**:
- Predatory journals (use Beall's List)
- Retracted articles
- Opinion pieces without empirical data
- Studies with N < 30 (insufficient statistical power)

---

### 3.2 Document Preprocessing

**Step 1: PDF Text Extraction**
```python
# Extract text from PDFs using OCR + structure parsing
for document in corpus:
    if document.type == "pdf":
        text = extract_pdf_text(document)  # pypdf2 or similar
        sections = parse_sections(text)    # Identify abstract, methods, results
    elif document.type == "abstract_only":
        text = document.abstract
        sections = {"abstract": text}
    
    # Quality check
    if len(text) < 500:  # Too short; likely extraction failure
        flag_for_manual_review(document)
```

**Step 2: Chunk Creation**
```python
# Chunk documents for LLM processing (≤8K tokens per chunk for Claude)
chunks = []
for section in ["abstract", "methods", "results", "discussion"]:
    if section in document.sections:
        chunks.extend(
            chunk_by_sentences(
                document.sections[section],
                max_tokens=1500,
                overlap=200  # Preserve context across chunks
            )
        )
```

**Step 3: Metadata Annotation**
```json
{
  "chunk_id": "smith_2022_abstract_001",
  "source_document": {
    "authors": ["Smith, J.", "Jones, A.", "Brown, K."],
    "year": 2022,
    "title": "Community Health Workers and Healthcare Access",
    "journal": "American Journal of Public Health",
    "doi": "10.2105/AJPH.2022.306798",
    "study_design": "RCT",
    "sample_size": 3200,
    "population": "Low-income adults, urban setting",
    "geographic_context": "Boston, MA"
  },
  "chunk_text": "...",
  "chunk_position": 1,
  "total_chunks": 12
}
```

**Step 4: Embedding & Indexing**
```python
# Create vector embeddings for semantic search
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')  # Lightweight, fast
embeddings = model.encode([chunk['chunk_text'] for chunk in chunks])

# Store in vector database (Pinecone, Weaviate, or FAISS)
vector_db.upsert(
    ids=[chunk['chunk_id'] for chunk in chunks],
    vectors=embeddings,
    metadata=[chunk['source_document'] for chunk in chunks]
)
```

**Output**: Searchable literature corpus (~50-100GB) ready for LLM queries

---

## 4. Stage 1: Guided Topology Discovery

### 4.1 Node Bank Initialization

**Node Hierarchy Framework**:
```
Level 1 (Macro-Structural): Federal/state policies, economic systems
  Examples: Medicaid design, housing policy, minimum wage law, carceral policy
  
Level 2 (Local-Structural): Municipal policies, built environment, market conditions
  Examples: Zoning, transit systems, clinic density, housing market tightness
  
Level 3 (Proximal Conditions): Household/individual exposures
  Examples: Housing quality, employment stability, healthcare access, food security
  
Level 4 (Physiological Pathways): Disease states, biomarkers, health behaviors
  Examples: Chronic stress, hypertension, depression, substance use
  
Level 5 (Crisis Endpoints): Acute events requiring intervention
  Examples: ED visits, hospitalizations, arrests, evictions, premature death
```

**LLM Prompt: Node Extraction**
```
SYSTEM: You are a public health researcher analyzing literature on structural determinants of health.

TASK: From the provided literature corpus, extract ALL distinct SYSTEM NODES (states, conditions, or outcomes) that appear in causal pathways linking structural policies to health outcomes.

For EACH node, provide:
1. node_name: Descriptive label (e.g., "Community_Health_Workers")
2. node_level: Hierarchical position (1=macro-policy, 2=local-structural, 3=proximal, 4=physiological, 5=crisis)
3. capacity_unit: How this node is measured
   - Counted resources: "# of full-time workers", "# of housing units"
   - Rates/percentages: "% population with insurance", "eviction rate per 1000 renters"
   - Index scores: "0-1 index" for qualitative constructs (e.g., "community cohesion")
   - Policy strength: "0-10 scale" for regulatory intensity
4. baseline_description: Typical values in US urban contexts
5. measurement_source: Where baseline data comes from (Census, CDC, local administrative data)

CONSTRAINTS:
- Focus on structural nodes (not individual behaviors unless mediated by structural conditions)
- Nodes must be intervention-relevant (can be changed through policy/programs)
- Avoid overly granular nodes ("asthma" is too specific; use "respiratory_disease")
- Combine conceptually equivalent nodes (e.g., "healthcare access" encompasses "appointment availability", "insurance coverage", "geographic proximity")

OUTPUT: JSON array of nodes
[
  {
    "node_name": "Community_Health_Workers",
    "node_level": 2,
    "capacity_unit": "FTE count per 10,000 population",
    "baseline_description": "Boston: ~1.2 CHW per 10,000 low-income residents",
    "measurement_source": "Health Resources & Services Administration (HRSA) data",
    "structural_origin": "Healthcare workforce policy, community-based organization funding"
  },
  ...
]

DO NOT include explanatory text. Output only valid JSON.
```

**LLM Processing**:
```python
# Call LLM with full literature corpus context
response = call_llm(
    model="claude-opus-4",
    system_prompt=NODE_EXTRACTION_PROMPT,
    user_context=retrieve_relevant_chunks(
        query="structural determinants health outcomes causal pathways",
        top_k=50  # Retrieve 50 most relevant chunks
    ),
    max_tokens=8000,
    temperature=0.2  # Low temperature for consistency
)

nodes_raw = json.loads(response)
```

**Output**: ~400-500 candidate nodes (before deduplication)

---

### 4.2 Mechanism Extraction (Edge Discovery)

**LLM Prompt: Guided Pathway Extraction**
```
SYSTEM: You are identifying causal mechanisms linking structural determinants to health outcomes.

CONTEXT: You have access to 300+ peer-reviewed studies on social determinants of health. Focus on mechanisms with empirical support (not theoretical speculation).

TASK: For each node-to-node connection below, determine if a causal mechanism exists in the literature. If yes, extract:
1. source_node: Starting node (e.g., "Housing_Quality")
2. target_node: Ending node (e.g., "Respiratory_Health")
3. mechanism_description: 2-3 sentence explanation of causal pathway
4. supporting_studies: List 2-3 key studies with [authors, year, study_design, sample_size] (qualitative reference only)
5. evidence_strength: "strong" (RCT or meta-analysis), "moderate" (multiple cohorts), "limited" (single observational study)
6. directionality: "positive" (source increases target) or "negative" (source decreases target)
7. spatial_variation: true/false - Does literature note that effect varies by geography, urbanicity, state policy context, or population characteristics?

**MVP Note**: Do NOT extract exact effect sizes, confidence intervals, or quantified moderators. Focus on existence, direction, and qualitative variation only.

GUIDED CONNECTIONS (check each):
Level 1 → Level 2:
- Medicaid_Work_Requirements → Employment_Precarity
- Just_Cause_Eviction_Law → Housing_Stability
- Minimum_Wage_Policy → Income_Security

Level 2 → Level 3:
- Housing_Market_Tightness → Housing_Affordability
- Community_Health_Workers → Healthcare_Continuity
- Public_Transit_Access → Employment_Stability

Level 3 → Level 4:
- Housing_Quality → Respiratory_Health
- Food_Security → Chronic_Stress
- Healthcare_Continuity → Chronic_Disease_Management

Level 4 → Level 5:
- Chronic_Stress → Cardiovascular_Disease
- Substance_Use → Overdose_Events
- Chronic_Disease_Burden → ED_Utilization

[Provide 50-100 guided connections across all level transitions]

OUTPUT: JSON array with only connections that have literature support
[
  {
    "source_node": "Housing_Quality",
    "target_node": "Respiratory_Health",
    "mechanism_description": "Poor housing quality (mold, inadequate ventilation, pest infestation) increases exposure to allergens and irritants, triggering asthma exacerbations and respiratory infections.",
    "supporting_studies": [
      {
        "authors": "Krieger et al.",
        "year": 2005,
        "study_design": "RCT",
        "sample_size": 274,
        "doi": "10.2105/AJPH.2004.042069"
      },
      {
        "authors": "Sandel et al.",
        "year": 2010,
        "study_design": "Cohort",
        "sample_size": 1842,
        "doi": "10.1542/peds.2009-3827"
      }
    ],
    "evidence_strength": "strong",
    "directionality": "negative",
    "spatial_variation": true,
    "spatial_variation_note": "Effect stronger in humid climates and older housing stock"
  },
  ...
]

**MVP Note**: Effect sizes (e.g., OR = 1.34) are extracted in Phase 2 only. See Document 10.
```

**Semantic Search Enhancement**:
```python
# For each guided connection, retrieve supporting literature
for connection in guided_connections:
    query = f"{connection['source_node']} affect {connection['target_node']} health mechanism"
    relevant_chunks = vector_db.search(
        query_embedding=model.encode(query),
        top_k=10,
        filter_metadata={"study_design": ["RCT", "Cohort"]}  # Prioritize higher-quality studies
    )
    
    # Pass relevant chunks to LLM for mechanism extraction
    mechanism = call_llm(
        model="claude-opus-4",
        prompt=MECHANISM_EXTRACTION_PROMPT,
        context=relevant_chunks,
        connection=connection
    )
    
    if mechanism:  # Literature supports this connection
        mechanisms_discovered.append(mechanism)
```

**Output**: ~200-300 mechanisms with literature citations

---

## 5. Stage 2: Inductive Pathway Synthesis

### 5.1 Discovering Novel Mechanisms

**LLM Prompt: Inductive Discovery**
```
SYSTEM: You are identifying causal mechanisms NOT captured by the guided discovery process.

CONTEXT: You have analyzed 300+ studies and extracted 200+ mechanisms linking structural policies to health. However, some important pathways may have been missed.

TASK: Identify 10-20 NOVEL mechanisms that:
1. Involve feedback loops (downstream effects influencing upstream conditions)
   Example: Health crises → job loss → housing instability → worse health
2. Capture interaction effects (two policies/conditions together produce non-additive effects)
   Example: Medicaid expansion + community health workers = synergistic improvement (not just additive)
3. Reveal population-specific pathways (mechanism differs by race, age, immigration status)
   Example: Police contact → health differently for Black vs. White populations
4. Describe temporal dynamics (immediate vs. cumulative vs. intergenerational effects)
   Example: Lead exposure → cognitive impairment (immediate) → educational outcomes (5 years) → employment (15 years)
5. Identify geographic variations (urban vs. rural; high vs. low segregation)
   Example: Community organizing more effective in high-density neighborhoods

For EACH novel mechanism, provide:
- Full pathway description
- Why this wasn't captured by guided discovery
- Supporting literature (if available) or theoretical justification
- Uncertainty level: "established" (multiple studies), "emerging" (1-2 studies), "theoretical" (plausible but limited evidence)

OUTPUT: JSON array of novel mechanisms
```

**Bidirectional Edge Discovery**:
```python
# Identify upstream feedback effects
for mechanism in mechanisms_discovered:
    target = mechanism['target_node']
    source = mechanism['source_node']
    
    # Search for reverse pathway
    reverse_query = f"How does {target} affect {source}? Feedback effects?"
    reverse_evidence = vector_db.search(query_embedding=model.encode(reverse_query), top_k=5)
    
    if has_sufficient_evidence(reverse_evidence):
        reverse_mechanism = extract_mechanism(source=target, target=source, evidence=reverse_evidence)
        mechanisms_discovered.append(reverse_mechanism)
```

**Output**: ~20-50 novel mechanisms (feedback loops, interactions, population-specific)

---

## 6. Stage 3: Deduplication & Consolidation

### 6.1 Semantic Clustering

**Objective**: Reduce ~250-350 candidate mechanisms to ~100-150 distinct pathways by identifying redundant descriptions of the same underlying mechanism.

```python
from sklearn.cluster import DBSCAN
import numpy as np

# Embed all mechanism descriptions
embeddings = model.encode([m['mechanism_description'] for m in mechanisms_discovered])

# Cluster semantically similar mechanisms
clustering = DBSCAN(
    eps=0.15,      # Similarity threshold (lower = tighter clusters)
    min_samples=1  # Allow singleton clusters (unique mechanisms)
).fit(embeddings)

# Group mechanisms by cluster
clusters = {}
for idx, label in enumerate(clustering.labels_):
    if label not in clusters:
        clusters[label] = []
    clusters[label].append(mechanisms_discovered[idx])

print(f"Discovered: {len(mechanisms_discovered)} mechanisms")
print(f"Clustered into: {len(clusters)} groups")
```

### 6.2 LLM-Guided Consolidation

**For each cluster with 2+ mechanisms**:

```
SYSTEM: You are consolidating redundant mechanism descriptions.

TASK: These mechanisms appear semantically similar. Determine:
1. Are they describing the SAME mechanism (different studies, same causal pathway)?
2. Are they VARIANTS (mechanism operates differently in different contexts)?

If SAME:
- Select the most precise description
- Merge supporting studies from all versions
- Create unified mechanism entry with combined evidence base

If VARIANTS:
- Keep separate entries
- Label as: "mechanism_name_variant_A", "mechanism_name_variant_B"
- Document conditions differentiating variants (e.g., urban vs. rural, policy context)

MECHANISMS:
{cluster_mechanisms_json}

OUTPUT: JSON decision
{
  "decision": "merge" | "keep_separate",
  "reasoning": "...",
  "consolidated_mechanism": {
    "mechanism_description": "...",
    "supporting_studies": [merged_list],
    "variants_noted": ["context A: stronger effect", "context B: weaker effect"]
  }
}
```

**Post-Consolidation Statistics**:
```python
# After consolidation
mechanisms_deduplicated = consolidate_clusters(clusters)

print(f"Final mechanism count: {len(mechanisms_deduplicated)}")
print(f"Redundancy reduction: {(1 - len(mechanisms_deduplicated)/len(mechanisms_discovered))*100:.1f}%")
```

**Typical Output**: ~100-150 mechanisms (40-50% reduction from initial discovery)

---

## 7. Node Bank Construction

### 7.1 Node Deduplication

**Objective**: Consolidate ~400-500 candidate nodes to ~400 final nodes by merging conceptually equivalent nodes and removing orphans.

```python
# Step 1: Semantic clustering of node names
node_embeddings = model.encode([n['node_name'] for n in nodes_raw])
node_clusters = DBSCAN(eps=0.12, min_samples=1).fit(node_embeddings)

# Step 2: LLM consolidation (same process as mechanisms)
for cluster in node_clusters:
    if len(cluster) > 1:
        decision = consolidate_nodes_llm(cluster)
        if decision['merge']:
            merged_node = create_merged_node(cluster, decision)
            nodes_final.append(merged_node)
        else:
            nodes_final.extend(cluster)  # Keep separate

# Step 3: Remove orphan nodes (no incoming or outgoing mechanisms)
nodes_final = [n for n in nodes_final if has_connections(n, mechanisms_deduplicated)]
```

### 7.2 Node Bank Structure

```json
{
  "node_id": "L2.014_community_health_workers",
  "node_name": "Community Health Workers",
  "node_level": 2,
  "capacity_unit": "FTE count per 10,000 population",
  "capacity_type": "infrastructure",
  "baseline_values": {
    "boston_ma": 1.2,
    "rural_mississippi": 0.3,
    "national_average": 0.8
  },
  "measurement_sources": [
    "HRSA Workforce Data",
    "State health department registries"
  ],
  "structural_origin": "Healthcare workforce policy; community health center funding (FQHC)",
  "functional_form_default": "sigmoid",
  "functional_form_rationale": "CHW effects saturate at high density (diminishing returns per additional worker)"
}
```

**Functional Form Assignment**:
- **Sigmoid**: Capacity building (workforce, infrastructure) with saturation
- **Logarithmic**: Resource accumulation with diminishing returns
- **Saturating Linear**: Hard physical limits (housing units, hospital beds)
- **Threshold-Activated**: Policy changes with activation points
- **Multiplicative Dampening**: Relative changes (percentages, rates)

---

## 8. Evidence Strength Assessment

### 8.1 Study Quality Scoring

```python
def assess_evidence_strength(supporting_studies):
    """
    Aggregate study quality into evidence strength rating
    """
    quality_points = 0
    total_n = 0
    
    for study in supporting_studies:
        # Study design points
        design_score = {
            "RCT": 4,
            "Cohort_Prospective": 3.5,
            "Cohort_Retrospective": 3,
            "Cross_Sectional": 2,
            "Qualitative": 1
        }[study['study_design']]
        
        # Sample size weight
        n_weight = np.log10(study['sample_size']) / 4  # Normalize to ~1 for n=10,000
        
        quality_points += design_score * n_weight
        total_n += study['sample_size']
    
    # Average quality across studies
    avg_quality = quality_points / len(supporting_studies)
    
    # Classify evidence strength
    if avg_quality >= 3.5 and len(supporting_studies) >= 3:
        return "strong"
    elif avg_quality >= 2.5 or (avg_quality >= 2.0 and len(supporting_studies) >= 5):
        return "moderate"
    else:
        return "limited"
```

### 8.2 Consistency Assessment

```python
def assess_consistency(supporting_studies):
    """
    Check if studies agree on directionality and magnitude
    """
    effect_directions = [s['effect_direction'] for s in supporting_studies]
    
    # All same direction?
    if len(set(effect_directions)) == 1:
        consistency = "high"
    elif effect_directions.count(max(set(effect_directions), key=effect_directions.count)) / len(effect_directions) >= 0.8:
        consistency = "moderate"
    else:
        consistency = "low"
    
    return consistency
```

**Flagging Rules**:
```
If evidence_strength == "limited" AND consistency == "low":
  → Flag: "UNCERTAIN - Requires expert review or additional literature"
  → Action: Use with caution; wide confidence intervals

If evidence_strength == "strong" AND consistency == "high":
  → Status: "VALIDATED - High confidence for use in projections"
  → Action: Core mechanism for MVP
```

---

## 9. Mechanism Bank Versioning

### 9.1 Version Control Schema

```json
{
  "mechanism_bank_version": "1.0.0",
  "release_date": "2026-01-15",
  "total_mechanisms": 147,
  "total_nodes": 423,
  "literature_corpus_version": "2025Q4",
  "llm_model": "claude-opus-4",
  "discovery_prompts_version": "1.2",
  "changelog": [
    {
      "version": "1.0.0",
      "changes": "Initial release post-deduplication",
      "mechanisms_added": 147,
      "mechanisms_removed": 0,
      "mechanisms_modified": 0
    }
  ]
}
```

### 9.2 Git-Based Lineage Tracking

```bash
# Each mechanism stored as separate JSON file
mechanism_bank/
├─ L1_to_L2/
│  ├─ medicaid_work_req_to_employment_precarity.json
│  └─ minimum_wage_to_income_security.json
├─ L2_to_L3/
│  ├─ chw_to_healthcare_continuity.json
│  └─ housing_market_to_affordability.json
└─ L3_to_L4/
   └─ housing_quality_to_respiratory_health.json

# Git commit messages trace changes
git log mechanism_bank/L2_to_L3/chw_to_healthcare_continuity.json
  commit a3f2c1: Updated effect size (0.32 → 0.35) based on new meta-analysis
  commit b8d4e9: Added moderator: clinic_integration (1.3× multiplier)
  commit c1a5f3: Initial discovery from literature synthesis
```

### 9.3 Audit Trail Requirements

Every mechanism includes:
```json
{
  "mechanism_id": "L2_014_to_L3_028",
  "discovery_metadata": {
    "discovered_by": "llm_guided_stage1",
    "llm_model": "claude-opus-4",
    "prompt_version": "1.2",
    "discovery_date": "2025-11-10",
    "literature_chunks_used": [
      "smith_2022_abstract_001",
      "jones_2020_results_003"
    ]
  },
  "validation_history": [
    {
      "date": "2025-11-12",
      "action": "automated_qa_passed",
      "checks": ["direction_consistency", "effect_size_plausibility", "citation_validity"]
    },
    {
      "date": "2025-12-01",
      "action": "effect_size_updated",
      "reason": "New RCT published; updated meta-analysis",
      "previous_value": 0.32,
      "new_value": 0.35
    }
  ]
}
```

---

## 10. Quality Assurance Checkpoints

### 10.1 Automated Validation

```python
def validate_mechanism_bank(mechanisms, nodes):
    """
    Run automated checks before deployment
    """
    errors = []
    warnings = []
    
    for mech in mechanisms:
        # Check 1: Both nodes exist
        if not (node_exists(mech['source_node'], nodes) and 
                node_exists(mech['target_node'], nodes)):
            errors.append(f"{mech['mechanism_id']}: Referenced node not in node bank")
        
        # Check 2: No self-loops
        if mech['source_node'] == mech['target_node']:
            errors.append(f"{mech['mechanism_id']}: Self-loop detected")
        
        # Check 3: Direction consistency
        if mech['directionality'] == "positive" and mech['mechanism_description'].lower().count("reduce") > 0:
            warnings.append(f"{mech['mechanism_id']}: Direction may be mislabeled")
        
        # Check 4: Literature citations resolve
        for study in mech['supporting_studies']:
            if not validate_doi(study['doi']):
                warnings.append(f"{mech['mechanism_id']}: Invalid DOI {study['doi']}")
        
        # Check 5: Evidence strength matches study count
        if mech['evidence_strength'] == "strong" and len(mech['supporting_studies']) < 3:
            warnings.append(f"{mech['mechanism_id']}: 'strong' evidence but <3 studies")
    
    return {"errors": errors, "warnings": warnings}
```

**Deployment Gate**: Mechanism bank releases only if `len(errors) == 0`.

---

### 10.2 Network Topology Validation

```python
# Check for disconnected components
import networkx as nx

G = nx.DiGraph()
for mech in mechanisms:
    G.add_edge(mech['source_node'], mech['target_node'])

# All nodes reachable from Level 1 (policy) nodes?
policy_nodes = [n for n in nodes if n['node_level'] == 1]
reachable = set()
for policy_node in policy_nodes:
    reachable.update(nx.descendants(G, policy_node))

unreachable = set(nodes) - reachable - set(policy_nodes)
if len(unreachable) > 0:
    print(f"WARNING: {len(unreachable)} nodes not reachable from policy interventions")
    print(f"Orphaned nodes: {unreachable}")
```

---

## 11. MVP Implementation Priorities

**Phase 1 (MVP)**:
- Single literature corpus synthesis (~300 papers)
- Claude Opus 4 for all LLM tasks
- Guided discovery + inductive synthesis (Stages 1-2)
- Semantic clustering with DBSCAN (eps=0.15)
- Manual consolidation for ambiguous clusters
- Target: 100-150 mechanisms, 400 nodes
- Evidence strength assessment (automated)
- Version 1.0 release

**Phase 2 Enhancements**:
- Continuous literature monitoring (quarterly updates)
- Multi-language corpus (Spanish, Mandarin)
- Advanced clustering (hierarchical, spectral methods)
- Automated consolidation (LLM-only, no manual review)
- Geographic-specific mechanism banks (Boston, Chicago, Atlanta)
- Version 2.0+ with differential mechanism activation by geography

---

## 12. Integration with Effect Quantification

**Handoff to Document 10**:

Once mechanisms are discovered and deduplicated, each mechanism passes to the **Effect Quantification Pipeline** (Document 10) where:
1. Effect sizes are extracted from supporting studies
2. Meta-analytic pooling generates point estimates and confidence intervals
3. Moderators are identified and quantified
4. Population stratification is encoded
5. Final mechanism records are created with complete parameter sets

**Data Flow**:
```
09_LLM_TOPOLOGY_DISCOVERY.md
  ↓ (Mechanisms with literature citations)
10_LLM_EFFECT_QUANTIFICATION.md
  ↓ (Mechanisms with effect sizes + CIs)
08_EFFECT_SIZE_TRANSLATION.md
  ↓ (Mechanisms with SD parameters)
05_MECHANISM_BANK_STRUCTURE.md
  ↓ (Complete mechanism bank deployed)
```

---

**Document Version**: 1.0  
**Cross-References**: `[10_LLM_EFFECT_QUANTIFICATION.md]`, `[08_EFFECT_SIZE_TRANSLATION.md]`, `[05_MECHANISM_BANK_STRUCTURE.md]`, `[11_LLM_MECHANISM_VALIDATION.md]`  
**Status**: Technical specification for MVP implementation
