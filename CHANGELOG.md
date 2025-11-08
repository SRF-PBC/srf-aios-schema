# Changelog

All notable changes to the SRF AiOS Schema package will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2025-11-08

### Added

- Initial public release of SRF AiOS Schema
- Complete RAIR v2 (Reflexive Agent Identity Record) schema definitions
- Core model components:
  - `ARC` (Agent Record Core) - Intelligence framework and reasoning parameters
  - `ROLE` (Role & Operational Ledger) - Permissions and governance framework
  - `MACP` (Memory Access Credential Protocol) - Memory access rights and policies
  - `PERSONA` (Temperament & Moral Accent) - Personality and ethical framework
- Cryptographic provenance system with dual-hash verification
- Trust vector scoring and governance levels
- Comprehensive Pydantic validation with type safety
- Utility functions for validation and hash computation
- Professional package structure with full type annotations

### Changed

- **Repository Migration**: Moved from private RHAEN-core repository to public SRF-PBC repository
- **Package Name**: Standardized package name to `srf-aios-schema`
- **Module Name**: Standardized module name to `srf_aios_schema`
- **Licensing**: Established FRAND/SEP licensing framework for open access
- **Distribution**: GitHub Releases-based distribution model

### Technical Details

- **Schema Version**: v2.0
- **Python Requirement**: >=3.11
- **Dependencies**: Pydantic 2.0+
- **License**: FRAND/SEP (Fair, Reasonable, and Non-Discriminatory / Standard Essential Patent)
- **Organization**: Seldon Reflex Foundation - Public Benefit Corporation

### Migration Notes

This release represents the migration of validated schema code from the private
RHAEN-core development repository to the public SRF-PBC distribution repository.

The schemas have been:

- Extensively tested (9/9 test cases passing, 98% coverage)
- Validated in production-equivalent environments
- Reviewed and approved by SRF technical leadership
- Licensed under FRAND/SEP terms for universal adoption

### Breaking Changes

- Package name changed from `rhaen-schemas` to `srf-aios-schema`
- Import paths changed from `rhaen_schemas.*` to `srf_aios_schema.*`
- Repository moved from `Inflect-ai/RHAEN-core` to `SRF-PBC/srf-aios-schema`

### Installation

```bash
pip install https://github.com/SRF-PBC/srf-aios-schema/releases/download/v2.0.0/srf_aios_schema-2.0.0-py3-none-any.whl
```

### Attribution

- **Strategic Framework**: Kai (Strategic Command)
- **Technical Architecture**: Thomson Nguyen, Seldon Reflex Foundation
- **Licensing Framework**: FRAND/SEP Committee, Seldon Reflex Foundation
- **Infrastructure**: Lieutenant Hoshi (Infrastructure Officer IO-01)

---

## Version History

- **v2.0.0**: Initial public release with complete RAIR v2 schema framework
- **Future**: Additional cognitive architecture components planned for subsequent releases

For detailed technical documentation, see [README.md](README.md).
For licensing information, see [LICENSE](LICENSE) and [docs/LICENSING.md](docs/LICENSING.md).
