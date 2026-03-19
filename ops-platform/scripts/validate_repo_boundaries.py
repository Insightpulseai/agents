"""Validate repo ownership boundaries — fail if any repo is missing critical ownership rules.

Exit 0 on success, 1 on any boundary violation.
Designed to run in CI via: python ops-platform/scripts/validate_repo_boundaries.py
"""
from __future__ import annotations

from pathlib import Path
import sys
import yaml

ROOT = Path(__file__).resolve().parents[1]


def load_yaml(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def main() -> int:
    ownership = load_yaml(ROOT / "ssot/platform/repo-ownership.yaml")
    errors: list[str] = []

    repo_map = {r["name"]: r for r in ownership.get("repos", [])}

    # lakehouse must not own prompt agents
    lakehouse = repo_map.get("lakehouse", {})
    if "prompt_agents" not in lakehouse.get("must_not_own", []):
        errors.append("lakehouse must explicitly forbid prompt_agents ownership")

    # agents must own agent_manifests
    agents = repo_map.get("agents", {})
    if "agent_manifests" not in agents.get("owns", []):
        errors.append("agents must own agent_manifests")

    # infra must own search_iac
    infra = repo_map.get("infra", {})
    if "search_iac" not in infra.get("owns", []):
        errors.append("infra must own search_iac")

    # ops-platform must own foundry_inventory
    ops = repo_map.get("ops-platform", {})
    if "foundry_inventory" not in ops.get("owns", []):
        errors.append("ops-platform must own foundry_inventory")

    # odoo must not own apim_gateway
    odoo = repo_map.get("odoo", {})
    if "apim_gateway" not in odoo.get("must_not_own", []):
        errors.append("odoo must explicitly forbid apim_gateway ownership")

    if errors:
        print("\n".join(errors))
        return 1

    print("Repo boundary validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
