# Project Foundations
## Systems-Based Health Impact Modeling Platform

**Document ID**: 01_PROJECT_FOUNDATIONS.md  
**Version**: 2.0  
**Last Updated**: November 15, 2025  
**Tier**: 1 - Foundational Principles

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [The Core Problem](#the-core-problem)
3. [The Solution Architecture](#the-solution-architecture)
4. [Five Key Innovations](#five-key-innovations)
5. [Structural Competency Framework](#structural-competency-framework)
6. [System Scope and Boundaries](#system-scope-and-boundaries)
7. [Target Users and Use Cases](#target-users-and-use-cases)
8. [Competitive Differentiation](#competitive-differentiation)

---

## Executive Summary

### What This Platform Does

The Systems-Based Health Impact Modeling Platform quantifies how structural interventions—housing policy, Medicaid design, workforce development, environmental remediation—cascade through interconnected social, spatial, and biological systems to affect health outcomes.

**Core Capability**: Accept any geography and demographic specification, automatically configure a system map from a bank of ~2000 empirically-grounded mechanisms, and project health impact of proposed interventions with full transparency and equity stratification.

### Why It Matters

State policymakers allocate billions annually on structural interventions yet cannot quantify their health effects. Health departments justify programs with "best practice" rather than evidence-based ROI. Foundations fund 50 programs across 5 states without standardized comparison. Community organizations document excellent work but cannot demonstrate health impact in terms funders understand.

**The Gap**: No integrated framework exists to model how structural changes propagate through systems to produce health outcomes, identify high-leverage intervention points, or compare effectiveness across diverse geographies while maintaining equity focus.

### Value Proposition

**For Health Departments**: Justify specific budget investments with projected outcomes. Identify which interventions generate highest health impact per dollar. Coordinate across silos (housing, health, employment).

**For Foundations**: Compare portfolio impact across geographies and intervention types. Identify redundancies and synergies. Allocate funds toward highest structural leverage points.

**For Community Organizations**: Demonstrate health impact of advocacy, organizing, and service work. Access credible quantification for funding justification.

**For Policymakers**: Model health consequences of policy decisions before implementation. Identify unintended effects. Prioritize interventions addressing root causes.

---

## The Core Problem

### Market Reality

$50B+ annual spending across state health, housing, labor, and education budgets with no integrated framework to:
- Quantify downstream health effects of structural policies
- Compare interventions across domains and geographies
- Identify leverage points where limited resources create disproportionate impact
- Project equity distributions (who benefits, who bears costs)
- Account for policy context reshaping intervention effectiveness

### Specific Pain Points

#### Health Departments
**Problem**: Cannot justify specific investments to legislatures beyond "this is best practice."

**Example**: A state health department funds community health workers at $40M annually. When asked "what health outcomes does this produce?" they respond with qualitative stories, not quantified projections stratified by population.

**Consequence**: Budget cuts target programs without evidence defense. Interventions addressing root causes defunded in favor of crisis response (which has visible immediate metrics).

#### Foundations
**Problem**: Allocate billions across interventions, geographies, program types without standardized impact comparison.

**Example**: A foundation funds housing stability programs in 5 states. Program A (legal defense) costs $500k, serves 200 families. Program B (rental assistance) costs $2M, serves 400 families. Which produces more health impact? In which geography? For which populations? No framework exists to answer.

**Consequence**: Portfolio strategy driven by anecdote and relationships rather than evidence. Cannot learn why identical programs produce different outcomes across states.

#### Community Organizations
**Problem**: Do structural work (housing advocacy, mutual aid, workforce development) but cannot quantify health impact in terms policymakers/funders understand.

**Example**: A community land trust preserves affordable housing for 500 families. They document tenant satisfaction, housing quality, neighborhood stability. But when city council asks "what's the health ROI?" they cannot answer in standardized metrics.

**Consequence**: Epistemically marginalized. Funding flows to medicalized interventions with clear

 outcome metrics, not structural interventions with complex causal chains.

#### Academic Researchers
**Problem**: Publish causal evidence about specific mechanisms (eviction → health discontinuity) but lack infrastructure to integrate findings into operational decision-support.

**Example**: 15 studies document that eviction increases ED visits. But no system exists to translate this into: "If City X passes just-cause eviction protection, projected ED visit reduction is Y (95% CI: [L, U]), concentrated in neighborhoods A, B, C, among populations D, E, F."

**Consequence**: Evidence remains siloed in journals. Policymakers make decisions without synthesized causal knowledge.

### Why Existing Tools Fall Short

| Tool Category | What It Does | Why Insufficient |
|--------------|-------------|------------------|
| **Health Impact Assessment (HIA)** | Qualitative evaluation of policy health effects | Non-quantified; project-specific; manual process (6-12 months per assessment); does not scale |
| **SROI Platforms** (Social Return on Investment) | Calculate monetized social return ratios | Forces arbitrary monetization into single ratio; ignores actor networks; misses spillovers/externalities; hides equity distributions |
| **BI Dashboards** (Tableau, Power BI) | Visualize existing data | Descriptive only; no causal inference; siloed data sources; cannot model interventions; no system visualization |
| **Health Data Warehouses** (CDC WONDER, state surveillance systems) | Query historical health outcomes | Surveillance tools; no forward modeling; no policy simulation; no intervention comparison |
| **Consulting Firms** (Bailit Health, Mathematica, RAND) | Custom policy analysis | $300k-$1M per engagement; opaque methodology; 6-18 month timeline; not scalable; findings don't generalize |
| **Academic System Dynamics Models** | Rigorously model causal systems with feedback loops | PhD expertise required; built from scratch per context; no reusable mechanism bank; no actor layer; inaccessible to practitioners |

**The Synthesis Gap**: No tool combines systems thinking (feedback loops, leverage points) + epidemiological rigor (effect sizes, confidence intervals) + equity centering (stratified outcomes) + scalability (reusable mechanisms) + transparency (auditable assumptions).

---

## The Solution Architecture

### Three-Layer Innovation

#### **Layer 1: System Map (Causal Network)**

**What**: Network of ~400 nodes representing structural conditions, intermediate states, and health outcomes, connected by ~2000 empirically-grounded mechanisms.

**How It Works**:
- Nodes = stocks (measurable quantities): "Housing Quality" (index 0-1), "Eviction Risk" (annual rate), "ED Utilization" (visits/year)
- Edges = mechanisms (causal relationships): "Eviction → Healthcare Discontinuity → ED Visits"
- Each mechanism has:
  - Functional form (sigmoid, linear, threshold, etc.)
  - Effect size from meta-analytic literature synthesis
  - Moderators (policy, demographic, implementation factors that strengthen/weaken effect)
  - Confidence intervals
  - Literature lineage (which studies support this pathway)

**Geographic Customization**:
- User specifies geography (Boston, rural Mississippi, etc.)
- System detects local policy context (Medicaid rules, housing protections, criminal justice approach)
- Adjusts mechanism effect sizes based on moderators
- Prunes network to ~100 most relevant nodes for that context
- Result: Boston system map ≠ Mississippi system map (different policy environments reshape causal pathways)

**User Interaction**:
- Interactive visualization showing structural determinants → intermediate mechanisms → health outcomes
- Click any node to see: what affects it, what it affects, supporting evidence
- Click any mechanism to see: effect size, confidence interval, moderating factors, source studies
- Select health outcome of interest; system highlights pathways that matter for that outcome

#### **Layer 2: Intervention Analysis**

**What**: User specifies intervention (scale CHWs from 50 to 200, pass just-cause eviction law, etc.), system calculates cascading effects.

**How It Works**:
1. **Baseline Equilibrium**: System solves for current state where stock flows balance
   - Crisis endpoints: Fixed at observed data (ED visits = 122,400/year)
   - Structural nodes: Measured directly (CHW count = 50)
   - Intermediate nodes: Calculated via inverse calibration to reproduce observed crisis endpoints

2. **Intervention Specification**: User changes a stock's capacity
   - Example: "Increase CHW capacity from 50 FTE to 200 FTE"
   - System doesn't calculate feasibility ($X budget → Y workers); user specifies capacity change and cost separately

3. **Cascade Calculation**: System propagates change through network
   - CHW stock increases → Healthcare Continuity stock increases (via mechanism with effect size 0.35)
   - Healthcare Continuity increases → ED Utilization decreases (via mechanism with effect size -0.20)
   - ED Utilization decreases → Projected ED visits reduced
   - Feedback loops accounted for (balancing and reinforcing)
   - System iterates to new equilibrium OR simulates forward to time horizon (whichever first)

4. **Outcome Projection**: Quantified at crisis endpoints only
   - Crisis endpoints: ED visits, hospitalizations, overdoses, arrests, deaths (have unit costs)
   - Intermediate outcomes: Tracked qualitatively (appointment adherence, housing stability, employment)
   - Equity stratification: Outcomes distributed by race/ethnicity, SES, insurance status based on literature-derived population moderators

5. **Uncertainty and Sensitivity**: Full transparency
   - 95% confidence intervals around effect sizes
   - Sensitivity analysis: vary effect sizes ±20%, show robustness
   - Monte Carlo simulation (1000 runs) for propagated uncertainty
   - Explicitly state when evidence is weak or correlational

**Output Format**:
- **Primary**: ED visits prevented, hospitalizations avoided, deaths averted (with CIs)
- **Monetization**: Crisis endpoints only (ED visit = $1,200, hospitalization = $8,500, etc.)
- **Cost-effectiveness**: Intervention cost vs. health value generated
- **Equity**: Which populations benefit most (stratified outcomes)
- **Sensitivities**: How results change if assumptions vary
- **Audit trail**: Click through to see mechanism chains, effect sizes, source studies

#### **Layer 3: Actor Network (Phase 2)**

**What**: Organizational infrastructure mapped onto causal mechanisms (which organizations intervene where, collaboration density, leverage via network position).

**How It Works** (Phase 2 Implementation):
- User clicks high-leverage node in system map
- System displays: which organizations currently intervene at this node, at what scale, with what coordination
- Identifies gaps: missing actors, coordination breakdowns
- Calculates ROI by actor: "Scaling Organization X from $Y to $Z capacity generates N health outcomes"
- Organizational leverage multiplier: does this actor create follow-on interventions through partnerships (amplification)?

**Value Add**:
- Moves from "what interventions work" to "who should deliver them and how should they coordinate"
- Surfaces collaboration opportunities
- Identifies organizational bottlenecks
- Enables network-building strategy alongside intervention strategy

---

## Five Key Innovations

### Innovation 1: LLM-Mediated Literature Synthesis

**Problem Solved**: Hand-curation of epidemiological mechanisms is slow (6-12 months per geography), expensive, and doesn't scale. Academic models are built from scratch per context.

**Our Approach**: Multi-stage LLM discovery pipeline
1. **Guided Topology Discovery**: LLM searches literature to identify which nodes connect (does eviction affect health? via what pathways?)
2. **Effect Quantification**: LLM extracts effect sizes from 300+ studies per mechanism, standardizes diverse metrics (RR, OR, β, d, HR → unified format)
3. **Meta-Analytic Pooling**: Statistical synthesis produces pooled effect size with confidence intervals and heterogeneity assessment
4. **Deduplication**: LLM clusters similar mechanisms ("eviction → healthcare disruption" = "housing instability → medication non-adherence"); merge to single pathway
5. **Expert Validation**: Domain experts review mechanisms for causal plausibility, structural competency, completeness

**Result**: 
- Mechanisms tied to literature (auditable, reproducible)
- Click any mechanism → see supporting studies, effect sizes, study populations, quality scores
- Rapid scaling: new geography operational in weeks, not months
- Version control: git-tracked lineage (which LLM version, which prompts, which studies, who approved)

**Why It Matters**: Transforms opaque SROI black boxes into transparent, scientifically defensible decision support.

### Innovation 2: Explicit Moderator Encoding

**Problem Solved**: Traditional tools assume effect sizes are universal ("CHW effect = 0.35 everywhere"). Reality: effects vary dramatically by context. Most tools hide this heterogeneity.

**Our Approach**: Every mechanism includes moderators—conditions that strengthen or weaken effects.

**Four Moderator Types**:

| Type | Example | Effect |
|------|---------|--------|
| **Policy** | Medicaid work requirements present vs. absent | CHW effect +0.10 when work requirements absent (healthcare access more stable) |
| **Demographic** | Black vs. White population | Eviction → health effect 1.8× stronger for Black populations (structural racism, discrimination) |
| **Geographic** | Urban vs. rural | CHW effect ×0.9 in rural (lower baseline healthcare density, transportation barriers) |
| **Implementation** | High vs. low program fidelity | CHW effect 2.1× when embedded in integrated healthcare system (vs. standalone program) |

**Encoding Format**:
```
Mechanism: CHW → Healthcare Continuity
Base effect: 0.35 (95% CI: 0.20-0.50)
Moderators:
  - Healthcare integration: +0.12 (integrated systems)
  - Medicaid work requirements: -0.08 (if present)
  - Population race (Black): +0.09 (disparity driver)
  - Rural geography: -0.05 (access barriers)
Adjusted effect: 0.35 + Σ(moderator adjustments)
```

**Result**: Effect sizes adapt to local context. Boston (integrated healthcare, no work requirements, diverse population) ≠ rural Mississippi (fragmented healthcare, work requirements, different demographics). Same intervention, different projected impact—system makes this explicit and quantified.

### Innovation 3: Equity Impact Detection

**Problem Solved**: Most systems identify disparities after analysis (descriptive). We identify them first to guide intervention selection (prescriptive).

**Our Approach**: When user specifies geography, system:
1. **Identifies Crisis Endpoints with Disparities**
   - Example: "Boston has 45 maternal deaths/year. Black women: 3.5× rate of White women."
2. **Decomposes Causes via Mechanism Bank**
   - Which mechanisms drive this disparity? 
     - Healthcare access (prenatal care gaps)
     - Provider discrimination (obstetric bias)
     - Chronic stress (weathering from structural racism)
     - Economic precarity (insurance instability, care avoidance)
3. **Ranks Interventions by Disparity Reduction Potential**
   - Show mechanisms that: (a) affect maternal mortality AND (b) have larger effects for Black women
   - Example: "Community doula programs: 2.8× effect for Black mothers (literature-derived population moderator)"
4. **Stratifies All Outcomes**
   - Every projection shows: total impact + distribution by race/ethnicity, SES, insurance status
   - Flags when interventions worsen equity (e.g., gentrification-inducing programs benefit wealthy, harm poor)

**Result**: Interventions focused on actual leverage points for equity, not generic "expand coverage" approaches that maintain disparities.

### Innovation 4: Version Control for Science

**Problem Solved**: Epidemiological assumptions are difficult to audit. Reproducibility is impossible. Changes over time are opaque.

**Our Approach**: Every mechanism has complete lineage:

```
mechanism_id: "eviction_healthcare_discontinuity_ed_visits"
discovery_date: "2024-05-20"
llm_version: "claude-3.5-sonnet-20241022"
discovery_prompt: [full prompt text stored]
source_studies: 
  - doi: 10.1111/2024-eviction-health
    effect: RR=1.34 (1.12-1.61)
    population: "Low-income adults, Boston"
  - [11 more studies]
pooled_effect: d=0.28 (0.23-0.33)
expert_reviewers:
  - "Dr. Sarah Chen (epidemiology)" - Approved 2024-06-15
  - "James Martinez (community organizer)" - Approved 2024-06-16
modifications:
  - v1.1: Added temporal dynamics (immediate vs. cumulative stress)
  - v1.2: Refined moderator for Medicaid context
git_commit: "8f3a2e1"
deployment_date: "2024-06-17"
```

**Result**:
- **Publishable Science**: Defend every number with traceable lineage
- **Reproducibility**: Run scenario in 2 years with same inputs → same outputs (unless mechanism bank updated)
- **Transparency**: Community can audit assumptions, challenge effect sizes, propose improvements
- **Accountability**: "This recommendation was based on mechanism v1.0, expert Dr. Smith, literature as of June 2024"
- **Improvement Tracking**: "In v2.0, we adjusted CHW effect from 0.35 to 0.30 because real-world outcomes showed..."

### Innovation 5: Contextual Adaptation Without Requiring Local Data

**Problem Solved**: Most systems require extensive local data collection (baseline surveys, health assessments, program evaluations). This takes months and costs $50k-$200k per geography, preventing scaling.

**Our Approach**: System uses available data in priority hierarchy:

**Priority 1: Local Empirical Data (if available)**
- Crisis endpoints: ED visits, hospitalizations (hospital administrative data)
- Structural capacity: CHW count, housing units (organizational records)
- Demographics: Census

**Priority 2: National Literature Benchmarks (default)**
- Mechanism effect sizes from meta-analytic synthesis
- Moderators from subgroup analyses in literature

**Priority 3: Policy Environment (scraped or user-input)**
- Medicaid rules (work requirements, expansion status)
- Housing policy (just-cause eviction, rent control)
- Criminal justice approach (reform vs. punitive)
- Detected automatically where possible, user-input where not

**Priority 4: Proxy Estimation (when direct measurement unavailable)**
- Intermediate nodes: Calculate via inverse calibration from observed crisis endpoints
- Example: "Healthcare Continuity" unmeasured → estimate what level would produce observed ED visits given other known stocks

**Process**:
1. User specifies: "Boston, low-income adults"
2. System retrieves: Census demographics, hospital data, policy context
3. System applies: Literature effect sizes + moderator adjustments for Boston context
4. System calibrates: Intermediate stocks to reproduce observed baseline
5. User can override: "Our local study shows effect is 0.25, not 0.35" → system accepts user input

**Result**: 
- New geographies operational in weeks (not months)
- No $50k baseline survey required
- Transparent about uncertainty (flags when evidence is weak, data is proxy)
- Improves over time as local data becomes available (Priority 1 replaces Priority 2-4)

---

## Structural Competency Framework

### Core Epistemology

**Structural competency** is the foundational epistemological stance shaping every mechanism in the platform.

**Core Assertions**:
1. Health disparities are products of legal, political, economic, and spatial systems—not individual behaviors
2. Individual behaviors matter but are fundamentally shaped by structures
3. Interventions must address root causes (housing policy, labor standards, healthcare design) not just symptoms (ED visits, chronic disease management)
4. Mechanisms operate at multiple scales simultaneously: federal policy → local markets → household conditions → biological stress
5. Equity requires understanding which systems benefit whom and at whose cost

### Implications for Design

#### Mechanism Development
**NOT**: "Stress causes disease" (individual-level, decontextualized)

**BUT**: "Discriminatory housing policies → eviction threat → economic precarity → chronic stress → disease" (structural, contextualized)

**Implementation**: Each mechanism in the bank explicitly traces from structural origins. Mechanisms that explain outcomes through individual deficits ("poor health literacy") are excluded unless embedded in structural analysis ("health literacy shaped by educational access shaped by school funding shaped by property tax structure").

#### Intervention Recommendations
**NOT**: "Educate people to manage stress better" (individual behavior change)

**BUT**: "Pass just-cause eviction protections + fund tenant legal defense + guarantee income" (structural change)

**Implementation**: System flags when proposed intervention treats symptoms without addressing causes. Example: "CHW program addresses healthcare access (symptom) but not insurance instability (cause). Consider: Medicaid expansion."

#### Leverage Point Identification
**NOT**: "Which interventions help most people?" (utilitarian, aggregate)

**BUT**: "Which interventions dismantle extractive systems AND prioritize most marginalized populations?" (structural justice, equity-centered)

**Implementation**: Recommendations prioritize leverage points that:
- Address root causes (not just symptoms)
- Reduce compulsory system contact (arrests, involuntary commitment, ED visits as last resort)
- Maximize decommodified resources (public housing, universal healthcare)
- Support community wealth circulation (local ownership, mutual aid)
- Minimize capital extraction (corporate rent-seeking, financialization)

#### Equity Analysis
**NOT**: "Here are health disparities" (descriptive, neutral)

**BUT**: "These disparities are evidence of which systems are working or failing for whom. Here's where structural change would reduce them." (diagnostic, prescriptive)

**Implementation**: Equity stratification is analytic core, not cosmetic add-on. Every mechanism includes population-specific moderators. Every outcome shows distribution by race/SES/geography. System identifies which interventions reduce disparities vs. maintain them.

### Three-Scale Framework

Mechanisms operate simultaneously at three scales:

#### **Scale 1: Structural (Federal/State Policy)**
- Medicaid design (expansion, work requirements, coverage scope)
- Housing policy (just-cause eviction, rent control, public housing funding)
- Criminal justice law (sentencing, policing, incarceration policy)
- Labor standards (minimum wage, worker protections, unionization rights)
- Healthcare system design (single-payer vs. private, integration level)

**Time Horizon**: 2-10 years for policy change  
**Intervention Type**: Legislative change, ballot initiatives, litigation  
**Example**: Pass state Medicaid expansion → 250,000 newly insured → reduced care avoidance → 12,000 ED visits prevented annually

#### **Scale 2: Institutional (Local Implementation)**
- Hospital integration level (coordinated vs. fragmented care systems)
- Community health worker density (capacity per 100k population)
- Police patrol intensity (surveillance burden)
- Real estate practice norms (discriminatory patterns)
- Healthcare provider behavior (bias, cultural competency)

**Time Horizon**: 1-5 years for institutional change  
**Intervention Type**: Organizational capacity building, training, coordination infrastructure  
**Example**: Integrate CHWs into primary care clinics → 2.1× effect vs. standalone programs → 35% improvement in healthcare continuity

#### **Scale 3: Individual/Household (Lived Experience)**
- Stress exposure (chronic, toxic)
- Healthcare access and utilization
- Economic security (income, assets, debt)
- Social support networks
- Health behaviors (shaped by access and structural conditions)

**Time Horizon**: Months to years for individual health change  
**Intervention Type**: Direct services, case management, mutual aid  
**Example**: Provide rental assistance → housing stability → reduced stress → improved medication adherence → 8% reduction in hospitalizations

### Critical Insight: Multi-Scale Interdependence

Individual-level interventions (CHWs, case management) only work when embedded in supportive structural conditions.

**Evidence**: CHW effect size 2.1× higher in integrated healthcare systems vs. fragmented systems. This isn't noise; it's the mechanism—structural conditions fundamentally reshape individual-level intervention effectiveness.

**Implication**: System models this interdependence explicitly. When user proposes CHW scale-up, system shows: "Projected effect: 0.35 (base) × 1.2 (Boston's integrated healthcare) × 0.9 (urban population density) = 0.38 adjusted effect for Boston."

---

## System Scope and Boundaries

### What This System DOES

✓ **Make causal mechanisms visible and quantifiable**
- Extract complex pathways from 300+ studies per mechanism
- Convert diverse evidence (RR, OR, β, d) into comparable metrics
- Users click any mechanism to see supporting studies, effect sizes, confidence intervals
- Full audit trail from literature to projection

✓ **Compare interventions across geographies**
- Same intervention has different effects in Boston vs. rural Mississippi
- System shows why (policy context, healthcare system, demographics)
- Enables multi-state portfolio analysis for foundations
- Identifies which contexts amplify/dampen specific interventions

✓ **Identify high-leverage intervention points**
- Mechanisms ranked by potential impact
- Filtered through structural competency (root causes, not symptoms)
- Highlights interventions addressing multiple disparities simultaneously
- Shows synergies and redundancies across programs

✓ **Stratify outcomes by equity dimensions**
- Results always broken down by race/ethnicity, SES, insurance status
- Identifies which populations benefit most from each intervention
- Flags when interventions worsen equity (gentrification, displacement)
- Population-specific moderators built into every mechanism

✓ **Handle uncertainty transparently**
- Every outcome has 95% confidence interval
- Sensitivity analysis shows robustness to assumption changes (±20% effect sizes)
- Explicitly states when evidence is weak, correlational, or from non-representative populations
- Monte Carlo simulation for propagated uncertainty through system

✓ **Adapt to local policy and demographic context**
- Mechanisms weighted based on local conditions (moderators)
- Policy environment (Medicaid rules, housing protections) directly affects projections
- Uses available data (no expensive baseline surveys required)
- Improves as local data becomes available

✓ **Suggest intervention combinations addressing multiple disparities**
- System identifies synergies (5 programs together create 1.3× multiplier)
- Shows redundancies (multiple programs addressing same pathway with no coordination)
- Maps complementarity across geographies (where to invest for maximum combined impact)

### What This System DOES NOT Do

✗ **Replace human judgment**
- It's a decision-support tool, not an algorithmic decision-maker
- Consultants, health officials, community leaders make final choices
- Users must understand and validate recommendations before implementation
- Political feasibility, community preferences, and local knowledge override quantitative projections

✗ **Predict exact outcomes**
- Too much uncertainty in real systems (behavior, politics, implementation quality, community response)
- System provides probability ranges and confidence intervals, not point predictions
- Actual outcomes depend on: implementation fidelity, political will, community engagement, unanticipated interactions
- Models are simplifications; some local factors not captured

✗ **Account for every local detail**
- Uses models (~400 nodes, ~2000 mechanisms), not complete system specification
- Some context-specific factors not represented in mechanism bank
- Users should add custom nodes/mechanisms if local knowledge reveals gaps
- Geographic pruning may miss locally-relevant pathways

✗ **Monetize non-health values**
- Housing as home (not just shelter with market price)
- Community as identity and belonging (not just social capital as resource)
- Cultural meaning and place attachment (not instrumental functions)
- System intentionally resists forced monetization into single ROI ratio
- Only crisis health endpoints monetized (ED visits, hospitalizations); intermediate outcomes tracked qualitatively

✗ **Handle intergenerational effects rigorously**
- Time horizons limited to 3-10 years
- Intergenerational transmission (trauma, epigenetics, wealth accumulation) flagged but not precisely modeled
- Users should consult life-course epidemiology frameworks for multi-generational projections
- System notes when effects extend beyond time horizon

✗ **Recommend against interventions**
- Shows tradeoffs, uncertainties, and equity distributions
- Final choice remains user's responsibility
- If field consensus supports intervention, system respects that (doesn't declare it harmful)
- Flags concerns (displacement risk, unintended consequences) but doesn't veto

✗ **Guarantee equity outcomes**
- Projections assume implementation quality, enforcement, community power
- Well-designed intervention can be poorly implemented
- Political feasibility affects real-world results
- Equity depends on: who controls implementation, accountability mechanisms, community voice in design

✗ **Replace community organizing or advocacy**
- Provides evidence to support organizing, not substitute for it
- Community must decide whether to use tool and how
- Tool doesn't replace: relationships, accountability structures, power-building
- Quantification serves organizing goals; doesn't determine them

### Why These Boundaries Exist

| Boundary | Rationale |
|----------|-----------|
| **Not predictive, probabilistic** | Real social systems are chaotic and complex. False precision destroys credibility. Better to be approximately right with quantified uncertainty than precisely wrong. |
| **Not a decision-maker** | Structural change requires human judgment, community input, political strategy. Algorithms cannot make value choices about equity, justice, priorities. |
| **Not purely quantitative** | Some values cannot be monetized without losing meaning. Qualitative evidence matters. Community knowledge complements scientific evidence. |
| **Not modeling everything** | Infinite complexity is unmanageable. Pick what matters most, model it well, be explicit about gaps. Bounded rationality. |
| **Not neutral** | Explicitly structural competency framing. Takes side with equity and justice. Won't recommend extractive interventions even if they improve aggregate metrics. |

### What Users Must Do (System Cannot Do Alone)

1. **Understand local politics**: System identifies leverage points; politics determines feasibility
2. **Engage community**: System suggests directions; community must decide priorities and validate against lived experience
3. **Build implementation capacity**: System shows what works; implementation quality matters more than intervention design
4. **Monitor real outcomes**: Compare actual results to predicted; update mechanism bank based on learnings
5. **Ensure equity in implementation**: System flags which populations should benefit; implementation must ensure it actually happens
6. **Adapt over time**: System provides version control and update process; users decide when to incorporate new evidence

---

## Target Users and Use Cases

### Primary User Personas

#### **Persona 1: State Health Department Director**

**Profile**: 
- Manages $500M annual health budget across 15 programs
- Reports to governor's office and legislature
- Must justify budget allocations with evidence
- Pressure to demonstrate ROI and population health improvement

**Starting Question**: "We spend half a billion on health programs. How do we know which create most health impact? How should we reallocate to maximize outcomes?"

**System Use**:
1. Specify geography: State (e.g., Massachusetts)
2. Specify populations served: Medicaid-eligible adults and children
3. Request: "Show me which interventions prevent most ED visits and hospitalizations"
4. Review: Ranked list with mechanism chains (policy → local conditions → health outcomes), equity distribution, cost-effectiveness, sensitivities
5. Compare: Current portfolio vs. optimized allocation
6. Analyze: Which programs are redundant (addressing same pathway with no coordination)? Which are complementary (addressing different pathways to same outcome)?
7. Model scenarios: "What if we shift $50M from Program A to Program B?" → projected outcome change

**Outcome**: Reallocates budget toward highest-leverage interventions. Justifies decisions to legislature with evidence-based projections. Coordinates across silos (housing assistance, CHW programs, Medicaid expansions addressed as integrated strategy).

**Value Metrics**:
- Evidence-based justification for $500M budget
- 15-25% improvement in health outcomes per dollar (from better allocation)
- Cross-silo coordination (housing + health + employment)
- Defensible against budget cuts (can show projected harm of defunding)

#### **Persona 2: Foundation Portfolio Director**

**Profile**:
- Manages $100M grantmaking across health, housing, employment
- Funds 50 different organizations across 5 states
- Must report impact to board and donors
- Seeks to maximize health equity outcomes

**Starting Question**: "We fund 50 programs across 5 states. Are they complementary or redundant? What's the comparative ROI? How do we rebalance portfolio for maximum equity impact?"

**System Use**:
1. Specify: 5 states where foundation operates
2. Input: 50 grantee interventions (program type, location, population, budget)
3. System analyzes:
   - Which mechanisms does each program address?
   - Are multiple programs addressing same pathway in same geography (redundancy)?
   - Are there complementary programs whose combined effect > sum of parts (synergy)?
   - Which geographies have gaps (high-impact mechanisms with no funded intervention)?
4. Compare ROI across states:
   - Same program type (legal defense for housing) has different impacts in different states (policy context reshapes effectiveness)
   - Identify: which state contexts amplify certain intervention types
5. Equity analysis:
   - Which programs reduce disparities vs. maintain them?
   - Which populations benefit from current portfolio vs. which are underserved?
6. Optimization:
   - System suggests portfolio rebalancing to maximize equity-weighted health outcomes
   - Shows: "Move $5M from State X (where this intervention has weak effect) to State Y (where policy context amplifies it)"

**Outcome**: Rebalances portfolio, reduces redundancy (saves $8M redirected to gaps), amplifies complementary programs (creates 1.4× multiplier through coordination), achieves 30% improvement in equity-weighted outcomes without increasing budget.

**Value Metrics**:
- Standardized impact comparison across 50 diverse programs
- Portfolio optimization (save money, improve outcomes)
- Evidence for board/donors (transparent methodology, defensible assumptions)
- Learning what works where (policy context insights)

#### **Persona 3: Community Organization Executive Director**

**Profile**:
- Runs community center serving 5,000 residents annually
- Operates 5 programs: food access, youth mentoring, family counseling, job training, organizing/advocacy
- Must justify impact to city government, foundations, and community
- Limited capacity for data collection and evaluation

**Starting Question**: "Our programs address root causes, but funders want quantified health impact. How do we demonstrate that organizing and integrated services create structural change that reduces health crises?"

**System Use** (via consultant using platform):
1. Consultant inputs: 5 programs with descriptions, populations served, estimated reach
2. System maps:
   - Food access → economic precarity reduction → medication adherence → reduced ED visits
   - Job training → income stability → housing stability → stress reduction → improved health
   - Organizing/advocacy → policy change (rent control, living wage) → population-level structural improvements
3. System shows:
   - Each program addresses different mechanisms in health system
   - Integrated approach creates synergies (clients access multiple services → multiplicative effect)
   - Organizing/advocacy has leverage (policy wins affect entire population, not just clients)
4. Output: Plain-language report with:
   - Estimated health impact (ED visits prevented, hospitalizations avoided)
   - Cost-effectiveness ($ per health outcome)
   - Equity distribution (who benefits)
   - Mechanism chains (makes structural logic visible)
   - Comparison to medicalized interventions (demonstrates community approach is competitive)

**Outcome**: Can now demonstrate to city council that $500k investment generates $2.1M in health value (4.2:1 ROI). Secures renewed funding. Uses evidence in organizing campaigns ("our programs prevent 450 ED visits annually—defunding would shift costs to hospitals").

**Value Metrics**:
- Credible quantification for funding justification
- Competitive comparison to clinical interventions
- Evidence for organizing/advocacy (makes structural change tangible)
- Plain-language explanation (accessible to community members and non-technical funders)

### Secondary User Personas

#### **Persona 4: Academic Researcher**

**Use**: Teaching tool for public health, urban planning, policy analysis courses. Research platform for generating publishable analyses.

**Value**: Students learn systems thinking + evidence synthesis. Mechanism bank serves as literature review infrastructure. Publications demonstrate real-world application of research.

#### **Persona 5: Policy Analyst**

**Use**: Model health impacts of proposed legislation before passage. Compare policy alternatives.

**Value**: Evidence-based policy design. Identify unintended consequences. Justify recommendations to legislators.

#### **Persona 6: Consultant / Technical Assistance Provider**

**Use**: Platform-assisted consulting for complex health equity decisions.

**Value**: Augments expertise with systematic analysis. Reduces engagement time from 6 months to 6 weeks. Transparent methodology clients can understand and validate.

---

## Competitive Differentiation

### Comparison Matrix

| Factor | SROI Tools (Sopact, PowerSROI) | Health Impact Assessment (Manual HIA) | Academic System Dynamics Models | **This Platform** |
|--------|-------------|-----------|-----------------|-------------------|
| **Speed** | Weeks (per project) | 6-18 months (per assessment) | Months (custom model per context) | Real-time scenarios (seconds) after geography setup |
| **Transparency** | Black-box monetization algorithms | Documented but qualitative | Published methodology but inaccessible | Full audit trail, clickable to source studies |
| **Actor Network Layer** | None | Sometimes qualitative | No | Built-in Phase 2 (organizational infrastructure mapped to mechanisms) |
| **System Visualization** | None | Qualitative diagrams | Possible but technical | Central feature; interactive, clickable nodes/mechanisms |
| **Equity Lens** | Generic diversity categories | Optional consideration | Rarely included | Primary; outcomes always stratified, disparities drive intervention selection |
| **Scalability** | Low (custom per project) | Very low (manual process) | Low (PhD expertise required) | High (templated discovery, reusable mechanism bank) |
| **Cost** | $50k-$300k per project | $100k-$500k per assessment | High (researcher time + months) | $80k-$400k annually (unlimited scenarios) |
| **Mechanism Source** | Assumed; not specified | Literature review per project | Hand-curated per model | LLM-synthesized from 300+ papers; auditable |
| **Effect Sizes** | Forced monetization into single ratio | Not quantified | Rigorously calibrated | Quantified + qualitative; handles uncertainty; literature-derived + context-adapted |
| **Context Handling** | Generic assumptions | Project-specific | Fixed per study | Adaptive; policy/demographic/geographic moderators explicit |
| **Reusability** | Low (findings don't generalize) | None (qualitative, project-specific) | None (model is context-specific) | High (mechanism bank reusable across geographies) |
| **Update Process** | Manual revision | New assessment required | Rebuild model | Systematic (new literature → LLM → validation → deploy update) |

### Unique Value Propositions

**vs. SROI Tools**:
- We don't force everything into monetized single ratio (SROI tools lose equity information)
- We show mechanism chains (SROI tools are black boxes)
- We adapt to geography (SROI tools use generic assumptions)
- We enable scenario comparison (SROI tools are project-by-project)

**vs. Manual HIA**:
- We quantify effects (HIA is qualitative)
- We scale across geographies (HIA is manual per project)
- We enable real-time scenario testing (HIA takes months)
- We maintain reusable mechanism bank (HIA starts from scratch each time)

**vs. Academic Models**:
- We're accessible to practitioners (academic models require PhD expertise)
- We're rapid (academic models take months to build)
- We're transparent (academic models are published but dense)
- We integrate equity (academic models rarely center justice)

**vs. All Existing Tools**:
- Only platform combining: systems thinking (feedback loops) + epidemiological rigor (effect sizes, CIs) + equity centering (stratified outcomes) + scalability (reusable mechanisms) + transparency (auditable assumptions)

---

## Document Metadata

**Version History**:
- v1.0 (2024-06): Initial foundations document
- v2.0 (2025-11): Major revision integrating SD paradigm, clarifying scope, expanding use cases

**Related Documents**:
- [02_METHODOLOGICAL_INTEGRATION.md] - Deep dive on SD + SEM + Bayesian synthesis
- [03_SYSTEM_ARCHITECTURE_OVERVIEW.md] - Technical system design
- [15_USER_INTERFACE_WORKFLOWS.md] - Detailed user interaction specifications

**Last Reviewed**: November 15, 2025  
**Next Review**: May 15, 2026 (6-month cycle for foundational documents)

**Maintainers**: Technical Architecture Team  
**Contributors**: Domain experts in public health, systems dynamics, equity research

---

**END OF DOCUMENT**
