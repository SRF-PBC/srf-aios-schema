# SRF AiOS Schema

Canonical schema definitions for SRF AiOS cognitive architecture

[![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)](https://github.com/SRF-PBC/srf-aios-schema)
[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-FRAND%2FSEP-green.svg)](LICENSE)

---

## Overview

SRF AiOS Schema provides the foundational data structures for the
**Seldon Reflex Foundation AI Operating System** (SRF AiOS), a cognitive
architecture system that represents the world's first mathematically governed
autonomous AI agent framework.

This package contains the **cognitive DNA** of SRF AiOS - the canonical
definitions for agent identity, memory structures, trust records, and reflexive
governance components.

## Installation

Install directly from GitHub Releases:

```bash
pip install https://github.com/SRF-PBC/srf-aios-schema/releases/download/v2.0.0/srf_aios_schema-2.0.0-py3-none-any.whl
```

## Quick Start

```python
from srf_aios_schema import RAIR, ARC, ROLE, MACP, PERSONA, TONEVector
from datetime import datetime, timezone

# Create agent identity components
arc = ARC(
    name="MyAgent",
    agent_name="MyAgent",
    reasoning_engine="llm",
    base_model="openai/gpt-4",
    checkpoint="latest",
    reasoning_params={"temperature": 0.7},
    context_window=8192,
    provider="openai",
    created_by="Developer"
)

role = ROLE(
    role_scope=["general"],
    permissions=["read", "write"],
    reflex_scope=["basic"],
    trust_vector=0.8
)

macp = MACP(
    scope=["memory.read"],
    issuer="SRF-Authority",
    expiration=datetime.now(timezone.utc).replace(year=2025)
)

persona = PERSONA(
    name="Analytical Assistant",
    temperament_profile="analytic",
    moral_accent="utilitarian",
    tone_vector=TONEVector(direct=0.8, warm=0.6, humorous=0.3, formal=0.7),
    alignment_directives=["Be helpful and accurate"],
    created_by="Developer"
)

# Create complete agent identity record
rair = RAIR(
    arc=arc,
    role=role, 
    macp=macp,
    persona=persona
)

print(f"Agent ID: {rair.arc.agent_id}")
print(f"RAIR Hash: {rair.provenance_hash}")
```

## Schema Components

### RAIR v2 (Reflexic Agent Identity Record)

The unified agent identity framework consisting of four components:

- **ARC** (Agent Record Core) - Core intelligence and reasoning parameters
- **ROLE** (Role & Operational Ledger) - Permissions and governance framework  
- **MACP** (Memory Access Credential Protocol) - Memory access rights and policies
- **PERSONA** (Temperament & Moral Accent) - Personality and ethical framework

### Key Features

- **Cryptographic Provenance**: All records include tamper-evident hash verification
- **Trust Vectors**: Mathematical trust scoring and governance levels
- **Memory Access Control**: Fine-grained credential-based memory permissions
- **Moral Reasoning**: Built-in ethical frameworks and alignment directives
- **Type Safety**: Full Pydantic validation with comprehensive type checking

## API Reference

### Core Models

#### `RAIR`

Complete agent identity record with four-component structure and cryptographic verification.

#### `ARC` (Agent Record Core)

- Agent identification and metadata
- Reasoning engine configuration
- Model parameters and provider settings

#### `ROLE` (Role & Operational Ledger)

- Permission scopes and governance levels
- Trust vector scoring
- Reflex scope definitions

#### `MACP` (Memory Access Credential Protocol)

- Memory access credentials
- Expiration-based security
- Policy tagging system

#### `PERSONA` (Temperament & Moral Accent)

- Temperament profiles and moral accents
- Tone vectors for communication style
- Alignment directives for ethical behavior

### Utility Functions

#### `validate_rair_configuration(rair_data: dict) -> tuple[bool, list[str]]`

Validate complete RAIR configuration and return validation results.

#### `compute_rair_hashes(rair: RAIR) -> dict`

Compute cryptographic hashes for identity verification.

## Development

### Requirements

- Python 3.11+
- Pydantic 2.0+

### Testing

```bash
# Install with dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run tests with coverage
pytest --cov=srf_aios_schema --cov-report=html
```

### Code Quality

```bash
# Format code
black src/ tests/

# Lint code
ruff check src/ tests/

# Type checking
mypy src/
```

## License

This project is licensed under **FRAND/SEP (Fair, Reasonable, and Non-Discriminatory / Standard Essential Patent)** terms.

See the [LICENSE](LICENSE) file for complete license text and the [Licensing Guide](docs/LICENSING.md) for implementation guidelines.

### License Summary

- **Open Access**: Free to use for research, development, and commercial applications
- **Attribution Required**: Credit the Seldon Reflex Foundation
- **Patent Protection**: Standard essential patents under FRAND terms
- **No Discrimination**: Equal access regardless of organization size or industry

## About SRF

The **Seldon Reflex Foundation** (SRF) is a public benefit corporation dedicated to advancing safe, governed artificial intelligence systems.

### Mission

Develop and distribute foundational technologies for **governed autonomous AI agents** that operate within mathematical frameworks for trust, memory, and ethical reasoning.

### Vision  

Enable the emergence of beneficial artificial general intelligence through open cognitive architecture standards and reflexive governance protocols.

## Support & Contact

- **Foundation**: [foundation@seldonreflex.org](mailto:foundation@seldonreflex.org)
- **Technical Support**: [thomson@seldonreflex.org](mailto:thomson@seldonreflex.org)
- **Issues**: [GitHub Issues](https://github.com/SRF-PBC/srf-aios-schema/issues)
- **Website**: [seldonreflex.org](https://www.seldonreflex.org)

## Contributing

We welcome contributions! Please:

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality  
4. Ensure all tests pass
5. Submit a pull request

For major changes, please open an issue first to discuss the proposed changes.

---

## Cognitive Architecture for the Future of AI

Building the foundation for safe, governed artificial intelligence
