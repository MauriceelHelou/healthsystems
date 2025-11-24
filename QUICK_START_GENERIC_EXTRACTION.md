# Quick Start: Generic Mechanism Extraction

## Prerequisites

```bash
# 1. Install dependencies
pip install -r backend/requirements.txt

# 2. Set API key in .env file
echo "ANTHROPIC_API_KEY=your-key-here" >> .env

# 3. Verify setup
python backend/scripts/run_generic_extraction.py --topic obesity --dry-run
```

## 5-Minute Quick Start

### Option 1: Run Example Script

```bash
# Run guided example extraction (small test)
python backend/scripts/example_generic_extraction.py
```

This will:
- Extract mechanisms for 3x3 node pairs
- Validate structural competency
- Demonstrate Bayesian weighting
- Show quality metrics

### Option 2: Extract Single Topic

```bash
# Dry run to see query count
python backend/scripts/run_generic_extraction.py --topic obesity --dry-run

# Small test (3 papers per query)
python backend/scripts/run_generic_extraction.py --topic obesity --limit 3

# Full extraction (10 papers per query)
python backend/scripts/run_generic_extraction.py --topic obesity
```

### Option 3: Batch Extract Multiple Topics

```bash
# Extract 3 topics in parallel
python backend/scripts/batch_topic_extraction.py \
  --topics obesity,diabetes,mental_health \
  --limit 5 \
  --save-report
```

## Available Topics

Pre-configured topics ready to use:

| Topic | From Nodes | To Nodes | Est. Queries |
|-------|------------|----------|--------------|
| **obesity** | 20 | 17 | 320 |
| **diabetes** | 20 | 18 | 340 |
| **mental_health** | 20 | 19 | 361 |
| **cardiovascular** | 20 | 18 | 340 |
| **respiratory** | 20 | 18 | 340 |

## Common Commands

### Test Before Running

```bash
# See how many queries will be generated
python backend/scripts/run_generic_extraction.py --topic TOPIC --dry-run
```

### Filter by Scale

```bash
# Extract only structural determinants (scales 1-3)
python backend/scripts/run_generic_extraction.py --topic TOPIC --scales 1,2,3
```

### Reduce Cost/Time

```bash
# Fewer papers per query (faster, cheaper)
python backend/scripts/run_generic_extraction.py --topic TOPIC --limit 3

# Filter by recent years only
# Edit config file: year_range in run_extraction()
```

### Custom Nodes

```bash
# Override node lists from config
python backend/scripts/run_generic_extraction.py --topic TOPIC \
  --from-nodes "node1,node2,node3" \
  --to-nodes "outcome1,outcome2,outcome3"
```

## Output

Extracted mechanisms are saved to:
```
mechanism-bank/mechanisms/{topic}/{category}/{mechanism_id}.yml
```

Example:
```
mechanism-bank/mechanisms/obesity/
├── built_environment/
│   └── food_environment_to_obesity_prevalence.yml
├── economic/
│   └── socioeconomic_status_to_diet_quality.yml
└── behavioral/
    └── physical_activity_to_bmi_continuous.yml
```

## Validation

Check extracted mechanisms:

```bash
# Run validation script
python backend/scripts/validate_mechanisms.py

# Check confidence scores in YAML files (llm_metadata section)
# Look for: extraction_confidence: high/medium/low
```

## Creating a New Topic

1. **Copy template**:
```bash
cp backend/config/topic_configs/obesity.yaml \
   backend/config/topic_configs/your_topic.yaml
```

2. **Edit config**:
   - Update `topic:` name
   - Customize `query_template:`
   - Define `from_nodes:` (upstream factors)
   - Define `to_nodes:` (health outcomes)

3. **Test**:
```bash
python backend/scripts/run_generic_extraction.py --topic your_topic --dry-run
```

4. **Run**:
```bash
python backend/scripts/run_generic_extraction.py --topic your_topic --limit 5
```

## Troubleshooting

### "No config found for topic"
- Create config file: `backend/config/topic_configs/{topic}.yaml`
- See: [backend/config/topic_configs/README.md](backend/config/topic_configs/README.md)

### "ANTHROPIC_API_KEY not set"
- Add to `.env` file: `ANTHROPIC_API_KEY=sk-ant-...`
- Or use: `--api-key` flag

### Too many queries (>1000)
- Reduce node pairs in config
- Use `--scales 1,2,3` to filter
- Use `--from-nodes` and `--to-nodes` to override

### Rate limit errors
- Reduce `--max-concurrent` (batch script)
- Reduce `--limit` (papers per query)
- Add delays between queries

### No mechanisms extracted
- Papers may not contain causal mechanisms
- Try broader query terms
- Check different node pairs
- Review query template

## Cost Estimates

| Scenario | Queries | Papers | API Calls | Est. Cost |
|----------|---------|--------|-----------|-----------|
| **Small test** | 10 | 30 | ~30 | $1-$5 |
| **Single topic (limited)** | 50 | 250 | ~250 | $5-$25 |
| **Single topic (full)** | 300 | 3000 | ~3000 | $30-$150 |
| **Batch 5 topics** | 1500 | 15000 | ~15000 | $150-$750 |

Reduce costs:
- Use `--limit 3` (instead of default 10)
- Filter by `--scales`
- Start with small node sets
- Use `--dry-run` to estimate

## Next Steps

1. ✅ Run example script to test workflow
2. ⬜ Extract one topic with `--limit 3`
3. ⬜ Review extracted mechanisms
4. ⬜ Adjust query template if needed
5. ⬜ Run full extraction or batch
6. ⬜ Validate and load to database

## Documentation

- **Full implementation guide**: [GENERIC_EXTRACTION_IMPLEMENTATION.md](GENERIC_EXTRACTION_IMPLEMENTATION.md)
- **Topic config guide**: [backend/config/topic_configs/README.md](backend/config/topic_configs/README.md)
- **Bayesian weighting docs**: [backend/algorithms/bayesian_weighting.py](backend/algorithms/bayesian_weighting.py)

## Support

- Review existing configs for examples
- Check error messages for specific issues
- Open issue on GitHub for bugs/questions
