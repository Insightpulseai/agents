# Foundry Publishing Model

## Overview

This document describes the deployment lifecycle for AI agents published
through Microsoft Azure AI Foundry, specifically the `ipai-odoo-copilot-azure`
agent used for InsightPulseAI Odoo Copilot.

## Lifecycle Stages

```
Build saved version
  -> Playground test
    -> Traces
      -> Evaluations
        -> Publish Agent Application
          -> Consume from backend
            -> Monitor and republish
```

### 1. Build Saved Version

- Finalize instructions, model selection, tools, and knowledge files.
- Save a named version in Foundry (e.g. `v1.0.0-staging`).

### 2. Playground Test

- Exercise the agent in the Foundry playground against representative queries:
  - Informational: "What are our outstanding VAT filings?"
  - Navigational: "Show me BIR 2307 for Q1 2026"
  - Compliance-calendar: "What deadlines are coming this month?"
  - Dry-run transactional: "Draft a task to reconcile March SLSP"

### 3. Traces

- Enable tracing in Foundry for the saved version.
- Capture request/response pairs, tool invocations, latency, and token usage.
- Review traces for:
  - Correct tool selection
  - Appropriate grounding from knowledge files
  - No hallucinated data or actions

### 4. Evaluations

- Run evaluation sets stored in `agents/foundry/ipai-odoo-copilot-azure/evals/`.
- Minimum pass criteria before publishing:
  - Accuracy >= 90% on compliance-calendar queries
  - No false-positive write recommendations in advisory mode
  - Latency p95 < 8 seconds

### 5. Publish Agent Application

- Publishing creates a stable **Agent Application** endpoint.
- This endpoint is the only production-grade surface. Never treat playground
  URLs as production.
- Use semantic versioning for published versions.

### 6. Consume from Backend

- The published Agent Application is consumed via the **Responses API**.
- Authentication: Entra ID / Azure Managed Identity (never browser-side keys).
- The server-side adapter lives in `ops-platform/adapters/foundry/`.

### 7. Monitor and Republish

- Track: request volume, latency, tool-call count, failures, escalation rate.
- Republish new versions through the same lifecycle when instructions, tools,
  or knowledge change.

## Environment Promotion

| Environment | Agent Application | Backend Adapter | Odoo Instance |
|-------------|-------------------|-----------------|---------------|
| DEV         | Playground only   | Local           | odoo-dev      |
| STAGING     | Published staging | staging adapter | odoo-staging  |
| PROD        | Published prod    | prod adapter    | odoo-prod     |

## Authentication

- Backend-to-Foundry: Azure Managed Identity / Entra ID token.
- Odoo-to-Backend: Internal service auth (session + CSRF or service token).
- Never expose Foundry credentials to the browser.

## Related Files

- `agents/foundry/ipai-odoo-copilot-azure/` — agent definition and policies
- `ops-platform/adapters/foundry/` — backend adapter
- `odoo/addons/ipai_odoo_copilot_bridge/` — Odoo integration module
