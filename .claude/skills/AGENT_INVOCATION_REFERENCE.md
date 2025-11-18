# HealthSystems Platform: Agent Invocation Quick Reference

**Last Updated**: November 17, 2025
**Purpose**: Quick reference for invoking subagents with examples

---

## Table of Contents

1. [Invocation Syntax](#invocation-syntax)
2. [Agent-Specific Examples](#agent-specific-examples)
3. [Common Scenarios](#common-scenarios)
4. [Input/Output Specifications](#inputoutput-specifications)
5. [Troubleshooting Quick Fixes](#troubleshooting-quick-fixes)

---

## Invocation Syntax

### Method 1: Explicit Invocation

**Template**:
```
"Use the [agent-name] agent to [specific task]."
```

**Examples**:
```
"Use the mechanism-validator agent to check these 5 mechanisms."
"Ask the epidemiology-advisor to review the causal logic."
"Have the code-reviewer audit backend/routes/mechanisms.py for security issues."
```

### Method 2: Implicit/Automatic

**Template**: Just describe the task; Claude will use appropriate agent

**Examples**:
```
"Validate all mechanisms in the housing category."
→ Automatically invokes mechanism-validator

"This extraction is missing spatial variation."
→ Automatically invokes llm-prompt-engineer

"Is this causal pathway epidemiologically sound?"
→ Automatically invokes epidemiology-advisor
```

### Method 3: Multi-Agent Coordination

**Template**: Describe complex workflow; Claude coordinates agents

**Examples**:
```
"Extract, validate, and commit 50 housing mechanisms."
→ Claude coordinates: llm-prompt-engineer → validator → epidemiologist

"Implement search API with full QA."
→ Claude coordinates: implements → code-reviewer → test-generator → api-documenter
```

---

## Agent-Specific Examples

### 1. mechanism-validator

**Purpose**: Validate mechanism YAML files

**Invocation Examples**:

```bash
# Single mechanism
"Validate mechanism-bank/mechanisms/housing_quality_respiratory.yml"

# Batch validation
"Validate all mechanisms in mechanism-bank/mechanisms/built_environment/"

# Focused validation
"Check these 10 mechanisms for structural competency only"

# Quality audit
"Audit the entire mechanism bank and generate quality report"
```

**Input Format**:
```yaml
# Expects mechanism YAML file or list of file paths
mechanism-bank/mechanisms/category/mechanism_id.yml
```

**Output Format**:
```markdown
**Mechanism ID**: housing_quality_respiratory
**Status**: ✅ APPROVED | ⚠️ NEEDS REVISION | ❌ REJECTED

**Issues Found**:
1. [Issue description with line number]
2. [Suggested fix]

**Equity Analysis**:
[Assessment of equity considerations]
```

---

### 2. llm-prompt-engineer

**Purpose**: Optimize LLM extraction prompts

**Invocation Examples**:

```bash
# Fix specific issue
"Spatial variation detection is at 40%. Optimize the prompt."

# General improvement
"Review and improve mechanism extraction prompts"

# Domain-specific
"Optimize prompts for extracting housing→health mechanisms"

# Cost optimization
"Reduce token usage in extraction prompts without sacrificing quality"
```

**Input Format**:
```python
# Current prompt location
backend/pipelines/llm_mechanism_discovery.py

# Or specific prompt text
"""
[Your current prompt text]
"""

# Plus performance metrics
- Spatial variation detection: 40%
- Directionality accuracy: 85%
- Cost per mechanism: $0.15
```

**Output Format**:
```markdown
## Prompt Analysis
[Issues identified]

## Improved Prompt
```python
system_prompt = """
[New prompt text]
"""
```

## Expected Improvements
- Spatial variation: 40% → 85%
- Cost reduction: 15% through caching
```

---

### 3. epidemiology-advisor

**Purpose**: Expert epidemiological review

**Invocation Examples**:

```bash
# Single mechanism review
"Review the causal logic of this Housing→Health pathway"

# Evidence assessment
"Assess the evidence quality for these 10 mechanisms"

# Theoretical validation
"Is this mechanism consistent with fundamental cause theory?"

# Dispute resolution
"The validator approved but I'm concerned about reverse causation. Review?"
```

**Input Format**:
```yaml
# Mechanism file or description
mechanism:
  name: Housing Quality → Respiratory Health
  source_node: Housing_Quality
  target_node: Respiratory_Health
  directionality: negative
  evidence:
    quality_rating: A
    n_studies: 8
```

**Output Format**:
```markdown
## Epidemiological Review: [Mechanism ID]

### Causal Logic: ✅ Strong | ⚠️ Moderate | ❌ Weak
[Assessment with Bradford Hill criteria]

### Evidence Quality: [Agree with A | Revise to B]
[Evidence evaluation]

### Recommendations:
1. [Specific suggestion]
2. [Additional consideration]

### Overall: Accept | Accept with revisions | Reject
```

---

### 4. code-reviewer

**Purpose**: Code quality and security review

**Invocation Examples**:

```bash
# Full file review
"Review backend/routes/mechanisms.py for quality and security"

# Focused review
"Check backend/routes/mechanisms.py for OWASP Top 10 vulnerabilities"

# Performance review
"Review this code for performance issues and optimization opportunities"

# Accessibility review
"Review frontend/src/components/MechanismList.tsx for WCAG 2.1 AA compliance"
```

**Input Format**:
```python
# File path
backend/routes/mechanisms.py

# Or code snippet
"""
@app.get("/mechanisms")
async def list_mechanisms(category: str = None):
    ...
"""

# Specify focus area
- Security only
- Performance only
- Best practices
- Full review
```

**Output Format**:
```markdown
## Code Review: [File/Feature Name]

### ✅ Strengths
- [What's done well]

### ⚠️ Issues Found

#### 🔴 Critical
- **File:Line**: [Issue]
  ```python
  # Current (problematic)
  ...

  # Suggested fix
  ...
  ```

#### 🟡 Important
- [Issue description]

#### 🟢 Minor
- [Nice-to-have improvement]

### Overall: Approve | Request Changes | Reject
```

---

### 5. test-generator

**Purpose**: Generate test suites

**Invocation Examples**:

```bash
# Generate tests for new code
"Generate tests for backend/routes/mechanisms.py search endpoint"

# Improve coverage
"Add edge case tests for the mechanism validation logic"

# Security tests
"Generate security tests for API authentication"

# Integration tests
"Create integration tests for the Census data pipeline"
```

**Input Format**:
```python
# File to test
backend/routes/mechanisms.py

# Or function to test
def search_mechanisms(query: str, filters: dict):
    ...

# Specify test type
- Unit tests
- Integration tests
- Edge cases
- Security tests
```

**Output Format**:
```python
# tests/test_mechanisms.py
import pytest

class TestMechanismSearch:
    def test_search_basic_query(self):
        """Test basic search functionality."""
        ...

    def test_search_empty_query(self):
        """Test handling of empty query."""
        ...

    # ... 10-20 more tests

# Coverage report
# Target: 90% coverage achieved
```

---

### 6. api-documenter

**Purpose**: Generate API documentation

**Invocation Examples**:

```bash
# Document new endpoint
"Document the POST /api/mechanisms/search endpoint"

# Full API docs
"Generate complete API documentation for all endpoints"

# OpenAPI spec
"Generate OpenAPI 3.0 specification for the API"

# Usage guide
"Create a Quick Start guide for the API with examples"
```

**Input Format**:
```python
# File with endpoints
backend/routes/mechanisms.py

# Or specific endpoint
@app.post("/mechanisms/search")
async def search_mechanisms(query: SearchQuery):
    ...
```

**Output Format**:
```markdown
## POST /api/mechanisms/search

Search mechanisms with full-text query.

### Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| query | string | Yes | Search query text |
| ...

### Request Example
```bash
curl -X POST "https://api.healthsystems.org/v1/mechanisms/search" \
  -H "Authorization: Bearer TOKEN" \
  -d '{"query": "housing"}'
```

### Response
```json
{
  "results": [...],
  "total": 42
}
```

### Error Codes
- 400: Invalid query
- 401: Unauthorized
- 429: Rate limit exceeded
```

---

### 7. data-pipeline-builder

**Purpose**: Build ETL pipelines and scrapers

**Invocation Examples**:

```bash
# New scraper
"Build an EPA air quality data scraper for county-level PM2.5 data"

# Pipeline design
"Design ETL pipeline for integrating Census and CDC data"

# Optimization
"Optimize the Census scraper for better performance and caching"

# Validation
"Add data quality validation to the CDC PLACES pipeline"
```

**Input Format**:
```python
# Data source details
- API: EPA Air Quality System
- Data: County-level PM2.5
- Update frequency: Daily
- Requirements: Error handling, caching, validation

# Or existing code to improve
data-sources/scrapers/census/census_api.py
```

**Output Format**:
```python
# data-sources/scrapers/epa/air_quality.py
class EPAAirQualityAPI:
    """
    EPA Air Quality scraper for county-level data.

    Features:
    - Automatic retries
    - Rate limiting
    - Redis caching
    - Data validation
    """

    def get_pm25_data(self, counties: List[str], date: str):
        ...

# Plus:
# - Config file (YAML)
# - Caching utilities
# - Validation schema
# - Usage examples
```

---

## Common Scenarios

### Scenario 1: "I just extracted 50 mechanisms. What now?"

**Invocation**:
```
"Validate these 50 mechanisms and report quality issues."
```

**What happens**:
- mechanism-validator audits all 50
- Returns approval/revision/rejection for each
- Lists specific issues

**Next step**:
```
"Fix the 5 mechanisms flagged for revision and get expert review for the rest."
```

---

### Scenario 2: "My extraction quality is poor."

**Invocation**:
```
"The LLM extraction has these issues:
- Missing spatial variation 40% of the time
- Incorrect directionality in 15% of cases
- Citations not in Chicago format

Fix the prompts."
```

**What happens**:
- llm-prompt-engineer analyzes issues
- Provides improved prompt addressing each issue
- Includes test cases

**Next step**:
```
"Test the improved prompt on 20 papers and validate results."
```

---

### Scenario 3: "I implemented a new API endpoint. Need full QA."

**Invocation**:
```
"I implemented POST /api/mechanisms/search in backend/routes/mechanisms.py.
Run full quality assurance: code review, tests, and documentation."
```

**What happens**:
1. code-reviewer checks code quality and security
2. You apply fixes
3. test-generator creates test suite
4. api-documenter generates docs

**Result**: Production-ready feature with tests and docs

---

### Scenario 4: "Need to build a data scraper."

**Invocation**:
```
"Build a CDC PLACES API scraper for county-level diabetes and obesity data.
Include error handling, caching, and validation."
```

**What happens**:
- data-pipeline-builder creates scraper class
- Includes all requested features
- Provides usage examples

**Next step**:
```
"Review this scraper for code quality and generate tests."
```
→ code-reviewer + test-generator

---

### Scenario 5: "Systematic issue in mechanism bank."

**Invocation**:
```
"Audit all 500 mechanisms for:
- Structural competency
- Citation format
- Equity considerations

Generate quality report."
```

**What happens**:
- mechanism-validator batch audits
- Generates quality metrics
- Lists all issues by category

**Next step**:
```
"Fix formatting issues and get expert review for structural competency concerns."
```

---

## Input/Output Specifications

### mechanism-validator

| Input | Output |
|-------|--------|
| YAML file path(s) | Validation report (✅/⚠️/❌ per mechanism) |
| Mechanism object(s) | List of issues with line numbers |
| Directory path | Quality metrics (completeness, accuracy) |

### llm-prompt-engineer

| Input | Output |
|-------|--------|
| Current prompt + performance metrics | Improved prompt template |
| Error patterns from validator | Few-shot examples |
| Domain (e.g., housing→health) | Domain-specific guidance |

### epidemiology-advisor

| Input | Output |
|-------|--------|
| Mechanism file or description | Causal logic assessment (✅/⚠️/❌) |
| Evidence claims | Evidence quality evaluation |
| Theoretical question | Expert opinion with references |

### code-reviewer

| Input | Output |
|-------|--------|
| File path or code snippet | Review report (strengths + issues) |
| Focus area (security, performance) | Specific suggestions with examples |
| Language (Python, TypeScript) | Language-specific best practices |

### test-generator

| Input | Output |
|-------|--------|
| Code file or function | Test file with 10-25 test cases |
| Test type (unit, integration) | Tests for specified type |
| Coverage gaps | Tests for uncovered code |

### api-documenter

| Input | Output |
|-------|--------|
| API endpoint code | Endpoint documentation |
| Multiple endpoints | Full API reference |
| Request: OpenAPI | OpenAPI 3.0 YAML spec |

### data-pipeline-builder

| Input | Output |
|-------|--------|
| Data source specs | Scraper/pipeline implementation |
| Existing pipeline | Optimization suggestions + code |
| Requirements (caching, validation) | Complete solution with requested features |

---

## Troubleshooting Quick Fixes

### Problem: "Agent returns incomplete result"

**Fix**:
```
# ❌ Vague
"Review this code."

# ✅ Specific
"Review backend/routes/mechanisms.py for:
- Security vulnerabilities (OWASP Top 10)
- Performance issues (N+1 queries, caching)
- Best practices (FastAPI patterns)"
```

---

### Problem: "Wrong agent used automatically"

**Fix**: Use explicit invocation
```
# ❌ Ambiguous
"Check if this mechanism is correct."

# ✅ Explicit
"Use the epidemiology-advisor agent to assess the causal logic of this mechanism."
```

---

### Problem: "Agent needs more context"

**Fix**: Provide file paths and specifics
```
# ❌ Insufficient
"Review the API."

# ✅ With context
"Review backend/routes/mechanisms.py, specifically the search_mechanisms function (lines 45-89).
Focus on input validation and SQL injection risks."
```

---

### Problem: "Agent takes too long"

**Fix**: Break into smaller tasks
```
# ❌ Too large
"Validate all 500 mechanisms."

# ✅ Batched
"Validate mechanisms in mechanism-bank/mechanisms/built_environment/ (50 files)."
# Then repeat for other categories
```

---

### Problem: "Contradictory results from multiple agents"

**Example**: Validator approves, epidemiologist rejects

**Fix**: Understand each agent's scope
```
# Validator checks format/schema → May approve
# Epidemiologist checks causal logic → May reject

# Resolution:
"Both assessments are valid. The mechanism has correct format but
questionable causal logic. Let's revise the causal pathway."
```

---

## Quick Command Reference

| Task | Command Template |
|------|------------------|
| Validate mechanism | `"Validate [file_path or description]"` |
| Fix extraction prompt | `"Fix prompt: [issue description]"` |
| Expert mechanism review | `"Get epidemiology expert review for [mechanism]"` |
| Review code | `"Review [file_path] for [focus area]"` |
| Generate tests | `"Generate tests for [file/function]"` |
| Document API | `"Document [endpoint or all endpoints]"` |
| Build pipeline | `"Build [data source] scraper with [requirements]"` |

---

## Best Practices Summary

### ✅ DO:
- Be specific about what you want
- Provide file paths or code context
- Specify focus areas (security, performance, etc.)
- Break large tasks into batches
- Use explicit invocation when ambiguous

### ❌ DON'T:
- Give vague instructions ("check this")
- Omit necessary context
- Ask agents to do tasks outside their expertise
- Send huge batches (split into manageable chunks)
- Expect perfect results without iteration

---

**Remember**: Agents are most effective when given clear, specific instructions with sufficient context. When in doubt, be more specific, not less.
