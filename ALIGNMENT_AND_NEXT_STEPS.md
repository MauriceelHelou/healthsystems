# Alignment with Docs & Critical Next Steps

## Executive Summary

After reviewing the project documentation, I've identified **critical misalignments** between the implemented extraction pipeline and the documented MVP scope. This document outlines what needs to be adjusted, what's missing, and a prioritized action plan.

---

## 🚨 Critical Misalignment: MVP vs. Phase 2 Scope

### The Problem

**Documentation states** ([docs/README.md](docs/README.md), [09_LLM_TOPOLOGY_DISCOVERY.md](docs/LLM%20&%20Discovery%20Pipeline/09_LLM_TOPOLOGY_DISCOVERY.md)):

> **⚠️ MVP Scope: Topology & Direction Only**
>
> **MVP Includes**:
> - ✓ Node identification
> - ✓ Mechanism existence (does A→B exist?)
> - ✓ Directionality (+/−)
> - ✓ Spatial variation flags
> - ✓ Evidence quality
>
> **MVP Excludes** (Phase 2):
> - ✗ Effect size extraction (β = 0.35)
> - ✗ Confidence intervals
> - ✗ Meta-analytic pooling
> - ✗ Quantified moderators

**But our implementation**:
- ✅ Extracts comprehensive quantitative metrics (effect sizes, CIs, meta-analysis metrics)
- ✅ Implements Bayesian weighting (Phase 2 feature per docs)
- ✅ Implements Monte Carlo uncertainty propagation (Phase 2 feature)
- ✅ Extracts moderator multipliers (quantified, not just qualitative)

### The Disconnect

The **LLM prompt** ([llm_mechanism_discovery.py:166-210](backend/pipelines/llm_mechanism_discovery.py#L166-210)) **already extracts Phase 2 quantification**:

```python
# From existing prompt (lines 168-210):
"""
### 5. EXTRACT QUANTITATIVE DATA (Comprehensive - When Available)
Extract ALL statistical measures when present in the abstract:

**PRIMARY EFFECT METRICS:**
- **Effect size value** (the numeric estimate)
- **Effect size type**: OR, RR, HR, beta, SMD...
- **Confidence interval**: Lower and upper bounds
...

**META-ANALYSIS METRICS:**
- **I² statistic**: Heterogeneity percentage
...
"""
```

**This is Phase 2 functionality** according to [10_LLM_EFFECT_QUANTIFICATION.md](docs/Phase%202%20-%20Quantification/10_LLM_EFFECT_QUANTIFICATION.md).

---

## Alignment Assessment

### ✅ **What Aligns with Docs**

| Feature | Docs Requirement | Implementation Status |
|---------|-----------------|----------------------|
| **Literature sources** | PubMed + Semantic Scholar + 15% grey lit | ✅ Implemented |
| **LLM-based extraction** | Claude for mechanism discovery | ✅ Using Claude Sonnet |
| **Node bank** | ~400 nodes, hierarchical levels | ⚠️ Config format ready, needs population |
| **Mechanism bank** | ~100-150 mechanisms per domain | ⚠️ Pipeline ready, needs execution |
| **Evidence grading** | A/B/C/D quality ratings | ✅ Implemented in prompt |
| **Deduplication** | Semantic clustering + consolidation | ❌ Not implemented |
| **Version control** | Git-based lineage tracking | ⚠️ Files created, not integrated |

### ❌ **Critical Gaps**

#### 1. **No Deduplication Pipeline** (Doc 09, Stage 3)

**Docs require** ([09_LLM_TOPOLOGY_DISCOVERY.md:411-486](docs/LLM%20&%20Discovery%20Pipeline/09_LLM_TOPOLOGY_DISCOVERY.md#L411-486)):

```
Stage 3: DEDUPLICATION & CLUSTERING
├─ Input: ~250-350 candidate mechanisms
├─ Process: Semantic clustering + LLM consolidation
├─ Output: ~100-150 deduplicated mechanisms
```

**Current implementation**: Mechanisms saved directly, no deduplication.

**Impact**: Will have duplicate mechanisms with slightly different descriptions from different papers.

#### 2. **No Node Discovery** (Doc 09, Section 4.1)

**Docs require**: LLM extracts node bank from literature corpus.

**Current implementation**: Uses pre-defined nodes from configs.

**Impact**: Misses potentially important nodes not anticipated in configs.

#### 3. **No Inductive Pathway Synthesis** (Doc 09, Stage 2)

**Docs require**: After guided discovery, LLM finds novel mechanisms (feedback loops, interactions).

**Current implementation**: Only processes guided from_node → to_node pairs from configs.

**Impact**: Misses feedback loops, bidirectional effects, and interaction mechanisms.

#### 4. **Quantification Embedded in MVP** (Should be Phase 2)

**Docs say**: Phase 1 = topology only, Phase 2 = quantification.

**Our prompt**: Extracts full quantification in Phase 1.

**Resolution needed**: Either:
- A) **Simplify to MVP scope** (topology + direction only)
- B) **Update docs** to acknowledge integrated quantification

**Recommendation**: Keep integrated quantification (more useful), but add flag to disable for true MVP.

#### 5. **No Bidirectional Mechanism Encoding**

**Docs require** ([05_MECHANISM_BANK_STRUCTURE.md:54-146](docs/Core%20Technical%20Architecture/05_MECHANISM_BANK_STRUCTURE.md#L54-146)):

```yaml
# Must encode A→B and B→A as SEPARATE mechanisms
# Different functional forms, parameters, moderators
```

**Current implementation**: Extracts unidirectional mechanisms only.

**Impact**: Feedback loops not properly modeled.

#### 6. **No Functional Form Assignment**

**Docs require** ([05_MECHANISM_BANK_STRUCTURE.md:146-232](docs/Core%20Technical%20Architecture/05_MECHANISM_BANK_STRUCTURE.md#L146-232)):

- Sigmoid (capacity building)
- Threshold (policy activation)
- Logarithmic (cumulative effects)
- Multiplicative dampening

**Current implementation**: Parameters extracted, but no functional form classification.

**Impact**: Can't translate to Systems Dynamics equations.

---

## What We Built vs. What's Needed

### ✅ **We Built (Good Foundation)**

1. **Generic extraction pipeline** - Topic-agnostic ✅
2. **Grey literature infrastructure** - Curated templates ✅
3. **Quality filtering** - Paper assessment before extraction ✅
4. **Bayesian weighting** - Full implementation (PyMC) ✅
5. **Confidence scoring** - Real-time validation ✅
6. **Batch processing** - Multi-topic parallel extraction ✅
7. **Comprehensive documentation** - Usage guides ✅

### ❌ **Still Missing (Critical for MVP)**

1. **Deduplication pipeline** - Semantic clustering + LLM consolidation
2. **Node discovery** - LLM-based node extraction from corpus
3. **Inductive synthesis** - Finding novel/feedback mechanisms
4. **Functional form classifier** - Assign sigmoid/threshold/etc.
5. **Bidirectional mechanism handler** - Detect and create reverse pathways
6. **Mechanism bank loader** - Load YAML to database
7. **Version control integration** - Git-based lineage tracking
8. **Validation against schema** - Enforce [05_MECHANISM_BANK_STRUCTURE.md](docs/Core%20Technical%20Architecture/05_MECHANISM_BANK_STRUCTURE.md) format

---

## Practical Usage: What Works Now

### ✅ **Ready to Use Today**

```bash
# Extract mechanisms for a topic (with quality filtering)
python backend/scripts/run_generic_extraction_enhanced.py \
  --topic obesity \
  --quality-threshold 0.7 \
  --extract-all-metrics

# Output: YAML files in mechanism-bank/mechanisms/obesity/
```

**What you get**:
- Mechanisms with from_node → to_node
- Direction (+/−)
- Evidence quality (A/B/C/D)
- Quantitative metrics (effect sizes, CIs)
- Supporting studies
- Confidence scores

**What's missing**:
- Duplicates not removed
- No functional forms assigned
- No bidirectional pairs
- Not validated against schema
- Not loaded to database

### ⚠️ **Manual Post-Processing Required**

After extraction, you must manually:

1. **Deduplicate mechanisms**
   - Review similar descriptions
   - Merge redundant entries
   - Keep best evidence

2. **Assign functional forms**
   - Review mechanism description
   - Choose sigmoid/threshold/linear/etc.
   - Add parameters (L, k, x0)

3. **Create bidirectional pairs**
   - Identify feedback loops
   - Create reverse mechanism (B→A)
   - Assign different functional form if needed

4. **Validate against schema**
   - Check [05_MECHANISM_BANK_STRUCTURE.md](docs/Core%20Technical%20Architecture/05_MECHANISM_BANK_STRUCTURE.md) format
   - Add missing fields (moderators, lineage)
   - Fix parameter structures

5. **Load to database**
   - Use API endpoint: `POST /api/mechanisms/admin/load-from-yaml`
   - Verify in database
   - Test in UI

---

## Prioritized Action Plan

### 🔴 **Phase 1: Make MVP Functional** (1-2 weeks)

These are CRITICAL gaps that prevent the pipeline from producing MVP-ready mechanisms.

#### 1.1 Implement Deduplication Pipeline

**What**: [09_LLM_TOPOLOGY_DISCOVERY.md:411-486](docs/LLM%20&%20Discovery%20Pipeline/09_LLM_TOPOLOGY_DISCOVERY.md#L411-486)

```python
# Create: backend/pipelines/mechanism_deduplication.py

def deduplicate_mechanisms(mechanisms: List[MechanismExtraction]) -> List[MechanismExtraction]:
    """
    Stage 3: Semantic clustering + LLM consolidation

    Steps:
    1. Embed mechanism descriptions (SentenceTransformer)
    2. DBSCAN clustering (eps=0.15)
    3. For each cluster with 2+ mechanisms:
       - LLM decides: SAME or VARIANTS
       - If SAME: merge, combine evidence
       - If VARIANTS: keep separate, label contexts

    Returns: Deduplicated mechanisms (~40-50% reduction)
    """
```

**Acceptance criteria**:
- Input: 200 mechanisms → Output: 100-120 mechanisms
- Consolidated evidence from merged mechanisms
- Variants properly labeled

#### 1.2 Implement Functional Form Classifier

**What**: Assign functional forms to extracted mechanisms

```python
# Create: backend/algorithms/functional_form_classifier.py

def classify_functional_form(mechanism: MechanismExtraction) -> str:
    """
    Classify mechanism into functional form based on:
    - Mechanism description (LLM analysis)
    - Node types (capacity vs. rate vs. state)
    - Evidence patterns (saturation, thresholds, linearity)

    Returns: "sigmoid" | "threshold" | "logarithmic" | "multiplicative_dampening" | "linear"
    """
```

**LLM Prompt**:
```
Given this mechanism description, classify into functional form:

DESCRIPTION: {mechanism.mechanism_pathway}
FROM: {from_node} (type: {node_type})
TO: {to_node} (type: {node_type})

FUNCTIONAL FORMS:
1. SIGMOID: Capacity building with saturation (CHW programs, infrastructure)
2. THRESHOLD: Policy activation (eviction protection, minimum threshold)
3. LOGARITHMIC: Cumulative effects with diminishing returns
4. MULTIPLICATIVE_DAMPENING: Proportional to current state
5. LINEAR: Simple proportional relationship

Choose form and justify.
```

#### 1.3 Implement Bidirectional Mechanism Detection

**What**: Identify feedback loops and create reverse mechanisms

```python
# Add to: backend/pipelines/llm_mechanism_discovery.py

def detect_bidirectional_mechanisms(mechanisms: List[MechanismExtraction]) -> List[MechanismExtraction]:
    """
    For each mechanism A→B, check if B→A exists in literature.

    LLM Prompt:
    "Given mechanism A→B, does literature support reverse pathway B→A?
     If yes, extract reverse mechanism with potentially different:
     - Functional form
     - Parameters
     - Moderators"

    Returns: Original mechanisms + reverse mechanisms (where supported)
    """
```

#### 1.4 Create Schema Validator & YAML Generator

**What**: Ensure extracted mechanisms match [05_MECHANISM_BANK_STRUCTURE.md](docs/Core%20Technical%20Architecture/05_MECHANISM_BANK_STRUCTURE.md)

```python
# Create: backend/scripts/validate_mechanism_schema.py

def validate_and_format_mechanism(mechanism: MechanismExtraction, functional_form: str) -> dict:
    """
    Transform LLM extraction to schema-compliant YAML structure:

    Required fields:
    - mechanism_id, direction, from_node, to_node
    - functional_form, equation, parameters
    - moderators (policy, demographic, geographic, implementation)
    - evidence (studies, meta-analysis, confidence)
    - lineage (discovery method, date, reviewers)
    - version, validation

    Returns: Dict ready for YAML export
    """
```

### 🟡 **Phase 2: Add Missing Discovery Features** (2-3 weeks)

#### 2.1 Node Discovery from Corpus

**What**: [09_LLM_TOPOLOGY_DISCOVERY.md:199-256](docs/LLM%20&%20Discovery%20Pipeline/09_LLM_TOPOLOGY_DISCOVERY.md#L199-256)

Let LLM discover nodes from literature (don't just use pre-defined list).

#### 2.2 Inductive Pathway Synthesis

**What**: [09_LLM_TOPOLOGY_DISCOVERY.md:361-409](docs/LLM%20&%20Discovery%20Pipeline/09_LLM_TOPOLOGY_DISCOVERY.md#L361-409)

After guided discovery, run inductive synthesis:
- Feedback loops
- Interaction effects
- Population-specific pathways

#### 2.3 Moderator Quantification

**What**: Currently extracts qualitative moderators, need quantified multipliers

Example:
```yaml
moderators:
  policy:
    - factor: "medicaid_work_requirements"
      present: -0.08  # ← Need to extract these numbers
      absent: +0.08
```

### 🟢 **Phase 3: Production Hardening** (1-2 weeks)

#### 3.1 Database Integration

- Create database schema for mechanisms
- Implement loader: `POST /api/mechanisms/admin/load-from-yaml`
- Add API endpoints for querying mechanisms

#### 3.2 Git-Based Version Control

- Implement lineage tracking
- Git commit hooks for mechanism changes
- Automated validation on PR

#### 3.3 Dashboard & Monitoring

- Extraction analytics dashboard
- Quality metrics over time
- Mechanism coverage by topic

---

## Recommended Immediate Actions

### Option A: "Quick Production" (Use What Works)

**Timeline**: 1 week

1. Run extraction for 5 topics with enhanced script
2. Manually deduplicate (review and merge)
3. Manually assign functional forms (use LLM assist)
4. Manually create bidirectional pairs (where obvious)
5. Load to database
6. Deploy MVP

**Pros**: Fast path to working MVP
**Cons**: Manual work, not scalable

### Option B: "Build Missing Pipeline" (Proper Implementation)

**Timeline**: 4-6 weeks

1. Implement deduplication pipeline (Week 1)
2. Implement functional form classifier (Week 2)
3. Implement bidirectional detection (Week 2)
4. Implement schema validator (Week 3)
5. Run full extraction + validation (Week 4)
6. Implement node discovery (Week 5)
7. Implement inductive synthesis (Week 6)
8. Deploy MVP

**Pros**: Scalable, automated, follows docs
**Cons**: Longer timeline

### Option C: "Hybrid" (Recommended)

**Timeline**: 2-3 weeks

**Week 1**: Build critical automation
- Deduplication pipeline
- Functional form classifier
- Schema validator

**Week 2**: Run extraction + validate
- Extract 5 topics
- Auto-deduplicate
- Auto-assign functional forms
- Manual review of bidirectional needs
- Load to database

**Week 3**: Deploy MVP + start Phase 2 features
- MVP deployed with working mechanisms
- Begin node discovery implementation
- Begin inductive synthesis

---

## Decision Matrix

| Criterion | Option A (Quick) | Option B (Proper) | Option C (Hybrid) |
|-----------|------------------|-------------------|-------------------|
| **Time to MVP** | 1 week | 6 weeks | 3 weeks |
| **Automation** | Low | High | Medium |
| **Scalability** | Poor | Excellent | Good |
| **Follows docs** | Partial | Full | Mostly |
| **Manual work** | High | Minimal | Some |
| **Risk** | Manual errors | Longer timeline | Balanced |
| **Recommendation** | ❌ Not sustainable | ✅ If time permits | ✅✅ **BEST** |

---

## Summary: What's Working, What's Not

### ✅ **Working Well**

- Generic extraction infrastructure
- Quality filtering (saves 30-50% cost)
- Grey literature framework
- Quantitative metrics extraction
- Bayesian weighting
- Comprehensive documentation

### ❌ **Critical Gaps**

- **No deduplication** (will have duplicates)
- **No functional forms** (can't use in Systems Dynamics)
- **No bidirectional** (feedback loops missing)
- **No schema validation** (won't match database)
- **Manual post-processing required**

### 🎯 **Recommended Path Forward**

**Implement Option C (Hybrid)**:

**Week 1**:
1. Build deduplication pipeline
2. Build functional form classifier
3. Build schema validator

**Week 2**:
1. Extract 5 topics (obesity, diabetes, mental_health, cardiovascular, respiratory)
2. Auto-deduplicate
3. Auto-assign functional forms
4. Manual review for bidirectional needs
5. Validate against schema

**Week 3**:
1. Load to database
2. Deploy MVP
3. Begin Phase 2 features (node discovery, inductive synthesis)

**Outcome**: Working MVP in 3 weeks with proper automation for future topics.

---

## Files That Need to Be Created

### Critical (Week 1)

1. `backend/pipelines/mechanism_deduplication.py`
2. `backend/algorithms/functional_form_classifier.py`
3. `backend/scripts/validate_mechanism_schema.py`
4. `backend/scripts/create_bidirectional_pairs.py`

### Important (Week 2-3)

5. `backend/pipelines/node_discovery.py`
6. `backend/pipelines/inductive_synthesis.py`
7. `backend/api/routes/mechanism_loader.py`
8. `backend/models/mechanism.py` (SQLAlchemy model)

### Nice-to-Have (Week 4+)

9. `backend/dashboards/extraction_analytics.py`
10. `backend/scripts/git_lineage_tracker.py`

---

## Conclusion

**We have a strong foundation** with the generic extraction pipeline, quality filtering, and grey literature support. However, **critical gaps remain** before it's MVP-ready:

1. **Deduplication** - Will have duplicates without this
2. **Functional forms** - Can't use in Systems Dynamics without this
3. **Schema validation** - Won't load to database without this

**Recommended**: **Option C (Hybrid)** - 3-week timeline to working MVP with key automation in place.

The enhanced extraction script is production-quality for **research extraction**, but needs **deduplication, functional form assignment, and schema validation** to be MVP-ready for the **HealthSystems Platform**.
