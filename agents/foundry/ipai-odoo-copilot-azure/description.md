# ipai-odoo-copilot-azure

InsightPulseAI Odoo Copilot deployed on Azure AI Foundry.

## Purpose

Provides AI-assisted compliance, finance operations, and ERP guidance
within the Odoo platform for Philippine business operations.

## Capabilities

- **Compliance Calendar**: BIR filing deadlines, upcoming due dates,
  overdue alerts.
- **Report Helper**: Guidance on VAT, EWT, SLSP, 2307, and related
  Philippine tax forms.
- **Finding/Task Management**: Summarize findings, draft tasks,
  track resolution status.
- **Record Navigation**: Help users find and understand Odoo records.
- **Exception Summaries**: Surface anomalies, overdue items, and
  readiness scores for the control tower.

## Architecture

```
Odoo UI
  -> Odoo Backend Controller
    -> ops-platform Foundry Adapter
      -> Published Foundry Agent Application
        -> Tools / Knowledge / Grounded Responses
```

## Related Documentation

- [Foundry Publishing Model](../../../infra/docs/architecture/FOUNDRY_PUBLISHING_MODEL.md)
- [Publish Policy](./publish-policy.md)
- [Runtime Contract](./runtime-contract.md)
- [Environment Modes](./env-modes.md)
