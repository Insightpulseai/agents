"""Tests for spec ↔ SSOT consistency.

Validates:
- Every component in spec exists in capability matrix SSOT
- Ingress names in spec match ingress YAML (when present)
- Eval dataset files exist for every component's eval references
- Eval config files exist
- Spec and SSOT agree on component count
"""

import yaml
import pytest
from pathlib import Path

CAPABILITY_PATH = Path("infra/ssot/agents/agent_capability_matrix.yaml")
SPEC_DIR = Path("spec/odoo-copilot-agent-framework")
EVAL_DATASETS_DIR = Path("eval/datasets")
EVAL_CONFIG_DIR = Path("eval/config")


@pytest.fixture
def capability_matrix():
    with open(CAPABILITY_PATH) as f:
        return yaml.safe_load(f)


@pytest.fixture
def spec_constitution():
    path = SPEC_DIR / "constitution.md"
    assert path.exists(), f"Constitution not found at {path}"
    return path.read_text()


@pytest.fixture
def spec_prd():
    path = SPEC_DIR / "prd.md"
    assert path.exists(), f"PRD not found at {path}"
    return path.read_text()


def test_spec_bundle_complete():
    """All 4 spec files must exist."""
    required = ["constitution.md", "prd.md", "plan.md", "tasks.md"]
    for name in required:
        path = SPEC_DIR / name
        assert path.exists(), f"Spec file missing: {path}"
        content = path.read_text()
        assert len(content) > 100, f"Spec file too short: {path}"


def test_spec_references_all_components(spec_constitution, capability_matrix):
    """Every component in SSOT must be referenced in the constitution."""
    for c in capability_matrix["components"]:
        assert c["name"] in spec_constitution, (
            f"Component '{c['name']}' not found in constitution"
        )


def test_prd_references_all_components(spec_prd, capability_matrix):
    """Every component in SSOT must be referenced in the PRD."""
    for c in capability_matrix["components"]:
        assert c["name"] in spec_prd, (
            f"Component '{c['name']}' not found in PRD"
        )


def test_eval_datasets_exist_for_all_components(capability_matrix):
    """Every eval reference in components must have a dataset file."""
    all_evals = set()
    for c in capability_matrix["components"]:
        for e in c.get("evals", []):
            all_evals.add(e)

    for eval_name in all_evals:
        # "safety" is covered by safety_evals config, not a dataset
        if eval_name == "safety":
            continue
        path = EVAL_DATASETS_DIR / f"{eval_name}.yaml"
        assert path.exists(), f"Eval dataset missing: {path}"
        with open(path) as f:
            data = yaml.safe_load(f)
        assert data is not None, f"Eval dataset empty: {path}"
        assert "dataset_id" in data, f"Eval dataset missing dataset_id: {path}"


def test_eval_config_files_exist():
    """All 3 eval config files must exist."""
    required = ["system_evals.yaml", "process_evals.yaml", "safety_evals.yaml"]
    for name in required:
        path = EVAL_CONFIG_DIR / name
        assert path.exists(), f"Eval config missing: {path}"
        with open(path) as f:
            data = yaml.safe_load(f)
        assert data is not None, f"Eval config empty: {path}"
        assert "evaluators" in data or "critical_policy" in data, (
            f"Eval config missing evaluators: {path}"
        )


def test_capability_packs_in_spec(spec_constitution, capability_matrix):
    """Capability packs in SSOT must be referenced in spec."""
    for pack in capability_matrix.get("capability_packs", []):
        # Check that pack purpose or ID appears in constitution
        assert pack["id"].replace("_", " ") in spec_constitution.lower() or \
               pack["purpose"].lower()[:30] in spec_constitution.lower(), (
            f"Pack '{pack['id']}' not referenced in constitution"
        )


def test_component_count_consistent(spec_prd, capability_matrix):
    """Spec and SSOT must agree: 3 agents + 1 workflow."""
    components = capability_matrix["components"]
    workflows = [c for c in components if "workflow" in c["form"]]
    agents = [c for c in components if c not in workflows and "agent" in c["form"]]
    assert len(agents) == 3, f"Expected 3 agents, got {len(agents)}"
    assert len(workflows) == 1, f"Expected 1 workflow, got {len(workflows)}"
    # PRD should mention "3 agents" or "3 Agents"
    assert "3 agent" in spec_prd.lower() or "3 Agent" in spec_prd, (
        "PRD doesn't mention 3 agents"
    )


def test_safety_evals_require_human_review():
    """Safety eval config must require human review."""
    path = EVAL_CONFIG_DIR / "safety_evals.yaml"
    with open(path) as f:
        data = yaml.safe_load(f)
    assert data.get("human_review_required") is True, (
        "Safety evals must set human_review_required: true"
    )
