# Node and System Definitions

**Version:** 1.1
**Last Updated:** 2025-11-19
**Purpose:** Foundational framework defining nodes, systems, and organizational principles for the HealthSystems Platform

---

## Table of Contents

1. [Core Concepts](#core-concepts)
2. [What is a Node?](#what-is-a-node)
3. [What is NOT a Node?](#what-is-not-a-node)
4. [Scale Hierarchy](#scale-hierarchy)
5. [Domain Taxonomy](#domain-taxonomy)
6. [Measurement Principles](#measurement-principles)
7. [Relationship to Mechanisms and Interventions](#relationship-to-mechanisms-and-interventions)
8. [Node Specification Standards](#node-specification-standards)
9. [Examples and Edge Cases](#examples-and-edge-cases)

---

## Core Concepts

### System Definition

A **health system** is the complete network of factors, processes, and feedback loops that determine population health outcomes. This includes:

- **Structural determinants (Scale 1-2)** - Policies, economic systems, power structures at federal/state level
- **Institutional infrastructure (Scale 3)** - Organizations, facilities, service delivery systems
- **Individual/household conditions (Scale 4)** - Lived experiences, resources, exposures at the individual level
- **Intermediate pathways (Scale 6)** - Behaviors, biological states, utilization patterns that mediate outcomes
- **Crisis endpoints (Scale 7)** - Health outcomes, system failures, mortality events

### Node Definition

A **node** is a measurable state variable within the health system that:

1. **Describes a condition or state** (not an action or intervention)
2. **Can be observed and quantified** with available or feasible data
3. **Represents a stock or rate** that accumulates or flows over time
4. **Influences or is influenced by** other nodes through mechanisms
5. **Exists independent of any specific intervention** (though interventions may affect it)

**Key Principle:** Nodes are **descriptive**, not **prescriptive**. They describe "what is" rather than "what should be done."

---

## What is a Node?

### Valid Node Types

#### 1. **State Variables (Stocks)**
Quantities that accumulate over time and can be measured at a point in time.

**Examples:**
- Uninsured population (persons)
- Affordable housing units (housing units)
- Physician density (physicians per 100,000 population)
- Median household income (dollars)
- Air pollution concentration (μg/m³ PM2.5)

#### 2. **Rate Variables (Flows)**
Quantities that measure change over time or frequency of events.

**Examples:**
- Eviction rate (evictions per 100 renter households per year)
- Hospitalization rate (admissions per 1,000 persons per year)
- Unemployment rate (% of labor force)
- Food insecurity rate (% of households)
- Overdose mortality rate (deaths per 100,000 population per year)

#### 3. **Policy State Variables**
Binary or categorical states describing policy regimes in force.

**Examples:**
- Medicaid expansion status (binary: expanded/not expanded)
- Minimum wage level (dollars per hour)
- Rent control stringency (categorical: none/moderate/strict)
- Cash bail reform status (binary: reformed/not reformed)

#### 4. **Quality/Intensity Measures**
Characteristics describing the quality or intensity of a condition.

**Examples:**
- Housing cost burden (% of income spent on housing)
- Network adequacy (% of needed specialists in network)
- Cultural competency training hours (hours per year)
- Transit service frequency (buses per hour)

#### 5. **Access/Availability Measures**
Geographic, financial, or temporal barriers to resources.

**Examples:**
- Distance to nearest primary care provider (miles)
- Pharmacy desert status (binary: yes/no)
- SNAP enrollment wait time (days)
- Transit route density (routes per square mile)

#### 6. **Exposure Measures**
Environmental, social, or occupational hazards.

**Examples:**
- Lead exposure prevalence (% of children with BLL ≥5 μg/dL)
- Workplace injury rate (injuries per 100 FTE workers per year)
- Noise exposure (decibels)
- Discrimination experiences (% reporting)

---

## What is NOT a Node?

### Invalid Node Types

#### 1. **Specific Interventions or Programs**
Interventions are **changes made to nodes**, not nodes themselves.

**NOT Nodes:**
- ❌ "Housing First program implementation"
- ❌ "Community health worker outreach campaign"
- ❌ "Smoking cessation intervention"
- ❌ "Diabetes prevention program enrollment"

**Why:** These are **actions** taken to change node values, not states that can be observed.

**Correct Formulation:**
- ✅ "Permanent supportive housing units" (the program creates units, which is the node)
- ✅ "Community health worker density" (the campaign affects density)
- ✅ "Smoking prevalence" (the intervention aims to reduce this node)
- ✅ "Diabetes prevention program capacity" (enrollment happens within this capacity)

#### 2. **Process Verbs or Actions**
Nodes describe states, not processes.

**NOT Nodes:**
- ❌ "Screening patients for social needs"
- ❌ "Implementing medication reconciliation"
- ❌ "Providing culturally competent care"

**Correct Formulation:**
- ✅ "Social needs screening rate" (% of patients screened)
- ✅ "Medication reconciliation completion rate" (% of admissions)
- ✅ "Cultural competency training completion" (% of staff trained)

#### 3. **Outcomes of Specific Research Studies**
Nodes must be generalizable population-level measures.

**NOT Nodes:**
- ❌ "Efficacy of intervention X in RCT Y"
- ❌ "Effect size from meta-analysis Z"

**Why:** These are **evidence about mechanisms**, not observable system states.

#### 4. **Subjective Goals or Aspirations**
Nodes must be objectively measurable.

**NOT Nodes:**
- ❌ "Health equity" (too broad)
- ❌ "Community wellbeing" (undefined)
- ❌ "Good housing" (subjective)

**Correct Formulation:**
- ✅ "Racial disparity in life expectancy" (years difference)
- ✅ "Community cohesion index" (validated scale score)
- ✅ "Housing quality deficiencies" (% of units with code violations)

#### 5. **Composite Indices Without Clear Definition**
If a node is an index, its construction must be specified.

**NOT Nodes (as stated):**
- ❌ "Neighborhood quality"
- ❌ "Healthcare system strength"

**Correct Formulation:**
- ✅ "Neighborhood Deprivation Index" (specify: composite of income, education, employment, housing)
- ✅ "Healthcare Access and Quality Index" (specify: composite of coverage, utilization, outcomes)

---

## Scale Hierarchy

Nodes are organized by the **level of system operation** they represent, forming a causal hierarchy from macro-structures to individual outcomes. The system uses a **1-7 scale** where:
- **1 = Structural determinants** (federal/state policy level)
- **2 = Built environment & infrastructure** (physical environment and regional structures)
- **3 = Institutional infrastructure** (organizations and service delivery)
- **4 = Individual/household conditions** (lived experiences)
- **5 = Individual behaviors & psychosocial** (health-seeking, adherence, coping)
- **6 = Intermediate pathways** (clinical measures and utilization patterns)
- **7 = Crisis endpoints** (acute health outcomes and mortality)

The 7-scale taxonomy reflects **causal distance** from health outcomes (decades → years → months → weeks → days → hours → immediate) and the **structural → individual spectrum** from macro-policy to crisis response.

### Scale 1: STRUCTURAL DETERMINANTS
**Entirely Structural - Federal/State Policy Level**

**Definition:** Policy regimes, laws, regulations, and macro-economic conditions that shape the rules and resources available across populations.

**Characteristics:**
- Set by legislation, regulation, or macro-economic forces
- Apply broadly across jurisdictions (federal, state, or regional)
- Change slowly (legislative timescales)
- Create the "opportunity structure" for institutions and individuals

**Domains:**
- Healthcare system policy
- Housing policy
- Labor and employment policy
- Criminal justice policy
- Education and child welfare policy
- Environmental and climate policy
- Taxation and fiscal policy
- Infrastructure investment policy
- Trade and economic policy

**Example Nodes:**
- Medicaid expansion status
- Minimum wage level
- Rent control stringency
- Mass incarceration rate
- Clean Air Act enforcement stringency

---

### Scale 2: BUILT ENVIRONMENT & INFRASTRUCTURE
**Physical Infrastructure, Environmental Quality, and Regional Structural Factors**

**Definition:** The physical environment, infrastructure systems, and environmental quality measures that shape health opportunities and exposures at the regional or neighborhood level. These structural factors sit between macro-policy (Scale 1) and institutional implementation (Scale 3).

**Characteristics:**
- Physical/environmental rather than policy or institutional
- Regional or neighborhood-level variation
- Changes occur over years to decades (slower than individual conditions)
- Shapes opportunities for health behaviors and exposures
- Often measurable through environmental monitoring or GIS data

**Causal Distance:** Years to decades from health outcomes

**Domains:**
- Air quality and pollution (PM2.5, ozone, pollutants)
- Water quality and contamination
- Noise pollution and environmental noise
- Climate and heat exposure (urban heat islands, extreme heat days)
- Green space and tree canopy (parks, natural areas)
- Walkability and pedestrian infrastructure (sidewalks, street connectivity)
- Transportation infrastructure (transit access, bike lanes, public transit density)
- Food environment (food deserts, grocery store access, supermarket density)
- Housing stock quality and age
- Neighborhood design and built environment quality

**Example Nodes:**
- PM2.5 air pollution concentration (μg/m³)
- Noise exposure level (decibels)
- Urban heat island intensity (°F above rural baseline)
- Green space per capita (acres per 1,000 residents)
- Walkability score (index 0-100)
- Transit stop density (stops per square mile)
- Food desert status (binary: yes/no grocery access within 1 mile)
- Bike lane mileage per capita
- Housing stock age (median year built)
- Street connectivity (intersection density)

---

### Scale 3: INSTITUTIONAL INFRASTRUCTURE
**Organizations, Systems, and Institutional Capacity**

**Definition:** Organizations, facilities, workforce, and local systems that deliver services and implement structural policies on the ground.

**Characteristics:**
- Operated by institutions (hospitals, agencies, schools, etc.)
- Geographic variation within policy contexts
- Capacity and quality vary based on funding and governance
- Intermediate between policy and individual experience

**Domains:**
- Healthcare delivery infrastructure
- Housing infrastructure and enforcement
- Social service organizations
- Education infrastructure
- Built environment and transportation
- Criminal justice system implementation
- Environmental infrastructure
- Public health infrastructure
- Community-based organizations

**Example Nodes:**
- Primary care physician density
- Affordable housing units per capita
- SNAP outreach worker caseload
- School nurse availability
- Transit route density
- Police per capita
- Air quality monitoring stations

---

### Scale 4: INDIVIDUAL/HOUSEHOLD CONDITIONS
**Proximal Living Conditions and Exposures**

**Definition:** The actual conditions, resources, exposures, and constraints experienced by individuals and households in their daily lives.

**Characteristics:**
- Directly experienced by people
- Shaped by structural and institutional factors
- High interpersonal variation
- Measurable through surveys, administrative data, or direct assessment

**Domains:**
- Economic security
- Housing stability and quality
- Healthcare access and coverage
- Food security
- Social connectedness and discrimination
- Environmental exposures
- Education and child development
- Employment conditions and occupational exposures
- Stress, trauma, and adversity
- Justice system contact
- Digital access and literacy
- Transportation access and burden

**Example Nodes:**
- Household income
- Housing cost burden
- Uninsured status
- Food insecurity
- Social isolation
- Lead exposure
- Educational attainment
- Workplace injury exposure
- Adverse childhood experiences
- Arrest rate
- Broadband access

---

### Scale 5: INDIVIDUAL BEHAVIORS & PSYCHOSOCIAL FACTORS
**Health-Seeking, Adherence, Coping, and Individual-Level Actions**

**Definition:** Individual-level behaviors, health-seeking actions, adherence patterns, and psychosocial responses that mediate between living conditions (Scale 4) and biological pathways (Scale 6). These represent individual agency operating within structural constraints.

**Characteristics:**
- Individual actions and choices (constrained by upstream factors)
- Modifiable through education, support, or behavior change interventions
- Shorter causal distance than conditions (days to weeks to health impacts)
- Bridge between material conditions and biological embodiment
- Often measured through surveys, self-report, or behavioral tracking

**Causal Distance:** Days to weeks from health outcomes

**Domains:**
- Healthcare-seeking and utilization behaviors
  - Medication adherence and compliance
  - Well-visit adherence (pediatric, adult preventive)
  - Screening adherence (cancer, chronic disease)
  - Care-seeking when sick
  - Delayed or forgone care due to barriers
  - Treatment adherence and follow-up

- Health risk behaviors
  - Tobacco use and smoking
  - Alcohol consumption patterns
  - Substance use behaviors
  - Physical activity and exercise
  - Sedentary behavior
  - Dietary patterns and nutrition choices

- Psychosocial factors
  - Health literacy and health knowledge
  - Patient activation and self-efficacy
  - Coping strategies and stress management
  - Social support utilization
  - Resilience and adaptation
  - Help-seeking behaviors

**Important Distinction:**
- **Scale 4 = Conditions** ("Can't afford medications" - material constraint)
- **Scale 5 = Behaviors** ("Skipping doses to save money" - behavioral response to constraint)

**Example Nodes:**
- Medication adherence rate (% taking as prescribed)
- Medication nonadherence (% not taking as prescribed)
- Well-child visit adherence (% on schedule)
- Preventive screening adherence (mammography, colonoscopy on time)
- Delayed care due to cost (% reporting)
- Forgone medical care (% with unmet need)
- Current smoking prevalence (% current smokers)
- Binge drinking prevalence (% reporting)
- Physical activity level (minutes per week)
- Sedentary behavior (hours per day)
- Fruit and vegetable consumption (servings per day)
- Health literacy score (index 0-100)
- Patient activation measure (PAM score)

**Key Insight:** Scale 5 behaviors are NOT freely chosen - they are shaped and constrained by Scale 1-4 structural and material conditions. This taxonomy explicitly rejects victim-blaming narratives by positioning behaviors DOWNSTREAM of structural determinants.

---

### Scale 6: INTERMEDIATE PATHWAYS
**Behaviors, Utilization, and Intermediate Risk Factors**

**Definition:** States and behaviors that mediate between living conditions and health outcomes. These are often partially modifiable by individuals but heavily constrained by upstream conditions.

**Characteristics:**
- Proximate to health outcomes in causal chains
- Influenced by individual/household conditions
- Include behaviors, biological risk factors, and healthcare utilization
- Often targets of clinical or behavioral interventions

**Domains:**
- Healthcare utilization and preventive care
- Chronic disease control and management
- Mental health and substance use treatment
- Health behaviors (smoking, physical activity, diet)
- Biological risk factors (blood pressure, glucose, BMI)
- Housing and neighborhood conditions
- Physiological stress (allostatic load)

**Example Nodes:**
- Preventive care utilization rate
- Diabetes control (HbA1c <7%)
- Mental health treatment rate
- Smoking prevalence
- Physical activity levels
- Hypertension control
- Medication adherence
- Allostatic load

---

### Scale 7: CRISIS ENDPOINTS
**Pure Crisis Endpoints - Acute Health Outcomes and Crises**

**Definition:** Acute health crises, chronic disease states, mortality, and other ultimate outcomes that the system seeks to prevent or minimize.

**Characteristics:**
- Represent system failures or disease burden
- Costly (medically, economically, socially)
- Often monetizable for policy analysis
- Lag indicators of upstream system performance

**Domains:**
- Acute care utilization (ED, hospitalization, ICU)
- Chronic disease prevalence
- Mental health and substance use crises
- Mortality (all-cause, premature, infant, maternal)
- Birth outcomes
- Disability and functional limitation
- Homelessness and housing crises
- Criminal justice involvement
- Medical bankruptcy and financial toxicity

**Example Nodes:**
- Emergency department visits
- Hospitalization rate
- ICU days
- Hospital readmissions
- Diabetes prevalence
- Hypertension prevalence
- Depression prevalence
- Suicide attempts
- Overdose deaths
- All-cause mortality
- Premature mortality (YPLL)
- Infant mortality
- Maternal mortality
- Adverse birth outcomes
- Disability-adjusted life years (DALYs)
- Homelessness person-years
- Incarceration rate
- Medical bankruptcy rate

---

## Domain Taxonomy

Domains represent **substantive areas of the health system** and cut across scales. A single domain (e.g., "Housing") includes nodes at structural, institutional, and individual levels.

### Primary Domains

#### 1. **Healthcare System**
- **Structural:** Insurance policy, coverage mandates, reimbursement rules, pharmaceutical regulation
- **Institutional:** Hospitals, clinics, providers, infrastructure, quality systems
- **Individual:** Coverage, access, utilization, continuity of care
- **Intermediate:** Preventive care, chronic disease management, medication adherence
- **Crisis:** ED visits, hospitalizations, readmissions, iatrogenic harms

#### 2. **Housing**
- **Structural:** Housing policy (rent control, public housing, vouchers, eviction laws)
- **Institutional:** Affordable housing stock, code enforcement, legal representation
- **Individual:** Housing cost burden, stability, quality, homelessness
- **Intermediate:** Home-based health risks (mold, lead, crowding)
- **Crisis:** Homelessness person-years, housing-related health crises

#### 3. **Economic Security**
- **Structural:** Labor policy (minimum wage, paid leave, unionization), taxation, safety net
- **Institutional:** Job training, benefits enrollment, case management
- **Individual:** Income, wealth, poverty, debt, employment status
- **Intermediate:** Economic stress, material hardship
- **Crisis:** Medical bankruptcy, financial toxicity, eviction

#### 4. **Employment and Occupational Health**
- **Structural:** Labor laws, workers' compensation, OSHA standards, union rights
- **Institutional:** Workplace safety infrastructure, enforcement, employee assistance
- **Individual:** Job quality, occupational exposures, workplace discrimination
- **Intermediate:** Work-related injuries and illnesses
- **Crisis:** Occupational fatalities, permanent disability

#### 5. **Food Security**
- **Structural:** SNAP policy, agricultural subsidies, nutrition standards
- **Institutional:** Food retail, food assistance infrastructure, food pantries
- **Individual:** Food insecurity, SNAP participation, diet quality
- **Intermediate:** Nutritional status, diet-related risk factors
- **Crisis:** Malnutrition, food-insecure health crises

#### 6. **Education**
- **Structural:** Education policy, funding formulas, school accountability
- **Institutional:** School infrastructure, staffing, programs
- **Individual:** Educational attainment, school experiences, childhood development
- **Intermediate:** Literacy, cognitive function
- **Crisis:** School dropout, developmental delays

#### 7. **Built Environment and Transportation**
- **Structural:** Transit funding, infrastructure investment, zoning, environmental regulation
- **Institutional:** Transit systems, parks, bike lanes, walkability infrastructure
- **Individual:** Transit access, commute burden, green space access, active transportation
- **Intermediate:** Physical activity, transportation barriers to care
- **Crisis:** Traffic injuries, heat-related illness

#### 8. **Environmental and Climate**
- **Structural:** Environmental regulation (Clean Air Act, lead abatement), climate policy
- **Institutional:** Air quality monitoring, lead remediation, climate adaptation infrastructure
- **Individual:** Air pollution exposure, lead exposure, heat exposure, flooding risk
- **Intermediate:** Respiratory function, heat stress
- **Crisis:** Asthma exacerbations, heat stroke, climate-related disasters

#### 9. **Criminal Justice**
- **Structural:** Sentencing laws, bail reform, drug policy, policing standards
- **Institutional:** Police, courts, jails, diversion programs, reentry services
- **Individual:** Arrest rate, incarceration exposure, justice system contact
- **Intermediate:** Reentry challenges, supervision conditions
- **Crisis:** Incarceration person-years, recidivism

#### 10. **Social Environment**
- **Structural:** Anti-discrimination law, civil rights enforcement
- **Institutional:** Community organizations, faith-based organizations, social cohesion programs
- **Individual:** Social isolation, discrimination experiences, community trust, civic engagement
- **Intermediate:** Social support, collective efficacy
- **Crisis:** Social isolation-related health outcomes

#### 11. **Behavioral Health**
- **Structural:** Mental health parity, substance use policy, commitment laws
- **Institutional:** Psychiatric beds, crisis services, treatment facilities, integrated care
- **Individual:** Mental health status, substance use, treatment access
- **Intermediate:** Mental health treatment, MAT, harm reduction
- **Crisis:** Suicide, overdose, psychiatric ED boarding, involuntary commitment

#### 12. **Long-Term Services and Supports**
- **Structural:** Medicaid LTSS policy, HCBS waivers, caregiver support policy
- **Institutional:** Nursing homes, assisted living, home health, adult day services
- **Individual:** Disability, ADL limitations, caregiver burden
- **Intermediate:** LTSS utilization, caregiver support
- **Crisis:** Nursing home admissions, caregiver burnout

#### 13. **Maternal and Child Health**
- **Structural:** Pregnancy Medicaid, WIC, EPSDT, family leave policy
- **Institutional:** OB/GYN access, NICU capacity, home visiting, well-child care
- **Individual:** Prenatal care access, birth spacing, breastfeeding
- **Intermediate:** Prenatal care utilization, postpartum care, well-child visits
- **Crisis:** Maternal mortality, infant mortality, adverse birth outcomes

#### 14. **Specialized Clinical Areas**
- Cancer care, kidney disease, organ transplantation, rehabilitation, oral health, vision and hearing, pain and palliative care, geriatrics
- Each includes structural, institutional, individual, intermediate, and crisis nodes

#### 15. **Public Health Infrastructure**
- **Structural:** Public health funding, legal authority, preparedness mandates
- **Institutional:** Health departments, surveillance systems, immunization infrastructure
- **Individual:** Immunization status, outbreak exposure
- **Intermediate:** Disease incidence, outbreak response
- **Crisis:** Epidemics, pandemic deaths

#### 16. **Digital and Information Access**
- **Structural:** Broadband policy, digital equity funding, telehealth regulation
- **Institutional:** Broadband infrastructure, digital literacy programs, telehealth platforms
- **Individual:** Internet access, device ownership, digital literacy
- **Intermediate:** Telehealth utilization, online health information seeking
- **Crisis:** Digital divide-related health disparities

#### 17. **Civic and Political Engagement**
- **Structural:** Voting rights, redistricting, campaign finance
- **Institutional:** Voter registration infrastructure, community organizing capacity
- **Individual:** Voter registration, turnout, civic participation
- **Intermediate:** Political efficacy, collective action
- **Crisis:** Disenfranchisement, civic disempowerment

---

## Measurement Principles

### 1. **Observability**
Every node must be **observable** in principle, even if current data are limited.

**Criteria:**
- Defined operational measurement approach exists or can be developed
- Measurement units are specified (%, count, rate, dollars, etc.)
- Measurement can be repeated over time
- Measurement can be disaggregated (by geography, demographics) when relevant

### 2. **Data Feasibility**
Prefer nodes with **existing data sources**, but include critical nodes even if data are currently unavailable.

**Data Tiers:**
- **Tier 1 (Excellent):** Routinely collected, publicly available, high quality (e.g., vital statistics, ACS, NHIS)
- **Tier 2 (Good):** Periodic surveys or administrative data with known limitations (e.g., BRFSS, HCUP, claims)
- **Tier 3 (Feasible):** Requires data linkage or special surveys, but feasible (e.g., linked survey-claims)
- **Tier 4 (Aspirational):** Not currently measured but measurable with investment (e.g., workplace injury surveillance in gig economy)

**Documentation Required:**
- Primary data source(s)
- Geographic granularity available
- Temporal frequency (annual, biennial, etc.)
- Known data quality issues

### 3. **Quantification**
All nodes must have **defined units of measurement**.

**Common Units:**
- **Counts:** Persons, units, facilities, workers
- **Rates:** Per 100,000 population, per 100 households, per 1,000 births
- **Percentages:** % of population, % of income, % with characteristic
- **Dollars:** Income, costs, expenditures
- **Time:** Days, years, hours
- **Physical units:** μg/m³, mg/dL, decibels, miles
- **Scores:** Index scores (specify range and construction)
- **Binary:** Yes/no, present/absent, implemented/not implemented

### 4. **Baseline Values**
Where possible, provide **US baseline values** to anchor the node in reality.

**Preferred Sources:**
- National representative surveys (NHIS, NHANES, ACS, CPS)
- Vital statistics (CDC WONDER)
- Administrative data (CMS, AHRQ, BLS)
- Peer-reviewed estimates

**Include:**
- National average/median
- Range or distribution (e.g., interquartile range, state variation)
- Disparities (by race/ethnicity, income, geography) if relevant
- Temporal trend (increasing/decreasing/stable)

### 5. **Temporal Dynamics**
Consider how nodes change over time.

**Stock vs. Flow:**
- **Stocks accumulate:** Housing units, population with insurance, physician supply
- **Flows occur over time:** Evictions per year, hospitalizations per year, new diagnoses per year

**Timescales:**
- **Fast:** Can change rapidly (weeks to months): Insurance coverage, employment
- **Medium:** Changes over years: Housing stock, provider supply, health behaviors
- **Slow:** Changes over decades: Educational attainment distribution, built environment

### 6. **Geographic Granularity**
Specify the **finest geographic level** at which the node can be meaningfully measured.

**Common Levels:**
- National
- State
- County
- ZIP code / ZCTA
- Census tract
- Neighborhood / block group
- Facility / organization catchment area

---

## Relationship to Mechanisms and Interventions

### Nodes, Mechanisms, and Interventions Form a System

```
[INTERVENTION] → changes → [NODE A] → [MECHANISM] → affects → [NODE B]
```

**Example:**
```
[Medicaid Expansion] → increases → [Insurance Coverage Rate]
                                           ↓
                                    [Access Mechanism]
                                           ↓
                                   → increases → [Primary Care Utilization]
                                                        ↓
                                                 [Prevention Mechanism]
                                                        ↓
                                                → decreases → [Preventable Hospitalization Rate]
```

### Mechanisms

A **mechanism** is a causal pathway connecting two or more nodes.

**Mechanism Definition:**
- **Source node(s):** The upstream condition(s)
- **Target node(s):** The downstream outcome(s)
- **Pathway:** The biological, behavioral, social, or structural process linking them
- **Direction:** Positive or negative influence
- **Strength:** Effect size (from evidence)
- **Evidence base:** Supporting research

**Example Mechanism:**
- **Name:** Housing Cost Burden to Mental Health
- **Source:** Housing cost burden (% of income on rent)
- **Target:** Depression prevalence (%)
- **Pathway:** Economic stress → cortisol dysregulation + sleep disruption + coping depletion → depressive symptoms
- **Direction:** Positive (higher burden → higher depression)
- **Strength:** +0.15 correlation (meta-analysis)
- **Evidence:** 15 studies, systematic review

**Mechanisms are NOT nodes.** They describe relationships *between* nodes.

### Interventions

An **intervention** is a deliberate change to one or more nodes, intended to propagate through mechanisms to improve outcomes.

**Intervention Definition:**
- **Target node(s):** Which node(s) does the intervention directly change?
- **Magnitude:** How much does it change the target node?
- **Mechanism(s) activated:** Which causal pathways propagate the change?
- **Downstream effects:** What other nodes are affected via mechanisms?
- **Implementation:** Who delivers it, where, to whom, at what cost?

**Example Intervention:**
- **Name:** Emergency rental assistance program
- **Target nodes:**
  - Housing cost burden (reduces by 10 percentage points)
  - Eviction rate (reduces by 50%)
- **Mechanisms activated:**
  - Housing stability → mental health
  - Economic stress reduction → physical health
  - Residential continuity → healthcare access
- **Downstream effects:**
  - Depression prevalence ↓
  - ED visits ↓
  - Chronic disease control ↑
- **Implementation:** County social services, $2,000/household, 6-month assistance

**Interventions are NOT nodes.** They are changes *to* nodes.

### Node-Mechanism-Intervention Workflow

1. **Define nodes:** Establish all measurable system states
2. **Map mechanisms:** Identify evidence-based causal pathways between nodes
3. **Design interventions:** Select target nodes and predict propagation via mechanisms
4. **Simulate:** Model how intervention-induced node changes flow through mechanisms
5. **Evaluate:** Measure actual node changes and compare to predictions

---

## Node Specification Standards

Every node in the inventory must include the following fields:

### Required Fields

#### 1. **Node Name**
- Clear, descriptive, standardized name
- Avoid abbreviations unless universally understood
- Use consistent terminology across related nodes

**Examples:**
- "Uninsured Rate"
- "Primary Care Physician Density"
- "Housing Cost Burden"
- "Air Pollution Concentration (PM2.5)"

#### 2. **Scale**
- Numeric value: 1 (entirely structural), 3 (institutional), 4 (individual/household), 6 (intermediate pathways), or 7 (crisis endpoints)
- Note: Scales 2 and 5 reserved for future taxonomy refinement

#### 3. **Domain(s)**
- Primary domain
- Secondary domain(s) if applicable (nodes can belong to multiple domains)

#### 4. **Type**
- Stock, Rate, Policy, Quality/Intensity, Access/Availability, Exposure, or other

#### 5. **Unit of Measurement**
- Precise units with denominators where applicable
- Include time period for rates

**Examples:**
- "Percent of population under age 65"
- "Per 100,000 population per year"
- "Dollars (2023 USD)"
- "μg/m³"
- "Binary: 0=not expanded, 1=expanded"

#### 6. **Description**
- 2-4 sentence operational definition
- Specify population denominator if relevant
- Clarify any ambiguities or edge cases
- Note any important measurement nuances

#### 7. **Baseline US Value**
- National estimate with year
- Range or variation if available
- Notable disparities if relevant
- Source for the baseline

**Example:**
"14.5% (2019, pre-COVID). Range: 2.5% (MA) to 18.4% (TX). Disparities: Hispanic 18.7%, Black 10.8%, White 7.9%. Source: ACS 2019."

#### 8. **Data Source(s)**
- Primary source(s) with full name and abbreviation
- URL or citation if available
- Geographic and temporal granularity
- Any known data quality limitations

**Example:**
"American Community Survey (ACS), 1-year estimates. Available annually at state, county, and ZCTA levels. Limitation: Undercounts undocumented immigrants. https://www.census.gov/programs-surveys/acs"

### Optional But Recommended Fields

#### 9. **Temporal Trend**
- Increasing, decreasing, stable, cyclical
- Brief description of recent trajectory

#### 10. **Related Nodes**
- Cross-references to closely related nodes
- Helps identify potential mechanisms

#### 11. **Policy Relevance**
- Which policies or interventions commonly target this node?

#### 12. **Equity Considerations**
- Known disparities or measurement issues affecting equity analysis

---

## Examples and Edge Cases

### Example 1: Clear Node

**Node Name:** Uninsured Rate
**Scale:** 4
**Domain:** Healthcare System
**Type:** Rate
**Unit:** Percent of population under age 65
**Description:** The percentage of the non-elderly population without any form of health insurance (public or private) at the time of survey. Includes those eligible but not enrolled in public programs.
**Baseline:** 10.3% (2019, pre-COVID). Range: 2.5% (MA) to 18.4% (TX). Source: ACS 2019.
**Data Source:** American Community Survey (ACS), annual. State and county levels.

**Why this is a valid node:**
- Observable state (insured/uninsured)
- Measurable with existing data
- Descriptive (not "enroll people in insurance")
- Influenced by policy (Medicaid expansion) but not itself a policy

---

### Example 2: Edge Case - Policy as Node

**Node Name:** Medicaid Expansion Status
**Scale:** 1
**Domain:** Healthcare System
**Type:** Policy
**Unit:** Binary (0=not expanded, 1=expanded)
**Description:** Whether a state has adopted the Affordable Care Act Medicaid expansion to cover adults up to 138% FPL. Coded as 1 if expansion is implemented, 0 otherwise.
**Baseline:** 39 states + DC expanded as of 2023. Source: KFF.
**Data Source:** Kaiser Family Foundation Medicaid expansion tracker.

**Why this is a valid node even though it's a policy:**
- It's a **state variable** describing a policy regime, not an action
- Observable and measurable (binary state)
- Influences downstream nodes (uninsured rate, access, utilization)
- Changes rarely (legislative events)

**Contrast with invalid "intervention":**
- ❌ "Implementing Medicaid expansion" = action/intervention
- ✅ "Medicaid expansion status" = state/node

---

### Example 3: Edge Case - Service Availability

**Node Name:** Federally Qualified Health Center Density
**Scale:** 3
**Domain:** Healthcare System
**Type:** Access/Availability
**Unit:** FQHCs per 100,000 population
**Description:** The number of Federally Qualified Health Center (FQHC) service delivery sites per 100,000 population in a county. Includes FQHC look-alikes. Does not include individual provider counts.
**Baseline:** 3.2 per 100,000 nationally (2022). Range: 0 (many rural counties) to 15+ (some urban counties). Source: HRSA UDS.
**Data Source:** HRSA Uniform Data System (UDS), annual reporting. County-level via geocoding.

**Why this is a valid node:**
- Observable infrastructure (count of facilities)
- Result of policy/funding but not itself a policy
- Influences individual access (mechanism)

**Contrast with invalid intervention:**
- ❌ "Opening new FQHCs" = intervention
- ✅ "FQHC density" = node affected by the intervention

---

### Example 4: Edge Case - Intermediate Pathway

**Node Name:** Hypertension Control Rate
**Scale:** 6
**Domain:** Healthcare System (secondary: Chronic Disease)
**Type:** Quality/Intensity
**Unit:** Percent of adults with diagnosed hypertension with BP <140/90 mmHg
**Description:** Among adults with diagnosed hypertension, the percentage who have their blood pressure controlled to <140/90 mmHg based on clinical measurement or self-report. Denominator includes only those aware of diagnosis.
**Baseline:** 43.7% (2017-2020, NHANES). Disparities: lower among Black adults (37.1%) and uninsured (35.2%). Source: CDC.
**Data Source:** National Health and Nutrition Examination Survey (NHANES), biennial. National and by demographics. County-level estimates from CDC PLACES (modeled).

**Why this is intermediate, not a crisis endpoint:**
- It's a **process measure** of disease control, not the disease outcome itself
- Mediates between access/treatment and outcomes (stroke, MI, mortality)
- Partially modifiable by individual behavior but heavily shaped by access and quality of care

**Contrast:**
- Intermediate: "Hypertension control rate"
- Crisis: "Stroke incidence" (the outcome uncontrolled HTN contributes to)

---

### Example 5: Edge Case - Composite Index

**Node Name:** Neighborhood Deprivation Index
**Scale:** 4
**Domain:** Economic Security (secondary: Social Environment)
**Type:** Exposure
**Unit:** Standardized score (mean=0, SD=1), higher = more deprived
**Description:** A composite index of neighborhood socioeconomic disadvantage, constructed from census tract-level measures of median income, poverty rate, unemployment rate, education, housing vacancy, and household structure. Standardized to mean=0, SD=1 at the national level.
**Baseline:** Mean=0 (by construction), SD=1. Range: -2.5 to +4.5. Disparities: Black residents experience mean NDI=+0.8, White residents -0.3. Source: Census ACS-derived.
**Data Source:** Constructed from American Community Survey 5-year estimates at census tract level. Multiple published versions (e.g., Kind et al., Messer et al.). Updated every 5 years.

**Why this is a valid node:**
- Composite, but **construction is specified** and replicable
- Widely used in health research
- Measures a coherent concept (neighborhood disadvantage)
- Observable via census data

**Requirement:** The index construction must be documented (which ACS variables, what weights).

---

### Example 6: Invalid "Node" - Too Vague

**Attempted Node Name:** "Community Resilience"

**Why this is NOT a valid node:**
- ❌ Undefined: What does "resilience" mean operationally?
- ❌ Not measurable: No specified unit or data source
- ❌ Too broad: Conflates multiple distinct constructs

**Correct Formulation (pick one or more specific nodes):**
- ✅ "Community Cohesion Index" (validated scale, e.g., collective efficacy survey)
- ✅ "Social Capital Index" (e.g., Putnam's civic participation measures)
- ✅ "Disaster Recovery Time" (days to restore services after disaster)

---

### Example 7: Invalid "Node" - Actually an Intervention

**Attempted Node Name:** "Community Health Worker Program Implementation"

**Why this is NOT a valid node:**
- ❌ Describes an **action/program**, not a state
- ❌ The "node" is actually the intervention itself

**Correct Formulation:**
- ✅ "Community Health Worker Density" (CHWs per 100,000 population)
- ✅ "CHW Program Reach" (% of target population enrolled)
- ✅ "CHW Workforce Capacity" (FTE CHWs in the county)

**Explanation:** The *program* is an intervention that affects the *density/capacity*, which is the node.

---

### Example 8: Process Measure vs. Outcome

**Question:** Is "ED visits for ambulatory care-sensitive conditions" a node?

**Answer:** Yes, it's a valid **crisis endpoint** node.

**Node Name:** Ambulatory Care-Sensitive Emergency Department Visit Rate
**Scale:** 7
**Domain:** Healthcare System
**Type:** Rate
**Unit:** ED visits for ACSC per 1,000 population per year
**Description:** Emergency department visits for conditions that could have been prevented with timely and effective outpatient care (e.g., uncontrolled diabetes, asthma, hypertension, COPD exacerbation). Based on AHRQ Prevention Quality Indicator (PQI) definitions.
**Baseline:** 58.3 per 1,000 (2019, Medicare). Higher in low-income areas (85.6 per 1,000 in highest poverty quartile). Source: AHRQ.
**Data Source:** Hospital discharge data (HCUP, Medicare claims), annual. State and county levels.

**Why this is a valid crisis node:**
- It's an **outcome** (ED visit occurred) not a process
- Represents a system failure (preventable with better primary care)
- Costly and measurable
- Upstream nodes (access, quality) affect it via mechanisms

---

## Summary Checklist

Before adding a node to the inventory, verify:

- ✅ **Descriptive, not prescriptive:** Describes a state, not an action
- ✅ **Observable:** Can be measured with existing or feasible data
- ✅ **Quantifiable:** Has defined units
- ✅ **Independent:** Exists as a system state, not as an intervention
- ✅ **Scale-appropriate:** Correctly classified as Scale 1 (structural), 3 (institutional), 4 (individual), 6 (intermediate), or 7 (crisis)
- ✅ **Domain-aligned:** Fits within one or more defined domains
- ✅ **Well-defined:** Clear operational definition, no ambiguity
- ✅ **Data-grounded:** Data source identified (even if aspirational)
- ✅ **Baseline-anchored:** US baseline value provided or noted as unavailable

---

## Version History

**Version 1.1 (2025-11-19):**
- **Updated to 1-7 scale system** (from previous 5-scale system)
  - Scale 1: Entirely structural (federal/state policy)
  - Scale 3: Institutional infrastructure
  - Scale 4: Individual/household conditions
  - Scale 6: Intermediate pathways
  - Scale 7: Pure crisis endpoints
  - Scales 2 and 5 reserved for future refinement
- Updated all examples to use numeric scale labels
- Clarified scale definitions with numeric identifiers

**Version 1.0 (2025-11-17):**
- Initial comprehensive framework
- Definitions of nodes, mechanisms, interventions
- 5-scale hierarchy established
- 17 primary domains defined
- Measurement principles codified
- Examples and edge cases documented

---

**End of Document**
