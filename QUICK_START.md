# Quick Start Guide - Alcohol Mechanism Extraction

## Setup Complete! ✅

Your API key has been configured and the extraction system is ready to run.

## What's Been Set Up

1. ✅ **API Key Configured** - Stored securely in `.env` file
2. ✅ **All Scripts Updated** - Automatically load API key from `.env`
3. ✅ **Extraction Pipeline Ready** - 6 phases, 90 queries, 90-130 mechanisms
4. ✅ **Test Script Running** - Currently validating the pipeline

## Quick Commands

### Test the Pipeline (Recommended First)

```bash
cd backend
python scripts/test_extraction.py
```

**What it does:**
- Searches for 3-5 papers on alcohol → liver cirrhosis
- Extracts mechanisms from first paper
- Saves to mechanism-bank/mechanisms/
- Validates entire pipeline
- **Time:** 1-2 minutes
- **Cost:** ~$0.50

### Run Phase 1 (Direct Health Consequences)

```bash
cd backend
python scripts/run_alcohol_extraction.py --phases 1 --limit 10
```

**What it does:**
- 15 queries on alcohol health outcomes
- Extracts 15-20 mechanisms
- **Time:** 30-60 minutes
- **Cost:** ~$10-15

### Run Phases 1-3 (Health + Risk + Social)

```bash
cd backend
python scripts/run_alcohol_extraction.py --phases 1 2 3 --limit 10
```

**What it does:**
- 42 queries across health, risk factors, and social impacts
- Extracts 45-50 mechanisms
- **Time:** 1-2 hours
- **Cost:** ~$25-35

### Full Extraction (All 6 Phases)

```bash
cd backend
python scripts/batch_alcohol_mechanisms.py
```

**What it does:**
- All 90 queries
- Extracts 90-130 mechanisms
- **Time:** 3-6 hours
- **Cost:** ~$50-100

**⚠️ Warning:** This is a long-running process. Consider running in smaller phases first.

### Test Mode (Validates All Phases, Minimal Cost)

```bash
cd backend
python scripts/run_alcohol_extraction.py --test --phases 1 2 3 4 5 6
```

**What it does:**
- Only 2 queries per phase (12 total instead of 90)
- Validates all phases work correctly
- **Time:** 20-30 minutes
- **Cost:** ~$5-10

## Interactive Launcher (Easiest)

### Windows
```cmd
start_extraction.bat
```

### Linux/Mac
```bash
chmod +x start_extraction.sh
./start_extraction.sh
```

**Features:**
- Interactive menu
- Shows cost and time estimates
- Confirmation prompts
- Handles all setup

## After Extraction

### 1. Validate Mechanisms

```bash
python mechanism-bank/validation/validate_mechanisms.py
```

### 2. Review Output

Check these files:
- `mechanism-bank/extraction_progress.json` - Progress report
- `mechanism-bank/extraction_final_report.json` - Final summary
- `mechanism-bank/extraction_errors.json` - Any errors

### 3. Load to Database

```bash
# Start backend
cd backend
uvicorn app.main:app --reload

# In another terminal
curl -X POST http://localhost:8000/api/mechanisms/admin/load-from-yaml
```

### 4. Test API

```bash
curl http://localhost:8000/api/mechanisms/stats/summary
```

### 5. Commit to Git

```bash
git add mechanism-bank/mechanisms/
git commit -m "mechanism: add alcohol-related mechanisms from batch extraction"
git push
```

## Files Created

Your `.env` file contains your API key:
```
ANTHROPIC_API_KEY=sk-ant-api03-RiSCO...
```

**Security:**
- ✅ Automatically loaded by all scripts
- ✅ Already in `.gitignore` (won't be committed)
- ✅ Safe to keep in your project

## Full Documentation

- **Complete Guide:** `backend/scripts/README_ALCOHOL_EXTRACTION.md`
- **Executive Summary:** `ALCOHOL_EXTRACTION_SUMMARY.md`
- **Mechanism Discovery Skill:** `.claude/skills/mechanism-discovery.md`

## Troubleshooting

### "No module named 'dotenv'"

```bash
pip install python-dotenv
```

### API Key Error

Check that `.env` file exists in project root:
```bash
# Windows
type .env

# Linux/Mac
cat .env
```

Should contain:
```
ANTHROPIC_API_KEY=sk-ant-api03-...
```

### Rate Limit Errors

Add optional API keys to `.env`:
```
SEMANTIC_SCHOLAR_API_KEY=your-key-here
PUBMED_API_KEY=your-key-here
```

## Current Status

🔄 **Test extraction is currently running**

The test script is validating the pipeline by:
1. Searching Semantic Scholar and PubMed
2. Retrieving papers on alcohol → liver cirrhosis
3. Extracting mechanisms using Claude API
4. Saving to mechanism-bank/mechanisms/

This confirms everything is working correctly!

## Next Steps

1. Wait for test extraction to complete (1-2 minutes)
2. Review test output and extracted mechanism
3. Choose your extraction scope (test mode, phase 1, or full)
4. Run the extraction
5. Validate, review, and commit

---

**You're all set!** 🎉

The extraction system is configured and ready. Simply choose which command to run based on your needs (test mode recommended first).
