# Topic Configuration Guide

This directory contains topic-specific configuration files for the generic mechanism extraction pipeline.

## Overview

The generic extraction pipeline allows you to extract causal mechanisms for any health topic by:
1. Defining node pairs (from → to) relevant to the topic
2. Specifying query templates for literature search
3. Configuring output directories and metadata

## File Structure

Each topic has its own YAML configuration file:

```
backend/config/topic_configs/
├── obesity.yaml
├── diabetes.yaml
├── mental_health.yaml
├── cardiovascular.yaml
├── respiratory.yaml
└── your_topic.yaml
```

## Configuration Format

```yaml
topic: your_topic_name

query_template: |
  Identify causal mechanisms linking {from_node} to {to_node} in the context of [your topic].

  Focus on:
  - [Key aspect 1]
  - [Key aspect 2]
  - [Key aspect 3]

  Provide evidence from peer-reviewed literature, prioritizing meta-analyses and systematic reviews.

from_nodes:
  - upstream_factor_1
  - upstream_factor_2
  - structural_determinant_1
  # ... list all source nodes

to_nodes:
  - downstream_outcome_1
  - intermediate_pathway_1
  - health_outcome_1
  # ... list all target nodes

scales:
  - 1  # Structural (policy, laws)
  - 2  # Built environment
  - 3  # Institutional
  - 4  # Individual conditions
  - 5  # Behaviors
  - 6  # Intermediate pathways
  - 7  # Health outcomes

output_dir: mechanism-bank/mechanisms/your_topic

notes: |
  Optional notes about the topic, key considerations, or special instructions.
```

## Required Fields

- **topic**: Short name for the topic (e.g., "obesity", "diabetes")
- **query_template**: Template for literature search queries
  - Use `{from_node}` and `{to_node}` as placeholders
  - Use `{topic}` if you want to reference the topic name
- **from_nodes**: List of source/upstream node IDs
- **to_nodes**: List of target/downstream node IDs

## Optional Fields

- **scales**: List of scale levels (1-7) to prioritize
- **output_dir**: Custom output directory (defaults to `mechanism-bank/mechanisms/{topic}`)
- **notes**: Additional context or instructions

## Node Naming Conventions

Use **snake_case** for node IDs:
- ✅ `housing_quality`, `food_insecurity`, `type_2_diabetes`
- ❌ `HousingQuality`, `food-insecurity`, `Type 2 Diabetes`

## Query Template Guidelines

1. **Be specific about the topic context**
   - ✅ "in the context of obesity"
   - ❌ "in health research"

2. **List key pathways or mechanisms to focus on**
   - Biological pathways
   - Environmental factors
   - Social determinants
   - Structural factors

3. **Request specific evidence types**
   - Meta-analyses
   - Systematic reviews
   - RCTs
   - Longitudinal cohorts

4. **Use placeholders correctly**
   - `{from_node}` → replaced with source node ID
   - `{to_node}` → replaced with target node ID
   - `{topic}` → replaced with topic name

## Scale Definitions

The 7-level scale represents causal distance from structural determinants to health outcomes:

1. **Structural**: Policy, laws, regulations, taxation, government programs
2. **Built Environment**: Housing, neighborhood, infrastructure, walkability
3. **Institutional**: Healthcare system, schools, workplaces, organizations
4. **Individual Conditions**: SES, employment, insurance, education
5. **Behaviors**: Diet, physical activity, smoking, medication adherence
6. **Intermediate Pathways**: Biological markers, inflammation, metabolic factors
7. **Health Outcomes**: Disease, mortality, hospitalization, crisis events

## Creating a New Topic Config

1. **Copy an existing config** (e.g., `obesity.yaml`) as a template
2. **Update the topic name** to match your new topic
3. **Define node pairs**:
   - List upstream factors (structural, environmental, social)
   - List downstream outcomes (intermediate pathways, health outcomes)
4. **Customize the query template**:
   - Specify key mechanisms or pathways
   - Mention relevant evidence types
5. **Test with dry run**:
   ```bash
   python backend/scripts/run_generic_extraction.py --topic your_topic --dry-run
   ```

## Example: Creating a "Cancer" Config

```yaml
topic: cancer

query_template: |
  Identify causal mechanisms linking {from_node} to {to_node} in the context of cancer prevention and outcomes.

  Focus on:
  - Environmental carcinogen exposure
  - Behavioral risk factors (smoking, diet, physical activity)
  - Healthcare access and screening
  - Socioeconomic determinants
  - Treatment access and quality

  Provide evidence from oncology research, prioritizing meta-analyses and large cohort studies.

from_nodes:
  - smoking
  - air_pollution
  - occupational_exposures
  - ultraviolet_radiation
  - alcohol_consumption
  - obesity
  - physical_inactivity
  - healthcare_access
  - screening_rates
  - socioeconomic_status

to_nodes:
  - lung_cancer
  - breast_cancer
  - colorectal_cancer
  - skin_cancer
  - cancer_mortality
  - cancer_stage_at_diagnosis
  - treatment_delay
  - cancer_recurrence

scales:
  - 1  # Structural (policy)
  - 2  # Environmental exposures
  - 3  # Healthcare system
  - 4  # Individual risk factors
  - 5  # Behaviors
  - 6  # Biological pathways
  - 7  # Cancer outcomes

output_dir: mechanism-bank/mechanisms/cancer
```

## Usage Examples

### Single Topic Extraction

```bash
# Extract mechanisms for obesity
python backend/scripts/run_generic_extraction.py --topic obesity

# Extract only structural-level mechanisms (scales 1-3)
python backend/scripts/run_generic_extraction.py --topic diabetes --scales 1,2,3

# Dry run to see query count
python backend/scripts/run_generic_extraction.py --topic mental_health --dry-run
```

### Batch Extraction

```bash
# Extract multiple topics in parallel
python backend/scripts/batch_topic_extraction.py --topics obesity,diabetes,mental_health

# Limit concurrent extractions
python backend/scripts/batch_topic_extraction.py --topics cardiovascular,respiratory --max-concurrent 2
```

### Custom Configuration

```bash
# Use a custom config file
python backend/scripts/run_generic_extraction.py --config path/to/custom_config.yaml

# Override nodes from config
python backend/scripts/run_generic_extraction.py --topic obesity \
  --from-nodes "food_environment,built_environment" \
  --to-nodes "obesity_prevalence,bmi_continuous"
```

## Best Practices

1. **Start with a small node set** to test
   - Use 5-10 from_nodes and 5-10 to_nodes
   - Run dry-run to estimate query count
   - Scale up after validating results

2. **Use structural competency lens**
   - Focus on upstream determinants (policy, environment)
   - Avoid individual blame ("poor health behaviors")
   - Emphasize root causes over proximate factors

3. **Prioritize high-quality evidence**
   - Request meta-analyses and systematic reviews in query template
   - Filter by minimum citations (default: 10)
   - Review extracted mechanisms for quality

4. **Organize by category**
   - Mechanisms are automatically saved to category subdirectories
   - Categories: built_environment, social_environment, economic, political, healthcare_access, biological, behavioral

5. **Monitor API costs**
   - Each paper abstract requires a Claude API call (~$0.01-0.05)
   - Estimate: 100 queries × 10 papers/query = 1000 API calls = $10-50
   - Use `--limit` to reduce papers per query during testing

## Troubleshooting

### Config not found

```
FileNotFoundError: No config found for topic 'your_topic'
```

**Solution**: Create `backend/config/topic_configs/your_topic.yaml`

### Too many queries

```
Dry run shows 10,000+ queries
```

**Solution**: Reduce node pairs or filter by scale:
```bash
python backend/scripts/run_generic_extraction.py --topic your_topic --scales 1,2
```

### API rate limits

If you hit rate limits, reduce `--limit` or `--max-concurrent`:
```bash
python backend/scripts/run_generic_extraction.py --topic your_topic --limit 5
```

## Support

For questions or issues:
1. Check existing topic configs for examples
2. Review [run_generic_extraction.py](../../scripts/run_generic_extraction.py) documentation
3. Open an issue in the repository
