# Comprehensive Health System Node Bank
**From Structural Determinants to Crisis Endpoints**

## Document Purpose

This is the **complete, non-redundant taxonomy** of nodes in the HealthSystems Platform, organized by scale and flow position. Each node represents a measurable stock in the health system.

**Total Nodes:** 156 (non-redundant core set)
**Organization:** By scale (structural → institutional → individual → intermediates → crisis endpoints)
**Coverage:** All major pathways from policy to health outcomes

---

## Node Bank Architecture

### Hierarchy

```
SCALE 1: STRUCTURAL (Policy/Systems)
    ↓ affects
SCALE 2: INSTITUTIONAL (Local Implementation)
    ↓ affects
SCALE 3: INDIVIDUAL/HOUSEHOLD (Lived Experience)
    ↓ flows through
INTERMEDIATE STOCKS (Proxy Indices/Pathways)
    ↓ determines
CRISIS ENDPOINTS (Health Outcomes)
```

### Node Types by Stock Category

**Type 1: Real Stocks** - Direct measurement, natural units
- Capacity (infrastructure, workforce)
- Flow rates (events per time)
- Prevalence (proportions)
- Physical conditions (environmental)

**Type 2: Proxy Index Stocks** - Constructed indices (0-1 or 0-10 scale)
- Composite measures
- Multi-component indices
- Calibrated constructs

**Type 3: Crisis Endpoints** - Monetized health outcomes
- Acute care utilization
- Morbidity and mortality
- Justice involvement
- Homelessness

---

## SCALE 1: STRUCTURAL (Federal/State Policy)

**Time Horizon:** 2-10 years
**Measurement:** Policy indices, statutory measures, system-level metrics
**Count:** 35 nodes

### Category: Healthcare System Policy

#### S1.01 **medicaid_expansion_status**
- **Type:** Binary (0=not expanded, 1=expanded)
- **Unit:** 0-1
- **Description:** Whether state has expanded Medicaid under ACA
- **Baseline (US avg):** 0.68 (as of 2024)
- **Data Source:** KFF State Health Facts

#### S1.02 **medicaid_work_requirements**
- **Type:** Binary (0=absent, 1=present)
- **Unit:** 0-1
- **Description:** Whether state imposes work requirements for Medicaid
- **Baseline (US avg):** 0.12
- **Data Source:** KFF, state Medicaid agencies

#### S1.03 **medicaid_coverage_generosity**
- **Type:** Proxy index
- **Unit:** 0-10 scale
- **Components:**
  - Expansion status (0-3 points)
  - Work requirements absent (0-2 points)
  - Scope of coverage (0-3 points)
  - Reimbursement adequacy (0-2 points)
- **Baseline (US avg):** 5.8
- **Data Source:** Constructed from KFF, state regulations

#### S1.04 **healthcare_single_payer_coverage**
- **Type:** Proportion
- **Unit:** 0-1 (% population in public plans)
- **Description:** Extent of single-payer vs. private insurance
- **Baseline (US avg):** 0.37 (Medicare + Medicaid)
- **Data Source:** Census ACS

#### S1.05 **prescription_drug_price_regulation**
- **Type:** Policy strength index
- **Unit:** 0-10 scale
- **Components:**
  - Price negotiation authority
  - Import allowances
  - Rebate requirements
- **Baseline (US avg):** 3.2
- **Data Source:** State pharmaceutical policy databases

### Category: Housing Policy

#### S1.06 **just_cause_eviction_law**
- **Type:** Binary (0=no, 1=yes)
- **Unit:** 0-1
- **Description:** State/local just-cause eviction requirements
- **Baseline (US avg):** 0.08
- **Data Source:** Eviction Lab, National Housing Law Project

#### S1.07 **eviction_notice_period_days**
- **Type:** Real (days)
- **Unit:** Days
- **Description:** Minimum notice period before eviction filing
- **Baseline (US avg):** 14 days
- **Data Source:** State landlord-tenant law compendiums

#### S1.08 **rent_control_coverage**
- **Type:** Proportion
- **Unit:** 0-1 (% housing units covered)
- **Description:** Extent of rent stabilization policies
- **Baseline (US avg):** 0.09
- **Data Source:** Local housing authorities, NMHC

#### S1.09 **eviction_protection_strength**
- **Type:** Proxy index
- **Unit:** 0-10 scale
- **Components:**
  - Just-cause required (0-3 points)
  - Notice period adequacy (0-2 points)
  - Legal representation access (0-3 points)
  - Rent control coverage (0-2 points)
- **Baseline (US avg):** 3.5
- **Data Source:** Constructed from housing policy data

#### S1.10 **public_housing_funding_per_capita**
- **Type:** Real (dollars)
- **Unit:** $/capita/year
- **Description:** Public and subsidized housing investment
- **Baseline (US avg):** $142/capita/year
- **Data Source:** HUD budget data, Census population

#### S1.11 **housing_voucher_coverage**
- **Type:** Proportion
- **Unit:** 0-1 (% eligible receiving)
- **Description:** Section 8 voucher availability vs. need
- **Baseline (US avg):** 0.24
- **Data Source:** HUD, Center on Budget and Policy Priorities

### Category: Labor Policy

#### S1.12 **minimum_wage_dollars**
- **Type:** Real (dollars)
- **Unit:** $/hour
- **Description:** State/local minimum wage
- **Baseline (US avg):** $10.50/hour (weighted by state population)
- **Data Source:** Department of Labor

#### S1.13 **minimum_wage_ratio_median**
- **Type:** Ratio
- **Unit:** 0-1 ratio
- **Description:** Minimum wage as proportion of median wage
- **Baseline (US avg):** 0.42
- **Data Source:** DOL, BLS OES

#### S1.14 **paid_sick_leave_mandate**
- **Type:** Binary (0=no, 1=yes)
- **Unit:** 0-1
- **Description:** Mandatory paid sick leave policy
- **Baseline (US avg):** 0.16
- **Data Source:** A Better Balance, NCSL

#### S1.15 **paid_family_leave_weeks**
- **Type:** Real (weeks)
- **Unit:** Weeks
- **Description:** Statutory paid family leave duration
- **Baseline (US avg):** 1.8 weeks (weighted, most states = 0)
- **Data Source:** NCSL, state labor departments

#### S1.16 **unionization_protection_strength**
- **Type:** Policy index
- **Unit:** 0-10 scale
- **Description:** Right-to-work status, collective bargaining protections
- **Baseline (US avg):** 4.5
- **Data Source:** NLRB, state labor law

#### S1.17 **workers_compensation_generosity**
- **Type:** Index
- **Unit:** 0-10 scale
- **Components:**
  - Benefit adequacy
  - Coverage scope
  - Accessibility
- **Baseline (US avg):** 5.5
- **Data Source:** Workers Compensation Research Institute

### Category: Criminal Justice Policy

#### S1.18 **incarceration_rate_per_100k**
- **Type:** Real (rate)
- **Unit:** Per 100,000 population
- **Description:** State incarceration rate
- **Baseline (US avg):** 419/100k
- **Data Source:** Bureau of Justice Statistics

#### S1.19 **mandatory_minimum_sentencing**
- **Type:** Proportion of offenses
- **Unit:** 0-1 (% offenses with mandatory minimums)
- **Description:** Extent of mandatory sentencing laws
- **Baseline (US avg):** 0.28
- **Data Source:** Sentencing Project, state criminal codes

#### S1.20 **three_strikes_law**
- **Type:** Binary (0=no, 1=yes)
- **Unit:** 0-1
- **Description:** Presence of habitual offender enhancement laws
- **Baseline (US avg):** 0.50
- **Data Source:** NCSL, Sentencing Project

#### S1.21 **cash_bail_reform_score**
- **Type:** Policy index
- **Unit:** 0-10 scale
- **Components:**
  - Pretrial release defaults
  - Bail amount restrictions
  - Risk assessment use
- **Baseline (US avg):** 3.8
- **Data Source:** Pretrial Justice Institute

#### S1.22 **criminal_justice_approach**
- **Type:** Proxy index (inverse of punitiveness)
- **Unit:** 0-10 scale (higher = reform-oriented)
- **Components:**
  - Incarceration rate (inverse, 35%)
  - Diversion programs (30%)
  - Community supervision (20%)
  - Bail reform (15%)
- **Baseline (US avg):** 4.2
- **Data Source:** Constructed from DOJ, Sentencing Project

#### S1.23 **drug_decriminalization_scope**
- **Type:** Index
- **Unit:** 0-10 scale
- **Description:** Extent of drug decriminalization (possession, use)
- **Baseline (US avg):** 2.1
- **Data Source:** Drug Policy Alliance, state statutes

### Category: Education & Child Welfare Policy

#### S1.24 **early_childhood_education_access**
- **Type:** Proportion
- **Unit:** 0-1 (% 3-4 year olds enrolled)
- **Description:** Universal pre-K availability
- **Baseline (US avg):** 0.34
- **Data Source:** NIEER State of Preschool

#### S1.25 **snap_eligibility_threshold**
- **Type:** Proportion of FPL
- **Unit:** % Federal Poverty Level
- **Description:** Income eligibility threshold for SNAP (food assistance)
- **Baseline (US avg):** 1.30 (130% FPL)
- **Data Source:** USDA FNS

#### S1.26 **tanf_benefit_adequacy**
- **Type:** Ratio
- **Unit:** 0-1 (TANF max / FPL)
- **Description:** Temporary Assistance benefit as % of poverty line
- **Baseline (US avg):** 0.27
- **Data Source:** Center on Budget and Policy Priorities

#### S1.27 **child_tax_credit_generosity**
- **Type:** Dollars per child
- **Unit:** $/child/year
- **Description:** State + federal child tax credit value
- **Baseline (US avg):** $2,000/child (federal only, as of 2024)
- **Data Source:** IRS, state tax codes

### Category: Environmental Policy

#### S1.28 **clean_air_standards_stringency**
- **Type:** Index
- **Unit:** 0-10 scale
- **Description:** State air quality standards beyond federal EPA minimums
- **Baseline (US avg):** 5.0 (federal baseline)
- **Data Source:** EPA state implementation plans

#### S1.29 **lead_abatement_funding_per_capita**
- **Type:** Real (dollars)
- **Unit:** $/capita/year
- **Description:** State investment in lead paint remediation
- **Baseline (US avg):** $2.80/capita/year
- **Data Source:** HUD lead hazard control grants

#### S1.30 **environmental_justice_policy**
- **Type:** Index
- **Unit:** 0-10 scale
- **Components:**
  - Environmental review requirements
  - Community representation
  - Cumulative impact assessment
- **Baseline (US avg):** 3.5
- **Data Source:** State environmental justice laws

### Category: Infrastructure Investment

#### S1.31 **public_transit_funding_per_capita**
- **Type:** Real (dollars)
- **Unit:** $/capita/year
- **Description:** State + local transit operating + capital funding
- **Baseline (US avg):** $185/capita/year
- **Data Source:** FTA National Transit Database

#### S1.32 **parks_investment_per_capita**
- **Type:** Real (dollars)
- **Unit:** $/capita/year
- **Description:** Municipal parks and recreation funding
- **Baseline (US avg):** $92/capita/year
- **Data Source:** Trust for Public Land, municipal budgets

#### S1.33 **affordable_housing_bond_capacity**
- **Type:** Real (dollars)
- **Unit:** $ millions authorized
- **Description:** State housing bond authority
- **Baseline (US avg):** Varies widely by state
- **Data Source:** State housing finance agencies

### Category: Taxation & Fiscal Policy

#### S1.34 **state_income_tax_progressivity**
- **Type:** Index
- **Unit:** 0-10 scale
- **Description:** How progressive is state income tax structure
- **Baseline (US avg):** 4.2
- **Data Source:** ITEP tax inequality index

#### S1.35 **social_safety_net_funding_per_capita**
- **Type:** Real (dollars)
- **Unit:** $/capita/year
- **Description:** Combined state spending on TANF, SNAP, housing assistance
- **Baseline (US avg):** $420/capita/year
- **Data Source:** State budgets, federal transfers

---

## SCALE 2: INSTITUTIONAL (Local Implementation)

**Time Horizon:** 1-5 years
**Measurement:** Organizational metrics, service density, implementation quality
**Count:** 42 nodes

### Category: Healthcare Delivery System

#### S2.01 **pcp_density**
- **Type:** Real (rate)
- **Unit:** PCPs per 100,000 population
- **Description:** Primary care physician density
- **Baseline (US avg):** 75/100k
- **Data Source:** HRSA Area Health Resources File

#### S2.02 **federally_qualified_health_centers_density**
- **Type:** Real (rate)
- **Unit:** FQHCs per 100,000 population
- **Description:** Community health center access points
- **Baseline (US avg):** 1.8/100k
- **Data Source:** HRSA Health Center Program

#### S2.03 **mental_health_provider_density**
- **Type:** Real (rate)
- **Unit:** Mental health providers per 100,000 population
- **Description:** Psychiatrists, psychologists, LCSWs
- **Baseline (US avg):** 28/100k
- **Data Source:** HRSA, SAMHSA

#### S2.04 **substance_use_treatment_capacity**
- **Type:** Real (rate)
- **Unit:** Treatment slots per 100,000 population
- **Description:** Residential + outpatient SUD treatment capacity
- **Baseline (US avg):** 180/100k
- **Data Source:** SAMHSA NSSATS

#### S2.05 **community_health_worker_density**
- **Type:** Real (rate)
- **Unit:** CHW FTEs per 100,000 population
- **Description:** Community health worker workforce
- **Baseline (US avg):** 8.5/100k (highly variable)
- **Data Source:** BLS, state CHW associations

#### S2.06 **hospital_bed_density**
- **Type:** Real (rate)
- **Unit:** Licensed beds per 100,000 population
- **Description:** Acute care hospital capacity
- **Baseline (US avg):** 260/100k
- **Data Source:** AHA Annual Survey

#### S2.07 **emergency_department_density**
- **Type:** Real (rate)
- **Unit:** EDs per 100,000 population
- **Description:** Emergency department access points
- **Baseline (US avg):** 8.2/100k
- **Data Source:** AHA Annual Survey

#### S2.08 **healthcare_system_integration**
- **Type:** Proxy index
- **Unit:** 0-1 scale
- **Components:**
  - EHR interoperability (40%)
  - Care coordination programs (35%)
  - Referral completion rate (25%)
- **Baseline (US avg):** 0.52
- **Data Source:** Constructed from AHA IT survey, AHRQ

#### S2.09 **patient_centered_medical_home_penetration**
- **Type:** Proportion
- **Unit:** 0-1 (% PCPs in PCMH model)
- **Description:** PCMH recognition/transformation
- **Baseline (US avg):** 0.41
- **Data Source:** NCQA PCMH recognition data

#### S2.10 **accountable_care_organization_coverage**
- **Type:** Proportion
- **Unit:** 0-1 (% population in ACO)
- **Description:** Population covered by ACO arrangements
- **Baseline (US avg):** 0.36
- **Data Source:** CMS ACO data, commercial payer reports

### Category: Housing Infrastructure

#### S2.11 **affordable_housing_units_per_capita**
- **Type:** Real (rate)
- **Unit:** Units per 1,000 population
- **Description:** Income-restricted affordable housing stock
- **Baseline (US avg):** 28/1k
- **Data Source:** HUD, National Housing Preservation Database

#### S2.12 **permanent_supportive_housing_units**
- **Type:** Real (count)
- **Unit:** Units
- **Description:** PSH for chronically homeless population
- **Baseline (US avg):** Varies by metro area
- **Data Source:** HUD Continuum of Care HMIS

#### S2.13 **housing_code_enforcement_capacity**
- **Type:** Real (rate)
- **Unit:** Inspectors per 10,000 housing units
- **Description:** Municipal housing inspection staffing
- **Baseline (US avg):** 1.2/10k units
- **Data Source:** Municipal building departments

#### S2.14 **eviction_legal_representation_rate**
- **Type:** Proportion
- **Unit:** 0-1 (% tenants with attorney)
- **Description:** Right to counsel or civil Gideon implementation
- **Baseline (US avg):** 0.03 (3% nationally)
- **Data Source:** National Coalition for a Civil Right to Counsel

### Category: Social Services Infrastructure

#### S2.15 **snap_outreach_intensity**
- **Type:** Index
- **Unit:** 0-10 scale
- **Description:** Proactivity of SNAP enrollment assistance
- **Baseline (US avg):** 4.5
- **Data Source:** USDA, state SNAP participation rates

#### S2.16 **tanf_case_management_ratio**
- **Type:** Real (ratio)
- **Unit:** Clients per case manager
- **Description:** TANF caseworker workload
- **Baseline (US avg):** 95:1
- **Data Source:** State TANF agencies

#### S2.17 **social_worker_density**
- **Type:** Real (rate)
- **Unit:** Social workers per 100,000 population
- **Description:** Licensed social work workforce
- **Baseline (US avg):** 110/100k
- **Data Source:** BLS OES

#### S2.18 **domestic_violence_shelter_capacity**
- **Type:** Real (rate)
- **Unit:** Beds per 100,000 population
- **Description:** Emergency domestic violence shelter availability
- **Baseline (US avg):** 12/100k
- **Data Source:** National Network to End Domestic Violence

#### S2.19 **homeless_services_capacity**
- **Type:** Real (rate)
- **Unit:** Emergency + transitional beds per 100,000
- **Description:** Homeless shelter and transitional housing
- **Baseline (US avg):** 35/100k
- **Data Source:** HUD Point-in-Time Count, HMIS

### Category: Education Infrastructure

#### S2.20 **school_counselor_ratio**
- **Type:** Real (ratio)
- **Unit:** Students per counselor
- **Description:** K-12 counselor availability
- **Baseline (US avg):** 430:1 (ASCA recommends 250:1)
- **Data Source:** NCES Common Core of Data

#### S2.21 **school_nurse_ratio**
- **Type:** Real (ratio)
- **Unit:** Students per nurse
- **Description:** K-12 school nurse staffing
- **Baseline (US avg):** 945:1 (NASN recommends 750:1)
- **Data Source:** NCES, state education agencies

#### S2.22 **afterschool_program_capacity**
- **Type:** Proportion
- **Unit:** 0-1 (% youth with access)
- **Description:** Afterschool and summer program availability
- **Baseline (US avg):** 0.24
- **Data Source:** Afterschool Alliance

### Category: Built Environment

#### S2.23 **public_transit_route_density**
- **Type:** Real (rate)
- **Unit:** Routes per 100,000 population
- **Description:** Transit service coverage
- **Baseline (US avg):** 18/100k (highly variable urban vs. rural)
- **Data Source:** FTA National Transit Database

#### S2.24 **green_space_acres_per_capita**
- **Type:** Real (rate)
- **Unit:** Park acres per 1,000 population
- **Description:** Municipal parks and green space
- **Baseline (US avg):** 11 acres/1k
- **Data Source:** Trust for Public Land ParkScore

#### S2.25 **bike_lane_miles_per_capita**
- **Type:** Real (rate)
- **Unit:** Miles per 100,000 population
- **Description:** Protected and conventional bike infrastructure
- **Baseline (US avg):** 8.5 miles/100k
- **Data Source:** League of American Bicyclists, PeopleForBikes

#### S2.26 **walkability_score**
- **Type:** Index
- **Unit:** 0-100 scale
- **Description:** Walk Score® or similar walkability metric
- **Baseline (US avg):** 48 (car-dependent)
- **Data Source:** Walk Score, EPA Smart Location Database

#### S2.27 **healthy_food_retail_density**
- **Type:** Real (rate)
- **Unit:** Supermarkets per 100,000 population
- **Description:** Access to healthy food retail
- **Baseline (US avg):** 12/100k
- **Data Source:** USDA Food Environment Atlas

#### S2.28 **food_pantry_density**
- **Type:** Real (rate)
- **Unit:** Food pantries per 100,000 population
- **Description:** Emergency food assistance points
- **Baseline (US avg):** 15/100k
- **Data Source:** Feeding America, state food bank associations

### Category: Criminal Justice Implementation

#### S2.29 **police_per_capita**
- **Type:** Real (rate)
- **Unit:** Sworn officers per 100,000 population
- **Description:** Law enforcement density
- **Baseline (US avg):** 240/100k
- **Data Source:** FBI UCR Law Enforcement Officers

#### S2.30 **pretrial_diversion_program_capacity**
- **Type:** Real (rate)
- **Unit:** Slots per 100,000 population
- **Description:** Alternative to prosecution program availability
- **Baseline (US avg):** 85/100k
- **Data Source:** Bureau of Justice Assistance

#### S2.31 **drug_court_capacity**
- **Type:** Real (rate)
- **Unit:** Drug court participants per 100,000 population
- **Description:** Treatment court availability
- **Baseline (US avg):** 45/100k
- **Data Source:** National Drug Court Resource Center

#### S2.32 **community_supervision_officers_ratio**
- **Type:** Real (ratio)
- **Unit:** Probationers/parolees per officer
- **Description:** Probation and parole officer caseload
- **Baseline (US avg):** 95:1
- **Data Source:** Bureau of Justice Statistics

#### S2.33 **reentry_program_capacity**
- **Type:** Real (rate)
- **Unit:** Program slots per 1,000 releases
- **Description:** Post-incarceration reintegration services
- **Baseline (US avg):** 120/1k releases
- **Data Source:** National Reentry Resource Center

### Category: Environmental Infrastructure

#### S2.34 **air_quality_monitoring_density**
- **Type:** Real (rate)
- **Unit:** Monitors per 100 square miles
- **Description:** EPA air quality monitoring stations
- **Baseline (US avg):** 0.08/100 sq mi
- **Data Source:** EPA AirNow

#### S2.35 **lead_pipe_replacement_rate**
- **Type:** Real (rate)
- **Unit:** % lead service lines replaced per year
- **Description:** Lead water infrastructure remediation pace
- **Baseline (US avg):** 0.03 (3% per year)
- **Data Source:** EPA, municipal water utilities

#### S2.36 **brownfield_remediation_funding**
- **Type:** Real (dollars)
- **Unit:** $ millions per year
- **Description:** Contaminated site cleanup investment
- **Baseline (US avg):** Varies by metro
- **Data Source:** EPA Brownfields Program

### Category: Organizational Quality & Implementation

#### S2.37 **cultural_competency_training_penetration**
- **Type:** Proportion
- **Unit:** 0-1 (% healthcare providers trained)
- **Description:** Ongoing cultural competency training
- **Baseline (US avg):** 0.45
- **Data Source:** Hospital HR data, accreditation surveys

#### S2.38 **interpreter_service_availability**
- **Type:** Binary/Coverage
- **Unit:** 0-1 (availability score)
- **Description:** Medical interpretation for LEP patients
- **Baseline (US avg):** 0.68
- **Data Source:** Hospital compliance reports

#### S2.39 **trauma_informed_care_penetration**
- **Type:** Proportion
- **Unit:** 0-1 (% organizations implementing TIC)
- **Description:** Trauma-informed care practice adoption
- **Baseline (US avg):** 0.32
- **Data Source:** SAMHSA, organizational surveys

#### S2.40 **community_benefit_spending**
- **Type:** Real (proportion of operating revenue)
- **Unit:** % of hospital revenue
- **Description:** Nonprofit hospital community benefit investment
- **Baseline (US avg):** 0.078 (7.8%)
- **Data Source:** IRS Form 990 Schedule H

#### S2.41 **pay_for_performance_penetration**
- **Type:** Proportion
- **Unit:** 0-1 (% revenue tied to quality)
- **Description:** Value-based payment prevalence
- **Baseline (US avg):** 0.39
- **Data Source:** Health Care Payment Learning & Action Network

#### S2.42 **community_health_needs_assessment_quality**
- **Type:** Index
- **Unit:** 0-10 scale
- **Description:** Quality and community engagement in CHNA
- **Baseline (US avg):** 5.2
- **Data Source:** Build Healthy Places Network assessment

---

## SCALE 3: INDIVIDUAL/HOUSEHOLD (Lived Experience)

**Time Horizon:** Months to 2 years
**Measurement:** Individual-level rates, household conditions, utilization
**Count:** 38 nodes

### Category: Economic Security

#### S3.01 **household_income_median**
- **Type:** Real (dollars)
- **Unit:** $/year
- **Description:** Median household income
- **Baseline (US avg):** $70,784 (2023)
- **Data Source:** Census ACS

#### S3.02 **poverty_rate**
- **Type:** Proportion
- **Unit:** 0-1 (% below FPL)
- **Description:** Population below federal poverty line
- **Baseline (US avg):** 0.118
- **Data Source:** Census ACS

#### S3.03 **deep_poverty_rate**
- **Type:** Proportion
- **Unit:** 0-1 (% below 50% FPL)
- **Description:** Population in deep poverty
- **Baseline (US avg):** 0.055
- **Data Source:** Census ACS

#### S3.04 **liquid_asset_poverty_rate**
- **Type:** Proportion
- **Unit:** 0-1 (% <$5,985 liquid assets)
- **Description:** Population without emergency savings
- **Baseline (US avg):** 0.43
- **Data Source:** CFED/Prosperity Now Scorecard

#### S3.05 **economic_precarity_index**
- **Type:** Proxy index
- **Unit:** 0-1 (higher = more precarious)
- **Components:**
  - Rent burden rate (35%)
  - Liquid asset poverty (30%)
  - Income volatility (25%)
  - Debt burden (10%)
- **Baseline (US avg):** 0.36
- **Data Source:** Constructed from Census, CFED, JPMCI

#### S3.06 **unemployment_rate**
- **Type:** Proportion
- **Unit:** 0-1 (% labor force unemployed)
- **Description:** Official unemployment rate
- **Baseline (US avg):** 0.037 (3.7%, as of 2024)
- **Data Source:** BLS Local Area Unemployment Statistics

#### S3.07 **underemployment_rate**
- **Type:** Proportion
- **Unit:** 0-1 (U-6 measure)
- **Description:** Unemployed + marginally attached + part-time for economic reasons
- **Baseline (US avg):** 0.071
- **Data Source:** BLS (metro areas only)

#### S3.08 **gig_economy_reliance**
- **Type:** Proportion
- **Unit:** 0-1 (% primary income from gig work)
- **Description:** Dependence on non-traditional employment
- **Baseline (US avg):** 0.16
- **Data Source:** JPMorgan Chase Institute, BLS contingent worker supplement

### Category: Housing Stability

#### S3.09 **housing_cost_burden_rate**
- **Type:** Proportion
- **Unit:** 0-1 (% paying >30% income on housing)
- **Description:** Population housing cost-burdened
- **Baseline (US avg):** 0.38
- **Data Source:** Census ACS

#### S3.10 **severe_housing_cost_burden_rate**
- **Type:** Proportion
- **Unit:** 0-1 (% paying >50% income on housing)
- **Description:** Population severely cost-burdened
- **Baseline (US avg):** 0.18
- **Data Source:** Census ACS

#### S3.11 **eviction_filing_rate_annual**
- **Type:** Real (rate)
- **Unit:** Eviction filings per 100 renter households per year
- **Description:** Eviction court case filing rate
- **Baseline (US avg):** 6.4 per 100 (pre-pandemic)
- **Data Source:** Eviction Lab

#### S3.12 **eviction_execution_rate**
- **Type:** Proportion of filings
- **Unit:** 0-1 (% filings → executed evictions)
- **Description:** Court-ordered eviction completion rate
- **Baseline (US avg):** 0.34
- **Data Source:** Eviction Lab, local courts

#### S3.13 **housing_instability_index**
- **Type:** Proxy index
- **Unit:** 0-1 (higher = more unstable)
- **Components:**
  - Cost burden >50% (40%)
  - Moved 2+ times in year (30%)
  - Doubled up (20%)
  - Eviction filed past year (10%)
- **Baseline (US avg):** 0.22
- **Data Source:** Constructed from ACS, Eviction Lab

#### S3.14 **homeownership_rate**
- **Type:** Proportion
- **Unit:** 0-1 (% households owning)
- **Description:** Owner-occupied housing rate
- **Baseline (US avg):** 0.656
- **Data Source:** Census ACS

#### S3.15 **homelessness_rate**
- **Type:** Real (rate)
- **Unit:** Per 10,000 population
- **Description:** Point-in-time homelessness prevalence
- **Baseline (US avg):** 17.5 per 10k
- **Data Source:** HUD Point-in-Time Count

### Category: Healthcare Access

#### S3.16 **uninsured_rate**
- **Type:** Proportion
- **Unit:** 0-1 (% without health insurance)
- **Description:** Population lacking health coverage
- **Baseline (US avg):** 0.088
- **Data Source:** Census ACS

#### S3.17 **underinsured_rate**
- **Type:** Proportion
- **Unit:** 0-1 (% with high out-of-pocket burden despite coverage)
- **Description:** Insured but high-deductible/cost-sharing
- **Baseline (US avg):** 0.23
- **Data Source:** Commonwealth Fund Biennial Health Insurance Survey

#### S3.18 **usual_source_of_care_rate**
- **Type:** Proportion
- **Unit:** 0-1 (% with regular provider)
- **Description:** Population with identified primary care provider
- **Baseline (US avg):** 0.73
- **Data Source:** NHIS, BRFSS

#### S3.19 **delayed_care_due_to_cost_rate**
- **Type:** Proportion
- **Unit:** 0-1 (% delaying needed care)
- **Description:** Cost-related care avoidance
- **Baseline (US avg):** 0.27
- **Data Source:** NHIS, Commonwealth Fund

#### S3.20 **healthcare_continuity_index**
- **Type:** Proxy index
- **Unit:** 0-1 (higher = better continuity)
- **Components:**
  - Insurance persistence (40%)
  - Provider retention (30%)
  - Appointment completion (30%)
- **Baseline (US avg):** 0.58
- **Data Source:** Constructed from claims data, surveys

#### S3.21 **prescription_medication_adherence**
- **Type:** Proportion
- **Unit:** 0-1 (PDC ≥0.80)
- **Description:** Medication adherence rate (proportion of days covered)
- **Baseline (US avg):** 0.54
- **Data Source:** Pharmacy claims, Medicare Star Ratings

### Category: Food Security

#### S3.22 **food_insecurity_rate**
- **Type:** Proportion
- **Unit:** 0-1 (% food insecure)
- **Description:** USDA food security measure
- **Baseline (US avg):** 0.125
- **Data Source:** Census Current Population Survey Food Security Supplement

#### S3.23 **very_low_food_security_rate**
- **Type:** Proportion
- **Unit:** 0-1 (% very low food security)
- **Description:** Severe food insecurity (hunger)
- **Baseline (US avg):** 0.048
- **Data Source:** CPS Food Security Supplement

#### S3.24 **snap_participation_rate_among_eligible**
- **Type:** Proportion
- **Unit:** 0-1 (% eligible receiving SNAP)
- **Description:** SNAP take-up rate
- **Baseline (US avg):** 0.82
- **Data Source:** USDA Food and Nutrition Service

### Category: Social Connectedness

#### S3.25 **social_isolation_rate**
- **Type:** Proportion
- **Unit:** 0-1 (% with <1 close social contact)
- **Description:** Severe social isolation prevalence
- **Baseline (US avg):** 0.28
- **Data Source:** BRFSS, General Social Survey

#### S3.26 **community_trust_index**
- **Type:** Proxy index
- **Unit:** 0-1 (higher = more trust)
- **Components:**
  - Survey trust score (50%)
  - Civic participation rate (30%)
  - Mutual aid density (20%)
- **Baseline (US avg):** 0.52
- **Data Source:** Constructed from GSS, AmeriCorps, local surveys

#### S3.27 **perceived_discrimination_rate**
- **Type:** Proportion
- **Unit:** 0-1 (% reporting discrimination past year)
- **Description:** Self-reported discrimination in daily life
- **Baseline (US avg):** 0.31 (varies dramatically by race)
- **Data Source:** BRFSS, Robert Wood Johnson Foundation surveys

### Category: Environmental Exposures

#### S3.28 **air_quality_index_avg**
- **Type:** Real (index)
- **Unit:** EPA AQI (0-500 scale)
- **Description:** Annual average AQI
- **Baseline (US avg):** 48 (good)
- **Data Source:** EPA AirNow

#### S3.29 **lead_exposure_risk**
- **Type:** Proportion
- **Unit:** 0-1 (% housing built pre-1978 with lead paint)
- **Description:** Population at risk of lead exposure
- **Baseline (US avg):** 0.38
- **Data Source:** Census AHS, HUD American Healthy Homes Survey

#### S3.30 **noise_pollution_exposure**
- **Type:** Real (decibels)
- **Unit:** dB average
- **Description:** Environmental noise exposure
- **Baseline (US avg):** 55 dB (varies urban/rural)
- **Data Source:** EPA, WHO noise maps

#### S3.31 **green_space_access**
- **Type:** Proportion
- **Unit:** 0-1 (% within 10-min walk of park)
- **Description:** Residential proximity to green space
- **Baseline (US avg):** 0.55
- **Data Source:** Trust for Public Land 10-Minute Walk

### Category: Education & Development

#### S3.32 **educational_attainment_hs_plus**
- **Type:** Proportion
- **Unit:** 0-1 (% HS diploma or higher, age 25+)
- **Description:** High school completion rate
- **Baseline (US avg):** 0.898
- **Data Source:** Census ACS

#### S3.33 **educational_attainment_bachelors_plus**
- **Type:** Proportion
- **Unit:** 0-1 (% Bachelor's or higher, age 25+)
- **Description:** College completion rate
- **Baseline (US avg):** 0.378
- **Data Source:** Census ACS

#### S3.34 **early_childhood_development_readiness**
- **Type:** Proportion
- **Unit:** 0-1 (% kindergarten-ready)
- **Description:** Developmental readiness at school entry
- **Baseline (US avg):** 0.48 (varies by assessment)
- **Data Source:** State kindergarten assessments, NAEYC

### Category: Stress & Adversity

#### S3.35 **chronic_stress_prevalence**
- **Type:** Proportion
- **Unit:** 0-1 (% reporting chronic stress)
- **Description:** Self-reported chronic stress
- **Baseline (US avg):** 0.44
- **Data Source:** APA Stress in America survey, BRFSS

#### S3.36 **adverse_childhood_experiences_score_avg**
- **Type:** Mean score
- **Unit:** 0-10 scale average
- **Description:** Population average ACE score
- **Baseline (US avg):** 1.4
- **Data Source:** BRFSS ACE module

#### S3.37 **intimate_partner_violence_rate**
- **Type:** Real (rate)
- **Unit:** Per 1,000 population per year
- **Description:** Reported IPV incidents
- **Baseline (US avg):** 4.2 per 1,000 (underreported)
- **Data Source:** NCVS, state coalitions

### Category: Justice System Contact

#### S3.38 **arrest_rate_annual**
- **Type:** Real (rate)
- **Unit:** Arrests per 1,000 population per year
- **Description:** Annual arrest rate
- **Baseline (US avg):** 32 per 1,000
- **Data Source:** FBI UCR Arrests

---

## INTERMEDIATE/PROXY STOCKS

**Description:** Composite indices and pathways between determinants and outcomes
**Count:** 18 nodes

### Health Behavior & Utilization

#### INT.01 **healthcare_seeking_rate**
- **Type:** Real (rate)
- **Unit:** Ambulatory visits per person per year
- **Description:** Healthcare utilization frequency
- **Baseline (US avg):** 3.2 visits/person/year
- **Data Source:** NHIS, MEPS

#### INT.02 **preventive_care_utilization_rate**
- **Type:** Proportion
- **Unit:** 0-1 (% receiving recommended preventive services)
- **Description:** Preventive service uptake
- **Baseline (US avg):** 0.57
- **Data Source:** NHIS, BRFSS

#### INT.03 **emergency_department_utilization_rate**
- **Type:** Real (rate)
- **Unit:** ED visits per 1,000 population per year
- **Description:** ED use rate (all-cause)
- **Baseline (US avg):** 420 per 1,000/year
- **Data Source:** NHAMCS, hospital discharge data

#### INT.04 **preventable_ed_visit_rate**
- **Type:** Real (rate)
- **Unit:** Preventable ED visits per 1,000 population per year
- **Description:** Low-acuity ED visits (NYU algorithm)
- **Baseline (US avg):** ~140 per 1,000/year (33% of total)
- **Data Source:** Hospital discharge data, NYU classification

### Chronic Disease Management

#### INT.05 **diabetes_management_quality**
- **Type:** Index
- **Unit:** 0-1 scale
- **Components:**
  - HbA1c testing rate
  - HbA1c control <8%
  - Eye exam completion
  - Nephropathy screening
- **Baseline (US avg):** 0.62
- **Data Source:** HEDIS, Medicare Star Ratings

#### INT.06 **hypertension_control_rate**
- **Type:** Proportion
- **Unit:** 0-1 (% with BP <140/90)
- **Description:** Blood pressure control among hypertensives
- **Baseline (US avg):** 0.48
- **Data Source:** NHANES, HEDIS

#### INT.07 **asthma_control_rate**
- **Type:** Proportion
- **Unit:** 0-1 (% well-controlled)
- **Description:** Asthma symptom control
- **Baseline (US avg):** 0.54
- **Data Source:** BRFSS, HEDIS medication ratio

### Mental Health & Substance Use

#### INT.08 **mental_health_treatment_rate**
- **Type:** Proportion
- **Unit:** 0-1 (% with mental illness receiving treatment)
- **Description:** Treatment engagement among those with need
- **Baseline (US avg):** 0.44
- **Data Source:** NSDUH, SAMHSA

#### INT.09 **substance_use_treatment_rate**
- **Type:** Proportion
- **Unit:** 0-1 (% with SUD receiving treatment)
- **Description:** Treatment engagement among those with SUD
- **Baseline (US avg):** 0.11
- **Data Source:** NSDUH

#### INT.10 **opioid_prescribing_rate**
- **Type:** Real (rate)
- **Unit:** Opioid prescriptions per 100 population per year
- **Description:** Prescription opioid exposure
- **Baseline (US avg):** 43.3 per 100 (declining from 81.3 in 2012)
- **Data Source:** CDC, IQVIA prescription data

### Physical Activity & Nutrition

#### INT.11 **physical_activity_rate**
- **Type:** Proportion
- **Unit:** 0-1 (% meeting aerobic + strength guidelines)
- **Description:** Population meeting physical activity guidelines
- **Baseline (US avg):** 0.24
- **Data Source:** NHIS, BRFSS

#### INT.12 **fruit_vegetable_consumption_adequate**
- **Type:** Proportion
- **Unit:** 0-1 (% meeting 5-a-day recommendation)
- **Description:** Dietary quality (fruit/vegetable intake)
- **Baseline (US avg):** 0.12
- **Data Source:** BRFSS, NHANES

### Smoking & Substance Use

#### INT.13 **smoking_prevalence**
- **Type:** Proportion
- **Unit:** 0-1 (% current smokers)
- **Description:** Cigarette smoking prevalence
- **Baseline (US avg):** 0.12 (declining)
- **Data Source:** NHIS, BRFSS

#### INT.14 **binge_drinking_prevalence**
- **Type:** Proportion
- **Unit:** 0-1 (% binge drinking past month)
- **Description:** Heavy episodic alcohol use
- **Baseline (US avg):** 0.26
- **Data Source:** NSDUH, BRFSS

### Housing Quality

#### INT.15 **housing_quality_index**
- **Type:** Proxy index
- **Unit:** 0-1 (higher = better quality)
- **Components:**
  - Lack of complete plumbing (inverse, 20%)
  - Lack of complete kitchen (inverse, 20%)
  - Crowding >1 person/room (inverse, 20%)
  - Structural defects (inverse, 20%)
  - Heating inadequacy (inverse, 20%)
- **Baseline (US avg):** 0.87
- **Data Source:** Constructed from Census AHS

#### INT.16 **neighborhood_safety_perception**
- **Type:** Proportion
- **Unit:** 0-1 (% feeling safe walking at night)
- **Description:** Perceived neighborhood safety
- **Baseline (US avg):** 0.71
- **Data Source:** BRFSS, local surveys

### Transportation Access

#### INT.17 **transportation_access_index**
- **Type:** Proxy index
- **Unit:** 0-1 (higher = better access)
- **Components:**
  - Vehicle access (50%)
  - Transit proximity (30%)
  - Walkability (20%)
- **Baseline (US avg):** 0.64
- **Data Source:** Constructed from ACS, EPA Smart Location

### Allostatic Load (Cumulative Stress)

#### INT.18 **allostatic_load_avg**
- **Type:** Biomarker index
- **Unit:** 0-10+ scale (count of high-risk biomarkers)
- **Components:**
  - Cardiovascular (SBP, DBP, pulse)
  - Metabolic (BMI, HbA1c, cholesterol)
  - Inflammatory (CRP, fibrinogen)
  - Neuroendocrine (cortisol, DHEA-S)
- **Baseline (US avg):** 2.8 (varies by race, SES)
- **Data Source:** NHANES biomarker data

---

## CRISIS ENDPOINTS (Health Outcomes)

**Description:** Monetized health outcomes used for ROI and burden calculation
**Count:** 23 nodes

### Acute Care Utilization

#### CRISIS.01 **ed_visits_annual**
- **Type:** Real (count)
- **Unit:** Visits per year
- **Description:** Emergency department visits (all-cause)
- **Unit Cost:** $1,200 per visit
- **Baseline (US avg):** 130 million visits/year nationally (420 per 1,000)
- **Data Source:** NHAMCS

#### CRISIS.02 **preventable_ed_visits_annual**
- **Type:** Real (count)
- **Unit:** Preventable visits per year
- **Description:** Low-acuity ED visits (ambulatory care-sensitive)
- **Unit Cost:** $1,200 per visit
- **Baseline (US avg):** ~43 million/year (33% of total)
- **Data Source:** Hospital discharge data, NYU algorithm

#### CRISIS.03 **hospitalizations_annual**
- **Type:** Real (count)
- **Unit:** Admissions per year
- **Description:** Inpatient hospitalizations (all-cause)
- **Unit Cost:** $12,500 per admission (average)
- **Baseline (US avg):** 35 million admissions/year (107 per 1,000)
- **Data Source:** NHDS, HCUP NIS

#### CRISIS.04 **ambulatory_care_sensitive_hospitalizations_annual**
- **Type:** Real (count)
- **Unit:** ACS admissions per year
- **Description:** Preventable hospitalizations (AHRQ PQI)
- **Unit Cost:** $12,500 per admission
- **Baseline (US avg):** ~5 million/year (14% of total)
- **Data Source:** HCUP, AHRQ PQI

#### CRISIS.05 **icu_days_annual**
- **Type:** Real (patient-days)
- **Unit:** ICU days per year
- **Description:** Intensive care unit utilization
- **Unit Cost:** $4,500 per day
- **Baseline (US avg):** Varies by region
- **Data Source:** Hospital discharge data

#### CRISIS.06 **readmissions_30day_rate**
- **Type:** Proportion
- **Unit:** 0-1 (% readmitted within 30 days)
- **Description:** All-cause 30-day readmission rate
- **Unit Cost:** Additional $12,500 per readmission
- **Baseline (US avg):** 0.14 (14%)
- **Data Source:** CMS Hospital Readmissions Reduction Program

### Chronic Disease Prevalence

#### CRISIS.07 **diabetes_prevalence**
- **Type:** Proportion
- **Unit:** 0-1 (% diagnosed diabetes)
- **Description:** Diagnosed diabetes prevalence
- **Annual Cost:** $9,600 per person-year (direct medical)
- **Baseline (US avg):** 0.105
- **Data Source:** NHIS, BRFSS

#### CRISIS.08 **hypertension_prevalence**
- **Type:** Proportion
- **Unit:** 0-1 (% diagnosed hypertension)
- **Description:** Diagnosed hypertension prevalence
- **Annual Cost:** $2,100 per person-year
- **Baseline (US avg):** 0.33
- **Data Source:** NHANES, BRFSS

#### CRISIS.09 **obesity_prevalence**
- **Type:** Proportion
- **Unit:** 0-1 (% BMI ≥30)
- **Description:** Obesity prevalence
- **Annual Cost:** $1,900 excess per person-year
- **Baseline (US avg):** 0.42
- **Data Source:** NHANES, BRFSS

#### CRISIS.10 **asthma_prevalence**
- **Type:** Proportion
- **Unit:** 0-1 (% current asthma)
- **Description:** Current asthma prevalence
- **Annual Cost:** $3,300 per person-year
- **Baseline (US avg):** 0.079
- **Data Source:** NHIS, BRFSS

### Mental Health & Substance Use Crises

#### CRISIS.11 **depression_prevalence**
- **Type:** Proportion
- **Unit:** 0-1 (% major depressive episode past year)
- **Description:** Major depression prevalence
- **Annual Cost:** $5,100 per person-year (direct medical + productivity)
- **Baseline (US avg):** 0.082
- **Data Source:** NSDUH, NHIS

#### CRISIS.12 **suicide_attempts_annual**
- **Type:** Real (count)
- **Unit:** Attempts requiring hospitalization per year
- **Description:** Serious suicide attempts
- **Unit Cost:** $18,000 per attempt (medical + psych)
- **Baseline (US avg):** ~550,000 attempts/year (1.7 per 1,000)
- **Data Source:** WISQARS, hospital data

#### CRISIS.13 **overdose_nonfatal_annual**
- **Type:** Real (count)
- **Unit:** Non-fatal overdoses per year
- **Description:** Drug overdose events (all drugs)
- **Unit Cost:** $25,000 per event (ED + hospital + follow-up)
- **Baseline (US avg):** ~100,000/year (varies dramatically by region)
- **Data Source:** EMS, syndromic surveillance, DAWN

#### CRISIS.14 **overdose_deaths_annual**
- **Type:** Real (count)
- **Unit:** Fatal overdoses per year
- **Description:** Drug overdose mortality
- **Unit Cost:** Included in VSL calculation (varies by age)
- **Baseline (US avg):** ~107,000/year (32 per 100,000)
- **Data Source:** CDC WONDER, NVSS

### Mortality

#### CRISIS.15 **all_cause_mortality_rate**
- **Type:** Real (rate)
- **Unit:** Deaths per 100,000 per year
- **Description:** All-cause mortality (age-adjusted)
- **Unit Cost:** Age-specific VSL ($500k-$10M)
- **Baseline (US avg):** 723.6 per 100,000 (age-adjusted)
- **Data Source:** CDC WONDER

#### CRISIS.16 **premature_mortality_ypll**
- **Type:** Real (count)
- **Unit:** Years of potential life lost (YPLL) before age 75
- **Description:** Premature death burden
- **Unit Cost:** Age-specific VSL
- **Baseline (US avg):** ~20 million YPLL nationally
- **Data Source:** CDC WONDER, County Health Rankings

#### CRISIS.17 **infant_mortality_rate**
- **Type:** Real (rate)
- **Unit:** Deaths per 1,000 live births
- **Description:** Infant mortality (<1 year)
- **Unit Cost:** VSL ~$10M
- **Baseline (US avg):** 5.4 per 1,000
- **Data Source:** NVSS

#### CRISIS.18 **maternal_mortality_rate**
- **Type:** Real (rate)
- **Unit:** Deaths per 100,000 live births
- **Description:** Pregnancy-related mortality
- **Unit Cost:** VSL $8-10M
- **Baseline (US avg):** 23.8 per 100,000 (highest in developed world)
- **Data Source:** NVSS, CDC Maternal Mortality Review

### Birth Outcomes

#### CRISIS.19 **adverse_birth_outcomes_annual**
- **Type:** Real (count)
- **Unit:** NICU admissions per year
- **Description:** Severe adverse birth outcomes requiring NICU
- **Unit Cost:** $100,000 per NICU admission (average)
- **Baseline (US avg):** ~450,000/year (12% of births)
- **Data Source:** Birth certificates, hospital discharge

#### CRISIS.20 **low_birthweight_rate**
- **Type:** Proportion
- **Unit:** 0-1 (% <2,500g)
- **Description:** Low birthweight prevalence
- **Unit Cost:** $54,000 excess cost (average)
- **Baseline (US avg):** 0.083
- **Data Source:** NVSS birth data

### Homelessness & Justice

#### CRISIS.21 **homelessness_person_years_annual**
- **Type:** Real (person-years)
- **Unit:** Person-years of homelessness per year
- **Description:** Annual homelessness burden
- **Unit Cost:** $50,000 per person-year (services + opportunity)
- **Baseline (US avg):** ~580,000 person-years
- **Data Source:** HUD Point-in-Time, HMIS

#### CRISIS.22 **arrests_annual**
- **Type:** Real (count)
- **Unit:** Arrests per year
- **Description:** Criminal justice arrests (all offenses)
- **Unit Cost:** $5,000 per arrest (processing + court + opportunity)
- **Baseline (US avg):** ~10 million/year (32 per 1,000)
- **Data Source:** FBI UCR

#### CRISIS.23 **incarceration_person_years_annual**
- **Type:** Real (person-years)
- **Unit:** Person-years incarcerated per year
- **Description:** Jail + prison incarceration burden
- **Unit Cost:** $45,000 per person-year (direct cost, excludes social costs)
- **Baseline (US avg):** ~2.1 million person-years (highest globally)
- **Data Source:** Bureau of Justice Statistics

---

## NODE RELATIONSHIP FRAMEWORK

### Canonical Pathways (Examples)

**Pathway 1: Eviction → Health Crisis**
```
S1.09 eviction_protection_strength (STRUCTURAL)
  ↓ moderates
S3.11 eviction_filing_rate_annual (INDIVIDUAL)
  ↓ increases
S3.13 housing_instability_index (INDIVIDUAL)
  ↓ disrupts
S3.20 healthcare_continuity_index (INTERMEDIATE)
  ↓ reduces
INT.02 preventive_care_utilization_rate (INTERMEDIATE)
  ↓ worsens
INT.06 hypertension_control_rate (INTERMEDIATE)
  ↓ increases
CRISIS.03 hospitalizations_annual (CRISIS ENDPOINT)
```

**Pathway 2: Medicaid Expansion → Mortality**
```
S1.01 medicaid_expansion_status (STRUCTURAL)
  ↓ increases
S3.16 uninsured_rate (inverse) (INDIVIDUAL)
  ↓ increases
S3.18 usual_source_of_care_rate (INDIVIDUAL)
  ↓ increases
S3.20 healthcare_continuity_index (INTERMEDIATE)
  ↓ increases
INT.02 preventive_care_utilization_rate (INTERMEDIATE)
  ↓ improves
INT.05 diabetes_management_quality (INTERMEDIATE)
  ↓ reduces
CRISIS.16 premature_mortality_ypll (CRISIS ENDPOINT)
```

**Pathway 3: Minimum Wage → Food Security → Health**
```
S1.12 minimum_wage_dollars (STRUCTURAL)
  ↓ increases
S3.01 household_income_median (INDIVIDUAL)
  ↓ reduces
S3.05 economic_precarity_index (INDIVIDUAL)
  ↓ reduces
S3.22 food_insecurity_rate (INDIVIDUAL)
  ↓ improves
INT.12 fruit_vegetable_consumption_adequate (INTERMEDIATE)
  ↓ reduces
CRISIS.07 diabetes_prevalence (CRISIS ENDPOINT)
```

**Pathway 4: Green Space → Mental Health**
```
S1.32 parks_investment_per_capita (STRUCTURAL)
  ↓ increases
S2.24 green_space_acres_per_capita (INSTITUTIONAL)
  ↓ increases
S3.31 green_space_access (INDIVIDUAL)
  ↓ increases
INT.11 physical_activity_rate (INTERMEDIATE)
  ↓ reduces
S3.35 chronic_stress_prevalence (INDIVIDUAL)
  ↓ reduces
CRISIS.11 depression_prevalence (CRISIS ENDPOINT)
```

**Pathway 5: Criminal Justice Reform → Reentry → Health**
```
S1.22 criminal_justice_approach (STRUCTURAL)
  ↓ increases (higher score = reform)
S2.33 reentry_program_capacity (INSTITUTIONAL)
  ↓ improves
S3.05 economic_precarity_index (post-release) (INDIVIDUAL)
  ↓ reduces
S3.13 housing_instability_index (INDIVIDUAL)
  ↓ reduces
S3.16 uninsured_rate (INDIVIDUAL)
  ↓ reduces
CRISIS.13 overdose_nonfatal_annual (CRISIS ENDPOINT)
```

---

## MEASUREMENT PROTOCOLS

### Data Source Priority

**Tier 1 (Preferred):** Administrative data, vital statistics
- Census ACS, NVSS, NHANES, hospital discharge data
- High validity, consistent methodology

**Tier 2 (Acceptable):** Established surveys, standardized assessments
- BRFSS, NHIS, NSDUH, MEPS
- Good validity, some sampling variability

**Tier 3 (Use with caution):** Local surveys, modeled estimates
- Community health needs assessments, small-area estimates
- Higher uncertainty, validation needed

### Geographic Specification

**National Baseline:** US average (weighted by population)
**Regional Baselines:** Required for 4 Census regions minimum
**Local Calibration:** Metro/county-specific where available

### Temporal Updates

**Annual:** Crisis endpoints, utilization rates, prevalence
**Biennial:** Survey-based intermediate stocks
**5-year:** Structural policy indices (slower-moving)

### Missing Data Protocols

**Imputation:** Small-area estimation (SAE) from state/national
**Proxy:** Use best available proxy with documented limitations
**Flag:** Indicate data quality and missingness in metadata

---

## SUMMARY STATISTICS

| Category | Node Count | % of Total |
|----------|------------|------------|
| **Scale 1: Structural** | 35 | 22.4% |
| **Scale 2: Institutional** | 42 | 26.9% |
| **Scale 3: Individual** | 38 | 24.4% |
| **Intermediate/Proxy** | 18 | 11.5% |
| **Crisis Endpoints** | 23 | 14.7% |
| **TOTAL** | **156** | **100%** |

### Coverage by Domain

| Domain | Nodes | Key Gaps |
|--------|-------|----------|
| **Healthcare System** | 28 | Mental health provider types, telehealth |
| **Housing** | 15 | Housing quality subcomponents |
| **Economic Security** | 18 | Wealth/assets beyond liquid |
| **Criminal Justice** | 14 | Police practices, court delays |
| **Food & Nutrition** | 7 | Food quality metrics |
| **Built Environment** | 12 | Noise, water quality |
| **Social Determinants** | 19 | Discrimination measurement |
| **Education** | 8 | School quality metrics |
| **Crisis Outcomes** | 23 | Disability, pain |
| **Other** | 12 | - |

---

## NEXT STEPS FOR EXPANSION

### Phase 1 Completion (to 400 nodes):

**Priority Additions:**
1. Disaggregate crisis endpoints by subtype (e.g., ED visits by diagnosis)
2. Add implementation quality indices (30-40 nodes)
3. Expand environmental exposures (water, noise, toxic sites)
4. Add healthcare quality measures (patient experience, clinical quality)
5. Expand justice system (court processing, probation quality)
6. Add behavioral health subspecialties (trauma, eating disorders)
7. Specify racial/ethnic stratification for key nodes

### Phase 2 Quantification:

**Mechanism Extraction:**
- For each node pair, specify effect sizes from literature
- Quantify moderators (exact multipliers)
- Document functional forms (sigmoid, log, threshold, etc.)
- Build feedback loop specifications

### Phase 3 Geographic Adaptation:

**Regional Baselines:**
- 50 states
- 100 largest metros
- Rural/urban splits
- Tribal lands

---

**Document Version:** 1.0
**Last Updated:** 2025-11-16
**Total Nodes:** 156 (core non-redundant set)
**Pathway Coverage:** 5 canonical pathways documented (50+ to come)
**Data Source Documentation:** Complete for all 156 nodes
**Baseline Values:** US national averages (as of 2023-2024)

**Maintained by:** HealthSystems Platform Team
**File Location:** `NODE_BANK_COMPREHENSIVE.md`
