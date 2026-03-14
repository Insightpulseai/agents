"""Tests for consistency between spec documents and SSOT YAMLs."""
import yaml
import pytest
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
MATRIX_PATH = REPO_ROOT / "infra" / "ssot" / "agents" / "agent_capability_matrix.yaml"
INGRESS_PATH = REPO_ROOT / "infra" / "ssot" / "platform" / "agent_ingress_matrix.yaml"
SPEC_DIR = REPO_ROOT / "spec" / "odoo-copilot-agent-framework"
EVAL_DIR = REPO_ROOT / "eval"


@pytest.fixture
def matrix():
    with open(MATRIX_PATH) as f:
        return yaml.safe_load(f)


@pytest.fixture
def ingress():
    with open(INGRESS_PATH) as f:
        return yaml.safe_load(f)


def test_spec_files_exist():
    """All spec bundle files must exist."""
    required = ["constitution.md", "prd.md", "plan.md", "tasks.md"]
    for filename in required:
        path = SPEC_DIR / filename
        assert path.exists(), f"Missing spec file: {path}"


def test_tax_pulse_spec_exists():
    """Tax pulse sub-agent spec must exist."""
    tp_dir = REPO_ROOT / "spec" / "tax-pulse-sub-agent"
    required = ["constitution.md", "prd.md", "plan.md", "tasks.md"]
    for filename in required:
        path = tp_dir / filename
        assert path.exists(), f"Missing tax-pulse spec: {path}"


def test_eval_datasets_exist():
    """Eval datasets for all 4 components must exist."""
    dataset_dir = EVAL_DIR / "datasets"
    required = ["advisory.yaml", "ops.yaml", "actions.yaml", "router.yaml"]
    for filename in required:
        path = dataset_dir / filename
        assert path.exists(), f"Missing eval dataset: {path}"


def test_eval_configs_exist():
    """Eval config files must exist."""
    config_dir = EVAL_DIR / "config"
    required = ["system_evals.yaml", "process_evals.yaml", "safety_evals.yaml"]
    for filename in required:
        path = config_dir / filename
        assert path.exists(), f"Missing eval config: {path}"


def test_eval_datasets_parse():
    """All eval dataset files must parse as valid YAML."""
    dataset_dir = EVAL_DIR / "datasets"
    for yaml_file in dataset_dir.glob("*.yaml"):
        with open(yaml_file) as f:
            data = yaml.safe_load(f)
        assert data is not None, f"{yaml_file} failed to parse"


def test_eval_configs_parse():
    """All eval config files must parse as valid YAML."""
    config_dir = EVAL_DIR / "config"
    for yaml_file in config_dir.glob("*.yaml"):
        with open(yaml_file) as f:
            data = yaml.safe_load(f)
        assert data is not None, f"{yaml_file} failed to parse"


def test_matrix_components_in_spec(matrix):
    """Every component in SSOT must be referenced in spec PRD."""
    prd_path = SPEC_DIR / "prd.md"
    prd_content = prd_path.read_text()
    for comp in matrix["components"]:
        assert comp["name"] in prd_content, f"{comp['name']} not found in PRD"


def test_ingress_paths_in_spec(ingress):
    """Key ingress paths must be referenced in spec plan."""
    plan_path = SPEC_DIR / "plan.md"
    plan_content = plan_path.read_text()
    key_paths = ["Foundry Project Client", "OpenAI-compatible client", "APIM", "Foundry Playgrounds"]
    for path_name in key_paths:
        assert path_name in plan_content, f"Ingress path '{path_name}' not found in plan"


def test_no_deprecated_web_paths():
    """No references to deprecated web-owned SSOT paths."""
    deprecated_patterns = [
        "infra/ssot/microsoft_cloud",
        "infra/ssot/roadmap",
        "infra/ssot/ai/",
        "infra/ssot/parity",
        "infra/ssot/ee_parity",
    ]
    for yaml_file in [MATRIX_PATH, INGRESS_PATH]:
        content = yaml_file.read_text()
        for pattern in deprecated_patterns:
            assert pattern not in content, f"Deprecated path '{pattern}' found in {yaml_file}"


def test_three_agents_one_workflow(matrix):
    """Exactly 3 agents and 1 workflow."""
    agents = [c for c in matrix["components"] if "workflow" not in c["form"]]
    workflows = [c for c in matrix["components"] if "workflow" in c["form"]]
    assert len(agents) == 3, f"Expected 3 agents, got {len(agents)}"
    assert len(workflows) == 1, f"Expected 1 workflow, got {len(workflows)}"


def test_training_artifacts_exist():
    """BIR SFT training artifacts must exist."""
    training_dir = EVAL_DIR / "training"
    required = ["bir_sft_catalog.yaml", "README_bir_sft.md"]
    for filename in required:
        path = training_dir / filename
        assert path.exists(), f"Missing training artifact: {path}"
