# System Architecture

## Overview

The HealthSystems Platform is a multi-tier web application designed to quantify structural determinants of health through Bayesian mechanism weighting and interactive visualizations.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                         Frontend                            │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  React/TypeScript SPA                                 │  │
│  │  - D3.js Visualizations                              │  │
│  │  - React Query (state management)                    │  │
│  │  - TailwindCSS (styling)                             │  │
│  │  - Accessibility-first design (WCAG 2.1 AA)          │  │
│  └──────────────────────────────────────────────────────┘  │
└──────────────────────┬──────────────────────────────────────┘
                       │ HTTPS / REST API
┌──────────────────────▼──────────────────────────────────────┐
│                      Backend API                            │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  FastAPI Application                                  │  │
│  │  - RESTful API endpoints                             │  │
│  │  - Request validation (Pydantic)                     │  │
│  │  - Authentication & authorization                    │  │
│  │  - Rate limiting                                     │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────┐  │
│  │  Services    │  │  Algorithms  │  │  ETL Pipelines  │  │
│  │              │  │              │  │                 │  │
│  │  - Business  │  │  - Bayesian  │  │  - Census API   │  │
│  │    logic     │  │    weighting │  │  - CDC scraper  │  │
│  │  - Data      │  │  - Network   │  │  - EPA data     │  │
│  │    validation│  │    analysis  │  │  - Caching      │  │
│  └──────────────┘  └──────────────┘  └─────────────────┘  │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│                    Data Layer                               │
│  ┌─────────────┐  ┌──────────┐  ┌───────────────────────┐  │
│  │ PostgreSQL  │  │  Redis   │  │  Mechanism Bank       │  │
│  │             │  │          │  │                       │  │
│  │ - User data │  │ - Cache  │  │  - YAML files        │  │
│  │ - Context   │  │ - Session│  │  - Version control   │  │
│  │ - Weights   │  │ - Queue  │  │  - Evidence citations│  │
│  └─────────────┘  └──────────┘  └───────────────────────┘  │
│                                                             │
│  ┌───────────────────────────────────────────────────────┐ │
│  │  Neo4j (Optional) - Graph relationships              │ │
│  └───────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

## Components

### Frontend Layer

**Technology Stack:**
- React 18 with TypeScript
- D3.js for force-directed graph visualizations
- TanStack Query for server state management
- Zustand for client state management
- TailwindCSS for styling
- Axios for HTTP requests

**Key Features:**
- Interactive mechanism network diagrams
- Contextual data input forms
- Real-time weight calculations
- Accessible interface (keyboard navigation, screen readers)
- Responsive design

### Backend Layer

**Technology Stack:**
- Python 3.11+
- FastAPI framework
- Pydantic for data validation
- SQLAlchemy for ORM
- PyMC for Bayesian inference
- NetworkX for graph analysis

**API Structure:**
```
/api/mechanisms      # Mechanism CRUD operations
/api/contexts        # Geographic context data
/api/weights         # Bayesian weight calculations
/api/visualizations  # Network graph generation
/api/exports         # Report generation
```

**Middleware:**
- CORS (for frontend communication)
- Request logging
- Rate limiting
- Error handling
- Authentication (JWT)

### Scientific Computing

**Bayesian Weighting Algorithm:**
```python
Prior: Literature effect sizes
  ↓
Likelihood: Contextual data (demographics, environment, etc.)
  ↓
Posterior: Updated mechanism weights with uncertainty
  ↓
Network propagation: Uncertainty through causal chains
```

**Key Algorithms:**
- Hierarchical Bayesian models (PyMC)
- Monte Carlo uncertainty propagation
- Network centrality analysis
- Meta-regression for moderators

### Data Integration Layer

**Data Sources:**
- U.S. Census Bureau (demographics, housing)
- CDC PLACES (health outcomes)
- EPA (environmental quality)
- Bureau of Labor Statistics (employment, wages)

**ETL Pipeline:**
1. Check cache for recent data
2. If cache miss, fetch from API
3. Validate data quality
4. Transform to standard schema
5. Store in database and cache
6. Return to application

### Data Storage

**PostgreSQL (Primary Database):**
- User accounts and permissions
- Geographic context data
- Calculated mechanism weights
- Analysis history

**Redis (Cache & Queue):**
- API response caching
- Session management
- Background job queue (Celery)

**Mechanism Bank (Version-Controlled Files):**
- YAML files for each mechanism
- Git for version control
- Separate from application database
- Read-only in production

**Neo4j (Optional Graph Database):**
- Mechanism relationship modeling
- Path analysis through causal networks
- Advanced graph queries

## Deployment Architecture

### Development Environment
```
Docker Compose
├── Backend (hot reload)
├── Frontend (dev server)
├── PostgreSQL
├── Redis
└── (Optional) Neo4j
```

### Production Environment
```
Kubernetes Cluster
├── Frontend Pods (Nginx)
├── Backend Pods (Gunicorn + Uvicorn)
├── PostgreSQL (managed service)
├── Redis (managed service)
├── Ingress (TLS termination)
└── Monitoring (Prometheus/Grafana)
```

## Security Considerations

- HTTPS only in production
- JWT authentication for API
- Role-based access control (RBAC)
- API rate limiting
- Input validation (Pydantic)
- SQL injection prevention (SQLAlchemy ORM)
- XSS prevention (React escaping)
- CSRF tokens for state-changing operations
- Secrets management (environment variables, vaults)

## Scalability

**Horizontal Scaling:**
- Stateless backend API (scales horizontally)
- Redis for shared session state
- Load balancer for traffic distribution

**Caching Strategy:**
- Redis for API responses
- Browser caching for static assets
- Mechanism bank cached in memory

**Performance Optimization:**
- Database indexing on common queries
- Lazy loading for visualizations
- Pagination for large result sets
- Background jobs for expensive computations

## Monitoring & Observability

- Application logs (JSON structured)
- Error tracking (Sentry)
- Performance monitoring (APM)
- Database query monitoring
- API endpoint metrics
- User analytics (privacy-preserving)

## Disaster Recovery

- Database backups (daily)
- Point-in-time recovery capability
- Mechanism bank in version control (Git)
- Infrastructure as code (Terraform)
- Documented recovery procedures

## Future Considerations

- Real-time collaboration features
- GraphQL API for flexible queries
- Machine learning for mechanism discovery
- Mobile application
- Multi-language support
- Federation with other health data platforms
