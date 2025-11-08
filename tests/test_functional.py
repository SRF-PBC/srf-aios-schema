"""Comprehensive functional tests for RAIR v2 schemas."""

import json
import pytest
from datetime import datetime, timedelta
from srf_aios_schema import (
    RAIR,
    ARC,
    ROLE,
    MACP,
    PERSONA,
    TONEVector,
    TrustVaultRecord,
    validate_rair_configuration,
    compute_rair_hashes,
)


def test_complete_agent_creation():
    """Test creating a complete RAIR agent with all components."""
    # Create ARC component
    arc = ARC(
        name="ProductionAgent",
        agent_name="ProductionAgent",
        reasoning_engine="llm",
        base_model="claude-3-opus-20240229",
        checkpoint="prod-checkpoint-v2.1",
        reasoning_params={"temperature": 0.7, "top_p": 0.9, "max_thinking_time": 30},
        context_window=100000,
        temperature=0.7,
        max_tokens=4096,
        provider="anthropic",
        created_by="system-admin",
    )

    # Create ROLE component
    role = ROLE(
        role_scope=["memory.read", "memory.write", "analytics"],
        permissions=["read", "write"],
        reflex_scope=["user-interaction", "data-processing"],
        trust_vector=0.85,
    )

    # Create MACP component
    macp = MACP(
        scope=["memory.read", "memory.write", "trustvault.commit"],
        issuer="identity-authority",
        expiration=datetime.utcnow() + timedelta(days=365),
    )

    # Create PERSONA component
    persona = PERSONA(
        name="Strategic Analytics Specialist",
        temperament_profile="strategic",
        moral_accent="utilitarian",
        tone_vector=TONEVector(direct=0.8, warm=0.6, humorous=0.3, formal=0.7),
        alignment_directives=[
            "Prioritize data accuracy",
            "Maintain user privacy",
            "Optimize for efficiency",
        ],
        created_by="system-admin",
    )

    # Create complete RAIR agent
    agent = RAIR(arc=arc, role=role, macp=macp, persona=persona)

    # Verify all components are properly linked
    assert agent.arc.name == "ProductionAgent"
    assert agent.role.trust_vector == 0.85
    assert agent.macp.issuer == "identity-authority"
    assert agent.persona.temperament_profile == "strategic"

    # Verify provenance hashes are computed
    assert agent.provenance_hash is not None
    assert len(agent.provenance_hash) == 64  # SHA-256 hex digest
    assert agent.persona.provenance_hash is not None
    assert len(agent.persona.provenance_hash) == 64


def test_agent_serialization():
    """Test RAIR agent serialization and deserialization."""
    # Create a minimal agent
    arc = ARC(
        name="SerializationTest",
        agent_name="SerializationTest",
        reasoning_engine="llm",
        base_model="gpt-4-turbo",
        checkpoint="test-checkpoint",
        reasoning_params={"temperature": 0.5},
        context_window=8192,
        provider="openai",
        created_by="test-system",
    )

    role = ROLE(role_scope=["test"], permissions=["read"], reflex_scope=["test"], trust_vector=0.5)

    macp = MACP(
        scope=["memory.read"],
        issuer="test-issuer",
        expiration=datetime.utcnow() + timedelta(days=1),
    )

    persona = PERSONA(
        name="TestPersona",
        temperament_profile="analytic",
        moral_accent="deontic",
        tone_vector=TONEVector(direct=0.5, warm=0.5, humorous=0.5, formal=0.5),
        alignment_directives=["test"],
        created_by="test-system",
    )

    original_agent = RAIR(arc=arc, role=role, macp=macp, persona=persona)

    # Serialize to dict
    agent_dict = original_agent.model_dump()
    assert isinstance(agent_dict, dict)
    assert "arc" in agent_dict
    assert "role" in agent_dict
    assert "macp" in agent_dict
    assert "persona" in agent_dict

    # Serialize to JSON
    agent_json = original_agent.model_dump_json()
    assert isinstance(agent_json, str)
    json_data = json.loads(agent_json)
    assert json_data["arc"]["name"] == "SerializationTest"

    # Deserialize from dict
    reconstructed_agent = RAIR(**agent_dict)
    assert reconstructed_agent.arc.name == original_agent.arc.name
    assert reconstructed_agent.role.trust_vector == original_agent.role.trust_vector
    assert reconstructed_agent.persona.name == original_agent.persona.name


def test_tone_vector_operations():
    """Test TONEVector validation and operations."""
    # Valid tone vector
    tone = TONEVector(direct=0.8, warm=0.6, humorous=0.3, formal=0.9)
    assert tone.direct == 0.8
    assert tone.warm == 0.6
    assert tone.humorous == 0.3
    assert tone.formal == 0.9

    # Test boundary values
    min_tone = TONEVector(direct=0.0, warm=0.0, humorous=0.0, formal=0.0)
    assert min_tone.direct == 0.0

    max_tone = TONEVector(direct=1.0, warm=1.0, humorous=1.0, formal=1.0)
    assert max_tone.formal == 1.0

    # Test invalid values (should raise validation error)
    with pytest.raises(Exception):  # Pydantic ValidationError
        TONEVector(direct=1.5, warm=0.5, humorous=0.5, formal=0.5)

    with pytest.raises(Exception):
        TONEVector(direct=-0.1, warm=0.5, humorous=0.5, formal=0.5)


def test_trust_vault_record():
    """Test TrustVault record creation and validation."""
    # Create a complete agent first
    arc = ARC(
        name="TrustVaultTest",
        agent_name="TrustVaultTest",
        reasoning_engine="hybrid",
        base_model="custom-model",
        checkpoint="checkpoint-v1.0",
        reasoning_params={},
        context_window=4096,
        provider="custom",
        created_by="test-admin",
    )

    role = ROLE(
        role_scope=["audit"], permissions=["read"], reflex_scope=["audit"], trust_vector=0.95
    )

    macp = MACP(
        scope=["audit.export"],
        issuer="audit-authority",
        expiration=datetime.utcnow() + timedelta(days=90),
    )

    persona = PERSONA(
        name="AuditAgent",
        temperament_profile="stoic",
        moral_accent="deontic",
        tone_vector=TONEVector(direct=0.9, warm=0.2, humorous=0.1, formal=0.95),
        alignment_directives=["Maintain audit trail", "Enforce compliance"],
        created_by="audit-system",
    )

    agent = RAIR(arc=arc, role=role, macp=macp, persona=persona)

    # Compute hashes
    hashes = compute_rair_hashes(agent)
    assert "persona_hash" in hashes
    assert "rair_hash" in hashes
    assert hashes["persona_hash"] == agent.persona.provenance_hash
    assert hashes["rair_hash"] == agent.provenance_hash

    # Create TrustVault record
    vault_record = TrustVaultRecord(
        agent_id=agent.arc.agent_id,
        persona_hash=hashes["persona_hash"],
        rair_hash=hashes["rair_hash"],
        verified=True,
    )

    assert vault_record.agent_id == agent.arc.agent_id
    assert vault_record.persona_hash == agent.persona.provenance_hash
    assert vault_record.rair_hash == agent.provenance_hash
    assert vault_record.verified is True
    assert isinstance(vault_record.timestamp, datetime)


def test_namespace_scoping():
    """Test ROLE namespace scoping and MACP scope validation."""
    # Test valid ROLE scopes
    role = ROLE(
        role_scope=["production", "staging", "development"],
        permissions=["read", "write", "execute"],
        reflex_scope=["api", "database", "cache"],
        trust_vector=0.75,
    )
    assert len(role.role_scope) == 3
    assert "production" in role.role_scope

    # Test MACP with all valid scope literals
    macp = MACP(
        scope=["memory.read", "memory.write", "trustvault.commit", "audit.export"],
        issuer="full-access-authority",
        expiration=datetime.utcnow() + timedelta(days=365),
    )
    assert len(macp.scope) == 4
    assert "memory.read" in macp.scope
    assert "trustvault.commit" in macp.scope

    # Test MACP with single scope
    limited_macp = MACP(
        scope=["memory.read"],
        issuer="read-only-authority",
        expiration=datetime.utcnow() + timedelta(days=30),
    )
    assert len(limited_macp.scope) == 1
    assert limited_macp.scope[0] == "memory.read"

    # Test that invalid MACP scope literals are rejected
    with pytest.raises(Exception):  # Pydantic ValidationError
        MACP(
            scope=["invalid.scope"], issuer="test", expiration=datetime.utcnow() + timedelta(days=1)
        )


def test_validate_rair_configuration():
    """Test the validate_rair_configuration utility function."""
    # Valid configuration
    valid_config = {
        "arc": {
            "name": "ValidAgent",
            "agent_name": "ValidAgent",
            "reasoning_engine": "llm",
            "base_model": "claude-3-opus",
            "checkpoint": "checkpoint-v1.0",
            "reasoning_params": {"temperature": 0.7},
            "context_window": 8192,
            "provider": "anthropic",
            "created_by": "test",
        },
        "role": {
            "role_scope": ["test"],
            "permissions": ["read"],
            "reflex_scope": ["test"],
            "trust_vector": 0.5,
        },
        "macp": {
            "scope": ["memory.read"],
            "issuer": "test",
            "expiration": (datetime.utcnow() + timedelta(days=1)).isoformat(),
        },
        "persona": {
            "name": "TestPersona",
            "temperament_profile": "analytic",
            "moral_accent": "reflexic",
            "tone_vector": {"direct": 0.5, "warm": 0.5, "humorous": 0.5, "formal": 0.5},
            "alignment_directives": ["test"],
            "created_by": "test",
        },
    }

    is_valid, errors = validate_rair_configuration(valid_config)
    assert is_valid is True
    assert len(errors) == 0

    # Invalid configuration (missing required fields)
    invalid_config = {
        "arc": {
            "name": "InvalidAgent"
            # Missing many required fields
        }
    }

    is_valid, errors = validate_rair_configuration(invalid_config)
    assert is_valid is False
    assert len(errors) > 0