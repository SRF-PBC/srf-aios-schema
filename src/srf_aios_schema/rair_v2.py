"""
RAIR Schema (Reflexic Agent Identity Record) — Unified integration of ARC, ROLE, MACP, and
PERSONA components with a dual-hash validation system for integrity verification and tamper
detection.

v3.0 (2026-07): PERSONA `temperament` and `moral_accent` migrated from fixed `Literal` enums
to an EMERGENT trait model — a free character narrative + an OPEN, weighted, evidence-grounded
facet set (vocabulary governed by the SRF facet lexicon). Rationale: identity, like meaning,
emerges from content/behavior; it is not selected from a menu (the v2 enum could not even
express "creative"). ARC / ROLE / MACP and the dual-hash / TrustVault provenance are unchanged.
"""

import hashlib
import json
import uuid
from datetime import datetime, UTC
from typing import Literal, Any
from pydantic import BaseModel, Field, field_validator, model_validator

# ---------- ARC: Agent Record Core ----------
class ARC(BaseModel):
    """Agent Record Core — the DURABLE identity core: who this agent is, from whom, since when.

    v4.0 (2026-07) — **the embodiment fields were REMOVED**: `reasoning_engine`, `base_model`,
    `checkpoint`, `reasoning_params`, `context_window`, `temperature`, `max_tokens`, `provider`,
    `license_class`.

    Rationale — **the model is fungible; an agent persists across vessel changes.** Sealing the
    vessel into the identity hash would (a) break the seal on every model upgrade, making an engine
    swap an appended correction on an immutable worldline, and (b) imply the agent *is* its weights —
    so upgrading the model would kill it and instantiate someone else. A self is not its substrate.

    Which substrate is currently computing an agent is an **adapter concern**, and per-action
    provenance is already emitted where the actions happen (commit trailers, run telemetry, and the
    Deployment Capsule layer per INV-DEP-1/2). The identity record does not track it, and must not:
    a second copy of runtime state is a second source of truth, and it drifts.
    """
    agent_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    arc_id: str = Field(default_factory=lambda: f"arc-{str(uuid.uuid4())[:8]}")
    name: str = Field(..., min_length=3, max_length=50)
    agent_name: str = Field(..., min_length=3, max_length=50)
    agent_class: str = Field(default="general", description="Agent classification")
    origin_signature: str = Field(default="", description="Cryptographic signature of agent origin")
    created_by: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    version: str = "4.0"
    provenance_hash: str | None = None

# ---------- ROLE: Role & Operational Ledger ----------
class ROLE(BaseModel):
    """Resource Operations License Envelope - Permissions and governance"""
    role_scope: list[str]
    permissions: list[Literal["read", "write", "execute", "audit", "admin"]]
    reflex_scope: list[str]
    trust_vector: float = Field(ge=0.0, le=1.0)
    governance_level: Literal["core", "restricted", "sandbox", "observer"] = "sandbox"
    memory_refs: list[str] | None = []
    version: int = 1

    @field_validator("role_scope")
    @classmethod
    def non_empty_scope(cls, v: list[str]) -> list[str]:
        if not v:
            raise ValueError("role_scope must contain at least one entry.")
        return v

# ---------- MACP: Memory Access Credential Protocol ----------
class MACP(BaseModel):
    """Memory Access Credential Package - Access rights and policies"""
    credential_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    scope: list[Literal["memory.read", "memory.write", "memory.search", "memory.handshake", "trustvault.commit", "audit.export"]]
    issuer: str
    expiration: datetime
    signature: str | None = None
    policy_tag: str | None = None

    @field_validator("expiration")
    @classmethod
    def expiration_future(cls, v: datetime) -> datetime:
        now = datetime.now(UTC) if v.tzinfo else datetime.utcnow()
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

# ---------- Emergent trait model (v3): facets, not enums ----------
# SRF principle: identity — like meaning — EMERGES from content/behavior; it is not
# selected from a fixed menu. Temperament and moral character are therefore a free
# narrative + an OPEN, weighted, evidence-grounded facet set (vocabulary governed by
# the SRF facet lexicon), never a closed Literal enum. (The v2 enum could not even
# express "creative".)
class WeightedFacet(BaseModel):
    """One named trait facet with a strength weight and optional episodic evidence.
    `facet` is a canonical name from the SRF facet lexicon — OPEN and reconciled, not a
    fixed enum: new facets are added, not chosen."""
    facet: str = Field(..., min_length=2, max_length=60)
    weight: float = Field(ge=0.0, le=1.0)
    evidence_refs: list[str] = Field(
        default_factory=list,
        description="Pointers to the episodes that evidence this facet (emergent grounding)",
    )

class Temperament(BaseModel):
    """Emergent temperament: a free character narrative + an open weighted facet set + an
    embedding for identity_resonance/distance. Replaces the v2 `temperament_profile` enum,
    which could not hold blends or novel traits."""
    narrative: str = Field(..., min_length=1, description="The prose character, un-rounded")
    facets: list[WeightedFacet] = Field(default_factory=list)
    embedding_ref: str | None = Field(
        default=None, description="Embedding of the narrative (pinned model) for resonance/distance"
    )

    @field_validator("facets")
    @classmethod
    def unique_facets(cls, v: list["WeightedFacet"]) -> list["WeightedFacet"]:
        names = [f.facet for f in v]
        if len(names) != len(set(names)):
            raise ValueError("facet names must be unique within a temperament profile.")
        return v

class MoralAccent(BaseModel):
    """Emergent moral character: a narrative + an open weighted facet set (e.g. virtue 0.8,
    reflexic 0.6) + an embedding. Replaces the v2 deontic/utilitarian/virtue/reflexic enum —
    a conscience is a blend, not one label."""
    narrative: str = Field(..., min_length=1, description="The prose moral character, un-rounded")
    facets: list[WeightedFacet] = Field(default_factory=list)
    embedding_ref: str | None = None

    @field_validator("facets")
    @classmethod
    def unique_facets(cls, v: list["WeightedFacet"]) -> list["WeightedFacet"]:
        names = [f.facet for f in v]
        if len(names) != len(set(names)):
            raise ValueError("facet names must be unique within a moral-accent profile.")
        return v

class PERSONA(BaseModel):
    """Temperament & Moral Accent - Agent personality and ethical framework (v3: emergent)"""
    persona_id: str = Field(default_factory=lambda: f"persona-{str(uuid.uuid4())[:8]}")
    name: str = Field(..., min_length=3, max_length=40)
    temperament: Temperament
    moral_accent: MoralAccent
    tone_vector: TONEVector
    alignment_directives: list[str]
    embedding_ref: str | None = None
    trust_seed: float = Field(ge=0.0, le=1.0, default=0.95)
    created_by: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    version: str = "3.0"
    provenance_hash: str | None = None

    @model_validator(mode="after")
    def _seal_persona(self) -> "PERSONA":
        """Auto-seal: compute the deterministic persona provenance hash on build.
        (v3 fix: was a before-validator that never fired for default/unset hashes.)"""
        if self.provenance_hash is None:
            body = self.model_dump(exclude={"provenance_hash"})
            self.provenance_hash = hashlib.sha256(
                json.dumps(body, sort_keys=True, default=str).encode()
            ).hexdigest()
        return self

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
    policy_version: str = "v4.0"
    provenance_hash: str | None = None

    @model_validator(mode="after")
    def _seal_rair(self) -> "RAIR":
        """Auto-seal: compute the deterministic RAIR provenance hash on build (covers the
        already-sealed persona → dual-hash). (v3 fix: was a before-validator that never fired.)"""
        if self.provenance_hash is None:
            body = self.model_dump(exclude={"provenance_hash"})
            self.provenance_hash = hashlib.sha256(
                json.dumps(body, sort_keys=True, default=str).encode()
            ).hexdigest()
        return self

# ---------- TrustVault Commit Record ----------
class TrustVaultRecord(BaseModel):
    """TrustVault commit record with dual-hash verification"""
    agent_id: str
    persona_hash: str
    rair_hash: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    verified: bool = True

# ---------- Validation Utilities ----------
def validate_rair_configuration(rair_data: dict[str, Any]) -> tuple[bool, list[str]]:
    """
    Validate complete RAIR configuration

    Returns:
        tuple: (is_valid, list_of_errors)
    """
    try:
        RAIR(**rair_data)  # Validation happens in constructor
        return True, []
    except Exception as e:
        return False, [str(e)]

def compute_rair_hashes(rair: RAIR) -> dict[str, str | None]:
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
SCHEMA_VERSION = "v4.0"
SCHEMA_COMPONENTS = ["ARC", "ROLE", "MACP", "PERSONA"]

# Export all models for easy importing
__all__ = [
    "ARC", "ROLE", "MACP", "PERSONA", "TONEVector",
    "WeightedFacet", "Temperament", "MoralAccent",
    "RAIR", "TrustVaultRecord",
    "validate_rair_configuration", "compute_rair_hashes",
    "SCHEMA_VERSION", "SCHEMA_COMPONENTS"
]
