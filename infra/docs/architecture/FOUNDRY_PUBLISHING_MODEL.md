# Foundry Publishing Model

## Overview

This document describes how Foundry agents are published and consumed
in the InsightPulseAI platform.

## Publish lifecycle

```
Build → Save Version → Trace → Evaluate → Publish Agent Application
```

## Consumption model

Published Agent Applications expose a stable endpoint.
Backend adapters invoke this endpoint using the Responses API.

```
Odoo UI
  → Odoo bridge controller
    → Backend adapter (FastAPI)
      → Published Agent Application (Responses API)
```

## Authentication

- Backend adapter uses `DefaultAzureCredential` (Entra ID)
- No API keys in application code
- No direct browser-to-Foundry privileged access

## Environment modes

| Mode | Purpose | Write allowed |
|------|---------|---------------|
| BUILD | Sandbox iteration | Yes (no audit) |
| STAGING | Integration validation | Yes (audited) |
| PROD-ADVISORY | Production read-first | No |
| PROD-ACTION | Production confirmed writes | Yes (confirmed + audited) |

## Related files

- `agents/foundry/ipai-odoo-copilot-azure/` — agent contract
- `ops-platform/adapters/foundry/` — backend adapter
- `odoo/addons/ipai_odoo_copilot_bridge/` — Odoo bridge module
