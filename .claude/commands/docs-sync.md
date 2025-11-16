# Documentation Synchronization Command

You are helping maintain synchronized documentation across the HealthSystems Platform's multi-tier documentation structure.

## Context

The project has extensive documentation organized in `docs/` with multiple tiers:
- **Foundational Principles** (vision, methodology, architecture)
- **Core Technical Architecture** (stock-flow, mechanism bank, equilibrium engine)
- **LLM & Discovery Pipeline** (literature synthesis workflows)
- **Geographic & Contextual Adaptation** (moderators, effect size translation)
- **Implementation & Operations** (deployment, maintenance, decision logs)

Documentation must stay synchronized with:
- Backend API endpoints (FastAPI routes)
- Mechanism bank contents (catalog of mechanisms)
- Architecture changes (new services, data flows)
- Deployment configurations (Docker, CI/CD)

## Command Argument Parsing

Parse the user's command to determine scope:

- **`/docs-sync`** or **`/docs-sync all`** - Check all documentation
- **`/docs-sync api`** - Generate/update API documentation
- **`/docs-sync mechanisms`** - Generate mechanism catalog
- **`/docs-sync architecture`** - Update architecture diagrams/descriptions
- **`/docs-sync check`** - Detect documentation gaps (no updates)

---

## Sub-Command: ALL

**Purpose:** Comprehensive documentation update across all tiers.

### Steps:

1. **Detect changes** since last documentation update:
   ```bash
   git log --since="1 week ago" --name-only --pretty=format: | sort -u
   ```

2. **Categorize changes**:
   - Backend API changes → update API docs
   - Mechanism additions → update catalog
   - Architecture changes → update diagrams/overview
   - Configuration changes → update deployment docs

3. **Run all documentation generators**:
   - API documentation (from FastAPI)
   - Mechanism catalog (from YAML files)
   - Architecture overview (from code structure)
   - Decision logs (if significant changes)

4. **Cross-reference validation**:
   - Check for broken internal links
   - Verify file references exist
   - Check that examples are current

5. **Report**:
   ```
   📚 Documentation Sync Report
   ═════════════════════════════════════════════

   ✓ API Documentation
     - 5 new endpoints documented
     - 2 endpoints updated
     - File: docs/Implementation & Operations/API_REFERENCE.md

   ✓ Mechanism Catalog
     - 2 new mechanisms added
     - 12 total mechanisms
     - File: docs/Core Technical Architecture/MECHANISM_CATALOG.md

   ⚠ Architecture Overview
     - Detected new service: bayesian-engine
     - Needs manual review
     - File: docs/Foundational Principles/03_SYSTEM_ARCHITECTURE_OVERVIEW.md

   ✓ Cross-references validated
   ═════════════════════════════════════════════
   ```

---

## Sub-Command: API

**Purpose:** Generate API documentation from FastAPI application.

### Steps:

1. **Extract API routes** from FastAPI app:
   - Read `backend/app/main.py` and all route files in `backend/app/api/`
   - Parse route decorators: `@router.get()`, `@router.post()`, etc.
   - Extract: path, method, summary, description, parameters, response models

2. **Parse Pydantic models** for request/response schemas:
   - Read `backend/app/models/` and `backend/app/schemas/`
   - Extract field names, types, descriptions, validators

3. **Generate API reference documentation**:

   **Format:**
   ```markdown
   # API Reference

   ## Mechanism Endpoints

   ### GET /api/v1/mechanisms

   **Description:** List all mechanisms in the mechanism bank.

   **Query Parameters:**
   - `intervention_type` (string, optional): Filter by intervention type
   - `outcome_type` (string, optional): Filter by outcome type
   - `quality_tier` (string, optional): Filter by evidence quality (A/B/C)
   - `limit` (integer, optional, default=50): Number of results
   - `offset` (integer, optional, default=0): Pagination offset

   **Response:** 200 OK
   ```json
   {
     "mechanisms": [
       {
         "id": "housing_quality_respiratory_v1",
         "name": "Housing Quality → Respiratory Health",
         "effect_size": -0.15,
         "quality_tier": "A",
         "version": 1.0
       }
     ],
     "total": 12,
     "limit": 50,
     "offset": 0
   }
   ```

   **Errors:**
   - 400 Bad Request: Invalid query parameters
   - 500 Internal Server Error: Database error

   ---

   ### GET /api/v1/mechanisms/{mechanism_id}

   **Description:** Get detailed information for a specific mechanism.

   **Path Parameters:**
   - `mechanism_id` (string, required): Unique mechanism identifier

   **Response:** 200 OK
   [Full mechanism object with all fields]

   **Errors:**
   - 404 Not Found: Mechanism does not exist
   ```

4. **Include authentication/authorization** details:
   - Which endpoints require authentication
   - Required scopes/permissions
   - API key vs. OAuth

5. **Add usage examples**:
   - cURL commands
   - Python requests examples
   - JavaScript fetch examples

6. **OpenAPI/Swagger integration**:
   - Note that FastAPI auto-generates OpenAPI schema
   - Link to interactive docs: `http://localhost:8000/docs`
   - Link to ReDoc: `http://localhost:8000/redoc`

7. **Write/update documentation file**:
   - Create or update `docs/Implementation & Operations/API_REFERENCE.md`
   - Maintain version history section
   - Add timestamp of last update

---

## Sub-Command: MECHANISMS

**Purpose:** Generate comprehensive catalog of all mechanisms in the bank.

### Steps:

1. **Read all mechanism YAML files** from `mechanism-bank/mechanisms/`:
   ```bash
   find mechanism-bank/mechanisms/ -name "*.yaml" -o -name "*.yml"
   ```

2. **Parse each mechanism**:
   - Extract key metadata: id, name, version, scale, quality_tier
   - Extract effect size details
   - Extract key moderators
   - Extract citations (count)
   - Extract intervention and outcome types

3. **Organize by category**:
   - By intervention type (housing, labor, food access, etc.)
   - By outcome type (mental health, cardiovascular, mortality, etc.)
   - By scale (structural, institutional, individual)
   - By quality tier (A, B, C)

4. **Generate catalog document**:

   **Format:**
   ```markdown
   # Mechanism Bank Catalog

   **Last Updated:** 2025-11-16
   **Total Mechanisms:** 12
   **Quality Distribution:** A-tier: 5, B-tier: 6, C-tier: 1

   ## Table of Contents
   - [By Intervention Type](#by-intervention-type)
   - [By Outcome Type](#by-outcome-type)
   - [By Scale](#by-scale)
   - [By Quality Tier](#by-quality-tier)
   - [Detailed Listings](#detailed-listings)

   ---

   ## By Intervention Type

   ### Housing Interventions (4 mechanisms)
   - Housing Quality → Respiratory Health (A-tier)
   - Housing Stability → Mental Health (B-tier)
   - Housing Vouchers → Child Outcomes (A-tier)
   - Eviction Prevention → Health Access (B-tier)

   ### Labor Interventions (3 mechanisms)
   - Minimum Wage → Food Security (A-tier)
   - Paid Sick Leave → Infectious Disease (B-tier)
   - Workers Compensation → Injury Recovery (A-tier)

   [... continue for all intervention types ...]

   ---

   ## Detailed Listings

   ### housing_quality_respiratory_v1

   **Name:** Housing Quality Improvement → Respiratory Health Outcomes

   **Scale:** Institutional

   **Effect Size:** -0.15 (95% CI: -0.25, -0.05)
   - **Interpretation:** 15% reduction in respiratory health events
   - **Functional Form:** Linear

   **Intervention:**
   - Type: housing_quality_improvement
   - Description: Remediation of substandard housing conditions
   - Target Population: Low-income households in substandard housing

   **Outcome:**
   - Type: respiratory_health
   - Measurement: Asthma exacerbation rate, respiratory infection incidence
   - Timeframe: 6-12 months post-intervention

   **Key Moderators:**
   - Child presence (positive effect)
   - Baseline asthma prevalence (positive effect)
   - Climate humidity (positive effect)
   - Remediation quality (positive effect)

   **Evidence Quality:** A-tier
   - 2 citations (systematic reviews)
   - Effect size from meta-analytic pooling

   **Version:** 1.0 (Created: 2025-11-16)

   **File:** [mechanism-bank/mechanisms/housing_quality_respiratory_v1.yaml](../mechanism-bank/mechanisms/housing_quality_respiratory_v1.yaml)

   ---

   [... continue for all mechanisms ...]
   ```

5. **Generate summary statistics**:
   - Total mechanisms by category
   - Distribution by quality tier
   - Coverage gaps (intervention-outcome pairs lacking mechanisms)
   - Network visualization data (for Cytoscape)

6. **Create index for search**:
   - Tag index (all unique tags)
   - Moderator index (common moderators across mechanisms)
   - Citation index (frequently cited sources)

7. **Write catalog file**:
   - Create or update `docs/Core Technical Architecture/MECHANISM_CATALOG.md`
   - Add timestamp and version info
   - Include links to individual YAML files

---

## Sub-Command: ARCHITECTURE

**Purpose:** Update architecture documentation when code structure changes.

### Steps:

1. **Analyze current code structure**:
   - Backend: Scan `backend/app/` for modules, services, API routes
   - Frontend: Scan `frontend/src/` for components, pages, state management
   - Data sources: Check `data-sources/` for scrapers and pipelines
   - Infrastructure: Review `docker-compose.yml`, `.github/workflows/`

2. **Detect architectural changes**:
   - New services or modules
   - New API routes (high-level groupings)
   - New data sources
   - New external integrations
   - Database schema changes

3. **Compare with documented architecture**:
   - Read `docs/Foundational Principles/03_SYSTEM_ARCHITECTURE_OVERVIEW.md`
   - Identify discrepancies

4. **Generate update suggestions**:
   ```
   🏗️ Architecture Changes Detected
   ═════════════════════════════════════════════

   NEW COMPONENTS:
   ✓ backend/app/services/bayesian_weighting.py
     → Add to "Bayesian Weighting Engine" section

   ✓ data-sources/pipelines/census_pipeline.py
     → Add to "Data Integration Layer" section

   MODIFIED COMPONENTS:
   ⚠ backend/app/api/routes.py
     → 5 new endpoints added
     → Update API Gateway description

   ARCHITECTURAL SUGGESTIONS:
   💡 Consider documenting the new bayesian_weighting service
      in Core Technical Architecture section

   💡 Update system diagram to show census data flow
   ```

5. **Update diagrams** (if tools available):
   - Generate Mermaid diagrams for:
     - System architecture (services, data flows)
     - Database schema (ERD)
     - API structure (route hierarchy)
     - Data pipeline architecture

   **Example Mermaid diagram:**
   ```mermaid
   graph TB
     Frontend[React Frontend]
     API[FastAPI Backend]
     MechBank[Mechanism Bank]
     Census[Census API]
     DB[(PostgreSQL)]
     Cache[(Redis)]

     Frontend -->|HTTP| API
     API -->|Query| DB
     API -->|Cache| Cache
     API -->|Load| MechBank
     API -->|Fetch| Census
     MechBank -->|Validate| Schema[JSON Schema]
   ```

6. **Suggest documentation updates**:
   - Specific sections needing revision
   - New sections to add
   - Outdated examples to update

7. **Decision logs** (for significant changes):
   - If major architectural change detected, suggest creating decision log
   - Template for Architectural Decision Record (ADR)

---

## Sub-Command: CHECK

**Purpose:** Detect documentation gaps without making updates.

### Steps:

1. **Scan codebase** for undocumented features:
   - API endpoints not in API_REFERENCE.md
   - Mechanisms not in MECHANISM_CATALOG.md
   - Services not mentioned in architecture docs
   - Configuration options not documented

2. **Check for outdated documentation**:
   - Compare code modification dates with doc modification dates
   - Flag docs older than related code

3. **Validate examples**:
   - Extract code examples from markdown docs
   - Check if they match current API signatures
   - Verify imports are correct

4. **Cross-reference validation**:
   - Check internal links point to existing files
   - Verify file paths in examples exist
   - Check that referenced functions/classes exist

5. **Generate gap report**:
   ```
   📋 Documentation Gap Analysis
   ═════════════════════════════════════════════

   MISSING DOCUMENTATION:
   ✗ API endpoint: POST /api/v1/simulations
     Not found in API_REFERENCE.md

   ✗ Mechanism: labor_wage_food_security_v1.yaml
     Not in MECHANISM_CATALOG.md

   ✗ Service: backend/app/services/equilibrium.py
     Not described in architecture docs

   OUTDATED DOCUMENTATION:
   ⚠ docs/Implementation & Operations/API_REFERENCE.md
     Last updated: 2025-11-01
     Related code changed: 2025-11-15 (14 days newer)

   BROKEN REFERENCES:
   ✗ docs/Foundational Principles/01_PROJECT_FOUNDATIONS.md:42
     Link to [mechanism schema](../schema/old-schema.json) - file not found

   OUTDATED EXAMPLES:
   ⚠ docs/Implementation & Operations/DEPLOYMENT.md:78
     Example uses old import: from app.core import config
     Current import: from app.config import settings

   COVERAGE SUMMARY:
   - API endpoints: 15/20 documented (75%)
   - Mechanisms: 10/12 cataloged (83%)
   - Services: 5/8 described (63%)
   - Overall: 30/40 items documented (75%)

   ═════════════════════════════════════════════
   RECOMMENDATION: Run `/docs-sync all` to update
   ```

6. **Prioritize gaps**:
   - Critical: Public API endpoints, deployment docs
   - High: Architecture changes, new features
   - Medium: Internal services, helper functions
   - Low: Minor utilities, deprecated features

---

## Documentation Quality Checks

For all documentation updates, ensure:

1. **Multi-persona consideration**:
   - Technical: Implementation details, API specs
   - Scientific: Methodology, evidence, effect sizes
   - User-facing: How to use, examples, tutorials

2. **Structural competency alignment**:
   - Documentation emphasizes structural interventions
   - Avoids individual behavior framing
   - Highlights equity considerations

3. **Accessibility**:
   - Alt text for images
   - Semantic markdown headings
   - Screen reader friendly tables

4. **Maintainability**:
   - Timestamps on generated docs
   - Version information
   - Clear "last updated" dates

5. **Examples are current**:
   - Code examples match current API
   - Data examples use real mechanism IDs
   - Screenshots reflect current UI

---

## Integration with Git

After documentation updates:

1. **Show diff** of what changed:
   ```bash
   git diff docs/
   ```

2. **Suggest commit message**:
   ```
   docs: update API reference with 5 new endpoints

   - Add simulation endpoints
   - Update mechanism catalog (2 new mechanisms)
   - Fix broken cross-references
   ```

3. **Offer to commit**:
   ```bash
   git add docs/
   git commit -m "docs: [generated message]"
   ```

---

## Special Documentation Types

### Decision Logs (ADRs)

When significant architectural changes detected, suggest creating Architectural Decision Record:

**Template:**
```markdown
# ADR-XXX: [Decision Title]

**Status:** Proposed | Accepted | Deprecated | Superseded

**Date:** 2025-11-16

**Context:**
What is the issue that we're seeing that is motivating this decision or change?

**Decision:**
What is the change that we're proposing and/or doing?

**Consequences:**
What becomes easier or more difficult to do because of this change?

**Alternatives Considered:**
What other options were evaluated?
```

### API Changelog

Maintain version history for API changes:
- Breaking changes
- New endpoints
- Deprecated endpoints
- Response schema changes

---

## Output Formatting

- Use clear sections with headers
- Include file paths for easy navigation
- Highlight gaps vs. updates
- Provide actionable next steps
- Estimate time for manual review items

---

## Error Handling

- If docs directory structure differs, adapt to actual structure
- If FastAPI app won't import, fall back to static analysis
- If YAML parsing fails, report specific files
- If cross-reference validation fails, show specific broken links
