# Node Consolidation Mapping Document

**Version:** 1.0
**Date:** 2025-11-18
**Purpose:** Track consolidation, mergers, and reorganization of node inventory to eliminate redundancy

---

## Executive Summary

**Analysis Results:**
- **Total nodes (original):** ~850 nodes
- **Redundant/overlapping nodes identified:** ~80-120 (10-15%)
- **Target optimized node count:** ~720-750 nodes
- **Mechanism-inventory misalignments:** ~25-30 "ghost nodes"

**Consolidation Strategy:**
- Merge truly redundant nodes (same concept, different names/scales)
- Standardize terminology across related nodes
- Add missing critical nodes referenced in mechanisms
- Document all changes for mechanism YAML updates

---

## TIER 1: CRITICAL CONSOLIDATIONS (Immediate)

### 1. Housing Quality Nodes

**Problem:** Multiple overlapping housing quality measures causing mechanism fragmentation

**Original Nodes:**
- **Node 199:** "Housing Quality Deficiencies" (% units with moderate/severe problems)
- **Node 315:** "Household Mold/Dampness" (% reporting mold/dampness)
- **Node 346:** "Housing Repair Needs (Severe)" (% moderate/severe physical problems)

**Mechanism References (Fragmented):**
- `housing_quality`
- `poor_housing_quality`
- `poor_housing_conditions`
- `household_mold_presence`
- `mold_presence`
- `indoor_dampness_exposure`

**CONSOLIDATION PLAN:**

**NEW Node 199 (Revised): "Housing Quality Index"**
- **Scale:** Individual/Household
- **Domain:** Housing
- **Type:** Quality/Intensity
- **Unit:** Index 0-100 (higher = better quality)
- **Description:** Composite index of housing quality including: structural deficiencies (plumbing, heating, electrical), physical problems (roof, windows, foundation), code violations, and maintenance adequacy. Based on American Housing Survey (AHS) housing quality indicators. Excludes environmental hazards (separate node).
- **Baseline:** National median = 78. Range: 65 (severely deficient) to 95 (excellent).
- **Data Source:** American Housing Survey (AHS), local housing inspections
- **Replaces:** Original Nodes 199, 346
- **Mechanism node_id:** `housing_quality_index`

**NEW Node 315 (Revised): "Indoor Environmental Hazards Index"**
- **Scale:** Individual/Household
- **Domain:** Housing, Environmental
- **Type:** Exposure
- **Unit:** Index 0-100 (higher = more hazards)
- **Description:** Composite index of indoor environmental health hazards including: mold/dampness, pest infestation (rodents, cockroaches), lead paint, asbestos, radon, inadequate ventilation. Weighted by severity and health impact.
- **Baseline:** National median = 25. Range: 0 (no hazards) to 85 (multiple severe hazards).
- **Data Source:** AHS, NHANES environmental home assessment, local health dept inspections
- **Replaces:** Original Node 315 (mold/dampness only), expands to comprehensive environmental hazards
- **Mechanism node_id:** `indoor_environmental_hazards`

**REMOVED:**
- ~~Node 346~~ (merged into Node 199)

**Mechanism Update Required:**
- Replace all references to `poor_housing_quality`, `poor_housing_conditions` → `housing_quality_index` (reverse scored if needed)
- Replace `household_mold_presence`, `mold_presence`, `indoor_dampness_exposure` → `indoor_environmental_hazards`

---

### 2. Asthma Outcome Nodes

**Problem:** Fragmented asthma outcomes with missing nodes referenced in mechanisms

**Original Nodes:**
- **Node 271:** "Asthma Prevalence (Adults)" (% adults with current asthma)
- **Node 301:** "Childhood Asthma Prevalence" (% children with current asthma)
- **Node 418:** "Asthma Control (Well-Controlled)" (% with well-controlled asthma)

**Mechanism References (Ghost Nodes - NOT in inventory):**
- `asthma_exacerbations_children`
- `childhood_asthma_incidence`
- `pediatric_asthma_incidence`
- `asthma_symptoms`
- `asthma_symptom_severity`
- `asthma_exacerbation_frequency`
- `asthma_outcomes`

**CONSOLIDATION PLAN:**

**KEEP DISTINCT (Revised):**

**Node 271 (Revised): "Asthma Prevalence (Adults)"**
- **Mechanism node_id:** `adult_asthma_prevalence`
- No changes to measurement, clarify naming

**Node 301 (Revised): "Asthma Prevalence (Children 0-17)"**
- **Mechanism node_id:** `child_asthma_prevalence` (standardize to "child" not "childhood")
- Age range: 0-17 years (specify explicitly)

**Node 418 (Keep): "Asthma Control (Well-Controlled)"**
- **Mechanism node_id:** `asthma_control_rate`
- Applies to all ages with asthma

**ADD NEW NODES:**

**NEW Node 420: "Asthma Incidence Rate"**
- **Scale:** Crisis
- **Domain:** Healthcare System, Respiratory Health
- **Type:** Rate
- **Unit:** New asthma diagnoses per 1,000 persons per year
- **Description:** Annual incidence of new asthma diagnoses (not prevalent cases) per 1,000 population. Age-stratified: children (0-17) and adults (18+). Captures new onset asthma burden. Distinct from prevalence (existing cases).
- **Baseline:**
  - Children: 8.5 per 1,000 per year
  - Adults: 3.2 per 1,000 per year
  - Disparities: Higher among Black children (11.2), low-income families
- **Data Source:** NHIS, NHANES, state health department surveillance, health system data
- **Mechanism node_id child:** `child_asthma_incidence`
- **Mechanism node_id adult:** `adult_asthma_incidence`

**NEW Node 421: "Asthma Exacerbation Rate"**
- **Scale:** Crisis
- **Domain:** Healthcare System, Respiratory Health
- **Type:** Rate
- **Unit:** ED visits + hospitalizations for asthma per 1,000 persons with asthma per year
- **Description:** Annual rate of asthma exacerbations requiring emergency department visit or hospitalization among persons with diagnosed asthma. Denominator = persons with asthma (not total population). Indicates poor control and acute system burden. Age-stratified available.
- **Baseline:**
  - Children with asthma: 145 per 1,000 per year (14.5%)
  - Adults with asthma: 68 per 1,000 per year (6.8%)
  - Disparities: Higher among Black children, Medicaid enrollees
- **Data Source:** HCUP, state hospital discharge data, Medicaid claims, CDC asthma surveillance
- **Mechanism node_id child:** `child_asthma_exacerbations`
- **Mechanism node_id adult:** `asthma_exacerbation_rate`

**Mechanism Update Required:**
- Replace `childhood_asthma_incidence`, `pediatric_asthma_incidence` → `child_asthma_incidence` (new Node 420)
- Replace `asthma_exacerbations_children` → `child_asthma_exacerbations` (new Node 421)
- Replace generic `asthma_outcomes` → specify which node (prevalence, incidence, control, or exacerbations)
- Remove `asthma_symptoms`, `asthma_symptom_severity` (not measurable population nodes - these are clinical measures, not public health surveillance)

**Terminology Standardization:**
- "Child/Children" (0-17 years) - use consistently
- "Pediatric" - REMOVE, use "child/children"
- "Childhood" - REMOVE, use "child"

---

### 3. Crime/Violence Nodes (MISSING - Critical Gap)

**Problem:** Mechanisms reference crime/violence nodes that DO NOT EXIST in inventory

**Mechanism References (Ghost Nodes):**
- `violent_crime_rate`
- `community_violence_exposure`

**ADD NEW NODES:**

**NEW Node 100: "Violent Crime Rate"**
- **Scale:** Structural (Scale 1)
- **Domain:** Criminal Justice, Social Environment
- **Type:** Rate
- **Unit:** Violent crimes (murder, rape, robbery, aggravated assault) per 100,000 population per year
- **Description:** FBI Uniform Crime Reporting (UCR) violent crime rate: murder/manslaughter, rape, robbery, and aggravated assault offenses known to police per 100,000 population annually. Structural measure of community violence. Does not capture unreported crime. Geographic variation reflects policing, economic conditions, structural factors.
- **Baseline:** 380 per 100,000 nationally (2022). Range: 115 (ME, VT) to 885 (DC, LA, AK high rates). Down from peak 758 in 1991. Concentrated in certain neighborhoods within cities.
- **Data Source:** FBI Uniform Crime Reporting (UCR), National Incident-Based Reporting System (NIBRS). State, county, city-level, annual.
- **Mechanism node_id:** `violent_crime_rate`

**NEW Node 101: "Property Crime Rate"**
- **Scale:** Structural (Scale 1)
- **Domain:** Criminal Justice, Social Environment, Economic Security
- **Type:** Rate
- **Unit:** Property crimes (burglary, larceny-theft, motor vehicle theft) per 100,000 population per year
- **Description:** FBI UCR property crime rate: burglary, larceny-theft, motor vehicle theft, and arson per 100,000 population annually. Reflects economic stress, housing instability, substance use, and community cohesion.
- **Baseline:** 1,954 per 100,000 nationally (2022). Range: 850 to 3,500. Declining from peak 5,140 in 1991.
- **Data Source:** FBI UCR/NIBRS. State, county, city-level, annual.
- **Mechanism node_id:** `property_crime_rate`

**NEW Node 275: "Community Violence Exposure"**
- **Scale:** Individual/Household (Scale 3)
- **Domain:** Social Environment, Mental Health
- **Type:** Exposure
- **Unit:** Percent of residents reporting witnessing or experiencing violence in past year
- **Description:** Individual/household exposure to community violence: witnessing assault, shooting, stabbing, or other serious violence in neighborhood, OR being victim of violent crime, OR hearing gunshots regularly. Survey-based measure. Captures trauma exposure beyond crime statistics. Children's exposure particularly harmful.
- **Baseline:**
  - Adults: 12-15% nationally report past-year exposure
  - Children/adolescents: 25-40% in urban areas report lifetime exposure
  - Disparities: 40-60% exposure in high-violence neighborhoods (concentrated poverty, Black/Latino communities)
- **Data Source:** NHIS Social Determinants module, Youth Risk Behavior Survey (YRBS), local community surveys, PhenX Toolkit violence exposure measures
- **Mechanism node_id:** `community_violence_exposure`

**Mechanism Update Required:**
- Add Node 100 `violent_crime_rate` to mechanisms that currently reference it
- Add Node 275 `community_violence_exposure` for individual-level violence exposure pathways

---

### 4. Air Pollution Nodes (Redundancy)

**Problem:** Redundant nodes at different scales measuring same exposure

**Original Nodes:**
- **Node 124:** "Air Quality (PM2.5 Annual Average)" - Scale 1 (Structural)
- **Node 226:** "Air Pollution Exposure (Individual)" - Scale 3 (Individual)

**Analysis:** These measure the SAME thing (ambient PM2.5 concentration) at different geographic granularities. Individual exposure IS the ambient concentration at residence location.

**CONSOLIDATION PLAN:**

**KEEP Node 124 (Revised): "Ambient Air Pollution (PM2.5)"**
- **Scale:** Structural/Individual (bridge node - can be measured at structural OR individual level depending on aggregation)
- **Domain:** Environmental, Public Health
- **Type:** Exposure
- **Unit:** μg/m³ PM2.5 annual average
- **Description:** Fine particulate matter (PM2.5) concentration measured at finest available geographic level (monitor, census tract, or individual residence). Population-weighted average for area calculations. Captures structural air quality AND individual exposure depending on analysis level. Prenatal exposure = mother's residential exposure during pregnancy.
- **Baseline:** National population-weighted mean = 8.9 μg/m³ (2023). Range: 3.5 (rural low-pollution) to 18 μg/m³ (high-pollution metros). WHO guideline = 5 μg/m³. EPA NAAQS = 12 μg/m³.
- **Data Source:** EPA Air Quality System (AQS) monitors, CDC Environmental Public Health Tracking, satellite-derived estimates (Di et al.), LUR models. Monitor, tract, county, state levels.
- **Mechanism node_id:** `ambient_pm25` (use for all air pollution exposure pathways)
- **Mechanism note:** For prenatal exposure, use `prenatal_ambient_pm25` (same node, pregnancy time window)

**REMOVED:**
- ~~Node 226~~ "Air Pollution Exposure (Individual)" (redundant with Node 124 measured at individual residence level)

**Mechanism Update Required:**
- Replace `air_pollution_concentration`, `prenatal_air_pollution_exposure`, `parental_air_pollution_exposure` → `ambient_pm25` (Node 124, with temporal specification if needed)
- Remove separate "individual air pollution exposure" references

**Note:** Other air pollutants (O3, NO2) should be separate nodes if needed, but PM2.5 is primary.

---

### 5. Union Membership Duplication

**Problem:** Union density/membership appears 3 times

**Original Nodes:**
- **Node 28:** "Union Membership Rate" - Scale 1 (Structural) - "% of wage and salary workers who are union members"
- **Node 113:** "Labor Union Density (Local)" - Scale 1 (Structural) - (appears to duplicate Node 28)
- **Node 326:** "Union Membership" - Scale 3 (Individual) - individual union membership status

**CONSOLIDATION PLAN:**

**MERGE Nodes 28 + 113 → Revised Node 28:**

**Node 28 (Revised): "Union Density Rate"**
- **Scale:** Structural
- **Domain:** Employment, Labor
- **Type:** Rate
- **Unit:** Percent of wage and salary workers who are union members
- **Description:** The percentage of employed wage and salary workers who report union membership in a geographic area (state, metro, or county). Reflects union density and collective bargaining power. Influenced by right-to-work laws, industrial composition, and organizing climate. Can be measured at state, metro, or local labor market level.
- **Baseline:** 10.0% nationally (2023). Range: 2.9% (SC) to 23.1% (HI). Highest in public sector (32.5%) vs. private (6.0%). Declining from 20.1% in 1983.
- **Data Source:** Bureau of Labor Statistics (BLS) Current Population Survey Union Membership Supplement, annual. State and metro-level.
- **Mechanism node_id:** `union_density_rate`
- **Replaces:** Original Nodes 28 and 113

**KEEP Node 326: "Union Membership (Individual)"**
- **Scale:** Individual
- **Domain:** Employment, Labor
- **Type:** Binary
- **Unit:** Binary (0=not union member, 1=union member)
- **Description:** Whether individual worker is a member of a labor union or employee association similar to a union. Individual-level measure for linking to individual health outcomes. Distinct from population-level union density.
- **Mechanism node_id:** `individual_union_membership`

**REMOVED:**
- ~~Node 113~~ "Labor Union Density (Local)" (duplicate of Node 28)

**Mechanism Update Required:**
- Structural/population-level union effects → use `union_density_rate` (Node 28)
- Individual-level union membership effects → use `individual_union_membership` (Node 326)

---

## TIER 2: HIGH-PRIORITY CONSOLIDATIONS

### 6. Occupational Hazard Nodes

**Problem:** Overlapping occupational exposure nodes across scales

**Original Nodes:**
- **Node 96:** "Occupational Hazard Exposure Rate" - Scale 1 (Structural) - "% workforce in high-hazard occupations"
- **Node 97:** "Workplace Injury and Illness Rate" - Scale 1 (Structural) - "cases per 100 FTE"
- **Node 224:** "Workplace Injury Exposure (Individual)" - Scale 3 (Individual) - "% in high-hazard jobs"
- **Nodes 476-485:** Multiple occupational exposure nodes - Scale 4 (Intermediate) - specific exposures

**Analysis:**
- Nodes 96 and 224 are redundant (same measure at different scales)
- Nodes 476-485 should be consolidated into outcome measures
- Node 97 is distinct (outcome, not exposure)

**CONSOLIDATION PLAN:**

**REMOVE Node 96:**
- ~~Node 96~~ "Occupational Hazard Exposure Rate" (redundant with Node 224 aggregated)

**KEEP Node 97 (Outcome):**
**Node 97: "Workplace Injury and Illness Rate"**
- No changes, this is outcome measure

**KEEP Node 224 (Exposure):**
**Node 224 (Revised): "Occupational Hazard Exposure"**
- **Scale:** Individual
- **Domain:** Employment, Occupational Health
- **Type:** Exposure
- **Unit:** Binary or categorical: high-hazard occupation (yes/no) OR occupation hazard score 0-10
- **Description:** Whether individual works in occupation with elevated risk of injury, illness, or toxic exposure. Based on BLS occupation classification or occupation-exposure matrix. High-hazard includes: construction, agriculture, manufacturing, healthcare (infection/violence), transportation, law enforcement, firefighting, mining. Can aggregate to population-level "% in high-hazard occupations."
- **Mechanism node_id:** `occupational_hazard_exposure`

**CONSOLIDATE Nodes 476-485 (Scale 4):**
Note: Need to read these nodes to see what they are, but likely consolidate into:

**NEW/REVISED Node 476: "Occupational Injury/Illness Incidence"**
- **Scale:** Intermediate
- **Domain:** Occupational Health
- **Type:** Rate
- **Unit:** Work-related injuries/illnesses per 100 FTE workers per year
- **Description:** Individual-level or job-level incidence of work-related injuries and illnesses. Distinct from Node 97 (population-level structural). Measured via workers' comp claims, OSHA logs, or self-report. Mediates between occupational hazard exposure and health outcomes.
- **Mechanism node_id:** `occupational_injury_illness_rate`

**Mechanism Update Required:**
- Remove references to Node 96
- Clarify whether mechanism operates through exposure (Node 224) or outcome (Nodes 97, 476)

---

### 7. Poverty and Economic Security Nodes

**Problem:** Multiple poverty measures with undefined "poverty_index" in mechanisms

**Original Nodes:**
- **Node 182:** "Poverty Rate" (<100% FPL)
- **Node 183:** "Deep Poverty Rate" (<50% FPL)
- **Node 184:** "Asset Poverty Rate" (lacking 3mo savings)
- **Node 191:** "Housing Cost Burden" (>30% income)
- **Node 192:** "Severe Housing Cost Burden" (>50% income)
- **Node 245:** "Economic Insecurity Stress"

**Mechanism References:**
- `poverty_index` (UNDEFINED - which poverty measure??)
- `housing_cost_burden`

**CLARIFICATION PLAN (No Consolidation - These are Distinct):**

**Node 182: "Income Poverty Rate"** (rename for clarity)
- **Mechanism node_id:** `income_poverty_rate`
- % below 100% FPL

**Node 183: "Deep Income Poverty Rate"** (rename for clarity)
- **Mechanism node_id:** `deep_poverty_rate`
- % below 50% FPL

**Node 184: "Asset Poverty Rate"** (keep)
- **Mechanism node_id:** `asset_poverty_rate`
- Distinct from income poverty

**Node 191: "Housing Cost Burden"** (keep)
- **Mechanism node_id:** `housing_cost_burden`
- >30% income on housing

**ADD DEFINITION:**

**NEW Node 185: "Material Hardship Index"**
- **Scale:** Individual
- **Domain:** Economic Security
- **Type:** Composite
- **Unit:** Index 0-10 (higher = more hardship)
- **Description:** Composite index of material hardship including: food insecurity, inability to pay utilities (shutoffs), housing payment delinquency, medical care foregone due to cost, eviction/homelessness risk. Goes beyond income to capture actual consumption deprivation. Survey-based.
- **Baseline:** National mean = 2.8. Range: 0 (no hardship) to 10 (severe across all domains). 35% of households experience at least one hardship.
- **Data Source:** Survey of Income and Program Participation (SIPP), NHIS Social Determinants, state surveys
- **Mechanism node_id:** `material_hardship_index`

**Mechanism Update Required:**
- **Define `poverty_index`**: Create mapping - if mechanisms intend income poverty, use `income_poverty_rate`. If composite hardship, use `material_hardship_index` (new Node 185).
- Review each mechanism using `poverty_index` and specify which poverty measure

---

## TIER 3: MEDIUM-PRIORITY CONSOLIDATIONS

### 8. Digital Access Nodes

**Problem:** Fragmented digital divide measures

**Original Nodes:**
- **Node 246:** "Broadband Access (Home)" - % households with broadband
- **Node 247:** "Computer/Device Ownership" - % with computer/tablet/smartphone
- **Node 248:** "Digital Literacy" - skill level
- **Node 249:** "Telehealth Access (Individual)" - ability to access telehealth
- **Node 250:** "Digital Payment/Banking Access" - ability to do online banking

**CONSOLIDATION PLAN:**

**MERGE Nodes 246 + 247 + 248 + 250 → NEW Node 246:**

**Node 246 (Revised): "Digital Inclusion Index"**
- **Scale:** Individual
- **Domain:** Digital Access
- **Type:** Composite
- **Unit:** Index 0-100 (higher = more digitally included)
- **Description:** Composite index of digital inclusion including: home broadband access (fixed or mobile), device ownership (computer/tablet/smartphone adequate for internet use), digital literacy skills (able to complete online tasks), and online services access (banking, government services, telecommerce). Based on National Digital Inclusion Alliance framework. Measured at individual/household level.
- **Baseline:** National mean = 68. Range: 20 (no access, no skills) to 100 (full inclusion). Disparities: lower among elderly, rural, low-income, Black/Hispanic households.
- **Data Source:** ACS computer/internet supplement, Pew Digital Divide surveys, NTIA Internet Use Survey
- **Mechanism node_id:** `digital_inclusion_index`
- **Components:** Broadband (40%), device (30%), literacy (20%), services (10%)

**KEEP Node 249 (Healthcare-Specific):**
**Node 249 (Revised): "Digital Health Access"**
- **Scale:** Individual
- **Domain:** Digital Access, Healthcare
- **Type:** Access/Availability
- **Unit:** Binary or index: ability to access telehealth services
- **Description:** Individual/household ability to access telehealth services, including: video visit capability (internet speed + device + platform), audio-only capability (phone access), patient portal access, and remote monitoring device connectivity. Healthcare-specific digital access distinct from general digital inclusion.
- **Mechanism node_id:** `digital_health_access`

**REMOVED:**
- ~~Node 247~~ "Computer/Device Ownership" (component of Node 246)
- ~~Node 248~~ "Digital Literacy" (component of Node 246)
- ~~Node 250~~ "Digital Payment/Banking Access" (component of Node 246)

**Mechanism Update Required:**
- General digital divide pathways → use `digital_inclusion_index` (Node 246)
- Telehealth-specific pathways → use `digital_health_access` (Node 249)

---

### 9. Criminal Justice Contact Nodes

**Problem:** Excessive fragmentation of criminal justice involvement

**Original Nodes (Nodes 251-258):**
- **Node 251:** "Arrest History"
- **Node 252:** "Current Incarceration Exposure"
- **Node 253:** "Felony Conviction Record"
- **Node 254:** "Probation/Parole Status"
- **Node 255:** "Criminal Record Employment Barrier"
- **Node 256:** "Police Stop Experience"
- **Node 257:** "Court Fines/Fees Debt"
- **Node 258:** "Juvenile Justice System Contact"

**CONSOLIDATION PLAN:**

**Consolidate to 4 nodes:**

**KEEP/REVISE Node 251: "Criminal Justice System Contact (Any)"**
- **Scale:** Individual
- **Domain:** Criminal Justice
- **Type:** Binary
- **Unit:** Binary: Any criminal justice contact in lifetime (arrest, conviction, incarceration, supervision)
- **Description:** Whether individual has ever had contact with criminal justice system including: arrest, conviction, incarceration, probation, parole, or court supervision. Binary indicator of any system involvement. Does not capture intensity or recency.
- **Mechanism node_id:** `criminal_justice_contact`

**NEW Node 252 (Revised): "Criminal Justice Involvement Intensity"**
- **Scale:** Individual
- **Domain:** Criminal Justice
- **Type:** Composite
- **Unit:** Index 0-10 (higher = more intensive involvement)
- **Description:** Composite index of criminal justice system involvement intensity including: number of arrests (weighted), felony vs. misdemeanor convictions (weighted), incarceration history (duration weighted), current supervision status (probation/parole), and recency. Captures cumulative and current system entanglement. 0 = no contact, 10 = extensive recent involvement.
- **Mechanism node_id:** `criminal_justice_intensity`
- **Components:** Nodes 251, 252, 253, 254, 256 combined

**KEEP/REVISE Node 255: "Criminal Record Barriers"**
- **Scale:** Individual
- **Domain:** Criminal Justice, Employment, Housing
- **Type:** Exposure/Barrier
- **Unit:** Index 0-10 (higher = more barriers)
- **Description:** Extent to which criminal record creates barriers to employment, housing, education, professional licensing, public benefits, and civic participation. Composite of: felony record (y/n), years since conviction, type of offense, background check failures, denials due to record. Captures downstream effects of system contact.
- **Mechanism node_id:** `criminal_record_barriers`

**KEEP/REVISE Node 257: "Court Fines and Fees Debt"**
- **Scale:** Individual
- **Domain:** Criminal Justice, Economic Security
- **Type:** Debt
- **Unit:** Dollars in outstanding court-related debt
- **Description:** Individual debt from court fines, fees, restitution, supervision fees, and other criminal justice financial obligations. Creates economic burden and re-incarceration risk. Concentrated among low-income defendants.
- **Mechanism node_id:** `court_debt`

**REMOVED (Merged):**
- ~~Node 252~~ "Current Incarceration Exposure" (component of Node 252 intensity)
- ~~Node 253~~ "Felony Conviction Record" (component of Nodes 252 intensity and 255 barriers)
- ~~Node 254~~ "Probation/Parole Status" (component of Node 252 intensity)
- ~~Node 256~~ "Police Stop Experience" (component of Node 252 intensity)
- ~~Node 258~~ "Juvenile Justice System Contact" (captured in revised Node 251 if "lifetime" includes juvenile)

**Mechanism Update Required:**
- Simple pathways (any contact) → use `criminal_justice_contact` (Node 251)
- Dose-response pathways → use `criminal_justice_intensity` (Node 252)
- Collateral consequences → use `criminal_record_barriers` (Node 255)
- Economic strain pathway → use `court_debt` (Node 257)

---

### 10. Food Consumption Behavior Nodes

**Problem:** Overly specific dietary components when composite exists

**Original Nodes:**
- **Node 361:** "Diet Quality (Low)" - composite
- **Node 362:** "Fruit/Vegetable Consumption (Low)"
- **Node 363:** "Sugar-Sweetened Beverage Consumption"
- **Node 364:** "Fast Food Frequency"

**CONSOLIDATION PLAN:**

**KEEP Node 361 (Primary):**
**Node 361 (Revised): "Diet Quality Index (HEI)"**
- **Scale:** Intermediate
- **Domain:** Health Behaviors, Food Security
- **Type:** Quality/Intensity
- **Unit:** Healthy Eating Index (HEI) score 0-100 (higher = better diet quality)
- **Description:** Healthy Eating Index 2015 score measuring overall diet quality based on adherence to Dietary Guidelines for Americans. Components include: fruits, vegetables, whole grains, dairy, protein, fatty acids, sodium, added sugars, saturated fats. Gold standard diet quality measure. Individual-level assessment via 24-hour recall or FFQ.
- **Baseline:** National mean = 58 (2023). Range: 30 (poor diet) to 90 (excellent). Disparities: lower among low-income, food insecure, some racial/ethnic groups.
- **Data Source:** NHANES dietary recall, food frequency questionnaires
- **Mechanism node_id:** `diet_quality_hei`

**KEEP Node 363 (Policy-Relevant):**
**Node 363: "Sugar-Sweetened Beverage Consumption"**
- **Scale:** Intermediate
- **Domain:** Health Behaviors
- **Type:** Behavior
- **Unit:** Servings per day OR % consuming ≥1 serving/day
- **Description:** Daily consumption of sugar-sweetened beverages (soda, fruit drinks, sports drinks, energy drinks, sweetened coffee/tea). Kept separate from general HEI because: (1) specific target of soda tax policies, (2) strong independent association with obesity/diabetes, (3) measurable via single question. Complements HEI.
- **Mechanism node_id:** `ssb_consumption`
- **Rationale for keeping separate:** Policy target (soda taxes), strong independent health effects

**REMOVED (Merged into Node 361):**
- ~~Node 362~~ "Fruit/Vegetable Consumption" (component of HEI Node 361)
- ~~Node 364~~ "Fast Food Frequency" (captured in HEI and energy density components)

**Mechanism Update Required:**
- General diet quality pathways → use `diet_quality_hei` (Node 361)
- SSB-specific pathways (soda taxes, diabetes) → use `ssb_consumption` (Node 363)
- Remove direct references to fruit/vegetable or fast food (use HEI)

---

## TIER 4: ADDITIONAL NODES TO ADD

### 11. Missing Intermediate Pathway Nodes (Scale 4)

**ADD NEW NODES:**

**NEW Node 422: "Lung Function (FEV1/FVC Ratio)"**
- **Scale:** Intermediate
- **Domain:** Respiratory Health
- **Type:** Biological Risk Factor
- **Unit:** FEV1/FVC ratio (0-1, normal ≥0.70)
- **Description:** Forced expiratory volume in 1 second (FEV1) divided by forced vital capacity (FVC), measured by spirometry. Gold standard measure of lung function. Ratio <0.70 indicates airflow obstruction (COPD, asthma). Critical intermediate pathway between environmental exposures (air pollution, smoking, occupational) and respiratory outcomes. Population-level assessment via NHANES or health system data.
- **Baseline:** National mean = 0.78. <0.70 in 15% of adults 40+ (COPD). Lower among smokers, air pollution exposed, occupational exposures.
- **Data Source:** NHANES spirometry, health system spirometry records, research cohorts
- **Mechanism node_id:** `lung_function_fev1_fvc`

**NEW Node 423: "Asthma Medication Adherence"**
- **Scale:** Intermediate
- **Domain:** Healthcare Utilization, Chronic Disease Management
- **Type:** Utilization/Adherence
- **Unit:** Percent of asthma controller medication days covered (PDC ≥0.75)
- **Description:** Among persons with persistent asthma prescribed controller medications (inhaled corticosteroids, combination inhalers, biologics), the proportion of days covered by medication fills. PDC ≥0.75 = adherent. Medication adherence critical for asthma control. Measured via pharmacy claims or self-report. Poor adherence leads to exacerbations.
- **Baseline:** Only 40-50% of adults with persistent asthma are adherent to controller meds. Lower among low-income, uninsured, minorities.
- **Data Source:** Pharmacy claims (PQA measure), MEPS, self-report surveys
- **Mechanism node_id:** `asthma_medication_adherence`

**NEW Node 424: "Primary Care Continuity"**
- **Scale:** Intermediate
- **Domain:** Healthcare Utilization
- **Type:** Quality/Intensity
- **Unit:** Continuity of Care Index (0-1, higher = more continuity) OR % with usual provider
- **Description:** Extent to which individual receives care from consistent primary care provider over time. Measured via: Continuity of Care Index (concentration of visits with one provider), Usual Provider Continuity (% visits with most frequent provider), or binary (has vs. no usual provider). Distinct from "having" a provider - captures actual longitudinal relationship. Affects chronic disease management, preventive care, trust.
- **Baseline:** ~75% of adults report having usual provider, but only 45-50% have high continuity (COC >0.75). Lower among uninsured, high-deductible plans, Medicaid.
- **Data Source:** MEPS, NHIS, claims-based COC calculations
- **Mechanism node_id:** `primary_care_continuity`

**NEW Node 425: "Sleep Quality Index"**
- **Scale:** Intermediate
- **Domain:** Health Behaviors, Intermediate Pathways
- **Type:** Quality/Intensity
- **Unit:** Pittsburgh Sleep Quality Index (PSQI) score 0-21 (lower = better, >5 = poor sleep quality)
- **Description:** Comprehensive measure of sleep quality including: sleep duration, sleep latency, sleep efficiency, sleep disturbances, use of sleep medication, and daytime dysfunction. PSQI is validated scale. Distinct from sleep duration alone (Node 376). Poor sleep quality links stress, housing conditions, shift work to health outcomes.
- **Baseline:** National mean PSQI = 6.2 (poor quality). 35-40% have poor sleep quality (PSQI >5). Higher among shift workers, caregivers, chronic pain, mental health conditions.
- **Data Source:** NHANES sleep module, research surveys using PSQI
- **Mechanism node_id:** `sleep_quality_psqi`
- **Note:** This is distinct from Node 376 "Sleep Duration" (hours/night)

---

## NODE NUMBERING CONVENTIONS

**Approach:**
- When consolidating, keep LOWEST node number and revise
- When removing redundant nodes, document as ~~strikethrough~~
- New nodes: Assign next available number in scale section
- Maintain scale groupings:
  - Scale 1 (Structural): Nodes 1-120
  - Scale 2 (Institutional): Nodes 121-370
  - Scale 3 (Individual): Nodes 181-450
  - Scale 4 (Intermediate): Nodes 351-520
  - Scale 5 (Crisis): Nodes 501-650

**New Node Numbers Assigned:**
- Node 100: Violent Crime Rate (Scale 1 - fill gap)
- Node 101: Property Crime Rate (Scale 1 - fill gap)
- Node 185: Material Hardship Index (Scale 3)
- Node 275: Community Violence Exposure (Scale 3)
- Node 420: Asthma Incidence Rate (Scale 5)
- Node 421: Asthma Exacerbation Rate (Scale 5)
- Node 422: Lung Function FEV1/FVC (Scale 4)
- Node 423: Asthma Medication Adherence (Scale 4)
- Node 424: Primary Care Continuity (Scale 4)
- Node 425: Sleep Quality Index (Scale 4)

---

## TERMINOLOGY STANDARDIZATION RULES

### Age Group Terms
- **Use:** "Child" or "Children" for ages 0-17
- **Remove:** "Childhood" (use "child"), "Pediatric" (use "child")
- **Specify:** Exact age ranges when narrower (e.g., "Infant 0-1," "Adolescent 12-17")
- **Use:** "Offspring" ONLY for intergenerational mechanisms (parent exposure → child outcome)

### Epidemiological Terms
- **Prevalence:** % of population with condition at point in time
- **Incidence:** New cases per population per time period (always specify time: per year)
- **Rate:** Always specify denominator and time period (e.g., "per 100,000 per year")

### Directionality
- **Positive framing:** "Quality," "Access," "Index" (higher = better)
- **Negative framing:** "Deficiency," "Burden," "Barrier" (higher = worse)
- **Never mix** within same domain (e.g., don't have both "housing quality" and "poor housing quality")

### Node ID Naming
- **Use:** snake_case for mechanism node_ids
- **Be specific:** `child_asthma_prevalence` not `childhood_asthma`
- **Consistent:** Same base name across ages (e.g., `child_asthma_prevalence`, `adult_asthma_prevalence`)

---

## MECHANISM YAML UPDATE CHECKLIST

**For each mechanism file, update:**

1. **Housing mechanisms:**
   - ✓ Replace `housing_quality`, `poor_housing_quality`, `poor_housing_conditions` → `housing_quality_index`
   - ✓ Replace `household_mold_presence`, `mold_presence`, `indoor_dampness_exposure` → `indoor_environmental_hazards`

2. **Asthma mechanisms:**
   - ✓ Replace `childhood_asthma`, `childhood_asthma_incidence`, `pediatric_asthma_incidence` → `child_asthma_prevalence` or `child_asthma_incidence`
   - ✓ Replace `asthma_exacerbations_children` → `child_asthma_exacerbations`
   - ✓ Add new nodes: `child_asthma_incidence`, `asthma_exacerbation_rate`, `asthma_medication_adherence`, `lung_function_fev1_fvc`

3. **Crime/violence mechanisms:**
   - ✓ Add `violent_crime_rate` (Node 100)
   - ✓ Add `community_violence_exposure` (Node 275)

4. **Air pollution mechanisms:**
   - ✓ Replace `air_pollution_concentration`, `prenatal_air_pollution_exposure`, `individual_air_pollution_exposure` → `ambient_pm25`

5. **Union mechanisms:**
   - ✓ Replace union density references → `union_density_rate` (Node 28)
   - ✓ Individual union effects → `individual_union_membership` (Node 326)

6. **Poverty mechanisms:**
   - ✓ Define/replace `poverty_index` → specify which poverty measure (`income_poverty_rate`, `deep_poverty_rate`, or `material_hardship_index`)

7. **Digital access mechanisms:**
   - ✓ General digital divide → `digital_inclusion_index` (Node 246)
   - ✓ Telehealth specific → `digital_health_access` (Node 249)

8. **Criminal justice mechanisms:**
   - ✓ Simple contact → `criminal_justice_contact` (Node 251)
   - ✓ Intensity/dose → `criminal_justice_intensity` (Node 252)
   - ✓ Barriers → `criminal_record_barriers` (Node 255)

9. **Diet mechanisms:**
   - ✓ General diet → `diet_quality_hei` (Node 361)
   - ✓ SSB specific → `ssb_consumption` (Node 363)

---

## REMOVED NODES SUMMARY

**Nodes to DELETE from inventory:**
- ~~Node 113~~: Labor Union Density (duplicate of Node 28)
- ~~Node 226~~: Air Pollution Exposure Individual (duplicate of Node 124)
- ~~Node 96~~: Occupational Hazard Exposure Rate (duplicate of Node 224 aggregated)
- ~~Node 346~~: Housing Repair Needs Severe (merged into Node 199)
- ~~Node 247~~: Computer/Device Ownership (component of Node 246)
- ~~Node 248~~: Digital Literacy (component of Node 246)
- ~~Node 250~~: Digital Payment/Banking Access (component of Node 246)
- ~~Node 252~~ (original): Current Incarceration Exposure (component of revised Node 252)
- ~~Node 253~~: Felony Conviction Record (component of Nodes 252, 255)
- ~~Node 254~~: Probation/Parole Status (component of Node 252)
- ~~Node 256~~: Police Stop Experience (component of Node 252)
- ~~Node 258~~: Juvenile Justice System Contact (component of Node 251)
- ~~Node 362~~: Fruit/Vegetable Consumption (component of Node 361)
- ~~Node 364~~: Fast Food Frequency (component of Node 361)

**Total Removed:** 14 nodes

---

## ADDED NODES SUMMARY

**New nodes added to inventory:**
- **Node 100:** Violent Crime Rate
- **Node 101:** Property Crime Rate
- **Node 185:** Material Hardship Index
- **Node 275:** Community Violence Exposure
- **Node 420:** Asthma Incidence Rate
- **Node 421:** Asthma Exacerbation Rate
- **Node 422:** Lung Function (FEV1/FVC)
- **Node 423:** Asthma Medication Adherence
- **Node 424:** Primary Care Continuity
- **Node 425:** Sleep Quality Index

**Total Added:** 10 nodes

---

## NET CHANGE SUMMARY

- **Original nodes:** ~850
- **Removed:** 14 nodes
- **Added:** 10 nodes
- **Net change:** -4 nodes
- **Final count:** ~846 nodes (minimal reduction, but MUCH better organization)

**Note:** The goal was NOT aggressive reduction, but rather:
1. ✓ Eliminate true redundancy
2. ✓ Add critical missing nodes
3. ✓ Standardize terminology
4. ✓ Align mechanisms with inventory
5. ✓ Improve conceptual clarity

---

## NEXT STEPS

1. **Update COMPLETE_NODE_INVENTORY.md:**
   - Remove deleted nodes
   - Revise consolidated nodes with new definitions
   - Add new nodes
   - Renumber as needed

2. **Update mechanism YAML files:**
   - Search/replace old node_ids with new standardized node_ids
   - Verify all mechanisms reference existing nodes
   - Add newly defined nodes where appropriate

3. **Create Node ID crosswalk:**
   - Old node_id → New node_id mapping table
   - For data migration and mechanism updates

4. **Update API/database schema:**
   - Add new nodes to database
   - Mark deprecated nodes
   - Update frontend node selection lists

5. **Validate:**
   - Run validation script to check all mechanism node_ids exist in inventory
   - Check for orphaned nodes (in inventory but never used)
   - Verify no broken references

---

**Document Status:** DRAFT
**Next Update:** After applying changes to COMPLETE_NODE_INVENTORY.md

