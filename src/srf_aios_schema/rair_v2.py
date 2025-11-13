"""
RAIR v2 Schema (Refined Algorithmic Intelligence Representative) - Unified integration of ARC, ROLE, MACP, and PERSONA components
with dual-hash validation system for integrity verification and tamper detection.
"""

import hashlib
import uuid
from datetime import datetime, timezone
from typing import Dict, List, Optional, Literal, Any
from pydantic import BaseModel, Field, field_validator, ConfigDict

from pydantic import BaseModel, Field, field_validator, constr
from typing import List, Dict, Optional, Literal
from datetime import datetime, timezone
import uuid
import hashlib
import json
import re

# ---------- ARC: Agent Record Core ----------
class ARC(BaseModel):
    """Autonomous Reasoning Component - Core intelligence framework"""
    agent_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    arc_id: str = Field(default_factory=lambda: f"arc-{str(uuid.uuid4())[:8]}")
    name: str = Field(..., min_length=3, max_length=50)
    agent_name: str = Field(..., min_length=3, max_length=50)
    agent_class: str = Field(default="general", description="Agent classification")
    reasoning_engine: Literal["llm", "symbolic", "neuro-symbolic", "hybrid"]
    base_model: str = Field(..., min_length=5, max_length=100)
    checkpoint: str = Field(..., min_length=8, max_length=100)
    reasoning_params: Dict[str, Any]
    context_window: int = Field(ge=1024, le=128000)
    temperature: float = Field(ge=0.0, le=2.0, default=0.7)
    max_tokens: int = Field(ge=1, le=4096, default=2048)
    provider: Literal["openai", "anthropic", "cohere", "local", "custom"]
    license_class: str = Field(default="tier3", description="License tier classification")
    origin_signature: str = Field(default="", description="Cryptographic signature of agent origin")
    created_by: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    version: str = "1.0"
    provenance_hash: Optional[str] = None

# ---------- ROLE: Role & Operational Ledger ----------
class ROLE(BaseModel):
    """Resource Operations License Envelope - Permissions and governance"""
    role_scope: List[str]
    permissions: List[Literal["read", "write", "execute", "audit", "admin"]]
    reflex_scope: List[str]
    trust_vector: float = Field(ge=0.0, le=1.0)
    governance_level: Literal["core", "restricted", "sandbox", "observer"] = "sandbox"
    memory_refs: Optional[List[str]] = []
    version: int = 1

    @field_validator("role_scope")
    @classmethod
    def non_empty_scope(cls, v):
        if not v:
            raise ValueError("role_scope must contain at least one entry.")
        return v

# ---------- MACP: Memory Access Credential Protocol ----------
class MACP(BaseModel):
    """Memory Access Credential Package - Access rights and policies"""
    credential_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    scope: List[Literal["memory.read", "memory.write", "memory.search", "memory.handshake", "trustvault.commit", "audit.export"]]
    issuer: str
    expiration: datetime
    signature: Optional[str] = None
    policy_tag: Optional[str] = None

    @field_validator("expiration")
    @classmethod
    def expiration_future(cls, v):
        now = datetime.now(timezone.utc) if v.tzinfo else datetime.utcnow()
        if v <= now:
            raise ValueError("credential expiration must be in the future.")
        return v

# ---------- PERSONA: Temperament & Moral Accent ----------
class TONEVector(BaseModel):
    """Tone vector defining agent communication style"""
    direct: float = Field(ge=0.0, le=1.0)
    warm: float = Field(ge=0.0, le=1.0)
    humorous: float = Field(ge=0.0, le=1.0)
    formal: float = Field(ge=0.0, le=1.0)

class PERSONA(BaseModel):
    """Temperament & Moral Accent - Agent personality and ethical framework"""
    persona_id: str = Field(default_factory=lambda: f"persona-{str(uuid.uuid4())[:8]}")
    name: str = Field(..., min_length=3, max_length=40)
    temperament_profile: Literal["strategic", "empathic", "analytic", "stoic", "adaptive"]
    moral_accent: Literal["deontic", "utilitarian", "virtue", "reflexic"]
    tone_vector: TONEVector
    alignment_directives: List[str]
    embedding_ref: Optional[str] = None
    trust_seed: float = Field(ge=0.0, le=1.0, default=0.95)
    created_by: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    version: str = "1.0"
    provenance_hash: Optional[str] = None

    @field_validator("provenance_hash", mode="before")
    @classmethod
    def compute_persona_hash(cls, v, info):
        """Compute deterministic hash of persona configuration"""
        if v is not None:
            return v
        
        values = info.data
        body = json.dumps({
            k: (str(v) if not isinstance(v, datetime) else v.isoformat())
            for k, v in values.items() if k != "provenance_hash"
        }, sort_keys=True, default=str).encode()
        return hashlib.sha256(body).hexdigest()

# ---------- RAIR: Reflexic Agent Identity Record ----------
class RAIR(BaseModel):
    """
    Unified Reflexic Agent Identity Record
    
    Combines ARC (origin), ROLE (function), MACP (rights), and PERSONA (conscience)
    into a single verifiable agent identity with dual-hash provenance system.
    """
    arc: ARC
    role: ROLE
    macp: MACP
    persona: PERSONA
    policy_version: str = "v2.0"
    provenance_hash: Optional[str] = None

    @field_validator("provenance_hash", mode="before")
    @classmethod
    def compute_rair_hash(cls, v, info):
        """Compute deterministic hash of complete RAIR configuration"""
        if v is not None:
            return v
            
        values = info.data
        body = json.dumps(values, default=str, sort_keys=True).encode()
        return hashlib.sha256(body).hexdigest()

# ---------- TrustVault Commit Record ----------
class TrustVaultRecord(BaseModel):
    """TrustVault commit record with dual-hash verification"""
    agent_id: str
    persona_hash: str
    rair_hash: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    verified: bool = True

# ---------- Validation Utilities ----------
def validate_rair_configuration(rair_data: dict) -> tuple[bool, list[str]]:
    """
    Validate complete RAIR configuration
    
    Returns:
        tuple: (is_valid, list_of_errors)
    """
    try:
        rair = RAIR(**rair_data)
        return True, []
    except Exception as e:
        return False, [str(e)]

def compute_rair_hashes(rair: RAIR) -> dict:
    """
    Compute both persona and RAIR provenance hashes
    
    Returns:
        dict: {"persona_hash": str, "rair_hash": str}
    """
    return {
        "persona_hash": rair.persona.provenance_hash,
        "rair_hash": rair.provenance_hash
    }

# ---------- Schema Information ----------
SCHEMA_VERSION = "v2.0"
SCHEMA_COMPONENTS = ["ARC", "ROLE", "MACP", "PERSONA"]

# Export all models for easy importing
__all__ = [
    "ARC", "ROLE", "MACP", "PERSONA", "TONEVector", "RAIR", "TrustVaultRecord",
    "validate_rair_configuration", "compute_rair_hashes",
    "SCHEMA_VERSION", "SCHEMA_COMPONENTS"
]