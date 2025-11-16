# Contributing to HealthSystems Platform

Thank you for your interest in contributing! This platform combines research rigor with production-quality software, so we maintain high standards for both scientific validity and code quality.

## Code of Conduct

This project is committed to:
- **Scientific integrity**: Evidence-based mechanism validation
- **Accessibility**: WCAG 2.1 AA compliance minimum
- **Structural competency**: Centering systemic interventions over individual behavior
- **Transparency**: Documenting uncertainty and assumptions
- **Collaboration**: Respectful, constructive peer review

## Development Workflow

### 1. Setting Up Your Environment

```bash
# Clone and set up
git clone <repository-url>
cd healthsystems

# Backend setup
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Frontend setup
cd ../frontend
npm install

# Install pre-commit hooks
pip install pre-commit
pre-commit install
```

### 2. Branch Strategy

- `main`: Production-ready code
- `develop`: Integration branch for features
- `feature/*`: Individual feature development
- `hotfix/*`: Urgent production fixes
- `mechanism/*`: Mechanism bank additions/updates

```bash
# Create a feature branch
git checkout develop
git pull origin develop
git checkout -b feature/your-feature-name
```

### 3. Making Changes

#### Code Standards

**Python (Backend)**
- Follow PEP 8 style guide
- Use type hints (mypy strict mode)
- Maximum line length: 100 characters
- Docstrings: Google style format

```python
def calculate_mechanism_weight(
    mechanism_id: str,
    context_data: Dict[str, Any],
    prior_strength: float = 0.5
) -> Tuple[float, float]:
    """Calculate Bayesian posterior weight for a mechanism.

    Args:
        mechanism_id: Unique identifier for the causal mechanism
        context_data: Geographic and demographic context
        prior_strength: Strength of prior belief (0-1)

    Returns:
        Tuple of (posterior_weight, confidence_interval)

    Raises:
        MechanismNotFoundError: If mechanism_id not in database
    """
```

**TypeScript/React (Frontend)**
- Follow Airbnb style guide
- Use functional components with hooks
- Accessibility: ARIA labels, keyboard navigation, semantic HTML
- Component naming: PascalCase for components, camelCase for utilities

```typescript
interface MechanismNodeProps {
  mechanismId: string;
  weight: number;
  confidenceInterval: [number, number];
  onSelect: (id: string) => void;
  ariaLabel?: string;
}

export const MechanismNode: React.FC<MechanismNodeProps> = ({
  mechanismId,
  weight,
  confidenceInterval,
  onSelect,
  ariaLabel
}) => {
  // Component implementation
};
```

#### Testing Requirements

All contributions must include tests:

**Backend Testing**
```bash
# Unit tests
pytest tests/unit/ -v

# Integration tests
pytest tests/integration/ -v

# Coverage requirement: 80% minimum
pytest --cov=. --cov-report=html --cov-fail-under=80
```

**Frontend Testing**
```bash
# Component tests
npm test

# Accessibility tests
npm run test:a11y

# E2E tests
npm run test:e2e
```

**Statistical Validation**
For algorithm changes, provide:
- Validation against known test cases
- Comparison with previous version
- Sensitivity analysis results

### 4. Documentation Standards

#### Code Comments
- Why, not what (code should be self-documenting)
- Decision rationale for non-obvious choices
- Citations for scientific formulas/methods

```python
# Use Chicago-style citations for scientific claims
# Effect size from Wilson et al. (2019): odds ratio = 1.45 (95% CI: 1.22-1.73)
prior_effect_size = 1.45
```

#### Multi-Level Documentation

**Technical Documentation** (`docs/technical/`)
- Architecture decisions
- API specifications
- Deployment procedures

**Scientific Documentation** (`docs/scientific/`)
- Statistical methodology
- Mechanism validation procedures
- Evidence synthesis approach

**User Guides** (`docs/user-guides/`)
- Separate guides by persona
- Screenshots and examples
- Accessibility instructions

### 5. Commit Messages

Use conventional commits format:

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style (formatting, no logic change)
- `refactor`: Code restructuring
- `test`: Adding/updating tests
- `chore`: Maintenance tasks
- `mechanism`: Mechanism bank updates

**Examples:**
```
feat(backend): add Bayesian mechanism weighting algorithm

Implements hierarchical Bayesian model for combining prior evidence
with contextual data. Uses PyMC for MCMC sampling.

Closes #123
```

```
mechanism(bank): add housing quality -> respiratory health pathway

Effect size: OR 1.34 (95% CI: 1.18-1.52)
Evidence: 8 studies, quality rating A
Citation: Krieger et al. (2010)

Refs #456
```

### 6. Pull Request Process

#### Before Submitting

- [ ] All tests pass locally
- [ ] Code follows style guidelines (linters pass)
- [ ] Documentation updated (if applicable)
- [ ] CHANGELOG.md updated
- [ ] Accessibility tested (for UI changes)
- [ ] No secrets or API keys committed

#### PR Template

```markdown
## Description
[Clear description of changes]

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update
- [ ] Mechanism bank addition

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] Accessibility tests pass
- [ ] Manual testing completed

## Scientific Validation (if applicable)
- [ ] Citations provided
- [ ] Effect sizes documented
- [ ] Uncertainty quantified
- [ ] Expert review obtained

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No new warnings generated
- [ ] CHANGELOG.md updated
```

#### Review Process

1. Automated checks must pass (CI/CD)
2. Peer review by 1-2 maintainers
3. Scientific review (for mechanism/algorithm changes)
4. Accessibility review (for UI changes)
5. Approval from code owner

### 7. Mechanism Bank Contributions

Adding/modifying causal mechanisms requires:

**Evidence Requirements**
- Minimum 3 peer-reviewed studies (or 1 meta-analysis)
- Effect size with confidence intervals
- Evidence quality rating (A/B/C)
- Chicago-style citations

**File Format** (`mechanism-bank/mechanisms/`)
```yaml
id: housing_quality_respiratory
name: Housing Quality → Respiratory Health
category: built_environment
mechanism_type: biological
effect_size:
  measure: odds_ratio
  point_estimate: 1.34
  confidence_interval: [1.18, 1.52]
  unit: per standard deviation improvement
evidence:
  quality_rating: A
  n_studies: 8
  citation: |
    Krieger, James, and Donna L. Higgins. 2010. "Housing and Health:
    Time Again for Public Health Action." *American Journal of Public Health*
    92 (5): 758–68. https://doi.org/10.2105/AJPH.92.5.758
last_updated: 2024-01-15
validated_by: [expert_initials]
```

**Validation Process**
```bash
# Run mechanism validation
python mechanism-bank/validation/validate_mechanisms.py

# Check citations
python mechanism-bank/validation/check_citations.py
```

### 8. Accessibility Guidelines

All UI contributions must meet:
- **WCAG 2.1 AA minimum** (AAA preferred)
- Color contrast ratio ≥ 4.5:1 for text
- Keyboard navigation support
- Screen reader compatibility
- Alternative text for visualizations
- Semantic HTML structure

**Testing Tools**
```bash
# Automated accessibility testing
npm run test:a11y

# Manual testing checklist
# - Tab through interface
# - Test with screen reader (NVDA/JAWS/VoiceOver)
# - Verify color contrast
# - Check ARIA labels
```

### 9. Getting Help

- **Technical questions**: Open a Discussion on GitHub
- **Bug reports**: Create an Issue with reproduction steps
- **Scientific methodology**: Contact research team [email]
- **Security vulnerabilities**: Email security@[project].org (do not open public issue)

## Recognition

Contributors will be acknowledged in:
- CHANGELOG.md for each release
- Project documentation
- Academic publications (if significant scientific contribution)

Thank you for contributing to making structural determinants of health visible and actionable!
