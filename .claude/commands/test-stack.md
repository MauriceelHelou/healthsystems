# Multi-Stack Test Orchestration Command

You are helping run tests across the HealthSystems Platform's multi-tier architecture (backend Python, frontend React, mechanism validation).

## Context

The project has three separate test suites:
- **Backend**: pytest in `backend/tests/` (requires PostgreSQL, Redis)
- **Frontend**: Jest in `frontend/` (unit + accessibility tests)
- **Mechanisms**: JSON schema validation in `mechanism-bank/`

Each has different requirements, and running all tests manually is cumbersome.

## Command Argument Parsing

Parse the user's command to determine scope:

- **`/test-stack`** or **`/test-stack all`** - Run all test suites
- **`/test-stack backend`** - Backend tests only
- **`/test-stack frontend`** - Frontend tests only
- **`/test-stack mechanisms`** - Mechanism validation only
- **`/test-stack changed`** - Smart mode: only test what changed (detect from git)
- **`/test-stack quick`** - Fast mode: skip integration tests, run unit tests only

---

## Intelligent Test Selection

Before running tests, analyze what changed:

1. **Check git status** to see modified files:
   ```bash
   git status --short
   git diff --name-only HEAD
   ```

2. **Determine scope**:
   - Changes in `backend/` → run backend tests
   - Changes in `frontend/` → run frontend tests
   - Changes in `mechanism-bank/mechanisms/` → run mechanism validation
   - Changes in `mechanism-bank/schema/` → run ALL mechanism validation
   - Changes in `.github/workflows/` → warn about CI changes
   - No changes → ask user what to run

3. **Environment check**:
   - Check if Docker services are running (for integration tests):
     ```bash
     docker ps --filter "name=healthsystems" --format "{{.Names}}"
     ```
   - If services not running and integration tests requested:
     - Offer to start services: `docker-compose up -d`
     - Or skip integration tests

---

## Sub-Command: ALL

**Purpose:** Run complete test suite across all tiers.

### Steps:

1. **Pre-flight checks**:
   - Verify Docker services running (postgres, redis)
   - Check Python virtual environment activated
   - Check Node.js dependencies installed

2. **Run tests in parallel** (separate terminal windows/processes):

   **Backend tests:**
   ```bash
   cd backend
   pytest tests/ -v --cov=app --cov-report=html --cov-report=term
   ```

   **Frontend tests:**
   ```bash
   cd frontend
   npm test -- --coverage --watchAll=false
   ```

   **Mechanism validation:**
   ```bash
   cd mechanism-bank
   python scripts/validate_mechanisms.py
   ```

3. **Aggregate results**:
   - Collect pass/fail status from each suite
   - Aggregate coverage metrics
   - Report total test count and time

4. **Display unified report**:
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
   ✓ Coverage: 87.1% (target: 80%)
   ✓ Accessibility: All tests passed
   ⏱ Duration: 8.7s

   Mechanisms (validation)
   ✓ 12 mechanisms validated
   ✓ All schemas valid
   ⏱ Duration: 0.3s

   ═══════════════════════════════════════════════════════════
   OVERALL: ✓ ALL TESTS PASSED
   Total: 228 tests in 21.4s
   ═══════════════════════════════════════════════════════════
   ```

5. **Coverage reports**:
   - Backend HTML report: `backend/htmlcov/index.html`
   - Frontend HTML report: `frontend/coverage/lcov-report/index.html`
   - Offer to open in browser

6. **Failure handling**:
   - If any suite fails, show detailed errors
   - Suggest fixes based on common issues
   - Offer to run just the failed tests

---

## Sub-Command: BACKEND

**Purpose:** Run backend Python tests with pytest.

### Steps:

1. **Check environment**:
   - Docker services running? (postgres, redis)
   - If not: offer to start or skip integration tests

2. **Determine test scope**:
   - **Default**: All tests with coverage
   - **Quick mode**: Unit tests only (skip integration)
   - **Specific**: If user mentions file/module, run only that

3. **Run pytest**:
   ```bash
   cd backend
   pytest tests/ -v --cov=app --cov-report=html --cov-report=term --cov-fail-under=80
   ```

   For quick mode:
   ```bash
   pytest tests/unit/ -v --cov=app
   ```

4. **Parse results**:
   - Number of passed/failed/skipped tests
   - Coverage percentage
   - Slow tests (>1s)
   - Failed test details

5. **Coverage analysis**:
   - Check if meets 80% threshold
   - Identify uncovered modules
   - Suggest areas needing tests

6. **Common failure suggestions**:
   - Database connection errors → check Docker
   - Import errors → check dependencies (`pip install -e .`)
   - Async errors → check pytest-asyncio plugin
   - Fixture errors → check conftest.py

---

## Sub-Command: FRONTEND

**Purpose:** Run frontend React tests with Jest.

### Steps:

1. **Check environment**:
   - Node modules installed? Check `frontend/node_modules/`
   - If not: offer to run `npm install`

2. **Run Jest**:
   ```bash
   cd frontend
   npm test -- --coverage --watchAll=false
   ```

3. **Parse results**:
   - Test suites passed/failed
   - Coverage by category (statements, branches, functions, lines)
   - Accessibility test results (jest-axe)

4. **Accessibility focus**:
   - Report any WCAG violations
   - Highlight components failing a11y tests
   - Suggest fixes (ARIA labels, semantic HTML, keyboard navigation)

5. **Coverage gaps**:
   - Identify untested components
   - Suggest component test templates
   - Check for integration test needs

6. **Common failure suggestions**:
   - Module not found → check imports, run `npm install`
   - Timeout errors → increase timeout for async tests
   - DOM errors → check React Testing Library queries
   - Accessibility violations → specific WCAG fix suggestions

---

## Sub-Command: MECHANISMS

**Purpose:** Validate mechanism YAML files against JSON schema.

### Steps:

1. **Run validation script**:
   ```bash
   cd mechanism-bank
   python scripts/validate_mechanisms.py
   ```

2. **Parse results**:
   - Number of mechanisms validated
   - Schema compliance
   - Required field checks
   - Value type validation

3. **Error reporting**:
   - Show specific validation errors with line numbers
   - Suggest fixes for common issues:
     - Missing required fields
     - Invalid value types
     - Malformed YAML
     - Citation formatting issues

4. **Lint YAML**:
   - Check indentation (should be 2 spaces)
   - Check for trailing whitespace
   - Validate special characters in strings

5. **Content validation** (beyond schema):
   - Effect sizes in plausible range (-5 to 5 for log ratios)
   - Confidence intervals make sense (lower < upper)
   - Citations have DOI or proper format
   - Dates are valid

---

## Sub-Command: CHANGED

**Purpose:** Smart test runner - only test what changed.

### Steps:

1. **Git analysis**:
   ```bash
   git diff --name-only HEAD
   git status --short
   ```

2. **Map changes to test suites**:
   - `backend/**/*.py` → backend tests
   - `frontend/**/*.{ts,tsx,js,jsx}` → frontend tests
   - `mechanism-bank/mechanisms/**/*.yaml` → mechanism validation
   - `backend/app/models/*.py` → backend tests + check migrations
   - `frontend/src/components/**` → component tests + accessibility

3. **Determine minimal test set**:
   - If only 1 file changed → test just that module
   - If multiple files → test affected suites
   - If schema changed → test everything

4. **Run targeted tests**:
   - Backend: `pytest tests/test_<module>.py`
   - Frontend: `npm test -- <ComponentName>`
   - Mechanisms: validate only changed files

5. **Report**:
   ```
   📊 Detected changes:
   - backend/app/services/bayesian.py
   - backend/tests/test_bayesian.py

   🎯 Running targeted tests:
   ✓ backend: pytest tests/test_bayesian.py

   Results: 15 tests passed in 2.1s
   ```

---

## Sub-Command: QUICK

**Purpose:** Fast feedback loop - unit tests only, skip integration tests.

### Steps:

1. **Backend quick tests**:
   ```bash
   pytest tests/unit/ -v --maxfail=3
   ```
   - Skip `tests/integration/`
   - Stop after 3 failures (--maxfail)
   - No coverage report (faster)

2. **Frontend quick tests**:
   ```bash
   npm test -- --coverage=false --maxWorkers=4
   ```
   - Skip coverage calculation
   - Parallel execution

3. **Mechanisms**:
   - Run validation (already fast)

4. **Report**:
   - Focus on pass/fail, not metrics
   - Show only failures
   - Estimated time saved vs. full suite

---

## Environment Troubleshooting

### Docker Services Not Running

```bash
# Check status
docker ps --filter "name=healthsystems"

# If not running, offer to start:
docker-compose up -d postgres redis

# Wait for health checks
docker-compose ps
```

### Python Environment Issues

```bash
# Check if venv activated
echo $VIRTUAL_ENV  # (Linux/Mac)
echo %VIRTUAL_ENV%  # (Windows)

# Suggest activation:
# Linux/Mac: source venv/bin/activate
# Windows: venv\Scripts\activate

# Check dependencies
pip list | grep -E "pytest|fastapi|sqlalchemy"
```

### Node Dependencies Issues

```bash
# Check if node_modules exists
ls frontend/node_modules

# Suggest install
cd frontend && npm install
```

---

## Coverage Reporting

After tests with coverage:

1. **Show coverage summary** in terminal

2. **Identify gaps**:
   - Modules below 80% threshold
   - Untested files
   - Untested branches

3. **Generate reports**:
   - HTML reports for detailed view
   - Terminal summary for quick check

4. **Suggest improvements**:
   - "Add tests for `app/services/equilibrium.py` (current: 45%)"
   - "Missing branch coverage in `app/api/routes.py` lines 89-92"

---

## Integration with Pre-commit

If tests fail and user is about to commit:

1. **Warn**: Tests failing, commit blocked
2. **Show failures**: Specific test failures
3. **Suggest**: Fix tests before committing
4. **Offer**: Run quick tests to validate fixes

---

## Performance Optimization

- Run test suites in parallel where possible
- Cache test results (pytest --cache)
- Skip slow tests in quick mode
- Use markers for test categorization:
  - `@pytest.mark.slow`
  - `@pytest.mark.integration`
  - `@pytest.mark.unit`

---

## Output Formatting

Use clear visual hierarchy:
- ✓ for success (green)
- ✗ for failure (red)
- ⚠ for warnings (yellow)
- ⏱ for timing
- 📊 for metrics
- 🎯 for targeted tests

Make output scannable and actionable.
