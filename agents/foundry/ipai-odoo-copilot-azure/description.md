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

## Target Azure AI Capabilities

This copilot leverages or targets the following Azure AI platform services:

| Status | Capability | Azure Service | Use Case |
|--------|-----------|---------------|----------|
| Active | Agent Application Publish | AI Foundry | Core runtime |
| Active | GenAIOps Pipeline | AI Foundry | CI/CD, eval, staging soak |
| Active | Knowledge Mining | AI Search | RAG compliance knowledge base |
| Planned | Document Intelligence | Document Intelligence | BIR form extraction, invoice OCR |
| Planned | Text Analysis | Language MCP Server | Compliance document NLP |
| Planned | Computer Vision | AI Vision | Receipt/invoice image processing |
| Planned | Multimodal Analysis | Content Understanding | Audit evidence verification |
| Planned | Agent Optimization | AI Foundry | Production latency/quality |
| Future | Speech Agent | Speech MCP Server | Voice-driven copilot |
| Future | Fine-Tuning | AI Foundry | Domain-specific PH compliance model |
| Future | Video Generation | AI Foundry | Training video auto-generation |
| Future | Teams Integration | M365 | Teams channel distribution |

Full inventory: [`agents/capabilities/azure_ai_target.yaml`](../../capabilities/azure_ai_target.yaml)
Certification alignment: [`agents/capabilities/certifications_alignment.yaml`](../../capabilities/certifications_alignment.yaml)

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
