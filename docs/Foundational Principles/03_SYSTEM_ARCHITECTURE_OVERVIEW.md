# System Architecture Overview
## High-Level Technical Design and Component Relationships

**Document ID**: 03_SYSTEM_ARCHITECTURE_OVERVIEW.md  
**Version**: 2.0  
**Last Updated**: November 15, 2025  
**Tier**: 1 - Foundational Principles

---

## Table of Contents

1. [Architecture Philosophy](#architecture-philosophy)
2. [System Components](#system-components)
3. [Data Flow Architecture](#data-flow-architecture)
4. [Component Relationships](#component-relationships)
5. [MVP vs. Phase 2 Scope](#mvp-vs-phase-2-scope)
6. [Technical Stack Overview](#technical-stack-overview)
7. [Scalability and Performance](#scalability-and-performance)

---

## Architecture Philosophy

### Design Principles

**1. Separation of Concerns**
- Mechanism discovery (LLM-driven) separate from calculation engine (SD-based)
- Data layer separate from computation layer separate from presentation layer
- Changes to one component don't break others

**2. Reusability and Modularity**
- Mechanism bank reusable across all geographies
- Geographic contexts plug into same mechanism bank
- Intervention scenarios use same calculation engine

**3. Transparency and Auditability**
- Every calculation traceable to source
- Git version control for all mechanisms
- Lineage tracking from literature → LLM → expert review → deployment

**4. Scalability First**
- Architecture supports 50+ geographies, 2000+ mechanisms
- Caching and parallelization built-in
- Cloud-native deployment for elastic scaling

**5. API-First Design**
- Core functions accessible via API
- Third-party integration possible
- User interface consumes same APIs as external users

---

## System Components

### Component Overview

```
┌────────────────────────────────────────────────────────────────┐
│                    SYSTEM ARCHITECTURE                          │
└────────────────────────────────────────────────────────────────┘

TIER 1: DATA LAYER
├─ [Mechanism Bank] Git repository, ~2000 mechanisms, versioned
├─ [Node Bank] 400 nodes with specs, units, functional forms
├─ [Geographic Contexts] Policy data, demographics, calibrations per geography
├─ [Literature Corpus] PDFs, abstracts, metadata for 300+ papers per mechanism
└─ [User Scenarios] Saved interventions, results, sensitivity analyses

TIER 2: DISCOVERY & SYNTHESIS LAYER
├─ [LLM Topology Discovery] Find connections between nodes via literature
├─ [LLM Effect Quantification] Extract effect sizes, meta-analyze, synthesize
├─ [Bayesian Inference Engine] MCMC sampling, posterior inference, uncertainty
├─ [Validation Pipeline] Automated checks, expert review, quality gates
└─ [Version Control] Git workflow for mechanism updates

TIER 3: COMPUTATION LAYER
├─ [Equilibrium Solver] Calculate pre-intervention baseline (inverse calibration)
├─ [Time Simulator] Post-intervention dynamics, annual steps, convergence
├─ [Cascade Calculator] Propagate changes through network, handle feedback
├─ [Uncertainty Propagator] Monte Carlo with posterior samples
└─ [Outcome Projector] Monetize crisis endpoints, stratify by population

TIER 4: CONTEXTUALIZATION LAYER
├─ [Moderator Engine] Apply policy/demographic/implementation adjustments
├─ [Geographic Pruner] Select relevant subset of nodes/mechanisms for geography
├─ [Initial State Calibrator] Set baseline stocks from data + inverse calculation
└─ [Policy Detector] Auto-detect Medicaid rules, housing policy, etc.

TIER 5: PRESENTATION LAYER
├─ [Web Interface] Interactive system map, scenario builder, dashboards
├─ [API Gateway] RESTful endpoints for programmatic access
├─ [Visualization Engine] Network graphs, outcome charts, sensitivity plots
└─ [Report Generator] PDF exports, plain-language summaries

TIER 6: INFRASTRUCTURE LAYER
├─ [Cloud Deployment] Scalable compute, storage, networking
├─ [Cache Layer] Mechanism lookups, common scenarios
├─ [Monitoring] Performance, errors, usage analytics
└─ [Security] Authentication, authorization, data protection
```

### Component Details

#### **Mechanism Bank (Data Layer)**

**Purpose**: Central repository of all causal pathways

**Structure**:
```
mechanisms/
├─ housing_to_health/
│   ├─ eviction_healthcare_discontinuity.yaml
│   ├─ housing_quality_respiratory.yaml
│   └─ rent_burden_economic_precarity.yaml
├─ healthcare_to_outcomes/
│   ├─ continuity_ed_utilization.yaml
│   └─ access_hospitalization.yaml
└─ [organized by domain]

Each mechanism file:
  mechanism_id: unique identifier
  from_node: upstream stock
  to_node: downstream stock
  functional_form: sigmoid|linear|threshold|log|multiplicative
  base_effect_size: pooled estimate
  confidence_interval: [lower, upper]
  moderators:
    - type: policy|demographic|implementation
      factor: specific moderator
      adjustment: effect modification
  source_studies: [DOI list]
  expert_reviews: [reviewer, date, approval]
  version: 1.0
  git_commit: commit hash
```

**Technology**: Git repository (GitHub), YAML files for human readability, parsed into PostgreSQL for querying

#### **Node Bank (Data Layer)**

**Purpose**: Defines all stocks in system with specifications

**Structure**:
```
nodes/
├─ structural/
│   ├─ chw_capacity.yaml
│   ├─ housing_quality.yaml
│   └─ policy_strength.yaml
├─ intermediate/
│   ├─ healthcare_continuity.yaml
│   ├─ economic_precarity.yaml
│   └─ community_trust.yaml
└─ crisis_endpoints/
    ├─ ed_visits.yaml
    ├─ hospitalizations.yaml
    └─ deaths.yaml

Each node file:
  node_id: unique identifier
  node_type: structural|intermediate|crisis_endpoint
  stock_unit: FTE|index_0_1|annual_count|etc
  measurement_method: direct|proxy_index|calibrated
  proxy_construction: [if proxy, formula for index]
  typical_range: [min, max] for validation
  data_sources: [census, admin data, surveys]
```

**Technology**: Git repository, YAML files, indexed in PostgreSQL

#### **Geographic Contexts (Data Layer)**

**Purpose**: Store location-specific data for contextualization

**Structure**:
```
geographies/
├─ boston_ma/
│   ├─ policy_environment.yaml
│   ├─ demographics.yaml
│   ├─ baseline_health_outcomes.yaml
│   └─ calibrated_stocks.yaml
├─ rural_mississippi/
└─ [per geography]

Policy environment:
  medicaid_expansion: true
  medicaid_work_requirements: false
  just_cause_eviction_score: 8
  rent_control: false
  healthcare_integration_index: 0.7
  
Demographics:
  population: 680000
  race_ethnicity:
    white: 0.44
    black: 0.24
    latinx: 0.19
  poverty_rate: 0.28
  
Baseline outcomes:
  ed_visits_annual: 122400
  hospitalizations_annual: 18500
  deaths_annual: 850
```

**Technology**: YAML files per geography, PostgreSQL for querying, updated via web scraping + user input

#### **LLM Discovery Pipeline (Discovery Layer)**

**Purpose**: Automated mechanism generation from literature

**Components**:
1. **Topology Discovery**: Query "Does Node A affect Node B?" → search literature → confidence score
2. **Effect Quantification**: Extract effect sizes from papers, standardize metrics
3. **Meta-Analysis**: Pool across studies, calculate heterogeneity, detect bias
4. **Validation**: Automated checks + expert review

**Technology**: 
- Python orchestration
- Claude API for LLM calls
- PubMed/Semantic Scholar APIs for literature
- R + Stan for Bayesian meta-analysis
- Git for version control

**Inputs**: Node pairs to test, literature corpus
**Outputs**: Validated mechanisms added to bank

#### **Equilibrium Solver (Computation Layer)**

**Purpose**: Calculate baseline state and post-intervention equilibrium

**Method**:
1. **Linearized Approximation**: Express system as matrix equation A×S=B
2. **Solve**: S = A⁻¹×B (linear algebra)
3. **Refine**: Iterative relaxation with nonlinear functions
4. **Validate**: Check that crisis endpoints match observed data

**Technology**:
- Python (NumPy for linear algebra, SciPy for optimization)
- Convergence criteria: max(|ΔS|) < 0.01

**Inputs**: Node bank, mechanism bank, observed crisis endpoints
**Outputs**: Calculated stock levels for all intermediate nodes

#### **Time Simulator (Computation Layer)**

**Purpose**: Project system forward after intervention

**Method**:
1. User specifies intervention (stock capacity change)
2. Apply ramp-up function (Year 1: 60%, Year 2: 90%, Year 3: 100%)
3. For each time step:
   - Calculate all mechanism flows based on current stocks
   - Update stocks based on net flows
   - Check convergence (max stock change < 1%)
4. Continue until convergence OR time horizon reached

**Technology**:
- Python simulation engine
- Annual time steps (configurable)
- Feedback loop handling via bounded functional forms

**Inputs**: Equilibrium baseline, intervention specification
**Outputs**: Stock trajectories over time, final equilibrium

#### **Web Interface (Presentation Layer)**

**Purpose**: User interaction, visualization, scenario building

**Features**:
1. **Interactive System Map**: D3.js network visualization, clickable nodes/mechanisms
2. **Scenario Builder**: Form-based intervention specification
3. **Dashboard**: Outcome projections, equity breakdowns, sensitivity charts
4. **Audit Trail**: Click-through to source studies, mechanism details
5. **Export**: PDF reports, CSV data, shareable links

**Technology**:
- React frontend
- D3.js for network visualization
- Recharts for outcome plots
- RESTful API calls to backend

---

## Data Flow Architecture

### User Scenario Workflow

```
USER ACTION: "Model CHW scale-up in Boston"

STEP 1: LOAD CONTEXT
├─ User selects: "Boston, MA"
├─ System retrieves: Geographic context (policy, demographics, baseline outcomes)
├─ System loads: Relevant nodes (~100 of 400 total)
└─ System loads: Relevant mechanisms (~500 of 2000 total)

STEP 2: CALCULATE BASELINE
├─ Fix: Crisis endpoints at observed values (ED = 122,400/year)
├─ Fix: Structural stocks at measured values (CHW = 50 FTE)
├─ Solve: Intermediate stocks via equilibrium calculation
└─ Validate: Does equilibrium reproduce observed crisis endpoints? (Yes → proceed)

STEP 3: USER SPECIFIES INTERVENTION
├─ User inputs: "CHW capacity 50 → 200 FTE"
├─ User inputs: "Cost: $6M over 3 years"
├─ User inputs: "Time horizon: 3 years"
└─ User inputs: "Ramp-up: Linear over 3 years"

STEP 4: APPLY MODERATORS
├─ System retrieves: Boston moderators (integration, Medicaid, demographics)
├─ System adjusts: Base effect 0.35 → Boston effect 0.60 (with moderators)
└─ System documents: Which moderators applied, how much adjustment

STEP 5: RUN SIMULATION
├─ Time step 1 (Year 1):
│   ├─ CHW: 50 → 100 FTE (50% of full increase)
│   ├─ Calculate flows: CHW → Continuity → ED
│   ├─ Update stocks: Continuity +0.08, ED -0.03
│   └─ Materializ

ed effect: 60% (ramp-up factor)
├─ Time step 2 (Year 2):
│   └─ [similar, 90% effect]
├─ Time step 3 (Year 3):
│   └─ [similar, 100% effect]
└─ Check convergence: System stable? (Yes → final equilibrium)

STEP 6: PROJECT OUTCOMES
├─ Calculate: ΔED_Visits = -4,200/year (at new equilibrium)
├─ Monetize: -4,200 × $1,200 = -$5.04M health value
├─ Stratify: 68% benefit to Black residents (population moderator)
└─ Quantify uncertainty: Monte Carlo with 1000 posterior samples → 95% CrI [-6,800, -1,800]

STEP 7: PRESENT TO USER
├─ Dashboard: Primary outcomes, cost-effectiveness, ROI
├─ Equity: Distribution by race/SES/insurance
├─ Sensitivity: Vary assumptions ±20%, show robustness
├─ Audit: Link to mechanism chains, source studies
└─ Export: PDF report, CSV data
```

### Mechanism Update Workflow

```
TRIGGER: New RCT published on CHW effectiveness

STEP 1: LITERATURE MONITORING
├─ PubMed API: Scheduled search for new papers on CHW
├─ LLM screening: Does this paper report CHW → health outcome?
└─ Flag: Paper relevant to mechanism "chw_healthcare_continuity"

STEP 2: EFFECT EXTRACTION
├─ LLM: Extract effect size from paper (RR, OR, β, d, etc.)
├─ Standardize: Convert to common metric (Cohen's d)
├─ Parse: Sample size, study design, population, CI
└─ Store: In extraction database with metadata

STEP 3: META-ANALYSIS UPDATE
├─ Retrieve: All existing studies for this mechanism (12 current)
├─ Add: New study (now 13 studies total)
├─ Re-run: Bayesian meta-analysis with updated data
├─ Compare: Old pooled effect (0.35) vs. new (0.36) → minimal change
└─ Update: Credible interval slightly narrower [0.22, 0.50] → [0.24, 0.48]

STEP 4: VALIDATION
├─ Automated checks: Effect size plausible? CI valid? Study quality adequate?
├─ Expert spot-check: Sample 10% of new mechanisms for manual review
└─ Approval: Domain expert signs off (or requests revision)

STEP 5: VERSION CONTROL
├─ Git commit: Update mechanism file with new effect size
├─ Tag: Version 1.1 (minor update, backward compatible)
├─ Document: Changelog explaining what changed and why
└─ Deploy: Push to production mechanism bank

STEP 6: NOTIFICATION
├─ Notify users: "Mechanism X updated based on new evidence"
├─ Re-run option: "Recalculate your saved scenarios with updated mechanism"
└─ Report: Show old vs. new projections (transparency)
```

---

## Component Relationships

### Component Dependency Graph

```
┌─────────────────────────────────────────────────────────────┐
│                   COMPONENT DEPENDENCIES                     │
└─────────────────────────────────────────────────────────────┘

                    [Literature Corpus]
                           ↓
                  [LLM Discovery Pipeline]
                           ↓
┌────────────────────────────────────────────────────┐
│              [Mechanism Bank]                       │
│                    ↑                                │
│         (version control, updates)                  │
│                    ↓                                │
│       [Validation & Expert Review]                  │
└────────────────────────────────────────────────────┘
                           ↓
              ┌────────────┴────────────┐
              ↓                         ↓
      [Node Bank]              [Geographic Contexts]
              ↓                         ↓
              └────────────┬────────────┘
                           ↓
                 [Equilibrium Solver]
                           ↓
               ┌───────────┴───────────┐
               ↓                       ↓
       [Time Simulator]      [Uncertainty Propagator]
               ↓                       ↓
               └───────────┬───────────┘
                           ↓
                 [Outcome Projector]
                           ↓
                   [Web Interface]
                           ↓
                        [User]
```

### Critical Interfaces

**Interface 1: Mechanism Bank ↔ Computation Engine**
```
Query: "Get mechanism from CHW to Healthcare_Continuity for Boston"

Mechanism Bank returns:
{
  mechanism_id: "chw_healthcare_continuity",
  functional_form: "sigmoid",
  base_effect: 0.35,
  moderators: [
    {type: "integration", value: +0.12},
    {type: "medicaid", value: +0.08}
  ],
  confidence_interval: [0.22, 0.50]
}

Computation Engine uses:
- functional_form to calculate ΔContinuity = sigmoid(ΔCHW, 0.35)
- moderators to adjust: 0.35 + 0.12 + 0.08 = 0.55 (Boston-specific)
- confidence_interval for uncertainty propagation
```

**Interface 2: Geographic Context ↔ Moderator Engine**
```
Query: "Get moderators for Boston"

Geographic Context returns:
{
  policy_environment: {
    medicaid_expansion: true,
    medicaid_work_requirements: false,
    healthcare_integration: 0.7
  },
  demographics: {
    black_proportion: 0.24,
    poverty_rate: 0.28
  }
}

Moderator Engine applies:
- medicaid_work_requirements: false → +0.08 to CHW effect
- healthcare_integration: 0.7 → +0.12 to CHW effect
- black_proportion: 0.24 → +0.09 to eviction effect (disparity driver)
```

**Interface 3: Time Simulator ↔ Web Interface**
```
Web Interface sends:
{
  geography: "boston_ma",
  intervention: {
    node: "chw_capacity",
    from_value: 50,
    to_value: 200,
    ramp_years: 3
  },
  time_horizon: 5,
  uncertainty_samples: 1000
}

Time Simulator returns:
{
  trajectory: [
    {year: 0, ed_visits: 122400},
    {year: 1, ed_visits: 120600},
    {year: 2, ed_visits: 119100},
    {year: 3, ed_visits: 118200},
    {year: 4, ed_visits: 118200}, // converged
    {year: 5, ed_visits: 118200}
  ],
  uncertainty: {
    year_3_ed_visits: {
      median: 118200,
      ci_95_lower: 115600,
      ci_95_upper: 121000
    }
  },
  equity: {
    black_benefit_proportion: 0.68
  }
}

Web Interface renders:
- Line chart showing ED_Visits over time with CI bands
- Bar chart showing equity distribution
- Table with cost-effectiveness metrics
```

---

## MVP vs. Phase 2 Scope

### MVP Scope

**Data Layer**:
- ✓ Mechanism bank: Target 2000 mechanisms (literature-derived, LLM-generated)
- ✓ Node bank: 400 nodes defined with specifications
- ✓ Geographic contexts: 1 demonstration geography (Boston)
- ✓ Literature corpus: 300+ papers per mechanism domain

**Discovery Layer**:
- ✓ LLM topology discovery functional
- ✓ LLM effect quantification operational
- ✓ Bayesian meta-analysis implemented
- ✓ Validation pipeline automated
- ✗ Community contribution workflow (deferred to Phase 2)

**Computation Layer**:
- ✓ Equilibrium solver operational
- ✓ Time simulator functional
- ✓ Uncertainty propagation via Monte Carlo
- ✗ Real-time policy detection (manual input in MVP)

**Contextualization Layer**:
- ✓ Moderator engine operational
- ✓ Geographic pruning implemented
- ✓ Initial state calibration functional
- ✗ Automatic policy scraping (manual input in MVP)

**Presentation Layer**:
- ✓ Web interface with system map
- ✓ Scenario builder
- ✓ Dashboard with outcomes, equity, sensitivity
- ✓ PDF export
- ✗ Mobile app (deferred to Phase 2)

**Infrastructure**:
- ✓ Cloud deployment (AWS or similar)
- ✓ Basic caching
- ✓ Authentication and authorization
- ✗ Multi-tenancy (single-organization in MVP)

### Phase 2 Additions

**Expansion Capabilities**:
- ✓ Multi-geography: 10+ cities operational
- ✓ Real-time policy detection: Automatic scraping of Medicaid rules, housing policy
- ✓ Actor network layer: Organizational mapping onto mechanisms

**Enhanced Analytics**:
- ✓ Intersectional equity analysis: Race × SES × geography stratification
- ✓ Multi-intervention optimization: Find best portfolio of 5 interventions
- ✓ Empirical calibration: Use local outcome data to refine mechanism effects

**Community Features**:
- ✓ External researcher contributions: Submit mechanisms via GitHub PR
- ✓ Open API: Third-party integration for research platforms
- ✓ Academic partnership: Joint publications, validation studies

**Advanced Interface**:
- ✓ Mobile app for field use
- ✓ Custom node/mechanism editor for consultants
- ✓ Real-time collaboration (multiple users in same scenario)

---

## Technical Stack Overview

### Technology Choices

**Backend**:
```
Python 3.11+
├─ Core logic: NumPy, SciPy (linear algebra, optimization)
├─ Network operations: NetworkX (graph algorithms)
├─ API framework: FastAPI (async, modern)
└─ Task queue: Celery (background jobs like MCMC)

R 4.3+
├─ Bayesian modeling: cmdstanr (Stan interface)
├─ Meta-analysis: metafor, bayesmeta
└─ Statistical validation: Custom scripts

Stan 2.32+
├─ MCMC sampling: Hamiltonian Monte Carlo
└─ Posterior inference: Hierarchical models
```

**Frontend**:
```
React 18+
├─ UI framework: Material-UI or Tailwind
├─ Visualization: D3.js (network), Recharts (plots)
├─ State management: Redux or Zustand
└─ API client: Axios

TypeScript
└─ Type safety for complex data structures
```

**Data Storage**:
```
PostgreSQL 15+
├─ Mechanism bank (indexed, queryable)
├─ Geographic contexts
├─ User scenarios and results
└─ Literature metadata

Git (GitHub)
├─ Mechanism YAML files (version control)
├─ Node specifications
├─ Documentation
└─ Code

S3 (or equivalent)
├─ Literature PDFs
├─ Large datasets (Census, health outcomes)
└─ Exported reports
```

**LLM Integration**:
```
Anthropic Claude API
├─ Topology discovery prompts
├─ Effect size extraction
├─ Literature synthesis
└─ Expert opinion aggregation
```

**Infrastructure**:
```
Cloud Platform: AWS (or Azure, GCP)
├─ Compute: EC2 or Fargate (containers)
├─ Storage: S3, RDS (PostgreSQL)
├─ Caching: Redis or ElastiCache
└─ CDN: CloudFront (static assets)

Orchestration:
├─ Docker: Containerization
├─ Kubernetes: Optional (if multi-tenancy)
└─ Terraform: Infrastructure as code
```

### Architecture Patterns

**Microservices** (loosely coupled):
```
├─ Mechanism Service: CRUD operations on mechanism bank
├─ Computation Service: Equilibrium solver, time simulator
├─ LLM Service: Discovery pipeline, effect quantification
├─ Geography Service: Context management, policy detection
└─ User Service: Authentication, scenarios, results
```

**Event-Driven** (for async workflows):
```
Event: New mechanism added
├─ Trigger: Validation pipeline
├─ Trigger: Re-index search
└─ Trigger: Notify subscribers

Event: User runs scenario
├─ Trigger: Computation service
├─ Trigger: Log to analytics
└─ Trigger: Cache result
```

**API-First** (internal and external use same APIs):
```
RESTful Endpoints:
├─ GET /mechanisms?from_node=X&to_node=Y
├─ POST /scenarios (create new scenario)
├─ GET /scenarios/{id}/results
├─ POST /equilibrium/solve (run calculation)
└─ GET /geographies/{id}/context
```

---

## Scalability and Performance

### Performance Targets

**User-Facing Operations**:
- Scenario execution: <30 seconds (single simulation)
- Sensitivity analysis: <5 minutes (1000 Monte Carlo runs)
- System map rendering: <2 seconds (100 nodes, 500 mechanisms)
- Dashboard load: <3 seconds (charts, tables)

**Background Operations**:
- Mechanism update: <1 hour (re-run meta-analysis)
- Geographic setup: <15 minutes (load context, calibrate baseline)
- LLM discovery: <2 hours (per mechanism domain, 50 mechanisms)

### Optimization Strategies

**1. Mechanism Caching**
```
Cache frequently accessed mechanisms
├─ Key: (from_node, to_node, geography)
├─ Value: Adjusted effect size with moderators
├─ TTL: 24 hours (or until mechanism updated)
└─ Backend: Redis

Reduces: Database queries by 80%
```

**2. Sparse Network Representation**
```
Most mechanisms inactive in any scenario (thresholds not met)
├─ Store: Adjacency list (not full matrix)
├─ Compute: Only active pathways
└─ Skip: Zero-flow mechanisms

Reduces: Computation by 60%
```

**3. Parallelization**
```
Monte Carlo runs are independent
├─ Split: 1000 runs across 8 CPU cores
├─ Aggregate: Combine results
└─ Speedup: ~7.5× (near-linear scaling)

Reduces: Sensitivity analysis time from 40min to 5min
```

**4. Linearization for Small Perturbations**
```
For sensitivity (±20% effect size variation):
├─ Use: Linear approximation (Jacobian matrix)
├─ Instead of: Full nonlinear simulation
└─ Accuracy: Within 5% of full simulation

Reduces: Sensitivity computation by 95%
```

**5. Geographic Pruning**
```
Don't load all 2000 mechanisms for every geography
├─ Select: Mechanisms relevant to local conditions
├─ Criteria: Node stocks above threshold, policy context match
├─ Result: ~500 active mechanisms per geography (25% of total)
└─ Reduces: Load time and memory

Reduces: System initialization by 70%
```

### Scalability Architecture

**Horizontal Scaling** (add more servers as demand grows):
```
Load Balancer
├─ Web Server 1 (React frontend)
├─ Web Server 2
└─ Web Server N

API Gateway
├─ Computation Service 1
├─ Computation Service 2
└─ Computation Service N

Database
├─ PostgreSQL Primary (writes)
└─ PostgreSQL Replicas (reads)
```

**Vertical Scaling** (for computation-heavy tasks):
```
MCMC Sampling:
├─ Requires: High-memory instance (64GB+)
├─ Duration: 30-60 minutes per mechanism
└─ Scheduled: Off-peak hours (batch processing)

Equilibrium Solving:
├─ Requires: Multi-core CPU (16+ cores)
├─ Duration: 1-5 minutes per geography
└─ On-demand: User-triggered
```

---

## Document Metadata

**Version History**:
- v1.0 (2024-06): Initial architecture document
- v2.0 (2025-11): Expanded component details, clarified MVP scope, added scalability section

**Related Documents**:
- [04_STOCK_FLOW_PARADIGM.md] - Detailed node/mechanism specifications
- [06_EQUILIBRIUM_CALCULATION_ENGINE.md] - Computation engine implementation
- [14_COMPUTATIONAL_INFRASTRUCTURE.md] - Infrastructure deployment details
- [18_REFERENCE_IMPLEMENTATION_MVP.md] - Concrete MVP implementation guide

**Last Reviewed**: November 15, 2025  
**Next Review**: May 15, 2026

---

**END OF DOCUMENT**
