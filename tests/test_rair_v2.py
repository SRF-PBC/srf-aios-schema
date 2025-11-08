"""Basic tests for RAIR v2 schemas."""

from srf_aios_schema import RAIR, ARC, ROLE, MACP, PERSONA, TONEVector


def test_imports():
    """Test that all main components can be imported."""
    assert RAIR is not None
    assert ARC is not None
    assert ROLE is not None
    assert MACP is not None
    assert PERSONA is not None
    assert TONEVector is not None


def test_rair_minimal():
    """Test minimal RAIR creation."""
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

    from datetime import datetime, timedelta

    macp = MACP(
        credential_id="cred-001",
        scope=["memory.read"],
        issuer="test-issuer",
        expiration=datetime.utcnow() + timedelta(days=30),
    )

    persona = PERSONA(
        name="TestBot",
        temperament_profile="analytic",
        moral_accent="reflexic",
        tone_vector=TONEVector(direct=0.5, warm=0.5, humorous=0.5, formal=0.5),
        alignment_directives=["test"],
        created_by="test-system",
    )

    agent = RAIR(arc=arc, role=role, macp=macp, persona=persona)

    assert agent.arc.name == "TestAgent"
    assert agent.role.role_scope == ["test"]
    assert agent.persona.name == "TestBot"


def test_package_version():
    """Test package version is accessible."""
    import srf_aios_schema

    assert hasattr(srf_aios_schema, "__version__")
    assert srf_aios_schema.__version__ == "2.0.0"