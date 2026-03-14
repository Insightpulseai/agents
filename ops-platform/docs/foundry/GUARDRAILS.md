# GUARDRAILS.md

## Purpose

Documents the guardrail configuration for Azure AI Foundry agents in the
InsightPulseAI platform.

---

## Current guardrails

### Project: `data-intel-ph`

| Guardrail | Type | Scope |
|---|---|---|
| `ipai-odoo-copilot-guardrail` | Custom | Agent-specific |
| `Microsoft.Default` | Platform | Project-wide |
| `Microsoft.DefaultV2` | Platform | Project-wide |

---

## Custom guardrail: `ipai-odoo-copilot-guardrail`

### Behavioral rules

1. **Grounding required** — All answers must cite sources with document name,
   section, and relevance score.
2. **Confidence threshold** — Answers below 0.5 confidence must trigger
   human escalation, not a guess.
3. **Tenant isolation** — Never cross company boundaries in responses or
   tool invocations.
4. **Write confirmation** — All write operations require explicit user
   confirmation before execution.
5. **No fabrication** — Never fabricate Odoo field names, model names, or
   API endpoints.
6. **Tool-only data access** — All ERP data access must go through the
   Odoo Agent Gateway, never raw database queries.

### Content filters

- Standard Azure content safety filters (hate, self-harm, sexual, violence)
  are enforced via `Microsoft.Default` and `Microsoft.DefaultV2`.
- The custom guardrail adds domain-specific behavioral constraints on top.

---

## Ownership

| Concern | Owner |
|---|---|
| Custom guardrail definition | `ops-platform` (inventory) + `agents` (behavioral spec) |
| Platform guardrails | Microsoft-managed |
| Guardrail inventory YAML | `ops-platform/ssot/foundry/guardrails.yaml` |

---

## Adding a new guardrail

1. Define the guardrail in the Foundry portal.
2. Add it to `ops-platform/ssot/foundry/guardrails.yaml`.
3. Reference it in the agent manifest (`agents/foundry/agents/<agent>/agent.manifest.yaml`).
4. CI will validate the cross-reference on next push.
