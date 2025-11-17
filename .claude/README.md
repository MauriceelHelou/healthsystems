# HealthSystems Platform - Claude Code Customizations

This directory contains custom slash commands, skills, MCP servers, and configurations designed specifically for the HealthSystems Platform development workflow.

## 🎯 Quick Start

### Phase 1 Foundation - Available Now

The following tools are ready to use:

1. **`/mechanism`** - Mechanism bank management
2. **`/test-stack`** - Multi-tier test orchestration
3. **`/docs-sync`** - Documentation synchronization
4. **MCP Servers** - Academic literature & public health data APIs
5. **Skills** - Mechanism discovery, structural competency, equity lens

---

## 📚 Slash Commands

### `/mechanism` - Mechanism Bank Management

Comprehensive tool for creating, validating, and managing causal mechanisms.

**Sub-commands:**

```bash
/mechanism create [intervention] -> [outcome]
```
Interactive AI-assisted wizard to create new mechanism YAML files:
- Literature search via MCP servers
- Effect size extraction
- Moderator identification
- Schema validation
- Git version control

**Example:**
```bash
/mechanism create housing quality -> respiratory health
```

---

```bash
/mechanism validate [file]
```
Run validation scripts on mechanism YAML files.

**Example:**
```bash
/mechanism validate housing_quality_respiratory_v1.yaml
```

---

```bash
/mechanism search <query>
```
Search mechanism bank by keywords, interventions, outcomes, or moderators.

**Example:**
```bash
/mechanism search housing
/mechanism search mental health outcomes
```

---

```bash
/mechanism version <file>
```
Bump mechanism version and commit with proper git tracking.

**Example:**
```bash
/mechanism version housing_quality_respiratory_v1.yaml
```

---

```bash
/mechanism lineage <id>
```
Show full version history and provenance of a mechanism.

**Example:**
```bash
/mechanism lineage housing_quality_respiratory_v1
```

---

### `/test-stack` - Multi-Tier Test Orchestration

Intelligent test runner across backend (pytest), frontend (Jest), and mechanism validation.

**Usage:**

```bash
/test-stack              # Run all test suites
/test-stack all          # Same as above
/test-stack backend      # Backend tests only
/test-stack frontend     # Frontend tests only
/test-stack mechanisms   # Mechanism validation only
/test-stack changed      # Smart: only test what changed (git detection)
/test-stack quick        # Fast: unit tests only, skip integration
```

**Features:**
- Environment detection (checks Docker services)
- Unified coverage reporting
- Intelligent test selection based on git changes
- Accessibility testing (frontend)
- Bayesian model testing

**Example output:**
```
═══════════════════════════════════════════════════════════
HEALTHSYSTEMS TEST SUITE RESULTS
═══════════════════════════════════════════════════════════

Backend (pytest)
✓ 127 passed, 0 failed, 2 skipped
✓ Coverage: 84.3% (target: 80%)
⏱ Duration: 12.4s

Frontend (Jest)
✓ 89 passed, 0 failed
✓ Coverage: 87.1%
✓ Accessibility: All tests passed
⏱ Duration: 8.7s

Mechanisms (validation)
✓ 12 mechanisms validated
⏱ Duration: 0.3s

═══════════════════════════════════════════════════════════
OVERALL: ✓ ALL TESTS PASSED
Total: 228 tests in 21.4s
═══════════════════════════════════════════════════════════
```

---

### `/docs-sync` - Documentation Synchronization

Generate and update documentation from code.

**Usage:**

```bash
/docs-sync              # Check all documentation
/docs-sync all          # Generate/update all docs
/docs-sync api          # Generate API documentation from FastAPI
/docs-sync mechanisms   # Generate mechanism catalog
/docs-sync architecture # Update architecture docs
/docs-sync check        # Detect gaps without updating
```

**Features:**
- Auto-generate API reference from FastAPI routes
- Create mechanism catalog from YAML bank
- Detect outdated documentation
- Validate cross-references
- Multi-tier doc support (technical, scientific, user-facing)

---

## 🤖 MCP Servers

MCP (Model Context Protocol) servers provide external data access for AI-assisted workflows.

### Academic Literature Server

**Purpose:** Search academic databases for literature synthesis.

**Capabilities:**
- Semantic Scholar API - comprehensive academic search
- CrossRef API - DOI metadata and citations
- PubMed - biomedical literature
- Effect size extraction
- Chicago-style citation generation

**Domains allowed:**
- `api.semanticscholar.org`
- `api.crossref.org`
- `eutils.ncbi.nlm.nih.gov`
- `pubmed.ncbi.nlm.nih.gov`

**Usage:**
When using `/mechanism create`, the AI will automatically search academic literature via this server to find effect sizes and supporting evidence.

### Public Health Data Server

**Purpose:** Access Census, CDC, EPA, and BLS data APIs.

**Capabilities:**
- Census API - demographics, ACS variables
- CDC WONDER - health outcomes, mortality
- EPA - environmental data
- BLS - labor statistics

**Domains allowed:**
- `api.census.gov`
- `data.cdc.gov`
- `wonder.cdc.gov`
- `api.bls.gov`
- `edg.epa.gov`

**Setup:**
Some APIs require free API keys:
1. Census API: https://api.census.gov/data/key_signup.html
2. BLS API: https://data.bls.gov/registrationEngine/

(MCP servers will work without keys but with rate limits)

### GitHub Server

**Purpose:** Repository operations, issues, pull requests.

**Usage:**
Automatically available for git operations within Claude Code.

---

## 🎓 Skills

Skills are specialized AI capabilities for complex workflows.

### Mechanism Discovery Skill

**Purpose:** End-to-end literature synthesis → mechanism creation workflow.

**Workflow:**
1. Literature search (via MCP servers)
2. Effect size extraction
3. Moderator identification
4. YAML generation with schema validation
5. Quality assessment
6. Version control

**Invoked by:** `/mechanism create` command

**Key features:**
- Meta-analytic pooling of effect sizes
- Structural competency enforcement
- Equity considerations
- Evidence quality tiering (A/B/C)

### Structural Competency Skill

**Purpose:** Ensure alignment with structural determinants framework.

**Reviews:**
- Mechanisms (intervention framing, moderators, outcomes)
- Code (data models, API endpoints, UI)
- Documentation (language, examples)

**Checks for:**
- Scale classification (structural/institutional vs. individual)
- Avoidance of victim-blaming language
- Structural framing of moderators
- Policy/resource focus

**Red flags:**
- Individual responsibility language ("compliance", "motivation")
- Biological race explanations
- "Cultural factors" without structural context

### Equity Lens Skill

**Purpose:** Systematic equity analysis for all features.

**Reviews:**
- Baseline disparities (with structural context)
- Differential effects (stratified by race, income, geography)
- Disparity impact (quantified reduction/exacerbation)
- Implementation equity (access barriers, safeguards)

**Outputs:**
- Disparity reduction calculations
- Equity impact rating (high/moderate/low/negative)
- Implementation recommendations
- Harm assessment

---

## 📋 Prompt Templates

Reusable templates for common tasks.

### `prompts/mechanism-review.md`

Comprehensive checklist for reviewing mechanisms:
- Schema validation
- Effect size plausibility
- Evidence quality assessment
- Moderator justification
- Structural competency alignment
- Equity considerations
- Citation completeness

### `prompts/test-generation.md`

Templates for generating comprehensive tests:
- Backend: API endpoints, services, Bayesian models, database models
- Frontend: Components, hooks, integration tests
- Accessibility testing patterns
- Coverage requirements (≥80%)

### `prompts/equity-analysis.md`

Structured template for equity analysis:
- Baseline disparity documentation
- Differential effects analysis
- Disparity impact calculation
- Implementation equity assessment
- Power & resources analysis
- Equity-centered recommendations

---

## ⚙️ Configuration

### Permissions (`settings.local.json`)

Enhanced permissions for development workflow:

**Allowed commands:**
- File operations: `ls`, `find`
- Git operations: `add`, `commit`, `status`, `diff`, `log`
- Docker: `ps`, `docker-compose ps`
- Testing: `pytest`, `npm test`
- Mechanism validation: `python mechanism-bank/scripts/validate_mechanisms.py`

These commands can be run without confirmation prompts.

---

## 🚀 Usage Examples

### Example 1: Create New Mechanism

```bash
User: /mechanism create minimum wage -> food security

Claude: I'll help you create a mechanism linking minimum wage to food security.

Let me search the academic literature for effect sizes...

[Searches via Academic Literature MCP server]

📚 Found 8 relevant papers:

[1] Averett et al. (2017) - Quasi-experimental study
    "The Effect of Minimum Wages on SNAP Enrollments"
    Effect: 10% wage increase → 8.7% reduction in SNAP enrollment

[2] Lenhart (2019) - Panel data analysis
    "The Effects of State-Level Minimum Wage on Household Poverty"
    Effect: $1 increase → 2.4% poverty reduction

[3] Dube (2019) - Meta-analysis
    "Minimum Wages and the Distribution of Family Incomes"
    Effect: 10% wage increase → 5-10% food insecurity reduction

Select papers to include (e.g., "1,3"): 1,2,3

[Extracts effect sizes, generates mechanism YAML with moderators]

Generated mechanism:
- Effect size: -0.075 log ratio (7.5% reduction in food insecurity)
- 95% CI: [-0.12, -0.03]
- Quality tier: A (meta-analysis + supporting studies)
- 12 moderators identified (policy environment, demographic, geographic, implementation)

[Runs schema validation]
✓ Schema validation passed

[Equity analysis]
⚖️ Equity Impact: Disparity-reducing
- Larger absolute benefit in low-income communities
- Estimated 18% disparity reduction

Ready to commit? (y/n): y

[Commits to git]
✓ Committed: mechanism-bank/mechanisms/minimum_wage_food_security_v1.yaml
```

---

### Example 2: Run Tests Before Committing

```bash
User: /test-stack changed

Claude: Detecting changed files...

📊 Detected changes:
- backend/app/services/bayesian_weighting.py
- backend/tests/test_bayesian_weighting.py
- frontend/src/components/MechanismCard.tsx

🎯 Running targeted tests:

Backend:
✓ pytest tests/test_bayesian_weighting.py (15 tests, 2.1s)

Frontend:
✓ npm test -- MechanismCard (8 tests, 1.3s)
✓ Accessibility: No violations

Results: All tests passed ✓
```

---

### Example 3: Sync Documentation

```bash
User: /docs-sync all

Claude: Analyzing documentation gaps...

📚 Documentation Sync Report
═════════════════════════════════════════════

✓ API Documentation
  - 3 new endpoints documented
  - File: docs/Implementation & Operations/API_REFERENCE.md

✓ Mechanism Catalog
  - 2 new mechanisms added (now 14 total)
  - File: docs/Core Technical Architecture/MECHANISM_CATALOG.md

⚠ Architecture Overview
  - New Bayesian service detected
  - Suggests manual review for integration

✓ Cross-references validated

═════════════════════════════════════════════

Ready to commit documentation updates? (y/n): y
```

---

## 🔧 Troubleshooting

### MCP Servers Not Working

**Issue:** Literature search or data fetching fails

**Solutions:**
1. Check MCP server configuration: `.claude/mcp_servers.json`
2. Verify network connectivity
3. Check API rate limits
4. For Census/BLS: Add API keys if needed

### Tests Failing on Docker Integration

**Issue:** `/test-stack` reports database connection errors

**Solutions:**
1. Check Docker services: `docker-compose ps`
2. Start services: `docker-compose up -d postgres redis`
3. Use quick mode to skip integration tests: `/test-stack quick`

### Schema Validation Errors

**Issue:** Mechanism validation fails

**Solutions:**
1. Check YAML syntax (indentation, special characters)
2. Verify all required fields present
3. Check value types match schema
4. Review schema: `mechanism-bank/schema/mechanism-schema.json`

### Git Commit Issues

**Issue:** `/mechanism` can't commit to git

**Solutions:**
1. Check git status: `git status`
2. Ensure changes are staged
3. Check git user config: `git config user.name` and `git config user.email`
4. Verify file permissions

---

## 📖 Best Practices

### When Creating Mechanisms

1. **Search literature first** - Use MCP servers to find published effect sizes
2. **Prioritize quality** - Use meta-analyses and systematic reviews (A-tier)
3. **Structural framing** - Focus on policy/institutional interventions
4. **Equity analysis** - Always consider differential effects
5. **Document uncertainty** - Include confidence intervals
6. **Cite properly** - Use Chicago style with DOIs

### When Running Tests

1. **Test incrementally** - Use `/test-stack changed` during development
2. **Check coverage** - Maintain ≥80% threshold
3. **Run full suite** before commits - Use `/test-stack all`
4. **Fix failures immediately** - Don't accumulate test debt
5. **Include accessibility** - Especially for frontend changes

### When Updating Documentation

1. **Sync regularly** - Run `/docs-sync check` weekly
2. **Update immediately** for API changes
3. **Multi-persona perspective** - Consider technical, scientific, and user audiences
4. **Cross-reference** - Link between related docs
5. **Examples current** - Ensure code examples work with current API

---

## 🛠️ Advanced Configuration

### Custom MCP Servers

To add additional MCP servers, edit `.claude/mcp_servers.json`:

```json
{
  "mcpServers": {
    "your-server-name": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-name"],
      "env": {
        "API_KEY": "your-key-here"
      },
      "description": "What this server does"
    }
  }
}
```

### Enhanced Permissions

To allow additional bash commands, edit `.claude/settings.local.json`:

```json
{
  "permissions": {
    "allow": [
      "Bash(your-command:*)"
    ]
  }
}
```

---

## 📊 Metrics & Monitoring

### Test Coverage Tracking

```bash
# Backend
pytest --cov=app --cov-report=html
open backend/htmlcov/index.html

# Frontend
npm test -- --coverage
open frontend/coverage/lcov-report/index.html
```

### Mechanism Bank Statistics

```bash
# Count mechanisms
find mechanism-bank/mechanisms/ -name "*.yaml" | wc -l

# Count by quality tier
grep -r "quality_tier: A" mechanism-bank/mechanisms/ | wc -l

# List recent additions
git log --since="1 month ago" --pretty=format:"%h %ad %s" -- mechanism-bank/mechanisms/
```

---

## 🎯 Roadmap

### Phase 2 (Future)

Planned enhancements:

1. **Bayesian Modeling MCP Server** - PyMC workflow support
2. **Graph Database Server** - Neo4j for network analysis
3. **Data Pipeline Agent** - ETL pipeline generation
4. **`/equity-check` command** - Automated equity analysis
5. **`/bayesian` command** - PyMC model helpers

---

## 📚 Additional Resources

### Project Documentation

- **Foundational Principles:** `docs/Foundational Principles/01_PROJECT_FOUNDATIONS.md`
- **Mechanism Bank Structure:** `docs/Core Technical Architecture/05_MECHANISM_BANK_STRUCTURE.md`
- **Stock-Flow Paradigm:** `docs/Core Technical Architecture/04_STOCK_FLOW_PARADIGM.md`

### External Resources

- Claude Code documentation: https://code.claude.com/docs
- MCP specification: https://modelcontextprotocol.io
- Semantic Scholar API: https://www.semanticscholar.org/product/api
- Census API: https://www.census.gov/data/developers/data-sets.html

---

## 🤝 Contributing

When adding new Claude Code customizations:

1. Follow existing patterns in `.claude/`
2. Document in this README
3. Test thoroughly before committing
4. Consider equity and structural competency implications
5. Update skills/prompts if relevant

---

## 📝 Support

For issues or questions:

1. Check this README first
2. Review skill/command documentation in `.claude/`
3. Check project documentation in `docs/`
4. Open issue in project repository with `[claude-code]` tag

---

**Version:** 1.0 (Phase 1 Foundation)
**Last Updated:** 2025-11-16
**Maintained by:** HealthSystems Platform Team
