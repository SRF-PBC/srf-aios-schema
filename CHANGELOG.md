# Changelog

All notable changes to the SRF AiOS Schema package will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [4.0.0] - 2026-07-19

### Changed (BREAKING)

- **ARC no longer carries the embodiment.** Removed `reasoning_engine`, `base_model`, `checkpoint`,
  `reasoning_params`, `context_window`, `temperature`, `max_tokens`, `provider`, `license_class`.
  ARC is now the **Agent Record Core** — the durable identity core only: `agent_id`, `arc_id`,
  `name`, `agent_name`, `agent_class`, `origin_signature`, `created_by`, `created_at`.
- **Rationale — the model is FUNGIBLE; an agent persists across vessel changes.** Sealing the vessel
  into the identity hash would (a) break the seal on every model upgrade — making an engine swap an
  *appended correction on an immutable worldline* — and (b) imply the agent **is** its weights, so
  upgrading the model would kill it and instantiate someone else. **A self is not its substrate.**
- **Embodiment is an ADAPTER concern and is not captured here at all.** The runtime that instantiates
  an agent already knows its own model; a second copy in the identity layer is a second source of
  truth and it drifts. Per-action provenance is already emitted where actions happen (commit
  trailers, run telemetry) and deployment belongs to the Deployment Capsule layer (INV-DEP-1/2).
- `SCHEMA_VERSION` -> `v4.0`; `RAIR.policy_version` -> `v4.0`; `ARC.version` -> `4.0`.
- ROLE / MACP / PERSONA and the dual-hash + TrustVault provenance are unchanged.

### Migration

- v3 RAIR instances must drop the nine embodiment fields from `arc`. Identity hashes change once,
  and then stop changing when the model does — which is the entire point.

## [3.0.1] - 2026-07-10

### Fixed

- **`ARC.context_window` upper bound REMOVED** (was `le=128000`). The ceiling was already wrong at
  first contact with a real agent — Kai runs at a **1M-token** window — and any fixed cap will be
  wrong again as frontier context windows grow. The sanity floor (`ge=1024`) is retained.
- **Principle (same as the v3.0.0 temperament-enum removal): a schema must not pre-decide what
  reality is allowed to be.** Non-breaking: widening a constraint; all v3.0.0-valid records remain
  valid.

## [3.0.0] - 2026-07-10

### Changed (BREAKING)

- **PERSONA temperament & moral_accent are now EMERGENT, not enums.** Replaced
  `temperament_profile: Literal["strategic","empathic","analytic","stoic","adaptive"]` and
  `moral_accent: Literal["deontic","utilitarian","virtue","reflexic"]` with structured
  emergent-trait models:
  - `Temperament` = free `narrative` + open weighted `facets` (`list[WeightedFacet]`) + `embedding_ref`.
  - `MoralAccent` = free `narrative` + open weighted `facets` + `embedding_ref`.
  - `WeightedFacet` = `{facet, weight, evidence_refs}` — facet names governed by the SRF facet
    lexicon (open + reconciled, not a fixed enum); `evidence_refs` point to the episodes that
    ground each facet (emergent grounding).
- **Rationale:** identity, like meaning, emerges from content/behavior — it is not selected from a
  fixed menu. The v2 enum could not express blends or novel traits (e.g. "creative"). This makes
  the identity schema consistent with the SRF substrate principle (IC-46: meaning from content).
- `PERSONA.version` → `3.0`; `RAIR.policy_version` → `v3.0`; `SCHEMA_VERSION` → `v3.0`.
- ARC / ROLE / MACP and the dual-hash + TrustVault provenance system are **unchanged**.

### Migration

- v2 RAIR instances carrying `temperament_profile`/`moral_accent` strings must migrate to the
  `Temperament`/`MoralAccent` objects (a scalar enum becomes a narrative + one-or-more facets).

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
