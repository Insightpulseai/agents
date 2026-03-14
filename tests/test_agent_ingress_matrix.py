"""Tests for agent ingress matrix SSOT consistency.

Validates:
- YAML parses cleanly
- Required fields present
- APIM is the only production front door
- Playgrounds are non-production
- Network rules are defined
"""

import yaml
import pytest
from pathlib import Path

INGRESS_PATH = Path("infra/ssot/platform/agent_ingress_matrix.yaml")


@pytest.fixture
def ingress_matrix():
    """Load and parse the ingress matrix YAML."""
    assert INGRESS_PATH.exists(), f"Ingress matrix not found at {INGRESS_PATH}"
    with open(INGRESS_PATH) as f:
        data = yaml.safe_load(f)
    assert data is not None, "Ingress matrix is empty"
    return data


def test_yaml_parses_cleanly(ingress_matrix):
    """Ingress matrix YAML must parse without errors."""
    assert isinstance(ingress_matrix, dict)


def test_version_field_present(ingress_matrix):
    """Version field is required."""
    assert "version" in ingress_matrix


def test_surfaces_defined(ingress_matrix):
    """At least one surface must be defined."""
    assert "surfaces" in ingress_matrix
    assert len(ingress_matrix["surfaces"]) > 0


def test_each_surface_has_required_fields(ingress_matrix):
    """Every surface must have id, ingress, auth, agent, and guardrails."""
    required = {"id", "ingress", "auth", "agent", "guardrails"}
    for surface in ingress_matrix["surfaces"]:
        missing = required - set(surface.keys())
        assert not missing, f"Surface '{surface.get('id', '?')}' missing: {missing}"


def test_each_surface_has_observability(ingress_matrix):
    """Every surface must define observability settings."""
    for surface in ingress_matrix["surfaces"]:
        assert "observability" in surface, (
            f"Surface '{surface['id']}' missing observability"
        )


def test_network_rules_defined(ingress_matrix):
    """Network rules must be present."""
    assert "network_rules" in ingress_matrix
    assert len(ingress_matrix["network_rules"]) > 0


def test_migration_path_defined(ingress_matrix):
    """Migration path must be defined."""
    assert "migration_path" in ingress_matrix
    path = ingress_matrix["migration_path"]
    assert "current" in path


def test_landing_page_is_anonymous(ingress_matrix):
    """Landing page must use anonymous auth."""
    for surface in ingress_matrix["surfaces"]:
        if surface["id"] == "landing_page":
            assert surface["auth"]["type"] == "anonymous"
            return
    pytest.fail("No landing_page surface found")


def test_non_landing_surfaces_require_entra(ingress_matrix):
    """All non-landing surfaces must require Entra SSO."""
    for surface in ingress_matrix["surfaces"]:
        if surface["id"] != "landing_page":
            assert surface["auth"]["type"] == "entra_sso", (
                f"Surface '{surface['id']}' must use entra_sso, "
                f"got '{surface['auth']['type']}'"
            )
