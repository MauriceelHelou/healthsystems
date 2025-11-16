# HealthSystems Platform Documentation

This directory contains comprehensive documentation organized by major architectural and conceptual domains.

## Documentation Structure

```
docs/
├── Foundational Principles/
├── Core Technical Architecture/
├── LLM & Discovery Pipeline/
├── Geographic & Contextual Adaptation/
├── Implementation & Operations/
└── Phase 2 - Quantification/
```

## Directory Purposes

### 1. Foundational Principles
Core concepts, theoretical frameworks, and guiding principles that underpin the HealthSystems Platform.

**Suggested content:**
- Structural determinants of health framework
- Systems thinking approach
- Evidence hierarchy and quality standards
- Ethical guidelines and principles
- Theoretical foundations

---

### 2. Core Technical Architecture
System design, technology stack, and architectural patterns.

**Suggested content:**
- System architecture diagrams
- Technology stack specifications
- Database schemas and data models
- API specifications (REST/GraphQL)
- Security architecture
- Deployment architecture
- Scalability and performance considerations

---

### 3. LLM & Discovery Pipeline
AI/ML integration, mechanism discovery, and natural language processing components.

**Suggested content:**
- LLM integration architecture
- Mechanism discovery algorithms
- Literature mining and evidence extraction
- Natural language query processing
- AI-assisted mechanism validation
- Prompt engineering strategies
- Model selection and evaluation

---

### 4. Geographic & Contextual Adaptation
Methods for adapting mechanisms to specific geographic and demographic contexts.

**Suggested content:**
- Contextual moderator specifications
- Geographic data integration (Census, CDC, EPA, BLS)
- Data scraping and ETL pipelines
- Spatial analysis methods
- Temporal adaptation strategies
- Cross-geography validation
- **[Phase 2]** Bayesian weighting methodology (see Phase 2 directory)

---

### 5. Implementation & Operations
Practical guides for development, deployment, and ongoing operations.

**Suggested content:**
- Development setup and workflows
- CI/CD pipeline documentation
- Testing strategies and procedures
- Deployment guides (staging, production)
- Monitoring and observability
- Incident response procedures
- Maintenance and update protocols
- User support documentation

---

### 6. Phase 2 - Quantification
Deferred capabilities for effect size quantification and Bayesian inference.

**⚠️ Note**: This directory contains specifications for **Phase 2 only**. MVP (Phase 1) focuses on topology and direction discovery without numerical quantification.

**Content:**
- Effect size translation methods (Document 08)
- LLM effect quantification pipeline (Document 10)
- Bayesian methodology extraction (Document 02B - to be created)
- Meta-analytic pooling specifications
- Uncertainty propagation methods
- Migration path from MVP to Phase 2

**Purpose**: Clearly separates topology discovery (MVP) from quantification capabilities (Phase 2), allowing focused implementation while maintaining complete technical specifications.

**See**: [Phase 2 - Quantification/README.md](Phase%202%20-%20Quantification/README.md) for complete rationale and implementation plan.

---

## Contributing Documentation

When adding documentation:

1. **Choose the appropriate directory** based on the content's primary focus
2. **Use clear, descriptive filenames** (e.g., `bayesian-weighting-algorithm.md`)
3. **Include examples** where applicable
4. **Add diagrams** using Mermaid or images in `assets/` subdirectories
5. **Cross-reference** related documents in other directories
6. **Update this README** if adding new major topics

## Documentation Standards

- **Format**: Markdown (.md) files
- **Diagrams**: Mermaid (preferred) or PNG/SVG in `assets/`
- **Code examples**: Use syntax highlighting with language tags
- **Equations**: Use LaTeX notation within markdown
- **Citations**: Chicago style for academic references
- **Links**: Use relative paths for internal documentation

## Getting Started

If you're new to the documentation:

1. Start with **Foundational Principles** to understand core concepts
2. Review **Core Technical Architecture** for system overview
3. Dive into specific domains (**LLM**, **Geographic**, **Implementation**) as needed

## Documentation Maintenance

- Review and update quarterly
- Mark deprecated content clearly
- Archive old versions in `docs/archive/` if needed
- Keep synchronized with code changes
