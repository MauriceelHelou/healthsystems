# HealthSystems Platform Documentation

This directory contains comprehensive documentation organized by major architectural and conceptual domains.

## Documentation Structure

```
docs/
├── Foundational Principles/     # Core concepts and theoretical frameworks
├── Core Technical Architecture/ # System design, schemas, APIs
├── LLM & Discovery Pipeline/    # Mechanism discovery with Semantic Scholar + Claude
├── Design/                      # UI/UX design system and mockups
├── Deployment/                  # Railway deployment guides
├── Implementation & Operations/ # DevOps, CI/CD, monitoring
├── Phase 2 - Quantification/    # Effect size extraction (future)
├── nodes/                       # Node inventory and consolidation
└── API_INTEGRATION_GUIDE.md     # API reference
```

## Key Documents

### Mechanism Discovery (Start Here)
- **[MECHANISM_DISCOVERY_PIPELINE.md](LLM%20%26%20Discovery%20Pipeline/MECHANISM_DISCOVERY_PIPELINE.md)** - Complete guide to automated literature-driven mechanism extraction using Semantic Scholar + PubMed + Claude

### Core Architecture
- **[05_MECHANISM_BANK_STRUCTURE.md](Core%20Technical%20Architecture/05_MECHANISM_BANK_STRUCTURE.md)** - Mechanism schema, functional forms, moderators
- **[04_STOCK_FLOW_PARADIGM.md](Core%20Technical%20Architecture/04_STOCK_FLOW_PARADIGM.md)** - Node/stock specifications

### Implementation
- **[backend/pipelines/README.md](../backend/pipelines/README.md)** - Pipeline code documentation
- **[backend/config/schema_config.py](../backend/config/schema_config.py)** - Centralized schema constants

---

## Directory Purposes

### 1. Foundational Principles
Core concepts, theoretical frameworks, and guiding principles.

**Contents:**
- Project foundations and navigation index
- Methodological integration
- System architecture overview

---

### 2. Core Technical Architecture
System design, technology stack, and architectural patterns.

**Contents:**
- Stock-flow paradigm (node specifications)
- Mechanism bank structure
- Equilibrium calculation engine
- Time simulation framework

---

### 3. LLM & Discovery Pipeline
AI/ML integration, mechanism discovery, and validation.

**Contents:**
- **MECHANISM_DISCOVERY_PIPELINE.md** - Unified discovery documentation
- **11_LLM_MECHANISM_VALIDATION.md** - Validation framework

**Implementation:**
- `backend/pipelines/literature_search.py` - Semantic Scholar + PubMed APIs
- `backend/pipelines/llm_mechanism_discovery.py` - Claude extraction
- `backend/pipelines/end_to_end_discovery.py` - Complete pipeline

---

### 4. Design
UI/UX design system, component library, and mockups.

**Contents:**
- Design system principles
- Dashboard layout
- Systems map visualization
- Component library

---

### 5. Implementation & Operations
Practical guides for development, deployment, and operations.

**Contents:**
- Computational infrastructure
- Deployment guides

---

### 6. Phase 2 - Quantification
Deferred capabilities for effect size quantification and Bayesian inference.

**⚠️ Note**: Phase 2 content. MVP focuses on topology and direction discovery.

**Contents:**
- Effect size translation methods
- LLM effect quantification pipeline
- Meta-analytic pooling specifications

**Note**: Quantitative effect data is currently extracted by `backend/scripts/extract_quantitative_effects.py` and stored in `mechanism-bank/quantitative_effects.json` for future use.

**See**: [Phase 2 - Quantification/README.md](Phase%202%20-%20Quantification/README.md)

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
