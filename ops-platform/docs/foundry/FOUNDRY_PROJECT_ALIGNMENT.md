# FOUNDRY_PROJECT_ALIGNMENT.md

## Purpose

Defines the canonical alignment between the Azure AI Foundry portal state
and the repo-backed source of truth.

---

## Current Foundry project

| Property | Value |
|---|---|
| Project name | `data-intel-ph` |
| Resource group | `rg-data-intel-ph` |
| Account/resource | `data-intel-ph-resource` |
| Project endpoint | `https://data-intel-ph-resource.services.ai.azure.com/api/projects/data-intel-ph` |
| Resource endpoint | `https://data-intel-ph-resource.services.ai.azure.com/` |
| OpenAI endpoint | `https://data-intel-ph-resource.openai.azure.com/` |

---

## Agents

| Agent | Type | Status |
|---|---|---|
| `ipai-odoo-copilot-azure` | prompt | active |

Repo mirror: `agents/foundry/agents/ipai-odoo-copilot-azure/agent.manifest.yaml`

---

## Model deployments

| Deployment | Kind | Repo mirror |
|---|---|---|
| `gpt-4.1` | chat | `ops-platform/ssot/foundry/model-deployments.yaml` |
| `text-embedding-3-small` | embeddings | `ops-platform/ssot/foundry/model-deployments.yaml` |

---

## Tools

| Tool | Type | Owner repo |
|---|---|---|
| `srchipaidev8tlstu` | Azure AI Search | `infra` |

Repo mirror: `ops-platform/ssot/foundry/tools.yaml`

---

## Guardrails

| Guardrail | Source |
|---|---|
| `ipai-odoo-copilot-guardrail` | Custom — repo-backed |
| `Microsoft.Default` | Platform default |
| `Microsoft.DefaultV2` | Platform default v2 |

Repo mirror: `ops-platform/ssot/foundry/guardrails.yaml`

---

## Sync doctrine

1. Every portal-created agent must have a repo-backed `agent.manifest.yaml`.
2. Every model deployment must appear in `ops-platform/ssot/foundry/model-deployments.yaml`.
3. Every tool attachment must appear in `ops-platform/ssot/foundry/tools.yaml`.
4. Every custom guardrail must appear in `ops-platform/ssot/foundry/guardrails.yaml`.
5. Knowledge source files must be source-controlled in `agents/foundry/knowledge/`.
6. CI validators (`validate_ssot.py`) enforce cross-reference integrity.

---

## Drift detection

The CI workflow `.github/workflows/ssot-platform-check.yml` runs on every
push and PR to main. It validates:

- all required SSOT files exist
- all five canonical repos are declared in `repo-ownership.yaml`
- model deployments referenced by projects exist in the model inventory
- tools referenced by projects exist in the tool inventory
- ownership boundaries are not violated
