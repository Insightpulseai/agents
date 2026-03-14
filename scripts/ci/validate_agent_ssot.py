#!/usr/bin/env python3
"""CI validator for agent SSOT artifacts.

Validates:
- YAML parse integrity
- Required fields and structure
- Component count invariants
- Ingress invariants
- Eval dataset/config existence
"""
import sys
import yaml
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.parent
ERRORS = []


def error(msg: str):
    ERRORS.append(msg)
    print(f"  FAIL: {msg}", file=sys.stderr)


def check(condition: bool, msg: str):
    if not condition:
        error(msg)


def validate_yaml(path: Path) -> dict | None:
    """Parse YAML and return data or None on failure."""
    if not path.exists():
        error(f"File not found: {path}")
        return None
    try:
        with open(path) as f:
            data = yaml.safe_load(f)
        if data is None:
            error(f"Empty YAML: {path}")
        return data
    except yaml.YAMLError as e:
        error(f"YAML parse error in {path}: {e}")
        return None


def validate_capability_matrix():
    print("Validating agent capability matrix...")
    path = REPO_ROOT / "infra" / "ssot" / "agents" / "agent_capability_matrix.yaml"
    data = validate_yaml(path)
    if not data:
        return

    check("version" in data, "capability matrix missing version")
    check(data.get("system") == "odoo_copilot_foundry", "system must be odoo_copilot_foundry")

    components = data.get("components", [])
    check(len(components) == 4, f"Expected 4 components, got {len(components)}")

    names = {c["name"] for c in components}
    expected = {
        "ipai-odoo-copilot-advisory",
        "ipai-odoo-copilot-ops",
        "ipai-odoo-copilot-actions",
        "ipai-odoo-copilot-router",
    }
    check(names == expected, f"Component names mismatch: {names} vs {expected}")

    # Check no vendor-specific agents
    vendor_keywords = ["databricks", "fal", "smartly", "quilt", "lions"]
    for name in names:
        for kw in vendor_keywords:
            check(kw not in name.lower(), f"Vendor-specific agent found: {name}")

    # Check required fields per component
    for comp in components:
        for field in ["form", "purpose", "allowed_actions", "blocked_actions", "evals"]:
            check(field in comp, f"{comp.get('name', '?')} missing {field}")

    # Check router is workflow
    router = next((c for c in components if c["name"] == "ipai-odoo-copilot-router"), None)
    if router:
        check("workflow" in router.get("form", ""), "Router must be workflow form")

    # Check capability packs exist
    check("capability_packs" in data, "Missing capability_packs section")


def validate_ingress_matrix():
    print("Validating agent ingress matrix...")
    path = REPO_ROOT / "infra" / "ssot" / "platform" / "agent_ingress_matrix.yaml"
    data = validate_yaml(path)
    if not data:
        return

    check("version" in data, "ingress matrix missing version")
    check(data.get("system") == "odoo_copilot_foundry", "system must be odoo_copilot_foundry")

    paths = data.get("ingress_paths", [])
    check(len(paths) >= 5, f"Expected >= 5 ingress paths, got {len(paths)}")

    names = {p["name"] for p in paths}
    required = {"foundry_project_client", "openai_compatible_client", "direct_rest", "apim_ai_gateway", "foundry_playgrounds"}
    check(required.issubset(names), f"Missing ingress paths: {required - names}")

    # APIM must be production
    apim = next((p for p in paths if p["name"] == "apim_ai_gateway"), None)
    if apim:
        check(apim.get("production") is True, "APIM must be marked production=true")

    # Playgrounds must not be production
    playgrounds = next((p for p in paths if p["name"] == "foundry_playgrounds"), None)
    if playgrounds:
        check(playgrounds.get("production") is False, "Playgrounds must be marked production=false")


def validate_eval_artifacts():
    print("Validating eval artifacts...")
    eval_dir = REPO_ROOT / "eval"

    # Datasets
    for name in ["advisory", "ops", "actions", "router"]:
        path = eval_dir / "datasets" / f"{name}.yaml"
        check(path.exists(), f"Missing eval dataset: {path}")
        if path.exists():
            validate_yaml(path)

    # Configs
    for name in ["system_evals", "process_evals", "safety_evals"]:
        path = eval_dir / "config" / f"{name}.yaml"
        check(path.exists(), f"Missing eval config: {path}")
        if path.exists():
            validate_yaml(path)

    # Training catalog
    catalog_path = eval_dir / "training" / "bir_sft_catalog.yaml"
    check(catalog_path.exists(), f"Missing training catalog: {catalog_path}")
    if catalog_path.exists():
        validate_yaml(catalog_path)


def validate_spec_files():
    print("Validating spec files...")
    spec_dir = REPO_ROOT / "spec" / "odoo-copilot-agent-framework"
    for name in ["constitution.md", "prd.md", "plan.md", "tasks.md"]:
        path = spec_dir / name
        check(path.exists(), f"Missing spec file: {path}")

    tp_dir = REPO_ROOT / "spec" / "tax-pulse-sub-agent"
    for name in ["constitution.md", "prd.md", "plan.md", "tasks.md"]:
        path = tp_dir / name
        check(path.exists(), f"Missing tax-pulse spec: {path}")


def main():
    print("=" * 60)
    print("Agent SSOT Validation")
    print("=" * 60)

    validate_capability_matrix()
    validate_ingress_matrix()
    validate_eval_artifacts()
    validate_spec_files()

    print("=" * 60)
    if ERRORS:
        print(f"FAILED: {len(ERRORS)} error(s)")
        for e in ERRORS:
            print(f"  - {e}")
        sys.exit(1)
    else:
        print("PASSED: All validations OK")
        sys.exit(0)


if __name__ == "__main__":
    main()
