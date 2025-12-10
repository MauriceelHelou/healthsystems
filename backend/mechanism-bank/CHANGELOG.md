# Mechanism Bank Changelog

All notable changes to the mechanism bank will be documented in this file.

## [Unreleased]

### Added
- Initial mechanism bank structure
- Validation schema and scripts
- Example mechanism: Housing Quality → Respiratory Health

## [1.0.0] - YYYY-MM-DD

### Added
- Mechanism bank initialization
- Schema v1.0 for mechanism validation
- Built environment category
- Social environment category
- Economic category
- Political category
- Biological category

---

## Format

### Entry Format
```
## [Version] - YYYY-MM-DD

### Added
- New mechanism: [name] (effect size: X.XX, CI: [X.XX-X.XX], quality: A/B/C)

### Changed
- Updated mechanism: [name] - [reason for update]
  - Old effect size: X.XX → New: X.XX
  - Evidence quality: B → A (added 5 new studies)

### Deprecated
- Mechanism [name] - superseded by [replacement]

### Removed
- Mechanism [name] - [reason for removal]
```

### Versioning Rules

- **MAJOR version** (e.g., 1.0 → 2.0): Breaking changes to schema or substantial mechanism revisions
- **MINOR version** (e.g., 1.0 → 1.1): New mechanisms added or evidence updates
- **PATCH version** (e.g., 1.0.0 → 1.0.1): Bug fixes, typos, or minor corrections
