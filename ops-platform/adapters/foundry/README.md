# Foundry Adapter

Server-side adapter for invoking the published `ipai-odoo-copilot-azure`
Agent Application.

## Responsibilities

- Attach tenant/user/session context
- Enforce environment mode policy
- Block unsafe direct writes
- Require confirmation for action mode
- Write audit events
- Call the Responses API against the published Agent Application

## Configuration

| Variable | Description |
|----------|-------------|
| `FOUNDRY_AGENT_APP_RESPONSES_ENDPOINT` | Published Agent Application endpoint URL |

## Authentication

Uses `DefaultAzureCredential` (Entra ID / managed identity / workload identity).

## Run

```bash
uvicorn foundry_adapter.service:app --host 0.0.0.0 --port 8100
```
