# PROMPT 5: Reorganize Test Files

## Context
Test files are **scattered throughout the codebase** in inconsistent locations, making them hard to find and maintain. Some tests are in `frontend/src/tests/`, others are co-located with components, and backend tests mix with source code.

## Current State

### Current Test File Locations

**Frontend tests (scattered):**
```
frontend/
├── src/
│   ├── tests/                          # Shared test utilities
│   │   ├── mocks/
│   │   ├── utils/
│   │   └── setup/
│   ├── views/
│   │   └── SystemsMapView.test.tsx     # ❌ Inconsistent location
│   ├── visualizations/
│   │   └── MechanismGraph.test.tsx     # ❌ Inconsistent location
│   └── setupTests.ts                   # ❌ Should be in tests/
│
├── e2e/
│   ├── diagnostic-console.spec.ts
│   └── hierarchical-diagram-debug.spec.ts
│
└── test-results/                       # ❌ Generated, should be in .gitignore
    └── ...
```

**Backend tests (inconsistent):**
```
backend/
├── api/
│   └── routes/
│       └── nodes_test.py               # ❌ Naming inconsistent (_test vs test_)
├── test_crisis_endpoints.py            # ❌ Root level
├── verify_test_setup.py                # ❌ Not a real test
└── (no tests/ directory)
```

### Problems

1. **Discoverability:** Hard to find all tests
2. **Naming inconsistency:** `_test.py` vs `test_.py`, `.test.tsx` vs `.spec.ts`
3. **Generated files committed:** `test-results/`, `playwright-report/`
4. **No test organization:** Unit vs integration vs e2e mixed

## Target Architecture

### Frontend Test Organization

```
frontend/
├── src/
│   └── (no test files here)
│
├── tests/
│   ├── unit/                           # Unit tests (mirrors src/ structure)
│   │   ├── views/
│   │   │   └── SystemsMapView.test.tsx
│   │   ├── visualizations/
│   │   │   └── MechanismGraph.test.tsx
│   │   ├── hooks/
│   │   │   ├── usePathfinding.test.tsx
│   │   │   └── useCrisisSubgraph.test.tsx
│   │   └── utils/
│   │       ├── api.test.ts
│   │       └── transformers.test.ts
│   │
│   ├── integration/                    # Integration tests
│   │   ├── pathfinder-flow.test.tsx
│   │   └── crisis-explorer-flow.test.tsx
│   │
│   ├── e2e/                            # End-to-end (Playwright)
│   │   ├── systems-map.spec.ts
│   │   ├── pathfinder.spec.ts
│   │   └── crisis-explorer.spec.ts
│   │
│   ├── setup/                          # Test setup/config
│   │   ├── setupTests.ts
│   │   └── testUtils.tsx
│   │
│   └── mocks/                          # Shared mocks
│       ├── handlers.ts
│       └── mockData.ts
│
├── .gitignore                          # Add test-results/, playwright-report/
└── jest.config.js                      # Update paths
```

### Backend Test Organization

```
backend/
├── tests/                              # All tests here
│   ├── unit/                           # Unit tests
│   │   ├── test_models.py
│   │   ├── test_transformers.py
│   │   └── algorithms/
│   │       └── test_bayesian_weighting.py
│   │
│   ├── integration/                    # Integration tests
│   │   └── api/
│   │       ├── test_mechanisms.py
│   │       ├── test_nodes.py
│   │       └── test_pathways.py
│   │
│   ├── fixtures/                       # Shared test data
│   │   ├── sample_mechanisms.yml
│   │   └── sample_nodes.json
│   │
│   └── conftest.py                     # Pytest configuration
│
└── (source code has no test files)
```

## Implementation Steps

### Step 1: Setup Frontend Test Directories

```bash
cd frontend

# Create new structure
mkdir -p tests/unit/views
mkdir -p tests/unit/visualizations
mkdir -p tests/unit/hooks
mkdir -p tests/unit/utils
mkdir -p tests/integration
mkdir -p tests/e2e
mkdir -p tests/setup
mkdir -p tests/mocks
```

### Step 2: Move Frontend Test Files

```bash
cd frontend

# Move existing test files
git mv src/views/SystemsMapView.test.tsx tests/unit/views/
git mv src/visualizations/MechanismGraph.test.tsx tests/unit/visualizations/

# Move setup files
git mv src/setupTests.ts tests/setup/
git mv src/tests/utils/test-utils.tsx tests/setup/testUtils.tsx

# Move mocks
git mv src/tests/mocks/handlers.ts tests/mocks/
git mv src/tests/mocks/mockData.ts tests/mocks/

# Move e2e tests
git mv e2e/ tests/e2e/

# Remove old directory
rm -rf src/tests/
```

### Step 3: Update Frontend Test Configs

**File: `frontend/jest.config.js`**

```javascript
export default {
  preset: 'ts-jest',
  testEnvironment: 'jsdom',

  // Update test locations
  roots: ['<rootDir>/tests'],
  testMatch: [
    '**/tests/unit/**/*.test.{ts,tsx}',
    '**/tests/integration/**/*.test.{ts,tsx}',
  ],

  // Setup files
  setupFilesAfterEnv: ['<rootDir>/tests/setup/setupTests.ts'],

  // Module paths
  modulePaths: ['<rootDir>/src'],
  moduleNameMapper: {
    '^@/(.*)$': '<rootDir>/src/$1',
    '\\.(css|less|scss|sass)$': 'identity-obj-proxy',
  },

  // Coverage
  collectCoverageFrom: [
    'src/**/*.{ts,tsx}',
    '!src/**/*.d.ts',
    '!src/main.tsx',
  ],
  coverageDirectory: '<rootDir>/coverage',
  coverageReporters: ['text', 'lcov', 'html'],
};
```

**File: `frontend/playwright.config.ts`**

```typescript
import { defineConfig } from '@playwright/test';

export default defineConfig({
  // Update test directory
  testDir: './tests/e2e',

  // Output directories
  outputDir: './test-results',

  use: {
    baseURL: 'http://localhost:5173',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
  },

  webServer: {
    command: 'npm run dev',
    port: 5173,
    reuseExistingServer: !process.env.CI,
  },
});
```

**File: `frontend/tsconfig.json`**

```json
{
  "compilerOptions": {
    // ... existing config
    "paths": {
      "@/*": ["./src/*"],
      "@tests/*": ["./tests/*"]
    }
  },
  "include": [
    "src",
    "tests"
  ]
}
```

### Step 4: Update Test Imports

**Example: Update a moved test file**

```typescript
// tests/unit/views/SystemsMapView.test.tsx

// OLD imports
import { render } from '../../tests/utils/test-utils';
import { mockData } from '../../tests/mocks/mockData';

// NEW imports
import { render } from '@tests/setup/testUtils';
import { mockData } from '@tests/mocks/mockData';
```

Run this find-replace across all test files:

```bash
cd frontend/tests

# Update import paths
find . -name "*.test.tsx" -o -name "*.test.ts" | xargs sed -i \
  's|from '\''../../tests/|from '\''@tests/|g'

find . -name "*.test.tsx" -o -name "*.test.ts" | xargs sed -i \
  's|from '\''../tests/|from '\''@tests/|g'
```

### Step 5: Setup Backend Test Directories

```bash
cd backend

# Create structure
mkdir -p tests/unit/algorithms
mkdir -p tests/integration/api
mkdir -p tests/fixtures
```

### Step 6: Move Backend Test Files

```bash
cd backend

# Move API tests
git mv api/routes/nodes_test.py tests/integration/api/test_nodes.py
git mv test_crisis_endpoints.py tests/integration/api/test_crisis_endpoints.py

# Remove verification script (not a real test)
git rm verify_test_setup.py

# Create conftest if needed
touch tests/conftest.py
```

### Step 7: Create Backend Test Config

**File: `backend/pytest.ini`**

```ini
[pytest]
# Test discovery
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*

# Output
addopts =
    --verbose
    --tb=short
    --strict-markers
    -ra
    --cov=.
    --cov-report=html
    --cov-report=term

# Coverage
[coverage:run]
source = .
omit =
    tests/*
    */migrations/*
    */venv/*
    */env/*

[coverage:report]
exclude_lines =
    pragma: no cover
    def __repr__
    raise NotImplementedError
    if __name__ == .__main__.:
```

**File: `backend/tests/conftest.py`**

```python
"""
Pytest configuration and fixtures.
"""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pathlib import Path

from models import Base


@pytest.fixture(scope="session")
def test_db():
    """Create test database."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    return engine


@pytest.fixture
def db_session(test_db):
    """Create test database session."""
    SessionLocal = sessionmaker(bind=test_db)
    session = SessionLocal()

    yield session

    session.close()


@pytest.fixture
def sample_mechanism():
    """Load sample mechanism from fixtures."""
    fixture_path = Path(__file__).parent / "fixtures" / "sample_mechanisms.yml"
    # Load and return
    pass
```

### Step 8: Update .gitignore

**File: `frontend/.gitignore`**

```gitignore
# Testing
test-results/
playwright-report/
coverage/
.nyc_output/

# Test screenshots/videos (if needed, otherwise commit)
tests/e2e/screenshots/
tests/e2e/videos/
```

**File: `backend/.gitignore`**

```gitignore
# Testing
.pytest_cache/
.coverage
htmlcov/
coverage.xml
*.cover

# Test databases
test.db
test.db-journal
```

### Step 9: Update package.json Scripts

**File: `frontend/package.json`**

```json
{
  "scripts": {
    "test": "jest",
    "test:unit": "jest tests/unit",
    "test:integration": "jest tests/integration",
    "test:e2e": "playwright test",
    "test:coverage": "jest --coverage",
    "test:watch": "jest --watch"
  }
}
```

### Step 10: Update CI/CD

**File: `.github/workflows/test.yml`**

```yaml
name: Tests

on: [push, pull_request]

jobs:
  frontend-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'

      - name: Install dependencies
        working-directory: frontend
        run: npm ci

      - name: Run unit tests
        working-directory: frontend
        run: npm run test:unit

      - name: Run integration tests
        working-directory: frontend
        run: npm run test:integration

      - name: Run e2e tests
        working-directory: frontend
        run: npm run test:e2e

      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          files: ./frontend/coverage/lcov.info

  backend-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        working-directory: backend
        run: pip install -r requirements.txt

      - name: Run tests
        working-directory: backend
        run: pytest

      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          files: ./backend/coverage.xml
```

## Migration Checklist

### Phase 1: Preparation (1 hour)
- [ ] Create all new test directories
- [ ] Backup current test files
- [ ] Update .gitignore first

### Phase 2: Frontend Migration (2 hours)
- [ ] Move all test files to new locations
- [ ] Update jest.config.js
- [ ] Update playwright.config.ts
- [ ] Update tsconfig.json paths
- [ ] Fix all import statements
- [ ] Run `npm test` to verify

### Phase 3: Backend Migration (1 hour)
- [ ] Move all test files
- [ ] Create pytest.ini
- [ ] Create conftest.py
- [ ] Rename tests (test_* convention)
- [ ] Run `pytest` to verify

### Phase 4: Documentation (30 minutes)
- [ ] Update README with test instructions
- [ ] Document test organization
- [ ] Update CI/CD configs

### Phase 5: Verification (30 minutes)
- [ ] All tests passing locally
- [ ] CI/CD pipeline passing
- [ ] Test coverage reports working
- [ ] Commit with message: "refactor: reorganize tests into standard structure"

## Testing Requirements

### Verify Everything Works

```bash
# Frontend
cd frontend
npm test                    # Should find all tests
npm run test:unit           # Only unit tests
npm run test:integration    # Only integration tests
npm run test:e2e            # Only e2e tests
npm run test:coverage       # Generate coverage

# Backend
cd backend
pytest                      # Should find all tests
pytest tests/unit          # Only unit tests
pytest tests/integration   # Only integration tests
pytest --cov               # Generate coverage
```

## Success Criteria

- ✅ All frontend tests in `frontend/tests/`
- ✅ All backend tests in `backend/tests/`
- ✅ Consistent naming: `test_*.py`, `*.test.tsx`
- ✅ Test results not committed to git
- ✅ All tests passing
- ✅ Coverage reports working
- ✅ CI/CD pipeline updated and passing
- ✅ Documentation updated

## Estimated Effort
**4 hours** (2 hours frontend, 1 hour backend, 1 hour verification)
