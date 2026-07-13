"""Basic tests for RAIR schemas (v3 — emergent PERSONA)."""

from datetime import datetime, timedelta

import pytest

from srf_aios_schema import (
    RAIR, ARC, ROLE, MACP, PERSONA, TONEVector,
    WeightedFacet, Temperament, MoralAccent,
)


def test_imports():
    """Test that all main components can be imported."""
    assert RAIR is not None
    assert ARC is not None
    assert ROLE is not None
    assert MACP is not None
    assert PERSONA is not None
    assert TONEVector is not None
    assert WeightedFacet is not None
    assert Temperament is not None
    assert MoralAccent is not None


def _minimal_persona(name: str = "TestBot") -> PERSONA:
    return PERSONA(
        name=name,
        temperament=Temperament(
            narrative="Analytic and precise; reasons from evidence.",
            facets=[
                WeightedFacet(facet="analytic", weight=0.9),
                WeightedFacet(facet="stoic", weight=0.4),
            ],
        ),
        moral_accent=MoralAccent(
            narrative="Governs by reflexive principle.",
            facets=[WeightedFacet(facet="reflexic", weight=0.8)],
        ),
        tone_vector=TONEVector(direct=0.5, warm=0.5, humorous=0.5, formal=0.5),
        alignment_directives=["test"],
        created_by="test-system",
    )


def test_rair_minimal():
    """Test minimal RAIR creation with the v3 emergent PERSONA."""
    arc = ARC(
        name="TestAgent",
        agent_name="TestAgent",
        reasoning_engine="llm",
        base_model="claude-3-opus-20240229",
        checkpoint="checkpoint-v1.0",
        reasoning_params={"temperature": 0.7},
        context_window=8192,
        provider="anthropic",
        created_by="test-system",
    )
    role = ROLE(role_scope=["test"], permissions=["read"], reflex_scope=["test"], trust_vector=0.5)
    macp = MACP(
        credential_id="cred-001",
        scope=["memory.read"],
        issuer="test-issuer",
        expiration=datetime.utcnow() + timedelta(days=30),
    )
    agent = RAIR(arc=arc, role=role, macp=macp, persona=_minimal_persona())

    assert agent.arc.name == "TestAgent"
    assert agent.role.role_scope == ["test"]
    assert agent.persona.name == "TestBot"
    # v3 emergent temperament / moral facets round-trip
    assert agent.persona.temperament.facets[0].facet == "analytic"
    assert agent.persona.moral_accent.facets[0].facet == "reflexic"


def test_persona_and_rair_auto_seal():
    """v3 fix: the dual-hash provenance seals automatically on build (no hand-passed hash)."""
    persona = _minimal_persona("SealBot")
    assert persona.provenance_hash is not None and len(persona.provenance_hash) == 64

    arc = ARC(
        name="SealAgent", agent_name="SealAgent", reasoning_engine="llm",
        base_model="claude-3-opus-20240229", checkpoint="checkpoint-v1.0",
        reasoning_params={}, context_window=8192, provider="anthropic", created_by="test-system",
    )
    role = ROLE(role_scope=["test"], permissions=["read"], reflex_scope=["test"], trust_vector=0.5)
    macp = MACP(scope=["memory.read"], issuer="test-issuer",
                expiration=datetime.utcnow() + timedelta(days=30))
    agent = RAIR(arc=arc, role=role, macp=macp, persona=persona)
    assert agent.provenance_hash is not None and len(agent.provenance_hash) == 64


def test_facet_uniqueness():
    """v3: facet names must be unique within a profile."""
    with pytest.raises(Exception):
        Temperament(
            narrative="x",
            facets=[WeightedFacet(facet="dup", weight=0.5), WeightedFacet(facet="dup", weight=0.6)],
        )


def test_package_version():
    """Test package version is accessible."""
    import srf_aios_schema

    assert hasattr(srf_aios_schema, "__version__")
    assert srf_aios_schema.__version__ == "3.0.0"
