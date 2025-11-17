# Critical Missing Nodes for Complete American Health System Mapping

## Executive Summary

The existing 592-node inventory provides strong coverage of **structural determinants → crisis endpoints** but has significant gaps in:
1. **Healthcare system operations and infrastructure** (thin coverage)
2. **Clinical care processes and quality** (minimal)
3. **Iatrogenic harms and medical errors** (absent)
4. **Specialized clinical domains** (fragmentary)
5. **Social services infrastructure detail** (conceptual only)
6. **Workplace and occupational health** (minimal)
7. **Public health infrastructure** (absent)
8. **Health system financing mechanisms** (surface level)

**Recommended additions:** ~300-400 nodes to achieve comprehensive mapping

---

## DOMAIN 1: HEALTHCARE SYSTEM STRUCTURE & OPERATIONS (67 missing nodes)

### Hospital System Infrastructure

**Currently Missing:**

#### 601. **Hospital Consolidation & Market Concentration**
- Type: Structural
- Unit: HHI (Herfindahl-Hirschman Index) 0-10,000
- Why Critical: Determines pricing power, care availability, competition
- Baseline: ~3,200 (highly concentrated in most markets)
- Connects to: Healthcare costs, access, quality variation

#### 602. **Hospital Ownership Type (For-Profit Share)**
- Type: Proportion
- Unit: 0-1 (% for-profit vs. nonprofit vs. public)
- Why Critical: Affects community benefit, charity care, pricing
- Baseline: 0.24 for-profit, 0.58 nonprofit, 0.18 public
- Connects to: Medical debt, community health investment

#### 603. **Academic Medical Center Presence**
- Type: Binary/Density
- Unit: 0-1 or AMCs per metro area
- Why Critical: Teaching hospitals provide tertiary care, safety net
- Connects to: Complex care access, research participation

#### 604. **Critical Access Hospital Status**
- Type: Count/Proportion
- Unit: CAHs per rural population
- Why Critical: Rural hospital closures → access crises
- Baseline: ~1,350 CAHs nationally, declining
- Connects to: Rural healthcare access, transfer delays

#### 605. **Hospital Closure Events**
- Type: Flow rate
- Unit: Closures per year, especially rural
- Why Critical: Creates healthcare deserts
- Connects to: Emergency care access, maternal mortality (rural)

#### 606. **Emergency Department Crowding Index**
- Type: Real-time operational metric
- Unit: Boarding hours, left-without-being-seen %
- Why Critical: Determines ED quality, patient safety
- Baseline: 30% of EDs report consistent crowding
- Connects to: Medical errors, adverse events, patient experience

#### 607. **Hospital Bed Occupancy Rate**
- Type: Proportion
- Unit: 0-1 (% beds occupied)
- Why Critical: >85% = quality degradation, strain
- Baseline: Avg 64%, but surges to >100% during crises
- Connects to: Hospital-acquired infections, staff burnout

#### 608. **ICU Capacity & Availability**
- Type: Real (rate + utilization)
- Unit: ICU beds per 100k + occupancy %
- Why Critical: Pandemic/surge response, critical care access
- Baseline: ~35 ICU beds/100k, highly variable
- Connects to: Crisis mortality, transfer delays

#### 609. **Ambulance Transport Time (EMS Response)**
- Type: Real (minutes)
- Unit: Mean response time + transport time
- Why Critical: Time-sensitive emergencies (stroke, MI, trauma)
- Baseline: Urban 7-9 min, rural 14-18 min
- Connects to: Stroke outcomes, MI survival, trauma mortality

#### 610. **Trauma Center Designation & Distribution**
- Type: Categorical (Level I-V) + density
- Unit: Trauma centers per 100k, geographic coverage
- Why Critical: Determines trauma survival
- Baseline: Major gaps in rural areas, some urban deserts
- Connects to: Injury mortality, helicopter transfer needs

### Provider Workforce

#### 611. **Physician Burnout Rate**
- Type: Proportion
- Unit: 0-1 (% reporting burnout symptoms)
- Why Critical: Affects quality, errors, retention, patient safety
- Baseline: 0.42-0.63 depending on specialty
- Connects to: Medical errors, care quality, workforce shortage

#### 612. **Nursing Shortage Severity**
- Type: Real (vacancy rate)
- Unit: Nursing vacancies per 100 positions
- Why Critical: Nurse-patient ratios determine outcomes
- Baseline: 17% vacancy rate nationally (2024)
- Connects to: Hospital-acquired infections, mortality, burnout

#### 613. **Nurse-to-Patient Ratio**
- Type: Real (ratio)
- Unit: Patients per RN
- Why Critical: Each additional patient → 7% higher mortality risk
- Baseline: Varies 4:1 to 8:1+, worsening
- Connects to: Hospital mortality, infections, falls

#### 614. **Advanced Practice Provider Scope of Practice**
- Type: Policy index
- Unit: 0-10 (restricted to full practice authority)
- Why Critical: Affects primary care access, especially rural
- Baseline: Only 26 states allow full NP practice
- Connects to: Primary care access, wait times

#### 615. **International Medical Graduate Workforce Share**
- Type: Proportion
- Unit: 0-1 (% physicians who are IMGs)
- Why Critical: Fills shortage areas, but visa restrictions create instability
- Baseline: 0.25 of physicians, higher in underserved areas
- Connects to: Primary care access, workforce diversity

#### 616. **Physician Maldistribution (Geographic)**
- Type: Variation metric
- Unit: Gini coefficient or ratio (highest:lowest)
- Why Critical: Concentration in affluent areas
- Connects to: Health equity, rural access

#### 617. **Community Health Worker Professionalization**
- Type: Policy index
- Unit: 0-10 (certification, reimbursement, career pathway)
- Why Critical: CHW effectiveness depends on integration
- Baseline: Only ~12 states have certification/reimbursement
- Connects to: CHW capacity effectiveness

#### 618. **Behavioral Health Workforce Shortage Severity**
- Type: Real (ratio to need)
- Unit: Providers per 100k vs. demand
- Why Critical: Severe shortage nationally
- Baseline: ~60% of counties have no psychiatrist
- Connects to: Mental health treatment access, crisis response

### Insurance System Infrastructure

#### 619. **Insurance Market Competition (Exchange)**
- Type: Real (count)
- Unit: Insurers participating per market
- Why Critical: Competition affects pricing, choice
- Baseline: ~50% of counties have ≤2 insurers
- Connects to: Premium affordability, network adequacy

#### 620. **Network Adequacy (Provider Panel Size)**
- Type: Real (ratio)
- Unit: In-network providers per 1,000 covered lives
- Why Critical: Narrow networks → access barriers despite coverage
- Connects to: Effective access, surprise billing

#### 621. **Prior Authorization Burden**
- Type: Real (rate + time)
- Unit: % services requiring PA, approval time
- Why Critical: Delays care, increases administrative costs
- Baseline: ~30% of services require PA, 2-14 day delays
- Connects to: Treatment delays, medication non-adherence

#### 622. **Insurance Claim Denial Rate**
- Type: Proportion
- Unit: 0-1 (% claims initially denied)
- Why Critical: Financial barriers, care delays
- Baseline: 15-20% initial denial rate
- Connects to: Medical debt, delayed care

#### 623. **Balance Billing / Surprise Billing Exposure**
- Type: Real (rate)
- Unit: % insured experiencing surprise bills
- Why Critical: Financial toxicity despite coverage
- Baseline: ~18% insured receive surprise bill annually
- Connects to: Medical debt, bankruptcy

#### 624. **Pharmacy Benefit Manager (PBM) Market Concentration**
- Type: Structural (market share)
- Unit: Top 3 PBM market share
- Why Critical: PBMs control drug access, pricing, pharmacy networks
- Baseline: Top 3 PBMs control ~80% of market
- Connects to: Prescription affordability, pharmacy access

#### 625. **Health Savings Account (HSA) Utilization**
- Type: Real (rate)
- Unit: % with high-deductible plans + HSA funding
- Why Critical: Tax-advantaged savings, but requires wealth
- Baseline: ~50% with HDHP, but only wealthy fund HSAs
- Connects to: Underinsured rate, deferred care

### Health Information Technology

#### 626. **Electronic Health Record (EHR) Interoperability**
- Type: Index
- Unit: 0-1 (data exchange capability)
- Why Critical: Determines care coordination, reduces duplicative testing
- Baseline: 0.40 (limited interoperability despite EHR adoption)
- Connects to: Care coordination, medical errors, costs

#### 627. **Health Information Exchange (HIE) Participation**
- Type: Proportion
- Unit: 0-1 (% providers participating in HIE)
- Why Critical: Enables cross-system coordination
- Baseline: 0.55 participation, variable use
- Connects to: Care continuity, ED utilization

#### 628. **Patient Portal Adoption & Use**
- Type: Proportion
- Unit: 0-1 (% patients with access + % active users)
- Why Critical: Patient engagement, self-management
- Baseline: 0.70 access, 0.30 active use
- Connects to: Medication adherence, chronic disease control

#### 629. **Telemedicine Infrastructure & Reimbursement**
- Type: Policy + capacity index
- Unit: 0-10 (broadband + equipment + payment parity)
- Why Critical: Access expansion, especially rural/disabled
- Baseline: Expanded during pandemic, now retrenching
- Connects to: Healthcare access (rural, mobility-limited)

#### 630. **Clinical Decision Support System (CDSS) Penetration**
- Type: Proportion
- Unit: 0-1 (% providers with effective CDSS)
- Why Critical: Reduces diagnostic errors, improves guideline adherence
- Baseline: 0.45 have some CDSS, effectiveness varies
- Connects to: Diagnostic accuracy, preventive care delivery

#### 631. **Health IT Usability & Alert Fatigue**
- Type: Index (inverse problem)
- Unit: Alerts per patient encounter, override rate
- Why Critical: Alert fatigue → ignored warnings → errors
- Baseline: 49-96% of drug alerts overridden
- Connects to: Medical errors, adverse drug events, burnout

### Quality Measurement & Accountability

#### 632. **Hospital Quality Reporting Participation**
- Type: Proportion
- Unit: 0-1 (% hospitals reporting to CMS)
- Why Critical: Public reporting drives improvement
- Baseline: >99% for Medicare-participating hospitals
- Connects to: Hospital quality variation, patient choice

#### 633. **Patient Safety Indicator (PSI) Events**
- Type: Real (rate)
- Unit: PSI events per 1,000 discharges
- Why Critical: Tracks preventable hospital harms
- Baseline: Varies by PSI, 3-15 per 1,000
- Connects to: Hospital-acquired conditions, mortality

#### 634. **Healthcare-Associated Infection (HAI) Rates**
- Type: Real (rate by type)
- Unit: CLABSI, CAUTI, SSI, C.diff per 1,000 patient-days
- Why Critical: Preventable iatrogenic harm
- Baseline: Variable by hospital, significant room for improvement
- Connects to: Sepsis, mortality, extended LOS

#### 635. **Diagnostic Error Rate**
- Type: Proportion
- Unit: 0-1 (% encounters with diagnostic error)
- Why Critical: Leading cause of malpractice, patient harm
- Baseline: Estimated 5-15% of diagnoses have errors
- Connects to: Delayed treatment, adverse outcomes, malpractice

#### 636. **Medication Error Rate**
- Type: Real (rate)
- Unit: Errors per 1,000 medication administrations
- Why Critical: Preventable adverse drug events
- Baseline: ~5 errors per 1,000, higher in certain settings
- Connects to: Adverse drug events, hospital complications

#### 637. **Surgical Site Infection Rate**
- Type: Real (rate)
- Unit: SSI per 100 surgical procedures (by type)
- Why Critical: Preventable postoperative complication
- Baseline: 0.5-3% depending on procedure
- Connects to: Reoperation, sepsis, mortality

#### 638. **Hospital Readmission Rate (All-Cause 30-Day)**
- Type: Proportion
- Unit: 0-1 (% readmitted within 30 days)
- Why Critical: Quality indicator, patient safety, costs
- Baseline: 0.14 (14%), higher for certain conditions
- **Note:** Exists in crisis endpoints but needs institutional-level node

#### 639. **Patient Experience Scores (HCAHPS)**
- Type: Index
- Unit: 0-10 scale (composite)
- Why Critical: Patient-centered care quality, satisfaction
- Baseline: National mean ~7.2
- Connects to: Patient engagement, adherence, trust

### Medical Training & Workforce Pipeline

#### 640. **Medical School Capacity & Slots**
- Type: Real (count)
- Unit: Medical school enrollments per year
- Why Critical: Pipeline for future physician workforce
- Baseline: ~22,000 MD/year, ~8,000 DO/year
- Connects to: Future physician supply, specialty mix

#### 641. **Residency Slot Availability**
- Type: Real (count + match rate)
- Unit: Residency positions vs. graduates
- Why Critical: Bottleneck in physician training
- Baseline: GME caps limit supply, unmatched graduates
- Connects to: Physician shortage, specialty distribution

#### 642. **Primary Care vs. Specialty Residency Ratio**
- Type: Ratio
- Unit: PC residency slots / specialty slots
- Why Critical: Determines future specialty balance
- Baseline: Skewed toward specialties, PC shortage worsening
- Connects to: Primary care access, cost inflation

#### 643. **Nursing School Capacity Constraints**
- Type: Real (rejection rate)
- Unit: Qualified applicants rejected due to capacity
- Why Critical: Artificial constraint on nurse supply
- Baseline: ~90,000 qualified applicants rejected annually
- Connects to: Nursing shortage, faculty shortage

#### 644. **Faculty Shortage (Nursing & Medical)**
- Type: Real (vacancy rate)
- Unit: % faculty positions unfilled
- Why Critical: Limits training capacity
- Connects to: Workforce pipeline bottleneck

#### 645. **Diversity in Health Professions Workforce**
- Type: Proportion
- Unit: 0-1 (% URM in physician, nursing workforce)
- Why Critical: Concordant care improves outcomes, equity
- Baseline: Physicians 5% Black, 6% Hispanic vs. 13%, 19% population
- Connects to: Cultural competency, health equity

#### 646. **Loan Debt Burden (Medical/Nursing Students)**
- Type: Real (dollars)
- Unit: Median debt at graduation
- Why Critical: Influences specialty choice, practice location
- Baseline: Median MD debt ~$200k, nurses ~$40-80k
- Connects to: Primary care shortage, rural physician shortage

#### 647. **Loan Repayment Program Effectiveness (NHSC, etc.)**
- Type: Real (participants + retention)
- Unit: Providers placed in underserved areas, retention post-commitment
- Why Critical: Addresses geographic maldistribution
- Baseline: ~10,000 NHSC clinicians, variable retention
- Connects to: Rural/underserved access

### Healthcare Consolidation & Market Dynamics

#### 648. **Vertical Integration (Payer-Provider)**
- Type: Real (market share)
- Unit: % care delivered by insurer-owned providers
- Why Critical: Changes incentives, competition, costs
- Baseline: Rapidly growing (UnitedHealth owns Optum, etc.)
- Connects to: Network adequacy, competition, costs

#### 649. **Private Equity Ownership in Healthcare**
- Type: Real (proportion)
- Unit: % of practices/hospitals PE-owned
- Why Critical: Profit extraction, staffing cuts, quality concerns
- Baseline: Rapidly growing, especially ER, anesthesia, dermatology
- Connects to: Surprise billing, quality variation, closures

#### 650. **Hospital-Physician Employment Rate**
- Type: Proportion
- Unit: 0-1 (% physicians employed vs. independent)
- Why Critical: Changes practice patterns, consolidation
- Baseline: ~0.70 employed (growing from 0.25 in 2000)
- Connects to: Physician autonomy, practice patterns

#### 651. **Certificate of Need (CON) Laws**
- Type: Policy (binary by state)
- Unit: 0-1 (CON required for new facilities/services)
- Why Critical: Limits competition, affects access
- Baseline: 35 states have CON laws
- Connects to: Hospital market concentration, access

### Pharmaceutical System Infrastructure

#### 652. **Drug Pricing Index (Inflation-Adjusted)**
- Type: Real (index)
- Unit: Index vs. CPI
- Why Critical: Drug costs major driver of healthcare costs
- Baseline: Outpaces inflation 2-3x annually
- Connects to: Medication affordability, non-adherence

#### 653. **Pharmacy Desert Prevalence**
- Type: Real (rate)
- Unit: % population >1 mile from pharmacy
- Why Critical: Medication access barrier
- Baseline: 10-15% in rural, 2-5% urban
- Connects to: Medication adherence, chronic disease control

#### 654. **340B Program Hospital Participation**
- Type: Proportion
- Unit: 0-1 (% hospitals enrolled in 340B)
- Why Critical: Discounted drugs for safety net, but misuse concerns
- Baseline: ~40% of hospitals, growing
- Connects to: Charity care, hospital revenue

#### 655. **Drug Shortage Events**
- Type: Real (count)
- Unit: Number of critical drug shortages active
- Why Critical: Affects treatment availability, quality
- Baseline: 100-200 active shortages at any time
- Connects to: Treatment delays, suboptimal alternatives

#### 656. **Generic Drug Substitution Rate**
- Type: Proportion
- Unit: 0-1 (% prescriptions filled generic vs. brand)
- Why Critical: Cost savings, access
- Baseline: ~0.90 (90% generic)
- Connects to: Prescription affordability

#### 657. **Direct-to-Consumer Pharmaceutical Advertising Spending**
- Type: Real (dollars)
- Unit: $ billions per year
- Why Critical: Drives demand, inappropriate prescribing
- Baseline: ~$6 billion/year (US one of only 2 countries allowing)
- Connects to: Overprescribing, costs, patient demands

### Regulatory & Oversight Infrastructure

#### 658. **State Health Department Capacity**
- Type: Index
- Unit: 0-10 (funding, staffing, capabilities)
- Why Critical: Public health infrastructure backbone
- Baseline: Highly variable by state, chronically underfunded
- Connects to: Disease surveillance, outbreak response

#### 659. **Health Facility Licensing & Inspection Frequency**
- Type: Real (rate)
- Unit: Inspections per year per facility
- Why Critical: Quality oversight, deficiency identification
- Baseline: Variable by state, many overdue
- Connects to: Nursing home quality, hospital safety

#### 660. **Medical Board Disciplinary Actions**
- Type: Real (rate)
- Unit: Actions per 1,000 physicians per year
- Why Critical: Physician quality, patient safety oversight
- Baseline: ~3-7 per 1,000 physicians annually
- Connects to: Medical errors, malpractice, impaired physicians

#### 661. **Certificate of Medical Necessity (CMN) Burden**
- Type: Real (proportion)
- Unit: % DME/services requiring CMN
- Why Critical: Administrative burden, access delays
- Connects to: Treatment delays, administrative costs

#### 662. **Prior Authorization for Medication (Step Therapy)**
- Type: Proportion
- Unit: % drug classes with step therapy requirements
- Why Critical: Delays optimal treatment
- Baseline: Affecting ~60% of specialty drugs
- Connects to: Treatment delays, disease progression

### Malpractice & Liability System

#### 663. **Medical Malpractice Insurance Premiums**
- Type: Real (dollars)
- Unit: Mean premium by specialty
- Why Critical: Affects practice location, defensive medicine
- Baseline: $7,500-$200,000/year depending on specialty
- Connects to: Physician location decisions, defensive medicine

#### 664. **Malpractice Climate (Claims Rate)**
- Type: Real (rate)
- Unit: Claims per 100 physician-years
- Why Critical: Defensive medicine, practice patterns
- Baseline: ~7-10 per 100 physician-years
- Connects to: Defensive medicine costs, imaging overuse

#### 665. **Tort Reform Presence (Damage Caps)**
- Type: Policy (binary + cap level)
- Unit: 0-1 (caps present) + dollar cap
- Why Critical: Affects malpractice environment, physician supply
- Baseline: ~30 states have some form of caps
- Connects to: Malpractice premiums, physician supply

### Payment & Reimbursement Mechanisms

#### 666. **Fee-for-Service vs. Value-Based Payment Mix**
- Type: Proportion
- Unit: 0-1 (% revenue from VBP arrangements)
- Why Critical: Payment model shapes care delivery
- Baseline: ~39% of payments in VBP arrangements (2024)
- Connects to: Care quality, preventive services, costs

#### 667. **Medicare Physician Fee Schedule (MPFS) Payment Rates**
- Type: Real (index)
- Unit: Payment rate vs. practice costs
- Why Critical: Determines Medicare participation
- Baseline: Declining in real terms, primary care especially
- Connects to: Medicare acceptance, access for seniors

---

## DOMAIN 2: CLINICAL CARE PROCESSES & QUALITY (58 missing nodes)

### Diagnosis & Screening

#### 668. **Cancer Screening Rates (by type)**
- Type: Proportion
- Unit: 0-1 (% eligible receiving recommended screening)
- Why Critical: Early detection dramatically improves outcomes
- Baseline: Colorectal 0.69, Breast 0.79, Cervical 0.81, Lung 0.16
- Connects to: Cancer stage at diagnosis, mortality

#### 669. **Diagnostic Imaging Utilization Rate**
- Type: Real (rate)
- Unit: Scans per 1,000 population
- Why Critical: Overuse → costs, radiation; underuse → missed diagnoses
- Baseline: Highly variable by region, defensive medicine
- Connects to: Diagnostic accuracy, costs, incidental findings

#### 670. **Incidental Finding Follow-Up Rate**
- Type: Proportion
- Unit: 0-1 (% incidental findings with appropriate follow-up)
- Why Critical: Can detect early disease or cause anxiety/overtreatment
- Connects to: Cancer detection, overtreatment cascade

#### 671. **Time to Diagnosis (by condition)**
- Type: Real (days)
- Unit: Days from symptom presentation to diagnosis
- Why Critical: Delays worsen outcomes, especially cancer, stroke, MI
- Baseline: Variable, longer for complex/rare conditions
- Connects to: Disease stage, treatment effectiveness

#### 672. **Misdiagnosis Rate (by condition)**
- Type: Proportion
- Unit: 0-1 (% initially misdiagnosed)
- Why Critical: Delays treatment, wrong treatment, patient harm
- Baseline: 10-15% estimated, higher for certain conditions
- Connects to: Adverse outcomes, delayed treatment

#### 673. **Diagnostic Test Turnaround Time**
- Type: Real (hours/days)
- Unit: Time from order to result availability
- Why Critical: Delays treatment initiation
- Connects to: Length of stay, treatment delays

### Treatment & Medication Management

#### 674. **Guideline-Concordant Care Rate**
- Type: Proportion
- Unit: 0-1 (% care following evidence-based guidelines)
- Why Critical: Guidelines represent best evidence
- Baseline: 50-80% depending on condition
- Connects to: Treatment effectiveness, outcomes

#### 675. **Polypharmacy Prevalence**
- Type: Proportion
- Unit: 0-1 (% on ≥5 medications)
- Why Critical: Drug interactions, non-adherence, adverse events
- Baseline: 0.40 of seniors, growing
- Connects to: Adverse drug events, falls, hospitalizations

#### 676. **Medication Reconciliation Accuracy**
- Type: Proportion
- Unit: 0-1 (% transitions with accurate med rec)
- Why Critical: Prevents medication errors at transitions
- Baseline: 50-60% accuracy at discharge
- Connects to: Medication errors, readmissions

#### 677. **Antibiotic Stewardship Program Effectiveness**
- Type: Index
- Unit: 0-10 (program presence + outcomes)
- Why Critical: Reduces antibiotic resistance, C.diff
- Baseline: Variable implementation and effectiveness
- Connects to: Antibiotic-resistant infections, C.diff colitis

#### 678. **Opioid Prescribing Appropriateness**
- Type: Index
- Unit: 0-10 (CDC guideline concordance)
- Why Critical: Prevents iatrogenic opioid use disorder
- Baseline: Improving but still problematic
- Connects to: Opioid use disorder, overdose

#### 679. **Pain Management Adequacy (Non-Opioid)**
- Type: Index
- Unit: 0-10 (multimodal pain management use)
- Why Critical: Balancing pain control with opioid risk
- Connects to: Chronic pain, opioid dependence

#### 680. **Treatment Abandonment Rate**
- Type: Proportion
- Unit: 0-1 (% starting but not completing treatment)
- Why Critical: Indicates barriers, determines outcomes
- Baseline: 20-40% for some conditions (e.g., HCV)
- Connects to: Disease progression, treatment failure

### Care Coordination & Transitions

#### 681. **Care Coordination Index**
- Type: Index
- Unit: 0-10 (composite of coordination processes)
- Why Critical: Fragmentation is major quality problem
- Connects to: Duplicative care, medical errors, patient experience

#### 682. **Hospital Discharge Planning Quality**
- Type: Index
- Unit: 0-10 (completeness, patient understanding)
- Why Critical: Determines readmission risk
- Baseline: Variable, often inadequate
- Connects to: Readmissions, medication errors

#### 683. **Post-Discharge Follow-Up Rate**
- Type: Proportion
- Unit: 0-1 (% with timely follow-up visit)
- Why Critical: Critical for preventing readmissions
- Baseline: 50-60% within 7 days
- Connects to: Readmissions, adverse events

#### 684. **Specialist Referral Wait Time**
- Type: Real (days)
- Unit: Days from referral to appointment
- Why Critical: Treatment delays, disease progression
- Baseline: 30-60 days typical, longer for some specialists
- Connects to: Treatment delays, outcomes

#### 685. **Specialist Communication Back to PCP Rate**
- Type: Proportion
- Unit: 0-1 (% referrals with specialist note back to PCP)
- Why Critical: Care coordination, prevents duplicative care
- Baseline: <50% in many settings
- Connects to: Coordination failures, duplicative testing

#### 686. **Transitions of Care Communication Quality**
- Type: Index
- Unit: 0-10 (completeness, timeliness)
- Why Critical: Handoff failures cause errors
- Connects to: Medical errors, adverse events

### Preventive Care Delivery

#### 687. **Immunization Rates (Adult)**
- Type: Proportion
- Unit: 0-1 (% receiving recommended vaccines)
- Why Critical: Preventable disease burden
- Baseline: Flu 0.48, Pneumo 0.67, Tdap 0.30, COVID highly variable
- Connects to: Infectious disease burden, hospitalizations

#### 688. **Well-Child Visit Completion Rate**
- Type: Proportion
- Unit: 0-1 (% children receiving recommended well-child visits)
- Why Critical: Early detection, development monitoring
- Baseline: 0.75-0.80
- Connects to: Developmental delays, preventable disease

#### 689. **Adolescent Preventive Visit Rate**
- Type: Proportion
- Unit: 0-1 (% teens with annual preventive visit)
- Why Critical: Critical period for mental health, substance use screening
- Baseline: 0.45
- Connects to: Mental health detection, substance use intervention

#### 690. **Cardiovascular Risk Screening Rate**
- Type: Proportion
- Unit: 0-1 (% eligible with lipid, BP screening)
- Why Critical: Primary prevention of leading cause of death
- Baseline: Variable, gaps in young adults
- Connects to: Preventable MI, stroke

#### 691. **Diabetes Screening Rate (Prediabetes Detection)**
- Type: Proportion
- Unit: 0-1 (% at-risk screened)
- Why Critical: Prediabetes intervention prevents diabetes
- Baseline: Low, many undiagnosed
- Connects to: Diabetes prevention, complications

#### 692. **Depression Screening in Primary Care**
- Type: Proportion
- Unit: 0-1 (% patients screened with PHQ-2/9)
- Why Critical: Detects undiagnosed depression
- Baseline: ~60% of practices screen
- Connects to: Mental health treatment access, outcomes

#### 693. **Substance Use Screening (SBIRT Implementation)**
- Type: Proportion
- Unit: 0-1 (% patients receiving SBIRT)
- Why Critical: Early intervention for substance use
- Baseline: <20% implementation despite guidelines
- Connects to: Substance use disorder prevention, treatment

#### 694. **Social Determinants of Health Screening Rate**
- Type: Proportion
- Unit: 0-1 (% patients screened for SDOH)
- Why Critical: Identifies social needs for intervention
- Baseline: Growing but still <30%
- Connects to: Social service referrals, holistic care

#### 695. **Advance Care Planning Documentation Rate**
- Type: Proportion
- Unit: 0-1 (% patients with documented ACP)
- Why Critical: Ensures end-of-life wishes honored
- Baseline: <30% have documented advance directives
- Connects to: End-of-life care quality, family distress

### Chronic Disease Management

#### 696. **Diabetes Care Quality (Composite Measure)**
- Type: Index
- Unit: 0-10 (HbA1c testing, control, eye exam, foot exam, nephropathy screening)
- Why Critical: Prevents complications
- Baseline: Variable, racial/ethnic disparities
- Connects to: Diabetic complications, amputations, blindness

#### 697. **Hypertension Treatment Intensification**
- Type: Proportion
- Unit: 0-1 (% uncontrolled HTN with treatment change)
- Why Critical: Clinical inertia major problem
- Baseline: <40% intensified when appropriate
- Connects to: Stroke, MI, cardiovascular mortality

#### 698. **COPD Exacerbation Prevention (Pulmonary Rehab Use)**
- Type: Proportion
- Unit: 0-1 (% COPD patients in pulmonary rehab)
- Why Critical: Dramatically reduces hospitalizations
- Baseline: <5% of eligible
- Connects to: COPD hospitalizations, mortality

#### 699. **Heart Failure Medication Optimization**
- Type: Proportion
- Unit: 0-1 (% on guideline-directed medical therapy)
- Why Critical: Mortality benefit with optimal therapy
- Baseline: 50-60% on full GDMT
- Connects to: Heart failure readmissions, mortality

#### 700. **Chronic Kidney Disease Monitoring**
- Type: Proportion
- Unit: 0-1 (% CKD patients with recommended monitoring)
- Why Critical: Prevents progression to ESRD
- Baseline: Undertested, many progress unnecessarily
- Connects to: Dialysis initiation, mortality

#### 701. **Lipid Management in Cardiovascular Disease**
- Type: Proportion
- Unit: 0-1 (% CVD patients on statin at goal)
- Why Critical: Secondary prevention of MI/stroke
- Baseline: ~65% on statin, fewer at goal
- Connects to: Recurrent MI, stroke

### Iatrogenic Harms & Medical Errors

#### 702. **Adverse Drug Events (ADE) Rate**
- Type: Real (rate)
- Unit: ADEs per 1,000 patient-days
- Why Critical: Preventable medication-related harm
- Baseline: ~5-10 per 1,000 patient-days
- Connects to: Hospital LOS, mortality, costs

#### 703. **Catheter-Associated UTI (CAUTI) Rate**
- Type: Real (rate)
- Unit: CAUTIs per 1,000 catheter-days
- Why Critical: Preventable HAI
- Baseline: National benchmark ~1 per 1,000, many exceed
- Connects to: Sepsis, extended LOS

#### 704. **Central Line-Associated Bloodstream Infection (CLABSI) Rate**
- Type: Real (rate)
- Unit: CLABSIs per 1,000 line-days
- Why Critical: Preventable, high mortality HAI
- Baseline: Benchmark ~0.5 per 1,000
- Connects to: Sepsis, mortality

#### 705. **Ventilator-Associated Pneumonia (VAP) Rate**
- Type: Real (rate)
- Unit: VAP per 1,000 ventilator-days
- Why Critical: Preventable ICU complication
- Baseline: ~1-3 per 1,000
- Connects to: ICU mortality, extended LOS

#### 706. **Hospital-Acquired Pressure Ulcer Rate**
- Type: Real (rate)
- Unit: Pressure ulcers per 1,000 patient-days
- Why Critical: Preventable, indicates care quality
- Baseline: 2-5 per 1,000 patient-days
- Connects to: Sepsis, pain, extended LOS

#### 707. **In-Hospital Fall Rate**
- Type: Real (rate)
- Unit: Falls per 1,000 patient-days
- Why Critical: Preventable injury, quality indicator
- Baseline: 3-5 per 1,000 patient-days
- Connects to: Hip fracture, head injury, mortality

#### 708. **Wrong-Site/Wrong-Procedure Surgery Events**
- Type: Real (rate)
- Unit: Events per 100,000 procedures
- Why Critical: Never event, patient safety
- Baseline: Rare but devastating
- Connects to: Patient harm, malpractice

#### 709. **Retained Surgical Item Events**
- Type: Real (rate)
- Unit: Events per 100,000 surgeries
- Why Critical: Never event, preventable
- Baseline: ~1 per 10,000 surgeries
- Connects to: Reoperation, infection, malpractice

#### 710. **Postoperative Sepsis Rate**
- Type: Real (rate)
- Unit: Sepsis per 1,000 surgeries
- Why Critical: Preventable complication
- Connects to: Mortality, extended LOS

#### 711. **Postoperative Respiratory Failure Rate**
- Type: Real (rate)
- Unit: Respiratory failure per 1,000 surgeries
- Why Critical: Serious complication, often preventable
- Connects to: ICU admission, mortality

#### 712. **Postoperative VTE (DVT/PE) Rate**
- Type: Real (rate)
- Unit: VTE per 1,000 surgeries
- Why Critical: Preventable with prophylaxis
- Baseline: Variable by surgery type
- Connects to: PE, mortality

#### 713. **Birth Trauma Rate (Obstetric)**
- Type: Real (rate)
- Unit: Birth injuries per 1,000 deliveries
- Why Critical: Quality of obstetric care indicator
- Connects to: Neonatal morbidity

#### 714. **Cesarean Section Rate (Primary, Low-Risk)**
- Type: Proportion
- Unit: 0-1 (% low-risk deliveries by C-section)
- Why Critical: Overuse indicator, maternal morbidity
- Baseline: 0.26 (26%), higher than recommended 0.10-0.15
- Connects to: Maternal morbidity, costs

#### 715. **Unplanned Extubation Rate**
- Type: Real (rate)
- Unit: Events per 1,000 ventilator-days
- Why Critical: Dangerous ICU adverse event
- Connects to: Respiratory distress, reintubation

#### 716. **Contrast-Induced Nephropathy Rate**
- Type: Real (rate)
- Unit: Events per 1,000 contrast exposures
- Why Critical: Preventable kidney injury
- Connects to: Acute kidney injury, dialysis

#### 717. **Oversedation/Opioid-Related Respiratory Depression Events**
- Type: Real (rate)
- Unit: Events per 1,000 patient-days on opioids
- Why Critical: Preventable serious harm
- Connects to: Respiratory failure, cardiac arrest

#### 718. **Delayed Diagnosis Leading to Serious Harm**
- Type: Real (rate)
- Unit: Events per 100,000 encounters
- Why Critical: Malpractice, poor outcomes
- Baseline: Hard to measure, estimated 40,000-80,000 deaths/year
- Connects to: Mortality, preventable morbidity

### Overuse & Low-Value Care

#### 719. **Low-Value Service Utilization Index**
- Type: Index
- Unit: 0-10 (composite of low-value services used)
- Why Critical: Wastes resources, can cause harm
- Baseline: Widespread use of low-value services
- Connects to: Costs, overdiagnosis, overtreatment

#### 720. **Antibiotic Overprescribing Rate (Viral Conditions)**
- Type: Proportion
- Unit: 0-1 (% viral URIs prescribed antibiotics)
- Why Critical: Drives resistance, unnecessary side effects
- Baseline: Still 30-50% in some settings
- Connects to: Antibiotic resistance, C.diff

#### 721. **Imaging Overuse (Low Back Pain, Sinusitis)**
- Type: Proportion
- Unit: 0-1 (% low-value imaging performed)
- Why Critical: Costs, incidental findings, unnecessary anxiety
- Baseline: High overuse persists
- Connects to: Costs, overtreatment cascade

#### 722. **Prostate Cancer Overscreening (PSA in Older Men)**
- Type: Proportion
- Unit: 0-1 (% men >70 screened)
- Why Critical: Overdiagnosis, overtreatment of indolent cancers
- Baseline: Decreasing but still performed
- Connects to: Overtreatment, morbidity from treatment

#### 723. **Preoperative Testing Overuse (Low-Risk Surgery)**
- Type: Proportion
- Unit: 0-1 (% low-risk surgeries with unnecessary testing)
- Why Critical: Costs, delays, incidental findings
- Connects to: Costs, false positives, delays

#### 724. **Vitamin D Screening Overuse**
- Type: Proportion
- Unit: 0-1 (% asymptomatic screened)
- Why Critical: Low-value, high cost
- Connects to: Healthcare costs

#### 725. **Continuous Cardiac Monitoring Overuse (Low-Risk Patients)**
- Type: Proportion
- Unit: 0-1 (% low-risk patients monitored)
- Why Critical: Alarm fatigue, false positives, costs
- Connects to: Alert fatigue, costs

---

## DOMAIN 3: SPECIALIZED CLINICAL AREAS (42 missing nodes)

### Cancer Care Continuum

#### 726. **Cancer Stage at Diagnosis**
- Type: Categorical distribution
- Unit: % diagnosed at each stage (I, II, III, IV)
- Why Critical: Determines survival, treatment intensity
- Baseline: Variable by cancer type, disparities exist
- Connects to: Cancer mortality, treatment costs

#### 727. **Oncology Treatment Access (Medical, Radiation, Surgical)**
- Type: Real (distance/time)
- Unit: Miles to nearest cancer center, wait times
- Why Critical: Delays worsen outcomes
- Baseline: Rural deserts, safety net access issues
- Connects to: Cancer outcomes, treatment abandonment

#### 728. **Clinical Trial Participation Rate (Cancer)**
- Type: Proportion
- Unit: 0-1 (% eligible patients enrolled in trials)
- Why Critical: Access to cutting-edge treatments, research progress
- Baseline: <5%, lower for minorities
- Connects to: Cancer outcomes, treatment innovation

#### 729. **Financial Toxicity from Cancer Treatment**
- Type: Index
- Unit: 0-10 (composite: cost, debt, bankruptcy)
- Why Critical: Affects treatment adherence, outcomes
- Baseline: 42% report financial hardship
- Connects to: Treatment abandonment, bankruptcy, worse outcomes

#### 730. **Cancer Survivorship Care Planning**
- Type: Proportion
- Unit: 0-1 (% survivors with documented care plan)
- Why Critical: Long-term surveillance, late effects
- Baseline: Low, <20% receive survivorship care plan
- Connects to: Late effects detection, quality of life

#### 731. **Palliative Care Integration in Cancer**
- Type: Proportion
- Unit: 0-1 (% advanced cancer with palliative care)
- Why Critical: Improves quality of life, may extend survival
- Baseline: <50% receive palliative care
- Connects to: Symptom burden, quality of life, hospice transitions

### Kidney Disease & Dialysis

#### 732. **Chronic Kidney Disease (CKD) Awareness**
- Type: Proportion
- Unit: 0-1 (% with CKD aware of diagnosis)
- Why Critical: Early management prevents progression
- Baseline: <50% of those with CKD aware
- Connects to: ESRD prevention, complications

#### 733. **Dialysis Modality (Hemodialysis vs. Peritoneal)**
- Type: Proportion
- Unit: 0-1 (% on PD vs. HD)
- Why Critical: PD associated with better quality of life, lower cost
- Baseline: <10% on PD in US (much higher elsewhere)
- Connects to: Quality of life, costs, hospitalization

#### 734. **Dialysis Adequacy (Kt/V)**
- Type: Real (ratio)
- Unit: Kt/V ratio
- Why Critical: Adequate dialysis improves outcomes
- Baseline: Target >1.2, some don't achieve
- Connects to: Mortality, morbidity

#### 735. **Kidney Transplant Wait Time**
- Type: Real (months)
- Unit: Median time on transplant list
- Why Critical: Waitlist mortality, quality of life
- Baseline: 3-5 years median, racial disparities
- Connects to: Dialysis duration, mortality, quality of life

#### 736. **Living Donor Kidney Transplant Rate**
- Type: Proportion
- Unit: 0-1 (% transplants from living donors)
- Why Critical: Better outcomes than deceased donor
- Baseline: ~30% of transplants
- Connects to: Transplant outcomes, waiting time

#### 737. **Vascular Access Type (AV Fistula vs. Catheter)**
- Type: Proportion
- Unit: 0-1 (% on AVF vs. catheter)
- Why Critical: Catheters → infection, worse outcomes
- Baseline: Target >80% AVF, many facilities below
- Connects to: Dialysis infections, hospitalizations, mortality

### Organ Transplantation

#### 738. **Organ Donation Rate**
- Type: Real (rate)
- Unit: Donors per million population
- Why Critical: Organ shortage crisis
- Baseline: ~30-40 per million, huge shortage
- Connects to: Wait list mortality, transplant access

#### 739. **Transplant Center Volume & Outcomes**
- Type: Real (count + survival rates)
- Unit: Transplants per year, 1-year survival
- Why Critical: Volume-outcome relationship
- Connects to: Transplant mortality, graft survival

#### 740. **Post-Transplant Medication Adherence**
- Type: Proportion
- Unit: 0-1 (% adherent to immunosuppression)
- Why Critical: Non-adherence → rejection
- Connects to: Graft failure, return to dialysis

### Rehabilitation Services

#### 741. **Post-Stroke Rehabilitation Access**
- Type: Proportion
- Unit: 0-1 (% stroke survivors receiving rehab)
- Why Critical: Determines functional recovery
- Baseline: Underutilization, insurance barriers
- Connects to: Disability, nursing home placement

#### 742. **Cardiac Rehabilitation Participation**
- Type: Proportion
- Unit: 0-1 (% post-MI patients completing cardiac rehab)
- Why Critical: Reduces recurrent MI, mortality by 25%
- Baseline: <25% participate despite evidence
- Connects to: Recurrent MI, mortality

#### 743. **Physical Therapy Access & Wait Times**
- Type: Real (days + availability)
- Unit: Days to PT appointment, therapists per 100k
- Why Critical: Delays worsen outcomes (especially post-surgery)
- Connects to: Functional recovery, chronic pain

### Dental & Oral Health

#### 744. **Dental Care Access**
- Type: Proportion
- Unit: 0-1 (% with dental visit past year)
- Why Critical: Oral health affects overall health
- Baseline: 0.64, lower for uninsured/Medicaid
- Connects to: Dental disease, systemic infections

#### 745. **Dental Insurance Coverage**
- Type: Proportion
- Unit: 0-1 (% with dental insurance)
- Why Critical: Major barrier to dental care
- Baseline: 0.77, but coverage often inadequate
- Connects to: Dental access, untreated decay

#### 746. **Untreated Dental Caries Prevalence**
- Type: Proportion
- Unit: 0-1 (% with untreated cavities)
- Why Critical: Causes pain, infections, systemic effects
- Baseline: 0.31 children, 0.27 adults
- Connects to: Dental pain, infections, ED visits

#### 747. **Dental Emergency Department Visits**
- Type: Real (rate)
- Unit: Dental ED visits per 100,000
- Why Critical: Preventable with dental access
- Baseline: ~800 per 100,000, growing
- Connects to: Healthcare costs, inefficient care

### Vision & Hearing

#### 748. **Vision Care Access**
- Type: Proportion
- Unit: 0-1 (% with eye exam past 2 years)
- Why Critical: Detects treatable conditions (glaucoma, diabetic retinopathy)
- Baseline: 0.55-0.60
- Connects to: Preventable blindness, falls

#### 749. **Diabetic Retinopathy Screening Rate**
- Type: Proportion
- Unit: 0-1 (% diabetics with annual eye exam)
- Why Critical: Prevents blindness
- Baseline: ~60% screened
- Connects to: Diabetic blindness, vision loss

#### 750. **Hearing Aid Utilization Among Those with Loss**
- Type: Proportion
- Unit: 0-1 (% with hearing loss using aids)
- Why Critical: Affects social isolation, cognitive decline
- Baseline: <30% use aids (cost barriers)
- Connects to: Social isolation, cognitive decline, falls

#### 751. **Hearing Screening (Newborn & School-Age)**
- Type: Proportion
- Unit: 0-1 (% screened)
- Why Critical: Early intervention for developmental delays
- Baseline: >98% newborns, variable school-age
- Connects to: Speech delays, educational outcomes

### Pain Management & Palliative Care

#### 752. **Chronic Pain Prevalence**
- Type: Proportion
- Unit: 0-1 (% with chronic pain)
- Why Critical: Affects quality of life, function, opioid use
- Baseline: 0.20 (20%), higher in some demographics
- Connects to: Disability, opioid use, depression

#### 753. **Multimodal Pain Management Utilization**
- Type: Index
- Unit: 0-10 (use of non-opioid modalities)
- Why Critical: Reduces opioid dependence
- Baseline: Underutilized
- Connects to: Chronic opioid use, function

#### 754. **Palliative Care Access (Serious Illness)**
- Type: Proportion
- Unit: 0-1 (% seriously ill with palliative care)
- Why Critical: Improves quality of life, reduces hospitalizations
- Baseline: <40% have access
- Connects to: Symptom burden, hospitalizations, quality of life

#### 755. **Hospice Enrollment (End-of-Life)**
- Type: Proportion
- Unit: 0-1 (% dying patients enrolled in hospice)
- Why Critical: Reduces suffering, ICU deaths
- Baseline: ~48% enroll, often late
- Connects to: ICU deaths, quality of death

#### 756. **Hospice Length of Stay**
- Type: Real (days)
- Unit: Median days in hospice
- Why Critical: Very short stays limit benefit
- Baseline: Median ~18 days (ideally >2-3 months)
- Connects to: End-of-life quality, family bereavement

### Maternal-Fetal Medicine

#### 757. **High-Risk Pregnancy Identification Rate**
- Type: Proportion
- Unit: 0-1 (% high-risk pregnancies identified early)
- Why Critical: Enables appropriate level of care
- Connects to: Maternal morbidity, preterm birth

#### 758. **Maternal-Fetal Medicine Specialist Access**
- Type: Real (availability)
- Unit: MFM specialists per 100,000 births
- Why Critical: Specialty care for high-risk pregnancies
- Baseline: Shortage, especially rural
- Connects to: Severe maternal morbidity, neonatal outcomes

#### 759. **Group Prenatal Care Participation (Centering Pregnancy)**
- Type: Proportion
- Unit: 0-1 (% pregnant receiving group care)
- Why Critical: Improves outcomes, satisfaction
- Baseline: <5% access
- Connects to: Preterm birth, maternal satisfaction

#### 760. **Postpartum Visit Attendance Rate**
- Type: Proportion
- Unit: 0-1 (% attending postpartum visit)
- Why Critical: Detects postpartum complications, depression
- Baseline: ~60% attend
- Connects to: Postpartum depression, complications

### Neonatology & Pediatric Specialty

#### 761. **Neonatal Intensive Care (NICU) Bed Availability**
- Type: Real (rate)
- Unit: NICU beds per 1,000 live births
- Why Critical: Access for high-risk newborns
- Baseline: Variable, rural transfer delays
- Connects to: Neonatal mortality, transfer risks

#### 762. **NICU Level of Care (by facility)**
- Type: Categorical
- Unit: Level I, II, III, IV designation
- Why Critical: Determines capabilities, outcomes
- Connects to: Neonatal outcomes, transfer needs

#### 763. **Pediatric Specialty Care Access**
- Type: Real (wait time + distance)
- Unit: Days to appointment, miles to pediatric specialist
- Why Critical: Children have unique needs
- Baseline: Shortage of pediatric subspecialists
- Connects to: Pediatric outcomes, family burden

### Geriatric & Gerontology

#### 764. **Geriatric Assessment Rate (Comprehensive)**
- Type: Proportion
- Unit: 0-1 (% older adults with CGA)
- Why Critical: Detects geriatric syndromes
- Baseline: Rare despite evidence
- Connects to: Falls, functional decline, polypharmacy

#### 765. **Geriatrician Availability**
- Type: Real (rate)
- Unit: Geriatricians per 10,000 adults 65+
- Why Critical: Severe shortage
- Baseline: ~1 per 10,000 (need ~3)
- Connects to: Geriatric care quality, polypharmacy

#### 766. **Deprescribing in Older Adults**
- Type: Proportion
- Unit: 0-1 (% on inappropriate meds who are deprescribed)
- Why Critical: Reduces polypharmacy harms
- Baseline: Rare, clinical inertia
- Connects to: Falls, cognitive impairment, ADEs

#### 767. **Age-Friendly Health System Designation**
- Type: Proportion
- Unit: 0-1 (% systems with 4Ms framework)
- Why Critical: Systematic geriatric care approach
- Baseline: Growing, ~15% of systems
- Connects to: Geriatric outcomes, delirium prevention

---

## DOMAIN 4: BEHAVIORAL HEALTH SYSTEM (35 missing nodes)

### Mental Health Treatment Infrastructure

#### 768. **Inpatient Psychiatric Bed Availability**
- Type: Real (rate)
- Unit: Psychiatric beds per 100,000 population
- Why Critical: Access for acute mental health crises
- Baseline: ~12 per 100,000 (down from 340 in 1960s)
- Connects to: Psychiatric ED boarding, involuntary commitment, criminalization

#### 769. **Psychiatric Emergency Department Boarding Time**
- Type: Real (hours)
- Unit: Mean hours waiting for psychiatric bed
- Why Critical: Traumatic, unsafe, ineffective
- Baseline: 10-24+ hours common
- Connects to: Patient safety, ED crowding, trauma

#### 770. **Mobile Crisis Team Coverage**
- Type: Proportion
- Unit: 0-1 (% population with access to mobile crisis)
- Why Critical: Diverts from ED, police, jail
- Baseline: <20% coverage nationally
- Connects to: Psychiatric hospitalization, police contact

#### 771. **Crisis Stabilization Unit Availability**
- Type: Real (rate)
- Unit: CSU beds per 100,000 population
- Why Critical: Alternative to psychiatric hospitalization
- Baseline: Very limited, growing
- Connects to: Psychiatric hospitalization, ED utilization

#### 772. **988 Suicide & Crisis Lifeline Response Time**
- Type: Real (seconds)
- Unit: Mean time to answer
- Why Critical: Immediate crisis response
- Baseline: Variable by state, improving
- Connects to: Suicide prevention, crisis de-escalation

#### 773. **Intensive Outpatient Program (IOP) Capacity**
- Type: Real (rate)
- Unit: IOP slots per 100,000 population
- Why Critical: Step-down from inpatient, prevent hospitalization
- Connects to: Psychiatric readmissions, community tenure

#### 774. **Partial Hospitalization Program (PHP) Capacity**
- Type: Real (rate)
- Unit: PHP slots per 100,000 population
- Why Critical: High-intensity outpatient alternative
- Connects to: Psychiatric hospitalization, treatment gaps

#### 775. **Assertive Community Treatment (ACT) Team Coverage**
- Type: Proportion
- Unit: 0-1 (% with SMI having access to ACT)
- Why Critical: Evidence-based for severe mental illness
- Baseline: <10% coverage
- Connects to: Psychiatric hospitalization, homelessness, criminal justice

#### 776. **Peer Support Specialist Workforce**
- Type: Real (rate)
- Unit: Certified peer specialists per 100,000
- Why Critical: Recovery-oriented, effective, lived experience
- Baseline: Growing but limited
- Connects to: Mental health recovery, treatment engagement

#### 777. **Mental Health Parity Enforcement**
- Type: Index
- Unit: 0-10 (compliance + enforcement)
- Why Critical: Ensures equal coverage for mental health
- Baseline: Weak enforcement despite federal law
- Connects to: Mental health treatment access, out-of-pocket costs

### Substance Use Treatment Continuum

#### 778. **Medication-Assisted Treatment (MAT) Availability**
- Type: Real (rate)
- Unit: MAT providers per 100,000 population
- Why Critical: Gold standard for opioid use disorder
- Baseline: Severe shortage, especially rural
- Connects to: Overdose, treatment outcomes

#### 779. **Buprenorphine Prescriber Density**
- Type: Real (rate)
- Unit: Waivered prescribers per 100,000
- Why Critical: Access to life-saving OUD medication
- Baseline: 47 per 100k nationally, rural deserts
- Connects to: Overdose mortality, treatment access

#### 780. **Methadone Clinic Proximity**
- Type: Real (distance)
- Unit: Miles to nearest methadone clinic
- Why Critical: Daily dosing requirement, geographic barrier
- Baseline: Urban concentration, rural deserts
- Connects to: Treatment access, retention

#### 781. **Residential Substance Use Treatment Capacity**
- Type: Real (rate)
- Unit: Residential beds per 100,000 with SUD
- Why Critical: Needed for severe SUD
- Baseline: Insufficient, waitlists common
- Connects to: Overdose, treatment gaps

#### 782. **Detoxification Service Availability**
- Type: Real (rate)
- Unit: Medical detox beds per 100,000
- Why Critical: Safe withdrawal, entry to treatment
- Baseline: Insufficient, ED used inappropriately
- Connects to: Treatment initiation, medical complications

#### 783. **Harm Reduction Service Density**
- Type: Real (rate)
- Unit: Syringe exchange programs, naloxone distribution sites per 100,000
- Why Critical: Reduces overdose, infectious disease
- Baseline: Legal barriers in many jurisdictions
- Connects to: Overdose, HIV, HCV transmission

#### 784. **Naloxone Distribution Rate (Community)**
- Type: Real (count)
- Unit: Naloxone kits distributed per 100,000
- Why Critical: Reverses overdoses, saves lives
- Baseline: Increasing but not universal
- Connects to: Overdose mortality

#### 785. **Recovery Housing Availability**
- Type: Real (rate)
- Unit: Recovery housing beds per 100,000
- Why Critical: Supportive environment post-treatment
- Baseline: Unmet need, quality variable
- Connects to: SUD relapse, housing stability

#### 786. **Substance Use Treatment Wait Time**
- Type: Real (days)
- Unit: Days from request to admission
- Why Critical: Delay → relapse, overdose
- Baseline: Days to weeks common
- Connects to: Treatment initiation, overdose risk

#### 787. **Substance Use Treatment Retention Rate**
- Type: Proportion
- Unit: 0-1 (% completing or staying >90 days)
- Why Critical: Retention determines outcomes
- Baseline: ~50% drop out early
- Connects to: SUD outcomes, relapse

### Integrated Behavioral Health

#### 788. **Behavioral Health Integration in Primary Care**
- Type: Proportion
- Unit: 0-1 (% primary care with co-located behavioral health)
- Why Critical: Improves access, reduces stigma
- Baseline: ~30% have some integration
- Connects to: Mental health treatment access, outcomes

#### 789. **Collaborative Care Model Implementation**
- Type: Proportion
- Unit: 0-1 (% practices using CCM for depression)
- Why Critical: Evidence-based, effective
- Baseline: <20% implementation
- Connects to: Depression outcomes, treatment engagement

#### 790. **Screening, Brief Intervention, Referral to Treatment (SBIRT) Penetration**
- Type: Proportion
- Unit: 0-1 (% practices implementing SBIRT)
- Why Critical: Early intervention for substance use
- Baseline: <20% despite guidelines
- Connects to: Substance use detection, intervention

### Specialty Behavioral Health Populations

#### 791. **Eating Disorder Treatment Availability**
- Type: Real (rate)
- Unit: Eating disorder specialists per 100,000
- Why Critical: Specialized treatment needed
- Baseline: Severe shortage
- Connects to: Eating disorder mortality, recovery

#### 792. **Trauma-Informed Care Implementation**
- Type: Proportion
- Unit: 0-1 (% behavioral health settings with TIC)
- Why Critical: Reduces retraumatization
- Baseline: Variable implementation
- Connects to: Treatment engagement, outcomes

#### 793. **Child & Adolescent Psychiatrist Density**
- Type: Real (rate)
- Unit: Child psychiatrists per 100,000 youth
- Why Critical: Severe shortage
- Baseline: ~8 per 100,000 (need ~47)
- Connects to: Pediatric mental health access

#### 794. **School-Based Mental Health Services**
- Type: Proportion
- Unit: 0-1 (% schools with on-site mental health)
- Why Critical: Access where youth are
- Baseline: ~40% of schools
- Connects to: Youth mental health access, crisis prevention

#### 795. **Geriatric Psychiatry Availability**
- Type: Real (rate)
- Unit: Geriatric psychiatrists per 100,000 seniors
- Why Critical: Specialized needs of older adults
- Baseline: Severe shortage
- Connects to: Late-life depression, dementia care

#### 796. **LGBTQ-Affirming Mental Health Provider Density**
- Type: Proportion
- Unit: 0-1 (% providers with LGBTQ competency training)
- Why Critical: Reduces disparities, improves outcomes
- Baseline: Limited
- Connects to: Mental health outcomes for LGBTQ youth/adults

#### 797. **First Episode Psychosis Program Availability**
- Type: Real (rate)
- Unit: NAVIGATE/OnTrackNY slots per 100,000
- Why Critical: Critical period for intervention
- Baseline: Sparse coverage
- Connects to: Psychosis outcomes, functional recovery

### Commitment & Involuntary Treatment

#### 798. **Involuntary Psychiatric Hold Rate**
- Type: Real (rate)
- Unit: 5150/72-hour holds per 100,000
- Why Critical: Indicates crisis response, coercion
- Connects to: Civil liberties, trauma, treatment relationship

#### 799. **Assisted Outpatient Treatment (AOT) Utilization**
- Type: Real (rate)
- Unit: AOT orders per 100,000 with SMI
- Why Critical: Controversial, mandated outpatient treatment
- Connects to: Psychiatric hospitalization, autonomy

#### 800. **Mental Health Court Availability**
- Type: Real (count)
- Unit: Mental health courts per metro area
- Why Critical: Diverts from incarceration
- Connects to: Incarceration, treatment access

#### 801. **Criminal Justice Diversion Program Capacity (Mental Health)**
- Type: Real (rate)
- Unit: Diversion slots per 100,000
- Why Critical: Prevents criminalization of mental illness
- Connects to: Incarceration, treatment engagement

#### 802. **Jail-Based Mental Health Services**
- Type: Index
- Unit: 0-10 (adequacy of jail mental health care)
- Why Critical: High prevalence of mental illness in jails
- Connects to: Suicide in custody, recidivism, outcomes

---

## DOMAIN 5: LONG-TERM SERVICES & SUPPORTS (28 missing nodes)

### Home & Community-Based Services

#### 803. **Home Health Care Availability**
- Type: Real (rate)
- Unit: Home health agencies per 100,000
- Why Critical: Enables aging in place
- Baseline: Variable by region
- Connects to: Nursing home admission, hospital readmissions

#### 804. **Home Health Aide Workforce Shortage**
- Type: Real (vacancy rate)
- Unit: % positions unfilled
- Why Critical: Limits home care capacity
- Baseline: 15-25% vacancy
- Connects to: Home care access, family caregiver burden

#### 805. **Adult Day Services Capacity**
- Type: Real (rate)
- Unit: Adult day center slots per 1,000 seniors
- Why Critical: Caregiver respite, socialization
- Baseline: Limited, declining
- Connects to: Caregiver burden, social isolation, nursing home delay

#### 806. **Personal Care Attendant Availability**
- Type: Real (rate + waitlist)
- Unit: PCAs per 1,000 disabled, waitlist time
- Why Critical: Enables community living for disabled
- Baseline: Severe shortage, long waitlists
- Connects to: Disability community tenure, institutional placement

#### 807. **Home Modification & Assistive Technology Access**
- Type: Proportion
- Unit: 0-1 (% needing modifications who receive)
- Why Critical: Prevents falls, enables independence
- Baseline: Low, cost barriers
- Connects to: Falls, nursing home placement

#### 808. **Meals on Wheels & Nutrition Program Coverage**
- Type: Proportion
- Unit: 0-1 (% eligible seniors receiving)
- Why Critical: Nutrition, socialization, wellness check
- Baseline: Serves ~2.4M, but 9M need
- Connects to: Malnutrition, social isolation (seniors)

#### 809. **PACE (Program of All-Inclusive Care for the Elderly) Enrollment**
- Type: Real (rate)
- Unit: PACE participants per 10,000 seniors
- Why Critical: Comprehensive care coordination for frail elders
- Baseline: Very limited availability
- Connects to: Nursing home diversion, hospitalizations

### Residential Care

#### 810. **Assisted Living Facility (ALF) Bed Availability**
- Type: Real (rate)
- Unit: ALF beds per 1,000 seniors
- Why Critical: Intermediate option between home and nursing home
- Baseline: Variable, affordability barrier
- Connects to: Nursing home placement, housing stability

#### 811. **Assisted Living Quality & Regulation**
- Type: Index
- Unit: 0-10 (staffing, services, oversight)
- Why Critical: Variable quality, limited regulation
- Connects to: Elder safety, quality of life

#### 812. **Board & Care / Group Home Capacity**
- Type: Real (rate)
- Unit: Beds per 100,000 with SMI or IDD
- Why Critical: Supportive living for special populations
- Baseline: Declining supply
- Connects to: Community tenure, hospitalization

#### 813. **Skilled Nursing Facility Quality (5-Star Rating Distribution)**
- Type: Categorical distribution
- Unit: % facilities at each star rating
- Why Critical: Quality highly variable
- Baseline: ~20% are 1-2 star (poor quality)
- Connects to: Nursing home mortality, hospitalizations, quality of life

#### 814. **Nursing Home Staffing Levels**
- Type: Real (hours)
- Unit: Direct care hours per resident day
- Why Critical: Staffing determines quality, safety
- Baseline: Below recommended 4.1 hrs/resident/day
- Connects to: Nursing home quality, falls, pressure ulcers

#### 815. **Nursing Home Turnover Rate (Staff)**
- Type: Proportion
- Unit: 0-1 (annual turnover rate)
- Why Critical: High turnover → poor quality
- Baseline: 50-100% annual turnover
- Connects to: Nursing home quality, continuity of care

### Long-Term Care Financing

#### 816. **Medicaid LTSS Spend (HCBS vs. Institutional)**
- Type: Proportion
- Unit: 0-1 (% LTSS on HCBS vs. nursing homes)
- Why Critical: Rebalancing toward home/community
- Baseline: Now ~60% HCBS (up from 20% in 1995)
- Connects to: Nursing home census, community living

#### 817. **Medicaid HCBS Waiver Waitlist**
- Type: Real (count + wait time)
- Unit: People waiting for waiver, years waiting
- Why Critical: Unmet need for community services
- Baseline: 600,000+ waiting, years-long waits
- Connects to: Institutional placement, family burden

#### 818. **Long-Term Care Insurance Penetration**
- Type: Proportion
- Unit: 0-1 (% seniors with LTC insurance)
- Why Critical: Protects against catastrophic costs
- Baseline: ~7% have policies (declining market)
- Connects to: Medicaid spend-down, family burden

#### 819. **Catastrophic Long-Term Care Costs (Out-of-Pocket)**
- Type: Real (dollars)
- Unit: Median OOP spending for LTC
- Why Critical: Impoverishing
- Baseline: ~$100k+ for nursing home stay
- Connects to: Asset depletion, Medicaid eligibility

### Caregiver Support

#### 820. **Family Caregiver Prevalence**
- Type: Proportion
- Unit: 0-1 (% adults providing unpaid care)
- Why Critical: Backbone of LTC system
- Baseline: 0.21 (21%), 53 million caregivers
- Connects to: Caregiver burden, workforce participation

#### 821. **Caregiver Support Program Availability**
- Type: Real (enrollment rate)
- Unit: % caregivers accessing support programs
- Why Critical: Reduces caregiver burden, burnout
- Baseline: <15% access services
- Connects to: Caregiver health, care recipient institutionalization

#### 822. **Paid Family Leave for Caregiving**
- Type: Policy + utilization
- Unit: 0-1 (policy presence) + % taking leave
- Why Critical: Enables caregiving without job loss
- Baseline: Only 13 states have programs
- Connects to: Caregiver burden, employment stability

#### 823. **Respite Care Availability**
- Type: Real (hours)
- Unit: Respite hours available per caregiver
- Why Critical: Prevents caregiver burnout
- Baseline: Very limited
- Connects to: Caregiver burden, institutionalization

### Disability Services

#### 824. **Intellectual & Developmental Disability (IDD) Waiver Access**
- Type: Proportion + waitlist
- Unit: 0-1 (% eligible receiving) + wait time
- Why Critical: Supports community living
- Baseline: Long waitlists, unmet need
- Connects to: Institutional placement, family burden

#### 825. **Supported Employment for People with Disabilities**
- Type: Proportion
- Unit: 0-1 (% disabled in competitive integrated employment)
- Why Critical: Economic participation, independence
- Baseline: <20% in integrated employment
- Connects to: Disability income, social inclusion

#### 826. **Accessible Housing Stock**
- Type: Proportion
- Unit: 0-1 (% housing units accessible)
- Why Critical: Enables community living for disabled
- Baseline: <5% of housing stock accessible
- Connects to: Institutional placement, housing instability

#### 827. **Personal Assistance Services Adequacy**
- Type: Index
- Unit: 0-10 (hours approved vs. need)
- Why Critical: Enables daily living for disabled
- Connects to: Institutional risk, quality of life

#### 828. **Olmstead Compliance (Community Integration Mandate)**
- Type: Index
- Unit: 0-10 (state compliance with ADA integration mandate)
- Why Critical: Legal right to community living
- Connects to: Institutional placement, HCBS access

### Dementia Care

#### 829. **Dementia Diagnosis Rate**
- Type: Proportion
- Unit: 0-1 (% with dementia who have diagnosis)
- Why Critical: Enables care planning, services
- Baseline: ~50% undiagnosed
- Connects to: Care planning, safety, caregiver burden

#### 830. **Memory Care Unit Availability**
- Type: Real (rate)
- Unit: Memory care beds per 1,000 seniors
- Why Critical: Specialized dementia care
- Connects to: Behavioral crises, caregiver burden

---

## DOMAIN 6: PUBLIC HEALTH INFRASTRUCTURE (25 missing nodes)

### Disease Surveillance & Monitoring

#### 831. **Infectious Disease Surveillance System Capacity**
- Type: Index
- Unit: 0-10 (timeliness, completeness, data quality)
- Why Critical: Early outbreak detection
- Baseline: Variable by jurisdiction
- Connects to: Outbreak control, pandemic response

#### 832. **Syndromic Surveillance Coverage**
- Type: Proportion
- Unit: 0-1 (% EDs, urgent care reporting)
- Why Critical: Real-time disease detection
- Connects to: Outbreak detection speed

#### 833. **Laboratory Testing Capacity (Public Health Labs)**
- Type: Real (capacity)
- Unit: Tests per day capacity
- Why Critical: Diagnostic capacity for outbreaks
- Connects to: Outbreak response, pandemic preparedness

#### 834. **Contact Tracing Workforce**
- Type: Real (rate)
- Unit: Contact tracers per 100,000 population
- Why Critical: Outbreak control
- Baseline: Decimated after COVID surge
- Connects to: Disease transmission, outbreak control

#### 835. **Vital Statistics Timeliness**
- Type: Real (lag time)
- Unit: Weeks from death to death certificate data
- Why Critical: Monitoring mortality trends
- Connects to: Public health surveillance, research

### Immunization Infrastructure

#### 836. **Immunization Registry Completeness**
- Type: Proportion
- Unit: 0-1 (% immunizations captured in registry)
- Why Critical: Tracking coverage, outbreak response
- Baseline: Variable by state
- Connects to: Immunization rates, outbreak response

#### 837. **Vaccine Distribution Infrastructure**
- Type: Index
- Unit: 0-10 (cold chain, access points, equity)
- Why Critical: Equitable vaccine access
- Connects to: Immunization rates, outbreak control

#### 838. **Vaccine Hesitancy Rate**
- Type: Proportion
- Unit: 0-1 (% hesitant or refusing vaccines)
- Why Critical: Herd immunity, outbreak risk
- Baseline: Growing, ~20-30%
- Connects to: Immunization rates, outbreaks

### Outbreak Response

#### 839. **Epidemic Response Funding (Sustained)**
- Type: Real (dollars)
- Unit: $ per capita sustained funding (not surge)
- Why Critical: Preparedness requires sustained capacity
- Baseline: Boom-bust cycle, chronic underfunding
- Connects to: Outbreak response capability

#### 840. **Public Health Emergency Preparedness Exercises**
- Type: Real (frequency)
- Unit: Drills per year
- Why Critical: Readiness testing
- Connects to: Pandemic/disaster response effectiveness

#### 841. **Strategic National Stockpile Adequacy**
- Type: Index
- Unit: 0-10 (supplies vs. need for major event)
- Why Critical: Surge capacity for pandemics, disasters
- Connects to: Pandemic response, disaster mortality

#### 842. **Public Health Workforce Capacity**
- Type: Real (rate)
- Unit: Public health workers per 100,000
- Why Critical: Foundational capacity
- Baseline: 50 per 100k (down from 60 in 2008)
- Connects to: All public health functions

#### 843. **Environmental Health Inspection Capacity**
- Type: Real (rate)
- Unit: Inspectors per 1,000 establishments
- Why Critical: Food safety, water, housing, vector control
- Connects to: Foodborne illness, environmental hazards

### Health Promotion & Prevention

#### 844. **Tobacco Control Policy Strength**
- Type: Index
- Unit: 0-10 (taxes, smoke-free laws, cessation support)
- Why Critical: Leading preventable cause of death
- Connects to: Smoking prevalence, lung cancer, COPD

#### 845. **Smoke-Free Policy Coverage**
- Type: Proportion
- Unit: 0-1 (% population covered by smoke-free laws)
- Why Critical: Secondhand smoke protection
- Connects to: Secondhand smoke exposure, asthma

#### 846. **Tobacco Cessation Program Availability**
- Type: Real (reach)
- Unit: Quitline capacity, NRT distribution per smoker
- Why Critical: Cessation support doubles quit rates
- Connects to: Smoking prevalence

#### 847. **Community Health Assessment Frequency & Quality**
- Type: Index
- Unit: 0-10 (recency, comprehensiveness, community engagement)
- Why Critical: Identifies health needs, guides priorities
- Connects to: Resource allocation, program targeting

#### 848. **Community Health Improvement Plan Implementation**
- Type: Index
- Unit: 0-10 (plan quality, implementation, progress)
- Why Critical: Translates assessment to action
- Connects to: Population health outcomes

#### 849. **Chronic Disease Prevention Program Reach**
- Type: Proportion
- Unit: 0-1 (% at-risk population reached by programs)
- Why Critical: Prevents diabetes, heart disease
- Connects to: Chronic disease incidence

#### 850. **Healthy Food Financing Initiative Funding**
- Type: Real (dollars)
- Unit: $ millions for grocery store incentives
- Why Critical: Addresses food deserts
- Connects to: Grocery access, food security

#### 851. **Community Water Fluoridation Coverage**
- Type: Proportion
- Unit: 0-1 (% population with fluoridated water)
- Why Critical: Prevents dental caries
- Baseline: 0.73 nationally
- Connects to: Dental health, especially children

#### 852. **Lead Poisoning Prevention Program Capacity**
- Type: Index
- Unit: 0-10 (screening, follow-up, remediation)
- Why Critical: Prevents developmental harm
- Connects to: Childhood lead exposure, neurodevelopment

### Vector Control & Environmental Health

#### 853. **Vector Control Program Capacity**
- Type: Index
- Unit: 0-10 (mosquito, tick, rodent control)
- Why Critical: Prevents vector-borne disease
- Connects to: West Nile, Lyme, Zika, plague

#### 854. **Foodborne Illness Surveillance**
- Type: Real (detection rate)
- Unit: Foodborne outbreaks detected per 100k
- Why Critical: Food safety
- Connects to: Foodborne illness burden

#### 855. **Restaurant Inspection Frequency**
- Type: Real (rate)
- Unit: Inspections per restaurant per year
- Why Critical: Food safety enforcement
- Baseline: Variable, often under-resourced
- Connects to: Foodborne illness

---

## DOMAIN 7: SOCIAL SERVICES INFRASTRUCTURE DETAIL (23 missing nodes)

### Child Welfare System

#### 856. **Child Protective Services (CPS) Caseload**
- Type: Real (ratio)
- Unit: Children per caseworker
- Why Critical: Determines quality of investigations
- Baseline: 60-100:1 (recommended 12-17:1)
- Connects to: Child safety, family outcomes

#### 857. **Foster Care Placement Stability**
- Type: Real (rate)
- Unit: Placement changes per child
- Why Critical: Stability critical for child development
- Baseline: 2-3 placements average, some many more
- Connects to: Childhood trauma, developmental outcomes

#### 858. **Foster Parent Recruitment & Retention**
- Type: Real (rate)
- Unit: Foster parents per 1,000 children in care
- Why Critical: Placement availability
- Baseline: Shortage in most jurisdictions
- Connects to: Group home/institutional placement

#### 859. **Kinship Care Support**
- Type: Index
- Unit: 0-10 (financial support, services for relative caregivers)
- Why Critical: Kinship care best for stability but often unsupported
- Connects to: Placement stability, family preservation

#### 860. **Family Reunification Rate**
- Type: Proportion
- Unit: 0-1 (% children reunified within 12 months)
- Why Critical: Goal of child welfare system
- Connects to: Family separation duration, outcomes

#### 861. **Adoption Finalization Timeliness**
- Type: Real (months)
- Unit: Months from TPR to adoption finalization
- Why Critical: Permanency for children
- Connects to: Child well-being, foster care duration

#### 862. **Preventive Services Funding (Child Welfare)**
- Type: Real (proportion)
- Unit: % child welfare spending on prevention vs. foster care
- Why Critical: Upstream investment
- Baseline: Historically 20% prevention, shifting under Family First Act
- Connects to: Family preservation, removal rates

### Homeless Services Continuum

#### 863. **Street Outreach Team Coverage**
- Type: Real (rate)
- Unit: Outreach workers per 1,000 experiencing unsheltered homelessness
- Why Critical: Engagement with unsheltered population
- Connects to: Service engagement, shelter entry

#### 864. **Emergency Shelter Utilization Rate**
- Type: Proportion
- Unit: 0-1 (% shelter capacity occupied)
- Why Critical: Indicates shortage if >95%
- Baseline: Many cities at capacity
- Connects to: Unshelteredness, turnaway

#### 865. **Transitional Housing Availability**
- Type: Real (rate)
- Unit: Transitional housing beds per 1,000 homeless
- Why Critical: Bridge to permanent housing
- Baseline: Declining (shift to Housing First)
- Connects to: Housing placement, shelter duration

#### 866. **Rapid Rehousing Program Scale**
- Type: Real (rate)
- Unit: RRH slots per 1,000 homeless annually
- Why Critical: Evidence-based, cost-effective
- Connects to: Returns to homelessness, shelter exit

#### 867. **Housing First Program Fidelity**
- Type: Index
- Unit: 0-10 (fidelity to Housing First model)
- Why Critical: Fidelity determines effectiveness
- Connects to: Housing stability, outcomes

#### 868. **Coordinated Entry System Effectiveness**
- Type: Index
- Unit: 0-10 (coverage, assessment quality, prioritization, placement speed)
- Why Critical: Efficient allocation of scarce resources
- Connects to: Housing placement, waitlist time

#### 869. **Homeless Services Case Management Ratios**
- Type: Real (ratio)
- Unit: Clients per case manager
- Why Critical: Determines support intensity
- Baseline: Often 40-60:1 (should be 15-20:1 for intensive)
- Connects to: Housing stability, service engagement

### Domestic Violence Services

#### 870. **Domestic Violence Shelter Turnaway Rate**
- Type: Proportion
- Unit: 0-1 (% requests for shelter turned away due to capacity)
- Why Critical: Indicates shortage
- Baseline: ~60% turned away nationally on census day
- Connects to: DV victim safety, homelessness risk

#### 871. **DV Advocacy Services Availability**
- Type: Real (rate)
- Unit: DV advocates per 100,000 population
- Why Critical: Support beyond shelter
- Connects to: Safety planning, legal advocacy, economic empowerment

#### 872. **Domestic Violence Legal Advocacy (Orders of Protection)**
- Type: Real (rate)
- Unit: DV legal advocates per 100,000
- Why Critical: Navigating legal system
- Connects to: Orders of protection, safety

### Benefits Enrollment & Navigation

#### 873. **Benefits Navigator Availability**
- Type: Real (rate)
- Unit: Benefits navigators per 10,000 low-income
- Why Critical: Enrollment assistance for complex programs
- Connects to: SNAP, Medicaid, SSI enrollment rates

#### 874. **SNAP Recertification Burden**
- Type: Index
- Unit: 0-10 (paperwork, frequency, difficulty)
- Why Critical: Administrative burden → loss of benefits
- Connects to: SNAP churn, food insecurity

#### 875. **Medicaid Enrollment Process Complexity**
- Type: Index
- Unit: 0-10 (paperwork, verification, time to enrollment)
- Why Critical: Determines effective coverage
- Connects to: Uninsured rate, enrollment

#### 876. **Social Service Referral Completion Rate**
- Type: Proportion
- Unit: 0-1 (% referrals that result in connection to service)
- Why Critical: Closed-loop referrals critical
- Baseline: Often <30% complete referrals
- Connects to: Unmet social needs, healthcare outcomes

#### 877. **Integrated Social Services (One-Stop Shop)**
- Type: Proportion
- Unit: 0-1 (% jurisdictions with integrated access points)
- Why Critical: Reduces burden, increases access
- Connects to: Service utilization, unmet needs

#### 878. **Universal Basic Income / Cash Transfer Pilots**
- Type: Real (enrollment)
- Unit: Participants in UBI/guaranteed income pilots
- Why Critical: Emerging evidence on unconditional cash
- Connects to: Economic security, health outcomes

---

## DOMAIN 8: WORKPLACE & OCCUPATIONAL HEALTH (19 missing nodes)

### Occupational Exposures & Hazards

#### 879. **Occupational Injury Rate**
- Type: Real (rate)
- Unit: Injuries per 100 FTE workers
- Why Critical: Preventable workplace harm
- Baseline: 2.8 per 100 FTE (BLS)
- Connects to: Injury, disability, workers' comp claims

#### 880. **Occupational Illness Rate**
- Type: Real (rate)
- Unit: Illnesses per 100 FTE workers
- Why Critical: Chronic occupational disease
- Baseline: Underreported
- Connects to: Chronic disease, disability

#### 881. **Workplace Fatality Rate**
- Type: Real (rate)
- Unit: Deaths per 100,000 workers
- Why Critical: Preventable workplace deaths
- Baseline: 3.5 per 100,000
- Connects to: Premature mortality

#### 882. **Workplace Safety Inspection Frequency (OSHA)**
- Type: Real (rate)
- Unit: Inspections per 1,000 worksites per year
- Why Critical: Enforcement of safety standards
- Baseline: Very low, would take 165 years to inspect all sites once
- Connects to: Occupational injuries, violations

#### 883. **Workplace Ergonomic Hazard Prevalence**
- Type: Proportion
- Unit: 0-1 (% workers exposed to ergonomic hazards)
- Why Critical: Musculoskeletal disorders major burden
- Connects to: Back injury, carpal tunnel, disability

#### 884. **Occupational Chemical/Toxin Exposure**
- Type: Proportion
- Unit: 0-1 (% workers exposed to hazardous substances)
- Why Critical: Cancer, chronic disease risk
- Connects to: Lung disease, cancer, neurological damage

#### 885. **Workplace Heat Stress Risk**
- Type: Proportion
- Unit: 0-1 (% workers exposed to heat stress)
- Why Critical: Climate change increasing risk
- Connects to: Heat illness, cardiovascular events

### Workers' Compensation System

#### 886. **Workers' Compensation Coverage Rate**
- Type: Proportion
- Unit: 0-1 (% workers covered by workers' comp)
- Why Critical: Safety net for occupational injury/illness
- Baseline: ~87% covered (excludes gig, farm, some small employers)
- Connects to: Financial security after injury

#### 887. **Workers' Compensation Claim Denial Rate**
- Type: Proportion
- Unit: 0-1 (% claims denied)
- Why Critical: Access to benefits
- Connects to: Medical care after injury, lost wages

#### 888. **Workers' Compensation Medical Care Quality**
- Type: Index
- Unit: 0-10 (treatment guidelines, provider networks, outcomes)
- Why Critical: Determines recovery
- Connects to: Return to work, disability duration

#### 889. **Return to Work Rate Post-Injury**
- Type: Proportion
- Unit: 0-1 (% injured workers returning to work)
- Why Critical: Economic and health outcome
- Connects to: Employment stability, disability

### Workplace Policies & Benefits

#### 890. **Paid Sick Leave Access**
- Type: Proportion
- Unit: 0-1 (% workers with paid sick leave)
- Why Critical: Ability to stay home when sick
- Baseline: 0.77 have access, lower for low-wage
- Connects to: Infectious disease transmission, presenteeism

#### 891. **Workplace Wellness Program Quality**
- Type: Index
- Unit: 0-10 (comprehensiveness, participation, outcomes)
- Why Critical: Worksite health promotion
- Baseline: Variable effectiveness
- Connects to: Chronic disease prevention, health behaviors

#### 892. **Employee Assistance Program (EAP) Utilization**
- Type: Proportion
- Unit: 0-1 (% eligible employees using EAP)
- Why Critical: Mental health, substance use support
- Baseline: Low utilization despite availability
- Connects to: Mental health treatment, substance use

#### 893. **Workplace Flexibility (Remote, Schedule Control)**
- Type: Index
- Unit: 0-10 (remote options, schedule control, predictability)
- Why Critical: Work-life balance, stress
- Connects to: Chronic stress, work-family conflict, mental health

#### 894. **Occupational Health Services On-Site**
- Type: Proportion
- Unit: 0-1 (% worksites with on-site health services)
- Why Critical: Access to occupational health providers
- Connects to: Early intervention, screening

### Specific Occupational Populations

#### 895. **Healthcare Worker Injury Rate (Needlestick, MSK, Violence)**
- Type: Real (rate)
- Unit: Injuries per 100 FTE healthcare workers
- Why Critical: High-risk occupation
- Connects to: Infectious disease exposure, musculoskeletal disorders

#### 896. **Agricultural Worker Pesticide Exposure**
- Type: Proportion
- Unit: 0-1 (% ag workers exposed to pesticides)
- Why Critical: Unique occupational hazard
- Connects to: Acute poisoning, chronic disease

#### 897. **Gig Economy Worker Occupational Safety & Benefits**
- Type: Index
- Unit: 0-10 (safety protections, injury compensation, benefits)
- Why Critical: Growing workforce with minimal protections
- Connects to: Occupational injury without compensation, benefit gaps

---

## DOMAIN 9: HEALTH EQUITY & DISCRIMINATION (17 missing nodes)

### Provider Bias & Discrimination

#### 898. **Implicit Bias in Clinical Decision-Making**
- Type: Index
- Unit: 0-10 (prevalence, impact on care)
- Why Critical: Drives health disparities
- Connects to: Diagnostic delays, treatment disparities, pain undertreatment

#### 899. **Pain Undertreatment Disparities (Racial/Ethnic)**
- Type: Real (disparity ratio)
- Unit: Ratio of opioid prescribing (White vs. Black for same condition)
- Why Critical: False beliefs about pain tolerance
- Baseline: Black patients receive less pain medication
- Connects to: Pain, suffering, mistrust

#### 900. **Cardiac Catheterization Disparities**
- Type: Real (disparity ratio)
- Unit: Cath rate ratio by race (same presenting symptoms)
- Why Critical: Well-documented treatment disparity
- Connects to: MI outcomes, mortality disparities

#### 901. **Kidney Transplant Referral Disparities**
- Type: Real (disparity ratio)
- Unit: Referral rate ratio by race
- Why Critical: Life-saving treatment access gap
- Connects to: Dialysis duration, mortality

#### 902. **Maternal Mortality Racial Disparity**
- Type: Real (disparity ratio)
- Unit: Black:White maternal mortality ratio
- Why Critical: Stark disparity (3-4x higher for Black women)
- Connects to: Maternal mortality, structural racism

#### 903. **Infant Mortality Racial Disparity**
- Type: Real (disparity ratio)
- Unit: Black:White infant mortality ratio
- Why Critical: Persistent 2x disparity
- Connects to: Infant mortality, birth equity

### Discrimination in Care Access

#### 904. **Disability Discrimination in Healthcare**
- Type: Proportion
- Unit: 0-1 (% disabled reporting discrimination)
- Why Critical: Ableism barriers to care
- Connects to: Unmet healthcare needs, health disparities

#### 905. **LGBTQ Discrimination in Healthcare**
- Type: Proportion
- Unit: 0-1 (% LGBTQ reporting discrimination)
- Why Critical: Drives health disparities, avoidance of care
- Baseline: ~25% report discrimination
- Connects to: Unmet needs, mental health disparities

#### 906. **Language Access Barriers (LEP Patients)**
- Type: Proportion
- Unit: 0-1 (% LEP patients without interpretation)
- Why Critical: Patient safety, quality, equity
- Baseline: Interpretation often unavailable despite legal requirements
- Connects to: Medical errors, unmet needs

#### 907. **Insurance-Based Care Quality Disparities (Medicaid vs. Private)**
- Type: Real (disparity ratio)
- Unit: Quality metric ratios (Medicaid vs. private)
- Why Critical: Two-tier healthcare system
- Connects to: Health outcomes, provider access

### Clinical Algorithms & Structural Racism

#### 908. **Race-Based Clinical Algorithm Use**
- Type: Proportion
- Unit: 0-1 (% algorithms using race)
- Why Critical: Embeds structural racism in care
- Examples: eGFR, VBAC calculator, lung function
- Connects to: Diagnostic delays, treatment barriers

#### 909. **Kidney Function Algorithm Bias (eGFR)**
- Type: Impact measure
- Unit: % Black patients misclassified for CKD staging/transplant
- Why Critical: Delays kidney care, transplant referral
- Connects to: CKD progression, transplant access

### Health Literacy & Communication

#### 910. **Health Literacy Level**
- Type: Proportion
- Unit: 0-1 (% proficient health literacy)
- Why Critical: Determines self-management ability
- Baseline: Only 12% proficient
- Connects to: Medication adherence, disease management, utilization

#### 911. **Patient-Provider Concordance (Racial/Linguistic)**
- Type: Proportion
- Unit: 0-1 (% patients with concordant provider)
- Why Critical: Improves communication, trust, outcomes
- Baseline: Low for minorities
- Connects to: Treatment adherence, outcomes, satisfaction

#### 912. **Shared Decision-Making Implementation**
- Type: Proportion
- Unit: 0-1 (% encounters with SDM tools)
- Why Critical: Patient autonomy, preference-concordant care
- Connects to: Treatment satisfaction, adherence

### Systemic Inequities

#### 913. **Residential Segregation Index (Dissimilarity)**
- Type: Real (index)
- Unit: 0-1 (dissimilarity index)
- Why Critical: Fundamental cause of health disparities
- Baseline: 0.60+ in many metros (high segregation)
- Connects to: Exposure to all structural determinants

#### 914. **Environmental Justice Screening Index (EJSCREEN)**
- Type: Real (index)
- Unit: 0-100 percentile
- Why Critical: Cumulative environmental burdens
- Connects to: Pollution exposure, health disparities

---

## DOMAIN 10: ADDITIONAL CRISIS ENDPOINTS (12 missing nodes)

### Disability & Functional Status

#### 915. **Disability-Adjusted Life Years (DALYs) Lost**
- Type: Real (years)
- Unit: DALYs per 1,000 population
- Why Critical: Combines mortality and morbidity burden
- Connects to: Overall disease burden, quality of life

#### 916. **Activities of Daily Living (ADL) Limitation Prevalence**
- Type: Proportion
- Unit: 0-1 (% with ≥1 ADL limitation)
- Why Critical: Functional disability
- Baseline: 0.08 overall, 0.25 for 65+
- Connects to: Long-term care need, quality of life

#### 917. **Instrumental Activities of Daily Living (IADL) Limitation**
- Type: Proportion
- Unit: 0-1 (% with ≥1 IADL limitation)
- Why Critical: Functional independence
- Connects to: Community tenure, caregiver burden

### Pain & Symptom Burden

#### 918. **Chronic Pain Interference with Life**
- Type: Index
- Unit: 0-10 (PEG scale: pain + enjoyment + general activity)
- Why Critical: Quality of life impact
- Connects to: Disability, mental health, opioid use

#### 919. **Uncontrolled Symptom Burden (Serious Illness)**
- Type: Proportion
- Unit: 0-1 (% with serious illness with uncontrolled symptoms)
- Why Critical: Suffering, quality of life
- Connects to: Palliative care need, hospitalizations

### Mental Health Crises

#### 920. **Psychiatric Emergency Department Visit Rate**
- Type: Real (rate)
- Unit: Psychiatric ED visits per 100,000
- Why Critical: Mental health crisis utilization
- Baseline: Growing rapidly
- Connects to: Mental health system gaps, psychiatric hospitalization

### Oral Health Crises

#### 921. **Dental Pain Prevalence**
- Type: Proportion
- Unit: 0-1 (% with dental pain past year)
- Why Critical: Untreated dental disease
- Connects to: Dental access, infections, quality of life

### Vision & Hearing Loss

#### 922. **Vision Impairment Prevalence**
- Type: Proportion
- Unit: 0-1 (% with vision impairment)
- Why Critical: Functional limitation, falls
- Connects to: Falls, social isolation, employment

#### 923. **Hearing Loss Prevalence**
- Type: Proportion
- Unit: 0-1 (% with hearing loss)
- Why Critical: Social isolation, cognitive decline
- Connects to: Social isolation, cognitive impairment

### Adverse Childhood Experiences (ACEs)

#### 924. **Child Trauma Exposure (Adverse Childhood Experiences)**
- Type: Proportion
- Unit: 0-1 (% children with ≥4 ACEs)
- Why Critical: Lifelong health impact
- Connects to: Chronic disease, mental health, substance use (across lifespan)

### Medical Bankruptcy

#### 925. **Medical Bankruptcy Rate**
- Type: Real (rate)
- Unit: Bankruptcies attributed to medical debt per 100,000
- Why Critical: Financial catastrophe from illness
- Baseline: ~66% of bankruptcies have medical component
- Connects to: Medical debt, economic crisis

### Preventable Mortality

#### 926. **Amenable Mortality Rate**
- Type: Real (rate)
- Unit: Deaths per 100,000 from conditions amenable to healthcare
- Why Critical: Healthcare system quality indicator
- Connects to: Healthcare quality, access, outcomes

---

## SUMMARY: TOTAL ADDITIONAL NODES RECOMMENDED

| Domain | Additional Nodes |
|--------|-----------------|
| 1. Healthcare System Structure & Operations | 67 |
| 2. Clinical Care Processes & Quality | 58 |
| 3. Specialized Clinical Areas | 42 |
| 4. Behavioral Health System | 35 |
| 5. Long-Term Services & Supports | 28 |
| 6. Public Health Infrastructure | 25 |
| 7. Social Services Infrastructure Detail | 23 |
| 8. Workplace & Occupational Health | 19 |
| 9. Health Equity & Discrimination | 17 |
| 10. Additional Crisis Endpoints | 12 |
| **TOTAL** | **326** |

## NEW GRAND TOTAL

**Existing nodes:** 592
**Recommended additions:** 326
**Comprehensive total:** **918 nodes**

This would provide **complete mapping of the American health system** from structural determinants through clinical processes to crisis endpoints, with full representation of:
- Healthcare operations and infrastructure
- Clinical quality and processes
- Iatrogenic harms
- All specialized clinical domains
- Complete behavioral health continuum
- Long-term care system
- Public health capacity
- Social services detail
- Occupational health
- Health equity mechanisms

The resulting 918-node model would be **research-grade, comprehensive, and non-redundant** - capable of modeling virtually any health intervention and its pathways to outcomes.

---

**Document Version:** 1.0
**Created:** 2025-11-16
**Purpose:** Identify critical gaps for complete health system mapping
**Recommended Priority:** Implement Domain 1-3 first (167 nodes), then 4-6 (88 nodes), then 7-10 (71 nodes)
