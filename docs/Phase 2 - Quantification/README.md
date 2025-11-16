# Phase 2: Quantification & Uncertainty

This directory contains specifications for quantitative capabilities deferred from MVP. **MVP focuses on identifying WHAT mechanisms exist and their DIRECTION**. Phase 2 adds **HOW MUCH** effect they have.

## MVP Delivers (Phase 1)

### Topology & Direction Only
- ✓ **Mechanism topology**: Which nodes connect to which
- ✓ **Directionality**: Positive or negative relationship
- ✓ **Qualitative spatial variation**: Flag when papers note geographic differences
- ✓ **2000 mechanisms catalogued**: Complete network structure

### What MVP Does NOT Include
- ✗ Exact effect sizes (e.g., β = 0.35)
- ✗ Confidence intervals
- ✗ Meta-analytic pooling
- ✗ Bayesian synthesis
- ✗ Quantified moderators (e.g., "1.30× for urban settings")
- ✗ Monte Carlo uncertainty propagation

**MVP Rationale**: Establishing the complete topology and directionality of 2000+ mechanisms is foundational. Quantification requires this structure to be in place first.

---

## Phase 2 Adds Quantification

### Exact Effect Estimation
Once topology is established, Phase 2 will add:

1. **Effect Size Extraction**
   - Parse OR, RR, β, HR, %, d from literature
   - Standardize all to Cohen's d
   - Extract confidence intervals

2. **Meta-Analytic Pooling**
   - Fixed-effects pooling (inverse-variance weighted)
   - Random-effects pooling (DerSimonian-Laird)
   - Heterogeneity assessment (I² statistic)
   - Publication bias detection (Egger's test)

3. **Bayesian Synthesis**
   - Informative priors by mechanism type
   - MCMC sampling for posterior distributions
   - Credible intervals (95%)
   - Prediction intervals accounting for heterogeneity
   - Posterior samples (2000 draws) for Monte Carlo

4. **Moderator Quantification**
   - Exact multipliers (e.g., urban setting = 1.30×)
   - Subgroup meta-analysis
   - Meta-regression for continuous moderators
   - Context-specific effect adjustments

5. **Uncertainty Propagation**
   - Monte Carlo simulation through causal chains
   - Confidence intervals on all projections
   - Sensitivity analysis
   - Full probabilistic forecasting

6. **Stock-Flow Parameter Calculation**
   - α parameter derivation from effect sizes
   - Functional form calibration (sigmoid, threshold, log)
   - Equilibrium solver with quantified effects
   - Time-series simulation with exact dynamics

---

## Documents in This Directory

### **08_EFFECT_SIZE_TRANSLATION.md**
**Purpose**: Convert diverse effect size formats to Cohen's d

**Content**:
- Conversion formulas: OR → d, RR → d, β → d, HR → d, r → d, % → d
- Confidence interval propagation
- Three translation approaches for SD parameters
- Moderator adjustment mathematics
- Worked examples with real studies

**When to Use**: Phase 2 implementation of effect quantification

---

### **10_LLM_EFFECT_QUANTIFICATION.md**
**Purpose**: LLM-based pipeline for extracting and pooling effect sizes

**Content**:
- Stage 1: Effect size extraction prompts
- Stage 2: Standardization to Cohen's d
- Stage 3: Meta-analytic pooling (fixed/random)
- Stage 4: Bayesian synthesis with MCMC
- Publication bias detection
- Heterogeneity assessment
- Quality control validation

**When to Use**: Phase 2 automation of literature synthesis

---

### **02B_BAYESIAN_METHODOLOGY.md** (to be created)
**Purpose**: Bayesian inference methodology for uncertainty quantification

**Content**:
- Prior specification by mechanism type
- MCMC sampling procedures
- Posterior distribution interpretation
- Credible interval calculation
- Prediction intervals
- Prior sensitivity analysis
- Integration with meta-analysis

**When to Use**: Phase 2 Bayesian implementation

---

## Implementation Sequence

### Phase 1 (Current - MVP)
**Goal**: Complete topology map of 2000 mechanisms

**Deliverables**:
1. All nodes identified and catalogued
2. All mechanisms mapped (A → B relationships)
3. All directions specified (+/−)
4. Spatial variation flags for mechanisms with geographic heterogeneity
5. Qualitative evidence references

**Timeline**: 6-12 months

**Technology**: LLM topology discovery, qualitative validation

---

### Phase 2 (Future - Quantification)
**Goal**: Add effect sizes to all 2000 mechanisms

**Deliverables**:
1. Effect sizes extracted from 200-300 papers per mechanism
2. Meta-analytic pooling for all mechanisms
3. Bayesian posteriors with credible intervals
4. Quantified moderators for key contexts
5. Monte Carlo uncertainty propagation
6. Full probabilistic forecasting capability

**Timeline**: 12-24 months after Phase 1 completion

**Technology**: LLM effect extraction, automated meta-analysis, Bayesian MCMC

---

## Why Separate Phases?

### Scientific Reasons
1. **Topology First**: Must know what connects before quantifying connections
2. **Validation**: Easier to validate 2000 relationships qualitatively than quantitatively
3. **Prioritization**: Some mechanisms matter for topology but not magnitude
4. **Iterative Refinement**: Topology errors compound in quantification

### Technical Reasons
1. **Computational Load**: Meta-analyzing 300 papers × 2000 mechanisms = 600,000 papers
2. **LLM Costs**: Effect extraction is 10× more expensive than topology discovery
3. **Data Availability**: Not all mechanisms have sufficient quantitative studies
4. **Quality Control**: Easier to validate in stages

### Practical Reasons
1. **Stakeholder Value**: Topology map is immediately useful (e.g., "what pathways exist?")
2. **Grant Milestones**: Fundable deliverable at Phase 1 completion
3. **Publication**: Topology map is publishable before quantification
4. **Team Scaling**: Can add econometricians/statisticians for Phase 2

---

## Migration Path from Phase 1 to Phase 2

### Data Structure Compatibility
Phase 1 mechanism records will have placeholders for Phase 2 fields:

```yaml
# Phase 1 Record
id: housing_quality_respiratory
direction: positive
spatial_variation_noted: true
supporting_studies:
  - "Krieger et al. (2002)"
  - "Jacobs et al. (2009)"

# Phase 2 Enhancement (same record, added fields)
id: housing_quality_respiratory
direction: positive
spatial_variation_noted: true
supporting_studies:
  - "Krieger et al. (2002)"
  - "Jacobs et al. (2009)"
effect_size:                    # ADDED IN PHASE 2
  measure: odds_ratio
  point_estimate: 1.34
  confidence_interval: [1.18, 1.52]
moderators:                     # ADDED IN PHASE 2
  - name: climate_humidity
    multiplier: 1.15
  - name: building_age
    multiplier: 1.10
```

No Phase 1 data is discarded—only enhanced.

---

## Current Status

**Phase 1 (MVP)**: IN PROGRESS
- Documentation updated to reflect topology-only scope
- LLM topology discovery pipeline specified
- Node bank structure defined
- Target: 2000 mechanisms by [DATE]

**Phase 2 (Quantification)**: SPECIFIED BUT NOT IMPLEMENTED
- Complete specifications in this directory
- Ready for implementation after Phase 1 completion
- Estimated start: [DATE]

---

## Questions About This Approach?

### "Why not do both phases simultaneously?"
**Answer**: Topology errors would propagate into effect size estimates. Better to validate structure first.

### "Can we do Phase 2 for a subset of mechanisms?"
**Answer**: Yes. High-priority mechanisms (e.g., top 100) could be quantified early for pilot testing.

### "What if a mechanism has direction but no quantifiable effect?"
**Answer**: Phase 1 includes it (useful for topology). Phase 2 flags it as "qualitative only" or uses proxy/simulation.

### "Will Phase 2 change any Phase 1 topologies?"
**Answer**: Possibly. If quantification reveals no effect (d ≈ 0), mechanism might be reclassified. This is expected refinement.

---

## Contact

Questions about Phase 2 scope or timeline? Contact [PROJECT_LEAD]
