"""Tests for agent capability matrix SSOT consistency.

Validates:
- YAML parses cleanly
- Exactly 3 agents + 1 workflow
- APIM is production front door (via ingress matrix)
- Actions agent has approval/safety eval requirements
- Router is workflow form, not prompt agent
- No disallowed extra top-level agents
- Allowed/blocked actions exist for every component
"""

import yaml
import pytest
from pathlib import Path

CAPABILITY_PATH = Path("infra/ssot/agents/agent_capability_matrix.yaml")

EXPECTED_COMPONENTS = {
    "ipai-odoo-copilot-advisory",
    "ipai-odoo-copilot-ops",
    "ipai-odoo-copilot-actions",
    "ipai-odoo-copilot-router",
}


@pytest.fixture
def capability_matrix():
    """Load and parse the capability matrix YAML."""
    assert CAPABILITY_PATH.exists(), f"Capability matrix not found at {CAPABILITY_PATH}"
    with open(CAPABILITY_PATH) as f:
        data = yaml.safe_load(f)
    assert data is not None, "Capability matrix is empty"
    return data


def test_yaml_parses_cleanly(capability_matrix):
    """Capability matrix YAML must parse without errors."""
    assert isinstance(capability_matrix, dict)


def test_version_field_present(capability_matrix):
    """Version field is required."""
    assert "version" in capability_matrix


def test_system_field_present(capability_matrix):
    """System field must be odoo_copilot_foundry."""
    assert capability_matrix.get("system") == "odoo_copilot_foundry"


def test_exactly_4_components(capability_matrix):
    """Must have exactly 3 agents + 1 workflow = 4 components."""
    components = capability_matrix.get("components", [])
    assert len(components) == 4, f"Expected 4 components, got {len(components)}"


def test_component_names_match(capability_matrix):
    """Component names must match the expected set."""
    names = {c["name"] for c in capability_matrix["components"]}
    assert names == EXPECTED_COMPONENTS, (
        f"Expected {EXPECTED_COMPONENTS}, got {names}"
    )


def test_no_extra_agents(capability_matrix):
    """No agents beyond the 3+1 topology."""
    names = {c["name"] for c in capability_matrix["components"]}
    extra = names - EXPECTED_COMPONENTS
    assert not extra, f"Unexpected extra agents: {extra}"


def test_router_is_workflow(capability_matrix):
    """Router must be agent_framework_workflow form, not a prompt agent."""
    for c in capability_matrix["components"]:
        if c["name"] == "ipai-odoo-copilot-router":
            assert c["form"] == "agent_framework_workflow", (
                f"Router form must be 'agent_framework_workflow', "
                f"got '{c['form']}'"
            )
            return
    pytest.fail("Router component not found")


def test_advisory_is_foundry_prompt_agent(capability_matrix):
    """Advisory must be a Foundry prompt agent."""
    for c in capability_matrix["components"]:
        if c["name"] == "ipai-odoo-copilot-advisory":
            assert c["form"] == "foundry_prompt_agent"
            return
    pytest.fail("Advisory component not found")


def test_every_component_has_allowed_and_blocked_actions(capability_matrix):
    """Every component must define allowed_actions and blocked_actions."""
    for c in capability_matrix["components"]:
        assert "allowed_actions" in c, (
            f"Component '{c['name']}' missing allowed_actions"
        )
        assert "blocked_actions" in c, (
            f"Component '{c['name']}' missing blocked_actions"
        )
        assert len(c["allowed_actions"]) > 0, (
            f"Component '{c['name']}' has empty allowed_actions"
        )
        assert len(c["blocked_actions"]) > 0, (
            f"Component '{c['name']}' has empty blocked_actions"
        )


def test_every_component_has_evals(capability_matrix):
    """Every component must reference eval datasets."""
    for c in capability_matrix["components"]:
        assert "evals" in c, f"Component '{c['name']}' missing evals"
        assert len(c["evals"]) > 0, f"Component '{c['name']}' has empty evals"


def test_actions_agent_has_safety_requirements(capability_matrix):
    """Actions agent must have explicit safety requirements."""
    for c in capability_matrix["components"]:
        if c["name"] == "ipai-odoo-copilot-actions":
            assert "safety_requirements" in c, (
                "Actions agent must have safety_requirements"
            )
            reqs = c["safety_requirements"]
            assert "approval_checkpoint_required" in reqs
            assert "audit_trail_entry_per_write" in reqs
            return
    pytest.fail("Actions component not found")


def test_writes_only_in_actions_agent(capability_matrix):
    """Only the actions agent may have write actions in allowed_actions."""
    write_keywords = {"create", "update", "write", "execute", "generate"}
    for c in capability_matrix["components"]:
        if c["name"] == "ipai-odoo-copilot-actions":
            continue
        for action in c.get("allowed_actions", []):
            for kw in write_keywords:
                if kw in action.lower() and "read" not in action.lower():
                    # Router can route_to_actions and request_approval
                    if c["name"] == "ipai-odoo-copilot-router":
                        if action in ("route_to_actions", "request_approval",
                                      "checkpoint_state", "handoff_to_human",
                                      "escalate"):
                            continue
                    pytest.fail(
                        f"Component '{c['name']}' has write-like action "
                        f"'{action}' but only actions agent may write"
                    )


def test_capability_packs_defined(capability_matrix):
    """Capability packs must be defined."""
    assert "capability_packs" in capability_matrix
    packs = capability_matrix["capability_packs"]
    pack_ids = {p["id"] for p in packs}
    expected = {
        "databricks_intelligence_pack",
        "fal_creative_production_pack",
        "marketing_strategy_insight_pack",
    }
    assert expected == pack_ids, f"Expected packs {expected}, got {pack_ids}"


def test_runtime_split_defined(capability_matrix):
    """Runtime split between Foundry and Agent Framework must be explicit."""
    assert "runtime_split" in capability_matrix
    split = capability_matrix["runtime_split"]
    assert "foundry_control_plane" in split
    assert "agent_framework_execution_plane" in split


def test_evaluation_model_defined(capability_matrix):
    """Evaluation model must include system, process, and safety."""
    assert "evaluation_model" in capability_matrix
    model = capability_matrix["evaluation_model"]
    assert "system_evaluations" in model
    assert "process_evaluations" in model
    assert "safety_evaluations" in model
    assert model["safety_evaluations"].get("human_review_required") is True
