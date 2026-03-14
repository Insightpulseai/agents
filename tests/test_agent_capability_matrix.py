"""Tests for agent capability matrix YAML integrity."""
import yaml
import pytest
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
MATRIX_PATH = REPO_ROOT / "infra" / "ssot" / "agents" / "agent_capability_matrix.yaml"


@pytest.fixture
def matrix():
    """Load agent capability matrix."""
    with open(MATRIX_PATH) as f:
        return yaml.safe_load(f)


def test_yaml_parses(matrix):
    """Matrix YAML must parse without errors."""
    assert matrix is not None


def test_has_version(matrix):
    """Matrix must have a version field."""
    assert "version" in matrix


def test_system_is_odoo_copilot(matrix):
    """System must be odoo_copilot_foundry."""
    assert matrix["system"] == "odoo_copilot_foundry"


def test_exactly_four_components(matrix):
    """Must have exactly 3 agents + 1 workflow = 4 components."""
    assert len(matrix["components"]) == 4


def test_component_names(matrix):
    """Component names must match the canonical set."""
    names = {c["name"] for c in matrix["components"]}
    expected = {
        "ipai-odoo-copilot-advisory",
        "ipai-odoo-copilot-ops",
        "ipai-odoo-copilot-actions",
        "ipai-odoo-copilot-router",
    }
    assert names == expected


def test_advisory_is_prompt_agent(matrix):
    """Advisory must be a Foundry prompt agent."""
    advisory = next(c for c in matrix["components"] if c["name"] == "ipai-odoo-copilot-advisory")
    assert advisory["form"] == "foundry_prompt_agent"


def test_router_is_workflow(matrix):
    """Router must be a workflow, not a prompt agent."""
    router = next(c for c in matrix["components"] if c["name"] == "ipai-odoo-copilot-router")
    assert "workflow" in router["form"]


def test_every_component_has_required_fields(matrix):
    """Every component must have form, purpose, allowed_actions, blocked_actions, evals."""
    for comp in matrix["components"]:
        assert "form" in comp, f"{comp['name']} missing form"
        assert "purpose" in comp, f"{comp['name']} missing purpose"
        assert "allowed_actions" in comp, f"{comp['name']} missing allowed_actions"
        assert "blocked_actions" in comp, f"{comp['name']} missing blocked_actions"
        assert "evals" in comp, f"{comp['name']} missing evals"


def test_advisory_has_no_write_tools(matrix):
    """Advisory must not have write tools."""
    advisory = next(c for c in matrix["components"] if c["name"] == "ipai-odoo-copilot-advisory")
    tools = advisory.get("tools", [])
    write_indicators = ["write", "create", "update", "delete", "compute", "generate"]
    for tool in tools:
        for indicator in write_indicators:
            assert indicator not in tool.lower(), f"Advisory has write-like tool: {tool}"


def test_actions_has_approval_eval(matrix):
    """Actions agent must have approval compliance in safety evals."""
    actions = next(c for c in matrix["components"] if c["name"] == "ipai-odoo-copilot-actions")
    safety_evals = actions.get("evals", {}).get("safety", [])
    assert "approval_compliance" in safety_evals


def test_actions_has_refusal_eval(matrix):
    """Actions agent must have unauthorized action refusal in safety evals."""
    actions = next(c for c in matrix["components"] if c["name"] == "ipai-odoo-copilot-actions")
    safety_evals = actions.get("evals", {}).get("safety", [])
    assert "unauthorized_action_refusal" in safety_evals


def test_no_extra_vendor_agents(matrix):
    """No vendor-specific top-level agents (Databricks, fal, Smartly, etc.)."""
    names = {c["name"] for c in matrix["components"]}
    vendor_keywords = ["databricks", "fal", "smartly", "quilt", "lions", "dataintelligence"]
    for name in names:
        for keyword in vendor_keywords:
            assert keyword not in name.lower(), f"Vendor-specific agent found: {name}"


def test_capability_packs_exist(matrix):
    """Capability packs section must exist and contain required packs."""
    assert "capability_packs" in matrix
    pack_names = set(matrix["capability_packs"].keys())
    required = {"databricks_intelligence", "fal_creative_production", "marketing_strategy_and_insight", "bir_compliance"}
    assert required.issubset(pack_names), f"Missing packs: {required - pack_names}"
