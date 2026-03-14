# Foundry Adapter

Server-side adapter for invoking the published `ipai-odoo-copilot-azure` Agent Application.

## Responsibilities

- Attach tenant/user/session context to requests
- Enforce environment mode policy (PROD-ADVISORY blocks writes)
- Require confirmation for PROD-ACTION write requests
- Write audit events for every request
- Call the Responses API against the published Agent Application
- Return safe responses to the Odoo bridge

## Authentication

Uses `DefaultAzureCredential` (Entra ID / Azure identity).
No API keys in application code or browser-side secrets.

## Running locally

```bash
pip install -e .
export FOUNDRY_AGENT_APP_RESPONSES_ENDPOINT="https://..."
uvicorn foundry_adapter.service:app --reload
```

## Environment variables

| Variable | Description |
|----------|-------------|
| `FOUNDRY_AGENT_APP_RESPONSES_ENDPOINT` | Stable endpoint URL of the published Agent Application |
