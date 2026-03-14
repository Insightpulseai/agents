"""Validate SSOT YAML files for structural integrity and cross-reference consistency.

Exit 0 on success, 1 on any validation error.
Designed to run in CI via: python ops-platform/scripts/validate_ssot.py
"""
from __future__ import annotations

from pathlib import Path
import sys
import yaml

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    ROOT / "ssot/platform/repo-ownership.yaml",
    ROOT / "ssot/foundry/project-inventory.yaml",
    ROOT / "ssot/foundry/model-deployments.yaml",
    ROOT / "ssot/foundry/tools.yaml",
]


def load_yaml(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def validate_required_files() -> list[str]:
    errors: list[str] = []
    for path in REQUIRED_FILES:
        if not path.exists():
            errors.append(f"missing required file: {path}")
    return errors


def validate_repo_ownership(data: dict) -> list[str]:
    errors: list[str] = []
    repos = data.get("repos", [])
    names = {r.get("name") for r in repos}
    required = {"odoo", "agents", "ops-platform", "infra", "lakehouse"}
    missing = required - names
    if missing:
        errors.append(f"missing repos in repo-ownership.yaml: {sorted(missing)}")
    return errors


def validate_foundry_inventory(
    projects: dict, models: dict, tools: dict
) -> list[str]:
    errors: list[str] = []

    project_list = projects.get("foundry_projects", [])
    if not project_list:
        return ["no foundry_projects defined"]

    known_model_names = {m["name"] for m in models.get("model_deployments", [])}
    known_tool_names = {t["name"] for t in tools.get("tools", [])}

    for proj in project_list:
        for model_name in proj.get("model_deployments", []):
            if model_name not in known_model_names:
                errors.append(
                    f"unknown model deployment referenced by project: {model_name}"
                )
        for tool_name in proj.get("tools", []):
            if tool_name not in known_tool_names:
                errors.append(
                    f"unknown tool referenced by project: {tool_name}"
                )

    return errors


def main() -> int:
    errors = validate_required_files()
    if errors:
        print("\n".join(errors))
        return 1

    repo_ownership = load_yaml(ROOT / "ssot/platform/repo-ownership.yaml")
    projects = load_yaml(ROOT / "ssot/foundry/project-inventory.yaml")
    models = load_yaml(ROOT / "ssot/foundry/model-deployments.yaml")
    tools = load_yaml(ROOT / "ssot/foundry/tools.yaml")

    errors.extend(validate_repo_ownership(repo_ownership))
    errors.extend(validate_foundry_inventory(projects, models, tools))

    if errors:
        print("\n".join(errors))
        return 1

    print("SSOT validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
