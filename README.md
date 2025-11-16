# HealthSystems Platform

A decision support platform for quantifying how structural interventions propagate through social-spatial-biological systems to affect health outcomes.

## Overview

The HealthSystems Platform makes structural determinants of health visible, quantifiable, and actionable by:

- **Self-configuring analysis**: Adapts to any geography/demographic context through automated data integration
- **Mechanism weighting**: Combines systems dynamics with epidemiological rigor using Bayesian inference
- **Interactive visualizations**: Force-directed graphs and dashboards accessible to diverse stakeholders
- **Transparent uncertainty**: Explicit confidence intervals and evidence quality metrics

## Architecture

This is a multi-tier web application consisting of:

- **Backend**: Python/FastAPI API with data pipelines and scientific computing
- **Frontend**: React/TypeScript interactive interface with D3.js visualizations
- **Mechanism Bank**: Versioned database of causal pathways with evidence citations
- **Data Sources**: ETL system integrating Census, CDC, environmental, and economic data

## Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- Docker and Docker Compose
- PostgreSQL 14+

### Development Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd healthsystems
   ```

2. **Start services with Docker Compose**
   ```bash
   docker-compose up -d
   ```

3. **Backend setup**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   python -m pytest  # Run tests
   ```

4. **Frontend setup**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

5. **Access the application**
   - Frontend: http://localhost:3000
   - API docs: http://localhost:8000/docs
   - API: http://localhost:8000/api

## Project Structure

```
healthsystems/
├── backend/           # Python API, data pipelines, scientific models
├── frontend/          # React/TypeScript UI with visualizations
├── mechanism-bank/    # Structured causal mechanism data
├── data-sources/      # ETL scripts and API integrations
├── docs/              # Multi-level documentation
├── infrastructure/    # Docker, K8s, deployment configs
└── .github/           # CI/CD workflows
```

## User Types

- **Community Organizations**: Visual, accessible systems maps for intervention planning
- **Academic Researchers**: Statistical rigor, reproducible computational methods
- **Health Departments**: Policy analysis with evidence-based mechanism weighting
- **Foundations**: Impact evaluation with quantified uncertainty
- **Consultants**: Scenario testing, custom report generation

## Key Features

### Structural Competency Framework
Explicit focus on structural interventions (housing policy, labor conditions, environmental justice) rather than individual behavior change.

### Evidence-Based Mechanism Bank
Each causal pathway includes:
- Effect size estimates with confidence intervals
- Evidence quality ratings
- Chicago-style academic citations
- Last updated timestamp

### Geographic Adaptation
Automatically scrapes and integrates contextual data:
- Census demographic data
- CDC health outcome data
- Environmental quality indicators
- Economic and labor statistics

### Bayesian Mechanism Weighting
Combines:
- Prior evidence from literature
- Geographic context data
- Expert consultant input
- Uncertainty propagation through systems

## Development

### Running Tests

```bash
# Backend tests
cd backend
pytest tests/ --cov=. --cov-report=html

# Frontend tests
cd frontend
npm test
npm run test:a11y  # Accessibility tests
```

### Code Quality

```bash
# Python linting and formatting
black backend/
isort backend/
flake8 backend/

# TypeScript/React linting
cd frontend
npm run lint
npm run format
```

### Pre-commit Hooks

```bash
pip install pre-commit
pre-commit install
```

## Documentation

- **[Technical Documentation](docs/technical/)**: Architecture, API specs, deployment
- **[Scientific Methodology](docs/scientific/)**: Statistical models, mechanism validation
- **[User Guides](docs/user-guides/)**: Interface tutorials by user type
- **[Decision Logs](docs/decision-logs/)**: Design choices and rationale

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for development workflow, coding standards, and pull request process.

## License

[Specify license - consider academic/research-friendly licenses like MIT or Apache 2.0]

## Citation

If you use this platform in academic research, please cite:

```
[Citation format to be determined]
```

## Contact

[Project contact information]

## Acknowledgments

This platform builds on research in:
- Structural determinants of health
- Systems science and complexity theory
- Social epidemiology
- Community-based participatory research
