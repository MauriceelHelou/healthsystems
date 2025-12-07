# Complete Node Inventory

**Version:** 1.0
**Last Updated:** 2025-11-18
**Total Nodes:** ~850 fully specified nodes
**Organization:** Hybrid (Scale Hierarchy + Domain Taxonomy)

---

## Document Structure

This inventory is organized hierarchically by **Scale** (primary) and **Domain** (secondary):

### Scale 1: STRUCTURAL DETERMINANTS (~120 nodes)
- Healthcare System Policy
- Housing Policy
- Labor and Employment Policy
- Criminal Justice Policy
- Education and Child Welfare Policy
- Environmental and Climate Policy
- Infrastructure Investment Policy
- Taxation and Fiscal Policy
- Trade and Economic Policy

### Scale 2: INSTITUTIONAL INFRASTRUCTURE (~250 nodes)
- Healthcare Delivery Infrastructure
- Housing Infrastructure
- Social Service Organizations
- Education Infrastructure
- Built Environment and Transportation
- Criminal Justice Implementation
- Environmental Infrastructure
- Public Health Infrastructure
- Workplace and Occupational Infrastructure
- Community-Based Organizations

### Scale 3: INDIVIDUAL/HOUSEHOLD CONDITIONS (~280 nodes)
- Economic Security
- Housing Stability and Quality
- Healthcare Access and Coverage
- Food Security
- Social Connectedness and Discrimination
- Environmental Exposures
- Education and Development
- Employment Conditions and Occupational Exposures
- Stress, Trauma, and Adversity
- Justice System Contact
- Digital Access and Literacy
- Transportation Access and Burden

### Scale 4: INTERMEDIATE PATHWAYS (~100 nodes)
- Healthcare Utilization and Preventive Care
- Chronic Disease Control and Management
- Mental Health and Substance Use Treatment
- Health Behaviors
- Biological Risk Factors
- Housing and Neighborhood Conditions
- Physiological Stress

### Scale 5: CRISIS ENDPOINTS (~100 nodes)
- Acute Care Utilization
- Chronic Disease Prevalence
- Mental Health and Substance Use Crises
- Mortality
- Birth Outcomes
- Disability and Functional Limitation
- Homelessness and Housing Crises
- Criminal Justice Involvement
- Financial Toxicity

---

## Node Specification Format

Each node includes:
- **Node Name**
- **Scale**
- **Domain(s)**
- **Type**
- **Unit of Measurement**
- **Description**
- **Baseline US Value**
- **Data Source(s)**

---

**NOTE:** This document consolidates and replaces:
- `complete_node_inventory.txt` (592 nodes, simple list)
- `NODE_BANK_COMPREHENSIVE.md` (156 nodes, partial specification)
- `MISSING_NODES_ANALYSIS.md` (gap analysis)

**See also:** `NODE_SYSTEM_DEFINITIONS.md` for foundational concepts and measurement principles.

---

# SCALE 1: STRUCTURAL DETERMINANTS

Federal/State Policy Level - Laws, regulations, and macro-economic conditions that shape the opportunity structure

---

## 1.1 HEALTHCARE SYSTEM POLICY

### Node 1: Medicaid Expansion Status
- **Scale:** 1
- **Domain:** Healthcare System
- **Type:** Policy
- **Unit:** Binary (0=not expanded, 1=expanded)
- **Description:** Whether a state has adopted the Affordable Care Act Medicaid expansion to cover adults up to 138% FPL. Coded as 1 if expansion is implemented, 0 otherwise. Includes states that have partially expanded or delayed implementation.
- **Baseline:** 40 states + DC expanded as of 2024. 10 states not expanded (mostly Southern states). Source: KFF State Health Facts.
- **Data Source:** Kaiser Family Foundation (KFF) Medicaid expansion tracker, updated quarterly. State-level only. https://www.kff.org/medicaid/issue-brief/status-of-state-medicaid-expansion-decisions/

### Node 2: Medicaid Work Requirements Status
- **Scale:** 4
- **Domain:** Healthcare System
- **Type:** Policy
- **Unit:** Binary (0=no work requirements, 1=work requirements implemented)
- **Description:** Whether a state has implemented Medicaid work or community engagement requirements for non-disabled adults. Includes approved waivers even if implementation is paused by litigation.
- **Baseline:** 0 states as of 2024 (all prior implementations struck down or rescinded). Historically: 8 states attempted 2018-2020. Source: KFF.
- **Data Source:** KFF Medicaid waiver tracker, CMS waiver database. State-level.

### Node 3: Medicaid Coverage Generosity Index
- **Scale:** 4
- **Domain:** Healthcare System
- **Type:** Policy
- **Unit:** Index score 0-100 (higher = more generous)
- **Description:** Composite index of Medicaid program generosity including: income eligibility thresholds for parents and childless adults, coverage of optional benefits (dental, vision, non-emergency medical transportation), reimbursement rates relative to Medicare, managed care penetration (inverse), and prior authorization stringency (inverse). Standardized 0-100 scale.
- **Baseline:** National median = 52. Range: 28 (TX) to 87 (NY, CA). Source: Medicaid and CHIP Payment and Access Commission (MACPAC) analysis.
- **Data Source:** MACPAC annual reports, KFF state Medicaid fact sheets, CMS financial reports. State-level, annual.

### Node 4: Marketplace Plan Availability
- **Scale:** 4
- **Domain:** Healthcare System
- **Type:** Access/Availability
- **Unit:** Number of insurance carriers offering plans on state marketplace
- **Description:** Count of distinct insurance carriers offering at least one plan on the state's ACA marketplace (exchange) for individual coverage. Does not include off-exchange plans. Measured during open enrollment period.
- **Baseline:** 3.2 carriers per state (median, 2024). Range: 1 carrier (WV, WY) to 12+ carriers (FL, CA). Down from 5.6 in 2015. Source: CMS marketplace data.
- **Data Source:** CMS Marketplace Open Enrollment Public Use Files, annual. State and county-level availability.

### Node 5: ACA Premium Tax Credit Generosity
- **Scale:** 1
- **Domain:** Healthcare System
- **Type:** Policy
- **Unit:** Maximum household income % FPL eligible for subsidies
- **Description:** The maximum income threshold for eligibility for premium tax credits (subsidies) for marketplace coverage. As of American Rescue Plan Act 2021, no income cap (previously 400% FPL). Measure captures policy in effect for plan year.
- **Baseline:** No income cap as of 2021 (temporary, extended through 2025). Pre-2021: 400% FPL. Source: IRS, KFF.
- **Data Source:** Federal legislation (ARPA, IRA), IRS regulations. Federal policy with state-specific impacts.

### Node 6: Prescription Drug Price Regulation Stringency
- **Scale:** 1
- **Domain:** Healthcare System
- **Type:** Policy
- **Unit:** Index 0-10 (higher = more stringent regulation)
- **Description:** State-level index of prescription drug price regulation including: drug price transparency laws (manufacturer reporting), price gouging prohibitions, importation programs, Medicaid supplemental rebates, PBM regulation, and participation in multi-state purchasing pools. Composite score 0-10.
- **Baseline:** National median = 3.5. Range: 0 (many states with no regulation) to 9 (CA, CO, ME). Source: National Academy for State Health Policy (NASHP).
- **Data Source:** NASHP Prescription Drug State Bill Tracking Database, annual. State-level.

### Node 7: Pharmacy Benefit Manager (PBM) Regulation Index
- **Scale:** 1
- **Domain:** Healthcare System
- **Type:** Policy
- **Unit:** Index 0-10 (higher = more regulated)
- **Description:** State-level index of PBM regulation including: licensure requirements, spread pricing restrictions, transparency requirements (rebates, formularies), network adequacy standards, gag clause prohibitions, and fiduciary duty standards. Composite 0-10 scale.
- **Baseline:** National median = 4.2. Range: 0 (no PBM-specific regulation) to 8.5 (AR, LA, OK with comprehensive laws). Source: NASHP, NCSL.
- **Data Source:** National Academy for State Health Policy (NASHP), National Conference of State Legislatures (NCSL) PBM tracking. State-level, annual.

### Node 8: Surprise Billing Protection Strength
- **Scale:** 1
- **Domain:** Healthcare System
- **Type:** Policy
- **Unit:** Index 0-10 (higher = stronger protection)
- **Description:** State-level index of consumer protections against surprise out-of-network billing, including: emergency services protection, scheduled services protection, dispute resolution mechanisms, network adequacy standards, and billing transparency requirements. Federal No Surprises Act (2022) establishes floor; state laws may exceed. Composite 0-10.
- **Baseline:** All states have baseline federal protection (5.0) as of 2022. State law variation: 5.0 (federal only) to 9.0 (CA, NY with additional protections). Source: Commonwealth Fund analysis.
- **Data Source:** Commonwealth Fund state balance billing analysis, NAIC model law tracking. State-level, updated with legislation.

### Node 9: Telehealth Payment Parity Laws
- **Scale:** 1
- **Domain:** Healthcare System
- **Type:** Policy
- **Unit:** Categorical: None, Private only, Medicaid only, Both
- **Description:** Whether state law requires private insurers and/or Medicaid to reimburse telehealth services at parity with in-person services. Coded as: None (no parity), Private only, Medicaid only, or Both. Many expanded during COVID-19; some expired.
- **Baseline:** 40 states + DC have some form of parity as of 2024 (27 both, 9 private only, 4 Medicaid only). 10 states have no parity requirement. Source: CCHP.
- **Data Source:** Center for Connected Health Policy (CCHP) State Telehealth Laws and Reimbursement Policies database, updated quarterly. State-level.

### Node 10: Certificate of Need (CON) Law Stringency
- **Scale:** 1
- **Domain:** Healthcare System
- **Type:** Policy
- **Unit:** Index 0-10 (higher = more stringent)
- **Description:** State-level index of Certificate of Need law stringency, measuring: services covered (hospital beds, MRI, ambulatory surgery, etc.), dollar thresholds for review, criteria stringency, and approval rates. CON laws require state approval before healthcare facility expansion. Composite 0-10 scale.
- **Baseline:** 35 states + DC have some CON regulations as of 2024. Index median = 4.5. Range: 0 (no CON: 15 states) to 9.2 (NY, WV very stringent). Source: Mercatus Center analysis.
- **Data Source:** Mercatus Center CON Database, National Conference of State Legislatures (NCSL). State-level, updated with legislation.

---

## 1.2 HOUSING POLICY

### Node 11: Rent Control / Stabilization Policy Strength
- **Scale:** 1
- **Domain:** Housing
- **Type:** Policy
- **Unit:** Index 0-10 (higher = stronger rent control)
- **Description:** Composite index of rent control and stabilization laws including: existence of rent caps, vacancy control vs. vacancy decontrol, just-cause eviction linkage, exemptions (new construction, small landlords), and enforcement mechanisms. 0 = no rent control (including states with preemption), 10 = comprehensive strong controls. Measured at state level or for major cities in preemption states.
- **Baseline:** Only 4 states allow local rent control (CA, OR, NY, NJ) + DC. Where allowed, city-level index median = 5.5. Range: 0 (37 states preempt rent control) to 8.5 (some CA cities). Source: Urban Institute analysis.
- **Data Source:** Urban Institute rent control policy database, local ordinances, NMHC state preemption tracking. State and major city-level.

### Node 12: Just-Cause Eviction Protection
- **Scale:** 4
- **Domain:** Housing
- **Type:** Policy
- **Unit:** Categorical: None, Moderate, Strong
- **Description:** Legal requirement that landlords provide a qualifying reason (non-payment, lease violation, owner move-in) to terminate a tenancy, rather than evicting without cause. Coded as: None (no requirement), Moderate (some protections, many exemptions), Strong (comprehensive, few exemptions). Measured at state or local level.
- **Baseline:** 5 states + DC have some state-level just-cause laws (CA, OR, NJ, NH, WA). ~30 cities have local ordinances. Majority of US renters have no protection (None). Source: Eviction Lab, NLIHC.
- **Data Source:** Eviction Lab policy database, National Low Income Housing Coalition (NLIHC) state scorecards, local ordinances. State and city-level.

### Node 13: Public Housing Funding Per Capita
- **Scale:** 1
- **Domain:** Housing
- **Type:** Policy
- **Unit:** Federal dollars per capita per year
- **Description:** Federal appropriations for Public Housing Operating Fund and Capital Fund divided by total US population. Measures federal investment in existing public housing stock maintenance and operations. Does not include vouchers or new construction.
- **Baseline:** $23.4 per capita (FY 2023). Declined from $45 per capita (inflation-adjusted) in 1980. Source: HUD budget, Census population.
- **Data Source:** HUD annual budget appropriations, Census population estimates. Federal-level, annual.

### Node 14: Housing Choice Voucher Coverage Rate
- **Scale:** 4
- **Domain:** Housing
- **Type:** Policy
- **Unit:** Percent of eligible households receiving vouchers
- **Description:** Among households eligible for Housing Choice Vouchers (Section 8) by income (<50% AMI), the percentage actually receiving vouchers. Measures the gap between eligibility and availability due to funding constraints. National and state-level estimates available.
- **Baseline:** 24.6% nationally (2022). Only 1 in 4 eligible households receive vouchers. State range: 15% (TX) to 42% (MA, DC). Source: CBPP analysis of HUD data.
- **Data Source:** HUD Picture of Subsidized Households, ACS income data for eligibility estimates. Center on Budget and Policy Priorities (CBPP) analyses. State and metro-level, annual.

### Node 15: Inclusionary Zoning Policy Prevalence
- **Scale:** 1
- **Domain:** Housing
- **Type:** Policy
- **Unit:** Percent of jurisdictions with inclusionary zoning in state
- **Description:** Percentage of municipalities within a state that have inclusionary zoning ordinances requiring or incentivizing affordable units in new residential development. Reflects state enabling legislation and local adoption. Voluntary vs. mandatory programs coded separately if tracked.
- **Baseline:** ~25% of large jurisdictions (>50k pop) nationwide have some form of inclusionary zoning (2023). Concentrated in CA, MA, NJ, CO. Source: Grounded Solutions Network.
- **Data Source:** Grounded Solutions Network Inclusionary Housing Database, local ordinances. State and city-level, updated periodically.

### Node 16: Single-Family Zoning Restriction Prevalence
- **Scale:** 6
- **Domain:** Housing
- **Type:** Policy
- **Unit:** Percent of residentially zoned land restricted to single-family
- **Description:** Percentage of residentially zoned land within a jurisdiction that is zoned exclusively for single-family detached housing, prohibiting duplexes, townhouses, and multifamily. Measure of exclusionary zoning. Requires GIS analysis of zoning maps.
- **Baseline:** ~75% of residentially zoned land in large metros is single-family exclusive (2020). Range: 45% (Minneapolis, after reform) to 95% (many suburban jurisdictions). Source: Furman Center, local analyses.
- **Data Source:** Local zoning maps (GIS), research analyses (e.g., Berkeley Terner Center, NYU Furman Center). City and metro-level, updated with zoning reforms.

### Node 17: Source of Income Discrimination Protection
- **Scale:** 1
- **Domain:** Housing
- **Type:** Policy
- **Unit:** Categorical: None, Limited, Comprehensive
- **Description:** Whether state or local law prohibits landlords from discriminating against tenants based on source of income (vouchers, disability benefits, etc.). Coded as: None (no protection), Limited (some protections with exemptions), Comprehensive (broad coverage, strong enforcement). Measured at state or local level.
- **Baseline:** 20 states + DC have some state-level protection (2024). ~100 localities have local ordinances. Majority of renters have no protection. Source: Poverty & Race Research Action Council (PRRAC).
- **Data Source:** Poverty & Race Research Action Council (PRRAC) Source of Income Laws database, local ordinances. State and city-level.

### Node 18: Eviction Legal Representation Right
- **Scale:** 4
- **Domain:** Housing
- **Type:** Policy
- **Unit:** Categorical: None, Partial, Universal right to counsel
- **Description:** Whether tenants have a legal right to free representation in eviction proceedings. Coded as: None (no right), Partial (right for some groups, e.g., low-income, or in some jurisdictions), Universal (all tenants in eviction proceedings). Measured at state or city level.
- **Baseline:** 4 jurisdictions have universal right to counsel (NYC, SF, Newark, CT statewide) as of 2024. ~15 cities have partial programs. Most of US has no right. Source: National Coalition for a Civil Right to Counsel.
- **Data Source:** National Coalition for a Civil Right to Counsel (NCCRC) Right to Counsel tracker, local legislation. State and city-level.

### Node 19: Eviction Filing Fee
- **Scale:** 4
- **Domain:** Housing
- **Type:** Policy
- **Unit:** Dollars (filing fee for landlord to file eviction)
- **Description:** The court filing fee a landlord must pay to initiate an eviction case. Low fees may incentivize frivolous or retaliatory filings. State and local court fees vary widely. Median value reported for state.
- **Baseline:** Median state = $95 (2023). Range: $15 (AR) to $450 (CA, some counties). Source: Eviction Lab, state court fee schedules.
- **Data Source:** Eviction Lab policy database, state and local court fee schedules. State and county-level.

### Node 20: Eviction Sealing/Expungement Law
- **Scale:** 1
- **Domain:** Housing
- **Type:** Policy
- **Unit:** Categorical: No sealing, Sealing after dismissal, Automatic sealing
- **Description:** Whether eviction records are sealed or expunged from public records, and under what conditions. Coded as: No sealing (all records public permanently), Sealing after dismissal (only dismissed cases sealed), Automatic sealing (cases sealed after time period or upon request). Eviction records create long-term housing barriers.
- **Baseline:** 7 states have some sealing provisions (CA, CO, CT, IL, NJ, VA, VT) as of 2024. Most states have no sealing (permanent public records). Source: Eviction Lab.
- **Data Source:** Eviction Lab policy database, state statutes. State-level.

---

## 1.3 LABOR AND EMPLOYMENT POLICY

### Node 21: Minimum Wage Level
- **Scale:** 1
- **Domain:** Economic Security, Employment
- **Type:** Policy
- **Unit:** Dollars per hour
- **Description:** The effective minimum wage in a jurisdiction, taking the higher of federal or state/local minimum wage. Does not include tipped minimum wage or training wages. Current statutory rate, not inflation-adjusted.
- **Baseline:** Federal = $7.25/hour (since 2009). State range: $7.25 (federal floor, 20 states) to $16.28 (WA state, 2024). Some cities higher (e.g., Seattle $19.97). Median state = $10.50. Source: DOL, EPI.
- **Data Source:** US Department of Labor Wage and Hour Division, Economic Policy Institute minimum wage tracker. State and city-level, updated with legislation.

### Node 22: Paid Sick Leave Mandate
- **Scale:** 1
- **Domain:** Employment
- **Type:** Policy
- **Unit:** Categorical: None, Limited, Comprehensive
- **Description:** Whether state or local law mandates employer-provided paid sick leave. Coded as: None (no mandate), Limited (covers some employers/workers, modest accrual), Comprehensive (broad coverage, generous accrual, family care included). Measured at state or local level.
- **Baseline:** 16 states + DC have state-level mandates (2024). ~20 cities have local ordinances. Majority of states have no mandate. Typical comprehensive: 1 hour per 30 hours worked. Source: NPWF, NELP.
- **Data Source:** National Partnership for Women & Families (NPWF), National Employment Law Project (NELP) paid leave trackers. State and city-level.

### Node 23: Paid Family Leave Policy Generosity
- **Scale:** 3
- **Domain:** Employment
- **Type:** Policy
- **Unit:** Index 0-10 (higher = more generous)
- **Description:** Composite index of paid family and medical leave programs including: duration (weeks covered), wage replacement rate, eligibility breadth (reasons covered: bonding, caregiving, own illness), coverage (% of workforce), and job protection. 0 = no program, 10 = comprehensive generous program. State-level.
- **Baseline:** 13 states + DC have paid family leave programs as of 2024. Index median (among states with programs) = 6.5. Range: 0 (37 states) to 9.2 (CA, WA comprehensive). Source: NPWF, NCSL.
- **Data Source:** National Partnership for Women & Families (NPWF), National Conference of State Legislatures (NCSL) paid leave database. State-level.

### Node 24: Unemployment Insurance Generosity Index
- **Scale:** 6
- **Domain:** Economic Security, Employment
- **Type:** Policy
- **Unit:** Index 0-10 (higher = more generous)
- **Description:** Composite index of unemployment insurance program generosity including: maximum benefit amount, duration (weeks), earnings replacement rate, eligibility requirements (work history, reason for separation), and waiting period. Standardized 0-10 scale. State-level variation.
- **Baseline:** National median = 5.0. Range: 2.8 (FL: low benefits, strict rules) to 8.5 (MA, NJ: generous benefits, looser rules). Average replacement rate = 45% of prior wages. Source: DOL, CBPP.
- **Data Source:** US Department of Labor UI Data, Center on Budget and Policy Priorities (CBPP) analyses. State-level, annual.

### Node 25: Workers' Compensation Coverage Rate
- **Scale:** 4
- **Domain:** Employment, Occupational Health
- **Type:** Policy
- **Unit:** Percent of workforce covered by workers' comp insurance
- **Description:** Percentage of employed workers covered by workers' compensation insurance, accounting for state-level exemptions (e.g., small employers, agricultural workers, domestic workers, gig workers). Measures breadth of coverage, not generosity.
- **Baseline:** ~92% of workers nationwide covered (2023). Range: 85% (TX: employers can opt out) to 98% (states with few exemptions). Source: NASI, state labor departments.
- **Data Source:** National Academy of Social Insurance (NASI) Workers' Compensation report, state labor departments. State-level, annual.

### Node 26: Workers' Compensation Benefit Adequacy
- **Scale:** 4
- **Domain:** Employment, Occupational Health
- **Type:** Policy
- **Unit:** Average weekly benefit as % of state average wage
- **Description:** The average weekly workers' compensation benefit for temporary total disability as a percentage of the state average weekly wage. Measures generosity of benefits. Most states target ~66% wage replacement but vary in caps and calculation methods.
- **Baseline:** National median = 62% (2023). Range: 48% (AL, MS: low caps) to 75% (IA, DE: generous). Source: NASI.
- **Data Source:** National Academy of Social Insurance (NASI) Workers' Compensation report. State-level, annual.

### Node 27: Right-to-Work Law Status
- **Scale:** 1
- **Domain:** Employment, Labor
- **Type:** Policy
- **Unit:** Binary (0=not right-to-work, 1=right-to-work)
- **Description:** Whether a state has a right-to-work law prohibiting union security agreements that require workers to pay union dues or fees as a condition of employment. Binary indicator. Right-to-work laws weaken union power and reduce membership.
- **Baseline:** 27 states have right-to-work laws as of 2024 (mostly Southern and Mountain West states). 23 states + DC do not. Source: NCSL, NRTW.
- **Data Source:** National Conference of State Legislatures (NCSL), National Right to Work Legal Defense Foundation. State-level.

### Node 28: Union Density Rate [REVISED - Consolidated with Node 113]
- **Scale:** 1
- **Domain:** Employment, Labor
- **Type:** Rate
- **Unit:** Percent of wage and salary workers who are union members
- **Description:** The percentage of employed wage and salary workers who report union membership in a geographic area (state, metro, or county). Reflects union density and collective bargaining power. Influenced by right-to-work laws, industrial composition, and organizing climate. Can be measured at state level for policy analysis or metro/county level for local labor market effects. Distinct from individual union membership (Node 326).
- **Baseline:** 10.0% nationally (2023). State range: 2.9% (SC) to 23.1% (HI). Metro range: 3% (Southern metros) to 22% (NYC, SF). Highest in public sector (32.5%) vs. private (6.0%). Declining from 20.1% in 1983. Source: BLS.
- **Data Source:** Bureau of Labor Statistics (BLS) Current Population Survey Union Membership Supplement, annual. State and metro-level. EPI provides metro estimates.
- **Consolidation Note:** Replaces former Node 113 "Labor Union Density (Local)" which measured identical concept at metro/county level. Now single node works at multiple geographic scales.
- **Mechanism node_id:** `union_density_rate`
- **Data Source:** Bureau of Labor Statistics (BLS) Current Population Survey Union Membership Supplement, annual. State-level.

### Node 29: Occupational Licensing Stringency
- **Scale:** 1
- **Domain:** Employment
- **Type:** Policy
- **Unit:** Percent of workforce in occupations requiring license
- **Description:** The percentage of workers employed in occupations that require a state-issued occupational license to practice. Measures extent of licensing regulation. Includes professional, trade, and service occupations. Does not measure stringency per se (education, exam requirements) but breadth.
- **Baseline:** ~22% of US workforce in licensed occupations (2023). State range: 12% to 33%. Most common: healthcare, education, legal, cosmetology, construction trades. Source: NCSL, Brookings analyses.
- **Data Source:** National Conference of State Legislatures (NCSL), research analyses (e.g., Kleiner & Krueger), state licensing boards. State-level estimates, periodic updates.

### Node 30: Ban-the-Box Policy Adoption
- **Scale:** 1
- **Domain:** Employment, Criminal Justice
- **Type:** Policy
- **Unit:** Categorical: None, Public employers only, Private employers included
- **Description:** Whether state or local law prohibits employers from asking about criminal history on job applications ("ban the box"), delaying inquiry until later in hiring. Coded as: None, Public employers only, or Private employers included. Aims to reduce employment barriers for people with records.
- **Baseline:** 37 states + DC have some ban-the-box policy (2024). 13 states: Public only. 11 states: Includes private employers. ~150 cities/counties have local ordinances. Source: NELP.
- **Data Source:** National Employment Law Project (NELP) Ban the Box tracker, local ordinances. State and city-level.

### Node 31: Non-Compete Agreement Restrictions
- **Scale:** 4
- **Domain:** Employment
- **Type:** Policy
- **Unit:** Categorical: Fully enforceable, Limited restrictions, Banned/Unenforceable
- **Description:** State-level restrictions on employer use of non-compete agreements that restrict worker mobility. Coded as: Fully enforceable (minimal restrictions), Limited restrictions (e.g., salary thresholds, duration limits), or Banned/Unenforceable (CA, ND, OK). Affects worker bargaining power and wages.
- **Baseline:** 3 states ban non-competes (CA, ND, OK). ~15 states have significant restrictions (salary thresholds, duration limits). ~32 states fully enforce with minimal restrictions. Source: Beck Reed Riden, EPI.
- **Data Source:** Beck Reed Riden law firm analysis, Economic Policy Institute, state statutes. State-level. Federal FTC ban proposed 2023 (pending).

### Node 32: Wage Theft Enforcement Strength
- **Scale:** 4
- **Domain:** Employment, Economic Security
- **Type:** Policy
- **Unit:** Index 0-10 (higher = stronger enforcement)
- **Description:** Composite index of state wage theft enforcement including: treble damages availability, criminal penalties, agency enforcement resources, retaliation protections, and misclassification penalties. 0 = weak (civil only, no agency), 10 = strong (criminal penalties, well-funded labor dept). Wage theft = employer failure to pay earned wages.
- **Baseline:** National median = 4.5. Range: 1.5 (states with no labor department enforcement) to 9.0 (CA, NY with strong enforcement and criminal penalties). Source: NELP, Economic Policy Institute analyses.
- **Data Source:** National Employment Law Project (NELP), Economic Policy Institute, state labor department reports. State-level.

### Node 33: Gig Worker Classification Laws
- **Scale:** 1
- **Domain:** Employment
- **Type:** Policy
- **Unit:** Categorical: ABC test, Multifactor test, Gig carve-out
- **Description:** State standard for determining whether a worker is an employee (entitled to protections) vs. independent contractor. Coded as: ABC test (strict, presumption of employment), Multifactor test (looser, common law), or Gig carve-out (special exemptions for app-based workers). Affects access to minimum wage, UI, workers' comp.
- **Baseline:** ~20 states use ABC test for UI or wage claims. Majority use multifactor test. CA passed gig carve-out (Prop 22, 2020). Source: NELP, NCSL.
- **Data Source:** National Employment Law Project (NELP), National Conference of State Legislatures (NCSL), state statutes. State-level.

---

## 1.3a CRIME AND COMMUNITY SAFETY [NEW SECTION - Added to fill mechanism gap]

### Node 100: Violent Crime Rate [NEW - Added to fill mechanism gap]
- **Scale:** 4
- **Domain:** Criminal Justice, Social Environment, Public Safety
- **Type:** Rate
- **Unit:** Violent crimes per 100,000 population per year
- **Description:** FBI Uniform Crime Reporting (UCR) violent crime rate: murder/nonnegligent manslaughter, rape, robbery, and aggravated assault offenses known to police per 100,000 population annually. Structural measure of community violence. Does not capture unreported crime (substantial undercount for sexual assault). Geographic variation reflects policing practices, economic conditions, structural inequality, and neighborhood factors. Crime reporting is voluntary and inconsistent across jurisdictions.
- **Baseline:** 380 per 100,000 nationally (2022). Range: 115 (ME, VT) to 885 (DC, LA, AK high rates). Down from peak 758 in 1991 but uptick 2020-2022. Crime concentrated in certain neighborhoods within cities - zip code variation much larger than state variation.
- **Data Source:** FBI Uniform Crime Reporting (UCR) Program, National Incident-Based Reporting System (NIBRS). State, county, city-level, annual. Transition from UCR to NIBRS ongoing (reporting gaps).
- **Mechanism node_id:** `violent_crime_rate`
- **Consolidation Note:** Previously missing from inventory but referenced in mechanisms linking violence exposure to mental health, stress, and child outcomes.

### Node 101: Property Crime Rate [NEW - Added for completeness]
- **Scale:** 5
- **Domain:** Criminal Justice, Social Environment, Economic Security
- **Type:** Rate
- **Unit:** Property crimes per 100,000 population per year
- **Description:** FBI UCR property crime rate: burglary, larceny-theft, motor vehicle theft, and arson per 100,000 population annually. Reflects economic stress, housing instability, substance use, community cohesion, and opportunity structures. Property crime rates are 5-6x higher than violent crime rates.
- **Baseline:** 1,954 per 100,000 nationally (2022). Range: 850 (Northeast states) to 3,500 (Western states, tourist areas). Declining from peak 5,140 in 1991. Substantial underreporting (many property crimes not reported to police).
- **Data Source:** FBI UCR/NIBRS. State, county, city-level, annual.
- **Mechanism node_id:** `property_crime_rate`
- **Consolidation Note:** Added for structural completeness alongside violent crime. Relevant for economic stress and neighborhood disorder mechanisms.

---

## 1.4 CRIMINAL JUSTICE POLICY

### Node 34: Incarceration Rate
- **Scale:** 7 (could be Individual, but treated as structural for macro prison policy effects)
- **Domain:** Criminal Justice
- **Type:** Rate
- **Unit:** Prisoners per 100,000 population (state prisons + local jails)
- **Description:** Combined incarceration rate including state prisons and local jails per 100,000 state population. Reflects sentencing severity, policing intensity, and use of incarceration. Includes pre-trial detention and sentenced inmates. Does not include federal prisons or ICE detention.
- **Baseline:** 664 per 100,000 nationally (2023). Range: 270 (MA) to 1,130 (MS). US rate is ~5x higher than most developed nations. Declined from peak of 755 in 2008. Source: Vera Institute, Prison Policy Initiative.
- **Data Source:** Vera Institute of Justice Incarceration Trends dataset, Bureau of Justice Statistics. State and county-level, annual.

### Node 35: Mandatory Minimum Sentencing Prevalence
- **Scale:** 1
- **Domain:** Criminal Justice
- **Type:** Policy
- **Unit:** Index 0-10 (higher = more prevalent mandatory minimums)
- **Description:** Index of prevalence and severity of mandatory minimum sentencing laws across offense categories (drug, violent, weapons, repeat offender enhancements). Measures scope of judicial discretion removal. 0 = few/no mandatory minimums, 10 = extensive across many offenses. State-level.
- **Baseline:** National median = 6.0. Range: 2.5 (states that have repealed most mandatory minimums) to 9.5 (FL, VA extensive). Federal system = 7.5. Source: Families Against Mandatory Minimums (FAMM), Sentencing Project.
- **Data Source:** Families Against Mandatory Minimums (FAMM) state law database, The Sentencing Project, state sentencing commissions. State-level.

### Node 36: Drug Decriminalization/Defelonization Status
- **Scale:** 1
- **Domain:** Criminal Justice, Substance Use
- **Type:** Policy
- **Unit:** Categorical: Fully criminalized, Marijuana decrim, Marijuana legal, Broader decrim
- **Description:** State policy on drug possession penalties. Coded as: Fully criminalized (all drugs criminal), Marijuana decriminalized (small possession civil fine), Marijuana legalized (recreational sale legal), or Broader decriminalization (additional drugs decriminalized, e.g., OR Measure 110). Affects incarceration, arrest records, health access.
- **Baseline:** Marijuana: 27 states decriminalized/medicalized, 24 states + DC legalized recreational (2024). Broader decrim: OR (2020-2024), some cities (e.g., Philadelphia). Source: NORML, Drug Policy Alliance.
- **Data Source:** NORML state law database, Drug Policy Alliance, Marijuana Policy Project. State-level.

### Node 37: Cash Bail Reform Status
- **Scale:** 3
- **Domain:** Criminal Justice, Economic Security
- **Type:** Policy
- **Unit:** Categorical: Cash bail default, Risk assessment, Eliminated for most offenses
- **Description:** State/local policy on pre-trial detention and bail. Coded as: Cash bail default (money bail widely used), Risk assessment (shift to risk-based detention, may retain cash bail option), or Eliminated (cash bail ended for most misdemeanors/non-violent felonies). Affects pre-trial detention, which impacts health, employment, housing.
- **Baseline:** 4 states have largely eliminated cash bail (NJ, NY, IL, CA). ~10 states use risk assessment. Majority still use cash bail as default. Source: Pretrial Justice Institute, Bail Project.
- **Data Source:** Pretrial Justice Institute state profiles, The Bail Project, state judiciary rules. State and county-level (varies by jurisdiction).

### Node 38: Three Strikes / Habitual Offender Law Stringency
- **Scale:** 1
- **Domain:** Criminal Justice
- **Type:** Policy
- **Unit:** Index 0-10 (higher = more stringent)
- **Description:** Index of three strikes and habitual offender sentencing enhancements including: number of priors to trigger (2 vs. 3), offense types covered (violent only vs. any felony), mandatory life without parole, and scope. 0 = no habitual offender enhancements, 10 = strict three strikes with life without parole. State-level.
- **Baseline:** 28 states have some form of three strikes or habitual offender law. Index median (among states with laws) = 5.5. Range: 0 (no law, 22 states) to 9.5 (CA original three strikes, pre-2012 reform; GA). Source: The Sentencing Project, FAMM.
- **Data Source:** The Sentencing Project, Families Against Mandatory Minimums (FAMM), state statutes. State-level.

### Node 39: Juvenile Justice Transfer Laws Stringency
- **Scale:** 1
- **Domain:** Criminal Justice, Child Welfare
- **Type:** Policy
- **Unit:** Index 0-10 (higher = easier transfer to adult court)
- **Description:** Index of ease of transferring juveniles to adult criminal court including: automatic transfer offenses, judicial waiver age thresholds, prosecutor direct file authority, and reverse waiver availability. 0 = narrow transfer, strong juvenile court jurisdiction; 10 = broad automatic transfer, low age thresholds. State-level.
- **Baseline:** National median = 5.0. Range: 1.5 (states with high age thresholds, narrow categories) to 9.0 (states with broad automatic transfer, prosecutor direct file for ages 13-14). Source: Campaign for Youth Justice, NCJFCJ.
- **Data Source:** Campaign for Youth Justice, National Center for Juvenile and Family Court Judges (NCJFCJ), state statutes. State-level.

### Node 40: Felon Disenfranchisement Stringency
- **Scale:** 4
- **Domain:** Criminal Justice, Civic Engagement
- **Type:** Policy
- **Unit:** Categorical: No restriction, Incarcerated only, Parole/probation included, Permanent for some
- **Description:** State restrictions on voting rights for people with felony convictions. Coded as: No restriction (vote during incarceration, ME/VT), Incarcerated only (rights restored upon release), Parole/probation included (rights suspended during supervision), or Permanent for some felonies (requires action to restore, AL, FL, etc.). Affects civic engagement and community power.
- **Baseline:** 2 states allow incarcerated voting. 23 states restrict during incarceration only. 13 states restrict during parole/probation. 11 states have permanent or long-term disenfranchisement. Affects ~4.6M people. Source: The Sentencing Project.
- **Data Source:** The Sentencing Project Felony Disenfranchisement database, Brennan Center, state election laws. State-level.

### Node 41: Civil Asset Forfeiture Reform Status
- **Scale:** 1
- **Domain:** Criminal Justice, Economic Security
- **Type:** Policy
- **Unit:** Index 0-10 (higher = stronger protections against forfeiture)
- **Description:** Index of civil asset forfeiture protections including: burden of proof standard (preponderance vs. clear and convincing vs. criminal conviction required), innocent owner protections, and limits on law enforcement retention of proceeds. 0 = low standard, agencies keep proceeds; 10 = conviction required, proceeds to general fund. State-level.
- **Baseline:** National median = 4.0. Range: 1.0 (weak protections, agencies incentivized) to 9.5 (NM, NE: conviction required, proceeds to schools). Source: Institute for Justice Policing for Profit report.
- **Data Source:** Institute for Justice Policing for Profit report (updated every 2-3 years), state statutes. State-level.

### Node 42: Police Accountability Law Strength
- **Scale:** 1
- **Domain:** Criminal Justice, Social Environment
- **Type:** Policy
- **Unit:** Index 0-10 (higher = stronger accountability)
- **Description:** Composite index of police accountability laws including: duty to intervene, use of force restrictions, chokehold bans, no-knock warrant limits, body camera requirements, civilian oversight, qualified immunity reform, and decertification for misconduct. 0 = minimal accountability, 10 = comprehensive reforms. State-level.
- **Baseline:** National median = 3.5 (as of 2024, post-2020 protests led to reforms). Range: 1.0 (minimal regulation) to 8.0 (CA, CO, CT with comprehensive post-2020 reforms). Source: ACLU, Campaign Zero, NCSL tracking.
- **Data Source:** ACLU police accountability tracker, Campaign Zero #8CantWait tracker, National Conference of State Legislatures (NCSL) police reform database. State-level.

---

## 1.5 EDUCATION AND CHILD WELFARE POLICY

### Node 43: Early Childhood Education (Pre-K) Access Funding Per Capita
- **Scale:** 1
- **Domain:** Education, Child Welfare
- **Type:** Policy
- **Unit:** State dollars per child age 3-4 per year
- **Description:** State spending on pre-kindergarten programs divided by the total population of 3- and 4-year-olds. Measures state investment in early childhood education access. Does not include Head Start (federal) or private preschool. Reflects funding availability, not enrollment.
- **Baseline:** National median = $1,100 per child age 3-4 (2023). Range: $0 (6 states with no state pre-K program) to $6,500 (DC, NJ, VT with universal pre-K). Source: NIEER State of Preschool Yearbook.
- **Data Source:** National Institute for Early Education Research (NIEER) State of Preschool Yearbook, annual. State-level.

### Node 44: Child Tax Credit Generosity (State Supplement)
- **Scale:** 1
- **Domain:** Economic Security, Child Welfare
- **Type:** Policy
- **Unit:** Maximum state credit dollars per child per year
- **Description:** Maximum value of state-level child tax credit (supplementing federal CTC). Measures state income support for families with children. Coded as $0 for states with no state CTC. Some fully refundable, some not (note in description). Does not include federal CTC.
- **Baseline:** 14 states have state-level CTC (2024). Median among states with credit = $500 per child. Range: $0 (36 states) to $1,800 (CA, VT, CO with generous refundable credits). Source: CBPP, ITEP.
- **Data Source:** Center on Budget and Policy Priorities (CBPP), Institute on Taxation and Economic Policy (ITEP) state tax credits database. State-level, annual.

### Node 45: SNAP Maximum Benefit Supplement
- **Scale:** 1
- **Domain:** Food Security, Economic Security
- **Type:** Policy
- **Unit:** Percent supplement above federal SNAP maximum
- **Description:** Percentage by which state SNAP benefits exceed federal maximum (via state supplements or waivers). Most states provide only federal maximum (0% supplement). A few states provide supplements for specific populations (elderly, disabled). Coded as % above federal max.
- **Baseline:** 3 states provide SNAP supplements (CA, HI, WI, historically). Median = 0% (47 states provide federal max only). Supplement range: 0% to 15% (HI for elderly/disabled). Source: CBPP, FNS.
- **Data Source:** Center on Budget and Policy Priorities (CBPP), USDA Food and Nutrition Service (FNS) state options report. State-level.

### Node 46: TANF Benefit Adequacy
- **Scale:** 1
- **Domain:** Economic Security, Child Welfare
- **Type:** Policy
- **Unit:** Maximum TANF benefit for family of 3 as % of federal poverty line
- **Description:** The maximum monthly TANF (Temporary Assistance for Needy Families) cash benefit for a family of three with no other income, expressed as a percentage of the federal poverty line. Measures cash assistance adequacy for poorest families. State-level variation.
- **Baseline:** National median = 22% of FPL (2023). Range: 10% (MS: $146/month) to 47% (NH, VT: $700-800/month). No state provides benefits above 50% FPL. Benefits have eroded significantly since 1996 welfare reform. Source: CBPP.
- **Data Source:** Center on Budget and Policy Priorities (CBPP) TANF state fact sheets, HHS Administration for Children and Families (ACF) data. State-level, annual.

### Node 47: TANF Work Requirement Stringency
- **Scale:** 1
- **Domain:** Economic Security, Child Welfare, Employment
- **Type:** Policy
- **Unit:** Index 0-10 (higher = more stringent)
- **Description:** Index of TANF work requirement stringency including: hours per week required, activities that count as work, exemptions (child age, caregiving, disability), time limits, and sanction severity. 0 = minimal requirements/generous exemptions, 10 = strict requirements/harsh sanctions. Federal baseline exists; state variation. State-level.
- **Baseline:** National median = 6.0. Range: 3.5 (states with broad exemptions, lenient sanctions) to 9.0 (states with strict hours, narrow exemptions, immediate full-family sanctions). Source: CBPP, Urban Institute TANF policy database.
- **Data Source:** Center on Budget and Policy Priorities (CBPP), Urban Institute TANF policy database, state TANF plans. State-level.

### Node 48: School Funding Equity (Progressivity) Index
- **Scale:** 3
- **Domain:** Education
- **Type:** Policy
- **Unit:** Index 0-10 (higher = more progressive/equitable)
- **Description:** Index of school funding equity measuring whether high-poverty districts receive more, equal, or less funding than low-poverty districts within a state. Combines: funding level, progressivity (extra for high-poverty), funding sources (state vs. local property tax reliance), and adequacy. 0 = regressive (high-poverty districts get less), 5 = flat, 10 = highly progressive. State-level.
- **Baseline:** National median = 4.8 (slightly regressive nationally). Range: 2.0 (states where high-poverty districts get 70% of what low-poverty get) to 8.5 (states with strong progressive formulas, NJ, MA). Source: Education Law Center, The Education Trust.
- **Data Source:** Education Law Center Making the Grade report (annual), The Education Trust Funding Gaps report, state education finance data. State-level.

### Node 49: Universal School Meals Policy
- **Scale:** 1
- **Domain:** Food Security, Education
- **Type:** Policy
- **Unit:** Categorical: None, Free for low-income only (federal), Free for all (universal)
- **Description:** Whether state policy provides free school meals (breakfast and lunch) for all students regardless of income. Coded as: None (no state policy, relying on federal income-based), Federal only (free/reduced based on income), or Universal (state funds free meals for all). Reduces food insecurity and stigma.
- **Baseline:** 9 states have universal free school meals as of 2024 (CA, ME, MA, MI, MN, NM, CO, VT, NV). Federal program provides free/reduced based on income (41 states). Source: FRAC, state legislation.
- **Data Source:** Food Research & Action Center (FRAC), state education departments, state legislation. State-level.

### Node 50: School Discipline Disparity Oversight
- **Scale:** 1
- **Domain:** Education, Criminal Justice
- **Type:** Policy
- **Unit:** Categorical: No oversight, Data reporting required, Disparity reduction mandates
- **Description:** State oversight of school discipline disparities by race/ethnicity/disability. Coded as: No oversight (no requirements), Data reporting required (districts must report suspension/expulsion by demographics), or Disparity reduction mandates (state requires action plans to reduce disparities). Aims to address school-to-prison pipeline.
- **Baseline:** 15 states require disparity data reporting (2024). 5 states require reduction action plans (CA, CT, MA). Majority have no oversight. Federal CRDC collects data but doesn't mandate state action. Source: ACLU, Education Commission of the States.
- **Data Source:** ACLU school discipline tracker, Education Commission of the States policy database, state education department regulations. State-level.

---

## 1.6 ENVIRONMENTAL AND CLIMATE POLICY

### Node 51: Clean Air Act Enforcement Stringency
- **Scale:** 4
- **Domain:** Environmental, Built Environment
- **Type:** Policy
- **Unit:** Index 0-10 (higher = more stringent)
- **Description:** Federal and state enforcement stringency of Clean Air Act standards, measured by: ambient air quality standards stringency, state implementation plan (SIP) strength, enforcement actions per violation, penalties, and monitoring density. 0 = minimal enforcement, 10 = aggressive enforcement exceeding federal standards. State-level variation.
- **Baseline:** National median = 5.5. Range: 2.0 (states with weak enforcement, industry accommodation) to 9.0 (CA with strict standards, aggressive enforcement). Source: EPA, EDF scorecards.
- **Data Source:** EPA Enforcement and Compliance History Online (ECHO), Environmental Defense Fund (EDF) state scorecards, state air quality agencies. State-level, annual.

### Node 52: Lead Abatement Policy Strength
- **Scale:** 1
- **Domain:** Environmental, Housing
- **Type:** Policy
- **Unit:** Index 0-10 (higher = stronger policy)
- **Description:** Composite index of state lead poisoning prevention policy including: blood lead screening requirements, lead safe housing laws, landlord disclosure mandates, proactive inspection programs, lead pipe replacement mandates, funding for abatement, and enforcement. 0 = minimal regulation, 10 = comprehensive proactive prevention. State-level.
- **Baseline:** National median = 4.0. Range: 1.5 (no state-level requirements beyond federal) to 8.5 (MD, RI, MA with comprehensive programs). Source: National Center for Healthy Housing (NCHH), CDC childhood lead policy database.
- **Data Source:** National Center for Healthy Housing (NCHH), CDC Childhood Lead Poisoning Prevention Program, state health departments. State-level.

### Node 53: Environmental Justice Screening Tool Adoption
- **Scale:** 1
- **Domain:** Environmental, Social Environment
- **Type:** Policy
- **Unit:** Categorical: No tool, Tool exists, Tool mandated for decision-making
- **Description:** Whether state has adopted an environmental justice screening tool to identify overburdened communities and whether its use is mandated in permitting/funding decisions. Coded as: No tool, Tool exists (informational), or Tool mandated (triggers enhanced review, community benefits). Examples: CalEnviroScreen, EJSCREEN.
- **Baseline:** ~25 states have developed EJ screening tools (2024). 10 states mandate use in decisions (CA, NJ, WA, etc.). 25 states have no tool. Source: EPA, state environmental agencies.
- **Data Source:** EPA EJ resources, state environmental agency websites, Environmental Law Institute tracking. State-level.

### Node 54: Climate Adaptation Funding Per Capita
- **Scale:** 1
- **Domain:** Environmental, Climate, Infrastructure
- **Type:** Policy
- **Unit:** State dollars per capita per year for climate adaptation
- **Description:** State appropriations for climate adaptation and resilience (excluding mitigation/emissions reduction) divided by state population. Includes: flood infrastructure, heat response, drought preparedness, wildfire prevention, coastal protection. Does not include federal disaster relief.
- **Baseline:** National median = $8 per capita (2023). Range: $0 (many states with no dedicated funding) to $95 per capita (CA, FL with major adaptation investments). Source: Georgetown Climate Center, state budgets.
- **Data Source:** Georgetown Climate Center state adaptation tracking, state budget appropriations analysis. State-level, annual.

### Node 55: Renewable Portfolio Standard (RPS) Stringency
- **Scale:** 4
- **Domain:** Environmental, Climate
- **Type:** Policy
- **Unit:** Percent of electricity from renewables required by target year
- **Description:** State renewable portfolio standard target: percentage of electricity generation that must come from renewable sources by a specified year. Measures commitment to clean energy transition. Coded as target % and year. If no RPS, coded as 0%.
- **Baseline:** 30 states + DC have RPS or clean energy standards (2024). Median target = 50% by 2030. Range: 0% (20 states with no RPS) to 100% by 2040 (CA, HI, NM, VA, WA). Source: NCSL, DSIRE.
- **Data Source:** National Conference of State Legislatures (NCSL), Database of State Incentives for Renewables & Efficiency (DSIRE). State-level.

### Node 56: Carbon Pricing/Cap-and-Trade Policy
- **Scale:** 4
- **Domain:** Environmental, Climate
- **Type:** Policy
- **Unit:** Categorical: None, Carbon tax, Cap-and-trade
- **Description:** Whether state has implemented carbon pricing mechanism. Coded as: None (no carbon price), Carbon tax (explicit $/ton CO2), or Cap-and-trade (emissions trading system). Only a few US states; regional initiatives (RGGI, CA). Affects energy costs and emissions.
- **Baseline:** 1 state carbon tax (WA). 2 cap-and-trade programs: CA (state), RGGI (11 Northeast states). 47 states have no carbon pricing. Source: World Bank Carbon Pricing Dashboard, state agencies.
- **Data Source:** World Bank Carbon Pricing Dashboard, Regional Greenhouse Gas Initiative (RGGI), California Air Resources Board (CARB), state legislation. State-level.

### Node 57: Flood Risk Disclosure Requirements
- **Scale:** 4
- **Domain:** Environmental, Climate, Housing
- **Type:** Policy
- **Unit:** Categorical: No requirement, FEMA zones only, Comprehensive (includes future risk)
- **Description:** Whether state requires disclosure of flood risk in real estate transactions. Coded as: No requirement, FEMA zones only (current 100-year floodplain), or Comprehensive (includes future climate-adjusted risk, past flooding). Affects housing decisions and disaster preparedness.
- **Baseline:** ~20 states require some flood disclosure (2024). Most require FEMA zones only. 5 states require past flood history (CA, IL, TX, NC, SC). 1 state requires future risk (CT). 30 states have no requirement. Source: NRDC, state real estate law.
- **Data Source:** Natural Resources Defense Council (NRDC) flood disclosure analysis, state real estate disclosure laws. State-level.

### Node 58: Heat Action Plan Existence
- **Scale:** 4
- **Domain:** Environmental, Climate, Public Health
- **Type:** Policy
- **Unit:** Binary (0=no plan, 1=plan exists)
- **Description:** Whether state or major city has adopted a heat action plan with protocols for extreme heat events, including: heat warning systems, cooling center activation, vulnerable population outreach, and utility shutoff moratoria during heat waves. Binary indicator at state or city level.
- **Baseline:** ~30 states or major cities have heat action plans (2024), concentrated in Southwest, Southeast, and urban areas. Plans vary widely in comprehensiveness. Source: CDC BRACE program, C40 Cities.
- **Data Source:** CDC Building Resilience Against Climate Effects (BRACE) program, C40 Cities Climate Leadership Group, state/city emergency management plans. State and major city-level.

### Node 59: Water Quality Regulation Stringency (PFAS, etc.)
- **Scale:** 2
- **Domain:** Environmental, Public Health
- **Type:** Policy
- **Unit:** Index 0-10 (higher = more stringent)
- **Description:** Index of state drinking water quality standards beyond federal Safe Drinking Water Act, focusing on emerging contaminants (PFAS, 1,4-dioxane, chromium-6, microplastics). Measures: contaminants regulated, MCL stringency vs. federal, testing requirements, public notification, remediation mandates. 0 = federal standards only, 10 = comprehensive state standards. State-level.
- **Baseline:** National median = 3.0. Range: 0 (federal only, ~30 states) to 8.5 (MI, NH, NJ, CA with strict PFAS standards). Source: EWG, EPA, Environmental Law Institute.
- **Data Source:** Environmental Working Group (EWG) Tap Water Database, EPA SDWA tracking, Environmental Law Institute state law database. State-level.

### Node 60: Pesticide Regulation Stringency
- **Scale:** 1
- **Domain:** Environmental, Occupational Health, Public Health
- **Type:** Policy
- **Unit:** Index 0-10 (higher = more stringent)
- **Description:** Index of state pesticide regulation stringency including: restricted pesticides beyond federal (EPA), buffer zones (schools, residences), notification requirements, licensing stringency, enforcement, and farmworker protections. 0 = federal only, 10 = comprehensive state restrictions. State-level.
- **Baseline:** National median = 4.5. Range: 1.0 (minimal state regulation) to 9.0 (CA with extensive restrictions, worker protections). Source: Pesticide Action Network, EPA, state agriculture departments.
- **Data Source:** Pesticide Action Network, EPA state pesticide program tracking, state agriculture/environmental agencies. State-level.

---

## 1.7 INFRASTRUCTURE INVESTMENT POLICY

### Node 61: Public Transit Operating Funding Per Capita
- **Scale:** 2
- **Domain:** Transportation, Infrastructure
- **Type:** Policy
- **Unit:** Combined federal and state dollars per capita per year
- **Description:** Combined federal and state funding for public transit operations (not capital) divided by state population. Measures ongoing support for transit service. Does not include local funding or fare revenue. Reflects accessibility of transit, particularly for low-income populations.
- **Baseline:** National median = $45 per capita (2023). Range: $2 (rural states with minimal transit) to $350+ (NY, DC with extensive systems). Source: FTA National Transit Database, state budgets.
- **Data Source:** FTA National Transit Database, state transportation department budgets, APTA analyses. State and metro-level, annual.

### Node 62: Active Transportation Infrastructure Investment
- **Scale:** 1
- **Domain:** Transportation, Infrastructure, Built Environment
- **Type:** Policy
- **Unit:** Dollars per capita per year for bike/ped infrastructure
- **Description:** State and federal funding for bicycle and pedestrian infrastructure (bike lanes, sidewalks, trails, crosswalks, bike-share) divided by state population. Measures commitment to active transportation and safe walkable communities.
- **Baseline:** National median = $12 per capita (2023). Range: $2 to $45 (OR, CA, CO with strong programs). Source: Alliance for Biking & Walking, state DOT budgets.
- **Data Source:** Alliance for Biking & Walking Benchmarking Reports, state transportation department budgets, Rails-to-Trails Conservancy. State and metro-level.

### Node 63: Parks and Green Space Investment Per Capita
- **Scale:** 2
- **Domain:** Built Environment, Infrastructure, Environmental
- **Type:** Policy
- **Unit:** State and local dollars per capita per year
- **Description:** Combined state and local government spending on parks, recreation, and green space (operations and capital) divided by population. Measures investment in accessible recreation and nature. Excludes federal lands (national parks).
- **Baseline:** National median = $95 per capita (2023). Range: $40 (lower investment states) to $350+ (high-investment cities like SF, DC). Source: Trust for Public Land City Park Facts, state budgets.
- **Data Source:** Trust for Public Land City Park Facts database (annual), US Census government finance data. City and metro-level, aggregated to state.

### Node 64: Affordable Housing Bond/Trust Fund Capitalization
- **Scale:** 1
- **Domain:** Housing, Infrastructure
- **Type:** Policy
- **Unit:** Dollars in housing trust fund or bond authority per capita
- **Description:** State affordable housing trust fund balance or housing bond authorization amount divided by state population. Measures dedicated state resources for affordable housing development and preservation. Does not include federal funds (HOME, LIHTC).
- **Baseline:** 48 states + DC have housing trust funds (2024), but funding levels vary dramatically. Median capitalization = $15 per capita. Range: $0 (minimal funding) to $200+ per capita (CA, MA with major investments). Source: Center for Community Change, state housing finance agencies.
- **Data Source:** Center for Community Change Housing Trust Fund Project, National Council of State Housing Agencies (NCSHA), state housing finance agency reports. State-level, annual.

### Node 65: Broadband Infrastructure Investment Per Capita
- **Scale:** 1
- **Domain:** Digital Access, Infrastructure
- **Type:** Policy
- **Unit:** State and federal dollars per capita for broadband expansion
- **Description:** Combined state and federal funding for broadband infrastructure expansion (not operations or subsidies) divided by state population. Includes: fiber buildout, rural broadband programs, digital equity grants. Measures commitment to closing digital divide.
- **Baseline:** National median = $50 per capita from recent federal infrastructure bill (IIJA 2021). State supplements range $0-$200 per capita. Source: NTIA, state broadband offices.
- **Data Source:** National Telecommunications and Information Administration (NTIA) BroadbandUSA, state broadband office reports, IIJA funding allocations. State-level.

### Node 66: Water Infrastructure Investment Per Capita
- **Scale:** 1
- **Domain:** Infrastructure, Environmental, Public Health
- **Type:** Policy
- **Unit:** Dollars per capita per year for water/wastewater infrastructure
- **Description:** Combined federal, state, and local investment in drinking water and wastewater infrastructure (treatment plants, pipe replacement, stormwater) divided by population. Critical for lead pipe replacement, PFAS treatment, CSO reduction. Measured via State Revolving Funds and direct appropriations.
- **Baseline:** National median = $180 per capita (2023). Range: $80 to $450 (varies by infrastructure age and state investment). Source: EPA Clean Water SRF, Drinking Water SRF, ASCE infrastructure report card.
- **Data Source:** EPA Clean Water State Revolving Fund (CWSRF), Drinking Water State Revolving Fund (DWSRF), ASCE Infrastructure Report Card. State-level, annual.

### Node 67: School Infrastructure Investment Per Student
- **Scale:** 3
- **Domain:** Education, Infrastructure
- **Type:** Policy
- **Unit:** Dollars per student per year for school facilities
- **Description:** State and local capital spending on K-12 school facilities (construction, renovation, maintenance) divided by student enrollment. Measures investment in safe, healthy learning environments (ventilation, lead abatement, accessibility). Does not include operations.
- **Baseline:** National median = $1,200 per student per year (2023). Range: $400 to $3,500 (varies by state funding role and deferred maintenance needs). Source: US Census school finance survey, 21st Century School Fund.
- **Data Source:** US Census Annual Survey of School System Finances, 21st Century School Fund State of Our Schools reports. State and district-level, annual.

---

## 1.8 TAXATION AND FISCAL POLICY

### Node 68: State Income Tax Progressivity
- **Scale:** 1
- **Domain:** Economic Security, Taxation
- **Type:** Policy
- **Unit:** Index 0-10 (higher = more progressive)
- **Description:** Index of state income tax progressivity measuring: top marginal rate, number of brackets, income level of top bracket, EITC refundability, child tax credits, and effective tax rates by income quintile. 0 = no income tax or flat tax, 10 = highly progressive with generous credits for low-income. State-level.
- **Baseline:** National median = 5.0. Range: 0 (9 states with no income tax: WA, TX, FL, NV, TN, SD, WY, AK, NH) to 9.5 (CA, NY with high top rates and progressive structures). Source: Institute on Taxation and Economic Policy (ITEP).
- **Data Source:** Institute on Taxation and Economic Policy (ITEP) Who Pays report (biennial), state tax codes. State-level.

### Node 69: State and Local Tax (SALT) Regressivity Index
- **Scale:** 4
- **Domain:** Economic Security, Taxation
- **Type:** Policy
- **Unit:** Ratio of effective tax rate (bottom 20% / top 1%)
- **Description:** The ratio of effective state and local tax rates (income, sales, property, excise) paid by the bottom 20% of income earners vs. the top 1%. Ratio >1.0 = regressive (poor pay higher %), <1.0 = progressive. Measures overall tax fairness including sales and property taxes. State-level.
- **Baseline:** National median ratio = 1.4 (regressive: bottom 20% pay 11.4%, top 1% pay 8.1%). Range: 1.0 (least regressive: CA, DC, VT) to 2.2 (most regressive: WA, FL, TX, TN). Source: ITEP Who Pays report.
- **Data Source:** Institute on Taxation and Economic Policy (ITEP) Who Pays report (biennial). State-level.

### Node 70: Earned Income Tax Credit (EITC) Refundability
- **Scale:** 1
- **Domain:** Economic Security, Taxation
- **Type:** Policy
- **Unit:** State EITC as % of federal EITC (0% if no state EITC)
- **Description:** State EITC generosity as a percentage of the federal EITC. Fully refundable state credits supplement federal EITC, providing income support to working poor families. Coded as 0% if no state EITC, % of federal if exists (e.g., 30% means state credit is 30% of federal amount).
- **Baseline:** 31 states + DC have state EITC (2024). Median among states with EITC = 20% of federal. Range: 0% (19 states) to 100% (CA state EITC can equal federal under certain circumstances). Source: CBPP, ITEP.
- **Data Source:** Center on Budget and Policy Priorities (CBPP), Institute on Taxation and Economic Policy (ITEP) state EITC database. State-level, annual.

### Node 71: Property Tax Circuit Breaker Coverage
- **Scale:** 4
- **Domain:** Economic Security, Taxation, Housing
- **Type:** Policy
- **Unit:** Categorical: No circuit breaker, Elderly only, All low-income
- **Description:** Whether state has property tax "circuit breaker" relief limiting property taxes as % of income for vulnerable populations. Coded as: No program, Elderly only, or All low-income. Protects against property tax-induced housing cost burden, particularly for elderly homeowners on fixed income.
- **Baseline:** 35 states + DC have some form of circuit breaker (2024). Most limit to elderly/disabled. ~15 states extend to all low-income. Source: AARP, Lincoln Institute of Land Policy.
- **Data Source:** AARP state property tax relief programs, Lincoln Institute of Land Policy, state revenue department programs. State-level.

### Node 72: Sales Tax Exemption for Necessities
- **Scale:** 6
- **Domain:** Economic Security, Taxation
- **Type:** Policy
- **Unit:** Index 0-10 (higher = more exemptions)
- **Description:** Index of sales tax exemptions for necessities (groceries, prescription drugs, OTC medications, diapers, menstrual products, utilities). Each category exempted adds to score. 0 = tax all necessities, 10 = exempt all. Reduces regressivity of sales tax. State-level.
- **Baseline:** National median = 5.0. Range: 0 (AL, HI, MS tax groceries and drugs) to 10 (OR, NH, MT, DE, AK have no/minimal sales tax; CA exempts most). 13 states still tax groceries. Source: CBPP, state revenue departments.
- **Data Source:** Center on Budget and Policy Priorities (CBPP) sales tax analysis, state revenue departments, Tax Policy Center. State-level.

### Node 73: Estate/Inheritance Tax Existence
- **Scale:** 4
- **Domain:** Economic Security, Taxation, Wealth
- **Type:** Policy
- **Unit:** Categorical: No tax, Inheritance tax, Estate tax
- **Description:** Whether state levies estate or inheritance taxes on wealth transfers at death. Coded as: No tax (most states), Inheritance tax (tax on heirs, rates vary by relationship), or Estate tax (tax on total estate before distribution, progressive rates). Affects wealth accumulation and inequality.
- **Baseline:** 12 states + DC have estate tax, 6 states have inheritance tax, 1 (MD) has both (2024). 33 states have neither. Estate tax thresholds range $1M (OR) to $13M (federal threshold, some states match). Source: Tax Foundation, state revenue departments.
- **Data Source:** Tax Foundation state estate tax reports, state revenue departments. State-level.

### Node 74: Safety Net Funding Per Capita
- **Scale:** 3
- **Domain:** Economic Security, Social Services
- **Type:** Policy
- **Unit:** State dollars per capita per year for safety net programs
- **Description:** Combined state spending on means-tested safety net programs (TANF, state supplements to SNAP/SSI, General Assistance, emergency assistance, childcare subsidies) divided by state population. Does not include Medicaid (captured separately). Measures state commitment to anti-poverty programs. State-level.
- **Baseline:** National median = $120 per capita (2023). Range: $40 (low-spending states) to $380 (HI, CA, NY with generous supplements). Source: CBPP analysis of state budgets.
- **Data Source:** Center on Budget and Policy Priorities (CBPP) state budget analyses, NASBO State Expenditure Reports, state budget documents. State-level, annual.

---

## 1.9 TRADE AND ECONOMIC POLICY

### Node 75: State Minimum Wage Indexed to Inflation
- **Scale:** 4
- **Domain:** Economic Security, Employment
- **Type:** Policy
- **Unit:** Binary (0=not indexed, 1=indexed)
- **Description:** Whether state minimum wage is automatically adjusted annually for inflation (typically tied to CPI). Binary indicator. Indexing prevents erosion of real wages. Without indexing, minimum wage loses purchasing power over time until legislature acts.
- **Baseline:** 18 states + DC index minimum wage to inflation (2024). 32 states do not (requires legislative action to increase). Source: EPI, NCSL.
- **Data Source:** Economic Policy Institute (EPI), National Conference of State Legislatures (NCSL) minimum wage tracking. State-level.

### Node 76: State Rainy Day Fund Balance
- **Scale:** 5
- **Domain:** Economic Security, Fiscal Policy
- **Type:** Policy
- **Unit:** Rainy day fund balance as % of state general fund expenditures
- **Description:** State budget stabilization fund (rainy day fund) balance as a percentage of annual general fund spending. Measures state fiscal cushion for recessions. Protects safety net and services during downturns. Higher = more fiscal resilience.
- **Baseline:** National median = 10.2% (2024). Range: 0% (a few states with depleted funds) to 40%+ (WY, AK, TX with resource-rich economies). NASBO recommends 15% minimum. Source: NASBO, Pew Charitable Trusts.
- **Data Source:** National Association of State Budget Officers (NASBO) Fiscal Survey, Pew Charitable Trusts Fiscal 50 dashboard. State-level, annual.

### Node 77: Economic Development Incentive Spending Per Capita
- **Scale:** 1
- **Domain:** Economic Security, Employment, Fiscal Policy
- **Type:** Policy
- **Unit:** State dollars per capita per year on business incentives
- **Description:** State spending on economic development incentives (tax credits, grants, loans to businesses) divided by state population. Includes: film tax credits, enterprise zones, discretionary incentive deals. High spending may crowd out public services. Controversial effectiveness. State-level.
- **Baseline:** National median = $35 per capita (2023). Range: $5 to $300 per capita (LA, NY, NV with large film/tourism credits). Source: Good Jobs First, state budget analysis.
- **Data Source:** Good Jobs First Subsidy Tracker, state economic development agency reports, state budgets. State-level, annual.

### Node 78: State Business Tax Climate Index
- **Scale:** 6
- **Domain:** Economic Security, Employment, Taxation
- **Type:** Policy
- **Unit:** Index rank 1-50 (1=most business-friendly)
- **Description:** Tax Foundation's State Business Tax Climate Index ranking states on: corporate income tax, individual income tax, sales tax, property tax, and unemployment insurance tax. Lower rank (closer to 1) = more competitive/business-friendly tax structure. Note: Pro-business perspective; not a progressivity or equity measure.
- **Baseline:** Ranked 1-50 (all states). Top: WY, SD, AK (no/low taxes). Bottom: NJ, NY, CA (higher taxes). Source: Tax Foundation.
- **Data Source:** Tax Foundation State Business Tax Climate Index (annual). State-level.

### Node 79: Prevailing Wage Law Existence
- **Scale:** 1
- **Domain:** Employment, Labor, Infrastructure
- **Type:** Policy
- **Unit:** Binary (0=no prevailing wage law, 1=law exists)
- **Description:** Whether state has "prevailing wage" law requiring contractors on public construction projects to pay wages and benefits at or above locally prevailing rates (similar to federal Davis-Bacon Act). Binary indicator. Supports construction worker wages and reduces race-to-bottom on public projects. Opposed by some as increasing costs.
- **Baseline:** 31 states + DC have prevailing wage laws (2024). 19 states have repealed or never had laws. Source: Economic Policy Institute, state labor departments.
- **Data Source:** Economic Policy Institute, National Conference of State Legislatures (NCSL), state labor departments. State-level.

### Node 80: Community Benefits Agreement Requirements
- **Scale:** 4
- **Domain:** Employment, Social Environment, Economic Security
- **Type:** Policy
- **Unit:** Categorical: No requirement, Voluntary encouraged, Mandatory for public projects
- **Description:** Whether state or city requires or encourages Community Benefits Agreements (CBAs) for major development projects receiving public subsidies. CBAs typically include: local hiring, living wages, affordable housing, community facilities. Coded as: No requirement, Voluntary encouraged, or Mandatory. Aims to ensure public investments benefit local communities. Mostly city-level.
- **Baseline:** No states mandate CBAs. ~40 cities have CBA policies or encourage CBAs (2024). Most are voluntary. LA, SF, NYC, Boston common. Source: Partnership for Working Families, local ordinances.
- **Data Source:** Partnership for Working Families CBA tracker, local ordinances. City-level.

---

## 1.10 ECONOMIC STRUCTURE AND MARKET CONDITIONS

### Node 81: Wealth Inequality (Gini Coefficient)
- **Scale:** 4
- **Domain:** Economic Security
- **Type:** Structural Condition
- **Unit:** Gini coefficient 0-1 (higher = more unequal)
- **Description:** Gini coefficient measuring wealth inequality (not income) within a state. Captures concentration of assets (home equity, financial assets, business equity) at top of distribution. 0 = perfect equality, 1 = one household owns everything. Wealth inequality exceeds income inequality and varies by state.
- **Baseline:** National Gini = 0.86 (2019, very high inequality). State range: 0.75 (AK, WV relatively equal) to 0.91 (NY, CA, CT extreme inequality). Source: Federal Reserve SCF, state estimates.
- **Data Source:** Federal Reserve Survey of Consumer Finances (SCF), state-level wealth estimates from academic analyses (e.g., Kuhn, Schularick, Steins). Triennial with lag.

### Node 82: Racial Wealth Gap
- **Scale:** 4
- **Domain:** Economic Security, Social Environment
- **Type:** Structural Condition
- **Unit:** Ratio of median White household wealth to median Black household wealth
- **Description:** The ratio of median household wealth for White households to Black households within a state. Measures structural wealth inequality by race. Ratio >1.0 indicates White advantage. Captures inter generational wealth accumulation gaps from historical discrimination (slavery, redlining, exclusion from New Deal programs).
- **Baseline:** National ratio = 7.8:1 (White households have 7.8x the wealth of Black households, 2019). State range: 4:1 to 12:1. DC, Northeast, Midwest show largest gaps. Source: Federal Reserve SCF, Urban Institute analysis.
- **Data Source:** Federal Reserve Survey of Consumer Finances (SCF), Urban Institute Race and Wealth Scorecard, Prosperity Now racial wealth divide state data. State-level, periodic.

### Node 83: Income Volatility Index
- **Scale:** 4
- **Domain:** Economic Security
- **Type:** Structural Condition
- **Unit:** Index 0-100 (higher = more volatile income)
- **Description:** Composite measure of household income volatility including: month-to-month income variation, job turnover rate, seasonal employment, gig economy participation, and self-employment. Captures economic insecurity from unpredictable earnings. Higher volatility associated with financial distress and health impacts. State and metro-level.
- **Baseline:** National median = 42 (2023). Range: 28 (stable industries, strong unions) to 65 (tourism, agriculture, gig-heavy metros). Source: JPMorgan Chase Institute, Pew income volatility research.
- **Data Source:** JPMorgan Chase Institute Financial Health Pulse, Pew Charitable Trusts income volatility analysis, Federal Reserve Survey of Household Economics. Metro-level, annual.

### Node 84: Median Discretionary Income After Necessities
- **Scale:** 4
- **Domain:** Economic Security
- **Type:** Structural Condition
- **Unit:** Dollars per month remaining after housing, food, transportation, healthcare, childcare
- **Description:** Median household income remaining after paying for necessities (housing 30% threshold, food USDA low-cost plan, transportation, health insurance + out-of-pocket, childcare market rate). Measures financial breathing room. Negative values = insufficient income to cover basics. Geographic variation driven by housing and childcare costs.
- **Baseline:** National median = $580/month (2023). Range: -$450 (high-cost metros where median income insufficient) to $1,800 (lower-cost areas with good wages). Source: United Way ALICE reports, MIT Living Wage Calculator.
- **Data Source:** United Way ALICE (Asset Limited, Income Constrained, Employed) county reports, MIT Living Wage Calculator, Economic Policy Institute Family Budget Calculator. County and metro-level, annual.

### Node 85: Household Debt-to-Income Ratio
- **Scale:** 4
- **Domain:** Economic Security
- **Type:** Structural Condition
- **Unit:** Median household total debt as ratio to annual income
- **Description:** Median household total debt (mortgage, auto, student, credit card, medical, other) divided by annual household income. Measures debt burden. Ratio >1.0 indicates debt exceeds annual income. Reflects necessity of borrowing to meet needs when wages insufficient, plus student loan burden. State-level variation.
- **Baseline:** National median = 1.08 (2023, debt exceeds income). Range: 0.65 (lower cost-of-living states) to 1.85 (high housing cost states). Source: Federal Reserve, Experian debt analysis.
- **Data Source:** Federal Reserve Consumer Credit Panel, Experian State of Credit reports, Urban Institute Debt in America database. State and metro-level, annual.

### Node 86: Predatory Lending Exposure
- **Scale:** 1
- **Domain:** Economic Security
- **Type:** Structural Condition
- **Unit:** Payday lenders + pawn shops per 100,000 population
- **Description:** Combined density of payday lenders, payday loans stores, pawn shops, title lenders, and check cashers per 100,000 population. Measures availability of high-cost alternative financial services that trap low-income households in debt cycles. Concentrated in low-income areas and states with weak regulation.
- **Baseline:** National median = 18 per 100,000 (2022). Range: 2 (states that ban payday lending: NY, NJ, CT) to 55+ (MS, AL, SC with minimal regulation). Source: CFPB, Pew payday lending research.
- **Data Source:** Consumer Financial Protection Bureau (CFPB) complaint database, Pew Charitable Trusts payday lending reports, Center for Responsible Lending, business license data. State and county-level.

### Node 87: Banking Access (Unbanked Rate)
- **Scale:** 4
- **Domain:** Economic Security
- **Type:** Structural Condition
- **Unit:** Percent of households without checking or savings account
- **Description:** Percentage of households that are "unbanked" (no one in household has checking or savings account at bank or credit union). Unbanked households rely on costly check cashers and cannot build savings. Concentrated among low-income, Black, Hispanic, immigrant populations. State and metro variation.
- **Baseline:** 4.5% nationally (2021, down from 7.1% in 2011). Range: 1.8% (NH) to 10.2% (MS). Disparities: 11.3% Black, 9.3% Hispanic, 2.1% White households unbanked. Source: FDIC.
- **Data Source:** FDIC National Survey of Unbanked and Underbanked Households (biennial). State and metro-level estimates available.

### Node 88: Underbanked Rate
- **Scale:** 4
- **Domain:** Economic Security
- **Type:** Structural Condition
- **Unit:** Percent of households using alternative financial services despite having bank account
- **Description:** Percentage of households that are "underbanked": have a bank account but used alternative financial services (payday loans, pawn shops, check cashers, money orders, etc.) in past 12 months. Indicates bank account insufficient for needs or distrust of banking. Higher costs, financial fragility.
- **Baseline:** 14.1% nationally (2021). Range: 7% to 23% across states. Highest in Southern states. Source: FDIC.
- **Data Source:** FDIC National Survey of Unbanked and Underbanked Households (biennial). State and metro-level.

### Node 89: Consumer Debt in Collections Rate
- **Scale:** 4
- **Domain:** Economic Security
- **Type:** Structural Condition
- **Unit:** Percent of adults with debt in collections
- **Description:** Percentage of adults (with credit file) who have any debt in third-party collections. Includes medical, credit card, utility, telecom debt. Indicates financial distress and past inability to pay. Damages credit scores, limits access to credit/housing. Geographic variation reflects economic conditions and healthcare costs.
- **Baseline:** 28% nationally (2022, pre-pandemic was 31%). Range: 13% (MN, ND) to 43% (MS, LA, NV). Medical debt is leading cause. Source: Urban Institute Debt in America.
- **Data Source:** Urban Institute Debt in America database (credit bureau data), Consumer Financial Protection Bureau (CFPB) data. State, metro, and ZIP-level, updated periodically.

### Node 90: Medical Debt Prevalence
- **Scale:** 1
- **Domain:** Economic Security, Healthcare Access
- **Type:** Structural Condition
- **Unit:** Percent of adults with medical debt in collections
- **Description:** Percentage of adults with medical debt in third-party collections on their credit report. Medical debt is leading source of collections debt. Reflects inadequate insurance, high cost-sharing, surprise billing, inability to pay. Concentrated in states without Medicaid expansion and with high uninsured rates.
- **Baseline:** 17.8% nationally (2022, down from 20% in 2020 after some debt removed from credit reports). Range: 7% (MN) to 28% (SC, NC). Source: Urban Institute, KFF.
- **Data Source:** Urban Institute Debt in America, Kaiser Family Foundation medical debt analysis, CFPB credit bureau data. State and county-level.

### Node 91: Bank Branch Density
- **Scale:** 2
- **Domain:** Economic Security, Built Environment
- **Type:** Structural Condition
- **Unit:** Bank branches per 100,000 population
- **Description:** Number of physical bank and credit union branches per 100,000 population. Measures access to traditional banking. Branch deserts (areas with no branches) limit cash deposits, in-person services, relationship banking. Branches declining nationwide due to online banking; disproportionately impacts low-income and elderly.
- **Baseline:** 28 branches per 100,000 nationally (2023, declining from 35 in 2010). Range: 18 (banking deserts in rural areas) to 50+ (urban financial centers). Source: FDIC Summary of Deposits.
- **Data Source:** FDIC Summary of Deposits (annual), NCUA Credit Union locator. State, county, and tract-level.

### Node 92: Credit Score Distribution (Median)
- **Scale:** 2
- **Domain:** Economic Security
- **Type:** Structural Condition
- **Unit:** Median FICO credit score
- **Description:** Median FICO credit score among adults with credit files in a geographic area. Measures creditworthiness and financial health. Scores <580 = poor, 580-669 = fair, 670-739 = good, 740-799 = very good, 800+ = exceptional. Affects ability to rent housing, get loans, job prospects. Reflects past financial stress and access to credit.
- **Baseline:** National median = 717 (2023, "good"). State range: 675 (MS) to 740 (MN, SD). Racial disparities: Black median = 627, Hispanic = 701, White = 734. Source: Experian, FICO.
- **Data Source:** Experian State of Credit report (annual), FICO, Federal Reserve Consumer Credit Panel. State and metro-level.

---

## 1.11 LABOR MARKET STRUCTURE

### Node 93: Job Quality Index
- **Scale:** 4
- **Domain:** Employment
- **Type:** Structural Condition
- **Unit:** Index 0-100 (higher = better job quality)
- **Description:** Composite index of job quality in regional labor market including: median wage, benefits availability (health, retirement, paid leave), schedule stability/predictability, advancement opportunities, union coverage, workplace safety, and worker power. Goes beyond minimum wage policy to measure actual job conditions. State and metro-level.
- **Baseline:** National median = 52 (2023). Range: 38 (low-wage service economy, weak labor protections) to 68 (high-wage, unionized industries). Source: RAND Job Quality Index, Aspen Institute.
- **Data Source:** RAND American Working Conditions Survey, Aspen Institute Future of Work Initiative, Bureau of Labor Statistics (BLS) compensation and safety data. Metro-level, updated periodically.

### Node 94: Precarious Employment Rate
- **Scale:** 4
- **Domain:** Employment
- **Type:** Structural Condition
- **Unit:** Percent of workforce in non-standard arrangements
- **Description:** Percentage of workers in precarious employment: temporary workers, contract workers, on-call, day laborers, and app-based gig workers. Excludes standard part-time. Precarious work characterized by instability, low pay, no benefits, unpredictable schedules. Growing share of economy; concentrated in low-income communities.
- **Baseline:** 15-20% nationally (2023, estimates vary). Range: 10% to 28% across metros. Highest in cities with large gig economy (ride-share, delivery). Source: BLS Contingent Worker Supplement, JPMorgan Chase Institute gig research.
- **Data Source:** Bureau of Labor Statistics Contingent Worker Supplement (CWS, periodic), JPMorgan Chase Institute gig economy data, Economic Policy Institute analyses. State and metro-level.

### Node 95: Wage Stagnation Rate
- **Scale:** 4
- **Domain:** Employment, Economic Security
- **Type:** Structural Condition
- **Unit:** Percent change in real median wage over 10 years
- **Description:** Inflation-adjusted change in median hourly wage over the previous 10 years. Measures whether wages are keeping pace with productivity and cost of living. Negative or near-zero = stagnation despite economic growth. Varies by state due to labor market tightness, unionization, industrial composition. Compares real (inflation-adjusted) wages.
- **Baseline:** +2.8% nationally (2013-2023, minimal growth over decade). Range: -5% (real wage decline) to +12% (strong wage growth, tight labor markets). Source: Economic Policy Institute, BLS.
- **Data Source:** Bureau of Labor Statistics Occupational Employment and Wage Statistics (OEWS), Current Population Survey. State-level, annual.

### Node 96: Occupational Hazard Exposure Rate
- **Scale:** 4
- **Domain:** Employment, Occupational Health
- **Type:** Structural Condition
- **Unit:** Percent of workforce in high-hazard occupations
- **Description:** Percentage of employed workers in occupations with high injury/illness risk: construction, manufacturing, agriculture, healthcare (lifting/violence), transportation, warehousing. Does not measure actual injury (that's Scale 3/5), but structural exposure risk based on occupation. Varies by regional industrial composition.
- **Baseline:** 32% nationally (2023). Range: 18% (service/knowledge economies) to 52% (manufacturing/extraction/agriculture states). Source: BLS OEWS, OSHA hazard classifications.
- **Data Source:** Bureau of Labor Statistics Occupational Employment and Wage Statistics (OEWS), OSHA hazard classifications by SOC code. State and metro-level, annual.

### Node 97: Workplace Injury and Illness Rate
- **Scale:** 4
- **Domain:** Employment, Occupational Health
- **Type:** Structural Condition (could be Individual, but aggregate rate is structural)
- **Unit:** Cases per 100 full-time equivalent (FTE) workers per year
- **Description:** Total recordable workplace injuries and illnesses per 100 FTE workers. Includes fatalities, days away from work cases, job transfer/restriction, and other recordable cases. Measures actual occupational health burden. Varies by industry mix and safety culture/enforcement. Underreporting is significant issue.
- **Baseline:** 2.7 cases per 100 FTE nationally (2022). Range: 1.8 to 4.2 across states. Highest: manufacturing, construction, agriculture, healthcare states. Declining long-term but still ~2.8M injuries/year. Source: BLS.
- **Data Source:** Bureau of Labor Statistics Survey of Occupational Injuries and Illnesses (SOII), annual. State-level, by industry.

### Node 98: Fatal Occupational Injury Rate
- **Scale:** 4
- **Domain:** Employment, Occupational Health
- **Type:** Structural Condition
- **Unit:** Fatalities per 100,000 FTE workers per year
- **Description:** Work-related fatalities per 100,000 full-time equivalent workers. Includes traumatic injuries (falls, struck by, caught in, transportation), violence, and acute exposures. Excludes long-term occupational disease (e.g., cancer from exposures). Concentrated in construction, transportation, agriculture, extraction. State variation reflects industrial mix and safety enforcement.
- **Baseline:** 3.6 per 100,000 FTE nationally (2022). Range: 1.5 (office economies) to 10+ (extraction, agriculture, fishing states like AK, WY, MT). Source: BLS CFOI.
- **Data Source:** Bureau of Labor Statistics Census of Fatal Occupational Injuries (CFOI), annual. State-level.

### Node 99: Industrial Composition Index
- **Scale:** 4
- **Domain:** Employment, Economic Security
- **Type:** Structural Condition
- **Unit:** Index 0-100 (higher = higher-wage industries)
- **Description:** Index capturing state/metro industrial composition weighted by wage/benefit levels. High-wage industries (tech, finance, professional services, manufacturing) score higher. Low-wage industries (retail, food service, personal services, agriculture) score lower. Structural constraint on available jobs and wages. Slow-changing.
- **Baseline:** National median = 50 (by construction). Range: 30 (service/tourism economies) to 75 (tech/finance hubs). Source: BLS QCEW, Brookings Metro Monitor.
- **Data Source:** Bureau of Labor Statistics Quarterly Census of Employment and Wages (QCEW), BEA regional economic accounts. State and metro-level, annual.

### Node 100: Part-Time for Economic Reasons Rate
- **Scale:** 6
- **Domain:** Employment, Economic Security
- **Type:** Structural Condition (labor market condition)
- **Unit:** Percent of workforce part-time involuntarily
- **Description:** Percentage of employed workers working part-time (<35 hours/week) because they cannot find full-time work or hours were cut. Involuntary part-time = underemployment. Distinct from voluntary part-time (choice). Indicates slack labor market and economic insecurity. Cyclical and structural components.
- **Baseline:** 3.5% nationally (2023, low due to tight labor market). Range: 2.5% to 5.5%. Recession peaks at 6-7%. Concentrated in retail, food service, personal services. Source: BLS.
- **Data Source:** Bureau of Labor Statistics Current Population Survey (CPS), Local Area Unemployment Statistics (LAUS). State and metro-level, monthly.

### Node 101: Labor Force Participation Rate
- **Scale:** 6
- **Domain:** Employment, Economic Security
- **Type:** Structural Condition
- **Unit:** Percent of working-age population (16+) in labor force
- **Description:** Percentage of civilian non-institutional population age 16+ who are working or actively seeking work. Measures engagement with formal economy. Lower rates indicate discouraged workers, early retirement, disability, caregiving, or school enrollment. Varies by state due to age distribution, disability prevalence, economic opportunity, and cultural factors. Declined nationally after 2008 and COVID.
- **Baseline:** 63.4% nationally (2023, below pre-2008 levels of 66%). Range: 56% (WV) to 70% (ND, SD). Gender gap: 57.3% women, 67.8% men. Source: BLS.
- **Data Source:** Bureau of Labor Statistics Current Population Survey (CPS), Local Area Unemployment Statistics (LAUS). State and metro-level, monthly.

### Node 102: Youth (16-24) Unemployment Rate
- **Scale:** 6
- **Domain:** Employment, Economic Security, Education
- **Type:** Structural Condition
- **Unit:** Percent of youth labor force unemployed
- **Description:** Unemployment rate for ages 16-24. Youth unemployment typically 2-3x overall rate. High youth unemployment associated with long-term scarring effects (lower lifetime earnings, health impacts). Concentrated among Black and Hispanic youth, dropouts, and disconnected youth. Geographic variation reflects education-economy match and job training.
- **Baseline:** 8.0% nationally (2023). Range: 4% to 14%. Disparities: 13.7% Black youth, 9.1% Hispanic, 6.7% White. Recession peaks at 18-20%. Source: BLS.
- **Data Source:** Bureau of Labor Statistics Current Population Survey (CPS). State-level, annual (sample size limits monthly estimates). EPI and Urban Institute produce metro estimates.

---

## 1.12 TRANSPORTATION SYSTEM STRUCTURE

### Node 103: Average Commute Time
- **Scale:** 4
- **Domain:** Transportation, Employment
- **Type:** Structural Condition
- **Unit:** Median minutes per one-way commute
- **Description:** Median travel time to work for workers age 16+ who commute (excludes work-from-home). Measures transportation burden and time tax. Longer commutes associated with worse health, less time for family/sleep, higher stress. Varies by sprawl, transit quality, housing affordability (long-distance commutes from affordable areas). Metro-level.
- **Baseline:** 27.6 minutes nationally (2021, one-way). Range: 17 minutes (rural areas, small metros) to 38 minutes (NYC metro). Over 60 minutes = "super-commuters" (2.8% of workers). Source: ACS.
- **Data Source:** American Community Survey (ACS) Journey to Work, annual. State, metro, county, and tract-level.

### Node 104: Vehicle Dependency Rate
- **Scale:** 4
- **Domain:** Transportation
- **Type:** Structural Condition
- **Unit:** Percent of workers who must drive alone to work
- **Description:** Percentage of commuters who drive alone (no carpool, transit, walk, bike options available or practical). Indicates lack of transportation alternatives. High vehicle dependency = transportation cost burden, exclusion of non-drivers, environmental impacts. Inverse of transit/walk/bike commute share.
- **Baseline:** 76.4% nationally drive alone (2021, remainder: carpool 9%, transit 5%, walk 2.7%, bike 0.5%, WFH 5.7%, other 0.7%). Range: 50% (transit-rich cities) to 85% (car-dependent sprawl). Source: ACS.
- **Data Source:** American Community Survey (ACS) Commuting Characteristics, annual. State, metro, county, tract-level.

### Node 105: Transit Service Frequency
- **Scale:** 2
- **Domain:** Transportation, Built Environment
- **Type:** Structural Condition
- **Unit:** Median wait time (minutes) for transit at median stop
- **Description:** Median headway (time between vehicles) at the median transit stop during peak hours. Measures quality and usability of transit. Frequent service (<10 min) enables spontaneous use; infrequent service (>30 min) requires schedule planning and discourages use. Varies dramatically: dense transit cities vs. minimal service suburbs.
- **Baseline:** National median = 30 minutes at median stop (2019, where transit exists). Range: 6 min (frequent service networks in NYC, SF) to 60+ min (suburban/rural minimal service). Many areas have no transit. Source: GTFS feeds analyzed by researchers.
- **Data Source:** General Transit Feed Specification (GTFS) data analyzed by researchers (e.g., Transit Center, ITDP), OpenTripPlanner. Metro and transit agency-level.

### Node 106: Job Accessibility by Transit
- **Scale:** 2
- **Domain:** Transportation, Employment
- **Type:** Structural Condition
- **Unit:** Percent of metro jobs accessible within 45 minutes by transit
- **Description:** Percentage of jobs in a metropolitan area reachable within 45 minutes by public transit from the median neighborhood. Measures functional transit access to employment. Low accessibility = spatial mismatch, limits employment options for car-less workers. Varies by transit coverage and job sprawl.
- **Baseline:** National median metro = 15% of jobs accessible within 45 min by transit (2022). Range: <5% (car-dependent metros with minimal transit) to 50%+ (NYC, SF, DC with extensive systems). Source: U of MN Accessibility Observatory.
- **Data Source:** University of Minnesota Accessibility Observatory (annual analysis of GTFS + LODES employment data). Metro-level.

### Node 107: Transportation Cost Burden
- **Scale:** 4
- **Domain:** Transportation, Economic Security
- **Type:** Structural Condition
- **Unit:** Median transportation costs as % of household income
- **Description:** Median household spending on transportation (vehicle purchase/lease, gas, insurance, maintenance, transit fares, parking) as percentage of income. HUD+DOT recommend <15%; >20% = cost-burdened. Higher in car-dependent sprawl with long commutes. Lower in transit-accessible walkable areas. Varies by housing-jobs balance and transit availability.
- **Baseline:** 17% nationally (2021, median household). Range: 10% (transit-rich, walkable cities) to 25% (car-dependent sprawl, long commutes). Low-income households: 22-30%. Source: BLS Consumer Expenditure Survey, CNT H+T Index.
- **Data Source:** Bureau of Labor Statistics Consumer Expenditure Survey, Center for Neighborhood Technology (CNT) Housing + Transportation (H+T) Affordability Index. Metro and neighborhood-level.

### Node 108: Transit Desert Prevalence
- **Scale:** 2
- **Domain:** Transportation, Built Environment
- **Type:** Structural Condition
- **Unit:** Percent of population living in transit deserts
- **Description:** Percentage of metro population living in "transit deserts": areas with no transit stop within 1/2 mile (walkable distance) OR transit service less frequent than every 30 minutes. Transit deserts exclude residents from car-free mobility. Concentrated in suburbs and low-density areas, but also some low-income inner-city areas (service gaps).
- **Baseline:** 45% of US metro population lives in transit deserts (2019, among 50 largest metros). Range: 15% (NYC metro, comprehensive coverage) to 75% (sprawling Sun Belt metros). Source: TransitCenter, Brookings.
- **Data Source:** TransitCenter analysis of GTFS data, Brookings metro transit analyses. Metro and neighborhood-level.

### Node 109: Pedestrian and Cyclist Safety (Fatality Rate)
- **Scale:** 7
- **Domain:** Transportation, Built Environment, Public Health
- **Type:** Structural Condition
- **Unit:** Pedestrian + cyclist fatalities per 100,000 population per year
- **Description:** Combined pedestrian and bicyclist deaths from vehicle crashes per 100,000 population. Indicates dangerous street design (high-speed roads, lack of sidewalks/crossings/bike lanes, poor lighting). Preventable through infrastructure improvements. Concentrated in Sun Belt sprawl with high-speed arterials. Disparities by race and income (pedestrian deaths higher in low-income areas).
- **Baseline:** 2.3 per 100,000 nationally (2022, ~7,500 deaths/year). Range: 0.8 (safe street design, low VMT states) to 4.5+ (FL, NM, AZ, SC dangerous roads). Rising nationally despite overall traffic safety improvements. Source: NHTSA, Smart Growth America.
- **Data Source:** National Highway Traffic Safety Administration (NHTSA) Fatality Analysis Reporting System (FARS), Smart Growth America Dangerous by Design report (periodic). State and metro-level, annual.

### Node 110: Walkability Index
- **Scale:** 2
- **Domain:** Transportation, Built Environment
- **Type:** Structural Condition
- **Unit:** Index 0-100 (higher = more walkable)
- **Description:** Composite index of walkability including: street connectivity (intersection density), mix of land uses (residential + services), pedestrian infrastructure (sidewalks, crossings), and population density. High walkability enables car-free living, physical activity, social interaction. Low walkability necessitates driving for all trips. Neighborhood-level metric aggregated to larger geographies.
- **Baseline:** National median neighborhood = 35 (2023, car-dependent). Range: 10 (unwalkable suburban sprawl) to 95 (dense, mixed-use urban neighborhoods). Only 10% of US neighborhoods score >70 (very walkable). Source: Walk Score, EPA Smart Location Database.
- **Data Source:** Walk Score (via Redfin, proprietary but widely used), EPA Smart Location Database (public, periodic updates). Neighborhood, tract, city, and metro-level.

---

## 1.13 COMMUNITY POWER AND CIVIC INFRASTRUCTURE

### Node 111: Voter Turnout Rate
- **Scale:** 4
- **Domain:** Civic Engagement, Social Environment
- **Type:** Structural Condition
- **Unit:** Percent of eligible population voting in general elections
- **Description:** Percentage of voting-eligible population (citizens 18+, not felons in states with disenfranchisement) who voted in the most recent general election. Presidential vs. midterm elections differ significantly. Measures civic engagement and political efficacy. Lower turnout associated with marginalization, voter suppression, and lack of competitive races. Geographic variation.
- **Baseline:** 66.8% in 2020 presidential (highest in decades), 50.3% in 2022 midterm. State range: 51% to 80% (presidential). Disparities: lower among young, low-income, renters, people of color in restrictive states. Source: US Elections Project.
- **Data Source:** US Elections Project (University of Florida), state election boards. State and county-level, biennial.

### Node 112: Community Organizing Density
- **Scale:** 4
- **Domain:** Social Environment, Civic Engagement
- **Type:** Structural Condition
- **Unit:** Community-based organizations per 10,000 population
- **Description:** Number of active community-based organizations (CBOs) focused on social change, advocacy, and mutual aid per 10,000 population. Includes neighborhood associations, tenant unions, worker centers, mutual aid networks, advocacy nonprofits. Measures grassroots organizing capacity and community power. Difficult to enumerate completely; based on IRS 501(c) registrations and surveys.
- **Baseline:** ~3.5 per 10,000 nationally (2022, significant variation). Range: 1.5 (weak organizing infrastructure) to 8+ (dense organizing ecosystems in urban areas). Source: National Council of Nonprofits, local organizing networks.
- **Data Source:** IRS 501(c) organization database (undercount), National Council of Nonprofits, state nonprofit associations, local organizing network surveys. Metro and county-level.

### ~~Node 113: Labor Union Density (Local)~~ [REMOVED - Consolidated into Node 28]
- **Consolidation Note:** This node measured the same thing as Node 28 (union membership rate / union density) but at metro/county level instead of state level. Merged into Node 28 which now explicitly works at multiple geographic scales (state, metro, county).
- **Migration:** Update all references to use Node 28 `union_density_rate`
- **Data Source:** Bureau of Labor Statistics CPS Union Membership Supplement (state-level), Economic Policy Institute metro estimates (modeled). Metro-level, annual.

### Node 114: Tenant Union and Organizing Capacity
- **Scale:** 4
- **Domain:** Housing, Social Environment
- **Type:** Structural Condition
- **Unit:** Tenant unions + tenant rights organizations per 100,000 renters
- **Description:** Number of active tenant unions, tenant associations, and tenant rights organizations per 100,000 renter households. Measures capacity for collective action on housing issues. Tenant organizing associated with better code enforcement, eviction resistance, and rent stabilization efforts. Data difficult; based on surveys and mapping projects.
- **Baseline:** ~1.2 per 100,000 renters nationally (2023, likely undercount). Range: 0 (minimal organizing) to 5+ (strong tenant movement cities: NYC, SF, LA, DC). Source: Tenant organizing networks, Right to the City Alliance.
- **Data Source:** Tenant organizing network surveys (e.g., Right to the City Alliance, Homes Guarantee campaign), local housing justice coalitions. City-level, updated periodically.

### Node 115: Civic Participation Rate (Beyond Voting)
- **Scale:** 4
- **Domain:** Civic Engagement, Social Environment
- **Type:** Structural Condition
- **Unit:** Percent of adults engaged in civic activities (past year)
- **Description:** Percentage of adults who participated in at least one non-electoral civic activity in the past year: attended public meeting, contacted elected official, attended protest/march, volunteered for community cause, served on committee, or participated in community problem-solving. Broader measure of civic engagement than voting. Survey-based.
- **Baseline:** 34% nationally (2022). Range: 22% to 48% across states and metros. Higher in college-educated, higher-income, and civically-engaged communities. Source: Current Population Survey Civic Engagement Supplement, National Conference on Citizenship.
- **Data Source:** US Census Current Population Survey Civic Engagement and Volunteering Supplement (periodic), National Conference on Citizenship Civic Health Index. State and metro-level.

### Node 116: Grassroots Funding Capacity
- **Scale:** 4
- **Domain:** Economic Security, Civic Engagement
- **Type:** Structural Condition
- **Unit:** Small donations (<$200) per capita to community organizations and campaigns
- **Description:** Total value of small donations (<$200 individual contributions) to local community organizations and local/state political campaigns divided by population. Proxy for grassroots financial capacity and community investment. Excludes large donations and corporate giving. Reflects ability to support local organizing and campaigns without reliance on wealthy donors.
- **Baseline:** ~$12 per capita nationally (2022). Range: $5 to $35+ (high civic engagement metros). Data incomplete; based on FEC political donations and nonprofit giving surveys. Source: Federal Election Commission, GuideStar.
- **Data Source:** Federal Election Commission (FEC) itemized contribution data (political), GuideStar/Candid nonprofit giving data. Incomplete for non-itemized <$200 donations to nonprofits. State and metro estimates.

### Node 117: Public Meeting Attendance Rate
- **Scale:** 4
- **Domain:** Civic Engagement
- **Type:** Structural Condition
- **Unit:** Average attendees per city council / county board meeting
- **Description:** Average number of public attendees at city council or county board meetings (excluding officials and staff). Measures direct democratic engagement and government accountability. Low attendance suggests disengagement, lack of awareness, or meetings scheduled inaccessibly. Varies by population size (denominator important), issue salience, and civic culture.
- **Baseline:** ~25 attendees at median city council meeting (2022, excludes virtual attendance COVID era). Range: 5 (low engagement) to 100+ (contested issues, engaged communities). Should be normed per capita for fair comparison. Source: National League of Cities surveys, local government data.
- **Data Source:** National League of Cities surveys, local government attendance records (where tracked). City and county-level.

### Node 118: Language Access in Government Services
- **Scale:** 1
- **Domain:** Civic Engagement, Social Environment
- **Type:** Structural Condition
- **Unit:** Percent of LEP population with language access to government services
- **Description:** Percentage of Limited English Proficient (LEP) residents who have meaningful language access to government services (translation/interpretation) in their primary language. Measured by: availability of translated materials, interpreter services, and multilingual staff for top non-English languages. Federal requirements exist but enforcement varies.
- **Baseline:** ~45% of LEP population has adequate access nationally (2022, estimate). Range: 10% (minimal translation) to 85% (comprehensive multilingual services). Higher in diverse urban areas with strong advocacy. Source: Migration Policy Institute, Language Access Network.
- **Data Source:** Migration Policy Institute language access assessments, Department of Justice Language Access Assessments, local government language access plans. City and county-level.

### Node 119: Media Diversity (Local News Outlets)
- **Scale:** 4
- **Domain:** Civic Engagement, Information Environment
- **Type:** Structural Condition
- **Unit:** Local news outlets per 100,000 population
- **Description:** Number of local news outlets (newspapers, TV stations, radio, online news sites) per 100,000 population. Measures information infrastructure for civic engagement. "News deserts" (areas with no/minimal local journalism) associated with lower civic engagement, less government accountability. Rapid decline due to consolidation and economic pressures.
- **Baseline:** 2.8 outlets per 100,000 nationally (2023, declining from 4.5 in 2005). Range: 0 (news deserts, mostly rural) to 8+ (major metros). Over 2,000 counties are news deserts or at risk. Source: UNC Hussman School News Deserts project.
- **Data Source:** UNC Hussman School of Journalism News Deserts and Ghost Newspapers project (biennial), Pew Research Center State of the News Media. County-level.

### Node 120: Digital Civic Engagement Infrastructure
- **Scale:** 4
- **Domain:** Civic Engagement, Digital Access
- **Type:** Structural Condition
- **Unit:** Percent of residents with access to online civic platforms
- **Description:** Percentage of residents with access (via broadband + device) to online civic engagement platforms: government websites, participatory budgeting, public comment systems, 311 apps, transparency portals. Requires both digital access (Node 65 funding, individual access at Scale 3) and platform existence. Measures digitaldivide in civic participation.
- **Baseline:** ~72% have access nationally (2023, limited by ~75% broadband access and device ownership). Range: 50% (rural, low-income areas) to 92% (high broadband, digital government metros). Source: Pew, Digital Government Research, NTIA.
- **Data Source:** Pew Research Center Internet & Technology, National Telecommunications and Information Administration (NTIA) digital access data, Digital Government Research Center. Metro and county-level.

---

## 1.14 CLIMATE AND ENVIRONMENTAL EXPOSURES

### Node 121: Extreme Heat Days Per Year
- **Scale:** 2
- **Domain:** Environmental, Climate, Public Health
- **Type:** Structural Condition
- **Unit:** Days per year with heat index >100°F
- **Description:** Average annual number of days with heat index (combines temperature and humidity) exceeding 100°F. Extreme heat causes mortality (especially elderly, outdoor workers), exacerbates chronic disease, strains infrastructure. Increasing due to climate change. Urban heat islands amplify exposure. Geographic variation: most severe in South, Southwest.
- **Baseline:** 17 days nationally (population-weighted, 2015-2023 average). Range: 0 days (northern states) to 80+ days (Phoenix, Houston). Increasing ~2-3 days per decade. Source: NOAA, CDC BRACE.
- **Data Source:** National Oceanic and Atmospheric Administration (NOAA) climate data, CDC BRACE heat exposure tracking, Climate Central analysis. County-level, annual.

### Node 122: Flood Risk Exposure (100-Year Floodplain)
- **Scale:** 2
- **Domain:** Environmental, Climate, Housing
- **Type:** Structural Condition
- **Unit:** Percent of population living in FEMA 100-year floodplain
- **Description:** Percentage of population residing in FEMA-designated Special Flood Hazard Areas (SFHAs, 100-year floodplain = 1% annual flood risk). Flood exposure causes housing damage, displacement, health impacts (mold, injury, stress), and economic loss. Concentrated in coastal areas and river valleys. Climate change increasing flood frequency beyond 100-year designation.
- **Baseline:** 8.7% of US population in FEMA 100-year floodplain (2023). Range: <1% (mountains, deserts) to 35%+ (coastal Louisiana, Florida, riverine areas). Does not include future climate-adjusted risk. Source: FEMA, First Street Foundation.
- **Data Source:** FEMA National Flood Hazard Layer (NFHL), First Street Foundation Flood Factor (includes climate projections), Census population. County and tract-level.

### Node 123: Wildfire Risk Exposure
- **Scale:** 2
- **Domain:** Environmental, Climate
- **Type:** Structural Condition
- **Unit:** Percent of population in high/very high wildfire hazard zones
- **Description:** Percentage of population living in areas designated as high or very high wildfire hazard potential by USFS. Wildfire smoke causes respiratory illness, cardiovascular events; fires cause displacement, housing loss, trauma. Concentrated in Western states (WUI: wildland-urban interface). Risk increasing with climate change and development.
- **Baseline:** 11% of US population in high/very high wildfire zones (2023). Range: 0% (non-fire-prone regions) to 40%+ (CA, OR, WA, CO mountain areas). Source: USDA Forest Service.
- **Data Source:** USDA Forest Service Wildfire Hazard Potential dataset, CAL FIRE, Climate Central, Census population. County and tract-level.

### Node 124: Ambient Air Pollution (PM2.5) [REVISED - Consolidated with Node 226]
- **Scale:** 2/Individual (bridge node - applicable at both scales)
- **Domain:** Environmental, Public Health
- **Type:** Exposure
- **Unit:** μg/m³ PM2.5 annual average
- **Description:** Annual average concentration of fine particulate matter (PM2.5, particles <2.5 micrometers) in ambient air, measured at finest available geographic level (monitor, census tract, or individual residence). PM2.5 causes cardiovascular disease, respiratory disease, premature mortality. For population analysis, use population-weighted average. For individual exposure, use residential location concentration. Prenatal exposure = mother's residential exposure during pregnancy.
- **Baseline:** 8.3 μg/m³ nationally (population-weighted, 2022). Range: 4 μg/m³ (clean rural) to 14+ μg/m³ (polluted urban/wildfire areas). EPA standard: 9 μg/m³ annual (2024). WHO guideline: 5 μg/m³. **Source:** EPA Air Quality System (AQS).
- **Data Source:** EPA AQS monitors, CDC Environmental Public Health Tracking, satellite-derived estimates, LUR models. Monitor, tract, county, state levels.
- **Consolidation Note:** Replaces former Node 226 "Air Pollution Exposure (Individual)" - same measure at different aggregation levels. Individual exposure IS ambient concentration at residence.
- **Mechanism node_id:** `ambient_pm25` (use for all PM2.5 exposure pathways, including prenatal)
- **Data Source:** EPA Air Quality System (AQS), modeled estimates for areas without monitors (EPA, NASA). County and tract-level, annual.

### Node 125: Climate Vulnerability Index
- **Scale:** 2
- **Domain:** Environmental, Climate, Public Health
- **Type:** Structural Condition
- **Unit:** Index 0-100 (higher = more vulnerable)
- **Description:** Composite index of community vulnerability to climate change impacts, combining: exposure (heat, flood, fire, drought, storm), sensitivity (elderly, children, chronic disease, poverty, housing quality), and adaptive capacity (resources, infrastructure, social cohesion). Identifies communities least able to cope with climate impacts. Index construction varies by source.
- **Baseline:** National median = 45 (2023). Range: 15 (low exposure, high adaptive capacity) to 85 (high exposure, low resources, marginalized communities). Rural poor and urban poor face highest vulnerability. Source: CDC SVI Climate module, EJScreen climate.
- **Data Source:** CDC Social Vulnerability Index (SVI) Climate and Health module, EPA EJScreen climate indicators, FEMA National Risk Index. County and tract-level, updated periodically.

### Node 126: Drought Severity
- **Scale:** 6
- **Domain:** Environmental, Climate
- **Type:** Structural Condition
- **Unit:** Percent of time in moderate/severe drought (5-year average)
- **Description:** Percentage of time (over previous 5 years) an area experienced moderate, severe, or exceptional drought conditions per US Drought Monitor. Drought impacts: water scarcity, agricultural losses, wildfires, economic stress, mental health (rural farmers). Concentrated in West, Plains; increasing frequency with climate change.
- **Baseline:** 18% of US in drought at any given time (2020-2024 average), but varies dramatically by region and year. Western states: 40-60% of time in drought. Source: US Drought Monitor.
- **Data Source:** US Drought Monitor (NOAA, USDA), updated weekly. State and county-level, historical archive for multi-year averages.

### Node 127: Superfund and Toxic Site Proximity
- **Scale:** 1
- **Domain:** Environmental, Public Health
- **Type:** Structural Condition
- **Unit:** Percent of population within 1 mile of Superfund or toxic site
- **Description:** Percentage of population living within 1 mile of an EPA Superfund site, brownfield, or other federally-tracked contaminated site (CERCLA, RCRA). Toxic site proximity associated with cancer, birth defects, respiratory disease. Sites disproportionately in low-income communities and communities of color (environmental racism). Cleanup slow.
- **Baseline:** 16.8% of US population within 1 mile of tracked toxic site (2022). Higher in industrial regions and urban areas. Disparities: 21% of Black population, 18% Hispanic, 14% White. Source: EPA EJScreen.
- **Data Source:** EPA EJScreen (Superfund, RCRA, brownfields), EPA Envirofacts. Tract-level, annual.

### Node 128: Water Insecurity / Quality Violations
- **Scale:** 4
- **Domain:** Environmental, Public Health
- **Type:** Structural Condition
- **Unit:** Percent of population served by systems with health-based violations
- **Description:** Percentage of population served by community water systems that had health-based violations of Safe Drinking Water Act standards in the past year. Violations include: contamination (lead, arsenic, nitrate, PFAS, bacteria), inadequate treatment. Disproportionately affects rural, low-income, tribal communities.
- **Baseline:** 7.2% of population served by violating systems (2022, ~23 million people). Range: <2% to 20%+ (rural areas with underfunded systems). Violations often years-long before remedy. Source: EPA.
- **Data Source:** EPA Safe Drinking Water Information System (SDWIS), Natural Resources Defense Council (NRDC) Watered Down Justice analysis. Water system and county-level, annual.

### Node 129: Urban Heat Island Intensity
- **Scale:** 2
- **Domain:** Environmental, Climate, Built Environment
- **Type:** Structural Condition
- **Unit:** Degrees Fahrenheit warmer than surrounding rural areas
- **Description:** Temperature difference (°F) between urban core and surrounding rural areas during summer, due to heat-absorbing pavement/buildings and lack of tree canopy. Urban heat islands amplify heat wave mortality. Intensity varies by development density and tree canopy. Disparities: low-income neighborhoods often hottest (less canopy, more pavement).
- **Baseline:** Median urban heat island = 7°F warmer (summer daytime, 2023). Range: 2°F (small towns, good tree cover) to 15°F+ (dense, treeless urban cores). Nighttime heat islands can exceed daytime. Source: NASA, NOAA, Climate Central.
- **Data Source:** NASA Landsat satellite surface temperature, NOAA urban heat island assessments, Climate Central urban heat analysis. City and neighborhood-level.

### Node 130: Green Space Access
- **Scale:** 2
- **Domain:** Environmental, Built Environment, Public Health
- **Type:** Structural Condition
- **Unit:** Percent of population within 10-minute walk (1/2 mile) of park
- **Description:** Percentage of residents living within a 10-minute walk (1/2 mile) of a public park or green space. Green space access associated with physical activity, mental health, heat mitigation, social cohesion. "Park deserts" concentrated in low-income areas and communities of color. Measured via GIS.
- **Baseline:** 55% of US population has 10-minute park access (2023). Range: 20% (park deserts in sprawl and disinvested neighborhoods) to 95% (high park access cities). Disparities: 43% of low-income, 62% of high-income. Source: Trust for Public Land.
- **Data Source:** Trust for Public Land ParkServe database (annual), park GIS data, Census blocks. Neighborhood and city-level.

---

**END OF SCALE 1: STRUCTURAL DETERMINANTS (Nodes 1-130)**

**SECTION COMPLETE:** 130 structural nodes covering:
- **Policy Infrastructure** (Nodes 1-80): Healthcare, Housing, Labor, Criminal Justice, Education, Environmental, Infrastructure Investment, Taxation, Trade policy
- **Economic Structure** (Nodes 81-92): Wealth inequality, income, debt, financial access
- **Labor Market Structure** (Nodes 93-102): Job quality, precarious work, wages, occupational hazards
- **Transportation System** (Nodes 103-110): Commute, vehicle dependency, transit, walkability
- **Community Power & Civic** (Nodes 111-120): Voter turnout, organizing, participation, information
- **Climate & Environmental** (Nodes 121-130): Heat, flood, wildfire, air/water quality, green space

---

# SCALE 2: INSTITUTIONAL INFRASTRUCTURE

Local Implementation and Organizational Level - Organizations, facilities, workforce, and local systems that deliver services

---

## 2.1 HEALTHCARE DELIVERY INFRASTRUCTURE

### Node 131: Primary Care Physician Density
- **Scale:** 3 | **Domain:** Healthcare | **Type:** Availability | **Unit:** PCPs per 100k pop
- **Description:** Primary care physicians per 100k population.
- **Baseline:** 75/100k (2023). Range: 40-120. **Source:** HRSA AHRF, annual, county-level.

### Node 132: Specialist Physician Density
- **Scale:** 3 | **Domain:** Healthcare | **Type:** Availability | **Unit:** Specialists per 100k
- **Description:** Specialist physicians per 100k.
- **Baseline:** 140/100k (2023). Range: 50-350+. **Source:** HRSA AHRF, county-level.

### Node 133: FQHC Density
- **Scale:** 3 | **Domain:** Healthcare | **Type:** Availability | **Unit:** FQHCs per 100k
- **Description:** Federally Qualified Health Center sites per 100k.
- **Baseline:** 3.2/100k (2022). Range: 0-15+. **Source:** HRSA UDS, county-level.

### Node 134: Hospital Beds Per Capita
- **Scale:** 3 | **Domain:** Healthcare | **Type:** Availability | **Unit:** Beds per 1k pop
- **Description:** Staffed acute care beds per 1k.
- **Baseline:** 2.4/1k (2023). Range: 1.5-5+. **Source:** AHA Survey, CMS, county-level.

### Node 135: Mental Health Provider Density
- **Scale:** 3 | **Domain:** Healthcare, Behavioral | **Type:** Availability | **Unit:** Providers per 100k
- **Description:** Mental health providers (psychiatrists, psychologists, LCSWs) per 100k.
- **Baseline:** 350/100k (2023). Range: 50-800+. **Source:** HRSA, SAMHSA, county-level.

### Node 136: SUD Treatment Facility Density
- **Scale:** 3 | **Domain:** Healthcare, Behavioral | **Type:** Availability | **Unit:** Facilities per 100k
- **Description:** Substance use disorder treatment facilities per 100k.
- **Baseline:** 11/100k (2023). Range: 2-30+. **Source:** SAMHSA N-SSATS, county-level.

### Node 137: Pharmacy Density
- **Scale:** 3 | **Domain:** Healthcare | **Type:** Availability | **Unit:** Pharmacies per 100k
- **Description:** Retail pharmacies per 100k.
- **Baseline:** 22/100k (2023). Range: 5-40+. **Source:** NCPDP, state boards, county-level.

### Node 138: Emergency Department Availability
- **Scale:** 7 | **Domain:** Healthcare | **Type:** Availability | **Unit:** EDs per 100k
- **Description:** Hospital emergency departments per 100k.
- **Baseline:** 1.1/100k (2023). Range: 0-3+. **Source:** AHA, CMS, county-level.

### Node 139: Nurse-to-Population Ratio
- **Scale:** 3 | **Domain:** Healthcare | **Type:** Availability | **Unit:** RNs per 100k
- **Description:** Registered nurses per 100k.
- **Baseline:** 1,100/100k (2023). Range: 600-1,800. **Source:** HRSA, state boards, county-level.

### Node 140: Hospital Market Concentration
- **Scale:** 3 | **Domain:** Healthcare | **Type:** Quality | **Unit:** HHI 0-10,000
- **Description:** Hospital market HHI. >2,500 = highly concentrated.
- **Baseline:** Median metro HHI=3,200 (2023). Range: 1,500-10,000. **Source:** AHA, metro-level.

---

## 2.2 HOUSING INFRASTRUCTURE

### Node 141: Affordable Housing Units
- **Scale:** 4 | **Domain:** Housing | **Type:** Availability | **Unit:** Units per 100 eligible HH
- **Description:** Subsidized affordable units per 100 households <50% AMI.
- **Baseline:** 37/100 (2023). **Source:** HUD PIH, county-level.

### Node 142: Public Housing Units
- **Scale:** 3 | **Domain:** Housing | **Type:** Availability | **Unit:** Units per 10k pop
- **Description:** Public housing units per 10k.
- **Baseline:** 35/10k (2023). Range: 0-200+. **Source:** HUD PIH, PHA-level.

### Node 143: Housing Choice Vouchers
- **Scale:** 3 | **Domain:** Housing | **Type:** Availability | **Unit:** Vouchers per 10k
- **Description:** Active Section 8 vouchers per 10k.
- **Baseline:** 75/10k (2023). Range: 10-250+. **Source:** HUD PIH, PHA-level.

### Node 144: Permanent Supportive Housing Units
- **Scale:** 3 | **Domain:** Housing, Behavioral | **Type:** Availability | **Unit:** PSH units per 10k
- **Description:** PSH units (housing + services) per 10k.
- **Baseline:** 12/10k (2023). Range: 0-50+. **Source:** HUD HIC, CoC-level.

### Node 145: Emergency Shelter Capacity
- **Scale:** 3 | **Domain:** Housing, Social Services | **Type:** Availability | **Unit:** Beds per 10k
- **Description:** Emergency shelter beds per 10k.
- **Baseline:** 22/10k (2023). Range: 5-80+. **Source:** HUD HIC, CoC-level.

### Node 146: Housing Code Enforcement Capacity
- **Scale:** 3 | **Domain:** Housing | **Type:** Availability | **Unit:** Inspectors per 100k units
- **Description:** Code enforcement inspectors per 100k housing units.
- **Baseline:** 15/100k units (2023). Range: 2-40+. **Source:** Local govt, ICMA, city-level.

### Node 147: Eviction Legal Aid Availability
- **Scale:** 3 | **Domain:** Housing, Legal | **Type:** Availability | **Unit:** Attorneys per 10k renters
- **Description:** Eviction defense attorneys per 10k renter households.
- **Baseline:** 0.5/10k renters (2023). Range: 0-3+. **Source:** LSC, city-level.

---

## 2.3 SOCIAL SERVICES INFRASTRUCTURE

### Node 148: Social Worker Density
- **Scale:** 3 | **Domain:** Social Services | **Type:** Availability | **Unit:** SWs per 100k
- **Description:** Licensed social workers per 100k.
- **Baseline:** 420/100k (2023). Range: 200-700+. **Source:** HRSA, state boards, county-level.

### Node 149: Food Pantry Density
- **Scale:** 3 | **Domain:** Food, Social Services | **Type:** Availability | **Unit:** Pantries per 100k
- **Description:** Emergency food pantries per 100k.
- **Baseline:** 12/100k (2023). Range: 3-30+. **Source:** Feeding America, county-level.

### Node 150: Child Welfare Worker Caseload
- **Scale:** 3 | **Domain:** Child Welfare | **Type:** Quality | **Unit:** Cases per worker
- **Description:** Average children per CPS caseworker. CWLA recommends 12-15.
- **Baseline:** 18 cases/worker (2023). Range: 10-35+. **Source:** CWLA, state CPS, state-level.

### Node 151: DV Shelter Capacity
- **Scale:** 3 | **Domain:** Social Services | **Type:** Availability | **Unit:** Beds per 100k
- **Description:** Domestic violence shelter beds per 100k.
- **Baseline:** 12/100k (2023). Range: 2-30+. **Source:** NNEDV, state-level.

---

## 2.4 EDUCATION INFRASTRUCTURE

### Node 152: School Counselor Ratio
- **Scale:** 3 | **Domain:** Education | **Type:** Quality | **Unit:** Students per counselor
- **Description:** Student-to-counselor ratio. ASCA recommends 250:1.
- **Baseline:** 430:1 (2023). Range: 200:1-800:1. **Source:** ED CRDC, district-level.

### Node 153: School Nurse Ratio
- **Scale:** 3 | **Domain:** Education, Healthcare | **Type:** Quality | **Unit:** Students per nurse
- **Description:** Student-to-nurse ratio. NASN recommends 750:1.
- **Baseline:** 950:1 (2023). Range: 400:1-2,000:1. **Source:** ED CRDC, district-level.

### Node 154: School-Based Health Centers
- **Scale:** 3 | **Domain:** Education, Healthcare | **Type:** Availability | **Unit:** SBHCs per 100 schools
- **Description:** School-based health centers per 100 schools.
- **Baseline:** 8/100 (2023). Range: 0-30+. **Source:** SBHA census, district-level.

### Node 155: Afterschool Program Access
- **Scale:** 3 | **Domain:** Education | **Type:** Availability | **Unit:** % students with access
- **Description:** Percent of K-12 students with afterschool program access.
- **Baseline:** 42% (2023). Range: 20-70%. **Source:** Afterschool Alliance, district-level.

---

## 2.5 BUILT ENVIRONMENT INFRASTRUCTURE

### Node 156: Transit Route Density
- **Scale:** 2 | **Domain:** Transportation | **Type:** Availability | **Unit:** Routes per sq mi
- **Description:** Transit routes per square mile (urbanized).
- **Baseline:** 1.8/sq mi (2023). Range: 0.3-8+. **Source:** FTA NTD, GTFS, metro-level.

### Node 157: Transit Stop Density
- **Scale:** 2 | **Domain:** Transportation | **Type:** Availability | **Unit:** Stops per sq mi
- **Description:** Bus/rail stops per square mile.
- **Baseline:** 45/sq mi (2023). Range: 10-200+. **Source:** GTFS, metro-level.

### Node 158: Bike Lane Mileage
- **Scale:** 2 | **Domain:** Transportation | **Type:** Availability | **Unit:** Miles per 100 sq mi
- **Description:** Bike lane miles per 100 sq mi.
- **Baseline:** 15/100 sq mi (2023). Range: 1-80+. **Source:** Alliance Biking & Walking, city-level.

### Node 159: Sidewalk Completeness
- **Scale:** 2 | **Domain:** Built Environment | **Type:** Quality | **Unit:** % streets with sidewalks
- **Description:** Percent of street miles with sidewalks both sides.
- **Baseline:** 42% (2023). Range: 10-85%. **Source:** Local GIS, city-level.

### Node 160: Park Acreage Per Capita
- **Scale:** 2 | **Domain:** Built Environment | **Type:** Availability | **Unit:** Acres per 1k residents
- **Description:** Park acres per 1k residents.
- **Baseline:** 10.2/1k (2023). Range: 2-40+. **Source:** TPL ParkServe, city-level.

### Node 161: Tree Canopy Coverage
- **Scale:** 2 | **Domain:** Built Environment, Environmental | **Type:** Quality | **Unit:** % land with canopy
- **Description:** Percent of land area with tree canopy.
- **Baseline:** 35% (metros, 2023). Range: 5-70%. **Source:** USFS, NASA, city-level.

### Node 162: Grocery Store Density
- **Scale:** 2 | **Domain:** Food | **Type:** Availability | **Unit:** Stores per 100k
- **Description:** Full-service grocery stores per 100k.
- **Baseline:** 18/100k (2023). Range: 5-35+. **Source:** USDA, NETS, tract-level.

### Node 163: Food Desert Prevalence
- **Scale:** 2 | **Domain:** Food | **Type:** Availability | **Unit:** % pop in food deserts
- **Description:** Percent living >1mi (urban) or >10mi (rural) from grocery + low-income/no vehicle.
- **Baseline:** 13.5% (2023). Range: 2-40%+. **Source:** USDA Food Access Atlas, tract-level.

---

## 2.6 CRIMINAL JUSTICE IMPLEMENTATION

### Node 164: Police Per Capita
- **Scale:** 4 | **Domain:** Criminal Justice | **Type:** Availability | **Unit:** Officers per 100k
- **Description:** Sworn police officers per 100k.
- **Baseline:** 240/100k (2023). Range: 100-500+. **Source:** FBI UCR, city-level.

### Node 165: Jail Capacity
- **Scale:** 3 | **Domain:** Criminal Justice | **Type:** Availability | **Unit:** Jail beds per 100k
- **Description:** Local jail beds per 100k.
- **Baseline:** 260/100k (2023). Range: 100-600+. **Source:** BJS, Vera, county-level.

### Node 166: Drug Court Availability
- **Scale:** 3 | **Domain:** Criminal Justice, Behavioral | **Type:** Availability | **Unit:** Drug courts per 100k
- **Description:** Specialty drug courts per 100k.
- **Baseline:** 0.5/100k (2023). Range: 0-2+. **Source:** NADCP, county-level.

### Node 167: Pretrial Diversion Programs
- **Scale:** 3 | **Domain:** Criminal Justice | **Type:** Availability | **Unit:** Programs per 100k
- **Description:** Pretrial diversion program capacity per 100k.
- **Baseline:** 0.8/100k (2023). Range: 0-3+. **Source:** BJS, local courts, county-level.

### Node 168: Reentry Service Providers
- **Scale:** 3 | **Domain:** Criminal Justice, Social Services | **Type:** Availability | **Unit:** Providers per 100k
- **Description:** Reentry service organizations per 100k.
- **Baseline:** 1.2/100k (2023). Range: 0-5+. **Source:** CSGJC, county-level.

---

## 2.7 PUBLIC HEALTH INFRASTRUCTURE

### Node 169: Public Health Department Staffing
- **Scale:** 3 | **Domain:** Public Health | **Type:** Availability | **Unit:** PH staff per 100k
- **Description:** Local/state public health department FTE staff per 100k.
- **Baseline:** 55/100k (2023, declining). Range: 20-120+. **Source:** NACCHO, ASTHO, county-level.

### Node 170: Immunization Clinic Density
- **Scale:** 3 | **Domain:** Public Health | **Type:** Availability | **Unit:** Clinics per 100k
- **Description:** Immunization clinic sites per 100k.
- **Baseline:** 8/100k (2023). Range: 2-20+. **Source:** CDC, state health depts, county-level.

### Node 171: Disease Surveillance Capacity
- **Scale:** 3 | **Domain:** Public Health | **Type:** Quality | **Unit:** Index 0-10
- **Description:** Public health surveillance system capacity index (reporting, lab, analysis).
- **Baseline:** Median=5.5 (2023). Range: 2-9. **Source:** CDC PHEP, state-level.

### Node 172: WIC Clinic Density
- **Scale:** 3 | **Domain:** Public Health, Food | **Type:** Availability | **Unit:** WIC sites per 100k
- **Description:** WIC program sites per 100k.
- **Baseline:** 6/100k (2023). Range: 1-15+. **Source:** USDA FNS, county-level.

---

## 2.8 WORKPLACE & OCCUPATIONAL INFRASTRUCTURE

### Node 173: OSHA Inspectors Per Workers
- **Scale:** 4 | **Domain:** Occupational Health | **Type:** Availability | **Unit:** Inspectors per 100k workers
- **Description:** Federal + state OSHA inspectors per 100k workers.
- **Baseline:** 2.5/100k workers (2023). Range: 1-5+ (state plans vs federal). **Source:** OSHA, state-level.

### Node 174: Worker Center Density
- **Scale:** 3 | **Domain:** Employment, Labor | **Type:** Availability | **Unit:** Centers per 100k workers
- **Description:** Worker centers (low-wage worker advocacy) per 100k workers.
- **Baseline:** 0.3/100k workers (2023). Range: 0-2+. **Source:** NDWA, NELP, metro-level.

### Node 175: Employee Assistance Programs
- **Scale:** 3 | **Domain:** Employment, Behavioral | **Type:** Availability | **Unit:** % workers with EAP access
- **Description:** Percent of workers with employer-provided EAP access.
- **Baseline:** 65% (2023). Range: 30-90%. **Source:** SHRM, BLS, state-level.

---

## 2.9 ORGANIZATIONAL QUALITY INDICATORS

### Node 176: Cultural Competency Training
- **Scale:** 3 | **Domain:** Healthcare, Social Services | **Type:** Quality | **Unit:** % orgs with training
- **Description:** Percent of health/social service orgs with cultural competency training.
- **Baseline:** 58% (2023). Range: 20-85%. **Source:** HRSA, CLAS standards, state-level.

### Node 177: Interpretation Services Availability
- **Scale:** 3 | **Domain:** Healthcare | **Type:** Quality | **Unit:** % facilities with interpreters
- **Description:** Percent of healthcare facilities with interpretation services for LEP patients.
- **Baseline:** 72% (2023). Range: 40-95%. **Source:** CLAS, state surveys, state-level.

### Node 178: Trauma-Informed Care Adoption
- **Scale:** 4 | **Domain:** Healthcare, Social Services | **Type:** Quality | **Unit:** % orgs trauma-informed
- **Description:** Percent of organizations with trauma-informed care practices.
- **Baseline:** 45% (2023). Range: 15-75%. **Source:** SAMHSA TIC assessment, state-level.

### Node 179: Community Benefit Spending
- **Scale:** 3 | **Domain:** Healthcare | **Type:** Quality | **Unit:** % revenue to community benefit
- **Description:** Nonprofit hospital community benefit spending as % of revenue (IRS requirement).
- **Baseline:** 7.5% (2023). Range: 2-15%. **Source:** IRS 990 Schedule H, hospital-level.

### Node 180: Health IT Interoperability
- **Scale:** 4 | **Domain:** Healthcare | **Type:** Quality | **Unit:** % with EHR interoperability
- **Description:** Percent of providers with interoperable EHR systems.
- **Baseline:** 48% (2023). Range: 20-70%. **Source:** ONC, state-level.

---

**END SCALE 2: Nodes 131-180 (50 institutional nodes)**

# SCALE 3: INDIVIDUAL/HOUSEHOLD CONDITIONS

Lived Experience Level - Actual conditions, resources, exposures, constraints experienced in daily life

---

## 3.1 ECONOMIC SECURITY (INDIVIDUAL)

### Node 181: Household Income (Median)
- **Scale:** 6 | **Domain:** Economic | **Unit:** Median $ annually
- **Baseline:** $74,580 (2023). Range: $45k-$140k+. **Source:** ACS, tract-level.

### Node 182: Poverty Rate
- **Scale:** 6 | **Domain:** Economic | **Unit:** % below FPL
- **Baseline:** 11.5% (2023). Range: 3-40%+. **Source:** ACS, tract-level.

### Node 183: Deep Poverty Rate
- **Scale:** 6 | **Domain:** Economic | **Unit:** % below 50% FPL
- **Baseline:** 5.3% (2023). Range: 1-20%+. **Source:** ACS, tract-level.

### Node 184: Asset Poverty Rate
- **Scale:** 6 | **Domain:** Economic | **Unit:** % lacking 3mo emergency savings
- **Baseline:** 38% (2023). Range: 20-60%+. **Source:** Fed SHED, Prosperity Now.

### Node 185: Unemployment Rate (Local)
- **Scale:** 6 | **Domain:** Employment | **Unit:** % labor force unemployed
- **Baseline:** 3.8% (2023). Range: 2-12%. **Source:** BLS LAUS, county/tract.

### Node 186: Underemployment Rate
- **Scale:** 6 | **Domain:** Employment | **Unit:** % working part-time involuntarily
- **Baseline:** 3.5% (2023). Range: 2-7%. **Source:** BLS CPS, state/metro.

### Node 187: Gig Economy Reliance
- **Scale:** 4 | **Domain:** Employment | **Unit:** % relying on gig work for income
- **Baseline:** 16% (2023). Range: 8-30%. **Source:** JPMChase, Pew, metro.

### Node 188: Multiple Job Holding
- **Scale:** 4 | **Domain:** Employment | **Unit:** % working multiple jobs
- **Baseline:** 7.8% (2023). Range: 4-12%. **Source:** BLS CPS, state.

### Node 189: Benefits Access (Health Insurance from Job)
- **Scale:** 4 | **Domain:** Employment, Healthcare | **Unit:** % workers with employer coverage
- **Baseline:** 54.3% (2023). Range: 35-70%. **Source:** ACS, county.

### Node 190: Retirement Account Access
- **Scale:** 4 | **Domain:** Economic, Employment | **Unit:** % with retirement account
- **Baseline:** 56% (2023). Range: 30-75%. **Source:** Fed SCF, state.

---

## 3.2 HOUSING STABILITY & QUALITY

### Node 191: Housing Cost Burden
- **Scale:** 4 | **Domain:** Housing, Economic | **Unit:** % paying >30% income on housing
- **Baseline:** 30.2% (2023). Range: 18-50%+. **Source:** ACS, tract.

### Node 192: Severe Housing Cost Burden
- **Scale:** 4 | **Domain:** Housing, Economic | **Unit:** % paying >50% income
- **Baseline:** 14.8% (2023). Range: 8-30%+. **Source:** ACS, tract.

### Node 193: Eviction Filing Rate
- **Scale:** 4 | **Domain:** Housing | **Unit:** Filings per 100 renter HH/year
- **Baseline:** 6.3/100 (2023). Range: 2-20+. **Source:** Eviction Lab, county.

### Node 194: Eviction Rate
- **Scale:** 7 | **Domain:** Housing | **Unit:** Evictions per 100 renter HH/year
- **Baseline:** 2.3/100 (2023). Range: 0.5-8+. **Source:** Eviction Lab, county.

### Node 195: Housing Instability
- **Scale:** 4 | **Domain:** Housing | **Unit:** % moved 2+ times in past year
- **Baseline:** 8.2% (2023). Range: 3-18%. **Source:** ACS, SHED, tract.

### Node 196: Homeownership Rate
- **Scale:** 4 | **Domain:** Housing, Economic | **Unit:** % households owning home
- **Baseline:** 66.0% (2023). Range: 35-85%. **Source:** ACS, tract.

### Node 197: Homelessness Rate
- **Scale:** 7 | **Domain:** Housing | **Unit:** Homeless per 10k pop
- **Baseline:** 18/10k (2024). Range: 5-80+. **Source:** HUD PIT Count, CoC.

### Node 198: Unsheltered Homelessness Rate
- **Scale:** 7 | **Domain:** Housing | **Unit:** Unsheltered per 10k
- **Baseline:** 7.5/10k (2024). Range: 1-40+. **Source:** HUD PIT, CoC.

### Node 199: Housing Quality Index (REVISED - Consolidated)
- **Scale:** 2 | **Domain:** Housing | **Unit:** Index 0-100 (higher = better quality)
- **Description:** Composite index of housing quality including: structural deficiencies (plumbing, heating, electrical), physical problems (roof, windows, foundation), code violations, and maintenance adequacy. Based on American Housing Survey (AHS) housing quality indicators. Excludes environmental hazards (see Node 315).
- **Baseline:** National median = 78. Range: 65 (severely deficient) to 95 (excellent condition). **Source:** AHS, local housing inspections.
- **Consolidation Note:** Replaces former "Housing Quality Deficiencies" (Node 199) and "Housing Repair Needs Severe" (former Node 346, now removed).
- **Mechanism node_id:** `housing_quality_index`

### Node 200: Overcrowding Rate
- **Scale:** 5 | **Domain:** Housing | **Unit:** % units >1 person per room
- **Baseline:** 3.2% (2023). Range: 1-12%. **Source:** ACS, tract.

---

## 3.3 HEALTHCARE ACCESS & COVERAGE

### Node 201: Uninsured Rate
- **Scale:** 5 | **Domain:** Healthcare | **Unit:** % without insurance
- **Baseline:** 8.0% (2023). Range: 2-18%. **Source:** ACS, county.

### Node 202: Underinsured Rate
- **Scale:** 5 | **Domain:** Healthcare | **Unit:** % with inadequate coverage
- **Baseline:** 23% insured adults (2023). Range: 15-35%. **Source:** Commonwealth Fund, state.

### Node 203: Usual Source of Care
- **Scale:** 5 | **Domain:** Healthcare | **Unit:** % with usual PCP/clinic
- **Baseline:** 76% (2023). Range: 60-85%. **Source:** BRFSS, state/metro.

### Node 204: Delayed Care Due to Cost
- **Scale:** 5 | **Domain:** Healthcare, Economic | **Unit:** % delayed in past year
- **Baseline:** 11.5% (2023). Range: 6-20%. **Source:** BRFSS, NHIS, state.

### Node 205: Skipped Medication Due to Cost
- **Scale:** 6 | **Domain:** Healthcare, Economic | **Unit:** % skipped meds past year
- **Baseline:** 9.2% (2023). Range: 5-16%. **Source:** BRFSS, state.

### Node 206: Medical Debt (Individuals)
- **Scale:** 6 | **Domain:** Healthcare, Economic | **Unit:** % with medical debt
- **Baseline:** 23% adults (2023). Range: 12-35%. **Source:** KFF, Urban Institute.

### Node 207: Prescription Drug Affordability
- **Scale:** 6 | **Domain:** Healthcare, Economic | **Unit:** % reporting Rx unaffordable
- **Baseline:** 18% (2023). Range: 10-28%. **Source:** KFF, BRFSS.

### Node 208: Preventive Care Utilization
- **Scale:** 6 | **Domain:** Healthcare | **Unit:** % with annual checkup
- **Baseline:** 68% (2023). Range: 55-78%. **Source:** BRFSS, state.

### Node 209: Dental Care Access
- **Scale:** 6 | **Domain:** Healthcare | **Unit:** % with dental visit past year
- **Baseline:** 65% (2023). Range: 50-75%. **Source:** BRFSS, state.

### Node 210: Mental Healthcare Access
- **Scale:** 6 | **Domain:** Healthcare, Behavioral | **Unit:** % needing MH who accessed care
- **Baseline:** 47% (2023). Range: 35-62%. **Source:** NSDUH, state.

---

## 3.4 FOOD SECURITY

### Node 211: Food Insecurity Rate
- **Scale:** 4 | **Domain:** Food | **Unit:** % households food insecure
- **Baseline:** 12.8% (2023). Range: 6-22%. **Source:** USDA, Feeding America, county.

### Node 212: Child Food Insecurity
- **Scale:** 4 | **Domain:** Food, Child | **Unit:** % children in food insecure HH
- **Baseline:** 17.0% (2023). Range: 8-28%. **Source:** Feeding America, county.

### Node 213: SNAP Participation Rate
- **Scale:** 2 | **Domain:** Food, Economic | **Unit:** % eligible participating
- **Baseline:** 82% eligible (2023). Range: 65-92%. **Source:** USDA FNS, state.

### Node 214: WIC Participation
- **Scale:** 2 | **Domain:** Food, Child | **Unit:** % eligible participating
- **Baseline:** 52% eligible (2023). Range: 35-70%. **Source:** USDA FNS, state.

### Node 215: Free/Reduced School Lunch Eligibility
- **Scale:** 3 | **Domain:** Food, Education | **Unit:** % students eligible
- **Baseline:** 50.9% (2023). Range: 20-85%. **Source:** ED NCES, district.

---

## 3.5 TRANSPORTATION ACCESS

### Node 216: Zero-Vehicle Households
- **Scale:** 4 | **Domain:** Transportation | **Unit:** % HH with no vehicle
- **Baseline:** 8.3% (2023). Range: 2-35% (urban). **Source:** ACS, tract.

### Node 217: Long Commute (>60min)
- **Scale:** 4 | **Domain:** Transportation, Employment | **Unit:** % with commute >60min
- **Baseline:** 9.6% workers (2023). Range: 3-25%. **Source:** ACS, tract.

### Node 218: Transit Commute Mode Share
- **Scale:** 4 | **Domain:** Transportation | **Unit:** % commuting by transit
- **Baseline:** 5.0% (2023). Range: <1-35%. **Source:** ACS, tract.

### Node 219: Walk/Bike Commute Share
- **Scale:** 4 | **Domain:** Transportation | **Unit:** % walking/biking
- **Baseline:** 3.2% (2023). Range: 1-15%. **Source:** ACS, tract.

### Node 220: Work-from-Home Rate
- **Scale:** 4 | **Domain:** Employment, Transportation | **Unit:** % WFH
- **Baseline:** 13.4% (2023, post-COVID). Range: 5-40%. **Source:** ACS, tract.

---

## 3.6 EMPLOYMENT CONDITIONS

### Node 221: Low-Wage Work
- **Scale:** 4 | **Domain:** Employment, Economic | **Unit:** % workers earning <$15/hr
- **Baseline:** 28% (2023). Range: 18-42%. **Source:** BLS OES, metro.

### Node 222: Unstable Work Schedule
- **Scale:** 2 | **Domain:** Employment | **Unit:** % with irregular schedules
- **Baseline:** 17% workers (2023). Range: 10-28%. **Source:** Fed SHED, surveys.

### Node 223: Lack of Paid Sick Leave
- **Scale:** 2 | **Domain:** Employment | **Unit:** % workers without paid sick leave
- **Baseline:** 24% (2023). Range: 12-40%. **Source:** BLS NLSY, state.

### Node 224: Workplace Injury Exposure (Individual)
- **Scale:** 2 | **Domain:** Employment, Occupational | **Unit:** % in high-hazard jobs
- **Baseline:** 32% (2023). Range: 18-52%. **Source:** BLS OES.

### Node 225: Workplace Discrimination Experience
- **Scale:** 2 | **Domain:** Employment, Social | **Unit:** % reporting discrimination
- **Baseline:** 14% workers (2023). Range: 8-22%. **Source:** EEOC, surveys.

---

## 3.7 ENVIRONMENTAL EXPOSURES (INDIVIDUAL)

### ~~Node 226: Air Pollution Exposure (Individual)~~ [REMOVED - Consolidated into Node 124]
- **Consolidation Note:** This node measured the same thing as Node 124 (ambient PM2.5 concentration) but at individual residence level. Merged into Node 124 which now works as a bridge node at both structural and individual scales.
- **Migration:** Update all references to use Node 124 `ambient_pm25`

### Node 227: Lead Exposure Prevalence (Children)
- **Scale:** 6 | **Domain:** Environmental, Child | **Unit:** % children BLL ≥5 μg/dL
- **Baseline:** 2.5% (2023, declining). Range: 0.5-12%. **Source:** CDC, state/county.

### Node 228: Noise Exposure
- **Scale:** 2 | **Domain:** Environmental | **Unit:** % exposed to >55dB
- **Baseline:** 35% (2023). Range: 15-60%. **Source:** EPA, DOT, metro.

### Node 229: Extreme Heat Exposure (Individual)
- **Scale:** 2 | **Domain:** Environmental, Climate | **Unit:** Days >100°F heat index
- **Baseline:** 17 days/year (2023). Range: 0-80+. **Source:** NOAA, tract.

### Node 230: Green Space Access (Individual)
- **Scale:** 2 | **Domain:** Environmental | **Unit:** % within 10min walk of park
- **Baseline:** 55% (2023). Range: 20-95%. **Source:** TPL, block.

---

## 3.8 SOCIAL ENVIRONMENT

### Node 231: Social Isolation
- **Scale:** 4 | **Domain:** Social | **Unit:** % socially isolated
- **Baseline:** 24% (2023). Range: 15-38%. **Source:** BRFSS, surveys.

### Node 232: Discrimination Experience
- **Scale:** 6 | **Domain:** Social | **Unit:** % reporting discrimination
- **Baseline:** 31% (2023). Range: 18-50%. **Source:** BRFSS, surveys.

### Node 233: Community Trust
- **Scale:** 6 | **Domain:** Social | **Unit:** % trusting neighbors
- **Baseline:** 54% (2023). Range: 35-72%. **Source:** GSS, surveys.

### Node 234: Neighborhood Safety Perception
- **Scale:** 6 | **Domain:** Social | **Unit:** % feeling safe
- **Baseline:** 71% (2023). Range: 45-88%. **Source:** Gallup, local surveys.

### Node 235: Civic Engagement (Individual)
- **Scale:** 6 | **Domain:** Social, Civic | **Unit:** % participated civically
- **Baseline:** 34% (2022). Range: 22-48%. **Source:** CPS Civic Supp.

---

## 3.9 EDUCATION & DEVELOPMENT

### Node 236: Educational Attainment (<HS)
- **Scale:** 6 | **Domain:** Education | **Unit:** % adults without HS/GED
- **Baseline:** 10.0% (2023). Range: 3-28%. **Source:** ACS, tract.

### Node 237: Bachelor's Degree Attainment
- **Scale:** 4 | **Domain:** Education | **Unit:** % adults with BA+
- **Baseline:** 37.5% (2023). Range: 12-75%. **Source:** ACS, tract.

### Node 238: Early Childhood Education Enrollment
- **Scale:** 6 | **Domain:** Education, Child | **Unit:** % age 3-4 in pre-K
- **Baseline:** 54% (2023). Range: 30-75%. **Source:** ACS, state.

### Node 239: Chronic School Absenteeism
- **Scale:** 3 | **Domain:** Education | **Unit:** % missing 15+ days/year
- **Baseline:** 26% (2023, post-COVID spike). Range: 12-45%. **Source:** ED CRDC, district.

### Node 240: School Suspension Rate
- **Scale:** 6 | **Domain:** Education, Criminal Justice | **Unit:** % students suspended
- **Baseline:** 6.5% (2023). Range: 2-15%. **Source:** ED CRDC, district.

---

## 3.10 STRESS, TRAUMA, & ADVERSITY

### Node 241: Chronic Stress
- **Scale:** 6 | **Domain:** Mental Health | **Unit:** % high chronic stress
- **Baseline:** 32% (2023). Range: 22-45%. **Source:** APA surveys, BRFSS.

### Node 242: Adverse Childhood Experiences (ACEs)
- **Scale:** 6 | **Domain:** Child, Trauma | **Unit:** % adults with 4+ ACEs
- **Baseline:** 12.5% (2023). Range: 8-20%. **Source:** BRFSS ACE module, state.

### Node 243: Intimate Partner Violence
- **Scale:** 6 | **Domain:** Social, Trauma | **Unit:** % experiencing IPV
- **Baseline:** 3.8% past year (2023). Range: 2-6%. **Source:** NISVS, BRFSS.

### Node 244: Gun Violence Exposure
- **Scale:** 6 | **Domain:** Social, Trauma | **Unit:** % witnessed/victim
- **Baseline:** 18% (2023). Range: 10-35%. **Source:** Pew, CDC WONDER.

### Node 244a: Community Violence Exposure [NEW - Added to fill mechanism gap]
- **Scale:** Individual
- **Domain:** Social Environment, Mental Health, Trauma, Child Development
- **Type:** Exposure
- **Unit:** % of residents reporting witnessing or experiencing violence in past year
- **Description:** Individual/household exposure to community violence including: witnessing assault, shooting, stabbing, or other serious violence in neighborhood, being victim of violent crime, OR hearing gunshots regularly in neighborhood. Survey-based measure. Captures trauma exposure beyond official crime statistics (which undercount and don't measure psychological impact). Children's and adolescents' exposure to community violence is particularly harmful for development, mental health, and academic outcomes. Concentrated in racially segregated, economically disinvested neighborhoods.
- **Baseline:**
  - Adults: 12-15% nationally report past-year exposure
  - Children/adolescents: 25-40% in urban areas report lifetime exposure, 10-15% past-year
  - Disparities: 40-60% exposure in high-violence neighborhoods (concentrated poverty, structural disinvestment, Black/Latino communities due to residential segregation)
- **Data Source:** NHIS Social Determinants of Health module, Youth Risk Behavior Survey (YRBS), National Survey of Children's Exposure to Violence (NatSCEV), local community health surveys, PhenX Toolkit violence exposure measures. State and county estimates, limited geographic granularity.
- **Mechanism node_id:** `community_violence_exposure`
- **Consolidation Note:** Previously missing from inventory but referenced in mechanisms linking neighborhood violence to PTSD, depression, asthma exacerbations (stress pathway), adverse birth outcomes, and child developmental outcomes.
- **Related Nodes:** Node 100 (Violent Crime Rate - structural), Node 244 (Gun Violence Exposure - specific type), Node 243 (Intimate Partner Violence - different exposure)

### Node 245: Economic Insecurity Stress
- **Scale:** 6 | **Domain:** Economic, Mental Health | **Unit:** % very/somewhat worried
- **Baseline:** 42% (2023). Range: 28-58%. **Source:** Fed SHED.

---

## 3.11 DIGITAL ACCESS

### Node 246: Digital Inclusion Index [REVISED - Consolidated 4 nodes]
- **Scale:** 6
- **Domain:** Digital Access, Social Determinants
- **Type:** Composite
- **Unit:** Index 0-100 (higher = more digitally included)
- **Description:** Composite index of digital inclusion including: (1) home broadband access (fixed or mobile) - 40%, (2) device ownership (computer/tablet/smartphone adequate for internet use) - 30%, (3) digital literacy skills (able to complete online tasks) - 20%, (4) online services access (banking, government services, e-commerce) - 10%. Based on National Digital Inclusion Alliance framework. Individual/household-level assessment.
- **Baseline:** National mean = 68. Range: 20 (no access, no skills, no use) to 100 (full inclusion across all dimensions). Disparities: lower among elderly (mean=45), rural (mean=58), low-income (mean=52), Black/Hispanic households (mean=62).
- **Data Source:** ACS computer/internet supplement, NTIA Internet Use Survey, Pew Digital Divide surveys, local digital equity assessments. Tract and county-level, annual.
- **Consolidation Note:** Replaces former Nodes 246 (broadband), 247 (device), 248 (literacy), 250 (banking) with comprehensive composite. Components can still be analyzed separately when needed.
- **Mechanism node_id:** `digital_inclusion_index`

### Node 249: Digital Health Access [REVISED - Healthcare-Specific]
- **Scale:** 4
- **Domain:** Digital Access, Healthcare
- **Type:** Access/Availability
- **Unit:** % of individuals able to access telehealth services
- **Description:** Individual/household ability to access telehealth services, including: video visit capability (internet speed + device + platform), audio-only capability (phone access), patient portal access, and remote monitoring device connectivity. Healthcare-specific digital access distinct from general digital inclusion (Node 246). Critical for healthcare access equity.
- **Baseline:** 62% able to access video telehealth (2023). Range: 40% (low digital inclusion areas) to 80% (high inclusion). Audio-only access: 95%. Patient portal access: 52%.
- **Data Source:** HINTS (Health Information National Trends Survey), NHIS telehealth supplement, health system patient portal enrollment data. State and metro-level.
- **Mechanism node_id:** `digital_health_access`

### ~~Node 247: Computer/Device Ownership~~ [REMOVED - Component of Node 246]
- **Migration:** Now component (30%) of Node 246 Digital Inclusion Index

### ~~Node 248: Digital Literacy~~ [REMOVED - Component of Node 246]
- **Migration:** Now component (20%) of Node 246 Digital Inclusion Index

### ~~Node 250: Digital Payment/Banking Access~~ [REMOVED - Component of Node 246]
- **Migration:** Now component (10%) of Node 246 Digital Inclusion Index

---

## 3.12 CRIMINAL JUSTICE CONTACT [SECTION REVISED - 8 nodes consolidated to 4]

### Node 251: Criminal Justice System Contact (Any) [REVISED]
- **Scale:** 4
- **Domain:** Criminal Justice
- **Type:** Binary
- **Unit:** Binary: Any criminal justice contact in lifetime (arrest, conviction, incarceration, supervision)
- **Description:** Whether individual has ever had contact with criminal justice system including: arrest, conviction, incarceration, probation, parole, court supervision, or juvenile justice involvement. Binary indicator of any system involvement. Does not capture intensity or recency. Includes both adult and juvenile system contact.
- **Baseline:** 31% of US adults have been arrested at least once (2023). 46% of Black men arrested by age 23. Range: 18-45% by state/demographic group.
- **Data Source:** Bureau of Justice Statistics (BJS) surveys, National Longitudinal Survey of Youth, state arrest records. State and demographic estimates.
- **Mechanism node_id:** `criminal_justice_contact`
- **Consolidation Note:** Combines former Nodes 251 (arrest), 258 (juvenile) into binary "any contact" measure.

### Node 252: Criminal Justice Involvement Intensity [REVISED - Consolidated]
- **Scale:** 4
- **Domain:** Criminal Justice
- **Type:** Composite
- **Unit:** Index 0-10 (higher = more intensive involvement)
- **Description:** Composite index of criminal justice system involvement intensity including: number of arrests (weighted), felony vs. misdemeanor convictions (weighted), incarceration history (duration weighted), current supervision status (probation/parole), police contact frequency, and recency of involvement. Captures cumulative and current system entanglement. 0 = no contact, 10 = extensive recent intensive involvement. Better predictor of health impacts than binary contact.
- **Baseline:** Among those with any contact: mean = 3.2. Distribution: 0 (no contact, 69%), 1-3 (minimal/past, 18%), 4-6 (moderate, 8%), 7-10 (intensive, 5%).
- **Data Source:** Constructed from BJS data, state corrections data, Vera Institute analyses, research cohorts with detailed criminal justice histories.
- **Mechanism node_id:** `criminal_justice_intensity`
- **Consolidation Note:** Combines former Nodes 252 (incarceration), 253 (felony), 254 (supervision), 256 (police stops) into comprehensive intensity measure.

### Node 255: Criminal Record Barriers [REVISED - Clarified]
- **Scale:** 4
- **Domain:** Criminal Justice, Employment, Housing, Social Determinants
- **Type:** Exposure/Barrier
- **Unit:** Index 0-10 (higher = more barriers)
- **Description:** Extent to which criminal record creates barriers to employment, housing, education, professional licensing, public benefits, and civic participation. Composite of: felony record (y/n weighted), years since conviction, type of offense, background check failures, denials due to record, and jurisdictional collateral consequences. Captures downstream effects of system contact beyond incarceration itself. "Invisible punishment."
- **Baseline:** Among those with records: mean barrier index = 5.2. 46% report record as major employment barrier. 67% with felonies report housing denials. Lifetime earnings loss: 40-50%.
- **Data Source:** NELP surveys, Brennan Center collateral consequences inventory, National Inventory of Collateral Consequences, self-report employment/housing outcomes.
- **Mechanism node_id:** `criminal_record_barriers`
- **Note:** Original Node 255 retained and clarified.

### Node 257: Court-Related Debt [REVISED - Clarified]
- **Scale:** 4
- **Domain:** Criminal Justice, Economic Security
- **Type:** Debt
- **Unit:** Dollars in outstanding court-related financial obligations
- **Description:** Individual debt from court fines, fees, restitution, supervision fees, public defender fees, and other criminal/civil justice financial obligations. Creates economic burden, re-incarceration risk (for non-payment), and credit damage. Concentrated among low-income defendants who cannot pay upfront. Median debt: $1,000-5,000; can exceed $10,000+.
- **Baseline:** 3.2% of US adults have legal financial obligations (2023, ~10M people). Among those with debt: median $2,400, mean $6,800. 40% in collections.
- **Data Source:** Brennan Center for Justice estimates, Fines and Fees Justice Center, state court data, credit bureau collections data.
- **Mechanism node_id:** `court_debt`
- **Note:** Original Node 257 retained and expanded.

### ~~Node 253: Felony Conviction Record~~ [REMOVED - Component of Nodes 252 & 255]
- **Migration:** Now component of Node 252 (intensity) and Node 255 (barriers)

### ~~Node 254: Probation/Parole Status~~ [REMOVED - Component of Node 252]
- **Migration:** Now component of Node 252 (intensity index)

### ~~Node 256: Police Stop Experience~~ [REMOVED - Component of Node 252]
- **Migration:** Now component of Node 252 (intensity index)

### ~~Node 258: Juvenile Justice System Contact~~ [REMOVED - Component of Node 251]
- **Migration:** Now included in Node 251 "any contact" (lifetime includes juvenile)

---

## 3.13 HEALTH STATUS (INDIVIDUAL)

### Node 259: Self-Rated Health (Fair/Poor)
- **Scale:** 4 | **Domain:** Health | **Unit:** % fair/poor health
- **Baseline:** 16.8% adults (2023). Range: 12-25%. **Source:** BRFSS, state.

### Node 260: Disability Status (Any)
- **Scale:** 4 | **Domain:** Health, Disability | **Unit:** % with any disability
- **Baseline:** 13.5% adults (2023). Range: 10-20%. **Source:** ACS, state.

### Node 261: Mobility Disability
- **Scale:** 4 | **Domain:** Health, Disability | **Unit:** % with serious difficulty walking
- **Baseline:** 7.1% adults (2023). Range: 5-12%. **Source:** ACS, state.

### Node 262: Cognitive Disability
- **Scale:** 4 | **Domain:** Health, Disability | **Unit:** % with cognitive difficulty
- **Baseline:** 5.4% adults (2023). Range: 4-9%. **Source:** ACS, state.

### Node 263: Self-Care Disability
- **Scale:** 4 | **Domain:** Health, Disability | **Unit:** % difficulty with self-care
- **Baseline:** 3.7% adults (2023). Range: 2.5-6%. **Source:** ACS, state.

### Node 264: Vision/Hearing Disability
- **Scale:** 6 | **Domain:** Health, Disability | **Unit:** % with vision/hearing difficulty
- **Baseline:** 6.8% adults (2023). Range: 5-11%. **Source:** ACS, state.

### Node 265: Activity Limitation
- **Scale:** 6 | **Domain:** Health, Disability | **Unit:** % limited in usual activities
- **Baseline:** 22% adults (2023). Range: 16-30%. **Source:** NHIS.

### Node 266: Chronic Pain
- **Scale:** 6 | **Domain:** Health | **Unit:** % with chronic pain
- **Baseline:** 20.5% adults (2023). Range: 15-28%. **Source:** NHIS, CDC.

### Node 267: High-Impact Chronic Pain
- **Scale:** 6 | **Domain:** Health | **Unit:** % pain limiting activities
- **Baseline:** 8.0% adults (2023). Range: 5-13%. **Source:** NHIS.

### Node 268: Obesity (Individual)
- **Scale:** 6 | **Domain:** Health | **Unit:** % BMI ≥30
- **Baseline:** 41.9% adults (2023). Range: 28-48%. **Source:** BRFSS, state.

### Node 269: Diabetes Diagnosis
- **Scale:** 6 | **Domain:** Health | **Unit:** % diagnosed diabetic
- **Baseline:** 11.6% adults (2023). Range: 8-16%. **Source:** BRFSS, state.

### Node 270: Hypertension Diagnosis
- **Scale:** 6 | **Domain:** Health | **Unit:** % diagnosed hypertensive
- **Baseline:** 32.9% adults (2023). Range: 25-42%. **Source:** BRFSS, state.

### Node 271: Asthma Prevalence (Adults) [REVISED - Terminology Standardized]
- **Scale:** 6 | **Domain:** Health, Respiratory | **Unit:** % adults with current asthma
- **Description:** Percentage of adults (18+) with current asthma (ever diagnosed AND still have asthma). Distinct from asthma incidence (new diagnoses) and lifetime asthma.
- **Baseline:** 9.0% adults (2023). Range: 7-13% by state. Disparities: Higher among women (10.8%), Black adults (11.1%), low-income. **Source:** BRFSS, state.
- **Mechanism node_id:** `adult_asthma_prevalence`

### Node 272: COPD Prevalence
- **Scale:** 6 | **Domain:** Health | **Unit:** % diagnosed COPD
- **Baseline:** 5.6% adults (2023). Range: 3-10%. **Source:** BRFSS, state.

### Node 273: Heart Disease Prevalence
- **Scale:** 6 | **Domain:** Health | **Unit:** % diagnosed heart disease
- **Baseline:** 6.1% adults (2023). Range: 4-9%. **Source:** BRFSS, state.

### Node 274: Stroke History
- **Scale:** 6 | **Domain:** Health | **Unit:** % ever had stroke
- **Baseline:** 3.1% adults (2023). Range: 2-5%. **Source:** BRFSS, state.

### Node 275: Cancer History
- **Scale:** 6 | **Domain:** Health | **Unit:** % ever diagnosed cancer
- **Baseline:** 6.9% adults (2023). Range: 5-10%. **Source:** BRFSS, state.

### Node 276: Kidney Disease
- **Scale:** 6 | **Domain:** Health | **Unit:** % diagnosed CKD
- **Baseline:** 3.2% adults (2023). Range: 2-5%. **Source:** BRFSS, state.

### Node 277: Depression Diagnosis
- **Scale:** 6 | **Domain:** Mental Health | **Unit:** % diagnosed depression
- **Baseline:** 21.0% adults (2023). Range: 15-28%. **Source:** BRFSS, state.

### Node 278: Anxiety Disorder
- **Scale:** 6 | **Domain:** Mental Health | **Unit:** % diagnosed anxiety
- **Baseline:** 18.5% adults (2023). Range: 12-25%. **Source:** NSDUH, surveys.

### Node 279: Serious Mental Illness (SMI)
- **Scale:** 5 | **Domain:** Mental Health | **Unit:** % SMI past year
- **Baseline:** 5.5% adults (2023). Range: 4-8%. **Source:** NSDUH, state.

### Node 280: Serious Psychological Distress
- **Scale:** 5 | **Domain:** Mental Health | **Unit:** % SPD (K6≥13)
- **Baseline:** 4.8% adults (2023). Range: 3-7%. **Source:** NHIS.

### Node 281: Suicidal Ideation
- **Scale:** 5 | **Domain:** Mental Health | **Unit:** % serious thoughts past year
- **Baseline:** 4.9% adults (2023). Range: 3.5-7%. **Source:** NSDUH, state.

### Node 282: Substance Use Disorder (Any)
- **Scale:** 5 | **Domain:** Behavioral Health | **Unit:** % SUD past year
- **Baseline:** 16.7% age 12+ (2023). Range: 12-22%. **Source:** NSDUH, state.

### Node 283: Alcohol Use Disorder
- **Scale:** 5 | **Domain:** Behavioral Health | **Unit:** % AUD past year
- **Baseline:** 10.6% adults (2023). Range: 7-15%. **Source:** NSDUH, state.

### Node 284: Opioid Use Disorder
- **Scale:** 5 | **Domain:** Behavioral Health | **Unit:** % OUD past year
- **Baseline:** 1.6% age 12+ (2023). Range: 0.8-3%. **Source:** NSDUH, state.

### Node 285: Stimulant Use Disorder
- **Scale:** 5 | **Domain:** Behavioral Health | **Unit:** % stimulant UD past year
- **Baseline:** 1.4% age 12+ (2023). Range: 0.6-2.5%. **Source:** NSDUH.

### Node 286: Illicit Drug Use (Past Month)
- **Scale:** 5 | **Domain:** Behavioral Health | **Unit:** % using illicit drugs
- **Baseline:** 21.4% age 12+ (2023). Range: 15-28%. **Source:** NSDUH, state.

### Node 287: Prescription Opioid Misuse
- **Scale:** 5 | **Domain:** Behavioral Health | **Unit:** % misusing Rx opioids past year
- **Baseline:** 3.4% age 12+ (2023). Range: 2-5%. **Source:** NSDUH, state.

### Node 288: Binge Drinking
- **Scale:** 5 | **Domain:** Behavioral Health | **Unit:** % binge drinking past month
- **Baseline:** 26.0% adults (2023). Range: 18-35%. **Source:** BRFSS, state.

### Node 289: Smoking (Current)
- **Scale:** 5 | **Domain:** Behavioral Health | **Unit:** % current smokers
- **Baseline:** 11.6% adults (2023). Range: 7-23%. **Source:** BRFSS, state.

### Node 290: E-Cigarette Use
- **Scale:** 5 | **Domain:** Behavioral Health | **Unit:** % current vaping
- **Baseline:** 6.0% adults (2023). Range: 3-9%. **Source:** BRFSS, surveys.

---

## 3.14 MATERNAL & CHILD HEALTH (INDIVIDUAL)

### Node 291: Prenatal Care (First Trimester)
- **Scale:** 5 | **Domain:** Maternal Health | **Unit:** % first trimester care
- **Baseline:** 77.6% (2023). Range: 65-88%. **Source:** NVSS, county.

### Node 292: Adequate Prenatal Care
- **Scale:** 5 | **Domain:** Maternal Health | **Unit:** % Kotelchuck adequate+
- **Baseline:** 68.2% (2023). Range: 55-80%. **Source:** NVSS, county.

### Node 293: Pregnancy Intention (Unintended)
- **Scale:** 5 | **Domain:** Maternal Health | **Unit:** % unintended pregnancies
- **Baseline:** 45% (2023). Range: 35-58%. **Source:** PRAMS, Guttmacher.

### Node 294: Maternal Smoking During Pregnancy
- **Scale:** 5 | **Domain:** Maternal Health, Child | **Unit:** % smoking while pregnant
- **Baseline:** 6.0% (2023). Range: 3-15%. **Source:** NVSS, state.

### Node 295: Maternal Chronic Conditions
- **Scale:** 5 | **Domain:** Maternal Health | **Unit:** % prepregnancy chronic disease
- **Baseline:** 28% (2023). Range: 20-38%. **Source:** PRAMS, CDC.

### Node 296: Maternal Postpartum Depression
- **Scale:** 6 | **Domain:** Maternal Health | **Unit:** % postpartum depression
- **Baseline:** 13.2% (2023). Range: 9-19%. **Source:** PRAMS, state.

### Node 297: Breastfeeding Initiation
- **Scale:** 6 | **Domain:** Child Health | **Unit:** % ever breastfed
- **Baseline:** 84.1% (2023). Range: 70-92%. **Source:** NVSS, state.

### Node 298: Breastfeeding Duration (6mo+)
- **Scale:** 6 | **Domain:** Child Health | **Unit:** % breastfeeding 6mo+
- **Baseline:** 58.3% (2023). Range: 45-72%. **Source:** NVSS, surveys, state.

### Node 299: Child Well-Visit Adherence
- **Scale:** 5 | **Domain:** Child Health | **Unit:** % well-child visits on time
- **Baseline:** 72% (2023). Range: 60-85%. **Source:** NCQA HEDIS, Medicaid.

### Node 300: Childhood Vaccination (Complete)
- **Scale:** 5 | **Domain:** Child Health | **Unit:** % fully vaccinated by 24mo
- **Baseline:** 69.8% (2023). Range: 58-82%. **Source:** CDC NIS, state.

### Node 301: Asthma Prevalence (Children 0-17) [REVISED - Terminology Standardized]
- **Scale:** 6 | **Domain:** Child Health, Respiratory | **Unit:** % children with current asthma
- **Description:** Percentage of children ages 0-17 years with current asthma (ever diagnosed AND still have asthma). Age range explicitly 0-17 years. Distinct from asthma incidence (new diagnoses).
- **Baseline:** 7.5% children 0-17 (2023). Range: 5-12% by state. Disparities: Higher among Black children (13.9%), boys (8.4% vs 6.5% girls), low-income families. **Source:** National Survey of Children's Health (NSCH), state.
- **Terminology Note:** Use "child/children" not "childhood" or "pediatric" per standardization.
- **Mechanism node_id:** `child_asthma_prevalence`

### Node 302: Childhood Obesity
- **Scale:** 6 | **Domain:** Child Health | **Unit:** % children obese
- **Baseline:** 19.7% age 2-19 (2023). Range: 12-28%. **Source:** NSCH, state.

### Node 303: Adverse Birth Environment (Maternal ACEs)
- **Scale:** 2 | **Domain:** Child, Maternal | **Unit:** % mothers 4+ ACEs
- **Baseline:** 14% (2023). Range: 9-22%. **Source:** PRAMS ACE module.

### Node 304: Child Special Healthcare Needs
- **Scale:** 2 | **Domain:** Child Health | **Unit:** % children with SHCN
- **Baseline:** 19.8% (2023). Range: 15-26%. **Source:** NSCH, state.

### Node 305: Teen Birth Exposure (Mother Age <20)
- **Scale:** 2 | **Domain:** Maternal, Child | **Unit:** % births to mothers <20
- **Baseline:** 4.6% births (2023). Range: 2-9%. **Source:** NVSS, county.

---

## 3.15 ADDITIONAL CLIMATE & ENVIRONMENTAL EXPOSURES

### Node 306: Extreme Heat Days Exposure
- **Scale:** 2 | **Domain:** Environmental, Climate | **Unit:** Days >95°F annually
- **Baseline:** 18 days (2023). Range: 0-90+. **Source:** NOAA, tract/block.

### Node 307: Wildfire Smoke Exposure
- **Scale:** 2 | **Domain:** Environmental, Climate | **Unit:** Days with unhealthy AQI
- **Baseline:** 8 days (2023). Range: 0-60+. **Source:** EPA AirNow, NOAA HMS.

### Node 308: Flood Risk Exposure (Individual)
- **Scale:** 4 | **Domain:** Environmental, Climate | **Unit:** % in 100-year floodplain
- **Baseline:** 4.2% housing units (2023). Range: 0-35%. **Source:** FEMA NFHL, tract.

### Node 309: Hurricane/Storm Exposure
- **Scale:** 4 | **Domain:** Environmental, Climate | **Unit:** % in high-risk zones
- **Baseline:** 11% coastal (2023). Range: 0-60%. **Source:** NOAA, FEMA, tract.

### Node 310: Drought Exposure
- **Scale:** 4 | **Domain:** Environmental, Climate | **Unit:** % in drought areas
- **Baseline:** 38% (2023, varies). Range: 0-100%. **Source:** US Drought Monitor.

### Node 311: Water Insecurity
- **Scale:** 4 | **Domain:** Environmental | **Unit:** % HH worried about water safety
- **Baseline:** 17% (2023). Range: 8-35%. **Source:** Household Pulse, surveys.

### Node 312: Pesticide Exposure (Residential)
- **Scale:** 2 | **Domain:** Environmental, Occupational | **Unit:** % near agricultural pesticide use
- **Baseline:** 8% (2023). Range: 2-25% (rural). **Source:** EPA, USGS.

### Node 313: Industrial Pollution Proximity
- **Scale:** 2 | **Domain:** Environmental | **Unit:** % within 1mi major emitter
- **Baseline:** 12% (2023). Range: 3-35%. **Source:** EPA TRI, tract.

### Node 314: Drinking Water Contamination Risk
- **Scale:** 2 | **Domain:** Environmental | **Unit:** % served by systems with violations
- **Baseline:** 7.5% (2023). Range: 2-20%. **Source:** EPA SDWIS, county.

### Node 315: Indoor Environmental Hazards Index (REVISED - Expanded)
- **Scale:** 2 | **Domain:** Housing, Environmental | **Unit:** Index 0-100 (higher = more hazards)
- **Description:** Composite index of indoor environmental health hazards including: mold/dampness, pest infestation (rodents, cockroaches), lead paint, asbestos, radon, and inadequate ventilation. Weighted by severity and health impact. Complements Housing Quality Index (Node 199) which focuses on structural quality.
- **Baseline:** National median = 25. Range: 0 (no hazards) to 85 (multiple severe hazards). **Source:** AHS, NHANES environmental home assessment, local health department inspections.
- **Consolidation Note:** Expanded from former "Household Mold/Dampness" to comprehensive environmental hazards composite. Related individual hazard nodes (316: Pests, 317: Radon) remain for specific analyses.
- **Mechanism node_id:** `indoor_environmental_hazards`

### Node 316: Household Pest Infestation
- **Scale:** 2 | **Domain:** Housing, Environmental | **Unit:** % reporting pest problems
- **Baseline:** 14% (2023). Range: 8-28%. **Source:** AHS.

### Node 317: Indoor Radon Exposure
- **Scale:** 2 | **Domain:** Environmental | **Unit:** % homes >4 pCi/L
- **Baseline:** 6.3% (2023). Range: 1-18%. **Source:** EPA radon maps.

### Node 318: PFAS Exposure Risk
- **Scale:** 6 | **Domain:** Environmental | **Unit:** % served by PFAS-detected water
- **Baseline:** 15% (2023 est). Range: 5-40%. **Source:** EPA UCMR, EWG.

---

## 3.16 ADDITIONAL EMPLOYMENT & ECONOMIC CONDITIONS

### Node 319: Multiple Job Holding
- **Scale:** 6 | **Domain:** Employment, Economic | **Unit:** % with 2+ jobs
- **Baseline:** 7.8% employed (2023). Range: 5-12%. **Source:** CPS, state.

### Node 320: Underemployment
- **Scale:** 6 | **Domain:** Employment, Economic | **Unit:** % part-time for economic reasons
- **Baseline:** 6.1% labor force (2023). Range: 4-10%. **Source:** BLS LAUS, state.

### Node 321: Job Insecurity Perception
- **Scale:** 4 | **Domain:** Employment | **Unit:** % worried about job loss
- **Baseline:** 18% employed (2023). Range: 12-28%. **Source:** Fed SHED, surveys.

### Node 322: Gig/Contract Work
- **Scale:** 4 | **Domain:** Employment | **Unit:** % contingent workers
- **Baseline:** 10.6% (2023). Range: 7-16%. **Source:** BLS CWS, surveys.

### Node 323: Retirement Savings Access
- **Scale:** 4 | **Domain:** Employment, Economic | **Unit:** % with employer retirement plan
- **Baseline:** 56% workers (2023). Range: 42-68%. **Source:** BLS NCS, state.

### Node 324: Paid Family Leave Access
- **Scale:** 4 | **Domain:** Employment | **Unit:** % with paid family leave
- **Baseline:** 27% workers (2023). Range: 15-90%. **Source:** BLS NCS, state.

### Node 325: Workplace Flexibility
- **Scale:** 4 | **Domain:** Employment | **Unit:** % with flexible schedules
- **Baseline:** 38% (2023). Range: 25-55%. **Source:** BLS, surveys.

### Node 326: Union Membership
- **Scale:** 4 | **Domain:** Employment, Labor | **Unit:** % workers unionized
- **Baseline:** 10.1% (2023). Range: 2-23%. **Source:** BLS, state.

### Node 327: Wage Theft Experience
- **Scale:** 6 | **Domain:** Employment, Economic | **Unit:** % reporting wage violations
- **Baseline:** 8.5% (2023). Range: 5-14%. **Source:** EPI surveys, DOL data.

### Node 328: Occupational Licensing Burden
- **Scale:** 6 | **Domain:** Employment | **Unit:** % in licensed occupations
- **Baseline:** 22% workers (2023). Range: 12-33%. **Source:** DOL, state studies.

---

## 3.17 ADDITIONAL SOCIAL & CIVIC ENVIRONMENT

### Node 329: Social Support (Low)
- **Scale:** 6 | **Domain:** Social Environment | **Unit:** % low social support
- **Baseline:** 18% (2023). Range: 12-28%. **Source:** BRFSS, surveys.

### Node 330: Loneliness
- **Scale:** 6 | **Domain:** Social, Mental Health | **Unit:** % often/always lonely
- **Baseline:** 22% adults (2023). Range: 15-32%. **Source:** BRFSS, surveys.

### Node 331: Civic Participation
- **Scale:** 4 | **Domain:** Civic | **Unit:** % voted in last election
- **Baseline:** 66% eligible (2020 pres). Range: 50-78%. **Source:** Census CPS, state.

### Node 332: Volunteer Rate
- **Scale:** 4 | **Domain:** Civic, Social | **Unit:** % volunteering
- **Baseline:** 28.3% (2023). Range: 20-42%. **Source:** AmeriCorps, CPS, state.

### Node 333: Organizational Membership
- **Scale:** 4 | **Domain:** Social, Civic | **Unit:** % belonging to organizations
- **Baseline:** 42% (2023). Range: 30-58%. **Source:** Surveys.

### Node 334: Religious Participation
- **Scale:** 4 | **Domain:** Social | **Unit:** % attending weekly+
- **Baseline:** 27% (2023). Range: 15-45%. **Source:** Pew, Gallup.

### Node 335: Neighborhood Trust
- **Scale:** 4 | **Domain:** Social | **Unit:** % trust most neighbors
- **Baseline:** 52% (2023). Range: 35-68%. **Source:** BRFSS, surveys.

### Node 336: Experienced Discrimination (Any Domain)
- **Scale:** 4 | **Domain:** Social | **Unit:** % reporting discrimination
- **Baseline:** 31% (2023). Range: 20-48% (varies by group). **Source:** RWJF surveys.

### Node 337: Language Barriers (LEP)
- **Scale:** 4 | **Domain:** Social, Healthcare | **Unit:** % limited English proficiency
- **Baseline:** 8.2% (2023). Range: 1-25%. **Source:** ACS, state.

### Node 338: Immigration Status Insecurity
- **Scale:** 4 | **Domain:** Social | **Unit:** % undocumented
- **Baseline:** 3.2% pop (2023). Range: 0.5-8%. **Source:** Pew, MPI, state.

---

## 3.18 ADDITIONAL HOUSING CONDITIONS

### Node 339: Household Crowding
- **Scale:** 4 | **Domain:** Housing | **Unit:** % >1 person/room
- **Baseline:** 3.2% (2023). Range: 1-12%. **Source:** ACS, tract.

### Node 340: Multigenerational Households
- **Scale:** 4 | **Domain:** Housing, Social | **Unit:** % HH with 3+ generations
- **Baseline:** 5.1% (2023). Range: 2-12%. **Source:** ACS, state.

### Node 341: Housing Instability (Multiple Moves)
- **Scale:** 4 | **Domain:** Housing | **Unit:** % moved 2+ times past year
- **Baseline:** 4.8% (2023). Range: 2-9%. **Source:** Surveys, ACS.

### Node 342: Utility Shutoff Experience
- **Scale:** 4 | **Domain:** Housing, Economic | **Unit:** % had utility shut off
- **Baseline:** 5.2% past year (2023). Range: 2-10%. **Source:** Household Pulse, surveys.

### Node 343: Housing Discrimination Experience
- **Scale:** 2 | **Domain:** Housing, Social | **Unit:** % reporting housing discrimination
- **Baseline:** 6.5% (2023). Range: 3-12%. **Source:** HUD HFEO, surveys.

### Node 344: Lack of Kitchen Facilities
- **Scale:** 2 | **Domain:** Housing | **Unit:** % HH lacking complete kitchen
- **Baseline:** 2.1% (2023). Range: 0.8-8%. **Source:** ACS, tract.

### Node 345: Lack of Plumbing
- **Scale:** 2 | **Domain:** Housing | **Unit:** % HH lacking complete plumbing
- **Baseline:** 0.5% (2023). Range: 0.1-8% (rural/tribal). **Source:** ACS, tract.

### ~~Node 346: Housing Repair Needs (Severe)~~ [REMOVED - Consolidated into Node 199]
- **Consolidation Note:** This node has been merged into Node 199 "Housing Quality Index" which now includes all structural and physical housing problems as a comprehensive composite measure.
- **Migration:** Update all references to use Node 199 `housing_quality_index`

### Node 347: Heating/Cooling Adequacy
- **Scale:** 4 | **Domain:** Housing, Energy | **Unit:** % unable to maintain temp
- **Baseline:** 8.3% (2023). Range: 4-16%. **Source:** AHS, EIA RECS.

---

## 3.19 ADDITIONAL HEALTHCARE & DISABILITY

### Node 348: Caregiver Burden
- **Scale:** 4 | **Domain:** Health, Social | **Unit:** % unpaid caregivers
- **Baseline:** 19.2% adults (2023). Range: 14-26%. **Source:** BRFSS, surveys.

### Node 349: Need for Personal Care Assistance
- **Scale:** 4 | **Domain:** Disability, LTSS | **Unit:** % needing help with ADLs
- **Baseline:** 6.8% adults (2023). Range: 5-11%. **Source:** NHIS, ACS.

### Node 350: Unmet LTSS Need
- **Scale:** 4 | **Domain:** Disability, LTSS | **Unit:** % needing but not receiving help
- **Baseline:** 2.4% (2023). Range: 1.5-4%. **Source:** NSLTCP, surveys.

### Node 351: Nursing Home Residence
- **Scale:** 5 | **Domain:** LTSS | **Unit:** % in nursing facilities
- **Baseline:** 1.0% age 65+ (2023). Range: 0.6-2.5%. **Source:** CMS, CDC.

### Node 352: Assisted Living Residence
- **Scale:** 5 | **Domain:** LTSS | **Unit:** % in assisted living
- **Baseline:** 1.8% age 65+ (2023). Range: 1-3.5%. **Source:** NCHS, industry.

### Node 353: Vision Impairment
- **Scale:** 5 | **Domain:** Health, Disability | **Unit:** % difficulty seeing
- **Baseline:** 4.6% (2023). Range: 3-7%. **Source:** NHIS, ACS.

### Node 354: Hearing Impairment
- **Scale:** 5 | **Domain:** Health, Disability | **Unit:** % difficulty hearing
- **Baseline:** 5.9% adults (2023). Range: 4-10%. **Source:** NHIS, ACS.

### Node 355: Medication Adherence (Low)
- **Scale:** 5 | **Domain:** Healthcare | **Unit:** % not taking meds as prescribed
- **Baseline:** 30% chronic disease patients (2023). Range: 20-45%. **Source:** Surveys, MEPS.

### Node 356: Specialist Access Delay
- **Scale:** 5 | **Domain:** Healthcare | **Unit:** % delayed specialist care needed
- **Baseline:** 12% (2023). Range: 7-19%. **Source:** MEPS, surveys.

### Node 357: Emergency Department Utilization (Frequent)
- **Scale:** 5 | **Domain:** Healthcare | **Unit:** % 4+ ED visits/year
- **Baseline:** 2.8% (2023). Range: 1.5-5%. **Source:** MEPS, state all-payer.

### Node 358: Hospitalization (Past Year)
- **Scale:** 5 | **Domain:** Healthcare | **Unit:** % hospitalized
- **Baseline:** 8.5% (2023). Range: 6-12%. **Source:** MEPS, NHIS.

### Node 359: Preventable Hospitalization (Individual)
- **Scale:** 5 | **Domain:** Healthcare | **Unit:** % with ambulatory-sensitive admission
- **Baseline:** 1.8% Medicare (2023). Range: 1-3.5%. **Source:** CMS, county.

### Node 360: Telemedicine Use
- **Scale:** 5 | **Domain:** Healthcare, Digital | **Unit:** % used telehealth past year
- **Baseline:** 37% (2023). Range: 25-52%. **Source:** HINTS, surveys.

---

## 3.20 ADDITIONAL FOOD & NUTRITION [SECTION REVISED - Consolidated]

### Node 361: Diet Quality Index (HEI-2015) [REVISED - Primary Measure]
- **Scale:** 5
- **Domain:** Health Behaviors, Food Security, Nutrition
- **Type:** Quality/Intensity
- **Unit:** Healthy Eating Index (HEI) score 0-100 (higher = better diet quality)
- **Description:** Healthy Eating Index 2015 score measuring overall diet quality based on adherence to Dietary Guidelines for Americans. Components include: total fruits, whole fruits, total vegetables, greens/beans, whole grains, dairy, total protein foods, seafood/plant proteins, fatty acids ratio, refined grains, sodium, added sugars, saturated fats (13 components). Gold standard comprehensive diet quality measure. Individual-level assessment via 24-hour dietary recall or food frequency questionnaire.
- **Baseline:** National mean HEI = 58 out of 100 (2023, "needs improvement"). Distribution: <50 (poor, 22%), 50-80 (needs improvement, 68%), >80 (good, 10%). Disparities: lower among low-income (mean=52), food insecure (mean=49), Black (mean=54), Hispanic (mean=57) compared to White (mean=61).
- **Data Source:** NHANES dietary recall (24-hour), food frequency questionnaires, What We Eat in America survey. National and demographic estimates, limited geographic granularity.
- **Mechanism node_id:** `diet_quality_hei`
- **Consolidation Note:** Replaces former low-quality framing with comprehensive index. Former Node 362 (fruits/vegetables) and Node 364 (fast food) are components of HEI and should not be modeled separately.

### Node 363: Sugar-Sweetened Beverage (SSB) Consumption [RETAINED - Policy-Relevant]
- **Scale:** 6
- **Domain:** Health Behaviors, Nutrition
- **Type:** Behavior
- **Unit:** Servings per day OR % consuming ≥1 serving/day
- **Description:** Daily consumption of sugar-sweetened beverages including soda, fruit drinks (not 100% juice), sports drinks, energy drinks, and sweetened coffee/tea. Kept separate from general HEI because: (1) specific target of soda tax policies, (2) strong independent association with obesity, diabetes, cardiovascular disease, (3) measurable via single survey question. Complements HEI (SSB is component of added sugars score).
- **Baseline:** 28% of adults consume SSB daily (2023). Mean among consumers: 1.8 servings/day. Range: 18% (lowest consumption states) to 42% (highest). Disparities: Higher among youth (45%), Black adults (42%), Hispanic adults (38%), low-income (35%).
- **Data Source:** BRFSS, NHANES 24-hour recall, Youth Risk Behavior Survey (YRBS). State-level, annual.
- **Mechanism node_id:** `ssb_consumption`
- **Rationale for keeping separate:** Policy target (soda taxes implemented in 8 jurisdictions), strong independent health effects, simple measurement.

### ~~Node 362: Fruit/Vegetable Consumption (Low)~~ [REMOVED - Component of Node 361]
- **Migration:** Now captured in Node 361 HEI (fruits and vegetables are 4 of 13 components). Use HEI for diet quality mechanisms.

### ~~Node 364: Fast Food Frequency~~ [REMOVED - Captured in Node 361]
- **Migration:** Fast food frequency is captured in HEI components (refined grains, saturated fats, added sugars, sodium). Use Node 361 HEI for overall diet quality pathways.

### Node 365: Food Assistance Receipt (Any)
- **Scale:** 4 | **Domain:** Food, Economic | **Unit:** % receiving any food assistance
- **Baseline:** 18% (2023). Range: 10-28%. **Source:** ACS, USDA, state.

---

## 3.21 ADDITIONAL FINANCIAL STRESS

### Node 366: Emergency Savings (Lacking)
- **Scale:** 4 | **Domain:** Economic | **Unit:** % unable to cover $400 emergency
- **Baseline:** 37% (2023). Range: 28-50%. **Source:** Fed SHED.

### Node 367: Checking/Savings Account (Unbanked)
- **Scale:** 4 | **Domain:** Economic | **Unit:** % no bank account
- **Baseline:** 4.5% HH (2023). Range: 2-10%. **Source:** FDIC, state.

### Node 368: Underbanked Status
- **Scale:** 4 | **Domain:** Economic | **Unit:** % using alternative financial services
- **Baseline:** 14.1% HH (2023). Range: 8-22%. **Source:** FDIC, state.

### Node 369: Payday Loan Use
- **Scale:** 4 | **Domain:** Economic | **Unit:** % used payday loan past year
- **Baseline:** 5.3% (2023). Range: 2-9%. **Source:** FDIC, Pew.

### Node 370: Credit Card Debt (High)
- **Scale:** 4 | **Domain:** Economic | **Unit:** % carrying high CC debt (>$5k)
- **Baseline:** 28% HH (2023). Range: 18-40%. **Source:** Fed SCF, surveys.

### Node 371: Student Loan Debt
- **Scale:** 4 | **Domain:** Economic, Education | **Unit:** % with student loans
- **Baseline:** 34% adults <40 (2023). Range: 22-48%. **Source:** Fed SCF, state.

### Node 372: Collections/Derogatory Marks
- **Scale:** 4 | **Domain:** Economic | **Unit:** % with debt in collections
- **Baseline:** 28% credit records (2023). Range: 18-42%. **Source:** CFPB, Urban Inst.

### Node 373: Credit Score (Subprime)
- **Scale:** 5 | **Domain:** Economic | **Unit:** % credit score <620
- **Baseline:** 18% (2023). Range: 12-28%. **Source:** CFPB, FICO estimates.

### Node 374: Bankruptcy (Recent)
- **Scale:** 5 | **Domain:** Economic | **Unit:** % filed past 2 years
- **Baseline:** 0.4% annually (2023). Range: 0.2-0.7%. **Source:** Courts, ABI.

### Node 375: Tax Refund Dependence
- **Scale:** 5 | **Domain:** Economic | **Unit:** % relying on EITC/refund
- **Baseline:** 14% filers (2023). Range: 8-22%. **Source:** IRS, state.

---

## 3.22 MISCELLANEOUS INDIVIDUAL CONDITIONS

### Node 376: Sleep Duration (Inadequate)
- **Scale:** 5 | **Domain:** Health | **Unit:** % <7 hours nightly
- **Baseline:** 35.2% adults (2023). Range: 28-45%. **Source:** BRFSS, state.

### Node 377: Physical Activity (Insufficient)
- **Scale:** 5 | **Domain:** Health | **Unit:** % not meeting guidelines
- **Baseline:** 77.6% adults (2023). Range: 68-85%. **Source:** BRFSS, state.

### Node 378: Sedentary Behavior
- **Scale:** 5 | **Domain:** Health | **Unit:** % sitting 8+ hours/day
- **Baseline:** 26% employed adults (2023). Range: 18-38%. **Source:** NHIS, surveys.

### Node 379: Flu Vaccination
- **Scale:** 5 | **Domain:** Healthcare, Prevention | **Unit:** % flu shot past year
- **Baseline:** 48.5% (2023). Range: 38-62%. **Source:** BRFSS, state.

### Node 380: COVID-19 Vaccination (Complete Primary)
- **Scale:** 5 | **Domain:** Healthcare, Prevention | **Unit:** % completed primary series
- **Baseline:** 69% (2023). Range: 52-82%. **Source:** CDC, state.

### Node 381: Cancer Screening (Colorectal)
- **Scale:** 5 | **Domain:** Healthcare, Prevention | **Unit:** % age 50-75 screened
- **Baseline:** 69.7% (2023). Range: 60-78%. **Source:** BRFSS, state.

### Node 382: Cancer Screening (Breast)
- **Scale:** 5 | **Domain:** Healthcare, Prevention | **Unit:** % women 50-74 mammogram
- **Baseline:** 76.4% (2023). Range: 68-84%. **Source:** BRFSS, state.

### Node 383: Cancer Screening (Cervical)
- **Scale:** 5 | **Domain:** Healthcare, Prevention | **Unit:** % women 21-65 screened
- **Baseline:** 81.1% (2023). Range: 72-88%. **Source:** BRFSS, state.

### Node 384: Dental Insurance
- **Scale:** 4 | **Domain:** Healthcare | **Unit:** % with dental coverage
- **Baseline:** 56% adults (2023). Range: 45-68%. **Source:** BRFSS, surveys.

### Node 385: Vision Insurance
- **Scale:** 4 | **Domain:** Healthcare | **Unit:** % with vision coverage
- **Baseline:** 52% (2023). Range: 40-65%. **Source:** Surveys.

### Node 386: Birth Control Access/Use
- **Scale:** 6 | **Domain:** Healthcare, Maternal | **Unit:** % using contraception
- **Baseline:** 65% women 15-49 (2023). Range: 55-75%. **Source:** NSFG.

### Node 387: STI Diagnosis (Past Year)
- **Scale:** 6 | **Domain:** Health | **Unit:** % diagnosed STI
- **Baseline:** 3.2% sexually active (2023). Range: 1.5-6%. **Source:** CDC STD Surveillance.

### Node 388: HIV Status (Diagnosed)
- **Scale:** 5 | **Domain:** Health | **Unit:** Rate per 100k living with diagnosed HIV
- **Baseline:** 380/100k (2023). Range: 150-850. **Source:** CDC HIV Surveillance.

### Node 389: Hepatitis C Prevalence
- **Scale:** 6 | **Domain:** Health | **Unit:** % anti-HCV positive
- **Baseline:** 1.0% adults (2023). Range: 0.5-2.5%. **Source:** CDC, NHANES.

### Node 390: Prescription Drug Coverage
- **Scale:** 5 | **Domain:** Healthcare | **Unit:** % with Rx coverage
- **Baseline:** 86% (2023). Range: 78-92%. **Source:** MEPS, KFF.

### Node 391: Out-of-Pocket Medical Spending
- **Scale:** 5 | **Domain:** Healthcare, Economic | **Unit:** Median annual OOP $
- **Baseline:** $1,200 (2023). Range: $400-$3,500. **Source:** MEPS.

### Node 392: Cost-Related Medication Nonadherence
- **Scale:** 5 | **Domain:** Healthcare, Economic | **Unit:** % skipped meds due to cost
- **Baseline:** 18% (2023). Range: 12-28%. **Source:** KFF, MEPS.

### Node 393: Delayed Care Due to Transportation
- **Scale:** 5 | **Domain:** Healthcare, Transportation | **Unit:** % delayed care—transport barrier
- **Baseline:** 5.6% (2023). Range: 3-11%. **Source:** MEPS, surveys.

### Node 394: Delayed Care Due to Cost
- **Scale:** 5 | **Domain:** Healthcare, Economic | **Unit:** % delayed care—cost barrier
- **Baseline:** 26% (2023). Range: 18-38%. **Source:** MEPS, KFF.

### Node 395: Health Literacy (Low)
- **Scale:** 5 | **Domain:** Healthcare | **Unit:** % below basic health literacy
- **Baseline:** 12% adults (2023). Range: 8-20%. **Source:** NAAL, PIAAC.

### Node 396: Medical Mistrust
- **Scale:** 6 | **Domain:** Healthcare, Social | **Unit:** % low trust in healthcare system
- **Baseline:** 28% (2023). Range: 18-48% (varies by group). **Source:** Surveys.

### Node 397: Usual Source of Care
- **Scale:** 6 | **Domain:** Healthcare | **Unit:** % with usual source
- **Baseline:** 77.5% (2023). Range: 68-86%. **Source:** NHIS, state.

### Node 398: Patient-Centered Medical Home Access
- **Scale:** 6 | **Domain:** Healthcare | **Unit:** % attributed to PCMH
- **Baseline:** 35% (2023). Range: 20-55%. **Source:** NCQA, state.

### Node 399: Chronic Disease Self-Management Support
- **Scale:** 6 | **Domain:** Healthcare | **Unit:** % chronic patients in self-mgmt programs
- **Baseline:** 18% (2023). Range: 10-30%. **Source:** BRFSS, surveys.

### Node 400: Advance Directive Completion
- **Scale:** 2 | **Domain:** Healthcare, LTSS | **Unit:** % with advance directive
- **Baseline:** 37% adults (2023). Range: 28-52%. **Source:** BRFSS, surveys.

---

**END SCALE 3: Nodes 181-400 (220 nodes total). Individual/Household Conditions complete.**

**PROGRESS: 400/850 (47%)**

---
---

# SCALE 4: INTERMEDIATE PATHWAYS (~150 NODES)

*Scale 4 captures intermediate processes and states that mediate between structural/individual conditions (Scales 1-3) and crisis endpoints (Scale 5). These include healthcare utilization patterns, biological risk factors, health behaviors enacted, disease management processes, environmental pathway exposures, and allostatic load markers.*

---

## 4.1 HEALTHCARE UTILIZATION PATTERNS

### Node 401: Primary Care Visit Rate
- **Scale:** 4 | **Domain:** Healthcare | **Unit:** Avg visits per person annually
- **Baseline:** 3.2 visits/year (2023). Range: 2.0-4.5. **Source:** MEPS, Medicare.

### Node 402: Specialist Visit Rate
- **Scale:** 4 | **Domain:** Healthcare | **Unit:** Avg specialist visits annually
- **Baseline:** 1.8 visits/year (2023). Range: 1.0-3.0. **Source:** MEPS.

### Node 403: Emergency Department Visit Rate
- **Scale:** 7 | **Domain:** Healthcare | **Unit:** ED visits per 1k pop
- **Baseline:** 420/1k (2023). Range: 280-650. **Source:** HCUP NEDS, state.

### Node 404: Avoidable ED Visit Rate
- **Scale:** 7 | **Domain:** Healthcare | **Unit:** Avoidable ED visits per 1k
- **Baseline:** 180/1k (2023). Range: 120-280. **Source:** HCUP, NYU algorithm.

### Node 405: Inpatient Admission Rate
- **Scale:** 6 | **Domain:** Healthcare | **Unit:** Admissions per 1k pop
- **Baseline:** 95/1k (2023). Range: 70-140. **Source:** HCUP NIS, state.

### Node 406: Ambulatory Care-Sensitive Admission Rate
- **Scale:** 6 | **Domain:** Healthcare | **Unit:** ACSC admissions per 1k Medicare
- **Baseline:** 48/1k (2023). Range: 30-80. **Source:** CMS, county.

### Node 407: 30-Day Hospital Readmission Rate
- **Scale:** 3 | **Domain:** Healthcare | **Unit:** % readmitted within 30 days
- **Baseline:** 15.5% (2023). Range: 12-21%. **Source:** CMS, hospital.

### Node 408: Preventive Service Utilization (Composite)
- **Scale:** 6 | **Domain:** Healthcare | **Unit:** % receiving age-appropriate prevention
- **Baseline:** 62% (2023). Range: 48-75%. **Source:** MEPS, HEDIS.

### Node 409: Mental Health Service Utilization Rate
- **Scale:** 6 | **Domain:** Healthcare, Behavioral | **Unit:** MH visits per 1k pop
- **Baseline:** 285/1k (2023). Range: 150-450. **Source:** MEPS, Medicaid.

### Node 410: SUD Treatment Entry Rate
- **Scale:** 6 | **Domain:** Healthcare, Behavioral | **Unit:** Treatment admissions per 1k need
- **Baseline:** 185/1k needing (2023). Range: 100-320. **Source:** SAMHSA TEDS.

### Node 411: Medication Fill Rate (Chronic Disease)
- **Scale:** 6 | **Domain:** Healthcare | **Unit:** Proportion of days covered (PDC)
- **Baseline:** 0.68 PDC (2023). Range: 0.50-0.82. **Source:** NCQA, PQA.

### Node 412: Dental Service Utilization
- **Scale:** 6 | **Domain:** Healthcare | **Unit:** Dental visits per person annually
- **Baseline:** 0.9 visits/year (2023). Range: 0.5-1.4. **Source:** ADA, MEPS.

### Node 413: Home Health Visit Rate
- **Scale:** 6 | **Domain:** Healthcare, LTSS | **Unit:** Home health episodes per 1k Medicare
- **Baseline:** 82/1k (2023). Range: 45-150. **Source:** CMS, state.

### Node 414: Observation Stay Rate
- **Scale:** 6 | **Domain:** Healthcare | **Unit:** Obs stays per 1k pop
- **Baseline:** 28/1k (2023). Range: 15-45. **Source:** HCUP, CMS.

### Node 415: Outpatient Surgery Rate
- **Scale:** 6 | **Domain:** Healthcare | **Unit:** Outpatient surgeries per 1k
- **Baseline:** 65/1k (2023). Range: 45-95. **Source:** HCUP, NSAS.

---

## 4.2 CHRONIC DISEASE MANAGEMENT & CONTROL

### Node 416: Diabetes Control (HbA1c <8%)
- **Scale:** 6 | **Domain:** Health | **Unit:** % diabetics with HbA1c <8%
- **Baseline:** 64% (2023). Range: 52-75%. **Source:** HEDIS, BRFSS.

### Node 417: Hypertension Control (<140/90)
- **Scale:** 6 | **Domain:** Health | **Unit:** % hypertensives controlled
- **Baseline:** 48% (2023). Range: 38-62%. **Source:** NHANES, HEDIS.

### Node 418: Asthma Control Rate [REVISED - Clarified]
- **Scale:** 6 | **Domain:** Health, Respiratory, Chronic Disease Management | **Unit:** % of persons with asthma who have well-controlled asthma
- **Description:** Among persons with diagnosed asthma (all ages), the percentage with well-controlled asthma based on: symptom frequency, nighttime awakenings, activity limitation, and rescue inhaler use. Analogous to HbA1c control for diabetes. Measured via validated Asthma Control Test (ACT) or clinical assessment. Well-controlled = ACT ≥20 or meeting NAEPP guidelines.
- **Baseline:** 56% of persons with asthma are well-controlled (2023). Range: 42-68% by state/population. Lower control among low-income, Black/Hispanic, uninsured, and Medicaid enrollees. **Source:** BRFSS asthma call-back surveys, HEDIS, research surveys.
- **Mechanism node_id:** `asthma_control_rate`

### Node 419: Cholesterol Management (Statin Use)
- **Scale:** 6 | **Domain:** Health | **Unit:** % high-risk on statins
- **Baseline:** 71% (2023). Range: 60-82%. **Source:** HEDIS, MEPS.

### Node 420: Depression Treatment Adherence
- **Scale:** 5 | **Domain:** Mental Health | **Unit:** % depressed receiving adequate Rx
- **Baseline:** 42% (2023). Range: 30-58%. **Source:** HEDIS, NSDUH.

### Node 421: HIV Viral Suppression
- **Scale:** 5 | **Domain:** Health | **Unit:** % PLWH virally suppressed
- **Baseline:** 66% (2023). Range: 52-78%. **Source:** CDC HIV surveillance.

### Node 422: Hepatitis C Treatment Completion
- **Scale:** 5 | **Domain:** Health | **Unit:** % HCV+ completing DAA therapy
- **Baseline:** 38% diagnosed (2023). Range: 25-55%. **Source:** CDC, claims.

### Node 423: Cancer Survivorship Follow-Up
- **Scale:** 5 | **Domain:** Health | **Unit:** % cancer survivors with follow-up
- **Baseline:** 68% (2023). Range: 55-80%. **Source:** SEER, surveys.

### Node 424: Heart Failure Medication Adherence
- **Scale:** 5 | **Domain:** Health | **Unit:** PDC for HF medications
- **Baseline:** 0.62 PDC (2023). Range: 0.48-0.76. **Source:** HEDIS, PQA.

### Node 425: COPD Appropriate Medication Use
- **Scale:** 6 | **Domain:** Health | **Unit:** % COPD on guideline meds
- **Baseline:** 58% (2023). Range: 45-72%. **Source:** HEDIS, claims.

---

## 4.3 MATERNAL & CHILD HEALTH PATHWAYS

### Node 426: Interpregnancy Interval (Short <18mo)
- **Scale:** 5 | **Domain:** Maternal | **Unit:** % births with interval <18mo
- **Baseline:** 28% (2023). Range: 20-38%. **Source:** NVSS.

### Node 427: Gestational Weight Gain (Inadequate/Excessive)
- **Scale:** 5 | **Domain:** Maternal | **Unit:** % outside IOM guidelines
- **Baseline:** 52% (2023). Range: 42-65%. **Source:** PRAMS, NVSS.

### Node 428: Prenatal Substance Exposure
- **Scale:** 5 | **Domain:** Maternal, Child | **Unit:** % births with prenatal substance exposure
- **Baseline:** 8.5% (2023). Range: 4-16%. **Source:** NVSS, PRAMS.

### Node 429: Breastfeeding Support Received
- **Scale:** 5 | **Domain:** Child, Maternal | **Unit:** % new mothers receiving lactation support
- **Baseline:** 58% (2023). Range: 42-72%. **Source:** PRAMS, mPINC.

### Node 430: Well-Child Visit Completion (0-15mo)
- **Scale:** 5 | **Domain:** Child | **Unit:** % completing 6+ well-child visits
- **Baseline:** 64% (2023). Range: 52-78%. **Source:** HEDIS, Medicaid.

### Node 431: Developmental Screening Rate
- **Scale:** 6 | **Domain:** Child | **Unit:** % children screened by age 3
- **Baseline:** 31% (2023). Range: 20-48%. **Source:** NSCH, surveys.

### Node 432: Early Intervention Service Receipt
- **Scale:** 6 | **Domain:** Child | **Unit:** % eligible receiving EI services
- **Baseline:** 72% identified (2023). Range: 55-88%. **Source:** IDEA Part C, state.

### Node 433: Lead Screening Rate (Children)
- **Scale:** 6 | **Domain:** Child, Environmental | **Unit:** % children screened for lead
- **Baseline:** 42% by age 2 (2023). Range: 25-68%. **Source:** CDC, state.

### Node 434: Adolescent Well-Visit Rate
- **Scale:** 6 | **Domain:** Child | **Unit:** % teens age 12-21 with annual visit
- **Baseline:** 52% (2023). Range: 42-66%. **Source:** HEDIS, NSCH.

### Node 435: Adolescent Depression Screening
- **Scale:** 6 | **Domain:** Child, Mental Health | **Unit:** % teens screened for depression
- **Baseline:** 58% (2023). Range: 42-72%. **Source:** HEDIS, NSCH.

---

## 4.4 BEHAVIORAL HEALTH TREATMENT PATHWAYS

### Node 436: SUD Medication Treatment Rate (OUD)
- **Scale:** 6 | **Domain:** Behavioral Health | **Unit:** % OUD receiving MAT
- **Baseline:** 22% (2023). Range: 12-38%. **Source:** SAMHSA TEDS, claims.

### Node 437: Mental Health Treatment Retention (90 days)
- **Scale:** 6 | **Domain:** Mental Health | **Unit:** % retained 90+ days
- **Baseline:** 48% (2023). Range: 35-62%. **Source:** TEDS, state systems.

### Node 438: Peer Support Service Utilization
- **Scale:** 6 | **Domain:** Behavioral Health | **Unit:** % BH patients receiving peer support
- **Baseline:** 18% (2023). Range: 8-32%. **Source:** SAMHSA, Medicaid.

### Node 439: Crisis Intervention Service Use
- **Scale:** 6 | **Domain:** Mental Health | **Unit:** Crisis contacts per 1k pop
- **Baseline:** 45/1k (2023). Range: 20-85. **Source:** SAMHSA, state systems.

### Node 440: Assertive Community Treatment (ACT) Enrollment
- **Scale:** 5 | **Domain:** Mental Health | **Unit:** ACT clients per 100k pop
- **Baseline:** 12/100k (2023). Range: 5-28. **Source:** SAMHSA, state.

### Node 441: Integrated Behavioral Health Visits
- **Scale:** 5 | **Domain:** Healthcare, Behavioral | **Unit:** % primary care visits with BH integration
- **Baseline:** 24% (2023). Range: 12-42%. **Source:** HRSA, surveys.

### Node 442: Recovery Housing Utilization
- **Scale:** 5 | **Domain:** Behavioral Health, Housing | **Unit:** Recovery housing residents per 100k
- **Baseline:** 28/100k (2023). Range: 10-65. **Source:** NARR, state.

### Node 443: Substance Use Harm Reduction Service Access
- **Scale:** 5 | **Domain:** Behavioral Health | **Unit:** Syringe exchange participants per 1k PWID
- **Baseline:** 180/1k PWID (2023). Range: 0-450. **Source:** CDC, NASEN.

### Node 444: Mental Health Hospitalization Rate
- **Scale:** 7 | **Domain:** Mental Health | **Unit:** Inpatient psych admits per 1k
- **Baseline:** 4.2/1k (2023). Range: 2.5-7.0. **Source:** HCUP, state.

### Node 445: Involuntary Commitment Rate
- **Scale:** 6 | **Domain:** Mental Health | **Unit:** Involuntary holds per 1k pop
- **Baseline:** 2.8/1k (2023). Range: 1.2-6.5. **Source:** State systems.

---

## 4.5 BIOLOGICAL RISK FACTORS & ALLOSTATIC LOAD

### Node 446: Elevated Inflammatory Markers (CRP)
- **Scale:** 4 | **Domain:** Health | **Unit:** % adults CRP >3 mg/L
- **Baseline:** 38% (2023). Range: 30-48%. **Source:** NHANES.

### Node 447: Metabolic Syndrome Prevalence
- **Scale:** 6 | **Domain:** Health | **Unit:** % adults with metabolic syndrome
- **Baseline:** 34% (2023). Range: 28-42%. **Source:** NHANES.

### Node 448: Prediabetes (Undiagnosed Dysglycemia)
- **Scale:** 6 | **Domain:** Health | **Unit:** % adults with prediabetes
- **Baseline:** 38% (2023). Range: 30-48%. **Source:** CDC, NHANES.

### Node 449: High Total Cholesterol
- **Scale:** 6 | **Domain:** Health | **Unit:** % adults total cholesterol ≥240
- **Baseline:** 11.4% (2023). Range: 8-16%. **Source:** NHANES.

### Node 450: Elevated Blood Lead Levels
- **Scale:** 2 | **Domain:** Environmental, Health | **Unit:** % children BLL ≥5 μg/dL
- **Baseline:** 2.2% (2023). Range: 0.5-8%. **Source:** CDC, state surveillance.

### Node 451: Cadmium Exposure (Biomarker)
- **Scale:** 2 | **Domain:** Environmental, Health | **Unit:** Geometric mean urine cadmium μg/L
- **Baseline:** 0.25 μg/L (2023). Range: 0.15-0.45. **Source:** NHANES.

### Node 452: Cotinine Levels (Secondhand Smoke)
- **Scale:** 6 | **Domain:** Environmental, Health | **Unit:** % nonsmokers detectable cotinine
- **Baseline:** 25% (2023). Range: 18-38%. **Source:** NHANES.

### Node 453: Allostatic Load Index (High)
- **Scale:** 5 | **Domain:** Health | **Unit:** % adults high allostatic load (≥4 indicators)
- **Baseline:** 32% (2023). Range: 24-42%. **Source:** NHANES, research.

### Node 454: Telomere Length (Short)
- **Scale:** 5 | **Domain:** Health | **Unit:** % adults shortest quartile telomeres
- **Baseline:** 25% by definition (2023). Range: 20-32% (varies by stress). **Source:** NHANES, research.

### Node 455: Chronic Stress Biomarkers (Cortisol)
- **Scale:** 5 | **Domain:** Health, Mental Health | **Unit:** % elevated hair cortisol
- **Baseline:** 28% (est 2023). Range: 18-42%. **Source:** Research studies.

---

## 4.6 HEALTH BEHAVIORS ENACTED

### Node 456: Smoking Cessation Attempts
- **Scale:** 5 | **Domain:** Behavioral Health | **Unit:** % smokers attempted quit past year
- **Baseline:** 57% (2023). Range: 48-68%. **Source:** BRFSS, state.

### Node 457: Smoking Cessation Treatment Use
- **Scale:** 5 | **Domain:** Behavioral Health, Healthcare | **Unit:** % quit attempts using treatment
- **Baseline:** 32% (2023). Range: 22-45%. **Source:** BRFSS, surveys.

### Node 458: Physical Activity Engagement (Any)
- **Scale:** 5 | **Domain:** Health | **Unit:** % some leisure-time activity
- **Baseline:** 77% (2023). Range: 68-85%. **Source:** BRFSS, state.

### Node 459: Weight Loss Attempts
- **Scale:** 6 | **Domain:** Health | **Unit:** % overweight/obese trying to lose weight
- **Baseline:** 62% (2023). Range: 52-72%. **Source:** NHANES, BRFSS.

### Node 460: Seatbelt Use
- **Scale:** 4 | **Domain:** Health, Safety | **Unit:** % always wear seatbelt
- **Baseline:** 90% (2023). Range: 82-96%. **Source:** BRFSS, observations.

### Node 461: Bicycle Helmet Use
- **Scale:** 4 | **Domain:** Health, Safety | **Unit:** % cyclists wearing helmets
- **Baseline:** 48% (2023). Range: 25-78%. **Source:** Observations, surveys.

### Node 462: Sun Protection Behaviors
- **Scale:** 2 | **Domain:** Health | **Unit:** % regularly using sun protection
- **Baseline:** 34% (2023). Range: 22-52%. **Source:** HINTS, surveys.

### Node 463: Hand Hygiene Compliance
- **Scale:** 5 | **Domain:** Health, Prevention | **Unit:** % reporting regular handwashing
- **Baseline:** 71% (2023). Range: 60-82%. **Source:** Surveys.

### Node 464: Safe Sexual Practices (Condom Use)
- **Scale:** 2 | **Domain:** Health | **Unit:** % sexually active using condoms
- **Baseline:** 24% (2023). Range: 18-35%. **Source:** NSFG, YRBS.

### Node 465: Medication Disposal (Proper)
- **Scale:** 2 | **Domain:** Health, Environmental | **Unit:** % properly disposing unused meds
- **Baseline:** 38% (2023). Range: 25-55%. **Source:** Surveys.

---

## 4.7 HOUSING & ENVIRONMENTAL EXPOSURES (PATHWAYS)

### Node 466: Radon Testing (Homes Tested)
- **Scale:** 2 | **Domain:** Housing, Environmental | **Unit:** % homes tested for radon
- **Baseline:** 14% (2023). Range: 8-28%. **Source:** EPA, surveys.

### Node 467: Radon Mitigation (Homes Mitigated)
- **Scale:** 2 | **Domain:** Housing, Environmental | **Unit:** % high-radon homes mitigated
- **Baseline:** 22% (2023). Range: 12-38%. **Source:** EPA, state.

### Node 468: Lead Paint Remediation Rate
- **Scale:** 2 | **Domain:** Housing, Environmental | **Unit:** Lead hazard control units per 1k pre-1978
- **Baseline:** 3.2/1k (2023). Range: 1.0-8.0. **Source:** HUD OLHCHH, state.

### Node 469: Water Filter Use (Households)
- **Scale:** 4 | **Domain:** Environmental | **Unit:** % HH using water filters
- **Baseline:** 58% (2023). Range: 42-72%. **Source:** Surveys, market data.

### Node 470: Air Purifier Use
- **Scale:** 4 | **Domain:** Environmental | **Unit:** % HH using air purifiers
- **Baseline:** 32% (2023). Range: 18-52%. **Source:** Market data, surveys.

### Node 471: Mold Remediation (Homes Addressed)
- **Scale:** 4 | **Domain:** Housing, Environmental | **Unit:** % homes with mold professionally remediated
- **Baseline:** 12% of affected (2023). Range: 6-22%. **Source:** Surveys.

### Node 472: Pest Control Services Use
- **Scale:** 4 | **Domain:** Housing, Environmental | **Unit:** % HH using professional pest control
- **Baseline:** 42% (2023). Range: 28-62%. **Source:** Market data, surveys.

### Node 473: Home Energy Efficiency Upgrades
- **Scale:** 2 | **Domain:** Housing, Energy | **Unit:** % homes with weatherization past 5yr
- **Baseline:** 8% (2023). Range: 4-18%. **Source:** EIA RECS, DOE WAP.

### Node 474: Indoor Temperature Maintenance
- **Scale:** 2 | **Domain:** Housing | **Unit:** % homes maintaining 68-78°F year-round
- **Baseline:** 78% (2023). Range: 62-88%. **Source:** EIA RECS.

### Node 475: Safe Water Access (Point-of-Use Treatment)
- **Scale:** 2 | **Domain:** Environmental | **Unit:** % at-risk HH with POE/POU treatment
- **Baseline:** 28% (2023). Range: 15-45%. **Source:** Surveys.

---

## 4.8 OCCUPATIONAL & INJURY EXPOSURES

### Node 476: Workplace Injury Rate
- **Scale:** 2 | **Domain:** Occupational | **Unit:** Injuries per 100 FTE workers
- **Baseline:** 2.7/100 FTE (2023). Range: 1.5-5.0. **Source:** BLS SOII, industry.

### Node 477: Occupational Illness Rate
- **Scale:** 2 | **Domain:** Occupational | **Unit:** Illnesses per 100 FTE workers
- **Baseline:** 0.9/100 FTE (2023). Range: 0.4-2.5. **Source:** BLS SOII.

### Node 478: Workers' Compensation Claim Rate
- **Scale:** 2 | **Domain:** Occupational | **Unit:** Claims per 100 covered workers
- **Baseline:** 1.8/100 (2023). Range: 1.0-3.5. **Source:** NASI, state.

### Node 479: Lost Work Time Injury Rate
- **Scale:** 2 | **Domain:** Occupational | **Unit:** DART rate per 100 FTE
- **Baseline:** 1.1/100 FTE (2023). Range: 0.6-2.5. **Source:** BLS SOII.

### Node 480: Occupational Noise Exposure
- **Scale:** 2 | **Domain:** Occupational | **Unit:** % workers exposed >85 dBA
- **Baseline:** 22% (2023). Range: 12-38%. **Source:** NIOSH, BLS.

### Node 481: Occupational Chemical Exposure
- **Scale:** 2 | **Domain:** Occupational | **Unit:** % workers with hazardous chem exposure
- **Baseline:** 18% (2023). Range: 8-32%. **Source:** NIOSH, OSHA.

### Node 482: Ergonomic Hazard Exposure
- **Scale:** 2 | **Domain:** Occupational | **Unit:** % workers with ergonomic risks
- **Baseline:** 35% (2023). Range: 22-52%. **Source:** BLS, NIOSH.

### Node 483: Heat Stress Exposure (Occupational)
- **Scale:** 2 | **Domain:** Occupational, Climate | **Unit:** % outdoor workers heat-exposed
- **Baseline:** 48% outdoor workers (2023). Range: 28-78%. **Source:** NIOSH, OSHA.

### Node 484: Fall Risk Exposure (Work)
- **Scale:** 4 | **Domain:** Occupational | **Unit:** % workers at elevation/fall risk
- **Baseline:** 24% (2023). Range: 12-42%. **Source:** OSHA, BLS.

### Node 485: Motor Vehicle Crash Rate (Occupational)
- **Scale:** 4 | **Domain:** Occupational, Transportation | **Unit:** Work-related crashes per 100 FTE
- **Baseline:** 0.8/100 FTE (2023). Range: 0.3-2.0. **Source:** BLS CFOI, NHTSA.

---

## 4.9 SOCIAL SUPPORT & CONNECTIVITY PROCESSES

### Node 486: Social Network Size
- **Scale:** 5 | **Domain:** Social | **Unit:** Mean number close contacts
- **Baseline:** 4.2 contacts (2023). Range: 2.5-6.5. **Source:** GSS, surveys.

### Node 487: Frequency of Social Contact
- **Scale:** 4 | **Domain:** Social | **Unit:** % daily+ in-person contact
- **Baseline:** 38% (2023). Range: 25-55%. **Source:** Surveys.

### Node 488: Social Participation (Events/Month)
- **Scale:** 4 | **Domain:** Social | **Unit:** Mean social events per month
- **Baseline:** 3.8 events (2023). Range: 2.0-6.5. **Source:** Time use surveys.

### Node 489: Family Support Received
- **Scale:** 4 | **Domain:** Social | **Unit:** % receiving family support when needed
- **Baseline:** 72% (2023). Range: 58-84%. **Source:** BRFSS, surveys.

### Node 490: Community Cohesion (Perceived)
- **Scale:** 4 | **Domain:** Social | **Unit:** % high community cohesion
- **Baseline:** 48% (2023). Range: 32-68%. **Source:** Surveys.

### Node 491: Religious/Spiritual Engagement
- **Scale:** 4 | **Domain:** Social | **Unit:** % high engagement (weekly+)
- **Baseline:** 31% (2023). Range: 18-52%. **Source:** Pew, GSS.

### Node 492: Neighborly Exchange Frequency
- **Scale:** 2 | **Domain:** Social | **Unit:** % exchanging favors with neighbors
- **Baseline:** 42% (2023). Range: 28-62%. **Source:** Surveys.

### Node 493: Online Social Connectivity
- **Scale:** 2 | **Domain:** Social, Digital | **Unit:** Mean hours social media/week
- **Baseline:** 8.2 hrs/week (2023). Range: 4-15. **Source:** Time use, Pew.

### Node 494: Intergenerational Contact
- **Scale:** 2 | **Domain:** Social | **Unit:** % regular contact across generations
- **Baseline:** 54% (2023). Range: 38-72%. **Source:** Surveys.

### Node 495: Peer Support Group Participation
- **Scale:** 2 | **Domain:** Social, Health | **Unit:** % in support groups
- **Baseline:** 12% adults (2023). Range: 6-22%. **Source:** Surveys.

---

## 4.10 ENVIRONMENTAL PATHWAY PROCESSES

### Node 496: Air Quality Alert Days
- **Scale:** 2 | **Domain:** Environmental | **Unit:** Days AQI >100 annually
- **Baseline:** 12 days (2023). Range: 0-60. **Source:** EPA AirNow, county.

### Node 497: Heat Advisory Days
- **Scale:** 2 | **Domain:** Climate, Environmental | **Unit:** Heat advisory days annually
- **Baseline:** 8 days (2023). Range: 0-45. **Source:** NOAA NWS.

### Node 498: Cooling Center Utilization
- **Scale:** 2 | **Domain:** Climate, Social | **Unit:** Visits per 1k pop during heat
- **Baseline:** 4.2/1k (2023). Range: 0.5-18. **Source:** Local agencies.

### Node 499: Green Space Utilization
- **Scale:** 2 | **Domain:** Environmental, Health | **Unit:** % using parks weekly+
- **Baseline:** 38% (2023). Range: 22-62%. **Source:** Surveys, NRPA.

### Node 500: Active Transportation Use (Walking/Biking)
- **Scale:** 2 | **Domain:** Transportation, Health | **Unit:** Mean walk/bike trips per week
- **Baseline:** 2.8 trips/week (2023). Range: 1.0-6.5. **Source:** NHTS, time use.

### Node 501: Public Transit Utilization
- **Scale:** 2 | **Domain:** Transportation | **Unit:** Transit trips per capita annually
- **Baseline:** 42 trips (2023). Range: 5-220. **Source:** APTA, FTA NTD.

### Node 502: Tree Canopy Cover (Change)
- **Scale:** 2 | **Domain:** Environmental | **Unit:** % change canopy cover 5yr
- **Baseline:** -1.2% (2023). Range: -5% to +3%. **Source:** NLCD, local.

### Node 503: Urban Heat Island Mitigation
- **Scale:** 2 | **Domain:** Climate, Environmental | **Unit:** Cool surface area %
- **Baseline:** 28% (2023). Range: 12-52%. **Source:** Remote sensing, local.

### Node 504: Stormwater Management (Green Infrastructure)
- **Scale:** 2 | **Domain:** Environmental | **Unit:** % impervious area with GI
- **Baseline:** 8% (2023). Range: 2-22%. **Source:** EPA, local utilities.

### Node 505: Brownfield Remediation Rate
- **Scale:** 2 | **Domain:** Environmental | **Unit:** Sites remediated per 100k pop
- **Baseline:** 2.4/100k (2023). Range: 0.5-8. **Source:** EPA, state.

---

## 4.11 FOOD & NUTRITION PATHWAYS

### Node 506: Food Pantry Utilization
- **Scale:** 4 | **Domain:** Food, Social | **Unit:** Visits per 1k pop
- **Baseline:** 185/1k (2023). Range: 80-380. **Source:** Feeding America.

### Node 507: SNAP Benefit Adequacy
- **Scale:** 2 | **Domain:** Food, Economic | **Unit:** % month covered by benefits
- **Baseline:** 68% of month (2023). Range: 55-82%. **Source:** USDA FNS.

### Node 508: School Meal Participation
- **Scale:** 3 | **Domain:** Food, Education | **Unit:** % eligible participating
- **Baseline:** 83% (2023). Range: 68-92%. **Source:** USDA FNS.

### Node 509: Farmers Market Utilization (SNAP)
- **Scale:** 2 | **Domain:** Food | **Unit:** % SNAP at farmers markets
- **Baseline:** 0.8% of SNAP $ (2023). Range: 0.2-3%. **Source:** USDA FNS.

### Node 510: Community Garden Participation
- **Scale:** 2 | **Domain:** Food, Social | **Unit:** Gardeners per 1k pop
- **Baseline:** 8.5/1k (2023). Range: 2-28. **Source:** ACGA, local.

### Node 511: Grocery Store Access (Utilization)
- **Scale:** 2 | **Domain:** Food | **Unit:** % primary shopping at full-service grocery
- **Baseline:** 72% (2023). Range: 45-88%. **Source:** Surveys.

### Node 512: Fresh Produce Consumption Frequency
- **Scale:** 4 | **Domain:** Food, Health | **Unit:** Mean servings fruit/veg daily
- **Baseline:** 2.1 servings (2023). Range: 1.2-3.5. **Source:** BRFSS, NHANES.

### Node 513: Home Meal Preparation Frequency
- **Scale:** 4 | **Domain:** Food | **Unit:** Meals cooked at home per week
- **Baseline:** 8.2 meals (2023). Range: 4-13. **Source:** Time use surveys.

### Node 514: Emergency Food Network Capacity Utilization
- **Scale:** 4 | **Domain:** Food, Social | **Unit:** % network capacity used
- **Baseline:** 78% (2023). Range: 55-98%. **Source:** Feeding America.

### Node 515: Nutrition Education Participation
- **Scale:** 5 | **Domain:** Food, Education | **Unit:** % food insecure receiving nutrition ed
- **Baseline:** 18% (2023). Range: 8-35%. **Source:** SNAP-Ed, EFNEP.

---

## 4.12 JUSTICE SYSTEM PATHWAY PROCESSES

### Node 516: Jail Booking Rate
- **Scale:** 4 | **Domain:** Criminal Justice | **Unit:** Bookings per 1k pop
- **Baseline:** 35/1k (2023). Range: 18-65. **Source:** BJS, jails.

### Node 517: Pretrial Detention Rate
- **Scale:** 4 | **Domain:** Criminal Justice | **Unit:** % defendants detained pretrial
- **Baseline:** 38% (2023). Range: 22-58%. **Source:** BJS, courts.

### Node 518: Diversion Program Utilization
- **Scale:** 4 | **Domain:** Criminal Justice | **Unit:** Diversions per 1k arrests
- **Baseline:** 82/1k arrests (2023). Range: 20-180. **Source:** State systems.

### Node 519: Reentry Service Receipt
- **Scale:** 6 | **Domain:** Criminal Justice | **Unit:** % released receiving reentry services
- **Baseline:** 28% (2023). Range: 12-52%. **Source:** NRRC, state.

### Node 520: Recidivism Rate (3-Year)
- **Scale:** 6 | **Domain:** Criminal Justice | **Unit:** % rearrested within 3yr
- **Baseline:** 68% (2023). Range: 55-82%. **Source:** BJS, state.

### Node 521: Probation Revocation Rate
- **Scale:** 6 | **Domain:** Criminal Justice | **Unit:** % probation revoked
- **Baseline:** 18% (2023). Range: 10-32%. **Source:** BJS, state.

### Node 522: Drug Court Participation
- **Scale:** 6 | **Domain:** Criminal Justice, Behavioral | **Unit:** Participants per 1k SUD arrests
- **Baseline:** 45/1k (2023). Range: 0-120. **Source:** NADCP, state.

### Node 523: Mental Health Court Utilization
- **Scale:** 6 | **Domain:** Criminal Justice, Mental Health | **Unit:** Participants per 100k pop
- **Baseline:** 12/100k (2023). Range: 0-35. **Source:** CMHS, state.

### Node 524: Restorative Justice Program Participation
- **Scale:** 4 | **Domain:** Criminal Justice | **Unit:** Cases per 1k offenses
- **Baseline:** 8/1k (2023). Range: 0-45. **Source:** State systems.

### Node 525: Expungement/Sealing Rate
- **Scale:** 4 | **Domain:** Criminal Justice | **Unit:** Records sealed per 1k eligible
- **Baseline:** 22/1k eligible (2023). Range: 5-85. **Source:** Courts, state.

---

## 4.13 EDUCATION & DEVELOPMENT PATHWAYS

### Node 526: Early Literacy Support Receipt
- **Scale:** 6 | **Domain:** Education, Child | **Unit:** % low-income children in literacy programs
- **Baseline:** 32% (2023). Range: 18-52%. **Source:** ACF Head Start, state.

### Node 527: After-School Program Participation
- **Scale:** 3 | **Domain:** Education, Child | **Unit:** % school-age in after-school programs
- **Baseline:** 18% (2023). Range: 10-32%. **Source:** Afterschool Alliance.

### Node 528: Tutoring/Academic Support Use
- **Scale:** 4 | **Domain:** Education | **Unit:** % students receiving tutoring
- **Baseline:** 24% (2023). Range: 12-42%. **Source:** NCES, surveys.

### Node 529: College Application Rate
- **Scale:** 4 | **Domain:** Education | **Unit:** % HS seniors applying to college
- **Baseline:** 68% (2023). Range: 45-88%. **Source:** NCES, state.

### Node 530: FAFSA Completion Rate
- **Scale:** 4 | **Domain:** Education, Economic | **Unit:** % eligible completing FAFSA
- **Baseline:** 52% (2023). Range: 38-72%. **Source:** ED FSA, state.

### Node 531: College Enrollment (Immediate)
- **Scale:** 4 | **Domain:** Education | **Unit:** % HS grads enrolling fall after graduation
- **Baseline:** 62% (2023). Range: 45-78%. **Source:** NCES, state.

### Node 532: College Persistence (2nd Year)
- **Scale:** 4 | **Domain:** Education | **Unit:** % first-year students returning
- **Baseline:** 74% (2023). Range: 58-88%. **Source:** NCES IPEDS.

### Node 533: Developmental Education Placement
- **Scale:** 4 | **Domain:** Education | **Unit:** % college students in remedial courses
- **Baseline:** 42% (2023). Range: 28-62%. **Source:** NCES, CCRC.

### Node 534: Student Support Service Utilization
- **Scale:** 4 | **Domain:** Education | **Unit:** % college students using support services
- **Baseline:** 38% (2023). Range: 22-58%. **Source:** NCES, surveys.

### Node 535: Apprenticeship Participation
- **Scale:** 4 | **Domain:** Education, Employment | **Unit:** Apprentices per 1k labor force
- **Baseline:** 2.8/1k (2023). Range: 1.0-6.5. **Source:** DOL, state.

---

## 4.14 ECONOMIC PATHWAY PROCESSES

### Node 536: Job Search Activity (Unemployed)
- **Scale:** 6 | **Domain:** Employment, Economic | **Unit:** Mean job applications per week
- **Baseline:** 5.2 apps (2023). Range: 3-9. **Source:** BLS, surveys.

### Node 537: Job Training Program Participation
- **Scale:** 6 | **Domain:** Employment, Education | **Unit:** % unemployed in training
- **Baseline:** 14% (2023). Range: 8-28%. **Source:** DOL, state.

### Node 538: Workforce Development Service Use
- **Scale:** 3 | **Domain:** Employment | **Unit:** % labor force using American Job Centers
- **Baseline:** 3.2% (2023). Range: 1.5-6%. **Source:** DOL WIOA, state.

### Node 539: Unemployment Insurance Receipt
- **Scale:** 6 | **Domain:** Employment, Economic | **Unit:** % unemployed receiving UI
- **Baseline:** 28% (2023). Range: 18-45%. **Source:** DOL, state.

### Node 540: Public Benefit Application Rate
- **Scale:** 4 | **Domain:** Economic, Social | **Unit:** Applications per 1k eligible
- **Baseline:** 420/1k eligible (2023). Range: 280-650. **Source:** HHS, state.

### Node 541: TANF Participation Rate
- **Scale:** 4 | **Domain:** Economic, Social | **Unit:** % eligible families participating
- **Baseline:** 21% (2023). Range: 8-48%. **Source:** ACF, state.

### Node 542: Housing Voucher Utilization Rate
- **Scale:** 6 | **Domain:** Housing, Economic | **Unit:** % vouchers issued and leased
- **Baseline:** 96% (2023). Range: 88-99%. **Source:** HUD PIC.

### Node 543: Emergency Rental Assistance Receipt
- **Scale:** 4 | **Domain:** Housing, Economic | **Unit:** Households assisted per 1k renters
- **Baseline:** 28/1k (2023). Range: 10-65. **Source:** Treasury ERA, local.

### Node 544: Eviction Filing Rate
- **Scale:** 4 | **Domain:** Housing, Economic | **Unit:** Eviction filings per 100 rental HH
- **Baseline:** 3.6/100 (2023). Range: 1.5-8.5. **Source:** Eviction Lab, courts.

### Node 545: Utility Assistance (LIHEAP) Receipt
- **Scale:** 4 | **Domain:** Housing, Economic | **Unit:** % eligible receiving LIHEAP
- **Baseline:** 16% (2023). Range: 8-32%. **Source:** HHS ACF, state.

---

## 4.15 CLIMATE ADAPTATION & RESILIENCE PATHWAYS

### Node 546: Extreme Weather Preparedness
- **Scale:** 2 | **Domain:** Climate, Safety | **Unit:** % HH with emergency supplies
- **Baseline:** 42% (2023). Range: 28-68%. **Source:** FEMA, surveys.

### Node 547: Evacuation Compliance (Hurricanes)
- **Scale:** 5 | **Domain:** Climate, Safety | **Unit:** % evacuating when ordered
- **Baseline:** 68% (2023). Range: 45-88%. **Source:** FEMA, NHC.

### Node 548: Flood Insurance Coverage
- **Scale:** 4 | **Domain:** Climate, Economic | **Unit:** % flood-prone homes insured
- **Baseline:** 32% SFHA (2023). Range: 12-62%. **Source:** FEMA NFIP.

### Node 549: Heat Illness Incidence
- **Scale:** 6 | **Domain:** Climate, Health | **Unit:** Heat illness ED visits per 100k
- **Baseline:** 28/100k (2023). Range: 8-95. **Source:** CDC ESSENCE, state.

### Node 550: Climate Migration (Internal)
- **Scale:** 4 | **Domain:** Climate, Housing | **Unit:** % moved due to climate/disaster 5yr
- **Baseline:** 2.8% (2023). Range: 0.5-12%. **Source:** Census, surveys.

**END SCALE 4: Nodes 401-550 (150 nodes total). Intermediate Pathways complete.**

**PROGRESS: 550/850 (65%)**

---
---

# SCALE 5: CRISIS ENDPOINTS (~300 NODES)

*Scale 5 captures acute crisis events, adverse health outcomes, mortality, system failures, and sentinel health events that represent the downstream consequences of conditions and pathways in Scales 1-4.*

---

## 5.1 MORTALITY ENDPOINTS

### Node 551: All-Cause Mortality Rate
- **Scale:** 7 | **Domain:** Health | **Unit:** Deaths per 100k pop
- **Baseline:** 880/100k (2023). Range: 650-1,150. **Source:** CDC WONDER, county.

### Node 552: Premature Mortality (YPLL)
- **Scale:** 4 | **Domain:** Health | **Unit:** Years of potential life lost per 100k <75
- **Baseline:** 7,400/100k (2023). Range: 4,500-12,000. **Source:** CDC WONDER, county.

### Node 553: Infant Mortality Rate
- **Scale:** 7 | **Domain:** Maternal, Child | **Unit:** Deaths per 1k live births
- **Baseline:** 5.6/1k (2023). Range: 3.5-10.0. **Source:** NVSS, county.

### Node 554: Neonatal Mortality
- **Scale:** 4 | **Domain:** Maternal, Child | **Unit:** Deaths <28 days per 1k births
- **Baseline:** 3.8/1k (2023). Range: 2.2-7.0. **Source:** NVSS, state.

### Node 555: Postneonatal Mortality
- **Scale:** 4 | **Domain:** Child | **Unit:** Deaths 28d-1yr per 1k births
- **Baseline:** 1.8/1k (2023). Range: 0.8-3.5. **Source:** NVSS, state.

### Node 556: Child Mortality (1-4 years)
- **Scale:** 4 | **Domain:** Child | **Unit:** Deaths per 100k children 1-4
- **Baseline:** 24/100k (2023). Range: 15-40. **Source:** CDC WONDER.

### Node 557: Maternal Mortality Ratio
- **Scale:** 4 | **Domain:** Maternal | **Unit:** Deaths per 100k live births
- **Baseline:** 32.9/100k (2023, US high). Range: 18-55. **Source:** NVSS, state.

### Node 558: Pregnancy-Related Mortality
- **Scale:** 4 | **Domain:** Maternal | **Unit:** Deaths per 100k live births
- **Baseline:** 22.3/100k (2023). Range: 12-42. **Source:** PMSS, state.

### Node 559: Cardiovascular Disease Mortality
- **Scale:** 4 | **Domain:** Health | **Unit:** Deaths per 100k
- **Baseline:** 240/100k (2023). Range: 180-350. **Source:** CDC WONDER, county.

### Node 560: Cancer Mortality
- **Scale:** 2 | **Domain:** Health | **Unit:** Deaths per 100k
- **Baseline:** 146/100k (2023). Range: 110-190. **Source:** CDC WONDER, county.

### Node 561: Respiratory Disease Mortality
- **Scale:** 2 | **Domain:** Health | **Unit:** Deaths per 100k
- **Baseline:** 52/100k (2023). Range: 35-80. **Source:** CDC WONDER, county.

### Node 561a: Asthma Incidence Rate [NEW - Added to fill mechanism gap]
- **Scale:** Crisis | **Domain:** Health, Respiratory | **Unit:** New asthma diagnoses per 1,000 persons per year
- **Description:** Annual incidence of new asthma diagnoses (not prevalent cases) per 1,000 population. Age-stratified: children (0-17) and adults (18+). Captures new onset asthma burden, distinct from prevalence (existing cases). Critical for evaluating environmental exposure effects and prevention interventions.
- **Baseline:**
  - Children 0-17: 8.5 per 1,000 per year
  - Adults 18+: 3.2 per 1,000 per year
  - Disparities: Higher among Black children (11.2/1,000), low-income families, urban areas
- **Data Source:** NHIS, NHANES, state health department asthma surveillance, health system EHR data, insurance claims (first asthma diagnosis code). County and state levels.
- **Mechanism node_id child:** `child_asthma_incidence`
- **Mechanism node_id adult:** `adult_asthma_incidence`
- **Consolidation Note:** Previously missing from inventory but referenced in multiple mechanisms. Now explicitly defined.

### Node 561b: Asthma Exacerbation Rate [NEW - Added to fill mechanism gap]
- **Scale:** Crisis | **Domain:** Health, Respiratory, Healthcare Utilization | **Unit:** ED visits + hospitalizations for asthma per 1,000 persons with asthma per year
- **Description:** Annual rate of asthma exacerbations requiring emergency department visit or hospitalization among persons with diagnosed asthma. Denominator = persons with asthma (not total population). Indicates poor asthma control and acute healthcare system burden. Age-stratified data available. Preventable with proper medication adherence and environmental control.
- **Baseline:**
  - Children with asthma: 145 per 1,000 per year (14.5% annual exacerbation rate)
  - Adults with asthma: 68 per 1,000 per year (6.8% annual exacerbation rate)
  - Disparities: Higher among Black children (220/1,000), Medicaid enrollees, uninsured, high air pollution areas
- **Data Source:** HCUP State Inpatient Databases, State Emergency Department Databases, Medicaid/Medicare claims, CDC National Asthma Surveillance. State and county levels.
- **Mechanism node_id child:** `child_asthma_exacerbations`
- **Mechanism node_id adult:** `asthma_exacerbation_rate`
- **Consolidation Note:** Previously missing from inventory but referenced in multiple mechanisms. Now explicitly defined.

### Node 562: Stroke Mortality
- **Scale:** 4 | **Domain:** Health | **Unit:** Deaths per 100k
- **Baseline:** 38/100k (2023). Range: 25-65. **Source:** CDC WONDER, county.

### Node 563: Diabetes Mortality
- **Scale:** 6 | **Domain:** Health | **Unit:** Deaths per 100k
- **Baseline:** 25/100k (2023). Range: 15-45. **Source:** CDC WONDER, county.

### Node 564: Alzheimer's/Dementia Mortality
- **Scale:** 4 | **Domain:** Health | **Unit:** Deaths per 100k
- **Baseline:** 32/100k (2023). Range: 20-52. **Source:** CDC WONDER, county.

### Node 565: Kidney Disease Mortality
- **Scale:** 4 | **Domain:** Health | **Unit:** Deaths per 100k
- **Baseline:** 13/100k (2023). Range: 8-22. **Source:** CDC WONDER, county.

### Node 566: Liver Disease Mortality
- **Scale:** 4 | **Domain:** Health | **Unit:** Deaths per 100k
- **Baseline:** 14.5/100k (2023). Range: 8-28. **Source:** CDC WONDER, county.

### Node 567: Suicide Rate
- **Scale:** 7 | **Domain:** Mental Health | **Unit:** Deaths per 100k
- **Baseline:** 14.2/100k (2023). Range: 8-28. **Source:** CDC WONDER, county.

### Node 568: Drug Overdose Mortality
- **Scale:** 7 | **Domain:** Behavioral Health | **Unit:** Deaths per 100k
- **Baseline:** 32.5/100k (2023). Range: 8-85. **Source:** CDC WONDER, county.

### Node 569: Opioid Overdose Mortality
- **Scale:** 7 | **Domain:** Behavioral Health | **Unit:** Deaths per 100k
- **Baseline:** 22.0/100k (2023). Range: 4-65. **Source:** CDC WONDER, county.

### Node 570: Alcohol-Induced Mortality
- **Scale:** 4 | **Domain:** Behavioral Health | **Unit:** Deaths per 100k
- **Baseline:** 12.5/100k (2023). Range: 6-28. **Source:** CDC WONDER, county.

### Node 571: Homicide Rate
- **Scale:** 4 | **Domain:** Criminal Justice, Violence | **Unit:** Deaths per 100k
- **Baseline:** 6.5/100k (2023). Range: 1.5-35. **Source:** CDC WONDER, FBI UCR, county.

### Node 572: Firearm Mortality
- **Scale:** 4 | **Domain:** Violence | **Unit:** Deaths per 100k
- **Baseline:** 14.8/100k (2023). Range: 5-32. **Source:** CDC WONDER, county.

### Node 573: Motor Vehicle Crash Mortality
- **Scale:** 4 | **Domain:** Transportation, Injury | **Unit:** Deaths per 100k
- **Baseline:** 12.9/100k (2023). Range: 6-28. **Source:** CDC WONDER, NHTSA, county.

### Node 574: Pedestrian/Cyclist Fatality Rate
- **Scale:** 7 | **Domain:** Transportation, Injury | **Unit:** Deaths per 100k
- **Baseline:** 2.8/100k (2023). Range: 0.8-7.5. **Source:** NHTSA FARS, county.

### Node 575: Occupational Fatality Rate
- **Scale:** 7 | **Domain:** Occupational | **Unit:** Deaths per 100k workers
- **Baseline:** 3.5/100k FTE (2023). Range: 1.5-10. **Source:** BLS CFOI.

### Node 576: Heat-Related Mortality
- **Scale:** 4 | **Domain:** Climate, Environmental | **Unit:** Deaths per 1M pop
- **Baseline:** 8.5/1M (2023). Range: 1-45. **Source:** CDC WONDER, county.

### Node 577: Cold-Related Mortality
- **Scale:** 4 | **Domain:** Climate, Environmental | **Unit:** Deaths per 1M pop
- **Baseline:** 1.8/1M (2023). Range: 0.2-8. **Source:** CDC WONDER.

### Node 578: Disaster-Related Mortality
- **Scale:** 4 | **Domain:** Climate, Environmental | **Unit:** Deaths per year
- **Baseline:** 0.15/100k annually (2023). Range: 0-20+ (varies). **Source:** FEMA, NOAA.

### Node 579: Sepsis Mortality
- **Scale:** 4 | **Domain:** Health | **Unit:** Deaths per 100k
- **Baseline:** 11.5/100k (2023). Range: 8-18. **Source:** CDC WONDER, claims.

### Node 580: Pneumonia/Influenza Mortality
- **Scale:** 4 | **Domain:** Health | **Unit:** Deaths per 100k
- **Baseline:** 13.2/100k (2023). Range: 8-24. **Source:** CDC WONDER, county.

---

## 5.2 BIRTH OUTCOMES & CRISES

### Node 581: Preterm Birth Rate
- **Scale:** 4 | **Domain:** Maternal, Child | **Unit:** % births <37 weeks
- **Baseline:** 10.4% (2023). Range: 7.5-15%. **Source:** NVSS, county.

### Node 582: Very Preterm Birth (<32 weeks)
- **Scale:** 7 | **Domain:** Maternal, Child | **Unit:** % births <32 weeks
- **Baseline:** 2.8% (2023). Range: 1.8-4.5%. **Source:** NVSS, county.

### Node 583: Low Birthweight Rate
- **Scale:** 4 | **Domain:** Maternal, Child | **Unit:** % births <2,500g
- **Baseline:** 8.3% (2023). Range: 5.5-12%. **Source:** NVSS, county.

### Node 584: Very Low Birthweight (<1,500g)
- **Scale:** 7 | **Domain:** Maternal, Child | **Unit:** % births <1,500g
- **Baseline:** 1.4% (2023). Range: 0.9-2.2%. **Source:** NVSS, county.

### Node 585: Small for Gestational Age (SGA)
- **Scale:** 4 | **Domain:** Maternal, Child | **Unit:** % births <10th percentile
- **Baseline:** 11.2% (2023). Range: 8-16%. **Source:** NVSS, research.

### Node 586: Neonatal Abstinence Syndrome (NAS)
- **Scale:** 4 | **Domain:** Maternal, Child | **Unit:** NAS cases per 1k births
- **Baseline:** 7.3/1k (2023). Range: 2-25. **Source:** NVSS, hospital data.

### Node 587: Stillbirth Rate
- **Scale:** 7 | **Domain:** Maternal | **Unit:** Fetal deaths ≥20wk per 1k births
- **Baseline:** 5.9/1k (2023). Range: 4.2-9.0. **Source:** NVSS, state.

### Node 588: Birth Trauma/Injury Rate
- **Scale:** 4 | **Domain:** Maternal, Child | **Unit:** Birth injuries per 1k births
- **Baseline:** 1.2/1k (2023). Range: 0.6-2.5. **Source:** Hospital discharge data.

### Node 589: Cesarean Delivery Rate
- **Scale:** 4 | **Domain:** Maternal | **Unit:** % births by C-section
- **Baseline:** 32.1% (2023). Range: 22-42%. **Source:** NVSS, state.

### Node 590: Severe Maternal Morbidity Rate
- **Scale:** 7 | **Domain:** Maternal | **Unit:** SMM per 10k deliveries
- **Baseline:** 144/10k (2023). Range: 95-220. **Source:** NVSS, HCUP, state.

### Node 591: Maternal ICU Admission Rate
- **Scale:** 7 | **Domain:** Maternal | **Unit:** ICU admits per 1k deliveries
- **Baseline:** 2.8/1k (2023). Range: 1.5-5.5. **Source:** Hospital data.

### Node 592: Maternal Hemorrhage Rate
- **Scale:** 6 | **Domain:** Maternal | **Unit:** Hemorrhage per 1k deliveries
- **Baseline:** 28/1k (2023). Range: 18-45. **Source:** Hospital data, HCUP.

### Node 593: Preeclampsia/Eclampsia Rate
- **Scale:** 6 | **Domain:** Maternal | **Unit:** Cases per 1k deliveries
- **Baseline:** 42/1k (2023). Range: 28-68. **Source:** Hospital data, NVSS.

### Node 594: Gestational Diabetes Rate
- **Scale:** 6 | **Domain:** Maternal | **Unit:** % pregnancies with GDM
- **Baseline:** 8.2% (2023). Range: 5-13%. **Source:** Hospital data, PRAMS.

### Node 595: Neonatal ICU Admission Rate
- **Scale:** 7 | **Domain:** Child | **Unit:** NICU admits per 1k births
- **Baseline:** 78/1k (2023). Range: 55-115. **Source:** Hospital data.

---

## 5.3 CHRONIC DISEASE CRISES & COMPLICATIONS

### Node 596: Acute Myocardial Infarction Rate
- **Scale:** 4 | **Domain:** Health | **Unit:** AMI per 100k adults
- **Baseline:** 235/100k (2023). Range: 160-380. **Source:** Hospital data, CMS.

### Node 597: Stroke Incidence
- **Scale:** 6 | **Domain:** Health | **Unit:** Strokes per 100k adults
- **Baseline:** 285/100k (2023). Range: 200-450. **Source:** Hospital data, CDC.

### Node 598: Heart Failure Hospitalization Rate
- **Scale:** 7 | **Domain:** Health | **Unit:** Admits per 1k Medicare
- **Baseline:** 12.5/1k (2023). Range: 8-22. **Source:** CMS, county.

### Node 599: COPD Hospitalization Rate
- **Scale:** 7 | **Domain:** Health | **Unit:** Admits per 1k adults
- **Baseline:** 4.8/1k (2023). Range: 2.5-9.5. **Source:** HCUP, state.

### Node 600: Asthma Hospitalization Rate
- **Scale:** 7 | **Domain:** Health | **Unit:** Admits per 100k
- **Baseline:** 42/100k (2023). Range: 25-85. **Source:** HCUP, state.

### Node 601: Diabetes Lower Extremity Amputation Rate
- **Scale:** 6 | **Domain:** Health | **Unit:** Amputations per 1k diabetics
- **Baseline:** 3.8/1k diabetics (2023). Range: 2.0-7.5. **Source:** CMS, state.

### Node 602: Diabetic Ketoacidosis (DKA) Admission Rate
- **Scale:** 4 | **Domain:** Health | **Unit:** DKA admits per 1k diabetics
- **Baseline:** 6.2/1k (2023). Range: 3.5-12. **Source:** Hospital data.

### Node 603: Hypoglycemic Crisis Rate
- **Scale:** 4 | **Domain:** Health | **Unit:** Severe hypo admits per 1k diabetics
- **Baseline:** 5.5/1k (2023). Range: 3-10. **Source:** Hospital data, CMS.

### Node 604: End-Stage Renal Disease Incidence
- **Scale:** 6 | **Domain:** Health | **Unit:** New ESRD cases per 1M pop
- **Baseline:** 365/1M (2023). Range: 220-650. **Source:** USRDS, state.

### Node 605: Dialysis Initiation Rate
- **Scale:** 4 | **Domain:** Health | **Unit:** New dialysis per 1M pop
- **Baseline:** 340/1M (2023). Range: 200-620. **Source:** USRDS, state.

### Node 606: Liver Failure/Cirrhosis Hospitalization
- **Scale:** 4 | **Domain:** Health | **Unit:** Admits per 100k
- **Baseline:** 38/100k (2023). Range: 18-75. **Source:** HCUP.

### Node 607: Cancer Incidence (All Sites)
- **Scale:** 6 | **Domain:** Health | **Unit:** New cases per 100k
- **Baseline:** 442/100k (2023). Range: 360-550. **Source:** SEER, state registries.

### Node 608: Lung Cancer Incidence
- **Scale:** 6 | **Domain:** Health | **Unit:** Cases per 100k
- **Baseline:** 54/100k (2023). Range: 35-85. **Source:** SEER, state.

### Node 609: Colorectal Cancer Incidence
- **Scale:** 6 | **Domain:** Health | **Unit:** Cases per 100k
- **Baseline:** 38/100k (2023). Range: 28-52. **Source:** SEER, state.

### Node 610: Breast Cancer Incidence
- **Scale:** 6 | **Domain:** Health | **Unit:** Cases per 100k women
- **Baseline:** 128/100k (2023). Range: 105-155. **Source:** SEER, state.

### Node 611: Late-Stage Cancer Diagnosis Rate
- **Scale:** 6 | **Domain:** Health | **Unit:** % diagnosed stage III/IV
- **Baseline:** 38% (2023). Range: 28-52%. **Source:** SEER.

### Node 612: Sepsis Hospitalization Rate
- **Scale:** 7 | **Domain:** Health | **Unit:** Admits per 1k adults
- **Baseline:** 6.8/1k (2023). Range: 4.5-11. **Source:** HCUP, claims.

### Node 613: Venous Thromboembolism (VTE) Rate
- **Scale:** 5 | **Domain:** Health | **Unit:** VTE per 100k
- **Baseline:** 115/100k (2023). Range: 80-165. **Source:** Hospital data.

### Node 614: Hip Fracture Rate (Age 65+)
- **Scale:** 5 | **Domain:** Health, Injury | **Unit:** Fractures per 1k elderly
- **Baseline:** 4.2/1k (2023). Range: 2.8-6.5. **Source:** Hospital data, CMS.

### Node 615: Pressure Ulcer Incidence (Hospital-Acquired)
- **Scale:** 6 | **Domain:** Health | **Unit:** % patients with HAC pressure ulcer
- **Baseline:** 2.8% (2023). Range: 1.5-5.5%. **Source:** CMS HAC, hospitals.

---

## 5.4 MENTAL HEALTH & SUBSTANCE USE CRISES

### Node 616: Psychiatric Hospitalization Rate
- **Scale:** 7 | **Domain:** Mental Health | **Unit:** Admits per 1k pop
- **Baseline:** 4.5/1k (2023). Range: 2.5-8.5. **Source:** HCUP, state.

### Node 617: Suicide Attempt Rate (ED/Hospital)
- **Scale:** 4 | **Domain:** Mental Health | **Unit:** Attempts per 100k
- **Baseline:** 275/100k (2023). Range: 180-450. **Source:** HCUP, CDC WISQARS.

### Node 618: Self-Harm Injury Rate
- **Scale:** 5 | **Domain:** Mental Health | **Unit:** ED visits per 100k
- **Baseline:** 185/100k (2023). Range: 120-320. **Source:** HCUP NEDS.

### Node 619: Opioid Overdose (Nonfatal) Rate
- **Scale:** 5 | **Domain:** Behavioral Health | **Unit:** ED visits per 100k
- **Baseline:** 85/100k (2023). Range: 25-220. **Source:** CDC DOSE, state.

### Node 620: Stimulant Overdose (Nonfatal) Rate
- **Scale:** 5 | **Domain:** Behavioral Health | **Unit:** ED visits per 100k
- **Baseline:** 42/100k (2023). Range: 15-110. **Source:** CDC, HCUP.

### Node 621: Alcohol Poisoning ED Visit Rate
- **Scale:** 7 | **Domain:** Behavioral Health | **Unit:** Visits per 100k
- **Baseline:** 38/100k (2023). Range: 18-75. **Source:** HCUP NEDS.

### Node 622: Substance Use-Related ED Visit Rate
- **Scale:** 7 | **Domain:** Behavioral Health | **Unit:** Visits per 1k pop
- **Baseline:** 12.5/1k (2023). Range: 6-28. **Source:** HCUP NEDS, state.

### Node 623: Involuntary Psychiatric Hold Rate
- **Scale:** 4 | **Domain:** Mental Health | **Unit:** Holds per 1k pop
- **Baseline:** 3.2/1k (2023). Range: 1.5-7.5. **Source:** State systems.

### Node 624: Psychiatric Emergency Service Utilization
- **Scale:** 4 | **Domain:** Mental Health | **Unit:** Crisis ED visits per 1k
- **Baseline:** 8.5/1k (2023). Range: 4-18. **Source:** HCUP, state systems.

### Node 625: Suicide by Firearm Rate
- **Scale:** 4 | **Domain:** Mental Health, Violence | **Unit:** Deaths per 100k
- **Baseline:** 7.7/100k (2023). Range: 2.5-18. **Source:** CDC WONDER.

### Node 626: Drug-Involved Crime Rate
- **Scale:** 5 | **Domain:** Criminal Justice, Behavioral | **Unit:** Arrests per 1k pop
- **Baseline:** 4.2/1k (2023). Range: 1.8-9.5. **Source:** FBI UCR, state.

### Node 627: Fentanyl-Involved Overdose Rate
- **Scale:** 5 | **Domain:** Behavioral Health | **Unit:** Deaths per 100k
- **Baseline:** 18.5/100k (2023). Range: 3-55. **Source:** CDC WONDER, state.

### Node 628: Polysubstance Overdose Rate
- **Scale:** 5 | **Domain:** Behavioral Health | **Unit:** Deaths per 100k
- **Baseline:** 12.2/100k (2023). Range: 4-35. **Source:** CDC WONDER.

### Node 629: Naloxone Administration Rate (EMS)
- **Scale:** 5 | **Domain:** Behavioral Health | **Unit:** Administrations per 1k pop
- **Baseline:** 2.8/1k (2023). Range: 0.5-12. **Source:** EMS, NEMSIS.

### Node 630: Substance Use Treatment Dropout Rate
- **Scale:** 5 | **Domain:** Behavioral Health | **Unit:** % leaving against advice
- **Baseline:** 32% (2023). Range: 22-48%. **Source:** TEDS, state.

---

## 5.5 INFECTIOUS DISEASE CRISES

### Node 631: HIV Incidence
- **Scale:** 6 | **Domain:** Health | **Unit:** New diagnoses per 100k
- **Baseline:** 12.5/100k (2023). Range: 3-45. **Source:** CDC HIV surveillance, state.

### Node 632: Hepatitis C Incidence
- **Scale:** 6 | **Domain:** Health | **Unit:** Acute HCV per 100k
- **Baseline:** 1.2/100k (2023). Range: 0.3-4.5. **Source:** CDC, state.

### Node 633: Tuberculosis Incidence
- **Scale:** 6 | **Domain:** Health | **Unit:** TB cases per 100k
- **Baseline:** 2.5/100k (2023). Range: 0.5-12. **Source:** CDC TB surveillance, state.

### Node 634: Sexually Transmitted Infection Rate (Composite)
- **Scale:** 4 | **Domain:** Health | **Unit:** STI cases per 100k
- **Baseline:** 680/100k (2023). Range: 320-1,400. **Source:** CDC STD surveillance.

### Node 635: Chlamydia Incidence
- **Scale:** 6 | **Domain:** Health | **Unit:** Cases per 100k
- **Baseline:** 495/100k (2023). Range: 220-950. **Source:** CDC, state.

### Node 636: Gonorrhea Incidence
- **Scale:** 6 | **Domain:** Health | **Unit:** Cases per 100k
- **Baseline:** 172/100k (2023). Range: 65-420. **Source:** CDC, state.

### Node 637: Syphilis Incidence
- **Scale:** 6 | **Domain:** Health | **Unit:** Cases per 100k
- **Baseline:** 18.5/100k (2023). Range: 4-65. **Source:** CDC, state.

### Node 638: Congenital Syphilis Rate
- **Scale:** 4 | **Domain:** Maternal, Child | **Unit:** Cases per 100k live births
- **Baseline:** 78/100k births (2023, rising). Range: 15-220. **Source:** CDC, state.

### Node 639: Vaccine-Preventable Disease Incidence
- **Scale:** 6 | **Domain:** Health | **Unit:** Cases per 100k
- **Baseline:** 15/100k (2023). Range: 3-45. **Source:** CDC, state.

### Node 640: Healthcare-Associated Infection Rate
- **Scale:** 2 | **Domain:** Health | **Unit:** HAIs per 1k patient-days
- **Baseline:** 3.2/1k days (2023). Range: 1.8-6.5. **Source:** CDC NHSN, CMS.

### Node 641: C. difficile Infection Rate
- **Scale:** 2 | **Domain:** Health | **Unit:** CDI per 100k pop
- **Baseline:** 68/100k (2023). Range: 35-125. **Source:** CDC, EIP.

### Node 642: MRSA Infection Rate
- **Scale:** 2 | **Domain:** Health | **Unit:** Invasive MRSA per 100k
- **Baseline:** 18/100k (2023). Range: 8-38. **Source:** CDC ABCs.

### Node 643: Foodborne Illness Outbreak Rate
- **Scale:** 2 | **Domain:** Health, Food | **Unit:** Outbreaks per 1M pop
- **Baseline:** 4.5/1M (2023). Range: 1.5-12. **Source:** CDC FoodNet.

### Node 644: Waterborne Disease Rate
- **Scale:** 4 | **Domain:** Health, Environmental | **Unit:** Cases per 100k
- **Baseline:** 2.8/100k (2023). Range: 0.5-12. **Source:** CDC, state.

### Node 645: Vector-Borne Disease Incidence
- **Scale:** 6 | **Domain:** Health, Environmental | **Unit:** Cases per 100k
- **Baseline:** 28/100k (2023). Range: 5-95. **Source:** CDC ArboNET, state.

---

## 5.6 INJURY & VIOLENCE CRISES

### Node 646: Traumatic Brain Injury (TBI) Hospitalization
- **Scale:** 4 | **Domain:** Injury | **Unit:** TBI admits per 100k
- **Baseline:** 82/100k (2023). Range: 55-135. **Source:** HCUP, CDC.

### Node 647: Spinal Cord Injury Incidence
- **Scale:** 6 | **Domain:** Injury | **Unit:** SCI per 1M pop
- **Baseline:** 54/1M (2023). Range: 32-85. **Source:** NSCISC.

### Node 648: Burn Injury Hospitalization
- **Scale:** 4 | **Domain:** Injury | **Unit:** Admits per 100k
- **Baseline:** 12.5/100k (2023). Range: 7-22. **Source:** HCUP, ABA.

### Node 649: Fall-Related Injury (Age 65+)
- **Scale:** 4 | **Domain:** Injury | **Unit:** ED visits per 1k elderly
- **Baseline:** 82/1k (2023). Range: 55-125. **Source:** HCUP, CDC WISQARS.

### Node 650: Unintentional Poisoning Rate
- **Scale:** 4 | **Domain:** Injury | **Unit:** ED visits per 100k
- **Baseline:** 185/100k (2023). Range: 95-350. **Source:** HCUP, CDC.

### Node 651: Motor Vehicle Crash Injury Rate
- **Scale:** 4 | **Domain:** Transportation, Injury | **Unit:** Injuries per 1k pop
- **Baseline:** 8.2/1k (2023). Range: 4.5-15. **Source:** NHTSA, state.

### Node 652: Pedestrian Injury Rate
- **Scale:** 4 | **Domain:** Transportation, Injury | **Unit:** Injuries per 100k
- **Baseline:** 42/100k (2023). Range: 18-95. **Source:** NHTSA, state.

### Node 653: Bicycle Crash Injury Rate
- **Scale:** 4 | **Domain:** Transportation, Injury | **Unit:** Injuries per 100k
- **Baseline:** 22/100k (2023). Range: 8-52. **Source:** NHTSA, local.

### Node 654: Drowning Incidence
- **Scale:** 6 | **Domain:** Injury | **Unit:** Deaths + rescues per 100k
- **Baseline:** 3.8/100k (2023). Range: 1.5-9.5. **Source:** CDC WONDER, Coast Guard.

### Node 655: Firearm Injury (Nonfatal) Rate
- **Scale:** 4 | **Domain:** Violence, Injury | **Unit:** ED visits per 100k
- **Baseline:** 28/100k (2023). Range: 8-95. **Source:** HCUP, CDC WISQARS.

### Node 656: Intimate Partner Violence (IPV) Injury Rate
- **Scale:** 4 | **Domain:** Violence | **Unit:** ED visits per 100k
- **Baseline:** 45/100k (2023). Range: 22-95. **Source:** HCUP, NISVS.

### Node 657: Child Maltreatment Substantiated Rate
- **Scale:** 4 | **Domain:** Child, Violence | **Unit:** Victims per 1k children
- **Baseline:** 8.4/1k (2023). Range: 4.5-16. **Source:** ACF NCANDS, state.

### Node 658: Child Physical Abuse Rate
- **Scale:** 4 | **Domain:** Child, Violence | **Unit:** Substantiated per 1k
- **Baseline:** 2.8/1k (2023). Range: 1.2-6.5. **Source:** NCANDS.

### Node 659: Child Sexual Abuse Rate
- **Scale:** 4 | **Domain:** Child, Violence | **Unit:** Substantiated per 1k
- **Baseline:** 0.8/1k (2023). Range: 0.3-2.2. **Source:** NCANDS.

### Node 660: Child Neglect Rate
- **Scale:** 4 | **Domain:** Child, Social | **Unit:** Substantiated per 1k
- **Baseline:** 5.2/1k (2023). Range: 2.5-11. **Source:** NCANDS.

### Node 661: Elder Abuse/Neglect (Reported) Rate
- **Scale:** 4 | **Domain:** Social, Violence | **Unit:** Reports per 1k age 65+
- **Baseline:** 18/1k (2023). Range: 8-38. **Source:** APS, NCEA.

### Node 662: Assault Injury Rate
- **Scale:** 4 | **Domain:** Violence | **Unit:** ED visits per 1k pop
- **Baseline:** 6.8/1k (2023). Range: 3.5-18. **Source:** HCUP, CDC.

### Node 663: Sexual Assault Rate
- **Scale:** 4 | **Domain:** Violence | **Unit:** Reports per 100k
- **Baseline:** 42/100k (2023). Range: 18-85. **Source:** FBI UCR, NISVS.

### Node 664: Human Trafficking (Identified) Rate
- **Scale:** 4 | **Domain:** Violence, Criminal Justice | **Unit:** Cases per 100k
- **Baseline:** 1.2/100k (2023). Range: 0.3-5.5. **Source:** DOJ, NHTH.

### Node 665: Workplace Violence Rate
- **Scale:** 4 | **Domain:** Occupational, Violence | **Unit:** Incidents per 1k workers
- **Baseline:** 3.5/1k (2023). Range: 1.5-8.5. **Source:** BLS, OSHA.

---

## 5.7 HOUSING & ECONOMIC CRISES

### Node 666: Homelessness Rate (Point-in-Time)
- **Scale:** 7 | **Domain:** Housing | **Unit:** Homeless per 10k pop
- **Baseline:** 18/10k (2023). Range: 6-65. **Source:** HUD PIT, CoC.

### Node 667: Unsheltered Homelessness Rate
- **Scale:** 7 | **Domain:** Housing | **Unit:** Unsheltered per 10k
- **Baseline:** 7.5/10k (2023). Range: 1.5-35. **Source:** HUD PIT.

### Node 668: Family Homelessness Rate
- **Scale:** 7 | **Domain:** Housing, Child | **Unit:** Homeless families per 10k HH
- **Baseline:** 4.2/10k (2023). Range: 1.5-15. **Source:** HUD PIT.

### Node 669: Youth Homelessness (Unaccompanied) Rate
- **Scale:** 7 | **Domain:** Housing, Child | **Unit:** Homeless youth per 10k age <25
- **Baseline:** 2.8/10k (2023). Range: 0.8-9.5. **Source:** HUD PIT, Chapin Hall.

### Node 670: Eviction Judgment Rate
- **Scale:** 4 | **Domain:** Housing, Economic | **Unit:** Evictions per 100 rentals
- **Baseline:** 2.2/100 (2023). Range: 0.8-5.5. **Source:** Eviction Lab, courts.

### Node 671: Foreclosure Rate
- **Scale:** 7 | **Domain:** Housing, Economic | **Unit:** Foreclosures per 1k owner units
- **Baseline:** 1.8/1k (2023). Range: 0.5-6.5. **Source:** RealtyTrac, state.

### Node 672: Utility Disconnection Rate
- **Scale:** 4 | **Domain:** Housing, Economic | **Unit:** Disconnects per 1k HH
- **Baseline:** 12/1k (2023). Range: 4-32. **Source:** Utilities, PUC.

### Node 673: Food Bank Emergency Distribution Rate
- **Scale:** 4 | **Domain:** Food, Economic | **Unit:** Emergency visits per 1k pop
- **Baseline:** 145/1k (2023). Range: 65-350. **Source:** Feeding America.

### Node 674: Personal Bankruptcy Filing Rate
- **Scale:** 4 | **Domain:** Economic | **Unit:** Filings per 1k adults
- **Baseline:** 1.8/1k (2023). Range: 0.8-4.2. **Source:** Courts, ABI.

### Node 675: Wage Garnishment Rate
- **Scale:** 4 | **Domain:** Economic | **Unit:** Garnishments per 1k workers
- **Baseline:** 6.5/1k (2023). Range: 3-14. **Source:** ADP, courts.

### Node 676: Vehicle Repossession Rate
- **Scale:** 4 | **Domain:** Economic, Transportation | **Unit:** Repos per 1k financed vehicles
- **Baseline:** 8.5/1k (2023). Range: 4-18. **Source:** Industry data.

### Node 677: Payday Loan Default Rate
- **Scale:** 4 | **Domain:** Economic | **Unit:** % loans defaulted
- **Baseline:** 22% (2023). Range: 15-35%. **Source:** CFPB, Pew.

### Node 678: Medical Debt Collections Rate
- **Scale:** 4 | **Domain:** Economic, Healthcare | **Unit:** % adults with medical collections
- **Baseline:** 18% (2023). Range: 10-32%. **Source:** CFPB, Urban Institute.

### Node 679: Child Foster Care Entry Rate
- **Scale:** 4 | **Domain:** Child, Social | **Unit:** Entries per 1k children
- **Baseline:** 3.8/1k (2023). Range: 1.8-9.5. **Source:** ACF AFCARS, state.

### Node 680: Child Welfare System Involvement Rate
- **Scale:** 4 | **Domain:** Child, Social | **Unit:** Investigations per 1k children
- **Baseline:** 42/1k (2023). Range: 22-85. **Source:** NCANDS, state.

---

## 5.8 CRIMINAL JUSTICE CRISES

### Node 681: Jail Incarceration Rate
- **Scale:** 7 | **Domain:** Criminal Justice | **Unit:** Jailed per 100k pop
- **Baseline:** 225/100k (2023). Range: 95-450. **Source:** BJS, jails.

### Node 682: Prison Incarceration Rate
- **Scale:** 7 | **Domain:** Criminal Justice | **Unit:** Imprisoned per 100k
- **Baseline:** 350/100k (2023). Range: 180-650. **Source:** BJS, state DOC.

### Node 683: Jail Mortality Rate
- **Scale:** 7 | **Domain:** Criminal Justice, Health | **Unit:** Deaths per 100k inmates
- **Baseline:** 185/100k (2023). Range: 95-350. **Source:** BJS, jails.

### Node 684: Prison Mortality Rate
- **Scale:** 7 | **Domain:** Criminal Justice, Health | **Unit:** Deaths per 100k inmates
- **Baseline:** 295/100k (2023). Range: 180-520. **Source:** BJS, state DOC.

### Node 685: Police Use of Force Incidents
- **Scale:** 4 | **Domain:** Criminal Justice, Violence | **Unit:** Incidents per 1k arrests
- **Baseline:** 18/1k (2023). Range: 8-45. **Source:** FBI, local agencies.

### Node 686: Police Shooting Rate
- **Scale:** 4 | **Domain:** Criminal Justice, Violence | **Unit:** Shootings per 1M pop
- **Baseline:** 3.5/1M (2023). Range: 0.8-12. **Source:** Mapping Police Violence, WaPo.

### Node 687: Wrongful Conviction Exoneration Rate
- **Scale:** 4 | **Domain:** Criminal Justice | **Unit:** Exonerations per 100k incarcerated
- **Baseline:** 8.5/100k (2023). Range: 3-22. **Source:** National Registry.

### Node 688: Juvenile Detention Rate
- **Scale:** 4 | **Domain:** Criminal Justice, Child | **Unit:** Youth detained per 100k age 10-17
- **Baseline:** 125/100k (2023). Range: 45-285. **Source:** OJJDP, state.

### Node 689: Juvenile Transfer to Adult Court Rate
- **Scale:** 4 | **Domain:** Criminal Justice, Child | **Unit:** Transfers per 1k juvenile arrests
- **Baseline:** 4.2/1k (2023). Range: 1-12. **Source:** OJJDP, state.

### Node 690: Pretrial Detention Mortality
- **Scale:** 3 | **Domain:** Criminal Justice, Health | **Unit:** Deaths per 100k pretrial detainees
- **Baseline:** 145/100k (2023). Range: 65-320. **Source:** BJS, jails.

---

## 5.9 EDUCATIONAL CRISES

### Node 691: High School Dropout Rate
- **Scale:** 6 | **Domain:** Education | **Unit:** % not completing HS
- **Baseline:** 5.3% (2023). Range: 2.8-12%. **Source:** NCES, state.

### Node 692: College Dropout Rate (First Year)
- **Scale:** 6 | **Domain:** Education | **Unit:** % not returning 2nd year
- **Baseline:** 26% (2023). Range: 12-42%. **Source:** NCES IPEDS.

### Node 693: Student Loan Default Rate (3-Year)
- **Scale:** 4 | **Domain:** Education, Economic | **Unit:** % defaulting within 3yr
- **Baseline:** 7.6% (2023). Range: 3-22%. **Source:** ED FSA, institution.

### Node 694: School Expulsion Rate
- **Scale:** 4 | **Domain:** Education | **Unit:** % students expelled
- **Baseline:** 0.4% (2023). Range: 0.1-1.5%. **Source:** ED CRDC, district.

### Node 695: School-Based Arrest Rate
- **Scale:** 4 | **Domain:** Education, Criminal Justice | **Unit:** Arrests per 1k students
- **Baseline:** 4.2/1k (2023). Range: 0.5-15. **Source:** ED CRDC, district.

---

## 5.10 HEALTHCARE SYSTEM FAILURE ENDPOINTS

### Node 696: Emergency Department Boarding Time
- **Scale:** 3 | **Domain:** Healthcare | **Unit:** Median hours boarded
- **Baseline:** 4.2 hrs (2023). Range: 1.5-12. **Source:** Hospitals, ACEP.

### Node 697: ED Walkout/Left Without Being Seen Rate
- **Scale:** 3 | **Domain:** Healthcare | **Unit:** % LWBS
- **Baseline:** 2.8% (2023). Range: 1-8%. **Source:** Hospitals, HCUP.

### Node 698: Ambulance Diversion Hours
- **Scale:** 3 | **Domain:** Healthcare | **Unit:** Hours on diversion annually
- **Baseline:** 85 hrs (2023). Range: 0-650. **Source:** EMS, hospitals.

### Node 699: Hospital Bed Occupancy (>95%)
- **Scale:** 3 | **Domain:** Healthcare | **Unit:** Days at surge capacity
- **Baseline:** 45 days (2023). Range: 5-180. **Source:** Hospitals, AHA.

### Node 700: ICU Bed Shortage Days
- **Scale:** 2 | **Domain:** Healthcare | **Unit:** Days no ICU beds
- **Baseline:** 12 days (2023). Range: 0-95. **Source:** Hospitals, state.

### Node 701: Mental Health Bed Shortage (Crisis)
- **Scale:** 2 | **Domain:** Mental Health, Healthcare | **Unit:** % psych admits delayed 24+ hrs
- **Baseline:** 38% (2023). Range: 18-72%. **Source:** State systems.

### Node 702: Medication Shortage Impact
- **Scale:** 2 | **Domain:** Healthcare | **Unit:** Critical shortages per year
- **Baseline:** 145 shortages (2023). Range: 85-220. **Source:** FDA, ASHP.

### Node 703: Healthcare Worker Shortage (Vacancy Rate)
- **Scale:** 2 | **Domain:** Healthcare | **Unit:** % RN positions vacant
- **Baseline:** 9.5% (2023). Range: 4-22%. **Source:** Hospitals, BLS.

### Node 704: Preventable Medical Error Rate
- **Scale:** 7 | **Domain:** Healthcare | **Unit:** Serious events per 1k admits
- **Baseline:** 2.8/1k (2023). Range: 1.2-6.5. **Source:** AHRQ PSI, CMS.

### Node 705: Hospital-Acquired Condition Rate
- **Scale:** 6 | **Domain:** Healthcare | **Unit:** HACs per 1k admits
- **Baseline:** 18/1k (2023). Range: 10-32. **Source:** CMS HAC.

### Node 706: Surgical Site Infection Rate
- **Scale:** 4 | **Domain:** Healthcare | **Unit:** SSI per 100 surgeries
- **Baseline:** 1.8/100 (2023). Range: 0.8-4.5. **Source:** CDC NHSN.

### Node 707: Central Line Infection (CLABSI) Rate
- **Scale:** 4 | **Domain:** Healthcare | **Unit:** CLABSI per 1k line-days
- **Baseline:** 0.8/1k (2023). Range: 0.3-2.5. **Source:** CDC NHSN, CMS.

### Node 708: Catheter UTI (CAUTI) Rate
- **Scale:** 4 | **Domain:** Healthcare | **Unit:** CAUTI per 1k catheter-days
- **Baseline:** 1.2/1k (2023). Range: 0.5-3.2. **Source:** CDC NHSN, CMS.

### Node 709: Ventilator-Associated Pneumonia (VAP) Rate
- **Scale:** 4 | **Domain:** Healthcare | **Unit:** VAP per 1k ventilator-days
- **Baseline:** 0.9/1k (2023). Range: 0.3-2.8. **Source:** CDC NHSN.

### Node 710: Wrong-Site Surgery Rate
- **Scale:** 4 | **Domain:** Healthcare | **Unit:** Events per 100k surgeries
- **Baseline:** 1.2/100k (2023). Range: 0.3-4.5. **Source:** Joint Commission, PSO.

---

## 5.11 ENVIRONMENTAL & CLIMATE CRISIS EVENTS

### Node 711: Heat Wave Mortality Events
- **Scale:** 4 | **Domain:** Climate, Health | **Unit:** Deaths per heat event
- **Baseline:** 8.5/event (2023). Range: 2-45. **Source:** CDC, NOAA.

### Node 712: Wildfire Evacuation Events
- **Scale:** 2 | **Domain:** Climate, Housing | **Unit:** Evacuations per 1M pop
- **Baseline:** 18/1M (2023). Range: 0-250. **Source:** CAL FIRE, FEMA.

### Node 713: Flood Displacement Events
- **Scale:** 2 | **Domain:** Climate, Housing | **Unit:** Displacements per 100k
- **Baseline:** 12/100k (2023). Range: 0-450. **Source:** FEMA, Red Cross.

### Node 714: Hurricane/Storm Casualties
- **Scale:** 2 | **Domain:** Climate, Health | **Unit:** Deaths + injuries per event
- **Baseline:** 22/major event (2023). Range: 3-850. **Source:** NOAA, FEMA.

### Node 715: Tornado Fatality Rate
- **Scale:** 7 | **Domain:** Climate, Health | **Unit:** Deaths per year
- **Baseline:** 75/year US (2023). Range: 25-550. **Source:** NOAA SPC.

### Node 716: Air Quality Emergency Days
- **Scale:** 2 | **Domain:** Environmental | **Unit:** Days AQI >150
- **Baseline:** 3.5 days (2023). Range: 0-28. **Source:** EPA AirNow, county.

### Node 717: Water System Failure Events
- **Scale:** 2 | **Domain:** Environmental | **Unit:** Boil orders per 100k pop
- **Baseline:** 2.8/100k (2023). Range: 0.5-18. **Source:** EPA, state.

### Node 718: Lead Poisoning Crisis (Community-Level)
- **Scale:** 2 | **Domain:** Environmental, Child | **Unit:** % children BLL ≥5 μg/dL in cluster
- **Baseline:** Varies (crisis if >10%). **Source:** CDC, state surveillance.

### Node 719: Chemical Spill/Exposure Events
- **Scale:** 2 | **Domain:** Environmental | **Unit:** Events per 1M pop
- **Baseline:** 1.2/1M (2023). Range: 0.2-8. **Source:** EPA, NRC.

### Node 720: Power Grid Failure (Extended Outage)
- **Scale:** 4 | **Domain:** Infrastructure | **Unit:** Outages >4hrs per 100k pop
- **Baseline:** 3.5/100k (2023). Range: 0.5-22. **Source:** DOE, utilities.

---

## 5.12 ADDITIONAL HEALTH CRISES

### Node 721: Acute Kidney Injury Hospitalization
- **Scale:** 4 | **Domain:** Health | **Unit:** AKI admits per 1k adults
- **Baseline:** 18/1k (2023). Range: 12-28. **Source:** Hospital data, CMS.

### Node 722: Acute Liver Failure Incidence
- **Scale:** 6 | **Domain:** Health | **Unit:** ALF per 1M pop
- **Baseline:** 8.5/1M (2023). Range: 4-18. **Source:** Hospital data, UNOS.

### Node 723: Anaphylaxis ED Visit Rate
- **Scale:** 7 | **Domain:** Health | **Unit:** Visits per 100k
- **Baseline:** 42/100k (2023). Range: 22-85. **Source:** HCUP.

### Node 724: Diabetic Coma Rate
- **Scale:** 6 | **Domain:** Health | **Unit:** Coma admits per 1k diabetics
- **Baseline:** 1.8/1k (2023). Range: 0.8-4.5. **Source:** Hospital data.

### Node 725: Acute Respiratory Failure Rate
- **Scale:** 4 | **Domain:** Health | **Unit:** ARF admits per 1k adults
- **Baseline:** 12.5/1k (2023). Range: 8-22. **Source:** Hospital data, HCUP.

### Node 726: Pulmonary Embolism Incidence
- **Scale:** 6 | **Domain:** Health | **Unit:** PE per 100k
- **Baseline:** 68/100k (2023). Range: 42-115. **Source:** Hospital data.

### Node 727: Aortic Aneurysm Rupture Rate
- **Scale:** 4 | **Domain:** Health | **Unit:** Ruptures per 100k age 50+
- **Baseline:** 8.5/100k (2023). Range: 4.5-16. **Source:** Hospital data.

### Node 728: Cardiac Arrest (Out-of-Hospital) Rate
- **Scale:** 4 | **Domain:** Health | **Unit:** OHCA per 100k
- **Baseline:** 95/100k (2023). Range: 65-145. **Source:** CARES, EMS.

### Node 729: Sudden Infant Death Syndrome (SIDS) Rate
- **Scale:** 4 | **Domain:** Child | **Unit:** Deaths per 100k live births
- **Baseline:** 38/100k (2023). Range: 22-68. **Source:** NVSS, CDC.

### Node 730: Pregnancy Loss (Miscarriage) Rate
- **Scale:** 4 | **Domain:** Maternal | **Unit:** Losses per 100 pregnancies
- **Baseline:** 15/100 (2023). Range: 12-22. **Source:** Research, NVSS.

### Node 731: Ectopic Pregnancy Rate
- **Scale:** 6 | **Domain:** Maternal | **Unit:** Per 1k pregnancies
- **Baseline:** 20/1k (2023). Range: 14-32. **Source:** Hospital data, research.

### Node 732: Postpartum Hemorrhage (Severe) Rate
- **Scale:** 4 | **Domain:** Maternal | **Unit:** Severe PPH per 1k deliveries
- **Baseline:** 12/1k (2023). Range: 7-22. **Source:** Hospital data, HCUP.

### Node 733: Obstetric Embolism Rate
- **Scale:** 4 | **Domain:** Maternal | **Unit:** Embolism per 100k deliveries
- **Baseline:** 18/100k (2023). Range: 8-38. **Source:** Hospital data.

### Node 734: Hypertensive Crisis (Emergency) Rate
- **Scale:** 4 | **Domain:** Health | **Unit:** Crises per 100k adults
- **Baseline:** 45/100k (2023). Range: 22-85. **Source:** ED data.

### Node 735: Hypoglycemic Emergency (Nond diabetic)
- **Scale:** 4 | **Domain:** Health | **Unit:** ED visits per 100k
- **Baseline:** 18/100k (2023). Range: 8-38. **Source:** HCUP.

### Node 736: Severe Allergic Reaction Rate
- **Scale:** 4 | **Domain:** Health | **Unit:** ED visits per 100k
- **Baseline:** 85/100k (2023). Range: 45-165. **Source:** HCUP.

### Node 737: Dehydration Hospitalization (Elderly)
- **Scale:** 2 | **Domain:** Health | **Unit:** Admits per 1k age 65+
- **Baseline:** 8.5/1k (2023). Range: 4.5-16. **Source:** CMS, hospital data.

### Node 738: Malnutrition Hospitalization Rate
- **Scale:** 7 | **Domain:** Health, Food | **Unit:** Admits per 100k
- **Baseline:** 22/100k (2023). Range: 10-52. **Source:** HCUP.

### Node 739: Hypothermia/Frostbite Incidence
- **Scale:** 6 | **Domain:** Climate, Health | **Unit:** Cases per 100k
- **Baseline:** 3.5/100k (2023). Range: 0.5-18. **Source:** ED data, CDC.

### Node 740: Heat Stroke Incidence
- **Scale:** 6 | **Domain:** Climate, Health | **Unit:** Cases per 100k
- **Scale:** 12/100k (2023). Range: 2-65. **Source:** ED data, CDC ESSENCE.

### Node 741: Carbon Monoxide Poisoning Rate
- **Scale:** 4 | **Domain:** Environmental, Housing | **Unit:** ED visits per 100k
- **Baseline:** 18/100k (2023). Range: 8-42. **Source:** HCUP, CDC.

### Node 742: Lead Poisoning (Adults) Rate
- **Scale:** 4 | **Domain:** Environmental, Occupational | **Unit:** BLL ≥10 μg/dL per 100k adults
- **Baseline:** 8.5/100k (2023). Range: 2-35. **Source:** State surveillance, OSHA.

### Node 743: Pesticide Poisoning Rate
- **Scale:** 4 | **Domain:** Environmental, Occupational | **Unit:** Cases per 100k
- **Baseline:** 4.5/100k (2023). Range: 1.2-22. **Source:** Poison centers, NPDS.

### Node 744: Asthma Exacerbation (Severe) Rate
- **Scale:** 4 | **Domain:** Health | **Unit:** Severe exacerbations per 1k asthmatics
- **Baseline:** 85/1k (2023). Range: 45-165. **Source:** ED data, claims.

### Node 745: COPD Exacerbation (Severe) Rate
- **Scale:** 4 | **Domain:** Health | **Unit:** Severe exacerbations per 1k COPD
- **Baseline:** 125/1k (2023). Range: 65-245. **Source:** ED data, CMS.

### Node 746: Sickle Cell Crisis Rate
- **Scale:** 4 | **Domain:** Health | **Unit:** Crises per 100 SCD patients
- **Baseline:** 85/100 (2023). Range: 45-165. **Source:** Hospital data.

### Node 747: Seizure-Related ED Visit Rate
- **Scale:** 7 | **Domain:** Health | **Unit:** Visits per 100k
- **Baseline:** 145/100k (2023). Range: 85-245. **Source:** HCUP NEDS.

### Node 748: Opioid Withdrawal Hospitalization
- **Scale:** 4 | **Domain:** Behavioral Health | **Unit:** Admits per 100k
- **Baseline:** 38/100k (2023). Range: 15-95. **Source:** Hospital data.

### Node 749: Alcohol Withdrawal (Severe) Rate
- **Scale:** 4 | **Domain:** Behavioral Health | **Unit:** DT/severe withdrawal per 100k
- **Baseline:** 22/100k (2023). Range: 10-52. **Source:** Hospital data.

### Node 750: Psychiatric Crisis (Non-Suicide) Rate
- **Scale:** 4 | **Domain:** Mental Health | **Unit:** Crisis ED visits per 1k pop
- **Baseline:** 6.5/1k (2023). Range: 3.5-14. **Source:** HCUP, state systems.

---

## 5.13 DISABILITY & FUNCTIONAL DECLINE CRISES

### Node 751: New Wheelchair Dependence Rate
- **Scale:** 4 | **Domain:** Disability | **Unit:** New wheelchair users per 1k adults
- **Baseline:** 2.8/1k (2023). Range: 1.5-5.5. **Source:** Medicare, surveys.

### Node 752: New Blindness/Severe Vision Loss Rate
- **Scale:** 4 | **Domain:** Disability | **Unit:** Incident blindness per 100k
- **Baseline:** 85/100k (2023). Range: 45-165. **Source:** Medicare, NEI.

### Node 753: New Deafness/Severe Hearing Loss Rate
- **Scale:** 4 | **Domain:** Disability | **Unit:** Incident severe loss per 100k
- **Baseline:** 145/100k (2023). Range: 75-285. **Source:** Medicare, surveys.

### Node 754: Amputation (Non-Trauma) Rate
- **Scale:** 4 | **Domain:** Health, Disability | **Unit:** Amputations per 100k
- **Baseline:** 28/100k (2023). Range: 15-65. **Source:** Hospital data, CMS.

### Node 755: Stroke-Related Disability Rate
- **Scale:** 4 | **Domain:** Health, Disability | **Unit:** % strokes with lasting disability
- **Baseline:** 42% (2023). Range: 32-58%. **Source:** Hospital data, registries.

### Node 756: TBI-Related Disability Rate
- **Scale:** 4 | **Domain:** Injury, Disability | **Unit:** % TBI with lasting impairment
- **Baseline:** 38% (2023). Range: 25-55%. **Source:** Research, TBI Model Systems.

### Node 757: Dementia Diagnosis Rate
- **Scale:** 6 | **Domain:** Health, Disability | **Unit:** New diagnoses per 1k age 65+
- **Baseline:** 22/1k (2023). Range: 14-38. **Source:** Medicare, claims.

### Node 758: Functional Decline (ADL Loss)
- **Scale:** 4 | **Domain:** Disability, LTSS | **Unit:** % age 65+ losing ADL independence
- **Baseline:** 8.5% annually (2023). Range: 5-15%. **Source:** Medicare, NHATS.

### Node 759: Nursing Home Placement (Unplanned)
- **Scale:** 4 | **Domain:** LTSS, Disability | **Unit:** Emergency placements per 1k age 65+
- **Baseline:** 4.5/1k (2023). Range: 2.5-9.5. **Source:** CMS, state.

### Node 760: Falls with Serious Injury (Age 65+)
- **Scale:** 6 | **Domain:** Injury, Disability | **Unit:** Falls with fracture/TBI per 1k elderly
- **Baseline:** 18/1k (2023). Range: 10-35. **Source:** Hospital data, CDC.

---

## 5.14 ADDITIONAL SYSTEM FAILURE & CRISIS INDICATORS

### Node 761: Ambulance Response Time >10min
- **Scale:** 6 | **Domain:** Healthcare, Emergency | **Unit:** % calls >10min response
- **Baseline:** 18% (2023). Range: 8-42%. **Source:** EMS, NEMSIS.

### Node 762: Ambulance Transport Refusal Rate
- **Scale:** 6 | **Domain:** Healthcare, Economic | **Unit:** % refusing transport due to cost
- **Baseline:** 8.5% (2023). Range: 3.5-18%. **Source:** EMS, NEMSIS.

### Node 763: Mental Health Crisis Call Volume
- **Scale:** 6 | **Domain:** Mental Health | **Unit:** MH crisis calls per 1k pop
- **Baseline:** 12.5/1k (2023). Range: 5.5-28. **Source:** 988, crisis lines.

### Node 764: Poison Control Center Call Rate
- **Scale:** 4 | **Domain:** Health, Environmental | **Unit:** Calls per 1k pop
- **Baseline:** 32/1k (2023). Range: 18-55. **Source:** NPDS, AAPCC.

### Node 765: Child Protective Services Removal Rate
- **Scale:** 4 | **Domain:** Child, Social | **Unit:** Removals per 1k children
- **Baseline:** 3.2/1k (2023). Range: 1.5-7.5. **Source:** AFCARS, state.

### Node 766: Adult Protective Services Investigation Rate
- **Scale:** 4 | **Domain:** Social, Disability | **Unit:** Investigations per 1k age 65+
- **Baseline:** 22/1k (2023). Range: 10-45. **Source:** State APS systems.

### Node 767: Domestic Violence Shelter Utilization
- **Scale:** 3 | **Domain:** Violence, Housing | **Unit:** Shelter days per 1k pop
- **Baseline:** 85/1k (2023). Range: 35-185. **Source:** NNEDV, state.

### Node 768: Crisis Pregnancy Center Utilization
- **Scale:** 4 | **Domain:** Maternal, Economic | **Unit:** Visits per 1k women 15-44
- **Baseline:** 42/1k (2023). Range: 18-95. **Source:** CPC networks, surveys.

### Node 769: Emergency Financial Assistance Requests
- **Scale:** 4 | **Domain:** Economic, Social | **Unit:** Requests per 1k pop
- **Baseline:** 65/1k (2023). Range: 28-145. **Source:** United Way 211, agencies.

### Node 770: Disaster Relief Application Rate
- **Scale:** 4 | **Domain:** Climate, Economic | **Unit:** FEMA applications per disaster
- **Baseline:** 850 per major disaster (2023). Range: 150-8,500. **Source:** FEMA.

### Node 771: Transfusion Reaction Rate
- **Scale:** 4 | **Domain:** Healthcare | **Unit:** Reactions per 1k transfusions
- **Baseline:** 1.2/1k (2023). Range: 0.5-3.5. **Source:** FDA, blood banks.

### Node 772: Organ Transplant Rejection (Acute) Rate
- **Scale:** 4 | **Domain:** Healthcare | **Unit:** Acute rejections per 100 transplants
- **Baseline:** 8.5/100 (2023). Range: 4-18. **Source:** UNOS, OPTN.

### Node 773: Dialysis Access Failure Rate
- **Scale:** 3 | **Domain:** Health | **Unit:** Access failures per 100 patient-years
- **Baseline:** 42/100 (2023). Range: 25-75. **Source:** USRDS, CMS.

### Node 774: Medical Device Failure/Recall Impact
- **Scale:** 3 | **Domain:** Healthcare | **Unit:** Serious device events per 100k pop
- **Baseline:** 18/100k (2023). Range: 8-42. **Source:** FDA MAUDE.

### Node 775: Blood Supply Shortage Days
- **Scale:** 3 | **Domain:** Healthcare | **Unit:** Days with critical shortage
- **Baseline:** 22 days (2023). Range: 5-85. **Source:** Red Cross, AABB.

### Node 776: Pharmacy Closure (Community Impact)
- **Scale:** 3 | **Domain:** Healthcare | **Unit:** Closures per 100k pop
- **Baseline:** 2.8/100k (2023). Range: 0.5-12. **Source:** NCPDP, pharmacy chains.

### Node 777: Mental Health Provider Burnout Rate
- **Scale:** 3 | **Domain:** Mental Health, Healthcare | **Unit:** % high burnout
- **Baseline:** 52% (2023). Range: 35-72%. **Source:** Surveys, research.

### Node 778: Healthcare Worker Assault Rate
- **Scale:** 4 | **Domain:** Healthcare, Violence | **Unit:** Assaults per 1k workers
- **Baseline:** 8.5/1k (2023). Range: 4-22. **Source:** BLS, OSHA.

### Node 779: School Shooting Incidents
- **Scale:** 3 | **Domain:** Violence, Education | **Unit:** Incidents per 10k schools
- **Baseline:** 0.8/10k (2023). Range: 0.2-2.5. **Source:** K-12 SSDB, FBI.

### Node 780: Mass Shooting Events
- **Scale:** 4 | **Domain:** Violence | **Unit:** Events (4+ shot) per 1M pop
- **Baseline:** 0.18/1M (2023). Range: 0.05-0.65. **Source:** GVA, FBI.

### Node 781: Hate Crime Rate
- **Scale:** 4 | **Domain:** Violence, Social | **Unit:** Offenses per 100k
- **Baseline:** 7.5/100k (2023). Range: 2.5-22. **Source:** FBI UCR, state.

### Node 782: Human Rights Violation (Documented) Rate
- **Scale:** 4 | **Domain:** Social, Criminal Justice | **Unit:** Violations per 100k
- **Baseline:** 4.2/100k (2023). Range: 1.2-15. **Source:** DOJ, advocacy orgs.

### Node 783: Labor Trafficking (Identified) Rate
- **Scale:** 4 | **Domain:** Economic, Violence | **Unit:** Cases per 100k
- **Baseline:** 0.8/100k (2023). Range: 0.2-3.5. **Source:** DOJ, NHTH.

### Node 784: Immigration Detention Rate
- **Scale:** 3 | **Domain:** Social, Criminal Justice | **Unit:** Detained per 1k immigrants
- **Baseline:** 12/1k (2023). Range: 3.5-35. **Source:** ICE, DHS.

### Node 785: Asylum Application Denial Rate
- **Scale:** 3 | **Domain:** Social | **Unit:** % applications denied
- **Baseline:** 68% (2023). Range: 45-88%. **Source:** EOIR, DHS.

### Node 786: Language Access Barrier (Healthcare)
- **Scale:** 3 | **Domain:** Healthcare, Social | **Unit:** % LEP reporting access issues
- **Baseline:** 42% LEP (2023). Range: 28-68%. **Source:** Surveys, OCR.

### Node 787: Medical Interpreter Unavailability Rate
- **Scale:** 3 | **Domain:** Healthcare, Social | **Unit:** % encounters needing but lacking interpreter
- **Baseline:** 22% (2023). Range: 12-45%. **Source:** Hospitals, surveys.

### Node 788: Disability Discrimination (Documented) Rate
- **Scale:** 4 | **Domain:** Disability, Social | **Unit:** Complaints per 100k with disability
- **Baseline:** 85/100k (2023). Range: 35-185. **Source:** EEOC, DOJ, HUD.

### Node 789: Housing Discrimination Complaints
- **Scale:** 4 | **Domain:** Housing, Social | **Unit:** Complaints per 100k pop
- **Baseline:** 18/100k (2023). Range: 8-42. **Source:** HUD FHEO.

### Node 790: Employment Discrimination Charges
- **Scale:** 4 | **Domain:** Employment, Social | **Unit:** Charges per 1k workers
- **Baseline:** 1.8/1k (2023). Range: 0.8-4.5. **Source:** EEOC.

### Node 791: Voting Rights Violation (Documented) Rate
- **Scale:** 4 | **Domain:** Civic, Social | **Unit:** Violations per 100k registered
- **Baseline:** 4.5/100k (2023). Range: 1.2-18. **Source:** DOJ, advocacy.

### Node 792: Public Benefit Application Denial Rate
- **Scale:** 3 | **Domain:** Economic, Social | **Unit:** % applications denied
- **Baseline:** 38% (2023). Range: 22-62%. **Source:** HHS, state agencies.

### Node 793: Medicaid Disenrollment (Procedural) Rate
- **Scale:** 3 | **Domain:** Healthcare, Economic | **Unit:** % disenrolled procedurally
- **Baseline:** 28% (2023 unwinding). Range: 15-55%. **Source:** CMS, KFF, state.

### Node 794: SNAP Benefit Reduction/Termination Rate
- **Scale:** 3 | **Domain:** Food, Economic | **Unit:** % benefits reduced/ended
- **Baseline:** 22% participants (2023). Range: 12-42%. **Source:** USDA FNS, state.

### Node 795: Childcare Center Closure Rate
- **Scale:** 3 | **Domain:** Child, Economic | **Unit:** Closures per 1k centers
- **Baseline:** 45/1k (2023). Range: 22-95. **Source:** State licensing, NAEYC.

### Node 796: Rural Hospital Closure Rate
- **Scale:** 3 | **Domain:** Healthcare | **Unit:** Closures per 1k rural hospitals
- **Baseline:** 12/1k annually (2023). Range: 5-28. **Source:** UNC Sheps, AHA.

### Node 797: Primary Care Practice Closure Rate
- **Scale:** 5 | **Domain:** Healthcare | **Unit:** Closures per 1k practices
- **Baseline:** 8.5/1k (2023). Range: 3.5-18. **Source:** HRSA, surveys.

### Node 798: Mental Health Clinic Closure Rate
- **Scale:** 3 | **Domain:** Mental Health, Healthcare | **Unit:** Closures per 1k clinics
- **Baseline:** 22/1k (2023). Range: 10-52. **Source:** SAMHSA, state.

### Node 799: Substance Use Treatment Program Closure
- **Scale:** 5 | **Domain:** Behavioral Health | **Unit:** Closures per 1k programs
- **Baseline:** 28/1k (2023). Range: 12-65. **Source:** SAMHSA N-SSATS.

### Node 800: Public Transit Route Cancellation Rate
- **Scale:** 2 | **Domain:** Transportation | **Unit:** % routes reduced/eliminated
- **Baseline:** 8.5% (2023). Range: 2.5-22%. **Source:** FTA NTD, transit agencies.

### Node 801: School Closure (Permanent) Rate
- **Scale:** 4 | **Domain:** Education | **Unit:** Closures per 1k schools
- **Baseline:** 12/1k (2023). Range: 4.5-32. **Source:** NCES, state.

### Node 802: Library Closure/Hour Reduction Rate
- **Scale:** 4 | **Domain:** Education, Social | **Unit:** % libraries reducing services
- **Baseline:** 18% (2023). Range: 8-38%. **Source:** IMLS, ALA.

### Node 803: Community Center Closure Rate
- **Scale:** 5 | **Domain:** Social | **Unit:** Closures per 1k centers
- **Baseline:** 22/1k (2023). Range: 8-52. **Source:** Local agencies, surveys.

### Node 804: Faith-Based Org Closure Rate (Community Impact)
- **Scale:** 5 | **Domain:** Social | **Unit:** % congregations closing
- **Baseline:** 2.8% annually (2023). Range: 1.2-6.5%. **Source:** ARDA, surveys.

### Node 805: Nonprofit Dissolution Rate (Health/Human Services)
- **Scale:** 3 | **Domain:** Social | **Unit:** Dissolutions per 1k nonprofits
- **Baseline:** 28/1k (2023). Range: 15-55. **Source:** IRS, NCCS.

### Node 806: Social Safety Net Gap (Unmet Need)
- **Scale:** 3 | **Domain:** Social, Economic | **Unit:** % eligible not receiving benefits
- **Baseline:** 42% (2023). Range: 28-68%. **Source:** HHS, research, state.

### Node 807: Crisis Hotline Unanswered Call Rate
- **Scale:** 3 | **Domain:** Mental Health, Social | **Unit:** % calls not answered
- **Baseline:** 18% (2023). Range: 8-42%. **Source:** 988, Lifeline, crisis lines.

### Node 808: Emergency Shelter Capacity Shortage
- **Scale:** 3 | **Domain:** Housing, Social | **Unit:** % turned away due to capacity
- **Baseline:** 32% (2023). Range: 18-65%. **Source:** HUD, CoC, providers.

### Node 809: Food Bank Capacity Shortage Days
- **Scale:** 3 | **Domain:** Food, Social | **Unit:** Days unable to meet demand
- **Baseline:** 22 days (2023). Range: 5-95. **Source:** Feeding America.

### Node 810: Blood Bank Critical Shortage Days
- **Scale:** 6 | **Domain:** Healthcare | **Unit:** Days <1 day supply
- **Baseline:** 8 days (2023). Range: 2-32. **Source:** Red Cross, AABB.

### Node 811: Organ Donation Waiting List Growth
- **Scale:** 6 | **Domain:** Healthcare | **Unit:** % annual increase waiting
- **Baseline:** 3.5% (2023). Range: 1-8%. **Source:** UNOS OPTN.

### Node 812: Vaccine Shortage Impact
- **Scale:** 6 | **Domain:** Healthcare, Prevention | **Unit:** Days with critical shortage
- **Baseline:** 12 days (2023). Range: 0-85. **Source:** CDC, FDA.

### Node 813: Insulin Affordability Crisis (Rationing)
- **Scale:** 6 | **Domain:** Healthcare, Economic | **Unit:** % diabetics rationing insulin
- **Baseline:** 18% (2023). Range: 10-32%. **Source:** Surveys, ADA.

### Node 814: Prescription Drug Affordability Crisis
- **Scale:** 3 | **Domain:** Healthcare, Economic | **Unit:** % not filling due to cost
- **Baseline:** 22% chronic disease (2023). Range: 12-42%. **Source:** KFF, surveys.

### Node 815: Medical Bankruptcy Rate
- **Scale:** 3 | **Domain:** Economic, Healthcare | **Unit:** % bankruptcies medical-related
- **Baseline:** 58% (2023). Range: 42-72%. **Source:** Courts, research.

### Node 816: Maternal Healthcare Desert (County-Level)
- **Scale:** 3 | **Domain:** Maternal, Healthcare | **Unit:** % counties no OB services
- **Baseline:** 32% counties (2023). Range: 15-55%. **Source:** March of Dimes.

### Node 817: Mental Health Provider Shortage (Severe)
- **Scale:** 3 | **Domain:** Mental Health, Healthcare | **Unit:** % population in HPSA
- **Baseline:** 45% (2023). Range: 28-72%. **Source:** HRSA HPSA.

### Node 818: Primary Care Shortage (Severe)
- **Scale:** 6 | **Domain:** Healthcare | **Unit:** % population in HPSA
- **Baseline:** 38% (2023). Range: 22-68%. **Source:** HRSA HPSA.

### Node 819: Dental Care Shortage (Severe)
- **Scale:** 6 | **Domain:** Healthcare | **Unit:** % population in HPSA
- **Baseline:** 42% (2023). Range: 28-72%. **Source:** HRSA HPSA.

### Node 820: Disability Services Waitlist (Years)
- **Scale:** 3 | **Domain:** Disability, LTSS | **Unit:** Median years on waitlist
- **Baseline:** 3.2 years (2023). Range: 0.5-12. **Source:** State Medicaid, KFF.

### Node 821: Affordable Housing Waitlist (Years)
- **Scale:** 3 | **Domain:** Housing, Economic | **Unit:** Median years on waitlist
- **Baseline:** 2.8 years (2023). Range: 0.5-8.5. **Source:** HUD, PHAs.

### Node 822: Childcare Waitlist (Months)
- **Scale:** 3 | **Domain:** Child, Economic | **Unit:** Median months waiting
- **Baseline:** 8.5 months (2023). Range: 2-24. **Source:** State agencies, surveys.

### Node 823: Mental Health Treatment Waitlist (Weeks)
- **Scale:** 3 | **Domain:** Mental Health | **Unit:** Median weeks to first appointment
- **Baseline:** 6.5 weeks (2023). Range: 2-22. **Source:** Surveys, providers.

### Node 824: Specialty Care Waitlist (Weeks)
- **Scale:** 3 | **Domain:** Healthcare | **Unit:** Median weeks to specialist
- **Baseline:** 4.5 weeks (2023). Range: 1.5-18. **Source:** Surveys, Merritt Hawkins.

### Node 825: SUD Treatment Capacity Shortage
- **Scale:** 3 | **Domain:** Behavioral Health | **Unit:** % needing but unable to access
- **Baseline:** 82% (2023). Range: 68-92%. **Source:** NSDUH, SAMHSA.

### Node 826: Crisis Stabilization Bed Shortage
- **Scale:** 3 | **Domain:** Mental Health, Healthcare | **Unit:** % needing bed but unavailable
- **Baseline:** 65% (2023). Range: 42-88%. **Source:** State systems, SAMHSA.

### Node 827: Detox Bed Shortage
- **Scale:** 3 | **Domain:** Behavioral Health | **Unit:** % needing but unable to access
- **Baseline:** 72% (2023). Range: 52-92%. **Source:** State systems, SAMHSA.

### Node 828: Respite Care Unavailability (Caregivers)
- **Scale:** 2 | **Domain:** LTSS, Social | **Unit:** % caregivers needing but unable
- **Baseline:** 68% (2023). Range: 48-85%. **Source:** Surveys, AARP.

### Node 829: Home Health Aide Shortage (Unmet Hours)
- **Scale:** 2 | **Domain:** LTSS, Healthcare | **Unit:** % needed hours unfilled
- **Baseline:** 42% (2023). Range: 28-72%. **Source:** State Medicaid, PHI.

### Node 830: Interpreter Service Unavailability (Critical)
- **Scale:** 2 | **Domain:** Healthcare, Social | **Unit:** % critical needs unmet
- **Baseline:** 28% (2023). Range: 15-55%. **Source:** Hospitals, OCR.

### Node 831: Accessible Transportation Denial Rate
- **Scale:** 2 | **Domain:** Disability, Transportation | **Unit:** % paratransit requests denied
- **Baseline:** 12% (2023). Range: 4-32%. **Source:** FTA, disability advocates.

### Node 832: Disability Benefit Application Denial Rate
- **Scale:** 6 | **Domain:** Disability, Economic | **Unit:** % SSDI/SSI denied initially
- **Baseline:** 65% (2023). Range: 52-78%. **Source:** SSA.

### Node 833: Unemployment Benefits Denial Rate
- **Scale:** 6 | **Domain:** Employment, Economic | **Unit:** % claims denied
- **Baseline:** 22% (2023). Range: 12-42%. **Source:** DOL, state.

### Node 834: Workers' Compensation Denial Rate
- **Scale:** 4 | **Domain:** Occupational, Economic | **Unit:** % claims denied
- **Baseline:** 38% (2023). Range: 22-62%. **Source:** State agencies, NASI.

### Node 835: Family Leave Request Denial Rate
- **Scale:** 4 | **Domain:** Employment, Social | **Unit:** % FMLA requests denied
- **Baseline:** 18% (2023). Range: 8-38%. **Source:** DOL, surveys.

### Node 836: School Meal Debt Crisis (Students Affected)
- **Scale:** 3 | **Domain:** Food, Education, Child | **Unit:** % students with meal debt
- **Baseline:** 12% (2023). Range: 4-28%. **Source:** School Nutrition Assn.

### Node 837: Student Lunch Shaming Incidents
- **Scale:** 4 | **Domain:** Food, Education, Child | **Unit:** Incidents per 1k students
- **Baseline:** 4.5/1k (2023). Range: 1-15. **Source:** Advocacy, surveys.

### Node 838: Energy Insecurity (Inability to Heat/Cool)
- **Scale:** 4 | **Domain:** Housing, Economic, Climate | **Unit:** % HH unable to maintain temp
- **Baseline:** 18% (2023). Range: 8-38%. **Source:** EIA RECS, Household Pulse.

### Node 839: Internet Disconnection Due to Cost
- **Scale:** 4 | **Domain:** Digital, Economic | **Unit:** % HH losing internet—cost
- **Baseline:** 12% (2023). Range: 5-28%. **Source:** Surveys, FCC.

### Node 840: Phone Disconnection Due to Cost
- **Scale:** 4 | **Domain:** Digital, Economic | **Unit:** % HH losing phone—cost
- **Baseline:** 8.5% (2023). Range: 3-22%. **Source:** Surveys, FCC.

### Node 841: Broadband Affordability Crisis
- **Scale:** 4 | **Domain:** Digital, Economic | **Unit:** % unable to afford broadband
- **Baseline:** 22% (2023). Range: 10-45%. **Source:** FCC, surveys.

### Node 842: Digital Literacy Barrier (Critical)
- **Scale:** 6 | **Domain:** Digital, Education | **Unit:** % unable to complete essential online tasks
- **Baseline:** 18% adults (2023). Range: 8-38%. **Source:** PIAAC, surveys.

### Node 843: Telehealth Inability Due to Digital Access
- **Scale:** 2 | **Domain:** Healthcare, Digital | **Unit:** % unable to access telehealth
- **Baseline:** 22% (2023). Range: 10-45%. **Source:** Surveys, FCC.

### Node 844: Banking Desert (No Physical Bank Access)
- **Scale:** 2 | **Domain:** Economic | **Unit:** % population in banking desert
- **Baseline:** 8.5% (2023). Range: 2-25%. **Source:** FDIC, NCRC.

### Node 845: Pharmacy Desert
- **Scale:** 2 | **Domain:** Healthcare | **Unit:** % population >5mi from pharmacy
- **Baseline:** 4.5% (2023). Range: 1-18%. **Source:** NCPDP, research.

### Node 846: Grocery Store Desert (Food Desert)
- **Scale:** 2 | **Domain:** Food | **Unit:** % population in food desert
- **Baseline:** 12.8% (2023). Range: 4-35%. **Source:** USDA ERS.

### Node 847: Healthcare Desert (No Primary Care)
- **Scale:** 3 | **Domain:** Healthcare | **Unit:** % population >30min from PCP
- **Baseline:** 18% rural (2023). Range: 5-52%. **Source:** HRSA, research.

### Node 848: Hospital Desert (No Hospital Access)
- **Scale:** 3 | **Domain:** Healthcare | **Unit:** % population >60min from hospital
- **Baseline:** 8.5% (2023). Range: 2-32%. **Source:** AHA, research.

### Node 849: Mental Health Desert (No Provider Access)
- **Scale:** 3 | **Domain:** Mental Health | **Unit:** % population no provider within 60min
- **Baseline:** 28% (2023). Range: 10-65%. **Source:** HRSA, SAMHSA.

### Node 850: Broadband Desert (No Access)
- **Scale:** 4 | **Domain:** Digital | **Unit:** % without broadband access
- **Baseline:** 12% (2023). Range: 3-42%. **Source:** FCC, county.

---

**END SCALE 5: Nodes 551-850 (300 nodes total). Crisis Endpoints complete.**

**FINAL INVENTORY COMPLETE: 850 NODES ACROSS 5 SCALES**

---

# INVENTORY SUMMARY

**Total Nodes: 850**

- **Scale 1 (Structural Determinants):** 130 nodes
  - Policy infrastructure: 80 nodes
  - Macro structural conditions: 50 nodes

- **Scale 2 (Institutional Infrastructure):** 50 nodes
  - Healthcare, housing, social services, education, built environment, criminal justice, public health, workplace, organizational quality

- **Scale 3 (Individual/Household Conditions):** 220 nodes
  - Economic security, housing, healthcare access, food, transportation, employment, environmental exposures, social environment, education, stress/trauma, digital access, criminal justice contact, health status, maternal/child health, climate exposures, additional economic/social conditions

- **Scale 4 (Intermediate Pathways):** 150 nodes
  - Healthcare utilization, chronic disease management, maternal/child pathways, behavioral health treatment, biological risk factors, health behaviors, housing/environmental pathways, occupational exposures, social support, environmental processes, food/nutrition, justice pathways, education/development, economic processes, climate adaptation

- **Scale 5 (Crisis Endpoints):** 300 nodes
  - Mortality, birth outcomes, chronic disease crises, mental health/SUD crises, infectious disease, injury/violence, housing/economic crises, criminal justice crises, educational crises, healthcare system failures, environmental/climate crises, additional health crises, disability/functional decline, system failure indicators, deserts/access crises

**Version 1.0 - Complete Node Inventory - January 2024**