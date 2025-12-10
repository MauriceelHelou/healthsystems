#!/usr/bin/env python3
"""
Generate Individual Node YAML Files

Creates YAML files for each node in the canonical inventory,
organized by scale in the nodes/by_scale/ directory structure.

Uses existing data where available and marks unknown fields as TBD.

Usage:
    # Generate all nodes from canonical inventory:
    python generate_node_yaml.py

    # Generate specific new nodes from a batch list:
    python generate_node_yaml.py --batch alcohol_nodes

    # List available batches:
    python generate_node_yaml.py --list-batches
"""

import json
import re
import yaml
import argparse
from pathlib import Path
from typing import Dict, Any, Optional, List
from collections import defaultdict

BASE_DIR = Path(__file__).parent.parent.parent
CANONICAL_NODES_PATH = BASE_DIR / 'nodes' / 'canonical_nodes.json'
DEDUP_MAP_PATH = BASE_DIR / 'backend' / 'reports' / 'node_deduplication_map.json'
OUTPUT_DIR = BASE_DIR / 'nodes' / 'by_scale'

# Scale directory names (1-7 scale per NODE_SYSTEM_DEFINITIONS.md)
SCALE_DIRS = {
    1: 'scale_1_structural_determinants',
    2: 'scale_2_built_environment',
    3: 'scale_3_institutional',
    4: 'scale_4_individual_household',
    5: 'scale_5_behaviors_psychosocial',
    6: 'scale_6_intermediate_pathways',
    7: 'scale_7_crisis_endpoints'
}

# Map domains to categories
DOMAIN_TO_CATEGORY = {
    'Healthcare System': 'healthcare_access',
    'Housing': 'built_environment',
    'Economic Security': 'economic',
    'Employment': 'economic',
    'Criminal Justice': 'social_environment',
    'Environmental': 'built_environment',
    'Behavioral Health': 'behavioral',
    'Education': 'social_environment',
    'Transportation': 'built_environment',
    'Food Systems': 'built_environment',
    'Social Support': 'social_environment',
    'Demographics': 'social_environment',
    'Biological': 'biological',
    'Policy': 'political',
    'Unknown': 'social_environment'
}

# Geographic variation heuristics by domain/type
GEO_VARIATION_HEURISTICS = {
    # Federal policies - uniform nationally
    'federal_policy': {'score': 1, 'level': 'federal'},
    # State policies - state variation
    'state_policy': {'score': 3, 'level': 'state'},
    # Local infrastructure - high variation
    'local_infrastructure': {'score': 4, 'level': 'county'},
    # Individual conditions - neighborhood variation
    'individual_condition': {'score': 4, 'level': 'neighborhood'},
    # Biomarkers - individual variation
    'biomarker': {'score': 5, 'level': 'neighborhood'},
    # Default
    'default': {'score': 3, 'level': 'state'}
}

# Data availability by domain
DATA_AVAILABILITY_HEURISTICS = {
    'Healthcare System': 'high',
    'Housing': 'moderate',
    'Economic Security': 'high',
    'Employment': 'high',
    'Criminal Justice': 'moderate',
    'Environmental': 'high',
    'Behavioral Health': 'moderate',
    'Education': 'high',
    'Transportation': 'moderate',
    'Food Systems': 'moderate',
    'Social Support': 'low',
    'Demographics': 'high',
    'Biological': 'moderate',
    'Policy': 'high',
    'Unknown': 'low'
}

# Common data sources by domain
DATA_SOURCES_BY_DOMAIN = {
    'Healthcare System': [
        {'name': 'CMS Medicare/Medicaid Data', 'granularity': 'county'},
        {'name': 'HRSA Area Health Resources Files', 'granularity': 'county'}
    ],
    'Housing': [
        {'name': 'Census Bureau ACS', 'granularity': 'tract'},
        {'name': 'HUD Housing Data', 'granularity': 'county'}
    ],
    'Economic Security': [
        {'name': 'Census Bureau ACS', 'granularity': 'tract'},
        {'name': 'Bureau of Labor Statistics', 'granularity': 'county'}
    ],
    'Employment': [
        {'name': 'Bureau of Labor Statistics', 'granularity': 'county'},
        {'name': 'Census Bureau ACS', 'granularity': 'tract'}
    ],
    'Criminal Justice': [
        {'name': 'Bureau of Justice Statistics', 'granularity': 'state'},
        {'name': 'Vera Institute of Justice', 'granularity': 'county'}
    ],
    'Environmental': [
        {'name': 'EPA Environmental Data', 'granularity': 'county'},
        {'name': 'CDC PLACES', 'granularity': 'tract'}
    ],
    'Behavioral Health': [
        {'name': 'SAMHSA NSDUH', 'granularity': 'state'},
        {'name': 'CDC BRFSS', 'granularity': 'state'}
    ],
    'Education': [
        {'name': 'NCES Education Statistics', 'granularity': 'county'},
        {'name': 'Census Bureau ACS', 'granularity': 'tract'}
    ],
    'Transportation': [
        {'name': 'DOT Transportation Data', 'granularity': 'county'},
        {'name': 'Census Bureau ACS', 'granularity': 'tract'}
    ],
    'Food Systems': [
        {'name': 'USDA Food Environment Atlas', 'granularity': 'county'},
        {'name': 'CDC BRFSS', 'granularity': 'state'}
    ],
    'Social Support': [
        {'name': 'Census Bureau ACS', 'granularity': 'tract'},
        {'name': 'CDC BRFSS', 'granularity': 'state'}
    ],
    'Demographics': [
        {'name': 'Census Bureau ACS', 'granularity': 'tract'},
        {'name': 'CDC WONDER', 'granularity': 'county'}
    ],
    'Biological': [
        {'name': 'NHANES', 'granularity': 'national'},
        {'name': 'CDC WONDER', 'granularity': 'county'}
    ],
    'Policy': [
        {'name': 'NCSL State Policy Database', 'granularity': 'state'},
        {'name': 'Federal Register', 'granularity': 'national'}
    ]
}

# Alcohol-specific data sources
ALCOHOL_DATA_SOURCES = [
    {'name': 'NIAAA Alcohol Policy Information System (APIS)', 'granularity': 'state'},
    {'name': 'SAMHSA NSDUH', 'granularity': 'state'},
    {'name': 'CDC BRFSS', 'granularity': 'state'},
    {'name': 'NHTSA FARS (fatalities)', 'granularity': 'state'}
]

# =============================================================================
# BATCH NODE DEFINITIONS
# =============================================================================
# Each batch is a list of node definitions that can be generated together.
# Format: {'id': str, 'name': str, 'scale': int, 'domain': str, 'type': str,
#          'unit': str, 'description': str (optional)}

BATCH_DEFINITIONS = {
    'alcohol_nodes': {
        'description': 'Alcohol-related nodes across all scales (mental health, trauma, social determinants)',
        'nodes': [
            # Scale 1 - Structural Determinants (Policy)
            {'id': 'mental_health_parity_enforcement', 'name': 'Mental Health Parity Enforcement', 'scale': 1,
             'domain': 'Policy', 'type': 'Policy', 'unit': 'enforcement index (0-100)',
             'description': 'Measures enforcement strength of Mental Health Parity and Addiction Equity Act. States with stronger enforcement have better access to SUD treatment. Key structural determinant affecting AUD treatment access.'},
            {'id': 'trauma_informed_care_policy', 'name': 'Trauma-Informed Care Policy', 'scale': 1,
             'domain': 'Policy', 'type': 'Policy', 'unit': 'policy adoption score (0-5)',
             'description': 'State-level adoption of trauma-informed care policies in healthcare and social services. Trauma is a major driver of alcohol misuse; TIC policies improve treatment engagement.'},
            {'id': 'workplace_drug_testing_policy', 'name': 'Workplace Drug Testing Policy', 'scale': 1,
             'domain': 'Policy', 'type': 'Policy', 'unit': 'policy stringency index',
             'description': 'State regulations on workplace drug/alcohol testing. Affects employment outcomes for people with AUD and may influence treatment-seeking behavior.'},
            {'id': 'naloxone_standing_order_policy', 'name': 'Naloxone Standing Order Policy', 'scale': 1,
             'domain': 'Policy', 'type': 'Policy', 'unit': 'binary (0=no, 1=yes)',
             'description': 'State policy allowing naloxone dispensing without individual prescription. Relevant to polysubstance use patterns often co-occurring with alcohol use disorder.'},
            {'id': 'social_host_liability_law', 'name': 'Social Host Liability Law', 'scale': 1,
             'domain': 'Policy', 'type': 'Policy', 'unit': 'liability strength (0-3)',
             'description': 'State laws holding social hosts liable for serving alcohol to minors or intoxicated persons. Reduces underage drinking and alcohol-related injuries at private events.'},
            {'id': 'happy_hour_regulation', 'name': 'Happy Hour Regulation', 'scale': 1,
             'domain': 'Policy', 'type': 'Policy', 'unit': 'restriction level (0-3)',
             'description': 'State/local regulations on alcohol price promotions including happy hours and drink specials. Price promotions increase consumption; regulations reduce binge drinking.'},

            # Scale 2 - Built Environment
            {'id': 'entertainment_district_density', 'name': 'Entertainment District Density', 'scale': 2,
             'domain': 'Environmental', 'type': 'Rate', 'unit': 'districts per 100,000 population',
             'description': 'Concentration of designated entertainment/nightlife districts. High density associated with increased alcohol availability and consumption in concentrated areas.'},
            {'id': 'college_campus_proximity', 'name': 'College Campus Proximity', 'scale': 2,
             'domain': 'Environmental', 'type': 'Exposure', 'unit': 'percent population within 1 mile',
             'description': 'Population proximity to college/university campuses. College environments associated with specific drinking cultures and elevated binge drinking rates.'},
            {'id': 'homeless_shelter_density', 'name': 'Homeless Shelter Density', 'scale': 2,
             'domain': 'Environmental', 'type': 'Rate', 'unit': 'beds per 10,000 population',
             'description': 'Availability of homeless shelter beds relative to population. Homelessness and AUD frequently co-occur; shelter access affects health outcomes for this population.'},
            {'id': 'halfway_house_availability', 'name': 'Halfway House Availability', 'scale': 2,
             'domain': 'Environmental', 'type': 'Rate', 'unit': 'beds per 10,000 population',
             'description': 'Availability of transitional housing for people in recovery. Critical infrastructure for maintaining sobriety after treatment completion.'},
            {'id': 'casino_gambling_venue_density', 'name': 'Casino/Gambling Venue Density', 'scale': 2,
             'domain': 'Environmental', 'type': 'Rate', 'unit': 'venues per 100,000 population',
             'description': 'Density of casinos and gambling establishments. Gambling venues typically serve alcohol and gambling disorder frequently co-occurs with AUD.'},

            # Scale 3 - Institutional Infrastructure
            {'id': 'peer_recovery_specialist_availability', 'name': 'Peer Recovery Specialist Availability', 'scale': 3,
             'domain': 'Healthcare System', 'type': 'Rate', 'unit': 'specialists per 100,000 population',
             'description': 'Availability of certified peer recovery specialists. Peers with lived experience improve treatment engagement and long-term recovery outcomes for AUD.'},
            {'id': 'medication_assisted_treatment_capacity', 'name': 'Medication-Assisted Treatment Capacity', 'scale': 3,
             'domain': 'Healthcare System', 'type': 'Rate', 'unit': 'treatment slots per 100,000 population',
             'description': 'Capacity for medication-assisted treatment for AUD including naltrexone, acamprosate, and disulfiram. MAT improves treatment outcomes but remains underutilized.'},
            {'id': 'crisis_stabilization_unit_beds', 'name': 'Crisis Stabilization Unit Beds', 'scale': 3,
             'domain': 'Healthcare System', 'type': 'Rate', 'unit': 'beds per 100,000 population',
             'description': 'Short-term crisis stabilization beds for acute psychiatric and substance use emergencies. Essential for managing severe alcohol withdrawal safely.'},
            {'id': 'dual_diagnosis_treatment_capacity', 'name': 'Dual Diagnosis Treatment Capacity', 'scale': 3,
             'domain': 'Healthcare System', 'type': 'Rate', 'unit': 'programs per 100,000 population',
             'description': 'Treatment programs addressing co-occurring mental health and substance use disorders. Majority of people with AUD have comorbid psychiatric conditions.'},
            {'id': 'employee_assistance_program_coverage', 'name': 'Employee Assistance Program Coverage', 'scale': 3,
             'domain': 'Healthcare System', 'type': 'Rate', 'unit': 'percent of workforce covered',
             'description': 'Proportion of workforce with access to Employee Assistance Programs. EAPs provide confidential early intervention for alcohol problems in workplace settings.'},
            {'id': 'drug_court_capacity', 'name': 'Drug Court Capacity', 'scale': 3,
             'domain': 'Criminal Justice', 'type': 'Rate', 'unit': 'slots per 100,000 population',
             'description': 'Capacity of drug/DUI court programs as alternative to incarceration. Courts connect people with treatment while maintaining accountability.'},
            {'id': 'school_based_prevention_program_coverage', 'name': 'School-Based Prevention Program Coverage', 'scale': 3,
             'domain': 'Education', 'type': 'Rate', 'unit': 'percent of schools with programs',
             'description': 'Coverage of evidence-based alcohol prevention programs in schools. Early prevention reduces initiation and delays onset of drinking.'},

            # Scale 4 - Individual/Household
            {'id': 'adverse_childhood_experiences_score', 'name': 'Adverse Childhood Experiences (ACEs) Score', 'scale': 4,
             'domain': 'Social Support', 'type': 'Rate', 'unit': 'mean ACE score (0-10)',
             'description': 'Population-level adverse childhood experiences including abuse, neglect, and household dysfunction. Strong dose-response relationship between ACEs and adult AUD.'},
            {'id': 'intimate_partner_violence_exposure', 'name': 'Intimate Partner Violence Exposure', 'scale': 4,
             'domain': 'Social Support', 'type': 'Rate', 'unit': 'percent experiencing IPV',
             'description': 'Prevalence of intimate partner violence exposure. Bidirectional relationship with alcohol: IPV increases drinking, alcohol increases IPV perpetration.'},
            {'id': 'job_loss_recent', 'name': 'Recent Job Loss', 'scale': 4,
             'domain': 'Employment', 'type': 'Rate', 'unit': 'percent experiencing job loss in past year',
             'description': 'Rate of recent involuntary job loss. Unemployment is a risk factor for increased alcohol consumption and development of AUD.'},
            {'id': 'social_isolation_index', 'name': 'Social Isolation Index', 'scale': 4,
             'domain': 'Social Support', 'type': 'Rate', 'unit': 'index score (0-100)',
             'description': 'Composite measure of social isolation including living alone, infrequent social contact, and lack of social participation. Isolation increases alcohol misuse risk.'},
            {'id': 'divorce_separation_status', 'name': 'Divorce/Separation Status', 'scale': 4,
             'domain': 'Demographics', 'type': 'Rate', 'unit': 'percent divorced or separated',
             'description': 'Rate of marital dissolution. Major life stressor associated with increased drinking; also consequence of problematic alcohol use.'},
            {'id': 'chronic_pain_prevalence', 'name': 'Chronic Pain Prevalence', 'scale': 4,
             'domain': 'Healthcare System', 'type': 'Rate', 'unit': 'percent with chronic pain',
             'description': 'Prevalence of chronic pain conditions. Chronic pain patients may self-medicate with alcohol; also risk factor for prescribed opioid misuse.'},
            {'id': 'sleep_disorder_prevalence', 'name': 'Sleep Disorder Prevalence', 'scale': 4,
             'domain': 'Behavioral Health', 'type': 'Rate', 'unit': 'percent with sleep disorders',
             'description': 'Prevalence of diagnosed or reported sleep disorders. Alcohol disrupts sleep architecture; people may use alcohol as sleep aid creating dependency.'},
            {'id': 'financial_stress_index', 'name': 'Financial Stress Index', 'scale': 4,
             'domain': 'Economic Security', 'type': 'Rate', 'unit': 'index score (0-100)',
             'description': 'Composite measure of financial stress including debt, inability to pay bills, and financial worry. Economic stress is a consistent predictor of increased drinking.'},

            # Scale 5 - Behaviors/Psychosocial
            {'id': 'social_drinking_frequency', 'name': 'Social Drinking Frequency', 'scale': 5,
             'domain': 'Behavioral Health', 'type': 'Behavior', 'unit': 'occasions per month',
             'description': 'Frequency of drinking in social settings. Normative social drinking patterns influence individual consumption and risk of escalation to problematic use.'},
            {'id': 'stress_coping_alcohol_use', 'name': 'Stress-Coping Alcohol Use', 'scale': 5,
             'domain': 'Behavioral Health', 'type': 'Behavior', 'unit': 'percent using alcohol to cope',
             'description': 'Prevalence of using alcohol as a coping mechanism for stress. Coping-motivated drinking is a risk factor for developing AUD.'},
            {'id': 'alcohol_expectancy_positive', 'name': 'Positive Alcohol Expectancies', 'scale': 5,
             'domain': 'Behavioral Health', 'type': 'Rate', 'unit': 'expectancy scale score',
             'description': 'Positive beliefs about alcohol effects (sociability, tension reduction). Higher positive expectancies predict greater consumption and problems.'},
            {'id': 'treatment_seeking_delay', 'name': 'Treatment-Seeking Delay', 'scale': 5,
             'domain': 'Behavioral Health', 'type': 'Rate', 'unit': 'mean years from problem onset to treatment',
             'description': 'Average delay between recognizing alcohol problem and seeking treatment. Stigma and other barriers create years-long delays in treatment entry.'},
            {'id': 'self_medication_behavior', 'name': 'Self-Medication Behavior', 'scale': 5,
             'domain': 'Behavioral Health', 'type': 'Behavior', 'unit': 'percent self-medicating',
             'description': 'Use of alcohol or other substances to manage mental health symptoms. Self-medication theory explains high comorbidity of AUD with anxiety and depression.'},
            {'id': 'depression_screening_positive', 'name': 'Depression Screening Positive', 'scale': 5,
             'domain': 'Behavioral Health', 'type': 'Rate', 'unit': 'percent screening positive (PHQ-9 >= 10)',
             'description': 'Prevalence of positive depression screening. Major depression and AUD frequently co-occur with bidirectional causal pathways.'},
            {'id': 'anxiety_disorder_prevalence', 'name': 'Anxiety Disorder Prevalence', 'scale': 5,
             'domain': 'Behavioral Health', 'type': 'Rate', 'unit': 'percent with anxiety disorder',
             'description': 'Prevalence of diagnosed anxiety disorders. Anxiety disorders are the most common psychiatric comorbidity with AUD.'},
            {'id': 'ptsd_prevalence', 'name': 'PTSD Prevalence', 'scale': 5,
             'domain': 'Behavioral Health', 'type': 'Rate', 'unit': 'percent with PTSD',
             'description': 'Prevalence of post-traumatic stress disorder. PTSD and AUD have 2-3x comorbidity; trauma exposure is a major pathway to alcohol misuse.'},

            # Scale 6 - Intermediate Pathways
            {'id': 'gamma_gt_elevated', 'name': 'Gamma-GT Elevated', 'scale': 6,
             'domain': 'Biological', 'type': 'Biomarker', 'unit': 'percent with elevated GGT (> 65 U/L)',
             'description': 'Prevalence of elevated gamma-glutamyl transferase. GGT is a sensitive biomarker for heavy alcohol use and liver damage.'},
            {'id': 'mean_corpuscular_volume_elevated', 'name': 'Mean Corpuscular Volume (MCV) Elevated', 'scale': 6,
             'domain': 'Biological', 'type': 'Biomarker', 'unit': 'percent with elevated MCV (> 100 fL)',
             'description': 'Prevalence of elevated MCV indicating macrocytosis. Chronic alcohol use causes vitamin B12 and folate deficiency leading to enlarged red blood cells.'},
            {'id': 'carbohydrate_deficient_transferrin', 'name': 'Carbohydrate-Deficient Transferrin (CDT)', 'scale': 6,
             'domain': 'Biological', 'type': 'Biomarker', 'unit': 'percent with elevated CDT (> 2.5%)',
             'description': 'CDT is a specific biomarker for heavy alcohol consumption over 2+ weeks. More specific than GGT for identifying chronic heavy drinking.'},
            {'id': 'alcohol_withdrawal_severity', 'name': 'Alcohol Withdrawal Severity', 'scale': 6,
             'domain': 'Biological', 'type': 'Rate', 'unit': 'mean CIWA-Ar score',
             'description': 'Average severity of alcohol withdrawal measured by Clinical Institute Withdrawal Assessment. Severe withdrawal (CIWA > 15) requires medical management.'},
            {'id': 'treatment_completion_rate', 'name': 'Treatment Completion Rate', 'scale': 6,
             'domain': 'Healthcare System', 'type': 'Rate', 'unit': 'percent completing treatment',
             'description': 'Proportion of patients completing SUD treatment programs. Treatment completion is a strong predictor of sustained recovery.'},
            {'id': 'thirty_day_abstinence_rate', 'name': '30-Day Abstinence Rate', 'scale': 6,
             'domain': 'Behavioral Health', 'type': 'Outcome', 'unit': 'percent abstinent at 30 days',
             'description': 'Proportion maintaining abstinence 30 days post-treatment. Early abstinence is a critical milestone predicting longer-term recovery.'},
            {'id': 'craving_intensity_score', 'name': 'Craving Intensity Score', 'scale': 6,
             'domain': 'Behavioral Health', 'type': 'Rate', 'unit': 'mean craving scale score (0-100)',
             'description': 'Average intensity of alcohol craving measured by validated scales. Craving intensity predicts relapse risk and guides treatment intensity.'},

            # Scale 7 - Crisis Endpoints
            {'id': 'alcoholic_hepatitis_hospitalization', 'name': 'Alcoholic Hepatitis Hospitalization', 'scale': 7,
             'domain': 'Healthcare System', 'type': 'Outcome', 'unit': 'hospitalizations per 100,000 population',
             'description': 'Rate of hospitalization for acute alcoholic hepatitis. Severe form of alcohol-related liver disease with high short-term mortality.'},
            {'id': 'pancreatitis_hospitalization_rate', 'name': 'Pancreatitis Hospitalization Rate', 'scale': 7,
             'domain': 'Healthcare System', 'type': 'Outcome', 'unit': 'hospitalizations per 100,000 population',
             'description': 'Rate of hospitalization for acute pancreatitis. Alcohol is the leading cause of chronic pancreatitis and second leading cause of acute pancreatitis.'},
            {'id': 'alcohol_related_motor_vehicle_fatality', 'name': 'Alcohol-Related Motor Vehicle Fatality', 'scale': 7,
             'domain': 'Healthcare System', 'type': 'Outcome', 'unit': 'deaths per 100,000 population',
             'description': 'Rate of motor vehicle fatalities involving alcohol-impaired driving. Leading cause of alcohol-attributable death among young adults.'},
            {'id': 'alcohol_induced_cardiomyopathy', 'name': 'Alcohol-Induced Cardiomyopathy', 'scale': 7,
             'domain': 'Healthcare System', 'type': 'Outcome', 'unit': 'cases per 100,000 population',
             'description': 'Incidence of cardiomyopathy attributed to chronic heavy alcohol use. Causes heart failure through direct toxic effects on cardiac muscle.'},
            {'id': 'alcohol_related_suicide_rate', 'name': 'Alcohol-Related Suicide Rate', 'scale': 7,
             'domain': 'Behavioral Health', 'type': 'Outcome', 'unit': 'deaths per 100,000 population',
             'description': 'Rate of suicide deaths with alcohol involvement. Alcohol present in approximately 25-50% of suicide deaths; AUD increases suicide risk 5-10x.'},
            {'id': 'alcohol_related_homicide_rate', 'name': 'Alcohol-Related Homicide Rate', 'scale': 7,
             'domain': 'Criminal Justice', 'type': 'Outcome', 'unit': 'deaths per 100,000 population',
             'description': 'Rate of homicide deaths with alcohol involvement. Alcohol involved in approximately 40% of homicides as risk factor for both perpetration and victimization.'},
            {'id': 'esophageal_varices_bleeding', 'name': 'Esophageal Varices Bleeding', 'scale': 7,
             'domain': 'Healthcare System', 'type': 'Outcome', 'unit': 'events per 100,000 population',
             'description': 'Rate of variceal bleeding events. Life-threatening complication of cirrhosis-related portal hypertension, commonly from alcohol-related liver disease.'},
        ]
    },
    'alcohol_nodes_expanded': {
        'description': 'Additional alcohol pathway nodes - protective factors, neurobiological, economic, and social determinants',
        'nodes': [
            # Scale 1 - More Policy Nodes
            {'id': 'alcohol_brief_intervention_mandate', 'name': 'Alcohol Brief Intervention Mandate', 'scale': 1,
             'domain': 'Policy', 'type': 'Policy', 'unit': 'mandate strength (0-3)',
             'description': 'State mandates requiring SBIRT (Screening, Brief Intervention, Referral to Treatment) in healthcare settings. Evidence-based approach for early identification and intervention.'},
            {'id': 'keg_registration_law', 'name': 'Keg Registration Law', 'scale': 1,
             'domain': 'Policy', 'type': 'Policy', 'unit': 'binary (0=no, 1=yes)',
             'description': 'Laws requiring registration of beer kegs to track purchaser. Reduces underage access to alcohol at parties and enables liability tracing.'},
            {'id': 'dram_shop_liability_law', 'name': 'Dram Shop Liability Law', 'scale': 1,
             'domain': 'Policy', 'type': 'Policy', 'unit': 'liability strength (0-3)',
             'description': 'Laws holding alcohol retailers liable for serving intoxicated persons or minors. Creates incentive for responsible serving practices.'},
            {'id': 'alcohol_ignition_interlock_mandate', 'name': 'Alcohol Ignition Interlock Mandate', 'scale': 1,
             'domain': 'Policy', 'type': 'Policy', 'unit': 'mandate coverage (0-3)',
             'description': 'Laws requiring ignition interlock devices for DUI offenders. Reduces repeat DUI offenses by preventing impaired driving.'},
            {'id': 'sunday_alcohol_sales_restriction', 'name': 'Sunday Alcohol Sales Restriction', 'scale': 1,
             'domain': 'Policy', 'type': 'Policy', 'unit': 'restriction level (0-2)',
             'description': 'Blue laws restricting alcohol sales on Sundays. Reduces availability and associated consumption; increasingly repealed in recent years.'},
            {'id': 'recovery_high_school_funding', 'name': 'Recovery High School Funding', 'scale': 1,
             'domain': 'Policy', 'type': 'Policy', 'unit': 'funding per capita',
             'description': 'State funding for recovery high schools serving students in substance use recovery. Supports academic continuation while maintaining sobriety.'},

            # Scale 2 - More Built Environment
            {'id': 'sober_living_home_density', 'name': 'Sober Living Home Density', 'scale': 2,
             'domain': 'Environmental', 'type': 'Rate', 'unit': 'beds per 10,000 population',
             'description': 'Availability of sober living environments providing peer-supported housing for people in recovery. Bridge between treatment and independent living.'},
            {'id': 'wet_shelter_availability', 'name': 'Wet Shelter Availability', 'scale': 2,
             'domain': 'Environmental', 'type': 'Rate', 'unit': 'beds per 10,000 homeless population',
             'description': 'Harm reduction shelters allowing alcohol consumption on-site. Serves chronically homeless with AUD who cannot access abstinence-based services.'},
            {'id': 'recovery_community_center_access', 'name': 'Recovery Community Center Access', 'scale': 2,
             'domain': 'Environmental', 'type': 'Rate', 'unit': 'centers per 100,000 population',
             'description': 'Community centers providing peer support, recovery meetings, and resources. Free, welcoming spaces supporting long-term recovery.'},
            {'id': 'sports_bar_density', 'name': 'Sports Bar Density', 'scale': 2,
             'domain': 'Environmental', 'type': 'Rate', 'unit': 'establishments per 10,000 population',
             'description': 'Concentration of sports bars and sports-themed drinking establishments. Associated with heavy episodic drinking during sporting events.'},
            {'id': 'drive_through_liquor_store_prevalence', 'name': 'Drive-Through Liquor Store Prevalence', 'scale': 2,
             'domain': 'Environmental', 'type': 'Rate', 'unit': 'stores per 100,000 population',
             'description': 'Availability of drive-through alcohol purchase. Increases accessibility and may facilitate impaired driving.'},

            # Scale 3 - More Institutional
            {'id': 'collegiate_recovery_program_availability', 'name': 'Collegiate Recovery Program Availability', 'scale': 3,
             'domain': 'Education', 'type': 'Rate', 'unit': 'programs per 100 colleges',
             'description': 'Campus-based recovery support programs for students in recovery. Enables continued education while maintaining sobriety in high-risk environment.'},
            {'id': 'workplace_eap_utilization_rate', 'name': 'Workplace EAP Utilization Rate', 'scale': 3,
             'domain': 'Healthcare System', 'type': 'Rate', 'unit': 'percent utilizing EAP services',
             'description': 'Rate of employee assistance program utilization for substance use concerns. Low utilization indicates stigma or awareness barriers.'},
            {'id': 'hospital_alcohol_detox_capacity', 'name': 'Hospital Alcohol Detox Capacity', 'scale': 3,
             'domain': 'Healthcare System', 'type': 'Rate', 'unit': 'beds per 100,000 population',
             'description': 'Medical detoxification capacity in hospital settings. Required for safe management of severe alcohol withdrawal (delirium tremens risk).'},
            {'id': 'addiction_psychiatry_workforce', 'name': 'Addiction Psychiatry Workforce', 'scale': 3,
             'domain': 'Healthcare System', 'type': 'Rate', 'unit': 'specialists per 100,000 population',
             'description': 'Availability of board-certified addiction psychiatrists. Subspecialty expertise for complex AUD with psychiatric comorbidities.'},
            {'id': 'faith_based_recovery_program_density', 'name': 'Faith-Based Recovery Program Density', 'scale': 3,
             'domain': 'Social Support', 'type': 'Rate', 'unit': 'programs per 100,000 population',
             'description': 'Availability of religious/spiritual recovery programs (Celebrate Recovery, etc.). Alternative pathway for those preferring faith-integrated treatment.'},
            {'id': 'alcohol_free_event_venue_availability', 'name': 'Alcohol-Free Event Venue Availability', 'scale': 3,
             'domain': 'Social Support', 'type': 'Rate', 'unit': 'venues per 100,000 population',
             'description': 'Availability of entertainment and social venues without alcohol service. Supports recovery-friendly socializing and sober nightlife alternatives.'},

            # Scale 4 - More Individual/Household
            {'id': 'veteran_status', 'name': 'Veteran Status', 'scale': 4,
             'domain': 'Demographics', 'type': 'Rate', 'unit': 'percent veteran population',
             'description': 'Proportion of population with military service history. Veterans have elevated AUD rates related to combat exposure, military culture, and PTSD.'},
            {'id': 'first_responder_occupation', 'name': 'First Responder Occupation', 'scale': 4,
             'domain': 'Employment', 'type': 'Rate', 'unit': 'percent employed as first responders',
             'description': 'Proportion employed as police, fire, EMS. First responders have elevated AUD risk from occupational trauma and cultural factors.'},
            {'id': 'hospitality_industry_employment', 'name': 'Hospitality Industry Employment', 'scale': 4,
             'domain': 'Employment', 'type': 'Rate', 'unit': 'percent employed in hospitality',
             'description': 'Employment in bars, restaurants, hotels. Hospitality workers have highest AUD rates of any occupation due to access and culture.'},
            {'id': 'childhood_parental_divorce', 'name': 'Childhood Parental Divorce', 'scale': 4,
             'domain': 'Social Support', 'type': 'Rate', 'unit': 'percent experiencing parental divorce',
             'description': 'History of parental divorce during childhood. ACE that increases risk of substance use disorders in adulthood.'},
            {'id': 'food_insecurity_rate', 'name': 'Food Insecurity Rate', 'scale': 4,
             'domain': 'Economic Security', 'type': 'Rate', 'unit': 'percent food insecure',
             'description': 'Household food insecurity prevalence. Paradoxically associated with AUD as stress response; also competes with resources for treatment.'},
            {'id': 'incarceration_history', 'name': 'Incarceration History', 'scale': 4,
             'domain': 'Criminal Justice', 'type': 'Rate', 'unit': 'percent with prior incarceration',
             'description': 'History of jail or prison incarceration. Strong bidirectional relationship with AUD; incarceration disrupts treatment continuity.'},
            {'id': 'multigenerational_household', 'name': 'Multigenerational Household', 'scale': 4,
             'domain': 'Demographics', 'type': 'Rate', 'unit': 'percent in multigenerational households',
             'description': 'Living in multigenerational households. Can be protective (family support) or risk factor (family drinking culture exposure).'},
            {'id': 'rural_residence', 'name': 'Rural Residence', 'scale': 4,
             'domain': 'Demographics', 'type': 'Rate', 'unit': 'percent rural population',
             'description': 'Rural vs urban residence. Rural areas have fewer treatment resources, higher stigma, but different drinking patterns than urban areas.'},

            # Scale 5 - More Behaviors/Psychosocial
            {'id': 'alcohol_use_disorder_stigma', 'name': 'Alcohol Use Disorder Stigma', 'scale': 5,
             'domain': 'Behavioral Health', 'type': 'Rate', 'unit': 'stigma index score',
             'description': 'Population-level stigma toward AUD measured by validated scales. Stigma is primary barrier to treatment-seeking and recovery support.'},
            {'id': 'drinking_refusal_self_efficacy', 'name': 'Drinking Refusal Self-Efficacy', 'scale': 5,
             'domain': 'Behavioral Health', 'type': 'Rate', 'unit': 'mean self-efficacy score',
             'description': 'Confidence in ability to refuse alcohol in high-risk situations. Protective factor and treatment target; predicts treatment success.'},
            {'id': 'recovery_capital_index', 'name': 'Recovery Capital Index', 'scale': 5,
             'domain': 'Behavioral Health', 'type': 'Rate', 'unit': 'index score (0-100)',
             'description': 'Composite measure of resources supporting recovery (social, physical, human, cultural capital). Higher recovery capital predicts sustained recovery.'},
            {'id': 'alcohol_use_normalization', 'name': 'Alcohol Use Normalization', 'scale': 5,
             'domain': 'Behavioral Health', 'type': 'Rate', 'unit': 'normalization score',
             'description': 'Degree to which heavy drinking is normalized in social networks. Social norms strongly influence consumption patterns and problem recognition.'},
            {'id': 'motivation_to_change_readiness', 'name': 'Motivation to Change Readiness', 'scale': 5,
             'domain': 'Behavioral Health', 'type': 'Rate', 'unit': 'readiness scale score',
             'description': 'Stage of change readiness for alcohol reduction. Treatment matching to readiness stage improves outcomes (motivational interviewing principles).'},
            {'id': 'prenatal_alcohol_use', 'name': 'Prenatal Alcohol Use', 'scale': 5,
             'domain': 'Behavioral Health', 'type': 'Rate', 'unit': 'percent of pregnancies with alcohol use',
             'description': 'Alcohol use during pregnancy. No safe amount; causes fetal alcohol spectrum disorders with lifelong neurodevelopmental consequences.'},
            {'id': 'concurrent_tobacco_use', 'name': 'Concurrent Tobacco Use', 'scale': 5,
             'domain': 'Behavioral Health', 'type': 'Rate', 'unit': 'percent with co-occurring tobacco use',
             'description': 'Concurrent alcohol and tobacco use prevalence. Synergistic health harms; tobacco use predicts poorer AUD treatment outcomes.'},
            {'id': 'concurrent_cannabis_use', 'name': 'Concurrent Cannabis Use', 'scale': 5,
             'domain': 'Behavioral Health', 'type': 'Rate', 'unit': 'percent with co-occurring cannabis use',
             'description': 'Concurrent alcohol and cannabis use. Increasingly common polysubstance pattern; may indicate different treatment needs.'},

            # Scale 6 - More Intermediate Pathways
            {'id': 'ast_alt_ratio_elevated', 'name': 'AST/ALT Ratio Elevated', 'scale': 6,
             'domain': 'Biological', 'type': 'Biomarker', 'unit': 'percent with ratio > 2.0',
             'description': 'Elevated AST/ALT ratio (De Ritis ratio). Ratio > 2 strongly suggests alcoholic liver disease over other hepatic conditions.'},
            {'id': 'thiamine_deficiency_rate', 'name': 'Thiamine Deficiency Rate', 'scale': 6,
             'domain': 'Biological', 'type': 'Biomarker', 'unit': 'percent with deficiency',
             'description': 'Prevalence of thiamine (vitamin B1) deficiency. Common in chronic alcoholism; causes Wernicke-Korsakoff syndrome if untreated.'},
            {'id': 'phosphatidylethanol_positive', 'name': 'Phosphatidylethanol (PEth) Positive', 'scale': 6,
             'domain': 'Biological', 'type': 'Biomarker', 'unit': 'percent PEth positive',
             'description': 'Direct alcohol biomarker with 3-4 week detection window. More sensitive and specific than traditional markers for monitoring abstinence.'},
            {'id': 'audit_c_positive_screen', 'name': 'AUDIT-C Positive Screen', 'scale': 6,
             'domain': 'Behavioral Health', 'type': 'Rate', 'unit': 'percent screening positive',
             'description': 'Positive screening on AUDIT-C (3-question alcohol screen). Standard primary care screening tool for hazardous drinking identification.'},
            {'id': 'alcohol_use_days_past_month', 'name': 'Alcohol Use Days Past Month', 'scale': 6,
             'domain': 'Behavioral Health', 'type': 'Rate', 'unit': 'mean days drinking per month',
             'description': 'Average number of drinking days in past 30 days. Treatment outcome measure; reduction indicates clinical improvement.'},
            {'id': 'heavy_drinking_days_past_month', 'name': 'Heavy Drinking Days Past Month', 'scale': 6,
             'domain': 'Behavioral Health', 'type': 'Rate', 'unit': 'mean heavy drinking days per month',
             'description': 'Average heavy drinking days (5+/4+ drinks men/women) per month. FDA-approved endpoint for AUD medication trials.'},
            {'id': 'one_year_recovery_rate', 'name': 'One-Year Recovery Rate', 'scale': 6,
             'domain': 'Healthcare System', 'type': 'Outcome', 'unit': 'percent in recovery at 1 year',
             'description': 'Proportion maintaining recovery at 1 year post-treatment. Key long-term outcome measure; 5 years recovery predicts lifetime stability.'},

            # Scale 7 - More Crisis Endpoints
            {'id': 'delirium_tremens_incidence', 'name': 'Delirium Tremens Incidence', 'scale': 7,
             'domain': 'Healthcare System', 'type': 'Outcome', 'unit': 'cases per 100,000 population',
             'description': 'Incidence of delirium tremens (severe alcohol withdrawal). Life-threatening condition with seizures, hallucinations; requires ICU management.'},
            {'id': 'alcohol_related_fall_injury', 'name': 'Alcohol-Related Fall Injury', 'scale': 7,
             'domain': 'Healthcare System', 'type': 'Outcome', 'unit': 'injuries per 100,000 population',
             'description': 'Fall injuries with alcohol involvement. Major cause of traumatic brain injury and hip fractures, especially in older adults.'},
            {'id': 'alcohol_related_drowning', 'name': 'Alcohol-Related Drowning', 'scale': 7,
             'domain': 'Healthcare System', 'type': 'Outcome', 'unit': 'deaths per 100,000 population',
             'description': 'Drowning deaths with alcohol involvement. Alcohol involved in 25-50% of drownings; impairs judgment, coordination, cold response.'},
            {'id': 'alcohol_related_fire_death', 'name': 'Alcohol-Related Fire Death', 'scale': 7,
             'domain': 'Healthcare System', 'type': 'Outcome', 'unit': 'deaths per 100,000 population',
             'description': 'Fire fatalities with alcohol involvement. Alcohol major factor in residential fire deaths due to impaired escape response.'},
            {'id': 'hepatorenal_syndrome_incidence', 'name': 'Hepatorenal Syndrome Incidence', 'scale': 7,
             'domain': 'Healthcare System', 'type': 'Outcome', 'unit': 'cases per 100,000 population',
             'description': 'Incidence of hepatorenal syndrome in alcoholic cirrhosis. Kidney failure secondary to advanced liver disease; very high mortality.'},
            {'id': 'spontaneous_bacterial_peritonitis', 'name': 'Spontaneous Bacterial Peritonitis', 'scale': 7,
             'domain': 'Healthcare System', 'type': 'Outcome', 'unit': 'cases per 100,000 population',
             'description': 'SBP incidence in cirrhotic patients. Serious infection of ascites fluid; common complication of alcoholic cirrhosis.'},
            {'id': 'alcohol_related_stroke', 'name': 'Alcohol-Related Stroke', 'scale': 7,
             'domain': 'Healthcare System', 'type': 'Outcome', 'unit': 'strokes per 100,000 population',
             'description': 'Stroke events attributable to alcohol use. Heavy drinking increases hemorrhagic stroke risk; moderate drinking effects debated.'},
            {'id': 'alcohol_related_cancer_mortality', 'name': 'Alcohol-Related Cancer Mortality', 'scale': 7,
             'domain': 'Healthcare System', 'type': 'Outcome', 'unit': 'deaths per 100,000 population',
             'description': 'Cancer deaths attributable to alcohol (oral, esophageal, liver, breast, colorectal). Alcohol is Group 1 carcinogen; no safe level for cancer.'},
        ]
    }
}


def normalize_node_id(text: str) -> str:
    """Normalize text to snake_case node ID."""
    if not text:
        return ""
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '_', text)
    text = re.sub(r'^_|_$', '', text)
    text = re.sub(r'_+', '_', text)
    return text


def estimate_geo_variation(node: Dict) -> Dict:
    """Estimate geographic variation based on node properties (1-7 scale system)."""
    node_type = node.get('type', 'Unknown')
    scale = node.get('scale', 4)  # Default to individual/household
    node_id = node.get('id', '')

    # Scale 1: Structural Determinants (federal/state policy)
    if scale == 1:
        if 'federal' in node_id:
            return {'score': 1, 'level': 'federal', 'notes': 'Federal policy - uniform across states'}
        return {'score': 2, 'level': 'state', 'notes': 'State-level policy variation'}

    # Scale 2: Built Environment & Infrastructure
    if scale == 2:
        return {'score': 4, 'level': 'county', 'notes': 'Physical infrastructure varies by region and locality'}

    # Scale 3: Institutional Infrastructure
    if scale == 3:
        return {'score': 3, 'level': 'county', 'notes': 'Varies by local healthcare/service infrastructure'}

    # Scale 4: Individual/Household Conditions
    if scale == 4:
        return {'score': 4, 'level': 'county', 'notes': 'Varies by local socioeconomic conditions'}

    # Scale 5: Individual Behaviors & Psychosocial
    if scale == 5:
        return {'score': 4, 'level': 'county', 'notes': 'Behavioral patterns vary by community and culture'}

    # Scale 6: Intermediate Pathways
    if scale == 6:
        if 'biomarker' in node_id or node_type == 'Biomarker':
            return {'score': 5, 'level': 'neighborhood', 'notes': 'Individual-level measurement, high local variation'}
        return {'score': 3, 'level': 'state', 'notes': 'Moderate regional variation in clinical measures'}

    # Scale 7: Crisis Endpoints
    if scale == 7:
        return {'score': 4, 'level': 'county', 'notes': 'Varies by local healthcare access and demographics'}

    return {'score': 3, 'level': 'state', 'notes': 'Moderate geographic variation expected'}


def estimate_data_quality(node: Dict) -> Dict:
    """Estimate data quality fields based on node properties."""
    domain = node.get('domain', 'Unknown')
    node_id = node.get('id', '')

    availability = DATA_AVAILABILITY_HEURISTICS.get(domain, 'low')

    # Frequency heuristic
    if 'rate' in node_id or 'mortality' in node_id:
        frequency = 'annual'
    elif 'policy' in node_id or 'status' in node_id:
        frequency = 'periodic'
    else:
        frequency = 'annual'

    # Bias notes
    if 'self_report' in node_id or 'survey' in node_id:
        bias_notes = 'Self-reported data may have recall bias and social desirability effects'
    elif 'rate' in node_id:
        bias_notes = 'Administrative data - may reflect reporting variations across jurisdictions'
    else:
        bias_notes = 'Standard survey/administrative data limitations apply'

    # Data sources
    if 'alcohol' in node_id or 'drinking' in node_id or 'aud' in node_id:
        sources = ALCOHOL_DATA_SOURCES.copy()
    else:
        sources = DATA_SOURCES_BY_DOMAIN.get(domain, [{'name': 'TBD', 'granularity': 'state'}])

    return {
        'availability': availability,
        'frequency': frequency,
        'bias_notes': bias_notes,
        'primary_sources': sources
    }


def generate_description(node: Dict) -> str:
    """Generate a description from node properties."""
    name = clean_field(node.get('name', node['id'].replace('_', ' ').title()))
    unit = clean_field(node.get('unit', 'TBD'))
    node_type = clean_field(node.get('type', 'Measure'))
    domain = clean_field(node.get('domain', 'health'))

    base = f"Measures {name.lower()}"

    if node_type == 'Policy':
        base = f"Policy indicator measuring {name.lower()}"
    elif node_type == 'Rate':
        base = f"Rate measure of {name.lower()}"
    elif node_type == 'Outcome':
        base = f"Health outcome measure: {name.lower()}"
    elif node_type == 'Behavior':
        base = f"Behavioral measure of {name.lower()}"

    # Add unit info
    if unit and unit != 'TBD':
        base += f". Measured in {unit}."
    else:
        base += "."

    # Add domain context
    base += f" Part of the {domain} domain."

    # Ensure minimum length
    if len(base) < 50:
        base += " This node tracks changes in health determinants across populations."

    return base


def clean_field(value: str) -> str:
    """Clean corrupted field data (e.g., 'Domain | **Unit:** ...')."""
    if not value or not isinstance(value, str):
        return value or 'Unknown'
    # Remove markdown artifacts and pipe-separated suffixes
    if '|' in value:
        value = value.split('|')[0].strip()
    if '**' in value:
        value = value.split('**')[0].strip()
    return value if value else 'Unknown'


def create_node_yaml(node: Dict) -> Dict[str, Any]:
    """Create a complete YAML structure for a node."""
    node_id = normalize_node_id(node.get('id', ''))
    name = clean_field(node.get('name', node_id.replace('_', ' ').title()))
    scale = node.get('scale', 4)  # Default to scale 4 (individual/household)
    domain = clean_field(node.get('domain', 'Unknown'))
    node_type = clean_field(node.get('type', 'Unknown'))
    unit = clean_field(node.get('unit', 'TBD'))

    # Map domain to category
    category = DOMAIN_TO_CATEGORY.get(domain, 'social_environment')

    # Estimate geographic variation
    geo_var = estimate_geo_variation(node)

    # Estimate data quality
    data_qual = estimate_data_quality(node)

    # Generate description
    description = generate_description(node)

    return {
        'id': node_id,
        'name': name,
        'scale': scale,
        'domain': domain,
        'category': category,
        'stock': {
            'value': 'TBD',
            'unit': unit,
            'year': 2024,
            'source': 'TBD - needs population from authoritative source'
        },
        'geographic_variation': geo_var,
        'data_quality': data_qual,
        'description': description,
        'type': node_type if node_type != 'Unknown' else 'Rate'
    }


def load_nodes_to_generate() -> list:
    """Load nodes from deduplication map or canonical file."""
    # Try dedup map first
    if DEDUP_MAP_PATH.exists():
        with open(DEDUP_MAP_PATH, 'r') as f:
            dedup_data = json.load(f)
        nodes_to_keep = dedup_data.get('mapping', {}).get('keep', {})
        return list(nodes_to_keep.values())

    # Fall back to canonical nodes
    with open(CANONICAL_NODES_PATH, 'r') as f:
        data = json.load(f)
    return data['nodes']


def write_yaml_file(node_data: Dict, output_path: Path):
    """Write a single node YAML file with nice formatting."""

    # Custom YAML representer for multi-line strings
    def str_representer(dumper, data):
        if '\n' in data or len(data) > 80:
            return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')
        return dumper.represent_scalar('tag:yaml.org,2002:str', data)

    yaml.add_representer(str, str_representer)

    with open(output_path, 'w', encoding='utf-8') as f:
        yaml.dump(node_data, f,
                  default_flow_style=False,
                  allow_unicode=True,
                  sort_keys=False,
                  width=100)


def generate_batch_nodes(batch_name: str, dry_run: bool = False) -> tuple[int, List[Dict]]:
    """
    Generate node YAML files from a batch definition.

    Args:
        batch_name: Name of the batch to generate (e.g., 'alcohol_nodes')
        dry_run: If True, only print what would be created without writing files

    Returns:
        Tuple of (count of nodes created, list of errors)
    """
    if batch_name not in BATCH_DEFINITIONS:
        print(f"ERROR: Batch '{batch_name}' not found.")
        print(f"Available batches: {', '.join(BATCH_DEFINITIONS.keys())}")
        return 0, [{'error': f'Batch {batch_name} not found'}]

    batch = BATCH_DEFINITIONS[batch_name]
    print("=" * 70)
    print(f"GENERATING BATCH: {batch_name}")
    print("=" * 70)
    print(f"Description: {batch['description']}")
    print(f"Nodes to generate: {len(batch['nodes'])}")

    if dry_run:
        print("\n[DRY RUN - No files will be created]")

    # Create output directories
    print("\n1. Creating directory structure...")
    for scale, dirname in SCALE_DIRS.items():
        dir_path = OUTPUT_DIR / dirname
        dir_path.mkdir(parents=True, exist_ok=True)

    # Generate YAML files
    print("\n2. Generating YAML files...")
    counts = defaultdict(int)
    errors = []
    skipped = 0

    for node in batch['nodes']:
        try:
            node_data = create_node_yaml(node)
            scale = node_data['scale']

            # Ensure valid scale (1-7)
            if scale not in SCALE_DIRS:
                scale = 4  # Default to scale 4
                node_data['scale'] = scale

            # Use custom description if provided
            if node.get('description'):
                node_data['description'] = node['description']

            # Output path
            scale_dir = SCALE_DIRS[scale]
            output_path = OUTPUT_DIR / scale_dir / f"{node_data['id']}.yaml"

            # Check if file already exists
            if output_path.exists():
                print(f"   SKIP (exists): {node_data['id']}")
                skipped += 1
                continue

            if dry_run:
                print(f"   WOULD CREATE: {output_path.relative_to(OUTPUT_DIR)}")
            else:
                write_yaml_file(node_data, output_path)
                print(f"   CREATED: {node_data['id']} (scale {scale})")

            counts[scale] += 1

        except Exception as e:
            errors.append({'node': node.get('id', 'unknown'), 'error': str(e)})
            print(f"   ERROR: {node.get('id', 'unknown')} - {e}")

    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    total = sum(counts.values())
    print(f"   Total nodes {'would be ' if dry_run else ''}created: {total}")
    print(f"   Skipped (already exist): {skipped}")

    print("\n   By scale:")
    for scale in sorted(counts.keys()):
        scale_name = SCALE_DIRS.get(scale, f'scale_{scale}')
        print(f"   - {scale_name}: {counts[scale]} nodes")

    if errors:
        print(f"\n   Errors: {len(errors)}")
        for err in errors[:10]:
            print(f"   - {err['node']}: {err['error']}")

    print(f"\n   Output directory: {OUTPUT_DIR}")

    return total, errors


def list_batches():
    """List all available batch definitions."""
    print("=" * 70)
    print("AVAILABLE BATCH DEFINITIONS")
    print("=" * 70)
    for name, batch in BATCH_DEFINITIONS.items():
        print(f"\n  {name}:")
        print(f"    Description: {batch['description']}")
        print(f"    Node count: {len(batch['nodes'])}")

        # Count by scale
        scale_counts = defaultdict(int)
        for node in batch['nodes']:
            scale_counts[node.get('scale', 4)] += 1

        print("    By scale:")
        for scale in sorted(scale_counts.keys()):
            print(f"      Scale {scale}: {scale_counts[scale]} nodes")


def main():
    parser = argparse.ArgumentParser(
        description='Generate node YAML files from canonical inventory or batch definitions',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python generate_node_yaml.py                    # Generate all canonical nodes
  python generate_node_yaml.py --batch alcohol_nodes  # Generate alcohol batch
  python generate_node_yaml.py --batch alcohol_nodes --dry-run  # Preview
  python generate_node_yaml.py --list-batches     # List available batches
        """
    )
    parser.add_argument('--batch', type=str, help='Generate nodes from a specific batch definition')
    parser.add_argument('--dry-run', action='store_true', help='Preview changes without creating files')
    parser.add_argument('--list-batches', action='store_true', help='List available batch definitions')

    args = parser.parse_args()

    if args.list_batches:
        list_batches()
        return 0

    if args.batch:
        total, errors = generate_batch_nodes(args.batch, dry_run=args.dry_run)
        return 1 if errors else 0

    # Default: generate all nodes from canonical inventory
    print("=" * 70)
    print("GENERATING NODE YAML FILES (from canonical inventory)")
    print("=" * 70)

    # Load nodes
    print("\n1. Loading nodes...")
    nodes = load_nodes_to_generate()
    print(f"   Nodes to generate: {len(nodes)}")

    # Create output directories
    print("\n2. Creating directory structure...")
    for scale, dirname in SCALE_DIRS.items():
        dir_path = OUTPUT_DIR / dirname
        dir_path.mkdir(parents=True, exist_ok=True)
        print(f"   Created: {dir_path}")

    # Generate YAML files
    print("\n3. Generating YAML files...")
    counts = defaultdict(int)
    errors = []

    for node in nodes:
        try:
            node_data = create_node_yaml(node)
            scale = node_data['scale']

            # Ensure valid scale (1-7)
            if scale not in SCALE_DIRS:
                scale = 4  # Default to scale 4 (individual/household)
                node_data['scale'] = scale

            # Output path
            scale_dir = SCALE_DIRS[scale]
            output_path = OUTPUT_DIR / scale_dir / f"{node_data['id']}.yaml"

            # Write file
            write_yaml_file(node_data, output_path)
            counts[scale] += 1

        except Exception as e:
            errors.append({'node': node.get('id', 'unknown'), 'error': str(e)})

    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    total = sum(counts.values())
    print(f"   Total YAML files generated: {total}")
    print("\n   By scale:")
    for scale in sorted(counts.keys()):
        scale_name = SCALE_DIRS.get(scale, f'scale_{scale}')
        print(f"   - {scale_name}: {counts[scale]} nodes")

    if errors:
        print(f"\n   Errors: {len(errors)}")
        for err in errors[:10]:
            print(f"   - {err['node']}: {err['error']}")

    print(f"\n   Output directory: {OUTPUT_DIR}")

    return 1 if errors else 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
