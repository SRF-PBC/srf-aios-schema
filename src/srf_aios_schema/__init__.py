"""
SRF AiOS Schema - Cognitive Architecture Schema Definitions

The Seldon Reflex Foundation AI Operating System schema package provides
foundational data structures for governed autonomous AI agents.

This package contains the canonical schema definitions for:
- RAIR v2 (Reflexic Agent Identity Records)
- Agent identity, memory, and governance structures
- Trust vectors and compliance frameworks
"""

__version__ = "2.0.0"
__author__ = "Seldon Reflex Foundation"
__email__ = "foundation@seldonreflex.org"
__license__ = "FRAND/SEP"

# Import all main components from rair_v2
from .rair_v2 import (
    # Core Models
    ARC,
    ROLE, 
    MACP,
    PERSONA,
    TONEVector,
    RAIR,
    TrustVaultRecord,
    
    # Utility Functions
    validate_rair_configuration,
    compute_rair_hashes,
    
    # Schema Metadata
    SCHEMA_VERSION,
    SCHEMA_COMPONENTS
)

# Package metadata
__all__ = [
    # Core Models
    "ARC",
    "ROLE", 
    "MACP",
    "PERSONA",
    "TONEVector", 
    "RAIR",
    "TrustVaultRecord",
    
    # Utility Functions
    "validate_rair_configuration",
    "compute_rair_hashes",
    
    # Schema Metadata
    "SCHEMA_VERSION",
    "SCHEMA_COMPONENTS",
    
    # Package Metadata
    "__version__",
    "__author__",
    "__email__",
    "__license__"
]

# Schema compatibility information
def get_schema_info():
    """Get schema version and compatibility information"""
    return {
        "package_version": __version__,
        "schema_version": SCHEMA_VERSION,
        "components": SCHEMA_COMPONENTS,
        "license": __license__,
        "foundation": "Seldon Reflex Foundation"
    }