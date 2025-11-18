# HealthSystems Platform: Subagent Workflow Patterns

**Last Updated**: November 17, 2025
**Purpose**: Common multi-agent workflows for coordinating specialized subagents

---

## Table of Contents

1. [Introduction](#introduction)
2. [Pattern Categories](#pattern-categories)
3. [Mechanism Discovery Workflows](#mechanism-discovery-workflows)
4. [Code Development Workflows](#code-development-workflows)
5. [Data Pipeline Workflows](#data-pipeline-workflows)
6. [Quality Assurance Workflows](#quality-assurance-workflows)
7. [Documentation Workflows](#documentation-workflows)
8. [Troubleshooting Workflows](#troubleshooting-workflows)

---

## Introduction

This document provides **reusable workflow patterns** for coordinating multiple subagents to accomplish complex tasks. Each pattern includes:

- **Goal**: What you're trying to achieve
- **Agents involved**: Which subagents participate
- **Steps**: Detailed sequence of operations
- **Expected outputs**: What you get at the end
- **Variations**: Alternative approaches

---

## Pattern Categories

| Category | Focus | Primary Agents |
|----------|-------|----------------|
| **Mechanism Discovery** | Extract and validate mechanisms from literature | llm-prompt-engineer, mechanism-validator, epidemiology-advisor |
| **Code Development** | Implement, review, test, and document features | code-reviewer, test-generator, api-documenter |
| **Data Pipeline** | Build and validate ETL workflows | data-pipeline-builder, code-reviewer, test-generator |
| **Quality Assurance** | Validate, review, and improve quality | mechanism-validator, epidemiology-advisor, code-reviewer |
| **Documentation** | Generate and maintain docs | api-documenter |
| **Troubleshooting** | Debug and optimize systems | llm-prompt-engineer, code-reviewer |

---

## Mechanism Discovery Workflows

### Pattern 1: Full Mechanism Discovery Pipeline

**Goal**: Extract, validate, and commit high-quality mechanisms from literature

**Agents**: llm-prompt-engineer → mechanism-validator → epidemiology-advisor

**Steps**:

```
1. USER REQUEST
   "Extract 50 mechanisms from housing→health literature"

2. MAIN CONVERSATION (Planning)
   - Identifies papers/sources
   - Determines extraction scope
   - Initiates prompt optimization

3. llm-prompt-engineer
   INPUT: Domain (housing→health), current prompt version
   TASK: Optimize extraction prompts for housing domain
   OUTPUT: Improved prompt template with:
     - Housing-specific examples
     - Spatial variation detection guidance
     - Evidence quality criteria for housing literature

4. MAIN CONVERSATION (Extraction)
   - Runs LLM extraction on 20 papers
   - Generates 50 candidate mechanisms
   - Prepares for validation

5. mechanism-validator
   INPUT: 50 extracted mechanisms
   TASK: Validate each for:
     - Structural competency
     - Schema compliance
     - Citation format
     - Equity considerations
   OUTPUT: Validation report:
     - ✅ 42 approved
     - ⚠️ 5 need revision (specific issues listed)
     - ❌ 3 rejected (structural competency failures)

6. MAIN CONVERSATION (Revision)
   - Fixes 5 mechanisms based on validator feedback
   - Re-validates revised mechanisms
   - Prepares 45 mechanisms for expert review

7. epidemiology-advisor
   INPUT: 45 validated mechanisms
   TASK: Expert epidemiological review:
     - Causal logic assessment
     - Evidence quality evaluation
     - Theoretical coherence check
   OUTPUT: Expert assessment:
     - ✅ 43 epidemiologically sound
     - ⚠️ 2 flagged for additional evidence needed

8. MAIN CONVERSATION (Final)
   - Creates mechanism bank entries (YAML files)
   - Generates commit message with summary
   - Commits 43 validated mechanisms
   - Flags 2 for future research

OUTPUT:
- 43 high-quality mechanisms in mechanism bank
- Validation report
- Expert review summary
- 2 mechanisms flagged for Phase 2 evidence collection
```

---

### Pattern 2: Rapid Iteration on Extraction Quality

**Goal**: Fix systematic extraction errors quickly

**Agents**: mechanism-validator → llm-prompt-engineer (iterative loop)

**Steps**:

```
1. USER IDENTIFIES ISSUE
   "Spatial variation detection rate is only 40%"

2. mechanism-validator
   INPUT: Last 100 extracted mechanisms
   TASK: Audit for spatial variation detection patterns
   OUTPUT: Analysis:
     - 40% detection rate confirmed
     - Missing when: Climate/urbanicity mentioned but not explicitly labeled
     - Pattern: Implicit spatial factors not detected

3. llm-prompt-engineer
   INPUT: Validator analysis, current prompt
   TASK: Fix spatial variation detection
   OUTPUT: Improved prompt with:
     - Explicit spatial variation checklist
     - Few-shot examples of implicit variation
     - Mechanism-based inference guidance

4. MAIN CONVERSATION
   - Tests improved prompt on 20 papers
   - Extracts mechanisms

5. mechanism-validator
   INPUT: 20 new extractions
   TASK: Re-audit spatial variation detection
   OUTPUT: Detection rate: 85% (improvement confirmed)

6. llm-prompt-engineer (OPTIONAL if < 90%)
   INPUT: Remaining issues
   TASK: Further refinement
   OUTPUT: Final prompt version

7. MAIN CONVERSATION
   - Commits improved prompt (version 1.2)
   - Documents performance improvement
   - Re-processes high-priority mechanisms with new prompt
```

---

### Pattern 3: Expert-Driven Mechanism Curation

**Goal**: High-stakes mechanisms require epidemiologist approval first

**Agents**: epidemiology-advisor → mechanism-validator

**Steps**:

```
1. USER REQUEST
   "Review these 10 high-priority policy→health mechanisms"

2. epidemiology-advisor
   INPUT: 10 mechanisms (raw or partially validated)
   TASK: Epidemiological assessment:
     - Causal plausibility
     - Evidence strength
     - Theoretical coherence
     - Policy relevance
   OUTPUT: Expert opinion for each:
     - Mechanism 1: ✅ Strong evidence, causally sound
     - Mechanism 2: ⚠️ Plausible but limited evidence
     - Mechanism 3: ❌ Reverse causation concern
     ...

3. MAIN CONVERSATION
   - Addresses epidemiologist concerns
   - Revises mechanisms as needed
   - Prepares approved mechanisms for format validation

4. mechanism-validator
   INPUT: Epidemiologist-approved mechanisms
   TASK: Format and structure validation only
   OUTPUT: Schema compliance report

5. MAIN CONVERSATION
   - Commits to mechanism bank with "Expert-reviewed" flag
   - Prioritizes high-evidence mechanisms for MVP
```

---

## Code Development Workflows

### Pattern 4: Feature Development with Full QA

**Goal**: Implement new feature with code review, tests, and docs

**Agents**: code-reviewer → test-generator → api-documenter

**Steps**:

```
1. USER REQUEST
   "Implement mechanism full-text search API with Elasticsearch"

2. MAIN CONVERSATION (Implementation)
   - Designs search endpoint architecture
   - Implements POST /api/mechanisms/search
   - Adds Elasticsearch integration
   - Basic error handling

3. code-reviewer
   INPUT: New search endpoint code
   TASK: Comprehensive code review:
     - Security (input validation, injection risks)
     - Performance (query optimization, caching)
     - Best practices (FastAPI patterns, async/await)
     - Accessibility (if UI components)
   OUTPUT: Review report:
     ✅ Strengths:
       - Good endpoint structure
       - Proper Pydantic models
     ⚠️ Issues Found:
       - Missing rate limiting
       - No input sanitization for search query
       - Cache not implemented
       - Error handling incomplete
     📝 Suggestions:
       - Add slowapi rate limiter
       - Sanitize special characters
       - Implement Redis caching (TTL: 300s)
       - Return structured errors

4. MAIN CONVERSATION (Revision)
   - Applies code-reviewer suggestions
   - Implements rate limiting
   - Adds input sanitization
   - Implements caching layer

5. test-generator
   INPUT: Revised search endpoint code
   TASK: Generate comprehensive test suite:
     - Unit tests for search logic
     - Integration tests with Elasticsearch
     - Edge cases (empty query, special chars, long queries)
     - Error scenarios (ES down, invalid index)
   OUTPUT: Test file with 15 test cases:
     - test_search_basic_query
     - test_search_with_filters
     - test_search_pagination
     - test_search_empty_results
     - test_search_invalid_query
     - test_search_rate_limit
     - test_search_cache_hit
     - test_search_elasticsearch_error
     ...

6. MAIN CONVERSATION
   - Runs tests: All pass ✅
   - Fixes any failing tests
   - Prepares for documentation

7. api-documenter
   INPUT: Search endpoint implementation
   TASK: Generate complete API docs:
     - OpenAPI spec addition
     - Endpoint description
     - Parameter documentation
     - Response schemas
     - Usage examples (curl, Python, JS)
     - Error codes
   OUTPUT: API documentation:
     - Updated openapi.yaml
     - README section with examples
     - Error reference updated

8. MAIN CONVERSATION
   - Reviews all artifacts
   - Creates PR with:
     * Implementation
     * Tests (15 cases, 95% coverage)
     * Documentation
   - Merges after approval
```

---

### Pattern 5: Security-Focused Code Review

**Goal**: Audit codebase for security vulnerabilities

**Agents**: code-reviewer (security mode) → test-generator (security tests)

**Steps**:

```
1. USER REQUEST
   "Audit all API endpoints for security vulnerabilities"

2. code-reviewer
   INPUT: All files in backend/routes/
   TASK: Security-focused review (OWASP Top 10):
     - SQL injection risks
     - XSS vulnerabilities
     - Authentication/authorization gaps
     - Secrets in code
     - Rate limiting missing
     - Input validation gaps
   OUTPUT: Security audit report:
     🔴 CRITICAL:
       - Mechanism search: No input sanitization (XSS risk)
       - User endpoints: Missing authentication
     🟡 IMPORTANT:
       - No rate limiting on public endpoints
       - API keys logged in debug mode
     🟢 MINOR:
       - Error messages too verbose (info disclosure)

3. MAIN CONVERSATION
   - Prioritizes fixes (critical first)
   - Implements security patches

4. test-generator
   INPUT: Security issues identified
   TASK: Generate security-specific tests:
     - SQL injection attempts
     - XSS payloads
     - Authentication bypass attempts
     - Rate limit testing
   OUTPUT: Security test suite (20 tests)

5. MAIN CONVERSATION
   - Runs security tests
   - Verifies all vulnerabilities fixed
   - Commits security patches
```

---

## Data Pipeline Workflows

### Pattern 6: Build and Validate Data Pipeline

**Goal**: Create robust, tested data scraper/ETL pipeline

**Agents**: data-pipeline-builder → code-reviewer → test-generator

**Steps**:

```
1. USER REQUEST
   "Build EPA air quality scraper for county-level PM2.5 data"

2. data-pipeline-builder
   INPUT: EPA API documentation, requirements
   TASK: Create complete pipeline:
     - EPA API client class
     - Authentication handling
     - Error handling & retries (3 attempts)
     - Rate limiting (respect API limits)
     - Data validation
     - Caching strategy
     - Progress logging
   OUTPUT: EPA scraper implementation:
     - data-sources/scrapers/epa/air_quality.py
     - Config: data-sources/configs/epa_variables.yml
     - Caching: utils/cache.py integration

3. code-reviewer
   INPUT: EPA scraper code
   TASK: Pipeline-specific review:
     - Error handling completeness
     - Data validation robustness
     - Performance (batch vs. sequential)
     - Logging and monitoring
     - Configuration management
   OUTPUT: Review report with suggestions:
     - Add progress bar for long-running scrapes
     - Implement incremental updates (don't re-fetch unchanged data)
     - Add data quality metrics tracking
     - Improve exception handling specificity

4. MAIN CONVERSATION
   - Applies suggestions
   - Implements incremental updates
   - Adds progress tracking

5. test-generator
   INPUT: Revised EPA scraper
   TASK: Generate pipeline tests:
     - Unit tests with mocked API
     - Integration test with real API (sandboxed)
     - Error scenarios (timeout, rate limit, invalid data)
     - Data validation tests
     - Cache behavior tests
   OUTPUT: Test suite (25 tests)

6. MAIN CONVERSATION
   - Runs tests
   - Fixes edge case handling
   - Commits pipeline with tests and docs
```

---

## Quality Assurance Workflows

### Pattern 7: Mechanism Bank Quality Audit

**Goal**: Audit entire mechanism bank for quality and consistency

**Agents**: mechanism-validator → epidemiology-advisor

**Steps**:

```
1. USER REQUEST
   "Audit all 500 mechanisms in the bank for quality"

2. mechanism-validator
   INPUT: All mechanism YAML files (500 total)
   TASK: Batch validation:
     - Schema compliance: 100%
     - Structural competency: Check each
     - Citation format: Chicago style verification
     - Equity considerations: Flagged if missing
   OUTPUT: Audit report:
     - 480 fully compliant (96%)
     - 15 structural competency issues
     - 5 citation format errors
     - 10 missing equity analysis

3. MAIN CONVERSATION
   - Groups issues by type
   - Creates fix tasks
   - Fixes formatting errors (citations)

4. epidemiology-advisor
   INPUT: 15 structural competency flagged mechanisms
   TASK: Expert review of flagged mechanisms:
     - Assess if truly problematic or false positive
     - Provide correction guidance
   OUTPUT: Expert assessment:
     - 10 confirmed issues (need reframing)
     - 5 false positives (actually okay)

5. MAIN CONVERSATION
   - Revises 10 problematic mechanisms
   - Re-validates with mechanism-validator
   - Updates mechanism bank
   - Generates quality report for stakeholders
```

---

## Documentation Workflows

### Pattern 8: Complete API Documentation Generation

**Goal**: Generate comprehensive, up-to-date API documentation

**Agents**: api-documenter

**Steps**:

```
1. USER REQUEST
   "Generate complete API documentation for all endpoints"

2. api-documenter
   INPUT: All route files in backend/routes/
   TASK: Generate full API documentation:
     - OpenAPI 3.0 specification
     - Endpoint descriptions
     - Parameter documentation
     - Response schemas
     - Error codes
     - Authentication docs
     - Rate limiting policies
     - Usage examples (curl, Python, JavaScript, TypeScript)
   OUTPUT: Complete documentation package:
     - openapi.yaml (OpenAPI spec)
     - API_REFERENCE.md (human-readable)
     - QUICK_START.md (getting started guide)
     - ERROR_CODES.md (error reference)
     - Code examples directory

3. MAIN CONVERSATION
   - Reviews generated docs
   - Tests all code examples
   - Deploys docs to documentation site
   - Announces to users
```

---

## Troubleshooting Workflows

### Pattern 9: Debug LLM Extraction Issues

**Goal**: Diagnose and fix systematic LLM extraction problems

**Agents**: mechanism-validator (diagnosis) → llm-prompt-engineer (fix)

**Steps**:

```
1. USER REPORTS ISSUE
   "Mechanisms are missing directionality or have incorrect +/−"

2. mechanism-validator
   INPUT: Recent 100 extractions
   TASK: Audit for directionality issues:
     - Count missing directionality
     - Identify incorrect assignments
     - Pattern detection
   OUTPUT: Diagnostic report:
     - 12% missing directionality field
     - 8% incorrect directionality
     - Pattern: Confusion with protective factors
       (e.g., "Income reduces food insecurity" marked positive)

3. llm-prompt-engineer
   INPUT: Diagnostic report, current prompt
   TASK: Fix directionality issues:
     - Add explicit directionality definition
     - Provide decision tree
     - Add few-shot examples of tricky cases
     - Include verification step
   OUTPUT: Improved prompt with:
     - Clear positive/negative definitions
     - Template: "When [source] INCREASES, [target] _____"
     - Examples of protective factors correctly labeled
     - Self-check instruction

4. MAIN CONVERSATION
   - Tests on 20 papers
   - Measures improvement

5. mechanism-validator
   INPUT: 20 new extractions
   TASK: Verify fix
   OUTPUT: Directionality accuracy: 98% (vs. 80% before)

6. MAIN CONVERSATION
   - Commits improved prompt
   - Schedules re-processing of problematic mechanisms
```

---

## Advanced Patterns

### Pattern 10: Parallel Agent Execution (Simulated)

**Goal**: Maximize efficiency by running independent agents "in parallel"

**Note**: Agents don't truly run in parallel, but can be queued in single message

**Steps**:

```
1. USER REQUEST
   "I have 3 independent tasks:
   - Review mechanism extraction prompts
   - Audit API security
   - Generate tests for data pipeline"

2. MAIN CONVERSATION (Sequential execution, but batched)
   Invokes agents sequentially but efficiently:

   A. llm-prompt-engineer
      Task: Review mechanism extraction prompts
      [Works independently]
      Returns: Prompt analysis and improvements

   B. code-reviewer
      Task: Audit API security
      [Works independently]
      Returns: Security audit report

   C. test-generator
      Task: Generate tests for data pipeline
      [Works independently]
      Returns: Test suite for pipeline

3. MAIN CONVERSATION
   - Receives all results
   - Presents unified summary to user
   - Coordinates follow-up actions
```

---

## Pattern Selection Guide

| Your Goal | Recommended Pattern |
|-----------|---------------------|
| Extract mechanisms from papers | Pattern 1: Full Discovery Pipeline |
| Fix LLM extraction quality | Pattern 2: Rapid Iteration |
| High-stakes mechanism review | Pattern 3: Expert-Driven Curation |
| Implement new API feature | Pattern 4: Feature Development with Full QA |
| Security audit | Pattern 5: Security-Focused Review |
| Build data scraper | Pattern 6: Build and Validate Pipeline |
| Quality check mechanism bank | Pattern 7: Mechanism Bank Audit |
| Generate API docs | Pattern 8: Complete Documentation |
| Debug extraction issues | Pattern 9: Debug LLM Extraction |
| Multiple independent tasks | Pattern 10: Parallel Execution |

---

## Creating Custom Patterns

### Template for New Workflow Pattern

```markdown
### Pattern X: [Workflow Name]

**Goal**: [What you're trying to accomplish]

**Agents**: [List agents involved]

**Steps**:
1. [Step description]
   Agent: [Which agent]
   Input: [What it receives]
   Task: [What it does]
   Output: [What it returns]

2. [Next step]
   ...

**Expected Outcome**: [Final deliverable]

**Variations**: [Alternative approaches]
```

---

## Best Practices for Workflow Coordination

### 1. Plan Before Executing
- Identify all required agents upfront
- Determine dependencies (which must run first)
- Prepare necessary context for each agent

### 2. Validate Between Stages
- Don't assume agent output is perfect
- Verify critical results before proceeding
- User review at key milestones

### 3. Handle Failures Gracefully
- If agent returns unexpected result, don't proceed blindly
- Revise and re-run if needed
- Escalate to user for ambiguous cases

### 4. Document Decisions
- Track why certain agents were chosen
- Document deviations from standard patterns
- Note performance metrics (time, quality)

### 5. Iterate and Improve
- Measure workflow effectiveness
- Identify bottlenecks
- Refine patterns based on experience

---

**Remember**: These patterns are starting points. Adapt them to your specific needs, and don't hesitate to create custom workflows that combine agents in novel ways.
