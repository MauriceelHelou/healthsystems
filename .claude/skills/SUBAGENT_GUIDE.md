# HealthSystems Platform Subagent Guide

**Last Updated**: November 17, 2025
**Purpose**: Complete guide to using specialized subagents for the HealthSystems Platform

---

## Table of Contents

1. [Overview](#overview)
2. [Available Subagents](#available-subagents)
3. [How Subagents Work](#how-subagents-work)
4. [When to Use Each Subagent](#when-to-use-each-subagent)
5. [Invocation Methods](#invocation-methods)
6. [Common Workflows](#common-workflows)
7. [Best Practices](#best-practices)
8. [Troubleshooting](#troubleshooting)

---

## Overview

The HealthSystems Platform uses **specialized subagents** to handle domain-specific tasks with deep expertise. Each subagent has:

- **Dedicated context window**: Separate from main conversation
- **Specialized system prompt**: Tailored instructions for its domain
- **Specific tool access**: Only the tools needed for its job
- **Independent operation**: Works autonomously and returns results

**Benefits**:
- ✅ **Context preservation**: Main conversation stays focused on high-level coordination
- ✅ **Deep expertise**: Subagents have domain-specific knowledge (epidemiology, prompt engineering, etc.)
- ✅ **Efficiency**: Parallel-like work through task delegation
- ✅ **Consistency**: Reusable patterns across projects

---

## Available Subagents

### 1. **mechanism-validator**
**Purpose**: Validate mechanism YAML files for structural competency and scientific rigor

**Expertise**:
- Structural determinants of health framework
- Chicago citation style validation
- YAML schema compliance
- Equity-centered analysis

**Use for**:
- Validating mechanisms after LLM extraction
- Auditing mechanism bank for quality
- Checking structural competency framing
- Verifying citations and evidence ratings

**Location**: `.claude/agents/mechanism-validator.md`

---

### 2. **llm-prompt-engineer**
**Purpose**: Optimize LLM prompts for mechanism discovery and extraction quality

**Expertise**:
- Anthropic Claude prompt engineering
- Structural competency by design
- Few-shot learning and chain-of-thought
- Cost optimization

**Use for**:
- Improving extraction quality (missing fields, incorrect directionality)
- Fixing systematic errors (spatial variation detection)
- Designing prompts for new mechanism types
- Optimizing API costs

**Location**: `.claude/agents/llm-prompt-engineer.md`

---

### 3. **epidemiology-advisor**
**Purpose**: Expert review of mechanisms for epidemiological accuracy and causal logic

**Expertise**:
- Social epidemiology and causal inference
- Bradford Hill criteria and DAG logic
- Study design and evidence evaluation
- Health equity and intersectionality

**Use for**:
- Expert review of high-priority mechanisms
- Resolving causal logic ambiguities
- Validating theoretical pathways
- Assessing evidence quality

**Location**: `.claude/agents/epidemiology-advisor.md`

---

### 4. **code-reviewer**
**Purpose**: Review backend/frontend code for quality, security, and best practices

**Expertise**:
- FastAPI and Python best practices
- React/TypeScript patterns
- OWASP security standards
- WCAG 2.1 AA accessibility

**Use for**:
- Pre-PR code reviews
- Security vulnerability scans
- Performance optimization suggestions
- Accessibility compliance checks

**Location**: `.claude/agents/code-reviewer.md`

---

### 5. **test-generator**
**Purpose**: Generate comprehensive test suites for backend and frontend code

**Expertise**:
- pytest fixtures and patterns
- Jest and React Testing Library
- Edge case identification
- Integration testing strategies

**Use for**:
- Creating test suites for new features
- Improving test coverage
- Adding edge case tests
- Writing integration tests

**Location**: `.claude/agents/test-generator.md`

---

### 6. **api-documenter**
**Purpose**: Generate and maintain API documentation with OpenAPI specs

**Expertise**:
- OpenAPI/Swagger specifications
- API design patterns
- Developer experience best practices
- Multi-language code examples

**Use for**:
- Documenting new/modified API endpoints
- Generating OpenAPI specifications
- Creating integration guides
- Updating API reference docs

**Location**: `.claude/agents/api-documenter.md`

---

### 7. **data-pipeline-builder**
**Purpose**: Create and optimize ETL pipelines and data scrapers

**Expertise**:
- Census, CDC, EPA, BLS APIs
- Data validation and quality checks
- Error handling and retry logic
- Caching strategies

**Use for**:
- Building new data scrapers
- Creating ETL workflows
- Data validation logic
- Performance optimization

**Location**: `.claude/agents/data-pipeline-builder.md`

---

## How Subagents Work

### Lifecycle

```
1. Main conversation identifies need for specialized task
   ↓
2. Subagent invoked (explicitly or automatically)
   ↓
3. Subagent receives task description + context
   ↓
4. Subagent works independently in own context window
   ↓
5. Subagent returns comprehensive results
   ↓
6. Main conversation continues with results
```

### Key Properties

**Stateless**: Each invocation is independent (no memory of previous calls)

**Autonomous**: Subagent completes entire task before returning

**Specialized**: Deep expertise in narrow domain

**Isolated Context**: Main conversation context is preserved

---

## When to Use Each Subagent

### Decision Tree

```
Task: Adding mechanisms to bank
├─> Extract from papers? → [Main + llm-prompt-engineer]
├─> Validate extracted mechanisms? → [mechanism-validator]
├─> Expert review needed? → [epidemiology-advisor]
└─> Ready to commit → [Main handles git]

Task: Implementing new API feature
├─> Write the code? → [Main writes initial implementation]
├─> Review code quality? → [code-reviewer]
├─> Add tests? → [test-generator]
├─> Document API? → [api-documenter]
└─> Merge PR → [Main handles git]

Task: Building data pipeline
├─> Design pipeline? → [data-pipeline-builder]
├─> Review implementation? → [code-reviewer]
├─> Add tests? → [test-generator]
└─> Deploy → [Main handles deployment]
```

### Complexity Threshold

**Use subagent when**:
- Task requires deep domain expertise
- Quality assurance needed (validation, review)
- Specialized pattern/template needed
- Multiple files involved in similar task

**Don't use subagent when**:
- Simple, one-off task
- Quick clarification question
- Main conversation has sufficient context
- Task doesn't match any subagent's expertise

---

## Invocation Methods

### Method 1: Explicit Invocation

**Direct request to use specific agent**:

```
"Use the mechanism-validator agent to review this mechanism file."

"Ask the epidemiology-advisor to assess the causal logic of this pathway."

"Have the code-reviewer check the security of my API endpoints."
```

### Method 2: Automatic Invocation

**Claude automatically uses appropriate agent when task matches expertise**:

```
User: "Validate all mechanisms in the housing category."
→ Claude automatically invokes mechanism-validator

User: "My LLM extraction is missing spatial variation 40% of the time."
→ Claude automatically invokes llm-prompt-engineer

User: "Is this causal pathway epidemiologically sound?"
→ Claude automatically invokes epidemiology-advisor
```

### Method 3: Coordination (Multi-Agent Workflows)

**Main conversation coordinates multiple agents**:

```
User: "Extract mechanisms from these 10 papers, validate them, and commit to the bank."

Main Claude coordinates:
1. Uses llm-prompt-engineer to optimize prompts
2. Runs extraction
3. Delegates to mechanism-validator for quality check
4. Delegates to epidemiology-advisor for expert review
5. Main handles git commit after approvals
```

---

## Common Workflows

### Workflow 1: Mechanism Discovery End-to-End

```
1. User: "Discover mechanisms from 20 housing→health papers"

2. Main: "I'll coordinate this multi-step process."

3. llm-prompt-engineer:
   - Reviews current extraction prompts
   - Optimizes for housing domain
   - Returns improved prompt template

4. Main: Runs extraction with optimized prompts
   - Generates 50 candidate mechanisms

5. mechanism-validator:
   - Validates all 50 mechanisms
   - Returns: 45 approved, 5 need revision

6. Main: Presents validation report to user
   - Shows specific issues with 5 rejected mechanisms

7. User: "Revise the 5 and get expert review"

8. Main: Fixes issues based on validator feedback

9. epidemiology-advisor:
   - Reviews all 45 approved mechanisms
   - Provides epidemiological assessment
   - Flags 2 for additional evidence needed

10. Main: Creates final set of 43 validated mechanisms

11. Main: Commits to mechanism bank with structured commit message
```

### Workflow 2: API Feature Development

```
1. User: "Implement mechanism search API with full-text search"

2. Main: Implements search endpoint
   - POST /api/mechanisms/search
   - Full-text search with Elasticsearch

3. code-reviewer:
   - Reviews implementation
   - Finds: Missing rate limiting, no input sanitization
   - Suggests: Add caching, improve error handling

4. Main: Applies code-reviewer suggestions

5. test-generator:
   - Creates 15 test cases
   - Covers happy path, edge cases, error scenarios

6. Main: Runs tests, all pass

7. api-documenter:
   - Generates OpenAPI spec
   - Creates usage examples (curl, Python, JS)
   - Documents error codes

8. Main: Commits feature with docs and tests
```

### Workflow 3: Data Pipeline Creation

```
1. User: "Build EPA air quality data scraper for county-level data"

2. data-pipeline-builder:
   - Creates EPA API scraper class
   - Implements error handling and retries
   - Adds caching and rate limiting
   - Includes data validation

3. code-reviewer:
   - Reviews scraper code
   - Suggests: Add progress logging, improve exception handling

4. Main: Applies suggestions

5. test-generator:
   - Creates unit tests for scraper
   - Adds integration test with mock API

6. Main: Runs tests, commits pipeline
```

### Workflow 4: Prompt Optimization Cycle

```
1. User: "Extraction missing spatial variation 40% of the time"

2. llm-prompt-engineer:
   - Analyzes current prompt
   - Identifies issue: No explicit spatial variation checklist
   - Provides improved prompt with:
     * Explicit spatial variation questions
     * Few-shot examples
     * Mechanism-based inference guidance

3. Main: Updates prompt, tests on 20 papers

4. mechanism-validator:
   - Audits extraction results
   - Reports: Spatial variation detection improved to 85%

5. llm-prompt-engineer:
   - Reviews remaining misses
   - Further refines prompt

6. Main: Final test shows 90% detection

7. Main: Commits new prompt version with performance metrics
```

---

## Best Practices

### 1. Clear Task Specification

**✅ Good**:
```
"Use mechanism-validator to check these 10 mechanisms for structural competency,
citation format, and equity considerations. Return a detailed report for each."
```

**❌ Vague**:
```
"Check some mechanisms."
```

### 2. Provide Sufficient Context

**✅ Good**:
```
"The LLM extraction for housing mechanisms is missing spatial variation when
climate or urbanicity are mentioned but not explicitly labeled as 'geographic differences.'
Use llm-prompt-engineer to fix this systematic issue."
```

**❌ Insufficient**:
```
"Improve the prompts."
```

### 3. Use Right Agent for the Job

**✅ Correct**:
```
Structural competency question → epidemiology-advisor
Prompt optimization → llm-prompt-engineer
Code security → code-reviewer
```

**❌ Wrong Agent**:
```
Structural competency question → code-reviewer
API documentation → test-generator
```

### 4. Chain Agents Appropriately

**✅ Good Sequence**:
```
1. llm-prompt-engineer (optimize prompts)
2. Main (run extraction)
3. mechanism-validator (validate outputs)
4. epidemiology-advisor (expert review)
```

**❌ Wrong Order**:
```
1. mechanism-validator (before extraction exists)
2. llm-prompt-engineer (after extraction already done)
```

### 5. Don't Overuse Agents

**When NOT to use agents**:
- Simple questions answerable in main conversation
- Tasks that don't match any agent's expertise
- When you just need clarification, not deep analysis

**Use main conversation for**:
- Coordination and orchestration
- Git operations (commits, branches)
- High-level planning
- User communication

---

## Troubleshooting

### Issue: Agent returns incomplete results

**Solution**: Provide more specific task description and expected outputs

```
❌ "Review this code"
✅ "Review this code for security vulnerabilities (OWASP Top 10),
   performance issues (N+1 queries, caching), and accessibility (WCAG 2.1 AA)"
```

### Issue: Wrong agent invoked automatically

**Solution**: Explicitly specify which agent to use

```
"Use the epidemiology-advisor agent to..."
```

### Issue: Agent takes too long / times out

**Solution**: Break task into smaller chunks

```
❌ "Validate all 500 mechanisms"
✅ "Validate these 50 housing mechanisms" (repeat in batches)
```

### Issue: Agent results contradict each other

**Example**: mechanism-validator approves but epidemiology-advisor rejects

**Solution**:
- Validator checks schema/format/structure
- Epidemiologist checks causal logic/evidence
- Both can be correct from their perspective
- Main conversation arbitrates and asks clarifying questions

### Issue: Agent doesn't have needed context

**Solution**: Provide file paths and specific details in request

```
❌ "Review the API code"
✅ "Review the mechanism search API in backend/routes/mechanisms.py,
   specifically the POST /search endpoint (lines 45-89)"
```

---

## Quick Reference

| Task | Primary Agent | Secondary Agents |
|------|--------------|------------------|
| Extract mechanisms from papers | llm-prompt-engineer | mechanism-validator |
| Validate mechanism quality | mechanism-validator | epidemiology-advisor |
| Expert causal logic review | epidemiology-advisor | - |
| Optimize LLM prompts | llm-prompt-engineer | mechanism-validator (feedback) |
| Review code quality | code-reviewer | - |
| Generate test suites | test-generator | - |
| Document API endpoints | api-documenter | - |
| Build data scrapers | data-pipeline-builder | code-reviewer, test-generator |
| Security audit | code-reviewer | - |
| Accessibility check | code-reviewer | - |

---

## Getting Help

**Questions about agents**:
- Read agent file: `.claude/agents/<agent-name>.md`
- Check workflow patterns: `.claude/skills/WORKFLOW_PATTERNS.md`
- See invocation reference: `.claude/skills/AGENT_INVOCATION_REFERENCE.md`

**Agent not working as expected**:
1. Check agent description in frontmatter (`when_to_use`)
2. Review examples in agent file
3. Provide more specific task description
4. Try explicit invocation instead of automatic

**Need new agent**:
- Identify gap in current agent coverage
- Create new agent file in `.claude/agents/`
- Follow existing agent template structure
- Add to this guide

---

**Remember**: Agents are tools to amplify your productivity. Use them strategically for tasks that benefit from specialized expertise, and coordinate from the main conversation for high-level workflows.
