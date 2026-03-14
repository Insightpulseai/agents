"""Contract tests for repo ownership boundaries.

These tests validate the structural invariants that CI must enforce:
- Repos own what they should own
- Repos do NOT own what they should not own
- Cross-repo references are consistent
"""
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]


def load_yaml(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def test_foundry_split():
    """Foundry ownership: lakehouse has no prompt agents, agents owns manifests, infra owns search."""
    ownership = load_yaml(ROOT / "ssot/platform/repo-ownership.yaml")
    repo_map = {r["name"]: r for r in ownership["repos"]}

    assert "prompt_agents" in repo_map["lakehouse"]["must_not_own"]
    assert "agent_manifests" in repo_map["agents"]["owns"]
    assert "search_iac" in repo_map["infra"]["owns"]


def test_odoo_boundaries():
    """Odoo owns ERP runtime and bridge but not infra or org policy."""
    ownership = load_yaml(ROOT / "ssot/platform/repo-ownership.yaml")
    repo_map = {r["name"]: r for r in ownership["repos"]}

    odoo = repo_map["odoo"]
    assert "odoo_runtime" in odoo["owns"]
    assert "odoo_ai_bridge" in odoo["owns"]
    assert "apim_gateway" in odoo["must_not_own"]
    assert "frontdoor_iac" in odoo["must_not_own"]


def test_ops_platform_boundaries():
    """ops-platform owns inventories and policy, not runtime code."""
    ownership = load_yaml(ROOT / "ssot/platform/repo-ownership.yaml")
    repo_map = {r["name"]: r for r in ownership["repos"]}

    ops = repo_map["ops-platform"]
    assert "foundry_inventory" in ops["owns"]
    assert "policy_docs" in ops["owns"]
    assert "workload_runtime_code" in ops["must_not_own"]


def test_infra_boundaries():
    """infra owns all IaC, not prompts or medallion logic."""
    ownership = load_yaml(ROOT / "ssot/platform/repo-ownership.yaml")
    repo_map = {r["name"]: r for r in ownership["repos"]}

    infra = repo_map["infra"]
    assert "azure_iac" in infra["owns"]
    assert "apim" in infra["owns"]
    assert "frontdoor" in infra["owns"]
    assert "search_iac" in infra["owns"]
    assert "prompts" in infra["must_not_own"]


def test_all_five_repos_present():
    """All five canonical repos must be declared."""
    ownership = load_yaml(ROOT / "ssot/platform/repo-ownership.yaml")
    names = {r["name"] for r in ownership["repos"]}
    assert names == {"odoo", "agents", "ops-platform", "infra", "lakehouse"}


def test_foundry_project_references_valid_models():
    """Every model deployment referenced by a Foundry project must exist in model-deployments.yaml."""
    projects = load_yaml(ROOT / "ssot/foundry/project-inventory.yaml")
    models = load_yaml(ROOT / "ssot/foundry/model-deployments.yaml")

    known = {m["name"] for m in models.get("model_deployments", [])}
    for proj in projects.get("foundry_projects", []):
        for dep in proj.get("model_deployments", []):
            assert dep in known, f"unknown model deployment: {dep}"


def test_foundry_project_references_valid_tools():
    """Every tool referenced by a Foundry project must exist in tools.yaml."""
    projects = load_yaml(ROOT / "ssot/foundry/project-inventory.yaml")
    tools = load_yaml(ROOT / "ssot/foundry/tools.yaml")

    known = {t["name"] for t in tools.get("tools", [])}
    for proj in projects.get("foundry_projects", []):
        for tool in proj.get("tools", []):
            assert tool in known, f"unknown tool: {tool}"


def test_foundry_project_references_valid_guardrails():
    """Every guardrail referenced by a Foundry project must exist in guardrails.yaml."""
    projects = load_yaml(ROOT / "ssot/foundry/project-inventory.yaml")
    guardrails = load_yaml(ROOT / "ssot/foundry/guardrails.yaml")

    known = {g["name"] for g in guardrails.get("guardrails", [])}
    for proj in projects.get("foundry_projects", []):
        for gr in proj.get("guardrails", []):
            assert gr in known, f"unknown guardrail: {gr}"


def test_knowledge_assets_have_source_paths():
    """Every knowledge asset must declare a source_path."""
    knowledge = load_yaml(ROOT / "ssot/foundry/knowledge-assets.yaml")
    for asset in knowledge.get("knowledge_assets", []):
        assert asset.get("source_path"), f"knowledge asset '{asset.get('name')}' missing source_path"


def test_knowledge_assets_reference_valid_agents():
    """Every agent referenced by a knowledge asset must exist in project inventory."""
    projects = load_yaml(ROOT / "ssot/foundry/project-inventory.yaml")
    knowledge = load_yaml(ROOT / "ssot/foundry/knowledge-assets.yaml")

    known_agents = set()
    for proj in projects.get("foundry_projects", []):
        known_agents.update(proj.get("agents", []))

    for asset in knowledge.get("knowledge_assets", []):
        for agent in asset.get("consumed_by_agents", []):
            assert agent in known_agents, f"unknown agent in knowledge asset: {agent}"
