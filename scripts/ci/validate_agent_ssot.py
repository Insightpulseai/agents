#!/usr/bin/env python3
"""Agent SSOT Validator — InsightPulseAI

Validates agent capability matrix and ingress matrix for consistency.

Checks:
- YAML files parse cleanly
- Required fields present
- Exactly 3 agents + 1 workflow
- APIM is the only production front door
- Playgrounds are non-production
- No disallowed extra top-level agents
- Eval dataset/config files exist
- Component names are consistent

Usage:
    python scripts/ci/validate_agent_ssot.py
"""

import sys
from pathlib import Path

import yaml

CAPABILITY_PATH = Path("infra/ssot/agents/agent_capability_matrix.yaml")
INGRESS_PATH = Path("infra/ssot/platform/agent_ingress_matrix.yaml")
EVAL_DATASETS_DIR = Path("eval/datasets")
EVAL_CONFIG_DIR = Path("eval/config")
SPEC_DIR = Path("spec/odoo-copilot-agent-framework")

EXPECTED_COMPONENTS = {
    "ipai-odoo-copilot-advisory",
    "ipai-odoo-copilot-ops",
    "ipai-odoo-copilot-actions",
    "ipai-odoo-copilot-router",
}

REQUIRED_EVAL_DATASETS = {"advisory", "ops", "actions", "router"}
REQUIRED_EVAL_CONFIGS = {"system_evals", "process_evals", "safety_evals"}
REQUIRED_SPEC_FILES = {"constitution.md", "prd.md", "plan.md", "tasks.md"}


def check(condition: bool, msg: str, errors: list[str]):
    if not condition:
        errors.append(msg)


def validate_capability_matrix(errors: list[str]):
    check(CAPABILITY_PATH.exists(), f"Missing: {CAPABILITY_PATH}", errors)
    if not CAPABILITY_PATH.exists():
        return None

    with open(CAPABILITY_PATH) as f:
        data = yaml.safe_load(f)

    check(data is not None, "Capability matrix is empty", errors)
    if data is None:
        return None

    check("version" in data, "Capability matrix missing version", errors)
    check(
        data.get("system") == "odoo_copilot_foundry",
        f"System must be 'odoo_copilot_foundry', got '{data.get('system')}'",
        errors,
    )

    components = data.get("components", [])
    check(len(components) == 4, f"Expected 4 components, got {len(components)}", errors)

    names = {c["name"] for c in components}
    check(
        names == EXPECTED_COMPONENTS,
        f"Components mismatch. Expected {EXPECTED_COMPONENTS}, got {names}",
        errors,
    )

    extra = names - EXPECTED_COMPONENTS
    check(not extra, f"Disallowed extra agents: {extra}", errors)

    for c in components:
        check(
            "allowed_actions" in c,
            f"Component '{c['name']}' missing allowed_actions",
            errors,
        )
        check(
            "blocked_actions" in c,
            f"Component '{c['name']}' missing blocked_actions",
            errors,
        )
        check(
            "evals" in c,
            f"Component '{c['name']}' missing evals",
            errors,
        )

    # Router must be workflow
    for c in components:
        if c["name"] == "ipai-odoo-copilot-router":
            check(
                c.get("form") == "agent_framework_workflow",
                f"Router must be workflow, got '{c.get('form')}'",
                errors,
            )

    # Actions must have safety requirements
    for c in components:
        if c["name"] == "ipai-odoo-copilot-actions":
            check(
                "safety_requirements" in c,
                "Actions agent missing safety_requirements",
                errors,
            )

    return data


def validate_ingress_matrix(errors: list[str]):
    check(INGRESS_PATH.exists(), f"Missing: {INGRESS_PATH}", errors)
    if not INGRESS_PATH.exists():
        return None

    with open(INGRESS_PATH) as f:
        data = yaml.safe_load(f)

    check(data is not None, "Ingress matrix is empty", errors)
    if data is None:
        return None

    check("version" in data, "Ingress matrix missing version", errors)

    # APIM must be production
    ingress = data.get("ingress", {})
    prod = ingress.get("production", {})
    check(
        prod.get("is_production") is True,
        "Production ingress must have is_production: true",
        errors,
    )

    # Playground must be non-production
    playground = ingress.get("playground", {})
    check(
        playground.get("is_production") is False,
        "Playground must have is_production: false",
        errors,
    )

    surfaces = data.get("surfaces", [])
    check(len(surfaces) > 0, "No surfaces defined in ingress matrix", errors)

    return data


def validate_eval_artifacts(errors: list[str]):
    for name in REQUIRED_EVAL_DATASETS:
        path = EVAL_DATASETS_DIR / f"{name}.yaml"
        check(path.exists(), f"Missing eval dataset: {path}", errors)

    for name in REQUIRED_EVAL_CONFIGS:
        path = EVAL_CONFIG_DIR / f"{name}.yaml"
        check(path.exists(), f"Missing eval config: {path}", errors)


def validate_spec_bundle(errors: list[str]):
    for name in REQUIRED_SPEC_FILES:
        path = SPEC_DIR / name
        check(path.exists(), f"Missing spec file: {path}", errors)


def main():
    errors: list[str] = []

    print("Validating agent SSOT...")
    validate_capability_matrix(errors)
    validate_ingress_matrix(errors)
    validate_eval_artifacts(errors)
    validate_spec_bundle(errors)

    if errors:
        print(f"\nFAIL: {len(errors)} error(s)")
        for e in errors:
            print(f"  ERROR: {e}")
        sys.exit(1)
    else:
        print("\nPASS: Agent SSOT validation complete.")
        sys.exit(0)


if __name__ == "__main__":
    main()
