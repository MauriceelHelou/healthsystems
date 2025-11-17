# Test Generation Prompt

Use this template when generating comprehensive tests for new features, ensuring 80% coverage and high quality standards.

## Test Generation Strategy

### For Backend (Python/pytest)

#### 1. API Endpoint Tests

**For each endpoint, generate:**

```python
# tests/test_api/test_[module]_endpoints.py

import pytest
from httpx import AsyncClient
from app.main import app

class Test[EndpointName]:
    """Tests for [endpoint description]"""

    @pytest.mark.asyncio
    async def test_success_case(self, client: AsyncClient):
        """Test successful request with valid data"""
        response = await client.get("/api/v1/[endpoint]")
        assert response.status_code == 200
        assert "expected_field" in response.json()

    @pytest.mark.asyncio
    async def test_with_query_params(self, client: AsyncClient):
        """Test with various query parameters"""
        response = await client.get("/api/v1/[endpoint]?param=value")
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_validation_error(self, client: AsyncClient):
        """Test with invalid input"""
        response = await client.post("/api/v1/[endpoint]", json={"invalid": "data"})
        assert response.status_code == 422  # Validation error

    @pytest.mark.asyncio
    async def test_not_found(self, client: AsyncClient):
        """Test with non-existent resource"""
        response = await client.get("/api/v1/[endpoint]/999999")
        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_unauthorized(self, client: AsyncClient):
        """Test without authentication (if required)"""
        # Remove auth headers
        response = await client.get("/api/v1/[endpoint]")
        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_pagination(self, client: AsyncClient):
        """Test pagination parameters"""
        response = await client.get("/api/v1/[endpoint]?limit=10&offset=0")
        assert response.status_code == 200
        assert len(response.json()["items"]) <= 10

    @pytest.mark.asyncio
    async def test_filtering(self, client: AsyncClient):
        """Test filtering parameters"""
        response = await client.get("/api/v1/[endpoint]?filter=value")
        assert response.status_code == 200
        # Verify filtering logic
```

#### 2. Service Layer Tests

**For each service function:**

```python
# tests/test_services/test_[module]_service.py

import pytest
from app.services.[module] import [ServiceClass]

class Test[ServiceFunction]:
    """Tests for [service function description]"""

    def test_basic_functionality(self):
        """Test core functionality with typical inputs"""
        result = service_function(input_data)
        assert result is not None
        assert expected_property in result

    def test_edge_cases(self):
        """Test edge cases"""
        # Empty input
        assert service_function([]) == expected_empty_result

        # Single item
        assert service_function([single_item]) == expected_single_result

        # Large input
        assert service_function(large_input) == expected_large_result

    def test_error_handling(self):
        """Test error conditions"""
        with pytest.raises(ValueError):
            service_function(invalid_input)

    @pytest.mark.parametrize("input,expected", [
        (input1, expected1),
        (input2, expected2),
        (input3, expected3),
    ])
    def test_multiple_scenarios(self, input, expected):
        """Test multiple scenarios with parametrization"""
        assert service_function(input) == expected

    def test_with_mocked_dependencies(self, mocker):
        """Test with mocked external dependencies"""
        mock_db = mocker.patch('app.services.[module].get_db')
        mock_db.return_value = mock_data

        result = service_function(input_data)
        assert result == expected_with_mock
        mock_db.assert_called_once()
```

#### 3. Bayesian Model Tests

**For PyMC models:**

```python
# tests/test_bayesian/test_[model]_model.py

import pytest
import pymc as pm
import numpy as np
from app.services.bayesian_weighting import build_model

class Test[ModelName]:
    """Tests for [model description]"""

    def test_model_builds(self):
        """Test that model builds without errors"""
        model = build_model(test_mechanisms, test_context)
        assert model is not None
        assert isinstance(model, pm.Model)

    def test_model_structure(self):
        """Test model has expected variables"""
        model = build_model(test_mechanisms, test_context)
        assert 'effect_size' in model.named_vars
        assert 'moderator_weights' in model.named_vars

    def test_prior_predictive(self):
        """Test prior predictive sampling"""
        model = build_model(test_mechanisms, test_context)
        with model:
            prior_samples = pm.sample_prior_predictive(samples=1000)

        # Check prior samples in reasonable range
        assert np.all(prior_samples.prior['effect_size'] > -5)
        assert np.all(prior_samples.prior['effect_size'] < 5)

    @pytest.mark.slow
    def test_sampling(self):
        """Test MCMC sampling (slow test)"""
        model = build_model(test_mechanisms, test_context)
        with model:
            trace = pm.sample(draws=100, tune=100, chains=2)

        # Check convergence
        assert trace.sample_stats['diverging'].sum() == 0

    def test_posterior_predictive(self):
        """Test posterior predictive sampling"""
        model = build_model(test_mechanisms, test_context)
        with model:
            trace = pm.sample(draws=100, tune=100)
            posterior_pred = pm.sample_posterior_predictive(trace)

        assert 'outcome' in posterior_pred.posterior_predictive
```

#### 4. Database Model Tests

**For SQLAlchemy models:**

```python
# tests/test_models/test_[model].py

import pytest
from app.models.[model] import [ModelClass]

class Test[ModelClass]:
    """Tests for [model] database model"""

    def test_create(self, db_session):
        """Test creating model instance"""
        instance = ModelClass(field1="value1", field2="value2")
        db_session.add(instance)
        db_session.commit()

        assert instance.id is not None
        assert instance.field1 == "value1"

    def test_relationships(self, db_session):
        """Test model relationships"""
        parent = ParentModel(name="parent")
        child = ChildModel(name="child", parent=parent)

        db_session.add(child)
        db_session.commit()

        assert child.parent == parent
        assert parent.children[0] == child

    def test_validation(self, db_session):
        """Test model validation"""
        with pytest.raises(ValueError):
            ModelClass(invalid_field="invalid")

    def test_query(self, db_session):
        """Test querying model"""
        instance = ModelClass(field1="value1")
        db_session.add(instance)
        db_session.commit()

        result = db_session.query(ModelClass).filter_by(field1="value1").first()
        assert result == instance
```

---

### For Frontend (React/Jest)

#### 1. Component Tests

**For each React component:**

```typescript
// src/components/[Component].test.tsx

import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { axe, toHaveNoViolations } from 'jest-axe';
import [Component] from './[Component]';

expect.extend(toHaveNoViolations);

describe('[Component]', () => {
  it('renders without crashing', () => {
    render(<[Component] />);
    expect(screen.getByRole('[role]')).toBeInTheDocument();
  });

  it('displays expected content', () => {
    render(<[Component] prop1="value1" />);
    expect(screen.getByText('Expected Text')).toBeInTheDocument();
  });

  it('handles user interaction', async () => {
    const mockHandler = jest.fn();
    render(<[Component] onAction={mockHandler} />);

    const button = screen.getByRole('button', { name: 'Action' });
    fireEvent.click(button);

    await waitFor(() => {
      expect(mockHandler).toHaveBeenCalledTimes(1);
    });
  });

  it('updates on prop change', () => {
    const { rerender } = render(<[Component] value="initial" />);
    expect(screen.getByText('initial')).toBeInTheDocument();

    rerender(<[Component] value="updated" />);
    expect(screen.getByText('updated')).toBeInTheDocument();
  });

  it('handles error states', () => {
    render(<[Component] error="Error message" />);
    expect(screen.getByRole('alert')).toHaveTextContent('Error message');
  });

  it('has no accessibility violations', async () => {
    const { container } = render(<[Component] />);
    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });

  it('supports keyboard navigation', () => {
    render(<[Component] />);
    const element = screen.getByRole('[role]');

    element.focus();
    expect(element).toHaveFocus();

    fireEvent.keyDown(element, { key: 'Enter' });
    // Assert expected behavior
  });
});
```

#### 2. Hook Tests

**For custom React hooks:**

```typescript
// src/hooks/[useHook].test.ts

import { renderHook, act } from '@testing-library/react';
import [useHook] from './[useHook]';

describe('[useHook]', () => {
  it('returns initial state', () => {
    const { result } = renderHook(() => [useHook]());
    expect(result.current.value).toBe(initialValue);
  });

  it('updates state on action', () => {
    const { result } = renderHook(() => [useHook]());

    act(() => {
      result.current.updateValue(newValue);
    });

    expect(result.current.value).toBe(newValue);
  });

  it('handles async operations', async () => {
    const { result, waitForNextUpdate } = renderHook(() => [useHook]());

    act(() => {
      result.current.fetchData();
    });

    await waitForNextUpdate();
    expect(result.current.data).toBeDefined();
  });
});
```

#### 3. Integration Tests

**For component interactions:**

```typescript
// src/integration/[Feature].test.tsx

import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import [FeatureComponent] from '../components/[Feature]';

describe('[Feature] Integration', () => {
  it('completes full workflow', async () => {
    const queryClient = new QueryClient();

    render(
      <QueryClientProvider client={queryClient}>
        <[FeatureComponent] />
      </QueryClientProvider>
    );

    // Step 1: User action
    const button = screen.getByRole('button', { name: 'Start' });
    fireEvent.click(button);

    // Step 2: Wait for API call
    await waitFor(() => {
      expect(screen.getByText('Loading...')).toBeInTheDocument();
    });

    // Step 3: Verify result
    await waitFor(() => {
      expect(screen.getByText('Success')).toBeInTheDocument();
    });
  });
});
```

---

### Coverage Requirements

**Ensure tests cover:**
- ✓ Success paths (happy path)
- ✓ Error handling (invalid input, exceptions)
- ✓ Edge cases (empty, null, boundary values)
- ✓ Validation (input validation, business rules)
- ✓ Integration (interaction between components/services)
- ✓ Accessibility (keyboard navigation, screen readers)

**Coverage targets:**
- Overall: ≥80%
- Statements: ≥80%
- Branches: ≥75%
- Functions: ≥80%
- Lines: ≥80%

---

### Test Organization

**Directory structure:**
```
backend/tests/
├── unit/
│   ├── test_services/
│   ├── test_models/
│   └── test_utils/
├── integration/
│   ├── test_api/
│   └── test_database/
├── test_bayesian/
└── conftest.py  # Shared fixtures

frontend/
├── src/
│   ├── components/[Component].test.tsx
│   ├── hooks/[useHook].test.ts
│   └── integration/[Feature].test.tsx
└── setupTests.ts
```

---

### Fixtures (pytest)

**Common fixtures to create:**

```python
# tests/conftest.py

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from app.main import app
from app.database import get_db

@pytest.fixture
async def client():
    """Async HTTP client for API testing"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

@pytest.fixture
async def db_session():
    """Database session for tests"""
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with AsyncSession(engine) as session:
        yield session

@pytest.fixture
def sample_mechanism():
    """Sample mechanism for testing"""
    return {
        "id": "test_mechanism_v1",
        "version": 1.0,
        "effect_size": {"estimate": {"value": -0.15}},
        # ... full mechanism structure
    }
```

---

### Test Markers

**Use markers to categorize tests:**

```python
# pytest.ini or pyproject.toml
[tool.pytest.ini_options]
markers = [
    "slow: marks tests as slow (deselect with '-m \"not slow\"')",
    "integration: marks tests as integration tests",
    "unit: marks tests as unit tests",
    "bayesian: marks tests for Bayesian models",
]
```

**Usage:**
```python
@pytest.mark.slow
def test_expensive_operation():
    """This test takes a long time"""
    pass

@pytest.mark.integration
async def test_full_workflow():
    """Integration test"""
    pass
```

---

### Accessibility Testing

**Required accessibility checks:**

```typescript
import { axe, toHaveNoViolations } from 'jest-axe';

expect.extend(toHaveNoViolations);

it('has no accessibility violations', async () => {
  const { container } = render(<Component />);
  const results = await axe(container);
  expect(results).toHaveNoViolations();
});

it('supports keyboard navigation', () => {
  render(<Component />);
  const button = screen.getByRole('button');

  // Tab to button
  button.focus();
  expect(button).toHaveFocus();

  // Activate with Enter
  fireEvent.keyDown(button, { key: 'Enter' });
  // Assert expected behavior

  // Activate with Space
  fireEvent.keyDown(button, { key: ' ' });
  // Assert expected behavior
});

it('has proper ARIA attributes', () => {
  render(<Component />);
  const element = screen.getByRole('button');

  expect(element).toHaveAttribute('aria-label');
  expect(element).toHaveAttribute('aria-pressed', 'false');
});
```

---

### Output

After generating tests, provide:

1. **Test file paths** where tests should be created
2. **Coverage estimate** of new tests
3. **Fixture dependencies** needed
4. **Any manual testing** still required
5. **Command to run** the new tests

**Example output:**
```
Generated tests for [feature]:

Files created:
- tests/test_api/test_mechanisms.py (15 tests)
- tests/test_services/test_bayesian_weighting.py (12 tests)
- frontend/src/components/MechanismCard.test.tsx (8 tests)

Estimated coverage: 85%

Run with:
  Backend: pytest tests/test_api/test_mechanisms.py -v
  Frontend: npm test -- MechanismCard

Manual testing needed:
- E2E workflow with real database
- Performance under load
```
