# Skill: Azure AI Foundry — Hosted Agent Workflows (VS Code Pro-Code)

source: https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/vs-code-agents-workflow-pro-code
extracted: 2026-03-15
applies-to: agents, infra

## What it is

Azure AI Foundry for VS Code extension enables building, running, visualizing, and deploying multi-agent workflows ("hosted agents"). Each agent in the workflow has its own model, tools, and instructions.

## When to use (decision matrix)

| Scenario | Use Foundry Hosted Agents | Use IPAI Agent Framework |
|----------|--------------------------|--------------------------|
| Tight Azure-native integration needed | Yes | No |
| Vendor-agnostic, Supabase-SSOT-anchored | No | Yes |
| Reference architecture study | Yes (patterns only) | N/A |
| Production multi-agent orchestration | Evaluate | Primary |

## Key Setup Steps (Python path)

### 1. Project scaffolding
```
Ctrl+Shift+P → "Microsoft Foundry: Create a New Hosted Agent"
→ Scaffolds workflow.py + .env template
```

### 2. Framework install
```bash
python -m venv .venv && source .venv/bin/activate
pip install azure-ai-agentserver-agentframework
```

### 3. Environment configuration (.env — never commit)
```
AZURE_AI_PROJECT_ENDPOINT=https://<resource>.services.ai.azure.com/api/projects/<project>
AZURE_AI_MODEL_DEPLOYMENT_NAME=<deployment>
```

### 4. Authentication
- Local dev: `DefaultAzureCredential` via `az login` or VS Code account
- CI: Service principal env vars (`AZURE_TENANT_ID`, `AZURE_CLIENT_ID`, `AZURE_CLIENT_SECRET`)
- Maps to existing ACA service principal pattern in `rg-ipai-dev`

### 5. Run modes

| Mode | How |
|------|-----|
| Interactive (debug) | F5 → HTTP server + AI Toolkit Agent Inspector |
| Container mode | Command palette → Open Container Agent Playground Locally → run main.py |

### 6. Observability
```python
from agent_framework.observability import setup_observability
setup_observability(vs_code_extension_port=4319)
```
- Visualizer: `Ctrl+Shift+P → "Microsoft Foundry: Open Visualizer for Hosted Agents"`
- Live execution graph of agent interactions
- Sensitive data tracing (local only): `enable_sensitive_data=True`
- OTLP on port 4319: watch for conflicts with n8n/Supabase stack locally

### 7. Deployment
```
Command palette → "Microsoft Foundry: Deploy Hosted Agent"
→ Specify container.py as entry
→ Appears under Hosted Agents (Preview) in extension tree
```

## IPAI Infrastructure Notes

- **Managed identity roles**: Foundry project needs `Azure AI User` + `AcrPull` on `rg-ipai-dev` / `rg-ipai-ai-dev`
- **Region**: Hosted agents require a supported region — confirm SEA availability before architecting
- **OTLP port**: Override via `FOUNDRY_OTLP_PORT` if conflicting with existing local services

## SSOT/SOR Mapping

- Foundry is NOT SSOT — it is a compute/orchestration layer
- Agent run state → `ops.runs` + `ops.run_events` (Supabase SSOT)
- Model deployments tracked in `ops.model_registry`
- Foundry project config stored in `infra/` as Bicep/Terraform

## Verdict

This is Microsoft's hosted alternative to the IPAI n8n + Claude multi-agent pattern. Tighter Azure integration but less portable (Foundry-coupled, no self-hosted option). Use as reference architecture for agent sequencing, observability patterns, and OTLP tracing — not for wholesale adoption.

## Cross-references

- Microsoft Agent Framework: `skills/azure/microsoft-agent-framework.md`
- Agentic SDLC constitution: `agents/system/agentic-sdlc-constitution.md`
