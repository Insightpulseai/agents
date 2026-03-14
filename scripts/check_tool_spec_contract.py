#!/usr/bin/env python3
"""Tool Spec Contract Gate — InsightPulseAI

Validates that every tool registered in the agent capability manifest
has a corresponding spec file and meets minimum requirements.

Gate ID: tool_spec_contract_gate
Blocks: E-FND-02

Usage:
    python scripts/check_tool_spec_contract.py [--strict]
"""

import json
import sys
from pathlib import Path

MANIFEST_PATH = Path("infra/ssot/agents/capability_manifest.json")
CONTRACTS_DIR = Path("contracts/tools")
TEMPLATE_PATH = CONTRACTS_DIR / "TOOL_SPEC_TEMPLATE.md"

REQUIRED_SECTIONS = [
    "Tool Name",
    "Endpoint",
    "Auth",
    "Input Schema",
    "Output Schema",
    "Scope",
    "Guardrails",
]


def load_manifest() -> dict:
    if not MANIFEST_PATH.exists():
        print(f"FAIL: Manifest not found at {MANIFEST_PATH}")
        sys.exit(1)
    with open(MANIFEST_PATH) as f:
        return json.load(f)


def check_template_exists() -> bool:
    if not TEMPLATE_PATH.exists():
        print(f"WARN: Template not found at {TEMPLATE_PATH}")
        return False
    return True


def check_tool_specs(manifest: dict, strict: bool = False) -> list[str]:
    errors = []
    agents = manifest.get("agents", [])

    for agent in agents:
        agent_id = agent.get("id", "unknown")
        tools_connected = agent.get("tools_connected", [])

        for tool in tools_connected:
            spec_path = CONTRACTS_DIR / f"{tool}.md"
            if not spec_path.exists():
                msg = f"{agent_id}: tool '{tool}' has no spec at {spec_path}"
                if strict:
                    errors.append(msg)
                else:
                    print(f"WARN: {msg}")
                continue

            # Check required sections
            content = spec_path.read_text()
            for section in REQUIRED_SECTIONS:
                if f"## {section}" not in content:
                    msg = f"{agent_id}: tool '{tool}' spec missing section '## {section}'"
                    if strict:
                        errors.append(msg)
                    else:
                        print(f"WARN: {msg}")

    return errors


def main():
    strict = "--strict" in sys.argv
    manifest = load_manifest()
    template_ok = check_template_exists()
    errors = check_tool_specs(manifest, strict=strict)

    # Summary
    agents = manifest.get("agents", [])
    total_tools = sum(len(a.get("tools_connected", [])) for a in agents)
    total_missing = sum(len(a.get("tools_missing", [])) for a in agents)

    print(f"\n--- Tool Spec Contract Gate ---")
    print(f"Agents: {len(agents)}")
    print(f"Tools connected: {total_tools}")
    print(f"Tools missing (not yet connected): {total_missing}")
    print(f"Template exists: {template_ok}")
    print(f"Errors: {len(errors)}")

    if errors:
        print("\nFAILURES:")
        for e in errors:
            print(f"  FAIL: {e}")
        sys.exit(1)
    else:
        print("\nPASS: Tool spec contract gate satisfied.")
        sys.exit(0)


if __name__ == "__main__":
    main()
