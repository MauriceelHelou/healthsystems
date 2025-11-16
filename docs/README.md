# Documentation

Multi-level documentation for the HealthSystems Platform.

## Documentation Structure

```
docs/
├── technical/         # For developers and system administrators
├── scientific/        # For researchers and methodologists
├── user-guides/       # For end users (by persona)
└── decision-logs/     # Design decisions and rationale
```

## Documentation Levels

### Technical Documentation (`technical/`)
Audience: Software developers, DevOps engineers, system administrators

Content:
- Architecture and system design
- API specifications and endpoints
- Database schemas
- Deployment procedures
- Development setup
- CI/CD pipelines
- Security considerations

### Scientific Documentation (`scientific/`)
Audience: Public health researchers, epidemiologists, statisticians

Content:
- Statistical methodology
- Bayesian weighting algorithms
- Mechanism validation procedures
- Evidence synthesis approach
- Uncertainty quantification
- Model assumptions and limitations
- Validation studies

### User Guides (`user-guides/`)
Audience: Community organizations, consultants, health departments, foundations

Content organized by persona:
- Community organizers: Visual interface guides, interpretation help
- Researchers: Data export, reproducibility, citation
- Consultants: Scenario testing, report generation
- Health departments: Policy analysis workflows
- Foundation staff: Impact evaluation methods

### Decision Logs (`decision-logs/`)
Audience: All stakeholders

Content:
- Why specific technologies were chosen
- Algorithm selection rationale
- Trade-offs in design decisions
- Future considerations
- Lessons learned

## Contributing to Documentation

### Style Guide

- **Clarity over cleverness**: Write for understanding, not impressiveness
- **Examples**: Include code examples and screenshots
- **Accessibility**: Use alt text for images, clear headings
- **Citations**: Chicago style for scientific claims
- **Version**: Document which version features were added

### File Format

- Primary: Markdown (.md)
- Diagrams: Mermaid diagrams in markdown
- API specs: OpenAPI/Swagger YAML
- Code examples: Syntax-highlighted code blocks

### Documentation Checklist

When adding new features:
- [ ] Update technical architecture docs
- [ ] Add API endpoint documentation
- [ ] Update user guides (if user-facing)
- [ ] Document assumptions (if scientific)
- [ ] Add decision log entry (if significant choice)
- [ ] Include code examples
- [ ] Test all code examples
- [ ] Add to changelog

## Building Documentation

We use Sphinx for technical documentation:

```bash
cd docs/technical
make html
```

## Live Documentation

- **API Documentation**: Auto-generated at `/docs` endpoint (FastAPI)
- **GitHub Pages**: User-facing documentation
- **Internal Wiki**: Developer knowledge base

## Contact

Questions about documentation? Open an issue or contact [documentation team].
