"""Tests for agent ingress matrix YAML integrity."""
import yaml
import pytest
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
INGRESS_PATH = REPO_ROOT / "infra" / "ssot" / "platform" / "agent_ingress_matrix.yaml"


@pytest.fixture
def ingress():
    """Load agent ingress matrix."""
    with open(INGRESS_PATH) as f:
        return yaml.safe_load(f)


def test_yaml_parses(ingress):
    """Ingress YAML must parse without errors."""
    assert ingress is not None


def test_has_version(ingress):
    """Ingress must have a version field."""
    assert "version" in ingress


def test_system_is_odoo_copilot(ingress):
    """System must be odoo_copilot_foundry."""
    assert ingress["system"] == "odoo_copilot_foundry"


def test_has_ingress_paths(ingress):
    """Must have ingress_paths defined."""
    assert "ingress_paths" in ingress
    assert len(ingress["ingress_paths"]) >= 5


def test_required_ingress_names(ingress):
    """Must include all required ingress paths."""
    names = {p["name"] for p in ingress["ingress_paths"]}
    required = {
        "foundry_project_client",
        "openai_compatible_client",
        "direct_rest",
        "apim_ai_gateway",
        "foundry_playgrounds",
    }
    assert required.issubset(names), f"Missing ingress paths: {required - names}"


def test_apim_is_production(ingress):
    """APIM AI gateway must be marked as the production front door."""
    apim = next(p for p in ingress["ingress_paths"] if p["name"] == "apim_ai_gateway")
    assert apim.get("production") is True


def test_playgrounds_not_production(ingress):
    """Foundry Playgrounds must be explicitly non-production."""
    playgrounds = next(p for p in ingress["ingress_paths"] if p["name"] == "foundry_playgrounds")
    assert playgrounds.get("production") is False


def test_every_path_has_purpose(ingress):
    """Every ingress path must have a purpose field."""
    for path in ingress["ingress_paths"]:
        assert "purpose" in path, f"{path['name']} missing purpose"


def test_every_path_has_governance(ingress):
    """Every ingress path must have a governance field."""
    for path in ingress["ingress_paths"]:
        assert "governance" in path, f"{path['name']} missing governance"


def test_component_ingress_ownership(ingress):
    """Component ingress ownership must be defined for all 4 components."""
    ownership = ingress.get("component_ingress_ownership", {})
    required = {"advisory", "ops", "actions", "router"}
    assert required.issubset(set(ownership.keys())), f"Missing components: {required - set(ownership.keys())}"
