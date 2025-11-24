# Alcohol Mechanism Extraction - Implementation Summary

**Date:** 2025-01-19
**Status:** Ready to Execute
**Prepared by:** Claude Code

---

## Executive Summary

I've created a comprehensive batch extraction system to discover and formalize 90-130 alcohol-related mechanisms from academic literature. The system is fully implemented and ready to run.

### What Was Created

✅ **Literature Search Pipeline** - Integrated Semantic Scholar + PubMed APIs
✅ **LLM Extraction Pipeline** - Claude-powered mechanism discovery
✅ **Batch Processing Scripts** - 6-phase extraction workflow
✅ **Validation System** - Schema compliance checking
✅ **Easy-to-use Launchers** - Windows (.bat) and Linux/Mac (.sh)
✅ **Comprehensive Documentation** - README with full instructions

---

## Current State Analysis

### Existing Mechanisms
- **Total:** 21 alcohol-related mechanisms
- **Coverage:** Strong on upstream determinants, weak on health outcomes
- **Gap:** 90-130 additional mechanisms needed

### Network Coverage Gaps

**1-Hop Direct Connections:**
- ❌ Missing ~15-20 health consequences (liver, cardiovascular, injuries, suicide)
- ❌ Missing ~18 risk factors (anxiety, PTSD, pain, discrimination, homelessness)
- ❌ Missing ~10 social consequences (IPV, child neglect, incarceration)
- ❌ Missing ~12 protective mechanisms (MAT, SBIRT, taxation, outlet restrictions)

**2-Hop Indirect Chains:**
- ❌ Missing ~20-30 connecting mechanisms (eviction→housing→AUD, alcohol→HTN→CVD)

**3-Hop Structural Pathways:**
- ❌ Missing ~15-20 policy mechanisms (Medicaid→insurance→treatment)

---

## Implementation Details

### File Structure

```
healthsystems/
├── backend/
│   ├── pipelines/
│   │   ├── llm_mechanism_discovery.py        [Existing - MVP topology extraction]
│   │   └── literature_search.py               [Existing - Semantic Scholar + PubMed]
│   └── scripts/
│       ├── batch_alcohol_mechanisms.py        [NEW - Main batch extractor]
│       ├── run_alcohol_extraction.py          [NEW - Simplified runner]
│       ├── test_extraction.py                 [NEW - Pipeline validator]
│       └── README_ALCOHOL_EXTRACTION.md       [NEW - Complete guide]
├── start_extraction.bat                       [NEW - Windows launcher]
├── start_extraction.sh                        [NEW - Linux/Mac launcher]
└── ALCOHOL_EXTRACTION_SUMMARY.md              [This file]
```

### Six Extraction Phases

#### Phase 1: Direct Health Consequences
**Queries:** 15
**Expected Mechanisms:** 15-20
**Examples:**
- Alcohol → Liver cirrhosis
- Alcohol → Hypertension
- Alcohol → Falls/injuries
- Alcohol → Motor vehicle crashes
- Alcohol → Suicide
- Alcohol → Cancer (liver, breast, esophageal, colorectal)
- Alcohol → Cardiomyopathy
- Alcohol → Pancreatitis
- Alcohol → GI bleeding
- Alcohol → Cognitive impairment/dementia

#### Phase 2: Missing Risk Factors
**Queries:** 17
**Expected Mechanisms:** 20-25
**Examples:**
- Anxiety disorders → Alcohol (self-medication)
- PTSD/trauma → Alcohol
- Chronic pain → Alcohol
- Sleep disorders → Alcohol
- Discrimination → Chronic stress → Alcohol
- IPV exposure → PTSD → Alcohol
- Homelessness → Alcohol
- Incarceration → Post-release alcohol
- Alcohol outlet density → Consumption
- Alcohol marketing → Youth initiation

#### Phase 3: Social/Behavioral Consequences
**Queries:** 10
**Expected Mechanisms:** 10-15
**Examples:**
- Alcohol → IPV perpetration
- Alcohol → Child neglect/abuse
- Alcohol → Criminal justice involvement
- Alcohol → Homelessness (direct pathway)
- Alcohol → Social isolation
- Alcohol → Medication non-adherence
- Alcohol → Sexual risk behaviors/STIs
- Alcohol → Relationship dissolution

#### Phase 4: Protective/Treatment Mechanisms
**Queries:** 14
**Expected Mechanisms:** 12-15
**Examples:**
- Medication for AUD (naltrexone, acamprosate) → Recovery
- SBIRT (Screening & Brief Intervention) → Reduced drinking
- Mental health treatment → Reduced self-medication
- Social support networks → Prevention
- Employment stability → Reduced alcohol misuse
- Housing stability → Reduced alcohol misuse
- Alcohol pricing/taxation → Reduced consumption
- Outlet density restrictions → Reduced access
- Workplace EAP → Early treatment

#### Phase 5: Two-Hop Chains
**Queries:** 14
**Expected Mechanisms:** 20-30
**Examples:**
- Eviction → Housing instability → AUD
- Unaffordable housing → Rent burden → AUD
- Alcohol → Liver disease → Transplant need
- Alcohol → Hypertension → Stroke/MI
- Alcohol → Falls → Hip fracture → Disability
- Alcohol → Unemployment → Poverty → Homelessness
- Provider shortage → Untreated mental health → Alcohol
- Discrimination → Chronic stress → Health outcomes

#### Phase 6: Three-Hop Structural Pathways
**Queries:** 10
**Expected Mechanisms:** 15-20
**Examples:**
- Medicaid expansion → Insurance coverage → Treatment access
- Minimum wage policy → Poverty reduction → Health
- Housing policy (zoning) → Rent burden → Health
- Mass incarceration → Family disruption → ACEs → AUD
- Education funding → Educational attainment → Employment → Health
- Mental health parity → Treatment coverage → Access → Outcomes

---

## How to Run

### Quick Start (Recommended)

**Windows:**
```cmd
start_extraction.bat
```

**Linux/Mac:**
```bash
chmod +x start_extraction.sh
./start_extraction.sh
```

Both launchers provide an interactive menu:
1. Test extraction (validates pipeline with single query)
2. Run Phase 1 only (~15-20 mechanisms, 30-60 min, $10-15)
3. Run Phases 1-3 (~45-50 mechanisms, 1-2 hours, $25-35)
4. Run ALL phases (~90-130 mechanisms, 3-6 hours, $50-100)
5. Test mode (2 queries per phase, validates all phases, $5-10)

### Prerequisites

**Required:**
```bash
export ANTHROPIC_API_KEY="your-key-here"
```

**Optional (for higher rate limits):**
```bash
export SEMANTIC_SCHOLAR_API_KEY="your-key-here"  # 10x higher limit
export PUBMED_EMAIL="your-email@example.com"     # Recommended by NCBI
export PUBMED_API_KEY="your-key-here"            # 10 req/sec vs 3 req/sec
```

### Manual Execution

**Test pipeline:**
```bash
cd backend
python scripts/test_extraction.py
```

**Run specific phases:**
```bash
cd backend
python scripts/run_alcohol_extraction.py --phases 1 2 3 --limit 10
```

**Full extraction:**
```bash
cd backend
python scripts/batch_alcohol_mechanisms.py
```

---

## Expected Output

### Mechanisms by Category

After complete extraction:

| Category | Current | After Extraction | Total |
|----------|---------|------------------|-------|
| Behavioral | 5 | +15-20 | 20-25 |
| Biological | 9 | +20-25 | 29-34 |
| Built Environment | 26 | +5-10 | 31-36 |
| Economic | 8 | +10-15 | 18-23 |
| Healthcare Access | 8 | +15-20 | 23-28 |
| Political | 6 | +10-15 | 16-21 |
| Social Environment | 8 | +15-20 | 23-28 |
| **TOTAL** | **70** | **+90-125** | **160-195** |

### Progress Tracking

During extraction, the system generates:

1. **`mechanism-bank/extraction_progress.json`** - Updated after each phase
   - Phases completed
   - Mechanisms extracted
   - Papers processed
   - Errors encountered

2. **`mechanism-bank/extraction_final_report.json`** - Final summary
   - Total duration
   - Total papers
   - Total mechanisms
   - Per-phase breakdown

3. **`mechanism-bank/extraction_errors.json`** - Error log
   - Papers that failed to process
   - Extraction errors
   - Schema validation errors

### YAML Mechanism Files

Each mechanism saved as: `{from_node_id}_to_{to_node_id}.yml`

Example structure:
```yaml
id: alcohol_use_disorder_to_liver_cirrhosis
name: Alcohol Use Disorder → Liver Cirrhosis
from_node:
  node_id: alcohol_use_disorder
  node_name: Alcohol Use Disorder
to_node:
  node_id: liver_cirrhosis
  node_name: Liver Cirrhosis
direction: positive
category: biological
mechanism_pathway:
  - Step 1: Chronic alcohol exposure causes hepatocyte damage
  - Step 2: Inflammation triggers stellate cell activation
  - Step 3: Collagen deposition leads to fibrosis
  - Step 4: Progressive fibrosis develops into cirrhosis
  - Step 5: Portal hypertension and liver failure ensue
evidence:
  quality_rating: A
  n_studies: 12
  primary_citation: "Citation in Chicago style..."
  doi: "10.xxxx/xxxxx"
moderators:
  - name: drinking_pattern
    direction: strengthens
    strength: strong
    description: "Binge drinking accelerates progression..."
structural_competency:
  equity_implications: "Access to addiction treatment..."
llm_metadata:
  extracted_by: claude-sonnet-4-20250514
  extraction_confidence: high
last_updated: 2025-01-19
version: 1.0
```

---

## Validation & Quality Control

### Automated Validation

After extraction, run:
```bash
python mechanism-bank/validation/validate_mechanisms.py
```

Checks:
- ✅ JSON schema compliance
- ✅ Required fields present
- ✅ Valid category values
- ✅ CI ordering (lower < upper)
- ✅ Evidence quality tiers (A/B/C) match study counts
- ✅ Citations include DOI or URL
- ✅ Date formats valid

### Manual Review Checklist

For each mechanism:
- [ ] Pathway description is clear and stepwise
- [ ] Direction is correct (positive/negative)
- [ ] Category assignment is appropriate
- [ ] Evidence quality tier is justified
- [ ] Moderators have clear rationale
- [ ] Citations are complete and accurate
- [ ] Structural competency alignment (traces to policy/systems, not individual blame)
- [ ] Equity implications are explicit

### Common Issues

**Schema Violations:**
- Missing required fields → Add manually
- Invalid category → Change to valid enum value
- CI ordering wrong → Fix confidence intervals
- Missing DOI → Add from paper or use URL

**Extraction Errors:**
- No abstract available → Paper skipped automatically
- LLM extraction failure → Logged in errors.json, review manually
- Rate limit hit → Script includes delays, should auto-recover

---

## Integration with System

### Load to Database

```bash
# Start backend
cd backend
uvicorn app.main:app --reload

# Load mechanisms
curl -X POST http://localhost:8000/api/mechanisms/admin/load-from-yaml
```

Response:
```json
{
  "mechanisms_loaded": 95,
  "errors": []
}
```

### Test API Endpoints

```bash
# Get all mechanisms
curl http://localhost:8000/api/mechanisms/

# Filter by category
curl http://localhost:8000/api/mechanisms/?category=biological

# Search pathways
curl "http://localhost:8000/api/mechanisms/search/pathway?from_node=alcohol_use_disorder&to_node=liver_disease_mortality"

# Get statistics
curl http://localhost:8000/api/mechanisms/stats/summary
```

### Update Frontend

The **AlcoholismSystemView** will automatically include new mechanisms if:
1. Mechanisms are loaded to database
2. Node IDs match the alcoholism filter criteria
3. Frontend is refreshed

May need to update `frontend/src/utils/alcoholismFilter.ts` to include new node IDs.

### Run Tests

```bash
cd backend
pytest tests/test_mechanisms_api.py -v
```

---

## Cost & Time Estimates

### API Costs

| Source | Cost |
|--------|------|
| Semantic Scholar | Free |
| PubMed | Free |
| Anthropic Claude | $50-100 for full extraction |

**Claude API breakdown:**
- ~300-500 papers
- ~4000 tokens per extraction (input + output)
- ~1.2-2M total tokens
- Input: $3/M tokens
- Output: $15/M tokens
- **Total: $50-100**

### Time Estimates

| Phase | Time |
|-------|------|
| Literature search | 30-60 min |
| Mechanism extraction | 2-4 hours |
| Validation | 30 min |
| Manual review | 2-3 hours |
| **Total** | **5-8 hours** |

**Note:** Most time is automated API calls. You can start the extraction and let it run unattended.

---

## Git Workflow

### After Extraction

```bash
# Check what was created
git status

# Stage new mechanisms
git add mechanism-bank/mechanisms/

# Commit by phase (recommended)
git commit -m "mechanism: add Phase 1 alcohol health consequences (20 mechanisms)

- Direct health outcomes: liver disease, cardiovascular, injuries, suicide, cancer
- Evidence quality: Tier A (12 meta-analyses, 8 systematic reviews)
- Sources: 45 papers from Semantic Scholar and PubMed (2010-2024)
- LLM-assisted extraction using claude-sonnet-4-20250514

Mechanisms added:
- alcohol_use_disorder_to_liver_cirrhosis
- alcohol_use_disorder_to_hypertension
- alcohol_intoxication_to_falls_injuries
- alcohol_intoxication_to_motor_vehicle_crashes
- alcohol_use_disorder_to_suicide_attempts
- chronic_alcohol_use_to_cancer_incidence
- alcoholic_cardiomyopathy_to_heart_failure
[... and 13 more]

🤖 Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>"

# Repeat for each phase
```

### Commit Strategy

**Option 1: One commit per phase** (Recommended)
- Easier to review
- Can cherry-pick if needed
- Clear progression

**Option 2: Single commit for all**
- Simpler git history
- Use detailed commit message with phase breakdown

**Option 3: One commit per mechanism**
- Maximum granularity
- Tedious for 90+ mechanisms
- Only for critical review needs

---

## Troubleshooting

### API Key Not Found

**Error:** `ANTHROPIC_API_KEY environment variable not set`

**Solution:**
```bash
# Windows
set ANTHROPIC_API_KEY=your-key-here

# Linux/Mac
export ANTHROPIC_API_KEY=your-key-here

# Permanent (add to ~/.bashrc or ~/.zshrc)
echo 'export ANTHROPIC_API_KEY="your-key-here"' >> ~/.bashrc
source ~/.bashrc
```

### Rate Limit Errors

**Error:** Too many requests to Semantic Scholar or PubMed

**Solutions:**
1. Script includes automatic delays (1s for S2, 0.5s for PubMed)
2. Set API keys for higher limits:
   - `SEMANTIC_SCHOLAR_API_KEY` → 10x higher limit
   - `PUBMED_API_KEY` → 10 req/sec vs 3 req/sec
3. Reduce `limit_per_query` parameter

### Extraction Fails

**Error:** LLM extraction fails for a paper

**What happens:**
- Error logged to `extraction_errors.json`
- Script continues with next paper
- No data loss

**To fix:**
- Review error log after completion
- Can manually extract from failed papers
- Or re-run extraction for that specific paper

### Validation Errors

**Error:** Mechanism fails schema validation

**Common causes:**
- Missing required field
- Invalid category value
- CI ordering wrong (lower ≥ upper)
- Missing DOI/URL in citation

**To fix:**
- Read error message from validator
- Edit YAML file manually
- Re-run validation

### No Papers Found

**Error:** Search returns 0 papers for a query

**Possible causes:**
1. Internet connection issue
2. API endpoint down
3. Query too specific
4. Year range too restrictive
5. Citation threshold too high

**Solutions:**
- Check internet connection
- Try broader query
- Reduce `min_citations` threshold
- Expand `year_range`

---

## Next Steps

### Immediate (Before Running)

1. ✅ Set `ANTHROPIC_API_KEY` environment variable
2. ✅ Read `backend/scripts/README_ALCOHOL_EXTRACTION.md`
3. ✅ Decide which phases to run (test first recommended)
4. ✅ Check available API credits

### During Extraction

1. Monitor progress in console output
2. Check `extraction_progress.json` periodically
3. Let script run unattended (3-6 hours for full extraction)
4. Don't interrupt - script saves progress after each phase

### After Extraction

1. ✅ Run validation: `python mechanism-bank/validation/validate_mechanisms.py`
2. ✅ Review `extraction_final_report.json`
3. ✅ Check `extraction_errors.json` for any failures
4. ✅ Manually review extracted mechanisms
5. ✅ Fix any validation errors
6. ✅ Load to database and test API
7. ✅ Run backend tests
8. ✅ Update frontend if needed
9. ✅ Commit to git
10. ✅ Update documentation

### Future Enhancements (Phase 2)

1. Add quantitative effect sizes (currently MVP topology only)
2. Implement meta-analysis pooling across studies
3. Add uncertainty quantification
4. Create mechanism variants for different contexts
5. Build mechanism recommendation system
6. Develop automated literature monitoring
7. Create mechanism visualization tools

---

## Support & Documentation

### Documentation Files

1. **`backend/scripts/README_ALCOHOL_EXTRACTION.md`** - Comprehensive extraction guide
2. **`ALCOHOL_EXTRACTION_SUMMARY.md`** - This file (executive summary)
3. **`mechanism-bank/README.md`** - Mechanism bank overview
4. **`docs/Core Technical Architecture/05_MECHANISM_BANK_STRUCTURE.md`** - Architecture details
5. **`.claude/skills/mechanism-discovery.md`** - Mechanism discovery skill guide

### Getting Help

If you encounter issues:
1. Check error messages in console output
2. Review `extraction_errors.json`
3. Consult README troubleshooting section
4. Check backend logs
5. Verify all dependencies installed: `pip install -r backend/requirements.txt`

---

## Success Metrics

### Quantitative

- [ ] **90-130 new mechanisms** extracted
- [ ] **≥90% validation pass** rate
- [ ] **≥80% confidence** ratings (high/medium)
- [ ] **≥60% Tier A/B** evidence quality
- [ ] **100% citations** include DOI or URL

### Qualitative

- [ ] Comprehensive coverage of 1-hop connections
- [ ] Critical 2-hop chains documented
- [ ] Structural pathways (3-hop) included
- [ ] Structural competency maintained throughout
- [ ] Equity implications explicit
- [ ] Ready for systems modeling and policy analysis

---

## Conclusion

The alcohol mechanism extraction system is **fully implemented and ready to execute**. The infrastructure provides:

✅ Automated literature search across multiple databases
✅ LLM-powered mechanism extraction with structural competency
✅ Schema validation and quality control
✅ Progress tracking and error handling
✅ Easy-to-use launchers for all platforms
✅ Comprehensive documentation

**To begin extraction, simply run:**
- Windows: `start_extraction.bat`
- Linux/Mac: `./start_extraction.sh`

Or test first with: `python backend/scripts/test_extraction.py`

The system will guide you through the process with an interactive menu.

---

**Prepared by:** Claude Code
**Date:** 2025-01-19
**Version:** 1.0
**Status:** ✅ Ready to Execute
